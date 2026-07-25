# Backtest H-004 — h004_adx

> Penembusan Donchian yang hanya diperdagangkan saat ADX(14) berada di 30 atau lebih menghasilkan ekspektasi positif setelah biaya nyata, pada kerangka eksekusi yang sama persis dengan H-002.

Sidik `98d6a5e15b2cc08b` · 3 kombinasi · 40 simbol · 27.3s

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- ekspektasi -0.0182R < 0.05R
- jendela positif 0.43 < 0.5

## Hasil luar sampel

- Perdagangan: **7,899**
- Total R: **-143.63**
- Ekspektasi: **-0.018183920344457614**
- Jendela positif: 154/356
- Alasan keluar: {'target': 2659, 'stop': 5127, 'akhir_data': 66, 'umur': 47}

## Sembilan gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0003 | 0.3 | 0 dari 40 simbol gagal |
| buy_and_hold | lulus | 0.7111 | 0.0 | median selisih 0.7111; unggul di 34/40 simbol |
| entri_acak | lulus | 0.0099 | 0.05 | 0 dari 100 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | lulus | -1.4067 | -1.5 | kerugian terburuk -1.407R dari 7899 perdagangan |
| funding | lulus | 3645.5676 | 0.0 | total funding mutlak 3645.567600 atas 7899 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 40 simbol gagal |
| checksum | lulus | 0.0000 | 0.0 | hilang 0, asing 0, tidak cocok 0 |
| survivorship | lulus | 0.8555 | 0.5 | porsi delisted diuji 0.1250 vs universe 0.1461 |

## Pembongkaran biaya

- Rerata biaya transaksi: **0.0313R**
- Rerata biaya funding: **-0.0001R**
- Rerata jarak stop terhadap harga: **3.942%**
- Perdagangan dengan biaya melebihi 1R: **0** dari 7,899

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| 1000PEPEUSDT | 28,232 | 10 | 223 | 58.70 | 0.26323 |
| AIOTUSDT | 10,812 | 2 | 57 | 32.12 | 0.56352 |
| 1000CHEEMSUSDT | 14,557 | 4 | 147 | 30.50 | 0.20747 |
| AEROUSDT | 14,338 | 4 | 109 | 23.39 | 0.21461 |
| 1000SATSUSDT | 22,930 | 8 | 178 | 20.32 | 0.11417 |
| AINUSDT | 9,110 | 2 | 36 | 14.65 | 0.40702 |
| 1000LUNCUSDT | 33,947 | 13 | 236 | 11.79 | 0.04997 |
| 1000FLOKIUSDT | 28,208 | 10 | 218 | 11.74 | 0.05384 |
| 1000CATUSDT | 15,396 | 5 | 139 | 10.01 | 0.07198 |
| 1000SHIBUSDT | 45,631 | 19 | 364 | 9.95 | 0.02733 |
