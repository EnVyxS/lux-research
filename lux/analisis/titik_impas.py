"""Aritmetika titik impas untuk mesin stop/target.

Dengan stop 1R dan target sebesar ``imbalan`` R, hanya ada dua hasil yang
mungkin bagi perdagangan yang selesai: menang sebesar imbalan, atau kalah
sebesar 1. Karena itu ekspektasi kotornya sepenuhnya ditentukan oleh laju kena
target, dan sebaran hasilnya **terpotong di kedua sisi**.

Konsekuensi yang sempat terlewat dan kini dikunci di sini: pada mesin semacam
ini, "keunggulan berasal dari perdagangan berekor panjang" adalah pernyataan
yang mustahil benar. Tidak ada ekor. Yang ada hanya laju kena target terhadap
titik impas.

Seluruh fungsi di modul ini murni aritmetika atas angka yang sudah dilaporkan.
Tidak ada data pasar yang dibaca, dan tidak ada putusan yang dihasilkan.
"""

from __future__ import annotations

# Alasan keluar yang hasilnya TIDAK terpotong di 1R maupun di imbalan, sehingga
# tidak boleh ikut menentukan laju kena target. Daftar ini eksplisit supaya
# alasan keluar baru harus diputuskan secara sadar, bukan diam-diam masuk ke
# penyebut. ``carry`` ditambahkan oleh ADR-008.
ALASAN_TIDAK_SELESAI = ("umur", "akhir_data", "carry")


def titik_impas(imbalan: float) -> float:
    """Laju kena target minimum agar ekspektasi kotor nol.

    Turunan: p·imbalan − (1−p) = 0  →  p = 1 / (1 + imbalan).
    """
    if imbalan <= 0:
        raise ValueError("imbalan harus positif")
    return 1.0 / (1.0 + imbalan)


def laju_kena_target(alasan_keluar: dict[str, int]) -> float:
    """Porsi target terhadap perdagangan yang benar-benar selesai.

    Keluar karena ``umur``, ``akhir_data``, dan ``carry`` (ADR-008) sengaja
    **tidak** dihitung: hasil ketiganya tidak terpotong di 1R maupun di
    imbalan, sehingga memasukkannya akan merusak aritmetika dua hasil yang
    menjadi dasar seluruh modul ini. Lihat ``ALASAN_TIDAK_SELESAI``.
    """
    target = int(alasan_keluar.get("target", 0))
    stop = int(alasan_keluar.get("stop", 0))
    selesai = target + stop
    if selesai == 0:
        raise ValueError("tidak ada perdagangan yang selesai di target atau stop")
    return target / selesai


def ekspektasi_kotor(laju: float, imbalan: float) -> float:
    """Ekspektasi sebelum biaya, dalam satuan R."""
    if not 0.0 <= laju <= 1.0:
        raise ValueError("laju harus berada di antara 0 dan 1")
    if imbalan <= 0:
        raise ValueError("imbalan harus positif")
    return laju * imbalan - (1.0 - laju)


def seretan_tersirat(kotor: float, bersih: float) -> float:
    """Selisih antara ekspektasi kotor dan ekspektasi bersih yang dilaporkan.

    Besaran ini menyerap fee, slippage, funding, dan sumbangan perdagangan yang
    keluar karena umur, habisnya data, atau pengaman carry. Ia **bukan** biaya
    transaksi murni dan tidak boleh dikutip seolah-olah begitu.
    """
    return kotor - bersih


def laju_dibutuhkan(target_bersih: float, seretan: float, imbalan: float) -> float:
    """Laju kena target yang diperlukan untuk mencapai ekspektasi bersih tertentu.

    Turunan: p·imbalan − (1−p) − seretan = target_bersih.
    """
    if imbalan <= 0:
        raise ValueError("imbalan harus positif")
    return (target_bersih + seretan + 1.0) / (1.0 + imbalan)


def ringkas_laporan(
    alasan_keluar: dict[str, int],
    ekspektasi_bersih: float,
    imbalan: float = 2.0,
    target_bersih: float = 0.05,
) -> dict:
    """Bongkar satu laporan backtest menjadi aritmetika titik impasnya."""
    laju = laju_kena_target(alasan_keluar)
    kotor = ekspektasi_kotor(laju, imbalan)
    seretan = seretan_tersirat(kotor, ekspektasi_bersih)
    perlu = laju_dibutuhkan(target_bersih, seretan, imbalan)
    selesai = int(alasan_keluar.get("target", 0)) + int(alasan_keluar.get("stop", 0))
    return {
        "imbalan": imbalan,
        "titik_impas": titik_impas(imbalan),
        "laju_kena_target": laju,
        "ekspektasi_kotor": kotor,
        "ekspektasi_bersih": ekspektasi_bersih,
        "seretan_tersirat": seretan,
        "laju_dibutuhkan": perlu,
        "kekurangan_laju": perlu - laju,
        "pemenang_tambahan": round((perlu - laju) * selesai),
        "perdagangan_selesai": selesai,
    }
