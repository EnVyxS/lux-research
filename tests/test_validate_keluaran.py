"""Pengujian nama keluaran validasi, pemilihan berkas, dan ambang per interval.

Yang dijaga di sini bukan ejaan nama berkas melainkan dua cacat senyap yang
hampir terjadi ketika ADR-016 langkah 3 disiapkan.

Pertama, `potong_ekor.yml` meneruskan `reports/universe_layak.json` sebagai
`--universe`, dan sebelum ADR-016 setiap interval menulis ke berkas itu.
Validasi 4h karena itu akan menimpa semesta 1h dan memberi ADR-003 daftar simbol
dari interval yang salah, tanpa satu pun pesan galat.

Kedua, `muat_ambang` membaca `min_bar_1h` apa pun intervalnya. 8.760 bar berarti
satu tahun pada 1h tetapi empat tahun pada 4h, sehingga semesta 4h akan menyusut
karena satuan yang diwarisi dan penyusutan itu akan tampak seperti temuan
tentang pasar (ADR-017).

Seluruh pengujian di berkas ini berjalan tanpa parquet dan tanpa jaringan.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from lux.validate_run import (
    INTERVAL_LEGASI,
    muat_ambang,
    nama_keluaran_universe,
    pilih_berkas,
)

AKAR = Path(__file__).resolve().parents[1]


def tulis_config(tmp_path: Path, universe: dict) -> Path:
    path = tmp_path / "lux.yaml"
    path.write_text(yaml.safe_dump({"universe": universe}), encoding="utf-8")
    return path


def universe_lengkap() -> dict:
    return {
        "min_bar_1h": 8760,
        "min_bar_4h": 2190,
        "min_median_quote_volume_harian": 1000000,
        "maks_rasio_bar_datar": 0.30,
    }


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


def test_ambang_dibaca_dari_kunci_per_interval(tmp_path) -> None:
    """4h WAJIB memakai lantainya sendiri, bukan lantai 1h."""
    path = tulis_config(tmp_path, universe_lengkap())
    assert muat_ambang(path, "1h").min_bar == 8760
    assert muat_ambang(path, "4h").min_bar == 2190


def test_ambang_bawaan_tetap_1h_agar_pemanggil_lama_tidak_patah(tmp_path) -> None:
    path = tulis_config(tmp_path, universe_lengkap())
    assert muat_ambang(path).min_bar == 8760


def test_kunci_interval_hilang_menghentikan_run(tmp_path) -> None:
    """Gagal keras, dan pesannya menyebut kunci yang hilang.

    Jatuh diam-diam ke min_bar_1h adalah cacat yang ADR-017 perbaiki, jadi
    ketiadaan kunci tidak boleh berujung pada laporan yang tampak sah.
    """
    universe = universe_lengkap()
    del universe["min_bar_4h"]
    path = tulis_config(tmp_path, universe)
    with pytest.raises(SystemExit) as galat:
        muat_ambang(path, "4h")
    assert "min_bar_4h" in str(galat.value)


def test_lantai_4h_setara_satu_tahun_seperti_1h() -> None:
    """Tripwire aritmetika atas config sungguhan, bukan atas config buatan.

    Yang dibekukan ADR-017 adalah maknanya: satu tahun kalender untuk setiap
    interval. Bila kelak salah satu angka digeser tanpa yang lain, kesetaraan
    ini pecah dan pengujian ini gagal lebih dulu daripada laporan.
    """
    cfg = yaml.safe_load((AKAR / "config" / "lux.yaml").read_text(encoding="utf-8"))
    u = cfg["universe"]
    assert u["min_bar_1h"] == 8760
    assert u["min_bar_4h"] == 2190
    assert u["min_bar_4h"] * 4 == u["min_bar_1h"]
