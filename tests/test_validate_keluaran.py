"""Pengujian nama keluaran validasi dan pemilihan berkas per interval.

Yang dijaga di sini bukan ejaan nama berkas melainkan satu cacat senyap yang
hampir terjadi: `potong_ekor.yml` meneruskan `reports/universe_layak.json`
sebagai `--universe`, dan sebelum ADR-016 setiap interval menulis ke berkas itu.
Validasi 4h karena itu akan menimpa semesta 1h dan memberi ADR-003 daftar simbol
dari interval yang salah, tanpa satu pun pesan galat.

Seluruh pengujian di berkas ini berjalan tanpa parquet dan tanpa jaringan.
"""

from __future__ import annotations

from lux.validate_run import (
    INTERVAL_LEGASI,
    nama_keluaran_universe,
    pilih_berkas,
)


def test_interval_legasi_adalah_1h() -> None:
    """Tripwire. Hanya 1h yang pernah punya pembaca berkas legasi."""
    assert INTERVAL_LEGASI == "1h"


def test_1h_menulis_berkas_legasi_agar_potong_ekor_tidak_patah() -> None:
    nama = nama_keluaran_universe("1h")
    assert nama == ["universe_layak_1h.json", "universe_layak.json"]


def test_4h_tidak_boleh_menyentuh_berkas_legasi() -> None:
    """Inti perbaikan: 4h secara konstruksi tak dapat menimpa semesta 1h."""
    nama = nama_keluaran_universe("4h")
    assert "universe_layak.json" not in nama
    assert nama == ["universe_layak_4h.json"]


def test_nama_kanonik_selalu_pertama_dan_menyebut_interval() -> None:
    for interval in ("1h", "4h", "1m", "1d"):
        nama = nama_keluaran_universe(interval)
        assert nama[0] == f"universe_layak_{interval}.json"
        assert interval in nama[0]


def test_pilih_berkas_hanya_mengambil_interval_yang_diminta(tmp_path) -> None:
    for nama in (
        "ohlcv_4h_shard00.parquet",
        "ohlcv_4h_tail_shard00.parquet",
        "ohlcv_1h_shard00.parquet",
        "funding_shard00.parquet",
    ):
        (tmp_path / nama).write_bytes(b"")
    dipilih = sorted(p.name for p in pilih_berkas(tmp_path, "4h"))
    assert dipilih == ["ohlcv_4h_shard00.parquet", "ohlcv_4h_tail_shard00.parquet"]


def test_pilih_berkas_menolak_aset_retry_juga_pada_4h(tmp_path) -> None:
    """Aturan aset usang berlaku bagi interval mana pun, bukan hanya 1h."""
    for nama in (
        "ohlcv_4h_shard00.parquet",
        "ohlcv_4h_shard01_retry.parquet",
    ):
        (tmp_path / nama).write_bytes(b"")
    dipilih = [p.name for p in pilih_berkas(tmp_path, "4h")]
    assert dipilih == ["ohlcv_4h_shard00.parquet"]
