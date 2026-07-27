# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Arsip rinci ada di **`STATE_LAMPIRAN.md`** dan wajib dibaca bersamanya. Jika sesuatu tidak tercatat di salah satu dari keduanya, anggap belum diketahui.

**Diperbarui:** 2026-07-27 13:30 WIB (versi 28) — ditulis sesudah blob v27 (`e387423cfb4ca67e7bad14301f4e50e551996954`, commit `a3355294`) dibaca **utuh**.

**Cacat alat pada v28 sendiri:** dorongan v28 **pertama** (commit `56633f80`) **terpotong** di tengah bagian 8 karena muatannya terlalu panjang dan saya tidak membacanya ulang utuh sebelum mengirim — pelanggaran **aturan 35** dalam bentuk yang belum pernah terjadi (bukan cacah salah, melainkan berkas tidak lengkap). Mitigasi struktural: arsip rinci dipindah ke `STATE_LAMPIRAN.md` (commit `7869b7d5`) supaya tidak ada muatan tunggal mendekati batas. Tidak ada angka yang dibuang. Commit terpotong itu **tidak dihapus dan tidak disembunyikan** (aturan 50).

**Tahap sekarang:** S22 — **H-014 DITOLAK.** Run `30221967019` selesai dalam **2 menit 19 detik** dan melahirkan putusan sah: rerata selisih bulanan SS′ − SH′ **−0,027715128544164157R** gagal terhadap ambang 0,020R, dan p uji tanda berpasangan bulanan **0,37596240375962403** gagal terhadap 0,05 (ADR-035). Penggabung keluar berkode **0** (aturan 48). **Empat belas hipotesis dinilai, empat belas ditolak. Nol kandidat bertahan.**

Temuan yang lebih penting daripada putusannya: **tanda besaran bergantung pada pembobotan** — satu himpunan 73 bulan yang sama memberi agregat **+0,027654R** (positif) dan rerata bulanan **−0,027715R** (negatif). Itu **cacat kelas keenam belas**, aturan **55**. Dan daftar `git add` di `h014.yml` yang saya tulis sendiri tidak memuat `reports/manifest_aset_4h.json`, sehingga gerbang `checksum` pada 4h **mustahil lulus selamanya** — **cacat kelas ketujuh belas**, aturan **56**.

**Tahap berikutnya:** (a) tutup cacat 17 dengan **menumpangkan** perbaikan daftar `git add` pada run 4h berikutnya, lalu adjudikasi paruh kedua R-B1; (b) jawab **anomali `buat_konfig`** (SH ≠ SH′) dengan membaca sumber, bukan menduga; (c) **funding sebagai SINYAL** — satu-satunya dimensi bersih yang belum pernah diuji, datanya sudah ada di rilis `tier-b-v1`, pra-registrasi disusun **sesudah** seluruh modul yang disebutnya dibaca, gerbang p bulanan wajib (ADR-031 keputusan 5), dan **pembobotan yang mengikat wajib dinyatakan sebelum run** (aturan 55).

