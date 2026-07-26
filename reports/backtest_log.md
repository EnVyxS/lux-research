# Log run backtest H-011 (ADR-013)

Commit: `102c297ca837e6c8f6bc0cd3ebd159eb7dce73e0`
Run: `30194733599`

| Langkah | Hasil |
|---|---|
| pasang dependensi | `success` |
| pytest | `success` |
| impor | `success` |
| unduh aset | `success` |
| jalan | `success` |

## Pra-terbang

```
=== pasang dependensi ===
Python 3.12.13
Collecting pytest
  Using cached pytest-9.1.1-py3-none-any.whl.metadata (7.6 kB)
Collecting pandas==2.2.3 (from -r requirements.txt (line 1))
  Using cached pandas-2.2.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (89 kB)
Collecting pyarrow==17.0.0 (from -r requirements.txt (line 2))
  Using cached pyarrow-17.0.0-cp312-cp312-manylinux_2_28_x86_64.whl.metadata (3.3 kB)
Collecting pyyaml==6.0.2 (from -r requirements.txt (line 6))
  Using cached PyYAML-6.0.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.1 kB)
Collecting numpy>=1.26.0 (from pandas==2.2.3->-r requirements.txt (line 1))
  Using cached numpy-2.5.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (6.6 kB)
Collecting python-dateutil>=2.8.2 (from pandas==2.2.3->-r requirements.txt (line 1))
  Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl.metadata (8.4 kB)
Collecting pytz>=2020.1 (from pandas==2.2.3->-r requirements.txt (line 1))
  Using cached pytz-2026.3.post1-py2.py3-none-any.whl.metadata (22 kB)
Collecting tzdata>=2022.7 (from pandas==2.2.3->-r requirements.txt (line 1))
  Using cached tzdata-2026.3-py2.py3-none-any.whl.metadata (1.4 kB)
Collecting iniconfig>=1.0.1 (from pytest)
  Using cached iniconfig-2.3.0-py3-none-any.whl.metadata (2.5 kB)
Collecting packaging>=22 (from pytest)
  Using cached packaging-26.2-py3-none-any.whl.metadata (3.5 kB)
Collecting pluggy<2,>=1.5 (from pytest)
  Using cached pluggy-1.6.0-py3-none-any.whl.metadata (4.8 kB)
Collecting pygments>=2.7.2 (from pytest)
  Using cached pygments-2.20.0-py3-none-any.whl.metadata (2.5 kB)
Collecting six>=1.5 (from python-dateutil>=2.8.2->pandas==2.2.3->-r requirements.txt (line 1))
  Using cached six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
Using cached pandas-2.2.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (12.7 MB)
Using cached pyarrow-17.0.0-cp312-cp312-manylinux_2_28_x86_64.whl (39.9 MB)
Using cached PyYAML-6.0.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (767 kB)
Using cached pytest-9.1.1-py3-none-any.whl (386 kB)
Using cached pluggy-1.6.0-py3-none-any.whl (20 kB)
Using cached iniconfig-2.3.0-py3-none-any.whl (7.5 kB)
Using cached numpy-2.5.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.7 MB)
Using cached packaging-26.2-py3-none-any.whl (100 kB)
Using cached pygments-2.20.0-py3-none-any.whl (1.2 MB)
Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
Using cached pytz-2026.3.post1-py2.py3-none-any.whl (508 kB)
Using cached six-1.17.0-py2.py3-none-any.whl (11 kB)
Using cached tzdata-2026.3-py2.py3-none-any.whl (348 kB)
Installing collected packages: pytz, tzdata, six, pyyaml, pygments, pluggy, packaging, numpy, iniconfig, python-dateutil, pytest, pyarrow, pandas

Successfully installed iniconfig-2.3.0 numpy-2.5.1 packaging-26.2 pandas-2.2.3 pluggy-1.6.0 pyarrow-17.0.0 pygments-2.20.0 pytest-9.1.1 python-dateutil-2.9.0.post0 pytz-2026.3.post1 pyyaml-6.0.2 six-1.17.0 tzdata-2026.3
Package         Version
--------------- ------------
iniconfig       2.3.0
numpy           2.5.1
packaging       26.2
pandas          2.2.3
pip             26.1.2
pluggy          1.6.0
pyarrow         17.0.0
Pygments        2.20.0
pytest          9.1.1
python-dateutil 2.9.0.post0
pytz            2026.3.post1
PyYAML          6.0.2
six             1.17.0
tzdata          2026.3
=== pytest ===
........................................................................ [ 13%]
........................................................................ [ 26%]
........................................................................ [ 39%]
........................................................................ [ 53%]
........................................................................ [ 66%]
........................................................................ [ 79%]
........................................................................ [ 92%]
......................................                                   [100%]
542 passed in 1.80s
=== impor ===
impor pihak ketiga siap
run_wf siap ('_retry',)
runner bersama siap
jumlah gerbang: 11
  nama: ('forward_fill', 'buy_and_hold', 'entri_acak', 'lookahead', 'invarian_risiko', 'funding', 'overlap', 'checksum', 'survivorship', 'konsentrasi', 'funding_ekor')
gerbang kesepuluh dan kesebelas terdaftar: ya
bawaan pengaman mati: True
ADR-013 sebaran siap: 13 kunci, std ddof=1 1.290994 galat baku 0.645497
sebaran tersambung ke runner: ya
alasan tidak selesai: ('umur', 'akhir_data', 'carry')
  titik impas 4R 0.2 8R 0.1111
H-011 siap: H-011 h011_semesta_penuh 12 kombinasi, sidik 8a6efde6d333
  batas simbol terpakai: 40 ramalan tertulis: 7
  saringan ADR-004 tetap: 168 0.25 30
mekanisme H-011 identik H-010: lookback [20, 55, 100] imbalan [2.0, 4.0, 6.0, 8.0] 12 kombinasi
ADR-009 ditegakkan: pengaman menyala di 12 dari 12 kandidat
kriteria tidak dilonggarkan dan tidak diperketat: Kriteria(min_ekspektasi_R=0.05, min_trade_luar_sampel=100, maks_p_entri_acak=0.05, min_jendela_positif_rasio=0.5)
semesta 438 = terpakai 40 + tertahan 398
  terpakai: 1000000BOBUSDT .. ANTUSDT
  tertahan: APEUSDT .. ZRXUSDT
=== unduh ===
total 571540
drwxr-xr-x  2 runner runner     4096 Jul 26 08:30 .
drwxr-xr-x 15 runner runner     4096 Jul 26 08:30 ..
-rw-r--r--  1 runner runner  1439106 Jul 26 08:30 funding_shard00.parquet
-rw-r--r--  1 runner runner  1525153 Jul 26 08:30 funding_shard01.parquet
-rw-r--r--  1 runner runner  1539799 Jul 26 08:30 funding_shard02.parquet
-rw-r--r--  1 runner runner  1566092 Jul 26 08:30 funding_shard03.parquet
-rw-r--r--  1 runner runner 89681568 Jul 26 08:30 ohlcv_1h_shard00.parquet
-rw-r--r--  1 runner runner 72981771 Jul 26 08:30 ohlcv_1h_shard01.parquet
-rw-r--r--  1 runner runner 63261856 Jul 26 08:30 ohlcv_1h_shard02.parquet
-rw-r--r--  1 runner runner 66281060 Jul 26 08:30 ohlcv_1h_shard03.parquet
-rw-r--r--  1 runner runner 72859250 Jul 26 08:30 ohlcv_1h_shard04.parquet
-rw-r--r--  1 runner runner 65268945 Jul 26 08:30 ohlcv_1h_shard05.parquet
-rw-r--r--  1 runner runner 64058851 Jul 26 08:30 ohlcv_1h_shard06.parquet
-rw-r--r--  1 runner runner 65172181 Jul 26 08:30 ohlcv_1h_shard07.parquet
-rw-r--r--  1 runner runner  4834550 Jul 26 08:30 ohlcv_1h_tail_shard00.parquet
-rw-r--r--  1 runner runner  5234777 Jul 26 08:30 ohlcv_1h_tail_shard01.parquet
-rw-r--r--  1 runner runner  4894539 Jul 26 08:30 ohlcv_1h_tail_shard02.parquet
-rw-r--r--  1 runner runner  4624261 Jul 26 08:30 ohlcv_1h_tail_shard03.parquet
559M	aset
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       145G   58G   88G  40% /
```

