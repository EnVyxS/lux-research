# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-26 04:30 WIB (versi 8)
**Tahap sekarang:** S8 **SELESAI** — tiga hipotesis dijalankan sampai putusan, ketiganya DITOLAK secara sah; kerangka eksekusi terbukti **bukan** penyebab kegagalan
**Tahap berikutnya:** S9 — menyerang sumber keunggulan, bukan sinyal harga keempat

---

## 1. Aturan membaca berkas ini

Bagian 3 adalah **fakta**: setiap baris punya bukti berupa commit, run ID, atau kutipan dokumentasi. Bagian 4 adalah **asumsi**: belum diukur, dan dilarang diperlakukan sebagai fakta. Memindahkan baris dari Bagian 4 ke Bagian 3 hanya boleh dengan bukti terlampir.

Lima aturan yang lahir dari kesalahan nyata, bukan dari teori:

1. **Angka yang lulus gerbang belum tentu benar.** Rasio 1h:4h 4,014 pernah dicatat sebagai uji silang yang lulus, padahal sedang melaporkan bug. Gerbang hanya menangkap cacat yang bentuknya sudah dibayangkan.
2. **Sha laporan yang tidak berubah bukan tanda pekerjaan masih berjalan.** Sekali disimpulkan ingest "masih berjalan" padahal job sudah mati merah 21 menit sebelumnya, dan yang menemukan pengguna.
3. **Penjelasan yang membuat anomali terasa wajar harus dicurigai lebih keras daripada anomalinya.**
4. **Lihat sebaran mentah sebelum berteori.** Metrik celah funding gagal lima putaran; satu tabel histogram di awal akan menyelesaikannya dalam satu putaran.
5. **Hipotesis yang ditolak tetap ditolak.** Ambang tidak disetel ulang setelah hasil terlihat; yang boleh dilakukan hanyalah mendaftarkan hipotesis baru dengan ID baru.

Aturan keenam, lahir di sesi ini: **percobaan yang dirancang agar informatif ke dua arah lebih berharga daripada percobaan yang dirancang agar berhasil.** H-003 gagal jauh lebih telak daripada H-002, dan justru karena itu ia mengajarkan sesuatu yang tidak bisa diajarkan oleh keberhasilan.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa.

Seluruh komputasi berjalan di GitHub Actions. Mesin lokal pengguna tidak sanggup melakukan backtest penuh, dan tidak ada VM cloud karena kendala kartu kredit.

---

## 3. Fakta terverifikasi

### HASIL RISET TERBARU — H-003 DITOLAK TELAK, DAN ITULAH TEMUANNYA

Sumber: `reports/backtest_h003.md` dan `.json`, run **`30175179866`**, commit kode `cd943f8`, commit laporan `15162e7`. ADR-005. Sidik hipotesis `3a1cdc867f61bf67`.

H-003 menguji **pembalikan jangka pendek**: membeli penutupan yang jatuh dua simpangan baku di bawah rerata bergulir, menjual yang melonjak dua simpangan baku di atasnya. Jendela 24, 72, 168 bar; tiga kombinasi; ambang z 2,0 ditetapkan di muka dan tidak dicari.

| Besaran | Nilai |
|---|---|
| Putusan | **DITOLAK** |
| Ekspektasi | **−0,24782R** |
| Total R | **−7.176,60** |
| Perdagangan luar sampel | 28.959 |
| Jendela positif | **25 / 356** |
| Gerbang gagal | `buy_and_hold`, `entri_acak`, `invarian_risiko` |
| Durasi | 43,6 detik, 40 simbol |

Gerbang `entri_acak` **p 1,0000**: seluruh 100 permutasi menyamai atau melampaui sinyal nyata. Entri acak lebih baik daripada pembalikan jangka pendek pada dataset ini.

### Temuan utama: asimetri 0,28R membuktikan kerangkanya bukan tertuduh

ADR-005 ditulis sebelum angka apa pun ada, dan menyebut dua tafsiran yang tidak dapat dipisahkan oleh data lama:

1. Arah taruhan H-001b salah, dan yang tersisa di pasar justru pembalikan.
2. Kerangkanya yang membatasi — stop 2×ATR, target 2R, biaya nyata menyisakan terlalu sedikit ruang bagi mekanisme apa pun.

**Keduanya salah, dan cara gagalnya yang menjawab.** Pada kerangka eksekusi yang identik bita demi bita, kelanjutan menghasilkan **+0,0316R** dan pembalikan menghasilkan **−0,2478R**. Rentang 0,28R antara dua mekanisme berlawanan itu mustahil muncul dari kerangka yang meredam segalanya. Kerangka ini **meneruskan** informasi arah dengan baik; tafsiran 2 terfalsifikasi oleh percobaannya sendiri.

