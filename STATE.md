# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi dan dibatasi ~400 baris. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-25 23:05 WIB
**Tahap sekarang:** S4 — Ingest Tier B **putaran 2** sedang berjalan (putaran 1 dinyatakan tidak sah)
**Tahap berikutnya:** jalankan ulang backfill ekor, lalu S5 — validasi data

---

## 1. Aturan membaca berkas ini

Bagian 3 adalah **fakta**: setiap baris punya bukti yang bisa diperiksa ulang berupa commit, run ID, atau kutipan dokumentasi. Bagian 4 adalah **asumsi**: belum diukur, dan dilarang diperlakukan sebagai fakta.

Memindahkan baris dari Bagian 4 ke Bagian 3 hanya boleh dilakukan dengan bukti terlampir. Kegagalan riset sebelumnya berakar pada asumsi yang perlahan diperlakukan sebagai kebenaran tanpa pernah diuji.

Aturan tambahan yang lahir dari sesi ini: **angka yang lulus gerbang belum tentu benar.** Rasio 1h:4h sebesar 4,014 pernah saya catat sebagai uji silang yang lulus, padahal ia sedang melaporkan sebuah bug. Gerbang hanya menangkap cacat yang bentuknya sudah dibayangkan.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa.

Seluruh komputasi berjalan di GitHub Actions. Mesin lokal pengguna tidak sanggup melakukan backtest penuh, dan tidak ada VM cloud karena kendala kartu kredit.

---

## 3. Fakta terverifikasi

### CACAT PARSER HEADER — temuan terpenting sesi ini

Sumber: `reports/tail_anomali.json`, diperbaiki di commit `5f222e8`.

`baca_zip` memakai `header=0` dan `skiprows=1` bersamaan pada berkas CSV berheader. `skiprows` membuang baris header, lalu `header=0` memperlakukan baris **data pertama** sebagai nama kolom dan membuangnya juga. Akibatnya **tepat satu bar hilang dari setiap berkas berheader**.

Bukti aritmetika dari backfill ekor harian:

| Interval | Hari ditambal | Baris | Seharusnya | Rasio terisi | Pecahan tepat |
|---|---|---|---|---|---|
| 1h | 18.222 | 419.109 | 437.328 | 0,9583 | 23/24 |
| 4h | 18.222 | 91.113 | 109.332 | 0,8334 | 5/6 |

Jumlah hari yang ditambal identik untuk kedua interval, jadi arsip Binance tidak bersalah. Rasio baris 1h:4h keluar 4,5999, yaitu tepat 23/5.

**Konsekuensi:** seluruh aset Parquet putaran 1 tidak sah. Pada berkas bulanan kerugiannya hanya 1 dari 720 bar (0,14%) sehingga lolos dua putaran penuh, dan rasio 4,014 yang tampak sehat sebenarnya adalah (720−1)/(180−1) = 4,017. Bar yang hilang selalu bar **pertama tiap bulan**, jadi ini bias sistematis, bukan derau acak.

Yang menemukannya bukan pembacaan ulang kode, melainkan invarian aritmetika sepele pada arsip berukuran kecil. Skala kecil membesarkan cacat 0,14% menjadi 17% sampai tak bisa disembunyikan. Ini alasan Tier B dikerjakan sebelum Tier A, dan alasan itu kini terbukti dua kali.

### Cacat URL non-ASCII — selesai

Tiga perpetual bernama huruf Han (`币安人生USDT`, `我踏马来了USDT`, `龙虾USDT`) gagal total pada putaran 1. Penyebabnya `klines_url()` tidak melakukan percent-encoding pada segmen path, sementara listing S3 lolos karena `urlencode` sudah meng-encode parameternya. Kegagalan asimetris: simbol masuk universe, unduhan nol persen.

Diperbaiki lewat helper `bv.seg()`. Terbukti pada `reports/ingest_retry.md`: 12.593 baris 1h dan 3.136 baris 4h, nol gagal, rasio 4,016.

Rata-rata riwayat ketiganya hanya ~4.200 bar 1h (~175 hari), sehingga ambang `min_bar_1h: 8760` di `config/lux.yaml` mengeluarkannya dari universe backtest **berdasarkan aturan yang ditulis sebelum angkanya dilihat**, bukan karena namanya aneh.

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

Universe riset tidak terpengaruh cacat parser, karena ia dibangun dari enumerasi nama berkas, bukan dari isinya.

Dataset lama berisi 528 simbol. Terhadap universe riset 790, artinya **262 simbol perpetual USDT hilang** dari upaya sebelumnya, dan yang hilang bukan sampel acak melainkan simbol yang mati.

**Catatan kejujuran tentang gerbang:** gerbang "harus melebihi 841" membandingkan 937 simbol arsip terhadap 841 simbol aktif dari snapshot `exchangeInfo`. Perbandingan itu tidak setara populasi. Bukti survivorship yang sesungguhnya adalah **129 simbol delisted yang hadir lengkap dengan riwayatnya**, termasuk SRMUSDT sampai 2024-05 dan FTTUSDT sampai 2026-06.

