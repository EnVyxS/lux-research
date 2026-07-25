"""Pengujian pengaman carry keras (ADR-008).

Yang paling penting di berkas ini bukan pengujian yang membuktikan pengaman
bekerja, melainkan pengujian yang membuktikan pengaman **tidak melakukan apa
pun** selama ambangnya nol. Tanpa itu, seluruh hasil H-001b sampai H-007 tidak
lagi dapat diulang, dan tidak akan ada yang menyadarinya.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from lux.analisis.titik_impas import ALASAN_TIDAK_SELESAI, laju_kena_target
from lux.backtest.engine import Konfig, carry_terealisasi_R, jalankan
from lux.funding_model import Jadwal

JAM = 3_600_000
AWAL = 1_700_000_000_000


def bingkai_datar(n_gerak: int = 30, n_datar: int = 40) -> pd.DataFrame:
    """Bar bergerak dulu supaya ATR terbentuk, lalu datar sempurna.

    Selama fase datar, harga tidak pernah menyentuh stop maupun target, jadi
    satu-satunya cara posisi tertutup adalah pengaman yang sedang diuji.
    """
    baris = []
    for i in range(n_gerak):
        naik = i % 2 == 0
        baris.append(
            {
                "open_time": AWAL + i * JAM,
                "open": 100.0,
                "high": 100.5 if naik else 100.2,
                "low": 99.5 if naik else 99.8,
                "close": 100.0,
            }
        )
    for i in range(n_gerak, n_gerak + n_datar):
        baris.append(
            {
                "open_time": AWAL + i * JAM,
                "open": 100.0,
                "high": 100.0,
                "low": 100.0,
                "close": 100.0,
            }
        )
    return pd.DataFrame(baris)


def sinyal_masuk_sekali(n: int, idx: int = 29) -> np.ndarray:
    s = np.zeros(n, dtype="int64")
    s[idx] = 1
    return s


def jadwal_mahal(rate: float = 0.003, tiap_jam: int = 8, n: int = 20) -> Jadwal:
    return Jadwal.dari_frame(
        pd.DataFrame(
            {
                "calc_time": [AWAL + (i + 1) * tiap_jam * JAM for i in range(n)],
                "last_funding_rate": [rate] * n,
            }
        )
    )


def test_bawaan_mati():
    assert Konfig().maks_carry_realisasi_R == 0.0


def test_negatif_ditolak():
    with pytest.raises(ValueError):
        Konfig(maks_carry_realisasi_R=-0.1)


def test_mati_berarti_tidak_ada_keluar_carry():
    df = bingkai_datar()
    hasil = jalankan(
        df,
        sinyal_masuk_sekali(len(df)),
        Konfig(),
        jadwal=jadwal_mahal(),
        symbol="UJI",
    )
    alasan = [p.alasan_keluar for p in hasil.perdagangan]
    assert "carry" not in alasan
    assert alasan == ["akhir_data"]


def test_pengaman_menyala_menutup_posisi():
    df = bingkai_datar()
    hasil = jalankan(
        df,
        sinyal_masuk_sekali(len(df)),
        Konfig(maks_carry_realisasi_R=0.25),
        jadwal=jadwal_mahal(),
        symbol="UJI",
    )
    assert [p.alasan_keluar for p in hasil.perdagangan] == ["carry"]


def test_keluar_di_pembukaan_bar_dengan_slippage_melawan():
    df = bingkai_datar()
    k = Konfig(maks_carry_realisasi_R=0.25)
    hasil = jalankan(
        df, sinyal_masuk_sekali(len(df)), k, jadwal=jadwal_mahal(), symbol="UJI"
    )
    p = hasil.perdagangan[0]
    # Long keluar: slippage memperburuk, jadi harga jual di bawah pembukaan.
    assert p.harga_keluar == pytest.approx(100.0 * (1.0 - k.slippage))


def test_short_yang_menerima_funding_tidak_pernah_terpicu():
    """Tanda salah di sini akan menutup justru posisi yang sedang dibayar."""
    df = bingkai_datar()
    s = np.zeros(len(df), dtype="int64")
    s[29] = -1
    hasil = jalankan(
        df,
        s,
        Konfig(maks_carry_realisasi_R=0.25),
        jadwal=jadwal_mahal(),
        symbol="UJI",
    )
    assert [p.alasan_keluar for p in hasil.perdagangan] == ["akhir_data"]
    # Short pada funding positif menerima uang: biaya funding bertanda negatif.
    assert hasil.perdagangan[0].biaya_funding < 0


def test_tanpa_jadwal_entri_ditolak():
    """Pengaman yang tidak dapat dinilai tidak boleh berarti posisi bebas."""
    df = bingkai_datar()
    hasil = jalankan(
        df,
        sinyal_masuk_sekali(len(df)),
        Konfig(maks_carry_realisasi_R=0.25),
        jadwal=None,
        symbol="UJI",
    )
    assert hasil.perdagangan == []


def test_umur_didahulukan_saat_keduanya_terpicu():
    df = bingkai_datar()
    hasil = jalankan(
        df,
        sinyal_masuk_sekali(len(df)),
        Konfig(maks_umur_bar=1, maks_carry_realisasi_R=0.25),
        jadwal=jadwal_mahal(),
        symbol="UJI",
    )
    assert hasil.perdagangan[0].alasan_keluar == "umur"


def test_ambang_lebih_tinggi_menahan_posisi_lebih_lama():
    df = bingkai_datar()
    cepat = jalankan(
        df,
        sinyal_masuk_sekali(len(df)),
        Konfig(maks_carry_realisasi_R=0.25),
        jadwal=jadwal_mahal(),
        symbol="UJI",
    ).perdagangan[0]
    lambat = jalankan(
        df,
        sinyal_masuk_sekali(len(df)),
        Konfig(maks_carry_realisasi_R=0.50),
        jadwal=jadwal_mahal(),
        symbol="UJI",
    ).perdagangan[0]
    assert lambat.keluar_ms > cepat.keluar_ms


def test_carry_terealisasi_R_positif_berarti_membayar():
    j = jadwal_mahal()
    nilai = carry_terealisasi_R(
        j,
        arah=1,
        masuk_ms=AWAL,
        sekarang_ms=AWAL + 9 * JAM,
        harga_masuk=100.0,
        jarak_stop=2.0,
    )
    # Satu penagihan 0,003 pada stop 2% dari harga: 0,003 / 0,02 = 0,15R.
    assert nilai == pytest.approx(0.15)


def test_carry_terealisasi_R_menolak_jarak_stop_nol():
    with pytest.raises(ValueError):
        carry_terealisasi_R(
            jadwal_mahal(),
            arah=1,
            masuk_ms=AWAL,
            sekarang_ms=AWAL + 9 * JAM,
            harga_masuk=100.0,
            jarak_stop=0.0,
        )


def test_carry_tidak_ikut_menghitung_laju_kena_target():
    """Alasan keluar baru tidak boleh diam-diam masuk penyebut titik impas."""
    assert "carry" in ALASAN_TIDAK_SELESAI
    tanpa = laju_kena_target({"target": 30, "stop": 70})
    dengan = laju_kena_target({"target": 30, "stop": 70, "carry": 500})
    assert tanpa == dengan == pytest.approx(0.30)
