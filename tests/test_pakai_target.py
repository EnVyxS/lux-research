"""Pengujian medan ``pakai_target`` (ADR-020 langkah 2).

Yang dijaga di sini bukan fitur barunya, melainkan **kenetralan bawaannya**. Medan
yang bawaannya menggeser perilaku akan mengubah arti dua belas laporan hipotesis
yang sudah dikomit, dan pergeseran itu tidak akan berbunyi di mana pun: laporannya
tetap terbentuk, angkanya tetap masuk akal, hanya nilainya yang lain.

Bingkai uji dibuat sekecil mungkin tetapi cukup panjang untuk ATR periode 14,
sebab bar dengan ATR NaN tidak boleh diperdagangkan dan entri akan diam-diam tidak
terjadi — pengujian yang lulus karena tidak ada perdagangan sama sekali adalah
pengujian yang tidak menguji apa pun.
"""

from __future__ import annotations

import dataclasses

import numpy as np
import pandas as pd
import pytest

from lux.backtest.engine import Konfig, jalankan

MS = 3_600_000


def bingkai(harga: list[float], lebar: float = 1.0) -> pd.DataFrame:
    """Bingkai OHLC sederhana: satu harga per bar, ditambah rentang intrabar.

    ``lebar`` menjaga ATR tetap positif. Tanpa rentang intrabar, ATR bisa nol dan
    entri ditolak oleh ``jarak > 0``, sehingga pengujian lulus tanpa menguji.
    """
    n = len(harga)
    return pd.DataFrame(
        {
            "open_time": [i * MS for i in range(n)],
            "open": harga,
            "high": [p + lebar for p in harga],
            "low": [p - lebar for p in harga],
            "close": harga,
        }
    )


def sinyal_di(n: int, indeks: int) -> np.ndarray:
    """Sinyal long tunggal pada penutupan bar ``indeks``; entri di bar berikutnya."""
    s = np.zeros(n, dtype="int64")
    s[indeks] = 1
    return s


def test_pakai_target_bawaan_menyala_dan_medan_paling_akhir():
    medan = [f.name for f in dataclasses.fields(Konfig)]
    # Dibaca dari definisi, bukan disalin dari sumbernya (aturan 31).
    assert medan[-1] == "pakai_target"
    assert Konfig().pakai_target is True
    # Medan ADR-016 wajib tetap tepat di depannya: posisi argumen medan lama
    # tidak boleh bergeser oleh penambahan ini.
    assert medan[-2] == "stop_hormati_celah"


def test_bawaan_medan_lama_tidak_bergeser():
    """Lima saringan lama wajib tetap MATI secara bawaan.

    Bila salah satu berubah, hasil H-001b berhenti dapat diulang, dan itu tidak
    akan terlihat dari laporan mana pun.
    """
    k = Konfig()
    assert k.maks_umur_bar == 0
    assert k.maks_carry_R == 0.0
    assert k.maks_carry_realisasi_R == 0.0
    assert k.maks_biaya_masuk_R == 0.0
    assert k.stop_hormati_celah is False
    assert k.imbalan_R == 2.0


def test_target_dinilai_saat_menyala_dan_tidak_saat_mati():
    """Bingkai yang sama, satu medan berbeda, dua jalur keluar yang berbeda.

    Harga melonjak jauh sesudah entri sehingga target PASTI tersentuh ketika ia
    ada. Karena itu munculnya ``target`` pada satu sisi dan hilangnya ia pada sisi
    lain sepenuhnya ditentukan oleh medannya, bukan oleh kebetulan data.
    """
    harga = [100.0] * 20 + [400.0] * 10
    df = bingkai(harga)
    s = sinyal_di(len(harga), 18)

    hidup = jalankan(df, s, Konfig(maks_umur_bar=5))
    mati = jalankan(df, s, Konfig(maks_umur_bar=5, pakai_target=False))

    assert [p.alasan_keluar for p in hidup.perdagangan] == ["target"]
    assert "target" not in [p.alasan_keluar for p in mati.perdagangan]
    # Keduanya benar-benar berdagang; bila salah satu kosong, uji ini hampa.
    assert hidup.jumlah_trade >= 1
    assert mati.jumlah_trade >= 1


def test_tanpa_target_keluar_lewat_umur():
    """Tanpa target dan tanpa stop tersentuh, satu-satunya jalan keluar adalah umur.

    Harga dijaga datar sesudah entri supaya stop tidak kena, dan ``umur`` mengisi
    pada pembukaan bar — yaitu harga bar sungguhan, jalur yang jujur terhadap celah.
    """
    harga = [100.0] * 40
    df = bingkai(harga)
    s = sinyal_di(len(harga), 18)

    hasil = jalankan(df, s, Konfig(maks_umur_bar=3, pakai_target=False))

    alasan = [p.alasan_keluar for p in hasil.perdagangan]
    assert "umur" in alasan
    assert "target" not in alasan
    # Umur diukur dalam bar sejak entri, bukan dalam waktu tempel.
    p = hasil.perdagangan[0]
    assert (p.keluar_ms - p.masuk_ms) == 3 * MS


def test_tanpa_target_tanpa_batas_umur_gagal_keras():
    """Horizon tetap tanpa horizon ditolak di pembuat Konfig, bukan di laporan.

    Bila ia dibiarkan lewat, run akan selesai dengan tenang dan seluruh
    perdagangan keluar lewat stop dan akhir_data — hasil yang tampak masuk akal
    untuk sel yang sebenarnya tidak menguji horizon apa pun.
    """
    with pytest.raises(ValueError) as e:
        Konfig(pakai_target=False)
    assert "maks_umur_bar" in str(e.value)
    # Menyala bersama umur nol tetap sah: itu perilaku sebelas hipotesis lama.
    assert Konfig(pakai_target=True, maks_umur_bar=0).maks_umur_bar == 0
