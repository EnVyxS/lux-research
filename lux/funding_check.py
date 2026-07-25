"""Menghitung ulang statistik funding dari Parquet yang sudah tersimpan.

Dijalankan alih-alih mengulang ingest, karena datanya sudah ada di Release dan
yang dipersoalkan adalah metriknya, bukan datanya.

Riwayat singkat metrik celah di modul ini, karena penting untuk tidak
mengulanginya:

1. Putaran pertama memakai satu langkah tetap per simbol, yaitu nilai terkecil
   pada kolom ``funding_interval_hours``. Hasilnya 1.380.741 celah dari
   1.982.017 baris.
2. Putaran kedua memakai langkah per baris dari kolom yang sama, dan
   mengecualikan baris tempat kisi berpindah. Hasilnya nyaris tidak berubah:
   1.193.209 celah, sementara peralihan kisi hanya 366 peristiwa pada 160
   simbol. Perpindahan rezim terlalu jarang untuk menjelaskan 60% baris.

Kesimpulan yang tersisa: kolom ``funding_interval_hours`` tidak dapat dipakai
sebagai kisi yang berlaku pada baris itu. Karena itu modul ini berhenti
mempercayainya dan **mengukur** kisi dari jarak antarbaris yang benar-benar
ada, lalu melaporkan selisih antara yang dideklarasikan dan yang teramati.
Bila keduanya berbeda jauh, itu sendiri temuan yang harus terlihat, bukan
disembunyikan di balik satu angka celah.

Pemakaian:
    python -m lux.funding_check --dir aset --universe reports/universe_layak.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

from lux.funding import AMBANG_EKSTREM, JAM_MS, periksa

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


def langkah_teramati(t: pd.Series) -> int | None:
    """Kisi yang benar-benar dipakai, diukur dari jarak antarbaris.

    Modus dipilih, bukan rerata atau minimum: satu penghentian perdagangan
    panjang akan menggeser rerata, dan satu peristiwa sisipan akan menggeser
    minimum, sedangkan modus bertahan selama mayoritas jarak masih normal.
    """
    beda = t.sort_values().diff().dropna()
    if beda.empty:
        return None
    modus = beda.mode()
    return int(modus.iloc[0]) if not modus.empty else None


def celah_teramati(t: pd.Series, langkah: int | None) -> tuple[int, int]:
    """(jumlah peristiwa celah, perkiraan periode yang hilang).

    Hanya jarak yang **lebih besar** dari kisi yang dihitung sebagai celah.
    Jarak yang lebih rapat adalah penyisipan, bukan kehilangan, dan dilaporkan
    lewat jalur lain supaya dua jenis anomali tidak saling menutupi.
    """
    if not langkah:
        return 0, 0
    beda = t.sort_values().diff().dropna()
    lebih = beda[beda > langkah]
    hilang = int(((lebih / langkah).round() - 1).clip(lower=0).sum())
    return int(len(lebih)), hilang


def biaya_tahunan(stat: dict) -> float | None:
    """Perkiraan biaya funding setahun bagi posisi long yang ditahan terus.

    Kisi yang dipakai adalah kisi teramati bila tersedia, karena kisi itu yang
    menentukan berapa kali biaya benar-benar ditagihkan.
    """
    jam = stat.get("jam_teramati")
    if not jam and stat.get("interval_jam"):
        jam = sum(stat["interval_jam"]) / len(stat["interval_jam"])
    if not jam or stat.get("rate_rerata") is None:
        return None
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
    sebaran_beda: Counter = Counter()

    for symbol, bagian in df.groupby("symbol", sort=True, observed=True):
        bagian = bagian.sort_values("calc_time")
        stat = periksa(bagian)
        stat["symbol"] = str(symbol)

        t = bagian["calc_time"]
        langkah = langkah_teramati(t)
        stat["langkah_teramati_ms"] = langkah
        stat["jam_teramati"] = round(langkah / JAM_MS, 4) if langkah else None

        peristiwa, hilang = celah_teramati(t, langkah)
        stat["celah_teramati"] = peristiwa
        stat["periode_hilang"] = hilang

        dideklarasi = stat["interval_jam"]
        stat["kolom_cocok_teramati"] = bool(
            stat["jam_teramati"] is not None
            and dideklarasi
            and any(abs(stat["jam_teramati"] - j) < 1e-6 for j in dideklarasi)
        )

        stat["biaya_tahunan_long"] = biaya_tahunan(stat)
        hasil.append(stat)

        # Sebaran jarak dikumpulkan global supaya bentuk kisi sebenarnya
        # terlihat sebagai data, bukan sebagai dugaan.
        beda = t.diff().dropna()
        for jam, n in (beda / JAM_MS).round(4).value_counts().items():
            sebaran_beda[float(jam)] += int(n)

    tidak_cocok = [h for h in hasil if not h["kolom_cocok_teramati"]]
    dengan_celah = [h for h in hasil if h["celah_teramati"] > 0]
    kisi_teramati: Counter = Counter(
        h["jam_teramati"] for h in hasil if h["jam_teramati"] is not None
    )
    kisi_dideklarasi: Counter = Counter()
    for h in hasil:
        for j in h["interval_jam"]:
            kisi_dideklarasi[j] += 1

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
        "celah_menurut_kolom": sum(h["celah"] for h in hasil),
        "celah_teramati": sum(h["celah_teramati"] for h in hasil),
        "periode_hilang": sum(h["periode_hilang"] for h in hasil),
        "simbol_dengan_celah": len(dengan_celah),
        "simbol_kolom_tidak_cocok": len(tidak_cocok),
        "positif": sum(h["positif"] for h in hasil),
        "negatif": sum(h["negatif"] for h in hasil),
        "ekstrem": sum(h["ekstrem"] for h in hasil),
        "kisi_teramati": {str(k): v for k, v in sorted(kisi_teramati.items())},
        "kisi_dideklarasi": {str(k): v for k, v in sorted(kisi_dideklarasi.items())},
        "awal": min(h["awal"] for h in hasil),
        "akhir": max(h["akhir"] for h in hasil),
    }
    ringkas["gerbang_lulus"] = (
        ringkas["duplikat"] == 0
        and ringkas["tidak_urut"] == 0
        and not ringkas["hilang_dari_universe"]
        and ringkas["simbol_kolom_tidak_cocok"] == 0
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
    total_beda = sum(sebaran_beda.values()) or 1

    md = [
        "# Pemeriksaan ulang funding rate",
        "",
        f"{ringkas['baris']:,} baris atas {ringkas['simbol']} simbol, "
        f"{tgl(ringkas['awal'])} sampai {tgl(ringkas['akhir'])}.",
        "",
        "## Kisi sebenarnya",
        "",
        "Dua putaran metrik sebelumnya memakai kolom `funding_interval_hours`",
        "sebagai kisi yang berlaku, dan keduanya melaporkan lebih dari separuh",
        "baris sebagai celah. Tabel di bawah mengukur jarak antarbaris apa adanya,",
        "supaya terlihat apakah kolom itu memang dapat dipercaya.",
        "",
        "| Jarak antarbaris (jam) | Peristiwa | Pangsa |",
        "|---|---|---|",
    ]
    for jam, n in sorted(sebaran_beda.items(), key=lambda kv: -kv[1])[:15]:
        md.append(f"| {jam:g} | {n:,} | {n / total_beda:.2%} |")

    md += [
        "",
        f"- Kisi teramati (modus per simbol): {ringkas['kisi_teramati']}",
        f"- Kisi menurut kolom: {ringkas['kisi_dideklarasi']}",
        f"- Simbol yang kolomnya tidak cocok dengan kisi teramati: "
        f"**{ringkas['simbol_kolom_tidak_cocok']} dari {ringkas['simbol']}**",
        "",
        "## Integritas",
        "",
        f"- Duplikat: **{ringkas['duplikat']}** | Tidak urut: **{ringkas['tidak_urut']}**",
        f"- Celah menurut kisi teramati: **{ringkas['celah_teramati']:,}** peristiwa "
        f"pada {ringkas['simbol_dengan_celah']} simbol, "
        f"setara {ringkas['periode_hilang']:,} periode hilang",
        f"- Celah menurut kolom interval (metrik lama): "
        f"{ringkas['celah_menurut_kolom']:,}",
        f"- Simbol layak tanpa data funding: {len(ringkas['hilang_dari_universe'])}",
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
        "| Simbol | Biaya setahun | Rerata per periode | Kisi teramati | Kolom |",
        "|---|---|---|---|---|",
    ]
    for h in biaya[:10]:
        md.append(
            f"| {h['symbol']} | {h['biaya_tahunan_long']:.1%} | "
            f"{h['rate_rerata']:.6f} | {h['jam_teramati']} | {h['interval_jam']} |"
        )

    md += [
        "",
        "## Sepuluh funding paling menguntungkan bagi long",
        "",
        "| Simbol | Biaya setahun | Rerata per periode | Kisi teramati | Kolom |",
        "|---|---|---|---|---|",
    ]
    for h in biaya[-10:][::-1]:
        md.append(
            f"| {h['symbol']} | {h['biaya_tahunan_long']:.1%} | "
            f"{h['rate_rerata']:.6f} | {h['jam_teramati']} | {h['interval_jam']} |"
        )

    if tidak_cocok:
        md += [
            "",
            "## Sepuluh ketidakcocokan kolom terhadap kisi teramati",
            "",
            "| Simbol | Kisi teramati | Kolom | Baris |",
            "|---|---|---|---|",
        ]
        for h in sorted(tidak_cocok, key=lambda h: -h["baris"])[:10]:
            md.append(
                f"| {h['symbol']} | {h['jam_teramati']} | {h['interval_jam']} | "
                f"{h['baris']:,} |"
            )

    md += ["", f"Gerbang lulus: **{ringkas['gerbang_lulus']}**"]

    (out / "funding_check.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(ringkas, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
