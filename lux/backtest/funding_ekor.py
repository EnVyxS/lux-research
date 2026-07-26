"""Gerbang kesebelas: funding yang **sadar ekor** (ADR-011).

Gerbang ``funding`` yang sudah ada menilai total funding mutlak. Ia memberi
10.253,97 untuk H-008 dan 10.199,59 untuk H-009 — selisih setengah persen —
sementara porsi funding pada perdagangan terburuk berubah dari 46,7% menjadi
16,5% dan gerbang ``invarian_risiko`` berbalik dari gagal menjadi lulus. Gerbang
yang memberi jawaban sama pada dua keadaan yang bertolak belakang tidak memuat
informasi. Rerata funding H-009 adalah 0,000328R per perdagangan, sedangkan
perdagangan terburuk H-008 membayar 0,9228R, yaitu 2.813 kali rerata itu; tidak
ada agregat yang mampu melihat rasio semacam itu.

Modul ini berdiri terpisah dari ``gerbang.py`` dengan alasan yang sama seperti
``konsentrasi.py`` dan sudah dibayar sekali lewat cacat komit ``4b77617``: ia
mengimpor ``Gerbang`` dari sana, jadi impor balik akan menutup siklus.

Ambang ditetapkan di ADR-011 **sebelum berkas ini ditulis** dan mengikat mulai
H-010. Ia tidak diterapkan ke belakang, sebab angka H-008 dan H-009 sudah
saya lihat ketika ambang disusun. Ambang yang ditulis setelah melihat data
hanya boleh menghakimi data yang belum ada.

Turunan ambang porsi 0,35 berasal dari konstruksi, bukan dari selera.
Perdagangan yang mati di stop kehilangan sekitar 1,00R kotor dengan biaya
transaksi rerata 0,034R, dan pengaman ADR-009 mengizinkan carry terealisasi
sampai 0,25R, sehingga batas atas porsi yang sah adalah
``0,25 / (1,00 + 0,25 + 0,034) = 0,195``. Pengaman diperiksa pada batas bar,
jadi satu bar terakhir dapat menambah carry sebelum keluar terlaksana; 0,35
kira-kira 1,8 kali batas itu, cukup untuk menampung kelewatan satu bar dan
tidak cukup untuk menampung kebocoran.

Dua keputusan bentuk yang perlu diingat:

1. **Hanya perdagangan merugi masuk perhitungan porsi.** Porsi funding terhadap
   laba tidak punya arti; membaginya dengan nilai positif akan mengencerkan
   ekor justru pada portofolio yang banyak menang.
2. **Tidak ada perdagangan merugi berarti tidak dapat dinilai, dan tidak dapat
   dinilai berarti GAGAL.** Ini terasa berlebihan sampai diingat bahwa keadaan
   itu jauh lebih mungkin lahir dari daftar perdagangan yang salah disalurkan
   daripada dari strategi yang tidak pernah rugi.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from math import isfinite

from lux.backtest.gerbang import Gerbang, _gagal_tak_ternilai

# Ambang ADR-011. Konstanta, bukan parameter yang boleh dilombakan.
AMBANG_PORSI_FUNDING_EKOR = 0.35
AMBANG_FUNDING_MAKS_R = 0.50
AMBANG_PORSI_DI_ATAS_PENGAMAN = 0.005

# Ambang pengaman carry ADR-009. Disalin sebagai konstanta acuan, bukan untuk
# diubah di sini; sumber kebenarannya tetap config/lux.yaml dan run_h009.
PENGAMAN_CARRY_R = 0.25

# Banyaknya perdagangan terburuk yang membentuk "ekor". Sepuluh dipilih agar
# setara dengan blok diagnosa_biaya.terburuk yang sudah dikomit sejak H-007,
# sehingga angka gerbang dapat diperiksa tangan terhadap laporan lama.
K_EKOR = 10

NAMA = "funding_ekor"


@dataclass(frozen=True)
class TradeFunding:
    """Satu perdagangan, disaring menjadi dua angka yang dibutuhkan gerbang."""

    R: float
    funding_R: float


def dari_rincian(baris: Iterable[dict]) -> list[TradeFunding]:
    """Ubah keluaran ``rincian_R`` menjadi daftar ``TradeFunding``.

    Kunci yang hilang menimbulkan ``KeyError``, bukan nilai bawaan nol. Nilai
    bawaan nol pada kolom funding akan membuat gerbang ini lulus justru ketika
    funding lupa dihitung, yaitu cacat yang persis ingin dicegah.
    """
    keluar: list[TradeFunding] = []
    for b in baris:
        kurang = [k for k in ("R", "funding_R") if k not in b]
        if kurang:
            raise KeyError(
                "baris rincian wajib memuat kunci "
                + ", ".join(repr(k) for k in kurang)
            )
        keluar.append(TradeFunding(R=float(b["R"]), funding_R=float(b["funding_R"])))
    return keluar


def porsi_funding(t: TradeFunding) -> float | None:
    """Porsi funding terhadap total kerugian satu perdagangan.

    Mengembalikan ``None`` untuk perdagangan yang tidak merugi, sebab porsi
    terhadap laba tidak punya tafsiran. Rabat funding (nilai negatif) dihitung
    sebagai nol, bukan sebagai porsi negatif: gerbang ini mengukur seberapa
    besar funding merusak, dan funding yang membayar kita tidak merusak apa pun.
    """
    if t.R >= 0:
        return None
    if t.funding_R <= 0:
        return 0.0
    return t.funding_R / abs(t.R)


def _kosong(sebab: str, n_trade: int) -> dict:
    return {
        "n_trade": n_trade,
        "dapat_dinilai": False,
        "sebab": sebab,
        "n_rugi": 0,
        "k_ekor": 0,
        "porsi_funding_ekor_maks": None,
        "porsi_funding_ekor_rerata": None,
        "funding_maks_R": None,
        "funding_total_mutlak_R": None,
        "n_di_atas_pengaman": None,
        "porsi_di_atas_pengaman": None,
    }


def ukur_funding_ekor(
    trades: Iterable[TradeFunding], k_ekor: int = K_EKOR
) -> dict:
    """Hitung seluruh besaran ekor funding tanpa memberi putusan.

    Pengukuran dipisahkan dari putusan dengan sengaja. ``Gerbang`` hanya punya
    satu ``nilai``, dan gerbang berisi beberapa sub-uji yang melaporkan satu
    angka adalah gerbang yang menyembunyikan sebagian besar alasannya.
    """
    ts = list(trades)
    if not ts:
        return _kosong("tidak ada perdagangan", 0)
    if any(not isfinite(t.R) or not isfinite(t.funding_R) for t in ts):
        return _kosong("nilai R atau funding tidak terhingga", len(ts))

    rugi = [t for t in ts if t.R < 0]
    if not rugi:
        return _kosong("tidak ada perdagangan merugi untuk menilai porsi ekor", len(ts))

    ekor = sorted(rugi, key=lambda t: t.R)[: max(1, k_ekor)]
    porsi = [p for p in (porsi_funding(t) for t in ekor) if p is not None]

    n_atas = sum(1 for t in ts if t.funding_R > PENGAMAN_CARRY_R)
    return {
        "n_trade": len(ts),
        "dapat_dinilai": True,
        "sebab": "",
        "n_rugi": len(rugi),
        "k_ekor": len(ekor),
        "porsi_funding_ekor_maks": max(porsi),
        "porsi_funding_ekor_rerata": sum(porsi) / len(porsi),
        "funding_maks_R": max(t.funding_R for t in ts),
        "funding_total_mutlak_R": sum(abs(t.funding_R) for t in ts),
        "n_di_atas_pengaman": n_atas,
        "porsi_di_atas_pengaman": n_atas / len(ts),
    }


def gerbang_funding_ekor(
    trades: Iterable[TradeFunding],
    jadwal_dimuat: bool,
    ambang_porsi: float = AMBANG_PORSI_FUNDING_EKOR,
    ambang_maks: float = AMBANG_FUNDING_MAKS_R,
    ambang_porsi_pengaman: float = AMBANG_PORSI_DI_ATAS_PENGAMAN,
) -> Gerbang:
    """Gerbang kesebelas. Empat sub-uji, semuanya harus lulus.

    ``nilai`` yang dilaporkan adalah ``porsi_funding_ekor_maks``, karena hanya
    besaran itu yang memisahkan H-008 dari H-009. Nama sub-uji yang gagal ikut
    ditulis ke ``catatan`` agar pengujian dapat memastikan **yang mana** yang
    jatuh, bukan sekadar bahwa ada yang jatuh.
    """
    if not jadwal_dimuat:
        return _gagal_tak_ternilai(NAMA, "jadwal funding tidak dimuat")

    u = ukur_funding_ekor(trades)
    if not u["dapat_dinilai"]:
        return _gagal_tak_ternilai(NAMA, u["sebab"])

    gagal: list[str] = []
    if u["porsi_funding_ekor_maks"] > ambang_porsi:
        gagal.append("porsi_funding_ekor_maks")
    if u["funding_maks_R"] > ambang_maks:
        gagal.append("funding_maks_R")
    if u["porsi_di_atas_pengaman"] > ambang_porsi_pengaman:
        gagal.append("porsi_trade_di_atas_pengaman")

    catatan = (
        f"porsi ekor maks {u['porsi_funding_ekor_maks']:.4f} "
        f"(rerata {u['porsi_funding_ekor_rerata']:.4f} atas {u['k_ekor']} terburuk), "
        f"funding maks {u['funding_maks_R']:.4f}R, "
        f"{u['n_di_atas_pengaman']} dari {u['n_trade']} trade di atas pengaman "
        f"({u['porsi_di_atas_pengaman']:.5f})"
    )
    if gagal:
        catatan = catatan + "; gagal: " + ", ".join(gagal)

    return Gerbang(
        nama=NAMA,
        lulus=not gagal,
        nilai=u["porsi_funding_ekor_maks"],
        ambang=ambang_porsi,
        catatan=catatan,
    )


def tabel_ekor_funding(
    trades: Iterable[TradeFunding], k_ekor: int = K_EKOR
) -> list[dict]:
    """Tabel sepuluh perdagangan merugi terburuk beserta porsi funding-nya.

    Dipakai runner untuk menulis bagian markdown. Angka yang tidak dapat
    diperiksa tangan terhadap laporan lama tidak berguna, jadi bentuknya
    disengaja mirip blok ``diagnosa_biaya.terburuk``.
    """
    rugi = sorted((t for t in trades if t.R < 0), key=lambda t: t.R)
    baris: list[dict] = []
    for i, t in enumerate(rugi[: max(1, k_ekor)], start=1):
        p = porsi_funding(t)
        baris.append(
            {
                "peringkat": i,
                "R": round(t.R, 4),
                "funding_R": round(t.funding_R, 4),
                "porsi_funding": None if p is None else round(p, 4),
            }
        )
    return baris
