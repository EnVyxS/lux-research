# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Arsip rinci ada di **`STATE_LAMPIRAN.md`** dan wajib dibaca bersamanya. Jika sesuatu tidak tercatat di salah satu dari keduanya, anggap belum diketahui.

**Diperbarui:** 2026-07-27 (versi 31) — ditulis sesudah blob v30 (`536258f02d0e414be6a7bb41453b2d6c56f1a102`, commit `11a0cafb`) dibaca **utuh**.

**KOREKSI ATAS KOREKSI — berlaku atas seluruh berkas ini dan atas v30.** v30 menyatakan rujukan "ADR-009" atas pengaman carry **keliru** dan menggantinya dengan ADR-008. **Itu koreksi yang terlalu keras.** Sesudah ADR-008 dan ADR-009 dibaca **utuh** (blob `1d1b9e5781d4a70aebb5829b8c423281bf497ee1` dan `2226847bbb983546f0290593e0b8d14b0c537bce`), yang benar berlapis tiga:

| Lapisan | Dokumen | Kutipan |
|---|---|---|
| **Medan** `Konfig.maks_carry_realisasi_R` dan mekanismenya (dinilai ulang tiap bar, alasan keluar `carry`) | **ADR-008** | "Medan baru `Konfig.maks_carry_realisasi_R`, bawaan **0.0 yang berarti MATI**" |
| **0,25 dipatok sebagai batas risiko yang TIDAK dilombakan** | **ADR-009** | "dikeluarkan dari ruang parameter dan dipatok menyala… Nilai yang dipatok adalah **0,25**" |
| **Asal angka 0,25** | **ADR-004** | "sudah ada di `config/lux.yaml` versi 2 sebagai `risiko.maks_carry_R = 0.25` sejak ADR-004" |

Di ADR-008, 0,25 masih **dilombakan** ({0,0 · 0,25 · 0,50}) dan **kalah 22 lawan 334** — dari kekalahan itulah aturan 12 lahir. Karena `run_h009.AMBANG_CARRY_KERAS` memasang **patokannya**, sebutan "pengaman carry keras ADR-009" di `lux/backtest/funding_ekor.py` **dapat dibela** dan tidak keliru. Berkas lama **tidak** ditulis ulang (aturan 50); jejak kedua kesalahan ada di jurnal 35, 36, dan **37**.

**Cacat alat yang masih tercatat dari v28:** dorongan v28 **pertama** (commit `56633f80`) **terpotong** di tengah bagian 8 — pelanggaran **aturan 35** dalam bentuk ketiga. Mitigasi struktural: arsip rinci dipindah ke `STATE_LAMPIRAN.md` (commit `7869b7d5`). Commit terpotong itu **tidak dihapus dan tidak disembunyikan** (aturan 50).

**Tahap sekarang:** S22 — **H-014 DITOLAK** (run `30221967019`, ADR-035); anomali SH ≠ SH′ **terjawab dari sumber** (ADR-036): kedua sel H-014 berjalan dengan pengaman carry terealisasi **MATI**. Itu **cacat kelas kedelapan belas**, aturan **57**. **H-015 kini TERDAFTAR** lewat **ADR-037** — pra-registrasi ditulis sebelum satu baris kodenya ada. **Empat belas hipotesis dinilai, empat belas ditolak. Nol kandidat bertahan.**

**Cacat 18 kini DIBAYAR SEBAGIAN, bukan tertutup.** `lux/backtest/konfig_audit.py` berikut 16 pengujiannya ada di `main` (commit `65916ec6`, **872 uji**), tetapi **belum ada satu run pun yang memanggilnya** (aturan 42). ADR-037 §7 menjadikan pemanggilan itu **syarat sah** run H-015.

**Beratnya cacat 18 naik (jurnal 37):** ADR-009 memutuskan pengaman itu **dipatok menyala untuk seterusnya**, bukan hanya untuk H-009. H-014 mengembalikannya diam-diam ke bawaan ADR-008 lewat `buat_konfig=None`, jadi ia **melanggar keputusan mengikat ADR-009** — bukan sekadar menjalankan pengaman yang kebetulan mati.

**Tahap berikutnya:** (a) **tulis kode H-015** menurut ADR-037, dengan `konfig_audit` tersambung — itulah penutup cacat 18 yang sebenarnya; (b) tutup cacat 17 dengan **menumpangkan** perbaikan daftar `git add` pada run 4h berikutnya; (c) adjudikasi R-J1.

**Tidak ada run yang sedang berjalan.** Satu-satunya proses berjadwal adalah `backfill_daily.yml`, tiap Senin 02:00 UTC.

---

## 1. Aturan membaca berkas ini

Bagian 3 adalah **fakta**: setiap baris punya bukti berupa commit, run ID, atau kutipan. Bagian 4 adalah **asumsi**: dilarang diperlakukan sebagai fakta. Pemindahan dari 4 ke 3 hanya dengan bukti terlampir.

Aturan yang lahir dari kesalahan nyata, bukan dari teori:

