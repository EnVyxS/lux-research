# Log backtest H-013

Run: `30214203863`
Commit: `93a4309b05a04f0124a09efbb13d5fbcdfba8ed9`

## Berkas hasil

Laporan yang dikomit tanpa backtest_h013_kontribusi.json berarti run GAGAL.

```
-rw-r--r-- 1 runner runner 4318 Jul 26 18:21 reports/backtest_h013_kontribusi.json
-rw-r--r-- 1 runner runner 1948 Jul 26 18:21 reports/backtest_h013_kontribusi.md

--- laporan per sel ---
-rw-r--r-- 1 runner runner 432490 Jul 26 18:21 reports/backtest_h013_ah_acak_horizon.json
-rw-r--r-- 1 runner runner 432584 Jul 26 18:19 reports/backtest_h013_as_acak_stop.json
-rw-r--r-- 1 runner runner   4318 Jul 26 18:21 reports/backtest_h013_kontribusi.json
-rw-r--r-- 1 runner runner 431966 Jul 26 18:16 reports/backtest_h013_sh_sinyal_horizon.json
-rw-r--r-- 1 runner runner 432200 Jul 26 18:14 reports/backtest_h013_ss_sinyal_stop.json
```

## logs/deps.log

```
Requirement already satisfied: pip in /opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/site-packages (26.1.2)
Collecting pytest
  Downloading pytest-9.1.1-py3-none-any.whl.metadata (7.6 kB)
Collecting pandas==2.2.3 (from -r requirements.txt (line 1))
  Downloading pandas-2.2.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (89 kB)
Collecting pyarrow==17.0.0 (from -r requirements.txt (line 2))
  Downloading pyarrow-17.0.0-cp312-cp312-manylinux_2_28_x86_64.whl.metadata (3.3 kB)
Collecting pyyaml==6.0.2 (from -r requirements.txt (line 6))
  Downloading PyYAML-6.0.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.1 kB)
Collecting numpy>=1.26.0 (from pandas==2.2.3->-r requirements.txt (line 1))
  Downloading numpy-2.5.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (6.6 kB)
Collecting python-dateutil>=2.8.2 (from pandas==2.2.3->-r requirements.txt (line 1))
  Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl.metadata (8.4 kB)
Collecting pytz>=2020.1 (from pandas==2.2.3->-r requirements.txt (line 1))
  Downloading pytz-2026.3.post1-py2.py3-none-any.whl.metadata (22 kB)
Collecting tzdata>=2022.7 (from pandas==2.2.3->-r requirements.txt (line 1))
  Downloading tzdata-2026.3-py2.py3-none-any.whl.metadata (1.4 kB)
Collecting iniconfig>=1.0.1 (from pytest)
  Downloading iniconfig-2.3.0-py3-none-any.whl.metadata (2.5 kB)
Collecting packaging>=22 (from pytest)
  Downloading packaging-26.2-py3-none-any.whl.metadata (3.5 kB)
Collecting pluggy<2,>=1.5 (from pytest)
  Downloading pluggy-1.6.0-py3-none-any.whl.metadata (4.8 kB)
Collecting pygments>=2.7.2 (from pytest)
  Downloading pygments-2.20.0-py3-none-any.whl.metadata (2.5 kB)
Collecting six>=1.5 (from python-dateutil>=2.8.2->pandas==2.2.3->-r requirements.txt (line 1))
  Downloading six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
Downloading pandas-2.2.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (12.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.7/12.7 MB 205.7 MB/s  0:00:00
Downloading pyarrow-17.0.0-cp312-cp312-manylinux_2_28_x86_64.whl (39.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 39.9/39.9 MB 90.6 MB/s  0:00:00
Downloading PyYAML-6.0.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (767 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 767.5/767.5 kB 131.2 MB/s  0:00:00
Downloading pytest-9.1.1-py3-none-any.whl (386 kB)
Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)
Downloading numpy-2.5.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.7/16.7 MB 291.7 MB/s  0:00:00
Downloading packaging-26.2-py3-none-any.whl (100 kB)
Downloading pygments-2.20.0-py3-none-any.whl (1.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 203.2 MB/s  0:00:00
Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
Downloading pytz-2026.3.post1-py2.py3-none-any.whl (508 kB)
Downloading six-1.17.0-py2.py3-none-any.whl (11 kB)
Downloading tzdata-2026.3-py2.py3-none-any.whl (348 kB)
Installing collected packages: pytz, tzdata, six, pyyaml, pygments, pluggy, packaging, numpy, iniconfig, python-dateutil, pytest, pyarrow, pandas

Successfully installed iniconfig-2.3.0 numpy-2.5.1 packaging-26.2 pandas-2.2.3 pluggy-1.6.0 pyarrow-17.0.0 pygments-2.20.0 pytest-9.1.1 python-dateutil-2.9.0.post0 pytz-2026.3.post1 pyyaml-6.0.2 six-1.17.0 tzdata-2026.3
numpy 2.5.1
pytest 9.1.1
```

