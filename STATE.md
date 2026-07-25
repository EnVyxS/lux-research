# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi dan dibatasi ~400 baris. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-25 23:55 WIB (versi 5)
**Tahap sekarang:** S4 **SELESAI DAN SAH** — Tier B putaran 2 lulus seluruh gerbang, termasuk gerbang yang ditetapkan sebelum datanya dilihat
**Tahap berikutnya:** S5 — validasi data per simbol dan penyaringan universe backtest

---

## 1. Aturan membaca berkas ini

Bagian 3 adalah **fakta**: setiap baris punya bukti yang bisa diperiksa ulang berupa commit, run ID, atau kutipan dokumentasi. Bagian 4 adalah **asumsi**: belum diukur, dan dilarang diperlakukan sebagai fakta.

Memindahkan baris dari Bagian 4 ke Bagian 3 hanya boleh dilakukan dengan bukti terlampir. Kegagalan riset sebelumnya berakar pada asumsi yang perlahan diperlakukan sebagai kebenaran tanpa pernah diuji.

Dua aturan tambahan yang lahir dari sesi ini, keduanya dibayar dengan kesalahan nyata:

1. **Angka yang lulus gerbang belum tentu benar.** Rasio 1h:4h sebesar 4,014 pernah dicatat sebagai uji silang yang lulus, padahal ia sedang melaporkan bug. Gerbang hanya menangkap cacat yang bentuknya sudah dibayangkan.
2. **Sha laporan yang tidak berubah bukan tanda pekerjaan masih berjalan.** Sha stagnan wajib diperiksa terhadap status run. Sekali saya menyimpulkan ingest "masih berjalan" padahal job sudah mati merah 21 menit sebelumnya, dan yang menemukannya pengguna, bukan saya.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa.

Seluruh komputasi berjalan di GitHub Actions. Mesin lokal pengguna tidak sanggup melakukan backtest penuh, dan tidak ada VM cloud karena kendala kartu kredit.

---

## 3. Fakta terverifikasi

### DATASET TIER B PUTARAN 2 — SAH, dan inilah dasar semua pekerjaan selanjutnya

Sumber: `reports/ingest_tier_b.md` pada commit `16638b4`, plus `reports/backfill_daily.md` dan `reports/tail_anomali.md` pada commit `fbead60`.

**Arsip bulanan:**

| Interval | Baris | Simbol OK | Gagal | Duplikat | Celah kisi | Ukuran |
|---|---|---|---|---|---|---|
| 1h | **14.106.623** | 790 | 0 | 0 | **112** | 533,6 MB |
| 4h | **3.526.969** | 790 | 0 | 0 | **112** | 145,1 MB |

**Ekor harian (bulan yang belum tercakup arsip bulanan):**

| Interval | Baris | Simbol OK | Gagal | Celah kisi | Ukuran |
|---|---|---|---|---|---|
| 1h | **439.056** | 790 | 0 | 3 | 18,7 MB |
| 4h | **109.764** | 790 | 0 | 3 | 5,2 MB |

**Total Tier B: 14.545.679 bar 1h dan 3.636.733 bar 4h, sekitar 703 MB, 790 dari 790 simbol tanpa satu pun kegagalan.**

Tiga gerbang yang ditulis **sebelum** run dijalankan, semuanya lulus:

| Gerbang | Kriteria pra-registrasi | Hasil |
|---|---|---|
| Rasio baris 1h:4h bulanan | ≈4,000 | **3,9996** |
| Rasio terisi ekor harian | ≈1,00 kedua interval | **1,0 dan 1,0** |
| Celah per simbol pada ekor | ≈0 | **0,0** |

Ekor harian menambal 18.294 hari untuk 763 simbol yang masih aktif, dan kini terisi **tepat penuh**: 439.056 baris dari 439.056 yang diharapkan, tanpa satu bar pun kurang. Putaran 1 hanya mencapai 0,9583 dan 0,8334.

### Perbandingan putaran 1 vs putaran 2 — bukti bahwa perbaikannya nyata

| Ukuran | Putaran 1 (cacat) | Putaran 2 (sah) | Perubahan |
|---|---|---|---|
| Baris 1h bulanan | 14.076.257 | 14.106.623 | **+30.366** |
| Baris 4h bulanan | 3.506.060 | 3.526.969 | +20.909 |
| Simbol gagal | 3 | **0** | non-ASCII selesai |
| **Celah kisi** | **17.169** | **112** | **−99,3%** |
| Rasio 1h:4h | 4,014 | 3,9996 | menuju 4,000 |
| Rasio terisi ekor 1h | 0,9583 | **1,0** | penuh |

