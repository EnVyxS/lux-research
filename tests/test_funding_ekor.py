"""Pengujian gerbang kesebelas (ADR-011).

Dua pengujian terakhir adalah syarat kelayakan gerbang ini: ia wajib memisahkan
H-008 dari H-009, dua keadaan yang gagal dipisahkan gerbang funding lama
(10.253,97 lawan 10.199,59, keduanya lulus). Bila keduanya lulus di sini juga,
gerbang ini tidak lebih berguna daripada yang digantikannya.
"""

import math

import pytest

from lux.backtest.funding_ekor import (
    AMBANG_FUNDING_MAKS_R,
    AMBANG_PORSI_DI_ATAS_PENGAMAN,
    AMBANG_PORSI_FUNDING_EKOR,
    K_EKOR,
    NAMA,
    PENGAMAN_CARRY_R,
    TradeFunding,
    dari_rincian,
    gerbang_funding_ekor,
    porsi_funding,
    tabel_ekor_funding,
    ukur_funding_ekor,
)


def _jinak(n: int = 100) -> list[TradeFunding]:
    """Portofolio wajar: separuh menang, kerugian 1R dengan funding kecil."""
    trades = [TradeFunding(R=2.0, funding_R=0.002) for _ in range(n // 2)]
    trades += [TradeFunding(R=-1.05, funding_R=0.05) for _ in range(n // 2)]
    return trades


def test_ambang_adr011_tetap():
    assert AMBANG_PORSI_FUNDING_EKOR == 0.35
    assert AMBANG_FUNDING_MAKS_R == 0.50
    assert AMBANG_PORSI_DI_ATAS_PENGAMAN == 0.005
    assert PENGAMAN_CARRY_R == 0.25
    assert K_EKOR == 10
    assert NAMA == "funding_ekor"


def test_dari_rincian_membaca_kunci_yang_dipakai_diagnosa():
    baris = [{"symbol": "ADAUSDT", "R": -1.2698, "funding_R": 0.2098}]
    (t,) = dari_rincian(baris)
    assert t.R == pytest.approx(-1.2698)
    assert t.funding_R == pytest.approx(0.2098)


def test_dari_rincian_menolak_kunci_funding_yang_hilang():
    with pytest.raises(KeyError):
        dari_rincian([{"R": -1.0}])


def test_porsi_funding_membagi_dengan_kerugian_total():
    t = TradeFunding(R=-2.0, funding_R=0.5)
    assert porsi_funding(t) == pytest.approx(0.25)


def test_porsi_funding_nol_bila_tidak_ada_funding():
    assert porsi_funding(TradeFunding(R=-1.0, funding_R=0.0)) == 0.0


def test_rabat_funding_dihitung_nol_bukan_negatif():
    assert porsi_funding(TradeFunding(R=-1.0, funding_R=-0.3)) == 0.0


def test_perdagangan_untung_dikecualikan_dari_porsi():
    assert porsi_funding(TradeFunding(R=2.0, funding_R=0.9)) is None


def test_ekor_diambil_dari_sepuluh_terburuk():
    trades = [TradeFunding(R=-float(i), funding_R=0.01) for i in range(1, 21)]
    u = ukur_funding_ekor(trades)
    assert u["k_ekor"] == 10
    # terburuk adalah -20R, jadi porsi terbesar justru milik -1R
    assert u["n_rugi"] == 20
    assert u["porsi_funding_ekor_maks"] == pytest.approx(0.01 / 11.0)


def test_menghitung_trade_di_atas_pengaman():
    trades = _jinak(96) + [TradeFunding(R=-1.3, funding_R=0.26)]
    u = ukur_funding_ekor(trades)
    assert u["n_di_atas_pengaman"] == 1
    assert u["porsi_di_atas_pengaman"] == pytest.approx(1 / 97)


def test_portofolio_jinak_lulus():
    g = gerbang_funding_ekor(_jinak(), jadwal_dimuat=True)
    assert g.lulus is True
    assert g.nama == "funding_ekor"
    assert g.ambang == AMBANG_PORSI_FUNDING_EKOR
    assert g.nilai == pytest.approx(0.05 / 1.05)


def test_perdagangan_tanpa_funding_sama_sekali_tetap_lulus():
    trades = [TradeFunding(R=-1.0, funding_R=0.0) for _ in range(20)]
    g = gerbang_funding_ekor(trades, jadwal_dimuat=True)
    assert g.lulus is True
    assert g.nilai == 0.0


def test_porsi_ekor_terlalu_besar_menjatuhkan_gerbang():
    trades = _jinak(98) + [TradeFunding(R=-1.5, funding_R=0.75)]
    g = gerbang_funding_ekor(trades, jadwal_dimuat=True)
    assert g.lulus is False
    assert "porsi_funding_ekor_maks" in g.catatan


def test_funding_maks_terlalu_besar_menjatuhkan_gerbang():
    # porsi masih 0,30 sehingga sub-uji porsi lulus, tetapi 0,6R melewati 0,5R
    trades = _jinak(98) + [TradeFunding(R=-2.0, funding_R=0.6)]
    g = gerbang_funding_ekor(trades, jadwal_dimuat=True)
    assert g.lulus is False
    assert "funding_maks_R" in g.catatan
    assert "porsi_funding_ekor_maks" not in g.catatan


def test_terlalu_banyak_trade_di_atas_pengaman_menjatuhkan_gerbang():
    trades = [TradeFunding(R=-1.0, funding_R=0.26) for _ in range(10)]
    trades += [TradeFunding(R=2.0, funding_R=0.001) for _ in range(90)]
    g = gerbang_funding_ekor(trades, jadwal_dimuat=True)
    assert g.lulus is False
    assert "porsi_trade_di_atas_pengaman" in g.catatan


def test_jadwal_tidak_dimuat_berarti_gagal_bukan_lulus():
    g = gerbang_funding_ekor(_jinak(), jadwal_dimuat=False)
    assert g.lulus is False
    assert g.nilai is None
    assert g.dapat_dinilai is False
    assert "jadwal" in g.catatan


def test_daftar_kosong_gagal_bukan_lulus_diam_diam():
    g = gerbang_funding_ekor([], jadwal_dimuat=True)
    assert g.lulus is False
    assert g.nilai is None


def test_tanpa_perdagangan_merugi_gagal_karena_tak_dapat_dinilai():
    trades = [TradeFunding(R=1.0, funding_R=0.01) for _ in range(10)]
    g = gerbang_funding_ekor(trades, jadwal_dimuat=True)
    assert g.lulus is False
    assert g.nilai is None
    assert "merugi" in g.catatan


def test_nilai_tak_terhingga_gagal_karena_tak_dapat_dinilai():
    trades = _jinak(10) + [TradeFunding(R=-math.inf, funding_R=0.1)]
    g = gerbang_funding_ekor(trades, jadwal_dimuat=True)
    assert g.lulus is False
    assert g.nilai is None


def test_tabel_ekor_hanya_memuat_kerugian_dan_terurut():
    trades = [
        TradeFunding(R=3.0, funding_R=0.4),
        TradeFunding(R=-1.1, funding_R=0.1),
        TradeFunding(R=-1.9, funding_R=0.9),
    ]
    baris = tabel_ekor_funding(trades)
    assert [b["R"] for b in baris] == [-1.9, -1.1]
    assert baris[0]["porsi_funding"] == pytest.approx(round(0.9 / 1.9, 4))


def test_sepuluh_terburuk_h008_GAGAL():
    """Keadaan yang diloloskan gerbang lama dengan nilai 10.253,97."""
    h008 = [
        TradeFunding(R=-1.9769, funding_R=0.9228),
        TradeFunding(R=-1.4067, funding_R=0.3866),
        TradeFunding(R=-1.3869, funding_R=0.3083),
        TradeFunding(R=-1.3637, funding_R=0.3285),
        TradeFunding(R=-1.3215, funding_R=0.2728),
        TradeFunding(R=-1.2698, funding_R=0.2098),
        TradeFunding(R=-1.2614, funding_R=0.1985),
        TradeFunding(R=-1.2362, funding_R=0.1789),
        TradeFunding(R=-1.2282, funding_R=0.1996),
        TradeFunding(R=-1.2154, funding_R=0.1714),
    ]
    g = gerbang_funding_ekor(h008, jadwal_dimuat=True)
    assert g.nilai == pytest.approx(0.9228 / 1.9769, abs=1e-6)
    assert g.nilai > AMBANG_PORSI_FUNDING_EKOR
    assert g.lulus is False


def test_enam_terburuk_h009_yang_diterbitkan_LULUS():
    """Keadaan sesudah pengaman ADR-009 menyala; gerbang lama memberi 10.199,59."""
    h009 = [
        TradeFunding(R=-1.2698, funding_R=0.2098),
        TradeFunding(R=-1.2614, funding_R=0.1985),
        TradeFunding(R=-1.2362, funding_R=0.1789),
        TradeFunding(R=-1.2282, funding_R=0.1996),
        TradeFunding(R=-1.2154, funding_R=0.1714),
        TradeFunding(R=-1.2021, funding_R=-0.0),
    ]
    g = gerbang_funding_ekor(h009, jadwal_dimuat=True)
    assert g.nilai == pytest.approx(0.2098 / 1.2698, abs=1e-6)
    assert g.nilai < AMBANG_PORSI_FUNDING_EKOR
    assert g.lulus is True
