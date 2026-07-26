# Backtest H-013-SH — h013_sh_sinyal_horizon

> Sel SH dari rancangan faktorial 2x2 ADR-015 bagian B: sinyal Donchian sungguhan, geometri keluar horizon tetap 48 bar tanpa target. Yang diuji BUKAN kelulusan sel ini melainkan selisih antar sel: sumbangan sinyal SS - AS dengan ambang 0,020R, sumbangan geometri SS - SH, dan interaksinya. Skor entri acak H-010 dan H-012 identik sampai lima desimal pada 0,04661R sementara sinyal sungguhan bergerak di sekitarnya, sehingga kemungkinan paling sederhana adalah sinyalnya tidak menyumbang apa pun — dan kemungkinan itu belum pernah diuji sekali pun dalam dua belas hipotesis.

Sidik `af1145aab7f13567` · 9 kombinasi · 437 simbol · 137.9s

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- ekspektasi 0.0372R < 0.05R
- p entri acak 0.2259 > 0.05
- jendela positif 0.49 < 0.5

Gerbang gagal: entri_acak, invarian_risiko, checksum, funding_ekor

## Hasil luar sampel

- Perdagangan: **44,614**
- Total R: **1658.15**
- Ekspektasi: **0.037166633609032385**
- Jendela positif: 1981/4082
- Alasan keluar: {'umur': 14197, 'stop': 28010, 'carry': 320, 'akhir_data': 2087}
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
| 2020-07 | 29 | +17.83 | +0.614845 |
| 2020-08 | 77 | -40.30 | -0.523369 |
| 2020-09 | 89 | +9.36 | +0.105119 |
| 2020-10 | 114 | -35.42 | -0.310711 |
| 2020-11 | 113 | +10.75 | +0.095114 |
| 2020-12 | 91 | +3.32 | +0.036450 |
| 2021-01 | 138 | -3.73 | -0.027055 |
| 2021-02 | 138 | +96.46 | +0.698957 |
| 2021-03 | 155 | -18.84 | -0.121559 |
| 2021-04 | 193 | +49.06 | +0.254217 |
| 2021-05 | 250 | +10.68 | +0.042721 |
| 2021-06 | 243 | +73.01 | +0.300457 |
| 2021-07 | 272 | +64.28 | +0.236332 |
| 2021-08 | 319 | +44.24 | +0.138688 |
| 2021-09 | 316 | -49.42 | -0.156397 |
| 2021-10 | 467 | -35.11 | -0.075181 |
| 2021-11 | 390 | -125.35 | -0.321398 |
| 2021-12 | 405 | -25.26 | -0.062372 |
| 2022-01 | 355 | +259.97 | +0.732303 |
| 2022-02 | 363 | -79.57 | -0.219209 |
| 2022-03 | 442 | +257.36 | +0.582268 |
| 2022-04 | 459 | +29.19 | +0.063603 |
| 2022-05 | 417 | +129.85 | +0.311390 |
| 2022-06 | 379 | +192.25 | +0.507247 |
| 2022-07 | 415 | -170.97 | -0.411977 |
| 2022-08 | 367 | +11.97 | +0.032612 |
| 2022-09 | 341 | -179.89 | -0.527540 |
| 2022-10 | 363 | +20.04 | +0.055212 |
| 2022-11 | 484 | -85.62 | -0.176907 |
| 2022-12 | 450 | -14.61 | -0.032456 |
| 2023-01 | 517 | +625.69 | +1.210240 |
| 2023-02 | 434 | -137.23 | -0.316208 |
| 2023-03 | 441 | -45.11 | -0.102283 |
| 2023-04 | 383 | -98.17 | -0.256325 |
| 2023-05 | 423 | +49.03 | +0.115902 |
| 2023-06 | 431 | +210.40 | +0.488164 |
| 2023-07 | 381 | -153.71 | -0.403436 |
| 2023-08 | 475 | +149.32 | +0.314364 |
| 2023-09 | 466 | -177.09 | -0.380029 |
| 2023-10 | 586 | +357.12 | +0.609427 |
| 2023-11 | 684 | -337.74 | -0.493765 |
| 2023-12 | 633 | -42.63 | -0.067350 |
| 2024-01 | 577 | -295.41 | -0.511971 |
| 2024-02 | 639 | +529.54 | +0.828694 |
| 2024-03 | 661 | -259.77 | -0.393003 |
| 2024-04 | 702 | +17.54 | +0.024987 |
| 2024-05 | 746 | -249.47 | -0.334416 |
| 2024-06 | 715 | +169.10 | +0.236499 |
| 2024-07 | 747 | +392.56 | +0.525511 |
| 2024-08 | 821 | +205.07 | +0.249784 |
| 2024-09 | 891 | +215.24 | +0.241566 |
| 2024-10 | 947 | -383.22 | -0.404664 |
| 2024-11 | 994 | +828.52 | +0.833521 |
| 2024-12 | 852 | -141.41 | -0.165970 |
| 2025-01 | 1,156 | -262.63 | -0.227188 |
| 2025-02 | 923 | +62.93 | +0.068182 |
| 2025-03 | 983 | +286.16 | +0.291105 |
| 2025-04 | 885 | +318.28 | +0.359637 |
| 2025-05 | 1,130 | +48.10 | +0.042567 |
| 2025-06 | 1,114 | -471.55 | -0.423297 |
| 2025-07 | 1,210 | +632.20 | +0.522483 |
| 2025-08 | 1,212 | -787.19 | -0.649494 |
| 2025-09 | 1,160 | -131.56 | -0.113411 |
| 2025-10 | 1,378 | +434.74 | +0.315488 |
| 2025-11 | 1,144 | -220.33 | -0.192593 |
| 2025-12 | 1,379 | -118.56 | -0.085973 |
| 2026-01 | 1,569 | +1069.79 | +0.681828 |
| 2026-02 | 1,202 | -648.51 | -0.539523 |
| 2026-03 | 1,348 | -365.89 | -0.271434 |
| 2026-04 | 1,256 | -267.07 | -0.212635 |
| 2026-05 | 1,079 | +139.14 | +0.128957 |
| 2026-06 | 574 | +153.99 | +0.268271 |
| 2026-07 | 132 | -57.59 | -0.436264 |

