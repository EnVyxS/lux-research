"""Menghitung ulang statistik funding dari Parquet yang sudah tersimpan.

Dijalankan alih-alih mengulang ingest, karena datanya sudah ada di Release dan
yang cacat adalah metriknya, bukan datanya. Mengunduh ulang dua puluh ribu
arsip untuk memperbaiki sebuah rumus adalah pemborosan yang tidak perlu.

Modul ini juga menjawab pertanyaan ekonomi yang menjadi alasan funding diambil:
berapa mahal biaya menahan posisi, dan ke arah mana biaya itu condong.

Pemakaian:
    python -m lux.funding_check --dir aset --universe reports/universe_layak.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

from lux.funding import AMBANG_EKSTREM, periksa

SETAHUN_JAM = 24 * 365


def muat_semua(direktori: Path) -> pd.DataFrame:
    berkas = sorted(direktori.glob("funding_shard*.parquet"))
    if not berkas:
        raise SystemExit(f"tidak ada funding_shard*.parquet di {direktori}")
    bagian = []
    for p in berkas:
        df = pd.read_parquet(p)
        bagian.append(df)
        print(f"  dibaca {p.name}: {len(df):,} baris", flush=True)
    gabung = pd.concat(bagian, ignore_index=True)
    gabung["symbol"] = gabung["symbol"].astype(str)
    return gabung


def biaya_tahunan(stat: dict) -> float | None:
    """Perkiraan biaya funding setahun bagi posisi long yang ditahan terus.

    Dinyatakan sebagai pecahan nilai posisi. Angka ini bukan ramalan, melainkan
    ukuran seberapa besar rintangan yang harus dilewati strategi long-bias
    sebelum menghasilkan apa pun.
    """
    if not stat["interval_jam"] or stat["rate_rerata"] is None:
        return None
    jam = sum(stat["interval_jam"]) / len(stat["interval_jam"])
    return stat["rate_rerata"] * (SETAHUN_JAM / jam)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--universe", default="reports/universe_layak.json")
    ap.add_argument("--out", default="reports")
    a = ap.parse_args(argv)

    df = muat_semua(Path(a.dir))
    layak = set(json.loads(Path(a.universe).read_text(encoding="utf-8"))["simbol"])
    ada = set(df["symbol"].unique())

    hasil: list[dict] = []
    for symbol, bagian in df.groupby("symbol", sort=True, observed=True):
        stat = periksa(bagian)
        stat["symbol"] = str(symbol)
        stat["biaya_tahunan_long"] = biaya_tahunan(stat)
        hasil.append(stat)

    kisi: dict[str, int] = {}
    for h in hasil:
        for j in h["interval_jam"]:
            kisi[str(j)] = kisi.get(str(j), 0) + 1

    berpindah = [h for h in hasil if len(h["interval_jam"]) > 1]
    dengan_celah = [h for h in hasil if h["celah"] > 0]
    biaya = sorted(
        (h for h in hasil if h["biaya_tahunan_long"] is not None),
        key=lambda h: -h["biaya_tahunan_long"],
    )

    ringkas = {
        "simbol": len(hasil),
        "baris": int(len(df)),
        "hilang_dari_universe": sorted(layak - ada),
        "di_luar_universe": sorted(ada - layak),
        "duplikat": sum(h["duplikat"] for h in hasil),
        "tidak_urut": sum(h["tidak_urut"] for h in hasil),
        "celah": sum(h["celah"] for h in hasil),
        "peralihan_kisi": sum(h["peralihan_kisi"] for h in hasil),
        "simbol_berpindah_kisi": len(berpindah),
        "simbol_dengan_celah": len(dengan_celah),
        "positif": sum(h["positif"] for h in hasil),
        "negatif": sum(h["negatif"] for h in hasil),
        "ekstrem": sum(h["ekstrem"] for h in hasil),
        "sebaran_interval_jam": kisi,
        "awal": min(h["awal"] for h in hasil),
        "akhir": max(h["akhir"] for h in hasil),
    }
    ringkas["gerbang_lulus"] = (
        ringkas["duplikat"] == 0
        and ringkas["tidak_urut"] == 0
        and not ringkas["hilang_dari_universe"]
    )

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "funding_check.json").write_text(
        json.dumps({"ringkasan": ringkas, "per_simbol": hasil}, indent=2),
        encoding="utf-8",
    )

    def tgl(ms: int) -> str:
        return pd.to_datetime(ms, unit="ms", utc=True).strftime("%Y-%m-%d")

    arah = ringkas["positif"] + ringkas["negatif"]
    pangsa = ringkas["positif"] / arah if arah else 0.0
    md = [
        "# Pemeriksaan ulang funding rate",
        "",
        f"{ringkas['baris']:,} baris atas {ringkas['simbol']} simbol, "
        f"{tgl(ringkas['awal'])} sampai {tgl(ringkas['akhir'])}.",
        "",
        "## Integritas",
        "",
        f"- Duplikat: **{ringkas['duplikat']}** | Tidak urut: **{ringkas['tidak_urut']}**",
        f"- Celah sejati: **{ringkas['celah']:,}** pada "
        f"{ringkas['simbol_dengan_celah']} simbol",
        f"- Peralihan kisi (sah): {ringkas['peralihan_kisi']:,} pada "
        f"{ringkas['simbol_berpindah_kisi']} simbol",
        f"- Simbol layak tanpa data funding: {len(ringkas['hilang_dari_universe'])}",
        f"- Sebaran interval funding (jam): {ringkas['sebaran_interval_jam']}",
        "",
        "Angka celah pada putaran pertama, 1.380.741, seluruhnya artefak asumsi",
        "bahwa kisi funding tetap delapan jam. Kisi itu berubah sepanjang hidup",
        "banyak pasangan, dan langkah kini dibaca dari kolom datanya sendiri.",
        "",
        "## Arah biaya",
        "",
        f"- Funding positif: {ringkas['positif']:,} ({pangsa:.1%}) | "
        f"negatif: {ringkas['negatif']:,}",
        f"- Melebihi {AMBANG_EKSTREM:.0%}: {ringkas['ekstrem']:,}",
        "",
        "Funding positif berarti long membayar short. Pangsa di atas separuh",
        "adalah rintangan struktural bagi strategi yang condong long, dan harus",
        "ditagihkan ke setiap posisi di backtest, bukan diabaikan.",
        "",
        "## Sepuluh biaya tahunan tertinggi bagi long",
        "",
        "| Simbol | Biaya setahun | Rerata per periode | Kisi (jam) |",
        "|---|---|---|---|",
    ]
    for h in biaya[:10]:
        md.append(
            f"| {h['symbol']} | {h['biaya_tahunan_long']:.1%} | "
            f"{h['rate_rerata']:.6f} | {h['interval_jam']} |"
        )

    md += [
        "",
        "## Sepuluh funding paling menguntungkan bagi long",
        "",
        "| Simbol | Biaya setahun | Rerata per periode | Kisi (jam) |",
        "|---|---|---|---|",
    ]
    for h in biaya[-10:][::-1]:
        md.append(
            f"| {h['symbol']} | {h['biaya_tahunan_long']:.1%} | "
            f"{h['rate_rerata']:.6f} | {h['interval_jam']} |"
        )

    md += ["", f"Gerbang lulus: **{ringkas['gerbang_lulus']}**"]

    (out / "funding_check.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(ringkas, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
