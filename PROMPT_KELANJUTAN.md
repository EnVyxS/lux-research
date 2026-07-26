# Prompt kelanjutan — tempel ini di sesi baru

> Disegarkan 2026-07-26 17:05 WIB, sesudah commit `62e1de14` (578 pengujian lulus; H-012 tahap 1–3 dari 5 selesai).
> Berkas ini hanya jembatan. **Sumber kebenaran tunggal tetap `STATE.md`** (versi 18, commit `fa2a7a65`).

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
- `search_code` **tidak berguna di repo ini** — indeks GitHub mengembalikan nol hasil untuk berkas yang jelas ada. Baca berkas langsung.
- **`get_file_contents` menuntut SHA 40 karakter penuh** atau nama branch/tag. Ref pendek gagal: `could not resolve ref "cad9b4df"`.
- Untuk menulis, **pakai `push_files`**, bukan `create_or_update_file`: SHA blob basi begitu ada tulisan. Bentuk argumennya `{ toolName, toolArguments: { owner, repo, branch, message, files } }` — jangan menaruh `owner`/`repo`/`branch` di tingkat atas.
- **`push_files` mengganti seluruh isi berkas.** Tulisan yang terpotong di tengah tidak menghasilkan berkas separuh, tetapi juga tidak menghasilkan apa pun — periksa hasilnya, jangan berasumsi. **Baca berkas sebelum menulis ulang.**
- Runner tidak punya `scipy`. Statistik memakai numpy dan pendekatan normal.
- Analisis atas laporan yang sudah dikomit bisa dikerjakan di sandbox tanpa jaringan. **Begitulah cacat terbesar riset ini ditemukan** — bukan oleh run baru, melainkan dengan menghitung ulang `per_simbol` sendiri.

### Posisi sekarang, ringkas

- **Dua belas hipotesis: sepuluh ditolak, satu diterima pada 40 simbol, satu ditolak pada 438 simbol — dan yang terakhir TERCEMAR.**
- **H-011 DITOLAK** (run `30194733599`, laporan commit `2bb7b963`, sidik `8a6efde6d333d8b5`, 838,1 detik). Kriteria utama, dihitung tangan dari `per_simbol`: ekspektasi 398 simbol tertahan **−0,091519R** atas 124.603 perdagangan. Empat gerbang gagal: `entri_acak` p 0,0631, `invarian_risiko` −470,0612R, `konsentrasi` tak dapat dinilai, `funding_ekor` lewat `funding_maks_R` 2,3900.
- **Penolakan itu tidak informatif tentang sinyal.** Seluruh angkanya dihasilkan satu simbol: **USDCUSDT**, 649 perdagangan, total **−18.861,06R**, ekspektasi **−29,06R per perdagangan**. ATR/harga-nya hampir nol sehingga `stop_frac` mencapai **3,1984e−06**, dan karena biaya dalam R berbanding balik dengan `stop_frac`, biaya satu perdagangan menjadi **312,73R**.
- **Yang cacat adalah definisi semesta, bukan mesin dan bukan sinyal.** Tak satu pun kriteria kelayakan menyentuh volatilitas. Cacat berumur sejak ADR-003, tak terlihat selama sepuluh hipotesis karena 40 simbol pertama secara alfabet tidak memuat satu pun stablecoin.
- **H-010 tidak direhabilitasi.** Keberatan terkuatnya kini terbukti: pada 300 permutasi, `entri_acak` mekanisme yang sama memberi p **0,0631** — gagal.
- **578 pengujian lulus**, laporan pada commit `62e1de14`.

### H-012 — sudah berjalan, tiga dari lima tahap selesai

Pra-registrasi penuh ada di `decisions/ADR-014` bagian 8: ambang dan **tujuh ramalan dibekukan**, termasuk ramalan saya sendiri bahwa **H-012 gagal** (0,010–0,045 pada periode tahan-waktu). Dua perubahan saja, tidak lebih.

**Selesai dan hijau:**

