# Laporan pengujian

Commit: `a911e99e40f205776d3899ff0b0a9b4e5607783f`
Kode keluar: `1`

```
E   AssertionError: assert {'n': 5, 'dap...99999997, ...} == {'n': 5, 'dap...R': 0.28, ...}
E     
E     Omitting 8 identical items, use -vv to show
E     Differing items:
E     {'rerata_R': 0.27999999999999997} != {'rerata_R': 0.28}
E     {'ci95_atas_R': 1.448441040393007} != {'ci95_atas_R': 1.4484410403930068}
E     {'std_R': 1.333041634758645} != {'std_R': 1.3330416347586447}
E     {'galat_baku_R': 0.5961543424315553} != {'galat_baku_R': 0.5961543424315552}
E     {'ci95_bawah_R': -0.888441040393007} != {'ci95_bawah_R': -0.8884410403930068}
E     
E     Full diff:
E       {
E           'n': 5,
E           'dapat_dinilai': True,
E           'sebab': '',
E     -     'rerata_R': 0.28,
E     +     'rerata_R': 0.27999999999999997,
E     -     'std_R': 1.3330416347586447,
E     ?                              ^^
E     +     'std_R': 1.333041634758645,
E     ?                              ^
E     -     'galat_baku_R': 0.5961543424315552,
E     ?                                      ^
E     +     'galat_baku_R': 0.5961543424315553,
E     ?                                      ^
E           'min_R': -1.0,
E           'q1_R': -0.4,
E           'median_R': 0.0,
E           'q3_R': 0.3,
E           'maks_R': 2.5,
E     -     'ci95_bawah_R': -0.8884410403930068,
E     ?                                      ^^
E     +     'ci95_bawah_R': -0.888441040393007,
E     ?                                      ^
E     -     'ci95_atas_R': 1.4484410403930068,
E     ?                                    ^^
E     +     'ci95_atas_R': 1.448441040393007,
E     ?                                    ^
E       }
=========================== short test summary info ============================
FAILED tests/test_sebaran.py::test_urutan_masukan_tidak_mengubah_hasil - AssertionError: assert {'n': 5, 'dap...99999997, ...} == {'n': 5, 'dap...R': 0.28, ...}
  
  Omitting 8 identical items, use -vv to show
  Differing items:
  {'rerata_R': 0.27999999999999997} != {'rerata_R': 0.28}
  {'ci95_atas_R': 1.448441040393007} != {'ci95_atas_R': 1.4484410403930068}
  {'std_R': 1.333041634758645} != {'std_R': 1.3330416347586447}
  {'galat_baku_R': 0.5961543424315553} != {'galat_baku_R': 0.5961543424315552}
  {'ci95_bawah_R': -0.888441040393007} != {'ci95_bawah_R': -0.8884410403930068}
  
  Full diff:
    {
        'n': 5,
        'dapat_dinilai': True,
        'sebab': '',
  -     'rerata_R': 0.28,
  +     'rerata_R': 0.27999999999999997,
  -     'std_R': 1.3330416347586447,
  ?                              ^^
  +     'std_R': 1.333041634758645,
  ?                              ^
  -     'galat_baku_R': 0.5961543424315552,
  ?                                      ^
  +     'galat_baku_R': 0.5961543424315553,
  ?                                      ^
        'min_R': -1.0,
        'q1_R': -0.4,
        'median_R': 0.0,
        'q3_R': 0.3,
        'maks_R': 2.5,
  -     'ci95_bawah_R': -0.8884410403930068,
  ?                                      ^^
  +     'ci95_bawah_R': -0.888441040393007,
  ?                                      ^
  -     'ci95_atas_R': 1.4484410403930068,
  ?                                    ^^
  +     'ci95_atas_R': 1.448441040393007,
  ?                                    ^
    }
1 failed, 524 passed in 2.13s
```
