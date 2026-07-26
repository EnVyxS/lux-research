"""Pengujian orkestrator H-012 (ADR-014 bagian 8).

Sebagian besar pengujian di sini adalah tripwire: nilainya bukan membuktikan
kode bekerja, melainkan berbunyi bila sebuah ambang pra-registrasi digeser
sesudah hasil terlihat. Itulah satu-satunya penjaga yang bekerja ketika yang
hendak menggeser ambang adalah saya sendiri.
"""

from __future__ import annotations

import pytest

from lux.backtest import run_h009, run_h010, run_h012
from lux.degenerasi import AMBANG_BIAYA_MASUK_R, AMBANG_MIN_STOP_FRAC


def test_periode_tahan_dibekukan():
    assert run_h012.PERIODE_TAHAN_TANGGAL == "2026-01-01"
    assert run_h012.PERIODE_TAHAN_MS == 1_767_225_600_000
    assert run_h012.PERIODE_TAHAN_BULAN == "2026-01"


def test_batas_void_dua_puluh():
    assert run_h012.BATAS_VOID == 20


def test_kriteria_tidak_bergerak():
    # Tidak dilonggarkan DAN tidak diperketat: keduanya sama-sama menyetel
    # ambang terhadap hasil yang sudah dilihat.
    k = run_h012.hipotesis_h012(run_h009.Konfig() if hasattr(run_h009, "Konfig") else __import__("lux.backtest.engine", fromlist=["Konfig"]).Konfig()).kriteria
    assert k.min_ekspektasi_R == 0.05
    assert k.min_trade_luar_sampel == 100
    assert k.maks_p_entri_acak == 0.05
    assert k.min_jendela_positif_rasio == 0.5


def test_mekanisme_diimpor_tanpa_perubahan():
    assert run_h012.kandidat_h010 is run_h010.kandidat
    assert run_h012.buat_konfig_h010 is run_h010.buat_konfig
    assert run_h010.buat_konfig is run_h009.buat_konfig
    assert list(run_h012.LOOKBACK_H010) == [20, 55, 100]
    assert list(run_h012.IMBALAN_H010) == [2.0, 4.0, 6.0, 8.0]
    assert len(run_h012.kandidat_h010()) == 12


def test_pengaman_adalah_turunan_aritmetik_lantai():
    # 2*(0,0005 + 0,0005) / 0,004 = 0,5. Diperiksa, bukan dipercaya sebagai
    # label (aturan 11).
    assert 2.0 * (0.0005 + 0.0005) / AMBANG_MIN_STOP_FRAC == pytest.approx(
        AMBANG_BIAYA_MASUK_R, abs=1e-12
    )


def test_kunci_config_dibaca_dari_berkas(tmp_path):
    p = tmp_path / "lux.yaml"
    p.write_text(
        "universe:\n  min_median_stop_frac: 0.004\n"
        "risiko:\n  maks_biaya_masuk_R: 0.5\n",
        encoding="utf-8",
    )
    k = run_h012.kunci_config(p)
    assert k["min_median_stop_frac"] == AMBANG_MIN_STOP_FRAC
    assert k["maks_biaya_masuk_R"] == AMBANG_BIAYA_MASUK_R


def test_kunci_config_nyata_sama_dengan_degenerasi():
    # Angka kembar di dua tempat wajib sama; bila tidak, salah satu digeser
    # tanpa dijurnalkan.
    k = run_h012.kunci_config("config/lux.yaml")
    assert k["min_median_stop_frac"] == AMBANG_MIN_STOP_FRAC
    assert k["maks_biaya_masuk_R"] == AMBANG_BIAYA_MASUK_R


def test_kunci_config_hilang_berbunyi(tmp_path):
    p = tmp_path / "lux.yaml"
    p.write_text("universe:\n  quote: USDT\n", encoding="utf-8")
    with pytest.raises(KeyError):
        run_h012.kunci_config(p)


def _periode(*baris):
    return [
        {
            "periode": b,
            "trade": t,
            "total_R": r,
            "ekspektasi_R": (r / t if t else None),
        }
        for b, t, r in baris
    ]


def test_agregat_tahan_berbobot_perdagangan():
    periode = _periode(
        ("2025-11", 1000, 100.0),
        ("2026-01", 100, 1.0),
        ("2026-02", 10, 5.0),
    )
    tahan = run_h012.agregat_tahan(periode)
    assert tahan["n_bulan"] == 2
    assert tahan["trade"] == 110
    # Berbobot perdagangan: 6/110 = 0,0545..., BUKAN rerata dari rerata
    # (0,01 dan 0,5 memberi 0,255).
    assert tahan["ekspektasi_R"] == pytest.approx(6.0 / 110.0)


def test_agregat_sebelum_melengkapi_tanpa_kehilangan_bulan():
    periode = _periode(
        ("2025-12", 50, -1.0),
        ("2026-01", 60, 2.0),
    )
    tahan = run_h012.agregat_tahan(periode)
    lama = run_h012.agregat_sebelum(periode)
    assert tahan["n_bulan"] + lama["n_bulan"] == 2
    assert tahan["trade"] + lama["trade"] == 110
    assert lama["ekspektasi_R"] == pytest.approx(-0.02)


def test_bulan_batas_milik_periode_tahan():
    periode = _periode(("2026-01", 10, 1.0))
    assert run_h012.agregat_tahan(periode)["trade"] == 10
    assert run_h012.agregat_sebelum(periode)["trade"] == 0


def test_periode_tahan_kosong_tidak_dapat_dinilai():
    periode = _periode(("2025-06", 500, 30.0))
    tahan = run_h012.agregat_tahan(periode)
    assert tahan["dapat_dinilai"] is False
    assert tahan["ekspektasi_R"] is None
    assert "tidak ada perdagangan" in tahan["sebab"]


def test_tujuh_ramalan_tertulis_dan_meramalkan_gagal():
    assert len(run_h012.RAMALAN) == 7
    assert "GAGAL" in run_h012.RAMALAN["3_ekspektasi_periode_tahan"]
    # Angka H-010 pada 300 permutasi wajib tercatat sebagai kegagalan, supaya
    # tidak ada yang menyebut H-012 sebagai rehabilitasi H-010.
    assert run_h012.SEBELUMNYA["h010_p_entri_acak_300_ulangan"] == 0.0631
    assert "bukan rehabilitasi" in run_h012.hipotesis_h012(
        __import__("lux.backtest.engine", fromlist=["Konfig"]).Konfig()
    ).pernyataan.lower()


def test_angka_haram_tidak_muncul_di_modul():
    # +0,060163R adalah hasil membuang USDCUSDT sesudah melihat hasilnya, dan
    # ia haram dipakai sebagai kelulusan. Ia tidak boleh menyelinap masuk
    # sebagai pembanding.
    isi = open(run_h012.__file__, encoding="utf-8").read()
    for haram in ("0.060163", "0.059546", "0.060168"):
        assert haram not in isi
