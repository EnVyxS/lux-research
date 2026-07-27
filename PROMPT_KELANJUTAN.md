# Titik masuk kelanjutan riset LUX — v6

Ditulis atas HEAD `87042f3e3821c474f971ef635ca48c6c4cb2d286` (jurnal 45).
v5 (blob `255c72e1`) menyuruh "sambungkan diagnostik" tanpa mengetahui bahwa
`emisi.py` akan lahir sebelum sisipan `runner.py`. Itu sudah terjadi; v6
memperbaikinya.

---

## §0 Urutan baca yang mengikat

Baca berurutan, **utuh**, sebelum melakukan apa pun:

1. Berkas ini.
2. `decisions/ADR-038.md` (blob `4051e9a3bcf5169cd7ccc18c89cd7697d6935e20`) — ia
   membekukan adjudikasi dan **melarang run H-015 kedua** sampai ADR-039 ada.
3. `STATE.md` (v33, 44.196 B, blob `6955d3d4b4857f658f18e2629af24e3922535ecf`),
   termasuk **60 aturan bernomor** di bagian 1. **Jangan menulis ulang aturan
   dari ingatan.**
   **Peringatan keutuhan:** STATE v33 **usang pada dua angka** — ia menyebut
   1012 uji (kini **1029**, `reports/tests.md` blob
   `56c1d6ec9702b6e37c4a1f6563a856efa46aba6a`, commit `9be91ae7`) dan belum
   menyebut `lux/diagnostik/emisi.py`. Sisanya berlaku.
4. `STATE_LAMPIRAN_ANGKA.md` (14.769 B, blob
   `a72f0a04cc87f71235158b59d0ca2a805910d6de`).
5. `journal/2026-07-27-45.md` dan `journal/2026-07-27-44.md`. **Jangan membaca
   `journal/` seluruhnya.**

Jangan mulai dari awal. Jangan mengulang pekerjaan yang sudah selesai. Bila
sesuatu tidak tercatat di berkas-berkas itu, anggap **belum diketahui**.

---

## §1 Posisi (terverifikasi)

- 15 hipotesis diselesaikan: **14 DITOLAK**, 1 (**H-015**) **TIDAK DAPAT
  DINILAI** (run `30249117960`, `gerbang_gagal = ["invarian_risiko",
  "checksum"]` pada ketiga sel K/F/A).
- **Nol kandidat.** 60 aturan. 21 kelas cacat.
- **1029 uji lulus**, kode 0, atas `9be91ae7`.
- Diagnostik ekor −1,5R: **alatnya lengkap, jalur runnya belum tersambung.**
  - `lux/diagnostik/pelanggaran_risiko.py` (10.461 B, blob `b8d5678a`) — murni.
  - `lux/diagnostik/emisi.py` (6.183 B, blob
    `981d1510469b6937b12d480bd474ddf6dfd0e980`) — penulis berkas.
  - `tests/test_emisi_diagnostik.py` (blob
    `954110bea8c1a7b3e5a7d0094133908f182cc73d`) — 17 butir.
- **ADR-039 belum ada, dan itu disengaja** (jurnal 45 §3): R-P1, R-P2, R-P3,
  R-Q3, R-Q4 semuanya diadjudikasi oleh laporan diagnostik yang **belum lahir**.
  Karena ADR-039 belum ada, **run H-015 kedua tetap terlarang**.

---

## §2 Larangan

1. **Jangan menjalankan H-015 kedua** sampai ADR-039 ada (ADR-038 §6).
2. **Jangan menyentuh** `h014.yml`, `h015.yml`, `backtest.yml`, `h013b.yml`
   kecuali memang bermaksud memulai run 4 jam. Sentuhan = run.
3. **Jangan membaca berkas 40 KB lalu menulis penggantinya di jendela konteks
   yang sama** (aturan 35 mitigasi 3). `push_files` mengganti berkas **utuh**.
   Korban lama: `STATE.md` v28 (`56633f80`) terpotong diam-diam, posisi cacat
   hidup di `main` ~3,5 jam.
4. **Jangan menyambung diagnostik dari `run_h015.py`.** `jalankan_spek`
   mengembalikan dict ringkasan, bukan objek `Perdagangan`. Sudah diverifikasi;
   jangan mencobanya lagi.
5. **Diagnostik hanya membaca.** Menyentuh `konfig`, gerbang, ambang, atau
   `putusan` membatalkan kesebandingan seluruh papan skor.
6. **Jangan menulis uji dari ringkasan API sendiri** (aturan 42, cacat 12).
   Salin pola dari uji yang sudah hijau, dan sertakan satu uji yang menjalankan
   mesin sungguhan.
7. **Jangan menulis ulang ambang dari ingatan.** Ambang dibaca dari kode
   (`inspect.signature`), tidak diketik dua kali.
8. **Ukuran bukan bukti.** Sesudah setiap dorongan, baca ulang berkas dari
   `main` dan pastikan **ekornya hadir**.
9. Jangan menulis `STATE_LAMPIRAN.md` (25.016 B, blob `7b68ee63`) tanpa
   membacanya utuh lebih dahulu — dorongan akan menghapus isinya.

---

## §3 Tugas berprioritas

