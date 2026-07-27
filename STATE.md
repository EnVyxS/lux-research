# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-27 09:56 WIB (versi 28) — ditulis sesudah blob v27 (`e387423cfb4ca67e7bad14301f4e50e551996954`, commit `a3355294`) dibaca **utuh**.

**Tahap sekarang:** S22 — **H-014 DITOLAK.** Run `30221967019` selesai dalam **2 menit 19 detik** dan melahirkan putusan sah: rerata selisih bulanan SS′ − SH′ **−0,027715128544164157R** gagal terhadap ambang 0,020R, dan p uji tanda berpasangan bulanan **0,37596240375962403** gagal terhadap 0,05 (ADR-035). Penggabung keluar berkode **0** (aturan 48). **Empat belas hipotesis dinilai, empat belas ditolak. Nol kandidat bertahan.** Temuan yang lebih penting daripada putusannya: **tanda besaran bergantung pada pembobotan** — satu himpunan 73 bulan yang sama memberi agregat **+0,027654R** (positif) dan rerata bulanan **−0,027715R** (negatif). Itu **cacat kelas keenam belas**, aturan **55**. Dan daftar `git add` di `h014.yml` yang saya tulis sendiri tidak memuat `reports/manifest_aset_4h.json`, sehingga gerbang `checksum` pada 4h **mustahil lulus selamanya** — **cacat kelas ketujuh belas**, aturan **56**.

**Tahap berikutnya:** (a) tutup cacat 17 dengan **menumpangkan** perbaikan daftar `git add` pada run 4h berikutnya, lalu adjudikasi paruh kedua R-B1; (b) jawab **anomali `buat_konfig`** (SH ≠ SH′) dengan membaca sumber, bukan menduga; (c) **funding sebagai SINYAL** — satu-satunya dimensi bersih yang belum pernah diuji sekali pun, datanya sudah ada di rilis `tier-b-v1`, pra-registrasi lengkap **sesudah** seluruh modul yang disebutnya dibaca, dan gerbang p bulanan wajib (ADR-031 keputusan 5).

---

## 1. Aturan membaca berkas ini

Bagian 3 adalah **fakta**: setiap baris punya bukti berupa commit, run ID, atau kutipan. Bagian 4 adalah **asumsi**: dilarang diperlakukan sebagai fakta. Pemindahan dari 4 ke 3 hanya dengan bukti terlampir.

Aturan yang lahir dari kesalahan nyata, bukan dari teori:

1. **Angka yang lulus gerbang belum tentu benar.** Rasio 1h:4h 4,014 pernah dicatat sebagai uji silang yang lulus, padahal sedang melaporkan bug.
2. **SHA laporan yang tidak berubah bukan tanda pekerjaan masih berjalan.**
3. **Penjelasan yang membuat anomali terasa wajar harus dicurigai lebih keras daripada anomalinya.**
4. **Lihat sebaran mentah sebelum berteori.** Metrik celah funding gagal lima putaran; satu histogram di awal cukup.
5. **Hipotesis yang ditolak tetap ditolak.** Ambang tidak disetel ulang setelah hasil terlihat.
6. (S8) **Percobaan yang informatif ke dua arah lebih berharga daripada percobaan yang dirancang agar berhasil.**
7. (S9) **Saringan yang membuang perdagangan tidak otomatis membuang perdagangan yang buruk.**
8. (S10) **Periksa apakah dugaanmu mungkin secara konstruksi sebelum menjadwalkannya sebagai penelitian.**
9. (S11) **Periksa apakah laporan yang sudah dikomit sudah menjawabnya.**
10. (S11) **Gerbang yang kegagalannya tidak tertulis ke `reports/` adalah titik buta yang menyamar sebagai gerbang.**
11. (S12) **Rerata tidak mengatakan apa pun tentang ekor.** Gerbang nilai ekstrem hanya boleh dibantah dengan nilai ekstrem.
12. (S12) **Batas risiko tidak dilombakan.**
13. (S12) **Peristiwa yang terlalu jarang tidak dapat dipilih oleh pemilih dalam sampel.**
14. (S12) **Ramalan yang salah lebih murah daripada ramalan yang tidak pernah ditulis.**
15. (S12) **Porsi terhadap nilai bersih bukan ukuran konsentrasi.** Pakai jackknife dan penyebut bruto.
16. (S12) **Proksi yang berkorelasi 0,97 dengan hal lain bukan proksi.**
17. (S12) **Gerbang yang memberi jawaban sama pada dua keadaan bertolak belakang tidak memuat informasi.**
18. (S12) **Angka jumlah yang ditulis tangan hanya boleh ada di satu tempat, yaitu pengujian tripwire.**
19. (S13) **Margin setipis satu satuan resolusi bukan margin.** `entri_acak` H-010 lulus p 0,049505 pada 100 permutasi; pada 300 permutasi mekanisme yang sama memberi **0,0631** dan **gagal**. Dikonfirmasi ulang di H-012: **0,06312292358803986**. Diperluas di S19: R-A4 meramal p ≤ 0,001 dan nyatanya 0,001100. Diperluas lagi di S20: **R-D1 meleset hanya tiga menit dua detik dan tetap dicatat MELESET.** Tipis bukan alasan, dan menghaluskannya berarti memindahkan tiang gawang sesudah bola ditendang.
20. (S13) **Ekspektasi yang naik karena penyebutnya menyusut bukan keunggulan yang membesar.**
21. (S13) **Kecurigaan wajib naik, bukan turun, ketika hasilnya menyenangkan.** Dipakai empat kali di S16–S17 atas run yang terasa terlalu cepat; keempatnya **tak berdasar**. Dipakai kelima kali di S18 atas +0,054842R, dan ia **berdasar** (ADR-024). Keenam kali di S19 atas p simbol 0,001100, dan ia **berdasar** (ADR-028). Ketujuh kali di S20 atas p per-perdagangan 0,003322, dan ia **berdasar** (ADR-031). Kedelapan kali di S21 atas +0,029481R, dan ia **berdasar** (ADR-033, cacat kelas keempat belas). **Kesembilan kali di S22 atas agregat +0,027654R yang melewati ambang, dan ia berdasar** (ADR-035, cacat kelas keenam belas). **Dan bentuk terbaliknya juga nyata:** di S22 saya mencurigai run 2 menit 19 detik sebagai kegagalan dan **salah** — kecepatan bukan bukti apa pun, isinya yang dibaca.
22. (S13, ADR-014) **Menuntut kesamaan bit pada agregat pecahan adalah pengujian yang menyala pada perilaku yang benar.** Di dalam satu fungsi murni, kesamaan bit tetap sah.
23. (S13, ADR-014) **Pagar yang memastikan masukan identik tidak memastikan masukan sah.** Diperluas di S17: **kesamaan hasil lintas dua run berbeda dilarang diterima tanpa pemeriksaan.** **Dipakai lagi di S22 pada arah sebaliknya:** SH dan SH′ nominal identik tetapi **tidak** identik (44.614 lawan 44.538), dan ketidaksamaan itu wajib dijelaskan, bukan dibulatkan menjadi derau.
24. (S13, ADR-014) **Satu simbol dapat mendominasi agregat 438 simbol.**
25. (S13, ADR-014) **Himpunan tertahan habis pada saat pertama kali dilihat.**
26. (S13, ADR-014) **Cacat yang membalik tanda hasil tidak boleh diperbaiki di dalam hipotesis yang sama.**
27. (S13, ADR-014) **Eksperimen yang tercemar tidak informatif ke arah mana pun.**
28. (S13, ADR-014) **Saringan yang menolak entri juga menolak saat pemilihan.** Terbukti kuantitatif di H-012: hanya **62** entri ditolak pengaman. **Terbukti kedua kali di S21 dengan mekanisme berbeda:** `maks_umur_bar` ikut menolak **entri** lewat proyeksi carry di `_boleh_masuk`, bukan hanya memotong perdagangan yang sudah terbuka.
29. (S14) **Pra-registrasi wajib diperiksa terhadap apa yang benar-benar dapat dihitung dari laporan.**
30. (S14) **Kriteria utama dihitung dari berkas laporan yang dikomit, bukan dari nilai yang beredar di memori run.**
31. (S15) **Pagar yang menyalin baris dari kode yang dijaganya tidak menjaga apa pun.**
32. (S15) **Aritmetika yang hidup di dalam `main` tidak dapat diuji.**
33. (S15) **Setiap langkah workflow wajib `tee` ke `logs/` dan seluruh `logs/` disalin ke `reports/` dengan `if: always()`.**
34. (S15) **Lingkungan pagar wajib memasang dependensi yang sama dengan `tests.yml`.**
35. (S16) **Muatan tulis yang panjang wajib dibaca ulang utuh sebelum dikirim, dan jumlah pengujian dicacah dari muatan yang benar-benar dikirim, bukan dari rencana.** Sejak aturan ini dipatuhi, dua puluh satu ramalan cacah berturut-turut tepat — lalu **deret itu PUTUS di S21** justru karena aturan ini dilanggar (R-H1, aturan 54).
36. (S16, ADR-016) **Ramalan yang dijamin benar oleh konstruksi bukan ramalan.** **Dibuktikan telanjang di S22:** R-H3 meramal run selesai di bawah 25 menit dan kenyataannya 2 menit 19 detik — ambang sepuluh kali lipat kenyataan, ramalan yang hampir tidak dapat salah, dan karena itu **TEPAT tetapi tidak berguna**.
37. (S17, ADR-017–019) **Angka yang benar untuk satu interval tidak berubah nilai ketika dipakai di interval lain — ia berubah MAKNA, dan diam.** Setiap besaran yang berarti "satu hari" wajib diturunkan lewat `lux.kerangka`, tidak pernah dari literal.
38. (S17) **Dua definisi atas satu dataset selalu dimenangkan oleh yang tidak terlihat.**
39. (S18) **Angka dapat hidup di berkas konfigurasi tanpa pernah masuk ke dalam program.** Cacat kelas kedelapan. **Kode wajib dibandingkan terhadap berkas, bukan hanya dibaca.**
40. (S18, ADR-024) **Putusan yang dihitung dari separuh kriteria pra-registrasi adalah putusan palsu, dan ia paling berbahaya ketika angkanya menyenangkan.** Cacat kelas kesembilan.
41. (S18, ADR-024) **Prosa kesimpulan yang dipatok di dalam kode bukan kesimpulan.** Cacat kelas kesepuluh; **sudah ditutup** di `b0e79220` (767 uji).
42. (S19, ADR-025) **Gerbang yang tidak mungkin lulus tidak menjaga apa pun, dan ia terlihat seperti gerbang yang bekerja.** Cacat kelas kesebelas. **Setiap kegagalan gerbang wajib diperiksa apakah ia mungkin lulus sama sekali; kegagalan yang mustahil dihindari bukan temuan, melainkan cacat.** **Terulang di S22 lewat pintu lain** (cacat 17): sampai daftar `git add` diperbaiki, kegagalan `checksum` pada 4h **wajib dibaca sebagai cacat alat, bukan sebagai temuan**.
43. (S19, ADR-026) **Rencana analisis wajib diperiksa terhadap struktur berkas laporan sebelum dijadwalkan.** ADR-024 menjadwalkan uji atas "4.082 jendela" padahal `per_simbol.jendela` adalah **cacah**. Pemasangan hanya mungkin pada **simbol (437)** dan **bulan (73)**.
44. (S19, ADR-028) **Ambang statistik tanpa satuan penarikan bukan ambang.** Cacat kelas kedua belas. Satuan resmi kini **bulan kalender UTC**. **Dibuktikan telanjang di S20:** satu run yang sama memberi p 0,003322 per perdagangan dan **0,205980** per bulan.
45. (S19, ADR-028) **`p` sah hanya untuk MENJATUHKAN, tidak untuk MENEGAKKAN.** Diperkuat di S21: `lux/analisis/berpasangan.py` menjalankan aturan ini secara struktural — ia **tidak pernah** memancarkan kelulusan, `memenuhi_adr015` dipatok `False`, dan pagar itu dikunci pengujian. **Dijalankan sampai ke putusan di S22:** H-014 hanya punya dua keluaran sah, dan `DITOLAK` adalah salah satunya.
46. (S19) **Ramalan saya tepat ketika menyangkut kode saya sendiri dan meleset ketika menyangkut pasar.** — **dan aturan ini sendiri difalsifikasi di S21:** R-H1 adalah ramalan tentang kode saya sendiri, dan ia meleset karena tidak dihitung dari berkasnya. **Sebelum membekukan ramalan angka, sebutkan asumsi yang menopangnya dan tandai mana yang belum diperiksa.** **S22 memberi bentuk ketiga:** R-G4 adalah ramalan tentang **mekanisme mesin saya sendiri** dan ia **meleset jauh** (umur 32,4% lawan ramalan >80%).
47. (S19–S20, ADR-030) **Alat yang selalu menghasilkan angka tidak menjaga apa pun.** Penggabung yang memaksakan keluaran atas himpunan bulan yang berbeda akan mencetak angka yang tampak waras atas dua himpunan yang bukan pasangan. Karena itu ia **MENOLAK** (kode 4), tidak memotong ke irisan, dan tidak mengisi nol. Berhenti adalah keluaran yang sah.
48. (S20, ADR-030) **Hasil yang menjatuhkan hipotesis wajib berkode keluar 0.** Merah hanya untuk mesin yang rusak, bukan untuk hipotesis yang mati. **Dijalankan di S22:** `gabung_h014` keluar 0 sambil menjatuhkan H-014.
49. (S20, ADR-031) **Besaran tidak boleh diukur terhadap satu undian nol.** Sel AS seed 42 (+0,011806R) ternyata ~0,98 simpangan baku **di bawah** rerata sebaran nol (+0,022916R). Setiap besaran terhadap sel nol wajib dilaporkan juga terhadap **rerata** sebaran nol; besaran terhadap satu seed hanya boleh dikutip bila nomor seed-nya ikut ditulis. **Sejak `6ae83062` aturan ini dijalankan oleh alat.** Bentuk umumnya: **besaran wajib dilaporkan dua kali**, dan bila sebaran nol tidak ada, ketiadaannya wajib dinyatakan — `gabung_h014.adjudikasi` mencetak `catatan_besaran` yang menyatakan bahwa nol permutasi geometri **belum dirancang**. **S22 memperlihatkan aturan ini tidak cukup: dua pelaporan dapat berbeda TANDA** (aturan 55).
50. (S20, ADR-031) **Ramalan yang terbukti salah alasannya dikoreksi sebagai PROSA di sumbernya, dan jejak bunyi aslinya tidak dihapus.** Laporan dan pesan commit yang sudah dikomit **tidak** ditulis ulang. Dijalankan oleh alat sejak `6ae83062`; dipatuhi lagi di S21 atas pesan commit `4af21176` yang memuat R-H1 yang meleset, dan di S22 atas prosa ADR-033 tentang umur 42 lawan 48.
51. (S20) **Sumber dan pagarnya adalah satu commit.** Commit `6ae83062` mengubah `gabung_h013b.py` tanpa membawa pengujiannya, padahal pesan commit itu sendiri meramalkan 819. **Perubahan modul yang membawa perilaku baru wajib satu dorongan dengan pengujiannya, dan ramalan cacah wajib menyebut commit mana yang diramalkan.** Dipatuhi di `4af21176` (dua modul + dua berkas uji, satu dorongan).
52. (S21, ADR-033) **Sel pembanding hanya boleh berbeda pada SATU medan; bila dua, selisihnya bukan pengukuran, dan namanya wajib menyebut kedua medan itu.** Cacat kelas keempat belas: `run_h013.umur_sel` memberi sel bertarget 42 bar dan sel tanpa target 48, jadi "sumbangan geometri keluar +0,029481R" mencampur ada-tidaknya target dengan panjang pegangan. Dijalankan oleh alat: `run_h014.medan_berbeda` mengembalikan **daftar** medan yang berbeda — bukan boolean, supaya laporan dapat menyebut medannya — dan `main` menolak berjalan bila daftar itu bukan tepat `["pakai_target"]`. **Aturan ini TIDAK dibatalkan oleh ADR-035**; yang dibatalkan hanya besar efek yang saya lekatkan pada medan umur (§ ADR-035 §4).
53. (S21, ADR-034) **Ambang hanya boleh dikutip sebagai beku bila dokumen yang membekukannya membekukannya untuk besaran yang sedang diuji; bila tidak, ia ambang BARU dan wajib dinyatakan begitu beserta tanggalnya.** Cacat kelas kelima belas: ADR-015 §4.4 membekukan ≥ 0,020R dan p ≤ 0,05 untuk kaki **sinyal** (SS − AS, p atas permutasi **sinyal**); untuk kaki **geometri** ia tidak pernah membekukan ambang, definisi p, maupun nol. ADR-032 dan ADR-033 keduanya menulis "ambang ADR-015 tidak bergerak" dan karena itu **meminjam ambang yang tidak pernah ada**.
54. (S21) **Ramalan cacah uji wajib dihitung dari berkas yang benar-benar akan didorong, bukan dari rencana pengujian; bila ramalan dan berkas berselisih, yang salah SELALU ramalannya.** Pesan commit `4af21176` menulis "850 (819 + 31), 17 uji baru … 14 …" sementara berkas yang didorong di commit yang sama memuat **20 dan 16**. Hasilnya **855**. Kedua berkas ada di tangan saya pada detik yang sama dengan ramalannya, jadi selisih lima uji itu dapat ditemukan **tanpa menjalankan apa pun**. Ini pengulangan aturan 35 dalam bentuk yang lebih sempit, dan ia dipasang terpisah justru karena aturan 35 tidak cukup mencegahnya.
55. (S22, ADR-035) **Besaran yang tandanya bergantung pada pembobotan bukan besaran.** Cacat kelas keenam belas. Setiap selisih antar sel wajib dilaporkan dalam **empat** bentuk sekaligus — **agregat**, **rerata per unit penarikan**, **berbobot**, dan **median** — dan dokumen pra-registrasi wajib menyatakan **mana yang mengikat sebelum run**. Bila keempatnya tidak sepakat tanda, putusannya **TIDAK DAPAT DINILAI** kecuali dokumen pra-registrasi sudah memilih satu. Untuk H-014 yang mengikat adalah **rerata bulanan**, sebab itulah yang dibaca kode yang dikomit sebelum satu angka pun ada — **kebetulan yang beruntung, bukan rancangan sadar**: ADR-034 tidak pernah menyatakannya.
56. (S22, ADR-035) **Berkas yang dilahirkan sebuah run dan dibutuhkan sebuah gerbang agar dapat lulus wajib ikut dikomit; daftar `git add` adalah bagian dari gerbang, bukan urusan tata usaha.** Cacat kelas ketujuh belas.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa. Seluruh komputasi berjalan di GitHub Actions.