**Tidak ada run yang sedang berjalan.** Satu-satunya proses berjadwal adalah `backfill_daily.yml`, tiap Senin 02:00 UTC.

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
19. (S13) **Margin setipis satu satuan resolusi bukan margin.** `entri_acak` H-010 lulus p 0,049505 pada 100 permutasi; pada 300 permutasi mekanisme yang sama memberi **0,0631** dan **gagal**. Dikonfirmasi ulang di H-012: **0,06312292358803986**. Diperluas di S19: R-A4 meramal p ≤ 0,001 dan nyatanya 0,001100. Diperluas lagi di S20: **R-D1 meleset hanya tiga menit dua detik dan tetap dicatat MELESET.** Tipis bukan alasan.
20. (S13) **Ekspektasi yang naik karena penyebutnya menyusut bukan keunggulan yang membesar.**
21. (S13) **Kecurigaan wajib naik, bukan turun, ketika hasilnya menyenangkan.** Dipakai empat kali di S16–S17 atas run yang terasa terlalu cepat; keempatnya **tak berdasar**. Kelima di S18 atas +0,054842R — **berdasar** (ADR-024). Keenam di S19 atas p simbol 0,001100 — **berdasar** (ADR-028). Ketujuh di S20 atas p per-perdagangan 0,003322 — **berdasar** (ADR-031). Kedelapan di S21 atas +0,029481R — **berdasar** (ADR-033, cacat 14). **Kesembilan di S22 atas agregat +0,027654R yang melewati ambang — berdasar** (ADR-035, cacat 16). **Bentuk terbaliknya juga nyata:** di S22 saya mencurigai run 2 menit 19 detik sebagai kegagalan dan **salah**.
22. (S13, ADR-014) **Menuntut kesamaan bit pada agregat pecahan adalah pengujian yang menyala pada perilaku yang benar.** Di dalam satu fungsi murni, kesamaan bit tetap sah.
23. (S13, ADR-014) **Pagar yang memastikan masukan identik tidak memastikan masukan sah.** Diperluas di S17: **kesamaan hasil lintas dua run berbeda dilarang diterima tanpa pemeriksaan.** **Dipakai lagi di S22 pada arah sebaliknya:** SH dan SH′ nominal identik tetapi **tidak** identik (44.614 lawan 44.538), dan ketidaksamaan itu wajib dijelaskan, bukan dibulatkan menjadi derau.
24. (S13, ADR-014) **Satu simbol dapat mendominasi agregat 438 simbol.**
25. (S13, ADR-014) **Himpunan tertahan habis pada saat pertama kali dilihat.**
26. (S13, ADR-014) **Cacat yang membalik tanda hasil tidak boleh diperbaiki di dalam hipotesis yang sama.**
27. (S13, ADR-014) **Eksperimen yang tercemar tidak informatif ke arah mana pun.**
28. (S13, ADR-014) **Saringan yang menolak entri juga menolak saat pemilihan.** Terbukti kuantitatif di H-012: hanya **62** entri ditolak pengaman. **Terbukti kedua kali di S21:** `maks_umur_bar` ikut menolak **entri** lewat proyeksi carry di `_boleh_masuk`.
29. (S14) **Pra-registrasi wajib diperiksa terhadap apa yang benar-benar dapat dihitung dari laporan.**
30. (S14) **Kriteria utama dihitung dari berkas laporan yang dikomit, bukan dari nilai yang beredar di memori run.**
31. (S15) **Pagar yang menyalin baris dari kode yang dijaganya tidak menjaga apa pun.**
32. (S15) **Aritmetika yang hidup di dalam `main` tidak dapat diuji.**
33. (S15) **Setiap langkah workflow wajib `tee` ke `logs/` dan seluruh `logs/` disalin ke `reports/` dengan `if: always()`.**
34. (S15) **Lingkungan pagar wajib memasang dependensi yang sama dengan `tests.yml`.**
35. (S16) **Muatan tulis yang panjang wajib dibaca ulang utuh sebelum dikirim, dan jumlah pengujian dicacah dari muatan yang benar-benar dikirim, bukan dari rencana.** Sejak aturan ini dipatuhi, dua puluh satu ramalan cacah berturut-turut tepat — lalu deret itu **PUTUS di S21** justru karena aturan ini dilanggar (R-H1, aturan 54). **DILANGGAR LAGI DI S22 dalam bentuk ketiga:** muatan `STATE.md` v28 pertama **terpotong** dan dikomit dalam keadaan terpotong (`56633f80`). Bukan cacah yang salah, melainkan **berkas yang tidak lengkap**. Mitigasi: berkas panjang dipecah supaya tidak ada muatan tunggal mendekati batas.
36. (S16, ADR-016) **Ramalan yang dijamin benar oleh konstruksi bukan ramalan.** **Dibuktikan telanjang di S22:** R-H3 meramal run selesai di bawah 25 menit; kenyataannya 2 menit 19 detik — **TEPAT tetapi tidak berguna**.
37. (S17, ADR-017–019) **Angka yang benar untuk satu interval tidak berubah nilai ketika dipakai di interval lain — ia berubah MAKNA, dan diam.** Setiap besaran yang berarti "satu hari" wajib diturunkan lewat `lux.kerangka`.
38. (S17) **Dua definisi atas satu dataset selalu dimenangkan oleh yang tidak terlihat.**
39. (S18) **Angka dapat hidup di berkas konfigurasi tanpa pernah masuk ke dalam program.** Cacat kelas kedelapan. **Kode wajib dibandingkan terhadap berkas, bukan hanya dibaca.**
40. (S18, ADR-024) **Putusan yang dihitung dari separuh kriteria pra-registrasi adalah putusan palsu, dan ia paling berbahaya ketika angkanya menyenangkan.** Cacat kelas kesembilan.
41. (S18, ADR-024) **Prosa kesimpulan yang dipatok di dalam kode bukan kesimpulan.** Cacat kelas kesepuluh; **ditutup** di `b0e79220` (767 uji).
42. (S19, ADR-025) **Gerbang yang tidak mungkin lulus tidak menjaga apa pun, dan ia terlihat seperti gerbang yang bekerja.** Cacat kelas kesebelas. **Setiap kegagalan gerbang wajib diperiksa apakah ia mungkin lulus sama sekali.** **Terulang di S22 lewat pintu lain** (cacat 17): sampai daftar `git add` diperbaiki, kegagalan `checksum` pada 4h **wajib dibaca sebagai cacat alat, bukan temuan**.
43. (S19, ADR-026) **Rencana analisis wajib diperiksa terhadap struktur berkas laporan sebelum dijadwalkan.** Pemasangan hanya mungkin pada **simbol (437)** dan **bulan (73)**; `per_simbol.jendela` adalah **cacah**.
44. (S19, ADR-028) **Ambang statistik tanpa satuan penarikan bukan ambang.** Cacat kelas kedua belas. Satuan resmi **bulan kalender UTC**. **Dibuktikan di S20:** satu run memberi p 0,003322 per perdagangan dan **0,205980** per bulan.
45. (S19, ADR-028) **`p` sah hanya untuk MENJATUHKAN, tidak untuk MENEGAKKAN.** Dijalankan secara struktural oleh `lux/analisis/berpasangan.py` (`memenuhi_adr015` dipatok `False`), dan sampai ke putusan di S22.
46. (S19) **Ramalan saya tepat ketika menyangkut kode saya sendiri dan meleset ketika menyangkut pasar** — **difalsifikasi di S21** (R-H1) dan diperkuat falsifikasinya di **S22** (R-G4 tentang mekanisme mesin saya sendiri, meleset jauh; dan muatan STATE v28 yang terpotong). **Sebelum membekukan ramalan angka, sebutkan asumsi yang menopangnya dan tandai mana yang belum diperiksa.**
47. (S19–S20, ADR-030) **Alat yang selalu menghasilkan angka tidak menjaga apa pun.** Penggabung **MENOLAK** (kode 4) alih-alih memotong ke irisan atau mengisi nol. Berhenti adalah keluaran yang sah.
48. (S20, ADR-030) **Hasil yang menjatuhkan hipotesis wajib berkode keluar 0.** Merah hanya untuk mesin yang rusak. **Dijalankan di S22:** `gabung_h014` keluar 0 sambil menjatuhkan H-014.
49. (S20, ADR-031) **Besaran tidak boleh diukur terhadap satu undian nol.** AS seed 42 (+0,011806R) ~0,98 simpangan baku **di bawah** rerata nol (+0,022916R). Besaran wajib dilaporkan **dua kali**; bila sebaran nol tidak ada, ketiadaannya wajib dinyatakan. **S22 memperlihatkan aturan ini tidak cukup: dua pelaporan dapat berbeda TANDA** (aturan 55).
50. (S20, ADR-031) **Ramalan yang terbukti salah alasannya dikoreksi sebagai PROSA di sumbernya, dan jejak bunyi aslinya tidak dihapus.** Laporan dan pesan commit yang sudah dikomit **tidak** ditulis ulang. Dipatuhi di S22 atas prosa ADR-033 tentang umur 42 lawan 48, dan atas commit terpotong `56633f80` yang **tidak** disembunyikan.
51. (S20) **Sumber dan pagarnya adalah satu commit.** Dipatuhi di `4af21176` (dua modul + dua berkas uji, satu dorongan).
52. (S21, ADR-033) **Sel pembanding hanya boleh berbeda pada SATU medan; bila dua, selisihnya bukan pengukuran.** Cacat kelas keempat belas. Dijalankan oleh alat: `run_h014.medan_berbeda` mengembalikan **daftar** medan, dan `main` menolak berjalan bila daftar itu bukan tepat `["pakai_target"]`. **TIDAK dibatalkan oleh ADR-035**; yang dibatalkan hanya besar efek yang saya lekatkan pada medan umur.
53. (S21, ADR-034) **Ambang hanya boleh dikutip sebagai beku bila dokumen yang membekukannya membekukannya untuk besaran yang sedang diuji; bila tidak, ia ambang BARU dan wajib dinyatakan begitu beserta tanggalnya.** Cacat kelas kelima belas.
54. (S21) **Ramalan cacah uji wajib dihitung dari berkas yang benar-benar akan didorong, bukan dari rencana; bila ramalan dan berkas berselisih, yang salah SELALU ramalannya.** `4af21176` meramal 850 (819+31) padahal berkasnya memuat 20+16 → **855**.
55. (S22, ADR-035) **Besaran yang tandanya bergantung pada pembobotan bukan besaran.** Cacat kelas keenam belas. Setiap selisih antar sel wajib dilaporkan dalam **empat** bentuk sekaligus — **agregat**, **rerata per unit penarikan**, **berbobot**, dan **median** — dan dokumen pra-registrasi wajib menyatakan **mana yang mengikat sebelum run**. Bila keempatnya tidak sepakat tanda, putusannya **TIDAK DAPAT DINILAI** kecuali pra-registrasi sudah memilih satu. Untuk H-014 yang mengikat adalah **rerata bulanan**, sebab itulah yang dibaca kode yang dikomit sebelum satu angka pun ada — **kebetulan yang beruntung, bukan rancangan sadar**: ADR-034 tidak pernah menyatakannya.
56. (S22, ADR-035) **Berkas yang dilahirkan sebuah run dan dibutuhkan sebuah gerbang agar dapat lulus wajib ikut dikomit; daftar `git add` adalah bagian dari gerbang, bukan urusan tata usaha.** Cacat kelas ketujuh belas.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa. Seluruh komputasi berjalan di GitHub Actions; repo adalah penyimpanan data sekaligus jurnal riset.

