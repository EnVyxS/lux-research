# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-26 00:45 WIB (versi 6)
**Tahap sekarang:** S5 **SELESAI DAN SAH** — validasi integritas dan penyaringan universe selesai; funding rate seluruh universe layak sudah masuk dan metriknya bersih
**Tahap berikutnya:** S6 — mesin backtest `lux/backtest/engine.py`

---

## 1. Aturan membaca berkas ini

Bagian 3 adalah **fakta**: setiap baris punya bukti berupa commit, run ID, atau kutipan dokumentasi. Bagian 4 adalah **asumsi**: belum diukur, dan dilarang diperlakukan sebagai fakta. Memindahkan baris dari Bagian 4 ke Bagian 3 hanya boleh dengan bukti terlampir.

Empat aturan yang lahir dari kesalahan nyata, bukan dari teori:

1. **Angka yang lulus gerbang belum tentu benar.** Rasio 1h:4h 4,014 pernah dicatat sebagai uji silang yang lulus, padahal sedang melaporkan bug. Gerbang hanya menangkap cacat yang bentuknya sudah dibayangkan.
2. **Sha laporan yang tidak berubah bukan tanda pekerjaan masih berjalan.** Sekali disimpulkan ingest "masih berjalan" padahal job sudah mati merah 21 menit sebelumnya, dan yang menemukan pengguna.
3. **Penjelasan yang membuat anomali terasa wajar harus dicurigai lebih keras daripada anomalinya.**
4. **Lihat sebaran mentah sebelum berteori.** Metrik celah funding gagal lima putaran; satu tabel histogram di awal akan menyelesaikannya dalam satu putaran.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa.

Seluruh komputasi berjalan di GitHub Actions. Mesin lokal pengguna tidak sanggup melakukan backtest penuh, dan tidak ada VM cloud karena kendala kartu kredit.

---

## 3. Fakta terverifikasi

### DATASET TIER B PUTARAN 2 — SAH, dasar semua pekerjaan selanjutnya

Sumber: `reports/ingest_tier_b.md` pada commit `16638b4`, `reports/backfill_daily.md` dan `reports/tail_anomali.md` pada `fbead60`.

| Interval | Baris bulanan | Ekor harian | Simbol OK | Gagal | Duplikat | Celah kisi |
|---|---|---|---|---|---|---|
| 1h | **14.106.623** | 439.056 | 790 | 0 | 0 | **112** |
| 4h | **3.526.969** | 109.764 | 790 | 0 | 0 | **112** |

**Total: 14.545.679 bar 1h dan 3.636.733 bar 4h, sekitar 703 MB, 790 dari 790 simbol tanpa satu pun kegagalan.**

Tiga gerbang yang ditulis **sebelum** run dijalankan, semuanya lulus: rasio baris 1h:4h **3,9996** terhadap target 4,000; rasio terisi ekor harian **1,0 dan 1,0**; celah per simbol pada ekor **0,0**.

### VALIDASI S5 — sumber: `reports/validate_1h.md`, commit `2356684`

| Ukuran | Nilai |
|---|---|
| Baris diperiksa | **14.545.679** |
| Simbol diperiksa | **790** |
| Pelanggaran fatal | **0** |
| Duplikat waktu | **0** |
| Celah kisi | **112** |
| **Simbol layak backtest** | **447** |
| Simbol ditolak | 343 |

Alasan penolakan, satu simbol bisa punya lebih dari satu: riwayat terlalu pendek 277, likuiditas tipis 77, terlalu banyak bar datar 74.

Nol pelanggaran fatal atas 14,5 juta bar berarti data konsisten dengan dirinya sendiri: tidak ada `high` di bawah badan lilin, tidak ada harga nol, tidak ada waktu mundur. Angka 112 celah cocok persis dengan `ingest_tier_b.md`, jadi dua modul yang ditulis terpisah sampai pada angka yang sama.

Selisih **12.593 baris** antara 14.558.272 dan 14.545.679 sudah dijelaskan tuntas, bukan diabaikan: aset `_retry` usang dari putaran 1 masih tersimpan di Release dan ikut terbaca. `lux/validate_run.py` kini menolak berkas berpola `_retry`, dan asetnya dihapus dari Release. **Mencatat sesuatu "tidak sah" di STATE tidak menghapusnya dari disk.**

Rentang: BCH, BTC, dan ETH masing-masing **57.552 bar tanpa satu celah pun**. Terpendek 611 bar. Median nilai transaksi harian BTCUSDT **12,3 miliar USDT**.

