# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-26 17:45 WIB (versi 19)

**Tahap sekarang:** S14 — **H-012 SUDAH DIPICU DAN SEDANG BERJALAN.** Kelima commit sisa ADR-014 selesai dan hijau: **615 pengujian lulus, kode keluar 0** (`reports/tests.md` @ `884d6c8e`). `backtest.yml` dibalik paling akhir pada commit **`f7da5cf3`**, dan karena berkas itu memicu dirinya sendiri lewat filter `paths`, run H-012 mulai pada commit tersebut.

**Tahap berikutnya:** **menunggu laporan H-012 dikomit balik**, lalu mengadjudikasi tujuh ramalan ADR-014 §8 satu per satu. Ramalan saya sendiri: **H-012 GAGAL** (ekspektasi periode tahan 0,010–0,045 terhadap ambang 0,05).

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
12. (S12) **Batas risiko tidak dilombakan.** Pengaman di dalam grid berarti menyerahkan keputusan risiko kepada fungsi tujuan yang tidak melihat risiko.
13. (S12) **Peristiwa yang terlalu jarang tidak dapat dipilih oleh pemilih dalam sampel.** Pengaman carry menyala 16 dari 14.925 (0,107%); kelangkaan, bukan biaya, yang membuatnya ditolak 334 lawan 22. Konsekuensi luas: **setiap pengaman yang menargetkan peristiwa langka akan selalu ditolak oleh pemilihan dalam sampel.**
14. (S12) **Ramalan yang salah lebih murah daripada ramalan yang tidak pernah ditulis.**
15. (S12) **Porsi terhadap nilai bersih bukan ukuran konsentrasi.** Pakai jackknife dan penyebut bruto.
16. (S12) **Proksi yang berkorelasi 0,97 dengan hal lain bukan proksi.** Umur dan jumlah perdagangan berkorelasi Spearman +0,9668.
17. (S12) **Gerbang yang memberi jawaban sama pada dua keadaan bertolak belakang tidak memuat informasi.** Syaratnya "memisahkan dua keadaan yang diketahui berbeda", dan itu wajib jadi pengujian.
18. (S12) **Angka jumlah yang ditulis tangan hanya boleh ada di satu tempat, yaitu pengujian tripwire.**
19. (S13) **Margin setipis satu satuan resolusi bukan margin.** `entri_acak` H-010 lulus p 0,049505 pada 100 permutasi; pada 300 permutasi mekanisme yang sama memberi **0,0631** dan **gagal**.
20. (S13) **Ekspektasi yang naik karena penyebutnya menyusut bukan keunggulan yang membesar.** H-010: ekspektasi +28,2%, laba total +0,80%, perdagangan −21,4%.
21. (S13) **Kecurigaan wajib naik, bukan turun, ketika hasilnya menyenangkan.** Tiga dari lima ramalan H-010 salah, ketiganya ke arah yang menguntungkan hipotesis.
22. (S13, ADR-014) **Menuntut kesamaan bit pada agregat pecahan adalah pengujian yang menyala pada perilaku yang benar.** Penjumlahan pecahan tidak asosiatif.
23. (S13, ADR-014) **Pagar yang memastikan masukan identik tidak memastikan masukan sah.** Semua pagar `run_h011` lulus — grid, kandidat, dataset, kriteria, identitas `buat_konfig` — dan semestanya tetap memuat simbol yang satuan risikonya runtuh.
24. (S13, ADR-014) **Satu simbol dapat mendominasi agregat 438 simbol.** Agregat wajib diperiksa terhadap ekstremnya sendiri sebelum ditafsirkan.
25. (S13, ADR-014) **Himpunan tertahan habis pada saat pertama kali dilihat.** Ia hanya bisa dibelanjakan sekali.
26. (S13, ADR-014) **Cacat yang membalik tanda hasil tidak boleh diperbaiki di dalam hipotesis yang sama.** Perbaikannya melahirkan hipotesis baru.
27. (S13, ADR-014) **Eksperimen yang tercemar tidak informatif ke arah mana pun.** Ia memakan satu hipotesis tanpa membayar pengetahuan; catat sebagai kerugian, bukan kemajuan.
28. (S13, ADR-014) **Saringan yang menolak entri juga menolak saat pemilihan.** Simbol yang degenerat sepanjang riwayat membuat semua kandidatnya berskor −inf, seluruh jendelanya dilewati, dan ia menyumbang **nol** penolakan sekaligus nol perdagangan — jadi ia **hilang dari hitungan penolakan**, bukan menonjol di dalamnya. Yang membuatnya terlihat hanya lantai semesta.
29. (S14) **Pra-registrasi wajib diperiksa terhadap apa yang benar-benar dapat dihitung dari laporan.** Kriteria utama H-012 dibekukan di ADR-014 §8 sejak sebelum S14, tetapi laporan backtest **tidak memuat satu pun stempel waktu perdagangan**, sehingga kriteria itu mustahil dihitung dari berkas yang dikomit. Ambang yang tidak dapat dihitung adalah ambang yang kelak diganti diam-diam oleh angka lain yang kebetulan tersedia. Dua commit S14 dipakai menutup lubang itu **sebelum** satu angka hasil dilihat.
30. (S14) **Kriteria utama dihitung dari berkas laporan yang dikomit, bukan dari nilai yang beredar di memori run.** Pola ini dimulai `run_h011` dan diteruskan `run_h012`; ia satu-satunya bentuk yang dapat diperiksa tangan oleh siapa pun setahun kemudian.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa. Seluruh komputasi berjalan di GitHub Actions.

---

## 3. Fakta terverifikasi

### H-012 — DIPICU, HASIL BELUM ADA (ADR-014 §8)

Enam commit S14, seluruhnya di `main`, berurutan sesuai urutan wajib ADR-014:

