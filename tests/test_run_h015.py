"""Uji runner H-015 (ADR-037 \u00a77).

Seluruh berkas ini berjalan tanpa satu bar parquet pun. Yang diuji adalah tiga
kewajiban runner dan aritmetika putusannya — bukan hasil backtest, yang memang
belum ada dan tidak boleh diramalkan dari sini.

Konfig dasar dibangun dari ``config/lux.yaml`` yang **sungguhan**, bukan dari
bawaan ``Konfig()``. Itu perbedaan yang sempat membuat run pengujian atas commit
4e6a6584 gagal, dan perbedaan itu justru gunanya: bawaan ``Konfig`` memuat
``maks_carry_R = 0.0`` sedangkan config memuat 0,25, sehingga fixture yang
memakai bawaan akan menguji konfig yang tidak pernah dijalankan siapa pun. Dengan
membaca config, berkas ini menjadi pagar berdiri: bila kelak ada yang menurunkan
``risiko.maks_carry_R``, run empat jam H-015 akan berhenti dengan kode 3 — dan
pytest mengatakannya lebih dahulu dalam tiga detik.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from lux.backtest.engine import Konfig
from lux.backtest.konfig_audit import laporan_kesebandingan
from lux.backtest.run_h002 import muat_konfig_h002
from lux.backtest.run_h013 import AMBANG_KONTRIBUSI_SINYAL, H_BAR, MIN_TRADE_SEL
from lux.backtest.run_h015 import (
    DATASET,
    NAMA_LAPORAN,
    NAMA_SEL,
    PEMBATAS_PUTUSAN,
    PENGAMAN_WAJIB,
    RAMALAN,
    buat_konfig_h015,
    hipotesis_h015,
    kandidat,
    konfig_dasar_h015,
    kontribusi_h015,
    main,
    prosa_h015,
)

CONTOH = {"lookback": 55, "imbalan_R": 2.0}

# Jalur config diturunkan dari letak berkas uji, bukan dari direktori kerja:
# uji yang hanya lulus bila dijalankan dari akar repo adalah uji yang akan
# gugur di tempat yang tidak ada hubungannya dengan isinya.
JALUR_CONFIG = Path(__file__).resolve().parents[1] / "config" / "lux.yaml"


def konfig_config() -> Konfig:
    return muat_konfig_h002(JALUR_CONFIG)


def dasar():
    return konfig_dasar_h015(konfig_config())


def ekspektasi(k=0.03, f=0.05, a=0.04):
    return {"K": k, "F": f, "A": a}


def trade(n=500):
    return {s: n for s in NAMA_SEL}


# --------------------------------------------------------------------------
# Pengaman: kewajiban ADR-037 §7
# --------------------------------------------------------------------------
def test_pengaman_wajib_menuntut_kedua_medan_carry():
    assert PENGAMAN_WAJIB == {
        "maks_carry_realisasi_R": 0.25,
        "maks_carry_R": 0.25,
    }


def test_config_memenuhi_pengaman_yang_dituntut_run():
    """Kaitan yang membuat run empat jam berhenti di detik pertama, bukan jam keempat.

    ``maks_carry_R`` datang dari ``config/lux.yaml`` dan **bukan** dipasang oleh
    kode H-015. Karena itu tuntutan di ``PENGAMAN_WAJIB`` bukan tautologi di
    medan ini: ia dapat gagal, dan bila ia gagal, ia gagal di sini.
    """
    assert konfig_config().maks_carry_R == PENGAMAN_WAJIB["maks_carry_R"]


def test_konfig_dasar_menyalakan_pengaman_carry_terealisasi():
    """Aturan 57. Bawaan Konfig adalah 0,0, dan itu keadaan H-014."""
    assert Konfig().maks_carry_realisasi_R == 0.0
    assert dasar().maks_carry_realisasi_R == 0.25


def test_audit_tidak_menghalangi_saat_pengaman_hidup():
    k = buat_konfig_h015(CONTOH, dasar())
    lap = laporan_kesebandingan("H-015-F", k, "H-013 SS", k, PENGAMAN_WAJIB)
    assert lap["pengaman_mati"] == []
    assert lap["menghalangi"] is False


def test_audit_menghalangi_saat_pengaman_dimatikan():
    """Persis keadaan H-014: medan itu 0,0 dan tidak seorang pun bertanya."""
    mati = replace(buat_konfig_h015(CONTOH, dasar()), maks_carry_realisasi_R=0.0)
    lap = laporan_kesebandingan("H-015-F", mati, "H-013 SS", mati, PENGAMAN_WAJIB)
    assert lap["pengaman_mati"] == ["maks_carry_realisasi_R"]
    assert lap["menghalangi"] is True


def test_audit_mencatat_seluruh_medan_konfig_bukan_pilihan():
    k = buat_konfig_h015(CONTOH, dasar())
    lap = laporan_kesebandingan("H-015-F", k, "H-013 SS", k, PENGAMAN_WAJIB)
    assert len(lap["konfig"]) == len(vars(k))
    assert "maks_carry_realisasi_R" in lap["konfig"]


# --------------------------------------------------------------------------
# Konfig sel
# --------------------------------------------------------------------------
def test_konfig_sel_memakai_horizon_48_bukan_42():
    assert buat_konfig_h015(CONTOH, dasar()).maks_umur_bar == H_BAR == 48


def test_konfig_sel_memasang_target():
    assert buat_konfig_h015(CONTOH, dasar()).pakai_target is True


def test_konfig_identik_untuk_ketiga_sel():
    """Yang boleh membedakan sel hanyalah fungsi sinyalnya."""
    k = [buat_konfig_h015(CONTOH, dasar()) for _ in NAMA_SEL]
    assert k[0] == k[1] == k[2]


def test_kandidat_hanya_melombakan_lookback():
    for p in kandidat():
        assert set(p) == {"lookback", "imbalan_R"}
        assert p["imbalan_R"] == 2.0


def test_kandidat_berjumlah_tiga():
    assert len(kandidat()) == 3


# --------------------------------------------------------------------------
# Hipotesis pra-registrasi
# --------------------------------------------------------------------------
def test_pernyataan_menyebut_pasal_yang_mengikat():
    p = hipotesis_h015("F", dasar()).pernyataan
    assert "ADR-037 \u00a75 mengikat" in p


def test_pernyataan_menyebut_f_min_k_haram():
    assert "haram" in hipotesis_h015("F", dasar()).pernyataan


def test_sidik_berbeda_antar_sel():
    """Bila dua sel bersidik sama, keduanya hipotesis yang sama."""
    sidik = {hipotesis_h015(s, dasar()).sidik() for s in NAMA_SEL}
    assert len(sidik) == 3


def test_dataset_menyebut_4h():
    assert "4h" in DATASET


def test_sel_tidak_dikenal_ditolak_hipotesis():
    with pytest.raises(ValueError, match="sel tidak dikenal"):
        hipotesis_h015("SS", dasar())


def test_nama_laporan_lengkap_dan_tidak_bertabrakan():
    assert set(NAMA_LAPORAN) == set(NAMA_SEL)
    assert len(set(NAMA_LAPORAN.values())) == 3


# --------------------------------------------------------------------------
# Aritmetika putusan
# --------------------------------------------------------------------------
def test_selisih_mengikat_adalah_f_minus_a():
    r = kontribusi_h015(ekspektasi(k=0.01, f=0.05, a=0.04), trade())
    assert r["selisih_mengikat_F_A_R"] == pytest.approx(0.01)


def test_selisih_tidak_mengikat_adalah_f_minus_k():
    r = kontribusi_h015(ekspektasi(k=0.01, f=0.05, a=0.04), trade())
    assert r["selisih_TIDAK_mengikat_F_K_R"] == pytest.approx(0.04)


def test_besaran_f_min_k_yang_besar_tidak_meluluskan():
    """Inti falsifikasi: unggul jauh atas kontrol, kalah atas acak."""
    r = kontribusi_h015(ekspektasi(k=-0.50, f=0.05, a=0.045), trade())
    assert r["selisih_TIDAK_mengikat_F_K_R"] > AMBANG_KONTRIBUSI_SINYAL
    assert r["lulus"] is False


def test_lulus_besaran_tepat_di_ambang():
    r = kontribusi_h015(ekspektasi(f=0.02, a=0.0), trade())
    assert r["selisih_mengikat_F_A_R"] == AMBANG_KONTRIBUSI_SINYAL
    assert r["lulus"] is True


def test_ambang_tidak_dilunakkan_oleh_pembulatan():
    """0,06 \u2212 0,04 bernilai 0,019999999999999997 dalam float biner.

    Karena itu ia **tidak** lulus, dan itu memang yang dikehendaki: membulatkan
    perbandingan berarti menggeser ambang beku ke bawah, dan ambang H-015 tidak
    bergerak sesudah kodenya ditulis (ADR-037 \u00a710). Tepi pisau ini dikunci di
    sini supaya kelak tidak ada yang "memperbaikinya" tanpa menyadari apa yang
    sedang ia geser.
    """
    r = kontribusi_h015(ekspektasi(f=0.06, a=0.04), trade())
    assert r["selisih_mengikat_F_A_R"] < AMBANG_KONTRIBUSI_SINYAL
    assert r["lulus"] is False


def test_sel_tipis_membuat_tidak_dapat_dinilai():
    t = trade()
    t["F"] = MIN_TRADE_SEL - 1
    r = kontribusi_h015(ekspektasi(), t)
    assert r["dapat_dinilai"] is False
    assert r["lulus"] is False
    assert r["selisih_mengikat_F_A_R"] is None


def test_ekspektasi_kosong_membuat_tidak_dapat_dinilai():
    e = ekspektasi()
    e["A"] = None
    assert kontribusi_h015(e, trade())["dapat_dinilai"] is False


def test_sel_kurang_ditolak():
    with pytest.raises(ValueError, match="sel tidak lengkap"):
        kontribusi_h015({"K": 0.0, "F": 0.0}, trade())


# --------------------------------------------------------------------------
# Prosa
# --------------------------------------------------------------------------
def test_prosa_selalu_memuat_pembatas_putusan():
    for r in (
        kontribusi_h015(ekspektasi(), trade()),
        kontribusi_h015(ekspektasi(), {s: 1 for s in NAMA_SEL}),
    ):
        assert any(PEMBATAS_PUTUSAN in b for b in prosa_h015(r))


def test_prosa_menyebut_negatif_saat_saringan_kalah_dari_acak():
    r = kontribusi_h015(ekspektasi(f=0.03, a=0.05), trade())
    assert any("negatif" in b for b in prosa_h015(r))


def test_prosa_membalik_arah_saat_f_a_lebih_besar():
    """Prosa yang tidak dapat salah adalah prosa yang tidak memuat informasi."""
    r = kontribusi_h015(ekspektasi(k=0.049, f=0.05, a=0.01), trade())
    assert any("membalik" in b for b in prosa_h015(r))


def test_prosa_tidak_dapat_dinilai_tidak_menafsirkan_apa_pun():
    r = kontribusi_h015(ekspektasi(), {s: 1 for s in NAMA_SEL})
    teks = " ".join(prosa_h015(r))
    assert "TIDAK DAPAT DINILAI" in teks


# --------------------------------------------------------------------------
# Pagar argumen: berjalan sebelum satu bar pun dimuat
# --------------------------------------------------------------------------
def argumen(**ganti):
    a = {
        "--dir": "aset",
        "--interval": "4h",
        "--universe": "reports/universe_layak_v2_4h.json",
        "--akhir-sejati": "reports/akhir_sejati_4h.json",
        "--min-median-stop-frac": "0.004",
        "--ulangan": "300",
    }
    a.update(ganti)
    keluar = []
    for k, v in a.items():
        keluar += [k, v]
    return keluar


def test_ulangan_kurang_ditolak():
    assert main(argumen(**{"--ulangan": "299"})) == 2


def test_interval_bukan_4h_ditolak():
    assert main(argumen(**{"--interval": "1h"})) == 2


def test_universe_1h_ditolak():
    assert main(argumen(**{"--universe": "reports/universe_layak_v2.json"})) == 2


def test_lantai_mati_ditolak():
    assert main(argumen(**{"--min-median-stop-frac": "0"})) == 2


# --------------------------------------------------------------------------
# Ramalan
# --------------------------------------------------------------------------
def test_lima_ramalan_terdaftar():
    assert set(RAMALAN) == {"R-L1", "R-L2", "R-L3", "R-L4", "R-L5"}


def test_ramalan_utama_menyatakan_ditolak():
    """Ramalan yang tidak dapat meleset bukan ramalan."""
    assert "DITOLAK" in RAMALAN["R-L2"]
