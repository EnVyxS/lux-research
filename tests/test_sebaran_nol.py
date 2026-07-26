"""Pengujian aritmetika sebaran nol (ADR-029 langkah 1).

Angka di dalam berkas ini kecil dan dihitung tangan, bukan disalin dari
keluaran modul. Pengujian yang bahannya diambil dari keluaran yang diuji hanya
membuktikan modul itu konsisten dengan dirinya sendiri.
"""

from __future__ import annotations

import pytest

from lux.analisis.sebaran_nol import (
    PEMBATAS,
    p_bulanan,
    p_ekor_atas,
    p_per_perdagangan,
    rerata_bulanan,
    rerata_bulanan_berbobot,
    selisih_bulanan,
)


def bulan(*baris: tuple[str, int, float]) -> list[dict]:
    """Baris bulanan seperti yang ditulis ``agregat_per_bulan``."""
    keluar = []
    for periode, trade, total in baris:
        keluar.append(
            {
                "periode": periode,
                "trade": trade,
                "total_R": total,
                "ekspektasi_R": total / trade,
                "dapat_dinilai": True,
                "sebab": "",
            }
        )
    return keluar


def test_p_teramati_di_atas_seluruh_nol_memakai_koreksi_satu():
    h = p_ekor_atas(0.5, [0.1, 0.2, 0.3])
    assert h["cacah_ge"] == 0
    # Bukan 0/3 = 0. Tiga tarikan tidak dapat membuktikan kemustahilan.
    assert h["p"] == pytest.approx(0.25)
    assert h["p_terkecil_yang_mungkin"] == pytest.approx(0.25)


def test_p_tidak_pernah_nol_bahkan_pada_tiga_ratus_tarikan():
    h = p_ekor_atas(99.0, [float(i) / 1000 for i in range(300)])
    assert h["p"] > 0
    assert h["p"] == pytest.approx(1 / 301)


def test_p_satu_ketika_seluruh_nol_mengalahkan_teramati():
    h = p_ekor_atas(0.05, [0.1, 0.2, 0.3])
    assert h["cacah_ge"] == 3
    assert h["p"] == pytest.approx(1.0)


def test_seri_dihitung_sebagai_bukti_melawan():
    h = p_ekor_atas(0.5, [0.5, 0.1])
    assert h["cacah_ge"] == 1
    assert h["p"] == pytest.approx(2 / 3)


def test_rerata_bulanan_memberi_bobot_sama_pada_tiap_bulan():
    b = bulan(("2025-01", 10, 5.0), ("2025-02", 30, 3.0))
    # (0,5 + 0,1) / 2, bukan 8/40.
    assert rerata_bulanan(b) == pytest.approx(0.3)


def test_rerata_berbobot_memberi_bobot_menurut_perdagangan():
    b = bulan(("2025-01", 10, 5.0), ("2025-02", 30, 3.0))
    assert rerata_bulanan_berbobot(b) == pytest.approx(8.0 / 40.0)


def test_himpunan_bulan_berbeda_ditolak_bukan_diselaraskan():
    a = bulan(("2025-01", 10, 1.0), ("2025-02", 10, 1.0))
    b = bulan(("2025-01", 10, 1.0), ("2025-03", 10, 1.0))
    with pytest.raises(ValueError, match="himpunan bulan tidak sama"):
        selisih_bulanan(a, b)


def test_urutan_baris_tidak_mengubah_hasil():
    a = bulan(("2025-01", 10, 5.0), ("2025-02", 10, 1.0))
    a_terbalik = list(reversed(a))
    assert rerata_bulanan(a) == pytest.approx(rerata_bulanan(a_terbalik))
    assert selisih_bulanan(a, a_terbalik) == pytest.approx(0.0)


def test_periode_ganda_ditolak():
    ganda = bulan(("2025-01", 10, 1.0)) + bulan(("2025-01", 10, 2.0))
    with pytest.raises(ValueError, match="periode ganda"):
        rerata_bulanan(ganda)


def test_berpasangan_dan_tak_berpasangan_menghasilkan_p_yang_sama():
    acuan = bulan(("2025-01", 10, 6.0), ("2025-02", 20, 4.0))
    nol = {
        1: bulan(("2025-01", 10, 1.0), ("2025-02", 20, 1.0)),
        2: bulan(("2025-01", 10, 9.0), ("2025-02", 20, 9.0)),
        3: bulan(("2025-01", 10, 2.0), ("2025-02", 20, 2.0)),
    }
    h = p_bulanan(acuan, nol)
    assert h["tak_berpasangan"]["p"] == pytest.approx(h["berpasangan"]["p"])
    assert h["sepakat"] is True
    # Satu seed dari tiga mengalahkan acuan, jadi (1 + 1) / (1 + 3).
    assert h["berpasangan"]["p"] == pytest.approx(0.5)


def test_keluaran_bulanan_menyatakan_satuan_dan_mengikat():
    acuan = bulan(("2025-01", 10, 6.0))
    h = p_bulanan(acuan, {1: bulan(("2025-01", 10, 1.0))})
    assert h["satuan"] == "bulan"
    assert h["mengikat"] is True
    assert h["taksiran_bawah"] is False
    assert h["n_bulan"] == 1
    assert "ADR-028" in h["pembatas"]


def test_keluaran_per_perdagangan_ditandai_taksiran_bawah_dan_tidak_mengikat():
    h = p_per_perdagangan(0.0666, {1: 0.01, 42: 0.02, 7: 0.03})
    assert h["satuan"] == "perdagangan"
    assert h["taksiran_bawah"] is True
    assert h["mengikat"] is False
    assert h["seed"] == [1, 7, 42]
    assert "MENJATUHKAN" in PEMBATAS
