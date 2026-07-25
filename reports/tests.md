# Laporan pengujian

Commit: `42fdae205cf7ad566eea33a12825da283186741c`
Kode keluar: `1`

```
.............................................FF.......                   [100%]
=================================== FAILURES ===================================
______________ test_median_harian_dihitung_per_hari_bukan_per_bar ______________
tests/test_validate.py:148: in test_median_harian_dihitung_per_hari_bukan_per_bar
    assert median == pytest.approx(24_000.0)
E   assert 12000.0 == 24000.0 ± 0.024
E     
E     comparison failed
E     Obtained: 12000.0
E     Expected: 24000.0 ± 0.024
_________________ test_median_tahan_terhadap_satu_hari_ekstrem _________________
tests/test_validate.py:156: in test_median_tahan_terhadap_satu_hari_ekstrem
    assert median == pytest.approx(24_000.0)
E   assert 60012000.0 == 24000.0 ± 0.024
E     
E     comparison failed
E     Obtained: 60012000.0
E     Expected: 24000.0 ± 0.024
=========================== short test summary info ============================
FAILED tests/test_validate.py::test_median_harian_dihitung_per_hari_bukan_per_bar - assert 12000.0 == 24000.0 ± 0.024
  
  comparison failed
  Obtained: 12000.0
  Expected: 24000.0 ± 0.024
FAILED tests/test_validate.py::test_median_tahan_terhadap_satu_hari_ekstrem - assert 60012000.0 == 24000.0 ± 0.024
  
  comparison failed
  Obtained: 60012000.0
  Expected: 24000.0 ± 0.024
2 failed, 52 passed in 0.89s
```
