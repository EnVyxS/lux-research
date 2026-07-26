"""Nilai p dari sebaran nol permutasi, pada satuan penarikan yang dinyatakan.

Modul ini menutup lubang yang ADR-024 buka dan ADR-029 rancang: ADR-015 bagian
4.4 menuntut **dua** syarat dalam satu kalimat — besaran ``SS − AS ≥ 0,020R``
**dan** ``p ≤ 0,05`` atas sedikitnya 300 ulangan permutasi sinyal — sementara
sampai hari ini hanya besarannya yang pernah dihitung. Yang dihitung di sini
adalah ``p`` itu.

MENGAPA MODUL SENDIRI, BUKAN DI DALAM ORKESTRATOR
-------------------------------------------------
Karena aritmetika yang hidup di dalam ``main`` tidak pernah benar-benar diuji,
dan itulah sebab dua cacat sebelumnya tidak berbunyi selama berbulan-bulan
(aturan 32). Perhitungan ``p`` juga jauh lebih murah daripada backtest yang
menghasilkan bahannya, sehingga ia wajib dapat dijalankan ulang tanpa membayar
ulang komputasinya (ADR-029 R6).

Modul daun: tidak mengimpor apa pun dari ``lux.backtest`` (aturan 8).

KOREKSI SATU, DAN MENGAPA IA BUKAN HIASAN
-----------------------------------------
``p`` dihitung sebagai ``(1 + cacah) / (1 + n)``, bukan ``cacah / n``. Akibatnya
``p`` **tidak pernah nol**. Itu disengaja: ``p = 0`` adalah klaim bahwa kejadian
sekuat itu mustahil, sedangkan 300 ulangan hanya sanggup mengatakan "tidak
terlihat dalam 300 tarikan". Batas terkecil yang dapat dibuktikan 300 tarikan
adalah ``1/301 ≈ 0,00332``, dan angka itulah yang akan tercetak alih-alih nol.
Ulangan yang teramati ikut dihitung sebagai satu tarikan yang sah dari sebaran
nol, sebab ia memang salah satunya.

SATUAN PENARIKAN WAJIB IKUT, SELALU
-----------------------------------
ADR-028 mematok satuan penarikan resmi pada **bulan kalender UTC**. Cacat kelas
kedua belas berbunyi tepat karena sebuah ambang statistik pernah dipatok tanpa
menyatakan satuannya, sehingga galatnya dapat mengecil hanya dengan menambah
simbol. Maka setiap keluaran modul ini membawa medan ``satuan``, dan keluaran
per perdagangan membawa ``taksiran_bawah: True`` beserta ``PEMBATAS``.

HIMPUNAN BULAN YANG TIDAK SAMA DITOLAK, BUKAN DISELARASKAN
----------------------------------------------------------
Bila sel teramati dan sebuah seed tidak memuat bulan yang sama, fungsi
berpasangan **melempar galat**. Menyelaraskan diam-diam — memotong ke irisan,
mengisi nol — berarti membandingkan dua himpunan berbeda tanpa jejak, dan
hasilnya tetap berupa angka yang tampak waras. Itu bentuk cacat yang paling
sulit terlihat.
"""

from __future__ import annotations

import math
from typing import Iterable, Mapping, Sequence

NAMA = "sebaran_nol"

# Kunci baris bulanan yang dihasilkan ``lux.analisis.periode.agregat_per_bulan``.
# Ditulis di sini sebagai harapan, bukan sebagai salinan aritmetika.
KUNCI_BULAN = ("periode", "trade", "total_R", "ekspektasi_R")

PEMBATAS = (
    "Nilai p di berkas ini sah HANYA pada satuan penarikan yang tertulis di "
    "medan `satuan`. Satuan resmi riset ini adalah BULAN kalender UTC "
    "(ADR-028); nilai p pada satuan perdagangan adalah TAKSIRAN BAWAH sebab "
    "perdagangan lintas simbol pada jendela yang bertumpang berkorelasi, "
    "sehingga ia hanya sah untuk MENJATUHKAN klaim dan tidak pernah untuk "
    "menegakkannya. p dihitung dengan koreksi (1 + cacah) / (1 + n) sehingga "
    "ia tidak pernah nol: 300 ulangan hanya sanggup membuktikan p turun sampai "
    "1/301, bukan sampai mustahil."
)


