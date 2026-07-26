"""Pengujian modul daun kerangka waktu (ADR-019 langkah 1 dan 2).

Yang diuji bukan sekadar dua angka, melainkan **sifat** yang membuat kelas cacat
"ambang buta interval" tidak dapat lahir lagi: setiap interval yang dikenal harus
menghasilkan satu hari penuh, dan interval yang tidak dikenal harus berbunyi.
"""

from __future__ import annotations

import pytest

from lux.kerangka import (
    INTERVAL_JAM,
    JAM_SEHARI,
    bar_per_hari,
    interval_dikenal,
    jam_interval,
)


def test_bar_per_hari_1h_adalah_24():
    assert bar_per_hari("1h") == 24


def test_bar_per_hari_4h_adalah_6():
    # Inti seluruh ADR-018 dan ADR-019: 24 bar pada 4h adalah empat hari,
    # bukan satu. Angka yang benar adalah enam.
    assert bar_per_hari("4h") == 6


def test_setiap_interval_dikenal_menyusun_satu_hari_penuh():
    # Sifat, bukan daftar nilai: berapa pun interval yang ditambahkan kemudian,
    # hasil kali bar dengan panjang jamnya wajib tepat sehari.
    for interval, jam in INTERVAL_JAM.items():
        assert bar_per_hari(interval) * jam == JAM_SEHARI


def test_interval_tak_dikenal_gagal_keras():
    # Bawaan yang dikembalikan diam-diam adalah cara cacat keempat lahir.
    with pytest.raises(SystemExit):
        bar_per_hari("15m")
    with pytest.raises(SystemExit):
        jam_interval("1d")


def test_pesan_galat_menyebut_interval_diminta_dan_yang_dikenal():
    with pytest.raises(SystemExit) as e:
        bar_per_hari("5m")
    pesan = str(e.value)
    assert "5m" in pesan
    for interval in interval_dikenal():
        assert interval in pesan


def test_interval_dikenal_terurut_dan_cocok_dengan_peta():
    assert interval_dikenal() == sorted(INTERVAL_JAM)
    assert interval_dikenal() == ["1h", "4h"]


def test_setiap_panjang_jam_positif_dan_membagi_sehari():
    for interval, jam in INTERVAL_JAM.items():
        assert jam > 0, interval
        assert JAM_SEHARI % jam == 0, interval


def test_hasil_selalu_bilangan_bulat_positif():
    # Pembagian bulat dipakai dengan sengaja; hasil float akan menyusup ke
    # pengirisan indeks dan gagal di tempat yang jauh dari sebabnya.
    for interval in interval_dikenal():
        n = bar_per_hari(interval)
        assert isinstance(n, int)
        assert n > 0


def test_ambang_potong_ekor_tetap_setara_satu_hari_kerangka():
    """Tripwire ADR-019 langkah 2: dua pihak, satu aritmetika.

    Kesetaraan ini tampak jelas hari ini, dan justru karena tampak jelas ia wajib
    diikat. Bila kemudian salah satu pihak disunting sendirian, yang berbunyi
    harus pengujian ini — bukan laporan hasil enam bulan kemudian.
    """
    from lux.potong_ekor import MIN_PANJANG, min_panjang_untuk

    for interval in interval_dikenal():
        assert min_panjang_untuk(interval) == bar_per_hari(interval), interval
    # Jalur 1h wajib bit-identik dengan sebelum ADR-019.
    assert MIN_PANJANG == bar_per_hari("1h") == 24
    # Pembungkus tetap gagal keras, dan pesannya tetap menyebut ADR.
    with pytest.raises(SystemExit) as e:
        min_panjang_untuk("15m")
    assert "ADR" in str(e.value)
