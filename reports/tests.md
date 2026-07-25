# Laporan pengujian

Commit: `f465f7f16e1d7028bb34f307d412d91aaa669e20`
Kode keluar: `1`

```
......................F................................................. [ 51%]
...................................................................      [100%]
=================================== FAILURES ===================================
__________ test_stop_menang_saat_stop_dan_target_sama_sama_tersentuh ___________
tests/test_engine.py:99: in test_stop_menang_saat_stop_dan_target_sama_sama_tersentuh
    assert hasil.jumlah_trade == 1
E   AssertionError: assert 0 == 1
E    +  where 0 = Hasil(symbol='', perdagangan=[], ekuitas=array([10000.   , 10000.   , 10000.   , 10000.   , 10000.   , 10000.   ,\n    ...600064800000, 1600068400000,\n       1600072000000, 1600075600000, 1600079200000, 1600082800000,\n       1600086400000])).jumlah_trade
=========================== short test summary info ============================
FAILED tests/test_engine.py::test_stop_menang_saat_stop_dan_target_sama_sama_tersentuh - AssertionError: assert 0 == 1
 +  where 0 = Hasil(symbol='', perdagangan=[], ekuitas=array([10000.   , 10000.   , 10000.   , 10000.   , 10000.   , 10000.   ,\n    ...600064800000, 1600068400000,\n       1600072000000, 1600075600000, 1600079200000, 1600082800000,\n       1600086400000])).jumlah_trade
1 failed, 138 passed in 1.04s
```