**1. Sisipan `runner.py` — jendela konteks bersih, tidak ada yang mendahuluinya.**
   - Baca `lux/backtest/runner.py` UTUH (40.322 B, blob `4ce34a3c`) di awal
     jendela, tanpa berkas 40 KB lain. **Tulis penggantinya di jendela
     berikutnya**, bukan di jendela pembacaan.
   - Di `jalankan_spek`, **setelah** `g_funding_ekor` dan **sebelum**
     `susun_laporan`: panggil
     `emisikan(semua_trade, konfig, <nama sel>, cacah_trade=<cacah trade sel>)`
     dari `lux.diagnostik.emisi`. Tambahkan **satu** kunci baru di dict `isi`
     (`"diagnostik_pelanggaran_risiko"`), berisi kembaliannya apa adanya.
   - `emisikan` tidak pernah melempar; bila gagal ia mengembalikan medan
     `galat`. Itu disengaja — diagnostik tidak berhak menjatuhkan run.
   - Sesudah didorong: baca ulang dari `main`, pastikan ekornya hadir.

**2. Masukkan `reports/pelanggaran_risiko_*.md` dan `.json` ke daftar `git add`
   workflow run** (aturan 56). Sentuhan itu **memulai run**, jadi bayar sekali
   saja: gabungkan dengan sentuhan yang memang dimaksudkan memulai run
   diagnostik (cacat 17 pernah membayar sembilan menit sia-sia).

**3. Adjudikasi** R-P1, R-P2, R-P3, R-Q3, R-Q4 (ADR-038 §7, jurnal 44 §5) dan
   R-R2, R-R3 (jurnal 45 §4) dari laporan diagnostik itu. **Baru kemudian tulis
   `decisions/ADR-039.md`.** Sesudah ADR-039 ada, pertanyaan "run H-015 kedua"
   boleh dibuka.

**4. `STATE.md` → v34.** Wajib di jendela yang **tidak** dipakai membaca berkas
   40 KB lain. Yang berubah: cacah uji 1012 → 1029; `lux/diagnostik/emisi.py`
   masuk daftar berkas; papan skor menambah R-R1 (TEPAT), R-R2 dan R-R3
   (terbuka); catatan bahwa ADR-039 ditunda dengan sebab.

**5. Utang lama, urutan bebas:**
   - R-L1: instrumentasi penolakan saringan menurut arah, atau **cabut** (cacat 21).
   - Cacat 19: satuan/pembobotan/p bulanan pada `praregistrasi.Kriteria`.
   - Misteri uji ke-17 (872 lawan 871) — lewat dorongan yang hanya menyentuh `tests/`.
   - R-J1: keluar `carry` sel SH dari `reports/backtest_h013_sh_sinyal_horizon.json`.
   - Sel A 162 s lawan K 70 s / F 74 s; entri acak nyata tertinggi A 0,10723R.
   - Baca commit `09ba5545` (`lux-backfill` jalan 06:07:39Z padahal cron `0 2 * * 1`).
   - Rasio bar datar 4h; utang audit konfig (aturan 39).

---

## §4 Ambang beku (jangan diubah, jangan dibulatkan)

lantai `stop_frac` **0,004** · pengawal biaya masuk **0,5R** · `BATAS_VOID` **20**
· batas data **2026-01-01** · selisih antar-sel **0,020R** (dibandingkan sebagai
float apa adanya; `0.06-0.04 = 0.019999999999999997` **gagal**, dan itu benar)
· p ≤ **0,05** atas bulan kalender UTC · ≥ **300** ulangan · ≥ **100** trade/sel
· `MAKS_RASIO_DATAR` **0,10** · rasio bar datar **0,30** · ekspektasi **0,05R**
· `invarian_risiko` **−1,5R** · `maks_umur_bar` ≤ **168** · gerbang ke-11
**0,35 / 0,50R / 0,005** · `maks_carry_realisasi_R` **0,25** · `AMBANG_RATE`
**0,0001** · `MIN_PENAGIHAN` **30** · `SEED_ACAK_H015` **20260727**.

---

## §5 Batas alat

- Tulis lewat `push_files` (**mengganti berkas utuh**). Tidak ada tambal baris.
- `search_code` tidak mengembalikan apa pun pada repo ini; pakai
  `get_file_contents` atas jalur direktori.
- `tests.yml` terpicu oleh `lux/**`, `tests/**`, `tests.yml`; 23–30 s; ia
  mengomit `reports/tests.md` **walau merah**.
- Runner: python 3.12.13, numpy 2.5.1, pytest 9.1.1, pandas 2.2.3, pyarrow
  17.0.0, pyyaml 6.0.2. Tidak ada scipy, tidak ada requests. 4 vCPU / 15 GB,
  batas 6 jam. `fapi.binance.com` → 451; `data.binance.vision` → 200.
- Kode keluar: **0** DITOLAK/LULUS · **2** pagar · **3** pengaman mati · **4**
  TIDAK DAPAT DINILAI.

---

## §6 Aturan kerja dengan operator

"lanjut"/"lanjutkan" = teruskan tanpa konfirmasi. Pisahkan fakta terverifikasi
(punya commit / run ID / kutipan) dari asumsi; bila belum terverifikasi,
katakan **"Ini memerlukan verifikasi."** Katakan bila operator salah, katakan
bila diri sendiri salah, jangan menghaluskan ramalan yang meleset. Perbarui
`STATE.md` tiap posisi berubah, tambah entri `journal/` tiap sesi (ditulis
**sebelum** hasil run terlihat bila membahas ramalan), segarkan berkas ini
sebelum konteks penuh.

Nomor ADR bebas: **ADR-039**. Jurnal berikutnya: **`journal/2026-07-27-46.md`**.