Tafsiran 1 juga terfalsifikasi, dan lebih keras: arah taruhan H-001b bukan hanya benar, ia satu-satunya arah yang punya tanda positif. Keunggulan kecil Donchian (p 0,0099, 0,032R) adalah **informasi arah yang nyata**, hanya terlalu tipis untuk menutup biaya. Kegagalan cermin H-003 adalah bukti pendukung terkuat yang dimiliki H-002 sampai hari ini.

**Yang tidak boleh disimpulkan:** bahwa membalik tanda H-003 menghasilkan strategi menguntungkan. Membalik tanda sinyal pembalikan tidak menghasilkan Donchian, dan biaya transaksi tetap dibayar ke arah mana pun taruhan dipasang. Ini hipotesis baru dan harus didaftarkan seperti hipotesis baru.

### Cacat yang ditemukan H-003 pada saringan ADR-004

`invarian_risiko` H-003 **GAGAL pada −1,8637R** meski saringan carry aktif. Perdagangan terburuk AKTUSDT: `kotor_R` −1,010, `funding_R` **0,833**, 77 jam, stop 5,064% dari harga.

`carry_terproyeksi_R` adalah **proyeksi dari rerata 30 hari terakhir, bukan jaminan**. Ketika rate melonjak setelah entri, atau ketika stop sangat lebar sehingga funding per R membesar, saringan itu tembus. Pada H-002 kebetulan tidak ada kasus yang menembusnya; pada 28.959 perdagangan H-003 ada. **Lulusnya gerbang pada satu hipotesis bukan bukti gerbang itu tidak bisa gagal pada hipotesis lain.**

Rerata `funding_R` H-003 adalah **−0,0017** — negatif, artinya posisi pembalikan rata-rata justru **menerima** funding. Ia tetap rugi telak. Funding bukan penyebab kegagalan H-003; arah sinyalnyalah penyebabnya.

### H-002 — DITOLAK, sembilan gerbang lulus

Sumber: `reports/backtest_h002.md`, run **`30174642490`**, commit laporan `858eedc`. Ekspektasi **0,03159R** < 0,05R. 18.883 perdagangan, 596,44R, 212/356 jendela positif, 32,6 detik. Saringan ADR-004: umur maksimum 168 bar, carry terproyeksi maksimum 0,25R atas jendela 30 hari.

| Besaran | H-001b | H-002 | H-003 |
|---|---|---|---|
| Mekanisme | Donchian | Donchian + saringan carry | pembalikan skor-z |
| Ekspektasi R | 0,03086 | **0,03159** | **−0,24782** |
| Total R | 589,17 | 596,44 | −7.176,60 |
| Perdagangan | 19.093 | 18.883 | 28.959 |
| Jendela positif | 208/356 | 212/356 | 25/356 |
| `invarian_risiko` | −2,5853 GAGAL | −1,3215 lulus | −1,8637 GAGAL |
| `entri_acak` p | — | 0,0099 lulus | 1,0000 GAGAL |
| Putusan | DITOLAK | DITOLAK | DITOLAK |

Dataset, kriteria, limit 40 simbol, dan kode penilaian identik pada ketiganya. Itulah yang membuat perbandingan di atas sah.

Alasan keluar H-002: stop 11.909, target 6.707, `akhir_data` 164, `umur` 103. H-003: stop 20.997, target 7.503, `akhir_data` 258, `umur` 201.

**Diagnosis ADR-004 terbukti benar** untuk H-002: kerugian yang melewati 1R berasal dari carry funding, bukan fee dan bukan cacat mesin. Ekspektasi hanya naik 0,0007R — saringan memperbaiki ekor kerugian, bukan keunggulan.

### H-001b — DITOLAK, tidak dihitung ulang selamanya

Sumber: `reports/backtest_h001.md`, run `30172926477`, commit `88746cf`. Ekspektasi 0,0309R; `invarian_risiko` gagal pada −2,5853R. Sidik `e458f4c82abf6735`. Perdagangan terburuk ANIMEUSDT: `funding_R` **1,545** atas posisi 130 jam — bukti yang melahirkan ADR-004.

### MESIN BACKTEST — sembilan gerbang terpasang dan terbukti bisa gagal

`lux/backtest/engine.py`, `gerbang.py`, `walk_forward.py`, `run_wf.py` (H-001b), `run_h002.py`, `run_h003.py`. Gerbang: `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`. **Gerbang yang tidak dapat dinilai berarti GAGAL.**

Bukti bahwa gerbangnya bukan hiasan, kini dari tiga hipotesis: `invarian_risiko` menjatuhkan H-001b dan H-003; `entri_acak` dan `buy_and_hold` menjatuhkan H-003; `checksum` pernah menemukan empat aset asing akibat pola unduh yang dipersempit; `forward_fill` menjatuhkan run pilot lewat panjang deret bar datar sementara rasionya lolos.

