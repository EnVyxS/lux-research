# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Arsip rinci ada di **`STATE_LAMPIRAN.md`** dan **`STATE_LAMPIRAN_ANGKA.md`**, dan wajib dibaca bersamanya. Jika sesuatu tidak tercatat di salah satu dari ketiganya, anggap belum diketahui.

**Diperbarui:** 2026-07-27 (versi 33) — ditulis sesudah blob v32 (`4c1ff162c33f5ab2510f677fb50092de86f0f544`, commit `0dd14098`) dibaca **utuh**. Aturan 1–58 dibawa **verbatim**; ditambahkan **aturan 59 dan 60**.

**MITIGASI ATURAN 35, DIJALANKAN DI v33.** v32 berukuran 48.058 B dan **tumbuh** melawan mitigasi aturan 35 sendiri. Seluruh tabel besaran H-011 sampai H-015 karena itu dipindahkan **verbatim** ke **`STATE_LAMPIRAN_ANGKA.md`**. Tidak ada angka yang dibuang; yang dibuang adalah kebiasaan menaruhnya di berkas yang wajib dibaca ulang utuh setiap sesi.

**KOREKSI YANG WAJIB DIBACA LEBIH DAHULU — v32 dan PROMPT v4 keliru.** Keduanya menyatakan H-015 "**berkode LENGKAP** serta hijau". Kata **lengkap TIDAK BENAR**: pada saat itu `lux/backtest/gabung_h015.py` **belum ada**, sehingga tidak ada satu pun alat yang dapat mengadjudikasi hasilnya. Berkas lama tidak ditulis ulang (aturan 50); jejaknya ada di jurnal 40, 41, dan 42.

**KOREKSI KEDUA.** v32 dan jurnal 40/41 mencatat "**delapan** butir pagar pra-terbang". `logs/preflight.log` H-015 mencetak **sembilan** (butir 1 sampai 9). Salah cacah oleh saya, bukan salah kode.

**KOREKSI KETIGA — atas penalaran saya sendiri.** Di jurnal 41 saya menyebut kerugian −11,4736R sebagai "ekor tunggal" dan membangun ramalan R-O2 di atas premis itu. Tabel ekor sel F membantahnya: sekurangnya **sepuluh** perdagangan melewati −4R. Premisnya salah, jadi R-O2 dinyatakan **cacat penalaran**, bukan "menunggu bukti".

**KOREKSI ATAS KOREKSI (dibawa dari v32, berlaku penuh).** v30 menyatakan rujukan "ADR-009" atas pengaman carry keliru dan menggantinya dengan ADR-008. Itu koreksi yang **terlalu keras**. Yang benar berlapis tiga:

| Lapisan | Dokumen | Kutipan |
|---|---|---|
| **Medan** `Konfig.maks_carry_realisasi_R` dan mekanismenya (dinilai ulang tiap bar, alasan keluar `carry`) | **ADR-008** | "Medan baru `Konfig.maks_carry_realisasi_R`, bawaan **0.0 yang berarti MATI**" |
| **0,25 dipatok sebagai batas risiko yang TIDAK dilombakan** | **ADR-009** | "dikeluarkan dari ruang parameter dan dipatok menyala… Nilai yang dipatok adalah **0,25**" |
| **Asal angka 0,25** | **ADR-004** | "sudah ada di `config/lux.yaml` versi 2 sebagai `risiko.maks_carry_R = 0.25` sejak ADR-004" |

Di ADR-008, 0,25 masih **dilombakan** ({0,0 · 0,25 · 0,50}) dan **kalah 22 lawan 334** — dari kekalahan itulah aturan 12 lahir. Karena `run_h009.AMBANG_CARRY_KERAS` memasang **patokannya**, sebutan "pengaman carry keras ADR-009" di `lux/backtest/funding_ekor.py` **dapat dibela**. Jejak kedua kesalahan ada di jurnal 35, 36, dan 37.

**Cacat alat yang masih tercatat dari v28:** dorongan v28 pertama (commit `56633f80`) **terpotong** di tengah bagian 8 — pelanggaran aturan 35 dalam bentuk ketiga. Commit terpotong itu **tidak dihapus dan tidak disembunyikan** (aturan 50).

**Tahap sekarang:** S22 — **H-015 DIJALANKAN dan putusannya TIDAK DAPAT DINILAI** (run `30249117960`, ADR-038). Ketiga selnya gagal dua gerbang: `checksum` (cacat alat, sudah dibayar) dan **`invarian_risiko` (substantif, tidak akan sembuh dengan run ulang)**. **ADR-038 membekukan adjudikasi seluruh jalur berjalan** sampai sebab kerugian melewati −1,5R diketahui. **Empat belas hipotesis dinilai, empat belas ditolak; H-015 belum terhitung karena belum dapat dinilai. Nol kandidat bertahan.**

**Cacat 18 DITUTUP.** Penutupnya adalah R-L5, dan R-L5 **TEPAT**: alasan keluar `carry` bercacah **82 / 27 / 26** pada sel K / F / A. Pengaman carry terealisasi terbukti hidup di dalam run sungguhan, bukan hanya di pytest.

**Cacat 17 DIBAYAR, efeknya belum terlihat.** `reports/manifest_aset_4h.json` kini ada di `main` (blob `b8f7b04253710be797e0fba501e70457c856d545`). H-011 dan H-012 lulus `checksum` karena manifes 1h-nya sudah ada sebelum run — itu bukti empiris mekanismenya benar. Cabang `runner.py` yang memancarkan "manifest baru ditulis pada run ini" **belum dibaca; ini memerlukan verifikasi**.

**KESALAHAN URUTAN, DIAKUI:** membayar cacat 17 di dalam sentuhan yang **memulai** run adalah keputusan sadar dan salah. Manifes seharusnya dikomit lewat dorongan yang tidak memicu apa pun. Ongkosnya satu run — dan ongkos itu ternyata murah, sebab run 4h H-015 hanya 8 menit 52 detik, bukan 4 jam.

**Tahap berikutnya:** (a) diagnostik ADR-038 §5.4 atas perdagangan yang melewati −1,5R; (b) jurnal 43; (c) instrumentasi penolakan saringan per arah, atau cabut R-L1.

**Tidak ada run yang sedang berjalan.** Satu-satunya proses berjadwal adalah `backfill_daily.yml`, tiap Senin 02:00 UTC.

---

## 1. Aturan membaca berkas ini

Bagian 3 adalah **fakta**: setiap baris punya bukti berupa commit, run ID, atau kutipan. Bagian 4 adalah **asumsi**: dilarang diperlakukan sebagai fakta. Pemindahan dari 4 ke 3 hanya dengan bukti terlampir.

Aturan yang lahir dari kesalahan nyata, bukan dari teori:

