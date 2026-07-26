"""Diagnostik geometri keluar (ADR-015 Bagian A).

Gerbang ``invarian_risiko`` gagal di tujuh dari dua belas hipotesis, dan lima
kegagalan pertama terjadi pada semesta tanpa satu pun stablecoin. Karena itu
penjelasan "satuan R runtuh pada simbol degenerat" tidak dapat menjelaskan
kelimanya. Sesuatu yang lain sudah bekerja sejak hipotesis pertama.

Modul ini tidak menjalankan mesin dan tidak memuat satu bar pun. Ia membaca
laporan yang **sudah dikomit** dan membongkar sepuluh perdagangan terburuk
yang tersimpan di ``diagnosa_biaya.terburuk``. Blok itu adalah keluaran
``run_wf.rincian_R`` apa adanya, jadi ia memuat ``alasan`` keluar - medan yang
tidak ada di ``ekor_funding.terburuk``.

Dua besaran yang dihitung di sini:

``R_terlampaui``
    Seberapa jauh kerugian melewati 1R. Mesin selalu mengisi stop tepat di harga
    stop, jadi kerugian di luar 1R tidak boleh berasal dari harga.

``celah_R``
    ``R_terlampaui`` dikurangi biaya yang tercatat. Nilai positif berarti ada
    kerugian yang **tidak dijelaskan** oleh biaya maupun oleh geometri stop, dan
    itulah yang dicurigai ADR-015: keluar karena umur atau carry dinilai pada
    pembukaan bar sebelum stop bar itu diuji, sehingga bar yang menganga
    melewati stop membayar seluruh selisih.

Ambang ``-1.5R`` disalin dari gerbang ``invarian_risiko`` dan **tidak bergerak**.
Diagnostik tidak boleh menjadi jalan keluar bagi hipotesis yang sudah divonis.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

NAMA = "geometri_keluar"

ALASAN_STOP = "stop"

#: Ambang gerbang invarian_risiko. Konstanta acuan, bukan parameter.
AMBANG_INVARIAN_R = -1.5

#: Medan yang wajib ada pada tiap baris ``diagnosa_biaya.terburuk``.
KUNCI_WAJIB: tuple[str, ...] = (
    "symbol",
    "R",
    "kotor_R",
    "transaksi_R",
    "funding_R",
    "stop_frac",
    "jam",
    "alasan",
)


def R_terlampaui(R: float) -> float:
    """Seberapa jauh kerugian melewati 1R. Nol bila tidak melewatinya.

    Perdagangan yang untung mengembalikan nol, bukan angka negatif: yang diukur
    adalah pelampauan, dan laba tidak melampaui apa pun.
    """
    r = float(R)
    if r >= -1.0:
        return 0.0
    return -r - 1.0


def celah_R(R: float, transaksi_R: float, funding_R: float) -> float:
    """Pelampauan yang tidak dijelaskan oleh biaya.

    Sengaja boleh negatif. Membatasinya di nol akan menyembunyikan keadaan di
    mana biaya justru lebih besar dari pelampauan, dan keadaan itu adalah bukti
    yang melawan dugaan ADR-015 - bukti semacam itu harus terlihat.
    """
    return R_terlampaui(R) - (float(transaksi_R) + float(funding_R))


def dari_terburuk(baris: Iterable[Mapping[str, Any]]) -> list[dict]:
    """Bongkar ``diagnosa_biaya.terburuk`` menjadi baris diagnostik.

    Kunci yang hilang menimbulkan ``KeyError``, bukan nilai bawaan. Nol pada
    kolom biaya akan membuat ``celah_R`` tampak besar justru ketika biaya lupa
    dicatat, yakni kesimpulan palsu yang mendukung dugaan saya sendiri.
    """
    keluar: list[dict] = []
    for b in baris:
        kurang = [k for k in KUNCI_WAJIB if k not in b]
        if kurang:
            raise KeyError(
                "baris terburuk wajib memuat kunci "
                + ", ".join(repr(k) for k in kurang)
            )
        R = float(b["R"])
        t = float(b["transaksi_R"])
        f = float(b["funding_R"])
        keluar.append(
            {
                "symbol": str(b["symbol"]),
                "R": R,
                "kotor_R": float(b["kotor_R"]),
                "transaksi_R": t,
                "funding_R": f,
                "stop_frac": float(b["stop_frac"]),
                "jam": float(b["jam"]),
                "alasan": str(b["alasan"]),
                "R_terlampaui": R_terlampaui(R),
                "celah_R": celah_R(R, t, f),
            }
        )
    return keluar


def ringkas(baris: Sequence[Mapping[str, Any]]) -> dict:
    """Ukur tanpa memberi putusan.

    ``ekor_menutup_ambang`` menjawab pertanyaan yang menentukan sah atau tidaknya
    kesimpulan apa pun tentang perdagangan di bawah ambang: bila perdagangan
    paling ringan di dalam ekor masih lebih buruk dari ambang, maka mungkin ada
    perdagangan lain di bawah ambang yang tidak tercatat, dan ekor ini tidak
    cukup untuk menghitungnya.
    """
    n = len(baris)
    if n == 0:
        return {
            "n": 0,
            "dapat_dinilai": False,
            "sebab": "tidak ada perdagangan terburuk di laporan",
            "n_stop": 0,
            "n_bukan_stop": 0,
            "porsi_bukan_stop": None,
            "terburuk": None,
            "pelanggar": [],
            "pelanggar_stop": [],
            "ekor_menutup_ambang": False,
            "median_R_terlampaui": {},
            "ambang": AMBANG_INVARIAN_R,
        }

    n_stop = sum(1 for b in baris if b["alasan"] == ALASAN_STOP)
    pelanggar = [b for b in baris if float(b["R"]) < AMBANG_INVARIAN_R]
    teringan = max(float(b["R"]) for b in baris)

    per_alasan: dict[str, list[float]] = {}
    for b in baris:
        per_alasan.setdefault(str(b["alasan"]), []).append(
            float(b["R_terlampaui"])
        )

    return {
        "n": n,
        "dapat_dinilai": True,
        "sebab": "",
        "n_stop": n_stop,
        "n_bukan_stop": n - n_stop,
        "porsi_bukan_stop": (n - n_stop) / n,
        "terburuk": min(baris, key=lambda b: float(b["R"])),
        "pelanggar": pelanggar,
        "pelanggar_stop": [
            b for b in pelanggar if b["alasan"] == ALASAN_STOP
        ],
        # Ekor menutup ambang bila perdagangan paling ringan di dalamnya sudah
        # di atas ambang: apa pun di bawah ambang mustahil berada di luar ekor.
        "ekor_menutup_ambang": teringan > AMBANG_INVARIAN_R,
        "median_R_terlampaui": {
            a: statistics.median(v) for a, v in sorted(per_alasan.items())
        },
        "ambang": AMBANG_INVARIAN_R,
    }


def adili(r: Mapping[str, Any]) -> list[dict]:
    """Adili empat ramalan Bagian A ADR-015, satu per satu.

    Ramalan 1 diadili sesuai bunyinya di ADR: bila alasan keluar perdagangan
    terburuk ternyata ``stop``, hasilnya bukan sekadar ramalan yang salah
    melainkan **seluruh Bagian A gugur**.
    """
    if not r["dapat_dinilai"]:
        return [
            {
                "ramalan": i,
                "hasil": "TIDAK DAPAT DINILAI",
                "bukti": r["sebab"],
            }
            for i in (1, 2, 3, 4)
        ]

    hasil: list[dict] = []
    t = r["terburuk"]

    if t["alasan"] != ALASAN_STOP:
        hasil.append(
            {
                "ramalan": 1,
                "hasil": "BENAR",
                "bukti": (
                    f"perdagangan terburuk {t['R']:.4f}R pada {t['symbol']} "
                    f"beralasan keluar '{t['alasan']}', bukan '{ALASAN_STOP}'"
                ),
            }
        )
    else:
        hasil.append(
            {
                "ramalan": 1,
                "hasil": "SALAH - BAGIAN A ADR-015 GUGUR",
                "bukti": (
                    f"perdagangan terburuk {t['R']:.4f}R pada {t['symbol']} "
                    f"beralasan keluar '{ALASAN_STOP}', sehingga bar yang "
                    "menganga bukan penjelasannya"
                ),
            }
        )

    if not r["ekor_menutup_ambang"]:
        hasil.append(
            {
                "ramalan": 2,
                "hasil": "TIDAK DAPAT DINILAI",
                "bukti": (
                    "perdagangan teringan di dalam ekor masih di bawah ambang "
                    f"{r['ambang']}R, jadi ekor ini tidak memuat semua "
                    "pelanggar"
                ),
            }
        )
    elif r["pelanggar_stop"]:
        daftar = ", ".join(
            f"{b['symbol']} {b['R']:.4f}R" for b in r["pelanggar_stop"]
        )
        hasil.append(
            {
                "ramalan": 2,
                "hasil": "SALAH",
                "bukti": f"ada keluar '{ALASAN_STOP}' di bawah ambang: {daftar}",
            }
        )
    else:
        hasil.append(
            {
                "ramalan": 2,
                "hasil": "BENAR",
                "bukti": (
                    f"tidak ada keluar '{ALASAN_STOP}' di bawah "
                    f"{r['ambang']}R, dan ekor terbukti memuat semua pelanggar"
                ),
            }
        )

    porsi = r["porsi_bukan_stop"]
    hasil.append(
        {
            "ramalan": 3,
            "hasil": "BENAR" if porsi >= 0.5 else "SALAH",
            "bukti": (
                f"porsi bukan-stop di {r['n']} terburuk = {porsi:.4f} "
                f"({r['n_bukan_stop']} dari {r['n']})"
            ),
        }
    )

    med = r["median_R_terlampaui"].get("umur")
    if med is None:
        hasil.append(
            {
                "ramalan": 4,
                "hasil": "TIDAK DAPAT DINILAI",
                "bukti": "tidak ada keluar 'umur' di dalam ekor",
            }
        )
    else:
        hasil.append(
            {
                "ramalan": 4,
                "hasil": "BENAR" if 0.0 <= med <= 0.10 else "SALAH",
                "bukti": f"median R_terlampaui kelompok 'umur' = {med:.6f}R",
            }
        )

    return hasil


def laporan_md(r: Mapping[str, Any], adjudikasi: Sequence[Mapping[str, Any]]) -> str:
    """Susun laporan markdown. Batas buktinya ditulis, bukan disembunyikan."""
    baris: list[str] = [
        "# Geometri keluar H-012 (ADR-015 Bagian A)",
        "",
        "Dihitung dari laporan yang **sudah dikomit**, bukan dari run baru. "
        "Tidak ada mesin yang dijalankan dan tidak ada angka baru yang "
        "diproduksi bagi hipotesis yang sudah divonis.",
        "",
        f"Ambang gerbang `invarian_risiko`: **{r['ambang']}R**, tidak bergerak.",
        "",
        "## Batas bukti",
        "",
        "Laporan hanya menyimpan **sepuluh** perdagangan terburuk, jadi tidak "
        "semua pertanyaan dapat dijawab darinya. Yang dapat dijawab dengan pasti "
        "adalah pertanyaan tentang perdagangan di bawah ambang, dan itu hanya "
        "bila perdagangan paling ringan di dalam ekor sudah berada di atas "
        "ambang - sebab dengan begitu tidak mungkin ada pelanggar di luar ekor.",
        "",
        f"- Ekor memuat semua pelanggar: **{'ya' if r['ekor_menutup_ambang'] else 'TIDAK'}**",
        "",
    ]

    if not r["dapat_dinilai"]:
        return "\n".join(baris + [f"Tidak dapat dinilai: {r['sebab']}.", ""])

    baris += [
        "## Sepuluh perdagangan terburuk",
        "",
        "| Simbol | R | Alasan | Transaksi R | Funding R | R terlampaui | Celah R | Stop % | Jam |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for b in sorted(r["pelanggar"] + [x for x in [] ], key=lambda x: float(x["R"])):
        pass
    return "\n".join(baris)


def muat(path: str | Path) -> list[dict]:
    """Baca blok ``diagnosa_biaya.terburuk`` dari laporan JSON yang dikomit."""
    isi = json.loads(Path(path).read_text(encoding="utf-8"))
    if "diagnosa_biaya" not in isi:
        raise KeyError("laporan tidak memuat 'diagnosa_biaya'")
    blok = isi["diagnosa_biaya"]
    if "terburuk" not in blok:
        raise KeyError("diagnosa_biaya tidak memuat 'terburuk'")
    return dari_terburuk(blok["terburuk"])


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="lux.analisis.geometri_keluar")
    p.add_argument("--laporan", required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args(argv)

    baris = muat(a.laporan)
    r = ringkas(baris)
    adjudikasi = adili(r)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(laporan_md(r, adjudikasi), encoding="utf-8")
    for h in adjudikasi:
        print(f"ramalan {h['ramalan']}: {h['hasil']} - {h['bukti']}", flush=True)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
