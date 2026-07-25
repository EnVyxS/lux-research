"""Pembalikan jangka pendek: skor-z penutupan terhadap rerata bergulir.

Mekanisme ini sengaja **berlawanan arah** dengan `breakout_atr`. Donchian
bertaruh penembusan berlanjut; modul ini bertaruh simpangan ekstrem kembali ke
rerata. Keduanya membaca informasi yang kurang lebih sama dan menyimpulkan hal
yang berkebalikan, dan itulah gunanya: menjalankan keduanya pada kerangka
eksekusi yang identik memisahkan pertanyaan "arah taruhannya salah" dari
pertanyaan "kerangkanya yang membatasi". Lihat `decisions/ADR-005`.

Seperti seluruh strategi di repo ini, sinyalnya **kausal secara struktural**:
rerata dan simpangan baku dihitung dari jendela yang berakhir di bar sebelumnya.
Bar yang sedang dinilai tidak pernah ikut membentuk rerata yang ia simpangi.
Tanpa `shift(1)`, penutupan ekstrem akan menarik reratanya sendiri ke arahnya
dan skor-z akan sistematis terlalu kecil — cacat yang tidak menghasilkan galat,
hanya hasil yang salah.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

AMBANG_BAKU = 2.0


def zskor(df: pd.DataFrame, jendela: int) -> np.ndarray:
    """Skor-z penutupan terhadap ``jendela`` bar **sebelum** bar berjalan.

    Bar pemanasan bernilai NaN, bukan nol. Nol berarti "tepat di rerata", sebuah
    pernyataan yang tidak boleh dibuat ketika reratanya belum ada.

    Simpangan baku nol menghasilkan NaN, bukan pembagian yang meledak atau tak
    hingga. Pasar yang benar-benar datar tidak punya simpangan ekstrem menurut
    definisi, dan ekor datar simbol mati (ADR-003) adalah tempat kondisi ini
    paling sering muncul.
    """
    if jendela < 5:
        raise ValueError("jendela minimal 5")
    c = df["close"].astype("float64")
    rerata = c.rolling(jendela).mean().shift(1)
    simpangan = c.rolling(jendela).std(ddof=0).shift(1)
    sah = simpangan > 0
    z = pd.Series(np.nan, index=c.index, dtype="float64")
    z[sah] = (c[sah] - rerata[sah]) / simpangan[sah]
    return z.to_numpy(dtype="float64")


def sinyal(df: pd.DataFrame, params: dict) -> np.ndarray:
    """+1 bila penutupan jatuh jauh di bawah rerata, -1 bila melonjak jauh di atas.

    Perhatikan tandanya: skor-z **negatif** menghasilkan sinyal **long**. Ini
    kebalikan langsung dari `breakout_atr.sinyal`, dan disengaja.
    """
    jendela = int(params["jendela"])
    ambang = float(params.get("ambang", AMBANG_BAKU))
    if ambang <= 0:
        raise ValueError("ambang harus positif")
    izinkan_short = bool(params.get("izinkan_short", True))

    z = zskor(df, jendela)
    s = np.zeros(len(df), dtype="int64")
    sah = np.isfinite(z)
    s[sah & (z <= -ambang)] = 1
    if izinkan_short:
        s[sah & (z >= ambang)] = -1
    return s


RUANG_PARAMETER = {"jendela": [24, 72, 168], "ambang": [AMBANG_BAKU]}


def kandidat() -> list[dict]:
    """Tiga kombinasi, sama sedikitnya dengan H-001b.

    24, 72, dan 168 bar adalah satu hari, tiga hari, dan satu minggu pada bar 1
    jam. Ketiganya dipilih karena satuan waktunya alami, bukan karena dicoba
    lebih dulu lalu disukai. ``ambang`` 2,0 tidak ikut dicari; ia angka baku
    statistik yang ditetapkan di muka oleh ADR-005.
    """
    return [
        {"jendela": j, "ambang": AMBANG_BAKU} for j in RUANG_PARAMETER["jendela"]
    ]