## Sebaran R dan galat baku (ADR-013)

Sampai H-010 laporan hanya memuat rerata, sehingga tidak ada hipotesis yang dapat dinilai secara statistik: mustahil mengatakan apakah selisih terhadap ambang berarti sesuatu atau tidak.

**Galat baku di bawah adalah taksiran BAWAH.** Ia mengandaikan perdagangan saling bebas, dan andaian itu tidak benar: perdagangan dari puluhan simbol kripto pada jendela waktu yang bertumpang berkorelasi lewat gerakan pasar bersama. Galat sesungguhnya lebih besar, jadi keyakinan sesungguhnya lebih kecil. Angka ini sah dipakai untuk **menjatuhkan** klaim, dan tidak sah dipakai untuk **menegakkan** klaim.

- Simpangan baku per perdagangan: **2.18891R** (ddof=1, n = 44,614)
- Galat baku ekspektasi: **0.010363R**
- Selang 95% (pendekatan normal): **[0.016855, 0.057478]R**
- Kuartil R: min -11.4736 · Q1 -1.0330 · median -1.0149 · Q3 0.7218 · maks 178.3832
- Jarak ke ambang 0.05R: **-0.012833R** = **-1.24 galat baku**

## Sebelas gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0014 | 0.3 | 0 dari 437 simbol gagal |
| buy_and_hold | lulus | 0.7792 | 0.0 | median selisih 0.7792; unggul di 392/437 simbol |
| entri_acak | GAGAL | 0.2259 | 0.05 | 67 dari 300 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -11.4736 | -1.5 | kerugian terburuk -11.474R dari 44614 perdagangan |
| funding | lulus | 79056.7855 | 0.0 | total funding mutlak 79056.785505 atas 44614 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 437 simbol gagal |
| checksum | GAGAL | 24.0000 | 0.0 | hilang 12, asing 12, tidak cocok 0 |
| survivorship | lulus | 1.0000 | 0.5 | porsi delisted diuji 0.1465 vs universe 0.1465 |
| konsentrasi | lulus | 0.8987 | 0.6 | 235 untung / 202 rugi dari 437 simbol; drop-1 0.03340R (retensi 0.8987), drop-22 0.01153R, median simbol +0.02524R, porsi bruto teratas 0.0445 (VELVETUSDT), setara 113.3 simbol |
| funding_ekor | GAGAL | 0.0273 | 0.35 | porsi ekor maks 0.0273 (rerata 0.0027 atas 10 terburuk), funding maks 0.4064R, 330 dari 44614 trade di atas pengaman (0.00740); gagal: porsi_trade_di_atas_pengaman |

