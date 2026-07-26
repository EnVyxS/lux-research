"""Pengujian ambang ekor datar per interval dan nama keluaran per interval.

Dua cacat yang dijaga di sini, keduanya ditemukan dengan membaca kode sebelum
menjalankannya (ADR-018).

Pertama, ambang `MIN_PANJANG = 24` bermakna satu hari pada bar 1h, tetapi empat
hari pada bar 4h. Ekor palsu sepanjang satu sampai tiga hari akan lolos tanpa
terdeteksi, dan ekor yang tidak terdeteksi adalah tepat cara gerbang survivorship
kehilangan dayanya menurut ADR-003.

Kedua, keempat keluaran modul ini dahulu bernama sama untuk interval apa pun,
sementara `backtest.yml` membaca `universe_layak_v2.json` dan `akhir_sejati.json`.
Run 4h akan menimpa masukan backtest H-012 tanpa satu pun pesan galat.

Seluruh pengujian berjalan tanpa parquet dan tanpa jaringan.
"""

from __future__ import annotations

import pandas as pd
import pytest

from lux.potong_ekor import (
    BERKAS_DASAR,
    INTERVAL_JAM,
    JAM_SEHARI,
    ekor_datar,
    evaluasi,
    min_panjang_untuk,
    nama_keluaran,
    potong,
)

MS_4H = 4 * 3_600_000


def bingkai_4h(harga_ekor: list[float], n_bergerak: int = 14) -> pd.DataFrame:
    """Bingkai kisi 4h: sejumlah bar bergerak, lalu ekor datar berharga tertentu.

    Bar bergerak dibuat tidak datar secara eksplisit (high di atas close), supaya
    yang terdeteksi sebagai blok datar hanya ekornya.
    """
    baris = []
    for i in range(n_bergerak):
        c = 100.0 + i
        baris.append(
            {
                "symbol": "UJIUSDT",
                "open_time": i * MS_4H,
                "open": c,
                "high": c + 1.0,
                "low": c - 1.0,
                "close": c,
                "volume": 10.0,
                "count": 5.0,
            }
        )
    for j, p in enumerate(harga_ekor):
        baris.append(
            {
                "symbol": "UJIUSDT",
                "open_time": (n_bergerak + j) * MS_4H,
                "open": p,
                "high": p,
                "low": p,
                "close": p,
                "volume": 0.0,
                "count": 0.0,
            }
        )
    return pd.DataFrame(baris)


def test_min_panjang_1h_adalah_satu_hari() -> None:
    assert min_panjang_untuk("1h") == 24


def test_min_panjang_4h_adalah_satu_hari_juga() -> None:
    """Inti ADR-018: angkanya berubah supaya maknanya tidak berubah."""
    assert min_panjang_untuk("4h") == 6


def test_setiap_interval_berambang_tepat_satu_hari() -> None:
    """Tripwire aritmetika. Bila satu angka digeser, kesetaraan ini pecah."""
    for interval, jam in INTERVAL_JAM.items():
        assert min_panjang_untuk(interval) * jam == JAM_SEHARI


def test_interval_tak_dikenal_gagal_keras() -> None:
    """Tidak boleh ada jalan mundur senyap ke ambang 1h."""
    with pytest.raises(SystemExit) as galat:
        min_panjang_untuk("15m")
    assert "15m" in str(galat.value)


def test_keluaran_1h_menulis_nama_lama_agar_backtest_tidak_patah() -> None:
    assert nama_keluaran("akhir_sejati.json", "1h") == [
        "akhir_sejati_1h.json",
        "akhir_sejati.json",
    ]


def test_keluaran_4h_tidak_boleh_menyentuh_nama_lama() -> None:
    """Inti perbaikan kedua: run 4h tak dapat menimpa masukan backtest 1h."""
    for dasar in BERKAS_DASAR:
        nama = nama_keluaran(dasar, "4h")
        assert nama == [dasar.replace(".", "_4h.", 1)]
        assert dasar not in nama


def test_nama_kanonik_selalu_pertama_dan_menyebut_interval() -> None:
    for dasar in BERKAS_DASAR:
        for interval in ("1h", "4h"):
            assert nama_keluaran(dasar, interval)[0].count(interval) == 1
            assert nama_keluaran(dasar, interval)[0].startswith(dasar.split(".")[0])


def test_dua_berkas_yang_dibaca_backtest_ada_di_daftar_dasar() -> None:
    """Tripwire: bila salah satu dihapus dari daftar, nama lama berhenti ditulis."""
    assert "universe_layak_v2.json" in BERKAS_DASAR
    assert "akhir_sejati.json" in BERKAS_DASAR


def test_ekor_sehari_pada_4h_terdeteksi_ambang_6_dan_lolos_ambang_24() -> None:
    """Pengujian yang membuktikan cacatnya nyata, bukan teoretis.

    Ekor enam bar 4h adalah ekor satu hari penuh. Dengan ambang 4h yang benar ia
    terdeteksi; dengan ambang 1h yang diwarisi ia tidak terlihat sama sekali.
    """
    df = bingkai_4h([50.0] * 6)
    assert ekor_datar(df, 6) == 6
    assert ekor_datar(df, 24) == 0
    assert len(potong(df, 6)) == 14
    assert len(potong(df, 24)) == 20


def test_ekor_datar_berharga_lebih_dari_satu_bukan_padding() -> None:
    """Pasar sekarat yang masih melangkah tidak dipangkas; ia ditolak lewat jalur lain."""
    df = bingkai_4h([50.0] * 3 + [51.0] * 3)
    assert ekor_datar(df, 6) == 0
    e = evaluasi("UJIUSDT", df, min_panjang=6, min_bar=2190)
    assert e["dipangkas"] == 0
    assert not e["layak"]
    assert "blok datar" in e["alasan"]


def test_lantai_riwayat_dinilai_setelah_ekor_dipangkas() -> None:
    df = bingkai_4h([50.0] * 6)
    e = evaluasi("UJIUSDT", df, min_panjang=6, min_bar=2190)
    assert e["dipangkas"] == 6
    assert e["bar_sisa"] == 14
    assert not e["layak"]
    assert "riwayat tersisa 14 bar, di bawah 2190" == e["alasan"]