### KOREKSI PENTING: 17.169 celah itu adalah bug, dan saya sempat menyatakan sebaliknya

Saya pernah menuliskan bahwa celah kisi identik 17.169 di 1h dan 4h **bukan** bug, dengan alasan jumlah diskontinuitas sama dengan jumlah blok arsip yang hilang dan tidak bergantung ukuran bar, sehingga konsistensinya "memperkuat metrik". Penalaran itu keliru.

Kesamaan angka antar interval bukan tanda kesehatan, melainkan **sidik jari satu bar yang hilang per berkas**: setiap awal bulan yang terpotong menciptakan tepat satu lompatan, sama banyak di 1h maupun di 4h. Setelah parser diperbaiki, angkanya jatuh ke 112. Sisa 112 itulah lubang arsip yang sungguhan.

Pelajarannya lebih berharga daripada datanya: saya merasionalisasi bukti yang sedang menunjuk ke bug saya sendiri, dan yang membongkarnya bukan argumen melainkan angka sesudah perbaikan. **Penjelasan yang membuat anomali terasa wajar harus dicurigai lebih keras daripada anomalinya.**

### Cacat parser — tiga lapis, semuanya sudah ditutup

Cacat 1, ditemukan lewat invarian aritmetika (`5f222e8`): `baca_zip` memakai `header=0` dan `skiprows=1` bersamaan, sehingga pandas membuang baris header **dan** memperlakukan baris data pertama sebagai nama kolom. Tepat satu bar hilang dari setiap berkas berheader. Pecahan buktinya bulat sempurna: 23/24 = 0,9583, 5/6 = 0,8334, 23/5 = 4,5999, dan (720−1)/(180−1) = 4,017 yang selama dua putaran menyamar sebagai rasio sehat.

Cacat 2 dan 3, ditemukan lewat pengujian sintetis sebelum data disentuh (`16638b4`):

- **BOM UTF-8 merusak deteksi header.** Pemeriksaan `lstrip()` lalu `startswith("open_time")` gagal karena BOM bukan karakter spasi. Deteksi gagal, baris header dibaca sebagai data, berkas ambruk. Kini dekode memakai `utf-8-sig`.
- **Satu baris sampah menggagalkan seluruh berkas.** `dtype=float64` di `read_csv` membuat pandas melempar galat keras pada satu sel non-numerik. Satu baris rusak akan menghapus **satu bulan penuh** dari dataset. Kini konversi dilakukan sesudah pembacaan dengan `errors="coerce"`, lalu hanya baris tanpa waktu atau tanpa harga yang dibuang. Kehilangan satu bar jauh lebih baik daripada kehilangan satu bulan.

Dua cacat terakhir tertangkap dengan biaya **43 detik**, bukan 18 menit, karena `pytest` kini berjalan di dalam job sebelum satu byte pun diunduh. Gerbang pra-terbang itu sudah membayar dirinya sendiri pada hari pertama.

### Cacat URL non-ASCII — selesai dan terbukti

Tiga perpetual bernama huruf Han (`币安人生USDT`, `我踏马来了USDT`, `龙虾USDT`) gagal total pada putaran 1 karena `klines_url()` tidak melakukan percent-encoding pada segmen path, sementara listing S3 lolos karena `urlencode` sudah meng-encode parameternya. Kegagalan asimetris: simbol masuk universe, unduhan nol persen. Diperbaiki lewat helper `bv.seg()`. Putaran 2 mencatat **790 dari 790 berhasil**.

Rata-rata riwayat ketiganya hanya ~4.200 bar 1h (~175 hari), sehingga ambang `min_bar_1h: 8760` mengeluarkannya dari universe backtest **berdasarkan aturan yang ditulis sebelum angkanya dilihat**, bukan karena namanya aneh.

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

Universe riset tidak terpengaruh cacat parser, karena ia dibangun dari enumerasi nama berkas, bukan dari isinya.

Dataset lama berisi 528 simbol. Terhadap universe riset 790, artinya **262 simbol perpetual USDT hilang** dari upaya sebelumnya, dan yang hilang bukan sampel acak melainkan simbol yang mati.

**Catatan kejujuran tentang gerbang:** gerbang "harus melebihi 841" membandingkan 937 simbol arsip terhadap 841 simbol aktif dari snapshot `exchangeInfo`. Perbandingan itu tidak setara populasi. Bukti survivorship yang sesungguhnya adalah **129 simbol delisted yang hadir lengkap dengan riwayatnya**, termasuk SRMUSDT sampai 2024-05 dan FTTUSDT sampai 2026-06.

