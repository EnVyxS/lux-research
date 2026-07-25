# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi dan dibatasi ~400 baris. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-25 21:40 WIB
**Tahap sekarang:** S4 — Ingest Tier B sedang berjalan
**Tahap berikutnya:** S5 — Validasi data, lalu backfill ekor harian

---

## 1. Aturan membaca berkas ini

Bagian 3 adalah **fakta**: setiap baris punya bukti yang bisa diperiksa ulang berupa commit, run ID, atau kutipan dokumentasi. Bagian 4 adalah **asumsi**: belum diukur, dan dilarang diperlakukan sebagai fakta.

Memindahkan baris dari Bagian 4 ke Bagian 3 hanya boleh dilakukan dengan bukti terlampir. Kegagalan riset sebelumnya berakar pada asumsi yang perlahan diperlakukan sebagai kebenaran tanpa pernah diuji.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa.

Seluruh komputasi berjalan di GitHub Actions. Mesin lokal pengguna tidak sanggup melakukan backtest penuh, dan tidak ada VM cloud karena kendala kartu kredit.

---

## 3. Fakta terverifikasi

### Universe — sumber: `reports/universe.json`, 2026-07-25T14:35Z

| Ukuran | Nilai |
|---|---|
| Simbol di arsip (pernah ada) | **937** |
| Kontrak perpetual | 872 |
| Kontrak bertanggal (delivery) | 50 |
| Varian SETTLED | 15 |
| **Perpetual USDT — universe riset** | **790** |
| Perpetual USDT masih aktif | 761 |
| Perpetual USDT sudah delisted | 29 |
| Baris point-in-time | 21.789 pasangan simbol-bulan |
| Rentang arsip bulanan | 2020-01 → 2026-06 |
| Simbol tanpa data 1h | 0 |
| Simbol dengan lubang arsip | 2, keduanya SETTLED |

**Universe riset adalah 790 perpetual USDT**, bukan 937. Kontrak bertanggal seperti `BTCUSDT_240329` dikecualikan karena tidak memakai funding rate dan punya tanggal kedaluwarsa, sehingga model biaya perpetual tidak berlaku padanya. Varian SETTLED dikecualikan karena riwayatnya terpotong.

Dataset lama berisi 528 simbol. Terhadap universe riset 790, artinya **262 simbol perpetual USDT hilang** dari upaya sebelumnya, dan yang hilang bukan sampel acak melainkan simbol yang mati.

**Catatan kejujuran tentang gerbang:** gerbang "harus melebihi 841" membandingkan 937 simbol arsip (semua quote, semua jenis kontrak) terhadap 841 simbol aktif dari snapshot `exchangeInfo` (semua quote). Perbandingan itu tidak sepenuhnya setara populasi. Bukti survivorship yang sesungguhnya bukan angka gerbangnya, melainkan **129 simbol delisted yang hadir di arsip lengkap dengan riwayatnya**, termasuk SRMUSDT sampai 2024-05 dan FTTUSDT sampai 2026-06.

### Ekor arsip — temuan yang mengubah rencana ingest

Hipotesis sebelumnya keliru dan sudah gugur. Saya menduga arsip kehilangan September sampai Desember 2019. Pemeriksaan arsip harian membantahnya:

| Simbol | Hari pertama di arsip harian | Bulan pertama di arsip bulanan |
|---|---|---|
| BTCUSDT | 2019-12-31 | 2020-01 |
| ETHUSDT | 2019-12-31 | 2020-01 |
| BCHUSDT | 2019-12-31 | 2020-01 |
| XRPUSDT | 2020-01-06 | 2020-01 |

Arsip memang dimulai 2019-12-31, bukan September 2019. Data tiga bulan pertama futures Binance tidak ada di arsip sama sekali, jadi tidak ada yang bisa diselamatkan. Kehilangan di ujung awal hanya **satu hari**.

Yang justru penting ada di ujung lain: arsip harian mencapai **2026-07-24**, sementara arsip bulanan berhenti di **2026-06**. Ingest yang hanya membaca arsip bulanan akan kehilangan sekitar **24 hari data terbaru**, diam-diam. Ini bukan cacat kecil untuk sistem yang harus diperdagangkan; ini menentukan seberapa mutakhir backtest bisa dibuat. Backfill ekor harian wajib ditambahkan sebelum S5 dinyatakan selesai.

### Kapasitas runner — sumber: `reports/doctor.json`

| Sumber daya | Nilai terukur |
|---|---|
| vCPU | 4 |
| RAM | 15 GB |
| Disk bebas | **88 GB** |
| CPU | bervariasi antar run: EPYC 7763 dan EPYC 9V74 |

Disk 88 GB, bukan 14 GB seperti yang diperkirakan. Sharding agresif tidak diperlukan. **Batas 6 jam per job, bukan disk, yang menjadi kendala utama.**

