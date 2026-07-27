# Laporan pengujian

Commit: `4e6a65845e99f819021a22703dd6e503fd933924`
Kode keluar: `1`

```
........................................................................ [  7%]
........................................................................ [ 15%]
........................................................................ [ 22%]
........................................................................ [ 30%]
........................................................................ [ 38%]
........................................................................ [ 45%]
........................................................................ [ 53%]
........................................................................ [ 61%]
........................................................................ [ 68%]
.................................................FF...............F..... [ 76%]
........................................................................ [ 84%]
........................................................................ [ 91%]
........................................................................ [ 99%]
....                                                                     [100%]
=================================== FAILURES ===================================
_______________ test_audit_tidak_menghalangi_saat_pengaman_hidup _______________
tests/test_run_h015.py:67: in test_audit_tidak_menghalangi_saat_pengaman_hidup
    assert lap["pengaman_mati"] == []
E   AssertionError: assert ['maks_carry_R'] == []
E     
E     Left contains one more item: 'maks_carry_R'
E     
E     Full diff:
E     - []
E     + [
E     +     'maks_carry_R',
E     + ]
________________ test_audit_menghalangi_saat_pengaman_dimatikan ________________
tests/test_run_h015.py:75: in test_audit_menghalangi_saat_pengaman_dimatikan
    assert lap["pengaman_mati"] == ["maks_carry_realisasi_R"]
E   AssertionError: assert ['maks_carry_..._realisasi_R'] == ['maks_carry_realisasi_R']
E     
E     At index 0 diff: 'maks_carry_R' != 'maks_carry_realisasi_R'
E     Left contains one more item: 'maks_carry_realisasi_R'
E     
E     Full diff:
E       [
E     +     'maks_carry_R',
E           'maks_carry_realisasi_R',
E       ]
______________________ test_lulus_besaran_tepat_di_ambang ______________________
tests/test_run_h015.py:168: in test_lulus_besaran_tepat_di_ambang
    assert r["lulus"] is True
E   assert False is True
=========================== short test summary info ============================
FAILED tests/test_run_h015.py::test_audit_tidak_menghalangi_saat_pengaman_hidup - AssertionError: assert ['maks_carry_R'] == []
  
  Left contains one more item: 'maks_carry_R'
  
  Full diff:
  - []
  + [
  +     'maks_carry_R',
  + ]
FAILED tests/test_run_h015.py::test_audit_menghalangi_saat_pengaman_dimatikan - AssertionError: assert ['maks_carry_..._realisasi_R'] == ['maks_carry_realisasi_R']
  
  At index 0 diff: 'maks_carry_R' != 'maks_carry_realisasi_R'
  Left contains one more item: 'maks_carry_realisasi_R'
  
  Full diff:
    [
  +     'maks_carry_R',
        'maks_carry_realisasi_R',
    ]
FAILED tests/test_run_h015.py::test_lulus_besaran_tepat_di_ambang - assert False is True
3 failed, 937 passed in 3.34s
```
