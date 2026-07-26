"""Dua pengaman H-013 yang TIDAK dibaca oleh pemuat config.

Berkas ini berdiri terpisah karena isinya bukan tentang rancangan H-013 melainkan
tentang satu cacat yang ditemukan run 30213913942: ``config/lux.yaml`` memuat
``maks_biaya_masuk_R`` dan ``stop_hormati_celah``, dan ``muat_konfig_h002`` tidak
pernah membaca keduanya. Angka yang hidup di berkas tetapi tidak di dalam program
lebih sulit terlihat daripada angka yang salah, sebab berkasnya tampak benar.

Uji kedua di bawah **mengunci cacatnya**, bukan memperbaikinya. Pemuat itu dipakai
dua belas hipotesis; menyentuhnya akan mengubah arti laporan yang sudah dikomit.
Bila suatu hari ia diperbaiki, uji ini akan gagal dan memaksa perbaikannya
dijurnalkan alih-alih menyelinap.
"""

from __future__ import annotations

from pathlib import Path

from lux.backtest.engine import Konfig
from lux.backtest.run_h002 import muat_konfig_h002
from lux.backtest.run_h013 import dasar_riset
from lux.degenerasi import AMBANG_BIAYA_MASUK_R

CONFIG_UJI = """
versi: 2
biaya:
  fee_efektif: 0.0005
  slippage: 0.0005
risiko:
  atr_periode: 14
  atr_pengali_stop: 2.0
  risiko_per_trade: 0.005
  maks_umur_bar: 168
  maks_carry_R: 0.25
  jendela_carry_hari: 30
  maks_biaya_masuk_R: 0.5
  stop_hormati_celah: true
"""


def test_dasar_riset_menyalakan_pengaman_dan_hormati_celah():
    """Kedua medan dipasang, dan tidak ada medan lain yang bergeser."""
    awal = Konfig(maks_carry_R=0.25, maks_umur_bar=168)
    assert awal.maks_biaya_masuk_R == 0.0
    assert awal.stop_hormati_celah is False

    k = dasar_riset(awal)
    assert k.maks_biaya_masuk_R == AMBANG_BIAYA_MASUK_R > 0
    assert k.stop_hormati_celah is True
    # Sisanya tidak disentuh: dasar_riset memasang pengaman, bukan menyetel ulang.
    assert k.maks_carry_R == 0.25
    assert k.maks_umur_bar == 168
    assert k.imbalan_R == awal.imbalan_R
    assert k.pakai_target is awal.pakai_target


def test_muat_konfig_h002_tidak_memetakan_pengaman_maupun_celah(tmp_path: Path):
    """Cacat dikunci sebagai perilaku, bukan sebagai catatan.

    Config di bawah memuat ``maks_biaya_masuk_R: 0.5`` dan
    ``stop_hormati_celah: true``; keduanya diabaikan oleh pemuat, jadi H-013 wajib
    memasangnya sendiri. Inilah sebab run 30213913942 mati di pagar.
    """
    p = tmp_path / "lux.yaml"
    p.write_text(CONFIG_UJI, encoding="utf-8")

    k = muat_konfig_h002(p)
    # Yang DIPETAKAN.
    assert k.maks_carry_R == 0.25
    assert k.maks_umur_bar == 168
    assert k.fee == 0.0005
    # Yang TIDAK dipetakan meskipun tertulis di berkas.
    assert k.maks_biaya_masuk_R == 0.0
    assert k.stop_hormati_celah is False
    # Dan dasar_riset menutup selisih itu.
    assert dasar_riset(k).maks_biaya_masuk_R == 0.5
    assert dasar_riset(k).stop_hormati_celah is True
