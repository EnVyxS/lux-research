# Pemeriksaan ulang funding rate

1,982,017 baris atas 447 simbol, 2020-01-01 sampai 2026-06-30.

## Integritas

- Duplikat: **0** | Tidak urut: **0**
- Celah sejati: **1,193,209** pada 447 simbol
- Peralihan kisi (sah): 366 pada 160 simbol
- Simbol layak tanpa data funding: 0
- Sebaran interval funding (jam): {'4': 304, '8': 244, '1': 96, '2': 14}

Angka celah pada putaran pertama, 1.380.741, seluruhnya artefak asumsi
bahwa kisi funding tetap delapan jam. Kisi itu berubah sepanjang hidup
banyak pasangan, dan langkah kini dibaca dari kolom datanya sendiri.

## Arah biaya

- Funding positif: 1,563,845 (79.1%) | negatif: 413,944
- Melebihi 2%: 85

Funding positif berarti long membayar short. Pangsa di atas separuh
adalah rintangan struktural bagi strategi yang condong long, dan harus
ditagihkan ke setiap posisi di backtest, bukan diabaikan.

## Sepuluh biaya tahunan tertinggi bagi long

| Simbol | Biaya setahun | Rerata per periode | Kisi (jam) |
|---|---|---|---|
| 1000WHYUSDT | 60.7% | 0.000277 | [4] |
| BULLAUSDT | 53.1% | 0.000151 | [1, 4] |
| BROCCOLIF3BUSDT | 52.7% | 0.000260 | [1, 4, 8] |
| HIPPOUSDT | 48.8% | 0.000139 | [1, 4] |
| BZRXUSDT | 44.0% | 0.000402 | [8] |
| KOMAUSDT | 43.9% | 0.000201 | [4] |
| 1000RATSUSDT | 43.2% | 0.000197 | [4] |
| SKYAIUSDT | 40.9% | 0.000187 | [4] |
| AGTUSDT | 40.3% | 0.000184 | [4] |
| 1000000BOBUSDT | 40.1% | 0.000274 | [4, 8] |

## Sepuluh funding paling menguntungkan bagi long

| Simbol | Biaya setahun | Rerata per periode | Kisi (jam) |
|---|---|---|---|
| MYXUSDT | -213.6% | -0.000610 | [1, 4] |
| FUNUSDT | -207.4% | -0.000552 | [1, 2, 4] |
| HOMEUSDT | -170.2% | -0.000486 | [1, 4] |
| MOVEUSDT | -158.1% | -0.000451 | [1, 4] |
| HUSDT | -157.1% | -0.000448 | [1, 4] |
| ORCAUSDT | -151.7% | -0.000404 | [1, 2, 4] |
| AERGOUSDT | -136.8% | -0.000468 | [2, 4] |
| SAHARAUSDT | -130.7% | -0.000373 | [1, 4] |
| FUSDT | -125.2% | -0.000357 | [1, 4] |
| RESOLVUSDT | -123.1% | -0.000351 | [1, 4] |

Gerbang lulus: **True**
