"""Audit Konfig: seluruh medan, selisih lintas hipotesis, pengaman yang mati.

Modul ini lahir dari **cacat kelas kedelapan belas** (ADR-036). H-014 berjalan
dengan pengaman carry terealisasi (``maks_carry_realisasi_R``, ADR-008) bernilai
**0,0 — mati** — sedangkan H-013 menjalankannya pada 0,25. Sebabnya satu baris:
H-013 menyalurkan setiap kandidat lewat ``run_h009.buat_konfig``, yang memasang
pengaman itu, sementara H-014 memakai ``buat_konfig=None`` sehingga fungsi itu
tidak pernah dipanggil dan ``Konfig`` kembali ke bawaannya.

Dua pagar yang seharusnya menangkapnya gagal karena **keduanya hanya melihat ke
dalam satu hipotesis**:

1. ``run_h014.medan_berbeda`` membandingkan sel A terhadap sel B. Medan yang
   salah **secara identik di kedua sel** tidak terlihat olehnya.
2. Manifes mencatat sebelas butir yang dianggap penting, bukan seluruh
   ``Konfig``. Medan yang tidak dianggap penting adalah tepat medan yang hilang
   tanpa ketahuan.

Karena itu modul ini menyediakan tiga hal, dan sengaja **tidak** menyediakan
yang keempat.

**Yang disediakan.** ``konfig_penuh`` memuntahkan seluruh medan tanpa memilih;
``selisih_konfig`` membandingkan dua Konfig medan demi medan, termasuk lintas
hipotesis; ``pengaman_mati`` menjawab satu pertanyaan yang tidak pernah diajukan
siapa pun di H-014, yaitu apakah pengaman yang seharusnya menyala memang
menyala.

**Yang tidak disediakan: daftar pengaman wajib.** Modul ini tidak memuat angka
0,25 di mana pun. Menyalinnya ke sini berarti pagar mengutip nilai dari kode
yang dijaganya, dan pagar semacam itu tidak menjaga apa pun (aturan 31). Setiap
run **wajib menyatakan sendiri** pengaman apa yang dituntutnya, dan pernyataan
itu ikut masuk ke manifes.

**Mengapa modul terpisah, bukan sisipan di ``run_h014.py``.** ADR-036 keputusan
4 melarang H-014 dijalankan ulang, jadi menanam alat ini di dalam berkas yang
hipotesisnya sudah mati akan membuatnya mati bersamanya. Alat ini dibuat untuk
hipotesis **berikutnya**. Sampai ia benar-benar dipanggil oleh sebuah run, ia
**belum menjaga apa pun** — aturan 42 berlaku atas modul ini sendiri, dan
kenyataan itu dicatat di sini alih-alih dibiarkan terasa seperti pekerjaan yang
sudah selesai.

Arah impor sengaja satu arah: modul ini tidak mengimpor satu pun modul
eksperimen, sehingga tidak ada lingkaran impor dan tidak ada nilai eksperimen
yang menyelinap masuk sebagai bawaan.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, is_dataclass
from typing import Any


def konfig_penuh(konfig: Any) -> dict[str, Any]:
    """Seluruh medan ``Konfig`` sebagai dict, terurut menurut nama.

    Tidak ada penyaringan dan tidak ada daftar medan penting. Justru medan yang
    tidak dianggap penting oleh siapa pun — ``maks_carry_realisasi_R`` — yang
    hilang tanpa ketahuan di H-014.

    Urutannya dibakukan supaya dua manifes dapat dibandingkan sebagai teks.
    """
    if isinstance(konfig, type) or not is_dataclass(konfig):
        raise TypeError(
            "konfig_penuh menuntut INSTANS dataclass Konfig, bukan kelas atau "
            "dict; dict yang sudah disaring adalah persis cara medan hilang"
        )
    isi = asdict(konfig)
    return {nama: isi[nama] for nama in sorted(isi)}


def selisih_konfig(kiri: Any, kanan: Any) -> dict[str, dict[str, Any]]:
    """Medan yang nilainya berbeda antara dua Konfig.

    Dipakai untuk dua hal yang berbeda: membandingkan sel A terhadap sel B di
    dalam satu hipotesis (aturan 52), dan membandingkan sebuah sel terhadap sel
    pembanding di **hipotesis pendahulunya** (ADR-036 keputusan 3). Yang kedua
    inilah yang tidak pernah dilakukan sebelum S22.

    Selisih **tidak dilarang**. Ia wajib dinyatakan.
    """
    if type(kiri) is not type(kanan):
        raise TypeError(
            "selisih_konfig menuntut dua instans kelas yang sama; "
            f"diterima {type(kiri).__name__} dan {type(kanan).__name__}"
        )
    a = konfig_penuh(kiri)
    b = konfig_penuh(kanan)
    return {
        nama: {"kiri": a[nama], "kanan": b[nama]}
        for nama in a
        if a[nama] != b[nama]
    }


def pengaman_mati(konfig: Any, wajib: Mapping[str, float]) -> list[str]:
    """Nama pengaman yang tidak bernilai seperti yang dituntut run ini.

    ``wajib`` memetakan nama medan ke nilai yang dituntut. Daftar itu **wajib
    datang dari pemanggil**; modul ini tidak punya pendapat tentang angkanya.

    Tiga penolakan yang disengaja, semuanya ``ValueError`` alih-alih diam:

    - daftar kosong ditolak, sebab "tidak menuntut apa pun" adalah keadaan H-014
      dan ia tidak boleh dapat dinyatakan secara tidak sengaja;
    - medan yang tidak ada pada Konfig ditolak, sebab salah ketik yang diam akan
      melaporkan pengaman menyala padahal tidak ada yang diperiksa;
    - ambang yang tidak positif ditolak, sebab menuntut nol berarti menuntut
      pengaman itu mati.

    Nilai ``bool`` ditolak sebagai ambang walau Python menganggapnya bilangan;
    ``True`` yang menyamar sebagai 1 adalah cara paling mudah menyatakan tuntutan
    yang tidak dimaksudkan siapa pun.
    """
    if not wajib:
        raise ValueError(
            "daftar pengaman wajib tidak boleh kosong; run yang tidak menuntut "
            "satu pengaman pun adalah keadaan yang melahirkan cacat kelas 18"
        )
    isi = konfig_penuh(konfig)
    mati: list[str] = []
    for nama, ambang in sorted(wajib.items()):
        if nama not in isi:
            raise ValueError(
                f"medan {nama!r} tidak ada pada {type(konfig).__name__}; "
                "pengaman yang salah nama tidak memeriksa apa pun"
            )
        if isinstance(ambang, bool) or not isinstance(ambang, (int, float)):
            raise ValueError(f"ambang pengaman {nama!r} harus bilangan, bukan bool")
        if ambang <= 0:
            raise ValueError(
                f"ambang pengaman {nama!r} harus positif; menuntut nol berarti "
                "menuntut pengaman itu mati"
            )
        if isi[nama] != ambang:
            mati.append(nama)
    return mati


def laporan_kesebandingan(
    nama_sel: str,
    konfig: Any,
    nama_pendahulu: str,
    konfig_pendahulu: Any,
    pengaman_wajib: Mapping[str, float],
) -> dict[str, Any]:
    """Laporan yang wajib ikut ke manifes setiap run (ADR-036 keputusan 2 dan 3).

    Isinya: seluruh medan Konfig sel ini, seluruh selisihnya terhadap sel
    pembanding di hipotesis pendahulu, daftar pengaman yang mati, dan prosa yang
    dapat dicetak ke log.

    **Selisih tidak menghalangi run.** Yang menghalangi hanyalah pengaman yang
    mati. Perbedaan antar hipotesis adalah hal biasa dan sering memang
    dimaksudkan; yang tidak boleh terjadi adalah perbedaan yang **tidak
    diketahui siapa pun**, dan itu diobati dengan mencetaknya, bukan dengan
    melarangnya.
    """
    selisih = selisih_konfig(konfig, konfig_pendahulu)
    mati = pengaman_mati(konfig, pengaman_wajib)
    prosa = [
        f"konfig {nama_sel}: {len(konfig_penuh(konfig))} medan tercatat utuh",
    ]
    if selisih:
        rinci = ", ".join(
            f"{nama} {nilai['kiri']!r} lawan {nilai['kanan']!r}"
            for nama, nilai in selisih.items()
        )
        prosa.append(f"selisih terhadap {nama_pendahulu}: {rinci}")
    else:
        prosa.append(f"tidak ada selisih terhadap {nama_pendahulu}")
    if mati:
        prosa.append(
            "PENGAMAN MATI: " + ", ".join(mati) + " — run tidak boleh dilanjutkan"
        )
    return {
        "sel": nama_sel,
        "pendahulu": nama_pendahulu,
        "konfig": konfig_penuh(konfig),
        "selisih_terhadap_pendahulu": selisih,
        "pengaman_mati": mati,
        "menghalangi": bool(mati),
        "prosa": prosa,
    }