1. `lux/degenerasi.py` + 21 pengujian — commit **`5af7a6bb`**, 563 lulus. Modul aritmetika murni. `AMBANG_MIN_STOP_FRAC = 0.004`, `AMBANG_BIAYA_MASUK_R = 0.5`, dan keduanya **turunan, bukan setelan**: biaya bolak-balik model bawaan 0,002 dari harga, dan 0,002/0,004 = 0,5, jadi lantai dan pengaman adalah satu pernyataan yang sama. Sengaja **tidak** mengimpor apa pun dari `lux.backtest` supaya engine boleh mengimpornya tanpa menutup lingkaran. Bar ber-ATR nol **disertakan** dalam median (membuangnya menaikkan median dan menyelamatkan simbol terburuk); simbol yang tak dapat dinilai **ditolak**.
2. Pengaman mesin — commit **`6ebf87b3`**, 574 lulus. `Konfig.maks_biaya_masuk_R`, bawaan **0,0 berarti MATI**, diletakkan paling akhir supaya posisi argumen medan lama tidak bergeser, bawaannya dikunci pengujian sehingga H-001b…H-011 tetap dapat diulang. Dinilai di dalam blok entri `engine.jalankan` tepat setelah `stop_pecahan = jarak/masuk` dihitung. **Penolakan bukan perdagangan**: tidak masuk histogram alasan keluar, dan dihitung terpisah dari penolakan carry. Jumlahnya di `Hasil.entri_ditolak_biaya`.
3. Perambatan walk-forward — commit **`62e1de14`**, 578 lulus. `HasilWalkForward.entri_ditolak_biaya` menjumlahkan **jendela uji saja**; penolakan saat pemilihan parameter adalah bagian dari pencarian dan akan terlipat sebanyak jumlah kandidat. Kunci `entri_ditolak_biaya` kini ada di `ringkas()`.

**Sisa, urutannya wajib:**

4. **`runner.jalankan_spek`**: teruskan `entri_ditolak_biaya` dari `ringkas()` ke JSON dan Markdown laporan sebagai alasan tersendiri, di samping `alasan_keluar` dan `diagnosa_biaya`. Tambahkan lantai semesta di `muat_konteks` lewat `degenerasi.saring_semesta` — semesta dibangun di sana dari `reports/universe_layak_v2.json` sebagai `sorted(semesta)[:limit]`. **`Opsi` belum punya medan lantai.** Simbol yang dibuang wajib tertulis di laporan beserta `median_stop_frac`-nya, bukan hilang diam-diam.
5. **`config/lux.yaml`** (versi 2) belum punya `universe.min_median_stop_frac: 0.004` maupun `risiko.maks_biaya_masuk_R: 0.5`. Tajuk berkas itu menyatakan setiap angka yang memengaruhi hasil harus tinggal di sana dan setiap perubahan wajib dijurnalkan.
6. **`lux/backtest/run_h012.py` + pengujiannya.** Mekanisme diimpor **tanpa perubahan** dari `run_h010`/`run_h009` (grid [20,55,100]×[2,4,6,8], `maks_carry_realisasi_R` 0,25, `maks_umur_bar` 168, kriteria 0,05R/100/0,05/0,5, `ulangan` 300). Wajib ada: `BATAS_VOID = 20` — bila lebih dari 20 simbol terbuang, **H-012 batal sebelum diadili**; batas periode tahan-waktu yang dibekukan; tujuh ramalan tertulis; semua pagar di depan sebelum satu bar pun dimuat.
7. **`.github/workflows/backtest.yml` dibalik paling akhir.** Langkah `impor` saat ini memaku identitas H-011↔H-010, `BATAS_H010`, penyambungan `sebaran`, dan sebelas nama gerbang — semuanya harus ditulis ulang untuk H-012, begitu pula tajuk penjelasnya.

**Dilarang menyebut H-012 "H-010 setelah perbaikan".**

### Satu temuan tahap 3 yang mengubah tafsir, bukan ambangnya

Pada simbol yang **seluruhnya** degenerat, pengaman menolak entri juga saat pemilihan parameter, sehingga semua kandidat berskor `-inf` dan **seluruh jendelanya dilewati**. Simbol seperti itu menyumbang nol penolakan dan nol perdagangan — ia tidak muncul di angka penolakan sama sekali; yang membuatnya terlihat hanya lantai semesta. Akibatnya **ramalan 5 ADR-014 (500–5.000 entri ditolak) mengukur hal yang lebih sempit** daripada yang dibayangkan saat ditulis: ia hanya menghitung simbol yang berubah degenerat di tengah jalan. Ramalan itu **tidak diubah** — ambang pra-registrasi tidak bergerak setelah kodenya dipahami; yang dicatat adalah penyempitan tafsirnya.

### Harga yang sudah terbayar dan tidak bisa ditarik

**Himpunan tertahan habis.** Hasil per simbol untuk seluruh 438 simbol pada 1h sudah dilihat, jadi setiap pengujian 1h berikutnya bersifat dalam-sampel pada tingkat semesta. Dimensi yang masih benar-benar bersih hanya **waktu** dan **kerangka waktu 4h**. Terima batas ini; jangan akali.

### Godaan yang wajib ditolak

