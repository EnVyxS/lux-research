"""Pengujian penyambungan gerbang kesebelas (ADR-011).

Berkas ini adalah **satu-satunya** tempat jumlah gerbang ditulis sebagai angka.
Disengaja: satu tripwire yang harus diubah dengan sadar lebih baik daripada
literal yang berserak di banyak berkas, dan jauh lebih baik daripada tidak ada
literal sama sekali — tanpa tripwire, gerbang yang hilang dari daftar tidak
meninggalkan gejala apa pun.
"""

from __future__ import annotations

from lux.backtest.funding_ekor import gerbang_funding_ekor
from lux.backtest.gerbang import NAMA_GERBANG, Gerbang, susun_laporan


def test_daftar_gerbang_menjadi_sebelas():
    """Tripwire. Bila gerbang kedua belas ditambahkan, ubah angka ini sadar."""
    assert len(NAMA_GERBANG) == 11
    assert NAMA_GERBANG[-1] == "funding_ekor"
    assert len(set(NAMA_GERBANG)) == 11


def test_sepuluh_gerbang_lama_tidak_lagi_cukup():
    lama = [Gerbang(n, True, 1.0, 0.0, "") for n in NAMA_GERBANG[:10]]
    lap = susun_laporan(lama)
    assert not lap.semua_lulus
    assert lap.yang_gagal == ["funding_ekor"]


def test_funding_ekor_gagal_menjatuhkan_seluruh_laporan():
    g = [Gerbang(n, n != "funding_ekor", 1.0, 0.0, "") for n in NAMA_GERBANG]
    lap = susun_laporan(g)
    assert not lap.semua_lulus
    assert lap.yang_gagal == ["funding_ekor"]


def test_kesebelas_lulus_berarti_laporan_lulus():
    lap = susun_laporan([Gerbang(n, True, 1.0, 0.0, "") for n in NAMA_GERBANG])
    assert lap.semua_lulus


def test_nama_gerbang_dari_fungsi_cocok_dengan_daftar():
    g = gerbang_funding_ekor([], jadwal_dimuat=False)
    assert g.nama in NAMA_GERBANG
    assert g.lulus is False


def test_konsentrasi_mendahului_funding_ekor():
    """Urutan laporan mengikuti urutan penambahan, bukan abjad."""
    assert NAMA_GERBANG.index("konsentrasi") < NAMA_GERBANG.index("funding_ekor")
