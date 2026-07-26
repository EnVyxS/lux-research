# Backtest H-012 — h012_periode_tertahan

> Seluruh pemilihan sejak H-001b memakai riwayat penuh 40 simbol pertama, dan H-011 menghabiskan himpunan simbol tertahan, sehingga satu-satunya dimensi yang belum pernah dipakai memilih apa pun adalah waktu. H-012 menjalankan mekanisme H-010 tanpa satu perubahan pun di atas semesta yang definisinya diperbaiki lebih dulu — lantai median stop_frac 0,004 dan pengaman biaya masuk 0,5R — lalu dinilai HANYA pada perdagangan yang dibuka sejak 2026-01-01 UTC. Bila ekspektasi pada periode itu bertahan di atas 0,05R, keunggulan itu bukan sifat dari rentang waktu tertentu; bila ia jatuh, mekanisme ini tidak memiliki keunggulan yang bertahan dan wajib ditinggalkan. H-012 bukan rehabilitasi H-010, yang gagal dengan p 0,0631 pada 300 permutasi.

Sidik `75f9c7ccd65ec30f` · 12 kombinasi · 437 simbol · 1220.6s

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- p entri acak 0.0631 > 0.05

Gerbang gagal: entri_acak, invarian_risiko, funding_ekor

## Hasil luar sampel

- Perdagangan: **135,681**
- Total R: **8091.52**
- Ekspektasi: **0.05963634457229065**
- Jendela positif: 2246/4081
- Alasan keluar: {'stop': 101417, 'umur': 9699, 'target': 21658, 'akhir_data': 2479, 'carry': 428}
- Entri ditolak pengaman biaya (ADR-014): **62**, pengaman 0.5R

Penolakan pengaman biaya **bukan perdagangan** dan karena itu tidak muncul di histogram alasan keluar maupun di jumlah perdagangan di atas. Angka itu juga **tidak** mengukur seluruh keadaan degenerat: pada simbol yang seluruhnya degenerat, pengaman menolak entri juga saat pemilihan parameter, sehingga semua kandidat berskor -inf, seluruh jendelanya dilewati, dan simbol itu menyumbang nol penolakan sekaligus nol perdagangan. Yang tercatat di sini hanyalah simbol yang berubah degenerat di tengah jalan; simbol yang degenerat sepanjang riwayatnya hanya terlihat di lantai semesta di bawah.

| Simbol | Entri ditolak |
|---|---|
| PAXGUSDT | 42 |
| BTCDOMUSDT | 11 |
| MASKUSDT | 4 |
| BNBUSDT | 3 |
| BTCUSDT | 1 |
| TRXUSDT | 1 |

## Lantai satuan R pada semesta (ADR-014)

Lantai median `stop_frac` **0.004**, diturunkan dari aritmetika biaya dan bukan disetel: biaya bolak-balik 0,002 dari harga menjadi tepat 0,5R di lantai itu. Kriteria ini seragam dan dipra-registrasi, sehingga ia bukan penyubsetan simbol pasca-hasil.

- Simbol dinilai: **438**
- Layak: **437**
- Dibuang: **1**

| Simbol | median stop_frac | biaya masuk R | Sebab |
|---|---|---|---|
| USDCUSDT | 1.293930e-04 | 15.46 | median jarak stop 1.294e-04 di bawah lantai 0.004 |

## Hasil menurut bulan masuk (ADR-014)

Setiap perdagangan dimiliki oleh bulan kalender UTC tempat ia **dibuka**, karena keputusan yang diuji adalah keputusan masuk. Akibatnya ada rembesan yang wajib dinyatakan: perdagangan yang dibuka sesaat sebelum batas sebuah periode dapat ditutup sesudahnya, dan besarnya rembesan itu terbatas oleh `maks_umur_bar` (168 bar).

Tabel ini **bukan** putusan dan bukan pula izin memilih periode terbaik sesudah melihatnya. Memilih periode setelah hasil terlihat adalah penyubsetan yang sama terlarangnya dengan memilih simbol.