1. **Angka yang lulus gerbang belum tentu benar.** Rasio 1h:4h 4,014 pernah dicatat sebagai uji silang yang lulus, padahal sedang melaporkan bug.
2. **SHA laporan yang tidak berubah bukan tanda pekerjaan masih berjalan.**
3. **Penjelasan yang membuat anomali terasa wajar harus dicurigai lebih keras daripada anomalinya.** **Dipakai dua kali di S22 pada diri sendiri, dan kedua kalinya saya kalah:** pertama "ADR-009 memasang pengamannya, jadi pengamannya milik ADR-009"; lalu koreksinya sendiri, "kalau bukan ADR-009 berarti ADR-008" — keduanya rapi, keduanya tidak lengkap. Yang benar berlapis tiga (lihat kepala berkas). **Bentuk kesalahannya: satu label untuk tiga keputusan yang berbeda lapisan.**
4. **Lihat sebaran mentah sebelum berteori.** Metrik celah funding gagal lima putaran; satu histogram di awal cukup.
5. **Hipotesis yang ditolak tetap ditolak.** Ambang tidak disetel ulang setelah hasil terlihat. **Dipakai di S22:** H-014 **tidak** dijalankan ulang dengan pengaman carry dinyalakan, sekalipun cacat 18 ditemukan sesudahnya, dan sekalipun kemudian diketahui H-014 melanggar ADR-009.
6. (S8) **Percobaan yang informatif ke dua arah lebih berharga daripada percobaan yang dirancang agar berhasil.** **Dipakai sebagai rancangan H-015:** sel A (penolakan acak setara) membuat H-015 informatif meski funding tidak memuat apa-apa.
7. (S9) **Saringan yang membuang perdagangan tidak otomatis membuang perdagangan yang buruk.** **Inti bahaya H-015:** saringan funding membuang long tiga kali lebih sering; itu bukan keunggulan.
8. (S10) **Periksa apakah dugaanmu mungkin secara konstruksi sebelum menjadwalkannya sebagai penelitian.**
9. (S11) **Periksa apakah laporan yang sudah dikomit sudah menjawabnya.**
10. (S11) **Gerbang yang kegagalannya tidak tertulis ke `reports/` adalah titik buta yang menyamar sebagai gerbang.**
11. (S12) **Rerata tidak mengatakan apa pun tentang ekor.** Gerbang nilai ekstrem hanya boleh dibantah dengan nilai ekstrem.
12. (S12) **Batas risiko tidak dilombakan.** Lahir di ADR-009 sesudah pemilih membuang pengaman pada **334 dari 356 jendela**. **Dilanggar tanpa sengaja di S22:** H-014 tidak melombakan batas itu, ia **mematikannya** (cacat 18, aturan 57) — dan mematikan lewat `None` tidak meninggalkan jejak di manifes, sedangkan melombakan meninggalkan jejak.
13. (S12) **Peristiwa yang terlalu jarang tidak dapat dipilih oleh pemilih dalam sampel.**
14. (S12) **Ramalan yang salah lebih murah daripada ramalan yang tidak pernah ditulis.**
15. (S12) **Porsi terhadap nilai bersih bukan ukuran konsentrasi.** Pakai jackknife dan penyebut bruto.
16. (S12) **Proksi yang berkorelasi 0,97 dengan hal lain bukan proksi.**
17. (S12) **Gerbang yang memberi jawaban sama pada dua keadaan bertolak belakang tidak memuat informasi.**
18. (S12) **Angka jumlah yang ditulis tangan hanya boleh ada di satu tempat, yaitu pengujian tripwire.**
19. (S13) **Margin setipis satu satuan resolusi bukan margin.** `entri_acak` H-010 lulus p 0,049505 pada 100 permutasi; pada 300 permutasi mekanisme yang sama memberi **0,0631** dan **gagal**. Dikonfirmasi ulang di H-012: **0,06312292358803986**. Diperluas di S19: R-A4 meramal p ≤ 0,001 dan nyatanya 0,001100. Diperluas lagi di S20: **R-D1 meleset hanya tiga menit dua detik dan tetap dicatat MELESET.** **Dan di S22: R-K2 meleset SATU uji — tetap MELESET.** Tipis bukan alasan.
20. (S13) **Ekspektasi yang naik karena penyebutnya menyusut bukan keunggulan yang membesar.**
21. (S13) **Kecurigaan wajib naik, bukan turun, ketika hasilnya menyenangkan.** Dipakai empat kali di S16–S17 atas run yang terasa terlalu cepat; keempatnya **tak berdasar**. Kelima di S18 atas +0,054842R — **berdasar** (ADR-024). Keenam di S19 atas p simbol 0,001100 — **berdasar** (ADR-028). Ketujuh di S20 atas p per-perdagangan 0,003322 — **berdasar** (ADR-031). Kedelapan di S21 atas +0,029481R — **berdasar** (ADR-033, cacat 14). **Kesembilan di S22 atas agregat +0,027654R — berdasar** (ADR-035, cacat 16). **Bentuk terbaliknya juga nyata:** di S22 saya mencurigai run 2 menit 19 detik sebagai kegagalan dan **salah**.
22. (S13, ADR-014) **Menuntut kesamaan bit pada agregat pecahan adalah pengujian yang menyala pada perilaku yang benar.** Di dalam satu fungsi murni, kesamaan bit tetap sah.
23. (S13, ADR-014) **Pagar yang memastikan masukan identik tidak memastikan masukan sah.** Diperluas di S17: **kesamaan hasil lintas dua run berbeda dilarang diterima tanpa pemeriksaan.** **Dipakai lagi di S22 pada arah sebaliknya, dan berbuah:** SH dan SH′ nominal identik tetapi **tidak** identik (44.614 lawan 44.538); menolak membulatkan selisih 0,17% menjadi derau adalah satu-satunya hal yang membongkar cacat 18.
24. (S13, ADR-014) **Satu simbol dapat mendominasi agregat 438 simbol.**
25. (S13, ADR-014) **Himpunan tertahan habis pada saat pertama kali dilihat.**
26. (S13, ADR-014) **Cacat yang membalik tanda hasil tidak boleh diperbaiki di dalam hipotesis yang sama.** **Dipakai di S22:** cacat 18 tidak diperbaiki di dalam H-014; perbaikannya hidup di H-015.
27. (S13, ADR-014) **Eksperimen yang tercemar tidak informatif ke arah mana pun.** **Diuji di S22 dan TIDAK berlaku pada H-014:** kedua sel salah **secara identik**, sehingga selisih antar sel tetap mengukur satu medan (ADR-036 §4).
28. (S13, ADR-014) **Saringan yang menolak entri juga menolak saat pemilihan.** Terbukti kuantitatif di H-012: hanya **62** entri ditolak pengaman. **Terbukti kedua kali di S21:** `maks_umur_bar` ikut menolak **entri** lewat proyeksi carry di `_boleh_masuk`.
29. (S14) **Pra-registrasi wajib diperiksa terhadap apa yang benar-benar dapat dihitung dari laporan.**
30. (S14) **Kriteria utama dihitung dari berkas laporan yang dikomit, bukan dari nilai yang beredar di memori run.**
31. (S15) **Pagar yang menyalin baris dari kode yang dijaganya tidak menjaga apa pun.** **Dipakai sebagai rancangan di S22:** `konfig_audit` sengaja **tidak** memuat angka 0,25; daftar pengaman wajib datang dari pemanggil.
32. (S15) **Aritmetika yang hidup di dalam `main` tidak dapat diuji.**
33. (S15) **Setiap langkah workflow wajib `tee` ke `logs/` dan seluruh `logs/` disalin ke `reports/` dengan `if: always()`.**
34. (S15) **Lingkungan pagar wajib memasang dependensi yang sama dengan `tests.yml`.**
35. (S16) **Muatan tulis yang panjang wajib dibaca ulang utuh sebelum dikirim, dan jumlah pengujian dicacah dari muatan yang benar-benar dikirim, bukan dari rencana.** **DILANGGAR DI S22 dalam bentuk ketiga:** muatan `STATE.md` v28 pertama **terpotong** dan dikomit terpotong (`56633f80`). Mitigasi: berkas panjang dipecah, dan setiap dorongan panjang **dibaca ulang dari `main` sesudah dikirim** — dijalankan atas `65916ec6`, v30, **ADR-037**, dan versi ini.
36. (S16, ADR-016) **Ramalan yang dijamin benar oleh konstruksi bukan ramalan.** **Dibuktikan telanjang di S22:** R-H3 meramal run selesai di bawah 25 menit; kenyataannya 2 menit 19 detik — **TEPAT tetapi tidak berguna**. Diulang sadar pada R-K4 (23 detik). Bentuk lain: **R-J3 sengaja ditulis padahal tidak akan pernah dapat diadili** (ADR-036 §6). **Dipakai di muka pada H-015:** R-L1 ditandai tak bernilai **sebelum** run.
37. (S17, ADR-017–019) **Angka yang benar untuk satu interval tidak berubah nilai ketika dipakai di interval lain — ia berubah MAKNA, dan diam.** Setiap besaran yang berarti "satu hari" wajib diturunkan lewat `lux.kerangka`.
38. (S17) **Dua definisi atas satu dataset selalu dimenangkan oleh yang tidak terlihat.**
39. (S18) **Angka dapat hidup di berkas konfigurasi tanpa pernah masuk ke dalam program.** Cacat kelas kedelapan. **Kode wajib dibandingkan terhadap berkas, bukan hanya dibaca.**
40. (S18, ADR-024) **Putusan yang dihitung dari separuh kriteria pra-registrasi adalah putusan palsu, dan ia paling berbahaya ketika angkanya menyenangkan.** Cacat kelas kesembilan.
41. (S18, ADR-024) **Prosa kesimpulan yang dipatok di dalam kode bukan kesimpulan.** Cacat kelas kesepuluh; **ditutup** di `b0e79220`.
42. (S19, ADR-025) **Gerbang yang tidak mungkin lulus tidak menjaga apa pun, dan ia terlihat seperti gerbang yang bekerja.** Cacat kelas kesebelas. **Terulang di S22 lewat pintu lain** (cacat 17). **Dan berlaku atas alat baru saya sendiri:** `konfig_audit` belum dipanggil satu run pun.
43. (S19, ADR-026) **Rencana analisis wajib diperiksa terhadap struktur berkas laporan sebelum dijadwalkan.** Pemasangan hanya mungkin pada **simbol (437)** dan **bulan (73)**.
44. (S19, ADR-028) **Ambang statistik tanpa satuan penarikan bukan ambang.** Cacat kelas kedua belas. Satuan resmi **bulan kalender UTC**. **Dibuktikan di S20:** satu run memberi p 0,003322 per perdagangan dan **0,205980** per bulan.
45. (S19, ADR-028) **`p` sah hanya untuk MENJATUHKAN, tidak untuk MENEGAKKAN.** Dijalankan secara struktural oleh `lux/analisis/berpasangan.py` (`memenuhi_adr015` dipatok `False`).
46. (S19) **Ramalan saya tepat ketika menyangkut kode saya sendiri dan meleset ketika menyangkut pasar** — **difalsifikasi di S21** (R-H1) dan **diperkuat falsifikasinya di S22** (R-G4; muatan STATE terpotong; cacat 18; R-K2). **Sebelum membekukan ramalan angka, sebutkan asumsi yang menopangnya dan tandai mana yang belum diperiksa.**
47. (S19–S20, ADR-030) **Alat yang selalu menghasilkan angka tidak menjaga apa pun.** Penggabung **MENOLAK** (kode 4) alih-alih memotong ke irisan atau mengisi nol. Berhenti adalah keluaran yang sah.
48. (S20, ADR-030) **Hasil yang menjatuhkan hipotesis wajib berkode keluar 0.** Merah hanya untuk mesin yang rusak. **Pengecualian yang dinyatakan ADR-037 §7:** `pengaman_mati` tidak kosong → kode keluar bukan nol, sebab itu mesin yang rusak, bukan hipotesis yang jatuh.
49. (S20, ADR-031) **Besaran tidak boleh diukur terhadap satu undian nol.** AS seed 42 (+0,011806R) ~0,98 simpangan baku **di bawah** rerata nol (+0,022916R). Besaran wajib dilaporkan **dua kali**. **S22 memperlihatkan aturan ini tidak cukup: dua pelaporan dapat berbeda TANDA** (aturan 55).
50. (S20, ADR-031) **Ramalan yang terbukti salah alasannya dikoreksi sebagai PROSA di sumbernya, dan jejak bunyi aslinya tidak dihapus.** Dipatuhi di S22 atas prosa ADR-033, atas commit terpotong `56633f80`, atas dokstring `run_h014`, atas rujukan ADR-009/ADR-008, **dan atas koreksi saya sendiri yang terlalu keras di v30** — diperbaiki di kepala berkas ini, bukan dengan menulis ulang v30.
51. (S20) **Sumber dan pagarnya adalah satu commit.** Dipatuhi di `4af21176` dan di `65916ec6`.
52. (S21, ADR-033) **Sel pembanding hanya boleh berbeda pada SATU medan; bila dua, selisihnya bukan pengukuran.** Cacat kelas keempat belas. **Keterbatasannya kini diketahui:** `medan_berbeda` hanya membandingkan sel A terhadap sel B **di dalam satu hipotesis**, sehingga medan yang salah **secara identik di kedua sel** tidak terlihat. Penambalnya `konfig_audit.selisih_konfig`, **belum tersambung**.
53. (S21, ADR-034) **Ambang hanya boleh dikutip sebagai beku bila dokumen yang membekukannya membekukannya untuk besaran yang sedang diuji; bila tidak, ia ambang BARU dan wajib dinyatakan begitu beserta tanggalnya.** Cacat kelas kelima belas. **Dipatuhi ADR-037 §3.1:** `AMBANG_RATE = 0,0001` dinyatakan sebagai ambang **baru**, lengkap dengan turunan konstruksinya.
54. (S21) **Ramalan cacah uji wajib dihitung dari berkas yang benar-benar akan didorong, bukan dari rencana; bila ramalan dan berkas berselisih, yang salah SELALU ramalannya.** `4af21176` meramal 850 dan memberi **855**; `65916ec6` meramal 871 dan memberi **872**.
55. (S22, ADR-035) **Besaran yang tandanya bergantung pada pembobotan bukan besaran.** Cacat kelas keenam belas. Setiap selisih antar sel wajib dilaporkan dalam **empat** bentuk — **agregat**, **rerata per unit penarikan**, **berbobot**, dan **median** — dan pra-registrasi wajib menyatakan **mana yang mengikat sebelum run**. **Dipatuhi ADR-037 §5:** yang mengikat adalah rerata bulanan tak berbobot.
56. (S22, ADR-035) **Berkas yang dilahirkan sebuah run dan dibutuhkan sebuah gerbang agar dapat lulus wajib ikut dikomit; daftar `git add` adalah bagian dari gerbang, bukan urusan tata usaha.** Cacat kelas ketujuh belas.
57. (S22, ADR-036) **Pengaman risiko wajib hidup di Konfig DASAR, bukan di dalam fungsi pembangun kandidat.** Cacat kelas kedelapan belas. Turunannya: (a) manifes run wajib memuat `asdict(konfig)` **utuh** per sel; (b) pagar kesebandingan wajib membandingkan Konfig sel terhadap Konfig sel pembanding di **hipotesis pendahulunya**, dan setiap selisih wajib **dinyatakan**, bukan dilarang. Pengaman yang dimaksud: **mekanisme ADR-008, patokan 0,25 ADR-009, angka asal ADR-004** (lihat kepala berkas).
58. (S22) **Selama mekanisme kelahiran sebuah angka belum diketahui, angka itu diramalkan sebagai BATAS BAWAH, bukan sebagai nilai pasti.** Perluasan aturan 54, dan **bukan** kelas cacat baru. Dua ramalan cacah uji berturut-turut meleset ke arah yang sama (850→855, 871→872) sementara cacah `def test_` yang saya tulis terverifikasi benar. Sampai uji ke-17 ditemukan, ramalan cacah uji berbunyi "paling sedikit N" — dipatuhi di R-L4.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa. Seluruh komputasi berjalan di GitHub Actions; repo adalah penyimpanan data sekaligus jurnal riset.

