# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi dan dibatasi ~400 baris. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-25 21:30 WIB
**Tahap sekarang:** S2 — Bootstrap, pengukuran runner selesai
**Tahap berikutnya:** S3 — Universe point-in-time

---

## 1. Aturan membaca berkas ini

Dua bagian di bawah dipisahkan dengan sengaja. **Bagian 3 adalah fakta**: setiap barisnya punya bukti yang bisa diperiksa ulang, berupa commit, run ID, atau kutipan dokumentasi. **Bagian 4 adalah asumsi**: belum diukur, dan dilarang diperlakukan sebagai fakta.

Memindahkan baris dari Bagian 4 ke Bagian 3 hanya boleh dilakukan setelah ada bukti yang dilampirkan. Ini bukan formalitas — kegagalan riset sebelumnya berakar pada asumsi yang perlahan diperlakukan sebagai kebenaran tanpa pernah diuji.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, secara sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa.

Seluruh komputasi berjalan di GitHub Actions. Mesin lokal pengguna tidak sanggup melakukan backtest penuh, dan tidak ada VM cloud karena kendala kartu kredit.

---

## 3. Fakta terverifikasi

### Kapasitas runner — diukur, bukan diasumsikan

Sumber: `reports/doctor.json`, run `30161543831`, 2026-07-25.

| Sumber daya | Nilai terukur | Catatan |
|---|---|---|
| vCPU | 4 | AMD EPYC 7763 |
| RAM | 15 GB | |
| **Disk bebas** | **88 GB** | jauh di atas perkiraan 14 GB |

Angka disk mengubah rencana secara material. Anggaran sebelumnya menganggap ~14 GB, yang memaksa ingest dipecah menjadi banyak shard kecil. Dengan 88 GB, seluruh Tier B muat sekaligus, dan bahkan Tier A per-simbol bisa diproses tanpa pemecahan agresif. **Batas 6 jam per job, bukan disk, yang kini menjadi kendala utama.**

### Konektivitas sumber data

| Temuan | Nilai | Implikasi |
|---|---|---|
| CDN `data.binance.vision` | HTTP 200 | jalur unduhan utama berfungsi |
| Endpoint S3 listing | HTTP 200, mengembalikan `CommonPrefixes` | enumerasi simbol dimungkinkan |
| **REST `fapi.binance.com/exchangeInfo`** | **HTTP 451** | **diblokir permanen dari runner** |
| Berkas 1h Jan 2024 | 38.890 byte zip, 91.706 byte CSV, 745 baris | 744 bar + 1 header, bulan lengkap tanpa celah |
| Rasio kompresi zip | 2,36× | |

**HTTP 451 berarti "Unavailable For Legal Reasons".** Runner GitHub berbasis di Amerika Serikat, dan Binance memblokir yurisdiksi itu. Ini bukan galat sementara dan tidak akan hilang dengan mencoba ulang.

Konsekuensinya mengikat: **universe tidak boleh dibangun dari REST API.** Satu-satunya sumber daftar simbol di dalam runner adalah enumerasi arsip S3. Kebetulan ini justru lebih baik secara metodologis — `exchangeInfo` hanya memuat simbol yang aktif hari ini, sehingga membangun universe darinya akan menanamkan survivorship bias sejak baris pertama. Arsip S3 memuat simbol yang sudah delisted.

Snapshot `exchangeInfo` yang sudah ada di Notion (841 simbol, 2026-07-21) tetap berguna sebagai **referensi metadata** untuk tick size, step size, dan minimum notional, karena diambil dari mesin lokal pengguna yang tidak terblokir.

### Infrastruktur

| Fakta | Bukti |
|---|---|
| Repo `EnVyxS/lux-research` publik | id `1312019687` |
| Token bisa menulis berkas biasa | commit `7e513be` |
| Token bisa menulis `.github/workflows/` | commit `4aa7654` |
| Runner bisa commit balik ke `main` | `reports/doctor.json` ada di repo |
| Menit Actions tak terbatas untuk repo publik | `github.com/pricing` |
| Job tunggal dibatasi 6 jam keras | dokumentasi limits GitHub |
| Aset Release dibatasi 2 GB per berkas | diskusi komunitas 146417 |
| Berkas di dalam git dibatasi 100 MB | dokumentasi berkas besar |
| Cron mati otomatis setelah 60 hari tanpa aktivitas | dokumentasi disabling workflows |

### Batas alat yang dimiliki agen

- Agen **tidak bisa** membuat rilis atau mengunggah aset. Parquet harus diunggah runner lewat `gh release upload`.
- Agen **tidak bisa** memicu workflow manual. Pemicu satu-satunya adalah push.
- Agen **tidak bisa** membaca log atau status workflow run. **Solusi yang sudah berjalan: setiap workflow menulis hasilnya ke `reports/` dan meng-commit balik.** Setiap workflow baru wajib mengikuti pola ini, atau hasilnya tidak akan pernah terlihat.
- Sandbox agen **tidak punya jaringan sama sekali**. Semua pengambilan data terjadi di runner.

