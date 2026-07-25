# Log run backtest H-007 (ADR-007)

Commit: `1970f6bb6c64842e8779e1927680a9b64af7a195`
Status langkah jalan: `success`

```
titik impas kotor per imbalan:
  1.0R -> 0.5000
  2.0R -> 0.3333
  3.0R -> 0.2500
  4.0R -> 0.2000
universe layak 438, diuji 40
  dibaca ohlcv_1h_shard00.parquet
  dibaca ohlcv_1h_shard01.parquet
  dibaca ohlcv_1h_shard02.parquet
  dibaca ohlcv_1h_shard03.parquet
  dibaca ohlcv_1h_shard04.parquet
  dibaca ohlcv_1h_shard05.parquet
  dibaca ohlcv_1h_shard06.parquet
  dibaca ohlcv_1h_shard07.parquet
  dibaca ohlcv_1h_tail_shard00.parquet
  dibaca ohlcv_1h_tail_shard01.parquet
  dibaca ohlcv_1h_tail_shard02.parquet
  dibaca ohlcv_1h_tail_shard03.parquet
  akhir_per_simbol: 790 simbol dari reports/akhir_sejati.json
40 simbol dimuat, 447 jadwal funding, 790 simbol dipindai untuk survivorship
checksum: hilang 0, asing 0, tidak cocok 0

=== H-007 terdaftar di hipotesis/H-007.json (sidik 7f5e7aeeaa29, 12 kombinasi) ===
  [10/40] 1000SATSUSDT: 261 trade, 6s
  [20/40] ACXUSDT: 148 trade, 15s
  [30/40] AKROUSDT: 174 trade, 20s
  [40/40] ANTUSDT: 322 trade, 29s
{
  "jumlah_simbol": 40,
  "jumlah_jendela": 356,
  "jendela_positif": 199,
  "jumlah_trade_luar_sampel": 14962,
  "total_R": 605.1026635410902,
  "ekspektasi_R": 0.04044263223774163
}
alasan keluar: {'target': 4125, 'stop': 10276, 'akhir_data': 190, 'umur': 371}
parameter terpilih: {'{"imbalan_R": 4.0, "lookback": 100}': 83, '{"imbalan_R": 3.0, "lookback": 20}': 40, '{"imbalan_R": 2.0, "lookback": 100}': 11, '{"imbalan_R": 3.0, "lookback": 100}': 32, '{"imbalan_R": 4.0, "lookback": 20}': 66, '{"imbalan_R": 3.0, "lookback": 55}': 29, '{"imbalan_R": 4.0, "lookback": 55}': 45, '{"imbalan_R": 2.0, "lookback": 55}': 12, '{"imbalan_R": 1.0, "lookback": 20}': 11, '{"imbalan_R": 2.0, "lookback": 20}': 15, '{"imbalan_R": 1.0, "lookback": 100}': 7, '{"imbalan_R": 1.0, "lookback": 55}': 5}
entri acak: nyata 0.10810R, p 0.009900990099009901
# Titik impas — bongkaran seluruh hipotesis

Dengan stop 1R dan target sebesar imbalan, ekspektasi kotor adalah `p·imbalan − (1−p)` dan titik impas kotor adalah `1/(1+imbalan)`. Sebaran hasilnya terpotong di kedua sisi, sehingga tidak ada ekor panjang yang dapat menyelamatkan ekspektasi.

| Hipotesis | Mekanisme | Imbalan | Laju kena target | Kotor | Bersih | Seretan | Laju dibutuhkan |
|---|---|---|---|---|---|---|---|
| H-002 | Donchian + saringan carry | 2,0 | 0.36028 | +0.08084 | +0.03159 | 0.04925 | 0.36642 |
| H-004 | + ADX >= 30 | 2,0 | 0.34151 | +0.02453 | -0.01818 | 0.04271 | 0.36424 |
| H-005 | entri retest | 2,0 | 0.33755 | +0.01265 | -0.03571 | 0.04836 | 0.36612 |
| H-006 | sapuan likuiditas | 2,0 | 0.30122 | -0.09633 | -0.13449 | 0.03816 | 0.36272 |
| H-003 | pembalikan skor-z | 2,0 | 0.26326 | -0.21021 | -0.24782 | 0.03761 | 0.36254 |
| H-007 | imbalan dipilih WF | campuran | 0.28644 | -0.14068 | +0.04044 | -0.18113 | 0.28962 |

"Laju dibutuhkan" adalah laju kena target yang diperlukan untuk mencapai ekspektasi bersih 0,05R dengan seretan biaya yang sama.

```
