# Backtest H-013-AH — h013_ah_acak_horizon

> Sel AH dari rancangan faktorial 2x2 ADR-015 bagian B: sinyal permutasi, geometri keluar horizon tetap 48 bar tanpa target. Yang diuji BUKAN kelulusan sel ini melainkan selisih antar sel: sumbangan sinyal SS - AS dengan ambang 0,020R, sumbangan geometri SS - SH, dan interaksinya. Skor entri acak H-010 dan H-012 identik sampai lima desimal pada 0,04661R sementara sinyal sungguhan bergerak di sekitarnya, sehingga kemungkinan paling sederhana adalah sinyalnya tidak menyumbang apa pun — dan kemungkinan itu belum pernah diuji sekali pun dalam dua belas hipotesis.

Sidik `4ada4587abede644` · 9 kombinasi · 437 simbol · 143.7s

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- p entri acak 0.1993 > 0.05

Gerbang gagal: entri_acak, lookahead, invarian_risiko, checksum, funding_ekor

## Hasil luar sampel

- Perdagangan: **45,378**
- Total R: **2639.66**
- Ekspektasi: **0.05817042814276683**
- Jendela positif: 2060/4082
- Alasan keluar: {'umur': 15588, 'stop': 27297, 'carry': 258, 'akhir_data': 2235}
- Entri ditolak pengaman biaya (ADR-014): **0**, pengaman 0.5R

Penolakan pengaman biaya **bukan perdagangan** dan karena itu tidak muncul di histogram alasan keluar maupun di jumlah perdagangan di atas. Angka itu juga **tidak** mengukur seluruh keadaan degenerat: pada simbol yang seluruhnya degenerat, pengaman menolak entri juga saat pemilihan parameter, sehingga semua kandidat berskor -inf, seluruh jendelanya dilewati, dan simbol itu menyumbang nol penolakan sekaligus nol perdagangan. Yang tercatat di sini hanyalah simbol yang berubah degenerat di tengah jalan; simbol yang degenerat sepanjang riwayatnya hanya terlihat di lantai semesta di bawah.

## Lantai satuan R pada semesta (ADR-014)

Lantai median `stop_frac` **0.004**, diturunkan dari aritmetika biaya dan bukan disetel: biaya bolak-balik 0,002 dari harga menjadi tepat 0,5R di lantai itu. Kriteria ini seragam dan dipra-registrasi, sehingga ia bukan penyubsetan simbol pasca-hasil.

- Simbol dinilai: **438**
- Layak: **437**
- Dibuang: **1**

| Simbol | median stop_frac | biaya masuk R | Sebab |
|---|---|---|---|
| USDCUSDT | 3.799992e-04 | 5.26 | median jarak stop 3.800e-04 di bawah lantai 0.004 |

## Hasil menurut bulan masuk (ADR-014)

Setiap perdagangan dimiliki oleh bulan kalender UTC tempat ia **dibuka**, karena keputusan yang diuji adalah keputusan masuk. Akibatnya ada rembesan yang wajib dinyatakan: perdagangan yang dibuka sesaat sebelum batas sebuah periode dapat ditutup sesudahnya, dan besarnya rembesan itu terbatas oleh `maks_umur_bar` (48 bar).

Tabel ini **bukan** putusan dan bukan pula izin memilih periode terbaik sesudah melihatnya. Memilih periode setelah hasil terlihat adalah penyubsetan yang sama terlarangnya dengan memilih simbol.

