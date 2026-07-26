# Backtest H-011 — h011_semesta_penuh

> H-010 lulus dengan ekspektasi 0,053028R, tetapi seluruh hasil sejak H-001b diukur pada 40 simbol pertama secara alfabet, yaitu kurang dari sepersepuluh semesta layak. H-011 menjalankan mekanisme H-010 tanpa satu perubahan pun atas seluruh 438 simbol dan dinilai pada 398 simbol yang belum pernah disentuh. Bila ekspektasi tertahan bertahan di atas 0,05R, keunggulan itu bukan sifat dari 40 simbol tertentu; bila ia jatuh, hasil H-010 adalah derau seleksi dan bukan temuan.

Sidik `8a6efde6d333d8b5` · 12 kombinasi · 438 simbol · 838.1s

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- ekspektasi -0.0791R < 0.05R
- p entri acak 0.0631 > 0.05

Gerbang gagal: entri_acak, invarian_risiko, konsentrasi, funding_ekor

## Hasil luar sampel

- Perdagangan: **136,337**
- Total R: **-10781.32**
- Ekspektasi: **-0.07907848558786414**
- Jendela positif: 2246/4092
- Alasan keluar: {'stop': 102068, 'umur': 9699, 'target': 21649, 'akhir_data': 2479, 'carry': 442}

## Sebaran R dan galat baku (ADR-013)

Sampai H-010 laporan hanya memuat rerata, sehingga tidak ada hipotesis yang dapat dinilai secara statistik: mustahil mengatakan apakah selisih terhadap ambang berarti sesuatu atau tidak.

**Galat baku di bawah adalah taksiran BAWAH.** Ia mengandaikan perdagangan saling bebas, dan andaian itu tidak benar: perdagangan dari puluhan simbol kripto pada jendela waktu yang bertumpang berkorelasi lewat gerakan pasar bersama. Galat sesungguhnya lebih besar, jadi keyakinan sesungguhnya lebih kecil. Angka ini sah dipakai untuk **menjatuhkan** klaim, dan tidak sah dipakai untuk **menegakkan** klaim.

- Simpangan baku per perdagangan: **4.24670R** (ddof=1, n = 136,337)
- Galat baku ekspektasi: **0.011501R**
- Selang 95% (pendekatan normal): **[-0.101621, -0.056536]R**
- Kuartil R: min -470.0612 · Q1 -1.0635 · median -1.0402 · Q3 -0.4224 · maks 12.9076
- Jarak ke ambang 0.05R: **-0.129078R** = **-11.22 galat baku**

## Sebelas gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0013 | 0.3 | 0 dari 438 simbol gagal |
| buy_and_hold | lulus | 0.8387 | 0.0 | median selisih 0.8387; unggul di 394/438 simbol |
| entri_acak | GAGAL | 0.0631 | 0.05 | 18 dari 300 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -470.0612 | -1.5 | kerugian terburuk -470.061R dari 136337 perdagangan |
| funding | lulus | 154526.9859 | 0.0 | total funding mutlak 154526.985930 atas 136337 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 438 simbol gagal |
| checksum | lulus | 0.0000 | 0.0 | hilang 0, asing 0, tidak cocok 0 |
| survivorship | lulus | 1.0000 | 0.5 | porsi delisted diuji 0.1461 vs universe 0.1461 |
| konsentrasi | GAGAL | — | — | tidak dapat dinilai: ekspektasi gabungan -0.07907848558786414 tidak positif sehingga retensi tidak bermakna |
| funding_ekor | GAGAL | 0.0102 | 0.35 | porsi ekor maks 0.0102 (rerata 0.0010 atas 10 terburuk), funding maks 2.3900R, 440 dari 136337 trade di atas pengaman (0.00323); gagal: funding_maks_R |

## Jackknife konsentrasi (ADR-010)

Buang penyumbang teratas satu per satu. Retensi adalah ekspektasi setelah pembuangan dibagi ekspektasi utuh. Ini menjawab pertanyaan yang sesungguhnya penting: apakah keunggulan tetap ada seandainya simbol paling untung tidak pernah ada.

