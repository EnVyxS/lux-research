# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi dan dibatasi ~400 baris. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-25 20:50 WIB
**Tahap sekarang:** S1 — Repositori (selesai sebagian)
**Tahap berikutnya:** S2 — Bootstrap dan pengukuran kapasitas runner

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

### Infrastruktur

| Fakta | Bukti |
|---|---|
| Repo `EnVyxS/lux-research` ada, publik | dibuat 2026-07-25, id `1312019687` |
| Token GitHub bisa membaca profil | `get_me` mengembalikan `EnVyxS`, id `90240108` |
| Menit Actions tak terbatas untuk repo publik | `github.com/pricing`, "Free for public repositories" |
| Job tunggal dibatasi 6 jam keras | `docs.github.com/en/actions/reference/limits` |
| Aset Release dibatasi 2 GB per berkas | `github.com/orgs/community/discussions/146417` |
| Berkas di dalam git dibatasi 100 MB | dokumentasi GitHub tentang berkas besar |
| Cron dinonaktifkan otomatis setelah 60 hari tanpa aktivitas | dokumentasi disabling-and-enabling-a-workflow |

### Batas alat yang dimiliki agen

Ini membentuk pembagian kerja, jadi jangan dilupakan.

- Agen **tidak bisa** membuat rilis atau mengunggah aset rilis. Semua tool rilis yang tersedia baca-saja. Parquet harus diunggah oleh runner lewat `gh release upload` di dalam workflow.
- Agen **tidak bisa** memicu workflow secara manual. Satu-satunya pemicu yang bisa dipakai agen adalah melakukan push.
- Agen **tidak bisa** membaca status atau log workflow run. Umpan balik hanya datang lewat job yang menuliskan hasilnya sendiri ke database Run Results di Notion.
- Sandbox agen **tidak punya akses jaringan sama sekali**. DNS mati total. Semua pengambilan data harus terjadi di runner Actions atau di mesin pengguna.

### Data

Hanya sebagian kecil dataset lama yang masih tersimpan permanen (~47 MB). Sisanya perlu diunduh ulang. Dataset lama berperan sebagai **pembanding untuk validasi silang, bukan sumber kebenaran**.

| Artefak persisten | Cakupan | Ukuran |
|---|---|---|
| Index Price Klines 1h | 832 simbol, 2026-06-09 → 07-21 | 17,7 MB |
| Mark Price Klines 1h | 838 simbol, 2026-06-09 → 07-21 | 16,5 MB |
| Open Interest 1h | 841 simbol, 2026-06-30 → 07-21 | 6,7 MB |
| Funding Rate 8h | 841 simbol, 2026-02-04 → 07-21 | 4,0 MB |
| Metadata Futures | 841 exchangeInfo, snapshot 2026-07-21 | 2,2 MB |

Sumber unduhan: `https://data.binance.vision/data/futures/um/...` — **prefix `data/` wajib**, tanpa itu S3 mengembalikan `NoSuchKey`.

### Anomali yang belum terjelaskan

Dataset lama berisi 528 simbol, sementara `exchangeInfo` hari ini mencantumkan 841 simbol aktif. Selisih 313 simbol ini adalah **indikasi kuat survivorship bias** pada dataset lama. Universe point-in-time yang dibangun di S3 harus menghasilkan **lebih dari 841 simbol historis**; jika tidak, pembangunan universe itu sendiri yang cacat.

---

## 4. Asumsi belum terverifikasi

Jangan bangun keputusan di atas baris-baris ini sebelum diukur.

| Asumsi | Cara memverifikasi |
|---|---|
| Runner punya ~14 GB disk bebas | workflow `doctor`, `df -h` |
| Runner punya 16 GB RAM dan 4 vCPU | workflow `doctor`, `free -g` dan `nproc` |
| Endpoint S3 listing Binance berfungsi | fase `preflight` skrip PowerShell |
| Data simbol delisted masih diarsipkan Binance | preflight menguji SRMUSDT, FTTUSDT, COCOSUSDT |
| Direktori `metrics/`, `bookTicker/`, `liquidationSnapshot/` tersedia | preflight |
| Tier B (1h + 4h seluruh universe) ≈ 28 juta baris, ≈0,9 GB | ukur setelah ingest pertama |
| Rasio kompresi CSV ke Parquet+zstd ≈ 9× | ukur setelah ingest pertama |

---

## 5. Penghalang aktif

Tidak ada penghalang yang menghentikan pekerjaan saat ini.

Yang masih dibutuhkan dari pengguna, tapi belum memblokir langkah berikutnya:

1. **Token integrasi Notion** disimpan sebagai GitHub Secret `NOTION_TOKEN`, agar runner bisa menulis hasil ke database Run Results. Tanpa ini, loop umpan balik otonom tidak menyala.
2. **Menjalankan `lux_fetch.ps1 -Phase preflight`** di mesin lokal dan mengirimkan `preflight_report.json`, untuk menutup lima asumsi di Bagian 4.

---

## 6. Tindakan berikutnya

1. Tulis workflow `doctor` untuk mengukur disk, RAM, CPU, dan konektivitas runner ke `data.binance.vision`.
2. Tulis `lux/binance_vision.py` dan bangun universe point-in-time. **Gerbang: hasil harus melebihi 841 simbol.**
3. Ingest Tier B lebih dulu, bukan Tier A. Volume kecil membuat kesalahan pipeline ketahuan murah.
4. Validasi hasil ingest terhadap sembilan gerbang mutu sebelum menyentuh Tier A.

---

## 7. Pengawasan otonom

Sebuah agen bernama **LUX Gatekeeper** sudah aktif di Notion. Ia terpicu ketika runner membuat baris baru di database Run Results, lalu menilai hasil terhadap sembilan gerbang mutu dan memberi verdict Lulus atau Ditolak.

Gerbang tersebut: forward-fill, buy-and-hold, entry acak, lookahead, invariant risiko, funding, overlap, checksum, dan survivorship.

Gatekeeper sudah diuji dengan baris sintetis yang mengandung dua cacat tertanam. Ia menolak baris itu, mengidentifikasi kedua cacat dengan benar, dan menolak mengeluarkan perintah lanjutan. Pengujian itu lulus.

Ketika verdict Ditolak, pipeline berhenti. Agen tidak boleh melanjutkan ke tahap berikutnya.

---

## 8. Arsip

- `journal/` — riwayat lengkap per sesi. Baca hanya bagian yang relevan.
- `decisions/` — ADR. ADR-002 menggantikan bagian penyimpanan pada ADR-001.
- Notion masih menyimpan Constitution riset dan halaman Pelajaran Metodologis. Keduanya belum dipindahkan ke repo ini.
