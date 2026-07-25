# Pemeriksaan ulang funding rate

1,982,017 baris atas 447 simbol, 2020-01-01 sampai 2026-06-30.

## Sebaran jarak antarbaris

Tabel ini yang seharusnya dibuat lebih dulu. Tiga putaran metrik celah
gagal karena berteori tentang bentuk kisi tanpa pernah melihatnya.

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

- Kisi yang paling sering dipakai tiap simbol: {'1.0': 3, '4.0': 267, '8.0': 177}
- Simbol yang hidup di lebih dari satu rezim kisi: **295 dari 447**

Kisi funding bukan sifat tetap sebuah simbol. Binance memindahkan
ratusan pasangan dari delapan jam ke empat jam, jadi satu simbol wajar
memiliki dua rezim berdurasi tahunan. Metrik apa pun yang memaksakan
satu kisi untuk seluruh umur simbol akan salah, tidak peduli kisi itu
diambil dari kolom metadata atau diukur dari data.

## Integritas

- Duplikat: **0** | Tidak urut: **0**
- Celah sejati, yaitu jarak melebihi 8 jam: **266612** peristiwa pada 202 simbol, setara 10,720 penagihan tak tercatat
- Jarak tidak selaras kisi sah, penyelarasan saat pindah rezim: 22
- Simbol layak tanpa data funding: 0

## Arah biaya

- Funding positif: 1,563,845 (79.1%) | negatif: 413,944
- Melebihi 2%: 85

Funding positif berarti long membayar short. Pangsa di atas separuh
adalah rintangan struktural bagi strategi yang condong long, dan harus
ditagihkan ke setiap posisi di backtest, bukan diabaikan.

## Sepuluh biaya tahunan tertinggi bagi long

Angka setahun adalah ekstrapolasi rerata historis, bukan ramalan. Ia
dipakai untuk menakar besaran rintangan, bukan sebagai masukan strategi.

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
| FUNUSDT | -121.0% | -0.000552 | 4.0 | [1, 2, 4] |
| SIGNUSDT | -112.1% | -0.000128 | 1.0 | [1, 2, 4, 8] |
| HOMEUSDT | -106.4% | -0.000486 | 4.0 | [1, 4, 8] |
| AERGOUSDT | -102.6% | -0.000468 | 4.0 | [2, 4, 8] |
| MOVEUSDT | -98.8% | -0.000451 | 4.0 | [1, 4, 8] |
| HUSDT | -98.2% | -0.000448 | 4.0 | [1, 2, 4, 8] |
| ORCAUSDT | -88.5% | -0.000404 | 4.0 | [1, 2, 4, 8] |
| SAHARAUSDT | -81.7% | -0.000373 | 4.0 | [1, 4, 8] |

## Simbol dengan celah sejati

| Simbol | Peristiwa | Penagihan hilang | Kisi utama |
|---|---|---|---|
| BNTUSDT | 862 | 2,501 | 8.0 |
| TRBUSDT | 1332 | 1,332 | 4.0 |
| BLZUSDT | 1310 | 1,310 | 4.0 |
| FLMUSDT | 1298 | 1,298 | 4.0 |
| STMXUSDT | 1106 | 1,106 | 4.0 |
| LPTUSDT | 794 | 794 | 4.0 |
| IMXUSDT | 676 | 676 | 4.0 |
| API3USDT | 659 | 659 | 4.0 |
| LITUSDT | 1433 | 562 | 8.0 |
| PERPUSDT | 158 | 158 | 4.0 |
| PUMPUSDT | 1 | 125 | 4.0 |
| UMAUSDT | 102 | 102 | 4.0 |
| NMRUSDT | 29 | 29 | 4.0 |
| YGGUSDT | 17 | 17 | 4.0 |
| DODOXUSDT | 14 | 14 | 4.0 |
| BROCCOLIF3BUSDT | 13 | 13 | 4.0 |
| CYBERUSDT | 9 | 9 | 4.0 |
| HIFIUSDT | 5 | 5 | 4.0 |
| CATIUSDT | 2 | 2 | 4.0 |
| BANANAS31USDT | 1 | 1 | 4.0 |

Jeda sepanjang ini adalah penghentian perdagangan sungguhan, bukan
data yang hilang: tidak ada funding ditagihkan ketika pasangannya
memang tidak diperdagangkan.

Gerbang lulus: **True**
