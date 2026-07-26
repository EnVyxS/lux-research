# Laporan pengujian

Commit: `3880408fabaf73947c966ac6ab32d39effb07e27`
Kode keluar: `1`

```
........................................................................ [ 11%]
........................................................................ [ 22%]
........................................................................ [ 33%]
........................................................................ [ 44%]
.................F...................................................... [ 56%]
........................................................................ [ 67%]
........................................................................ [ 78%]
........................................................................ [ 89%]
..................................................................       [100%]
=================================== FAILURES ===================================
_________________ test_main_mengirim_satu_baris_tanpa_jaringan _________________
tests/test_notion_reporter_cli.py:61: in test_main_mengirim_satu_baris_tanpa_jaringan
    kode = pelapor.main(
lux/notion_reporter.py:286: in main
    kode, teks = kirim(payload_baris(db, properti), pengirim=pengirim)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
lux/notion_reporter.py:223: in kirim
    raise GalatPelapor(
E   lux.notion_reporter.GalatPelapor: NOTION_TOKEN tidak tersedia; baris hasil tidak dikirim
=========================== short test summary info ============================
FAILED tests/test_notion_reporter_cli.py::test_main_mengirim_satu_baris_tanpa_jaringan - lux.notion_reporter.GalatPelapor: NOTION_TOKEN tidak tersedia; baris hasil tidak dikirim
1 failed, 641 passed in 2.46s
```
