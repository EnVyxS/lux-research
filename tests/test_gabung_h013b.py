"""Pagar penggabung Jalur B: cakupan, kematian gerbang, dan putusan dua syarat.

Yang dijaga bukan angkanya, melainkan keadaan-keadaan di mana penggabung WAJIB
menolak melahirkan putusan. Sebuah penggabung yang selalu menghasilkan angka
adalah penggabung yang tidak menjaga apa pun.

Sejak ADR-031 berkas ini juga menjaga dua hal yang bukan pagar putusan melainkan
pagar KEJUJURAN laporan: besaran wajib ikut diukur terhadap rerata sebaran nol
(aturan 49), dan prosa ramalan yang terbantah dikoreksi tanpa menghapus bunyi
aslinya (aturan 50).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lux.backtest.gabung_h013b import (
    AMBANG_P,
    BUNYI_ASLI_R_D3,
    EKSPEKTASI_SS,
    KOREKSI_R_D3,
    PEMBATAS,
    adjudikasi,
    daftar_pecahan,
    muat_pecahan,
    periksa_bulan,
    periksa_cakupan,
    ringkas,
    tulis_laporan,
)
from lux.backtest.run_h013 import AMBANG_KONTRIBUSI_SINYAL, MIN_ULANGAN
from lux.backtest.run_h013b import EKSPEKTASI_AS_SEED42, SEED_AKHIR, SEED_AWAL


def bulan(periode: str, trade: int = 10, total: float = 1.0) -> dict:
    return {
        "periode": periode,
        "trade": trade,
        "total_R": total,
        "ekspektasi_R": total / trade,
    }


def tulis_pecahan(
    tmp: Path,
    lo: int,
    hi: int,
    *,
    gerbang: str = "MATI (sampel_permutasi=0)",
    selesai: bool = True,
    r_d5=None,
    seed_paksa=None,
) -> Path:
    seed = list(range(lo, hi)) if seed_paksa is None else seed_paksa
    p = tmp / f"h013b_seed_{lo}_{hi}.json"
    p.write_text(
        json.dumps(
            {
                "pecahan": [lo, hi],
                "seed_diminta": seed,
                "seed_selesai": seed,
                "selesai": selesai,
                "gerbang_entri_acak": gerbang,
                "r_d5_cocok": r_d5,
                "baris": [
                    {
                        "seed": s,
                        "ekspektasi_R": 0.01 + s / 10000,
                        "total_R": 100.0,
                        "trade": 5000,
                        "bulan": [bulan("2025-01"), bulan("2025-02")],
                    }
                    for s in seed
                ],
            }
        ),
        encoding="utf-8",
    )
    return p


def ringkasan_sintetis(tmp: Path) -> dict:
    """Enam puluh seed sintetis, cukup untuk menguji aritmetika laporan.

    Cakupan sengaja TIDAK utuh 300: yang diuji di sini bukan kelayakan putusan
    melainkan kejujuran angka dan prosanya, dan pagar cakupan sudah diuji
    terpisah. Nilai seed 0,01 sampai 0,0159 membuat rerata nol berada DI ATAS
    ekspektasi sel AS seed 42, yaitu bentuk yang sama dengan run 30217516013.
    """
    tulis_pecahan(tmp, 0, 30, r_d5=True)
    tulis_pecahan(tmp, 30, 60)
    muat = muat_pecahan(daftar_pecahan(tmp))
    bulan_ss = [bulan("2025-01"), bulan("2025-02")]
    return ringkas(muat, bulan_ss, [])


def test_daftar_pecahan_urut_menurut_seed_bukan_nama(tmp_path):
    tulis_pecahan(tmp_path, 120, 150)
    tulis_pecahan(tmp_path, 30, 60)
    nama = [p.name for p in daftar_pecahan(tmp_path)]
    assert nama == ["h013b_seed_30_60.json", "h013b_seed_120_150.json"]


def test_muat_pecahan_menggabungkan_seed(tmp_path):
    tulis_pecahan(tmp_path, 0, 30, r_d5=None)
    tulis_pecahan(tmp_path, 30, 60, r_d5=True)
    muat = muat_pecahan(daftar_pecahan(tmp_path))
    assert len(muat["seed"]) == 60
    assert muat["r_d5_terbukti"] is True
    assert len(muat["pecahan"]) == 2


def test_muat_pecahan_menolak_gerbang_tak_dinyatakan(tmp_path):
    tulis_pecahan(tmp_path, 0, 30, gerbang="hidup")
    with pytest.raises(ValueError, match="gerbang"):
        muat_pecahan(daftar_pecahan(tmp_path))


def test_muat_pecahan_menolak_pecahan_belum_selesai(tmp_path):
    tulis_pecahan(tmp_path, 0, 30, selesai=False)
    with pytest.raises(ValueError, match="selesai"):
        muat_pecahan(daftar_pecahan(tmp_path))


def test_muat_pecahan_menolak_r_d5_meleset(tmp_path):
    tulis_pecahan(tmp_path, 30, 60, r_d5=False)
    with pytest.raises(ValueError, match="R-D5"):
        muat_pecahan(daftar_pecahan(tmp_path))


def test_muat_pecahan_menolak_seed_kembar(tmp_path):
    tulis_pecahan(tmp_path, 0, 30)
    tulis_pecahan(tmp_path, 30, 60, seed_paksa=list(range(20, 50)))
    with pytest.raises(ValueError, match="kembar"):
        muat_pecahan(daftar_pecahan(tmp_path))


def test_muat_pecahan_menolak_kosong():
    with pytest.raises(ValueError):
        muat_pecahan([])


def test_periksa_cakupan_menerima_rentang_utuh():
    periksa_cakupan(range(SEED_AWAL, SEED_AKHIR))


def test_periksa_cakupan_menolak_lubang_di_tengah():
    seed = [s for s in range(SEED_AWAL, SEED_AKHIR) if s != 137]
    with pytest.raises(ValueError, match="tidak utuh"):
        periksa_cakupan(seed)


def test_periksa_cakupan_menolak_kurang_dari_ambang():
    with pytest.raises(ValueError, match=str(MIN_ULANGAN)):
        periksa_cakupan(range(SEED_AWAL, SEED_AKHIR - 3))


def test_periksa_bulan_diam_ketika_himpunan_sama():
    acuan = [bulan("2025-01"), bulan("2025-02")]
    nol = {1: [bulan("2025-02"), bulan("2025-01")], 2: list(acuan)}
    assert periksa_bulan(acuan, nol) == []


def test_periksa_bulan_melaporkan_setiap_seed_yang_berbeda():
    acuan = [bulan("2025-01"), bulan("2025-02")]
    nol = {1: [bulan("2025-01")], 2: list(acuan), 3: [bulan("2025-03")]}
    pesan = periksa_bulan(acuan, nol)
    assert len(pesan) == 2
    assert "seed 1" in pesan[0] and "seed 3" in pesan[1]


def test_adjudikasi_menolak_besaran_lulus_tetapi_p_gagal():
    """Inilah cacat ADR-024 yang ditutup: besaran saja tidak pernah cukup."""
    h = adjudikasi(
        besaran=0.0548, p=0.4, n=300, trade_terkecil=5000, bulan_cocok=True
    )
    assert h["melewati_ambang_besaran"] is True
    assert h["putusan"] == "DITOLAK"
    assert h["lulus"] is False


def test_adjudikasi_menolak_p_kecil_tetapi_besaran_gagal():
    h = adjudikasi(
        besaran=0.001, p=0.0001, n=300, trade_terkecil=5000, bulan_cocok=True
    )
    assert h["putusan"] == "DITOLAK"
    assert h["melewati_ambang_besaran"] is False


def test_adjudikasi_tak_ternilai_bukan_gagal():
    kurang = adjudikasi(
        besaran=0.0548, p=0.01, n=297, trade_terkecil=5000, bulan_cocok=True
    )
    assert kurang["putusan"] == "TIDAK DAPAT DINILAI"
    assert str(MIN_ULANGAN) in kurang["sebab"]
    bulan_beda = adjudikasi(
        besaran=0.0548, p=0.01, n=300, trade_terkecil=5000, bulan_cocok=False
    )
    assert bulan_beda["putusan"] == "TIDAK DAPAT DINILAI"
    tipis = adjudikasi(
        besaran=0.0548, p=0.01, n=300, trade_terkecil=99, bulan_cocok=True
    )
    assert tipis["putusan"] == "TIDAK DAPAT DINILAI"


def test_adjudikasi_lulus_menuntut_dua_syarat_dan_ambang_tak_bergeser():
    h = adjudikasi(
        besaran=0.0548, p=0.004, n=300, trade_terkecil=5000, bulan_cocok=True
    )
    assert h["putusan"] == "LULUS"
    assert h["lulus"] is True
    assert AMBANG_P == 0.05
    assert AMBANG_KONTRIBUSI_SINYAL == 0.020
    assert h["satuan_p"] == "bulan"
    assert EKSPEKTASI_SS > 0
    assert "ADR-028" in PEMBATAS and "MENJATUHKAN" in PEMBATAS


def test_bunyi_asli_r_d3_tersimpan_verbatim():
    """Aturan 50: yang dikoreksi adalah alasannya, bukan riwayatnya."""
    assert "permutasinya cacat" in BUNYI_ASLI_R_D3
    assert str(EKSPEKTASI_SS) in BUNYI_ASLI_R_D3


def test_prosa_r_d3_terkoreksi_tidak_lagi_menyebut_permutasi_cacat(tmp_path):
    isi = ringkasan_sintetis(tmp_path)
    r = isi["ramalan"]["R-D3"]
    assert "cacat" not in r["bunyi"]
    assert r["bunyi_asli"] == BUNYI_ASLI_R_D3
    assert r["bunyi"] != r["bunyi_asli"]


def test_koreksi_r_d3_menyatakan_permutasinya_sehat():
    assert "sehat" in KOREKSI_R_D3
    assert "TERBANTAH" in KOREKSI_R_D3
    assert "MELESET" in KOREKSI_R_D3


def test_ringkas_melaporkan_besaran_terhadap_rerata_nol(tmp_path):
    """Aturan 49: satu undian nol bukan sebaran nol."""
    isi = ringkasan_sintetis(tmp_path)
    rerata = isi["sebaran_seed"]["rerata"]
    assert isi["besaran_terhadap_rerata_nol_R"] == pytest.approx(
        EKSPEKTASI_SS - rerata
    )
    assert isi["besaran_sumbangan_sinyal_R"] == pytest.approx(
        EKSPEKTASI_SS - EKSPEKTASI_AS_SEED42
    )


def test_besaran_terhadap_rerata_nol_lebih_kecil_ketika_undian_di_bawah_rerata(
    tmp_path,
):
    """Bentuk cacat kelas ketiga belas, dijaga oleh angka dan bukan oleh niat."""
    isi = ringkasan_sintetis(tmp_path)
    assert EKSPEKTASI_AS_SEED42 < isi["sebaran_seed"]["rerata"]
    assert isi["besaran_terhadap_rerata_nol_R"] < isi["besaran_sumbangan_sinyal_R"]
    assert isi["jarak_as_seed42_dari_rerata_nol_sb"] < 0


def test_jarak_dari_rerata_nol_terhitung_dalam_simpangan_baku(tmp_path):
    isi = ringkasan_sintetis(tmp_path)
    std = isi["sebaran_seed"]["std"]
    rerata = isi["sebaran_seed"]["rerata"]
    assert std is not None and std > 0
    assert isi["jarak_ss_dari_rerata_nol_sb"] == pytest.approx(
        (EKSPEKTASI_SS - rerata) / std
    )
    assert isi["jarak_ss_dari_rerata_nol_sb"] > 0
    assert isi["ramalan"]["R-D3"]["jarak_ss_dari_rerata_nol_sb"] == pytest.approx(
        isi["jarak_ss_dari_rerata_nol_sb"]
    )


def test_putusan_r_d3_tetap_lahir_dari_angka_bukan_dari_prosa(tmp_path):
    isi = ringkasan_sintetis(tmp_path)
    r = isi["ramalan"]["R-D3"]
    assert r["seed_tertinggi_R"] == pytest.approx(isi["sebaran_seed"]["maks"])
    assert r["tepat"] is (r["seed_tertinggi_R"] > EKSPEKTASI_SS)
    assert r["tepat"] is False


def test_laporan_memuat_bunyi_asli_dan_koreksi_sekaligus(tmp_path):
    isi = ringkasan_sintetis(tmp_path)
    _, m = tulis_laporan(isi, tmp_path / "out", "uji_h013b_p")
    teks = m.read_text(encoding="utf-8")
    assert "bunyi asli:" in teks
    assert "koreksi:" in teks
    assert "permutasinya cacat" in teks
    assert "Besaran diukur dua kali" in teks
    assert "terhadap rerata sebaran nol" in teks
