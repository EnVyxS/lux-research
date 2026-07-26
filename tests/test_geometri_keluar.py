"""Pengujian diagnostik geometri keluar (ADR-015 Bagian A).

Seluruh angka di sini buatan. Tidak satu pun diambil dari laporan H-012, sebab
pengujian yang memakai angka nyata akan berubah hasilnya ketika laporan berubah,
dan pengujian yang bisa berubah bersama data bukan pengujian.
"""

from __future__ import annotations

import json

import pytest

from lux.analisis import geometri_keluar as gk


def baris_uji(
    symbol: str = "AAAUSDT",
    R: float = -1.0,
    alasan: str = "stop",
    transaksi: float = 0.03,
    funding: float = 0.01,
    stop_frac: float = 0.035,
    jam: float = 5.0,
) -> dict:
    """Satu baris terburuk buatan, bentuknya persis keluaran ``rincian_R``."""
    return {
        "symbol": symbol,
        "R": R,
        "kotor_R": R + transaksi + funding,
        "transaksi_R": transaksi,
        "funding_R": funding,
        "stop_frac": stop_frac,
        "jam": jam,
        "alasan": alasan,
    }


def test_R_terlampaui_nol_untuk_kerugian_dalam_1R():
    assert gk.R_terlampaui(-0.8) == 0.0
    assert gk.R_terlampaui(-1.0) == 0.0


def test_R_terlampaui_positif_di_luar_1R():
    assert gk.R_terlampaui(-21.3131) == pytest.approx(20.3131)


def test_R_terlampaui_nol_untuk_laba():
    assert gk.R_terlampaui(2.5) == 0.0


def test_celah_R_nol_bila_biaya_menjelaskan():
    assert gk.celah_R(-1.05, 0.03, 0.02) == pytest.approx(0.0)


def test_celah_R_positif_bila_biaya_tidak_menjelaskan():
    celah = gk.celah_R(-21.3131, 0.0359, 0.4825)
    assert celah > 19.0


def test_celah_R_negatif_bila_biaya_melebihi_pelampauan():
    # Bukti yang melawan dugaan ADR-015 harus terlihat, bukan dipotong di nol.
    assert gk.celah_R(-1.02, 0.30, 0.20) < 0.0


def test_dari_terburuk_menolak_kunci_hilang():
    rusak = baris_uji()
    del rusak["alasan"]
    with pytest.raises(KeyError) as e:
        gk.dari_terburuk([rusak])
    assert "alasan" in str(e.value)


def test_dari_terburuk_memetakan_medan_apa_adanya():
    hasil = gk.dari_terburuk(
        [baris_uji(symbol="BBBUSDT", R=-2.0, stop_frac=0.012, jam=48.0)]
    )
    assert len(hasil) == 1
    b = hasil[0]
    assert b["symbol"] == "BBBUSDT"
    assert b["stop_frac"] == pytest.approx(0.012)
    assert b["jam"] == pytest.approx(48.0)
    assert b["R_terlampaui"] == pytest.approx(1.0)


def test_ringkas_menghitung_porsi_bukan_stop():
    baris = gk.dari_terburuk(
        [
            baris_uji(R=-1.2, alasan="stop"),
            baris_uji(R=-1.1, alasan="stop"),
            baris_uji(R=-1.3, alasan="umur"),
            baris_uji(R=-1.4, alasan="carry"),
        ]
    )
    r = gk.ringkas(baris)
    assert r["n"] == 4
    assert r["n_stop"] == 2
    assert r["porsi_bukan_stop"] == pytest.approx(0.5)


def test_ringkas_mengurutkan_dan_menandai_terburuk():
    baris = gk.dari_terburuk(
        [baris_uji(symbol="RINGAN", R=-1.1), baris_uji(symbol="BERAT", R=-9.0)]
    )
    r = gk.ringkas(baris)
    assert r["terburuk"]["symbol"] == "BERAT"
    assert [b["symbol"] for b in r["baris"]] == ["BERAT", "RINGAN"]


def test_ringkas_menemukan_pelanggar_dan_ekor_menutup_ambang():
    baris = gk.dari_terburuk(
        [
            baris_uji(symbol="PELANGGAR", R=-9.0, alasan="umur"),
            baris_uji(symbol="AMAN", R=-1.3865),
        ]
    )
    r = gk.ringkas(baris)
    assert [b["symbol"] for b in r["pelanggar"]] == ["PELANGGAR"]
    assert r["pelanggar_stop"] == []
    assert r["ekor_menutup_ambang"] is True


