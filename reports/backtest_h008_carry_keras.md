# Backtest H-008 — h008_carry_keras

> Dengan sinyal Donchian yang tidak diubah sama sekali, menambahkan keluar paksa saat carry TEREALISASI melewati ambang yang dipilih walk-forward menghasilkan ekspektasi bersih di luar sampel minimal 0,05R dan membuat gerbang invarian_risiko lulus. Saringan ADR-004 menebak biaya sekali di saat entri dan tidak pernah menilai ulang; pengaman ini tidak menebak apa pun, ia menjumlahkan penagihan yang sudah terjadi pada pembukaan tiap bar.

Sidik `dfeeea04fd4107f6` · 36 kombinasi · 40 simbol · 208.6s

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- ekspektasi 0.0413R < 0.05R

Gerbang gagal: invarian_risiko

## Hasil luar sampel

- Perdagangan: **14,933**
- Total R: **616.20**
- Ekspektasi: **0.04126450148301717**
- Jendela positif: 198/356
- Alasan keluar: {'stop': 10254, 'target': 4117, 'umur': 371, 'akhir_data': 189, 'carry': 2}

## Sembilan gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0003 | 0.3 | 0 dari 40 simbol gagal |
| buy_and_hold | lulus | 0.7333 | 0.0 | median selisih 0.7333; unggul di 36/40 simbol |
| entri_acak | lulus | 0.0099 | 0.05 | 0 dari 100 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -1.9769 | -1.5 | kerugian terburuk -1.977R dari 14933 perdagangan |
| funding | lulus | 10253.9714 | 0.0 | total funding mutlak 10253.971383 atas 14933 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 40 simbol gagal |
| checksum | lulus | 0.0000 | 0.0 | hilang 0, asing 0, tidak cocok 0 |
| survivorship | lulus | 0.8555 | 0.5 | porsi delisted diuji 0.1250 vs universe 0.1461 |

## Pembongkaran biaya

- Rerata biaya transaksi: **0.0343R**
- Rerata biaya funding: **0.0004R**
- Rerata jarak stop terhadap harga: **3.606%**
- Perdagangan dengan biaya melebihi 1R: **0** dari 14,933

## Parameter yang terpilih di dalam sampel

| Parameter | Jumlah jendela |
|---|---|
| `{"imbalan_R": 4.0, "lookback": 100, "maks_carry_realisasi_R": 0.0}` | 78 |
| `{"imbalan_R": 4.0, "lookback": 20, "maks_carry_realisasi_R": 0.0}` | 59 |
| `{"imbalan_R": 4.0, "lookback": 55, "maks_carry_realisasi_R": 0.0}` | 40 |
| `{"imbalan_R": 3.0, "lookback": 20, "maks_carry_realisasi_R": 0.0}` | 38 |
| `{"imbalan_R": 3.0, "lookback": 100, "maks_carry_realisasi_R": 0.0}` | 30 |
| `{"imbalan_R": 3.0, "lookback": 55, "maks_carry_realisasi_R": 0.0}` | 29 |
| `{"imbalan_R": 2.0, "lookback": 20, "maks_carry_realisasi_R": 0.0}` | 14 |
| `{"imbalan_R": 2.0, "lookback": 55, "maks_carry_realisasi_R": 0.0}` | 12 |
| `{"imbalan_R": 2.0, "lookback": 100, "maks_carry_realisasi_R": 0.0}` | 11 |
| `{"imbalan_R": 1.0, "lookback": 20, "maks_carry_realisasi_R": 0.0}` | 11 |
| `{"imbalan_R": 1.0, "lookback": 100, "maks_carry_realisasi_R": 0.0}` | 7 |
| `{"imbalan_R": 4.0, "lookback": 20, "maks_carry_realisasi_R": 0.25}` | 6 |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| ADAUSDT | 56,800 | 24 | 911 | 113.21 | 0.12427 |
| ALGOUSDT | 53,511 | 22 | 977 | 72.71 | 0.07443 |
| 1000FLOKIUSDT | 28,208 | 10 | 388 | 70.81 | 0.1825 |
| ALPHAUSDT | 42,363 | 17 | 682 | 65.82 | 0.09651 |
| AIOTUSDT | 10,812 | 2 | 44 | 57.38 | 1.30399 |
| AIUSDT | 20,183 | 7 | 215 | 53.59 | 0.24926 |
| 1000SATSUSDT | 22,930 | 8 | 261 | 53.22 | 0.20391 |
| 1000PEPEUSDT | 28,232 | 10 | 348 | 48.74 | 0.14006 |
| 1000BONKUSDT | 23,410 | 8 | 300 | 46.38 | 0.15459 |
| 1000CHEEMSUSDT | 14,557 | 4 | 193 | 39.24 | 0.20332 |