---

## 3. Fakta terverifikasi

### H-015 TERDAFTAR — ADR-037, pra-registrasi funding sebagai SINYAL

**Bukti:** `decisions/ADR-037.md`, blob **`dfec68a7fbacd0b1c67ba0a0486099ec6d7ee02a`** (15.999 B), commit **`08e21b3fd6e940f180d4ef472a7a1a5b14b95324`**, dibaca ulang utuh dari `main` sesudah didorong (aturan 35). Ditulis **sebelum** satu baris kode H-015 ada.

**Modul yang dibaca utuh sebelum ADR ditulis** (aturan 8, 29, 43): `lux/funding_model.py` (`ef867388…`), `lux/funding.py` (`7e6af69a…`), `lux/backtest/funding_ekor.py` (`b21fedce…`), `lux/strategi/breakout_atr.py` (`3ac5d3bf…`), `lux/praregistrasi.py` (`98a2806e…`), `lux/backtest/engine.py` (`81c1db8a…`), ADR-008, ADR-009.

**Rancangan, tiga sel:** **K** kontrol tanpa saringan · **F** dengan saringan funding · **A** penolakan **acak** yang menyamai cacah penolakan F **per arah per bulan**. **Hanya F − A yang mengikat putusan**; F − K dilaporkan tetapi tidak dapat meluluskan apa pun — sebab funding positif pada **79,1%** periode, sehingga saringan apa pun condong membuang long, dan kecondongan arah bukan keunggulan funding.

