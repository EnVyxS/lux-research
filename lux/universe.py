"""Membangun universe point-in-time dari arsip.

Mengapa bukan dari ``exchangeInfo``: endpoint itu hanya memuat simbol yang
aktif HARI INI. Membangun universe darinya menanamkan survivorship bias di
baris pertama pipeline, yaitu cacat yang merusak dataset upaya sebelumnya
(528 simbol, padahal arsip memuat 937). Arsip memuat simbol yang sudah
delisted, jadi arsip adalah satu-satunya sumber yang sah. Endpoint REST juga
mengembalikan HTTP 451 dari runner GitHub.

Definisi keanggotaan: sebuah simbol dianggap dapat diperdagangkan pada bulan M
bila arsip memuat berkas kline untuk simbol itu pada bulan M. Definisi ini
diturunkan dari data, bukan diasumsikan.

Tidak semua yang ada di arsip layak masuk universe riset. Arsip mencampur tiga
jenis kontrak yang perilakunya berbeda secara fundamental:

  perp     kontrak perpetual, tanpa tanggal kedaluwarsa, memakai funding rate
  delivery kontrak berjangka bertanggal seperti BTCUSDT_240329, kedaluwarsa
           dan TIDAK memakai funding, sehingga model biaya perpetual salah
           bila diterapkan padanya
  settled  varian bertanda SETTLED, sisa penyelesaian khusus, riwayatnya
           terpotong dan tidak mewakili perdagangan normal

Mencampur ketiganya akan mencemari backtest dengan instrumen yang model
biayanya tidak berlaku. Klasifikasi dilakukan di sini, sekali, dan hasilnya
ikut tersimpan di parquet.

Keluaran:
  reference/universe_pit.parquet      satu baris per (symbol, month)
  reference/universe_symbols.parquet  satu baris per symbol
  reports/universe.json               ringkasan mesin, termasuk hasil gerbang
"""

from __future__ import annotations

import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from lux import binance_vision as bv

INTERVAL = "1h"
WORKERS = 8

# Gerbang. Snapshot exchangeInfo 2026-07-21 memuat 841 simbol aktif. Universe
# historis WAJIB melebihi angka itu; bila tidak, enumerasinya sendiri cacat.
GERBANG_MIN_SIMBOL = 841

QUOTES = ("USDT", "USDC", "BUSD", "USD")
RE_DELIVERY = re.compile(r"_\d{6}$")

# Majors dipakai untuk memeriksa apakah arsip HARIAN memuat periode yang tidak
# tercakup arsip BULANAN. Binance USD-M futures diluncurkan September 2019,
# sementara arsip bulanan tampak mulai Januari 2020.
MAJORS = ("BTCUSDT", "ETHUSDT", "BCHUSDT", "XRPUSDT")


def jenis_kontrak(symbol: str) -> str:
    if symbol.endswith("SETTLED"):
        return "settled"
    if RE_DELIVERY.search(symbol):
        return "delivery"
    return "perp"


def quote_asset(symbol: str) -> str:
    dasar = RE_DELIVERY.sub("", symbol)
    if dasar.endswith("SETTLED"):
        dasar = dasar[: -len("SETTLED")]
    for q in QUOTES:
        if dasar.endswith(q):
            return q
    return "LAIN"


def bulan_sekarang() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


def _bulan_lalu(bulan: str) -> str:
    return str(pd.Period(bulan, freq="M") - 1)


def kumpulkan() -> dict[str, list[str]]:
    simbol = bv.list_symbols()
    print(f"simbol ditemukan di arsip: {len(simbol)}")

    def ambil(s: str) -> tuple[str, list[str]]:
        try:
            return s, bv.list_months(s, INTERVAL)
        except Exception as exc:  # noqa: BLE001
            print(f"PERINGATAN gagal melisting {s}: {exc}")
            return s, []

    hasil: dict[str, list[str]] = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for i, (s, bulan) in enumerate(pool.map(ambil, simbol), 1):
            hasil[s] = bulan
            if i % 100 == 0:
                print(f"  {i}/{len(simbol)}")
    return hasil


