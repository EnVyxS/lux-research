# Log run backtest H-010 (ADR-012)

Commit: `0a30ced4696c6ee74b070be5da50ee83ba12973a`
Run: `30193898133`

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
........................................................................ [ 14%]
........................................................................ [ 28%]
........................................................................ [ 42%]
........................................................................ [ 56%]
........................................................................ [ 70%]
........................................................................ [ 84%]
........................................................................ [ 98%]
......                                                                   [100%]
510 passed in 1.81s
=== impor ===
impor pihak ketiga siap
run_wf siap ('_retry',)
runner bersama siap
jumlah gerbang: 11
  nama: ('forward_fill', 'buy_and_hold', 'entri_acak', 'lookahead', 'invarian_risiko', 'funding', 'overlap', 'checksum', 'survivorship', 'konsentrasi', 'funding_ekor')
gerbang kesepuluh dan kesebelas terdaftar: ya
bawaan pengaman mati: True
alasan tidak selesai: ('umur', 'akhir_data', 'carry')
  titik impas 4R 0.2 8R 0.1111
H-010 siap: H-010 h010_imbalan_diperluas 12 kombinasi, sidik 14b2f3bfa8a7
  lookback [20, 55, 100] imbalan [2.0, 4.0, 6.0, 8.0] kandidat 12
  ambang carry DIPATOK: 0.25
  saringan ADR-004 tetap: 168 0.25 30
kontrak beku H-009 utuh: ya
ADR-012 ditegakkan: imbalan [1.0, 2.0, 3.0, 4.0] -> [2.0, 4.0, 6.0, 8.0] dengan 12 kombinasi
ADR-009 ditegakkan: pengaman menyala di 12 dari 12 kandidat
=== unduh ===
total 571540
drwxr-xr-x  2 runner runner     4096 Jul 26 08:03 .
drwxr-xr-x 15 runner runner     4096 Jul 26 08:03 ..
-rw-r--r--  1 runner runner  1439106 Jul 26 08:03 funding_shard00.parquet
-rw-r--r--  1 runner runner  1525153 Jul 26 08:03 funding_shard01.parquet
-rw-r--r--  1 runner runner  1539799 Jul 26 08:03 funding_shard02.parquet
-rw-r--r--  1 runner runner  1566092 Jul 26 08:03 funding_shard03.parquet
-rw-r--r--  1 runner runner 89681568 Jul 26 08:03 ohlcv_1h_shard00.parquet
-rw-r--r--  1 runner runner 72981771 Jul 26 08:03 ohlcv_1h_shard01.parquet
-rw-r--r--  1 runner runner 63261856 Jul 26 08:03 ohlcv_1h_shard02.parquet
-rw-r--r--  1 runner runner 66281060 Jul 26 08:03 ohlcv_1h_shard03.parquet
-rw-r--r--  1 runner runner 72859250 Jul 26 08:03 ohlcv_1h_shard04.parquet
-rw-r--r--  1 runner runner 65268945 Jul 26 08:03 ohlcv_1h_shard05.parquet
-rw-r--r--  1 runner runner 64058851 Jul 26 08:03 ohlcv_1h_shard06.parquet
-rw-r--r--  1 runner runner 65172181 Jul 26 08:03 ohlcv_1h_shard07.parquet
-rw-r--r--  1 runner runner  4834550 Jul 26 08:03 ohlcv_1h_tail_shard00.parquet
-rw-r--r--  1 runner runner  5234777 Jul 26 08:03 ohlcv_1h_tail_shard01.parquet
-rw-r--r--  1 runner runner  4894539 Jul 26 08:03 ohlcv_1h_tail_shard02.parquet
-rw-r--r--  1 runner runner  4624261 Jul 26 08:03 ohlcv_1h_tail_shard03.parquet
559M	aset
```

## Langkah jalan

```
ADR-012 grid imbalan: [2.0, 4.0, 6.0, 8.0] (H-007: [1.0, 2.0, 3.0, 4.0])
ADR-009 ambang carry keras DIPATOK: 0.25
kandidat: 12 kombinasi
  titik impas kotor 2.0R: 0.3333
  titik impas kotor 4.0R: 0.2000
  titik impas kotor 6.0R: 0.1429
  titik impas kotor 8.0R: 0.1111
  pembanding H-007: +0.04044R, gerbang: invarian_risiko -1.9769
  pembanding H-008: +0.04126R, gerbang: invarian_risiko -1.9769
  pembanding H-009: +0.04136R, gerbang: tidak ada, ditolak oleh ambang 0,05R
  ramalan porsi_jendela_imbalan_8: 30-55 persen; di atas 54,5 persen berarti penempelan bersifat mekanis, di bawah 25 persen berarti dinding H-007 bukan dinding
  ramalan laju_kena_target: turun ke 0,13-0,20 dari 0,27544
  ramalan porsi_tak_selesai: naik dari 3,7 persen ke lebih dari 12 persen
  ramalan porsi_funding_ekor_maks: naik ke 0,20-0,35; di atas 0,35 gerbang kesebelas GAGAL dan itu temuan, bukan alasan melonggarkan ambang
  ramalan ekspektasi_R: 0,030-0,048, jadi tidak mencapai 0,05
