"""H-009 — pengaman carry DIPATOK menyala, bukan dilombakan (ADR-009).

H-008 memasang pengaman carry terealisasi lalu menyerahkan ambangnya kepada
walk-forward. Hasilnya: 334 dari 356 jendela memilih 0,0, yang berarti
mematikan pengaman itu sepenuhnya. Nilai 0,50 tidak pernah dipilih satu kali
pun. Gerbang ``invarian_risiko`` jatuh di angka yang sama persis dengan H-007,
−1,9769R, dan perdagangan terburuk terbukti berjalan dengan pengaman mati.

Buktinya deduktif, bukan tebakan. Perdagangan itu menumpuk carry 0,9228R,
melewati ambang teraktif mana pun di grid, tetapi keluar beralasan ``stop``
dan bukan ``carry``. Kalau pengaman menyala, ia pasti memicu lebih dulu.

Sebabnya struktural, bukan kebetulan. Walk-forward memilih dengan
memaksimalkan ekspektasi dalam sampel. ``invarian_risiko`` dinilai setelah
pemilihan selesai dan tidak pernah masuk fungsi tujuan. Pengaman risiko
memotong posisi sebelum sempat pulih, jadi ia memakan ekspektasi, jadi
pemaksimal ekspektasi akan selalu mematikannya bila diberi pilihan.

Maka H-009 tidak mengubah mekanismenya sama sekali. Yang diubah hanya siapa
yang memutuskan. Ambang dipatok pada 0,25 dan dikeluarkan dari ruang
parameter. Grid kembali persis ke grid H-007.

Mengapa 0,25 dan bukan angka lain: nilai itu sudah tertulis di
``config/lux.yaml`` versi 2 sebagai ``risiko.maks_carry_R`` sejak ADR-004,
ditetapkan sebelum H-002 dijalankan. Ia bukan nilai yang menang setelah hasil
terlihat — di H-008 ia justru kalah telak, 22 lawan 334.

``lux/strategi/`` tidak disentuh, sama seperti H-007 dan H-008.

Pemakaian:
    python -m lux.backtest.run_h009 --dir aset --limit 40
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import replace
from pathlib import Path

from lux.backtest.engine import Konfig
from lux.backtest.run_h002 import hipotesis_h002, muat_konfig_h002
from lux.backtest.run_h007 import IMBALAN as IMBALAN_H007
from lux.backtest.run_h007 import LOOKBACK as LOOKBACK_H007
from lux.backtest.runner import Opsi, Spek, jalankan_spek, muat_konteks
from lux.praregistrasi import Hipotesis, Kriteria
from lux.strategi import breakout_atr

# Disalin dari H-007 lewat impor, bukan diketik ulang. Menyalin dengan tangan
# membuka peluang grid menyempit diam-diam ke arah nilai yang sudah diketahui
# menang; mengimpornya membuat penyempitan itu mustahil secara konstruksi.
# list() dipakai supaya modul ini tidak berbagi objek yang sama dengan H-007.
LOOKBACK = list(LOOKBACK_H007)
IMBALAN = list(IMBALAN_H007)

# Konstanta, bukan sumbu parameter. Inilah keseluruhan isi ADR-009.
# Asalnya config/lux.yaml v2 (ADR-004), ditetapkan sebelum H-002 dijalankan.
AMBANG_CARRY_KERAS = 0.25

# Disalin kata per kata dari hipotesis_h002. Diuji kesamaannya.
DATASET = (
    "tier-b-v1 ohlcv_1h + funding_shard, "
    "universe_layak_v2 438 simbol (ADR-003, ekor datar dipangkas)"
)

# Kunci yang HARAM muncul di kandidat. Bila ia muncul, pemilih kembali
# memegang keputusan risiko dan percobaan ini kehilangan seluruh maknanya.
KUNCI_TERLARANG = "maks_carry_realisasi_R"


def kandidat() -> list[dict]:
    """Grid H-007 apa adanya: hanya lookback dan imbalan yang dipilih."""
    return [
        {"lookback": lb, "imbalan_R": im} for lb in LOOKBACK for im in IMBALAN
    ]


def buat_konfig(params: dict, dasar: Konfig) -> Konfig:
    """Imbalan berasal dari kandidat; pengaman carry TIDAK.

    Ambang dipasang dari konstanta modul untuk setiap kandidat tanpa kecuali,
    sehingga tidak ada satu pun jendela yang bisa menjalankan strategi ini
    dengan pengaman mati. Saringan proyeksi ADR-004 tetap diwarisi menyala.
    """
    if KUNCI_TERLARANG in params:
        raise ValueError(
            f"{KUNCI_TERLARANG} adalah batas risiko, bukan parameter (ADR-009)"
        )
    return replace(
        dasar,
        imbalan_R=float(params["imbalan_R"]),
        maks_carry_realisasi_R=AMBANG_CARRY_KERAS,
    )


def hipotesis_h009(konfig: Konfig, komit: str = "") -> Hipotesis:
    return Hipotesis(
        id="H-009",
        pernyataan=(
            "Dengan sinyal Donchian yang tidak diubah dan grid H-007 yang tidak "
            "diubah, memaksa keluar saat carry TEREALISASI melewati 0,25R — "
            "ambang yang dipatok konstan dan sengaja dikeluarkan dari ruang "
            "parameter — membuat gerbang invarian_risiko lulus. H-008 gagal "
            "bukan karena mekanismenya keliru melainkan karena pemilih yang "
            "memaksimalkan ekspektasi selalu mematikan pengaman yang memakan "
            "ekspektasi. Batas risiko karena itu tidak boleh dilombakan."
        ),
        dataset=DATASET,
        ruang_parameter={
            "lookback": LOOKBACK,
            "imbalan_R": IMBALAN,
            # Ditulis sebagai daftar berisi satu nilai supaya ia ikut ke dalam
            # sidik hipotesis. Menjalankan ulang dengan ambang lain akan
            # menghasilkan sidik berbeda dan tertolak pra-registrasi.
            KUNCI_TERLARANG: [AMBANG_CARRY_KERAS],
            "atr_pengali_stop": [konfig.atr_pengali_stop],
            "maks_umur_bar": [konfig.maks_umur_bar],
            "maks_carry_R": [konfig.maks_carry_R],
            "jendela_carry_hari": [konfig.jendela_carry_hari],
        },
        # Kriteria tidak berubah sedikit pun dari H-002, H-007, dan H-008.
        # Melonggarkannya sekarang, setelah tahu pengaman ini memakan
        # ekspektasi, adalah bentuk kecurangan yang paling mudah dibela.
        kriteria=Kriteria(
            min_ekspektasi_R=0.05,
            min_trade_luar_sampel=100,
            maks_p_entri_acak=0.05,
            min_jendela_positif_rasio=0.5,
        ),
        komit=komit,
    )


def spek_h009(konfig: Konfig, komit: str = "") -> Spek:
    return Spek(
        h=hipotesis_h009(konfig, komit),
        sinyal=breakout_atr.sinyal,
        kandidat=kandidat(),
        nama="h009_carry_dipatok",
        params_lookahead={"lookback": 55},
        buat_konfig=buat_konfig,
    )


# Pembanding tetap, disalin dari laporan yang sudah dikomit. Tidak satu pun
# dijalankan ulang.
PEMBANDING = {
    "H-007": (0.04044, "invarian_risiko -1.9769"),
    "H-008": (0.04126, "invarian_risiko -1.9769"),
}

# Ditulis sebelum run, sama seperti di ADR-009. Ramalan ketiga sengaja
# merugikan hipotesis ini sendiri: bila pengaman bekerja, ia menutup posisi
# yang sebagian akan pulih, jadi ekspektasi WAJIB turun. Kalau ternyata naik,
# yang patut dicurigai adalah pengamannya tidak benar-benar memicu.
RAMALAN = {
    "keluar_carry": "melonjak dari 2 ke ratusan",
    "kerugian_terburuk_R": "lebih kecil dari 1,5 sehingga invarian_risiko lulus",
    "ekspektasi_R": "turun di bawah 0,04126 milik H-008",
}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--interval", default="1h")
    ap.add_argument("--universe", default="reports/universe_layak_v2.json")
    ap.add_argument("--akhir-sejati", default="reports/akhir_sejati.json")
    ap.add_argument("--config", default="config/lux.yaml")
    ap.add_argument("--out", default="reports")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--ulangan", type=int, default=100)
    ap.add_argument("--komit", default="")
    a = ap.parse_args(argv)

    konfig = muat_konfig_h002(Path(a.config))

    # Seluruh pemeriksaan di bawah ini berjalan sebelum satu bar pun dimuat.
    # Pemeriksaan yang bisa gagal tidak boleh diletakkan di ujung run panjang.
    if hipotesis_h009(konfig).dataset != hipotesis_h002(konfig).dataset:
        raise ValueError("dataset H-009 tidak identik dengan H-002")

    if konfig.maks_carry_R <= 0:
        raise ValueError("H-009 menuntut saringan ADR-004 tetap menyala")

    if LOOKBACK != list(LOOKBACK_H007) or IMBALAN != list(IMBALAN_H007):
        raise ValueError("grid H-009 wajib identik dengan H-007")

    for p in kandidat():
        if KUNCI_TERLARANG in p:
            raise ValueError(f"{KUNCI_TERLARANG} bocor ke ruang pencarian")

    if AMBANG_CARRY_KERAS <= 0:
        raise ValueError("ambang carry keras wajib menyala di H-009")

    opsi = Opsi(
        dir_aset=Path(a.dir),
        out=Path(a.out),
        interval=a.interval,
        universe=Path(a.universe),
        akhir_sejati=Path(a.akhir_sejati),
        limit=a.limit,
        ulangan=a.ulangan,
    )

    print(f"ADR-004 proyeksi: maks_carry_R={konfig.maks_carry_R}", flush=True)
    print(
        f"ADR-009 ambang carry keras DIPATOK: {AMBANG_CARRY_KERAS} "
        f"(bukan parameter, tidak dilombakan)",
        flush=True,
    )
    print(f"kandidat: {len(kandidat())} kombinasi", flush=True)
    for id_, (eks, gerbang) in PEMBANDING.items():
        print(f"  pembanding {id_}: {eks:+.5f}R, gerbang gagal: {gerbang}", flush=True)
    for nama, isi in RAMALAN.items():
        print(f"  ramalan {nama}: {isi}", flush=True)

    ktx = muat_konteks(opsi)
    hasil = jalankan_spek(spek_h009(konfig, a.komit), ktx, konfig, opsi)

    keluar = hasil["alasan_keluar"]
    print(f"\nkeluar karena pengaman carry: {keluar.get('carry', 0)}", flush=True)
    print(f"gerbang gagal: {hasil['gerbang_gagal']}", flush=True)
    print(
        f"ekspektasi {hasil['ekspektasi_R']} vs H-008 {PEMBANDING['H-008'][0]}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
