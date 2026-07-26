"""Pengujian modul H-013 (ADR-015 bagian B, ADR-020, ADR-021, ADR-022, ADR-023).

Yang diuji di sini adalah **peta sel, satuan jendela, dan aritmetika selisih**,
bukan hasil backtest. Ketiganya justru bagian yang paling mudah salah tanpa
berbunyi: sel yang salah dipetakan tetap menghasilkan empat laporan yang tampak
wajar, jendela yang salah satuan tetap menghasilkan laporan yang rapi dan kosong,
dan selisih yang salah tanda tetap menghasilkan angka yang masuk akal.

Tidak ada pengujian di berkas ini yang memuat bar harga atau memanggil strategi.
Pengacakan diuji lewat ``permutasi_sinyal`` yang berdiri sendiri, persis supaya ia
dapat diuji tanpa bingkai.
"""

from __future__ import annotations

import dataclasses
import inspect

import numpy as np
import pytest

from lux.backtest.engine import Konfig
from lux.backtest.gerbang import gerbang_entri_acak
from lux.backtest.run_h007 import LOOKBACK as LOOKBACK_H007
from lux.backtest.run_h009 import (
    AMBANG_CARRY_KERAS,
    DATASET as DATASET_H009,
    KUNCI_TERLARANG,
)
from lux.backtest.run_h013 import (
    AMBANG_KONTRIBUSI_SINYAL,
    DATASET,
    H_BAR,
    HARI_EMBARGO,
    HARI_LATIH,
    HARI_UJI,
    IMBALAN_BEKU,
    LOOKBACK,
    MIN_TRADE_SEL,
    MIN_ULANGAN,
    NAMA_SEL,
    PEMANASAN,
    SEED_PERMUTASI,
    UMUR_SEL_STOP,
    bar_dibutuhkan,
    buat_konfig_sel,
    hipotesis_h013,
    jendela_bar,
    kandidat,
    kontribusi,
    pakai_target_sel,
    permutasi_sinyal,
    sinyal_acak_sel,
    umur_sel,
)
from lux.backtest.runner import Opsi


def bawaan_opsi(nama: str):
    """Nilai bawaan yang DIDEKLARASIKAN pada medan ``Opsi``.

    Sengaja tidak membangun instans: yang dijaga adalah bawaan pada definisi
    medan, bukan nilai pada satu objek yang kebetulan dibangun.
    """
    for f in dataclasses.fields(Opsi):
        if f.name == nama:
            return f.default
    raise AssertionError(f"Opsi tidak punya medan {nama}")


def test_empat_sel_dan_peta_geometri_serta_sinyal():
    assert NAMA_SEL == ("SS", "SH", "AS", "AH")
    # Huruf pertama sinyal, huruf kedua geometri. Peta yang tertukar akan
    # menghasilkan empat laporan yang tetap tampak wajar.
    assert pakai_target_sel("SS") is True
    assert pakai_target_sel("AS") is True
    assert pakai_target_sel("SH") is False
    assert pakai_target_sel("AH") is False
    assert sinyal_acak_sel("AS") is True
    assert sinyal_acak_sel("AH") is True
    assert sinyal_acak_sel("SS") is False
    assert sinyal_acak_sel("SH") is False
    with pytest.raises(ValueError):
        pakai_target_sel("XX")


def test_kandidat_tiga_kombinasi_dan_imbalan_beku():
    k = kandidat()
    assert len(k) == len(LOOKBACK) == len(list(LOOKBACK_H007))
    # ADR-022: imbalan tidak dilombakan. Bila ia kembali dilombakan, sel
    # bertarget memperoleh keuntungan pemilihan gratis.
    assert {p["imbalan_R"] for p in k} == {IMBALAN_BEKU}
    assert [p["lookback"] for p in k] == list(LOOKBACK_H007)
    for p in k:
        assert KUNCI_TERLARANG not in p
        assert "pakai_target" not in p
        assert "maks_umur_bar" not in p


def test_umur_sel_stop_42_dan_horizon_48():
    # 42 adalah tujuh hari pada 4h; 168 dari config adalah 28 hari dan itulah
    # cacat senyap keenam.
    assert UMUR_SEL_STOP == 42
    assert H_BAR == 48
    assert umur_sel("SS") == 42
    assert umur_sel("AS") == 42
    assert umur_sel("SH") == 48
    assert umur_sel("AH") == 48
    assert UMUR_SEL_STOP != 168