universe layak 438, diuji 40
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
40 simbol dimuat, 447 jadwal funding, 790 simbol dipindai untuk survivorship
checksum: hilang 0, asing 0, tidak cocok 0

=== H-010 terdaftar di hipotesis/H-010.json (sidik 14b2f3bfa8a7, 12 kombinasi) ===
  [10/40] 1000SATSUSDT: 233 trade, 12s
  [20/40] ACXUSDT: 98 trade, 30s
  [30/40] AKROUSDT: 92 trade, 41s
  [40/40] ANTUSDT: 280 trade, 59s
{
  "jumlah_simbol": 40,
  "jumlah_jendela": 356,
  "jendela_positif": 188,
  "jumlah_trade_luar_sampel": 11734,
  "total_R": 622.2348185492804,
  "ekspektasi_R": 0.05302836360569971
}
alasan keluar: {'stop': 8776, 'umur': 879, 'target': 1839, 'akhir_data': 214, 'carry': 26}
parameter terpilih: {'{"imbalan_R": 8.0, "lookback": 20}': 47, '{"imbalan_R": 6.0, "lookback": 100}': 34, '{"imbalan_R": 8.0, "lookback": 100}': 61, '{"imbalan_R": 8.0, "lookback": 55}': 54, '{"imbalan_R": 6.0, "lookback": 55}': 30, '{"imbalan_R": 4.0, "lookback": 55}': 18, '{"imbalan_R": 2.0, "lookback": 55}': 14, '{"imbalan_R": 6.0, "lookback": 20}': 32, '{"imbalan_R": 2.0, "lookback": 20}': 19, '{"imbalan_R": 4.0, "lookback": 100}': 15, '{"imbalan_R": 4.0, "lookback": 20}': 26, '{"imbalan_R": 2.0, "lookback": 100}': 6}
konsentrasi: 26 untung / 14 rugi dari 40 simbol; drop-1 0.04549R (retensi 0.8578), drop-2 0.03924R, median simbol +0.04604R, porsi bruto teratas 0.1346 (ADAUSDT), setara 14.9 simbol
funding ekor: porsi ekor maks 0.1675 (rerata 0.1487 atas 10 terburuk), funding maks 0.4144R, 26 dari 11734 trade di atas pengaman (0.00222)
entri acak: nyata 0.04661R, p 0.04950495049504951

laju kena target: 0.15672 (H-009 0.27544)
porsi perdagangan tak selesai: 0.09536 (H-009 0.03832)
keluar karena pengaman carry: 26
porsi funding ekor maks: 0.16749100396531466 (H-009 0.165, ambang 0,35)
retensi drop-1: 0.8578454756024698
gerbang gagal: []
ekspektasi 0.05302836360569971 vs H-009 0.041359
```
