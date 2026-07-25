# Log run backtest H-002

Commit: `ee1f705c18b0c4b414e1b1bd6ec114afd36f2a9f`
Status langkah jalan: `success`

```
hipotesis H-002 terdaftar di hipotesis/H-002.json (sidik 16fb57692a6f)
ruang pencarian: 3 kombinasi (umur maks 168 bar, carry maks 0.25R, jendela 30 hari)
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
  [10/40] 1000SATSUSDT: 378 trade, 5s
  [15/40] 1MBABYDOGEUSDT: 232 trade, 7s
  [20/40] ACXUSDT: 162 trade, 8s
  [25/40] AGTUSDT: 102 trade, 9s
  [30/40] AKROUSDT: 217 trade, 9s
  [35/40] ALPHAUSDT: 879 trade, 10s
  [40/40] ANTUSDT: 373 trade, 11s
{
  "jumlah_simbol": 40,
  "jumlah_jendela": 356,
  "jendela_positif": 212,
  "jumlah_trade_luar_sampel": 18883,
  "total_R": 596.4426936993348,
  "ekspektasi_R": 0.03158622537199252
}
biaya rerata: transaksi 0.034534421301562764R, funding 0.000536020846484891R, 0 trade berbiaya di atas 1R
alasan keluar: {'target': 6707, 'stop': 11909, 'akhir_data': 164, 'umur': 103}
entri acak: nyata 0.07392R, p 0.009900990099009901, 32s
# Backtest H-002 — batas umur posisi dan saringan carry (ADR-004)

> Penembusan Donchian pada penutupan bar 1 jam menghasilkan ekspektasi positif setelah fee, slippage, dan funding nyata, bila posisi dibatasi umurnya dan entri dengan carry funding terproyeksi berlebihan ditolak, pada perp USDT yang lolos ambang kelayakan, dinilai hanya di luar sampel.

Sidik hipotesis `16fb57692a6f0888` · ruang 3 kombinasi · 40 simbol · 32.6s

Saringan: umur maksimum **168 bar**, carry terproyeksi maksimum **0.25R** atas jendela 30 hari.

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- ekspektasi 0.0316R < 0.05R

## Hasil luar sampel

- Perdagangan: **18,883**
- Total R: **596.44**
- Ekspektasi: **0.03158622537199252**
- Jendela positif: 212/356
- Alasan keluar: {'target': 6707, 'stop': 11909, 'akhir_data': 164, 'umur': 103}

```