| Commit | Isi | Pengujian |
|---|---|---|
| `bfb5f2d9` | `runner.py`: lantai semesta di `muat_konteks` lewat `degenerasi.saring_semesta`, `entri_ditolak_biaya` sebagai alasan tersendiri di laporan, simbol dibuang tertulis beserta `median_stop_frac` + `tests/test_runner_lantai.py` | 578 → **589** |
| `81b213b2` | `config/lux.yaml`: `universe.min_median_stop_frac: 0.004`, `risiko.maks_biaya_masuk_R: 0.5` | 589 |
| `0684bca0` | `lux/analisis/periode.py` + `tests/test_periode.py`, hijau sendiri lebih dulu | 589 → **601** |
| `f6efbd7a` | sambungan `periode` ke `runner.jalankan_spek`: blok `agregat_periode` di JSON + tabel Markdown | **601** |
| `884d6c8e` | `lux/backtest/run_h012.py` + `tests/test_run_h012.py` | 601 → **615** |
| `f7da5cf3` | `backtest.yml` dibalik ke H-012, langkah `impor` ditulis ulang — **memicu run** | — |

**Pengujian terverifikasi:** `reports/tests.md` @ `f6efbd7a` → **601 lulus, kode keluar 0**, 2,51 detik. `reports/tests.md` @ `884d6c8e` (run **`30198241082`**) → **615 lulus, kode keluar 0**, 2,99 detik. **Ketiga ramalan jumlah pengujian S14 tepat** (589, 601, 615), ditulis sebelum laporan dibaca. Ini menjadi ramalan jumlah pengujian tepat kesepuluh berturut-turut.

**Yang dipatok sebelum run, dan haram digeser sesudahnya:**

- Lantai `universe.min_median_stop_frac` = **0,004**, dan pengaman `risiko.maks_biaya_masuk_R` = **0,5**. Keduanya **satu batas yang dinyatakan dua kali**: biaya bolak-balik `2×(fee_efektif + slippage)` = 0,002 dari harga menjadi tepat 0,5R pada jarak stop 0,004. Aritmetika itu **dihitung** di langkah `impor` dan di `run_h012`, bukan dipercaya sebagai label.
- **Periode tahan-waktu beku: sejak `2026-01-01` UTC**, yaitu `PERIODE_TAHAN_MS = 1767225600000`, bulan `2026-01`. Tanggal kalender, bukan jendela bergulir, karena "n hari terakhir" bergeser tiap kali data bertambah dan batas yang bergeser bukan batas. Titik batas dimiliki **periode tahan** (`>=`).
- **`BATAS_VOID = 20`.** Bila lantai membuang lebih dari 20 simbol, `run_h012` mencetak H-012 BATAL dan keluar dengan kode 2 **tanpa mengadili apa pun**, karena semesta yang menyusut sebanyak itu bukan lagi semesta yang dipra-registrasi. Jalan keluarnya ADR baru, bukan menurunkan lantai dan bukan menaikkan `BATAS_VOID`.
- Kriteria pra-registrasi **tidak bergerak**: `min_ekspektasi_R` 0,05 · `min_trade_luar_sampel` 100 · `maks_p_entri_acak` 0,05 · `min_jendela_positif_rasio` 0,5. `--ulangan` minimum **300**; `run_h012` menolak di bawahnya.
- Mekanisme **identik H-010/H-009**: `kandidat_h010 is run_h010.kandidat`, `buat_konfig_h010 is run_h009.buat_konfig`, `lookback` [20, 55, 100], `imbalan_R` [2, 4, 6, 8], 12 kombinasi. `maks_biaya_masuk_R` dilarang masuk ruang pencarian (aturan 12).
- `Konfig` H-012 dibentuk lewat `dataclasses.replace(muat_konfig_h002(...), maks_biaya_masuk_R=...)`, sebab `run_h002` dibekukan dan tidak membaca kunci ADR-014. Modul beku tidak disunting.

**Tujuh ramalan H-012, tertulis di `run_h012.RAMALAN` dan dicetak sebelum run:** (1) 1–6 simbol dibuang lantai, >20 berarti BATAL · (2) ekspektasi seluruh riwayat 0,050–0,065, **hanya konsistensi, haram jadi bukti** · (3) **ekspektasi periode tahan 0,010–0,045, jadi H-012 GAGAL** · (4) p entri acak 0,01–0,20, p > 0,05 menjatuhkan meski ekspektasinya tinggi · (5) 500–5.000 entri ditolak pengaman, tafsirnya sempit karena aturan 28 · (6) `invarian_risiko` LULUS; bila masih gagal, seluruh ADR-014 keliru · (7) durasi 10–60 menit.

**Batas kejujuran yang wajib ikut dikutip.** Periode tahan **tidak** sebersih himpunan simbol tertahan sebelum H-011. Riwayat yang sudah dilihat memuat periode itu di dalam agregatnya; yang belum pernah dilihat adalah **angkanya secara terpisah**. Klaim "data ini belum pernah disentuh" tidak sah. Selain itu perdagangan yang dibuka sesaat sebelum batas dapat ditutup sesudahnya, dan rembesan itu terbatas oleh `maks_umur_bar` 168 bar = tujuh hari, arahnya tidak diketahui.

**Dua utang teknis S14, dicatat terbuka:**

1. `runner.median_stop_frac_bingkai` memakai ATR bar `t` dibagi **close** bar `t`, sedangkan mesin memakai ATR bar `t-1` terhadap **open** bar `t` yang sudah diberi slippage. Selisihnya per mil; kriteria yang dinilai berselisih tiga orde besaran (3,2e−06 lawan 4e−03), jadi ia tidak dapat memindahkan satu simbol pun melewati lantai. Tertulis di docstring.
2. `tests/test_run_h012.py::test_kriteria_tidak_bergerak` memakai satu baris `hasattr` + `__import__` yang jelek dan rapuh secara gaya. Ia hijau, tetapi wajib dirapikan menjadi impor `engine.Konfig` biasa.

### H-011 — DITOLAK, dan yang terbongkar adalah cacat semesta (ADR-014)

Run **`30194733599`**, laporan **`2bb7b963`**, sidik **`8a6efde6d333d8b5`**, **838,1 detik**, 438 simbol, 12 kombinasi. Berkas `reports/backtest_h011_semesta_penuh.{md,json}`.

Kriteria utama dihitung tangan dari `per_simbol`, bukan dari blok `putusan`:

| Kelompok | n simbol | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|
| Teruji (40 pertama alfabet) | 40 | 11.734 | +622,2348 | **+0,053028** |
| **Tertahan (398)** | 398 | 124.603 | **−11.403,5584** | **−0,091519** |
| Seluruh semesta | 438 | 136.337 | −10.781,3236 | −0,079078 |

