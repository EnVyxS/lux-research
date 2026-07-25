"""Pengujian pendaftaran H-007."""

from __future__ import annotations

import pytest

from lux.backtest.engine import Konfig
from lux.backtest.run_h007 import IMBALAN, LOOKBACK, hipotesis_h007, kandidat, spek_h007
from lux.backtest.run_wf import hipotesis_h001

KONFIG = Konfig(maks_umur_bar=168, maks_carry_R=0.25)


def test_id_dan_jumlah_kombinasi():
    h = hipotesis_h007(KONFIG)
    assert h.id == "H-007"
    assert h.jumlah_kombinasi == len(LOOKBACK) * len(IMBALAN) == 12


def test_kandidat_cocok_dengan_ruang_terdaftar():
    assert len(kandidat()) == hipotesis_h007(KONFIG).jumlah_kombinasi


def test_imbalan_baku_ikut_diuji():
    """2R harus ada agar hasilnya dapat disandingkan dengan H-002."""
    assert 2.0 in IMBALAN


def test_kriteria_sama_dengan_hipotesis_tunggal_lama():
    """Percobaan tunggal: tidak ada koreksi multiplisitas, tidak ada pelonggaran."""
    k = hipotesis_h007(KONFIG).kriteria
    lama = hipotesis_h001().kriteria
    assert k.min_ekspektasi_R == lama.min_ekspektasi_R
    assert k.maks_p_entri_acak == lama.maks_p_entri_acak
    assert k.min_trade_luar_sampel == lama.min_trade_luar_sampel
    assert k.min_jendela_positif_rasio == lama.min_jendela_positif_rasio


def test_dataset_identik():
    assert hipotesis_h007(KONFIG).dataset == hipotesis_h001().dataset


def test_sidik_berbeda_dari_hipotesis_lama():
    assert hipotesis_h007(KONFIG).sidik() != hipotesis_h001().sidik()


def test_stop_tidak_ikut_dicari():
    """ADR-007 mengunci stop; hanya satu nilai yang boleh terdaftar."""
    ruang = hipotesis_h007(KONFIG).ruang_parameter
    assert ruang["atr_pengali_stop"] == [KONFIG.atr_pengali_stop]


def test_spek_membawa_konfig_per_kandidat():
    s = spek_h007(KONFIG)
    assert s.buat_konfig is not None
    assert s.nama == "h007_keluar"


def test_spek_memakai_sinyal_lama_tanpa_perubahan():
    """ADR-006 melarang sinyal harga baru; H-007 memakai Donchian apa adanya."""
    from lux.strategi.breakout_atr import sinyal as sinyal_breakout

    assert spek_h007(KONFIG).sinyal is sinyal_breakout


def test_setiap_kandidat_punya_dua_kunci():
    for k in kandidat():
        assert set(k) == {"lookback", "imbalan_R"}
        assert k["imbalan_R"] in IMBALAN
        assert k["lookback"] in LOOKBACK
}