---

## 3. Fakta terverifikasi

### H-014 — DITOLAK (ADR-035, run `30221967019`)

**Bukti:** pemicu `52c64ac576e81883cd516316437edfff1d596ac4` pada 2026-07-26T21:52:25Z; laporan dikomit **`603477ce8b9b55e2a67d9a7a0e7c3c843c2be379`** pada 2026-07-26T21:54:44Z; log blob **`03e0c35c54134d9906515e2df515eb5f1c939b6c`**. Runner melaporkan **`855 passed in 2.98s`** sebelum satu berkas diunduh. Delapan butir pagar pra-terbang lulus **pada percobaan pertama**. 157 MB aset 4h terunduh (16 berkas), 438 simbol dimuat, **437 layak** sesudah lantai membuang USDCUSDT. Sel SSp **56,9 s**, sel SHp **52,6 s**, seluruh run **2 menit 19 detik**.

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

Alasan keluar SS′: `stop` 33.748 · `target` 18.667 · `umur` 5.174 · `akhir_data` 1.735. SH′: `stop` 28.013 · `umur` 14.426 · `akhir_data` 2.099.

SS′: 309 untung / 128 rugi, drop-1 **0,06639R** (retensi **0,9872**), drop-22 0,05419R, median simbol +0,06789R, porsi bruto teratas 0,0139 (SANDUSDT), funding maks 0,8285R, std **1,37827R**, galat baku 0,005659R (+3,05 SE), parameter terpilih {55:836, 20:1711, 100:1535}, sidik `197c10e3f0d2`.
SH′: 234 untung / 203 rugi, drop-1 **0,03583R** (retensi **0,9047**), drop-22 0,01225R, median simbol +0,02710R, porsi bruto teratas 0,0431 (VELVETUSDT), funding maks **2,9000R** (juga gagal `porsi_trade_di_atas_pengaman`), std **2,20818R**, galat baku 0,010463R (−0,99 SE), parameter {55:1073, 20:1995, 100:1014}, sidik `5721a88e59eb`. 73 bulan pada kedua sel.