## Langkah jalan

```
H-011 semesta penuh: limit 0, ulangan 300 (H-010: limit 40, ulangan 100)
grid identik H-010: lookback [20, 55, 100], imbalan [2.0, 4.0, 6.0, 8.0], 12 kombinasi
simbol sudah terpakai: 40 (1000000BOBUSDT .. ANTUSDT)
  ramalan ekspektasi_tertahan_R: 0,020-0,045, jadi TURUN di bawah ambang 0,05 dan H-011 gagal
  ramalan tafsir_batas: di atas 0,05 pada 398 simbol asing adalah bukti terkuat yang pernah dihasilkan riset ini; di bawah 0,020 berarti hasil 40 simbol adalah derau seleksi dan H-010 wajib diperlakukan sebagai kebetulan
  ramalan p_entri_acak: 0,01-0,15; p di atas 0,05 menjatuhkan H-011 MESKIPUN ekspektasinya tinggi
  ramalan jumlah_trade: 100.000-160.000 (penskalaan 11.734 x 438/40 = 128.487)
  ramalan retensi_drop_1: minimal 0,95; dengan 438 simbol satu simbol tak boleh berarti
  ramalan durasi: 15-60 menit; melewati batas 330 menit adalah timeout dan itu informasi, bukan alasan memperkecil semesta
  ramalan porsi_funding_ekor_maks: 0,10-0,30, tetap di bawah ambang 0,35
universe layak 438, diuji 438
  dibaca ohlcv_1h_shard00.parquet
  dibaca ohlcv_1h_shard01.parquet
  dibaca ohlcv_1h_shard02.parquet
  dibaca ohlcv_1h_shard03.parquet
  dibaca ohlcv_1h_shard04.parquet
  dibaca ohlcv_1h_shard05.parquet
  dibaca ohlcv_1h_shard06.parquet
  dibaca ohlcv_1h_shard07.parquet
  dibaca ohlcv_1h_tail_shard00.parquet
  dibaca ohlcv_1h_tail_shard01.parquet
  dibaca ohlcv_1h_tail_shard02.parquet
  dibaca ohlcv_1h_tail_shard03.parquet
  akhir_per_simbol: 790 simbol dari reports/akhir_sejati.json
438 simbol dimuat, 447 jadwal funding, 790 simbol dipindai untuk survivorship
checksum: hilang 0, asing 0, tidak cocok 0

=== H-011 terdaftar di hipotesis/H-011.json (sidik 8a6efde6d333, 12 kombinasi) ===
  [10/438] 1000SATSUSDT: 233 trade, 12s
  [20/438] ACXUSDT: 98 trade, 30s
  [30/438] AKROUSDT: 92 trade, 40s
  [40/438] ANTUSDT: 280 trade, 58s
  [50/438] ASRUSDT: 36 trade, 76s
  [60/438] AVAXUSDT: 580 trade, 93s
  [70/438] BANANAUSDT: 140 trade, 105s
  [80/438] BICOUSDT: 277 trade, 125s
  [90/438] BRETTUSDT: 133 trade, 139s
  [100/438] C98USDT: 546 trade, 152s
  [110/438] CHRUSDT: 626 trade, 168s
  [120/438] CTSIUSDT: 591 trade, 188s
  [130/438] DFUSDT: 148 trade, 202s
  [140/438] DUSDT: 72 trade, 214s
  [150/438] EOSUSDT: 664 trade, 237s
  [160/438] FIDAUSDT: 101 trade, 252s
  [170/438] FUSDT: 59 trade, 266s
  [180/438] GPSUSDT: 74 trade, 280s
  [190/438] HFTUSDT: 394 trade, 294s
  [200/438] HUSDT: 81 trade, 304s
  [210/438] INJUSDT: 378 trade, 317s
  [220/438] JTOUSDT: 346 trade, 335s
  [230/438] KSMUSDT: 776 trade, 352s
  [240/438] LRCUSDT: 649 trade, 370s
  [250/438] MATICUSDT: 396 trade, 390s
  [260/438] MKRUSDT: 576 trade, 402s
  [270/438] MYROUSDT: 137 trade, 411s
  [280/438] NOTUSDT: 172 trade, 427s
  [290/438] ONTUSDT: 751 trade, 446s
  [300/438] PERPUSDT: 211 trade, 459s
  [310/438] PORTALUSDT: 197 trade, 469s
  [320/438] RAYSOLUSDT: 146 trade, 481s
  [330/438] RNDRUSDT: 116 trade, 495s
  [340/438] SANDUSDT: 677 trade, 516s
  [350/438] SKYAIUSDT: 53 trade, 527s
  [360/438] SQDUSDT: 42 trade, 539s
  [370/438] SUNUSDT: 143 trade, 556s
  [380/438] TACUSDT: 82 trade, 568s
  [390/438] TRBUSDT: 761 trade, 584s
  [400/438] UNIUSDT: 651 trade, 600s
  [410/438] VINEUSDT: 63 trade, 610s
  [420/438] WUSDT: 233 trade, 621s
  [430/438] YGGUSDT: 349 trade, 646s
  [438/438] ZRXUSDT: 848 trade, 664s
{
  "jumlah_simbol": 438,
  "jumlah_jendela": 4092,
  "jendela_positif": 2246,
  "jumlah_trade_luar_sampel": 136337,
  "total_R": -10781.323489592633,
  "ekspektasi_R": -0.07907848558786414
}
alasan keluar: {'stop': 102068, 'umur': 9699, 'target': 21649, 'akhir_data': 2479, 'carry': 442}
parameter terpilih: {'{"imbalan_R": 8.0, "lookback": 20}': 575, '{"imbalan_R": 6.0, "lookback": 100}': 408, '{"imbalan_R": 8.0, "lookback": 100}': 656, '{"imbalan_R": 8.0, "lookback": 55}': 498, '{"imbalan_R": 6.0, "lookback": 55}': 323, '{"imbalan_R": 4.0, "lookback": 55}': 180, '{"imbalan_R": 2.0, "lookback": 55}': 99, '{"imbalan_R": 6.0, "lookback": 20}': 434, '{"imbalan_R": 2.0, "lookback": 20}': 254, '{"imbalan_R": 4.0, "lookback": 100}': 221, '{"imbalan_R": 4.0, "lookback": 20}': 347, '{"imbalan_R": 2.0, "lookback": 100}': 97}
konsentrasi: tidak dapat dinilai: ekspektasi gabungan -0.07907848558786414 tidak positif sehingga retensi tidak bermakna
funding ekor: porsi ekor maks 0.0102 (rerata 0.0010 atas 10 terburuk), funding maks 2.3900R, 440 dari 136337 trade di atas pengaman (0.00323); gagal: funding_maks_R
sebaran: std 4.24670R, galat baku 0.011501R, jarak ke ambang -0.129078R = -11.22 galat baku
entri acak: nyata 0.04661R, p 0.06312292358803986

=== KRITERIA UTAMA ADR-013: SIMBOL TERTAHAN ===
tertahan: 398 simbol, 124,603 trade, total -11403.56R, ekspektasi -0.09151913196311486
sudah terpakai: 40 simbol, 11,734 trade, total 622.23R, ekspektasi 0.053028362024884944
selisih tertahan - terpakai: -0.144547R
kriteria utama terhadap 0.05R: GAGAL (ramalan saya: GAGAL, 0,020-0,045)
catatan: total_R di per_simbol dibulatkan empat desimal, jadi ekspektasi tertahan terikat galat pembulatan orde 1e-4 R per simbol; galat baku subkumpulan ini TIDAK dapat dihitung dari per_simbol

putusan seluruh kumpulan: False
ekspektasi seluruh kumpulan: -0.07907848558786414 (H-010 0.05302836360569971)
trade: 136,337 (H-010 11,734)
p entri acak: 0.06312292358803986 (H-010 0.04950495049504951)
retensi drop-1: None (H-010 0.8578454756024698)
galat baku: 0.011501240543736661
jarak ke ambang dalam galat baku: -11.223005474670956
porsi funding ekor maks: 0.010229285698450875
gerbang gagal: ['entri_acak', 'invarian_risiko', 'konsentrasi', 'funding_ekor']
durasi: 838.1s
```
