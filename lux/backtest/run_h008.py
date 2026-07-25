"""H-008 — pengaman carry keras, sinyal tidak diubah sama sekali (ADR-008).

H-007 adalah hasil terbaik yang pernah diukur (+0,04044R) dan dijatuhkan oleh
``invarian_risiko`` pada −1,977R, bukan oleh ekspektasinya. Gerbang itu sudah
menjatuhkan empat dari tujuh hipotesis, dan penyebabnya diketahui: saringan
carry ADR-004 hanya menebak sekali di saat entri.

Modul ini menambahkan satu sumbu parameter — ambang carry **terealisasi** yang
memaksa posisi ditutup — dan membiarkan walk-forward memilihnya, termasuk
memilih 0,0 yang berarti menolak pengaman ini sama sekali.

``lux/strategi/`` tidak disentuh, sama seperti H-007.

Pemakaian:
    python -m lux.backtest.run_h008 --dir aset --limit 40
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import replace
from pathlib import Path

from lux.backtest.engine import Konfig
from lux.backtest.run_h002 import hipotesis_h002, muat_konfig_h002
from lux.backtest.runner import Opsi, Spek, jalankan_spek, muat_konteks
from lux.praregistrasi import Hipotesis, Kriteria
from lux.strategi import breakout_atr

# Grid lookback dan imbalan disalin PERSIS dari H-007. Mempersempitnya karena
# 4R menang di sana berarti menyetel ruang pencarian setelah melihat hasil,
# dan itu bentuk penyetelan pasca-hoc yang paling mudah dibela sekaligus
# paling merusak.
LOOKBACK = [20, 55, 100]
IMBALAN = [1.0, 2.0, 3.0, 4.0]
# 0,0 berarti pengaman MATI. Ia ikut dilombakan supaya percobaan ini informatif
# ke dua arah: bila walk-forward jarang memilih nilai selain 0,0, itu bukti
# bahwa pengaman ini merugikan, didapat dari run yang sama.
CARRY_KERAS = [0.0, 0.25, 0.50]

# Disalin kata per kata dari hipotesis_h002, sama seperti H-007. Diuji
# kesamaannya di tests/test_run_h008.py.
DATASET = (
    "tier-b-v1 ohlcv_1h + funding_shard, "
    "universe_layak_v2 438 simbol (ADR-003, ekor datar dipangkas)"
)


def kandidat() -> list[dict]:
    return [
        {"lookback": lb, "imbalan_R": im, "maks_carry_realisasi_R": ck}
        for lb in LOOKBACK
        for im in IMBALAN
        for ck in CARRY_KERAS
    ]


def buat_konfig(params: dict, dasar: Konfig) -> Konfig:
    """Konfig per kandidat: hanya imbalan dan ambang carry keras yang berubah.

    Seluruh medan lain — fee, slippage, pengali stop, saringan carry ADR-004 —
    diwarisi apa adanya. Saringan proyeksi ADR-004 sengaja **tetap menyala**:
    ADR-008 menambah pengaman, bukan menggantinya, dan mematikannya di sini
    akan mencampur dua perubahan dalam satu percobaan.
    """
    return replace(
        dasar,
        imbalan_R=float(params["imbalan_R"]),
        maks_carry_realisasi_R=float(params["maks_carry_realisasi_R"]),
    )


def hipotesis_h008(konfig: Konfig, komit: str = "") -> Hipotesis:
    return Hipotesis(
        id="H-008",
        pernyataan=(
            "Dengan sinyal Donchian yang tidak diubah sama sekali, menambahkan "
            "keluar paksa saat carry TEREALISASI melewati ambang yang dipilih "
            "walk-forward menghasilkan ekspektasi bersih di luar sampel minimal "
            "0,05R dan membuat gerbang invarian_risiko lulus. Saringan ADR-004 "
            "menebak biaya sekali di saat entri dan tidak pernah menilai ulang; "
            "pengaman ini tidak menebak apa pun, ia menjumlahkan penagihan yang "
            "sudah terjadi pada pembukaan tiap bar."
        ),
        dataset=DATASET,
        ruang_parameter={
            "lookback": LOOKBACK,
            "imbalan_R": IMBALAN,
            "maks_carry_realisasi_R": CARRY_KERAS,
            "atr_pengali_stop": [konfig.atr_pengali_stop],
            "maks_umur_bar": [konfig.maks_umur_bar],
            "maks_carry_R": [konfig.maks_carry_R],
            "jendela_carry_hari": [konfig.jendela_carry_hari],
        },
        # Percobaan tunggal, jadi tidak ada koreksi multiplisitas. Kriterianya
        # sama persis dengan H-002 dan H-007.
        kriteria=Kriteria(
            min_ekspektasi_R=0.05,
            min_trade_luar_sampel=100,
            maks_p_entri_acak=0.05,
            min_jendela_positif_rasio=0.5,
        ),
        komit=komit,
    )


def spek_h008(konfig: Konfig, komit: str = "") -> Spek:
    return Spek(
        h=hipotesis_h008(konfig, komit),
        sinyal=breakout_atr.sinyal,
        kandidat=kandidat(),
        nama="h008_carry_keras",
        params_lookahead={"lookback": 55},
        buat_konfig=buat_konfig,
    )


# Pembanding tetap, disalin dari laporan yang sudah dikomit. Tidak satu pun
# dijalankan ulang.
PEMBANDING = {
    "H-002": (0.03159, "tidak ada"),
    "H-007": (0.04044, "invarian_risiko -1.9769"),
}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--interval", default="1h")
    ap.add_argument("--universe", default="reports/universe_layak_v2.json")
    ap.add_argument("--akhir-sejati", default="reports/akhir_sejati.json")
    ap.add_argument("--config", default="config/lux.yaml")
    ap.add_argument("--out", default="reports")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--ulangan", type=int, default=100)
    ap.add_argument("--komit", default="")
    a = ap.parse_args(argv)

    konfig = muat_konfig_h002(Path(a.config))

    # Dataset wajib identik dengan H-002 dan H-007; bila tidak, perbandingannya
    # tidak sah. Diperiksa sebelum satu bar pun dimuat, bukan di ujung run.
    if hipotesis_h008(konfig).dataset != hipotesis_h002(konfig).dataset:
        raise ValueError("dataset H-008 tidak identik dengan H-002")

    # Saringan proyeksi ADR-004 wajib tetap menyala, kalau tidak yang diukur
    # bukan tambahan pengaman melainkan pertukaran satu pengaman dengan yang
    # lain. Diperiksa di sini, bukan diasumsikan dari isi berkas konfigurasi.
    if konfig.maks_carry_R <= 0:
        raise ValueError("H-008 menuntut saringan ADR-004 tetap menyala")

    opsi = Opsi(
        dir_aset=Path(a.dir),
        out=Path(a.out),
        interval=a.interval,
        universe=Path(a.universe),
        akhir_sejati=Path(a.akhir_sejati),
        limit=a.limit,
        ulangan=a.ulangan,
    )

    print(f"ADR-004 proyeksi: maks_carry_R={konfig.maks_carry_R}", flush=True)
    print(f"ADR-008 ambang carry keras yang dilombakan: {CARRY_KERAS}", flush=True)
    print(f"kandidat: {len(kandidat())} kombinasi", flush=True)
    for id_, (eks, gerbang) in PEMBANDING.items():
        print(f"  pembanding {id_}: {eks:+.5f}R, gerbang gagal: {gerbang}", flush=True)

    ktx = muat_konteks(opsi)
    hasil = jalankan_spek(spek_h008(konfig, a.komit), ktx, konfig, opsi)

    keluar = hasil["alasan_keluar"]
    print(f"\nkeluar karena pengaman carry: {keluar.get('carry', 0)}", flush=True)
    print(f"gerbang gagal: {hasil['gerbang_gagal']}", flush=True)
    print(
        f"ekspektasi {hasil['ekspektasi_R']} vs H-007 {PEMBANDING['H-007'][0]}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
