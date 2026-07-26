# Prompt kelanjutan — tempel ini di sesi baru

> Disegarkan 2026-07-26 15:05 WIB, sesudah commit `80986db3` (STATE versi 16).
> Berkas ini hanya jembatan. **Sumber kebenaran tunggal tetap `STATE.md`.**

---

## Tempel mulai dari sini

Sebelum melakukan apa pun, baca `STATE.md` di repositori GitHub publik **EnVyxS/lux-research**. Itu jurnal tunggal dan satu-satunya sumber kebenaran tentang posisi riset. **Jangan membaca `journal/` secara utuh** — hanya bila ada rujukan spesifik. Lanjutkan dari titik terakhir; jangan mulai dari awal dan jangan mengulang pekerjaan yang sudah selesai.

Selama proses, periksa kembali workflow sebelumnya sebelum menjalankan yang berikutnya, dan hapus workflow yang sudah tidak diperlukan agar repo tetap bersih.

### Konteks

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang karena tercemar survivorship bias dan overfitting. Mesin lokal tidak sanggup backtest penuh dan tidak ada VM cloud, jadi **seluruh komputasi berjalan di GitHub Actions** dan repo GitHub adalah penyimpanan data sekaligus jurnal riset.

### Batas alat yang harus dipahami sejak awal

- Sandbox agen **tidak punya jaringan**. Semua pengambilan data terjadi di runner Actions.
- Agen **tidak bisa membaca log workflow**, dan daftar alat GitHub yang tersedia **tidak memuat satu pun fungsi Actions**. Solusi yang sudah berjalan: setiap workflow menulis hasil ke `reports/` lalu commit balik; agen membacanya lewat API biasa.
- Agen **tidak bisa memicu workflow manual**. Setiap workflow punya filter `paths` pada berkasnya sendiri, jadi push ke berkas itu yang memicunya. `tests.yml` memfilter `lux/**` dan `tests/**`.
- Agen tidak bisa membuat atau mengunggah rilis; runner melakukannya lewat `gh release upload`.
- REST `fapi.binance.com` mengembalikan **HTTP 451** dari runner. Jangan taruh di jalur kritis. CDN `data.binance.vision` normal.
- `search_code` **tidak berguna di repo ini** — indeks GitHub belum memuatnya dan mengembalikan nol hasil untuk berkas yang jelas ada. Baca berkas langsung.
- Untuk menulis, **pakai `push_files`**, bukan `create_or_update_file`: SHA blob basi begitu ada tulisan. Bentuk argumennya `{ toolName, toolArguments: { owner, repo, branch, message, files } }` — jangan menaruh `owner`/`repo`/`branch` di tingkat atas.

### Posisi sekarang, ringkas

- **Sembilan hipotesis diuji, sembilan ditolak.** Terbaik: **H-009 +0,041359R**, dan itu yang pertama **lulus seluruh sembilan gerbang** — ditolak semata oleh ambang profitabilitas 0,05R. Jarak menuju kelayakan **0,008641R atau 20,9%**.
- **Gerbang kini sebelas**, semuanya terkodekan dan hijau: `konsentrasi` (ADR-010, `8cf70f08`) dan `funding_ekor` (ADR-011, `114b0d7e`). **494 pengujian lulus**, laporan `ad691072`.
- Ambang ADR-010 dan ADR-011 ditulis sesudah sebagian data terlihat, jadi keduanya **mengikat mulai H-010** dan tidak diterapkan ke belakang. Ini tertulis terbuka di kedua ADR.
- Tiga orkestrator lama (`run_wf`, `run_h002`, `run_h003`) dibekukan dan hanya menyusun sembilan gerbang; bila dijalankan lagi laporannya gagal, dan itu pernyataan yang benar.
- Dataset Tier B sah: 14.545.679 bar 1h, 790 simbol, universe layak v2 **438 simbol**, funding 1.982.017 baris.

### Tindakan berikutnya