**Kode H-014:** commit **`4af2117639c15ace7ba4a442ce2841091a1e25fb`** — `run_h014.py`, `gabung_h014.py`, `tests/test_run_h014.py` (20 uji), `tests/test_gabung_h014.py` (16 uji), **satu dorongan** (aturan 51); `reports/tests.md` blob **`94e5096e2f989edc13d3f1a95daa84b6b512331e`**, run **`30221837845`**, keluar 0, **`855 passed in 3.06s`**. Workflow `.github/workflows/h014.yml` commit **`52c64ac5`**: satu pekerjaan, `timeout-minutes: 180`, delapan butir pagar pra-terbang, dua sel berurutan, penggabung di pekerjaan yang sama — **tetapi daftar `git add`-nya cacat** (cacat 17).

**H-014 tidak pernah dapat LULUS, dan itu dipra-registrasi** (ADR-034 §2): `gabung_h014.PUTUSAN_MUNGKIN = ("DITOLAK", "TIDAK DAPAT DINILAI")`, tidak ada cabang `LULUS` di seluruh jalurnya, dan sebuah pengujian menuntut bahwa besaran besar **dan** p kecil sekalipun menghasilkan `TIDAK DAPAT DINILAI`.

### CACAT KELAS KEENAM BELAS — tanda besaran bergantung pada pembobotan (ADR-035 §2, aturan 55)

Satu himpunan **73 bulan yang sama** memberi:

| Cara membobot | Nilai | Tanda |
|---|---|---|
| selisih **agregat** | **+0,027654378351416438R** | **POSITIF** |
| **rerata** selisih bulanan | **−0,027715128544164157R** | **NEGATIF** |
| rerata **berbobot trade** | −0,012499029724652699R | NEGATIF |
| **median** selisih bulanan | +0,03495217650445759R | POSITIF |
| fraksi bulan positif | 0,5616438356164384 | — |

Dua angka pertama **hampir sama besar dan berlawanan tanda**. Agregat membobot menurut jumlah perdagangan sehingga didominasi bulan bervolume besar; rerata bulanan memberi setiap bulan bobot sama sehingga menghukum ekor bulan buruk. Bentuknya: **mayoritas bulan condong ke sel bertarget, tetapi beberapa bulan condong ke sel tanpa target dengan besar yang jauh lebih ekstrem.**

**Bila pembobotan bebas dipilih, H-014 melewati ambang besaran hari ini dengan agregat +0,0277R.** Yang mencegahnya bukan kehati-hatian saya melainkan bahwa `gabung_h014.adjudikasi` membaca `rerata_selisih`, dan kode itu dikomit **sebelum** satu angka pun ada. **p 0,376 menjatuhkan hipotesis pada pembobotan mana pun**, jadi putusannya tidak bergantung pada keberuntungan itu — tetapi ambang besarannya bergantung.

### CACAT KELAS KETUJUH BELAS — gerbang yang saya sendiri buat mustahil lulus (ADR-035 §3, aturan 56)

Log run mencetak, verbatim:

> `manifest aset reports/manifest_aset_4h.json (12 berkas interval 4h)`
> `checksum: tidak dapat dinilai: manifest baru ditulis pada run ini`

Itu **separuh pertama R-B1 TEPAT**. Tetapi `reports/manifest_aset_4h.json` **tidak ada di `main`** — diperiksa langsung, jawabannya "the file does not exist in the repository". Sebabnya daftar `git add` di `h014.yml`: ia menambahkan `reports/backtest_h014_*`, `reports/h014_run.json`, `reports/h014_berpasangan.*`, `reports/h014_log.md`, `hipotesis/H-014-*.json` — **dan tidak manifesnya**. Terverifikasi dari sumber (`runner.py` blob `4ce34a3c`): bila manifest belum ada, `muat_konteks` menulisnya lalu memancarkan `Gerbang("checksum", False, …, "tidak dapat dinilai: manifest baru ditulis pada run ini")` — gerbang itu hanya dapat lulus bila berkasnya **bertahan** di `main`.

**Keputusan (ADR-035 §3):** manifes 4h **tidak** didorong sebagai commit tersendiri; menyentuh `h014.yml` memicu ulang seluruh run. Perbaikan daftar `git add` **menumpang run 4h berikutnya**. Sampai itu terjadi, **kegagalan `checksum` pada 4h wajib dibaca sebagai cacat alat** (aturan 42).

### KLAIM ADR-033 DIBATALKAN SEBAGIAN — umur 42 lawan 48 bukan sebab utama (ADR-035 §4)

| Sel | Umur | Trade |
|---|---|---|
| SS (H-013) | 42 | 60.018 |
| **SS′ (H-014)** | **48** | **59.324** |
| SH (H-013) | 48 | 44.614 |
| **SH′ (H-014)** | **48** | **44.538** |

Efek menaikkan umur 42 → 48 pada sel bertarget: **−694 perdagangan, −1,2%**. Jarak antar sel dengan umur **disetarakan**: **+33,2%**. Jadi jarak perdagangan itu **hampir seluruhnya `pakai_target`**: target menutup **18.667** posisi di SS′, membebaskan modal lebih awal, sehingga lebih banyak entri lolos proyeksi carry. **Aturan 52 tidak dibatalkan** dan **+0,029481R tetap haram dikutip**. Yang dibatalkan adalah **besar** yang saya lekatkan pada medan umur — saya menyebut sesuatu "sebab terukur" sebelum mengukurnya.

### ANOMALI SH ≠ SH′ — MEMERLUKAN VERIFIKASI (ADR-035 §5)

Konfigurasi **nominal sama**: Donchian sungguhan, `pakai_target=False`, `maks_umur_bar=48`, `imbalan_R=2.0`, lantai 0,004, pengaman 0,5R, `stop_hormati_celah` menyala, jendela {1080,540,42}, pemanasan 200, semesta 437 yang sama.

| | Trade | Ekspektasi R | Lookback terpilih (20 / 55 / 100) |
|---|---|---|---|
| SH | 44.614 | +0,037166633609032385 | 1987 / 1069 / 1026 |
| SH′ | **44.538** | **+0,03959765698185091** | **1995 / 1073 / 1014** |