### FUNDING RATE S5b — sumber: `reports/funding_check.md`, commit `0448a67`

| Ukuran | Nilai |
|---|---|
| Baris | **1.982.017** |
| Simbol | **447 dari 447** universe layak |
| Rentang | 2020-01-01 → 2026-06-30 |
| Duplikat / tidak urut | **0 / 0** |
| Celah sejati | **3 peristiwa pada 3 simbol** |
| Funding positif | 1.563.845 (**79,1%**) |
| Melebihi 2% | 85 |

**Sebaran jarak antarbaris, dibulatkan ke kisi sah terdekat:** 4 jam 52,00%, 8 jam 45,23%, 1 jam 2,68%, 2 jam 0,09%, ditambah 19 jarak 3 jam, 3 jarak 6 jam, dan tiga jarak sangat panjang.

**Kisi funding bukan sifat tetap sebuah simbol: 295 dari 447 simbol hidup di lebih dari satu rezim kisi.** Kisi utama: 269 simbol di 4 jam, 174 di 8 jam, 4 di 1 jam. Ini konsekuensi langsung bagi model biaya — `funding_interval_jam: 8` di `config/lux.yaml` **tidak mewakili kenyataan** dan wajib diganti kisi per simbol per waktu.

Ketiga celah sejati adalah penghentian perdagangan sungguhan: BNTUSDT 20.016 jam setara 2.501 penagihan, LITUSDT 4.500 jam setara 562, PUMPUSDT 504 jam setara 125. Backtest harus memperlakukan rentang ini sebagai periode tanpa posisi, bukan sebagai biaya nol.

**Funding positif 79,1% berarti long membayar short pada empat dari lima periode.** Ini rintangan struktural bagi strategi yang condong long dan harus ditagihkan ke setiap posisi.

Biaya tahunan tertinggi bagi long: 1000WHYUSDT 60,7%, 1000000BOBUSDT 60,1%, BROCCOLIF3BUSDT 57,0%. Paling menguntungkan long: MYXUSDT −533,9%, LAUSDT −272,6%, LAYERUSDT −230,7%. Angka setahun adalah ekstrapolasi rerata historis untuk menakar besaran rintangan, **bukan sinyal strategi**.

### METRIK CELAH FUNDING — lima putaran gagal, dan mengapa

Dicatat lengkap karena ini kegagalan penalaran paling mahal di sesi ini.

| Putaran | Definisi celah | Hasil | Cacat |
|---|---|---|---|
| 1 | langkah tetap dari nilai terkecil kolom interval | 1.380.741 | satu kisi untuk seumur hidup simbol |
| 2 | langkah per baris dari kolom interval | 1.193.209 | sama |
| 3 | langkah dari modus jarak teramati | 587.131 | sama |
| 4 | jarak melebihi 8 jam, tanpa toleransi | 266.612 | waktu dibandingkan tanpa epsilon |
| 5 | jarak melebihi 8 jam, toleransi 1 menit | **3** | — |

Putaran 3 membuktikan kolom `funding_interval_hours` **tidak pernah salah**: nol dari 447 simbol yang kolomnya tidak cocok dengan kisi teramati. Yang salah selalu asumsi bahwa kisi itu tetap.

Putaran 4 dibongkar oleh pertentangan di dalam laporannya sendiri: 266.612 peristiwa celah hanya menghasilkan 10.720 penagihan hilang, padahal satu celah menurut definisinya melewatkan setidaknya satu penagihan. TRBUSDT mencatat 1.332 peristiwa dengan tepat 1.332 penagihan hilang pada kisi 4 jam, yang hanya mungkin bila jaraknya 8 jam — kisi sah, bukan celah.

Penyebabnya **jitter stempel waktu bursa**: 1.193.171 jarak tidak tepat di kisi, dengan pergeseran terbesar hanya **47 milidetik**. Tabel sebaran sempat menyembunyikannya karena jam dibulatkan ke empat desimal, resolusi 0,36 detik. **Alat diagnosisnya sendiri yang membutakan.** Angka 1.193.171 itu hampir sama persis dengan hasil putaran 2 sebesar 1.193.209, yang berarti putaran 2 sesungguhnya sedang mengukur jitter, bukan rezim kisi.

Aturan permanen: **semua perbandingan waktu memakai toleransi, dan besar pergeseran dilaporkan sebagai angka tersendiri** supaya toleransi tidak menjadi tempat sembunyi anomali sungguhan.

### Cacat parser — tiga lapis, semuanya sudah ditutup