**Sinyal:** `rerata, n = jadwal[s].statistik_trailing(sampai_ms=t_masuk, jendela_ms=30*HARI_MS)`; entri ditolak bila `d × rerata > AMBANG_RATE` atau `n < MIN_PENAGIHAN`. `statistik_trailing` dipilih karena batas atas jendelanya adalah waktu masuk itu sendiri dan **tidak ada argumen yang dapat menggesernya maju** — kebocoran masa depan mustahil **secara bentuk**, bukan karena kehati-hatian.

**Konstanta beku:** `AMBANG_RATE = 0,0001` (turunan konstruksi §3.1: 0,125R ÷ lebar stop 3,61% ÷ 48 penagihan = 0,000094, dibulatkan) · `MIN_PENAGIHAN = 30` · `SEED_ACAK_H015 = 20260727` · `imbalan_R` 2,0 · `maks_umur_bar` 48 · `pakai_target` True · `lookback` {20,55,100} · **`maks_carry_realisasi_R` 0,25 dan `maks_carry_R` 0,25, keduanya di Konfig dasar** · horizon 4h. Ruang pencarian **3 kombinasi** × 3 sel.

**Kriteria mengikat (§5):** satuan **bulan kalender UTC**; pembobotan mengikat **rerata bulanan tak berbobot**, keempat pembobotan tetap dilaporkan; LULUS menuntut rerata bulanan (F−A) ≥ +0,020R, p tanda bulanan ≤ 0,05, ≥100 trade tiap sel, ≥300 ulangan, sebelas gerbang lulus tiap sel, dan `pengaman_mati` kosong. `PUTUSAN_MUNGKIN = ("LULUS", "DITOLAK", "TIDAK DAPAT DINILAI")` — cabang LULUS **ada** karena H-015 didaftarkan sebelum datanya dilihat; larangan menambah LULUS tetap berlaku atas H-014.

**Ramalan, ditulis sebelum run:** R-L1 (F menolak long >3× short — **ditandai tak bernilai, dijamin konstruksi**) · **R-L2 H-015 DITOLAK** · R-L3 |F−A| < |F−K| · R-L4 cacah uji **paling sedikit 884** · **R-L5 keluar `carry` bukan nol pada ketiga sel** — bila R-L5 gagal, run batal sebagai dasar putusan apa pun dan cacat 18 kembali terbuka penuh.

### CACAT KELAS KESEMBILAN BELAS — berkas pra-registrasi tidak mampu mengunci kriterianya sendiri (ADR-037 §8)

**Terverifikasi dari `lux/praregistrasi.py` blob `98a2806e630811167b2f1c826a927b611c9083d0`.** `Kriteria` memuat empat medan: `min_ekspektasi_R`, `min_trade_luar_sampel`, `maks_p_entri_acak`, `min_jendela_positif_rasio`. **Tidak ada medan untuk satuan penarikan, pembobotan mengikat, maupun p bulanan.** Medan terakhirnya bahkan mengunci satuan yang **sudah ditinggalkan** — jendela walk-forward, sedangkan aturan 44 dan ADR-031 §5 memindahkan satuan ke bulan kalender.

Akibatnya: **berkas yang satu-satunya tugasnya membuat kriteria mustahil diubah, tidak mampu menyatakan kriteria yang sekarang mengikat.** `nilai()` akan memutus menurut aturan tiga belas hipotesis lalu.

**Keputusan H-015:** kriteria mengikat adalah ADR-037 §5; **`praregistrasi.nilai()` tidak dipakai sebagai pemutus**; berkas hipotesis tetap didaftarkan lewat `simpan()` dan `pernyataan` wajib memuat string `"ADR-037 §5 mengikat"` beserta sidik ADR. **Utang terbuka:** `Kriteria` perlu medan satuan, pembobotan, dan p bulanan berikut pengujiannya — **bukan** pekerjaan run H-015.

### CACAT KELAS KEDELAPAN BELAS — H-014 berjalan dengan pengaman carry keras **MATI** (ADR-036, aturan 57)