Selisih 76 perdagangan (0,17%) dan **+0,00243R** — kecil, **bukan nol** (aturan 23). Satu-satunya perbedaan jalur kode yang diketahui: H-013 memakai `buat_konfig=buat_konfig_sel(sel)`, H-014 memakai `None`.

**Yang sudah dibaca di S22 (fakta):** `lux/backtest/walk_forward.py` blob **`5a686e229c0292bdea2219278a318b96fa675637`** memuat `konfig_untuk(params) = buat_konfig(params, k) if buat_konfig is not None else k`, dan konfig itu dipakai **di dalam lingkaran pemilihan kandidat** (`_skor_baku(jalankan(latih, s, konfig_untuk(params), …))`) sekaligus untuk jendela uji; pemilihan memakai pembanding tegas `skor > skor_terbaik`, sehingga perbedaan sekecil apa pun pada skor menggeser kandidat terpilih. **Hipotesis kerja, BELUM diverifikasi:** bila `buat_konfig_sel` menghasilkan Konfig yang tidak identik medan demi medan dengan Konfig dasar H-014, lookback terpilih bergeser dan seluruh selisih ini terjelaskan. Yang belum dibaca berdampingan: `run_h013.buat_konfig_sel`, `run_h014.konfig_sel_h014`, `run_wf.py`. **Ini memerlukan verifikasi.** Sampai terjawab, **SS′ − SH′ bukan "SS − SH yang sudah diperbaiki"**.

### CACAT KELAS KEEMPAT BELAS dan KELIMA BELAS (ADR-033, ADR-034)

**Keempat belas:** `run_h013.umur_sel` memberi 42 untuk sel bertarget dan 48 untuk sel tanpa target, jadi **SS − SH mencampur dua medan**, dan `maks_umur_bar` bukan medan pasif (`engine._boleh_masuk` memakainya untuk proyeksi carry). **Putusan H-013 tidak berubah** — ia mati pada p bulanan 0,205980 kaki **sinyal**. Yang berubah: **`+0,029481R` tidak mengukur apa yang namanya sebut**.

**Kelima belas:** ADR-032 dan ADR-033 mengutip ambang ADR-015 §4.4 (≥ 0,020R, p ≤ 0,05, ≥300 ulangan, ≥100 trade) sebagai beku untuk kaki **geometri**, padahal §4.4 membekukannya untuk kaki **sinyal** (SS − AS, permutasi sinyal). Untuk geometri ADR-015 hanya menuntut besarannya **dilaporkan**. Ambang H-014 karena itu **BARU**, dibekukan 2026-07-27, dinyatakan di kode (`CATATAN_AMBANG`), laporan md, dan pagar pra-terbang butir 4.

### ADR-032 DIBATALKAN SEBAGIAN (ADR-033 §2)

Keberatan B ADR-032 ("tanpa stop, penyebut R adalah jarak nosional") **SALAH**: `engine.jalankan` mengevaluasi `kena_stop` **tanpa syarat**, `pakai_target=False` hanya mematikan target, `jarak = k.atr_pengali_stop * atr_t` di kedua sel, jadi penyebut R **dibangun identik**. Akibatnya **`AH = +0,05817042814276683R` kembali TIDAK TERJELASKAN — ini memerlukan verifikasi**; H-014 tidak menyentuhnya. **R-F1…R-F5 DIBATALKAN** dan tidak akan pernah punya angka: nol permutasi jarak stop tidak dapat dijalankan tanpa bedah `engine.jalankan`.

### JALUR B — H-013 DITOLAK (ADR-031, run `30217516013`)

Pemicu `97b36c19`; sepuluh pecahan mengomit 20:13:43Z–20:28:15Z; laporan p `1d746879` pada 20:28:37Z. Sepuluh dari sepuluh pecahan hadir, seed utuh 300 pada [0,300), 73 bulan pada SS, keluar 0.

| Syarat ADR-015 §4.4 | Nilai | Ambang | Terpenuhi |
|---|---|---|---|
| besaran SS − AS | **+0,054842R** | 0,020R | ya |
| **p satuan bulan** | **0,205980** | 0,05 | **TIDAK** |
| ulangan | 300 | 300 | ya |
| trade terkecil antar sel | 54.812 | 100 | ya |