Model CPU berbeda antar run. Setiap tolok ukur berbasis waktu harus mencatat model CPU-nya, atau perbandingan antar run tidak sah.

### Konektivitas

| Temuan | Nilai | Implikasi |
|---|---|---|
| CDN `data.binance.vision` | 200 | jalur unduhan utama |
| S3 listing | 200, `CommonPrefixes` | satu-satunya sumber universe |
| REST `fapi.binance.com` | **451** | diblokir permanen dari runner |
| Checksum SHA256 | cocok | verifikasi berfungsi |
| Berkas 1h Jan 2024 | 745 baris = 744 bar + header | bulan lengkap |

HTTP 451 berarti diblokir atas dasar hukum; runner GitHub berbasis di AS. Ini permanen. Snapshot `exchangeInfo` dari mesin lokal pengguna tetap dipakai, tapi hanya sebagai referensi metadata tick size, step size, dan minimum notional.

### Infrastruktur

| Fakta | Bukti |
|---|---|
| Repo `EnVyxS/lux-research` publik | id `1312019687` |
| Token bisa menulis berkas dan workflow | commit `7e513be`, `4aa7654` |
| Runner bisa commit balik ke `main` | `reports/` terisi |
| Menit Actions tak terbatas untuk repo publik | `github.com/pricing` |
| Job dibatasi 6 jam keras | dokumentasi limits GitHub |
| Aset Release 2 GB per berkas | diskusi komunitas 146417 |
| Berkas git 100 MB | dokumentasi berkas besar |
| Cron mati setelah 60 hari tanpa aktivitas | dokumentasi disabling workflows |

### Batas alat agen dan solusinya

- Agen **tidak bisa** membuat atau mengunggah rilis. Runner melakukannya lewat `gh release upload`.
- Agen **tidak bisa** memicu workflow manual. Pemicu satu-satunya adalah push, jadi setiap workflow diberi filter `paths` pada berkasnya sendiri.
- Agen **tidak bisa** membaca log workflow. **Solusi wajib: setiap workflow menulis hasil ke `reports/` dan meng-commit balik.** Workflow yang tidak mengikuti pola ini hasilnya tidak akan pernah terlihat.
- Sandbox agen **tidak punya jaringan**. Semua pengambilan data terjadi di runner.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| Tier B ≈ 28 juta baris, ≈0,9 GB | `reports/ingest_tier_b.json` |
| Rasio CSV ke Parquet+zstd ≈ 9× | sama |
| Throughput cukup untuk Tier A dalam 6 jam | ukur dari durasi shard Tier B |
| Arsip harian punya cakupan simbol setara arsip bulanan | belum diperiksa |
| `metrics/`, `bookTicker/`, `liquidationSnapshot/` tersedia | belum |
| Funding rate tersedia untuk seluruh 790 perp | belum |

Throughput 1,30 MiB/s yang terukur di `doctor.json` **tidak boleh dipakai**. Berkas ujinya hanya 1,9 MB sehingga waktunya didominasi latensi, bukan bandwidth.

---

## 5. Penghalang aktif

Tidak ada yang menghentikan pekerjaan.

Dibutuhkan dari pengguna, belum memblokir: **token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`, agar runner dapat menulis ke database Run Results dan membangunkan agen pengawas.

---

## 6. Tindakan berikutnya

1. Baca `reports/ingest_tier_b.json` setelah ingest selesai. Gerbang: nol duplikat, nol simbol gagal.
2. **Tambahkan backfill ekor harian** untuk menutup 2026-07-01 sampai hari ini, plus 2019-12-31. Tanpa ini data selalu tertinggal sebulan.
3. Bandingkan hasil terhadap Dataset G lama sebagai uji silang independen.
4. Ingest funding rate; tanpa itu model biaya perpetual tidak lengkap.
5. Baru setelah semua gerbang lulus, pertimbangkan Tier A (1m).

---

## 7. Pengawasan otonom

Agen **LUX Gatekeeper** aktif di Notion. Terpicu saat runner membuat baris di database Run Results, menilai hasil terhadap sembilan gerbang mutu: forward-fill, buy-and-hold, entry acak, lookahead, invariant risiko, funding, overlap, checksum, survivorship.

Sudah diuji dengan baris sintetis bercacat; menolak dengan benar dan menolak mengeluarkan perintah lanjutan.

**Verdict Ditolak menghentikan pipeline.**

---

## 8. Peta repo

| Path | Isi |
|---|---|
| `lux/binance_vision.py` | klien arsip: listing S3, unduhan resumable, verifikasi checksum |
| `lux/universe.py` | universe point-in-time dan klasifikasi jenis kontrak |
| `lux/ingest.py` | ingest Tier B dengan validasi per simbol |
| `lux/summarize.py` | agregasi laporan antar shard |
| `reference/` | parquet universe |
| `reports/` | keluaran mesin tiap run, sumber bukti Bagian 3 |
| `journal/` | riwayat per sesi |
| `decisions/` | ADR |
