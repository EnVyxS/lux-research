"""Pengujian parser funding rate, seluruhnya tanpa jaringan.

Setiap cacat yang pernah ditemukan pada parser klines diuji ulang di sini,
karena cacat yang sama cenderung lahir kembali di modul berikutnya.
"""

from __future__ import annotations

import zipfile

import pytest

from lux.funding import AMBANG_EKSTREM, KOLOM, baca_zip, funding_url, periksa

HEADER = ",".join(KOLOM)
JAM8 = 8 * 3_600_000
AWAL = 1_600_000_000_000 - (1_600_000_000_000 % JAM8)


def baris(i: int, rate: float = 0.0001) -> str:
    return f"{AWAL + i * JAM8},8,{rate}"


def buat_zip(path, isi: bytes, nama: str = "data.csv"):
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(nama, isi)
    return path


def test_url_memakai_percent_encoding(tmp_path):
    url = funding_url("\u9f99\u867eUSDT", "2024-01")
    assert "%" in url
    assert "\u9f99" not in url
    assert url.endswith("-fundingRate-2024-01.zip")


def test_jumlah_baris_sama_dengan_dan_tanpa_header(tmp_path):
    """Cacat paling mahal sesi ini: satu baris hilang per berkas berheader."""
    isi = "\n".join(baris(i) for i in range(5))
    a = buat_zip(tmp_path / "a" / "arsip.zip", (HEADER + "\n" + isi).encode())
    b = buat_zip(tmp_path / "b" / "arsip.zip", isi.encode())
    assert len(baca_zip(a)) == 5
    assert len(baca_zip(b)) == 5


def test_bom_tidak_merusak_deteksi_header(tmp_path):
    isi = HEADER + "\n" + "\n".join(baris(i) for i in range(3))
    p = buat_zip(tmp_path / "c" / "arsip.zip", ("\ufeff" + isi).encode("utf-8"))
    assert len(baca_zip(p)) == 3


def test_baris_sampah_dibuang_bukan_menggagalkan_berkas(tmp_path):
    isi = HEADER + "\n" + baris(0) + "\nangka,delapan,bukan_angka\n" + baris(1)
    p = buat_zip(tmp_path / "d" / "arsip.zip", isi.encode())
    assert len(baca_zip(p)) == 2


def test_lebar_dua_kolom_tetap_terbaca(tmp_path):
    """Arsip lama sempat tidak memuat kolom interval jam."""
    isi = "\n".join(f"{AWAL + i * JAM8},0.0001" for i in range(4))
    p = buat_zip(tmp_path / "e" / "arsip.zip", isi.encode())
    df = baca_zip(p)
    assert len(df) == 4
    assert list(df.columns) == KOLOM
    assert df["funding_interval_hours"].isna().all()


def test_stempel_mikrodetik_dinormalisasi(tmp_path):
    mikro = (AWAL) * 1000
    isi = HEADER + "\n" + f"{mikro},8,0.0001"
    p = buat_zip(tmp_path / "f" / "arsip.zip", isi.encode())
    df = baca_zip(p)
    assert int(df.loc[0, "calc_time"]) == AWAL


def test_funding_negatif_dipertahankan(tmp_path):
    """Funding negatif berarti short yang membayar; membuangnya memihak arah."""
    isi = HEADER + "\n" + baris(0, -0.0005) + "\n" + baris(1, 0.0003)
    p = buat_zip(tmp_path / "g" / "arsip.zip", isi.encode())
    df = baca_zip(p)
    stat = periksa(df)
    assert stat["negatif"] == 1
    assert stat["positif"] == 1
    assert stat["rate_min"] == pytest.approx(-0.0005)


def test_nilai_ekstrem_dicatat_bukan_dibuang(tmp_path):
    isi = HEADER + "\n" + baris(0, 0.05) + "\n" + baris(1, 0.0001)
    p = buat_zip(tmp_path / "h" / "arsip.zip", isi.encode())
    df = baca_zip(p)
    stat = periksa(df)
    assert stat["baris"] == 2  # tidak dibuang
    assert stat["ekstrem"] == 1
    assert stat["rate_maks"] > AMBANG_EKSTREM


def test_kisi_delapan_jam_tanpa_celah(tmp_path):
    isi = HEADER + "\n" + "\n".join(baris(i) for i in range(10))
    p = buat_zip(tmp_path / "i" / "arsip.zip", isi.encode())
    stat = periksa(baca_zip(p))
    assert stat["celah"] == 0
    assert stat["interval_jam"] == [8]


def test_celah_terdeteksi(tmp_path):
    isi = HEADER + "\n" + baris(0) + "\n" + baris(5)
    p = buat_zip(tmp_path / "j" / "arsip.zip", isi.encode())
    assert periksa(baca_zip(p))["celah"] == 1


def test_kisi_empat_jam_tidak_dianggap_celah(tmp_path):
    """Sebagian pasangan memakai funding 4 jam; langkah diambil dari data."""
    jam4 = 4 * 3_600_000
    isi = HEADER + "\n" + "\n".join(
        f"{AWAL + i * jam4},4,0.0001" for i in range(6)
    )
    p = buat_zip(tmp_path / "k" / "arsip.zip", isi.encode())
    stat = periksa(baca_zip(p))
    assert stat["interval_jam"] == [4]
    assert stat["celah"] == 0


def test_berkas_hanya_header_tidak_melempar(tmp_path):
    """Bulan tanpa funding memang ada, misalnya kontrak yang baru terdaftar.

    Sebelum perbaikan, keadaan sah ini melempar ``EmptyDataError`` dan ditangkap
    sebagai kegagalan bulan, sehingga satu berkas kosong dapat menandai simbol
    yang datanya sebenarnya lengkap.
    """
    p = buat_zip(tmp_path / "l" / "arsip.zip", (HEADER + "\n").encode())
    df = baca_zip(p)
    assert df.empty
    assert list(df.columns) == KOLOM
    assert periksa(df)["baris"] == 0


def test_berkas_benar_benar_kosong_tidak_melempar(tmp_path):
    p = buat_zip(tmp_path / "m" / "arsip.zip", b"")
    df = baca_zip(p)
    assert df.empty
    assert periksa(df)["baris"] == 0


def test_berkas_berisi_hanya_baris_sampah_tidak_melempar(tmp_path):
    isi = HEADER + "\n" + "sampah,sampah,sampah\n"
    p = buat_zip(tmp_path / "n" / "arsip.zip", isi.encode())
    df = baca_zip(p)
    assert df.empty
    assert list(df.columns) == KOLOM