## Jackknife konsentrasi (ADR-010)

Buang penyumbang teratas satu per satu. Retensi adalah ekspektasi setelah pembuangan dibagi ekspektasi utuh. Ini menjawab pertanyaan yang sesungguhnya penting: apakah keunggulan tetap ada seandainya simbol paling untung tidak pernah ada.

| k | Dibuang | Simbol sisa | Trade | Total R | Ekspektasi R | Retensi |
|---|---|---|---|---|---|---|
| 0 | — | 437 | 44,614 | 1658.15 | 0.037167 | 1.0000 |
| 1 | VELVETUSDT | 436 | 44,598 | 1489.58 | 0.033400 | 0.8987 |
| 2 | DOGEUSDT | 435 | 44,362 | 1414.75 | 0.031891 | 0.8581 |
| 3 | ENJUSDT | 434 | 44,133 | 1345.57 | 0.030489 | 0.8203 |
| 4 | ADAUSDT | 433 | 43,897 | 1287.98 | 0.029341 | 0.7894 |
| 5 | BTCUSDT | 432 | 43,664 | 1232.48 | 0.028227 | 0.7595 |

## Ekor funding (ADR-011)

Gerbang funding lama menilai total mutlak dan memberi nilai yang praktis sama untuk dua keadaan yang ekornya berbeda 4,4 kali. Yang dinilai di sini adalah porsi funding terhadap kerugian pada sepuluh perdagangan terburuk, karena di situlah funding pernah menyumbang 46,7% kerugian sementara reratanya hanya 0,0004R.

- Porsi funding terbesar di ekor: **0.0273** (ambang 0,35)
- Rerata porsi di 10 terburuk: **0.0027**
- Funding terbesar satu perdagangan: **0.4064R** (ambang 0,50R)
- Perdagangan di atas pengaman 0,25R: **330** dari 44,614 (0.00740, ambang 0,005)

| # | R | Funding R | Porsi funding |
|---|---|---|---|
| 1 | -11.4736 | -0.0102 | 0.0000 |
| 2 | -9.8142 | -0.0000 | 0.0000 |
| 3 | -8.8098 | -0.0000 | 0.0000 |
| 4 | -8.3672 | 0.2281 | 0.0273 |
| 5 | -7.3796 | 0.0000 | 0.0000 |
| 6 | -6.2576 | -0.0000 | 0.0000 |
| 7 | -6.1494 | -0.0090 | 0.0000 |
| 8 | -5.6667 | -0.0000 | 0.0000 |
| 9 | -5.5778 | 0.0000 | 0.0000 |
| 10 | -4.7218 | -0.0029 | 0.0000 |

## Pembongkaran biaya

- Rerata biaya transaksi: **0.0178R**
- Rerata biaya funding: **-0.0008R**
- Rerata jarak stop terhadap harga: **6.743%**
- Perdagangan dengan biaya melebihi 1R: **0** dari 44,614

## Parameter yang terpilih di dalam sampel

| Parameter | Jumlah jendela |
|---|---|
| `{"imbalan_R": 2.0, "lookback": 20}` | 1987 |
| `{"imbalan_R": 2.0, "lookback": 55}` | 1069 |
| `{"imbalan_R": 2.0, "lookback": 100}` | 1026 |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| VELVETUSDT | 2,248 | 2 | 16 | 168.57 | 10.53572 |
| DOGEUSDT | 13,234 | 22 | 236 | 74.83 | 0.31707 |
| ENJUSDT | 12,749 | 21 | 229 | 69.18 | 0.3021 |
| ADAUSDT | 14,200 | 24 | 236 | 57.59 | 0.24403 |
| BTCUSDT | 14,388 | 24 | 233 | 55.49 | 0.23818 |
| SOLUSDT | 12,809 | 21 | 226 | 53.43 | 0.23641 |
| BNBUSDT | 14,140 | 24 | 270 | 52.91 | 0.19595 |
| 1000PEPEUSDT | 7,058 | 10 | 107 | 51.60 | 0.48225 |
| RUNEUSDT | 12,899 | 21 | 177 | 48.41 | 0.27349 |
| BLZUSDT | 9,350 | 15 | 169 | 48.02 | 0.28412 |
