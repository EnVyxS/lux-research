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
ketidaktahuan; memilih stop berarti membayar untuk ketidaktahuan itu.

**Slippage selalu melawan posisi**, baik saat masuk maupun keluar.

**Funding ditagih dari jadwal nyata**, bukan dari kisi tetap. Lihat
``lux/funding_model.py``; kisi tetap delapan jam terbukti salah untuk 269 dari
447 simbol layak.

**Hanya satu posisi terbuka pada satu waktu.** Posisi bertumpuk membuat
ekuitas naik karena penambahan eksposur, bukan karena keunggulan sinyal.

**Posisi yang masih terbuka saat data habis ditutup dan dicatat**, dengan
alasan keluar ``akhir_data``. Versi pertama mesin ini diam-diam membuangnya,
dan cacat itu tertangkap oleh sebuah pengujian yang sebenarnya sedang menguji
hal lain. Membuang posisi terbuka bukan kelalaian netral: posisi yang belum
ditutup cenderung yang sedang merugi, karena yang menguntungkan lebih dulu
menyentuh target. Menghilangkannya berarti menghapus kerugian dari catatan.

**ADR-004 menambahkan dua saringan yang seluruhnya bawaan MATI.** Keduanya
hanya menyala bila diminta secara eksplisit lewat ``Konfig``:

- ``maks_umur_bar`` menutup posisi yang terlalu lama dipegang, pada pembukaan
  bar berikutnya. Pemeriksaan umur dilakukan **sebelum** stop dan target bar
  itu diuji, karena pembukaan bar mendahului pergerakan intrabar. Urutan
  sebaliknya akan memberi posisi satu bar gratis untuk menyentuh target.
- ``maks_carry_R`` membatalkan entri yang ongkos funding terproyeksinya
  melebihi ambang. Proyeksi hanya membaca masa lalu; lihat
  ``lux.funding_model.carry_terproyeksi_R``.

**ADR-008 menambahkan saringan ketiga, juga bawaan MATI:**

- ``maks_carry_realisasi_R`` menutup posisi yang ongkos funding **yang sudah
  benar-benar tertagih** melewati ambang. Berbeda dengan ``maks_carry_R`` yang
  menebak sekali di saat entri lalu tidak pernah menilai ulang, saringan ini
  tidak menebak apa pun: ia menjumlahkan penagihan yang sudah terjadi dan
  dinilai ulang pada pembukaan tiap bar. Saringan proyeksi terbukti tembus di
  H-001b, H-003, H-005, dan H-007 justru karena rate dapat melonjak setelah
  entri, dan proyeksi tidak punya cara mengetahuinya.

**ADR-014 menambahkan saringan keempat, juga bawaan MATI:**

- ``maks_biaya_masuk_R`` menolak entri yang biaya transaksi bolak-baliknya,
  dinyatakan dalam satuan R, melebihi ambang. Saringan ini menutup cacat
  terbesar yang pernah ditemukan riset ini: satuan R kehilangan artinya ketika
  jarak stop mendekati nol. Pada USDCUSDT rasio ATR terhadap harga praktis nol
  sehingga ``stop_frac`` mencapai 3,1984e-06, satu perdagangan mencatat biaya
  312,73R, dan gerbang ``invarian_risiko`` melaporkan -470,06R terhadap ambang
  -1,5R. Empat puluh simbol pertama secara alfabet tidak memuat satu pun
  pasangan semacam itu, jadi cacat ini laten sejak H-001b dan baru terbuka di
  H-011.

  Tiga hal yang disengaja pada saringan ini. Pertama, aritmetikanya **tidak**
  ditulis di sini melainkan diambil dari ``lux.degenerasi.entri_terlalu_mahal``,
  supaya lantai semesta dan pengaman mesin mustahil melenceng satu terhadap
  yang lain. Kedua, arah impornya satu arah: ``lux.degenerasi`` tidak mengimpor
  modul ini, sehingga tidak ada lingkaran impor yang baru terasa jauh di dalam
  run. Ketiga, penolakan **bukan perdagangan** dan karena itu tidak masuk
  histogram alasan keluar; jumlahnya dicatat di ``Hasil.entri_ditolak_biaya``
  agar sampai ke laporan sebagai alasannya sendiri alih-alih menghilang tanpa
  jejak. Entri yang ditolak karena carry dihitung terpisah, karena mencampur
  dua sebab penolakan membuat laporan berbohong tentang penyebabnya.