def test_ringkas_ekor_tidak_menutup_ambang_bila_semua_pelanggar():
    baris = gk.dari_terburuk(
        [baris_uji(R=-9.0), baris_uji(R=-8.0)]
    )
    assert gk.ringkas(baris)["ekor_menutup_ambang"] is False


def test_ringkas_kosong_tidak_dapat_dinilai():
    r = gk.ringkas([])
    assert r["dapat_dinilai"] is False
    assert r["terburuk"] is None
    assert r["porsi_bukan_stop"] is None


def test_ambang_tidak_bergerak():
    # Diagnostik yang ambangnya bisa bergeser adalah pintu belakang bagi
    # hipotesis yang sudah divonis.
    assert gk.AMBANG_INVARIAN_R == -1.5
    assert gk.RENTANG_RAMALAN_4 == (0.0, 0.10)


def test_adili_ramalan_1_benar_bila_bukan_stop():
    baris = gk.dari_terburuk([baris_uji(R=-9.0, alasan="umur")])
    h = gk.adili(gk.ringkas(baris))
    assert h[0]["ramalan"] == 1
    assert h[0]["hasil"] == "BENAR"


def test_adili_ramalan_1_gugur_bila_stop():
    baris = gk.dari_terburuk([baris_uji(R=-9.0, alasan="stop")])
    h = gk.adili(gk.ringkas(baris))
    assert "GUGUR" in h[0]["hasil"]


def test_adili_ramalan_2_salah_bila_ada_stop_di_bawah_ambang():
    baris = gk.dari_terburuk(
        [
            baris_uji(symbol="XXXUSDT", R=-4.0, alasan="stop"),
            baris_uji(R=-1.2, alasan="umur"),
        ]
    )
    h = gk.adili(gk.ringkas(baris))
    assert h[1]["ramalan"] == 2
    assert h[1]["hasil"] == "SALAH"
    assert "XXXUSDT" in h[1]["bukti"]


def test_adili_ramalan_2_tidak_dapat_dinilai_bila_ekor_tidak_menutup():
    baris = gk.dari_terburuk(
        [baris_uji(R=-9.0, alasan="umur"), baris_uji(R=-8.0, alasan="umur")]
    )
    h = gk.adili(gk.ringkas(baris))
    assert h[1]["hasil"] == "TIDAK DAPAT DINILAI"


def test_adili_ramalan_3_dari_porsi():
    baris = gk.dari_terburuk(
        [baris_uji(R=-1.2, alasan="stop"), baris_uji(R=-1.1, alasan="stop")]
    )
    h = gk.adili(gk.ringkas(baris))
    assert h[2]["ramalan"] == 3
    assert h[2]["hasil"] == "SALAH"


def test_adili_ramalan_4_umur_dalam_rentang():
    baris = gk.dari_terburuk([baris_uji(R=-1.05, alasan="umur")])
    h = gk.adili(gk.ringkas(baris))
    assert h[3]["ramalan"] == 4
    assert h[3]["hasil"] == "BENAR"


def test_muat_menolak_json_tanpa_diagnosa(tmp_path):
    p = tmp_path / "laporan.json"
    p.write_text(json.dumps({"gabungan": {}}), encoding="utf-8")
    with pytest.raises(KeyError):
        gk.muat(p)


def test_main_menulis_laporan_dengan_tabel(tmp_path):
    p = tmp_path / "laporan.json"
    p.write_text(
        json.dumps(
            {
                "diagnosa_biaya": {
                    "terburuk": [
                        baris_uji(symbol="ZZZUSDT", R=-9.0, alasan="umur"),
                        baris_uji(symbol="YYYUSDT", R=-1.2, alasan="stop"),
                    ]
                }
            }
        ),
        encoding="utf-8",
    )
    keluar = tmp_path / "sub" / "geometri.md"
    assert gk.main(["--laporan", str(p), "--out", str(keluar)]) == 0
    teks = keluar.read_text(encoding="utf-8")
    assert "ZZZUSDT" in teks
    assert "umur" in teks
    assert "Adjudikasi ramalan Bagian A" in teks
}