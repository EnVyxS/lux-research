"""Pengujian pemilihan berkas aset.

Aturan ini lahir dari kejadian nyata: aset `_retry` pra-perbaikan parser masih
tergeletak di Release, ikut tertangkap pola unduhan, dan membuat tiga simbol
terhitung dua kali sebagai 12.593 duplikat yang tampak seperti data rusak.
"""

from __future__ import annotations

from pathlib import Path

from lux.validate_run import pilih_berkas


def sentuh(direktori: Path, *nama: str) -> None:
    for n in nama:
        (direktori / n).write_bytes(b"")


def test_shard_bulanan_dan_ekor_ikut_terpilih(tmp_path):
    sentuh(
        tmp_path,
        "ohlcv_1h_shard00.parquet",
        "ohlcv_1h_shard07.parquet",
        "ohlcv_1h_tail_shard00.parquet",
    )
    nama = [p.name for p in pilih_berkas(tmp_path, "1h")]
    assert len(nama) == 3
    assert "ohlcv_1h_tail_shard00.parquet" in nama


def test_aset_retry_usang_ditolak(tmp_path):
    sentuh(
        tmp_path,
        "ohlcv_1h_shard00.parquet",
        "ohlcv_1h_shard00_retry.parquet",
    )
    nama = [p.name for p in pilih_berkas(tmp_path, "1h")]
    assert nama == ["ohlcv_1h_shard00.parquet"]


def test_interval_lain_tidak_ikut_terbaca(tmp_path):
    sentuh(tmp_path, "ohlcv_1h_shard00.parquet", "ohlcv_4h_shard00.parquet")
    nama = [p.name for p in pilih_berkas(tmp_path, "4h")]
    assert nama == ["ohlcv_4h_shard00.parquet"]


def test_direktori_kosong_menghasilkan_daftar_kosong(tmp_path):
    assert pilih_berkas(tmp_path, "1h") == []