**Anomali SH ≠ SH′ TERJAWAB.** Bukan derau float. Rantainya dibaca dari lima berkas sumber:

| Berkas | Blob |
|---|---|
| `lux/backtest/run_h014.py` | `dd2429f03d60c799535188fdccf736c58ec30c33` |
| `lux/backtest/run_h013.py` | `239b88d0b048b1ccc659cbb70fc15013172096b4` |
| `lux/backtest/run_h009.py` | `aee7409339187554a60e727f59b275362bbeedc9` |
| `lux/backtest/run_h002.py` | `8bf480da315eb04eba08d5721ea747b13e6a88df` |
| `lux/backtest/engine.py` | `81c1db8ad147dae149795db1d1166476efd210a9` |

- H-013 memakai `buat_konfig=buat_konfig_sel(sel)` → `run_h009.buat_konfig` → `replace(dasar, imbalan_R=…, maks_carry_realisasi_R=AMBANG_CARRY_KERAS)` dengan **`AMBANG_CARRY_KERAS = 0.25`**.
- H-014 memakai **`buat_konfig=None`**, jadi fungsi itu **tidak pernah dipanggil**.
- `run_h002.muat_konfig_h002` membangun `Konfig` dari **delapan** kunci, dan `maks_carry_realisasi_R` **bukan** salah satunya.
- **Terverifikasi dari `engine.py`:** `Konfig` adalah `@dataclass(frozen=True)` dan **`maks_carry_realisasi_R` berbawaan `0.0`** — keadaan MATI.
- **Terverifikasi dari ADR-009 (baru di v31):** pengaman itu **dipatok menyala untuk seterusnya**, bukan hanya untuk H-009. Maka H-014 **melanggar keputusan mengikat ADR-009**.

| Medan | SH (H-013) | SH′ (H-014) |
|---|---|---|
| `pakai_target` | False | False |
| `maks_umur_bar` | 48 | 48 |
| `imbalan_R` | 2,0 | 2,0 |
| **`maks_carry_realisasi_R`** | **0,25 — menyala** | **0,0 — MATI** |

**Bukti pendukung dari laporan run:** alasan keluar kedua sel H-014 **tidak memuat kunci `carry` sama sekali**.

**Mengapa dua pagar tidak menangkapnya:** `medan_berbeda` hanya melihat sel A lawan sel B **di dalam** H-014; `manifes["parameter_beku"]` mencatat sebelas butir pilihan, **bukan** seluruh `Konfig`.

**Akibat terhadap putusan (ADR-036 §4):** **H-014 tetap DITOLAK, ADR-035 tidak dicabut.** Kedua sel salah **secara identik**, jadi SS′ − SH′ tetap mengukur satu medan (aturan 52 utuh); p bulanan 0,375962 dan rerata bulanan −0,027715R jauh dari ambang ke arah yang salah; **tidak ada run ulang** (aturan 5, 26). Yang gugur adalah **kesebandingan lintas hipotesis**. Yang tidak dihaluskan: **sebuah run riset berjalan dengan pengaman risiko mati, yang mematikannya bukan pemaksimal ekspektasi melainkan saya lewat satu argumen bernilai `None`, dan aturan 12 yang dilanggarnya lahir dari ADR yang sama.**

### Pembayaran sebagian cacat 18 — modul `konfig_audit` (commit `65916ec6`)

**Ada di `main`, terverifikasi, dan belum menjaga apa pun.**

- Empat fungsi: `konfig_penuh`, `selisih_konfig`, `pengaman_mati`, `laporan_kesebandingan`.
- **Selisih tidak menghalangi run; pengaman mati menghalangi.**
- Modul **tidak memuat angka 0,25**; daftar pengaman wajib datang dari pemanggil (aturan 31).
- `tests/test_konfig_audit.py` blob `77f76e69d6dac4d9b8dc9546b6e45672a0a40e04`, **16 uji**, dua di antaranya membangun ulang pasangan Konfig SH dan SH′ sebagai uji regresi cacat 18.
- **Penyimpangan yang dinyatakan:** ADR-036 keputusan 2 dan 3 menyebut `run_h014.py`; alat ini lahir sebagai modul terpisah. Dicatat di jurnal 35 §2.
- **Utang tersisa:** penyambungan ke runner. ADR-037 §7 menjadikannya syarat sah run H-015: panggil `laporan_kesebandingan` dengan `pengaman_wajib = {"maks_carry_realisasi_R": 0.25, "maks_carry_R": 0.25}`, taruh `asdict(konfig)` utuh di manifes, berhenti berkode bukan nol bila `pengaman_mati` tidak kosong.

### Pengujian — 872 lulus, dan satu di antaranya belum terjelaskan

**Terverifikasi:** run `30243626098` atas commit `65916ec6`, laporan dikomit `61504ef6`, `Kode keluar: 0`, **`872 passed in 3.19s`**. `tests.yml` memanggil `python -m pytest tests -q --tb=short` — polos, tanpa doctest, hanya lintasan `tests/` (blob `73f55a703ecf856cdec2498645e1c4137e155fc5`).

**Terverifikasi juga:** sejak cacah 855, hanya **dua** commit menyentuh `tests/` (`4af21176`, `65916ec6`), sedangkan berkas uji baru memuat **16** fungsi `def test_`. Selisih **+17**, jadi **satu uji lahir tanpa ditulis**. Enam berkas sudah dibaca dan bersih dari parametrisasi atas daftar berkas. **Sumbernya belum diketahui — ini memerlukan verifikasi**; berlaku aturan 58.

### H-014 — DITOLAK (ADR-035, run `30221967019`)

**Bukti:** pemicu `52c64ac576e81883cd516316437edfff1d596ac4` pada 2026-07-26T21:52:25Z; laporan dikomit **`603477ce8b9b55e2a67d9a7a0e7c3c843c2be379`** pada 21:54:44Z; log blob **`03e0c35c54134d9906515e2df515eb5f1c939b6c`**. Runner melaporkan **`855 passed in 2.98s`** sebelum satu berkas diunduh. Delapan butir pagar pra-terbang lulus **pada percobaan pertama**. 157 MB aset 4h terunduh, 438 simbol dimuat, **437 layak**. Sel SS′ **56,9 s**, sel SH′ **52,6 s**, seluruh run **2 menit 19 detik**.

| Syarat (BARU, dibekukan 2026-07-27, ADR-034) | Nilai | Ambang | Terpenuhi |
|---|---|---|---|
| rerata selisih bulanan SS′ − SH′ | **−0,027715128544164157R** | ≥ 0,020R | **TIDAK** |
| p uji tanda berpasangan bulanan | **0,37596240375962403** | ≤ 0,05 | **TIDAK** |
| pasangan bulan | 73 | ≥ 2 | ya |
| trade sel A / sel B | 59.324 / 44.538 | ≥ 100 | ya |

