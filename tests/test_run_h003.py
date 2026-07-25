"""Pengujian orkestrator H-003.

Yang dikunci: kriteria dan dataset benar-benar identik dengan dua hipotesis
sebelumnya, sidiknya berbeda, dan ruang pencarian tidak membengkak. Tanpa itu
perbandingan tiga hipotesis kehilangan artinya.
"""

from __future__ import annotations

import json
from pathlib import Path

from lux.backtest.engine import Konfig
from lux.backtest.run_h002 import hipotesis_h002
from lux.backtest.run_h003 import banding, hipotesis_h003
from lux.backtest.run_wf import hipotesis_h001

KONFIG = Konfig(maks_umur_bar=168, maks_carry_R=0.25)


def test_kriteria_identik_dengan_dua_hipotesis_sebelumnya():
    assert hipotesis_h003(KONFIG).kriteria == hipotesis_h001().kriteria
    assert hipotesis_h003(KONFIG).kriteria == hipotesis_h002(KONFIG).kriteria


def test_dataset_identik():
    assert hipotesis_h003(KONFIG).dataset == hipotesis_h001().dataset


def test_sidik_berbeda_dari_h002():
    """Mekanismenya lain, jadi pendaftarannya wajib lain."""
    assert hipotesis_h003(KONFIG).sidik() != hipotesis_h002(KONFIG).sidik()


def test_ruang_pencarian_tetap_tiga_kombinasi():
    h = hipotesis_h003(KONFIG)
    assert h.jumlah_kombinasi == 3
    assert h.ruang_parameter["jendela"] == [24, 72, 168]
    assert h.ruang_parameter["ambang"] == [2.0]


def test_id_hipotesis_baru():
    assert hipotesis_h003(KONFIG).id == "H-003"


def test_banding_tanpa_berkas_bukan_error(tmp_path):
    assert banding(tmp_path / "tidak_ada.json", "H-002") is None


def test_banding_membaca_p_entri_acak(tmp_path):
    p = tmp_path / "backtest_h002.json"
    p.write_text(
        json.dumps(
            {
                "gabungan": {
                    "ekspektasi_R": 0.0316,
                    "total_R": 596.44,
                    "jumlah_trade_luar_sampel": 18883,
                },
                "gerbang": {
                    "gerbang": [
                        {"nama": "invarian_risiko", "nilai": -1.3215},
                        {"nama": "entri_acak", "nilai": 0.0099},
                    ]
                },
                "putusan": {"lulus": False},
            }
        ),
        encoding="utf-8",
    )
    b = banding(p, "H-002")
    assert b["p_entri_acak"] == 0.0099
    assert b["label"] == "H-002"
