# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-27 03:40 WIB (versi 25)

**Tahap sekarang:** S20 — **Jalur B SELESAI dan H-013 DITOLAK.** Run **`30217516013`** (sepuluh pecahan × 30 seed + penggabung, pemicu `97b36c19`) menghitung untuk **pertama kalinya dalam tiga belas hipotesis** kedua syarat ADR-015 §4.4 atas run yang sama: besaran SS − AS **+0,054842R ≥ 0,020R** (terpenuhi) dan **p = 0,205980 pada satuan bulan > 0,05** (TIDAK terpenuhi), atas 300 ulangan penuh dengan trade terkecil 54.812. Putusan **DITOLAK**, penggabung keluar berkode **0** karena DITOLAK adalah HASIL (ADR-030 R2). Berkas putusan: `reports/h013b_p.json` blob `cd45685b`, `.md` blob `4c780435`, log penggabung `48fbfa8b`.

**Tahap berikutnya:** **funding sebagai SINYAL** — satu-satunya dimensi bersih yang belum pernah diuji sekali pun, datanya sudah ada di rilis `tier-b-v1`. Wajib dipra-registrasi lengkap **sebelum** satu baris kode ditulis, dan wajib melewati gerbang p bulanan (ADR-031 keputusan 5). Sebelum itu: utang tertulis di bagian 6 butir 3–9.

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
21. (S13) **Kecurigaan wajib naik, bukan turun, ketika hasilnya menyenangkan.** Dipakai empat kali di S16–S17 atas run yang terasa terlalu cepat; keempatnya **tak berdasar**. Dipakai kelima kali di S18 atas +0,054842R, dan ia **berdasar** (ADR-024). Keenam kali di S19 atas p simbol 0,001100, dan ia **berdasar** (ADR-028). Ketujuh kali di S20 atas p per-perdagangan 0,003322, dan ia **berdasar** (ADR-031).
22. (S13, ADR-014) **Menuntut kesamaan bit pada agregat pecahan adalah pengujian yang menyala pada perilaku yang benar.** Di dalam satu fungsi murni, kesamaan bit tetap sah.
23. (S13, ADR-014) **Pagar yang memastikan masukan identik tidak memastikan masukan sah.** Diperluas di S17: **kesamaan hasil lintas dua run berbeda dilarang diterima tanpa pemeriksaan.**
24. (S13, ADR-014) **Satu simbol dapat mendominasi agregat 438 simbol.**
25. (S13, ADR-014) **Himpunan tertahan habis pada saat pertama kali dilihat.**
26. (S13, ADR-014) **Cacat yang membalik tanda hasil tidak boleh diperbaiki di dalam hipotesis yang sama.**
27. (S13, ADR-014) **Eksperimen yang tercemar tidak informatif ke arah mana pun.**
28. (S13, ADR-014) **Saringan yang menolak entri juga menolak saat pemilihan.** Terbukti kuantitatif di H-012: hanya **62** entri ditolak pengaman.
29. (S14) **Pra-registrasi wajib diperiksa terhadap apa yang benar-benar dapat dihitung dari laporan.**
30. (S14) **Kriteria utama dihitung dari berkas laporan yang dikomit, bukan dari nilai yang beredar di memori run.**
31. (S15) **Pagar yang menyalin baris dari kode yang dijaganya tidak menjaga apa pun.**
32. (S15) **Aritmetika yang hidup di dalam `main` tidak dapat diuji.**
33. (S15) **Setiap langkah workflow wajib `tee` ke `logs/` dan seluruh `logs/` disalin ke `reports/` dengan `if: always()`.**
34. (S15) **Lingkungan pagar wajib memasang dependensi yang sama dengan `tests.yml`.**
35. (S16) **Muatan tulis yang panjang wajib dibaca ulang utuh sebelum dikirim, dan jumlah pengujian dicacah dari muatan yang benar-benar dikirim, bukan dari rencana.** Sejak aturan ini dipatuhi, **sembilan belas** ramalan cacah berturut-turut tepat.
36. (S16, ADR-016) **Ramalan yang dijamin benar oleh konstruksi bukan ramalan.**
37. (S17, ADR-017–019) **Angka yang benar untuk satu interval tidak berubah nilai ketika dipakai di interval lain — ia berubah MAKNA, dan diam.** Setiap besaran yang berarti "satu hari" wajib diturunkan lewat `lux.kerangka`, tidak pernah dari literal.
38. (S17) **Dua definisi atas satu dataset selalu dimenangkan oleh yang tidak terlihat.**
39. (S18) **Angka dapat hidup di berkas konfigurasi tanpa pernah masuk ke dalam program.** Cacat kelas kedelapan. **Kode wajib dibandingkan terhadap berkas, bukan hanya dibaca.**
40. (S18, ADR-024) **Putusan yang dihitung dari separuh kriteria pra-registrasi adalah putusan palsu, dan ia paling berbahaya ketika angkanya menyenangkan.** Cacat kelas kesembilan.
41. (S18, ADR-024) **Prosa kesimpulan yang dipatok di dalam kode bukan kesimpulan.** Cacat kelas kesepuluh; **sudah ditutup** di `b0e79220` (767 uji).
42. (S19, ADR-025) **Gerbang yang tidak mungkin lulus tidak menjaga apa pun, dan ia terlihat seperti gerbang yang bekerja.** Cacat kelas kesebelas: nama manifest aset dipatok `manifest_aset.json` untuk interval apa pun. **Setiap kegagalan gerbang wajib diperiksa apakah ia mungkin lulus sama sekali; kegagalan yang mustahil dihindari bukan temuan, melainkan cacat.**
43. (S19, ADR-026) **Rencana analisis wajib diperiksa terhadap struktur berkas laporan sebelum dijadwalkan.** ADR-024 menjadwalkan uji atas "4.082 jendela" padahal `per_simbol.jendela` adalah **cacah**. Pemasangan hanya mungkin pada **simbol (437)** dan **bulan (73)**.
44. (S19, ADR-028) **Ambang statistik tanpa satuan penarikan bukan ambang.** Cacat kelas kedua belas. Satuan resmi kini **bulan kalender UTC**. **Dibuktikan telanjang di S20:** satu run yang sama memberi p 0,003322 per perdagangan dan **0,205980** per bulan.
45. (S19, ADR-028) **`p` sah hanya untuk MENJATUHKAN, tidak untuk MENEGAKKAN.**
46. (S19) **Ramalan saya tepat ketika menyangkut kode saya sendiri dan meleset ketika menyangkut pasar.** Sembilan belas ramalan cacah uji berturut-turut tepat; dari sebelas ramalan angka H-013 sembilan meleset, dan dari lima ramalan Jalur B dua meleset. Sebab tiap kekeliruan sama: sebuah asumsi yang tidak pernah diperiksa diperlakukan sebagai fakta. **Sebelum membekukan ramalan angka, sebutkan asumsi yang menopangnya dan tandai mana yang belum diperiksa.**
47. (S19–S20, ADR-030) **Alat yang selalu menghasilkan angka tidak menjaga apa pun.** Penggabung yang memaksakan keluaran atas himpunan bulan yang berbeda akan mencetak angka yang tampak waras atas dua himpunan yang bukan pasangan. Karena itu ia **MENOLAK** (kode 4), tidak memotong ke irisan, dan tidak mengisi nol. Berhenti adalah keluaran yang sah.
48. (S20, ADR-030) **Hasil yang menjatuhkan hipotesis wajib berkode keluar 0.** Menandai DITOLAK sebagai kegagalan pekerjaan akan mendorong siapa pun mengutak-utik sampai papan hijau. Merah hanya untuk mesin yang rusak, bukan untuk hipotesis yang mati.
49. (S20, ADR-031) **Besaran tidak boleh diukur terhadap satu undian nol.** Sel AS seed 42 (+0,011806R) ternyata ~0,98 simpangan baku **di bawah** rerata sebaran nol (+0,022916R). Setiap besaran terhadap sel nol wajib dilaporkan juga terhadap **rerata** sebaran nol; besaran terhadap satu seed hanya boleh dikutip bila nomor seed-nya ikut ditulis.
50. (S20, ADR-031) **Ramalan yang terbukti salah alasannya dikoreksi sebagai PROSA di sumbernya, dan jejak bunyi aslinya tidak dihapus.** Laporan yang sudah dikomit tidak ditulis ulang untuk menutupi ramalan yang meleset.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa. Seluruh komputasi berjalan di GitHub Actions.

---

## 3. Fakta terverifikasi

### JALUR B — PUTUSAN LAHIR, H-013 DITOLAK (ADR-031)

Run **`30217516013`**, pemicu `97b36c19` pada 2026-07-26T19:45:13Z. Sepuluh pecahan mengomit antara 20:13:43Z dan 20:28:15Z; laporan p dikomit `1d746879` pada 20:28:37Z. **Sepuluh dari sepuluh pecahan hadir, seed utuh 300 pada [0,300), 73 bulan pada sel SS, kode keluar penggabung 0.**

