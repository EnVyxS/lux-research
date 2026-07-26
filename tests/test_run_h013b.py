"""Pagar Jalur B: pengacakan tunggal, nama laporan terpisah, penyerapan ringkas.

Seluruh pengujian di berkas ini berjalan tanpa satu bar pun data. Yang dijaga
bukan hasil, melainkan tiga hal yang bila salah akan menghasilkan angka yang
tampak waras: dua implementasi pengacakan, laporan yang saling menimpa, dan
pembuangan bulan yang tidak tercatat.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from lux.backtest.run_h002 import muat_konfig_h002
from lux.backtest.run_h013 import (
    NAMA_LAPORAN,
    SEED_PERMUTASI,
    UMUR_SEL_STOP,
    dasar_riset,
    kandidat,
    sinyal_acak,
)
from lux.backtest.run_h013b import (
    EKSPEKTASI_AS_SEED42,
    NAMA_SPEK,
    SEED_AKHIR,
    SEED_AWAL,
    SEED_PER_PECAHAN,
    PEMBATAS,
    baca_bulan,
    baris_seed,
    daftar_seed,
    jalur_antara,
    jalur_pecahan,
    periksa_kesetaraan,
    sinyal_acak_seed,
    spek_seed,
)
from lux.strategi import breakout_atr

PANJANG = 97


@pytest.fixture
def sinyal_palsu(monkeypatch):
    """Ganti sinyal Donchian dengan pola tetap.

    Yang diuji di sini adalah lapisan permutasi, bukan strategi. Menetapkan
    sinyal dasarnya membuat perbedaan apa pun antara dua pembungkus hanya dapat
    berasal dari pengacakannya.
    """
    dasar = np.where(np.arange(PANJANG) % 3 == 0, 1, np.where(np.arange(PANJANG) % 5 == 0, -1, 0))
    monkeypatch.setattr(breakout_atr, "sinyal", lambda df, params: dasar.copy())
    return dasar


@pytest.fixture
def bingkai():
    return pd.DataFrame({"close": np.arange(PANJANG, dtype=float)})


def test_seed_42_identik_dengan_sinyal_acak(sinyal_palsu, bingkai):
    """Satu implementasi pengacakan saja; dua akan melahirkan dua sebaran nol."""
    a = sinyal_acak(bingkai, {})
    b = sinyal_acak_seed(SEED_PERMUTASI)(bingkai, {})
    assert np.array_equal(a, b)


def test_periksa_kesetaraan_lulus(sinyal_palsu, bingkai):
    assert periksa_kesetaraan(bingkai, {}) is True


def test_seed_berbeda_menghasilkan_urutan_berbeda(sinyal_palsu, bingkai):
    a = sinyal_acak_seed(42)(bingkai, {})
    b = sinyal_acak_seed(43)(bingkai, {})
    assert not np.array_equal(a, b)


def test_seed_sama_dua_kali_identik(sinyal_palsu, bingkai):
    a = sinyal_acak_seed(7)(bingkai, {})
    b = sinyal_acak_seed(7)(bingkai, {})
    assert np.array_equal(a, b)


def test_permutasi_menjaga_jumlah_dan_arah(sinyal_palsu, bingkai):
    """Yang dihancurkan adalah waktunya, bukan komposisinya."""
    hasil = sinyal_acak_seed(11)(bingkai, {})
    assert sorted(np.asarray(hasil).tolist()) == sorted(sinyal_palsu.tolist())


def test_nama_spek_tidak_menimpa_laporan_h013():
    """Laporan run 30214203863 adalah satu-satunya pembanding; ia tak boleh hilang."""
    assert NAMA_SPEK not in set(NAMA_LAPORAN.values())
    assert "h013b" in NAMA_SPEK


def test_spek_seed_membekukan_geometri_sel_as():
    dasar = dasar_riset(muat_konfig_h002(Path("config/lux.yaml")))
    spek = spek_seed(5, dasar)
    k = spek.buat_konfig(kandidat()[0], dasar)
    assert k.pakai_target is True
    assert k.maks_umur_bar == UMUR_SEL_STOP
    assert spek.nama == NAMA_SPEK


def test_daftar_seed_tiga_puluh_tanpa_kembar():
    s = daftar_seed(30, 60)
    assert len(s) == SEED_PER_PECAHAN
    assert len(set(s)) == len(s)
    assert SEED_PERMUTASI in s


def test_daftar_seed_menolak_rentang_kosong_dan_kepanjangan():
    with pytest.raises(ValueError):
        daftar_seed(60, 60)
    with pytest.raises(ValueError):
        daftar_seed(0, SEED_PER_PECAHAN + 1)
    with pytest.raises(ValueError):
        daftar_seed(SEED_AKHIR - 5, SEED_AKHIR + 5)


def test_rentang_beku_memenuhi_ambang_ulangan():
    assert SEED_AKHIR - SEED_AWAL >= 300
    assert (SEED_AKHIR - SEED_AWAL) % SEED_PER_PECAHAN == 0


def test_jalur_pecahan_dan_antara():
    assert jalur_pecahan(30, 60, "reports") == Path("reports/h013b_seed_30_60.json")
    assert jalur_antara(NAMA_SPEK, "reports") == Path(
        "reports/backtest_h013b_as_seed.json"
    )


def test_baca_bulan_membuang_sisanya(tmp_path):
    """432.200 B masuk, hanya agregat bulanan keluar."""
    p = tmp_path / "backtest_h013b_as_seed.json"
    p.write_text(
        json.dumps(
            {
                "per_simbol": [{"simbol": "X", "jendela": 9}] * 400,
                "sebaran": {"std_R": 1.3},
                "agregat_periode": [
                    {
                        "periode": "2025-01",
                        "trade": 10,
                        "total_R": 5.0,
                        "ekspektasi_R": 0.5,
                        "dapat_dinilai": True,
                        "sebab": "",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    hasil = baca_bulan(p)
    assert hasil["bulan"] == [
        {"periode": "2025-01", "trade": 10, "total_R": 5.0, "ekspektasi_R": 0.5}
    ]
    assert hasil["dibuang"] == []


def test_baca_bulan_mencatat_bulan_yang_dibuang(tmp_path):
    """Pembuangan diam-diam mengubah himpunan bulan tanpa jejak."""
    p = tmp_path / "antara.json"
    p.write_text(
        json.dumps(
            {
                "agregat_periode": [
                    {"periode": "2025-01", "trade": 10, "total_R": 5.0, "ekspektasi_R": 0.5},
                    {"periode": "2025-02", "trade": 0, "total_R": 0.0, "ekspektasi_R": None},
                ]
            }
        ),
        encoding="utf-8",
    )
    hasil = baca_bulan(p)
    assert [b["periode"] for b in hasil["bulan"]] == ["2025-01"]
    assert hasil["dibuang"] == ["2025-02"]


def test_baca_bulan_menolak_laporan_tanpa_agregat(tmp_path):
    p = tmp_path / "antara.json"
    p.write_text(json.dumps({"gabungan": {"ekspektasi_R": 0.1}}), encoding="utf-8")
    with pytest.raises(ValueError):
        baca_bulan(p)
    with pytest.raises(FileNotFoundError):
        baca_bulan(tmp_path / "tidak_ada.json")


def test_baris_seed_ringkas():
    hasil = {
        "ekspektasi_R": 0.0118,
        "total_R": 660.25,
        "trade": 55927,
        "jumlah_jendela": 4082,
        "sidik": "5ee4b130f9ed228d",
        "detik": 12.5,
        "per_simbol": [{"simbol": "X"}] * 400,
    }
    baris = baris_seed(3, hasil, {"bulan": [], "dibuang": ["2025-02"]})
    assert baris["seed"] == 3
    assert baris["bulan_dibuang"] == ["2025-02"]
    assert "per_simbol" not in baris


def test_pembatas_menyatakan_gerbang_mati_dan_satuan():
    assert "entri_acak" in PEMBATAS
    assert "sampel_permutasi" in PEMBATAS
    assert "BULAN" in PEMBATAS
    assert "ADR-028" in PEMBATAS
    assert EKSPEKTASI_AS_SEED42 > 0
