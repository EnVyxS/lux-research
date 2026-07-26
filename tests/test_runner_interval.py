"""Runner wajib memasok interval ke gerbang forward_fill (ADR-019 langkah 3b).

Uji pertama adalah **tripwire tekstual** dan kelemahannya dinyatakan di sini
alih-alih disembunyikan: ia menjaga baris pemanggilan, bukan perilaku gerbangnya.
Alasan memilih bentuk lemah ini adalah ``jalankan_spek`` menuntut dataset parquet,
jadwal funding, dan manifest aset supaya berjalan, sehingga menguji perilakunya
di sini berarti membangun separuh pipeline di dalam berkas uji. Perilaku
gerbangnya sendiri sudah diuji enam kali di ``tests/test_forward_fill_interval.py``.

Yang dijaga tripwire ini persis satu hal: seseorang — termasuk saya di sesi
berikutnya — tidak boleh mengembalikan pemanggilan itu menjadi tanpa argumen dan
lolos hijau.
"""

from __future__ import annotations

import inspect
from pathlib import Path

from lux.backtest import runner
from lux.kerangka import bar_per_hari


def test_jalankan_spek_memasok_interval_ke_gerbang_forward_fill():
    sumber = inspect.getsource(runner.jalankan_spek)
    assert "gerbang_forward_fill(df, interval=opsi.interval)" in sumber
    # Bentuk tanpa argumen adalah cacat yang diperbaiki ADR-019; ia tidak boleh
    # kembali diam-diam.
    assert "gerbang_forward_fill(df)" not in sumber


def test_interval_bawaan_opsi_memberi_ambang_dua_puluh_empat():
    # Ini yang membuat jalur 1h bit-identik: bawaan Opsi menghasilkan ambang yang
    # sama persis dengan bawaan lama gerbang, yakni 24.
    opsi = runner.Opsi(dir_aset=Path("aset"))
    assert opsi.interval == "1h"
    assert bar_per_hari(opsi.interval) == 24
