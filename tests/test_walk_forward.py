"""Pengujian walk-forward dan pra-registrasi."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from lux.backtest.walk_forward import (
    Jendela,
    bagi_jendela,
    jalankan_walk_forward,
)
from lux.praregistrasi import Hipotesis, Kriteria, muat, nilai, simpan

JAM = 3_600_000
AWAL = 1_600_000_000_000


def bingkai(n, naik=0.5):
    harga = [100.0 + i * naik for i in range(n)]
    return pd.DataFrame(
        {
            "open_time": [AWAL + i * JAM for i in range(n)],
            "open": harga,
            "high": [p + 1.0 for p in harga],
            "low": [p - 1.0 for p in harga],
            "close": harga,
        }
    )


# --- pembagian jendela ----------------------------------------------------
def test_jendela_uji_tidak_saling_bertindih():
    js = bagi_jendela(1000, 300, 100)
    for a, b in zip(js, js[1:]):
        assert a.uji_akhir <= b.uji_awal


def test_jendela_uji_selalu_setelah_jendela_latih():
    for j in bagi_jendela(1000, 300, 100, embargo=24):
        assert j.uji_awal >= j.latih_akhir
        assert j.embargo == 24


def test_embargo_menyisipkan_jarak_kosong():
    tanpa = bagi_jendela(1000, 300, 100, embargo=0)[0]
    dengan = bagi_jendela(1000, 300, 100, embargo=50)[0]
    assert tanpa.uji_awal == tanpa.latih_akhir
    assert dengan.uji_awal == dengan.latih_akhir + 50


def test_jendela_berjangkar_tumbuh_dari_awal():
    js = bagi_jendela(1000, 300, 100, berjangkar=True)
    assert all(j.latih_awal == 0 for j in js)
    assert js[-1].panjang_latih > js[0].panjang_latih


def test_jendela_bergulir_panjangnya_tetap():
    js = bagi_jendela(1000, 300, 100)
    assert len({j.panjang_latih for j in js}) == 1


def test_sisa_data_yang_tidak_cukup_dibuang_bukan_dipendekkan():
    js = bagi_jendela(455, 300, 100)
    assert len(js) == 1
    assert all(j.panjang_uji == 100 for j in js)


def test_data_terlalu_pendek_menghasilkan_nol_jendela():
    assert bagi_jendela(100, 300, 100) == []


def test_jendela_menolak_batas_mustahil():
    with pytest.raises(ValueError):
        Jendela(latih_awal=0, latih_akhir=100, uji_awal=50, uji_akhir=150)
    with pytest.raises(ValueError):
        Jendela(latih_awal=0, latih_akhir=0, uji_awal=0, uji_akhir=10)
    with pytest.raises(ValueError):
        bagi_jendela(1000, 300, 100, embargo=-1)


# --- eksekusi walk-forward ------------------------------------------------
def sinyal_periodik(d, params):
    return (np.arange(len(d)) % params["jeda"] == 0).astype(int)


def test_hanya_perdagangan_luar_sampel_yang_dihitung():
    df = bingkai(900)
    hasil = jalankan_walk_forward(
        df,
        kandidat=[{"jeda": 20}, {"jeda": 30}],
        buat_sinyal=sinyal_periodik,
        panjang_latih=300,
        panjang_uji=150,
        min_trade_latih=1,
    )
    r = hasil.ringkas()
    assert r["jumlah_jendela"] >= 1
    assert r["jumlah_trade_luar_sampel"] == len(hasil.perdagangan_luar_sampel)


def test_jumlah_kandidat_ikut_dicatat():
    """Mencoba banyak kombinasi adalah pencarian, dan besarnya harus terlihat."""
    df = bingkai(900)
    kandidat = [{"jeda": j} for j in range(10, 40)]
    hasil = jalankan_walk_forward(
        df,
        kandidat=kandidat,
        buat_sinyal=sinyal_periodik,
        panjang_latih=300,
        panjang_uji=150,
        min_trade_latih=1,
    )
    assert hasil.ringkas()["jumlah_kandidat"] == 30


def test_pemanasan_tidak_membuka_posisi_sebelum_jendela_uji():
    """Bar pemanasan hanya boleh memberi makan indikator."""
    df = bingkai(900)
    hasil = jalankan_walk_forward(
        df,
        kandidat=[{"jeda": 15}],
        buat_sinyal=sinyal_periodik,
        panjang_latih=300,
        panjang_uji=150,
        pemanasan=50,
        min_trade_latih=1,
    )
    for h in hasil.per_jendela:
        batas = df["open_time"].iloc[h.jendela.uji_awal]
        for p in h.hasil_uji.perdagangan:
            assert p.masuk_ms >= batas


def test_buat_sinyal_hanya_menerima_potongan_yang_diberikan():
    """Kebocoran antar jendela mustahil bila fungsi sinyal tidak melihat sisanya."""
    df = bingkai(900)
    panjang_terlihat = []

    def perekam(d, params):
        panjang_terlihat.append(len(d))
        return np.zeros(len(d), dtype=int)

    jalankan_walk_forward(
        df,
        kandidat=[{"jeda": 20}],
        buat_sinyal=perekam,
        panjang_latih=300,
        panjang_uji=150,
        min_trade_latih=1,
    )
    assert panjang_terlihat
    assert all(n < len(df) for n in panjang_terlihat)


def test_jendela_tanpa_kandidat_layak_dilewati_bukan_dipaksakan():
    df = bingkai(900)
    hasil = jalankan_walk_forward(
        df,
        kandidat=[{"jeda": 20}],
        buat_sinyal=lambda d, p: np.zeros(len(d), dtype=int),
        panjang_latih=300,
        panjang_uji=150,
        min_trade_latih=5,
    )
    assert hasil.per_jendela == []
    assert hasil.ringkas()["ekspektasi_R"] is None


def test_kandidat_kosong_ditolak():
    with pytest.raises(ValueError):
        jalankan_walk_forward(
            bingkai(900),
            kandidat=[],
            buat_sinyal=sinyal_periodik,
            panjang_latih=300,
            panjang_uji=150,
        )


def test_sinyal_dengan_panjang_salah_ditolak():
    with pytest.raises(ValueError):
        jalankan_walk_forward(
            bingkai(900),
            kandidat=[{"jeda": 20}],
            buat_sinyal=lambda d, p: np.zeros(3, dtype=int),
            panjang_latih=300,
            panjang_uji=150,
        )


# --- pra-registrasi -------------------------------------------------------
def hipotesis():
    return Hipotesis(
        id="H-001",
        pernyataan="Breakout ATR unggul pada perp USDT likuid",
        dataset="tier-b-v1 1h",
        ruang_parameter={"jeda": [10, 20, 30], "pengali": [1.5, 2.0]},
    )


def test_jumlah_kombinasi_dihitung_di_muka():
    assert hipotesis().jumlah_kombinasi == 6


def test_sidik_tidak_bergantung_pada_waktu_pembuatan():
    a = hipotesis()
    b = Hipotesis(
        id=a.id,
        pernyataan=a.pernyataan,
        dataset=a.dataset,
        ruang_parameter=dict(a.ruang_parameter),
        dibuat_utc="2020-01-01T00:00:00+00:00",
    )
    assert a.sidik() == b.sidik()


def test_sidik_berubah_saat_kriteria_diubah():
    a = hipotesis()
    b = Hipotesis(
        id=a.id,
        pernyataan=a.pernyataan,
        dataset=a.dataset,
        ruang_parameter=dict(a.ruang_parameter),
        kriteria=Kriteria(min_ekspektasi_R=0.01),
    )
    assert a.sidik() != b.sidik()


def test_menyimpan_ulang_isi_sama_dibiarkan(tmp_path):
    p = tmp_path / "h.json"
    simpan(hipotesis(), p)
    simpan(hipotesis(), p)
    assert muat(p)["id"] == "H-001"


def test_menyunting_hipotesis_setelah_terdaftar_ditolak(tmp_path):
    """Inti seluruh modul: ambang tidak boleh dilonggarkan setelah hasil terlihat."""
    p = tmp_path / "h.json"
    simpan(hipotesis(), p)
    longgar = Hipotesis(
        id="H-001",
        pernyataan=hipotesis().pernyataan,
        dataset=hipotesis().dataset,
        ruang_parameter=hipotesis().ruang_parameter,
        kriteria=Kriteria(min_ekspektasi_R=0.001),
    )
    with pytest.raises(ValueError):
        simpan(longgar, p)


def test_hipotesis_tanpa_ruang_parameter_ditolak():
    with pytest.raises(ValueError):
        Hipotesis(id="H", pernyataan="x", dataset="d", ruang_parameter={})


def test_penilaian_mengumpulkan_semua_alasan_kegagalan():
    ringkasan = {
        "jumlah_trade_luar_sampel": 10,
        "ekspektasi_R": 0.001,
        "jumlah_jendela": 4,
        "jendela_positif": 1,
    }
    putusan = nilai(hipotesis(), ringkasan, p_entri_acak=0.4)
    assert not putusan.lulus
    assert len(putusan.alasan) == 4


def test_uji_entri_acak_yang_tidak_dijalankan_dianggap_gagal():
    ringkasan = {
        "jumlah_trade_luar_sampel": 500,
        "ekspektasi_R": 0.2,
        "jumlah_jendela": 4,
        "jendela_positif": 4,
    }
    putusan = nilai(hipotesis(), ringkasan, p_entri_acak=None)
    assert not putusan.lulus
    assert putusan.alasan == ["uji entri acak tidak dijalankan"]


def test_hasil_yang_memenuhi_semua_kriteria_lulus():
    ringkasan = {
        "jumlah_trade_luar_sampel": 500,
        "ekspektasi_R": 0.2,
        "jumlah_jendela": 4,
        "jendela_positif": 3,
    }
    putusan = nilai(hipotesis(), ringkasan, p_entri_acak=0.01)
    assert putusan.lulus
    assert putusan.alasan == []
