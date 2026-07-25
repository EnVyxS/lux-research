"""Pengujian strategi breakout Donchian.

Yang paling penting di sini adalah kausalitasnya, bukan hasilnya. Strategi
boleh saja tidak menguntungkan; yang tidak boleh adalah menang karena melihat
bar yang belum terjadi.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from lux.backtest.gerbang import gerbang_lookahead
from lux.strategi.breakout_atr import batas_donchian, kandidat, sinyal

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


def test_batas_tidak_menyertakan_bar_berjalan():
    """Bar yang menembus tidak boleh ikut membentuk batas yang ditembusnya."""
    df = bingkai([100.0] * 10 + [200.0])
    atas, _ = batas_donchian(df, 5)
    assert atas[-1] == pytest.approx(101.0)


def test_periode_pemanasan_bernilai_kosong():
    df = bingkai([100.0 + i for i in range(30)])
    atas, bawah = batas_donchian(df, 10)
    assert np.isnan(atas[:10]).all()
    assert np.isnan(bawah[:10]).all()


def test_lookback_terlalu_kecil_ditolak():
    with pytest.raises(ValueError):
        batas_donchian(bingkai([100.0] * 10), 1)


def test_penembusan_atas_menghasilkan_sinyal_long():
    df = bingkai([100.0] * 20 + [500.0])
    s = sinyal(df, {"lookback": 10})
    assert s[-1] == 1


def test_penembusan_bawah_menghasilkan_sinyal_short():
    df = bingkai([100.0] * 20 + [1.0])
    s = sinyal(df, {"lookback": 10})
    assert s[-1] == -1


def test_short_dapat_dimatikan_lewat_parameter():
    df = bingkai([100.0] * 20 + [1.0])
    s = sinyal(df, {"lookback": 10, "izinkan_short": False})
    assert s[-1] == 0


def test_pemanasan_tidak_menghasilkan_sinyal():
    """Menebak di wilayah pemanasan menghasilkan perdagangan paling awal, yang
    justru paling menentukan arah seluruh kurva ekuitas."""
    df = bingkai([100.0 + i * 3 for i in range(40)])
    s = sinyal(df, {"lookback": 20})
    assert (s[:20] == 0).all()


def test_pasar_datar_tidak_menghasilkan_sinyal():
    df = bingkai([100.0] * 60)
    assert (sinyal(df, {"lookback": 20}) == 0).all()


def test_strategi_lolos_gerbang_lookahead():
    """Uji yang sama yang akan dijalankan di runner, dijalankan di sini dulu."""
    rng = np.random.default_rng(7)
    harga = 100.0 + np.cumsum(rng.normal(0, 1, 400))
    df = bingkai(list(harga))
    g = gerbang_lookahead(df, lambda d: sinyal(d, {"lookback": 55}))
    assert g.lulus, g.catatan


def test_ruang_parameter_tetap_kecil():
    """Ruang yang membengkak diam-diam adalah pencarian yang tidak dihitung."""
    assert len(kandidat()) == 3
