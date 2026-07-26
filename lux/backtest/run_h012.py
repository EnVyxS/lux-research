"""H-012 — apakah keunggulan ada pada periode waktu yang belum pernah dipakai.

H-012 BUKAN "H-010 SETELAH PERBAIKAN"
-------------------------------------
Penamaan itu dilarang, dan bukan karena selera. H-010 **tidak** direhabilitasi:
ketika mekanismenya dijalankan dengan 300 permutasi, p entri acaknya 0,0631,
yakni **gagal** terhadap ambang 0,05 yang tidak pernah bergerak. Kelulusan
H-010 pada 100 permutasi (p 0,049505) berjarak tepat satu satuan resolusi dari
kegagalan, dan resolusi yang lebih baik menjatuhkannya. Angka +0,060163R yang
muncul bila USDCUSDT dibuang dari laporan H-011 **haram** dipakai sebagai
kelulusan apa pun: ia adalah hasil membuang satu simbol setelah melihat
hasilnya, yaitu tepat perbuatan yang dilarang ADR-013 bagian 8.

Jadi mekanisme di sini diperlakukan sebagai mekanisme yang **belum terbukti
sama sekali**, dan H-012 adalah pertanyaan baru pada dimensi yang belum pernah
dipakai memilih apa pun.

APA YANG DIUBAH, DAN MENGAPA HANYA ITU
--------------------------------------
1. **Definisi semesta diperbaiki lebih dulu.** Yang cacat pada H-011 bukan
   mesin dan bukan sinyal, melainkan definisi semesta: kriteria kelayakan tidak
   menyentuh volatilitas sama sekali, sehingga USDCUSDT — sebuah pasangan
   stablecoin dengan ATR/harga praktis nol — lolos, lalu satu perdagangannya
   menagih 312,73R dan gerbang ``invarian_risiko`` melaporkan -470,06R. Satuan R
   berhenti bermakna ketika jarak stop mendekati nol, karena setiap biaya
   dinyatakan dengan MEMBAGI jarak itu. Lantai median ``stop_frac`` 0,004
   memperbaiki definisinya untuk simbol mana pun, termasuk yang belum ada hari
   ini.
2. **Pengaman mesin 0,5R** menolak entri yang biaya bolak-baliknya melebihi
   separuh satuan risiko. Ia pasangan aritmetika dari lantai di atas, bukan
   angka kedua yang berdiri sendiri.
3. **Kriteria dinilai pada periode waktu tertahan**, sejak 2026-01-01 UTC.

MEKANISMENYA TIDAK BERUBAH SAMA SEKALI. Grid, sinyal, konfig per kandidat, dan
pengaman carry diimpor apa adanya dari H-010 dan H-009, dan modul ini menolak
berjalan bila salah satunya berbeda — alasan yang sama seperti H-011: bila
mekanisme ikut berubah, perubahan hasil tidak dapat dipisahkan dari penyebabnya.

MENGAPA WAKTU, DAN SEJUJUR APA IA BERSIH
----------------------------------------
Himpunan simbol tertahan sudah habis: H-011 memperlihatkan hasil per simbol
untuk seluruh 438 simbol, jadi tidak ada lagi simbol yang belum disentuh.
Dimensi yang tersisa hanya waktu dan kerangka 4h. Karena itu kriteria utama
H-012 adalah ekspektasi pada periode waktu terakhir.

Batas kejujuran yang wajib ikut tercetak: periode ini **tidak** sebersih himpunan
simbol tertahan sebelum H-011. Riwayat yang sudah dilihat memuat periode
terakhir di dalam agregatnya. Yang belum pernah dilihat adalah periode terakhir
**sebagai angkanya sendiri**. Klaim "data ini belum pernah disentuh" tidak sah;
yang sah hanyalah "angka ini belum pernah dilihat terpisah". Kelemahan itu
ditulis di sini supaya ia tidak hilang ketika laporannya dibaca setahun
kemudian.

Batasnya dibekukan sebagai TANGGAL KALENDER, bukan "n hari terakhir": batas
bergulir bergeser setiap kali data bertambah, dan batas yang bergeser bukan
batas. Tanggalnya dipilih sekarang, sebelum satu angka hasil pun dilihat.

RAMALAN SAYA: H-012 GAGAL. Ekspektasi periode tahan diramalkan 0,010-0,045,
di bawah ambang 0,05 yang tidak bergerak.

Pemakaian:
    python -m lux.backtest.run_h012 --dir aset --limit 0 --ulangan 300
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path
from typing import Iterable

import yaml

from lux.analisis.periode import bulan_dari_ms, ms_dari_tanggal
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
from lux.degenerasi import AMBANG_BIAYA_MASUK_R, AMBANG_MIN_STOP_FRAC
from lux.praregistrasi import Hipotesis, Kriteria
from lux.strategi import breakout_atr

NAMA = "h012_periode_tertahan"

# Batas periode tahan-waktu, DIBEKUKAN sebelum satu angka hasil dilihat.
# Tanggal kalender, bukan jendela bergulir: "180 hari terakhir" bergeser setiap
# kali data bertambah dan karena itu bukan batas.
PERIODE_TAHAN_TANGGAL = "2026-01-01"
PERIODE_TAHAN_MS = ms_dari_tanggal(PERIODE_TAHAN_TANGGAL)
PERIODE_TAHAN_BULAN = bulan_dari_ms(PERIODE_TAHAN_MS)

# Berapa banyak simbol yang boleh dibuang lantai sebelum H-012 kehilangan
# maknanya. ADR-014 meramalkan 1-6 simbol tersingkir. Bila lebih dari 20 yang
# jatuh, semesta yang diuji bukan lagi semesta yang dipra-registrasi, dan
# menilai hipotesis di atas semesta yang tak dikenali sama saja mengarang
# pertanyaan baru sesudah melihat data. Dalam keadaan itu H-012 DIBATALKAN,
# bukan dilonggarkan dan bukan pula dinilai diam-diam.
BATAS_VOID = 20

# Ukuran H-010 dan H-011, disalin dari laporan, tidak dijalankan ulang. Keduanya
# hadir sebagai KONTEKS, bukan sebagai pembanding kelulusan: H-010 gagal pada
# 300 permutasi, dan angka H-011 dihasilkan semesta yang definisinya cacat.
SEBELUMNYA = {
    "h010_ekspektasi_R": 0.05302836360569971,
    "h010_p_entri_acak_100_ulangan": 0.04950495049504951,
    "h010_p_entri_acak_300_ulangan": 0.0631,
    "h011_ekspektasi_R_semesta_penuh": -0.079078,
    "h011_invarian_risiko_R": -470.0611513462926,
    "h011_usdcusdt_stop_frac": 3.1984170825288993e-06,
}

# Tujuh ramalan ADR-014 bagian 8, ditulis sebelum run. Yang ketiga merugikan
# hipotesis ini sendiri.
RAMALAN = {
    "1_simbol_tersingkir": (
        f"1-6 simbol dibuang lantai; lebih dari {BATAS_VOID} berarti H-012 "
        "BATAL sebelum diadili"
    ),
    "2_ekspektasi_seluruh_riwayat": (
        "0,050-0,065; ini hanya pemeriksaan konsistensi terhadap H-010 dan "
        "HARAM dipakai sebagai bukti kelulusan, sebab seluruh riwayat sudah "
        "dipakai memilih segalanya sejak H-001b"
    ),
    "3_ekspektasi_periode_tahan": (
        "0,010-0,045, jadi DI BAWAH ambang 0,05 dan H-012 GAGAL — ini ramalan "
        "saya sendiri terhadap hipotesis saya sendiri"
    ),
    "4_p_entri_acak": (
        "0,01-0,20; p di atas 0,05 menjatuhkan H-012 MESKIPUN ekspektasinya "
        "tinggi, sebagaimana p 0,0631 menjatuhkan mekanisme ini di H-010"
    ),
    "5_entri_ditolak_pengaman": (
        "500-5.000 entri ditolak; tafsirnya SEMPIT karena simbol yang degenerat "
        "sepanjang riwayat menyumbang NOL penolakan — pengaman menolak juga "
        "saat pemilihan parameter sehingga seluruh jendelanya dilewati"
    ),
    "6_invarian_risiko": (
        "LULUS; bila ia masih gagal, lantai 0,004 belum menutup jalan masuk "
        "degenerasi dan seluruh ADR-014 keliru"
    ),
    "7_durasi": "10-60 menit",
}


def kunci_config(path: str | Path) -> dict:
    """Dua angka ADR-014 dari ``config/lux.yaml``.

    Dibaca dari berkas alih-alih diketik di sini, karena tajuk ``config/lux.yaml``
    menyatakan setiap angka yang memengaruhi hasil hidup di satu tempat yang
    perubahannya dijurnalkan. ``muat_konfig_h002`` tidak dapat dipakai untuk ini:
    modul ``run_h002`` dibekukan (aturan 7) dan tidak membaca kunci ADR-014.
    """
    cfg = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return {
        "min_median_stop_frac": float(cfg["universe"]["min_median_stop_frac"]),
        "maks_biaya_masuk_R": float(cfg["risiko"]["maks_biaya_masuk_R"]),
    }


def agregat_tahan(
    agregat_periode: Iterable[dict], mulai_bulan: str = PERIODE_TAHAN_BULAN
) -> dict:
    """Ekspektasi berbobot perdagangan pada periode tahan, dari laporan.

    Sumbernya blok ``agregat_periode`` di laporan yang baru ditulis, dan
    perbandingan bulannya leksikografis — sah karena bentuknya ``YYYY-MM``
    dengan nol di depan. Berbobot perdagangan, bukan rerata dari rerata bulanan:
    rerata dari rerata memberi bulan berisi selusin perdagangan bobot yang sama
    dengan bulan berisi ribuan, dan bulan tersepi hampir selalu bulan paling
    ekstrem.

    Berbeda dengan blok ``per_simbol``, ``total_R`` di sini **tidak** dibulatkan,
    jadi tidak ada galat pembulatan yang perlu diakui seperti pada H-011.
    """
    baris = [b for b in agregat_periode if b["periode"] >= mulai_bulan]
    trade = sum(int(b["trade"]) for b in baris)
    total = float(sum(float(b["total_R"]) for b in baris))
    return {
        "mulai_bulan": mulai_bulan,
        "n_bulan": len(baris),
        "trade": trade,
        "total_R": total,
        "ekspektasi_R": (total / trade) if trade else None,
        "dapat_dinilai": trade > 0,
        "sebab": "" if trade else "tidak ada perdagangan pada periode tahan",
    }


def agregat_sebelum(
    agregat_periode: Iterable[dict], mulai_bulan: str = PERIODE_TAHAN_BULAN
) -> dict:
    """Sisi seberang batas, yaitu periode yang sudah pernah dilihat.

    Bukan hiasan: tanpa pembanding, angka periode tahan tidak dapat dibedakan
    antara "keunggulan tidak bertahan di waktu" dan "seluruh semesta memburuk
    pada periode itu, termasuk di dalam sampel". Kedua tafsir menuntut tindakan
    berbeda.
    """
    baris = [b for b in agregat_periode if b["periode"] < mulai_bulan]
    trade = sum(int(b["trade"]) for b in baris)
    total = float(sum(float(b["total_R"]) for b in baris))
    return {
        "sebelum_bulan": mulai_bulan,
        "n_bulan": len(baris),
        "trade": trade,
        "total_R": total,
        "ekspektasi_R": (total / trade) if trade else None,
        "dapat_dinilai": trade > 0,
        "sebab": "" if trade else "tidak ada perdagangan sebelum periode tahan",
    }


def hipotesis_h012(konfig: Konfig, komit: str = "") -> Hipotesis:
    return Hipotesis(
        id="H-012",
        pernyataan=(
            "Seluruh pemilihan sejak H-001b memakai riwayat penuh 40 simbol "
            "pertama, dan H-011 menghabiskan himpunan simbol tertahan, "
            "sehingga satu-satunya dimensi yang belum pernah dipakai memilih "
            "apa pun adalah waktu. H-012 menjalankan mekanisme H-010 tanpa "
            "satu perubahan pun di atas semesta yang definisinya diperbaiki "
            "lebih dulu — lantai median stop_frac 0,004 dan pengaman biaya "
            "masuk 0,5R — lalu dinilai HANYA pada perdagangan yang dibuka "
            f"sejak {PERIODE_TAHAN_TANGGAL} UTC. Bila ekspektasi pada periode "
            "itu bertahan di atas 0,05R, keunggulan itu bukan sifat dari "
            "rentang waktu tertentu; bila ia jatuh, mekanisme ini tidak "
            "memiliki keunggulan yang bertahan dan wajib ditinggalkan. H-012 "
            "bukan rehabilitasi H-010, yang gagal dengan p 0,0631 pada 300 "
            "permutasi."
        ),
        dataset=DATASET,
        ruang_parameter={
            "lookback": list(LOOKBACK_H010),
            "imbalan_R": list(IMBALAN_H010),
            KUNCI_TERLARANG: [AMBANG_CARRY_KERAS],
            "semesta": [
                f"universe_layak_v2 dengan lantai median stop_frac "
                f"{AMBANG_MIN_STOP_FRAC}"
            ],
            "periode_dinilai": [f"sejak {PERIODE_TAHAN_TANGGAL} UTC"],
            "maks_biaya_masuk_R": [AMBANG_BIAYA_MASUK_R],
            "atr_pengali_stop": [konfig.atr_pengali_stop],
            "maks_umur_bar": [konfig.maks_umur_bar],
            "maks_carry_R": [konfig.maks_carry_R],
            "jendela_carry_hari": [konfig.jendela_carry_hari],
        },
        # Tidak dilonggarkan dan tidak diperketat. Keduanya sama-sama menyetel
        # ambang terhadap hasil yang sudah dilihat.
        kriteria=Kriteria(
            min_ekspektasi_R=0.05,
            min_trade_luar_sampel=100,
            maks_p_entri_acak=0.05,
            min_jendela_positif_rasio=0.5,
        ),
        komit=komit,
    )


def spek_h012(konfig: Konfig, komit: str = "") -> Spek:
    return Spek(
        h=hipotesis_h012(konfig, komit),
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

    # Seluruh pagar di bawah selesai dalam hitungan detik, sebelum satu bar pun
    # dimuat. Menaruh pemeriksaan yang bisa gagal di ujung run panjang berarti
    # membuang puluhan menit komputasi demi mengetahui hal yang sudah dapat
    # diketahui sekarang.
    if a.ulangan < 300:
        raise ValueError(
            "ulangan H-012 tidak boleh di bawah 300; pada 100 ulangan "
            "mekanisme ini memberi p 0,049505 dan pada 300 ulangan 0,0631 — "
            "resolusi rendah itulah yang dulu menyembunyikan kegagalannya"
        )

    kunci = kunci_config(a.config)

    # Tripwire angka kembar (aturan 10). Lantai dan pengaman hidup di dua
    # tempat: config/lux.yaml sebagai satu-satunya sumber angka, dan
    # lux/degenerasi.py sebagai turunan aritmetiknya. Bila keduanya berselisih,
    # salah satu sudah digeser tanpa dijurnalkan, dan run ini berhenti.
    if kunci["min_median_stop_frac"] != AMBANG_MIN_STOP_FRAC:
        raise ValueError(
            f"lantai di config ({kunci['min_median_stop_frac']}) tidak sama "
            f"dengan lux.degenerasi ({AMBANG_MIN_STOP_FRAC}); satu di antaranya "
            "digeser tanpa dijurnalkan"
        )
    if kunci["maks_biaya_masuk_R"] != AMBANG_BIAYA_MASUK_R:
        raise ValueError(
            f"pengaman di config ({kunci['maks_biaya_masuk_R']}) tidak sama "
            f"dengan lux.degenerasi ({AMBANG_BIAYA_MASUK_R})"
        )

    # Aritmetika yang melahirkan kedua angka, diperiksa dan tidak dipercayai
    # sebagai label (aturan 11): biaya bolak-balik 2*(fee+slippage) dibagi
    # lantai jarak stop harus tepat sama dengan pengaman.
    dasar = muat_konfig_h002(Path(a.config))
    bolak_balik = 2.0 * (dasar.fee_efektif + dasar.slippage)
    turunan = bolak_balik / AMBANG_MIN_STOP_FRAC
    if abs(turunan - AMBANG_BIAYA_MASUK_R) > 1e-12:
        raise ValueError(
            f"pengaman {AMBANG_BIAYA_MASUK_R}R bukan turunan dari lantai "
            f"{AMBANG_MIN_STOP_FRAC} pada biaya {bolak_balik}: "
            f"seharusnya {turunan}"
        )

    # run_h002 dibekukan dan tidak membaca kunci ADR-014, jadi pengaman
    # dipasang di sini lewat replace — bukan dengan menyunting modul beku.
    konfig = dataclasses.replace(
        dasar, maks_biaya_masuk_R=kunci["maks_biaya_masuk_R"]
    )

    if konfig.maks_biaya_masuk_R <= 0:
        raise ValueError("H-012 menuntut pengaman biaya masuk menyala")

    if konfig.maks_carry_R <= 0:
        raise ValueError("H-012 menuntut saringan ADR-004 tetap menyala")

    if AMBANG_CARRY_KERAS <= 0:
        raise ValueError("ambang carry keras wajib menyala di H-012")

    if hipotesis_h012(konfig).dataset != hipotesis_h002(konfig).dataset:
        raise ValueError("dataset H-012 tidak identik dengan H-002")

    # Mekanisme wajib identik dengan H-010. Bila grid ikut berubah, perubahan
    # hasil tidak dapat dipisahkan dari perubahan semesta dan periode.
    if list(LOOKBACK_H010) != [20, 55, 100]:
        raise ValueError("lookback H-010 bergeser; mekanisme H-012 tidak identik")

    if list(IMBALAN_H010) != [2.0, 4.0, 6.0, 8.0]:
        raise ValueError("imbalan H-010 bergeser; mekanisme H-012 tidak identik")

    if kandidat_h010() != [
        {"lookback": lb, "imbalan_R": im}
        for lb in LOOKBACK_H010
        for im in IMBALAN_H010
    ]:
        raise ValueError("kandidat H-012 tidak identik dengan H-010")

    if buat_konfig_h010 is not buat_konfig_h009:
        raise ValueError(
            "buat_konfig H-010 bukan lagi fungsi H-009; pematokan pengaman "
            "carry tidak lagi dijalankan kode yang sama"
        )

    for p in kandidat_h010():
        if KUNCI_TERLARANG in p:
            raise ValueError(f"{KUNCI_TERLARANG} bocor ke ruang pencarian")
        if "maks_biaya_masuk_R" in p:
            raise ValueError(
                "maks_biaya_masuk_R bocor ke ruang pencarian; batas risiko "
                "dipatok, tidak pernah dilombakan (ADR-009)"
            )

    opsi = Opsi(
        dir_aset=Path(a.dir),
        out=Path(a.out),
        interval=a.interval,
        universe=Path(a.universe),
        akhir_sejati=Path(a.akhir_sejati),
        limit=a.limit,
        ulangan=a.ulangan,
        min_median_stop_frac=kunci["min_median_stop_frac"],
    )

    print(
        f"H-012 periode tertahan: limit {a.limit}, ulangan {a.ulangan}, "
        f"lantai {opsi.min_median_stop_frac}, pengaman "
        f"{konfig.maks_biaya_masuk_R}R",
        flush=True,
    )
    print(
        f"periode tahan DIBEKUKAN sejak {PERIODE_TAHAN_TANGGAL} UTC "
        f"(bulan {PERIODE_TAHAN_BULAN}, ms {PERIODE_TAHAN_MS})",
        flush=True,
    )
    print(
        "H-012 BUKAN rehabilitasi H-010: mekanisme ini gagal dengan p "
        f"{SEBELUMNYA['h010_p_entri_acak_300_ulangan']} pada 300 permutasi",
        flush=True,
    )
    print(
        f"grid identik H-010: lookback {list(LOOKBACK_H010)}, "
        f"imbalan {list(IMBALAN_H010)}, {len(kandidat_h010())} kombinasi",
        flush=True,
    )
    for nama, isi in RAMALAN.items():
        print(f"  ramalan {nama}: {isi}", flush=True)

    ktx = muat_konteks(opsi, konfig)

    if ktx.saringan is None:
        raise ValueError(
            "lantai semesta tidak menyala padahal H-012 mensyaratkannya"
        )

    n_ditolak = int(ktx.saringan["n_ditolak"])
    print(
        f"lantai membuang {n_ditolak} simbol (batas void {BATAS_VOID})",
        flush=True,
    )
    if n_ditolak > BATAS_VOID:
        print(
            f"H-012 BATAL: {n_ditolak} simbol dibuang lantai, lebih dari "
            f"{BATAS_VOID}. Semesta yang tersisa bukan lagi semesta yang "
            "dipra-registrasi, jadi menilai hipotesis di atasnya sama dengan "
            "mengarang pertanyaan baru sesudah melihat data. Yang wajib "
            "dilakukan adalah ADR baru tentang definisi semesta, BUKAN "
            "menurunkan lantai dan bukan menaikkan batas void.",
            flush=True,
        )
        return 2

    if not ktx.bingkai:
        raise ValueError("tidak ada simbol tersisa sesudah lantai")

    hasil = jalankan_spek(spek_h012(konfig, a.komit), ktx, konfig, opsi)

    # Kriteria utama dihitung dari laporan yang baru ditulis, bukan dari nilai
    # yang beredar di memori, supaya angka yang diadjudikasi adalah angka yang
    # benar-benar dikomit ke repo dan dapat diperiksa tangan siapa pun.
    laporan = json.loads(
        (Path(a.out) / f"backtest_{NAMA}.json").read_text(encoding="utf-8")
    )
    periode = laporan["agregat_periode"]
    tahan = agregat_tahan(periode)
    lama = agregat_sebelum(periode)

    print("", flush=True)
    print("=== KRITERIA UTAMA ADR-014: PERIODE WAKTU TERTAHAN ===", flush=True)
    print(
        f"tahan (sejak {PERIODE_TAHAN_BULAN}): {tahan['n_bulan']} bulan, "
        f"{tahan['trade']:,} trade, total {tahan['total_R']:.2f}R, "
        f"ekspektasi {tahan['ekspektasi_R']}",
        flush=True,
    )
    print(
        f"sebelum: {lama['n_bulan']} bulan, {lama['trade']:,} trade, "
        f"total {lama['total_R']:.2f}R, ekspektasi {lama['ekspektasi_R']}",
        flush=True,
    )
    if tahan["dapat_dinilai"] and lama["dapat_dinilai"]:
        print(
            f"selisih tahan - sebelum: "
            f"{tahan['ekspektasi_R'] - lama['ekspektasi_R']:+.6f}R",
            flush=True,
        )
    if tahan["dapat_dinilai"]:
        ambang = hipotesis_h012(konfig).kriteria.min_ekspektasi_R
        cukup_trade = tahan["trade"] >= 100
        lulus_utama = tahan["ekspektasi_R"] >= ambang and cukup_trade
        print(
            f"kriteria utama terhadap {ambang}R dengan minimal 100 trade: "
            f"{'LULUS' if lulus_utama else 'GAGAL'} "
            f"(ramalan saya: GAGAL, 0,010-0,045)",
            flush=True,
        )
        if not cukup_trade:
            print(
                "periode tahan tidak memenuhi 100 perdagangan: itu TIDAK DAPAT "
                "DINILAI, bukan lulus dan bukan gagal karena sinyal",
                flush=True,
            )
    else:
        print(f"kriteria utama TIDAK DAPAT DINILAI: {tahan['sebab']}", flush=True)

    print(
        "catatan kejujuran: periode ini tidak sebersih himpunan simbol "
        "tertahan sebelum H-011. Riwayat yang sudah dilihat memuat periode ini "
        "di dalam agregatnya; yang belum pernah dilihat adalah angkanya secara "
        "terpisah. Perdagangan yang dibuka sesaat sebelum batas dapat ditutup "
        "sesudahnya, dan rembesan itu terbatas oleh maks_umur_bar "
        f"({konfig.maks_umur_bar} bar).",
        flush=True,
    )

    print("", flush=True)
    print(f"putusan seluruh kumpulan: {hasil['lulus']}", flush=True)
    print(
        f"ekspektasi seluruh riwayat: {hasil['ekspektasi_R']} "
        f"(H-010 {SEBELUMNYA['h010_ekspektasi_R']}; angka ini HANYA "
        "pemeriksaan konsistensi, bukan bukti)",
        flush=True,
    )
    print(f"trade: {hasil['trade']:,}", flush=True)
    print(
        f"p entri acak: {hasil['p_entri_acak']} "
        f"(mekanisme ini: {SEBELUMNYA['h010_p_entri_acak_300_ulangan']} "
        "pada 300 permutasi di H-010)",
        flush=True,
    )
    print(f"entri ditolak pengaman: {hasil.get('entri_ditolak_biaya')}", flush=True)
    print(f"simbol dibuang lantai: {hasil.get('simbol_dibuang_lantai')}", flush=True)
    print(f"bulan dengan trade: {hasil.get('bulan_dengan_trade')}", flush=True)
    print(f"retensi drop-1: {hasil.get('retensi_drop_1')}", flush=True)
    print(f"galat baku: {hasil.get('galat_baku_R')}", flush=True)
    print(f"jarak ke ambang dalam galat baku: {hasil.get('jarak_galat_baku')}", flush=True)
    print(f"gerbang gagal: {hasil['gerbang_gagal']}", flush=True)
    print(f"durasi: {hasil['detik']}s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
