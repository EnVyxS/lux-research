"""Pengujian ADR-004: batas umur posisi dan saringan carry funding.

Dua hal yang dikunci di sini lebih penting daripada saringannya sendiri.

Pertama, **saringan itu mati secara bawaan**. Bila suatu hari ia menyala tanpa
diminta, hasil H-001b yang sudah ditolak akan berubah diam-diam dan seluruh
perbandingan antar hipotesis kehilangan artinya.

Kedua, **proyeksi carry hanya boleh membaca masa lalu**. Menolak entri karena
mengetahui funding yang belum terjadi adalah lookahead paling telanjang yang
mungkin ada di sistem ini, dan ia akan terlihat seperti perbaikan.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from lux.backtest.engine import Konfig, jalankan
from lux.funding_model import Jadwal, carry_terproyeksi_R

JAM = 3_600_000
HARI = 24 * JAM
AWAL = 1_600_000_000_000


def bingkai(harga: list[float], rentang: float = 1.0) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open_time": [AWAL + i * JAM for i in range(len(harga))],
            "open": harga,
            "high": [p + rentang for p in harga],
            "low": [p - rentang for p in harga],
            "close": harga,
        }
    )


def jadwal_rata(rate: float, mulai: int, sampai: int, langkah: int = 8 * JAM) -> Jadwal:
    t = list(range(mulai, sampai, langkah))
    return Jadwal.dari_frame(
        pd.DataFrame({"calc_time": t, "last_funding_rate": [rate] * len(t)})
    )


# --- statistik trailing ---------------------------------------------------
def test_statistik_trailing_tidak_membaca_masa_depan():
    """Rate sesudah waktu masuk tidak boleh memengaruhi apa pun."""
    t = [AWAL + i * 8 * JAM for i in range(10)]
    rate = [0.0001] * 5 + [0.5] * 5
    j = Jadwal.dari_frame(pd.DataFrame({"calc_time": t, "last_funding_rate": rate}))
    rerata, n = j.statistik_trailing(t[4], 30 * HARI)
    assert n == 5
    assert rerata == pytest.approx(0.0001)


def test_statistik_trailing_jendela_kosong_bukan_tebakan():
    j = jadwal_rata(0.0001, AWAL, AWAL + 10 * HARI)
    rerata, n = j.statistik_trailing(AWAL - 1, 30 * HARI)
    assert (rerata, n) == (0.0, 0)


def test_statistik_trailing_menolak_jendela_tak_masuk_akal():
    j = jadwal_rata(0.0001, AWAL, AWAL + 10 * HARI)
    with pytest.raises(ValueError):
        j.statistik_trailing(AWAL, 0)


# --- proyeksi carry -------------------------------------------------------
def test_kerapatan_penagihan_ikut_menentukan_proyeksi():
    """Kisi empat jam menagih dua kali lebih sering pada rate yang sama.

    Mengabaikan kerapatan akan mengulang persis bentuk kesalahan yang membuat
    lux/funding_model.py ditulis.
    """
    mulai = AWAL - 30 * HARI
    delapan = jadwal_rata(0.0001, mulai, AWAL, 8 * JAM)
    empat = jadwal_rata(0.0001, mulai, AWAL, 4 * JAM)
    a = carry_terproyeksi_R(delapan, 1, AWAL, 7 * HARI, 0.04, 30 * HARI)
    b = carry_terproyeksi_R(empat, 1, AWAL, 7 * HARI, 0.04, 30 * HARI)
    assert b == pytest.approx(2 * a, rel=0.05)


def test_short_diproyeksikan_dibayar_saat_carry_positif():
    j = jadwal_rata(0.001, AWAL - 30 * HARI, AWAL)
    long = carry_terproyeksi_R(j, 1, AWAL, 7 * HARI, 0.04, 30 * HARI)
    short = carry_terproyeksi_R(j, -1, AWAL, 7 * HARI, 0.04, 30 * HARI)
    assert long > 0 > short
    assert short == pytest.approx(-long)


def test_tanpa_riwayat_penagihan_proyeksinya_nol():
    j = jadwal_rata(0.001, AWAL, AWAL + 10 * HARI)
    assert carry_terproyeksi_R(j, 1, AWAL - 1, 7 * HARI, 0.04, 30 * HARI) == 0.0


def test_proyeksi_menolak_masukan_mustahil():
    j = jadwal_rata(0.001, AWAL - 30 * HARI, AWAL)
    with pytest.raises(ValueError):
        carry_terproyeksi_R(j, 0, AWAL, 7 * HARI, 0.04)
    with pytest.raises(ValueError):
        carry_terproyeksi_R(j, 1, AWAL, 7 * HARI, 0.0)
    with pytest.raises(ValueError):
        carry_terproyeksi_R(j, 1, AWAL, -1, 0.04)


# --- batas umur posisi ----------------------------------------------------
def test_bawaan_tidak_menyaring_apa_pun():
    """Kunci utama berkas ini: H-001b harus tetap dapat diulang persis."""
    k = Konfig()
    assert k.maks_umur_bar == 0
    assert k.maks_carry_R == 0.0


def test_tanpa_batas_umur_posisi_menggantung_sampai_akhir_data():
    df = bingkai([100.0] * 60)
    sinyal = np.zeros(len(df), dtype=int)
    sinyal[20] = 1
    hasil = jalankan(df, sinyal)
    assert hasil.jumlah_trade == 1
    assert hasil.perdagangan[0].alasan_keluar == "akhir_data"


def test_batas_umur_menutup_posisi_pada_pembukaan_bar_berikutnya():
    df = bingkai([100.0] * 60)
    sinyal = np.zeros(len(df), dtype=int)
    sinyal[20] = 1
    hasil = jalankan(df, sinyal, Konfig(maks_umur_bar=5, slippage=0.001))
    p = hasil.perdagangan[0]
    assert p.alasan_keluar == "umur"
    # Masuk pada pembukaan bar 21, keluar pada pembukaan bar 26.
    assert p.masuk_ms == AWAL + 21 * JAM
    assert p.keluar_ms == AWAL + 26 * JAM
    # Slippage tetap melawan posisi saat keluar.
    assert p.harga_keluar == pytest.approx(100.0 * (1 - 0.001))


def test_batas_umur_diperiksa_sebelum_target_bar_itu():
    """Bar tempat umur tercapai tidak boleh menghadiahkan target.

    Bar 26 dibuat menyapu jauh ke atas. Bila pemeriksaan umur dijalankan
    sesudah stop dan target, posisi akan keluar sebagai 'target' dan mesin
    memberi satu bar gratis kepada setiap posisi yang kedaluwarsa.
    """
    df = bingkai([100.0] * 60)
    df.loc[26, "high"] = 300.0
    sinyal = np.zeros(len(df), dtype=int)
    sinyal[20] = 1
    hasil = jalankan(df, sinyal, Konfig(maks_umur_bar=5))
    assert hasil.perdagangan[0].alasan_keluar == "umur"


def test_stop_tetap_menang_atas_umur_yang_belum_tercapai():
    df = bingkai([100.0] * 60)
    df.loc[24, "low"] = 1.0
    sinyal = np.zeros(len(df), dtype=int)
    sinyal[20] = 1
    hasil = jalankan(df, sinyal, Konfig(maks_umur_bar=100))
    assert hasil.perdagangan[0].alasan_keluar == "stop"


# --- saringan carry di dalam mesin ---------------------------------------
def test_carry_positif_ekstrem_membatalkan_entri_long():
    df = bingkai([100.0] * 60)
    sinyal = np.zeros(len(df), dtype=int)
    sinyal[20] = 1
    j = jadwal_rata(0.01, AWAL - 30 * HARI, AWAL + 60 * JAM)
    k = Konfig(maks_umur_bar=5, maks_carry_R=0.05)
    assert jalankan(df, sinyal, k, jadwal=j).jumlah_trade == 0


def test_carry_negatif_tidak_menghalangi_entri_long():
    """Saringan harus menyaring biaya, bukan menyaring perdagangan."""
    df = bingkai([100.0] * 60)
    sinyal = np.zeros(len(df), dtype=int)
    sinyal[20] = 1
    j = jadwal_rata(-0.01, AWAL - 30 * HARI, AWAL + 60 * JAM)
    k = Konfig(maks_umur_bar=5, maks_carry_R=0.05)
    assert jalankan(df, sinyal, k, jadwal=j).jumlah_trade == 1


def test_carry_ekstrem_tidak_menghalangi_short():
    """Pada carry positif, short justru dibayar."""
    df = bingkai([100.0] * 60)
    sinyal = np.zeros(len(df), dtype=int)
    sinyal[20] = -1
    j = jadwal_rata(0.01, AWAL - 30 * HARI, AWAL + 60 * JAM)
    k = Konfig(maks_umur_bar=5, maks_carry_R=0.05)
    assert jalankan(df, sinyal, k, jadwal=j).jumlah_trade == 1


def test_saringan_menyala_tanpa_jadwal_menolak_entri():
    """Tanpa jadwal, biaya tidak dapat dinilai. Tidak dapat dinilai berarti tolak."""
    df = bingkai([100.0] * 60)
    sinyal = np.zeros(len(df), dtype=int)
    sinyal[20] = 1
    k = Konfig(maks_umur_bar=5, maks_carry_R=0.05)
    assert jalankan(df, sinyal, k, jadwal=None).jumlah_trade == 0


def test_saringan_carry_tanpa_batas_umur_ditolak_keras():
    """Tanpa umur maksimum, tidak ada rentang yang dapat diproyeksikan."""
    df = bingkai([100.0] * 60)
    sinyal = np.zeros(len(df), dtype=int)
    sinyal[20] = 1
    j = jadwal_rata(0.01, AWAL - 30 * HARI, AWAL + 60 * JAM)
    with pytest.raises(ValueError):
        jalankan(df, sinyal, Konfig(maks_carry_R=0.05), jadwal=j)


def test_konfig_menolak_saringan_negatif():
    with pytest.raises(ValueError):
        Konfig(maks_umur_bar=-1)
    with pytest.raises(ValueError):
        Konfig(maks_carry_R=-0.1)
    with pytest.raises(ValueError):
        Konfig(jendela_carry_hari=0)