**ADR-016 menambahkan medan kelima, juga bawaan MATI:**

- ``stop_hormati_celah`` membuat stop diisi pada harga **terburuk** antara harga
  stop dan harga pembukaan bar. Tanpanya stop selalu terisi tepat di harga stop
  meski bar **membuka jauh melewatinya**, sehingga mesin ini mustahil melahirkan
  stop lebih buruk dari sekitar 1R ditambah biaya. Akibatnya gerbang
  ``invarian_risiko`` praktis tidak punya daya pada jalur stop dan hanya dapat
  dijatuhkan oleh ``umur``, ``carry``, dan ``akhir_data``, yaitu tiga jalur yang
  mengisi pada harga bar sungguhan. Itulah sebab satu-satunya pelanggar ambang
  di H-012, -21,3131R pada STGUSDT, muncul di jalur ``carry``: jalur itulah
  satu-satunya yang jujur terhadap celah harga.

  **Target sengaja tidak diperlakukan simetris.** Ia tetap terisi pada harga
  target walau bar membuka melewatinya, sebab celah yang menguntungkan adalah
  hadiah atas ketidaktahuan, persis yang dilarang oleh aturan "stop menang bila
  keduanya tersentuh".

**ADR-020 menambahkan medan keenam, dan bawaannya MENYALA:**

- ``pakai_target`` mematikan sisi target sepenuhnya ketika ia ``False``: tidak ada
  harga target yang dipasang dan ``kena_target`` tidak pernah dinilai, sehingga
  posisi hanya dapat keluar lewat ``stop``, ``umur``, ``carry``, dan
  ``akhir_data``. Medan ini ada karena sel "horizon tetap" pada H-013 (ADR-015
  bagian 4.1) mustahil dibuat tanpanya, dan karena jalan pintasnya — memberi
  ``imbalan_R`` nilai raksasa — bukan "tanpa target" melainkan target yang
  letaknya dipilih tanpa dasar, yang pada simbol yang bergerak ekstrem masih
  dapat tersentuh.

  **Arah bawaannya sengaja berlawanan dengan lima medan di atas.** Kelima medan
  itu bawaannya MATI karena masing-masing MENAMBAH saringan; medan ini bawaannya
  MENYALA karena ia MEMPERTAHANKAN perilaku yang sudah ada. Aturan "medan baru
  bawaannya tidak mengubah hasil lama" **tidak** berarti "bawaannya selalu
  ``False``", dan membacanya secara harfiah di sini justru akan mematikan target
  pada seluruh dua belas hipotesis. Jangan merapikannya menjadi ``False``.

  Dua hal yang wajib diketahui sebelum memakainya. Pertama, mematikan target
  bersama ``maks_umur_bar`` nol **ditolak keras**, sebab "horizon tetap tanpa
  horizon" akan berjalan dan hasilnya tetap tampak masuk akal — semua perdagangan
  keluar lewat ``stop`` dan ``akhir_data`` — sehingga tidak ada yang berbunyi.
  Kedua, sel tanpa target menutup hampir seluruh perdagangannya lewat ``umur``,
  dan ``umur`` mengisi pada harga bar sungguhan; sel itu karena itu **lebih
  rentan** menjatuhkan ``invarian_risiko`` bukan karena keluarnya lebih buruk,
  melainkan karena keluarnya lebih jujur.