Sebaran nol 300 seed: rerata **+0,022916R** · sd **+0,011377R** · rentang **−0,004632R … +0,057394R** · sel SS +0,066648R. p satuan perdagangan pada run yang sama **0,003322** — `taksiran_bawah`, **haram** menegakkan klaim (aturan 45). **Bila satuan boleh dipilih sesudah hasil terlihat, H-013 lulus hari ini dengan p 0,0033.** Jalur A membenarkan dengan mesin berbeda: p bulanan berpasangan **0,365363**, bootstrap memuat nol.

**Cacat kelas ketiga belas (ADR-031, sudah dipasang ke alat):** +0,054842R dihitung terhadap **satu** sel nol seed 42; terhadap rerata nol ia **+0,043732R** — dua puluh persen lebih kecil. Dibayar di sumber lewat `6ae83062` dan `5bd73fbf` (819 uji). `reports/h013b_p.md` **tetap** memuat prosa R-D3 yang salah dan **tidak** ditulis ulang (aturan 50).

### JALUR A — keberartian jatuh pada satuan bulan (modul `48cf1b9f`, blob `a9fba624`, hasil `e3309954`)

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

**SH lawan AH:** simbol — rerata −0,010358R, berbobot −0,023331R, agregat −0,021004R, fraksi 0,4760, p 0,777622. Bulan — rerata −0,029960R, berbobot −0,028521R, median −0,072371R, fraksi 0,4110, **p 0,280372**, bootstrap [−0,084772, +0,024341]R. **Anomali SH < AH turun pangkat menjadi derau.** Adjudikasi R-A1…R-A6: empat tepat, **R-A4 MELESET** (0,001100 lawan ≤ 0,001), **R-A5 MELESET JAUH** (0,365363 lawan ≤ 0,01).

### Papan skor hipotesis — EMPAT BELAS DINILAI, EMPAT BELAS DITOLAK

| ID | Mekanisme | Ekspektasi R | Putusan |
|---|---|---|---|
| H-001b | Donchian polos | 0,03086 | DITOLAK (`invarian_risiko` −2,5853) |
| H-002 | Donchian + saringan carry | 0,03159 | DITOLAK |
| H-003 | pembalikan skor-z | −0,24782 | DITOLAK |
| H-004 | Donchian + ADX ≥ 30 | −0,01818 | DITOLAK |
| H-005 | entri retest | −0,03571 | DITOLAK |
| H-006 | sapuan likuiditas | −0,13449 | DITOLAK |
| H-007 | imbalan bergrid | — | DITOLAK (di bawah ambang) |
| H-008 | saringan rezim | — | DITOLAK |
| H-009 | pemilihan imbalan walk-forward | — | DITOLAK |
| H-010 | imbalan 4R terbatas | — | DITOLAK (`entri_acak` 0,0631 pada 300 ulangan) |
| H-011 | pengaman biaya masuk | — | DITOLAK |
| H-012 | himpunan tertahan sejak 2026-01 | **+0,041713** | DITOLAK (< 0,05R; `entri_acak` 0,063123) |
| H-013 | dekomposisi sinyal/geometri | +0,066648 (SS) | **DITOLAK** (p bulan 0,205980) |
| **H-014** | `pakai_target` satu medan, umur setara | +0,067252 (SS′) | **DITOLAK** (rerata bulanan −0,027715R; p 0,375962) |

### Angka yang HARAM dikutip sebagai kelulusan

`+0,029481R` ("kontribusi geometri" — mencampur dua medan) · **`+0,027654R` sebagai besaran yang lulus** (agregat; yang mengikat rerata bulanan) · `+0,054842R`, `+0,043732R`, `+0,066648R` sebagai kelulusan · `+0,060163R` · `+0,059636R` · p 0,001100 (satuan simbol) · p 0,003322 dan "+2,99 galat baku" (satuan perdagangan) · kata "LULUS" di `reports/backtest_h013_kontribusi.md` · prosa R-D3 di `reports/h013b_p.md` · ambang ADR-015 §4.4 sebagai pra-registrasi kaki geometri · "226 jendela / 63,5%" (yang benar 194 / 54,5%).

**Larangan permanen:** jangan pernah menyatakan sistem siap diperdagangkan; jangan menambahkan cabang `LULUS` ke H-014; jangan menambal `berpasangan.py` agar memancarkan kelulusan.

### Ambang beku — tidak digeser

lantai 0,004 · pengaman 0,5R · `BATAS_VOID` 20 · potong tanggal 2026-01-01 · SS−AS 0,020R · p ≤ 0,05 · ≥300 ulangan · ≥100 trade per sel · `MAKS_RASIO_DATAR` 0,10 · rasio 0,30 · ekspektasi 0,05R · `invarian_risiko` −1,5R · `maks_umur_bar` ≤ 168 · `imbalan_R` **tidak** dipatok 8,0.

