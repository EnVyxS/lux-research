"""Pengujian pembongkaran biaya per perdagangan.

Gerbang invarian risiko menjatuhkan run pilot dengan kerugian terburuk
-2,585R. Mesin selalu mengisi stop tepat di harga stop, sehingga kerugian yang
berasal dari harga tidak mungkin melewati 1R. Sisanya wajib berasal dari biaya.
Pengujian ini mengunci aritmetika pembongkarannya supaya klaim itu dapat
diperiksa ulang, bukan dipercaya.
"""

from lux.backtest.engine import Perdagangan
from lux.backtest.run_wf import diagnosa_biaya, rincian_R


def buat(**kw) -> Perdagangan:
    dasar = dict(
        symbol="XUSDT",
        arah=1,
        masuk_ms=0,
        keluar_ms=3_600_000,
        harga_masuk=100.0,
        harga_keluar=99.0,
        ukuran=10.0,
        jarak_stop=1.0,
        alasan_keluar="stop",
        biaya_transaksi=0.0,
        biaya_funding=0.0,
        laba_kotor=-10.0,
    )
    dasar.update(kw)
    return Perdagangan(**dasar)


def test_stop_tanpa_biaya_rugi_tepat_satu_R():
    # Risiko = jarak_stop * ukuran = 1,0 * 10 = 10. Kerugian kotor 10.
    r = rincian_R(buat())
    assert r["R"] == -1.0
    assert r["kotor_R"] == -1.0
    assert r["transaksi_R"] == 0.0


def test_biaya_transaksi_mendorong_kerugian_melewati_satu_R():
    r = rincian_R(buat(biaya_transaksi=10.0))
    assert r["transaksi_R"] == 1.0
    assert r["R"] == -2.0


def test_komponen_selalu_menjumlah_kembali_ke_R():
    r = rincian_R(buat(biaya_transaksi=3.0, biaya_funding=2.5))
    assert abs((r["kotor_R"] - r["transaksi_R"] - r["funding_R"]) - r["R"]) < 1e-12


def test_funding_negatif_justru_mengurangi_kerugian():
    # Funding bisa dibayarkan kepada pemegang posisi, bukan hanya ditagih.
    r = rincian_R(buat(biaya_funding=-5.0))
    assert r["funding_R"] == -0.5
    assert r["R"] == -0.5


def test_stop_frac_adalah_jarak_stop_terhadap_harga_masuk():
    r = rincian_R(buat())
    assert abs(r["stop_frac"] - 0.01) < 1e-12


def test_risiko_nol_tidak_melempar():
    r = rincian_R(buat(jarak_stop=0.0))
    assert r["R"] == 0.0
    assert r["stop_frac"] == 0.0


def test_diagnosa_mengurutkan_yang_terburuk_lebih_dulu():
    d = diagnosa_biaya(
        [
            buat(laba_kotor=20.0, alasan_keluar="target"),
            buat(biaya_transaksi=10.0),
            buat(),
        ],
        n=2,
    )
    assert d["jumlah"] == 3
    assert [round(x["R"], 6) for x in d["terburuk"]] == [-2.0, -1.0]


def test_diagnosa_menghitung_perdagangan_yang_biayanya_melebihi_satu_R():
    d = diagnosa_biaya(
        [
            buat(biaya_transaksi=12.0),
            buat(biaya_transaksi=1.0),
            buat(biaya_transaksi=6.0, biaya_funding=6.0),
        ]
    )
    assert d["trade_biaya_lebih_1R"] == 2


def test_diagnosa_atas_daftar_kosong_tidak_mengarang_rerata():
    d = diagnosa_biaya([])
    assert d["jumlah"] == 0
    assert d["rerata_transaksi_R"] is None
    assert d["terburuk"] == []
