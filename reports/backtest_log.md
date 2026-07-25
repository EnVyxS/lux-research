# Log run backtest H-008 (ADR-008)

Commit: `245747ee11894c2fbc771c7a98fdc3b4c782e4bf`
Run: `30177253467`

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
........................................................................ [ 17%]
........................................................................ [ 35%]
........................................................................ [ 52%]
........................................................................ [ 70%]
........................................................................ [ 87%]
...................................................                      [100%]
411 passed in 2.20s
=== impor ===
impor pihak ketiga siap
run_wf siap ('_retry',)
runner bersama siap
ADR-008 bawaan mati: True
alasan tidak selesai: ('umur', 'akhir_data', 'carry')
H-008 siap: H-008 h008_carry_keras 36 kombinasi, sidik dfeeea04fd41
  lookback [20, 55, 100] imbalan [1.0, 2.0, 3.0, 4.0] carry keras [0.0, 0.25, 0.5] kandidat 36
  saringan ADR-004 tetap: 168 0.25 30
=== unduh ===
total 571540
drwxr-xr-x  2 runner runner     4096 Jul 25 22:16 .
drwxr-xr-x 15 runner runner     4096 Jul 25 22:16 ..
-rw-r--r--  1 runner runner  1439106 Jul 25 22:16 funding_shard00.parquet
-rw-r--r--  1 runner runner  1525153 Jul 25 22:16 funding_shard01.parquet
-rw-r--r--  1 runner runner  1539799 Jul 25 22:16 funding_shard02.parquet
-rw-r--r--  1 runner runner  1566092 Jul 25 22:16 funding_shard03.parquet
-rw-r--r--  1 runner runner 89681568 Jul 25 22:16 ohlcv_1h_shard00.parquet
-rw-r--r--  1 runner runner 72981771 Jul 25 22:16 ohlcv_1h_shard01.parquet
-rw-r--r--  1 runner runner 63261856 Jul 25 22:16 ohlcv_1h_shard02.parquet
-rw-r--r--  1 runner runner 66281060 Jul 25 22:16 ohlcv_1h_shard03.parquet
-rw-r--r--  1 runner runner 72859250 Jul 25 22:16 ohlcv_1h_shard04.parquet
-rw-r--r--  1 runner runner 65268945 Jul 25 22:16 ohlcv_1h_shard05.parquet
-rw-r--r--  1 runner runner 64058851 Jul 25 22:16 ohlcv_1h_shard06.parquet
-rw-r--r--  1 runner runner 65172181 Jul 25 22:16 ohlcv_1h_shard07.parquet
-rw-r--r--  1 runner runner  4834550 Jul 25 22:16 ohlcv_1h_tail_shard00.parquet
-rw-r--r--  1 runner runner  5234777 Jul 25 22:16 ohlcv_1h_tail_shard01.parquet
-rw-r--r--  1 runner runner  4894539 Jul 25 22:16 ohlcv_1h_tail_shard02.parquet
-rw-r--r--  1 runner runner  4624261 Jul 25 22:16 ohlcv_1h_tail_shard03.parquet
559M	aset
```

## Langkah jalan

```
ADR-004 proyeksi: maks_carry_R=0.25
ADR-008 ambang carry keras yang dilombakan: [0.0, 0.25, 0.5]
kandidat: 36 kombinasi
  pembanding H-002: +0.03159R, gerbang gagal: tidak ada
  pembanding H-007: +0.04044R, gerbang gagal: invarian_risiko -1.9769
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

=== H-008 terdaftar di hipotesis/H-008.json (sidik dfeeea04fd41, 36 kombinasi) ===
  [10/40] 1000SATSUSDT: 261 trade, 37s
  [20/40] ACXUSDT: 148 trade, 94s
  [30/40] AKROUSDT: 155 trade, 127s
  [40/40] ANTUSDT: 322 trade, 181s
{
  "jumlah_simbol": 40,
  "jumlah_jendela": 356,
  "jendela_positif": 198,
  "jumlah_trade_luar_sampel": 14933,
  "total_R": 616.2028006458954,
  "ekspektasi_R": 0.04126450148301717
}
alasan keluar: {'stop': 10254, 'target': 4117, 'umur': 371, 'akhir_data': 189, 'carry': 2}
parameter terpilih: {'{"imbalan_R": 3.0, "lookback": 20, "maks_carry_realisasi_R": 0.25}': 4, '{"imbalan_R": 2.0, "lookback": 100, "maks_carry_realisasi_R": 0.0}': 11, '{"imbalan_R": 4.0, "lookback": 100, "maks_carry_realisasi_R": 0.0}': 78, '{"imbalan_R": 3.0, "lookback": 100, "maks_carry_realisasi_R": 0.0}': 30, '{"imbalan_R": 4.0, "lookback": 20, "maks_carry_realisasi_R": 0.0}': 59, '{"imbalan_R": 3.0, "lookback": 55, "maks_carry_realisasi_R": 0.0}': 29, '{"imbalan_R": 3.0, "lookback": 20, "maks_carry_realisasi_R": 0.0}': 38, '{"imbalan_R": 4.0, "lookback": 55, "maks_carry_realisasi_R": 0.0}': 40, '{"imbalan_R": 2.0, "lookback": 55, "maks_carry_realisasi_R": 0.0}': 12, '{"imbalan_R": 1.0, "lookback": 20, "maks_carry_realisasi_R": 0.0}': 11, '{"imbalan_R": 4.0, "lookback": 20, "maks_carry_realisasi_R": 0.25}': 6, '{"imbalan_R": 2.0, "lookback": 20, "maks_carry_realisasi_R": 0.0}': 14, '{"imbalan_R": 1.0, "lookback": 100, "maks_carry_realisasi_R": 0.0}': 7, '{"imbalan_R": 4.0, "lookback": 55, "maks_carry_realisasi_R": 0.25}': 5, '{"imbalan_R": 4.0, "lookback": 100, "maks_carry_realisasi_R": 0.25}': 5, '{"imbalan_R": 3.0, "lookback": 100, "maks_carry_realisasi_R": 0.25}': 2, '{"imbalan_R": 1.0, "lookback": 55, "maks_carry_realisasi_R": 0.0}': 5}
entri acak: nyata 0.10787R, p 0.009900990099009901

keluar karena pengaman carry: 2
gerbang gagal: ['invarian_risiko']
ekspektasi 0.04126450148301717 vs H-007 0.04044
```
