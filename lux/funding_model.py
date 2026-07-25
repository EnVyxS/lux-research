"""Penagihan funding dari jadwal nyata tiap simbol.

Model lama menagih funding dengan rumus ``rate × (jam_ditahan / 8)``. Data
membuktikan rumus itu salah untuk mayoritas universe: dari 447 simbol layak,
269 berkisi empat jam dan hanya 174 yang berkisi delapan jam, sementara **295
simbol hidup di lebih dari satu rezim kisi** sepanjang umurnya. Pembagi tetap
delapan jam akan menagih setengah dari yang seharusnya pada simbol berkisi
empat jam, dan karena funding bernilai positif pada 79,1% periode, kekurangan
tagihan itu langsung menjadi keuntungan palsu bagi strategi yang condong long.

Modul ini membuang asumsi kisi sepenuhnya. Funding tidak dihitung, melainkan
**dijumlahkan dari peristiwa penagihan yang benar-benar terjadi** di dalam
rentang posisi dipegang. Simbol yang berpindah dari delapan jam ke empat jam di
tengah riwayat tertagih dengan benar tanpa satu baris kode khusus, karena yang
dibaca adalah stempel waktunya sendiri.

Aturan batas ditetapkan di sini, bukan diserahkan pada kebetulan implementasi:
sebuah penagihan dibebankan bila stempelnya **lebih besar dari waktu masuk dan
tidak melebihi waktu keluar**. Masuk tepat pada detik penagihan berarti tidak
ikut membayar, karena posisi belum dipegang saat potret diambil. Keluar tepat
pada detik penagihan berarti tetap membayar. Pilihan ini konservatif terhadap
kepentingan strategi: bila keliru, ia menagih lebih, bukan kurang.

Jeda perdagangan tidak perlu diperlakukan khusus. Selama penghentian, bursa
tidak menerbitkan penagihan, sehingga jumlahnya nol dengan sendirinya. Itulah
keuntungan menjumlahkan peristiwa alih-alih mengalikan durasi.

ADR-004 menambahkan satu kemampuan lagi: **memproyeksikan** carry ke depan
untuk keperluan saringan entri. Proyeksi itu dipisahkan dengan tegas dari
penagihan sesungguhnya dan hanya boleh membaca masa lalu; lihat
``statistik_trailing`` dan ``carry_terproyeksi_R``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

HARI_MS = 86_400_000


@dataclass(frozen=True)
class Jadwal:
    """Riwayat penagihan funding satu simbol, terurut menaik.

    ``kumulatif`` disimpan agar penjumlahan rentang mana pun selesai dalam dua
    pencarian biner. Backtest memanggil ini jutaan kali, dan penjumlahan
    berulang atas irisan akan mendominasi waktu jalan.
    """

    waktu: np.ndarray
    rate: np.ndarray
    kumulatif: np.ndarray

    @classmethod
    def dari_frame(cls, df: pd.DataFrame) -> "Jadwal":
        d = df.sort_values("calc_time")
        waktu = d["calc_time"].to_numpy(dtype="int64")
        rate = d["last_funding_rate"].to_numpy(dtype="float64")
        kumulatif = np.concatenate([[0.0], np.cumsum(rate)])
        return cls(waktu=waktu, rate=rate, kumulatif=kumulatif)

    def __len__(self) -> int:
        return int(self.waktu.size)

    def _irisan(self, masuk_ms: int, keluar_ms: int) -> tuple[int, int]:
        if keluar_ms < masuk_ms:
            raise ValueError("waktu keluar mendahului waktu masuk")
        awal = int(np.searchsorted(self.waktu, masuk_ms, side="right"))
        akhir = int(np.searchsorted(self.waktu, keluar_ms, side="right"))
        return awal, akhir

    def jumlah_rate(self, masuk_ms: int, keluar_ms: int) -> float:
        """Total funding rate yang tertagih selama posisi dipegang.

        Tanda mengikuti konvensi bursa: nilai positif berarti long membayar.
        """
        awal, akhir = self._irisan(masuk_ms, keluar_ms)
        return float(self.kumulatif[akhir] - self.kumulatif[awal])

    def jumlah_penagihan(self, masuk_ms: int, keluar_ms: int) -> int:
        """Berapa kali funding ditagihkan selama posisi dipegang."""
        awal, akhir = self._irisan(masuk_ms, keluar_ms)
        return akhir - awal

    def statistik_trailing(
        self, sampai_ms: int, jendela_ms: int
    ) -> tuple[float, int]:
        """Rerata rate dan jumlah penagihan pada jendela yang BERAKHIR di ``sampai_ms``.

        Fungsi ini adalah satu-satunya jalan sah menuju proyeksi carry, dan
        bentuknya sengaja dibuat sehingga masa depan mustahil ikut terbaca:
        batas atas jendela adalah waktu masuk itu sendiri, tidak ada argumen
        yang dapat menggesernya ke depan.

        Jendela yang kosong mengembalikan ``(0.0, 0)``. Nol di sini berarti
        bursa tidak menerbitkan penagihan apa pun pada periode itu, bukan
        bahwa datanya hilang; pemanggil yang membutuhkan pembedaan itu dapat
        memeriksa jumlahnya.
        """
        if jendela_ms <= 0:
            raise ValueError("jendela_ms harus positif")
        mulai = sampai_ms - jendela_ms
        awal = int(np.searchsorted(self.waktu, mulai, side="right"))
        akhir = int(np.searchsorted(self.waktu, sampai_ms, side="right"))
        n = akhir - awal
        if n <= 0:
            return 0.0, 0
        total = float(self.kumulatif[akhir] - self.kumulatif[awal])
        return total / n, n


def muat_jadwal(direktori: str | Path) -> dict[str, Jadwal]:
    """Baca seluruh shard funding menjadi jadwal per simbol."""
    direktori = Path(direktori)
    berkas = sorted(direktori.glob("funding_shard*.parquet"))
    if not berkas:
        raise FileNotFoundError(f"tidak ada funding_shard*.parquet di {direktori}")
    df = pd.concat([pd.read_parquet(p) for p in berkas], ignore_index=True)
    return {
        str(s): Jadwal.dari_frame(bagian)
        for s, bagian in df.groupby("symbol", sort=True, observed=True)
    }


def funding_dalam_R(
    jadwal: Jadwal,
    masuk_ms: int,
    keluar_ms: int,
    stop_pecahan: float,
    arah: int = 1,
) -> float:
    """Ongkos funding satu posisi, dalam satuan R.

    ``arah`` +1 untuk long dan -1 untuk short. Nilai kembalian positif berarti
    biaya, negatif berarti posisi justru dibayar. Kesalahan tanda di sini
    menghasilkan strategi yang tampak untung justru karena menerima biaya yang
    seharusnya ia bayar, jadi tandanya diuji tersendiri.
    """
    if arah not in (1, -1):
        raise ValueError("arah harus +1 atau -1")
    if stop_pecahan <= 0:
        raise ValueError("stop_pecahan harus positif")
    return arah * jadwal.jumlah_rate(masuk_ms, keluar_ms) / stop_pecahan


def carry_terproyeksi_R(
    jadwal: Jadwal,
    arah: int,
    masuk_ms: int,
    umur_ms: int,
    stop_pecahan: float,
    jendela_ms: int = 30 * HARI_MS,
) -> float:
    """Perkiraan ongkos funding sepanjang umur maksimum posisi, dalam satuan R.

    ADR-004. Angka ini **bukan** biaya yang akan ditagih; ia hanya dipakai
    untuk memutuskan apakah sebuah entri layak dibuka. Perbedaannya penting:
    biaya sesungguhnya dijumlahkan dari peristiwa yang terjadi, sedangkan yang
    ini adalah tebakan yang dibuat sebelum peristiwanya ada.

    Tebakannya disusun dari dua besaran yang keduanya dibaca dari jendela masa
    lalu yang berakhir tepat di ``masuk_ms``: rerata rate dan kerapatan
    penagihan. Kerapatan ikut dipakai, bukan hanya rerata rate, karena simbol
    berkisi empat jam menagih dua kali lebih sering daripada simbol berkisi
    delapan jam pada rate yang sama persis. Mengabaikan kerapatan akan
    mengulang bentuk kesalahan yang membuat modul ini ditulis.

    Nilai positif berarti diperkirakan membayar, negatif berarti diperkirakan
    dibayar.
    """
    if arah not in (1, -1):
        raise ValueError("arah harus +1 atau -1")
    if stop_pecahan <= 0:
        raise ValueError("stop_pecahan harus positif")
    if umur_ms < 0:
        raise ValueError("umur_ms tidak boleh negatif")
    rerata, n = jadwal.statistik_trailing(masuk_ms, jendela_ms)
    if n == 0:
        return 0.0
    perkiraan_penagihan = n * (umur_ms / jendela_ms)
    return arah * rerata * perkiraan_penagihan / stop_pecahan


def ambil_jadwal(jadwal: dict[str, Jadwal], symbol: str) -> Jadwal:
    """Ambil jadwal sebuah simbol, atau tolak dengan keras.

    Simbol tanpa jadwal tidak boleh diperlakukan sebagai simbol berbiaya nol.
    Diam-diam menagih nol adalah cara paling halus memasukkan keuntungan palsu
    ke dalam hasil backtest, dan cacat semacam itu tidak meninggalkan jejak di
    kurva ekuitas. Seluruh 447 simbol layak sudah terbukti memiliki data
    funding, jadi ketiadaan jadwal berarti ada yang salah pada pemuatan, bukan
    pada pasarnya.
    """
    j = jadwal.get(symbol)
    if j is None or len(j) == 0:
        raise KeyError(f"tidak ada jadwal funding untuk {symbol}")
    return j