Selama kelima nilai ADR-004/008/014/016 nol atau salah dan ``pakai_target``
menyala, mesin berperilaku persis seperti sebelum keenam ADR itu, dan itu dikunci
oleh pengujian, bukan diandaikan.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from lux.degenerasi import entri_terlalu_mahal
from lux.funding_model import (
    HARI_MS,
    Jadwal,
    carry_terproyeksi_R,
    funding_dalam_R,
)


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
    # ADR-004. Nol berarti mati. Jangan mengubah nilai bawaan ini: hasil H-001b
    # hanya dapat diulang selama mesin bawaannya tidak menyaring apa pun.
    maks_umur_bar: int = 0
    maks_carry_R: float = 0.0
    jendela_carry_hari: int = 30
    # ADR-008. Nol berarti mati, dengan alasan yang sama seperti di atas.
    # Medan ini sengaja diletakkan paling akhir supaya posisi argumen medan
    # lama tidak bergeser.
    maks_carry_realisasi_R: float = 0.0
    # ADR-014. Nol berarti mati, dan diletakkan paling akhir dengan alasan yang
    # sama: posisi argumen medan lama tidak boleh bergeser.
    maks_biaya_masuk_R: float = 0.0
    # ADR-016. False berarti mati, dan diletakkan paling akhir dengan alasan
    # yang sama. Menyalakannya MEMPERBURUK hasil; itu memang tujuannya.
    stop_hormati_celah: bool = False
    # ADR-020. True berarti MENYALA, yaitu perilaku lama. Arahnya berlawanan
    # dengan lima medan di atas dengan sengaja: medan ini mempertahankan
    # perilaku, tidak menambah saringan. Lihat docstring modul sebelum
    # "merapikannya" menjadi False.
    pakai_target: bool = True

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
        if self.maks_umur_bar < 0:
            raise ValueError("maks_umur_bar tidak boleh negatif")
        if self.maks_carry_R < 0:
            raise ValueError("maks_carry_R tidak boleh negatif")
        if self.jendela_carry_hari <= 0:
            raise ValueError("jendela_carry_hari harus positif")
        if self.maks_carry_realisasi_R < 0:
            raise ValueError("maks_carry_realisasi_R tidak boleh negatif")
        if self.maks_biaya_masuk_R < 0:
            raise ValueError("maks_biaya_masuk_R tidak boleh negatif")
        # ADR-020. "Horizon tetap tanpa horizon" akan berjalan tanpa keluhan dan
        # hasilnya tetap tampak masuk akal, sebab seluruh perdagangan keluar
        # lewat stop dan akhir_data. Karena itu ia ditolak di sini, bukan
        # diserahkan kepada pembaca laporan.
        if not self.pakai_target and self.maks_umur_bar <= 0:
            raise ValueError(
                "pakai_target mati menuntut maks_umur_bar positif; tanpa target "
                "dan tanpa batas umur, posisi hanya keluar lewat stop dan "
                "akhir_data sehingga tidak ada horizon yang diuji"
            )


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

        Perdagangan yang untung 100 dolar tidak berarti apa-apa sampai
        diketahui berapa yang dipertaruhkan untuk mendapatkannya.
        """
        risiko = self.jarak_stop * self.ukuran
        return self.laba / risiko if risiko > 0 else 0.0


@dataclass
class Hasil:
    symbol: str
    perdagangan: list[Perdagangan] = field(default_factory=list)
    ekuitas: np.ndarray = field(default_factory=lambda: np.array([]))
    waktu: np.ndarray = field(default_factory=lambda: np.array([]))
    # ADR-014. Entri yang ditolak pengaman biaya. Bukan perdagangan, jadi tidak
    # masuk histogram alasan keluar, tetapi wajib tercatat: saringan yang
    # membuang entri tanpa jejak adalah titik buta, sama seperti gerbang yang
    # hasilnya tidak pernah ditulis ke reports/ (aturan 10).
    entri_ditolak_biaya: int = 0

    @property
    def jumlah_trade(self) -> int:
        return len(self.perdagangan)

    def ringkas(self) -> dict:
        """Ringkasan yang selalu menyertakan biaya, bukan hanya laba."""
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
                "entri_ditolak_biaya": self.entri_ditolak_biaya,
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
            "entri_ditolak_biaya": self.entri_ditolak_biaya,
        }


def atr(
    high: np.ndarray, low: np.ndarray, close: np.ndarray, periode: int = 14
) -> np.ndarray:
    """Average True Range versi Wilder.

    Nilai pada indeks t hanya memakai bar sampai t, sehingga aman dipakai untuk
    keputusan pada penutupan bar t. Periode awal bernilai NaN dan bar tersebut
    tidak boleh diperdagangkan; mengisi NaN dengan nilai apa pun berarti
    menentukan ukuran posisi dari volatilitas yang belum diketahui.
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