---

## 3. Fakta terverifikasi

### H-014 — DITOLAK (ADR-035, run `30221967019`)

**Bukti:** pemicu `52c64ac576e81883cd516316437edfff1d596ac4` pada 2026-07-26T21:52:25Z; laporan dikomit **`603477ce8b9b55e2a67d9a7a0e7c3c843c2be379`** pada 2026-07-26T21:54:44Z; log blob **`03e0c35c54134d9906515e2df515eb5f1c939b6c`**. Runner melaporkan **`855 passed in 2.98s`** sebelum satu berkas diunduh. Delapan butir pagar pra-terbang lulus **pada percobaan pertama**. 157 MB aset 4h terunduh, 438 simbol dimuat, **437 layak** sesudah lantai membuang USDCUSDT. Sel SSp **56,9 s**, sel SHp **52,6 s**, **seluruh run 2 menit 19 detik** dari pemicu sampai commit laporan.

| Syarat (BARU, dibekukan 2026-07-27, ADR-034) | Nilai | Ambang | Terpenuhi |
|---|---|---|---|
| rerata selisih bulanan SS′ − SH′ | **−0,027715128544164157R** | ≥ 0,020R | **TIDAK** |
| p uji tanda berpasangan bulanan | **0,37596240375962403** | ≤ 0,05 | **TIDAK** |
| pasangan bulan | 73 | ≥ 2 | ya |
| trade sel A / sel B | 59.324 / 44.538 | ≥ 100 | ya |

`p` dihitung dengan m 3759, ulangan 10000, seed 20260727. Bootstrap 95% **[−0,09067851377334449, +0,029103950604927244]** (seed 20260728) — **memuat nol**. `memenuhi_adr015` **false**, sebagaimana dipatok modul. Penggabung keluar berkode **0** (aturan 48).

**Angka kedua sel:**

| Sel | `pakai_target` | `maks_umur_bar` | Trade | Ekspektasi R | Jendela positif | p entri acak | Gerbang gagal |
|---|---|---|---|---|---|---|---|
| SS′ | **True** | 48 | **59.324** | **+0,06725203533326735** | 2229 / 4082 | 0,016611295681063124 | `invarian_risiko`, `checksum`, `funding_ekor` |
| SH′ | **False** | 48 | **44.538** | **+0,03959765698185091** | 1982 / 4082 | 0,21926910299003322 | `entri_acak`, `invarian_risiko`, `checksum`, `funding_ekor` |

Alasan keluar SS′: `stop` 33.748 · `target` 18.667 · `umur` 5.174 · `akhir_data` 1.735. SH′: `stop` 28.013 · `umur` 14.426 · `akhir_data` 2.099. Konsentrasi SS′ 309 untung / 128 rugi, drop-1 **0,06639R** (retensi **0,9872**), drop-22 0,05419R, median simbol +0,06789R, porsi bruto teratas 0,0139 (SANDUSDT), funding maks 0,8285R; SH′ 234 untung / 203 rugi, drop-1 **0,03583R** (retensi **0,9047**), drop-22 0,01225R, median simbol +0,02710R, porsi bruto teratas 0,0431 (VELVETUSDT), funding maks **2,9000R** (juga gagal `porsi_trade_di_atas_pengaman`). Sebaran SS′ std **1,37827R**, galat baku 0,005659R (+3,05 SE); SH′ std **2,20818R**, galat baku 0,010463R (−0,99 SE) — tanpa target, sebarannya **enam puluh persen lebih lebar**. Parameter terpilih SS′ {55:836, 20:1711, 100:1535}, SH′ {55:1073, 20:1995, 100:1014}. Sidik SS′ `197c10e3f0d2`, SH′ `5721a88e59eb`. 73 bulan pada kedua sel.

### CACAT KELAS KEENAM BELAS — tanda besaran bergantung pada pembobotan (ADR-035 §2, aturan 55)

Satu himpunan **73 bulan yang sama** memberi:

| Cara membobot | Nilai | Tanda |
|---|---|---|
| selisih **agregat** | **+0,027654378351416438R** | **POSITIF** |
| **rerata** selisih bulanan | **−0,027715128544164157R** | **NEGATIF** |
| rerata **berbobot trade** | −0,012499029724652699R | NEGATIF |
| **median** selisih bulanan | +0,03495217650445759R | POSITIF |
| fraksi bulan positif | 0,5616438356164384 | — |