| Syarat ADR-015 §4.4 | Nilai | Ambang | Terpenuhi |
|---|---|---|---|
| besaran SS − AS | **+0,054842R** | 0,020R | ya |
| **p satuan bulan** | **0,205980** | 0,05 | **TIDAK** |
| ulangan | 300 | 300 | ya |
| trade terkecil antar sel | 54.812 | 100 | ya |

**Sebaran nol atas 300 seed:** rerata **+0,022916R** · simpangan baku **+0,011377R** · rentang **−0,004632R … +0,057394R** · ekspektasi sel SS yang dibandingkan **+0,066648R**.

**p satuan perdagangan pada run yang sama: 0,003322** (cacah 0 dari 300) — sel SS melampaui **seluruh** 300 undian nol pada satuan itu. Ia berlabel `taksiran_bawah` dan **haram** dipakai menegakkan klaim (aturan 45, ADR-028).

**Temuan terpenting bukan putusannya, melainkan satuannya.** Satu run, dua angka p yang berlawanan arah, dan yang membuat satuan bulan sah bukan besarnya melainkan bahwa ia dibekukan ADR-028 **sebelum** kedua angka ini ada. **Bila satuan boleh dipilih sesudah hasil terlihat, H-013 lulus hari ini dengan p 0,0033.** Sebabnya statistik: 60.018 perdagangan bukan 60.018 bukti bebas — perdagangan lintas simbol pada jendela yang bertumpang berkorelasi, sehingga satuan perdagangan menghitung bukti yang sama berkali-kali. Pada 73 bulan, sumbangan sinyal tenggelam di dalam derau bulan-ke-bulan.

Jalur A membenarkannya dengan mesin berbeda: p bulanan berpasangan **0,365363**, bootstrap memuat nol. Angkanya memang tidak sama (0,205980 lawan 0,365363) sebab ujinya berbeda — Jalur A menguji selisih berpasangan per bulan, Jalur B menguji sel SS terhadap 300 sinyal acak yang dibangkitkan ulang. Arahnya sama.

### CACAT KELAS KETIGA BELAS — besaran diukur terhadap satu undian nol (ADR-031)

Sumbangan sinyal +0,054842R dihitung sebagai SS − AS dengan AS = **satu** sel, seed 42, +0,011806R. Sesudah sebaran nolnya diketahui, seed 42 terletak sekitar **0,98 simpangan baku di bawah rerata nol**.

- Terhadap seed 42: +0,066648 − 0,011806 = **+0,054842R**
- Terhadap rerata sebaran nol: +0,066648 − 0,022916 = **+0,043732R**

Dua puluh persen lebih kecil. Putusan **tidak berubah** — keduanya melewati 0,020R dan yang menjatuhkan H-013 adalah p — tetapi angka yang dikutip di seluruh laporan sebelumnya lebih bagus daripada yang pantas, dan sebabnya struktural: satu undian nol tidak punya galat. Sekeluarga dengan cacat kelas kedua belas, yang hari ini terbukti lagi: simpangan baku antar seed **0,011377R** melawan galat baku per perdagangan **0,005570R** — **dua kali lebih lebar**.

Larangan menghitung ulang H-001b sampai H-012 **tetap berlaku**. Aturan 49 berlaku untuk hipotesis yang akan datang.

### Mesin Jalur B — tiga modul, masing-masing hijau sendiri lebih dulu

| Modul | Commit | Uji | Isi |
|---|---|---|---|
| `lux/analisis/sebaran_nol.py` | `05df8b78` | **779** | `KUNCI_BULAN`, `rerata_bulanan`, `rerata_bulanan_berbobot`, `selisih_bulanan`, `p_ekor_atas` (`p = (1+cacah)/(1+n)`), `p_per_perdagangan` (`taksiran_bawah: True`, `mengikat: False`), `p_bulanan` (`satuan: "bulan"`, `mengikat: True`) |
| `lux/backtest/run_h013b.py` | `4f09c8d5` | **795** | `NAMA_SPEK="h013b_as_seed"`, `SEED_PER_PECAHAN=30`, `EKSPEKTASI_AS_SEED42=0.01180570125176449`, `periksa_kesetaraan`, `baris_seed`, keluar 3 bila R-D5 meleset |
| `lux/backtest/gabung_h013b.py` | `0859e8dd` | **811** | `EKSPEKTASI_SS=0.06664781299919262`, `TRADE_SS=60018`, `AMBANG_P=0.05`, `periksa_cakupan`, `periksa_bulan`, `adjudikasi`, `ringkas`, `tulis_laporan` |

Workflow `.github/workflows/h013b.yml` (`97b36c19`) memuat empat hal yang tidak ada di dua belas workflow lain: sepuluh penulis satu cabang dengan **lingkaran ulang dorong sepuluh kali berjeda acak**, berkas antara `backtest_h013b_as_seed.json` yang **tidak pernah dikomit** (ia ditulis ulang 30 kali per pecahan oleh `jalankan_spek` dengan nama berkas yang sama), `fail-fast: false`, dan **kode keluar 4 yang tetap mengomit laporannya lebih dulu**.

**Bahaya yang hanya tertangkap karena membaca sebelum menulis:** `jalankan_spek` menulis `backtest_<nama>.json` dengan nama yang sama setiap panggilan, jadi tanpa `NAMA_SPEK` tersendiri Jalur B akan **menimpa diam-diam** laporan sel AS run 30214203863 yang sudah dikomit.

**Bahaya rekayasa baru yang dicatat (ADR-030 R3):** `git pull --rebase --autostash` sekali — pola yang lulus di dua belas workflow — **tidak cukup** pada matriks. Pecahan yang kalah lomba dorong **hilang tanpa suara** lalu menyamar sebagai "cakupan seed tidak utuh", sehingga kegagalan git berkedok kegagalan backtest.

### H-013 — RUN SEL, ANGKANYA (run `30214203863`)

Mesin commit **`93a4309b`**, laporan dikomit **`e060749c`** pada 2026-07-26T18:21:35Z, sekitar **sepuluh menit** sesudah push. Delapan butir pagar pra-terbang **lulus**, 739 uji hijau di runner, 157 MB aset 4h terunduh, 438 simbol dimuat, **437 layak** sesudah lantai membuang **USDCUSDT** (median `stop_frac` 3,799992e−04), 4.082 jendela per sel.

| Sel | Sinyal | Target | Umur (bar 4h) | Trade | Ekspektasi R | p entri acak | Gerbang gagal |
|---|---|---|---|---|---|---|---|
| SS | sungguhan | ya | 42 | 60.018 | **+0,066648** | 0,0166 | `invarian_risiko`, `checksum` |
| SH | sungguhan | tidak | 48 | 44.614 | +0,037167 | 0,2259 | `entri_acak`, `invarian_risiko`, `checksum`, `funding_ekor` |
| AS | permutasi seed 42 | ya | 42 | 55.927 | +0,011806 | 0,3588 | `entri_acak`, `lookahead`, `invarian_risiko`, `checksum`, `konsentrasi` |
| AH | permutasi | tidak | 48 | 45.378 | +0,058170 | 0,1993 | `entri_acak`, `lookahead`, `invarian_risiko`, `checksum`, `funding_ekor` |

Sidik: SS `06c3805bdd7ad4de` · SH `af1145aab7f13567` · AS `5ee4b130f9ed228d` · AH `4ada4587abede644`.

Tiga selisih: **sinyal (SS − AS) +0,054842R terhadap seed 42, +0,043732R terhadap rerata nol** · **geometri (SS − SH) +0,029481R** · **interaksi +0,075846R**. Turunan yang wajib ikut dikutip: **SH − AH = −0,021004R**.

`parameter_beku` run itu, yang dipakai ulang apa adanya oleh Jalur B: `imbalan_R` 2,0 · `h_bar` 48 · `umur_sel_stop` 42 · `lookback` [20,55,100] · `seed_permutasi` 42 · `ulangan` 300 · `min_median_stop_frac` 0,004 · `maks_biaya_masuk_R` 0,5 · `stop_hormati_celah` true · `jendela_bar` {1080,540,42} · `pemanasan` 200 · `bar_dibutuhkan` 1862.

**Medan `lulus` di `backtest_h013_kontribusi.json` tetap TIDAK SAH** dibaca sebagai kelulusan: ia dihitung dari `sinyal >= AMBANG_KONTRIBUSI_SINYAL` saja, dan `p_entri_acak` adalah **uji lain**. Sejak S20, putusan H-013 yang sah **hanya** yang lahir dari `reports/h013b_p.json`.

**Cacat kelas kesepuluh sudah DITUTUP** di `b0e79220` (run `30216468770`, **767** uji): prosa `kontribusi.md` dulu mematok "sumbangan geometri lebih besar daripada sumbangan sinyal" padahal geometri +0,029481R < sinyal +0,054842R — laporan yang membantah datanya sendiri. Prosanya sekarang diturunkan dari angka dan dijaga pengujian.

### JALUR A — SELESAI, MENJATUHKAN KEBERARTIAN PADA SATUAN BULAN

