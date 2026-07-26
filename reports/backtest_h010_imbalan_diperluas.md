# Backtest H-010 — h010_imbalan_diperluas

> Pada H-007, H-008, dan H-009 pemilih walk-forward menempel di batas atas grid imbalan, 194 dari 356 jendela di H-009. Selama dinding itu tidak digeser, dua tafsiran tidak dapat dipisahkan: optimum berada di 4R, atau optimum berada di luar grid dan yang terukur hanyalah dindingnya. H-010 menggeser dinding menjadi [2, 4, 6, 8] dengan jumlah kombinasi identik dan seluruh unsur lain tidak diubah. Bila laju kena target turun lebih lambat daripada titik impas 1/(1+imbalan), ekspektasi naik; bila lebih cepat, ia turun dan dinding H-007 terbukti bukan artefak.

Sidik `14b2f3bfa8a754b5` · 12 kombinasi · 40 simbol · 117.5s

## Putusan

**LULUS**

## Hasil luar sampel

- Perdagangan: **11,734**
- Total R: **622.23**
- Ekspektasi: **0.05302836360569971**
- Jendela positif: 188/356
- Alasan keluar: {'stop': 8776, 'umur': 879, 'target': 1839, 'akhir_data': 214, 'carry': 26}

## Sebelas gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0003 | 0.3 | 0 dari 40 simbol gagal |
| buy_and_hold | lulus | 0.7986 | 0.0 | median selisih 0.7986; unggul di 36/40 simbol |
| entri_acak | lulus | 0.0495 | 0.05 | 4 dari 100 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | lulus | -1.2733 | -1.5 | kerugian terburuk -1.273R dari 11734 perdagangan |
| funding | lulus | 11523.3110 | 0.0 | total funding mutlak 11523.311034 atas 11734 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 40 simbol gagal |
| checksum | lulus | 0.0000 | 0.0 | hilang 0, asing 0, tidak cocok 0 |
| survivorship | lulus | 0.8555 | 0.5 | porsi delisted diuji 0.1250 vs universe 0.1461 |
| konsentrasi | lulus | 0.8578 | 0.6 | 26 untung / 14 rugi dari 40 simbol; drop-1 0.04549R (retensi 0.8578), drop-2 0.03924R, median simbol +0.04604R, porsi bruto teratas 0.1346 (ADAUSDT), setara 14.9 simbol |
| funding_ekor | lulus | 0.1675 | 0.35 | porsi ekor maks 0.1675 (rerata 0.1487 atas 10 terburuk), funding maks 0.4144R, 26 dari 11734 trade di atas pengaman (0.00222) |

## Jackknife konsentrasi (ADR-010)

Buang penyumbang teratas satu per satu. Retensi adalah ekspektasi setelah pembuangan dibagi ekspektasi utuh. Ini menjawab pertanyaan yang sesungguhnya penting: apakah keunggulan tetap ada seandainya simbol paling untung tidak pernah ada.

| k | Dibuang | Simbol sisa | Trade | Total R | Ekspektasi R | Retensi |
|---|---|---|---|---|---|---|
| 0 | — | 40 | 11,734 | 622.23 | 0.053028 | 1.0000 |
| 1 | ADAUSDT | 39 | 11,035 | 501.98 | 0.045490 | 0.8578 |
| 2 | AAVEUSDT | 38 | 10,360 | 406.53 | 0.039240 | 0.7400 |
| 3 | ALGOUSDT | 37 | 9,623 | 337.80 | 0.035104 | 0.6620 |
| 4 | 1000BONKUSDT | 36 | 9,432 | 271.67 | 0.028803 | 0.5432 |
| 5 | AIUSDT | 35 | 9,283 | 208.40 | 0.022450 | 0.4234 |

## Ekor funding (ADR-011)

Gerbang funding lama menilai total mutlak dan memberi nilai yang praktis sama untuk dua keadaan yang ekornya berbeda 4,4 kali. Yang dinilai di sini adalah porsi funding terhadap kerugian pada sepuluh perdagangan terburuk, karena di situlah funding pernah menyumbang 46,7% kerugian sementara reratanya hanya 0,0004R.

- Porsi funding terbesar di ekor: **0.1675** (ambang 0,35)
- Rerata porsi di 10 terburuk: **0.1487**
- Funding terbesar satu perdagangan: **0.4144R** (ambang 0,50R)
- Perdagangan di atas pengaman 0,25R: **26** dari 11,734 (0.00222, ambang 0,005)

| # | R | Funding R | Porsi funding |
|---|---|---|---|
| 1 | -1.2733 | 0.1988 | 0.1561 |
| 2 | -1.2698 | 0.2098 | 0.1652 |
| 3 | -1.2588 | 0.1763 | 0.1401 |
| 4 | -1.2529 | 0.2052 | 0.1638 |
| 5 | -1.2528 | 0.1453 | 0.1160 |
| 6 | -1.2436 | 0.2083 | 0.1675 |
| 7 | -1.2362 | 0.1789 | 0.1447 |
| 8 | -1.2360 | 0.1409 | 0.1140 |
| 9 | -1.2353 | 0.1932 | 0.1564 |
| 10 | -1.2311 | 0.2014 | 0.1636 |

## Pembongkaran biaya

- Rerata biaya transaksi: **0.0353R**
- Rerata biaya funding: **0.0009R**
- Rerata jarak stop terhadap harga: **3.501%**
- Perdagangan dengan biaya melebihi 1R: **0** dari 11,734

## Parameter yang terpilih di dalam sampel

| Parameter | Jumlah jendela |
|---|---|
| `{"imbalan_R": 8.0, "lookback": 100}` | 61 |
| `{"imbalan_R": 8.0, "lookback": 55}` | 54 |
| `{"imbalan_R": 8.0, "lookback": 20}` | 47 |
| `{"imbalan_R": 6.0, "lookback": 100}` | 34 |
| `{"imbalan_R": 6.0, "lookback": 20}` | 32 |
| `{"imbalan_R": 6.0, "lookback": 55}` | 30 |
| `{"imbalan_R": 4.0, "lookback": 20}` | 26 |
| `{"imbalan_R": 2.0, "lookback": 20}` | 19 |
| `{"imbalan_R": 4.0, "lookback": 55}` | 18 |
| `{"imbalan_R": 4.0, "lookback": 100}` | 15 |
| `{"imbalan_R": 2.0, "lookback": 55}` | 14 |
| `{"imbalan_R": 2.0, "lookback": 100}` | 6 |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| ADAUSDT | 56,800 | 24 | 699 | 120.25 | 0.17203 |
| AAVEUSDT | 50,585 | 21 | 675 | 95.46 | 0.14142 |
| ALGOUSDT | 53,511 | 22 | 737 | 68.72 | 0.09325 |
| 1000BONKUSDT | 23,410 | 8 | 191 | 66.14 | 0.34626 |
| AIUSDT | 20,183 | 7 | 149 | 63.26 | 0.42458 |
| AIOTUSDT | 10,812 | 2 | 32 | 57.55 | 1.79837 |
| 1000FLOKIUSDT | 28,208 | 10 | 335 | 53.28 | 0.15905 |
| ALPHAUSDT | 42,363 | 17 | 561 | 46.98 | 0.08375 |
| 1000PEPEUSDT | 28,232 | 10 | 324 | 46.82 | 0.14451 |
| 1000SHIBUSDT | 45,631 | 19 | 685 | 40.73 | 0.05946 |
