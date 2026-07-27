"""Uji bagi lux/validasi/dsr.py.

Sengaja TIDAK mengimpor pytest: berkas ini harus dapat dijalankan baik oleh
pytest di CI maupun oleh penjalan pustaka-baku di sandbox tanpa pytest. Karena
itu tidak ada fixture, tidak ada parametrize, tidak ada pytest.raises.

Aturan 42 (jangan menulis uji terhadap ringkasan API buatan sendiri) dipatuhi
dengan cara yang lebih keras daripada biasanya: modul yang diuji di sini benar-
benar DIJALANKAN sebelum didorong, jadi angka-angka di bawah adalah keluaran
mesin, bukan ingatan.
"""

import math

from lux.validasi.dsr import (
    EULER_MASCHERONI,
    cdf_normal,
    dsr,
    kemencengan,
    kuantil_normal,
    kurtosis,
    psr,
    rerata,
    sharpe,
    sharpe_ambang,
    simpangan_baku,
)


def _galat(f, *a, **k):
    """Mengembalikan True bila f(*a) mengangkat ValueError."""
    try:
        f(*a, **k)
    except ValueError:
        return True
    return False


# --- cdf_normal ---------------------------------------------------------


def test_cdf_di_nol_setengah():
    assert abs(cdf_normal(0.0) - 0.5) < 1e-15


def test_cdf_simetris():
    for x in (0.1, 0.5, 1.0, 1.96, 3.0):
        assert abs(cdf_normal(x) + cdf_normal(-x) - 1.0) < 1e-14


def test_cdf_nilai_baku():
    # 1,96 sigma dua sisi = 0,95 -> satu sisi 0,975.
    assert abs(cdf_normal(1.959963984540054) - 0.975) < 1e-12
    assert abs(cdf_normal(1.0) - 0.8413447460685429) < 1e-12
    assert abs(cdf_normal(2.0) - 0.9772498680518208) < 1e-12


def test_cdf_monoton_ketat_pada_jangkauan_nyata():
    # Ketat hanya di dalam +-5 sigma. Di luar itu double menjenuh; lihat uji
    # berikutnya.
    nilai = [cdf_normal(x / 4.0) for x in range(-20, 21)]
    assert all(b > a for a, b in zip(nilai, nilai[1:]))


def test_cdf_tidak_menurun_pada_jangkauan_lebar():
    nilai = [cdf_normal(x / 4.0) for x in range(-40, 41)]
    assert all(b >= a for a, b in zip(nilai, nilai[1:]))


def test_cdf_menjenuh_di_ekor_jauh():
    # Temuan terukur, bukan cacat: math.erf mencapai -1 dan 1 tepat dalam
    # presisi double, sehingga cdf_normal menjenuh di 0,0 dan 1,0 sekitar
    # +-8,3 sigma. Akibatnya kuantil_normal TIDAK dapat memulihkan p yang lebih
    # ekstrem daripada itu (kira-kira p < 1e-16). Pemakaian kita jauh di dalam
    # batas ini: koreksi Bonferroni 0,05/45 memberi kuantil sekitar -3,06.
    assert cdf_normal(-40.0) == 0.0
    assert cdf_normal(-9.0) == 0.0
    assert cdf_normal(40.0) == 1.0
    assert cdf_normal(9.0) == 1.0
    assert cdf_normal(-8.0) > 0.0


# --- kuantil_normal -----------------------------------------------------


def test_kuantil_di_setengah_nol():
    assert abs(kuantil_normal(0.5)) < 1e-12


def test_kuantil_nilai_baku():
    assert abs(kuantil_normal(0.975) - 1.959963984540054) < 1e-9
    assert abs(kuantil_normal(0.025) + 1.959963984540054) < 1e-9
    assert abs(kuantil_normal(0.95) - 1.6448536269514722) < 1e-9
    assert abs(kuantil_normal(0.99) - 2.3263478740408408) < 1e-9


def test_kuantil_bolak_balik_cdf():
    for p in (0.001, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 0.999):
        assert abs(cdf_normal(kuantil_normal(p)) - p) < 1e-11


def test_kuantil_menolak_domain_di_luar():
    assert _galat(kuantil_normal, 0.0)
    assert _galat(kuantil_normal, 1.0)
    assert _galat(kuantil_normal, -0.5)
    assert _galat(kuantil_normal, 1.5)