Membuang USDCUSDT menghasilkan **+0,060163R** pada 397 simbol tertahan. **Angka itu haram dipakai sebagai kelulusan atau sebagai bukti H-010 benar** — itu penyubsetan simbol pasca-hasil yang dilarang ADR-013 bagian 8, dan sudah masuk daftar angka terlarang di STATE bagian 4. Ia hanya boleh muncul berlabel diagnostik, selalu bersama larangannya. Jalan yang sah hanya satu: kriteria kelayakan semesta yang **dipra-registrasi dan seragam**, yaitu H-012.

### Tindakan berikutnya sesudah H-012

1. **Pisahkan sinyal dari geometri keluar.** Skor entri acak jatuh 56,8% di H-010; selama belum terpisah, klaim "ada keunggulan sinyal" belum berdiri. Butuh ADR sendiri. Pertanyaan paling penting yang tersisa.
2. Perketat `lux/funding.py::gerbang_lulus` (utang ADR-011 bagian 6).
3. Horizon 4h — prasyaratnya `validate.yml` untuk 4h. Lalu funding sebagai sinyal berarah. Masing-masing butuh ADR.
4. **Uji silang Dataset G lama (528 simbol)** — satu-satunya butir yang masih terbuka dari daftar tugas awal.
5. `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md`; salin ADR-001 dan ADR-002 ke `decisions/` (teksnya **tidak** ada di `reference/`); reporter Notion butuh Secret `NOTION_TOKEN`; instruksi Gatekeeper masih menyebut sembilan gerbang.
6. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, dengan ≥24 shard.

**Sudah lunas, jangan dikerjakan ulang:** `std_R`/`galat_baku_R` lewat `lux/analisis/sebaran.py`; docstring `lux/costs.py` (`c80cf6d3`); modul degenerasi, pengaman mesin, dan perambatan walk-forward.

### Cara saya ingin kamu bekerja

- Ketika saya menulis "lanjut", teruskan langsung dari titik terakhir tanpa konfirmasi dan tanpa mengulang penjelasan.
- **Pisahkan fakta terverifikasi dari asumsi.** Asumsi hanya naik jadi fakta bila ada bukti terlampir berupa commit, run ID, atau kutipan sumber.
- Katakan bila saya salah, dan katakan bila kamu sendiri salah.
- Perbarui `STATE.md` setiap kali posisi riset berubah, tambahkan entri `journal/` tiap sesi.
- Sebelum konteks penuh, perbarui berkas ini.

---

## Aturan kerja yang dibayar mahal — jangan pelajari ulang

