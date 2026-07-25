"""Pengujian metrik kisi funding.

Dua pelajaran dikunci di berkas ini, keduanya dibayar dengan putaran metrik
yang gagal:

1. Kisi funding berubah sepanjang umur sebuah simbol, jadi metrik apa pun yang
   memaksakan satu kisi untuk seluruh riwayat akan salah.
2. Waktu tidak boleh dibandingkan tanpa toleransi. Pergeseran beberapa
   milidetik bukan penagihan yang hilang.
"""

from __future__ import annotations

import pandas as pd
import pytest

from lux.funding_check import (
    TOLERANSI_MS,
    biaya_tahunan,
    celah_teramati,
    geseran,
    langkah_teramati,
    tidak_selaras,
)

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
    assert celah_teramati(waktu(JAM8, 30), JAM8) == (0, 0)


def test_peralihan_delapan_ke_empat_jam_bukan_celah():
    """Inti dari tiga putaran metrik yang gagal.

    Simbol yang hidup separuh umurnya di kisi delapan jam lalu pindah ke empat
    jam tidak kehilangan satu pun penagihan. Metrik yang memaksakan kisi empat
    jam ke seluruh riwayat akan melaporkan separuh datanya sebagai celah.
    """
    t = list(waktu(JAM8, 200))
    mulai = t[-1]
    t += [mulai + (i + 1) * 4 * JAM for i in range(400)]
    s = pd.Series(t)
    assert langkah_teramati(s) == 4 * JAM
    assert celah_teramati(s, langkah_teramati(s)) == (0, 0)


def test_kisi_delapan_jam_penuh_tidak_pernah_dianggap_celah():
    assert celah_teramati(waktu(JAM8, 50), 4 * JAM) == (0, 0)


def test_jarak_di_atas_delapan_jam_adalah_celah():
    t = pd.Series([AWAL, AWAL + 9 * JAM])
    peristiwa, _ = celah_teramati(t, JAM8)
    assert peristiwa == 1


def test_jitter_milidetik_bukan_celah():
    """Putaran metrik keempat gagal tepat di sini.

    Jarak delapan jam lebih beberapa milidetik lolos ambang "lebih dari delapan
    jam", lalu dibulatkan menjadi tepat satu penagihan hilang. Data sungguhan
    memuat 1.193.171 jarak semacam ini dengan pergeseran terbesar 47 ms, dan
    seluruhnya sempat terhitung sebagai kerusakan data.
    """
    t = pd.Series([AWAL, AWAL + JAM8 + 3, AWAL + 2 * JAM8 + 47])
    assert celah_teramati(t, JAM8) == (0, 0)
    jumlah, maks = geseran(t)
    assert jumlah == 2
    assert maks == 44


def test_pergeseran_melebihi_toleransi_tetap_celah():
    """Toleransi tidak boleh menjadi tempat sembunyi anomali sungguhan."""
    t = pd.Series([AWAL, AWAL + JAM8 + TOLERANSI_MS * 2])
    assert celah_teramati(t, JAM8)[0] == 1


def test_jitter_tidak_memecah_kisi_saat_mengukur_langkah():
    t = pd.Series([AWAL + i * JAM8 + i % 5 for i in range(40)])
    assert langkah_teramati(t) == JAM8


def test_penagihan_hilang_dihitung_dengan_kisi_simbol():
    """Jeda yang sama berarti lebih banyak penagihan hilang pada kisi rapat."""
    t = pd.Series([AWAL, AWAL + 504 * JAM])
    _, hilang_8 = celah_teramati(t, JAM8)
    _, hilang_4 = celah_teramati(t, 4 * JAM)
    assert hilang_8 == 62
    assert hilang_4 == 125


def test_jarak_lebih_rapat_bukan_celah():
    """Penyisipan bukan kehilangan; keduanya tidak boleh saling menutupi."""
    t = pd.Series([AWAL, AWAL + JAM, AWAL + JAM8])
    assert celah_teramati(t, JAM8) == (0, 0)


def test_dua_jarak_tidak_selaras_dihitung_dua():
    """Jarak 3 jam dan 5 jam sama-sama bukan kisi sah."""
    t = pd.Series([AWAL, AWAL + 3 * JAM, AWAL + 8 * JAM])
    assert tidak_selaras(t) == 2


def test_jarak_empat_jam_setelah_tiga_jam_tetap_sah():
    """Harapan pengujian yang pernah salah, dikunci supaya tidak lahir lagi.

    Deret AWAL, +3 jam, +7 jam menghasilkan jarak 3 jam lalu 4 jam. Hanya yang
    pertama tidak selaras; empat jam adalah kisi sah dan tidak boleh ikut
    dihitung hanya karena berdiri di sebelah jarak yang ganjil.
    """
    t = pd.Series([AWAL, AWAL + 3 * JAM, AWAL + 7 * JAM])
    assert tidak_selaras(t) == 1


def test_kisi_sah_tidak_dihitung_tidak_selaras():
    for langkah in (1, 2, 4, 8):
        assert tidak_selaras(waktu(langkah * JAM, 10)) == 0


def test_jeda_panjang_tidak_dihitung_sebagai_tidak_selaras():
    """Satu anomali hanya boleh muncul di satu kolom."""
    t = pd.Series([AWAL, AWAL + 500 * JAM])
    assert tidak_selaras(t) == 0
    assert celah_teramati(t, JAM8)[0] == 1


def test_urutan_acak_dirapikan_sebelum_dinilai():
    t = pd.Series([AWAL + 2 * JAM8, AWAL, AWAL + JAM8])
    assert langkah_teramati(t) == JAM8
    assert celah_teramati(t, JAM8) == (0, 0)


def test_biaya_tahunan_memakai_kisi_teramati_bukan_kolom():
    stat = {"jam_teramati": 8.0, "interval_jam": [4], "rate_rerata": 0.0001}
    assert biaya_tahunan(stat) == pytest.approx(0.1095, abs=1e-4)


def test_biaya_tahunan_jatuh_ke_kolom_bila_tak_teramati():
    stat = {"jam_teramati": None, "interval_jam": [8], "rate_rerata": 0.0001}
    assert biaya_tahunan(stat) == pytest.approx(0.1095, abs=1e-4)


def test_biaya_tahunan_tanpa_informasi_apa_pun_tidak_menebak():
    assert (
        biaya_tahunan({"jam_teramati": None, "interval_jam": [], "rate_rerata": 0.1})
        is None
    )
