"""Pengujian entri retest ("sniper entry").

Yang dikunci: bar penembusan tidak boleh menjadi bar entri, dan peluang yang
tidak pernah kembali harus benar-benar hangus.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from lux.backtest.gerbang import gerbang_lookahead
from lux.strategi.retest import kandidat, sinyal

JAM = 3_600_000
AWAL = 1_600_000_000_000


def bingkai(harga):
    return pd.DataFrame(
        {
            "open_time": [AWAL + i * JAM for i in range(len(harga))],
            "open": harga,
            "high": [p + 0.5 for p in harga],
            "low": [p - 0.5 for p in harga],
            "close": harga,
        }
    )


def test_bar_penembusan_bukan_bar_entri():
    df = bingkai([100.0] * 30 + [140.0])
    s = sinyal(df, {"lookback": 10, "jendela_retest": 6})
    assert s[-1] == 0


def test_entri_terjadi_saat_harga_kembali_ke_level():
    # Menembus di bar 30, kembali menyentuh level 100,5 di bar 31, lalu ditutup
    # di atasnya.
    df = bingkai([100.0] * 30 + [140.0, 101.0])
    s = sinyal(df, {"lookback": 10, "jendela_retest": 6})
    assert s[-1] == 1


def test_peluang_hangus_setelah_jendela_habis():
    df = bingkai([100.0] * 30 + [140.0] + [139.0] * 8 + [101.0])
    s = sinyal(df, {"lookback": 10, "jendela_retest": 3})
    assert (s == 0).all()


def test_retest_yang_menutup_di_bawah_level_tidak_masuk():
    """Menyentuh saja tidak cukup; penutupan harus di sisi penembusan."""
    df = bingkai([100.0] * 30 + [140.0, 99.0])
    s = sinyal(df, {"lookback": 10, "jendela_retest": 6})
    assert s[-1] == 0


def test_sisi_short_bekerja_serupa():
    df = bingkai([100.0] * 30 + [60.0, 99.0])
    s = sinyal(df, {"lookback": 10, "jendela_retest": 6})
    assert s[-1] == -1


def test_short_dapat_dimatikan():
    df = bingkai([100.0] * 30 + [60.0, 99.0])
    s = sinyal(df, {"lookback": 10, "jendela_retest": 6, "izinkan_short": False})
    assert (s <= 0).sum() == len(s)
    assert (s == -1).sum() == 0


def test_jendela_nol_ditolak():
    with pytest.raises(ValueError):
        sinyal(bingkai([100.0] * 40), {"lookback": 10, "jendela_retest": 0})


def test_sinyal_lebih_jarang_daripada_penembusan_polos():
    from lux.strategi.breakout_atr import sinyal as sinyal_breakout

    rng = np.random.default_rng(21)
    df = bingkai(list(100.0 + np.cumsum(rng.normal(0, 1, 800))))
    polos = int((sinyal_breakout(df, {"lookback": 55}) != 0).sum())
    tunda = int((sinyal(df, {"lookback": 55, "jendela_retest": 12}) != 0).sum())
    assert tunda < polos


def test_lolos_gerbang_lookahead():
    rng = np.random.default_rng(17)
    df = bingkai(list(100.0 + np.cumsum(rng.normal(0, 1, 400))))
    g = gerbang_lookahead(
        df, lambda d: sinyal(d, {"lookback": 55, "jendela_retest": 12})
    )
    assert g.lulus, g.catatan


def test_ruang_parameter_tetap_kecil():
    assert len(kandidat()) == 3
