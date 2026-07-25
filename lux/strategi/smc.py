"""Sapuan likuiditas — bagian SMC yang dapat dikodekan tanpa penafsiran.

Sebagian besar kosakata Smart Money Concepts tidak punya definisi yang dapat
diuji: order block, fair value gap, dan BOS/CHoCH digambar berbeda oleh dua orang
yang melihat grafik yang sama. Satu bagian lolos dari masalah itu, yaitu sapuan
likuiditas: sumbu menembus ekstrem ``N`` bar sebelumnya, lalu penutupan kembali
ke dalam rentang. Definisi itu tidak menyisakan ruang tafsir dan dapat diperiksa
bar demi bar.

Harus dicatat sebelum hasilnya ada: mekanisme ini adalah **pembalikan di level**,
dan H-003 sudah menunjukkan pembalikan jangka pendek rugi telak pada dataset ini
(−0,2478R, p entri acak 1,0). Prior-nya buruk. Modul ini tetap ditulis karena
satu-satunya cara mengakhiri perdebatan tentang SMC adalah mengukurnya dengan
gerbang yang sama dengan yang menjatuhkan Donchian.

Kausalitas: ekstrem pembanding dihitung dari jendela yang berakhir di bar
sebelumnya. Bar yang menyapu tidak pernah ikut membentuk level yang disapunya.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def level_sapuan(df: pd.DataFrame, jendela: int) -> tuple[np.ndarray, np.ndarray]:
    if jendela < 5:
        raise ValueError("jendela minimal 5")
    atas = df["high"].rolling(jendela).max().shift(1).to_numpy(dtype="float64")
    bawah = df["low"].rolling(jendela).min().shift(1).to_numpy(dtype="float64")
    return atas, bawah


def sinyal(df: pd.DataFrame, params: dict) -> np.ndarray:
    """+1 saat sumbu menyapu dasar lalu menutup kembali di atasnya, -1 sebaliknya.

    Perhatikan bahwa arahnya berlawanan dengan penembusan: menembus dasar lalu
    ditutup kembali ke dalam dibaca sebagai likuiditas yang diambil, bukan sebagai
    kelanjutan turun.
    """
    jendela = int(params["jendela"])
    izinkan_short = bool(params.get("izinkan_short", True))
    atas, bawah = level_sapuan(df, jendela)
    c = df["close"].to_numpy(dtype="float64")
    h = df["high"].to_numpy(dtype="float64")
    l = df["low"].to_numpy(dtype="float64")

    s = np.zeros(len(df), dtype="int64")
    sah = np.isfinite(atas) & np.isfinite(bawah)
    s[sah & (l < bawah) & (c > bawah)] = 1
    if izinkan_short:
        s[sah & (h > atas) & (c < atas)] = -1
    return s


RUANG_PARAMETER = {"jendela": [20, 50, 100]}


def kandidat() -> list[dict]:
    return [{"jendela": j} for j in RUANG_PARAMETER["jendela"]]
