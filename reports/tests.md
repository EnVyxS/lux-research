# Laporan pengujian

Commit: `499c64c7fe961cf02b0d97b5a5508f9306363b15`
Kode keluar: `1`

```
........................................................................ [  7%]
........................................................................ [ 15%]
........................................................................ [ 23%]
........................................................................ [ 31%]
........................................................................ [ 39%]
........................................................................ [ 47%]
........................................................................ [ 55%]
........................................................................ [ 63%]
........................................................................ [ 71%]
........................................................................ [ 79%]
..............................................FFF....................... [ 87%]
........................................................................ [ 95%]
.........................................                                [100%]
=================================== FAILURES ===================================
_________________ test_sel_f_menolak_long_saat_funding_positif _________________
tests/test_saringan_funding.py:245: in test_sel_f_menolak_long_saat_funding_positif
    assert f(bingkai(), {}).tolist() == [0] * 6
           ^^^^^^^^^^^^^^^^
lux/backtest/saringan_funding.py:294: in bungkus
    jadwal = ambil_jadwal(jadwal_semua, simbol)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
lux/funding_model.py:199: in ambil_jadwal
    if j is None or len(j) == 0:
                    ^^^^^^
E   TypeError: object of type 'JadwalBoneka' has no len()
_______________ test_sel_f_meloloskan_short_saat_funding_positif _______________
tests/test_saringan_funding.py:251: in test_sel_f_meloloskan_short_saat_funding_positif
    assert f(bingkai(), {}).tolist() == [-1] * 6
           ^^^^^^^^^^^^^^^^
lux/backtest/saringan_funding.py:294: in bungkus
    jadwal = ambil_jadwal(jadwal_semua, simbol)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
lux/funding_model.py:199: in ambil_jadwal
    if j is None or len(j) == 0:
                    ^^^^^^
E   TypeError: object of type 'JadwalBoneka' has no len()
_______________ test_sel_a_membuang_cacah_yang_sama_dengan_sel_f _______________
tests/test_saringan_funding.py:257: in test_sel_a_membuang_cacah_yang_sama_dengan_sel_f
    n_f = int((sinyal_sel("F", j, dasar_tetap(1))(df, {}) == 0).sum())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
lux/backtest/saringan_funding.py:294: in bungkus
    jadwal = ambil_jadwal(jadwal_semua, simbol)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
lux/funding_model.py:199: in ambil_jadwal
    if j is None or len(j) == 0:
                    ^^^^^^
E   TypeError: object of type 'JadwalBoneka' has no len()
=========================== short test summary info ============================
FAILED tests/test_saringan_funding.py::test_sel_f_menolak_long_saat_funding_positif - TypeError: object of type 'JadwalBoneka' has no len()
FAILED tests/test_saringan_funding.py::test_sel_f_meloloskan_short_saat_funding_positif - TypeError: object of type 'JadwalBoneka' has no len()
FAILED tests/test_saringan_funding.py::test_sel_a_membuang_cacah_yang_sama_dengan_sel_f - TypeError: object of type 'JadwalBoneka' has no len()
3 failed, 902 passed in 3.39s
```
