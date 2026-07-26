"""Uji berpasangan tingkat simbol dan bulan untuk selisih antar sel (ADR-026).

ADR-024 menahan putusan H-013 karena kriteria utama ADR-015 §4.4 hanya
setengah terhitung: besaran SS−AS ada (+0,054842R), p permutasi sinyalnya tidak
ada sama sekali. ADR-024 menawarkan "Jalur A" sebagai uji berpasangan atas 4.082
jendela dari laporan yang sudah dikomit. **Tawaran itu salah**, dan ADR-026
mengoreksinya: ``runner.jalankan_spek`` tidak menulis satu pun nilai R per
jendela — ``per_simbol.jendela`` adalah JUMLAH jendela dan ``per_simbol.parameter``
hanya parameter tiap jendela. Yang benar-benar dapat dipasangkan dari berkas yang
dikomit hanyalah dua tingkat: **simbol** (dari ``per_simbol``) dan **bulan**
(dari ``agregat_periode``).

MODUL SENDIRI, DAN TIDAK MENGIMPOR ``lux.backtest``. Alasannya sama dengan
``sebaran.py``: orkestrator lama dibekukan karena hasilnya sudah dikomit, dan
arah impor yang menutup lingkaran sudah pernah menjadi cacat (``4b77617``).
Ambang tidak diketik ulang di sini; pemanggil menyerahkannya, persis seperti
``runner`` menyerahkan ``min_ekspektasi_R`` ke ``jarak_ambang``.

PEMBATAS YANG WAJIB IKUT TERCETAK DI SETIAP LAPORAN
---------------------------------------------------
p yang dihasilkan modul ini mengukur ketidakpastian **penarikan simbol atau
bulan**. Ia **bukan** sebaran permutasi sinyal, sehingga ia **tidak** memenuhi
ADR-015 §4.4 yang menuntut p atas minimal 300 permutasi sinyal. Mengikuti kaidah
yang sudah dibayar di ADR-013: angka ini sah dipakai untuk **menjatuhkan** klaim
SS−AS, dan **tidak** sah dipakai untuk menegakkannya. Karena itu modul ini tidak
pernah memancarkan kunci ``lulus`` bernilai benar — secara sengaja, dan hal itu
dikunci oleh test.

Uji tanda dipilih, bukan uji-t, karena selisih antar simbol tidak mendekati
normal dan ``scipy`` tidak tersedia di runner. Nilai p memakai koreksi tambah
satu ``(1 + m) / (1 + ulangan)``, yang membuat p tidak pernah nol: p nol adalah
pernyataan yang tidak dapat dipertanggungjawabkan oleh sampel berhingga.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

NAMA = "berpasangan"

# Seed dan ulangan bawaan. Keduanya dicetak ke laporan supaya hasilnya dapat
# diulang persis, dan supaya tidak ada yang bisa memilih seed sesudah melihat p.
SEED = 20260727
ULANGAN = 10000

PEMBATAS = (
    "p di sini mengukur ketidakpastian PENARIKAN SIMBOL/BULAN, bukan sebaran "
    "permutasi sinyal. Ia TIDAK memenuhi ADR-015 pasal 4.4 yang menuntut p atas "
    "minimal 300 permutasi sinyal. Angka ini sah dipakai untuk MENJATUHKAN "
    "klaim selisih antar sel, dan tidak sah dipakai untuk MENEGAKKANNYA."
)


def _nilai(baris: dict, kunci: str) -> float | None:
    """Ambil satu nilai numerik; ``None`` tetap ``None``, tak finit ditolak keras."""
    v = baris.get(kunci)
    if v is None:
        return None
    x = float(v)
    if not math.isfinite(x):
        raise ValueError(
            f"nilai tidak finit pada kunci {kunci!r}; itu tanda cacat mesin, "
            "bukan tanda data langka"
        )
    return x


def pasangkan(
    daftar_a: Iterable[dict],
    daftar_b: Iterable[dict],
    kunci_id: str,
    kunci_nilai: str = "ekspektasi_R",
    kunci_bobot: str = "trade",
    kunci_total: str = "total_R",
) -> dict:
    """Pasangkan dua daftar agregat menurut ``kunci_id``.

    Hanya irisan yang dipasangkan, dan yang di luar irisan **wajib tercatat**
    (``hanya_a``, ``hanya_b``): himpunan yang menyusut tanpa catatan tidak dapat
    dibedakan dari penyubsetan setelah melihat hasil.
    """
    a = {str(b[kunci_id]): b for b in daftar_a}
    b = {str(x[kunci_id]): x for x in daftar_b}
    id_a, id_b = set(a), set(b)

    pasangan: list[dict] = []
    tanpa_nilai: list[str] = []
    for k in sorted(id_a & id_b):
        va = _nilai(a[k], kunci_nilai)
        vb = _nilai(b[k], kunci_nilai)
        if va is None or vb is None:
            tanpa_nilai.append(k)
            continue
        pasangan.append(
            {
                "id": k,
                "a": va,
                "b": vb,
                "selisih": va - vb,
                "bobot_a": float(a[k].get(kunci_bobot) or 0.0),
                "bobot_b": float(b[k].get(kunci_bobot) or 0.0),
                "total_a": float(a[k].get(kunci_total) or 0.0),
                "total_b": float(b[k].get(kunci_total) or 0.0),
            }
        )

    return {
        "kunci_id": kunci_id,
        "kunci_nilai": kunci_nilai,
        "pasangan": pasangan,
        "n_pasangan": len(pasangan),
        "hanya_a": sorted(id_a - id_b),
        "hanya_b": sorted(id_b - id_a),
        "tanpa_nilai": tanpa_nilai,
    }


def pasangan_simbol(isi_a: dict, isi_b: dict) -> dict:
    """437 pasang dari blok ``per_simbol`` dua laporan sel."""
    return pasangkan(
        isi_a.get("per_simbol", []), isi_b.get("per_simbol", []), "symbol"
    )


def pasangan_bulan(isi_a: dict, isi_b: dict) -> dict:
    """73 pasang dari blok ``agregat_periode`` dua laporan sel."""
    return pasangkan(
        isi_a.get("agregat_periode", []),
        isi_b.get("agregat_periode", []),
        "periode",
    )


def uji_tanda(
    selisih: Sequence[float], ulangan: int = ULANGAN, seed: int = SEED
) -> dict:
    """Permutasi tanda berpasangan dua sisi atas rerata selisih."""
    d = np.asarray(list(selisih), dtype=float)
    n = int(d.size)
    if n < 2:
        return {
            "n": n,
            "dapat_dinilai": False,
            "sebab": "butuh minimal dua pasang",
            "rerata": float(d[0]) if n == 1 else None,
            "p": None,
            "ulangan": 0,
            "seed": int(seed),
            "pembatas": PEMBATAS,
        }

    rerata = float(d.mean())
    rng = np.random.default_rng(seed)
    tanda = rng.integers(0, 2, size=(int(ulangan), n)).astype(np.int8) * 2 - 1
    sebaran = (tanda * d).mean(axis=1)
    m = int(np.count_nonzero(np.abs(sebaran) >= abs(rerata) - 1e-15))
    return {
        "n": n,
        "dapat_dinilai": True,
        "sebab": "",
        "rerata": rerata,
        "p": (1.0 + m) / (1.0 + float(ulangan)),
        "m_lebih_ekstrem": m,
        "ulangan": int(ulangan),
        "seed": int(seed),
        "pembatas": PEMBATAS,
    }


def bootstrap(
    selisih: Sequence[float],
    ulangan: int = ULANGAN,
    seed: int = SEED,
    alpha: float = 0.05,
) -> dict:
    """Selang persentil bootstrap berpasangan untuk rerata selisih."""
    d = np.asarray(list(selisih), dtype=float)
    n = int(d.size)
    if n < 2:
        return {
            "n": n,
            "dapat_dinilai": False,
            "sebab": "butuh minimal dua pasang",
            "rerata": float(d[0]) if n == 1 else None,
            "bawah": None,
            "atas": None,
            "alpha": float(alpha),
            "pembatas": PEMBATAS,
        }

    rng = np.random.default_rng(seed + 1)
    idx = rng.integers(0, n, size=(int(ulangan), n))
    sebaran = d[idx].mean(axis=1)
    bawah, atas = (
        float(v)
        for v in np.percentile(
            sebaran, [100.0 * alpha / 2.0, 100.0 * (1.0 - alpha / 2.0)]
        )
    )
    return {
        "n": n,
        "dapat_dinilai": True,
        "sebab": "",
        "rerata": float(d.mean()),
        "bawah": bawah,
        "atas": atas,
        "alpha": float(alpha),
        "ulangan": int(ulangan),
        "seed": int(seed) + 1,
        "pembatas": PEMBATAS,
    }


def ringkas(
    hasil_pasangan: dict,
    ambang: float,
    ulangan: int = ULANGAN,
    seed: int = SEED,
) -> dict:
    """Ringkasan lengkap satu tingkat pemasangan.

    ``ambang`` diserahkan pemanggil dan hanya dipakai untuk melaporkan apakah
    **besaran** rerata selisih melewatinya. Itu bukan putusan: ADR-015 §4.4
    menuntut besaran **dan** p permutasi sinyal, dan p yang kedua tidak dihitung
    di modul ini. Karena itu kunci ``memenuhi_adr015`` selalu ``False``.
    """
    ps = hasil_pasangan["pasangan"]
    d = [p["selisih"] for p in ps]
    n = len(ps)

    dasar = {
        "kunci_id": hasil_pasangan["kunci_id"],
        "kunci_nilai": hasil_pasangan["kunci_nilai"],
        "n_pasangan": n,
        "hanya_a": hasil_pasangan["hanya_a"],
        "hanya_b": hasil_pasangan["hanya_b"],
        "tanpa_nilai": hasil_pasangan["tanpa_nilai"],
        "ambang_besaran": float(ambang),
        "memenuhi_adr015": False,
        "sebab_adr015": PEMBATAS,
        "pembatas": PEMBATAS,
    }

    if n < 2:
        return dasar | {
            "dapat_dinilai": False,
            "sebab": "butuh minimal dua pasang",
            "rerata_selisih": None,
            "rerata_berbobot": None,
            "selisih_agregat": None,
            "median_selisih": None,
            "fraksi_positif": None,
            "melewati_ambang_besaran": None,
            "uji_tanda": uji_tanda(d, ulangan=ulangan, seed=seed),
            "bootstrap": bootstrap(d, ulangan=ulangan, seed=seed),
        }

    a = np.asarray(d, dtype=float)
    bobot_a = np.asarray([p["bobot_a"] for p in ps], dtype=float)
    total_a = float(sum(p["total_a"] for p in ps))
    total_b = float(sum(p["total_b"] for p in ps))
    trade_a = float(bobot_a.sum())
    trade_b = float(sum(p["bobot_b"] for p in ps))

    rerata = float(a.mean())
    berbobot = float(np.average(a, weights=bobot_a)) if trade_a > 0 else None
    agregat = (
        total_a / trade_a - total_b / trade_b
        if trade_a > 0 and trade_b > 0
        else None
    )

    return dasar | {
        "dapat_dinilai": True,
        "sebab": "",
        "rerata_selisih": rerata,
        "rerata_berbobot": berbobot,
        "selisih_agregat": agregat,
        "median_selisih": float(np.median(a)),
        "fraksi_positif": float(np.count_nonzero(a > 0)) / float(n),
        "trade_a": trade_a,
        "trade_b": trade_b,
        "melewati_ambang_besaran": bool(rerata >= float(ambang)),
        "uji_tanda": uji_tanda(d, ulangan=ulangan, seed=seed),
        "bootstrap": bootstrap(d, ulangan=ulangan, seed=seed),
    }


def _baris_md(judul: str, r: dict) -> list[str]:
    strip = "\u2014"
    if not r["dapat_dinilai"]:
        return [f"### {judul}", "", f"Tidak dapat dinilai: {r['sebab']}.", ""]
    ut = r["uji_tanda"]
    bs = r["bootstrap"]
    fmt = lambda v: strip if v is None else f"{v:+.6f}"
    return [
        f"### {judul}",
        "",
        f"- Pasangan: **{r['n_pasangan']:,}**",
        f"- Rerata selisih: **{fmt(r['rerata_selisih'])}R**",
        f"- Rerata berbobot trade: **{fmt(r['rerata_berbobot'])}R**",
        f"- Selisih agregat (pembanding): **{fmt(r['selisih_agregat'])}R**",
        f"- Median selisih: **{fmt(r['median_selisih'])}R**",
        f"- Fraksi pasangan positif: **{r['fraksi_positif']:.4f}**",
        f"- p uji tanda ({ut['ulangan']:,} ulangan, seed {ut['seed']}): "
        f"**{ut['p']:.6f}**",
        f"- Selang bootstrap 95%: **[{fmt(bs['bawah'])}, {fmt(bs['atas'])}]R**",
        f"- Melewati ambang besaran {r['ambang_besaran']}R: "
        f"**{'ya' if r['melewati_ambang_besaran'] else 'tidak'}**",
        f"- Memenuhi ADR-015 pasal 4.4: **TIDAK**",
        "",
    ]


def tulis_laporan(
    nama: str,
    per_simbol: dict,
    per_bulan: dict,
    out: Path | str = Path("reports"),
    catatan: str = "",
) -> dict:
    """Tulis JSON dan Markdown; keduanya wajib memuat ``PEMBATAS``."""
    isi = {
        "nama": nama,
        "pembatas": PEMBATAS,
        "catatan": catatan,
        "per_simbol": per_simbol,
        "per_bulan": per_bulan,
    }
    d = Path(out)
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{nama}.json").write_text(
        json.dumps(isi, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    md = [
        f"# Uji berpasangan {nama} (ADR-026, Jalur A)",
        "",
        f"> {PEMBATAS}",
        "",
    ]
    if catatan:
        md += [catatan, ""]
    md += ["## Hasil", ""]
    md += _baris_md("Tingkat simbol", per_simbol)
    md += _baris_md("Tingkat bulan", per_bulan)
    md += [
        "## Yang tidak dijawab laporan ini",
        "",
        "Putusan sah H-013 menuntut sebaran permutasi **sinyal** atas minimal "
        "300 seed pada sel pembanding (Jalur B ADR-026). Laporan ini hanya "
        "menentukan apakah Jalur B layak dibeli.",
        "",
    ]
    (d / f"{nama}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return isi


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Jalur A ADR-026")
    p.add_argument("--sel-a", required=True, help="JSON laporan sel utama (SS)")
    p.add_argument("--sel-b", required=True, help="JSON laporan sel pembanding (AS)")
    p.add_argument("--nama", default="h013_berpasangan")
    p.add_argument("--ambang", type=float, required=True)
    p.add_argument("--ulangan", type=int, default=ULANGAN)
    p.add_argument("--seed", type=int, default=SEED)
    p.add_argument("--out", default="reports")
    a = p.parse_args(argv)

    isi_a = json.loads(Path(a.sel_a).read_text(encoding="utf-8"))
    isi_b = json.loads(Path(a.sel_b).read_text(encoding="utf-8"))

    rs = ringkas(
        pasangan_simbol(isi_a, isi_b), a.ambang, ulangan=a.ulangan, seed=a.seed
    )
    rb = ringkas(
        pasangan_bulan(isi_a, isi_b), a.ambang, ulangan=a.ulangan, seed=a.seed
    )
    tulis_laporan(
        a.nama,
        rs,
        rb,
        out=a.out,
        catatan=f"Sel A `{a.sel_a}` terhadap sel B `{a.sel_b}`.",
    )
    print(json.dumps({"per_simbol": rs, "per_bulan": rb}, indent=2), flush=True)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
