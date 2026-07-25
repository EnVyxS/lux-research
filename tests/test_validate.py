"""Pengujian pemeriksaan integritas dan kelayakan.

Setiap pengujian di sini membangun bingkai data sintetis yang melanggar tepat
satu invarian, supaya kegagalan menunjuk langsung ke penyebabnya.
"""

from __future__ import annotations

import pandas as pd
import pytest

from lux.validate import (
    AmbangKelayakan,
    median_quote_volume_harian,
    nilai_kelayakan,
    periksa_seri,
    rasio_bar_datar,
)

STEP = 3_600_000
AWAL = 1_600_000_000_000 - (1_600_000_000_000 % STEP)


def bingkai(n: int = 24, **ubah) -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "open_time": [AWAL + i * STEP for i in range(n)],
            "open": [100.0] * n,
            "high": [101.0] * n,
            "low": [99.0] * n,
            "close": [100.5] * n,
            "volume": [10.0] * n,
            "quote_volume": [1000.0] * n,
        }
    )
    for kolom, nilai in ubah.items():
        df[kolom] = nilai
    return df


def test_seri_bersih_lulus():
    h = periksa_seri(bingkai(), "BTCUSDT", "1h")
    assert h.lulus
    assert h.pelanggaran_fatal == 0
    assert h.celah == 0


def test_seri_kosong_tidak_lulus():
    h = periksa_seri(pd.DataFrame(), "BTCUSDT", "1h")
    assert not h.lulus
    assert "seri kosong" in h.catatan


def test_duplikat_waktu_terdeteksi():
    df = bingkai(5)
    df.loc[4, "open_time"] = df.loc[3, "open_time"]
    h = periksa_seri(df, "BTCUSDT", "1h")
    assert h.duplikat_waktu == 1
    assert not h.lulus


def test_waktu_mundur_terdeteksi():
    df = bingkai(5)
    df.loc[3, "open_time"] = AWAL - STEP
    h = periksa_seri(df, "BTCUSDT", "1h")
    assert h.waktu_tidak_urut >= 1
    assert not h.lulus


def test_waktu_tidak_selaras_kisi_terdeteksi():
    """Stempel yang meleset dari kisi menandakan salah satuan atau salah zona."""
    df = bingkai(3)
    df.loc[1, "open_time"] = df.loc[1, "open_time"] + 1234
    h = periksa_seri(df, "BTCUSDT", "1h")
    assert h.tidak_selaras_kisi == 1
    assert not h.lulus


def test_high_lebih_kecil_dari_close_terdeteksi():
    """Kolom OHLC tertukar menghasilkan backtest yang tampak ajaib."""
    df = bingkai(3)
    df.loc[1, "high"] = 99.5  # lebih kecil dari close 100.5
    h = periksa_seri(df, "BTCUSDT", "1h")
    assert h.high_lebih_kecil == 1
    assert not h.lulus


def test_low_lebih_besar_dari_open_terdeteksi():
    df = bingkai(3)
    df.loc[2, "low"] = 100.2  # lebih besar dari open 100.0
    h = periksa_seri(df, "BTCUSDT", "1h")
    assert h.low_lebih_besar == 1
    assert not h.lulus


def test_harga_nol_terdeteksi():
    df = bingkai(3)
    df.loc[1, "low"] = 0.0
    h = periksa_seri(df, "BTCUSDT", "1h")
    assert h.harga_non_positif >= 1
    assert not h.lulus


def test_volume_negatif_terdeteksi():
    df = bingkai(3)
    df.loc[1, "volume"] = -1.0
    h = periksa_seri(df, "BTCUSDT", "1h")
    assert h.volume_negatif == 1
    assert not h.lulus


def test_nilai_kosong_terdeteksi():
    df = bingkai(3)
    df.loc[1, "close"] = None
    h = periksa_seri(df, "BTCUSDT", "1h")
    assert h.nilai_kosong >= 1
    assert not h.lulus


def test_celah_tercatat_tapi_tidak_fatal():
    """Perdagangan memang pernah terhenti; itu fakta, bukan kerusakan."""
    df = bingkai(5)
    df.loc[3, "open_time"] = df.loc[2, "open_time"] + 5 * STEP
    df.loc[4, "open_time"] = df.loc[3, "open_time"] + STEP
    h = periksa_seri(df, "BTCUSDT", "1h")
    assert h.celah == 1
    assert h.pelanggaran_fatal == 0
    assert h.lulus


