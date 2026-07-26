"""Jalur berkas manifest aset, satu per interval (ADR-025).

CACAT KELAS KESEBELAS YANG DIPERBAIKI DI SINI
---------------------------------------------
``runner.muat_konteks`` menulis dan membaca satu nama tetap,
``reports/manifest_aset.json``, apa pun intervalnya. Berkas itu lahir di era 1h
dan memuat tepat dua belas kunci ``ohlcv_1h_*``. Ketika H-013 berjalan di 4h, ia
membaca dua belas berkas ``ohlcv_4h_*``, jadi tidak ada satu nama pun yang
bertemu: gerbang ``checksum`` melaporkan "hilang 12, asing 12, tidak cocok 0".
Dan karena manifest hanya ditulis **bila berkasnya belum ada**, manifest 4h tidak
akan pernah lahir dengan sendirinya.

Akibatnya bukan sekadar satu gerbang merah. Gerbang itu **tidak mungkin lulus**
di 4h, dan gerbang yang tidak mungkin lulus tidak menjaga apa pun: keutuhan dua
belas berkas 4h di balik angka +0,066648R belum pernah terverifikasi sekali pun.
Tidak ada tanda berkas itu rusak; yang tidak ada adalah bukti bahwa ia utuh.

BENTUK YANG DIPILIH, DAN MENGAPA
--------------------------------
Untuk ``1h`` nama berkasnya **tetap** ``manifest_aset.json`` tanpa akhiran. Itu
bukan ketidakkonsistenan yang terlewat, melainkan syarat: manifest 1h yang sudah
dikomit adalah satu-satunya bukti keutuhan data di balik sebelas hipotesis lama,
dan mengganti namanya akan membuat gerbang ``checksum`` pada jalur 1h ikut buta
sehingga seluruh hasil lama berubah status menjadi "tidak dapat dinilai".
Memperbaiki cacat dengan cara melahirkan cacat yang sama di jalur lain bukan
perbaikan.

Modul ini **tidak mengimpor apa pun dari** ``lux.backtest``. Arah impor yang
menutup lingkaran sudah pernah menjadi cacat di proyek ini (``4b77617``), dan
``runner`` yang mengimpor modul ini adalah arah yang benar.
"""

from __future__ import annotations

from pathlib import Path

NAMA_DASAR = "manifest_aset"

# Interval yang memakai nama tanpa akhiran, karena berkasnya sudah dikomit dan
# menjadi rujukan keutuhan data sebelas hipotesis pertama.
INTERVAL_WARISAN = "1h"


def jalur_manifest(interval: str, out: Path | str = Path("reports")) -> Path:
    """Kembalikan jalur manifest untuk satu interval.

    ``1h`` memetakan ke ``manifest_aset.json`` (nama warisan, tidak boleh
    berubah); interval lain ke ``manifest_aset_<interval>.json``.

    Interval kosong ditolak keras alih-alih dijatuhkan ke nama warisan. Bila
    interval hilang karena cacat pemanggil, jatuh diam-diam ke nama 1h berarti
    menulis checksum 4h ke dalam berkas yang menjadi rujukan hasil 1h — merusak
    bukti keutuhan yang justru sedang dijaga.
    """
    iv = str(interval or "").strip()
    if not iv:
        raise ValueError(
            "interval wajib diisi; jatuh diam-diam ke manifest 1h akan "
            "mencemari rujukan keutuhan hasil lama"
        )
    if "/" in iv or "\\" in iv or iv in {".", ".."}:
        raise ValueError(f"interval tidak sah untuk nama berkas: {iv!r}")
    nama = (
        f"{NAMA_DASAR}.json"
        if iv == INTERVAL_WARISAN
        else f"{NAMA_DASAR}_{iv}.json"
    )
    return Path(out) / nama
