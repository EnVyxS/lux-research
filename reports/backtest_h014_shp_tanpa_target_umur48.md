# Backtest H-014-SHp — h014_shp_tanpa_target_umur48

> Sel SH' — breakout Donchian dengan stop ATR TANPA target, batas umur 48 bar 4h, yakni umur yang SAMA dengan sel SS'. Selisih keduanya karena itu mengukur ada-tidaknya target dan bukan panjang pegangan.

Sidik `5721a88e59ebe90f` · 3 kombinasi · 437 simbol · 52.6s

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- ekspektasi 0.0396R < 0.05R
- p entri acak 0.2193 > 0.05
- jendela positif 0.49 < 0.5

Gerbang gagal: entri_acak, invarian_risiko, checksum, funding_ekor

## Hasil luar sampel

- Perdagangan: **44,538**
- Total R: **1763.60**
- Ekspektasi: **0.03959765698185091**
- Jendela positif: 1982/4082
- Alasan keluar: {'umur': 14426, 'stop': 28013, 'akhir_data': 2099}
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
| 2020-07 | 24 | +40.13 | +1.672251 |
| 2020-08 | 77 | -48.18 | -0.625755 |
| 2020-09 | 88 | +14.73 | +0.167408 |
| 2020-10 | 112 | -36.73 | -0.327920 |
| 2020-11 | 108 | +2.10 | +0.019428 |
| 2020-12 | 90 | -3.96 | -0.044051 |
| 2021-01 | 142 | +5.40 | +0.038040 |
| 2021-02 | 118 | +139.33 | +1.180742 |
| 2021-03 | 157 | -14.49 | -0.092294 |
| 2021-04 | 174 | +47.34 | +0.272087 |
| 2021-05 | 235 | +28.75 | +0.122358 |
| 2021-06 | 228 | +74.51 | +0.326795 |
| 2021-07 | 284 | +49.69 | +0.174960 |
| 2021-08 | 320 | +45.57 | +0.142416 |
| 2021-09 | 312 | -48.69 | -0.156063 |
| 2021-10 | 465 | -42.51 | -0.091414 |
| 2021-11 | 378 | -117.97 | -0.312083 |
| 2021-12 | 403 | -28.39 | -0.070450 |
| 2022-01 | 354 | +261.56 | +0.738870 |
| 2022-02 | 363 | -79.57 | -0.219209 |
| 2022-03 | 442 | +257.36 | +0.582268 |
| 2022-04 | 459 | +29.19 | +0.063603 |
| 2022-05 | 417 | +129.67 | +0.310950 |
| 2022-06 | 377 | +194.34 | +0.515489 |
| 2022-07 | 415 | -170.97 | -0.411977 |
| 2022-08 | 366 | +11.57 | +0.031609 |
| 2022-09 | 340 | -179.29 | -0.527337 |
| 2022-10 | 364 | +17.02 | +0.046766 |
| 2022-11 | 483 | -91.38 | -0.189188 |
| 2022-12 | 451 | -26.93 | -0.059715 |
| 2023-01 | 516 | +633.43 | +1.227568 |
| 2023-02 | 436 | -139.28 | -0.319439 |
| 2023-03 | 443 | -44.54 | -0.100536 |
| 2023-04 | 390 | -90.04 | -0.230880 |
| 2023-05 | 426 | +58.58 | +0.137513 |
| 2023-06 | 434 | +210.99 | +0.486147 |
| 2023-07 | 383 | -147.38 | -0.384817 |
| 2023-08 | 478 | +148.35 | +0.310347 |
| 2023-09 | 466 | -170.22 | -0.365287 |
| 2023-10 | 587 | +356.12 | +0.606684 |
| 2023-11 | 684 | -337.74 | -0.493765 |
| 2023-12 | 633 | -44.43 | -0.070183 |
| 2024-01 | 577 | -295.41 | -0.511971 |
| 2024-02 | 636 | +551.36 | +0.866917 |
| 2024-03 | 648 | -244.46 | -0.377247 |
| 2024-04 | 702 | +18.62 | +0.026530 |
| 2024-05 | 740 | -250.46 | -0.338457 |
| 2024-06 | 716 | +174.65 | +0.243926 |
| 2024-07 | 750 | +400.95 | +0.534597 |
| 2024-08 | 826 | +219.17 | +0.265342 |
| 2024-09 | 892 | +210.71 | +0.236219 |
| 2024-10 | 947 | -382.96 | -0.404394 |
| 2024-11 | 994 | +825.89 | +0.830877 |
| 2024-12 | 851 | -145.65 | -0.171150 |
| 2025-01 | 1,154 | -261.56 | -0.226656 |
| 2025-02 | 921 | +68.20 | +0.074052 |
| 2025-03 | 981 | +288.99 | +0.294588 |
| 2025-04 | 887 | +312.71 | +0.352545 |
| 2025-05 | 1,134 | +46.76 | +0.041235 |
| 2025-06 | 1,115 | -476.48 | -0.427337 |
| 2025-07 | 1,211 | +630.85 | +0.520932 |
| 2025-08 | 1,209 | -786.25 | -0.650329 |
| 2025-09 | 1,159 | -124.01 | -0.106995 |
| 2025-10 | 1,377 | +423.17 | +0.307310 |
| 2025-11 | 1,142 | -217.51 | -0.190464 |
| 2025-12 | 1,373 | -123.50 | -0.089948 |
| 2026-01 | 1,571 | +1072.38 | +0.682611 |
| 2026-02 | 1,194 | -643.35 | -0.538818 |
| 2026-03 | 1,354 | -364.78 | -0.269411 |
| 2026-04 | 1,265 | -279.91 | -0.221272 |
| 2026-05 | 1,082 | +128.12 | +0.118409 |
| 2026-06 | 573 | +154.32 | +0.269320 |
| 2026-07 | 135 | -60.01 | -0.444532 |

