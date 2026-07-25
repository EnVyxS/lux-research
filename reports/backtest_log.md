# Log run backtest

Commit: `11d698cffe45a4268ff6e7926b7164afde2297e3`
Status langkah jalan: `failure`

```
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/home/runner/work/lux-research/lux-research/lux/backtest/run_wf.py", line 797, in <module>
    sys.exit(main())
             ^^^^^^
  File "/home/runner/work/lux-research/lux-research/lux/backtest/run_wf.py", line 439, in main
    jalur = simpan(h, a.hipotesis)
            ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/lux-research/lux-research/lux/praregistrasi.py", line 119, in simpan
    raise ValueError(
ValueError: hipotesis H-001 sudah terdaftar dengan isi berbeda; buat id baru alih-alih menyunting yang lama
```
