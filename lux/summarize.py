"""Menggabungkan laporan per shard menjadi satu laporan.

Dijalankan sebagai job terpisah setelah semua shard selesai. Alasannya bukan
kerapian: delapan job yang meng-commit ke branch yang sama secara bersamaan
akan saling menimpa. Satu job agregasi menghapus balapan itu sepenuhnya.

Versi pertama hanya melaporkan JUMLAH simbol yang gagal. Itu cacat: angka
"3 simbol gagal" tidak bisa didiagnosis maupun diperbaiki karena nama dan
alasannya hanya ada di artifact yang kedaluwarsa dalam tujuh hari. Versi ini
mengangkat nama simbol dan pesan galatnya ke dalam laporan yang di-commit.

Pemakaian: python -m lux.summarize <direktori_shard> [nama_keluaran]
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def kumpulkan_kegagalan(sumber: Path) -> list[dict]:
    """Mengangkat entri gagal dari berkas detail per simbol."""
    kegagalan: list[dict] = []
    for p in sorted(sumber.rglob("detail_*.json")):
        try:
            data = json.loads(p.read_text())
        except Exception:  # noqa: BLE001
            continue
        if not isinstance(data, list):
            continue
        for c in data:
            if isinstance(c, dict) and c.get("error"):
                kegagalan.append(
                    {
                        "symbol": c.get("symbol"),
                        "interval": c.get("interval"),
                        "error": str(c.get("error"))[:300],
                        "contoh_gagal": c.get("contoh_gagal"),
                        "sumber": p.name,
                    }
                )
    return kegagalan


def main() -> int:
    sumber = Path(sys.argv[1] if len(sys.argv) > 1 else "shards")
    nama = sys.argv[2] if len(sys.argv) > 2 else "ingest_tier_b"
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
            t = total.setdefault(interval, {})
            for k, v in d.items():
                if isinstance(v, (int, float)) and k != "detik":
                    t[k] = t.get(k, 0) + v
            t["detik_maks"] = max(t.get("detik_maks", 0), d.get("detik", 0))

    kegagalan = kumpulkan_kegagalan(sumber)

    # Gerbang mutu. Gagal berarti pipeline berhenti, bukan dilanjutkan dengan
    # catatan kecil di bawah tabel.
    gerbang = {
        interval: {
            "tidak_ada_duplikat": t.get("total_duplikat", 0) == 0,
            "tidak_ada_simbol_gagal": t.get("simbol_gagal", 0) == 0,
            "ada_baris": t.get("baris", 0) > 0,
        }
        for interval, t in total.items()
    }

    hasil = {
        "waktu_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "jumlah_shard": len(ringkasan_shard),
        "total": total,
        "gerbang": gerbang,
        "semua_gerbang_lulus": all(all(g.values()) for g in gerbang.values()),
        "jumlah_kegagalan": len(kegagalan),
        "kegagalan": kegagalan,
        "per_shard": ringkasan_shard,
    }

    Path(f"reports/{nama}.json").write_text(
        json.dumps(hasil, indent=2, ensure_ascii=False, default=str)
    )

    baris = [f"# Laporan {nama}", "", f"Digabung dari {len(ringkasan_shard)} shard.", ""]
    baris.append("| Interval | Baris | Simbol OK | Gagal | Duplikat | Celah kisi | Ukuran |")
    baris.append("|---|---|---|---|---|---|---|")
    for interval, t in sorted(total.items()):
        baris.append(
            f"| {interval} | {t.get('baris', 0):,} | {t.get('simbol_berhasil', 0)} | "
            f"{t.get('simbol_gagal', 0)} | {t.get('total_duplikat', 0):,} | "
            f"{t.get('total_celah_kisi', 0):,} | {t.get('bytes', 0) / 1048576:.1f} MB |"
        )

    if kegagalan:
        baris += ["", "## Simbol gagal", "", "| Simbol | Interval | Galat |", "|---|---|---|"]
        for k in kegagalan:
            pesan = str(k["error"]).replace("|", "/")[:160]
            baris.append(f"| {k['symbol']} | {k['interval']} | {pesan} |")

    baris += ["", f"Semua gerbang lulus: **{hasil['semua_gerbang_lulus']}**", ""]
    Path(f"reports/{nama}.md").write_text(chr(10).join(baris))

    print(
        json.dumps(
            {k: v for k, v in hasil.items() if k != "per_shard"},
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