| Bulan masuk | Trade | Total R | Ekspektasi R |
|---|---|---|---|
| 2020-07 | 55 | +27.02 | +0.491250 |
| 2020-08 | 106 | -47.38 | -0.447027 |
| 2020-09 | 182 | +58.84 | +0.323282 |
| 2020-10 | 234 | -29.86 | -0.127604 |
| 2020-11 | 278 | -44.32 | -0.159424 |
| 2020-12 | 294 | -13.10 | -0.044555 |
| 2021-01 | 373 | -67.62 | -0.181279 |
| 2021-02 | 231 | +1.23 | +0.005318 |
| 2021-03 | 329 | -46.32 | -0.140803 |
| 2021-04 | 390 | -57.20 | -0.146661 |
| 2021-05 | 742 | +97.86 | +0.131886 |
| 2021-06 | 879 | +200.89 | +0.228547 |
| 2021-07 | 1,002 | +90.48 | +0.090297 |
| 2021-08 | 1,001 | -110.06 | -0.109948 |
| 2021-09 | 1,016 | +277.44 | +0.273075 |
| 2021-10 | 1,241 | -107.09 | -0.086290 |
| 2021-11 | 979 | -167.93 | -0.171536 |
| 2021-12 | 1,040 | +466.96 | +0.448997 |
| 2022-01 | 951 | +539.44 | +0.567239 |
| 2022-02 | 958 | +153.73 | +0.160467 |
| 2022-03 | 1,191 | +112.33 | +0.094313 |
| 2022-04 | 1,088 | +324.23 | +0.298007 |
| 2022-05 | 1,283 | +83.67 | +0.065212 |
| 2022-06 | 1,128 | +367.98 | +0.326221 |
| 2022-07 | 1,082 | +116.71 | +0.107864 |
| 2022-08 | 1,094 | -31.66 | -0.028944 |
| 2022-09 | 1,239 | -669.08 | -0.540012 |
| 2022-10 | 1,345 | -85.05 | -0.063236 |
| 2022-11 | 1,395 | +27.02 | +0.019373 |
| 2022-12 | 1,403 | +126.75 | +0.090345 |
| 2023-01 | 1,853 | +377.90 | +0.203937 |
| 2023-02 | 1,451 | -15.24 | -0.010505 |
| 2023-03 | 1,682 | +78.84 | +0.046871 |
| 2023-04 | 1,481 | -430.93 | -0.290971 |
| 2023-05 | 1,596 | -169.15 | -0.105984 |
| 2023-06 | 1,770 | +752.68 | +0.425245 |
| 2023-07 | 1,562 | -475.65 | -0.304511 |
| 2023-08 | 1,961 | +159.37 | +0.081272 |
| 2023-09 | 1,627 | -500.68 | -0.307732 |
| 2023-10 | 1,821 | +262.20 | +0.143987 |
| 2023-11 | 1,967 | -873.29 | -0.443970 |
| 2023-12 | 2,061 | -389.57 | -0.189021 |
| 2024-01 | 1,773 | +17.71 | +0.009991 |
| 2024-02 | 2,322 | +40.90 | +0.017614 |
| 2024-03 | 2,054 | -230.08 | -0.112014 |
| 2024-04 | 2,352 | +1178.99 | +0.501271 |
| 2024-05 | 2,290 | -558.24 | -0.243771 |
| 2024-06 | 2,393 | +498.18 | +0.208181 |
| 2024-07 | 2,786 | +1276.55 | +0.458203 |
| 2024-08 | 2,306 | +1048.36 | +0.454622 |
| 2024-09 | 2,453 | -147.09 | -0.059963 |
| 2024-10 | 2,268 | -599.06 | -0.264136 |
| 2024-11 | 2,548 | +1356.34 | +0.532314 |
| 2024-12 | 2,550 | +0.67 | +0.000263 |
| 2025-01 | 2,601 | +66.75 | +0.025662 |
| 2025-02 | 2,821 | +247.69 | +0.087803 |
| 2025-03 | 2,778 | +709.73 | +0.255481 |
| 2025-04 | 3,019 | +526.71 | +0.174466 |
| 2025-05 | 3,116 | +969.65 | +0.311185 |
| 2025-06 | 2,675 | -393.03 | -0.146927 |
| 2025-07 | 3,535 | +1111.95 | +0.314556 |
| 2025-08 | 3,463 | -1172.22 | -0.338500 |
| 2025-09 | 3,613 | +103.96 | +0.028773 |
| 2025-10 | 4,439 | +1757.44 | +0.395909 |
| 2025-11 | 3,617 | -66.96 | -0.018512 |
| 2025-12 | 4,431 | -948.34 | -0.214023 |
| 2026-01 | 4,577 | +2347.27 | +0.512839 |
| 2026-02 | 3,791 | -854.68 | -0.225451 |
| 2026-03 | 3,896 | -241.25 | -0.061922 |
| 2026-04 | 4,304 | -584.64 | -0.135835 |
| 2026-05 | 3,317 | +197.26 | +0.059468 |
| 2026-06 | 1,723 | +168.49 | +0.097787 |
| 2026-07 | 509 | -109.88 | -0.215876 |

