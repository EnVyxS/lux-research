"""Pengujian parser kline.

Seluruh pengujian di sini memakai berkas ZIP sintetis, tanpa jaringan sama
sekali, sehingga berjalan dalam hitungan milidetik.

Keberadaan berkas ini adalah konsekuensi langsung dari satu bug: parser
membuang tepat satu bar dari setiap berkas berheader, karena ``header=0`` dan
``skiprows=1`` dipakai bersamaan. Pada berkas bulanan kerugiannya 1 dari 720 bar
dan tidak terlihat selama dua putaran penuh. Yang akhirnya menyingkapnya bukan
pemeriksaan kode, melainkan sebuah invarian: rasio jumlah baris 1h terhadap 4h
wajib mendekati 4, dan pada backfill harian rasionya 4,60 alias tepat 23/5.

Pelajarannya dicatat di sini supaya tidak hilang: invarian aritmetika sederhana
menangkap cacat yang tidak tertangkap oleh membaca ulang kode.
"""

from __future__ import annotations

import io
import zipfile
from pathlib import Path

import pytest

from lux.ingest import KOLOM, baca_zip

HEADER = ",".join(KOLOM)


def baris_csv(open_time: int) -> str:
    return (
        f"{open_time},100.0,101.0,99.0,100.5,1000.0,{open_time + 3599999},"
        "100500.0,50,500.0,50250.0,0"
    )


def buat_zip(tmp_path: Path, isi: str, nama: str = "data.csv") -> Path:
    path = tmp_path / "arsip.zip"
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(nama, isi)
    return path


def test_berkas_tanpa_header_terbaca_utuh(tmp_path: Path):
    isi = "\n".join(baris_csv(1600000000000 + i * 3600000) for i in range(24))
    df = baca_zip(buat_zip(tmp_path, isi))
    assert len(df) == 24


def test_berkas_berheader_terbaca_utuh(tmp_path: Path):
    """Inilah pengujian yang seharusnya ada sejak awal.

    Dua puluh empat baris data harus tetap dua puluh empat, bukan dua puluh
    tiga. Bug lama membuat baris pertama diperlakukan sebagai nama kolom.
    """
    data = "\n".join(baris_csv(1600000000000 + i * 3600000) for i in range(24))
    df = baca_zip(buat_zip(tmp_path, HEADER + "\n" + data))
    assert len(df) == 24


def test_bar_pertama_tidak_hilang_pada_berkas_berheader(tmp_path: Path):
    awal = 1600000000000
    data = "\n".join(baris_csv(awal + i * 3600000) for i in range(6))
    df = baca_zip(buat_zip(tmp_path, HEADER + "\n" + data))
    assert int(df["open_time"].min()) == awal


def test_jumlah_baris_sama_dengan_dan_tanpa_header(tmp_path: Path):
    """Invarian utama: keberadaan header tidak boleh mengubah jumlah bar."""
    data = "\n".join(baris_csv(1600000000000 + i * 3600000) for i in range(10))
    tanpa = baca_zip(buat_zip(tmp_path / "a", data))
    dengan = baca_zip(buat_zip(tmp_path / "b", HEADER + "\n" + data))
    assert len(tanpa) == len(dengan) == 10


def test_rasio_1h_terhadap_4h_mendekati_empat(tmp_path: Path):
    """Invarian yang menyingkap bug asli, dijaga sebagai pengujian.

    Satu hari berisi 24 bar 1h dan 6 bar 4h. Rasio berapa pun selain 4 berarti
    ada bar yang hilang di salah satu sisi.
    """
    satu_jam = "\n".join(baris_csv(1600000000000 + i * 3600000) for i in range(24))
    empat_jam = "\n".join(baris_csv(1600000000000 + i * 14400000) for i in range(6))
    df1 = baca_zip(buat_zip(tmp_path / "h1", HEADER + "\n" + satu_jam))
    df4 = baca_zip(buat_zip(tmp_path / "h4", HEADER + "\n" + empat_jam))
    assert len(df1) / len(df4) == pytest.approx(4.0)


def test_stempel_mikrodetik_dinormalisasi(tmp_path: Path):
    mikro = 1600000000000000  # mikrodetik
    isi = baris_csv(mikro)
    df = baca_zip(buat_zip(tmp_path, isi))
    assert int(df["open_time"].iloc[0]) == 1600000000000


def test_berkas_kosong_menghasilkan_dataframe_kosong(tmp_path: Path):
    df = baca_zip(buat_zip(tmp_path, ""))
    assert df.empty


def test_zip_tanpa_csv_ditolak(tmp_path: Path):
    path = tmp_path / "arsip.zip"
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("catatan.txt", "bukan csv")
    with pytest.raises(RuntimeError):
        baca_zip(path)


def test_baris_sampah_dibuang_bukan_menggagalkan_berkas(tmp_path: Path):
    data = "\n".join(
        [
            baris_csv(1600000000000),
            "bukan,angka,sama,sekali,x,y,z,a,b,c,d,e",
            baris_csv(1600000003600000 // 1),
        ]
    )
    df = baca_zip(buat_zip(tmp_path, data))
    assert len(df) == 2


def test_kolom_bertipe_numerik(tmp_path: Path):
    df = baca_zip(buat_zip(tmp_path, baris_csv(1600000000000)))
    assert df["open_time"].dtype == "int64"
    for kolom in ("open", "high", "low", "close", "volume"):
        assert df[kolom].dtype == "float64"


def test_urutan_kolom_sesuai_spesifikasi(tmp_path: Path):
    df = baca_zip(buat_zip(tmp_path, baris_csv(1600000000000)))
    assert list(df.columns) == KOLOM


def test_encoding_utf8_bom_tidak_merusak_deteksi_header(tmp_path: Path):
    data = "\n".join(baris_csv(1600000000000 + i * 3600000) for i in range(3))
    isi = "\ufeff" + HEADER + "\n" + data
    df = baca_zip(buat_zip(tmp_path, isi))
    # BOM tidak boleh menyebabkan baris header ikut terbaca sebagai data.
    assert len(df) == 3