def periksa_arsip_harian() -> dict:
    """Apakah arsip harian memuat periode sebelum arsip bulanan dimulai?

    Bila ya, ingest yang hanya membaca arsip bulanan akan diam-diam kehilangan
    bulan-bulan pertama sejarah futures Binance. Kehilangan diam-diam seperti
    itu persis jenis cacat yang harus tertangkap sebelum backtest, bukan
    sesudah angkanya terlihat meyakinkan.
    """
    hasil = {}
    for sym in MAJORS:
        try:
            prefix = f"{bv.ROOT}/daily/klines/{sym}/{INTERVAL}/"
            tanggal = sorted(
                k.rsplit("/", 1)[-1][:-4].split("-", 2)[-1]
                for k in bv.list_keys(prefix)
                if k.endswith(".zip")
            )
            bulanan = bv.list_months(sym, INTERVAL)
            hasil[sym] = {
                "harian_pertama": tanggal[0] if tanggal else None,
                "harian_terakhir": tanggal[-1] if tanggal else None,
                "jumlah_hari": len(tanggal),
                "bulanan_pertama": bulanan[0] if bulanan else None,
                "harian_lebih_awal": bool(
                    tanggal and bulanan and tanggal[0][:7] < bulanan[0]
                ),
            }
        except Exception as exc:  # noqa: BLE001
            hasil[sym] = {"error": f"{type(exc).__name__}: {exc}"}
    return hasil


def main() -> int:
    Path("reference").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)

    peta = kumpulkan()
    sekarang = bulan_sekarang()
    ambang_aktif = _bulan_lalu(sekarang)

    baris_pit = []
    baris_sym = []
    tanpa_data = []

    for sym, bulan in sorted(peta.items()):
        if not bulan:
            tanpa_data.append(sym)
            continue
        jenis = jenis_kontrak(sym)
        for b in bulan:
            baris_pit.append(
                {"symbol": sym, "month": b, "interval": INTERVAL, "contract_type": jenis}
            )
        rentang = pd.period_range(bulan[0], bulan[-1], freq="M")
        baris_sym.append(
            {
                "symbol": sym,
                "quote": quote_asset(sym),
                "contract_type": jenis,
                "first_month": bulan[0],
                "last_month": bulan[-1],
                "n_months": len(bulan),
                "n_months_rentang": len(rentang),
                "bulan_hilang": len(rentang) - len(bulan),
                "masih_aktif": bulan[-1] >= ambang_aktif,
            }
        )

    pit = pd.DataFrame(baris_pit)
    sym_df = pd.DataFrame(baris_sym)

    pit.to_parquet("reference/universe_pit.parquet", index=False, compression="zstd")
    sym_df.to_parquet(
        "reference/universe_symbols.parquet", index=False, compression="zstd"
    )

    perp = sym_df[sym_df["contract_type"] == "perp"]
    perp_usdt = perp[perp["quote"] == "USDT"]
    berlubang = sym_df[sym_df["bulan_hilang"] > 0]
    lain = sym_df[sym_df["quote"] == "LAIN"]

    ringkasan = {
        "waktu_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "interval": INTERVAL,
        "total_simbol": len(sym_df),
        "total_baris_pit": len(pit),
        "bulan_paling_awal": pit["month"].min() if len(pit) else None,
        "bulan_paling_akhir": pit["month"].max() if len(pit) else None,
        "per_jenis_kontrak": sym_df["contract_type"].value_counts().to_dict(),
        "per_quote": sym_df["quote"].value_counts().to_dict(),
        "perp": {
            "total": len(perp),
            "usdt": len(perp_usdt),
            "masih_aktif": int(perp["masih_aktif"].sum()),
            "delisted": int((~perp["masih_aktif"]).sum()),
            "usdt_masih_aktif": int(perp_usdt["masih_aktif"].sum()),
            "usdt_delisted": int((~perp_usdt["masih_aktif"]).sum()),
        },
        "contoh_quote_lain": lain["symbol"].head(20).tolist(),
        "simbol_tanpa_data_1h": len(tanpa_data),
        "simbol_dengan_lubang_arsip": len(berlubang),
        "total_bulan_hilang": int(sym_df["bulan_hilang"].sum()),
        "contoh_lubang": berlubang.nlargest(10, "bulan_hilang")[
            ["symbol", "contract_type", "first_month", "last_month", "bulan_hilang"]
        ].to_dict("records"),
        "arsip_harian": periksa_arsip_harian(),
        "gerbang_min_simbol": GERBANG_MIN_SIMBOL,
        "gerbang_lulus": bool(len(sym_df) > GERBANG_MIN_SIMBOL),
    }

    Path("reports/universe.json").write_text(
        json.dumps(ringkasan, indent=2, ensure_ascii=False, default=str)
    )
    print(json.dumps(ringkasan, indent=2, ensure_ascii=False, default=str)[:6000])

    if not ringkasan["gerbang_lulus"]:
        print("GERBANG GAGAL: jumlah simbol historis tidak melebihi snapshot aktif.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
