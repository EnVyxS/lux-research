"""Manifest aset wajib punya satu berkas per interval (ADR-025).

Empat uji pertama mengunci pemetaan namanya, dua berikutnya mengunci penolakan
masukan yang cacat, dan tiga terakhir mengunci hal yang paling mudah hilang di
sesi berikutnya: bahwa jalur 1h **tidak** berubah nama, sehingga manifest 1h yang
sudah dikomit tetap menjadi rujukan keutuhan sebelas hipotesis lama.

Uji perilaku ``muat_konteks`` sendiri tidak ada di sini dan itu dinyatakan
terbuka: ``muat_konteks`` menuntut parquet, jadwal funding, dan semesta supaya
berjalan, jadi mengujinya di sini berarti membangun separuh pipeline di dalam
berkas uji. Penyambungannya diuji sebagai tripwire tekstual di langkah 2, dengan
kelemahan yang sama seperti ``tests/test_runner_interval.py``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from lux.backtest.manifest import (
    INTERVAL_WARISAN,
    NAMA_DASAR,
    jalur_manifest,
)


def test_satu_jam_memakai_nama_warisan_tanpa_akhiran():
    # Inilah syarat keterulangan: berkas ini sudah dikomit dan menjadi bukti
    # keutuhan data di balik sebelas hipotesis pertama.
    assert jalur_manifest("1h") == Path("reports/manifest_aset.json")
    assert INTERVAL_WARISAN == "1h"
    assert NAMA_DASAR == "manifest_aset"


def test_empat_jam_memakai_nama_sendiri():
    assert jalur_manifest("4h") == Path("reports/manifest_aset_4h.json")


def test_interval_lain_mengikuti_pola_yang_sama():
    assert jalur_manifest("1d") == Path("reports/manifest_aset_1d.json")
    assert jalur_manifest("15m") == Path("reports/manifest_aset_15m.json")


def test_direktori_keluaran_dihormati(tmp_path: Path):
    assert jalur_manifest("4h", tmp_path) == tmp_path / "manifest_aset_4h.json"
    assert jalur_manifest("1h", str(tmp_path)) == tmp_path / "manifest_aset.json"


def test_interval_kosong_ditolak_keras():
    # Jatuh diam-diam ke nama 1h akan menulis checksum interval lain ke dalam
    # berkas rujukan hasil 1h. Itu merusak bukti yang sedang dijaga.
    for buruk in ("", "   ", None):
        with pytest.raises(ValueError):
            jalur_manifest(buruk)  # type: ignore[arg-type]


def test_interval_dengan_pemisah_jalur_ditolak():
    for buruk in ("../1h", "a/b", "a\\b", ".", ".."):
        with pytest.raises(ValueError):
            jalur_manifest(buruk)


def test_spasi_di_tepi_dipangkas_bukan_dijadikan_nama_baru():
    assert jalur_manifest(" 4h ") == jalur_manifest("4h")
    assert jalur_manifest(" 1h ") == Path("reports/manifest_aset.json")


def test_setiap_interval_mendapat_berkas_yang_berbeda():
    jalur = {
        jalur_manifest(iv) for iv in ("1h", "4h", "1d", "15m", "5m")
    }
    assert len(jalur) == 5, "dua interval berbagi satu manifest = gerbang buta"


def test_nama_warisan_tidak_pernah_dipakai_interval_lain():
    warisan = Path("reports/manifest_aset.json")
    for iv in ("4h", "1d", "15m", "5m", "30m", "2h", "8h", "1w"):
        assert jalur_manifest(iv) != warisan
