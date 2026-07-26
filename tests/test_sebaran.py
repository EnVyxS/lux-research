"""Pengujian modul sebaran (utang ADR-013 bagian 7).

Modul ini dibangun karena laporan yang dikomit tidak memuat simpangan baku,
sehingga tidak ada hipotesis — termasuk H-010 yang sudah lulus — yang dapat
dinilai secara statistik. Pengujian di bawah mengunci hal-hal yang mudah salah
tanpa terlihat salah: ddof, pembagian nol, dan nilai tidak finit.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass

import pytest

from lux.analisis.sebaran import (
    KUNCI,
    Z_95,
    dari_perdagangan,
    jarak_ambang,
    ukur_sebaran,
)


@dataclass
class PerdaganganPalsu:
    R: float


def test_std_memakai_ddof_1_bukan_ddof_0():
    u = ukur_sebaran([1.0, 2.0, 3.0, 4.0])
    # ddof=1: sqrt(5/3) = 1.2909944487358056
    assert abs(u["std_R"] - 1.2909944487358056) < 1e-12
    # ddof=0 akan memberi 1.118033988749895; memakainya berarti menyatakan
    # sampel ini adalah seluruh populasi perdagangan yang mungkin.
    assert abs(u["std_R"] - 1.118033988749895) > 1e-6


def test_galat_baku_adalah_std_dibagi_akar_n():
    u = ukur_sebaran([1.0, 2.0, 3.0, 4.0])
    assert abs(u["galat_baku_R"] - u["std_R"] / math.sqrt(4)) < 1e-15
    assert abs(u["galat_baku_R"] - 0.6454972243679028) < 1e-12


def test_rerata_cocok_dengan_hitungan_tangan():
    u = ukur_sebaran([1.0, 2.0, 3.0, 4.0])
    assert abs(u["rerata_R"] - 2.5) < 1e-15
    assert u["n"] == 4
    assert u["dapat_dinilai"] is True


def test_kuartil_terurut_dan_ekstrem_benar():
    u = ukur_sebaran([float(i) for i in range(1, 11)])
    assert u["min_R"] == 1.0
    assert u["maks_R"] == 10.0
    assert u["min_R"] <= u["q1_R"] <= u["median_R"] <= u["q3_R"] <= u["maks_R"]


def test_selang_kepercayaan_simetris_terhadap_rerata():
    u = ukur_sebaran([1.0, 2.0, 3.0, 4.0])
    tengah = (u["ci95_bawah_R"] + u["ci95_atas_R"]) / 2
    assert abs(tengah - u["rerata_R"]) < 1e-12
    lebar = u["ci95_atas_R"] - u["ci95_bawah_R"]
    assert abs(lebar - 2 * Z_95 * u["galat_baku_R"]) < 1e-12


def test_satu_perdagangan_tidak_dapat_dinilai():
    u = ukur_sebaran([0.5])
    assert u["n"] == 1
    assert u["dapat_dinilai"] is False
    assert u["std_R"] is None
    assert u["galat_baku_R"] is None
    assert u["rerata_R"] == 0.5
    assert u["sebab"]


def test_kosong_tidak_dapat_dinilai():
    u = ukur_sebaran([])
    assert u["n"] == 0
    assert u["dapat_dinilai"] is False
    assert u["rerata_R"] is None
    assert u["sebab"]


def test_nilai_tidak_finit_ditolak_keras():
    with pytest.raises(ValueError):
        ukur_sebaran([0.1, float("nan")])
    with pytest.raises(ValueError):
        ukur_sebaran([0.1, float("inf")])


def test_urutan_masukan_tidak_mengubah_hasil():
    """Sifat yang dijamin adalah kesamaan sampai presisi float, bukan bit.

    Versi pertama pengujian ini menuntut kesamaan bit dan GAGAL di run commit
    `a911e99e`: rerata 0.28 lawan 0.27999999999999997, selisih satu satuan
    terakhir. Penjumlahan float tidak asosiatif, jadi yang salah adalah
    tuntutannya, bukan modulnya. Menuntut kesamaan bit atas agregat float adalah
    pengujian yang akan menyala pada perilaku yang benar.
    """
    xs = [0.3, -1.0, 2.5, 0.0, -0.4]
    a = ukur_sebaran(xs)
    b = ukur_sebaran(list(reversed(xs)))
    assert set(a) == set(b)
    for k in a:
        if isinstance(a[k], float):
            assert abs(a[k] - b[k]) < 1e-12, k
        else:
            assert a[k] == b[k], k


def test_seluruh_kunci_selalu_ada():
    for xs in ([], [0.5], [0.5, 1.5]):
        u = ukur_sebaran(xs)
        assert set(u) == set(KUNCI)


def test_sebaran_nol_tidak_membagi_nol():
    u = ukur_sebaran([0.5] * 10)
    assert u["dapat_dinilai"] is True
    assert u["std_R"] == 0.0
    assert u["galat_baku_R"] == 0.0
    j = jarak_ambang(u, 0.05)
    assert j["jarak_galat_baku"] is None
    assert j["dapat_dinilai"] is False
    assert abs(j["jarak_R"] - 0.45) < 1e-12


def test_jarak_dalam_satuan_galat_baku_dihitung_benar():
    # [1, 3]: rerata 2, std ddof=1 = sqrt(2), galat baku = sqrt(2)/sqrt(2) = 1.
    u = ukur_sebaran([1.0, 3.0])
    assert abs(u["galat_baku_R"] - 1.0) < 1e-15
    j = jarak_ambang(u, 1.0)
    assert abs(j["jarak_R"] - 1.0) < 1e-15
    assert abs(j["jarak_galat_baku"] - 1.0) < 1e-15
    assert j["dapat_dinilai"] is True


def test_jarak_negatif_bila_rerata_di_bawah_ambang():
    u = ukur_sebaran([1.0, 3.0])
    j = jarak_ambang(u, 5.0)
    assert j["jarak_R"] < 0
    assert j["jarak_galat_baku"] < 0


def test_jarak_ambang_atas_ukuran_tak_ternilai():
    j = jarak_ambang(ukur_sebaran([]), 0.05)
    assert j["dapat_dinilai"] is False
    assert j["jarak_R"] is None
    assert j["sebab"]


def test_dari_perdagangan_mengambil_R_dan_hasil_dapat_diserialkan():
    trades = [PerdaganganPalsu(R=0.4), PerdaganganPalsu(R=-1.0)]
    assert dari_perdagangan(trades) == [0.4, -1.0]
    u = ukur_sebaran(dari_perdagangan(trades))
    # Laporan JSON tidak boleh gagal karena tipe numpy yang menyelip.
    json.dumps(u)
    json.dumps(jarak_ambang(u, 0.05))