`p` dihitung dengan m 3759, ulangan 10000, seed 20260727. Bootstrap 95% **[−0,09067851377334449, +0,029103950604927244]** (seed 20260728) — **memuat nol**. `memenuhi_adr015` **false**. Penggabung keluar berkode **0** (aturan 48).

| Sel | `pakai_target` | `maks_umur_bar` | Trade | Ekspektasi R | Jendela positif | p entri acak | Gerbang gagal |
|---|---|---|---|---|---|---|---|
| SS′ | **True** | 48 | **59.324** | **+0,06725203533326735** | 2229 / 4082 | 0,016611295681063124 | `invarian_risiko`, `checksum`, `funding_ekor` |
| SH′ | **False** | 48 | **44.538** | **+0,03959765698185091** | 1982 / 4082 | 0,21926910299003322 | `entri_acak`, `invarian_risiko`, `checksum`, `funding_ekor` |

Alasan keluar SS′: `stop` 33.748 · `target` 18.667 · `umur` 5.174 · `akhir_data` 1.735. SH′: `stop` 28.013 · `umur` 14.426 · `akhir_data` 2.099. **Nol `carry` pada keduanya** — lihat cacat 18, dan bandingkan R-L5.

SS′: 309 untung / 128 rugi, drop-1 **0,06639R** (retensi **0,9872**), drop-22 0,05419R, median simbol +0,06789R, porsi bruto teratas 0,0139 (SANDUSDT), funding maks 0,8285R, std **1,37827R**, galat baku 0,005659R (+3,05 SE), parameter {55:836, 20:1711, 100:1535}, sidik `197c10e3f0d2`.
SH′: 234 untung / 203 rugi, drop-1 **0,03583R** (retensi **0,9047**), drop-22 0,01225R, median simbol +0,02710R, porsi bruto teratas 0,0431 (VELVETUSDT), funding maks **2,9000R**, std **2,20818R**, galat baku 0,010463R (−0,99 SE), parameter {55:1073, 20:1995, 100:1014}, sidik `5721a88e59eb`. 73 bulan pada kedua sel.

**Kode H-014:** commit **`4af2117639c15ace7ba4a442ce2841091a1e25fb`**; `reports/tests.md` blob **`94e5096e2f989edc13d3f1a95daa84b6b512331e`**, run **`30221837845`**, **`855 passed in 3.06s`**. Workflow `h014.yml` commit **`52c64ac5`**: `timeout-minutes: 180`, delapan butir pagar pra-terbang — **tetapi daftar `git add`-nya cacat** (cacat 17).

**H-014 tidak pernah dapat LULUS, dan itu dipra-registrasi** (ADR-034 §2): `PUTUSAN_MUNGKIN = ("DITOLAK", "TIDAK DAPAT DINILAI")`.

### CACAT KELAS KEENAM BELAS — tanda besaran bergantung pada pembobotan (ADR-035 §2, aturan 55)

| Cara membobot | Nilai | Tanda |
|---|---|---|
| selisih **agregat** | **+0,027654378351416438R** | **POSITIF** |
| **rerata** selisih bulanan | **−0,027715128544164157R** | **NEGATIF** |
| rerata **berbobot trade** | −0,012499029724652699R | NEGATIF |
| **median** selisih bulanan | +0,03495217650445759R | POSITIF |
| fraksi bulan positif | 0,5616438356164384 | — |

Dua angka pertama **hampir sama besar dan berlawanan tanda**. **Bila pembobotan bebas dipilih, H-014 melewati ambang besaran dengan agregat +0,0277R.** Yang mencegahnya bukan kehati-hatian saya melainkan `gabung_h014.adjudikasi` membaca `rerata_selisih`, dan kode itu dikomit **sebelum** satu angka pun ada. **p 0,376 menjatuhkan hipotesis pada pembobotan mana pun.**

### CACAT KELAS KETUJUH BELAS — gerbang yang saya sendiri buat mustahil lulus (ADR-035 §3, aturan 56)

Log run mencetak, verbatim:

> `manifest aset reports/manifest_aset_4h.json (12 berkas interval 4h)`
> `checksum: tidak dapat dinilai: manifest baru ditulis pada run ini`

Itu **separuh pertama R-B1 TEPAT**. Tetapi `reports/manifest_aset_4h.json` **tidak ada di `main`**: daftar `git add` di `h014.yml` tidak menambahkannya. Terverifikasi dari `runner.py` (blob `4ce34a3c`): gerbang itu hanya lulus bila berkasnya **bertahan** di `main`.

**Keputusan:** perbaikan **menumpang run 4h berikutnya** — yaitu run H-015 — tetapi **tidak digabung** ke dalam commit kodenya. Sampai itu, **kegagalan `checksum` pada 4h wajib dibaca sebagai cacat alat** (aturan 42).

### KLAIM ADR-033 DIBATALKAN SEBAGIAN — umur 42 lawan 48 bukan sebab utama (ADR-035 §4)

| Sel | Umur | Trade |
|---|---|---|
| SS (H-013) | 42 | 60.018 |
| **SS′ (H-014)** | **48** | **59.324** |
| SH (H-013) | 48 | 44.614 |
| **SH′ (H-014)** | **48** | **44.538** |

Efek menaikkan umur 42 → 48 pada sel bertarget: **−694 perdagangan, −1,2%**. Jarak antar sel dengan umur **disetarakan**: **+33,2%** — hampir seluruhnya `pakai_target`. **Aturan 52 tidak dibatalkan** dan **+0,029481R tetap haram dikutip**. **Catatan ADR-036:** baris SH lawan SH′ kini diketahui **juga** memuat efek pengaman carry yang mati.

### CACAT KELAS KEEMPAT BELAS dan KELIMA BELAS (ADR-033, ADR-034)

**Keempat belas:** `run_h013.umur_sel` memberi 42 untuk sel bertarget dan 48 untuk sel tanpa target, jadi **SS − SH mencampur dua medan**. **Putusan H-013 tidak berubah** — ia mati pada p bulanan 0,205980 kaki **sinyal**. Yang berubah: **`+0,029481R` tidak mengukur apa yang namanya sebut**.

**Kelima belas:** ADR-032 dan ADR-033 mengutip ambang ADR-015 §4.4 sebagai beku untuk kaki **geometri**, padahal §4.4 membekukannya untuk kaki **sinyal**. Ambang H-014 karena itu **BARU**, dibekukan 2026-07-27.

### ADR-032 DIBATALKAN SEBAGIAN (ADR-033 §2)

