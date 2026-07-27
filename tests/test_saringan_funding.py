"""Uji saringan funding H-015 (ADR-037).

Yang diuji di sini adalah aritmetikanya, bukan hasil backtestnya: seluruh berkas
ini berjalan tanpa satu bar parquet pun dan tanpa mesin backtest, sesuai aturan
32. Jadwal funding diwakili boneka yang hanya menyediakan
``statistik_trailing``, sebab itulah **satu-satunya** jalur data funding yang
boleh dipakai modul yang diuji (ADR-037 §2) — dan boneka yang tidak menyediakan
apa pun selain itu membuat pelanggarannya gagal seketika alih-alih lolos diam.

Boneka itu juga menyediakan ``__len__``, dan pengecualian ini perlu dijelaskan
karena ia dibayar dengan satu run gagal (30245804583, tiga uji gugur dengan
``TypeError: object of type 'JadwalBoneka' has no len()``). ``ambil_jadwal``
menguji kesahihan hasil pencarian dengan ``len(j) == 0``: jadwal kosong
diperlakukan sama dengan jadwal yang tidak ada, supaya simbol tanpa data tidak
pernah diam-diam menjadi simbol berbiaya nol. Itu jalur **pencarian**, bukan
jalur **aritmetika funding**; boneka ini tetap tidak punya ``jumlah_rate``,
``jumlah_penagihan``, maupun ``kumulatif``, sehingga setiap upaya menghitung
funding di luar ``statistik_trailing`` tetap gugur seketika.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from lux.backtest.saringan_funding import (
    AMBANG_RATE,
    JENDELA_MS,
    MIN_PENAGIHAN,
    NAMA_SEL,
    SEED_ACAK_H015,
    arah_ditolak,
    bulan_utc,
    mask_tolak,
    penolakan_setara,
    simbol_bingkai,
    sinyal_sel,
    terapkan,
    waktu_bingkai,
)
from lux.funding_model import ambil_jadwal

JAM_MS = 3_600_000


class JadwalBoneka:
    """``statistik_trailing`` dan ``__len__``. Sengaja tidak punya yang lain."""

    def __init__(self, rerata, n=MIN_PENAGIHAN):
        self.rerata = rerata
        self.n = n
        self.dipanggil: list[tuple[int, int]] = []

    def __len__(self):
        return int(self.n)

    def statistik_trailing(self, sampai_ms, jendela_ms):
        self.dipanggil.append((int(sampai_ms), int(jendela_ms)))
        return self.rerata, self.n


def bingkai(n=6, simbol="AAAUSDT", mulai=1_700_000_000_000, langkah=4 * JAM_MS):
    return pd.DataFrame(
        {
            "open_time": [mulai + i * langkah for i in range(n)],
            "symbol": [simbol] * n,
            "close": np.arange(n, dtype="float64") + 1.0,
        }
    )


# --------------------------------------------------------------------------
# Putusan satu entri
# --------------------------------------------------------------------------
def test_long_ditolak_saat_funding_positif_melewati_ambang():
    assert arah_ditolak(1, AMBANG_RATE * 2, MIN_PENAGIHAN) is True


def test_long_diterima_saat_funding_negatif():
    assert arah_ditolak(1, -AMBANG_RATE * 2, MIN_PENAGIHAN) is False


def test_short_ditolak_saat_funding_negatif_melewati_ambang():
    """Tanda dibalik untuk short: pemegang short membayar saat rate negatif."""
    assert arah_ditolak(-1, -AMBANG_RATE * 2, MIN_PENAGIHAN) is True


def test_short_diterima_saat_funding_positif():
    assert arah_ditolak(-1, AMBANG_RATE * 2, MIN_PENAGIHAN) is False


def test_ambang_tidak_inklusif():
    """Tepat di ambang bukan pelanggaran; hanya yang melewatinya ditolak."""
    assert arah_ditolak(1, AMBANG_RATE, MIN_PENAGIHAN) is False


def test_jadwal_tipis_menolak_meski_funding_menguntungkan():
    """Data tipis berbahaya, bukan netral (ADR-037 §3)."""
    assert arah_ditolak(1, -1.0, MIN_PENAGIHAN - 1) is True


def test_penagihan_tepat_di_minimum_dinilai():
    assert arah_ditolak(1, -1.0, MIN_PENAGIHAN) is False


def test_rerata_kosong_menolak():
    assert arah_ditolak(1, None, MIN_PENAGIHAN + 5) is True


def test_sinyal_nol_tidak_pernah_ditolak():
    assert arah_ditolak(0, 1.0, 0) is False


# --------------------------------------------------------------------------
# Mask atas satu bingkai
# --------------------------------------------------------------------------
def test_mask_hanya_menanyakan_bar_bersinyal():
    j = JadwalBoneka(0.0)
    s = np.array([0, 1, 0, -1, 0, 0])
    t = waktu_bingkai(bingkai())
    mask_tolak(s, t, j)
    assert len(j.dipanggil) == 2


def test_mask_memakai_open_time_bar_itu_sendiri():
    """Bukan bar berikutnya: memakai bar berikutnya adalah kebocoran."""
    j = JadwalBoneka(0.0)
    df = bingkai()
    t = waktu_bingkai(df)
    s = np.array([0, 0, 1, 0, 0, 0])
    mask_tolak(s, t, j)
    assert j.dipanggil == [(int(t[2]), JENDELA_MS)]


def test_mask_tanpa_jadwal_menolak_seluruh_entri():
    s = np.array([1, 0, -1, 0, 1, 0])
    t = waktu_bingkai(bingkai())
    hasil = mask_tolak(s, t, None)
    assert hasil.tolist() == [True, False, True, False, True, False]


def test_mask_menolak_panjang_tidak_sepadan():
    with pytest.raises(ValueError, match="panjang sinyal"):
        mask_tolak(np.array([1, 0]), np.array([1, 2, 3]), JadwalBoneka(0.0))


# --------------------------------------------------------------------------
# Penolakan acak setara — inti falsifikasi
# --------------------------------------------------------------------------
def test_penolakan_setara_menjaga_cacah_per_arah():
    s = np.array([1, 1, 1, 1, -1, -1, -1, -1])
    tolak = np.array([True, True, False, False, True, False, False, False])
    b = np.array(["2026-01"] * 8, dtype=object)
    hasil = penolakan_setara(s, tolak, b)
    assert int(hasil[s == 1].sum()) == 2
    assert int(hasil[s == -1].sum()) == 1


def test_penolakan_setara_menjaga_cacah_per_bulan():
    s = np.array([1, 1, 1, 1])
    tolak = np.array([True, False, False, False])
    b = np.array(["2026-01", "2026-01", "2026-02", "2026-02"], dtype=object)
    hasil = penolakan_setara(s, tolak, b)
    assert int(hasil[:2].sum()) == 1
    assert int(hasil[2:].sum()) == 0


def test_penolakan_setara_tidak_pernah_menyentuh_bar_tanpa_sinyal():
    s = np.array([1, 0, 1, 0, 1])
    tolak = np.array([True, False, True, False, False])
    b = np.array(["2026-01"] * 5, dtype=object)
    hasil = penolakan_setara(s, tolak, b)
    assert not hasil[s == 0].any()


def test_penolakan_setara_berulang_sama_dengan_seed_sama():
    s = np.array([1] * 10)
    tolak = np.array([True] * 4 + [False] * 6)
    b = np.array(["2026-03"] * 10, dtype=object)
    a = penolakan_setara(s, tolak, b, seed=SEED_ACAK_H015)
    c = penolakan_setara(s, tolak, b, seed=SEED_ACAK_H015)
    assert a.tolist() == c.tolist()


def test_penolakan_setara_umumnya_memilih_entri_yang_lain():
    """Bila ia memilih entri yang sama persis, ia bukan pembanding."""
    s = np.array([1] * 20)
    tolak = np.array([True] * 10 + [False] * 10)
    b = np.array(["2026-04"] * 20, dtype=object)
    hasil = penolakan_setara(s, tolak, b)
    assert hasil.tolist() != tolak.tolist()
    assert int(hasil.sum()) == 10


def test_penolakan_setara_seluruhnya_ditolak_tetap_seluruhnya():
    s = np.array([1, 1, 1])
    tolak = np.array([True, True, True])
    b = np.array(["2026-05"] * 3, dtype=object)
    assert penolakan_setara(s, tolak, b).tolist() == [True, True, True]


def test_penolakan_setara_menolak_panjang_tidak_sepadan():
    with pytest.raises(ValueError, match="tidak sepadan"):
        penolakan_setara(np.array([1, 1]), np.array([True]), np.array(["x"], dtype=object))


# --------------------------------------------------------------------------
# Bingkai, bulan, penerapan
# --------------------------------------------------------------------------
def test_simbol_bingkai_membaca_kolom():
    assert simbol_bingkai(bingkai(simbol="XYZUSDT")) == "XYZUSDT"


def test_simbol_bingkai_menolak_bingkai_campuran():
    df = bingkai(n=2)
    df.loc[1, "symbol"] = "LAINUSDT"
    with pytest.raises(ValueError, match="wajib tepat satu"):
        simbol_bingkai(df)


def test_simbol_bingkai_menolak_kolom_hilang():
    df = bingkai().drop(columns=["symbol"])
    with pytest.raises(ValueError, match="tanpa kolom"):
        simbol_bingkai(df)


def test_bulan_utc_memberi_label_yang_benar():
    # 2026-01-01T00:00:00Z
    assert bulan_utc(np.array([1_767_225_600_000], dtype="int64"))[0] == "2026-01"


def test_terapkan_tidak_menyunting_di_tempat():
    s = np.array([1, -1, 1])
    hasil = terapkan(s, np.array([True, False, False]))
    assert s.tolist() == [1, -1, 1]
    assert hasil.tolist() == [0, -1, 1]


# --------------------------------------------------------------------------
# Kontrak pencarian jadwal
# --------------------------------------------------------------------------
def test_jadwal_kosong_ditolak_seperti_jadwal_yang_tidak_ada():
    """``len(j) == 0`` adalah uji kesahihan, bukan basa-basi.

    Inilah jalur yang membuat run 30245804583 gagal, dan ia dikunci di sini
    supaya perbaikan boneka tidak diam-diam melemahkannya.
    """
    with pytest.raises(KeyError):
        ambil_jadwal({"AAAUSDT": JadwalBoneka(0.0, n=0)}, "AAAUSDT")


def test_sel_f_dengan_jadwal_kosong_menolak_bukan_meloloskan():
    j = {"AAAUSDT": JadwalBoneka(-1.0, n=0)}
    f = sinyal_sel("F", j, dasar_tetap(1))
    assert f(bingkai(), {}).tolist() == [0] * 6


# --------------------------------------------------------------------------
# Tiga sel
# --------------------------------------------------------------------------
def dasar_tetap(arah):
    def f(df, params):
        return np.full(len(df), arah, dtype="int64")

    return f


def test_sel_kontrol_adalah_fungsi_dasar_itu_sendiri():
    """Bukan pembungkus yang kebetulan tidak menolak apa pun."""
    d = dasar_tetap(1)
    assert sinyal_sel("K", {}, d) is d


def test_sel_f_menolak_long_saat_funding_positif():
    j = {"AAAUSDT": JadwalBoneka(AMBANG_RATE * 5)}
    f = sinyal_sel("F", j, dasar_tetap(1))
    assert f(bingkai(), {}).tolist() == [0] * 6


def test_sel_f_meloloskan_short_saat_funding_positif():
    j = {"AAAUSDT": JadwalBoneka(AMBANG_RATE * 5)}
    f = sinyal_sel("F", j, dasar_tetap(-1))
    assert f(bingkai(), {}).tolist() == [-1] * 6


def test_sel_a_membuang_cacah_yang_sama_dengan_sel_f():
    j = {"AAAUSDT": JadwalBoneka(AMBANG_RATE * 5)}
    df = bingkai(n=12)
    n_f = int((sinyal_sel("F", j, dasar_tetap(1))(df, {}) == 0).sum())
    n_a = int((sinyal_sel("A", j, dasar_tetap(1))(df, {}) == 0).sum())
    assert n_f == n_a == 12


def test_sel_f_tanpa_jadwal_simbol_menolak_semuanya():
    f = sinyal_sel("F", {}, dasar_tetap(1))
    assert f(bingkai(), {}).tolist() == [0] * 6


def test_sel_tidak_dikenal_ditolak():
    with pytest.raises(ValueError, match="sel tidak dikenal"):
        sinyal_sel("Z", {}, dasar_tetap(1))


def test_nama_sel_persis_tiga_dan_urutannya_tetap():
    assert NAMA_SEL == ("K", "F", "A")


def test_ambang_beku_tidak_bergeser():
    """Pagar terhadap penggeseran ambang sesudah hasil terlihat (ADR-037 §10)."""
    assert AMBANG_RATE == 0.0001
    assert MIN_PENAGIHAN == 30
    assert SEED_ACAK_H015 == 20260727