1. **Angka yang lulus gerbang belum tentu benar.** Rasio 1h:4h 4,014 pernah dicatat sebagai uji silang yang lulus, padahal sedang melaporkan bug.
2. **SHA laporan yang tidak berubah bukan tanda pekerjaan masih berjalan.**
3. **Penjelasan yang membuat anomali terasa wajar harus dicurigai lebih keras daripada anomalinya.** **Dipakai dua kali di S22 pada diri sendiri, dan kedua kalinya saya kalah:** pertama "ADR-009 memasang pengamannya, jadi pengamannya milik ADR-009"; lalu koreksinya sendiri, "kalau bukan ADR-009 berarti ADR-008" — keduanya rapi, keduanya tidak lengkap. Yang benar berlapis tiga (lihat kepala berkas). **Bentuk kesalahannya: satu label untuk tiga keputusan yang berbeda lapisan.**
4. **Lihat sebaran mentah sebelum berteori.** Metrik celah funding gagal lima putaran; satu histogram di awal cukup. **Dipakai lagi di S22 akhir dan berbuah:** membaca sepuluh baris tabel ekor sel F membatalkan seluruh penalaran "ekor tunggal" yang saya bangun tanpa melihat sebarannya.
5. **Hipotesis yang ditolak tetap ditolak.** Ambang tidak disetel ulang setelah hasil terlihat. **Dipakai di S22:** H-014 **tidak** dijalankan ulang dengan pengaman carry dinyalakan, sekalipun cacat 18 ditemukan sesudahnya. **Dipakai kedua kali di ADR-038:** ambang `invarian_risiko` −1,5R **tidak** digeser sekalipun ia menghalangi setiap putusan.
6. (S8) **Percobaan yang informatif ke dua arah lebih berharga daripada percobaan yang dirancang agar berhasil.** **Terbukti pada H-015:** sel A membuat run tetap informatif, dan yang paling informatif justru datang dari arah yang tidak dirancang — gerbangnya, bukan sinyalnya.
7. (S9) **Saringan yang membuang perdagangan tidak otomatis membuang perdagangan yang buruk.** Saringan funding membuang 6.281 perdagangan dari 59.306; **pemecahan per arahnya tidak pernah dipancarkan** (cacat 21).
8. (S10) **Periksa apakah dugaanmu mungkin secara konstruksi sebelum menjadwalkannya sebagai penelitian.**
9. (S11) **Periksa apakah laporan yang sudah dikomit sudah menjawabnya.** **Dipakai di S22 akhir dan berbuah besar:** R-O3 diadjudikasi utuh **tanpa satu run pun**, hanya dengan membaca laporan H-011 dan H-012 yang sudah dikomit berbulan riset lalu.
10. (S11) **Gerbang yang kegagalannya tidak tertulis ke `reports/` adalah titik buta yang menyamar sebagai gerbang.**
11. (S12) **Rerata tidak mengatakan apa pun tentang ekor.** Gerbang nilai ekstrem hanya boleh dibantah dengan nilai ekstrem. **Bentuk kedua ditemukan di S22:** **kuartil pun tidak mengatakan apa pun tentang ekor.** Q1 −1,0289 lawan min −11,4736 saya baca sebagai bukti ekor tunggal; kenyataannya sepuluh perdagangan terburuk semuanya melewati −4R. Ekor hanya dapat dibaca dari daftar ekor.
12. (S12) **Batas risiko tidak dilombakan.** Lahir di ADR-009 sesudah pemilih membuang pengaman pada **334 dari 356 jendela**. **Dilanggar tanpa sengaja di S22:** H-014 tidak melombakan batas itu, ia **mematikannya** (cacat 18, aturan 57) — dan mematikan lewat `None` tidak meninggalkan jejak di manifes.
13. (S12) **Peristiwa yang terlalu jarang tidak dapat dipilih oleh pemilih dalam sampel.**
14. (S12) **Ramalan yang salah lebih murah daripada ramalan yang tidak pernah ditulis.** **Batasnya ditemukan di S22 dan menjadi aturan 60:** ramalan yang **tidak dapat dinilai** lebih mahal daripada keduanya, sebab ia tampak seperti disiplin.
15. (S12) **Porsi terhadap nilai bersih bukan ukuran konsentrasi.** Pakai jackknife dan penyebut bruto.
16. (S12) **Proksi yang berkorelasi 0,97 dengan hal lain bukan proksi.**
17. (S12) **Gerbang yang memberi jawaban sama pada dua keadaan bertolak belakang tidak memuat informasi.**
18. (S12) **Angka jumlah yang ditulis tangan hanya boleh ada di satu tempat, yaitu pengujian tripwire.**
19. (S13) **Margin setipis satu satuan resolusi bukan margin.** `entri_acak` H-010 lulus p 0,049505 pada 100 permutasi; pada 300 permutasi mekanisme yang sama memberi **0,0631** dan **gagal**. Dikonfirmasi ulang di H-012: **0,06312292358803986**. Diperluas di S19: R-A4 meramal p ≤ 0,001 dan nyatanya 0,001100. Diperluas lagi di S20: **R-D1 meleset hanya tiga menit dua detik dan tetap dicatat MELESET.** **Dan di S22: R-K2 meleset SATU uji — tetap MELESET.** Tipis bukan alasan. **Bentuk ketiganya muncul di S22 sebagai float biner:** `0.06 - 0.04` bernilai `0.019999999999999997`, jatuh 3 × 10⁻¹⁸ di bawah ambang 0,020 dan karena itu **TIDAK** lulus — dan ambang itu **tidak** dilunakkan dengan pembulatan.
20. (S13) **Ekspektasi yang naik karena penyebutnya menyusut bukan keunggulan yang membesar.**
21. (S13) **Kecurigaan wajib naik, bukan turun, ketika hasilnya menyenangkan.** Dipakai empat kali di S16–S17 atas run yang terasa terlalu cepat; keempatnya **tak berdasar**. Kelima di S18 atas +0,054842R — **berdasar** (ADR-024). Keenam di S19 atas p simbol 0,001100 — **berdasar** (ADR-028). Ketujuh di S20 atas p per-perdagangan 0,003322 — **berdasar** (ADR-031). Kedelapan di S21 atas +0,029481R — **berdasar** (ADR-033, cacat 14). Kesembilan di S22 atas agregat +0,027654R — **berdasar** (ADR-035, cacat 16). **Bentuk terbaliknya juga nyata:** di S22 saya mencurigai run 2 menit 19 detik sebagai kegagalan dan **salah**. **Kesepuluh di S22 akhir atas sel F yang +5,22 galat baku di atas ambang — berdasar, dan sebabnya bukan statistik melainkan gerbang.**
22. (S13, ADR-014) **Menuntut kesamaan bit pada agregat pecahan adalah pengujian yang menyala pada perilaku yang benar.** Di dalam satu fungsi murni, kesamaan bit tetap sah.
23. (S13, ADR-014) **Pagar yang memastikan masukan identik tidak memastikan masukan sah.** Diperluas di S17: **kesamaan hasil lintas dua run berbeda dilarang diterima tanpa pemeriksaan.** **Dipakai lagi di S22 pada arah sebaliknya, dan berbuah:** SH dan SH′ nominal identik tetapi **tidak** identik (44.614 lawan 44.538). **Bentuk ketiga di S22 akhir:** −11,4736R **identik** pada empat sel bersinyal berbeda — dan kali ini keidentikan itu **bermakna**, sebab ia membuktikan perdagangan itu bukan sifat sinyal melainkan sifat data.
24. (S13, ADR-014) **Satu simbol dapat mendominasi agregat 438 simbol.**
25. (S13, ADR-014) **Himpunan tertahan habis pada saat pertama kali dilihat.**
26. (S13, ADR-014) **Cacat yang membalik tanda hasil tidak boleh diperbaiki di dalam hipotesis yang sama.** **Dipakai di S22:** cacat 18 tidak diperbaiki di dalam H-014; perbaikannya hidup di H-015, dan di sana ia terbukti bekerja.
27. (S13, ADR-014) **Eksperimen yang tercemar tidak informatif ke arah mana pun.** **Diuji di S22 dan TIDAK berlaku pada H-014:** kedua sel salah **secara identik**, sehingga selisih antar sel tetap mengukur satu medan (ADR-036 §4).
28. (S13, ADR-014) **Saringan yang menolak entri juga menolak saat pemilihan.** Terbukti kuantitatif di H-012: hanya **62** entri ditolak pengaman. **Terbukti kedua kali di S21:** `maks_umur_bar` ikut menolak **entri** lewat proyeksi carry di `_boleh_masuk`.
29. (S14) **Pra-registrasi wajib diperiksa terhadap apa yang benar-benar dapat dihitung dari laporan.** **Dilanggar di S22 pada R-L1, dan itu melahirkan aturan 60.**
30. (S14) **Kriteria utama dihitung dari berkas laporan yang dikomit, bukan dari nilai yang beredar di memori run.**
31. (S15) **Pagar yang menyalin baris dari kode yang dijaganya tidak menjaga apa pun.** **Dipakai sebagai rancangan di S22:** `konfig_audit` sengaja **tidak** memuat angka 0,25; daftar pengaman wajib datang dari pemanggil. **Diperkuat di S22 akhir:** tuntutan atas `maks_carry_R` **bukan** tautologi sebab angkanya datang dari `config/lux.yaml`; tuntutan atas `maks_carry_realisasi_R` **nyaris** tautologi dan yang dijaganya adalah **jalurnya**, bukan angkanya.
32. (S15) **Aritmetika yang hidup di dalam `main` tidak dapat diuji.**
33. (S15) **Setiap langkah workflow wajib `tee` ke `logs/` dan seluruh `logs/` disalin ke `reports/` dengan `if: always()`.** **Terbukti menyelamatkan di S22 akhir:** run `30249117960` merah, dan seluruh laporannya tetap dikomit (`5b2f70b6`) — tanpa itu, putusan H-015 tidak akan pernah terbaca.
34. (S15) **Lingkungan pagar wajib memasang dependensi yang sama dengan `tests.yml`.**
35. (S16) **Muatan tulis yang panjang wajib dibaca ulang utuh sebelum dikirim, dan jumlah pengujian dicacah dari muatan yang benar-benar dikirim, bukan dari rencana.** **DILANGGAR DI S22 dalam bentuk ketiga:** muatan `STATE.md` v28 pertama **terpotong** dan dikomit terpotong (`56633f80`). Mitigasi: berkas panjang dipecah, dan setiap dorongan panjang **dibaca ulang dari `main` sesudah dikirim**. **Mitigasi ketiga:** jangan membaca berkas 40 KB lalu menulis penggantinya dalam jendela konteks yang sama. **Mitigasi keempat, dijalankan di v33:** tabel besaran dipindah ke `STATE_LAMPIRAN_ANGKA.md` supaya `STATE.md` **menyusut**, sebab v32 tumbuh menjadi 48.058 B.
36. (S17, ADR-016) **Ramalan yang dijamin benar oleh konstruksi bukan ramalan.** **Dibuktikan telanjang di S22:** R-H3 meramal run selesai di bawah 25 menit; kenyataannya 2 menit 19 detik — **TEPAT tetapi tidak berguna**. Diulang sadar pada R-K4 (23 detik). Bentuk lain: **R-J3 sengaja ditulis padahal tidak akan pernah dapat diadili** (ADR-036 §6). **Bentuk keempat di S22:** dua ramalan cacah uji yang **tepat persis** justru jatuh pada run yang **gagal**. **Bentuk kelima, dan yang paling buruk, menjadi aturan 60.**
37. (S17, ADR-017–019) **Angka yang benar untuk satu interval tidak berubah nilai ketika dipakai di interval lain — ia berubah MAKNA, dan diam.** Setiap besaran yang berarti "satu hari" wajib diturunkan lewat `lux.kerangka`. **Bentuk baru di S22 akhir:** ambang `invarian_risiko` −1,5R bernilai sama pada 1h dan 4h, tetapi **bentuk ekor yang dihadapinya berbeda** — satu pelanggaran pada H-012, sekurangnya sepuluh pada H-015.
38. (S17) **Dua definisi atas satu dataset selalu dimenangkan oleh yang tidak terlihat.**
39. (S18) **Angka dapat hidup di berkas konfigurasi tanpa pernah masuk ke dalam program.** Cacat kelas kedelapan. **Kode wajib dibandingkan terhadap berkas, bukan hanya dibaca.** **Dipakai terbalik di S22 dan menyelamatkan:** uji H-015 gagal justru karena fixture memakai bawaan `Konfig()` alih-alih `config/lux.yaml`; yang salah **ujinya**.
40. (S18, ADR-024) **Putusan yang dihitung dari separuh kriteria pra-registrasi adalah putusan palsu, dan ia paling berbahaya ketika angkanya menyenangkan.** Cacat kelas kesembilan. **Bentuk terburuknya terbukti nyata di S22 akhir:** `gabung_h014` menghitung putusan tanpa memeriksa gerbang sama sekali (cacat 20, aturan 59).
41. (S18, ADR-024) **Prosa kesimpulan yang dipatok di dalam kode bukan kesimpulan.** Cacat kelas kesepuluh; **ditutup** di `b0e79220`.
42. (S19, ADR-025) **Gerbang yang tidak mungkin lulus tidak menjaga apa pun, dan ia terlihat seperti gerbang yang bekerja.** Cacat kelas kesebelas. **Terulang di S22 lewat pintu lain** (cacat 17, kini dibayar). **Dan berlaku atas alat saya sendiri:** 977 uji hijau berarti kodenya tidak menabrak dirinya sendiri, bukan bahwa ia menjaga sesuatu. Yang menutup cacat 18 adalah **R-L5 dari run sungguhan**, tepat seperti aturan ini menuntut.
43. (S19, ADR-026) **Rencana analisis wajib diperiksa terhadap struktur berkas laporan sebelum dijadwalkan.** Pemasangan hanya mungkin pada **simbol (437)** dan **bulan (73)**.
44. (S19, ADR-028) **Ambang statistik tanpa satuan penarikan bukan ambang.** Cacat kelas kedua belas. Satuan resmi **bulan kalender UTC**. **Dibuktikan di S20:** satu run memberi p 0,003322 per perdagangan dan **0,205980** per bulan.
45. (S19, ADR-028) **`p` sah hanya untuk MENJATUHKAN, tidak untuk MENEGAKKAN.** Dijalankan secara struktural oleh `lux/analisis/berpasangan.py` (`memenuhi_adr015` dipatok `False`) — dan pagar pra-terbang H-015 butir 2 membuktikan patokan itu bertahan bahkan di cabang LULUS.
46. (S19) **Ramalan saya tepat ketika menyangkut kode saya sendiri dan meleset ketika menyangkut pasar** — **difalsifikasi di S21** (R-H1) dan **diperkuat falsifikasinya di S22** (R-G4; muatan STATE terpotong; cacat 18; R-K2; **R-M1 yang meleset dua kali sekaligus tentang run saya sendiri**). **Sebelum membekukan ramalan angka, sebutkan asumsi yang menopangnya dan tandai mana yang belum diperiksa.**
47. (S19–S20, ADR-030) **Alat yang selalu menghasilkan angka tidak menjaga apa pun.** Penggabung **MENOLAK** (kode 4) alih-alih memotong ke irisan atau mengisi nol. Berhenti adalah keluaran yang sah. **Dibuktikan mahal-mahal di S22 akhir:** `gabung_h015` berhenti kode 4 dan membuat run merah; itu **bekerja sebagaimana dirancang**, dan penggabung pendahulunya yang tidak berhenti justru yang cacat.
48. (S20, ADR-030) **Hasil yang menjatuhkan hipotesis wajib berkode keluar 0.** Merah hanya untuk mesin yang rusak. **Pengecualian ADR-037 §7:** `pengaman_mati` tidak kosong → kode bukan nol. Terpasang di `run_h015.main` sebagai kode 3. **Perluasan yang terbukti di S22:** kode 4 (TIDAK DAPAT DINILAI) **juga** sah merah, sebab keadaan itu bukan hipotesis yang jatuh.
49. (S20, ADR-031) **Besaran tidak boleh diukur terhadap satu undian nol.** AS seed 42 (+0,011806R) ~0,98 simpangan baku **di bawah** rerata nol (+0,022916R). Besaran wajib dilaporkan **dua kali**. **S22 memperlihatkan aturan ini tidak cukup: dua pelaporan dapat berbeda TANDA** (aturan 55).
50. (S20, ADR-031) **Ramalan yang terbukti salah alasannya dikoreksi sebagai PROSA di sumbernya, dan jejak bunyi aslinya tidak dihapus.** Dipatuhi di S22 atas prosa ADR-033, atas commit terpotong `56633f80`, atas dokstring `run_h014`, atas rujukan ADR-009/ADR-008, atas koreksi v30 yang terlalu keras, **dan di v33 atas tiga kesalahan saya sendiri: "berkode lengkap", "delapan pagar", dan "ekor tunggal".**
51. (S20) **Sumber dan pagarnya adalah satu commit.** Dipatuhi di `4af21176`, `65916ec6`, `499c64c7`, `4e6a6584`, dan **`29c0f4a0`** (`gabung_h015.py` + 35 ujinya).
52. (S21, ADR-033) **Sel pembanding hanya boleh berbeda pada SATU medan; bila dua, selisihnya bukan pengukuran.** Cacat kelas keempat belas. **Keterbatasannya diketahui:** `medan_berbeda` hanya membandingkan sel A terhadap sel B **di dalam satu hipotesis**. Penambalnya `konfig_audit.selisih_konfig`, **kini terbukti bekerja pada run sungguhan**: H-015 melaporkan selisih terhadap H-013 SS hanya pada `maks_umur_bar` (48 lawan 42), dan selisih itu **dinyatakan**, bukan disembunyikan.
53. (S21, ADR-034) **Ambang hanya boleh dikutip sebagai beku bila dokumen yang membekukannya membekukannya untuk besaran yang sedang diuji; bila tidak, ia ambang BARU dan wajib dinyatakan begitu beserta tanggalnya.** Cacat kelas kelima belas. **Dipatuhi ADR-037 §3.1.**
54. (S21) **Ramalan cacah uji wajib dihitung dari berkas yang benar-benar akan didorong, bukan dari rencana; bila ramalan dan berkas berselisih, yang salah SELALU ramalannya.** `4af21176` meramal 850 dan memberi **855**; `65916ec6` meramal 871 dan memberi **872**.
55. (S22, ADR-035) **Besaran yang tandanya bergantung pada pembobotan bukan besaran.** Cacat kelas keenam belas. Setiap selisih antar sel wajib dilaporkan dalam **empat** bentuk — agregat, rerata per unit penarikan, berbobot, dan median — dan pra-registrasi wajib menyatakan **mana yang mengikat sebelum run**. Dipatuhi ADR-037 §5. **Terulang di H-015:** F − K bulanan **−0,0157R** lawan F − K ekspektasi run **+0,0135R**, berlawanan tanda; keduanya haram dipakai.
56. (S22, ADR-035) **Berkas yang dilahirkan sebuah run dan dibutuhkan sebuah gerbang agar dapat lulus wajib ikut dikomit; daftar `git add` adalah bagian dari gerbang, bukan urusan tata usaha.** Cacat kelas ketujuh belas. **DIBAYAR** di `017e0ac3`; efeknya baru terlihat pada run 4h berikutnya. **Pelajaran tambahan yang mahal:** pembayarannya **tidak boleh** menumpang sentuhan yang memulai run.
57. (S22, ADR-036) **Pengaman risiko wajib hidup di Konfig DASAR, bukan di dalam fungsi pembangun kandidat.** Cacat kelas kedelapan belas. Turunannya: (a) manifes run wajib memuat `asdict(konfig)` **utuh** per sel; (b) pagar kesebandingan wajib membandingkan Konfig sel terhadap Konfig sel pembanding di hipotesis pendahulunya, dan setiap selisih wajib **dinyatakan**. **DITUTUP oleh R-L5:** carry 82 / 27 / 26 pada sel K / F / A.
58. (S22) **Selama mekanisme kelahiran sebuah angka belum diketahui, angka itu diramalkan sebagai BATAS BAWAH, bukan sebagai nilai pasti.** Perluasan aturan 54, bukan kelas cacat baru. Dua ramalan cacah uji berturut-turut meleset ke arah yang sama (850→855, 871→872) sementara cacah `def test_` yang saya tulis terverifikasi benar. Sampai uji ke-17 ditemukan, ramalan cacah uji berbunyi "paling sedikit N" — dipatuhi di R-L4 dan R-N1. **TIDAK DICABUT** oleh ketepatan berturut-turut di S22 (905, 907, 940, 942, 977): semuanya terjadi pada berkas yang saya tulis sendiri, dalam satu sesi, tanpa parametrisasi — itu menghitung, bukan meramal.
59. **(S22, ADR-038) Adjudikator yang tidak memeriksa gerbang bukan adjudikator; ia mesin cetak putusan.** Cacat kelas **kedua puluh**. `gabung_h014.adjudikasi` menghitung putusan H-014 tanpa membaca `gerbang_gagal` sekali pun, padahal kedua sel gagal **tiga** gerbang. `gabung_h015` memeriksanya, dan justru karena itu H-015 berhenti kode 4 alih-alih mengumumkan DITOLAK dengan +0,008903R. **Pengakuan tandingan yang tidak dihaluskan: seandainya saya menulis `gabung_h015` mengikuti preseden `gabung_h014`, cacat ini tidak akan pernah terlihat, dan H-015 hari ini akan diumumkan DITOLAK atas angka yang tidak berhak.** Turunannya: setiap penggabung baru wajib memuat `gerbang_gagal_tak_dimaklumi`, dan pemakluman gerbang hanya sah bila ditulis **sebelum** run **dan** kegagalannya dijamin konstruksi.
60. **(S22, ADR-038) Ramalan atas besaran yang kodenya tidak pernah memancarkan adalah hiasan, bukan disiplin — dan ia lebih buruk daripada ramalan yang meleset.** Cacat kelas **kedua puluh satu**. R-L1 dipra-registrasi berbunyi "sel F menolak long lebih dari 3x lebih sering daripada short"; sesudah `h015_log.md` dan `backtest_h015_f_saringan.md` dibaca utuh, **tidak ada satu medan pun** yang mencatat penolakan saringan menurut arah. Ramalan yang meleset mengajari sesuatu; ramalan yang tak ternilai lolos dari falsifikasi sambil terlihat seperti kejujuran. Turunannya: setiap ramalan wajib menyebut **berkas dan medan** yang akan mengadjudikasinya, dan bila medan itu belum dipancarkan, instrumentasinya ditulis lebih dahulu **atau ramalannya dicabut**.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa. Seluruh komputasi berjalan di GitHub Actions; repo adalah penyimpanan data sekaligus jurnal riset.

