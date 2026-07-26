# Log run pemangkasan ekor datar 4h

Commit: `5296162d3787e1871d5c7dc2b7934c6c5ceca6ba`
Interval: `4h`
Status langkah jalan: `success`

```
interval 4h · min_panjang 6 bar (= 24 jam) · min_bar 2190 · maks_rasio 0.1
universe masukan: reports/universe_layak_4h.json
kandidat layak lama: 447
  dibaca ohlcv_4h_shard00.parquet
  dibaca ohlcv_4h_shard01.parquet
  dibaca ohlcv_4h_shard02.parquet
  dibaca ohlcv_4h_shard03.parquet
  dibaca ohlcv_4h_shard04.parquet
  dibaca ohlcv_4h_shard05.parquet
  dibaca ohlcv_4h_shard06.parquet
  dibaca ohlcv_4h_shard07.parquet
  dibaca ohlcv_4h_tail_shard00.parquet
  dibaca ohlcv_4h_tail_shard01.parquet
  dibaca ohlcv_4h_tail_shard02.parquet
  dibaca ohlcv_4h_tail_shard03.parquet
790 simbol dimuat dari aset
  ditulis: akhir_sejati_4h.json
  ditulis: universe_layak_v2_4h.json
  ditulis: potong_ekor_4h.json
  ditulis: potong_ekor_4h.md
# Pemangkasan ekor datar 4h

Pelaksanaan ADR-003. Aset tidak ditulis ulang; pemangkasan berlaku saat muat, dan tabel ini adalah catatan yang dapat diaudit atasnya.

- Ambang ekor: **6 bar** (= 24 jam) · lantai riwayat: **2,190 bar** · maks rasio datar: **0.1**

- Simbol dipindai (seluruh aset): **790**
- Simbol yang punya ekor datar: **141**
- Total bar dipangkas: **270,398**

- Kandidat layak lama: **447**
- Layak setelah ADR-003: **438**
- Ditolak: **9**
- Di antara kandidat, yang ekornya dipangkas: **62**

## Tiga puluh pemangkasan terbesar

| Simbol | Bar awal | Dipangkas | Bar sisa | Akhir sejati | Rasio sisa | Layak | Alasan |
|---|---|---|---|---|---|---|---|
| RENUSDT | 12,665 | 3,591 | 9,074 | 2024-12-03 | 0.0000 | ya | - |
| BLZUSDT | 12,821 | 3,471 | 9,350 | 2024-12-23 | 0.0000 | ya | - |
| FTMUSDT | 12,749 | 3,387 | 9,362 | 2025-01-06 | 0.0000 | ya | - |
| REEFUSDT | 11,873 | 3,291 | 8,582 | 2025-01-22 | 0.0000 | ya | - |
| OMGUSDT | 13,252 | 3,237 | 10,015 | 2025-01-31 | 0.0000 | ya | - |
| STMXUSDT | 11,705 | 3,111 | 8,594 | 2025-02-21 | 0.0000 | ya | - |
| LINAUSDT | 11,693 | 2,907 | 8,786 | 2025-03-27 | 0.0000 | ya | - |
| BALUSDT | 12,917 | 2,799 | 10,118 | 2025-04-14 | 0.0000 | ya | - |
| DEFIUSDT | 12,941 | 2,085 | 10,856 | 2025-08-11 | 0.0000 | ya | - |
| LEVERUSDT | 7,275 | 1,947 | 5,328 | 2025-09-03 | 0.0000 | ya | - |
| MKRUSDT | 13,001 | 1,917 | 11,084 | 2025-09-08 | 0.0000 | ya | - |
| ALPHAUSDT | 12,419 | 1,827 | 10,592 | 2025-09-23 | 0.0000 | ya | - |
| BAKEUSDT | 11,357 | 1,767 | 9,590 | 2025-10-03 | 0.0000 | ya | - |
| HIFIUSDT | 6,255 | 1,767 | 4,488 | 2025-10-03 | 0.0000 | ya | - |
| MYROUSDT | 5,230 | 1,515 | 3,715 | 2025-11-14 | 0.0000 | ya | - |
| FLMUSDT | 12,719 | 1,473 | 11,246 | 2025-11-21 | 0.0000 | ya | - |
| PERPUSDT | 7,419 | 1,473 | 5,946 | 2025-11-21 | 0.0000 | ya | - |
| TOKENUSDT | 5,967 | 1,389 | 4,578 | 2025-12-05 | 0.0000 | ya | - |
| FXSUSDT | 7,692 | 1,197 | 6,495 | 2026-01-06 | 0.0000 | ya | - |
| TOMOUSDT | 7,945 | 1,175 | 6,770 | 2023-11-14 | 0.0000 | ya | - |
| SXPUSDT | 12,850 | 1,071 | 11,779 | 2025-12-05 | 0.0000 | ya | - |
| CHESSUSDT | 4,169 | 1,011 | 3,158 | 2026-02-06 | 0.0000 | ya | - |
| DFUSDT | 3,430 | 1,011 | 2,419 | 2026-02-06 | 0.0000 | ya | - |
| GHSTUSDT | 4,017 | 1,011 | 3,006 | 2026-02-06 | 0.0000 | ya | - |
| NKNUSDT | 11,597 | 1,011 | 10,586 | 2026-02-06 | 0.0000 | ya | - |
| OMUSDT | 5,355 | 909 | 4,446 | 2026-02-23 | 0.0000 | ya | - |
| 1000WHYUSDT | 3,640 | 777 | 2,863 | 2026-03-17 | 0.0000 | ya | - |
| HOOKUSDT | 7,674 | 735 | 6,939 | 2026-03-24 | 0.0000 | ya | - |
| LRCUSDT | 12,599 | 735 | 11,864 | 2026-03-24 | 0.0000 | ya | - |
| NTRNUSDT | 5,901 | 735 | 5,166 | 2026-03-24 | 0.0000 | ya | - |

## Sebab penolakan

| Sebab | Jumlah |
|---|---|
| blok datar 117 bar | 1 |
| blok datar 2361 bar | 1 |
| blok datar 495 bar | 1 |
| blok datar 1953 bar | 1 |
| blok datar 597 bar | 1 |
| riwayat tersisa 1849 bar | 1 |
| blok datar 159 bar | 1 |
| blok datar 1587 bar | 1 |
| riwayat tersisa 2107 bar | 1 |

```
