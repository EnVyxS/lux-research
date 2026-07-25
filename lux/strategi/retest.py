"""Entri retest: menembus dulu, masuk belakangan.

Terjemahan mekanis dari "sniper entry". Alih-alih masuk pada bar yang menembus,
posisi baru dibuka bila harga kembali menyentuh level yang ditembus lalu menutup
di sisi penembusan, dalam ``jendela_retest`` bar. Yang tidak pernah kembali
dilewatkan sepenuhnya.

Alasan menguji ini spesifik, bukan sekadar karena populer. H-002 mencatat biaya
transaksi rerata 0,0345R terhadap keunggulan 0,032R — biaya per perdagangan
hampir menelan seluruh keunggulan. Masuk lebih dekat ke level berarti stop yang
sama menutup jarak harga yang lebih kecil, sehingga biaya per R mengecil. Bila
harganya adalah kehilangan seluruh penembusan yang lari tanpa menoleh, itulah
yang akan diukur.

Tidak ada parameter toleransi. Retest didefinisikan sebagai sumbu yang benar-benar
menyentuh level, bukan "mendekati sejauh k×ATR". Toleransi adalah parameter
tersembunyi yang akan menggoda untuk disetel setelah hasil terlihat.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from lux.strategi.breakout_atr import batas_donchian

LOOKBACK = 55


def sinyal(df: pd.DataFrame, params: dict) -> np.ndarray:
    """+1 saat retest penembusan atas terkonfirmasi, -1 untuk sisi bawah.

    Mesin keadaan berjalan maju satu bar sekali dan tidak pernah menengok ke
    depan: penembusan didaftarkan **setelah** bar berjalan dinilai, sehingga bar
    penembusan itu sendiri tidak pernah menjadi bar entri.
    """
    lookback = int(params.get("lookback", LOOKBACK))
    jendela = int(params["jendela_retest"])
    if jendela < 1:
        raise ValueError("jendela_retest minimal 1")
    izinkan_short = bool(params.get("izinkan_short", True))

    atas, bawah = batas_donchian(df, lookback)
    c = df["close"].to_numpy(dtype="float64")
    h = df["high"].to_numpy(dtype="float64")
    l = df["low"].to_numpy(dtype="float64")
    n = len(df)
    s = np.zeros(n, dtype="int64")

    level_long: float | None = None
    umur_long = 0
    level_short: float | None = None
    umur_short = 0

    for i in range(n):
        if level_long is not None:
            if umur_long > jendela:
                level_long = None
            elif l[i] <= level_long and c[i] > level_long:
                s[i] = 1
                level_long = None
            else:
                umur_long += 1

        if level_short is not None:
            if umur_short > jendela:
                level_short = None
            elif h[i] >= level_short and c[i] < level_short:
                if izinkan_short:
                    s[i] = -1
                level_short = None
            else:
                umur_short += 1

        if np.isfinite(atas[i]) and c[i] > atas[i]:
            level_long, umur_long = float(atas[i]), 1
        if izinkan_short and np.isfinite(bawah[i]) and c[i] < bawah[i]:
            level_short, umur_short = float(bawah[i]), 1

    return s


RUANG_PARAMETER = {"jendela_retest": [6, 12, 24], "lookback": [LOOKBACK]}


def kandidat() -> list[dict]:
    return [
        {"jendela_retest": j, "lookback": LOOKBACK}
        for j in RUANG_PARAMETER["jendela_retest"]
    ]