---

## 3. Fakta terverifikasi

> Seluruh **besaran** H-011 sampai H-015 ada di **`STATE_LAMPIRAN_ANGKA.md`**, bukan di sini. Bagian ini memuat putusan, sebab, bukti, dan cacat.

### H-015 — TIDAK DAPAT DINILAI (run `30249117960`, ADR-038)

**Bukti:** workflow `.github/workflows/h015.yml` didorong `017e0ac3` pada 08:14:15Z; job `89922832695` **merah** sesudah **8 menit 52 detik**; laporan tetap dikomit **`5b2f70b6`** pada 08:23:08Z lewat `if: always()`. Sembilan pagar pra-terbang lulus. `logs/uji.log` **`977 passed in 3.49s`**. `logs/lantai.log` `lantai=0.004`. `logs/unduh.log` `16` berkas / `157M aset`.

**Putusan verbatim dari `logs/gabung.log`:** `"putusan": "TIDAK DAPAT DINILAI"`, `"dapat_dinilai": true`, `"lulus": false`, `"pengaman_mati": {}`.

**Sebab kemerahan run bukan operasional.** `gabung_h015` keluar berkode **4**, dan langkah "Tegakkan kode keluar penggabung" menerjemahkannya menjadi `exit 1`. Sebab substantifnya: **`invarian_risiko` dan `checksum` merah di ketiga sel**.

