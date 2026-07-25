"""Runner bersama untuk keluarga hipotesis (ADR-006).

ADR-005 mensyaratkan ekstraksi ini sebelum orkestrator keempat dibuat, dan
syaratnya dipenuhi di sini. Tiga orkestrator lama — ``run_wf`` (H-001b),
``run_h002``, ``run_h003`` — **tidak disentuh**, sehingga angka lama tetap dapat
diulang. Modul ini mengimpor fungsi penilaian dari ``run_wf`` seperti mereka,
jadi seluruh hipotesis dinilai oleh kode yang sama.

Data dimuat sekali untuk seluruh keluarga. Selain hemat waktu, itu menjamin
semua hipotesis melihat kumpulan berkas yang identik, sehingga gerbang
``checksum`` cukup dinilai sekali dan perbandingan antar hipotesis sah.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

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
from lux.praregistrasi import Hipotesis, nilai, simpan


@dataclass
class Opsi:
    """Parameter run yang berlaku sama untuk seluruh keluarga.

    Nilai bawaannya sengaja sama persis dengan H-002 dan H-003. Mengubah salah
    satunya membuat perbandingan antar hipotesis tidak sah.
    """

    dir_aset: Path
    out: Path = Path("reports")
    interval: str = "1h"
    universe: Path = Path("reports/universe_layak_v2.json")
    akhir_sejati: Path = Path("reports/akhir_sejati.json")
    limit: int = 40
    panjang_latih: int = 4320
    panjang_uji: int = 2160
    embargo: int = 168
    pemanasan: int = 200
    ulangan: int = 100
    sampel_permutasi: int = 10


@dataclass
class Konteks:
    """Data yang dimuat sekali dan dipakai seluruh keluarga."""

    bingkai: dict[str, pd.DataFrame]
    jadwal: dict
    akhir: dict
    semesta: list[str]
    sampel: set[str]
    gerbang_cs: Gerbang
    semesta_layak: list[str]
    mati: list[str]


@dataclass
class Spek:
    """Satu hipotesis beserta sinyalnya."""

    h: Hipotesis
    sinyal: Callable[[pd.DataFrame, dict], np.ndarray]
    kandidat: list[dict]
    nama: str
    params_lookahead: dict = field(default_factory=dict)


def muat_konteks(opsi: Opsi) -> Konteks:
    semesta = json.loads(Path(opsi.universe).read_text(encoding="utf-8"))["simbol"]
    dipilih = sorted(semesta)[: opsi.limit] if opsi.limit > 0 else sorted(semesta)
    print(f"universe layak {len(semesta)}, diuji {len(dipilih)}", flush=True)

    bingkai, berkas = muat_ohlcv(Path(opsi.dir_aset), opsi.interval, set(dipilih))
    jadwal = muat_jadwal(Path(opsi.dir_aset))
    akhir = akhir_per_simbol(
        Path(opsi.dir_aset), opsi.interval, Path(opsi.akhir_sejati)
    )
    print(
        f"{len(bingkai)} simbol dimuat, {len(jadwal)} jadwal funding, "
        f"{len(akhir)} simbol dipindai untuk survivorship",
        flush=True,
    )

    # Checksum dinilai sekali: berkasnya sama untuk seluruh keluarga.
    manifest_path = Path(opsi.out) / "manifest_aset.json"
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
    print(f"checksum: {gerbang_cs.catatan}", flush=True)

    semesta_layak = [s for s in semesta if s in akhir]
    mati = simbol_mati_dari_akhir({s: akhir[s] for s in semesta_layak})

    return Konteks(
        bingkai=bingkai,
        jadwal=jadwal,
        akhir=akhir,
        semesta=semesta,
        sampel=set(sorted(bingkai)[: opsi.sampel_permutasi]),
        gerbang_cs=gerbang_cs,
        semesta_layak=semesta_layak,
        mati=mati,
    )


def jalankan_spek(
    spek: Spek, ktx: Konteks, konfig: Konfig, opsi: Opsi
) -> dict:
    """Menjalankan satu hipotesis sampai putusan dan menulis laporannya."""
    t0 = time.time()
    jalur = simpan(spek.h, f"hipotesis/{spek.h.id}.json")
    print(
        f"\n=== {spek.h.id} terdaftar di {jalur} (sidik {spek.h.sidik()[:12]}, "
        f"{spek.h.jumlah_kombinasi} kombinasi) ===",
        flush=True,
    )

    ringkasan_simbol: list[dict] = []
    per_simbol: list[dict] = []
    semua_trade = []
    hasil_per_simbol: dict[str, Hasil] = {}
    jendela_sampel: list[tuple[pd.DataFrame, np.ndarray, str]] = []
    g_forward: list[Gerbang] = []
    nama_forward: list[str] = []
    g_bnh: list[Gerbang] = []

    for i, s in enumerate(sorted(ktx.bingkai), 1):
        df = ktx.bingkai[s]
        try:
            jadwal = ambil_jadwal(ktx.jadwal, s)
        except KeyError as e:
            print(f"  [{i}] {s}: DILEWATI, {e}", flush=True)
            continue

        wf = jalankan_walk_forward(
            df,
            kandidat=spek.kandidat,
            buat_sinyal=spek.sinyal,
            panjang_latih=opsi.panjang_latih,
            panjang_uji=opsi.panjang_uji,
            embargo=opsi.embargo,
            pemanasan=opsi.pemanasan,
            konfig=konfig,
            jadwal=jadwal,
            symbol=s,
            simpan_bingkai=s in ktx.sampel,
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
                        ekuitas=np.array(
                            [konfig.modal_awal, konfig.modal_awal + laba]
                        ),
                    ),
                    df.iloc[awal_uji:akhir_uji],
                )
            )

        for hj in wf.per_jendela:
            if hj.bingkai_uji is not None and hj.sinyal_uji is not None:
                jendela_sampel.append((hj.bingkai_uji, hj.sinyal_uji, s))

        if i % 10 == 0 or i == len(ktx.bingkai):
            print(
                f"  [{i}/{len(ktx.bingkai)}] {s}: "
                f"{r['jumlah_trade_luar_sampel']} trade, {time.time() - t0:.0f}s",
                flush=True,
            )

    gabungan = ringkas_gabungan(ringkasan_simbol)
    diagnosa = diagnosa_biaya(semua_trade)
    alasan: dict[str, int] = {}
    for p in semua_trade:
        alasan[p.alasan_keluar] = alasan.get(p.alasan_keluar, 0) + 1

    print(json.dumps(gabungan, indent=2), flush=True)
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
                    jadwal=ktx.jadwal.get(sym),
                    symbol=sym,
                )
                rs.extend(p.R for p in hasil_j.perdagangan)
            return float(np.mean(rs)) if rs else float("-inf")

        nyata = penilai(sinyal_gabung)
        gerbang_acak = gerbang_entri_acak(
            nyata, sinyal_gabung, penilai, ulangan=opsi.ulangan
        )
        p_acak = gerbang_acak.nilai
        print(f"entri acak: nyata {nyata:.5f}R, p {p_acak}", flush=True)
    else:
        gerbang_acak = Gerbang(
            "entri_acak",
            False,
            None,
            None,
            "tidak dapat dinilai: tidak ada jendela sampel",
        )

    if ktx.bingkai:
        contoh = ktx.bingkai[sorted(ktx.bingkai)[0]]
        gerbang_la = gerbang_lookahead(
            contoh.iloc[:5000], lambda d: spek.sinyal(d, spek.params_lookahead)
        )
    else:
        gerbang_la = Gerbang(
            "lookahead", False, None, None, "tidak dapat dinilai: tidak ada data"
        )

    laporan = susun_laporan(
        [
            gerbang_ff,
            gerbang_bnh,
            gerbang_acak,
            gerbang_la,
            gerbang_invarian_risiko(hasil_pool),
            gerbang_funding(hasil_pool, jadwal_dimuat=bool(ktx.jadwal)),
            gerbang_overlap_gabungan(hasil_per_simbol),
            ktx.gerbang_cs,
            gerbang_survivorship(
                simbol_diuji=[r["symbol"] for r in ringkasan_simbol],
                simbol_delisted=ktx.mati,
                simbol_universe=ktx.semesta_layak,
            ),
        ]
    )
    putusan = nilai(spek.h, gabungan, p_acak)

    isi = {
        "hipotesis": spek.h.ke_dict() | {"sidik": spek.h.sidik()},
        "parameter_run": {
            "interval": opsi.interval,
            "limit": opsi.limit,
            "panjang_latih": opsi.panjang_latih,
            "panjang_uji": opsi.panjang_uji,
            "embargo": opsi.embargo,
            "pemanasan": opsi.pemanasan,
            "ulangan_permutasi": opsi.ulangan,
            "maks_umur_bar": konfig.maks_umur_bar,
            "maks_carry_R": konfig.maks_carry_R,
            "jendela_carry_hari": konfig.jendela_carry_hari,
        },
        "gabungan": gabungan,
        "alasan_keluar": alasan,
        "diagnosa_biaya": diagnosa,
        "gerbang": laporan.ke_dict(),
        "putusan": {"lulus": putusan.lulus, "alasan": putusan.alasan},
        "per_simbol": per_simbol,
        "detik": round(time.time() - t0, 1),
    }
    out = Path(opsi.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"backtest_{spek.nama}.json").write_text(
        json.dumps(isi, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    md = [
        f"# Backtest {spek.h.id} — {spek.nama}",
        "",
        f"> {spek.h.pernyataan}",
        "",
        f"Sidik `{spek.h.sidik()[:16]}` \u00b7 {spek.h.jumlah_kombinasi} kombinasi "
        f"\u00b7 {gabungan['jumlah_simbol']} simbol \u00b7 {isi['detik']}s",
        "",
        "## Putusan",
        "",
        f"**{'LULUS' if putusan.lulus and laporan.semua_lulus else 'DITOLAK'}**",
        "",
    ]
    if putusan.alasan:
        md += ["Kriteria pra-registrasi yang tidak terpenuhi:", ""]
        md += [f"- {al}" for al in putusan.alasan] + [""]
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
        "## Sembilan gerbang",
        "",
        "| Gerbang | Putusan | Nilai | Ambang | Catatan |",
        "|---|---|---|---|---|",
    ]
    for g in laporan.gerbang:
        n = "\u2014" if g.nilai is None else f"{g.nilai:.4f}"
        am = "\u2014" if g.ambang is None else f"{g.ambang}"
        md.append(
            f"| {g.nama} | {'lulus' if g.lulus else 'GAGAL'} | {n} | {am} | "
            f"{g.catatan} |"
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
        ]
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

    (out / f"backtest_{spek.nama}.md").write_text(
        "\n".join(md) + "\n", encoding="utf-8"
    )

    return {
        "id": spek.h.id,
        "nama": spek.nama,
        "sidik": spek.h.sidik()[:16],
        "ekspektasi_R": gabungan["ekspektasi_R"],
        "total_R": gabungan["total_R"],
        "trade": gabungan["jumlah_trade_luar_sampel"],
        "jendela_positif": gabungan["jendela_positif"],
        "jumlah_jendela": gabungan["jumlah_jendela"],
        "p_entri_acak": p_acak,
        "gerbang_gagal": laporan.yang_gagal,
        "lulus": bool(putusan.lulus and laporan.semua_lulus),
        "alasan": putusan.alasan,
        "rerata_transaksi_R": diagnosa.get("rerata_transaksi_R"),
        "detik": isi["detik"],
    }
