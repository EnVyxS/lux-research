"""Ingest funding rate perpetual dari arsip Binance Vision.

Tanpa funding, model biaya perpetual bohong. Biaya transaksi hanya muncul dua
kali per posisi, sedangkan funding menagih setiap delapan jam selama posisi
dipegang. Strategi tren yang menahan posisi berhari-hari bisa membayar funding
berkali lipat dari ongkos masuk-keluarnya.

Bentuk arsipnya berbeda dari klines: tidak ada segmen interval pada path.

    data/futures/um/monthly/fundingRate/{SYMBOL}/{SYMBOL}-fundingRate-YYYY-MM.zip

Seluruh pelajaran parser dari ingest klines dipasang di sini sejak awal, bukan
ditemukan lagi lewat data cacat:

- ``utf-8-sig`` supaya BOM tidak merusak deteksi header;
- tanpa ``dtype`` ketat, konversi memakai ``errors="coerce"``, supaya satu
  baris sampah tidak menggagalkan satu bulan penuh;
- ``header=None`` dengan ``skiprows`` yang dihitung, bukan ``header=0``
  bersamaan ``skiprows``, yang dulu membuang satu baris tiap berkas;
- stempel mikrodetik dinormalisasi ke milidetik;
- berkas tanpa baris data dikembalikan sebagai frame kosong, bukan galat.
  Bulan tanpa funding memang ada, misalnya saat kontrak baru terdaftar di
  penghujung bulan, dan satu berkas semacam itu tidak boleh menghapus seluruh
  riwayat simbolnya.
"""

from __future__ import annotations

import argparse
import io
import json
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

from lux import binance_vision as bv

KOLOM = ["calc_time", "funding_interval_hours", "last_funding_rate"]
KOLOM_SEMPIT = ["calc_time", "last_funding_rate"]

# Stempel di atas ambang ini pasti mikrodetik, bukan milidetik: 1e14 ms setara
# tahun 5138, jauh di luar rentang data mana pun yang masuk akal.
AMBANG_MIKRO = 1e14

JAM_MS = 3_600_000

# Funding rate wajar berada jauh di bawah 1%. Nilai di atas ambang ini tidak
# dibuang, hanya dihitung, karena lonjakan ekstrem memang pernah terjadi dan
# membuangnya diam-diam berarti menyembunyikan biaya nyata dari backtest.
AMBANG_EKSTREM = 0.02


def frame_kosong() -> pd.DataFrame:
    return pd.DataFrame({k: pd.Series(dtype="float64") for k in KOLOM})


def funding_url(symbol: str, month: str) -> str:
    s = bv.seg(symbol)
    return f"{bv.CDN}/{bv.ROOT}/monthly/fundingRate/{s}/{s}-fundingRate-{month}.zip"


def list_bulan(symbol: str) -> list[str]:
    """Bulan yang tersedia, ``YYYY-MM``. Path funding tanpa segmen interval."""
    base = f"{bv.ROOT}/monthly/fundingRate/{symbol}/"
    bulan = set()
    for key in bv.list_keys(base):
        nama = key.rsplit("/", 1)[-1]
        if not nama.endswith(".zip"):
            continue
        bagian = nama[:-4].split("-")
        if len(bagian) >= 2:
            bulan.add(f"{bagian[-2]}-{bagian[-1]}")
    return sorted(bulan)


