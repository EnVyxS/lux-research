"""H-015 — apakah saringan funding memuat informasi, atau hanya kecondongan arah?

H-014 mati dengan cara yang tidak menyenangkan: ia berjalan dengan pengaman
carry terealisasi **mati**, dan tidak seorang pun — termasuk dua pagar yang
dipasang justru untuk itu — menyadarinya sampai runnya selesai (ADR-036).
Modul ini karena itu memanggil ``konfig_audit`` sebelum memuat satu bar pun, dan
berhenti bila pengaman yang dituntutnya tidak menyala.

TIGA SEL, SATU SELISIH YANG MENGIKAT
------------------------------------

| Sel | Sinyal | Maksud |
|---|---|---|
| K | Donchian apa adanya | kontrol |
| F | Donchian, entri ditolak saringan funding | hipotesis |
| A | Donchian, entri ditolak **acak** dengan cacah identik | pembanding |

Yang mengikat hanya **F − A** (ADR-037 §5). ``F − K`` dihitung dan dicetak,
tetapi dilabeli tidak mengikat di setiap tempat ia muncul, sebab funding
bernilai positif pada **79,1%** periode: saringan funding apa pun karena itu
membuang long jauh lebih sering daripada short dan akan mengalahkan kontrol
meski tidak memuat setitik pun informasi. Memakai ``F − K`` sebagai dasar
kelulusan ada di daftar angka haram.

LIMA HAL YANG WAJIB DIKETAHUI SEBELUM MEMBACA HASILNYA
-------------------------------------------------------
**1. Ketiga sel wajib berkonfig identik, dan itu ditegakkan.** Satu-satunya yang
membedakan sel adalah fungsi sinyalnya. Bila konfig antar sel berselisih, selisih
F − A akan memuat perbedaan mesin alih-alih perbedaan informasi — dan itu persis
bentuk cacat kelas 18, hanya berpindah tempat.

**2. Konfig pendahulu tidak diketik ulang.** Pembandingnya dibangun oleh kode
H-013 sendiri lewat ``run_h013.buat_konfig_sel("SS")``. Pagar yang mengutip nilai
dari ingatan penulisnya tidak menjaga apa pun (aturan 31); yang dilaporkan di
sini adalah selisih terhadap yang **sungguh dijalankan**.

**3. Selisih terhadap H-013 memang diharapkan ada, dan itu bukan kegagalan.**
``maks_umur_bar`` 48 lawan 42: H-013 sel stop memakai tujuh hari, sedangkan
ADR-037 mematok horizon 48 bar. Selisih tidak menghalangi run; yang menghalangi
hanya pengaman yang mati.

**4. ``lookahead`` DIJAMIN gagal pada sel A.** Penolakan acak bergantung pada
cacah per bulan di seluruh potongan, sedangkan gerbang itu memotong bingkai lalu
menuntut sinyal awal tidak berubah. Menurut aturan 36 itu konsekuensi
konstruksi, bukan temuan, dan haram dilaporkan sebagai temuan. Sel F **tidak**
memperoleh pemakluman itu: saringannya hanya membaca masa lalu, jadi bila
``lookahead`` jatuh pada F, yang jatuh adalah kodenya.

**5. Keluar ``carry`` yang nol pada ketiga sel adalah sidik jari cacat 18
(R-L5).** Pengaman carry menyala di konfig dasar; bila tidak satu pun posisi
keluar lewat jalur itu, audit yang hijau tidak cukup untuk mempercayai runnya.

Pemakaian:
    python -m lux.backtest.run_h015 --dir aset --interval 4h \\
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

from lux.backtest.engine import Konfig
from lux.backtest.konfig_audit import laporan_kesebandingan, selisih_konfig
from lux.backtest.run_h002 import muat_konfig_h002
from lux.backtest.run_h007 import LOOKBACK as LOOKBACK_H007
from lux.backtest.run_h009 import (
    AMBANG_CARRY_KERAS,
    KUNCI_TERLARANG,
    buat_konfig,
)
from lux.backtest.run_h012 import kunci_config
from lux.backtest.run_h013 import (
    AMBANG_KONTRIBUSI_SINYAL,
    HARI_EMBARGO,
    HARI_LATIH,
    HARI_UJI,
    H_BAR,
    IMBALAN_BEKU,
    MIN_TRADE_SEL,
    MIN_ULANGAN,
    PEMANASAN,
    bar_dibutuhkan,
    buat_konfig_sel,
    dasar_riset,
    jendela_bar,
)
from lux.backtest.runner import Opsi, Spek, jalankan_spek, muat_konteks
from lux.backtest.saringan_funding import (
    AMBANG_RATE,
    JENDELA_HARI,
    MIN_PENAGIHAN,
    NAMA_SEL,
    SEED_ACAK_H015,
    sinyal_sel,
)
from lux.degenerasi import AMBANG_BIAYA_MASUK_R
from lux.praregistrasi import Hipotesis, Kriteria
from lux.strategi import breakout_atr

NAMA_LAPORAN = {
    "K": "h015_k_kontrol",
    "F": "h015_f_saringan",
    "A": "h015_a_acak",
}

LOOKBACK = list(LOOKBACK_H007)

# ADR-037 §7. Daftar ini WAJIB dinyatakan oleh run, bukan oleh alat auditnya:
# pagar yang mengutip angka dari kode yang dijaganya tidak menjaga apa pun.
# Bila salah satu dari keduanya tidak bernilai 0,25 pada Konfig dasar, run ini
# berhenti dengan kode 3 — itu memang tujuannya, dan menurunkan tuntutannya
# sesudah melihat kode keluar adalah pelanggaran ADR-037 §10.
PENGAMAN_WAJIB = {
    "maks_carry_realisasi_R": 0.25,
    "maks_carry_R": 0.25,
}

NAMA_PENDAHULU = "H-013 SS"

DATASET = (
    "tier-b-v1 ohlcv_4h + funding_shard, "
    "universe_layak_v2_4h 438 simbol berlantai (ADR-017, ADR-018), "
    "jadwal funding per simbol dari funding_model"
)

PEMBATAS_PUTUSAN = (
    "Medan `lulus` di berkas ini hanya menguji BESARAN F \u2212 A terhadap ambang "
    "0,020R. Ia BUKAN kelulusan hipotesis: ADR-037 \u00a75 menuntut besaran itu "
    "DAN p \u2264 0,05 atas satuan penarikan bulan kalender UTC (ADR-028), dan p "
    "tidak dihitung di berkas ini. Selisih F \u2212 K yang ikut tercetak TIDAK "
    "MENGIKAT dalam bentuk apa pun: funding positif pada 79,1% periode membuat "
    "saringan apa pun mengalahkan kontrol tanpa memuat informasi, sehingga "
    "memakainya sebagai dasar kelulusan ada di daftar angka haram."
)

RAMALAN = {
    "R-L1": (
        "sel F menolak long lebih dari 3x lebih sering daripada short; "
        "DIJAMIN konstruksi, jadi ketepatannya tidak bernilai apa-apa"
    ),
    "R-L2": "H-015 DITOLAK: rerata bulanan F \u2212 A kurang dari +0,020R",
    "R-L3": "nilai mutlak F \u2212 A lebih kecil daripada nilai mutlak F \u2212 K",
    "R-L4": "cacah pytest paling sedikit 884",
    "R-L5": (
        "keluar `carry` bukan nol pada ketiga sel; nol berarti sidik jari "
        "cacat 18 dan run dibatalkan meski audit konfig hijau"
    ),
}


def kandidat() -> list[dict]:
    """Tiga kandidat lookback, sama persis dengan H-013.

    Grid diimpor dari H-007 dan tidak diketik ulang. Menyalinnya dengan tangan
    membuka peluang grid menyempit diam-diam ke arah nilai yang sudah diketahui
    menang, dan penyempitan semacam itu tidak meninggalkan jejak.
    """
    return [{"lookback": lb, "imbalan_R": IMBALAN_BEKU} for lb in LOOKBACK]


def buat_konfig_h015(params: dict, dasar: Konfig) -> Konfig:
    """Konfig satu kandidat: mekanisme H-009 diwarisi, geometri dipatok ADR-037.

    ``maks_umur_bar`` dan ``pakai_target`` **tidak** berasal dari kandidat.
    Keduanya struktural; melombakannya berarti mengulang cacat H-008 tempat
    pemaksimal ekspektasi mematikan pengaman yang memakan ekspektasi.

    Fungsi ini identik untuk ketiga sel. Itu bukan kebetulan melainkan syarat:
    yang membedakan sel hanyalah sinyalnya.
    """
    k = buat_konfig(params, dasar)
    return replace(k, maks_umur_bar=H_BAR, pakai_target=True)


def konfig_dasar_h015(konfig: Konfig) -> Konfig:
    """Konfig dasar run ini: pengaman carry dinyalakan di dasarnya (aturan 57).

    H-014 memasang pengaman itu hanya di jalur ``buat_konfig``, lalu memakai
    ``buat_konfig=None`` sehingga jalur itu tidak pernah dilewati dan ``Konfig``
    kembali ke bawaannya yang **mati**. Menyalakannya di dasar berarti bahkan
    jalur yang lupa memanggil pabrik konfig tetap berjalan dengan pengaman
    hidup.
    """
    return replace(
        dasar_riset(konfig),
        maks_carry_realisasi_R=AMBANG_CARRY_KERAS,
        maks_umur_bar=H_BAR,
        pakai_target=True,
    )


def hipotesis_h015(sel: str, konfig: Konfig, komit: str = "") -> Hipotesis:
    if sel not in NAMA_SEL:
        raise ValueError(f"sel tidak dikenal: {sel!r}; yang dikenal {NAMA_SEL}")
    peran = {
        "K": "kontrol, Donchian apa adanya",
        "F": "hipotesis, entri ditolak saringan funding",
        "A": "pembanding, entri ditolak acak dengan cacah identik sel F",
    }[sel]
    return Hipotesis(
        id=f"H-015-{sel}",
        pernyataan=(
            f"Sel {sel} ({peran}) dari rancangan tiga sel ADR-037. Yang diuji "
            "bukan kelulusan sel ini melainkan selisih F \u2212 A: apakah saringan "
            "funding memuat INFORMASI, ataukah keunggulannya seluruhnya berasal "
            "dari kecondongan arah. Funding positif pada 79,1% periode, sehingga "
            "saringan apa pun membuang long jauh lebih sering daripada short dan "
            "akan mengalahkan kontrol tanpa memuat apa pun. Karena itu hanya "
            "ADR-037 \u00a75 mengikat, dan selisih F \u2212 K haram dipakai sebagai dasar "
            "kelulusan."
        ),
        dataset=DATASET,
        ruang_parameter={
            "lookback": LOOKBACK,
            "imbalan_R": [IMBALAN_BEKU],
            "sel": [sel],
            "ambang_rate": [AMBANG_RATE],
            "min_penagihan": [MIN_PENAGIHAN],
            "jendela_funding_hari": [JENDELA_HARI],
            "seed_acak": [SEED_ACAK_H015],
            "maks_umur_bar": [H_BAR],
            "pakai_target": [True],
            "jendela_hari": [HARI_LATIH, HARI_UJI, HARI_EMBARGO],
            KUNCI_TERLARANG: [AMBANG_CARRY_KERAS],
            "maks_carry_R": [konfig.maks_carry_R],
            "maks_biaya_masuk_R": [konfig.maks_biaya_masuk_R],
            "stop_hormati_celah": [konfig.stop_hormati_celah],
        },
        # Tidak dilonggarkan sedikit pun, meski sel pembanding memang tidak
        # dimaksudkan lulus. Perlu dicatat terbuka: kriteria ini TIDAK dapat
        # menyatakan satuan penarikan maupun p bulanan (cacat 19, ADR-037 \u00a78),
        # jadi ia bukan tempat kriteria H-015 yang sesungguhnya hidup.
        kriteria=Kriteria(
            min_ekspektasi_R=0.05,
            min_trade_luar_sampel=100,
            maks_p_entri_acak=0.05,
            min_jendela_positif_rasio=0.5,
        ),
        komit=komit,
    )


def spek_sel(sel: str, jadwal_semua, konfig: Konfig, komit: str = "") -> Spek:
    """Spek satu sel. Dibangun **sesudah** konteks dimuat, sebab ia butuh jadwal.

    Saringan mengenali simbolnya dari kolom ``symbol`` pada bingkai, sehingga
    kontrak ``buat_sinyal(df, params)`` yang dipakai empat belas hipotesis tidak
    perlu diperlebar. Memperlebarnya berarti menyentuh ``runner.py``, dan itu
    membahayakan pengulangan seluruh laporan yang sudah dikomit.
    """
    return Spek(
        h=hipotesis_h015(sel, konfig, komit),
        sinyal=sinyal_sel(sel, jadwal_semua, breakout_atr.sinyal),
        kandidat=kandidat(),
        nama=NAMA_LAPORAN[sel],
        params_lookahead={"lookback": 55},
        buat_konfig=buat_konfig_h015,
    )


def kontribusi_h015(ekspektasi: dict, trade: dict) -> dict:
    """Dua selisih, dan hanya satu di antaranya boleh menentukan apa pun.

    Aritmetika ini berdiri di tingkat modul, bukan di dalam ``main``, karena
    aritmetika yang hanya hidup di dalam ``main`` tidak pernah benar-benar
    diuji — dan justru aritmetika inilah keseluruhan isi H-015.

    Sel yang perdagangan luar sampelnya kurang dari ``MIN_TRADE_SEL`` membuat
    seluruh perbandingan TIDAK DAPAT DINILAI, bukan membuatnya gagal. Sel F yang
    tipis adalah hasil yang sangat mungkin di sini: saringan yang menolak
    hampir seluruh long dapat menyisakan terlalu sedikit perdagangan untuk
    dinilai, dan keadaan itu wajib berbunyi alih-alih dilaporkan sebagai angka.
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
        "ambang_selisih_mengikat_R": AMBANG_KONTRIBUSI_SINYAL,
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
            "selisih_mengikat_F_A_R": None,
            "selisih_TIDAK_mengikat_F_K_R": None,
            "lulus": False,
        }

    f = float(ekspektasi["F"])
    a = float(ekspektasi["A"])
    k = float(ekspektasi["K"])
    return dasar | {
        "dapat_dinilai": True,
        "sebab": "",
        "selisih_mengikat_F_A_R": f - a,
        "selisih_TIDAK_mengikat_F_K_R": f - k,
        "lulus": (f - a) >= AMBANG_KONTRIBUSI_SINYAL,
    }