Modul `lux/analisis/berpasangan.py` commit **`48cf1b9f`**, RAMALAN 749 → run `30215332779`: **`749 passed in 2,92s`**, TEPAT. Workflow `berpasangan.yml` commit **`5970c136`** dengan R-A1…R-A6 dibekukan **sebelum** run. Hasil `e3309954`; `--ambang 0.020 --ulangan 10000 --seed 20260727`.

**SS lawan AS (sumbangan sinyal):**

| Besaran | tingkat simbol (437) | tingkat bulan (73) |
|---|---|---|
| rerata selisih | +0,035625R | +0,023327R |
| rerata berbobot trade | +0,053518R | +0,047950R |
| selisih agregat | +0,054842R | +0,054842R |
| median selisih | +0,050280R | +0,036628R |
| fraksi positif | 0,6293 | **0,5342** |
| p uji tanda | **0,001100** | **0,365363** |
| bootstrap 95% | [+0,015182, +0,055725]R | **[−0,027040, +0,073620]R — MEMUAT NOL** |

**SH lawan AH:** simbol — rerata −0,010358R, berbobot −0,023331R, agregat −0,021004R, median −0,009670R, fraksi positif 0,4760, p 0,777622, bootstrap [−0,052779, +0,046846]R. Bulan — rerata −0,029960R, berbobot −0,028521R, median −0,072371R, fraksi positif 0,4110, p 0,280372, bootstrap [−0,084772, +0,024341]R. **Anomali SH < AH turun pangkat menjadi derau**; ia bukan temuan dan tidak menuntut penjelasan.

Kedua laporan mencetak `memenuhi_adr015: false` secara struktural: `ringkas()` **selalu** mengembalikan `False` untuk medan itu, sebab uji tanda bukan uji permutasi sinyal.

**Adjudikasi R-A1…R-A6 — empat tepat, dua meleset:** R-A1 TEPAT (437/73) · R-A2 TEPAT (+0,035625R) · R-A3 TEPAT (agregat direkonstruksi persis) · **R-A4 MELESET** (p 0,001100 lawan ramalan ≤ 0,001) · **R-A5 MELESET JAUH** (p bulan 0,365363 lawan ≤ 0,01; fraksi 0,5342 lawan ≥ 0,60) · R-A6 TEPAT.

### CACAT KELAS KESEBELAS — gerbang yang tidak mungkin lulus (ADR-025, DITUTUP)

`reports/manifest_aset.json` (blob `2e95a0ff`, 1.198 B) memuat **dua belas kunci, seluruhnya `ohlcv_1h_*`**. Run H-013 membaca dua belas berkas `ohlcv_4h_*`, jadi irisan namanya **nol**, dan `muat_konteks` hanya menulis manifest `if not manifest_path.exists()` — manifest 4h **tidak mungkin lahir**.

Perbaikan dua langkah sengaja dipisah: **`fb128c93`** modul daun `lux/backtest/manifest.py` + pengujian, RAMALAN **758** TEPAT (run `30215769103`); **`43cd4eed`** `muat_konteks` memanggil `jalur_manifest(opsi.interval, opsi.out)` + medan `parameter_run.manifest_aset` + 3 tripwire, RAMALAN **761** TEPAT (run `30215936212`). Jalur 1h **bit-identik**; gerbang **tidak dilemahkan** — sebelumnya mustahil lulus pada 4h, sesudahnya mungkin lulus dan mungkin gagal.

**Utang terbuka:** langkah 2 menulis ulang `runner.py` seutuhnya. Uji tidak menjaga prosa komentar dan docstring. Pembanding: blob **`fc79e070bbf6ad6f48898958a4942bac876949ca`**. Utang sejenis untuk `run_h013.py`: blob **`418f6084`**.

### CACAT KELAS KEDUA BELAS — ambang tanpa satuan penarikan (ADR-028)

Yang dipakai selama dua belas hipotesis adalah **per perdagangan**, sehingga galat baku dapat dikecilkan hanya dengan menambah simbol. H-013 memperlihatkannya telanjang: SS berjarak **+2,99 galat baku** dari ambang atas `n = 60.018`; dipasangkan menurut bulan, bootstrap **memuat nol**. **ADR-028 (`48c83d59`) mematok:** satuan resmi **bulan kalender UTC (73 unit)** menurut waktu **masuk**; **simbol (437)** sebagai pembanding, bukan pengganti; **per perdagangan DILARANG sebagai bukti keberartian** dan wajib berlabel `taksiran_bawah`; tidak satu angka ambang ADR-015 pun digeser.

**Sebelas penolakan H-001b–H-012 tetap berdiri dan tetap haram dihitung ulang.** Arah biasnya melindungi mereka: per-perdagangan **melebihkan** keyakinan. Yang **tidak** dilindungi adalah **H-010** — setiap p yang pernah dikutip untuknya lebih lemah daripada tertulis; statusnya tidak berubah, ia sudah gagal pada 0,0631.

### AUDIT EMPAT BELAS WORKFLOW — SELESAI

| Workflow | `git pull --rebase --autostash` | Catatan |
|---|---|---|
| `tests.yml` | **ada** | filter `lux/**`, `tests/**`, dirinya sendiri |
| `funding.yml` | **ada** (job `gabung`) | masih memakai `reports/universe_layak.json` (447 pra-lantai) |
| `funding_check.yml` | **ada** | masukan sama |
| `universe.yml` | **ada** | gerbang ditegakkan **sesudah** commit, disengaja |
| `doctor.yml` | **ada** | `set +e` disengaja: kegagalan probe adalah data |
| `backfill_daily.yml` | **ada** | **satu-satunya berjadwal**: `cron: '0 2 * * 1'`, unggah rilis `--clobber` |
| `notion_asap.yml` | **TIDAK ADA** | `git push` polos, `git commit ... \|\| echo` menelan kegagalan |
| `h013b.yml` | **ada, di dalam lingkaran ulang** | sepuluh penulis satu cabang; pola sekali-tarik tidak cukup |

Dengan `validate.yml`, `potong_ekor.yml`, `backtest.yml`, `ingest_tier_b.yml`, `geometri.yml`, dan `berpasangan.yml`, maka **tiga belas dari empat belas** memakai pola itu.

**Temuan yang tidak dicari:** `backfill_daily.yml` berjalan setiap Senin 02:00 UTC tanpa dipicu manusia, mengunggah Parquet dengan `--clobber`, dan mengomit ke `reports/` — ia dapat mengubah aset dan laporan tanpa saya memicunya, dan sesudah ADR-025 ia mengancam manifest keutuhan (ADR-025 R4).

### TEMUAN S17 — lima cacat buta-interval, semuanya ditutup

| # | Cacat | Akibat bila 4h dijalankan apa adanya | Ditutup di |
|---|---|---|---|
| 1 | `validate_run` menulis `universe_layak.json` tanpa interval | keluaran 4h menimpa masukan 1h | `02933b85` |
| 2 | `muat_ambang` membaca `min_bar_1h` untuk interval apa pun | lantai 8.760 bar dipakai untuk 4h (= 4 tahun) | `fe7fd30e` |
| 3 | `MIN_PANJANG` / `MIN_BAR` buta interval di `potong_ekor` | ekor 1–3 hari lolos pada 4h | `6aacef40` |
| 4 | keluaran `potong_ekor` 4h menimpa masukan backtest 1h | dataset H-012 tertimpa tanpa pesan galat | `6aacef40` + pagar `5296162d` |
| 5 | **`muat_ohlcv` memangkas ekor dengan ambang 1h** | **dua definisi ekor; yang menentukan hasil adalah yang salah** | `409343f3` |

Cacat **keenam** (`maks_umur_bar` 168 = 28 hari pada 4h) ditutup ADR-020; **ketujuh** (jendela walk-forward 4320/2160/168 → **1.080/540/42**, satu jendela 1.862 bar) ditutup ADR-023 (`4007e189`, dilaksanakan `8bda1473`). `pemanasan` 200 **tidak** dikonversi dengan sengaja, dan ketidaksimetrisan itu dijaga pengujian. Terbukti di run: **4.082 jendela per sel**. Cacat **kedelapan** aturan 39; **kesembilan** dan **kesepuluh** ADR-024; **kesebelas** ADR-025; **kedua belas** ADR-028; **ketiga belas** ADR-031.

### CACAT KELAS KEDELAPAN — angka di config yang tidak pernah dibaca program

Run H-013 **pertama** (`30213913942`, commit `135b159c`) mati di pagar pra-terbang butir 3: `assert dasar.maks_biaya_masuk_R == AMBANG_BIAYA_MASUK_R`. Sebabnya dibaca verbatim dari `run_h002.py` (blob `8bf480da`): **`muat_konfig_h002` memetakan delapan kunci saja** — `fee`, `slippage`, `atr_periode`, `atr_pengali_stop`, `risiko_per_trade`, `maks_umur_bar`, `maks_carry_R`, `jendela_carry_hari`. `maks_biaya_masuk_R` dan `stop_hormati_celah` tidak ada di sana meski tertulis di `config/lux.yaml` sebagai `0.5` dan `true`.