| Gerbang | Sifat | Keadaan |
|---|---|---|
| `checksum` | **cacat alat** (cacat 17) | manifes 4h ditulis oleh run itu sendiri; kini ada di `main`, **dibayar** |
| `invarian_risiko` | **substantif** | kerugian terburuk **−11,4736R** lawan ambang −1,5R; **tidak akan sembuh dengan run ulang** |

Urutan sebab checksum kini **terverifikasi dari log**, bukan lagi dugaan: `manifest aset reports/manifest_aset_4h.json (12 berkas interval 4h)` diikuti langsung `checksum: tidak dapat dinilai: manifest baru ditulis pada run ini`.

**Waktu run membatalkan seluruh kerangka "run panjang":** tiga sel hanya 70 s + 74 s + 162 s. Kenaikan `timeout-minutes` 180 → 350 **tidak diperlukan** — kehati-hatian yang tidak terbayar. **Reruns 4h murah.**

### ADR-038 — adjudikasi seluruh jalur DIBEKUKAN, gerbang TIDAK dilunakkan

**Bukti:** `decisions/ADR-038.md`, commit **`26ee44620da3bcba2690edcf0f2178d7c0209210`**.

**Fakta yang memaksanya (tabel utuh di `STATE_LAMPIRAN_ANGKA.md` §1):** `invarian_risiko` **GAGAL** pada H-011 (−470,0612R, 1h, tanpa lantai), H-012 (−21,3131R, 1h), H-013 SS (−11,4736R, 4h), H-014 SSp/SHp, dan ketiga sel H-015 (−11,4736R). **Tidak ada satu pun hasil, pada interval apa pun, yang pernah lolos sebelas gerbang.** R-O3 **TEPAT**, dan lebih luas daripada yang saya ramalkan — saya menduga jalur 4h saja.

