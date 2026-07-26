"""Sebaran R dan galat baku ekspektasi. Utang yang diakui ADR-013 bagian 7.

H-010 lulus dengan ekspektasi 0,053028R terhadap ambang 0,05R. Laporan yang
dikomit **tidak memuat simpangan baku per perdagangan**, hanya rerata dan
sepuluh terburuk, sehingga tidak ada cara mengetahui apakah 0,053028 berbeda
secara berarti dari 0,041359 milik H-009 atau dari ambangnya sendiri. Kekurangan
itu membuat seluruh papan skor sepuluh hipotesis tidak dapat dinilai secara
statistik. Modul ini menutupnya.

MODUL SENDIRI, BUKAN SUNTINGAN. ``ringkas_gabungan`` berada di ``run_wf.py``,
orkestrator H-001b yang dibekukan karena hasilnya sudah dikomit. Menambah kunci
di sana akan menyentuh berkas beku dan mengubah keluaran tiga orkestrator lama.
Karena itu perhitungan berdiri di sini dan ``runner.py`` yang memanggilnya,
persis seperti ``konsentrasi.py`` (ADR-010) dan ``funding_ekor.py`` (ADR-011).
Modul ini **tidak mengimpor apa pun dari lux.backtest**, sehingga tidak ada arah
impor yang bisa menutup lingkaran seperti cacat ``4b77617``.

PERINGATAN YANG WAJIB IKUT TERCETAK DI LAPORAN. Galat baku di bawah
mengasumsikan perdagangan saling bebas. Asumsi itu **tidak benar** di sini:
perdagangan dari 40 simbol kripto pada jendela waktu yang bertumpang saling
berkorelasi lewat gerakan pasar bersama. Akibatnya galat baku yang dihitung modul
ini adalah **taksiran BAWAH** — galat sesungguhnya lebih besar, jadi keyakinan
sesungguhnya lebih kecil. Angka ini boleh dipakai untuk menjatuhkan klaim
("bahkan dengan asumsi paling longgar pun jaraknya kurang dari satu galat
baku"), dan **tidak boleh** dipakai untuk menegakkan klaim.

Selang 95% memakai pendekatan normal ``z = 1,959964`` karena ``scipy`` tidak
tersedia di runner dan tidak akan ditambahkan hanya untuk satu nilai kritis.
Pada n di atas seribu perbedaannya terhadap sebaran-t di bawah 0,2%.
"""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np

# Nilai kritis normal dua sisi untuk 95%.
Z_95 = 1.959963984540054

NAMA = "sebaran"

# Kunci yang SELALU ada, apa pun keadaannya. Pemanggil tidak boleh perlu
# memeriksa keberadaan kunci, hanya nilainya.
KUNCI = (
    "n",
    "dapat_dinilai",
    "sebab",
    "rerata_R",
    "std_R",
    "galat_baku_R",
    "min_R",
    "q1_R",
    "median_R",
    "q3_R",
    "maks_R",
    "ci95_bawah_R",
    "ci95_atas_R",
)


def dari_perdagangan(perdagangan: Iterable) -> list[float]:
    """Mengambil nilai R dari objek Perdagangan mana pun yang punya atribut R."""
    return [float(p.R) for p in perdagangan]


def _tak_ternilai(n: int, sebab: str, rerata: float | None) -> dict:
    return {
        "n": n,
        "dapat_dinilai": False,
        "sebab": sebab,
        "rerata_R": rerata,
        "std_R": None,
        "galat_baku_R": None,
        "min_R": rerata,
        "q1_R": rerata,
        "median_R": rerata,
        "q3_R": rerata,
        "maks_R": rerata,
        "ci95_bawah_R": None,
        "ci95_atas_R": None,
    }


def ukur_sebaran(nilai_R: Iterable[float]) -> dict:
    """Mengukur sebaran R beserta galat baku reratanya.

    Simpangan baku memakai ``ddof=1`` karena yang diukur adalah sampel
    perdagangan, bukan populasi seluruh perdagangan yang mungkin. Dengan n di
    atas sepuluh ribu perbedaannya kecil, tetapi memakai ddof=0 berarti
    menyatakan sampel ini adalah seluruh dunia, dan itu pernyataan yang salah.

    Nilai tidak finit ditolak keras, bukan dibersihkan diam-diam: NaN pada R
    berarti ada cacat di mesin eksekusi, dan cacat itu wajib berbunyi.
    """
    xs = [float(x) for x in nilai_R]
    for x in xs:
        if not math.isfinite(x):
            raise ValueError(
                "nilai R tidak finit; sebaran tidak boleh diukur atas NaN atau "
                "infinit karena itu tanda cacat mesin, bukan tanda data langka"
            )

    n = len(xs)
    if n == 0:
        return _tak_ternilai(0, "tidak ada perdagangan", None)
    if n == 1:
        return _tak_ternilai(
            1, "butuh minimal dua perdagangan untuk simpangan baku", xs[0]
        )

    a = np.asarray(xs, dtype=float)
    rerata = float(a.mean())
    std = float(a.std(ddof=1))
    galat_baku = std / math.sqrt(n)
    q1, med, q3 = (float(v) for v in np.percentile(a, [25.0, 50.0, 75.0]))

    return {
        "n": n,
        "dapat_dinilai": True,
        "sebab": "",
        "rerata_R": rerata,
        "std_R": std,
        "galat_baku_R": galat_baku,
        "min_R": float(a.min()),
        "q1_R": q1,
        "median_R": med,
        "q3_R": q3,
        "maks_R": float(a.max()),
        "ci95_bawah_R": rerata - Z_95 * galat_baku,
        "ci95_atas_R": rerata + Z_95 * galat_baku,
    }


def jarak_ambang(ukuran: dict, ambang: float) -> dict:
    """Jarak rerata terhadap sebuah ambang, dalam R dan dalam satuan galat baku.

    Ini **bukan** gerbang dan tidak boleh dijadikan gerbang. Ambang 0,05R adalah
    kriteria pra-registrasi; menambahkan syarat statistik di atasnya sekarang,
    setelah H-010 lulus, berarti menyetel ambang terhadap hasil. Fungsi ini hanya
    melaporkan seberapa tipis kelulusan atau kegagalan itu.
    """
    ambang = float(ambang)
    rerata = ukuran.get("rerata_R")
    galat_baku = ukuran.get("galat_baku_R")

    if rerata is None:
        return {
            "ambang": ambang,
            "jarak_R": None,
            "jarak_galat_baku": None,
            "dapat_dinilai": False,
            "sebab": ukuran.get("sebab") or "rerata tidak tersedia",
        }

    jarak = rerata - ambang
    if not galat_baku:
        return {
            "ambang": ambang,
            "jarak_R": jarak,
            "jarak_galat_baku": None,
            "dapat_dinilai": False,
            "sebab": "galat baku nol atau tidak tersedia",
        }

    return {
        "ambang": ambang,
        "jarak_R": jarak,
        "jarak_galat_baku": jarak / galat_baku,
        "dapat_dinilai": True,
        "sebab": "",
    }