## Sebaran R dan galat baku (ADR-013)

Sampai H-010 laporan hanya memuat rerata, sehingga tidak ada hipotesis yang dapat dinilai secara statistik: mustahil mengatakan apakah selisih terhadap ambang berarti sesuatu atau tidak.

**Galat baku di bawah adalah taksiran BAWAH.** Ia mengandaikan perdagangan saling bebas, dan andaian itu tidak benar: perdagangan dari puluhan simbol kripto pada jendela waktu yang bertumpang berkorelasi lewat gerakan pasar bersama. Galat sesungguhnya lebih besar, jadi keyakinan sesungguhnya lebih kecil. Angka ini sah dipakai untuk **menjatuhkan** klaim, dan tidak sah dipakai untuk **menegakkan** klaim.

- Simpangan baku per perdagangan: **2.22746R** (ddof=1, n = 135,681)
- Galat baku ekspektasi: **0.006047R**
- Selang 95% (pendekatan normal): **[0.047784, 0.071489]R**
- Kuartil R: min -21.3131 · Q1 -1.0632 · median -1.0401 · Q3 -0.4209 · maks 12.9076
- Jarak ke ambang 0.05R: **+0.009636R** = **+1.59 galat baku**

## Sebelas gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0013 | 0.3 | 0 dari 437 simbol gagal |
| buy_and_hold | lulus | 0.8401 | 0.0 | median selisih 0.8401; unggul di 394/437 simbol |
| entri_acak | GAGAL | 0.0631 | 0.05 | 18 dari 300 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -21.3131 | -1.5 | kerugian terburuk -21.313R dari 135681 perdagangan |
| funding | lulus | 153788.1322 | 0.0 | total funding mutlak 153788.132234 atas 135681 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 437 simbol gagal |
| checksum | lulus | 0.0000 | 0.0 | hilang 0, asing 0, tidak cocok 0 |
| survivorship | lulus | 1.0000 | 0.5 | porsi delisted diuji 0.1465 vs universe 0.1465 |
| konsentrasi | lulus | 0.9849 | 0.6 | 306 untung / 131 rugi dari 437 simbol; drop-1 0.05873R (retensi 0.9849), drop-22 0.04497R, median simbol +0.06285R, porsi bruto teratas 0.0142 (FLMUSDT), setara 174.3 simbol |
| funding_ekor | GAGAL | 0.1693 | 0.35 | porsi ekor maks 0.1693 (rerata 0.0988 atas 10 terburuk), funding maks 0.6601R, 430 dari 135681 trade di atas pengaman (0.00317); gagal: funding_maks_R |

## Jackknife konsentrasi (ADR-010)

Buang penyumbang teratas satu per satu. Retensi adalah ekspektasi setelah pembuangan dibagi ekspektasi utuh. Ini menjawab pertanyaan yang sesungguhnya penting: apakah keunggulan tetap ada seandainya simbol paling untung tidak pernah ada.

