"""Pemeriksaan integritas OHLCV dan penyaringan universe yang layak diuji.

Modul ini memisahkan dua hal yang sering dicampur:

1. **Integritas** — apakah datanya secara internal konsisten. Pertanyaan ini
   punya jawaban benar atau salah, tidak bergantung selera.
2. **Kelayakan** — apakah sebuah instrumen cukup panjang riwayatnya dan cukup
   likuid untuk diuji. Ini keputusan, dan keputusannya diambil dari ambang di
   ``config/lux.yaml`` yang ditulis sebelum datanya dilihat.

Pemisahan itu penting. Membuang simbol karena datanya rusak adalah kebersihan;
membuang simbol karena hasilnya tidak menyenangkan adalah survivorship bias.
Hanya aturan tertulis yang membedakan keduanya, dan aturan itu harus mendahului
angkanya.

Seluruh fungsi di sini murni dan dapat diuji tanpa jaringan.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

STEP_MS = {"1m": 60_000, "5m": 300_000, "15m": 900_000, "1h": 3_600_000, "4h": 14_400_000}


@dataclass
class HasilPeriksa:
    """Rangkuman pelanggaran pada satu seri simbol.

    Pelanggaran dicatat sebagai jumlah, bukan sebagai bendera lulus/gagal saja.
    Laporan yang hanya berisi "gagal" tanpa besaran tidak bisa didiagnosis, dan
    angka yang tidak bisa didiagnosis tidak berguna.
    """

    symbol: str
    interval: str
    baris: int = 0
    duplikat_waktu: int = 0
    waktu_tidak_urut: int = 0
    tidak_selaras_kisi: int = 0
    celah: int = 0
    high_lebih_kecil: int = 0
    low_lebih_besar: int = 0
    harga_non_positif: int = 0
    volume_negatif: int = 0
    nilai_kosong: int = 0
    bar_datar: int = 0
    catatan: list[str] = field(default_factory=list)

    @property
    def pelanggaran_fatal(self) -> int:
        """Pelanggaran yang membuat seri tidak boleh dipakai sama sekali.

        Celah dan bar datar TIDAK termasuk. Celah adalah fakta pasar dan arsip:
        perdagangan memang pernah terhenti. Yang fatal adalah data yang
        bertentangan dengan dirinya sendiri, karena itu berarti pembacaan kita
        salah, bukan pasarnya.
        """
        return (
            self.duplikat_waktu
            + self.waktu_tidak_urut
            + self.tidak_selaras_kisi
            + self.high_lebih_kecil
            + self.low_lebih_besar
            + self.harga_non_positif
            + self.volume_negatif
            + self.nilai_kosong
        )

    @property
    def lulus(self) -> bool:
        return self.baris > 0 and self.pelanggaran_fatal == 0

    def sebagai_dict(self) -> dict:
        d = {
            k: v
            for k, v in self.__dict__.items()
            if not k.startswith("_")
        }
        d["pelanggaran_fatal"] = self.pelanggaran_fatal
        d["lulus"] = self.lulus
        return d


def periksa_seri(df: pd.DataFrame, symbol: str, interval: str) -> HasilPeriksa:
    """Memeriksa satu seri OHLCV terhadap invarian yang harus selalu benar.

    Invarian yang diperiksa dipilih karena masing-masing pernah dilanggar oleh
    data nyata atau oleh cacat kode, bukan karena kelengkapan teoretis.
    """
    h = HasilPeriksa(symbol=symbol, interval=interval, baris=len(df))
    if df.empty:
        h.catatan.append("seri kosong")
        return h

    step = STEP_MS.get(interval)
    if step is None:
        raise ValueError(f"interval tidak dikenal: {interval}")

    waktu = df["open_time"]

    h.duplikat_waktu = int(waktu.duplicated().sum())
    h.waktu_tidak_urut = int((waktu.diff().dropna() < 0).sum())

    # Setiap bar wajib jatuh tepat pada kelipatan intervalnya sejak epoch.
    # Pelanggaran di sini berarti stempel waktu salah satuan atau salah zona,
    # dan itu merusak segalanya yang dihitung sesudahnya.
    h.tidak_selaras_kisi = int((waktu % step != 0).sum())

    beda = waktu.diff().dropna()
    h.celah = int((beda != step).sum())

    for kolom in ("open", "high", "low", "close"):
        h.nilai_kosong += int(df[kolom].isna().sum())
        h.harga_non_positif += int((df[kolom] <= 0).sum())

    # Invarian OHLC: high adalah maksimum, low adalah minimum. Pelanggaran
    # berarti kolom tertukar, dan kolom tertukar menghasilkan backtest yang
    # tampak sangat menguntungkan karena stop tidak pernah kena.
    tertinggi = df[["open", "close"]].max(axis=1)
    terendah = df[["open", "close"]].min(axis=1)
    h.high_lebih_kecil = int((df["high"] < tertinggi).sum())
    h.low_lebih_besar = int((df["low"] > terendah).sum())

    if "volume" in df.columns:
        h.volume_negatif = int((df["volume"] < 0).sum())

    h.bar_datar = int((df["high"] == df["low"]).sum())

    return h


def rasio_bar_datar(h: HasilPeriksa) -> float:
    return h.bar_datar / h.baris if h.baris else 1.0


@dataclass(frozen=True)
class AmbangKelayakan:
    """Ambang inklusi universe, dibekukan sebelum data dilihat."""

    min_bar: int = 8760
    min_median_quote_volume_harian: float = 1_000_000.0
    maks_rasio_bar_datar: float = 0.30


def median_quote_volume_harian(df: pd.DataFrame, interval: str) -> float:
    """Median nilai transaksi per hari, bukan per bar.

    Diukur dalam mata uang quote supaya sebanding antar instrumen yang harga
    satuannya berbeda ribuan kali. Median dipakai, bukan rata-rata, karena satu
    hari peluncuran yang gila dapat mengangkat rata-rata instrumen yang sehari
    hari nyaris tidak diperdagangkan.
    """
    if df.empty or "quote_volume" not in df.columns:
        return 0.0
    per_hari = (df["open_time"] // 86_400_000).astype("int64")
    harian = df.groupby(per_hari)["quote_volume"].sum()
    return float(harian.median()) if len(harian) else 0.0


def nilai_kelayakan(
    h: HasilPeriksa,
    median_harian: float,
    ambang: AmbangKelayakan | None = None,
) -> tuple[bool, list[str]]:
    """Memutuskan apakah satu simbol layak masuk universe backtest.

    Mengembalikan alasan penolakan, bukan sekadar penilaian. Simbol yang ditolak
    tanpa alasan tercatat akan terlihat seperti simbol yang tidak pernah ada,
    dan itulah bentuk survivorship bias yang paling sulit dideteksi belakangan.
    """
    a = ambang or AmbangKelayakan()
    alasan: list[str] = []

    if not h.lulus:
        alasan.append(f"integritas gagal ({h.pelanggaran_fatal} pelanggaran fatal)")
    if h.baris < a.min_bar:
        alasan.append(f"riwayat terlalu pendek ({h.baris} < {a.min_bar} bar)")
    if median_harian < a.min_median_quote_volume_harian:
        alasan.append(
            f"likuiditas terlalu tipis (median {median_harian:,.0f} < "
            f"{a.min_median_quote_volume_harian:,.0f})"
        )
    rasio = rasio_bar_datar(h)
    if rasio > a.maks_rasio_bar_datar:
        alasan.append(f"terlalu banyak bar datar ({rasio:.2%} > {a.maks_rasio_bar_datar:.0%})")

    return (len(alasan) == 0, alasan)
