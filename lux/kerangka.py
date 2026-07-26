"""Aritmetika kerangka waktu: satu hari itu berapa bar.

Modul ini ada karena satu pertanyaan sepele ternyata dijawab berbeda-beda di
tempat berbeda, dan setiap jawaban yang menyimpang berbentuk **ambang dalam
satuan bar yang tidak tahu intervalnya**. Tiga kali kelas cacat yang sama sudah
ditemukan di proyek ini:

- ``validate_run.muat_ambang`` membaca ``min_bar_1h`` tanpa memandang interval
  (diperbaiki ADR-017);
- ``potong_ekor.MIN_PANJANG`` bernilai 24, yang berarti satu hari pada 1h tetapi
  empat hari pada 4h (diperbaiki ADR-018);
- ``gerbang_forward_fill(maks_deret_datar=24)`` dan ``muat_ohlcv`` yang tidak
  meneruskan interval ke pemangkas ekor (ADR-019, yakni sebab modul ini ada).

Dua syarat rancangan yang tidak boleh dilanggar.

**Pertama, modul ini tidak mengimpor apa pun dari ``lux``.** Itu bukan soal
kerapian. Rantai ``gerbang → potong_ekor → diag_datar → run_wf → gerbang`` sudah
pernah melahirkan impor sirkular pada komit ``4b77617``, dan ``run_wf`` sampai
sekarang memakai impor lazy di dalam fungsi untuk memutusnya. Bila aritmetika ini
tinggal di ``potong_ekor``, maka ``gerbang.py`` yang membutuhkannya akan menutup
rantai itu kembali. Sebagai daun, modul ini dapat diimpor siapa pun tanpa risiko.

**Kedua, interval tak dikenal gagal keras.** Mengembalikan nilai bawaan ketika
intervalnya tidak dikenali adalah cara paling andal melahirkan cacat keempat dari
kelas yang sama: ambangnya akan tampak masuk akal, laporannya akan tampak
konsisten, dan tidak ada yang berbunyi.
"""

from __future__ import annotations

JAM_SEHARI = 24

# Interval yang dipahami pipeline, beserta panjangnya dalam jam. Menambah
# interval baru di sini otomatis menyebarkannya ke seluruh pemakai; itulah
# gunanya modul ini. Interval yang panjangnya tidak membagi sehari dengan rata
# ditolak oleh bar_per_hari, bukan dibulatkan diam-diam.
INTERVAL_JAM: dict[str, int] = {"1h": 1, "4h": 4}


def interval_dikenal() -> list[str]:
    """Daftar interval yang dikenal, terurut, untuk pesan galat dan pengujian."""
    return sorted(INTERVAL_JAM)


def jam_interval(interval: str) -> int:
    """Panjang satu bar dalam jam. Gagal keras bila intervalnya tak dikenal."""
    if interval not in INTERVAL_JAM:
        raise SystemExit(
            f"interval tidak dikenal: {interval!r}; "
            f"yang dikenal {interval_dikenal()}"
        )
    return INTERVAL_JAM[interval]


def bar_per_hari(interval: str) -> int:
    """Berapa bar yang menyusun satu hari penuh pada ``interval``.

    Ini satu-satunya tempat yang boleh menjawab pertanyaan itu. Setiap ambang
    yang dimaksudkan sebagai "satu hari" wajib memanggil fungsi ini alih-alih
    menuliskan angka bar, sebab angka bar yang ditulis tangan benar hanya untuk
    satu interval dan salah tanpa suara untuk interval lainnya.
    """
    jam = jam_interval(interval)
    if JAM_SEHARI % jam != 0:
        raise SystemExit(
            f"interval {interval!r} sepanjang {jam} jam tidak membagi "
            f"{JAM_SEHARI} jam dengan rata; ambang satu hari menjadi taksa"
        )
    return JAM_SEHARI // jam
