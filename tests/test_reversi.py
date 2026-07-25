"""Pengujian strategi pembalikan jangka pendek.

Seperti pada breakout, yang dikunci adalah kausalitas dan tanda sinyal, bukan
keuntungannya. Strategi boleh rugi; yang tidak boleh adalah melihat bar yang
belum terjadi, atau memasang taruhan ke arah yang berlawanan dari maksudnya.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from lux.backtest.gerbang import gerbang_lookahead
from lux.strategi.reversi_zskor import kandidat, sinyal, zskor

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


def test_bar_berjalan_tidak_membentuk_reratanya_sendiri():
    """Tanpa shift(1), penutupan ekstrem menarik reratanya sendiri dan skor-z
    jadi sistematis terlalu kecil. Cacat itu tidak melempar galat apa pun."""
    rng = np.random.default_rng(3)
    harga = list(100.0 + rng.normal(0, 1, 60))
    df = bingkai(harga)
    z = zskor(df, 24)

    c = pd.Series(harga, dtype="float64")
    rerata = c.rolling(24).mean().shift(1)
    simpangan = c.rolling(24).std(ddof=0).shift(1)
    harap = (c - rerata) / simpangan
    assert z[-1] == pytest.approx(float(harap.iloc[-1]))


def test_pemanasan_bernilai_nan_bukan_nol():
    df = bingkai([100.0 + i for i in range(40)])
    z = zskor(df, 24)
    assert np.isnan(z[:24]).all()
    assert np.isfinite(z[24:]).all()


def test_jendela_terlalu_kecil_ditolak():
    with pytest.raises(ValueError):
        zskor(bingkai([100.0] * 20), 4)


def test_ambang_tidak_positif_ditolak():
    with pytest.raises(ValueError):
        sinyal(bingkai([100.0] * 40), {"jendela": 10, "ambang": 0.0})


def test_pasar_datar_tidak_menghasilkan_sinyal():
    """Simpangan nol harus menghasilkan NaN, bukan pembagian tak hingga. Ekor
    datar simbol mati (ADR-003) adalah tempat kondisi ini paling sering ada."""
    df = bingkai([100.0] * 60)
    z = zskor(df, 24)
    assert np.isnan(z[24:]).all()
    assert (sinyal(df, {"jendela": 24}) == 0).all()


def test_penurunan_ekstrem_menghasilkan_long():
    """Tandanya kebalikan breakout: skor-z negatif berarti beli."""
    df = bingkai([100.0, 101.0] * 15 + [80.0])
    s = sinyal(df, {"jendela": 24, "ambang": 2.0})
    assert s[-1] == 1


def test_lonjakan_ekstrem_menghasilkan_short():
    df = bingkai([100.0, 101.0] * 15 + [130.0])
    s = sinyal(df, {"jendela": 24, "ambang": 2.0})
    assert s[-1] == -1


def test_short_dapat_dimatikan():
    df = bingkai([100.0, 101.0] * 15 + [130.0])
    s = sinyal(df, {"jendela": 24, "ambang": 2.0, "izinkan_short": False})
    assert s[-1] == 0


def test_simpangan_kecil_tidak_menghasilkan_sinyal():
    """Dua simpangan baku adalah ambang, bukan sekadar arah."""
    df = bingkai([100.0, 101.0] * 15 + [100.4])
    assert sinyal(df, {"jendela": 24, "ambang": 2.0})[-1] == 0


def test_arah_berlawanan_dengan_breakout():
    """Bukti bahwa H-003 benar-benar menguji mekanisme lain, bukan varian."""
    from lux.strategi.breakout_atr import sinyal as sinyal_breakout

    df = bingkai([100.0 + i * 0.1 for i in range(60)] + [140.0])
    assert sinyal_breakout(df, {"lookback": 24})[-1] == 1
    assert sinyal(df, {"jendela": 24, "ambang": 2.0})[-1] == -1


def test_lolos_gerbang_lookahead():
    rng = np.random.default_rng(11)
    harga = 100.0 + np.cumsum(rng.normal(0, 1, 400))
    df = bingkai(list(harga))
    g = gerbang_lookahead(df, lambda d: sinyal(d, {"jendela": 72, "ambang": 2.0}))
    assert g.lulus, g.catatan


def test_ruang_parameter_tetap_kecil():
    assert len(kandidat()) == 3
    assert all(k["ambang"] == 2.0 for k in kandidat())
