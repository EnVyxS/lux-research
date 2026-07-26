"""H-011 — apakah hasil 40 simbol pertama mewakili 438 simbol (ADR-013 bagian 8).

Seluruh hasil dari H-001b sampai H-010 berdiri di atas **40 simbol pertama
secara alfabet**. Asumsi itu belum pernah diuji sekali pun, dan sekarang ia
menopang satu-satunya hipotesis yang lulus. H-011 mengujinya.

MEKANISMENYA TIDAK BERUBAH SAMA SEKALI. Grid, sinyal, konfig per kandidat,
pengaman carry, dan kriteria diimpor apa adanya dari H-010 dan H-009. Modul ini
**menolak berjalan** bila salah satunya berbeda, karena H-011 yang mengubah
mekanisme sekaligus semesta tidak menjawab pertanyaan apa pun: kalau hasilnya
berubah, tidak akan diketahui penyebab mana yang bekerja. Yang berubah hanya
``--limit``, dari 40 menjadi 0 yang berarti seluruh semesta layak.

``--ulangan`` dinaikkan dari 100 ke 300. Itu **peningkatan resolusi, bukan
pelonggaran ambang**: ambang p tetap 0,05, tetapi resolusinya membaik dari
0,0099 ke 0,00332. Alasannya H-010 lulus dengan p 0,049505, yaitu jarak tepat
satu satuan resolusi dari kegagalan. Angka ini ditetapkan di ADR-013 sebelum
hasil H-011 terlihat.

KRITERIA UTAMA BUKAN ``putusan`` DI DALAM LAPORAN. Berkas laporan menilai
kumpulan 438 simbol sebagai satu kesatuan, dan angka itu masih memuat 40 simbol
yang sudah dipakai memilih segalanya sejak H-001b. Yang menjawab pertanyaan
adalah **ekspektasi berbobot perdagangan atas 398 simbol tertahan**, dihitung di
sini dari blok ``per_simbol`` di laporan yang sama. Perhitungannya sengaja
sesederhana penjumlahan dua kolom, supaya tidak ada kode baru yang bisa
menyelundupkan asumsi.

Ramalan tertulis, dari ADR-013: ekspektasi tertahan **turun** ke 0,020-0,045 dan
H-011 gagal. Bila ia tetap di atas 0,05 pada 398 simbol yang belum pernah
disentuh, itu bukti terkuat yang pernah dihasilkan riset ini.

Keterbatasan yang wajib ikut tercetak: ``per_simbol`` membulatkan ``total_R`` ke
empat desimal untuk dibaca manusia, jadi ekspektasi tertahan terikat galat
pembulatan orde 1e-4 R dikali jumlah simbol dibagi jumlah perdagangan —
besarannya jauh di bawah desimal yang ditafsirkan, tetapi ia ada. Galat baku
subkumpulan tertahan **tidak dapat** dihitung dari ``per_simbol`` karena sebaran
per perdagangan tidak dipecah per simbol; blok ``sebaran`` di laporan berlaku
untuk seluruh kumpulan.

Pemakaian:
    python -m lux.backtest.run_h011 --dir aset --limit 0 --ulangan 300
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

from lux.backtest.engine import Konfig
from lux.backtest.run_h002 import hipotesis_h002, muat_konfig_h002
from lux.backtest.run_h009 import buat_konfig as buat_konfig_h009
from lux.backtest.run_h009 import (
    AMBANG_CARRY_KERAS,
    DATASET,
    KUNCI_TERLARANG,
)
from lux.backtest.run_h010 import IMBALAN as IMBALAN_H010
from lux.backtest.run_h010 import LOOKBACK as LOOKBACK_H010
from lux.backtest.run_h010 import buat_konfig as buat_konfig_h010
from lux.backtest.run_h010 import kandidat as kandidat_h010
from lux.backtest.runner import Opsi, Spek, jalankan_spek, muat_konteks
from lux.praregistrasi import Hipotesis, Kriteria
from lux.strategi import breakout_atr

# Satu-satunya tempat angka 40 ditulis tangan. Ia adalah nilai ``limit`` yang
# dipakai H-001b sampai H-010, jadi ia menentukan simbol mana yang sudah
# terpakai dan karena itu tidak lagi tertahan. Pengujian yang menyalakan alarm
# bila angka ini bergeser adalah tripwire yang disengaja (aturan 18).
BATAS_H010 = 40

NAMA = "h011_semesta_penuh"

# Ukuran H-010 dari reports/backtest_h010_imbalan_diperluas.json, disalin, tidak
# dijalankan ulang.
H010 = {
    "ekspektasi_R": 0.05302836360569971,
    "total_R": 622.2348185492804,
    "trade": 11734,
    "p_entri_acak": 0.04950495049504951,
    "retensi_drop_1": 0.8578454756024698,
    "simbol": 40,
}

# Ditulis di ADR-013 sebelum run. Ramalan pertama merugikan hipotesis ini
# sendiri: saya meramalkan H-011 gagal.
RAMALAN = {
    "ekspektasi_tertahan_R": (
        "0,020-0,045, jadi TURUN di bawah ambang 0,05 dan H-011 gagal"
    ),
    "tafsir_batas": (
        "di atas 0,05 pada 398 simbol asing adalah bukti terkuat yang pernah "
        "dihasilkan riset ini; di bawah 0,020 berarti hasil 40 simbol adalah "
        "derau seleksi dan H-010 wajib diperlakukan sebagai kebetulan"
    ),
    "p_entri_acak": (
        "0,01-0,15; p di atas 0,05 menjatuhkan H-011 MESKIPUN ekspektasinya "
        "tinggi"
    ),
    "jumlah_trade": "100.000-160.000 (penskalaan 11.734 x 438/40 = 128.487)",
    "retensi_drop_1": "minimal 0,95; dengan 438 simbol satu simbol tak boleh berarti",
    "durasi": (
        "15-60 menit; melewati batas 330 menit adalah timeout dan itu "
        "informasi, bukan alasan memperkecil semesta"
    ),
    "porsi_funding_ekor_maks": "0,10-0,30, tetap di bawah ambang 0,35",
}


def simbol_teruji(universe: str | Path, batas: int = BATAS_H010) -> list[str]:
    """Simbol yang sudah dipakai H-001b sampai H-010.

    Diambil dengan aturan yang sama persis dengan runner, yaitu ``sorted(...)``
    lalu dipotong di ``limit``. Daftarnya tidak pernah diketik tangan: menulis
    40 nama simbol di berkas ini akan menjadi salinan kedua dari sesuatu yang
    sudah diketahui berkas universe, dan salinan kedua adalah tempat kekeliruan
    berikutnya bersembunyi.
    """
    semesta = json.loads(Path(universe).read_text(encoding="utf-8"))["simbol"]
    return sorted(semesta)[:batas]


def agregat(baris: Iterable[dict]) -> dict:
    """Ekspektasi berbobot perdagangan atas sekumpulan baris ``per_simbol``.

    Berbobot perdagangan, bukan rerata dari rerata per simbol. Rerata dari
    rerata memberi simbol dengan 32 perdagangan bobot yang sama dengan simbol
    berisi 737 perdagangan, dan pencilan seperti AIOTUSDT (+1,798R atas 32
    perdagangan) akan mendominasi angka yang seharusnya menggambarkan seluruh
    semesta.
    """
    baris = list(baris)
    trade = sum(int(r["trade"]) for r in baris)
    total = float(sum(float(r["total_R"]) for r in baris))
    return {
        "n_simbol": len(baris),
        "trade": trade,
        "total_R": total,
        "ekspektasi_R": (total / trade) if trade else None,
        "dapat_dinilai": trade > 0,
        "sebab": "" if trade else "tidak ada perdagangan",
    }


def pisah_tertahan(per_simbol: Iterable[dict], teruji: Iterable[str]) -> dict:
    """Memisahkan simbol tertahan dari simbol yang sudah terpakai."""
    sudah = set(teruji)
    baris = list(per_simbol)
    return {
        "tertahan": agregat(r for r in baris if r["symbol"] not in sudah),
        "teruji": agregat(r for r in baris if r["symbol"] in sudah),
    }


def hipotesis_h011(konfig: Konfig, komit: str = "") -> Hipotesis:
    return Hipotesis(
        id="H-011",
        pernyataan=(
            "H-010 lulus dengan ekspektasi 0,053028R, tetapi seluruh hasil "
            "sejak H-001b diukur pada 40 simbol pertama secara alfabet, yaitu "
            "kurang dari sepersepuluh semesta layak. H-011 menjalankan "
            "mekanisme H-010 tanpa satu perubahan pun atas seluruh 438 simbol "
            "dan dinilai pada 398 simbol yang belum pernah disentuh. Bila "
            "ekspektasi tertahan bertahan di atas 0,05R, keunggulan itu bukan "
            "sifat dari 40 simbol tertentu; bila ia jatuh, hasil H-010 adalah "
            "derau seleksi dan bukan temuan."
        ),
        dataset=DATASET,
        ruang_parameter={
            "lookback": list(LOOKBACK_H010),
            "imbalan_R": list(IMBALAN_H010),
            KUNCI_TERLARANG: [AMBANG_CARRY_KERAS],
            "semesta": ["seluruh universe_layak_v2"],
            "atr_pengali_stop": [konfig.atr_pengali_stop],
            "maks_umur_bar": [konfig.maks_umur_bar],
            "maks_carry_R": [konfig.maks_carry_R],
            "jendela_carry_hari": [konfig.jendela_carry_hari],
        },
        # Tidak dilonggarkan, dan tidak pula DIPERKETAT setelah H-010 lulus.
        # Keduanya sama-sama menyetel ambang terhadap hasil.
        kriteria=Kriteria(
            min_ekspektasi_R=0.05,
            min_trade_luar_sampel=100,
            maks_p_entri_acak=0.05,
            min_jendela_positif_rasio=0.5,
        ),
        komit=komit,
    )


def spek_h011(konfig: Konfig, komit: str = "") -> Spek:
    return Spek(
        h=hipotesis_h011(konfig, komit),
        sinyal=breakout_atr.sinyal,
        kandidat=kandidat_h010(),
        nama=NAMA,
        params_lookahead={"lookback": 55},
        buat_konfig=buat_konfig_h010,
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--interval", default="1h")
    ap.add_argument("--universe", default="reports/universe_layak_v2.json")
    ap.add_argument("--akhir-sejati", default="reports/akhir_sejati.json")
    ap.add_argument("--config", default="config/lux.yaml")
    ap.add_argument("--out", default="reports")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--ulangan", type=int, default=300)
    ap.add_argument("--komit", default="")
    a = ap.parse_args(argv)

    # Seluruh pemeriksaan di bawah selesai dalam hitungan detik, sebelum satu
    # bar pun dimuat. Menaruhnya di ujung run 438 simbol berarti membuang
    # puluhan menit komputasi untuk mengetahui hal yang sudah bisa diketahui
    # sekarang.
    if 0 < a.limit <= BATAS_H010:
        raise ValueError(
            f"limit {a.limit} tidak menyisakan simbol tertahan di luar "
            f"{BATAS_H010} simbol yang sudah dipakai H-001b sampai H-010; "
            "H-011 tidak menjawab apa pun tanpa simbol asing"
        )

    if a.ulangan < 100:
        raise ValueError(
            "ulangan H-011 tidak boleh di bawah 100; resolusi p adalah alasan "
            "hipotesis ini ada"
        )

    konfig = muat_konfig_h002(Path(a.config))

    if hipotesis_h011(konfig).dataset != hipotesis_h002(konfig).dataset:
        raise ValueError("dataset H-011 tidak identik dengan H-002")

    if konfig.maks_carry_R <= 0:
        raise ValueError("H-011 menuntut saringan ADR-004 tetap menyala")

    if AMBANG_CARRY_KERAS <= 0:
        raise ValueError("ambang carry keras wajib menyala di H-011")

    # Inti H-011: mekanismenya WAJIB identik dengan H-010. Bila grid ikut
    # berubah, perubahan hasil tidak dapat dipisahkan dari perubahan semesta.
    if list(LOOKBACK_H010) != [20, 55, 100]:
        raise ValueError("lookback H-010 bergeser; H-011 kehilangan pembanding")

    if kandidat_h010() != [
        {"lookback": lb, "imbalan_R": im}
        for lb in LOOKBACK_H010
        for im in IMBALAN_H010
    ]:
        raise ValueError("kandidat H-011 tidak identik dengan H-010")

    if buat_konfig_h010 is not buat_konfig_h009:
        raise ValueError(
            "buat_konfig H-010 bukan lagi fungsi H-009; pematokan pengaman "
            "carry tidak lagi dijalankan kode yang sama"
        )

    for p in kandidat_h010():
        if KUNCI_TERLARANG in p:
            raise ValueError(f"{KUNCI_TERLARANG} bocor ke ruang pencarian")

    opsi = Opsi(
        dir_aset=Path(a.dir),
        out=Path(a.out),
        interval=a.interval,
        universe=Path(a.universe),
        akhir_sejati=Path(a.akhir_sejati),
        limit=a.limit,
        ulangan=a.ulangan,
    )

    teruji = simbol_teruji(a.universe)
    print(
        f"H-011 semesta penuh: limit {a.limit}, ulangan {a.ulangan} "
        f"(H-010: limit {BATAS_H010}, ulangan 100)",
        flush=True,
    )
    print(f"grid identik H-010: lookback {list(LOOKBACK_H010)}, "
          f"imbalan {list(IMBALAN_H010)}, {len(kandidat_h010())} kombinasi",
          flush=True)
    print(f"simbol sudah terpakai: {len(teruji)} "
          f"({teruji[0]} .. {teruji[-1]})", flush=True)
    for nama, isi in RAMALAN.items():
        print(f"  ramalan {nama}: {isi}", flush=True)

    ktx = muat_konteks(opsi)
    hasil = jalankan_spek(spek_h011(konfig, a.komit), ktx, konfig, opsi)

    # Kriteria utama dihitung dari laporan yang baru ditulis, bukan dari nilai
    # yang beredar di memori, supaya angka yang diadjudikasi adalah angka yang
    # benar-benar dikomit ke repo.
    laporan = json.loads(
        (Path(a.out) / f"backtest_{NAMA}.json").read_text(encoding="utf-8")
    )
    pisah = pisah_tertahan(laporan["per_simbol"], teruji)
    tertahan, lama = pisah["tertahan"], pisah["teruji"]

    print("", flush=True)
    print("=== KRITERIA UTAMA ADR-013: SIMBOL TERTAHAN ===", flush=True)
    print(
        f"tertahan: {tertahan['n_simbol']} simbol, {tertahan['trade']:,} trade, "
        f"total {tertahan['total_R']:.2f}R, ekspektasi {tertahan['ekspektasi_R']}",
        flush=True,
    )
    print(
        f"sudah terpakai: {lama['n_simbol']} simbol, {lama['trade']:,} trade, "
        f"total {lama['total_R']:.2f}R, ekspektasi {lama['ekspektasi_R']}",
        flush=True,
    )
    if tertahan["dapat_dinilai"] and lama["dapat_dinilai"]:
        print(
            f"selisih tertahan - terpakai: "
            f"{tertahan['ekspektasi_R'] - lama['ekspektasi_R']:+.6f}R",
            flush=True,
        )
    if tertahan["dapat_dinilai"]:
        ambang = hipotesis_h011(konfig).kriteria.min_ekspektasi_R
        lulus_utama = tertahan["ekspektasi_R"] >= ambang
        print(
            f"kriteria utama terhadap {ambang}R: "
            f"{'LULUS' if lulus_utama else 'GAGAL'} "
            f"(ramalan saya: GAGAL, 0,020-0,045)",
            flush=True,
        )
    print(
        "catatan: total_R di per_simbol dibulatkan empat desimal, jadi "
        "ekspektasi tertahan terikat galat pembulatan orde 1e-4 R per simbol; "
        "galat baku subkumpulan ini TIDAK dapat dihitung dari per_simbol",
        flush=True,
    )

    print("", flush=True)
    print(f"putusan seluruh kumpulan: {hasil['lulus']}", flush=True)
    print(f"ekspektasi seluruh kumpulan: {hasil['ekspektasi_R']} "
          f"(H-010 {H010['ekspektasi_R']})", flush=True)
    print(f"trade: {hasil['trade']:,} (H-010 {H010['trade']:,})", flush=True)
    print(f"p entri acak: {hasil['p_entri_acak']} "
          f"(H-010 {H010['p_entri_acak']})", flush=True)
    print(f"retensi drop-1: {hasil.get('retensi_drop_1')} "
          f"(H-010 {H010['retensi_drop_1']})", flush=True)
    print(f"galat baku: {hasil.get('galat_baku_R')}", flush=True)
    print(f"jarak ke ambang dalam galat baku: {hasil.get('jarak_galat_baku')}",
          flush=True)
    print(f"porsi funding ekor maks: {hasil.get('porsi_funding_ekor_maks')}",
          flush=True)
    print(f"gerbang gagal: {hasil['gerbang_gagal']}", flush=True)
    print(f"durasi: {hasil['detik']}s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