Keberatan B ADR-032 ("tanpa stop, penyebut R adalah jarak nosional") **SALAH**: `engine.jalankan` mengevaluasi `kena_stop` **tanpa syarat**, `pakai_target=False` hanya mematikan target, jadi penyebut R **dibangun identik**. Akibatnya **`AH = +0,05817042814276683R` kembali TIDAK TERJELASKAN — ini memerlukan verifikasi**. **R-F1…R-F5 DIBATALKAN.**

### JALUR B — H-013 DITOLAK (ADR-031, run `30217516013`)

Pemicu `97b36c19`; sepuluh pecahan 20:13:43Z–20:28:15Z; laporan p `1d746879`. Seed utuh 300 pada [0,300), 73 bulan pada SS, keluar 0.

| Syarat ADR-015 §4.4 | Nilai | Ambang | Terpenuhi |
|---|---|---|---|
| besaran SS − AS | **+0,054842R** | 0,020R | ya |
| **p satuan bulan** | **0,205980** | 0,05 | **TIDAK** |
| ulangan | 300 | 300 | ya |
| trade terkecil antar sel | 54.812 | 100 | ya |

Sebaran nol 300 seed: rerata **+0,022916R** · sd **+0,011377R** · rentang **−0,004632R … +0,057394R** · sel SS +0,066648R. p satuan perdagangan 0,003322 — **haram** menegakkan (aturan 45). Jalur A membenarkan dengan mesin berbeda: p bulanan berpasangan **0,365363**, bootstrap memuat nol.

**Cacat kelas ketiga belas (ADR-031):** +0,054842R dihitung terhadap **satu** sel nol seed 42; terhadap rerata nol ia **+0,043732R**. Dibayar di sumber lewat `6ae83062` dan `5bd73fbf`. `reports/h013b_p.md` **tetap** memuat prosa R-D3 yang salah (aturan 50).

### JALUR A — keberartian jatuh pada satuan bulan

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

**SH lawan AH:** simbol — rerata −0,010358R, berbobot −0,023331R, agregat −0,021004R, fraksi 0,4760, p 0,777622. Bulan — rerata −0,029960R, berbobot −0,028521R, median −0,072371R, fraksi 0,4110, **p 0,280372**. **Anomali SH < AH turun pangkat menjadi derau.** R-A1…R-A6: empat tepat, **R-A4 MELESET**, **R-A5 MELESET JAUH**.

### Papan skor hipotesis — EMPAT BELAS DINILAI, EMPAT BELAS DITOLAK

| ID | Mekanisme | Ekspektasi R | Putusan |
|---|---|---|---|
| H-001b | Donchian polos | 0,03086 | DITOLAK (`invarian_risiko` −2,5853) |
| H-002 | Donchian + saringan carry | 0,03159 | DITOLAK |
| H-003 | pembalikan skor-z | −0,24782 | DITOLAK |
| H-004 | Donchian + ADX ≥ 30 | −0,01818 | DITOLAK |
| H-005 | entri retest | −0,03571 | DITOLAK |
| H-006 | sapuan likuiditas | −0,13449 | DITOLAK |
| H-007 | imbalan bergrid | — | DITOLAK |
| H-008 | saringan rezim / carry keras dilombakan | — | DITOLAK (pemilih mematikan pengaman, 334/356) |
| H-009 | pengaman dipatok 0,25 | — | DITOLAK |
| H-010 | imbalan 4R terbatas | — | DITOLAK (`entri_acak` 0,0631) |
| H-011 | pengaman biaya masuk | — | DITOLAK |
| H-012 | himpunan tertahan sejak 2026-01 | **+0,041713** | DITOLAK (< 0,05R) |
| H-013 | dekomposisi sinyal/geometri | +0,066648 (SS) | **DITOLAK** (p bulan 0,205980) |
| **H-014** | `pakai_target` satu medan, umur setara | +0,067252 (SS′) | **DITOLAK** (rerata bulanan −0,027715R; p 0,375962) |
| **H-015** | **funding sebagai sinyal (K/F/A)** | — | **TERDAFTAR (ADR-037), belum dijalankan** |

### Angka yang HARAM dikutip sebagai kelulusan

`+0,029481R` · **`+0,027654R` sebagai besaran yang lulus** · `+0,054842R`, `+0,043732R`, `+0,066648R` sebagai kelulusan · `+0,060163R` · `+0,059636R` · p 0,001100 (satuan simbol) · p 0,003322 dan "+2,99 galat baku" · kata "LULUS" di `reports/backtest_h013_kontribusi.md` · prosa R-D3 di `reports/h013b_p.md` · ambang ADR-015 §4.4 sebagai pra-registrasi kaki geometri · "226 jendela / 63,5%" (yang benar 194 / 54,5%) · **angka H-014 mana pun dibandingkan langsung dengan angka H-013** (ADR-036) · **angka H-015 mana pun dibandingkan langsung dengan H-014** (ADR-037 §10: konfignya berbeda pada pengaman carry) · **F − K sebagai dasar kelulusan H-015**.

**Larangan permanen:** jangan pernah menyatakan sistem siap diperdagangkan; jangan menambahkan cabang `LULUS` ke H-014; jangan menambal `berpasangan.py` agar memancarkan kelulusan; **jangan menjalankan ulang H-014 dengan pengaman carry dinyalakan** (aturan 5); **jangan menggeser `AMBANG_RATE`, `MIN_PENAGIHAN`, atau seed H-015 sesudah hasil terlihat** (ADR-037 §10).

### Ambang beku — tidak digeser

lantai 0,004 · pengaman 0,5R · `BATAS_VOID` 20 · potong tanggal 2026-01-01 · SS−AS 0,020R · p ≤ 0,05 · ≥300 ulangan · ≥100 trade per sel · `MAKS_RASIO_DATAR` 0,10 · rasio 0,30 · ekspektasi 0,05R · `invarian_risiko` −1,5R · `maks_umur_bar` ≤ 168 · `imbalan_R` **tidak** dipatok 8,0 · **`maks_carry_realisasi_R` = 0,25 (mekanisme ADR-008, patokan ADR-009, angka ADR-004), wajib hidup di Konfig dasar (aturan 57)** · **`AMBANG_RATE` = 0,0001 dan `MIN_PENAGIHAN` = 30 (ADR-037, baru 2026-07-27)** · gerbang kesebelas 0,35 / 0,50R / 0,005 (ADR-011).

---

## 4. Asumsi — BUKAN fakta