Tiga fakta turunan: (a) **−11,4736R identik pada empat sel bersinyal berbeda** → perdagangan itu sifat **data**, bukan sifat sinyal; (b) lantai ADR-014 memperbaiki kerugian terburuk **faktor 41** (470R → 11,47R) dan tetap **7,6 kali** ambang; (c) bentuk ekor 1h dan 4h **berbeda** — H-012 punya **satu** pelanggaran, H-015 sekurangnya **sepuluh**.

**Bukan sebabnya, terverifikasi:** funding (porsi funding 0,0000 pada perdagangan terburuk) dan biaya (0 dari 53.025 perdagangan berbiaya > 1R).

**Putusan ADR-038:** selama `invarian_risiko` merah, **tidak ada putusan atas angka** di jalur mana pun. Putusan DITOLAK H-001…H-014 **tetap** — angka tak terpercaya tidak dapat menyelamatkan hipotesis, hanya gagal menjatuhkannya. Yang **dibatalkan** adalah kewenangan besarannya. **Dilarang permanen:** memaklumi `invarian_risiko`, menggeser ambang 1,5R, menaikkan `min_median_stop_frac` di atas 0,004, membuang perdagangan ekor, dan menghidupkan kembali angka H-011…H-015 dengan gerbang yang direformulasi kelak.

**Run H-015 kedua belum boleh dimulai** — ia hanya akan menghijaukan `checksum` dan menyisakan `invarian_risiko` merah (R-O1). Yang boleh jalan berikutnya hanya **diagnostik** ADR-038 §5.4.

### CACAT KELAS KEDUA PULUH — adjudikator buta gerbang (aturan 59)

**Bukti:** `reports/h014_run.json` (blob `5642b7cf47e3117a1c455095ca1da49caebab66d`) mencatat `gerbang_gagal` SSp `["invarian_risiko","checksum","funding_ekor"]` dan SHp `["entri_acak","invarian_risiko","checksum","funding_ekor"]`. `gabung_h014.adjudikasi` **tidak pernah membaca medan itu**. H-014 diumumkan DITOLAK atas angka yang lahir di balik empat gerbang merah.

**Akibat:** setiap tabel angka H-011…H-015 di berkas ini dan di lampiran **wajib membawa keterangan gerbang mana yang merah**. Dijalankan di v33.

### CACAT KELAS KEDUA PULUH SATU — ramalan tak ternilai (aturan 60)

**Bukti:** `reports/h015_log.md` (blob `7eb5fd1ee4e1f44a6049c5ac37439ae56ca05c36`, 23.125 B) dan `backtest_h015_f_saringan.md` dibaca **utuh**; tidak ada medan penolakan saringan menurut arah. Yang ada hanya `entri ditolak pengaman biaya: 0` — pengaman ADR-014, bukan saringan funding. **R-L1 BELUM DINILAI dan tidak dapat dinilai dari artefak yang dikomit.**