Cacat 1 (`5f222e8`): `baca_zip` memakai `header=0` dan `skiprows=1` bersamaan, sehingga tepat satu bar hilang dari setiap berkas berheader. Pecahan buktinya bulat sempurna: 23/24 = 0,9583, 5/6 = 0,8334, dan (720−1)/(180−1) = 4,017 yang selama dua putaran menyamar sebagai rasio sehat.

Cacat 2 dan 3 (`16638b4`), ditemukan lewat pengujian sintetis sebelum data disentuh: **BOM UTF-8 merusak deteksi header** karena BOM bukan karakter spasi, kini dekode memakai `utf-8-sig`; dan **satu baris sampah menggagalkan seluruh berkas** karena `dtype=float64` melempar galat keras, kini konversi memakai `errors="coerce"` sesudah pembacaan. Kehilangan satu bar jauh lebih baik daripada kehilangan satu bulan.

Koreksi yang wajib diingat: celah kisi identik 17.169 di 1h dan 4h pernah saya nyatakan **bukan** bug, dengan alasan konsistensinya memperkuat metrik. Setelah parser diperbaiki angkanya jatuh ke 112. Kesamaan itu adalah sidik jari satu bar hilang per berkas.

### Cacat URL non-ASCII — selesai dan terbukti

Tiga perpetual bernama huruf Han gagal total pada putaran 1 karena `klines_url()` tidak melakukan percent-encoding pada segmen path. Diperbaiki lewat `bv.seg()`; putaran 2 mencatat 790 dari 790 berhasil. Ketiganya tetap keluar dari universe backtest karena riwayatnya ~4.200 bar, berdasarkan ambang yang ditulis sebelum angkanya dilihat.

### Universe — `reports/universe.json`, 2026-07-25T14:35Z

| Ukuran | Nilai |
|---|---|
| Simbol di arsip (pernah ada) | **937** |
| Perpetual USDT — universe riset | **790** |
| Masih aktif / delisted | 761 / 29 |
| **Layak backtest** | **447** |
| Baris point-in-time | 21.789 pasangan simbol-bulan |
| Rentang arsip bulanan | 2020-01 → 2026-06 |

Dataset lama berisi 528 simbol; terhadap 790 berarti 262 perpetual USDT hilang, dan yang hilang bukan sampel acak melainkan simbol yang mati. Bukti survivorship yang sesungguhnya adalah **129 simbol delisted hadir lengkap dengan riwayatnya**, termasuk SRMUSDT sampai 2024-05.

Gerbang "harus melebihi 841" tidak setara populasi: 937 simbol arsip dibandingkan 841 simbol aktif dari snapshot `exchangeInfo`.

### Ekor arsip

Arsip bulanan berhenti di **2026-06**, arsip harian mencapai **2026-07-24**. `lux/backfill_daily.py` menutupnya dengan aturan umum, bukan tambalan tanggal. Hipotesis "Sep–Des 2019 hilang" sudah gugur: arsip harian majors mulai 2019-12-31.

### Model biaya — `lux/costs.py`, `config/lux.yaml`

Biaya dinyatakan dalam satuan R: `cost_R = 2·(fee+slippage)/stop_frac`; `winrate_impas = (1+biaya_R)/(imbalan+1)`. Stop 0,1% dengan biaya bolak-balik 0,2% menghabiskan 2R sebelum posisi bergerak, sehingga titik impas pada imbalan 2R tepat 100% — mati secara aritmetika. `layak_secara_biaya()` menolak konfigurasi semacam itu sebelum backtest dijalankan.

**Wajib diperbaiki sebelum S6:** `funding_R` masih memakai pembagi 8 jam tetap. Data membuktikan 269 dari 447 simbol berkisi 4 jam dan 295 simbol berpindah rezim, jadi pembagi tetap akan salah menghitung biaya pada mayoritas universe.

### Pengujian — `reports/tests.md`

**99 pengujian hijau** pada commit `e0496e0`, seluruhnya tanpa jaringan dan selesai dalam ~1 detik.

CI sudah **empat kali** menangkap kesalahan saya sendiri sebelum satu byte pun diunduh, dengan biaya 43, 26, 23, dan 49 detik. Tiga di antaranya harapan pengujian yang keliru, satu cacat produksi sungguhan (`EmptyDataError` pada berkas funding tanpa baris data). Urutan itu penting: **setelah beberapa kali pengujian yang salah, godaan terbesar adalah menganggap setiap uji merah sebagai kesalahan pengujian.**

### Kapasitas runner — `reports/doctor.json`

