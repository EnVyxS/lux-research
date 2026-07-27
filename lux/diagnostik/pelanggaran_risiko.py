"""Rincian setiap perdagangan yang melewati ambang ``invarian_risiko``.

ADR-038 bagian 5.4. Gerbang ``invarian_risiko`` merah pada H-011 sampai H-015
tanpa satu pun pengecualian, dan yang dilaporkannya hanya satu angka: kerugian
terburuk. Satu angka tidak dapat membedakan tiga sebab yang sangat berbeda
akibatnya:

1. **Celah harga.** Stop terisi pada pembukaan bar yang sudah membuka jauh di
   seberang stop. Ini kerugian yang jujur; ambang -1,5R memang tidak dapat
   dijamin oleh mesin apa pun yang menghormati celah, dan ``stop_hormati_celah``
   memang menyala di ``config/lux.yaml``.
2. **Ukuran posisi salah hitung.** Ini yang ditakuti gerbang itu sejak awal, dan
   ini berarti satuan R tidak berarti apa-apa di seluruh papan skor.
3. **Keluar pada harga bar sungguhan lewat jalur bukan-stop** (``umur``,
   ``carry``, ``akhir_data``), yang tidak pernah dibatasi oleh jarak stop.

Modul ini memisahkan ketiganya per perdagangan. Ia **tidak** menilai, tidak
mengubah ambang, dan tidak memancarkan putusan.

**Batas kemampuannya dinyatakan di muka.** ``Perdagangan`` tidak menyimpan harga
pembukaan bar keluar, jadi modul ini tidak dapat membuktikan secara langsung
bahwa pengisian terjadi pada pembukaan bar. Yang dapat dilakukannya: membalik
slippage keluar untuk memperoleh harga pengisian **bruto**, lalu
membandingkannya dengan stop teoretis. Bila bruto lebih buruk daripada stop
teoretis sementara ``alasan_keluar`` adalah ``stop``, maka menurut
``lux.backtest.engine.harga_stop_terisi`` hanya ada satu sumber angka itu, yaitu
pembukaan bar. Pembuktian penuh menuntut instrumentasi di dalam mesin; itu
sengaja tidak dilakukan di sini, sebab menyentuh mesin untuk menjelaskan hasil
yang sudah lahir adalah cara termurah mencemari eksperimen berikutnya.

**Ambangnya tidak ditulis tangan.** Ia dibaca dari nilai bawaan
``gerbang_invarian_risiko`` lewat ``inspect``. Ambang yang disalin dengan tangan
akan tertinggal pada saat gerbangnya digeser, dan tertinggalnya berupa
diagnostik yang berbohong tentang gerbang yang sedang diperiksanya (aturan 53).
"""

from __future__ import annotations

import inspect
from collections import Counter
from collections.abc import Iterable, Sequence
from datetime import datetime, timezone

from lux.backtest.engine import Perdagangan
from lux.backtest.gerbang import gerbang_invarian_risiko

# Dibaca dari gerbangnya sendiri, bukan disalin. Lihat docstring modul.
AMBANG_KERUGIAN_R: float = float(
    inspect.signature(gerbang_invarian_risiko).parameters["maks_kerugian_R"].default
)

# Selisih di bawah ini dianggap nol; ia lahir dari pembagian dan perkalian
# pecahan, bukan dari celah harga.
TOLERANSI_R: float = 1e-9

# Jalur keluar yang mengisi pada harga bar sungguhan dan karena itu tidak
# pernah dibatasi oleh jarak stop. Lihat docstring ``lux.backtest.engine``.
ALASAN_HARGA_BAR: tuple[str, ...] = ("umur", "carry", "akhir_data")

KOLOM: tuple[str, ...] = (
    "symbol",
    "arah",
    "alasan_keluar",
    "R",
    "selisih_stop_R",
    "stop_frac",
    "masuk_iso",
    "keluar_iso",
    "harga_masuk",
    "stop_teoretis",
    "harga_keluar_bruto",
    "harga_keluar",
)


def _periksa_slippage(slippage: float) -> None:
    if not 0.0 <= float(slippage) < 1.0:
        raise ValueError("slippage harus di dalam [0, 1)")