Baris teruji **identik bit-per-bit** dengan H-010 (622,2348185492804; 0,05302836360569971). Mekanisme benar-benar diimpor tanpa perubahan; hanya semestanya berbeda.

**Sebaran:** std per perdagangan **4,24670** (ddof=1, n 136.337), galat baku **0,011501**, selang 95% **[−0,101621, −0,056536]**, jarak ke ambang **−0,129078R = −11,22 galat baku**. Kuartil R: min −470,0612 · Q1 −1,0635 · median **−1,0402** · Q3 −0,4224 · maks 12,9076. Sah untuk **menjatuhkan**, bukan menegakkan.

**Gerbang gagal:** `entri_acak` p **0,0631** (18/300) · `invarian_risiko` **−470,0612R** · `konsentrasi` tak dapat dinilai · `funding_ekor` lewat `funding_maks_R` **2,3900** > 0,50. Lulus: forward_fill 0,0013 · buy_and_hold 0,8387 unggul 394/438 · lookahead 0,0 · funding 154.526,99 · overlap 0,0 · checksum 0,0 · survivorship 1,0.

Alasan keluar: stop 102.068 · target 21.649 · umur 9.699 · akhir_data 2.479 · carry 442. Jendela positif 2.246/4.092 = 0,54887. Rerata `stop_frac` 0,03489824448280757.

**Penyebab tunggal:** `USDCUSDT` — 29.527 bar, 11 jendela, 649 perdagangan, total_R **−18.861,0596**, ekspektasi **−29,06173**. Pasangan stablecoin: ATR/harga hampir nol, `stop_frac` terburuk **3,1984170825288993e−06**, `transaksi_R` **312,7333** pada satu perdagangan ber-`R` **−470,0612** yang kotornya hanya −157,3278. Sepuluh perdagangan terburuk dari 438 simbol semuanya miliknya. Rerata biaya transaksi melonjak **0,03534R → 0,12552R**; 478 perdagangan berbiaya lebih dari 1R. Ini **cacat pengukuran**, bukan temuan pasar.

**Adjudikasi tujuh ramalan ADR-013 §8:** (1) tertahan 0,020–0,045 → −0,091519 **SALAH** · (2) cabang tak aktif · (3) < 0,020 **TERPICU** · (4) p 0,01–0,15 → 0,0631 **BENAR** dan menolak · (5) trade 100.000–160.000 → 136.337 **BENAR** · (6) retensi ≥ 0,95 → **TAK TERSELESAIKAN** (cacat sejak ditulis) · (7) durasi 15–60 menit → 13,97 menit **SALAH**.

### SEMESTA LAYAK v2 — CACAT, DAN CACATNYA SUDAH DITAMBAL UNTUK H-012

Kriteria lama `config/lux.yaml`: `min_bar_1h` 8760, `min_median_quote_volume_harian` 1.000.000, `maks_rasio_bar_datar` 0,30. **Tidak satu pun menyentuh volatilitas**; USDCUSDT lolos ketiganya dan saringan volume justru menariknya masuk. Cacat berumur sejak ADR-003, tak terlihat selama sepuluh hipotesis karena 40 simbol pertama alfabet tidak memuat pasangan stablecoin.

Sejak `81b213b2` berkas itu memuat `universe.min_median_stop_frac: 0.004` dan `risiko.maks_biaya_masuk_R: 0.5`. Nomor `versi` **tetap 2**, sengaja: belum seluruh pembaca berkas itu diperiksa, jadi menaikkannya adalah perubahan yang akibatnya tidak diketahui. Alasannya tertulis di dalam berkas. Terverifikasi: `muat_konfig_h002` memakai `yaml.safe_load` lalu hanya mengambil kunci yang disebutnya dan tidak memvalidasi kunci asing, jadi penambahan ini **tidak** menjatuhkan pembacaan lama.

Papan skor **tidak** dihitung ulang (aturan 5); ia diberi catatan.

### HIMPUNAN TERTAHAN — HABIS

Hasil per simbol untuk seluruh 438 simbol pada 1h sudah dilihat. Setiap pengujian 1h berikutnya bersifat dalam-sampel pada tingkat semesta. Dimensi yang masih bersih hanya **waktu** (dipakai H-012) dan **kerangka 4h** (belum tervalidasi).

### H-010 — LULUS pada 40 simbol, dengan empat keberatan; TIDAK DIREHABILITASI

Run **`30193898133`**, sidik **`14b2f3bfa8a754b5`**, **117,5 detik**, 40 simbol.

| Kriteria | Ambang | Nilai | Putusan |
|---|---|---|---|
| `min_ekspektasi_R` | ≥ 0,05 | **0,053028** | lulus |
| `min_trade_luar_sampel` | ≥ 100 | 11.734 | lulus |
| `maks_p_entri_acak` | ≤ 0,05 | **0,049505** | lulus, satu satuan resolusi |
| `min_jendela_positif_rasio` | ≥ 0,50 | **0,528090** | lulus |

Gerbang: forward_fill 0,000253 · buy_and_hold 0,798562 · entri_acak p 0,049505 nyata 0,04661R · lookahead 0,0 · invarian_risiko −1,273250 · funding 11.523,31 · overlap 0,0 · checksum 0,0 · survivorship 0,855469 · konsentrasi 0,857845 · funding_ekor 0,167491. Keluar: stop 8.776 · target 1.839 · umur 879 · akhir_data 214 · carry 26. Laju target 0,15672. `total_R` 622,2348185492804.

**Empat keberatan:** (1) p 0,049505 = (4+1)/(100+1), dan **pada 300 permutasi mekanisme yang sama memberi 0,0631 — gagal**; (2) skor nyata entri acak turun **0,10781R → 0,04661R (−56,8%)**, tafsiran paling tidak menyenangkan: keunggulan mungkin **seluruhnya** milik geometri keluar; (3) jendela positif 0,528090 turun dari 0,556180; (4) diukur pada semesta yang kini diketahui cacat.

**Dekomposisi:** kotor R 0,0759727 → 0,0892483 (+17,5%) · transaksi 0,0342866 → 0,0353377 · funding 0,0003276 → 0,0008823 (+169%) · bersih 0,0413585 → 0,0530283 (+28,2%). Agregat: bersih 617,28 → 622,23 (**+0,80%**), perdagangan 14.925 → 11.734 (**−21,4%**). Aturan 20.