def baca_zip(path: Path) -> pd.DataFrame:
    """Membaca satu ZIP funding menjadi DataFrame bersih.

    Lebar kolom ditangani secara defensif: arsip lama sempat tidak memuat kolom
    ``funding_interval_hours``. Menebak lebar dan salah akan menggeser seluruh
    kolom tanpa melempar galat, dan pergeseran senyap itu jenis kerusakan yang
    paling mahal.
    """
    with zipfile.ZipFile(path) as z:
        nama = z.namelist()[0]
        mentah = z.read(nama)

    awal = mentah[:64].decode("utf-8-sig", "ignore").lstrip().lstrip("\ufeff").lower()
    punya_header = awal.startswith("calc_time")

    try:
        df = pd.read_csv(
            io.BytesIO(mentah),
            header=None,
            skiprows=1 if punya_header else 0,
            encoding="utf-8-sig",
        )
    except pd.errors.EmptyDataError:
        # Berkas hanya berisi header, atau kosong sama sekali. Ini keadaan sah,
        # bukan kerusakan, dan harus dikembalikan sebagai frame kosong supaya
        # bulan-bulan lain pada simbol yang sama tetap terbaca.
        return frame_kosong()

    if df.shape[1] >= 3:
        df = df.iloc[:, :3]
        df.columns = KOLOM
    elif df.shape[1] == 2:
        df.columns = KOLOM_SEMPIT
        df["funding_interval_hours"] = pd.NA
        df = df[KOLOM]
    else:
        raise ValueError(f"lebar kolom tak terduga: {df.shape[1]} pada {path.name}")

    for c in KOLOM:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(subset=["calc_time", "last_funding_rate"])
    if df.empty:
        return frame_kosong()

    besar = df["calc_time"] > AMBANG_MIKRO
    if besar.any():
        df.loc[besar, "calc_time"] = df.loc[besar, "calc_time"] // 1000

    df["calc_time"] = df["calc_time"].astype("int64")
    return df.reset_index(drop=True)


def periksa(df: pd.DataFrame) -> dict:
    """Invarian funding. Dilaporkan sebagai jumlah, bukan lulus/gagal saja."""
    if df.empty:
        return {
            "baris": 0,
            "duplikat": 0,
            "tidak_urut": 0,
            "celah": 0,
            "positif": 0,
            "negatif": 0,
            "ekstrem": 0,
            "rate_min": None,
            "rate_maks": None,
            "interval_jam": [],
        }

    t = df["calc_time"]
    beda = t.diff().dropna()

    jam = sorted(
        int(x) for x in pd.unique(df["funding_interval_hours"].dropna()) if x == x
    )
    # Kisi funding tidak selalu 8 jam. Sebagian pasangan memakai 4 jam, dan
    # sebagian pernah berpindah. Karena itu langkah yang diharapkan diambil dari
    # data, bukan diasumsikan.
    langkah = int(jam[0]) * JAM_MS if jam else 8 * JAM_MS

    r = df["last_funding_rate"]
    return {
        "baris": int(len(df)),
        "duplikat": int(t.duplicated().sum()),
        "tidak_urut": int((beda < 0).sum()),
        "celah": int((beda != langkah).sum()),
        "positif": int((r > 0).sum()),
        "negatif": int((r < 0).sum()),
        "ekstrem": int((r.abs() > AMBANG_EKSTREM).sum()),
        "rate_min": float(r.min()),
        "rate_maks": float(r.max()),
        "interval_jam": jam,
    }


def ingest_simbol(symbol: str, tmp: Path) -> tuple[pd.DataFrame, dict]:
    bulan = list_bulan(symbol)
    bagian: list[pd.DataFrame] = []
    gagal: list[str] = []

    for b in bulan:
        url = funding_url(symbol, b)
        try:
            path = bv.download(url, tmp / symbol)
            df_bulan = baca_zip(path)
            if not df_bulan.empty:
                bagian.append(df_bulan)
            path.unlink(missing_ok=True)
        except Exception as exc:  # noqa: BLE001
            gagal.append(f"{b}: {exc}")

    if not bagian:
        return pd.DataFrame(), {
            "symbol": symbol,
            "bulan": len(bulan),
            "gagal": gagal,
            **periksa(pd.DataFrame()),
        }

    df = pd.concat(bagian, ignore_index=True)
    df = df.drop_duplicates(subset=["calc_time"]).sort_values("calc_time")
    df = df.reset_index(drop=True)
    df.insert(0, "symbol", symbol)

    stat = {"symbol": symbol, "bulan": len(bulan), "gagal": gagal, **periksa(df)}
    return df, stat


