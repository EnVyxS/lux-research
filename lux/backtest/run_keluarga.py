"""Menjalankan keluarga H-004, H-005, H-006 dalam satu run (ADR-006).

Ketiganya didaftarkan sebelum dijalankan dan seluruhnya dilaporkan, lulus maupun
gagal. Karena tiga percobaan dilakukan sekaligus, ambang `maks_p_entri_acak`
diperketat ke 0,05/3 = 0,0167 di muka, bukan setelah melihat hasil.

Pemakaian:
    python -m lux.backtest.run_keluarga --dir aset --limit 40
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from lux.backtest.engine import Konfig
from lux.backtest.run_h002 import muat_konfig_h002
from lux.backtest.runner import Konteks, Opsi, Spek, jalankan_spek, muat_konteks
from lux.praregistrasi import Hipotesis, Kriteria
from lux.strategi import retest, rezim_adx, smc

# Koreksi Bonferroni untuk tiga percobaan serentak, ditetapkan ADR-006 sebelum
# satu angka pun terlihat.
JUMLAH_PERCOBAAN = 3
AMBANG_P = round(0.05 / JUMLAH_PERCOBAAN, 4)

DATASET = (
    "tier-b-v1 ohlcv_1h + funding_shard, "
    "universe_layak_v2 438 simbol (ADR-003, ekor datar dipangkas)"
)


def kriteria() -> Kriteria:
    """Sama dengan H-001b kecuali ambang p yang lebih ketat."""
    return Kriteria(
        min_ekspektasi_R=0.05,
        min_trade_luar_sampel=100,
        maks_p_entri_acak=AMBANG_P,
        min_jendela_positif_rasio=0.5,
    )


def _ruang(dasar: dict, konfig: Konfig) -> dict:
    return dict(dasar) | {
        "maks_umur_bar": [konfig.maks_umur_bar],
        "maks_carry_R": [konfig.maks_carry_R],
        "jendela_carry_hari": [konfig.jendela_carry_hari],
    }


def spek_h004(konfig: Konfig, komit: str = "") -> Spek:
    h = Hipotesis(
        id="H-004",
        pernyataan=(
            "Penembusan Donchian yang hanya diperdagangkan saat ADX(14) berada di "
            "30 atau lebih menghasilkan ekspektasi positif setelah biaya nyata, "
            "pada kerangka eksekusi yang sama persis dengan H-002."
        ),
        dataset=DATASET,
        ruang_parameter=_ruang(rezim_adx.RUANG_PARAMETER, konfig),
        kriteria=kriteria(),
        komit=komit,
    )
    return Spek(
        h=h,
        sinyal=rezim_adx.sinyal,
        kandidat=rezim_adx.kandidat(),
        nama="h004_adx",
        params_lookahead={"lookback": 55, "adx_min": rezim_adx.AMBANG_ADX},
    )


def spek_h005(konfig: Konfig, komit: str = "") -> Spek:
    h = Hipotesis(
        id="H-005",
        pernyataan=(
            "Menunda entri sampai harga kembali menyentuh level Donchian 55 yang "
            "baru ditembus lalu menutup di sisi penembusan menghasilkan ekspektasi "
            "positif setelah biaya nyata, pada kerangka eksekusi yang sama persis "
            "dengan H-002."
        ),
        dataset=DATASET,
        ruang_parameter=_ruang(retest.RUANG_PARAMETER, konfig),
        kriteria=kriteria(),
        komit=komit,
    )
    return Spek(
        h=h,
        sinyal=retest.sinyal,
        kandidat=retest.kandidat(),
        nama="h005_retest",
        params_lookahead={"jendela_retest": 12, "lookback": retest.LOOKBACK},
    )


def spek_h006(konfig: Konfig, komit: str = "") -> Spek:
    h = Hipotesis(
        id="H-006",
        pernyataan=(
            "Sapuan likuiditas — sumbu yang menembus ekstrem N bar sebelumnya lalu "
            "ditutup kembali ke dalam rentang, diperdagangkan berlawanan arah "
            "sapuan — menghasilkan ekspektasi positif setelah biaya nyata, pada "
            "kerangka eksekusi yang sama persis dengan H-002."
        ),
        dataset=DATASET,
        ruang_parameter=_ruang(smc.RUANG_PARAMETER, konfig),
        kriteria=kriteria(),
        komit=komit,
    )
    return Spek(
        h=h,
        sinyal=smc.sinyal,
        kandidat=smc.kandidat(),
        nama="h006_smc",
        params_lookahead={"jendela": 50},
    )


def semua_spek(konfig: Konfig, komit: str = "") -> list[Spek]:
    return [spek_h004(konfig, komit), spek_h005(konfig, komit), spek_h006(konfig, komit)]


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

    t0 = time.time()
    konfig = muat_konfig_h002(Path(a.config))
    opsi = Opsi(
        dir_aset=Path(a.dir),
        out=Path(a.out),
        interval=a.interval,
        universe=Path(a.universe),
        akhir_sejati=Path(a.akhir_sejati),
        limit=a.limit,
        ulangan=a.ulangan,
    )

    print(
        f"keluarga ADR-006: {JUMLAH_PERCOBAAN} hipotesis, ambang p entri acak "
        f"{AMBANG_P} (Bonferroni)",
        flush=True,
    )
    ktx = muat_konteks(opsi)

    hasil = [jalankan_spek(s, ktx, konfig, opsi) for s in semua_spek(konfig, a.komit)]

    out = Path(a.out)
    (out / "keluarga_adr006.json").write_text(
        json.dumps(
            {
                "ambang_p_bonferroni": AMBANG_P,
                "jumlah_percobaan": JUMLAH_PERCOBAAN,
                "hasil": hasil,
                "detik": round(time.time() - t0, 1),
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    md = [
        "# Keluarga ADR-006 — H-004, H-005, H-006",
        "",
        f"Tiga hipotesis dijalankan serentak pada kerangka eksekusi identik H-002. "
        f"Ambang `p entri acak` diperketat ke **{AMBANG_P}** (Bonferroni 0,05/3) "
        f"sebelum hasil terlihat.",
        "",
        "| Hipotesis | Mekanisme | Ekspektasi R | Total R | Trade | Jendela + | p acak | Putusan |",
        "|---|---|---|---|---|---|---|---|",
    ]
    label = {
        "H-004": "breakout + ADX ≥ 30",
        "H-005": "entri retest (sniper)",
        "H-006": "sapuan likuiditas (SMC)",
    }
    for r in hasil:
        eks = "—" if r["ekspektasi_R"] is None else f"{r['ekspektasi_R']:.5f}"
        p = "—" if r["p_entri_acak"] is None else f"{r['p_entri_acak']:.4f}"
        md.append(
            f"| {r['id']} | {label.get(r['id'], '')} | {eks} | {r['total_R']:.2f} | "
            f"{r['trade']:,} | {r['jendela_positif']}/{r['jumlah_jendela']} | {p} | "
            f"{'LULUS' if r['lulus'] else 'DITOLAK'} |"
        )

    md += ["", "## Alasan penolakan", ""]
    for r in hasil:
        md.append(f"**{r['id']}** — {label.get(r['id'], '')}")
        if r["gerbang_gagal"]:
            md.append(f"- Gerbang gagal: {', '.join(r['gerbang_gagal'])}")
        for al in r["alasan"]:
            md.append(f"- {al}")
        if not r["gerbang_gagal"] and not r["alasan"]:
            md.append("- tidak ada; hipotesis ini lulus")
        md.append("")

    md += [
        "## Pembanding tetap",
        "",
        "| Hipotesis | Ekspektasi R | Putusan |",
        "|---|---|---|",
        "| H-001b Donchian | 0,03086 | DITOLAK |",
        "| H-002 Donchian + saringan carry | 0,03159 | DITOLAK |",
        "| H-003 pembalikan skor-z | −0,24782 | DITOLAK |",
        "",
        "Angka pembanding disalin dari laporan yang sudah dikomit; ketiganya "
        "tidak dijalankan ulang.",
    ]

    (out / "keluarga_adr006.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
