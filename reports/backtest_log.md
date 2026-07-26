# Log backtest H-012

Run: `30200123505`
Commit: `56a325d27603a4a8afc72ac23432e4408c641afa`

## Berkas hasil

Laporan yang dikomit tanpa berkas hasil berarti run GAGAL.

```
-rw-r--r-- 1 runner runner 433866 Jul 26 11:47 reports/backtest_h012_periode_tertahan.json
-rw-r--r-- 1 runner runner  11657 Jul 26 11:47 reports/backtest_h012_periode_tertahan.md
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
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.7/12.7 MB 47.8 MB/s  0:00:00
Downloading pyarrow-17.0.0-cp312-cp312-manylinux_2_28_x86_64.whl (39.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 39.9/39.9 MB 207.3 MB/s  0:00:00
Downloading PyYAML-6.0.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (767 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 767.5/767.5 kB 150.7 MB/s  0:00:00
Downloading pytest-9.1.1-py3-none-any.whl (386 kB)
Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)
Downloading numpy-2.5.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.7/16.7 MB 292.4 MB/s  0:00:00
Downloading packaging-26.2-py3-none-any.whl (100 kB)
Downloading pygments-2.20.0-py3-none-any.whl (1.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 216.7 MB/s  0:00:00
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
615 passed in 2.47s
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
H-012 periode tertahan: limit 0, ulangan 300, lantai 0.004, pengaman 0.5R
biaya bolak-balik 0.002 / lantai 0.004 = 0.5R
periode tahan DIBEKUKAN sejak 2026-01-01 UTC (bulan 2026-01, ms 1767225600000)
H-012 BUKAN rehabilitasi H-010: mekanisme ini gagal dengan p 0.0631 pada 300 permutasi
grid identik H-010: lookback [20, 55, 100], imbalan [2.0, 4.0, 6.0, 8.0], 12 kombinasi
  ramalan 1_simbol_tersingkir: 1-6 simbol dibuang lantai; lebih dari 20 berarti H-012 BATAL sebelum diadili
  ramalan 2_ekspektasi_seluruh_riwayat: 0,050-0,065; ini hanya pemeriksaan konsistensi terhadap H-010 dan HARAM dipakai sebagai bukti kelulusan, sebab seluruh riwayat sudah dipakai memilih segalanya sejak H-001b
  ramalan 3_ekspektasi_periode_tahan: 0,010-0,045, jadi DI BAWAH ambang 0,05 dan H-012 GAGAL — ini ramalan saya sendiri terhadap hipotesis saya sendiri
  ramalan 4_p_entri_acak: 0,01-0,20; p di atas 0,05 menjatuhkan H-012 MESKIPUN ekspektasinya tinggi, sebagaimana p 0,0631 menjatuhkan mekanisme ini di H-010
  ramalan 5_entri_ditolak_pengaman: 500-5.000 entri ditolak; tafsirnya SEMPIT karena simbol yang degenerat sepanjang riwayat menyumbang NOL penolakan — pengaman menolak juga saat pemilihan parameter sehingga seluruh jendelanya dilewati
  ramalan 6_invarian_risiko: LULUS; bila ia masih gagal, lantai 0,004 belum menutup jalan masuk degenerasi dan seluruh ADR-014 keliru
  ramalan 7_durasi: 10-60 menit
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
lantai median stop_frac 0.004: 437 layak, 1 dibuang dari 438 simbol dimuat
  DIBUANG USDCUSDT: median_stop_frac 1.293930e-04, median jarak stop 1.294e-04 di bawah lantai 0.004
lantai membuang 1 simbol (batas void 20)

=== H-012 terdaftar di hipotesis/H-012.json (sidik 75f9c7ccd65e, 12 kombinasi) ===
  [10/437] 1000SATSUSDT: 233 trade, 17s
  [20/437] ACXUSDT: 98 trade, 44s
  [30/437] AKROUSDT: 92 trade, 59s
  [40/437] ANTUSDT: 280 trade, 85s
  [50/437] ASRUSDT: 36 trade, 111s
  [60/437] AVAXUSDT: 580 trade, 136s
  [70/437] BANANAUSDT: 140 trade, 153s
  [80/437] BICOUSDT: 277 trade, 182s
  [90/437] BRETTUSDT: 133 trade, 203s
  [100/437] C98USDT: 546 trade, 222s
  [110/437] CHRUSDT: 626 trade, 245s
  [120/437] CTSIUSDT: 591 trade, 275s
  [130/437] DFUSDT: 148 trade, 295s
  [140/437] DUSDT: 72 trade, 313s
  [150/437] EOSUSDT: 664 trade, 347s
  [160/437] FIDAUSDT: 101 trade, 369s
  [170/437] FUSDT: 59 trade, 390s
  [180/437] GPSUSDT: 74 trade, 410s
  [190/437] HFTUSDT: 394 trade, 431s
  [200/437] HUSDT: 81 trade, 446s
  [210/437] INJUSDT: 378 trade, 466s
  [220/437] JTOUSDT: 346 trade, 492s
  [230/437] KSMUSDT: 776 trade, 516s
  [240/437] LRCUSDT: 649 trade, 543s
  [250/437] MATICUSDT: 396 trade, 571s
  [260/437] MKRUSDT: 576 trade, 589s
  [270/437] MYROUSDT: 137 trade, 602s
  [280/437] NOTUSDT: 172 trade, 625s
  [290/437] ONTUSDT: 751 trade, 651s
  [300/437] PERPUSDT: 211 trade, 670s
  [310/437] PORTALUSDT: 197 trade, 684s
  [320/437] RAYSOLUSDT: 146 trade, 701s
  [330/437] RNDRUSDT: 116 trade, 722s
  [340/437] SANDUSDT: 677 trade, 752s
  [350/437] SKYAIUSDT: 53 trade, 768s
  [360/437] SQDUSDT: 42 trade, 786s
  [370/437] SUNUSDT: 143 trade, 811s
  [380/437] TACUSDT: 82 trade, 828s
  [390/437] TRBUSDT: 761 trade, 850s
  [400/437] UNIUSDT: 651 trade, 874s
  [410/437] VIRTUALUSDT: 118 trade, 889s
  [420/437] XAIUSDT: 193 trade, 906s
  [430/437] ZECUSDT: 732 trade, 946s
  [437/437] ZRXUSDT: 848 trade, 967s
{
  "jumlah_simbol": 437,
  "jumlah_jendela": 4081,
  "jendela_positif": 2246,
  "jumlah_trade_luar_sampel": 135681,
  "total_R": 8091.518867912968,
  "ekspektasi_R": 0.05963634457229065
}
alasan keluar: {'stop': 101417, 'umur': 9699, 'target': 21658, 'akhir_data': 2479, 'carry': 428}
entri ditolak pengaman biaya: 62 (pengaman 0.5R, lantai semesta 0.004)
bulan dengan perdagangan: 73
parameter terpilih: {'{"imbalan_R": 8.0, "lookback": 20}': 574, '{"imbalan_R": 6.0, "lookback": 100}': 408, '{"imbalan_R": 8.0, "lookback": 100}': 655, '{"imbalan_R": 8.0, "lookback": 55}': 496, '{"imbalan_R": 6.0, "lookback": 55}': 325, '{"imbalan_R": 4.0, "lookback": 55}': 180, '{"imbalan_R": 2.0, "lookback": 55}': 97, '{"imbalan_R": 6.0, "lookback": 20}': 434, '{"imbalan_R": 2.0, "lookback": 20}': 252, '{"imbalan_R": 4.0, "lookback": 100}': 221, '{"imbalan_R": 4.0, "lookback": 20}': 347, '{"imbalan_R": 2.0, "lookback": 100}': 92}
konsentrasi: 306 untung / 131 rugi dari 437 simbol; drop-1 0.05873R (retensi 0.9849), drop-22 0.04497R, median simbol +0.06285R, porsi bruto teratas 0.0142 (FLMUSDT), setara 174.3 simbol
funding ekor: porsi ekor maks 0.1693 (rerata 0.0988 atas 10 terburuk), funding maks 0.6601R, 430 dari 135681 trade di atas pengaman (0.00317); gagal: funding_maks_R
sebaran: std 2.22746R, galat baku 0.006047R, jarak ke ambang +0.009636R = +1.59 galat baku
entri acak: nyata 0.04661R, p 0.06312292358803986

=== KRITERIA UTAMA ADR-014: PERIODE WAKTU TERTAHAN ===
tahan (sejak 2026-01): 7 bulan, 22,117 trade, total 922.56R, ekspektasi 0.04171275623950187
sebelum: 66 bulan, 113,564 trade, total 7168.96R, ekspektasi 0.06312702826744307
selisih tahan - sebelum: -0.021414R
kriteria utama terhadap 0.05R dengan minimal 100 trade: GAGAL (ramalan saya: GAGAL, 0,010-0,045)
catatan kejujuran: periode ini tidak sebersih himpunan simbol tertahan sebelum H-011. Riwayat yang sudah dilihat memuat periode ini di dalam agregatnya; yang belum pernah dilihat adalah angkanya secara terpisah. Perdagangan yang dibuka sesaat sebelum batas dapat ditutup sesudahnya, dan rembesan itu terbatas oleh maks_umur_bar (168 bar).

putusan seluruh kumpulan: False
ekspektasi seluruh riwayat: 0.05963634457229065 (H-010 0.05302836360569971; angka ini HANYA pemeriksaan konsistensi, bukan bukti)
trade: 135,681
p entri acak: 0.06312292358803986 (mekanisme ini: 0.0631 pada 300 permutasi di H-010)
entri ditolak pengaman: 62
simbol dibuang lantai: ['USDCUSDT']
bulan dengan trade: 73
retensi drop-1: 0.9848579853627102
galat baku: 0.006047141981068382
jarak ke ambang dalam galat baku: 1.5935370134286386
gerbang gagal: ['entri_acak', 'invarian_risiko', 'funding_ekor']
durasi: 1220.6s
```
