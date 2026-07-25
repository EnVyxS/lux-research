"""Pengujian sembilan gerbang mutu.

Setiap gerbang diuji tiga hal: ia meloloskan kasus bersih, ia menjatuhkan
kasus kotor, dan ia menolak melulus­kan diri ketika tidak punya bahan untuk
menilai.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from lux.backtest.engine import Hasil, Perdagangan
from lux.backtest.gerbang import (
    NAMA_GERBANG,
    Gerbang,
    gerbang_buy_and_hold,
    gerbang_checksum,
    gerbang_entri_acak,
    gerbang_forward_fill,
    gerbang_funding,
    gerbang_invarian_risiko,
    gerbang_lookahead,
    gerbang_overlap,
    gerbang_survivorship,
    susun_laporan,
)

JAM = 3_600_000
AWAL = 1_600_000_000_000


def bingkai(harga, rentang=1.0):
    return pd.DataFrame(
        {
            "open_time": [AWAL + i * JAM for i in range(len(harga))],
            "open": harga,
            "high": [p + rentang for p in harga],
            "low": [p - rentang for p in harga],
            "close": harga,
        }
    )


def bingkai_datar(n):
    return pd.DataFrame(
        {
            "open_time": [AWAL + i * JAM for i in range(n)],
            "open": [100.0] * n,
            "high": [100.0] * n,
            "low": [100.0] * n,
            "close": [100.0] * n,
        }
    )


def trade(R_target=1.0, masuk=AWAL, keluar=AWAL + JAM, funding=0.0):
    return Perdagangan(
        symbol="X",
        arah=1,
        masuk_ms=masuk,
        keluar_ms=keluar,
        harga_masuk=100.0,
        harga_keluar=100.0 + R_target,
        ukuran=1.0,
        jarak_stop=1.0,
        alasan_keluar="target",
        biaya_transaksi=0.0,
        biaya_funding=funding,
        laba_kotor=R_target,
    )


# --- 1. forward-fill ------------------------------------------------------
def test_forward_fill_meloloskan_data_bergerak():
    assert gerbang_forward_fill(bingkai([100.0 + i for i in range(50)])).lulus


def test_forward_fill_menjatuhkan_data_yang_diisi_ulang():
    g = gerbang_forward_fill(bingkai_datar(50))
    assert not g.lulus
    assert g.nilai == pytest.approx(1.0)


def test_forward_fill_menjatuhkan_deret_datar_panjang_meski_rasio_kecil():
    """Rasio rendah bisa menyembunyikan lubang panjang di satu tempat."""
    harga = [100.0 + i for i in range(200)]
    df = bingkai(harga)
    for i in range(30, 60):
        df.loc[i, ["open", "high", "low", "close"]] = 100.0
    g = gerbang_forward_fill(df)
    assert not g.lulus


def test_forward_fill_bingkai_kosong_gagal_bukan_lulus():
    g = gerbang_forward_fill(pd.DataFrame(columns=["open", "high", "low", "close"]))
    assert not g.lulus and not g.dapat_dinilai


# --- 2. buy-and-hold ------------------------------------------------------
def test_buy_and_hold_menjatuhkan_strategi_yang_kalah_dari_diam():
    df = bingkai([100.0 * (1.01**i) for i in range(50)])
    h = Hasil(symbol="X", ekuitas=np.linspace(10_000.0, 10_100.0, 50))
    assert not gerbang_buy_and_hold(h, df).lulus


def test_buy_and_hold_meloloskan_strategi_yang_unggul():
    df = bingkai([100.0] * 50)
    h = Hasil(symbol="X", ekuitas=np.linspace(10_000.0, 12_000.0, 50))
    assert gerbang_buy_and_hold(h, df).lulus


def test_buy_and_hold_tanpa_ekuitas_gagal():
    g = gerbang_buy_and_hold(Hasil(symbol="X"), bingkai([100.0] * 5))
    assert not g.lulus and not g.dapat_dinilai


# --- 3. entri acak --------------------------------------------------------
def test_entri_acak_menjatuhkan_hasil_yang_biasa_saja():
    """Bila permutasi menyamai hasil nyata, yang terukur bukan pemilihan momen."""
    sinyal = np.array([0, 1, 0, -1, 1, 0, 0, 1])
    g = gerbang_entri_acak(1.0, sinyal, lambda s: 1.0, ulangan=50)
    assert not g.lulus
    assert g.nilai == pytest.approx(1.0)


def test_entri_acak_meloloskan_hasil_yang_tak_tertandingi():
    sinyal = np.array([0, 1, 0, -1, 1, 0, 0, 1])
    g = gerbang_entri_acak(99.0, sinyal, lambda s: 0.0, ulangan=99)
    assert g.lulus
    assert g.nilai == pytest.approx(0.01)


def test_entri_acak_tidak_pernah_menghasilkan_p_nol():
    """Sampel terbatas tidak boleh mengaku pasti."""
    sinyal = np.array([1, 0, -1, 1])
    g = gerbang_entri_acak(1e9, sinyal, lambda s: 0.0, ulangan=1000)
    assert g.nilai > 0.0


def test_entri_acak_tanpa_sinyal_gagal():
    g = gerbang_entri_acak(1.0, np.zeros(10, dtype=int), lambda s: 0.0)
    assert not g.lulus and not g.dapat_dinilai


def test_entri_acak_mempertahankan_jumlah_dan_arah_sinyal():
    """Permutasi harus merusak waktunya saja, bukan komposisinya."""
    sinyal = np.array([1, 1, -1, 0, 0, 0])
    dilihat = []
    gerbang_entri_acak(1.0, sinyal, lambda s: dilihat.append(s.copy()) or 0.0, 5)
    for s in dilihat:
        assert sorted(s.tolist()) == sorted(sinyal.tolist())


# --- 4. lookahead ---------------------------------------------------------
def test_lookahead_meloloskan_sinyal_kausal():
    df = bingkai([100.0 + i for i in range(60)])

    def sinyal(d):
        c = d["close"].to_numpy()
        return (np.arange(len(c)) % 7 == 0).astype(int)

    assert gerbang_lookahead(df, sinyal).lulus


def test_lookahead_menjatuhkan_normalisasi_seluruh_periode():
    """Rerata seluruh periode adalah lookahead yang paling sering lolos."""
    df = bingkai([100.0 + i for i in range(60)])

    def sinyal(d):
        c = d["close"].to_numpy()
        return (c > c.mean()).astype(int)

    g = gerbang_lookahead(df, sinyal)
    assert not g.lulus
    assert g.nilai > 0


def test_lookahead_data_terlalu_pendek_gagal():
    g = gerbang_lookahead(bingkai([100.0] * 5), lambda d: np.zeros(len(d), dtype=int))
    assert not g.lulus and not g.dapat_dinilai


# --- 5. invarian risiko ---------------------------------------------------
def test_invarian_risiko_meloloskan_kerugian_wajar():
    h = Hasil(symbol="X", perdagangan=[trade(1.0), trade(-1.1)])
    assert gerbang_invarian_risiko(h).lulus


def test_invarian_risiko_menjatuhkan_kerugian_ekstrem():
    h = Hasil(symbol="X", perdagangan=[trade(1.0), trade(-4.0)])
    g = gerbang_invarian_risiko(h)
    assert not g.lulus
    assert g.nilai == pytest.approx(-4.0)


def test_invarian_risiko_tanpa_trade_gagal():
    g = gerbang_invarian_risiko(Hasil(symbol="X"))
    assert not g.lulus and not g.dapat_dinilai


# --- 6. funding -----------------------------------------------------------
def test_funding_menjatuhkan_hasil_yang_fundingnya_nol():
    h = Hasil(symbol="X", perdagangan=[trade(funding=0.0)])
    assert not gerbang_funding(h, jadwal_dimuat=True).lulus


def test_funding_meloloskan_hasil_yang_menagih():
    h = Hasil(symbol="X", perdagangan=[trade(funding=0.03)])
    assert gerbang_funding(h, jadwal_dimuat=True).lulus


def test_funding_tanpa_jadwal_gagal_bukan_lulus():
    """Lupa memuat jadwal tidak boleh terlihat sama dengan tidak ada biaya."""
    h = Hasil(symbol="X", perdagangan=[trade(funding=0.0)])
    g = gerbang_funding(h, jadwal_dimuat=False)
    assert not g.lulus and not g.dapat_dinilai


# --- 7. overlap -----------------------------------------------------------
def test_overlap_meloloskan_perdagangan_berurutan():
    h = Hasil(
        symbol="X",
        perdagangan=[
            trade(masuk=AWAL, keluar=AWAL + JAM),
            trade(masuk=AWAL + JAM, keluar=AWAL + 2 * JAM),
        ],
    )
    assert gerbang_overlap(h).lulus


def test_overlap_menjatuhkan_posisi_bertumpuk():
    h = Hasil(
        symbol="X",
        perdagangan=[
            trade(masuk=AWAL, keluar=AWAL + 5 * JAM),
            trade(masuk=AWAL + JAM, keluar=AWAL + 6 * JAM),
        ],
    )
    g = gerbang_overlap(h)
    assert not g.lulus
    assert g.nilai == pytest.approx(1.0)


# --- 8. checksum ----------------------------------------------------------
def test_checksum_meloloskan_manifest_yang_cocok():
    m = {"a.parquet": "aa", "b.parquet": "bb"}
    assert gerbang_checksum(m, dict(m)).lulus


def test_checksum_menjatuhkan_berkas_asing():
    """Kasus nyata: aset _retry usang menambah 12.593 baris ke hasil validasi."""
    m = {"a.parquet": "aa"}
    g = gerbang_checksum(m, {"a.parquet": "aa", "a_retry.parquet": "cc"})
    assert not g.lulus


def test_checksum_menjatuhkan_isi_yang_berubah():
    assert not gerbang_checksum({"a": "aa"}, {"a": "zz"}).lulus


def test_checksum_manifest_kosong_gagal():
    g = gerbang_checksum({}, {})
    assert not g.lulus and not g.dapat_dinilai


# --- 9. survivorship ------------------------------------------------------
def test_survivorship_meloloskan_porsi_delisted_yang_sebanding():
    semesta = [f"S{i}" for i in range(100)]
    mati = semesta[:20]
    diuji = semesta[:10] + semesta[20:70]
    assert gerbang_survivorship(diuji, mati, semesta).lulus


def test_survivorship_menjatuhkan_uji_yang_hanya_memakai_yang_selamat():
    semesta = [f"S{i}" for i in range(100)]
    mati = semesta[:20]
    assert not gerbang_survivorship(semesta[20:], mati, semesta).lulus


def test_survivorship_universe_tanpa_delisted_gagal():
    semesta = [f"S{i}" for i in range(10)]
    g = gerbang_survivorship(semesta, [], semesta)
    assert not g.lulus and not g.dapat_dinilai


# --- laporan gabungan -----------------------------------------------------
def test_laporan_menuntut_kesembilan_gerbang_hadir():
    lulus_semua = [
        Gerbang(n, True, 1.0, 0.0, "") for n in NAMA_GERBANG[:8]
    ]
    lap = susun_laporan(lulus_semua)
    assert not lap.semua_lulus
    assert "survivorship" in lap.yang_gagal


def test_laporan_lulus_hanya_bila_sembilan_sembilannya_lulus():
    lap = susun_laporan([Gerbang(n, True, 1.0, 0.0, "") for n in NAMA_GERBANG])
    assert lap.semua_lulus
    assert lap.yang_gagal == []


def test_satu_gerbang_gagal_menjatuhkan_seluruhnya():
    g = [Gerbang(n, n != "funding", 1.0, 0.0, "") for n in NAMA_GERBANG]
    lap = susun_laporan(g)
    assert not lap.semua_lulus
    assert lap.yang_gagal == ["funding"]
    assert lap.ke_dict()["gerbang_gagal"] == ["funding"]
