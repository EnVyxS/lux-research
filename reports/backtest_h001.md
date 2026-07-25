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
- Ekspektasi: **0.030857864162317453**
- Jendela positif: 208/356

## Sembilan gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0003 | 0.3 | 0 dari 40 simbol gagal |
| buy_and_hold | lulus | 0.7897 | 0.0 | median selisih 0.7897; unggul di 35/40 simbol |
| entri_acak | lulus | 0.0099 | 0.05 | 0 dari 100 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -2.5853 | -1.5 | kerugian terburuk -2.585R dari 19093 perdagangan |
| funding | lulus | 10414.5175 | 0.0 | total funding mutlak 10414.517455 atas 19093 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 40 simbol gagal |
| checksum | lulus | 0.0000 | 0.0 | hilang 0, asing 0, tidak cocok 0 |
| survivorship | lulus | 0.8555 | 0.5 | porsi delisted diuji 0.1250 vs universe 0.1461 |

## Pembongkaran biaya

Mesin mengisi stop tepat di harga stop, sehingga kerugian yang berasal dari harga tidak dapat melewati 1R. Kerugian di luar itu wajib berasal dari biaya, dan tabel ini memperlihatkannya per perdagangan.

- Rerata biaya transaksi: **0.0343R**
- Rerata biaya funding: **0.0014R**
- Rerata jarak stop terhadap harga: **3.568%**
- Perdagangan dengan biaya melebihi 1R: **1** dari 19,093

| Simbol | R | Kotor R | Transaksi R | Funding R | Stop % harga | Jam | Alasan |
|---|---|---|---|---|---|---|---|
| ANIMEUSDT | -2.585 | -1.013 | 0.026 | 1.545 | 3.847 | 130.0 | stop |
| ACEUSDT | -1.436 | -1.023 | 0.045 | 0.369 | 2.272 | 96.0 | stop |
| ADAUSDT | -1.403 | -1.038 | 0.077 | 0.289 | 1.295 | 38.0 | stop |
| 1000XECUSDT | -1.395 | -1.013 | 0.026 | 0.356 | 3.987 | 219.0 | stop |
| ANIMEUSDT | -1.371 | -1.009 | 0.018 | 0.344 | 5.808 | 196.0 | stop |
| ADAUSDT | -1.341 | -1.011 | 0.023 | 0.306 | 4.177 | 117.0 | stop |
| ACEUSDT | -1.296 | -1.014 | 0.028 | 0.254 | 3.682 | 42.0 | stop |
| ACTUSDT | -1.295 | -1.011 | 0.022 | 0.262 | 4.666 | 16.0 | stop |
| 1000WHYUSDT | -1.293 | -1.006 | 0.012 | 0.276 | 7.929 | 41.0 | stop |
| 1000WHYUSDT | -1.290 | -1.015 | 0.031 | 0.244 | 3.201 | 39.0 | stop |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| ALGOUSDT | 53,511 | 22 | 1215 | 66.48 | 0.05471 |
| ADAUSDT | 56,800 | 24 | 1327 | 66.29 | 0.04996 |
| 1000PEPEUSDT | 28,232 | 10 | 502 | 59.74 | 0.11901 |
| 1000BONKUSDT | 23,410 | 8 | 335 | 54.54 | 0.1628 |
| 1000CHEEMSUSDT | 14,557 | 4 | 253 | 51.73 | 0.20446 |
| ALPHAUSDT | 42,363 | 17 | 881 | 51.30 | 0.05823 |
| AIOTUSDT | 10,812 | 2 | 78 | 49.48 | 0.63442 |
| AAVEUSDT | 50,585 | 21 | 1041 | 45.12 | 0.04334 |
| AIUSDT | 20,183 | 7 | 299 | 42.28 | 0.14142 |
| 1000CATUSDT | 15,396 | 5 | 263 | 41.05 | 0.15609 |

## Sepuluh simbol dengan total R terendah

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| ANTUSDT | 19,829 | 7 | 374 | -40.79 | -0.10906 |
| AIXBTUSDT | 13,950 | 4 | 249 | -26.46 | -0.10626 |
| ANIMEUSDT | 13,135 | 4 | 215 | -25.82 | -0.12009 |
| ANKRUSDT | 48,137 | 20 | 1152 | -18.26 | -0.01585 |
| AGLDUSDT | 26,206 | 10 | 514 | -15.29 | -0.02975 |
| AGTUSDT | 10,334 | 2 | 115 | -14.07 | -0.12231 |
| ALPINEUSDT | 10,671 | 2 | 102 | -10.30 | -0.10096 |
| 1000XECUSDT | 42,525 | 17 | 983 | -9.35 | -0.00951 |
| ACHUSDT | 29,962 | 11 | 658 | -8.27 | -0.01257 |
| AKROUSDT | 11,835 | 3 | 186 | -6.48 | -0.03483 |