def test_jendela_1h_tidak_bergeser_dari_bawaan_opsi():
    """ADR-023 tidak boleh mengubah arti dua belas laporan yang sudah dikomit.

    Dibandingkan terhadap bawaan ``Opsi`` yang sungguh dipakai H-001b sampai
    H-012, bukan terhadap angka yang diketik ulang di sini.
    """
    j = jendela_bar("1h")
    assert j["panjang_latih"] == bawaan_opsi("panjang_latih") == 4320
    assert j["panjang_uji"] == bawaan_opsi("panjang_uji") == 2160
    assert j["embargo"] == bawaan_opsi("embargo") == 168
    assert PEMANASAN == bawaan_opsi("pemanasan") == 200
    # Dan maksud waktunya memang itu: 180, 90, dan 7 hari pada 1h.
    assert (HARI_LATIH, HARI_UJI, HARI_EMBARGO) == (180, 90, 7)


def test_jendela_4h_dikonversi_dan_muat_di_bawah_lantai():
    """Cacat buta-interval ketujuh: 6.848 bar 4h adalah sekitar 3,1 tahun.

    Dataset 4h hanya sekitar 4.600 bar per simbol dan lantai kelayakannya 2.190
    bar (`universe.min_bar_4h`), jadi tanpa konversi keempat sel menghasilkan nol
    jendela dan laporan yang rapi tetapi kosong.
    """
    j = jendela_bar("4h")
    assert j == {"panjang_latih": 1080, "panjang_uji": 540, "embargo": 42}
    assert bar_dibutuhkan("4h") == 200 + 1080 + 42 + 540 == 1862
    assert bar_dibutuhkan("1h") == 6848
    # Muat di bawah lantai kelayakan 4h, sebagai aritmetika dan bukan harapan.
    assert bar_dibutuhkan("4h") < 2190
    # Tanpa konversi, kebutuhannya justru melampaui panjang rata-rata simbol 4h.
    assert bar_dibutuhkan("1h") > 4600


def test_pemanasan_tidak_dikonversi():
    """Ketidaksimetrisan yang disengaja (ADR-023 keputusan 2).

    Pemanasan adalah kebutuhan bar milik indikator: lookback terbesar 100 ditambah
    ATR 14. Mengonversinya "demi keseragaman" menyisakan 50 bar pada 4h dan
    membuat lookback 100 mustahil dihitung.
    """
    assert PEMANASAN == 200
    assert "pemanasan" not in jendela_bar("4h")
    assert "pemanasan" not in jendela_bar("1h")
    assert PEMANASAN > max(LOOKBACK) + 14


def test_buat_konfig_sel_mewarisi_carry_keras_dan_medan_sel():
    params = {"lookback": 20, "imbalan_R": IMBALAN_BEKU}
    dasar = Konfig(maks_carry_R=0.25)

    ks = buat_konfig_sel("SS")(params, dasar)
    kh = buat_konfig_sel("SH")(params, dasar)

    # Mekanisme H-009 diwarisi apa adanya, tidak disalin.
    assert ks.maks_carry_realisasi_R == AMBANG_CARRY_KERAS
    assert kh.maks_carry_realisasi_R == AMBANG_CARRY_KERAS
    assert ks.imbalan_R == IMBALAN_BEKU

    assert ks.pakai_target is True and ks.maks_umur_bar == 42
    assert kh.pakai_target is False and kh.maks_umur_bar == 48


def test_buat_konfig_sel_menolak_kunci_terlarang():
    """Batas risiko tidak boleh masuk lewat kandidat, juga lewat pembungkus."""
    params = {
        "lookback": 20,
        "imbalan_R": IMBALAN_BEKU,
        KUNCI_TERLARANG: 0.0,
    }
    with pytest.raises(ValueError):
        buat_konfig_sel("SS")(params, Konfig(maks_carry_R=0.25))


def test_permutasi_sinyal_mempertahankan_jumlah_dan_arah():
    s = np.array([1] * 10 + [-1] * 5 + [0] * 85, dtype="int64")
    acak = permutasi_sinyal(s)
    assert acak.size == s.size
    # Jumlah dan arah entri persis sama; hanya waktunya yang hancur.
    assert int((acak == 1).sum()) == 10
    assert int((acak == -1).sum()) == 5
    assert int((acak == 0).sum()) == 85