Perbaikannya **tidak menyentuh pemuat lama**: `run_h013.dasar_riset` memasang kedua medan eksplisit — commit **`ab3e9792`**, **739** uji, ramalan tepat. Satu uji **mengunci cacatnya sebagai perilaku**: config uji bernilai `0.5` tetap wajib menghasilkan `0.0`. Pagar butir 3 **diperkuat** (`93a4309b`). **H-012 tidak terkena.**

### UTANG TEKNIS — kunci config yang tidak pernah dibaca

1. `universe.maks_rasio_bar_datar: 0.30` — **tidak dibaca gerbang backtest**; 0,30 hidup sebagai bawaan fungsi dan literal.
2. `risiko.maks_biaya_masuk_R: 0.5` — tidak dipetakan `muat_konfig_h002` (dipasang ulang oleh `dasar_riset`).
3. `risiko.stop_hormati_celah: true` — sama.

Keberatan ADR-018 yang masih berdiri: `MAKS_RASIO_DATAR = 0.10` dipakai untuk kedua interval padahal rasio bar datar 4h mekanis lebih kecil, jadi gerbang itu **lebih longgar** di 4h. Menggesernya sesudah melihat hasil 4h melanggar aturan 13.

### KERANGKA 4h — semesta berdiri sendiri, dan kesamaannya diperiksa

**Validasi 4h**, run **`30211176709`**, ADR-017 (`494c9bbc`): **3.636.733 baris / 790 simbol**; **layak 447**; tidak layak 343 (riwayat pendek 277, bar datar 74, likuiditas 77); celah 112; duplikat **0**. Keempat ramalan benar.

**Pemangkasan ekor 4h**, run **`30211673239`**, ADR-018 (`30a6d228`): ambang **6 bar**, lantai 2.190; **790 dipindai** · **141 berekor datar** · **270.398 bar dipangkas** · 447 → **438 layak / 9 ditolak** · **nol** penolakan `maks_rasio`. Selisih ramalan bar −82 (0,030%).

**Aturan 23 dijalankan dua kali:** 438 simbol 4h (blob `e7d0f5ca`) dibandingkan **simbol per simbol** dengan 438 simbol 1h — **identik**. Blob `universe_layak_v2.json` identik sebelum dan sesudah run 4h (`a484670f`). **Ambang 4h benar-benar diturunkan ulang:** `universe_layak_v2_4h.json` memuat `"interval":"4h"`, `"min_bar":2190`, `"min_panjang":6`.

**ASET 4h TERVERIFIKASI ADA** di rilis `tier-b-v1` (id `359778114`): 12 berkas, 157.628.619 B.

**Kelayakan 1h lawan 4h — angka identik, dan itu BELUM dijelaskan:** kedua laporan validasi melaporkan **447 layak / 790**, 343 ditolak, 277 riwayat pendek, 77 likuiditas tipis, **74 bar datar**, 112 celah — sama persis — sementara cacah bar berbeda benar (BTCUSDT 57.552 lawan 14.388). **Ini memerlukan verifikasi.**

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
| `47ef9a90` · `ba42a401` · `e7697300` · `1a3e1e5d` · `409343f3` | 702 · 703 · 709 · 711 · 714 | sama | TEPAT |
| ADR-020 langkah 1–3 | 716 · 721 · 734 | sama | TEPAT |
| `8bda1473` · `ab3e9792` | 737 · 739 | sama | TEPAT |
| `48cf1b9f` · `fb128c93` · `43cd4eed` | 749 · 758 · 761 | sama | TEPAT |
| `b0e79220` (cacat kesepuluh) | **767** | 767 | TEPAT |
| `05df8b78` (`sebaran_nol.py`) | **779** | 779 | TEPAT |
| `4f09c8d5` (`run_h013b.py`) | **795** | 795 | TEPAT |
| `0859e8dd` (`gabung_h013b.py`) | **811** | **811 passed in 3,24s** | TEPAT |

Jejak: 444 → … → 761 → 767 → 779 → 795 → **811**. **Sembilan belas ramalan cacah berturut-turut tepat.** Blob `reports/tests.md` terakhir: **`e6bdaf690111c6350be8635dc0fd7eb2bf4ff782`** (run `30217319899`). Berkas markdown **tidak** memicu `tests.yml`, jadi 811 tetap berlaku sesudah commit dokumentasi.

**Papan ramalan perilaku sistem:** S18 nol dari enam tepat; S19 empat dari enam pada Jalur A; **S20 tiga dari lima pada Jalur B**. Gabungan sebelas ramalan angka H-013: sembilan meleset (aturan 46).

### Adjudikasi ramalan Jalur B — tiga tepat, dua meleset

| Ramalan | Isi | Nyata | Putusan |
|---|---|---|---|
| R-D1 | satu pecahan 30 seed selesai < 40 menit | pecahan terlambat mengomit **43 menit 2 detik** sesudah pemicu; sembilan lainnya 28–39 menit | **MELESET** |
| R-D2 | satu pecahan < 1 MB, sepuluh < 10 MB | **370,5 kB** per pecahan, **3,705 MB** bertumpuk | TEPAT |
| R-D3 | ≥ 1 seed melampaui +0,066648R | seed tertinggi **+0,057394R** | **MELESET** |
| R-D4 | simpangan baku antar seed > +0,005570R | **+0,011377R** | TEPAT |
| R-D5 | seed 42 = +0,01180570125176449R dalam 1e-12 | penggabung keluar 0 | TEPAT |

**R-D1:** yang diramalkan adalah lamanya pecahan berjalan; yang dapat diukur hanyalah selisih waktu commit terhadap pemicu, yang memuat waktu antre dan jeda lingkaran ulang dorong. Log workflow tak terbaca, jadi lama pekerjaan itu sendiri **memerlukan verifikasi** — tetapi bukti satu-satunya melampaui ambang yang saya sebut, jadi ia dicatat MELESET (aturan 19).

**R-D3:** prosa ramalannya berbunyi "bila tidak, permutasinya cacat", dan prosa itu ikut terbantah. Permutasinya **sehat** — rerata nol +0,022916R dan sebarannya rapat serta hampir simetris. Yang salah inferensi saya: dengan simpangan baku 0,011377R, angka 0,066648R terletak sekitar **3,8 simpangan baku** di atas rerata nol, jadi 300 undian memang tidak dapat menyentuhnya. Saya menuntut kejadian berpeluang kecil lalu menyebutnya syarat kesehatan. **Akibatnya `reports/h013b_p.md` yang sudah dikomit memuat prosa yang salah**, sebab teksnya dicetak dari tetapan RAMALAN di sumber — diperbaiki menurut aturan 50, angka tidak disentuh.

### Ramalan beku yang SUDAH teradili di S20

| Kode | Isi | Nyata | Putusan |
|---|---|---|---|
| R-B2 / R-C1 | Jalur B per-perdagangan memberi p ≤ 0,05 tetapi **menyesatkan** | 0,003322 | **TEPAT** |
| R-B3 / R-C2 | Jalur B pada satuan bulan memberi p > 0,05 sehingga H-013 **DITOLAK** | 0,205980 | **TEPAT** |
| R-C3 | selisih p per-perdagangan lawan p bulanan lebih dari satu orde besaran | 0,003322 lawan 0,205980 = faktor **62** | **TEPAT** |

### Ramalan beku yang MASIH belum teradili

| Kode | Isi | Sumber |
|---|---|---|
| R-B1 | run 4h pertama sesudah ADR-025 melaporkan `checksum` "tidak dapat dinilai: manifest baru ditulis pada run ini"; run kedua **lulus** dengan dua belas `ohlcv_4h_*` | ADR-027 §7 |
| R-B4 | pemasangan bulanan **berbobot trade** tetap p > 0,05 | ADR-027 §7 — Jalur B tidak menghitung varian berbobot |
| ADR-016 ramalan 5 | ekspektasi R dengan `stop_hormati_celah` menyala lebih rendah daripada dengan medan mati | ADR-016 |

### H-012 — DITOLAK (ADR-014 §8)

Run **`30200123505`**, commit **`56a325d2`**, sidik **`75f9c7ccd65ec30f`**, **1220,6 detik**, 437 dari 438 simbol, 4.081 jendela.

| Sisi batas | Bulan | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|
| **Tahan (sejak `2026-01`)** | 7 | **22.117** | +922,56 | **+0,041713** |
| Sebelum `2026-01` | 66 | 113.564 | +7.168,96 | +0,063127 |
| Seluruh riwayat | 73 | 135.681 | +8.091,52 | +0,059636 |

Selisih tahan − sebelum **−0,021414R**. **0,041713R < 0,05R → GAGAL.** Sebelas gerbang: **entri_acak GAGAL p 0,06312292358803986** · **invarian_risiko GAGAL −21,3131R** · **funding_ekor GAGAL `funding_maks_R` 0,6601**. Skor entri acak nyata **0,04661R** — persis angka H-010. Sebaran: std 2,22746R, galat baku 0,006047R, CI95 **[0,047784, 0,071489]R** yang **memuat** 0,05. Entri ditolak pengaman **62**. Galat baku itu **per perdagangan**, jadi lebih lemah daripada tertulis — dan arah biasnya tidak menyelamatkan H-012.

