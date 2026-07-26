"""Pengujian perambatan hitungan penolakan biaya ke walk-forward (ADR-014).

Bingkai uji di sini dibuat agar jarak stop dapat dihitung tangan. Harga tetap
100, sehingga true range setiap bar sama dengan 2*rentang dan ATR sama dengan
itu. Jarak stop 2*ATR = 4*rentang, jadi stop_frac kira-kira 0,04*rentang.

- rentang 0,1025 -> stop_frac 0,0041 -> di atas lantai 0,004 -> entri diterima
- rentang 0,0975 -> stop_frac 0,0039 -> di bawah lantai -> entri ditolak

Bingkai berubah dari yang pertama ke yang kedua di tengah jalan, sehingga ada
jendela latih yang masih dapat memilih kandidat sementara jendela ujinya sudah
degenerat. Itulah satu-satunya keadaan yang menghasilkan penolakan tercatat:
simbol yang degenerat sepanjang hidupnya membuat seluruh kandidat berskor -inf
dan jendelanya dilewati.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from lux.backtest.engine import Konfig
from lux.backtest.walk_forward import jalankan_walk_forward
from lux.degenerasi import AMBANG_BIAYA_MASUK_R

JAM = 3_600_000
AWAL = 1_600_000_000_000
BATAS_BERUBAH = 450


def bingkai_berubah(n: int = 900) -> pd.DataFrame:
    rentang = [0.1025 if i < BATAS_BERUBAH else 0.0975 for i in range(n)]
    return pd.DataFrame(
        {
            "open_time": [AWAL + i * JAM for i in range(n)],
            "open": [100.0] * n,
            "high": [100.0 + r for r in rentang],
            "low": [100.0 - r for r in rentang],
            "close": [100.0] * n,
        }
    )


def sinyal_periodik(d, params):
    return (np.arange(len(d)) % params["jeda"] == 0).astype(int)


def jalankan(konfig: Konfig):
    return jalankan_walk_forward(
        bingkai_berubah(),
        kandidat=[{"jeda": 20}],
        buat_sinyal=sinyal_periodik,
        panjang_latih=300,
        panjang_uji=150,
        konfig=konfig,
        min_trade_latih=1,
    )


def test_ringkasan_selalu_memuat_kunci_penolakan():
    r = jalankan(Konfig()).ringkas()
    assert r["entri_ditolak_biaya"] == 0
    assert r["jumlah_trade_luar_sampel"] > 0


def test_penolakan_tercatat_ketika_pengaman_menyala():
    hasil = jalankan(Konfig(maks_biaya_masuk_R=AMBANG_BIAYA_MASUK_R))
    assert hasil.entri_ditolak_biaya > 0
    assert hasil.ringkas()["entri_ditolak_biaya"] == hasil.entri_ditolak_biaya


def test_penolakan_dijumlahkan_dari_jendela_uji_saja():
    hasil = jalankan(Konfig(maks_biaya_masuk_R=AMBANG_BIAYA_MASUK_R))
    assert hasil.entri_ditolak_biaya == sum(
        h.hasil_uji.entri_ditolak_biaya for h in hasil.per_jendela
    )


def test_pengaman_tidak_menghapus_perdagangan_di_wilayah_sehat():
    mati = jalankan(Konfig())
    nyala = jalankan(Konfig(maks_biaya_masuk_R=AMBANG_BIAYA_MASUK_R))
    # Jendela uji yang masih sehat tetap berdagang; yang hilang hanya yang
    # berada di wilayah degenerat.
    assert nyala.ringkas()["jumlah_trade_luar_sampel"] > 0
    assert (
        nyala.ringkas()["jumlah_trade_luar_sampel"]
        <= mati.ringkas()["jumlah_trade_luar_sampel"]
    )
