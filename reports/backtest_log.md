# Log run backtest H-003

Commit: `cd943f84176ab572e83f36690cb70c1887b48eda`
Status langkah jalan: `success`

```
hipotesis H-003 terdaftar di hipotesis/H-003.json (sidik 3a1cdc867f61)
ruang pencarian: 3 kombinasi (jendela [24, 72, 168], ambang 2.0)
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
  [5/40] 1000CHEEMSUSDT: 472 trade, 4s
  [10/40] 1000SATSUSDT: 519 trade, 6s
  [15/40] 1MBABYDOGEUSDT: 413 trade, 8s
  [20/40] ACXUSDT: 318 trade, 9s
  [25/40] AGTUSDT: 106 trade, 11s
  [30/40] AKROUSDT: 256 trade, 11s
  [35/40] ALPHAUSDT: 1485 trade, 13s
  [40/40] ANTUSDT: 505 trade, 15s
{
  "jumlah_simbol": 40,
  "jumlah_jendela": 356,
  "jendela_positif": 25,
  "jumlah_trade_luar_sampel": 28959,
  "total_R": -7176.59924421273,
  "ekspektasi_R": -0.24781930467946856
}
biaya rerata: transaksi 0.03353019486624796R, funding -0.0017218206444440914R, 0 trade berbiaya di atas 1R
alasan keluar: {'target': 7503, 'stop': 20997, 'akhir_data': 258, 'umur': 201}
entri acak: nyata -0.26690R, p 1.0, 43s
# Backtest H-003 — pembalikan jangka pendek (ADR-005)

> Pembalikan jangka pendek — membeli penutupan yang jatuh dua simpangan baku di bawah rerata bergulir dan menjual yang melonjak dua simpangan baku di atasnya — menghasilkan ekspektasi positif setelah fee, slippage, dan funding nyata, pada kerangka eksekusi yang sama persis dengan H-002, dinilai hanya di luar sampel.

Sidik hipotesis `3a1cdc867f61bf67` · ruang 3 kombinasi · 40 simbol · 43.6s

Kerangka eksekusi identik H-002. Yang berbeda hanya sinyalnya, dan arahnya berlawanan.

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- ekspektasi -0.2478R < 0.05R
- p entri acak 1.0000 > 0.05
- jendela positif 0.07 < 0.5

Gerbang gagal: buy_and_hold, entri_acak, invarian_risiko

## Hasil luar sampel

- Perdagangan: **28,959**
- Total R: **-7176.60**
```