def harga_stop_terisi(
    stop: float, pembukaan: float, arah: int, hormati_celah: bool
) -> float:
    """Harga pengisian stop, dengan atau tanpa menghormati celah harga (ADR-016).

    Aritmetikanya diletakkan di fungsi tingkat modul, bukan disisipkan di dalam
    ``jalankan``, supaya ia dapat diuji tanpa membangun bingkai bar lengkap.
    Aritmetika yang hanya hidup di dalam lingkaran besar adalah aritmetika yang
    tidak pernah benar-benar diuji (aturan 32).

    Ketika ``hormati_celah`` mati, hasilnya **persis** ``stop``, tanpa
    menyentuh ``pembukaan`` sama sekali.
    """
    if not hormati_celah:
        return float(stop)
    if arah == 1:
        return float(min(stop, pembukaan))
    return float(max(stop, pembukaan))


def _catat(
    symbol: str,
    arah: int,
    masuk_ms: int,
    harga_masuk: float,
    ukuran: float,
    jarak_stop: float,
    harga_keluar: float,
    keluar_ms: int,
    alasan: str,
    fee: float,
    jadwal: Jadwal | None,
) -> Perdagangan:
    kotor = arah * (harga_keluar - harga_masuk) * ukuran
    transaksi = fee * ukuran * (harga_masuk + harga_keluar)
    dana = 0.0
    if jadwal is not None:
        dana = arah * jadwal.jumlah_rate(masuk_ms, keluar_ms) * harga_masuk * ukuran
    return Perdagangan(
        symbol=symbol,
        arah=arah,
        masuk_ms=masuk_ms,
        keluar_ms=keluar_ms,
        harga_masuk=harga_masuk,
        harga_keluar=harga_keluar,
        ukuran=ukuran,
        jarak_stop=jarak_stop,
        alasan_keluar=alasan,
        biaya_transaksi=transaksi,
        biaya_funding=dana,
        laba_kotor=kotor,
    )


def _boleh_masuk(
    k: Konfig,
    jadwal: Jadwal | None,
    arah: int,
    masuk_ms: int,
    stop_pecahan: float,
    interval_ms: int,
) -> bool:
    """Saringan carry terproyeksi (ADR-004). Mati bila ``maks_carry_R`` nol.

    Bila saringan menyala tetapi jadwal funding tidak ada, entri **ditolak**.
    Menganggap simbol tanpa jadwal berbiaya nol adalah bentuk kelalaian yang
    menyamar sebagai kelulusan, dan justru pada saringan biaya kelalaian itu
    paling menguntungkan hasil.

    ADR-008 memakai alasan yang sama: pengaman carry keras juga mustahil
    dinilai tanpa jadwal, jadi entri ditolak alih-alih dibuka tanpa pengawasan.

    Pengaman biaya masuk ADR-014 **tidak** diletakkan di sini. Ia dinilai di
    pemanggil supaya penolakan karena biaya dapat dihitung terpisah dari
    penolakan karena carry; satu fungsi yang mengembalikan satu ``bool`` untuk
    dua sebab berbeda akan menghapus perbedaan itu dari laporan.
    """
    if k.maks_carry_realisasi_R > 0 and jadwal is None:
        return False
    if k.maks_carry_R <= 0:
        return True
    if k.maks_umur_bar <= 0:
        raise ValueError("saringan carry menuntut maks_umur_bar yang positif")
    if interval_ms <= 0:
        raise ValueError("jarak antar bar tidak diketahui; saringan carry tidak sah")
    if jadwal is None:
        return False
    proyeksi = carry_terproyeksi_R(
        jadwal,
        arah=arah,
        masuk_ms=masuk_ms,
        umur_ms=k.maks_umur_bar * interval_ms,
        stop_pecahan=stop_pecahan,
        jendela_ms=k.jendela_carry_hari * HARI_MS,
    )
    return proyeksi <= k.maks_carry_R


