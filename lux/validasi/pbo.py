"""Probability of Backtest Overfitting (PBO) lewat CSCV.

Dipra-registrasi di ADR-040 §4.4 butir 4.

Rujukan:
  Bailey, D. H., Borwein, J. M., Lopez de Prado, M. & Zhu, Q. J. (2015).
  *The Probability of Backtest Overfitting.* Journal of Computational Finance.
  CSCV = Combinatorially Symmetric Cross-Validation.

Gagasannya, sesingkat mungkin. Kita mencoba banyak konfigurasi dan memilih yang
terbaik. Pertanyaannya bukan "seberapa bagus yang terbaik", melainkan: bila
kita memilih yang terbaik pada separuh data, seberapa sering ia jatuh ke
separuh bawah pada separuh data yang lain? Bila sering, maka pemilihan kita
mengejar derau. PBO adalah pecahan itu.

Pagar rancangan:

1. Murni pustaka baku. Tanpa numpy, tanpa pandas, tanpa scipy. Matriks laba
   diterima sebagai senarai-dari-senarai biasa, bukan DataFrame, supaya modul
   ini dapat dijalankan dan diverifikasi di lingkungan tanpa pandas/pyarrow.
2. HANYA menghitung. Tidak membaca berkas, tidak menulis berkas, dan tidak
   menyentuh konfigurasi, gerbang, ambang beku, atau ``putusan``.
3. CSCV simetris: setiap belahan latih berpasangan dengan komplemennya, dan
   kedua arah dihitung. Itulah arti "symmetric" pada namanya; melewatkannya
   membuat taksiran PBO menceng.

Kesepakatan bentuk data yang WAJIB dipatuhi pemanggil:

  ``matriks[t][n]`` adalah laba pada periode ``t`` bagi konfigurasi ``n``.
  Jadi baris = waktu, kolom = konfigurasi. Menyerahkan transposenya akan
  menghasilkan angka yang tampak masuk akal dan tidak berarti apa-apa; karena
  itu bentuknya diperiksa dan ketidakcocokan panjang baris diangkat sebagai
  galat, bukan dibiarkan.

  Satuan laba harus SATU periode yang sama untuk seluruh kolom (misalnya R per
  bulan). PBO tidak peduli skalanya, tetapi ia peduli bahwa baris ke-t pada
  semua kolom adalah periode yang sama.
"""

from __future__ import annotations

import math
from itertools import combinations
from typing import List, Sequence

# Ambang pra-registrasi ADR-040 §4.4: kandidat harus PBO < 0,50.
AMBANG_PBO = 0.50

# Pagar biaya. C(16,8) = 12.870 sudah di atas cukup; C(20,10) = 184.756 akan
# membuat satu adjudikasi memakan menit tanpa menambah ketelitian yang berarti.
# Bila terlampaui, modul MENOLAK alih-alih berjalan lama secara senyap.
MAKS_KOMBINASI = 20000

# Sentinel bagi kolom bervarians nol. Kolom datar tidak punya Sharpe; ia tidak
# boleh terpilih sebagai juara latih, dan ia harus menempati peringkat terbawah
# pada uji. -inf melakukan keduanya tanpa cabang khusus.
KINERJA_DEGENERAT = float("-inf")


def periksa_matriks(matriks: Sequence[Sequence[float]]) -> tuple:
    """Memeriksa bentuk matriks laba dan mengembalikan (n_observasi, n_konfigurasi)."""
    n_observasi = len(matriks)
    if n_observasi == 0:
        raise ValueError("matriks kosong")
    n_konfigurasi = len(matriks[0])
    if n_konfigurasi < 2:
        raise ValueError(
            "PBO tak bermakna dengan kurang dari 2 konfigurasi, "
            f"diterima {n_konfigurasi}"
        )
    for t, baris in enumerate(matriks):
        if len(baris) != n_konfigurasi:
            raise ValueError(
                f"baris {t} panjangnya {len(baris)}, seharusnya {n_konfigurasi}; "
                "matriks[t][n] = laba periode t bagi konfigurasi n"
            )
    return n_observasi, n_konfigurasi


