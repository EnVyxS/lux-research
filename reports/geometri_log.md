# Log diagnostik geometri keluar

Commit: `51758f3656384335b67f2654ff7b7532ddfd5148`
Run: `30209272338`

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
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.7/12.7 MB 46.8 MB/s  0:00:00
Downloading pyarrow-17.0.0-cp312-cp312-manylinux_2_28_x86_64.whl (39.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 39.9/39.9 MB 119.8 MB/s  0:00:00
Downloading PyYAML-6.0.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (767 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 767.5/767.5 kB 71.5 MB/s  0:00:00
Downloading pytest-9.1.1-py3-none-any.whl (386 kB)
Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)
Downloading numpy-2.5.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.7/16.7 MB 119.2 MB/s  0:00:00
Downloading packaging-26.2-py3-none-any.whl (100 kB)
Downloading pygments-2.20.0-py3-none-any.whl (1.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 94.9 MB/s  0:00:00
Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
Downloading pytz-2026.3.post1-py2.py3-none-any.whl (508 kB)
Downloading six-1.17.0-py2.py3-none-any.whl (11 kB)
Downloading tzdata-2026.3-py2.py3-none-any.whl (348 kB)
Installing collected packages: pytz, tzdata, six, pyyaml, pygments, pluggy, packaging, numpy, iniconfig, python-dateutil, pytest, pyarrow, pandas

Successfully installed iniconfig-2.3.0 numpy-2.5.1 packaging-26.2 pandas-2.2.3 pluggy-1.6.0 pyarrow-17.0.0 pygments-2.20.0 pytest-9.1.1 python-dateutil-2.9.0.post0 pytz-2026.3.post1 pyyaml-6.0.2 six-1.17.0 tzdata-2026.3
```

## logs/geometri.log
```
-rw-r--r-- 1 runner runner 433866 Jul 26 15:56 reports/backtest_h012_periode_tertahan.json
ramalan 1: BENAR - perdagangan terburuk -21.3131R pada STGUSDT beralasan keluar 'carry', bukan 'stop'
ramalan 2: BENAR - tidak ada keluar 'stop' di bawah -1.5R, dan ekor terbukti memuat semua pelanggar
ramalan 3: SALAH - porsi bukan-stop di 10 terburuk = 0.1000 (1 dari 10)
ramalan 4: TIDAK DAPAT DINILAI - tidak ada keluar 'umur' di dalam ekor
# Geometri keluar H-012 (ADR-015 Bagian A)

Dihitung dari laporan yang **sudah dikomit**, bukan dari run baru. Tidak ada mesin yang dijalankan dan tidak ada angka baru yang diproduksi bagi hipotesis yang sudah divonis DITOLAK.

Ambang gerbang `invarian_risiko`: **-1.5R**, tidak bergerak.

## Batas bukti

Laporan hanya menyimpan **sepuluh** perdagangan terburuk, jadi tidak semua pertanyaan dapat dijawab darinya. Pertanyaan tentang perdagangan di bawah ambang dapat dijawab dengan pasti hanya bila perdagangan paling ringan di dalam ekor sudah berada di atas ambang, sebab dengan begitu mustahil ada pelanggar di luar ekor.

- Ekor memuat semua pelanggar: **ya**
- Perdagangan di bawah ambang: **1**

## 10 perdagangan terburuk

| Simbol | R | Alasan | Transaksi R | Funding R | R terlampaui | Celah R | Stop % harga | Jam |
|---|---|---|---|---|---|---|---|---|
| STGUSDT | -21.3131 | carry | 0.0559 | 0.4825 | 20.3131 | +19.7747 | 2.197 | 1.0 |
| TRXUSDT | -1.4966 | stop | 0.2123 | 0.1779 | 0.4966 | +0.1064 | 0.472 | 50.0 |
| TRXUSDT | -1.4246 | stop | 0.1979 | 0.1280 | 0.4246 | +0.0987 | 0.504 | 81.0 |
| TRXUSDT | -1.4176 | stop | 0.1751 | 0.1547 | 0.4176 | +0.0878 | 0.573 | 60.0 |
| BTCDOMUSDT | -1.4159 | stop | 0.1588 | 0.1774 | 0.4159 | +0.0796 | 0.632 | 109.0 |
| SUNUSDT | -1.4103 | stop | 0.1142 | 0.2387 | 0.4103 | +0.0573 | 0.880 | 59.0 |
| TRXUSDT | -1.4068 | stop | 0.1505 | 0.1813 | 0.4068 | +0.0750 | 0.662 | 96.0 |
| SUNUSDT | -1.4061 | stop | 0.1729 | 0.1466 | 0.4061 | +0.0867 | 0.580 | 50.0 |
| PAXGUSDT | -1.3870 | stop | 0.1778 | 0.1206 | 0.3870 | +0.0887 | 0.561 | 102.0 |
| BTCDOMUSDT | -1.3865 | stop | 0.2274 | 0.0456 | 0.3865 | +0.1135 | 0.439 | 11.0 |

## Median R terlampaui menurut alasan keluar

| Alasan | Median R terlampaui |
|---|---|
| carry | 20.313091 |
| stop | 0.410263 |

## Adjudikasi ramalan Bagian A

| Ramalan | Hasil | Bukti |
|---|---|---|
| 1 | **BENAR** | perdagangan terburuk -21.3131R pada STGUSDT beralasan keluar 'carry', bukan 'stop' |
| 2 | **BENAR** | tidak ada keluar 'stop' di bawah -1.5R, dan ekor terbukti memuat semua pelanggar |
| 3 | **SALAH** | porsi bukan-stop di 10 terburuk = 0.1000 (1 dari 10) |
| 4 | **TIDAK DAPAT DINILAI** | tidak ada keluar 'umur' di dalam ekor |
```

## logs/uji.log
```
......................                                                   [100%]
22 passed in 0.08s
```

