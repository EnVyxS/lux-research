# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-26 04:10 WIB (versi 7)
**Tahap sekarang:** S7 **SELESAI** — mesin backtest lengkap dengan sembilan gerbang, dua hipotesis dijalankan sampai putusan, keduanya DITOLAK secara sah
**Tahap berikutnya:** S8 — hipotesis keluarga strategi baru (H-003), bukan penyetelan ulang H-002

---

## 1. Aturan membaca berkas ini

Bagian 3 adalah **fakta**: setiap baris punya bukti berupa commit, run ID, atau kutipan dokumentasi. Bagian 4 adalah **asumsi**: belum diukur, dan dilarang diperlakukan sebagai fakta. Memindahkan baris dari Bagian 4 ke Bagian 3 hanya boleh dengan bukti terlampir.

Lima aturan yang lahir dari kesalahan nyata, bukan dari teori:

1. **Angka yang lulus gerbang belum tentu benar.** Rasio 1h:4h 4,014 pernah dicatat sebagai uji silang yang lulus, padahal sedang melaporkan bug. Gerbang hanya menangkap cacat yang bentuknya sudah dibayangkan.
2. **Sha laporan yang tidak berubah bukan tanda pekerjaan masih berjalan.** Sekali disimpulkan ingest "masih berjalan" padahal job sudah mati merah 21 menit sebelumnya, dan yang menemukan pengguna.
3. **Penjelasan yang membuat anomali terasa wajar harus dicurigai lebih keras daripada anomalinya.**
4. **Lihat sebaran mentah sebelum berteori.** Metrik celah funding gagal lima putaran; satu tabel histogram di awal akan menyelesaikannya dalam satu putaran.
5. **Hipotesis yang ditolak tetap ditolak.** Ambang tidak disetel ulang setelah hasil terlihat; yang boleh dilakukan hanyalah mendaftarkan hipotesis baru dengan ID baru.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa.

Seluruh komputasi berjalan di GitHub Actions. Mesin lokal pengguna tidak sanggup melakukan backtest penuh, dan tidak ada VM cloud karena kendala kartu kredit.

---

## 3. Fakta terverifikasi

### HASIL RISET TERBARU — H-002 DITOLAK DENGAN SEMBILAN GERBANG LULUS

Sumber: `reports/backtest_h002.md` dan `.json`, run **`30174642490`**, commit laporan `858eedc`.

| Besaran | Nilai |
|---|---|
| Putusan | **DITOLAK** |
| Alasan | ekspektasi **0,03159R** < ambang 0,05R |
| Perdagangan luar sampel | 18.883 |
| Total R | 596,44 |
| Jendela positif | 212 / 356 |
| Sembilan gerbang | **semuanya lulus** |
| Durasi | 32,6 detik, 40 simbol |

Saringan ADR-004 yang membedakannya dari H-001b: umur posisi maksimum **168 bar**, carry funding terproyeksi maksimum **0,25R** atas jendela **30 hari**.

| Besaran | H-001b (`30172926477`) | H-002 (`30174642490`) |
|---|---|---|
| Kerugian terburuk (`invarian_risiko`) | −2,5853R (**GAGAL**) | **−1,3215R (lulus)** |
| Rerata `funding_R` | 0,0014 | 0,0005 |
| Perdagangan berbiaya di atas 1R | 1 | **0** |
| Ekspektasi | 0,03086R | 0,03159R |
| Perdagangan | 19.093 | 18.883 |
| Putusan | DITOLAK | DITOLAK |

Alasan keluar H-002: stop 11.909, target 6.707, `akhir_data` 164, `umur` 103. Batas umur benar-benar mengikat, jadi perbaikan invarian risiko tidak seluruhnya berasal dari saringan carry.

**Diagnosis ADR-004 terbukti benar.** Kerugian yang melewati 1R memang berasal dari carry funding, bukan dari fee dan bukan dari cacat mesin. Menutup jalurnya memulihkan invarian risiko tanpa menyentuh satu ambang pun.

**Yang tidak boleh disimpulkan:** bahwa saringannya berhasil. Ekspektasi hanya naik 0,0007R, jauh di dalam derau. Saringan memperbaiki ekor kerugian, bukan keunggulan.

Pertentangan yang paling informatif ada di sini: gerbang `entri_acak` lulus dengan **p 0,0099**, artinya sinyal Donchian secara statistik mengalahkan entri acak, tetapi besarnya hanya 0,032R — sekitar dua pertiga di bawah ambang yang ditulis sebelum data dilihat. Ada keunggulan, dan ukurannya terlalu kecil untuk dibangun di atasnya setelah biaya nyata.

