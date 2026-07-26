# Log run backtest H-009 (ADR-009)

Commit: `d5f18c6f8859d200b73c9a2fde122ed6657a8115`
Run: `30186730437`

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
........................................................................ [ 16%]
........................................................................ [ 32%]
........................................................................ [ 48%]
........................................................................ [ 64%]
........................................................................ [ 81%]
........................................................................ [ 97%]
............                                                             [100%]
444 passed in 2.24s
=== impor ===
impor pihak ketiga siap
run_wf siap ('_retry',)
runner bersama siap
bawaan pengaman mati: True
alasan tidak selesai: ('umur', 'akhir_data', 'carry')
H-009 siap: H-009 h009_carry_dipatok 12 kombinasi, sidik eac6c83305bd
  lookback [20, 55, 100] imbalan [1.0, 2.0, 3.0, 4.0] kandidat 12
  ambang carry DIPATOK: 0.25
  saringan ADR-004 tetap: 168 0.25 30
grid identik dengan H-007: ya
ADR-009 ditegakkan: pengaman menyala di 12 dari 12 kandidat
=== unduh ===
total 571540
drwxr-xr-x  2 runner runner     4096 Jul 26 03:48 .
drwxr-xr-x 15 runner runner     4096 Jul 26 03:48 ..
-rw-r--r--  1 runner runner  1439106 Jul 26 03:48 funding_shard00.parquet
-rw-r--r--  1 runner runner  1525153 Jul 26 03:48 funding_shard01.parquet
-rw-r--r--  1 runner runner  1539799 Jul 26 03:48 funding_shard02.parquet
-rw-r--r--  1 runner runner  1566092 Jul 26 03:48 funding_shard03.parquet
-rw-r--r--  1 runner runner 89681568 Jul 26 03:48 ohlcv_1h_shard00.parquet
-rw-r--r--  1 runner runner 72981771 Jul 26 03:48 ohlcv_1h_shard01.parquet
-rw-r--r--  1 runner runner 63261856 Jul 26 03:48 ohlcv_1h_shard02.parquet
-rw-r--r--  1 runner runner 66281060 Jul 26 03:48 ohlcv_1h_shard03.parquet
-rw-r--r--  1 runner runner 72859250 Jul 26 03:48 ohlcv_1h_shard04.parquet
-rw-r--r--  1 runner runner 65268945 Jul 26 03:48 ohlcv_1h_shard05.parquet
-rw-r--r--  1 runner runner 64058851 Jul 26 03:48 ohlcv_1h_shard06.parquet
-rw-r--r--  1 runner runner 65172181 Jul 26 03:48 ohlcv_1h_shard07.parquet
-rw-r--r--  1 runner runner  4834550 Jul 26 03:48 ohlcv_1h_tail_shard00.parquet
-rw-r--r--  1 runner runner  5234777 Jul 26 03:48 ohlcv_1h_tail_shard01.parquet
-rw-r--r--  1 runner runner  4894539 Jul 26 03:48 ohlcv_1h_tail_shard02.parquet
-rw-r--r--  1 runner runner  4624261 Jul 26 03:48 ohlcv_1h_tail_shard03.parquet
559M	aset
```

## Langkah jalan

```
ADR-004 proyeksi: maks_carry_R=0.25
ADR-009 ambang carry keras DIPATOK: 0.25 (bukan parameter, tidak dilombakan)
kandidat: 12 kombinasi
  pembanding H-007: +0.04044R, gerbang gagal: invarian_risiko -1.9769
  pembanding H-008: +0.04126R, gerbang gagal: invarian_risiko -1.9769
  ramalan keluar_carry: melonjak dari 2 ke ratusan
  ramalan kerugian_terburuk_R: lebih kecil dari 1,5 sehingga invarian_risiko lulus
  ramalan ekspektasi_R: turun di bawah 0,04126 milik H-008
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

=== H-009 terdaftar di hipotesis/H-009.json (sidik eac6c83305bd, 12 kombinasi) ===
  [10/40] 1000SATSUSDT: 261 trade, 16s
  [20/40] ACXUSDT: 148 trade, 40s
  [30/40] AKROUSDT: 155 trade, 54s
  [40/40] ANTUSDT: 322 trade, 77s
{
  "jumlah_simbol": 40,
  "jumlah_jendela": 356,
  "jendela_positif": 198,
  "jumlah_trade_luar_sampel": 14925,
  "total_R": 617.2774008809608,
  "ekspektasi_R": 0.041358619824519986
}
alasan keluar: {'stop': 10242, 'target': 4111, 'umur': 368, 'akhir_data': 188, 'carry': 16}
parameter terpilih: {'{"imbalan_R": 3.0, "lookback": 20}': 42, '{"imbalan_R": 2.0, "lookback": 100}': 12, '{"imbalan_R": 4.0, "lookback": 100}': 82, '{"imbalan_R": 3.0, "lookback": 100}': 32, '{"imbalan_R": 4.0, "lookback": 20}': 64, '{"imbalan_R": 3.0, "lookback": 55}': 27, '{"imbalan_R": 4.0, "lookback": 55}': 48, '{"imbalan_R": 2.0, "lookback": 55}': 12, '{"imbalan_R": 1.0, "lookback": 20}': 11, '{"imbalan_R": 2.0, "lookback": 20}': 14, '{"imbalan_R": 1.0, "lookback": 100}': 7, '{"imbalan_R": 1.0, "lookback": 55}': 5}
entri acak: nyata 0.10781R, p 0.009900990099009901

keluar karena pengaman carry: 16
gerbang gagal: []
ekspektasi 0.041358619824519986 vs H-008 0.04126
```
