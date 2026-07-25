"""Uji pemangkasan ekor datar.

Dua kasus yang paling menentukan ada di sini dan keduanya soal apa yang TIDAK
boleh dipangkas: ekor datar yang harganya masih melangkah (pasar sekarat tetapi
nyata) dan blok datar di tengah riwayat (lubang yang tidak dapat ditutup tanpa
menyambung dua periode terpisah).
"""

from __future__ import annotations

import pandas as pd

from lux.potong_ekor import ekor_datar, evaluasi, potong, rasio_datar

JAM = 3_600_000
AWAL = 1_600_000_000_000


def datar(harga: float):
    return (harga, harga, harga, harga)


def gerak(harga: float):
    return (harga, harga + 1.0, harga - 1.0, harga)


def buat(baris) -> pd.DataFrame:
    n = len(baris)
    return pd.DataFrame(
        {
            "open_time": [AWAL + i * JAM for i in range(n)],
            "open": [b[0] for b in baris],
            "high": [b[1] for b in baris],
            "low": [b[2] for b in baris],
            "close": [b[3] for b in baris],
            "volume": [10.0] * n,
            "count": [5] * n,
        }
    )


def test_ekor_datar_ditemukan():
    df = buat([gerak(100.0)] * 10 + [datar(50.0)] * 30)
    assert ekor_datar(df, min_panjang=24) == 30


def test_ekor_yang_lebih_pendek_dari_ambang_tidak_dipangkas():
    df = buat([gerak(100.0)] * 10 + [datar(50.0)] * 5)
    assert ekor_datar(df, min_panjang=24) == 0
    assert len(potong(df, min_panjang=24)) == 15


def test_ekor_datar_yang_harganya_melangkah_tidak_dipangkas():
    """Tiap barnya datar tetapi harganya berpindah: pasar sekarat, bukan padding."""
    df = buat([gerak(100.0)] * 10 + [datar(50.0 + i) for i in range(30)])
    assert ekor_datar(df, min_panjang=24) == 0


def test_tanpa_ekor_bingkai_dikembalikan_utuh():
    df = buat([gerak(100.0)] * 40)
    assert ekor_datar(df) == 0
    assert len(potong(df)) == 40


def test_potong_membuang_persis_panjang_ekornya():
    df = buat([gerak(100.0)] * 10 + [datar(50.0)] * 30)
    sisa = potong(df, min_panjang=24)
    assert len(sisa) == 10
    assert sisa["open_time"].iloc[-1] == AWAL + 9 * JAM


def test_bingkai_yang_seluruhnya_datar_terpangkas_habis():
    df = buat([datar(50.0)] * 30)
    assert len(potong(df, min_panjang=24)) == 0


def test_bingkai_kosong_tidak_melempar():
    df = buat([])
    assert ekor_datar(df) == 0
    assert len(potong(df)) == 0


def test_blok_di_tengah_tidak_ikut_terpangkas():
    df = buat([gerak(100.0)] * 5 + [datar(50.0)] * 30 + [gerak(100.0)] * 5)
    assert ekor_datar(df, min_panjang=24) == 0
    assert len(potong(df, min_panjang=24)) == 40


def test_simbol_dengan_blok_tengah_dikeluarkan():
    df = buat([gerak(100.0)] * 5 + [datar(50.0)] * 30 + [gerak(100.0)] * 5)
    e = evaluasi("X", df, min_panjang=24, min_bar=1, maks_rasio=1.0)
    assert e["layak"] is False
    assert "di tengah riwayat" in e["alasan"]


def test_simbol_bersih_tetap_layak():
    df = buat([gerak(100.0 + i) for i in range(50)])
    e = evaluasi("X", df, min_panjang=24, min_bar=10, maks_rasio=0.10)
    assert e["layak"] is True
    assert e["alasan"] == ""
    assert e["dipangkas"] == 0


def test_riwayat_tersisa_terlalu_pendek_ditolak():
    df = buat([gerak(100.0)] * 10 + [datar(50.0)] * 30)
    e = evaluasi("X", df, min_panjang=24, min_bar=8760, maks_rasio=1.0)
    assert e["layak"] is False
    assert "di bawah 8760" in e["alasan"]
    assert e["bar_sisa"] == 10


def test_akhir_sejati_adalah_bar_terakhir_yang_tersisa():
    df = buat([gerak(100.0)] * 10 + [datar(50.0)] * 30)
    e = evaluasi("X", df, min_panjang=24, min_bar=1, maks_rasio=1.0)
    assert e["akhir_ms"] == AWAL + 9 * JAM
    assert e["dipangkas"] == 30


def test_rasio_datar_dihitung_atas_sisa_bukan_atas_bingkai_asli():
    df = buat([gerak(100.0)] * 10 + [datar(50.0)] * 30)
    assert rasio_datar(df) == 0.75
    e = evaluasi("X", df, min_panjang=24, min_bar=1, maks_rasio=1.0)
    assert e["rasio_datar_sisa"] == 0.0


def test_rasio_sisa_yang_masih_tinggi_ditolak():
    baris = []
    for i in range(20):
        baris.append(datar(50.0 + i))
        baris.append(gerak(100.0))
    e = evaluasi("X", buat(baris), min_panjang=24, min_bar=1, maks_rasio=0.10)
    assert e["layak"] is False
    assert "rasio bar datar" in e["alasan"]


def test_bingkai_kosong_tidak_membuat_akhir_ms_melempar():
    e = evaluasi("X", buat([datar(50.0)] * 30), min_panjang=24, min_bar=1)
    assert e["akhir_ms"] is None
    assert e["layak"] is False
    assert "tidak ada bar tersisa" in e["alasan"]