Dua angka pertama **hampir sama besar dan berlawanan tanda**. Bukan derau pembulatan dan bukan dua uji berbeda: satu besaran yang tandanya **ditentukan oleh cara membobot bulan**. Agregat membobot menurut jumlah perdagangan sehingga didominasi bulan bervolume besar; rerata bulanan memberi setiap bulan bobot sama sehingga menghukum ekor bulan buruk. Median positif dan fraksi 0,5616 memberi bentuknya: **mayoritas bulan condong ke sel bertarget, tetapi beberapa bulan condong ke sel tanpa target dengan besar yang jauh lebih ekstrem.**

**Bila pembobotan bebas dipilih, H-014 melewati ambang besaran hari ini dengan agregat +0,0277R.** Yang mencegahnya bukan kehati-hatian saya melainkan bahwa `gabung_h014.adjudikasi` membaca `rerata_selisih`, dan kode itu dikomit **sebelum** satu angka pun ada. **p 0,376 menjatuhkan hipotesis pada pembobotan mana pun**, jadi putusannya tidak bergantung pada keberuntungan itu — tetapi ambang besarannya bergantung.

### CACAT KELAS KETUJUH BELAS — gerbang yang saya sendiri buat mustahil lulus (ADR-035 §3, aturan 56)

Log run mencetak, verbatim:

> `manifest aset reports/manifest_aset_4h.json (12 berkas interval 4h)`
> `checksum: tidak dapat dinilai: manifest baru ditulis pada run ini`

Itu **separuh pertama R-B1 TEPAT**. Tetapi `reports/manifest_aset_4h.json` **tidak ada di `main`** — diperiksa langsung, jawabannya "the file does not exist in the repository". Sebabnya daftar `git add` di `h014.yml` yang saya tulis sendiri: ia menambahkan `reports/backtest_h014_*`, `reports/h014_run.json`, `reports/h014_berpasangan.*`, `reports/h014_log.md`, dan `hipotesis/H-014-*.json` — **dan tidak manifesnya**.

Akibatnya setiap run 4h berikutnya menulis manifest baru lagi dan melapor "tidak dapat dinilai" lagi, **selamanya**. Gerbang `checksum` pada 4h **mustahil lulus** — bentuk kedua cacat kelas kesebelas, masuk lewat pintu lain, dan kali ini **saya yang membuatnya**. ADR-025 memperbaiki *nama* berkasnya; saya lupa berkas itu harus **bertahan**.

**Keputusan (ADR-035 §3):** manifes 4h **tidak** didorong sebagai commit tersendiri. Menyentuh `h014.yml` memicu ulang seluruh run yang baru saja melahirkan putusan sah — memboroskan komputasi untuk nol pengetahuan. Perbaikan daftar `git add` **menumpang run 4h berikutnya**. Sampai itu terjadi, **kegagalan `checksum` pada 4h wajib dibaca sebagai cacat alat, bukan sebagai temuan** (aturan 42).

### KLAIM ADR-033 DIBATALKAN SEBAGIAN — umur 42 lawan 48 bukan sebab utama (ADR-035 §4)

ADR-033 menulis bahwa umur 42 lawan 48 adalah "sebab terukur pertama dari 60.018 lawan 44.614 perdagangan". Sekarang angkanya ada:

| Sel | Umur | Trade |
|---|---|---|
| SS (H-013) | 42 | 60.018 |
| **SS′ (H-014)** | **48** | **59.324** |
| SH (H-013) | 48 | 44.614 |
| **SH′ (H-014)** | **48** | **44.538** |

Efek menaikkan umur 42 → 48 pada sel bertarget: **−694 perdagangan, −1,2%**. Jarak antar sel dengan umur **disetarakan**: 59.324 lawan 44.538 = **+33,2%**. Jadi jarak perdagangan itu **hampir seluruhnya `pakai_target`**, bukan ketidaksamaan umur. Mekanismenya sekarang terukur: target menutup **18.667** posisi di SS′, membebaskan modal lebih awal, sehingga lebih banyak entri berikutnya lolos proyeksi carry.

**Aturan 52 TIDAK dibatalkan** dan **+0,029481R tetap haram dikutip** sebagai sumbangan geometri. Yang dibatalkan adalah **besar** yang saya lekatkan pada medan umur. Saya menyebut sesuatu "sebab terukur" sebelum mengukurnya; yang saya punya waktu itu hanyalah mekanisme yang masuk akal.

### ANOMALI SH ≠ SH′ — MEMERLUKAN VERIFIKASI (ADR-035 §5)

Konfigurasi **nominal sama**: sinyal Donchian sungguhan, `pakai_target=False`, `maks_umur_bar=48`, `imbalan_R=2.0`, lantai 0,004, pengaman 0,5R, `stop_hormati_celah` menyala, jendela {1080,540,42}, pemanasan 200, semesta 437 simbol yang sama.

| | Trade | Ekspektasi R | Lookback terpilih (20 / 55 / 100) |
|---|---|---|---|
| SH | 44.614 | +0,037166633609032385 | 1987 / 1069 / 1026 |
| SH′ | **44.538** | **+0,03959765698185091** | **1995 / 1073 / 1014** |

Selisih 76 perdagangan (0,17%) dan **+0,00243R**. Kecil, **bukan nol**, dan menurut aturan 23 wajib diperiksa. Satu-satunya perbedaan jalur kode yang diketahui: H-013 memakai `buat_konfig=buat_konfig_sel(sel)`, H-014 memakai `buat_konfig=None` dan memasang geometri di Konfig dasar. **Jadi jalur `buat_konfig` bukan no-op dan ia menyentuh pemilihan parameter dalam sampel** — buktinya cacah lookback terpilih bergeser. **Ini memerlukan verifikasi.** Sampai sebabnya diketahui, **SS′ − SH′ tidak boleh dibandingkan dengan SS − SH sebagai "angka yang sama sesudah diperbaiki"**.

**Yang sudah dibaca di S22 (fakta, bukan dugaan):** `lux/backtest/walk_forward.py` (blob `5a686e229c0292bdea2219278a318b96fa675637`) memuat `konfig_untuk(params) = buat_konfig(params, k) if buat_konfig is not None else k`, dan konfig itu dipakai **di dalam lingkaran pemilihan kandidat** (`_skor_baku(jalankan(latih, s, konfig_untuk(params), …))`) sekaligus untuk jendela uji. Docstringnya menjanjikan: bila `buat_konfig` tidak diberikan, "jalur eksekusinya sama persis seperti sebelum ADR-007". Jadi bila `buat_konfig_sel` mengembalikan Konfig yang **tidak** identik medan demi medan dengan Konfig dasar H-014, skor dalam sampel bergeser dan lookback terpilih bergeser — **itu hipotesis kerja, belum diverifikasi**; yang belum dibaca adalah `run_h013.buat_konfig_sel` dan `run_h014.konfig_sel_h014` berdampingan.

### CACAT KELAS KEEMPAT BELAS — selisih yang mencampur dua medan (ADR-033)

`run_h013.umur_sel` mengembalikan `UMUR_SEL_STOP = 42` untuk sel bertarget dan `H_BAR = 48` untuk sel tanpa target. Jadi **SS − SH mencampur dua medan**: ada-tidaknya target **dan** panjang pegangan. Dan `maks_umur_bar` bukan medan pasif — `engine._boleh_masuk` memakainya untuk proyeksi carry (`umur_ms = k.maks_umur_bar * interval_ms`), sehingga **42 dan 48 menolak entri yang berbeda**.

**Putusan H-013 tidak berubah** — ia mati pada p bulanan 0,205980 kaki **sinyal**, dan SS maupun AS keduanya berumur 42. Yang berubah adalah makna satu angka: **`+0,029481R` tidak mengukur apa yang namanya sebut**, dan ia haram dipakai sebagai pembanding H-014 maupun sebagai "versi sebelum perbaikan".

### CACAT KELAS KELIMA BELAS — ambang yang dipinjam dari pra-registrasi yang tidak memuatnya (ADR-034)

ADR-032 dan ADR-033 keduanya menulis bahwa "ambang ADR-015 tidak bergerak: ≥ 0,020R, p ≤ 0,05, ≥ 300 ulangan, ≥ 100 trade". Itu **tidak benar untuk kaki geometri**. ADR-015 §4.4 mendefinisikan besaran sebagai **SS − AS** dan p sebagai **permutasi sinyal**; untuk selisih geometri ia mempersyaratkan hanya bahwa besarannya **dilaporkan**. Tidak ada ambang, tidak ada definisi p, tidak ada nol. **Aturan 53** dipasang, dan ambang H-014 dinyatakan **baru** di tiga tempat: kode (`CATATAN_AMBANG`), laporan md, dan pagar pra-terbang butir 4.

### H-014 TIDAK PERNAH DAPAT LULUS, DAN ITU DIPRA-REGISTRASI (ADR-034 §2)

`lux/analisis/berpasangan.py` menyatakan sendiri, verbatim: "p yang dihasilkan modul ini mengukur ketidakpastian **penarikan simbol atau bulan**. Ia **bukan** sebaran permutasi sinyal… Angka ini sah dipakai untuk **menjatuhkan** klaim SS−AS, dan **tidak** sah dipakai untuk menegakkannya. Karena itu modul ini tidak pernah memancarkan kunci `lulus` bernilai benar — secara sengaja, dan hal itu dikunci oleh test." Maka `gabung_h014.PUTUSAN_MUNGKIN = ("DITOLAK", "TIDAK DAPAT DINILAI")`, tidak ada cabang `LULUS` di seluruh jalur H-014, dan sebuah pengujian menuntut bahwa besaran besar **dan** p kecil sekalipun menghasilkan `TIDAK DAPAT DINILAI`. Pagar pra-terbang butir 3 **menjalankan** adjudikasi itu atas masukan sintetis.

**Kode H-014:** commit **`4af2117639c15ace7ba4a442ce2841091a1e25fb`** — `lux/backtest/run_h014.py`, `lux/backtest/gabung_h014.py`, `tests/test_run_h014.py` (20 uji), `tests/test_gabung_h014.py` (16 uji), **satu dorongan** (aturan 51). `reports/tests.md` blob **`94e5096e2f989edc13d3f1a95daa84b6b512331e`**, run **`30221837845`**, keluar **0**, **`855 passed in 3.06s`**. **Workflow** `.github/workflows/h014.yml` commit **`52c64ac576e81883cd516316437edfff1d596ac4`**: satu pekerjaan, `timeout-minutes: 180`, delapan butir pagar pra-terbang, kedua sel berurutan, penggabung di pekerjaan yang sama, kedua laporan sel dikomit — **tetapi daftar `git add`-nya cacat** (cacat 17).

**Empat bahaya yang ditemukan dengan MEMBACA SUMBER, bukan dengan menunggu run gagal:**

1. `runner.jalankan_spek` memanggil `praregistrasi.simpan(spek.h, f"hipotesis/{spek.h.id}.json")`. Memakai `hipotesis_h013` akan **menimpa pra-registrasi H-013 yang sudah dikomit**. H-014 punya hipotesis sendiri, id **per sel** (`H-014-SSp`, `H-014-SHp`).
2. `jalankan_spek` menulis `backtest_<nama>.json` dengan nama **sama** setiap panggilan; `run_h014.periksa_nama` menuntut nama H-014 berbeda dari keempat `NAMA_LAPORAN` H-013 dan dari `run_h013b.NAMA_SPEK`.
3. `Spek.buat_konfig` sengaja `None`: satu-satunya pintu yang memungkinkan `pakai_target` atau `maks_umur_bar` **dilombakan**, dan itu dilarang ADR-033 §7. Laporan mencetak `konfig_per_kandidat: false`. **Catatan S22:** pintu yang ditutup itu ternyata juga sumber anomali SH ≠ SH′ (§ di atas).
4. Berkas md tiap sel **tetap** mencetak `LULUS` atau `DITOLAK` milik pra-registrasi **per sel** dari runner — bukan putusan H-014. `Kriteria` per sel dibiarkan pada nilai bawaan (0,05R, 100 trade, p 0,05, rasio 0,5) dan sebuah pengujian menuntutnya.

