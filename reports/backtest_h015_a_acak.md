# Backtest H-015-A — h015_a_acak

> Sel A (pembanding, entri ditolak acak dengan cacah identik sel F) dari rancangan tiga sel ADR-037. Yang diuji bukan kelulusan sel ini melainkan selisih F − A: apakah saringan funding memuat INFORMASI, ataukah keunggulannya seluruhnya berasal dari kecondongan arah. Funding positif pada 79,1% periode, sehingga saringan apa pun membuang long jauh lebih sering daripada short dan akan mengalahkan kontrol tanpa memuat apa pun. Karena itu hanya ADR-037 §5 mengikat, dan selisih F − K haram dipakai sebagai dasar kelulusan.

Sidik `96fa54b7cca7abb1` · 9 kombinasi · 437 simbol · 223.0s

## Putusan

**DITOLAK**

Gerbang gagal: invarian_risiko, checksum

## Hasil luar sampel

- Perdagangan: **53,904**
- Total R: **4260.19**
- Ekspektasi: **0.07903293535777578**
- Jendela positif: 2260/4083
- Alasan keluar: {'target': 16956, 'stop': 30395, 'umur': 4937, 'akhir_data': 1590, 'carry': 26}
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
| 2020-07 | 13 | +4.71 | +0.362525 |
| 2020-08 | 30 | -9.39 | -0.312945 |
| 2020-09 | 78 | +24.82 | +0.318247 |
| 2020-10 | 96 | -17.81 | -0.185493 |
| 2020-11 | 65 | -37.38 | -0.575104 |
| 2020-12 | 85 | +3.73 | +0.043829 |
| 2021-01 | 66 | -34.65 | -0.524955 |
| 2021-02 | 68 | -12.44 | -0.182970 |
| 2021-03 | 74 | -20.58 | -0.278173 |
| 2021-04 | 91 | -45.52 | -0.500207 |
| 2021-05 | 312 | +72.76 | +0.233215 |
| 2021-06 | 380 | +39.41 | +0.103710 |
| 2021-07 | 454 | +104.98 | +0.231229 |
| 2021-08 | 394 | -64.58 | -0.163909 |
| 2021-09 | 267 | +30.16 | +0.112973 |
| 2021-10 | 254 | -79.79 | -0.314150 |
| 2021-11 | 207 | -26.70 | -0.129002 |
| 2021-12 | 450 | +73.43 | +0.163174 |
| 2022-01 | 592 | +255.48 | +0.431547 |
| 2022-02 | 509 | +43.77 | +0.085986 |
| 2022-03 | 678 | +198.73 | +0.293119 |
| 2022-04 | 579 | +112.59 | +0.194454 |
| 2022-05 | 633 | +111.69 | +0.176452 |
| 2022-06 | 441 | +93.64 | +0.212334 |
| 2022-07 | 558 | -90.17 | -0.161592 |
| 2022-08 | 467 | +54.51 | +0.116722 |
| 2022-09 | 324 | -156.65 | -0.483498 |
| 2022-10 | 531 | +21.54 | +0.040562 |
| 2022-11 | 574 | -35.54 | -0.061912 |
| 2022-12 | 534 | +13.36 | +0.025021 |
| 2023-01 | 912 | +405.31 | +0.444419 |
| 2023-02 | 351 | -31.20 | -0.088888 |
| 2023-03 | 558 | +72.97 | +0.130779 |
| 2023-04 | 485 | -104.39 | -0.215228 |
| 2023-05 | 521 | +50.29 | +0.096529 |
| 2023-06 | 666 | +178.16 | +0.267508 |
| 2023-07 | 437 | -139.97 | -0.320304 |
| 2023-08 | 595 | +73.87 | +0.124146 |
| 2023-09 | 478 | -62.31 | -0.130364 |
| 2023-10 | 857 | +115.15 | +0.134359 |
| 2023-11 | 634 | -266.14 | -0.419777 |
| 2023-12 | 236 | -66.02 | -0.279729 |
| 2024-01 | 418 | -126.19 | -0.301888 |
| 2024-02 | 620 | +131.00 | +0.211296 |
| 2024-03 | 289 | -7.88 | -0.027255 |
| 2024-04 | 779 | +382.79 | +0.491380 |
| 2024-05 | 936 | -281.62 | -0.300875 |
| 2024-06 | 992 | +182.84 | +0.184318 |
| 2024-07 | 1,344 | +545.63 | +0.405976 |
| 2024-08 | 1,445 | +672.04 | +0.465077 |
| 2024-09 | 1,077 | +54.19 | +0.050313 |
| 2024-10 | 990 | -172.48 | -0.174222 |
| 2024-11 | 1,329 | +421.15 | +0.316889 |
| 2024-12 | 820 | +94.42 | +0.115146 |
| 2025-01 | 1,179 | -103.03 | -0.087392 |
| 2025-02 | 1,350 | +314.90 | +0.233262 |
| 2025-03 | 1,282 | +365.06 | +0.284756 |
| 2025-04 | 1,420 | +395.80 | +0.278735 |
| 2025-05 | 1,648 | +308.22 | +0.187029 |
| 2025-06 | 1,330 | -237.78 | -0.178780 |
| 2025-07 | 1,760 | +450.27 | +0.255833 |
| 2025-08 | 1,229 | -619.58 | -0.504131 |
| 2025-09 | 1,406 | -63.85 | -0.045415 |
| 2025-10 | 1,735 | +217.49 | +0.125355 |
| 2025-11 | 1,358 | -10.07 | -0.007415 |
| 2025-12 | 1,574 | -217.22 | -0.138005 |
| 2026-01 | 2,221 | +1255.75 | +0.565400 |
| 2026-02 | 1,479 | -441.20 | -0.298311 |
| 2026-03 | 1,469 | -199.36 | -0.135709 |
| 2026-04 | 1,623 | -251.24 | -0.154798 |
| 2026-05 | 1,398 | +265.31 | +0.189778 |
| 2026-06 | 724 | +106.98 | +0.147759 |
| 2026-07 | 146 | -25.98 | -0.177961 |

