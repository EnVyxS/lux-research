# Backtest H-013-AS — h013_as_acak_stop

> Sel AS dari rancangan faktorial 2x2 ADR-015 bagian B: sinyal permutasi, geometri keluar stop + target. Yang diuji BUKAN kelulusan sel ini melainkan selisih antar sel: sumbangan sinyal SS - AS dengan ambang 0,020R, sumbangan geometri SS - SH, dan interaksinya. Skor entri acak H-010 dan H-012 identik sampai lima desimal pada 0,04661R sementara sinyal sungguhan bergerak di sekitarnya, sehingga kemungkinan paling sederhana adalah sinyalnya tidak menyumbang apa pun — dan kemungkinan itu belum pernah diuji sekali pun dalam dua belas hipotesis.

Sidik `5ee4b130f9ed228d` · 9 kombinasi · 437 simbol · 134.4s

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- ekspektasi 0.0118R < 0.05R
- p entri acak 0.3588 > 0.05

Gerbang gagal: entri_acak, lookahead, invarian_risiko, checksum, konsentrasi

## Hasil luar sampel

- Perdagangan: **55,927**
- Total R: **660.26**
- Ekspektasi: **0.01180570125176449**
- Jendela positif: 2046/4082
- Alasan keluar: {'target': 14491, 'umur': 8574, 'stop': 30853, 'akhir_data': 1913, 'carry': 96}
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

Setiap perdagangan dimiliki oleh bulan kalender UTC tempat ia **dibuka**, karena keputusan yang diuji adalah keputusan masuk. Akibatnya ada rembesan yang wajib dinyatakan: perdagangan yang dibuka sesaat sebelum batas sebuah periode dapat ditutup sesudahnya, dan besarnya rembesan itu terbatas oleh `maks_umur_bar` (42 bar).

Tabel ini **bukan** putusan dan bukan pula izin memilih periode terbaik sesudah melihatnya. Memilih periode setelah hasil terlihat adalah penyubsetan yang sama terlarangnya dengan memilih simbol.

| Bulan masuk | Trade | Total R | Ekspektasi R |
|---|---|---|---|
| 2020-07 | 35 | +23.31 | +0.665926 |
| 2020-08 | 87 | -0.47 | -0.005392 |
| 2020-09 | 110 | -15.55 | -0.141348 |
| 2020-10 | 117 | +9.55 | +0.081586 |
| 2020-11 | 116 | -0.93 | -0.008056 |
| 2020-12 | 132 | +10.85 | +0.082231 |
| 2021-01 | 139 | +40.70 | +0.292788 |
| 2021-02 | 186 | +24.48 | +0.131612 |
| 2021-03 | 194 | +31.80 | +0.163918 |
| 2021-04 | 248 | +11.45 | +0.046172 |
| 2021-05 | 331 | -50.75 | -0.153334 |
| 2021-06 | 338 | -8.68 | -0.025668 |
| 2021-07 | 392 | +20.54 | +0.052393 |
| 2021-08 | 404 | +46.77 | +0.115758 |
| 2021-09 | 418 | +0.95 | +0.002277 |
| 2021-10 | 489 | +31.26 | +0.063935 |
| 2021-11 | 474 | -49.04 | -0.103460 |
| 2021-12 | 477 | -46.05 | -0.096550 |
| 2022-01 | 498 | +0.25 | +0.000510 |
| 2022-02 | 505 | -84.46 | -0.167238 |
| 2022-03 | 550 | -36.37 | -0.066136 |
| 2022-04 | 562 | +85.27 | +0.151719 |
| 2022-05 | 584 | +113.35 | +0.194097 |
| 2022-06 | 544 | +11.85 | +0.021781 |
| 2022-07 | 543 | -86.05 | -0.158464 |
| 2022-08 | 488 | -32.49 | -0.066586 |
| 2022-09 | 463 | -12.81 | -0.027674 |
| 2022-10 | 484 | -3.98 | -0.008219 |
| 2022-11 | 496 | -3.55 | -0.007152 |
| 2022-12 | 527 | -3.73 | -0.007087 |
| 2023-01 | 668 | -6.65 | -0.009962 |
| 2023-02 | 584 | +34.59 | +0.059226 |
| 2023-03 | 605 | +2.52 | +0.004160 |
| 2023-04 | 560 | -52.09 | -0.093013 |
| 2023-05 | 584 | -12.44 | -0.021302 |
| 2023-06 | 636 | -20.12 | -0.031627 |
| 2023-07 | 547 | -77.14 | -0.141032 |
| 2023-08 | 561 | -37.56 | -0.066961 |
| 2023-09 | 551 | -23.73 | -0.043065 |
| 2023-10 | 686 | +119.91 | +0.174790 |
| 2023-11 | 698 | -35.98 | -0.051542 |
| 2023-12 | 764 | -43.51 | -0.056953 |
| 2024-01 | 726 | -148.65 | -0.204750 |
| 2024-02 | 751 | +269.36 | +0.358663 |
| 2024-03 | 808 | -6.37 | -0.007888 |
| 2024-04 | 754 | -2.37 | -0.003144 |
| 2024-05 | 840 | -179.54 | -0.213742 |
| 2024-06 | 893 | +111.74 | +0.125131 |
| 2024-07 | 1,079 | +37.32 | +0.034591 |
| 2024-08 | 1,273 | +138.30 | +0.108641 |
| 2024-09 | 1,113 | +10.03 | +0.009012 |
| 2024-10 | 1,218 | -146.02 | -0.119886 |
| 2024-11 | 1,264 | +321.86 | +0.254636 |
| 2024-12 | 1,206 | -112.70 | -0.093447 |
| 2025-01 | 1,151 | +0.99 | +0.000858 |
| 2025-02 | 1,062 | -4.88 | -0.004591 |
| 2025-03 | 1,165 | +109.18 | +0.093713 |
| 2025-04 | 1,280 | +15.49 | +0.012103 |
| 2025-05 | 1,417 | -60.54 | -0.042724 |
| 2025-06 | 1,386 | -98.11 | -0.070784 |
| 2025-07 | 1,508 | +72.09 | +0.047808 |
| 2025-08 | 1,433 | -40.89 | -0.028533 |
| 2025-09 | 1,395 | -91.50 | -0.065589 |
| 2025-10 | 1,565 | +30.07 | +0.019212 |
| 2025-11 | 1,563 | +250.45 | +0.160235 |
| 2025-12 | 1,733 | -3.27 | -0.001885 |
| 2026-01 | 1,869 | +376.57 | +0.201480 |
| 2026-02 | 1,664 | +70.74 | +0.042512 |
| 2026-03 | 1,696 | -90.61 | -0.053424 |
| 2026-04 | 1,586 | -142.23 | -0.089681 |
| 2026-05 | 1,274 | +134.58 | +0.105637 |
| 2026-06 | 713 | +0.82 | +0.001149 |
| 2026-07 | 167 | -36.90 | -0.220952 |

