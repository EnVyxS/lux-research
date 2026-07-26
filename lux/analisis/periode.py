"""Agregat hasil menurut PERIODE WAKTU masuknya perdagangan (ADR-014 bagian 8).

Modul ini lahir dari satu kekurangan yang baru terlihat ketika H-012 disiapkan.
Pra-registrasi ADR-014 menetapkan kriteria utama H-012 sebagai **ekspektasi
berbobot perdagangan pada periode waktu terakhir yang dibekukan sebagai luar
sampel**, karena himpunan simbol tertahan sudah habis dan dimensi yang masih
bersih hanya waktu. Tetapi laporan backtest sampai H-011 **tidak memuat satu pun
stempel waktu perdagangan**: blok ``per_simbol`` hanya menyimpan jumlah
perdagangan dan total R per simbol, dan blok ``diagnosa_biaya`` hanya menyimpan
sepuluh perdagangan terburuk. Kriteria utama itu karena itu mustahil dihitung
dari laporan yang dikomit, dan angka yang mustahil dihitung ulang dari repo
adalah angka yang tidak dapat diaudit.

Maka agregat per bulan ditulis ke laporan, dan modul inilah yang menghitungnya.

MENGAPA WAKTU MASUK, BUKAN WAKTU KELUAR
---------------------------------------
Sebuah perdagangan dimiliki oleh periode tempat ia **dibuka**. Alasannya bukan
selera: keputusan yang diuji adalah keputusan masuk, dan itulah satu-satunya
saat ketika seluruh informasi yang dipakai strategi sudah tersedia. Memakai
waktu keluar akan memindahkan perdagangan ke periode yang belum ada ketika
keputusannya diambil.

Akibatnya ada rembesan yang wajib dinyatakan, bukan disembunyikan: perdagangan
yang dibuka sesaat sebelum batas periode dapat ditutup sesudahnya, sehingga
sebagian hasilnya secara harfiah terjadi di dalam periode tahan. Besarnya
rembesan itu terbatas oleh ``maks_umur_bar``, yaitu 168 bar satu jam = tujuh
hari, dan arahnya tidak diketahui — ia tidak dirancang untuk menguntungkan
hipotesis. Ia tetap dicatat karena batas yang tidak dinyatakan adalah batas yang
kelak disalahtafsirkan sebagai ketiadaan batas.

BULAN KALENDER UTC, BUKAN JENDELA BERGULIR
------------------------------------------
Pengelompokan memakai bulan kalender UTC. Bulan kalender tidak dapat digeser
sesudah hasil terlihat tanpa terlihat jelas di riwayat git, sedangkan "180 hari
terakhir" bergeser setiap kali data bertambah dan karena itu bukan batas yang
beku. Batas periode tahan dinyatakan sebagai tanggal, dan penilaiannya memakai
perbandingan ``>=`` terhadap stempel waktu masuk.

BATAS KEJUJURAN YANG WAJIB IKUT TERCETAK
----------------------------------------
Periode tahan ini **tidak** sebersih himpunan simbol tertahan sebelum H-011.
Hasil per simbol atas seluruh riwayat 438 simbol sudah dilihat di H-011, dan
riwayat itu memuat periode terakhir. Yang belum pernah dilihat adalah periode
terakhir **secara terpisah**. Jadi klaim yang sah hanyalah: angka ini belum
pernah dilihat sebagai angka sendiri. Klaim "data ini belum pernah disentuh"
tidak sah, dan menuliskannya akan menjadi kebohongan yang paling mudah dipercaya
karena ia menyenangkan.

Modul ini sengaja tidak mengimpor apa pun dari ``lux.backtest`` (aturan 8) dan
menerima perdagangan secara bebek: apa pun yang punya ``masuk_ms`` dan ``R``.
"""

from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Iterable, Sequence

NAMA = "periode"

# Kunci yang selalu ada di setiap baris agregat, supaya pembaca laporan tidak
# perlu menebak bentuknya.
KUNCI = ("periode", "trade", "total_R", "ekspektasi_R")


