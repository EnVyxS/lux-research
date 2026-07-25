# Backtest H-005 — h005_retest

> Menunda entri sampai harga kembali menyentuh level Donchian 55 yang baru ditembus lalu menutup di sisi penembusan menghasilkan ekspektasi positif setelah biaya nyata, pada kerangka eksekusi yang sama persis dengan H-002.

Sidik `9c4b6324e79569eb` · 3 kombinasi · 40 simbol · 37.0s

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- ekspektasi -0.0357R < 0.05R
- p entri acak 0.0396 > 0.0167
- jendela positif 0.42 < 0.5

Gerbang gagal: invarian_risiko

## Hasil luar sampel

- Perdagangan: **12,194**
- Total R: **-435.49**
- Ekspektasi: **-0.03571355152313172**
- Jendela positif: 151/356
- Alasan keluar: {'target': 4057, 'stop': 7962, 'umur': 66, 'akhir_data': 109}

## Sembilan gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0003 | 0.3 | 0 dari 40 simbol gagal |
| buy_and_hold | lulus | 0.6375 | 0.0 | median selisih 0.6375; unggul di 34/40 simbol |
| entri_acak | lulus | 0.0396 | 0.05 | 3 dari 100 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -1.9122 | -1.5 | kerugian terburuk -1.912R dari 12194 perdagangan |
| funding | lulus | 6100.9307 | 0.0 | total funding mutlak 6100.930675 atas 12194 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 40 simbol gagal |
| checksum | lulus | 0.0000 | 0.0 | hilang 0, asing 0, tidak cocok 0 |
| survivorship | lulus | 0.8555 | 0.5 | porsi delisted diuji 0.1250 vs universe 0.1461 |

## Pembongkaran biaya

- Rerata biaya transaksi: **0.0339R**
- Rerata biaya funding: **0.0016R**
- Rerata jarak stop terhadap harga: **3.574%**
- Perdagangan dengan biaya melebihi 1R: **0** dari 12,194

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| 1000BONKUSDT | 23,410 | 8 | 321 | 34.97 | 0.10896 |
| 1MBABYDOGEUSDT | 16,237 | 5 | 176 | 25.39 | 0.14424 |
| AEROUSDT | 14,338 | 4 | 165 | 21.75 | 0.13182 |
| 1000SATSUSDT | 22,930 | 8 | 234 | 18.34 | 0.07836 |
| 1000000BOBUSDT | 9,952 | 2 | 35 | 12.67 | 0.36192 |
| AIOTUSDT | 10,812 | 2 | 66 | 11.43 | 0.1732 |
| AINUSDT | 9,110 | 2 | 58 | 10.88 | 0.18758 |
| AAVEUSDT | 50,585 | 21 | 768 | 8.89 | 0.01157 |
| AEVOUSDT | 20,723 | 7 | 269 | 8.84 | 0.03288 |
| 1000CATUSDT | 15,396 | 5 | 200 | 8.70 | 0.04351 |
