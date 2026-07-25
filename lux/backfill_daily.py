"""Backfill dari arsip HARIAN untuk bulan yang tidak tercakup arsip bulanan.

Arsip bulanan Binance tertinggal. Pada 2026-07-25, arsip bulanan berhenti di
2026-06 sementara arsip harian sudah mencapai 2026-07-24. Ingest yang hanya
membaca arsip bulanan akan kehilangan sekitar 24 hari data terbaru tanpa
memberi tanda apa pun.

Kehilangan diam-diam adalah kelas cacat paling berbahaya dalam riset
kuantitatif: hasilnya tetap terlihat masuk akal, hanya saja menggambarkan
periode yang salah. Modul ini menutupnya.

Cara kerjanya sengaja umum, bukan menambal tanggal tertentu: untuk tiap simbol
ia membandingkan bulan yang tersedia di arsip bulanan terhadap bulan yang
tersedia di arsip harian, lalu mengunduh harian HANYA untuk bulan yang tidak
tercakup. Aturan ini tetap benar berapa pun lamanya arsip bulanan tertinggal,
termasuk untuk 2019-12-31 di ujung paling awal.
"""

from __future__ import annotations

import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from lux import binance_vision as bv
from lux.ingest import SIMPAN, STEP_MS, baca_zip, muat_universe


def daily_url(symbol: str, interval: str, tanggal: str) -> str:
    return (
        f"{bv.CDN}/{bv.ROOT}/daily/klines/{symbol}/{interval}/"
        f"{symbol}-{interval}-{tanggal}.zip"
    )


def tanggal_harian(symbol: str, interval: str) -> list[str]:
    prefix = f"{bv.ROOT}/daily/klines/{symbol}/{interval}/"
    hasil = []
    for k in bv.list_keys(prefix):
        nama = k.rsplit("/", 1)[-1]
        if not nama.endswith(".zip"):
            continue
        bagian = nama[:-4].split("-")
        if len(bagian) >= 3:
            hasil.append(f"{bagian[-3]}-{bagian[-2]}-{bagian[-1]}")
    return sorted(set(hasil))


def backfill_simbol(symbol: str, interval: str, tmp: Path) -> tuple[pd.DataFrame, dict]:
    mulai = time.time()
    catatan = {"symbol": symbol, "interval": interval}

    try:
        bulanan = set(bv.list_months(symbol, interval))
        harian = tanggal_harian(symbol, interval)
    except Exception as exc:  # noqa: BLE001
        catatan["error"] = f"listing gagal: {exc}"
        return pd.DataFrame(), catatan

    # Hanya hari yang bulannya TIDAK ada di arsip bulanan.
    perlu = [t for t in harian if t[:7] not in bulanan]
    catatan["hari_perlu"] = len(perlu)

    if not perlu:
        catatan["baris"] = 0
        catatan["detik"] = round(time.time() - mulai, 2)
        return pd.DataFrame(), catatan

    bagian, gagal = [], []
    for t in perlu:
        url = daily_url(symbol, interval, t)
        try:
            path = bv.download(url, tmp / symbol / interval)
            bagian.append(baca_zip(path))
            path.unlink(missing_ok=True)
        except Exception as exc:  # noqa: BLE001
            gagal.append({"tanggal": t, "galat": str(exc)[:200]})

    if not bagian:
        catatan["error"] = "semua unduhan harian gagal"
        catatan["contoh_gagal"] = gagal[:3]
        return pd.DataFrame(), catatan

    df = pd.concat(bagian, ignore_index=True)
    df["symbol"] = symbol
    sebelum = len(df)
    df = df.drop_duplicates(subset=["open_time"]).sort_values("open_time")

    step = STEP_MS[interval]
    beda = df["open_time"].diff().dropna()

    catatan.update(
        {
            "hari_gagal": len(gagal),
            "contoh_gagal": gagal[:3],
            "baris": len(df),
            "duplikat_dibuang": sebelum - len(df),
            "celah_kisi": int((beda != step).sum()),
            "tanggal_pertama": perlu[0],
            "tanggal_terakhir": perlu[-1],
            "detik": round(time.time() - mulai, 2),
        }
    )
    return df[SIMPAN], catatan


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--shard", type=int, default=0)
    p.add_argument("--shards", type=int, default=1)
    p.add_argument("--intervals", default="1h,4h")
    p.add_argument("--quote", default="USDT")
    p.add_argument("--workers", type=int, default=6)
    p.add_argument("--out", default="out")
    a = p.parse_args()

    semua = muat_universe(a.quote)
    milik_saya = [s for i, s in enumerate(semua) if i % a.shards == a.shard]

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    tmp = Path("/tmp/lux_backfill")
    tmp.mkdir(parents=True, exist_ok=True)

    print(f"backfill shard {a.shard}/{a.shards}: {len(milik_saya)} simbol")

    ringkasan = {
        "shard": a.shard,
        "shards": a.shards,
        "quote": a.quote,
        "simbol_ditugaskan": len(milik_saya),
        "mulai_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "interval": {},
    }

    for interval in [x.strip() for x in a.intervals.split(",")]:
        mulai = time.time()
        potongan, catatan = [], []

        def kerjakan(s: str):
            return backfill_simbol(s, interval, tmp)

        with ThreadPoolExecutor(max_workers=a.workers) as pool:
            for i, (df, cat) in enumerate(pool.map(kerjakan, milik_saya), 1):
                catatan.append(cat)
                if len(df):
                    potongan.append(df)
                if i % 20 == 0:
                    print(f"  {interval}: {i}/{len(milik_saya)}")

        if potongan:
            gabung = pd.concat(potongan, ignore_index=True)
            gabung["symbol"] = gabung["symbol"].astype("category")
            berkas = out / f"ohlcv_{interval}_tail_shard{a.shard:02d}.parquet"
            gabung.to_parquet(berkas, index=False, compression="zstd")
            ukuran, baris = berkas.stat().st_size, len(gabung)
        else:
            berkas, ukuran, baris = None, 0, 0

        ringkasan["interval"][interval] = {
            "baris": baris,
            "simbol_berhasil": sum(1 for c in catatan if not c.get("error")),
            "simbol_gagal": sum(1 for c in catatan if c.get("error")),
            "simbol_butuh_backfill": sum(1 for c in catatan if c.get("hari_perlu", 0) > 0),
            "total_hari_diunduh": sum(c.get("hari_perlu", 0) for c in catatan),
            "total_duplikat": sum(c.get("duplikat_dibuang", 0) for c in catatan),
            "total_celah_kisi": sum(c.get("celah_kisi", 0) for c in catatan),
            "berkas": str(berkas) if berkas else None,
            "bytes": ukuran,
            "detik": round(time.time() - mulai, 1),
        }

        Path(f"{a.out}/detail_tail_{interval}_shard{a.shard:02d}.json").write_text(
            json.dumps(catatan, indent=2, ensure_ascii=False, default=str)
        )
        print(json.dumps(ringkasan["interval"][interval], indent=2, ensure_ascii=False))

    ringkasan["selesai_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    Path(f"{a.out}/ringkasan_shard{a.shard:02d}.json").write_text(
        json.dumps(ringkasan, indent=2, ensure_ascii=False, default=str)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