def waktu_iso(ms: int) -> str:
    """Stempel waktu UTC. Zona waktu ditulis eksplisit, tidak diandaikan."""
    return datetime.fromtimestamp(int(ms) / 1000.0, tz=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def harga_keluar_bruto(harga_keluar: float, arah: int, slippage: float) -> float:
    """Balik slippage keluar untuk memperoleh harga pengisian sebelum slippage.

    Mesin mengisi keluar pada ``harga * (1 - arah * slippage)``; lihat
    ``lux.backtest.engine._harga_eksekusi`` dengan ``masuk=False``. Fungsi ini
    adalah kebalikannya, dan diletakkan di tingkat modul supaya dapat diuji
    terhadap harga bar yang diketahui, bukan hanya terhadap dirinya sendiri.
    """
    _periksa_slippage(slippage)
    faktor = 1.0 - int(arah) * float(slippage)
    if faktor <= 0.0:
        raise ValueError("faktor slippage keluar tidak positif")
    return float(harga_keluar) / faktor


def baris_untuk(p: Perdagangan, slippage: float) -> dict:
    """Satu baris diagnostik untuk satu perdagangan.

    Seluruh besaran harga ikut dilaporkan mentah. Diagnostik yang hanya
    memancarkan besaran turunan memaksa pembacanya mempercayai aritmetika yang
    justru sedang diperiksa.
    """
    risiko = float(p.jarak_stop) * float(p.ukuran)
    if risiko <= 0.0:
        raise ValueError("perdagangan tanpa risiko positif tidak dapat dirinci")
    bruto = harga_keluar_bruto(p.harga_keluar, p.arah, slippage)
    stop_teoretis = float(p.harga_masuk) - int(p.arah) * float(p.jarak_stop)
    selisih_stop_R = int(p.arah) * (stop_teoretis - bruto) / float(p.jarak_stop)
    slippage_keluar_R = (
        int(p.arah) * (bruto - float(p.harga_keluar)) / float(p.jarak_stop)
    )
    laba_kotor_R = float(p.laba_kotor) / risiko
    biaya_transaksi_R = float(p.biaya_transaksi) / risiko
    biaya_funding_R = float(p.biaya_funding) / risiko
    return {
        "symbol": p.symbol,
        "arah": int(p.arah),
        "alasan_keluar": p.alasan_keluar,
        "R": float(p.R),
        "laba_kotor_R": laba_kotor_R,
        "biaya_transaksi_R": biaya_transaksi_R,
        "biaya_funding_R": biaya_funding_R,
        "selisih_stop_R": selisih_stop_R,
        "slippage_keluar_R": slippage_keluar_R,
        "residu_identitas_R": laba_kotor_R
        - (-1.0 - selisih_stop_R - slippage_keluar_R),
        "stop_frac": float(p.jarak_stop) / float(p.harga_masuk),
        "masuk_ms": int(p.masuk_ms),
        "keluar_ms": int(p.keluar_ms),
        "masuk_iso": waktu_iso(p.masuk_ms),
        "keluar_iso": waktu_iso(p.keluar_ms),
        "harga_masuk": float(p.harga_masuk),
        "harga_keluar": float(p.harga_keluar),
        "harga_keluar_bruto": bruto,
        "stop_teoretis": stop_teoretis,
        "jarak_stop": float(p.jarak_stop),
        "ukuran": float(p.ukuran),
        "risiko": risiko,
        "celah_melewati_stop": (
            p.alasan_keluar == "stop" and selisih_stop_R > TOLERANSI_R
        ),
        "harga_bar_sungguhan": p.alasan_keluar in ALASAN_HARGA_BAR,
    }


def baris_pelanggaran(
    perdagangan: Iterable[Perdagangan],
    slippage: float,
    maks_kerugian_R: float = AMBANG_KERUGIAN_R,
) -> list[dict]:
    """Baris untuk setiap perdagangan yang melewati ambang, terburuk lebih dahulu.

    Ambang dibaca dengan tanda yang **persis** sama dengan gerbangnya: gerbang
    lulus bila ``terburuk >= -maks_kerugian_R``, jadi pelanggaran adalah
    ``R < -maks_kerugian_R``. Kesetaraan itu diuji terhadap gerbang yang
    sesungguhnya, bukan dinyatakan di komentar.

    Perdagangan tanpa risiko positif dilewati tanpa keluhan: ``Perdagangan.R``
    mengembalikan 0,0 untuknya, sehingga ia mustahil menjadi pelanggaran, dan
    menggagalkan seluruh diagnostik karena satu baris semacam itu akan membuat
    alat ini tidak dapat dijalankan justru pada data yang paling perlu dibaca.
    """
    _periksa_slippage(slippage)
    batas = -float(maks_kerugian_R)
    baris: list[dict] = []
    for p in perdagangan:
        if float(p.jarak_stop) * float(p.ukuran) <= 0.0:
            continue
        if float(p.R) < batas:
            baris.append(baris_untuk(p, slippage))
    baris.sort(key=lambda b: (b["R"], b["symbol"], b["keluar_ms"]))
    return baris


def ringkas_pelanggaran(
    baris: Sequence[dict],
    cacah_trade: int | None = None,
    maks_kerugian_R: float = AMBANG_KERUGIAN_R,
) -> dict:
    """Ringkasan cacah, sebab, dan simbol. Tidak ada putusan di sini."""
    per_alasan = Counter(b["alasan_keluar"] for b in baris)
    per_symbol = Counter(b["symbol"] for b in baris)
    return {
        "ambang_R": -float(maks_kerugian_R),
        "cacah_pelanggaran": len(baris),
        "cacah_trade": cacah_trade,
        "porsi": (
            len(baris) / cacah_trade
            if cacah_trade is not None and cacah_trade > 0
            else None
        ),
        "terburuk_R": baris[0]["R"] if baris else None,
        "paling_ringan_R": baris[-1]["R"] if baris else None,
        "per_alasan": dict(sorted(per_alasan.items(), key=lambda kv: (-kv[1], kv[0]))),
        "per_symbol": dict(
            sorted(per_symbol.items(), key=lambda kv: (-kv[1], kv[0]))[:10]
        ),
        "cacah_celah_melewati_stop": sum(
            1 for b in baris if b["celah_melewati_stop"]
        ),
        "cacah_harga_bar_sungguhan": sum(
            1 for b in baris if b["harga_bar_sungguhan"]
        ),
        "terburuk_selisih_stop_R": (
            max(b["selisih_stop_R"] for b in baris) if baris else None
        ),
    }


def ke_markdown(
    baris: Sequence[dict],
    ringkas: dict,
    judul: str = "Pelanggaran ambang invarian_risiko",
    batas_baris: int = 200,
) -> str:
    """Laporan Markdown. Kosong pun ditulis, sebab nol adalah temuan."""
    garis = [f"# {judul}", ""]
    garis.append(f"- ambang: {ringkas['ambang_R']}R")
    garis.append(f"- pelanggaran: {ringkas['cacah_pelanggaran']}")
    garis.append(f"- dari trade: {ringkas['cacah_trade']}")
    garis.append(f"- porsi: {ringkas['porsi']}")
    garis.append(f"- terburuk: {ringkas['terburuk_R']}R")
    garis.append(f"- paling ringan: {ringkas['paling_ringan_R']}R")
    garis.append(f"- per alasan keluar: {ringkas['per_alasan']}")
    garis.append(f"- sepuluh simbol teratas: {ringkas['per_symbol']}")
    garis.append(
        f"- pengisian di seberang stop: {ringkas['cacah_celah_melewati_stop']}"
    )
    garis.append(
        f"- keluar pada harga bar sungguhan: {ringkas['cacah_harga_bar_sungguhan']}"
    )
    garis.append(
        f"- selisih stop terburuk: {ringkas['terburuk_selisih_stop_R']}R"
    )
    garis.append("")
    if not baris:
        garis.append("Tidak ada perdagangan yang melewati ambang.")
        garis.append("")
        return "\n".join(garis)
    garis.append("| " + " | ".join(KOLOM) + " |")
    garis.append("|" + "|".join(["---"] * len(KOLOM)) + "|")
    for b in baris[:batas_baris]:
        garis.append("| " + " | ".join(str(b[k]) for k in KOLOM) + " |")
    if len(baris) > batas_baris:
        garis.append("")
        garis.append(
            f"Dipotong pada {batas_baris} baris dari {len(baris)}; "
            "sisanya ada di JSON."
        )
    garis.append("")
    return "\n".join(garis)
