# Backtest H-014-SSp — h014_ssp_target_umur48

> Sel SS' — breakout Donchian dengan stop ATR DAN target imbalan 2.0R, batas umur 48 bar 4h. Sel pembanding bagi SH'; keduanya berbeda HANYA pada ada-tidaknya target.

Sidik `197c10e3f0d2a74f` · 3 kombinasi · 437 simbol · 56.9s

## Putusan

**DITOLAK**

Gerbang gagal: invarian_risiko, checksum, funding_ekor

## Hasil luar sampel

- Perdagangan: **59,324**
- Total R: **3989.66**
- Ekspektasi: **0.06725203533326735**
- Jendela positif: 2229/4082
- Alasan keluar: {'target': 18667, 'stop': 33748, 'umur': 5174, 'akhir_data': 1735}
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
| 2020-07 | 38 | +21.37 | +0.562370 |
| 2020-08 | 78 | -29.55 | -0.378833 |
| 2020-09 | 103 | +17.01 | +0.165159 |
| 2020-10 | 118 | -26.41 | -0.223771 |
| 2020-11 | 164 | -1.86 | -0.011313 |
| 2020-12 | 132 | -0.38 | -0.002903 |
| 2021-01 | 209 | -52.89 | -0.253071 |
| 2021-02 | 225 | +98.28 | +0.436794 |
| 2021-03 | 198 | -10.27 | -0.051875 |
| 2021-04 | 246 | +24.60 | +0.100020 |
| 2021-05 | 347 | +95.60 | +0.275502 |
| 2021-06 | 312 | +36.74 | +0.117769 |
| 2021-07 | 350 | +29.58 | +0.084524 |
| 2021-08 | 429 | -4.03 | -0.009388 |
| 2021-09 | 361 | -73.04 | -0.202340 |
| 2021-10 | 497 | -59.58 | -0.119871 |
| 2021-11 | 443 | -49.76 | -0.112333 |
| 2021-12 | 527 | +76.76 | +0.145661 |
| 2022-01 | 617 | +272.86 | +0.442229 |
| 2022-02 | 554 | +50.61 | +0.091358 |
| 2022-03 | 683 | +194.44 | +0.284689 |
| 2022-04 | 599 | +111.93 | +0.186857 |
| 2022-05 | 643 | +151.52 | +0.235650 |
| 2022-06 | 552 | +138.03 | +0.250059 |
| 2022-07 | 547 | -105.65 | -0.193146 |
| 2022-08 | 479 | +45.89 | +0.095805 |
| 2022-09 | 377 | -185.63 | -0.492385 |
| 2022-10 | 565 | +38.43 | +0.068013 |
| 2022-11 | 589 | -14.14 | -0.024001 |
| 2022-12 | 573 | +40.97 | +0.071495 |
| 2023-01 | 931 | +397.28 | +0.426724 |
| 2023-02 | 526 | -63.97 | -0.121618 |
| 2023-03 | 618 | +80.06 | +0.129552 |
| 2023-04 | 529 | -111.28 | -0.210366 |
| 2023-05 | 535 | +50.92 | +0.095175 |
| 2023-06 | 670 | +177.69 | +0.265214 |
| 2023-07 | 437 | -151.57 | -0.346846 |
| 2023-08 | 607 | +75.94 | +0.125114 |
| 2023-09 | 491 | -78.20 | -0.159261 |
| 2023-10 | 871 | +93.49 | +0.107341 |
| 2023-11 | 765 | -273.83 | -0.357952 |
| 2023-12 | 876 | -54.69 | -0.062429 |
| 2024-01 | 656 | -250.57 | -0.381964 |
| 2024-02 | 979 | +300.47 | +0.306912 |
| 2024-03 | 826 | -135.71 | -0.164296 |
| 2024-04 | 926 | +202.07 | +0.218214 |
| 2024-05 | 797 | -290.58 | -0.364591 |
| 2024-06 | 899 | +221.58 | +0.246474 |
| 2024-07 | 1,075 | +393.45 | +0.365998 |
| 2024-08 | 1,349 | +644.69 | +0.477904 |
| 2024-09 | 1,029 | +83.16 | +0.080812 |
| 2024-10 | 955 | -186.03 | -0.194791 |
| 2024-11 | 1,504 | +524.28 | +0.348591 |
| 2024-12 | 1,144 | -4.72 | -0.004128 |
| 2025-01 | 1,273 | -117.99 | -0.092686 |
| 2025-02 | 1,402 | +299.32 | +0.213494 |
| 2025-03 | 1,324 | +350.16 | +0.264475 |
| 2025-04 | 1,446 | +392.14 | +0.271186 |
| 2025-05 | 1,635 | +291.50 | +0.178286 |
| 2025-06 | 1,301 | -228.84 | -0.175894 |
| 2025-07 | 1,761 | +445.41 | +0.252928 |
| 2025-08 | 1,266 | -626.65 | -0.494981 |
| 2025-09 | 1,458 | -40.45 | -0.027744 |
| 2025-10 | 1,859 | +227.09 | +0.122155 |
| 2025-11 | 1,544 | +3.80 | +0.002460 |
| 2025-12 | 1,808 | -292.44 | -0.161750 |
| 2026-01 | 2,457 | +1401.01 | +0.570212 |
| 2026-02 | 1,695 | -487.62 | -0.287683 |
| 2026-03 | 1,569 | -212.12 | -0.135192 |
| 2026-04 | 1,657 | -231.37 | -0.139633 |
| 2026-05 | 1,433 | +237.13 | +0.165480 |
| 2026-06 | 748 | +150.53 | +0.201246 |
| 2026-07 | 138 | -46.33 | -0.335709 |

