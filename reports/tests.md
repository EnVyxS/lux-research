# Laporan pengujian

Commit: `7a0c416d5de6ae47473bcb83e3416081c04de7f1`
Kode keluar: `1`

```
...........F..                                                           [100%]
=================================== FAILURES ===================================
______________ test_stop_sangat_sempit_membuat_strategi_mustahil _______________
tests/test_costs.py:85: in test_stop_sangat_sempit_membuat_strategi_mustahil
    assert winrate_impas(2.0, biaya) > 1.0
E   assert 1.0 > 1.0
E    +  where 1.0 = winrate_impas(2.0, 2.0)
=========================== short test summary info ============================
FAILED tests/test_costs.py::test_stop_sangat_sempit_membuat_strategi_mustahil - assert 1.0 > 1.0
 +  where 1.0 = winrate_impas(2.0, 2.0)
1 failed, 13 passed in 0.04s
```
