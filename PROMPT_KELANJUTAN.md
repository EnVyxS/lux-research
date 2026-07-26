# Prompt kelanjutan riset LUX

Tempel isi berkas ini sebagai pesan pertama di sesi baru.

---

Sebelum melakukan apa pun, baca `STATE.md` di repositori GitHub publik **EnVyxS/lux-research**. Berkas itu jurnal tunggal dan satu-satunya sumber kebenaran tentang posisi riset. **Jangan membaca `journal/` secara utuh.** Lanjutkan dari titik terakhir; jangan memulai dari awal dan jangan mengulang pekerjaan yang sudah selesai.

## Konteks

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang karena tercemar survivorship bias dan overfitting. Mesin lokal tidak sanggup backtest penuh dan tidak ada VM cloud karena kendala kartu kredit, jadi **seluruh komputasi berjalan di GitHub Actions** dan repo adalah penyimpanan data sekaligus jurnal riset.

## Batas alat yang harus dipahami sejak awal

- Sandbox agen **tidak punya jaringan**. Semua pengambilan data terjadi di runner Actions.
- Agen **tidak bisa membaca log workflow**; daftar alat GitHub tidak memuat satu pun fungsi Actions. Solusi yang sudah berjalan: setiap workflow menulis hasilnya ke `reports/` lalu commit balik, dan agen membacanya lewat API biasa.
- Agen **tidak bisa memicu workflow manual**. Tiap workflow punya filter `paths` pada berkasnya sendiri, jadi menyuntingnya adalah cara memicunya.
- Agen tidak bisa membuat rilis; runner melakukannya lewat `gh release upload`.
- REST `fapi.binance.com` mengembalikan **HTTP 451** dari runner. Jangan taruh di jalur kritis.
- Untuk penggantian berkas utuh gunakan `push_files`, bukan `create_or_update_file` — SHA blob menjadi basi begitu ada tulisan lain.

## Posisi sekarang, ringkas

Sembilan hipotesis sudah divonis, **seluruhnya DITOLAK**. Yang terbaik adalah **H-009**: ekspektasi **+0,041359R** dengan **nol gerbang gagal** — pertama kalinya kesembilan gerbang mutu lulus bersamaan. Ia ditolak hanya oleh ambang pra-registrasi 0,05R. Jarak menuju kelayakan tunggal dan terukur: **+0,008641R, yaitu naik 20,9%.**

Kerugian ekor sudah diselesaikan. Penyebabnya **funding pada ekor, bukan pada rerata**: pada perdagangan terburuk H-008, funding menyumbang 0,9228R dari kerugian 1,9769R, yaitu 46,7%. Memaksa keluar saat carry terealisasi melewati 0,25R — ambang **dipatok, bukan dilombakan** — memindahkan gerbang `invarian_risiko` dari −1,9769R ke **−1,2698R**, dan memotong tepat kelima perdagangan yang carry-nya di atas ambang tanpa satu pun korban sampingan.

**Tindakan berikutnya: ADR-010, gerbang konsentrasi.** Sepuluh dari 40 simbol menghasilkan 101,2% laba dan 30 sisanya merugi −7,61R. Tidak satu pun dari sembilan gerbang menilai konsentrasi. Datanya sudah dikomit di `per_simbol`, jadi **tidak butuh run baru**.

## Cara saya ingin kamu bekerja

- Ketika saya menulis "lanjut", teruskan langsung dari titik terakhir tanpa konfirmasi dan tanpa mengulang penjelasan.
- Pisahkan fakta terverifikasi dari asumsi. Asumsi hanya naik jadi fakta bila ada bukti terlampir berupa commit, run ID, atau kutipan sumber.
- Katakan bila saya salah, dan katakan bila kamu sendiri salah.
- Perbarui `STATE.md` setiap kali posisi riset berubah, tambahkan entri `journal/` tiap sesi.
- Sebelum konteks penuh, perbarui berkas ini.

## Aturan yang dibayar dengan kesalahan nyata — jangan pelajari ulang dengan cara mahal

1. Angka yang lulus gerbang belum tentu benar.
2. SHA laporan yang tidak berubah berarti **belum ditulis**, bukan berhasil.
3. Penjelasan yang membuat anomali terasa wajar harus dicurigai lebih keras daripada anomalinya.
4. Lihat sebaran mentah sebelum berteori.
5. Hipotesis yang ditolak tetap ditolak. Ambang tidak pernah disetel ulang setelah hasil terlihat.
6. Percobaan yang informatif ke dua arah lebih berharga daripada yang dirancang agar berhasil.
7. Saringan yang membuang perdagangan tidak otomatis membuang perdagangan yang buruk.
8. Periksa apakah dugaanmu mungkin secara konstruksi sebelum menjadwalkannya.
9. Periksa apakah laporan yang sudah dikomit sudah menjawabnya sebelum menjalankan run.
10. Gerbang yang kegagalannya tidak tertulis ke `reports/` adalah titik buta yang menyamar sebagai gerbang.
11. **Rerata tidak mengatakan apa pun tentang ekor, dan ekor tidak mengatakan apa pun tentang frekuensi.**
12. **Batas risiko tidak dilombakan.**
13. **Peristiwa yang terlalu jarang tidak dapat dipilih oleh pemilih dalam sampel, seberapa pun bergunanya.**
14. **Ramalan yang salah lebih murah daripada ramalan yang tidak pernah ditulis.**

Selain itu: pytest wajib hijau sebelum unduhan; gerbang yang bisa gagal ditaruh sebelum unduhan, bukan sesudahnya; commit laporan tanpa berkas hasil berarti run **gagal**; hijau bukan berarti berhasil — baca laporan yang dikomit; jangan pernah menekan hasil negatif; jangan pernah mematok parameter yang menang pasca-hoc; jangan pernah menyempitkan grid setelah melihat pemenangnya.

**Yang DILARANG:** melombakan ambang pengaman dalam bentuk apa pun; mematok `imbalan_R` ke 4,0; menghitung ulang hipotesis yang sudah divonis; melonggarkan ambang `invarian_risiko` dari −1,5R; **menurunkan ambang ekspektasi 0,05R karena H-009 nyaris mencapainya.**
