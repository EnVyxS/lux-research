"""Uji bagi lux/validasi/pbo.py.

Seperti test_dsr.py: sengaja TIDAK mengimpor pytest, supaya berkas yang sama
dapat dijalankan oleh pytest di CI dan oleh penjalan pustaka-baku di sandbox.
Tanpa fixture, tanpa parametrize, tanpa pytest.raises.

Dua uji inti di bawah adalah yang sebenarnya penting, dan keduanya DETERMINISTIK
-- tanpa bilangan acak, sehingga hasilnya tidak dapat berubah antar putaran:

  test_pbo_nol_ketika_juara_memang_juara   -> PBO harus 0,0
  test_pbo_satu_ketika_pemilihan_mengejar_derau -> PBO harus 1,0

Bila kedua ujung itu benar, arah tanda PBO terbukti; sisanya memeriksa pagar.
"""

import math

from lux.validasi.pbo import (
    AMBANG_PBO,
    KINERJA_DEGENERAT,
    MAKS_KOMBINASI,
    bagi_subsampel,
    kinerja,
    logit,
    pbo,
    peringkat_tengah,
    periksa_matriks,
)


def _galat(f, *a, **k):
    try:
        f(*a, **k)
    except ValueError:
        return True
    return False


def _derau(c, t):
    """Derau kecil deterministik, berbeda per kolom supaya tidak ada seri palsu."""
    return (((c + 1) * (t + 3)) % 7 - 3) * 0.0001


# --- periksa_matriks ----------------------------------------------------


def test_periksa_matriks_bentuk():
    n_obs, n_kon = periksa_matriks([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]])
    assert n_obs == 3
    assert n_kon == 2


def test_periksa_matriks_menolak_kosong():
    assert _galat(periksa_matriks, [])


def test_periksa_matriks_menolak_satu_konfigurasi():
    # PBO adalah pernyataan tentang PEMILIHAN; tanpa pilihan ia tak bermakna.
    assert _galat(periksa_matriks, [[0.1], [0.2]])


def test_periksa_matriks_menolak_baris_tak_sama_panjang():
    assert _galat(periksa_matriks, [[0.1, 0.2], [0.3]])


# --- bagi_subsampel -----------------------------------------------------


def test_bagi_subsampel_blok_berurutan():
    bagian = bagi_subsampel(8, 4)
    assert bagian == [[0, 1], [2, 3], [4, 5], [6, 7]]


def test_bagi_subsampel_menolak_ganjil():
    assert _galat(bagi_subsampel, 9, 3)


def test_bagi_subsampel_menolak_terlalu_sedikit():
    assert _galat(bagi_subsampel, 8, 1)


def test_bagi_subsampel_menolak_pembagian_bersisa():
    # Sisa periode tidak boleh terbuang senyap.
    assert _galat(bagi_subsampel, 10, 4)


def test_bagi_subsampel_menolak_blok_satu_periode():
    # Sharpe tak terdefinisi atas satu observasi.
    assert _galat(bagi_subsampel, 8, 8)


# --- kinerja ------------------------------------------------------------


def test_kinerja_nilai_diketahui():
    matriks = [[1.0, 0.0], [2.0, 0.0], [3.0, 0.0], [4.0, 0.0]]
    diharap = 2.5 / math.sqrt(5.0 / 3.0)
    assert abs(kinerja(matriks, [0, 1, 2, 3], 0) - diharap) < 1e-14


def test_kinerja_kolom_datar_sentinel_bukan_galat():
    matriks = [[1.0, 0.0], [2.0, 0.0], [3.0, 0.0], [4.0, 0.0]]
    assert kinerja(matriks, [0, 1, 2, 3], 1) == KINERJA_DEGENERAT


def test_kinerja_hanya_memakai_baris_yang_diminta():
    matriks = [[1.0, 0.0], [2.0, 0.0], [100.0, 0.0], [200.0, 0.0]]
    a = kinerja(matriks, [0, 1], 0)
    b = kinerja(matriks, [2, 3], 0)
    assert abs(a - 1.5 / math.sqrt(0.5)) < 1e-12
    assert abs(b - 150.0 / math.sqrt(5000.0)) < 1e-12


def test_kinerja_menolak_satu_baris():
    assert _galat(kinerja, [[1.0, 0.0], [2.0, 0.0]], [0], 0)


# --- peringkat_tengah ---------------------------------------------------


def test_peringkat_terbaik_dan_terburuk():
    nilai = [1.0, 2.0, 3.0]
    assert peringkat_tengah(nilai, 2) == 3.0
    assert peringkat_tengah(nilai, 0) == 1.0


def test_peringkat_seri_dibagi_rata():
    nilai = [1.0, 1.0, 3.0]
    assert peringkat_tengah(nilai, 0) == 1.5
    assert peringkat_tengah(nilai, 1) == 1.5


def test_peringkat_semua_seri():
    nilai = [2.0, 2.0, 2.0, 2.0]
    assert peringkat_tengah(nilai, 0) == 2.5


# --- logit --------------------------------------------------------------


