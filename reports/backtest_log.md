# Log backtest H-012

Run: `30198942815`
Commit: `1637d035fb102ed994c7e8377b4f25bfad906066`

## Berkas hasil

Laporan yang dikomit tanpa berkas hasil berarti run GAGAL.

```
ls: cannot access 'reports/backtest_h012_periode_tertahan.md': No such file or directory
ls: cannot access 'reports/backtest_h012_periode_tertahan.json': No such file or directory
(berkas hasil TIDAK ADA - run GAGAL sebelum selesai)
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
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.7/12.7 MB 172.0 MB/s  0:00:00
Downloading pyarrow-17.0.0-cp312-cp312-manylinux_2_28_x86_64.whl (39.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 39.9/39.9 MB 266.3 MB/s  0:00:00
Downloading PyYAML-6.0.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (767 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 767.5/767.5 kB 142.0 MB/s  0:00:00
Downloading pytest-9.1.1-py3-none-any.whl (386 kB)
Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)
Downloading numpy-2.5.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.7/16.7 MB 254.3 MB/s  0:00:00
Downloading packaging-26.2-py3-none-any.whl (100 kB)
Downloading pygments-2.20.0-py3-none-any.whl (1.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 207.6 MB/s  0:00:00
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
........................................................................ [ 11%]
........................................................................ [ 23%]
........................................................................ [ 35%]
........................................................................ [ 46%]
........................................................................ [ 58%]
........................................................................ [ 70%]
........................................................................ [ 81%]
........................................................................ [ 93%]
.......................................                                  [100%]
615 passed in 2.75s
```

## logs/preflight.log

```
1. mekanisme identik H-010/H-009: OK
2. ambang pra-registrasi dan batas periode: OK
3. angka kembar config <-> degenerasi: OK
4. 0.002 / 0.004 = 0.5R: OK
5. bawaan pengaman dan lantai tetap MATI: OK
6. lantai dan agregat periode tersambung di runner: OK
7. batas periode dimiliki periode tahan: OK
8. angka haram tidak dipakai sebagai pembanding: OK

pagar pra-terbang H-012: LULUS
lantai 0.004, pengaman 0.5R
periode tahan sejak 2026-01-01 UTC
  ramalan 1_simbol_tersingkir: 1-6 simbol dibuang lantai; lebih dari 20 berarti H-012 BATAL sebelum diadili
  ramalan 2_ekspektasi_seluruh_riwayat: 0,050-0,065; ini hanya pemeriksaan konsistensi terhadap H-010 dan HARAM dipakai sebagai bukti kelulusan, sebab seluruh riwayat sudah dipakai memilih segalanya sejak H-001b
  ramalan 3_ekspektasi_periode_tahan: 0,010-0,045, jadi DI BAWAH ambang 0,05 dan H-012 GAGAL — ini ramalan saya sendiri terhadap hipotesis saya sendiri
  ramalan 4_p_entri_acak: 0,01-0,20; p di atas 0,05 menjatuhkan H-012 MESKIPUN ekspektasinya tinggi, sebagaimana p 0,0631 menjatuhkan mekanisme ini di H-010
  ramalan 5_entri_ditolak_pengaman: 500-5.000 entri ditolak; tafsirnya SEMPIT karena simbol yang degenerat sepanjang riwayat menyumbang NOL penolakan — pengaman menolak juga saat pemilihan parameter sehingga seluruh jendelanya dilewati
  ramalan 6_invarian_risiko: LULUS; bila ia masih gagal, lantai 0,004 belum menutup jalan masuk degenerasi dan seluruh ADR-014 keliru
  ramalan 7_durasi: 10-60 menit
```

## logs/unduh.log

```
16
559M	aset
```

## logs/backtest.log

```
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/home/runner/work/lux-research/lux-research/lux/backtest/run_h012.py", line 533, in <module>
    sys.exit(main())
             ^^^^^^
  File "/home/runner/work/lux-research/lux-research/lux/backtest/run_h012.py", line 327, in main
    bolak_balik = 2.0 * (dasar.fee_efektif + dasar.slippage)
                         ^^^^^^^^^^^^^^^^^
AttributeError: 'Konfig' object has no attribute 'fee_efektif'
```
