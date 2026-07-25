# Laporan pengujian

Commit: `4886ff18bd621f949466a1b8877aa1f3957c666a`
Kode keluar: `1`

```
.......................F................................................ [ 28%]
........................................................................ [ 57%]
........................................................................ [ 86%]
...................................                                      [100%]
=================================== FAILURES ===================================
_____________ test_blok_yang_menempel_di_akhir_riwayat_tertangkap ______________
tests/test_diag_datar.py:90: in test_blok_yang_menempel_di_akhir_riwayat_tertangkap
    assert letak(blok[0]["posisi_frac"]) == "akhir"
E   AssertionError: assert 'tengah' == 'akhir'
E     
E     - akhir
E     + tengah
=========================== short test summary info ============================
FAILED tests/test_diag_datar.py::test_blok_yang_menempel_di_akhir_riwayat_tertangkap - AssertionError: assert 'tengah' == 'akhir'
  
  - akhir
  + tengah
1 failed, 250 passed in 1.57s
```
