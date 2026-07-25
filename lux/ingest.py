"""Ingest Tier B: kline 1h dan 4h untuk seluruh universe perpetual.

Tier B dikerjakan lebih dulu, bukan Tier A (1m), dengan alasan yang disengaja:
volumenya kecil, sehingga kesalahan pipeline ketahuan murah. Keputusan itu sudah
terbukti dua kali. Putaran pertama menyingkap cacat URL non-ASCII, dan backfill
ekor menyingkap cacat parser header — keduanya dengan biaya belasan menit, bukan
berjam-jam pada 90 GB data 1-menit.

Validasi dijalankan SAAT ingest, bukan sesudahnya. Setiap simbol diperiksa
terhadap kisi waktu yang seharusnya, dan hasilnya ikut dilaporkan. Data yang
cacat tetap ditulis, tapi cacatnya tercatat — menyembunyikan cacat jauh lebih
berbahaya daripada memilikinya.

Dua jebakan format yang ditangani di sini:

1. Berkas CSV Binance yang lebih baru memiliki baris header, yang lama tidak.
   Membaca tanpa deteksi akan menyisipkan baris teks ke dalam kolom numerik.
   PERINGATAN yang lahir dari kesalahan nyata: header tidak boleh dilewati dua
   kali. Menggabungkan ``header=0`` dengan ``skiprows=1`` membuat pandas
   membuang baris header sekaligus memperlakukan baris DATA pertama sebagai
   nama kolom, sehingga tepat satu bar hilang dari setiap berkas berheader.
   Pada berkas bulanan kerugiannya cuma 1 dari 720 bar dan lolos dari perhatian;
   pada berkas harian kerugiannya 1 dari 24 dan langsung merusak rasio interval.
2. Sebagian berkas terbaru memakai stempel waktu MIKRODETIK, bukan milidetik.
   Tanpa normalisasi, dua berkas dari simbol yang sama tidak akan tersambung
   dan seluruh kisi waktu menjadi kacau.
"""

from __future__ import annotations

import argparse
import io
import json
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from lux import binance_vision as bv
from lux.universe import jenis_kontrak, quote_asset

KOLOM = [
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "quote_volume",
    "count",
    "taker_buy_base",
    "taker_buy_quote",
    "ignore",
]

SIMPAN = [
    "symbol",
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "quote_volume",
    "count",
    "taker_buy_base",
    "taker_buy_quote",
]

STEP_MS = {"1m": 60_000, "5m": 300_000, "15m": 900_000, "1h": 3_600_000, "4h": 14_400_000}

# Stempel waktu di atas ambang ini pasti mikrodetik. Milidetik untuk tahun 2286
# pun masih di bawahnya, jadi ambang ini aman.
AMBANG_MIKRO = 1e14


