"""H-014 — geometri keluar sendirian, dengan umur pegangan DISETARAKAN (ADR-033, ADR-034).

H-013 mengukur ``SS − SH`` dan menamainya "sumbangan geometri keluar"
(+0,029481R). Nama itu **salah**, dan sebabnya baru terlihat sesudah
``run_h013.umur_sel`` dibaca: sel bertarget memakai ``UMUR_SEL_STOP`` = 42 bar
sedangkan sel tanpa target memakai ``H_BAR`` = 48. Jadi selisih itu mencampur
**dua** medan — ada-tidaknya target **dan** batas umur 42 lawan 48 — dan
``maks_umur_bar`` bukan medan pasif: ``engine._boleh_masuk`` memakainya untuk
proyeksi carry (``umur_ms = k.maks_umur_bar * interval_ms``), sehingga 42 dan 48
**menolak entri yang berbeda**. Itulah sebab terukur pertama dari 60.018 lawan
44.614 perdagangan. Cacat kelas keempat belas, dan aturan 52 lahir darinya.

Modul ini menjalankan perbandingan yang namanya jujur: **satu** medan berbeda.

    SS′  pakai_target=True   maks_umur_bar=48
    SH′  pakai_target=False  maks_umur_bar=48

EMPAT BAHAYA YANG DITEMUKAN DENGAN MEMBACA SUMBER, BUKAN DENGAN MENUNGGU RUN GAGAL
---------------------------------------------------------------------------------
**1. Hipotesis H-014 wajib milik sendiri, dan id-nya per sel.**
``runner.jalankan_spek`` memanggil ``praregistrasi.simpan(spek.h,
f"hipotesis/{spek.h.id}.json")``. Memakai ``run_h013.hipotesis_h013`` akan
menulis ke ``hipotesis/H-013*.json`` — berkas pra-registrasi yang **sudah
dikomit**. Dan karena ``simpan`` menolak id yang sama dengan isi berbeda ("buat
id baru alih-alih menyunting yang lama"), dua sel tidak boleh berbagi satu id:
keduanya memakai ``H-014-SSp`` dan ``H-014-SHp``.

**2. Nama laporan sel wajib unik.** ``jalankan_spek`` menulis
``backtest_<spek.nama>.json`` — nama yang sama setiap pemanggilan. Pagar yang
menyelamatkan Jalur B dipasang ulang di sini, dan sebuah pengujian menuntut
nama H-014 berbeda dari keempat ``NAMA_LAPORAN`` H-013 maupun dari
``run_h013b.NAMA_SPEK``.

**3. ``buat_konfig`` sengaja TIDAK dipakai.** ADR-033 §7 melarang melombakan
``maks_umur_bar`` dan ``pakai_target``, dan ``Spek.buat_konfig`` adalah satu-
satunya pintu yang memungkinkannya. Geometri karena itu dipasang **sekali** di
Konfig dasar tiap sel, dan laporan akan mencatat ``konfig_per_kandidat: false``.

**4. Berkas md tiap sel akan tetap mencetak LULUS atau DITOLAK, dan itu BUKAN
putusan H-014.** Angka itu adalah putusan ``praregistrasi.nilai`` terhadap
kriteria **per sel** (ekspektasi ≥ 0,05R, ≥ 100 trade, p entri acak ≤ 0,05,
rasio jendela positif ≥ 0,5). Laporan H-013 mencetak ``**LULUS**`` dengan cara
yang sama sementara kriteria utama ADR-015 §4.4 belum pernah dihitung. Manifes
run ini menyatakannya, dan adjudikasinya berdiri di modul lain
(``gabung_h014``) yang **tidak punya cabang LULUS sama sekali**.

AMBANG: BARU, DIBEKUKAN HARI INI (ADR-034, aturan 53)
-----------------------------------------------------
ADR-015 §4.4 membekukan ambang untuk kaki **sinyal** (``SS − AS``, p atas
permutasi **sinyal**). Untuk kaki **geometri** ADR-015 tidak pernah membekukan
ambang, definisi p, maupun nol. Mengutipnya sebagai pra-registrasi kaki ini
adalah cacat kelas kelima belas. Karena itu ambang H-014 dinyatakan **baru,
dibekukan 2026-07-27**, dan 0,020R dipinjam **dengan sadar** justru supaya tidak
ada ambang yang dipilih agar mudah dilewati.

H-014 MUSTAHIL LULUS, DAN ITU DINYATAKAN SEBELUM ANGKANYA ADA
-------------------------------------------------------------
Signifikansinya diadjudikasi ``lux.analisis.berpasangan`` pada satuan bulan
kalender UTC (ADR-028). Modul itu menyatakan sendiri bahwa p-nya mengukur
ketidakpastian penarikan bulan dan **bukan** sebaran permutasi sinyal, sehingga
ia sah untuk **menjatuhkan** dan tidak sah untuk **menegakkan**; ia memancarkan
``memenuhi_adr015: False`` tanpa syarat. Maka H-014 hanya punya dua keluaran:
**DITOLAK** atau **TIDAK DAPAT DINILAI**.

Pemakaian:
    python -m lux.backtest.run_h014 --dir aset --interval 4h \\
        --universe reports/universe_layak_v2_4h.json \\
        --akhir-sejati reports/akhir_sejati_4h.json \\
        --min-median-stop-frac 0.004
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, replace
from pathlib import Path

import numpy as np
import pandas as pd

from lux.backtest.engine import Konfig
from lux.backtest.run_h002 import muat_konfig_h002
from lux.backtest.run_h012 import kunci_config
from lux.backtest.run_h013 import (
    DATASET,
    H_BAR,
    IMBALAN_BEKU,
    LOOKBACK,
    MIN_TRADE_SEL,
    MIN_ULANGAN,
    NAMA_LAPORAN,
    PEMANASAN,
    UMUR_SEL_STOP,
    bar_dibutuhkan,
    dasar_riset,
    jendela_bar,
    kandidat,
)
from lux.backtest.runner import Opsi, Spek, jalankan_spek, muat_konteks
from lux.praregistrasi import Hipotesis
from lux.strategi import breakout_atr

NAMA = "h014"

# Dua sel, dan hanya dua. Tanda kutip tunggal pada nama (SS′/SH′) ditulis "p"
# di kode supaya nama berkas tetap ASCII.
NAMA_SEL = ("SSp", "SHp")

# Nama laporan sel. SENGAJA berbeda dari seluruh NAMA_LAPORAN H-013 dan dari
# run_h013b.NAMA_SPEK; sebuah pengujian menuntut perbedaan itu, sebab
# jalankan_spek menulis backtest_<nama>.json dengan nama yang sama tiap
# pemanggilan dan akan menimpa laporan yang sudah dikomit tanpa satu pesan galat.
NAMA_LAPORAN_H014 = {
    "SSp": "h014_ssp_target_umur48",
    "SHp": "h014_shp_tanpa_target_umur48",
}

# Umur pegangan disetarakan. Inilah seluruh isi H-014: bukan angka baru, tetapi
# angka yang SAMA di kedua sel.
UMUR_SETARA = H_BAR

# Ambang. BARU, dibekukan hari ini (ADR-034, aturan 53).
AMBANG_BESARAN_R = 0.020
AMBANG_P = 0.05
CATATAN_AMBANG = (
    "Ambang H-014 adalah ambang BARU yang dibekukan 2026-07-27, bukan kutipan "
    "ADR-015 pasal 4.4. Pasal itu membekukan ambang untuk kaki SINYAL (SS-AS, p "
    "atas permutasi sinyal); untuk kaki GEOMETRI, ADR-015 tidak pernah "
    "membekukan ambang, definisi p, maupun nol. Angka 0,020R dipinjam DENGAN "
    "SADAR dari pasal 4.4 supaya tidak ada ambang yang dipilih agar mudah "
    "dilewati."
)

# Putusan yang mungkin. Tidak ada LULUS, dan itu dinyatakan sebelum satu angka
# pun ada (ADR-034 pasal 2).
PUTUSAN_MUNGKIN = ("DITOLAK", "TIDAK DAPAT DINILAI")

SAMPEL_PERMUTASI = 10

PEMBATAS = (
    "H-014 MUSTAHIL LULUS, dan itu dipra-registrasi sebelum angkanya ada: "
    "putusannya hanya DITOLAK atau TIDAK DAPAT DINILAI. Signifikansinya "
    "diadjudikasi lux.analisis.berpasangan pada satuan BULAN kalender UTC, dan "
    "modul itu menyatakan sendiri bahwa p-nya mengukur ketidakpastian penarikan "
    "bulan, BUKAN sebaran permutasi sinyal; ia sah untuk MENJATUHKAN dan tidak "
    "sah untuk MENEGAKKAN. Berkas md tiap sel akan tetap mencetak LULUS atau "
    "DITOLAK milik pra-registrasi PER SEL dari runner; itu BUKAN putusan H-014. "
    "SS' dan SH' di sini BUKAN sel SS dan SH run 30214203863: kedua sel di sana "
    "berbeda pada DUA medan (target dan umur 42 lawan 48), sehingga +0,029481R "
    "tidak boleh dipakai sebagai pembanding maupun sebagai 'versi sebelum "
    "perbaikan'."
)


def pakai_target_h014(sel: str) -> bool:
    """Satu-satunya medan yang berbeda antar sel."""
    if sel not in NAMA_SEL:
        raise ValueError(f"sel {sel!r} bukan salah satu dari {NAMA_SEL}")
    return sel == "SSp"


def umur_sel_h014(sel: str) -> int:
    """Umur pegangan, SAMA di kedua sel. Inilah perbaikan atas cacat 14.

    Fungsinya tetap menerima ``sel`` supaya ia dapat diuji simetris dan supaya
    ketidakbergantungannya pada sel terlihat dari tanda tangannya, bukan hanya
    dari tubuhnya.
    """
    if sel not in NAMA_SEL:
        raise ValueError(f"sel {sel!r} bukan salah satu dari {NAMA_SEL}")
    return int(UMUR_SETARA)


def konfig_sel_h014(sel: str, dasar: Konfig) -> Konfig:
    """Konfig sel: umur disetarakan, target dinyalakan atau dimatikan.

    ``Konfig.__post_init__`` menolak ``pakai_target=False`` dengan
    ``maks_umur_bar <= 0``; syarat itu terpenuhi karena umurnya 48 di kedua sel.
    """
    return replace(
        dasar,
        pakai_target=pakai_target_h014(sel),
        maks_umur_bar=umur_sel_h014(sel),
        imbalan_R=IMBALAN_BEKU,
    )


def medan_berbeda(dasar: Konfig) -> list[str]:
    """Medan Konfig yang berbeda antar kedua sel. Aturan 52 dinilai di sini.

    Dikembalikan sebagai daftar dan bukan sebagai boolean supaya laporan dapat
    **menyebut** medannya, sebagaimana aturan 52 menuntut.
    """
        # noqa: E501 tidak perlu; baris di bawah pendek.
    a = asdict(konfig_sel_h014("SSp", dasar))
    b = asdict(konfig_sel_h014("SHp", dasar))
    return sorted(k for k in a if a[k] != b[k])


def sinyal_nyata(df: pd.DataFrame, params: dict) -> np.ndarray:
    """Donchian yang sama seperti seluruh keluarga, tanpa pengacakan apa pun.

    Kedua sel H-014 memakai sinyal sungguhan, dan itu perbaikan yang terukur
    atas Jalur B: ``gerbang_lookahead`` dan ``gerbang_entri_acak`` **dapat
    dinilai** di keduanya, sedangkan pada sel AS/AH keduanya gagal karena
    konstruksi (ADR-021).
    """
    return breakout_atr.sinyal(df, params)


def pernyataan_sel(sel: str) -> str:
    if pakai_target_h014(sel):
        return (
            "Sel SS' — breakout Donchian dengan stop ATR DAN target imbalan "
            f"{IMBALAN_BEKU}R, batas umur {UMUR_SETARA} bar 4h. Sel pembanding "
            "bagi SH'; keduanya berbeda HANYA pada ada-tidaknya target."
        )
    return (
        "Sel SH' — breakout Donchian dengan stop ATR TANPA target, batas umur "
        f"{UMUR_SETARA} bar 4h, yakni umur yang SAMA dengan sel SS'. Selisih "
        "keduanya karena itu mengukur ada-tidaknya target dan bukan panjang "
        "pegangan."
    )


def hipotesis_h014(sel: str, konfig: Konfig, komit: str = "") -> Hipotesis:
    """Hipotesis per sel, dengan id sendiri.

    Id per sel bukan kerapian: ``praregistrasi.simpan`` menolak id yang sama
    dengan isi berbeda, dan pernyataan kedua sel memang berbeda. Prefiks
    ``H-014-`` juga menjauhkannya dari ``hipotesis/H-013*.json`` yang sudah
    dikomit dan tidak boleh tertimpa.

    ``Kriteria`` dibiarkan pada nilai bawaannya — 0,05R, 100 trade, p 0,05,
    rasio jendela positif 0,5 — dan sebuah pengujian menuntutnya. Melonggarkan
    kriteria per sel akan membuat berkas md sel mencetak LULUS lebih mudah, dan
    berkas itulah yang paling mungkin dibaca orang tanpa membaca adjudikasinya.
    """
    k = konfig_sel_h014(sel, konfig)
    return Hipotesis(
        id=f"H-014-{sel}",
        pernyataan=pernyataan_sel(sel),
        dataset=DATASET,
        ruang_parameter={
            "lookback": list(LOOKBACK),
            "pakai_target": [k.pakai_target],
            "maks_umur_bar": [k.maks_umur_bar],
            "imbalan_R": [k.imbalan_R],
        },
        komit=komit,
    )


def spek_h014(sel: str, konfig: Konfig, komit: str = "") -> Spek:
    """Spek satu sel. ``buat_konfig`` sengaja ``None`` (ADR-033 pasal 7)."""
    return Spek(
        h=hipotesis_h014(sel, konfig, komit),
        sinyal=sinyal_nyata,
        kandidat=kandidat(),
        nama=NAMA_LAPORAN_H014[sel],
        params_lookahead={"lookback": 55},
        buat_konfig=None,
    )


def opsi_h014(a, jen: dict) -> Opsi:
    """Opsi run. Berbeda dari Jalur B: ``sampel_permutasi`` MENYALA.

    Di Jalur B gerbang ``entri_acak`` dimatikan karena 300 permutasi bersarang
    di dalam 300 seed adalah pemborosan atas angka yang tidak dipakai. Di sini
    kedua sel memakai sinyal sungguhan dan gerbang itu **berarti**, jadi ia
    dinyalakan pada ambang ulangan yang tidak diturunkan.
    """
    return Opsi(
        dir_aset=Path(a.dir),
        out=Path(a.out),
        interval=a.interval,
        universe=Path(a.universe),
        akhir_sejati=Path(a.akhir_sejati),
        limit=a.limit,
        panjang_latih=jen["panjang_latih"],
        panjang_uji=jen["panjang_uji"],
        embargo=jen["embargo"],
        pemanasan=PEMANASAN,
        ulangan=MIN_ULANGAN,
        sampel_permutasi=SAMPEL_PERMUTASI,
        min_median_stop_frac=a.min_median_stop_frac,
    )


def jalur_manifes(out: Path | str = "reports") -> Path:
    return Path(out) / "h014_run.json"


def jalur_sel(sel: str, out: Path | str = "reports") -> Path:
    return Path(out) / f"backtest_{NAMA_LAPORAN_H014[sel]}.json"


def periksa_nama() -> bool:
    """Tuntut nama laporan H-014 tidak menimpa apa pun yang sudah dikomit."""
    from lux.backtest.run_h013b import NAMA_SPEK as NAMA_SPEK_B

    dipakai = set(NAMA_LAPORAN.values()) | {NAMA_SPEK_B}
    tumpang = sorted(set(NAMA_LAPORAN_H014.values()) & dipakai)
    if tumpang:
        raise ValueError(
            f"nama laporan H-014 {tumpang} bertumpang dengan laporan yang sudah "
            "dikomit; jalankan_spek akan menimpanya tanpa satu pesan galat"
        )
    return True


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--interval", default="4h")
    ap.add_argument("--universe", default="reports/universe_layak_v2_4h.json")
    ap.add_argument("--akhir-sejati", default="reports/akhir_sejati_4h.json")
    ap.add_argument("--config", default="config/lux.yaml")
    ap.add_argument("--out", default="reports")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--min-median-stop-frac", type=float, required=True)
    ap.add_argument("--komit", default="")
    a = ap.parse_args(argv)

    # Seluruh pagar berjalan sebelum satu bar pun dimuat.
    if a.interval != "4h":
        print(
            f"DITOLAK: H-014 hanya sah pada kerangka 4h, diberi {a.interval!r}.",
            flush=True,
        )
        return 2
    for nama_arg, jalur in (
        ("universe", a.universe),
        ("akhir-sejati", a.akhir_sejati),
    ):
        if "4h" not in Path(jalur).name:
            print(f"DITOLAK: {nama_arg} {jalur!r} tidak menyebut 4h.", flush=True)
            return 2
    if a.min_median_stop_frac <= 0:
        print(
            "DITOLAK: lantai median stop_frac wajib menyala, sama seperti run "
            "yang menghasilkan seluruh sel H-013.",
            flush=True,
        )
        return 2

    periksa_nama()

    dasar = dasar_riset(muat_konfig_h002(Path(a.config)))
    kunci = kunci_config(Path(a.config))
    if kunci["min_median_stop_frac"] != a.min_median_stop_frac:
        raise ValueError(
            f"lantai pemanggil {a.min_median_stop_frac} berselisih dengan config "
            f"{kunci['min_median_stop_frac']}"
        )
    if not dasar.stop_hormati_celah or dasar.maks_biaya_masuk_R <= 0:
        raise ValueError("dua pengaman dasar_riset tidak terpasang")

    beda = medan_berbeda(dasar)
    if beda != ["pakai_target"]:
        raise ValueError(
            f"kedua sel berbeda pada {beda}; aturan 52 menuntut TEPAT satu "
            "medan, dan selisih dua medan bukan pengukuran"
        )

    jen = jendela_bar(a.interval)
    opsi = opsi_h014(a, jen)

    print(f"H-014: dua sel {NAMA_SEL}, satu medan berbeda: {beda}", flush=True)
    print(
        f"umur pegangan DISETARAKAN {UMUR_SETARA} bar di KEDUA sel; "
        f"H-013 memakai {UMUR_SEL_STOP} lawan {H_BAR} dan karena itu "
        "+0,029481R mencampur dua medan (cacat kelas keempat belas)",
        flush=True,
    )
    print(f"AMBANG: {CATATAN_AMBANG}", flush=True)
    print(f"PUTUSAN YANG MUNGKIN: {PUTUSAN_MUNGKIN}", flush=True)
    print(f"PEMBATAS: {PEMBATAS}", flush=True)
    print(f"bar dibutuhkan satu jendela: {bar_dibutuhkan(a.interval)}", flush=True)

    ktx = muat_konteks(opsi, konfig_sel_h014("SSp", dasar))

    ringkas: dict[str, dict] = {}
    for sel in NAMA_SEL:
        konfig = konfig_sel_h014(sel, dasar)
        print(
            f"\n--- sel {sel}: pakai_target {konfig.pakai_target}, "
            f"maks_umur_bar {konfig.maks_umur_bar} ---",
            flush=True,
        )
        hasil = jalankan_spek(spek_h014(sel, dasar, a.komit), ktx, konfig, opsi)
        ringkas[sel] = hasil
        print(
            f"sel {sel}: ekspektasi {hasil['ekspektasi_R']!r}, "
            f"{hasil['trade']} trade, {hasil['bulan_dengan_trade']} bulan, "
            f"gerbang gagal {hasil['gerbang_gagal']}, {hasil.get('detik')} s",
            flush=True,
        )

    kurang = [s for s in NAMA_SEL if int(ringkas[s]["trade"]) < MIN_TRADE_SEL]
    manifes = {
        "hipotesis": "H-014",
        "sel": list(NAMA_SEL),
        "nama_laporan": NAMA_LAPORAN_H014,
        "medan_berbeda": beda,
        "putusan_mungkin": list(PUTUSAN_MUNGKIN),
        "satuan_penarikan": "bulan",
        "ambang": {
            "besaran_R": AMBANG_BESARAN_R,
            "p": AMBANG_P,
            "min_trade_sel": MIN_TRADE_SEL,
            "catatan": CATATAN_AMBANG,
        },
        "sel_di_bawah_min_trade": kurang,
        "parameter_beku": {
            "maks_umur_bar": int(UMUR_SETARA),
            "imbalan_R": IMBALAN_BEKU,
            "lookback": list(LOOKBACK),
            "jendela_bar": jen,
            "pemanasan_bar": PEMANASAN,
            "ulangan_permutasi": MIN_ULANGAN,
            "sampel_permutasi": SAMPEL_PERMUTASI,
            "min_median_stop_frac": a.min_median_stop_frac,
            "maks_biaya_masuk_R": dasar.maks_biaya_masuk_R,
            "stop_hormati_celah": dasar.stop_hormati_celah,
            "konfig_per_kandidat": False,
        },
        "ringkasan_sel": ringkas,
        "pembatas": PEMBATAS,
    }
    Path(a.out).mkdir(parents=True, exist_ok=True)
    jalur_manifes(a.out).write_text(
        json.dumps(manifes, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nmanifes ditulis: {jalur_manifes(a.out)}", flush=True)
    print(
        "PUTUSAN H-014 BELUM ADA. Ia lahir dari python -m "
        "lux.backtest.gabung_h014, dan berkas md tiap sel yang mencetak LULUS "
        "atau DITOLAK hanya menyatakan pra-registrasi PER SEL milik runner.",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
