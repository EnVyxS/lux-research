"""Jalur B — sebaran nol permutasi sinyal untuk H-013, dipecah sepuluh bagian.

ADR-015 bagian 4.4 menuntut **dua** syarat dalam satu kalimat: besaran
``SS − AS ≥ 0,020R`` **dan** ``p ≤ 0,05`` atas sedikitnya 300 ulangan permutasi
sinyal. Sampai run 30214203863 hanya besarannya yang pernah dihitung, dan medan
``lulus`` di laporan kontribusi karena itu bukan kelulusan hipotesis (ADR-024).
Modul ini menghasilkan bahan untuk syarat yang kedua: **300 sel AS**, masing-masing
dengan seed permutasi berbeda, sehingga ekspektasi sel SS dapat dibandingkan
terhadap sebaran nol yang sungguh-sungguh ditarik alih-alih diandaikan.

Aritmetika ``p`` **tidak** ada di sini. Ia ada di ``lux.analisis.sebaran_nol``,
modul daun yang sudah diuji, sebab aritmetika yang hanya hidup di dalam ``main``
tidak pernah benar-benar diuji dan itulah sebab dua cacat sebelumnya tidak
berbunyi selama berbulan-bulan (aturan 32). Yang ada di sini hanyalah orkestrasi:
menjalankan sel, menyerap yang perlu, membuang sisanya.

EMPAT KEPUTUSAN YANG WAJIB DIKETAHUI SEBELUM MEMBACA PECAHAN
------------------------------------------------------------
**1. Laporan antara memakai nama sendiri, dan itu bukan kerapian belaka.**
``jalankan_spek`` menulis ``backtest_<nama>.json`` — nama yang **sama** pada
setiap pemanggilan. Bila Jalur B memakai ``h013_as_acak_stop``, pemanggilan
pertama akan **menimpa laporan sel AS run 30214203863 yang sudah dikomit**, dan
satu-satunya pembanding sah bagi seluruh jalur ini hilang tanpa jejak. Karena itu
nama speknya ``h013b_as_seed``: berkas antara, ditimpa 30 kali per pecahan, dan
**tidak** dikomit. Menamai unik per seed juga ditolak: 432.200 B kali 300
mendekati 130 MB dikomit untuk satu jalur analisis (ADR-029 R2).

**2. Gerbang ``entri_acak`` DIMATIKAN, dan kematiannya wajib tercetak.**
``jalankan_spek`` menjalankan gerbang itu dengan ``opsi.ulangan`` permutasi di
dalam **setiap** pemanggilan. Pada Jalur B itu berarti 300 permutasi bersarang di
dalam 300 seed — 90.000 backtest — untuk sebuah angka yang tidak dipakai sekali
pun, sebab sebaran nol Jalur B dibangun dari seed-nya sendiri. Mekanismenya
dimatikan lewat ``sampel_permutasi = 0``: ``ktx.sampel`` menjadi himpunan kosong
sehingga tidak ada ``jendela_sampel`` dan gerbangnya melaporkan "tidak dapat
dinilai". Setiap pecahan **wajib** menyatakannya, sebab pelonggaran yang tidak
dinyatakan adalah cara paling rapi sebuah pagar berhenti menjaga.

**3. Seed 42 ada di dalam rentang, dan ia tripwire gratis (R-D5).**
Sel AS run 30214203863 memakai seed 42, dan angkanya sudah dikomit:
``+0,01180570125176449R``. Bila alat ini benar, seed 42 wajib mereproduksinya
**tepat** — bukan mendekati. Bila meleset, pecahan tetap ditulis (bukti jangan
dibuang) tetapi ``r_d5_cocok`` bernilai ``false`` dan kode keluar 3, sebab
sebaran nol yang tidak dapat mereproduksi satu titik yang diketahui bukan sebaran
nol untuk perbandingan itu.

**4. Hanya ada SATU implementasi permutasi.** ``sinyal_acak_seed(42)`` wajib
bitwise identik dengan ``sinyal_acak`` milik ``run_h013``, dan pengujian menuntut
kesamaan itu. Dua implementasi pengacakan adalah cara paling andal melahirkan dua
sebaran nol yang berbeda tanpa ada yang menyadarinya. Seed tidak dapat disuntikkan
lewat ``Spek.sinyal`` — tanda tangannya ``(df, params)`` dan ``sinyal_acak``
memanggil ``permutasi_sinyal`` tanpa menyerahkan seed — sehingga pabrik fungsi
berdiri di sini alih-alih ``run_h013`` ditulis ulang untuk ketiga kalinya.

SATUAN PENARIKAN
----------------
Pecahan menyimpan agregat **bulanan** (``agregat_periode``), bukan ekspektasi
gabungan saja, sebab ADR-028 mematok satuan penarikan pada bulan kalender UTC.
Ekspektasi gabungan ikut disimpan hanya supaya versi per perdagangan dapat
dihitung sebagai pembanding yang ditandai **taksiran bawah**.

Bulan tanpa perdagangan dibuang dari sebaran tetapi **dicatat** di
``bulan_dibuang``. Pembuangan diam-diam akan mengubah himpunan bulan per seed,
dan ``sebaran_nol.selisih_bulanan`` justru menolak himpunan yang tidak sama —
penolakan itu hanya berguna bila apa yang dibuang terlihat.

Pemakaian (satu pecahan per pekerjaan, sepuluh pekerjaan sejajar):
    python -m lux.backtest.run_h013b --dir aset --interval 4h \\
        --universe reports/universe_layak_v2_4h.json \\
        --akhir-sejati reports/akhir_sejati_4h.json \\
        --min-median-stop-frac 0.004 --seed-awal 30 --seed-akhir 60
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

from lux.analisis.sebaran_nol import KUNCI_BULAN
from lux.backtest.engine import Konfig
from lux.backtest.run_h002 import muat_konfig_h002
from lux.backtest.run_h012 import kunci_config
from lux.backtest.run_h013 import (
    MIN_ULANGAN,
    NAMA_LAPORAN,
    PEMANASAN,
    SEED_PERMUTASI,
    UMUR_SEL_STOP,
    bar_dibutuhkan,
    buat_konfig_sel,
    dasar_riset,
    hipotesis_h013,
    jendela_bar,
    kandidat,
    permutasi_sinyal,
    sinyal_acak,
)
from lux.backtest.runner import Opsi, Spek, jalankan_spek, muat_konteks
from lux.strategi import breakout_atr

NAMA = "h013b"

# Nama spek Jalur B. SENGAJA berbeda dari seluruh nilai NAMA_LAPORAN; sebuah
# pengujian menuntut perbedaan itu, sebab kesamaannya akan menimpa laporan yang
# sudah dikomit tanpa satu pun pesan galat.
NAMA_SPEK = "h013b_as_seed"

# 300 seed, sepuluh pecahan berisi 30. Angka 300 bukan pilihan hari ini: ia
# ambang ulangan ADR-015 yang dibekukan, dan ia tidak diturunkan.
SEED_AWAL = 0
SEED_AKHIR = 300
SEED_PER_PECAHAN = 30

# R-D5. Ekspektasi sel AS run 30214203863, dikutip apa adanya dari laporan yang
# sudah dikomit. Toleransinya bukan "sekitar": permutasi dengan seed yang sama
# atas data yang sama wajib menghasilkan bilangan yang sama.
EKSPEKTASI_AS_SEED42 = 0.01180570125176449
TOLERANSI_SEED42 = 1e-12

PEMBATAS = (
    "Pecahan ini adalah BAHAN, bukan putusan: tidak ada satu pun nilai p di "
    "dalamnya. p dihitung oleh lux.analisis.sebaran_nol pada satuan penarikan "
    "BULAN kalender UTC (ADR-028); satuan perdagangan hanya sah untuk "
    "MENJATUHKAN klaim. Gerbang `entri_acak` DIMATIKAN di seluruh run Jalur B "
    "lewat sampel_permutasi = 0, sebab ia akan menjalankan 300 permutasi di "
    "dalam setiap seed untuk angka yang jalur ini tidak pakai; sebaran nol "
    "Jalur B dibangun dari seed-nya sendiri. Sepuluh gerbang lain tetap "
    "dinilai. Sel AS memang TIDAK dimaksudkan lulus kriteria apa pun."
)


def sinyal_acak_seed(seed: int):
    """Pabrik fungsi sinyal: Donchian yang sama, waktunya diacak dengan ``seed``.

    Ia ada karena ``Spek.sinyal`` bertanda tangan ``(df, params)`` sehingga seed
    tidak dapat dititipkan lewat parameter, dan karena ``run_h013.sinyal_acak``
    memanggil ``permutasi_sinyal`` tanpa menyerahkan seed — seed 42 terpaku di
    sana. Pabrik ini **tidak** menyalin aritmetika pengacakan: ia memanggil
    ``permutasi_sinyal`` yang sama, dan pengujian menuntut ``sinyal_acak_seed(42)``
    bitwise identik dengan ``sinyal_acak``.

    Seperti ``sinyal_acak``, permutasi dilakukan **per bingkai**, bukan atas
    gabungan lintas jendela (ADR-021 keputusan 2). Jumlah dan arah entri karena
    itu terjaga per simbol, yang lebih ketat daripada terjaga secara agregat.
    """
    s = int(seed)

    def sinyal(df: pd.DataFrame, params: dict) -> np.ndarray:
        return permutasi_sinyal(breakout_atr.sinyal(df, params), seed=s)

    sinyal.__name__ = f"sinyal_acak_seed_{s}"
    return sinyal


def periksa_kesetaraan(df: pd.DataFrame, params: dict) -> bool:
    """Tuntut ``sinyal_acak_seed(42)`` identik dengan ``sinyal_acak``.

    Dijalankan sebagai pagar pra-terbang atas bingkai sungguhan, bukan hanya di
    dalam pengujian atas bingkai sintetis, sebab yang hendak dijamin adalah
    kesamaan pada data yang benar-benar dipakai run ini.
    """
    a = np.asarray(sinyal_acak(df, params))
    b = np.asarray(sinyal_acak_seed(SEED_PERMUTASI)(df, params))
    if not np.array_equal(a, b):
        raise ValueError(
            "sinyal_acak_seed(42) tidak identik dengan sinyal_acak; ada dua "
            "implementasi pengacakan, dan sebaran nol Jalur B tidak sebanding "
            "dengan sel AS yang sudah dikomit"
        )
    return True


def daftar_seed(awal: int, akhir: int) -> list[int]:
    """Seed pada selang setengah terbuka ``[awal, akhir)``, tanpa kembar."""
    if akhir <= awal:
        raise ValueError(f"rentang seed kosong: [{awal}, {akhir})")
    if awal < SEED_AWAL or akhir > SEED_AKHIR:
        raise ValueError(
            f"rentang [{awal}, {akhir}) keluar dari rentang beku "
            f"[{SEED_AWAL}, {SEED_AKHIR})"
        )
    if akhir - awal > SEED_PER_PECAHAN:
        raise ValueError(
            f"pecahan {akhir - awal} seed melampaui {SEED_PER_PECAHAN}; "
            "batas 6 jam per pekerjaan tidak dapat ditawar"
        )
    return list(range(int(awal), int(akhir)))


def jalur_pecahan(awal: int, akhir: int, out: Path | str = "reports") -> Path:
    """Satu berkas ringkas per pecahan (ADR-029 R2)."""
    return Path(out) / f"h013b_seed_{int(awal)}_{int(akhir)}.json"


def jalur_antara(nama: str, out: Path | str = "reports") -> Path:
    """Laporan yang ``jalankan_spek`` tulis, yang akan dibaca lalu ditimpa."""
    return Path(out) / f"backtest_{nama}.json"


def baca_bulan(jalur: Path | str) -> dict:
    """Serap agregat bulanan dari laporan yang **baru ditulis**, buang sisanya.

    Inilah rancangan yang lulus pemeriksaan struktur (ADR-029 R1). Dua rancangan
    sebelumnya jatuh: nilai kembalian ``jalankan_spek`` adalah ringkasan yang
    medan bulanannya hanya sebuah **cacah** (``bulan_dengan_trade``), dan laporan
    per seed bernama unik berarti ~130 MB dikomit.

    Baris bulan tanpa ``ekspektasi_R`` dibuang dari sebaran tetapi dikembalikan
    di ``dibuang``. ``sebaran_nol._peta_bulan`` menolak baris semacam itu, dan
    ``selisih_bulanan`` menolak himpunan bulan yang tidak sama; penolakan itu
    hanya berguna bila apa yang dibuang terlihat.
    """
    p = Path(jalur)
    if not p.exists():
        raise FileNotFoundError(
            f"laporan antara {p} tidak ada; jalankan_spek tidak menulis apa pun"
        )
    isi = json.loads(p.read_text(encoding="utf-8"))
    if "agregat_periode" not in isi:
        raise ValueError(
            f"{p} tanpa medan agregat_periode; R per bulan tidak dapat diambil "
            "dari mana pun selain berkas ini"
        )
    baris = isi["agregat_periode"]
    if not isinstance(baris, list):
        raise ValueError(f"agregat_periode di {p} bukan daftar: {type(baris)}")

    bulan: list[dict] = []
    dibuang: list[str] = []
    for b in baris:
        kurang = [k for k in KUNCI_BULAN if k not in b]
        if kurang:
            raise ValueError(f"baris bulan tanpa kunci {kurang}: {b}")
        if b["ekspektasi_R"] is None or int(b["trade"]) <= 0:
            dibuang.append(str(b["periode"]))
            continue
        bulan.append({k: b[k] for k in KUNCI_BULAN})
    if not bulan:
        raise ValueError(f"{p} tidak menyisakan satu pun bulan dengan perdagangan")
    return {"bulan": bulan, "dibuang": dibuang}


def baris_seed(seed: int, hasil: dict, terbaca: dict) -> dict:
    """Satu baris pecahan. Ringkas dengan sengaja: yang tidak dipakai tidak ikut.

    Laporan sel utuh berukuran 432.200 B. Yang dibutuhkan sebaran nol hanyalah
    ekspektasi gabungan dan agregat bulanan, sehingga sisanya dibuang di sini —
    di sisi runner, sebelum apa pun dikomit.
    """
    return {
        "seed": int(seed),
        "ekspektasi_R": hasil["ekspektasi_R"],
        "total_R": hasil["total_R"],
        "trade": int(hasil["trade"]),
        "jumlah_jendela": hasil["jumlah_jendela"],
        "sidik": hasil["sidik"],
        "detik": hasil.get("detik"),
        "bulan": terbaca["bulan"],
        "bulan_dibuang": terbaca["dibuang"],
    }


def opsi_seed(a, jen: dict) -> Opsi:
    """Opsi Jalur B. ``sampel_permutasi = 0`` mematikan gerbang ``entri_acak``.

    ``ulangan`` tetap dipasang pada ambang beku meski tak terpakai, supaya tidak
    ada berkas Jalur B yang tampak seolah ambang itu diturunkan.
    """
    return Opsi(
        dir_aset=Path(a.dir),
        out=Path(a.out),
        interval=a.interval,
        universe=Path(a.universe),
        akhir_sejati=Path(a.akhir_sejati),
        limit=a.limit,
        panjang_latih=jen["panjang_latih"],
        panjang_uji=jen["panjang_uji"],
        embargo=jen["embargo"],
        pemanasan=PEMANASAN,
        ulangan=MIN_ULANGAN,
        sampel_permutasi=0,
        min_median_stop_frac=a.min_median_stop_frac,
    )


def spek_seed(seed: int, konfig: Konfig, komit: str = "") -> Spek:
    """Spek sel AS dengan seed tertentu, memakai nama laporan Jalur B.

    Hipotesis, kandidat, dan pembuat konfig **diimpor** dari ``run_h013``, tidak
    diketik ulang: geometri keluar sel AS wajib identik dengan sel AS run
    30214203863, sebab satu-satunya yang boleh berbeda adalah seed.
    """
    return Spek(
        h=hipotesis_h013("AS", konfig, komit),
        sinyal=sinyal_acak_seed(seed),
        kandidat=kandidat(),
        nama=NAMA_SPEK,
        params_lookahead={"lookback": 55},
        buat_konfig=buat_konfig_sel("AS"),
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--interval", default="4h")
    ap.add_argument("--universe", default="reports/universe_layak_v2_4h.json")
    ap.add_argument("--akhir-sejati", default="reports/akhir_sejati_4h.json")
    ap.add_argument("--config", default="config/lux.yaml")
    ap.add_argument("--out", default="reports")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--min-median-stop-frac", type=float, required=True)
    ap.add_argument("--seed-awal", type=int, required=True)
    ap.add_argument("--seed-akhir", type=int, required=True)
    ap.add_argument("--komit", default="")
    a = ap.parse_args(argv)

    # Seluruh pagar berjalan sebelum satu bar pun dimuat.
    if a.interval != "4h":
        print(
            f"DITOLAK: Jalur B hanya sah pada kerangka 4h, diberi {a.interval!r}.",
            flush=True,
        )
        return 2
    for nama_arg, jalur in (("universe", a.universe), ("akhir-sejati", a.akhir_sejati)):
        if "4h" not in Path(jalur).name:
            print(
                f"DITOLAK: {nama_arg} {jalur!r} tidak menyebut 4h.", flush=True
            )
            return 2
    if a.min_median_stop_frac <= 0:
        print(
            "DITOLAK: lantai median stop_frac wajib menyala, sama seperti run "
            "yang menghasilkan sel SS pembandingnya.",
            flush=True,
        )
        return 2
    if SEED_AKHIR - SEED_AWAL < MIN_ULANGAN:
        raise ValueError(
            f"rentang seed beku hanya {SEED_AKHIR - SEED_AWAL} < {MIN_ULANGAN}; "
            "ambang ulangan ADR-015 tidak diturunkan"
        )
    if NAMA_SPEK in set(NAMA_LAPORAN.values()):
        raise ValueError(
            f"nama spek Jalur B {NAMA_SPEK} bertumpang dengan laporan H-013 yang "
            "sudah dikomit; laporan itu akan tertimpa"
        )

    seed = daftar_seed(a.seed_awal, a.seed_akhir)

    dasar = dasar_riset(muat_konfig_h002(Path(a.config)))
    kunci = kunci_config(Path(a.config))
    if kunci["min_median_stop_frac"] != a.min_median_stop_frac:
        raise ValueError(
            f"lantai pemanggil {a.min_median_stop_frac} berselisih dengan config "
            f"{kunci['min_median_stop_frac']}"
        )
    if not dasar.stop_hormati_celah or dasar.maks_biaya_masuk_R <= 0:
        raise ValueError("dua pengaman dasar_riset tidak terpasang")

    dasar_as = replace(dasar, maks_umur_bar=UMUR_SEL_STOP, pakai_target=True)
    jen = jendela_bar(a.interval)
    opsi = opsi_seed(a, jen)
    if opsi.sampel_permutasi != 0:
        raise ValueError("gerbang entri_acak wajib mati di Jalur B")

    print(f"Jalur B pecahan [{a.seed_awal}, {a.seed_akhir}): {len(seed)} seed", flush=True)
    print(f"nama laporan antara: {NAMA_SPEK} (ditimpa tiap seed, TIDAK dikomit)", flush=True)
    print(
        "GERBANG entri_acak MATI (sampel_permutasi=0): ia akan menjalankan "
        f"{MIN_ULANGAN} permutasi di dalam SETIAP seed untuk angka yang jalur "
        "ini tidak pakai. Sepuluh gerbang lain tetap dinilai.",
        flush=True,
    )
    print(
        f"geometri sel AS dibekukan: pakai_target {dasar_as.pakai_target}, "
        f"maks_umur_bar {dasar_as.maks_umur_bar} bar 4h; satu-satunya yang "
        "berbeda antar run adalah seed",
        flush=True,
    )
    print(f"bar dibutuhkan satu jendela: {bar_dibutuhkan(a.interval)}", flush=True)
    print(f"PEMBATAS: {PEMBATAS}", flush=True)
    if SEED_PERMUTASI in seed:
        print(
            f"R-D5 aktif di pecahan ini: seed {SEED_PERMUTASI} WAJIB "
            f"mereproduksi {EKSPEKTASI_AS_SEED42!r} (toleransi {TOLERANSI_SEED42})",
            flush=True,
        )

    ktx = muat_konteks(opsi, dasar_as)
    if opsi.sampel_permutasi == 0 and ktx.sampel:
        raise ValueError(
            f"sampel permutasi tidak kosong ({len(ktx.sampel)}); gerbang "
            "entri_acak masih akan berjalan"
        )

    # Kesetaraan diperiksa atas bingkai SUNGGUHAN, bukan hanya sintetis.
    kunci_bingkai = sorted(ktx.bingkai)
    periksa_kesetaraan(ktx.bingkai[kunci_bingkai[0]], kandidat()[0])
    print(
        f"sinyal_acak_seed(42) identik dengan sinyal_acak pada {kunci_bingkai[0]}",
        flush=True,
    )

    jalur = jalur_pecahan(a.seed_awal, a.seed_akhir, a.out)
    antara = jalur_antara(NAMA_SPEK, a.out)
    Path(a.out).mkdir(parents=True, exist_ok=True)

    baris: list[dict] = []
    r_d5_cocok = None
    for s in seed:
        hasil = jalankan_spek(spek_seed(s, dasar_as, a.komit), ktx, dasar_as, opsi)
        terbaca = baca_bulan(antara)
        baris.append(baris_seed(s, hasil, terbaca))
        print(
            f"seed {s}: ekspektasi {hasil['ekspektasi_R']!r}, "
            f"{hasil['trade']} trade, {len(terbaca['bulan'])} bulan "
            f"({len(terbaca['dibuang'])} dibuang), {hasil.get('detik')} s",
            flush=True,
        )
        if s == SEED_PERMUTASI:
            beda = abs(float(hasil["ekspektasi_R"]) - EKSPEKTASI_AS_SEED42)
            r_d5_cocok = beda <= TOLERANSI_SEED42
            print(
                f"R-D5: seed {s} selisih {beda!r} terhadap sel AS yang dikomit — "
                f"{'TEPAT' if r_d5_cocok else 'MELESET'}",
                flush=True,
            )

        # Ditulis ulang setiap seed selesai: batas 6 jam per pekerjaan tidak
        # boleh menghapus seluruh pekerjaan sebuah pecahan.
        jalur.write_text(
            json.dumps(
                {
                    "hipotesis": "H-013b",
                    "pecahan": [a.seed_awal, a.seed_akhir],
                    "seed_diminta": seed,
                    "seed_selesai": [b["seed"] for b in baris],
                    "selesai": len(baris) == len(seed),
                    "gerbang_entri_acak": "MATI (sampel_permutasi=0)",
                    "satuan_penarikan": "bulan",
                    "r_d5_cocok": r_d5_cocok,
                    "ekspektasi_as_seed42_dikomit": EKSPEKTASI_AS_SEED42,
                    "parameter_beku": {
                        "pakai_target": dasar_as.pakai_target,
                        "maks_umur_bar": dasar_as.maks_umur_bar,
                        "jendela_bar": jen,
                        "pemanasan_bar": PEMANASAN,
                        "min_median_stop_frac": a.min_median_stop_frac,
                        "maks_biaya_masuk_R": dasar_as.maks_biaya_masuk_R,
                        "stop_hormati_celah": dasar_as.stop_hormati_celah,
                    },
                    "pembatas": PEMBATAS,
                    "baris": baris,
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    print(f"\npecahan ditulis: {jalur} ({len(baris)} seed)", flush=True)
    if r_d5_cocok is False:
        print(
            "KODE KELUAR 3: R-D5 meleset. Pecahan tetap ditulis — bukti jangan "
            "dibuang — tetapi sebaran nol ini TIDAK sebanding dengan sel AS yang "
            "sudah dikomit sampai selisihnya dijelaskan.",
            flush=True,
        )
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
