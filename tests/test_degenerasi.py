"""Pengujian lantai jarak stop dan pengaman biaya masuk (ADR-014).

Satu pengujian di bawah sengaja memuat angka ambang secara harfiah
(``test_ambang_tidak_boleh_digeser``). Itu tripwire yang disengaja, aturan 18:
angka yang ditulis tangan hanya boleh hidup di tepat satu pengujian, dan
tugasnya berbunyi bila ambang pra-registrasi digeser.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from lux.costs import ModelBiaya, biaya_dalam_R
from lux.degenerasi import (
    AMBANG_BIAYA_MASUK_R,
    AMBANG_MIN_STOP_FRAC,
    KASUS_USDCUSDT,
    biaya_masuk_R,
    entri_terlalu_mahal,
    layak_stop_frac,
    median_stop_frac,
    periksa_derivasi,
    saring_semesta,
    stop_frac_deret,
)


def test_ambang_tidak_boleh_digeser():
    # Tripwire pra-registrasi ADR-014. Bila baris ini gagal, yang bergeser
    # adalah ambang yang dibekukan sebelum H-012 dijalankan.
    assert AMBANG_MIN_STOP_FRAC == 0.004
    assert AMBANG_BIAYA_MASUK_R == 0.5


def test_ambang_diturunkan_dari_aritmetika_biaya():
    d = periksa_derivasi()
    assert d["konsisten"] is True
    assert d["biaya_bolak_balik"] == pytest.approx(0.002, abs=1e-15)
    assert biaya_dalam_R(AMBANG_MIN_STOP_FRAC) == pytest.approx(
        AMBANG_BIAYA_MASUK_R, abs=1e-12
    )


def test_lantai_dan_pengaman_sepakat_di_titik_batas():
    # Dua cara menyatakan satu batas: median tepat di lantai diterima, dan
    # entri tepat di lantai tidak ditolak.
    assert layak_stop_frac(AMBANG_MIN_STOP_FRAC) is True
    assert entri_terlalu_mahal(AMBANG_MIN_STOP_FRAC) is False
    sedikit_di_bawah = AMBANG_MIN_STOP_FRAC * 0.999
    assert layak_stop_frac(sedikit_di_bawah) is False
    assert entri_terlalu_mahal(sedikit_di_bawah) is True


def test_stop_frac_deret_menolak_panjang_berbeda():
    with pytest.raises(ValueError):
        stop_frac_deret([1.0, 2.0], [10.0])


def test_stop_frac_deret_menolak_pengali_tidak_positif():
    with pytest.raises(ValueError):
        stop_frac_deret([1.0], [10.0], pengali=0.0)


def test_stop_frac_deret_membuang_atr_tidak_finit():
    d = stop_frac_deret([np.nan, 1.0, np.inf], [100.0, 100.0, 100.0])
    assert d.tolist() == [pytest.approx(0.02)]


def test_stop_frac_deret_menyertakan_atr_nol():
    # ATR nol adalah keadaan degenerat yang sedang dicari, bukan data hilang.
    # Membuangnya akan menaikkan median dan menyelamatkan simbol terburuk.
    d = stop_frac_deret([0.0, 1.0], [100.0, 100.0])
    assert d.size == 2
    assert d[0] == 0.0
    assert median_stop_frac([0.0, 0.0, 1.0], [100.0] * 3) == pytest.approx(0.0)


def test_stop_frac_deret_membuang_harga_tidak_positif():
    d = stop_frac_deret([1.0, 1.0, 1.0], [0.0, -5.0, 50.0])
    assert d.tolist() == [pytest.approx(0.04)]


def test_median_kosong_mengembalikan_none():
    assert median_stop_frac([], []) is None
    assert median_stop_frac([np.nan, np.nan], [10.0, 10.0]) is None


def test_median_memakai_median_bukan_rerata():
    # Satu lonjakan volatilitas tidak boleh menyelamatkan simbol yang nyaris
    # tidak pernah bergerak.
    atr = [0.0, 0.0, 0.0, 0.0, 100.0]
    harga = [100.0] * 5
    assert median_stop_frac(atr, harga) == pytest.approx(0.0)
    assert float(np.mean(stop_frac_deret(atr, harga))) > 0.0


def test_tidak_dapat_dinilai_ditolak_bukan_diloloskan():
    assert layak_stop_frac(None) is False
    assert layak_stop_frac(math.nan) is False
    assert layak_stop_frac(math.inf) is False


def test_layak_stop_frac_menolak_ambang_tidak_positif():
    with pytest.raises(ValueError):
        layak_stop_frac(0.05, ambang=0.0)


def test_biaya_masuk_pada_stop_nol_tak_hingga_bukan_galat():
    # Pengaman ini dipanggil di dalam gelung mesin; ia tidak boleh mematikan
    # run panjang di perdagangan ke seratus ribu.
    assert biaya_masuk_R(0.0) == math.inf
    assert biaya_masuk_R(-1.0) == math.inf
    assert biaya_masuk_R(math.nan) == math.inf
    assert entri_terlalu_mahal(0.0) is True


def test_biaya_masuk_naik_ketika_stop_menyempit():
    assert biaya_masuk_R(0.001) > biaya_masuk_R(0.01) > biaya_masuk_R(0.1)


def test_kasus_usdcusdt_tertangkap_pengaman():
    sf = KASUS_USDCUSDT["stop_frac"]
    assert entri_terlalu_mahal(sf) is True
    assert layak_stop_frac(sf) is False
    # Laporan hanya memuat fee (slippage sudah tertanam di harga eksekusi),
    # jadi separuh angka modul ini wajib mereproduksi kolom laporan.
    hanya_fee = biaya_masuk_R(sf) / 2.0
    assert hanya_fee == pytest.approx(
        KASUS_USDCUSDT["transaksi_R_di_laporan"], rel=0.01
    )
    assert biaya_masuk_R(sf) > 600.0


def test_stop_khas_semesta_tidak_tertangkap():
    # rerata_stop_frac H-011 adalah 0,03489824448280757. Pengaman yang menolak
    # entri normal bukan pengaman melainkan saringan hasil.
    khas = 0.03489824448280757
    assert entri_terlalu_mahal(khas) is False
    assert biaya_masuk_R(khas) < 0.06
    assert layak_stop_frac(khas) is True


def test_entri_terlalu_mahal_menolak_ambang_tidak_positif():
    with pytest.raises(ValueError):
        entri_terlalu_mahal(0.01, ambang=0.0)


def test_model_biaya_lain_menggeser_biaya_tetapi_bukan_ambang():
    murah = ModelBiaya(fee=0.0001, slippage=0.0001)
    assert biaya_masuk_R(0.004, murah) == pytest.approx(0.1, abs=1e-12)
    assert entri_terlalu_mahal(0.004, model=murah) is False


def test_saring_semesta_memisahkan_dan_mengurutkan():
    hasil = saring_semesta(
        {
            "ZZZUSDT": 0.05,
            "USDCUSDT": KASUS_USDCUSDT["stop_frac"],
            "AAAUSDT": 0.004,
            "KOSONGUSDT": None,
        }
    )
    assert hasil["layak"] == ["AAAUSDT", "ZZZUSDT"]
    assert [b["symbol"] for b in hasil["ditolak"]] == ["KOSONGUSDT", "USDCUSDT"]


def test_saring_semesta_tidak_kehilangan_simbol():
    peta = {f"S{i}USDT": (0.05 if i % 2 else 1e-06) for i in range(20)}
    hasil = saring_semesta(peta)
    assert hasil["n_masuk"] == 20
    assert hasil["n_layak"] + hasil["n_ditolak"] == hasil["n_masuk"]
    assert set(hasil["layak"]) | {b["symbol"] for b in hasil["ditolak"]} == set(peta)


def test_saring_semesta_mencatat_biaya_dan_sebab():
    hasil = saring_semesta({"USDCUSDT": KASUS_USDCUSDT["stop_frac"], "XUSDT": None})
    per_simbol = {b["symbol"]: b for b in hasil["ditolak"]}
    assert per_simbol["USDCUSDT"]["biaya_masuk_R"] > 600.0
    assert "di bawah lantai" in per_simbol["USDCUSDT"]["sebab"]
    assert per_simbol["XUSDT"]["biaya_masuk_R"] is None
    assert "tidak dapat dinilai" in per_simbol["XUSDT"]["sebab"]
    assert hasil["ambang"] == AMBANG_MIN_STOP_FRAC
