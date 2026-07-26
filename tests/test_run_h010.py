"""Pengujian H-010 (ADR-012): dinding grid digeser, sisanya tidak berubah.

Yang dijaga di sini bukan kebenaran hipotesisnya, melainkan bahwa percobaan
ini mengubah TEPAT SATU hal terhadap H-009. Setiap pengujian di bawah
menutup satu cara percobaan ini bisa menjadi dua percobaan sekaligus tanpa
saya sadari.
"""

from __future__ import annotations

import pytest

from lux.backtest import run_h009, run_h010
from lux.backtest.engine import Konfig
from lux.backtest.run_h007 import IMBALAN as IMBALAN_H007
from lux.backtest.run_h007 import LOOKBACK as LOOKBACK_H007


def test_jumlah_kombinasi_identik_dengan_h009():
    # Multiplisitas yang sama berarti ambang p 0,05 tetap sebanding. Dihitung
    # dari kedua fungsi, bukan dari angka 12 yang ditulis tangan.
    assert len(run_h010.kandidat()) == len(run_h009.kandidat())


def test_lookback_tidak_disentuh():
    assert run_h010.LOOKBACK == list(LOOKBACK_H007)


def test_grid_imbalan_benar_benar_bergeser():
    assert run_h010.IMBALAN != list(IMBALAN_H007)


def test_dinding_bergeser_ke_luar_bukan_ke_dalam():
    assert max(run_h010.IMBALAN) > max(IMBALAN_H007)


def test_jangkar_pembanding_bertahan():
    # Tanpa 2,0 dan 4,0 di grid, perubahan ekspektasi tidak dapat dipisahkan
    # dari perubahan grid.
    for j in run_h010.JANGKAR:
        assert j in run_h010.IMBALAN


def test_grid_imbalan_naik_dan_tanpa_duplikat():
    assert run_h010.IMBALAN == sorted(set(run_h010.IMBALAN))


def test_buat_konfig_adalah_fungsi_h009_apa_adanya():
    # Bukan salinan. Salinan bisa melenceng; identitas objek tidak bisa.
    assert run_h010.buat_konfig is run_h009.buat_konfig


def test_pengaman_carry_terpasang_pada_setiap_kandidat():
    dasar = Konfig()
    for p in run_h010.kandidat():
        k = run_h010.buat_konfig(p, dasar)
        assert k.maks_carry_realisasi_R == run_h010.AMBANG_CARRY_KERAS
        assert k.imbalan_R == p["imbalan_R"]


def test_kunci_terlarang_ditolak_di_buat_konfig():
    with pytest.raises(ValueError):
        run_h010.buat_konfig(
            {"imbalan_R": 8.0, run_h010.KUNCI_TERLARANG: 0.5}, Konfig()
        )


def test_kunci_terlarang_tidak_bocor_ke_kandidat():
    for p in run_h010.kandidat():
        assert run_h010.KUNCI_TERLARANG not in p


def test_dataset_identik_dengan_h009():
    assert run_h010.DATASET == run_h009.DATASET


def test_kriteria_tidak_dilonggarkan():
    kr = run_h010.hipotesis_h010(Konfig()).kriteria
    assert kr.min_ekspektasi_R == 0.05
    assert kr.min_trade_luar_sampel == 100
    assert kr.maks_p_entri_acak == 0.05
    assert kr.min_jendela_positif_rasio == 0.5


def test_sidik_berbeda_dari_h009():
    # Grid yang berbeda wajib menghasilkan sidik berbeda, kalau tidak
    # pra-registrasi tidak bisa membedakan kedua percobaan.
    k = Konfig()
    assert (
        run_h010.hipotesis_h010(k).sidik() != run_h009.hipotesis_h009(k).sidik()
    )


def test_ambang_carry_ikut_ke_dalam_ruang_parameter():
    ruang = run_h010.hipotesis_h010(Konfig()).ruang_parameter
    assert ruang[run_h010.KUNCI_TERLARANG] == [run_h010.AMBANG_CARRY_KERAS]


def test_ramalan_lengkap_sebelum_run():
    for kunci in (
        "porsi_jendela_imbalan_8",
        "laju_kena_target",
        "porsi_tak_selesai",
        "porsi_funding_ekor_maks",
        "ekspektasi_R",
    ):
        assert kunci in run_h010.RAMALAN


def test_pembanding_memuat_h009():
    assert "H-009" in run_h010.PEMBANDING
