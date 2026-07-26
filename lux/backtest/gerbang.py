"""Sepuluh gerbang mutu yang harus dilewati sebelum sebuah hasil dipercaya.

Gerbang ini dipasang **bersamaan dengan mesinnya**, bukan sesudah ada hasil
pertama. Urutan itu penting dan bukan soal kerapian: gerbang yang dirancang
setelah melihat hasil akan dirancang, tanpa niat buruk sekalipun, sedemikian
rupa sehingga hasil itu lolos. Ambang yang ditulis di sini ditetapkan sebelum
satu strategi pun dijalankan.

**Aturan pokok: gerbang yang tidak dapat dinilai berarti GAGAL, bukan lulus.**
Ini terbalik dari kebiasaan umum dan memang disengaja. Bila data funding tidak
dimuat, gerbang funding tidak boleh mengembalikan "lulus" hanya karena tidak
menemukan pelanggaran; ia tidak menemukan apa-apa karena tidak memeriksa apa
pun. Kelalaian yang menyamar sebagai kelulusan adalah cara paling sunyi sebuah
pipeline riset membohongi pemiliknya.

Sembilan gerbang pertama: forward-fill, buy-and-hold, entri acak, lookahead,
invarian risiko, funding, overlap, checksum, survivorship.

Gerbang kesepuluh, **konsentrasi**, ditambahkan oleh ADR-010 dan tinggal di
``lux/backtest/konsentrasi.py``, bukan di berkas ini. Alasannya teknis dan
sudah dibayar sekali: modul itu mengimpor ``Gerbang`` dari sini, sehingga bila
berkas ini mengimpornya balik lahirlah impor sirkular seperti cacat komit
``4b77617``. ``NAMA_GERBANG`` tetap menjadi satu-satunya daftar resmi, dan
runner-lah yang menyatukan keduanya.

Konsekuensi yang perlu diketahui: tiga orkestrator lama yang dibekukan
(``run_wf``, ``run_h002``, ``run_h003``) hanya menyusun sembilan gerbang. Bila
salah satunya dijalankan lagi, ``konsentrasi`` akan tercatat sebagai "gerbang
tidak dijalankan" dan laporannya gagal. Itu bukan cacat melainkan pernyataan
yang benar: orkestrator itu sungguh tidak mengukur konsentrasi.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from lux.backtest.engine import Hasil


@dataclass(frozen=True)
class Gerbang:
    """Hasil satu gerbang.

    ``nilai`` dan ``ambang`` selalu ikut dilaporkan, bukan hanya lulus/gagal.
    Gerbang yang hanya mengembalikan boolean menyembunyikan seberapa dekat
    sebuah hasil dengan kegagalan, dan jarak itu sering lebih informatif
    daripada putusannya.
    """

    nama: str
    lulus: bool
    nilai: float | None
    ambang: float | None
    catatan: str

    @property
    def dapat_dinilai(self) -> bool:
        return self.nilai is not None


def _gagal_tak_ternilai(nama: str, sebab: str) -> Gerbang:
    return Gerbang(
        nama=nama,
        lulus=False,
        nilai=None,
        ambang=None,
        catatan=f"tidak dapat dinilai: {sebab}",
    )


# --------------------------------------------------------------------------
# 1. Forward-fill
# --------------------------------------------------------------------------
def gerbang_forward_fill(
    df: pd.DataFrame, maks_rasio_datar: float = 0.30, maks_deret_datar: int = 24
) -> Gerbang:
    """Menolak data yang harganya diisi ulang, bukan diperdagangkan.

    Bar datar sempurna berarti tidak ada transaksi pada periode itu. Sinyal
    yang lahir dari deretan bar seperti itu memperdagangkan harga yang tidak
    pernah ditawarkan siapa pun, dan stop pada bar datar tidak akan pernah
    tersentuh sehingga kerugian tampak lebih kecil daripada semestinya.
    """
    if df.empty:
        return _gagal_tak_ternilai("forward_fill", "bingkai kosong")
    o = df["open"].to_numpy(dtype="float64")
    h = df["high"].to_numpy(dtype="float64")
    l = df["low"].to_numpy(dtype="float64")
    c = df["close"].to_numpy(dtype="float64")
    datar = (o == h) & (h == l) & (l == c)
    rasio = float(datar.mean())

    deret = 0
    terpanjang = 0
    for d in datar:
        deret = deret + 1 if d else 0
        terpanjang = max(terpanjang, deret)

    lulus = rasio <= maks_rasio_datar and terpanjang <= maks_deret_datar
    return Gerbang(
        nama="forward_fill",
        lulus=lulus,
        nilai=rasio,
        ambang=maks_rasio_datar,
        catatan=f"rasio bar datar {rasio:.4f}, deret terpanjang {terpanjang} bar",
    )


# --------------------------------------------------------------------------
# 2. Buy-and-hold
# --------------------------------------------------------------------------
def gerbang_buy_and_hold(
    hasil: Hasil, df: pd.DataFrame, min_keunggulan: float = 0.0
) -> Gerbang:
    """Strategi harus mengalahkan tindakan tidak melakukan apa-apa.

    Sebagian besar strategi yang tampak berhasil pada aset yang naik panjang
    sesungguhnya hanya sedang memegang aset itu dengan langkah tambahan yang
    memakan biaya. Perbandingannya tidak sepenuhnya setara karena strategi
    memakai posisi berukuran risiko dan bisa short, jadi drawdown kedua pihak
    ikut dilaporkan agar keunggulan tipis tidak disalahbaca sebagai keunggulan.
    """
    if hasil.ekuitas.size == 0 or df.empty:
        return _gagal_tak_ternilai("buy_and_hold", "tidak ada kurva ekuitas")
    c = df["close"].to_numpy(dtype="float64")
    if c[0] <= 0:
        return _gagal_tak_ternilai("buy_and_hold", "harga awal tidak sah")
    imbal_strategi = float(hasil.ekuitas[-1] / hasil.ekuitas[0] - 1.0)
    imbal_pasar = float(c[-1] / c[0] - 1.0)
    selisih = imbal_strategi - imbal_pasar
    return Gerbang(
        nama="buy_and_hold",
        lulus=selisih > min_keunggulan,
        nilai=selisih,
        ambang=min_keunggulan,
        catatan=f"strategi {imbal_strategi:.4f} vs pasar {imbal_pasar:.4f}",
    )


# --------------------------------------------------------------------------
# 3. Entri acak
# --------------------------------------------------------------------------
def gerbang_entri_acak(
    nilai_nyata: float,
    sinyal: np.ndarray,
    penilai: Callable[[np.ndarray], float],
    ulangan: int = 200,
    seed: int = 42,
    maks_p: float = 0.05,
) -> Gerbang:
    """Uji permutasi: apakah waktunya yang berarti, atau sekadar seringnya?

    Sinyal diacak urutannya sehingga jumlah dan arah entri persis sama, tetapi
    waktunya hancur. Bila hasil sesungguhnya tidak lebih baik daripada sebaran
    entri acak, yang terukur selama ini adalah eksposur dan ukuran posisi, bukan
    kemampuan memilih momen. Ini gerbang yang paling sering menjatuhkan strategi
    yang kurva ekuitasnya terlihat meyakinkan.
    """
    if ulangan < 1:
        return _gagal_tak_ternilai("entri_acak", "ulangan harus minimal 1")
    if not np.isfinite(nilai_nyata):
        return _gagal_tak_ternilai("entri_acak", "nilai nyata tidak terdefinisi")
    if int((np.asarray(sinyal) != 0).sum()) == 0:
        return _gagal_tak_ternilai("entri_acak", "tidak ada sinyal untuk diacak")

    rng = np.random.default_rng(seed)
    dasar = np.asarray(sinyal).copy()
    sebanding = 0
    for _ in range(ulangan):
        acak = rng.permutation(dasar)
        nilai = penilai(acak)
        if np.isfinite(nilai) and nilai >= nilai_nyata:
            sebanding += 1
    # Penyebut ulangan+1 memasukkan hasil nyata itu sendiri ke dalam sebaran,
    # sehingga p tidak pernah nol. Nilai p nol adalah klaim kepastian yang
    # tidak pernah dihasilkan oleh sampel terbatas.
    p = (sebanding + 1) / (ulangan + 1)
    return Gerbang(
        nama="entri_acak",
        lulus=p <= maks_p,
        nilai=p,
        ambang=maks_p,
        catatan=f"{sebanding} dari {ulangan} permutasi menyamai atau melampaui",
    )


# --------------------------------------------------------------------------
# 4. Lookahead
# --------------------------------------------------------------------------
def gerbang_lookahead(
    df: pd.DataFrame,
    fungsi_sinyal: Callable[[pd.DataFrame], np.ndarray],
    titik_potong: Iterable[int] | None = None,
) -> Gerbang:
    """Sinyal untuk bar t tidak boleh berubah ketika bar sesudahnya dihapus.

    Ini menangkap bentuk lookahead yang paling sering lolos tanpa disadari:
    jendela bergulir yang terpusat, normalisasi memakai rerata atau simpangan
    seluruh periode, penskalaan memakai harga tertinggi sepanjang data, dan
    pengisian nilai kosong dengan metode mundur. Semuanya tampak wajar dalam
    kode dan tidak satu pun meninggalkan jejak pada kurva ekuitas.
    """
    n = len(df)
    if n < 10:
        return _gagal_tak_ternilai("lookahead", "data terlalu pendek untuk dipotong")
    potong = list(titik_potong) if titik_potong is not None else [
        n // 4,
        n // 2,
        (3 * n) // 4,
    ]
    penuh = np.asarray(fungsi_sinyal(df))
    if penuh.size != n:
        return _gagal_tak_ternilai("lookahead", "panjang sinyal tidak sama dengan bar")

    beda_total = 0
    for k in potong:
        if k < 2 or k > n:
            continue
        sebagian = np.asarray(fungsi_sinyal(df.iloc[:k].copy()))
        if sebagian.size != k:
            return _gagal_tak_ternilai(
                "lookahead", "sinyal potongan tidak sepanjang potongannya"
            )
        beda_total += int((sebagian != penuh[:k]).sum())

    return Gerbang(
        nama="lookahead",
        lulus=beda_total == 0,
        nilai=float(beda_total),
        ambang=0.0,
        catatan=f"{beda_total} sinyal berubah saat data masa depan dihapus",
    )


# --------------------------------------------------------------------------
# 5. Invarian risiko
# --------------------------------------------------------------------------
def gerbang_invarian_risiko(hasil: Hasil, maks_kerugian_R: float = 1.5) -> Gerbang:
    """Tidak ada satu perdagangan pun yang boleh rugi jauh melebihi 1R.

    Ambang 1,5R bukan 1,0R karena biaya transaksi dan funding memang menambah
    kerugian di luar jarak stop, dan itu sah. Yang tidak sah adalah kerugian
    besar yang berasal dari ukuran posisi salah hitung atau stop yang tidak
    dihormati. Kerugian ekstrem tunggal juga penanda paling awal bahwa sizing
    memakai modal, bukan risiko.
    """
    if hasil.jumlah_trade == 0:
        return _gagal_tak_ternilai("invarian_risiko", "tidak ada perdagangan")
    rs = np.array([p.R for p in hasil.perdagangan], dtype="float64")
    terburuk = float(rs.min())
    return Gerbang(
        nama="invarian_risiko",
        lulus=terburuk >= -maks_kerugian_R,
        nilai=terburuk,
        ambang=-maks_kerugian_R,
        catatan=f"kerugian terburuk {terburuk:.3f}R dari {rs.size} perdagangan",
    )


# --------------------------------------------------------------------------
# 6. Funding
# --------------------------------------------------------------------------
def gerbang_funding(hasil: Hasil, jadwal_dimuat: bool) -> Gerbang:
    """Funding harus benar-benar dihitung, bukan kebetulan bernilai nol.

    Gerbang ini ada karena funding nol tidak terlihat berbeda dari funding yang
    lupa dipasang. Pada 79,1% periode funding bernilai positif, sehingga pemegang
    long membayar; strategi long yang funding-nya persis nol hampir pasti sedang
    tidak memperhitungkannya sama sekali.

    Catatan yang diperoleh dengan mahal di S12: gerbang ini hanya memastikan
    funding **dihitung**, bukan bahwa pengaruhnya jinak. Rerata funding 0,0004R
    pernah saya pakai untuk menyimpulkan funding tidak bersalah, padahal pada
    kerugian terburuk H-008 porsinya 46,7%. Rerata tidak mengatakan apa pun
    tentang ekor.
    """
    if not jadwal_dimuat:
        return _gagal_tak_ternilai("funding", "jadwal funding tidak dimuat")
    if hasil.jumlah_trade == 0:
        return _gagal_tak_ternilai("funding", "tidak ada perdagangan")
    total = float(sum(abs(p.biaya_funding) for p in hasil.perdagangan))
    return Gerbang(
        nama="funding",
        lulus=total > 0.0,
        nilai=total,
        ambang=0.0,
        catatan=f"total funding mutlak {total:.6f} atas {hasil.jumlah_trade} trade",
    )


# --------------------------------------------------------------------------
# 7. Overlap
# --------------------------------------------------------------------------
def gerbang_overlap(hasil: Hasil) -> Gerbang:
    """Perdagangan tidak boleh saling bertindih waktunya.

    Posisi bertumpuk menaikkan ekuitas lewat penambahan eksposur, bukan lewat
    keunggulan sinyal, dan sekaligus merusak arti satuan R karena risiko
    serempaknya menjadi kelipatan dari yang dinyatakan.
    """
    if hasil.jumlah_trade == 0:
        return _gagal_tak_ternilai("overlap", "tidak ada perdagangan")
    urut = sorted(hasil.perdagangan, key=lambda p: p.masuk_ms)
    tindih = sum(1 for a, b in zip(urut, urut[1:]) if b.masuk_ms < a.keluar_ms)
    return Gerbang(
        nama="overlap",
        lulus=tindih == 0,
        nilai=float(tindih),
        ambang=0.0,
        catatan=f"{tindih} pasang perdagangan bertindih",
    )


# --------------------------------------------------------------------------
# 8. Checksum
# --------------------------------------------------------------------------
def gerbang_checksum(
    manifest: dict[str, str], terhitung: dict[str, str]
) -> Gerbang:
    """Data yang dipakai harus data yang sama dengan yang divalidasi.

    Tanpa gerbang ini, satu aset yang diam-diam ditimpa atau satu berkas usang
    yang tertinggal di direktori kerja cukup untuk membuat seluruh hasil tidak
    dapat diulang. Kejadian nyata di proyek ini: aset ``_retry`` yang sudah
    dinyatakan tidak sah tetap ikut terbaca dan menambahkan 12.593 baris ke
    hasil validasi, karena mencatat sesuatu tidak sah tidak menghapusnya dari
    disk.
    """
    if not manifest:
        return _gagal_tak_ternilai("checksum", "manifest kosong")
    hilang = sorted(set(manifest) - set(terhitung))
    asing = sorted(set(terhitung) - set(manifest))
    beda = sorted(k for k in manifest if k in terhitung and manifest[k] != terhitung[k])
    masalah = len(hilang) + len(asing) + len(beda)
    return Gerbang(
        nama="checksum",
        lulus=masalah == 0,
        nilai=float(masalah),
        ambang=0.0,
        catatan=f"hilang {len(hilang)}, asing {len(asing)}, tidak cocok {len(beda)}",
    )


# --------------------------------------------------------------------------
# 9. Survivorship
# --------------------------------------------------------------------------
def gerbang_survivorship(
    simbol_diuji: Iterable[str],
    simbol_delisted: Iterable[str],
    simbol_universe: Iterable[str],
    rasio_minimum: float = 0.5,
) -> Gerbang:
    """Simbol yang sudah mati harus ikut diuji, sebanding porsinya di universe.

    Menguji hanya simbol yang masih diperdagangkan hari ini berarti menguji
    hanya yang selamat. Universe kita memuat 29 perp USDT yang sudah delisted
    dari 790; menghilangkan semuanya akan membuang justru kasus-kasus terburuk,
    yang biasanya mati setelah pergerakan paling merusak.

    Ambang ditetapkan sebagai porsi relatif, bukan jumlah mutlak, karena
    penyaringan kelayakan yang sah memang boleh menggugurkan sebagian simbol
    mati; yang tidak boleh adalah menggugurkan hampir semuanya.
    """
    diuji = set(simbol_diuji)
    mati = set(simbol_delisted)
    semesta = set(simbol_universe)
    if not diuji or not semesta:
        return _gagal_tak_ternilai("survivorship", "daftar simbol kosong")
    porsi_semesta = len(mati & semesta) / len(semesta)
    if porsi_semesta == 0:
        return _gagal_tak_ternilai(
            "survivorship", "universe tidak memuat simbol delisted"
        )
    porsi_diuji = len(mati & diuji) / len(diuji)
    rasio = porsi_diuji / porsi_semesta
    return Gerbang(
        nama="survivorship",
        lulus=rasio >= rasio_minimum,
        nilai=rasio,
        ambang=rasio_minimum,
        catatan=(
            f"porsi delisted diuji {porsi_diuji:.4f} vs universe {porsi_semesta:.4f}"
        ),
    )


# --------------------------------------------------------------------------
# 10. Konsentrasi — lihat lux/backtest/konsentrasi.py
# --------------------------------------------------------------------------
# Gerbang kesepuluh sengaja tidak didefinisikan di berkas ini agar tidak ada
# impor sirkular. Ia hidup di lux/backtest/konsentrasi.py dan dipanggil oleh
# runner. Namanya tetap terdaftar di NAMA_GERBANG di bawah, sehingga bila
# runner lupa memanggilnya, susun_laporan mencatatnya sebagai gagal.


# --------------------------------------------------------------------------
# Laporan gabungan
# --------------------------------------------------------------------------
@dataclass
class LaporanGerbang:
    gerbang: list[Gerbang] = field(default_factory=list)

    @property
    def semua_lulus(self) -> bool:
        """Tidak ada rata-rata dan tidak ada keringanan.

        Satu gerbang gagal berarti pipeline berhenti. Membiarkan sembilan dari
        sepuluh dianggap cukup akan mengubah gerbang menjadi skor, dan skor
        selalu bisa dinegosiasikan.

        Jumlahnya dibandingkan dengan ``len(NAMA_GERBANG)``, bukan dengan angka
        yang ditulis tangan. Angka yang ditulis tangan akan tertinggal pada saat
        gerbang berikutnya ditambahkan, dan tertinggalnya akan berupa kelulusan.
        """
        return len(self.gerbang) == len(NAMA_GERBANG) and all(
            g.lulus for g in self.gerbang
        )

    @property
    def yang_gagal(self) -> list[str]:
        return [g.nama for g in self.gerbang if not g.lulus]

    def ke_dict(self) -> dict:
        return {
            "semua_lulus": self.semua_lulus,
            "gerbang_gagal": self.yang_gagal,
            "rincian": [
                {
                    "nama": g.nama,
                    "lulus": g.lulus,
                    "nilai": g.nilai,
                    "ambang": g.ambang,
                    "catatan": g.catatan,
                }
                for g in self.gerbang
            ],
        }


NAMA_GERBANG = (
    "forward_fill",
    "buy_and_hold",
    "entri_acak",
    "lookahead",
    "invarian_risiko",
    "funding",
    "overlap",
    "checksum",
    "survivorship",
    "konsentrasi",
)


def susun_laporan(gerbang: Iterable[Gerbang]) -> LaporanGerbang:
    """Susun laporan sambil memastikan kesepuluh gerbang benar-benar hadir.

    Gerbang yang lupa dijalankan dicatat sebagai gagal dengan sebab yang jelas.
    Diam bukan kelulusan.
    """
    ada = {g.nama: g for g in gerbang}
    lengkap = []
    for nama in NAMA_GERBANG:
        lengkap.append(
            ada.get(nama) or _gagal_tak_ternilai(nama, "gerbang tidak dijalankan")
        )
    return LaporanGerbang(gerbang=lengkap)
