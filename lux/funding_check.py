"""Menghitung ulang statistik funding dari Parquet yang sudah tersimpan.

Dijalankan alih-alih mengulang ingest, karena datanya sudah ada di Release dan
yang dipersoalkan adalah metriknya, bukan datanya.

Riwayat metrik celah di modul ini ditulis lengkap karena kesalahannya berulang
tiga kali dengan bentuk yang sama:

1. Langkah tetap per simbol, diambil dari nilai terkecil kolom
   ``funding_interval_hours``. Hasil: 1.380.741 celah dari 1.982.017 baris.
2. Langkah per baris dari kolom yang sama, peralihan dikecualikan. Hasil nyaris
   sama, 1.193.209, padahal peralihan hanya 366 peristiwa pada 160 simbol.
3. Langkah diukur dari modus jarak antarbaris, bukan dari kolom. Hasil masih
   587.131, dan sekaligus membuktikan kolomnya tidak pernah salah: nol dari 447
   simbol yang kolomnya tidak cocok dengan kisi teramati.

Sebaran jarak mentah menutup kasusnya. Seluruh 1.981.570 jarak jatuh pada
4 jam (52,0%), 8 jam (45,2%), 1 jam (2,7%), 2 jam (0,1%), ditambah 19 jarak
3 jam, 3 jarak 6 jam, dan tiga jarak sangat panjang.

Cacatnya sama pada ketiga putaran: memaksakan **satu** kisi untuk seluruh umur
simbol. Binance memindahkan ratusan pasangan dari 8 jam ke 4 jam, sehingga satu
simbol wajar memiliki dua rezim berdurasi tahunan. Menilai separuh riwayat
dengan kisi separuh lainnya menghasilkan ratusan ribu celah semu.

Aturan yang dipakai sekarang tidak memerlukan asumsi kisi sama sekali: karena
kisi funding terpanjang adalah delapan jam, setiap jarak yang melebihi delapan
jam berarti ada periode yang benar-benar tidak tertagih. Jarak yang lebih
pendek adalah kisi sah atau penyelarasan saat berpindah rezim, dan dihitung
terpisah supaya tetap terlihat.

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

# Kisi funding terpanjang yang dipakai Binance. Jarak di atas ini tidak dapat
# dijelaskan oleh rezim mana pun, jadi pasti ada periode yang hilang.
MAKS_KISI_JAM = 8
MAKS_KISI_MS = MAKS_KISI_JAM * JAM_MS

# Kisi yang sah dipakai sebagai interval funding.
KISI_SAH_JAM = (1, 2, 4, 8)


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
    """Kisi paling sering dipakai simbol ini, diukur dari jarak antarbaris.

    Dipakai untuk menaksir berapa periode yang hilang di dalam sebuah celah,
    bukan untuk menentukan apakah sesuatu adalah celah. Modus dipilih karena
    rerata tertipu satu jeda panjang dan minimum tertipu satu penyisipan.
    """
    beda = t.sort_values().diff().dropna()
    if beda.empty:
        return None
    modus = beda.mode()
    return int(modus.iloc[0]) if not modus.empty else None


def celah_teramati(t: pd.Series, langkah: int | None = None) -> tuple[int, int]:
    """(jumlah peristiwa celah, perkiraan periode yang hilang).

    Celah didefinisikan tanpa mengasumsikan kisi simbol: jarak yang melebihi
    kisi terpanjang yang mungkin. Jumlah periode hilang ditaksir memakai kisi
    yang paling sering dipakai simbol tersebut, karena satu jeda 504 jam berarti
    126 penagihan hilang bagi simbol berkisi 4 jam tetapi 63 bagi yang 8 jam.
    """
    beda = t.sort_values().diff().dropna()
    lebih = beda[beda > MAKS_KISI_MS]
    if lebih.empty:
        return 0, 0
    dasar = langkah or MAKS_KISI_MS
    hilang = int(((lebih / dasar).round() - 1).clip(lower=0).sum())
    return int(len(lebih)), hilang


def tidak_selaras(t: pd.Series) -> int:
    """Jarak di bawah kisi terpanjang yang bukan kisi sah.

    Bukan pelanggaran: ini penyelarasan saat sebuah simbol berpindah rezim,
    misalnya melompat tiga jam sekali untuk masuk ke kisi empat jam. Dihitung
    supaya jumlahnya tetap terlihat, bukan lenyap ke dalam angka celah.
    """
    beda = t.sort_values().diff().dropna()
    pendek = beda[beda <= MAKS_KISI_MS]
    jam = (pendek / JAM_MS).round(4)
    return int((~jam.isin(KISI_SAH_JAM)).sum())


def biaya_tahunan(stat: dict) -> float | None:
    """Perkiraan biaya funding setahun bagi posisi long yang ditahan terus.

    Memakai kisi teramati bila ada, karena kisi itulah yang menentukan berapa
    kali biaya benar-benar ditagihkan.
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
        stat["jarak_tidak_selaras"] = tidak_selaras(t)

        jam_hadir = sorted(
            set((t.diff().dropna() / JAM_MS).round(4)) & set(KISI_SAH_JAM)
        )
        stat["rezim_kisi"] = [int(j) for j in jam_hadir]

        stat["biaya_tahunan_long"] = biaya_tahunan(stat)
        hasil.append(stat)

        for jam, n in (t.diff().dropna() / JAM_MS).round(4).value_counts().items():
            sebaran_beda[float(jam)] += int(n)

    dengan_celah = [h for h in hasil if h["celah_teramati"] > 0]
    berbilang_rezim = [h for h in hasil if len(h["rezim_kisi"]) > 1]
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
        "simbol_dengan_celah": len(dengan_celah),
        "simbol_berbilang_rezim": len(berbilang_rezim),
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
    total_beda = sum(sebaran_beda.values()) or 1

    md = [
        "# Pemeriksaan ulang funding rate",
        "",
        f"{ringkas['baris']:,} baris atas {ringkas['simbol']} simbol, "
        f"{tgl(ringkas['awal'])} sampai {tgl(ringkas['akhir'])}.",
        "",
        "## Sebaran jarak antarbaris",
        "",
        "Tabel ini yang seharusnya dibuat lebih dulu. Tiga putaran metrik celah",
        "gagal karena berteori tentang bentuk kisi tanpa pernah melihatnya.",
        "",
        "| Jarak (jam) | Peristiwa | Pangsa |",
        "|---|---|---|",
    ]
    for jam, n in sorted(sebaran_beda.items(), key=lambda kv: -kv[1])[:15]:
        md.append(f"| {jam:g} | {n:,} | {n / total_beda:.2%} |")

    md += [
        "",
        f"- Kisi yang paling sering dipakai tiap simbol: {ringkas['kisi_teramati']}",
        f"- Simbol yang hidup di lebih dari satu rezim kisi: "
        f"**{ringkas['simbol_berbilang_rezim']} dari {ringkas['simbol']}**",
        "",
        "Kisi funding bukan sifat tetap sebuah simbol. Binance memindahkan",
        "ratusan pasangan dari delapan jam ke empat jam, jadi satu simbol wajar",
        "memiliki dua rezim berdurasi tahunan. Metrik apa pun yang memaksakan",
        "satu kisi untuk seluruh umur simbol akan salah, tidak peduli kisi itu",
        "diambil dari kolom metadata atau diukur dari data.",
        "",
        "## Integritas",
        "",
        f"- Duplikat: **{ringkas['duplikat']}** | Tidak urut: **{ringkas['tidak_urut']}**",
        f"- Celah sejati, yaitu jarak melebihi {MAKS_KISI_JAM} jam: "
        f"**{ringkas['celah']}** peristiwa pada {ringkas['simbol_dengan_celah']} simbol, "
        f"setara {ringkas['periode_hilang']:,} penagihan tak tercatat",
        f"- Jarak tidak selaras kisi sah, penyelarasan saat pindah rezim: "
        f"{ringkas['jarak_tidak_selaras']}",
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
        "Angka setahun adalah ekstrapolasi rerata historis, bukan ramalan. Ia",
        "dipakai untuk menakar besaran rintangan, bukan sebagai masukan strategi.",
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
            "data yang hilang: tidak ada funding ditagihkan ketika pasangannya",
            "memang tidak diperdagangkan.",
        ]

    md += ["", f"Gerbang lulus: **{ringkas['gerbang_lulus']}**"]

    (out / "funding_check.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(ringkas, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
