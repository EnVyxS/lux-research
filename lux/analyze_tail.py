"""Menelusuri dua anomali pada backfill ekor harian.

Anomali 1 — rasio interval. Ingest bulanan menghasilkan rasio baris 1h:4h
sebesar 4,014 dan tambalan simbol non-ASCII 4,016. Keduanya wajar, karena satu
hari berisi 24 bar 1h dan 6 bar 4h. Backfill ekor justru menghasilkan 4,60.
Selisih 13% itu berarti ada bar 4h yang tidak terbentuk, dan penyebabnya harus
diketahui sebelum data dipakai.

Anomali 2 — jumlah celah kisi. Backfill hanya mengambil ekor sepanjang sekitar
24 hari yang seharusnya bersambung, tapi melaporkan 17.462 celah untuk 787
simbol, yakni sekitar 22 celah per simbol. Angka yang hampir sama dengan jumlah
batas antar-berkas harian itu mencurigakan, dan celahnya identik pada 1h maupun
4h.

Modul ini tidak mengunduh data lagi. Ia membaca berkas detail per simbol yang
sudah dihasilkan backfill, sehingga diagnosisnya berbiaya hitungan detik.
Menebak penyebabnya tanpa memeriksa data justru pemborosan yang lebih mahal.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

# Bar yang seharusnya terbentuk dari satu hari penuh.
BAR_PER_HARI = {"1m": 1440, "5m": 288, "15m": 96, "1h": 24, "4h": 6}


def main() -> int:
    sumber = Path(sys.argv[1] if len(sys.argv) > 1 else "shards")
    Path("reports").mkdir(exist_ok=True)

    per_interval: dict[str, list[dict]] = {}
    for p in sorted(sumber.rglob("detail_tail_*.json")):
        try:
            data = json.loads(p.read_text())
        except Exception:  # noqa: BLE001
            continue
        for c in data:
            if isinstance(c, dict) and c.get("interval"):
                per_interval.setdefault(c["interval"], []).append(c)

    if not per_interval:
        print("tidak ada detail_tail ditemukan")
        return 1

    hasil: dict[str, dict] = {}

    for interval, catatan in sorted(per_interval.items()):
        diharapkan = BAR_PER_HARI.get(interval)
        aktif = [c for c in catatan if c.get("hari_perlu", 0) > 0 and not c.get("error")]

        # Apakah setiap simbol menghasilkan tepat jumlah bar yang seharusnya?
        cocok, kurang, lebih = [], [], []
        for c in aktif:
            target = c["hari_perlu"] * diharapkan
            baris = c.get("baris", 0)
            if baris == target:
                cocok.append(c["symbol"])
            elif baris < target:
                kurang.append(
                    {
                        "symbol": c["symbol"],
                        "hari_perlu": c["hari_perlu"],
                        "baris": baris,
                        "target": target,
                        "kekurangan": target - baris,
                        "celah_kisi": c.get("celah_kisi"),
                    }
                )
            else:
                lebih.append(
                    {
                        "symbol": c["symbol"],
                        "hari_perlu": c["hari_perlu"],
                        "baris": baris,
                        "target": target,
                        "kelebihan": baris - target,
                    }
                )

        # Sebaran jumlah hari yang perlu ditambal. Bila 1h dan 4h punya sebaran
        # berbeda, berarti ketersediaan arsip harian memang berbeda per interval
        # dan itu menjelaskan anomali rasio tanpa perlu menuduh parser.
        sebaran_hari = Counter(c["hari_perlu"] for c in aktif)

        # Apakah celah kisi sebanding dengan jumlah hari, atau dengan jumlah
        # batas antar-berkas? Korelasi kasar cukup untuk membedakannya.
        celah_vs_hari = [
            {
                "symbol": c["symbol"],
                "hari_perlu": c["hari_perlu"],
                "celah_kisi": c.get("celah_kisi", 0),
                "baris": c.get("baris", 0),
            }
            for c in sorted(aktif, key=lambda x: -x.get("celah_kisi", 0))[:25]
        ]

        total_hari = sum(c["hari_perlu"] for c in aktif)
        total_baris = sum(c.get("baris", 0) for c in aktif)
        total_celah = sum(c.get("celah_kisi", 0) for c in aktif)

        hasil[interval] = {
            "simbol_aktif": len(aktif),
            "bar_per_hari_diharapkan": diharapkan,
            "total_hari_ditambal": total_hari,
            "total_baris": total_baris,
            "baris_diharapkan": total_hari * diharapkan,
            "rasio_terisi": round(total_baris / (total_hari * diharapkan), 4)
            if total_hari
            else None,
            "simbol_tepat": len(cocok),
            "simbol_kurang": len(kurang),
            "simbol_lebih": len(lebih),
            "total_celah": total_celah,
            "celah_per_simbol": round(total_celah / len(aktif), 2) if aktif else None,
            "celah_per_hari": round(total_celah / total_hari, 4) if total_hari else None,
            "sebaran_hari_perlu": dict(sorted(sebaran_hari.items())),
            "contoh_kurang": sorted(kurang, key=lambda x: -x["kekurangan"])[:15],
            "contoh_lebih": lebih[:10],
            "celah_terbanyak": celah_vs_hari,
        }

    # Perbandingan langsung antar interval. Bila jumlah hari yang ditambal sama
    # tapi rasio terisinya berbeda, cacatnya ada pada pembacaan berkas 4h.
    # Bila jumlah harinya sendiri berbeda, arsipnya memang tidak simetris.
    if "1h" in hasil and "4h" in hasil:
        h1, h4 = hasil["1h"], hasil["4h"]
        hasil["perbandingan"] = {
            "hari_sama": h1["total_hari_ditambal"] == h4["total_hari_ditambal"],
            "hari_1h": h1["total_hari_ditambal"],
            "hari_4h": h4["total_hari_ditambal"],
            "rasio_baris_1h_per_4h": round(h1["total_baris"] / h4["total_baris"], 4)
            if h4["total_baris"]
            else None,
            "rasio_seharusnya": 4.0,
            "diagnosis": (
                "arsip harian tidak simetris antar interval"
                if h1["total_hari_ditambal"] != h4["total_hari_ditambal"]
                else "jumlah hari sama, selisih ada pada isi berkas"
            ),
        }

    Path("reports/tail_anomali.json").write_text(
        json.dumps(hasil, indent=2, ensure_ascii=False, default=str)
    )

    baris_md = ["# Anomali backfill ekor", ""]
    baris_md.append("| Interval | Simbol | Hari | Baris | Diharapkan | Terisi | Celah/simbol |")
    baris_md.append("|---|---|---|---|---|---|---|")
    for interval in sorted(k for k in hasil if k != "perbandingan"):
        d = hasil[interval]
        baris_md.append(
            f"| {interval} | {d['simbol_aktif']} | {d['total_hari_ditambal']:,} | "
            f"{d['total_baris']:,} | {d['baris_diharapkan']:,} | "
            f"{d['rasio_terisi']} | {d['celah_per_simbol']} |"
        )
    if "perbandingan" in hasil:
        p = hasil["perbandingan"]
        baris_md += [
            "",
            "## Perbandingan interval",
            "",
            f"- Hari ditambal 1h: {p['hari_1h']:,}, 4h: {p['hari_4h']:,}",
            f"- Rasio baris 1h:4h = {p['rasio_baris_1h_per_4h']} (seharusnya 4,0)",
            f"- Diagnosis: **{p['diagnosis']}**",
        ]
    Path("reports/tail_anomali.md").write_text(chr(10).join(baris_md) + "\n")

    print(json.dumps({k: v for k, v in hasil.items()}, indent=2, ensure_ascii=False)[:4000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
