"""Pengujian orkestrator walk-forward.

Tiga pengujian di berkas ini mengunci cacat yang sempat ada di versi pertama
orkestrator: overlap yang dinilai atas perdagangan campuran antar simbol,
survivorship yang membandingkan subset dengan dirinya sendiri, dan gerbang
gabungan yang meluluskan mayoritas alih-alih menuntut semuanya.

Tambahan ADR-003: dua pengujian baru mengunci perilaku pemangkasan ekor datar
pada ``muat_ohlcv`` dan pembacaan tanggal kematian sejati pada
``akhir_per_simbol``.
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from lux.backtest.engine import Hasil, Perdagangan
from lux.backtest.gerbang import Gerbang
from lux.backtest.run_wf import (
    akhir_per_simbol,
    gabung_gerbang,
    gerbang_bnh_gabungan,
    gerbang_overlap_gabungan,
    hipotesis_h001,
    muat_ohlcv,
    pilih_berkas,
    ringkas_gabungan,
    sha256_berkas,
    simbol_mati,
    simbol_mati_dari_akhir,
)

HARI = 86_400_000
JAM = 3_600_000
AWAL = 1_600_000_000_000


def bingkai_sampai(akhir_ms, n=10):
    return pd.DataFrame({"open_time": [akhir_ms - (n - 1 - i) * HARI for i in range(n)]})


def trade(symbol, masuk, keluar):
    return Perdagangan(
        symbol=symbol,
        arah=1,
        masuk_ms=masuk,
        keluar_ms=keluar,
        harga_masuk=100.0,
        harga_keluar=101.0,
        ukuran=1.0,
        jarak_stop=2.0,
        alasan_keluar="target",
        biaya_transaksi=0.1,
        biaya_funding=0.01,
        laba_kotor=1.0,
    )


# --- ADR-003: muat_ohlcv memangkas ekor datar ----------------------------
def test_muat_ohlcv_memangkas_ekor_datar(tmp_path):
    """muat_ohlcv harus memanggil potong_ekor per simbol setelah sort.

    Ekor datar (o=h=l=c, volume 0) dari simbol mati harus terpangkas sebelum
    data masuk ke walk-forward. Bila tidak, bar palsu ikut diperdagangkan dan
    posisi dapat bertahan berbulan-bulan tanpa volume nyata.
    """
    N_HIDUP = 200  # bar dengan harga bergerak
    N_EKOR = 50   # bar datar di ujung (simulasi padding simbol mati)
    N_TOTAL = N_HIDUP + N_EKOR

    times = [AWAL + i * JAM for i in range(N_TOTAL)]
    # Bar hidup: harga naik sedikit tiap bar
    opens = [100.0 + i * 0.01 for i in range(N_HIDUP)] + [101.99] * N_EKOR
    highs = [o + 0.5 for o in opens[:N_HIDUP]] + list(opens[N_HIDUP:])
    lows = [o - 0.5 for o in opens[:N_HIDUP]] + list(opens[N_HIDUP:])
    closes = list(opens)
    volumes = [500.0] * N_HIDUP + [0.0] * N_EKOR

    df = pd.DataFrame({
        "symbol": ["TESUSDT"] * N_TOTAL,
        "open_time": times,
        "open": opens,
        "high": highs,
        "low": lows,
        "close": closes,
        "volume": volumes,
    })
    pq.write_table(pa.Table.from_pandas(df), tmp_path / "ohlcv_1h_shard00.parquet")

    bingkai, _ = muat_ohlcv(tmp_path, "1h", {"TESUSDT"})

    assert "TESUSDT" in bingkai
    # Ekor 50 bar datar harus hilang
    assert len(bingkai["TESUSDT"]) == N_HIDUP


# --- ADR-003: akhir_per_simbol membaca dari JSON --------------------------
def test_akhir_per_simbol_membaca_akhir_sejati_json(tmp_path):
    """Bila akhir_sejati.json tersedia, stempel harus diambil dari sana.

    Stempel mentah dari parquet untuk simbol mati sama dengan tanggal ujung
    dataset, sehingga gerbang survivorship tidak dapat membedakan simbol mati
    dari simbol hidup. JSON menyimpan tanggal kematian nyata.
    """
    data = {
        "interval": "1h",
        "akhir": {
            "BTCUSDT": {"akhir_ms": 1784934000000, "dipangkas": 0, "bar_awal": 57552},
            "RENUSDT": {"akhir_ms": 1733216400000, "dipangkas": 14366, "bar_awal": 50657},
        },
    }
    json_path = tmp_path / "akhir_sejati.json"
    json_path.write_text(json.dumps(data), encoding="utf-8")

    hasil = akhir_per_simbol(tmp_path, "1h", json_path)

    assert hasil["BTCUSDT"] == 1784934000000
    # RENUSDT: tanggal kematian sejati, jauh lebih awal dari ujung dataset
    assert hasil["RENUSDT"] == 1733216400000
    assert len(hasil) == 2


def test_akhir_per_simbol_fallback_bila_json_tidak_ada(tmp_path):
    """Bila JSON tidak ada, fungsi jatuh ke parquet mentah (fallback).

    Dalam produksi ini tidak boleh terjadi, tapi fallback penting untuk
    pengujian unit yang tidak membutuhkan JSON.
    """
    # Tidak ada JSON, tidak ada parquet — hasilnya kosong
    hasil = akhir_per_simbol(tmp_path, "1h", tmp_path / "tidak_ada.json")
    assert hasil == {}


def test_akhir_per_simbol_tanpa_json_path_fallback_ke_parquet(tmp_path):
    """Bila akhir_sejati_path=None, harus tetap membaca dari parquet."""
    # Tidak ada parquet — hasilnya kosong, tidak ada error
    hasil = akhir_per_simbol(tmp_path, "1h", None)
    assert hasil == {}


# --- simbol mati ----------------------------------------------------------
def test_simbol_mati_dikenali_dari_data_sendiri():
    b = {
        "HIDUP": bingkai_sampai(AWAL + 400 * HARI),
        "MATI": bingkai_sampai(AWAL + 100 * HARI),
    }
    assert simbol_mati(b) == {"MATI"}


def test_simbol_yang_baru_berhenti_belum_dianggap_mati():
    b = {
        "A": bingkai_sampai(AWAL + 400 * HARI),
        "B": bingkai_sampai(AWAL + 390 * HARI),
    }
    assert simbol_mati(b, ambang_hari=30) == set()


def test_simbol_mati_pada_kumpulan_kosong():
    assert simbol_mati({}) == set()
    assert simbol_mati_dari_akhir({}) == set()


def test_simbol_mati_dari_stempel_akhir():
    akhir = {"A": AWAL + 400 * HARI, "B": AWAL + 10 * HARI}
    assert simbol_mati_dari_akhir(akhir) == {"B"}


# --- penggabungan ---------------------------------------------------------
def test_ekspektasi_gabungan_menimbang_jumlah_perdagangan():
    """Simbol dengan tiga trade tidak boleh setara dengan yang tiga ratus."""
    kecil = {
        "jumlah_trade_luar_sampel": 3,
        "total_R": 3.0,
        "jumlah_jendela": 1,
        "jendela_positif": 1,
    }
    besar = {
        "jumlah_trade_luar_sampel": 300,
        "total_R": -30.0,
        "jumlah_jendela": 5,
        "jendela_positif": 1,
    }
    g = ringkas_gabungan([kecil, besar])
    assert g["jumlah_trade_luar_sampel"] == 303
    assert g["ekspektasi_R"] == pytest.approx(-27.0 / 303)
    assert g["ekspektasi_R"] < 0


def test_gabungan_tanpa_trade_tidak_mengarang_ekspektasi():
    g = ringkas_gabungan(
        [
            {
                "jumlah_trade_luar_sampel": 0,
                "total_R": 0.0,
                "jumlah_jendela": 2,
                "jendela_positif": 0,
            }
        ]
    )
    assert g["ekspektasi_R"] is None


def test_satu_simbol_gagal_menjatuhkan_gerbang_gabungan():
    """Gerbang bukan skor: mayoritas lulus tidak cukup."""
    daftar = [
        Gerbang("x", True, 0.1, 0.3, ""),
        Gerbang("x", True, 0.2, 0.3, ""),
        Gerbang("x", False, 0.9, 0.3, ""),
    ]
    g = gabung_gerbang("x", daftar, 0.3)
    assert not g.lulus
    assert g.nilai == 0.9


def test_gerbang_gabungan_tanpa_simbol_tidak_dapat_dinilai():
    g = gabung_gerbang("x", [], 0.3)
    assert not g.lulus
    assert g.nilai is None


# --- overlap --------------------------------------------------------------
def test_posisi_serempak_pada_simbol_berbeda_bukan_pelanggaran():
    """Dua simbol berjalan bersamaan adalah diversifikasi, bukan penumpukan."""
    hasil = {
        "A": Hasil(symbol="A", perdagangan=[trade("A", 0, 100), trade("A", 200, 300)]),
        "B": Hasil(symbol="B", perdagangan=[trade("B", 0, 100), trade("B", 200, 300)]),
    }
    assert gerbang_overlap_gabungan(hasil).lulus


def test_posisi_bertindih_pada_simbol_sama_tetap_gagal():
    hasil = {
        "A": Hasil(symbol="A", perdagangan=[trade("A", 0, 500), trade("A", 100, 600)]),
    }
    assert not gerbang_overlap_gabungan(hasil).lulus


# --- buy and hold ---------------------------------------------------------
def test_bnh_memakai_median_bukan_rerata():
    """Satu simbol yang meroket tidak boleh menyelamatkan sisanya."""
    daftar = [
        Gerbang("buy_and_hold", False, -0.1, 0.0, ""),
        Gerbang("buy_and_hold", False, -0.2, 0.0, ""),
        Gerbang("buy_and_hold", True, 50.0, 0.0, ""),
    ]
    g = gerbang_bnh_gabungan(daftar)
    assert not g.lulus
    assert g.nilai == pytest.approx(-0.1)


def test_bnh_tanpa_simbol_tidak_dapat_dinilai():
    g = gerbang_bnh_gabungan([])
    assert not g.lulus
    assert g.nilai is None


# --- lain-lain ------------------------------------------------------------
def test_aset_retry_tidak_pernah_ikut_terbaca(tmp_path):
    """Aturan yang sama dengan validasi, diulang agar tidak diam-diam berubah."""
    (tmp_path / "ohlcv_1h_shard00.parquet").write_bytes(b"x")
    (tmp_path / "ohlcv_1h_retry_shard00.parquet").write_bytes(b"x")
    nama = [p.name for p in pilih_berkas(tmp_path, "1h")]
    assert nama == ["ohlcv_1h_shard00.parquet"]


def test_sha256_berkas_stabil(tmp_path):
    p = tmp_path / "a.bin"
    p.write_bytes(b"lux")
    assert sha256_berkas(p) == sha256_berkas(p)
    assert len(sha256_berkas(p)) == 64


def test_hipotesis_h001_terkunci_pada_kriteria_yang_ketat():
    h = hipotesis_h001()
    assert h.kriteria.min_trade_luar_sampel == 100
    assert h.kriteria.maks_p_entri_acak == 0.05
    assert h.jumlah_kombinasi == 3
    # Dataset harus mencerminkan ADR-003
    assert "438" in h.dataset
    assert "ADR-003" in h.dataset


def test_hasil_pool_menerima_ekuitas_satu_titik():
    """Bentuk yang dipakai orkestrator untuk gerbang lintas simbol."""
    h = Hasil(symbol="POOL", perdagangan=[trade("A", 0, 1)], ekuitas=np.array([10000.0]))
    assert h.jumlah_trade == 1
