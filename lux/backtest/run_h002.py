"""Menjalankan hipotesis H-002: batas umur posisi dan saringan carry funding.

H-001b DITOLAK oleh gerbang ``invarian_risiko`` dengan kerugian terburuk
-2,5853R terhadap ambang -1,5R (run 30172926477, laporan
``reports/backtest_h001.md``). Pembongkaran biaya menunjukkan penyebabnya bukan
fee melainkan funding: perdagangan terburuk memuat ``transaksi_R`` 0,026 dan
``funding_R`` 1,545 pada posisi yang dipegang 130 jam.

Berkas ini adalah tanggapan sah atas temuan itu, dan bentuknya penting.

**Yang tidak dilakukan.** Ambang gerbang tidak dilonggarkan. Kriteria H-001b
tidak disunting. H-001b tetap ditolak selamanya dan hasilnya tidak dihitung
ulang. Melonggarkan ambang setelah melihat hasil akan mengubah sembilan gerbang
menjadi angka yang dapat dinegosiasikan, dan seluruh nilainya terletak pada
kenyataan bahwa ia tidak dapat.

**Yang dilakukan.** Hipotesis baru dengan dua saringan kelayakan perdagangan,
didaftarkan sebelum dijalankan, memakai dataset dan ambang yang sama persis
dengan H-001b sehingga satu-satunya perbedaan adalah saringannya. Lihat
``decisions/ADR-004-carry-funding.md``.

**Mengapa berkas terpisah, bukan sebuah flag di run_wf.py.** Menambahkan flag
berarti kode yang menghasilkan H-001b ikut berubah, dan sejak saat itu tidak
ada lagi cara memastikan angka H-001b dapat diulang. Seluruh fungsi pemuatan,
gerbang gabungan, dan pembongkaran biaya diimpor dari ``run_wf`` apa adanya,
jadi kedua hipotesis tetap dinilai oleh kode penilaian yang sama.

Nilai kedua saringan dibaca dari ``config/lux.yaml``, bukan dari argumen baris
perintah, supaya ia tercatat di satu tempat yang wajib disertai alasan di
journal dan ikut masuk ke dalam sidik hipotesis.

Pemakaian:
    python -m lux.backtest.run_h002 --dir aset --interval 1h \\
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
from lux.strategi import breakout_atr


def muat_konfig_h002(path: Path) -> Konfig:
    """Konfig lengkap dengan kedua saringan ADR-004.

    Kunci yang hilang menghasilkan ``KeyError``, bukan nilai bawaan. Diam-diam
    menjalankan H-002 dengan saringan mati akan menghasilkan angka H-001b di
    bawah nama H-002, dan itu adalah kekeliruan yang paling sulit terlihat dari
    laporan.
    """
    import yaml

    with Path(path).open(encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    b, r = cfg["biaya"], cfg["risiko"]
    k = Konfig(
        fee=float(b["fee_efektif"]),
        slippage=float(b["slippage"]),
        atr_periode=int(r["atr_periode"]),
        atr_pengali_stop=float(r["atr_pengali_stop"]),
        risiko_per_trade=float(r["risiko_per_trade"]),
        maks_umur_bar=int(r["maks_umur_bar"]),
        maks_carry_R=float(r["maks_carry_R"]),
        jendela_carry_hari=int(r["jendela_carry_hari"]),
    )
    if k.maks_umur_bar <= 0 or k.maks_carry_R <= 0:
        raise ValueError(
            "H-002 menuntut maks_umur_bar dan maks_carry_R yang positif; "
            "tanpa keduanya yang dijalankan adalah H-001b dengan nama lain"
        )
    return k


def hipotesis_h002(konfig: Konfig, komit: str = "") -> Hipotesis:
    """H-002, dengan ambang kelulusan yang sama persis dengan H-001b.

    Kriteria tidak dilonggarkan satu angka pun. Bila H-002 lulus
    ``invarian_risiko`` tetapi ekspektasinya tetap di bawah 0,05R, kesimpulannya
    adalah breakout Donchian tidak punya keunggulan pada dataset ini, bukan
    bahwa saringannya kurang ketat.

    Nilai kedua saringan masuk ke ruang parameter sebagai daftar satu unsur.
    Keduanya tidak dicari; mereka ditetapkan di muka. Menuliskannya di sini
    membuat sidik hipotesis berubah bila nilainya diubah, sehingga percobaan
    diam-diam dengan nilai lain akan tertolak oleh praregistrasi yang bersifat
    sekali tulis.
    """
    return Hipotesis(
        id="H-002",
        pernyataan=(
            "Penembusan Donchian pada penutupan bar 1 jam menghasilkan ekspektasi "
            "positif setelah fee, slippage, dan funding nyata, bila posisi dibatasi "
            "umurnya dan entri dengan carry funding terproyeksi berlebihan ditolak, "
            "pada perp USDT yang lolos ambang kelayakan, dinilai hanya di luar sampel."
        ),
        dataset=(
            "tier-b-v1 ohlcv_1h + funding_shard, "
            "universe_layak_v2 438 simbol (ADR-003, ekor datar dipangkas)"
        ),
        ruang_parameter=dict(breakout_atr.RUANG_PARAMETER)
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


def banding_h001(path: Path) -> dict | None:
    """Angka pembanding dari laporan H-001b, bila ada.

    Dibaca dari berkas, tidak ditulis ulang dari ingatan. Angka yang diketik
    ulang oleh manusia atau agen adalah angka yang tidak dapat diaudit.
    """
    if not Path(path).exists():
        return None
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    invarian = None
    for g in d.get("gerbang", {}).get("gerbang", []):
        if g.get("nama") == "invarian_risiko":
            invarian = g.get("nilai")
    return {
        "ekspektasi_R": d.get("gabungan", {}).get("ekspektasi_R"),
        "total_R": d.get("gabungan", {}).get("total_R"),
        "jumlah_trade_luar_sampel": d.get("gabungan", {}).get(
            "jumlah_trade_luar_sampel"
        ),
        "invarian_risiko": invarian,
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
    ap.add_argument("--hipotesis", default="hipotesis/H-002.json")
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

    # Config dibaca lebih dulu karena nilainya ikut membentuk hipotesis.
    konfig = muat_konfig_h002(Path(a.config))
    h = hipotesis_h002(konfig, a.komit)
    jalur = simpan(h, a.hipotesis)
    print(f"hipotesis {h.id} terdaftar di {jalur} (sidik {h.sidik()[:12]})", flush=True)
    print(
        f"ruang pencarian: {h.jumlah_kombinasi} kombinasi "
        f"(umur maks {konfig.maks_umur_bar} bar, carry maks {konfig.maks_carry_R}R, "
        f"jendela {konfig.jendela_carry_hari} hari)",
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

    kandidat = breakout_atr.kandidat()
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
            buat_sinyal=breakout_atr.sinyal,
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

    # Berapa banyak posisi yang benar-benar ditutup oleh batas umur. Bila
    # angkanya nol, saringan umur tidak pernah mengikat dan setiap perbaikan
    # yang terlihat berasal dari saringan carry, bukan dari batas umur.
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
            lambda d: breakout_atr.sinyal(d, {"lookback": 55}),
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
            "tidak dapat dinilai: manifest baru ditulis pada run ini; "
            "run berikutnya akan membandingkannya",
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
    banding = banding_h001(Path(a.out) / "backtest_h001.json")

    out = Path(a.out)
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
        "banding_h001b": banding,
        "per_simbol": per_simbol,
        "detik": round(time.time() - t0, 1),
    }
    (out / "backtest_h002.json").write_text(
        json.dumps(isi, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    md = [
        "# Backtest H-002 — batas umur posisi dan saringan carry (ADR-004)",
        "",
        f"> {h.pernyataan}",
        "",
        f"Sidik hipotesis `{h.sidik()[:16]}` \u00b7 ruang {h.jumlah_kombinasi} kombinasi "
        f"\u00b7 {gabungan['jumlah_simbol']} simbol \u00b7 {isi['detik']}s",
        "",
        f"Saringan: umur maksimum **{konfig.maks_umur_bar} bar**, carry terproyeksi "
        f"maksimum **{konfig.maks_carry_R}R** atas jendela "
        f"{konfig.jendela_carry_hari} hari.",
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
    ]

    if banding:
        md += [
            "## Perbandingan dengan H-001b",
            "",
            "Dataset, ambang, dan seluruh kode penilaian identik. Satu-satunya "
            "perbedaan adalah kedua saringan.",
            "",
            "| Besaran | H-001b | H-002 |",
            "|---|---|---|",
            f"| Ekspektasi R | {banding['ekspektasi_R']} | {gabungan['ekspektasi_R']} |",
            f"| Total R | {banding['total_R']} | {round(gabungan['total_R'], 2)} |",
            f"| Trade luar sampel | {banding['jumlah_trade_luar_sampel']} | "
            f"{gabungan['jumlah_trade_luar_sampel']} |",
            f"| Kerugian terburuk (R) | {banding['invarian_risiko']} | "
            f"{gerbang_ir.nilai} |",
            f"| Putusan pra-registrasi | {banding['lulus']} | {putusan.lulus} |",
            "",
        ]

    md += [
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

    md += [
        "",
        "## Pembongkaran biaya",
        "",
    ]
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

    (out / "backtest_h002.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:24]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
