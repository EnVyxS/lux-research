"""H-007 — struktur keluar, sinyal tidak diubah sama sekali (ADR-007).

Enam hipotesis sebelumnya menggeser laju kena target sambil membiarkan titik
impas tetap di 1/3. Modul ini menggeser titik impasnya, dengan memperlakukan
``imbalan_R`` sebagai parameter yang dipilih walk-forward bersama ``lookback``.

``lux/strategi/`` tidak disentuh. Itu disengaja: ADR-006 melarang sinyal harga
ketujuh, dan cara paling jelas untuk membuktikan larangan itu dihormati adalah
tidak menulis satu baris pun sinyal baru.

Pemakaian:
    python -m lux.backtest.run_h007 --dir aset --limit 40
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path

from lux.analisis.titik_impas import ringkas_laporan, titik_impas
from lux.backtest.engine import Konfig
from lux.backtest.run_h002 import muat_konfig_h002
from lux.backtest.runner import Opsi, Spek, jalankan_spek, muat_konteks
from lux.backtest.run_wf import hipotesis_h001
from lux.praregistrasi import Hipotesis, Kriteria
from lux.strategi import breakout_atr

LOOKBACK = [20, 55, 100]
IMBALAN = [1.0, 2.0, 3.0, 4.0]

DATASET = (
    "tier-b-v1 ohlcv_1h + funding_shard, "
    "universe_layak_v2 438 simbol (ADR-003, ekor datar dipangkas)"
)


def kandidat() -> list[dict]:
    return [{"lookback": lb, "imbalan_R": im} for lb in LOOKBACK for im in IMBALAN]


def buat_konfig(params: dict, dasar: Konfig) -> Konfig:
    """Konfig per kandidat: hanya imbalan yang berubah.

    Seluruh medan lain — fee, slippage, pengali stop, saringan carry ADR-004 —
    diwarisi apa adanya. Bila ada yang ikut berubah diam-diam di sini, H-007
    tidak lagi dapat dibandingkan dengan H-002 dan seluruh ADR-007 kehilangan
    dasarnya.
    """
    return replace(dasar, imbalan_R=float(params["imbalan_R"]))


def hipotesis_h007(konfig: Konfig, komit: str = "") -> Hipotesis:
    return Hipotesis(
        id="H-007",
        pernyataan=(
            "Dengan sinyal Donchian yang tidak diubah sama sekali, memperlakukan "
            "rasio imbalan sebagai parameter yang dipilih walk-forward "
            "menghasilkan ekspektasi bersih di luar sampel minimal 0,05R. "
            "Yang diuji adalah titik impas, bukan sinyal: titik impas kotor "
            "adalah 1/(1+imbalan), sehingga imbalan 3R menurunkannya dari 0,333 "
            "ke 0,250."
        ),
        dataset=DATASET,
        ruang_parameter={
            "lookback": LOOKBACK,
            "imbalan_R": IMBALAN,
            "atr_pengali_stop": [konfig.atr_pengali_stop],
            "maks_umur_bar": [konfig.maks_umur_bar],
            "maks_carry_R": [konfig.maks_carry_R],
            "jendela_carry_hari": [konfig.jendela_carry_hari],
        },
        # Percobaan tunggal, jadi tidak ada koreksi multiplisitas. Kriterianya
        # sama persis dengan H-001b.
        kriteria=Kriteria(
            min_ekspektasi_R=0.05,
            min_trade_luar_sampel=100,
            maks_p_entri_acak=0.05,
            min_jendela_positif_rasio=0.5,
        ),
        komit=komit,
    )


def spek_h007(konfig: Konfig, komit: str = "") -> Spek:
    return Spek(
        h=hipotesis_h007(konfig, komit),
        sinyal=breakout_atr.sinyal,
        kandidat=kandidat(),
        nama="h007_keluar",
        params_lookahead={"lookback": 55},
        buat_konfig=buat_konfig,
    )


# Pembanding tetap, disalin dari laporan yang sudah dikomit. Tidak satu pun
# dijalankan ulang.
PEMBANDING = [
    ("H-002", "Donchian + saringan carry", {"target": 6707, "stop": 11909}, 0.03159),
    ("H-004", "+ ADX >= 30", {"target": 2659, "stop": 5127}, -0.01818),
    ("H-005", "entri retest", {"target": 4057, "stop": 7962}, -0.03571),
    ("H-006", "sapuan likuiditas", {"target": 6032, "stop": 13993}, -0.13449),
    ("H-003", "pembalikan skor-z", {"target": 7503, "stop": 20997}, -0.24782),
]


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

    print("titik impas kotor per imbalan:", flush=True)
    for im in IMBALAN:
        print(f"  {im}R -> {titik_impas(im):.4f}", flush=True)

    ktx = muat_konteks(opsi)
    hasil = jalankan_spek(spek_h007(konfig, a.komit), ktx, konfig, opsi)

    # Aritmetika titik impas atas hasil sendiri dan seluruh pembanding.
    # Imbalan H-007 berbeda antar jendela, jadi bongkarannya memakai imbalan
    # dasar dan hanya berlaku sebagai perkiraan; itu dinyatakan terus terang
    # alih-alih disembunyikan.
    baris = []
    for id_, label, alasan, bersih in PEMBANDING:
        r = ringkas_laporan(alasan, bersih, imbalan=2.0)
        baris.append((id_, label, "2,0", r))
    try:
        r_h007 = ringkas_laporan(
            hasil["alasan_keluar"], hasil["ekspektasi_R"] or 0.0, imbalan=2.0
        )
        baris.append(("H-007", "imbalan dipilih WF", "campuran", r_h007))
    except ValueError as e:
        print(f"bongkaran titik impas H-007 dilewati: {e}", flush=True)

    md = [
        "# Titik impas — bongkaran seluruh hipotesis",
        "",
        "Dengan stop 1R dan target sebesar imbalan, ekspektasi kotor adalah "
        "`p·imbalan − (1−p)` dan titik impas kotor adalah `1/(1+imbalan)`. "
        "Sebaran hasilnya terpotong di kedua sisi, sehingga tidak ada ekor "
        "panjang yang dapat menyelamatkan ekspektasi.",
        "",
        "| Hipotesis | Mekanisme | Imbalan | Laju kena target | Kotor | Bersih | Seretan | Laju dibutuhkan |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for id_, label, im, r in baris:
        md.append(
            f"| {id_} | {label} | {im} | {r['laju_kena_target']:.5f} | "
            f"{r['ekspektasi_kotor']:+.5f} | {r['ekspektasi_bersih']:+.5f} | "
            f"{r['seretan_tersirat']:.5f} | {r['laju_dibutuhkan']:.5f} |"
        )
    md += [
        "",
        "\"Laju dibutuhkan\" adalah laju kena target yang diperlukan untuk "
        "mencapai ekspektasi bersih 0,05R dengan seretan biaya yang sama.",
        "",
    ]

    out = Path(a.out)
    (out / "titik_impas.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (out / "titik_impas.json").write_text(
        json.dumps(
            [
                {"id": id_, "mekanisme": label, "imbalan": im} | r
                for id_, label, im, r in baris
            ],
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print("\n".join(md), flush=True)

    assert hipotesis_h001().dataset == DATASET, "dataset harus identik"
    return 0


if __name__ == "__main__":
    sys.exit(main())
