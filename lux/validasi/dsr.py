"""Deflated Sharpe Ratio (DSR) dan Probabilistic Sharpe Ratio (PSR).

Dipra-registrasi di ADR-040 §4.4 butir 5.

Rujukan:
  Bailey, D. H. & Lopez de Prado, M. (2014). *The Deflated Sharpe Ratio:
  Correcting for Selection Bias, Backtest Overfitting, and Non-Normality.*
  Journal of Portfolio Management 40(5), 94-107.

Pagar rancangan yang menentukan bentuk modul ini:

1. ``scipy`` TIDAK tersedia di lingkungan runner (terverifikasi). Karena itu
   kuantil normal dibangun dari ``math.erf`` pustaka baku dengan pembagian dua,
   bukan dari ``scipy.stats.norm.ppf``.
2. Modul ini murni pustaka baku: tanpa numpy, tanpa pandas. Maka ia tidak dapat
   rusak karena beda versi numpy/pandas antar lingkungan.
3. Modul ini HANYA menghitung. Ia tidak membaca berkas, tidak menulis berkas,
   dan tidak menyentuh konfigurasi, gerbang, ambang beku, atau ``putusan``.

Kesepakatan satuan yang WAJIB dipatuhi pemanggil:

  Seluruh Sharpe di modul ini adalah Sharpe **per observasi** (bukan
  disetahunkan). Bila sampelnya laba bulanan, SR-nya bulanan. Mencampur Sharpe
  tahunan dengan ``n_observasi`` bulanan menghasilkan angka yang tampak masuk
  akal dan salah -- justru jenis kesalahan yang DSR seharusnya mencegah.
"""

from __future__ import annotations

import math
from typing import Sequence

# Konstanta Euler-Mascheroni, dipakai pada taksiran Sharpe maksimum harapan.
EULER_MASCHERONI = 0.5772156649015329

# Batas jepit bagi pembagian dua kuantil normal. Z(-40) dan Z(40) sudah jauh di
# luar jangkauan double, jadi jepitan ini tidak pernah menjadi pengikat nyata.
BATAS_JEPIT = 40.0
TOLERANSI_KUANTIL = 1e-13
MAKS_ITERASI = 300


