"""Runner bersama untuk keluarga hipotesis (ADR-006, diperluas ADR-007, ADR-010, ADR-011, ADR-013, ADR-014).

ADR-005 mensyaratkan ekstraksi ini sebelum orkestrator keempat dibuat, dan
syaratnya dipenuhi di sini. Tiga orkestrator lama — ``run_wf`` (H-001b),
``run_h002``, ``run_h003`` — **tidak disentuh**, sehingga angka lama tetap dapat
diulang. Modul ini mengimpor fungsi penilaian dari ``run_wf`` seperti mereka,
jadi seluruh hipotesis dinilai oleh kode yang sama.

Data dimuat sekali untuk seluruh keluarga. Selain hemat waktu, itu menjamin
semua hipotesis melihat kumpulan berkas yang identik, sehingga gerbang
``checksum`` cukup dinilai sekali dan perbandingan antar hipotesis sah.

Sejak ADR-007, sebuah ``Spek`` boleh membawa ``buat_konfig`` sehingga parameter
keluar ikut dipilih walk-forward. Uji permutasi memakai konfig milik masing-
masing jendela, bukan konfig dasar, agar yang dibandingkan benar-benar wilayah
penilaian yang sama.

Sejak ADR-010 runner menilai gerbang kesepuluh, ``konsentrasi``, dari agregat
per simbol dan menulis tabel jackknife ke laporan. Agregat yang dipakai adalah
``ringkasan_simbol`` yang belum dibulatkan, bukan blok ``per_simbol`` yang
dibulatkan ke empat desimal untuk keperluan pembacaan manusia.

Sejak ADR-011 runner menilai gerbang kesebelas, ``funding_ekor``, dari
pembongkaran per perdagangan yang sama dengan ``diagnosa_biaya`` — keduanya
memakai ``rincian_R``, sehingga angka gerbang dapat diperiksa tangan terhadap
blok ``diagnosa_biaya.terburuk`` di laporan yang sama.

Sejak ADR-013 runner menulis **sebaran R dan galat baku ekspektasi**. Sampai
H-010 laporan hanya memuat rerata, sehingga tidak ada satu pun dari sepuluh
hipotesis — termasuk yang lulus — yang dapat dinilai secara statistik: mustahil
mengatakan apakah 0,053028R berbeda secara berarti dari 0,041359R atau dari
ambang 0,05R. Perhitungannya berdiri di ``lux.analisis.sebaran`` karena
``ringkas_gabungan`` berada di ``run_wf`` yang dibekukan. Ambang pembandingnya
diambil dari ``spek.h.kriteria.min_ekspektasi_R``, bukan diketik ulang, supaya
angka ambang tetap hidup di satu tempat saja.

ADR-014 MENAMBAHKAN TIGA HAL, DAN HANYA TIGA
--------------------------------------------
**Pertama, penolakan pengaman biaya masuk ikut ditulis ke laporan** sebagai
alasan tersendiri. Penolakan **bukan perdagangan**, jadi ia haram masuk
histogram ``alasan_keluar``; tanpa baris sendiri ia hilang tanpa jejak, dan
saringan yang membuang entri tanpa jejak adalah titik buta yang sama jenisnya
dengan gerbang yang hasilnya tidak pernah ditulis ke ``reports/``.

Angka itu wajib ditafsirkan dengan satu peringatan yang sudah dibayar: pada
simbol yang **seluruhnya** degenerat, pengaman menolak entri juga saat
pemilihan parameter, sehingga semua kandidat berskor ``-inf`` dan seluruh
jendelanya dilewati. Simbol semacam itu menyumbang **nol** penolakan dan nol
perdagangan. Jadi angka ini hanya menghitung simbol yang berubah degenerat di
tengah jalan; yang membuat simbol degenerat total terlihat hanyalah lantai
semesta.

**Kedua, lantai semesta.** ``muat_konteks`` menyaring simbol yang median
``stop_frac``-nya di bawah lantai lewat ``lux.degenerasi.saring_semesta``.
Medan ``Opsi.min_median_stop_frac`` bawaannya **0.0 yang berarti MATI**, dengan
alasan yang sama seperti empat saringan mesin: hasil H-001b sampai H-011 harus
tetap dapat diulang, dan itu hanya mungkin bila runner bawaannya tidak
menyaring apa pun. Ambangnya **tidak diketik di modul ini**; pemanggil
menyerahkannya, dan pemanggil mengambilnya dari ``lux.degenerasi``.

Simbol yang dibuang **wajib tertulis di laporan beserta median
``stop_frac``-nya**. Semesta yang menyusut tanpa catatan adalah penyubsetan
simbol yang tidak dapat dibedakan dari kecurangan ketika laporannya dibaca
setahun kemudian.

**Ketiga, agregat per bulan masuk.** Laporan sampai H-011 tidak memuat satu pun
stempel waktu perdagangan, sehingga kriteria utama H-012 — ekspektasi pada
periode waktu terakhir yang dibekukan — mustahil dihitung dari laporan yang
dikomit. Blok ``agregat_periode`` menutup lubang itu. Ia hanya membaca ulang
perdagangan yang sama menurut bulan kalender UTC waktu **masuk**; tidak ada
ambang, putusan, maupun perilaku mesin yang tersentuh olehnya.

ADR-019 MENGUBAH SATU BARIS
---------------------------
Gerbang ``forward_fill`` kini dipanggil dengan ``interval=opsi.interval``,
sehingga ambang deret bar datarnya berarti **satu hari** alih-alih 24 bar apa pun
intervalnya. Pada 1h tidak ada yang berubah sedikit pun, sebab
``bar_per_hari("1h")`` sama dengan bawaan lama; pada 4h ambangnya menjadi 6 bar,
dan tanpa itu keheningan tiga hari penuh lolos sebagai data bersih.

Ambang yang diserahkan ke ``gabung_gerbang`` tetap ``0.30`` dan itu disengaja:
0,30 adalah ambang **rasio** bar datar, bukan ambang **deret**. Keduanya syarat
yang berbeda pada gerbang yang sama.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd

from lux.analisis.periode import agregat_per_bulan
from lux.analisis.periode import dari_perdagangan as pasangan_periode
from lux.analisis.sebaran import (
    KUNCI as KUNCI_SEBARAN,
    dari_perdagangan,
    jarak_ambang,
    ukur_sebaran,
)
from lux.backtest.engine import Hasil, Konfig, atr, jalankan
from lux.backtest.funding_ekor import (
    dari_rincian,
    gerbang_funding_ekor,
    tabel_ekor_funding,
    ukur_funding_ekor,
)
from lux.backtest.gerbang import (
    Gerbang,
    gerbang_buy_and_hold,
    gerbang_checksum,
    gerbang_entri_acak,
    gerbang_forward_fill,
    gerbang_funding,
    gerbang_invarian_risiko,
    gerbang_lookahead,
    gerbang_survivorship,
    susun_laporan,
)
from lux.backtest.konsentrasi import (
    dari_ringkasan,
    gerbang_konsentrasi,
    tabel_jackknife,
)
from lux.backtest.run_wf import (
    akhir_per_simbol,
    diagnosa_biaya,
    gabung_gerbang,
    gerbang_bnh_gabungan,
    gerbang_overlap_gabungan,
    muat_ohlcv,
    rincian_R,
    ringkas_gabungan,
    sha256_berkas,
    simbol_mati_dari_akhir,
)
from lux.backtest.walk_forward import jalankan_walk_forward
from lux.degenerasi import median_stop_frac, saring_semesta
from lux.funding_model import ambil_jadwal, muat_jadwal
from lux.praregistrasi import Hipotesis, nilai, simpan


@dataclass
class Opsi:
    """Parameter run yang berlaku sama untuk seluruh keluarga.

    Nilai bawaannya sengaja sama persis dengan H-002 dan H-003. Mengubah salah
    satunya membuat perbandingan antar hipotesis tidak sah.
    """

    dir_aset: Path
    out: Path = Path("reports")
    interval: str = "1h"
    universe: Path = Path("reports/universe_layak_v2.json")
    akhir_sejati: Path = Path("reports/akhir_sejati.json")
    limit: int = 40
    panjang_latih: int = 4320
    panjang_uji: int = 2160
    embargo: int = 168
    pemanasan: int = 200
    ulangan: int = 100
    sampel_permutasi: int = 10
    # ADR-014. Nol berarti MATI, dan medan ini diletakkan paling akhir dengan
    # alasan yang sama seperti medan Konfig baru: posisi argumen medan lama
    # tidak boleh bergeser, dan hasil sebelas hipotesis lama harus tetap dapat
    # diulang tanpa satu simbol pun tersaring.
    min_median_stop_frac: float = 0.0


@dataclass
class Konteks:
    """Data yang dimuat sekali dan dipakai seluruh keluarga."""

    bingkai: dict[str, pd.DataFrame]
    jadwal: dict
    akhir: dict
    semesta: list[str]
    sampel: set[str]
    gerbang_cs: Gerbang
    semesta_layak: list[str]
    mati: list[str]
    # ADR-014. Hasil lengkap lantai semesta, atau None bila lantai mati.
    # Dibawa sampai ke laporan supaya semesta yang menyusut selalu punya
    # penjelasan yang dapat diperiksa tangan.
    saringan: dict | None = None


@dataclass
class Spek:
    """Satu hipotesis beserta sinyalnya."""

    h: Hipotesis
    sinyal: Callable[[pd.DataFrame, dict], np.ndarray]
    kandidat: list[dict]
    nama: str
    params_lookahead: dict = field(default_factory=dict)
    # ADR-007: bila diisi, tiap kandidat membawa Konfig sendiri sehingga
    # parameter keluar ikut dipilih di dalam sampel.
    buat_konfig: Callable[[dict, Konfig], Konfig] | None = None


def median_stop_frac_bingkai(
    df: pd.DataFrame, konfig: Konfig | None = None
) -> float | None:
    """Median jarak stop satu simbol sepanjang riwayatnya, atau ``None``.

    ATR dihitung oleh ``engine.atr``, bukan oleh salinan di sini, dan aritmetika
    medannya diserahkan ke ``lux.degenerasi``. Dua implementasi dari besaran yang
    sama adalah cara paling andal melahirkan selisih yang tidak terdeteksi
    siapa pun.

    Satu ketidaktepatan yang disengaja dan wajib diketahui: mesin menentukan
    ukuran posisi dari ATR bar ``t-1`` terhadap harga **pembukaan** bar ``t``
    yang sudah diberi slippage, sedangkan di sini ATR bar ``t`` dibagi harga
    **penutupan** bar ``t``. Selisihnya berorde satu bar dan satu slippage,
    yakni per mil. Kriteria yang dinilai berselisih tiga orde besaran
    (3,2e-06 terhadap 4e-03), jadi ketidaktepatan ini tidak dapat memindahkan
    satu simbol pun melewati lantai. Ia tetap dicatat di sini alih-alih
    dibiarkan tersembunyi.
    """
    k = konfig or Konfig()
    wajib = ("high", "low", "close")
    kurang = [c for c in wajib if c not in df.columns]
    if kurang:
        raise ValueError(f"kolom wajib hilang: {kurang}")
    if len(df) == 0:
        return None
    h = df["high"].to_numpy(dtype="float64")
    l = df["low"].to_numpy(dtype="float64")
    c = df["close"].to_numpy(dtype="float64")
    a = atr(h, l, c, k.atr_periode)
    return median_stop_frac(a, c, k.atr_pengali_stop)


def saring_bingkai(
    bingkai: dict[str, pd.DataFrame],
    ambang: float,
    konfig: Konfig | None = None,
) -> tuple[dict[str, pd.DataFrame], dict]:
    """Buang simbol yang satuan risikonya runtuh, dengan alasan tercatat.

    Putusannya seluruhnya milik ``lux.degenerasi.saring_semesta``; fungsi ini
    hanya menyiapkan medannya dan membuang bingkai yang ditolak. Tidak ada nama
    simbol yang diperlakukan istimewa di sini, karena degenerasi dibuktikan oleh
    ``stop_frac`` dan bukan oleh ejaan (saringan nama naif sempat menandai
    ``BUSDT`` dan ``TUSDT``).
    """
    if ambang <= 0:
        raise ValueError("ambang lantai stop harus positif")
    medan = {
        s: median_stop_frac_bingkai(bingkai[s], konfig) for s in sorted(bingkai)
    }
    hasil = saring_semesta(medan, ambang)
    layak = set(hasil["layak"])
    tersisa = {s: bingkai[s] for s in sorted(bingkai) if s in layak}
    return tersisa, hasil


def muat_konteks(opsi: Opsi, konfig: Konfig | None = None) -> Konteks:
    semesta = json.loads(Path(opsi.universe).read_text(encoding="utf-8"))["simbol"]
    dipilih = sorted(semesta)[: opsi.limit] if opsi.limit > 0 else sorted(semesta)
    print(f"universe layak {len(semesta)}, diuji {len(dipilih)}", flush=True)

    bingkai, berkas = muat_ohlcv(Path(opsi.dir_aset), opsi.interval, set(dipilih))
    jadwal = muat_jadwal(Path(opsi.dir_aset))
    akhir = akhir_per_simbol(
        Path(opsi.dir_aset), opsi.interval, Path(opsi.akhir_sejati)
    )
    print(
        f"{len(bingkai)} simbol dimuat, {len(jadwal)} jadwal funding, "
        f"{len(akhir)} simbol dipindai untuk survivorship",
        flush=True,
    )

    # Checksum dinilai sekali: berkasnya sama untuk seluruh keluarga. Dinilai
    # atas SELURUH berkas yang benar-benar dibaca, termasuk berkas simbol yang
    # sebentar lagi dibuang lantai. Yang dijaga gerbang ini adalah keutuhan
    # data yang disentuh, bukan keanggotaan semesta.
    manifest_path = Path(opsi.out) / "manifest_aset.json"
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
            "tidak dapat dinilai: manifest baru ditulis pada run ini",
        )
    print(f"checksum: {gerbang_cs.catatan}", flush=True)

    # ADR-014: lantai satuan R sebagai kriteria kelayakan semesta. Simbol yang
    # ditolak keluar dari semesta seluruhnya, bukan hanya dari pengujian, sebab
    # ia memang tidak layak diuji dan bukan sekadar tidak diuji kali ini.
    saringan: dict | None = None
    if opsi.min_median_stop_frac > 0:
        sebelum = len(bingkai)
        bingkai, saringan = saring_bingkai(
            bingkai, opsi.min_median_stop_frac, konfig
        )
        dibuang = {b["symbol"] for b in saringan["ditolak"]}
        semesta = [s for s in semesta if s not in dibuang]
        print(
            f"lantai median stop_frac {opsi.min_median_stop_frac}: "
            f"{saringan['n_layak']} layak, {saringan['n_ditolak']} dibuang "
            f"dari {sebelum} simbol dimuat",
            flush=True,
        )
        for b in saringan["ditolak"]:
            m = b["median_stop_frac"]
            print(
                f"  DIBUANG {b['symbol']}: median_stop_frac "
                f"{'-' if m is None else format(m, '.6e')}, {b['sebab']}",
                flush=True,
            )
    else:
        print("lantai median stop_frac: MATI", flush=True)

    semesta_layak = [s for s in semesta if s in akhir]
    mati = simbol_mati_dari_akhir({s: akhir[s] for s in semesta_layak})

    return Konteks(
        bingkai=bingkai,
        jadwal=jadwal,
        akhir=akhir,
        semesta=semesta,
        sampel=set(sorted(bingkai)[: opsi.sampel_permutasi]),
        gerbang_cs=gerbang_cs,
        semesta_layak=semesta_layak,
        mati=mati,
        saringan=saringan,
    )


def jalankan_spek(
    spek: Spek, ktx: Konteks, konfig: Konfig, opsi: Opsi
) -> dict:
    """Menjalankan satu hipotesis sampai putusan dan menulis laporannya."""
    t0 = time.time()
    jalur = simpan(spek.h, f"hipotesis/{spek.h.id}.json")
    print(
        f"\n=== {spek.h.id} terdaftar di {jalur} (sidik {spek.h.sidik()[:12]}, "
        f"{spek.h.jumlah_kombinasi} kombinasi) ===",
        flush=True,
    )

    ringkasan_simbol: list[dict] = []
    per_simbol: list[dict] = []
    semua_trade = []
    hasil_per_simbol: dict[str, Hasil] = {}
    jendela_sampel: list[tuple[pd.DataFrame, np.ndarray, str, Konfig]] = []
    g_forward: list[Gerbang] = []
    nama_forward: list[str] = []
    g_bnh: list[Gerbang] = []
    parameter_terpilih: dict[str, int] = {}

    for i, s in enumerate(sorted(ktx.bingkai), 1):
        df = ktx.bingkai[s]
        try:
            jadwal = ambil_jadwal(ktx.jadwal, s)
        except KeyError as e:
            print(f"  [{i}] {s}: DILEWATI, {e}", flush=True)
            continue

        wf = jalankan_walk_forward(
            df,
            kandidat=spek.kandidat,
            buat_sinyal=spek.sinyal,
            panjang_latih=opsi.panjang_latih,
            panjang_uji=opsi.panjang_uji,
            embargo=opsi.embargo,
            pemanasan=opsi.pemanasan,
            konfig=konfig,
            jadwal=jadwal,
            symbol=s,
            simpan_bingkai=s in ktx.sampel,
            buat_konfig=spek.buat_konfig,
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
                # ADR-014. Per simbol, supaya penolakan yang menumpuk di satu
                # simbol tidak menyamar sebagai penolakan yang merata.
                "entri_ditolak_biaya": r["entri_ditolak_biaya"],
                "parameter": r["parameter_per_jendela"],
            }
        )

        # Berapa sering tiap kandidat terpilih. Parameter yang meloncat-loncat
        # berarti tidak ada yang stabil untuk ditemukan.
        for p in r["parameter_per_jendela"]:
            kunci = json.dumps(p, sort_keys=True, ensure_ascii=False)
            parameter_terpilih[kunci] = parameter_terpilih.get(kunci, 0) + 1

        # ADR-019. Interval dipasok supaya ambang deret bar datar berarti satu
        # HARI, bukan 24 bar. Untuk 1h nilainya tetap 24 sehingga hasil lama
        # tidak bergeser; untuk 4h ia menjadi 6.
        g_forward.append(gerbang_forward_fill(df, interval=opsi.interval))
        nama_forward.append(s)

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
                jendela_sampel.append(
                    (hj.bingkai_uji, hj.sinyal_uji, s, hj.konfig or konfig)
                )

        if i % 10 == 0 or i == len(ktx.bingkai):
            print(
                f"  [{i}/{len(ktx.bingkai)}] {s}: "
                f"{r['jumlah_trade_luar_sampel']} trade, {time.time() - t0:.0f}s",
                flush=True,
            )

    gabungan = ringkas_gabungan(ringkasan_simbol)
    diagnosa = diagnosa_biaya(semua_trade)
    alasan: dict[str, int] = {}
    for p in semua_trade:
        alasan[p.alasan_keluar] = alasan.get(p.alasan_keluar, 0) + 1

    # ADR-014. Penolakan pengaman biaya BUKAN perdagangan, jadi ia sengaja
    # tidak dijumlahkan ke dalam ``alasan`` di atas: mencampurnya akan membuat
    # histogram alasan keluar berbohong tentang jumlah perdagangan. Ia berdiri
    # sebagai angkanya sendiri.
    entri_ditolak_biaya = sum(r["entri_ditolak_biaya"] for r in ringkasan_simbol)
    simbol_dengan_penolakan = sorted(
        (
            {"symbol": r["symbol"], "entri_ditolak_biaya": r["entri_ditolak_biaya"]}
            for r in ringkasan_simbol
            if r["entri_ditolak_biaya"] > 0
        ),
        key=lambda b: -b["entri_ditolak_biaya"],
    )

    # ADR-014. Agregat menurut bulan kalender UTC waktu MASUK. Ditulis ke
    # laporan karena kriteria utama H-012 adalah ekspektasi pada periode waktu
    # terakhir yang dibekukan, dan kriteria utama wajib dapat dihitung ulang
    # dari berkas yang dikomit — bukan dari nilai yang beredar di memori run.
    agregat_periode = agregat_per_bulan(pasangan_periode(semua_trade))

    # ADR-013. Nilai R tidak finit adalah cacat mesin dan wajib berbunyi, tetapi
    # bunyinya ditulis ke laporan alih-alih melempar galat: menaruh pemeriksaan
    # yang bisa gagal di UJUNG run panjang berarti membuang seluruh komputasi
    # yang sudah selesai. Aturan itu sudah dibayar mahal sebelumnya.
    try:
        sebaran = ukur_sebaran(dari_perdagangan(semua_trade))
    except ValueError as e:
        sebaran = {k: None for k in KUNCI_SEBARAN}
        sebaran["n"] = len(semua_trade)
        sebaran["dapat_dinilai"] = False
        sebaran["sebab"] = f"CACAT MESIN: {e}"
    jarak = jarak_ambang(sebaran, spek.h.kriteria.min_ekspektasi_R)

    # ADR-010. Agregat yang dipakai belum dibulatkan; blok per_simbol di laporan
    # membulatkan ke empat desimal untuk dibaca manusia, dan pembulatan itu
    # tidak perlu diwariskan ke putusan gerbang.
    kontribusi = dari_ringkasan(ringkasan_simbol)
    jackknife = tabel_jackknife(kontribusi)
    g_konsentrasi = gerbang_konsentrasi(kontribusi)

    # ADR-011. Sumbernya rincian_R yang sama dengan diagnosa_biaya, supaya angka
    # gerbang dapat diperiksa tangan terhadap blok terburuk di laporan ini.
    trade_funding = dari_rincian(rincian_R(p) for p in semua_trade)
    ukuran_funding = ukur_funding_ekor(trade_funding)
    ekor_funding = tabel_ekor_funding(trade_funding)
    g_funding_ekor = gerbang_funding_ekor(
        trade_funding, jadwal_dimuat=bool(ktx.jadwal)
    )

    print(json.dumps(gabungan, indent=2), flush=True)
    print(f"alasan keluar: {alasan}", flush=True)
    print(
        f"entri ditolak pengaman biaya: {entri_ditolak_biaya} "
        f"(pengaman {konfig.maks_biaya_masuk_R}R, "
        f"lantai semesta {opsi.min_median_stop_frac})",
        flush=True,
    )
    print(f"bulan dengan perdagangan: {len(agregat_periode)}", flush=True)
    print(f"parameter terpilih: {parameter_terpilih}", flush=True)
    print(f"konsentrasi: {g_konsentrasi.catatan}", flush=True)
    print(f"funding ekor: {g_funding_ekor.catatan}", flush=True)
    if sebaran["dapat_dinilai"]:
        print(
            f"sebaran: std {sebaran['std_R']:.5f}R, galat baku "
            f"{sebaran['galat_baku_R']:.6f}R, jarak ke ambang "
            f"{jarak['jarak_R']:+.6f}R"
            + (
                f" = {jarak['jarak_galat_baku']:+.2f} galat baku"
                if jarak["jarak_galat_baku"] is not None
                else ""
            ),
            flush=True,
        )
    else:
        print(f"sebaran: tidak dapat dinilai, {sebaran['sebab']}", flush=True)

    hasil_pool = Hasil(
        symbol="POOL",
        perdagangan=semua_trade,
        ekuitas=np.array([konfig.modal_awal]),
    )

    gerbang_ff = gabung_gerbang("forward_fill", g_forward, 0.30, nama_forward)
    gerbang_bnh = gerbang_bnh_gabungan(g_bnh)

    p_acak: float | None = None
    if jendela_sampel:
        panjang = [len(s_) for _, s_, _, _ in jendela_sampel]
        batas = np.cumsum([0] + panjang)
        sinyal_gabung = np.concatenate([s_ for _, s_, _, _ in jendela_sampel])

        def penilai(sinyal_acak: np.ndarray) -> float:
            rs = []
            for k, (bingkai_j, _, sym, konfig_j) in enumerate(jendela_sampel):
                potong = sinyal_acak[batas[k] : batas[k + 1]]
                hasil_j = jalankan(
                    bingkai_j,
                    potong,
                    konfig_j,
                    jadwal=ktx.jadwal.get(sym),
                    symbol=sym,
                )
                rs.extend(p.R for p in hasil_j.perdagangan)
            return float(np.mean(rs)) if rs else float("-inf")

        nyata = penilai(sinyal_gabung)
        gerbang_acak = gerbang_entri_acak(
            nyata, sinyal_gabung, penilai, ulangan=opsi.ulangan
        )
        p_acak = gerbang_acak.nilai
        print(f"entri acak: nyata {nyata:.5f}R, p {p_acak}", flush=True)
    else:
        gerbang_acak = Gerbang(
            "entri_acak",
            False,
            None,
            None,
            "tidak dapat dinilai: tidak ada jendela sampel",
        )

    if ktx.bingkai:
        contoh = ktx.bingkai[sorted(ktx.bingkai)[0]]
        gerbang_la = gerbang_lookahead(
            contoh.iloc[:5000], lambda d: spek.sinyal(d, spek.params_lookahead)
        )
    else:
        gerbang_la = Gerbang(
            "lookahead", False, None, None, "tidak dapat dinilai: tidak ada data"
        )

    laporan = susun_laporan(
        [
            gerbang_ff,
            gerbang_bnh,
            gerbang_acak,
            gerbang_la,
            gerbang_invarian_risiko(hasil_pool),
            gerbang_funding(hasil_pool, jadwal_dimuat=bool(ktx.jadwal)),
            gerbang_overlap_gabungan(hasil_per_simbol),
            ktx.gerbang_cs,
            gerbang_survivorship(
                simbol_diuji=[r["symbol"] for r in ringkasan_simbol],
                simbol_delisted=ktx.mati,
                simbol_universe=ktx.semesta_layak,
            ),
            g_konsentrasi,
            g_funding_ekor,
        ]
    )
    putusan = nilai(spek.h, gabungan, p_acak)

    isi = {
        "hipotesis": spek.h.ke_dict() | {"sidik": spek.h.sidik()},
        "parameter_run": {
            "interval": opsi.interval,
            "limit": opsi.limit,
            "panjang_latih": opsi.panjang_latih,
            "panjang_uji": opsi.panjang_uji,
            "embargo": opsi.embargo,
            "pemanasan": opsi.pemanasan,
            "ulangan_permutasi": opsi.ulangan,
            "maks_umur_bar": konfig.maks_umur_bar,
            "maks_carry_R": konfig.maks_carry_R,
            "jendela_carry_hari": konfig.jendela_carry_hari,
            "maks_carry_realisasi_R": konfig.maks_carry_realisasi_R,
            # ADR-014. Dua angka yang wajib terlihat di laporan, karena tanpa
            # keduanya mustahil membedakan run yang lantainya menyala dari run
            # yang lantainya mati.
            "maks_biaya_masuk_R": konfig.maks_biaya_masuk_R,
            "min_median_stop_frac": opsi.min_median_stop_frac,
            "konfig_per_kandidat": spek.buat_konfig is not None,
        },
        "gabungan": gabungan,
        "alasan_keluar": alasan,
        # ADR-014: alasannya sendiri, di samping alasan_keluar dan
        # diagnosa_biaya, bukan di dalam salah satunya.
        "entri_ditolak_biaya": entri_ditolak_biaya,
        "entri_ditolak_biaya_per_simbol": simbol_dengan_penolakan,
        "lantai_semesta": ktx.saringan,
        "agregat_periode": agregat_periode,
        "parameter_terpilih": parameter_terpilih,
        "diagnosa_biaya": diagnosa,
        "sebaran": sebaran,
        "jarak_ambang_ekspektasi": jarak,
        "gerbang": laporan.ke_dict(),
        "jackknife": jackknife,
        "ekor_funding": {"ukuran": ukuran_funding, "terburuk": ekor_funding},
        "putusan": {"lulus": putusan.lulus, "alasan": putusan.alasan},
        "per_simbol": per_simbol,
        "detik": round(time.time() - t0, 1),
    }
    out = Path(opsi.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"backtest_{spek.nama}.json").write_text(
        json.dumps(isi, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    md = [
        f"# Backtest {spek.h.id} — {spek.nama}",
        "",
        f"> {spek.h.pernyataan}",
        "",
        f"Sidik `{spek.h.sidik()[:16]}` \u00b7 {spek.h.jumlah_kombinasi} kombinasi "
        f"\u00b7 {gabungan['jumlah_simbol']} simbol \u00b7 {isi['detik']}s",
        "",
        "## Putusan",
        "",
        f"**{'LULUS' if putusan.lulus and laporan.semua_lulus else 'DITOLAK'}**",
        "",
    ]
    if putusan.alasan:
        md += ["Kriteria pra-registrasi yang tidak terpenuhi:", ""]
        md += [f"- {al}" for al in putusan.alasan] + [""]
    if laporan.yang_gagal:
        md += [f"Gerbang gagal: {', '.join(laporan.yang_gagal)}", ""]

    md += [
        "## Hasil luar sampel",
        "",
        f"- Perdagangan: **{gabungan['jumlah_trade_luar_sampel']:,}**",
        f"- Total R: **{gabungan['total_R']:.2f}**",
        f"- Ekspektasi: **{gabungan['ekspektasi_R']}**",
        f"- Jendela positif: {gabungan['jendela_positif']}/{gabungan['jumlah_jendela']}",
        f"- Alasan keluar: {alasan}",
        f"- Entri ditolak pengaman biaya (ADR-014): "
        f"**{entri_ditolak_biaya:,}**, pengaman "
        f"{konfig.maks_biaya_masuk_R}R",
        "",
        "Penolakan pengaman biaya **bukan perdagangan** dan karena itu tidak "
        "muncul di histogram alasan keluar maupun di jumlah perdagangan di "
        "atas. Angka itu juga **tidak** mengukur seluruh keadaan degenerat: "
        "pada simbol yang seluruhnya degenerat, pengaman menolak entri juga "
        "saat pemilihan parameter, sehingga semua kandidat berskor -inf, "
        "seluruh jendelanya dilewati, dan simbol itu menyumbang nol penolakan "
        "sekaligus nol perdagangan. Yang tercatat di sini hanyalah simbol yang "
        "berubah degenerat di tengah jalan; simbol yang degenerat sepanjang "
        "riwayatnya hanya terlihat di lantai semesta di bawah.",
        "",
    ]
    if simbol_dengan_penolakan:
        md += [
            "| Simbol | Entri ditolak |",
            "|---|---|",
        ]
        for b in simbol_dengan_penolakan[:20]:
            md.append(f"| {b['symbol']} | {b['entri_ditolak_biaya']:,} |")
        md += [""]

    md += ["## Lantai satuan R pada semesta (ADR-014)", ""]
    if ktx.saringan is None:
        md += [
            "Lantai **MATI** (`min_median_stop_frac` = "
            f"{opsi.min_median_stop_frac}). Semesta dipakai apa adanya, sama "
            "seperti H-001b sampai H-011.",
            "",
        ]
    else:
        sr = ktx.saringan
        md += [
            f"Lantai median `stop_frac` **{sr['ambang']}**, diturunkan dari "
            "aritmetika biaya dan bukan disetel: biaya bolak-balik 0,002 dari "
            "harga menjadi tepat 0,5R di lantai itu. Kriteria ini seragam dan "
            "dipra-registrasi, sehingga ia bukan penyubsetan simbol "
            "pasca-hasil.",
            "",
            f"- Simbol dinilai: **{sr['n_masuk']}**",
            f"- Layak: **{sr['n_layak']}**",
            f"- Dibuang: **{sr['n_ditolak']}**",
            "",
        ]
        if sr["ditolak"]:
            md += [
                "| Simbol | median stop_frac | biaya masuk R | Sebab |",
                "|---|---|---|---|",
            ]
            for b in sr["ditolak"]:
                m = b["median_stop_frac"]
                bm = b["biaya_masuk_R"]
                md.append(
                    f"| {b['symbol']} "
                    f"| {'\u2014' if m is None else format(m, '.6e')} "
                    f"| {'\u2014' if bm is None else format(bm, '.2f')} "
                    f"| {b['sebab']} |"
                )
            md += [""]
        else:
            md += ["Tidak ada simbol yang dibuang lantai.", ""]

    md += [
        "## Hasil menurut bulan masuk (ADR-014)",
        "",
        "Setiap perdagangan dimiliki oleh bulan kalender UTC tempat ia "
        "**dibuka**, karena keputusan yang diuji adalah keputusan masuk. "
        "Akibatnya ada rembesan yang wajib dinyatakan: perdagangan yang dibuka "
        "sesaat sebelum batas sebuah periode dapat ditutup sesudahnya, dan "
        "besarnya rembesan itu terbatas oleh `maks_umur_bar` "
        f"({konfig.maks_umur_bar} bar).",
        "",
        "Tabel ini **bukan** putusan dan bukan pula izin memilih periode "
        "terbaik sesudah melihatnya. Memilih periode setelah hasil terlihat "
        "adalah penyubsetan yang sama terlarangnya dengan memilih simbol.",
        "",
        "| Bulan masuk | Trade | Total R | Ekspektasi R |",
        "|---|---|---|---|",
    ]
    for b in agregat_periode:
        e = "\u2014" if b["ekspektasi_R"] is None else f"{b['ekspektasi_R']:+.6f}"
        md.append(
            f"| {b['periode']} | {b['trade']:,} | {b['total_R']:+.2f} | {e} |"
        )

    md += [
        "",
        "## Sebaran R dan galat baku (ADR-013)",
        "",
        "Sampai H-010 laporan hanya memuat rerata, sehingga tidak ada hipotesis "
        "yang dapat dinilai secara statistik: mustahil mengatakan apakah "
        "selisih terhadap ambang berarti sesuatu atau tidak.",
        "",
        "**Galat baku di bawah adalah taksiran BAWAH.** Ia mengandaikan "
        "perdagangan saling bebas, dan andaian itu tidak benar: perdagangan "
        "dari puluhan simbol kripto pada jendela waktu yang bertumpang "
        "berkorelasi lewat gerakan pasar bersama. Galat sesungguhnya lebih "
        "besar, jadi keyakinan sesungguhnya lebih kecil. Angka ini sah dipakai "
        "untuk **menjatuhkan** klaim, dan tidak sah dipakai untuk "
        "**menegakkan** klaim.",
        "",
    ]
    if sebaran["dapat_dinilai"]:
        md += [
            f"- Simpangan baku per perdagangan: **{sebaran['std_R']:.5f}R** "
            f"(ddof=1, n = {sebaran['n']:,})",
            f"- Galat baku ekspektasi: **{sebaran['galat_baku_R']:.6f}R**",
            f"- Selang 95% (pendekatan normal): "
            f"**[{sebaran['ci95_bawah_R']:.6f}, {sebaran['ci95_atas_R']:.6f}]R**",
            f"- Kuartil R: min {sebaran['min_R']:.4f} \u00b7 "
            f"Q1 {sebaran['q1_R']:.4f} \u00b7 median {sebaran['median_R']:.4f} "
            f"\u00b7 Q3 {sebaran['q3_R']:.4f} \u00b7 maks {sebaran['maks_R']:.4f}",
            f"- Jarak ke ambang {jarak['ambang']}R: "
            f"**{jarak['jarak_R']:+.6f}R**"
            + (
                f" = **{jarak['jarak_galat_baku']:+.2f} galat baku**"
                if jarak["jarak_galat_baku"] is not None
                else f" (satuan galat baku tidak dapat dihitung: {jarak['sebab']})"
            ),
        ]
    else:
        md += [f"Tidak dapat dinilai: {sebaran['sebab']}."]

    md += [
        "",
        "## Sebelas gerbang",
        "",
        "| Gerbang | Putusan | Nilai | Ambang | Catatan |",
        "|---|---|---|---|---|",
    ]
    for g in laporan.gerbang:
        n = "\u2014" if g.nilai is None else f"{g.nilai:.4f}"
        am = "\u2014" if g.ambang is None else f"{g.ambang}"
        md.append(
            f"| {g.nama} | {'lulus' if g.lulus else 'GAGAL'} | {n} | {am} | "
            f"{g.catatan} |"
        )

    md += [
        "",
        "## Jackknife konsentrasi (ADR-010)",
        "",
        "Buang penyumbang teratas satu per satu. Retensi adalah ekspektasi "
        "setelah pembuangan dibagi ekspektasi utuh. Ini menjawab pertanyaan yang "
        "sesungguhnya penting: apakah keunggulan tetap ada seandainya simbol "
        "paling untung tidak pernah ada.",
        "",
        "| k | Dibuang | Simbol sisa | Trade | Total R | Ekspektasi R | Retensi |",
        "|---|---|---|---|---|---|---|",
    ]
    strip = "\u2014"
    for b in jackknife:
        dibuang = b["dibuang"] or strip
        e = strip if b["ekspektasi_R"] is None else f"{b['ekspektasi_R']:.6f}"
        ret = strip if b["retensi"] is None else f"{b['retensi']:.4f}"
        md.append(
            f"| {b['k']} | {dibuang} | {b['simbol_sisa']} | {b['trade']:,} | "
            f"{b['total_R']:.2f} | {e} | {ret} |"
        )

    md += [
        "",
        "## Ekor funding (ADR-011)",
        "",
        "Gerbang funding lama menilai total mutlak dan memberi nilai yang "
        "praktis sama untuk dua keadaan yang ekornya berbeda 4,4 kali. Yang "
        "dinilai di sini adalah porsi funding terhadap kerugian pada sepuluh "
        "perdagangan terburuk, karena di situlah funding pernah menyumbang "
        "46,7% kerugian sementara reratanya hanya 0,0004R.",
        "",
    ]
    if ukuran_funding["dapat_dinilai"]:
        md += [
            f"- Porsi funding terbesar di ekor: "
            f"**{ukuran_funding['porsi_funding_ekor_maks']:.4f}** "
            f"(ambang 0,35)",
            f"- Rerata porsi di {ukuran_funding['k_ekor']} terburuk: "
            f"**{ukuran_funding['porsi_funding_ekor_rerata']:.4f}**",
            f"- Funding terbesar satu perdagangan: "
            f"**{ukuran_funding['funding_maks_R']:.4f}R** (ambang 0,50R)",
            f"- Perdagangan di atas pengaman 0,25R: "
            f"**{ukuran_funding['n_di_atas_pengaman']:,}** dari "
            f"{ukuran_funding['n_trade']:,} "
            f"({ukuran_funding['porsi_di_atas_pengaman']:.5f}, ambang 0,005)",
            "",
            "| # | R | Funding R | Porsi funding |",
            "|---|---|---|---|",
        ]
        for b in ekor_funding:
            porsi = (
                strip if b["porsi_funding"] is None else f"{b['porsi_funding']:.4f}"
            )
            md.append(
                f"| {b['peringkat']} | {b['R']:.4f} | {b['funding_R']:.4f} | "
                f"{porsi} |"
            )
    else:
        md += [f"Tidak dapat dinilai: {ukuran_funding['sebab']}."]

    md += ["", "## Pembongkaran biaya", ""]
    if diagnosa["jumlah"]:
        md += [
            f"- Rerata biaya transaksi: **{diagnosa['rerata_transaksi_R']:.4f}R**",
            f"- Rerata biaya funding: **{diagnosa['rerata_funding_R']:.4f}R**",
            f"- Rerata jarak stop terhadap harga: "
            f"**{diagnosa['rerata_stop_frac'] * 100:.3f}%**",
            f"- Perdagangan dengan biaya melebihi 1R: "
            f"**{diagnosa['trade_biaya_lebih_1R']:,}** dari {diagnosa['jumlah']:,}",
        ]
    else:
        md += ["Tidak ada perdagangan untuk dibongkar."]

    if parameter_terpilih:
        md += [
            "",
            "## Parameter yang terpilih di dalam sampel",
            "",
            "| Parameter | Jumlah jendela |",
            "|---|---|",
        ]
        for kunci, jml in sorted(
            parameter_terpilih.items(), key=lambda kv: -kv[1]
        )[:12]:
            md.append(f"| `{kunci}` | {jml} |")

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

    (out / f"backtest_{spek.nama}.md").write_text(
        "\n".join(md) + "\n", encoding="utf-8"
    )

    return {
        "id": spek.h.id,
        "nama": spek.nama,
        "sidik": spek.h.sidik()[:16],
        "ekspektasi_R": gabungan["ekspektasi_R"],
        "total_R": gabungan["total_R"],
        "trade": gabungan["jumlah_trade_luar_sampel"],
        "jendela_positif": gabungan["jendela_positif"],
        "jumlah_jendela": gabungan["jumlah_jendela"],
        "p_entri_acak": p_acak,
        "gerbang_gagal": laporan.yang_gagal,
        "lulus": bool(putusan.lulus and laporan.semua_lulus),
        "alasan": putusan.alasan,
        "alasan_keluar": alasan,
        "entri_ditolak_biaya": entri_ditolak_biaya,
        "simbol_dibuang_lantai": (
            [] if ktx.saringan is None else [b["symbol"] for b in ktx.saringan["ditolak"]]
        ),
        "bulan_dengan_trade": len(agregat_periode),
        "rerata_transaksi_R": diagnosa.get("rerata_transaksi_R"),
        "retensi_drop_1": g_konsentrasi.nilai,
        "porsi_funding_ekor_maks": g_funding_ekor.nilai,
        "std_R": sebaran["std_R"],
        "galat_baku_R": sebaran["galat_baku_R"],
        "jarak_galat_baku": jarak["jarak_galat_baku"],
        "detik": isi["detik"],
    }