### Ekor arsip

Arsip bulanan berhenti di **2026-06**, arsip harian mencapai **2026-07-24**. Ingest yang hanya membaca arsip bulanan kehilangan ~24 hari terbaru tanpa tanda apa pun. `lux/backfill_daily.py` menutupnya dengan aturan umum: bandingkan bulan yang ada di arsip bulanan dengan bulan yang ada di arsip harian, unduh harian hanya untuk bulan yang tidak tercakup. Bukan tambalan tanggal, jadi tidak perlu disentuh lagi bulan depan.

Hipotesis lama "Sep–Des 2019 hilang" sudah gugur: arsip harian majors mulai 2019-12-31, dan kehilangan di ujung awal hanya satu hari. Tiga bulan pertama futures Binance tidak ada di arsip sama sekali.

### Model biaya — `lux/costs.py`, `config/lux.yaml`

Biaya dinyatakan dalam satuan R, bukan persen harga, supaya sebanding langsung dengan target keuntungan. `cost_R = 2·(fee+slippage)/stop_frac`; `funding_R = rate·(jam/8)/stop_frac` dengan tanda berbalik untuk short; `winrate_impas = (1+biaya_R)/(imbalan+1)`.

Angka yang layak diingat: stop 0,1% dengan biaya bolak-balik 0,2% menghabiskan 2R sebelum posisi bergerak, sehingga titik impas pada imbalan 2R tepat 100% — mati secara aritmetika. `layak_secara_biaya()` menolak konfigurasi semacam itu **sebelum** backtest dijalankan, karena mesin backtest akan patuh menggambar kurva ekuitas untuk parameter yang mustahil.

Seluruh parameter yang memengaruhi hasil ada di `config/lux.yaml`, tidak tersebar sebagai konstanta di kode. Parameter tersembunyi adalah jalur paling umum masuknya overfitting tanpa jejak.

### Pengujian — `reports/tests.md`

28 pengujian, semuanya tanpa jaringan, berjalan dalam hitungan milidetik: 16 untuk model biaya, 12 untuk parser dengan ZIP sintetis. Dua di antaranya menjaga invarian yang menyingkap bug: jumlah bar tidak boleh berubah karena keberadaan header, dan rasio 1h:4h harus tepat 4,0.

Pengujian kini berjalan **di dalam** job ingest sebelum satu byte pun diunduh. Pada putaran pertama, tidak ada satu pun pengujian yang jalan sebelum job 18 menit dimulai.

CI juga sudah menangkap kesalahan saya sendiri: sebuah asersi menuntut `winrate_impas(2,2) > 1.0` padahal aritmetikanya tepat 1,0. Yang salah asersinya, bukan implementasinya. Pengujian yang menuntut hal keliru berbahaya karena mengundang orang menambal kode yang sudah benar.

### Kapasitas runner — sumber: `reports/doctor.json`

| Sumber daya | Nilai terukur |
|---|---|
| vCPU | 4 |
| RAM | 15 GB |
| Disk bebas | **88 GB** |
| CPU | bervariasi antar run: EPYC 7763 dan EPYC 9V74 |

Disk 88 GB, bukan 14 GB seperti diperkirakan. **Batas 6 jam per job, bukan disk, yang menjadi kendala utama.** Model CPU berbeda antar run, jadi setiap tolok ukur berbasis waktu wajib mencatat model CPU-nya.

Durasi terukur putaran 1: delapan shard paralel, 790 simbol, dua interval, selesai ~18 menit; shard terlama 554,7 detik untuk bagian 1h saja. Data 1m sekitar 60× lebih besar, sehingga satu shard akan menembus batas 6 jam. **Tier A butuh minimal 24 shard, bukan 8.**

### Konektivitas

| Temuan | Nilai | Implikasi |
|---|---|---|
| CDN `data.binance.vision` | 200 | jalur unduhan utama |
| S3 listing | 200, `CommonPrefixes` | satu-satunya sumber universe |
| REST `fapi.binance.com` | **451** | diblokir permanen dari runner |
| Checksum SHA256 | cocok | verifikasi berfungsi |

HTTP 451 berarti diblokir atas dasar hukum; runner GitHub berbasis di AS. Snapshot `exchangeInfo` dari mesin lokal pengguna tetap dipakai, tapi hanya sebagai referensi tick size, step size, dan minimum notional.

### Infrastruktur

| Fakta | Bukti |
|---|---|
| Repo `EnVyxS/lux-research` publik | id `1312019687` |
| Token bisa menulis berkas dan workflow | commit `7e513be`, `4aa7654` |
| Runner bisa commit balik ke `main` | `reports/` terisi |
| Runner bisa membaca artifact run lain | `diagnose.yml`, `analyze_tail.yml` |
| Menit Actions tak terbatas untuk repo publik | `github.com/pricing` |
| Job dibatasi 6 jam keras | dokumentasi limits GitHub |
| Aset Release 2 GB per berkas | diskusi komunitas 146417 |
| Cron mati setelah 60 hari tanpa aktivitas | dokumentasi disabling workflows |