def test_logit_setengah_nol():
    assert abs(logit(0.5)) < 1e-15


def test_logit_monoton_dan_antisimetris():
    assert logit(0.75) > 0.0
    assert logit(0.25) < 0.0
    assert abs(logit(0.75) + logit(0.25)) < 1e-14


def test_logit_menolak_domain_di_luar():
    assert _galat(logit, 0.0)
    assert _galat(logit, 1.0)
    assert _galat(logit, 1.5)


# --- pbo: dua ujung deterministik ---------------------------------------


def _matriks_juara_sejati():
    """Kolom 0 unggul di SETIAP periode; empat kolom lain hanya berderau."""
    matriks = []
    for t in range(32):
        baris = [0.10 + 0.01 * ((t % 3) - 1)]
        for c in range(1, 5):
            baris.append(_derau(c, t))
        matriks.append(baris)
    return matriks


def test_pbo_nol_ketika_juara_memang_juara():
    hasil = pbo(_matriks_juara_sejati(), s_bagian=8)
    assert hasil["pbo"] == 0.0, hasil
    assert hasil["cacah_logit_negatif"] == 0
    assert hasil["logit_median"] > 0.0
    assert hasil["lulus"] is True


def _matriks_derau_terpilih():
    """Delapan konfigurasi, delapan blok: konfigurasi c hanya bagus di blok c.

    Inilah bentuk baku overfitting. Pada setiap belahan, juara latih selalu
    konfigurasi yang lonjakannya berada DI DALAM latih, dan konfigurasi yang
    lonjakannya berada di uji selalu mengalahkannya di luar sampel. Peringkat
    luar sampel juara latih karena itu selalu di separuh bawah, dan PBO harus
    tepat 1,0.
    """
    matriks = []
    for t in range(32):
        blok = t // 4
        baris = []
        for c in range(8):
            baris.append(0.05 + _derau(c, t) if c == blok else _derau(c, t))
        matriks.append(baris)
    return matriks


def test_pbo_satu_ketika_pemilihan_mengejar_derau():
    hasil = pbo(_matriks_derau_terpilih(), s_bagian=8)
    assert hasil["pbo"] == 1.0, hasil
    assert hasil["cacah_logit_negatif"] == hasil["cacah_dinilai"]
    assert hasil["logit_median"] < 0.0
    assert hasil["lulus"] is False


def test_pbo_kemerosotan_negatif_pada_kasus_overfit():
    # Juara latih harus tampil LEBIH BURUK di luar sampel; itu tanda merosot.
    hasil = pbo(_matriks_derau_terpilih(), s_bagian=8)
    assert hasil["kemerosotan_luar_sampel"] < 0.0, hasil


def test_pbo_menjelajahi_seluruh_kombinasi_simetris():
    hasil = pbo(_matriks_juara_sejati(), s_bagian=8)
    assert hasil["cacah_kombinasi"] == math.comb(8, 4) == 70
    assert hasil["cacah_dinilai"] == 70
    assert hasil["cacah_semua_degenerat"] == 0


def test_pbo_selalu_pecahan():
    for s in (4, 8):
        hasil = pbo(_matriks_derau_terpilih(), s_bagian=s)
        assert 0.0 <= hasil["pbo"] <= 1.0
        assert 0.0 < hasil["omega_median"] < 1.0


def test_pbo_mengembalikan_seluruh_perantara():
    hasil = pbo(_matriks_juara_sejati(), s_bagian=8)
    for kunci in (
        "n_observasi",
        "n_konfigurasi",
        "s_bagian",
        "cacah_kombinasi",
        "cacah_dinilai",
        "cacah_semua_degenerat",
        "pbo",
        "cacah_logit_negatif",
        "logit_median",
        "omega_median",
        "rerata_sharpe_latih_terpilih",
        "rerata_sharpe_uji_terpilih",
        "kemerosotan_luar_sampel",
        "ambang",
        "lulus",
    ):
        assert kunci in hasil, kunci
    assert hasil["n_observasi"] == 32
    assert hasil["n_konfigurasi"] == 5
    assert hasil["ambang"] == AMBANG_PBO


def test_ambang_pbo_terpatok_setengah():
    # ADR-040 4.4: kandidat harus PBO < 0,50.
    assert AMBANG_PBO == 0.50


def test_pbo_menolak_kombinasi_terlalu_banyak():
    # C(22,11) = 705.432, jauh di atas MAKS_KOMBINASI.
    matriks = [[_derau(0, t), _derau(1, t)] for t in range(44)]
    assert math.comb(22, 11) > MAKS_KOMBINASI
    assert _galat(pbo, matriks, 22)


def test_pbo_menolak_papan_datar_seluruhnya():
    matriks = [[0.0, 1.0] for _ in range(8)]
    assert _galat(pbo, matriks, 4)


def test_pbo_menolak_s_bagian_tak_sah():
    matriks = _matriks_juara_sejati()
    assert _galat(pbo, matriks, 7)
    assert _galat(pbo, matriks, 5)
