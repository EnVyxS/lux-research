"""Pengujian adjudikasi H-015.

Yang dijaga di sini bukan hanya kebenaran aritmetika, melainkan tiga pembedaan
yang mudah runtuh diam-diam:

1. cabang LULUS **ada** (ADR-037 pasal 5) tetapi tidak pernah mengaku memenuhi
   ADR-015 pasal 4.4;
2. trade tipis menghasilkan TIDAK DAPAT DINILAI, **bukan** DITOLAK, berbeda dari
   ``gabung_h014``;
3. ``lookahead`` dimaklumi pada sel A dan **tidak** pada sel F.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lux.backtest import gabung_h015 as g
from lux.backtest.gerbang import NAMA_GERBANG

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


def run(
    pengaman: dict[str, list[str]] | None = None,
    gerbang: dict[str, list[str]] | None = None,
    ulangan: int = 300,
) -> dict:
    pengaman = pengaman or {}
    gerbang = gerbang or {}
    return {
        "hipotesis": "H-015",
        "sel": {
            s: {"gerbang_gagal": list(gerbang.get(s, []))} for s in ("K", "F", "A")
        },
        "audit_konfig": {
            s: {"pengaman_mati": list(pengaman.get(s, []))} for s in ("K", "F", "A")
        },
        "parameter_beku": {"ulangan": ulangan},
    }


DELAPAN_NOL = [0.0] * 8
BERGOYANG = [1.0, -0.8, 0.9, -0.7, 0.8, -0.6, 0.7, -0.5]


def adjudikasi(a: dict, b: dict, r: dict | None = None, **ganti):
    arg = dict(
        ambang_besaran=0.020,
        ambang_p=0.05,
        min_trade=100,
        min_ulangan=300,
        ulangan=ULANGAN_UJI,
    )
    arg.update(ganti)
    return g.adjudikasi(a, b, r if r is not None else run(), **arg)


# --------------------------------------------------------------------------
# Bentuk putusan
# --------------------------------------------------------------------------
def test_putusan_mungkin_bertiga():
    assert g.PUTUSAN_MUNGKIN == ("LULUS", "DITOLAK", "TIDAK DAPAT DINILAI")


def test_cabang_lulus_ada_berbeda_dari_h014():
    from lux.backtest import gabung_h014

    assert g.LULUS not in gabung_h014.PUTUSAN_MUNGKIN
    assert g.LULUS in g.PUTUSAN_MUNGKIN


def test_pembatas_menyangkal_adr015_dan_f_k():
    assert "BUKAN" in g.PEMBATAS
    assert "ADR-015" in g.PEMBATAS
    assert "F - K" in g.PEMBATAS
    assert "0,029481" in g.PEMBATAS


# --------------------------------------------------------------------------
# Tiga putusan
# --------------------------------------------------------------------------
def test_besaran_kecil_ditolak():
    h = adjudikasi(sel([0.001] * 8), sel(DELAPAN_NOL))
    assert h["putusan"] == g.DITOLAK
    assert any("rerata selisih bulanan" in a for a in h["alasan"])


def test_p_besar_ditolak_meski_besaran_lolos():
    h = adjudikasi(sel(BERGOYANG), sel(DELAPAN_NOL))
    assert h["besaran_rerata_bulanan_R"] >= 0.020
    assert h["p"] > 0.05
    assert h["putusan"] == g.DITOLAK


def test_besaran_dan_p_lolos_menghasilkan_lulus():
    h = adjudikasi(sel([0.5] * 8), sel(DELAPAN_NOL))
    assert h["p"] <= 0.05
    assert h["putusan"] == g.LULUS


def test_lulus_tetap_menyangkal_adr015():
    h = adjudikasi(sel([0.5] * 8), sel(DELAPAN_NOL))
    assert h["putusan"] == g.LULUS
    assert h["memenuhi_adr015"] is False
    assert h["per_bulan"]["memenuhi_adr015"] is False
    assert any("BUKAN kelulusan ADR-015" in a for a in h["alasan"])


def test_lulus_tidak_menyatakan_siap_diperdagangkan():
    h = adjudikasi(sel([0.5] * 8), sel(DELAPAN_NOL))
    assert any("siap diperdagangkan" in a for a in h["alasan"])


def test_ambang_tepat_di_batas_tidak_dilunakkan():
    h = adjudikasi(sel([0.019] * 8), sel(DELAPAN_NOL))
    assert h["putusan"] == g.DITOLAK


# --------------------------------------------------------------------------
# TIDAK DAPAT DINILAI: struktur pasangan
# --------------------------------------------------------------------------
def test_himpunan_bulan_tidak_sama_tidak_dapat_dinilai():
    a = sel([0.5] * 8)
    b = sel(DELAPAN_NOL, nama_bulan=[f"2024-{i + 1:02d}" for i in range(8)])
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


# --------------------------------------------------------------------------
# TIDAK DAPAT DINILAI: trade tipis, BUKAN DITOLAK
# --------------------------------------------------------------------------
def test_trade_tipis_tidak_dapat_dinilai_bukan_ditolak():
    h = adjudikasi(sel([0.5] * 8, trade=50), sel(DELAPAN_NOL))
    assert h["putusan"] == g.TIDAK_DAPAT_DINILAI
    assert h["putusan"] != g.DITOLAK
    assert any("trade sel F 50" in a for a in h["alasan"])


def test_trade_tipis_sel_a_juga_menghentikan():
    h = adjudikasi(sel([0.5] * 8), sel(DELAPAN_NOL, trade=99))
    assert h["putusan"] == g.TIDAK_DAPAT_DINILAI
    assert any("trade sel A 99" in a for a in h["alasan"])


# --------------------------------------------------------------------------
# TIDAK DAPAT DINILAI: kriteria yang hidup di h015_run.json
# --------------------------------------------------------------------------
def test_pengaman_mati_tidak_dapat_dinilai():
    r = run(pengaman={"F": ["maks_carry_realisasi_R"]})
    h = adjudikasi(sel([0.5] * 8), sel(DELAPAN_NOL), r)
    assert h["putusan"] == g.TIDAK_DAPAT_DINILAI
    assert h["pengaman_mati"] == {"F": ["maks_carry_realisasi_R"]}
    assert any("ADR-036" in a for a in h["alasan"])


def test_ulangan_kurang_tidak_dapat_dinilai():
    h = adjudikasi(sel([0.5] * 8), sel(DELAPAN_NOL), run(ulangan=299))
    assert h["putusan"] == g.TIDAK_DAPAT_DINILAI
    assert any("ulangan permutasi run 299" in a for a in h["alasan"])


def test_ulangan_hilang_tidak_dapat_dinilai():
    r = run()
    r["parameter_beku"] = {}
    h = adjudikasi(sel([0.5] * 8), sel(DELAPAN_NOL), r)
    assert h["putusan"] == g.TIDAK_DAPAT_DINILAI
    assert h["ulangan_run"] is None


# --------------------------------------------------------------------------
# Pemakluman gerbang (aturan 36)
# --------------------------------------------------------------------------
def test_lookahead_pada_sel_a_dimaklumi():
    r = run(gerbang={"A": ["lookahead"]})
    h = adjudikasi(sel([0.5] * 8), sel(DELAPAN_NOL), r)
    assert h["gerbang_gagal_tak_dimaklumi"] == {}
    assert h["putusan"] == g.LULUS


def test_lookahead_pada_sel_f_tidak_dimaklumi():
    r = run(gerbang={"F": ["lookahead"]})
    h = adjudikasi(sel([0.5] * 8), sel(DELAPAN_NOL), r)
    assert h["putusan"] == g.TIDAK_DAPAT_DINILAI
    assert h["gerbang_gagal_tak_dimaklumi"] == {"F": ["lookahead"]}


def test_gerbang_lain_pada_sel_a_tidak_dimaklumi():
    r = run(gerbang={"A": ["lookahead", "overlap"]})
    h = adjudikasi(sel([0.5] * 8), sel(DELAPAN_NOL), r)
    assert h["putusan"] == g.TIDAK_DAPAT_DINILAI
    assert h["gerbang_gagal_tak_dimaklumi"] == {"A": ["overlap"]}


def test_gerbang_dimaklumi_hanya_sel_a():
    assert set(g.GERBANG_DIMAKLUMI) == {"A"}


def test_nama_gerbang_dimaklumi_benar_benar_ada():
    for daftar in g.GERBANG_DIMAKLUMI.values():
        for nama in daftar:
            assert nama in NAMA_GERBANG


# --------------------------------------------------------------------------
# Pelaporan
# --------------------------------------------------------------------------
def test_besaran_dilaporkan_dua_kali():
    h = adjudikasi(sel([0.5] * 8), sel(DELAPAN_NOL))
    assert h["besaran_rerata_bulanan_R"] is not None
    assert h["besaran_agregat_R"] is not None
    assert "cacat kelas 16" in h["catatan_besaran"]


def test_selisih_f_k_dihitung_dan_dilabeli_tidak_mengikat():
    h = adjudikasi(
        sel([0.5] * 8), sel(DELAPAN_NOL), isi_k=sel([0.1] * 8)
    )
    assert h["selisih_TIDAK_mengikat_F_K"] == pytest.approx(0.4)
    assert "haram" in h["catatan_F_K"]


def test_tanpa_sel_k_selisih_f_k_kosong():
    h = adjudikasi(sel([0.5] * 8), sel(DELAPAN_NOL))
    assert h["selisih_TIDAK_mengikat_F_K"] is None


def test_pasangan_adalah_f_dikurangi_a():
    h = adjudikasi(sel([0.3] * 8), sel([0.1] * 8))
    assert h["besaran_rerata_bulanan_R"] == pytest.approx(0.2)


def test_laporan_memuat_kedua_pembatas(tmp_path: Path):
    h = adjudikasi(sel(BERGOYANG), sel(DELAPAN_NOL))
    g.tulis_laporan(h, out=tmp_path, nama="uji_h015")
    isi = json.loads((tmp_path / "uji_h015.json").read_text(encoding="utf-8"))
    md = (tmp_path / "uji_h015.md").read_text(encoding="utf-8")
    assert isi["pembatas"] == g.PEMBATAS
    assert isi["pembatas_berpasangan"]
    assert "TIDAK MENGIKAT" in md or "haram" in md
    assert "Memenuhi ADR-015 pasal 4.4: **TIDAK**" in md


# --------------------------------------------------------------------------
# Kode keluar
# --------------------------------------------------------------------------
def tulis(tmp_path: Path, isi_f: dict, isi_a: dict, r: dict) -> list[str]:
    f = tmp_path / "f.json"
    a = tmp_path / "a.json"
    rj = tmp_path / "run.json"
    f.write_text(json.dumps(isi_f), encoding="utf-8")
    a.write_text(json.dumps(isi_a), encoding="utf-8")
    rj.write_text(json.dumps(r), encoding="utf-8")
    return [
        "--run", str(rj), "--sel-f", str(f), "--sel-a", str(a),
        "--ambang-besaran", "0.020", "--ambang-p", "0.05",
        "--min-trade", "100", "--min-ulangan", "300",
        "--ulangan", str(ULANGAN_UJI), "--out", str(tmp_path),
    ]


def test_exit_0_untuk_ditolak(tmp_path: Path):
    argv = tulis(tmp_path, sel(BERGOYANG), sel(DELAPAN_NOL), run())
    assert g.main(argv + ["--nama", "keluar_tolak"]) == 0


def test_exit_0_untuk_lulus(tmp_path: Path):
    argv = tulis(tmp_path, sel([0.5] * 8), sel(DELAPAN_NOL), run())
    assert g.main(argv + ["--nama", "keluar_lulus"]) == 0


def test_exit_4_untuk_tidak_dapat_dinilai(tmp_path: Path):
    argv = tulis(
        tmp_path, sel([0.5] * 8), sel(DELAPAN_NOL), run(ulangan=10)
    )
    assert g.main(argv + ["--nama", "keluar_tdn"]) == 4


def test_exit_2_bila_run_hilang(tmp_path: Path):
    argv = tulis(tmp_path, sel([0.5] * 8), sel(DELAPAN_NOL), run())
    argv[1] = str(tmp_path / "tidak_ada.json")
    assert g.main(argv + ["--nama", "keluar_2a"]) == 2


def test_exit_2_bila_agregat_periode_hilang(tmp_path: Path):
    argv = tulis(tmp_path, {"gabungan": {}}, sel(DELAPAN_NOL), run())
    assert g.main(argv + ["--nama", "keluar_2b"]) == 2


def test_exit_2_bila_run_tanpa_audit_konfig(tmp_path: Path):
    r = run()
    del r["audit_konfig"]
    argv = tulis(tmp_path, sel([0.5] * 8), sel(DELAPAN_NOL), r)
    assert g.main(argv + ["--nama", "keluar_2c"]) == 2


def test_muat_sel_menolak_berkas_hilang(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        g.muat_sel(tmp_path / "tidak_ada.json")


def test_muat_run_menolak_berkas_hilang(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        g.muat_run(tmp_path / "tidak_ada.json")
