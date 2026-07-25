"""Pengujian konfig per kandidat pada walk-forward (ADR-007).

Yang paling penting dikunci di sini bukan fitur barunya, melainkan bahwa jalur
lama tidak berubah sedikit pun. H-001b, H-002, dan H-003 harus tetap dapat
diulang bita demi bita.
"""

from __future__ import annotations

from dataclasses import replace

import numpy as np
import pandas as pd

from lux.backtest.engine import Konfig
from lux.backtest.walk_forward import jalankan_walk_forward
from lux.strategi.breakout_atr import sinyal as sinyal_breakout

JAM = 3_600_000
AWAL = 1_600_000_000_000


def bingkai(n=3000, seed=7):
    rng = np.random.default_rng(seed)
    harga = 100.0 + np.cumsum(rng.normal(0, 1, n))
    return pd.DataFrame(
        {
            "open_time": [AWAL + i * JAM for i in range(n)],
            "open": harga,
            "high": harga + 1.0,
            "low": harga - 1.0,
            "close": harga,
        }
    )


KANDIDAT = [{"lookback": 20}, {"lookback": 55}]
ARG = dict(panjang_latih=1000, panjang_uji=500, embargo=24, pemanasan=100)


def total_R(wf):
    return sum(p.R for p in wf.perdagangan_luar_sampel)


def test_tanpa_buat_konfig_perilaku_tidak_berubah():
    df = bingkai()
    k = Konfig(imbalan_R=2.0)
    lama = jalankan_walk_forward(df, KANDIDAT, sinyal_breakout, konfig=k, **ARG)
    baru = jalankan_walk_forward(
        df,
        KANDIDAT,
        sinyal_breakout,
        konfig=k,
        buat_konfig=lambda params, dasar: dasar,
        **ARG,
    )
    assert len(lama.perdagangan_luar_sampel) == len(baru.perdagangan_luar_sampel)
    assert total_R(lama) == total_R(baru)


def test_konfig_per_kandidat_benar_benar_mengubah_hasil():
    df = bingkai()
    k = Konfig(imbalan_R=2.0)
    dasar = jalankan_walk_forward(df, KANDIDAT, sinyal_breakout, konfig=k, **ARG)
    lebar = jalankan_walk_forward(
        df,
        KANDIDAT,
        sinyal_breakout,
        konfig=k,
        buat_konfig=lambda params, d: replace(d, imbalan_R=4.0),
        **ARG,
    )
    assert total_R(dasar) != total_R(lebar)


def test_konfig_yang_dipakai_ikut_tersimpan():
    df = bingkai()
    wf = jalankan_walk_forward(
        df,
        [{"lookback": 20, "imbalan_R": 3.0}],
        sinyal_breakout,
        konfig=Konfig(),
        buat_konfig=lambda p, d: replace(d, imbalan_R=float(p["imbalan_R"])),
        **ARG,
    )
    assert wf.per_jendela
    for hj in wf.per_jendela:
        assert hj.konfig is not None
        assert hj.konfig.imbalan_R == 3.0


def test_medan_lain_tidak_ikut_berubah():
    """Hanya imbalan yang boleh bergerak; sisanya diwarisi apa adanya."""
    from lux.backtest.run_h007 import buat_konfig

    dasar = Konfig(maks_umur_bar=168, maks_carry_R=0.25, atr_pengali_stop=2.0)
    baru = buat_konfig({"imbalan_R": 3.0}, dasar)
    assert baru.imbalan_R == 3.0
    assert baru.maks_umur_bar == dasar.maks_umur_bar
    assert baru.maks_carry_R == dasar.maks_carry_R
    assert baru.atr_pengali_stop == dasar.atr_pengali_stop
    assert baru.fee == dasar.fee and baru.slippage == dasar.slippage


def test_imbalan_lebih_besar_menghasilkan_lebih_sedikit_kemenangan_target():
    """Ramalan mekanis ADR-007, diuji pada data sintetis."""
    df = bingkai(seed=11)
    k = Konfig()
    kena = {}
    for im in (1.0, 4.0):
        wf = jalankan_walk_forward(
            df,
            [{"lookback": 20}],
            sinyal_breakout,
            konfig=k,
            buat_konfig=lambda p, d, im=im: replace(d, imbalan_R=im),
            **ARG,
        )
        trades = wf.perdagangan_luar_sampel
        kena[im] = sum(1 for p in trades if p.alasan_keluar == "target")
    assert kena[4.0] <= kena[1.0]
