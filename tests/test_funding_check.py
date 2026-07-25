"""Pengujian metrik kisi teramati.

Pelajaran yang dikunci di sini: metrik tidak boleh mempercayai kolom metadata
sebagai kebenaran tentang bentuk datanya sendiri. Dua putaran metrik funding
gagal justru karena mempercayainya.
"""

from __future__ import annotations

import pandas as pd
import pytest

from lux.funding_check import biaya_tahunan, celah_teramati, langkah_teramati

JAM = 3_600_000
JAM8 = 8 * JAM
AWAL = 1_600_000_000_000 - (1_600_000_000_000 % JAM8)


def waktu(langkah: int, n: int, mulai: int = AWAL) -> pd.Series:
    return pd.Series([mulai + i * langkah for i in range(n)])


def test_langkah_teramati_mengenali_kisi_delapan_jam():
    assert langkah_teramati(waktu(JAM8, 20)) == JAM8


def test_langkah_teramati_mengenali_kisi_empat_jam():
    assert langkah_teramati(waktu(4 * JAM, 20)) == 4 * JAM


def test_modus_bertahan_terhadap_satu_penghentian_panjang():
    """Rerata akan tertipu oleh satu jeda panjang; modus tidak."""
    t = list(waktu(JAM8, 20))
    t.append(t[-1] + 200 * JAM8)
    s = pd.Series(t)
    assert langkah_teramati(s) == JAM8
    assert s.diff().dropna().mean() > JAM8 * 5


def test_langkah_teramati_pada_seri_satu_baris_tidak_menebak():
    assert langkah_teramati(pd.Series([AWAL])) is None


def test_deret_rapi_tidak_punya_celah():
    t = waktu(JAM8, 30)
    assert celah_teramati(t, JAM8) == (0, 0)


def test_satu_periode_hilang_dihitung_satu():
    t = pd.Series([AWAL, AWAL + JAM8, AWAL + 3 * JAM8])
    peristiwa, hilang = celah_teramati(t, JAM8)
    assert peristiwa == 1
    assert hilang == 1


def test_jeda_panjang_dihitung_sebagai_banyak_periode():
    t = pd.Series([AWAL, AWAL + 10 * JAM8])
    peristiwa, hilang = celah_teramati(t, JAM8)
    assert peristiwa == 1
    assert hilang == 9


def test_jarak_lebih_rapat_bukan_celah():
    """Penyisipan bukan kehilangan; keduanya tidak boleh saling menutupi."""
    t = pd.Series([AWAL, AWAL + JAM, AWAL + JAM8])
    peristiwa, hilang = celah_teramati(t, JAM8)
    assert peristiwa == 0
    assert hilang == 0


def test_tanpa_langkah_tidak_menghitung_celah():
    assert celah_teramati(waktu(JAM8, 5), None) == (0, 0)


def test_urutan_acak_dirapikan_sebelum_dinilai():
    t = pd.Series([AWAL + 2 * JAM8, AWAL, AWAL + JAM8])
    assert langkah_teramati(t) == JAM8
    assert celah_teramati(t, JAM8) == (0, 0)


def test_biaya_tahunan_memakai_kisi_teramati_bukan_kolom():
    """Bila kolom dan kenyataan berbeda, kenyataan yang menentukan biaya."""
    stat = {"jam_teramati": 8.0, "interval_jam": [4], "rate_rerata": 0.0001}
    assert biaya_tahunan(stat) == pytest.approx(0.1095, abs=1e-4)


def test_biaya_tahunan_jatuh_ke_kolom_bila_tak_teramati():
    stat = {"jam_teramati": None, "interval_jam": [8], "rate_rerata": 0.0001}
    assert biaya_tahunan(stat) == pytest.approx(0.1095, abs=1e-4)


def test_biaya_tahunan_tanpa_informasi_apa_pun_tidak_menebak():
    assert biaya_tahunan({"jam_teramati": None, "interval_jam": [], "rate_rerata": 0.1}) is None