**Dinding grid:** imbalan 8,0 dipilih 162 jendela (45,51%), di bawah 54,5% milik batas lama, jadi optimum kini di dalam grid. Di H-011 (4.092 jendela) 8,0 memimpin 1.729 (42,25%). Dinding `lookback` larut: 20→124, 55→116, 100→116.

**Konsentrasi H-010:** 26 untung / 14 rugi · drop-1 0,04549R (retensi **0,857845**) · median simbol +0,04604R · porsi bruto teratas 0,1346 (ADAUSDT) · setara 14,9 simbol. Pencilan **AIOTUSDT 32 perdagangan, +1,79837R**: dilarang dibuang, dilarang dijadikan bukti.

### GERBANG KESEBELAS `funding_ekor` (ADR-011) dan KESEPULUH `konsentrasi` (ADR-010)

`funding_ekor` empat sub-uji: `porsi_funding_ekor_maks` ≤ **0,35** · `funding_maks_R` ≤ **0,50** · `porsi_trade_di_atas_pengaman` ≤ **0,005** · `jadwal_dimuat` wajib. Mengikat mulai H-010. Bukti bergigi: H-008 → 0,467 GAGAL · H-009 → 0,165 lulus · H-010 → 0,167491 lulus · **H-011 → GAGAL lewat `funding_maks_R` 2,3900**, dan yang menjatuhkannya perdagangan USDCUSDT yang sama.

`konsentrasi`: `drop_1_positif` > 0 · `drop_5persen_positif` > 0 · `retensi_drop_1` ≥ 0,60 · `median_simbol_positif` > 0 · `porsi_bruto_teratas` ≤ 0,25 dengan penyebut bruto. **Sub-uji tak dapat dinilai = GAGAL**, terbukti bekerja di H-011.

Konsekuensi diterima sadar: tiga orkestrator beku (`run_wf`, `run_h002`, `run_h003`) hanya menyusun sembilan gerbang.

### H-009 dan keluarga sebelumnya

H-009 run **`30186730437`**, sidik `eac6c83305bd1069`: +0,041359R, 617,28R, 14.925 perdagangan, keluar carry 16, `invarian_risiko` **−1,2698 LULUS**, DITOLAK oleh ambang 0,05R, `entri_acak` p 0,0099. Pengaman memotong tepat sasaran: lima perdagangan terburuk H-008 yang carry-nya melewati 0,25R hilang seluruhnya; lima berikutnya bertahan dengan R identik sampai belasan desimal (ADAUSDT `-1.2697928364736204`). **Nol korban sampingan.** Pemilih mematikan pengaman 334 dari 356 jendela — sebabnya **kelangkaan**, bukan biaya (aturan 13).

**Konsentrasi H-009:** simbol laba 28 → +883,62R, rugi 12 → −266,35R, bersih +617,28R, HHI 0,0621 setara 16,1 simbol, drop-1 retensi 87,0%. **Dilarang:** membuang 12 simbol merugi menaikkan ekspektasi ke ±0,0752R — survivorship bias telanjang.

H-003 run `30175179866`: −0,24782R, `entri_acak` p 1,0000. Bersama H-006: **pada 1h perp USDT, pembalikan jangka pendek rugi sistematis.** Keluarga ADR-006 run `30175665060` ditolak bertiga dengan ambang Bonferroni **0,0167** yang ditetapkan sebelum satu angka terlihat dan bergigi (p H-005 0,0396 akan lolos 0,05).

### Papan skor dua belas hipotesis

| ID | Mekanisme | Ekspektasi R | Gerbang gagal | Putusan |
|---|---|---|---|---|
| H-001b | Donchian polos | 0,03086 | `invarian_risiko` −2,5853 | DITOLAK |
| H-002 | Donchian + saringan carry | 0,03159 | tidak ada | DITOLAK |
| H-003 | pembalikan skor-z | −0,24782 | `entri_acak`, `invarian_risiko` | DITOLAK |
| H-004 | Donchian + ADX ≥ 30 | −0,01818 | tidak ada | DITOLAK |
| H-005 | entri retest | −0,03571 | `invarian_risiko` | DITOLAK |
| H-006 | sapuan likuiditas | −0,13449 | `entri_acak`, `invarian_risiko` | DITOLAK |
| H-007 | imbalan dipilih walk-forward | 0,04044 | `invarian_risiko` −1,9769 | DITOLAK |
| H-008 | pengaman carry dilombakan | 0,04126 | `invarian_risiko` −1,9769 | DITOLAK, pengaman dimatikan pemilih |
| H-009 | pengaman carry dipatok 0,25 | 0,041359 | tidak ada | DITOLAK oleh ambang 0,05R |
| H-010 | grid imbalan {2,4,6,8}, 40 simbol | 0,053028 | tidak ada dari sebelas | LULUS, empat keberatan; **p 0,0631 pada 300 permutasi** |
| H-011 | mekanisme H-010 atas 438 simbol | −0,079078 (tertahan −0,091519) | `entri_acak`, `invarian_risiko`, `konsentrasi`, `funding_ekor` | **DITOLAK, dan TERCEMAR** |
| **H-012** | semesta berlantai 0,004 + pagar 0,5R, dinilai pada periode sejak 2026-01-01 | **belum ada** | belum ada | **SEDANG BERJALAN** |

Sidik: H-001b `e458f4c82abf6735` · H-002 `16fb57692a6f0888` · H-003 `3a1cdc867f61bf67` · H-004 `98d6a5e15b2cc08b` · H-005 `9c4b6324e79569eb` · H-006 `e503a9a833182b25` · H-007 `7f5e7aeeaa29284b` · H-008 `dfeeea04fd4107f6` · H-009 `eac6c83305bd1069` · H-010 `14b2f3bfa8a754b5` · H-011 `8a6efde6d333d8b5`.

**Kesimpulan struktural:** enam percobaan pada sisi **masuk** menghasilkan nol perbaikan; empat percobaan pada sisi **keluar** menghasilkan +28% (H-007), penutupan gerbang risiko (H-009), dan +28% lagi (H-010). **Sisi keluar satu-satunya arah yang pernah memberi leverage**, dan skor entri acak H-010 yang turun 56,8% adalah bukti terkuat sejauh ini bahwa keunggulannya mungkin seluruhnya ada di sana.