Pra-registrasi bersifat **sekali tulis**. Nilai saringan ikut masuk ke sidik hipotesis, sehingga percobaan diam-diam dengan nilai lain akan tertolak.

Pola orkestrator sudah mapan: satu hipotesis, satu orkestrator, dibekukan setelah dijalankan, seluruh fungsi pemuatan dan penilaian diimpor dari `run_wf`. **Tiga salinan adalah batas wajar; orkestrator keempat harus didahului ekstraksi runner bersama.**

### MODEL FUNDING NYATA — `lux/funding_model.py`

`Jadwal` per simbol dari `funding_shard*.parquet`; penagihan dihitung dari stempel nyata, bukan kisi 8 jam tetap. `statistik_trailing` merangkum rerata rate pada jendela yang **berakhir tepat di saat entri**; `carry_terproyeksi_R` menskalakannya dengan kepadatan penagihan. `biaya.funding_interval_jam` sudah dihapus dari `config/lux.yaml`, diganti `funding_dari_jadwal_nyata: true` (`5341871`).

### DATASET TIER B PUTARAN 2 — SAH, dasar semua pekerjaan selanjutnya

Sumber: `reports/ingest_tier_b.md` pada `16638b4`, `reports/backfill_daily.md` dan `reports/tail_anomali.md` pada `fbead60`.

| Interval | Baris bulanan | Ekor harian | Simbol OK | Gagal | Duplikat | Celah kisi |
|---|---|---|---|---|---|---|
| 1h | **14.106.623** | 439.056 | 790 | 0 | 0 | **112** |
| 4h | **3.526.969** | 109.764 | 790 | 0 | 0 | **112** |

**Total 14.545.679 bar 1h dan 3.636.733 bar 4h, sekitar 703 MB, 790 dari 790 simbol tanpa satu pun kegagalan.** Rasio 1h:4h **3,9996**.

### VALIDASI S5 — `reports/validate_1h.md`, commit `2356684`

14.545.679 baris, 790 simbol, **0 pelanggaran fatal**, 0 duplikat, 112 celah kisi, **447 simbol layak**, 343 ditolak. Selisih 12.593 baris dijelaskan tuntas: aset `_retry` usang, kini ditolak `POLA_DILARANG`.

### ADR-003 EKOR DATAR — universe layak v2

141 dari 790 simbol berekor datar, 1.081.920 bar dipangkas (7,4%), universe layak 447 → **438** (`reports/universe_layak_v2.json`). Pemangkasan diterapkan saat muat lewat `lux/potong_ekor.potong`; aset Parquet tidak pernah ditulis ulang.

### FUNDING RATE S5b — `reports/funding_check.md`, commit `0448a67`

1.982.017 baris, 447 dari 447 simbol layak, 2020-01-01 → 2026-06-30, 0 duplikat, **3 celah sejati**, funding positif **79,1%**. **295 dari 447 simbol hidup di lebih dari satu rezim kisi.** Jitter stempel maksimum **47 ms**.

Carry ekstrem bagi long: 1000WHYUSDT 60,7%/tahun, 1000000BOBUSDT 60,1%, BROCCOLIF3BUSDT 57,0%; AERGOUSDT −102,6%/tahun bagi short.

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1** (`5f222e8`): `header=0` + `skiprows=1` menghilangkan satu bar per berkas; menyamar sebagai rasio 4,014.
- **Parser 2 dan 3** (`16638b4`): BOM UTF-8 (kini `utf-8-sig`); satu baris sampah menggagalkan seluruh berkas (kini `errors="coerce"`).
- **URL non-ASCII**: percent-encoding lewat `bv.seg()`.
- **Metrik celah funding**: gagal lima putaran karena mengira kisi funding tetap; penyebabnya jitter 47 ms yang disembunyikan pembulatan empat desimal. **Alat diagnosisnya sendiri yang membutakan.**
- **Circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`), diputus dengan import lazy.

### Universe — `reports/universe.json`

937 simbol pernah ada; **790 perpetual USDT** jadi universe riset; 761 aktif, 29 delisted; 447 layak, **438 setelah ADR-003**. Dataset lama 528 simbol berarti 262 hilang, dan yang hilang bukan sampel acak melainkan simbol yang mati.

### Pengujian — `reports/tests.md`

**318 pengujian hijau** pada commit `5dda655`, kode keluar 0, 1,26 detik, seluruhnya tanpa jaringan. Naik dari 299 (`8a29df1`) lewat `test_reversi.py` (12) dan `test_run_h003.py` (7).

### Kapasitas runner — `reports/doctor.json`

4 vCPU, 15 GB RAM, 88 GB disk bebas. **Batas 6 jam per job, bukan disk, yang menjadi kendala utama.** Backtest 40 simbol selesai di bawah satu menit; **Tier A butuh minimal 24 shard**.

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
| Keunggulan kelanjutan membesar pada horizon lebih panjang (4h) | jalankan hipotesis baru pada 4h setelah validasi 4h |
| Funding sebagai **sinyal** memuat informasi arah, bukan hanya biaya | uji hipotesis berbasis funding, belum pernah dilakukan |
| Integritas 4h sama bersihnya dengan 1h | jalankan `validate.yml` untuk interval 4h |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap universe layak v2 438 |
| Hasil 40 simbol pertama mewakili 438 simbol | jalankan `--limit 0` sekali, hanya untuk hipotesis yang layak |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 (14.076.257 baris 1h, 3.506.060 baris 4h, 17.169 celah, rasio 4,014); metrik celah funding putaran 1–4 (1.380.741 · 1.193.209 · 587.131 · 266.612); seluruh run pilot H-001 termasuk `30170073890` (0,0317R, 19.060 perdagangan, 604,26R) karena datanya memuat ekor palsu.

---

## 5. Penghalang aktif

Tidak ada yang menghentikan pekerjaan.

Dibutuhkan dari pengguna, belum memblokir: **token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`, agar runner dapat menulis ke database Run Results dan membangunkan agen pengawas.

