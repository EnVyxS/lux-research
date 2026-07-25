"""Pengujian sapuan likuiditas, satu-satunya bagian SMC yang dapat dikodekan
tanpa penafsiran.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from lux.backtest.gerbang import gerbang_lookahead
from lux.strategi.smc import kandidat, level_sapuan, sinyal

JAM = 3_600_000
AWAL = 1_600_000_000_000


def bingkai(baris):
    """baris: daftar (high, low, close)."""
    return pd.DataFrame(
        {
            "open_time": [AWAL + i * JAM for i in range(len(baris))],
            "open": [b[2] for b in baris],
            "high": [b[0] for b in baris],
            "low": [b[1] for b in baris],
            "close": [b[2] for b in baris],
        }
    )


def datar(n):
    return [(101.0, 99.0, 100.0)] * n


def test_level_tidak_menyertakan_bar_berjalan():
    df = bingkai(datar(20) + [(200.0, 50.0, 100.0)])
    atas, bawah = level_sapuan(df, 10)
    assert atas[-1] == pytest.approx(101.0)
    assert bawah[-1] == pytest.approx(99.0)


def test_sapuan_dasar_menghasilkan_long():
    df = bingkai(datar(20) + [(101.0, 90.0, 100.0)])
    assert sinyal(df, {"jendela": 10})[-1] == 1


def test_sapuan_puncak_menghasilkan_short():
    df = bingkai(datar(20) + [(115.0, 99.0, 100.0)])
    assert sinyal(df, {"jendela": 10})[-1] == -1


def test_penembusan_tanpa_kembali_bukan_sapuan():
    """Menembus dan ditutup di luar rentang adalah penembusan, bukan sapuan."""
    df = bingkai(datar(20) + [(101.0, 90.0, 92.0)])
    assert sinyal(df, {"jendela": 10})[-1] == 0


def test_short_dapat_dimatikan():
    df = bingkai(datar(20) + [(115.0, 99.0, 100.0)])
    assert sinyal(df, {"jendela": 10, "izinkan_short": False})[-1] == 0


def test_pemanasan_tidak_menghasilkan_sinyal():
    df = bingkai(datar(40))
    assert (sinyal(df, {"jendela": 20})[:20] == 0).all()


def test_jendela_terlalu_kecil_ditolak():
    with pytest.raises(ValueError):
        level_sapuan(bingkai(datar(20)), 4)


def test_lolos_gerbang_lookahead():
    rng = np.random.default_rng(23)
    harga = 100.0 + np.cumsum(rng.normal(0, 1, 400))
    df = bingkai([(p + 1.0, p - 1.0, p) for p in harga])
    g = gerbang_lookahead(df, lambda d: sinyal(d, {"jendela": 50}))
    assert g.lulus, g.catatan


def test_ruang_parameter_tetap_kecil():
    assert len(kandidat()) == 3
