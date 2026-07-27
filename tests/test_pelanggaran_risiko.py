"""Uji diagnostik pelanggaran ambang risiko (ADR-038 bagian 5.4).

Dua uji terakhir sengaja menjalankan **mesin sungguhan** atas bar yang sama dan
hanya membedakan ``stop_hormati_celah``. Uji yang hanya menyusun
``Perdagangan`` dengan tangan menguji model penulisnya tentang mesin, bukan
mesinnya (cacat kelas 12, aturan 42).
"""

from __future__ import annotations

import inspect

import numpy as np
import pandas as pd
import pytest

from lux.backtest.engine import Konfig, Perdagangan, jalankan
from lux.backtest.gerbang import gerbang_invarian_risiko
from lux.diagnostik.pelanggaran_risiko import (
    AMBANG_KERUGIAN_R,
    KOLOM,
    baris_pelanggaran,
    baris_untuk,
    harga_keluar_bruto,
    ke_markdown,
    ringkas_pelanggaran,
    waktu_iso,
)

JAM_MS = 3_600_000


def _trade(
    R: float,
    arah: int = 1,
    symbol: str = "AAAUSDT",
    alasan: str = "stop",
    harga_masuk: float = 100.0,
    jarak_stop: float = 4.0,
    ukuran: float = 12.5,
    transaksi: float = 0.0,
    funding: float = 0.0,
    masuk_ms: int = 0,
    keluar_ms: int = JAM_MS,
) -> Perdagangan:
    """Perdagangan sintetis yang harga keluarnya konsisten dengan R-nya."""
    risiko = jarak_stop * ukuran
    kotor = R * risiko + transaksi + funding
    return Perdagangan(
        symbol=symbol,
        arah=arah,
        masuk_ms=masuk_ms,
        keluar_ms=keluar_ms,
        harga_masuk=harga_masuk,
        harga_keluar=harga_masuk + kotor / (arah * ukuran),
        ukuran=ukuran,
        jarak_stop=jarak_stop,
        alasan_keluar=alasan,
        biaya_transaksi=transaksi,
        biaya_funding=funding,
        laba_kotor=kotor,
    )


class HasilBoneka:
    """Cukup untuk gerbang: ia hanya membaca jumlah_trade dan perdagangan."""

    def __init__(self, perdagangan):
        self.perdagangan = list(perdagangan)

    @property
    def jumlah_trade(self):
        return len(self.perdagangan)


def _bingkai(bar):
    return pd.DataFrame(
        {
            "open_time": [i * JAM_MS for i in range(len(bar))],
            "open": [b[0] for b in bar],
            "high": [b[1] for b in bar],
            "low": [b[2] for b in bar],
            "close": [b[3] for b in bar],
        }
    )


BAR_CELAH = [
    (100.0, 101.0, 99.0, 100.0),
    (100.0, 101.0, 99.0, 100.0),
    (100.0, 101.0, 99.0, 100.0),
    (100.0, 101.0, 99.0, 100.0),
    (60.0, 61.0, 55.0, 58.0),
    (58.0, 59.0, 57.0, 58.0),
]
SINYAL_CELAH = np.array([0, 0, 1, 0, 0, 0], dtype="int64")


def _jalankan_celah(hormati: bool):
    konfig = Konfig(
        atr_periode=2,
        atr_pengali_stop=2.0,
        slippage=0.0005,
        fee=0.0005,
        stop_hormati_celah=hormati,
    )
    hasil = jalankan(_bingkai(BAR_CELAH), SINYAL_CELAH, konfig, None, "GAPUSDT")
    return hasil, konfig


# --- ambang -----------------------------------------------------------------
def test_ambang_dibaca_dari_gerbang():
    bawaan = inspect.signature(gerbang_invarian_risiko).parameters[
        "maks_kerugian_R"
    ].default
    assert AMBANG_KERUGIAN_R == float(bawaan)


def test_ambang_masih_satu_setengah_R():
    assert AMBANG_KERUGIAN_R == 1.5


def test_tanpa_pelanggaran_daftar_kosong():
    assert baris_pelanggaran([_trade(-1.0), _trade(0.5)], 0.0005) == []


def test_pelanggaran_terdeteksi():
    baris = baris_pelanggaran([_trade(-1.6)], 0.0005)
    assert len(baris) == 1
    assert baris[0]["R"] == pytest.approx(-1.6)


