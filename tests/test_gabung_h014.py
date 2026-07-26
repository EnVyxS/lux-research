"""Pengujian adjudikasi H-014. Yang dijaga: tidak ada jalan menuju LULUS."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lux.backtest import gabung_h014 as g

ULANGAN_UJI = 1000


def bulan(nama: str, ekspektasi, trade: int = 200) -> dict:
    total = None if ekspektasi is None else float(ekspektasi) * trade
    return {
        "periode": nama,
        "trade": trade,
        "total_R": 0.0 if total is None else total,
        "ekspektasi_R": ekspektasi,
    }


def sel(nilai: list, nama_bulan: list[str] | None = None, trade: int = 60_000) -> dict:
    nama_bulan = nama_bulan or [f"2025-{i + 1:02d}" for i in range(len(nilai))]
    return {
        "gabungan": {"jumlah_trade_luar_sampel": trade},
        "agregat_periode": [bulan(n, v) for n, v in zip(nama_bulan, nilai)],
    }


DELAPAN_NOL = [0.0] * 8
BERGOYANG = [1.0, -0.8, 0.9, -0.7, 0.8, -0.6, 0.7, -0.5]


def adjudikasi(a: dict, b: dict, **ganti):
    arg = dict(ambang_besaran=0.020, ambang_p=0.05, min_trade=100, ulangan=ULANGAN_UJI)
    arg.update(ganti)
    return g.adjudikasi(a, b, **arg)


def test_putusan_mungkin_hanya_dua():
    assert g.PUTUSAN_MUNGKIN == ("DITOLAK", "TIDAK DAPAT DINILAI")


def test_besaran_kecil_ditolak():
    h = adjudikasi(sel([0.001] * 8), sel(DELAPAN_NOL))
    assert h["putusan"] == g.DITOLAK
    assert any("rerata selisih bulanan" in a for a in h["alasan"])


def test_p_besar_ditolak_meski_besaran_lolos():
    h = adjudikasi(sel(BERGOYANG), sel(DELAPAN_NOL))
    assert h["besaran_rerata_bulanan_R"] >= 0.020
    assert h["p"] > 0.05
    assert h["putusan"] == g.DITOLAK


def test_besaran_dan_p_lolos_tetap_bukan_lulus():
    h = adjudikasi(sel([0.5] * 8), sel(DELAPAN_NOL))
    assert h["p"] <= 0.05
    assert h["putusan"] == g.TIDAK_DAPAT_DINILAI
    assert any("BUKAN kelulusan" in a for a in h["alasan"])


def test_himpunan_bulan_tidak_sama_tidak_dapat_dinilai():
    a = sel([0.5] * 8)
    b = sel([0.0] * 8, nama_bulan=[f"2024-{i + 1:02d}" for i in range(8)])
    h = adjudikasi(a, b)
    assert h["putusan"] == g.TIDAK_DAPAT_DINILAI
    assert any("himpunan bulan tidak sama" in x for x in h["alasan"])


def test_bulan_tanpa_ekspektasi_tidak_dapat_dinilai():
    a = sel([0.5] * 8)
    a["agregat_periode"][3]["ekspektasi_R"] = None
    h = adjudikasi(a, sel(DELAPAN_NOL))
    assert h["putusan"] == g.TIDAK_DAPAT_DINILAI
    assert h["per_bulan"]["tanpa_nilai"] == ["2025-04"]


def test_pasangan_kurang_dari_dua_tidak_dapat_dinilai():
    h = adjudikasi(sel([0.5]), sel([0.0]))
    assert h["putusan"] == g.TIDAK_DAPAT_DINILAI


def test_trade_di_bawah_lantai_ditolak():
    h = adjudikasi(sel([0.5] * 8, trade=50), sel(DELAPAN_NOL))
    assert h["putusan"] == g.DITOLAK
    assert any("trade sel a 50" in a for a in h["alasan"])


def test_besaran_dilaporkan_dua_kali():
    h = adjudikasi(sel([0.5] * 8), sel(DELAPAN_NOL))
    assert h["besaran_rerata_bulanan_R"] is not None
    assert h["besaran_agregat_R"] is not None
    assert "rerata sebaran nol" in h["catatan_besaran"]


def test_memenuhi_adr015_selalu_false():
    h = adjudikasi(sel([0.5] * 8), sel(DELAPAN_NOL))
    assert h["memenuhi_adr015"] is False
    assert h["per_bulan"]["memenuhi_adr015"] is False


def test_pembatas_menyangkal_pembanding_h013():
    assert "0,029481" in g.PEMBATAS
    assert "DUA medan" in g.PEMBATAS


def test_laporan_memuat_pembatas(tmp_path: Path):
    h = adjudikasi(sel(BERGOYANG), sel(DELAPAN_NOL))
    g.tulis_laporan(h, out=tmp_path, nama="uji_h014")
    isi = json.loads((tmp_path / "uji_h014.json").read_text(encoding="utf-8"))
    md = (tmp_path / "uji_h014.md").read_text(encoding="utf-8")
    assert isi["pembatas"] == g.PEMBATAS
    assert "0,029481" in md
    assert "BARU" in md


def test_exit_0_untuk_ditolak(tmp_path: Path):
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    a.write_text(json.dumps(sel(BERGOYANG)), encoding="utf-8")
    b.write_text(json.dumps(sel(DELAPAN_NOL)), encoding="utf-8")
    kode = g.main(
        [
            "--sel-a", str(a), "--sel-b", str(b),
            "--ambang-besaran", "0.020", "--ambang-p", "0.05",
            "--min-trade", "100", "--ulangan", str(ULANGAN_UJI),
            "--out", str(tmp_path), "--nama", "keluar_h014",
        ]
    )
    assert kode == 0


def test_exit_4_untuk_tidak_dapat_dinilai(tmp_path: Path):
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    a.write_text(json.dumps(sel([0.5] * 8)), encoding="utf-8")
    b.write_text(json.dumps(sel(DELAPAN_NOL)), encoding="utf-8")
    kode = g.main(
        [
            "--sel-a", str(a), "--sel-b", str(b),
            "--ambang-besaran", "0.020", "--ambang-p", "0.05",
            "--min-trade", "100", "--ulangan", str(ULANGAN_UJI),
            "--out", str(tmp_path), "--nama", "keluar_h014b",
        ]
    )
    assert kode == 4


def test_exit_2_bila_agregat_periode_hilang(tmp_path: Path):
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    a.write_text(json.dumps({"gabungan": {}}), encoding="utf-8")
    b.write_text(json.dumps(sel(DELAPAN_NOL)), encoding="utf-8")
    kode = g.main(
        [
            "--sel-a", str(a), "--sel-b", str(b),
            "--ambang-besaran", "0.020", "--ambang-p", "0.05",
            "--min-trade", "100", "--out", str(tmp_path),
        ]
    )
    assert kode == 2


def test_muat_sel_menolak_berkas_hilang(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        g.muat_sel(tmp_path / "tidak_ada.json")