### Papan skor hipotesis — TIGA BELAS DINILAI, TIGA BELAS DITOLAK

| ID | Mekanisme | Ekspektasi R | Gerbang gagal | Putusan |
|---|---|---|---|---|
| H-001b | Donchian polos | 0,03086 | `invarian_risiko` −2,5853 | DITOLAK |
| H-002 | Donchian + saringan carry | 0,03159 | tidak ada | DITOLAK |
| H-003 | pembalikan skor-z | −0,24782 | `entri_acak`, `invarian_risiko` | DITOLAK |
| H-004 | Donchian + ADX ≥ 30 | −0,01818 | tidak ada | DITOLAK |
| H-005 | entri retest | −0,03571 | `invarian_risiko` | DITOLAK |
| H-006 | sapuan likuiditas | −0,13449 | `entri_acak`, `invarian_risiko` | DITOLAK |
| H-007 | imbalan dipilih walk-forward | 0,04044 | `invarian_risiko` −1,9769 | DITOLAK |
| H-008 | pengaman carry dilombakan | 0,04126 | `invarian_risiko` −1,9769 | DITOLAK |
| H-009 | pengaman carry dipatok 0,25 | 0,041359 | tidak ada | DITOLAK oleh ambang 0,05R |
| H-010 | grid imbalan {2,4,6,8}, 40 simbol | 0,053028 | tidak ada dari sebelas | LULUS, empat keberatan; **p 0,0631 pada 300 permutasi**; seluruh p-nya per perdagangan, jadi lebih lemah daripada tertulis |
| H-011 | mekanisme H-010 atas 438 simbol | −0,079078 | empat gerbang | **DITOLAK, dan TERCEMAR** |
| H-012 | semesta berlantai 0,004 + pagar 0,5R, sejak 2026-01-01 | **0,041713 (periode tahan)** | `entri_acak` · `invarian_risiko` · `funding_ekor` | **DITOLAK** |
| **H-013** | faktorial 2×2 sinyal × geometri keluar, 4h | SS +0,066648; SS − AS +0,054842 (seed 42) / +0,043732 (rerata nol) | SS: `invarian_risiko`, `checksum` | **DITOLAK — p bulanan 0,205980 > 0,05** (ADR-031) |

Sidik dua belas hipotesis pertama: H-001b `e458f4c82abf6735` · H-002 `16fb57692a6f0888` · H-003 `3a1cdc867f61bf67` · H-004 `98d6a5e15b2cc08b` · H-005 `9c4b6324e79569eb` · H-006 `e503a9a833182b25` · H-007 `7f5e7aeeaa29284b` · H-008 `dfeeea04fd4107f6` · H-009 `eac6c83305bd1069` · H-010 `14b2f3bfa8a754b5` · H-011 `8a6efde6d333d8b5` · H-012 `75f9c7ccd65ec30f`.

**Tiga belas dinilai, tiga belas ditolak. Nol kandidat bertahan.** Yang pernah "lulus" (H-010) lulus pada 100 permutasi dan gagal pada 300.

**Kesimpulan struktural — DITARIK sebagai panduan.** Sampai S17, enam percobaan sisi masuk menghasilkan nol perbaikan sementara empat percobaan sisi keluar menghasilkan seluruh kemajuan. Run H-013 memberi angka berlawanan (sinyal +0,054842 lawan geometri +0,029481), lalu Jalur A dan Jalur B memperlihatkan angka sinyal itu **tidak berarti pada satuan bulan**. Jadi bacaan lama tidak dipulihkan, bacaan baru tidak ditegakkan, dan **geometri keluar belum pernah diuji sendiri dengan mesin p bulanan**.

### TEMUAN S16 — mesin buta terhadap celah harga pada jalur stop

1. Gerbang `invarian_risiko` H-012 gagal pada **−21,3131R** terhadap ambang −1,5R.
2. Diagnostik `lux/analisis/geometri_keluar.py`, run **`30209272338`**: perdagangan itu **STGUSDT**, keluar lewat **`carry`**, `transaksi_R` 0,0559, `funding_R` 0,4825, pelampauan di luar biaya **20,3131R**, `stop_frac` 2,197%, `jam` **1,0**.
3. Tidak satu pun keluar `stop` di bawah −1,5R; stop terburuk **−1,4966R**; median pelampauan jalur stop **0,410263R**.
4. `engine.py` (blob `621298a8`): di blok stop/target, `harga = stop if kena_stop else target`. **Harga bar tidak pernah dipakai.**

**Konsekuensi:** `invarian_risiko` **praktis tidak berdaya pada jalur stop**; dua belas hipotesis pertama dinilai mesin yang **optimistis terhadap risiko celah**; arah biasnya **melawan penolakan**, jadi **tidak ada vonis yang perlu dibalik**, tetapi **tidak satu pun angka R lama boleh disebut konservatif**. Klaim "mekanisme stop sendiri sehat" **DITARIK** (ADR-016 §2). Perbaikan terpasang: `stop_hormati_celah` bawaan **MATI** + `harga_stop_terisi` (`955b419a`), dinyalakan di config (`fb710521`) — dan S18 membuktikan penyalaan lewat config itu **tidak pernah bekerja** untuk pemuat H-002. **Hasil H-001b sampai H-012 TIDAK dihitung ulang.**

**Catatan yang masih berdiri:** pada H-013 `stop_hormati_celah` **menyala** dan `invarian_risiko` **tetap gagal pada keempat sel**, termasuk SS. Jadi kegagalan itu tidak dapat dijelaskan sebagai kebutaan celah, dan besarnya **belum dibaca**.

### SEMESTA, HIMPUNAN TERTAHAN, TITIK IMPAS

**Himpunan tertahan HABIS**: hasil per simbol 438 simbol sudah dilihat (H-011), tabel 73 bulan sudah dilihat (H-012), dimensi 4h sudah terpakai (H-013).

Titik impas `1/(1+imbalan)`: 1R 0,5000 · 2R 0,3333 · 4R 0,2000 · 6R 0,1429 · 8R 0,1111. Di H-009, **194 dari 356 jendela (54,5%)** memilih imbalan 4,0 — versi 16 menulis 226 dan 63,5%; **itu salah**. Seretan: H-002 0,04926 · H-009 0,034614 · H-010 0,036220 · H-011 0,125520 (tercemar) · H-012 **0,035900**.

Pemilihan lookback H-013 per sel (dari 4.082 jendela): SS 20→1682, 55→846, 100→1554 · SH 20→1987, 55→1069, 100→1026 · AS 20→1408, 55→1089, 100→1585 · AH 20→1392, 55→1073, 100→1617.

### MESIN BACKTEST

**`engine.Konfig` — nama medan terverifikasi dari sumber:** `fee` (0,0005), `slippage` (0,0005), `atr_periode` (14), `atr_pengali_stop` (2,0), `risiko_per_trade` (0,005), `imbalan_R` (2,0), `modal_awal` (10.000), `izinkan_short` (True), `maks_umur_bar` (0), `maks_carry_R` (0,0), `jendela_carry_hari` (30), `maks_carry_realisasi_R` (0,0), `maks_biaya_masuk_R` (0,0), **`stop_hormati_celah` (False)**, `pakai_target`. **Tidak ada medan bernama `fee_efektif`** — itu kunci YAML. Lima medan bawaan **MATI** dan dikunci pengujian serta pagar `dataclasses.fields`.

**Urutan pemeriksaan per bar:** umur → carry realisasi → stop/target → entri (pengaman biaya lalu carry proyeksi) → ekuitas. `umur` dan `carry` mengisi pada `o[t]`, `akhir_data` pada `c[-1]`.

Gerbang (11): `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`, `konsentrasi`, `funding_ekor`. **Tidak dapat dinilai = GAGAL.**

**`runner.Opsi`** (pembanding blob `fc79e070`): `dir_aset`, `out=reports`, `interval="1h"`, `universe=reports/universe_layak_v2.json`, `akhir_sejati`, `limit=40`, `panjang_latih=4320`, `panjang_uji=2160`, `embargo=168`, `pemanasan=200`, `ulangan=100`, `sampel_permutasi=10`, `min_median_stop_frac=0.0`. `Konteks(bingkai, jadwal, akhir, semesta, sampel, gerbang_cs, semesta_layak, mati, saringan)`. **`muat_konteks` memakai `jalur_manifest(opsi.interval, opsi.out)`** dan menulis `parameter_run.manifest_aset`.

**`jalankan_spek` mengembalikan** `id, nama, sidik, ekspektasi_R, total_R, trade, jendela_positif, jumlah_jendela, p_entri_acak, gerbang_gagal, lulus, alasan, alasan_keluar, entri_ditolak_biaya, simbol_dibuang_lantai, bulan_dengan_trade (CACAH saja), rerata_transaksi_R, retensi_drop_1, porsi_funding_ekor_maks, std_R, galat_baku_R, jarak_galat_baku, detik` — dan menulis `out/backtest_{spek.nama}.json` + `.md` dengan **nama berkas yang sama setiap panggilan** (aturan 47 dan bahaya penimpaan Jalur B).