def prosa_h015(ringkas: dict) -> list[str]:
    """Kalimat penafsir yang diturunkan dari angka, bukan dipatok (aturan 41).

    Prosa yang dipatok **dapat** salah tanpa pernah berbunyi; itu sudah terjadi
    sekali pada laporan H-013 yang membantah datanya sendiri.
    """
    if not ringkas.get("dapat_dinilai"):
        return [
            "**TIDAK DAPAT DINILAI.** Tidak satu pun kalimat penafsir ditulis, "
            "sebab tidak ada selisih yang sah untuk ditafsirkan. "
            f"Sebab: {ringkas.get('sebab') or 'tidak dinyatakan'}",
            "",
            PEMBATAS_PUTUSAN,
            "",
        ]

    fa = float(ringkas["selisih_mengikat_F_A_R"])
    fk = float(ringkas["selisih_TIDAK_mengikat_F_K_R"])
    ambang = float(ringkas["ambang_selisih_mengikat_R"])
    baris: list[str] = []

    if fa < 0:
        baris.append(
            f"Selisih mengikat F \u2212 A **negatif** ({fa:+.6f}R): saringan funding "
            "kalah dari pembuangan acak yang cacahnya sama. Bila ini bertahan "
            "sesudah p bulanan dihitung, yang gugur bukan hanya H-015 melainkan "
            "anggapan bahwa rate funding memuat informasi arah sama sekali."
        )
    elif fa < ambang:
        baris.append(
            f"Selisih mengikat F \u2212 A ({fa:+.6f}R) **di bawah** ambang beku "
            f"{ambang}R, jadi separuh kriteria yang dapat dihitung sudah tidak "
            "terpenuhi. Ambang itu tidak digeser."
        )
    else:
        baris.append(
            f"Selisih mengikat F \u2212 A ({fa:+.6f}R) **melewati** ambang besaran "
            f"{ambang}R. Itu aritmetika, bukan kelulusan: p bulanan belum "
            "dihitung di berkas ini."
        )

    if abs(fk) > abs(fa):
        baris.append(
            f"Selisih TIDAK mengikat F \u2212 K ({fk:+.6f}R) lebih besar dalam nilai "
            f"mutlak daripada F \u2212 A ({fa:+.6f}R). Bacaan itu konsisten dengan "
            "funding positif 79,1%: sebagian keunggulan saringan terhadap "
            "kontrol adalah kecondongan arah, bukan informasi. Angka F \u2212 K "
            "tetap haram dipakai sebagai dasar kelulusan."
        )
    else:
        baris.append(
            f"Selisih F \u2212 A ({fa:+.6f}R) tidak lebih kecil daripada F \u2212 K "
            f"({fk:+.6f}R) dalam nilai mutlak. Ini **membalik** R-L3 dan menuntut "
            "pemeriksaan: pada funding yang positif 79,1% periode, keadaan itu "
            "tidak diharapkan dan lebih mungkin menandakan cacat pada "
            "pencocokan cacah sel A daripada menandakan informasi."
        )

    hasil: list[str] = []
    for b in baris:
        hasil += [b, ""]
    hasil += [PEMBATAS_PUTUSAN, ""]
    return hasil


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
    ap.add_argument("--min-median-stop-frac", type=float, required=True)
    ap.add_argument("--komit", default="")
    a = ap.parse_args(argv)

    # Pagar argumen berjalan sebelum config dibaca dan jauh sebelum data dimuat.
    # Pemeriksaan yang bisa gagal tidak boleh diletakkan di ujung run empat jam.
    if a.ulangan < MIN_ULANGAN:
        print(
            f"DITOLAK: ulangan permutasi {a.ulangan} < {MIN_ULANGAN}. "
            "Ambang ADR-015 tidak bergerak.",
            flush=True,
        )
        return 2

    if a.interval != "4h":
        print(
            f"DITOLAK: H-015 hanya sah pada kerangka 4h, diberi {a.interval!r}. "
            f"Horizon {H_BAR} bar diturunkan untuk 4h.",
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
            "DITOLAK: lantai median stop_frac wajib menyala di H-015. "
            "Tanpa lantai, satu simbol degenerat cukup untuk menguasai selisih "
            "antar sel, seperti USDCUSDT di H-011.",
            flush=True,
        )
        return 2

    mentah = muat_konfig_h002(Path(a.config))
    dasar = konfig_dasar_h015(mentah)

    if dasar.maks_biaya_masuk_R != AMBANG_BIAYA_MASUK_R:
        raise ValueError(
            f"pengaman biaya masuk gagal terpasang: {dasar.maks_biaya_masuk_R} "
            f"bukan {AMBANG_BIAYA_MASUK_R}"
        )
    if not dasar.stop_hormati_celah:
        raise ValueError("stop_hormati_celah wajib menyala (ADR-016)")

    kunci = kunci_config(Path(a.config))
    if kunci["maks_biaya_masuk_R"] != AMBANG_BIAYA_MASUK_R:
        raise ValueError(
            f"config maks_biaya_masuk_R {kunci['maks_biaya_masuk_R']} berselisih "
            f"dengan degenerasi {AMBANG_BIAYA_MASUK_R}"
        )
    if kunci["min_median_stop_frac"] != a.min_median_stop_frac:
        raise ValueError(
            f"lantai yang diberikan pemanggil {a.min_median_stop_frac} berselisih "
            f"dengan config {kunci['min_median_stop_frac']}"
        )

    if "4h" not in DATASET:
        raise ValueError("dataset H-015 wajib menyebut kerangka 4h")
    if LOOKBACK != list(LOOKBACK_H007):
        raise ValueError("lookback H-015 wajib identik dengan H-007")
    for p in kandidat():
        if KUNCI_TERLARANG in p:
            raise ValueError(f"{KUNCI_TERLARANG} bocor ke ruang pencarian")
        if "pakai_target" in p or "maks_umur_bar" in p:
            raise ValueError("geometri keluar tidak boleh dilombakan (ADR-020)")

    # ADR-037 §10. Ambang yang bergeser sesudah hasil terlihat adalah cacat yang
    # tidak meninggalkan jejak, jadi jejaknya dibuat di sini.
    if (AMBANG_RATE, MIN_PENAGIHAN, SEED_ACAK_H015) != (0.0001, 30, 20260727):
        raise ValueError(
            f"ambang H-015 bergeser dari ADR-037: rate {AMBANG_RATE}, "
            f"penagihan {MIN_PENAGIHAN}, seed {SEED_ACAK_H015}"
        )

    contoh = {"lookback": 55, "imbalan_R": IMBALAN_BEKU}
    konfig_sel = {s: buat_konfig_h015(contoh, dasar) for s in NAMA_SEL}

    # Ketiga sel WAJIB berkonfig identik. Bila tidak, selisih F - A akan memuat
    # perbedaan mesin alih-alih perbedaan informasi.
    for s in NAMA_SEL[1:]:
        beda = selisih_konfig(konfig_sel[s], konfig_sel[NAMA_SEL[0]])
        if beda:
            raise ValueError(
                f"konfig sel {s} berselisih dari sel {NAMA_SEL[0]}: {beda}; "
                "yang boleh membedakan sel hanyalah fungsi sinyalnya"
            )

    # Pembanding dibangun oleh kode H-013 SENDIRI, tidak diketik ulang.
    konfig_pendahulu = buat_konfig_sel("SS")(contoh, dasar_riset(mentah))

    audit = {
        s: laporan_kesebandingan(
            f"H-015-{s}",
            konfig_sel[s],
            NAMA_PENDAHULU,
            konfig_pendahulu,
            PENGAMAN_WAJIB,
        )
        for s in NAMA_SEL
    }

    print(f"H-015 tiga sel: {list(NAMA_SEL)}", flush=True)
    for s in NAMA_SEL:
        for baris in audit[s]["prosa"]:
            print(f"  [{s}] {baris}", flush=True)

    menghalangi = [s for s in NAMA_SEL if audit[s]["menghalangi"]]
    if menghalangi:
        # Inilah kewajiban ketiga ADR-037 §7, dan inilah yang tidak ada di
        # H-014. Kode 3 dibedakan dari kode 2 supaya sebab berhentinya terbaca
        # dari log CI tanpa membuka laporan.
        print(
            "DIHENTIKAN: pengaman mati pada sel "
            + ", ".join(menghalangi)
            + ". H-014 berjalan sampai selesai dalam keadaan seperti ini dan "
            "hasilnya tidak dapat dipakai (ADR-036).",
            flush=True,
        )
        return 3

    jen = jendela_bar(a.interval)
    butuh = bar_dibutuhkan(a.interval)

    print(f"pengaman dituntut: {PENGAMAN_WAJIB}", flush=True)
    print(
        f"saringan: ambang rate {AMBANG_RATE}, minimum penagihan "
        f"{MIN_PENAGIHAN}, jendela {JENDELA_HARI} hari, seed acak "
        f"{SEED_ACAK_H015} (semuanya beku, ADR-037)",
        flush=True,
    )
    print(
        f"jendela {a.interval}: latih {jen['panjang_latih']}, uji "
        f"{jen['panjang_uji']}, embargo {jen['embargo']}, pemanasan "
        f"{PEMANASAN} bar TIDAK dikonversi; satu jendela menuntut {butuh} bar",
        flush=True,
    )
    print(
        "KONSEKUENSI KONSTRUKSI (bukan temuan): lookahead DIJAMIN gagal pada "
        "sel A. Pada sel F ia TIDAK dimaklumi — saringannya hanya membaca masa "
        "lalu, jadi bila ia jatuh di F, yang jatuh adalah kodenya.",
        flush=True,
    )
    print(
        "MENGIKAT hanya F \u2212 A. Selisih F \u2212 K dicetak dan HARAM dipakai "
        "sebagai dasar kelulusan.",
        flush=True,
    )
    for nama, isi_ramalan in RAMALAN.items():
        print(f"  ramalan {nama}: {isi_ramalan}", flush=True)

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

    # Spek dibangun SESUDAH konteks, sebab saringan butuh jadwal funding.
    ktx = muat_konteks(opsi, dasar)

    hasil_sel: dict[str, dict] = {}
    for s in NAMA_SEL:
        print(f"\n### SEL {s}: {NAMA_LAPORAN[s]}", flush=True)
        hasil_sel[s] = jalankan_spek(
            spek_sel(s, ktx.jadwal, dasar, a.komit), ktx, dasar, opsi
        )
        print(
            f"sel {s}: {hasil_sel[s]['jumlah_jendela']} jendela, "
            f"{hasil_sel[s]['trade']} trade luar sampel "
            f"(ambang ternilai {MIN_TRADE_SEL}); "
            f"alasan keluar {hasil_sel[s]['alasan_keluar']}",
            flush=True,
        )

    ringkas = kontribusi_h015(
        {s: hasil_sel[s]["ekspektasi_R"] for s in NAMA_SEL},
        {s: hasil_sel[s]["trade"] for s in NAMA_SEL},
    )

    isi = {
        "hipotesis": "H-015",
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
            }
            for s in NAMA_SEL
        },
        # Kewajiban kedua ADR-037 \u00a77: seluruh medan Konfig ikut, tanpa disaring.
        # Manifes H-014 mencatat sebelas butir yang dianggap penting, dan medan
        # yang hilang justru medan yang tidak dianggap penting siapa pun.
        "audit_konfig": audit,
        "pengaman_wajib": PENGAMAN_WAJIB,
        "kontribusi": ringkas,
        "pembatas_putusan": PEMBATAS_PUTUSAN,
        "parameter_beku": {
            "ambang_rate": AMBANG_RATE,
            "min_penagihan": MIN_PENAGIHAN,
            "jendela_funding_hari": JENDELA_HARI,
            "seed_acak": SEED_ACAK_H015,
            "imbalan_R": IMBALAN_BEKU,
            "maks_umur_bar": H_BAR,
            "lookback": LOOKBACK,
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
    (out / "h015_run.json").write_text(
        json.dumps(isi, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    strip = "\u2014"

    def angka(x, fmt="+.6f"):
        return strip if x is None else format(x, fmt)

    md = [
        "# H-015 \u2014 informasi funding atau kecondongan arah?",
        "",
        "Yang mengikat hanya **F \u2212 A**. Sel K adalah kontrol dan selisih "
        "terhadapnya **tidak mengikat dalam bentuk apa pun**.",
        "",
        "| Sel | Peran | Jendela | Trade | Ekspektasi R | p acak | Gerbang gagal |",
        "|---|---|---|---|---|---|---|",
    ]
    peran_md = {
        "K": "kontrol",
        "F": "saringan funding",
        "A": "penolakan acak setara",
    }
    for s in NAMA_SEL:
        b = isi["sel"][s]
        md.append(
            f"| {s} | {peran_md[s]} | {b['jumlah_jendela']:,} | {b['trade']:,} "
            f"| {angka(b['ekspektasi_R'])} | {angka(b['p_entri_acak'], '.4f')} "
            f"| {', '.join(b['gerbang_gagal']) or strip} |"
        )
    md += [
        "",
        "## Dua selisih",
        "",
        f"- **MENGIKAT** F \u2212 A: **{angka(ringkas['selisih_mengikat_F_A_R'])}R** "
        f"terhadap ambang {AMBANG_KONTRIBUSI_SINYAL}R",
        f"- TIDAK mengikat F \u2212 K: {angka(ringkas['selisih_TIDAK_mengikat_F_K_R'])}R",
        "",
        f"**{'LULUS besaran' if ringkas['lulus'] else ('TIDAK DAPAT DINILAI' if not ringkas['dapat_dinilai'] else 'GAGAL besaran')}**",
        "",
        "## Bacaan angka",
        "",
    ]
    md += prosa_h015(ringkas)

    (out / "h015_run.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print("", flush=True)
    print(json.dumps(ringkas, indent=2, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