---

## 6. Tindakan berikutnya

Tiga hipotesis sinyal harga sudah dijalankan sampai putusan. ADR-005 melarang hipotesis harga keempat sebagai reaksi terhadap kegagalan H-003, dan larangan itu berlaku.

Dua arah yang sah, keduanya menyerang hal yang belum pernah disentuh, dan masing-masing wajib didahului ADR sebelum kodenya ditulis:

1. **Horizon.** Keunggulan kelanjutan nyata tetapi tipis (0,032R) sementara biaya transaksi rerata 0,0345R. Biaya per perdagangan hampir menelan seluruh keunggulan. Horizon lebih panjang membagi biaya yang sama ke pergerakan yang lebih besar. **Prasyarat: validasi 4h** — tanpa itu, hasil 4h tidak boleh dipercaya.
2. **Sumber data yang belum dipakai sebagai sinyal.** Funding selama ini hanya diperlakukan sebagai biaya. 79,1% penagihan positif dan carry ekstrem sampai −533,9%/tahun adalah struktur yang belum pernah diuji kandungan informasi arahnya.

Sisanya, tidak memblokir:

3. Perketat `gerbang_lulus` di `lux/funding.py` supaya celah dan jitter ikut menilai.
4. Perbaiki docstring `lux/costs.py` yang masih menyebut pembagi funding 8 jam tetap.
5. Diff terhadap Dataset G lama (528 simbol). **Satu-satunya butir dari daftar tugas awal pengguna yang benar-benar masih terbuka.**
6. `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md`; salin ADR-001 dan ADR-002 ke `decisions/`.
7. Pelapor Notion (`NOTION_TOKEN`) agar LUX Gatekeeper menerima hasil run otomatis.
8. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, dengan ≥24 shard.

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
| `lux/strategi/breakout_atr.py` | sinyal kelanjutan (H-001b, H-002) |
| `lux/strategi/reversi_zskor.py` | sinyal pembalikan (H-003), arah berlawanan |
| `lux/backtest/engine.py` | mesin eksekusi: stop, target, batas umur, saringan carry |
| `lux/backtest/gerbang.py` | sembilan gerbang mutu |
| `lux/backtest/walk_forward.py` | pemilihan parameter dalam sampel, penilaian di luar sampel |
| `lux/backtest/run_wf.py` | orkestrator H-001b — **jangan disunting** |
| `lux/backtest/run_h002.py` | orkestrator H-002 (ADR-004) — dibekukan |
| `lux/backtest/run_h003.py` | orkestrator H-003 (ADR-005) — dibekukan |
| `tests/` | **318** pengujian tanpa jaringan, wajib hijau sebelum unduhan |
| `reports/` | keluaran mesin tiap run, sumber bukti Bagian 3 |
| `hipotesis/` | pendaftaran sekali tulis: `H-001b`, `H-002`, `H-003` |
| `decisions/` | ADR-003 (ekor datar), ADR-004 (carry funding), ADR-005 (pembalikan) |
| `journal/` | riwayat per sesi |

**Workflow aktif (10):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`.

**Dihapus di S7** karena masukannya artifact yang kedaluwarsa 90 hari sementara keluarannya sudah permanen di `reports/`: `analyze_tail.yml` (`07860a7`), `diagnose.yml` (`f4af734`), `diag_datar.yml` (`41ca693`). `retry_failed.yml` dihapus lebih dulu di `3a206c6`. Modul Python-nya tetap ada.

Release **`tier-b-v1`** memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`. Pola unduh backtest wajib `ohlcv_1h_*.parquet`.