**Modul H-013** (`lux/backtest/run_h013.py`, blob `239b88d0`, pembanding `418f6084`): `NAMA_SEL` (SS, SH, AS, AH) · `dasar_riset(konfig)` · `permutasi_sinyal` · `sinyal_acak` (**tanpa seed**) · `kontribusi` · `prosa_kontribusi`. Beku: `IMBALAN_BEKU` 2,0 · `H_BAR` 48 · `UMUR_SEL_STOP` 42 · `SEED_PERMUTASI` 42 · `AMBANG_KONTRIBUSI_SINYAL` 0,020 · `MIN_ULANGAN` 300 · `MIN_TRADE_SEL` 100 · `PEMANASAN` 200 · `SKOR_ACAK_TERDAHULU` 0,04661.

**Modul Jalur A** (`lux/analisis/berpasangan.py`, blob `a9fba624`): `SEED=20260727`, `ULANGAN=10000`, `pasangkan`, `pasangan_simbol`, `pasangan_bulan`, `uji_tanda`, `bootstrap`, `ringkas` (**selalu** `memenuhi_adr015: False`). **Tidak ada R per jendela di berkas laporan mana pun** (aturan 43).

**Modul manifest** (`lux/backtest/manifest.py`): `jalur_manifest(interval, out)` — modul daun; 1h → `manifest_aset.json`, lain → `manifest_aset_<interval>.json`.

### DATASET TIER B PUTARAN 2

**14.545.679 bar 1h dan 3.636.733 bar 4h**, 790 simbol, rasio 3,9996, ~703 MB. 1h: 447 valid → v2 **438** → berlantai **437**. 4h: 447 valid → v2 **438** (identik 1h, terperiksa) → berlantai **437** pada H-013. Funding 1.982.017 baris, 3 celah sejati, 79,1% positif; run H-013 memuat **447 jadwal funding** dan memindai **790 simbol** untuk survivorship.

### Kapasitas runner dan konektivitas

4 vCPU, 15 GB RAM. **Batas 6 jam per job yang mengikat, bukan disk.** H-012 memakai 1220,6 s; H-013 empat sel sekitar sepuluh menit termasuk unduhan; **satu pecahan Jalur B 30 seed mengomit 28–43 menit sesudah pemicu, sepuluh pecahan paralel dengan `max-parallel: 10`**. Sel AS ~75 detik per lintasan penuh, jadi 300 seed berurut ≈ 6,25 jam — di atas batas, karena itu matriks. python 3.12.13, numpy 2.5.1, pytest 9.1.1, pandas 2.2.3, pyarrow 17.0.0, **tanpa scipy**, **tanpa requests**. CDN `data.binance.vision` 200; REST `fapi.binance.com` **451 permanen**. Timeout: backtest 330, validate 120, potong_ekor 60, ingest 330, berpasangan 20, **h013b pecahan 180 dan penggabung 30**.

### Batas alat agen dan solusinya

