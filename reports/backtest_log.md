# Log run backtest keluarga ADR-006

Commit: `ae3df8c50bec77e5614f3cd5729a97b5708ac0bb`
Status langkah jalan: `success`

```
keluarga ADR-006: 3 hipotesis, ambang p entri acak 0.0167 (Bonferroni)
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

=== H-004 terdaftar di hipotesis/H-004.json (sidik 98d6a5e15b2c, 3 kombinasi) ===
  [10/40] 1000SATSUSDT: 178 trade, 2s
  [20/40] ACXUSDT: 70 trade, 5s
  [30/40] AKROUSDT: 59 trade, 7s
  [40/40] ANTUSDT: 150 trade, 11s
{
  "jumlah_simbol": 40,
  "jumlah_jendela": 356,
  "jendela_positif": 154,
  "jumlah_trade_luar_sampel": 7899,
  "total_R": -143.6347868008707,
  "ekspektasi_R": -0.018183920344457614
}
alasan keluar: {'target': 2659, 'stop': 5127, 'akhir_data': 66, 'umur': 47}
entri acak: nyata 0.06815R, p 0.009900990099009901

=== H-005 terdaftar di hipotesis/H-005.json (sidik 9c4b6324e795, 3 kombinasi) ===
  [10/40] 1000SATSUSDT: 234 trade, 4s
  [20/40] ACXUSDT: 136 trade, 10s
  [30/40] AKROUSDT: 124 trade, 13s
  [40/40] ANTUSDT: 220 trade, 19s
{
  "jumlah_simbol": 40,
  "jumlah_jendela": 356,
  "jendela_positif": 151,
  "jumlah_trade_luar_sampel": 12194,
  "total_R": -435.4910472730682,
  "ekspektasi_R": -0.03571355152313172
}
alasan keluar: {'target': 4057, 'stop': 7962, 'umur': 66, 'akhir_data': 109}
entri acak: nyata 0.00415R, p 0.039603960396039604

=== H-006 terdaftar di hipotesis/H-006.json (sidik e503a9a83318, 3 kombinasi) ===
  [10/40] 1000SATSUSDT: 328 trade, 2s
  [20/40] ACXUSDT: 210 trade, 4s
  [30/40] AKROUSDT: 182 trade, 6s
  [40/40] ANTUSDT: 469 trade, 8s
{
  "jumlah_simbol": 40,
  "jumlah_jendela": 356,
  "jendela_positif": 76,
  "jumlah_trade_luar_sampel": 20385,
  "total_R": -2741.510048211513,
  "ekspektasi_R": -0.13448663469274041
}
alasan keluar: {'target': 6032, 'stop': 13993, 'akhir_data': 210, 'umur': 150}
entri acak: nyata -0.14069R, p 1.0
# Keluarga ADR-006 — H-004, H-005, H-006

Tiga hipotesis dijalankan serentak pada kerangka eksekusi identik H-002. Ambang `p entri acak` diperketat ke **0.0167** (Bonferroni 0,05/3) sebelum hasil terlihat.

| Hipotesis | Mekanisme | Ekspektasi R | Total R | Trade | Jendela + | p acak | Putusan |
|---|---|---|---|---|---|---|---|
| H-004 | breakout + ADX ≥ 30 | -0.01818 | -143.63 | 7,899 | 154/356 | 0.0099 | DITOLAK |
| H-005 | entri retest (sniper) | -0.03571 | -435.49 | 12,194 | 151/356 | 0.0396 | DITOLAK |
| H-006 | sapuan likuiditas (SMC) | -0.13449 | -2741.51 | 20,385 | 76/356 | 1.0000 | DITOLAK |

## Alasan penolakan

**H-004** — breakout + ADX ≥ 30
- ekspektasi -0.0182R < 0.05R
- jendela positif 0.43 < 0.5

**H-005** — entri retest (sniper)
- Gerbang gagal: invarian_risiko
- ekspektasi -0.0357R < 0.05R
- p entri acak 0.0396 > 0.0167
- jendela positif 0.42 < 0.5

**H-006** — sapuan likuiditas (SMC)
- Gerbang gagal: entri_acak, invarian_risiko
- ekspektasi -0.1345R < 0.05R
- p entri acak 1.0000 > 0.0167
- jendela positif 0.21 < 0.5

## Pembanding tetap

| Hipotesis | Ekspektasi R | Putusan |
|---|---|---|
| H-001b Donchian | 0,03086 | DITOLAK |
| H-002 Donchian + saringan carry | 0,03159 | DITOLAK |
| H-003 pembalikan skor-z | −0,24782 | DITOLAK |

Angka pembanding disalin dari laporan yang sudah dikomit; ketiganya tidak dijalankan ulang.
```
