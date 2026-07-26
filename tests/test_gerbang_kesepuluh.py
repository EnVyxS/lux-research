"""Pengujian penyambungan gerbang kesepuluh (ADR-010).

Berkas terpisah dari ``test_gerbang.py`` supaya jelas apa yang berubah ketika
daftar gerbang bertambah, dan supaya pengujian lama tidak perlu disentuh.

Yang dikunci: daftar resmi memuat konsentrasi, laporan menuntut kehadirannya,
dan ``semua_lulus`` tidak lagi bergantung pada angka yang ditulis tangan.

**Diperbaiki saat gerbang kesebelas masuk.** Versi pertama berkas ini memakai
``len(NAMA_GERBANG) == 10`` di tiga tempat, yaitu persis literal tulisan tangan
yang dilarang oleh berkas yang diujinya. Literalnya pecah begitu ADR-011
menambah satu gerbang. Sekarang berkas ini hanya menguji kehadiran dan
kewajiban ``konsentrasi``; jumlah gerbang diuji di satu tempat saja, di
``test_gerbang_kesebelas.py``, supaya perubahannya harus disengaja.
"""

from __future__ import annotations

from lux.backtest.gerbang import NAMA_GERBANG, Gerbang, susun_laporan
from lux.backtest.konsentrasi import gerbang_konsentrasi


def test_konsentrasi_terdaftar_dan_daftar_tidak_berulang():
    assert "konsentrasi" in NAMA_GERBANG
    assert len(set(NAMA_GERBANG)) == len(NAMA_GERBANG)


def test_laporan_tanpa_konsentrasi_tidak_cukup():
    """Orkestrator yang lupa gerbang ini harus gagal, bukan lolos diam-diam."""
    lama = [
        Gerbang(n, True, 1.0, 0.0, "") for n in NAMA_GERBANG if n != "konsentrasi"
    ]
    lap = susun_laporan(lama)
    assert not lap.semua_lulus
    assert lap.yang_gagal == ["konsentrasi"]


def test_seluruh_gerbang_lulus_berarti_laporan_lulus():
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