def test_permutasi_sinyal_deterministik_dan_mengubah_urutan():
    s = np.array([1] * 10 + [0] * 90, dtype="int64")
    a = permutasi_sinyal(s)
    b = permutasi_sinyal(s)
    assert np.array_equal(a, b)
    # Bila urutannya tidak berubah, sel acak bukan sel acak.
    assert not np.array_equal(a, s)


def test_permutasi_memakai_seed_yang_sama_dengan_gerbang():
    """Satu riset, satu mekanisme pengacakan, satu seed.

    Dibaca dari tanda tangan gerbang, bukan disalin sebagai angka, supaya
    perubahan seed di salah satu sisi berbunyi di sini.
    """
    bawaan = inspect.signature(gerbang_entri_acak).parameters["seed"].default
    assert SEED_PERMUTASI == bawaan == 42
    # Dan pengacakannya sungguh rng.permutation dengan seed itu.
    s = np.arange(50)
    harap = np.random.default_rng(42).permutation(s)
    assert np.array_equal(permutasi_sinyal(s), harap)


def test_kontribusi_aritmetika_tiga_selisih():
    e = {"SS": 0.060, "SH": 0.030, "AS": 0.045, "AH": 0.010}
    t = dict.fromkeys(NAMA_SEL, 500)
    r = kontribusi(e, t)
    assert r["dapat_dinilai"] is True
    assert r["sumbangan_sinyal_R"] == pytest.approx(0.015)
    assert r["sumbangan_geometri_R"] == pytest.approx(0.030)
    # (SS-AS) - (SH-AH) = 0,015 - 0,020 = -0,005
    assert r["interaksi_R"] == pytest.approx(-0.005)
    # 0,015 < 0,020 sehingga GAGAL, dan ambangnya tidak boleh bergerak.
    assert r["lulus"] is False
    assert r["ambang_sumbangan_sinyal_R"] == AMBANG_KONTRIBUSI_SINYAL


def test_kontribusi_menolak_sel_yang_kurang():
    with pytest.raises(ValueError):
        kontribusi({"SS": 0.06, "SH": 0.03, "AS": 0.04}, dict.fromkeys(NAMA_SEL, 500))


def test_kontribusi_tidak_dapat_dinilai_bila_trade_kurang():
    """Sel tipis membuat seluruh perbandingan tak ternilai, bukan gagal.

    Menilai selisih dari sel tipis berarti melaporkan kebisingan sebagai temuan;
    menyebutnya gagal berarti menuduh sinyal atas kekurangan data.
    """
    e = {"SS": 0.060, "SH": 0.030, "AS": 0.045, "AH": 0.010}
    t = dict.fromkeys(NAMA_SEL, 500) | {"AH": MIN_TRADE_SEL - 1}
    r = kontribusi(e, t)
    assert r["dapat_dinilai"] is False
    assert r["lulus"] is False
    assert r["sumbangan_sinyal_R"] is None
    assert "AH" in r["sebab"]

    # Ekspektasi yang tidak terdefinisi diperlakukan sama.
    r2 = kontribusi(e | {"SH": None}, dict.fromkeys(NAMA_SEL, 500))
    assert r2["dapat_dinilai"] is False


def test_ambang_pra_registrasi_tidak_bergerak():
    assert AMBANG_KONTRIBUSI_SINYAL == 0.020
    assert MIN_ULANGAN == 300
    assert MIN_TRADE_SEL == 100
    k = hipotesis_h013("SS", Konfig(maks_carry_R=0.25)).kriteria
    assert k.min_ekspektasi_R == 0.05
    assert k.min_trade_luar_sampel == 100
    assert k.maks_p_entri_acak == 0.05
    assert k.min_jendela_positif_rasio == 0.5


def test_dataset_h013_berbeda_dari_h002_dan_menyebut_4h():
    """Tripwire dibalik: di sini kesamaan dataset yang menjadi cacat."""
    assert "4h" in DATASET
    assert DATASET != DATASET_H009
    assert "1h" not in DATASET
    # Sidik keempat sel wajib berbeda, kalau tidak pra-registrasi akan menolak
    # sel kedua sebagai penyuntingan sel pertama.
    sidik = {
        s: hipotesis_h013(s, Konfig(maks_carry_R=0.25)).sidik() for s in NAMA_SEL
    }
    assert len(set(sidik.values())) == len(NAMA_SEL)