### Ekor arsip

Arsip bulanan berhenti di **2026-06**, arsip harian mencapai **2026-07-24**. Ingest yang hanya membaca arsip bulanan kehilangan ~24 hari terbaru tanpa tanda apa pun. `lux/backfill_daily.py` menutupnya dengan aturan umum: bandingkan bulan yang ada di arsip bulanan dengan bulan yang ada di arsip harian, unduh harian hanya untuk bulan yang tidak tercakup. Bukan tambalan tanggal, jadi tidak perlu disentuh lagi bulan depan.

Hipotesis lama "Sep–Des 2019 hilang" sudah gugur: arsip harian majors mulai 2019-12-31. Tiga bulan pertama futures Binance tidak ada di arsip sama sekali.

### Model biaya — `lux/costs.py`, `config/lux.yaml`

Biaya dinyatakan dalam satuan R, bukan persen harga, supaya sebanding langsung dengan target keuntungan. `cost_R = 2·(fee+slippage)/stop_frac`; `funding_R = rate·(jam/8)/stop_frac` dengan tanda berbalik untuk short; `winrate_impas = (1+biaya_R)/(imbalan+1)`.

Angka yang layak diingat: stop 0,1% dengan biaya bolak-balik 0,2% menghabiskan 2R sebelum posisi bergerak, sehingga titik impas pada imbalan 2R tepat 100% — mati secara aritmetika. `layak_secara_biaya()` menolak konfigurasi semacam itu **sebelum** backtest dijalankan, karena mesin backtest akan patuh menggambar kurva ekuitas untuk parameter yang mustahil.

Seluruh parameter yang memengaruhi hasil ada di `config/lux.yaml`, tidak tersebar sebagai konstanta di kode. Parameter tersembunyi adalah jalur paling umum masuknya overfitting tanpa jejak.

### Validasi data — `lux/validate.py` (baru, commit `42fdae2`)

Modul ini memisahkan dua hal yang sering dicampur, dan pencampurannya adalah cara paling halus survivorship bias masuk:

- **Integritas** — apakah data konsisten dengan dirinya sendiri. Punya jawaban benar atau salah. Yang diperiksa: duplikat waktu, waktu mundur, stempel tidak selaras kisi interval, `high` lebih kecil dari `max(open,close)`, `low` lebih besar dari `min(open,close)`, harga nol atau negatif, volume negatif, nilai kosong.
- **Kelayakan** — apakah instrumen cukup panjang dan cukup likuid untuk diuji. Ini keputusan, dan ambangnya sudah beku di `config/lux.yaml` sebelum datanya dilihat.

Dua keputusan desain yang perlu dipertahankan:

1. **Celah bukan pelanggaran fatal.** Perdagangan memang pernah terhenti; itu fakta pasar, bukan kerusakan data. Yang fatal adalah data yang bertentangan dengan dirinya sendiri, karena itu berarti pembacaan kita salah, bukan pasarnya.
2. **Penolakan selalu menyertakan alasan, dan semua alasan dikumpulkan, bukan hanya yang pertama.** Simbol yang ditolak tanpa alasan tercatat akan terlihat seperti simbol yang tidak pernah ada.

Likuiditas diukur sebagai **median** nilai transaksi harian, bukan rata-rata, karena satu hari peluncuran yang gila dapat mengangkat rata-rata instrumen yang sehari-hari nyaris tidak diperdagangkan.

### Pengujian — `reports/tests.md`

**32 pengujian hijau** pada commit `16638b4` (`32 passed in 0.66s`), ditambah 22 pengujian validasi pada `42fdae2`. Semuanya tanpa jaringan, selesai dalam hitungan milidetik.

Invarian yang menjaga bug tidak kembali: jumlah bar tidak boleh berubah karena keberadaan header, rasio 1h:4h harus tepat 4,0, BOM tidak boleh merusak deteksi header, dan satu baris sampah tidak boleh menggagalkan berkas.

CI juga sudah dua kali menangkap kesalahan saya sendiri: sebuah asersi menuntut `winrate_impas(2,2) > 1.0` padahal aritmetikanya tepat 1,0, dan dua berkas uji ditulis ke direktori yang belum dibuat. Pengujian yang menuntut hal keliru berbahaya karena mengundang orang menambal kode yang sudah benar.

### Kapasitas runner — sumber: `reports/doctor.json`

| Sumber daya | Nilai terukur |
|---|---|
| vCPU | 4 |
| RAM | 15 GB |
| Disk bebas | **88 GB** |
| CPU | bervariasi antar run: EPYC 7763 dan EPYC 9V74 |