## logs/uji.log

```
........................................................................ [  9%]
........................................................................ [ 19%]
........................................................................ [ 29%]
........................................................................ [ 38%]
........................................................................ [ 48%]
........................................................................ [ 58%]
........................................................................ [ 68%]
........................................................................ [ 77%]
........................................................................ [ 87%]
........................................................................ [ 97%]
...................                                                      [100%]
739 passed in 2.80s
```

## logs/preflight.log

```
1. mekanisme diimpor tanpa perubahan, imbalan BEKU: OK
2. ambang ADR-015 tidak bergerak: OK
3. angka kembar, pengaman DIPASANG dasar_riset: OK
4. jendela 4h {'panjang_latih': 1080, 'panjang_uji': 540, 'embargo': 42}, satu jendela 1862 bar (1h 6848): OK
5. pakai_target, batas umur, dan pengaman per sel: OK
6. bawaan pengaman dan lantai tetap MATI: OK
7. permutasi memakai seed dan mekanisme gerbang: OK
8. angka haram tidak dipakai, sidik empat sel berbeda: OK

pagar pra-terbang H-013: LULUS
lantai 0.004, pengaman 0.5R
empat sel ['SS', 'SH', 'AS', 'AH'], 3 kandidat per sel
KONSEKUENSI KONSTRUKSI (bukan temuan): lookahead dan entri_acak GAGAL pada sel AS dan AH
  ramalan sumbangan_sinyal_R: 0,000-0,015 sehingga GAGAL terhadap ambang 0,020; ini ramalan ADR-015 bagian 4.5 yang diulang tanpa perubahan
  ramalan sumbangan_geometri_R: nilai mutlaknya LEBIH BESAR daripada sumbangan sinyal
  ramalan invarian_risiko: gagal pada SH dan AH, lulus atau hampir lulus pada SS; sebabnya umur mengisi di harga bar sungguhan sedangkan jalur stop tidak, jadi itu BUKAN bukti target lebih baik
  ramalan peringkat_AH: AH belum tentu terburuk; bila AH mengalahkan AS, yang terukur adalah keunggulan geometri di atas sinyal nol
```

## logs/lantai.log

```
lantai=0.004
```

## logs/unduh.log

```
16
157M	aset
--- berkas 4h ---
-rw-r--r--  1 runner runner 23609925 Jul 26 18:12 ohlcv_4h_shard00.parquet
-rw-r--r--  1 runner runner 19595753 Jul 26 18:12 ohlcv_4h_shard01.parquet
-rw-r--r--  1 runner runner 17515963 Jul 26 18:12 ohlcv_4h_shard02.parquet
-rw-r--r--  1 runner runner 18412119 Jul 26 18:12 ohlcv_4h_shard03.parquet
-rw-r--r--  1 runner runner 19904881 Jul 26 18:12 ohlcv_4h_shard04.parquet
-rw-r--r--  1 runner runner 17959843 Jul 26 18:12 ohlcv_4h_shard05.parquet
-rw-r--r--  1 runner runner 17326751 Jul 26 18:12 ohlcv_4h_shard06.parquet
-rw-r--r--  1 runner runner 17844356 Jul 26 18:12 ohlcv_4h_shard07.parquet
-rw-r--r--  1 runner runner  1362914 Jul 26 18:12 ohlcv_4h_tail_shard00.parquet
-rw-r--r--  1 runner runner  1437885 Jul 26 18:12 ohlcv_4h_tail_shard01.parquet
-rw-r--r--  1 runner runner  1364053 Jul 26 18:12 ohlcv_4h_tail_shard02.parquet
-rw-r--r--  1 runner runner  1294176 Jul 26 18:12 ohlcv_4h_tail_shard03.parquet
```