## Sebaran R dan galat baku (ADR-013)

Sampai H-010 laporan hanya memuat rerata, sehingga tidak ada hipotesis yang dapat dinilai secara statistik: mustahil mengatakan apakah selisih terhadap ambang berarti sesuatu atau tidak.

**Galat baku di bawah adalah taksiran BAWAH.** Ia mengandaikan perdagangan saling bebas, dan andaian itu tidak benar: perdagangan dari puluhan simbol kripto pada jendela waktu yang bertumpang berkorelasi lewat gerakan pasar bersama. Galat sesungguhnya lebih besar, jadi keyakinan sesungguhnya lebih kecil. Angka ini sah dipakai untuk **menjatuhkan** klaim, dan tidak sah dipakai untuk **menegakkan** klaim.

- Simpangan baku per perdagangan: **1.37635R** (ddof=1, n = 53,904)
- Galat baku ekspektasi: **0.005928R**
- Selang 95% (pendekatan normal): **[0.067414, 0.090652]R**
- Kuartil R: min -11.4736 · Q1 -1.0273 · median -1.0077 · Q3 1.9553 · maks 3.9173
- Jarak ke ambang 0.05R: **+0.029033R** = **+4.90 galat baku**

## Sebelas gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0014 | 0.3 | 0 dari 437 simbol gagal |
| buy_and_hold | lulus | 0.8218 | 0.0 | median selisih 0.8218; unggul di 391/437 simbol |
| entri_acak | lulus | 0.0066 | 0.05 | 1 dari 300 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -11.4736 | -1.5 | kerugian terburuk -11.474R dari 53904 perdagangan |
| funding | lulus | 45172.6832 | 0.0 | total funding mutlak 45172.683151 atas 53904 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 437 simbol gagal |
| checksum | GAGAL | — | — | tidak dapat dinilai: manifest baru ditulis pada run ini |
| survivorship | lulus | 1.0000 | 0.5 | porsi delisted diuji 0.1465 vs universe 0.1465 |
| konsentrasi | lulus | 0.9890 | 0.6 | 321 untung / 116 rugi dari 437 simbol; drop-1 0.07817R (retensi 0.9890), drop-22 0.06693R, median simbol +0.07840R, porsi bruto teratas 0.0132 (RUNEUSDT), setara 193.5 simbol |
| funding_ekor | lulus | 0.0273 | 0.35 | porsi ekor maks 0.0273 (rerata 0.0028 atas 10 terburuk), funding maks 0.3531R, 26 dari 53904 trade di atas pengaman (0.00048) |

