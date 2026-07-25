"""Pengujian pendaftaran keluarga ADR-006.

Yang dikunci: koreksi multiplisitas benar-benar terpasang di kriteria, ketiga
hipotesis punya sidik berbeda, dan ruang pencarian tidak membengkak diam-diam.
"""

from __future__ import annotations

import pytest

from lux.backtest.engine import Konfig
from lux.backtest.run_keluarga import (
    AMBANG_P,
    JUMLAH_PERCOBAAN,
    kriteria,
    semua_spek,
)
from lux.backtest.run_wf import hipotesis_h001

KONFIG = Konfig(maks_umur_bar=168, maks_carry_R=0.25)


def test_ambang_bonferroni():
    assert JUMLAH_PERCOBAAN == 3
    assert AMBANG_P == pytest.approx(0.0167, abs=1e-4)
    assert kriteria().maks_p_entri_acak == AMBANG_P


def test_ambang_p_lebih_ketat_daripada_hipotesis_tunggal():
    """Tiga percobaan serentak tidak boleh dinilai selonggar satu percobaan."""
    assert kriteria().maks_p_entri_acak < hipotesis_h001().kriteria.maks_p_entri_acak


def test_ambang_lain_tidak_dilonggarkan():
    k = kriteria()
    lama = hipotesis_h001().kriteria
    assert k.min_ekspektasi_R == lama.min_ekspektasi_R
    assert k.min_trade_luar_sampel == lama.min_trade_luar_sampel
    assert k.min_jendela_positif_rasio == lama.min_jendela_positif_rasio


def test_tiga_hipotesis_dengan_id_baru():
    assert [s.h.id for s in semua_spek(KONFIG)] == ["H-004", "H-005", "H-006"]


def test_sidik_ketiganya_berbeda():
    sidik = {s.h.sidik() for s in semua_spek(KONFIG)}
    assert len(sidik) == 3


def test_masing_masing_tiga_kombinasi():
    for s in semua_spek(KONFIG):
        assert s.h.jumlah_kombinasi == 3, s.h.id


def test_dataset_identik_dengan_hipotesis_lama():
    for s in semua_spek(KONFIG):
        assert s.h.dataset == hipotesis_h001().dataset


def test_kandidat_cocok_dengan_ruang_terdaftar():
    """Ruang yang didaftarkan harus benar-benar ruang yang dicari."""
    for s in semua_spek(KONFIG):
        assert len(s.kandidat) == s.h.jumlah_kombinasi, s.h.id


def test_nama_laporan_unik():
    nama = [s.nama for s in semua_spek(KONFIG)]
    assert len(set(nama)) == 3