---

## 4. Asumsi — BUKAN fakta

1. **Kelayakan 1h dan 4h identik (447/74/112)** belum dijelaskan.
2. **`AH = +0,05817042814276683R`** — sel permutasi tanpa target mengungguli sel sungguhan tanpa target; sesudah ADR-032 dibatalkan sebagian, penyebabnya **tidak diketahui**.
3. **Besar kegagalan `invarian_risiko`** pada enam sel H-013/H-014 belum pernah dibaca.
4. **Anomali `buat_konfig`** (§3) — hipotesis kerja ada, verifikasi belum.
5. **Rasio bar datar 1h lawan 4h** — `reports/diag_datar.json`; penolakan 4h seharusnya ≤ 74.
6. **Funding sebagai sinyal** belum pernah diuji sekali pun.

---

## 5. Penghalang aktif

- **Tidak ada run yang sedang berjalan.**
- **Cacat 17 terbuka:** gerbang `checksum` 4h mustahil lulus sampai daftar `git add` `h014.yml` diperbaiki, dan perbaikan itu wajib **menumpang** run 4h berikutnya.
- `backfill_daily.yml` berjalan tiap Senin 02:00 UTC tanpa dipicu manusia.
- `notion_asap.yml` masih tanpa `git pull --rebase --autostash`.
- Tiga kunci `config/lux.yaml` masih tidak dibaca program (lampiran §8).

---

## 6. Tindakan berikutnya (urutan mengikat)

1. **Tutup cacat 17** — sunting daftar `git add` `h014.yml` **bersamaan** dengan run 4h berikutnya yang memang perlu dijalankan; jangan menyentuhnya sendirian. Sesudah manifes 4h ada di `main`, adjudikasi **paruh kedua R-B1**.
2. **Jawab anomali `buat_konfig`** — baca `run_wf.py`, `run_h013.buat_konfig_sel`, `run_h014.konfig_sel_h014` **utuh**, berdampingan. Jangan menduga.
3. **Funding sebagai SINYAL** — baca seluruh modul yang akan disebut pra-registrasi **sebelum** menulisnya (aturan 8, 29, 43, pelajaran S21). Pra-registrasi wajib menyatakan: satuan penarikan **bulan kalender UTC**, gerbang **p bulanan**, dan **pembobotan mana yang mengikat** (aturan 55). Empat pembobotan wajib dilaporkan sekaligus.
4. **Baca besar kegagalan `invarian_risiko`** lewat skrip sisi runner — jangan menarik JSON 432 KB ke konteks.
5. **Rasio bar datar 4h** dari `reports/diag_datar.json`.
6. **Nasib workflow** — `notion_asap.yml`, `backfill_daily.yml`, `funding*.yml`, `doctor.yml`, `universe.yml`.
7. **Segarkan `PROMPT_KELANJUTAN.md`** sebelum konteks penuh.
8. Utang panjang: audit config aturan 39, `runner.py` lawan `fc79e070`, `run_h013.py` lawan `418f6084`, `requirements-dev.txt`.

Nomor ADR bebas berikutnya: **ADR-036**. Jurnal berikutnya: **`journal/2026-07-27-34.md`** (33 dipakai sesi ini).

---

## 7. Disiplin kerja

- Pisahkan fakta (commit / run ID / kutipan) dari asumsi; bila belum terverifikasi, katakan **"Ini memerlukan verifikasi."**
- Ramalan ditulis **sebelum** hasil terlihat, dan yang meleset **tidak dihaluskan**.
- `STATE.md` diperbarui setiap posisi berubah; satu entri `journal/` per sesi; ADR untuk setiap keputusan yang membatasi masa depan.
- Berkas panjang **dipecah**; setiap muatan dorongan dibaca ulang utuh sebelum dikirim (aturan 35).

---

## 8. Rujukan cepat

Repo `EnVyxS/lux-research`, cabang `main`. Rincian peta repo, inventaris modul, audit workflow, batas alat, papan ramalan, angka H-012/H-013, dan rantai commit ada di **`STATE_LAMPIRAN.md`**.

Tonggak terakhir: `4af21176` (kode H-014, **855 uji**) → `52c64ac5` (pemicu run `30221967019`) → `603477ce` (laporan H-014) → `a3355294` (v27) → `a25160ca` (ADR-035 + jurnal 32) → `d49aab94` → `e34961f5` (PROMPT v2) → `56633f80` (**v28 terpotong**) → `7869b7d5` (lampiran v1) → **v28 utuh (berkas ini)**.