### Data yang sudah dimiliki

Hanya ~47 MB yang masih persisten. Sisanya perlu diunduh ulang. Dataset lama berperan sebagai **pembanding validasi silang, bukan sumber kebenaran**.

| Artefak persisten | Cakupan | Ukuran |
|---|---|---|
| Index Price Klines 1h | 832 simbol, 2026-06-09 → 07-21 | 17,7 MB |
| Mark Price Klines 1h | 838 simbol, 2026-06-09 → 07-21 | 16,5 MB |
| Open Interest 1h | 841 simbol, 2026-06-30 → 07-21 | 6,7 MB |
| Funding Rate 8h | 841 simbol, 2026-02-04 → 07-21 | 4,0 MB |
| Metadata Futures | 841 exchangeInfo, snapshot 2026-07-21 | 2,2 MB |

Sumber unduhan: `https://data.binance.vision/data/futures/um/...` — **prefix `data/` wajib**, tanpa itu S3 mengembalikan `NoSuchKey`.

### Anomali survivorship yang belum tuntas

Dataset lama berisi 528 simbol, sementara snapshot `exchangeInfo` mencantumkan 841 simbol aktif. Selisih 313 simbol adalah indikasi kuat survivorship bias pada dataset lama. Universe point-in-time yang dibangun di S3 harus menghasilkan **lebih dari 841 simbol historis**; jika tidak, pembangunan universe itu sendiri yang cacat.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi | Status |
|---|---|---|
| Arsip S3 memuat simbol delisted | probe `universe_probe.json` | sedang diukur |
| Jumlah simbol historis > 841 | probe `universe_probe.json` | sedang diukur |
| Throughput unduhan cukup untuk Tier A dalam 6 jam | probe berkas 1m | sedang diukur |
| Tier B (1h + 4h seluruh universe) ≈ 28 juta baris, ≈0,9 GB | ukur setelah ingest pertama | belum |
| Rasio CSV ke Parquet+zstd ≈ 9× | ukur setelah ingest pertama | belum |
| Direktori `metrics/`, `bookTicker/`, `liquidationSnapshot/` tersedia | probe lanjutan | belum |

Catatan: run pertama melaporkan `checksum_ok: false`. **Itu bug milik agen, bukan data rusak** — berkas disimpan dengan nama `probe.zip` sementara berkas `.CHECKSUM` merujuk nama aslinya, sehingga `sha256sum -c` mustahil cocok. Sudah diperbaiki; hasil ulang menunggu.

---

## 5. Penghalang aktif

Tidak ada yang menghentikan pekerjaan saat ini.

Dibutuhkan dari pengguna, tapi belum memblokir:

1. **Token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`, agar runner bisa menulis ke database Run Results dan membangunkan agen pengawas.

Catatan: kebutuhan menjalankan `lux_fetch.ps1 -Phase preflight` di mesin lokal **sudah gugur**. Runner ternyata bisa menjalankan semua probe itu sendiri, jadi mesin lokal tidak lagi berada di jalur kritis.

---

## 6. Tindakan berikutnya

1. Baca `reports/universe_probe.json` untuk menutup dua asumsi teratas.
2. Tulis `lux/binance_vision.py` — klien arsip dengan enumerasi S3, unduhan resumable, dan verifikasi checksum wajib.
3. Bangun universe point-in-time dari arsip. **Gerbang: hasil harus melebihi 841 simbol.** Di bawah itu, berhenti dan selidiki.
4. Ingest Tier B lebih dulu, bukan Tier A. Volume kecil membuat kesalahan pipeline ketahuan murah.
5. Validasi terhadap sembilan gerbang mutu sebelum menyentuh Tier A.

---

## 7. Pengawasan otonom

Agen **LUX Gatekeeper** aktif di Notion. Ia terpicu ketika runner membuat baris baru di database Run Results, lalu menilai hasil terhadap sembilan gerbang mutu: forward-fill, buy-and-hold, entry acak, lookahead, invariant risiko, funding, overlap, checksum, dan survivorship.

Gatekeeper sudah diuji dengan baris sintetis bercacat. Ia menolak baris itu, mengidentifikasi kedua cacat dengan benar, dan menolak mengeluarkan perintah lanjutan.

**Ketika verdict Ditolak, pipeline berhenti.** Agen tidak boleh melanjutkan ke tahap berikutnya.

---

## 8. Arsip

- `reports/` — keluaran mesin dari setiap workflow run. Sumber bukti untuk Bagian 3.
- `journal/` — riwayat lengkap per sesi. Baca hanya bagian yang relevan.
- `decisions/` — ADR. ADR-002 menggantikan bagian penyimpanan pada ADR-001.
- Notion masih menyimpan Constitution riset dan halaman Pelajaran Metodologis.
