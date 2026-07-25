# Laporan pengujian

Commit: `4e67e0bdadbda7eebf935ec2ce14cf1683981a77`
Kode keluar: `2`

```

==================================== ERRORS ====================================
__________________ ERROR collecting tests/test_diag_datar.py ___________________
ImportError while importing test module '/home/runner/work/lux-research/lux-research/tests/test_diag_datar.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_diag_datar.py:18: in <module>
    from lux.diag_datar import _deret, blok_datar, letak, letak_blok, ringkas_simbol
lux/diag_datar.py:50: in <module>
    from lux.backtest.run_wf import pilih_berkas
lux/backtest/run_wf.py:74: in <module>
    from lux.potong_ekor import potong as _potong_ekor
lux/potong_ekor.py:34: in <module>
    from lux.diag_datar import KOLOM_BACA, blok_datar, tanggal
E   ImportError: cannot import name 'KOLOM_BACA' from partially initialized module 'lux.diag_datar' (most likely due to a circular import) (/home/runner/work/lux-research/lux-research/lux/diag_datar.py)
___________________ ERROR collecting tests/test_diagnosa.py ____________________
ImportError while importing test module '/home/runner/work/lux-research/lux-research/tests/test_diagnosa.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_diagnosa.py:11: in <module>
    from lux.backtest.run_wf import diagnosa_biaya, rincian_R
lux/backtest/run_wf.py:74: in <module>
    from lux.potong_ekor import potong as _potong_ekor
lux/potong_ekor.py:34: in <module>
    from lux.diag_datar import KOLOM_BACA, blok_datar, tanggal
lux/diag_datar.py:50: in <module>
    from lux.backtest.run_wf import pilih_berkas
E   ImportError: cannot import name 'pilih_berkas' from partially initialized module 'lux.backtest.run_wf' (most likely due to a circular import) (/home/runner/work/lux-research/lux-research/lux/backtest/run_wf.py)
__________________ ERROR collecting tests/test_potong_ekor.py __________________
ImportError while importing test module '/home/runner/work/lux-research/lux-research/tests/test_potong_ekor.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_potong_ekor.py:13: in <module>
    from lux.potong_ekor import ekor_datar, evaluasi, potong, rasio_datar
lux/potong_ekor.py:34: in <module>
    from lux.diag_datar import KOLOM_BACA, blok_datar, tanggal
lux/diag_datar.py:50: in <module>
    from lux.backtest.run_wf import pilih_berkas
lux/backtest/run_wf.py:74: in <module>
    from lux.potong_ekor import potong as _potong_ekor
E   ImportError: cannot import name 'potong' from partially initialized module 'lux.potong_ekor' (most likely due to a circular import) (/home/runner/work/lux-research/lux-research/lux/potong_ekor.py)
____________________ ERROR collecting tests/test_run_wf.py _____________________
ImportError while importing test module '/home/runner/work/lux-research/lux-research/tests/test_run_wf.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_run_wf.py:25: in <module>
    from lux.backtest.run_wf import (
lux/backtest/run_wf.py:74: in <module>
    from lux.potong_ekor import potong as _potong_ekor
lux/potong_ekor.py:34: in <module>
    from lux.diag_datar import KOLOM_BACA, blok_datar, tanggal
lux/diag_datar.py:50: in <module>
    from lux.backtest.run_wf import pilih_berkas
E   ImportError: cannot import name 'pilih_berkas' from partially initialized module 'lux.backtest.run_wf' (most likely due to a circular import) (/home/runner/work/lux-research/lux-research/lux/backtest/run_wf.py)
=========================== short test summary info ============================
ERROR tests/test_diag_datar.py
ERROR tests/test_diagnosa.py
ERROR tests/test_potong_ekor.py
ERROR tests/test_run_wf.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
4 errors in 0.90s
```