### Pengujian — 977 lulus

Run **`30248730497`** atas `29c0f4a0`, laporan **`abed0edf`**, **`977 passed`**, kode keluar 0. Ditegaskan ulang oleh `logs/uji.log` run H-015: **`977 passed in 3.49s`**.

Rantai merah–hijau S22, dua akar tunggal yang sama (**uji ditulis terhadap model saya tentang kode, bukan terhadap kode** — aturan 42): `499c64c7` → `3 failed, 902 passed` (`TypeError: object of type 'JadwalBoneka' has no len()`) → `a04478a7` → **907**; `4e6a6584` → `3 failed, 937 passed` (`assert ['maks_carry_R'] == []`; `'maks_carry_R' != 'maks_carry_realisasi_R'`; `assert False is True` atas `0.06 - 0.04 = 0.019999999999999997`) → `bccaa55f` → **942**; `29c0f4a0` (`gabung_h015.py` 18.869 B + 35 uji) → **977**.

Dua yang pertama cacat fixture: `dasar()` membangun konfig dari bawaan `Konfig()` (`maks_carry_R = 0.0`) alih-alih dari `config/lux.yaml` yang memuat `maks_carry_R: 0.25` (blob `8a66f15cf559f64dbebb523a29f21357a9300607`). Fixture kini membaca config sungguhan lewat `muat_konfig_h002`, sehingga uji itu menjadi **pagar berdiri**. Yang ketiga bukan cacat dan **tidak** ditambal (ADR-037 §10).

**Adjudikasi cacah uji:** ≥905 → 905 · ≥907 → 907 · ≥940 → 940 · ≥942 → 942 · **R-N1 ≥977 → 977** · **R-L4 (≥884) TERPENUHI**. Semuanya tepat; **aturan 58 tetap berdiri**. **Uji ke-17 masih belum terjelaskan** (872 nyata lawan 871 diramalkan) — **ini memerlukan verifikasi**.

### `gabung_h015.py` — satu-satunya adjudikator yang memeriksa gerbang

**Bukti:** blob `5f96bb4a3d0b01e0febec1610b9fcc94a35ed70e` (18.869 B), commit `29c0f4a0`, 35 uji menyatu (aturan 51). `PUTUSAN_MUNGKIN = ("LULUS","DITOLAK","TIDAK DAPAT DINILAI")` · `MIN_PASANGAN = 2` · `SEL_MENGIKAT = ("F","A")` · `SEL_KONTROL = "K"` · **`GERBANG_DIMAKLUMI = {"A": ("lookahead",)}`** · `KUNCI_RUN_WAJIB = ("sel","audit_konfig","parameter_beku")`. Fungsi `gerbang_gagal_tak_dimaklumi` inilah yang menghasilkan kode 4. **Kode 0 = DITOLAK atau LULUS · 4 = TIDAK DAPAT DINILAI · 2 = pagar · 3 = pengaman mati.**

### `gerbang.py` — sebelas gerbang, aturan pokoknya

**Bukti:** blob `9bddf8d36e3446219c3b234e20b57b1d1bb3dd72`, dibaca utuh. `NAMA_GERBANG = ("forward_fill","buy_and_hold","entri_acak","lookahead","invarian_risiko","funding","overlap","checksum","survivorship","konsentrasi","funding_ekor")`. `gerbang_invarian_risiko(hasil, maks_kerugian_R=1.5)` → `terburuk = min(p.R)`, lulus bila `terburuk >= -maks_kerugian_R`. `LaporanGerbang.semua_lulus` menuntut `len(gerbang) == len(NAMA_GERBANG)`; `susun_laporan` mengisi gerbang yang lupa dijalankan sebagai **gagal**. Aturan pokoknya verbatim: **"gerbang yang tidak dapat dinilai berarti GAGAL, bukan lulus"**.

### H-015 TERDAFTAR — ADR-037, funding sebagai SINYAL

**Bukti:** blob `dfec68a7fbacd0b1c67ba0a0486099ec6d7ee02a` (15.999 B), commit `08e21b3f`, ditulis **sebelum** satu baris kode H-015 ada. Rancangan tiga sel: **K** kontrol · **F** saringan funding · **A** penolakan acak setara per arah per bulan. **Hanya F − A mengikat**; F − K haram meluluskan apa pun sebab funding positif pada **79,1%** periode. Sinyal memakai `statistik_trailing(sampai_ms=t_masuk, jendela_ms=30*HARI_MS)` — kebocoran masa depan mustahil **secara bentuk**. Konstanta beku: `AMBANG_RATE 0,0001` (turunan §3.1) · `MIN_PENAGIHAN 30` · seed `20260727` · `imbalan_R 2,0` · `maks_umur_bar 48` · `lookback {20,55,100}` · `maks_carry_realisasi_R` dan `maks_carry_R` **0,25 di Konfig dasar**.

### CACAT KELAS KESEMBILAN BELAS — `praregistrasi.Kriteria` tidak dapat mengunci kriterianya sendiri

**Terverifikasi dari blob `98a2806e630811167b2f1c826a927b611c9083d0`.** Empat medan: `min_ekspektasi_R`, `min_trade_luar_sampel`, `maks_p_entri_acak`, `min_jendela_positif_rasio`. **Tidak ada medan untuk satuan penarikan, pembobotan mengikat, maupun p bulanan**, dan medan terakhirnya mengunci satuan yang sudah ditinggalkan. `praregistrasi.nilai()` **tidak dipakai** sebagai pemutus H-015. **Utang terbuka.**

### CACAT KELAS KEDELAPAN BELAS — DITUTUP

H-014 berjalan dengan pengaman carry keras **MATI** karena `buat_konfig=None`, sehingga `run_h009.buat_konfig` (`AMBANG_CARRY_KERAS = 0.25`) tidak pernah dipanggil, dan `Konfig` berbawaan `maks_carry_realisasi_R = 0.0`. Bukti pendukung: alasan keluar kedua sel H-014 **tidak memuat kunci `carry` sama sekali**. Ia **melanggar keputusan mengikat ADR-009**.

**Penutupnya: R-L5 TEPAT** — alasan keluar `carry` bercacah **82 / 27 / 26** pada sel K / F / A H-015. Pengaman terbukti hidup di run sungguhan. `konfig_audit` (blob `75a5334620befcd4c85fcfc57220ad82618d33f1`, 16 uji) melaporkan `pengaman_mati []` dan `menghalangi false` pada ketiga sel.

**Yang tidak dihaluskan:** sebuah run riset berjalan dengan pengaman risiko mati, yang mematikannya bukan pemaksimal ekspektasi melainkan saya lewat satu argumen bernilai `None`, dan aturan 12 yang dilanggarnya lahir dari ADR yang sama.

### Papan skor hipotesis — EMPAT BELAS DINILAI, EMPAT BELAS DITOLAK