### ADR-032 DIBATALKAN SEBAGIAN — klaim saya sendiri difalsifikasi dalam ~20 menit (ADR-033 §2)

ADR-032 (`7269af2e`) mempra-registrasi H-014 dengan nol "permutasi jarak stop" dan lima ramalan R-F1…R-F5. ADR-033 (`b9dc917d`) membatalkan §2 keberatan B dan §3–§6. Bunyi asli yang dibatalkan: "**Keberatan B — AH terlalu tinggi untuk sel acak.** … tanpa stop, penyebut R adalah jarak nosional yang tak pernah diuji pasar… Jadi SS − SH sebagian adalah selisih **definisi penyebut**."

**SALAH.** `engine.jalankan` mengevaluasi `kena_stop` **tanpa syarat**; `pakai_target=False` hanya mematikan target. `jarak = k.atr_pengali_stop * atr_t` di kedua sel dan `Perdagangan.R = laba / (jarak_stop * ukuran)`, jadi penyebut R **dibangun identik**. Akibatnya **`AH = +0,05817042814276683R` kembali TIDAK TERJELASKAN** — **ini memerlukan verifikasi.** H-014 tidak menyentuhnya.

**R-F1…R-F5 DIBATALKAN, bukan diadili.** Nol ADR-032 §3 **tidak dapat dijalankan**: `jarak_stop` dihitung di dalam `engine.jalankan` tanpa jalur masukan per perdagangan.

### JALUR B — PUTUSAN LAHIR, H-013 DITOLAK (ADR-031)

Run **`30217516013`**, pemicu `97b36c19` pada 2026-07-26T19:45:13Z. Sepuluh pecahan mengomit antara 20:13:43Z dan 20:28:15Z; laporan p dikomit `1d746879` pada 20:28:37Z. **Sepuluh dari sepuluh pecahan hadir, seed utuh 300 pada [0,300), 73 bulan pada sel SS, kode keluar penggabung 0.**

| Syarat ADR-015 §4.4 | Nilai | Ambang | Terpenuhi |
|---|---|---|---|
| besaran SS − AS | **+0,054842R** | 0,020R | ya |
| **p satuan bulan** | **0,205980** | 0,05 | **TIDAK** |
| ulangan | 300 | 300 | ya |
| trade terkecil antar sel | 54.812 | 100 | ya |

**Sebaran nol atas 300 seed:** rerata **+0,022916R** · simpangan baku **+0,011377R** · rentang **−0,004632R … +0,057394R** · ekspektasi sel SS yang dibandingkan **+0,066648R**.

**p satuan perdagangan pada run yang sama: 0,003322** — berlabel `taksiran_bawah` dan **haram** dipakai menegakkan klaim (aturan 45).

**Temuan terpenting bukan putusannya, melainkan satuannya.** Satu run, dua angka p berlawanan arah, dan yang membuat satuan bulan sah bukan besarnya melainkan bahwa ia dibekukan ADR-028 **sebelum** kedua angka ini ada. **Bila satuan boleh dipilih sesudah hasil terlihat, H-013 lulus hari ini dengan p 0,0033.** Jalur A membenarkannya dengan mesin berbeda: p bulanan berpasangan **0,365363**, bootstrap memuat nol.

### CACAT KELAS KETIGA BELAS — besaran diukur terhadap satu undian nol (ADR-031, SUDAH DIPASANG KE ALAT)

Sumbangan sinyal +0,054842R dihitung dengan AS = **satu** sel, seed 42, +0,011806R, yang terletak ~**0,98 simpangan baku di bawah** rerata nol.

- Terhadap seed 42: **+0,054842R**
- Terhadap rerata sebaran nol: **+0,043732R** — **dua puluh persen lebih kecil**

Putusan tidak berubah; angka yang dikutip sebelumnya lebih bagus daripada yang pantas. Dibayar di sumber lewat `6ae83062` (`BUNYI_ASLI_R_D3`, `KOREKSI_R_D3`, `besaran_terhadap_rerata_nol_R`) dan `5bd73fbf` (16 → **24** pengujian). `reports/h013b_p.md` yang sudah dikomit **tetap** memuat prosa R-D3 yang salah dan **tidak** ditulis ulang (aturan 50).

### Mesin Jalur B dan H-014 — modul yang berdiri hijau sendiri lebih dulu

| Modul | Commit | Uji | Isi |
|---|---|---|---|
| `lux/analisis/sebaran_nol.py` | `05df8b78` | **779** | `p_ekor_atas` (`p=(1+cacah)/(1+n)`), `p_per_perdagangan` (`mengikat: False`), `p_bulanan` (`mengikat: True`) |
| `lux/backtest/run_h013b.py` | `4f09c8d5` | **795** | `NAMA_SPEK="h013b_as_seed"`, 30 seed per pecahan, keluar 3 bila R-D5 meleset |
| `lux/backtest/gabung_h013b.py` | `0859e8dd` → `6ae83062` → `5bd73fbf` | **811** → **819** | dua syarat, `BUNYI_ASLI_R_D3`, aturan 49 di alat |
| **`lux/backtest/run_h014.py` + `gabung_h014.py`** | **`4af21176`** | **855** | dua sel satu medan, `medan_berbeda`, `periksa_nama`, `PUTUSAN_MUNGKIN` tanpa `LULUS` |

### H-013 — RUN SEL, ANGKANYA (run `30214203863`)

Mesin commit **`93a4309b`**, laporan dikomit **`e060749c`** pada 2026-07-26T18:21:35Z. 438 simbol dimuat, **437 layak** sesudah lantai membuang **USDCUSDT** (median `stop_frac` 3,799992e−04), 4.082 jendela per sel.

| Sel | Sinyal | Target | Umur (bar 4h) | Trade | Ekspektasi R | p entri acak | Gerbang gagal |
|---|---|---|---|---|---|---|---|
| SS | sungguhan | ya | **42** | 60.018 | **+0,066648** | 0,0166 | `invarian_risiko`, `checksum` |
| SH | sungguhan | tidak | **48** | 44.614 | +0,037167 | 0,2259 | `entri_acak`, `invarian_risiko`, `checksum`, `funding_ekor` |
| AS | permutasi seed 42 | ya | **42** | 55.927 | +0,011806 | 0,3588 | `entri_acak`, `lookahead`, `invarian_risiko`, `checksum`, `konsentrasi` |
| AH | permutasi | tidak | **48** | 45.378 | +0,058170 | 0,1993 | `entri_acak`, `lookahead`, `invarian_risiko`, `checksum`, `funding_ekor` |

Sidik: SS `06c3805bdd7ad4de` · SH `af1145aab7f13567` · AS `5ee4b130f9ed228d` · AH `4ada4587abede644`.

Tiga selisih: **sinyal (SS − AS) +0,054842R terhadap seed 42, +0,043732R terhadap rerata nol** · **"geometri" (SS − SH) +0,029481R — MENCAMPUR DUA MEDAN, cacat 14** · interaksi +0,075846R · **SH − AH = −0,021004R**.

`parameter_beku`: `imbalan_R` 2,0 · `h_bar` 48 · `umur_sel_stop` 42 · `lookback` [20,55,100] · `seed_permutasi` 42 · `ulangan` 300 · `min_median_stop_frac` 0,004 · `maks_biaya_masuk_R` 0,5 · `stop_hormati_celah` true · `jendela_bar` {1080,540,42} · `pemanasan` 200 · `bar_dibutuhkan` 1862.

**Medan `lulus` di `backtest_h013_kontribusi.json` tetap TIDAK SAH.** Putusan H-013 yang sah **hanya** yang lahir dari `reports/h013b_p.json`.

### JALUR A — SELESAI, MENJATUHKAN KEBERARTIAN PADA SATUAN BULAN

Modul `lux/analisis/berpasangan.py` commit **`48cf1b9f`** (blob `a9fba624`), RAMALAN 749 TEPAT. Hasil `e3309954`; `--ambang 0.020 --ulangan 10000 --seed 20260727`.

**SS lawan AS:**

| Besaran | simbol (437) | bulan (73) |
|---|---|---|
| rerata selisih | +0,035625R | +0,023327R |
| rerata berbobot trade | +0,053518R | +0,047950R |
| selisih agregat | +0,054842R | +0,054842R |
| median selisih | +0,050280R | +0,036628R |
| fraksi positif | 0,6293 | **0,5342** |
| p uji tanda | **0,001100** | **0,365363** |
| bootstrap 95% | [+0,015182, +0,055725]R | **[−0,027040, +0,073620]R — MEMUAT NOL** |

**SH lawan AH:** simbol — rerata −0,010358R, berbobot −0,023331R, agregat −0,021004R, fraksi 0,4760, p 0,777622. Bulan — rerata −0,029960R, berbobot −0,028521R, median −0,072371R, fraksi 0,4110, **p 0,280372**, bootstrap [−0,084772, +0,024341]R. **Anomali SH < AH turun pangkat menjadi derau.**

Adjudikasi R-A1…R-A6: empat tepat, **R-A4 MELESET** (0,001100 lawan ≤ 0,001), **R-A5 MELESET JAUH** (0,365363 lawan ≤ 0,01).

### CACAT KELAS KESEBELAS — gerbang yang tidak mungkin lulus (ADR-025, DITUTUP untuk 1h, TERBUKA LAGI untuk 4h lewat cacat 17)

`reports/manifest_aset.json` (blob `2e95a0ff`) memuat **dua belas kunci, seluruhnya `ohlcv_1h_*`**, sementara H-013 membaca dua belas berkas `ohlcv_4h_*` — irisan **nol**. Perbaikan dua langkah: **`fb128c93`** (modul daun `manifest.py`, **758** TEPAT) dan **`43cd4eed`** (`muat_konteks` memakai `jalur_manifest`, **761** TEPAT). Jalur 1h **bit-identik**. **Terverifikasi ulang di S22 dengan membaca `runner.py` (blob `4ce34a3c`):** bila manifest belum ada, `muat_konteks` menulisnya lalu memancarkan `Gerbang("checksum", False, …, "tidak dapat dinilai: manifest baru ditulis pada run ini")` — jadi gerbang itu hanya dapat lulus bila berkasnya **bertahan** di `main` (cacat 17).

**Utang terbuka:** langkah 2 menulis ulang `runner.py` seutuhnya; pembanding blob **`fc79e070bbf6ad6f48898958a4942bac876949ca`**. Utang sejenis `run_h013.py`: blob **`418f6084`**.

### CACAT KELAS KEDUA BELAS — ambang tanpa satuan penarikan (ADR-028)

**ADR-028 (`48c83d59`) mematok:** satuan resmi **bulan kalender UTC (73 unit)** menurut waktu **masuk**; **simbol (437)** sebagai pembanding, bukan pengganti; **per perdagangan DILARANG sebagai bukti keberartian**. Tidak satu angka ambang ADR-015 pun digeser.