1. **Kelayakan 1h dan 4h identik (447/74/112)** belum dijelaskan.
2. **`AH = +0,05817042814276683R`** — sesudah ADR-032 dibatalkan sebagian, penyebabnya **tidak diketahui**.
3. **Besar kegagalan `invarian_risiko`** pada enam sel H-013/H-014 belum pernah dibaca. **Kini lebih menarik:** dua sel H-014 gagal gerbang itu **tanpa** pengaman carry keras — dan H-015 akan menjalankannya **dengan** pengaman hidup.
4. **Cacah keluar `carry` sel SH** (`reports/backtest_h013_sh_sinyal_horizon.json`) belum dibaca — R-J1 menyatakan > 0.
5. **Apakah eksperimen lain memakai `buat_konfig=None`** — R-J2 menduga tidak ada sejak ADR-008, tetapi `run_wf.py` (H-001b) mendahuluinya dan belum diperiksa. **Kepercayaan rendah.**
6. **Asal uji ke-17** pada cacah 872 belum diketahui. Berlaku aturan 58.
7. **Rasio bar datar 1h lawan 4h** — `reports/diag_datar.json`; penolakan 4h seharusnya ≤ 74.
8. **Apakah funding memuat informasi arah** — kini **terdaftar sebagai H-015**, belum dijalankan, belum diketahui. Ramalan saya sendiri (R-L2) adalah **tidak**.

---

## 5. Penghalang aktif

- **Tidak ada run yang sedang berjalan.**
- **Cacat 18 terbuka, dibayar sebagian:** `konfig_audit` ada tetapi **belum dipanggil satu run pun** (aturan 42). Penutupnya adalah runner H-015 berikut bukti R-L5.
- **Cacat 17 terbuka:** gerbang `checksum` 4h mustahil lulus sampai daftar `git add` `h014.yml` diperbaiki, dan perbaikan itu wajib **menumpang** run 4h berikutnya.
- **Cacat 19 terbuka:** `praregistrasi.Kriteria` tidak dapat menyatakan satuan penarikan, pembobotan mengikat, maupun p bulanan.
- **Cacah uji tidak dapat diramal** sampai uji ke-17 ditemukan (aturan 58).
- `backfill_daily.yml` berjalan tiap Senin 02:00 UTC tanpa dipicu manusia.
- `notion_asap.yml` masih tanpa `git pull --rebase --autostash`.
- Tiga kunci `config/lux.yaml` masih tidak dibaca program (lampiran §8).

---

## 6. Tindakan berikutnya (urutan mengikat)

1. **Tulis kode H-015 menurut ADR-037.** Modulnya sudah dibaca seluruhnya; pra-registrasi sudah terkunci. Yang ditulis: saringan funding lewat `statistik_trailing`, sel K/F/A, penolakan acak setara berseed, runner yang **memanggil `konfig_audit.laporan_kesebandingan`**, menaruh `asdict(konfig)` utuh di manifes, dan **berhenti berkode bukan nol bila `pengaman_mati` tidak kosong**. Sumber dan pengujiannya **satu commit** (aturan 51). Ramalan cacah uji **paling sedikit 884** (aturan 58).
2. **Tutup cacat 17 bersamaan run 4h H-015** — sunting daftar `git add` di workflow, **tidak** digabung ke commit kode H-015. Sesudah manifes 4h ada di `main`, adjudikasi **paruh kedua R-B1**.
3. **Adjudikasi R-J1** — baca cacah keluar `carry` sel SH lewat skrip sisi runner; jangan menarik JSON 432 KB ke konteks. Sekalian baca besar kegagalan `invarian_risiko` enam sel.
4. **Temukan uji ke-17** — satu dorongan yang **hanya** menyentuh `tests/` tanpa menambah modul baru di `lux/`.
5. **Bayar cacat 19** — medan satuan/pembobotan/p bulanan pada `praregistrasi.Kriteria` berikut pengujian yang menolak hipotesis tanpa satuan. **Sesudah** H-015 berjalan, bukan sebelum.
6. **Rasio bar datar 4h** dari `reports/diag_datar.json`.
7. **Nasib workflow** — `notion_asap.yml`, `backfill_daily.yml`, `funding*.yml`, `doctor.yml`, `universe.yml`.
8. **Segarkan `PROMPT_KELANJUTAN.md`** sebelum konteks penuh — wajib memuat `STATE_LAMPIRAN.md`, batas muatan dorongan, ADR-036 dan **ADR-037**, aturan 57 dan 58, **cacat 19**, status "dibayar sebagian" cacat 18, dan cacah 872.
9. Utang panjang: audit config aturan 39, `runner.py` lawan `fc79e070`, `run_h013.py` lawan `418f6084`, `requirements-dev.txt`.

Nomor ADR bebas berikutnya: **ADR-038**. Jurnal berikutnya: **`journal/2026-07-27-38.md`** (33–37 dipakai sesi ini).

---

## 7. Disiplin kerja

- Pisahkan fakta (commit / run ID / kutipan) dari asumsi; bila belum terverifikasi, katakan **"Ini memerlukan verifikasi."**
- Ramalan ditulis **sebelum** hasil terlihat, dan yang meleset **tidak dihaluskan**. Cacah uji diramalkan sebagai **batas bawah** (aturan 58).
- **Koreksi pun dapat salah.** Bila sebuah koreksi ternyata terlalu keras, ia diperbaiki sebagai prosa dan kedua kesalahan tetap tercatat (aturan 50, dijalankan di v31).
- `STATE.md` diperbarui setiap posisi berubah; satu entri `journal/` per sesi; ADR untuk setiap keputusan yang membatasi masa depan.
- Berkas panjang **dipecah**; setiap muatan dorongan dibaca ulang **dari `main` sesudah dikirim** (aturan 35).

---

## 8. Rujukan cepat

Repo `EnVyxS/lux-research`, cabang `main`. Rincian peta repo, inventaris modul, audit workflow, batas alat, papan ramalan, angka H-012/H-013, dan rantai commit ada di **`STATE_LAMPIRAN.md`**.

Tonggak terakhir: `4af21176` (kode H-014, 855 uji) → `52c64ac5` (pemicu run `30221967019`) → `603477ce` (laporan H-014) → `a3355294` (v27) → `a25160ca` (ADR-035 + jurnal 32) → `e34961f5` (PROMPT v2) → `56633f80` (**v28 terpotong**) → `7869b7d5` (lampiran v1) → `f065fe92` (v28 utuh) → `03b5fc92` (jurnal 33) → `a9cbb4e8` (ADR-036 + jurnal 34) → `5474df2b` (v29) → `65916ec6` (modul `konfig_audit` + 16 uji + jurnal 35) → `61504ef6` (laporan uji, **872**) → `d62f2df9` (jurnal 36) → `11a0cafb` (v30) → **`a326932a`** (jurnal 37, koreksi tiga lapis) → **`08e21b3f`** (ADR-037, pra-registrasi H-015) → **v31 (berkas ini)**.

**Posisi: 14 hipotesis dinilai, 14 DITOLAK, 1 terdaftar belum dijalankan. 58 aturan. 19 kelas cacat. 872 uji.**
