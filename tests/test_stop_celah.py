"""Pengujian ADR-016: stop yang menghormati celah harga.

Angka di sini dibuat bulat dengan sengaja: ``fee`` dan ``slippage`` nol, dan
bingkai barnya rata sehingga ATR tepat 1,0. Pengujian yang angkanya berantakan
akan lulus tanpa seorang pun tahu apa yang sebenarnya diuji.

Bingkai: delapan bar 1h. Entri terjadi pada pembukaan bar 4 dengan harga 100,5,
jarak stop 2,0, stop 98,5 untuk long dan 102,5 untuk short, ukuran 25, sehingga
risiko awal 50 dan satu R sama dengan 50 satuan uang.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from lux.backtest.engine import Konfig, harga_stop_terisi, jalankan

JAM_MS = 3_600_000


def konfig(hormati: bool) -> Konfig:
    return Konfig(
        fee=0.0,
        slippage=0.0,
        atr_periode=2,
        atr_pengali_stop=2.0,
        risiko_per_trade=0.005,
        modal_awal=10_000.0,
        stop_hormati_celah=hormati,
    )


def bingkai(bar5: dict) -> pd.DataFrame:
    """Empat bar rata, satu bar entri, lalu ``bar5`` sebagai bar keluar."""
    baris = [
        {"open": 100.5, "high": 101.0, "low": 100.0, "close": 100.5} for _ in range(5)
    ]
    baris.append(bar5)
    baris += [{"open": 100.5, "high": 101.0, "low": 100.0, "close": 100.5}] * 2
    df = pd.DataFrame(baris)
    df["open_time"] = [(i + 1) * JAM_MS for i in range(len(df))]
    return df


def sinyal(arah: int, n: int = 8) -> np.ndarray:
    s = np.zeros(n, dtype="int64")
    s[3] = arah
    return s


def satu_perdagangan(df: pd.DataFrame, arah: int, hormati: bool):
    hasil = jalankan(df, sinyal(arah), konfig(hormati), None, "UJIUSDT")
    assert hasil.jumlah_trade == 1, [p.alasan_keluar for p in hasil.perdagangan]
    return hasil.perdagangan[0]


CELAH_TURUN = {"open": 90.0, "high": 90.0, "low": 89.0, "close": 89.5}
CELAH_NAIK = {"open": 115.0, "high": 116.0, "low": 115.0, "close": 115.5}
TANPA_CELAH = {"open": 99.0, "high": 99.0, "low": 98.0, "close": 98.2}
CELAH_KE_TARGET = {"open": 120.0, "high": 121.0, "low": 119.5, "close": 120.0}


def test_medan_bawaan_mati():
    # Bila bawaannya pernah berubah menjadi True, seluruh hasil lama berhenti
    # dapat diulang tanpa satu pun pengujian lain mengeluh.
    assert Konfig().stop_hormati_celah is False


def test_harga_stop_terisi_mati_tidak_menyentuh_pembukaan():
    assert harga_stop_terisi(98.5, 1.0, 1, False) == pytest.approx(98.5)
    assert harga_stop_terisi(102.5, 9_999.0, -1, False) == pytest.approx(102.5)


def test_harga_stop_terisi_menyala_memilih_yang_terburuk():
    assert harga_stop_terisi(98.5, 90.0, 1, True) == pytest.approx(90.0)
    assert harga_stop_terisi(98.5, 99.0, 1, True) == pytest.approx(98.5)
    assert harga_stop_terisi(102.5, 115.0, -1, True) == pytest.approx(115.0)
    assert harga_stop_terisi(102.5, 99.0, -1, True) == pytest.approx(102.5)


def test_long_mati_tetap_satu_R_meski_bar_membuka_jauh_di_bawah_stop():
    p = satu_perdagangan(bingkai(CELAH_TURUN), 1, False)
    assert p.alasan_keluar == "stop"
    assert p.R == pytest.approx(-1.0)


def test_long_menyala_jauh_lebih_buruk_dari_satu_R():
    p = satu_perdagangan(bingkai(CELAH_TURUN), 1, True)
    assert p.alasan_keluar == "stop"
    # (90,0 - 100,5) * 25 / 50 = -5,25
    assert p.R == pytest.approx(-5.25)


def test_short_menyala_jauh_lebih_buruk_dari_satu_R():
    mati = satu_perdagangan(bingkai(CELAH_NAIK), -1, False)
    menyala = satu_perdagangan(bingkai(CELAH_NAIK), -1, True)
    assert mati.R == pytest.approx(-1.0)
    # -(115,0 - 100,5) * 25 / 50 = -7,25
    assert menyala.R == pytest.approx(-7.25)


def test_tanpa_celah_identik_bit_demi_bit():
    mati = satu_perdagangan(bingkai(TANPA_CELAH), 1, False)
    menyala = satu_perdagangan(bingkai(TANPA_CELAH), 1, True)
    assert mati.harga_keluar == menyala.harga_keluar
    assert mati.R == menyala.R


def test_target_tidak_pernah_lebih_baik_meski_bar_membuka_melewatinya():
    # Celah yang menguntungkan adalah hadiah atas ketidaktahuan. Menghormati
    # celah pada sisi target akan membayar hadiah itu.
    mati = satu_perdagangan(bingkai(CELAH_KE_TARGET), 1, False)
    menyala = satu_perdagangan(bingkai(CELAH_KE_TARGET), 1, True)
    assert mati.alasan_keluar == "target"
    assert menyala.alasan_keluar == "target"
    assert mati.R == pytest.approx(2.0)
    assert menyala.R == pytest.approx(2.0)