**Sebelas penolakan H-001b–H-012 tetap berdiri dan tetap haram dihitung ulang.** Yang **tidak** dilindungi adalah **H-010**: setiap p yang pernah dikutip untuknya lebih lemah daripada tertulis.

### AUDIT LIMA BELAS WORKFLOW — SELESAI

| Workflow | `git pull --rebase --autostash` | Catatan |
|---|---|---|
| `tests.yml` | **ada** | filter `lux/**`, `tests/**`, dirinya sendiri |
| `funding.yml` · `funding_check.yml` | **ada** | masih memakai `reports/universe_layak.json` (447 pra-lantai) |
| `universe.yml` | **ada** | gerbang ditegakkan **sesudah** commit, disengaja |
| `doctor.yml` | **ada** | `set +e` disengaja |
| `backfill_daily.yml` | **ada** | **satu-satunya berjadwal**: `cron: '0 2 * * 1'`, `--clobber` |
| `notion_asap.yml` | **TIDAK ADA** | `git push` polos, `git commit … \|\| echo` menelan kegagalan |
| `h013b.yml` | **ada, di dalam lingkaran ulang** | sepuluh penulis satu cabang |
| **`h014.yml`** | **ada, di dalam lingkaran ulang delapan kali** | satu pekerjaan; kedua laporan sel dikomit; **daftar `git add` cacat — cacat 17** |

Dengan `validate.yml`, `potong_ekor.yml`, `backtest.yml`, `ingest_tier_b.yml`, `geometri.yml`, dan `berpasangan.yml`, maka **empat belas dari lima belas** memakai pola itu.

**Temuan yang tidak dicari:** `backfill_daily.yml` berjalan setiap Senin 02:00 UTC tanpa dipicu manusia dan mengancam manifest keutuhan (ADR-025 R4).

### TEMUAN S17 — lima cacat buta-interval, semuanya ditutup

| # | Cacat | Ditutup di |
|---|---|---|
| 1 | `validate_run` menulis `universe_layak.json` tanpa interval | `02933b85` |
| 2 | `muat_ambang` membaca `min_bar_1h` untuk interval apa pun | `fe7fd30e` |
| 3 | `MIN_PANJANG`/`MIN_BAR` buta interval di `potong_ekor` | `6aacef40` |
| 4 | keluaran `potong_ekor` 4h menimpa masukan 1h | `6aacef40` + `5296162d` |
| 5 | **`muat_ohlcv` memangkas ekor dengan ambang 1h** | `409343f3` |

Cacat **keenam** ADR-020; **ketujuh** ADR-023; **kedelapan** aturan 39; **kesembilan/kesepuluh** ADR-024; **kesebelas** ADR-025; **kedua belas** ADR-028; **ketiga belas** ADR-031; **keempat belas** ADR-033; **kelima belas** ADR-034; **keenam belas dan ketujuh belas** ADR-035.

### CACAT KELAS KEDELAPAN — angka di config yang tidak pernah dibaca program

Run H-013 **pertama** (`30213913942`, `135b159c`) mati di pagar butir 3. Sebabnya: **`muat_konfig_h002` memetakan delapan kunci saja**; `maks_biaya_masuk_R` dan `stop_hormati_celah` tidak ada di sana meski tertulis di `config/lux.yaml` sebagai `0.5` dan `true`. Perbaikan `ab3e9792` (**739**) memasangnya di `dasar_riset`; satu uji **mengunci cacatnya sebagai perilaku**. Pagar diperkuat `93a4309b`. Pagar `h014.yml` butir 6 mengunci lagi bentuk yang sama.

### UTANG TEKNIS — kunci config yang tidak pernah dibaca

1. `universe.maks_rasio_bar_datar: 0.30` — **tidak dibaca gerbang backtest**.
2. `risiko.maks_biaya_masuk_R: 0.5` — tidak dipetakan `muat_konfig_h002`.
3. `risiko.stop_hormati_celah: true` — sama.

Keberatan ADR-018 yang masih berdiri: `MAKS_RASIO_DATAR = 0.10` dipakai untuk kedua interval, jadi gerbang itu **lebih longgar** di 4h.

### KERANGKA 4h — semesta berdiri sendiri, dan kesamaannya diperiksa

**Validasi 4h** run `30211176709` (ADR-017): 3.636.733 baris / 790 simbol; layak 447; celah 112; duplikat 0. **Pemangkasan ekor 4h** run `30211673239` (ADR-018): ambang 6 bar, 447 → **438 layak**, nol penolakan `maks_rasio`.

**Aturan 23 dijalankan dua kali:** 438 simbol 4h dibandingkan **simbol per simbol** dengan 438 simbol 1h — **identik**. `universe_layak_v2_4h.json` memuat `"interval":"4h"`, `"min_bar":2190`, `"min_panjang":6`.

**ASET 4h TERVERIFIKASI ADA** di rilis `tier-b-v1` (id `359778114`): 12 berkas, 157.628.619 B. Run H-014 mengunduh 16 berkas / 157M.

**Kelayakan 1h lawan 4h identik (447/74/112) dan itu BELUM dijelaskan. Ini memerlukan verifikasi.**

### Papan ramalan jumlah pengujian

| Commit | Ramalan | Nyata | Putusan |
|---|---|---|---|
| `864da2ec` | 635 | **638** | SALAH |
| `3880408f` · `b4b1963c` | 642 · 643 | sama | TEPAT |
| `eae7eb3a` | 662 | **665** | SALAH |
| `955b419a` | 673 | 673 | TEPAT |
| `fb710521` | 673 tetap | — | **TIDAK DAPAT DIADILI** |
| `02933b85` · `fe7fd30e` | 679 · 683 | sama | TEPAT |
| `6aacef40` | **693** | **694** | **SALAH** |
| `47ef9a90` … `409343f3` | 702 … 714 | sama | TEPAT |
| ADR-020 langkah 1–3 | 716 · 721 · 734 | sama | TEPAT |
| `8bda1473` · `ab3e9792` | 737 · 739 | sama | TEPAT |
| `48cf1b9f` · `fb128c93` · `43cd4eed` | 749 · 758 · 761 | sama | TEPAT |
| `b0e79220` | **767** | 767 | TEPAT |
| `05df8b78` · `4f09c8d5` · `0859e8dd` | 779 · 795 · 811 | sama | TEPAT |
| `6ae83062` (R-E1b) | **811** | 811 (run `30219837959`) | TEPAT |
| `5bd73fbf` (R-E1a) | **819** | 819 (run `30219885271`) | TEPAT |
| **`4af21176` (R-H1)** | **850** | **855 passed in 3,06s** (run `30221837845`) | **MELESET** |

Jejak: 444 → … → 811 → 819 → **855**. **Deret dua puluh satu ramalan cacah tepat berturut-turut PUTUS pada `4af21176`**, penyebabnya aritmetika saya: rencana 17+14 lawan berkas 20+16 (aturan 54). Blob `reports/tests.md`: `d768d55f` (811) → `0e480f90` (819) → **`94e5096e2f989edc13d3f1a95daa84b6b512331e`** (855). Berkas markdown **tidak** memicu `tests.yml`, jadi 855 tetap berlaku sesudah commit dokumentasi. **Run `30221967019` mengulang `855 passed in 2.98s` di sisi runner sebelum unduhan** — cacah yang sama, mesin yang berbeda.

**Papan ramalan perilaku sistem:** S18 nol dari enam tepat; S19 empat dari enam; S20 tiga dari lima; **S21–S22 gabungan: R-H1 MELESET, R-G1 SEPARUH, R-G2a TEPAT, R-G2b TEPAT, R-G3 TEPAT, R-G4 MELESET JAUH, R-H2 TEPAT, R-H3 TEPAT tetapi tidak berguna, R-B1 separuh pertama TEPAT** — lima tepat, satu separuh, dua meleset, satu tak berguna. Gabungan sebelas ramalan angka H-013: sembilan meleset (aturan 46).

### Adjudikasi ramalan S22 (ADR-035 §6)

| Kode | Isi | Nyata | Putusan |
|---|---|---|---|
| **R-G1** | SS′ − SH′ **< +0,029481R**; taksiran 0,010–0,025R | agregat **+0,027654R** | **SEPARUH**: arah TEPAT, taksiran **MELESET** (di atas 0,025) |
| **R-G2a** | p bulanan **> 0,05** → DITOLAK; taksiran 0,15–0,60 | **0,375962** | **TEPAT**, di dalam taksiran |
| **R-G2b** | bootstrap 95% memuat nol | **[−0,090679, +0,029104]R** | **TEPAT** |
| **R-G3** | trade SS′ melampaui SH′ **≥ 20%** | **+33,2%** | **TEPAT** |
| **R-G4** | **> 80%** trade SH′ keluar lewat `umur` | **32,4%** (14.426 / 44.538); `stop` **62,9%** | **MELESET JAUH** |
| **R-H2** | pagar pra-terbang lulus percobaan pertama | delapan butir OK | **TEPAT** |
| **R-H3** | run selesai < 25 menit | **2 menit 19 detik** | **TEPAT tetapi TIDAK BERGUNA** (aturan 36) |
| **R-B1** separuh pertama | run 4h pertama melapor `checksum` "tidak dapat dinilai: manifest baru ditulis pada run ini" | **kalimat itu persis** | **TEPAT** |
| **R-B1** separuh kedua | run 4h **kedua** lulus `checksum` | — | **MUSTAHIL sampai cacat 17 ditutup** |

**R-G4 salah pada mekanismenya, bukan hanya angkanya.** Menghapus target tidak mengubah posisi menjadi "pegang sampai waktu habis"; ia mengubahnya menjadi "pegang sampai stop kena, dan stop biasanya kena lebih dulu". Itu sekaligus menjelaskan std yang melebar (2,20818R lawan 1,37827R) dan retensi drop-1 yang jatuh (0,9047 lawan 0,9872): tanpa target, hasilnya bergantung pada lebih sedikit kejadian besar.

### Ramalan beku yang MASIH belum teradili

| Kode | Isi | Sumber |
|---|---|---|
| R-B1 separuh kedua | run 4h **kedua** lulus `checksum` | ADR-027 §7 — **mustahil sampai cacat 17 ditutup** |
| R-B4 | pemasangan bulanan **berbobot trade** tetap p > 0,05 | ADR-027 §7 |
| ADR-016 ramalan 5 | ekspektasi R dengan `stop_hormati_celah` menyala lebih rendah | ADR-016 |

**DIBATALKAN, tidak akan pernah punya angka:** **R-F1…R-F5** (ADR-032) — nol permutasi jarak stop tidak dapat dijalankan tanpa bedah `engine.jalankan`.

### H-012 — DITOLAK (ADR-014 §8)

Run **`30200123505`**, commit **`56a325d2`**, sidik **`75f9c7ccd65ec30f`**, 437 dari 438 simbol, 4.081 jendela.

| Sisi batas | Bulan | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|
| **Tahan (sejak `2026-01`)** | 7 | **22.117** | +922,56 | **+0,041713** |
| Sebelum `2026-01` | 66 | 113.564 | +7.168,96 | +0,063127 |
| Seluruh riwayat | 73 | 135.681 | +8.091,52 | +0,059636 |

**0,041713R < 0,05R → GAGAL.** `entri_acak` GAGAL p 0,06312292358803986 · `invarian_risiko` GAGAL −21,3131R · `funding_ekor` GAGAL 0,6601. Entri ditolak pengaman **62**.

### Papan skor hipotesis — EMPAT BELAS DINILAI, EMPAT BELAS DITOLAK

