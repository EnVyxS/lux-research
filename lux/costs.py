"""Model biaya, dinyatakan dalam satuan R.

Satu R adalah jarak dari harga masuk ke stop. Menyatakan biaya dalam R, bukan
dalam persen harga, membuat satu pertanyaan bisa dijawab langsung: berapa besar
keunggulan yang harus dimiliki sebuah sinyal sebelum ia sekadar menutup ongkos.

Ini bukan detail akuntansi. Sebagian besar strategi yang tampak menguntungkan
sebelum biaya sebenarnya sedang memindahkan uang ke bursa, dan itu baru terlihat
ketika biaya dinyatakan dalam satuan yang sama dengan target keuntungan.

Dua komponen dipisahkan dengan sengaja:

- Biaya transaksi terjadi dua kali, saat masuk dan saat keluar.
- Funding hanya berlaku pada perpetual dan tumbuh seiring lamanya posisi
  dipegang. Strategi yang menahan posisi berhari-hari bisa habis oleh funding
  meski arah tebakannya benar.

BATAS PEMAKAIAN MODUL INI (penting, jangan dilanggar)
-----------------------------------------------------
``funding_dalam_R`` di modul ini memakai pembagi interval TETAP
(``ModelBiaya.funding_interval_jam``, bawaan 8 jam) dan satu ``funding_rate``
tunggal. Itu APROKSIMASI untuk penalaran di atas kertas: menghitung titik impas,
memeriksa apakah sebuah konfigurasi mustahil, dan menulis ambang sebelum
eksperimen.

Aproksimasi itu BUKAN jalur kritis backtest. Mesin backtest memakai jadwal
funding nyata dari arsip (``config/lux.yaml``:
``biaya.funding_dari_jadwal_nyata: true``), yaitu ``lux/funding.py`` dengan
``Jadwal`` bercap waktu sesungguhnya, karena interval funding di Binance tidak
konstan: 295 dari 447 simbol berjadwal funding pernah berada di lebih dari satu
rezim grid interval. Memakai pembagi 8 jam untuk simbol berinterval 4 jam akan
mengecilkan ongkos funding sekitar setengahnya, dan arah kesalahannya selalu
membuat strategi tampak lebih baik daripada kenyataan.

Ada dua fungsi bernama sama di repo ini, dan keduanya berbeda arti:

- ``lux.costs.funding_dalam_R``  -> aproksimasi interval tetap, hanya untuk
  perhitungan tangan dan pemeriksaan kelayakan sebelum eksperimen.
- ``lux.funding.funding_dalam_R`` -> jadwal nyata, dipakai mesin backtest.

Jangan pernah mengimpor yang pertama ke jalur eksekusi backtest.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelBiaya:
    """Parameter biaya yang dibekukan sebelum eksperimen dijalankan.

    ``funding_interval_jam`` adalah asumsi penyederhanaan, bukan fakta pasar.
    Interval funding sesungguhnya dibaca dari jadwal arsip oleh
    ``lux/funding.py``; lihat catatan BATAS PEMAKAIAN di docstring modul.
    """

    fee: float = 0.0005
    slippage: float = 0.0005
    funding_interval_jam: float = 8.0

    @property
    def biaya_satu_sisi(self) -> float:
        return self.fee + self.slippage

    @property
    def biaya_bolak_balik(self) -> float:
        return 2.0 * self.biaya_satu_sisi


def stop_frac(atr: float, harga: float, pengali: float = 2.0) -> float:
    """Jarak stop sebagai pecahan harga."""
    if harga <= 0:
        raise ValueError("harga harus positif")
    if atr < 0:
        raise ValueError("ATR tidak boleh negatif")
    return pengali * (atr / harga)


def biaya_dalam_R(stop_pecahan: float, model: ModelBiaya | None = None) -> float:
    """Biaya transaksi bolak-balik, dinyatakan dalam satuan R.

    Stop yang sempit membuat biaya membengkak secara relatif. Inilah alasan
    strategi frekuensi tinggi dengan stop ketat hampir selalu gagal setelah
    biaya diperhitungkan, betapa pun bagusnya kurva ekuitas kotornya.
    """
    if stop_pecahan <= 0:
        raise ValueError("stop_pecahan harus positif")
    m = model or ModelBiaya()
    return m.biaya_bolak_balik / stop_pecahan


def funding_dalam_R(
    funding_rate: float,
    jam_ditahan: float,
    stop_pecahan: float,
    arah: int = 1,
    model: ModelBiaya | None = None,
) -> float:
    """Ongkos funding selama posisi ditahan, dalam satuan R (APROKSIMASI).

    Fungsi ini membagi ``jam_ditahan`` dengan interval TETAP
    ``model.funding_interval_jam`` dan mengalikannya dengan satu
    ``funding_rate`` tunggal. Dua penyederhanaan sekaligus: interval dianggap
    konstan, dan rate dianggap tidak berubah selama posisi dipegang. Keduanya
    salah di data nyata.

    Pakai fungsi ini hanya untuk perhitungan kasar sebelum eksperimen. Ongkos
    funding yang masuk ke laporan backtest berasal dari ``lux/funding.py``
    memakai jadwal arsip, bukan dari sini. Bila suatu saat angka dari fungsi ini
    muncul di ``reports/``, itu cacat, bukan hasil.

    ``arah`` bernilai +1 untuk long dan -1 untuk short. Funding rate positif
    berarti long membayar short, jadi tandanya berbalik untuk short. Kesalahan
    tanda di sini menghasilkan strategi yang tampak untung justru karena
    dibayar oleh biaya yang seharusnya ia bayar.
    """
    if arah not in (1, -1):
        raise ValueError("arah harus +1 atau -1")
    if jam_ditahan < 0:
        raise ValueError("jam_ditahan tidak boleh negatif")
    if stop_pecahan <= 0:
        raise ValueError("stop_pecahan harus positif")
    m = model or ModelBiaya()
    periode = jam_ditahan / m.funding_interval_jam
    return arah * funding_rate * periode / stop_pecahan


def total_biaya_R(
    stop_pecahan: float,
    funding_rate: float = 0.0,
    jam_ditahan: float = 0.0,
    arah: int = 1,
    model: ModelBiaya | None = None,
) -> float:
    """Jumlah biaya transaksi dan funding aproksimatif, dalam R.

    Warisan sifat aproksimatif dari ``funding_dalam_R`` di modul ini berlaku
    penuh di sini juga.
    """
    return biaya_dalam_R(stop_pecahan, model) + funding_dalam_R(
        funding_rate, jam_ditahan, stop_pecahan, arah, model
    )


def winrate_impas(rasio_imbalan: float, biaya_R: float) -> float:
    """Tingkat kemenangan minimum agar strategi sekadar impas.

    Dengan target ``rasio_imbalan`` R dan kerugian 1 R, ekspektasi bersih nol
    tercapai saat p*(imbalan - biaya) = (1 - p)*(1 + biaya), sehingga
    p = (1 + biaya) / (imbalan + 1).

    Angka inilah pembanding yang jujur. Sebuah strategi dengan winrate 55%
    terdengar bagus sampai terlihat bahwa titik impasnya berada di 58%.

    Nilai kembalian dapat melebihi 1,0. Itu bukan kesalahan, melainkan cara
    rumus ini menyatakan bahwa strategi tersebut mustahil menguntungkan pada
    struktur biaya tersebut. Jangan pernah menjepitnya ke 1,0: menyembunyikan
    angka mustahil akan membuat konfigurasi yang tidak layak tampak wajar.
    """
    if rasio_imbalan <= 0:
        raise ValueError("rasio_imbalan harus positif")
    return (1.0 + biaya_R) / (rasio_imbalan + 1.0)


def layak_secara_biaya(rasio_imbalan: float, biaya_R: float) -> bool:
    """Apakah konfigurasi ini punya harapan sama sekali.

    Bila biaya sama besar atau lebih besar daripada target imbalan, kemenangan
    pun tidak menghasilkan apa pun, sehingga winrate 100% sekalipun hanya
    berujung nol atau minus. Ambang ini harus diperiksa SEBELUM backtest
    dijalankan, karena mesin backtest akan dengan patuh menghasilkan kurva
    ekuitas untuk konfigurasi yang secara aritmetika sudah mati.
    """
    if rasio_imbalan <= 0:
        raise ValueError("rasio_imbalan harus positif")
    return rasio_imbalan > biaya_R and winrate_impas(rasio_imbalan, biaya_R) < 1.0
