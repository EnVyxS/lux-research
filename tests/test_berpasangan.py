"""Test Jalur A ADR-026.

Yang dikunci di sini bukan hanya aritmetika, melainkan juga **pembatas**: modul
ini tidak boleh pernah memancarkan putusan yang memenuhi ADR-015, dan pembatas
itu wajib ikut ke dalam laporan. Cacat kelas kesepuluh (prosa kesimpulan yang
dipatok di kode) lahir karena tidak ada test yang menuntut kesesuaian antara
angka dan kalimat; test di berkas ini adalah pembayaran utang itu.
"""

from __future__ import annotations

import json

from lux.analisis.berpasangan import (
    PEMBATAS,
    bootstrap,
    pasangan_bulan,
    pasangan_simbol,
    ringkas,
    tulis_laporan,
    uji_tanda,
)


def _sel(baris_simbol, baris_bulan=None):
    return {
        "per_simbol": baris_simbol,
        "agregat_periode": baris_bulan or [],
    }


def test_pasangkan_hanya_irisan_dan_sisanya_tercatat():
    a = _sel(
        [
            {"symbol": "AAA", "ekspektasi_R": 0.10, "trade": 100, "total_R": 10.0},
            {"symbol": "BBB", "ekspektasi_R": 0.20, "trade": 50, "total_R": 10.0},
            {"symbol": "HANYA_A", "ekspektasi_R": 9.0, "trade": 1, "total_R": 9.0},
        ]
    )
    b = _sel(
        [
            {"symbol": "AAA", "ekspektasi_R": 0.05, "trade": 100, "total_R": 5.0},
            {"symbol": "BBB", "ekspektasi_R": 0.30, "trade": 50, "total_R": 15.0},
            {"symbol": "HANYA_B", "ekspektasi_R": 1.0, "trade": 2, "total_R": 2.0},
        ]
    )
    h = pasangan_simbol(a, b)
    assert h["n_pasangan"] == 2
    assert [p["id"] for p in h["pasangan"]] == ["AAA", "BBB"]
    assert h["hanya_a"] == ["HANYA_A"]
    assert h["hanya_b"] == ["HANYA_B"]
    assert h["pasangan"][0]["selisih"] == 0.05


def test_pasangan_dengan_nilai_kosong_dibuang_dan_dicatat():
    a = _sel([{"symbol": "AAA", "ekspektasi_R": None, "trade": 0, "total_R": 0.0}])
    b = _sel([{"symbol": "AAA", "ekspektasi_R": 0.1, "trade": 5, "total_R": 0.5}])
    h = pasangan_simbol(a, b)
    assert h["n_pasangan"] == 0
    assert h["tanpa_nilai"] == ["AAA"]


def test_pasangan_bulan_memakai_kunci_periode():
    a = _sel([], [{"periode": "2025-01", "ekspektasi_R": 0.2, "trade": 10, "total_R": 2.0}])
    b = _sel([], [{"periode": "2025-01", "ekspektasi_R": 0.1, "trade": 10, "total_R": 1.0}])
    h = pasangan_bulan(a, b)
    assert h["kunci_id"] == "periode"
    assert h["n_pasangan"] == 1
    assert abs(h["pasangan"][0]["selisih"] - 0.1) < 1e-12


def test_uji_tanda_selisih_simetris_memberi_p_besar():
    d = [0.1, -0.1, 0.2, -0.2, 0.05, -0.05]
    u = uji_tanda(d, ulangan=2000, seed=1)
    assert u["dapat_dinilai"] is True
    assert abs(u["rerata"]) < 1e-12
    assert u["p"] > 0.5


def test_uji_tanda_semua_positif_memberi_p_kecil():
    d = [0.05] * 40
    u = uji_tanda(d, ulangan=2000, seed=2)
    assert u["p"] <= 0.01
    assert u["p"] > 0.0


def test_uji_tanda_deterministik_pada_seed_sama():
    d = [0.03, -0.01, 0.07, 0.02, -0.04, 0.06]
    a = uji_tanda(d, ulangan=500, seed=7)
    b = uji_tanda(d, ulangan=500, seed=7)
    c = uji_tanda(d, ulangan=500, seed=8)
    assert a["p"] == b["p"]
    assert a["m_lebih_ekstrem"] == b["m_lebih_ekstrem"]
    assert isinstance(c["p"], float)