### Titik impas

`1/(1+imbalan)`: 1R 0,5000 · 2R 0,3333 · 3R 0,2500 · 4R 0,2000 · 6R 0,1429 · 8R 0,1111. Di H-009, **194 dari 356 jendela (54,5%)** memilih imbalan 4,0. **Versi 16 menulis 226 dan 63,5%; itu salah.**

| Hipotesis | Laju target | Bersih tercatat | Seretan |
|---|---|---|---|
| H-002 | 0,36028 | +0,03159 | 0,04926 |
| H-009 | 0,27544 | +0,041359 | 0,034614 |
| H-010 | 0,15672 | +0,053028 | 0,036220 |
| H-011 | 0,15879 | −0,079078 | 0,125520 (tercemar) |

### MESIN BACKTEST

`lux/backtest/`: `engine.py`, `gerbang.py`, `konsentrasi.py`, `funding_ekor.py`, `walk_forward.py`, `run_wf.py`, `run_h002.py`, `run_h003.py`, `runner.py`, `run_keluarga.py`, `run_h007.py`–`run_h011.py`, **`run_h012.py`**. Analisis: `lux/analisis/{titik_impas,sebaran,periode}.py`. Degenerasi: `lux/degenerasi.py`.

**`lux/degenerasi.py`** (`5af7a6bb`): `AMBANG_MIN_STOP_FRAC = 0.004`, `AMBANG_BIAYA_MASUK_R = 0.5`, `KASUS_USDCUSDT`, dan fungsi `periksa_derivasi`, `stop_frac_deret`, `median_stop_frac`, `layak_stop_frac`, `biaya_masuk_R`, `entri_terlalu_mahal`, `saring_semesta(median_per_simbol, ambang, model)` → `{ambang, n_masuk, n_layak, n_ditolak, layak, ditolak[{symbol, median_stop_frac, biaya_masuk_R, sebab}]}`.

**`lux/analisis/periode.py`** (`0684bca0`): `ms_dari_tanggal`, `bulan_dari_ms`, `dari_perdagangan`, `agregat_per_bulan`, `agregat_sejak`, `agregat_sebelum`, `bandingkan_batas`. Bulan kalender UTC, kepemilikan menurut waktu **masuk**, `math.fsum`, periode kosong → `ekspektasi_R is None` dan `dapat_dinilai False` (bukan nol).

**Rantai impor yang tidak boleh diputus.** `run_h012` mengimpor `IMBALAN_H010`, `LOOKBACK_H010`, `buat_konfig_h010`, `kandidat_h010` dari `run_h010`, dan `AMBANG_CARRY_KERAS`, `DATASET`, `KUNCI_TERLARANG`, `buat_konfig` dari `run_h009` — pola yang sama dengan `run_h011`. `run_h010` mengimpor dari `run_h009` dan `LOOKBACK` dari `run_h007`. `run_h009` mem-`assert` gridnya identik `run_h007`, jadi **`run_h007.IMBALAN` haram disunting**.

**Laporan sekarang memuat** (sejak `bfb5f2d9` dan `f6efbd7a`): `entri_ditolak_biaya`, `entri_ditolak_biaya_per_simbol`, `lantai_semesta` (termasuk tabel simbol dibuang beserta `median_stop_frac` dan `biaya_masuk_R`), `agregat_periode` (per bulan masuk), serta `parameter_run.maks_biaya_masuk_R` dan `parameter_run.min_median_stop_frac`. Penolakan pengaman **tidak** dijumlahkan ke `alasan_keluar`, sebab penolakan bukan perdagangan.

Gerbang: `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`, `konsentrasi`, `funding_ekor`. **Gerbang yang tidak dapat dinilai berarti GAGAL.** Alasan keluar: `stop`, `target`, `umur`, `carry`, `akhir_data`; urutan per bar umur → carry → stop/target → entri → ekuitas; `ALASAN_TIDAK_SELESAI = ("umur", "akhir_data", "carry")`.

Bawaan yang **wajib tetap MATI** supaya H-001b–H-011 dapat diulang: `Konfig().maks_biaya_masuk_R == 0.0`, `Opsi(...).min_median_stop_frac == 0.0`, `Hasil.entri_ditolak_biaya == 0`. Ketiganya dikunci pengujian dan diperiksa lagi di langkah `impor`.

### DATASET TIER B PUTARAN 2

**14.545.679 bar 1h dan 3.636.733 bar 4h**, 790 simbol, rasio 1h:4h **3,9996**, ~703 MB. Validasi 1h: 0 pelanggaran fatal, **447 simbol layak**; ADR-003 memangkas 141 simbol berekor datar (1.081.920 bar, 7,4%), universe layak v2 = **438**. Funding: 1.982.017 baris, 447 simbol, 3 celah sejati, 79,1% positif, jitter maks 47 ms, 295 dari 447 simbol lintas rezim kisi. Carry ekstrem: 1000WHYUSDT +60,7%/tahun, AERGOUSDT −102,6%, MYXUSDT −533,9%.

### Pengujian — `reports/tests.md`

**615 hijau** pada `884d6c8e`, kode keluar 0, 2,99 detik, tanpa jaringan. Jejaknya utuh dan tiap langkah diramalkan lebih dulu: 444 → 462 → 467 → 488 → 494 → 510 → 525 → 542 → 563 → 574 → 578 → **589** (+11 `test_runner_lantai.py`) → **601** (+12 `test_periode.py`) → **615** (+14 `test_run_h012.py`). **Sepuluh ramalan jumlah pengujian berturut-turut tepat.**

Angka jumlah tulis tangan hanya di tripwire: `test_gerbang_kesebelas.py` (jumlah gerbang), `test_run_h011.py::test_batas_h010_adalah_empat_puluh`, dan `test_run_h012.py` (`BATAS_VOID`, batas periode tahan, ambang kriteria).

### Kapasitas runner dan konektivitas

