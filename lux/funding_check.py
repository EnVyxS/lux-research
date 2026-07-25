"""Menghitung ulang statistik funding dari Parquet yang sudah tersimpan.

Riwayat metrik celah di modul ini ditulis lengkap karena kesalahannya berulang
empat kali, dan bentuk kesalahannya berubah tiap putaran:

1. Langkah tetap per simbol dari nilai terkecil kolom ``funding_interval_hours``.
   Hasil: 1.380.741 celah dari 1.982.017 baris.
2. Langkah per baris dari kolom yang sama. Hasil nyaris sama, 1.193.209.
3. Langkah dari modus jarak antarbaris. Hasil 587.131, sekaligus membuktikan
   kolomnya tidak pernah salah: nol dari 447 simbol yang kolomnya tidak cocok.
   Cacat ketiganya sama, yaitu memaksakan satu kisi untuk seluruh umur simbol,
   padahal 295 dari 447 simbol hidup di lebih dari satu rezim kisi.
4. Celah didefinisikan sebagai jarak melebihi delapan jam, tanpa toleransi.
   Hasil 266.612 peristiwa yang hanya menghasilkan 10.720 penagihan hilang.
   Rasio yang mustahil itu yang membongkarnya: jarak 8 jam lebih beberapa
   milidetik lolos ambang, lalu dibulatkan menjadi tepat satu periode hilang.

Pembandingan waktu tanpa toleransi adalah cacat yang sama seperti membandingkan
bilangan pecahan dengan tanda sama dengan. Stempel waktu bursa bergeser beberapa
milidetik, dan pergeseran itu bukan data yang hilang. Semua perbandingan kisi di
bawah memakai toleransi satu menit, dan besar pergeseran yang sesungguhnya
dilaporkan sebagai angka tersendiri supaya tidak lagi tersembunyi.

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

# Kisi funding terpanjang yang dipakai Binance.
MAKS_KISI_JAM = 8
MAKS_KISI_MS = MAKS_KISI_JAM * JAM_MS

# Kisi yang sah dipakai sebagai interval funding.
KISI_SAH_JAM = (1, 2, 4, 8)
KISI_SAH_MS = tuple(j * JAM_MS for j in KISI_SAH_JAM)

# Pergeseran stempel waktu di bawah ini bukan anomali. Satu menit dipilih karena
# jauh lebih besar dari jitter bursa yang teramati namun jauh lebih kecil dari
# jarak antar-kisi terdekat, yaitu satu jam.
TOLERANSI_MS = 60_000


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


def _beda(t: pd.Series) -> pd.Series:
    return t.sort_values().diff().dropna()


def langkah_teramati(t: pd.Series) -> int | None:
    """Kisi paling sering dipakai simbol ini, diukur dari jarak antarbaris.

    Dipakai untuk menaksir berapa periode hilang di dalam sebuah celah, bukan
    untuk menentukan apakah sesuatu adalah celah. Modus dipilih karena rerata
    tertipu satu jeda panjang dan minimum tertipu satu penyisipan. Jarak
    dibulatkan ke kisi sah terdekat lebih dulu agar jitter milidetik tidak
    memecah satu kisi menjadi puluhan nilai berbeda.
    """
    beda = _beda(t)
    if beda.empty:
        return None
    modus = _ke_kisi_terdekat(beda).mode()
    return int(modus.iloc[0]) if not modus.empty else None


def _ke_kisi_terdekat(beda: pd.Series) -> pd.Series:
    """Petakan tiap jarak ke kisi sah terdekat, atau ke dirinya sendiri.

    Jarak yang menyimpang lebih dari toleransi dibiarkan apa adanya supaya
    anomali tidak dirapikan menjadi seolah-olah normal.
    """
    jarak = pd.concat([(beda - k).abs() for k in KISI_SAH_MS], axis=1)
    terdekat = pd.Series(KISI_SAH_MS, dtype="int64").reindex(
        jarak.values.argmin(axis=1)
    )
    terdekat.index = beda.index
    dekat = jarak.min(axis=1) <= TOLERANSI_MS
    return terdekat.where(dekat, beda).astype("int64")


def celah_teramati(t: pd.Series, langkah: int | None = None) -> tuple[int, int]:
    """(jumlah peristiwa celah, perkiraan penagihan yang hilang).

    Celah tidak mengasumsikan kisi simbol: jarak yang melampaui kisi terpanjang
    yang mungkin, dengan toleransi. Jumlah penagihan hilang ditaksir memakai
    kisi utama simbol, karena jeda 504 jam berarti 125 penagihan hilang bagi
    simbol berkisi 4 jam tetapi 62 bagi yang 8 jam.
    """
    beda = _beda(t)
    lebih = beda[beda > MAKS_KISI_MS + TOLERANSI_MS]
    if lebih.empty:
        return 0, 0
    dasar = langkah or MAKS_KISI_MS
    hilang = int(((lebih / dasar).round() - 1).clip(lower=0).sum())
    return int(len(lebih)), hilang


def tidak_selaras(t: pd.Series) -> int:
    """Jarak di bawah kisi terpanjang yang bukan kisi sah mana pun.

    Bukan pelanggaran: ini penyelarasan saat simbol berpindah rezim. Dihitung
    supaya jumlahnya tetap terlihat, bukan lenyap ke dalam angka celah.
    """
    beda = _beda(t)
    pendek = beda[beda <= MAKS_KISI_MS + TOLERANSI_MS]
    if pendek.empty:
        return 0
    jarak = pd.concat([(pendek - k).abs() for k in KISI_SAH_MS], axis=1).min(axis=1)
    return int((jarak > TOLERANSI_MS).sum())


def geseran(t: pd.Series) -> tuple[int, int]:
    """(berapa jarak yang tidak tepat di kisi, pergeseran terbesar dalam ms).

    Mengukur jitter stempel waktu bursa. Putaran metrik keempat gagal karena
    menganggap pergeseran ini sebagai data hilang, jadi sekarang ia dilaporkan
    sebagai besaran tersendiri alih-alih diam-diam ditoleransi.
    """
    beda = _beda(t)
    pendek = beda[beda <= MAKS_KISI_MS + TOLERANSI_MS]
    if pendek.empty:
        return 0, 0
    jarak = pd.concat([(pendek - k).abs() for k in KISI_SAH_MS], axis=1).min(axis=1)
    kena = jarak[(jarak > 0) & (jarak <= TOLERANSI_MS)]
    return int(len(kena)), int(kena.max()) if not kena.empty else 0


def biaya_tahunan(stat: dict) -> float | None:
    """Perkiraan biaya funding setahun bagi long yang ditahan terus."""
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
    sebaran: Counter = Counter()

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
        stat["jarak_tidak_selaras"] = tidak_selaras(t)

        n_geser, maks_geser = geseran(t)
        stat["jarak_bergeser"] = n_geser
        stat["geseran_maks_ms"] = maks_geser

        beda = _beda(t)
        rapi = _ke_kisi_terdekat(beda)
        stat["rezim_kisi"] = sorted(
            int(j / JAM_MS) for j in set(rapi.unique()) & set(KISI_SAH_MS)
        )
        stat["biaya_tahunan_long"] = biaya_tahunan(stat)
        hasil.append(stat)

        for ms, n in rapi.value_counts().items():
            sebaran[round(ms / JAM_MS, 4)] += int(n)

    dengan_celah = [h for h in hasil if h["celah_teramati"] > 0]
    kisi_teramati: Counter = Counter(
        h["jam_teramati"] for h in hasil if h["jam_teramati"] is not None
    )
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
        "celah": sum(h["celah_teramati"] for h in hasil),
        "periode_hilang": sum(h["periode_hilang"] for h in hasil),
        "jarak_tidak_selaras": sum(h["jarak_tidak_selaras"] for h in hasil),
        "jarak_bergeser": sum(h["jarak_bergeser"] for h in hasil),
        "geseran_maks_ms": max(h["geseran_maks_ms"] for h in hasil),
        "simbol_dengan_celah": len(dengan_celah),
        "simbol_berbilang_rezim": len([h for h in hasil if len(h["rezim_kisi"]) > 1]),
        "positif": sum(h["positif"] for h in hasil),
        "negatif": sum(h["negatif"] for h in hasil),
        "ekstrem": sum(h["ekstrem"] for h in hasil),
        "kisi_teramati": {str(k): v for k, v in sorted(kisi_teramati.items())},
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
    total = sum(sebaran.values()) or 1

    md = [
        "# Pemeriksaan ulang funding rate",
        "",
        f"{ringkas['baris']:,} baris atas {ringkas['simbol']} simbol, "
        f"{tgl(ringkas['awal'])} sampai {tgl(ringkas['akhir'])}.",
        "",
        "## Sebaran jarak antarbaris",
        "",
        "Jarak dibulatkan ke kisi sah terdekat bila selisihnya di bawah satu",
        "menit. Tanpa pembulatan itu, jitter milidetik memecah satu kisi menjadi",
        "puluhan nilai dan menyamar sebagai celah.",
        "",
        "| Jarak (jam) | Peristiwa | Pangsa |",
        "|---|---|---|",
    ]
    for jam, n in sorted(sebaran.items(), key=lambda kv: -kv[1])[:15]:
        md.append(f"| {jam:g} | {n:,} | {n / total:.2%} |")

    md += [
        "",
        f"- Kisi utama tiap simbol: {ringkas['kisi_teramati']}",
        f"- Simbol yang hidup di lebih dari satu rezim: "
        f"**{ringkas['simbol_berbilang_rezim']} dari {ringkas['simbol']}**",
        f"- Jarak yang tidak tepat di kisi namun masih dalam toleransi: "
        f"{ringkas['jarak_bergeser']:,}, pergeseran terbesar "
        f"{ringkas['geseran_maks_ms']:,} ms",
        "",
        "Kisi funding bukan sifat tetap sebuah simbol. Binance memindahkan",
        "ratusan pasangan dari delapan jam ke empat jam, jadi satu simbol wajar",
        "memiliki dua rezim berdurasi tahunan.",
        "",
        "## Integritas",
        "",
        f"- Duplikat: **{ringkas['duplikat']}** | Tidak urut: **{ringkas['tidak_urut']}**",
        f"- Celah sejati, jarak melebihi {MAKS_KISI_JAM} jam di luar toleransi: "
        f"**{ringkas['celah']:,}** peristiwa pada {ringkas['simbol_dengan_celah']} "
        f"simbol, setara {ringkas['periode_hilang']:,} penagihan tak tercatat",
        f"- Jarak tidak selaras kisi sah: {ringkas['jarak_tidak_selaras']}",
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
        "Angka setahun adalah ekstrapolasi rerata historis, bukan ramalan.",
        "",
        "| Simbol | Biaya setahun | Rerata per periode | Kisi utama | Rezim |",
        "|---|---|---|---|---|",
    ]
    for h in biaya[:10]:
        md.append(
            f"| {h['symbol']} | {h['biaya_tahunan_long']:.1%} | "
            f"{h['rate_rerata']:.6f} | {h['jam_teramati']} | {h['rezim_kisi']} |"
        )

    md += [
        "",
        "## Sepuluh funding paling menguntungkan bagi long",
        "",
        "| Simbol | Biaya setahun | Rerata per periode | Kisi utama | Rezim |",
        "|---|---|---|---|---|",
    ]
    for h in biaya[-10:][::-1]:
        md.append(
            f"| {h['symbol']} | {h['biaya_tahunan_long']:.1%} | "
            f"{h['rate_rerata']:.6f} | {h['jam_teramati']} | {h['rezim_kisi']} |"
        )

    if dengan_celah:
        md += [
            "",
            "## Simbol dengan celah sejati",
            "",
            "| Simbol | Peristiwa | Penagihan hilang | Kisi utama |",
            "|---|---|---|---|",
        ]
        for h in sorted(dengan_celah, key=lambda h: -h["periode_hilang"])[:20]:
            md.append(
                f"| {h['symbol']} | {h['celah_teramati']} | "
                f"{h['periode_hilang']:,} | {h['jam_teramati']} |"
            )
        md += [
            "",
            "Jeda sepanjang ini adalah penghentian perdagangan sungguhan, bukan",
            "data hilang: tidak ada funding ditagihkan ketika pasangannya memang",
            "tidak diperdagangkan. Backtest harus memperlakukan rentang ini",
            "sebagai periode tanpa posisi, bukan sebagai biaya nol.",
        ]

    md += ["", f"Gerbang lulus: **{ringkas['gerbang_lulus']}**"]

    (out / "funding_check.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(ringkas, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