| ID | Mekanisme | Ekspektasi R | Gerbang gagal | Putusan |
|---|---|---|---|---|
| H-001b | Donchian polos | 0,03086 | `invarian_risiko` −2,5853 | DITOLAK |
| H-002 | Donchian + saringan carry | 0,03159 | tidak ada | DITOLAK |
| H-003 | pembalikan skor-z | −0,24782 | `entri_acak`, `invarian_risiko` | DITOLAK |
| H-004 | Donchian + ADX ≥ 30 | −0,01818 | tidak ada | DITOLAK |
| H-005 | entri retest | −0,03571 | `invarian_risiko` | DITOLAK |
| H-006 | sapuan likuiditas | −0,13449 | `entri_acak`, `invarian_risiko` | DITOLAK |
| H-007 | imbalan dipilih walk-forward | 0,04044 | `invarian_risiko` | DITOLAK |
| H-008 | pengaman carry dilombakan | 0,04126 | `invarian_risiko` | DITOLAK |
| H-009 | pengaman carry dipatok 0,25 | 0,041359 | tidak ada | DITOLAK oleh ambang 0,05R |
| H-010 | grid imbalan {2,4,6,8}, 40 simbol | 0,053028 | tidak ada dari sebelas | LULUS, empat keberatan; **p 0,0631 pada 300 permutasi**; seluruh p-nya per perdagangan |
| H-011 | mekanisme H-010 atas 438 simbol | −0,079078 | empat gerbang | **DITOLAK, dan TERCEMAR** |
| H-012 | semesta berlantai + pagar 0,5R, sejak 2026-01-01 | **0,041713** | tiga gerbang | **DITOLAK** |
| H-013 | faktorial 2×2 sinyal × geometri keluar, 4h | SS +0,066648; SS − AS +0,054842 (seed 42) / +0,043732 (rerata nol) | SS: `invarian_risiko`, `checksum` | **DITOLAK — p bulanan 0,205980 > 0,05** |
| **H-014** | target lawan tanpa target, umur **disetarakan 48** | SS′ +0,067252 · SH′ +0,039598; rerata selisih bulanan **−0,027715** | SS′: `invarian_risiko`, `checksum`, `funding_ekor`; SH′: + `entri_acak` | **DITOLAK — besaran −0,027715R < 0,020R dan p bulanan 0,375962 > 0,05** |

**Empat belas dinilai, empat belas ditolak. Nol kandidat bertahan.**

**Kesimpulan struktural tetap DITARIK sebagai panduan.** Run H-013 memberi angka yang tampak berlawanan (sinyal +0,054842 lawan "geometri" +0,029481), lalu Jalur A dan B memperlihatkan angka sinyal itu **tidak berarti pada satuan bulan**, ADR-033 memperlihatkan angka geometri itu **tidak mengukur geometri saja**, dan ADR-035 memperlihatkan bahwa selisih geometri yang **sudah** dibersihkan pun **tandanya bergantung pada pembobotan**. Jadi bacaan lama tidak dipulihkan dan bacaan baru tidak ditegakkan.

### TEMUAN S16 — mesin buta terhadap celah harga pada jalur stop

Gerbang `invarian_risiko` H-012 gagal pada **−21,3131R**; perdagangan itu **STGUSDT**, keluar lewat **`carry`**, pelampauan di luar biaya **20,3131R**, `jam` **1,0**. Di blok stop/target lama, `harga = stop if kena_stop else target` — **harga bar tidak pernah dipakai**. Perbaikan: `stop_hormati_celah` + `harga_stop_terisi` (`955b419a`), dinyalakan di config (`fb710521`) — dan S18 membuktikan penyalaan lewat config itu **tidak pernah bekerja** untuk pemuat H-002. **Hasil H-001b–H-012 TIDAK dihitung ulang.** Klaim "mekanisme stop sendiri sehat" **DITARIK**.

**Catatan yang masih berdiri:** pada H-013 `stop_hormati_celah` **menyala** dan `invarian_risiko` **tetap gagal pada keempat sel**; pada H-014 ia gagal pada **kedua** sel; besarnya **belum dibaca** di keenam sel.

### SEMESTA, HIMPUNAN TERTAHAN, TITIK IMPAS

**Himpunan tertahan HABIS.** Titik impas `1/(1+imbalan)`: 1R 0,5000 · 2R 0,3333 · 4R 0,2000 · 6R 0,1429 · 8R 0,1111. Di H-009, **194 dari 356 jendela (54,5%)** memilih imbalan 4,0 — versi 16 menulis 226 dan 63,5%; **itu salah**. Seretan: H-002 0,04926 · H-009 0,034614 · H-010 0,036220 · H-012 **0,035900**.

Pemilihan lookback H-013 per sel: SS 20→1682, 55→846, 100→1554 · SH 20→1987, 55→1069, 100→1026 · AS 20→1408, 55→1089, 100→1585 · AH 20→1392, 55→1073, 100→1617. **H-014:** SS′ 20→1711, 55→836, 100→1535 · SH′ 20→1995, 55→1073, 100→1014.

### MESIN BACKTEST

**`engine.Konfig` — nama medan terverifikasi dari sumber (blob `81c1db8a`):** `fee` (0,0005), `slippage` (0,0005), `atr_periode` (14), `atr_pengali_stop` (2,0), `risiko_per_trade` (0,005), `imbalan_R` (2,0), `modal_awal` (10.000), `izinkan_short` (True), `maks_umur_bar` (0), `maks_carry_R` (0,0), `jendela_carry_hari` (30), `maks_carry_realisasi_R` (0,0), `maks_biaya_masuk_R` (0,0), **`stop_hormati_celah` (False)**, `pakai_target` (True). `__post_init__` **menolak** `not pakai_target and maks_umur_bar <= 0`. `Perdagangan.R = laba / (jarak_stop * ukuran)`; di `jalankan`, `jarak = k.atr_pengali_stop * atr_t` **di kedua jenis sel**, `stop_pecahan = jarak / masuk`, `target = masuk + s*jarak*k.imbalan_R` bila bertarget dan `nan` bila tidak. Alasan keluar: `umur`, `carry`, `stop`, `target`, `akhir_data`. **`_boleh_masuk` memakai `umur_ms = k.maks_umur_bar * interval_ms`** — sebab cacat kelas keempat belas.

**Urutan pemeriksaan per bar:** umur → carry realisasi → stop/target → entri → ekuitas.

Gerbang (11): `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`, `konsentrasi`, `funding_ekor`. **Tidak dapat dinilai = GAGAL.**

**`runner.Opsi`** (blob `4ce34a3c6226b31539b22f5bd09426aaba51a927`, pembanding `fc79e070`): `dir_aset`, `out=reports`, `interval="1h"`, `universe`, `akhir_sejati`, `limit=40`, `panjang_latih=4320`, `panjang_uji=2160`, `embargo=168`, `pemanasan=200`, `ulangan=100`, `sampel_permutasi=10`, `min_median_stop_frac=0.0`. `Spek(h, sinyal, kandidat, nama, params_lookahead, buat_konfig)`. `muat_konteks` memakai `jalur_manifest(opsi.interval, opsi.out)` dan `sampel = set(sorted(bingkai)[:opsi.sampel_permutasi])`.

**`jalankan_spek` mengembalikan** `id, nama, sidik, ekspektasi_R, total_R, trade, jendela_positif, jumlah_jendela, p_entri_acak, gerbang_gagal, lulus, alasan, alasan_keluar, entri_ditolak_biaya, simbol_dibuang_lantai, bulan_dengan_trade (CACAH saja), rerata_transaksi_R, retensi_drop_1, porsi_funding_ekor_maks, std_R, galat_baku_R, jarak_galat_baku, detik` — dan menulis `out/backtest_{spek.nama}.json` + `.md` dengan **nama berkas yang sama setiap panggilan**, serta mendaftarkan `hipotesis/{spek.h.id}.json` lewat `praregistrasi.simpan`. Blok `agregat_periode` **sudah** ditulisnya lewat `agregat_per_bulan(pasangan_periode(semua_trade))`. **Terverifikasi S22:** laporan md-nya mencetak `**LULUS**` bila `putusan.lulus and laporan.semua_lulus` — itulah perangkap yang membuat berkas md sel mencetak putusan yang bukan putusan hipotesisnya.

**`walk_forward.jalankan_walk_forward`** (blob `5a686e229c0292bdea2219278a318b96fa675637`, dibaca utuh S22): `konfig_untuk(params) = buat_konfig(params, k) if buat_konfig is not None else k`, dipakai **di dalam lingkaran pemilihan kandidat** dan untuk jendela uji; `HasilJendela.konfig` menyimpan konfig yang benar-benar dipakai agar uji permutasi memakai konfig yang sama; `_skor_baku` memberi `-inf` bila trade latih di bawah `min_trade_latih` (bawaan 10); jendela tanpa kandidat layak **dilewati** tanpa perdagangan; sinyal pada bar pemanasan **dipaksa nol**; `entri_ditolak_biaya` dijumlahkan **hanya dari jendela uji**. Docstring menjanjikan jalur `buat_konfig=None` "sama persis seperti sebelum ADR-007".

**Modul H-013** (`run_h013.py`, blob `239b88d0`, pembanding `418f6084`): `NAMA_SEL` (SS, SH, AS, AH) · `NAMA_LAPORAN` · `dasar_riset` · `jendela_bar` · `bar_dibutuhkan` · `kandidat` · `pakai_target_sel` · **`umur_sel` (42 lawan 48 — cacat 14)** · `permutasi_sinyal` · `sinyal_acak` · `sinyal_sel` · `buat_konfig_sel` · `hipotesis_h013` · `spek_sel` · `kontribusi` · `prosa_kontribusi`. Beku: `IMBALAN_BEKU` 2,0 · `H_BAR` 48 · `UMUR_SEL_STOP` 42 · `SEED_PERMUTASI` 42 · `AMBANG_KONTRIBUSI_SINYAL` 0,020 · `MIN_ULANGAN` 300 · `MIN_TRADE_SEL` 100 · `PEMANASAN` 200 · `SKOR_ACAK_TERDAHULU` 0,04661 · `LOOKBACK` [20,55,100].

**Modul H-014** (`run_h014.py` + `gabung_h014.py`, `4af21176`): `NAMA_SEL=("SSp","SHp")` · `NAMA_LAPORAN_H014` · `UMUR_SETARA=48` · `AMBANG_BESARAN_R=0.020` · `AMBANG_P=0.05` · `CATATAN_AMBANG` · `PUTUSAN_MUNGKIN` · `pakai_target_h014` · `umur_sel_h014` · `konfig_sel_h014` · **`medan_berbeda`** · `sinyal_nyata` · `hipotesis_h014` · `spek_h014` · `opsi_h014` · `jalur_manifes` · `jalur_sel` · **`periksa_nama`**; penggabung: `muat_sel` · `trade_sel` · **`adjudikasi`** (dua putusan saja, membaca `rerata_selisih`) · `tulis_laporan` · `main` (keluar 0/4/2).

**Modul Jalur A** (`berpasangan.py`, blob `a9fba624`): `NAMA="berpasangan"`, `SEED=20260727`, `ULANGAN=10000`, `PEMBATAS`, `pasangkan`, `pasangan_simbol`, `pasangan_bulan`, `uji_tanda` (`p=(1+m)/(1+ulangan)`), `bootstrap` (seed+1), `ringkas` (**selalu** `memenuhi_adr015: False`), `tulis_laporan`, `main`. `_nilai` melempar pada nilai tak finit. **Tidak ada R per jendela di berkas laporan mana pun** (aturan 43).

