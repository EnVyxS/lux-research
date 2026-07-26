"""Lantai jarak stop dan pengaman biaya masuk (ADR-014 bagian 8).

Modul ini ada karena satu cacat yang sudah laten sejak H-001b dan baru terbuka
di H-011: **satuan R kehilangan artinya ketika jarak stop mendekati nol.**

Satu R adalah jarak dari harga masuk ke stop. Seluruh biaya dinyatakan dengan
membaginya dengan jarak itu (``lux.costs.biaya_dalam_R``). Pembagian itu tidak
punya batas bawah. Pada USDCUSDT, sebuah pasangan stablecoin terhadap dolar,
rasio ATR terhadap harga praktis nol sehingga ``stop_frac`` mencapai
3,1984e-06. Akibatnya satu perdagangan mencatat biaya transaksi **312,73R** dan
gerbang ``invarian_risiko`` melaporkan **-470,06R** terhadap ambang -1,5R.
Simbol itu sendirian memikul -18.861,06R dari total -10.781,32R atas 438 simbol.

Empat puluh simbol pertama secara alfabet tidak memuat satu pun pasangan
semacam itu, sehingga H-002 sampai H-010 tidak pernah bertemu keadaan ini.
Itu bukan keberuntungan yang menenangkan, melainkan bukti bahwa semesta kecil
menyembunyikan cacat, bukan menghindarinya.

DUA AMBANG, KEDUANYA DITURUNKAN DARI ARITMETIKA
-----------------------------------------------
Ambang di sini **tidak** disetel terhadap hasil H-011. Keduanya berasal dari
model biaya yang sudah dibekukan sejak awal:

- Biaya bolak-balik pada ``ModelBiaya`` bawaan adalah ``2 * (fee + slippage)``
  = 0,002 dari harga.
- Biaya itu menjadi tepat **0,5R** ketika jarak stop bernilai **0,004** dari
  harga, karena 0,002 / 0,004 = 0,5.

Maka ``AMBANG_MIN_STOP_FRAC = 0.004`` dan ``AMBANG_BIAYA_MASUK_R = 0.5`` adalah
dua cara menyatakan satu batas yang sama, dan keduanya bertemu di titik batas:
median tepat di lantai diterima, dan entri di lantai itu tidak ditolak.

Kedua angka itu dibekukan di ADR-014 sebelum H-012 dijalankan. Menggesernya
sesudah melihat hasil H-012 adalah pelanggaran, dan disebut demikian di sana.

MENGAPA LANTAI, BUKAN PEMBUANGAN SIMBOL
---------------------------------------
Membuang USDCUSDT dari semesta sesudah melihat hasilnya adalah pemilihan
subkumpulan pasca-hoc, yaitu bentuk kecurangan yang paling mudah dibela.
Diagnostik yang diperoleh dengan cara itu tercatat di ADR-014 sebagai
**terlarang dipakai sebagai hasil**. Yang sah hanya aturan yang seragam,
ditulis lebih dulu, dan berlaku untuk simbol mana pun yang memenuhinya —
termasuk simbol yang belum ada di semesta hari ini.

DEGENERASI DIBUKTIKAN OLEH ``stop_frac``, BUKAN OLEH EJAAN
----------------------------------------------------------
Saringan pertama yang saya tulis mencari pola nama stablecoin dan langsung
menandai ``BUSDT`` serta ``TUSDT``, yang hampir pasti token "B" dan "T" dan
bukan stablecoin sama sekali. Angka yang diturunkan dari saringan itu dibuang
seluruhnya. Di modul ini tidak ada satu pun nama simbol yang dipakai sebagai
kriteria; yang dipakai hanya besaran terukur.

BATAS MODUL INI
---------------
Modul ini **sengaja tidak mengimpor** ``lux.backtest.engine``. Engine akan
mengimpornya pada tahap berikutnya, dan impor dua arah adalah cara paling andal
melahirkan lingkaran impor yang baru terasa jauh di dalam run. Karena itu ATR
tidak dihitung di sini: pemanggil menyerahkan deret ATR yang sudah jadi.

Aritmetika biaya diambil apa adanya dari ``lux.costs.biaya_dalam_R``. Dua
implementasi dari besaran yang sama adalah cara paling andal melahirkan selisih
yang tidak terdeteksi siapa pun, dan pada besaran biaya selisih itu hampir
selalu berpihak pada hasil yang lebih indah.

SATU CATATAN SKALA YANG WAJIB DIPAHAMI
--------------------------------------
``biaya_masuk_R`` di sini menghitung fee **dan** slippage, yaitu 0,002 dari
harga. Kolom ``transaksi_R`` di laporan backtest hanya memuat fee, karena
slippage sudah tertanam di harga eksekusi. Jadi angka modul ini kira-kira dua
kali angka laporan: pada ``stop_frac`` 3,1984e-06, laporan mencatat 312,73R
sementara modul ini menghitung 625,5R. Perbedaan itu disengaja dan arahnya
aman, sebab pengaman yang menghitung seluruh biaya lebih ketat daripada
pengaman yang lupa slippage.
"""

