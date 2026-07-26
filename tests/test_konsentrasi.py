"""Pengujian gerbang konsentrasi (ADR-010).

Yang dikunci di sini bukan hanya bahwa gerbangnya bekerja, melainkan bahwa ia
tidak mengulang kekeliruan yang melahirkannya: penyebut yang dipakai harus
bruto, sehingga porsi tidak pernah bisa melewati satu.
"""

from __future__ import annotations

import pytest

from lux.backtest.konsentrasi import (
    AMBANG_RETENSI_DROP_1,
    Kontribusi,
    dari_per_simbol,
    dari_ringkasan,
    gerbang_konsentrasi,
    jumlah_drop_5persen,
    tabel_jackknife,
    ukur_konsentrasi,
)


def kon(sym: str, r: float, tr: int = 10) -> Kontribusi:
    return Kontribusi(symbol=sym, total_R=float(r), trade=int(tr))


def datar(n: int = 20, r: float = 1.0, tr: int = 10) -> list[Kontribusi]:
    """Portofolio yang keunggulannya tersebar rata sempurna."""
    return [kon(f"S{i:02d}", r, tr) for i in range(n)]


# --- kasus yang tidak dapat dinilai --------------------------------------
def test_portofolio_kosong_gagal_bukan_lulus():
    g = gerbang_konsentrasi([])
    assert not g.lulus and not g.dapat_dinilai


def test_satu_simbol_tidak_dapat_dinilai():
    """Sebaran satu simbol bukan sebaran, dan diam bukan kelulusan."""
    g = gerbang_konsentrasi([kon("A", 10.0)])
    assert not g.lulus and not g.dapat_dinilai
    assert "dua simbol" in g.catatan


def test_semua_simbol_merugi_tidak_dapat_dinilai():
    """Retensi adalah rasio; penyebut negatif membuatnya terbaca terbalik."""
    g = gerbang_konsentrasi([kon(f"S{i}", -1.0) for i in range(5)])
    assert not g.lulus and not g.dapat_dinilai


def test_simbol_tanpa_perdagangan_diabaikan():
    u = ukur_konsentrasi(datar(20) + [kon("Z", 0.0, 0)])
    assert u["n_simbol"] == 20


# --- kasus bersih dan kasus kotor ----------------------------------------
def test_portofolio_datar_lulus():
    g = gerbang_konsentrasi(datar(20))
    assert g.lulus
    assert g.nama == "konsentrasi"
    assert g.nilai == pytest.approx(1.0)
    assert g.ambang == pytest.approx(AMBANG_RETENSI_DROP_1)


def test_satu_simbol_dominan_dijatuhkan():
    kontrib = [kon("RAJA", 100.0)] + datar(19, 0.1)
    u = ukur_konsentrasi(kontrib)
    assert u["ekspektasi_R"] == pytest.approx(101.9 / 200)
    assert u["ekspektasi_drop_1"] == pytest.approx(1.9 / 190)
    assert u["retensi_drop_1"] == pytest.approx(0.019627, abs=1e-6)
    assert u["porsi_bruto_teratas"] == pytest.approx(100.0 / 101.9)
    g = gerbang_konsentrasi(kontrib)
    assert not g.lulus
    assert "retensi_drop_1" in g.catatan
    assert "porsi_bruto_teratas" in g.catatan


def test_dua_simbol_tidak_bisa_lolos_porsi():
    """Dengan dua simbol, porsi teratas minimal 0,5 dan ambangnya 0,25."""
    g = gerbang_konsentrasi([kon("A", 1.0), kon("B", 1.0)])
    assert g.dapat_dinilai
    assert not g.lulus
    assert "porsi_bruto_teratas" in g.catatan


def test_porsi_tepat_di_ambang_lulus():
    """Ambang 0,25 bersifat inklusif; empat simbol setara tepat menyentuhnya."""
    kontrib = datar(4, 5.0)
    u = ukur_konsentrasi(kontrib)
    assert u["porsi_bruto_teratas"] == pytest.approx(0.25)
    assert gerbang_konsentrasi(kontrib).lulus


def test_median_negatif_menjatuhkan_meski_agregat_positif():
    """Agregat positif dapat lahir dari sedikit pemenang besar.

    Di sini keempat sub-uji berbasis jackknife lolos dan hanya median yang
    menjatuhkan, sehingga sub-uji itu terbukti punya daya sendiri.
    """
    kontrib = datar(5, 18.0, 100) + [kon(f"R{i:02d}", -0.5, 10) for i in range(15)]
    u = ukur_konsentrasi(kontrib)
    assert u["ekspektasi_R"] > 0
    assert u["retensi_drop_1"] > AMBANG_RETENSI_DROP_1
    assert u["porsi_bruto_teratas"] == pytest.approx(0.2)
    assert u["median_ekspektasi_simbol"] == pytest.approx(-0.05)
    g = gerbang_konsentrasi(kontrib)
    assert not g.lulus
    assert "median_simbol_positif" in g.catatan
    assert "retensi_drop_1" not in g.catatan


