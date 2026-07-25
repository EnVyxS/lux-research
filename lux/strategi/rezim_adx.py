"""Breakout Donchian yang hanya aktif saat pasar sedang tren (ADX ≥ 30).

H-002 menunjukkan breakout punya keunggulan nyata tetapi tipis: 0,032R terhadap
biaya transaksi rerata 0,0345R. Hipotesis di balik modul ini sederhana — sebagian
besar penembusan terjadi saat pasar tidak sedang tren, dan penembusan semacam itu
yang memakan biaya tanpa memberi apa-apa.

ADX diambil apa adanya dari Wilder, dengan ambang 30 yang sudah dipakai luas jauh
sebelum riset ini. Angka itu **tidak dicari**; mencarinya berarti mengubah
saringan menjadi parameter dan menghidupkan kembali persis masalah yang dilarang
ADR-004.

Kausalitas: seluruh nilai ADX digeser satu bar. Keputusan di bar i hanya boleh
memakai ADX yang sudah selesai dihitung di bar i-1.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from lux.strategi.breakout_atr import sinyal as sinyal_breakout

AMBANG_ADX = 30.0
PERIODE_ADX = 14


def _rma(x: pd.Series, periode: int) -> pd.Series:
    """Perataan Wilder. Bukan EMA biasa: alpha 1/periode, bukan 2/(periode+1)."""
    return x.ewm(alpha=1.0 / periode, adjust=False).mean()


def adx(df: pd.DataFrame, periode: int = PERIODE_ADX) -> np.ndarray:
    """ADX Wilder, **sudah digeser satu bar** sehingga aman dipakai di bar berjalan.

    Nilai yang dikembalikan pada indeks i adalah ADX yang selesai dihitung pada
    bar i-1. Tanpa pergeseran ini, saringan rezim akan memakai pergerakan bar
    yang sedang dinilai untuk memutuskan apakah bar itu layak diperdagangkan.
    """
    if periode < 2:
        raise ValueError("periode minimal 2")
    h = df["high"].astype("float64")
    l = df["low"].astype("float64")
    c = df["close"].astype("float64")

    naik = h.diff()
    turun = -l.diff()
    plus_dm = np.where((naik > turun) & (naik > 0), naik, 0.0)
    minus_dm = np.where((turun > naik) & (turun > 0), turun, 0.0)

    tr = pd.concat(
        [h - l, (h - c.shift(1)).abs(), (l - c.shift(1)).abs()], axis=1
    ).max(axis=1)

    atr_w = _rma(tr, periode)
    plus_di = 100.0 * _rma(pd.Series(plus_dm, index=df.index), periode) / atr_w
    minus_di = 100.0 * _rma(pd.Series(minus_dm, index=df.index), periode) / atr_w

    jumlah = plus_di + minus_di
    dx = 100.0 * (plus_di - minus_di).abs() / jumlah.where(jumlah > 0)
    nilai = _rma(dx.fillna(0.0), periode)

    # Wilder butuh dua kali periode sebelum ADX punya arti. Sebelum itu NaN,
    # bukan angka kecil yang kebetulan lolos atau kebetulan menyaring.
    nilai = nilai.copy()
    nilai.iloc[: 2 * periode] = np.nan
    return nilai.shift(1).to_numpy(dtype="float64")


def sinyal(df: pd.DataFrame, params: dict) -> np.ndarray:
    """Sinyal breakout yang dipadamkan di luar rezim tren."""
    ambang = float(params.get("adx_min", AMBANG_ADX))
    periode = int(params.get("adx_periode", PERIODE_ADX))
    s = sinyal_breakout(df, params)
    a = adx(df, periode)
    return np.where(np.isfinite(a) & (a >= ambang), s, 0).astype("int64")


RUANG_PARAMETER = {
    "lookback": [20, 55, 100],
    "adx_min": [AMBANG_ADX],
    "adx_periode": [PERIODE_ADX],
}


def kandidat() -> list[dict]:
    return [
        {"lookback": lb, "adx_min": AMBANG_ADX, "adx_periode": PERIODE_ADX}
        for lb in RUANG_PARAMETER["lookback"]
    ]