def bagi_subsampel(n_observasi: int, s_bagian: int) -> List[List[int]]:
    """Memecah indeks periode menjadi ``s_bagian`` blok berurutan sama panjang.

    Blok BERURUTAN, bukan acak: CSCV dirancang atas potongan waktu yang utuh,
    dan mengacak baris akan merusak kebergantungan serial yang justru menjadi
    pokok persoalan.

    ``s_bagian`` harus genap (CSCV membelah menjadi dua bagian sama besar) dan
    harus membagi ``n_observasi`` habis. Bila tidak habis, sisa periode akan
    terbuang secara senyap -- maka di sini ia diangkat sebagai galat.
    """
    if s_bagian < 2:
        raise ValueError("s_bagian harus >= 2")
    if s_bagian % 2 != 0:
        raise ValueError(f"s_bagian harus genap, diterima {s_bagian}")
    if n_observasi % s_bagian != 0:
        raise ValueError(
            f"{n_observasi} observasi tidak terbagi habis oleh {s_bagian} bagian; "
            "potong atau pilih s_bagian lain, jangan biarkan sisa terbuang"
        )
    panjang = n_observasi // s_bagian
    if panjang < 2:
        raise ValueError(
            "tiap bagian perlu >= 2 periode supaya Sharpe terdefinisi, "
            f"diterima {panjang}"
        )
    return [list(range(i * panjang, (i + 1) * panjang)) for i in range(s_bagian)]


def kinerja(matriks: Sequence[Sequence[float]], indeks: Sequence[int], kolom: int) -> float:
    """Sharpe per observasi kolom ``kolom`` atas baris ``indeks``.

    Sengaja dihitung di sini alih-alih memanggil ``dsr.sharpe`` supaya kolom
    datar mengembalikan sentinel dan bukan mengangkat galat: pada papan nyata
    beberapa konfigurasi memang tidak berdagang sama sekali di sebagian periode,
    dan itu bukan alasan membatalkan seluruh adjudikasi.
    """
    nilai = [matriks[t][kolom] for t in indeks]
    n = len(nilai)
    if n < 2:
        raise ValueError("perlu >= 2 observasi")
    mu = sum(nilai) / n
    ragam = sum((x - mu) ** 2 for x in nilai) / (n - 1)
    if ragam <= 0.0:
        return KINERJA_DEGENERAT
    return mu / math.sqrt(ragam)


def peringkat_tengah(nilai: Sequence[float], terpilih: int) -> float:
    """Peringkat-tengah (midrank) ``nilai[terpilih]`` di dalam ``nilai``.

    1 = terburuk, len(nilai) = terbaik. Seri dibagi rata, sehingga sekumpulan
    konfigurasi yang identik tidak memberi keuntungan atau kerugian palsu pada
    yang terpilih -- ia mendapat peringkat tengah kelompok serinya.
    """
    acuan = nilai[terpilih]
    lebih_kecil = sum(1 for x in nilai if x < acuan)
    seri = sum(1 for x in nilai if x == acuan)
    return lebih_kecil + (seri + 1) / 2.0


def logit(omega: float) -> float:
    """Logit peringkat relatif. omega harus di dalam (0, 1)."""
    if not (0.0 < omega < 1.0):
        raise ValueError(f"omega harus di dalam (0, 1), diterima {omega!r}")
    return math.log(omega / (1.0 - omega))


