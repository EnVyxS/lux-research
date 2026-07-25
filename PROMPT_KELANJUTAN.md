# Prompt kelanjutan

Salin seluruh blok di bawah ke percakapan baru bila sesi terputus atau konteks
penuh. Berkas ini diperbarui setiap kali posisi riset berubah signifikan.

---

Lanjutkan riset LUX. Jangan memulai dari nol dan jangan mengulang pekerjaan
yang sudah selesai.

**Langkah pertama yang wajib:** baca `STATE.md` di repositori GitHub
`EnVyxS/lux-research` (publik). Berkas itu adalah jurnal tunggal dan satu-satunya
sumber kebenaran tentang posisi riset. Jangan membaca `journal/` secara utuh.

## Konteks

Saya membangun sistem trading kuantitatif untuk Binance USD-M Futures dari nol.
Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja
dibuang karena tercemar survivorship bias dan overfitting. Hanya data mentah dan
pelajaran metodologis yang dibawa.

Mesin lokal saya tidak sanggup melakukan backtest penuh, dan saya tidak bisa
menyewa VM cloud karena kendala kartu kredit. Karena itu **seluruh komputasi
berjalan di GitHub Actions**, dan repositori GitHub adalah tempat penyimpanan
data sekaligus jurnal riset.

## Batas alat yang harus dipahami sejak awal

- Sandbox agen **tidak punya akses jaringan**. Semua pengambilan data terjadi di
  runner GitHub Actions.
- Agen **tidak bisa membaca log workflow**. Solusinya sudah berjalan dan wajib
  diikuti setiap workflow baru: **tulis hasil ke `reports/` lalu commit balik ke
  repo**, agen membacanya lewat API biasa.
- Agen **tidak bisa memicu workflow secara manual**. Setiap workflow diberi
  filter `paths` pada berkasnya sendiri, sehingga push ke berkas itu memicunya.
- Agen **tidak bisa membuat atau mengunggah rilis**. Runner melakukannya lewat
  `gh release upload`.
- REST `fapi.binance.com` mengembalikan **HTTP 451** dari runner GitHub. Jangan
  pernah menaruhnya di jalur kritis.

## Yang sudah selesai

1. Repositori `EnVyxS/lux-research` dibuat, izin tulis penuh terverifikasi
   termasuk `.github/workflows/`.
2. Kapasitas runner terukur: 4 vCPU, 15 GB RAM, **88 GB disk**. Batas 6 jam per
   job adalah kendala utama, bukan disk.
3. Universe point-in-time dibangun dari arsip S3, bukan dari `exchangeInfo`:
   **937 simbol pernah ada**, terdiri dari 872 perpetual, 50 kontrak bertanggal,
   15 varian SETTLED. **Universe riset = 790 perpetual USDT.** Dataset lama hanya
   punya 528, jadi 262 simbol hilang.
4. Klien arsip `lux/binance_vision.py` dengan listing S3, unduhan resumable, dan
   verifikasi checksum SHA256.
5. Ingest Tier B (1h dan 4h) dan backfill ekor harian sudah ditulis.
6. Agen pengawas **LUX Gatekeeper** aktif di Notion, sudah diuji dan lulus.

## Yang masih harus dikerjakan

1. Baca `reports/ingest_tier_b.json`. Gerbang: nol duplikat, nol simbol gagal.
2. Jalankan backfill ekor harian. Arsip bulanan berhenti di 2026-06 sementara
   arsip harian mencapai 2026-07-24, jadi tanpa backfill data selalu tertinggal
   sebulan.
3. Uji silang hasil terhadap Dataset G lama sebagai pembanding independen.
4. Ingest funding rate. Tanpa itu model biaya perpetual tidak lengkap.
5. Tulis mesin backtest beserta sembilan gerbang mutu.
6. Pra-registrasi eksperimen sebelum menjalankannya.

## Cara saya ingin Anda bekerja

- Ketika saya menulis **"lanjut"**, teruskan langsung dari titik terakhir tanpa
  meminta konfirmasi dan tanpa mengulang penjelasan.
- Pisahkan **fakta terverifikasi** dari **asumsi**. Asumsi hanya naik menjadi
  fakta bila ada bukti terlampir berupa commit, run ID, atau kutipan sumber.
- Katakan bila saya salah, dan katakan bila Anda sendiri salah. Riset ini gagal
  sebelumnya justru karena asumsi yang tidak pernah diuji.
- Perbarui `STATE.md` setiap kali posisi riset berubah, dan tambahkan entri baru
  di `journal/` untuk tiap sesi.
- Sebelum konteks penuh, perbarui berkas `PROMPT_KELANJUTAN.md` ini.
