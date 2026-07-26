# Backtest H-009 — h009_carry_dipatok

> Dengan sinyal Donchian yang tidak diubah dan grid H-007 yang tidak diubah, memaksa keluar saat carry TEREALISASI melewati 0,25R — ambang yang dipatok konstan dan sengaja dikeluarkan dari ruang parameter — membuat gerbang invarian_risiko lulus. H-008 gagal bukan karena mekanismenya keliru melainkan karena pemilih yang memaksimalkan ekspektasi selalu mematikan pengaman yang memakan ekspektasi. Batas risiko karena itu tidak boleh dilombakan.

Sidik `eac6c83305bd1069` · 12 kombinasi · 40 simbol · 155.4s

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- ekspektasi 0.0414R < 0.05R

## Hasil luar sampel

- Perdagangan: **14,925**
- Total R: **617.28**
- Ekspektasi: **0.041358619824519986**
- Jendela positif: 198/356
- Alasan keluar: {'stop': 10242, 'target': 4111, 'umur': 368, 'akhir_data': 188, 'carry': 16}

## Sembilan gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0003 | 0.3 | 0 dari 40 simbol gagal |
| buy_and_hold | lulus | 0.7333 | 0.0 | median selisih 0.7333; unggul di 36/40 simbol |
| entri_acak | lulus | 0.0099 | 0.05 | 0 dari 100 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | lulus | -1.2698 | -1.5 | kerugian terburuk -1.270R dari 14925 perdagangan |
| funding | lulus | 10199.5891 | 0.0 | total funding mutlak 10199.589140 atas 14925 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 40 simbol gagal |
| checksum | lulus | 0.0000 | 0.0 | hilang 0, asing 0, tidak cocok 0 |
| survivorship | lulus | 0.8555 | 0.5 | porsi delisted diuji 0.1250 vs universe 0.1461 |

## Pembongkaran biaya

- Rerata biaya transaksi: **0.0343R**
- Rerata biaya funding: **0.0003R**
- Rerata jarak stop terhadap harga: **3.605%**
- Perdagangan dengan biaya melebihi 1R: **0** dari 14,925

## Parameter yang terpilih di dalam sampel

| Parameter | Jumlah jendela |
|---|---|
| `{"imbalan_R": 4.0, "lookback": 100}` | 82 |
| `{"imbalan_R": 4.0, "lookback": 20}` | 64 |
| `{"imbalan_R": 4.0, "lookback": 55}` | 48 |
| `{"imbalan_R": 3.0, "lookback": 20}` | 42 |
| `{"imbalan_R": 3.0, "lookback": 100}` | 32 |
| `{"imbalan_R": 3.0, "lookback": 55}` | 27 |
| `{"imbalan_R": 2.0, "lookback": 20}` | 14 |
| `{"imbalan_R": 2.0, "lookback": 100}` | 12 |
| `{"imbalan_R": 2.0, "lookback": 55}` | 12 |
| `{"imbalan_R": 1.0, "lookback": 20}` | 11 |
| `{"imbalan_R": 1.0, "lookback": 100}` | 7 |
| `{"imbalan_R": 1.0, "lookback": 55}` | 5 |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| ADAUSDT | 56,800 | 24 | 911 | 113.30 | 0.12437 |
| ALGOUSDT | 53,511 | 22 | 977 | 73.75 | 0.07549 |
| 1000FLOKIUSDT | 28,208 | 10 | 389 | 70.76 | 0.18189 |
| ALPHAUSDT | 42,363 | 17 | 682 | 65.82 | 0.09651 |
| AIOTUSDT | 10,812 | 2 | 44 | 60.09 | 1.36566 |
| AIUSDT | 20,183 | 7 | 215 | 53.59 | 0.24926 |
| 1000SATSUSDT | 22,930 | 8 | 261 | 53.22 | 0.20391 |
| 1000PEPEUSDT | 28,232 | 10 | 348 | 48.74 | 0.14006 |
| 1000BONKUSDT | 23,410 | 8 | 300 | 46.38 | 0.15459 |
| 1000CHEEMSUSDT | 14,557 | 4 | 193 | 39.24 | 0.20332 |
