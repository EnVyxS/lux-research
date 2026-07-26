"""Pengujian H-014. Yang dijaga di sini adalah aturan 52 dan larangan LULUS."""

from __future__ import annotations

from dataclasses import asdict
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from lux.backtest import run_h013 as h13
from lux.backtest import run_h014 as m
from lux.backtest.engine import Konfig
from lux.backtest.run_h013b import NAMA_SPEK as NAMA_SPEK_B
from lux.praregistrasi import Kriteria
from lux.strategi import breakout_atr


def bingkai(n: int = 600) -> pd.DataFrame:
    rng = np.random.default_rng(7)
    harga = 100.0 + np.cumsum(rng.normal(0.0, 1.0, size=n))
    harga = np.abs(harga) + 10.0
    return pd.DataFrame(
        {
            "open_time": np.arange(n, dtype="int64") * 14_400_000,
            "open": harga,
            "high": harga + 1.0,
            "low": harga - 1.0,
            "close": harga,
            "volume": np.full(n, 1000.0),
        }
    )


def args_palsu(**ganti) -> SimpleNamespace:
    dasar = dict(
        dir="aset",
        out="reports",
        interval="4h",
        universe="reports/universe_layak_v2_4h.json",
        akhir_sejati="reports/akhir_sejati_4h.json",
        limit=40,
        min_median_stop_frac=0.004,
    )
    dasar.update(ganti)
    return SimpleNamespace(**dasar)


def test_dua_sel_saja():
    assert m.NAMA_SEL == ("SSp", "SHp")
    assert len(m.NAMA_LAPORAN_H014) == 2


def test_nama_laporan_tidak_menimpa_h013():
    assert not set(m.NAMA_LAPORAN_H014.values()) & set(h13.NAMA_LAPORAN.values())


def test_nama_laporan_bukan_nama_spek_jalur_b():
    assert NAMA_SPEK_B not in set(m.NAMA_LAPORAN_H014.values())


def test_periksa_nama_lulus():
    assert m.periksa_nama() is True


def test_umur_sama_di_kedua_sel():
    assert m.umur_sel_h014("SSp") == m.umur_sel_h014("SHp") == h13.H_BAR == 48


def test_umur_bukan_42_yang_mencampur_dua_medan():
    assert m.UMUR_SETARA != h13.UMUR_SEL_STOP


def test_pakai_target_satu_nyala_satu_mati():
    assert m.pakai_target_h014("SSp") is True
    assert m.pakai_target_h014("SHp") is False


def test_sel_asing_ditolak():
    with pytest.raises(ValueError):
        m.pakai_target_h014("SS")
    with pytest.raises(ValueError):
        m.umur_sel_h014("AH")


def test_tepat_satu_medan_berbeda():
    assert m.medan_berbeda(Konfig()) == ["pakai_target"]


def test_konfig_sel_menghormati_pagar_engine():
    sh = m.konfig_sel_h014("SHp", Konfig())
    assert sh.pakai_target is False and sh.maks_umur_bar > 0
    assert asdict(sh)["imbalan_R"] == h13.IMBALAN_BEKU


def test_putusan_mungkin_tanpa_lulus():
    assert m.PUTUSAN_MUNGKIN == ("DITOLAK", "TIDAK DAPAT DINILAI")
    assert "LULUS" not in m.PUTUSAN_MUNGKIN


def test_ambang_dinyatakan_baru():
    assert m.AMBANG_BESARAN_R == 0.020
    assert "2026-07-27" in m.CATATAN_AMBANG
    assert "BARU" in m.CATATAN_AMBANG


def test_pembatas_menyatakan_mustahil_lulus():
    assert "MUSTAHIL LULUS" in m.PEMBATAS
    assert "0,029481" in m.PEMBATAS


def test_sinyal_nyata_tidak_diacak():
    df = bingkai()
    p = h13.kandidat()[0]
    assert np.array_equal(m.sinyal_nyata(df, p), breakout_atr.sinyal(df, p))


def test_hipotesis_id_beda_antar_sel():
    a = m.hipotesis_h014("SSp", Konfig())
    b = m.hipotesis_h014("SHp", Konfig())
    assert a.id != b.id
    assert a.id.startswith("H-014-") and b.id.startswith("H-014-")
    assert a.sidik() != b.sidik()


def test_kriteria_per_sel_tidak_dilonggarkan():
    assert asdict(m.hipotesis_h014("SSp", Konfig()).kriteria) == asdict(Kriteria())


def test_spek_tanpa_buat_konfig():
    assert m.spek_h014("SSp", Konfig()).buat_konfig is None


def test_opsi_menyalakan_gerbang_entri_acak():
    o = m.opsi_h014(args_palsu(), h13.jendela_bar("4h"))
    assert o.sampel_permutasi > 0
    assert o.ulangan == h13.MIN_ULANGAN


def test_main_menolak_interval_bukan_4h():
    assert m.main(["--dir", "aset", "--interval", "1h", "--min-median-stop-frac", "0.004"]) == 2


def test_main_menolak_lantai_mati():
    assert m.main(["--dir", "aset", "--min-median-stop-frac", "0"]) == 2
