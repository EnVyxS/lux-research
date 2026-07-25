# Laporan pengujian

Commit: `de72d67f238fcc7a8d88433b32db30d5bfc5d13e`
Kode keluar: `1`

```
...........................F............................................ [ 98%]
.                                                                        [100%]
=================================== FAILURES ===================================
______________________ test_berkas_kosong_tidak_melempar _______________________
tests/test_funding.py:127: in test_berkas_kosong_tidak_melempar
    df = baca_zip(p)
         ^^^^^^^^^^^
lux/funding.py:87: in baca_zip
    df = pd.read_csv(
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/site-packages/pandas/io/parsers/readers.py:1026: in read_csv
    return _read(filepath_or_buffer, kwds)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/site-packages/pandas/io/parsers/readers.py:620: in _read
    parser = TextFileReader(filepath_or_buffer, **kwds)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/site-packages/pandas/io/parsers/readers.py:1620: in __init__
    self._engine = self._make_engine(f, self.engine)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/site-packages/pandas/io/parsers/readers.py:1898: in _make_engine
    return mapping[engine](f, **self.options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/site-packages/pandas/io/parsers/c_parser_wrapper.py:93: in __init__
    self._reader = parsers.TextReader(src, **kwds)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
parsers.pyx:581: in pandas._libs.parsers.TextReader.__cinit__
    ???
E   pandas.errors.EmptyDataError: No columns to parse from file
=========================== short test summary info ============================
FAILED tests/test_funding.py::test_berkas_kosong_tidak_melempar - pandas.errors.EmptyDataError: No columns to parse from file
1 failed, 72 passed in 1.02s
```
