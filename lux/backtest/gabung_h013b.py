"""Penggabung Jalur B — satu-satunya berkas yang boleh melahirkan putusan H-013.

Sepuluh pecahan seed menghasilkan bahan; berkas ini mengubahnya menjadi ``p``.
ADR-015 pasal 4.4 menuntut **dua** syarat dalam satu kalimat — besaran
``SS − AS ≥ 0,020R`` **dan** ``p ≤ 0,05`` atas sedikitnya 300 ulangan permutasi
sinyal — dan sampai run 30214203863 hanya besarannya pernah dihitung. Medan
``lulus`` di laporan kontribusi karena itu bukan kelulusan hipotesis (ADR-024).
Di sini keduanya berdiri bersama, atau tidak berdiri sama sekali.

Aritmetika ``p`` **tidak** ada di sini; ia ada di ``lux.analisis.sebaran_nol``
yang sudah diuji. Pembaca agregat bulanan juga tidak disalin: ia diimpor dari
``run_h013b``. Arah impornya ``backtest → analisis``, tidak pernah sebaliknya
(aturan 8), dan itulah sebab penggabung berdiri di ``lux/backtest`` meskipun
pekerjaannya analisis: ia butuh pembaca milik orkestrator.

EMPAT KEADAAN YANG MEMBUATNYA MENOLAK MELAHIRKAN PUTUSAN
--------------------------------------------------------
**1. Cakupan seed tidak utuh.** Seed wajib menutup ``[0, 300)`` persis. 297 seed
bukan "hampir 300": ia melanggar ambang ulangan yang dibekukan, dan ``p`` dari
sebaran yang bolong tidak dapat ditafsirkan sebab yang hilang mungkin justru
ekor atasnya.

**2. Himpunan bulan berbeda.** Bila sebuah seed tidak memuat bulan yang sama
dengan sel SS, laporan **TIDAK DAPAT DINILAI** tetap ditulis lalu proses keluar
dengan kode 4. Penggabung tidak memotong ke irisan dan tidak mengisi nol.
Penyelarasan diam-diam menghasilkan angka yang tampak waras atas dua himpunan
yang berbeda, dan bentuk cacat itu paling sulit terlihat karena tidak ada yang
berbunyi.

**3. Kematian gerbang tidak dinyatakan.** Pecahan yang tidak mencantumkan bahwa
gerbang ``entri_acak`` dimatikan ditolak. Pelonggaran yang tidak dinyatakan
adalah cara paling rapi sebuah pagar berhenti menjaga.

**4. R-D5 tidak terbukti.** Bila tidak satu pecahan pun membuktikan seed 42
mereproduksi ekspektasi sel AS yang sudah dikomit, sebaran nol ini tidak terbukti
sebanding dengan sel SS yang menjadi pembandingnya.

SATU HAL YANG BUKAN KEGAGALAN
-----------------------------
**DITOLAK adalah hasil.** Bila ``p`` bulanan melampaui 0,05, H-013 gugur dan
kode keluarnya tetap 0, sebab run yang menjatuhkan hipotesis bekerja dengan benar.
Yang menghasilkan kode keluar bukan-nol hanyalah keadaan di mana putusan **tidak
dapat** dibentuk.

Pemakaian:
    python -m lux.backtest.gabung_h013b --dir reports \\
        --sel reports/backtest_h013_ss_sinyal_stop.json --out reports
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Iterable, Mapping

from lux.analisis.sebaran_nol import (
    PEMBATAS as PEMBATAS_SEBARAN,
    p_bulanan,
    p_per_perdagangan,
)
from lux.backtest.run_h013 import (
    AMBANG_KONTRIBUSI_SINYAL,
    MIN_TRADE_SEL,
    MIN_ULANGAN,
)
from lux.backtest.run_h013b import (
    EKSPEKTASI_AS_SEED42,
    SEED_AKHIR,
    SEED_AWAL,
    baca_bulan,
)

NAMA = "h013b_p"

# Sel SS run 30214203863, dikutip apa adanya dari laporan yang sudah dikomit.
# Ia TIDAK dihitung ulang di sini: menghitung ulang sel pembanding dengan mesin
# yang lebih baru berarti membandingkan dua mesin, bukan dua sinyal.
EKSPEKTASI_SS = 0.06664781299919262
TRADE_SS = 60018

# Galat baku per perdagangan sel SS. Dipakai HANYA sebagai pembanding untuk R-D4,
# yaitu untuk menunjukkan bahwa satuan penarikan mengubah besar galatnya — bukan
# sebagai bukti apa pun tentang sinyal (cacat kelas kedua belas).
GALAT_BAKU_PER_PERDAGANGAN_SS = 0.005570

# ADR-015 pasal 4.4. Tidak digeser, dan tidak akan digeser sesudah hasil terlihat.
AMBANG_P = 0.05

PEMBATAS = (
    "Putusan di berkas ini menuntut DUA syarat sekaligus, seperti bunyi ADR-015 "
    "pasal 4.4: besaran SS \u2212 AS \u2265 0,020R DAN p \u2264 0,05 atas sedikitnya 300 "
    "ulangan permutasi sinyal. Satu syarat saja tidak pernah cukup, dan besaran "
    "tanpa p adalah keadaan yang membuat medan `lulus` di laporan kontribusi "
    "H-013 tidak sah dibaca sebagai kelulusan (ADR-024). Satuan penarikan yang "
    "MENGIKAT adalah bulan kalender UTC (ADR-028); p per perdagangan ikut "
    "dilaporkan sebagai taksiran bawah dan hanya sah untuk MENJATUHKAN. "
    "Gerbang `entri_acak` dimatikan di seluruh run Jalur B, dan sel AS memang "
    "tidak dimaksudkan lulus kriteria apa pun. DITOLAK adalah hasil, bukan "
    "kegagalan run."
)


def daftar_pecahan(dir_laporan: Path | str) -> list[Path]:
    """Berkas pecahan, diurutkan menurut seed awal dan bukan menurut nama.

    Urutan leksikografis akan menaruh ``h013b_seed_120_150`` sebelum
    ``h013b_seed_30_60``, dan urutan itu akan menyesatkan pembaca laporan meski
    tidak mengubah ``p``.
    """
    d = Path(dir_laporan)
    berkas = list(d.glob("h013b_seed_*.json"))

    def kunci(p: Path) -> int:
        bagian = p.stem.split("_")
        try:
            return int(bagian[2])
        except (IndexError, ValueError) as e:
            raise ValueError(f"nama pecahan tak terbaca: {p.name}") from e

    return sorted(berkas, key=kunci)


def muat_pecahan(jalur: Iterable[Path | str]) -> dict:
    """Gabungkan pecahan, dengan tiga penolakan tegas.

    Yang ditolak: pecahan yang belum selesai, pecahan yang tidak menyatakan
    gerbang ``entri_acak`` mati, dan seed kembar antar pecahan. Seed kembar
    berarti dua pekerjaan menjalankan seed yang sama, sehingga sebaran nolnya
    lebih sempit daripada yang tampak dari jumlah barisnya.
    """
    daftar = [Path(p) for p in jalur]
    if not daftar:
        raise ValueError("tidak ada satu pun berkas pecahan")

    seed: dict[int, dict] = {}
    pecahan: list[dict] = []
    r_d5_terbukti = False
    for p in daftar:
        isi = json.loads(p.read_text(encoding="utf-8"))
        gerbang = str(isi.get("gerbang_entri_acak", ""))
        if "MATI" not in gerbang:
            raise ValueError(
                f"{p.name} tidak menyatakan gerbang entri_acak mati "
                f"(medan berisi {gerbang!r}); pelonggaran yang tidak dinyatakan "
                "tidak diterima"
            )
        if not isi.get("selesai"):
            raise ValueError(
                f"{p.name} belum selesai: {len(isi.get('seed_selesai') or [])} "
                f"dari {len(isi.get('seed_diminta') or [])} seed"
            )
        if isi.get("r_d5_cocok") is False:
            raise ValueError(
                f"{p.name} melaporkan R-D5 MELESET; sebaran nol ini tidak "
                "sebanding dengan sel AS yang sudah dikomit"
            )
        if isi.get("r_d5_cocok") is True:
            r_d5_terbukti = True
        for baris in isi.get("baris") or []:
            s = int(baris["seed"])
            if s in seed:
                raise ValueError(f"seed kembar antar pecahan: {s}")
            for k in ("ekspektasi_R", "trade", "bulan"):
                if k not in baris:
                    raise ValueError(f"baris seed {s} tanpa kunci {k}")
            seed[s] = baris
        pecahan.append(
            {
                "berkas": p.name,
                "pecahan": isi.get("pecahan"),
                "seed": len(isi.get("baris") or []),
                "r_d5_cocok": isi.get("r_d5_cocok"),
            }
        )

    return {"seed": seed, "pecahan": pecahan, "r_d5_terbukti": r_d5_terbukti}


def periksa_cakupan(seed: Iterable[int]) -> None:
    """Seed wajib menutup ``[SEED_AWAL, SEED_AKHIR)`` persis.

    Lubang di tengah tidak lebih ringan daripada kekurangan di ujung: yang hilang
    mungkin justru tarikan di ekor atas, yaitu tarikan yang paling menentukan
    besar ``p``.
    """
    ada = sorted(int(s) for s in seed)
    wajib = list(range(SEED_AWAL, SEED_AKHIR))
    if len(set(ada)) != len(ada):
        raise ValueError("seed kembar di dalam gabungan")
    if ada != wajib:
        hilang = sorted(set(wajib) - set(ada))
        asing = sorted(set(ada) - set(wajib))
        raise ValueError(
            f"cakupan seed tidak utuh: {len(ada)} dari {len(wajib)}; "
            f"hilang {hilang[:12]}{'...' if len(hilang) > 12 else ''}, "
            f"asing {asing[:12]}{'...' if len(asing) > 12 else ''}. "
            f"Ambang {MIN_ULANGAN} ulangan tidak diturunkan."
        )


def periksa_bulan(
    bulan_teramati: Iterable[Mapping], nol_bulanan: Mapping[int, Iterable[Mapping]]
) -> list[str]:
    """Laporkan setiap seed yang himpunan bulannya berbeda dari sel SS.

    Dipanggil **sebelum** ``p_bulanan`` supaya seluruh ketidaksesuaian terkumpul
    sekaligus. ``selisih_bulanan`` akan melempar pada yang pertama, dan galat
    tunggal itu menyembunyikan seberapa luas persoalannya.
    """
    acuan = {str(b["periode"]) for b in bulan_teramati}
    pesan: list[str] = []
    for s in sorted(nol_bulanan):
        punya = {str(b["periode"]) for b in nol_bulanan[s]}
        if punya != acuan:
            hilang = sorted(acuan - punya)
            asing = sorted(punya - acuan)
            pesan.append(
                f"seed {s}: {len(punya)} bulan lawan {len(acuan)} pada SS; "
                f"hilang {hilang[:6]}, asing {asing[:6]}"
            )
    return pesan


def adjudikasi(
    besaran: float,
    p: float | None,
    n: int,
    trade_terkecil: int,
    bulan_cocok: bool,
) -> dict:
    """Putusan ADR-015 pasal 4.4: dua syarat sekaligus, atau tidak sama sekali.

    Ketidakcukupan bahan menghasilkan **TIDAK DAPAT DINILAI**, bukan GAGAL.
    Perbedaan itu bukan kehalusan bahasa: hipotesis yang gagal sudah selesai,
    sedangkan yang tak ternilai masih menunggu bahan, dan mencampurnya akan
    membuat sebelas penolakan terdahulu tampak lebih kuat daripada sebenarnya.
    """
    sebab: list[str] = []
    if not bulan_cocok:
        sebab.append("himpunan bulan antar seed dan sel SS tidak sama")
    if n < MIN_ULANGAN:
        sebab.append(f"ulangan {n} < {MIN_ULANGAN}")
    if trade_terkecil < MIN_TRADE_SEL:
        sebab.append(f"perdagangan sel terkecil {trade_terkecil} < {MIN_TRADE_SEL}")
    if p is None:
        sebab.append("p tidak terhitung")

    dasar = {
        "besaran_R": besaran,
        "ambang_besaran_R": AMBANG_KONTRIBUSI_SINYAL,
        "p": p,
        "ambang_p": AMBANG_P,
        "satuan_p": "bulan",
        "n": int(n),
        "min_ulangan": MIN_ULANGAN,
        "trade_terkecil": int(trade_terkecil),
        "melewati_ambang_besaran": besaran >= AMBANG_KONTRIBUSI_SINYAL,
    }
    if sebab:
        return dasar | {
            "dapat_dinilai": False,
            "putusan": "TIDAK DAPAT DINILAI",
            "lulus": False,
            "sebab": "; ".join(sebab),
        }

    lulus = besaran >= AMBANG_KONTRIBUSI_SINYAL and float(p) <= AMBANG_P
    return dasar | {
        "dapat_dinilai": True,
        "putusan": "LULUS" if lulus else "DITOLAK",
        "lulus": lulus,
        "sebab": "",
    }


def ringkas(muat: dict, bulan_ss: list[dict], pesan_bulan: list[str]) -> dict:
    """Susun seluruh angka, termasuk adjudikasi R-D3 dan R-D4.

    R-D3 dan R-D4 diadili di sini alih-alih di dalam prosa, sebab ramalan yang
    dinilai oleh mata pembaca bukan ramalan yang diadili.
    """
    seed = muat["seed"]
    nol_bulanan = {s: seed[s]["bulan"] for s in seed}
    nol_gabungan = {s: float(seed[s]["ekspektasi_R"]) for s in seed}
    trade_terkecil = min([TRADE_SS] + [int(seed[s]["trade"]) for s in seed])

    bulan_cocok = not pesan_bulan
    hasil_bulan = p_bulanan(bulan_ss, nol_bulanan) if bulan_cocok else None
    hasil_trade = p_per_perdagangan(EKSPEKTASI_SS, nol_gabungan)

    nilai = sorted(nol_gabungan.values())
    rerata = float(math.fsum(nilai) / len(nilai))
    std = (
        math.sqrt(math.fsum((x - rerata) ** 2 for x in nilai) / (len(nilai) - 1))
        if len(nilai) > 1
        else None
    )

    besaran = EKSPEKTASI_SS - EKSPEKTASI_AS_SEED42
    putusan = adjudikasi(
        besaran=besaran,
        p=None if hasil_bulan is None else hasil_bulan["tak_berpasangan"]["p"],
        n=len(seed),
        trade_terkecil=trade_terkecil,
        bulan_cocok=bulan_cocok,
    )

    return {
        "hipotesis": "H-013",
        "jalur": "B",
        "ekspektasi_ss_dikomit": EKSPEKTASI_SS,
        "ekspektasi_as_seed42_dikomit": EKSPEKTASI_AS_SEED42,
        "besaran_sumbangan_sinyal_R": besaran,
        "putusan": putusan,
        "p_bulan": hasil_bulan,
        "p_perdagangan": hasil_trade,
        "ketidaksesuaian_bulan": pesan_bulan,
        "sebaran_seed": {
            "n": len(nilai),
            "rerata": rerata,
            "std": std,
            "min": nilai[0],
            "maks": nilai[-1],
        },
        "ramalan": {
            "R-D3": {
                "bunyi": (
                    "sedikitnya satu seed melampaui ekspektasi sel SS "
                    f"{EKSPEKTASI_SS}; bila tidak, permutasinya cacat"
                ),
                "tepat": nilai[-1] > EKSPEKTASI_SS,
                "seed_tertinggi_R": nilai[-1],
            },
            "R-D4": {
                "bunyi": (
                    "simpangan baku antar seed MELAMPAUI galat baku per "
                    f"perdagangan {GALAT_BAKU_PER_PERDAGANGAN_SS}R, bukti "
                    "langsung cacat kelas kedua belas"
                ),
                "tepat": None if std is None else std > GALAT_BAKU_PER_PERDAGANGAN_SS,
                "std_antar_seed": std,
                "galat_baku_per_perdagangan": GALAT_BAKU_PER_PERDAGANGAN_SS,
            },
        },
        "pecahan": muat["pecahan"],
        "r_d5_terbukti": muat["r_d5_terbukti"],
        "gerbang_entri_acak": "MATI di seluruh run Jalur B",
        "pembatas": PEMBATAS,
        "pembatas_sebaran": PEMBATAS_SEBARAN,
    }


def tulis_laporan(isi: dict, out: Path | str = "reports", nama: str = NAMA) -> tuple:
    """Dua berkas: JSON untuk mesin, Markdown untuk manusia, angka yang sama."""
    d = Path(out)
    d.mkdir(parents=True, exist_ok=True)
    j = d / f"{nama}.json"
    m = d / f"{nama}.md"
    j.write_text(json.dumps(isi, indent=2, ensure_ascii=False), encoding="utf-8")

    p = isi["putusan"]
    strip = "\u2014"

    def angka(x, fmt="+.6f"):
        return strip if x is None else format(float(x), fmt)

    baris = [
        "# H-013 Jalur B \u2014 p atas sebaran nol permutasi sinyal",
        "",
        f"**{p['putusan']}**",
        "",
        PEMBATAS,
        "",
        "## Dua syarat ADR-015 pasal 4.4",
        "",
        "| Syarat | Nilai | Ambang | Terpenuhi |",
        "|---|---|---|---|",
        f"| besaran SS \u2212 AS | {angka(p['besaran_R'])}R | "
        f"{AMBANG_KONTRIBUSI_SINYAL}R | "
        f"{'ya' if p['melewati_ambang_besaran'] else 'TIDAK'} |",
        f"| p (satuan bulan) | {angka(p['p'], '.6f')} | {AMBANG_P} | "
        f"{'ya' if p['p'] is not None and float(p['p']) <= AMBANG_P else 'TIDAK'} |",
        f"| ulangan | {p['n']} | {MIN_ULANGAN} | "
        f"{'ya' if p['n'] >= MIN_ULANGAN else 'TIDAK'} |",
        "",
    ]
    if p["sebab"]:
        baris += [f"Sebab tak ternilai: {p['sebab']}", ""]

    if isi["ketidaksesuaian_bulan"]:
        baris += [
            "## Himpunan bulan tidak sama",
            "",
            "Penggabung TIDAK memotong ke irisan dan TIDAK mengisi nol. "
            "Penyelarasan diam-diam akan membandingkan dua himpunan berbeda "
            "tanpa jejak.",
            "",
        ]
        baris += [f"- {t}" for t in isi["ketidaksesuaian_bulan"][:20]]
        baris += [""]

    s = isi["sebaran_seed"]
    baris += [
        "## Sebaran nol antar seed",
        "",
        f"- n: {s['n']}",
        f"- rerata: {angka(s['rerata'])}R",
        f"- simpangan baku: {angka(s['std'])}R",
        f"- rentang: {angka(s['min'])}R sampai {angka(s['maks'])}R",
        f"- ekspektasi sel SS yang dibandingkan: {angka(EKSPEKTASI_SS)}R",
        "",
        "## Ramalan yang dibekukan sebelum satu seed pun berjalan",
        "",
    ]
    for kunci, r in isi["ramalan"].items():
        status = {True: "TEPAT", False: "MELESET", None: "tidak ternilai"}[r["tepat"]]
        baris += [f"- **{kunci}** {status}: {r['bunyi']}"]
    baris += [
        "",
        "## p pada satuan perdagangan (taksiran bawah, tidak mengikat)",
        "",
        f"p = {angka(isi['p_perdagangan']['p'], '.6f')} "
        f"(cacah {isi['p_perdagangan']['cacah_ge']} dari {isi['p_perdagangan']['n']}). "
        "Ia hanya sah untuk MENJATUHKAN klaim.",
        "",
        PEMBATAS_SEBARAN,
        "",
    ]
    m.write_text("\n".join(baris) + "\n", encoding="utf-8")
    return j, m


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="reports")
    ap.add_argument("--sel", default="reports/backtest_h013_ss_sinyal_stop.json")
    ap.add_argument("--out", default="reports")
    ap.add_argument("--nama", default=NAMA)
    a = ap.parse_args(argv)

    pecahan = daftar_pecahan(a.dir)
    if not pecahan:
        print(f"DITOLAK: tidak ada pecahan h013b_seed_*.json di {a.dir}", flush=True)
        return 2
    print(f"pecahan ditemukan: {[p.name for p in pecahan]}", flush=True)

    muat = muat_pecahan(pecahan)
    periksa_cakupan(muat["seed"])
    if not muat["r_d5_terbukti"]:
        raise ValueError(
            "tidak satu pecahan pun membuktikan R-D5 (seed 42 mereproduksi "
            "ekspektasi sel AS yang dikomit); sebaran nol ini belum terbukti "
            "sebanding dengan sel SS pembandingnya"
        )
    print(f"seed utuh: {len(muat['seed'])} pada [{SEED_AWAL}, {SEED_AKHIR})", flush=True)

    bulan_ss = baca_bulan(a.sel)["bulan"]
    print(f"bulan sel SS: {len(bulan_ss)}", flush=True)

    pesan = periksa_bulan(bulan_ss, {s: muat["seed"][s]["bulan"] for s in muat["seed"]})
    isi = ringkas(muat, bulan_ss, pesan)
    j, m = tulis_laporan(isi, a.out, a.nama)
    print(f"laporan: {j}, {m}", flush=True)
    print(json.dumps(isi["putusan"], indent=2, ensure_ascii=False), flush=True)

    if pesan:
        print(
            f"KODE KELUAR 4: {len(pesan)} seed berhimpunan bulan berbeda. "
            "Laporan TIDAK DAPAT DINILAI sudah ditulis; penyelarasan menuntut "
            "keputusan tertulis, bukan potongan diam-diam.",
            flush=True,
        )
        return 4

    # DITOLAK adalah hasil, bukan kegagalan run.
    return 0


if __name__ == "__main__":
    sys.exit(main())