**Modul praregistrasi** (`lux/praregistrasi.py`, blob `98a2806e`): `Kriteria(min_ekspektasi_R=0.05, min_trade_luar_sampel=100, maks_p_entri_acak=0.05, min_jendela_positif_rasio=0.5)` · `Hipotesis(id, pernyataan, dataset, ruang_parameter, kriteria, dibuat_utc, komit)` dengan `sidik()` yang **mengecualikan waktu** · **`simpan` menolak id sama dengan isi berbeda** · `nilai(h, ringkasan, p_entri_acak)` mengumpulkan **seluruh** alasan kegagalan.

### DATASET TIER B PUTARAN 2

**14.545.679 bar 1h dan 3.636.733 bar 4h**, 790 simbol, rasio 3,9996, ~703 MB. 1h: 447 valid → v2 **438** → berlantai **437**. 4h: sama, **437** pada H-013 dan H-014. Funding 1.982.017 baris, 3 celah sejati, 79,1% positif.

### Kapasitas runner dan konektivitas

4 vCPU, 15 GB RAM. **Batas 6 jam per job yang mengikat.** H-012 memakai 1220,6 s; H-013 empat sel ~sepuluh menit termasuk unduhan; satu pecahan Jalur B 30 seed mengomit 28–43 menit sesudah pemicu. **H-014 dua sel 4h: 109,5 detik komputasi, 2 menit 19 detik dinding termasuk unduhan 157 MB** — jadi **waktu run 1h yang lama didominasi UNDUHAN, bukan komputasi**, dan "terlalu cepat" bukan bukti kegagalan. python 3.12.13, numpy 2.5.1, pytest 9.1.1, pandas 2.2.3, pyarrow 17.0.0, **tanpa scipy**, **tanpa requests**. CDN `data.binance.vision` 200; REST `fapi.binance.com` **451 permanen**. Timeout: backtest 330, validate 120, potong_ekor 60, ingest 330, berpasangan 20, h013b 180/30, **h014 180**.

### Batas alat agen dan solusinya

