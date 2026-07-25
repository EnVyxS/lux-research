"""Breakout Donchian: strategi kandidat pertama, sengaja dipilih yang sederhana.

Strategi pertama yang diuji sebaiknya yang sudah lama dikenal dan sudah lama
dicurigai, bukan yang paling menjanjikan. Alasannya bukan kerendahhatian:
seluruh pipeline di sekitarnya belum pernah menjatuhkan apa pun, jadi yang
sedang diuji malam ini sesungguhnya adalah pipeline-nya, bukan strateginya.
Breakout Donchian pada perp kripto adalah kandidat yang baik justru karena
banyak bukti publik menyebutnya sudah tergerus. Bila pipeline kita meluluskannya
dengan gemilang, yang rusak hampir pasti pipeline-nya.

Seluruh sinyal di modul ini **kausal secara struktural**: batas atas dan bawah
dihitung dari jendela yang berakhir di bar sebelumnya, tidak pernah menyertakan
bar yang sedang dinilai. Dengan begitu ``high`` dan ``low`` bar berjalan tidak
ikut menentukan apakah bar itu menembus, yang jelas mustahil diketahui saat
keputusan diambil.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def batas_donchian(df: pd.DataFrame, lookback: int) -> tuple[np.ndarray, np.ndarray]:
    """Batas atas dan bawah dari ``lookback`` bar **sebelum** bar berjalan.

    ``shift(1)`` di sini bukan detail gaya. Tanpanya, bar yang harganya
    menembus akan ikut membentuk batas yang ditembusnya, sehingga tidak ada
    penembusan yang pernah tercatat, atau lebih buruk, tercatat dengan memakai
    harga tertinggi hari itu yang baru diketahui setelah hari itu berakhir.
    """
    if lookback < 2:
        raise ValueError("lookback minimal 2")
    atas = df["high"].rolling(lookback).max().shift(1).to_numpy(dtype="float64")
    bawah = df["low"].rolling(lookback).min().shift(1).to_numpy(dtype="float64")
    return atas, bawah


def sinyal(df: pd.DataFrame, params: dict) -> np.ndarray:
    """Sinyal keputusan pada penutupan tiap bar.

    Mengembalikan +1 bila penutupan menembus batas atas, -1 bila menembus batas
    bawah, 0 selebihnya. Bar yang batasnya belum terdefinisi bernilai 0, bukan
    ditebak: menebak di wilayah pemanasan menghasilkan perdagangan yang paling
    awal dan paling sering menentukan arah seluruh kurva ekuitas.
    """
    lookback = int(params["lookback"])
    izinkan_short = bool(params.get("izinkan_short", True))
    atas, bawah = batas_donchian(df, lookback)
    c = df["close"].to_numpy(dtype="float64")

    s = np.zeros(len(df), dtype="int64")
    sah = np.isfinite(atas) & np.isfinite(bawah)
    s[sah & (c > atas)] = 1
    if izinkan_short:
        s[sah & (c < bawah)] = -1
    return s


RUANG_PARAMETER = {"lookback": [20, 55, 100]}


def kandidat() -> list[dict]:
    """Daftar kombinasi parameter yang akan dicoba tiap jendela latih.

    Ruangnya sengaja kecil. Tiga kandidat berarti peluang menemukan sesuatu
    yang bagus secara kebetulan jauh lebih kecil daripada ratusan kombinasi,
    dan angka 20/55/100 dipilih karena ketiganya sudah dipakai luas jauh
    sebelum riset ini, bukan karena kami mencobanya lalu menyukainya.
    """
    return [{"lookback": lb} for lb in RUANG_PARAMETER["lookback"]]
