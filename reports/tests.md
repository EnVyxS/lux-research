# Laporan pengujian

Commit: `bac1818e2626b618684e2ea3cfb7cac0a98cc9f0`
Kode keluar: `1`

```
................................................F....................... [ 72%]
............................                                             [100%]
=================================== FAILURES ===================================
______________ test_jarak_tiga_jam_dihitung_sebagai_tidak_selaras ______________
tests/test_funding_check.py:97: in test_jarak_tiga_jam_dihitung_sebagai_tidak_selaras
    assert tidak_selaras(t) == 2
E   assert 1 == 2
E    +  where 1 = tidak_selaras(0    1599984000000\n1    1599994800000\n2    1600009200000\ndtype: int64)
=========================== short test summary info ============================
FAILED tests/test_funding_check.py::test_jarak_tiga_jam_dihitung_sebagai_tidak_selaras - assert 1 == 2
 +  where 1 = tidak_selaras(0    1599984000000\n1    1599994800000\n2    1600009200000\ndtype: int64)
1 failed, 99 passed in 1.06s
```
