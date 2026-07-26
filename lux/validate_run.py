"""Menjalankan validasi integritas dan kelayakan atas aset Parquet Tier B.

Dipanggil dari runner, bukan dari sandbox agen, karena berkasnya ratusan MB.

Keluaran sengaja mencatat **alasan** setiap penolakan, bukan hanya jumlahnya.
Laporan yang hanya menyebut "447 simbol lolos" tidak bisa didiagnosis, dan
angka yang tidak bisa didiagnosis pernah membuat riset ini kehilangan dua
putaran penuh.

ADR-016 langkah 3 menambahkan satu hal: nama berkas universe kini menyebut
interval. Sebelumnya seluruh interval menulis ke `universe_layak.json` yang sama,
sehingga validasi 4h akan menimpa semesta 1h tanpa satu pun pesan galat,
sementara `potong_ekor.yml` meneruskan tepat berkas itu lewat `--universe`.

ADR-017 menambahkan yang kedua: ambang jumlah bar dibaca per interval. `8760`
bukan angka sembarang melainkan satu tahun kalender dalam bar 1h; dipakai ulang
pada 4h ia diam-diam berubah makna menjadi empat tahun.

Pemakaian:
    python -m lux.validate_run --dir aset --interval 1h --config config/lux.yaml
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

from lux.validate import (
    AmbangKelayakan,
    median_quote_volume_harian,
    nilai_kelayakan,
    periksa_seri,
    rasio_bar_datar,
)

# Aset yang tidak boleh ikut dibaca. `_retry` adalah keluaran tambalan sebelum
# cacat parser header diperbaiki; simbolnya kini tercakup penuh oleh ingest
# normal. Membiarkannya ikut terbaca membuat tiga simbol terhitung dua kali dan
# muncul sebagai 12.593 "duplikat waktu" yang tampak seperti data rusak.
POLA_DILARANG = ("_retry",)

# Interval yang berkas universe-nya masih ditulis dengan nama lama. Hanya 1h,
# karena hanya 1h yang pernah punya pembaca: `potong_ekor.yml` meneruskan
# `reports/universe_layak.json` sebagai `--universe`.
INTERVAL_LEGASI = "1h"


def nama_keluaran_universe(interval: str) -> list[str]:
    """Nama berkas universe layak yang ditulis untuk sebuah interval.

    Keputusan ini hidup sebagai fungsi tingkat modul, bukan di dalam `main`,
    supaya ia dapat diuji tanpa parquet dan tanpa jaringan (aturan 32). Yang
    dicegah bukan kesalahan tulis melainkan penimpaan senyap: berkas legasi
    ditulis **hanya** untuk 1h, sehingga run 4h secara konstruksi tidak dapat
    menyentuh semesta 1h yang menjadi masukan ADR-003.

    Nama berinterval selalu berada di posisi pertama; ia yang kanonik.
    """
    nama = [f"universe_layak_{interval}.json"]
    if interval == INTERVAL_LEGASI:
        nama.append("universe_layak.json")
    return nama


def pilih_berkas(direktori: Path, interval: str) -> list[Path]:
    """Memilih berkas yang sah dibaca, dan menolak sisa aset usang.

    Penyaringan dilakukan di sini, bukan pada pola unduhan, supaya aturannya
    dapat diuji tanpa jaringan dan tidak diam-diam berubah saat workflow
    disunting.
    """
    semua = sorted(direktori.glob(f"ohlcv_{interval}_*.parquet"))
    return [p for p in semua if not any(t in p.name for t in POLA_DILARANG)]


def muat_ambang(path: Path, interval: str = INTERVAL_LEGASI) -> AmbangKelayakan:
    """Membaca ambang dari config. Gagal keras bila config tidak terbaca.

    Diam-diam memakai nilai bawaan akan membuat laporan tampak sah padahal
    aturannya bukan aturan yang disepakati.

    Lantai jumlah bar dibaca dari kunci `min_bar_<interval>` (ADR-017). Tidak ada
    jalan mundur ke `min_bar_1h`: satu tahun pada 1h adalah 8.760 bar sedangkan
    pada 4h 2.190, jadi mewarisi angka 1h berarti menuntut empat tahun riwayat
    tanpa seorang pun memutuskannya. Kunci yang hilang WAJIB menghentikan run,
    sebab semesta yang salah definisi sudah sekali menggugurkan satu hipotesis
    (H-011) tanpa memberi tahu apa pun tentang sinyal.
    """
    import yaml

    with path.open(encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    u = cfg["universe"]
    kunci_bar = f"min_bar_{interval}"
    if kunci_bar not in u:
        raise SystemExit(
            f"config {path} tidak memuat universe.{kunci_bar}; "
            f"tambahkan lantai riwayat untuk interval {interval} lebih dulu "
            f"(ADR-017). Nilai bawaan sengaja tidak disediakan."
        )
    return AmbangKelayakan(
        min_bar=int(u[kunci_bar]),
        min_median_quote_volume_harian=float(u["min_median_quote_volume_harian"]),
        maks_rasio_bar_datar=float(u["maks_rasio_bar_datar"]),
    )


def muat_semua(direktori: Path, interval: str) -> tuple[pd.DataFrame, list[str]]:
    """Menggabungkan seluruh shard yang sah, termasuk ekor harian.

    Satu simbol bisa tersebar di berkas bulanan dan berkas ekor dengan nomor
    shard berbeda, karena jumlah shard kedua tahap tidak sama. Karena itu
    penggabungan harus dilakukan atas seluruh berkas, bukan per shard.
    """
    berkas = pilih_berkas(direktori, interval)
    if not berkas:
        raise SystemExit(f"tidak ada berkas ohlcv_{interval}_*.parquet sah di {direktori}")
    diabaikan = [
        p.name
        for p in sorted(direktori.glob(f"ohlcv_{interval}_*.parquet"))
        if p not in berkas
    ]
    for nama in diabaikan:
        print(f"  DIABAIKAN (aset usang): {nama}", flush=True)
    bagian = []
    for p in berkas:
        df = pd.read_parquet(p)
        bagian.append(df)
        print(f"  dibaca {p.name}: {len(df):,} baris", flush=True)
    gabung = pd.concat(bagian, ignore_index=True)
    gabung["symbol"] = gabung["symbol"].astype(str)
    return gabung, diabaikan


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--interval", default="1h")
    ap.add_argument("--config", default="config/lux.yaml")
    ap.add_argument("--out", default="reports")
    a = ap.parse_args(argv)

    ambang = muat_ambang(Path(a.config), a.interval)
    print(
        f"interval {a.interval} "
        f"ambang: min_bar={ambang.min_bar} "
        f"min_median_quote={ambang.min_median_quote_volume_harian:,.0f} "
        f"maks_bar_datar={ambang.maks_rasio_bar_datar}",
        flush=True,
    )

    df, diabaikan = muat_semua(Path(a.dir), a.interval)
    print(f"total {len(df):,} baris, {df['symbol'].nunique()} simbol", flush=True)

    hasil: list[dict] = []
    for symbol, bagian in df.groupby("symbol", sort=True, observed=True):
        bagian = bagian.sort_values("open_time").reset_index(drop=True)
        h = periksa_seri(bagian, str(symbol), a.interval)
        median = median_quote_volume_harian(bagian, a.interval)
        layak, alasan = nilai_kelayakan(h, median, ambang)
        baris = h.sebagai_dict()
        baris.pop("catatan", None)
        baris["median_quote_harian"] = round(median, 2)
        baris["rasio_bar_datar"] = round(rasio_bar_datar(h), 4)
        baris["layak"] = layak
        baris["alasan"] = alasan
        hasil.append(baris)

    integritas_gagal = [h for h in hasil if not h["lulus"]]
    layak = [h for h in hasil if h["layak"]]
    tidak_layak = [h for h in hasil if not h["layak"]]

    # Kenapa simbol ditolak, bukan sekadar berapa banyak.
    sebab = Counter()
    for h in tidak_layak:
        for al in h["alasan"]:
            sebab[al.split(" (")[0]] += 1

    ringkas = {
        "interval": a.interval,
        "min_bar": ambang.min_bar,
        "berkas_diabaikan": diabaikan,
        "total_simbol": len(hasil),
        "total_baris": int(len(df)),
        "integritas_gagal": len(integritas_gagal),
        "layak": len(layak),
        "tidak_layak": len(tidak_layak),
        "sebab_penolakan": dict(sebab),
        "total_celah": int(sum(h["celah"] for h in hasil)),
        "total_duplikat": int(sum(h["duplikat_waktu"] for h in hasil)),
        "gerbang_integritas_lulus": len(integritas_gagal) == 0,
    }

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"validate_{a.interval}.json").write_text(
        json.dumps({"ringkasan": ringkas, "per_simbol": hasil}, indent=2),
        encoding="utf-8",
    )
    teks_universe = json.dumps(
        {
            "interval": a.interval,
            "ambang": {
                "min_bar": ambang.min_bar,
                "min_median_quote_volume_harian": ambang.min_median_quote_volume_harian,
                "maks_rasio_bar_datar": ambang.maks_rasio_bar_datar,
            },
            "jumlah": len(layak),
            "simbol": sorted(h["symbol"] for h in layak),
        },
        indent=2,
    )
    for nama in nama_keluaran_universe(a.interval):
        (out / nama).write_text(teks_universe, encoding="utf-8")
        print(f"  universe ditulis: {nama}", flush=True)

    baris_md = [
        f"# Validasi Tier B {a.interval}",
        "",
        f"Total {ringkas['total_baris']:,} baris atas {ringkas['total_simbol']} simbol.",
        f"Lantai riwayat interval ini: {ambang.min_bar:,} bar.",
        "",
        "## Integritas",
        "",
        f"- Simbol dengan pelanggaran fatal: **{ringkas['integritas_gagal']}**",
        f"- Total duplikat waktu: {ringkas['total_duplikat']:,}",
        f"- Total celah (bukan pelanggaran; perdagangan memang pernah berhenti): "
        f"{ringkas['total_celah']:,}",
    ]
    if diabaikan:
        baris_md += ["", f"- Berkas usang yang sengaja diabaikan: {', '.join(diabaikan)}"]

    baris_md += [
        "",
        "## Kelayakan universe backtest",
        "",
        f"- **Layak: {ringkas['layak']} dari {ringkas['total_simbol']}**",
        f"- Ditolak: {ringkas['tidak_layak']}",
        "",
        "Satu simbol dapat ditolak oleh lebih dari satu sebab, jadi kolom di bawah",
        "tidak dimaksudkan berjumlah sama dengan total penolakan.",
        "",
        "| Sebab penolakan | Simbol |",
        "|---|---|",
    ]
    for k, v in sorted(sebab.items(), key=lambda kv: -kv[1]):
        baris_md.append(f"| {k} | {v} |")

    if integritas_gagal:
        baris_md += [
            "",
            "## Simbol yang gagal integritas",
            "",
            "| Simbol | Duplikat | Tidak urut | Luar kisi | High<max | Low>min | "
            "Harga\u22640 | Kosong |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for h in integritas_gagal[:50]:
            baris_md.append(
                f"| {h['symbol']} | {h['duplikat_waktu']} | {h['waktu_tidak_urut']} | "
                f"{h['tidak_selaras_kisi']} | {h['high_lebih_kecil']} | "
                f"{h['low_lebih_besar']} | {h['harga_non_positif']} | {h['nilai_kosong']} |"
            )

    terpendek = sorted(hasil, key=lambda h: h["baris"])[:10]
    baris_md += [
        "",
        "## Sepuluh simbol dengan riwayat terpendek",
        "",
        "| Simbol | Bar | Median quote harian | Layak |",
        "|---|---|---|---|",
    ]
    for h in terpendek:
        baris_md.append(
            f"| {h['symbol']} | {h['baris']:,} | {h['median_quote_harian']:,.0f} | "
            f"{'ya' if h['layak'] else 'tidak'} |"
        )

    terpanjang = sorted(hasil, key=lambda h: -h["baris"])[:10]
    baris_md += [
        "",
        "## Sepuluh simbol dengan riwayat terpanjang",
        "",
        "| Simbol | Bar | Median quote harian | Celah | Layak |",
        "|---|---|---|---|---|",
    ]
    for h in terpanjang:
        baris_md.append(
            f"| {h['symbol']} | {h['baris']:,} | {h['median_quote_harian']:,.0f} | "
            f"{h['celah']} | {'ya' if h['layak'] else 'tidak'} |"
        )

    (out / f"validate_{a.interval}.md").write_text("\n".join(baris_md) + "\n", encoding="utf-8")

    print(json.dumps(ringkas, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
