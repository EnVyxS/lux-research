"""Saringan funding sebagai sinyal — tiga sel H-015 (ADR-037).

Modul ini **tidak** menghitung aritmetika funding sendiri. Seluruh angka funding
datang dari ``lux.funding_model``, dan larangan itu bukan soal kerapian: dua
implementasi funding adalah cara paling andal melahirkan dua deret biaya yang
berbeda tanpa ada yang menyadarinya (aturan 32, dan larangan tetap ADR-037 §10).

TIGA SEL, DAN HANYA SATU SELISIH YANG MENGIKAT
----------------------------------------------
=====  ======================================  ============================
Sel    Sinyal                                  Maksud
=====  ======================================  ============================
``K``  Donchian apa adanya                     kontrol
``F``  Donchian, entri ditolak saringan        hipotesis
``A``  Donchian, entri ditolak **acak**        pembanding kecondongan arah
=====  ======================================  ============================

Sel ``A`` membuang entri dengan **cacah yang sama persis** dengan sel ``F``, per
arah per bulan kalender UTC, tetapi memilih **yang mana** secara acak berseed
tanpa melihat funding sedikit pun.

Sebabnya satu angka: funding positif pada **79,1%** periode (ADR-037 §1).
Saringan funding apa pun karena itu membuang long jauh lebih sering daripada
short, bahkan bila ia tidak memuat setitik pun informasi. Maka:

- ``F − A`` mengukur **informasi funding**, dan hanya inilah yang mengikat.
- ``F − K`` mengukur informasi funding **ditambah** kecondongan arah, dan ia
  haram dipakai sebagai dasar kelulusan (ADR-037 §4, daftar angka haram).

KEBOCORAN MUSTAHIL SECARA BENTUK, BUKAN KARENA HATI-HATI
---------------------------------------------------------
Satu-satunya jalan masuk data funding di sini adalah
``Jadwal.statistik_trailing(sampai_ms, jendela_ms)``, yang menurut bentuknya
hanya dapat melihat penagihan **sebelum** ``sampai_ms``. Tidak ada jalur lain
yang dipanggil, dan itu keputusan mengikat ADR-037 §2: sebuah saringan yang
"berhati-hati tidak melihat masa depan" bergantung pada disiplin penulisnya,
sedangkan saringan yang **tidak punya cara** melihat masa depan tidak.

``sampai_ms`` diambil dari ``open_time`` bar yang sinyalnya dinilai, yakni saat
entri diputuskan. Penagihan yang stempelnya persis sama dengan pembukaan bar
sudah selesai dan sudah publik pada saat itu, jadi memasukkannya bukan
kebocoran; yang akan menjadi kebocoran adalah memakai ``open_time`` bar
berikutnya, dan itu tidak dilakukan di mana pun di berkas ini.

Akibat yang disengaja: sinyal pada bar ``t`` hanya bergantung pada bar ``≤ t``,
sehingga saringan ini **tahan pemotongan** dan gerbang ``lookahead`` — yang
memotong bingkai lalu menuntut sinyal awal tidak berubah — tetap sah dinilai
pada sel ``F``. Pada sel ``A`` gerbang itu **dijamin gagal** karena penolakan
acak bergantung pada cacah per bulan di seluruh potongan; menurut aturan 36 itu
konsekuensi konstruksi, bukan temuan, dan haram dilaporkan sebagai temuan.

DUA AMBANG, KEDUANYA BEKU
-------------------------
``AMBANG_RATE`` diturunkan, bukan dipilih (ADR-037 §3.1): setengah pengaman
carry 0,125R dibagi lebar stop rerata 0,0361 memberi 0,00451 rate kumulatif yang
ditanggung sepanjang horizon, dan dibagi 48 penagihan menjadi 0,000094 —
dibulatkan ke **0,0001**. Menggesernya sesudah hasil terlihat menuntut membantah
salah satu dari empat angka itu di depan umum, dan itulah gunanya.

``MIN_PENAGIHAN`` = 30. Jadwal yang lebih tipis dari itu membuat entri
**DITOLAK**, bukan dilewatkan. Data tipis diperlakukan berbahaya, bukan netral.
Arah kerugiannya jelas dan merugikan hipotesisnya sendiri: sel ``F`` kehilangan
perdagangan justru di tempat yang paling tidak diketahui.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping

import numpy as np
import pandas as pd

from lux.funding_model import HARI_MS, ambil_jadwal

# Kolom yang wajib ada pada bingkai. Keduanya lahir di ``run_wf.muat_ohlcv``,
# yang menulis ``symbol`` sebagai str lalu mengelompokkan menurutnya; kolomnya
# ikut pada tiap bingkai per simbol, dan potongan ``iloc`` di walk_forward
# mempertahankannya.
KUNCI_WAKTU = "open_time"
KUNCI_SIMBOL = "symbol"

# ADR-037 §3.1. Diturunkan, tidak dipilih. Tidak bergerak sesudah hasil terlihat.
AMBANG_RATE = 0.0001
MIN_PENAGIHAN = 30

# Jendela penarikan statistik funding. Sama dengan ``jendela_carry_hari`` bawaan
# Konfig, dan disamakan dengan sengaja: dua jendela funding yang berbeda di satu
# run akan membuat saringan dan pengaman carry berbicara tentang dua masa lalu.
JENDELA_HARI = 30
JENDELA_MS = JENDELA_HARI * HARI_MS

# ADR-037 §4. Dibekukan sebelum satu angka pun terlihat.
SEED_ACAK_H015 = 20260727

NAMA_SEL = ("K", "F", "A")


def simbol_bingkai(df: pd.DataFrame) -> str:
    """Nama simbol milik bingkai, atau ``ValueError`` yang berbunyi.

    Saringan ini butuh ``Jadwal`` milik simbol, sedangkan ``buat_sinyal`` di
    ``walk_forward`` hanya menerima ``(df, params)``. Simbolnya karena itu
    dibaca dari bingkai itu sendiri alih-alih memperluas kontrak yang dipakai
    empat belas hipotesis.

    Bingkai bercampur simbol adalah cacat pemuatan, bukan keadaan yang boleh
    ditangani diam-diam: bila ia terjadi, seluruh saringan akan memakai jadwal
    milik simbol yang salah dan hasilnya tetap tampak wajar.
    """
    if KUNCI_SIMBOL not in df.columns:
        raise ValueError(
            f"bingkai tanpa kolom {KUNCI_SIMBOL!r}; saringan funding mustahil "
            "mengetahui jadwal milik siapa"
        )
    unik = pd.unique(df[KUNCI_SIMBOL].astype(str))
    if len(unik) != 1:
        raise ValueError(
            f"bingkai memuat {len(unik)} simbol, wajib tepat satu: {list(unik)[:5]}"
        )
    return str(unik[0])


def waktu_bingkai(df: pd.DataFrame) -> np.ndarray:
    if KUNCI_WAKTU not in df.columns:
        raise ValueError(f"bingkai tanpa kolom {KUNCI_WAKTU!r}")
    return df[KUNCI_WAKTU].to_numpy(dtype="int64")


def bulan_utc(waktu: np.ndarray) -> np.ndarray:
    """Label bulan kalender UTC, satuan penarikan resmi (ADR-028, aturan 55).

    Dikembalikan sebagai larik string ``YYYY-MM`` supaya pengelompokannya sama
    persis dengan ``lux.analisis.periode`` dan tidak melahirkan satuan kedua.
    """
    ts = pd.to_datetime(np.asarray(waktu, dtype="int64"), unit="ms", utc=True)
    return np.asarray(pd.DatetimeIndex(ts).strftime("%Y-%m"), dtype=object)


def arah_ditolak(arah: int, rerata: float | None, n: int | None) -> bool:
    """Putusan satu entri, ADR-037 §3. Aritmetika murni, tanpa bingkai.

    Dua sebab penolakan, dan keduanya sengaja tidak dibedakan di luar sini:

    1. ``n < MIN_PENAGIHAN`` — jadwal terlalu tipis untuk dinilai.
    2. ``d × rerata > AMBANG_RATE`` — arah yang diambil membayar funding.

    ``d`` bernilai ``+1`` untuk long dan ``−1`` untuk short, sebab pemegang long
    membayar ketika rate positif dan menerima ketika negatif. Tanda inilah
    seluruh isi hipotesis; membalikkannya akan menghasilkan saringan yang
    justru memburu biaya.

    Sinyal nol tidak pernah ditolak: tidak ada entri untuk ditolak.
    """
    if arah == 0:
        return False
    if n is None or int(n) < MIN_PENAGIHAN:
        return True
    if rerata is None:
        return True
    d = 1.0 if arah > 0 else -1.0
    return bool(d * float(rerata) > AMBANG_RATE)


def mask_tolak(
    sinyal: np.ndarray,
    waktu: np.ndarray,
    jadwal,
    jendela_ms: int = JENDELA_MS,
) -> np.ndarray:
    """Larik boolean: entri mana yang ditolak saringan funding.

    Hanya bar dengan sinyal bukan nol yang ditanya; bar lain tidak punya entri
    untuk ditolak, dan menanyakannya hanya akan memperlambat run empat jam.

    ``jadwal`` diterima sebagai objek, bukan sebagai kamus, supaya aritmetika
    ini dapat diuji tanpa membangun jadwal funding sungguhan (aturan 32).
    """
    s = np.asarray(sinyal)
    t = np.asarray(waktu, dtype="int64")
    if s.size != t.size:
        raise ValueError(
            f"panjang sinyal {s.size} tidak sama dengan panjang waktu {t.size}"
        )
    tolak = np.zeros(s.size, dtype=bool)
    if jadwal is None:
        # Tidak ada jadwal berarti tidak ada yang dapat dinilai. Menolak
        # seluruhnya lebih jujur daripada meloloskan seluruhnya, dan akibatnya
        # terlihat sebagai sel F yang kosong alih-alih sebagai sel F yang
        # kebetulan sama dengan kontrol.
        tolak[s != 0] = True
        return tolak
    for i in np.flatnonzero(s):
        rerata, n = jadwal.statistik_trailing(int(t[i]), jendela_ms)
        tolak[i] = arah_ditolak(int(s[i]), rerata, n)
    return tolak


def penolakan_setara(
    sinyal: np.ndarray,
    tolak: np.ndarray,
    bulan: np.ndarray,
    seed: int = SEED_ACAK_H015,
) -> np.ndarray:
    """Penolakan acak dengan cacah identik, per arah per bulan kalender UTC.

    Inilah sel ``A``, dan inilah satu-satunya pembanding yang membuat H-015
    dapat difalsifikasi. Yang dijaga identik adalah **cacah** entri yang
    dibuang untuk setiap pasangan (arah, bulan); yang diacak adalah **entri
    mana** yang dibuang.

    Pencocokan dilakukan per bulan, bukan secara agregat, karena kecondongan
    arah funding berubah antar rezim. Mencocokkan hanya secara agregat akan
    membiarkan sel ``A`` membuang long di bulan yang salah, dan selisih yang
    terukur kemudian akan memuat perbedaan waktu alih-alih perbedaan informasi.

    Seed dibekukan di ADR-037 §4 dan **tidak** dicampur dengan nama simbol:
    pengacakan yang bergantung nama akan berubah diam-diam ketika semesta
    berubah, dan run yang sama tidak lagi menghasilkan angka yang sama.
    """
    s = np.asarray(sinyal)
    t = np.asarray(tolak, dtype=bool)
    b = np.asarray(bulan, dtype=object)
    if not (s.size == t.size == b.size):
        raise ValueError(
            f"panjang tidak sepadan: sinyal {s.size}, tolak {t.size}, bulan {b.size}"
        )
    rng = np.random.default_rng(seed)
    hasil = np.zeros(s.size, dtype=bool)
    # Urutan iterasi dibuat pasti (arah lalu bulan terurut) supaya deret acak
    # yang ditarik tidak bergantung pada urutan kamus.
    for arah in (1, -1):
        pada_arah = s == arah
        if not pada_arah.any():
            continue
        for nama_bulan in sorted({str(x) for x in b[pada_arah]}):
            idx = np.flatnonzero(pada_arah & (b == nama_bulan))
            k = int(t[idx].sum())
            if k <= 0:
                continue
            if k >= idx.size:
                hasil[idx] = True
                continue
            hasil[rng.choice(idx, size=k, replace=False)] = True
    return hasil


def terapkan(sinyal: np.ndarray, tolak: np.ndarray) -> np.ndarray:
    """Nolkan sinyal yang ditolak. Salinan, bukan sunting di tempat.

    ``walk_forward`` menyimpan larik sinyal jendela uji untuk uji permutasi;
    menyunting di tempat berarti wilayah yang diuji permutasi tidak lagi sama
    dengan wilayah yang dinilai.
    """
    s = np.asarray(sinyal).copy()
    s[np.asarray(tolak, dtype=bool)] = 0
    return s


def sinyal_sel(
    sel: str,
    jadwal_semua: Mapping[str, object],
    dasar: Callable[[pd.DataFrame, dict], np.ndarray],
    seed: int = SEED_ACAK_H015,
    jendela_ms: int = JENDELA_MS,
) -> Callable[[pd.DataFrame, dict], np.ndarray]:
    """Bangun fungsi sinyal untuk satu sel.

    Sel ``K`` mengembalikan ``dasar`` **apa adanya**, bukan ``dasar`` yang
    dibungkus dengan penolakan kosong. Kontrol yang melewati jalur kode berbeda
    dari kontrol sesungguhnya bukan lagi kontrol, dan selisih sekecil apa pun
    yang lahir dari pembungkus akan terhitung sebagai informasi funding.

    Sel ``A`` menghitung penolakan sel ``F`` lebih dahulu — ia memang harus,
    sebab yang disamakan adalah cacahnya — lalu membuang yang lain secara acak.
    Jadi sel ``A`` **melihat** funding untuk menentukan berapa, dan **tidak**
    memakainya untuk menentukan yang mana.
    """
    if sel not in NAMA_SEL:
        raise ValueError(f"sel tidak dikenal: {sel!r}; yang dikenal {NAMA_SEL}")
    if sel == "K":
        return dasar

    acak = sel == "A"

    def bungkus(df: pd.DataFrame, params: dict) -> np.ndarray:
        s = np.asarray(dasar(df, params))
        if s.size != len(df):
            raise ValueError(
                f"panjang sinyal dasar {s.size} tidak sama dengan bingkai {len(df)}"
            )
        simbol = simbol_bingkai(df)
        waktu = waktu_bingkai(df)
        try:
            jadwal = ambil_jadwal(jadwal_semua, simbol)
        except KeyError:
            jadwal = None
        tolak = mask_tolak(s, waktu, jadwal, jendela_ms=jendela_ms)
        if acak:
            tolak = penolakan_setara(s, tolak, bulan_utc(waktu), seed=seed)
        return terapkan(s, tolak)

    return bungkus
