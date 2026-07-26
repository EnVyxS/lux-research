"""Arah kalimat penafsir H-013 wajib mengikuti angka (aturan 41, cacat kesepuluh).

Sampai commit ini penulis laporan mencetak "sumbangan geometri yang lebih besar
daripada sumbangan sinyal" pada nilai apa pun, dan pada run 30214203863 angkanya
justru sebaliknya. Yang diuji di sini bukan bunyi kalimatnya melainkan
**ketergantungannya pada angka**: satu masukan menghasilkan satu arah, masukan
yang dibalik menghasilkan arah yang lain.

Satu pengujian di berkas ini adalah tripwire tekstual atas sumber ``run_h013``,
dan kelemahannya dinyatakan terbuka: ia menjaga agar kalimat yang dipatok tidak
kembali dan agar penulis md tetap memanggil ``prosa_kontribusi``, tetapi ia tidak
menjaga isi laporan yang sungguh ditulis di runner.
"""

from __future__ import annotations

import inspect

from lux.backtest import run_h013
from lux.backtest.run_h013 import (
    AMBANG_KONTRIBUSI_SINYAL,
    PEMBATAS_INVARIAN,
    PEMBATAS_PUTUSAN,
    kontribusi,
    prosa_kontribusi,
)


def teks(ringkas: dict) -> str:
    return "\n".join(prosa_kontribusi(ringkas))


def test_geometri_dominan_menghasilkan_kalimat_geometri():
    # SS 0,060 SH 0,010 AS 0,050 AH 0,000 -> sinyal 0,010, geometri 0,050
    r = kontribusi(
        {"SS": 0.060, "SH": 0.010, "AS": 0.050, "AH": 0.000},
        dict.fromkeys(run_h013.NAMA_SEL, 500),
    )
    t = teks(r)
    assert "Sumbangan **geometri**" in t
    assert "Sumbangan **sinyal** (" not in t
    assert "mengukur struktur" in t


def test_sinyal_dominan_membalik_kalimat():
    """Angka run 30214203863: sinyal +0,054842R lawan geometri +0,029481R.

    Inilah keadaan tempat prosa lama berbohong. Bila kalimat lama kembali, uji
    ini jatuh.
    """
    r = kontribusi(
        {"SS": 0.066648, "SH": 0.037167, "AS": 0.011806, "AH": 0.058170},
        {"SS": 60018, "SH": 44614, "AS": 55927, "AH": 45378},
    )
    t = teks(r)
    assert "Sumbangan **sinyal**" in t
    assert "membalik" in t
    # Kalimat yang dipatok itu tidak boleh muncul ketika angkanya berlawanan.
    assert "geometri** (" not in t.split("Sumbangan **sinyal**")[0]
    assert "mengukur struktur" not in t


def test_sumbangan_sinyal_negatif_dinyatakan_terbuka():
    r = kontribusi(
        {"SS": 0.020, "SH": 0.010, "AS": 0.050, "AH": 0.000},
        dict.fromkeys(run_h013.NAMA_SEL, 500),
    )
    t = teks(r)
    assert "negatif" in t
    assert "kalah dari sinyal yang waktunya diacak" in t


def test_di_bawah_ambang_disebut_di_bawah_ambang():
    # sinyal 0,010 < 0,020, dan ambangnya dibaca dari ringkas, bukan diketik.
    r = kontribusi(
        {"SS": 0.060, "SH": 0.010, "AS": 0.050, "AH": 0.000},
        dict.fromkeys(run_h013.NAMA_SEL, 500),
    )
    assert r["ambang_sumbangan_sinyal_R"] == AMBANG_KONTRIBUSI_SINYAL
    t = teks(r)
    assert "**di bawah** ambang" in t
    assert "tidak digeser" in t


def test_dua_pembatas_selalu_ikut_termasuk_saat_tak_ternilai():
    """Keterbatasan putusan tidak bergantung angka, jadi ia tidak boleh hilang."""
    r_nilai = kontribusi(
        {"SS": 0.060, "SH": 0.010, "AS": 0.050, "AH": 0.000},
        dict.fromkeys(run_h013.NAMA_SEL, 500),
    )
    r_tipis = kontribusi(
        {"SS": 0.060, "SH": 0.010, "AS": 0.050, "AH": 0.000},
        dict.fromkeys(run_h013.NAMA_SEL, 500) | {"AH": 3},
    )
    for r in (r_nilai, r_tipis):
        t = teks(r)
        assert PEMBATAS_PUTUSAN in t
        assert PEMBATAS_INVARIAN in t
    # Saat tak ternilai, tidak boleh ada kalimat yang menafsirkan besaran.
    t_tipis = teks(r_tipis)
    assert "TIDAK DAPAT DINILAI" in t_tipis
    assert "Sumbangan **geometri**" not in t_tipis
    assert "Sumbangan **sinyal**" not in t_tipis
    # Dan pembatas putusan wajib menyebut kedua ADR yang melahirkannya.
    assert "ADR-024" in PEMBATAS_PUTUSAN
    assert "ADR-028" in PEMBATAS_PUTUSAN


def test_tripwire_prosa_tidak_lagi_dipatok_di_penulis_md():
    """Tripwire tekstual, dan ia memang lemah — dicatat sebagai lemah."""
    sumber = inspect.getsource(run_h013)
    # Kalimat yang dipatok itu tidak boleh hidup di sumber mana pun lagi.
    assert "Sumbangan geometri yang lebih besar daripada sumbangan sinyal" not in sumber
    # Dan penulis md wajib memanggil fungsi yang dapat diuji.
    assert "md += prosa_kontribusi(ringkas)" in sumber
