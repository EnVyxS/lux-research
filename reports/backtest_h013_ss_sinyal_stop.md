# Backtest H-013-SS — h013_ss_sinyal_stop

> Sel SS dari rancangan faktorial 2x2 ADR-015 bagian B: sinyal Donchian sungguhan, geometri keluar stop + target. Yang diuji BUKAN kelulusan sel ini melainkan selisih antar sel: sumbangan sinyal SS - AS dengan ambang 0,020R, sumbangan geometri SS - SH, dan interaksinya. Skor entri acak H-010 dan H-012 identik sampai lima desimal pada 0,04661R sementara sinyal sungguhan bergerak di sekitarnya, sehingga kemungkinan paling sederhana adalah sinyalnya tidak menyumbang apa pun — dan kemungkinan itu belum pernah diuji sekali pun dalam dua belas hipotesis.

Sidik `06c3805bdd7ad4de` · 9 kombinasi · 437 simbol · 129.6s

## Putusan

**DITOLAK**

Gerbang gagal: invarian_risiko, checksum

## Hasil luar sampel

- Perdagangan: **60,018**
- Total R: **4000.07**
- Ekspektasi: **0.06664781299919262**
- Jendela positif: 2250/4082
- Alasan keluar: {'target': 18293, 'stop': 33467, 'carry': 92, 'umur': 6474, 'akhir_data': 1692}
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
| 2020-07 | 39 | +23.93 | +0.613653 |
| 2020-08 | 81 | -35.22 | -0.434826 |
| 2020-09 | 111 | +17.82 | +0.160510 |
| 2020-10 | 127 | -25.17 | -0.198180 |
| 2020-11 | 172 | -11.63 | -0.067617 |
| 2020-12 | 144 | +13.62 | +0.094565 |
| 2021-01 | 209 | -40.85 | -0.195478 |
| 2021-02 | 241 | +78.12 | +0.324153 |
| 2021-03 | 218 | +2.08 | +0.009547 |
| 2021-04 | 262 | +37.97 | +0.144922 |
| 2021-05 | 360 | +104.21 | +0.289458 |
| 2021-06 | 315 | +39.64 | +0.125829 |
| 2021-07 | 343 | +44.85 | +0.130753 |
| 2021-08 | 427 | -7.83 | -0.018327 |
| 2021-09 | 345 | -62.27 | -0.180484 |
| 2021-10 | 491 | -59.82 | -0.121842 |
| 2021-11 | 449 | -72.99 | -0.162566 |
| 2021-12 | 539 | +89.37 | +0.165798 |
| 2022-01 | 623 | +274.16 | +0.440060 |
| 2022-02 | 554 | +46.10 | +0.083207 |
| 2022-03 | 686 | +180.03 | +0.262429 |
| 2022-04 | 607 | +113.97 | +0.187766 |
| 2022-05 | 664 | +154.13 | +0.232124 |
| 2022-06 | 560 | +188.70 | +0.336962 |
| 2022-07 | 538 | -103.35 | -0.192093 |
| 2022-08 | 490 | -12.00 | -0.024496 |
| 2022-09 | 376 | -182.19 | -0.484561 |
| 2022-10 | 576 | +34.87 | +0.060533 |
| 2022-11 | 594 | -30.23 | -0.050887 |
| 2022-12 | 586 | +42.20 | +0.072020 |
| 2023-01 | 953 | +389.83 | +0.409058 |
| 2023-02 | 551 | -70.52 | -0.127978 |
| 2023-03 | 622 | +91.78 | +0.147553 |
| 2023-04 | 531 | -149.25 | -0.281072 |
| 2023-05 | 544 | +39.09 | +0.071857 |
| 2023-06 | 671 | +170.73 | +0.254439 |
| 2023-07 | 449 | -143.76 | -0.320176 |
| 2023-08 | 596 | +61.98 | +0.103985 |
| 2023-09 | 499 | -83.96 | -0.168253 |
| 2023-10 | 862 | +74.59 | +0.086528 |
| 2023-11 | 778 | -288.12 | -0.370336 |
| 2023-12 | 881 | -80.78 | -0.091696 |
| 2024-01 | 660 | -205.82 | -0.311845 |
| 2024-02 | 989 | +307.02 | +0.310436 |
| 2024-03 | 849 | -113.90 | -0.134157 |
| 2024-04 | 944 | +171.07 | +0.181222 |
| 2024-05 | 802 | -247.73 | -0.308887 |
| 2024-06 | 923 | +220.28 | +0.238660 |
| 2024-07 | 1,118 | +438.34 | +0.392077 |
| 2024-08 | 1,386 | +679.15 | +0.490007 |
| 2024-09 | 1,050 | +52.15 | +0.049666 |
| 2024-10 | 976 | -208.98 | -0.214120 |
| 2024-11 | 1,515 | +529.66 | +0.349609 |
| 2024-12 | 1,148 | +3.46 | +0.003015 |
| 2025-01 | 1,310 | -111.65 | -0.085229 |
| 2025-02 | 1,418 | +293.41 | +0.206916 |
| 2025-03 | 1,344 | +319.59 | +0.237791 |
| 2025-04 | 1,478 | +388.22 | +0.262666 |
| 2025-05 | 1,690 | +318.77 | +0.188622 |
| 2025-06 | 1,319 | -247.39 | -0.187560 |
| 2025-07 | 1,790 | +470.05 | +0.262596 |
| 2025-08 | 1,290 | -604.62 | -0.468697 |
| 2025-09 | 1,447 | -41.91 | -0.028961 |
| 2025-10 | 1,806 | +255.91 | +0.141701 |
| 2025-11 | 1,546 | -84.57 | -0.054700 |
| 2025-12 | 1,804 | -262.92 | -0.145744 |
| 2026-01 | 2,458 | +1436.58 | +0.584452 |
| 2026-02 | 1,732 | -469.01 | -0.270790 |
| 2026-03 | 1,606 | -244.51 | -0.152246 |
| 2026-04 | 1,653 | -237.24 | -0.143519 |
| 2026-05 | 1,432 | +208.37 | +0.145512 |
| 2026-06 | 748 | +168.45 | +0.225198 |
| 2026-07 | 123 | -33.98 | -0.276260 |

