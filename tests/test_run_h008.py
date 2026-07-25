"""Pengujian orkestrator H-008 (ADR-008)."""

from __future__ import annotations

import pytest

from lux.backtest.engine import Konfig
from lux.backtest.run_h002 import hipotesis_h002
from lux.backtest.run_h008 import (
    CARRY_KERAS,
    IMBALAN,
    LOOKBACK,
    buat_konfig,
    hipotesis_h008,
    kandidat,
    spek_h008,
)
from lux.backtest.run_h007 import IMBALAN as IMBALAN_H007
from lux.backtest.run_h007 import LOOKBACK as LOOKBACK_H007

DASAR = Konfig(maks_umur_bar=168, maks_carry_R=0.25)


def test_jumlah_kandidat():
    k = kandidat()
    assert len(k) == len(LOOKBACK) * len(IMBALAN) * len(CARRY_KERAS) == 36
    assert len({tuple(sorted(d.items())) for d in k}) == 36


def test_grid_lookback_dan_imbalan_identik_dengan_h007():
    """Mempersempit grid setelah melihat hasil H-007 adalah penyetelan pasca-hoc."""
    assert LOOKBACK == LOOKBACK_H007
    assert IMBALAN == IMBALAN_H007


def test_nol_ikut_dilombakan():
    """Tanpa 0,0 percobaan ini hanya bisa membenarkan gagasannya sendiri."""
    assert 0.0 in CARRY_KERAS


def test_buat_konfig_mengubah_dua_medan_saja():
    hasil = buat_konfig(
        {"lookback": 55, "imbalan_R": 3.0, "maks_carry_realisasi_R": 0.25}, DASAR
    )
    assert hasil.imbalan_R == 3.0
    assert hasil.maks_carry_realisasi_R == 0.25
    # Semua medan lain diwarisi apa adanya.
    for medan in (
        "fee",
        "slippage",
        "atr_periode",
        "atr_pengali_stop",
        "risiko_per_trade",
        "modal_awal",
        "izinkan_short",
        "maks_umur_bar",
        "maks_carry_R",
        "jendela_carry_hari",
    ):
        assert getattr(hasil, medan) == getattr(DASAR, medan)


def test_saringan_adr004_tetap_menyala_di_tiap_kandidat():
    """ADR-008 menambah pengaman, bukan menukarnya dengan yang lama."""
    for p in kandidat():
        assert buat_konfig(p, DASAR).maks_carry_R == DASAR.maks_carry_R


def test_kandidat_nol_berarti_pengaman_mati():
    hasil = buat_konfig(
        {"lookback": 20, "imbalan_R": 2.0, "maks_carry_realisasi_R": 0.0}, DASAR
    )
    assert hasil.maks_carry_realisasi_R == 0.0


def test_setiap_kandidat_menghasilkan_konfig_sah():
    for p in kandidat():
        k = buat_konfig(p, DASAR)
        assert k.imbalan_R > 0
        assert k.maks_carry_realisasi_R >= 0


def test_dataset_identik_dengan_h002():
    """Beda satu karakter pun membuat perbandingan tidak sah."""
    assert hipotesis_h008(DASAR).dataset == hipotesis_h002(DASAR).dataset


def test_identitas_dan_kriteria():
    h = hipotesis_h008(DASAR)
    assert h.id == "H-008"
    assert h.kriteria.min_ekspektasi_R == 0.05
    assert h.kriteria.min_trade_luar_sampel == 100
    # Percobaan tunggal: tidak ada koreksi multiplisitas.
    assert h.kriteria.maks_p_entri_acak == 0.05
    assert h.kriteria.min_jendela_positif_rasio == 0.5


def test_jumlah_kombinasi_cocok_dengan_kandidat():
    assert hipotesis_h008(DASAR).jumlah_kombinasi == len(kandidat())


def test_pernyataan_menyebut_invarian_risiko():
    """Hipotesis ini menargetkan gerbang, bukan hanya ekspektasi."""
    assert "invarian_risiko" in hipotesis_h008(DASAR).pernyataan


def test_sidik_berubah_saat_ambang_berubah():
    """Percobaan diam-diam dengan ambang lain harus tertolak pra-registrasi."""
    lain = Konfig(maks_umur_bar=168, maks_carry_R=0.50)
    assert hipotesis_h008(DASAR).sidik() != hipotesis_h008(lain).sidik()


def test_spek():
    s = spek_h008(DASAR)
    assert s.nama == "h008_carry_keras"
    assert s.params_lookahead == {"lookback": 55}
    assert s.buat_konfig is not None
    assert len(s.kandidat) == 36


def test_strategi_tidak_disentuh():
    """ADR-006 melarang sinyal harga ketujuh; H-008 memakai sinyal H-002."""
    from lux.strategi import breakout_atr

    assert spek_h008(DASAR).sinyal is breakout_atr.sinyal


@pytest.mark.parametrize("ck", CARRY_KERAS)
def test_semua_ambang_tidak_negatif(ck):
    assert ck >= 0.0