| ID | Mekanisme | Putusan | Gerbang saat angkanya lahir |
|---|---|---|---|
| H-001b | Donchian polos | DITOLAK | `invarian_risiko` −2,5853 |
| H-002 | Donchian + saringan carry | DITOLAK | — |
| H-003 | pembalikan skor-z | DITOLAK | — |
| H-004 | Donchian + ADX ≥ 30 | DITOLAK | — |
| H-005 | entri retest | DITOLAK | — |
| H-006 | sapuan likuiditas | DITOLAK | — |
| H-007 | imbalan bergrid | DITOLAK | — |
| H-008 | carry keras dilombakan | DITOLAK | pemilih mematikan pengaman, 334/356 |
| H-009 | pengaman dipatok 0,25 | DITOLAK | — |
| H-010 | imbalan 4R terbatas | DITOLAK | `entri_acak` 0,0631 |
| H-011 | pengaman biaya masuk | DITOLAK | **`invarian_risiko` −470,0612R** |
| H-012 | himpunan tertahan sejak 2026-01 | DITOLAK | **`entri_acak` 0,0631 · `invarian_risiko` −21,3131 · `funding_ekor`** |
| H-013 | dekomposisi sinyal/geometri | DITOLAK (p bulan 0,205980) | **`invarian_risiko` −11,4736** |
| H-014 | `pakai_target` satu medan | DITOLAK (rerata bulanan −0,027715R; p 0,375962) | **`invarian_risiko`, `checksum`, `funding_ekor` — dan adjudikatornya tidak memeriksanya (cacat 20)** |
| **H-015** | **funding sebagai sinyal (K/F/A)** | **TIDAK DAPAT DINILAI** | **`invarian_risiko`, `checksum` di ketiga sel** |

### Angka yang HARAM dikutip sebagai kelulusan

`+0,029481R` · `+0,027654R` sebagai besaran yang lulus · `+0,054842R`, `+0,043732R`, `+0,066648R` sebagai kelulusan · `+0,060163R` · `+0,059636R` · p 0,001100 (satuan simbol) · p 0,003322 dan "+2,99 galat baku" · kata "LULUS" di `reports/backtest_h013_kontribusi.md` · prosa R-D3 di `reports/h013b_p.md` · ambang ADR-015 §4.4 sebagai pra-registrasi kaki geometri · "226 jendela / 63,5%" (yang benar 194 / 54,5%) · angka H-014 mana pun dibandingkan langsung dengan H-013 (ADR-036) · angka H-015 mana pun dibandingkan langsung dengan H-014 (ADR-037 §10) · **F − K sebagai dasar kelulusan H-015** · **SELURUH angka run `30249117960`, sebab ketiga selnya gagal gerbang (ADR-038 §5.3)**.

**Larangan permanen:** jangan pernah menyatakan sistem siap diperdagangkan; jangan menambahkan cabang `LULUS` ke H-014; jangan menambal `berpasangan.py`; jangan menjalankan ulang H-014 dengan pengaman carry dinyalakan (aturan 5); jangan menggeser `AMBANG_RATE`, `MIN_PENAGIHAN`, atau seed H-015 sesudah hasil terlihat; jangan melunakkan ambang 0,020R dengan pembulatan; jangan menulis aritmetika funding kedua di luar `funding_model`; jangan menyentuh `lux/strategi/`; **jangan memaklumi `invarian_risiko`; jangan menggeser ambang 1,5R; jangan menaikkan lantai 0,004 agar gerbang hijau (ADR-038 §5.2)**.

### Ambang beku — tidak digeser

lantai 0,004 · pengaman biaya masuk 0,5R · `BATAS_VOID` 20 · potong tanggal 2026-01-01 · selisih antar sel 0,020R · p ≤ 0,05 · ≥300 ulangan · ≥100 trade per sel · `MAKS_RASIO_DATAR` 0,10 · rasio datar 0,30 · ekspektasi 0,05R · **`invarian_risiko` −1,5R (ditegaskan ADR-038)** · `maks_umur_bar` ≤ 168 · `imbalan_R` **tidak** dipatok 8,0 · `maks_carry_realisasi_R` = 0,25 (mekanisme ADR-008, patokan ADR-009, angka ADR-004), wajib hidup di Konfig dasar (aturan 57) · `AMBANG_RATE` 0,0001 dan `MIN_PENAGIHAN` 30 (ADR-037, baru 2026-07-27) · gerbang kesebelas 0,35 / 0,50R / 0,005 (ADR-011).

---

## 4. Asumsi — BUKAN fakta

1. **Sebab kerugian melewati −1,5R belum diketahui.** `config/lux.yaml` memuat `stop_hormati_celah: true`, jadi kerugian > 1R **mungkin** konsekuensi pemodelan yang jujur; cabang mesin yang melaksanakannya belum dibaca baris demi baris. Dugaan tandingan yang belum tersingkirkan: ukuran posisi dihitung dari modal, bukan dari risiko. **Ini memerlukan verifikasi** dan ia pertanyaan terpenting yang terbuka sekarang.
2. **Identitas perdagangan −11,4736R** (simbol, tanggal, harga masuk/stop/keluar) tidak ada di artefak mana pun yang dikomit; hanya dapat diperoleh lewat skrip sisi runner.
3. **Sel A memakan 162 detik lawan K 70 s dan F 74 s** — lebih dari dua kali lipat, belum terjelaskan. Begitu pula `entri acak nyata` A **0,10723R** yang tertinggi dari ketiga sel.
4. **Cabang `runner.py`** yang memancarkan "manifest baru ditulis pada run ini" belum dibaca. Preseden H-011/H-012 (checksum lulus dengan manifes 1h yang sudah ada) menaikkan keyakinan menjadi dugaan berdasar, bukan fakta.
5. **`AH = +0,05817042814276683R`** — sesudah ADR-032 dibatalkan sebagian, penyebabnya tidak diketahui.
6. **Cacah keluar `carry` sel SH** (`reports/backtest_h013_sh_sinyal_horizon.json`) belum dibaca — R-J1 menyatakan > 0.
7. **R-J2 TERJAWAB SEBAGIAN**: `run_wf.py` (blob `c51f91d6…`) tidak memuat `buat_konfig` maupun `jadwal`. Belum dituangkan sebagai adjudikasi resmi.
8. **Asal uji ke-17** pada cacah 872 belum diketahui. Berlaku aturan 58.
9. **Rasio bar datar 1h lawan 4h** — `reports/diag_datar.json`; penolakan 4h seharusnya ≤ 74.
10. **Apakah funding memuat informasi arah** — **masih belum diketahui**, dan run yang seharusnya menjawabnya tidak dapat dinilai. Rerata bulanan F − A +0,008903R tidak boleh dipakai ke arah mana pun.
11. **Bacaan ADR-037 §5 lawan `berpasangan.PEMBATAS`** — pendamaian yang saya usulkan (LULUS = lulus pra-registrasi, `memenuhi_adr015` tetap False) belum diverifikasi. Tidak mendesak: cabang LULUS tak tercapai.
12. **Commit `09ba55450a42482b58a0bd2feb212d0ac697d59b`** (`lux-backfill`, 2026-07-27T06:07:39Z) mendarat pada 06:07 UTC padahal cron berbunyi `'0 2 * * 1'`. Isinya belum dibaca.

---

## 5. Penghalang aktif

