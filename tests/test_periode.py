"""Pengujian agregat per periode waktu (ADR-014 bagian 8).

Satu pengujian memuat batas periode tahan H-012 secara harfiah sebagai
tripwire (aturan 10): bila batas itu digeser sesudah hasil terlihat, baris itu
yang berbunyi.
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from lux.analisis.periode import (
    KUNCI,
    agregat_per_bulan,
    agregat_sebelum,
    agregat_sejak,
    bandingkan_batas,
    bulan_dari_ms,
    dari_perdagangan,
    ms_dari_tanggal,
)

AWAL_2026 = ms_dari_tanggal("2026-01-01")
HARI = 86_400_000


@dataclass
class PerdaganganPalsu:
    masuk_ms: int
    R: float


def test_tanggal_ke_ms_utc():
    # 2026-01-01T00:00:00Z. Diperiksa terhadap nilai yang dihitung terpisah,
    # bukan terhadap fungsi yang sedang diuji.
    assert AWAL_2026 == 1_767_225_600_000
    assert ms_dari_tanggal("1970-01-01") == 0


def test_bulan_dari_ms_memakai_utc():
    assert bulan_dari_ms(AWAL_2026) == "2026-01"
    assert bulan_dari_ms(AWAL_2026 - 1) == "2025-12"
    assert bulan_dari_ms(AWAL_2026 + 40 * HARI) == "2026-02"


def test_batas_periode_tahan_h012_tidak_boleh_digeser():
    # Tripwire pra-registrasi. Batas H-012 dibekukan pada 2026-01-01 UTC
    # sebelum satu angka hasil pun dilihat.
    assert ms_dari_tanggal("2026-01-01") == 1_767_225_600_000


def test_agregat_per_bulan_berbobot_perdagangan():
    pasangan = [
        (AWAL_2026, 1.0),
        (AWAL_2026 + HARI, -3.0),
        (AWAL_2026 + 40 * HARI, 2.0),
    ]
    baris = agregat_per_bulan(pasangan)
    assert [b["periode"] for b in baris] == ["2026-01", "2026-02"]
    assert baris[0]["trade"] == 2
    assert baris[0]["total_R"] == pytest.approx(-2.0)
    assert baris[0]["ekspektasi_R"] == pytest.approx(-1.0)
    assert baris[1]["ekspektasi_R"] == pytest.approx(2.0)
    for b in baris:
        for k in KUNCI:
            assert k in b


def test_agregat_per_bulan_terurut_dan_tidak_kehilangan_perdagangan():
    pasangan = [(AWAL_2026 + i * 20 * HARI, 0.1) for i in range(12)]
    baris = agregat_per_bulan(pasangan)
    assert [b["periode"] for b in baris] == sorted(b["periode"] for b in baris)
    assert sum(b["trade"] for b in baris) == 12


def test_agregat_per_bulan_kosong():
    assert agregat_per_bulan([]) == []


def test_titik_batas_dimiliki_periode_tahan():
    # Perbandingan >= : perdagangan tepat di batas masuk periode tahan.
    tahan = agregat_sejak([(AWAL_2026, 1.0)], AWAL_2026)
    assert tahan["trade"] == 1
    lama = agregat_sebelum([(AWAL_2026, 1.0)], AWAL_2026)
    assert lama["trade"] == 0


def test_agregat_sejak_memisahkan_dengan_benar():
    pasangan = [
        (AWAL_2026 - 10 * HARI, 5.0),
        (AWAL_2026 + 10 * HARI, -1.0),
        (AWAL_2026 + 200 * HARI, -1.0),
    ]
    tahan = agregat_sejak(pasangan, AWAL_2026)
    assert tahan["trade"] == 2
    assert tahan["ekspektasi_R"] == pytest.approx(-1.0)
    assert agregat_sebelum(pasangan, AWAL_2026)["ekspektasi_R"] == pytest.approx(5.0)


def test_periode_kosong_tidak_dapat_dinilai_bukan_nol():
    # Ekspektasi nol dan ekspektasi yang tidak ada adalah dua hal berbeda;
    # menyamakannya membuat periode tanpa perdagangan tampak netral.
    kosong = agregat_sejak([(AWAL_2026 - HARI, 1.0)], AWAL_2026)
    assert kosong["trade"] == 0
    assert kosong["ekspektasi_R"] is None
    assert kosong["dapat_dinilai"] is False
    assert "tidak ada perdagangan" in kosong["sebab"]


def test_bandingkan_batas_utuh():
    pasangan = [(AWAL_2026 + (i - 5) * 30 * HARI, float(i)) for i in range(10)]
    b = bandingkan_batas(pasangan, AWAL_2026)
    assert b["utuh"] is True
    assert b["n_masuk"] == 10
    assert b["tahan"]["trade"] + b["sebelum"]["trade"] == 10


def test_dari_perdagangan_membaca_masuk_ms_dan_R():
    trades = [
        PerdaganganPalsu(masuk_ms=AWAL_2026, R=0.5),
        PerdaganganPalsu(masuk_ms=AWAL_2026 + HARI, R=-0.5),
    ]
    pasangan = dari_perdagangan(trades)
    assert pasangan == [(AWAL_2026, 0.5), (AWAL_2026 + HARI, -0.5)]
    assert agregat_sejak(pasangan, AWAL_2026)["total_R"] == pytest.approx(0.0)


def test_penjumlahan_banyak_pecahan_tidak_kehilangan_digit():
    # fsum, bukan sum: 100.000 kali 0,1 harus tepat 10.000.
    pasangan = [(AWAL_2026 + i, 0.1) for i in range(100_000)]
    b = agregat_sejak(pasangan, AWAL_2026)
    assert b["total_R"] == pytest.approx(10_000.0, abs=1e-9)