1. **Pytest hijau sebelum unduhan apa pun.** Gerbang yang bisa gagal ditaruh sebelum langkah panjang, bukan sesudahnya. Berlaku juga di dalam kode: `ukur_sebaran` melempar galat pada nilai tidak finit, jadi `runner.py` menangkapnya dan menulisnya ke laporan alih-alih menjatuhkan run 438 simbol di ujungnya.
2. **Modul baru berdiri hijau sendiri lebih dulu, penyambungan menyusul.** Dipakai enam kali: 462→467, 488→494, 494→510, 525→542, 563→574, 574→578.
3. **Tulis ramalan jumlah pengujian sebelum membaca laporan.** Sepuluh ramalan berturut-turut tepat: 563, 574, 578 yang terakhir.
4. **Blob laporan yang tidak berubah berarti belum ditulis** — bukan berhasil, bukan gagal. Hasil H-011 butuh enam pengambilan; H-010 sebelas; laporan 578 butuh empat.
5. **Commit laporan tanpa berkas hasil berarti run GAGAL.** Hijau ≠ berhasil; baca laporan yang dikomit.
6. **Baca modulnya sebelum menulis kode terhadapnya, dan baca berkasnya sebelum menulis ulang.** Jangan pernah menebak nama simbol yang diimpor.
7. **Jangan menyunting modul yang dibekukan** — `run_wf`, `run_h002`, `run_h003`, `run_h007`, `run_h008`, `run_h009`. `run_h009` memasang `assert` bahwa gridnya identik `run_h007`, jadi `run_h007.IMBALAN` haram disunting.
8. **Jangan mengimpor ke arah yang bisa menutup siklus** (cacat `4b77617`). Itu sebabnya `konsentrasi.py`, `funding_ekor.py`, `sebaran.py`, dan `degenerasi.py` berdiri sebagai modul sendiri — yang terakhir di tingkat atas, bukan di dalam `lux/backtest/`, justru supaya engine boleh mengimpornya.
9. **Medan `Konfig` baru diletakkan paling akhir dan bawaannya MATI.** Empat saringan mesin kini bawaannya nol: `maks_umur_bar`, `maks_carry_R`, `maks_carry_realisasi_R`, `maks_biaya_masuk_R`. Itulah satu-satunya alasan hasil lama masih dapat diulang.
10. **Jangan menulis angka jumlah dengan tangan.** Satu literal tripwire per hal yang dijaga: `test_gerbang_kesebelas.py` untuk jumlah gerbang, `BATAS_H010` untuk batas 40 simbol, ambang di `test_degenerasi.py`, bawaan mati di `test_pengaman_biaya.py`.
11. **Periksa setiap hitungan secara aritmetis dan jangan percaya label buatan sendiri.** Kekeliruan hitung sejauh ini: "26 simbol positif", label "16 pengujian", dan "226 jendela / 63,5%" yang seharusnya **194 / 54,5%**. **Cari di repo sebelum memercayai ingatan.**
12. **Keputusan metodologi dikomit sebelum kodenya** (ADR-011 → `funding_ekor.py`; ADR-012 → `run_h010.py`; ADR-013 → `sebaran.py` dan `run_h011.py`; ADR-014 → `degenerasi.py` dan pengaman mesin).
13. **Ambang pra-registrasi tidak berubah setelah hasil terlihat** — dan sesudah kelulusan ia juga tidak boleh diperketat. Keduanya sama-sama menyetel ambang terhadap hasil.
14. **Hipotesis yang ditolak tidak dihitung ulang.** Hipotesis serempak butuh koreksi multiplisitas yang dipatok di muka (p H-005 0,0396 lolos 0,05 tetapi gagal 0,0167).
15. **Rerata bukan ekor. Porsi terhadap nilai bersih bukan konsentrasi. Pencilan bukan sebaran. Proksi yang berkorelasi 0,97 dengan hal lain bukan proksi.**
16. **Gerbang yang memberi jawaban sama pada dua keadaan bertolak belakang tidak memuat informasi.**
17. **Aturan yang diketahui bukan aturan yang diterapkan.**
18. **Batas risiko bukan parameter yang dilombakan.** Pemaksimal ekspektasi akan selalu mematikan pengaman yang menargetkan peristiwa langka (16 dari 14.925 = 0,107%).
19. **Margin sesempit resolusi alat ukur bukan margin.** p 0,049505 pada 100 permutasi adalah satu satuan dari kegagalan — dan pada 300 permutasi ia memang gagal (0,0631).
20. **Ekspektasi yang naik karena penyebutnya menyusut bukan keunggulan yang lebih besar.**
21. **Kecurigaan harus NAIK, bukan turun, ketika hasilnya menyenangkan.**
22. **Galat baku yang dihitung di bawah andaian kebebasan yang salah hanya boleh menjatuhkan klaim, tidak boleh menegakkannya.** Jangan pernah mengarang statistik yang tidak ada di laporan.
23. **Jangan menuntut kesamaan bit pada agregat pecahan.** Penjumlahan pecahan tidak asosiatif; pengujian semacam itu menyala pada modul yang benar. Pakai toleransi.
24. **Pagar yang memastikan masukan identik tidak memastikan masukan sah.** Semua pagar `run_h011` lulus dan semestanya tetap memuat simbol yang satuan risikonya runtuh.
25. **Satu simbol dapat mendominasi agregat 438 simbol.** Periksa agregat terhadap ekstremnya sendiri sebelum menafsirkannya. Dan **biaya yang dibagi oleh penyebut yang bisa mendekati nol adalah biaya tak terbatas** — satuan risiko butuh lantai, dipra-registrasi, bukan berupa pembuangan simbol pasca-hasil. **Degenerasi dibuktikan oleh `stop_frac`, bukan oleh ejaan nama simbol** (saringan nama naif sempat menandai `BUSDT` dan `TUSDT`).
26. **Himpunan tertahan habis pada saat pertama kali dilihat.** Belanjakan hanya pada pertanyaan yang mekanismenya sudah bersih.
27. **Cacat yang membalik tanda hasil tidak boleh diperbaiki di dalam hipotesis yang sama.** Perbaikannya melahirkan hipotesis baru.
28. **Eksperimen yang tercemar tidak informatif ke arah mana pun.** Ia memakan satu hipotesis tanpa membayar pengetahuan; catat sebagai kerugian, bukan kemajuan.
29. **Saringan yang menolak entri juga menolaknya saat pemilihan parameter.** Simbol yang selalu degenerat karena itu MENGHILANG dari hitungan penolakan alih-alih muncul di dalamnya. Sebelum menafsirkan angka apa pun yang dihasilkan sebuah saringan, tanyakan lebih dulu keadaan mana yang justru membuat angka itu nol.
30. **Jangan pernah menekan hasil negatif, membuang simbol merugi, membuang simbol muda, mematok parameter yang menang belakangan, menurunkan ambang 0,05R, melonggarkan lantai 0,004 atau pengaman 0,5R, atau menyebut sistem layak diperdagangkan.**
