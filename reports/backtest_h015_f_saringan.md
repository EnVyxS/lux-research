# Backtest H-015-F — h015_f_saringan

> Sel F (hipotesis, entri ditolak saringan funding) dari rancangan tiga sel ADR-037. Yang diuji bukan kelulusan sel ini melainkan selisih F − A: apakah saringan funding memuat INFORMASI, ataukah keunggulannya seluruhnya berasal dari kecondongan arah. Funding positif pada 79,1% periode, sehingga saringan apa pun membuang long jauh lebih sering daripada short dan akan mengalahkan kontrol tanpa memuat apa pun. Karena itu hanya ADR-037 §5 mengikat, dan selisih F − K haram dipakai sebagai dasar kelulusan.

Sidik `f4b823362d12c27b` · 9 kombinasi · 437 simbol · 137.1s

## Putusan

**DITOLAK**

Gerbang gagal: invarian_risiko, checksum

## Hasil luar sampel

- Perdagangan: **53,025**
- Total R: **4306.42**
- Ekspektasi: **0.08121494707506911**
- Jendela positif: 2269/4083
- Alasan keluar: {'target': 16706, 'stop': 29835, 'umur': 4881, 'akhir_data': 1576, 'carry': 27}
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
| 2020-07 | 9 | +5.20 | +0.577962 |
| 2020-08 | 28 | -5.56 | -0.198507 |
| 2020-09 | 68 | +18.03 | +0.265097 |
| 2020-10 | 95 | -13.91 | -0.146404 |
| 2020-11 | 49 | -16.15 | -0.329628 |
| 2020-12 | 85 | +12.82 | +0.150808 |
| 2021-01 | 66 | -41.87 | -0.634423 |
| 2021-02 | 71 | -11.97 | -0.168538 |
| 2021-03 | 78 | -25.27 | -0.323946 |
| 2021-04 | 86 | -43.35 | -0.504100 |
| 2021-05 | 311 | +68.10 | +0.218987 |
| 2021-06 | 362 | +36.49 | +0.100798 |
| 2021-07 | 452 | +100.25 | +0.221799 |
| 2021-08 | 301 | -18.83 | -0.062546 |
| 2021-09 | 271 | +37.32 | +0.137702 |
| 2021-10 | 240 | -112.42 | -0.468396 |
| 2021-11 | 210 | -21.43 | -0.102064 |
| 2021-12 | 447 | +50.73 | +0.113497 |
| 2022-01 | 600 | +249.53 | +0.415885 |
| 2022-02 | 519 | +57.36 | +0.110517 |
| 2022-03 | 689 | +190.73 | +0.276823 |
| 2022-04 | 586 | +119.36 | +0.203691 |
| 2022-05 | 622 | +124.89 | +0.200788 |
| 2022-06 | 410 | +96.37 | +0.235060 |
| 2022-07 | 537 | -69.58 | -0.129578 |
| 2022-08 | 459 | +49.43 | +0.107686 |
| 2022-09 | 327 | -168.68 | -0.515849 |
| 2022-10 | 528 | +22.10 | +0.041854 |
| 2022-11 | 559 | -15.25 | -0.027274 |
| 2022-12 | 527 | +16.33 | +0.030981 |
| 2023-01 | 895 | +423.96 | +0.473704 |
| 2023-02 | 339 | -7.76 | -0.022886 |
| 2023-03 | 560 | +68.49 | +0.122307 |
| 2023-04 | 473 | -94.82 | -0.200458 |
| 2023-05 | 515 | +55.15 | +0.107086 |
| 2023-06 | 670 | +185.92 | +0.277488 |
| 2023-07 | 447 | -141.58 | -0.316739 |
| 2023-08 | 597 | +74.46 | +0.124726 |
| 2023-09 | 486 | -72.85 | -0.149906 |
| 2023-10 | 871 | +110.41 | +0.126766 |
| 2023-11 | 587 | -226.93 | -0.386595 |
| 2023-12 | 226 | -85.10 | -0.376551 |
| 2024-01 | 412 | -127.10 | -0.308505 |
| 2024-02 | 509 | +171.08 | +0.336109 |
| 2024-03 | 299 | -7.21 | -0.024129 |
| 2024-04 | 788 | +395.38 | +0.501749 |
| 2024-05 | 948 | -289.06 | -0.304916 |
| 2024-06 | 974 | +193.14 | +0.198299 |
| 2024-07 | 1,331 | +541.73 | +0.407010 |
| 2024-08 | 1,438 | +660.49 | +0.459308 |
| 2024-09 | 1,082 | +62.26 | +0.057542 |
| 2024-10 | 1,005 | -186.35 | -0.185423 |
| 2024-11 | 1,168 | +324.10 | +0.277486 |
| 2024-12 | 807 | +109.81 | +0.136071 |
| 2025-01 | 1,168 | -97.33 | -0.083334 |
| 2025-02 | 1,359 | +293.80 | +0.216188 |
| 2025-03 | 1,272 | +337.98 | +0.265711 |
| 2025-04 | 1,402 | +393.03 | +0.280336 |
| 2025-05 | 1,614 | +305.75 | +0.189434 |
| 2025-06 | 1,313 | -248.22 | -0.189045 |
| 2025-07 | 1,755 | +450.18 | +0.256513 |
| 2025-08 | 1,226 | -624.47 | -0.509355 |
| 2025-09 | 1,397 | -65.22 | -0.046689 |
| 2025-10 | 1,725 | +232.31 | +0.134671 |
| 2025-11 | 1,336 | -21.96 | -0.016434 |
| 2025-12 | 1,536 | -226.72 | -0.147607 |
| 2026-01 | 2,204 | +1248.75 | +0.566582 |
| 2026-02 | 1,445 | -412.62 | -0.285547 |
| 2026-03 | 1,426 | -181.95 | -0.127592 |
| 2026-04 | 1,589 | -239.12 | -0.150482 |
| 2026-05 | 1,386 | +252.27 | +0.182015 |
| 2026-06 | 707 | +106.99 | +0.151334 |
| 2026-07 | 146 | -25.44 | -0.174214 |

