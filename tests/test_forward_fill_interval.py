"""Gerbang forward_fill harus mengukur SATU HARI, bukan 24 bar (ADR-019).

Kasus inti ada di ``test_deret_dua_puluh_bar_lolos_1h_tetapi_gagal_4h``. Deret 20
bar datar adalah kurang dari sehari pada 1h, tetapi lebih dari tiga hari pada 4h.
Sampai ADR-019 gerbang menyatakan keduanya bersih, dan itu berarti mesin
diizinkan memperdagangkan tiga hari tanpa satu transaksi pun.
"""

from __future__ import annotations

import pandas as pd
import pytest

from lux.backtest.gerbang import gerbang_forward_fill
from lux.kerangka import bar_per_hari

MS = 3_600_000


def bingkai(n_bergerak: int, n_datar: int, harga: float = 100.0) -> pd.DataFrame:
    """Bingkai dengan bar bergerak lalu ekor datar sempurna sepanjang n_datar."""
    baris = []
    for i in range(n_bergerak):
        p = harga + i
        baris.append(
            {
                "open_time": i * MS,
                "open": p,
                "high": p + 0.5,
                "low": p - 0.5,
                "close": p + 0.25,
            }
        )
    p = harga + n_bergerak
    for j in range(n_datar):
        baris.append(
            {
                "open_time": (n_bergerak + j) * MS,
                "open": p,
                "high": p,
                "low": p,
                "close": p,
            }
        )
    return pd.DataFrame(baris)


def bingkai_datar_tersebar(n: int) -> pd.DataFrame:
    """Bar datar berselang-seling: deret terpanjang 1, tetapi rasionya separuh."""
    baris = []
    for i in range(n):
        p = 100.0 + i
        if i % 2 == 0:
            baris.append(
                {"open_time": i * MS, "open": p, "high": p, "low": p, "close": p}
            )
        else:
            baris.append(
                {
                    "open_time": i * MS,
                    "open": p,
                    "high": p + 0.5,
                    "low": p - 0.5,
                    "close": p + 0.25,
                }
            )
    return pd.DataFrame(baris)


def test_bawaan_masih_24_agar_jalur_1h_bit_identik():
    # 24 bar datar tepat di ambang: lolos. Ini perilaku sebelum ADR-019 dan ia
    # wajib tidak bergerak, sebab sebelas hipotesis lama bergantung padanya.
    g = gerbang_forward_fill(bingkai(300, 24))
    assert g.lulus
    g25 = gerbang_forward_fill(bingkai(300, 25))
    assert not g25.lulus


def test_interval_4h_menurunkan_ambang_deret_ke_enam():
    assert bar_per_hari("4h") == 6
    assert gerbang_forward_fill(bingkai(300, 6), interval="4h").lulus
    assert not gerbang_forward_fill(bingkai(300, 7), interval="4h").lulus


def test_deret_dua_puluh_bar_lolos_1h_tetapi_gagal_4h():
    # Inti ADR-019. Bingkai yang sama, putusan yang berbeda, dan yang berbeda
    # hanyalah arti satu bar.
    df = bingkai(300, 20)
    assert gerbang_forward_fill(df, interval="1h").lulus
    assert not gerbang_forward_fill(df, interval="4h").lulus


def test_interval_menang_atas_maks_deret_datar_eksplisit():
    # Urutan wajib tegas: bila keduanya dipasok, interval yang menentukan.
    df = bingkai(300, 20)
    assert not gerbang_forward_fill(
        df, maks_deret_datar=1000, interval="4h"
    ).lulus
    assert gerbang_forward_fill(df, maks_deret_datar=1, interval="1h").lulus


def test_interval_tak_dikenal_gagal_keras():
    with pytest.raises(SystemExit):
        gerbang_forward_fill(bingkai(300, 5), interval="15m")


def test_rasio_dinilai_terpisah_dari_deret_dan_tetap_yang_dilaporkan():
    # Deret terpanjang hanya 1 bar sehingga syarat deret lolos pada interval apa
    # pun, tetapi rasio 0,5 melewati 0,30. Nilai yang dilaporkan tetap rasio,
    # dan itu memang sudah tercatat sebagai keterbatasan pelaporan di run_wf.
    g = gerbang_forward_fill(bingkai_datar_tersebar(100), interval="4h")
    assert not g.lulus
    assert g.nilai == pytest.approx(0.5)
    assert g.ambang == pytest.approx(0.30)
    assert "deret terpanjang 1 bar" in g.catatan