**Kesimpulan yang sudah ditetapkan di muka oleh ADR-004:** breakout Donchian 1 jam tidak punya keunggulan yang memadai pada dataset ini. `maks_umur_bar` dan `maks_carry_R` **tidak** akan disetel ulang untuk mengejar 0,05R.

### H-001b — DITOLAK, tidak dihitung ulang selamanya

Sumber: `reports/backtest_h001.md`, run `30172926477`, commit `88746cf`. Ekspektasi 0,0309R < 0,05R; `invarian_risiko` gagal pada −2,5853R. Sidik hipotesis `e458f4c82abf6735`. Perdagangan terburuk ANIMEUSDT: `kotor_R` −1,013, `transaksi_R` 0,026, `funding_R` **1,545** atas posisi 130 jam — inilah bukti yang melahirkan ADR-004.

### MESIN BACKTEST — sembilan gerbang terpasang dan terbukti bisa gagal

`lux/backtest/engine.py`, `gerbang.py`, `walk_forward.py`, `run_wf.py` (H-001b), `run_h002.py` (H-002). Gerbang: `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`. **Gerbang yang tidak dapat dinilai berarti GAGAL.**

Bukti bahwa gerbangnya bukan hiasan: `invarian_risiko` menjatuhkan H-001b, `checksum` pernah menemukan empat aset asing akibat pola unduh yang dipersempit, `forward_fill` menjatuhkan run pilot lewat panjang deret bar datar sementara rasionya lolos.

Pra-registrasi bersifat **sekali tulis**: menyimpan ulang ID yang sama dengan isi berbeda ditolak dengan galat. Nilai saringan ikut masuk ke sidik hipotesis, sehingga percobaan diam-diam dengan nilai lain akan tertolak.

`run_wf.py` sengaja **tidak** disentuh saat H-002 dibuat, agar angka H-001b tetap dapat diulang. `run_h002.py` mengimpor seluruh fungsi pemuatan dan penilaian dari `run_wf`, jadi kedua hipotesis dinilai oleh kode yang sama.

### MODEL FUNDING NYATA — `lux/funding_model.py`

`Jadwal` per simbol dari `funding_shard*.parquet`; penagihan dihitung dari stempel nyata, bukan dari kisi 8 jam tetap. `statistik_trailing` merangkum rerata rate pada jendela yang **berakhir tepat di saat entri** (tidak boleh melihat masa depan), `carry_terproyeksi_R` menskalakannya dengan kepadatan penagihan. `biaya.funding_interval_jam` sudah **dihapus** dari `config/lux.yaml`, diganti `funding_dari_jadwal_nyata: true` (`5341871`).

### DATASET TIER B PUTARAN 2 — SAH, dasar semua pekerjaan selanjutnya

Sumber: `reports/ingest_tier_b.md` pada commit `16638b4`, `reports/backfill_daily.md` dan `reports/tail_anomali.md` pada `fbead60`.

| Interval | Baris bulanan | Ekor harian | Simbol OK | Gagal | Duplikat | Celah kisi |
|---|---|---|---|---|---|---|
| 1h | **14.106.623** | 439.056 | 790 | 0 | 0 | **112** |
| 4h | **3.526.969** | 109.764 | 790 | 0 | 0 | **112** |

**Total: 14.545.679 bar 1h dan 3.636.733 bar 4h, sekitar 703 MB, 790 dari 790 simbol tanpa satu pun kegagalan.** Rasio baris 1h:4h **3,9996**; rasio terisi ekor harian 1,0 dan 1,0; celah per simbol pada ekor 0,0.

### VALIDASI S5 — `reports/validate_1h.md`, commit `2356684`

14.545.679 baris, 790 simbol, **0 pelanggaran fatal**, 0 duplikat, 112 celah kisi, **447 simbol layak**, 343 ditolak (riwayat pendek 277, likuiditas tipis 77, bar datar 74). Selisih 12.593 baris sudah dijelaskan tuntas: aset `_retry` usang, kini ditolak `POLA_DILARANG` dan dihapus dari Release.

### ADR-003 EKOR DATAR — universe layak v2

Harga terakhir simbol mati disalin sampai ujung dataset. 141 dari 790 simbol berekor datar, 1.081.920 bar dipangkas (7,4%), universe layak 447 → **438** (`reports/universe_layak_v2.json`). Pemangkasan diterapkan **saat muat** lewat `lux/potong_ekor.potong`; aset Parquet tidak pernah ditulis ulang. Tanggal kematian sejati dibaca dari `reports/akhir_sejati.json`.

