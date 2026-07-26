"""Adjudikasi H-014: uji tanda berpasangan per bulan, tanpa satu cabang LULUS.

Modul ini membaca dua laporan sel yang ditulis ``runner.jalankan_spek`` dan
memasangkan blok ``agregat_periode`` keduanya menurut bulan kalender UTC waktu
masuk (ADR-028). Aritmetika pemasangan, uji tanda, dan bootstrap **tidak** ada
di sini: seluruhnya milik ``lux.analisis.berpasangan``, modul daun yang sudah
diuji. Aritmetika yang hanya hidup di dalam ``main`` tidak pernah benar-benar
diuji, dan itulah sebab dua cacat sebelumnya tidak berbunyi berbulan-bulan
(aturan 32).

H-014 MUSTAHIL LULUS (ADR-034 pasal 2)
--------------------------------------
``berpasangan`` menyatakan sendiri bahwa p-nya mengukur ketidakpastian
**penarikan bulan**, bukan sebaran permutasi sinyal, sehingga ia sah untuk
MENJATUHKAN dan tidak sah untuk MENEGAKKAN; ia memancarkan
``memenuhi_adr015: False`` tanpa syarat, dan pagar itu benar. Maka ``adjudikasi``
hanya dapat mengembalikan dua putusan:

- **DITOLAK** — besaran gagal, atau p > ambang, atau sel di bawah 100 trade.
- **TIDAK DAPAT DINILAI** — himpunan bulan tidak sama, pasangan kurang dari dua,
  ada bulan tanpa ekspektasi, **atau** besaran dan p keduanya lolos.

Kemungkinan terakhir itu sengaja tidak diberi nama "lulus". Bila besaran besar
dan p kecil, yang diperoleh hanyalah "tidak dapat dijatuhkan oleh uji ini";
kelulusan menuntut nol permutasi geometri yang **belum ada**, dan ADR-033 pasal 3
sudah membuktikan bahwa membuatnya menuntut bedah ``engine.jalankan`` yang
dipakai tiga belas hipotesis.

KODE KELUAR
-----------
``0`` DITOLAK — hasil yang mematikan hipotesis adalah hasil yang **berhasil**
diperoleh (aturan 48). ``4`` TIDAK DAPAT DINILAI. ``2`` pagar pra-terbang.
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

NAMA = "h014_berpasangan"

DITOLAK = "DITOLAK"
TIDAK_DAPAT_DINILAI = "TIDAK DAPAT DINILAI"
PUTUSAN_MUNGKIN = (DITOLAK, TIDAK_DAPAT_DINILAI)

# Lantai pasangan adalah lantai modul yang dipakai, bukan angka baru: uji_tanda
# dan bootstrap keduanya menuntut minimal dua pasang. Tidak ada ambang jumlah
# bulan yang dikarang di sini, sebab ambang yang dikarang sesudah rancangan
# dibekukan adalah ambang yang dipilih.
MIN_PASANGAN = 2

PEMBATAS = (
    "Putusan H-014 hanya dapat DITOLAK atau TIDAK DAPAT DINILAI; tidak ada "
    "cabang LULUS di modul ini, dan pengujian menuntut ketiadaannya (ADR-034). "
    "SS' dan SH' BUKAN sel SS dan SH run 30214203863: kedua sel di sana berbeda "
    "pada DUA medan sekaligus (ada-tidaknya target DAN umur 42 lawan 48), "
    "sehingga +0,029481R tidak boleh dipakai sebagai pembanding maupun sebagai "
    "'versi sebelum perbaikan'. Berkas md tiap sel mencetak LULUS atau DITOLAK "
    "milik pra-registrasi PER SEL dari runner; itu bukan putusan H-014."
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


def trade_sel(isi: dict) -> int:
    """Jumlah perdagangan luar sampel satu sel."""
    return int(isi.get("gabungan", {}).get("jumlah_trade_luar_sampel", 0) or 0)


def adjudikasi(
    isi_a: dict,
    isi_b: dict,
    ambang_besaran: float,
    ambang_p: float,
    min_trade: int,
    ulangan: int = ULANGAN,
    seed: int = SEED,
) -> dict:
    """Putusan H-014. Nilai kembaliannya SELALU salah satu ``PUTUSAN_MUNGKIN``.

    Besaran dilaporkan **dua kali** (aturan 49): selisih agregat dan rerata
    selisih bulanan. Keduanya tidak identik, dan menyebut hanya satu di antaranya
    adalah cara paling mudah membuat besaran terlihat lebih besar daripada
    seharusnya. Pembanding terhadap **rerata nol** tidak ada di sini, dan itu
    dinyatakan alih-alih dibiarkan tak disebut: uji ini tidak menarik sebaran
    nol permutasi geometri, sebab nol semacam itu belum dirancang.
    """
    per_bulan = ringkas(
        pasangan_bulan(isi_a, isi_b), ambang_besaran, ulangan=ulangan, seed=seed
    )
    trade_a, trade_b = trade_sel(isi_a), trade_sel(isi_b)

    sebab: list[str] = []
    tak_dapat: list[str] = []

    if per_bulan["hanya_a"] or per_bulan["hanya_b"]:
        tak_dapat.append(
            f"himpunan bulan tidak sama: hanya_a {per_bulan['hanya_a']}, "
            f"hanya_b {per_bulan['hanya_b']}"
        )
    if per_bulan["tanpa_nilai"]:
        tak_dapat.append(
            f"bulan tanpa ekspektasi di salah satu sel: {per_bulan['tanpa_nilai']}"
        )
    if per_bulan["n_pasangan"] < MIN_PASANGAN:
        tak_dapat.append(
            f"pasangan bulan {per_bulan['n_pasangan']} < {MIN_PASANGAN}"
        )

    besaran_bulanan = per_bulan.get("rerata_selisih")
    besaran_agregat = per_bulan.get("selisih_agregat")
    p = (per_bulan.get("uji_tanda") or {}).get("p")

    if not tak_dapat:
        for nama, n in (("a", trade_a), ("b", trade_b)):
            if n < int(min_trade):
                sebab.append(f"trade sel {nama} {n} < {min_trade}")
        if besaran_bulanan is None or besaran_bulanan < float(ambang_besaran):
            sebab.append(
                f"rerata selisih bulanan {besaran_bulanan!r} < {ambang_besaran}R"
            )
        if p is None or p > float(ambang_p):
            sebab.append(f"p uji tanda bulanan {p!r} > {ambang_p}")

    if tak_dapat:
        putusan, alasan = TIDAK_DAPAT_DINILAI, tak_dapat
    elif sebab:
        putusan, alasan = DITOLAK, sebab
    else:
        putusan, alasan = (
            TIDAK_DAPAT_DINILAI,
            [
                "besaran dan p keduanya lolos, tetapi itu BUKAN kelulusan: p di "
                "sini mengukur penarikan bulan dan sah hanya untuk "
                "menjatuhkan. Kelulusan menuntut sebaran nol permutasi "
                "geometri yang belum dirancang (ADR-033 pasal 3, ADR-034 "
                "pasal 2)."
            ],
        )

    assert putusan in PUTUSAN_MUNGKIN
    return {
        "hipotesis": "H-014",
        "putusan": putusan,
        "alasan": alasan,
        "besaran_rerata_bulanan_R": besaran_bulanan,
        "besaran_agregat_R": besaran_agregat,
        "catatan_besaran": (
            "Dua besaran dilaporkan sebab keduanya tidak identik (aturan 49). "
            "Pembanding terhadap rerata sebaran nol TIDAK ADA di uji ini: nol "
            "permutasi geometri belum dirancang."
        ),
        "p": p,
        "ambang_besaran_R": float(ambang_besaran),
        "ambang_p": float(ambang_p),
        "min_trade_sel": int(min_trade),
        "trade_a": trade_a,
        "trade_b": trade_b,
        "satuan_penarikan": "bulan",
        "per_bulan": per_bulan,
        "putusan_mungkin": list(PUTUSAN_MUNGKIN),
        "memenuhi_adr015": False,
        "pembatas": PEMBATAS,
        "pembatas_berpasangan": PEMBATAS_BERPASANGAN,
    }


def tulis_laporan(
    hasil: dict, out: Path | str = "reports", nama: str = NAMA
) -> dict:
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
        "# H-014 — geometri keluar dengan umur pegangan disetarakan",
        "",
        f"> {hasil['pembatas']}",
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
        f"- Rerata selisih bulanan: **{fmt(hasil['besaran_rerata_bulanan_R'])}R**",
        f"- Selisih agregat: **{fmt(hasil['besaran_agregat_R'])}R**",
        f"- Ambang besaran: {hasil['ambang_besaran_R']}R — ambang **BARU**, "
        "dibekukan 2026-07-27 (ADR-034, aturan 53), bukan kutipan ADR-015 "
        "pasal 4.4 yang membekukan ambang bagi kaki sinyal.",
        "",
        f"{hasil['catatan_besaran']}",
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
        f"- Trade sel A / sel B: **{hasil['trade_a']:,}** / "
        f"**{hasil['trade_b']:,}**, lantai {hasil['min_trade_sel']}",
        f"- Memenuhi ADR-015 pasal 4.4: **TIDAK**",
        "",
        "## Yang tidak dijawab laporan ini",
        "",
        "Putusan LULUS tidak mungkin dihasilkan uji ini dan tidak ada cabang "
        "kodenya. Kelulusan kaki geometri menuntut sebaran nol permutasi "
        "**geometri** yang belum dirancang; ADR-033 pasal 3 membuktikan bahwa "
        "nol jarak stop menuntut bedah `engine.jalankan` yang dipakai tiga "
        "belas hipotesis, dan bedah itu tidak dibeli.",
        "",
    ]
    (d / f"{nama}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return hasil


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Adjudikasi H-014 (ADR-033, ADR-034)")
    ap.add_argument("--sel-a", required=True, help="JSON laporan sel SS'")
    ap.add_argument("--sel-b", required=True, help="JSON laporan sel SH'")
    ap.add_argument("--ambang-besaran", type=float, required=True)
    ap.add_argument("--ambang-p", type=float, required=True)
    ap.add_argument("--min-trade", type=int, required=True)
    ap.add_argument("--ulangan", type=int, default=ULANGAN)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--out", default="reports")
    ap.add_argument("--nama", default=NAMA)
    a = ap.parse_args(argv)

    try:
        isi_a = muat_sel(a.sel_a)
        isi_b = muat_sel(a.sel_b)
    except (FileNotFoundError, ValueError) as e:
        print(f"DITOLAK pagar pra-terbang: {e}", flush=True)
        return 2

    hasil = adjudikasi(
        isi_a,
        isi_b,
        ambang_besaran=a.ambang_besaran,
        ambang_p=a.ambang_p,
        min_trade=a.min_trade,
        ulangan=a.ulangan,
        seed=a.seed,
    )
    tulis_laporan(hasil, out=a.out, nama=a.nama)
    print(json.dumps(hasil, indent=2, ensure_ascii=False), flush=True)
    print(f"\nPUTUSAN H-014: {hasil['putusan']}", flush=True)
    for al in hasil["alasan"]:
        print(f"  - {al}", flush=True)

    if hasil["putusan"] == DITOLAK:
        # Aturan 48: hasil yang mematikan hipotesis adalah hasil yang berhasil
        # diperoleh, dan ia tidak boleh menyamar sebagai run gagal.
        return 0
    return 4


if __name__ == "__main__":
    sys.exit(main())