| k | Dibuang | Simbol sisa | Trade | Total R | Ekspektasi R | Retensi |
|---|---|---|---|---|---|---|
| 0 | — | 437 | 135,681 | 8091.52 | 0.059636 | 1.0000 |
| 1 | FLMUSDT | 436 | 135,088 | 7934.17 | 0.058733 | 0.9849 |
| 2 | ONEUSDT | 435 | 134,406 | 7792.57 | 0.057978 | 0.9722 |
| 3 | TRXUSDT | 434 | 133,685 | 7651.96 | 0.057239 | 0.9598 |
| 4 | GALAUSDT | 433 | 133,274 | 7517.24 | 0.056404 | 0.9458 |
| 5 | CAKEUSDT | 432 | 133,022 | 7384.27 | 0.055512 | 0.9308 |

## Ekor funding (ADR-011)

Gerbang funding lama menilai total mutlak dan memberi nilai yang praktis sama untuk dua keadaan yang ekornya berbeda 4,4 kali. Yang dinilai di sini adalah porsi funding terhadap kerugian pada sepuluh perdagangan terburuk, karena di situlah funding pernah menyumbang 46,7% kerugian sementara reratanya hanya 0,0004R.

- Porsi funding terbesar di ekor: **0.1693** (ambang 0,35)
- Rerata porsi di 10 terburuk: **0.0988**
- Funding terbesar satu perdagangan: **0.6601R** (ambang 0,50R)
- Perdagangan di atas pengaman 0,25R: **430** dari 135,681 (0.00317, ambang 0,005)

| # | R | Funding R | Porsi funding |
|---|---|---|---|
| 1 | -21.3131 | 0.4825 | 0.0226 |
| 2 | -1.4966 | 0.1779 | 0.1189 |
| 3 | -1.4246 | 0.1280 | 0.0898 |
| 4 | -1.4176 | 0.1547 | 0.1092 |
| 5 | -1.4159 | 0.1774 | 0.1253 |
| 6 | -1.4103 | 0.2387 | 0.1693 |
| 7 | -1.4068 | 0.1813 | 0.1288 |
| 8 | -1.4061 | 0.1466 | 0.1042 |
| 9 | -1.3870 | 0.1206 | 0.0869 |
| 10 | -1.3865 | 0.0456 | 0.0329 |

## Pembongkaran biaya

- Rerata biaya transaksi: **0.0359R**
- Rerata biaya funding: **-0.0010R**
- Rerata jarak stop terhadap harga: **3.507%**
- Perdagangan dengan biaya melebihi 1R: **0** dari 135,681

## Parameter yang terpilih di dalam sampel

| Parameter | Jumlah jendela |
|---|---|
| `{"imbalan_R": 8.0, "lookback": 100}` | 655 |
| `{"imbalan_R": 8.0, "lookback": 20}` | 574 |
| `{"imbalan_R": 8.0, "lookback": 55}` | 496 |
| `{"imbalan_R": 6.0, "lookback": 20}` | 434 |
| `{"imbalan_R": 6.0, "lookback": 100}` | 408 |
| `{"imbalan_R": 4.0, "lookback": 20}` | 347 |
| `{"imbalan_R": 6.0, "lookback": 55}` | 325 |
| `{"imbalan_R": 2.0, "lookback": 20}` | 252 |
| `{"imbalan_R": 4.0, "lookback": 100}` | 221 |
| `{"imbalan_R": 4.0, "lookback": 55}` | 180 |
| `{"imbalan_R": 2.0, "lookback": 55}` | 97 |
| `{"imbalan_R": 2.0, "lookback": 100}` | 92 |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| FLMUSDT | 44,978 | 18 | 593 | 157.35 | 0.26535 |
| ONEUSDT | 46,793 | 19 | 682 | 141.60 | 0.20763 |
| TRXUSDT | 57,064 | 24 | 721 | 140.61 | 0.19502 |
| GALAUSDT | 42,501 | 17 | 411 | 134.72 | 0.32778 |
| CAKEUSDT | 23,892 | 8 | 252 | 132.97 | 0.52767 |
| FXSUSDT | 25,974 | 9 | 356 | 130.50 | 0.36656 |
| LINAUSDT | 35,139 | 14 | 460 | 128.75 | 0.27989 |
| ADAUSDT | 56,800 | 24 | 699 | 120.25 | 0.17203 |
| FTMUSDT | 37,443 | 15 | 373 | 119.83 | 0.32127 |
| BTCUSDT | 57,552 | 24 | 690 | 116.49 | 0.16883 |
