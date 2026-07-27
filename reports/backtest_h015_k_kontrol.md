# Backtest H-015-K — h015_k_kontrol

> Sel K (kontrol, Donchian apa adanya) dari rancangan tiga sel ADR-037. Yang diuji bukan kelulusan sel ini melainkan selisih F − A: apakah saringan funding memuat INFORMASI, ataukah keunggulannya seluruhnya berasal dari kecondongan arah. Funding positif pada 79,1% periode, sehingga saringan apa pun membuang long jauh lebih sering daripada short dan akan mengalahkan kontrol tanpa memuat apa pun. Karena itu hanya ADR-037 §5 mengikat, dan selisih F − K haram dipakai sebagai dasar kelulusan.

Sidik `61dc0acf646d5b69` · 9 kombinasi · 437 simbol · 136.0s

## Putusan

**DITOLAK**

Gerbang gagal: invarian_risiko, checksum

## Hasil luar sampel

- Perdagangan: **59,306**
- Total R: **4016.87**
- Ekspektasi: **0.06773132069859376**
- Jendela positif: 2228/4085
- Alasan keluar: {'target': 18643, 'stop': 33703, 'carry': 82, 'umur': 5149, 'akhir_data': 1729}
- Entri ditolak pengaman biaya (ADR-014): **0**, pengaman 0.5R

Penolakan pengaman biaya **bukan perdagangan** dan karena itu tidak muncul di histogram alasan keluar maupun di jumlah perdagangan di atas. Angka itu juga **tidak** mengukur seluruh keadaan degenerat: pada simbol yang seluruhnya degenerat, pengaman menolak entri juga saat pemilihan parameter, sehingga semua kandidat berskor -inf, seluruh jendelanya dilewati, dan simbol itu menyumbang nol penolakan sekaligus nol perdagangan. Yang tercatat di sini hanyalah simbol yang berubah degenerat di tengah jalan; simbol yang degenerat sepanjang riwayatnya hanya terlihat di lantai semesta di bawah.

## Lantai satuan R pada semesta (ADR-014)

Lantai median `stop_frac` **0.004**, diturunkan dari aritmetika biaya dan bukan disetel: biaya bolak-balik 0,002 dari harga menjadi tepat 0,5R di lantai itu. Kriteria ini seragam dan dipra-registrasi, sehingga ia bukan penyubsetan simbol pasca-hasil.

- Simbol dinilai: **438**
- Layak: **437**
- Dibuang: **1**

| Simbol | median stop_frac | biaya masuk R | Sebab |
|---|---|---|---|
| USDCUSDT | 3.797195e-04 | 5.27 | median jarak stop 3.797e-04 di bawah lantai 0.004 |

## Hasil menurut bulan masuk (ADR-014)

Setiap perdagangan dimiliki oleh bulan kalender UTC tempat ia **dibuka**, karena keputusan yang diuji adalah keputusan masuk. Akibatnya ada rembesan yang wajib dinyatakan: perdagangan yang dibuka sesaat sebelum batas sebuah periode dapat ditutup sesudahnya, dan besarnya rembesan itu terbatas oleh `maks_umur_bar` (48 bar).

Tabel ini **bukan** putusan dan bukan pula izin memilih periode terbaik sesudah melihatnya. Memilih periode setelah hasil terlihat adalah penyubsetan yang sama terlarangnya dengan memilih simbol.

