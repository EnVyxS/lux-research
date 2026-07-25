"""Pra-registrasi hipotesis: menulis tebakan sebelum melihat jawabannya.

Modul ini tidak menghitung apa pun. Fungsinya semata membuat satu hal menjadi
mustahil: mengubah kriteria keberhasilan setelah hasilnya terlihat.

Tanpa berkas seperti ini, urutan kejadian yang paling wajar dan paling merusak
adalah sebagai berikut. Sebuah strategi diuji, ekspektasinya 0,04R padahal
tadinya diharapkan 0,10R. Muncul pikiran yang terdengar masuk akal: mungkin
ambangnya memang terlalu ambisius, mungkin periodenya kebetulan buruk, mungkin
lebih adil menilai tanpa dua jendela terakhir. Setiap penyesuaian itu bisa
dibenarkan satu per satu, dan gabungan seluruhnya adalah hasil yang tidak
mengandung informasi apa pun selain keinginan penelitinya.

Karena itu berkas hipotesis bersifat **sekali tulis**. Menyimpan ulang dengan
isi berbeda ditolak dengan galat, bukan diperingatkan.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class Kriteria:
    """Ambang keberhasilan yang ditetapkan sebelum eksperimen dijalankan."""

    min_ekspektasi_R: float = 0.05
    min_trade_luar_sampel: int = 100
    maks_p_entri_acak: float = 0.05
    min_jendela_positif_rasio: float = 0.5

    def __post_init__(self) -> None:
        if self.min_trade_luar_sampel < 1:
            raise ValueError("min_trade_luar_sampel harus positif")
        if not 0 < self.maks_p_entri_acak < 1:
            raise ValueError("maks_p_entri_acak harus di antara 0 dan 1")
        if not 0 <= self.min_jendela_positif_rasio <= 1:
            raise ValueError("min_jendela_positif_rasio harus di antara 0 dan 1")


@dataclass(frozen=True)
class Hipotesis:
    id: str
    pernyataan: str
    dataset: str
    ruang_parameter: dict
    kriteria: Kriteria = field(default_factory=Kriteria)
    dibuat_utc: str = ""
    komit: str = ""

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("id hipotesis wajib diisi")
        if not self.pernyataan.strip():
            raise ValueError("pernyataan hipotesis wajib diisi")
        if not self.ruang_parameter:
            raise ValueError("ruang parameter wajib dinyatakan di muka")
        if not self.dibuat_utc:
            object.__setattr__(
                self,
                "dibuat_utc",
                datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            )

    @property
    def jumlah_kombinasi(self) -> int:
        """Besar ruang pencarian, dihitung di muka.

        Angka ini ditulis sebelum eksperimen justru agar tidak mengejutkan
        sesudahnya. Ruang berisi 500 kombinasi hampir pasti memuat sesuatu yang
        terlihat berhasil secara kebetulan, dan mengetahui itu di awal adalah
        satu-satunya waktu ketika pengetahuan itu masih bisa mengubah rancangan.
        """
        n = 1
        for nilai in self.ruang_parameter.values():
            n *= max(1, len(nilai) if isinstance(nilai, (list, tuple)) else 1)
        return n

    def ke_dict(self) -> dict:
        d = asdict(self)
        d["jumlah_kombinasi"] = self.jumlah_kombinasi
        return d

    def sidik(self) -> str:
        """Sidik jari isi hipotesis, tanpa memasukkan waktu pembuatan.

        Waktu sengaja dikeluarkan agar hipotesis yang isinya identik menghasilkan
        sidik yang sama dan dapat dibandingkan antar sesi.
        """
        inti = {
            "id": self.id,
            "pernyataan": self.pernyataan,
            "dataset": self.dataset,
            "ruang_parameter": self.ruang_parameter,
            "kriteria": asdict(self.kriteria),
        }
        teks = json.dumps(inti, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(teks.encode("utf-8")).hexdigest()


def simpan(h: Hipotesis, path: str | Path) -> Path:
    """Tulis hipotesis sekali saja.

    Bila berkas sudah ada dengan isi yang sama persis, penyimpanan ulang
    dibiarkan lewat agar pipeline yang diulang tidak patah. Bila isinya
    berbeda, penyimpanan **ditolak**: itulah satu-satunya kejadian yang benar
    benar ingin dicegah modul ini.
    """
    p = Path(path)
    baru = h.ke_dict()
    baru["sidik"] = h.sidik()
    if p.exists():
        lama = json.loads(p.read_text(encoding="utf-8"))
        if lama.get("sidik") != baru["sidik"]:
            raise ValueError(
                f"hipotesis {h.id} sudah terdaftar dengan isi berbeda; "
                "buat id baru alih-alih menyunting yang lama"
            )
        return p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(baru, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


def muat(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


@dataclass(frozen=True)
class Putusan:
    lulus: bool
    alasan: list[str]


def nilai(h: Hipotesis, ringkasan: dict, p_entri_acak: float | None) -> Putusan:
    """Bandingkan hasil terhadap kriteria yang sudah dikunci.

    Semua alasan kegagalan dikumpulkan, bukan hanya yang pertama. Melaporkan
    satu kegagalan mengundang perbaikan setempat lalu pengujian ulang, dan
    pengujian ulang berkali-kali atas data yang sama adalah bentuk lain dari
    pencarian yang tidak dihitung.
    """
    k = h.kriteria
    alasan: list[str] = []

    n = ringkasan.get("jumlah_trade_luar_sampel", 0)
    if n < k.min_trade_luar_sampel:
        alasan.append(f"trade luar sampel {n} < {k.min_trade_luar_sampel}")

    e = ringkasan.get("ekspektasi_R")
    if e is None:
        alasan.append("ekspektasi R tidak terdefinisi")
    elif e < k.min_ekspektasi_R:
        alasan.append(f"ekspektasi {e:.4f}R < {k.min_ekspektasi_R}R")

    if p_entri_acak is None:
        alasan.append("uji entri acak tidak dijalankan")
    elif p_entri_acak > k.maks_p_entri_acak:
        alasan.append(f"p entri acak {p_entri_acak:.4f} > {k.maks_p_entri_acak}")

    jml = ringkasan.get("jumlah_jendela", 0)
    if jml > 0:
        rasio = ringkasan.get("jendela_positif", 0) / jml
        if rasio < k.min_jendela_positif_rasio:
            alasan.append(
                f"jendela positif {rasio:.2f} < {k.min_jendela_positif_rasio}"
            )
    else:
        alasan.append("tidak ada jendela walk-forward")

    return Putusan(lulus=not alasan, alasan=alasan)
