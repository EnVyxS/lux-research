"""Pengujian orkestrator H-002.

Yang dikunci di sini bukan hasil backtestnya, melainkan tiga hal yang bila
rusak akan membuat seluruh perbandingan H-001b vs H-002 kehilangan arti:
konfig yang benar-benar terbaca dari berkas, hipotesis yang ambangnya tidak
dilonggarkan, dan sidik yang berubah bila nilai saringan diubah.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lux.backtest.engine import Konfig
from lux.backtest.run_h002 import banding_h001, hipotesis_h002, muat_konfig_h002
from lux.backtest.run_wf import hipotesis_h001

AKAR = Path(__file__).resolve().parents[1]


def test_config_nyata_memuat_kedua_saringan():
    """Config yang dipakai produksi harus benar-benar menyalakan saringan."""
    k = muat_konfig_h002(AKAR / "config" / "lux.yaml")
    assert k.maks_umur_bar == 168
    assert k.maks_carry_R == 0.25
    assert k.jendela_carry_hari == 30


def test_config_tanpa_saringan_ditolak(tmp_path):
    """H-002 dengan saringan mati adalah H-001b dengan nama lain."""
    p = tmp_path / "c.yaml"
    p.write_text(
        "biaya:\n  fee_efektif: 0.0005\n  slippage: 0.0005\n"
        "risiko:\n  atr_periode: 14\n  atr_pengali_stop: 2.0\n"
        "  risiko_per_trade: 0.005\n  maks_umur_bar: 0\n  maks_carry_R: 0.0\n"
        "  jendela_carry_hari: 30\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        muat_konfig_h002(p)


def test_config_tanpa_kunci_gagal_keras(tmp_path):
    p = tmp_path / "c.yaml"
    p.write_text(
        "biaya:\n  fee_efektif: 0.0005\n  slippage: 0.0005\n"
        "risiko:\n  atr_periode: 14\n  atr_pengali_stop: 2.0\n"
        "  risiko_per_trade: 0.005\n",
        encoding="utf-8",
    )
    with pytest.raises(KeyError):
        muat_konfig_h002(p)


def test_ambang_h002_sama_persis_dengan_h001b():
    """Tidak satu angka pun boleh dilonggarkan setelah H-001b ditolak."""
    a = hipotesis_h001().kriteria
    b = hipotesis_h002(Konfig(maks_umur_bar=168, maks_carry_R=0.25)).kriteria
    assert a == b


def test_dataset_h002_identik_dengan_h001b():
    """Perbandingan hanya sah bila datanya sama."""
    assert (
        hipotesis_h002(Konfig(maks_umur_bar=168, maks_carry_R=0.25)).dataset
        == hipotesis_h001().dataset
    )


def test_ruang_pencarian_tetap_kecil_dan_menyebut_saringan():
    h = hipotesis_h002(Konfig(maks_umur_bar=168, maks_carry_R=0.25))
    assert h.jumlah_kombinasi == 3
    assert h.ruang_parameter["maks_umur_bar"] == [168]
    assert h.ruang_parameter["maks_carry_R"] == [0.25]


def test_sidik_berubah_bila_saringan_diubah():
    """Percobaan diam-diam dengan nilai lain harus tertolak praregistrasi."""
    a = hipotesis_h002(Konfig(maks_umur_bar=168, maks_carry_R=0.25)).sidik()
    b = hipotesis_h002(Konfig(maks_umur_bar=72, maks_carry_R=0.25)).sidik()
    assert a != b


def test_banding_tanpa_laporan_lama_bukan_error(tmp_path):
    assert banding_h001(tmp_path / "tidak_ada.json") is None


def test_banding_membaca_angka_dari_berkas(tmp_path):
    p = tmp_path / "backtest_h001.json"
    p.write_text(
        json.dumps(
            {
                "gabungan": {
                    "ekspektasi_R": 0.0309,
                    "total_R": 589.17,
                    "jumlah_trade_luar_sampel": 19093,
                },
                "gerbang": {
                    "gerbang": [
                        {"nama": "invarian_risiko", "nilai": -2.5853},
                        {"nama": "checksum", "nilai": 0.0},
                    ]
                },
                "putusan": {"lulus": False},
            }
        ),
        encoding="utf-8",
    )
    b = banding_h001(p)
    assert b["invarian_risiko"] == -2.5853
    assert b["lulus"] is False
