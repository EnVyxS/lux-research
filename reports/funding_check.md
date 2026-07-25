# Pemeriksaan ulang funding rate

1,982,017 baris atas 447 simbol, 2020-01-01 sampai 2026-06-30.

## Kisi sebenarnya

Dua putaran metrik sebelumnya memakai kolom `funding_interval_hours`
sebagai kisi yang berlaku, dan keduanya melaporkan lebih dari separuh
baris sebagai celah. Tabel di bawah mengukur jarak antarbaris apa adanya,
supaya terlihat apakah kolom itu memang dapat dipercaya.

| Jarak antarbaris (jam) | Peristiwa | Pangsa |
|---|---|---|
| 4 | 1,030,440 | 52.00% |
| 8 | 896,332 | 45.23% |
| 1 | 53,009 | 2.68% |
| 2 | 1,764 | 0.09% |
| 3 | 19 | 0.00% |
| 6 | 3 | 0.00% |
| 20016 | 1 | 0.00% |
| 4500 | 1 | 0.00% |
| 504 | 1 | 0.00% |

- Kisi teramati (modus per simbol): {'1.0': 3, '4.0': 267, '8.0': 177}
- Kisi menurut kolom: {'1': 96, '2': 14, '4': 304, '8': 244}
- Simbol yang kolomnya tidak cocok dengan kisi teramati: **0 dari 447**

## Integritas

- Duplikat: **0** | Tidak urut: **0**
- Celah menurut kisi teramati: **587,131** peristiwa pada 447 simbol, setara 41,184 periode hilang
- Celah menurut kolom interval (metrik lama): 1,193,209
- Simbol layak tanpa data funding: 0

## Arah biaya

- Funding positif: 1,563,845 (79.1%) | negatif: 413,944
- Melebihi 2%: 85

Funding positif berarti long membayar short. Pangsa di atas separuh
adalah rintangan struktural bagi strategi yang condong long, dan harus
ditagihkan ke setiap posisi di backtest, bukan diabaikan.

## Sepuluh biaya tahunan tertinggi bagi long

| Simbol | Biaya setahun | Rerata per periode | Kisi teramati | Kolom |
|---|---|---|---|---|
| 1000WHYUSDT | 60.7% | 0.000277 | 4.0 | [4] |
| 1000000BOBUSDT | 60.1% | 0.000274 | 4.0 | [4, 8] |
| BROCCOLIF3BUSDT | 57.0% | 0.000260 | 4.0 | [1, 4, 8] |
| BZRXUSDT | 44.0% | 0.000402 | 8.0 | [8] |
| KOMAUSDT | 43.9% | 0.000201 | 4.0 | [4] |
| 1000RATSUSDT | 43.2% | 0.000197 | 4.0 | [4] |
| SKYAIUSDT | 40.9% | 0.000187 | 4.0 | [4] |
| AGTUSDT | 40.3% | 0.000184 | 4.0 | [4] |
| ARCUSDT | 40.0% | 0.000182 | 4.0 | [4] |
| BULLAUSDT | 33.2% | 0.000151 | 4.0 | [1, 4] |

## Sepuluh funding paling menguntungkan bagi long

| Simbol | Biaya setahun | Rerata per periode | Kisi teramati | Kolom |
|---|---|---|---|---|
| MYXUSDT | -533.9% | -0.000610 | 1.0 | [1, 4] |
| LAUSDT | -272.6% | -0.000311 | 1.0 | [1, 4, 8] |
| FUNUSDT | -121.0% | -0.000552 | 4.0 | [1, 2, 4] |
| SIGNUSDT | -112.1% | -0.000128 | 1.0 | [1, 4] |
| HOMEUSDT | -106.4% | -0.000486 | 4.0 | [1, 4] |
| AERGOUSDT | -102.6% | -0.000468 | 4.0 | [2, 4] |
| MOVEUSDT | -98.8% | -0.000451 | 4.0 | [1, 4] |
| HUSDT | -98.2% | -0.000448 | 4.0 | [1, 4] |
| ORCAUSDT | -88.5% | -0.000404 | 4.0 | [1, 2, 4] |
| SAHARAUSDT | -81.7% | -0.000373 | 4.0 | [1, 4] |

Gerbang lulus: **True**
