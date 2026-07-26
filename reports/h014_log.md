# Log H-014

Run: `30221967019`
Commit: `52c64ac576e81883cd516316437edfff1d596ac4`
Kode keluar penggabung: `0`

Kode 0 = DITOLAK, dan itu HASIL (aturan 48), bukan kegagalan run.
Kode 4 = TIDAK DAPAT DINILAI. Tidak ada kode untuk LULUS sebab
tidak ada cabangnya: H-014 dipra-registrasi MUSTAHIL LULUS.


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
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.7/12.7 MB 281.6 MB/s  0:00:00
Downloading pyarrow-17.0.0-cp312-cp312-manylinux_2_28_x86_64.whl (39.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 39.9/39.9 MB 224.7 MB/s  0:00:00
Downloading PyYAML-6.0.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (767 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 767.5/767.5 kB 160.8 MB/s  0:00:00
Downloading pytest-9.1.1-py3-none-any.whl (386 kB)
Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)
Downloading numpy-2.5.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.7/16.7 MB 253.0 MB/s  0:00:00
Downloading packaging-26.2-py3-none-any.whl (100 kB)
Downloading pygments-2.20.0-py3-none-any.whl (1.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 232.0 MB/s  0:00:00
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
........................................................................ [  8%]
........................................................................ [ 16%]
........................................................................ [ 25%]
........................................................................ [ 33%]
........................................................................ [ 42%]
........................................................................ [ 50%]
........................................................................ [ 58%]
........................................................................ [ 67%]
........................................................................ [ 75%]
........................................................................ [ 84%]
........................................................................ [ 92%]
...............................................................          [100%]
855 passed in 2.98s
```

## logs/preflight.log

```
1. satu medan berbeda ['pakai_target'], umur setara 48 di kedua sel: OK
   sel SSp -> reports/backtest_h014_ssp_target_umur48.json
   sel SHp -> reports/backtest_h014_shp_tanpa_target_umur48.json
2. nama laporan H-014 tidak menimpa laporan yang dikomit: OK
3. besaran DAN p keduanya lolos tetap bukan kelulusan (TIDAK DAPAT DINILAI): OK
4. ambang BARU dinyatakan sebagai baru, bukan dikutip: OK
5. larangan membandingkan ke +0,029481R ikut tercetak: OK
6. pengaman dipasang dasar_riset, geometri TIDAK dilombakan: OK
7. hipotesis H-014-SSp dan H-014-SHp berdiri sendiri: OK
8. semesta dan akhir sejati 4h ada: OK

pagar pra-terbang H-014: LULUS
KONSEKUENSI KONSTRUKSI (bukan temuan): berkas md tiap sel akan
mencetak LULUS atau DITOLAK milik pra-registrasi PER SEL runner.
Putusan H-014 hanya lahir dari gabung_h014, dan ia MUSTAHIL LULUS.
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
H-014: dua sel ('SSp', 'SHp'), satu medan berbeda: ['pakai_target']
umur pegangan DISETARAKAN 48 bar di KEDUA sel; H-013 memakai 42 lawan 48 dan karena itu +0,029481R mencampur dua medan (cacat kelas keempat belas)
AMBANG: Ambang H-014 adalah ambang BARU yang dibekukan 2026-07-27, bukan kutipan ADR-015 pasal 4.4. Pasal itu membekukan ambang untuk kaki SINYAL (SS-AS, p atas permutasi sinyal); untuk kaki GEOMETRI, ADR-015 tidak pernah membekukan ambang, definisi p, maupun nol. Angka 0,020R dipinjam DENGAN SADAR dari pasal 4.4 supaya tidak ada ambang yang dipilih agar mudah dilewati.
PUTUSAN YANG MUNGKIN: ('DITOLAK', 'TIDAK DAPAT DINILAI')
PEMBATAS: H-014 MUSTAHIL LULUS, dan itu dipra-registrasi sebelum angkanya ada: putusannya hanya DITOLAK atau TIDAK DAPAT DINILAI. Signifikansinya diadjudikasi lux.analisis.berpasangan pada satuan BULAN kalender UTC, dan modul itu menyatakan sendiri bahwa p-nya mengukur ketidakpastian penarikan bulan, BUKAN sebaran permutasi sinyal; ia sah untuk MENJATUHKAN dan tidak sah untuk MENEGAKKAN. Berkas md tiap sel akan tetap mencetak LULUS atau DITOLAK milik pra-registrasi PER SEL dari runner; itu BUKAN putusan H-014. SS' dan SH' di sini BUKAN sel SS dan SH run 30214203863: kedua sel di sana berbeda pada DUA medan (target dan umur 42 lawan 48), sehingga +0,029481R tidak boleh dipakai sebagai pembanding maupun sebagai 'versi sebelum perbaikan'.
bar dibutuhkan satu jendela: 1862
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
  DIBUANG USDCUSDT: median_stop_frac 3.799992e-04, median jarak stop 3.800e-04 di bawah lantai 0.004

--- sel SSp: pakai_target True, maks_umur_bar 48 ---

=== H-014-SSp terdaftar di hipotesis/H-014-SSp.json (sidik 197c10e3f0d2, 3 kombinasi) ===
  [10/437] 1000SATSUSDT: 157 trade, 1s
  [20/437] ACXUSDT: 70 trade, 2s
  [30/437] AKROUSDT: 41 trade, 2s
  [40/437] ANTUSDT: 102 trade, 3s
  [50/437] ASRUSDT: 29 trade, 4s
  [60/437] AVAXUSDT: 330 trade, 5s
  [70/437] BANANAUSDT: 87 trade, 5s
  [80/437] BICOUSDT: 159 trade, 6s
  [90/437] BRETTUSDT: 89 trade, 7s
  [100/437] C98USDT: 263 trade, 8s
  [110/437] CHRUSDT: 284 trade, 8s
  [120/437] CTSIUSDT: 227 trade, 9s
  [130/437] DFUSDT: 44 trade, 10s
  [140/437] DUSDT: 44 trade, 11s
  [150/437] EOSUSDT: 288 trade, 12s
  [160/437] FIDAUSDT: 71 trade, 12s
  [170/437] FUSDT: 29 trade, 13s
  [180/437] GPSUSDT: 40 trade, 14s
  [190/437] HFTUSDT: 194 trade, 15s
  [200/437] HUSDT: 24 trade, 15s
  [210/437] INJUSDT: 190 trade, 16s
  [220/437] JTOUSDT: 135 trade, 17s
  [230/437] KSMUSDT: 271 trade, 17s
  [240/437] LRCUSDT: 263 trade, 18s
  [250/437] MATICUSDT: 185 trade, 19s
  [260/437] MKRUSDT: 268 trade, 20s
  [270/437] MYROUSDT: 38 trade, 20s
  [280/437] NOTUSDT: 100 trade, 21s
  [290/437] ONTUSDT: 331 trade, 22s
  [300/437] PERPUSDT: 115 trade, 23s
  [310/437] PORTALUSDT: 115 trade, 23s
  [320/437] RAYSOLUSDT: 46 trade, 24s
  [330/437] RNDRUSDT: 42 trade, 24s
  [340/437] SANDUSDT: 288 trade, 25s
  [350/437] SKYAIUSDT: 23 trade, 26s
  [360/437] SQDUSDT: 38 trade, 26s
  [370/437] SUNUSDT: 93 trade, 27s
  [380/437] TACUSDT: 45 trade, 28s
  [390/437] TRBUSDT: 266 trade, 29s
  [400/437] UNIUSDT: 283 trade, 29s
  [410/437] VIRTUALUSDT: 45 trade, 30s
  [420/437] XAIUSDT: 106 trade, 31s
  [430/437] ZECUSDT: 404 trade, 32s
  [437/437] ZRXUSDT: 304 trade, 33s
{
  "jumlah_simbol": 437,
  "jumlah_jendela": 4082,
  "jendela_positif": 2229,
  "jumlah_trade_luar_sampel": 59324,
  "total_R": 3989.659744110752,
  "ekspektasi_R": 0.06725203533326735
}
alasan keluar: {'target': 18667, 'stop': 33748, 'umur': 5174, 'akhir_data': 1735}
entri ditolak pengaman biaya: 0 (pengaman 0.5R, lantai semesta 0.004)
bulan dengan perdagangan: 73
parameter terpilih: {'{"imbalan_R": 2.0, "lookback": 55}': 836, '{"imbalan_R": 2.0, "lookback": 20}': 1711, '{"imbalan_R": 2.0, "lookback": 100}': 1535}
konsentrasi: 309 untung / 128 rugi dari 437 simbol; drop-1 0.06639R (retensi 0.9872), drop-22 0.05419R, median simbol +0.06789R, porsi bruto teratas 0.0139 (SANDUSDT), setara 181.1 simbol
funding ekor: porsi ekor maks 0.0273 (rerata 0.0027 atas 10 terburuk), funding maks 0.8285R, 82 dari 59324 trade di atas pengaman (0.00138); gagal: funding_maks_R
sebaran: std 1.37827R, galat baku 0.005659R, jarak ke ambang +0.017252R = +3.05 galat baku
entri acak: nyata 0.07085R, p 0.016611295681063124
sel SSp: ekspektasi 0.06725203533326735, 59324 trade, 73 bulan, gerbang gagal ['invarian_risiko', 'checksum', 'funding_ekor'], 56.9 s

--- sel SHp: pakai_target False, maks_umur_bar 48 ---

=== H-014-SHp terdaftar di hipotesis/H-014-SHp.json (sidik 5721a88e59eb, 3 kombinasi) ===
  [10/437] 1000SATSUSDT: 106 trade, 1s
  [20/437] ACXUSDT: 46 trade, 1s
  [30/437] AKROUSDT: 41 trade, 2s
  [40/437] ANTUSDT: 74 trade, 3s
  [50/437] ASRUSDT: 23 trade, 3s
  [60/437] AVAXUSDT: 228 trade, 4s
  [70/437] BANANAUSDT: 56 trade, 5s
  [80/437] BICOUSDT: 114 trade, 6s
  [90/437] BRETTUSDT: 67 trade, 6s
  [100/437] C98USDT: 205 trade, 7s
  [110/437] CHRUSDT: 225 trade, 8s
  [120/437] CTSIUSDT: 180 trade, 9s
  [130/437] DFUSDT: 32 trade, 9s
  [140/437] DUSDT: 35 trade, 10s
  [150/437] EOSUSDT: 221 trade, 11s
  [160/437] FIDAUSDT: 38 trade, 11s
  [170/437] FUSDT: 23 trade, 12s
  [180/437] GPSUSDT: 31 trade, 13s
  [190/437] HFTUSDT: 144 trade, 13s
  [200/437] HUSDT: 20 trade, 14s
  [210/437] INJUSDT: 146 trade, 14s
  [220/437] JTOUSDT: 98 trade, 15s
  [230/437] KSMUSDT: 208 trade, 16s
  [240/437] LRCUSDT: 209 trade, 17s
  [250/437] MATICUSDT: 131 trade, 18s
  [260/437] MKRUSDT: 206 trade, 18s
  [270/437] MYROUSDT: 48 trade, 19s
  [280/437] NOTUSDT: 63 trade, 19s
  [290/437] ONTUSDT: 277 trade, 20s
  [300/437] PERPUSDT: 84 trade, 21s
  [310/437] PORTALUSDT: 81 trade, 21s
  [320/437] RAYSOLUSDT: 28 trade, 22s
  [330/437] RNDRUSDT: 41 trade, 22s
  [340/437] SANDUSDT: 192 trade, 23s
  [350/437] SKYAIUSDT: 22 trade, 24s
  [360/437] SQDUSDT: 26 trade, 24s
  [370/437] SUNUSDT: 60 trade, 25s
  [380/437] TACUSDT: 20 trade, 26s
  [390/437] TRBUSDT: 264 trade, 26s
  [400/437] UNIUSDT: 222 trade, 27s
  [410/437] VIRTUALUSDT: 28 trade, 27s
  [420/437] XAIUSDT: 84 trade, 28s
  [430/437] ZECUSDT: 241 trade, 29s
  [437/437] ZRXUSDT: 250 trade, 30s
{
  "jumlah_simbol": 437,
  "jumlah_jendela": 4082,
  "jendela_positif": 1982,
  "jumlah_trade_luar_sampel": 44538,
  "total_R": 1763.6004466576758,
  "ekspektasi_R": 0.03959765698185091
}
alasan keluar: {'umur': 14426, 'stop': 28013, 'akhir_data': 2099}
entri ditolak pengaman biaya: 0 (pengaman 0.5R, lantai semesta 0.004)
bulan dengan perdagangan: 73
parameter terpilih: {'{"imbalan_R": 2.0, "lookback": 55}': 1073, '{"imbalan_R": 2.0, "lookback": 20}': 1995, '{"imbalan_R": 2.0, "lookback": 100}': 1014}
konsentrasi: 234 untung / 203 rugi dari 437 simbol; drop-1 0.03583R (retensi 0.9047), drop-22 0.01225R, median simbol +0.02710R, porsi bruto teratas 0.0431 (VELVETUSDT), setara 111.6 simbol
funding ekor: porsi ekor maks 0.0273 (rerata 0.0027 atas 10 terburuk), funding maks 2.9000R, 307 dari 44538 trade di atas pengaman (0.00689); gagal: funding_maks_R, porsi_trade_di_atas_pengaman
sebaran: std 2.20818R, galat baku 0.010463R, jarak ke ambang -0.010402R = -0.99 galat baku
entri acak: nyata 0.06363R, p 0.21926910299003322
sel SHp: ekspektasi 0.03959765698185091, 44538 trade, 73 bulan, gerbang gagal ['entri_acak', 'invarian_risiko', 'checksum', 'funding_ekor'], 52.6 s

manifes ditulis: reports/h014_run.json
PUTUSAN H-014 BELUM ADA. Ia lahir dari python -m lux.backtest.gabung_h014, dan berkas md tiap sel yang mencetak LULUS atau DITOLAK hanya menyatakan pra-registrasi PER SEL milik runner.
```

## logs/gabung.log

```
{
  "hipotesis": "H-014",
  "putusan": "DITOLAK",
  "alasan": [
    "rerata selisih bulanan -0.027715128544164157 < 0.02R",
    "p uji tanda bulanan 0.37596240375962403 > 0.05"
  ],
  "besaran_rerata_bulanan_R": -0.027715128544164157,
  "besaran_agregat_R": 0.027654378351416438,
  "catatan_besaran": "Dua besaran dilaporkan sebab keduanya tidak identik (aturan 49). Pembanding terhadap rerata sebaran nol TIDAK ADA di uji ini: nol permutasi geometri belum dirancang.",
  "p": 0.37596240375962403,
  "ambang_besaran_R": 0.02,
  "ambang_p": 0.05,
  "min_trade_sel": 100,
  "trade_a": 59324,
  "trade_b": 44538,
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
    "rerata_selisih": -0.027715128544164157,
    "rerata_berbobot": -0.012499029724652699,
    "selisih_agregat": 0.027654378351416438,
    "median_selisih": 0.03495217650445759,
    "fraksi_positif": 0.5616438356164384,
    "trade_a": 59324.0,
    "trade_b": 44538.0,
    "melewati_ambang_besaran": false,
    "uji_tanda": {
      "n": 73,
      "dapat_dinilai": true,
      "sebab": "",
      "rerata": -0.027715128544164157,
      "p": 0.37596240375962403,
      "m_lebih_ekstrem": 3759,
      "ulangan": 10000,
      "seed": 20260727,
      "pembatas": "p di sini mengukur ketidakpastian PENARIKAN SIMBOL/BULAN, bukan sebaran permutasi sinyal. Ia TIDAK memenuhi ADR-015 pasal 4.4 yang menuntut p atas minimal 300 permutasi sinyal. Angka ini sah dipakai untuk MENJATUHKAN klaim selisih antar sel, dan tidak sah dipakai untuk MENEGAKKANNYA."
    },
    "bootstrap": {
      "n": 73,
      "dapat_dinilai": true,
      "sebab": "",
      "rerata": -0.027715128544164157,
      "bawah": -0.09067851377334449,
      "atas": 0.029103950604927244,
      "alpha": 0.05,
      "ulangan": 10000,
      "seed": 20260728,
      "pembatas": "p di sini mengukur ketidakpastian PENARIKAN SIMBOL/BULAN, bukan sebaran permutasi sinyal. Ia TIDAK memenuhi ADR-015 pasal 4.4 yang menuntut p atas minimal 300 permutasi sinyal. Angka ini sah dipakai untuk MENJATUHKAN klaim selisih antar sel, dan tidak sah dipakai untuk MENEGAKKANNYA."
    }
  },
  "putusan_mungkin": [
    "DITOLAK",
    "TIDAK DAPAT DINILAI"
  ],
  "memenuhi_adr015": false,
  "pembatas": "Putusan H-014 hanya dapat DITOLAK atau TIDAK DAPAT DINILAI; tidak ada cabang LULUS di modul ini, dan pengujian menuntut ketiadaannya (ADR-034). SS' dan SH' BUKAN sel SS dan SH run 30214203863: kedua sel di sana berbeda pada DUA medan sekaligus (ada-tidaknya target DAN umur 42 lawan 48), sehingga +0,029481R tidak boleh dipakai sebagai pembanding maupun sebagai 'versi sebelum perbaikan'. Berkas md tiap sel mencetak LULUS atau DITOLAK milik pra-registrasi PER SEL dari runner; itu bukan putusan H-014.",
  "pembatas_berpasangan": "p di sini mengukur ketidakpastian PENARIKAN SIMBOL/BULAN, bukan sebaran permutasi sinyal. Ia TIDAK memenuhi ADR-015 pasal 4.4 yang menuntut p atas minimal 300 permutasi sinyal. Angka ini sah dipakai untuk MENJATUHKAN klaim selisih antar sel, dan tidak sah dipakai untuk MENEGAKKANNYA."
}

PUTUSAN H-014: DITOLAK
  - rerata selisih bulanan -0.027715128544164157 < 0.02R
  - p uji tanda bulanan 0.37596240375962403 > 0.05
```
