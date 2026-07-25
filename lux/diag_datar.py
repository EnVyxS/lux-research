"""Membongkar blok bar datar: di mana letaknya, satu harga atau banyak, ada volume atau tidak.

Gerbang ``gerbang_forward_fill`` hanya menjawab "berapa". Berapa tidak dapat
ditindaklanjuti. Menghapus simbol, memperlebar ambang, dan memperbaiki pipa data
adalah tiga tindakan yang sangat berbeda, dan yang menentukan pilihannya bukan
panjang blok melainkan **sebabnya**.

Tiga penanda di sini memisahkan tiga sebab yang berbeda konsekuensinya:

- **Letak** (``posisi_frac``). Blok yang menempel di awal riwayat hampir selalu
  padding: bar yang dibuat sebelum simbolnya benar-benar diperdagangkan. Blok di
  tengah riwayat berarti feed berhenti sementara, dan itu masalah lain.
- **Jumlah harga unik**. Satu harga sepanjang blok berarti nilai terakhir
  disalin berulang; harga yang tetap melangkah meski tiap barnya datar berarti
  pasarnya nyata tetapi bertransaksi jarang. Yang pertama data palsu, yang kedua
  data sah yang tidak layak diperdagangkan. Keduanya harus ditolak, tetapi hanya
  yang pertama menuntut perbaikan pipa data.
- **Volume**. Bar datar dengan volume nol adalah ketiadaan transaksi. Bar datar
  dengan volume positif adalah transaksi nyata pada satu harga, yang mungkin
  saja terjadi pada aset yang sangat tidak likuid.

Alasan modul ini ada sama sekali: pada run pilot, deret datar terpanjang hampir
sama panjangnya dengan seluruh bar datar simbol itu. Bar datar yang tersebar
adalah sifat pasar; bar datar yang menggumpal dalam satu blok adalah peristiwa.
Peristiwa punya tanggal, dan tanggal dapat dicocokkan dengan riwayat perakitan
data.

Jalur baca sengaja diambil dari ``lux.backtest.run_wf.pilih_berkas`` supaya
diagnostik ini melihat kumpulan berkas yang sama persis dengan yang dipakai
backtest. Jalur baca kedua yang ditulis ulang di sini akan menjadi tempat
ketiganya bisa berbeda tanpa ada yang menyadari.

Pemakaian:
    python -m lux.diag_datar --dir aset --interval 1h \\
        --universe reports/universe_layak.json --min-panjang 24
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd

from lux.backtest.run_wf import pilih_berkas

KOLOM_BACA = [
    "symbol",
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "count",
]


def _deret(mask: np.ndarray) -> list[tuple[int, int]]:
    """Batas tiap deret ``True`` yang bersambung, sebagai pasangan indeks inklusif.

    Ditulis lewat selisih agar tidak ada lingkaran Python atas 14 juta bar. Dua
    ujung array ditangani terpisah karena selisih tidak pernah melaporkan deret
    yang dimulai pada indeks nol atau berakhir pada indeks terakhir.
    """
    if mask.size == 0:
        return []
    d = np.diff(mask.astype(np.int8))
    mulai = list(np.flatnonzero(d == 1) + 1)
    akhir = list(np.flatnonzero(d == -1))
    if bool(mask[0]):
        mulai.insert(0, 0)
    if bool(mask[-1]):
        akhir.append(int(mask.size - 1))
    return [(int(a), int(b)) for a, b in zip(mulai, akhir)]


def blok_datar(df: pd.DataFrame, min_panjang: int = 2) -> list[dict]:
    """Semua blok bar datar bersambung, terpanjang lebih dulu.

    Definisi bar datar sama persis dengan gerbangnya: keempat harga sama. Ia
    tidak diimpor dari sana melainkan diulang, karena gerbang mengembalikan satu
    angka sedangkan yang dibutuhkan di sini adalah batas tiap bloknya.
    """
    n = len(df)
    if n == 0:
        return []
    o = df["open"].to_numpy(dtype="float64")
    h = df["high"].to_numpy(dtype="float64")
    l = df["low"].to_numpy(dtype="float64")
    c = df["close"].to_numpy(dtype="float64")
    t = df["open_time"].to_numpy(dtype="int64")
    datar = (o == h) & (h == l) & (l == c)

    if "volume" in df.columns:
        vol = df["volume"].to_numpy(dtype="float64")
    else:
        vol = np.full(n, np.nan)
    if "count" in df.columns:
        cnt = df["count"].to_numpy(dtype="float64")
    else:
        cnt = np.full(n, np.nan)

    keluar: list[dict] = []
    for a, b in _deret(datar):
        panjang = b - a + 1
        if panjang < min_panjang:
            continue
        potong = c[a : b + 1]
        keluar.append(
            {
                "indeks_mulai": a,
                "indeks_akhir": b,
                "panjang": int(panjang),
                "mulai_ms": int(t[a]),
                "akhir_ms": int(t[b]),
                "harga_unik": int(np.unique(potong).size),
                "harga_awal": float(potong[0]),
                "harga_akhir": float(potong[-1]),
                "volume_total": float(np.nansum(vol[a : b + 1])),
                "count_total": float(np.nansum(cnt[a : b + 1])),
                "posisi_frac": float(a / n),
            }
        )
    keluar.sort(key=lambda r: -r["panjang"])
    return keluar


def letak(posisi_frac: float, batas: float = 0.02) -> str:
    """Nama letak blok, supaya laporan dapat dibaca tanpa menafsirkan pecahan.

    Ambang 2% dipakai untuk "awal" karena padding pra-listing selalu menempel
    persis di indeks nol; blok yang mulai setelah 2% riwayat sudah berlalu bukan
    padding, apa pun sebabnya.
    """
    if posisi_frac <= batas:
        return "awal"
    if posisi_frac >= 1.0 - batas:
        return "akhir"
    return "tengah"


def tanggal(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=UTC).strftime("%Y-%m-%d")


def ringkas_simbol(symbol: str, df: pd.DataFrame, min_panjang: int) -> dict | None:
    """Satu baris laporan untuk satu simbol, atau ``None`` bila bersih."""
    blok = blok_datar(df, min_panjang=min_panjang)
    if not blok:
        return None
    semua_datar = int(sum(b["panjang"] for b in blok_datar(df, min_panjang=1)))
    terpanjang = blok[0]
    return {
        "symbol": symbol,
        "bar": int(len(df)),
        "bar_datar": semua_datar,
        "rasio_datar": float(semua_datar / len(df)) if len(df) else 0.0,
        "jumlah_blok": len(blok),
        "terpanjang": terpanjang,
        "porsi_datar_di_blok_terpanjang": (
            float(terpanjang["panjang"] / semua_datar) if semua_datar else 0.0
        ),
        "blok": blok[:5],
    }


def muat(direktori: Path, interval: str, simbol: set[str]) -> dict[str, pd.DataFrame]:
    berkas = pilih_berkas(Path(direktori), interval)
    if not berkas:
        raise SystemExit(f"tidak ada ohlcv_{interval}_*.parquet sah di {direktori}")
    bagian = []
    for p in berkas:
        df = pd.read_parquet(p, columns=KOLOM_BACA)
        df["symbol"] = df["symbol"].astype(str)
        bagian.append(df[df["symbol"].isin(simbol)])
        print(f"  dibaca {p.name}", flush=True)
    gabung = pd.concat(bagian, ignore_index=True)
    hasil: dict[str, pd.DataFrame] = {}
    for s, b in gabung.groupby("symbol", sort=True, observed=True):
        hasil[str(s)] = b.sort_values("open_time").reset_index(drop=True)
    return hasil


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--interval", default="1h")
    ap.add_argument("--universe", default="reports/universe_layak.json")
    ap.add_argument("--out", default="reports")
    ap.add_argument("--min-panjang", type=int, default=24)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args(argv)

    semesta = json.loads(Path(a.universe).read_text(encoding="utf-8"))["simbol"]
    dipilih = sorted(semesta)[: a.limit] if a.limit > 0 else sorted(semesta)
    print(f"universe layak {len(semesta)}, dipindai {len(dipilih)}", flush=True)

    bingkai = muat(Path(a.dir), a.interval, set(dipilih))
    print(f"{len(bingkai)} simbol dimuat", flush=True)

    baris = []
    for s in sorted(bingkai):
        r = ringkas_simbol(s, bingkai[s], a.min_panjang)
        if r is not None:
            baris.append(r)
    baris.sort(key=lambda r: -r["terpanjang"]["panjang"])

    n_awal = sum(1 for r in baris if letak(r["terpanjang"]["posisi_frac"]) == "awal")
    n_tengah = sum(1 for r in baris if letak(r["terpanjang"]["posisi_frac"]) == "tengah")
    n_akhir = sum(1 for r in baris if letak(r["terpanjang"]["posisi_frac"]) == "akhir")
    n_beku = sum(1 for r in baris if r["terpanjang"]["harga_unik"] == 1)
    n_tanpa_volume = sum(1 for r in baris if r["terpanjang"]["volume_total"] == 0.0)

    isi = {
        "interval": a.interval,
        "min_panjang": a.min_panjang,
        "simbol_dipindai": len(bingkai),
        "simbol_bermasalah": len(baris),
        "letak_terpanjang": {"awal": n_awal, "tengah": n_tengah, "akhir": n_akhir},
        "blok_terpanjang_satu_harga": n_beku,
        "blok_terpanjang_tanpa_volume": n_tanpa_volume,
        "simbol": baris,
    }
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "diag_datar.json").write_text(
        json.dumps(isi, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    md = [
        "# Diagnostik blok bar datar",
        "",
        "Bar datar yang tersebar adalah sifat pasar. Bar datar yang menggumpal "
        "dalam satu blok bersambung adalah peristiwa, dan peristiwa punya tanggal.",
        "",
        f"- Interval: **{a.interval}** \u00b7 ambang blok: **{a.min_panjang} bar**",
        f"- Simbol dipindai: **{len(bingkai):,}**",
        f"- Simbol dengan blok melewati ambang: **{len(baris):,}**",
        f"- Letak blok terpanjang: awal **{n_awal}**, tengah **{n_tengah}**, "
        f"akhir **{n_akhir}**",
        f"- Blok terpanjang yang harganya persis satu nilai: **{n_beku}**",
        f"- Blok terpanjang yang volumenya nol: **{n_tanpa_volume}**",
        "",
        "## Tiga puluh blok terpanjang",
        "",
        "| Simbol | Bar | Rasio datar | Blok | Panjang | Porsi datar | Letak | "
        "Mulai | Selesai | Harga unik | Volume | Count |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in baris[:30]:
        b = r["terpanjang"]
        md.append(
            f"| {r['symbol']} | {r['bar']:,} | {r['rasio_datar']:.4f} | "
            f"{r['jumlah_blok']} | {b['panjang']:,} | "
            f"{r['porsi_datar_di_blok_terpanjang']:.3f} | "
            f"{letak(b['posisi_frac'])} | {tanggal(b['mulai_ms'])} | "
            f"{tanggal(b['akhir_ms'])} | {b['harga_unik']:,} | "
            f"{b['volume_total']:,.0f} | {b['count_total']:,.0f} |"
        )
    md += [""]
    (out / "diag_datar.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
