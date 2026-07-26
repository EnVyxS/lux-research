"""Jalur muat backtest wajib memangkas ekor dengan ambang intervalnya (ADR-019 3c).

Cacat senyap kelima: ``muat_ohlcv`` menerima interval, memakainya untuk memilih
berkas, lalu memanggil pemangkas tanpa meneruskannya. Akibatnya pada 4h ada dua
definisi ekor atas satu dataset — workflow pemangkasan memakai satu hari, jalur
muat backtest memakai empat hari — dan yang menentukan angka hasil hipotesis
adalah yang kedua.

Uji di sini menulis parquet sungguhan lalu menjalankan ``muat_ohlcv`` apa adanya,
jadi yang diuji perilaku dan bukan teks sumber. Kolomnya cukup enam karena
``lux.diag_datar.blok_datar`` memperlakukan ``volume`` dan ``count`` sebagai
opsional; itu diperiksa di sumbernya lebih dulu, bukan diandaikan.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from lux.backtest.run_wf import muat_ohlcv

MS_1H = 3_600_000
MS_4H = 4 * MS_1H
SIMBOL = "XUSDT"


def tulis_parquet(
    direktori: Path, interval: str, n_bergerak: int, n_datar: int
) -> Path:
    """Satu berkas ohlcv dengan ekor datar berharga tunggal di ujungnya."""
    langkah = MS_4H if interval == "4h" else MS_1H
    baris = []
    for i in range(n_bergerak):
        p = 100.0 + i
        baris.append(
            {
                "symbol": SIMBOL,
                "open_time": i * langkah,
                "open": p,
                "high": p + 0.5,
                "low": p - 0.5,
                "close": p + 0.25,
            }
        )
    beku = 100.0 + n_bergerak
    for j in range(n_datar):
        baris.append(
            {
                "symbol": SIMBOL,
                "open_time": (n_bergerak + j) * langkah,
                "open": beku,
                "high": beku,
                "low": beku,
                "close": beku,
            }
        )
    direktori.mkdir(parents=True, exist_ok=True)
    path = direktori / f"ohlcv_{interval}_0001.parquet"
    pd.DataFrame(baris).to_parquet(path, index=False)
    return path


def test_ekor_sehari_pada_4h_dipangkas_saat_muat(tmp_path):
    # Delapan bar 4h adalah lebih dari satu hari, jadi ambang 6 menangkapnya.
    # Dengan bawaan lama 24 bar, ekor ini akan masuk ke backtest utuh.
    tulis_parquet(tmp_path, "4h", n_bergerak=300, n_datar=8)
    bingkai, berkas = muat_ohlcv(tmp_path, "4h", {SIMBOL})
    assert len(berkas) == 1
    assert len(bingkai[SIMBOL]) == 300


def test_ekor_yang_sama_tidak_dipangkas_pada_1h(tmp_path):
    # Bingkai dengan ekor delapan bar yang sama, tetapi pada 1h delapan bar
    # kurang dari sehari sehingga ia BUKAN ekor. Inilah bukti bahwa yang berubah
    # adalah arti satu bar, bukan aturannya.
    tulis_parquet(tmp_path, "1h", n_bergerak=300, n_datar=8)
    bingkai, _ = muat_ohlcv(tmp_path, "1h", {SIMBOL})
    assert len(bingkai[SIMBOL]) == 308


def test_ekor_sehari_penuh_pada_1h_tetap_dipangkas(tmp_path):
    # Perilaku lama, wajib utuh: 24 bar 1h adalah satu hari dan tetap dipangkas
    # persis seperti sebelum ADR-019. Ini yang menjaga H-001b sampai H-012.
    tulis_parquet(tmp_path, "1h", n_bergerak=300, n_datar=24)
    bingkai, _ = muat_ohlcv(tmp_path, "1h", {SIMBOL})
    assert len(bingkai[SIMBOL]) == 300