4 vCPU, 15 GB RAM, 88 GB disk. **Batas 6 jam per job yang menjadi kendala, bukan disk.** H-010 117,5 s untuk 40 simbol; H-011 838,1 s untuk 438 simbol dengan 300 ulangan. Aset 559 MB per run. python 3.12.13, numpy 2.5.1, pytest 9.1.1, **tanpa scipy**. CDN `data.binance.vision` 200; REST `fapi.binance.com` **451 permanen**.

### Batas alat agen dan solusinya

- Daftar alat GitHub **tidak memuat satu pun fungsi Actions**: tidak ada pembacaan run, job, langkah, atau log. Diverifikasi ulang di S14 lewat `listTools`.
- `search_code` **nol hasil di repo ini**. Baca berkas langsung. `get_file_contents` menuntut SHA 40 karakter penuh; `list_commits` dipakai untuk memperolehnya.
- `push_files` **mengganti seluruh isi berkas**, jadi baca dulu sebelum menulis ulang. Ia lebih aman daripada `create_or_update_file`.
- Setiap workflow diberi filter `paths` pada berkasnya sendiri. `tests.yml` memfilter `lux/**` dan `tests/**` — terbukti lagi di S14: setiap commit kode memicunya dan laporannya kembali dalam ~1 menit.
- **Setiap langkah yang bisa gagal wajib menulis hasilnya ke `reports/`** dengan `if: always()`; **gerbang yang bisa gagal ditaruh sebelum unduhan**; **jangan pernah menaruh pemeriksaan yang bisa gagal di akhir run panjang**.
- **Commit laporan tanpa berkas hasil berarti run GAGAL, bukan sedang berjalan.** Blob laporan yang tidak berubah berarti **belum ditulis**.
- **Modul baru berdiri hijau sendiri lebih dulu, penyambungan menyusul.** Dipakai lima kali; yang terbaru `periode.py` (601 sendiri, lalu tersambung tanpa menambah pengujian).
- **Baca modulnya sebelum menulis kode terhadapnya.** Di S14 pembacaan `run_h011.py` memberi bentuk persis `Hipotesis`/`Kriteria` dan pola "kriteria utama dari laporan", dan pembacaan `run_h002.py` membuktikan kunci YAML baru tidak menjatuhkan pembacaan lama.
- **Tulisan yang hanya menyentuh dokumen** (`STATE.md`, `PROMPT_KELANJUTAN.md`, `journal/`, `decisions/`) tidak memicu workflow apa pun dan aman dikerjakan selagi backtest berjalan.
- **Analisis atas laporan yang sudah dikomit dapat dikerjakan di sandbox tanpa jaringan.**

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1** (`5f222e8`): `header=0` + `skiprows=1` menghilangkan satu bar per berkas. **Parser 2 dan 3** (`16638b4`): BOM UTF-8. **URL non-ASCII**: percent-encoding lewat `bv.seg()`.
- **Metrik celah funding**: gagal lima putaran karena mengira kisi funding tetap.
- **Circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`). Alasan mengapa `konsentrasi.py`, `funding_ekor.py`, `sebaran.py`, dan `periode.py` berdiri sebagai modul sendiri.
- **S11:** langkah pra-terbang `backtest.yml` bisu; diperbaiki `245747ee`.
- **S12:** STATE v11 menaikkan kekeliruan analitis menjadi fakta ("funding bukan penyebab kerugian ekor"); ditarik v12. **S12:** STATE v13 menaikkan artefak aritmetika ("sepuluh simbol menghasilkan 101,2% laba"); ditarik v14. **S12:** dugaan "simbol muda lebih menguntungkan" lahir dari dua pencilan; difalsifikasi v15. **S12:** `test_gerbang_kesepuluh.py` memakai literal `== 10` di berkas yang justru melarangnya; diperbaiki `114b0d7e`.
- **S13:** ADR-012 v1 dan STATE v16 menulis "226 dari 356 jendela (63,5%)" padahal benar **194 (54,5%)**. Angka benar sudah ada di tiga tempat di repo dan tetap dikarang dari ingatan. **Kelas kesalahan yang sama tiga kali dalam dua sesi: jumlah yang tidak dijumlah ulang.**
- **S13:** `test_sebaran.py` menuntut kesamaan **bit** di bawah pembalikan urutan; modulnya benar, pengujiannya salah. Diperbaiki `2650ae32`. Aturan 22.
- **S13:** saringan pola nama menandai `BUSDT` dan `TUSDT` sebagai stablecoin padahal keduanya token "B" dan "T". **Degenerasi wajib dibuktikan lewat `stop_frac`, bukan ejaan nama.** Angka "+0,060168R" turunannya dibuang.
- **S14:** pra-registrasi ADR-014 menetapkan kriteria yang laporannya tidak mampu menghasilkan. Ditemukan saat menyiapkan `run_h012`, ditutup dua commit sebelum satu angka hasil dilihat. Aturan 29.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| **Sinyal masih punya keunggulan sesudah lantai `stop_frac` dan pagar biaya** | **H-012 sedang berjalan. Ramalan saya: ekspektasi periode tahan 0,010–0,045, yakni GAGAL** |
| Lantai 0,004 benar-benar menutup jalan masuk degenerasi | `invarian_risiko` H-012 wajib LULUS; bila masih gagal, seluruh ADR-014 keliru |
| Keunggulan H-010 bukan seluruhnya milik geometri keluar | skor entri acak turun 56,8%; butuh uji yang memisahkan sinyal dari geometri keluar, dan uji itu belum dirancang |
| Keunggulan kelanjutan membesar pada horizon 4h | jalankan hipotesis 4h setelah `validate.yml` untuk 4h |
| Funding sebagai **sinyal** memuat informasi arah | uji hipotesis berbasis funding, belum pernah dilakukan |
| Integritas 4h sama bersihnya dengan 1h | jalankan `validate.yml` untuk interval 4h |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap universe layak v2 438 |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |

**Diselesaikan sebelumnya:** saringan rezim tren memperbaiki breakout (**salah**, H-004) · retest memperkecil biaya per R secara menguntungkan (**salah**, H-005) · SMC yang dapat dikodekan punya keunggulan (**salah**, H-006) · imbalan lebih besar menaikkan ekspektasi (**benar**, +28%) · lama pegang membesarkan kerugian ekor (**benar**) · pengaman carry dipatok membuat `invarian_risiko` lulus (**benar**) · "biaya menjaga risiko memakan ekspektasi" (**salah**) · keunggulan bertahan bila penyumbang terbesar dibuang (**benar**, retensi 87,0%) · "ekspektasi bergantung umur simbol" (**salah**, Spearman −0,0336, p 0,8351) · "kerugian ekor dari bar menganga" dan "dari stop rapat" (**salah**) · "funding bukan penyebab kerugian ekor" (**ditarik**, 46,7%) · "laba terkonsentrasi pada sepuluh simbol" (**ditarik**) · "gerbang funding memantau biaya funding" (**salah**) · "optimum imbalan di luar grid H-007" (**benar sebagian**) · "dinding `lookback` perlu digeser" (**hangus**) · "target lebih jauh membesarkan porsi funding ekor" (**salah**) · "H-010 akan menjadi penolakan kesepuluh" (**salah**).

**"Hasil 40 simbol pertama mewakili 438 simbol" — TIDAK TERJAWAB, bukan terjawab.** H-011 menjawab dengan angka tercemar, jadi pertanyaannya masih terbuka sementara alat untuk menjawabnya sudah habis. Aturan 27. Ini kerugian, bukan kemajuan.

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 (14.076.257 baris 1h, 3.506.060 baris 4h, 17.169 celah, rasio 4,014) · metrik celah funding putaran 1–4 · seluruh run pilot H-001 termasuk `30170073890` · porsi "101,2%" sebagai bukti konsentrasi · selisih muda-lawan-tua +0,017–0,033R sebagai efek umur · nilai gerbang `funding` (10.253,97 / 10.199,59) sebagai bukti funding aman · "226 jendela / 63,5%" (benar 194 / 54,5%) · ekspektasi H-010 0,053028R sebagai bukti sistem layak dagang · **+0,060163R** dan **+0,059546R** (tertahan/semesta tanpa USDCUSDT) sebagai keunggulan atau kelulusan — penyubsetan pasca-hasil yang dilarang ADR-013 §8, boleh muncul hanya berlabel diagnostik beserta larangannya · **+0,060168R** (saringan nama yang salah, dibuang seluruhnya) · **281 dari 398 simbol positif** dan **median per simbol +0,06343** (rerata setara-bobot, bukan kriteria pra-registrasi) · **−0,091519R** sah **hanya bersama sebabnya**, yaitu satuan R yang degenerat.

---

## 5. Penghalang aktif

Tidak ada yang menghentikan pekerjaan. H-012 sedang berjalan dan hasilnya akan dikomit balik ke `reports/` oleh runner.

Dibutuhkan dari pengguna, belum memblokir: **token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`.

