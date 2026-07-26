"""Pengujian orkestrator H-009 (ADR-009).

Inti ADR-009 hanya satu kalimat: batas risiko tidak dilombakan. Sebagian besar
pengujian di bawah ini ada untuk membuat pelanggaran kalimat itu gagal secara
mekanis, bukan sekadar tercela secara moral.
"""

from __future__ import annotations

import pytest

from lux.backtest.engine import Konfig
from lux.backtest.run_h002 import hipotesis_h002
from lux.backtest.run_h007 import IMBALAN as IMBALAN_H007
from lux.backtest.run_h007 import LOOKBACK as LOOKBACK_H007
from lux.backtest.run_h008 import CARRY_KERAS as CARRY_KERAS_H008
from lux.backtest.run_h008 import hipotesis_h008
from lux.backtest.run_h009 import (
    AMBANG_CARRY_KERAS,
    IMBALAN,
    KUNCI_TERLARANG,
    LOOKBACK,
    RAMALAN,
    buat_konfig,
    hipotesis_h009,
    kandidat,
    spek_h009,
)

DASAR = Konfig(maks_umur_bar=168, maks_carry_R=0.25)


def test_jumlah_kandidat():
    k = kandidat()
    assert len(k) == len(LOOKBACK) * len(IMBALAN) == 12
    assert len({tuple(sorted(d.items())) for d in k}) == 12


def test_grid_identik_dengan_h007():
    """Grid H-009 wajib sama persis dengan H-007, tanpa penyempitan diam-diam."""
    assert LOOKBACK == LOOKBACK_H007
    assert IMBALAN == IMBALAN_H007


def test_grid_bukan_objek_yang_sama_dengan_h007():
    """Menyalin nilainya, bukan berbagi daftarnya."""
    assert LOOKBACK is not LOOKBACK_H007
    assert IMBALAN is not IMBALAN_H007


def test_imbalan_tidak_dipatok_ke_pemenang_h007():
    """4,0 menang di 194 dari 356 jendela; mematoknya adalah penyetelan pasca-hoc."""
    assert len(IMBALAN) == 4
    assert 1.0 in IMBALAN


def test_pengaman_tidak_muncul_di_kandidat():
    """Inti ADR-009: pemilih tidak boleh menyentuh batas risiko."""
    for p in kandidat():
        assert KUNCI_TERLARANG not in p
        assert set(p) == {"lookback", "imbalan_R"}


def test_pengaman_menyala_di_setiap_kandidat_tanpa_kecuali():
    for p in kandidat():
        k = buat_konfig(p, DASAR)
        assert k.maks_carry_realisasi_R == AMBANG_CARRY_KERAS
        assert k.maks_carry_realisasi_R > 0


def test_tidak_ada_jalan_mematikan_pengaman():
    """Kandidat yang menyelundupkan ambang harus ditolak, bukan dipatuhi."""
    with pytest.raises(ValueError):
        buat_konfig(
            {"lookback": 55, "imbalan_R": 2.0, KUNCI_TERLARANG: 0.0}, DASAR
        )


def test_ambang_bukan_pemenang_pasca_hoc():
    """0,25 adalah salah satu pilihan di H-008 dan ia KALAH, 22 lawan 334.

    Nilai ini diwarisi dari config/lux.yaml v2 sejak ADR-004, jauh sebelum
    hasil H-008 terlihat. Ia dipilih karena sudah ditetapkan, bukan karena
    menang.
    """
    assert AMBANG_CARRY_KERAS == 0.25
    assert AMBANG_CARRY_KERAS in CARRY_KERAS_H008
    assert AMBANG_CARRY_KERAS != 0.0


def test_buat_konfig_mengubah_dua_medan_saja():
    hasil = buat_konfig({"lookback": 55, "imbalan_R": 3.0}, DASAR)
    assert hasil.imbalan_R == 3.0
    assert hasil.maks_carry_realisasi_R == AMBANG_CARRY_KERAS
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


def test_saringan_adr004_tetap_menyala():
    """ADR-009 menambah pengaman keras, tidak menukar saringan proyeksi."""
    for p in kandidat():
        assert buat_konfig(p, DASAR).maks_carry_R == DASAR.maks_carry_R


def test_dataset_identik_dengan_h002():
    """Beda satu karakter pun membuat perbandingan tidak sah."""
    assert hipotesis_h009(DASAR).dataset == hipotesis_h002(DASAR).dataset


def test_identitas_dan_kriteria_tidak_dilonggarkan():
    h = hipotesis_h009(DASAR)
    assert h.id == "H-009"
    assert h.kriteria.min_ekspektasi_R == 0.05
    assert h.kriteria.min_trade_luar_sampel == 100
    assert h.kriteria.maks_p_entri_acak == 0.05
    assert h.kriteria.min_jendela_positif_rasio == 0.5


def test_kriteria_sama_persis_dengan_h008():
    """Ambang tidak boleh bergeser di antara dua percobaan yang dibandingkan."""
    a = hipotesis_h009(DASAR).kriteria
    b = hipotesis_h008(DASAR).kriteria
    assert a == b


def test_ambang_ikut_ke_dalam_sidik():
    """Menjalankan ulang dengan ambang lain wajib menghasilkan sidik berbeda."""
    rp = hipotesis_h009(DASAR).ruang_parameter
    assert rp[KUNCI_TERLARANG] == [AMBANG_CARRY_KERAS]


def test_sidik_berbeda_dari_h008():
    """H-009 adalah percobaan baru, bukan H-008 yang dihitung ulang."""
    assert hipotesis_h009(DASAR).sidik() != hipotesis_h008(DASAR).sidik()


def test_sidik_berubah_saat_konfig_dasar_berubah():
    lain = Konfig(maks_umur_bar=168, maks_carry_R=0.50)
    assert hipotesis_h009(DASAR).sidik() != hipotesis_h009(lain).sidik()


def test_jumlah_kombinasi_cocok_dengan_kandidat():
    assert hipotesis_h009(DASAR).jumlah_kombinasi == len(kandidat())


def test_pernyataan_menyebut_invarian_risiko():
    assert "invarian_risiko" in hipotesis_h009(DASAR).pernyataan


def test_ramalan_ditulis_sebelum_run():
    """Termasuk ramalan yang merugikan hipotesis ini sendiri."""
    assert set(RAMALAN) == {
        "keluar_carry",
        "kerugian_terburuk_R",
        "ekspektasi_R",
    }
    assert "turun" in RAMALAN["ekspektasi_R"]


def test_spek():
    s = spek_h009(DASAR)
    assert s.nama == "h009_carry_dipatok"
    assert s.params_lookahead == {"lookback": 55}
    assert s.buat_konfig is not None
    assert len(s.kandidat) == 12


def test_strategi_tidak_disentuh():
    """ADR-006 melarang sinyal harga ketujuh; H-009 memakai sinyal H-002."""
    from lux.strategi import breakout_atr

    assert spek_h009(DASAR).sinyal is breakout_atr.sinyal


@pytest.mark.parametrize("p", kandidat())
def test_setiap_kandidat_menghasilkan_konfig_sah(p):
    k = buat_konfig(p, DASAR)
    assert k.imbalan_R > 0
    assert k.maks_carry_realisasi_R == AMBANG_CARRY_KERAS