def test_bootstrap_selang_memuat_rerata():
    d = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08]
    b = bootstrap(d, ulangan=1000, seed=3)
    assert b["dapat_dinilai"] is True
    assert b["bawah"] <= b["rerata"] <= b["atas"]


def test_ringkas_tidak_pernah_menyatakan_memenuhi_adr015():
    a = _sel(
        [
            {"symbol": "AAA", "ekspektasi_R": 0.50, "trade": 100, "total_R": 50.0},
            {"symbol": "BBB", "ekspektasi_R": 0.60, "trade": 100, "total_R": 60.0},
            {"symbol": "CCC", "ekspektasi_R": 0.70, "trade": 100, "total_R": 70.0},
        ]
    )
    b = _sel(
        [
            {"symbol": "AAA", "ekspektasi_R": 0.00, "trade": 100, "total_R": 0.0},
            {"symbol": "BBB", "ekspektasi_R": 0.00, "trade": 100, "total_R": 0.0},
            {"symbol": "CCC", "ekspektasi_R": 0.00, "trade": 100, "total_R": 0.0},
        ]
    )
    r = ringkas(pasangan_simbol(a, b), ambang=0.020, ulangan=500, seed=4)
    # Besaran jauh melewati ambang dan p sekecil mungkin, namun putusan ADR-015
    # tetap TIDAK terpenuhi. Justru di keadaan menyenangkan inilah putusan
    # separuh kriteria paling berbahaya (ADR-024).
    assert r["melewati_ambang_besaran"] is True
    assert r["memenuhi_adr015"] is False
    assert "lulus" not in r
    assert r["fraksi_positif"] == 1.0


def test_ringkas_selisih_agregat_dan_berbobot_konsisten():
    # Bobot tak sama, supaya rerata tak berbobot berbeda dari agregat.
    a = _sel(
        [
            {"symbol": "AAA", "ekspektasi_R": 0.10, "trade": 100, "total_R": 10.0},
            {"symbol": "BBB", "ekspektasi_R": 0.40, "trade": 10, "total_R": 4.0},
        ]
    )
    b = _sel(
        [
            {"symbol": "AAA", "ekspektasi_R": 0.05, "trade": 100, "total_R": 5.0},
            {"symbol": "BBB", "ekspektasi_R": 0.05, "trade": 10, "total_R": 0.5}, 
        ]
    )
    r = ringkas(pasangan_simbol(a, b), ambang=0.020, ulangan=200, seed=5)
    assert abs(r["rerata_selisih"] - 0.20) < 1e-12
    assert abs(r["rerata_berbobot"] - (0.05 * 100 + 0.35 * 10) / 110.0) < 1e-12
    assert abs(r["selisih_agregat"] - (14.0 / 110.0 - 5.5 / 110.0)) < 1e-12


def test_tulis_laporan_memuat_pembatas_di_json_dan_md(tmp_path):
    a = _sel(
        [
            {"symbol": "AAA", "ekspektasi_R": 0.10, "trade": 10, "total_R": 1.0},
            {"symbol": "BBB", "ekspektasi_R": 0.20, "trade": 10, "total_R": 2.0},
        ],
        [
            {"periode": "2025-01", "ekspektasi_R": 0.1, "trade": 10, "total_R": 1.0},
            {"periode": "2025-02", "ekspektasi_R": 0.2, "trade": 10, "total_R": 2.0},
        ],
    )
    b = _sel(
        [
            {"symbol": "AAA", "ekspektasi_R": 0.05, "trade": 10, "total_R": 0.5},
            {"symbol": "BBB", "ekspektasi_R": 0.05, "trade": 10, "total_R": 0.5},
        ],
        [
            {"periode": "2025-01", "ekspektasi_R": 0.05, "trade": 10, "total_R": 0.5},
            {"periode": "2025-02", "ekspektasi_R": 0.05, "trade": 10, "total_R": 0.5},
        ],
    )
    rs = ringkas(pasangan_simbol(a, b), ambang=0.020, ulangan=200, seed=6)
    rb = ringkas(pasangan_bulan(a, b), ambang=0.020, ulangan=200, seed=6)
    tulis_laporan("uji_pembatas", rs, rb, out=tmp_path)

    isi = json.loads((tmp_path / "uji_pembatas.json").read_text(encoding="utf-8"))
    md = (tmp_path / "uji_pembatas.md").read_text(encoding="utf-8")
    assert isi["pembatas"] == PEMBATAS
    assert PEMBATAS in md
    assert "Memenuhi ADR-015 pasal 4.4: **TIDAK**" in md
