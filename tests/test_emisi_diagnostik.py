"""Uji emisi laporan diagnostik (ADR-038 bagian 5.4, rancangan jurnal 44).

Boneka perdagangan di sini disalin dari ``tests/test_pelanggaran_risiko.py``
yang sudah hijau, dan uji terakhir menjalankan **mesin sungguhan**. Uji yang
hanya menyusun ``Perdagangan`` dengan tangan menguji model penulisnya tentang
mesin, bukan mesinnya (cacat kelas 12, aturan 42).
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

from lux.backtest.engine import Konfig, Perdagangan, jalankan
from lux.diagnostik.emisi import (
    AWALAN,
    emisikan,
    jalur_laporan,
    tulis_laporan,
)
from lux.diagnostik.pelanggaran_risiko import AMBANG_KERUGIAN_R, KOLOM

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


def _konfig(slippage: float = 0.0005, hormati: bool = True) -> Konfig:
    return Konfig(
        atr_periode=2,
        atr_pengali_stop=2.0,
        slippage=slippage,
        fee=0.0005,
        stop_hormati_celah=hormati,
    )


def _muat_json(p):
    return json.loads(p.read_text(encoding="utf-8"))


BAR_CELAH = [
    (100.0, 101.0, 99.0, 100.0),
    (100.0, 101.0, 99.0, 100.0),
    (100.0, 101.0, 99.0, 100.0),
    (100.0, 101.0, 99.0, 100.0),
    (60.0, 61.0, 55.0, 58.0),
    (58.0, 59.0, 57.0, 58.0),
]
SINYAL_CELAH = np.array([0, 0, 1, 0, 0, 0], dtype="int64")


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


# --- berkas keluaran --------------------------------------------------------
def test_menulis_dua_berkas(tmp_path):
    ringkas = tulis_laporan([_trade(-9.0)], _konfig(), "K", dir_laporan=tmp_path)
    assert (tmp_path / f"{AWALAN}K.md").exists()
    assert (tmp_path / f"{AWALAN}K.json").exists()
    assert ringkas["berkas_md"].endswith(f"{AWALAN}K.md")


def test_nama_berkas_memakai_nama_sel(tmp_path):
    tulis_laporan([_trade(-2.0)], _konfig(), "h015_F", dir_laporan=tmp_path)
    assert jalur_laporan("h015_F", ".json", tmp_path).exists()


def test_direktori_dibuat_bila_belum_ada(tmp_path):
    tujuan = tmp_path / "belum" / "ada"
    tulis_laporan([_trade(-2.0)], _konfig(), "A", dir_laporan=tujuan)
    assert (tujuan / f"{AWALAN}A.md").exists()


@pytest.mark.parametrize("nama", ["../lolos", "a/b", ""])
def test_nama_tidak_sah_ditolak(tmp_path, nama):
    with pytest.raises(ValueError):
        tulis_laporan([_trade(-2.0)], _konfig(), nama, dir_laporan=tmp_path)


# --- isi laporan ------------------------------------------------------------
def test_markdown_memuat_nama_dan_kolom(tmp_path):
    tulis_laporan([_trade(-2.0)], _konfig(), "K", dir_laporan=tmp_path)
    teks = (tmp_path / f"{AWALAN}K.md").read_text(encoding="utf-8")
    assert "K" in teks
    for k in KOLOM:
        assert k in teks


def test_json_memuat_baris_dan_ringkas(tmp_path):
    tulis_laporan(
        [_trade(-9.0), _trade(-2.0, symbol="BBBUSDT", alasan="umur")],
        _konfig(),
        "K",
        dir_laporan=tmp_path,
    )
    data = _muat_json(tmp_path / f"{AWALAN}K.json")
    assert data["ringkas"]["cacah_pelanggaran"] == 2
    assert data["cacah_baris"] == 2
    assert [b["R"] for b in data["baris"]] == pytest.approx([-9.0, -2.0])
    assert data["ringkas"]["per_alasan"] == {"stop": 1, "umur": 1}


def test_tanpa_pelanggaran_tetap_menulis(tmp_path):
    ringkas = tulis_laporan([_trade(-1.0)], _konfig(), "K", dir_laporan=tmp_path)
    assert ringkas["cacah_pelanggaran"] == 0
    assert "Tidak ada perdagangan yang melewati ambang." in (
        tmp_path / f"{AWALAN}K.md"
    ).read_text(encoding="utf-8")


def test_ambang_dari_gerbang_bukan_diketik(tmp_path):
    ringkas = tulis_laporan([_trade(-2.0)], _konfig(), "K", dir_laporan=tmp_path)
    assert ringkas["ambang_R"] == pytest.approx(-AMBANG_KERUGIAN_R)


def test_cacah_trade_dilaporkan_dari_pemanggil(tmp_path):
    ringkas = tulis_laporan(
        [_trade(-2.0)], _konfig(), "K", dir_laporan=tmp_path, cacah_trade=1000
    )
    assert ringkas["cacah_trade"] == 1000
    assert ringkas["porsi"] == pytest.approx(0.001)


def test_json_dipotong_dan_dinyatakan(tmp_path):
    trades = [_trade(-2.0 - i / 100) for i in range(5)]
    ringkas = tulis_laporan(
        trades, _konfig(), "K", dir_laporan=tmp_path, batas_baris_json=2
    )
    data = _muat_json(tmp_path / f"{AWALAN}K.json")
    assert ringkas["dipotong_json"] is True
    assert data["cacah_baris"] == 5
    assert data["cacah_baris_ditulis"] == 2
    assert data["ringkas"]["cacah_pelanggaran"] == 5


# --- kemurnian --------------------------------------------------------------
def test_slippage_diambil_dari_konfig(tmp_path):
    trade = _trade(-9.0)
    a = tulis_laporan([trade], _konfig(slippage=0.0), "A", dir_laporan=tmp_path)
    b = tulis_laporan([trade], _konfig(slippage=0.01), "B", dir_laporan=tmp_path)
    assert a["terburuk_selisih_stop_R"] != b["terburuk_selisih_stop_R"]
    assert _muat_json(tmp_path / f"{AWALAN}B.json")["slippage"] == pytest.approx(0.01)


def test_konfig_tidak_diubah(tmp_path):
    konfig = _konfig()
    medan = ("slippage", "fee", "stop_hormati_celah", "atr_periode", "atr_pengali_stop")
    sebelum = {k: getattr(konfig, k) for k in medan}
    tulis_laporan([_trade(-9.0)], konfig, "K", dir_laporan=tmp_path)
    assert {k: getattr(konfig, k) for k in medan} == sebelum


# --- pintu masuk sisi runner ------------------------------------------------
def test_emisikan_menangkap_galat_dan_memancarkannya(tmp_path):
    hasil = emisikan([_trade(-2.0)], _konfig(), "../lolos", dir_laporan=tmp_path)
    assert "galat" in hasil
    assert "ValueError" in hasil["galat"]


def test_emisikan_mengembalikan_kunci_untuk_isi(tmp_path):
    hasil = emisikan([_trade(-9.0)], _konfig(), "K", dir_laporan=tmp_path)
    for k in (
        "berkas_md",
        "berkas_json",
        "cacah_pelanggaran",
        "per_alasan",
        "terburuk_R",
    ):
        assert k in hasil
    assert "galat" not in hasil


# --- mesin sungguhan --------------------------------------------------------
def test_mesin_sungguhan_ujung_ke_ujung(tmp_path):
    konfig = _konfig(hormati=True)
    hasil = jalankan(_bingkai(BAR_CELAH), SINYAL_CELAH, konfig, None, "GAPUSDT")
    ringkas = emisikan(
        hasil.perdagangan, konfig, "celah", dir_laporan=tmp_path,
        cacah_trade=hasil.jumlah_trade,
    )
    data = _muat_json(tmp_path / f"{AWALAN}celah.json")
    assert ringkas["cacah_pelanggaran"] == 1
    assert ringkas["per_alasan"] == {"stop": 1}
    assert ringkas["cacah_celah_melewati_stop"] == 1
    assert data["baris"][0]["harga_keluar_bruto"] == pytest.approx(BAR_CELAH[4][0])
    assert data["baris"][0]["R"] == pytest.approx(-10.0400025, abs=1e-6)
