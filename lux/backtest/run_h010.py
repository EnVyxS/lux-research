"""H-010 - dinding grid imbalan digeser ke luar (ADR-012).

H-007, H-008, dan H-009 memakai grid imbalan yang sama, `[1, 2, 3, 4]`, dan di
ketiganya pemilih walk-forward menempel di batas atas. Di H-009 imbalan 4,0
dipilih 194 dari 356 jendela, yaitu 54,5%.

Selama tiga hipotesis saya membaca pola itu sebagai bukti bahwa menurunkan
titik impas bekerja. Itu benar, tetapi ada tafsiran kedua yang tidak pernah
diperiksa: optimumnya mungkin berada di luar grid, dan yang terukur hanya
dinding grid. Selama dindingnya tidak digeser, kedua tafsiran itu tidak dapat
dipisahkan. Itu cacat rancangan H-007, bukan hipotesis baru.

Maka H-010 mengubah tepat satu hal: `IMBALAN` menjadi `[2, 4, 6, 8]`. Dua
jangkar lama dipertahankan supaya hasilnya sebanding, jumlah kombinasi tetap
dua belas supaya multiplisitasnya identik, dan `LOOKBACK` tidak disentuh.

Catatan implementasi yang penting. `run_h009` mengimpor grid dari `run_h007`
dan menolak berjalan bila keduanya berbeda, jadi grid H-007 haram disentuh:
mengubahnya akan membatalkan penjaga H-009 dan mengubah arti laporan yang
sudah dikomit. Modul ini karena itu mendefinisikan gridnya sendiri, tetapi
mengimpor `buat_konfig`, `DATASET`, `KUNCI_TERLARANG`, dan `AMBANG_CARRY_KERAS`
dari `run_h009` apa adanya. Pematokan pengaman carry dijalankan oleh kode yang
sama persis, bukan oleh salinan yang bisa melenceng diam-diam.

Bahaya yang sudah diketahui sebelum run: target lebih jauh berarti pegangan
lebih lama, jadi perdagangan tak selesai membengkak dan carry membesar. Porsi
perdagangan tak selesai dicetak sebelum ekspektasi ditafsirkan. Bila mayoritas
perdagangan berakhir karena batas umur, yang terukur adalah batas umur, bukan
struktur keluar. Ini juga hipotesis pertama tempat gerbang kesebelas mengikat.

`lux/strategi/` tidak disentuh, sama seperti H-007, H-008, dan H-009.

Pemakaian:
    python -m lux.backtest.run_h010 --dir aset --limit 40
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lux.analisis.titik_impas import ALASAN_TIDAK_SELESAI, titik_impas
from lux.backtest.engine import Konfig
from lux.backtest.run_h002 import hipotesis_h002, muat_konfig_h002
from lux.backtest.run_h007 import IMBALAN as IMBALAN_H007
from lux.backtest.run_h007 import LOOKBACK as LOOKBACK_H007
from lux.backtest.run_h009 import (
    AMBANG_CARRY_KERAS,
    DATASET,
    KUNCI_TERLARANG,
    buat_konfig,
)
from lux.backtest.runner import Opsi, Spek, jalankan_spek, muat_konteks
from lux.praregistrasi import Hipotesis, Kriteria
from lux.strategi import breakout_atr

# LOOKBACK diimpor, IMBALAN tidak. Perbedaan itulah keseluruhan isi ADR-012.
LOOKBACK = list(LOOKBACK_H007)
IMBALAN = [2.0, 4.0, 6.0, 8.0]

# Dua nilai yang wajib bertahan supaya H-010 sebanding dengan H-009. Bila
# keduanya hilang, perubahan ekspektasi tidak dapat dipisahkan dari perubahan
# grid.
JANGKAR = (2.0, 4.0)

# Pembanding tetap, disalin dari laporan yang sudah dikomit. Tidak satu pun
# dijalankan ulang.
PEMBANDING = {
    "H-007": (0.04044, "invarian_risiko -1.9769"),
    "H-008": (0.04126, "invarian_risiko -1.9769"),
    "H-009": (0.041359, "tidak ada, ditolak oleh ambang 0,05R"),
}

# Ukuran H-009 yang menjadi titik banding, dari reports/backtest_h009_*.json.
H009_LAJU_TARGET = 4111 / 14925
H009_PORSI_TAK_SELESAI = (368 + 188 + 16) / 14925
H009_PORSI_FUNDING_EKOR = 0.165

# Ditulis sebelum run, sama seperti di ADR-012 bagian 5. Ramalan keempat
# sengaja merugikan hipotesis ini sendiri.
RAMALAN = {
    "porsi_jendela_imbalan_8": (
        "30-55 persen; di atas 54,5 persen berarti penempelan bersifat "
        "mekanis, di bawah 25 persen berarti dinding H-007 bukan dinding"
    ),
    "laju_kena_target": "turun ke 0,13-0,20 dari 0,27544",
    "porsi_tak_selesai": "naik dari 3,7 persen ke lebih dari 12 persen",
    "porsi_funding_ekor_maks": (
        "naik ke 0,20-0,35; di atas 0,35 gerbang kesebelas GAGAL dan itu "
        "temuan, bukan alasan melonggarkan ambang"
    ),
    "ekspektasi_R": "0,030-0,048, jadi tidak mencapai 0,05",
}


def kandidat() -> list[dict]:
    """Grid H-009 dengan satu dinding digeser: imbalan, bukan lookback."""
    return [
        {"lookback": lb, "imbalan_R": im} for lb in LOOKBACK for im in IMBALAN
    ]


def hipotesis_h010(konfig: Konfig, komit: str = "") -> Hipotesis:
    return Hipotesis(
        id="H-010",
        pernyataan=(
            "Pada H-007, H-008, dan H-009 pemilih walk-forward menempel di "
            "batas atas grid imbalan, 194 dari 356 jendela di H-009. Selama "
            "dinding itu tidak digeser, dua tafsiran tidak dapat dipisahkan: "
            "optimum berada di 4R, atau optimum berada di luar grid dan yang "
            "terukur hanyalah dindingnya. H-010 menggeser dinding menjadi "
            "[2, 4, 6, 8] dengan jumlah kombinasi identik dan seluruh unsur "
            "lain tidak diubah. Bila laju kena target turun lebih lambat "
            "daripada titik impas 1/(1+imbalan), ekspektasi naik; bila lebih "
            "cepat, ia turun dan dinding H-007 terbukti bukan artefak."
        ),
        dataset=DATASET,
        ruang_parameter={
            "lookback": LOOKBACK,
            "imbalan_R": IMBALAN,
            KUNCI_TERLARANG: [AMBANG_CARRY_KERAS],
            "atr_pengali_stop": [konfig.atr_pengali_stop],
            "maks_umur_bar": [konfig.maks_umur_bar],
            "maks_carry_R": [konfig.maks_carry_R],
            "jendela_carry_hari": [konfig.jendela_carry_hari],
        },
        # Tidak dilonggarkan sedikit pun dari H-002 sampai H-009. Melonggarkan
        # sekarang, setelah tahu H-009 hanya kurang 0,008641R, adalah bentuk
        # kecurangan yang paling mudah dibela dan paling merusak.
        kriteria=Kriteria(
            min_ekspektasi_R=0.05,
            min_trade_luar_sampel=100,
            maks_p_entri_acak=0.05,
            min_jendela_positif_rasio=0.5,
        ),
        komit=komit,
    )


def spek_h010(konfig: Konfig, komit: str = "") -> Spek:
    return Spek(
        h=hipotesis_h010(konfig, komit),
        sinyal=breakout_atr.sinyal,
        kandidat=kandidat(),
        nama="h010_imbalan_diperluas",
        params_lookahead={"lookback": 55},
        buat_konfig=buat_konfig,
    )


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

    # Seluruh pemeriksaan di bawah berjalan sebelum satu bar pun dimuat.
    if hipotesis_h010(konfig).dataset != hipotesis_h002(konfig).dataset:
        raise ValueError("dataset H-010 tidak identik dengan H-002")

    if konfig.maks_carry_R <= 0:
        raise ValueError("H-010 menuntut saringan ADR-004 tetap menyala")

    if LOOKBACK != list(LOOKBACK_H007):
        raise ValueError("lookback H-010 wajib identik dengan H-007")

    if IMBALAN == list(IMBALAN_H007):
        raise ValueError("grid imbalan H-010 tidak digeser; ADR-012 kosong")

    if len(IMBALAN) != len(IMBALAN_H007):
        raise ValueError(
            "jumlah kombinasi H-010 wajib identik dengan H-009 agar "
            "multiplisitasnya sebanding"
        )

    if max(IMBALAN) <= max(IMBALAN_H007):
        raise ValueError("dinding grid wajib digeser KE LUAR, bukan ke dalam")

    hilang = [j for j in JANGKAR if j not in IMBALAN]
    if hilang:
        raise ValueError(f"jangkar pembanding hilang dari grid: {hilang}")

    for p in kandidat():
        if KUNCI_TERLARANG in p:
            raise ValueError(f"{KUNCI_TERLARANG} bocor ke ruang pencarian")

    if AMBANG_CARRY_KERAS <= 0:
        raise ValueError("ambang carry keras wajib menyala di H-010")

    opsi = Opsi(
        dir_aset=Path(a.dir),
        out=Path(a.out),
        interval=a.interval,
        universe=Path(a.universe),
        akhir_sejati=Path(a.akhir_sejati),
        limit=a.limit,
        ulangan=a.ulangan,
    )

    print(f"ADR-012 grid imbalan: {IMBALAN} (H-007: {list(IMBALAN_H007)})", flush=True)
    print(f"ADR-009 ambang carry keras DIPATOK: {AMBANG_CARRY_KERAS}", flush=True)
    print(f"kandidat: {len(kandidat())} kombinasi", flush=True)
    for im in IMBALAN:
        print(f"  titik impas kotor {im}R: {titik_impas(im):.4f}", flush=True)
    for id_, (eks, gerbang) in PEMBANDING.items():
        print(f"  pembanding {id_}: {eks:+.5f}R, gerbang: {gerbang}", flush=True)
    for nama, isi in RAMALAN.items():
        print(f"  ramalan {nama}: {isi}", flush=True)

    ktx = muat_konteks(opsi)
    hasil = jalankan_spek(spek_h010(konfig, a.komit), ktx, konfig, opsi)

    keluar = hasil["alasan_keluar"]
    total = sum(keluar.values())
    tak_selesai = sum(v for k, v in keluar.items() if k in ALASAN_TIDAK_SELESAI)

    print("", flush=True)
    if total:
        laju = keluar.get("target", 0) / total
        porsi = tak_selesai / total
        print(
            f"laju kena target: {laju:.5f} (H-009 {H009_LAJU_TARGET:.5f})",
            flush=True,
        )
        # Dicetak SEBELUM ekspektasi, karena bila angka ini besar maka yang
        # diukur adalah batas umur dan bukan struktur keluar.
        print(
            f"porsi perdagangan tak selesai: {porsi:.5f} "
            f"(H-009 {H009_PORSI_TAK_SELESAI:.5f})",
            flush=True,
        )
    print(f"keluar karena pengaman carry: {keluar.get('carry', 0)}", flush=True)
    print(
        f"porsi funding ekor maks: {hasil.get('porsi_funding_ekor_maks')} "
        f"(H-009 {H009_PORSI_FUNDING_EKOR}, ambang 0,35)",
        flush=True,
    )
    print(f"retensi drop-1: {hasil.get('retensi_drop_1')}", flush=True)
    print(f"gerbang gagal: {hasil['gerbang_gagal']}", flush=True)
    print(
        f"ekspektasi {hasil['ekspektasi_R']} vs H-009 {PEMBANDING['H-009'][0]}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
