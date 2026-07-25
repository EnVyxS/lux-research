"""Membangun universe point-in-time dari arsip.

Mengapa bukan dari ``exchangeInfo``: endpoint itu hanya memuat simbol yang
aktif HARI INI. Membangun universe darinya menanamkan survivorship bias di
baris pertama pipeline, yaitu cacat yang merusak dataset upaya sebelumnya
(528 simbol, padahal arsip memuat jauh lebih banyak). Arsip memuat simbol yang
sudah delisted, jadi arsip adalah satu-satunya sumber yang sah.

Definisi keanggotaan yang dipakai: sebuah simbol dianggap dapat diperdagangkan
pada bulan M bila arsip memuat berkas kline untuk simbol itu pada bulan M.
Definisi ini diturunkan dari data, bukan diasumsikan.

Keluaran:
  reference/universe_pit.parquet      satu baris per (symbol, month)
  reference/universe_symbols.parquet  satu baris per symbol
  reports/universe.json               ringkasan mesin, termasuk hasil gerbang
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from lux import binance_vision as bv

INTERVAL = "1h"
WORKERS = 8

# Gerbang. Snapshot exchangeInfo 2026-07-21 memuat 841 simbol aktif. Universe
# historis WAJIB melebihi angka itu; bila tidak, enumerasinya sendiri cacat dan
# pipeline harus berhenti alih-alih melanjutkan dengan data yang bias.
GERBANG_MIN_SIMBOL = 841

QUOTES = ("USDT", "USDC", "BUSD", "USD")


def quote_asset(symbol: str) -> str:
    for q in QUOTES:
        if symbol.endswith(q):
            return q
    return "LAIN"


def bulan_sekarang() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


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


def main() -> int:
    Path("reference").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)

    peta = kumpulkan()
    sekarang = bulan_sekarang()

    baris_pit = []
    baris_sym = []
    tanpa_data = []

    for sym, bulan in sorted(peta.items()):
        if not bulan:
            tanpa_data.append(sym)
            continue
        for b in bulan:
            baris_pit.append({"symbol": sym, "month": b, "interval": INTERVAL})
        # Rentang kalender penuh antara bulan pertama dan terakhir. Selisihnya
        # terhadap jumlah bulan yang benar-benar ada mengungkap lubang arsip.
        rentang = pd.period_range(bulan[0], bulan[-1], freq="M")
        baris_sym.append(
            {
                "symbol": sym,
                "quote": quote_asset(sym),
                "first_month": bulan[0],
                "last_month": bulan[-1],
                "n_months": len(bulan),
                "n_months_rentang": len(rentang),
                "bulan_hilang": len(rentang) - len(bulan),
                "masih_aktif": bulan[-1] >= sekarang[:7] or bulan[-1] >= _bulan_lalu(sekarang),
            }
        )

    pit = pd.DataFrame(baris_pit)
    sym_df = pd.DataFrame(baris_sym)

    pit.to_parquet("reference/universe_pit.parquet", index=False, compression="zstd")
    sym_df.to_parquet("reference/universe_symbols.parquet", index=False, compression="zstd")

    total = len(sym_df)
    aktif = int(sym_df["masih_aktif"].sum())
    delisted = total - aktif
    berlubang = sym_df[sym_df["bulan_hilang"] > 0]

    ringkasan = {
        "waktu_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "interval": INTERVAL,
        "total_simbol": total,
        "simbol_masih_aktif": aktif,
        "simbol_delisted": delisted,
        "simbol_tanpa_data_1h": len(tanpa_data),
        "contoh_tanpa_data": tanpa_data[:20],
        "total_baris_pit": len(pit),
        "bulan_paling_awal": pit["month"].min() if len(pit) else None,
        "bulan_paling_akhir": pit["month"].max() if len(pit) else None,
        "per_quote": sym_df["quote"].value_counts().to_dict(),
        "simbol_dengan_lubang_arsip": len(berlubang),
        "total_bulan_hilang": int(sym_df["bulan_hilang"].sum()),
        "contoh_lubang": berlubang.nlargest(10, "bulan_hilang")[
            ["symbol", "first_month", "last_month", "bulan_hilang"]
        ].to_dict("records"),
        "gerbang_min_simbol": GERBANG_MIN_SIMBOL,
        "gerbang_lulus": bool(total > GERBANG_MIN_SIMBOL),
    }

    Path("reports/universe.json").write_text(
        json.dumps(ringkasan, indent=2, ensure_ascii=False, default=str)
    )
    print(json.dumps(ringkasan, indent=2, ensure_ascii=False, default=str)[:4000])

    if not ringkasan["gerbang_lulus"]:
        print("GERBANG GAGAL: jumlah simbol historis tidak melebihi snapshot aktif.")
        return 1
    return 0


def _bulan_lalu(bulan: str) -> str:
    p = pd.Period(bulan, freq="M") - 1
    return str(p)


if __name__ == "__main__":
    raise SystemExit(main())