from __future__ import annotations

import math
from typing import Mapping, Sequence

import numpy as np

from lux.costs import ModelBiaya, biaya_dalam_R

NAMA = "degenerasi"

# Lantai jarak stop sebagai pecahan harga. Diturunkan, bukan disetel: pada model
# biaya bawaan, biaya bolak-balik 0,002 dari harga menjadi tepat 0,5R di sini.
AMBANG_MIN_STOP_FRAC = 0.004

# Batas biaya satu entri dalam satuan R. Pasangan aritmetika dari lantai di atas.
AMBANG_BIAYA_MASUK_R = 0.5

# Bukti dari lapangan, disalin dari reports/backtest_h011_semesta_penuh.json
# @ 2bb7b963. Dipakai sebagai jangkar pengujian supaya modul ini diuji terhadap
# angka yang benar-benar terjadi, bukan hanya terhadap angka karangan.
KASUS_USDCUSDT = {
    "symbol": "USDCUSDT",
    "stop_frac": 3.1984170825288993e-06,
    "transaksi_R_di_laporan": 312.7333222023922,
    "R": -470.0611513462926,
}


def periksa_derivasi(model: ModelBiaya | None = None) -> dict:
    """Bukti bahwa kedua ambang adalah satu batas yang sama.

    Dikembalikan sebagai data alih-alih dipaksakan sebagai ``assert`` di waktu
    impor, supaya kegagalannya muncul di pengujian dan di gerbang pra-terbang,
    bukan sebagai kematian mendadak di tengah run panjang.
    """
    m = model or ModelBiaya()
    biaya_di_lantai = biaya_dalam_R(AMBANG_MIN_STOP_FRAC, m)
    return {
        "biaya_bolak_balik": m.biaya_bolak_balik,
        "lantai_stop_frac": AMBANG_MIN_STOP_FRAC,
        "biaya_di_lantai_R": biaya_di_lantai,
        "ambang_biaya_masuk_R": AMBANG_BIAYA_MASUK_R,
        "konsisten": abs(biaya_di_lantai - AMBANG_BIAYA_MASUK_R) < 1e-12,
    }


def stop_frac_deret(
    atr_deret: Sequence[float] | np.ndarray,
    harga: Sequence[float] | np.ndarray,
    pengali: float = 2.0,
) -> np.ndarray:
    """Deret jarak stop sebagai pecahan harga, hanya dari titik yang sah.

    Yang dibuang **hanya** nilai yang tidak dapat dihitung: ATR tidak finit
    (periode pemanasan) dan harga yang tidak positif.

    ATR bernilai **nol tetap disertakan**, dan itu keputusan yang penting.
    ATR nol berarti harga tidak bergerak sama sekali, yaitu justru keadaan
    degenerat yang sedang dicari. Membuangnya akan menaikkan median dan membuat
    simbol paling degenerat tampak paling layak. Arah kesalahan itu tepat arah
    yang paling merugikan.
    """
    if pengali <= 0:
        raise ValueError("pengali stop harus positif")
    a = np.asarray(atr_deret, dtype="float64")
    h = np.asarray(harga, dtype="float64")
    if a.shape != h.shape:
        raise ValueError("panjang deret ATR dan harga harus sama")
    sah = np.isfinite(a) & np.isfinite(h) & (a >= 0.0) & (h > 0.0)
    return pengali * (a[sah] / h[sah])