## Sebaran R dan galat baku (ADR-013)

Sampai H-010 laporan hanya memuat rerata, sehingga tidak ada hipotesis yang dapat dinilai secara statistik: mustahil mengatakan apakah selisih terhadap ambang berarti sesuatu atau tidak.

**Galat baku di bawah adalah taksiran BAWAH.** Ia mengandaikan perdagangan saling bebas, dan andaian itu tidak benar: perdagangan dari puluhan simbol kripto pada jendela waktu yang bertumpang berkorelasi lewat gerakan pasar bersama. Galat sesungguhnya lebih besar, jadi keyakinan sesungguhnya lebih kecil. Angka ini sah dipakai untuk **menjatuhkan** klaim, dan tidak sah dipakai untuk **menegakkan** klaim.

- Simpangan baku per perdagangan: **2.20818R** (ddof=1, n = 44,538)
- Galat baku ekspektasi: **0.010463R**
- Selang 95% (pendekatan normal): **[0.019090, 0.060105]R**
- Kuartil R: min -11.4736 · Q1 -1.0331 · median -1.0150 · Q3 0.7193 · maks 178.3832
- Jarak ke ambang 0.05R: **-0.010402R** = **-0.99 galat baku**

## Sebelas gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0014 | 0.3 | 0 dari 437 simbol gagal |
| buy_and_hold | lulus | 0.7832 | 0.0 | median selisih 0.7832; unggul di 393/437 simbol |
| entri_acak | GAGAL | 0.2193 | 0.05 | 65 dari 300 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -11.4736 | -1.5 | kerugian terburuk -11.474R dari 44538 perdagangan |
| funding | lulus | 80830.2897 | 0.0 | total funding mutlak 80830.289748 atas 44538 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 437 simbol gagal |
| checksum | GAGAL | — | — | tidak dapat dinilai: manifest baru ditulis pada run ini |
| survivorship | lulus | 1.0000 | 0.5 | porsi delisted diuji 0.1465 vs universe 0.1465 |
| konsentrasi | lulus | 0.9047 | 0.6 | 234 untung / 203 rugi dari 437 simbol; drop-1 0.03583R (retensi 0.9047), drop-22 0.01225R, median simbol +0.02710R, porsi bruto teratas 0.0431 (VELVETUSDT), setara 111.6 simbol |
| funding_ekor | GAGAL | 0.0273 | 0.35 | porsi ekor maks 0.0273 (rerata 0.0027 atas 10 terburuk), funding maks 2.9000R, 307 dari 44538 trade di atas pengaman (0.00689); gagal: funding_maks_R, porsi_trade_di_atas_pengaman |