## logs/backtest.log

```
H-013 empat sel: ['SS', 'SH', 'AS', 'AH']
kandidat per sel: 3 (imbalan BEKU 2.0)
batas umur: sel stop 42 bar 4h = 7 hari, sel horizon 48 bar 4h (config 168 TIDAK dipakai)
ADR-023 jendela 4h: latih 1080 (180 hari), uji 540 (90 hari), embargo 42 (7 hari), pemanasan 200 bar TIDAK dikonversi
bar dibutuhkan satu jendela: 1862 (bawaan 1h akan menuntut 6848)
lantai median stop_frac: 0.004
pengaman biaya masuk: 0.5R, stop_hormati_celah True (keduanya DIPASANG dasar_riset; pemuat config tidak membacanya)
ulangan permutasi per sel: 300
seed permutasi: 42 (sama dengan gerbang)
skor acak terdahulu yang memicu H-013: 0.04661R, identik di H-010 dan H-012
KONSEKUENSI KONSTRUKSI (bukan temuan): lookahead dan entri_acak akan GAGAL pada sel AS dan AH; kelulusan gerbang hanya syarat pada SS
  ramalan sumbangan_sinyal_R: 0,000-0,015 sehingga GAGAL terhadap ambang 0,020; ini ramalan ADR-015 bagian 4.5 yang diulang tanpa perubahan
  ramalan sumbangan_geometri_R: nilai mutlaknya LEBIH BESAR daripada sumbangan sinyal
  ramalan invarian_risiko: gagal pada SH dan AH, lulus atau hampir lulus pada SS; sebabnya umur mengisi di harga bar sungguhan sedangkan jalur stop tidak, jadi itu BUKAN bukti target lebih baik
  ramalan peringkat_AH: AH belum tentu terburuk; bila AH mengalahkan AS, yang terukur adalah keunggulan geometri di atas sinyal nol
universe layak 438, diuji 438
  ambang ekor datar 6 bar untuk interval 4h
  dibaca ohlcv_4h_shard00.parquet
  dibaca ohlcv_4h_shard01.parquet
  dibaca ohlcv_4h_shard02.parquet
  dibaca ohlcv_4h_shard03.parquet
  dibaca ohlcv_4h_shard04.parquet
  dibaca ohlcv_4h_shard05.parquet
  dibaca ohlcv_4h_shard06.parquet
  dibaca ohlcv_4h_shard07.parquet
  dibaca ohlcv_4h_tail_shard00.parquet
  dibaca ohlcv_4h_tail_shard01.parquet
  dibaca ohlcv_4h_tail_shard02.parquet
  dibaca ohlcv_4h_tail_shard03.parquet
  akhir_per_simbol: 790 simbol dari reports/akhir_sejati_4h.json
438 simbol dimuat, 447 jadwal funding, 790 simbol dipindai untuk survivorship
checksum: hilang 12, asing 12, tidak cocok 0
lantai median stop_frac 0.004: 437 layak, 1 dibuang dari 438 simbol dimuat
  DIBUANG USDCUSDT: median_stop_frac 3.799992e-04, median jarak stop 3.800e-04 di bawah lantai 0.004

### SEL SS: sinyal sungguhan, pakai_target True, maks_umur_bar 42

=== H-013-SS terdaftar di hipotesis/H-013-SS.json (sidik 06c3805bdd7a, 9 kombinasi) ===
  [10/437] 1000SATSUSDT: 152 trade, 1s
  [20/437] ACXUSDT: 70 trade, 3s
  [30/437] AKROUSDT: 41 trade, 4s
  [40/437] ANTUSDT: 117 trade, 6s
  [50/437] ASRUSDT: 29 trade, 8s
  [60/437] AVAXUSDT: 349 trade, 9s
  [70/437] BANANAUSDT: 95 trade, 11s
  [80/437] BICOUSDT: 163 trade, 13s
  [90/437] BRETTUSDT: 89 trade, 14s
  [100/437] C98USDT: 257 trade, 16s
  [110/437] CHRUSDT: 282 trade, 17s
  [120/437] CTSIUSDT: 231 trade, 19s
  [130/437] DFUSDT: 44 trade, 21s
  [140/437] DUSDT: 44 trade, 22s
  [150/437] EOSUSDT: 289 trade, 24s
  [160/437] FIDAUSDT: 68 trade, 26s
  [170/437] FUSDT: 30 trade, 27s
  [180/437] GPSUSDT: 43 trade, 28s
  [190/437] HFTUSDT: 191 trade, 30s
  [200/437] HUSDT: 24 trade, 31s
  [210/437] INJUSDT: 181 trade, 32s
  [220/437] JTOUSDT: 137 trade, 34s
  [230/437] KSMUSDT: 273 trade, 36s
  [240/437] LRCUSDT: 275 trade, 38s
  [250/437] MATICUSDT: 181 trade, 40s
  [260/437] MKRUSDT: 267 trade, 41s
  [270/437] MYROUSDT: 38 trade, 42s
  [280/437] NOTUSDT: 93 trade, 43s
  [290/437] ONTUSDT: 356 trade, 45s
  [300/437] PERPUSDT: 103 trade, 46s
  [310/437] PORTALUSDT: 110 trade, 47s
  [320/437] RAYSOLUSDT: 46 trade, 49s
  [330/437] RNDRUSDT: 42 trade, 50s
  [340/437] SANDUSDT: 279 trade, 52s
  [350/437] SKYAIUSDT: 23 trade, 53s
  [360/437] SQDUSDT: 38 trade, 54s
  [370/437] SUNUSDT: 63 trade, 56s
  [380/437] TACUSDT: 45 trade, 57s
  [390/437] TRBUSDT: 241 trade, 59s
  [400/437] UNIUSDT: 275 trade, 61s
  [410/437] VIRTUALUSDT: 46 trade, 62s
  [420/437] XAIUSDT: 106 trade, 63s
  [430/437] ZECUSDT: 389 trade, 66s
  [437/437] ZRXUSDT: 325 trade, 67s
{
  "jumlah_simbol": 437,
  "jumlah_jendela": 4082,
  "jendela_positif": 2250,
  "jumlah_trade_luar_sampel": 60018,
  "total_R": 4000.0684405855427,
  "ekspektasi_R": 0.06664781299919262
}
alasan keluar: {'target': 18293, 'stop': 33467, 'carry': 92, 'umur': 6474, 'akhir_data': 1692}
entri ditolak pengaman biaya: 0 (pengaman 0.5R, lantai semesta 0.004)
bulan dengan perdagangan: 73
parameter terpilih: {'{"imbalan_R": 2.0, "lookback": 55}': 846, '{"imbalan_R": 2.0, "lookback": 20}': 1682, '{"imbalan_R": 2.0, "lookback": 100}': 1554}
konsentrasi: 317 untung / 120 rugi dari 437 simbol; drop-1 0.06575R (retensi 0.9866), drop-22 0.05400R, median simbol +0.06697R, porsi bruto teratas 0.0155 (BNBUSDT), setara 182.7 simbol
funding ekor: porsi ekor maks 0.0273 (rerata 0.0027 atas 10 terburuk), funding maks 0.4243R, 93 dari 60018 trade di atas pengaman (0.00155)
sebaran: std 1.36459R, galat baku 0.005570R, jarak ke ambang +0.016648R = +2.99 galat baku
entri acak: nyata 0.06592R, p 0.016611295681063124
sel SS: 4082 jendela, 60018 trade luar sampel (ambang ternilai 100)

### SEL SH: sinyal sungguhan, pakai_target False, maks_umur_bar 48

=== H-013-SH terdaftar di hipotesis/H-013-SH.json (sidik af1145aab7f1, 9 kombinasi) ===
  [10/437] 1000SATSUSDT: 106 trade, 1s
  [20/437] ACXUSDT: 46 trade, 3s
  [30/437] AKROUSDT: 41 trade, 4s
  [40/437] ANTUSDT: 74 trade, 6s
  [50/437] ASRUSDT: 23 trade, 8s
  [60/437] AVAXUSDT: 228 trade, 10s
  [70/437] BANANAUSDT: 56 trade, 11s
  [80/437] BICOUSDT: 114 trade, 13s
  [90/437] BRETTUSDT: 62 trade, 14s
  [100/437] C98USDT: 206 trade, 16s
  [110/437] CHRUSDT: 225 trade, 17s
  [120/437] CTSIUSDT: 180 trade, 19s
  [130/437] DFUSDT: 32 trade, 21s
  [140/437] DUSDT: 35 trade, 22s
  [150/437] EOSUSDT: 219 trade, 25s
  [160/437] FIDAUSDT: 38 trade, 26s
  [170/437] FUSDT: 23 trade, 28s
  [180/437] GPSUSDT: 31 trade, 29s
  [190/437] HFTUSDT: 144 trade, 30s
  [200/437] HUSDT: 14 trade, 32s
  [210/437] INJUSDT: 146 trade, 33s
  [220/437] JTOUSDT: 98 trade, 35s
  [230/437] KSMUSDT: 208 trade, 36s
  [240/437] LRCUSDT: 209 trade, 38s
  [250/437] MATICUSDT: 117 trade, 40s
  [260/437] MKRUSDT: 199 trade, 42s
  [270/437] MYROUSDT: 48 trade, 43s
  [280/437] NOTUSDT: 63 trade, 44s
  [290/437] ONTUSDT: 280 trade, 46s
  [300/437] PERPUSDT: 84 trade, 47s
  [310/437] PORTALUSDT: 81 trade, 48s
  [320/437] RAYSOLUSDT: 28 trade, 49s
  [330/437] RNDRUSDT: 41 trade, 51s
  [340/437] SANDUSDT: 192 trade, 53s
  [350/437] SKYAIUSDT: 23 trade, 54s
  [360/437] SQDUSDT: 26 trade, 56s
  [370/437] SUNUSDT: 52 trade, 57s
  [380/437] TACUSDT: 20 trade, 58s
  [390/437] TRBUSDT: 260 trade, 60s
  [400/437] UNIUSDT: 222 trade, 62s
  [410/437] VIRTUALUSDT: 28 trade, 63s
  [420/437] XAIUSDT: 84 trade, 64s
  [430/437] ZECUSDT: 253 trade, 67s
  [437/437] ZRXUSDT: 244 trade, 68s
{
  "jumlah_simbol": 437,
  "jumlah_jendela": 4082,
  "jendela_positif": 1981,
  "jumlah_trade_luar_sampel": 44614,
  "total_R": 1658.1521918333708,
  "ekspektasi_R": 0.037166633609032385
}
alasan keluar: {'umur': 14197, 'stop': 28010, 'carry': 320, 'akhir_data': 2087}
entri ditolak pengaman biaya: 0 (pengaman 0.5R, lantai semesta 0.004)
bulan dengan perdagangan: 73
parameter terpilih: {'{"imbalan_R": 2.0, "lookback": 55}': 1069, '{"imbalan_R": 2.0, "lookback": 20}': 1987, '{"imbalan_R": 2.0, "lookback": 100}': 1026}
konsentrasi: 235 untung / 202 rugi dari 437 simbol; drop-1 0.03340R (retensi 0.8987), drop-22 0.01153R, median simbol +0.02524R, porsi bruto teratas 0.0445 (VELVETUSDT), setara 113.3 simbol
funding ekor: porsi ekor maks 0.0273 (rerata 0.0027 atas 10 terburuk), funding maks 0.4064R, 330 dari 44614 trade di atas pengaman (0.00740); gagal: porsi_trade_di_atas_pengaman
sebaran: std 2.18891R, galat baku 0.010363R, jarak ke ambang -0.012833R = -1.24 galat baku
entri acak: nyata 0.05547R, p 0.22591362126245848
sel SH: 4082 jendela, 44614 trade luar sampel (ambang ternilai 100)

### SEL AS: sinyal permutasi, pakai_target True, maks_umur_bar 42

=== H-013-AS terdaftar di hipotesis/H-013-AS.json (sidik 5ee4b130f9ed, 9 kombinasi) ===
  [10/437] 1000SATSUSDT: 102 trade, 1s
  [20/437] ACXUSDT: 42 trade, 3s
  [30/437] AKROUSDT: 44 trade, 5s
  [40/437] ANTUSDT: 85 trade, 6s
  [50/437] ASRUSDT: 23 trade, 8s
  [60/437] AVAXUSDT: 308 trade, 10s
  [70/437] BANANAUSDT: 57 trade, 12s
  [80/437] BICOUSDT: 110 trade, 14s
  [90/437] BRETTUSDT: 80 trade, 16s
  [100/437] C98USDT: 260 trade, 17s
  [110/437] CHRUSDT: 236 trade, 19s
  [120/437] CTSIUSDT: 211 trade, 21s
  [130/437] DFUSDT: 28 trade, 23s
  [140/437] DUSDT: 36 trade, 24s
  [150/437] EOSUSDT: 202 trade, 27s
  [160/437] FIDAUSDT: 73 trade, 28s
  [170/437] FUSDT: 23 trade, 30s
  [180/437] GPSUSDT: 35 trade, 32s
  [190/437] HFTUSDT: 157 trade, 33s
  [200/437] HUSDT: 31 trade, 34s
  [210/437] INJUSDT: 208 trade, 36s
  [220/437] JTOUSDT: 108 trade, 38s
  [230/437] KSMUSDT: 309 trade, 40s
  [240/437] LRCUSDT: 234 trade, 42s
  [250/437] MATICUSDT: 189 trade, 44s
  [260/437] MKRUSDT: 251 trade, 45s
  [270/437] MYROUSDT: 60 trade, 46s
  [280/437] NOTUSDT: 84 trade, 48s
  [290/437] ONTUSDT: 331 trade, 50s
  [300/437] PERPUSDT: 103 trade, 52s
  [310/437] PORTALUSDT: 80 trade, 53s
  [320/437] RAYSOLUSDT: 60 trade, 54s
  [330/437] RNDRUSDT: 41 trade, 56s
  [340/437] SANDUSDT: 291 trade, 58s
  [350/437] SKYAIUSDT: 31 trade, 59s
  [360/437] SQDUSDT: 29 trade, 61s
  [370/437] SUNUSDT: 74 trade, 62s
  [380/437] TACUSDT: 24 trade, 64s
  [390/437] TRBUSDT: 282 trade, 66s
  [400/437] UNIUSDT: 269 trade, 67s
  [410/437] VIRTUALUSDT: 73 trade, 69s
  [420/437] XAIUSDT: 110 trade, 70s
  [430/437] ZECUSDT: 334 trade, 73s
  [437/437] ZRXUSDT: 271 trade, 75s
{
  "jumlah_simbol": 437,
  "jumlah_jendela": 4082,
  "jendela_positif": 2046,
  "jumlah_trade_luar_sampel": 55927,
  "total_R": 660.2574539074326,
  "ekspektasi_R": 0.01180570125176449
}
alasan keluar: {'target': 14491, 'umur': 8574, 'stop': 30853, 'akhir_data': 1913, 'carry': 96}
entri ditolak pengaman biaya: 0 (pengaman 0.5R, lantai semesta 0.004)
bulan dengan perdagangan: 73
parameter terpilih: {'{"imbalan_R": 2.0, "lookback": 55}': 1089, '{"imbalan_R": 2.0, "lookback": 100}': 1585, '{"imbalan_R": 2.0, "lookback": 20}': 1408}
konsentrasi: 248 untung / 189 rugi dari 437 simbol; drop-1 0.01097R (retensi 0.9288), drop-22 -0.00040R, median simbol +0.02012R, porsi bruto teratas 0.0197 (ETHUSDT), setara 144.8 simbol; sub-uji gagal: drop_5persen_positif
funding ekor: porsi ekor maks 0.0108 (rerata 0.0024 atas 10 terburuk), funding maks 0.4213R, 99 dari 55927 trade di atas pengaman (0.00177)
sebaran: std 1.30621R, galat baku 0.005523R, jarak ke ambang -0.038194R = -6.92 galat baku
entri acak: nyata 0.00018R, p 0.3588039867109635
sel AS: 4082 jendela, 55927 trade luar sampel (ambang ternilai 100)

### SEL AH: sinyal permutasi, pakai_target False, maks_umur_bar 48

=== H-013-AH terdaftar di hipotesis/H-013-AH.json (sidik 4ada4587abed, 9 kombinasi) ===
  [10/437] 1000SATSUSDT: 86 trade, 1s
  [20/437] ACXUSDT: 40 trade, 4s
  [30/437] AKROUSDT: 37 trade, 5s
  [40/437] ANTUSDT: 79 trade, 7s
  [50/437] ASRUSDT: 13 trade, 9s
  [60/437] AVAXUSDT: 244 trade, 11s
  [70/437] BANANAUSDT: 50 trade, 12s
  [80/437] BICOUSDT: 84 trade, 15s
  [90/437] BRETTUSDT: 64 trade, 17s
  [100/437] C98USDT: 205 trade, 18s
  [110/437] CHRUSDT: 203 trade, 20s
  [120/437] CTSIUSDT: 176 trade, 22s
  [130/437] DFUSDT: 22 trade, 24s
  [140/437] DUSDT: 28 trade, 26s
  [150/437] EOSUSDT: 185 trade, 28s
  [160/437] FIDAUSDT: 52 trade, 30s
  [170/437] FUSDT: 16 trade, 32s
  [180/437] GPSUSDT: 33 trade, 33s
  [190/437] HFTUSDT: 130 trade, 35s
  [200/437] HUSDT: 24 trade, 36s
  [210/437] INJUSDT: 172 trade, 38s
  [220/437] JTOUSDT: 98 trade, 40s
  [230/437] KSMUSDT: 218 trade, 42s
  [240/437] LRCUSDT: 187 trade, 44s
  [250/437] MATICUSDT: 151 trade, 47s
  [260/437] MKRUSDT: 213 trade, 48s
  [270/437] MYROUSDT: 47 trade, 49s
  [280/437] NOTUSDT: 56 trade, 51s
  [290/437] ONTUSDT: 265 trade, 53s
  [300/437] PERPUSDT: 86 trade, 55s
  [310/437] PORTALUSDT: 72 trade, 56s
  [320/437] RAYSOLUSDT: 42 trade, 57s
  [330/437] RNDRUSDT: 30 trade, 59s
  [340/437] SANDUSDT: 253 trade, 61s
  [350/437] SKYAIUSDT: 23 trade, 63s
  [360/437] SQDUSDT: 25 trade, 64s
  [370/437] SUNUSDT: 69 trade, 66s
  [380/437] TACUSDT: 22 trade, 68s
  [390/437] TRBUSDT: 246 trade, 69s
  [400/437] UNIUSDT: 210 trade, 71s
  [410/437] VIRTUALUSDT: 42 trade, 73s
  [420/437] XAIUSDT: 95 trade, 74s
  [430/437] ZECUSDT: 257 trade, 77s
  [437/437] ZRXUSDT: 239 trade, 79s
{
  "jumlah_simbol": 437,
  "jumlah_jendela": 4082,
  "jendela_positif": 2060,
  "jumlah_trade_luar_sampel": 45378,
  "total_R": 2639.657688262473,
  "ekspektasi_R": 0.05817042814276683
}
alasan keluar: {'umur': 15588, 'stop': 27297, 'carry': 258, 'akhir_data': 2235}
entri ditolak pengaman biaya: 0 (pengaman 0.5R, lantai semesta 0.004)
bulan dengan perdagangan: 73
parameter terpilih: {'{"imbalan_R": 2.0, "lookback": 20}': 1392, '{"imbalan_R": 2.0, "lookback": 100}': 1617, '{"imbalan_R": 2.0, "lookback": 55}': 1073}
konsentrasi: 270 untung / 167 rugi dari 437 simbol; drop-1 0.05658R (retensi 0.9726), drop-22 0.03461R, median simbol +0.04659R, porsi bruto teratas 0.0202 (ENJUSDT), setara 137.5 simbol
funding ekor: porsi ekor maks 0.0110 (rerata 0.0027 atas 10 terburuk), funding maks 0.7422R, 271 dari 45378 trade di atas pengaman (0.00597); gagal: funding_maks_R, porsi_trade_di_atas_pengaman
sebaran: std 1.92789R, galat baku 0.009050R, jarak ke ambang +0.008170R = +0.90 galat baku
entri acak: nyata 0.05846R, p 0.19933554817275748
sel AH: 4082 jendela, 45378 trade luar sampel (ambang ternilai 100)

{
  "ambang_sumbangan_sinyal_R": 0.02,
  "min_trade_per_sel": 100,
  "ekspektasi_R": {
    "SS": 0.06664781299919262,
    "SH": 0.037166633609032385,
    "AS": 0.01180570125176449,
    "AH": 0.05817042814276683
  },
  "trade": {
    "SS": 60018,
    "SH": 44614,
    "AS": 55927,
    "AH": 45378
  },
  "dapat_dinilai": true,
  "sebab": "",
  "sumbangan_sinyal_R": 0.05484211174742813,
  "sumbangan_geometri_R": 0.029481179390160234,
  "interaksi_R": 0.07584590628116258,
  "lulus": true
}
```
