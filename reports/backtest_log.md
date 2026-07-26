# Log backtest H-013

Run: `30213913942`
Commit: `135b159c1857ad32105f519b5014ec1b1d6eba00`

## Berkas hasil

Laporan yang dikomit tanpa backtest_h013_kontribusi.json berarti run GAGAL.

```
ls: cannot access 'reports/backtest_h013_kontribusi.md': No such file or directory
ls: cannot access 'reports/backtest_h013_kontribusi.json': No such file or directory
(ringkasan kontribusi TIDAK ADA - run GAGAL sebelum selesai)

--- laporan per sel ---
ls: cannot access 'reports/backtest_h013_*.json': No such file or directory
(tidak satu sel pun menulis laporan)
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
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.7/12.7 MB 122.1 MB/s  0:00:00
Downloading pyarrow-17.0.0-cp312-cp312-manylinux_2_28_x86_64.whl (39.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 39.9/39.9 MB 161.4 MB/s  0:00:00
Downloading PyYAML-6.0.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (767 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 767.5/767.5 kB 63.9 MB/s  0:00:00
Downloading pytest-9.1.1-py3-none-any.whl (386 kB)
Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)
Downloading numpy-2.5.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.7/16.7 MB 300.9 MB/s  0:00:00
Downloading packaging-26.2-py3-none-any.whl (100 kB)
Downloading pygments-2.20.0-py3-none-any.whl (1.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 191.3 MB/s  0:00:00
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
........................................................................ [ 39%]
........................................................................ [ 48%]
........................................................................ [ 58%]
........................................................................ [ 68%]
........................................................................ [ 78%]
........................................................................ [ 87%]
........................................................................ [ 97%]
.................                                                        [100%]
737 passed in 2.76s
```

## logs/preflight.log

```
1. mekanisme diimpor tanpa perubahan, imbalan BEKU: OK
2. ambang ADR-015 tidak bergerak: OK
Traceback (most recent call last):
  File "<stdin>", line 65, in <module>
AssertionError
```

## logs/lantai.log

```
(langkah ini tidak pernah berjalan atau tidak menulis apa pun)
```

## logs/unduh.log

```
total 153972
drwxr-xr-x  2 runner runner     4096 Jul 26 17:01 .
drwxr-xr-x 15 runner runner     4096 Jul 26 17:00 ..
-rw-r--r--  1 runner runner 23609925 Jul 26 17:01 ohlcv_4h_shard00.parquet
-rw-r--r--  1 runner runner 19595753 Jul 26 17:00 ohlcv_4h_shard01.parquet
-rw-r--r--  1 runner runner 17515963 Jul 26 17:01 ohlcv_4h_shard02.parquet
-rw-r--r--  1 runner runner 18412119 Jul 26 17:00 ohlcv_4h_shard03.parquet
-rw-r--r--  1 runner runner 19904881 Jul 26 17:01 ohlcv_4h_shard04.parquet
-rw-r--r--  1 runner runner 17959843 Jul 26 17:01 ohlcv_4h_shard05.parquet
-rw-r--r--  1 runner runner 17326751 Jul 26 17:01 ohlcv_4h_shard06.parquet
-rw-r--r--  1 runner runner 17844356 Jul 26 17:01 ohlcv_4h_shard07.parquet
-rw-r--r--  1 runner runner  1362914 Jul 26 17:01 ohlcv_4h_tail_shard00.parquet
-rw-r--r--  1 runner runner  1437885 Jul 26 17:01 ohlcv_4h_tail_shard01.parquet
-rw-r--r--  1 runner runner  1364053 Jul 26 17:01 ohlcv_4h_tail_shard02.parquet
-rw-r--r--  1 runner runner  1294176 Jul 26 17:01 ohlcv_4h_tail_shard03.parquet
151M	aset
```

## logs/backtest.log

```
(langkah ini tidak pernah berjalan atau tidak menulis apa pun)
```