def _peta_bulan(bulan: Iterable[Mapping]) -> dict[str, Mapping]:
    """Baris bulanan menjadi peta ``periode -> baris``, dengan penolakan tegas.

    Periode ganda ditolak alih-alih ditimpa. Dua baris untuk bulan yang sama
    berarti bahan masukannya sudah rusak sebelum aritmetika dimulai, dan
    menimpanya akan menyembunyikan kerusakan itu di balik angka yang waras.
    """
    peta: dict[str, Mapping] = {}
    for b in bulan:
        p = str(b["periode"])
        if p in peta:
            raise ValueError(f"periode ganda pada masukan: {p}")
        if b.get("ekspektasi_R") is None:
            raise ValueError(f"periode {p} tanpa ekspektasi_R; ia tak dapat dipasangkan")
        peta[p] = b
    if not peta:
        raise ValueError("tidak ada satu pun baris bulanan")
    return peta


def rerata_bulanan(bulan: Iterable[Mapping]) -> float:
    """Rerata ekspektasi antar bulan, tiap bulan berbobot sama.

    Inilah satuan penarikan resmi ADR-028: yang ditarik adalah bulan, jadi
    bulan berisi 3.000 perdagangan tidak lebih berhak daripada bulan berisi 40.
    Pembobotan menurut jumlah perdagangan adalah pertanyaan yang berbeda, dan ia
    dijawab oleh fungsi di bawah — bukan oleh fungsi ini.
    """
    peta = _peta_bulan(bulan)
    nilai = [float(peta[k]["ekspektasi_R"]) for k in sorted(peta)]
    return float(math.fsum(nilai) / len(nilai))


def rerata_bulanan_berbobot(bulan: Iterable[Mapping]) -> float:
    """Ekspektasi gabungan lewat jalur bulanan, berbobot jumlah perdagangan.

    Ia dilaporkan **di samping** yang berbobot sama, bukan sebagai penggantinya.
    Keduanya menjawab pertanyaan berbeda, dan menyembunyikan salah satunya
    membuat pembaca tidak dapat melihat apakah kesimpulan bergantung pada
    pilihan pembobotan.
    """
    peta = _peta_bulan(bulan)
    trade = math.fsum(float(peta[k]["trade"]) for k in sorted(peta))
    if trade <= 0:
        raise ValueError("total perdagangan nol; rerata berbobot tak terdefinisi")
    total = math.fsum(float(peta[k]["total_R"]) for k in sorted(peta))
    return float(total / trade)


def selisih_bulanan(
    bulan_a: Iterable[Mapping], bulan_b: Iterable[Mapping]
) -> float:
    """Rerata selisih bulanan ``a − b`` atas bulan yang **sama**.

    Himpunan bulan yang berbeda melempar galat; lihat catatan modul. Perumusan
    berpasangan ini secara aljabar sama dengan selisih dua ``rerata_bulanan``
    ketika himpunan bulannya identik, dan kesamaan itu dituntut oleh pengujian
    supaya kelak tidak ada yang memilih perumusan yang angkanya lebih enak.
    """
    pa = _peta_bulan(bulan_a)
    pb = _peta_bulan(bulan_b)
    if set(pa) != set(pb):
        hilang = sorted(set(pa) - set(pb))
        asing = sorted(set(pb) - set(pa))
        raise ValueError(
            f"himpunan bulan tidak sama: hilang di b {hilang}, asing di b {asing}"
        )
    beda = [
        float(pa[k]["ekspektasi_R"]) - float(pb[k]["ekspektasi_R"])
        for k in sorted(pa)
    ]
    return float(math.fsum(beda) / len(beda))