def test_persis_di_ambang_bukan_pelanggaran():
    assert baris_pelanggaran([_trade(-AMBANG_KERUGIAN_R)], 0.0005) == []


def test_sedikit_di_bawah_ambang_adalah_pelanggaran():
    assert len(baris_pelanggaran([_trade(-1.5000001)], 0.0005)) == 1


@pytest.mark.parametrize(
    "rs",
    [
        (-1.4, -0.2, 0.9),
        (-1.5, -1.0),
        (-1.6, 0.3),
        (-9.0, -1.6, -1.5, 2.0),
    ],
)
def test_setara_dengan_gerbang_sungguhan(rs):
    trades = [_trade(r) for r in rs]
    gerbang = gerbang_invarian_risiko(HasilBoneka(trades))
    baris = baris_pelanggaran(trades, 0.0005)
    assert gerbang.lulus == (len(baris) == 0)
    assert gerbang.nilai == pytest.approx(min(t.R for t in trades))
    assert gerbang.ambang == pytest.approx(-AMBANG_KERUGIAN_R)


def test_urut_terburuk_lebih_dahulu():
    baris = baris_pelanggaran([_trade(-2.0), _trade(-9.0), _trade(-3.0)], 0.0005)
    assert [b["R"] for b in baris] == pytest.approx([-9.0, -3.0, -2.0])


def test_ambang_dapat_dipasok_lebih_ketat():
    assert len(baris_pelanggaran([_trade(-1.1)], 0.0005, maks_kerugian_R=1.0)) == 1


# --- aritmetika baris -------------------------------------------------------
def test_bruto_long_membalik_slippage():
    assert harga_keluar_bruto(59.97, 1, 0.0005) == pytest.approx(60.0)


def test_bruto_short_membalik_ke_arah_lain():
    assert harga_keluar_bruto(60.03, -1, 0.0005) == pytest.approx(60.0)


def test_bruto_tanpa_slippage_tidak_bergerak():
    assert harga_keluar_bruto(123.456, 1, 0.0) == pytest.approx(123.456)


def test_slippage_tidak_sah_ditolak():
    with pytest.raises(ValueError):
        harga_keluar_bruto(100.0, 1, 1.0)


def test_slippage_negatif_ditolak():
    with pytest.raises(ValueError):
        baris_pelanggaran([_trade(-2.0)], -0.1)


def test_stop_teoretis_long():
    b = baris_untuk(_trade(-2.0, arah=1), 0.0005)
    assert b["stop_teoretis"] == pytest.approx(96.0)


def test_stop_teoretis_short():
    b = baris_untuk(_trade(-2.0, arah=-1), 0.0005)
    assert b["stop_teoretis"] == pytest.approx(104.0)


def test_stop_frac():
    b = baris_untuk(_trade(-2.0, harga_masuk=100.0, jarak_stop=4.0), 0.0005)
    assert b["stop_frac"] == pytest.approx(0.04)


def test_identitas_R_selalu_nol():
    for arah in (1, -1):
        for R in (-1.6, -5.0, -20.0):
            b = baris_untuk(_trade(R, arah=arah, transaksi=1.0, funding=0.5), 0.0005)
            assert b["residu_identitas_R"] == pytest.approx(0.0, abs=1e-9)


def test_R_adalah_kotor_dikurangi_biaya():
    b = baris_untuk(_trade(-3.0, transaksi=2.0, funding=1.0), 0.0005)
    assert b["R"] == pytest.approx(
        b["laba_kotor_R"] - b["biaya_transaksi_R"] - b["biaya_funding_R"]
    )


def test_celah_hanya_untuk_alasan_stop():
    b = baris_untuk(_trade(-8.0, alasan="umur"), 0.0005)
    assert b["selisih_stop_R"] > 0
    assert b["celah_melewati_stop"] is False
    assert b["harga_bar_sungguhan"] is True


def test_celah_ditandai_untuk_stop_yang_lebih_buruk():
    b = baris_untuk(_trade(-8.0, alasan="stop"), 0.0005)
    assert b["celah_melewati_stop"] is True
    assert b["harga_bar_sungguhan"] is False


def test_stop_tanpa_celah_tidak_ditandai():
    b = baris_untuk(_trade(-1.6, alasan="stop", transaksi=30.0), 0.0005)
    assert b["selisih_stop_R"] < 1e-9
    assert b["celah_melewati_stop"] is False


