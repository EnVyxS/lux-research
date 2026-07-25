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
- Ekspektasi: **-0.24781930467946856**
- Jendela positif: 25/356
- Alasan keluar: {'target': 7503, 'stop': 20997, 'akhir_data': 258, 'umur': 201}

## Perbandingan tiga hipotesis

Dataset, kriteria, dan kode penilaian identik pada ketiganya.

| Besaran | H-001b | H-002 | H-003 |
|---|---|---|---|
| Ekspektasi R | 0.030857864162317453 | 0.03158622537199252 | -0.24781930467946856 |
| Total R | 589.1692004511272 | 596.4426936993348 | -7176.60 |
| Trade luar sampel | 19093 | 18883 | 28959 |
| Kerugian terburuk R | None | None | -1.8636755413456403 |
| p entri acak | None | None | 1.0 |
| Putusan | False | False | False |

## Sembilan gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0003 | 0.3 | 0 dari 40 simbol gagal |
| buy_and_hold | GAGAL | -0.0783 | 0.0 | median selisih -0.0783; unggul di 19/40 simbol |
| entri_acak | GAGAL | 1.0000 | 0.05 | 100 dari 100 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -1.8637 | -1.5 | kerugian terburuk -1.864R dari 28959 perdagangan |
| funding | lulus | 13153.5414 | 0.0 | total funding mutlak 13153.541375 atas 28959 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 40 simbol gagal |
| checksum | lulus | 0.0000 | 0.0 | hilang 0, asing 0, tidak cocok 0 |
| survivorship | lulus | 0.8555 | 0.5 | porsi delisted diuji 0.1250 vs universe 0.1461 |

## Pembongkaran biaya

- Rerata biaya transaksi: **0.0335R**
- Rerata biaya funding: **-0.0017R**
- Rerata jarak stop terhadap harga: **3.636%**
- Perdagangan dengan biaya melebihi 1R: **0** dari 28,959

| Simbol | R | Kotor R | Transaksi R | Funding R | Stop % harga | Jam | Alasan |
|---|---|---|---|---|---|---|---|
| AKTUSDT | -1.864 | -1.010 | 0.020 | 0.833 | 5.064 | 77.0 | stop |
| ALPHAUSDT | -1.478 | -1.012 | 0.023 | 0.444 | 4.506 | 3.0 | stop |
| ANIMEUSDT | -1.476 | -1.009 | 0.018 | 0.448 | 5.628 | 1.0 | stop |
| 1000WHYUSDT | -1.409 | -1.013 | 0.027 | 0.368 | 3.599 | 91.0 | stop |
| ALPHAUSDT | -1.349 | -1.032 | 0.064 | 0.254 | 1.584 | 9.0 | stop |
| ACHUSDT | -1.346 | -1.005 | 0.009 | 0.332 | 12.182 | 65.0 | stop |
| ADAUSDT | -1.309 | -1.014 | 0.028 | 0.268 | 3.504 | 135.0 | stop |
| AGLDUSDT | -1.299 | -1.010 | 0.020 | 0.269 | 5.125 | 42.0 | stop |
| AGLDUSDT | -1.268 | -1.011 | 0.021 | 0.237 | 4.958 | 43.0 | stop |
| ADAUSDT | -1.259 | -1.049 | 0.098 | 0.113 | 1.030 | 40.0 | stop |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| AGTUSDT | 10,334 | 2 | 106 | 6.01 | 0.05665 |
| 1000000BOBUSDT | 9,952 | 2 | 74 | 0.22 | 0.00292 |
| 1000WHYUSDT | 11,446 | 3 | 112 | -8.72 | -0.07782 |
| ALPINEUSDT | 10,671 | 2 | 174 | -25.02 | -0.1438 |
| AIXBTUSDT | 13,950 | 4 | 391 | -45.39 | -0.11609 |
| ANIMEUSDT | 13,135 | 4 | 204 | -53.00 | -0.25982 |
| AINUSDT | 9,110 | 2 | 170 | -54.53 | -0.32076 |
| AIOTUSDT | 10,812 | 2 | 156 | -65.84 | -0.42203 |
| AKTUSDT | 14,725 | 4 | 353 | -67.15 | -0.19021 |
| AKROUSDT | 11,835 | 3 | 256 | -72.58 | -0.28351 |

## Sepuluh simbol dengan total R terendah

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| ADAUSDT | 56,800 | 24 | 2034 | -598.66 | -0.29432 |
| ALGOUSDT | 53,511 | 22 | 1859 | -448.30 | -0.24115 |
| 1INCHUSDT | 48,902 | 20 | 1711 | -405.57 | -0.23703 |
| AAVEUSDT | 50,585 | 21 | 1696 | -398.75 | -0.23511 |
| 1000SHIBUSDT | 45,631 | 19 | 1573 | -393.11 | -0.24991 |
| 1000XECUSDT | 42,525 | 17 | 1318 | -365.00 | -0.27693 |
| ANKRUSDT | 48,137 | 20 | 1537 | -333.91 | -0.21725 |
| ALICEUSDT | 46,965 | 19 | 1379 | -321.60 | -0.23321 |
| ALPHAUSDT | 42,363 | 17 | 1485 | -316.93 | -0.21342 |
| 1000PEPEUSDT | 28,232 | 10 | 947 | -284.02 | -0.29991 |