| Bulan masuk | Trade | Total R | Ekspektasi R |
|---|---|---|---|
| 2020-07 | 22 | +10.02 | +0.455632 |
| 2020-08 | 67 | -6.80 | -0.101566 |
| 2020-09 | 87 | -13.01 | -0.149581 |
| 2020-10 | 92 | +31.59 | +0.343387 |
| 2020-11 | 94 | +22.48 | +0.239124 |
| 2020-12 | 96 | +24.09 | +0.250943 |
| 2021-01 | 121 | +19.07 | +0.157618 |
| 2021-02 | 150 | +59.31 | +0.395418 |
| 2021-03 | 164 | +42.65 | +0.260080 |
| 2021-04 | 210 | +68.58 | +0.326588 |
| 2021-05 | 256 | -17.34 | -0.067718 |
| 2021-06 | 273 | -19.09 | -0.069911 |
| 2021-07 | 316 | +1.68 | +0.005325 |
| 2021-08 | 310 | +91.50 | +0.295153 |
| 2021-09 | 335 | -28.17 | -0.084090 |
| 2021-10 | 358 | +9.40 | +0.026267 |
| 2021-11 | 369 | -91.52 | -0.248028 |
| 2021-12 | 388 | -57.99 | -0.149447 |
| 2022-01 | 404 | +168.61 | +0.417361 |
| 2022-02 | 371 | -68.11 | -0.183594 |
| 2022-03 | 452 | +126.95 | +0.280869 |
| 2022-04 | 437 | +151.65 | +0.347017 |
| 2022-05 | 420 | +201.37 | +0.479449 |
| 2022-06 | 428 | +93.76 | +0.219069 |
| 2022-07 | 465 | -187.32 | -0.402839 |
| 2022-08 | 430 | -15.58 | -0.036237 |
| 2022-09 | 407 | -71.83 | -0.176488 |
| 2022-10 | 433 | -40.74 | -0.094090 |
| 2022-11 | 433 | -6.63 | -0.015315 |
| 2022-12 | 442 | +63.02 | +0.142587 |
| 2023-01 | 512 | +357.15 | +0.697564 |
| 2023-02 | 456 | -36.83 | -0.080778 |
| 2023-03 | 478 | +17.00 | +0.035555 |
| 2023-04 | 454 | -14.10 | -0.031053 |
| 2023-05 | 473 | +31.81 | +0.067255 |
| 2023-06 | 488 | +165.42 | +0.338968 |
| 2023-07 | 459 | -100.55 | -0.219059 |
| 2023-08 | 487 | +18.15 | +0.037267 |
| 2023-09 | 496 | -73.37 | -0.147930 |
| 2023-10 | 540 | +264.01 | +0.488904 |
| 2023-11 | 601 | -20.83 | -0.034652 |
| 2023-12 | 601 | -13.24 | -0.022034 |
| 2024-01 | 630 | -205.11 | -0.325574 |
| 2024-02 | 564 | +550.32 | +0.975745 |
| 2024-03 | 657 | -63.28 | -0.096313 |
| 2024-04 | 614 | +8.37 | +0.013636 |
| 2024-05 | 726 | -182.51 | -0.251385 |
| 2024-06 | 739 | +253.64 | +0.343225 |
| 2024-07 | 892 | +134.36 | +0.150626 |
| 2024-08 | 910 | +18.72 | +0.020568 |
| 2024-09 | 913 | +24.28 | +0.026593 |
| 2024-10 | 971 | -292.85 | -0.301594 |
| 2024-11 | 930 | +776.27 | +0.834697 |
| 2024-12 | 990 | -226.83 | -0.229118 |
| 2025-01 | 985 | +48.40 | +0.049137 |
| 2025-02 | 901 | -58.85 | -0.065316 |
| 2025-03 | 992 | +165.44 | +0.166771 |
| 2025-04 | 1,018 | +33.29 | +0.032701 |
| 2025-05 | 1,125 | -65.32 | -0.058059 |
| 2025-06 | 1,154 | -356.17 | -0.308639 |
| 2025-07 | 1,176 | +329.85 | +0.280489 |
| 2025-08 | 1,224 | -272.63 | -0.222739 |
| 2025-09 | 1,137 | +0.83 | +0.000734 |
| 2025-10 | 1,306 | +406.44 | +0.311210 |
| 2025-11 | 1,267 | +0.08 | +0.000066 |
| 2025-12 | 1,357 | +76.33 | +0.056250 |
| 2026-01 | 1,506 | +518.73 | +0.344443 |
| 2026-02 | 1,304 | -105.92 | -0.081223 |
| 2026-03 | 1,417 | -177.27 | -0.125102 |
| 2026-04 | 1,331 | +21.20 | +0.015931 |
| 2026-05 | 1,032 | +190.91 | +0.184991 |
| 2026-06 | 579 | -21.40 | -0.036961 |
| 2026-07 | 156 | -45.92 | -0.294381 |

## Sebaran R dan galat baku (ADR-013)

Sampai H-010 laporan hanya memuat rerata, sehingga tidak ada hipotesis yang dapat dinilai secara statistik: mustahil mengatakan apakah selisih terhadap ambang berarti sesuatu atau tidak.

**Galat baku di bawah adalah taksiran BAWAH.** Ia mengandaikan perdagangan saling bebas, dan andaian itu tidak benar: perdagangan dari puluhan simbol kripto pada jendela waktu yang bertumpang berkorelasi lewat gerakan pasar bersama. Galat sesungguhnya lebih besar, jadi keyakinan sesungguhnya lebih kecil. Angka ini sah dipakai untuk **menjatuhkan** klaim, dan tidak sah dipakai untuk **menegakkan** klaim.

- Simpangan baku per perdagangan: **1.92789R** (ddof=1, n = 45,378)
- Galat baku ekspektasi: **0.009050R**
- Selang 95% (pendekatan normal): **[0.040432, 0.075909]R**
- Kuartil R: min -6.2925 · Q1 -1.0293 · median -1.0122 · Q3 0.7838 · maks 78.0789
- Jarak ke ambang 0.05R: **+0.008170R** = **+0.90 galat baku**