---

## 6. Tindakan berikutnya

1. **Ambil laporan H-012 ketika sudah dikomit:** `reports/backtest_h012_periode_tertahan.{md,json}` dan `reports/backtest_log.md`. Blob yang tidak berubah berarti **belum ditulis**, bukan gagal. Laporan yang dikomit tanpa berkas hasil berarti run **GAGAL**.

2. **Adjudikasi tujuh ramalan satu per satu, tanpa menggeser apa pun.** Urutan pembacaan yang benar: pertama `lantai_semesta.n_ditolak` terhadap `BATAS_VOID` 20; bila terlampaui, H-012 **BATAL** dan yang wajib ditulis adalah ADR baru tentang definisi semesta. Lalu `agregat_periode` → ekspektasi sejak `2026-01` sebagai **kriteria utama**, termasuk syarat 100 perdagangan; periode tahan dengan kurang dari 100 perdagangan berarti **TIDAK DAPAT DINILAI**, bukan lulus dan bukan gagal karena sinyal. Baru sesudahnya gerbang, sebaran, dan konteks.

3. **Rapikan utang S14:** satu baris `hasattr`/`__import__` di `tests/test_run_h012.py::test_kriteria_tidak_bergerak`.

4. **Uji yang memisahkan sinyal dari geometri keluar.** Skor entri acak turun 56,8% di H-010, jadi kemungkinan seluruh keunggulan ada di sisi keluar. Rancangannya belum ada dan wajib punya ADR sendiri. **Ini pertanyaan paling penting yang tersisa** apa pun hasil H-012.

5. **Horizon 4h.** Prasyarat mutlak `validate.yml` untuk 4h. Satu-satunya kerangka waktu yang masih benar-benar bersih.

6. **Funding sebagai sinyal.** Belum pernah diuji kandungan informasi arahnya.

**Yang DILARANG:** menyatakan sistem siap dagang · mengutip +0,060163R sebagai kelulusan · membuang USDCUSDT atau simbol lain sebagai penyelamatan pasca-hasil · **menyebut H-012 sebagai "H-010 setelah perbaikan"** · menggeser lantai 0,004, pagar 0,5R, `BATAS_VOID` 20, atau batas periode `2026-01-01` sesudah hasil terlihat · memilih subset simbol atau subset periode sesudah melihat tabel `agregat_periode` · mematok `imbalan_R` ke 8,0 · menurunkan `--ulangan` dari 300 · menaikkan `maks_umur_bar` dari 168 · membuang simbol merugi · memakai `konsentrasi` atau `funding_ekor` sebagai penyaring simbol · saringan berbasis umur simbol · membuang AIOTUSDT · melombakan ambang pengaman · menghitung ulang hipotesis yang sudah divonis · melonggarkan `invarian_risiko` dari −1,5R · melonggarkan ambang ADR-011 · **menurunkan maupun menaikkan ambang ekspektasi 0,05R**.

Sisanya, tidak memblokir:

7. Perketat `lux/funding.py::gerbang_lulus`, masih terlalu longgar dan berdiri di jalur ingest. Utang ADR-011.
8. Diff terhadap Dataset G lama (528 simbol). Satu-satunya butir daftar tugas awal pengguna yang masih terbuka.
9. `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md`; salin ADR-001 dan ADR-002 ke `decisions/`.
10. Pelapor Notion (`NOTION_TOKEN`); instruksi Gatekeeper masih menyebut sembilan gerbang.
11. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, dengan ≥24 shard.
12. Naikkan `versi` di `config/lux.yaml` sesudah seluruh pembacanya diperiksa.

---

## 7. Pengawasan otonom

