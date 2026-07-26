# Prompt kelanjutan — tempel ini di sesi baru

> Disegarkan 2026-07-26 16:20 WIB, sesudah commit `fa2a7a65` (STATE versi 18, tahap S13).
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
- Agen **tidak bisa memicu workflow manual**. Setiap workflow punya filter `paths` pada berkasnya sendiri, jadi push ke berkas itu yang memicunya. `tests.yml` memfilter `lux/**` dan `tests/**`; `backtest.yml` memfilter dirinya sendiri.
- Agen tidak bisa membuat atau mengunggah rilis; runner melakukannya lewat `gh release upload`.
- REST `fapi.binance.com` mengembalikan **HTTP 451** dari runner. Jangan taruh di jalur kritis. CDN `data.binance.vision` normal.
- `search_code` **tidak berguna di repo ini** — indeks GitHub belum memuatnya dan mengembalikan nol hasil untuk berkas yang jelas ada. Baca berkas langsung.
- Untuk menulis, **pakai `push_files`**, bukan `create_or_update_file`: SHA blob basi begitu ada tulisan. Bentuk argumennya `{ toolName, toolArguments: { owner, repo, branch, message, files } }` — jangan menaruh `owner`/`repo`/`branch` di tingkat atas.
- **`push_files` mengganti seluruh isi berkas.** Tulisan yang terpotong di tengah tidak menghasilkan berkas separuh, tetapi juga tidak menghasilkan apa pun — periksa hasilnya, jangan berasumsi.
- Runner tidak punya `scipy`. Statistik memakai numpy dan pendekatan normal.
- Analisis atas laporan yang sudah dikomit bisa dikerjakan di sandbox tanpa jaringan. **Begitulah cacat terbesar sesi ini ditemukan** — bukan oleh run baru, melainkan dengan menghitung ulang `per_simbol` sendiri.

### Posisi sekarang, ringkas

- **Dua belas hipotesis: sepuluh ditolak, satu diterima pada 40 simbol, satu ditolak pada 438 simbol — dan yang terakhir TERCEMAR.**
- **H-011 DITOLAK** (run `30194733599`, laporan commit `2bb7b963`, sidik `8a6efde6d333d8b5`, 838,1 detik). Kriteria utama, dihitung tangan dari `per_simbol`: ekspektasi 398 simbol tertahan **−0,091519R** atas 124.603 perdagangan. Empat gerbang gagal: `entri_acak` p 0,0631, `invarian_risiko` −470,0612R, `konsentrasi` tak dapat dinilai, `funding_ekor` lewat `funding_maks_R` 2,3900.
- **Tetapi penolakan itu tidak informatif tentang sinyal.** Seluruh angkanya dihasilkan oleh satu simbol: **USDCUSDT**, pasangan stablecoin terhadap stablecoin, 649 perdagangan, total **−18.861,06R**, ekspektasi **−29,06R per perdagangan**. ATR/harga-nya hampir nol sehingga `stop_frac` mencapai **3,2e−06**, dan karena biaya dalam R berbanding balik dengan `stop_frac`, biaya transaksi satu perdagangan menjadi **312,73R**. Sepuluh perdagangan terburuk dari 438 simbol semuanya miliknya.
- **Yang cacat adalah definisi semesta, bukan mesin dan bukan sinyal.** Kriteria kelayakan (`min_bar_1h`, volume, rasio bar datar) tidak satu pun menyentuh volatilitas; saringan volume bahkan menarik pasangan stablecoin masuk. Cacat ini berumur sejak ADR-003 dan tak terlihat selama sepuluh hipotesis karena 40 simbol pertama secara alfabet tidak memuat satu pun stablecoin.
- **Baris 40 simbol di H-011 keluar identik bit-per-bit dengan H-010** (622,2348185492804R; 0,05302836360569971). Mekanismenya memang diimpor tanpa perubahan; pagar pra-terbang bekerja — dan tetap tidak cukup, karena pagar yang memastikan masukan *identik* tidak memastikan masukan *sah*.
- **H-010 tidak direhabilitasi oleh pencemaran ini.** Ia tetap satu run, 40 simbol yang dipilih secara alfabet, dengan empat keberatan — dan keberatan terkuatnya kini terbukti: pada 300 permutasi, `entri_acak` mekanisme yang sama memberi p **0,0631**, yakni **gagal**. Resolusi yang lebih tinggi membalik putusan yang dulu lolos dengan jarak satu satuan resolusi.
- **542 pengujian lulus**, laporan pada commit `e22745aa`. Utang statistik ADR-013 lunas; laporan kini memuat simpangan baku, galat baku, kuartil, dan jarak ambang. Di H-011 jaraknya **−11,22 galat baku**.
- Dataset Tier B sah: 14.545.679 bar 1h, 790 simbol, universe layak v2 **438 simbol** (kini berstatus **cacat**), funding 1.982.017 baris.