**H-010** — hipotesis pertama yang dinilai sebelas gerbang. Mekanismenya **belum diputuskan** dan wajib punya ADR sendiri lebih dulu, dengan ramalan tertulis sebelum run. Arah yang terbukti punya leverage adalah **sisi keluar**: enam percobaan sisi masuk memberi nol perbaikan, dua percobaan sisi keluar memberi +28% lalu menutup gerbang risiko.

Sisanya ada di `STATE.md` bagian 6, termasuk satu-satunya butir yang masih terbuka dari daftar tugas awal: **uji silang Dataset G lama (528 simbol)**.

### Cara saya ingin kamu bekerja

- Ketika saya menulis "lanjut", teruskan langsung dari titik terakhir tanpa konfirmasi dan tanpa mengulang penjelasan.
- **Pisahkan fakta terverifikasi dari asumsi.** Asumsi hanya naik jadi fakta bila ada bukti terlampir berupa commit, run ID, atau kutipan sumber.
- Katakan bila saya salah, dan katakan bila kamu sendiri salah.
- Perbarui `STATE.md` setiap kali posisi riset berubah, tambahkan entri `journal/` tiap sesi.
- Sebelum konteks penuh, perbarui berkas ini.

---

## Aturan kerja yang dibayar mahal — jangan pelajari ulang

1. **Pytest hijau sebelum unduhan apa pun.** Gerbang yang bisa gagal ditaruh sebelum langkah panjang, bukan sesudahnya.
2. **Modul baru berdiri hijau sendiri lebih dulu, penyambungan menyusul.** Dipakai dua kali: 462 lalu 467, kemudian 488 lalu 494.
3. **Tulis ramalan jumlah pengujian sebelum membaca laporan.**
4. **Blob laporan yang tidak berubah berarti belum ditulis** — bukan berhasil, bukan gagal. Penyambungan terakhir butuh tiga pengambilan.
5. **Commit laporan tanpa berkas hasil berarti run GAGAL.** Hijau ≠ berhasil; baca laporan yang dikomit.
6. **Baca modulnya sebelum menulis kode terhadapnya.** Jangan pernah menebak nama simbol yang diimpor.
7. **Jangan mengimpor ke arah yang bisa menutup siklus** (cacat `4b77617`). Itu sebabnya `konsentrasi.py` dan `funding_ekor.py` berdiri sebagai modul sendiri.
8. **Jangan menulis angka jumlah dengan tangan** — kode memakai `len(NAMA_GERBANG)`. Satu literal tripwire diizinkan, hanya di `test_gerbang_kesebelas.py`. Saya sendiri melanggar ini dan pengujiannya pecah.
9. **Keputusan metodologi dikomit sebelum kodenya** (ADR-011 mendahului `funding_ekor.py`).
10. **Ambang pra-registrasi tidak berubah setelah hasil terlihat.** Gerbang yang ambangnya ditulis setelah melihat data hanya mengikat mulai hipotesis berikutnya.
11. **Hipotesis yang ditolak tidak dihitung ulang.** Hipotesis serempak butuh koreksi multiplisitas yang dipatok di muka (p H-005 0,0396 lolos 0,05 tetapi gagal 0,0167).
12. **Rerata bukan ekor. Porsi terhadap nilai bersih bukan konsentrasi. Pencilan bukan sebaran. Proksi yang berkorelasi 0,97 dengan hal lain bukan proksi.** Empat kekeliruan membaca sebaran, semuanya nyata, semuanya sudah ditarik.
13. **Gerbang yang memberi jawaban sama pada dua keadaan bertolak belakang tidak memuat informasi.** Validasi gerbang baru dengan memisahkan dua keadaan yang sudah diketahui berbeda — sebagai pengujian, bukan keyakinan.
14. **Aturan yang diketahui bukan aturan yang diterapkan.** Aturan 8 sudah ada saat kekeliruan konsentrasi terjadi.
15. **Batas risiko bukan parameter yang dilombakan.** Pemaksimal ekspektasi akan selalu mematikan pengaman yang menargetkan peristiwa langka (16 dari 14.925 = 0,107%).
16. **Jangan pernah menekan hasil negatif, membuang simbol merugi, membuang simbol muda, mematok parameter yang menang belakangan, atau menurunkan ambang 0,05R.**