## Sebaran R dan galat baku (ADR-013)

Sampai H-010 laporan hanya memuat rerata, sehingga tidak ada hipotesis yang dapat dinilai secara statistik: mustahil mengatakan apakah selisih terhadap ambang berarti sesuatu atau tidak.

**Galat baku di bawah adalah taksiran BAWAH.** Ia mengandaikan perdagangan saling bebas, dan andaian itu tidak benar: perdagangan dari puluhan simbol kripto pada jendela waktu yang bertumpang berkorelasi lewat gerakan pasar bersama. Galat sesungguhnya lebih besar, jadi keyakinan sesungguhnya lebih kecil. Angka ini sah dipakai untuk **menjatuhkan** klaim, dan tidak sah dipakai untuk **menegakkan** klaim.

- Simpangan baku per perdagangan: **1.36459R** (ddof=1, n = 60,018)
- Galat baku ekspektasi: **0.005570R**
- Selang 95% (pendekatan normal): **[0.055731, 0.077565]R**
- Kuartil R: min -11.4736 · Q1 -1.0286 · median -1.0087 · Q3 1.9495 · maks 3.9173
- Jarak ke ambang 0.05R: **+0.016648R** = **+2.99 galat baku**

## Sebelas gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0014 | 0.3 | 0 dari 437 simbol gagal |
| buy_and_hold | lulus | 0.8096 | 0.0 | median selisih 0.8096; unggul di 391/437 simbol |
| entri_acak | lulus | 0.0166 | 0.05 | 4 dari 300 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -11.4736 | -1.5 | kerugian terburuk -11.474R dari 60018 perdagangan |
| funding | lulus | 55973.3510 | 0.0 | total funding mutlak 55973.351010 atas 60018 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 437 simbol gagal |
| checksum | GAGAL | 24.0000 | 0.0 | hilang 12, asing 12, tidak cocok 0 |
| survivorship | lulus | 1.0000 | 0.5 | porsi delisted diuji 0.1465 vs universe 0.1465 |
| konsentrasi | lulus | 0.9866 | 0.6 | 317 untung / 120 rugi dari 437 simbol; drop-1 0.06575R (retensi 0.9866), drop-22 0.05400R, median simbol +0.06697R, porsi bruto teratas 0.0155 (BNBUSDT), setara 182.7 simbol |
| funding_ekor | lulus | 0.0273 | 0.35 | porsi ekor maks 0.0273 (rerata 0.0027 atas 10 terburuk), funding maks 0.4243R, 93 dari 60018 trade di atas pengaman (0.00155) |