def pbo(matriks: Sequence[Sequence[float]], s_bagian: int = 8) -> dict:
    """PBO lewat CSCV. Mengembalikan seluruh perantara supaya dapat diperiksa ulang.

    Prosedur, tiap langkah dapat dilacak di keluaran:

    1. Bagi periode menjadi ``s_bagian`` blok berurutan.
    2. Untuk setiap cara memilih separuh blok sebagai latih, komplemennya
       menjadi uji. Kedua arah muncul dengan sendirinya karena seluruh
       kombinasi C(S, S/2) dijelajahi -- itulah simetri CSCV.
    3. Pada latih, pilih konfigurasi dengan Sharpe tertinggi.
    4. Pada uji, hitung peringkat relatif konfigurasi itu:
       omega = peringkat / (N + 1), sehingga omega selalu di dalam (0, 1).
    5. PBO = pecahan kombinasi dengan omega < 0,5, yakni logit < 0.

    Tafsirnya: PBO 0,5 berarti juara dalam-sampel sama saja dengan lemparan koin
    di luar sampel -- pencarian tidak menemukan apa pun selain derau. PBO kecil
    berarti peringkatnya bertahan.
    """
    n_observasi, n_konfigurasi = periksa_matriks(matriks)
    bagian = bagi_subsampel(n_observasi, s_bagian)
    separuh = s_bagian // 2
    cacah = math.comb(s_bagian, separuh)
    if cacah > MAKS_KOMBINASI:
        raise ValueError(
            f"C({s_bagian},{separuh}) = {cacah} melampaui MAKS_KOMBINASI = "
            f"{MAKS_KOMBINASI}; pilih s_bagian lebih kecil"
        )

    logit_semua: List[float] = []
    omega_semua: List[float] = []
    kinerja_latih_terpilih: List[float] = []
    kinerja_uji_terpilih: List[float] = []
    cacah_semua_degenerat = 0

    seluruh = set(range(s_bagian))
    for pilihan in combinations(range(s_bagian), separuh):
        idx_latih = [t for b in pilihan for t in bagian[b]]
        idx_uji = [t for b in sorted(seluruh - set(pilihan)) for t in bagian[b]]

        nilai_latih = [kinerja(matriks, idx_latih, n) for n in range(n_konfigurasi)]
        if all(v == KINERJA_DEGENERAT for v in nilai_latih):
            cacah_semua_degenerat += 1
            continue
        terpilih = max(range(n_konfigurasi), key=lambda n: nilai_latih[n])

        nilai_uji = [kinerja(matriks, idx_uji, n) for n in range(n_konfigurasi)]
        peringkat = peringkat_tengah(nilai_uji, terpilih)
        omega = peringkat / (n_konfigurasi + 1.0)

        omega_semua.append(omega)
        logit_semua.append(logit(omega))
        kinerja_latih_terpilih.append(nilai_latih[terpilih])
        kinerja_uji_terpilih.append(nilai_uji[terpilih])

    if not logit_semua:
        raise ValueError(
            "tidak ada kombinasi yang dapat dinilai; seluruh kolom datar pada "
            "setiap belahan latih"
        )

    negatif = sum(1 for x in logit_semua if x < 0.0)
    nilai_pbo = negatif / len(logit_semua)
    terurut = sorted(logit_semua)
    tengah = len(terurut) // 2
    if len(terurut) % 2 == 1:
        logit_median = terurut[tengah]
    else:
        logit_median = 0.5 * (terurut[tengah - 1] + terurut[tengah])

    layak_latih = [x for x in kinerja_latih_terpilih if x != KINERJA_DEGENERAT]
    layak_uji = [x for x in kinerja_uji_terpilih if x != KINERJA_DEGENERAT]
    rerata_latih = sum(layak_latih) / len(layak_latih) if layak_latih else None
    rerata_uji = sum(layak_uji) / len(layak_uji) if layak_uji else None
    kemerosotan = (
        None if rerata_latih is None or rerata_uji is None else rerata_uji - rerata_latih
    )

    return {
        "n_observasi": n_observasi,
        "n_konfigurasi": n_konfigurasi,
        "s_bagian": s_bagian,
        "cacah_kombinasi": cacah,
        "cacah_dinilai": len(logit_semua),
        "cacah_semua_degenerat": cacah_semua_degenerat,
        "pbo": nilai_pbo,
        "cacah_logit_negatif": negatif,
        "logit_median": logit_median,
        "omega_median": sorted(omega_semua)[len(omega_semua) // 2],
        "rerata_sharpe_latih_terpilih": rerata_latih,
        "rerata_sharpe_uji_terpilih": rerata_uji,
        "kemerosotan_luar_sampel": kemerosotan,
        "ambang": AMBANG_PBO,
        "lulus": nilai_pbo < AMBANG_PBO,
    }