4 vCPU, 15 GB RAM, **88 GB disk bebas**, model CPU bervariasi antar run. **Batas 6 jam per job, bukan disk, yang menjadi kendala utama.** Delapan shard paralel, 790 simbol, dua interval selesai ~13 menit; shard terlama 554,7 detik. Data 1m sekitar 60× lebih besar, sehingga **Tier A butuh minimal 24 shard**.

### Konektivitas

CDN `data.binance.vision` 200; S3 listing 200; REST `fapi.binance.com` **451 permanen** karena runner berbasis di AS; checksum SHA256 cocok. Snapshot `exchangeInfo` dari mesin pengguna dipakai hanya sebagai referensi tick size, step size, dan minimum notional.

### Batas alat agen dan solusinya

- Agen **tidak bisa** membuat rilis, memicu workflow manual, membaca log, mengunduh artifact, atau melihat status run.
- Setiap workflow diberi filter `paths` pada berkasnya sendiri; **menyunting workflow adalah satu-satunya cara memicunya.**
- **Setiap workflow wajib menulis hasil ke `reports/` dan meng-commit balik.** Workflow yang tidak mengikuti pola ini hasilnya tidak akan pernah terlihat.
- Runner bisa membaca artifact run lain lewat `gh run list` plus `gh run download`.
- Sandbox agen **tidak punya jaringan**. Semua pengambilan data terjadi di runner.
- Gerbang `pytest` wajib berjalan **sebelum** unduhan di setiap workflow.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| Integritas 4h sama bersihnya dengan 1h | jalankan `validate.yml` untuk interval 4h |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap universe layak 447 |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |
| `metrics/`, `bookTicker/`, `liquidationSnapshot/` tersedia | belum diprobe |

Throughput 1,30 MiB/s dari `doctor.json` **tidak boleh dipakai**: berkas ujinya 1,9 MB sehingga waktunya didominasi latensi.

**Angka yang dilarang dikutip:** seluruh hasil putaran 1 (14.076.257 baris 1h, 3.506.060 baris 4h, 17.169 celah, rasio 4,014) dan seluruh metrik celah funding putaran 1 sampai 4 (1.380.741, 1.193.209, 587.131, 266.612).

---

## 5. Penghalang aktif

Tidak ada yang menghentikan pekerjaan.

Dibutuhkan dari pengguna, belum memblokir: **token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`, agar runner dapat menulis ke database Run Results dan membangunkan agen pengawas.

---

## 6. Tindakan berikutnya

1. **Ganti model funding di `config/lux.yaml` dan `lux/costs.py`** dari konstanta 8 jam menjadi kisi per simbol per waktu. Ini prasyarat S6, bukan penyempurnaan.
2. **`lux/backtest/engine.py`** dengan sembilan gerbang mutu terpasang sejak awal, bukan ditambahkan setelah ada hasil. Hipotesis dipra-registrasi sebelum dijalankan.
3. Jalankan validasi untuk interval 4h.
4. Diff terhadap Dataset G lama (528 simbol) sebagai uji silang survivorship dari sumber berbeda.
5. `lux/manifest.py` — catatan write-once atas setiap aset beserta SHA256.
6. Baru setelah semua gerbang lulus, pertimbangkan Tier A (1m) dengan ≥24 shard.

---

## 7. Pengawasan otonom

Agen **LUX Gatekeeper** aktif di Notion. Terpicu saat runner membuat baris di database Run Results, menilai hasil terhadap sembilan gerbang mutu: forward-fill, buy-and-hold, entry acak, lookahead, invariant risiko, funding, overlap, checksum, survivorship. Sudah diuji dengan baris sintetis bercacat dan menolak dengan benar. **Verdict Ditolak menghentikan pipeline.**

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
| `lux/validate_run.py` | pemuat aset Release, penolak berkas usang `_retry` |
| `lux/funding.py` | ingest funding rate dari arsip bulanan |
| `lux/funding_check.py` | metrik kisi funding, celah, dan biaya tahunan |
| `lux/costs.py` | model biaya dalam satuan R |
| `lux/summarize.py` | agregasi laporan antar shard, termasuk nama simbol gagal |
| `lux/analyze_tail.py` | penelusuran anomali dari artifact tanpa unduh ulang |
| `tests/` | 99 pengujian tanpa jaringan, wajib hijau sebelum unduhan |
| `reference/` | parquet universe |
| `reports/` | keluaran mesin tiap run, sumber bukti Bagian 3 |
| `journal/` | riwayat per sesi |
| `decisions/` | ADR |

Release **`tier-b-v1`** memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`.
