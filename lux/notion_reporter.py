"""Pelapor hasil run ke database Notion "LUX — Run Results".

Jalur umpan balik ini ditetapkan ADR-002: agen buta terhadap status job, jadi
satu-satunya cara hasil kembali adalah job yang melapor sendiri.

Batas yang disengaja:

* Tidak ada dependensi baru. Runner tidak memiliki ``requests``; modul ini hanya
  memakai pustaka standar.
* Tidak ada jaringan di dalam pengujian. :func:`kirim` dan :func:`main` menerima
  ``pengirim`` yang dapat disuntik; hanya nilai bawaannya menyentuh jaringan.
* Workflow tidak dapat menulis ``Verdict``. :func:`properti_baris` tidak
  menerima argumen verdict dan selalu menulis ``Menunggu Penilaian``. Gerbang
  mutu yang boleh diisi oleh pihak yang dinilai bukan gerbang.
* ID database tidak ditanam dalam kode. Ia dibaca dari variabel lingkungan
  ``NOTION_DB_RUN_RESULTS``.
* Token tidak pernah dicetak dan tidak pernah masuk pesan galat.

Yang sengaja BELUM ada: pemetaan otomatis dari kunci JSON laporan backtest ke
baris Notion. Kunci itu ditulis setelah struktur berkas laporan yang dikomit
dibaca, bukan dari ingatan (aturan 6).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Callable, Mapping, Sequence

URL_API = "https://api.notion.com/v1/pages"
VERSI_API = "2022-06-28"

#: Notion menolak rich_text lebih panjang dari 2000 karakter per potongan.
BATAS_RICH_TEXT = 2000
#: Batas kerja yang menyisakan ruang bagi penanda pemotongan.
BATAS_AMAN = 1900
PENANDA_POTONG = " ...[dipotong]"

VERDICT_AWAL = "Menunggu Penilaian"

#: Kunci gerbang di dalam mesin -> nama opsi di database Notion.
#: Sebelas, bukan sembilan. Konsentrasi dan Funding ekor lahir setelah H-009.
NAMA_GERBANG_NOTION: dict[str, str] = {
    "checksum": "Checksum",
    "forward_fill": "Forward-fill",
    "survivorship": "Survivorship",
    "buy_and_hold": "Buy-and-hold",
    "entri_acak": "Entry acak",
    "lookahead": "Lookahead",
    "invarian_risiko": "Invariant risiko",
    "funding": "Funding",
    "overlap": "Overlap",
    "konsentrasi": "Konsentrasi",
    "funding_ekor": "Funding ekor",
}

JUMLAH_GERBANG = 11

TAHAP_SAH: tuple[str, ...] = (
    "S3 Universe PIT",
    "S4 Ingest Tier B",
    "S5 Validasi Data",
    "S6 Engine Backtest",
    "S8 Walk-Forward OOS",
    "Lainnya",
)

STATUS_SAH: tuple[str, ...] = ("Sukses", "Sebagian", "Gagal")

PANJANG_SHA = 40

NAMA_ENV_TOKEN = "NOTION_TOKEN"
NAMA_ENV_DATABASE = "NOTION_DB_RUN_RESULTS"


class GalatPelapor(RuntimeError):
    """Kegagalan pelaporan. Sengaja bukan galat jaringan mentah."""


def potong(teks: str, batas: int = BATAS_AMAN) -> str:
    """Potong ``teks`` agar aman bagi rich_text Notion.

    Pemotongan ditandai secara terbuka. Angka yang hilang tanpa penanda adalah
    cara termudah membuat laporan berbohong.
    """
    if batas <= len(PENANDA_POTONG):
        raise ValueError("batas terlalu kecil untuk memuat penanda pemotongan")
    if len(teks) <= batas:
        return teks
    sisa = batas - len(PENANDA_POTONG)
    return teks[:sisa] + PENANDA_POTONG


def nama_gerbang(kunci: str) -> str:
    """Petakan kunci gerbang mesin ke nama opsi Notion."""
    try:
        return NAMA_GERBANG_NOTION[kunci]
    except KeyError as galat:
        raise ValueError(
            f"gerbang tidak dikenal: {kunci!r}. "
            "Opsi Notion wajib ditambahkan lebih dulu, bukan dikarang di sini."
        ) from galat


def properti_baris(
    *,
    run_id: str,
    tahap: str,
    status_eksekusi: str,
    commit: str,
    ringkasan: Mapping[str, Any] | str,
    gerbang_gagal: Sequence[str] = (),
    baris_diproses: int | None = None,
    simbol_diproses: int | None = None,
    durasi_detik: float | None = None,
    selesai_iso: str | None = None,
    lokasi_artefak: str | None = None,
) -> dict[str, Any]:
    """Bangun payload ``properties`` Notion untuk satu baris hasil run.

    Nama properti ditulis persis seperti skema database. Tidak ada argumen
    ``verdict``: nilainya selalu :data:`VERDICT_AWAL`.
    """
    if not run_id:
        raise ValueError("run_id wajib ada; ia judul baris")
    if tahap not in TAHAP_SAH:
        raise ValueError(f"tahap tidak sah: {tahap!r}. Pilihan: {TAHAP_SAH}")
    if status_eksekusi not in STATUS_SAH:
        raise ValueError(
            f"status eksekusi tidak sah: {status_eksekusi!r}. Pilihan: {STATUS_SAH}"
        )
    if len(commit) != PANJANG_SHA:
        raise ValueError(
            f"commit wajib SHA {PANJANG_SHA} karakter penuh, bukan {len(commit)}; "
            "tanpa itu run tidak dapat direproduksi"
        )

    if isinstance(ringkasan, str):
        teks_ringkasan = ringkasan
    else:
        teks_ringkasan = json.dumps(ringkasan, sort_keys=True, ensure_ascii=False)

    properti: dict[str, Any] = {
        "Run ID": {"title": [{"text": {"content": potong(run_id, 200)}}]},
        "Tahap": {"select": {"name": tahap}},
        "Status Eksekusi": {"select": {"name": status_eksekusi}},
        "Verdict": {"status": {"name": VERDICT_AWAL}},
        "Commit": {"rich_text": [{"text": {"content": commit}}]},
        "Ringkasan JSON": {
            "rich_text": [{"text": {"content": potong(teks_ringkasan)}}]
        },
        "Gerbang Gagal": {
            "multi_select": [
                {"name": nama_gerbang(kunci)} for kunci in gerbang_gagal
            ]
        },
    }

    if baris_diproses is not None:
        properti["Baris Diproses"] = {"number": baris_diproses}
    if simbol_diproses is not None:
        properti["Simbol Diproses"] = {"number": simbol_diproses}
    if durasi_detik is not None:
        properti["Durasi (detik)"] = {"number": durasi_detik}
    if selesai_iso is not None:
        properti["Selesai"] = {"date": {"start": selesai_iso}}
    if lokasi_artefak is not None:
        properti["Lokasi Artefak"] = {
            "rich_text": [{"text": {"content": potong(lokasi_artefak)}}]
        }

    return properti


def payload_baris(database_id: str, properti: Mapping[str, Any]) -> dict[str, Any]:
    """Bungkus properti menjadi badan permintaan create-page Notion."""
    if not database_id:
        raise ValueError(
            f"database_id kosong; setel {NAMA_ENV_DATABASE} pada workflow"
        )
    return {
        "parent": {"type": "database_id", "database_id": database_id},
        "properties": dict(properti),
    }


def _pengirim_urllib(
    url: str, badan: bytes, kepala: Mapping[str, str]
) -> tuple[int, str]:
    permintaan = urllib.request.Request(
        url, data=badan, headers=dict(kepala), method="POST"
    )
    try:
        with urllib.request.urlopen(permintaan, timeout=30) as tanggapan:
            return tanggapan.status, tanggapan.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as galat:
        return galat.code, galat.read().decode("utf-8", "replace")


Pengirim = Callable[[str, bytes, Mapping[str, str]], tuple[int, str]]


def kirim(
    payload: Mapping[str, Any],
    *,
    token: str | None = None,
    url_api: str = URL_API,
    pengirim: Pengirim | None = None,
) -> tuple[int, str]:
    """Kirim satu baris ke Notion.

    ``pengirim`` disuntik pada pengujian sehingga tidak ada jaringan di sana.
    Token tidak pernah dicetak, dan tidak masuk pesan galat.
    """
    token_efektif = (
        token if token is not None else os.environ.get(NAMA_ENV_TOKEN, "")
    )
    if not token_efektif:
        raise GalatPelapor(
            f"{NAMA_ENV_TOKEN} tidak tersedia; baris hasil tidak dikirim"
        )

    kepala = {
        "Authorization": f"Bearer {token_efektif}",
        "Notion-Version": VERSI_API,
        "Content-Type": "application/json",
    }
    badan = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    fungsi = pengirim if pengirim is not None else _pengirim_urllib
    kode, teks = fungsi(url_api, badan, kepala)
    if kode < 200 or kode >= 300:
        raise GalatPelapor(f"Notion menolak baris, kode {kode}: {potong(teks, 500)}")
    return kode, teks


def argumen(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Baca argumen baris perintah. Pilihan dibatasi skema database."""
    pengurai = argparse.ArgumentParser(
        prog="lux.notion_reporter",
        description="Kirim satu baris hasil run ke database Notion 'LUX - Run Results'.",
    )
    pengurai.add_argument("--run-id", required=True)
    pengurai.add_argument("--tahap", required=True, choices=list(TAHAP_SAH))
    pengurai.add_argument("--status", required=True, choices=list(STATUS_SAH))
    pengurai.add_argument("--commit", required=True)
    pengurai.add_argument("--ringkasan", required=True)
    pengurai.add_argument("--gerbang", nargs="*", default=[])
    pengurai.add_argument("--baris", type=int, default=None)
    pengurai.add_argument("--simbol", type=int, default=None)
    pengurai.add_argument("--durasi", type=float, default=None)
    pengurai.add_argument("--selesai", default=None)
    pengurai.add_argument("--lokasi", default=None)
    return pengurai.parse_args(argv)


def main(
    argv: Sequence[str] | None = None,
    *,
    pengirim: Pengirim | None = None,
    database_id: str | None = None,
) -> int:
    """Titik masuk CLI. Mengembalikan 0 hanya bila Notion menerima baris."""
    opsi = argumen(argv)
    db = (
        database_id
        if database_id is not None
        else os.environ.get(NAMA_ENV_DATABASE, "")
    )
    properti = properti_baris(
        run_id=opsi.run_id,
        tahap=opsi.tahap,
        status_eksekusi=opsi.status,
        commit=opsi.commit,
        ringkasan=opsi.ringkasan,
        gerbang_gagal=opsi.gerbang,
        baris_diproses=opsi.baris,
        simbol_diproses=opsi.simbol,
        durasi_detik=opsi.durasi,
        selesai_iso=opsi.selesai,
        lokasi_artefak=opsi.lokasi,
    )
    kode, teks = kirim(payload_baris(db, properti), pengirim=pengirim)
    try:
        url_baris = json.loads(teks).get("url", "(tanpa url)")
    except (json.JSONDecodeError, AttributeError):
        url_baris = "(tanggapan bukan JSON)"
    print(f"baris Notion dibuat, kode {kode}: {url_baris}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