- Daftar alat GitHub **tidak memuat satu pun fungsi Actions**. Diverifikasi ulang di S18–S22.
- `search_code` **nol hasil di repo ini**. `get_file_contents` menuntut SHA 40 karakter penuh, tetapi **menerima `ref: "main"`**, pada direktori memberi **ukuran berkas**, dan **menerima SHA commit apa pun** — itulah cara mengadili laporan yang sudah tertimpa.
- `push_files` **mengganti seluruh isi berkas**; baca dulu, dan baca ulang muatannya sebelum mengirim (aturan 35, 54). **Tidak ada mode tambal.** Bentuk panggilan yang benar: `owner`/`repo`/`branch`/`message`/`files` seluruhnya **di dalam** `toolArguments`.
- Filter `paths` per berkas: menyentuh `backtest.yml`, `h013b.yml`, atau **`h014.yml`** **langsung memulai run**. `tests.yml` memfilter `lux/**` dan `tests/**`, jadi `config/`, `journal/`, `decisions/`, dan `STATE.md` **tidak** memicunya.
- **Kabar buruk datang dalam 23–32 detik; kabar baik 10–45 menit** — kecuali `tests.yml`, yang memberi kabar **baik** dalam ~23 detik juga, dan kecuali run 4h yang komputasinya memang pendek. **Baca isinya, jangan membaca kecepatannya.**
- **Kegagalan pagar pra-terbang tidak meninggalkan commit sama sekali**, sebab langkah commit `if: always()` menemukan nol berkas dan keluar 1. Jadi **diam bukan tanda lulus dan bukan tanda gagal**.
- **Commit laporan tanpa berkas hasil berarti run GAGAL. Blob laporan yang tidak berubah berarti belum ditulis.**
- **Beberapa pekerjaan yang mengomit ke satu cabang menuntut lingkaran ulang dorong**; yang kalah lomba hilang **tanpa suara**.
- **Pekerjaan matriks yang bergantung pada keluaran pekerjaan lain wajib `git fetch` + `git checkout origin/main -- reports`** — pelajaran `h013b.yml`.
- **`backfill_daily.yml` berjadwal mingguan**, jadi tidak setiap perubahan blob berasal dari saya.
- **Modul baru berdiri hijau sendiri lebih dulu. Baca modulnya sebelum menulis kode terhadapnya** — dilanggar tiga kali dalam tiga puluh menit di S21.

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1–3**, **metrik celah funding**, **circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`).
- **S12:** STATE v11 dan v13 menaikkan kekeliruan menjadi fakta; ditarik v12 dan v14.
- **S13:** "226 dari 356 jendela (63,5%)" padahal **194 (54,5%)**.
- **S15:** empat run gagal berturut. Aturan 31–34.
- **S16:** dua commit cacat; dua ramalan cacah salah; klaim "mekanisme stop sehat" ditarik. Aturan 35–36.
- **S17:** lima cacat buta-interval; ramalan 693 salah. Aturan 37–38.
- **S18:** cacat kelas kedelapan, kesembilan, kesepuluh. Aturan 39–41.
- **S19:** cacat kesebelas dan kedua belas; ADR-024 menjadwalkan uji per jendela yang **mustahil**. Aturan 42–46.
- **S20:** cacat **ketiga belas**; dua rancangan Jalur B jatuh sebelum ditulis; satu bahaya penimpaan diam-diam tertangkap karena membaca `runner.py`; dua ramalan meleset; `6ae83062` mendorong sumber tanpa pagarnya. Aturan 47–51.
- **S21:** cacat **keempat belas** dan **kelima belas**. **Tiga koreksi diri dalam ~30 menit dengan satu akar sebab yang sama: merancang di atas modul yang belum dibaca.** Ditambah **R-H1 meleset** oleh aritmetika sendiri. Aturan 52–54.
- **S22:** cacat **keenam belas** (tanda besaran bergantung pembobotan) dan **ketujuh belas** (berkas gerbang tidak masuk daftar `git add`). **Satu kesimpulan salah yang dinyatakan sebagai kesimpulan, bukan sebagai dugaan: "2 menit 19 detik berarti run gagal".** Run itu berhasil. **R-G4 meleset jauh pada mekanismenya**, dan **R-H3 tepat tetapi tidak berguna**. Aturan 55–56.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| **Sebab `AH = +0,05817042814276683R` setinggi itu pada sel acak** | penjelasan penyebut R **DIFALSIFIKASI** (ADR-033 §2); penjelasan baru belum ada. **Ini memerlukan verifikasi.** |
| **Sebab SH ≠ SH′** (44.614 lawan 44.538; +0,037167R lawan +0,039598R; lookback bergeser) | baca `run_h013.buat_konfig_sel` dan `run_h014.konfig_sel_h014` berdampingan; `walk_forward` sudah dibaca dan memperlihatkan konfig dipakai **di dalam** pemilihan kandidat. **Ini memerlukan verifikasi.** |
| **Besar kegagalan `invarian_risiko`** pada empat sel H-013 dan dua sel H-014 | baca JSON sel lewat skrip sisi runner, **jangan** ditarik ke konteks (432 KB per berkas) |
| **Gerbang `checksum` 4h lulus pada run 4h KEDUA** | R-B1 separuh kedua — **mustahil sampai cacat 17 ditutup** |
| **Prosa dan komentar `runner.py` tidak bergeser oleh `43cd4eed`** | bandingkan terhadap blob `fc79e070` |
| **Prosa `run_h013.py` tidak bergeser oleh `b0e79220`** | bandingkan terhadap blob `418f6084` |
| Angka kelayakan 1h dan 4h yang identik (447/74/112) benar | bandingkan `reports/diag_datar.json` terhadap perhitungan 4h; penolakan 4h semestinya **≤ 74** |
| STGUSDT benar-benar bergerak melawan ~46,8% dalam ~satu bar 1h | bar itu di rilis artefak, sandbox tanpa jaringan |
| Ekspektasi R dengan `stop_hormati_celah` menyala lebih rendah | ADR-016 ramalan 5 |
| Funding sebagai **sinyal** memuat informasi arah | belum pernah diuji |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap universe layak v2 438 |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |

**Difalsifikasi sebelumnya:** saringan rezim tren memperbaiki breakout · retest memperkecil biaya per R · SMC yang dapat dikodekan punya keunggulan · "biaya menjaga risiko memakan ekspektasi" · "ekspektasi bergantung umur simbol" · "kerugian ekor dari bar menganga pada stop" · sinyal `breakout_atr` punya keunggulan yang bertahan di waktu pada 1h (H-012) · lantai 0,004 menutup **seluruh** jalan masuk degenerasi · "hasil 40 simbol mewakili 438 simbol" · **"jendela walk-forward adalah jumlah bar"** · **"nilai di `config/lux.yaml` sampai ke mesin"** · **"semesta 4h disalin dari 1h"** · **"laporan memuat R per jendela"** · **"sumbangan sinyal tersebar merata di waktu"** · **"SH < AH menuntut penjelasan"** · **"laporan memuat agregat bulanan yang dapat dipakai langsung"** · **"sebaran nol cukup lebar sampai menyentuh +0,066648R"** · **"sumbangan sinyal +0,054842R sah tanpa menyebut seed"** · **"SS − SH mengukur geometri keluar"** (cacat 14) · **"penyebut R berbeda antara sel bertarget dan sel tanpa target"** (ADR-033 §2) · **"ambang ADR-015 §4.4 berlaku untuk kaki geometri"** (cacat 15) · **"`berpasangan.py` dapat mengadili kelulusan"** (ADR-034 §1) · **"ramalan tentang kode saya sendiri selalu tepat"** (R-H1) · **"umur 42 lawan 48 adalah sebab utama jarak 60.018 lawan 44.614"** (ADR-035 §4: −1,2%) · **"tanpa target, posisi dipegang sampai umur habis"** (R-G4: `stop` 62,9%) · **"besaran yang dilaporkan dua kali cukup untuk mengamankan putusan"** (cacat 16) · **"run yang selesai dalam 2 menit 19 detik berarti gagal"** · **"jalur `buat_konfig=None` dan `buat_konfig=buat_konfig_sel` memberi hasil yang sama"** (ADR-035 §5).

**Terbukti benar:** imbalan lebih besar menaikkan ekspektasi (+28%) · lama pegang membesarkan kerugian ekor · keunggulan bertahan bila penyumbang terbesar dibuang (H-013 retensi 0,9866; SS′ 0,9872) · "H-012 gagal", diramalkan sebelum run · jalur 1h bit-identik sesudah ADR-019 · konversi jendela ADR-023 menghasilkan 4.082 jendela per sel · dugaan manifest 1h lawan aset 4h sebagai sebab `checksum` · **"p per-perdagangan menyesatkan sementara p bulanan menjatuhkan"** · **"simpangan baku antar seed melampaui galat baku per perdagangan"** · **"koreksi prosa tidak merusak satu pun dari 811 pengujian"** · **"`maks_umur_bar` ikut menolak entri lewat proyeksi carry"** · **"tanpa target sebaran R melebar dan retensi jatuh"** (2,20818R lawan 1,37827R; 0,9047 lawan 0,9872) · **"target membebaskan modal lebih awal sehingga lebih banyak entri lolos proyeksi carry"** (+33,2% trade).

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 · metrik celah funding putaran 1–4 · seluruh run pilot H-001 · porsi "101,2%" · nilai gerbang `funding` sebagai bukti funding aman · "226 jendela / 63,5%" · ekspektasi H-010 0,053028R sebagai bukti layak dagang · **+0,060163R** · **+0,059546R** · **+0,060168R** · **281 dari 398 simbol positif** dan median **+0,06343** · **−0,091519R** tanpa sebabnya · **+0,059636R** sebagai kelulusan · **+2.347,27R bulan 2026-01** · gerbang bar datar 4h sebagai bukti kebersihan data · **`+0,054842R` sebagai kelulusan H-013, dan sebagai besaran mana pun tanpa menyebut seed 42** · **`+0,043732R` sebagai kelulusan** · **`+0,066648R` sebagai bukti layak dagang** · kata "LULUS" pada `reports/backtest_h013_kontribusi.md` · **`p = 0,001100` tingkat simbol sebagai bukti keberartian** · **`p = 0,003322` satuan perdagangan sebagai bukti keberartian** · **p atau galat baku per-perdagangan mana pun sebagai bukti keberartian**, termasuk "+2,99 galat baku" dan "+3,05 SE" · **prosa R-D3 di `reports/h013b_p.md` sebagai penilaian kesehatan permutasi** · **`+0,029481R` sebagai sumbangan geometri keluar, sebagai pembanding H-014, atau sebagai "versi sebelum perbaikan"** · **kata `LULUS` pada berkas md sel H-014 sebagai putusan H-014** · **ambang ADR-015 §4.4 sebagai pra-registrasi kaki geometri** · **`+0,027654R` sebagai sumbangan geometri keluar atau sebagai besaran yang melewati ambang** · **salah satu dari empat pembobotan H-014 tanpa menyebut ketiga lainnya** (aturan 55) · **`+0,067252R` (SS′) sebagai bukti layak dagang** · **kegagalan `checksum` 4h sebagai temuan** sampai cacat 17 ditutup.

---

## 5. Penghalang aktif

**TIDAK ADA RUN YANG SEDANG BERJALAN.** Run `30221967019` selesai dan laporannya dikomit `603477ce`. Berkas hasil yang ada di `main`: `reports/backtest_h014_ssp_target_umur48.{json,md}`, `reports/backtest_h014_shp_tanpa_target_umur48.{json,md}`, `reports/h014_run.json`, `reports/h014_berpasangan.{json,md}`, `reports/h014_log.md`, `hipotesis/H-014-SSp.json`, `hipotesis/H-014-SHp.json`. **`reports/manifest_aset_4h.json` TIDAK ADA** — cacat 17.

**Penghalang nyata:** setiap perbaikan yang menyentuh `.github/workflows/h014.yml` **memicu run penuh**. Karena itu perbaikan daftar `git add` (cacat 17) dan pembersihan komentar `run_h014.medan_berbeda` **wajib menumpang** run 4h berikutnya yang memang dikehendaki, bukan didorong sendirian.

Tidak ada yang dibutuhkan dari pengguna. **`backfill_daily.yml` dapat berjalan sendiri setiap Senin 02:00 UTC.**

---

## 6. Tindakan berikutnya

1. ~~ADR-017 s.d. ADR-023~~ · ~~H-013~~ · ~~Jalur A~~ · ~~ADR-025–028~~ · ~~STATE v23–v26~~ · ~~cacat kesepuluh~~ · ~~Jalur B tiga modul~~ · ~~ADR-029/030~~ · ~~run Jalur B~~ · ~~ADR-031~~ · ~~aturan 49–50 ke alat (819)~~ · ~~ADR-032/033/034~~ · ~~kode H-014 + pengujian (855)~~ · ~~workflow `h014.yml`~~ · ~~run H-014 dan adjudikasi R-G/R-H~~ · ~~ADR-035 + jurnal 32~~ · ~~STATE v28~~ — **selesai**.
2. **Cacat 17:** tambahkan `reports/manifest_aset_4h.json` ke daftar `git add` di `h014.yml` (aturan 56), **menumpang** run 4h berikutnya. Sesudah run itu, adjudikasi **paruh kedua R-B1**.
3. **Anomali `buat_konfig` (SH ≠ SH′):** baca `run_h013.buat_konfig_sel` dan `run_h014.konfig_sel_h014` berdampingan; `walk_forward.py` sudah dibaca utuh di S22 dan memperlihatkan konfig kandidat dipakai **di dalam** lingkaran pemilihan. Sampai terjawab, SS′ − SH′ **bukan** "SS − SH yang sudah diperbaiki".
4. **Buang komentar menjorok berlebihan di `run_h014.medan_berbeda`** — **jangan didorong sendirian**, tumpangkan.
5. **Baca nilai `invarian_risiko`** pada enam sel (empat H-013, dua H-014) lewat skrip sisi runner.
6. **Selesaikan pertanyaan bar datar 1h lawan 4h:** bandingkan `reports/diag_datar.json` terhadap perhitungan 4h; penolakan 4h semestinya **≤ 74**. Sambungkan `maks_rasio_bar_datar` ke gerbang (aturan 39).
7. **Nasib `notion_asap.yml`** dan **`backfill_daily.yml`**; tinjau `funding.yml`, `funding_check.yml`, `doctor.yml`, `universe.yml`. **Jangan hapus tanpa keputusan tertulis.**
8. **Program riset lanjutan: funding sebagai SINYAL** — satu-satunya dimensi bersih yang tersisa. **Pra-registrasi lengkap wajib ditulis dan dikomit lebih dulu, dan modul-modul yang disebutnya wajib dibaca SEBELUM pra-registrasi ditulis** (pelajaran S21). Gerbang p bulanan wajib (ADR-031 keputusan 5). **Wajib menyatakan pembobotan mana yang mengikat sebelum run** (aturan 55). ADR-015 §4.5 butir 5 tampak terbalik dan §6 sudah berjanji mengakuinya.
9. **Cari penjelasan baru bagi `AH = +0,058170R`** — penjelasan penyebut R sudah mati.
10. Utang ekor panjang: bandingkan `runner.py` terhadap `fc79e070` dan `run_h013.py` terhadap `418f6084` · `hasattr`/`__import__` di `test_run_h012.py` · pengujian `biaya_bolak_balik_R` · `pytest` ke `requirements-dev.txt` · tripwire tekstual `inspect.getsource` (lemah, dicatat lemah) · pemetaan `dari_laporan` pelapor Notion · perketat `lux/funding.py::gerbang_lulus` · diff Dataset G lama · salin ADR-001/ADR-002 ke `decisions/` · naikkan `versi` config sesudah seluruh pembacanya diperiksa · **Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, ≥24 shard**.

**Yang DILARANG:** menyatakan sistem siap dagang · **menyebut H-013 lulus** · **menyebut H-014 lulus — tidak ada cabang kodenya, dan menambahkannya dilarang** · **menambal `berpasangan.py` supaya dapat memancarkan kelulusan** · **mengutip +0,054842R, +0,043732R, atau +0,066648R sebagai kelulusan** · **mengutip +0,029481R atau +0,027654R sebagai sumbangan geometri keluar** · **mengutip satu pembobotan tanpa ketiga lainnya** (aturan 55) · **membaca kegagalan `checksum` 4h sebagai temuan sampai cacat 17 ditutup** (aturan 42, 56) · **membandingkan SS′ − SH′ dengan SS − SH sebagai "angka yang sama sesudah diperbaiki"** · **menyebut umur 42 lawan 48 sebagai sebab utama jarak 60.018 lawan 44.614** · **mengutip ambang ADR-015 §4.4 sebagai pra-registrasi kaki geometri** (aturan 53) · **mengutip p atau galat baku per-perdagangan sebagai bukti keberartian** · **mengutip p 0,001100 tingkat simbol sebagai kelulusan** · mengutip +0,060163R atau +0,059636R sebagai kelulusan · **memilih satuan penarikan atau pembobotan sesudah hasil terlihat** · membuang simbol atau memilih bulan sesudah melihat hasil · **menyebut H-012, H-013, atau H-014 sebagai "H-010 setelah perbaikan"** · menyebut angka R lama **konservatif** · **menghitung ulang H-001b sampai H-012** · menggeser lantai 0,004, pagar 0,5R, `BATAS_VOID` 20, batas `2026-01-01`, **ambang 0,020R**, **p ≤ 0,05**, **≥300 ulangan**, **≥100 trade per sel**, `MAKS_RASIO_DATAR` 0,10, atau ambang rasio 0,30 · **melonggarkan ambang dengan berdalih memperbaiki satuan penarikan atau pembobotan** · mematok `imbalan_R` ke 8,0 · melombakan `imbalan_R`, `h`, `pakai_target`, **atau `maks_umur_bar`** · **memakai `Spek.buat_konfig` untuk geometri** · menurunkan `--ulangan` dari 300 · menaikkan `maks_umur_bar` dari 168 sebagai penyelamatan · membuang simbol merugi · memakai `konsentrasi` atau `funding_ekor` sebagai penyaring simbol · melombakan ambang pengaman · melonggarkan `invarian_risiko` dari −1,5R · **menggeser ambang ekspektasi 0,05R** · menjadikan `stop_hormati_celah` parameter yang dilombakan · **memperbaiki `muat_konfig_h002` tanpa ADR** · **menurunkan pagar pra-terbang yang menemukan cacat** · **menyentuh `reports/manifest_aset.json`** · **menimpa `hipotesis/H-013*.json` atau `hipotesis/H-014*.json`** · **menandai putusan DITOLAK sebagai kegagalan pekerjaan** (aturan 48) · **menulis ulang laporan atau pesan commit yang sudah dikomit untuk menutupi ramalan yang meleset** (aturan 50) · **menghapus jejak `BUNYI_ASLI_R_D3`** · **mendorong perubahan modul tanpa pengujiannya di dorongan yang sama** (aturan 51) · **meramal cacah uji dari rencana alih-alih dari berkas** (aturan 54) · **mendorong perubahan berkas workflow hanya untuk kosmetik** (memicu run untuk nol pengetahuan) · **membekukan ramalan durasi selebar R-H3 lagi**.

---

## 7. Pengawasan otonom — DIHENTIKAN

Agen **LUX Gatekeeper** dan **LUX Gatekeeper Reporter** **tidak dipakai lagi.** Keputusan pengguna, 2026-07-26.

Bukti dari sisi Notion atas baris asap `3a9d5df0-96f9-81df-90a7-f6075d071680`: agen itu mengadili **setiap** baris otomatis dalam sekitar dua menit, termasuk baris yang menyatakan `bukan_hasil_riset=true`, dan memakai `Ditolak` untuk "bukti tidak cukup" padahal `Ditolak` semestinya berarti hipotesis gagal. **Vonis yang salah arti lebih buruk daripada tidak ada vonis** — S18 menambahkan bentuk kedua (vonis dari separuh kriteria), S19 bentuk ketiga (**satuan salah**), S20 bentuk keempat (**benar pada satu satuan dan terbalik pada satuan lain di dalam satu run**), S21 bentuk kelima (**vonis atas besaran yang namanya tidak sesuai dengan apa yang diukurnya**, cacat 14), dan **S22 bentuk keenam: vonis yang tandanya bergantung pada cara membobot** (cacat 16).

Kolom `Verdict` di database `LUX — Run Results` karena itu menjadi kolom **manusia**.

---

## 8. Peta repo

| Path | Isi |
|---|---|
| `config/lux.yaml` | seluruh parameter yang memengaruhi hasil; **satu kunci masih TIDAK DIBACA gerbang**: `maks_rasio_bar_datar`; `versi` masih 2 |
| `lux/kerangka.py` | **modul daun**: `bar_per_hari`, `jam_interval`, `bar_dari_hari` |
| `lux/binance_vision.py` · `lux/universe.py` | arsip dan universe point-in-time |
| `lux/ingest.py` · `lux/backfill_daily.py` | ingest Tier B d