def median_stop_frac(
    atr_deret: Sequence[float] | np.ndarray,
    harga: Sequence[float] | np.ndarray,
    pengali: float = 2.0,
) -> float | None:
    """Median jarak stop sebuah simbol, atau ``None`` bila tak dapat dinilai.

    Median, bukan rerata: satu lonjakan volatilitas tidak boleh menyelamatkan
    simbol yang sepanjang hidupnya nyaris tidak bergerak.
    """
    d = stop_frac_deret(atr_deret, harga, pengali)
    if d.size == 0:
        return None
    return float(np.median(d))


def layak_stop_frac(
    median: float | None, ambang: float = AMBANG_MIN_STOP_FRAC
) -> bool:
    """Apakah simbol dengan median ini layak diuji.

    Simbol yang **tidak dapat dinilai** ditolak, bukan diloloskan. Meloloskan
    yang tidak diketahui adalah kelalaian yang menyamar sebagai kelulusan, dan
    pada pengaman risiko kelalaian itu selalu menguntungkan hasil.
    """
    if ambang <= 0:
        raise ValueError("ambang lantai stop harus positif")
    if median is None:
        return False
    if not math.isfinite(median):
        return False
    return median >= ambang


def biaya_masuk_R(
    stop_pecahan: float, model: ModelBiaya | None = None
) -> float:
    """Biaya bolak-balik satu entri dalam satuan R, tanpa melempar galat.

    Jarak stop nol atau tidak finit mengembalikan ``inf`` alih-alih
    ``ValueError``. Pengaman ini dipanggil di dalam gelung mesin backtest, dan
    pengaman yang bisa mematikan run 838 detik di perdagangan ke seratus ribu
    bukan pengaman melainkan bahaya baru. Tak hingga adalah jawaban yang benar:
    biaya yang dibagi nol memang tak terbatas.
    """
    if not math.isfinite(stop_pecahan) or stop_pecahan <= 0.0:
        return math.inf
    return biaya_dalam_R(stop_pecahan, model)


def entri_terlalu_mahal(
    stop_pecahan: float,
    ambang: float = AMBANG_BIAYA_MASUK_R,
    model: ModelBiaya | None = None,
) -> bool:
    """Apakah entri ini wajib ditolak karena biayanya melebihi ``ambang`` R.

    Perbandingannya ``>``, bukan ``>=``, supaya entri tepat di titik batas
    tetap sah dan lantai semesta serta pengaman mesin sepakat di titik yang
    sama persis.
    """
    if ambang <= 0:
        raise ValueError("ambang biaya masuk harus positif")
    return biaya_masuk_R(stop_pecahan, model) > ambang


def saring_semesta(
    median_per_simbol: Mapping[str, float | None],
    ambang: float = AMBANG_MIN_STOP_FRAC,
    model: ModelBiaya | None = None,
) -> dict:
    """Pisahkan simbol layak dari simbol degenerat, dengan alasan tercatat.

    Tidak ada nama simbol yang diperlakukan istimewa. Yang menentukan hanya
    median jarak stop, sehingga aturan ini berlaku sama untuk simbol yang belum
    ada di semesta hari ini.
    """
    layak: list[str] = []
    ditolak: list[dict] = []
    for s in sorted(median_per_simbol):
        m = median_per_simbol[s]
        if layak_stop_frac(m, ambang):
            layak.append(s)
            continue
        if m is None:
            sebab = "median jarak stop tidak dapat dinilai"
        elif not math.isfinite(m):
            sebab = "median jarak stop tidak finit"
        else:
            sebab = f"median jarak stop {m:.3e} di bawah lantai {ambang}"
        ditolak.append(
            {
                "symbol": s,
                "median_stop_frac": m,
                "biaya_masuk_R": (None if m is None else biaya_masuk_R(m, model)),
                "sebab": sebab,
            }
        )
    return {
        "ambang": ambang,
        "n_masuk": len(median_per_simbol),
        "n_layak": len(layak),
        "n_ditolak": len(ditolak),
        "layak": layak,
        "ditolak": ditolak,
    }
