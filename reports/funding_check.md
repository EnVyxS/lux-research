# Pemeriksaan ulang funding rate

1,982,017 baris atas 447 simbol, 2020-01-01 sampai 2026-06-30.

## Sebaran jarak antarbaris

Jarak dibulatkan ke kisi sah terdekat bila selisihnya di bawah satu
menit. Tanpa pembulatan itu, jitter milidetik memecah satu kisi menjadi
puluhan nilai dan menyamar sebagai celah.

| Jarak (jam) | Peristiwa | Pangsa |
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

- Kisi utama tiap simbol: {'1.0': 4, '4.0': 269, '8.0': 174}
- Simbol yang hidup di lebih dari satu rezim: **295 dari 447**
- Jarak yang tidak tepat di kisi namun masih dalam toleransi: 1,193,171, pergeseran terbesar 47 ms

Kisi funding bukan sifat tetap sebuah simbol. Binance memindahkan
ratusan pasangan dari delapan jam ke empat jam, jadi satu simbol wajar
memiliki dua rezim berdurasi tahunan.

## Integritas

- Duplikat: **0** | Tidak urut: **0**
- Celah sejati, jarak melebihi 8 jam di luar toleransi: **3** peristiwa pada 3 simbol, setara 3,188 penagihan tak tercatat
- Jarak tidak selaras kisi sah: 22
- Simbol layak tanpa data funding: 0

## Arah biaya

- Funding positif: 1,563,845 (79.1%) | negatif: 413,944
- Melebihi 2%: 85

Funding positif berarti long membayar short. Pangsa di atas separuh
adalah rintangan struktural bagi strategi yang condong long, dan harus
ditagihkan ke setiap posisi di backtest, bukan diabaikan.

## Sepuluh biaya tahunan tertinggi bagi long

Angka setahun adalah ekstrapolasi rerata historis, bukan ramalan.

| Simbol | Biaya setahun | Rerata per periode | Kisi utama | Rezim |
|---|---|---|---|---|
| 1000WHYUSDT | 60.7% | 0.000277 | 4.0 | [4] |
| 1000000BOBUSDT | 60.1% | 0.000274 | 4.0 | [4, 8] |
| BROCCOLIF3BUSDT | 57.0% | 0.000260 | 4.0 | [1, 4, 8] |
| BZRXUSDT | 44.0% | 0.000402 | 8.0 | [8] |
| KOMAUSDT | 43.9% | 0.000201 | 4.0 | [4, 8] |
| 1000RATSUSDT | 43.2% | 0.000197 | 4.0 | [4, 8] |
| SKYAIUSDT | 40.9% | 0.000187 | 4.0 | [4, 8] |
| AGTUSDT | 40.3% | 0.000184 | 4.0 | [4, 8] |
| ARCUSDT | 40.0% | 0.000182 | 4.0 | [4, 8] |
| BULLAUSDT | 33.2% | 0.000151 | 4.0 | [1, 2, 4, 8] |

## Sepuluh funding paling menguntungkan bagi long

| Simbol | Biaya setahun | Rerata per periode | Kisi utama | Rezim |
|---|---|---|---|---|
| MYXUSDT | -533.9% | -0.000610 | 1.0 | [1, 4, 8] |
| LAUSDT | -272.6% | -0.000311 | 1.0 | [1, 4, 8] |
| LAYERUSDT | -230.7% | -0.000263 | 1.0 | [1, 2, 4, 8] |
| FUNUSDT | -121.0% | -0.000552 | 4.0 | [1, 2, 4] |
| SIGNUSDT | -112.1% | -0.000128 | 1.0 | [1, 2, 4, 8] |
| HOMEUSDT | -106.4% | -0.000486 | 4.0 | [1, 4, 8] |
| AERGOUSDT | -102.6% | -0.000468 | 4.0 | [2, 4, 8] |
| MOVEUSDT | -98.8% | -0.000451 | 4.0 | [1, 4, 8] |
| HUSDT | -98.2% | -0.000448 | 4.0 | [1, 2, 4, 8] |
| ORCAUSDT | -88.5% | -0.000404 | 4.0 | [1, 2, 4, 8] |

## Simbol dengan celah sejati

| Simbol | Peristiwa | Penagihan hilang | Kisi utama |
|---|---|---|---|
| BNTUSDT | 1 | 2,501 | 8.0 |
| LITUSDT | 1 | 562 | 8.0 |
| PUMPUSDT | 1 | 125 | 4.0 |

Jeda sepanjang ini adalah penghentian perdagangan sungguhan, bukan
data hilang: tidak ada funding ditagihkan ketika pasangannya memang
tidak diperdagangkan. Backtest harus memperlakukan rentang ini
sebagai periode tanpa posisi, bukan sebagai biaya nol.

Gerbang lulus: **True**
