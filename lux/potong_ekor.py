"""Memangkas ekor datar simbol mati dan menghitung tanggal kematian sejati.

Pelaksanaan ADR-003. Diagnostik ``lux.diag_datar`` membuktikan bahwa 62 dari 447
simbol layak berakhir dengan blok bar datar berharga tunggal yang membentang
sampai bar terakhir dataset, sebagian sepanjang dua puluh bulan. Harga terakhir
simbol yang berhenti diperdagangkan disalin berulang sampai ujung dataset.

Akibat terpenting bukan bar palsu yang dapat diperdagangkan, melainkan bahwa
**gerbang survivorship kehilangan kemampuannya untuk gagal**. Simbol mati
dikenali dari stempel bar terakhirnya, dan bar terakhir simbol mati ini sama
dengan bar terakhir simbol yang masih hidup.

Aset Parquet sengaja tidak ditulis ulang. Aset bersifat write-once, dan menulis
ulang 703 MB data untuk membuang ekornya akan menghapus kemampuan memeriksa
kembali keputusan ini terhadap data aslinya. Pemangkasan dilakukan saat muat,
dan tanggal kematian sejati disimpan sekali sebagai tabel yang dapat dibaca
manusia supaya angka yang dipakai gerbang survivorship dapat diperiksa.

ADR-018 menambahkan dua hal, keduanya karena kerangka 4h.

Pertama, ambang panjang ekor dihitung dari **waktu**, bukan dari jumlah bar yang
diwarisi: satu hari kalender berarti 24 bar pada 1h dan 6 bar pada 4h. Memakai
24 untuk 4h akan membiarkan ekor palsu sepanjang satu sampai tiga hari lolos
tanpa terdeteksi.

Kedua, keluaran modul ini kini menyebut interval. Sebelumnya keempat berkasnya
bernama sama untuk interval apa pun, sementara ``backtest.yml`` membaca dua di
antaranya — sehingga run 4h akan menimpa masukan backtest 1h tanpa satu pun
pesan galat.

Pemakaian:
    python -m lux.potong_ekor --dir aset --interval 4h \\
        --universe reports/universe_layak_4h.json --out reports
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from lux.diag_datar import KOLOM_BACA, blok_datar, tanggal
from lux.backtest.run_wf import pilih_berkas
from lux.validate_run import INTERVAL_LEGASI, muat_ambang

# Ambang panjang ekor dinyatakan dalam WAKTU, lalu diterjemahkan ke jumlah bar.
# Angka 24 pada 1h bukan angka sembarang: ia satu hari kalender, dan ia sengaja
# sama dengan maks_deret_datar pada gerbang forward_fill supaya yang dipangkas di
# sini persis yang dikeluhkan di sana. ADR-018 bagian 4 mencatat bahwa kesamaan
# itu belum berlaku untuk 4h, dan bahwa menyamakannya adalah prasyarat H-013.
JAM_SEHARI = 24
INTERVAL_JAM = {"1h": 1, "4h": 4}

# Nilai bawaan fungsi, setara satu hari pada 1h. `main` selalu memasok nilai per
# interval secara eksplisit; konstanta ini tidak pernah menjadi jalan mundur
# senyap bagi interval lain.
MIN_PANJANG = JAM_SEHARI // INTERVAL_JAM[INTERVAL_LEGASI]

# ADR-003 butir 6: diturunkan dari 0,30. Sesudah ekor palsu hilang, membiarkan
# 30% bar tanpa transaksi bukan lagi toleransi yang dapat dipertanggungjawabkan.
# Rasio simbol bermasalah berdesakan tepat di bawah 0,30 (DFUSDT 0,2950,
# MYROUSDT 0,2899, RENUSDT 0,2836), yang menunjukkan ambang lama disetel pas di
# atas kelas cacat yang seharusnya ia tangkap.
#
# ADR-018 mempertahankan 0,10 untuk kedua interval, dengan keberatan tertulis:
# rasio bar datar 4h mekanis lebih kecil, jadi gerbang ini lebih LONGGAR di sana.
MAKS_RASIO_DATAR = 0.10

# Berkas keluaran, dengan nama dasar tanpa interval. Dua yang pertama dibaca oleh
# backtest.yml; itu sebabnya nama lama tetap ditulis untuk 1h.
BERKAS_DASAR = (
    "akhir_sejati.json",
    "universe_layak_v2.json",
    "potong_ekor.json",
    "potong_ekor.md",
)


def min_panjang_untuk(interval: str) -> int:
    """Panjang ekor minimum dalam bar, setara satu hari kalender.

    Gagal keras untuk interval yang belum diputuskan. Nilai bawaan tersembunyi
    adalah tepat cacat yang ADR-017 dan ADR-018 perbaiki: angka yang benar untuk
    satu interval berubah makna, bukan berubah nilai, ketika dipakai di interval
    lain.
    """
    if interval not in INTERVAL_JAM:
        raise SystemExit(
            f"interval {interval} belum punya ambang ekor datar; tambahkan ke "
            f"INTERVAL_JAM dan bekukan keputusannya di ADR lebih dulu "
            f"(ADR-018). Interval yang dikenal: {sorted(INTERVAL_JAM)}"
        )
    return JAM_SEHARI // INTERVAL_JAM[interval]


def nama_keluaran(dasar: str, interval: str) -> list[str]:
    """Nama berkas keluaran untuk sebuah interval; yang kanonik selalu pertama.

    Berkas bernama lama ditulis **hanya** untuk 1h, karena hanya 1h yang punya
    pembaca: ``backtest.yml`` meneruskan ``reports/universe_layak_v2.json`` dan
    ``reports/akhir_sejati.json``. Dengan begitu run 4h secara konstruksi tidak
    dapat menimpa masukan backtest 1h.
    """
    batang, _, ekstensi = dasar.rpartition(".")
    nama = [f"{batang}_{interval}.{ekstensi}"]
    if interval == INTERVAL_LEGASI:
        nama.append(dasar)
    return nama


def tulis_keluaran(out: Path, dasar: str, interval: str, teks: str) -> list[str]:
    """Menulis satu keluaran ke seluruh nama yang berlaku bagi interval itu."""
    ditulis = []
    for nama in nama_keluaran(dasar, interval):
        (out / nama).write_text(teks, encoding="utf-8")
        ditulis.append(nama)
        print(f"  ditulis: {nama}", flush=True)
    return ditulis


def rasio_datar(df: pd.DataFrame) -> float:
    n = len(df)
    if n == 0:
        return 0.0
    o = df["open"].to_numpy(dtype="float64")
    h = df["high"].to_numpy(dtype="float64")
    l = df["low"].to_numpy(dtype="float64")
    c = df["close"].to_numpy(dtype="float64")
    return float((((o == h) & (h == l)) & (l == c)).mean())


def ekor_datar(df: pd.DataFrame, min_panjang: int = MIN_PANJANG) -> int:
    """Panjang ekor datar berharga tunggal yang menempel di bar terakhir.

    Nol bila tidak ada, bila ekornya lebih pendek dari ambang, atau bila harga
    di dalamnya lebih dari satu nilai. Syarat harga tunggal itu yang memisahkan
    padding dari pasar yang benar-benar sekarat tetapi masih bergerak.
    """
    n = len(df)
    if n == 0:
        return 0
    for b in blok_datar(df, min_panjang=min_panjang):
        if b["indeks_akhir"] == n - 1 and b["harga_unik"] == 1:
            return int(b["panjang"])
    return 0


def potong(df: pd.DataFrame, min_panjang: int = MIN_PANJANG) -> pd.DataFrame:
    """Bingkai tanpa ekor datarnya. Dikembalikan apa adanya bila tidak ada ekor."""
    p = ekor_datar(df, min_panjang)
    if p == 0:
        return df
    return df.iloc[: len(df) - p]


def evaluasi(
    symbol: str,
    df: pd.DataFrame,
    min_panjang: int,
    min_bar: int,
    maks_rasio: float = MAKS_RASIO_DATAR,
) -> dict:
    """Putusan kelayakan satu simbol sesudah ekornya dipangkas.

    ``min_panjang`` dan ``min_bar`` wajib dipasok. Keduanya bergantung interval,
    dan nilai bawaan untuk besaran yang bergantung interval sudah sekali hampir
    menyusutkan semesta 4h tanpa keputusan siapa pun.

    Urutan pemeriksaannya disengaja: blok tengah diperiksa sebelum panjang
    riwayat, supaya simbol yang punya lubang di tengah dilaporkan karena
    lubangnya, bukan karena akibat lubang itu.
    """
    bar_awal = len(df)
    dipangkas = ekor_datar(df, min_panjang)
    sisa = potong(df, min_panjang)
    n = len(sisa)
    tersisa = blok_datar(sisa, min_panjang=min_panjang)
    rasio = rasio_datar(sisa)

    if n == 0:
        alasan = "tidak ada bar tersisa setelah ekor dipangkas"
    elif tersisa:
        alasan = (
            f"blok datar {tersisa[0]['panjang']} bar di tengah riwayat, "
            "tidak dapat dipangkas tanpa menyambung dua periode terpisah"
        )
    elif n < min_bar:
        alasan = f"riwayat tersisa {n} bar, di bawah {min_bar}"
    elif rasio > maks_rasio:
        alasan = f"rasio bar datar {rasio:.4f} di atas {maks_rasio}"
    else:
        alasan = ""

    return {
        "symbol": symbol,
        "bar_awal": int(bar_awal),
        "bar_sisa": int(n),
        "dipangkas": int(dipangkas),
        "rasio_datar_sisa": rasio,
        "akhir_ms": int(sisa["open_time"].iloc[-1]) if n else None,
        "layak": alasan == "",
        "alasan": alasan,
    }


def muat_semua(direktori: Path, interval: str) -> dict[str, pd.DataFrame]:
    berkas = pilih_berkas(Path(direktori), interval)
    if not berkas:
        raise SystemExit(f"tidak ada ohlcv_{interval}_*.parquet sah di {direktori}")
    bagian = []
    for p in berkas:
        df = pd.read_parquet(p, columns=KOLOM_BACA)
        df["symbol"] = df["symbol"].astype(str)
        bagian.append(df)
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
    ap.add_argument("--universe", default=None)
    ap.add_argument("--config", default="config/lux.yaml")
    ap.add_argument("--out", default="reports")
    ap.add_argument("--min-panjang", type=int, default=None)
    ap.add_argument("--min-bar", type=int, default=None)
    ap.add_argument("--maks-rasio", type=float, default=MAKS_RASIO_DATAR)
    a = ap.parse_args(argv)

    interval = a.interval
    min_panjang = a.min_panjang if a.min_panjang is not None else min_panjang_untuk(interval)
    # Lantai riwayat punya satu sumber kebenaran: config. muat_ambang gagal keras
    # bila interval ini belum punya kuncinya (ADR-017).
    min_bar = (
        a.min_bar
        if a.min_bar is not None
        else muat_ambang(Path(a.config), interval).min_bar
    )
    universe = a.universe or f"reports/universe_layak_{interval}.json"

    print(
        f"interval {interval} · min_panjang {min_panjang} bar (= {JAM_SEHARI} jam) · "
        f"min_bar {min_bar} · maks_rasio {a.maks_rasio}",
        flush=True,
    )
    print(f"universe masukan: {universe}", flush=True)

    kandidat = set(json.loads(Path(universe).read_text(encoding="utf-8"))["simbol"])
    print(f"kandidat layak lama: {len(kandidat)}", flush=True)

    bingkai = muat_semua(Path(a.dir), interval)
    print(f"{len(bingkai)} simbol dimuat dari aset", flush=True)

    # Tanggal kematian sejati dihitung atas SELURUH simbol, bukan hanya
    # kandidat, karena gerbang survivorship menilai porsi delisted terhadap
    # populasi penuh. Menghitungnya hanya atas yang layak akan mengulang persis
    # kesalahan yang membuat gerbang itu tidak bisa gagal.
    akhir: dict[str, dict] = {}
    hasil: list[dict] = []
    for s in sorted(bingkai):
        e = evaluasi(s, bingkai[s], min_panjang, min_bar, a.maks_rasio)
        akhir[s] = {
            "akhir_ms": e["akhir_ms"],
            "dipangkas": e["dipangkas"],
            "bar_awal": e["bar_awal"],
        }
        if s in kandidat:
            hasil.append(e)

    layak = [e["symbol"] for e in hasil if e["layak"]]
    ditolak = [e for e in hasil if not e["layak"]]
    dipangkas = [e for e in hasil if e["dipangkas"] > 0]
    total_dipangkas = sum(v["dipangkas"] for v in akhir.values())
    simbol_dipangkas_semua = sum(1 for v in akhir.values() if v["dipangkas"] > 0)

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    tulis_keluaran(
        out,
        "akhir_sejati.json",
        interval,
        json.dumps(
            {
                "interval": interval,
                "min_panjang": min_panjang,
                "simbol": len(akhir),
                "simbol_dipangkas": simbol_dipangkas_semua,
                "bar_dipangkas": int(total_dipangkas),
                "akhir": akhir,
            },
            indent=2,
            ensure_ascii=False,
        ),
    )
    tulis_keluaran(
        out,
        "universe_layak_v2.json",
        interval,
        json.dumps(
            {
                "sumber": "ADR-003, setelah ekor datar dipangkas",
                "interval": interval,
                "min_panjang": min_panjang,
                "min_bar": min_bar,
                "maks_rasio_datar": a.maks_rasio,
                "jumlah": len(layak),
                "simbol": layak,
            },
            indent=2,
            ensure_ascii=False,
        ),
    )
    tulis_keluaran(
        out,
        "potong_ekor.json",
        interval,
        json.dumps({"interval": interval, "hasil": hasil}, indent=2, ensure_ascii=False),
    )

    md = [
        f"# Pemangkasan ekor datar {interval}",
        "",
        "Pelaksanaan ADR-003. Aset tidak ditulis ulang; pemangkasan berlaku saat "
        "muat, dan tabel ini adalah catatan yang dapat diaudit atasnya.",
        "",
        f"- Ambang ekor: **{min_panjang} bar** (= {JAM_SEHARI} jam) · "
        f"lantai riwayat: **{min_bar:,} bar** · maks rasio datar: **{a.maks_rasio}**",
        "",
        f"- Simbol dipindai (seluruh aset): **{len(akhir):,}**",
        f"- Simbol yang punya ekor datar: **{simbol_dipangkas_semua:,}**",
        f"- Total bar dipangkas: **{int(total_dipangkas):,}**",
        "",
        f"- Kandidat layak lama: **{len(kandidat):,}**",
        f"- Layak setelah ADR-003: **{len(layak):,}**",
        f"- Ditolak: **{len(ditolak):,}**",
        f"- Di antara kandidat, yang ekornya dipangkas: **{len(dipangkas):,}**",
        "",
        "## Tiga puluh pemangkasan terbesar",
        "",
        "| Simbol | Bar awal | Dipangkas | Bar sisa | Akhir sejati | Rasio sisa | "
        "Layak | Alasan |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for e in sorted(hasil, key=lambda r: -r["dipangkas"])[:30]:
        md.append(
            f"| {e['symbol']} | {e['bar_awal']:,} | {e['dipangkas']:,} | "
            f"{e['bar_sisa']:,} | "
            f"{tanggal(e['akhir_ms']) if e['akhir_ms'] else '-'} | "
            f"{e['rasio_datar_sisa']:.4f} | {'ya' if e['layak'] else 'tidak'} | "
            f"{e['alasan'] or '-'} |"
        )

    sebab: dict[str, int] = {}
    for e in ditolak:
        kunci = e["alasan"].split(",")[0].split(" di ")[0]
        kunci = " ".join(kunci.split()[:4])
        sebab[kunci] = sebab.get(kunci, 0) + 1
    md += ["", "## Sebab penolakan", "", "| Sebab | Jumlah |", "|---|---|"]
    for k, v in sorted(sebab.items(), key=lambda kv: -kv[1]):
        md.append(f"| {k} | {v} |")
    md += [""]

    tulis_keluaran(out, "potong_ekor.md", interval, "\n".join(md) + "\n")
    print("\n".join(md), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
