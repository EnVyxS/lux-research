"""Menggabungkan laporan per shard menjadi satu laporan ingest.

Dijalankan sebagai job terpisah setelah semua shard selesai. Alasannya bukan
kerapian: delapan job yang meng-commit ke branch yang sama secara bersamaan
akan saling menimpa. Satu job agregasi menghapus balapan itu sepenuhnya.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    sumber = Path(sys.argv[1] if len(sys.argv) > 1 else "shards")
    Path("reports").mkdir(exist_ok=True)

    ringkasan_shard = [
        json.loads(p.read_text()) for p in sorted(sumber.rglob("ringkasan_shard*.json"))
    ]
    if not ringkasan_shard:
        print("tidak ada ringkasan shard ditemukan")
        return 1

    total: dict[str, dict] = {}
    for r in ringkasan_shard:
        for interval, d in r["interval"].items():
            t = total.setdefault(
                interval,
                {
                    "baris": 0,
                    "simbol_berhasil": 0,
                    "simbol_gagal": 0,
                    "total_bar_hilang": 0,
                    "total_duplikat": 0,
                    "total_celah_kisi": 0,
                    "simbol_bermasalah": 0,
                    "bytes": 0,
                    "detik_maks": 0,
                },
            )
            for k in (
                "baris",
                "simbol_berhasil",
                "simbol_gagal",
                "total_bar_hilang",
                "total_duplikat",
                "total_celah_kisi",
                "simbol_bermasalah",
                "bytes",
            ):
                t[k] += d.get(k, 0)
            t["detik_maks"] = max(t["detik_maks"], d.get("detik", 0))

    # Gerbang mutu tahap ingest. Gagal berarti pipeline berhenti, bukan
    # dilanjutkan dengan catatan kecil di bawah tabel.
    gerbang = {}
    for interval, t in total.items():
        gerbang[interval] = {
            "tidak_ada_duplikat": t["total_duplikat"] == 0,
            "tidak_ada_simbol_gagal": t["simbol_gagal"] == 0,
            "ada_baris": t["baris"] > 0,
        }

    hasil = {
        "waktu_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "jumlah_shard": len(ringkasan_shard),
        "total": total,
        "gerbang": gerbang,
        "semua_gerbang_lulus": all(all(g.values()) for g in gerbang.values()),
        "per_shard": ringkasan_shard,
    }

    Path("reports/ingest_tier_b.json").write_text(
        json.dumps(hasil, indent=2, ensure_ascii=False, default=str)
    )

    baris = ["# Laporan ingest Tier B", "", f"Digabung dari {len(ringkasan_shard)} shard.", ""]
    baris += ["| Interval | Baris | Simbol OK | Simbol gagal | Bar hilang | Celah kisi | Ukuran |", "|---|---|---|---|---|---|---|"]
    for interval, t in sorted(total.items()):
        baris.append(
            f"| {interval} | {t['baris']:,} | {t['simbol_berhasil']} | "
            f"{t['simbol_gagal']} | {t['total_bar_hilang']:,} | "
            f"{t['total_celah_kisi']:,} | {t['bytes'] / 1048576:.1f} MB |"
        )
    baris += ["", f"Semua gerbang lulus: **{hasil['semua_gerbang_lulus']}**", ""]
    Path("reports/ingest_tier_b.md").write_text(chr(10).join(baris))

    print(json.dumps({k: v for k, v in hasil.items() if k != "per_shard"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