Akibat terpentingnya bukan bar palsu yang dapat diperdagangkan, melainkan bahwa **gerbang survivorship kehilangan kemampuannya untuk gagal** sebelum ini diperbaiki.

### FUNDING RATE S5b — `reports/funding_check.md`, commit `0448a67`

1.982.017 baris, 447 dari 447 simbol layak, 2020-01-01 → 2026-06-30, 0 duplikat, **3 celah sejati**, funding positif **79,1%**. Kisi bukan sifat tetap simbol: **295 dari 447 hidup di lebih dari satu rezim**; 269 utama di 4 jam, 174 di 8 jam. Jitter stempel maksimum **47 ms** — semua perbandingan waktu wajib memakai toleransi, dan besar pergeseran dilaporkan tersendiri.

Carry ekstrem bagi long: 1000WHYUSDT 60,7%/tahun, 1000000BOBUSDT 60,1%, BROCCOLIF3BUSDT 57,0%; AERGOUSDT −102,6%/tahun bagi short.

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1** (`5f222e8`): `header=0` + `skiprows=1` menghilangkan satu bar per berkas; menyamar sebagai rasio 4,014.
- **Parser 2 dan 3** (`16638b4`): BOM UTF-8 merusak deteksi header (kini `utf-8-sig`); satu baris sampah menggagalkan seluruh berkas (kini `errors="coerce"`).
- **URL non-ASCII**: percent-encoding lewat `bv.seg()`; putaran 2 mencatat 790 dari 790 berhasil.
- **Metrik celah funding**: gagal lima putaran karena mengira kisi funding tetap; penyebab akhirnya jitter 47 ms yang disembunyikan pembulatan empat desimal. **Alat diagnosisnya sendiri yang membutakan.**
- **Circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`), diputus dengan import lazy.

### Universe — `reports/universe.json`

937 simbol pernah ada; **790 perpetual USDT** jadi universe riset; 761 aktif, 29 delisted; 447 layak, **438 setelah ADR-003**. Dataset lama 528 simbol berarti 262 hilang, dan yang hilang bukan sampel acak melainkan simbol yang mati. 129 simbol delisted hadir lengkap dengan riwayatnya, termasuk SRMUSDT sampai 2024-05.

### Pengujian — `reports/tests.md`

**299 pengujian hijau** pada commit `8a29df1`, kode keluar 0, selesai 1,46 detik, seluruhnya tanpa jaringan. Naik dari 268 pada `42a8b79` (18 uji `test_carry.py`, 9 uji `test_run_h002.py`, dan tambahan lain di sesi ini).

CI sudah berkali-kali menangkap kesalahan sebelum satu byte pun diunduh. **Setelah beberapa kali pengujian yang salah, godaan terbesar adalah menganggap setiap uji merah sebagai kesalahan pengujian.**

### Kapasitas runner — `reports/doctor.json`

4 vCPU, 15 GB RAM, 88 GB disk bebas. **Batas 6 jam per job, bukan disk, yang menjadi kendala utama.** Delapan shard paralel, 790 simbol, dua interval selesai ~13 menit. Data 1m sekitar 60× lebih besar, sehingga **Tier A butuh minimal 24 shard**.

### Konektivitas

CDN `data.binance.vision` 200; S3 listing 200; REST `fapi.binance.com` **451 permanen**; checksum SHA256 cocok.

### Batas alat agen dan solusinya

- Agen **tidak bisa** membuat rilis, memicu workflow manual, membaca log, mengunduh artifact, atau melihat status run.
- Setiap workflow diberi filter `paths` pada berkasnya sendiri; **menyunting workflow adalah satu-satunya cara memicunya.**
- **Setiap workflow wajib menulis hasil ke `reports/` dan meng-commit balik** dengan `if: always()`.
- Sandbox agen **tidak punya jaringan**. Gerbang `pytest` wajib berjalan **sebelum** unduhan di setiap workflow.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| Integritas 4h sama bersihnya dengan 1h | jalankan `validate.yml` untuk interval 4h |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap universe layak v2 438 |
| Hasil 40 simbol pertama mewakili 438 simbol | jalankan `--limit 0` sekali, hanya untuk hipotesis yang layak |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |
| `metrics/`, `bookTicker/`, `liquidationSnapshot/` tersedia | belum diprobe |

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 (14.076.257 baris 1h, 3.506.060 baris 4h, 17.169 celah, rasio 4,014); metrik celah funding putaran 1–4 (1.380.741 · 1.193.209 · 587.131 · 266.612); seluruh run pilot H-001 termasuk `30170073890` (0,0317R, 19.060 perdagangan, 604,26R) karena datanya memuat ekor palsu.

---

## 5. Penghalang aktif

Tidak ada yang menghentikan pekerjaan.

Dibutuhkan dari pengguna, belum memblokir: **token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`, agar runner dapat menulis ke database Run Results dan membangunkan agen pengawas.

