"""Menjalankan hipotesis H-003: pembalikan jangka pendek (ADR-005).

Kerangka eksekusinya sama persis dengan H-002 — stop 2×ATR, target 2R, batas
umur 168 bar, saringan carry 0,25R, dataset dan kriteria identik. Satu-satunya
yang berubah adalah modul sinyalnya, dan arahnya berlawanan.

Itulah seluruh maksud percobaan ini. Bila H-003 lulus, arah taruhan H-001b
memang keliru. Bila H-003 gagal dengan pola yang sama — keunggulan statistik ada
tetapi besarnya di bawah ambang — maka yang tertuduh adalah kerangka stop/target
dan biayanya, bukan arah sinyal, dan pekerjaan berikutnya harus menyerang itu.

Orkestrator ketiga yang berdiri sendiri, mengikuti pola yang sudah mapan: satu
hipotesis, satu orkestrator, dibekukan setelah dijalankan. Seluruh fungsi
pemuatan dan penilaian diimpor dari ``run_wf`` sehingga ketiga hipotesis dinilai
oleh kode yang sama dan perbandingannya sah. Bila orkestrator keempat
dibutuhkan, ekstrak runner bersama lebih dulu.

Pemakaian:
    python -m lux.backtest.run_h003 --dir aset --interval 1h \\
        --universe reports/universe_layak_v2.json \\
        --akhir-sejati reports/akhir_sejati.json \\
        --limit 40
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

from lux.backtest.engine import Hasil, Konfig, jalankan
from lux.backtest.gerbang import (
    Gerbang,
    gerbang_buy_and_hold,
    gerbang_checksum,
    gerbang_entri_acak,
    gerbang_forward_fill,
    gerbang_funding,
    gerbang_invarian_risiko,
    gerbang_lookahead,
    gerbang_survivorship,
    susun_laporan,
)
from lux.backtest.run_h002 import muat_konfig_h002
from lux.backtest.run_wf import (
    akhir_per_simbol,
    diagnosa_biaya,
    gabung_gerbang,
    gerbang_bnh_gabungan,
    gerbang_overlap_gabungan,
    muat_ohlcv,
    ringkas_gabungan,
    sha256_berkas,
    simbol_mati_dari_akhir,
)
from lux.backtest.walk_forward import jalankan_walk_forward
from lux.funding_model import ambil_jadwal, muat_jadwal
from lux.praregistrasi import Hipotesis, Kriteria, nilai, simpan
from lux.strategi import reversi_zskor


def hipotesis_h003(konfig: Konfig, komit: str = "") -> Hipotesis:
    """H-003, kriteria dan dataset identik dengan H-001b dan H-002.

    Tidak satu ambang pun dilonggarkan. Perbandingan tiga hipotesis hanya sah
    bila yang berbeda hanya sinyalnya.
    """
    return Hipotesis(
        id="H-003",
        pernyataan=(
            "Pembalikan jangka pendek — membeli penutupan yang jatuh dua simpangan "
            "baku di bawah rerata bergulir dan menjual yang melonjak dua simpangan "
            "baku di atasnya — menghasilkan ekspektasi positif setelah fee, "
            "slippage, dan funding nyata, pada kerangka eksekusi yang sama persis "
            "dengan H-002, dinilai hanya di luar sampel."
        ),
        dataset=(
            "tier-b-v1 ohlcv_1h + funding_shard, "
            "universe_layak_v2 438 simbol (ADR-003, ekor datar dipangkas)"
        ),
        ruang_parameter=dict(reversi_zskor.RUANG_PARAMETER)
        | {
            "maks_umur_bar": [konfig.maks_umur_bar],
            "maks_carry_R": [konfig.maks_carry_R],
            "jendela_carry_hari": [konfig.jendela_carry_hari],
        },
        kriteria=Kriteria(
            min_ekspektasi_R=0.05,
            min_trade_luar_sampel=100,
            maks_p_entri_acak=0.05,
            min_jendela_positif_rasio=0.5,
        ),
        komit=komit,
    )


def banding(path: Path, label: str) -> dict | None:
    """Angka pembanding dibaca dari laporan, tidak pernah diketik ulang."""
    if not Path(path).exists():
        return None
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    invarian = None
    p_acak = None
    for g in d.get("gerbang", {}).get("gerbang", []):
        if g.get("nama") == "invarian_risiko":
            invarian = g.get("nilai")
        if g.get("nama") == "entri_acak":
            p_acak = g.get("nilai")
    return {
        "label": label,
        "ekspektasi_R": d.get("gabungan", {}).get("ekspektasi_R"),
        "total_R": d.get("gabungan", {}).get("total_R"),
        "jumlah_trade_luar_sampel": d.get("gabungan", {}).get(
            "jumlah_trade_luar_sampel"
        ),
        "invarian_risiko": invarian,
        "p_entri_acak": p_acak,
        "lulus": d.get("putusan", {}).get("lulus"),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--interval", default="1h")
    ap.add_argument("--universe", default="reports/universe_layak_v2.json")
    ap.add_argument("--akhir-sejati", default="reports/akhir_sejati.json")
    ap.add_argument("--config", default="config/lux.yaml")
    ap.add_argument("--out", default="reports")
    ap.add_argument("--hipotesis", default="hipotesis/H-003.json")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--panjang-latih", type=int, default=4320)
    ap.add_argument("--panjang-uji", type=int, default=2160)
    ap.add_argument("--embargo", type=int, default=168)
    ap.add_argument("--pemanasan", type=int, default=200)
    ap.add_argument("--ulangan", type=int, default=100)
    ap.add_argument("--sampel-permutasi", type=int, default=10)
    ap.add_argument("--komit", default="")
    a = ap.parse_args(argv)

    t0 = time.time()

    konfig = muat_konfig_h002(Path(a.config))
    h = hipotesis_h003(konfig, a.komit)
    jalur = simpan(h, a.hipotesis)
    print(f"hipotesis {h.id} terdaftar di {jalur} (sidik {h.sidik()[:12]})", flush=True)
    print(
        f"ruang pencarian: {h.jumlah_kombinasi} kombinasi "
        f"(jendela {reversi_zskor.RUANG_PARAMETER['jendela']}, "
        f"ambang {reversi_zskor.AMBANG_BAKU})",
        flush=True,
    )

    semesta = json.loads(Path(a.universe).read_text(encoding="utf-8"))["simbol"]
    dipilih = sorted(semesta)[: a.limit] if a.limit > 0 else sorted(semesta)
    print(f"universe layak {len(semesta)}, diuji {len(dipilih)}", flush=True)

    bingkai, berkas = muat_ohlcv(Path(a.dir), a.interval, set(dipilih))
    jadwal_semua = muat_jadwal(Path(a.dir))
    akhir_semesta = akhir_per_simbol(Path(a.dir), a.interval, Path(a.akhir_sejati))
    print(
        f"{len(bingkai)} simbol dimuat, {len(jadwal_semua)} jadwal funding, "
        f"{len(akhir_semesta)} simbol dipindai untuk survivorship",
        flush=True,
    )

    sampel = set(sorted(bingkai)[: a.sampel_permutasi])

    kandidat = reversi_zskor.kandidat()
    ringkasan_simbol: list[dict] = []
    per_simbol: list[dict] = []
    semua_trade = []
    hasil_per_simbol: dict[str, Hasil] = {}
    jendela_sampel: list[tuple[pd.DataFrame, np.ndarray, str]] = []
    g_forward: list[Gerbang] = []
    nama_forward: list[str] = []
    g_bnh: list[Gerbang] = []

    for i, s in enumerate(sorted(bingkai), 1):
        df = bingkai[s]
        try:
            jadwal = ambil_jadwal(jadwal_semua, s)
        except KeyError as e:
            print(f"  [{i}] {s}: DILEWATI, {e}", flush=True)
            continue

        wf = jalankan_walk_forward(
            df,
            kandidat=kandidat,
            buat_sinyal=reversi_zskor.sinyal,
            panjang_latih=a.panjang_latih,
            panjang_uji=a.panjang_uji,
            embargo=a.embargo,
            pemanasan=a.pemanasan,
            konfig=konfig,
            jadwal=jadwal,
            symbol=s,
            simpan_bingkai=s in sampel,
        )
        r = wf.ringkas()
        trade_simbol = wf.perdagangan_luar_sampel
        ringkasan_simbol.append(r)
        semua_trade.extend(trade_simbol)
        hasil_per_simbol[s] = Hasil(symbol=s, perdagangan=trade_simbol)
        per_simbol.append(
            {
                "symbol": s,
                "bar": int(len(df)),
                "jendela": r["jumlah_jendela"],
                "trade": r["jumlah_trade_luar_sampel"],
                "total_R": round(r["total_R"], 4),
                "ekspektasi_R": (
                    None if r["ekspektasi_R"] is None else round(r["ekspektasi_R"], 5)
                ),
                "parameter": r["parameter_per_jendela"],
            }
        )

        g_forward.append(gerbang_forward_fill(df))
        nama_forward.append(s)

        if wf.per_jendela and trade_simbol:
            awal_uji = wf.per_jendela[0].jendela.uji_awal
            akhir_uji = wf.per_jendela[-1].jendela.uji_akhir
            laba = float(sum(p.laba for p in trade_simbol))
            g_bnh.append(
                gerbang_buy_and_hold(
                    Hasil(
                        symbol=s,
                        perdagangan=trade_simbol,
                        ekuitas=np.array([konfig.modal_awal, konfig.modal_awal + laba]),
                    ),
                    df.iloc[awal_uji:akhir_uji],
                )
            )

        for hj in wf.per_jendela:
            if hj.bingkai_uji is not None and hj.sinyal_uji is not None:
                jendela_sampel.append((hj.bingkai_uji, hj.sinyal_uji, s))

        if i % 5 == 0 or i == len(bingkai):
            print(
                f"  [{i}/{len(bingkai)}] {s}: {r['jumlah_trade_luar_sampel']} trade, "
                f"{time.time() - t0:.0f}s",
                flush=True,
            )

    gabungan = ringkas_gabungan(ringkasan_simbol)
    print(json.dumps(gabungan, indent=2), flush=True)

    diagnosa = diagnosa_biaya(semua_trade)
    print(
        "biaya rerata: transaksi "
        f"{diagnosa['rerata_transaksi_R']}R, funding {diagnosa['rerata_funding_R']}R, "
        f"{diagnosa['trade_biaya_lebih_1R']} trade berbiaya di atas 1R",
        flush=True,
    )

    alasan: dict[str, int] = {}
    for p in semua_trade:
        alasan[p.alasan_keluar] = alasan.get(p.alasan_keluar, 0) + 1
    print(f"alasan keluar: {alasan}", flush=True)

    hasil_pool = Hasil(
        symbol="POOL",
        perdagangan=semua_trade,
        ekuitas=np.array([konfig.modal_awal]),
    )

    gerbang_ff = gabung_gerbang("forward_fill", g_forward, 0.30, nama_forward)
    gerbang_bnh = gerbang_bnh_gabungan(g_bnh)

    p_acak: float | None = None
    if jendela_sampel:
        panjang = [len(s_) for _, s_, _ in jendela_sampel]
        batas = np.cumsum([0] + panjang)
        sinyal_gabung = np.concatenate([s_ for _, s_, _ in jendela_sampel])

        def penilai(sinyal_acak: np.ndarray) -> float:
            rs = []
            for k, (bingkai_j, _, sym) in enumerate(jendela_sampel):
                potong = sinyal_acak[batas[k] : batas[k + 1]]
                hasil_j = jalankan(
                    bingkai_j,
                    potong,
                    konfig,
                    jadwal=jadwal_semua.get(sym),
                    symbol=sym,
                )
                rs.extend(p.R for p in hasil_j.perdagangan)
            return float(np.mean(rs)) if rs else float("-inf")

        nyata = penilai(sinyal_gabung)
        gerbang_acak = gerbang_entri_acak(
            nyata, sinyal_gabung, penilai, ulangan=a.ulangan
        )
        p_acak = gerbang_acak.nilai
        print(
            f"entri acak: nyata {nyata:.5f}R, p {p_acak}, {time.time() - t0:.0f}s",
            flush=True,
        )
    else:
        gerbang_acak = Gerbang(
            "entri_acak",
            False,
            None,
            None,
            "tidak dapat dinilai: tidak ada jendela sampel",
        )

    if bingkai:
        contoh = bingkai[sorted(bingkai)[0]]
        gerbang_la = gerbang_lookahead(
            contoh.iloc[:5000],
            lambda d: reversi_zskor.sinyal(d, {"jendela": 72, "ambang": 2.0}),
        )
    else:
        gerbang_la = Gerbang(
            "lookahead", False, None, None, "tidak dapat dinilai: tidak ada data"
        )

    gerbang_ir = gerbang_invarian_risiko(hasil_pool)
    gerbang_fd = gerbang_funding(hasil_pool, jadwal_dimuat=bool(jadwal_semua))
    gerbang_ov = gerbang_overlap_gabungan(hasil_per_simbol)

    manifest_path = Path(a.out) / "manifest_aset.json"
    terhitung = {p.name: sha256_berkas(p) for p in berkas}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        gerbang_cs = gerbang_checksum(manifest, terhitung)
    else:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(terhitung, indent=2, sort_keys=True), encoding="utf-8"
        )
        gerbang_cs = Gerbang(
            "checksum",
            False,
            None,
            None,
            "tidak dapat dinilai: manifest baru ditulis pada run ini",
        )

    semesta_layak = [s for s in semesta if s in akhir_semesta]
    mati = simbol_mati_dari_akhir({s: akhir_semesta[s] for s in semesta_layak})
    gerbang_sv = gerbang_survivorship(
        simbol_diuji=[r["symbol"] for r in ringkasan_simbol],
        simbol_delisted=mati,
        simbol_universe=semesta_layak,
    )

    laporan = susun_laporan(
        [
            gerbang_ff,
            gerbang_bnh,
            gerbang_acak,
            gerbang_la,
            gerbang_ir,
            gerbang_fd,
            gerbang_ov,
            gerbang_cs,
            gerbang_sv,
        ]
    )
    putusan = nilai(h, gabungan, p_acak)
    out = Path(a.out)
    pembanding = [
        b
        for b in (
            banding(out / "backtest_h001.json", "H-001b"),
            banding(out / "backtest_h002.json", "H-002"),
        )
        if b
    ]

    out.mkdir(parents=True, exist_ok=True)
    isi = {
        "hipotesis": h.ke_dict() | {"sidik": h.sidik()},
        "parameter_run": {
            "interval": a.interval,
            "limit": a.limit,
            "panjang_latih": a.panjang_latih,
            "panjang_uji": a.panjang_uji,
            "embargo": a.embargo,
            "pemanasan": a.pemanasan,
            "ulangan_permutasi": a.ulangan,
            "sampel_permutasi": sorted(sampel),
            "simbol_mati_di_universe": len(mati),
            "maks_umur_bar": konfig.maks_umur_bar,
            "maks_carry_R": konfig.maks_carry_R,
            "jendela_carry_hari": konfig.jendela_carry_hari,
        },
        "gabungan": gabungan,
        "alasan_keluar": alasan,
        "diagnosa_biaya": diagnosa,
        "gerbang": laporan.ke_dict(),
        "putusan": {"lulus": putusan.lulus, "alasan": putusan.alasan},
        "pembanding": pembanding,
        "per_simbol": per_simbol,
        "detik": round(time.time() - t0, 1),
    }
    (out / "backtest_h003.json").write_text(
        json.dumps(isi, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    md = [
        "# Backtest H-003 — pembalikan jangka pendek (ADR-005)",
        "",
        f"> {h.pernyataan}",
        "",
        f"Sidik hipotesis `{h.sidik()[:16]}` \u00b7 ruang {h.jumlah_kombinasi} kombinasi "
        f"\u00b7 {gabungan['jumlah_simbol']} simbol \u00b7 {isi['detik']}s",
        "",
        "Kerangka eksekusi identik H-002. Yang berbeda hanya sinyalnya, dan arahnya "
        "berlawanan.",
        "",
        "## Putusan",
        "",
        f"**{'LULUS' if putusan.lulus and laporan.semua_lulus else 'DITOLAK'}**",
        "",
    ]
    if putusan.alasan:
        md += ["Kriteria pra-registrasi yang tidak terpenuhi:", ""]
        md += [f"- {al}" for al in putusan.alasan]
        md += [""]
    if laporan.yang_gagal:
        md += [f"Gerbang gagal: {', '.join(laporan.yang_gagal)}", ""]

    md += [
        "## Hasil luar sampel",
        "",
        f"- Perdagangan: **{gabungan['jumlah_trade_luar_sampel']:,}**",
        f"- Total R: **{gabungan['total_R']:.2f}**",
        f"- Ekspektasi: **{gabungan['ekspektasi_R']}**",
        f"- Jendela positif: {gabungan['jendela_positif']}/{gabungan['jumlah_jendela']}",
        f"- Alasan keluar: {alasan}",
        "",
        "## Perbandingan tiga hipotesis",
        "",
        "Dataset, kriteria, dan kode penilaian identik pada ketiganya.",
        "",
        "| Besaran | "
        + " | ".join([b["label"] for b in pembanding] + ["H-003"])
        + " |",
        "|---" * (len(pembanding) + 2) + "|",
        "| Ekspektasi R | "
        + " | ".join(
            [f"{b['ekspektasi_R']}" for b in pembanding]
            + [f"{gabungan['ekspektasi_R']}"]
        )
        + " |",
        "| Total R | "
        + " | ".join(
            [f"{b['total_R']}" for b in pembanding] + [f"{gabungan['total_R']:.2f}"]
        )
        + " |",
        "| Trade luar sampel | "
        + " | ".join(
            [f"{b['jumlah_trade_luar_sampel']}" for b in pembanding]
            + [f"{gabungan['jumlah_trade_luar_sampel']}"]
        )
        + " |",
        "| Kerugian terburuk R | "
        + " | ".join(
            [f"{b['invarian_risiko']}" for b in pembanding] + [f"{gerbang_ir.nilai}"]
        )
        + " |",
        "| p entri acak | "
        + " | ".join([f"{b['p_entri_acak']}" for b in pembanding] + [f"{p_acak}"])
        + " |",
        "| Putusan | "
        + " | ".join([f"{b['lulus']}" for b in pembanding] + [f"{putusan.lulus}"])
        + " |",
        "",
        "## Sembilan gerbang",
        "",
        "| Gerbang | Putusan | Nilai | Ambang | Catatan |",
        "|---|---|---|---|---|",
    ]
    for g in laporan.gerbang:
        n = "\u2014" if g.nilai is None else f"{g.nilai:.4f}"
        am = "\u2014" if g.ambang is None else f"{g.ambang}"
        md.append(
            f"| {g.nama} | {'lulus' if g.lulus else 'GAGAL'} | {n} | {am} | {g.catatan} |"
        )

    md += ["", "## Pembongkaran biaya", ""]
    if diagnosa["jumlah"]:
        md += [
            f"- Rerata biaya transaksi: **{diagnosa['rerata_transaksi_R']:.4f}R**",
            f"- Rerata biaya funding: **{diagnosa['rerata_funding_R']:.4f}R**",
            f"- Rerata jarak stop terhadap harga: "
            f"**{diagnosa['rerata_stop_frac'] * 100:.3f}%**",
            f"- Perdagangan dengan biaya melebihi 1R: "
            f"**{diagnosa['trade_biaya_lebih_1R']:,}** dari {diagnosa['jumlah']:,}",
            "",
            "| Simbol | R | Kotor R | Transaksi R | Funding R | Stop % harga | Jam | Alasan |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for r in diagnosa["terburuk"]:
            md.append(
                f"| {r['symbol']} | {r['R']:.3f} | {r['kotor_R']:.3f} | "
                f"{r['transaksi_R']:.3f} | {r['funding_R']:.3f} | "
                f"{r['stop_frac'] * 100:.3f} | {r['jam']:.1f} | {r['alasan']} |"
            )
    else:
        md += ["Tidak ada perdagangan untuk dibongkar."]

    md += [
        "",
        "## Sepuluh simbol dengan total R tertinggi",
        "",
        "| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |",
        "|---|---|---|---|---|---|",
    ]
    for r in sorted(per_simbol, key=lambda x: -x["total_R"])[:10]:
        md.append(
            f"| {r['symbol']} | {r['bar']:,} | {r['jendela']} | {r['trade']} | "
            f"{r['total_R']:.2f} | {r['ekspektasi_R']} |"
        )
    md += [
        "",
        "## Sepuluh simbol dengan total R terendah",
        "",
        "| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |",
        "|---|---|---|---|---|---|",
    ]
    for r in sorted(per_simbol, key=lambda x: x["total_R"])[:10]:
        md.append(
            f"| {r['symbol']} | {r['bar']:,} | {r['jendela']} | {r['trade']} | "
            f"{r['total_R']:.2f} | {r['ekspektasi_R']} |"
        )

    (out / "backtest_h003.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:24]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
