"""Menuliskan diagnostik pelanggaran ambang risiko ke ``reports/``.

ADR-038 bagian 5.4 menuntut satu laporan per sel atas setiap perdagangan yang
melewati ambang ``invarian_risiko``. ``lux.diagnostik.pelanggaran_risiko``
sudah menghitungnya, tetapi ia murni: ia tidak menyentuh berkas. Modul ini
adalah satu-satunya tempat di paket diagnostik yang menulis ke cakram, dan ia
sengaja dipisahkan supaya aritmetikanya dapat diuji tanpa cakram sama sekali.

**Larangan yang berlaku atas modul ini.** Ia membaca dua hal saja: daftar
``Perdagangan`` dan ``konfig.slippage``. Ia tidak menyentuh ``konfig``, tidak
memanggil gerbang, tidak membaca maupun menulis ambang, dan tidak memancarkan
satu pun medan yang dapat dibaca sebagai putusan. Sisipan diagnostik yang
mengubah satu angka pun pada laporan hipotesis membatalkan kesebandingan
seluruh papan skor (jurnal 44 bagian 3.4).

**Ambang tidak ditulis ulang di sini.** Ia datang dari
``pelanggaran_risiko.AMBANG_KERUGIAN_R``, yang sendiri membacanya dari nilai
bawaan ``gerbang_invarian_risiko``. Angka 1,5 tidak diketik di berkas ini, dan
tidak boleh diketik.

**Mengapa ada dua pintu masuk.** ``tulis_laporan`` melempar bila sesuatu salah;
itu bentuk yang benar untuk pytest dan untuk skrip. ``emisikan`` menangkap
setiap kekecualian dan mengembalikannya sebagai medan ``galat``; itu bentuk yang
benar untuk sisi runner, sebab diagnostik yang dapat menjatuhkan run hipotesis
adalah diagnostik yang mengubah hasil, dan itu justru yang dilarang. Galatnya
**dipancarkan**, tidak ditelan diam-diam: bila medan ``galat`` ada, laporan itu
tidak ada, dan itu terbaca di ``isi``.

**Mengapa JSON dipotong.** Pelanggaran dapat bercacah puluhan ribu. Ambang
bawaan ``BATAS_BARIS_JSON`` menahan berkas keluaran agar tidak tumbuh menjadi
ratusan KB yang tidak dapat dibaca ulang; pemotongan **dinyatakan** lewat medan
``dipotong`` dan ``cacah_baris``, bukan disembunyikan. Cacah pelanggaran penuh
selalu ada di ``ringkas``, sehingga R-P2 tetap dapat diadjudikasi walau barisnya
dipotong.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from lux.diagnostik.pelanggaran_risiko import (
    baris_pelanggaran,
    ke_markdown,
    ringkas_pelanggaran,
)

DIR_LAPORAN = Path("reports")
AWALAN = "pelanggaran_risiko_"

# Nama sel ikut menjadi nama berkas. Ia karena itu dibatasi ke aksara yang
# tidak dapat keluar dari direktori laporan; ".." dan "/" ditolak, bukan
# dibersihkan diam-diam.
POLA_NAMA = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")

BATAS_BARIS_MD = 200
BATAS_BARIS_JSON = 2000


def periksa_nama(nama: str) -> str:
    """Nama sel yang sah, atau ``ValueError``."""
    teks = str(nama)
    if ".." in teks or not POLA_NAMA.match(teks):
        raise ValueError(f"nama sel tidak sah untuk nama berkas: {nama!r}")
    return teks


def jalur_laporan(nama: str, sufiks: str, dir_laporan: Path | str = DIR_LAPORAN) -> Path:
    """Jalur berkas laporan untuk satu sel dan satu sufiks."""
    return Path(dir_laporan) / f"{AWALAN}{periksa_nama(nama)}{sufiks}"


def tulis_laporan(
    perdagangan: Iterable[Any],
    konfig: Any,
    nama: str,
    dir_laporan: Path | str = DIR_LAPORAN,
    cacah_trade: int | None = None,
    batas_baris_md: int = BATAS_BARIS_MD,
    batas_baris_json: int = BATAS_BARIS_JSON,
) -> dict:
    """Tulis ``.md`` dan ``.json`` untuk satu sel; kembalikan ringkasannya.

    ``konfig`` dibaca untuk ``slippage`` saja. Nilai kembalinya sengaja kecil:
    ia dimaksudkan untuk ditaruh apa adanya di dalam dict ``isi`` sisi runner,
    dan dict itu ikut masuk ke laporan hipotesis. Barisnya tinggal di JSON.
    """
    nama = periksa_nama(nama)
    slippage = float(konfig.slippage)
    daftar = list(perdagangan)
    if cacah_trade is None:
        cacah_trade = len(daftar)
    baris = baris_pelanggaran(daftar, slippage)
    ringkas = ringkas_pelanggaran(baris, cacah_trade=int(cacah_trade))

    p_md = jalur_laporan(nama, ".md", dir_laporan)
    p_json = jalur_laporan(nama, ".json", dir_laporan)
    p_md.parent.mkdir(parents=True, exist_ok=True)

    teks = ke_markdown(
        baris,
        ringkas,
        judul=f"Pelanggaran ambang invarian_risiko \u2014 {nama}",
        batas_baris=batas_baris_md,
    )
    p_md.write_text(teks, encoding="utf-8")

    baris_json = baris[:batas_baris_json]
    muatan = {
        "nama": nama,
        "ambang_R": ringkas["ambang_R"],
        "slippage": slippage,
        "ringkas": ringkas,
        "cacah_baris": len(baris),
        "cacah_baris_ditulis": len(baris_json),
        "dipotong": len(baris_json) < len(baris),
        "baris": baris_json,
    }
    p_json.write_text(
        json.dumps(muatan, indent=1, sort_keys=True, ensure_ascii=False),
        encoding="utf-8",
    )

    return {
        "nama": nama,
        "berkas_md": str(p_md),
        "berkas_json": str(p_json),
        "ambang_R": ringkas["ambang_R"],
        "cacah_pelanggaran": ringkas["cacah_pelanggaran"],
        "cacah_trade": ringkas["cacah_trade"],
        "porsi": ringkas["porsi"],
        "terburuk_R": ringkas["terburuk_R"],
        "per_alasan": ringkas["per_alasan"],
        "cacah_celah_melewati_stop": ringkas["cacah_celah_melewati_stop"],
        "cacah_harga_bar_sungguhan": ringkas["cacah_harga_bar_sungguhan"],
        "terburuk_selisih_stop_R": ringkas["terburuk_selisih_stop_R"],
        "dipotong_json": muatan["dipotong"],
    }


def emisikan(
    perdagangan: Iterable[Any],
    konfig: Any,
    nama: str,
    dir_laporan: Path | str = DIR_LAPORAN,
    cacah_trade: int | None = None,
) -> dict:
    """``tulis_laporan`` yang tidak pernah melempar. Untuk sisi runner.

    Diagnostik tidak berhak menjatuhkan run hipotesis. Bila ia gagal, yang
    dikembalikan adalah dict bermedan ``galat`` — terbaca di ``isi``, tidak
    ditelan.
    """
    try:
        return tulis_laporan(
            perdagangan,
            konfig,
            nama,
            dir_laporan=dir_laporan,
            cacah_trade=cacah_trade,
        )
    except Exception as exc:  # noqa: BLE001 - lihat docstring
        return {"nama": str(nama), "galat": repr(exc)}
