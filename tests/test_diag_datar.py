"""Uji pembongkaran blok bar datar.

Yang diuji di sini terutama batas-batasnya: deret yang menempel di indeks nol
dan di indeks terakhir adalah dua tempat paling sering terlewat pada pendeteksi
deret berbasis selisih, dan keduanya justru kasus yang paling ingin ditemukan
(padding awal riwayat dan feed yang berhenti di ujung).

Uji ``test_blok_yang_menempel_di_akhir_riwayat_tertangkap`` menjatuhkan versi
pertama ``letak()`` yang menilai posisi hanya dari titik mulai blok. Uji itu
dipertahankan apa adanya.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from lux.diag_datar import _deret, blok_datar, letak, letak_blok, ringkas_simbol

JAM = 3_600_000
AWAL = 1_600_000_000_000


def datar(harga: float):
    return (harga, harga, harga, harga)


def gerak(harga: float):
    return (harga, harga + 1.0, harga - 1.0, harga)


def buat(baris, volume=None, count=None) -> pd.DataFrame:
    n = len(baris)
    return pd.DataFrame(
        {
            "open_time": [AWAL + i * JAM for i in range(n)],
            "open": [b[0] for b in baris],
            "high": [b[1] for b in baris],
            "low": [b[2] for b in baris],
            "close": [b[3] for b in baris],
            "volume": volume if volume is not None else [10.0] * n,
            "count": count if count is not None else [5] * n,
        }
    )


def test_deret_menangkap_yang_menempel_di_kedua_ujung():
    mask = np.array([True, True, False, True, False, True, True])
    assert _deret(mask) == [(0, 1), (3, 3), (5, 6)]


def test_deret_atas_mask_kosong_tidak_melempar():
    assert _deret(np.array([], dtype=bool)) == []


def test_deret_atas_mask_seluruhnya_benar():
    assert _deret(np.array([True, True, True])) == [(0, 2)]


def test_bingkai_kosong_tidak_melempar():
    assert blok_datar(buat([])) == []


def test_tanpa_bar_datar_tidak_melaporkan_blok():
    df = buat([gerak(100.0), gerak(101.0), gerak(102.0)])
    assert blok_datar(df, min_panjang=2) == []


def test_satu_blok_dilaporkan_dengan_batas_yang_benar():
    df = buat([gerak(100.0), datar(50.0), datar(50.0), datar(50.0), gerak(100.0)])
    blok = blok_datar(df, min_panjang=2)
    assert len(blok) == 1
    assert blok[0]["indeks_mulai"] == 1
    assert blok[0]["indeks_akhir"] == 3
    assert blok[0]["panjang"] == 3
    assert blok[0]["mulai_ms"] == AWAL + JAM
    assert blok[0]["akhir_ms"] == AWAL + 3 * JAM


def test_blok_yang_menempel_di_awal_riwayat_tertangkap():
    df = buat([datar(50.0), datar(50.0), gerak(100.0), gerak(101.0)])
    blok = blok_datar(df, min_panjang=2)
    assert len(blok) == 1
    assert blok[0]["indeks_mulai"] == 0
    assert blok[0]["posisi_frac"] == 0.0
    assert letak_blok(blok[0]) == "awal"


def test_blok_yang_menempel_di_akhir_riwayat_tertangkap():
    df = buat([gerak(100.0), gerak(101.0), datar(50.0), datar(50.0)])
    blok = blok_datar(df, min_panjang=2)
    assert len(blok) == 1
    assert blok[0]["indeks_akhir"] == 3
    assert blok[0]["posisi_akhir_frac"] == 1.0
    assert letak_blok(blok[0]) == "akhir"


def test_blok_panjang_di_ujung_tidak_disebut_tengah():
    """Cacat versi pertama: semakin panjang bloknya, semakin jauh titik mulainya
    dari ujung, sehingga feed yang mati paling lama justru paling mudah lolos."""
    df = buat([gerak(100.0)] * 3 + [datar(50.0)] * 7)
    blok = blok_datar(df, min_panjang=2)[0]
    assert blok["posisi_frac"] == 0.3
    assert letak_blok(blok) == "akhir"


def test_blok_yang_menutupi_seluruh_riwayat_punya_namanya_sendiri():
    df = buat([datar(50.0)] * 5)
    blok = blok_datar(df, min_panjang=2)[0]
    assert letak_blok(blok) == "seluruh"


def test_min_panjang_menyaring_blok_pendek():
    df = buat([datar(50.0), gerak(100.0), datar(60.0), datar(60.0), datar(60.0)])
    assert len(blok_datar(df, min_panjang=2)) == 1
    assert len(blok_datar(df, min_panjang=1)) == 2
    assert blok_datar(df, min_panjang=4) == []


def test_blok_terpanjang_diurutkan_lebih_dulu():
    df = buat(
        [datar(50.0), datar(50.0), gerak(100.0), datar(60.0), datar(60.0), datar(60.0)]
    )
    blok = blok_datar(df, min_panjang=2)
    assert [b["panjang"] for b in blok] == [3, 2]


def test_dua_blok_terpisah_tidak_digabung():
    df = buat([datar(50.0), datar(50.0), gerak(100.0), datar(50.0), datar(50.0)])
    blok = blok_datar(df, min_panjang=2)
    assert len(blok) == 2
    assert sum(b["panjang"] for b in blok) == 4


def test_harga_unik_membedakan_feed_beku_dari_pasar_melompat():
    beku = buat([datar(50.0), datar(50.0), datar(50.0)])
    melompat = buat([datar(50.0), datar(51.0), datar(52.0)])
    assert blok_datar(beku, min_panjang=2)[0]["harga_unik"] == 1
    assert blok_datar(melompat, min_panjang=2)[0]["harga_unik"] == 3


def test_volume_dan_count_dijumlahkan_atas_blok():
    df = buat(
        [gerak(100.0), datar(50.0), datar(50.0)],
        volume=[1.0, 2.0, 3.0],
        count=[9, 4, 6],
    )
    blok = blok_datar(df, min_panjang=2)[0]
    assert blok["volume_total"] == 5.0
    assert blok["count_total"] == 10.0


def test_kolom_volume_yang_tidak_ada_tidak_melempar():
    df = buat([gerak(100.0), datar(50.0), datar(50.0)]).drop(columns=["volume"])
    blok = blok_datar(df, min_panjang=2)[0]
    assert blok["panjang"] == 2


def test_letak_memberi_nama_yang_benar():
    assert letak(0.0, 0.5) == "awal"
    assert letak(0.4, 0.6) == "tengah"
    assert letak(0.5, 1.0) == "akhir"
    assert letak(0.0, 1.0) == "seluruh"


def test_simbol_bersih_dikembalikan_sebagai_none():
    df = buat([gerak(100.0), gerak(101.0), gerak(102.0)])
    assert ringkas_simbol("X", df, min_panjang=2) is None


def test_porsi_datar_di_blok_terpanjang_menandai_gumpalan():
    menggumpal = buat([datar(50.0)] * 8 + [gerak(100.0)] * 8)
    tersebar = buat([datar(50.0), gerak(100.0)] * 8)
    r1 = ringkas_simbol("A", menggumpal, min_panjang=2)
    r2 = ringkas_simbol("B", tersebar, min_panjang=2)
    assert r1 is not None
    assert r1["porsi_datar_di_blok_terpanjang"] == 1.0
    assert r1["letak_terpanjang"] == "awal"
    assert r2 is None


def test_bar_datar_dihitung_atas_seluruh_bingkai_bukan_hanya_blok_besar():
    df = buat([datar(50.0)] * 4 + [gerak(100.0)] + [datar(60.0)])
    r = ringkas_simbol("A", df, min_panjang=4)
    assert r is not None
    assert r["bar_datar"] == 5
    assert r["jumlah_blok"] == 1
    assert r["porsi_datar_di_blok_terpanjang"] == 4 / 5