def test_bar_datar_dihitung():
    df = bingkai(4)
    df.loc[0, "high"] = 100.0
    df.loc[0, "low"] = 100.0
    h = periksa_seri(df, "BTCUSDT", "1h")
    assert h.bar_datar == 1
    assert rasio_bar_datar(h) == pytest.approx(0.25)


def test_interval_tidak_dikenal_ditolak():
    with pytest.raises(ValueError):
        periksa_seri(bingkai(2), "BTCUSDT", "3h")


def test_median_harian_dihitung_per_hari_bukan_per_bar():
    df = bingkai(48)  # dua hari penuh, 1000 per bar
    median = median_quote_volume_harian(df, "1h")
    assert median == pytest.approx(24_000.0)


def test_median_tahan_terhadap_satu_hari_ekstrem():
    """Median dipakai justru agar satu hari peluncuran tidak menipu."""
    df = bingkai(72)
    df.loc[df.index[:24], "quote_volume"] = 10_000_000.0
    median = median_quote_volume_harian(df, "1h")
    assert median == pytest.approx(24_000.0)


def test_simbol_wajar_dinyatakan_layak():
    df = bingkai(9000)
    df["quote_volume"] = 100_000.0
    h = periksa_seri(df, "BTCUSDT", "1h")
    layak, alasan = nilai_kelayakan(h, median_quote_volume_harian(df, "1h"))
    assert layak, alasan
    assert alasan == []


def test_riwayat_pendek_ditolak_dengan_alasan():
    """Kasus nyata: tiga perpetual meme berumur ~175 hari."""
    df = bingkai(4200)
    df["quote_volume"] = 100_000.0
    h = periksa_seri(df, "MEMEUSDT", "1h")
    layak, alasan = nilai_kelayakan(h, median_quote_volume_harian(df, "1h"))
    assert not layak
    assert any("riwayat terlalu pendek" in a for a in alasan)


def test_likuiditas_tipis_ditolak_dengan_alasan():
    df = bingkai(9000)
    df["quote_volume"] = 1.0
    h = periksa_seri(df, "SEPIUSDT", "1h")
    layak, alasan = nilai_kelayakan(h, median_quote_volume_harian(df, "1h"))
    assert not layak
    assert any("likuiditas terlalu tipis" in a for a in alasan)


def test_terlalu_banyak_bar_datar_ditolak():
    df = bingkai(9000)
    df["quote_volume"] = 100_000.0
    df.loc[df.index[:5000], "high"] = 99.0
    df.loc[df.index[:5000], "low"] = 99.0
    df.loc[df.index[:5000], "open"] = 99.0
    df.loc[df.index[:5000], "close"] = 99.0
    h = periksa_seri(df, "BEKUUSDT", "1h")
    layak, alasan = nilai_kelayakan(h, median_quote_volume_harian(df, "1h"))
    assert not layak
    assert any("bar datar" in a for a in alasan)


def test_semua_alasan_penolakan_dikumpulkan_bukan_yang_pertama_saja():
    df = bingkai(100)
    df["quote_volume"] = 1.0
    h = periksa_seri(df, "BURUKUSDT", "1h")
    layak, alasan = nilai_kelayakan(h, median_quote_volume_harian(df, "1h"))
    assert not layak
    assert len(alasan) >= 2


def test_ambang_dapat_diganti_secara_eksplisit():
    df = bingkai(200)
    df["quote_volume"] = 100_000.0
    h = periksa_seri(df, "KECILUSDT", "1h")
    ambang = AmbangKelayakan(min_bar=100, min_median_quote_volume_harian=1000.0)
    layak, alasan = nilai_kelayakan(h, median_quote_volume_harian(df, "1h"), ambang)
    assert layak, alasan


def test_hasil_dapat_diserialkan():
    h = periksa_seri(bingkai(), "BTCUSDT", "1h")
    d = h.sebagai_dict()
    assert d["symbol"] == "BTCUSDT"
    assert d["lulus"] is True
    assert "pelanggaran_fatal" in d