def baca_zip(path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as z:
        nama = [n for n in z.namelist() if n.endswith(".csv")]
        if not nama:
            raise RuntimeError(f"tidak ada CSV di {path}")
        with z.open(nama[0]) as f:
            mentah = f.read()

    if not mentah.strip():
        return pd.DataFrame(columns=KOLOM)

    awal = mentah[:64].decode("utf-8", "ignore").lstrip().lower()
    punya_header = awal.startswith("open_time")

    # ``header=None`` selalu, dan baris header dibuang HANYA lewat skiprows.
    # Jangan pernah memakai keduanya sekaligus; lihat catatan pada docstring
    # modul ini.
    df = pd.read_csv(
        io.BytesIO(mentah),
        header=None,
        names=KOLOM,
        skiprows=1 if punya_header else 0,
        dtype={c: "float64" for c in KOLOM[1:6] + KOLOM[7:11]},
    )

    if df.empty:
        return df

    ot = pd.to_numeric(df["open_time"], errors="coerce")
    df = df.loc[ot.notna()].copy()
    ot = ot.dropna()
    # Normalisasi mikrodetik ke milidetik.
    mikro = ot > AMBANG_MIKRO
    ot = ot.where(~mikro, ot // 1000)
    df["open_time"] = ot.astype("int64")
    return df


def ingest_simbol(symbol: str, interval: str, tmp: Path) -> tuple[pd.DataFrame, dict]:
    mulai = time.time()
    catatan = {"symbol": symbol, "interval": interval}

    try:
        bulan = bv.list_months(symbol, interval)
    except Exception as exc:  # noqa: BLE001
        catatan["error"] = f"listing gagal: {exc}"
        return pd.DataFrame(), catatan

    if not bulan:
        catatan["error"] = "tidak ada berkas bulanan"
        return pd.DataFrame(), catatan

    bagian = []
    gagal = []
    for b in bulan:
        url = bv.klines_url(symbol, interval, b)
        try:
            path = bv.download(url, tmp / bv.seg(symbol) / interval)
            bagian.append(baca_zip(path))
            path.unlink(missing_ok=True)
        except Exception as exc:  # noqa: BLE001
            gagal.append({"bulan": b, "galat": str(exc)[:200]})

    if not bagian:
        catatan["error"] = "semua unduhan gagal"
        catatan["gagal"] = gagal[:5]
        return pd.DataFrame(), catatan

    df = pd.concat(bagian, ignore_index=True)
    df["symbol"] = symbol

    sebelum = len(df)
    df = df.drop_duplicates(subset=["open_time"]).sort_values("open_time")
    duplikat = sebelum - len(df)

    # Periksa kisi waktu. Selisih antar bar HARUS konstan; setiap selisih lain
    # adalah celah yang harus tercatat, bukan diisi diam-diam.
    step = STEP_MS[interval]
    beda = df["open_time"].diff().dropna()
    celah = int((beda != step).sum())
    bar_diharapkan = int((df["open_time"].iloc[-1] - df["open_time"].iloc[0]) // step + 1)

    # Bar datar adalah bar tanpa pergerakan harga sama sekali. Rasio tinggi
    # menandakan instrumen tidak likuid, bukan kesalahan data, tapi tetap harus
    # terlihat sebelum masuk backtest.
    datar = int((df["high"] == df["low"]).sum())
    volume_nol = int((df["volume"] == 0).sum())

    catatan.update(
        {
            "bulan_tersedia": len(bulan),
            "bulan_gagal": len(gagal),
            "contoh_gagal": gagal[:3],
            "baris": len(df),
            "bar_diharapkan": bar_diharapkan,
            "bar_hilang": bar_diharapkan - len(df),
            "duplikat_dibuang": duplikat,
            "celah_kisi": celah,
            "bar_datar": datar,
            "rasio_bar_datar": round(datar / len(df), 4) if len(df) else None,
            "bar_volume_nol": volume_nol,
            "waktu_pertama": int(df["open_time"].iloc[0]),
            "waktu_terakhir": int(df["open_time"].iloc[-1]),
            "detik": round(time.time() - mulai, 2),
        }
    )
    return df[SIMPAN], catatan


def muat_universe(quote: str) -> list[str]:
    path = Path("reference/universe_symbols.parquet")
    if not path.exists():
        raise SystemExit(
            "reference/universe_symbols.parquet tidak ada. Jalankan workflow universe dulu."
        )
    df = pd.read_parquet(path)

    # Kolom klasifikasi mungkin belum ada bila parquet berasal dari versi lama.
    # Dihitung ulang agar penyaringan tidak pernah gagal diam-diam.
    if "contract_type" not in df.columns:
        df["contract_type"] = df["symbol"].map(jenis_kontrak)
    if "quote" not in df.columns:
        df["quote"] = df["symbol"].map(quote_asset)

    pilih = df[(df["contract_type"] == "perp") & (df["quote"] == quote)]
    return sorted(pilih["symbol"].tolist())


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--shard", type=int, default=0)
    p.add_argument("--shards", type=int, default=1)
    p.add_argument("--intervals", default="1h,4h")
    p.add_argument("--quote", default="USDT")
    p.add_argument("--workers", type=int, default=6)
    p.add_argument("--out", default="out")
    p.add_argument("--limit", type=int, default=0, help="batasi simbol untuk uji cepat")
    p.add_argument(
        "--symbols",
        default="",
        help="daftar simbol dipisah koma; melewati universe, dipakai untuk menambal",
    )
    p.add_argument(
        "--suffix",
        default="",
        help="akhiran nama berkas keluaran agar tambalan tidak menimpa aset penuh",
    )
    a = p.parse_args()

    if a.symbols.strip():
        semua = [s.strip() for s in a.symbols.split(",") if s.strip()]
    else:
        semua = muat_universe(a.quote)
    if a.limit:
        semua = semua[: a.limit]
    milik_saya = [s for i, s in enumerate(semua) if i % a.shards == a.shard]

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    tmp = Path("/tmp/lux_ingest")
    tmp.mkdir(parents=True, exist_ok=True)

    print(
        f"shard {a.shard}/{a.shards}: {len(milik_saya)} simbol dari {len(semua)} "
        f"({a.quote} perp)"
    )

    ringkasan = {
        "shard": a.shard,
        "shards": a.shards,
        "quote": a.quote,
        "simbol_ditugaskan": len(milik_saya),
        "mulai_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "interval": {},
    }

    for interval in a.intervals.split(","):
        interval = interval.strip()
        mulai = time.time()
        potongan = []
        catatan = []

        def kerjakan(s: str):
            return ingest_simbol(s, interval, tmp)

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
            berkas = out / f"ohlcv_{interval}_shard{a.shard:02d}{a.suffix}.parquet"
            gabung.to_parquet(
                berkas, index=False, compression="zstd", row_group_size=1_000_000
            )
            ukuran = berkas.stat().st_size
            baris = len(gabung)
        else:
            berkas, ukuran, baris = None, 0, 0

        bermasalah = [c for c in catatan if c.get("error") or c.get("celah_kisi", 0) > 0]
        ringkasan["interval"][interval] = {
            "baris": baris,
            "simbol_berhasil": sum(1 for c in catatan if not c.get("error")),
            "simbol_gagal": sum(1 for c in catatan if c.get("error")),
            "total_bar_hilang": sum(c.get("bar_hilang", 0) for c in catatan),
            "total_duplikat": sum(c.get("duplikat_dibuang", 0) for c in catatan),
            "total_celah_kisi": sum(c.get("celah_kisi", 0) for c in catatan),
            "simbol_bermasalah": len(bermasalah),
            "berkas": str(berkas) if berkas else None,
            "bytes": ukuran,
            "detik": round(time.time() - mulai, 1),
        }

        Path(f"{a.out}/detail_{interval}_shard{a.shard:02d}.json").write_text(
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