| Bulan masuk | Trade | Total R | Ekspektasi R |
|---|---|---|---|
| 2020-07 | 38 | +20.47 | +0.538735 |
| 2020-08 | 78 | -29.55 | -0.378833 |
| 2020-09 | 103 | +17.01 | +0.165159 |
| 2020-10 | 118 | -26.41 | -0.223771 |
| 2020-11 | 160 | -1.09 | -0.006793 |
| 2020-12 | 130 | +1.69 | +0.013011 |
| 2021-01 | 201 | -48.64 | -0.241988 |
| 2021-02 | 226 | +88.82 | +0.393020 |
| 2021-03 | 198 | -9.10 | -0.045952 |
| 2021-04 | 247 | +25.13 | +0.101756 |
| 2021-05 | 351 | +99.69 | +0.284024 |
| 2021-06 | 311 | +43.14 | +0.138702 |
| 2021-07 | 346 | +30.01 | +0.086737 |
| 2021-08 | 418 | +6.39 | +0.015277 |
| 2021-09 | 347 | -71.52 | -0.206111 |
| 2021-10 | 489 | -61.73 | -0.126237 |
| 2021-11 | 435 | -52.49 | -0.120664 |
| 2021-12 | 527 | +76.76 | +0.145661 |
| 2022-01 | 617 | +272.86 | +0.442229 |
| 2022-02 | 554 | +50.61 | +0.091358 |
| 2022-03 | 683 | +194.44 | +0.284689 |
| 2022-04 | 599 | +111.93 | +0.186857 |
| 2022-05 | 643 | +151.58 | +0.235738 |
| 2022-06 | 552 | +138.43 | +0.250778 |
| 2022-07 | 547 | -105.65 | -0.193146 |
| 2022-08 | 480 | +45.75 | +0.095308 |
| 2022-09 | 377 | -185.63 | -0.492385 |
| 2022-10 | 565 | +38.43 | +0.068013 |
| 2022-11 | 589 | -13.15 | -0.022331 |
| 2022-12 | 573 | +40.97 | +0.071495 |
| 2023-01 | 931 | +397.28 | +0.426724 |
| 2023-02 | 526 | -63.97 | -0.121618 |
| 2023-03 | 618 | +80.06 | +0.129552 |
| 2023-04 | 529 | -111.28 | -0.210366 |
| 2023-05 | 536 | +50.27 | +0.093791 |
| 2023-06 | 670 | +177.69 | +0.265214 |
| 2023-07 | 437 | -151.57 | -0.346846 |
| 2023-08 | 607 | +75.94 | +0.125114 |
| 2023-09 | 491 | -78.20 | -0.159261 |
| 2023-10 | 871 | +93.42 | +0.107255 |
| 2023-11 | 765 | -273.83 | -0.357952 |
| 2023-12 | 876 | -54.69 | -0.062429 |
| 2024-01 | 656 | -250.57 | -0.381964 |
| 2024-02 | 979 | +299.93 | +0.306365 |
| 2024-03 | 826 | -135.71 | -0.164296 |
| 2024-04 | 926 | +202.07 | +0.218214 |
| 2024-05 | 797 | -291.65 | -0.365935 |
| 2024-06 | 899 | +221.58 | +0.246474 |
| 2024-07 | 1,075 | +393.00 | +0.365578 |
| 2024-08 | 1,349 | +644.69 | +0.477904 |
| 2024-09 | 1,029 | +83.16 | +0.080812 |
| 2024-10 | 955 | -186.03 | -0.194791 |
| 2024-11 | 1,504 | +526.73 | +0.350218 |
| 2024-12 | 1,144 | -4.72 | -0.004128 |
| 2025-01 | 1,275 | -117.96 | -0.092514 |
| 2025-02 | 1,404 | +301.00 | +0.214390 |
| 2025-03 | 1,323 | +347.02 | +0.262299 |
| 2025-04 | 1,446 | +389.93 | +0.269660 |
| 2025-05 | 1,632 | +291.11 | +0.178375 |
| 2025-06 | 1,303 | -226.55 | -0.173869 |
| 2025-07 | 1,763 | +446.11 | +0.253039 |
| 2025-08 | 1,268 | -625.01 | -0.492910 |
| 2025-09 | 1,458 | -41.75 | -0.028633 |
| 2025-10 | 1,859 | +227.09 | +0.122155 |
| 2025-11 | 1,545 | +1.71 | +0.001105 |
| 2025-12 | 1,809 | -292.89 | -0.161909 |
| 2026-01 | 2,458 | +1398.57 | +0.568989 |
| 2026-02 | 1,695 | -488.11 | -0.287973 |
| 2026-03 | 1,568 | -216.18 | -0.137871 |
| 2026-04 | 1,656 | -225.20 | -0.135989 |
| 2026-05 | 1,444 | +246.98 | +0.171037 |
| 2026-06 | 759 | +153.67 | +0.202465 |
| 2026-07 | 143 | -45.42 | -0.317628 |

## Sebaran R dan galat baku (ADR-013)

Sampai H-010 laporan hanya memuat rerata, sehingga tidak ada hipotesis yang dapat dinilai secara statistik: mustahil mengatakan apakah selisih terhadap ambang berarti sesuatu atau tidak.

**Galat baku di bawah adalah taksiran BAWAH.** Ia mengandaikan perdagangan saling bebas, dan andaian itu tidak benar: perdagangan dari puluhan simbol kripto pada jendela waktu yang bertumpang berkorelasi lewat gerakan pasar bersama. Galat sesungguhnya lebih besar, jadi keyakinan sesungguhnya lebih kecil. Angka ini sah dipakai untuk **menjatuhkan** klaim, dan tidak sah dipakai untuk **menegakkan** klaim.

- Simpangan baku per perdagangan: **1.37780R** (ddof=1, n = 59,306)
- Galat baku ekspektasi: **0.005658R**
- Selang 95% (pendekatan normal): **[0.056642, 0.078820]R**
- Kuartil R: min -11.4736 · Q1 -1.0289 · median -1.0095 · Q3 1.9521 · maks 3.9173
- Jarak ke ambang 0.05R: **+0.017731R** = **+3.13 galat baku**