## Jackknife konsentrasi (ADR-010)

Buang penyumbang teratas satu per satu. Retensi adalah ekspektasi setelah pembuangan dibagi ekspektasi utuh. Ini menjawab pertanyaan yang sesungguhnya penting: apakah keunggulan tetap ada seandainya simbol paling untung tidak pernah ada.

| k | Dibuang | Simbol sisa | Trade | Total R | Ekspektasi R | Retensi |
|---|---|---|---|---|---|---|
| 0 | — | 437 | 44,538 | 1763.60 | 0.039598 | 1.0000 |
| 1 | VELVETUSDT | 436 | 44,522 | 1595.03 | 0.035826 | 0.9047 |
| 2 | DOGEUSDT | 435 | 44,294 | 1510.07 | 0.034092 | 0.8610 |
| 3 | BTCUSDT | 434 | 44,057 | 1440.01 | 0.032685 | 0.8254 |
| 4 | ENJUSDT | 433 | 43,828 | 1370.58 | 0.031272 | 0.7897 |
| 5 | SOLUSDT | 432 | 43,600 | 1307.15 | 0.029981 | 0.7571 |

## Ekor funding (ADR-011)

Gerbang funding lama menilai total mutlak dan memberi nilai yang praktis sama untuk dua keadaan yang ekornya berbeda 4,4 kali. Yang dinilai di sini adalah porsi funding terhadap kerugian pada sepuluh perdagangan terburuk, karena di situlah funding pernah menyumbang 46,7% kerugian sementara reratanya hanya 0,0004R.

- Porsi funding terbesar di ekor: **0.0273** (ambang 0,35)
- Rerata porsi di 10 terburuk: **0.0027**
- Funding terbesar satu perdagangan: **2.9000R** (ambang 0,50R)
- Perdagangan di atas pengaman 0,25R: **307** dari 44,538 (0.00689, ambang 0,005)

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
- Rerata biaya funding: **-0.0001R**
- Rerata jarak stop terhadap harga: **6.725%**
- Perdagangan dengan biaya melebihi 1R: **5** dari 44,538

## Parameter yang terpilih di dalam sampel

| Parameter | Jumlah jendela |
|---|---|
| `{"imbalan_R": 2.0, "lookback": 20}` | 1995 |
| `{"imbalan_R": 2.0, "lookback": 55}` | 1073 |
| `{"imbalan_R": 2.0, "lookback": 100}` | 1014 |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| VELVETUSDT | 2,248 | 2 | 16 | 168.57 | 10.53572 |
| DOGEUSDT | 13,234 | 22 | 228 | 84.96 | 0.37265 |
| BTCUSDT | 14,388 | 24 | 237 | 70.05 | 0.29557 |
| ENJUSDT | 12,749 | 21 | 229 | 69.43 | 0.3032 |
| SOLUSDT | 12,809 | 21 | 228 | 63.43 | 0.27819 |
| 1000PEPEUSDT | 7,058 | 10 | 103 | 59.75 | 0.58014 |
| ZILUSDT | 13,336 | 22 | 250 | 51.70 | 0.2068 |
| BNBUSDT | 14,140 | 24 | 270 | 51.36 | 0.19022 |
| ETCUSDT | 14,290 | 24 | 244 | 50.74 | 0.20797 |
| ADAUSDT | 14,200 | 24 | 245 | 49.77 | 0.20314 |