def test_risiko_nol_dilewati_bukan_menggagalkan():
    aman = _trade(-2.0)
    rusak = Perdagangan(
        symbol="NOLUSDT",
        arah=1,
        masuk_ms=0,
        keluar_ms=JAM_MS,
        harga_masuk=100.0,
        harga_keluar=90.0,
        ukuran=0.0,
        jarak_stop=0.0,
        alasan_keluar="stop",
        biaya_transaksi=0.0,
        biaya_funding=0.0,
        laba_kotor=-100.0,
    )
    baris = baris_pelanggaran([rusak, aman], 0.0005)
    assert [b["symbol"] for b in baris] == ["AAAUSDT"]


def test_risiko_nol_ditolak_bila_dirinci_langsung():
    rusak = _trade(-2.0)
    rusak = Perdagangan(**{**rusak.__dict__, "jarak_stop": 0.0})
    with pytest.raises(ValueError):
        baris_untuk(rusak, 0.0005)


def test_waktu_iso_utc():
    assert waktu_iso(0) == "1970-01-01T00:00:00Z"


# --- ringkasan dan markdown -------------------------------------------------
def test_ringkas_menghitung_cacah_dan_porsi():
    baris = baris_pelanggaran(
        [_trade(-2.0), _trade(-9.0, symbol="BBBUSDT", alasan="umur")], 0.0005
    )
    r = ringkas_pelanggaran(baris, cacah_trade=100)
    assert r["cacah_pelanggaran"] == 2
    assert r["porsi"] == pytest.approx(0.02)
    assert r["terburuk_R"] == pytest.approx(-9.0)
    assert r["paling_ringan_R"] == pytest.approx(-2.0)
    assert r["per_alasan"] == {"stop": 1, "umur": 1}
    assert r["cacah_harga_bar_sungguhan"] == 1


def test_ringkas_kosong_aman():
    r = ringkas_pelanggaran([], cacah_trade=0)
    assert r["cacah_pelanggaran"] == 0
    assert r["porsi"] is None
    assert r["terburuk_R"] is None


def test_markdown_memuat_kolom_dan_simbol():
    baris = baris_pelanggaran([_trade(-2.0)], 0.0005)
    teks = ke_markdown(baris, ringkas_pelanggaran(baris, 10))
    for k in KOLOM:
        assert k in teks
    assert "AAAUSDT" in teks


def test_markdown_kosong_menyatakan_nol():
    teks = ke_markdown([], ringkas_pelanggaran([], 10))
    assert "Tidak ada perdagangan yang melewati ambang." in teks


def test_markdown_memotong_dan_mengatakannya():
    baris = baris_pelanggaran([_trade(-2.0 - i / 100) for i in range(5)], 0.0005)
    teks = ke_markdown(baris, ringkas_pelanggaran(baris, 5), batas_baris=2)
    assert "Dipotong pada 2 baris dari 5" in teks


# --- mesin sungguhan --------------------------------------------------------
def test_mesin_celah_melahirkan_pelanggaran_dan_terbaca():
    hasil, konfig = _jalankan_celah(True)
    assert hasil.jumlah_trade == 1
    p = hasil.perdagangan[0]
    assert p.alasan_keluar == "stop"
    gerbang = gerbang_invarian_risiko(hasil)
    assert gerbang.lulus is False
    baris = baris_pelanggaran(hasil.perdagangan, konfig.slippage)
    assert len(baris) == 1
    b = baris[0]
    # Harga pengisian bruto WAJIB sama dengan pembukaan bar keluar; itulah
    # satu-satunya sumber angka itu di harga_stop_terisi.
    assert b["harga_keluar_bruto"] == pytest.approx(BAR_CELAH[4][0])
    assert b["celah_melewati_stop"] is True
    assert b["selisih_stop_R"] == pytest.approx(9.0125, abs=1e-6)
    assert b["R"] == pytest.approx(-10.0400025, abs=1e-6)
    assert b["residu_identitas_R"] == pytest.approx(0.0, abs=1e-9)


def test_mesin_tanpa_hormati_celah_tidak_melanggar():
    hasil, konfig = _jalankan_celah(False)
    assert hasil.jumlah_trade == 1
    assert gerbang_invarian_risiko(hasil).lulus is True
    assert baris_pelanggaran(hasil.perdagangan, konfig.slippage) == []
    assert hasil.perdagangan[0].R == pytest.approx(-1.0365128, abs=1e-6)