Agen **LUX Gatekeeper** aktif di Notion. Terpicu saat runner membuat baris di database Run Results, menilai hasil terhadap gerbang mutu. Sudah diuji dengan baris sintetis bercacat dan menolak dengan benar. **Verdict Ditolak menghentikan pipeline.** Instruksinya masih menyebut sembilan gerbang dan perlu disesuaikan menjadi sebelas bila pelapor Notion diaktifkan.

---

## 8. Peta repo

| Path | Isi |
|---|---|
| `config/lux.yaml` | seluruh parameter yang memengaruhi hasil; **kini memuat lantai `min_median_stop_frac` 0,004 dan pagar `maks_biaya_masuk_R` 0,5; `versi` masih 2 dengan alasan tertulis** |
| `lux/binance_vision.py` | klien arsip: listing S3, unduhan, checksum, percent-encoding |
| `lux/universe.py` | universe point-in-time dan klasifikasi jenis kontrak |
| `lux/ingest.py` · `lux/backfill_daily.py` | ingest Tier B dan penutup celah ekor |
| `lux/validate.py` · `lux/validate_run.py` | integritas OHLCV, kelayakan universe, penolak aset `_retry` |
| `lux/funding.py` · `lux/funding_check.py` | ingest funding rate dan metrik kisinya; `gerbang_lulus` masih terlalu longgar |
| `lux/funding_model.py` | jadwal funding nyata, penagihan, carry terproyeksi dan terealisasi |
| `lux/costs.py` | model biaya dalam satuan R; aproksimasi interval tetap, **BUKAN jalur kritis**, tertulis eksplisit sejak `c80cf6d3` |
| **`lux/degenerasi.py`** | **satuan R yang runtuh: ambang 0,004 dan 0,5R, kasus USDCUSDT, `saring_semesta`** |
| `lux/diag_datar.py` · `lux/potong_ekor.py` | diagnosis dan pemangkasan ekor datar (ADR-003) |
| `lux/praregistrasi.py` | hipotesis sekali tulis dan penilaian terhadap kriteria |
| `lux/analisis/titik_impas.py` | aritmetika titik impas atas laporan yang sudah dikomit |
| `lux/analisis/sebaran.py` | std, galat baku, kuartil, jarak ambang. Bukan gerbang. **Galat bakunya taksiran bawah** |
| **`lux/analisis/periode.py`** | **agregat per bulan masuk; batas periode tahan; kepemilikan menurut waktu masuk** |
| `lux/strategi/breakout_atr.py` | sinyal kelanjutan (H-001b, H-002, H-007–H-012) |
| `lux/strategi/reversi_zskor.py` · `rezim_adx.py` · `retest.py` · `smc.py` | H-003 · H-004 · H-005 · H-006 |
| `lux/backtest/engine.py` | mesin eksekusi: stop, target, batas umur, saringan carry, pengaman carry terealisasi, **pagar `maks_biaya_masuk_R` bawaan MATI** |
| `lux/backtest/gerbang.py` | sembilan gerbang pertama + `NAMA_GERBANG` sebelas nama; `semua_lulus` memakai `len(NAMA_GERBANG)` |
| `lux/backtest/konsentrasi.py` · `funding_ekor.py` | gerbang kesepuluh dan kesebelas |
| `lux/backtest/walk_forward.py` | pemilihan parameter dalam sampel; konfig per kandidat (ADR-007); merambatkan `entri_ditolak_biaya` dari jendela **uji** saja |
| `lux/backtest/run_wf.py` | orkestrator H-001b — **jangan disunting**; sumber `rincian_R`, `diagnosa_biaya`, `ringkas_gabungan` |
| `lux/backtest/run_h002.py` · `run_h003.py` | orkestrator beku; hanya sembilan gerbang; `muat_konfig_h002` tidak membaca kunci ADR-014 |
| `lux/backtest/runner.py` | **runner bersama**: muat sekali, **lantai semesta**, jalankan, nilai sebelas gerbang, tulis jackknife, ekor funding, sebaran, **penolakan biaya, dan agregat periode** |
| `lux/backtest/run_keluarga.py` | keluarga ADR-006 (H-004, H-005, H-006) |
| `lux/backtest/run_h007.py` | **sumber grid bersama, HARAM disunting** |
| `lux/backtest/run_h008.py` · `run_h009.py` | dibekukan; `run_h009` sumber `buat_konfig` dan `AMBANG_CARRY_KERAS` |
| `lux/backtest/run_h010.py` | H-010; sumber grid imbalan {2,4,6,8} dan `kandidat()` |
| `lux/backtest/run_h011.py` | H-011, semesta penuh; `BATAS_H010 = 40` |
| **`lux/backtest/run_h012.py`** | **H-012: `BATAS_VOID = 20`, `PERIODE_TAHAN_TANGGAL = "2026-01-01"`, tujuh ramalan, tripwire angka kembar config↔degenerasi** |
| `tests/` | **615** pengujian tanpa jaringan, wajib hijau sebelum unduhan |
| `reports/` | keluaran mesin tiap run. `umur_simbol.md` pengecualian: dihitung di sandbox, provenansnya tertulis di dalamnya |
| `hipotesis/` | pendaftaran sekali tulis: `H-001b` … `H-011`, **`H-012` ditulis runner saat run** |
| `decisions/` | ADR-003 … **ADR-014** |
| `journal/` | riwayat per sesi, sampai **`2026-07-26-10.md`** |

**Workflow aktif (10):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`. **`backtest.yml` sekarang menjalankan `lux.backtest.run_h012`** dengan `limit` 0 dan `ulangan` 300, dan langkah `impor`-nya memuat delapan kelompok pagar ADR-014 yang berhenti dalam hitungan detik: mekanisme identik H-010/H-009, ambang pra-registrasi, angka kembar config↔`degenerasi`, aritmetika 0,002/0,004 = 0,5, bawaan MATI, sambungan lantai + `agregat_periode` benar-benar ada di `runner`, perilaku batas periode pada data buatan, dan larangan angka haram.

**Dihapus di S7:** `analyze_tail.yml` (`07860a7`), `diagnose.yml` (`f4af734`), `diag_datar.yml` (`41ca693`), `retry_failed.yml` (`3a206c6`).

Release **`tier-b-v1`** memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`. Pola unduh backtest wajib `ohlcv_1h_*.parquet`.
