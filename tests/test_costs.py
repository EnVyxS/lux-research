"""Pengujian model biaya.

Pengujian ini menjaga sifat-sifat yang harus benar apa pun implementasinya,
bukan sekadar mengunci angka keluaran hari ini.

Catatan atas satu kegagalan nyata: versi pertama berkas ini menuntut
``winrate_impas(2.0, 2.0) > 1.0``, padahal aritmetikanya menghasilkan tepat
1,0. Yang salah adalah asersinya, bukan implementasinya, dan kesalahan itu
ditangkap oleh CI sebelum sempat memengaruhi keputusan apa pun. Pengujian yang
menuntut hal keliru adalah bahaya tersendiri: ia mengundang orang menambal kode
yang sudah benar.
"""

from __future__ import annotations

import math

import pytest

from lux.costs import (
    ModelBiaya,
    biaya_dalam_R,
    funding_dalam_R,
    layak_secara_biaya,
    stop_frac,
    total_biaya_R,
    winrate_impas,
)


def test_stop_frac_dasar():
    assert stop_frac(atr=100.0, harga=10000.0, pengali=2.0) == pytest.approx(0.02)


def test_stop_frac_menolak_harga_tidak_masuk_akal():
    with pytest.raises(ValueError):
        stop_frac(atr=1.0, harga=0.0)


def test_biaya_bolak_balik_dua_kali_satu_sisi():
    m = ModelBiaya(fee=0.0005, slippage=0.0005)
    assert m.biaya_bolak_balik == pytest.approx(2 * m.biaya_satu_sisi)


def test_biaya_R_pada_stop_dua_persen():
    # Biaya bolak-balik 0,2% terhadap stop 2% berarti seperspuluh R.
    assert biaya_dalam_R(0.02) == pytest.approx(0.1)


def test_stop_lebih_sempit_berarti_biaya_lebih_besar():
    assert biaya_dalam_R(0.005) > biaya_dalam_R(0.02)


def test_funding_berbanding_lurus_dengan_lama_tahan():
    a = funding_dalam_R(0.0001, jam_ditahan=8, stop_pecahan=0.02)
    b = funding_dalam_R(0.0001, jam_ditahan=24, stop_pecahan=0.02)
    assert b == pytest.approx(3 * a)


def test_funding_berbalik_tanda_untuk_short():
    long = funding_dalam_R(0.0001, 8, 0.02, arah=1)
    short = funding_dalam_R(0.0001, 8, 0.02, arah=-1)
    assert long == pytest.approx(-short)


def test_funding_nol_saat_tidak_ditahan():
    assert funding_dalam_R(0.01, 0.0, 0.02) == 0.0


def test_total_biaya_menjumlahkan_kedua_komponen():
    total = total_biaya_R(0.02, funding_rate=0.0001, jam_ditahan=8)
    assert total == pytest.approx(biaya_dalam_R(0.02) + funding_dalam_R(0.0001, 8, 0.02))


def test_winrate_impas_tanpa_biaya_sesuai_teori():
    # Dengan imbalan 1R dan tanpa biaya, titik impas ada di 50%.
    assert winrate_impas(1.0, 0.0) == pytest.approx(0.5)
    # Dengan imbalan 2R dan tanpa biaya, cukup sepertiga.
    assert winrate_impas(2.0, 0.0) == pytest.approx(1 / 3)


def test_biaya_menaikkan_ambang_impas():
    tanpa = winrate_impas(2.0, 0.0)
    dengan = winrate_impas(2.0, biaya_dalam_R(0.02))
    assert dengan > tanpa


def test_stop_sangat_sempit_membuat_strategi_mustahil():
    # Stop 0,1% dengan biaya 0,2% bolak-balik berarti dua R hilang sebelum
    # perdagangan dimulai. Pada imbalan 2R, titik impasnya tepat 100% dan
    # kemenangan pun hanya menghasilkan nol, jadi konfigurasi ini mati.
    biaya = biaya_dalam_R(0.001)
    assert biaya == pytest.approx(2.0)
    assert winrate_impas(2.0, biaya) == pytest.approx(1.0)
    assert not layak_secara_biaya(2.0, biaya)


def test_ambang_impas_boleh_melebihi_satu():
    # Tidak boleh dijepit ke 1,0: angka di atas satu adalah cara rumus ini
    # menyatakan bahwa konfigurasinya mustahil.
    assert winrate_impas(1.0, 2.0) > 1.0
    assert not layak_secara_biaya(1.0, 2.0)


def test_konfigurasi_wajar_dinyatakan_layak():
    biaya = biaya_dalam_R(0.02)
    assert layak_secara_biaya(2.0, biaya)
    assert winrate_impas(2.0, biaya) < 0.4


def test_semua_masukan_tidak_masuk_akal_ditolak():
    with pytest.raises(ValueError):
        biaya_dalam_R(0.0)
    with pytest.raises(ValueError):
        funding_dalam_R(0.0001, 8, 0.02, arah=0)
    with pytest.raises(ValueError):
        funding_dalam_R(0.0001, -1, 0.02)
    with pytest.raises(ValueError):
        winrate_impas(0.0, 0.1)
    with pytest.raises(ValueError):
        layak_secara_biaya(0.0, 0.1)


def test_tidak_ada_nilai_nan_yang_lolos():
    nilai = total_biaya_R(0.02, 0.0001, 8)
    assert math.isfinite(nilai)
