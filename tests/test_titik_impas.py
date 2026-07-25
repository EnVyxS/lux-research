"""Pengujian aritmetika titik impas.

Angka H-002 dipakai sebagai kasus nyata, sehingga klaim di ADR-007 diperiksa
mesin dan bukan sekadar dipercaya.
"""

from __future__ import annotations

import pytest

from lux.analisis.titik_impas import (
    ekspektasi_kotor,
    laju_dibutuhkan,
    laju_kena_target,
    ringkas_laporan,
    seretan_tersirat,
    titik_impas,
)

# Histogram alasan keluar H-002, disalin dari reports/backtest_h002.md.
H002 = {"target": 6707, "stop": 11909, "akhir_data": 164, "umur": 103}
H002_BERSIH = 0.03159


def test_titik_impas_baku():
    assert titik_impas(2.0) == pytest.approx(1 / 3)
    assert titik_impas(1.0) == pytest.approx(0.5)
    assert titik_impas(3.0) == pytest.approx(0.25)
    assert titik_impas(4.0) == pytest.approx(0.2)


def test_imbalan_lebih_besar_menurunkan_titik_impas():
    nilai = [titik_impas(i) for i in (1.0, 2.0, 3.0, 4.0)]
    assert nilai == sorted(nilai, reverse=True)


def test_imbalan_tidak_positif_ditolak():
    with pytest.raises(ValueError):
        titik_impas(0.0)


def test_laju_mengabaikan_umur_dan_akhir_data():
    """Keluar karena umur tidak terpotong di 1R maupun di imbalan."""
    assert laju_kena_target(H002) == pytest.approx(6707 / 18616)


def test_laju_tanpa_perdagangan_selesai_ditolak():
    with pytest.raises(ValueError):
        laju_kena_target({"umur": 12, "akhir_data": 3})


def test_ekspektasi_kotor_nol_tepat_di_titik_impas():
    for im in (1.0, 2.0, 3.0, 4.0):
        assert ekspektasi_kotor(titik_impas(im), im) == pytest.approx(0.0, abs=1e-12)


def test_h002_hanya_sedikit_di_atas_titik_impas():
    laju = laju_kena_target(H002)
    assert laju > titik_impas(2.0)
    assert laju - titik_impas(2.0) == pytest.approx(0.0270, abs=5e-4)


def test_h002_kotor_dan_seretan():
    kotor = ekspektasi_kotor(laju_kena_target(H002), 2.0)
    assert kotor == pytest.approx(0.08084, abs=1e-4)
    assert seretan_tersirat(kotor, H002_BERSIH) == pytest.approx(0.04926, abs=1e-4)


def test_h002_kekurangan_laju_kurang_dari_satu_poin_persen():
    r = ringkas_laporan(H002, H002_BERSIH, imbalan=2.0, target_bersih=0.05)
    assert r["laju_dibutuhkan"] == pytest.approx(0.36642, abs=1e-4)
    assert 0.0 < r["kekurangan_laju"] < 0.01
    assert r["pemenang_tambahan"] == pytest.approx(114, abs=3)


def test_laju_dibutuhkan_konsisten_dengan_ekspektasi_kotor():
    """Bolak-balik: laju yang dibutuhkan harus benar-benar menghasilkan target."""
    perlu = laju_dibutuhkan(0.05, 0.04926, 2.0)
    assert ekspektasi_kotor(perlu, 2.0) - 0.04926 == pytest.approx(0.05, abs=1e-9)


def test_urutan_hipotesis_mengikuti_laju_kena_target():
    """Klaim inti ADR-007: enam hasil terurut sempurna menurut satu angka."""
    data = [
        ({"target": 6707, "stop": 11909}, 0.03159),
        ({"target": 2659, "stop": 5127}, -0.01818),
        ({"target": 4057, "stop": 7962}, -0.03571),
        ({"target": 6032, "stop": 13993}, -0.13449),
        ({"target": 7503, "stop": 20997}, -0.24782),
    ]
    laju = [laju_kena_target(a) for a, _ in data]
    bersih = [b for _, b in data]
    assert laju == sorted(laju, reverse=True)
    assert bersih == sorted(bersih, reverse=True)
