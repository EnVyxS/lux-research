"""Runner wajib mengambil jalur manifest dari jalur_manifest (ADR-025 langkah 2).

Dua uji pertama adalah **tripwire tekstual**, dan kelemahannya dinyatakan di sini
alih-alih disembunyikan: keduanya menjaga baris pemanggilan, bukan perilaku
berkasnya. Alasannya sama seperti ``tests/test_runner_interval.py`` —
``muat_konteks`` menuntut parquet, jadwal funding, dan semesta supaya berjalan,
jadi mengujinya secara utuh di sini berarti membangun separuh pipeline di dalam
berkas uji.

Yang dijaga: nama berkas yang dipatok tidak boleh kembali diam-diam, karena
bentuk itulah yang membuat gerbang ``checksum`` tidak mungkin lulus pada interval
selain 1h.
"""

from __future__ import annotations

import inspect
from pathlib import Path

from lux.backtest import runner
from lux.backtest.manifest import jalur_manifest


def test_muat_konteks_memakai_jalur_manifest():
    sumber = inspect.getsource(runner.muat_konteks)
    assert "jalur_manifest(opsi.interval, opsi.out)" in sumber
    # Bentuk lama: satu nama tetap untuk semua interval. Itu cacat kelas
    # kesebelas dan tidak boleh kembali.
    assert 'Path(opsi.out) / "manifest_aset.json"' not in sumber


def test_runner_mengimpor_jalur_manifest_bukan_menyalinnya():
    assert runner.jalur_manifest is jalur_manifest
    sumber = inspect.getsource(runner)
    assert "from lux.backtest.manifest import jalur_manifest" in sumber


def test_jalur_1h_tetap_berkas_warisan():
    # Ini yang membuat jalur 1h bit-identik: opsi bawaan menunjuk berkas yang
    # sama persis dengan yang dipakai sebelas hipotesis lama.
    opsi = runner.Opsi(dir_aset=Path("aset"))
    assert opsi.interval == "1h"
    assert jalur_manifest(opsi.interval, opsi.out) == Path(
        "reports/manifest_aset.json"
    )
    assert jalur_manifest("4h", opsi.out) == Path(
        "reports/manifest_aset_4h.json"
    )