## Sebaran R dan galat baku (ADR-013)

Sampai H-010 laporan hanya memuat rerata, sehingga tidak ada hipotesis yang dapat dinilai secara statistik: mustahil mengatakan apakah selisih terhadap ambang berarti sesuatu atau tidak.

**Galat baku di bawah adalah taksiran BAWAH.** Ia mengandaikan perdagangan saling bebas, dan andaian itu tidak benar: perdagangan dari puluhan simbol kripto pada jendela waktu yang bertumpang berkorelasi lewat gerakan pasar bersama. Galat sesungguhnya lebih besar, jadi keyakinan sesungguhnya lebih kecil. Angka ini sah dipakai untuk **menjatuhkan** klaim, dan tidak sah dipakai untuk **menegakkan** klaim.

- Simpangan baku per perdagangan: **1.30621R** (ddof=1, n = 55,927)
- Galat baku ekspektasi: **0.005523R**
- Selang 95% (pendekatan normal): **[0.000980, 0.022631]R**
- Kuartil R: min -7.3767 · Q1 -1.0272 · median -1.0068 · Q3 1.9023 · maks 3.2783
- Jarak ke ambang 0.05R: **-0.038194R** = **-6.92 galat baku**

## Sebelas gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0014 | 0.3 | 0 dari 437 simbol gagal |
| buy_and_hold | lulus | 0.7927 | 0.0 | median selisih 0.7927; unggul di 390/437 simbol |
| entri_acak | GAGAL | 0.3588 | 0.05 | 107 dari 300 permutasi menyamai atau melampaui |
| lookahead | GAGAL | 337.0000 | 0.0 | 337 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -7.3767 | -1.5 | kerugian terburuk -7.377R dari 55927 perdagangan |
| funding | lulus | 51906.4367 | 0.0 | total funding mutlak 51906.436670 atas 55927 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 437 simbol gagal |
| checksum | GAGAL | 24.0000 | 0.0 | hilang 12, asing 12, tidak cocok 0 |
| survivorship | lulus | 1.0000 | 0.5 | porsi delisted diuji 0.1465 vs universe 0.1465 |
| konsentrasi | GAGAL | 0.9288 | 0.6 | 248 untung / 189 rugi dari 437 simbol; drop-1 0.01097R (retensi 0.9288), drop-22 -0.00040R, median simbol +0.02012R, porsi bruto teratas 0.0197 (ETHUSDT), setara 144.8 simbol; sub-uji gagal: drop_5persen_positif |
| funding_ekor | lulus | 0.0108 | 0.35 | porsi ekor maks 0.0108 (rerata 0.0024 atas 10 terburuk), funding maks 0.4213R, 99 dari 55927 trade di atas pengaman (0.00177) |

