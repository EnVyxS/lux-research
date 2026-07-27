# Log H-015

Run: `30249117960`
Commit: `017e0ac37fe15059b520bacb9c7df0d4f1edccd3`
Kode keluar penggabung: `4`

Kode 0 = DITOLAK ATAU LULUS. Keduanya adjudikasi yang BERHASIL
diperoleh (aturan 48), dan tidak boleh menyamar sebagai run gagal.
Kode 4 = TIDAK DAPAT DINILAI. Kode 2 = pagar pra-terbang.

LULUS di sini berarti lulus kriteria pra-registrasi ADR-037 5,
dan BUKAN kelulusan ADR-015 4.4: p-nya mengukur penarikan bulan
kalender UTC, bukan permutasi sinyal.


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
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.7/12.7 MB 80.1 MB/s  0:00:00
Downloading pyarrow-17.0.0-cp312-cp312-manylinux_2_28_x86_64.whl (39.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 39.9/39.9 MB 254.2 MB/s  0:00:00
Downloading PyYAML-6.0.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (767 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 767.5/767.5 kB 132.9 MB/s  0:00:00
Downloading pytest-9.1.1-py3-none-any.whl (386 kB)
Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)
Downloading numpy-2.5.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.7/16.7 MB 333.1 MB/s  0:00:00
Downloading packaging-26.2-py3-none-any.whl (100 kB)
Downloading pygments-2.20.0-py3-none-any.whl (1.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 204.4 MB/s  0:00:00
Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
Downloading pytz-2026.3.post1-py2.py3-none-any.whl (508 kB)
Downloading six-1.17.0-py2.py3-none-any.whl (11 kB)
Downloading tzdata-2026.3-py2.py3-none-any.whl (348 kB)
Installing collected packages: pytz, tzdata, six, pyyaml, pygments, pluggy, packaging, numpy, iniconfig, python-dateutil, pytest, pyarrow, pandas

Successfully installed iniconfig-2.3.0 numpy-2.5.1 packaging-26.2 pandas-2.2.3 pluggy-1.6.0 pyarrow-17.0.0 pygments-2.20.0 pytest-9.1.1 python-dateutil-2.9.0.post0 pytz-2026.3.post1 pyyaml-6.0.2 six-1.17.0 tzdata-2026.3
numpy 2.5.1
```

## logs/uji.log

```
........................................................................ [  7%]
........................................................................ [ 14%]
........................................................................ [ 22%]
........................................................................ [ 29%]
........................................................................ [ 36%]
........................................................................ [ 44%]
........................................................................ [ 51%]
........................................................................ [ 58%]
........................................................................ [ 66%]
........................................................................ [ 73%]
........................................................................ [ 81%]
........................................................................ [ 88%]
........................................................................ [ 95%]
.........................................                                [100%]
977 passed in 3.49s
```

## logs/preflight.log

```
1. cabang LULUS tercapai atas masukan sintetis (0.010989): OK
2. cabang LULUS tetap memancarkan memenuhi_adr015 False: OK
3. larangan F - K dan +0,029481R ikut tercetak: OK
4. lookahead dimaklumi di A dan TIDAK di F: OK
5. ambang H-015 tidak bergeser dari ADR-037: OK
   sel K -> reports/backtest_h015_k_kontrol.json
   sel F -> reports/backtest_h015_f_saringan.json
   sel A -> reports/backtest_h015_a_acak.json
6. nama laporan H-015 tidak menimpa laporan yang dikomit: OK
7. pengaman carry MENYALA di ketiga sel (bukan seperti H-014): OK
8. ketiga sel berkonfig identik; hanya sinyalnya berbeda: OK
9. semesta dan akhir sejati 4h ada: OK

pagar pra-terbang H-015: LULUS
KONSEKUENSI KONSTRUKSI (bukan temuan): lookahead DIJAMIN gagal di
sel A, dan berkas md tiap sel akan mencetak LULUS atau DITOLAK
milik pra-registrasi PER SEL runner. Putusan H-015 hanya lahir
dari gabung_h015, dan LULUS di sana BUKAN kelulusan ADR-015 4.4.
```

## logs/lantai.log

```
lantai=0.004
```

## logs/unduh.log

```
16
157M	aset
```

## logs/jalan.log

```
H-015 tiga sel: ['K', 'F', 'A']
  [K] konfig H-015-K: 15 medan tercatat utuh
  [K] selisih terhadap H-013 SS: maks_umur_bar 48 lawan 42
  [F] konfig H-015-F: 15 medan tercatat utuh
  [F] selisih terhadap H-013 SS: maks_umur_bar 48 lawan 42
  [A] konfig H-015-A: 15 medan tercatat utuh
  [A] selisih terhadap H-013 SS: maks_umur_bar 48 lawan 42
pengaman dituntut: {'maks_carry_realisasi_R': 0.25, 'maks_carry_R': 0.25}
saringan: ambang rate 0.0001, minimum penagihan 30, jendela 30 hari, seed acak 20260727 (semuanya beku, ADR-037)
jendela 4h: latih 1080, uji 540, embargo 42, pemanasan 200 bar TIDAK dikonversi; satu jendela menuntut 1862 bar
KONSEKUENSI KONSTRUKSI (bukan temuan): lookahead DIJAMIN gagal pada sel A. Pada sel F ia TIDAK dimaklumi — saringannya hanya membaca masa lalu, jadi bila ia jatuh di F, yang jatuh adalah kodenya.
MENGIKAT hanya F − A. Selisih F − K dicetak dan HARAM dipakai sebagai dasar kelulusan.
  ramalan R-L1: sel F menolak long lebih dari 3x lebih sering daripada short; DIJAMIN konstruksi, jadi ketepatannya tidak bernilai apa-apa
  ramalan R-L2: H-015 DITOLAK: rerata bulanan F − A kurang dari +0,020R
  ramalan R-L3: nilai mutlak F − A lebih kecil daripada nilai mutlak F − K
  ramalan R-L4: cacah pytest paling sedikit 884
  ramalan R-L5: keluar `carry` bukan nol pada ketiga sel; nol berarti sidik jari cacat 18 dan run dibatalkan meski audit konfig hijau
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
manifest aset reports/manifest_aset_4h.json (12 berkas interval 4h)
checksum: tidak dapat dinilai: manifest baru ditulis pada run ini
lantai median stop_frac 0.004: 437 layak, 1 dibuang dari 438 simbol dimuat
  DIBUANG USDCUSDT: median_stop_frac 3.797195e-04, median jarak stop 3.797e-04 di bawah lantai 0.004

### SEL K: h015_k_kontrol

=== H-015-K terdaftar di hipotesis/H-015-K.json (sidik 61dc0acf646d, 9 kombinasi) ===
  [10/437] 1000SATSUSDT: 157 trade, 1s
  [20/437] ACXUSDT: 70 trade, 3s
  [30/437] AKROUSDT: 41 trade, 4s
  [40/437] ANTUSDT: 102 trade, 6s
  [50/437] ASRUSDT: 29 trade, 8s
  [60/437] AVAXUSDT: 330 trade, 10s
  [70/437] BANANAUSDT: 87 trade, 11s
  [80/437] BICOUSDT: 159 trade, 13s
  [90/437] BRETTUSDT: 89 trade, 14s
  [100/437] C98USDT: 264 trade, 16s
  [110/437] CHRUSDT: 284 trade, 17s
  [120/437] CTSIUSDT: 227 trade, 19s
  [130/437] DFUSDT: 44 trade, 21s
  [140/437] DUSDT: 44 trade, 22s
  [150/437] EOSUSDT: 288 trade, 25s
  [160/437] FIDAUSDT: 71 trade, 26s
  [170/437] FUSDT: 29 trade, 28s
  [180/437] GPSUSDT: 40 trade, 29s
  [190/437] HFTUSDT: 194 trade, 31s
  [200/437] HUSDT: 24 trade, 32s
  [210/437] INJUSDT: 190 trade, 33s
  [220/437] JTOUSDT: 135 trade, 35s
  [230/437] KSMUSDT: 271 trade, 37s
  [240/437] LRCUSDT: 263 trade, 39s
  [250/437] MATICUSDT: 185 trade, 41s
  [260/437] MKRUSDT: 268 trade, 42s
  [270/437] MYROUSDT: 38 trade, 43s
  [280/437] NOTUSDT: 100 trade, 45s
  [290/437] ONTUSDT: 331 trade, 47s
  [300/437] PERPUSDT: 115 trade, 48s
  [310/437] PORTALUSDT: 115 trade, 49s
  [320/437] RAYSOLUSDT: 46 trade, 51s
  [330/437] RNDRUSDT: 42 trade, 52s
  [340/437] SANDUSDT: 288 trade, 54s
  [350/437] SKYAIUSDT: 23 trade, 56s
  [360/437] SQDUSDT: 38 trade, 57s
  [370/437] SUNUSDT: 93 trade, 59s
  [380/437] TACUSDT: 45 trade, 60s
  [390/437] TRBUSDT: 266 trade, 62s
  [400/437] UNIUSDT: 283 trade, 63s
  [410/437] VIRTUALUSDT: 45 trade, 64s
  [420/437] XAIUSDT: 106 trade, 66s
  [430/437] ZECUSDT: 404 trade, 68s
  [437/437] ZRXUSDT: 304 trade, 70s
{
  "jumlah_simbol": 437,
  "jumlah_jendela": 4085,
  "jendela_positif": 2228,
  "jumlah_trade_luar_sampel": 59306,
  "total_R": 4016.8737053508016,
  "ekspektasi_R": 0.06773132069859376
}
alasan keluar: {'target': 18643, 'stop': 33703, 'carry': 82, 'umur': 5149, 'akhir_data': 1729}
entri ditolak pengaman biaya: 0 (pengaman 0.5R, lantai semesta 0.004)
bulan dengan perdagangan: 73
parameter terpilih: {'{"imbalan_R": 2.0, "lookback": 55}': 836, '{"imbalan_R": 2.0, "lookback": 20}': 1707, '{"imbalan_R": 2.0, "lookback": 100}': 1542}
konsentrasi: 308 untung / 129 rugi dari 437 simbol; drop-1 0.06687R (retensi 0.9873), drop-22 0.05488R, median simbol +0.06711R, porsi bruto teratas 0.0139 (SANDUSDT), setara 181.0 simbol
funding ekor: porsi ekor maks 0.0273 (rerata 0.0027 atas 10 terburuk), funding maks 0.4243R, 84 dari 59306 trade di atas pengaman (0.00142)
sebaran: std 1.37780R, galat baku 0.005658R, jarak ke ambang +0.017731R = +3.13 galat baku
entri acak: nyata 0.07311R, p 0.009966777408637873
sel K: 4085 jendela, 59306 trade luar sampel (ambang ternilai 100); alasan keluar {'target': 18643, 'stop': 33703, 'carry': 82, 'umur': 5149, 'akhir_data': 1729}

### SEL F: h015_f_saringan

=== H-015-F terdaftar di hipotesis/H-015-F.json (sidik f4b823362d12, 9 kombinasi) ===
  [10/437] 1000SATSUSDT: 144 trade, 1s
  [20/437] ACXUSDT: 69 trade, 4s
  [30/437] AKROUSDT: 33 trade, 5s
  [40/437] ANTUSDT: 95 trade, 7s
  [50/437] ASRUSDT: 26 trade, 9s
  [60/437] AVAXUSDT: 308 trade, 10s
  [70/437] BANANAUSDT: 73 trade, 12s
  [80/437] BICOUSDT: 159 trade, 14s
  [90/437] BRETTUSDT: 89 trade, 15s
  [100/437] C98USDT: 241 trade, 17s
  [110/437] CHRUSDT: 251 trade, 19s
  [120/437] CTSIUSDT: 180 trade, 21s
  [130/437] DFUSDT: 44 trade, 23s
  [140/437] DUSDT: 31 trade, 24s
  [150/437] EOSUSDT: 241 trade, 27s
  [160/437] FIDAUSDT: 59 trade, 28s
  [170/437] FUSDT: 26 trade, 30s
  [180/437] GPSUSDT: 25 trade, 31s
  [190/437] HFTUSDT: 166 trade, 33s
  [200/437] HUSDT: 31 trade, 34s
  [210/437] INJUSDT: 158 trade, 36s
  [220/437] JTOUSDT: 131 trade, 38s
  [230/437] KSMUSDT: 260 trade, 39s
  [240/437] LRCUSDT: 241 trade, 42s
  [250/437] MATICUSDT: 159 trade, 44s
  [260/437] MKRUSDT: 232 trade, 45s
  [270/437] MYROUSDT: 44 trade, 46s
  [280/437] NOTUSDT: 99 trade, 48s
  [290/437] ONTUSDT: 260 trade, 50s
  [300/437] PERPUSDT: 112 trade, 51s
  [310/437] PORTALUSDT: 114 trade, 52s
  [320/437] RAYSOLUSDT: 46 trade, 54s
  [330/437] RNDRUSDT: 40 trade, 55s
  [340/437] SANDUSDT: 270 trade, 58s
  [350/437] SKYAIUSDT: 2 trade, 59s
  [360/437] SQDUSDT: 20 trade, 60s
  [370/437] SUNUSDT: 84 trade, 62s
  [380/437] TACUSDT: 19 trade, 64s
  [390/437] TRBUSDT: 229 trade, 65s
  [400/437] UNIUSDT: 279 trade, 67s
  [410/437] VIRTUALUSDT: 44 trade, 68s
  [420/437] XAIUSDT: 92 trade, 70s
  [430/437] ZECUSDT: 335 trade, 73s
  [437/437] ZRXUSDT: 279 trade, 74s
{
  "jumlah_simbol": 437,
  "jumlah_jendela": 4083,
  "jendela_positif": 2269,
  "jumlah_trade_luar_sampel": 53025,
  "total_R": 4306.42256865554,
  "ekspektasi_R": 0.08121494707506911
}
alasan keluar: {'target': 16706, 'stop': 29835, 'umur': 4881, 'akhir_data': 1576, 'carry': 27}
entri ditolak pengaman biaya: 0 (pengaman 0.5R, lantai semesta 0.004)
bulan dengan perdagangan: 73
parameter terpilih: {'{"imbalan_R": 2.0, "lookback": 55}': 909, '{"imbalan_R": 2.0, "lookback": 20}': 1958, '{"imbalan_R": 2.0, "lookback": 100}': 1216}
konsentrasi: 314 untung / 123 rugi dari 437 simbol; drop-1 0.08018R (retensi 0.9873), drop-22 0.06783R, median simbol +0.08248R, porsi bruto teratas 0.0155 (XLMUSDT), setara 189.6 simbol
funding ekor: porsi ekor maks 0.0273 (rerata 0.0028 atas 10 terburuk), funding maks 0.3531R, 27 dari 53025 trade di atas pengaman (0.00051)
sebaran: std 1.37651R, galat baku 0.005978R, jarak ke ambang +0.031215R = +5.22 galat baku
entri acak: nyata 0.08720R, p 0.009966777408637873
sel F: 4083 jendela, 53025 trade luar sampel (ambang ternilai 100); alasan keluar {'target': 16706, 'stop': 29835, 'umur': 4881, 'akhir_data': 1576, 'carry': 27}

### SEL A: h015_a_acak

=== H-015-A terdaftar di hipotesis/H-015-A.json (sidik 96fa54b7cca7, 9 kombinasi) ===
  [10/437] 1000SATSUSDT: 144 trade, 3s
  [20/437] ACXUSDT: 69 trade, 8s
  [30/437] AKROUSDT: 34 trade, 10s
  [40/437] ANTUSDT: 98 trade, 15s
  [50/437] ASRUSDT: 26 trade, 19s
  [60/437] AVAXUSDT: 299 trade, 23s
  [70/437] BANANAUSDT: 73 trade, 26s
  [80/437] BICOUSDT: 158 trade, 31s
  [90/437] BRETTUSDT: 89 trade, 35s
  [100/437] C98USDT: 240 trade, 38s
  [110/437] CHRUSDT: 267 trade, 42s
  [120/437] CTSIUSDT: 200 trade, 47s
  [130/437] DFUSDT: 44 trade, 50s
  [140/437] DUSDT: 32 trade, 53s
  [150/437] EOSUSDT: 248 trade, 59s
  [160/437] FIDAUSDT: 62 trade, 63s
  [170/437] FUSDT: 25 trade, 66s
  [180/437] GPSUSDT: 30 trade, 70s
  [190/437] HFTUSDT: 171 trade, 73s
  [200/437] HUSDT: 27 trade, 76s
  [210/437] INJUSDT: 149 trade, 79s
  [220/437] JTOUSDT: 128 trade, 83s
  [230/437] KSMUSDT: 274 trade, 87s
  [240/437] LRCUSDT: 243 trade, 92s
  [250/437] MATICUSDT: 170 trade, 96s
  [260/437] MKRUSDT: 249 trade, 99s
  [270/437] MYROUSDT: 45 trade, 101s
  [280/437] NOTUSDT: 99 trade, 105s
  [290/437] ONTUSDT: 253 trade, 110s
  [300/437] PERPUSDT: 115 trade, 113s
  [310/437] PORTALUSDT: 114 trade, 115s
  [320/437] RAYSOLUSDT: 46 trade, 118s
  [330/437] RNDRUSDT: 43 trade, 121s
  [340/437] SANDUSDT: 261 trade, 126s
  [350/437] SKYAIUSDT: 2 trade, 129s
  [360/437] SQDUSDT: 20 trade, 132s
  [370/437] SUNUSDT: 92 trade, 136s
  [380/437] TACUSDT: 19 trade, 139s
  [390/437] TRBUSDT: 233 trade, 142s
  [400/437] UNIUSDT: 286 trade, 146s
  [410/437] VIRTUALUSDT: 44 trade, 149s
  [420/437] XAIUSDT: 92 trade, 152s
  [430/437] ZECUSDT: 329 trade, 158s
  [437/437] ZRXUSDT: 301 trade, 162s
{
  "jumlah_simbol": 437,
  "jumlah_jendela": 4083,
  "jendela_positif": 2260,
  "jumlah_trade_luar_sampel": 53904,
  "total_R": 4260.191347525546,
  "ekspektasi_R": 0.07903293535777578
}
alasan keluar: {'target': 16956, 'stop': 30395, 'umur': 4937, 'akhir_data': 1590, 'carry': 26}
entri ditolak pengaman biaya: 0 (pengaman 0.5R, lantai semesta 0.004)
bulan dengan perdagangan: 73
parameter terpilih: {'{"imbalan_R": 2.0, "lookback": 55}': 923, '{"imbalan_R": 2.0, "lookback": 20}': 1937, '{"imbalan_R": 2.0, "lookback": 100}': 1223}
konsentrasi: 321 untung / 116 rugi dari 437 simbol; drop-1 0.07817R (retensi 0.9890), drop-22 0.06693R, median simbol +0.07840R, porsi bruto teratas 0.0132 (RUNEUSDT), setara 193.5 simbol
funding ekor: porsi ekor maks 0.0273 (rerata 0.0028 atas 10 terburuk), funding maks 0.3531R, 26 dari 53904 trade di atas pengaman (0.00048)
sebaran: std 1.37635R, galat baku 0.005928R, jarak ke ambang +0.029033R = +4.90 galat baku
entri acak: nyata 0.10723R, p 0.006644518272425249
sel A: 4083 jendela, 53904 trade luar sampel (ambang ternilai 100); alasan keluar {'target': 16956, 'stop': 30395, 'umur': 4937, 'akhir_data': 1590, 'carry': 26}

{
  "ambang_selisih_mengikat_R": 0.02,
  "min_trade_per_sel": 100,
  "ekspektasi_R": {
    "K": 0.06773132069859376,
    "F": 0.08121494707506911,
    "A": 0.07903293535777578
  },
  "trade": {
    "K": 59306,
    "F": 53025,
    "A": 53904
  },
  "dapat_dinilai": true,
  "sebab": "",
  "selisih_mengikat_F_A_R": 0.0021820117172933334,
  "selisih_TIDAK_mengikat_F_K_R": 0.01348362637647535,
  "lulus": false
}
```

## logs/gabung.log

```
{
  "hipotesis": "H-015",
  "putusan": "TIDAK DAPAT DINILAI",
  "alasan": [
    "gerbang gagal tanpa pemakluman: {'A': ['checksum', 'invarian_risiko'], 'F': ['checksum', 'invarian_risiko'], 'K': ['checksum', 'invarian_risiko']}. Gerbang ada supaya angkanya tidak dipercaya, jadi angkanya tidak dipakai untuk menjatuhkan maupun menegakkan apa pun"
  ],
  "besaran_rerata_bulanan_R": 0.008903082974700181,
  "besaran_agregat_R": 0.0021820117172933196,
  "catatan_besaran": "Dua besaran dilaporkan sebab keduanya tidak identik (aturan 49). Yang MENGIKAT adalah rerata bulanan, sebab satuan penarikan H-015 adalah bulan kalender UTC (ADR-028). H-014 mati dengan kedua angka ini berlawanan tanda, dan itu tercatat sebagai cacat kelas 16.",
  "p": 0.1872812718728127,
  "ambang_besaran_R": 0.02,
  "ambang_p": 0.05,
  "min_trade_sel": 100,
  "min_ulangan": 300,
  "ulangan_run": 300,
  "trade_F": 53025,
  "trade_A": 53904,
  "pengaman_mati": {},
  "gerbang_gagal_tak_dimaklumi": {
    "A": [
      "checksum",
      "invarian_risiko"
    ],
    "F": [
      "checksum",
      "invarian_risiko"
    ],
    "K": [
      "checksum",
      "invarian_risiko"
    ]
  },
  "gerbang_dimaklumi": {
    "A": [
      "lookahead"
    ]
  },
  "satuan_penarikan": "bulan",
  "per_bulan": {
    "kunci_id": "periode",
    "kunci_nilai": "ekspektasi_R",
    "n_pasangan": 73,
    "hanya_a": [],
    "hanya_b": [],
    "tanpa_nilai": [],
    "ambang_besaran": 0.02,
    "memenuhi_adr015": false,
    "sebab_adr015": "p di sini mengukur ketidakpastian PENARIKAN SIMBOL/BULAN, bukan sebaran permutasi sinyal. Ia TIDAK memenuhi ADR-015 pasal 4.4 yang menuntut p atas minimal 300 permutasi sinyal. Angka ini sah dipakai untuk MENJATUHKAN klaim selisih antar sel, dan tidak sah dipakai untuk MENEGAKKANNYA.",
    "pembatas": "p di sini mengukur ketidakpastian PENARIKAN SIMBOL/BULAN, bukan sebaran permutasi sinyal. Ia TIDAK memenuhi ADR-015 pasal 4.4 yang menuntut p atas minimal 300 permutasi sinyal. Angka ini sah dipakai untuk MENJATUHKAN klaim selisih antar sel, dan tidak sah dipakai untuk MENEGAKKANNYA.",
    "dapat_dinilai": true,
    "sebab": "",
    "rerata_selisih": 0.008903082974700181,
    "rerata_berbobot": 0.001667219936026623,
    "selisih_agregat": 0.0021820117172933196,
    "median_selisih": 0.002404502189742308,
    "fraksi_positif": 0.589041095890411,
    "trade_a": 53025.0,
    "trade_b": 53904.0,
    "melewati_ambang_besaran": false,
    "uji_tanda": {
      "n": 73,
      "dapat_dinilai": true,
      "sebab": "",
      "rerata": 0.008903082974700181,
      "p": 0.1872812718728127,
      "m_lebih_ekstrem": 1872,
      "ulangan": 10000,
      "seed": 20260727,
      "pembatas": "p di sini mengukur ketidakpastian PENARIKAN SIMBOL/BULAN, bukan sebaran permutasi sinyal. Ia TIDAK memenuhi ADR-015 pasal 4.4 yang menuntut p atas minimal 300 permutasi sinyal. Angka ini sah dipakai untuk MENJATUHKAN klaim selisih antar sel, dan tidak sah dipakai untuk MENEGAKKANNYA."
    },
    "bootstrap": {
      "n": 73,
      "dapat_dinilai": true,
      "sebab": "",
      "rerata": 0.008903082974700181,
      "bawah": -0.003112849756744765,
      "atas": 0.02188788728847709,
      "alpha": 0.05,
      "ulangan": 10000,
      "seed": 20260728,
      "pembatas": "p di sini mengukur ketidakpastian PENARIKAN SIMBOL/BULAN, bukan sebaran permutasi sinyal. Ia TIDAK memenuhi ADR-015 pasal 4.4 yang menuntut p atas minimal 300 permutasi sinyal. Angka ini sah dipakai untuk MENJATUHKAN klaim selisih antar sel, dan tidak sah dipakai untuk MENEGAKKANNYA."
    }
  },
  "selisih_TIDAK_mengikat_F_K": -0.01571883629037982,
  "catatan_F_K": "Selisih F - K TIDAK MENGIKAT dalam bentuk apa pun dan haram dipakai sebagai dasar kelulusan.",
  "putusan_mungkin": [
    "LULUS",
    "DITOLAK",
    "TIDAK DAPAT DINILAI"
  ],
  "memenuhi_adr015": false,
  "pembatas": "Putusan H-015 dapat LULUS, DITOLAK, atau TIDAK DAPAT DINILAI. LULUS di sini berarti LULUS KRITERIA PRA-REGISTRASI ADR-037 pasal 5, dan BUKAN kelulusan ADR-015 pasal 4.4: p yang dipakai berasal dari penarikan bulan kalender UTC (ADR-028), bukan dari sebaran permutasi sinyal, sehingga medan memenuhi_adr015 tetap False bahkan pada cabang LULUS. Yang mengikat hanya F - A. Selisih F - K ikut dicetak dan HARAM dipakai sebagai dasar kelulusan: funding positif pada 79,1% periode membuat saringan apa pun mengalahkan kontrol tanpa memuat setitik pun informasi. Angka +0,029481R milik H-014 bukan pembanding H-015 dalam bentuk apa pun.",
  "pembatas_berpasangan": "p di sini mengukur ketidakpastian PENARIKAN SIMBOL/BULAN, bukan sebaran permutasi sinyal. Ia TIDAK memenuhi ADR-015 pasal 4.4 yang menuntut p atas minimal 300 permutasi sinyal. Angka ini sah dipakai untuk MENJATUHKAN klaim selisih antar sel, dan tidak sah dipakai untuk MENEGAKKANNYA."
}

PUTUSAN H-015: TIDAK DAPAT DINILAI
  - gerbang gagal tanpa pemakluman: {'A': ['checksum', 'invarian_risiko'], 'F': ['checksum', 'invarian_risiko'], 'K': ['checksum', 'invarian_risiko']}. Gerbang ada supaya angkanya tidak dipercaya, jadi angkanya tidak dipakai untuk menjatuhkan maupun menegakkan apa pun
```
