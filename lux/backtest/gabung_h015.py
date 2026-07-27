"""Adjudikasi H-015: selisih F - A pada satuan bulan, dengan LULUS yang dibatasi.

Modul ini membaca ``reports/h015_run.json`` beserta laporan sel F dan A yang
ditulis ``runner.jalankan_spek``, lalu menjatuhkan putusan menurut ADR-037 pasal
5. Aritmetika pemasangan, uji tanda, dan bootstrap **tidak** ada di sini:
seluruhnya milik ``lux.analisis.berpasangan``, modul daun yang sudah diuji.
Aritmetika yang hanya hidup di dalam ``main`` tidak pernah benar-benar diuji,
dan itulah sebab dua cacat sebelumnya tidak berbunyi berbulan-bulan (aturan 32).

TEGANGAN YANG DIDAMAIKAN DI SINI, BUKAN DISEMBUNYIKAN
-----------------------------------------------------
``berpasangan.PEMBATAS`` menyatakan, verbatim, bahwa p-nya "sah dipakai untuk
MENJATUHKAN klaim selisih antar sel, dan tidak sah dipakai untuk
MENEGAKKANNYA", dan ``ringkas`` memancarkan ``memenuhi_adr015: False`` tanpa
syarat. Karena itulah ``gabung_h014`` tidak punya cabang LULUS sama sekali.
Namun ADR-037 pasal 5 menuntut ``PUTUSAN_MUNGKIN`` bertiga.

Keduanya dapat benar sekaligus hanya bila arti LULUS dipersempit dan
dipersempit di dalam kode, bukan di dalam prosa laporan:

**LULUS = lulus kriteria pra-registrasi ADR-037 pasal 5.** Ia BUKAN kelulusan
ADR-015 pasal 4.4, sebab p yang dipakai berasal dari penarikan bulan kalender
UTC (ADR-028), bukan dari sebaran permutasi sinyal. Medan ``memenuhi_adr015``
karena itu tetap ``False`` bahkan pada cabang LULUS, dan pengujian mengunci hal
itu. Bila pembedaan ini tidak dikodekan, "LULUS" H-015 akan dibaca sebagai
kelulusan ADR-015 oleh siapa pun yang membaca cepat -- yaitu cacat kelas 9
dengan baju baru.

TIGA HAL YANG DIAMBIL DARI KODE, BUKAN DARI PRESEDEN H-014
-----------------------------------------------------------
**1. Trade tipis menghasilkan TIDAK DAPAT DINILAI, bukan DITOLAK.** Ini sengaja
berbeda dari ``gabung_h014``, yang menjadikannya DITOLAK.
``run_h015.kontribusi_h015`` menyatakan aturannya sendiri: "Sel yang perdagangan
luar sampelnya kurang dari MIN_TRADE_SEL membuat seluruh perbandingan TIDAK
DAPAT DINILAI, bukan membuatnya gagal." Modul H-015 yang mengikat H-015, bukan
preseden hipotesis sebelumnya. Sel F yang tipis adalah hasil yang sangat mungkin
di sini: saringan yang menolak hampir seluruh long dapat menyisakan terlalu
sedikit perdagangan untuk dinilai, dan keadaan itu wajib berbunyi alih-alih
dilaporkan sebagai angka.

**2. ``lookahead`` yang gagal pada sel A dimaklumi; pada sel F tidak.**
Penolakan acak bergantung pada cacah per bulan di seluruh potongan, sedangkan
gerbang itu memotong bingkai lalu menuntut sinyal awal tidak berubah. Menurut
aturan 36 itu konsekuensi konstruksi, bukan temuan. Menuntut ``gerbang_gagal``
kosong pada ketiga sel akan membuat H-015 mustahil dinilai selamanya. Saringan
sel F hanya membaca masa lalu, jadi bila ``lookahead`` jatuh di F, yang jatuh
adalah kodenya, dan tidak ada pemakluman.

**3. Nama gerbang divalidasi terhadap ``gerbang.NAMA_GERBANG`` saat impor.**
Pemakluman yang salah eja tidak akan menempel pada apa pun, dan kesalahannya
baru terlihat empat jam kemudian dalam bentuk "TIDAK DAPAT DINILAI". Pagar yang
mengutip nama dari ingatan penulisnya tidak menjaga apa pun (aturan 31).

AMBANG TIDAK DIKETIK ULANG DI SINI
----------------------------------
Seluruh ambang diserahkan pemanggil sebagai argumen wajib, persis seperti
``gabung_h014``. Ambang yang diketik ulang di modul adjudikasi adalah ambang
yang dapat bergeser tanpa meninggalkan jejak di ADR mana pun.

KODE KELUAR
-----------
``0`` DITOLAK **dan** LULUS -- keduanya adalah adjudikasi yang **berhasil**
diperoleh, dan hasil yang mematikan hipotesis tidak boleh menyamar sebagai run
gagal (aturan 48). ``4`` TIDAK DAPAT DINILAI. ``2`` pagar pra-terbang.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from lux.analisis.berpasangan import (
    PEMBATAS as PEMBATAS_BERPASANGAN,
    SEED,
    ULANGAN,
    pasangan_bulan,
    ringkas,
)
from lux.backtest.gerbang import NAMA_GERBANG

NAMA = "h015_berpasangan"

LULUS = "LULUS"
DITOLAK = "DITOLAK"
TIDAK_DAPAT_DINILAI = "TIDAK DAPAT DINILAI"
PUTUSAN_MUNGKIN = (LULUS, DITOLAK, TIDAK_DAPAT_DINILAI)

# Lantai pasangan adalah lantai modul yang dipakai, bukan angka baru: uji_tanda
# dan bootstrap keduanya menuntut minimal dua pasang.
MIN_PASANGAN = 2

# Sel yang selisihnya mengikat, berurutan: yang pertama dikurangi yang kedua.
SEL_MENGIKAT = ("F", "A")
SEL_KONTROL = "K"

# Aturan 36. Hanya sel A, dan hanya gerbang ini.
GERBANG_DIMAKLUMI: dict[str, tuple[str, ...]] = {"A": ("lookahead",)}

_TAK_DIKENAL = sorted(
    {g for daftar in GERBANG_DIMAKLUMI.values() for g in daftar} - set(NAMA_GERBANG)
)
if _TAK_DIKENAL:  # pragma: no cover - pagar impor
    raise ValueError(
        f"gerbang dimaklumi tidak ada di NAMA_GERBANG: {_TAK_DIKENAL}. "
        "Pemakluman yang salah eja tidak menempel pada apa pun dan baru "
        "terlihat sesudah run empat jam selesai."
    )

KUNCI_RUN_WAJIB = ("sel", "audit_konfig", "parameter_beku")

PEMBATAS = (
    "Putusan H-015 dapat LULUS, DITOLAK, atau TIDAK DAPAT DINILAI. LULUS di "
    "sini berarti LULUS KRITERIA PRA-REGISTRASI ADR-037 pasal 5, dan BUKAN "
    "kelulusan ADR-015 pasal 4.4: p yang dipakai berasal dari penarikan bulan "
    "kalender UTC (ADR-028), bukan dari sebaran permutasi sinyal, sehingga "
    "medan memenuhi_adr015 tetap False bahkan pada cabang LULUS. Yang mengikat "
    "hanya F - A. Selisih F - K ikut dicetak dan HARAM dipakai sebagai dasar "
    "kelulusan: funding positif pada 79,1% periode membuat saringan apa pun "
    "mengalahkan kontrol tanpa memuat setitik pun informasi. Angka +0,029481R "
    "milik H-014 bukan pembanding H-015 dalam bentuk apa pun."
)


def muat_sel(jalur: Path | str) -> dict:
    """Baca satu laporan sel dan tuntut medan yang benar-benar dipakai."""
    p = Path(jalur)
    if not p.exists():
        raise FileNotFoundError(f"laporan sel {p} tidak ada")
    isi = json.loads(p.read_text(encoding="utf-8"))
    if "agregat_periode" not in isi:
        raise ValueError(
            f"{p} tanpa medan agregat_periode; R per bulan tidak dapat diambil "
            "dari mana pun selain berkas ini"
        )
    if not isinstance(isi["agregat_periode"], list):
        raise ValueError(f"agregat_periode di {p} bukan daftar")
    return isi


def muat_run(jalur: Path | str) -> dict:
    """Baca ``h015_run.json``; tiga dari enam kriteria ADR-037 hidup di sana."""
    p = Path(jalur)
    if not p.exists():
        raise FileNotFoundError(f"laporan run {p} tidak ada")
    isi = json.loads(p.read_text(encoding="utf-8"))
    kurang = [k for k in KUNCI_RUN_WAJIB if k not in isi]
    if kurang:
        raise ValueError(
            f"{p} tanpa medan {kurang}; tanpa medan itu kriteria pengaman, "
            "ulangan, dan gerbang tidak dapat diperiksa sama sekali"
        )
    return isi


def trade_sel(isi: dict) -> int:
    """Jumlah perdagangan luar sampel satu sel."""
    return int(isi.get("gabungan", {}).get("jumlah_trade_luar_sampel", 0) or 0)


def pengaman_mati(run: dict) -> dict[str, list[str]]:
    """Sel yang pengaman wajibnya tidak menyala. Kosong berarti bersih."""
    audit = run.get("audit_konfig") or {}
    keluar: dict[str, list[str]] = {}
    for s in sorted(audit):
        mati = sorted(audit[s].get("pengaman_mati") or [])
        if mati:
            keluar[s] = mati
    return keluar


def gerbang_gagal_tak_dimaklumi(run: dict) -> dict[str, list[str]]:
    """Gerbang gagal, sesudah pemakluman aturan 36 dikurangkan."""
    sel = run.get("sel") or {}
    keluar: dict[str, list[str]] = {}
    for s in sorted(sel):
        gagal = list(sel[s].get("gerbang_gagal") or [])
        dimaklumi = set(GERBANG_DIMAKLUMI.get(s, ()))
        sisa = sorted(g for g in gagal if g not in dimaklumi)
        if sisa:
            keluar[s] = sisa
    return keluar


def ulangan_run(run: dict) -> int | None:
    """Cacah ulangan permutasi yang sungguh dipakai run, bukan yang diniatkan."""
    v = (run.get("parameter_beku") or {}).get("ulangan")
    return None if v is None else int(v)


def adjudikasi(
    isi_f: dict,
    isi_a: dict,
    run: dict,
    *,
    ambang_besaran: float,
    ambang_p: float,
    min_trade: int,
    min_ulangan: int,
    isi_k: dict | None = None,
    ulangan: int = ULANGAN,
    seed: int = SEED,
) -> dict:
    """Putusan H-015. Nilai kembaliannya SELALU salah satu ``PUTUSAN_MUNGKIN``.

    Besaran dilaporkan **dua kali** (aturan 49): rerata selisih bulanan dan
    selisih agregat. Keduanya tidak identik, dan menyebut hanya satu di
    antaranya adalah cara paling mudah membuat besaran terlihat lebih besar
    daripada seharusnya. Yang mengikat adalah rerata bulanan, sebab satuan
    penarikan H-015 adalah bulan kalender UTC (ADR-028); H-014 mati justru
    karena kedua angka itu berlawanan tanda (cacat kelas 16).
    """
    per_bulan = ringkas(
        pasangan_bulan(isi_f, isi_a), ambang_besaran, ulangan=ulangan, seed=seed
    )
    trade_f, trade_a = trade_sel(isi_f), trade_sel(isi_a)

    fk = None
    if isi_k is not None:
        fk = ringkas(
            pasangan_bulan(isi_f, isi_k), ambang_besaran, ulangan=ulangan, seed=seed
        )

    sebab: list[str] = []
    tak_dapat: list[str] = []

    if per_bulan["hanya_a"] or per_bulan["hanya_b"]:
        tak_dapat.append(
            f"himpunan bulan tidak sama: hanya di F {per_bulan['hanya_a']}, "
            f"hanya di A {per_bulan['hanya_b']}"
        )
    if per_bulan["tanpa_nilai"]:
        tak_dapat.append(
            f"bulan tanpa ekspektasi di salah satu sel: {per_bulan['tanpa_nilai']}"
        )
    if per_bulan["n_pasangan"] < MIN_PASANGAN:
        tak_dapat.append(f"pasangan bulan {per_bulan['n_pasangan']} < {MIN_PASANGAN}")

    # Trade tipis TIDAK menjatuhkan hipotesis; ia membuat perbandingan tidak
    # ada. Ini sengaja berbeda dari gabung_h014, mengikuti pernyataan
    # run_h015.kontribusi_h015.
    for nama, n in (("F", trade_f), ("A", trade_a)):
        if n < int(min_trade):
            tak_dapat.append(
                f"trade sel {nama} {n} < {min_trade}: perbandingan tidak dapat "
                "dinilai, bukan gagal"
            )

    mati = pengaman_mati(run)
    if mati:
        tak_dapat.append(
            f"pengaman wajib mati pada sel {mati}; H-014 berjalan sampai selesai "
            "dalam keadaan seperti ini dan hasilnya tidak dapat dipakai (ADR-036)"
        )

    n_ulangan = ulangan_run(run)
    if n_ulangan is None or n_ulangan < int(min_ulangan):
        tak_dapat.append(
            f"ulangan permutasi run {n_ulangan!r} < {min_ulangan}; ambang ADR-015 "
            "tidak bergerak"
        )

    gerbang = gerbang_gagal_tak_dimaklumi(run)
    if gerbang:
        tak_dapat.append(
            f"gerbang gagal tanpa pemakluman: {gerbang}. Gerbang ada supaya "
            "angkanya tidak dipercaya, jadi angkanya tidak dipakai untuk "
            "menjatuhkan maupun menegakkan apa pun"
        )

    besaran_bulanan = per_bulan.get("rerata_selisih")
    besaran_agregat = per_bulan.get("selisih_agregat")
    p = (per_bulan.get("uji_tanda") or {}).get("p")

    if not tak_dapat:
        if besaran_bulanan is None or besaran_bulanan < float(ambang_besaran):
            sebab.append(
                f"rerata selisih bulanan F - A {besaran_bulanan!r} < "
                f"{ambang_besaran}R"
            )
        if p is None or p > float(ambang_p):
            sebab.append(f"p uji tanda bulanan {p!r} > {ambang_p}")

    if tak_dapat:
        putusan, alasan = TIDAK_DAPAT_DINILAI, tak_dapat
    elif sebab:
        putusan, alasan = DITOLAK, sebab
    else:
        putusan, alasan = (
            LULUS,
            [
                f"rerata selisih bulanan F - A {besaran_bulanan!r} >= "
                f"{ambang_besaran}R dan p {p!r} <= {ambang_p} atas "
                f"{per_bulan['n_pasangan']} bulan kalender UTC, dengan seluruh "
                "pengaman menyala dan tanpa gerbang gagal yang tak dimaklumi.",
                "LULUS ini adalah kelulusan KRITERIA PRA-REGISTRASI ADR-037 "
                "pasal 5. Ia BUKAN kelulusan ADR-015 pasal 4.4: p di sini "
                "mengukur penarikan bulan, bukan permutasi sinyal, sehingga "
                "memenuhi_adr015 tetap False.",
                "Ia juga BUKAN pernyataan bahwa sistem siap diperdagangkan.",
            ],
        )

    assert putusan in PUTUSAN_MUNGKIN
    return {
        "hipotesis": "H-015",
        "putusan": putusan,
        "alasan": alasan,
        "besaran_rerata_bulanan_R": besaran_bulanan,
        "besaran_agregat_R": besaran_agregat,
        "catatan_besaran": (
            "Dua besaran dilaporkan sebab keduanya tidak identik (aturan 49). "
            "Yang MENGIKAT adalah rerata bulanan, sebab satuan penarikan H-015 "
            "adalah bulan kalender UTC (ADR-028). H-014 mati dengan kedua angka "
            "ini berlawanan tanda, dan itu tercatat sebagai cacat kelas 16."
        ),
        "p": p,
        "ambang_besaran_R": float(ambang_besaran),
        "ambang_p": float(ambang_p),
        "min_trade_sel": int(min_trade),
        "min_ulangan": int(min_ulangan),
        "ulangan_run": n_ulangan,
        "trade_F": trade_f,
        "trade_A": trade_a,
        "pengaman_mati": mati,
        "gerbang_gagal_tak_dimaklumi": gerbang,
        "gerbang_dimaklumi": {k: list(v) for k, v in GERBANG_DIMAKLUMI.items()},
        "satuan_penarikan": "bulan",
        "per_bulan": per_bulan,
        "selisih_TIDAK_mengikat_F_K": (
            None if fk is None else fk.get("rerata_selisih")
        ),
        "catatan_F_K": (
            "Selisih F - K TIDAK MENGIKAT dalam bentuk apa pun dan haram "
            "dipakai sebagai dasar kelulusan."
        ),
        "putusan_mungkin": list(PUTUSAN_MUNGKIN),
        "memenuhi_adr015": False,
        "pembatas": PEMBATAS,
        "pembatas_berpasangan": PEMBATAS_BERPASANGAN,
    }


def tulis_laporan(hasil: dict, out: Path | str = "reports", nama: str = NAMA) -> dict:
    d = Path(out)
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{nama}.json").write_text(
        json.dumps(hasil, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    strip = "\u2014"
    fmt = lambda v: strip if v is None else f"{v:+.6f}"
    pb = hasil["per_bulan"]
    ut = pb.get("uji_tanda") or {}
    bs = pb.get("bootstrap") or {}
    md = [
        "# H-015 \u2014 informasi funding atau kecondongan arah?",
        "",
        f"> {hasil['pembatas']}",
        "",
        f"> {hasil['pembatas_berpasangan']}",
        "",
        "## Putusan",
        "",
        f"**{hasil['putusan']}**",
        "",
    ]
    md += [f"- {a}" for a in hasil["alasan"]] + [""]
    md += [
        "## Besaran, dilaporkan dua kali (aturan 49)",
        "",
        f"- Rerata selisih bulanan F - A (MENGIKAT): "
        f"**{fmt(hasil['besaran_rerata_bulanan_R'])}R**",
        f"- Selisih agregat F - A: **{fmt(hasil['besaran_agregat_R'])}R**",
        f"- Ambang besaran: {hasil['ambang_besaran_R']}R, dibekukan ADR-037 dan "
        "tidak digeser sesudah hasil terlihat (ADR-037 pasal 10).",
        "",
        hasil["catatan_besaran"],
        "",
        f"- Selisih F - K: **{fmt(hasil['selisih_TIDAK_mengikat_F_K'])}R** "
        f"\u2014 {hasil['catatan_F_K']}",
        "",
        "## Signifikansi pada satuan bulan (ADR-028)",
        "",
        f"- Pasangan bulan: **{pb.get('n_pasangan')}**",
        f"- p uji tanda: **{fmt(ut.get('p'))}** "
        f"({ut.get('ulangan')} ulangan, seed {ut.get('seed')}), ambang "
        f"{hasil['ambang_p']}",
        f"- Selang bootstrap 95%: **[{fmt(bs.get('bawah'))}, "
        f"{fmt(bs.get('atas'))}]R**",
        f"- Fraksi bulan positif: {pb.get('fraksi_positif')}",
        f"- Trade sel F / sel A: **{hasil['trade_F']:,}** / "
        f"**{hasil['trade_A']:,}**, lantai {hasil['min_trade_sel']}",
        f"- Ulangan permutasi run: **{hasil['ulangan_run']}**, lantai "
        f"{hasil['min_ulangan']}",
        f"- Pengaman mati: {hasil['pengaman_mati'] or 'tidak ada'}",
        f"- Gerbang gagal tanpa pemakluman: "
        f"{hasil['gerbang_gagal_tak_dimaklumi'] or 'tidak ada'}",
        f"- Gerbang dimaklumi (aturan 36): {hasil['gerbang_dimaklumi']}",
        "- Memenuhi ADR-015 pasal 4.4: **TIDAK**",
        "",
        "## Yang tidak dijawab laporan ini",
        "",
        "Bahkan pada cabang LULUS, laporan ini tidak menyatakan bahwa saringan "
        "funding memenuhi ADR-015 pasal 4.4, dan tidak menyatakan bahwa sistem "
        "siap diperdagangkan. Kelulusan ADR-015 menuntut sebaran nol permutasi "
        "sinyal atas minimal 300 seed; yang dihitung di sini adalah penarikan "
        "bulan kalender UTC.",
        "",
    ]
    (d / f"{nama}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return hasil


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Adjudikasi H-015 (ADR-037)")
    ap.add_argument("--run", required=True, help="JSON reports/h015_run.json")
    ap.add_argument("--sel-f", required=True, help="JSON laporan sel F")
    ap.add_argument("--sel-a", required=True, help="JSON laporan sel A")
    ap.add_argument("--sel-k", default="", help="JSON laporan sel K (tidak mengikat)")
    ap.add_argument("--ambang-besaran", type=float, required=True)
    ap.add_argument("--ambang-p", type=float, required=True)
    ap.add_argument("--min-trade", type=int, required=True)
    ap.add_argument("--min-ulangan", type=int, required=True)
    ap.add_argument("--ulangan", type=int, default=ULANGAN)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--out", default="reports")
    ap.add_argument("--nama", default=NAMA)
    a = ap.parse_args(argv)

    try:
        run = muat_run(a.run)
        isi_f = muat_sel(a.sel_f)
        isi_a = muat_sel(a.sel_a)
        isi_k = muat_sel(a.sel_k) if a.sel_k else None
    except (FileNotFoundError, ValueError) as e:
        print(f"DITOLAK pagar pra-terbang: {e}", flush=True)
        return 2

    hasil = adjudikasi(
        isi_f,
        isi_a,
        run,
        ambang_besaran=a.ambang_besaran,
        ambang_p=a.ambang_p,
        min_trade=a.min_trade,
        min_ulangan=a.min_ulangan,
        isi_k=isi_k,
        ulangan=a.ulangan,
        seed=a.seed,
    )
    tulis_laporan(hasil, out=a.out, nama=a.nama)
    print(json.dumps(hasil, indent=2, ensure_ascii=False), flush=True)
    print(f"\nPUTUSAN H-015: {hasil['putusan']}", flush=True)
    for al in hasil["alasan"]:
        print(f"  - {al}", flush=True)

    if hasil["putusan"] in (DITOLAK, LULUS):
        # Aturan 48: adjudikasi yang berhasil diperoleh tidak boleh menyamar
        # sebagai run gagal, ke arah mana pun putusannya jatuh.
        return 0
    return 4


if __name__ == "__main__":
    sys.exit(main())
