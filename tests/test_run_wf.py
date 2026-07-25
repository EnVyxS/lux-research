"""Pengujian orkestrator walk-forward."""

from __future__ import annotations

import pandas as pd
import pytest

from lux.backtest.run_wf import (
    hipotesis_h001,
    pilih_berkas,
    ringkas_gabungan,
    sha256_berkas,
    simbol_mati,
)

HARI = 86_400_000
AWAL = 1_600_000_000_000


def bingkai_sampai(akhir_ms, n=10):
    return pd.DataFrame({"open_time": [akhir_ms - (n - 1 - i) * HARI for i in range(n)]})


def test_simbol_mati_dikenali_dari_data_sendiri():
    b = {
        "HIDUP": bingkai_sampai(AWAL + 400 * HARI),
        "MATI": bingkai_sampai(AWAL + 100 * HARI),
    }
    assert simbol_mati(b) == {"MATI"}


def test_simbol_yang_baru_berhenti_belum_dianggap_mati():
    b = {
        "A": bingkai_sampai(AWAL + 400 * HARI),
        "B": bingkai_sampai(AWAL + 390 * HARI),
    }
    assert simbol_mati(b, ambang_hari=30) == set()


def test_simbol_mati_pada_kumpulan_kosong():
    assert simbol_mati({}) == set()


def test_ekspektasi_gabungan_menimbang_jumlah_perdagangan():
    """Simbol dengan tiga trade tidak boleh setara dengan yang tiga ratus."""
    kecil = {
        "jumlah_trade_luar_sampel": 3,
        "total_R": 3.0,
        "jumlah_jendela": 1,
        "jendela_positif": 1,
    }
    besar = {
        "jumlah_trade_luar_sampel": 300,
        "total_R": -30.0,
        "jumlah_jendela": 5,
        "jendela_positif": 1,
    }
    g = ringkas_gabungan([kecil, besar])
    assert g["jumlah_trade_luar_sampel"] == 303
    assert g["ekspektasi_R"] == pytest.approx(-27.0 / 303)
    assert g["ekspektasi_R"] < 0


def test_gabungan_tanpa_trade_tidak_mengarang_ekspektasi():
    g = ringkas_gabungan(
        [{"jumlah_trade_luar_sampel": 0, "total_R": 0.0, "jumlah_jendela": 2, "jendela_positif": 0}]
    )
    assert g["ekspektasi_R"] is None


def test_aset_retry_tidak_pernah_ikut_terbaca(tmp_path):
    """Aturan yang sama dengan validasi, diulang agar tidak diam-diam berubah."""
    (tmp_path / "ohlcv_1h_shard00.parquet").write_bytes(b"x")
    (tmp_path / "ohlcv_1h_retry_shard00.parquet").write_bytes(b"x")
    nama = [p.name for p in pilih_berkas(tmp_path, "1h")]
    assert nama == ["ohlcv_1h_shard00.parquet"]


def test_sha256_berkas_stabil(tmp_path):
    p = tmp_path / "a.bin"
    p.write_bytes(b"lux")
    assert sha256_berkas(p) == sha256_berkas(p)
    assert len(sha256_berkas(p)) == 64


def test_hipotesis_h001_terkunci_pada_kriteria_yang_ketat():
    h = hipotesis_h001()
    assert h.kriteria.min_trade_luar_sampel == 100
    assert h.kriteria.maks_p_entri_acak == 0.05
    assert h.jumlah_kombinasi == 3
