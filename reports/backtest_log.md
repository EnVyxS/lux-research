# Log run backtest

Commit: `5c797a29d3b7a8d2202c083fbe637950726edb32`
Status langkah jalan: `success`

```
hipotesis H-001b terdaftar di hipotesis/H-001b.json (sidik e458f4c82abf)
ruang pencarian: 3 kombinasi
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
  [5/40] 1000CHEEMSUSDT: 253 trade, 4s
  [10/40] 1000SATSUSDT: 401 trade, 5s
  [15/40] 1MBABYDOGEUSDT: 232 trade, 6s
  [20/40] ACXUSDT: 113 trade, 7s
  [25/40] AGTUSDT: 115 trade, 8s
  [30/40] AKROUSDT: 186 trade, 8s
  [35/40] ALPHAUSDT: 881 trade, 9s
  [40/40] ANTUSDT: 374 trade, 10s
{
  "jumlah_simbol": 40,
  "jumlah_jendela": 356,
  "jendela_positif": 208,
  "jumlah_trade_luar_sampel": 19093,
  "total_R": 589.1692004511272,
  "ekspektasi_R": 0.030857864162317453
}
biaya rerata: transaksi 0.03434066055484234R, funding 0.001446581590609118R, 1 trade berbiaya di atas 1R
entri acak: nyata 0.07385R, p 0.009900990099009901, 28s
# Backtest H-001b — breakout Donchian 1 jam (ADR-003)

> Penembusan Donchian pada penutupan bar 1 jam menghasilkan ekspektasi positif setelah fee, slippage, dan funding nyata, pada perp USDT yang lolos ambang kelayakan, dinilai hanya di luar sampel.

Sidik hipotesis `e458f4c82abf6735` · ruang 3 kombinasi · 40 simbol · 28.3s

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- ekspektasi 0.0309R < 0.05R

Gerbang gagal: invarian_risiko

## Hasil luar sampel

- Perdagangan: **19,093**
- Total R: **589.17**
```