def p_ekor_atas(teramati: float, nol: Sequence[float]) -> dict:
    """Pecahan tarikan nol yang mencapai atau melampaui nilai teramati.

    Perbandingannya ``>=`` dan bukan ``>``: tarikan yang sama persis dengan
    nilai teramati adalah bukti melawan, bukan bukti mendukung. Koreksi satu
    dijelaskan di catatan modul.
    """
    daftar = [float(x) for x in nol]
    if not daftar:
        raise ValueError("sebaran nol kosong; p tak dapat dihitung")
    cacah = sum(1 for x in daftar if x >= float(teramati))
    n = len(daftar)
    rerata = float(math.fsum(daftar) / n)
    if n > 1:
        ragam = math.fsum((x - rerata) ** 2 for x in daftar) / (n - 1)
        std = math.sqrt(ragam)
    else:
        std = None
    return {
        "teramati": float(teramati),
        "n": n,
        "cacah_ge": cacah,
        "p": (1 + cacah) / (1 + n),
        "p_terkecil_yang_mungkin": 1 / (1 + n),
        "nol_rerata": rerata,
        "nol_std": std,
        "nol_min": min(daftar),
        "nol_maks": max(daftar),
    }


def p_per_perdagangan(teramati: float, nol: Mapping[int, float]) -> dict:
    """``p`` pada satuan perdagangan — taksiran bawah, dan ditandai demikian.

    Ia dihitung dan dilaporkan justru supaya dapat dibandingkan terhadap versi
    bulanan. Jalur A sudah menunjukkan keduanya dapat berbeda lebih dari satu
    orde besaran (0,001100 lawan 0,365363), dan perbedaan itu sendiri adalah
    temuan tentang struktur data.
    """
    seed = sorted(nol)
    hasil = p_ekor_atas(teramati, [nol[s] for s in seed])
    return hasil | {
        "satuan": "perdagangan",
        "taksiran_bawah": True,
        "mengikat": False,
        "seed": seed,
        "pembatas": PEMBATAS,
    }


def p_bulanan(
    bulan_teramati: Iterable[Mapping],
    nol_bulanan: Mapping[int, Iterable[Mapping]],
) -> dict:
    """``p`` pada satuan bulan kalender UTC — inilah yang mengikat (ADR-028).

    Dua perumusan dihitung sekaligus dan keduanya dilaporkan:

    - **tak berpasangan**: sebaran nol dari ``rerata_bulanan`` tiap seed,
      dibandingkan terhadap ``rerata_bulanan`` sel teramati;
    - **berpasangan**: sebaran nol dari ``selisih_bulanan`` per bulan.

    Keduanya wajib menghasilkan ``p`` yang sama ketika himpunan bulannya
    identik, dan bila kelak keduanya berselisih, itu tanda cacat — bukan tanda
    bahwa salah satunya boleh dipilih.
    """
    if not nol_bulanan:
        raise ValueError("tidak ada satu pun seed pada sebaran nol")
    acuan = list(bulan_teramati)
    peta_acuan = _peta_bulan(acuan)
    rerata_acuan = rerata_bulanan(acuan)
    berbobot_acuan = rerata_bulanan_berbobot(acuan)

    seed = sorted(nol_bulanan)
    per_seed: list[dict] = []
    for s in seed:
        baris = list(nol_bulanan[s])
        # Melempar bila himpunan bulannya tidak sama. Itu disengaja.
        beda = selisih_bulanan(acuan, baris)
        per_seed.append(
            {
                "seed": s,
                "rerata_bulanan": rerata_bulanan(baris),
                "rerata_bulanan_berbobot": rerata_bulanan_berbobot(baris),
                "selisih_berpasangan": beda,
            }
        )

    tak_berpasangan = p_ekor_atas(
        rerata_acuan, [b["rerata_bulanan"] for b in per_seed]
    )
    berbobot = p_ekor_atas(
        berbobot_acuan, [b["rerata_bulanan_berbobot"] for b in per_seed]
    )
    # Berpasangan: seed mengalahkan sel teramati tepat ketika selisihnya <= 0.
    # Tandanya dibalik supaya ekor yang dihitung tetap ekor yang sama.
    berpasangan = p_ekor_atas(
        0.0, [-b["selisih_berpasangan"] for b in per_seed]
    )

    return {
        "satuan": "bulan",
        "taksiran_bawah": False,
        "mengikat": True,
        "n_bulan": len(peta_acuan),
        "seed": seed,
        "rerata_bulanan_teramati": rerata_acuan,
        "rerata_bulanan_berbobot_teramati": berbobot_acuan,
        "tak_berpasangan": tak_berpasangan,
        "berbobot": berbobot,
        "berpasangan": berpasangan,
        "sepakat": tak_berpasangan["p"] == berpasangan["p"],
        "per_seed": per_seed,
        "pembatas": PEMBATAS,
    }