## Sebaran R dan galat baku (ADR-013)

Sampai H-010 laporan hanya memuat rerata, sehingga tidak ada hipotesis yang dapat dinilai secara statistik: mustahil mengatakan apakah selisih terhadap ambang berarti sesuatu atau tidak.

**Galat baku di bawah adalah taksiran BAWAH.** Ia mengandaikan perdagangan saling bebas, dan andaian itu tidak benar: perdagangan dari puluhan simbol kripto pada jendela waktu yang bertumpang berkorelasi lewat gerakan pasar bersama. Galat sesungguhnya lebih besar, jadi keyakinan sesungguhnya lebih kecil. Angka ini sah dipakai untuk **menjatuhkan** klaim, dan tidak sah dipakai untuk **menegakkan** klaim.

- Simpangan baku per perdagangan: **1.37651R** (ddof=1, n = 53,025)
- Galat baku ekspektasi: **0.005978R**
- Selang 95% (pendekatan normal): **[0.069499, 0.092931]R**
- Kuartil R: min -11.4736 · Q1 -1.0270 · median -1.0072 · Q3 1.9554 · maks 3.9173
- Jarak ke ambang 0.05R: **+0.031215R** = **+5.22 galat baku**

## Sebelas gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0014 | 0.3 | 0 dari 437 simbol gagal |
| buy_and_hold | lulus | 0.8224 | 0.0 | median selisih 0.8224; unggul di 393/437 simbol |
| entri_acak | lulus | 0.0100 | 0.05 | 2 dari 300 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -11.4736 | -1.5 | kerugian terburuk -11.474R dari 53025 perdagangan |
| funding | lulus | 44134.2410 | 0.0 | total funding mutlak 44134.240990 atas 53025 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 437 simbol gagal |
| checksum | GAGAL | — | — | tidak dapat dinilai: manifest baru ditulis pada run ini |
| survivorship | lulus | 1.0000 | 0.5 | porsi delisted diuji 0.1465 vs universe 0.1465 |
| konsentrasi | lulus | 0.9873 | 0.6 | 314 untung / 123 rugi dari 437 simbol; drop-1 0.08018R (retensi 0.9873), drop-22 0.06783R, median simbol +0.08248R, porsi bruto teratas 0.0155 (XLMUSDT), setara 189.6 simbol |
| funding_ekor | lulus | 0.0273 | 0.35 | porsi ekor maks 0.0273 (rerata 0.0028 atas 10 terburuk), funding maks 0.3531R, 27 dari 53025 trade di atas pengaman (0.00051) |