def ms_dari_tanggal(tanggal: str) -> int:
    """Ubah ``YYYY-MM-DD`` UTC menjadi stempel waktu milidetik.

    Sengaja hanya menerima tanggal, bukan waktu: batas periode yang membawa jam
    dan menit mengundang penggeseran halus yang sulit terlihat di diff.
    """
    t = datetime.strptime(tanggal, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(t.timestamp() * 1000)


def bulan_dari_ms(ms: int) -> str:
    """Bulan kalender UTC sebuah stempel waktu, sebagai ``YYYY-MM``."""
    t = datetime.fromtimestamp(int(ms) / 1000.0, tz=timezone.utc)
    return f"{t.year:04d}-{t.month:02d}"


def dari_perdagangan(perdagangan: Iterable) -> list[tuple[int, float]]:
    """Ambil ``(masuk_ms, R)`` dari perdagangan mesin, tanpa mengimpornya."""
    return [(int(p.masuk_ms), float(p.R)) for p in perdagangan]


def _agregat(pasangan: Sequence[tuple[int, float]]) -> dict:
    trade = len(pasangan)
    total = float(math.fsum(r for _, r in pasangan))
    return {
        "trade": trade,
        "total_R": total,
        "ekspektasi_R": (total / trade) if trade else None,
        "dapat_dinilai": trade > 0,
        "sebab": "" if trade else "tidak ada perdagangan pada periode ini",
    }


def agregat_per_bulan(pasangan: Iterable[tuple[int, float]]) -> list[dict]:
    """Ekspektasi berbobot perdagangan untuk setiap bulan kalender UTC.

    Berbobot perdagangan, bukan rerata dari rerata bulanan. Rerata dari rerata
    memberi bulan berisi 12 perdagangan bobot yang sama dengan bulan berisi
    3.000, dan bulan tersepi hampir selalu bulan paling ekstrem.

    ``math.fsum`` dipakai supaya penjumlahan puluhan ribu pecahan tidak
    kehilangan digit; penjumlahan pecahan tidak asosiatif, dan itu sudah pernah
    menjadi sumber pengujian yang menyala pada modul yang benar (aturan 23).
    """
    ember: dict[str, list[tuple[int, float]]] = {}
    for ms, r in pasangan:
        ember.setdefault(bulan_dari_ms(ms), []).append((ms, r))
    return [
        {"periode": bulan} | _agregat(ember[bulan]) for bulan in sorted(ember)
    ]


def agregat_sejak(
    pasangan: Iterable[tuple[int, float]], mulai_ms: int
) -> dict:
    """Agregat perdagangan yang MASUK pada atau sesudah ``mulai_ms``.

    Perbandingannya ``>=`` supaya perdagangan tepat di batas termasuk di dalam
    periode tahan. Titik batas harus dimiliki oleh salah satu sisi secara
    eksplisit; membiarkannya ambigu berarti dua perhitungan atas data yang sama
    dapat berbeda tanpa ada yang keliru.
    """
    isi = [(ms, r) for ms, r in pasangan if int(ms) >= int(mulai_ms)]
    return {"mulai_ms": int(mulai_ms)} | _agregat(isi)


def agregat_sebelum(
    pasangan: Iterable[tuple[int, float]], mulai_ms: int
) -> dict:
    """Agregat sisi lain dari batas, yaitu periode yang sudah pernah dilihat.

    Ia bukan hiasan. Tanpa pembanding di sisi seberang batas, angka periode
    tahan tidak dapat dibedakan antara "keunggulan tidak bertahan di waktu" dan
    "seluruh semesta memang berubah pada periode itu, termasuk di dalam sampel".
    Kedua tafsiran itu menuntut tindakan berbeda.
    """
    isi = [(ms, r) for ms, r in pasangan if int(ms) < int(mulai_ms)]
    return {"sebelum_ms": int(mulai_ms)} | _agregat(isi)


def bandingkan_batas(
    pasangan: Iterable[tuple[int, float]], mulai_ms: int
) -> dict:
    """Kedua sisi batas sekaligus, beserta pemeriksaan bahwa tak ada yang hilang.

    Pemeriksaan penjumlahan itu bukan paranoia berlebihan: saringan yang
    kehilangan baris di tengah jalan adalah cacat yang paling sulit terlihat,
    sebab hasilnya tetap berupa angka yang tampak waras.
    """
    isi = list(pasangan)
    tahan = agregat_sejak(isi, mulai_ms)
    lama = agregat_sebelum(isi, mulai_ms)
    return {
        "mulai_ms": int(mulai_ms),
        "tahan": tahan,
        "sebelum": lama,
        "utuh": (tahan["trade"] + lama["trade"]) == len(isi),
        "n_masuk": len(isi),
    }
