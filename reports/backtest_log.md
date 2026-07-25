# Log run backtest

Commit: `7db94434939cf793610e6285a76cb2635204c671`
Status langkah jalan: `success`

```
hipotesis H-001 terdaftar di hipotesis/H-001.json (sidik f172b1ba07f2)
ruang pencarian: 3 kombinasi
universe layak 447, diuji 40
  dibaca ohlcv_1h_shard00.parquet
  dibaca ohlcv_1h_shard01.parquet
  dibaca ohlcv_1h_shard02.parquet
  dibaca ohlcv_1h_shard03.parquet
  dibaca ohlcv_1h_shard04.parquet
  dibaca ohlcv_1h_shard05.parquet
  dibaca ohlcv_1h_shard06.parquet
  dibaca ohlcv_1h_shard07.parquet
40 simbol dimuat, 447 jadwal funding, 790 simbol dipindai untuk survivorship
  [5/40] 1000CHEEMSUSDT: 253 trade, 4s
  [10/40] 1000SATSUSDT: 401 trade, 5s
  [15/40] 1MBABYDOGEUSDT: 232 trade, 6s
  [20/40] ACXUSDT: 113 trade, 7s
  [25/40] AGLDUSDT: 470 trade, 8s
  [30/40] AIXBTUSDT: 249 trade, 8s
  [35/40] ALICEUSDT: 1125 trade, 10s
  [40/40] ANKRUSDT: 1077 trade, 11s
{
  "jumlah_simbol": 40,
  "jumlah_jendela": 349,
  "jendela_positif": 204,
  "jumlah_trade_luar_sampel": 18524,
  "total_R": 647.1102772677592,
  "ekspektasi_R": 0.03493361462253073
}
entri acak: nyata 0.07691R, p 0.009900990099009901, 30s
# Backtest H-001 — breakout Donchian 1 jam

> Penembusan Donchian pada penutupan bar 1 jam menghasilkan ekspektasi positif setelah fee, slippage, dan funding nyata, pada perp USDT yang lolos ambang kelayakan, dinilai hanya di luar sampel.

Sidik hipotesis `f172b1ba07f25717` · ruang 3 kombinasi · 40 simbol · 30.3s

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- ekspektasi 0.0349R < 0.05R

Gerbang gagal: forward_fill, invarian_risiko, checksum

## Hasil luar sampel

- Perdagangan: **18,524**
- Total R: **647.11**
```
