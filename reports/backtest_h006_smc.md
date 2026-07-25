# Backtest H-006 — h006_smc

> Sapuan likuiditas — sumbu yang menembus ekstrem N bar sebelumnya lalu ditutup kembali ke dalam rentang, diperdagangkan berlawanan arah sapuan — menghasilkan ekspektasi positif setelah biaya nyata, pada kerangka eksekusi yang sama persis dengan H-002.

Sidik `e503a9a833182b25` · 3 kombinasi · 40 simbol · 29.5s

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- ekspektasi -0.1345R < 0.05R
- p entri acak 1.0000 > 0.0167
- jendela positif 0.21 < 0.5

Gerbang gagal: entri_acak, invarian_risiko

## Hasil luar sampel

- Perdagangan: **20,385**
- Total R: **-2741.51**
- Ekspektasi: **-0.13448663469274041**
- Jendela positif: 76/356
- Alasan keluar: {'target': 6032, 'stop': 13993, 'akhir_data': 210, 'umur': 150}

## Sembilan gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0003 | 0.3 | 0 dari 40 simbol gagal |
| buy_and_hold | lulus | 0.4065 | 0.0 | median selisih 0.4065; unggul di 31/40 simbol |
| entri_acak | GAGAL | 1.0000 | 0.05 | 100 dari 100 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -1.6780 | -1.5 | kerugian terburuk -1.678R dari 20385 perdagangan |
| funding | lulus | 11140.5541 | 0.0 | total funding mutlak 11140.554099 atas 20385 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 40 simbol gagal |
| checksum | lulus | 0.0000 | 0.0 | hilang 0, asing 0, tidak cocok 0 |
| survivorship | lulus | 0.8555 | 0.5 | porsi delisted diuji 0.1250 vs universe 0.1461 |

## Pembongkaran biaya

- Rerata biaya transaksi: **0.0336R**
- Rerata biaya funding: **-0.0026R**
- Rerata jarak stop terhadap harga: **3.603%**
- Perdagangan dengan biaya melebihi 1R: **0** dari 20,385

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| ACXUSDT | 14,289 | 4 | 210 | 20.64 | 0.09828 |
| 1000000BOBUSDT | 9,952 | 2 | 66 | 11.51 | 0.17441 |
| AGTUSDT | 10,334 | 2 | 95 | 9.13 | 0.09609 |
| 1000CHEEMSUSDT | 14,557 | 4 | 200 | 5.06 | 0.02531 |
| ANIMEUSDT | 13,135 | 4 | 157 | -2.67 | -0.01698 |
| 1000WHYUSDT | 11,446 | 3 | 98 | -5.65 | -0.0577 |
| AIXBTUSDT | 13,950 | 4 | 314 | -12.00 | -0.03822 |
| ALCHUSDT | 13,525 | 4 | 201 | -18.94 | -0.09422 |
| AIOTUSDT | 10,812 | 2 | 92 | -22.77 | -0.24749 |
| 1000CATUSDT | 15,396 | 5 | 302 | -24.56 | -0.08131 |