## Jackknife konsentrasi (ADR-010)

Buang penyumbang teratas satu per satu. Retensi adalah ekspektasi setelah pembuangan dibagi ekspektasi utuh. Ini menjawab pertanyaan yang sesungguhnya penting: apakah keunggulan tetap ada seandainya simbol paling untung tidak pernah ada.

| k | Dibuang | Simbol sisa | Trade | Total R | Ekspektasi R | Retensi |
|---|---|---|---|---|---|---|
| 0 | — | 437 | 53,904 | 4260.19 | 0.079033 | 1.0000 |
| 1 | RUNEUSDT | 436 | 53,633 | 4192.28 | 0.078166 | 0.9890 |
| 2 | SANDUSDT | 435 | 53,372 | 4126.72 | 0.077320 | 0.9783 |
| 3 | FILUSDT | 434 | 53,097 | 4066.33 | 0.076583 | 0.9690 |
| 4 | XLMUSDT | 433 | 52,759 | 4011.69 | 0.076038 | 0.9621 |
| 5 | ETHUSDT | 432 | 52,440 | 3960.17 | 0.075518 | 0.9555 |

## Ekor funding (ADR-011)

Gerbang funding lama menilai total mutlak dan memberi nilai yang praktis sama untuk dua keadaan yang ekornya berbeda 4,4 kali. Yang dinilai di sini adalah porsi funding terhadap kerugian pada sepuluh perdagangan terburuk, karena di situlah funding pernah menyumbang 46,7% kerugian sementara reratanya hanya 0,0004R.

- Porsi funding terbesar di ekor: **0.0273** (ambang 0,35)
- Rerata porsi di 10 terburuk: **0.0028**
- Funding terbesar satu perdagangan: **0.3531R** (ambang 0,50R)
- Perdagangan di atas pengaman 0,25R: **26** dari 53,904 (0.00048, ambang 0,005)

| # | R | Funding R | Porsi funding |
|---|---|---|---|
| 1 | -11.4736 | -0.0102 | 0.0000 |
| 2 | -8.3672 | 0.2281 | 0.0273 |
| 3 | -7.3796 | 0.0000 | 0.0000 |
| 4 | -6.2576 | -0.0000 | 0.0000 |
| 5 | -6.1494 | -0.0090 | 0.0000 |
| 6 | -6.0902 | 0.0000 | 0.0000 |
| 7 | -4.7218 | -0.0029 | 0.0000 |
| 8 | -4.4356 | -0.0000 | 0.0000 |
| 9 | -4.1287 | 0.0012 | 0.0003 |
| 10 | -4.0538 | 0.0000 | 0.0000 |

## Pembongkaran biaya

- Rerata biaya transaksi: **0.0173R**
- Rerata biaya funding: **-0.0032R**
- Rerata jarak stop terhadap harga: **7.042%**
- Perdagangan dengan biaya melebihi 1R: **0** dari 53,904

## Parameter yang terpilih di dalam sampel

| Parameter | Jumlah jendela |
|---|---|
| `{"imbalan_R": 2.0, "lookback": 20}` | 1937 |
| `{"imbalan_R": 2.0, "lookback": 100}` | 1223 |
| `{"imbalan_R": 2.0, "lookback": 55}` | 923 |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| RUNEUSDT | 12,905 | 21 | 271 | 67.91 | 0.25058 |
| SANDUSDT | 12,017 | 20 | 261 | 65.56 | 0.2512 |
| FILUSDT | 12,623 | 21 | 275 | 60.39 | 0.2196 |
| XLMUSDT | 14,242 | 24 | 338 | 54.64 | 0.16164 |
| ETHUSDT | 14,394 | 24 | 319 | 51.52 | 0.16151 |
| DOGEUSDT | 13,240 | 22 | 307 | 48.83 | 0.15907 |
| TRBUSDT | 12,881 | 21 | 233 | 48.23 | 0.20701 |
| AXSUSDT | 12,443 | 20 | 240 | 48.14 | 0.2006 |
| BTCUSDT | 14,394 | 24 | 291 | 45.28 | 0.1556 |
| VETUSDT | 14,092 | 24 | 248 | 44.51 | 0.17948 |