### Batas alat agen dan solusinya

- Agen **tidak bisa** membuat atau mengunggah rilis. Runner melakukannya lewat `gh release upload`.
- Agen **tidak bisa** memicu workflow manual. Pemicu satu-satunya adalah push, jadi setiap workflow diberi filter `paths` pada berkasnya sendiri.
- Agen **tidak bisa** membaca log workflow. **Setiap workflow wajib menulis hasil ke `reports/` dan meng-commit balik.** Workflow yang tidak mengikuti pola ini hasilnya tidak akan pernah terlihat.
- Agen **tidak bisa** mengunduh artifact, tapi runner bisa. `gh run list` plus `gh run download` di dalam runner membuat artifact run mana pun terbaca secara tidak langsung, jauh lebih murah daripada mengulang pekerjaan. Pola ini yang memungkinkan diagnosis cacat parser tanpa mengunduh ulang data.
- Sandbox agen **tidak punya jaringan**. Semua pengambilan data terjadi di runner.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| Jumlah baris Tier B yang sah | `reports/ingest_tier_b.json` putaran 2 |
| Rasio 1h:4h akan menjadi ≈4,00 setelah perbaikan | sama; ini gerbang utamanya |
| Celah kisi turun drastis setelah perbaikan | sama |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |
| Funding rate tersedia untuk seluruh 790 perp | belum diperiksa |
| `metrics/`, `bookTicker/`, `liquidationSnapshot/` tersedia | belum |

Throughput 1,30 MiB/s dari `doctor.json` **tidak boleh dipakai**: berkas ujinya 1,9 MB sehingga waktunya didominasi latensi.

Angka Tier B putaran 1 (14.076.257 baris 1h, 3.506.060 baris 4h, 677,6 MiB) **tidak boleh dikutip lagi**. Semuanya kekurangan satu bar per berkas.

---

## 5. Penghalang aktif

Tidak ada yang menghentikan pekerjaan.

Dibutuhkan dari pengguna, belum memblokir: **token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`, agar runner dapat menulis ke database Run Results dan membangunkan agen pengawas.

---

## 6. Tindakan berikutnya

1. Baca `reports/ingest_tier_b.json` putaran 2. Gerbang: nol duplikat, nol simbol gagal, **dan rasio baris 1h:4h harus ≈4,00**.
2. Jalankan ulang `backfill_daily.yml` — cakupan bulanan berubah dan hasil lamanya sama-sama cacat.
3. Jalankan `analyze_tail.yml` lagi setelah backfill baru; rasio terisi harus ≈1,00, bukan 0,958 dan 0,833.
4. Bandingkan hasil terhadap Dataset G lama (528 simbol) sebagai uji silang independen.
5. Ingest funding rate; tanpa itu model biaya perpetual tidak lengkap.
6. Terapkan ambang `config/lux.yaml` untuk menyaring universe backtest, lalu catat berapa simbol yang tersisa.
7. Baru setelah semua gerbang lulus, pertimbangkan Tier A (1m) dengan ≥24 shard.

---

## 7. Pengawasan otonom

Agen **LUX Gatekeeper** aktif di Notion. Terpicu saat runner membuat baris di database Run Results, menilai hasil terhadap sembilan gerbang mutu: forward-fill, buy-and-hold, entry acak, lookahead, invariant risiko, funding, overlap, checksum, survivorship.

Sudah diuji dengan baris sintetis bercacat; menolak dengan benar dan menolak mengeluarkan perintah lanjutan.

**Verdict Ditolak menghentikan pipeline.**

---

## 8. Peta repo

| Path | Isi |
|---|---|
| `config/lux.yaml` | seluruh parameter yang memengaruhi hasil |
| `lux/binance_vision.py` | klien arsip: listing S3, unduhan, checksum, percent-encoding |
| `lux/universe.py` | universe point-in-time dan klasifikasi jenis kontrak |
| `lux/ingest.py` | ingest Tier B dengan validasi per simbol |
| `lux/backfill_daily.py` | penutup celah ekor dari arsip harian |
| `lux/costs.py` | model biaya dalam satuan R |
| `lux/summarize.py` | agregasi laporan antar shard, termasuk nama simbol gagal |
| `lux/analyze_tail.py` | penelusuran anomali dari artifact tanpa unduh ulang |
| `tests/` | pengujian tanpa jaringan, wajib hijau sebelum ingest |
| `reference/` | parquet universe |
| `reports/` | keluaran mesin tiap run, sumber bukti Bagian 3 |
| `journal/` | riwayat per sesi |
| `decisions/` | ADR |