### Harga yang sudah terbayar dan tidak bisa ditarik

**Himpunan tertahan habis.** Hasil per simbol untuk seluruh 438 simbol pada 1h sudah dilihat, jadi setiap pengujian 1h berikutnya bersifat dalam-sampel pada tingkat semesta. Dimensi yang masih benar-benar bersih hanya **waktu** dan **kerangka waktu 4h**. Terima batas ini; jangan akali.

### Godaan yang wajib ditolak

Membuang USDCUSDT menghasilkan **+0,060163R** pada 397 simbol tertahan. **Angka itu haram dipakai sebagai kelulusan atau sebagai bukti H-010 benar** — itu penyubsetan simbol pasca-hasil yang dilarang ADR-013 bagian 8, dan sudah masuk daftar angka terlarang di STATE bagian 4 beserta alasannya. Ia hanya boleh muncul berlabel diagnostik, selalu bersama larangannya.

Jalan yang sah hanya satu: **kriteria kelayakan semesta yang dipra-registrasi dan berlaku seragam untuk semua simbol**, bukan pengecualian yang dipilih sesudah melihat hasil. Itulah H-012.

### Tindakan berikutnya

1. **H-012 — sudah didaftarkan penuh di `decisions/ADR-014` bagian 8, ambang dan tujuh ramalan dibekukan.** Dua perubahan saja: (a) semesta membuang simbol yang **median `stop_frac` < 0,004** — turunan aritmetis, karena biaya bolak-balik 0,002 dari harga berarti tepat 0,5R pada `stop_frac` 0,004; (b) mesin **menolak entri yang biayanya melampaui 0,5R**, sebagai pagar risiko sejenis `maks_carry_R`, bukan knob yang dicari, dan penolakannya wajib tercatat sebagai alasan tersendiri di laporan. Kriteria utama: ekspektasi berbobot perdagangan pada **periode waktu luar sampel yang dibekukan**. Ramalan saya: **0,010–0,045, jadi H-012 gagal.** Urutan wajib: modul dan pengujian hijau lebih dulu, workflow dibalik sesudahnya. **Dilarang menyebutnya "H-010 setelah perbaikan".**
2. **Pisahkan sinyal dari geometri keluar.** Skor entri acak jatuh 56,8% di H-010; selama belum terpisah, klaim "ada keunggulan sinyal" belum berdiri. Butuh ADR sendiri. Ini pertanyaan paling penting yang tersisa selain H-012.
3. Perketat `lux/funding.py::gerbang_lulus` (utang ADR-011 bagian 6).
4. Horizon 4h — prasyaratnya `validate.yml` untuk 4h. Lalu funding sebagai sinyal berarah. Masing-masing butuh ADR.
5. **Uji silang Dataset G lama (528 simbol)** — satu-satunya butir yang masih terbuka dari daftar tugas awal.
6. `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md`; salin ADR-001 dan ADR-002 ke `decisions/` (teksnya **tidak** ada di `reference/`, jadi perlu sumber); reporter Notion butuh Secret `NOTION_TOKEN`; instruksi Gatekeeper masih menyebut sembilan gerbang.
7. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, dengan ≥24 shard.

**Sudah lunas, jangan dikerjakan ulang:** `std_R`/`galat_baku_R` lewat `lux/analisis/sebaran.py`; docstring `lux/costs.py` (`c80cf6d3`).

### Cara saya ingin kamu bekerja

- Ketika saya menulis "lanjut", teruskan langsung dari titik terakhir tanpa konfirmasi dan tanpa mengulang penjelasan.
- **Pisahkan fakta terverifikasi dari asumsi.** Asumsi hanya naik jadi fakta bila ada bukti terlampir berupa commit, run ID, atau kutipan sumber.
- Katakan bila saya salah, dan katakan bila kamu sendiri salah.
- Perbarui `STATE.md` setiap kali posisi riset berubah, tambahkan entri `journal/` tiap sesi.
- Sebelum konteks penuh, perbarui berkas ini.

---

## Aturan kerja yang dibayar mahal — jangan pelajari ulang

