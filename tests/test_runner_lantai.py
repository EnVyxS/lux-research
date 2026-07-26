"""Pengujian lantai semesta di runner (ADR-014 bagian 8 butir 1).

Yang diuji di sini **bukan** aritmetika lantainya — itu sudah diuji di
``tests/test_degenerasi.py`` dan tidak diulang. Yang diuji adalah
penyambungannya: bahwa runner memanggil aritmetika itu alih-alih menuliskan
salinannya, bahwa bawaannya MATI sehingga hasil H-001b sampai H-011 tetap dapat
diulang, dan bahwa simbol yang dibuang meninggalkan jejak lengkap.

Seluruh pengujian di berkas ini berjalan tanpa jaringan dan tanpa berkas aset;
bingkai dibuat sintetis supaya nilai ATR-nya diketahui secara tertutup.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from lux.backtest.engine import Konfig
from lux.backtest.runner import (
    Opsi,
    median_stop_frac_bingkai,
    saring_bingkai,
)
from lux.degenerasi import AMBANG_MIN_STOP_FRAC, KASUS_USDCUSDT


def bingkai(n: int = 200, harga: float = 100.0, rentang: float = 1.0) -> pd.DataFrame:
    """Bingkai dengan true range tetap, sehingga ATR Wilder = ``rentang``.

    Harga penutupan tetap, jadi median stop_frac = pengali * rentang / harga
    dan dapat diperiksa tangan.
    """
    close = np.full(n, harga, dtype="float64")
    return pd.DataFrame(
        {
            "open_time": np.arange(n, dtype="int64") * 3_600_000,
            "open": close,
            "high": close + rentang / 2.0,
            "low": close - rentang / 2.0,
            "close": close,
        }
    )


def test_median_stop_frac_bingkai_dihitung_dari_atr_wilder():
    # ATR = 1,0 pada harga 100 dengan pengali 2,0 -> 0,02.
    assert median_stop_frac_bingkai(bingkai()) == pytest.approx(0.02)


def test_median_stop_frac_bingkai_memakai_pengali_konfig():
    k = Konfig(atr_pengali_stop=4.0)
    assert median_stop_frac_bingkai(bingkai(), k) == pytest.approx(0.04)


def test_median_stop_frac_bingkai_kosong_tidak_dapat_dinilai():
    kosong = bingkai().iloc[0:0]
    assert median_stop_frac_bingkai(kosong) is None


def test_riwayat_lebih_pendek_dari_pemanasan_atr_tidak_dapat_dinilai():
    # Seluruh ATR NaN. Tidak dapat dinilai berarti DITOLAK, bukan diloloskan.
    pendek = bingkai(n=10)
    assert median_stop_frac_bingkai(pendek) is None
    _, hasil = saring_bingkai({"XUSDT": pendek}, AMBANG_MIN_STOP_FRAC)
    assert hasil["n_layak"] == 0
    assert "tidak dapat dinilai" in hasil["ditolak"][0]["sebab"]


def test_median_stop_frac_bingkai_menuntut_kolom_wajib():
    with pytest.raises(ValueError):
        median_stop_frac_bingkai(bingkai().drop(columns=["high"]))


def test_simbol_seperti_usdcusdt_dibuang():
    # Harga 1,0 dengan rentang 1e-06: median stop_frac 2e-06, seorde dengan
    # 3,1984e-06 yang tercatat di laporan H-011.
    degenerat = bingkai(harga=1.0, rentang=1e-06)
    m = median_stop_frac_bingkai(degenerat)
    assert m is not None and m < KASUS_USDCUSDT["stop_frac"] * 10
    tersisa, hasil = saring_bingkai(
        {"NORMALUSDT": bingkai(), "DEGENUSDT": degenerat}, AMBANG_MIN_STOP_FRAC
    )
    assert sorted(tersisa) == ["NORMALUSDT"]
    assert [b["symbol"] for b in hasil["ditolak"]] == ["DEGENUSDT"]


def test_simbol_normal_tidak_tersentuh():
    peta = {f"S{i}USDT": bingkai(harga=100.0 + i) for i in range(5)}
    tersisa, hasil = saring_bingkai(peta, AMBANG_MIN_STOP_FRAC)
    assert sorted(tersisa) == sorted(peta)
    assert hasil["n_ditolak"] == 0


def test_saring_bingkai_tidak_kehilangan_simbol():
    peta = {
        f"S{i}USDT": (bingkai() if i % 2 else bingkai(harga=1.0, rentang=1e-06))
        for i in range(10)
    }
    tersisa, hasil = saring_bingkai(peta, AMBANG_MIN_STOP_FRAC)
    assert hasil["n_masuk"] == 10
    assert hasil["n_layak"] + hasil["n_ditolak"] == 10
    assert set(tersisa) | {b["symbol"] for b in hasil["ditolak"]} == set(peta)
    assert set(tersisa) == set(hasil["layak"])


def test_simbol_dibuang_membawa_median_dan_biaya():
    # Simbol yang hilang tanpa angka tidak dapat dibedakan dari penyubsetan
    # simbol yang dilarang ADR-013 bagian 8.
    _, hasil = saring_bingkai(
        {"DEGENUSDT": bingkai(harga=1.0, rentang=1e-06)}, AMBANG_MIN_STOP_FRAC
    )
    b = hasil["ditolak"][0]
    assert b["median_stop_frac"] == pytest.approx(2e-06)
    assert b["biaya_masuk_R"] > 600.0
    assert "di bawah lantai" in b["sebab"]
    assert hasil["ambang"] == AMBANG_MIN_STOP_FRAC


def test_saring_bingkai_menolak_ambang_tidak_positif():
    with pytest.raises(ValueError):
        saring_bingkai({"XUSDT": bingkai()}, 0.0)


def test_lantai_bawaan_mati_di_opsi():
    # Tripwire keterulangan: begitu bawaan ini bukan nol, sebelas hipotesis
    # lama berhenti dapat diulang.
    assert Opsi(dir_aset=Path("aset")).min_median_stop_frac == 0.0
