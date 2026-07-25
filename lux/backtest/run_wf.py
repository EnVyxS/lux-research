"""Menjalankan hipotesis H-001 secara utuh: walk-forward, gerbang, putusan.

Dipanggil dari runner, bukan sandbox agen, karena asetnya ratusan megabita.

Urutan di sini disengaja dan tidak boleh dibalik. Hipotesis didaftarkan
**sebelum** data dimuat, sehingga kriteria kelulusan sudah terkunci di disk
saat angka pertama muncul. Uji permutasi dijalankan atas wilayah penilaian yang
sama persis dengan yang dilaporkan, bukan atas wilayah yang dihitung ulang.
Dan putusan akhir dibuat oleh pembanding yang tidak tahu apa-apa tentang berapa
hasilnya, hanya tentang ambang yang sudah tertulis.

Tiga gerbang tidak boleh dinilai atas kumpulan perdagangan yang sudah
dicampur antar simbol, dan ketiganya sempat salah dipasang di versi pertama
berkas ini:

- **Overlap** dinilai per simbol. Dua posisi pada dua simbol berbeda memang
  berjalan bersamaan, dan menilainya dari kumpulan campuran akan selalu
  melaporkan tumpang tindih yang sebenarnya sah.
- **Survivorship** dinilai terhadap universe layak yang penuh, bukan terhadap
  subset yang kebetulan diuji. Membandingkan subset dengan dirinya sendiri
  selalu menghasilkan rasio satu, yaitu gerbang yang tidak pernah bisa gagal.
- **Buy-and-hold** tidak boleh memakai kurva ekuitas jendela yang disambung,
  karena tiap jendela memulai ulang dari modal awal sehingga sambungannya
  hanya mencerminkan jendela terakhir.

Gerbang gabungan wajib menyebut **nama** simbol yang menjatuhkannya. Laporan
yang hanya berbunyi "4 dari 40 simbol gagal" memaksa pembacanya menebak, dan
angka gabungan yang ditampilkan bisa saja bukan dimensi yang menyebabkan
kegagalan: gerbang forward-fill menjatuhkan run pilot lewat panjang deret bar
datar, sementara yang tercetak justru rasionya, yang lolos ambang.

ADR-003 (ekor datar): Aset Parquet **tidak** ditulis ulang. Pemangkasan
diterapkan saat muat lewat ``_potong_ekor`` sehingga prinsip write-once tetap
terjaga. Tanggal kematian sejati simbol dibaca dari ``reports/akhir_sejati.json``
alih-alih dari stempel bar terakhir mentah — perbedaan ini krusial karena
pipa data mengisi harga terakhir simbol mati sampai ujung dataset, sehingga
stempel mentah tidak dapat membedakan simbol mati dari simbol hidup.

Pemakaian:
    python -m lux.backtest.run_wf --dir aset --interval 1h \\
        --universe reports/universe_layak_v2.json \\
        --akhir-sejati reports/akhir_sejati.json \\
        --limit 40
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

from lux.backtest.engine import Hasil, Konfig, Perdagangan, jalankan
from lux.backtest.gerbang import (
    Gerbang,
    gerbang_buy_and_hold,
    gerbang_checksum,
    gerbang_entri_acak,
    gerbang_forward_fill,
    gerbang_funding,
    gerbang_invarian_risiko,
    gerbang_lookahead,
    gerbang_overlap,
    gerbang_survivorship,
    susun_laporan,
)
from lux.backtest.walk_forward import jalankan_walk_forward
from lux.funding_model import ambil_jadwal, muat_jadwal
from lux.potong_ekor import potong as _potong_ekor
from lux.praregistrasi import Hipotesis, Kriteria, nilai, simpan
from lux.strategi import breakout_atr

POLA_DILARANG = ("_retry",)
HARI_MS = 86_400_000
JAM_MS = 3_600_000


# --------------------------------------------------------------------------
# Pemuatan
# --------------------------------------------------------------------------
def pilih_berkas(direktori: Path, interval: str) -> list[Path]:
    """Berkas yang sah dibaca. Aturannya sama dengan validasi, dan sengaja
    diulang di sini alih-alih diimpor, agar backtest tidak diam-diam ikut
    berubah bila aturan validasi disunting."""
    semua = sorted(Path(direktori).glob(f"ohlcv_{interval}_*.parquet"))
    return [p for p in semua if not any(t in p.name for t in POLA_DILARANG)]


def sha256_berkas(path: Path, blok: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for potongan in iter(lambda: f.read(blok), b""):
            h.update(potongan)
    return h.hexdigest()


def muat_ohlcv(
    direktori: Path, interval: str, simbol: set[str]
) -> tuple[dict[str, pd.DataFrame], list[Path]]:
    """Muat OHLCV per simbol dan pangkas ekor datar sesuai ADR-003.

    Pemangkasan diterapkan setelah sort, sebelum data masuk ke backtest.
    Aset Parquet tidak disentuh; prinsip write-once tetap terjaga.
    """
    berkas = pilih_berkas(direktori, interval)
    if not berkas:
        raise SystemExit(f"tidak ada ohlcv_{interval}_*.parquet sah di {direktori}")
    bagian = []
    for p in berkas:
        df = pd.read_parquet(p)
        df["symbol"] = df["symbol"].astype(str)
        bagian.append(df[df["symbol"].isin(simbol)])
        print(f"  dibaca {p.name}", flush=True)
    gabung = pd.concat(bagian, ignore_index=True)
    hasil = {}
    for s, b in gabung.groupby("symbol", sort=True, observed=True):
        sorted_b = b.sort_values("open_time").reset_index(drop=True)
        hasil[str(s)] = _potong_ekor(sorted_b)
    return hasil, berkas


def akhir_per_simbol(
    direktori: Path,
    interval: str,
    akhir_sejati_path: Path | None = None,
) -> dict[str, int]:
    """Stempel bar terakhir *sejati* tiap simbol di seluruh aset.

    Bila ``akhir_sejati_path`` ada dan filenya tersedia, stempel dibaca dari
    sana. File itu dihasilkan oleh ``lux.potong_ekor`` dan menyimpan tanggal
    kematian nyata simbol — bukan stempel bar terakhir mentah yang untuk simbol
    mati sama dengan tanggal ujung dataset (karena pipa data mengisi harga
    terakhir sampai ujung).

    Membaca dua kolom mentah sebagai fallback masih tersedia untuk pengujian
    unit, tapi pada produksi selalu harus ada ``akhir_sejati.json``.
    """
    if akhir_sejati_path is not None and Path(akhir_sejati_path).exists():
        data = json.loads(Path(akhir_sejati_path).read_text(encoding="utf-8"))
        akhir = {s: int(v["akhir_ms"]) for s, v in data["akhir"].items()}
        print(
            f"  akhir_per_simbol: {len(akhir)} simbol dari {akhir_sejati_path}",
            flush=True,
        )
        return akhir

    # Fallback: hitung dari parquet mentah. Hasilnya bisa menyesatkan untuk
    # simbol mati karena stempel terakhirnya identik dengan simbol hidup.
    print(
        "  peringatan: akhir_sejati.json tidak tersedia, memakai stempel parquet mentah",
        flush=True,
    )
    akhir: dict[str, int] = {}
    for p in pilih_berkas(Path(direktori), interval):
        df = pd.read_parquet(p, columns=["symbol", "open_time"])
        m = df.groupby("symbol", observed=True)["open_time"].max()
        for s, t in m.items():
            s = str(s)
            akhir[s] = max(akhir.get(s, 0), int(t))
    return akhir


def muat_konfig(path: Path) -> Konfig:
    """Gagal keras bila config tidak terbaca. Diam-diam memakai nilai bawaan
    membuat laporan tampak sah padahal aturannya bukan yang disepakati."""
    import yaml

    with Path(path).open(encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    b, r = cfg["biaya"], cfg["risiko"]
    return Konfig(
        fee=float(b["fee_efektif"]),
        slippage=float(b["slippage"]),
        atr_periode=int(r["atr_periode"]),
        atr_pengali_stop=float(r["atr_pengali_stop"]),
        risiko_per_trade=float(r["risiko_per_trade"]),
    )


# --------------------------------------------------------------------------
# Pembongkaran biaya
# --------------------------------------------------------------------------
def rincian_R(p: Perdagangan) -> dict:
    """Pecah satu perdagangan menjadi komponen-komponennya dalam satuan R.

    Kerugian yang melewati 1R hanya punya dua sumber yang mungkin: harga yang
    menembus stop, atau biaya. Mesin ini selalu mengisi stop tepat di harga
    stop, sehingga sumber pertama tertutup secara struktural dan sisanya wajib
    biaya. Pembongkaran ini ada supaya klaim tersebut dapat diperiksa langsung
    dari laporan, bukan disimpulkan dari penalaran tentang kode.

    ``stop_frac`` ikut dilaporkan karena biaya dalam satuan R berbanding
    terbalik dengannya: pada stop yang sangat rapat, fee dan slippage yang
    tampak kecil terhadap harga menjadi besar terhadap risiko.
    """
    risiko = p.jarak_stop * p.ukuran
    if risiko <= 0:
        return {
            "symbol": p.symbol,
            "R": 0.0,
            "kotor_R": 0.0,
            "transaksi_R": 0.0,
            "funding_R": 0.0,
            "stop_frac": 0.0,
            "jam": 0.0,
            "alasan": p.alasan_keluar,
        }
    return {
        "symbol": p.symbol,
        "R": p.laba / risiko,
        "kotor_R": p.laba_kotor / risiko,
        "transaksi_R": p.biaya_transaksi / risiko,
        "funding_R": p.biaya_funding / risiko,
        "stop_frac": p.jarak_stop / p.harga_masuk if p.harga_masuk > 0 else 0.0,
        "jam": (p.keluar_ms - p.masuk_ms) / JAM_MS,
        "alasan": p.alasan_keluar,
    }


def diagnosa_biaya(perdagangan: list[Perdagangan], n: int = 10) -> dict:
    """Ringkas beban biaya atas seluruh perdagangan, plus n terburuk.

    Rerata dikembalikan sebagai ``None`` bila tidak ada perdagangan. Nol akan
    terbaca sebagai "tidak ada biaya", padahal artinya "tidak ada yang diukur".
    """
    rincian = [rincian_R(p) for p in perdagangan]
    if not rincian:
        return {
            "jumlah": 0,
            "rerata_transaksi_R": None,
            "rerata_funding_R": None,
            "rerata_stop_frac": None,
            "trade_biaya_lebih_1R": 0,
            "terburuk": [],
        }
    return {
        "jumlah": len(rincian),
        "rerata_transaksi_R": float(np.mean([r["transaksi_R"] for r in rincian])),
        "rerata_funding_R": float(np.mean([r["funding_R"] for r in rincian])),
        "rerata_stop_frac": float(np.mean([r["stop_frac"] for r in rincian])),
        "trade_biaya_lebih_1R": int(
            sum(1 for r in rincian if r["transaksi_R"] + r["funding_R"] > 1.0)
        ),
        "terburuk": sorted(rincian, key=lambda r: r["R"])[:n],
    }


# --------------------------------------------------------------------------
# Definisi turunan
# --------------------------------------------------------------------------
def simbol_mati_dari_akhir(
    akhir: dict[str, int], ambang_hari: int = 30
) -> set[str]:
    """Simbol yang datanya berhenti jauh sebelum data lain berakhir.

    Definisi ini sengaja diturunkan dari data itu sendiri, bukan dari daftar
    delisting eksternal. Daftar eksternal bisa hilang, berubah, atau tidak
    tersedia untuk bursa lain di kemudian hari; sedangkan "berhenti terbit"
    dapat diperiksa ulang siapa pun dari aset yang sama.

    Dengan ADR-003, stempel yang masuk ke sini sudah dikoreksi: simbol mati
    menggunakan tanggal kematian sejatinya, bukan tanggal ujung dataset.
    """
    if not akhir:
        return set()
    terakhir = max(akhir.values())
    batas = terakhir - ambang_hari * HARI_MS
    return {s for s, t in akhir.items() if t < batas}


def simbol_mati(bingkai: dict[str, pd.DataFrame], ambang_hari: int = 30) -> set[str]:
    akhir = {s: int(d["open_time"].iloc[-1]) for s, d in bingkai.items() if len(d)}
    return simbol_mati_dari_akhir(akhir, ambang_hari)


def ringkas_gabungan(ringkasan_per_simbol: list[dict]) -> dict:
    """Gabungkan ringkasan lintas simbol tanpa merata-ratakan rata-rata.

    Merata-ratakan ekspektasi antar simbol memberi bobot sama pada simbol yang
    menghasilkan tiga perdagangan dan simbol yang menghasilkan tiga ratus.
    Karena itu ekspektasi gabungan dihitung dari total R dibagi total
    perdagangan, bukan dari rerata ekspektasi.
    """
    n = sum(r["jumlah_trade_luar_sampel"] for r in ringkasan_per_simbol)
    total_r = sum(r["total_R"] for r in ringkasan_per_simbol)
    jendela = sum(r["jumlah_jendela"] for r in ringkasan_per_simbol)
    positif = sum(r["jendela_positif"] for r in ringkasan_per_simbol)
    return {
        "jumlah_simbol": len(ringkasan_per_simbol),
        "jumlah_jendela": jendela,
        "jendela_positif": positif,
        "jumlah_trade_luar_sampel": n,
        "total_R": float(total_r),
        "ekspektasi_R": float(total_r / n) if n else None,
    }


# --------------------------------------------------------------------------
# Gerbang yang harus digabung per simbol
# --------------------------------------------------------------------------
def gabung_gerbang(
    nama: str,
    daftar: list[Gerbang],
    ambang: float | None,
    nama_simbol: list[str] | None = None,
) -> Gerbang:
    """Gabungkan gerbang per simbol menjadi satu putusan.

    Satu simbol gagal berarti gerbangnya gagal. Menghitung berapa persen simbol
    yang lulus akan mengubah gerbang menjadi skor, dan angka nilainya diambil
    dari kasus terburuk supaya jarak menuju kegagalan tetap terlihat.

    Bila ``nama_simbol`` diberikan, nama simbol yang gagal ikut dicetak beserta
    catatan aslinya. Tanpa itu, laporan hanya menyebut jumlah, dan jumlah tidak
    dapat ditindaklanjuti: catatan asli menyimpan dimensi mana yang dilanggar,
    yang belum tentu sama dengan angka gabungan yang ditampilkan.
    """
    if not daftar:
        return Gerbang(nama, False, None, ambang, "tidak dapat dinilai: tidak ada simbol")
    pasang = list(zip(nama_simbol or [""] * len(daftar), daftar))
    gagal = [(s, g) for s, g in pasang if not g.lulus]
    ternilai = [g.nilai for g in daftar if g.nilai is not None]
    catatan = f"{len(gagal)} dari {len(daftar)} simbol gagal"
    if gagal and any(s for s, _ in gagal):
        rinci = "; ".join(f"{s} ({g.catatan})" for s, g in gagal[:5])
        if len(gagal) > 5:
            rinci += f"; dan {len(gagal) - 5} lagi"
        catatan = f"{catatan} — {rinci}"
    return Gerbang(
        nama,
        not gagal,
        max(ternilai) if ternilai else None,
        ambang,
        catatan,
    )


def gerbang_overlap_gabungan(hasil_per_simbol: dict[str, Hasil]) -> Gerbang:
    """Overlap dinilai per simbol, tidak pernah atas kumpulan campuran.

    Dua posisi pada dua simbol berbeda memang berjalan bersamaan; itu
    diversifikasi, bukan penumpukan. Yang dilarang adalah dua posisi pada simbol
    yang sama.
    """
    nama = [s for s, h in sorted(hasil_per_simbol.items()) if h.jumlah_trade]
    daftar = [
        gerbang_overlap(hasil_per_simbol[s]) for s in nama
    ]
    return gabung_gerbang("overlap", daftar, 0.0, nama)


def gerbang_bnh_gabungan(daftar: list[Gerbang]) -> Gerbang:
    """Keunggulan terhadap buy-and-hold dinilai dari median lintas simbol.

    Median dipilih, bukan rerata, karena satu simbol yang naik ribuan persen
    dapat menyeret rerata menjadi positif meskipun strategi kalah di hampir
    semua simbol lain.
    """
    nilai_nilai = [g.nilai for g in daftar if g.nilai is not None]
    if not nilai_nilai:
        return Gerbang(
            "buy_and_hold", False, None, 0.0, "tidak dapat dinilai: tidak ada simbol"
        )
    arr = np.array(nilai_nilai, dtype="float64")
    med = float(np.median(arr))
    unggul = int((arr > 0).sum())
    return Gerbang(
        "buy_and_hold",
        med > 0.0,
        med,
        0.0,
        f"median selisih {med:.4f}; unggul di {unggul}/{arr.size} simbol",
    )


def hipotesis_h001(komit: str = "") -> Hipotesis:
    return Hipotesis(
        id="H-001",
        pernyataan=(
            "Penembusan Donchian pada penutupan bar 1 jam menghasilkan ekspektasi "
            "positif setelah fee, slippage, dan funding nyata, pada perp USDT yang "
            "lolos ambang kelayakan, dinilai hanya di luar sampel."
        ),
        dataset=(
            "tier-b-v1 ohlcv_1h + funding_shard, "
            "universe_layak_v2 438 simbol (ADR-003, ekor datar dipangkas)"
        ),
        ruang_parameter=dict(breakout_atr.RUANG_PARAMETER),
        kriteria=Kriteria(
            min_ekspektasi_R=0.05,
            min_trade_luar_sampel=100,
            maks_p_entri_acak=0.05,
            min_jendela_positif_rasio=0.5,
        ),
        komit=komit,
    )


# --------------------------------------------------------------------------
# Utama
# --------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--interval", default="1h")
    ap.add_argument("--universe", default="reports/universe_layak_v2.json")
    ap.add_argument("--akhir-sejati", default="reports/akhir_sejati.json")
    ap.add_argument("--config", default="config/lux.yaml")
    ap.add_argument("--out", default="reports")
    ap.add_argument("--hipotesis", default="hipotesis/H-001.json")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--panjang-latih", type=int, default=4320)
    ap.add_argument("--panjang-uji", type=int, default=2160)
    ap.add_argument("--embargo", type=int, default=168)
    ap.add_argument("--pemanasan", type=int, default=200)
    ap.add_argument("--ulangan", type=int, default=100)
    ap.add_argument("--sampel-permutasi", type=int, default=10)
    ap.add_argument("--komit", default="")
    a = ap.parse_args(argv)

    t0 = time.time()

    # 1. Hipotesis dikunci sebelum satu baris data pun dibaca.
    h = hipotesis_h001(a.komit)
    jalur = simpan(h, a.hipotesis)
    print(f"hipotesis {h.id} terdaftar di {jalur} (sidik {h.sidik()[:12]})", flush=True)
    print(f"ruang pencarian: {h.jumlah_kombinasi} kombinasi", flush=True)

    konfig = muat_konfig(Path(a.config))
    semesta = json.loads(Path(a.universe).read_text(encoding="utf-8"))["simbol"]
    dipilih = sorted(semesta)[: a.limit] if a.limit > 0 else sorted(semesta)
    print(f"universe layak {len(semesta)}, diuji {len(dipilih)}", flush=True)

    bingkai, berkas = muat_ohlcv(Path(a.dir), a.interval, set(dipilih))
    jadwal_semua = muat_jadwal(Path(a.dir))
    akhir_semesta = akhir_per_simbol(
        Path(a.dir), a.interval, Path(a.akhir_sejati)
    )
    print(
        f"{len(bingkai)} simbol dimuat, {len(jadwal_semua)} jadwal funding, "
        f"{len(akhir_semesta)} simbol dipindai untuk survivorship",
        flush=True,
    )

    # Sampel permutasi dipilih sebelum hasil terlihat, dari daftar terurut,
    # sehingga tidak mungkin menjadi pilihan yang menguntungkan.
    sampel = set(sorted(bingkai)[: a.sampel_permutasi])

    kandidat = breakout_atr.kandidat()
    ringkasan_simbol: list[dict] = []
    per_simbol: list[dict] = []
    semua_trade = []
    hasil_per_simbol: dict[str, Hasil] = {}
    jendela_sampel: list[tuple[pd.DataFrame, np.ndarray, str]] = []
    g_forward: list[Gerbang] = []
    nama_forward: list[str] = []
    g_bnh: list[Gerbang] = []

    for i, s in enumerate(sorted(bingkai), 1):
        df = bingkai[s]
        try:
            jadwal = ambil_jadwal(jadwal_semua, s)
        except KeyError as e:
            print(f"  [{i}] {s}: DILEWATI, {e}", flush=True)
            continue

        wf = jalankan_walk_forward(
            df,
            kandidat=kandidat,
            buat_sinyal=breakout_atr.sinyal,
            panjang_latih=a.panjang_latih,
            panjang_uji=a.panjang_uji,
            embargo=a.embargo,
            pemanasan=a.pemanasan,
            konfig=konfig,
            jadwal=jadwal,
            symbol=s,
            simpan_bingkai=s in sampel,
        )
        r = wf.ringkas()
        trade_simbol = wf.perdagangan_luar_sampel
        ringkasan_simbol.append(r)
        semua_trade.extend(trade_simbol)
        hasil_per_simbol[s] = Hasil(symbol=s, perdagangan=trade_simbol)
        per_simbol.append(
            {
                "symbol": s,
                "bar": int(len(df)),
                "jendela": r["jumlah_jendela"],
                "trade": r["jumlah_trade_luar_sampel"],
                "total_R": round(r["total_R"], 4),
                "ekspektasi_R": (
                    None if r["ekspektasi_R"] is None else round(r["ekspektasi_R"], 5)
                ),
                "parameter": r["parameter_per_jendela"],
            }
        )

        g_forward.append(gerbang_forward_fill(df))
        nama_forward.append(s)

        # Buy-and-hold: laba luar sampel atas modal awal, dibandingkan dengan
        # memegang aset sepanjang wilayah penilaian. Kurva ekuitas tiap jendela
        # tidak disambung karena masing-masing memulai ulang dari modal awal.
        if wf.per_jendela and trade_simbol:
            awal_uji = wf.per_jendela[0].jendela.uji_awal
            akhir_uji = wf.per_jendela[-1].jendela.uji_akhir
            laba = float(sum(p.laba for p in trade_simbol))
            g_bnh.append(
                gerbang_buy_and_hold(
                    Hasil(
                        symbol=s,
                        perdagangan=trade_simbol,
                        ekuitas=np.array(
                            [konfig.modal_awal, konfig.modal_awal + laba]
                        ),
                    ),
                    df.iloc[awal_uji:akhir_uji],
                )
            )

        for hj in wf.per_jendela:
            if hj.bingkai_uji is not None and hj.sinyal_uji is not None:
                jendela_sampel.append((hj.bingkai_uji, hj.sinyal_uji, s))

        if i % 5 == 0 or i == len(bingkai):
            print(
                f"  [{i}/{len(bingkai)}] {s}: {r['jumlah_trade_luar_sampel']} trade, "
                f"{time.time() - t0:.0f}s",
                flush=True,
            )

    gabungan = ringkas_gabungan(ringkasan_simbol)
    print(json.dumps(gabungan, indent=2), flush=True)

    diagnosa = diagnosa_biaya(semua_trade)
    print(
        "biaya rerata: transaksi "
        f"{diagnosa['rerata_transaksi_R']}R, funding {diagnosa['rerata_funding_R']}R, "
        f"{diagnosa['trade_biaya_lebih_1R']} trade berbiaya di atas 1R",
        flush=True,
    )

    # ----------------------------------------------------------------------
    # Sembilan gerbang
    # ----------------------------------------------------------------------
    hasil_pool = Hasil(
        symbol="POOL",
        perdagangan=semua_trade,
        ekuitas=np.array([konfig.modal_awal]),
    )

    gerbang_ff = gabung_gerbang("forward_fill", g_forward, 0.30, nama_forward)
    gerbang_bnh = gerbang_bnh_gabungan(g_bnh)

    # Entri acak atas wilayah penilaian yang sama persis.
    p_acak: float | None = None
    if jendela_sampel:
        panjang = [len(s_) for _, s_, _ in jendela_sampel]
        batas = np.cumsum([0] + panjang)
        sinyal_gabung = np.concatenate([s_ for _, s_, _ in jendela_sampel])

        def penilai(sinyal_acak: np.ndarray) -> float:
            rs = []
            for k, (bingkai_j, _, sym) in enumerate(jendela_sampel):
                potong = sinyal_acak[batas[k] : batas[k + 1]]
                hasil_j = jalankan(
                    bingkai_j,
                    potong,
                    konfig,
                    jadwal=jadwal_semua.get(sym),
                    symbol=sym,
                )
                rs.extend(p.R for p in hasil_j.perdagangan)
            return float(np.mean(rs)) if rs else float("-inf")

        nyata = penilai(sinyal_gabung)
        gerbang_acak = gerbang_entri_acak(
            nyata, sinyal_gabung, penilai, ulangan=a.ulangan
        )
        p_acak = gerbang_acak.nilai
        print(
            f"entri acak: nyata {nyata:.5f}R, p {p_acak}, {time.time() - t0:.0f}s",
            flush=True,
        )
    else:
        gerbang_acak = Gerbang(
            "entri_acak", False, None, None, "tidak dapat dinilai: tidak ada jendela sampel"
        )

    # Lookahead atas fungsi sinyal, bukan atas hasil.
    if bingkai:
        contoh = bingkai[sorted(bingkai)[0]]
        gerbang_la = gerbang_lookahead(
            contoh.iloc[:5000],
            lambda d: breakout_atr.sinyal(d, {"lookback": 55}),
        )
    else:
        gerbang_la = Gerbang("lookahead", False, None, None, "tidak dapat dinilai: tidak ada data")

    gerbang_ir = gerbang_invarian_risiko(hasil_pool)
    gerbang_fd = gerbang_funding(hasil_pool, jadwal_dimuat=bool(jadwal_semua))
    gerbang_ov = gerbang_overlap_gabungan(hasil_per_simbol)

    # Checksum aset terhadap manifest sekali-tulis.
    manifest_path = Path(a.out) / "manifest_aset.json"
    terhitung = {p.name: sha256_berkas(p) for p in berkas}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        gerbang_cs = gerbang_checksum(manifest, terhitung)
    else:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(terhitung, indent=2, sort_keys=True), encoding="utf-8"
        )
        gerbang_cs = Gerbang(
            "checksum",
            False,
            None,
            None,
            "tidak dapat dinilai: manifest baru ditulis pada run ini; "
            "run berikutnya akan membandingkannya",
        )

    # Survivorship terhadap universe layak yang penuh, bukan subset yang diuji.
    # Stempel akhir_semesta sudah dikoreksi ADR-003 sehingga simbol mati
    # menggunakan tanggal kematian nyatanya, bukan tanggal ujung dataset.
    semesta_layak = [s for s in semesta if s in akhir_semesta]
    mati = simbol_mati_dari_akhir(
        {s: akhir_semesta[s] for s in semesta_layak}
    )
    gerbang_sv = gerbang_survivorship(
        simbol_diuji=[r["symbol"] for r in ringkasan_simbol],
        simbol_delisted=mati,
        simbol_universe=semesta_layak,
    )

    laporan = susun_laporan(
        [
            gerbang_ff,
            gerbang_bnh,
            gerbang_acak,
            gerbang_la,
            gerbang_ir,
            gerbang_fd,
            gerbang_ov,
            gerbang_cs,
            gerbang_sv,
        ]
    )
    putusan = nilai(h, gabungan, p_acak)

    # ----------------------------------------------------------------------
    # Laporan
    # ----------------------------------------------------------------------
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    isi = {
        "hipotesis": h.ke_dict() | {"sidik": h.sidik()},
        "parameter_run": {
            "interval": a.interval,
            "limit": a.limit,
            "panjang_latih": a.panjang_latih,
            "panjang_uji": a.panjang_uji,
            "embargo": a.embargo,
            "pemanasan": a.pemanasan,
            "ulangan_permutasi": a.ulangan,
            "sampel_permutasi": sorted(sampel),
            "simbol_mati_di_universe": len(mati),
        },
        "gabungan": gabungan,
        "diagnosa_biaya": diagnosa,
        "gerbang": laporan.ke_dict(),
        "putusan": {"lulus": putusan.lulus, "alasan": putusan.alasan},
        "per_simbol": per_simbol,
        "detik": round(time.time() - t0, 1),
    }
    (out / "backtest_h001.json").write_text(
        json.dumps(isi, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    md = [
        "# Backtest H-001 \u2014 breakout Donchian 1 jam",
        "",
        f"> {h.pernyataan}",
        "",
        f"Sidik hipotesis `{h.sidik()[:16]}` \u00b7 ruang {h.jumlah_kombinasi} kombinasi "
        f"\u00b7 {gabungan['jumlah_simbol']} simbol \u00b7 {isi['detik']}s",
        "",
        "## Putusan",
        "",
        f"**{'LULUS' if putusan.lulus and laporan.semua_lulus else 'DITOLAK'}**",
        "",
    ]
    if putusan.alasan:
        md += ["Kriteria pra-registrasi yang tidak terpenuhi:", ""]
        md += [f"- {al}" for al in putusan.alasan]
        md += [""]
    if laporan.yang_gagal:
        md += [f"Gerbang gagal: {', '.join(laporan.yang_gagal)}", ""]

    md += [
        "## Hasil luar sampel",
        "",
        f"- Perdagangan: **{gabungan['jumlah_trade_luar_sampel']:,}**",
        f"- Total R: **{gabungan['total_R']:.2f}**",
        f"- Ekspektasi: **{gabungan['ekspektasi_R']}**",
        f"- Jendela positif: {gabungan['jendela_positif']}/{gabungan['jumlah_jendela']}",
        "",
        "## Sembilan gerbang",
        "",
        "| Gerbang | Putusan | Nilai | Ambang | Catatan |",
        "|---|---|---|---|---|",
    ]
    for g in laporan.gerbang:
        n = "\u2014" if g.nilai is None else f"{g.nilai:.4f}"
        am = "\u2014" if g.ambang is None else f"{g.ambang}"
        md.append(
            f"| {g.nama} | {'lulus' if g.lulus else 'GAGAL'} | {n} | {am} | {g.catatan} |"
        )

    md += [
        "",
        "## Pembongkaran biaya",
        "",
        "Mesin mengisi stop tepat di harga stop, sehingga kerugian yang berasal "
        "dari harga tidak dapat melewati 1R. Kerugian di luar itu wajib berasal "
        "dari biaya, dan tabel ini memperlihatkannya per perdagangan.",
        "",
    ]
    if diagnosa["jumlah"]:
        md += [
            f"- Rerata biaya transaksi: **{diagnosa['rerata_transaksi_R']:.4f}R**",
            f"- Rerata biaya funding: **{diagnosa['rerata_funding_R']:.4f}R**",
            f"- Rerata jarak stop terhadap harga: "
            f"**{diagnosa['rerata_stop_frac'] * 100:.3f}%**",
            f"- Perdagangan dengan biaya melebihi 1R: "
            f"**{diagnosa['trade_biaya_lebih_1R']:,}** dari {diagnosa['jumlah']:,}",
            "",
            "| Simbol | R | Kotor R | Transaksi R | Funding R | Stop % harga | Jam | Alasan |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for r in diagnosa["terburuk"]:
            md.append(
                f"| {r['symbol']} | {r['R']:.3f} | {r['kotor_R']:.3f} | "
                f"{r['transaksi_R']:.3f} | {r['funding_R']:.3f} | "
                f"{r['stop_frac'] * 100:.3f} | {r['jam']:.1f} | {r['alasan']} |"
            )
    else:
        md += ["Tidak ada perdagangan untuk dibongkar."]

    md += [
        "",
        "## Sepuluh simbol dengan total R tertinggi",
        "",
        "| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |",
        "|---|---|---|---|---|---|",
    ]
    for r in sorted(per_simbol, key=lambda x: -x["total_R"])[:10]:
        md.append(
            f"| {r['symbol']} | {r['bar']:,} | {r['jendela']} | {r['trade']} | "
            f"{r['total_R']:.2f} | {r['ekspektasi_R']} |"
        )
    md += [
        "",
        "## Sepuluh simbol dengan total R terendah",
        "",
        "| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |",
        "|---|---|---|---|---|---|",
    ]
    for r in sorted(per_simbol, key=lambda x: x["total_R"])[:10]:
        md.append(
            f"| {r['symbol']} | {r['bar']:,} | {r['jendela']} | {r['trade']} | "
            f"{r['total_R']:.2f} | {r['ekspektasi_R']} |"
        )

    (out / "backtest_h001.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:20]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