- Daftar alat GitHub **tidak memuat satu pun fungsi Actions**. Diverifikasi ulang di S18, S19, dan S20.
- `search_code` **nol hasil di repo ini**. `get_file_contents` menuntut SHA 40 karakter penuh, tetapi **menerima `ref: "main"`**, dan pada direktori ia memberi **ukuran berkas** — itulah cara mengadili ramalan ukuran tanpa menarik isinya.
- `push_files` **mengganti seluruh isi berkas**; baca dulu sebelum menulis ulang, dan baca ulang muatannya sebelum mengirim (aturan 35). **Tidak ada mode tambal.**
- Filter `paths` per berkas: menyentuh `.github/workflows/backtest.yml` atau `h013b.yml` **langsung memulai run**. `tests.yml` memfilter `lux/**` dan `tests/**`, jadi perubahan `config/`, `journal/`, `decisions/`, dan `STATE.md` **tidak** memicunya.
- **Kabar buruk datang dalam 23–32 detik; kabar baik 10–45 menit** — kecuali `tests.yml`, yang memberi kabar **baik** dalam ~23 detik juga. Jadi jangan membaca cepatnya laporan uji sebagai kegagalan; **baca isinya**.
- **Pada workflow matriks, diam pada menit kelima adalah tanda baik**, sebab kegagalan pecahan tetap mengomit lognya lewat `if: always()`.
- **Commit laporan tanpa berkas hasil berarti run GAGAL. Blob laporan yang tidak berubah berarti belum ditulis.** Berkas yang belum lahir memberi "path does not point to a file", dan itu **bukan** galat alat.
- **Beberapa pekerjaan yang mengomit ke satu cabang menuntut lingkaran ulang dorong**; yang kalah lomba hilang **tanpa suara** (ADR-030 R3).
- **`backfill_daily.yml` berjadwal mingguan**, jadi tidak setiap perubahan blob berasal dari saya.
- **Modul baru berdiri hijau sendiri lebih dulu. Baca modulnya sebelum menulis kode terhadapnya.**

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1–3**, **metrik celah funding**, **circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`).
- **S12:** STATE v11 dan v13 menaikkan kekeliruan menjadi fakta; ditarik v12 dan v14.
- **S13:** "226 dari 356 jendela (63,5%)" padahal **194 (54,5%)**.
- **S15:** empat run gagal berturut (`30198306280` · `30198631730` · `30198840830` · `30198942815`). Aturan 31–34.
- **S16:** dua commit cacat (`953ce24a`, `2a0f8545`); dua ramalan cacah salah; klaim "mekanisme stop sehat" ditarik. Aturan 35–36.
- **S17:** lima cacat buta-interval; ramalan 693 salah; klaim v21 tentang `git pull --rebase` salah. Aturan 37–38.
- **S18:** cacat kelas kedelapan, kesembilan, kesepuluh. Aturan 39–41.
- **S19:** cacat kesebelas dan kedua belas. **Kekeliruan saya sendiri:** ADR-024 menjadwalkan uji per jendela yang **mustahil** karena datanya tidak ada di laporan; dikoreksi ADR-026. Dua ramalan Jalur A meleset. Aturan 42–46.
- **S20:** cacat kelas **ketiga belas** (besaran terhadap satu undian nol). **Dua rancangan Jalur B saya sendiri jatuh sebelum ditulis** (ADR-029 §2): agregat bulanan dari `jalankan_spek` mustahil sebab `bulan_dengan_trade` adalah **cacah** — "saya menganggap angka tersedia karena namanya muncul"; dan nama laporan unik per seed akan melahirkan ~130 MB. **Satu bahaya penimpaan diam-diam** tertangkap hanya karena membaca ulang `runner.py` sebelum menulis. **Dua ramalan Jalur B meleset**, salah satunya berikut alasannya (R-D3). Aturan 47–50.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| **Besar kegagalan `invarian_risiko` pada sel SS** | baca `reports/backtest_h013_ss_sinyal_stop.json` (432.200 B) lewat skrip sisi runner, **jangan** ditarik ke konteks |
| **Lama satu pecahan Jalur B tanpa waktu antre dan tanpa jeda dorong** | log workflow tak terbaca; hanya dapat diukur bila pecahan mencetak `detik` ke berkasnya |
| **Gerbang `checksum` 4h lulus pada run 4h KEDUA sesudah ADR-025** | R-B1; run pertama akan menulis manifest baru dan melapor "tidak dapat dinilai" |
| **Prosa dan komentar `runner.py` tidak bergeser oleh penulisan ulang `43cd4eed`** | bandingkan terhadap blob `fc79e070bbf6ad6f48898958a4942bac876949ca` |
| **Prosa `run_h013.py` tidak bergeser oleh penulisan ulang `b0e79220`** | bandingkan terhadap blob `418f6084` |
| Angka kelayakan 1h dan 4h yang identik (447/74/112) benar, bukan berkas yang tertukar | bandingkan `reports/diag_datar.json` terhadap perhitungan bar datar 4h; bar datar 4h semestinya **≤ 74** |
| STGUSDT benar-benar bergerak melawan ~46,8% dalam rentang ~satu bar 1h | bar itu di rilis artefak, dan sandbox tanpa jaringan |
| Ekspektasi R dengan `stop_hormati_celah` menyala lebih rendah daripada dengan medan mati | ramalan 5 ADR-016; **belum teradili** |
| **Geometri keluar (SS − SH +0,029481R) berarti pada satuan bulan** | belum diuji; mesin p bulanan sudah ada dan tinggal diarahkan |
| Funding sebagai **sinyal** memuat informasi arah | belum pernah diuji |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap universe layak v2 438 |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |

**Difalsifikasi sebelumnya:** saringan rezim tren memperbaiki breakout · retest memperkecil biaya per R · SMC yang dapat dikodekan punya keunggulan · "biaya menjaga risiko memakan ekspektasi" · "ekspektasi bergantung umur simbol" · "kerugian ekor dari bar menganga pada stop" · sinyal `breakout_atr` punya keunggulan yang bertahan di waktu pada 1h (H-012) · lantai 0,004 menutup **seluruh** jalan masuk degenerasi (sebagian) · "hasil 40 simbol mewakili 438 simbol" · dugaan bahwa `gabung_gerbang` membuang syarat deret datar · **"jendela walk-forward adalah jumlah bar"** (ADR-023) · **"nilai di `config/lux.yaml` sampai ke mesin"** (aturan 39) · **"semesta 4h disalin dari 1h"** · **"laporan memuat R per jendela"** (aturan 43) · **"sumbangan sinyal tersebar merata di waktu"** (fraksi bulan positif 0,5342) · **"SH < AH menuntut penjelasan"** (derau) · **"laporan memuat agregat bulanan yang dapat dipakai langsung"** (ADR-029 §2) · **"sebaran nol cukup lebar sampai menyentuh +0,066648R"** (R-D3; 3,8 simpangan baku) · **"sumbangan sinyal +0,054842R adalah besaran yang sah tanpa menyebut seed"** (aturan 49).

**Terbukti benar:** imbalan lebih besar menaikkan ekspektasi (+28%) · lama pegang membesarkan kerugian ekor · keunggulan bertahan bila penyumbang terbesar dibuang (retensi 0,9849; H-013 drop-1 0,06575R, retensi 0,9866) · "H-012 gagal", diramalkan sebelum run · jalur 1h bit-identik sesudah ADR-019 · konversi jendela ADR-023 menghasilkan 4.082 jendela per sel · dugaan manifest 1h lawan aset 4h sebagai sebab `checksum` (blob `2e95a0ff`) · **"p per-perdagangan menyesatkan sementara p bulanan menjatuhkan"** (R-B2, R-B3, R-C3) · **"simpangan baku antar seed melampaui galat baku per perdagangan"** (R-D4).

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 · metrik celah funding putaran 1–4 · seluruh run pilot H-001 termasuk `30170073890` · porsi "101,2%" · nilai gerbang `funding` sebagai bukti funding aman · "226 jendela / 63,5%" · ekspektasi H-010 0,053028R sebagai bukti layak dagang · **+0,060163R** · **+0,059546R** · **+0,060168R** · **281 dari 398 simbol positif** dan median **+0,06343** · **−0,091519R** tanpa sebabnya · **+0,059636R** sebagai kelulusan · **+2.347,27R bulan 2026-01** atau bulan mana pun · gerbang bar datar 4h dan `maks_rasio` 4h sebagai bukti kebersihan data · **`+0,054842R` sebagai kelulusan H-013, dan sebagai besaran mana pun tanpa menyebut seed 42** · **`+0,043732R` sebagai kelulusan** · **`+0,066648R` sebagai bukti layak dagang** · kata "LULUS" pada `reports/backtest_h013_kontribusi.md` · **`p = 0,001100` tingkat simbol sebagai bukti keberartian** · **`p = 0,003322` satuan perdagangan Jalur B sebagai bukti keberartian atau kelulusan** · **p atau galat baku per-perdagangan mana pun sebagai bukti keberartian**, termasuk "+2,99 galat baku" · **prosa R-D3 di `reports/h013b_p.md` sebagai penilaian atas kesehatan permutasi**.

---

## 5. Penghalang aktif

Tidak ada run yang berjalan. Tidak ada yang dibutuhkan dari pengguna. Satu hal yang wajib diingat: **`backfill_daily.yml` dapat berjalan sendiri setiap Senin 02:00 UTC**, dan sesudah ADR-025 ia juga dapat menyentuh berkas manifest keutuhan.

---

## 6. Tindakan berikutnya

1. ~~ADR-017 s.d. ADR-023~~ · ~~jalankan H-013~~ · ~~Jalur A~~ · ~~ADR-025 manifest per interval~~ · ~~ADR-026/027/028~~ · ~~STATE v23, v24~~ · ~~cacat kelas kesepuluh (767)~~ · ~~ADR-029 rancangan Jalur B~~ · ~~Jalur B tiga modul (779, 795, 811)~~ · ~~ADR-030 keputusan langkah 3~~ · ~~jalankan Jalur B (run 30217516013)~~ · ~~ADR-031 adjudikasi~~ · ~~segarkan PROMPT_KELANJUTAN.md~~ · ~~STATE v25~~ — **selesai**.
2. **Perbaiki prosa ramalan R-D3** di `lux/backtest/gabung_h013b.py` menurut aturan 50: koreksi alasannya, **jangan** sentuh angkanya, **jangan** hapus jejak bunyi aslinya.
3. **Baca `reports/backtest_h013_ss_sinyal_stop.json`** untuk nilai `invarian_risiko` SS. Lewat skrip sisi runner yang mencetak ringkasan ke `reports/`, **jangan** menarik 432 KB ke konteks.
4. **Selesaikan pertanyaan bar datar 1h lawan 4h:** bandingkan `reports/diag_datar.json` terhadap perhitungan 4h. Bar 4h datar hanya bila keempat bar 1h datar, jadi penolakan 4h semestinya **≤ 74**.
5. **Nasib `notion_asap.yml`** (`git push` polos, `git commit \|\| echo` yang menelan kegagalan) dan **`backfill_daily.yml`** (cron mingguan + `--clobber`, mengancam ADR-025 R4). Perbaiki atau hapus **dengan keputusan tertulis**.
6. **Tinjau workflow yang mungkin tak lagi diperlukan:** `funding.yml`, `funding_check.yml` (keduanya masih memakai `reports/universe_layak.json` pra-lantai), `doctor.yml`, `universe.yml`. **Jangan hapus tanpa keputusan tertulis.**
7. Utang teknis: **sambungkan `maks_rasio_bar_datar` config ke gerbang** · periksa kunci config lain yang mungkin tak pernah dibaca (aturan 39) · bandingkan `runner.py` terhadap blob `fc79e070` dan `run_h013.py` terhadap `418f6084` · `hasattr`/`__import__` di `test_run_h012.py` · pengujian `biaya_bolak_balik_R` · `pytest` ke `requirements-dev.txt` · nama ganda legasi `potong_ekor` · tripwire tekstual `inspect.getsource` (lemah, dicatat sebagai lemah) · pemetaan `dari_laporan` pelapor Notion terhadap kunci JSON `runner.py`.
8. **Uji geometri keluar sendiri dengan mesin p bulanan** (SS − SH +0,029481R). Mesinnya sudah ada; ia belum pernah diarahkan ke sana, dan tanpa itu "pemisahan sinyal dari geometri keluar" hanya separuh dijawab.
9. **Program riset lanjutan: funding sebagai SINYAL** — satu-satunya dimensi bersih yang tersisa, belum pernah diuji sekali pun, datanya sudah ada. **Pra-registrasi lengkap wajib ditulis dan dikomit lebih dulu**, dengan p bulanan sebagai gerbang (ADR-031 keputusan 5). ADR-015 §4.5 butir 5 tampak terbalik dan §6 sudah berjanji mengakuinya.
10. Perketat `lux/funding.py::gerbang_lulus` · diff Dataset G lama · `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md` · salin ADR-001/ADR-002 ke `decisions/` · naikkan `versi` config sesudah seluruh pembacanya diperiksa · Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, ≥24 shard.

**Yang DILARANG:** menyatakan sistem siap dagang · **menyebut H-013 lulus** · **mengutip +0,054842R, +0,043732R, atau +0,066648R sebagai kelulusan atau kelayakan** · **mengutip p per-perdagangan atau galat baku per-perdagangan sebagai bukti keberartian, termasuk 0,003322** · **mengutip p 0,001100 tingkat simbol sebagai kelulusan** · mengutip +0,060163R atau +0,059636R sebagai kelulusan · **memilih satuan penarikan sesudah hasil terlihat** · membuang simbol atau memilih bulan sesudah melihat hasil · **menyebut H-012 atau H-013 sebagai "H-010 setelah perbaikan"** · menyebut angka R lama **konservatif** · **menghitung ulang H-001b sampai H-012 dengan mesin ADR-016, satuan ADR-028, maupun aturan 49** · menggeser lantai 0,004, pagar 0,5R, `BATAS_VOID` 20, batas `2026-01-01`, **ambang SS − AS 0,020R**, **p ≤ 0,05**, **≥300 ulangan**, **≥100 trade per sel**, `MAKS_RASIO_DATAR` 0,10, atau ambang rasio 0,30 · **melonggarkan ambang dengan berdalih memperbaiki satuan penarikan** · mematok `imbalan_R` ke 8,0 · melombakan `imbalan_R`, `h`, atau `pakai_target` · menurunkan `--ulangan` dari 300 · **menurunkan cakupan seed dari 300 atau memotong ke irisan bulan yang tidak utuh** · menaikkan `maks_umur_bar` dari 168 sebagai penyelamatan · membuang simbol merugi · memakai `konsentrasi` atau `funding_ekor` sebagai penyaring simbol · melombakan ambang pengaman · melonggarkan `invarian_risiko` dari −1,5R · **menurunkan maupun menaikkan ambang ekspektasi 0,05R** · menjadikan `stop_hormati_celah` parameter yang dilombakan · **memperbaiki `muat_konfig_h002` tanpa ADR** · **menurunkan pagar pra-terbang yang menemukan cacat** · **menyentuh `reports/manifest_aset.json`** · **menandai putusan DITOLAK sebagai kegagalan pekerjaan** (aturan 48) · **menulis ulang laporan yang sudah dikomit untuk menutupi ramalan yang meleset** (aturan 50).

---

## 7. Pengawasan otonom — DIHENTIKAN

Agen **LUX Gatekeeper** dan **LUX Gatekeeper Reporter** **tidak dipakai lagi.** Keputusan pengguna, 2026-07-26.

Bukti dari sisi Notion atas baris asap `3a9d5df0-96f9-81df-90a7-f6075d071680`: agen itu mengadili **setiap** baris otomatis dalam sekitar dua menit, termasuk baris yang menyatakan `bukan_hasil_riset=true`, dan memakai `Ditolak` untuk "bukti tidak cukup" padahal `Ditolak` semestinya berarti hipotesis gagal. **Vonis yang salah arti lebih buruk daripada tidak ada vonis** — S18 menambahkan bentuk kedua (vonis benar arti dari separuh kriteria), S19 bentuk ketiga (benar arti, lengkap kriteria, **satuan salah**), dan S20 memperlihatkan bentuk keempat yang paling halus: **vonis yang benar pada satu satuan dan terbalik pada satuan lain di dalam satu run yang sama.**

Kolom `Verdict` di database `LUX — Run Results` karena itu menjadi kolom **manusia**. Pelapor Notion tetap dipertahankan sebagai papan hasil yang dapat dibaca dari ponsel.

---

## 8. Peta repo

| Path | Isi |
|---|---|
| `config/lux.yaml` | seluruh parameter yang memengaruhi hasil; `min_bar_1h` 8.760, `min_bar_4h` 2.190, lantai 0,004, pagar 0,5R, `stop_hormati_celah` true; **satu kunci masih TIDAK DIBACA gerbang**: `maks_rasio_bar_datar`; `versi` masih 2 |
| `lux/kerangka.py` | **modul daun**: `JAM_SEHARI`, `INTERVAL_JAM`, `bar_per_hari`, `jam_interval`, `interval_dikenal`, `bar_dari_hari` |
| `lux/binance_vision.py` | klien arsip: listing S3, unduhan, checksum |
| `lux/universe.py` | universe point-in-time dan klasifikasi kontrak |
| `lux/ingest.py` · `lux/backfill_daily.py` | ingest Tier B dan penutup celah ekor |
| `lux/validate.py` · `lux/validate_run.py` | integritas OHLCV; `muat_ambang(path, interval)` gagal keras |
| `lux/funding.py` · `lux/funding_check.py` | ingest funding dan metrik kisinya; `gerbang_lulus` masih longgar |
| `lux/funding_model.py` | jadwal funding nyata, penagihan, carry |
| `lux/costs.py` | model biaya dalam satuan R; **BUKAN jalur kritis** |
| `lux/degenerasi.py` | ambang 0,004 dan 0,5R, `saring_semesta`, `AMBANG_BIAYA_MASUK_R` |
| `lux/notion_reporter.py` | pelapor baris hasil lewat `urllib.request` |
| `lux/diag_datar.py` · `lux/potong_ekor.py` | diagnosis dan pemangkasan ekor datar; keluaran **berinterval** |
| `lux/praregistrasi.py` | hipotesis sekali tulis; **tidak membaca config** |
| `lux/analisis/{titik_impas,sebaran,periode,geometri_keluar}.py` | aritmetika atas laporan yang dikomit; galat baku **taksiran bawah**, **haram** menegakkan klaim |
| `lux/analisis/berpasangan.py` | **Jalur A**: pemasangan simbol dan bulan, uji tanda, bootstrap |
| `lux/analisis/sebaran_nol.py` | **Jalur B**: `p_ekor_atas`, `p_per_perdagangan` (`mengikat: False`), `p_bulanan` (`mengikat: True`) |
| `lux/strategi/breakout_atr.py` | sinyal kelanjutan (H-001b, H-002, H-007–H-013) |
| `lux/strategi/{reversi_zskor,rezim_adx,retest,smc}.py` | H-003 · H-004 · H-005 · H-006 |
| `lux/backtest/engine.py` | mesin eksekusi; **lima saringan bawaan MATI**; `harga_stop_terisi`; `pakai_target` |
| `lux/backtest/gerbang.py` | sembilan gerbang pertama |
| `lux/backtest/konsentrasi.py` · `funding_ekor.py` | gerbang kesepuluh dan kesebelas |
| `lux/backtest/manifest.py` | **modul daun**: `jalur_manifest(interval, out)` (ADR-025) |
| `lux/backtest/walk_forward.py` | pemilihan parameter dalam sampel; tidak memanggil gerbang apa pun |
| `lux/backtest/run_wf.py` | orkestrator H-001b — **jangan disunting kecuali dengan ADR** |
| `lux/backtest/run_h002.py` · `run_h003.py` | orkestrator beku; **`muat_konfig_h002` memetakan DELAPAN kunci saja** |
| `lux/backtest/runner.py` | runner bersama: muat sekali, lantai semesta, sebelas gerbang, jackknife, ekor funding, sebaran, agregat periode, manifest per interval; **`jalankan_spek` menulis nama berkas yang sama setiap panggilan** |
| `lux/backtest/run_h007.py` | **sumber grid bersama, HARAM disunting** |
| `lux/backtest/run_h010.py` · `run_h011.py` · `run_h012.py` | grid imbalan {2,4,6,8} · `BATAS_H010 = 40` · `BATAS_VOID = 20` |
| `lux/backtest/run_h013.py` | empat sel H-013; `kontribusi` hanya separuh kriteria (ADR-024); prosa md **sudah** diturunkan dari angka (`b0e79220`) |
| `lux/backtest/run_h013b.py` | **Jalur B pecahan**: 30 seed per pecahan, `NAMA_SPEK="h013b_as_seed"`, keluar 3 bila R-D5 meleset |
| `lux/backtest/gabung_h013b.py` | **Jalur B penggabung**: `periksa_cakupan`, `periksa_bulan`, `adjudikasi` dua syarat, keluar 4 bila bulan berbeda |
| `tests/` | **811** pengujian tanpa jaringan, wajib hijau sebelum unduhan |
| `reports/` | keluaran mesin tiap run; empat berkas sel H-013 ~432 KB; sepuluh pecahan Jalur B ~370 kB masing-masing; `h013b_p.json` **satu-satunya berkas putusan H-013 yang sah**; `manifest_aset.json` **hanya 1h** |
| `hipotesis/` | pendaftaran sekali tulis: `H-001b` … `H-012`, `H-013-SS/SH/AS/AH` |
| `decisions/` | ADR-003 … **ADR-031** |
| `journal/` | riwayat per sesi, sampai **`2026-07-27-26.md`** |

**Workflow aktif (14):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`, `notion_asap`, `geometri`, `berpasangan`, **`h013b`**. **Tiga belas dari empat belas** memakai `git pull --rebase --autostash origin main` sebelum push; **`notion_asap.yml` tidak**. **`backfill_daily.yml` satu-satunya berjadwal.** `h013b.yml` satu-satunya matriks dan satu-satunya yang mendorong di dalam lingkaran ulang.

