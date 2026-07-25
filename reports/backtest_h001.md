# Backtest H-001 — breakout Donchian 1 jam

> Penembusan Donchian pada penutupan bar 1 jam menghasilkan ekspektasi positif setelah fee, slippage, dan funding nyata, pada perp USDT yang lolos ambang kelayakan, dinilai hanya di luar sampel.

Sidik hipotesis `f172b1ba07f25717` · ruang 3 kombinasi · 40 simbol · 29.9s

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- ekspektasi 0.0317R < 0.05R

Gerbang gagal: forward_fill, invarian_risiko, checksum

## Hasil luar sampel

- Perdagangan: **19,060**
- Total R: **604.26**
- Ekspektasi: **0.031703229028761756**
- Jendela positif: 208/359

## Sembilan gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | GAGAL | 0.2137 | 0.3 | 4 dari 40 simbol gagal — 1000WHYUSDT (rasio bar datar 0.2137, deret terpanjang 3111 bar); AERGOUSDT (rasio bar datar 0.0288, deret terpanjang 470 bar); AIUSDT (rasio bar datar 0.0943, deret terpanjang 2101 bar); ALPHAUSDT (rasio bar datar 0.1472, deret terpanjang 7310 bar) |
| buy_and_hold | lulus | 0.8007 | 0.0 | median selisih 0.8007; unggul di 36/40 simbol |
| entri_acak | lulus | 0.0099 | 0.05 | 0 dari 100 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -2.5853 | -1.5 | kerugian terburuk -2.585R dari 19060 perdagangan |
| funding | lulus | 11238.2546 | 0.0 | total funding mutlak 11238.254635 atas 19060 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 40 simbol gagal |
| checksum | GAGAL | — | — | tidak dapat dinilai: manifest baru ditulis pada run ini; run berikutnya akan membandingkannya |
| survivorship | lulus | 0.7450 | 0.5 | porsi delisted diuji 0.0250 vs universe 0.0336 |

## Pembongkaran biaya

Mesin mengisi stop tepat di harga stop, sehingga kerugian yang berasal dari harga tidak dapat melewati 1R. Kerugian di luar itu wajib berasal dari biaya, dan tabel ini memperlihatkannya per perdagangan.

- Rerata biaya transaksi: **0.0342R**
- Rerata biaya funding: **0.0012R**
- Rerata jarak stop terhadap harga: **3.582%**
- Perdagangan dengan biaya melebihi 1R: **2** dari 19,060

| Simbol | R | Kotor R | Transaksi R | Funding R | Stop % harga | Jam | Alasan |
|---|---|---|---|---|---|---|---|
| ANIMEUSDT | -2.585 | -1.013 | 0.026 | 1.545 | 3.847 | 130.0 | stop |
| AERGOUSDT | -2.276 | -1.021 | 0.042 | 1.212 | 2.391 | 76.0 | stop |
| AERGOUSDT | -1.498 | -1.043 | 0.086 | 0.370 | 1.162 | 34.0 | stop |
| AERGOUSDT | -1.479 | -1.019 | 0.038 | 0.422 | 2.659 | 174.0 | stop |
| AERGOUSDT | -1.468 | -1.007 | 0.013 | 0.448 | 7.921 | 62.0 | stop |
| ACEUSDT | -1.436 | -1.023 | 0.045 | 0.369 | 2.272 | 96.0 | stop |
| AERGOUSDT | -1.423 | -1.007 | 0.014 | 0.401 | 7.162 | 79.0 | stop |
| ADAUSDT | -1.403 | -1.038 | 0.077 | 0.289 | 1.295 | 38.0 | stop |
| 1000XECUSDT | -1.395 | -1.013 | 0.026 | 0.356 | 3.987 | 219.0 | stop |
| ANIMEUSDT | -1.371 | -1.009 | 0.018 | 0.344 | 5.808 | 196.0 | stop |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| ALGOUSDT | 53,511 | 22 | 1215 | 66.48 | 0.05471 |
| ADAUSDT | 56,800 | 24 | 1327 | 66.29 | 0.04996 |
| 1000PEPEUSDT | 28,232 | 10 | 502 | 59.74 | 0.11901 |
| 1000BONKUSDT | 23,410 | 8 | 335 | 54.54 | 0.1628 |
| 1000CHEEMSUSDT | 14,557 | 4 | 253 | 51.73 | 0.20446 |
| AIOTUSDT | 10,812 | 2 | 78 | 49.48 | 0.63442 |
| ALPHAUSDT | 49,673 | 20 | 919 | 47.82 | 0.05203 |
| AIUSDT | 22,284 | 8 | 319 | 45.57 | 0.14287 |
| AAVEUSDT | 50,585 | 21 | 1041 | 45.12 | 0.04334 |
| 1000CATUSDT | 15,396 | 5 | 263 | 41.05 | 0.15609 |

## Sepuluh simbol dengan total R terendah

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| AIXBTUSDT | 13,950 | 4 | 249 | -26.46 | -0.10626 |
| ANIMEUSDT | 13,135 | 4 | 215 | -25.82 | -0.12009 |
| AERGOUSDT | 16,345 | 5 | 274 | -24.28 | -0.08863 |
| ANKRUSDT | 48,137 | 20 | 1152 | -18.26 | -0.01585 |
| AGLDUSDT | 26,206 | 10 | 514 | -15.29 | -0.02975 |
| AGTUSDT | 10,334 | 2 | 115 | -14.07 | -0.12231 |
| ALPINEUSDT | 10,671 | 2 | 102 | -10.30 | -0.10096 |
| 1000XECUSDT | 42,525 | 17 | 983 | -9.35 | -0.00951 |
| ACHUSDT | 29,962 | 11 | 658 | -8.27 | -0.01257 |
| AKROUSDT | 11,835 | 3 | 186 | -6.48 | -0.03483 |