def muat_simbol_layak(path: Path) -> list[str]:
    """Funding hanya diambil untuk simbol yang akan diuji.

    Mengambil funding untuk 790 simbol saat hanya 447 yang layak berarti
    membayar waktu runner untuk data yang tidak akan pernah dipakai.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    return list(data["simbol"])


def gabungkan_laporan(direktori: Path, keluaran: Path) -> dict:
    detail: list[dict] = []
    for p in sorted(direktori.glob("detail_funding_shard*.json")):
        detail += json.loads(p.read_text(encoding="utf-8"))

    berhasil = [d for d in detail if d["baris"] > 0]
    gagal = [d for d in detail if d["baris"] == 0]
    kisi: dict[str, int] = {}
    for d in detail:
        for j in d.get("interval_jam", []):
            kisi[str(j)] = kisi.get(str(j), 0) + 1

    ringkas = {
        "simbol_total": len(detail),
        "simbol_berhasil": len(berhasil),
        "simbol_kosong": len(gagal),
        "baris": sum(d["baris"] for d in detail),
        "duplikat": sum(d["duplikat"] for d in detail),
        "tidak_urut": sum(d["tidak_urut"] for d in detail),
        "celah": sum(d["celah"] for d in detail),
        "positif": sum(d["positif"] for d in detail),
        "negatif": sum(d["negatif"] for d in detail),
        "ekstrem": sum(d["ekstrem"] for d in detail),
        "sebaran_interval_jam": kisi,
        "simbol_kosong_nama": sorted(d["symbol"] for d in gagal)[:50],
    }
    ringkas["gerbang_lulus"] = (
        ringkas["duplikat"] == 0
        and ringkas["tidak_urut"] == 0
        and ringkas["simbol_kosong"] == 0
        and ringkas["baris"] > 0
    )

    keluaran.parent.mkdir(parents=True, exist_ok=True)
    (keluaran.parent / "funding.json").write_text(
        json.dumps({"ringkasan": ringkas, "per_simbol": detail}, indent=2),
        encoding="utf-8",
    )

    total_arah = ringkas["positif"] + ringkas["negatif"]
    pangsa = ringkas["positif"] / total_arah if total_arah else 0.0
    md = [
        "# Ingest funding rate",
        "",
        f"- Simbol: **{ringkas['simbol_berhasil']} dari {ringkas['simbol_total']}**",
        f"- Baris: **{ringkas['baris']:,}**",
        f"- Duplikat: {ringkas['duplikat']} | Tidak urut: {ringkas['tidak_urut']} | "
        f"Celah kisi: {ringkas['celah']:,}",
        f"- Funding positif: {ringkas['positif']:,} "
        f"({pangsa:.1%}) | negatif: {ringkas['negatif']:,}",
        f"- Melebihi {AMBANG_EKSTREM:.0%}: {ringkas['ekstrem']:,} (dicatat, tidak dibuang)",
        f"- Sebaran interval funding (jam): {ringkas['sebaran_interval_jam']}",
        "",
        f"Gerbang lulus: **{ringkas['gerbang_lulus']}**",
        "",
        "Pangsa funding positif di atas 50% berarti pemegang posisi long membayar",
        "lebih sering daripada menerima. Itu biaya struktural yang harus ditanggung",
        "strategi long-bias, dan mengabaikannya membuat backtest tampak lebih baik",
        "daripada kenyataannya.",
    ]
    keluaran.write_text("\n".join(md) + "\n", encoding="utf-8")
    return ringkas


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--shards", type=int, default=1)
    ap.add_argument("--universe", default="reports/universe_layak.json")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--out", default="out")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--merge", default="")
    a = ap.parse_args(argv)

    if a.merge:
        ringkas = gabungkan_laporan(Path(a.merge), Path("reports/funding.md"))
        print(json.dumps(ringkas, indent=2))
        return 0

    simbol = muat_simbol_layak(Path(a.universe))
    if a.limit:
        simbol = simbol[: a.limit]
    milik_saya = [s for i, s in enumerate(simbol) if i % a.shards == a.shard]
    print(f"shard {a.shard}/{a.shards}: {len(milik_saya)} simbol", flush=True)

    tmp = Path("/tmp/lux_funding")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    hasil: list[pd.DataFrame] = []
    detail: list[dict] = []

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        for df, stat in ex.map(lambda s: ingest_simbol(s, tmp), milik_saya):
            if not df.empty:
                hasil.append(df)
            detail.append(stat)
            print(f"  {stat['symbol']}: {stat['baris']} baris", flush=True)

    nama = f"{a.shard:02d}"
    if hasil:
        gabung = pd.concat(hasil, ignore_index=True)
        gabung["symbol"] = gabung["symbol"].astype("category")
        gabung.to_parquet(
            out / f"funding_shard{nama}.parquet",
            compression="zstd",
            row_group_size=1_000_000,
            index=False,
        )

    (out / f"detail_funding_shard{nama}.json").write_text(
        json.dumps(detail, indent=2), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
