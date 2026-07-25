"""Walk-forward: memilih parameter di masa lalu, menilai di masa depan.

Satu-satunya angka yang boleh disebut sebagai bukti di modul ini adalah hasil
**di luar sampel**. Hasil di dalam sampel tetap dicatat, tetapi dicatat sebagai
catatan proses, bukan sebagai temuan. Alasannya bukan kehati-hatian berlebihan:
memilih parameter terbaik dari sekumpulan kandidat pada data yang sama dengan
data penilaiannya akan selalu menghasilkan angka bagus, bahkan ketika sinyalnya
murni derau. Semakin banyak kandidat dicoba, semakin bagus angka itu.

Tiga hal yang dijaga di sini:

**Embargo.** Antara ujung data latih dan awal data uji disisipkan jarak kosong.
Tanpa itu, indikator yang butuh pemanasan di awal jendela uji akan menghitung
dari bar yang baru saja dipakai untuk memilih parameter, dan kebocorannya kecil
tapi sistematis di setiap jendela.

**Pemanasan yang dibungkam.** Jendela uji boleh diberi bar tambahan di depannya
agar indikator sempat matang, tetapi sinyal pada bar-bar itu dipaksa nol.
Pemanasan hanya boleh memberi makan indikator, tidak boleh membuka posisi di
wilayah yang bukan wilayah penilaian.

**Jumlah kandidat dilaporkan.** Mencoba 200 kombinasi lalu melaporkan yang
terbaik bukan penemuan, melainkan pencarian. Angkanya disimpan bersama hasil
agar besarnya ruang pencarian tidak hilang dari ingatan saat hasilnya dinilai.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from lux.backtest.engine import Hasil, Konfig, Perdagangan, jalankan
from lux.funding_model import Jadwal


@dataclass(frozen=True)
class Jendela:
    """Batas indeks satu putaran walk-forward. Akhir bersifat eksklusif."""

    latih_awal: int
    latih_akhir: int
    uji_awal: int
    uji_akhir: int

    def __post_init__(self) -> None:
        if self.latih_awal < 0:
            raise ValueError("latih_awal tidak boleh negatif")
        if self.latih_akhir <= self.latih_awal:
            raise ValueError("jendela latih kosong")
        if self.uji_akhir <= self.uji_awal:
            raise ValueError("jendela uji kosong")
        if self.uji_awal < self.latih_akhir:
            raise ValueError("jendela uji tidak boleh mendahului akhir jendela latih")

    @property
    def panjang_latih(self) -> int:
        return self.latih_akhir - self.latih_awal

    @property
    def panjang_uji(self) -> int:
        return self.uji_akhir - self.uji_awal

    @property
    def embargo(self) -> int:
        return self.uji_awal - self.latih_akhir


def bagi_jendela(
    n_bar: int,
    panjang_latih: int,
    panjang_uji: int,
    embargo: int = 0,
    berjangkar: bool = False,
) -> list[Jendela]:
    """Bagi data menjadi deretan jendela latih-uji yang tidak saling bertindih.

    ``berjangkar`` membuat jendela latih tumbuh dari awal data alih-alih
    bergulir. Keduanya sah, tetapi jendela bergulir lebih jujur terhadap pasar
    yang rezimnya berubah, karena tidak memaksa parameter menjelaskan periode
    yang sudah tidak relevan.

    Sisa data di ujung yang tidak cukup untuk satu jendela penuh **dibuang**,
    tidak dipendekkan. Jendela uji yang lebih pendek akan menghasilkan jumlah
    perdagangan yang tidak sebanding dan diam-diam memberi bobot berbeda pada
    periode terakhir.
    """
    if panjang_latih < 1 or panjang_uji < 1:
        raise ValueError("panjang latih dan uji harus positif")
    if embargo < 0:
        raise ValueError("embargo tidak boleh negatif")

    jendela: list[Jendela] = []
    mulai = 0
    while True:
        latih_akhir = mulai + panjang_latih
        uji_awal = latih_akhir + embargo
        uji_akhir = uji_awal + panjang_uji
        if uji_akhir > n_bar:
            break
        jendela.append(
            Jendela(
                latih_awal=0 if berjangkar else mulai,
                latih_akhir=latih_akhir,
                uji_awal=uji_awal,
                uji_akhir=uji_akhir,
            )
        )
        mulai += panjang_uji
    return jendela


@dataclass
class HasilJendela:
    jendela: Jendela
    parameter: dict
    skor_latih: float
    hasil_uji: Hasil
    # Bingkai dan sinyal jendela uji disimpan agar uji permutasi dapat
    # dijalankan ulang atas wilayah penilaian yang sama persis. Tanpa ini,
    # gerbang entri acak harus menghitung ulang sinyal dan berisiko menguji
    # wilayah yang sedikit berbeda dari yang dinilai.
    bingkai_uji: pd.DataFrame | None = None
    sinyal_uji: np.ndarray | None = None


@dataclass
class HasilWalkForward:
    symbol: str
    per_jendela: list[HasilJendela] = field(default_factory=list)
    jumlah_kandidat: int = 0

    @property
    def perdagangan_luar_sampel(self) -> list[Perdagangan]:
        return [p for h in self.per_jendela for p in h.hasil_uji.perdagangan]

    def ringkas(self) -> dict:
        """Ringkasan yang hanya menghitung perdagangan di luar sampel.

        ``jumlah_kandidat`` dan ``parameter_per_jendela`` ikut dilaporkan agar
        dua hal tidak hilang saat hasil dibaca ulang kemudian: seberapa luas
        pencarian dilakukan, dan apakah parameter terpilih berubah-ubah tiap
        jendela. Parameter yang meloncat-loncat berarti tidak ada yang stabil
        untuk ditemukan, meskipun rata-rata hasilnya kebetulan positif.
        """
        trades = self.perdagangan_luar_sampel
        n = len(trades)
        dasar = {
            "symbol": self.symbol,
            "jumlah_jendela": len(self.per_jendela),
            "jumlah_kandidat": self.jumlah_kandidat,
            "jumlah_trade_luar_sampel": n,
            "parameter_per_jendela": [h.parameter for h in self.per_jendela],
        }
        if n == 0:
            dasar.update(
                {
                    "total_R": 0.0,
                    "ekspektasi_R": None,
                    "winrate": None,
                    "jendela_positif": 0,
                }
            )
            return dasar
        rs = np.array([p.R for p in trades], dtype="float64")
        positif = sum(
            1
            for h in self.per_jendela
            if sum(p.R for p in h.hasil_uji.perdagangan) > 0
        )
        dasar.update(
            {
                "total_R": float(rs.sum()),
                "ekspektasi_R": float(rs.mean()),
                "winrate": float((rs > 0).mean()),
                "jendela_positif": positif,
            }
        )
        return dasar


def _skor_baku(hasil: Hasil, min_trade: int) -> float:
    """Skor pemilihan parameter: ekspektasi R, dengan syarat jumlah minimum.

    Kandidat yang hanya menghasilkan sedikit perdagangan dibuang alih-alih
    diberi skor rendah. Ekspektasi dari tiga perdagangan bukan ekspektasi yang
    buruk, melainkan bukan ekspektasi sama sekali, dan bila diperlakukan sebagai
    angka ia akan menang melawan kandidat waras hanya karena kebetulan.
    """
    r = hasil.ringkas()
    if r["jumlah_trade"] < min_trade or r["ekspektasi_R"] is None:
        return float("-inf")
    return float(r["ekspektasi_R"])


def jalankan_walk_forward(
    df: pd.DataFrame,
    kandidat: Sequence[dict],
    buat_sinyal: Callable[[pd.DataFrame, dict], np.ndarray],
    panjang_latih: int,
    panjang_uji: int,
    embargo: int = 0,
    pemanasan: int = 0,
    berjangkar: bool = False,
    konfig: Konfig | None = None,
    jadwal: Jadwal | None = None,
    symbol: str = "",
    min_trade_latih: int = 10,
    simpan_bingkai: bool = False,
) -> HasilWalkForward:
    """Pilih parameter pada tiap jendela latih, nilai pada jendela uji.

    ``buat_sinyal`` menerima potongan bingkai dan satu set parameter, lalu
    mengembalikan sinyal sepanjang potongan itu. Fungsi ini **tidak pernah**
    melihat data di luar potongan yang diberikan, dan itulah yang membuat
    kebocoran antar jendela mustahil terjadi lewat jalur ini.

    ``pemanasan`` menambahkan bar di depan jendela uji untuk mematangkan
    indikator. Sinyal pada bar pemanasan dipaksa nol sebelum mesin dijalankan.
    """
    if not kandidat:
        raise ValueError("kandidat parameter kosong")
    if pemanasan < 0:
        raise ValueError("pemanasan tidak boleh negatif")

    k = konfig or Konfig()
    jendela = bagi_jendela(
        len(df), panjang_latih, panjang_uji, embargo=embargo, berjangkar=berjangkar
    )
    hasil = HasilWalkForward(symbol=symbol, jumlah_kandidat=len(kandidat))

    for j in jendela:
        latih = df.iloc[j.latih_awal : j.latih_akhir].reset_index(drop=True)
        terbaik: dict | None = None
        skor_terbaik = float("-inf")
        for params in kandidat:
            s = np.asarray(buat_sinyal(latih, params))
            if s.size != len(latih):
                raise ValueError("panjang sinyal latih tidak sama dengan potongan")
            skor = _skor_baku(
                jalankan(latih, s, k, jadwal=jadwal, symbol=symbol), min_trade_latih
            )
            if skor > skor_terbaik:
                skor_terbaik = skor
                terbaik = params

        if terbaik is None or skor_terbaik == float("-inf"):
            # Tidak ada kandidat yang layak di jendela ini. Jendela dilewati
            # tanpa perdagangan, bukan dipaksa memakai kandidat terbaik dari
            # yang sama-sama tidak layak.
            continue

        awal_potong = max(0, j.uji_awal - pemanasan)
        uji = df.iloc[awal_potong : j.uji_akhir].reset_index(drop=True)
        s_uji = np.asarray(buat_sinyal(uji, terbaik)).copy()
        if s_uji.size != len(uji):
            raise ValueError("panjang sinyal uji tidak sama dengan potongan")
        n_pemanasan = j.uji_awal - awal_potong
        if n_pemanasan > 0:
            # Pemanasan memberi makan indikator, bukan membuka posisi.
            s_uji[:n_pemanasan] = 0

        hasil.per_jendela.append(
            HasilJendela(
                jendela=j,
                parameter=dict(terbaik),
                skor_latih=skor_terbaik,
                hasil_uji=jalankan(uji, s_uji, k, jadwal=jadwal, symbol=symbol),
                bingkai_uji=uji if simpan_bingkai else None,
                sinyal_uji=s_uji if simpan_bingkai else None,
            )
        )

    return hasil
