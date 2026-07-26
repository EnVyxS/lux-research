"""Ukuran konsentrasi keunggulan antar simbol (ADR-010).

Modul ini lahir dari kekeliruan saya sendiri, dan itu ditulis di sini supaya
tidak terulang. Pada S12 saya melaporkan bahwa "sepuluh dari 40 simbol
menghasilkan 101,2% laba" lalu menyebutnya fragilitas terbesar yang tersisa.
Angkanya benar, tafsirnya menyesatkan **secara konstruksi**: bila ada penyumbang
negatif sama sekali, porsi penyumbang teratas terhadap total *bersih* hampir
pasti melewati 100% tanpa konsentrasi apa pun, karena penyebutnya sudah
dikecilkan oleh yang merugi. Porsi terhadap nilai bersih bukan ukuran
konsentrasi. Ia bahkan bukan ukuran apa pun.

Yang dipakai di sini ada dua, keduanya kebal terhadap cacat itu.

1. **Jackknife.** Buang penyumbang teratas satu per satu, hitung ulang
   ekspektasinya. Ini menjawab pertanyaan yang sesungguhnya ingin dijawab:
   apakah keunggulan tetap ada seandainya simbol paling untung tidak pernah
   ada. Tidak ada penyebut yang bisa dimanipulasi oleh tanda.
2. **Penyebut bruto.** Porsi diukur terhadap jumlah laba simbol yang untung,
   bukan terhadap laba bersih portofolio. Penyebut bruto tidak dapat
   dikecilkan oleh penyumbang negatif, sehingga porsinya selalu terletak di
   antara 0 dan 1. Bila sebuah ukuran bisa melewati 100%, yang salah adalah
   ukurannya, bukan datanya.

Gerbang ini sengaja **tidak** ditaruh di ``gerbang.py``. ``NAMA_GERBANG`` tetap
tinggal di sana, dan bila gerbang.py mengimpor modul ini sementara modul ini
mengimpor ``Gerbang`` dari sana, lahirlah impor sirkular. Cacat itu pernah
terjadi di proyek ini (komit ``4b77617``) dan sekali sudah cukup mahal.
Runner-lah yang menyatukan keduanya.

Ambang di bawah ditulis di ADR-010 **sesudah** hasil H-009 dilihat. Karena itu
untuk H-009 ia hanya deskriptif dan baru mengikat mulai H-010. Itu bukan
kelonggaran yang saya berikan pada diri sendiri, itu konsekuensi dari aturan
yang sama yang menjaga seluruh proyek ini: ambang yang ditulis setelah melihat
data akan, tanpa niat buruk sekalipun, ditulis sedemikian rupa sehingga data
itu lolos.

Satu catatan yang lebih penting daripada seluruh modul ini: gerbang ini menguji
apakah keunggulan tersebar, **bukan** menyarankan agar simbol yang merugi
dibuang. Membuang kedua belas simbol merugi H-009 menaikkan ekspektasi dari
0,0414R ke sekitar 0,0752R dan akan melewati ambang 0,05R. Itu bukan penemuan,
itu survivorship bias yang dikerjakan dengan tangan sendiri, dan itulah persis
mekanisme yang mencemari bot v8.4.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from statistics import median

from lux.backtest.gerbang import Gerbang, _gagal_tak_ternilai

# --- Ambang ADR-010, mengikat mulai H-010 --------------------------------
AMBANG_RETENSI_DROP_1 = 0.60
AMBANG_PORSI_BRUTO_TERATAS = 0.25
PORSI_DROP = 0.05
K_MAKS_JACKKNIFE = 5

NAMA_SUB_UJI = (
    "drop_1_positif",
    "drop_5persen_positif",
    "retensi_drop_1",
    "median_simbol_positif",
    "porsi_bruto_teratas",
)


@dataclass(frozen=True)
class Kontribusi:
    """Sumbangan satu simbol terhadap hasil luar sampel."""

    symbol: str
    total_R: float
    trade: int


def dari_ringkasan(baris: Iterable[Mapping]) -> list[Kontribusi]:
    """Sumber yang dianjurkan: ``ringkasan_simbol`` milik runner.

    ``total_R`` di sana belum dibulatkan. ``per_simbol`` yang ditulis ke laporan
    membulatkannya ke empat desimal; pembulatan itu tidak akan mengubah putusan
    gerbang ini, tetapi tetap tidak ada alasan mewarisinya ke perhitungan.
    """
    return [
        Kontribusi(
            symbol=str(b["symbol"]),
            total_R=float(b["total_R"]),
            trade=int(b["jumlah_trade_luar_sampel"]),
        )
        for b in baris
    ]


def dari_per_simbol(baris: Iterable[Mapping]) -> list[Kontribusi]:
    """Sumber alternatif: blok ``per_simbol`` di laporan yang sudah dikomit.

    Dipakai untuk memeriksa ulang hasil lama tanpa menjalankan apa pun.
    """
    return [
        Kontribusi(
            symbol=str(b["symbol"]),
            total_R=float(b["total_R"]),
            trade=int(b["trade"]),
        )
        for b in baris
    ]


def jumlah_drop_5persen(n: int) -> int:
    """Berapa simbol teratas yang dibuang pada sub-uji kedua.

    Dibulatkan ke atas, dan minimal satu. Pembulatan ke bawah akan membuat
    sub-uji ini tidak melakukan apa-apa pada portofolio kecil, yang justru
    portofolio paling rentan terhadap satu simbol tunggal.
    """
    return max(1, math.ceil(PORSI_DROP * n))


def _urut(kontrib: Iterable[Kontribusi]) -> list[Kontribusi]:
    """Urut menurun berdasarkan total R; nama simbol memutus seri.

    Pemutus seri itu bukan kerapian. Tanpa urutan yang deterministik, dua run
    atas data yang sama bisa membuang simbol yang berbeda dan menghasilkan
    angka jackknife yang berbeda.
    """
    return sorted(kontrib, key=lambda k: (-k.total_R, k.symbol))


def _ekspektasi(kontrib: Iterable[Kontribusi]) -> float | None:
    sisa = list(kontrib)
    trade = sum(k.trade for k in sisa)
    if trade <= 0:
        return None
    return sum(k.total_R for k in sisa) / trade


def ukur_konsentrasi(kontrib: Iterable[Kontribusi]) -> dict:
    """Hitung seluruh ukuran konsentrasi sekaligus.

    Dipisahkan dari gerbangnya supaya tiap sub-ukuran dapat diuji langsung.
    ``Gerbang`` hanya menyimpan satu ``nilai``, dan sebuah gerbang dengan lima
    sub-uji yang hanya melaporkan satu angka adalah gerbang yang menyembunyikan
    empat per lima alasannya.
    """
    dipakai = [k for k in kontrib if k.trade > 0]
    n = len(dipakai)
    hasil: dict = {"n_simbol": n, "dapat_dinilai": False, "sebab": ""}

    if n < 2:
        hasil["sebab"] = (
            f"butuh minimal dua simbol yang berdagang untuk mengukur sebaran, ada {n}"
        )
        return hasil

    urut = _urut(dipakai)
    total_R = sum(k.total_R for k in urut)
    trade = sum(k.trade for k in urut)
    eks = _ekspektasi(urut)
    laba_bruto = sum(k.total_R for k in urut if k.total_R > 0.0)
    rugi_bruto = sum(k.total_R for k in urut if k.total_R < 0.0)

    hasil.update(
        {
            "n_positif": sum(1 for k in urut if k.total_R > 0.0),
            "n_negatif": sum(1 for k in urut if k.total_R < 0.0),
            "trade": trade,
            "total_R": total_R,
            "ekspektasi_R": eks,
            "laba_bruto_R": laba_bruto,
            "rugi_bruto_R": rugi_bruto,
            "simbol_teratas": urut[0].symbol,
        }
    )

    # Retensi adalah rasio dua ekspektasi. Bila penyebutnya tidak positif,
    # rasio itu berubah tanda dan menjadi tidak dapat dibaca. Strategi yang
    # ekspektasinya nol atau negatif sudah gagal di tempat lain; di sini ia
    # dinyatakan tidak dapat dinilai, yang menurut aturan pokok berarti gagal.
    if eks is None or eks <= 0.0:
        hasil["sebab"] = (
            f"ekspektasi gabungan {eks} tidak positif sehingga retensi tidak bermakna"
        )
        return hasil

    k_drop = jumlah_drop_5persen(n)
    eks_drop1 = _ekspektasi(urut[1:])
    eks_dropk = _ekspektasi(urut[k_drop:]) if k_drop < n else None

    if eks_drop1 is None:
        hasil["sebab"] = "membuang simbol teratas tidak menyisakan perdagangan"
        return hasil

    eks_simbol = [k.total_R / k.trade for k in urut]
    bagian = [k.total_R / laba_bruto for k in urut if k.total_R > 0.0]
    hhi = sum(b * b for b in bagian)

    hasil.update(
        {
            "dapat_dinilai": True,
            "k_drop": k_drop,
            "ekspektasi_drop_1": eks_drop1,
            "ekspektasi_drop_k": eks_dropk,
            "retensi_drop_1": eks_drop1 / eks,
            "median_ekspektasi_simbol": median(eks_simbol),
            "porsi_bruto_teratas": urut[0].total_R / laba_bruto,
            "hhi_bruto": hhi,
            "setara_simbol": (1.0 / hhi) if hhi > 0.0 else None,
        }
    )
    return hasil


def tabel_jackknife(
    kontrib: Iterable[Kontribusi], k_maks: int = K_MAKS_JACKKNIFE
) -> list[dict]:
    """Buang k penyumbang teratas, laporkan ekspektasi dan retensinya.

    Baris k=0 adalah portofolio utuh, sehingga retensinya selalu 1 dan tabel
    ini dapat dibaca tanpa mengetahui angka pembandingnya dari tempat lain.
    """
    dipakai = _urut([k for k in kontrib if k.trade > 0])
    dasar = _ekspektasi(dipakai)
    baris: list[dict] = []
    for k in range(min(k_maks, len(dipakai) - 1) + 1):
        sisa = dipakai[k:]
        e = _ekspektasi(sisa)
        baris.append(
            {
                "k": k,
                "dibuang": None if k == 0 else dipakai[k - 1].symbol,
                "simbol_sisa": len(sisa),
                "trade": sum(x.trade for x in sisa),
                "total_R": round(sum(x.total_R for x in sisa), 4),
                "ekspektasi_R": None if e is None else round(e, 6),
                "retensi": (
                    None
                    if (e is None or dasar is None or dasar <= 0.0)
                    else round(e / dasar, 4)
                ),
            }
        )
    return baris


def gerbang_konsentrasi(
    kontrib: Iterable[Kontribusi],
    ambang_retensi: float = AMBANG_RETENSI_DROP_1,
    ambang_porsi_bruto: float = AMBANG_PORSI_BRUTO_TERATAS,
) -> Gerbang:
    """Keunggulan harus tersebar, bukan bertumpu pada beberapa simbol.

    Lima sub-uji, semuanya harus lulus. Empat pertama menanyakan hal yang sama
    dari sudut berbeda: apakah keunggulan bertahan tanpa penyumbang teratas.
    Yang kelima membatasi porsi penyumbang teratas terhadap laba **bruto**,
    dan penyebut bruto itu wajib, bukan pilihan gaya.

    ``nilai`` yang dilaporkan adalah retensi setelah satu simbol dibuang,
    karena itu satu-satunya sub-uji yang kontinu dan jaraknya terhadap ambang
    informatif. Keempat sub-uji lain masuk ke ``catatan`` beserta angkanya.
    """
    u = ukur_konsentrasi(kontrib)
    if not u["dapat_dinilai"]:
        return _gagal_tak_ternilai("konsentrasi", u["sebab"])

    sub = {
        "drop_1_positif": u["ekspektasi_drop_1"] > 0.0,
        "drop_5persen_positif": (
            u["ekspektasi_drop_k"] is not None and u["ekspektasi_drop_k"] > 0.0
        ),
        "retensi_drop_1": u["retensi_drop_1"] >= ambang_retensi,
        "median_simbol_positif": u["median_ekspektasi_simbol"] > 0.0,
        "porsi_bruto_teratas": u["porsi_bruto_teratas"] <= ambang_porsi_bruto,
    }
    gagal = [nama for nama in NAMA_SUB_UJI if not sub[nama]]

    dropk = u["ekspektasi_drop_k"]
    catatan = (
        f"{u['n_positif']} untung / {u['n_negatif']} rugi dari {u['n_simbol']} simbol; "
        f"drop-1 {u['ekspektasi_drop_1']:.5f}R (retensi {u['retensi_drop_1']:.4f}), "
        f"drop-{u['k_drop']} "
        f"{'tak ternilai' if dropk is None else format(dropk, '.5f') + 'R'}, "
        f"median simbol {u['median_ekspektasi_simbol']:+.5f}R, "
        f"porsi bruto teratas {u['porsi_bruto_teratas']:.4f} "
        f"({u['simbol_teratas']}), setara "
        f"{u['setara_simbol']:.1f} simbol"
    )
    if gagal:
        catatan += f"; sub-uji gagal: {', '.join(gagal)}"

    return Gerbang(
        nama="konsentrasi",
        lulus=not gagal,
        nilai=u["retensi_drop_1"],
        ambang=ambang_retensi,
        catatan=catatan,
    )