1. **Pytest hijau sebelum unduhan apa pun.** Gerbang yang bisa gagal ditaruh sebelum langkah panjang, bukan sesudahnya. Berlaku juga di dalam kode: `ukur_sebaran` melempar galat pada nilai tidak finit, jadi `runner.py` menangkapnya dan menulisnya ke laporan alih-alih menjatuhkan run 438 simbol di ujungnya.
2. **Modul baru berdiri hijau sendiri lebih dulu, penyambungan menyusul.** Dipakai empat kali: 462→467, 488→494, 494→510, 525→542.
3. **Tulis ramalan jumlah pengujian sebelum membaca laporan.** Tujuh ramalan berturut-turut tepat.
4. **Blob laporan yang tidak berubah berarti belum ditulis** — bukan berhasil, bukan gagal. Hasil H-011 butuh enam pengambilan; H-010 sebelas.
5. **Commit laporan tanpa berkas hasil berarti run GAGAL.** Hijau ≠ berhasil; baca laporan yang dikomit.
6. **Baca modulnya sebelum menulis kode terhadapnya.** Jangan pernah menebak nama simbol yang diimpor.
7. **Jangan menyunting modul yang dibekukan** — `run_wf`, `run_h002`, `run_h003`, `run_h007`, `run_h008`, `run_h009`. `run_h009` memasang `assert` bahwa gridnya identik `run_h007`, jadi `run_h007.IMBALAN` haram disunting.
8. **Jangan mengimpor ke arah yang bisa menutup siklus** (cacat `4b77617`). Itu sebabnya `konsentrasi.py`, `funding_ekor.py`, dan `sebaran.py` berdiri sebagai modul sendiri.
9. **Jangan menulis angka jumlah dengan tangan.** Satu literal tripwire per hal yang dijaga: `test_gerbang_kesebelas.py` untuk jumlah gerbang, `BATAS_H010` untuk batas 40 simbol.
10. **Periksa setiap hitungan secara aritmetis dan jangan percaya label buatan sendiri.** Empat kekeliruan hitung sejauh ini: "26 simbol positif", label "16 pengujian", dan "226 jendela / 63,5%" yang seharusnya **194 / 54,5%** — angka benarnya sudah ada di tiga tempat di repo. **Cari di repo sebelum memercayai ingatan.**
11. **Keputusan metodologi dikomit sebelum kodenya** (ADR-011 → `funding_ekor.py`; ADR-012 → `run_h010.py`; ADR-013 → `sebaran.py` dan `run_h011.py`; ADR-014 → lantai `stop_frac`).
12. **Ambang pra-registrasi tidak berubah setelah hasil terlihat** — dan sesudah kelulusan ia juga tidak boleh diperketat. Keduanya sama-sama menyetel ambang terhadap hasil.
13. **Hipotesis yang ditolak tidak dihitung ulang.** Hipotesis serempak butuh koreksi multiplisitas yang dipatok di muka (p H-005 0,0396 lolos 0,05 tetapi gagal 0,0167).
14. **Rerata bukan ekor. Porsi terhadap nilai bersih bukan konsentrasi. Pencilan bukan sebaran. Proksi yang berkorelasi 0,97 dengan hal lain bukan proksi.**
15. **Gerbang yang memberi jawaban sama pada dua keadaan bertolak belakang tidak memuat informasi.**
16. **Aturan yang diketahui bukan aturan yang diterapkan.**
17. **Batas risiko bukan parameter yang dilombakan.** Pemaksimal ekspektasi akan selalu mematikan pengaman yang menargetkan peristiwa langka (16 dari 14.925 = 0,107%).
18. **Margin sesempit resolusi alat ukur bukan margin.** p 0,049505 pada 100 permutasi adalah satu satuan dari kegagalan — dan pada 300 permutasi ia memang gagal (0,0631).
19. **Ekspektasi yang naik karena penyebutnya menyusut bukan keunggulan yang lebih besar.**
20. **Kecurigaan harus NAIK, bukan turun, ketika hasilnya menyenangkan.**
21. **Galat baku yang dihitung di bawah andaian kebebasan yang salah hanya boleh menjatuhkan klaim, tidak boleh menegakkannya.** Jangan pernah mengarang statistik yang tidak ada di laporan.
22. **Jangan menuntut kesamaan bit pada agregat pecahan.** Penjumlahan pecahan tidak asosiatif; pengujian semacam itu menyala pada modul yang benar. Pakai toleransi.
23. **Pagar yang memastikan masukan identik tidak memastikan masukan sah.** Semua pagar `run_h011` lulus dan semestanya tetap memuat simbol yang satuan risikonya runtuh.
24. **Satu simbol dapat mendominasi agregat 438 simbol.** Periksa agregat terhadap ekstremnya sendiri sebelum menafsirkannya. Dan **biaya yang dibagi oleh penyebut yang bisa mendekati nol adalah biaya tak terbatas** — satuan risiko butuh lantai, dan lantainya wajib dipra-registrasi, bukan berupa pembuangan simbol pasca-hasil.
25. **Himpunan tertahan habis pada saat pertama kali dilihat.** Belanjakan hanya pada pertanyaan yang mekanismenya sudah bersih.
26. **Cacat yang membalik tanda hasil tidak boleh diperbaiki di dalam hipotesis yang sama.** Perbaikannya melahirkan hipotesis baru.
27. **Eksperimen yang tercemar tidak informatif ke arah mana pun.** Ia memakan satu hipotesis tanpa membayar pengetahuan; catat sebagai kerugian, bukan kemajuan.
28. **Jangan pernah menekan hasil negatif, membuang simbol merugi, membuang simbol muda, mematok parameter yang menang belakangan, menurunkan ambang 0,05R, atau menyebut sistem layak diperdagangkan.**