---

## 6. Tindakan berikutnya

1. **H-003: keluarga strategi baru, didaftarkan sebelum dijalankan.** Donchian sudah diuji sampai tuntas dan keunggulannya nyata tetapi terlalu kecil (0,032R vs ambang 0,05R). Yang sah adalah menguji mekanisme berbeda, bukan menyetel ulang saringan H-002. Ruang parameter tetap wajib kecil dan ditulis di muka.
2. **Perketat `gerbang_lulus` di `lux/funding.py`** supaya celah dan jitter ikut menilai.
3. **Validasi interval 4h** — baru 1h yang dijalankan.
4. **Diff terhadap Dataset G lama (528 simbol)** sebagai uji silang survivorship dari sumber berbeda. Ini satu-satunya butir dari daftar tugas awal pengguna yang benar-benar masih terbuka.
5. `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md`; salin ADR-001 dan ADR-002 ke `decisions/`.
6. Pelapor Notion (`NOTION_TOKEN`) agar LUX Gatekeeper menerima hasil run secara otomatis.
7. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, dengan ≥24 shard.

---

## 7. Pengawasan otonom

Agen **LUX Gatekeeper** aktif di Notion. Terpicu saat runner membuat baris di database Run Results, menilai hasil terhadap sembilan gerbang mutu. Sudah diuji dengan baris sintetis bercacat dan menolak dengan benar. **Verdict Ditolak menghentikan pipeline.**

---

## 8. Peta repo

| Path | Isi |
|---|---|
| `config/lux.yaml` | seluruh parameter yang memengaruhi hasil |
| `lux/binance_vision.py` | klien arsip: listing S3, unduhan, checksum, percent-encoding |
| `lux/universe.py` | universe point-in-time dan klasifikasi jenis kontrak |
| `lux/ingest.py` | ingest Tier B dengan validasi per simbol |
| `lux/backfill_daily.py` | penutup celah ekor dari arsip harian |
| `lux/validate.py` · `lux/validate_run.py` | integritas OHLCV, kelayakan universe, penolak aset `_retry` |
| `lux/funding.py` · `lux/funding_check.py` | ingest funding rate dan metrik kisinya |
| `lux/funding_model.py` | jadwal funding nyata, penagihan, carry terproyeksi |
| `lux/costs.py` | model biaya dalam satuan R |
| `lux/diag_datar.py` · `lux/potong_ekor.py` | diagnosis dan pemangkasan ekor datar (ADR-003) |
| `lux/praregistrasi.py` | hipotesis sekali tulis dan penilaian terhadap kriteria |
| `lux/backtest/engine.py` | mesin eksekusi: stop, target, batas umur, saringan carry |
| `lux/backtest/gerbang.py` | sembilan gerbang mutu |
| `lux/backtest/walk_forward.py` | pemilihan parameter dalam sampel, penilaian di luar sampel |
| `lux/backtest/run_wf.py` | orkestrator H-001b — **jangan disunting**, agar hasilnya tetap dapat diulang |
| `lux/backtest/run_h002.py` | orkestrator H-002 (ADR-004) |
| `tests/` | 299 pengujian tanpa jaringan, wajib hijau sebelum unduhan |
| `reports/` | keluaran mesin tiap run, sumber bukti Bagian 3 |
| `hipotesis/` | pendaftaran sekali tulis: `H-001b.json`, `H-002.json` |
| `decisions/` | ADR-003 (ekor datar), ADR-004 (carry funding) |
| `journal/` | riwayat per sesi |

**Workflow aktif (10):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`.

**Dihapus di S7** karena masukannya artifact yang kedaluwarsa 90 hari sementara keluarannya sudah permanen di `reports/`: `analyze_tail.yml` (`07860a7`), `diagnose.yml` (`f4af734`), `diag_datar.yml` (`41ca693`). `retry_failed.yml` dihapus lebih dulu di `3a206c6`. Modul Python-nya tetap ada; yang dihapus hanya pemicunya.

Release **`tier-b-v1`** memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`. Pola unduh backtest wajib `ohlcv_1h_*.parquet`.
