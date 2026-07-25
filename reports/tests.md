# Laporan pengujian

Commit: `5f222e8a13f65e0a39f82f838062e57aee7b5ac1`
Kode keluar: `1`

```
E   FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pytest-of-runner/pytest-0/test_jumlah_baris_sama_dengan_0/a/arsip.zip'
__________________ test_rasio_1h_terhadap_4h_mendekati_empat ___________________
tests/test_ingest.py:84: in test_rasio_1h_terhadap_4h_mendekati_empat
    df1 = baca_zip(buat_zip(tmp_path / "h1", HEADER + "\n" + satu_jam))
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_ingest.py:39: in buat_zip
    with zipfile.ZipFile(path, "w") as z:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/zipfile/__init__.py:1352: in __init__
    self.fp = io.open(file, filemode)
              ^^^^^^^^^^^^^^^^^^^^^^^
E   FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pytest-of-runner/pytest-0/test_rasio_1h_terhadap_4h_mend0/h1/arsip.zip'
_____________ test_baris_sampah_dibuang_bukan_menggagalkan_berkas ______________
parsers.pyx:1161: in pandas._libs.parsers.TextReader._convert_tokens
    ???
E   TypeError: Cannot cast array data from dtype('O') to dtype('float64') according to the rule 'safe'

During handling of the above exception, another exception occurred:
tests/test_ingest.py:117: in test_baris_sampah_dibuang_bukan_menggagalkan_berkas
    df = baca_zip(buat_zip(tmp_path, data))
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
lux/ingest.py:98: in baca_zip
    df = pd.read_csv(
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/site-packages/pandas/io/parsers/readers.py:1026: in read_csv
    return _read(filepath_or_buffer, kwds)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/site-packages/pandas/io/parsers/readers.py:626: in _read
    return parser.read(nrows)
           ^^^^^^^^^^^^^^^^^^
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/site-packages/pandas/io/parsers/readers.py:1923: in read
    ) = self._engine.read(  # type: ignore[attr-defined]
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/site-packages/pandas/io/parsers/c_parser_wrapper.py:234: in read
    chunks = self._reader.read_low_memory(nrows)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
parsers.pyx:838: in pandas._libs.parsers.TextReader.read_low_memory
    ???
parsers.pyx:921: in pandas._libs.parsers.TextReader._read_rows
    ???
parsers.pyx:1066: in pandas._libs.parsers.TextReader._convert_column_data
    ???
parsers.pyx:1167: in pandas._libs.parsers.TextReader._convert_tokens
    ???
E   ValueError: could not convert string to float: 'angka'
_____________ test_encoding_utf8_bom_tidak_merusak_deteksi_header ______________
parsers.pyx:1161: in pandas._libs.parsers.TextReader._convert_tokens
    ???
E   TypeError: Cannot cast array data from dtype('O') to dtype('float64') according to the rule 'safe'

During handling of the above exception, another exception occurred:
tests/test_ingest.py:136: in test_encoding_utf8_bom_tidak_merusak_deteksi_header
    df = baca_zip(buat_zip(tmp_path, isi))
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
lux/ingest.py:98: in baca_zip
    df = pd.read_csv(
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/site-packages/pandas/io/parsers/readers.py:1026: in read_csv
    return _read(filepath_or_buffer, kwds)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/site-packages/pandas/io/parsers/readers.py:626: in _read
    return parser.read(nrows)
           ^^^^^^^^^^^^^^^^^^
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/site-packages/pandas/io/parsers/readers.py:1923: in read
    ) = self._engine.read(  # type: ignore[attr-defined]
/opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/site-packages/pandas/io/parsers/c_parser_wrapper.py:234: in read
    chunks = self._reader.read_low_memory(nrows)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
parsers.pyx:838: in pandas._libs.parsers.TextReader.read_low_memory
    ???
parsers.pyx:921: in pandas._libs.parsers.TextReader._read_rows
    ???
parsers.pyx:1066: in pandas._libs.parsers.TextReader._convert_column_data
    ???
parsers.pyx:1167: in pandas._libs.parsers.TextReader._convert_tokens
    ???
E   ValueError: could not convert string to float: 'open'
=========================== short test summary info ============================
FAILED tests/test_ingest.py::test_jumlah_baris_sama_dengan_dan_tanpa_header - FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pytest-of-runner/pytest-0/test_jumlah_baris_sama_dengan_0/a/arsip.zip'
FAILED tests/test_ingest.py::test_rasio_1h_terhadap_4h_mendekati_empat - FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pytest-of-runner/pytest-0/test_rasio_1h_terhadap_4h_mend0/h1/arsip.zip'
FAILED tests/test_ingest.py::test_baris_sampah_dibuang_bukan_menggagalkan_berkas - ValueError: could not convert string to float: 'angka'
FAILED tests/test_ingest.py::test_encoding_utf8_bom_tidak_merusak_deteksi_header - ValueError: could not convert string to float: 'open'
4 failed, 24 passed in 0.78s
```