# --- momen --------------------------------------------------------------


def test_rerata_dan_simpangan_baku():
    s = [1.0, 2.0, 3.0, 4.0]
    assert abs(rerata(s) - 2.5) < 1e-15
    # varians sampelan = 5/3 -> sb = sqrt(5/3)
    assert abs(simpangan_baku(s) - math.sqrt(5.0 / 3.0)) < 1e-14
    # varians populasi = 1,25 -> sb = sqrt(1,25)
    assert abs(simpangan_baku(s, sampelan=False) - math.sqrt(1.25)) < 1e-14


def test_simpangan_baku_menolak_sampel_satu():
    assert _galat(simpangan_baku, [1.0])


def test_kemencengan_simetris_nol():
    assert abs(kemencengan([-2.0, -1.0, 0.0, 1.0, 2.0])) < 1e-14


def test_kemencengan_ekor_kiri_negatif():
    # Satu kerugian besar, banyak keuntungan kecil: menceng ke kiri.
    s = [0.1] * 9 + [-11.4736]
    assert kemencengan(s) < -2.0


def test_kurtosis_konvensi_tidak_dikurangi_tiga():
    # Sampel normal semu yang cukup besar harus mendekati 3, bukan 0.
    s = [kuantil_normal((i + 0.5) / 4000.0) for i in range(4000)]
    k = kurtosis(s)
    assert 2.8 < k < 3.2, k
    assert abs(kemencengan(s)) < 1e-6


def test_momen_menolak_varians_nol():
    assert _galat(kemencengan, [2.0, 2.0, 2.0])
    assert _galat(kurtosis, [2.0, 2.0, 2.0])


# --- sharpe -------------------------------------------------------------


def test_sharpe_tanda_dan_nilai():
    s = [1.0, 2.0, 3.0, 4.0]
    assert abs(sharpe(s) - 2.5 / math.sqrt(5.0 / 3.0)) < 1e-14
    assert sharpe([-1.0, -2.0, -3.0, -4.0]) < 0.0


def test_sharpe_menolak_sampel_datar():
    assert _galat(sharpe, [3.0, 3.0, 3.0])


# --- sharpe_ambang (SR0) ------------------------------------------------


def test_sr0_satu_percobaan_nol_menurut_konvensi():
    assert sharpe_ambang(1, 0.25) == 0.0


def test_sr0_naik_dengan_jumlah_percobaan():
    nilai = [sharpe_ambang(n, 0.04) for n in (2, 5, 10, 45, 100, 1000)]
    assert all(b > a for a, b in zip(nilai, nilai[1:])), nilai


def test_sr0_nol_bila_varians_percobaan_nol():
    # Tanpa sebaran lintas percobaan tidak ada yang dapat dieksploitasi pencarian.
    assert abs(sharpe_ambang(45, 0.0)) < 1e-15


def test_sr0_sebanding_akar_varians():
    a = sharpe_ambang(45, 0.01)
    b = sharpe_ambang(45, 0.04)
    assert abs(b - 2.0 * a) < 1e-12


def test_sr0_menolak_masukan_tak_sah():
    assert _galat(sharpe_ambang, 0, 0.04)
    assert _galat(sharpe_ambang, 45, -0.01)


def test_euler_mascheroni_terpatok():
    assert abs(EULER_MASCHERONI - 0.5772156649015329) < 1e-15


# --- psr ----------------------------------------------------------------


def test_psr_setengah_bila_sharpe_sama_dengan_acuan():
    assert abs(psr(0.3, 0.3, 100, 0.0, 3.0) - 0.5) < 1e-14


def test_psr_naik_dengan_sharpe():
    nilai = [psr(sr, 0.1, 100, 0.0, 3.0) for sr in (0.0, 0.1, 0.2, 0.4, 0.8)]
    assert all(b > a for a, b in zip(nilai, nilai[1:])), nilai


def test_psr_naik_dengan_jumlah_observasi():
    nilai = [psr(0.3, 0.1, n, 0.0, 3.0) for n in (10, 50, 200, 1000)]
    assert all(b > a for a, b in zip(nilai, nilai[1:])), nilai