## Sebelas gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0014 | 0.3 | 0 dari 437 simbol gagal |
| buy_and_hold | lulus | 0.8150 | 0.0 | median selisih 0.8150; unggul di 392/437 simbol |
| entri_acak | lulus | 0.0100 | 0.05 | 2 dari 300 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -11.4736 | -1.5 | kerugian terburuk -11.474R dari 59306 perdagangan |
| funding | lulus | 55925.6083 | 0.0 | total funding mutlak 55925.608330 atas 59306 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 437 simbol gagal |
| checksum | GAGAL | — | — | tidak dapat dinilai: manifest baru ditulis pada run ini |
| survivorship | lulus | 1.0000 | 0.5 | porsi delisted diuji 0.1465 vs universe 0.1465 |
| konsentrasi | lulus | 0.9873 | 0.6 | 308 untung / 129 rugi dari 437 simbol; drop-1 0.06687R (retensi 0.9873), drop-22 0.05488R, median simbol +0.06711R, porsi bruto teratas 0.0139 (SANDUSDT), setara 181.0 simbol |
| funding_ekor | lulus | 0.0273 | 0.35 | porsi ekor maks 0.0273 (rerata 0.0027 atas 10 terburuk), funding maks 0.4243R, 84 dari 59306 trade di atas pengaman (0.00142) |

## Jackknife konsentrasi (ADR-010)

Buang penyumbang teratas satu per satu. Retensi adalah ekspektasi setelah pembuangan dibagi ekspektasi utuh. Ini menjawab pertanyaan yang sesungguhnya penting: apakah keunggulan tetap ada seandainya simbol paling untung tidak pernah ada.

| k | Dibuang | Simbol sisa | Trade | Total R | Ekspektasi R | Retensi |
|---|---|---|---|---|---|---|
| 0 | — | 437 | 59,306 | 4016.87 | 0.067731 | 1.0000 |
| 1 | SANDUSDT | 436 | 59,018 | 3946.74 | 0.066874 | 0.9873 |
| 2 | BNBUSDT | 435 | 58,657 | 3878.08 | 0.066115 | 0.9761 |
| 3 | AXSUSDT | 434 | 58,330 | 3810.75 | 0.065331 | 0.9646 |
| 4 | RUNEUSDT | 433 | 58,039 | 3749.68 | 0.064606 | 0.9539 |
| 5 | XLMUSDT | 432 | 57,621 | 3688.83 | 0.064019 | 0.9452 |

## Ekor funding (ADR-011)

Gerbang funding lama menilai total mutlak dan memberi nilai yang praktis sama untuk dua keadaan yang ekornya berbeda 4,4 kali. Yang dinilai di sini adalah porsi funding terhadap kerugian pada sepuluh perdagangan terburuk, karena di situlah funding pernah menyumbang 46,7% kerugian sementara reratanya hanya 0,0004R.

- Porsi funding terbesar di ekor: **0.0273** (ambang 0,35)
- Rerata porsi di 10 terburuk: **0.0027**
- Funding terbesar satu perdagangan: **0.4243R** (ambang 0,50R)
- Perdagangan di atas pengaman 0,25R: **84** dari 59,306 (0.00142, ambang 0,005)

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
- Rerata biaya funding: **0.0012R**
- Rerata jarak stop terhadap harga: **7.173%**
- Perdagangan dengan biaya melebihi 1R: **0** dari 59,306

## Parameter yang terpilih di dalam sampel

| Parameter | Jumlah jendela |
|---|---|
| `{"imbalan_R": 2.0, "lookback": 20}` | 1707 |
| `{"imbalan_R": 2.0, "lookback": 100}` | 1542 |
| `{"imbalan_R": 2.0, "lookback": 55}` | 836 |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| SANDUSDT | 12,017 | 20 | 288 | 70.13 | 0.24352 |
| BNBUSDT | 14,146 | 24 | 361 | 68.66 | 0.19019 |
| AXSUSDT | 12,443 | 20 | 327 | 67.33 | 0.20591 |
| RUNEUSDT | 12,905 | 21 | 291 | 61.07 | 0.20987 |
| XLMUSDT | 14,242 | 24 | 418 | 60.85 | 0.14557 |
| ONEUSDT | 11,705 | 19 | 278 | 57.59 | 0.20715 |
| BTCUSDT | 14,394 | 24 | 327 | 56.52 | 0.17285 |
| SOLUSDT | 12,815 | 21 | 324 | 53.11 | 0.16392 |
| KSMUSDT | 12,635 | 21 | 271 | 53.06 | 0.19578 |
| ALGOUSDT | 13,384 | 22 | 341 | 48.78 | 0.14306 |
