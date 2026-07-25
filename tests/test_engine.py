"""Pengujian mesin backtest.

Yang diuji di sini bukan apakah mesinnya menghasilkan laba, melainkan apakah
ia menolak menghasilkan laba yang tidak semestinya. Setiap pengujian mengunci
satu pilihan pesimistis yang, bila terbalik, membuat hasil backtest lebih indah
daripada kenyataan.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from lux.backtest.engine import Konfig, Perdagangan, atr, jalankan
from lux.funding_model import Jadwal

JAM = 3_600_000
AWAL = 1_600_000_000_000


def bingkai(harga: list[float], rentang: float = 1.0) -> pd.DataFrame:
    """Bingkai OHLC sederhana: tiap bar dibuka dan ditutup di harga yang sama."""
    return pd.DataFrame(
        {
            "open_time": [AWAL + i * JAM for i in range(len(harga))],
            "open": harga,
            "high": [p + rentang for p in harga],
            "low": [p - rentang for p in harga],
            "close": harga,
        }
    )


def test_atr_mengabaikan_bar_yang_belum_cukup():
    df = bingkai([100.0] * 30)
    a = atr(df["high"].to_numpy(), df["low"].to_numpy(), df["close"].to_numpy(), 14)
    assert np.isnan(a[:14]).all()
    assert np.isfinite(a[14:]).all()


def test_atr_tidak_memakai_bar_masa_depan():
    """Memotong data di titik mana pun tidak boleh mengubah nilai sebelumnya."""
    df = bingkai([100.0 + i * 0.3 for i in range(60)])
    penuh = atr(df["high"].to_numpy(), df["low"].to_numpy(), df["close"].to_numpy())
    potong = atr(
        df["high"].to_numpy()[:40],
        df["low"].to_numpy()[:40],
        df["close"].to_numpy()[:40],
    )
    assert np.allclose(penuh[14:40], potong[14:40], equal_nan=True)


def test_atr_kurang_data_mengembalikan_nan_semua():
    df = bingkai([100.0] * 5)
    a = atr(df["high"].to_numpy(), df["low"].to_numpy(), df["close"].to_numpy(), 14)
    assert np.isnan(a).all()


def test_sinyal_dieksekusi_pada_bar_berikutnya():
    """Pencegahan lookahead yang paling penting di seluruh mesin."""
    harga = [100.0] * 20 + [100.0] * 20
    df = bingkai(harga)
    sinyal = np.zeros(len(df), dtype=int)
    sinyal[20] = 1
    hasil = jalankan(df, sinyal)
    assert hasil.jumlah_trade >= 0
    if hasil.perdagangan:
        assert hasil.perdagangan[0].masuk_ms == AWAL + 21 * JAM


def test_sinyal_pada_bar_terakhir_diabaikan():
    df = bingkai([100.0] * 30)
    sinyal = np.zeros(len(df), dtype=int)
    sinyal[-1] = 1
    assert jalankan(df, sinyal).jumlah_trade == 0


def test_sinyal_sebelum_atr_siap_tidak_membuka_posisi():
    """Memperdagangkan volatilitas yang belum diketahui adalah menebak."""
    df = bingkai([100.0] * 30)
    sinyal = np.zeros(len(df), dtype=int)
    sinyal[3] = 1
    assert jalankan(df, sinyal).jumlah_trade == 0


def test_stop_menang_saat_stop_dan_target_sama_sama_tersentuh():
    """Ketidaktahuan urutan di dalam bar tidak boleh berbuah laba."""
    harga = [100.0] * 20
    df = bingkai(harga)
    df.loc[21 if len(df) > 21 else len(df) - 1, "high"] = 100.0
    df = bingkai(harga + [100.0] * 5)
    # Bar terakhir menyapu jauh ke dua arah sekaligus.
    df.loc[len(df) - 1, "high"] = 200.0
    df.loc[len(df) - 1, "low"] = 1.0
    sinyal = np.zeros(len(df), dtype=int)
    sinyal[len(df) - 2] = 1
    hasil = jalankan(df, sinyal)
    assert hasil.jumlah_trade == 1
    assert hasil.perdagangan[0].alasan_keluar == "stop"


def test_hanya_satu_posisi_terbuka_pada_satu_waktu():
    df = bingkai([100.0] * 60)
    sinyal = np.zeros(len(df), dtype=int)
    sinyal[20:40] = 1
    hasil = jalankan(df, sinyal)
    for a, b in zip(hasil.perdagangan, hasil.perdagangan[1:]):
        assert a.keluar_ms <= b.masuk_ms


def test_short_dapat_dimatikan():
    df = bingkai([100.0] * 40)
    sinyal = np.zeros(len(df), dtype=int)
    sinyal[20] = -1
    assert jalankan(df, sinyal, Konfig(izinkan_short=False)).jumlah_trade == 0


def test_slippage_memperburuk_harga_masuk_kedua_arah():
    df = bingkai([100.0] * 40)
    for arah in (1, -1):
        sinyal = np.zeros(len(df), dtype=int)
        sinyal[20] = arah
        hasil = jalankan(df, sinyal, Konfig(slippage=0.001))
        if hasil.perdagangan:
            p = hasil.perdagangan[0]
            if arah == 1:
                assert p.harga_masuk > 100.0
            else:
                assert p.harga_masuk < 100.0


def test_ukuran_posisi_mempertaruhkan_pecahan_modal_yang_ditetapkan():
    """Invarian risiko: kerugian pada stop harus sama dengan risiko per trade."""
    df = bingkai([100.0] * 40)
    sinyal = np.zeros(len(df), dtype=int)
    sinyal[20] = 1
    k = Konfig(risiko_per_trade=0.01, modal_awal=10_000.0, slippage=0.0)
    hasil = jalankan(df, sinyal, k)
    if hasil.perdagangan:
        p = hasil.perdagangan[0]
        assert p.jarak_stop * p.ukuran == pytest.approx(100.0)


def test_biaya_transaksi_selalu_mengurangi_hasil():
    p = Perdagangan(
        symbol="X",
        arah=1,
        masuk_ms=AWAL,
        keluar_ms=AWAL + JAM,
        harga_masuk=100.0,
        harga_keluar=100.0,
        ukuran=1.0,
        jarak_stop=1.0,
        alasan_keluar="target",
        biaya_transaksi=0.1,
        biaya_funding=0.0,
        laba_kotor=0.0,
    )
    assert p.laba == pytest.approx(-0.1)
    assert p.R == pytest.approx(-0.1)


def test_funding_ditagih_dari_jadwal_untuk_posisi_long():
    df = bingkai([100.0] * 60)
    sinyal = np.zeros(len(df), dtype=int)
    sinyal[20] = 1
    j = Jadwal.dari_frame(
        pd.DataFrame(
            {
                "calc_time": [AWAL + i * 8 * JAM for i in range(10)],
                "last_funding_rate": [0.001] * 10,
            }
        )
    )
    hasil = jalankan(df, sinyal, jadwal=j)
    if hasil.perdagangan:
        assert hasil.perdagangan[0].biaya_funding >= 0.0


def test_tanpa_sinyal_ekuitas_tidak_bergerak():
    df = bingkai([100.0 + i for i in range(40)])
    hasil = jalankan(df, np.zeros(len(df), dtype=int))
    assert hasil.jumlah_trade == 0
    assert np.allclose(hasil.ekuitas, 10_000.0)


def test_ringkasan_tanpa_trade_tidak_mengarang_angka():
    """Winrate dari nol perdagangan tidak terdefinisi, bukan nol."""
    df = bingkai([100.0] * 30)
    r = jalankan(df, np.zeros(len(df), dtype=int)).ringkas()
    assert r["jumlah_trade"] == 0
    assert r["winrate"] is None
    assert r["ekspektasi_R"] is None


def test_panjang_sinyal_tidak_cocok_ditolak():
    df = bingkai([100.0] * 30)
    with pytest.raises(ValueError):
        jalankan(df, np.zeros(5, dtype=int))


def test_kolom_wajib_hilang_ditolak():
    df = bingkai([100.0] * 30).drop(columns=["high"])
    with pytest.raises(ValueError):
        jalankan(df, np.zeros(30, dtype=int))


def test_waktu_tidak_menaik_ditolak():
    df = bingkai([100.0] * 30)
    df.loc[5, "open_time"] = df.loc[4, "open_time"]
    with pytest.raises(ValueError):
        jalankan(df, np.zeros(30, dtype=int))


def test_konfig_menolak_parameter_mustahil():
    with pytest.raises(ValueError):
        Konfig(risiko_per_trade=1.5)
    with pytest.raises(ValueError):
        Konfig(atr_pengali_stop=0.0)
    with pytest.raises(ValueError):
        Konfig(imbalan_R=-1.0)