def cdf_normal(x: float) -> float:
    """Fungsi distribusi kumulatif normal baku, dari ``math.erf``."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def kuantil_normal(p: float) -> float:
    """Kuantil normal baku (invers CDF) lewat pembagian dua.

    Sengaja lambat dan sengaja sederhana: ia dipanggil beberapa kali per
    adjudikasi, bukan di dalam lingkaran panas. Pembagian dua atas fungsi yang
    monoton naik tidak dapat menyimpang, berbeda dengan hampiran rasional yang
    galatnya sulit dibuktikan tanpa scipy sebagai pembanding.
    """
    if not (0.0 < p < 1.0):
        raise ValueError(f"p harus di dalam (0, 1), diterima {p!r}")
    bawah, atas = -BATAS_JEPIT, BATAS_JEPIT
    for _ in range(MAKS_ITERASI):
        tengah = 0.5 * (bawah + atas)
        if cdf_normal(tengah) < p:
            bawah = tengah
        else:
            atas = tengah
        if atas - bawah < TOLERANSI_KUANTIL:
            break
    return 0.5 * (bawah + atas)


def _momen_pusat(sampel: Sequence[float], orde: int) -> float:
    n = len(sampel)
    rerata = sum(sampel) / n
    return sum((x - rerata) ** orde for x in sampel) / n


def rerata(sampel: Sequence[float]) -> float:
    if not sampel:
        raise ValueError("sampel kosong")
    return sum(sampel) / len(sampel)


def simpangan_baku(sampel: Sequence[float], sampelan: bool = True) -> float:
    """Simpangan baku. ``sampelan=True`` memakai pembagi (n-1)."""
    n = len(sampel)
    if n < 2:
        raise ValueError("perlu sedikitnya 2 observasi")
    mu = sum(sampel) / n
    jumlah = sum((x - mu) ** 2 for x in sampel)
    pembagi = (n - 1) if sampelan else n
    return math.sqrt(jumlah / pembagi)


def kemencengan(sampel: Sequence[float]) -> float:
    """Kemencengan populasi (m3 / m2**1.5).

    Dipakai taksiran populasi, bukan taksiran tak-bias Fisher, karena rumus PSR
    Bailey-Lopez de Prado ditulis atas momen populasi.
    """
    if len(sampel) < 2:
        raise ValueError("perlu sedikitnya 2 observasi")
    m2 = _momen_pusat(sampel, 2)
    if m2 <= 0.0:
        raise ValueError("varians nol: kemencengan tak terdefinisi")
    return _momen_pusat(sampel, 3) / (m2 ** 1.5)


def kurtosis(sampel: Sequence[float]) -> float:
    """Kurtosis populasi **tidak** dikurangi 3 (normal menghasilkan ~3,0).

    Rumus PSR memakai gamma4 mentah. Menyerahkan kurtosis lebih (excess)
    ke fungsi ini menggeser hasil secara senyap; itu sebabnya konvensinya
    dinyatakan di sini dan dijaga oleh uji.
    """
    if len(sampel) < 2:
        raise ValueError("perlu sedikitnya 2 observasi")
    m2 = _momen_pusat(sampel, 2)
    if m2 <= 0.0:
        raise ValueError("varians nol: kurtosis tak terdefinisi")
    return _momen_pusat(sampel, 4) / (m2 ** 2)


def sharpe(sampel: Sequence[float], sampelan: bool = True) -> float:
    """Sharpe per observasi, tanpa penyetahunan dan tanpa suku bunga bebas risiko.

    Sampel diasumsikan sudah berupa laba lebih (excess). Pada papan LUX satuannya
    adalah R per perdagangan atau R per bulan, tergantung apa yang diserahkan.
    """
    sb = simpangan_baku(sampel, sampelan=sampelan)
    if sb <= 0.0:
        raise ValueError("simpangan baku nol: Sharpe tak terdefinisi")
    return rerata(sampel) / sb


def sharpe_ambang(n_percobaan: int, varians_sharpe_percobaan: float) -> float:
    """SR0: Sharpe maksimum yang diharapkan dari ``n_percobaan`` percobaan nol.

    Inilah inti deflasi. Bila kita menjalankan N percobaan yang seluruhnya tanpa
    edaran nyata, Sharpe terbaik di antaranya tetap positif semata karena
    pencarian. SR0 adalah nilai harapan Sharpe terbaik itu, dan kandidat harus
    mengalahkannya, bukan mengalahkan nol.

    Konvensi yang dinyatakan terang: ``n_percobaan == 1`` menghasilkan 0,0.
    Dengan satu percobaan tidak ada bias pemilihan, jadi ambangnya nol. Ini
    konvensi, bukan limit rumus -- rumusnya sendiri menyimpang di N = 1.
    """
    if n_percobaan < 1:
        raise ValueError("n_percobaan harus >= 1")
    if varians_sharpe_percobaan < 0.0:
        raise ValueError("varians tidak boleh negatif")
    if n_percobaan == 1:
        return 0.0
    n = float(n_percobaan)
    suku_satu = (1.0 - EULER_MASCHERONI) * kuantil_normal(1.0 - 1.0 / n)
    suku_dua = EULER_MASCHERONI * kuantil_normal(1.0 - 1.0 / (n * math.e))
    return math.sqrt(varians_sharpe_percobaan) * (suku_satu + suku_dua)


def psr(
    sharpe_teramati: float,
    sharpe_acuan: float,
    n_observasi: int,
    kemencengan_: float,
    kurtosis_: float,
) -> float:
    """Probabilistic Sharpe Ratio: peluang Sharpe sejati melampaui ``sharpe_acuan``.

    Penyebutnya memuat koreksi non-normalitas. Kemencengan negatif dan kurtosis
    tinggi -- persis bentuk sebaran R kita, dengan ekor -11,4736R -- membesarkan
    penyebut dan karena itu MENURUNKAN PSR. Itu memang maksudnya: Sharpe
    telanjang atas sebaran berekor tebal menyesatkan.
    """
    if n_observasi < 2:
        raise ValueError("perlu sedikitnya 2 observasi")
    penyebut_kuadrat = (
        1.0
        - kemencengan_ * sharpe_teramati
        + 0.25 * (kurtosis_ - 1.0) * sharpe_teramati ** 2
    )
    if penyebut_kuadrat <= 0.0:
        raise ValueError(
            "penyebut PSR tidak positif; momen yang diserahkan tidak konsisten "
            f"(kemencengan={kemencengan_!r}, kurtosis={kurtosis_!r}, "
            f"sharpe={sharpe_teramati!r})"
        )
    z = ((sharpe_teramati - sharpe_acuan) * math.sqrt(n_observasi - 1)) / math.sqrt(
        penyebut_kuadrat
    )
    return cdf_normal(z)


def dsr(
    sampel: Sequence[float],
    n_percobaan: int,
    varians_sharpe_percobaan: float,
) -> dict:
    """DSR = PSR dengan acuan SR0 dari ``n_percobaan``.

    Mengembalikan seluruh perantara supaya angkanya dapat diperiksa ulang orang
    lain dari berkas laporan, bukan hanya satu bilangan akhir.

    ``varians_sharpe_percobaan`` adalah varians Sharpe **lintas percobaan**, dan
    ia harus ditaksir dari papan percobaan yang benar-benar dijalankan. Ia BUKAN
    varians laba di dalam satu percobaan. Menukar keduanya adalah kesalahan yang
    membuat DSR tampak jinak.
    """
    n = len(sampel)
    if n < 2:
        raise ValueError("perlu sedikitnya 2 observasi")
    sr = sharpe(sampel)
    g3 = kemencengan(sampel)
    g4 = kurtosis(sampel)
    sr0 = sharpe_ambang(n_percobaan, varians_sharpe_percobaan)
    nilai = psr(sr, sr0, n, g3, g4)
    return {
        "n_observasi": n,
        "n_percobaan": n_percobaan,
        "sharpe_teramati": sr,
        "sharpe_ambang": sr0,
        "kemencengan": g3,
        "kurtosis": g4,
        "varians_sharpe_percobaan": varians_sharpe_percobaan,
        "dsr": nilai,
        "lulus": nilai > 0.95,
    }
