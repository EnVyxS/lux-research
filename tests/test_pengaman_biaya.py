"""Pengujian pengaman biaya masuk di mesin (ADR-014).

Yang diuji di sini bukan apakah pengaman ini memperbaiki hasil, melainkan tiga
hal yang lebih penting: bawaannya benar-benar mati sehingga hasil lama tetap
dapat diulang, ia menolak keadaan degenerat yang menghancurkan satuan R, dan ia
TIDAK menyentuh entri normal. Pengaman yang ikut membuang entri normal bukan
pengaman melainkan saringan hasil, dan saringan hasil adalah overfitting yang
memakai nama lain.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from lux.backtest.engine import Hasil, Konfig, jalankan
from lux.degenerasi import AMBANG_BIAYA_MASUK_R

JAM = 3_600_000
AWAL = 1_600_000_000_000


def bingkai(harga: list[float], rentang: float) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open_time": [AWAL + i * JAM for i in range(len(harga))],
            "open": harga,
            "high": [p + rentang for p in harga],
            "low": [p - rentang for p in harga],
            "close": harga,
        }
    )


def bingkai_degenerat(n: int = 60) -> pd.DataFrame:
    """Tiruan pasangan stablecoin: harga sekitar 1,0 dengan gerak orde 1e-6.

    Inilah bentuk USDCUSDT di data nyata: ATR terhadap harga praktis nol,
    sehingga stop_frac mendekati nol dan biaya dalam satuan R meledak.
    """
    harga = [1.0 + (1e-6 if i % 2 else 0.0) for i in range(n)]
    return bingkai(harga, 5e-7)


def bingkai_normal(n: int = 60) -> pd.DataFrame:
    return bingkai([100.0 + (0.5 if i % 2 else 0.0) for i in range(n)], 1.0)


def sinyal_di(n: int, indeks: int) -> np.ndarray:
    s = np.zeros(n, dtype=int)
    s[indeks] = 1
    return s


def test_bawaan_pengaman_mati():
    # Tripwire: hasil H-001b sampai H-011 hanya dapat diulang selama bawaan
    # mesin tidak menyaring apa pun.
    assert Konfig().maks_biaya_masuk_R == 0.0


def test_konfig_menolak_pengaman_negatif():
    with pytest.raises(ValueError):
        Konfig(maks_biaya_masuk_R=-0.1)


def test_hasil_bawaan_menghitung_nol_penolakan():
    h = Hasil(symbol="X")
    assert h.entri_ditolak_biaya == 0
    assert h.ringkas()["entri_ditolak_biaya"] == 0


def test_simbol_degenerat_menghancurkan_satuan_R_ketika_pengaman_mati():
    """Keadaan yang sesungguhnya terjadi di H-011, direproduksi kecil-kecilan."""
    df = bingkai_degenerat()
    hasil = jalankan(df, sinyal_di(len(df), 20))
    assert hasil.jumlah_trade == 1
    assert hasil.entri_ditolak_biaya == 0
    # Satu perdagangan sanggup melanggar ambang gerbang invarian risiko -1,5R
    # berkali-kali lipat, tanpa satu pun harga bergerak lebih dari 1e-6.
    assert hasil.perdagangan[0].R < -100.0


def test_pengaman_menolak_seluruh_entri_pada_simbol_degenerat():
    df = bingkai_degenerat()
    hasil = jalankan(
        df,
        sinyal_di(len(df), 20),
        Konfig(maks_biaya_masuk_R=AMBANG_BIAYA_MASUK_R),
    )
    assert hasil.jumlah_trade == 0
    assert hasil.entri_ditolak_biaya == 1
    assert hasil.ringkas()["entri_ditolak_biaya"] == 1


def test_penolakan_bukan_perdagangan():
    """Penolakan tidak boleh masuk histogram alasan keluar."""
    df = bingkai_degenerat()
    hasil = jalankan(
        df,
        sinyal_di(len(df), 20),
        Konfig(maks_biaya_masuk_R=AMBANG_BIAYA_MASUK_R),
    )
    assert [p.alasan_keluar for p in hasil.perdagangan] == []
    assert hasil.ringkas()["total_R"] == 0.0


def test_setiap_bar_yang_ditolak_dihitung():
    df = bingkai_degenerat()
    s = np.ones(len(df), dtype=int)
    hasil = jalankan(df, s, Konfig(maks_biaya_masuk_R=AMBANG_BIAYA_MASUK_R))
    # ATR pertama yang finit berada di indeks atr_periode, jadi entri pertama
    # yang mungkin ada di bar atr_periode + 1. Jumlahnya dihitung, bukan
    # diketik: angka yang diketik tangan akan bergeser diam-diam bila
    # atr_periode berubah.
    assert hasil.entri_ditolak_biaya == len(df) - (Konfig().atr_periode + 1)
    assert hasil.jumlah_trade == 0


def test_simbol_normal_tidak_disentuh_pengaman():
    df = bingkai_normal()
    s = sinyal_di(len(df), 20)
    mati = jalankan(df, s)
    nyala = jalankan(df, s, Konfig(maks_biaya_masuk_R=AMBANG_BIAYA_MASUK_R))
    assert nyala.entri_ditolak_biaya == 0
    assert nyala.jumlah_trade == mati.jumlah_trade > 0
    # Perbandingan dengan toleransi, bukan kesetaraan bit (aturan 22).
    for a, b in zip(mati.perdagangan, nyala.perdagangan):
        assert a.R == pytest.approx(b.R, rel=1e-12, abs=1e-15)
        assert a.alasan_keluar == b.alasan_keluar


def test_ambang_sangat_longgar_setara_dengan_pengaman_mati():
    df = bingkai_degenerat()
    s = sinyal_di(len(df), 20)
    mati = jalankan(df, s)
    longgar = jalankan(df, s, Konfig(maks_biaya_masuk_R=1e9))
    assert longgar.entri_ditolak_biaya == 0
    assert longgar.jumlah_trade == mati.jumlah_trade
    assert longgar.perdagangan[0].R == pytest.approx(mati.perdagangan[0].R)


def test_pengaman_sepakat_dengan_lantai_semesta_di_titik_batas():
    """Ambang mesin dan lantai semesta wajib bertemu di titik yang sama.

    Bingkai di bawah dibuat supaya jarak stop dapat dihitung tangan: harga
    tetap, sehingga true range setiap bar adalah 2*rentang dan ATR sama dengan
    itu. Jarak stop = 2*ATR = 4*rentang, dan dengan slippage nol harga masuk
    tepat 100, sehingga stop_frac = 0,04*rentang.
    """
    k = Konfig(slippage=0.0, maks_biaya_masuk_R=AMBANG_BIAYA_MASUK_R)
    # stop_frac 0,0039 -> di bawah lantai 0,004 -> ditolak
    di_bawah = bingkai([100.0] * 40, 0.0975)
    hasil_bawah = jalankan(di_bawah, sinyal_di(40, 20), k)
    assert hasil_bawah.jumlah_trade == 0
    assert hasil_bawah.entri_ditolak_biaya == 1
    # stop_frac 0,0041 -> di atas lantai -> diterima
    di_atas = bingkai([100.0] * 40, 0.1025)
    hasil_atas = jalankan(di_atas, sinyal_di(40, 20), k)
    assert hasil_atas.jumlah_trade == 1
    assert hasil_atas.entri_ditolak_biaya == 0


def test_penolakan_carry_tidak_dihitung_sebagai_penolakan_biaya():
    """Dua sebab penolakan tidak boleh tercampur di laporan.

    ADR-008 menolak entri ketika pengaman carry keras menyala tetapi jadwal
    funding tidak ada. Penolakan itu sah, tetapi ia bukan penolakan biaya.
    """
    df = bingkai_normal()
    hasil = jalankan(
        df,
        sinyal_di(len(df), 20),
        Konfig(maks_carry_realisasi_R=0.25, maks_biaya_masuk_R=AMBANG_BIAYA_MASUK_R),
        jadwal=None,
    )
    assert hasil.jumlah_trade == 0
    assert hasil.entri_ditolak_biaya == 0