## Jackknife konsentrasi (ADR-010)

Buang penyumbang teratas satu per satu. Retensi adalah ekspektasi setelah pembuangan dibagi ekspektasi utuh. Ini menjawab pertanyaan yang sesungguhnya penting: apakah keunggulan tetap ada seandainya simbol paling untung tidak pernah ada.

| k | Dibuang | Simbol sisa | Trade | Total R | Ekspektasi R | Retensi |
|---|---|---|---|---|---|---|
| 0 | — | 437 | 55,927 | 660.26 | 0.011806 | 1.0000 |
| 1 | ETHUSDT | 436 | 55,608 | 609.75 | 0.010965 | 0.9288 |
| 2 | LTCUSDT | 435 | 55,299 | 569.21 | 0.010293 | 0.8719 |
| 3 | UNIUSDT | 434 | 55,030 | 532.57 | 0.009678 | 0.8198 |
| 4 | HBARUSDT | 433 | 54,772 | 496.61 | 0.009067 | 0.7680 |
| 5 | TNSRUSDT | 432 | 54,668 | 461.87 | 0.008449 | 0.7156 |

## Ekor funding (ADR-011)

Gerbang funding lama menilai total mutlak dan memberi nilai yang praktis sama untuk dua keadaan yang ekornya berbeda 4,4 kali. Yang dinilai di sini adalah porsi funding terhadap kerugian pada sepuluh perdagangan terburuk, karena di situlah funding pernah menyumbang 46,7% kerugian sementara reratanya hanya 0,0004R.

- Porsi funding terbesar di ekor: **0.0108** (ambang 0,35)
- Rerata porsi di 10 terburuk: **0.0024**
- Funding terbesar satu perdagangan: **0.4213R** (ambang 0,50R)
- Perdagangan di atas pengaman 0,25R: **99** dari 55,927 (0.00177, ambang 0,005)

| # | R | Funding R | Porsi funding |
|---|---|---|---|
| 1 | -7.3767 | -0.0000 | 0.0000 |
| 2 | -7.0985 | -0.0000 | 0.0000 |
| 3 | -7.0716 | 0.0589 | 0.0083 |
| 4 | -5.7363 | -0.0000 | 0.0000 |
| 5 | -5.2851 | 0.0569 | 0.0108 |
| 6 | -4.9338 | 0.0010 | 0.0002 |
| 7 | -4.7453 | 0.0175 | 0.0037 |
| 8 | -4.4878 | -0.0000 | 0.0000 |
| 9 | -4.4870 | -0.0000 | 0.0000 |
| 10 | -4.4728 | 0.0028 | 0.0006 |

## Pembongkaran biaya

- Rerata biaya transaksi: **0.0171R**
- Rerata biaya funding: **0.0015R**
- Rerata jarak stop terhadap harga: **7.121%**
- Perdagangan dengan biaya melebihi 1R: **0** dari 55,927

## Parameter yang terpilih di dalam sampel

| Parameter | Jumlah jendela |
|---|---|
| `{"imbalan_R": 2.0, "lookback": 100}` | 1585 |
| `{"imbalan_R": 2.0, "lookback": 20}` | 1408 |
| `{"imbalan_R": 2.0, "lookback": 55}` | 1089 |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| ETHUSDT | 14,388 | 24 | 319 | 50.50 | 0.15832 |
| LTCUSDT | 14,302 | 24 | 309 | 40.55 | 0.13122 |
| UNIUSDT | 12,815 | 21 | 269 | 36.64 | 0.13621 |
| HBARUSDT | 11,705 | 19 | 258 | 35.95 | 0.13936 |
| TNSRUSDT | 5,024 | 7 | 104 | 34.74 | 0.33406 |
| FILUSDT | 12,617 | 21 | 259 | 34.41 | 0.13284 |
| BTCUSDT | 14,388 | 24 | 358 | 31.87 | 0.08901 |
| ARPAUSDT | 10,440 | 17 | 220 | 31.31 | 0.14233 |
| C98USDT | 10,776 | 17 | 260 | 30.94 | 0.11901 |
| VANRYUSDT | 5,180 | 7 | 91 | 29.46 | 0.32373 |
