"""Pengujian orkestrator H-011 (ADR-013 bagian 8).

Yang dikunci di sini bukan hasilnya, melainkan bahwa H-011 **tidak mengubah
mekanisme apa pun**. Sebuah H-011 yang diam-diam menggeser grid sambil
memperbesar semesta tidak menjawab pertanyaan apa pun, dan kekeliruan seperti
itu tidak akan terlihat dari angka keluarannya.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lux.backtest import run_h009, run_h010, run_h011
from lux.backtest.run_h002 import muat_konfig_h002

KONFIG = muat_konfig_h002(Path("config/lux.yaml"))


def test_grid_identik_dengan_h010():
    # Inti H-011: yang berubah semestanya, bukan mekanismenya.
    assert run_h011.LOOKBACK_H010 == run_h010.LOOKBACK
    assert run_h011.IMBALAN_H010 == run_h010.IMBALAN


def test_kandidat_identik_dengan_h010():
    assert run_h011.spek_h011(KONFIG).kandidat == run_h010.kandidat()
    assert len(run_h010.kandidat()) == 12


def test_buat_konfig_adalah_objek_yang_sama_dengan_h009():
    # Identitas objek, bukan kesamaan perilaku: salinan bisa melenceng,
    # identitas tidak bisa.
    assert run_h011.buat_konfig_h010 is run_h009.buat_konfig
    assert run_h011.spek_h011(KONFIG).buat_konfig is run_h009.buat_konfig


def test_dataset_identik_dengan_h009():
    assert run_h011.DATASET == run_h009.DATASET
    assert run_h011.hipotesis_h011(KONFIG).dataset == run_h009.DATASET


def test_id_dan_sidik_berbeda_dari_h010():
    h11 = run_h011.hipotesis_h011(KONFIG)
    h10 = run_h010.hipotesis_h010(KONFIG)
    assert h11.id == "H-011"
    assert h11.sidik() != h10.sidik()


def test_jumlah_kombinasi_tetap_dua_belas():
    # Semesta ditambahkan sebagai satu nilai, jadi multiplisitasnya tidak
    # berubah dan sebanding dengan H-007 sampai H-010.
    assert run_h011.hipotesis_h011(KONFIG).jumlah_kombinasi == 12


def test_pengaman_carry_terekam_tetapi_tidak_dicari():
    rp = run_h011.hipotesis_h011(KONFIG).ruang_parameter
    assert rp[run_h009.KUNCI_TERLARANG] == [run_h009.AMBANG_CARRY_KERAS]
    for p in run_h010.kandidat():
        assert run_h009.KUNCI_TERLARANG not in p


def test_kriteria_tidak_dilonggarkan_dan_tidak_diperketat():
    k = run_h011.hipotesis_h011(KONFIG).kriteria
    assert k.min_ekspektasi_R == 0.05
    assert k.min_trade_luar_sampel == 100
    assert k.maks_p_entri_acak == 0.05
    assert k.min_jendela_positif_rasio == 0.5


def test_spek_nama_dan_params_lookahead():
    s = run_h011.spek_h011(KONFIG)
    assert s.nama == "h011_semesta_penuh"
    assert s.params_lookahead == {"lookback": 55}


def test_batas_h010_adalah_empat_puluh():
    """Tripwire yang disengaja (aturan 18).

    Angka 40 hidup di satu tempat saja, ``BATAS_H010``, karena ia menentukan
    simbol mana yang dianggap tertahan. Bila ia bergeser tanpa sengaja,
    seluruh adjudikasi H-011 menilai kumpulan yang salah tanpa satu pun galat
    muncul. Pengujian ini ada supaya pergeseran itu berbunyi.
    """
    assert run_h011.BATAS_H010 == 40


def test_simbol_teruji_diambil_terurut_dari_berkas(tmp_path: Path):
    nama = [f"SYM{i:03d}USDT" for i in range(45)]
    p = tmp_path / "u.json"
    p.write_text(json.dumps({"simbol": list(reversed(nama))}), encoding="utf-8")
    teruji = run_h011.simbol_teruji(p)
    assert teruji == sorted(nama)[:40]
    assert len(teruji) == 40


def test_agregat_berbobot_perdagangan_bukan_rerata_dari_rerata():
    baris = [
        {"symbol": "A", "trade": 10, "total_R": 10.0},  # ekspektasi 1,0
        {"symbol": "B", "trade": 90, "total_R": 0.0},  # ekspektasi 0,0
    ]
    a = run_h011.agregat(baris)
    assert a["trade"] == 100
    assert abs(a["total_R"] - 10.0) < 1e-12
    # Berbobot: 0,10. Rerata dari rerata akan memberi 0,50.
    assert abs(a["ekspektasi_R"] - 0.1) < 1e-12


def test_agregat_tanpa_perdagangan_tidak_dapat_dinilai():
    a = run_h011.agregat([{"symbol": "A", "trade": 0, "total_R": 0.0}])
    assert a["dapat_dinilai"] is False
    assert a["ekspektasi_R"] is None
    assert a["sebab"]
    assert run_h011.agregat([])["dapat_dinilai"] is False


def test_pisah_tertahan_mengecualikan_tepat_simbol_terpakai():
    per_simbol = [
        {"symbol": "AAA", "trade": 10, "total_R": 5.0},
        {"symbol": "BBB", "trade": 20, "total_R": 4.0},
        {"symbol": "CCC", "trade": 30, "total_R": -3.0},
    ]
    pisah = run_h011.pisah_tertahan(per_simbol, ["AAA"])
    assert pisah["teruji"]["n_simbol"] == 1
    assert pisah["tertahan"]["n_simbol"] == 2
    assert pisah["tertahan"]["trade"] == 50
    assert abs(pisah["tertahan"]["total_R"] - 1.0) < 1e-12
    assert abs(pisah["tertahan"]["ekspektasi_R"] - 0.02) < 1e-12
    assert abs(pisah["teruji"]["ekspektasi_R"] - 0.5) < 1e-12


def test_limit_yang_tidak_menyisakan_simbol_asing_ditolak():
    with pytest.raises(ValueError):
        run_h011.main(["--dir", "aset", "--limit", "40"])
    with pytest.raises(ValueError):
        run_h011.main(["--dir", "aset", "--limit", "1"])


def test_ulangan_tidak_boleh_diturunkan():
    # Resolusi p adalah alasan hipotesis ini ada; menurunkannya setelah melihat
    # p 0,049505 milik H-010 adalah penyetelan terhadap hasil.
    with pytest.raises(ValueError):
        run_h011.main(["--dir", "aset", "--limit", "0", "--ulangan", "50"])


def test_ramalan_tertulis_dan_merugikan_hipotesis_sendiri():
    assert len(run_h011.RAMALAN) == 7
    assert "gagal" in run_h011.RAMALAN["ekspektasi_tertahan_R"].lower()
    for isi in run_h011.RAMALAN.values():
        assert isi.strip()
