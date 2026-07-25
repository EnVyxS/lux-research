"""Pengujian penagihan funding dari jadwal nyata.

Yang dikunci di sini adalah aturan yang tidak boleh berubah diam-diam: batas
rentang penagihan, tanda untuk long dan short, perilaku pada simbol yang
berpindah kisi, dan penolakan simbol tanpa jadwal.
"""

from __future__ import annotations

import pandas as pd
import pytest

from lux.funding_model import Jadwal, ambil_jadwal, funding_dalam_R

JAM = 3_600_000
JAM8 = 8 * JAM
AWAL = 1_600_000_000_000 - (1_600_000_000_000 % JAM8)


def jadwal(langkah: int, n: int, rate: float = 0.0001, mulai: int = AWAL) -> Jadwal:
    return Jadwal.dari_frame(
        pd.DataFrame(
            {
                "calc_time": [mulai + i * langkah for i in range(n)],
                "last_funding_rate": [rate] * n,
            }
        )
    )


def test_posisi_yang_tidak_melewati_penagihan_bebas_biaya():
    j = jadwal(JAM8, 10)
    assert j.jumlah_penagihan(AWAL + 1, AWAL + JAM8 - 1) == 0
    assert j.jumlah_rate(AWAL + 1, AWAL + JAM8 - 1) == 0.0


def test_masuk_tepat_pada_detik_penagihan_tidak_ikut_membayar():
    """Posisi belum dipegang saat potret diambil."""
    j = jadwal(JAM8, 10)
    assert j.jumlah_penagihan(AWAL, AWAL + JAM8 - 1) == 0


def test_keluar_tepat_pada_detik_penagihan_tetap_membayar():
    """Bila aturan batas keliru, ia menagih lebih, bukan kurang."""
    j = jadwal(JAM8, 10)
    assert j.jumlah_penagihan(AWAL, AWAL + JAM8) == 1


def test_jumlah_penagihan_sesuai_lama_posisi():
    j = jadwal(JAM8, 20)
    assert j.jumlah_penagihan(AWAL, AWAL + 5 * JAM8) == 5


def test_simbol_berpindah_kisi_tertagih_tanpa_kode_khusus():
    """Alasan utama modul ini ada.

    Rumus lama dengan pembagi delapan jam akan menagih 3 periode untuk rentang
    24 jam ini, padahal simbolnya sudah pindah ke kisi empat jam dan tertagih
    6 kali. Selisihnya bukan pembulatan, melainkan setengah dari biaya.
    """
    lama = [AWAL + i * JAM8 for i in range(10)]
    pindah = lama[-1]
    baru = [pindah + (i + 1) * 4 * JAM for i in range(10)]
    j = Jadwal.dari_frame(
        pd.DataFrame(
            {
                "calc_time": lama + baru,
                "last_funding_rate": [0.0001] * 20,
            }
        )
    )
    assert j.jumlah_penagihan(pindah, pindah + 24 * JAM) == 6
    assert j.jumlah_rate(pindah, pindah + 24 * JAM) == pytest.approx(0.0006)


def test_jeda_perdagangan_tidak_menagih_apa_pun():
    """Selama penghentian, bursa tidak menerbitkan penagihan."""
    t = [AWAL, AWAL + JAM8, AWAL + JAM8 + 504 * JAM]
    j = Jadwal.dari_frame(
        pd.DataFrame({"calc_time": t, "last_funding_rate": [0.0001] * 3})
    )
    assert j.jumlah_penagihan(AWAL + JAM8, AWAL + JAM8 + 100 * JAM) == 0


def test_rate_yang_berbeda_dijumlahkan_apa_adanya():
    j = Jadwal.dari_frame(
        pd.DataFrame(
            {
                "calc_time": [AWAL, AWAL + JAM8, AWAL + 2 * JAM8],
                "last_funding_rate": [0.0001, -0.0004, 0.0002],
            }
        )
    )
    assert j.jumlah_rate(AWAL - 1, AWAL + 2 * JAM8) == pytest.approx(-0.0001)


def test_long_membayar_saat_funding_positif():
    j = jadwal(JAM8, 5, rate=0.0001)
    biaya = funding_dalam_R(j, AWAL, AWAL + 3 * JAM8, stop_pecahan=0.01, arah=1)
    assert biaya == pytest.approx(0.03)


def test_short_dibayar_saat_funding_positif():
    """Tanda yang terbalik menghasilkan keuntungan palsu, jadi diuji terpisah."""
    j = jadwal(JAM8, 5, rate=0.0001)
    biaya = funding_dalam_R(j, AWAL, AWAL + 3 * JAM8, stop_pecahan=0.01, arah=-1)
    assert biaya == pytest.approx(-0.03)


def test_stop_sempit_membuat_funding_membengkak_dalam_R():
    """Biaya yang sama menjadi jauh lebih berat relatif terhadap risiko."""
    j = jadwal(JAM8, 5, rate=0.0001)
    lebar = funding_dalam_R(j, AWAL, AWAL + 3 * JAM8, stop_pecahan=0.05)
    sempit = funding_dalam_R(j, AWAL, AWAL + 3 * JAM8, stop_pecahan=0.005)
    assert sempit == pytest.approx(lebar * 10)


def test_arah_tidak_sah_ditolak():
    with pytest.raises(ValueError):
        funding_dalam_R(jadwal(JAM8, 3), AWAL, AWAL + JAM8, 0.01, arah=0)


def test_stop_nol_ditolak():
    with pytest.raises(ValueError):
        funding_dalam_R(jadwal(JAM8, 3), AWAL, AWAL + JAM8, 0.0)


def test_keluar_mendahului_masuk_ditolak():
    with pytest.raises(ValueError):
        jadwal(JAM8, 3).jumlah_rate(AWAL + JAM8, AWAL)


def test_simbol_tanpa_jadwal_ditolak_bukan_dianggap_gratis():
    """Menagih nol diam-diam adalah cara paling halus memalsukan keuntungan."""
    with pytest.raises(KeyError):
        ambil_jadwal({"BTCUSDT": jadwal(JAM8, 3)}, "ETHUSDT")


def test_jadwal_kosong_ditolak():
    kosong = Jadwal.dari_frame(
        pd.DataFrame({"calc_time": [], "last_funding_rate": []})
    )
    with pytest.raises(KeyError):
        ambil_jadwal({"BTCUSDT": kosong}, "BTCUSDT")


def test_urutan_masukan_tidak_memengaruhi_hasil():
    acak = pd.DataFrame(
        {
            "calc_time": [AWAL + 2 * JAM8, AWAL, AWAL + JAM8],
            "last_funding_rate": [0.0003, 0.0001, 0.0002],
        }
    )
    j = Jadwal.dari_frame(acak)
    assert j.jumlah_rate(AWAL - 1, AWAL + 2 * JAM8) == pytest.approx(0.0006)
    assert j.jumlah_penagihan(AWAL, AWAL + JAM8) == 1
