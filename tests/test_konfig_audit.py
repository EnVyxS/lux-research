"""Pagar untuk ``lux.backtest.konfig_audit`` (ADR-036, aturan 57).

Pengujian nomor tujuh dan lima belas adalah **pengujian regresi cacat kelas
kedelapan belas**: keduanya membangun ulang pasangan Konfig SH (H-013) dan SH′
(H-014) yang sungguhan dan menuntut alat ini melihat apa yang tidak dilihat
siapa pun pada 2026-07-26.
"""

from dataclasses import fields, replace

import pytest

from lux.backtest.engine import Konfig
from lux.backtest.konfig_audit import (
    konfig_penuh,
    laporan_kesebandingan,
    pengaman_mati,
    selisih_konfig,
)

# Nilai sungguhan dari run_h009.AMBANG_CARRY_KERAS. Ditulis di berkas uji, BUKAN
# di modul yang diuji: pagar boleh menyebut angka, modul umum tidak boleh.
CARRY_KERAS = 0.25


def konfig_sh() -> Konfig:
    """Sel SH H-013: lewat buat_konfig, pengaman carry keras MENYALA."""
    return Konfig(
        imbalan_R=2.0,
        maks_umur_bar=48,
        pakai_target=False,
        maks_carry_realisasi_R=CARRY_KERAS,
    )


def konfig_shp() -> Konfig:
    """Sel SH′ H-014: buat_konfig=None, pengaman carry keras MATI."""
    return Konfig(imbalan_R=2.0, maks_umur_bar=48, pakai_target=False)


def test_konfig_penuh_memuat_seluruh_medan():
    isi = konfig_penuh(Konfig())
    assert set(isi) == {f.name for f in fields(Konfig)}


def test_konfig_penuh_memuat_medan_yang_tidak_pernah_disetel():
    isi = konfig_penuh(Konfig())
    assert isi["maks_carry_realisasi_R"] == 0.0


def test_konfig_penuh_terurut_menurut_nama():
    isi = konfig_penuh(Konfig())
    assert list(isi) == sorted(isi)


def test_konfig_penuh_menolak_kelas_bukan_instans():
    with pytest.raises(TypeError):
        konfig_penuh(Konfig)


def test_konfig_penuh_menolak_dict():
    with pytest.raises(TypeError):
        konfig_penuh({"maks_carry_realisasi_R": 0.25})


def test_selisih_kosong_untuk_konfig_identik():
    assert selisih_konfig(Konfig(), Konfig()) == {}


def test_selisih_menemukan_pengaman_yang_diam():
    selisih = selisih_konfig(konfig_sh(), konfig_shp())
    assert list(selisih) == ["maks_carry_realisasi_R"]
    assert selisih["maks_carry_realisasi_R"] == {"kiri": CARRY_KERAS, "kanan": 0.0}


def test_selisih_menemukan_lebih_dari_satu_medan():
    kiri = Konfig(maks_umur_bar=42)
    kanan = Konfig(maks_umur_bar=48, imbalan_R=3.0)
    assert set(selisih_konfig(kiri, kanan)) == {"maks_umur_bar", "imbalan_R"}


def test_selisih_menolak_kelas_berbeda():
    with pytest.raises(TypeError):
        selisih_konfig(Konfig(), "Konfig")


def test_pengaman_mati_menemukan_pengaman_yang_mati():
    assert pengaman_mati(konfig_shp(), {"maks_carry_realisasi_R": CARRY_KERAS}) == [
        "maks_carry_realisasi_R"
    ]


def test_pengaman_mati_kosong_ketika_pengaman_hidup():
    assert pengaman_mati(konfig_sh(), {"maks_carry_realisasi_R": CARRY_KERAS}) == []


def test_pengaman_mati_menolak_daftar_kosong():
    with pytest.raises(ValueError):
        pengaman_mati(konfig_sh(), {})


def test_pengaman_mati_menolak_medan_tak_dikenal():
    with pytest.raises(ValueError):
        pengaman_mati(konfig_sh(), {"maks_carry_realisasi": CARRY_KERAS})


def test_pengaman_mati_menolak_ambang_nol():
    with pytest.raises(ValueError):
        pengaman_mati(konfig_sh(), {"maks_carry_realisasi_R": 0.0})


def test_pengaman_mati_menolak_ambang_bool():
    with pytest.raises(ValueError):
        pengaman_mati(konfig_sh(), {"stop_hormati_celah": True})


def test_laporan_menghalangi_run_h014_yang_sungguhan():
    lap = laporan_kesebandingan(
        "SHp",
        konfig_shp(),
        "SH (H-013)",
        konfig_sh(),
        {"maks_carry_realisasi_R": CARRY_KERAS},
    )
    assert lap["menghalangi"] is True
    assert lap["pengaman_mati"] == ["maks_carry_realisasi_R"]
    assert list(lap["selisih_terhadap_pendahulu"]) == ["maks_carry_realisasi_R"]
    assert set(lap["konfig"]) == {f.name for f in fields(Konfig)}
    assert any("PENGAMAN MATI" in baris for baris in lap["prosa"])


def test_laporan_selisih_yang_disengaja_tidak_menghalangi():
    ini = replace(konfig_sh(), maks_umur_bar=48)
    pendahulu = replace(konfig_sh(), maks_umur_bar=42)
    lap = laporan_kesebandingan(
        "SSp", ini, "SS (H-013)", pendahulu, {"maks_carry_realisasi_R": CARRY_KERAS}
    )
    assert lap["menghalangi"] is False
    assert lap["pengaman_mati"] == []
    assert list(lap["selisih_terhadap_pendahulu"]) == ["maks_umur_bar"]
    assert any("selisih terhadap SS (H-013)" in baris for baris in lap["prosa"])