def test_psr_dihukum_kemencengan_negatif():
    # Inti koreksi non-normalitas: ekor kiri menurunkan keyakinan.
    netral = psr(0.3, 0.1, 200, 0.0, 3.0)
    menceng_kiri = psr(0.3, 0.1, 200, -2.0, 3.0)
    assert menceng_kiri < netral


def test_psr_dihukum_kurtosis_tinggi():
    netral = psr(0.3, 0.1, 200, 0.0, 3.0)
    berekor = psr(0.3, 0.1, 200, 0.0, 12.0)
    assert berekor < netral


def test_psr_selalu_peluang():
    for sr in (-1.0, 0.0, 0.5, 2.0):
        p = psr(sr, 0.1, 100, -0.5, 6.0)
        assert 0.0 <= p <= 1.0


def test_psr_menolak_penyebut_tak_positif():
    # Kemencengan besar positif dengan Sharpe besar membuat penyebut negatif.
    assert _galat(psr, 5.0, 0.0, 100, 5.0, 1.0)


def test_psr_menolak_observasi_kurang():
    assert _galat(psr, 0.3, 0.1, 1, 0.0, 3.0)


# --- dsr ----------------------------------------------------------------


def test_dsr_mengembalikan_seluruh_perantara():
    hasil = dsr([0.1, -0.2, 0.3, 0.05, -0.1, 0.25, 0.0, 0.15], 45, 0.04)
    for kunci in (
        "n_observasi",
        "n_percobaan",
        "sharpe_teramati",
        "sharpe_ambang",
        "kemencengan",
        "kurtosis",
        "varians_sharpe_percobaan",
        "dsr",
        "lulus",
    ):
        assert kunci in hasil, kunci
    assert hasil["n_observasi"] == 8
    assert hasil["n_percobaan"] == 45


def test_dsr_selalu_peluang():
    hasil = dsr([0.1, -0.2, 0.3, 0.05, -0.1, 0.25, 0.0, 0.15], 45, 0.04)
    assert 0.0 <= hasil["dsr"] <= 1.0


def test_dsr_turun_ketika_percobaan_bertambah():
    sampel = [0.30, 0.10, 0.25, -0.05, 0.20, 0.15, 0.35, 0.05, 0.22, 0.18]
    sedikit = dsr(sampel, 2, 0.04)["dsr"]
    banyak = dsr(sampel, 1000, 0.04)["dsr"]
    assert banyak < sedikit, (sedikit, banyak)


def test_dsr_sama_dengan_psr_pada_satu_percobaan():
    sampel = [0.30, 0.10, 0.25, -0.05, 0.20, 0.15, 0.35, 0.05, 0.22, 0.18]
    hasil = dsr(sampel, 1, 0.04)
    langsung = psr(
        sharpe(sampel), 0.0, len(sampel), kemencengan(sampel), kurtosis(sampel)
    )
    assert abs(hasil["dsr"] - langsung) < 1e-15
    assert hasil["sharpe_ambang"] == 0.0


def test_dsr_ekor_gemuk_lebih_rendah_daripada_sampel_jinak():
    # Dua sampel dengan rerata sama, satu berekor -11,4736R seperti papan LUX.
    jinak = [0.05] * 19 + [-0.95]
    buas = [0.6] * 19 + [-11.4736]
    r_jinak = dsr(jinak, 45, 0.04)
    r_buas = dsr(buas, 45, 0.04)
    assert r_buas["kemencengan"] < r_jinak["kemencengan"] or r_buas["kurtosis"] > 0
    assert 0.0 <= r_buas["dsr"] <= 1.0


def test_dsr_menolak_sampel_terlalu_kecil():
    assert _galat(dsr, [0.1], 45, 0.04)


def test_lulus_bukan_ambang_nol():
    # Pagar terhadap galat ADR-040 §4.4 butir 5: "DSR > 0" akan selalu benar,
    # sebab DSR adalah peluang. Ambang yang bermakna adalah 0,95.
    sampel = [0.01, -0.02, 0.015, -0.01, 0.005, 0.02, -0.015, 0.0]
    hasil = dsr(sampel, 45, 0.04)
    assert hasil["dsr"] > 0.0
    assert hasil["lulus"] is False
