# Prompt kelanjutan — mulai dari sini

Salin isi berkas ini ke sesi baru bila konteks penuh.

---

Sebelum melakukan apa pun, baca `STATE.md` di repo publik **EnVyxS/lux-research**. Berkas itu jurnal tunggal dan satu-satunya sumber kebenaran tentang posisi riset. **Jangan membaca `journal/` secara utuh.** STATE.md saat ini **versi 11**.

Lanjutkan riset LUX. Jangan memulai dari awal dan jangan mengulang pekerjaan yang sudah selesai.

## Posisi singkat

Delapan hipotesis sudah divonis, **seluruhnya DITOLAK**. Terbaik: **H-007, +0,04044R**, gagal hanya pada gerbang `invarian_risiko` (−1,9769R terhadap ambang −1,5R). Kriteria lulus adalah ekspektasi ≥ 0,05R **dan** sembilan gerbang lulus.

S11 baru saja menutup satu jalur: **funding bukan penyebab kerugian ekor.** H-008 memasang keluar paksa saat carry terealisasi melewati ambang; ia menembak **2 kali dari 14.933 perdagangan**, walk-forward mematikannya di **334 dari 356 jendela**, tidak pernah memilih ambang 0,50, dan kerugian terburuk tetap **−1,9769R**, identik sampai empat desimal dengan H-007.

**Penyebab kerugian −1,977R belum diketahui.** Dua kandidat, keduanya belum diukur: keluar di pembukaan bar yang menganga melewati stop (`umur`/`carry`/`akhir_data` dieksekusi di pembukaan, sebelum stop diperiksa), atau stop yang sangat rapat sehingga biaya dalam R membengkak.

## Tindakan berikutnya

**ADR-009 — diagnosis, bukan mekanisme.** Bongkar perdagangan terburuk: alasan keluar, lebar stop terhadap harga, pembongkaran biaya, dan apakah pembukaan bar keluar berada di luar stop. Ini pembacaan atas hasil yang sudah ada, tidak butuh pra-registrasi, dan **tidak boleh menghasilkan putusan hipotesis**. Mekanisme baru dirancang setelah angkanya terlihat, bukan sebelumnya.

Setelah itu: horizon 4h (**prasyarat: jalankan `validate.yml` untuk 4h**), lalu funding sebagai sinyal arah.

## Batas alat, sudah diverifikasi

- Sandbox agen **tidak punya jaringan**. Semua pengambilan data terjadi di runner Actions.
- Daftar alat GitHub **tidak memuat satu pun fungsi Actions**: tidak ada pembacaan run, job, langkah, atau log. Setiap workflow wajib menulis hasilnya ke `reports/` dan commit balik dengan `if: always()` — termasuk **setiap langkah pra-terbang**.
- Agen tidak bisa memicu workflow manual. Tiap workflow punya filter `paths` pada berkasnya sendiri; menyuntingnya adalah satu-satunya cara memicunya.
- Agen tidak bisa membuat rilis. Runner melakukannya lewat `gh release upload`.
- REST `fapi.binance.com` mengembalikan **HTTP 451** dari runner. Jangan taruh di jalur kritis.
- **Commit laporan tanpa berkas hasil berarti run GAGAL, bukan sedang berjalan.**
- Blob laporan yang tidak berubah berarti **belum ditulis**, bukan berhasil.

## Cara bekerja yang saya harapkan

- Ketika saya menulis "lanjut", teruskan langsung dari titik terakhir tanpa konfirmasi dan tanpa mengulang penjelasan.
- Pisahkan fakta terverifikasi dari asumsi. Asumsi naik jadi fakta hanya dengan bukti terlampir: commit, run ID, atau kutipan sumber.
- Katakan bila saya salah, dan katakan bila kamu sendiri salah.
- Perbarui `STATE.md` setiap kali posisi riset berubah; tambahkan entri `journal/` tiap sesi; perbarui berkas ini sebelum konteks penuh.
- **Jangan pernah menyembunyikan hasil negatif.** Itu yang meracuni bot v8.4.
- **Jangan mematok parameter yang menang pasca-hoc**, dan jangan mempersempit grid setelah melihat nilai mana yang menang.
- Sebelum menjadwalkan percobaan, periksa apakah laporan yang sudah dikomit sudah menjawabnya. Aturan ini lahir dari ADR-008 yang biayanya satu run penuh.