- **Tidak ada run yang sedang berjalan.**
- **`invarian_risiko` merah di seluruh jalur.** Ini penghalang utama: tidak ada hipotesis yang dapat diadjudikasi atas angka sampai sebabnya diketahui (ADR-038).
- **Cacat 19 terbuka:** `praregistrasi.Kriteria` tidak dapat menyatakan satuan penarikan, pembobotan mengikat, maupun p bulanan.
- **Cacat 20 terbuka sebagai utang perbaikan:** `gabung_h014` tetap buta gerbang; ia **tidak** ditambal dan H-014 **tidak** dijalankan ulang, tetapi setiap penggabung baru wajib memeriksa gerbang (aturan 59).
- **Cacat 21 terbuka:** R-L1 tidak dapat dinilai; instrumentasi penolakan per arah belum ada.
- **Cacat 17 dibayar, belum terbukti.** Efeknya baru terlihat pada run 4h berikutnya.
- Cacah uji tidak dapat diramal sampai uji ke-17 ditemukan (aturan 58).
- `backfill_daily.yml` berjalan tiap Senin 02:00 UTC tanpa dipicu manusia — dan sekali mendarat 06:07 UTC (asumsi 12).
- `notion_asap.yml` masih tanpa `git pull --rebase --autostash`.
- Tiga kunci `config/lux.yaml` masih tidak dibaca program (lampiran §8).

---

## 6. Tindakan berikutnya (urutan mengikat)

1. **Diagnostik ADR-038 §5.4.** Skrip sisi runner yang memancarkan, untuk setiap perdagangan yang melewati −1,5R: simbol, waktu masuk, harga masuk, harga stop, harga keluar, alasan keluar, dan selisih stop–keluar. **Tidak mengubah putusan apa pun.** Adjudikasi R-P1, R-P2, R-P3. Murah: tidak menuntut backtest penuh.
2. **Jurnal 43.**
3. **Instrumentasi penolakan saringan per arah, atau cabut R-L1** (aturan 60).
4. **Baca cabang `runner.py`** yang memancarkan catatan manifes (asumsi 4).
5. **Jelaskan sel A 162 detik** dan `entri acak nyata` A tertinggi (asumsi 3).
6. **Adjudikasi R-J1** dan **tuangkan R-J2** sebagai adjudikasi resmi.
7. **Temukan uji ke-17** — satu dorongan yang hanya menyentuh `tests/`.
8. **Bayar cacat 19** — medan satuan/pembobotan/p bulanan pada `praregistrasi.Kriteria`.
9. **PROMPT_KELANJUTAN v5** sebelum konteks penuh.
10. **Rasio bar datar 4h**; **baca commit `09ba5545`**; nasib workflow lain; utang audit config aturan 39.

**Run H-015 kedua TIDAK ada dalam daftar ini,** dan itu disengaja (ADR-038 §6).

Nomor ADR bebas berikutnya: **ADR-039**. Jurnal berikutnya: **`journal/2026-07-27-43.md`** (33–42 dipakai).

---

## 7. Disiplin kerja

- Pisahkan fakta (commit / run ID / kutipan) dari asumsi; bila belum terverifikasi, katakan **"Ini memerlukan verifikasi."**
- Ramalan ditulis **sebelum** hasil terlihat, wajib menyebut **berkas dan medan** yang akan mengadjudikasinya (aturan 60), dan yang meleset **tidak dihaluskan**. Cacah uji diramalkan sebagai **batas bawah** (aturan 58).
- **Koreksi pun dapat salah.** Bila sebuah koreksi ternyata terlalu keras, ia diperbaiki sebagai prosa dan kedua kesalahan tetap tercatat (aturan 50).
- **Uji ditulis dari badan fungsi, bukan dari ringkasan API sendiri.**
- **Setiap adjudikator wajib memeriksa gerbang** (aturan 59).
- `STATE.md` diperbarui setiap posisi berubah; satu entri `journal/` per sesi; ADR untuk setiap keputusan yang membatasi masa depan.
- Berkas panjang **dipecah**; setiap muatan dorongan dibaca ulang **dari `main` sesudah dikirim** (aturan 35); besaran tinggal di `STATE_LAMPIRAN_ANGKA.md`, bukan di sini.

---

## 8. Rujukan cepat

Repo `EnVyxS/lux-research`, cabang `main`. Peta repo, inventaris modul, audit workflow, batas alat, dan papan ramalan lama ada di **`STATE_LAMPIRAN.md`**. Seluruh besaran H-011…H-015 ada di **`STATE_LAMPIRAN_ANGKA.md`**.

**Batas alat yang diperbarui:** tidak ada fungsi Actions; log run hanya lewat `reports/*_log.md` yang dikomit. `search_code` nihil. Menyentuh `h014.yml`/`backtest.yml`/`h013b.yml`/`h015.yml` **memulai run**. `tests.yml` 23–30 s. **Run H-015 tiga sel penuh 8 m 52 s — reruns 4h MURAH.** `fapi.binance.com` 451, `data.binance.vision` 200. Runner: python 3.12.13, numpy 2.5.1, pytest 9.1.1, pandas 2.2.3, pyarrow 17.0.0, pyyaml 6.0.2, tanpa scipy/requests, 4 vCPU / 15 GB, batas 6 jam. Rilis `tier-b-v1` id `359778114`, aset 4h 12 berkas / 157.628.619 B.

**Ramalan aktif.** TEPAT: R-N1 (977) · R-L3 · R-L4 · **R-L5** (carry 82/27/26, menutup cacat 18) · **R-O3** (gerbang merah di seluruh jalur). MELESET: R-N2 · **R-L2** (saya meramal DITOLAK, hasilnya TIDAK DAPAT DINILAI — besaran kecil **tidak** menyelamatkan ramalan putusan) · **R-M1** (dua kali sekaligus: run tidak gagal operasional dan tidak panjang) · R-K2 · R-H1 · R-G4. TAK DAPAT DINILAI: **R-L1** (cacat 21). CACAT PENALARAN: **R-O2** (premis "ekor tunggal" runtuh). BELUM: R-M2 · R-O1 · R-B1 paruh kedua · R-J1 · R-J2 · **R-P1** (keluar pada harga pembukaan bar) · **R-P2** (10 ≤ pelanggaran ≤ 500 dari 59.306) · **R-P3** (sekurangnya satu ekor dari simbol yang median `stop_frac`-nya nyaris menyentuh lantai).

Tonggak terakhir: `0dd14098` (v32) → `29c0f4a0` (`gabung_h015` + 35 uji) → `abed0edf` (**977 hijau**) → `16f4af2e` (jurnal 40) → `017e0ac3` (`h015.yml`) → `5b2f70b6` (laporan H-015, run `30249117960` **merah**) → `93d69c08` (jurnal 41) → `3d1d3e37` (jurnal 42) → **`26ee4462` (ADR-038)** → **v33 (berkas ini)**.

**Posisi: 14 hipotesis dinilai, 14 DITOLAK; H-015 dijalankan dan TIDAK DAPAT DINILAI. 60 aturan. 21 kelas cacat. 977 uji. Nol hasil yang pernah lolos sebelas gerbang.**