## Sebelas gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0014 | 0.3 | 0 dari 437 simbol gagal |
| buy_and_hold | lulus | 0.8106 | 0.0 | median selisih 0.8106; unggul di 391/437 simbol |
| entri_acak | GAGAL | 0.1993 | 0.05 | 59 dari 300 permutasi menyamai atau melampaui |
| lookahead | GAGAL | 337.0000 | 0.0 | 337 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -6.2925 | -1.5 | kerugian terburuk -6.292R dari 45378 perdagangan |
| funding | lulus | 69841.2059 | 0.0 | total funding mutlak 69841.205899 atas 45378 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 437 simbol gagal |
| checksum | GAGAL | 24.0000 | 0.0 | hilang 12, asing 12, tidak cocok 0 |
| survivorship | lulus | 1.0000 | 0.5 | porsi delisted diuji 0.1465 vs universe 0.1465 |
| konsentrasi | lulus | 0.9726 | 0.6 | 270 untung / 167 rugi dari 437 simbol; drop-1 0.05658R (retensi 0.9726), drop-22 0.03461R, median simbol +0.04659R, porsi bruto teratas 0.0202 (ENJUSDT), setara 137.5 simbol |
| funding_ekor | GAGAL | 0.0110 | 0.35 | porsi ekor maks 0.0110 (rerata 0.0027 atas 10 terburuk), funding maks 0.7422R, 271 dari 45378 trade di atas pengaman (0.00597); gagal: funding_maks_R, porsi_trade_di_atas_pengaman |

## Jackknife konsentrasi (ADR-010)

Buang penyumbang teratas satu per satu. Retensi adalah ekspektasi setelah pembuangan dibagi ekspektasi utuh. Ini menjawab pertanyaan yang sesungguhnya penting: apakah keunggulan tetap ada seandainya simbol paling untung tidak pernah ada.

| k | Dibuang | Simbol sisa | Trade | Total R | Ekspektasi R | Retensi |
|---|---|---|---|---|---|---|
| 0 | — | 437 | 45,378 | 2639.66 | 0.058170 | 1.0000 |
| 1 | ENJUSDT | 436 | 45,144 | 2554.17 | 0.056578 | 0.9726 |
| 2 | BTCUSDT | 435 | 44,872 | 2477.59 | 0.055215 | 0.9492 |
| 3 | UNIUSDT | 434 | 44,662 | 2410.85 | 0.053980 | 0.9280 |
| 4 | SOLUSDT | 433 | 44,437 | 2345.56 | 0.052784 | 0.9074 |
| 5 | ETHUSDT | 432 | 44,167 | 2281.85 | 0.051664 | 0.8882 |

## Ekor funding (ADR-011)

Gerbang funding lama menilai total mutlak dan memberi nilai yang praktis sama untuk dua keadaan yang ekornya berbeda 4,4 kali. Yang dinilai di sini adalah porsi funding terhadap kerugian pada sepuluh perdagangan terburuk, karena di situlah funding pernah menyumbang 46,7% kerugian sementara reratanya hanya 0,0004R.

- Porsi funding terbesar di ekor: **0.0110** (ambang 0,35)
- Rerata porsi di 10 terburuk: **0.0027**
- Funding terbesar satu perdagangan: **0.7422R** (ambang 0,50R)
- Perdagangan di atas pengaman 0,25R: **271** dari 45,378 (0.00597, ambang 0,005)

| # | R | Funding R | Porsi funding |
|---|---|---|---|
| 1 | -6.2925 | -0.0000 | 0.0000 |
| 2 | -5.7363 | -0.0000 | 0.0000 |
| 3 | -5.3704 | 0.0000 | 0.0000 |
| 4 | -5.2851 | 0.0569 | 0.0108 |
| 5 | -4.9338 | 0.0010 | 0.0002 |
| 6 | -4.7453 | 0.0175 | 0.0037 |
| 7 | -4.4870 | -0.0000 | 0.0000 |
| 8 | -4.4728 | 0.0028 | 0.0006 |
| 9 | -4.1082 | 0.0012 | 0.0003 |
| 10 | -3.6341 | 0.0401 | 0.0110 |

## Pembongkaran biaya

- Rerata biaya transaksi: **0.0173R**
- Rerata biaya funding: **0.0006R**
- Rerata jarak stop terhadap harga: **6.990%**
- Perdagangan dengan biaya melebihi 1R: **0** dari 45,378

## Parameter yang terpilih di dalam sampel

| Parameter | Jumlah jendela |
|---|---|
| `{"imbalan_R": 2.0, "lookback": 100}` | 1617 |
| `{"imbalan_R": 2.0, "lookback": 20}` | 1392 |
| `{"imbalan_R": 2.0, "lookback": 55}` | 1073 |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| ENJUSDT | 12,749 | 21 | 234 | 85.49 | 0.36535 |
| BTCUSDT | 14,388 | 24 | 272 | 76.57 | 0.28152 |
| UNIUSDT | 12,815 | 21 | 210 | 66.74 | 0.31783 |
| SOLUSDT | 12,809 | 21 | 225 | 65.29 | 0.29017 |
| ETHUSDT | 14,388 | 24 | 270 | 63.71 | 0.23598 |
| DENTUSDT | 11,126 | 18 | 188 | 62.43 | 0.33206 |
| IMXUSDT | 9,720 | 15 | 184 | 62.31 | 0.33865 |
| FILUSDT | 12,617 | 21 | 192 | 62.09 | 0.32338 |
| DOGEUSDT | 13,234 | 22 | 207 | 54.65 | 0.26399 |
| TRXUSDT | 14,266 | 24 | 290 | 53.21 | 0.18348 |