Disk 88 GB, bukan 14 GB seperti diperkirakan. **Batas 6 jam per job, bukan disk, yang menjadi kendala utama.** Model CPU berbeda antar run, jadi setiap tolok ukur berbasis waktu wajib mencatat model CPU-nya.

Durasi terukur: delapan shard paralel, 790 simbol, dua interval, selesai ~18 menit; shard terlama 554,7 detik untuk bagian 1h saja. Data 1m sekitar 60× lebih besar, sehingga satu shard akan menembus batas 6 jam. **Tier A butuh minimal 24 shard, bukan 8.**

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
- Agen **tidak bisa** mengunduh artifact, tapi runner bisa. `gh run list` plus `gh run download` di dalam runner membuat artifact run mana pun terbaca secara tidak langsung. Pola ini yang memungkinkan diagnosis cacat parser tanpa mengunduh ulang data.
- Agen **tidak bisa** melihat status run. Kesimpulan tentang berjalan atau tidaknya sebuah job hanya boleh diambil dari perubahan sha laporan **plus** konfirmasi pengguna, bukan dari sha saja.
- Sandbox agen **tidak punya jaringan**. Semua pengambilan data terjadi di runner.
- Analisis kini digabung ke dalam job penghasil datanya (`analyze_tail` berjalan di job `gabung`), supaya diagnosis tidak tertunda menunggu workflow terpisah dipicu.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| Seluruh 790 simbol lolos pemeriksaan integritas per simbol | jalankan `lux/validate.py` atas aset Release |
| Berapa simbol tersisa setelah ambang kelayakan diterapkan | sama; angkanya wajib dicatat apa pun hasilnya |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |
| Funding rate tersedia untuk seluruh 790 perp | belum diperiksa |
| `metrics/`, `bookTicker/`, `liquidationSnapshot/` tersedia | belum |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap 1h putaran 2 |

Throughput 1,30 MiB/s dari `doctor.json` **tidak boleh dipakai**: berkas ujinya 1,9 MB sehingga waktunya didominasi latensi.

**Angka yang dilarang dikutip:** seluruh hasil putaran 1 (14.076.257 baris 1h, 3.506.060 baris 4h, 677,6 MiB, 17.169 celah, rasio 4,014) dan hasil `ingest_retry` serta `backfill` putaran 1. Semuanya kekurangan satu bar per berkas. Aset Parquet pra-`16638b4` di Release sudah tertimpa oleh putaran 2 (`--clobber`), kecuali aset `_retry` yang kini digantikan oleh ingest normal karena ketiga simbol non-ASCII sudah berhasil.

---

## 5. Penghalang aktif

Tidak ada yang menghentikan pekerjaan.

Dibutuhkan dari pengguna, belum memblokir: **token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`, agar runner dapat menulis ke database Run Results dan membangunkan agen pengawas.

---

## 6. Tindakan berikutnya

1. Tulis `.github/workflows/validate.yml`: unduh aset Parquet dari Release `tier-b-v1`, jalankan `lux/validate.py` per simbol, tulis `reports/validate.md` dan `reports/universe_layak.json`. **Catat jumlah simbol yang lolos dan seluruh alasan penolakan**, bukan hanya jumlahnya.
2. Ingest funding rate dari `data/futures/um/monthly/fundingRate/`; tanpa itu model biaya perpetual tidak lengkap.
3. Diff terhadap Dataset G lama (528 simbol) sebagai uji silang independen dari sumber berbeda.
4. `lux/manifest.py` — catatan write-once atas setiap aset beserta SHA256, supaya asal setiap baris dapat dilacak.
5. Mesin backtest (`lux/backtest/engine.py`) dengan sembilan gerbang mutu terpasang sejak awal, bukan ditambahkan setelah ada hasil.
6. Baru setelah semua gerbang lulus, pertimbangkan Tier A (1m) dengan ≥24 shard.

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
| `lux/validate.py` | integritas OHLCV dan penyaringan kelayakan universe |
| `lux/costs.py` | model biaya dalam satuan R |
| `lux/summarize.py` | agregasi laporan antar shard, termasuk nama simbol gagal |
| `lux/analyze_tail.py` | penelusuran anomali dari artifact tanpa unduh ulang |
| `tests/` | pengujian tanpa jaringan, wajib hijau sebelum ingest |
| `reference/` | parquet universe |
| `reports/` | keluaran mesin tiap run, sumber bukti Bagian 3 |
| `journal/` | riwayat per sesi |
| `decisions/` | ADR |