# --- inti ADR-010: penyebut bruto ---------------------------------------
def test_penyebut_bruto_bukan_bersih():
    """Kekeliruan S12, dikunci agar tidak lahir kembali.

    Portofolio ini bersih +1,4R dengan penyumbang teratas +10R. Penyebut bersih
    akan melaporkan porsi 714%, sebuah angka yang tidak mungkin dan tidak
    berarti. Penyebut bruto melaporkan 96,2%, yang tinggi dan memang benar.
    """
    kontrib = [kon("A", 10.0), kon("B", -9.0)] + datar(8, 0.05)
    u = ukur_konsentrasi(kontrib)
    assert u["total_R"] == pytest.approx(1.4)
    assert u["laba_bruto_R"] == pytest.approx(10.4)
    assert u["rugi_bruto_R"] == pytest.approx(-9.0)
    assert u["porsi_bruto_teratas"] == pytest.approx(10.0 / 10.4)
    assert u["porsi_bruto_teratas"] <= 1.0


def test_porsi_bruto_selalu_di_antara_nol_dan_satu():
    """Sifat yang tidak boleh bergantung pada data."""
    for rugi in (-0.5, -5.0, -50.0, -500.0):
        u = ukur_konsentrasi([kon("A", 60.0), kon("B", 40.0), kon("C", rugi)])
        if u["dapat_dinilai"]:
            assert 0.0 <= u["porsi_bruto_teratas"] <= 1.0


# --- pembulatan lima persen ----------------------------------------------
def test_jumlah_drop_5persen_dibulatkan_ke_atas():
    assert jumlah_drop_5persen(40) == 2
    assert jumlah_drop_5persen(21) == 2
    assert jumlah_drop_5persen(20) == 1
    assert jumlah_drop_5persen(100) == 5


def test_jumlah_drop_5persen_minimal_satu():
    """Pembulatan ke bawah akan membuat sub-uji ini tidak berbuat apa-apa."""
    assert jumlah_drop_5persen(1) == 1
    assert jumlah_drop_5persen(2) == 1


# --- tabel jackknife -----------------------------------------------------
def test_tabel_jackknife_menurun_dan_berbaris_rapi():
    kontrib = [kon(f"S{i:02d}", 10.0 - i) for i in range(10)]
    t = tabel_jackknife(kontrib)
    assert len(t) == 6
    assert t[0]["k"] == 0 and t[0]["dibuang"] is None
    assert t[0]["retensi"] == pytest.approx(1.0)
    assert t[1]["dibuang"] == "S00"
    retensi = [b["retensi"] for b in t]
    assert retensi == sorted(retensi, reverse=True)
    assert t[-1]["simbol_sisa"] == 5


def test_tabel_jackknife_tidak_menghabiskan_portofolio():
    t = tabel_jackknife([kon("A", 2.0), kon("B", 1.0)])
    assert [b["k"] for b in t] == [0, 1]
    assert t[1]["simbol_sisa"] == 1


# --- kesetaraan dua sumber ----------------------------------------------
def test_dua_sumber_menghasilkan_ukuran_yang_sama():
    ringkasan = [
        {"symbol": "A", "total_R": 5.0, "jumlah_trade_luar_sampel": 20},
        {"symbol": "B", "total_R": 4.0, "jumlah_trade_luar_sampel": 30},
        {"symbol": "C", "total_R": -1.0, "jumlah_trade_luar_sampel": 10},
    ]
    per_simbol = [
        {"symbol": b["symbol"], "total_R": b["total_R"], "trade": b["jumlah_trade_luar_sampel"]}
        for b in ringkasan
    ]
    assert dari_ringkasan(ringkasan) == dari_per_simbol(per_simbol)
    assert ukur_konsentrasi(dari_ringkasan(ringkasan)) == ukur_konsentrasi(
        dari_per_simbol(per_simbol)
    )


# --- HHI ------------------------------------------------------------------
def test_hhi_portofolio_datar_setara_jumlah_simbolnya():
    u = ukur_konsentrasi(datar(20))
    assert u["hhi_bruto"] == pytest.approx(0.05)
    assert u["setara_simbol"] == pytest.approx(20.0)


def test_hhi_mengabaikan_penyumbang_negatif():
    """HHI diukur atas pangsa laba bruto, jadi yang merugi tidak menambah pangsa."""
    a = ukur_konsentrasi(datar(10, 2.0))
    b = ukur_konsentrasi(datar(10, 2.0) + [kon("RUGI", -1.0)])
    assert a["hhi_bruto"] == pytest.approx(b["hhi_bruto"])
