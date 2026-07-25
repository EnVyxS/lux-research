"""Mesin backtest: eksekusi, biaya, dan pencatatan perdagangan.

Mesin ini dibangun dengan satu kecurigaan tetap terhadap dirinya sendiri:
sebuah mesin backtest akan dengan patuh menggambar kurva ekuitas yang indah
untuk aturan yang mustahil dijalankan di pasar sungguhan. Karena itu setiap
keputusan yang bisa condong ke arah hasil yang lebih bagus dibuat condong ke
arah sebaliknya, dan ditulis di sini agar tidak diam-diam berubah.

**Sinyal diputuskan pada penutupan bar t, dieksekusi pada pembukaan bar t+1.**
Ini bukan preferensi gaya melainkan pencegahan lookahead secara struktural.
Selama eksekusi memakai harga dari bar yang sama dengan bar pengambilan
keputusan, tidak ada disiplin penulisan strategi yang bisa menyelamatkan
hasilnya, karena harga penutupan belum diketahui ketika keputusan diambil.

**Bila stop dan target sama-sama tersentuh di dalam satu bar, stop yang
dimenangkan.** Data OHLC tidak memuat urutan kejadian di dalam bar, jadi
urutannya tidak diketahui. Memilih target berarti memberi hadiah atas
ketidaktahuan; memilih stop berarti membayar untuk ketidaktahuan itu. Pilihan
kedua yang jujur. Pada strategi bertarget lebar, asumsi ini bisa memangkas
hasil beberapa persen, dan pemangkasan itu memang harus terjadi.

**Slippage selalu melawan posisi**, baik saat masuk maupun keluar. Bursa tidak
pernah memberi harga yang lebih baik dari yang diminta secara sistematis.

**Funding ditagih dari jadwal nyata**, bukan dari kisi tetap. Lihat
``lux/funding_model.py``; kisi tetap delapan jam terbukti salah untuk 269 dari
447 simbol layak.

**Hanya satu posisi terbuka pada satu waktu.** Posisi bertumpuk membuat
ekuitas naik karena penambahan eksposur, bukan karena keunggulan sinyal, dan
itu salah satu cara paling umum hasil backtest terlihat hebat tanpa sebab.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from lux.funding_model import Jadwal


@dataclass(frozen=True)
class Konfig:
    """Parameter yang dibekukan sebelum eksperimen dijalankan."""

    fee: float = 0.0005
    slippage: float = 0.0005
    atr_periode: int = 14
    atr_pengali_stop: float = 2.0
    risiko_per_trade: float = 0.005
    imbalan_R: float = 2.0
    modal_awal: float = 10_000.0
    izinkan_short: bool = True

    def __post_init__(self) -> None:
        if self.atr_periode < 2:
            raise ValueError("atr_periode minimal 2")
        if self.atr_pengali_stop <= 0:
            raise ValueError("atr_pengali_stop harus positif")
        if not 0 < self.risiko_per_trade < 1:
            raise ValueError("risiko_per_trade harus di antara 0 dan 1")
        if self.imbalan_R <= 0:
            raise ValueError("imbalan_R harus positif")
        if self.modal_awal <= 0:
            raise ValueError("modal_awal harus positif")


@dataclass(frozen=True)
class Perdagangan:
    symbol: str
    arah: int
    masuk_ms: int
    keluar_ms: int
    harga_masuk: float
    harga_keluar: float
    ukuran: float
    jarak_stop: float
    alasan_keluar: str
    biaya_transaksi: float
    biaya_funding: float
    laba_kotor: float

    @property
    def laba(self) -> float:
        return self.laba_kotor - self.biaya_transaksi - self.biaya_funding

    @property
    def R(self) -> float:
        """Hasil bersih dalam satuan risiko awal.

        Dinyatakan dalam R agar sebanding antar simbol dan antar tingkat
        volatilitas. Perdagangan yang untung 100 dolar tidak berarti apa-apa
        sampai diketahui berapa yang dipertaruhkan untuk mendapatkannya.
        """
        risiko = self.jarak_stop * self.ukuran
        return self.laba / risiko if risiko > 0 else 0.0


@dataclass
class Hasil:
    symbol: str
    perdagangan: list[Perdagangan] = field(default_factory=list)
    ekuitas: np.ndarray = field(default_factory=lambda: np.array([]))
    waktu: np.ndarray = field(default_factory=lambda: np.array([]))

    @property
    def jumlah_trade(self) -> int:
        return len(self.perdagangan)

    def ringkas(self) -> dict:
        """Ringkasan yang selalu menyertakan biaya, bukan hanya laba.

        Laba bersih tanpa total biaya di sebelahnya menyembunyikan strategi
        yang sesungguhnya sedang memindahkan uang ke bursa.
        """
        n = self.jumlah_trade
        if n == 0:
            return {
                "jumlah_trade": 0,
                "laba_bersih": 0.0,
                "total_R": 0.0,
                "winrate": None,
                "ekspektasi_R": None,
                "biaya_transaksi": 0.0,
                "biaya_funding": 0.0,
                "maks_drawdown": 0.0,
                "ekuitas_akhir": float(self.ekuitas[-1]) if self.ekuitas.size else 0.0,
            }
        rs = np.array([p.R for p in self.perdagangan], dtype="float64")
        menang = int((rs > 0).sum())
        puncak = np.maximum.accumulate(self.ekuitas)
        dd = (self.ekuitas - puncak) / puncak
        return {
            "jumlah_trade": n,
            "laba_bersih": float(sum(p.laba for p in self.perdagangan)),
            "total_R": float(rs.sum()),
            "winrate": menang / n,
            "ekspektasi_R": float(rs.mean()),
            "biaya_transaksi": float(sum(p.biaya_transaksi for p in self.perdagangan)),
            "biaya_funding": float(sum(p.biaya_funding for p in self.perdagangan)),
            "maks_drawdown": float(dd.min()),
            "ekuitas_akhir": float(self.ekuitas[-1]),
        }


def atr(
    high: np.ndarray, low: np.ndarray, close: np.ndarray, periode: int = 14
) -> np.ndarray:
    """Average True Range versi Wilder.

    Nilai pada indeks t hanya memakai bar sampai t, sehingga aman dipakai untuk
    keputusan pada penutupan bar t. Periode awal bernilai NaN dan bar tersebut
    tidak boleh diperdagangkan; mengisi NaN dengan nilai apa pun berarti
    memperdagangkan volatilitas yang belum diketahui.
    """
    n = close.size
    hasil = np.full(n, np.nan, dtype="float64")
    if n < periode + 1:
        return hasil
    tr = np.empty(n, dtype="float64")
    tr[0] = high[0] - low[0]
    sebelum = close[:-1]
    tr[1:] = np.maximum(
        high[1:] - low[1:],
        np.maximum(np.abs(high[1:] - sebelum), np.abs(low[1:] - sebelum)),
    )
    hasil[periode] = tr[1 : periode + 1].mean()
    for i in range(periode + 1, n):
        hasil[i] = (hasil[i - 1] * (periode - 1) + tr[i]) / periode
    return hasil


def _harga_eksekusi(harga: float, arah: int, masuk: bool, slippage: float) -> float:
    """Slippage selalu memperburuk harga, ke arah mana pun posisinya."""
    sisi = arah if masuk else -arah
    return harga * (1.0 + sisi * slippage)


def jalankan(
    df: pd.DataFrame,
    sinyal: np.ndarray,
    konfig: Konfig | None = None,
    jadwal: Jadwal | None = None,
    symbol: str = "",
) -> Hasil:
    """Jalankan satu backtest atas satu simbol.

    ``df`` wajib memuat kolom ``open_time``, ``open``, ``high``, ``low``,
    ``close``, terurut menaik tanpa duplikat.

    ``sinyal[t]`` adalah keputusan yang diambil pada **penutupan bar t**,
    bernilai +1 untuk long, -1 untuk short, 0 untuk diam. Eksekusinya terjadi
    pada **pembukaan bar t+1**. Sinyal pada bar terakhir diabaikan karena tidak
    ada bar berikutnya untuk mengeksekusinya, dan mengeksekusinya pada bar yang
    sama persis adalah bentuk lookahead yang paling sering lolos tanpa
    disadari.
    """
    k = konfig or Konfig()
    wajib = ("open_time", "open", "high", "low", "close")
    kurang = [c for c in wajib if c not in df.columns]
    if kurang:
        raise ValueError(f"kolom wajib hilang: {kurang}")
    if len(sinyal) != len(df):
        raise ValueError("panjang sinyal harus sama dengan jumlah bar")

    waktu = df["open_time"].to_numpy(dtype="int64")
    if np.any(np.diff(waktu) <= 0):
        raise ValueError("open_time harus menaik tanpa duplikat")

    o = df["open"].to_numpy(dtype="float64")
    h = df["high"].to_numpy(dtype="float64")
    l = df["low"].to_numpy(dtype="float64")
    c = df["close"].to_numpy(dtype="float64")
    a = atr(h, l, c, k.atr_periode)

    n = len(df)
    ekuitas = np.empty(n, dtype="float64")
    modal = k.modal_awal
    perdagangan: list[Perdagangan] = []

    arah = 0
    harga_masuk = 0.0
    masuk_ms = 0
    ukuran = 0.0
    jarak_stop = 0.0
    stop = 0.0
    target = 0.0

    for t in range(n):
        if arah != 0:
            kena_stop = l[t] <= stop if arah == 1 else h[t] >= stop
            kena_target = h[t] >= target if arah == 1 else l[t] <= target
            if kena_stop or kena_target:
                # Stop menang bila keduanya tersentuh: urutan di dalam bar
                # tidak diketahui, dan ketidaktahuan tidak boleh berbuah laba.
                harga = stop if kena_stop else target
                alasan = "stop" if kena_stop else "target"
                keluar = _harga_eksekusi(harga, arah, False, k.slippage)
                keluar_ms = int(waktu[t])
                kotor = arah * (keluar - harga_masuk) * ukuran
                transaksi = k.fee * ukuran * (harga_masuk + keluar)
                dana = 0.0
                if jadwal is not None:
                    dana = (
                        arah
                        * jadwal.jumlah_rate(masuk_ms, keluar_ms)
                        * harga_masuk
                        * ukuran
                    )
                p = Perdagangan(
                    symbol=symbol,
                    arah=arah,
                    masuk_ms=masuk_ms,
                    keluar_ms=keluar_ms,
                    harga_masuk=harga_masuk,
                    harga_keluar=keluar,
                    ukuran=ukuran,
                    jarak_stop=jarak_stop,
                    alasan_keluar=alasan,
                    biaya_transaksi=transaksi,
                    biaya_funding=dana,
                    laba_kotor=kotor,
                )
                perdagangan.append(p)
                modal += p.laba
                arah = 0

        if arah == 0 and t >= 1:
            s = int(sinyal[t - 1])
            if s != 0 and not (s == -1 and not k.izinkan_short):
                atr_t = a[t - 1]
                if np.isfinite(atr_t) and atr_t > 0:
                    jarak = k.atr_pengali_stop * atr_t
                    masuk = _harga_eksekusi(o[t], s, True, k.slippage)
                    if jarak > 0 and masuk > 0:
                        arah = s
                        harga_masuk = masuk
                        masuk_ms = int(waktu[t])
                        jarak_stop = jarak
                        ukuran = (modal * k.risiko_per_trade) / jarak
                        stop = masuk - s * jarak
                        target = masuk + s * jarak * k.imbalan_R

        if arah != 0:
            ekuitas[t] = modal + arah * (c[t] - harga_masuk) * ukuran
        else:
            ekuitas[t] = modal

    return Hasil(symbol=symbol, perdagangan=perdagangan, ekuitas=ekuitas, waktu=waktu)