## Sebaran R dan galat baku (ADR-013)

Sampai H-010 laporan hanya memuat rerata, sehingga tidak ada hipotesis yang dapat dinilai secara statistik: mustahil mengatakan apakah selisih terhadap ambang berarti sesuatu atau tidak.

**Galat baku di bawah adalah taksiran BAWAH.** Ia mengandaikan perdagangan saling bebas, dan andaian itu tidak benar: perdagangan dari puluhan simbol kripto pada jendela waktu yang bertumpang berkorelasi lewat gerakan pasar bersama. Galat sesungguhnya lebih besar, jadi keyakinan sesungguhnya lebih kecil. Angka ini sah dipakai untuk **menjatuhkan** klaim, dan tidak sah dipakai untuk **menegakkan** klaim.

- Simpangan baku per perdagangan: **1.37827R** (ddof=1, n = 59,324)
- Galat baku ekspektasi: **0.005659R**
- Selang 95% (pendekatan normal): **[0.056161, 0.078343]R**
- Kuartil R: min -11.4736 · Q1 -1.0289 · median -1.0096 · Q3 1.9520 · maks 3.9173
- Jarak ke ambang 0.05R: **+0.017252R** = **+3.05 galat baku**

## Sebelas gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0014 | 0.3 | 0 dari 437 simbol gagal |
| buy_and_hold | lulus | 0.8134 | 0.0 | median selisih 0.8134; unggul di 392/437 simbol |
| entri_acak | lulus | 0.0166 | 0.05 | 4 dari 300 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -11.4736 | -1.5 | kerugian terburuk -11.474R dari 59324 perdagangan |
| funding | lulus | 56288.2674 | 0.0 | total funding mutlak 56288.267438 atas 59324 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 437 simbol gagal |
| checksum | GAGAL | — | — | tidak dapat dinilai: manifest baru ditulis pada run ini |
| survivorship | lulus | 1.0000 | 0.5 | porsi delisted diuji 0.1465 vs universe 0.1465 |
| konsentrasi | lulus | 0.9872 | 0.6 | 309 untung / 128 rugi dari 437 simbol; drop-1 0.06639R (retensi 0.9872), drop-22 0.05419R, median simbol +0.06789R, porsi bruto teratas 0.0139 (SANDUSDT), setara 181.1 simbol |
| funding_ekor | GAGAL | 0.0273 | 0.35 | porsi ekor maks 0.0273 (rerata 0.0027 atas 10 terburuk), funding maks 0.8285R, 82 dari 59324 trade di atas pengaman (0.00138); gagal: funding_maks_R |

## Jackknife konsentrasi (ADR-010)