## Jackknife konsentrasi (ADR-010)

Buang penyumbang teratas satu per satu. Retensi adalah ekspektasi setelah pembuangan dibagi ekspektasi utuh. Ini menjawab pertanyaan yang sesungguhnya penting: apakah keunggulan tetap ada seandainya simbol paling untung tidak pernah ada.

| k | Dibuang | Simbol sisa | Trade | Total R | Ekspektasi R | Retensi |
|---|---|---|---|---|---|---|
| 0 | — | 437 | 53,025 | 4306.42 | 0.081215 | 1.0000 |
| 1 | XLMUSDT | 436 | 52,696 | 4225.36 | 0.080184 | 0.9873 |
| 2 | RUNEUSDT | 435 | 52,433 | 4160.25 | 0.079344 | 0.9770 |
| 3 | SANDUSDT | 434 | 52,163 | 4096.12 | 0.078525 | 0.9669 |
| 4 | AXSUSDT | 433 | 51,930 | 4036.08 | 0.077721 | 0.9570 |
| 5 | VETUSDT | 432 | 51,676 | 3982.08 | 0.077059 | 0.9488 |

## Ekor funding (ADR-011)

Gerbang funding lama menilai total mutlak dan memberi nilai yang praktis sama untuk dua keadaan yang ekornya berbeda 4,4 kali. Yang dinilai di sini adalah porsi funding terhadap kerugian pada sepuluh perdagangan terburuk, karena di situlah funding pernah menyumbang 46,7% kerugian sementara reratanya hanya 0,0004R.

- Porsi funding terbesar di ekor: **0.0273** (ambang 0,35)
- Rerata porsi di 10 terburuk: **0.0028**
- Funding terbesar satu perdagangan: **0.3531R** (ambang 0,50R)
- Perdagangan di atas pengaman 0,25R: **27** dari 53,025 (0.00051, ambang 0,005)

| # | R | Funding R | Porsi funding |
|---|---|---|---|
| 1 | -11.4736 | -0.0102 | 0.0000 |
| 2 | -8.3672 | 0.2281 | 0.0273 |
| 3 | -7.3796 | 0.0000 | 0.0000 |
| 4 | -6.2576 | -0.0000 | 0.0000 |
| 5 | -6.1494 | -0.0090 | 0.0000 |
| 6 | -6.0902 | 0.0000 | 0.0000 |
| 7 | -5.6667 | -0.0000 | 0.0000 |
| 8 | -4.7218 | -0.0029 | 0.0000 |
| 9 | -4.4356 | -0.0000 | 0.0000 |
| 10 | -4.1287 | 0.0012 | 0.0003 |

## Pembongkaran biaya

- Rerata biaya transaksi: **0.0174R**
- Rerata biaya funding: **-0.0038R**
- Rerata jarak stop terhadap harga: **7.011%**
- Perdagangan dengan biaya melebihi 1R: **0** dari 53,025

## Parameter yang terpilih di dalam sampel

| Parameter | Jumlah jendela |
|---|---|
| `{"imbalan_R": 2.0, "lookback": 20}` | 1958 |
| `{"imbalan_R": 2.0, "lookback": 100}` | 1216 |
| `{"imbalan_R": 2.0, "lookback": 55}` | 909 |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| XLMUSDT | 14,242 | 24 | 329 | 81.06 | 0.24638 |
| RUNEUSDT | 12,905 | 21 | 263 | 65.12 | 0.24759 |
| SANDUSDT | 12,017 | 20 | 270 | 64.13 | 0.23752 |
| AXSUSDT | 12,443 | 20 | 233 | 60.04 | 0.25767 |
| VETUSDT | 14,092 | 24 | 254 | 54.00 | 0.21261 |
| FILUSDT | 12,623 | 21 | 266 | 51.07 | 0.19199 |
| BTCUSDT | 14,394 | 24 | 300 | 50.14 | 0.16714 |
| ETHUSDT | 14,394 | 24 | 316 | 47.70 | 0.15096 |
| DOGEUSDT | 13,240 | 22 | 334 | 46.15 | 0.13817 |
| GALAUSDT | 10,632 | 17 | 241 | 45.67 | 0.18949 |
