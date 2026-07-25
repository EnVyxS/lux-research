"""Pengujian saringan rezim ADX.

Yang dikunci: ADX tidak boleh memakai bar yang sedang dinilai, dan saringan harus
benar-benar memadamkan sinyal, bukan sekadar meneruskannya.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from lux.backtest.gerbang import gerbang_lookahead
from lux.strategi.breakout_atr import sinyal as sinyal_breakout
from lux.strategi.rezim_adx import AMBANG_ADX, adx, kandidat, sinyal

JAM = 3_600_000
AWAL = 1_600_000_000_000


def bingkai(harga):
    return pd.DataFrame(
        {
            "open_time": [AWAL + i * JAM for i in range(len(harga))],
            "open": harga,
            "high": [p + 1.0 for p in harga],
            "low": [p - 1.0 for p in harga],
            "close": harga,
        }
    )


def test_pemanasan_adx_kosong():
    df = bingkai([100.0 + i for i in range(80)])
    a = adx(df, 14)
    assert np.isnan(a[:28]).all()


def test_tren_kuat_menghasilkan_adx_tinggi():
    df = bingkai([100.0 + i * 2 for i in range(120)])
    a = adx(df, 14)
    assert np.nanmax(a) > AMBANG_ADX


def test_pasar_bolak_balik_menghasilkan_adx_rendah():
    df = bingkai([100.0 + (i % 2) for i in range(120)])
    a = adx(df, 14)
    assert np.nanmax(a[40:]) < AMBANG_ADX


def test_saringan_memadamkan_sinyal_di_luar_tren():
    """Saringan yang tidak pernah memadamkan apa pun bukan saringan."""
    harga = [100.0 + (i % 2) for i in range(200)] + [200.0]
    df = bingkai(harga)
    assert sinyal_breakout(df, {"lookback": 20})[-1] == 1
    assert sinyal(df, {"lookback": 20, "adx_min": AMBANG_ADX})[-1] == 0


def test_ambang_nol_meneruskan_seluruh_sinyal_breakout():
    rng = np.random.default_rng(5)
    df = bingkai(list(100.0 + np.cumsum(rng.normal(0, 1, 400))))
    dasar = sinyal_breakout(df, {"lookback": 55})
    lolos = sinyal(df, {"lookback": 55, "adx_min": 0.0})
    # Hanya wilayah pemanasan ADX yang boleh berbeda.
    assert (lolos[40:] == dasar[40:]).all()


def test_saringan_tidak_pernah_menambah_sinyal():
    rng = np.random.default_rng(9)
    df = bingkai(list(100.0 + np.cumsum(rng.normal(0, 1, 500))))
    dasar = sinyal_breakout(df, {"lookback": 55})
    disaring = sinyal(df, {"lookback": 55, "adx_min": AMBANG_ADX})
    assert (np.abs(disaring) <= np.abs(dasar)).all()


def test_lolos_gerbang_lookahead():
    rng = np.random.default_rng(13)
    df = bingkai(list(100.0 + np.cumsum(rng.normal(0, 1, 400))))
    g = gerbang_lookahead(df, lambda d: sinyal(d, {"lookback": 55, "adx_min": 30.0}))
    assert g.lulus, g.catatan


def test_ruang_parameter_tetap_kecil():
    assert len(kandidat()) == 3
    assert all(k["adx_min"] == 30.0 for k in kandidat())