**Dihapus di S7:** `analyze_tail.yml` (`07860a7`), `diagnose.yml` (`f4af734`), `diag_datar.yml` (`41ca693`), `retry_failed.yml` (`3a206c6`).

Release **`tier-b-v1`** (id `359778114`) memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`. **Aset 4h ada: 12 berkas, 157.628.619 B.**

**Rantai commit S18–S20 (naik):** `4007e189` → `8bda1473` → `135b159c` → `ab3e9792` → `93a4309b` → `9ca18373` → `e060749c` → `4a00f8e4` (STATE v23) → `341c1486` (ADR-025+026) → `48cf1b9f` (749) → `a4a4a46a` → `5970c136` → `e3309954` (Jalur A) → `ae149fe9` (ADR-027) → `fb128c93` (758) → `aa59afba` → `43cd4eed` (761) → `e544a952` → `48c83d59` (ADR-028) → `43fc6052` (STATE v24) → `b0e79220` (767) → `1566de0c` → `6c639275` (journal-23) → `d3f44f76` (ADR-029+journal-24) → `05df8b78` (779) → `e61be44f` → `4f09c8d5` (795) → `7ee531b3` → `0859e8dd` (811) → `56a27110` → **`97b36c19`** (h013b.yml, pemicu) → `af470704` (ADR-030+journal-25, ditulis sebelum hasil) → `c849486f` (PROMPT_KELANJUTAN v24+) → sepuluh commit pecahan `lux-h013b` → **`1d746879`** (laporan p, DITOLAK) → `dc028faa` (ADR-031+journal-26) → **STATE v25**.