| k | Dibuang | Simbol sisa | Trade | Total R | Ekspektasi R | Retensi |
|---|---|---|---|---|---|---|
| 0 | — | 438 | 136,337 | -10781.32 | -0.079078 | — |
| 1 | FLMUSDT | 437 | 135,744 | -10938.67 | -0.080583 | — |
| 2 | ONEUSDT | 436 | 135,062 | -11080.27 | -0.082038 | — |
| 3 | TRXUSDT | 435 | 134,340 | -11219.91 | -0.083519 | — |
| 4 | GALAUSDT | 434 | 133,929 | -11354.63 | -0.084781 | — |
| 5 | CAKEUSDT | 433 | 133,677 | -11487.60 | -0.085936 | — |

## Ekor funding (ADR-011)

Gerbang funding lama menilai total mutlak dan memberi nilai yang praktis sama untuk dua keadaan yang ekornya berbeda 4,4 kali. Yang dinilai di sini adalah porsi funding terhadap kerugian pada sepuluh perdagangan terburuk, karena di situlah funding pernah menyumbang 46,7% kerugian sementara reratanya hanya 0,0004R.

- Porsi funding terbesar di ekor: **0.0102** (ambang 0,35)
- Rerata porsi di 10 terburuk: **0.0010**
- Funding terbesar satu perdagangan: **2.3900R** (ambang 0,50R)
- Perdagangan di atas pengaman 0,25R: **440** dari 136,337 (0.00323, ambang 0,005)

| # | R | Funding R | Porsi funding |
|---|---|---|---|
| 1 | -470.0612 | -0.0000 | 0.0000 |
| 2 | -233.6455 | 2.3900 | 0.0102 |
| 3 | -219.7828 | -0.0000 | 0.0000 |
| 4 | -213.3181 | -0.0000 | 0.0000 |
| 5 | -188.5200 | -0.0000 | 0.0000 |
| 6 | -186.8235 | 0.0000 | 0.0000 |
| 7 | -181.2225 | -0.0000 | 0.0000 |
| 8 | -174.7619 | -0.0000 | 0.0000 |
| 9 | -170.2822 | -0.0000 | 0.0000 |
| 10 | -167.3001 | 0.0000 | 0.0000 |

## Pembongkaran biaya

- Rerata biaya transaksi: **0.1255R**
- Rerata biaya funding: **-0.0016R**
- Rerata jarak stop terhadap harga: **3.490%**
- Perdagangan dengan biaya melebihi 1R: **478** dari 136,337

## Parameter yang terpilih di dalam sampel

| Parameter | Jumlah jendela |
|---|---|
| `{"imbalan_R": 8.0, "lookback": 100}` | 656 |
| `{"imbalan_R": 8.0, "lookback": 20}` | 575 |
| `{"imbalan_R": 8.0, "lookback": 55}` | 498 |
| `{"imbalan_R": 6.0, "lookback": 20}` | 434 |
| `{"imbalan_R": 6.0, "lookback": 100}` | 408 |
| `{"imbalan_R": 4.0, "lookback": 20}` | 347 |
| `{"imbalan_R": 6.0, "lookback": 55}` | 323 |
| `{"imbalan_R": 2.0, "lookback": 20}` | 254 |
| `{"imbalan_R": 4.0, "lookback": 100}` | 221 |
| `{"imbalan_R": 4.0, "lookback": 55}` | 180 |
| `{"imbalan_R": 2.0, "lookback": 55}` | 99 |
| `{"imbalan_R": 2.0, "lookback": 100}` | 97 |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| FLMUSDT | 44,978 | 18 | 593 | 157.35 | 0.26535 |
| ONEUSDT | 46,793 | 19 | 682 | 141.60 | 0.20763 |
| TRXUSDT | 57,064 | 24 | 722 | 139.64 | 0.1934 |
| GALAUSDT | 42,501 | 17 | 411 | 134.72 | 0.32778 |
| CAKEUSDT | 23,892 | 8 | 252 | 132.97 | 0.52767 |
| FXSUSDT | 25,974 | 9 | 356 | 130.50 | 0.36656 |
| LINAUSDT | 35,139 | 14 | 460 | 128.75 | 0.27989 |
| ADAUSDT | 56,800 | 24 | 699 | 120.25 | 0.17203 |
| FTMUSDT | 37,443 | 15 | 373 | 119.83 | 0.32127 |
| BTCUSDT | 57,552 | 24 | 690 | 116.49 | 0.16883 |
