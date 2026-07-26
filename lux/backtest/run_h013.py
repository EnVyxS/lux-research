"""H-013 — memisahkan sumbangan sinyal dari sumbangan geometri keluar.

Sepuluh hipotesis pertama menaikkan atau menurunkan ekspektasi dengan menyentuh
geometri keluar: imbalan, batas umur, pengaman carry, dinding grid. Sepanjang itu
satu pertanyaan tidak pernah ditanyakan sekali pun, padahal ia pertanyaan yang
paling menentukan apakah riset ini punya isi: **apakah sinyalnya sendiri
menyumbang sesuatu?**

Satu angka membuat pertanyaan itu tidak dapat ditunda lagi. Skor entri acak
H-010 dan H-012 **identik sampai lima desimal, 0,04661R**, sementara ekspektasi
sinyal sungguhan bergerak di sekitar 0,041–0,060R. Dua hipotesis dengan geometri
berbeda menghasilkan pembanding acak yang sama, dan sinyal sungguhan tidak
terpisah jauh darinya. Itu bukan bukti bahwa sinyal tidak berguna — tetapi ia
membuat kemungkinan itu menjadi kemungkinan yang paling sederhana.

Rancangannya faktorial 2x2 (ADR-015 bagian B), dan yang dibandingkan adalah
**selisih antar sel**, bukan kelulusan satu sel:

| Sel | Sinyal | Geometri keluar |
|---|---|---|
| SS | Donchian sungguhan | stop + target |
| SH | Donchian sungguhan | horizon tetap `h`, tanpa target |
| AS | permutasi Donchian | stop + target |
| AH | permutasi Donchian | horizon tetap `h`, tanpa target |

- **Sumbangan sinyal = SS − AS.** Inilah kriteria utama, ambang **0,020R**.
- **Sumbangan geometri = SS − SH.**
- **Interaksi = (SS − AS) − (SH − AH).**

LIMA HAL YANG WAJIB DIKETAHUI SEBELUM MEMBACA HASILNYA
------------------------------------------------------
**1. Tripwire dataset DIBALIK di sini.** ``run_h010`` dan ``run_h012`` menuntut
dataset identik dengan H-002. Modul ini menuntut yang sebaliknya: dataset wajib
**berbeda** dan wajib menyebut ``4h``. H-013 berjalan pada kerangka 4h dengan
semesta berlantai, jadi menuntut kesamaan berarti memaku identitas dataset yang
salah. Ini juga sebab teknis mengapa **menyebut H-013 sebagai "H-010 setelah
perbaikan" dilarang**: interval, semesta, dan grid ketiganya berbeda.

**2. ``maks_umur_bar`` tidak diambil dari config.** ``config/lux.yaml`` memuat 168,
yang benar untuk 1h dan berarti **28 hari** pada 4h. Sel stop-target memakai
``bar_dari_hari(7, "4h")`` = **42**, sel horizon memakai **48** dari ADR-015.
Tanpa itu, SS − SH akan mengukur panjang pegangan alih-alih ada-tidaknya target.

**3. Jendela walk-forward juga satuan waktu (ADR-023).** ``panjang_latih``,
``panjang_uji``, dan ``embargo`` diturunkan dari 180, 90, dan 7 hari lewat
``lux.kerangka``. Memakai bawaan 1h apa adanya menuntut 6.848 bar 4h — sekitar 3,1
tahun — sehingga hampir tidak ada simbol yang menghasilkan satu jendela pun, dan
kegagalannya **sunyi**: laporan tetap terbentuk dan hanya berbunyi "tidak dapat
dinilai". ``pemanasan`` sengaja **tidak** dikonversi; ia kebutuhan bar milik
indikator, bukan satuan waktu.

**4. ``imbalan_R`` dibekukan 2.0 di keempat sel (ADR-022).** Pada sel tanpa target
ia tidak berpengaruh, sehingga melombakannya berarti memberi sel bertarget dua
belas kesempatan memilih melawan tiga — keuntungan gratis yang arahnya persis
mendukung kesimpulan yang paling menyenangkan.

**5. ``lookahead`` dan ``entri_acak`` DIJAMIN gagal pada sel AS dan AH (ADR-021).**
Permutasi bergantung panjang array, sedangkan gerbang lookahead memotong data lalu
menuntut sinyal awal tidak berubah. Menurut aturan 36 itu konsekuensi konstruksi,
bukan ramalan, dan haram dilaporkan sebagai temuan. Sebelas gerbang tetap dinilai
dan ditulis pada keempat sel; kelulusannya hanya menjadi syarat pada sel SS.

Pemakaian:
    python -m lux.backtest.run_h013 --dir aset --interval 4h \\
        --universe reports/universe_layak_v2_4h.json \\
        --akhir-sejati reports/akhir_sejati_4h.json \\
        --min-median-stop-frac 0.004 --ulangan 300
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

from lux.backtest.engine import Konfig
from lux.backtest.run_h002 import hipotesis_h002, muat_konfig_h002
from lux.backtest.run_h007 import LOOKBACK as LOOKBACK_H007
from lux.backtest.run_h009 import (
    AMBANG_CARRY_KERAS,
    DATASET as DATASET_H009,
    KUNCI_TERLARANG,
    buat_konfig,
)
from lux.backtest.run_h010 import JANGKAR
from lux.backtest.runner import Opsi, Spek, jalankan_spek, muat_konteks
from lux.kerangka import bar_dari_hari
from lux.praregistrasi import Hipotesis, Kriteria
from lux.strategi import breakout_atr

# Empat sel. Huruf pertama sinyal, huruf kedua geometri keluar.
NAMA_SEL = ("SS", "SH", "AS", "AH")

NAMA_LAPORAN = {
    "SS": "h013_ss_sinyal_stop",
    "SH": "h013_sh_sinyal_horizon",
    "AS": "h013_as_acak_stop",
    "AH": "h013_ah_acak_horizon",
}

# Grid diimpor, tidak diketik ulang. Menyalin dengan tangan membuka peluang grid
# menyempit diam-diam ke arah nilai yang sudah diketahui menang.
LOOKBACK = list(LOOKBACK_H007)

# ADR-022. Dibekukan, bukan dilombakan. Nilainya jangkar H-010 dan bawaan Konfig,
# jadi ia bukan angka yang dipilih hari ini.
IMBALAN_BEKU = 2.0

# ADR-015 bagian 4.4, tidak dilombakan.
H_BAR = 48

# ADR-020. Tujuh hari pada kerangka 4h. Config memuat 168, yang pada 4h berarti
# 28 hari; memakainya akan membuat SS - SH mengukur panjang pegangan.
UMUR_SEL_STOP = bar_dari_hari(7, "4h")

# ADR-023. Maksud sesungguhnya dari bawaan Opsi 4320/2160/168, dinyatakan dalam
# satuan yang tidak bergantung interval.
HARI_LATIH = 180
HARI_UJI = 90
HARI_EMBARGO = 7

# TIDAK dikonversi, dan ketidaksimetrisan itu disengaja: pemanasan adalah
# kebutuhan BAR milik indikator (lookback terbesar 100 ditambah ATR 14), bukan
# rentang waktu. Mengonversinya "demi keseragaman" akan menyisakan 50 bar pada 4h
# dan membuat lookback 100 mustahil dihitung.
PEMANASAN = 200

# ADR-021. Seed yang sama dengan gerbang_entri_acak, dan pengacakan yang sama.
SEED_PERMUTASI = 42

# Ambang beku ADR-015 bagian B. Tidak bergerak sesudah hasil terlihat.
AMBANG_KONTRIBUSI_SINYAL = 0.020
MIN_ULANGAN = 300
MIN_TRADE_SEL = 100

DATASET = (
    "tier-b-v1 ohlcv_4h + funding_shard, "
    "universe_layak_v2_4h 438 simbol berlantai (ADR-017, ADR-018)"
)

# Satu-satunya angka dari H-010 dan H-012 yang dikutip, dan ia dikutip justru
# karena ia pembanding acak dan bukan hasil: 0,04661R muncul identik di kedua
# hipotesis. Ekspektasi keduanya TIDAK dikutip di sini.
SKOR_ACAK_TERDAHULU = 0.04661

RAMALAN = {
    "sumbangan_sinyal_R": (
        "0,000-0,015 sehingga GAGAL terhadap ambang 0,020; ini ramalan "
        "ADR-015 bagian 4.5 yang diulang tanpa perubahan"
    ),
    "sumbangan_geometri_R": "nilai mutlaknya LEBIH BESAR daripada sumbangan sinyal",
    "invarian_risiko": (
        "gagal pada SH dan AH, lulus atau hampir lulus pada SS; sebabnya "
        "umur mengisi di harga bar sungguhan sedangkan jalur stop tidak, "
        "jadi itu BUKAN bukti target lebih baik"
    ),
    "peringkat_AH": (
        "AH belum tentu terburuk; bila AH mengalahkan AS, yang terukur adalah "
        "keunggulan geometri di atas sinyal nol"
    ),
}


def jendela_bar(interval: str) -> dict:
    """Panjang jendela walk-forward dalam bar, diturunkan dari hari (ADR-023).

    Pada 1h hasilnya wajib identik dengan bawaan ``Opsi`` — 4320, 2160, 168 —
    supaya dua belas laporan yang sudah dikomit tetap dapat diulang. Pada 4h
    ketiganya menyusut seperempat, sebab yang dimaksud memang rentang waktu dan
    bukan jumlah bar.

    ``pemanasan`` tidak ada di sini dengan sengaja; ia bukan satuan waktu.
    """
    return {
        "panjang_latih": bar_dari_hari(HARI_LATIH, interval),
        "panjang_uji": bar_dari_hari(HARI_UJI, interval),
        "embargo": bar_dari_hari(HARI_EMBARGO, interval),
    }


def bar_dibutuhkan(interval: str) -> int:
    """Bar minimum agar satu jendela walk-forward dapat terbentuk.

    Dihitung, bukan diperkirakan, sebab inilah angka yang menentukan apakah run
    menghasilkan perdagangan atau menghasilkan laporan kosong yang tampak rapi.
    """
    j = jendela_bar(interval)
    return PEMANASAN + j["panjang_latih"] + j["embargo"] + j["panjang_uji"]


def pakai_target_sel(sel: str) -> bool:
    """Huruf kedua menentukan geometri keluar: S stop-target, H horizon tetap."""
    if sel not in NAMA_SEL:
        raise ValueError(f"sel tidak dikenal: {sel!r}; yang dikenal {NAMA_SEL}")
    return sel[1] == "S"


def umur_sel(sel: str) -> int:
    """Batas umur per sel, dalam bar 4h.

    Sel horizon memakai ``h`` dari ADR-015; sel stop-target memakai tujuh hari
    yang diturunkan dari satuan waktu, bukan angka 168 dari config.
    """
    return UMUR_SEL_STOP if pakai_target_sel(sel) else H_BAR


def sinyal_acak_sel(sel: str) -> bool:
    """Huruf pertama menentukan sinyal: S sungguhan, A permutasi."""
    if sel not in NAMA_SEL:
        raise ValueError(f"sel tidak dikenal: {sel!r}; yang dikenal {NAMA_SEL}")
    return sel[0] == "A"


def kandidat() -> list[dict]:
    """Tiga kandidat lookback, dan hanya itu (ADR-022).

    ``imbalan_R`` tetap ikut di dalam kandidat meski dibekukan, sebab
    ``run_h009.buat_konfig`` membacanya dari sana. Membuangnya berarti menyalin
    ulang mekanisme konfig, dan salinan itulah yang paling mudah melenceng.
    """
    return [{"lookback": lb, "imbalan_R": IMBALAN_BEKU} for lb in LOOKBACK]


def permutasi_sinyal(sinyal: np.ndarray, seed: int = SEED_PERMUTASI) -> np.ndarray:
    """Acak urutan sinyal tanpa mengubah jumlah maupun arahnya.

    Pengacakannya **sama** dengan ``gerbang_entri_acak``: ``default_rng(seed)``
    lalu ``rng.permutation``. Tidak ada mekanisme pengacakan kedua di riset ini;
    dua implementasi pengacakan adalah cara paling andal melahirkan dua sebaran
    nol yang berbeda tanpa ada yang menyadarinya.

    Aritmetikanya berdiri sebagai fungsi tingkat modul supaya ia dapat diuji
    tanpa membangun bingkai bar dan tanpa memanggil strategi (aturan 32).
    """
    dasar = np.asarray(sinyal)
    rng = np.random.default_rng(seed)
    return rng.permutation(dasar)


def sinyal_acak(df: pd.DataFrame, params: dict) -> np.ndarray:
    """Sinyal Donchian yang sama, waktunya dihancurkan.

    Permutasi dilakukan **per bingkai yang diberikan**, bukan atas gabungan
    lintas jendela seperti gerbang (ADR-021 keputusan 2). Akibatnya jumlah dan
    arah entri terjaga **per simbol**, yang lebih ketat daripada terjaga secara
    agregat — dan akibatnya pula angka sel AS **tidak** boleh diharapkan sama
    dengan skor acak gerbang. Bila keduanya kebetulan berdekatan, itu bukan
    konfirmasi.
    """
    return permutasi_sinyal(breakout_atr.sinyal(df, params))


def sinyal_sel(sel: str):
    return sinyal_acak if sinyal_acak_sel(sel) else breakout_atr.sinyal


def buat_konfig_sel(sel: str):
    """Bungkus ``run_h009.buat_konfig`` lalu tegakkan dua medan milik sel.

    Mekanisme carry keras diwarisi apa adanya, termasuk penolakan
    ``KUNCI_TERLARANG``. Yang ditambahkan hanya ``maks_umur_bar`` dan
    ``pakai_target``, dan keduanya **tidak** berasal dari kandidat: keduanya
    struktural, dan melombakan keduanya berarti mengulang cacat H-008 tempat
    pemaksimal ekspektasi mematikan pengaman yang memakan ekspektasi.
    """
    pakai = pakai_target_sel(sel)
    umur = umur_sel(sel)

    def bungkus(params: dict, dasar: Konfig) -> Konfig:
        k = buat_konfig(params, dasar)
        return replace(k, maks_umur_bar=umur, pakai_target=pakai)

    return bungkus


def hipotesis_h013(sel: str, konfig: Konfig, komit: str = "") -> Hipotesis:
    pakai = pakai_target_sel(sel)
    acak = sinyal_acak_sel(sel)
    return Hipotesis(
        id=f"H-013-{sel}",
        pernyataan=(
            f"Sel {sel} dari rancangan faktorial 2x2 ADR-015 bagian B: sinyal "
            f"{'permutasi' if acak else 'Donchian sungguhan'}, geometri keluar "
            f"{'stop + target' if pakai else f'horizon tetap {H_BAR} bar tanpa target'}. "
            "Yang diuji BUKAN kelulusan sel ini melainkan selisih antar sel: "
            "sumbangan sinyal SS - AS dengan ambang 0,020R, sumbangan geometri "
            "SS - SH, dan interaksinya. Skor entri acak H-010 dan H-012 identik "
            "sampai lima desimal pada 0,04661R sementara sinyal sungguhan "
            "bergerak di sekitarnya, sehingga kemungkinan paling sederhana "
            "adalah sinyalnya tidak menyumbang apa pun — dan kemungkinan itu "
            "belum pernah diuji sekali pun dalam dua belas hipotesis."
        ),
        dataset=DATASET,
        ruang_parameter={
            "lookback": LOOKBACK,
            # Dibekukan (ADR-022). Ditulis sebagai daftar satu nilai supaya ia
            # ikut ke dalam sidik hipotesis.
            "imbalan_R": [IMBALAN_BEKU],
            "sel": [sel],
            "pakai_target": [pakai],
            "sinyal_dipermutasi": [acak],
            "maks_umur_bar": [umur_sel(sel)],
            # ADR-023. Ikut ke dalam sidik, sebab mengubah panjang jendela
            # mengubah arti seluruh perbandingan.
            "jendela_hari": [HARI_LATIH, HARI_UJI, HARI_EMBARGO],
            KUNCI_TERLARANG: [AMBANG_CARRY_KERAS],
            "atr_pengali_stop": [konfig.atr_pengali_stop],
            "maks_carry_R": [konfig.maks_carry_R],
            "jendela_carry_hari": [konfig.jendela_carry_hari],
            "maks_biaya_masuk_R": [konfig.maks_biaya_masuk_R],
        },
        # Tidak dilonggarkan sedikit pun dari H-002 sampai H-012, meskipun sel
        # pembanding memang tidak dimaksudkan lulus.
        kriteria=Kriteria(
            min_ekspektasi_R=0.05,
            min_trade_luar_sampel=100,
            maks_p_entri_acak=0.05,
            min_jendela_positif_rasio=0.5,
        ),
        komit=komit,
    )


def spek_sel(sel: str, konfig: Konfig, komit: str = "") -> Spek:
    return Spek(
        h=hipotesis_h013(sel, konfig, komit),
        sinyal=sinyal_sel(sel),
        kandidat=kandidat(),
        nama=NAMA_LAPORAN[sel],
        params_lookahead={"lookback": 55},
        buat_konfig=buat_konfig_sel(sel),
    )


def kontribusi(ekspektasi: dict, trade: dict) -> dict:
    """Tiga selisih antar sel, beserta putusan kriteria utama.

    Aritmetika ini berdiri di sini alih-alih di ``main`` karena aritmetika yang
    hanya hidup di dalam ``main`` tidak pernah benar-benar diuji, dan justru
    aritmetika inilah keseluruhan isi H-013.

    Sel yang perdagangan luar sampelnya kurang dari ``MIN_TRADE_SEL`` membuat
    seluruh perbandingan **TIDAK DAPAT DINILAI**, bukan membuatnya gagal dan
    bukan pula dinilai dengan sel yang tersisa. Menilai selisih dari sel yang
    tipis berarti melaporkan kebisingan sebagai temuan.
    """
    kurang = [s for s in NAMA_SEL if s not in ekspektasi or s not in trade]
    if kurang:
        raise ValueError(f"sel tidak lengkap: {kurang}; wajib {list(NAMA_SEL)}")

    tipis = [
        s
        for s in NAMA_SEL
        if ekspektasi[s] is None or int(trade[s]) < MIN_TRADE_SEL
    ]
    dasar = {
        "ambang_sumbangan_sinyal_R": AMBANG_KONTRIBUSI_SINYAL,
        "min_trade_per_sel": MIN_TRADE_SEL,
        "ekspektasi_R": {s: ekspektasi[s] for s in NAMA_SEL},
        "trade": {s: int(trade[s]) for s in NAMA_SEL},
    }
    if tipis:
        return dasar | {
            "dapat_dinilai": False,
            "sebab": (
                f"sel dengan perdagangan luar sampel kurang dari "
                f"{MIN_TRADE_SEL} atau tanpa ekspektasi: {tipis}"
            ),
            "sumbangan_sinyal_R": None,
            "sumbangan_geometri_R": None,
            "interaksi_R": None,
            "lulus": False,
        }

    ss = float(ekspektasi["SS"])
    sh = float(ekspektasi["SH"])
    a_s = float(ekspektasi["AS"])
    ah = float(ekspektasi["AH"])
    sinyal = ss - a_s
    geometri = ss - sh
    return dasar | {
        "dapat_dinilai": True,
        "sebab": "",
        "sumbangan_sinyal_R": sinyal,
        "sumbangan_geometri_R": geometri,
        "interaksi_R": (ss - a_s) - (sh - ah),
        "lulus": sinyal >= AMBANG_KONTRIBUSI_SINYAL,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--interval", default="4h")
    ap.add_argument("--universe", default="reports/universe_layak_v2_4h.json")
    ap.add_argument("--akhir-sejati", default="reports/akhir_sejati_4h.json")
    ap.add_argument("--config", default="config/lux.yaml")
    ap.add_argument("--out", default="reports")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--ulangan", type=int, default=MIN_ULANGAN)
    # Diserahkan pemanggil, tidak diketik di modul ini. Pola yang sama dipakai
    # runner untuk lantai ADR-014: ambang yang hidup di dua tempat akan
    # melenceng di salah satunya.
    ap.add_argument("--min-median-stop-frac", type=float, required=True)
    ap.add_argument("--komit", default="")
    a = ap.parse_args(argv)

    konfig = muat_konfig_h002(Path(a.config))

    # Seluruh pagar di bawah berjalan sebelum satu bar pun dimuat. Pemeriksaan
    # yang bisa gagal tidak boleh diletakkan di ujung run panjang.
    if a.ulangan < MIN_ULANGAN:
        print(
            f"DITOLAK: ulangan permutasi {a.ulangan} < {MIN_ULANGAN}. "
            "Ambang ADR-015 tidak bergerak.",
            flush=True,
        )
        return 2

    if a.interval != "4h":
        print(
            f"DITOLAK: H-013 hanya sah pada kerangka 4h, diberi {a.interval!r}. "
            f"Batas umur {UMUR_SEL_STOP} dan {H_BAR} keduanya diturunkan untuk 4h.",
            flush=True,
        )
        return 2

    for nama_arg, jalur in (("universe", a.universe), ("akhir-sejati", a.akhir_sejati)):
        if "4h" not in Path(jalur).name:
            print(
                f"DITOLAK: {nama_arg} {jalur!r} tidak menyebut 4h; "
                "memakai berkas 1h pada kerangka 4h adalah cacat buta-interval.",
                flush=True,
            )
            return 2

    if a.min_median_stop_frac <= 0:
        print(
            "DITOLAK: lantai median stop_frac wajib menyala di H-013. "
            "Tanpa lantai, satu simbol degenerat cukup untuk menguasai "
            "seluruh selisih antar sel, seperti USDCUSDT di H-011.",
            flush=True,
        )
        return 2

    if konfig.maks_biaya_masuk_R <= 0:
        print(
            "DITOLAK: pengaman biaya masuk ADR-014 wajib menyala di H-013.",
            flush=True,
        )
        return 2

    if konfig.maks_carry_R <= 0:
        raise ValueError("H-013 menuntut saringan ADR-004 tetap menyala")

    if AMBANG_CARRY_KERAS <= 0:
        raise ValueError("ambang carry keras wajib menyala di H-013")

    # Tripwire DIBALIK: dataset wajib BERBEDA dari H-002, sebab H-013 berjalan
    # pada 4h dengan semesta berlantai.
    if DATASET == hipotesis_h002(konfig).dataset or DATASET == DATASET_H009:
        raise ValueError(
            "dataset H-013 wajib berbeda dari H-002/H-009; interval dan "
            "semestanya memang bukan yang sama"
        )
    if "4h" not in DATASET:
        raise ValueError("dataset H-013 wajib menyebut kerangka 4h")

    if LOOKBACK != list(LOOKBACK_H007):
        raise ValueError("lookback H-013 wajib identik dengan H-007")

    if IMBALAN_BEKU not in JANGKAR:
        raise ValueError(
            f"imbalan beku {IMBALAN_BEKU} bukan jangkar H-010 {JANGKAR}"
        )

    if len(kandidat()) != len(LOOKBACK):
        raise ValueError("kandidat H-013 wajib hanya melombakan lookback")

    for p in kandidat():
        if KUNCI_TERLARANG in p:
            raise ValueError(f"{KUNCI_TERLARANG} bocor ke ruang pencarian")
        if "pakai_target" in p or "maks_umur_bar" in p:
            raise ValueError("geometri keluar tidak boleh dilombakan (ADR-020)")

    if UMUR_SEL_STOP == konfig.maks_umur_bar:
        raise ValueError(
            f"maks_umur_bar sel stop wajib diturunkan dari hari, bukan diambil "
            f"dari config ({konfig.maks_umur_bar} bar = 28 hari pada 4h)"
        )

    # ADR-023. Jendela 1h wajib tidak bergeser sedikit pun, dan jendela 4h wajib
    # cukup pendek untuk menghasilkan sedikitnya satu jendela di atas lantai
    # kelayakan. Keduanya dihitung di sini, bukan dipercaya.
    j1 = jendela_bar("1h")
    if (j1["panjang_latih"], j1["panjang_uji"], j1["embargo"]) != (4320, 2160, 168):
        raise ValueError(
            f"jendela 1h bergeser dari bawaan Opsi: {j1}; dua belas laporan "
            "yang sudah dikomit tidak lagi dapat diulang"
        )

    jen = jendela_bar(a.interval)
    butuh = bar_dibutuhkan(a.interval)
    if butuh >= bar_dibutuhkan("1h"):
        raise ValueError(
            f"jendela {a.interval} menuntut {butuh} bar, tidak lebih sedikit "
            "daripada 1h; konversi ADR-023 tidak berjalan"
        )

    opsi = Opsi(
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
        ulangan=a.ulangan,
        min_median_stop_frac=a.min_median_stop_frac,
    )

    print(f"H-013 empat sel: {list(NAMA_SEL)}", flush=True)
    print(f"kandidat per sel: {len(kandidat())} (imbalan BEKU {IMBALAN_BEKU})", flush=True)
    print(
        f"batas umur: sel stop {UMUR_SEL_STOP} bar 4h = 7 hari, "
        f"sel horizon {H_BAR} bar 4h (config {konfig.maks_umur_bar} TIDAK dipakai)",
        flush=True,
    )
    print(
        f"ADR-023 jendela {a.interval}: latih {jen['panjang_latih']} "
        f"({HARI_LATIH} hari), uji {jen['panjang_uji']} ({HARI_UJI} hari), "
        f"embargo {jen['embargo']} ({HARI_EMBARGO} hari), "
        f"pemanasan {PEMANASAN} bar TIDAK dikonversi",
        flush=True,
    )
    print(
        f"bar dibutuhkan satu jendela: {butuh} "
        f"(bawaan 1h akan menuntut {bar_dibutuhkan('1h')})",
        flush=True,
    )
    print(f"lantai median stop_frac: {a.min_median_stop_frac}", flush=True)
    print(f"pengaman biaya masuk: {konfig.maks_biaya_masuk_R}R", flush=True)
    print(f"ulangan permutasi per sel: {a.ulangan}", flush=True)
    print(f"seed permutasi: {SEED_PERMUTASI} (sama dengan gerbang)", flush=True)
    print(
        f"skor acak terdahulu yang memicu H-013: {SKOR_ACAK_TERDAHULU}R, "
        "identik di H-010 dan H-012",
        flush=True,
    )
    print(
        "KONSEKUENSI KONSTRUKSI (bukan temuan): lookahead dan entri_acak akan "
        "GAGAL pada sel AS dan AH; kelulusan gerbang hanya syarat pada SS",
        flush=True,
    )
    for nama, isi_ramalan in RAMALAN.items():
        print(f"  ramalan {nama}: {isi_ramalan}", flush=True)

    ktx = muat_konteks(opsi, konfig)

    hasil_sel: dict[str, dict] = {}
    for sel in NAMA_SEL:
        dasar_sel = replace(
            konfig, maks_umur_bar=umur_sel(sel), pakai_target=pakai_target_sel(sel)
        )
        print(
            f"\n### SEL {sel}: sinyal "
            f"{'permutasi' if sinyal_acak_sel(sel) else 'sungguhan'}, "
            f"pakai_target {dasar_sel.pakai_target}, "
            f"maks_umur_bar {dasar_sel.maks_umur_bar}",
            flush=True,
        )
        hasil_sel[sel] = jalankan_spek(
            spek_sel(sel, dasar_sel, a.komit), ktx, dasar_sel, opsi
        )
        # Dicetak SEBELUM ekspektasi ditafsirkan: nol jendela berarti cacat
        # konfigurasi, bukan temuan tentang sinyal (ADR-023 keputusan 4).
        print(
            f"sel {sel}: {hasil_sel[sel]['jumlah_jendela']} jendela, "
            f"{hasil_sel[sel]['trade']} trade luar sampel "
            f"(ambang ternilai {MIN_TRADE_SEL})",
            flush=True,
        )

    ringkas = kontribusi(
        {s: hasil_sel[s]["ekspektasi_R"] for s in NAMA_SEL},
        {s: hasil_sel[s]["trade"] for s in NAMA_SEL},
    )

    isi = {
        "hipotesis": "H-013",
        "sel": {
            s: {
                "id": hasil_sel[s]["id"],
                "nama": hasil_sel[s]["nama"],
                "sidik": hasil_sel[s]["sidik"],
                "ekspektasi_R": hasil_sel[s]["ekspektasi_R"],
                "total_R": hasil_sel[s]["total_R"],
                "trade": hasil_sel[s]["trade"],
                "jumlah_jendela": hasil_sel[s]["jumlah_jendela"],
                "jendela_positif": hasil_sel[s]["jendela_positif"],
                "p_entri_acak": hasil_sel[s]["p_entri_acak"],
                "gerbang_gagal": hasil_sel[s]["gerbang_gagal"],
                "alasan_keluar": hasil_sel[s]["alasan_keluar"],
                "pakai_target": pakai_target_sel(s),
                "maks_umur_bar": umur_sel(s),
                "sinyal_dipermutasi": sinyal_acak_sel(s),
            }
            for s in NAMA_SEL
        },
        "kontribusi": ringkas,
        "parameter_beku": {
            "imbalan_R": IMBALAN_BEKU,
            "h_bar": H_BAR,
            "umur_sel_stop": UMUR_SEL_STOP,
            "lookback": LOOKBACK,
            "seed_permutasi": SEED_PERMUTASI,
            "ulangan": a.ulangan,
            "min_median_stop_frac": a.min_median_stop_frac,
            "jendela_bar": jen,
            "pemanasan_bar": PEMANASAN,
            "bar_dibutuhkan_satu_jendela": butuh,
        },
        "ramalan": RAMALAN,
    }
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "backtest_h013_kontribusi.json").write_text(
        json.dumps(isi, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    strip = "\u2014"

    def angka(x, fmt="+.6f"):
        return strip if x is None else format(x, fmt)

    md = [
        "# H-013 \u2014 sumbangan sinyal terhadap sumbangan geometri keluar",
        "",
        "Yang dinilai adalah **selisih antar sel**, bukan kelulusan satu sel. "
        "Sel SH, AS, dan AH adalah pembanding, bukan kandidat untuk didagangkan.",
        "",
        "`lookahead` dan `entri_acak` **dijamin gagal** pada sel AS dan AH "
        "karena permutasi bergantung panjang array (ADR-021). Itu konsekuensi "
        "konstruksi dan bukan temuan tentang data.",
        "",
        f"Jendela walk-forward diturunkan dari hari (ADR-023): latih "
        f"{jen['panjang_latih']} bar, uji {jen['panjang_uji']}, embargo "
        f"{jen['embargo']}, pemanasan {PEMANASAN} bar yang **tidak** dikonversi. "
        f"Satu jendela menuntut {butuh} bar.",
        "",
        "## Empat sel",
        "",
        "| Sel | Sinyal | Target | Umur (bar 4h) | Jendela | Trade | Ekspektasi R | p acak | Gerbang gagal |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for s in NAMA_SEL:
        b = isi["sel"][s]
        md.append(
            f"| {s} | {'permutasi' if b['sinyal_dipermutasi'] else 'sungguhan'} "
            f"| {'ya' if b['pakai_target'] else 'tidak'} "
            f"| {b['maks_umur_bar']} | {b['jumlah_jendela']:,} | {b['trade']:,} "
            f"| {angka(b['ekspektasi_R'])} | {angka(b['p_entri_acak'], '.4f')} "
            f"| {', '.join(b['gerbang_gagal']) or strip} |"
        )

    md += [
        "",
        "## Tiga selisih",
        "",
        f"- Sumbangan **sinyal** (SS \u2212 AS): **{angka(ringkas['sumbangan_sinyal_R'])}R** "
        f"terhadap ambang {AMBANG_KONTRIBUSI_SINYAL}R",
        f"- Sumbangan **geometri** (SS \u2212 SH): **{angka(ringkas['sumbangan_geometri_R'])}R**",
        f"- **Interaksi** (SS\u2212AS) \u2212 (SH\u2212AH): **{angka(ringkas['interaksi_R'])}R**",
        "",
        f"**{'LULUS' if ringkas['lulus'] else ('TIDAK DAPAT DINILAI' if not ringkas['dapat_dinilai'] else 'GAGAL')}**",
        "",
    ]
    if not ringkas["dapat_dinilai"]:
        md += [ringkas["sebab"], ""]
    md += [
        "Sumbangan geometri yang lebih besar daripada sumbangan sinyal berarti "
        "sepuluh hipotesis pertama mengukur struktur keluar, bukan kemampuan "
        "memilih momen. Itu hasil yang sah dan tidak boleh dibaca sebagai "
        "kegagalan mesin.",
        "",
        "`invarian_risiko` yang jatuh pada sel tanpa target **bukan** bukti "
        "target lebih baik: jalur `umur` mengisi pada harga bar sungguhan, "
        "sedangkan jalur stop tanpa `stop_hormati_celah` tidak pernah lebih "
        "buruk dari sekitar 1R.",
        "",
    ]
    (out / "backtest_h013_kontribusi.md").write_text(
        "\n".join(md) + "\n", encoding="utf-8"
    )

    print("", flush=True)
    print(json.dumps(ringkas, indent=2, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