Buang penyumbang teratas satu per satu. Retensi adalah ekspektasi setelah pembuangan dibagi ekspektasi utuh. Ini menjawab pertanyaan yang sesungguhnya penting: apakah keunggulan tetap ada seandainya simbol paling untung tidak pernah ada.

| k | Dibuang | Simbol sisa | Trade | Total R | Ekspektasi R | Retensi |
|---|---|---|---|---|---|---|
| 0 | — | 437 | 59,324 | 3989.66 | 0.067252 | 1.0000 |
| 1 | SANDUSDT | 436 | 59,036 | 3919.53 | 0.066392 | 0.9872 |
| 2 | BNBUSDT | 435 | 58,675 | 3849.79 | 0.065612 | 0.9756 |
| 3 | AXSUSDT | 434 | 58,348 | 3782.46 | 0.064826 | 0.9639 |
| 4 | RUNEUSDT | 433 | 58,057 | 3721.39 | 0.064099 | 0.9531 |
| 5 | XLMUSDT | 432 | 57,639 | 3660.54 | 0.063508 | 0.9443 |

## Ekor funding (ADR-011)

Gerbang funding lama menilai total mutlak dan memberi nilai yang praktis sama untuk dua keadaan yang ekornya berbeda 4,4 kali. Yang dinilai di sini adalah porsi funding terhadap kerugian pada sepuluh perdagangan terburuk, karena di situlah funding pernah menyumbang 46,7% kerugian sementara reratanya hanya 0,0004R.

- Porsi funding terbesar di ekor: **0.0273** (ambang 0,35)
- Rerata porsi di 10 terburuk: **0.0027**
- Funding terbesar satu perdagangan: **0.8285R** (ambang 0,50R)
- Perdagangan di atas pengaman 0,25R: **82** dari 59,324 (0.00138, ambang 0,005)

| # | R | Funding R | Porsi funding |
|---|---|---|---|
| 1 | -11.4736 | -0.0102 | 0.0000 |
| 2 | -8.3672 | 0.2281 | 0.0273 |
| 3 | -7.3796 | 0.0000 | 0.0000 |
| 4 | -6.2576 | -0.0000 | 0.0000 |
| 5 | -6.1494 | -0.0090 | 0.0000 |
| 6 | -6.0902 | 0.0000 | 0.0000 |
| 7 | -5.6667 | -0.0000 | 0.0000 |
| 8 | -5.5778 | 0.0000 | 0.0000 |
| 9 | -4.7218 | -0.0029 | 0.0000 |
| 10 | -4.4356 | -0.0000 | 0.0000 |

## Pembongkaran biaya

- Rerata biaya transaksi: **0.0170R**
- Rerata biaya funding: **0.0014R**
- Rerata jarak stop terhadap harga: **7.172%**
- Perdagangan dengan biaya melebihi 1R: **0** dari 59,324

## Parameter yang terpilih di dalam sampel

| Parameter | Jumlah jendela |
|---|---|
| `{"imbalan_R": 2.0, "lookback": 20}` | 1711 |
| `{"imbalan_R": 2.0, "lookback": 100}` | 1535 |
| `{"imbalan_R": 2.0, "lookback": 55}` | 836 |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| SANDUSDT | 12,011 | 20 | 288 | 70.13 | 0.24352 |
| BNBUSDT | 14,140 | 24 | 361 | 69.74 | 0.19318 |
| AXSUSDT | 12,437 | 20 | 327 | 67.33 | 0.20591 |
| RUNEUSDT | 12,899 | 21 | 291 | 61.07 | 0.20987 |
| XLMUSDT | 14,236 | 24 | 418 | 60.85 | 0.14557 |
| BTCUSDT | 14,388 | 24 | 327 | 57.95 | 0.17721 |
| ONEUSDT | 11,699 | 19 | 278 | 57.59 | 0.20715 |
| KSMUSDT | 12,629 | 21 | 271 | 53.00 | 0.19557 |
| SOLUSDT | 12,809 | 21 | 324 | 52.89 | 0.16324 |
| ALGOUSDT | 13,378 | 22 | 341 | 48.78 | 0.14306 |
