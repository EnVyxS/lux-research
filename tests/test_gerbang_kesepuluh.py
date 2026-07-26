"""Pengujian penyambungan gerbang kesepuluh (ADR-010).

Berkas terpisah dari ``test_gerbang.py`` supaya jelas apa yang berubah ketika
daftar gerbang bertambah, dan supaya pengujian lama tidak perlu disentuh.

Yang dikunci: daftar resmi memuat konsentrasi, laporan menuntut kehadirannya,
dan ``semua_lulus`` tidak lagi bergantung pada angka yang ditulis tangan.
"""

from __future__ import annotations

from lux.backtest.gerbang import NAMA_GERBANG, Gerbang, susun_laporan
from lux.backtest.konsentrasi import gerbang_konsentrasi


def test_daftar_gerbang_menjadi_sepuluh():
    assert len(NAMA_GERBANG) == 10
    assert NAMA_GERBANG[-1] == "konsentrasi"
    assert len(set(NAMA_GERBANG)) == 10


def test_sembilan_gerbang_lama_tidak_lagi_cukup():
    """Orkestrator yang lupa gerbang baru harus gagal, bukan lolos diam-diam."""
    lama = [Gerbang(n, True, 1.0, 0.0, "") for n in NAMA_GERBANG[:9]]
    lap = susun_laporan(lama)
    assert not lap.semua_lulus
    assert lap.yang_gagal == ["konsentrasi"]


def test_kesepuluh_lulus_berarti_laporan_lulus():
    lap = susun_laporan([Gerbang(n, True, 1.0, 0.0, "") for n in NAMA_GERBANG])
    assert lap.semua_lulus
    assert lap.yang_gagal == []


def test_konsentrasi_gagal_menjatuhkan_seluruh_laporan():
    g = [Gerbang(n, n != "konsentrasi", 1.0, 0.0, "") for n in NAMA_GERBANG]
    lap = susun_laporan(g)
    assert not lap.semua_lulus
    assert lap.yang_gagal == ["konsentrasi"]


def test_nama_gerbang_dari_fungsi_cocok_dengan_daftar():
    """Nama yang dikembalikan fungsi harus sama dengan yang didaftarkan.

    Salah tulis satu huruf akan membuat susun_laporan menganggap gerbangnya
    tidak dijalankan, dan gerbang yang benar-benar berjalan akan dibuang.
    """
    g = gerbang_konsentrasi([])
    assert g.nama in NAMA_GERBANG