def carry_terealisasi_R(
    jadwal: Jadwal,
    arah: int,
    masuk_ms: int,
    sekarang_ms: int,
    harga_masuk: float,
    jarak_stop: float,
) -> float:
    """Ongkos funding yang SUDAH tertagih sampai ``sekarang_ms``, dalam satuan R.

    ADR-008. Tidak ada tebakan di sini: yang dijumlahkan adalah penagihan yang
    benar-benar terjadi. Nilai positif berarti posisi membayar.

    Aritmetikanya diserahkan ke ``lux.funding_model.funding_dalam_R`` alih-alih
    ditulis ulang. Dua implementasi dari besaran yang sama adalah cara paling
    andal melahirkan selisih tanda yang tidak terdeteksi siapa pun, dan pada
    besaran biaya selisih tanda selalu berpihak pada hasil yang lebih indah.
    """
    if harga_masuk <= 0:
        raise ValueError("harga_masuk harus positif")
    if jarak_stop <= 0:
        raise ValueError("jarak_stop harus positif")
    return funding_dalam_R(
        jadwal,
        masuk_ms=masuk_ms,
        keluar_ms=sekarang_ms,
        stop_pecahan=jarak_stop / harga_masuk,
        arah=arah,
    )


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

    ``sinyal[t]`` adalah keputusan pada **penutupan bar t**: +1 long, -1 short,
    0 diam. Eksekusinya terjadi pada **pembukaan bar t+1**. Sinyal pada bar
    terakhir diabaikan karena tidak ada bar berikutnya untuk mengeksekusinya.
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
    # Jarak antar bar diukur dari datanya sendiri, bukan dari nama interval.
    # Nama interval bisa berbohong; stempel waktu tidak.
    interval_ms = int(np.median(np.diff(waktu))) if n > 1 else 0
    ekuitas = np.empty(n, dtype="float64")
    modal = k.modal_awal
    perdagangan: list[Perdagangan] = []
    ditolak_biaya = 0

    arah = 0
    harga_masuk = 0.0
    masuk_ms = 0
    masuk_idx = 0
    ukuran = 0.0
    jarak_stop = 0.0
    stop = 0.0
    target = 0.0

    for t in range(n):
        # ADR-004: umur diperiksa lebih dulu karena pembukaan bar mendahului
        # pergerakan intrabar. Memeriksanya sesudah stop dan target akan
        # memberi posisi satu bar gratis untuk menyentuh target.
        if arah != 0 and k.maks_umur_bar > 0 and (t - masuk_idx) >= k.maks_umur_bar:
            p = _catat(
                symbol,
                arah,
                masuk_ms,
                harga_masuk,
                ukuran,
                jarak_stop,
                _harga_eksekusi(o[t], arah, False, k.slippage),
                int(waktu[t]),
                "umur",
                k.fee,
                jadwal,
            )
            perdagangan.append(p)
            modal += p.laba
            arah = 0

        # ADR-008: pengaman carry keras, dinilai pada pembukaan bar dari
        # penagihan yang sudah benar-benar terjadi. Ditempatkan SESUDAH
        # pemeriksaan umur supaya semantik ADR-004 tidak bergeser: bila
        # keduanya terpicu di bar yang sama, harga keluarnya sama sehingga
        # labanya identik dan hanya labelnya yang berbeda.
        if arah != 0 and k.maks_carry_realisasi_R > 0 and jadwal is not None:
            if (
                carry_terealisasi_R(
                    jadwal,
                    arah=arah,
                    masuk_ms=masuk_ms,
                    sekarang_ms=int(waktu[t]),
                    harga_masuk=harga_masuk,
                    jarak_stop=jarak_stop,
                )
                > k.maks_carry_realisasi_R
            ):
                p = _catat(
                    symbol,
                    arah,
                    masuk_ms,
                    harga_masuk,
                    ukuran,
                    jarak_stop,
                    _harga_eksekusi(o[t], arah, False, k.slippage),
                    int(waktu[t]),
                    "carry",
                    k.fee,
                    jadwal,
                )
                perdagangan.append(p)
                modal += p.laba
                arah = 0

        if arah != 0:
            kena_stop = l[t] <= stop if arah == 1 else h[t] >= stop
            # ADR-020: ketika target dimatikan, ia tidak pernah dinilai. Lapis
            # pertama pengamanannya adalah target bernilai NaN di bawah; lapis
            # kedua adalah medan ini. Satu lapis cukup secara logika, tetapi
            # perbandingan dengan harga target yang tertinggal dari entri
            # sebelumnya adalah kebocoran yang tidak akan berbunyi.
            if k.pakai_target:
                kena_target = h[t] >= target if arah == 1 else l[t] <= target
            else:
                kena_target = False
            if kena_stop or kena_target:
                # Stop menang bila keduanya tersentuh: urutan di dalam bar
                # tidak diketahui, dan ketidaktahuan tidak boleh berbuah laba.
                #
                # ADR-016: bila bar MEMBUKA sudah melewati stop, pesanan stop
                # di pasar sungguhan terisi pada pembukaan itu, bukan pada
                # harga stop. Target tidak diperlakukan simetris; lihat
                # docstring modul.
                if kena_stop:
                    harga = harga_stop_terisi(
                        stop, float(o[t]), arah, k.stop_hormati_celah
                    )
                else:
                    harga = target
                p = _catat(
                    symbol,
                    arah,
                    masuk_ms,
                    harga_masuk,
                    ukuran,
                    jarak_stop,
                    _harga_eksekusi(harga, arah, False, k.slippage),
                    int(waktu[t]),
                    "stop" if kena_stop else "target",
                    k.fee,
                    jadwal,
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
                        stop_pecahan = jarak / masuk
                        # ADR-014: pengaman biaya masuk. Dinilai SEBELUM
                        # saringan carry karena ia lebih murah dan karena
                        # sebabnya harus dapat dibedakan di laporan. Penolakan
                        # di sini bukan perdagangan.
                        if k.maks_biaya_masuk_R > 0 and entri_terlalu_mahal(
                            stop_pecahan, k.maks_biaya_masuk_R
                        ):
                            ditolak_biaya += 1
                        elif _boleh_masuk(
                            k, jadwal, s, int(waktu[t]), stop_pecahan, interval_ms
                        ):
                            arah = s
                            harga_masuk = masuk
                            masuk_ms = int(waktu[t])
                            masuk_idx = t
                            jarak_stop = jarak
                            ukuran = (modal * k.risiko_per_trade) / jarak
                            stop = masuk - s * jarak
                            # ADR-020: tanpa target, tidak ada harga target yang
                            # dipasang sama sekali. NaN dipilih alih-alih nilai
                            # jauh, supaya setiap perbandingan dengannya bernilai
                            # False dan tidak ada angka yang bisa tersentuh.
                            if k.pakai_target:
                                target = masuk + s * jarak * k.imbalan_R
                            else:
                                target = float("nan")

        if arah != 0:
            ekuitas[t] = modal + arah * (c[t] - harga_masuk) * ukuran
        else:
            ekuitas[t] = modal

    if arah != 0 and n > 0:
        # Posisi yang belum ditutup cenderung yang sedang merugi, karena yang
        # menguntungkan lebih dulu menyentuh target. Membuangnya berarti
        # menghapus kerugian dari catatan.
        p = _catat(
            symbol,
            arah,
            masuk_ms,
            harga_masuk,
            ukuran,
            jarak_stop,
            _harga_eksekusi(float(c[-1]), arah, False, k.slippage),
            int(waktu[-1]),
            "akhir_data",
            k.fee,
            jadwal,
        )
        perdagangan.append(p)
        modal += p.laba
        ekuitas[-1] = modal

    return Hasil(
        symbol=symbol,
        perdagangan=perdagangan,
        ekuitas=ekuitas,
        waktu=waktu,
        entri_ditolak_biaya=ditolak_biaya,
    )