## Jackknife konsentrasi (ADR-010)

Buang penyumbang teratas satu per satu. Retensi adalah ekspektasi setelah pembuangan dibagi ekspektasi utuh. Ini menjawab pertanyaan yang sesungguhnya penting: apakah keunggulan tetap ada seandainya simbol paling untung tidak pernah ada.

| k | Dibuang | Simbol sisa | Trade | Total R | Ekspektasi R | Retensi |
|---|---|---|---|---|---|---|
| 0 | — | 437 | 60,018 | 4000.07 | 0.066648 | 1.0000 |
| 1 | BNBUSDT | 436 | 59,652 | 3922.38 | 0.065754 | 0.9866 |
| 2 | AXSUSDT | 435 | 59,350 | 3852.41 | 0.064910 | 0.9739 |
| 3 | SANDUSDT | 434 | 59,071 | 3784.56 | 0.064068 | 0.9613 |
| 4 | XLMUSDT | 433 | 58,646 | 3725.28 | 0.063521 | 0.9531 |
| 5 | RUNEUSDT | 432 | 58,342 | 3671.80 | 0.062936 | 0.9443 |

## Ekor funding (ADR-011)

Gerbang funding lama menilai total mutlak dan memberi nilai yang praktis sama untuk dua keadaan yang ekornya berbeda 4,4 kali. Yang dinilai di sini adalah porsi funding terhadap kerugian pada sepuluh perdagangan terburuk, karena di situlah funding pernah menyumbang 46,7% kerugian sementara reratanya hanya 0,0004R.

- Porsi funding terbesar di ekor: **0.0273** (ambang 0,35)
- Rerata porsi di 10 terburuk: **0.0027**
- Funding terbesar satu perdagangan: **0.4243R** (ambang 0,50R)
- Perdagangan di atas pengaman 0,25R: **93** dari 60,018 (0.00155, ambang 0,005)

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
- Rerata biaya funding: **0.0016R**
- Rerata jarak stop terhadap harga: **7.170%**
- Perdagangan dengan biaya melebihi 1R: **0** dari 60,018

## Parameter yang terpilih di dalam sampel

| Parameter | Jumlah jendela |
|---|---|
| `{"imbalan_R": 2.0, "lookback": 20}` | 1682 |
| `{"imbalan_R": 2.0, "lookback": 100}` | 1554 |
| `{"imbalan_R": 2.0, "lookback": 55}` | 846 |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| BNBUSDT | 14,140 | 24 | 366 | 77.69 | 0.21227 |
| AXSUSDT | 12,437 | 20 | 302 | 69.97 | 0.23168 |
| SANDUSDT | 12,011 | 20 | 279 | 67.85 | 0.24319 |
| XLMUSDT | 14,236 | 24 | 425 | 59.28 | 0.13948 |
| RUNEUSDT | 12,899 | 21 | 304 | 53.48 | 0.17593 |
| KSMUSDT | 12,629 | 21 | 273 | 52.90 | 0.19377 |
| MANAUSDT | 11,717 | 19 | 266 | 52.74 | 0.19826 |
| SOLUSDT | 12,809 | 21 | 334 | 49.96 | 0.14957 |
| NEARUSDT | 12,622 | 21 | 300 | 48.53 | 0.16176 |
| FTMUSDT | 9,362 | 15 | 242 | 48.36 | 0.19984 |
