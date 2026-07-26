# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-26 16:15 WIB (versi 18)

**Tahap sekarang:** S13 — **H-011 DITOLAK, dan penolakannya tidak informatif.** Ekspektasi 398 simbol tertahan **−0,091519R**, tetapi angka itu dihasilkan oleh **satu simbol yang satuan R-nya runtuh** (USDCUSDT, `stop_frac` 3,2e−06, ekspektasi −29,06R per perdagangan, total −18.861,06R). Yang terbongkar bukan sifat sinyal, melainkan **cacat pada definisi semesta** yang berumur sejak ADR-003.

**Tahap berikutnya:** **H-012** — lantai `stop_frac` pada kelayakan semesta plus pagar biaya 0,5R di mesin, diadjudikasi pada **periode waktu** yang dibekukan karena himpunan simbol tertahan sudah habis. Didaftarkan penuh di ADR-014 §8.

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
13. (S12) **Peristiwa yang terlalu jarang tidak dapat dipilih oleh pemilih dalam sampel.** Pengaman carry menyala 16 dari 14.925 (0,107%); kelangkaan, bukan biaya, yang membuatnya ditolak 334 lawan 22.
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
25. (S13, ADR-014) **Himpunan tertahan habis pada saat pertama kali dilihat.** Ia hanya bisa dibelanjakan sekali, jadi belanjakan pada pertanyaan yang mekanismenya sudah bersih.
26. (S13, ADR-014) **Cacat yang membalik tanda hasil tidak boleh diperbaiki di dalam hipotesis yang sama.** Perbaikannya melahirkan hipotesis baru.
27. (S13, ADR-014) **Eksperimen yang tercemar tidak informatif ke arah mana pun.** Ia memakan satu hipotesis tanpa membayar pengetahuan; catat sebagai kerugian, bukan kemajuan.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa. Seluruh komputasi berjalan di GitHub Actions.

---

## 3. Fakta terverifikasi

### H-011 — DITOLAK, dan yang terbongkar adalah cacat semesta (ADR-014)

Run **`30194733599`**, kode **`102c297c`**, laporan **`2bb7b963`**, sidik **`8a6efde6d333d8b5`**, **838,1 detik**, 438 simbol, 12 kombinasi. Berkas `reports/backtest_h011_semesta_penuh.{md,json}`.

Kriteria utama dihitung tangan dari `per_simbol`, bukan dari blok `putusan`:

| Kelompok | n simbol | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|
| Teruji (40 pertama alfabet) | 40 | 11.734 | +622,2348 | **+0,053028** |
| **Tertahan (398)** | 398 | 124.603 | **−11.403,5584** | **−0,091519** |
| Seluruh semesta | 438 | 136.337 | −10.781,3236 | −0,079078 |

Baris teruji **identik bit-per-bit** dengan H-010 (622,2348185492804; 0,05302836360569971). Mekanisme benar-benar diimpor tanpa perubahan; hanya semestanya berbeda.

**Sebaran (mesin ADR-013, pemakaian pertama):** std per perdagangan **4,24670** (ddof=1, n 136.337), galat baku **0,011501**, selang 95% **[−0,101621, −0,056536]**, jarak ke ambang **−0,129078R = −11,22 galat baku**. Kuartil R: min −470,0612 · Q1 −1,0635 · median **−1,0402** · Q3 −0,4224 · maks 12,9076. Pemakaian sah: untuk **menjatuhkan**, bukan menegakkan.

**Gerbang gagal:** `entri_acak` p **0,0631** (18/300) · `invarian_risiko` **−470,0612R** · `konsentrasi` tak dapat dinilai (ekspektasi gabungan negatif) · `funding_ekor` lewat `funding_maks_R` **2,3900** > 0,50. Lulus: forward_fill 0,0013 · buy_and_hold 0,8387 unggul 394/438 · lookahead 0,0 · funding 154.526,99 · overlap 0,0 · checksum 0,0 · survivorship 1,0 (0,1461 vs 0,1461, eksak karena semesta penuh).

Alasan keluar: stop 102.068 · target 21.649 · umur 9.699 · akhir_data 2.479 · carry 442. Jendela positif 2.246/4.092 = 0,54887.

**Penyebab tunggal:**

```
USDCUSDT: 29.527 bar, 11 jendela, 649 perdagangan,
          total_R -18.861,0596, ekspektasi_R -29,06173
```

Pasangan stablecoin terhadap stablecoin: ATR/harga hampir nol, `stop_frac` pada perdagangan terburuk **3,1984e−06**. Biaya dalam R berbanding balik dengan `stop_frac`, jadi `transaksi_R` mencapai **312,7333** pada satu perdagangan ber-`R` **−470,0612** yang `kotor_R`-nya hanya −157,3278. **Sepuluh perdagangan terburuk dari 438 simbol semuanya milik USDCUSDT**, dan `funding_maks_R` 2,3900 yang menjatuhkan gerbang kesebelas juga miliknya. Rerata biaya transaksi melonjak **0,03534R → 0,12552R (3,55 kali)**; 478 perdagangan berbiaya lebih dari 1R.

Ini **cacat pengukuran**, bukan temuan pasar: ketika ATR/harga menuju nol, R berhenti menjadi satuan risiko dan semua besaran dalam R menjadi tak terbatas. `invarian_risiko` menangkapnya dengan benar; yang gagal adalah definisi semesta.

**Adjudikasi tujuh ramalan ADR-013 §8 — dua benar, dua salah, satu tak terselesaikan:**

| # | Ramalan | Hasil | Putusan |
|---|---|---|---|
| 1 | ekspektasi tertahan 0,020–0,045 | −0,091519 | **SALAH** (arah benar, besaran jauh di luar) |
| 2 | ≥ 0,05 = bukti terkuat | tidak terjadi | cabang tak aktif |
| 3 | < 0,020 = hasil 40 simbol derau seleksi | terpicu | **TERPICU** |
| 4 | p entri acak 0,01–0,15; p>0,05 menolak | 0,0631 | **BENAR**, dan menolak |
| 5 | trade 100.000–160.000 | 136.337 | **BENAR** (taksiran 128.487, keliru +6,1%) |
| 6 | retensi_drop_1 ≥ 0,95 | tak dapat dinilai | **TAK TERSELESAIKAN** |
| 7 | durasi 15–60 menit | **13,97 menit** | **SALAH**, lebih cepat dari lantai |

Ramalan 6 cacat sejak ditulis: retensi hanya bermakna bila ekspektasi gabungan positif, jadi itu ramalan yang mustahil dinilai bila hipotesisnya gagal.

### SEMESTA LAYAK v2 — DINYATAKAN CACAT

Kriteria di `config/lux.yaml` versi 2: `min_bar_1h` 8760, `min_median_quote_volume_harian` 1.000.000, `maks_rasio_bar_datar` 0,30. **Tidak satu pun menyentuh volatilitas.** USDCUSDT lolos ketiganya dengan mudah; saringan volume bahkan menariknya masuk.

Cacat ini berumur sejak ADR-003 dan tak terlihat selama sepuluh hipotesis karena 40 simbol pertama secara alfabet tidak memuat satu pun pasangan stablecoin. H-002 sampai H-011 mewarisinya, tetapi hanya secara **laten**. Papan skor **tidak** dihitung ulang (aturan 5); ia diberi catatan ini.

### HIMPUNAN TERTAHAN — HABIS

Hasil per simbol untuk seluruh 438 simbol pada 1h sudah dilihat. **Tidak ada lagi simbol yang belum tersentuh di Tier B 1h.** Setiap pengujian 1h berikutnya bersifat dalam-sampel pada tingkat semesta. Dimensi yang masih bersih hanya **waktu** dan **kerangka waktu** (4h, belum tervalidasi). Aturan 25.

### H-010 — LULUS, dengan empat keberatan

Run **`30193898133`**, kode **`0a30ced4`**, laporan **`c035dcee`**, sidik **`14b2f3bfa8a7`**, **117,5 detik**, 40 simbol, 12 kombinasi. Mekanisme identik H-009 kecuali satu hal: grid imbalan {1,2,3,4} → **{2,4,6,8}**, kombinasi tetap 12, jangkar 2,0 dan 4,0 dipertahankan. Nol baris ditulis di `lux/strategi/`.

| Kriteria | Ambang | Nilai | Putusan |
|---|---|---|---|
| `min_ekspektasi_R` | ≥ 0,05 | **0,053028** | lulus |
| `min_trade_luar_sampel` | ≥ 100 | 11.734 | lulus |
| `maks_p_entri_acak` | ≤ 0,05 | **0,049505** | lulus, satu satuan resolusi |
| `min_jendela_positif_rasio` | ≥ 0,50 | **0,528090** | lulus |

Sebelas gerbang: forward_fill 0,000253 · buy_and_hold 0,798562 unggul 36/40 · **entri_acak p 0,049505, nyata 0,04661R** · lookahead 0,0 · invarian_risiko **−1,273250** · funding 11.523,31 · overlap 0,0 · checksum 0,0 · survivorship 0,855469 · konsentrasi **0,857845** · funding_ekor **0,167491**. Gerbang gagal: nol. Alasan keluar: stop 8.776 · target 1.839 · **umur 879** · akhir_data 214 · carry 26. Laju kena target **0,15672**, porsi tak selesai 0,09536.

**Empat keberatan:**

1. p 0,049505 = (4+1)/(100+1). Satu permutasi lagi memberi 0,059406 dan H-010 gagal. **Pada 300 permutasi di H-011, mekanisme yang sama memberi p 0,0631 — gagal.** Resolusi yang lebih tinggi membalik putusannya.
2. Skor nyata entri acak turun **0,10781R → 0,04661R (−56,8%)**. Entri acak memakai geometri keluar yang identik, jadi tafsiran paling tidak menyenangkan: sebagian besar perbaikan berasal dari **geometri keluar**, bukan kandungan informasi sinyal.
3. Jendela positif 0,528090 vs ambang 0,50, turun dari 0,556180.
4. Ia diukur pada 40 simbol dari semesta yang kini diketahui cacat. Angka 0,053028 tetap benar sebagai aritmetika atas 40 simbol itu, dan tetap bukan keunggulan tervalidasi.

**Dekomposisi eksak (identitas tertutup sampai tujuh desimal):**

| Per perdagangan | H-009 | H-010 | Perubahan |
|---|---|---|---|
| Kotor R | 0,0759727 | **0,0892483** | **+17,5%** |
| Biaya transaksi | 0,0342866 | 0,0353377 | +3,1% |
| Biaya funding | 0,0003276 | 0,0008823 | **+169%** |
| **Bersih R** | **0,0413585** | **0,0530283** | **+28,2%** |

Agregat: kotor total 1.133,89 → 1.047,24 (−7,6%) · biaya 516,62 → 425,01 (−17,7%) · **bersih 617,28 → 622,23 (+0,80%)** · perdagangan 14.925 → 11.734 (−21,4%). Aturan 20.

**Dinding grid:** imbalan 8,0 → **162 jendela (45,51%)** · 6,0 → 96 (26,97%) · 4,0 → 59 (16,57%) · 2,0 → 39 (10,96%); jumlah tepat 356. Porsi 45,51% **di bawah** 54,5% milik H-009, jadi penempelan bukan mekanis dan dinding H-007 memang dinding. Rerata imbalan 6,140, titik impas 0,1400 lawan laju nyata 0,15672.

**Pola pemilihan stabil pada semesta sebelas kali lebih besar:** di H-011 (4.092 jendela) imbalan 8,0 memimpin dengan 656+575+498 = **1.729 (42,25%)**, lalu 6,0 1.165, 4,0 748, 2,0 450.

**Dinding `lookback` larut:** H-009 memilih 100 sebanyak 133 jendela; H-010 memberi 20→124, 55→116, 100→116. Menggeser satu sumbu mengubah pilihan pada sumbu lain, jadi kedua sumbu tidak dapat ditafsirkan sendiri-sendiri.

**Ramalan ADR-012 — dua benar, tiga salah:** porsi jendela imbalan 8,0 30–55% → 45,51% BENAR · laju target 0,13–0,20 → 0,15672 BENAR · porsi tak selesai >12% → 9,54% SALAH · porsi funding ekor 0,20–0,35 → 0,16749 SALAH · ekspektasi 0,030–0,048 → 0,053028 SALAH. Ketiganya salah ke arah yang menguntungkan hipotesis. Aturan 21.

**Ramalan ADR-011 — tiga-tiganya BENAR:** porsi ekor 0,14–0,20 → 0,167491 · porsi di atas pengaman 0,00107–0,005 → 0,002216 (26/11.734) · `funding_maks_R` 0,25–0,50 → 0,414441.

**Konsentrasi H-010:** 26 untung / 14 rugi · drop-1 0,04549R (retensi 0,857845) · drop-2 0,03924R · median simbol +0,04604R · porsi bruto teratas 0,1346 (ADAUSDT) · setara 14,9 simbol · jackknife k=3 0,035104, k=4 0,028803, k=5 0,022450.

**Pencilan yang wajib diingat:** AIOTUSDT 32 perdagangan, ekspektasi **+1,79837R**. Dilarang dibuang, dilarang dijadikan bukti.

**Utang ADR-013 §7 — LUNAS.** `lux/analisis/sebaran.py` (`a911e99e`, 15 pengujian; koreksi pengujian saya sendiri `2650ae32`) disambungkan ke `runner.py` (`485694e1`). Laporan memuat `std_R`, `galat_baku_R`, kuartil, dan jarak ambang dalam galat baku, dengan peringatan tertulis bahwa galat baku itu **taksiran bawah** karena perdagangan tidak saling bebas. `ukur_sebaran` melempar `ValueError` pada R tak-hingga dan pemanggilnya menangkapnya menjadi `CACAT MESIN: …` di laporan, supaya pemeriksaan di akhir run panjang tidak menghancurkan run.

### GERBANG KESEBELAS `funding_ekor` — HIDUP (ADR-011)

`446a3732` ADR → `163a7bad` modul + 21 pengujian (**488 hijau**, laporan `1a8ee96f`) → `114b0d7e` penyambungan (**494 hijau**, laporan `ad691072`).

Masalah yang diselesaikan: gerbang `funding` lama menilai total mutlak dan memberi 10.253,97 (H-008) lawan 10.199,59 (H-009), selisih **−0,53%**, keduanya LULUS — padahal funding pada perdagangan terburuk berbeda **4,4 kali** (0,9228R = 46,7% lawan 0,2098R = 16,5%) dan `invarian_risiko` berbalik dari GAGAL ke LULUS. Titik buta yang menyamar sebagai gerbang. Aturan 17.

Empat sub-uji, semua harus lulus: `porsi_funding_ekor_maks` ≤ **0,35** · `funding_maks_R` ≤ **0,50** · `porsi_trade_di_atas_pengaman` ≤ **0,005** · `jadwal_dimuat` wajib. **Pengungkapan:** 0,35 duduk di antara dua nilai yang sudah terlihat (0,467 dan 0,165), jadi gerbang ini **mengikat mulai H-010**, tidak ke belakang.

Bukti bergigi, dikunci sebagai pengujian: sepuluh terburuk H-008 → 0,467 **GAGAL**; enam terburuk H-009 → 0,165 lulus; H-010 → 0,167491 lulus; **H-011 → GAGAL lewat `funding_maks_R` 2,3900**, dan yang menjatuhkannya adalah perdagangan USDCUSDT yang sama — jadi ia ikut menandai cacat semesta, bukan cacat funding.

### GERBANG KESEPULUH `konsentrasi` (ADR-010)

Modul `211fb3bd` (18 pengujian, 462 hijau), penyambungan `8cf70f08` (5 pengujian, 467 hijau, laporan `10732424`). `semua_lulus` memakai `len(NAMA_GERBANG)`, bukan literal.

Ambang, **mengikat mulai H-010**: `drop_1_positif` > 0 · `drop_5persen_positif` > 0 atas ⌈0,05·N⌉ · `retensi_drop_1` ≥ 0,60 · `median_simbol_positif` > 0 · `porsi_bruto_teratas` ≤ 0,25 dengan penyebut bruto. **Sub-uji yang tidak dapat dinilai berarti GAGAL** — terbukti bekerja di H-011: ekspektasi gabungan negatif membuat retensi tak bermakna, dan gerbang menolak menilai alih-alih memberi angka palsu.

Konsekuensi diterima sadar: tiga orkestrator beku (`run_wf`, `run_h002`, `run_h003`) hanya menyusun sembilan gerbang, jadi bila dijalankan lagi laporannya gagal pada `konsentrasi` dan `funding_ekor`. Angka lama di `reports/` tidak berubah.

### RAMALAN 3 ADR-010 — DIFALSIFIKASI: umur simbol tidak menerangkan apa pun

`reports/umur_simbol.md`, commit **`bce8cf89`**, dihitung di sandbox dari `per_simbol` H-009 — nol run baru. Spearman(umur, ekspektasi) **−0,0336**, p dua sisi 20.000 permutasi seed 42 = **0,8351**, Spearman(umur, jumlah trade) +0,9668. Per ember umur tidak monoton: 2–4 jendela +0,056342 · 5–9 **+0,068240** · 10–19 +0,026059 · 20–24 +0,035878. **Membuang simbol muda menurunkan ekspektasi** ke 0,038970. Asal kekeliruan: dua pencilan, AIOTUSDT dan 1000000BOBUSDT.

### H-009 — DITOLAK, tetapi sembilan gerbang lulus untuk pertama kalinya

Run **`30186730437`**, kode **`d5f18c6f`**, laporan **`77b7492c`**, sidik `eac6c83305bd1069`, 155,4 detik.

| | H-007 | H-008 | **H-009** |
|---|---|---|---|
| Ekspektasi R | +0,04044 | +0,04126 | **+0,041359** |
| Total R | +605,10 | +616,20 | **+617,28** |
| Perdagangan | 14.962 | 14.933 | **14.925** |
| Keluar `carry` | — | 2 | **16** |
| `invarian_risiko` | −1,9769 GAGAL | −1,9769 GAGAL | **−1,2698 LULUS** |

DITOLAK, alasan tunggal `ekspektasi 0.0414R < 0.05R`. `entri_acak` p **0,0099**, nyata 0,10781R. Keluar: stop 10.242, target 4.111, umur 368, akhir_data 188, carry 16.

**Pengaman memotong tepat sasaran.** Lima perdagangan terburuk H-008 yang carry-nya melewati 0,25R (AIOTUSDT funding 0,9228 · ALGOUSDT 0,3866 · 1000XECUSDT 0,3083 · AAVEUSDT 0,3285 · 1000XECUSDT 0,2728) **hilang seluruhnya** di H-009; lima berikutnya (ADAUSDT 0,2098 · 1000FLOKIUSDT 0,1985 · 1000WHYUSDT 0,1789 · 1000XECUSDT 0,1996 · 1000FLOKIUSDT 0,1714) **bertahan dengan R identik sampai belasan desimal** (ADAUSDT `-1.2697928364736204` di kedua run). **Nol korban sampingan.**

**Ramalan H-009 — dua dari tiga SALAH:** keluar carry melonjak ke ratusan → **16, SALAH** · kerugian terburuk di bawah 1,5R → −1,2698 **BENAR** · ekspektasi turun di bawah 0,04126R → naik ke 0,041359 **SALAH**. Selisih 0,00009R: ekspektasi H-009 **tidak berubah**, yang berubah hanya ekornya.

**Mengapa pemilih menolak pengaman yang ternyata gratis.** Klaim ADR-009 bahwa pengaman memakan ekspektasi **separuhnya terbantah**: di luar sampel ia tidak memakan ekspektasi sama sekali. Yang tetap fakta: pemilih mematikannya **334 dari 356 jendela** (0,0 → 334 · 0,25 → 22 · 0,50 → 0). Penjelasan yang benar adalah **kelangkaan**, bukan biaya. Aturan 13. Konsekuensi luas: **setiap pengaman yang menargetkan peristiwa langka akan selalu ditolak oleh pemilihan dalam sampel.**

### KONSENTRASI LABA — klaim versi 13 DITARIK

"Sepuluh dari 40 simbol menghasilkan 101,2% laba": angkanya benar, tafsirannya menyesatkan **secara konstruksi**, karena penyebutnya sudah dipotong kerugian. Yang benar (H-009): simbol laba **28** → **+883,62R**, simbol rugi **12** → **−266,35R**, bersih **+617,28R**; 28/40 menguntungkan · median +0,0325R · kuartil −0,0170 / +0,0325 / +0,1401 · rentang −0,21618 sampai +1,36566 · **HHI 0,0621, setara 16,1 simbol**. Jackknife: drop-1 ADAUSDT → +0,035962 (retensi **87,0%**) · drop-2 0,033000 · drop-3 0,028420 · drop-4 0,024540 · drop-5 0,019590 (47,4%) · drop-8 0,007028 · drop-10 ≤ 0.

**Dilarang tegas:** membuang 12 simbol merugi menaikkan ekspektasi ke sekitar **0,0752R** dan melewati ambang. Survivorship bias telanjang.

### Papan skor sebelas hipotesis

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
| **H-010** | grid imbalan {2,4,6,8}, 40 simbol | **0,053028** | tidak ada dari sebelas | **LULUS**, empat keberatan |
| **H-011** | mekanisme H-010 atas 438 simbol | **−0,079078** (tertahan **−0,091519**) | `entri_acak`, `invarian_risiko`, `konsentrasi`, `funding_ekor` | **DITOLAK, dan TERCEMAR** |

Sidik: H-001b `e458f4c82abf6735` · H-002 `16fb57692a6f0888` · H-003 `3a1cdc867f61bf67` · H-004 `98d6a5e15b2cc08b` · H-005 `9c4b6324e79569eb` · H-006 `e503a9a833182b25` · H-007 `7f5e7aeeaa29284b` · H-008 `dfeeea04fd4107f6` · H-009 `eac6c83305bd1069` · H-010 `14b2f3bfa8a754b5` · **H-011 `8a6efde6d333d8b5`**.

**Kesimpulan struktural:** enam percobaan pada sisi **masuk** menghasilkan nol perbaikan; empat percobaan pada sisi **keluar** menghasilkan +28% (H-007), penutupan gerbang risiko (H-009), dan +28% lagi (H-010). **Sisi keluar satu-satunya arah yang pernah memberi leverage.** Sisi masuk tetap belum terbukti memuat informasi — dan skor entri acak H-010 yang turun 56,8% adalah bukti terkuat sejauh ini bahwa keunggulannya mungkin **seluruhnya** ada di sisi keluar.

### PENYEBAB KEGAGALAN `invarian_risiko` — TERUKUR

Perdagangan terburuk H-008 AIOTUSDT: R −1,9769 = kotor −1,0182 − transaksi 0,0359 − **funding 0,9228**. Funding **46,7%** kerugian terburuk. Dua kandidat penjelasan saya sendiri terbantah oleh data yang sama: stop bekerja sempurna (kotor −1,0065 sampai −1,0260) dan stop rapat bukan penyebabnya (lebar terburuk 2,83% lawan rerata 3,61%). Di H-010 kerugian terburuk **−1,273250**. **Di H-011 penyebab kegagalannya berbeda sama sekali: bukan funding melainkan `stop_frac` degenerat.**

### Titik impas

`1/(1+imbalan)`: 1R 0,5000 · 2R 0,3333 · 3R 0,2500 · 4R 0,2000 · 6R 0,1429 · 8R 0,1111, dikunci `tests/test_titik_impas.py`. Di H-009, **194 dari 356 jendela (54,5%) memilih imbalan 4,0** (82 + 64 + 48), terverifikasi tiga kali. **Versi 16 menulis 226 dan 63,5%; itu salah dan sudah diperbaiki.**

| Hipotesis | Laju kena target | Kotor `3p−1` | Bersih tercatat | Seretan |
|---|---|---|---|---|
| H-002 | 0,36028 | +0,08084 | +0,03159 | 0,04926 |
| H-004 | 0,34151 | +0,02453 | −0,01818 | 0,04272 |
| H-005 | 0,33755 | +0,01265 | −0,03571 | 0,04836 |
| H-006 | 0,30122 | −0,09633 | −0,13449 | 0,03815 |
| H-003 | 0,26326 | −0,21021 | −0,24782 | 0,03761 |
| H-009 | 0,27544 | — | +0,041359 | 0,034614 |
| **H-010** | **0,15672** | — | **+0,053028** | **0,036220** |
| **H-011** | **0,15879** | — | **−0,079078** | **0,125520 (tercemar)** |

### KELUARGA ADR-006 — DITOLAK BERTIGA

Run `30175665060`, kode `1aedb84`, laporan `c0636bf`. Ambang p diperketat ke **0,0167 (Bonferroni 0,05/3) sebelum satu angka pun terlihat**, dan itu bergigi: p H-005 0,0396 akan lolos ambang biasa 0,05. Trend breakout tidak diuji ulang karena itu persis H-001b dan H-002. Bagian SMC lain (order block, FVG, BOS/CHoCH) tidak diuji karena tidak punya definisi mekanis.

### H-003 — pembalikan skor-z, DITOLAK telak

Run `30175179866`. −0,24782R, 28.959 perdagangan, 25/356 jendela positif, `entri_acak` p 1,0000. Dengan H-006 gagal serupa: **pada 1h perp USDT, pembalikan jangka pendek rugi sistematis.**

### MESIN BACKTEST

`lux/backtest/`: `engine.py`, `gerbang.py`, `konsentrasi.py`, `funding_ekor.py`, `walk_forward.py`, `run_wf.py` (H-001b), `run_h002.py`, `run_h003.py`, `runner.py`, `run_keluarga.py`, `run_h007.py`, `run_h008.py`, `run_h009.py`, `run_h010.py`, **`run_h011.py`**. Analisis: `lux/analisis/{titik_impas,sebaran}.py`.

**Rantai impor yang tidak boleh diputus.** `run_h011` mengimpor `IMBALAN_H010`, `LOOKBACK_H010`, `buat_konfig_h010`, `kandidat_h010` dari `run_h010`, dan `AMBANG_CARRY_KERAS`, `DATASET`, `KUNCI_TERLARANG`, `buat_konfig_h009` dari `run_h009`. `run_h010` mengimpor `buat_konfig`, `DATASET`, `KUNCI_TERLARANG`, `AMBANG_CARRY_KERAS` dari `run_h009` dan `LOOKBACK` dari `run_h007`. `run_h009` memasang `assert` bahwa gridnya identik `run_h007`, jadi **`run_h007.IMBALAN` haram disunting**.

Gerbang: `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`, `konsentrasi`, `funding_ekor`. **Gerbang yang tidak dapat dinilai berarti GAGAL.**

Lima alasan keluar: `stop`, `target`, `umur`, `carry`, `akhir_data`. Urutan per bar: umur → carry → stop/target → entri → ekuitas. `ALASAN_TIDAK_SELESAI = ("umur", "akhir_data", "carry")`.

Pra-registrasi **sekali tulis**; nilai saringan ikut masuk sidik. `hipotesis/H-011.json` terdaftar dengan sidik `8a6efde6d333d8b5`.

**Pagar pra-terbang `run_h011` yang terbukti bekerja** (dan terbukti tidak cukup — aturan 23): `0 < limit <= 40` untuk mode terbatas, `ulangan >= 100`, dataset identik H-002, `maks_carry_R > 0`, `AMBANG_CARRY_KERAS > 0`, `LOOKBACK_H010 == [20,55,100]`, daftar kandidat identik, `buat_konfig_h010 is buat_konfig_h009`, dan larangan `KUNCI_TERLARANG` masuk grid.

### DATASET TIER B PUTARAN 2 — SAH, tetapi kelayakannya cacat

**14.545.679 bar 1h dan 3.636.733 bar 4h**, 790 simbol, 112 celah kisi, rasio 1h:4h **3,9996**, sekitar 703 MB. Validasi 1h: 0 pelanggaran fatal, **447 simbol layak**. ADR-003 memangkas 141 simbol berekor datar, 1.081.920 bar (7,4%), universe layak v2 = **438** — **kini dinyatakan cacat karena tanpa lantai volatilitas**. Funding: 1.982.017 baris, 447 simbol, 3 celah sejati, 79,1% positif, jitter maksimum 47 ms, 295 dari 447 simbol hidup di lebih dari satu rezim kisi. Carry ekstrem: 1000WHYUSDT +60,7%/tahun, AERGOUSDT −102,6%, MYXUSDT −533,9%.

### Pengujian — `reports/tests.md`

**542 pengujian hijau** pada commit `e22745aa` (laporan `21d1b850`), kode keluar 0, 2,40 detik, tanpa jaringan. Jejak aritmetisnya utuh dan tiap langkah diramalkan lebih dulu: 444 → **462** (+18 `test_konsentrasi.py`) → **467** (+5 `test_gerbang_kesepuluh.py`) → **488** (+21 `test_funding_ekor.py`) → **494** (+6 `test_gerbang_kesebelas.py`) → **510** (+16 `test_run_h010.py`) → **525** (+15 `test_sebaran.py`, setelah satu kegagalan yang pengujiannya sendiri yang salah) → **542** (+17 `test_run_h011.py`). Tujuh ramalan jumlah pengujian berturut-turut, semuanya tepat.

Angka jumlah yang ditulis tangan hanya ada di dua tripwire: `tests/test_gerbang_kesebelas.py` (jumlah gerbang) dan `tests/test_run_h011.py::test_batas_h010_adalah_empat_puluh` (`BATAS_H010`).

### Kapasitas runner dan konektivitas

4 vCPU, 15 GB RAM, 88 GB disk. **Batas 6 jam per job yang menjadi kendala, bukan disk.** H-010 117,5 detik untuk 40 simbol; **H-011 838,1 detik untuk 438 simbol dengan 300 ulangan permutasi** — penskalaan jauh lebih baik daripada linier karena permutasi tidak berskala dengan jumlah simbol. Aset 559 MB per run. Runner python 3.12.13, numpy 2.5.1, pytest 9.1.1, **tanpa scipy** (karena itu `sebaran.py` memakai pendekatan normal). CDN `data.binance.vision` 200; REST `fapi.binance.com` **451 permanen**.

### Batas alat agen dan solusinya

- Daftar alat GitHub yang tersedia **tidak memuat satu pun fungsi Actions** — tidak ada pembacaan run, job, langkah, atau log. Diverifikasi di S11.
- `search_code` **tidak berguna di repo ini**; indeksnya belum memuat repo muda. Baca berkas langsung.
- Agen tidak bisa membuat rilis, memicu workflow manual, atau mengunduh artifact.
- Setiap workflow diberi filter `paths` pada berkasnya sendiri. `tests.yml` memfilter `lux/**` dan `tests/**`.
- **Setiap langkah yang bisa gagal wajib menulis hasilnya ke `reports/`** dengan `if: always()`.
- **Gerbang yang bisa gagal ditaruh sebelum unduhan**, dan **jangan pernah menaruh pemeriksaan yang bisa gagal di akhir run panjang** — tangkap dan tulis ke laporan.
- Sandbox agen **tidak punya jaringan**. `pytest` wajib berjalan sebelum unduhan.
- **Commit laporan tanpa berkas hasil berarti run GAGAL, bukan sedang berjalan.**
- Blob laporan yang tidak berubah berarti **belum ditulis**. H-011 butuh **enam** pengambilan; H-010 butuh **sebelas**. **SHA blob basi begitu ada tulisan**; `push_files` lebih aman daripada `create_or_update_file`.
- **Modul baru berdiri hijau sendiri lebih dulu, penyambungan menyusul.** Dipakai empat kali: `konsentrasi.py` (462 lalu 467), `funding_ekor.py` (488 lalu 494), `run_h010.py` (510), `sebaran.py` (525 lalu 525 tersambung lalu 542).
- **Baca modulnya sebelum menulis kode terhadapnya.** Pembacaan `run_h009.py` menemukan `assert` grid beku; pembacaan `backtest.yml` menemukan angka 194 yang membuktikan "226" salah.
- **Tulisan yang hanya menyentuh dokumen** (`STATE.md`, `PROMPT_KELANJUTAN.md`, `journal/`, `decisions/`) tidak memicu workflow apa pun dan aman dikerjakan selagi backtest berjalan.
- **Analisis atas laporan yang sudah dikomit dapat dikerjakan di sandbox tanpa jaringan.** Kriteria utama H-011 dihitung begitu, dan begitulah cacat USDCUSDT ditemukan.

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1** (`5f222e8`): `header=0` + `skiprows=1` menghilangkan satu bar per berkas.
- **Parser 2 dan 3** (`16638b4`): BOM UTF-8; satu baris sampah menggagalkan seluruh berkas.
- **URL non-ASCII**: percent-encoding lewat `bv.seg()`.
- **Metrik celah funding**: gagal lima putaran karena mengira kisi funding tetap.
- **Circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`). Alasan terdokumentasi mengapa `konsentrasi.py`, `funding_ekor.py`, dan `sebaran.py` berdiri sebagai modul sendiri.
- **S10:** kurung kurawal liar di `tests/test_run_h007.py`; diperbaiki `e81e34e`.
- **S11:** langkah pra-terbang `backtest.yml` bisu; diperbaiki `245747ee`.
- **S12:** STATE v11 menaikkan kekeliruan analitis menjadi fakta ("funding bukan penyebab kerugian ekor"); ditarik di v12. Penyebabnya memakai rerata untuk menyimpulkan tentang ekor.
- **S12:** STATE v13 menaikkan artefak aritmetika ("sepuluh simbol menghasilkan 101,2% laba") menjadi fragilitas terbesar; ditarik di ADR-010 dan v14. Penyebabnya penyebut bersih.
- **S12:** dugaan "simbol muda lebih menguntungkan" lahir dari dua pencilan; difalsifikasi di v15.
- **S12:** `tests/test_gerbang_kesepuluh.py` memakai literal `== 10` di tiga tempat, di berkas yang menguji kode yang justru melarang literal semacam itu. Diperbaiki `114b0d7e`. Aturan 18.
- **S13:** ADR-012 v1 dan STATE v16 menulis **"226 dari 356 jendela (63,5%)"** padahal yang benar **194 (54,5%)**. Angka benar sudah ada di tiga tempat di repo dan tetap dikarang dari ingatan. Diperbaiki di ADR-012 dan v17. **Kelas kesalahan yang sama dengan "26 simbol positif" dan label "16 pengujian": jumlah yang tidak dijumlah ulang. Tiga kali dalam dua sesi.**
- **S13:** `tests/test_sebaran.py::test_urutan_masukan_tidak_mengubah_hasil` menuntut kesamaan **bit** hasil di bawah pembalikan urutan masukan. Modulnya benar, pengujiannya salah: penjumlahan pecahan tidak asosiatif (`rerata_R` 0,27999999999999997 lawan 0,28). Diperbaiki `2650ae32` dengan toleransi 1e−12. Aturan 22.
- **S13:** ADR-014 mencatat saringan pola nama saya sendiri yang menandai `BUSDT` dan `TUSDT` sebagai stablecoin padahal keduanya token "B" dan "T". Angka turunannya dibuang. **Degenerasi wajib dibuktikan lewat `stop_frac`, bukan lewat ejaan nama.**

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| **Sinyal masih punya keunggulan setelah lantai `stop_frac` diterapkan** | **H-012, ADR-014 §8. Ramalan saya: pada periode luar sampel waktu, ekspektasi 0,010–0,045 — yakni GAGAL** |
| Keunggulan H-010 bukan seluruhnya milik geometri keluar | skor entri acak turun 56,8%; butuh uji yang memisahkan sinyal dari geometri keluar, dan uji itu belum dirancang |
| Keunggulan bertahan pada periode waktu yang belum dilihat | satu-satunya dimensi luar sampel yang masih tersisa; wajib dibekukan sebelum dipakai |
| Keunggulan kelanjutan membesar pada horizon lebih panjang (4h) | jalankan hipotesis baru pada 4h setelah validasi 4h |
| Funding sebagai **sinyal** memuat informasi arah, bukan hanya biaya | uji hipotesis berbasis funding, belum pernah dilakukan |
| Integritas 4h sama bersihnya dengan 1h | jalankan `validate.yml` untuk interval 4h |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap universe layak v2 438 |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |

**Diselesaikan di S9:** saringan rezim tren memperbaiki breakout (**salah**, H-004); retest memperkecil biaya per R secara menguntungkan (**salah**, H-005); SMC yang dapat dikodekan punya keunggulan (**salah**, H-006).

**Diselesaikan di S10:** menurunkan titik impas lewat imbalan lebih besar menaikkan ekspektasi (**benar**, +28%); menaikkan lama pegang membesarkan kerugian ekor (**benar**).

**Diselesaikan di S12:** pengaman carry dipatok membuat `invarian_risiko` lulus (**benar**) · "biaya menjaga risiko memakan ekspektasi" (**salah**) · keunggulan bertahan bila penyumbang terbesar dibuang (**benar**, retensi 87,0%) · "ekspektasi bergantung umur simbol" (**salah**) · "kerugian ekor dari bar menganga" (**salah**) · "dari stop sangat rapat" (**salah**) · "funding bukan penyebab kerugian ekor" (**ditarik**, 46,7%) · "laba terkonsentrasi pada sepuluh simbol" (**ditarik**) · "gerbang funding memantau biaya funding" (**salah**).

**Diselesaikan di S13:**

- "Optimum imbalan berada di luar grid H-007" — **BENAR sebagian.** Batas atas 8,0 dipilih 45,51% jendela, jadi grid lama membatasi; tetapi porsinya di bawah 54,5% milik batas lama, jadi optimumnya kini **di dalam** grid.
- "Dinding `lookback` juga perlu digeser" — **hangus.** Menggeser dinding imbalan melarutkannya sendiri.
- "Target lebih jauh membesarkan porsi funding di ekor" — **SALAH.** 0,16749 lawan 0,165.
- "H-010 akan menjadi penolakan kesepuluh" — **SALAH.** Ia lulus.
- **"Hasil 40 simbol pertama mewakili 438 simbol" — TIDAK TERJAWAB, bukan terjawab.** H-011 menjawab dengan angka yang tercemar cacat semesta, jadi pertanyaannya masih terbuka sementara alat untuk menjawabnya (himpunan tertahan) sudah habis. Aturan 27. Ini kerugian, bukan kemajuan.

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 (14.076.257 baris 1h, 3.506.060 baris 4h, 17.169 celah, rasio 4,014); metrik celah funding putaran 1–4 (1.380.741 · 1.193.209 · 587.131 · 266.612); seluruh run pilot H-001 termasuk `30170073890`; **porsi "101,2%" sebagai bukti konsentrasi**; **selisih muda-lawan-tua +0,017 sampai +0,033R sebagai efek umur**; **nilai gerbang `funding` (10.253,97 / 10.199,59) sebagai bukti funding aman**; **"226 jendela / 63,5%" — yang benar 194 / 54,5%**; **ekspektasi H-010 0,053028R sebagai bukti sistem layak dagang**; dan yang baru dari ADR-014:

- **+0,060163R** (tertahan 397 tanpa USDCUSDT) dan **+0,059546R** (437 tanpa USDCUSDT) — dilarang dikutip sebagai keunggulan, kelulusan, atau bukti H-010 benar. Membuang simbol setelah melihat hasilnya adalah penyubsetan pasca-hasil yang dilarang ADR-013 §8. Boleh muncul hanya berlabel diagnostik beserta larangannya.
- **+0,060168R** — angka "tanpa stablecoin" yang saringan namanya salah. Dibuang seluruhnya.
- **281 dari 398 simbol positif** dan **median per simbol +0,06343** — rerata setara-bobot per simbol, bukan kriteria yang dipra-registrasi. Dilarang menggantikan kriteria berbobot perdagangan.
- **−0,091519R** — sah dikutip **hanya bersama sebabnya**, yaitu satuan R yang degenerat. Dikutip sendirian ia menyesatkan ke arah sebaliknya.

---

## 5. Penghalang aktif

Tidak ada yang menghentikan pekerjaan.

Dibutuhkan dari pengguna, belum memblokir: **token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`.

---

## 6. Tindakan berikutnya

1. **H-012 — lantai `stop_frac` dan pagar biaya.** Didaftarkan penuh di ADR-014 §8 dengan tujuh ramalan dibekukan. Dua perubahan saja, keduanya dipatok sebelum dijalankan: (a) kelayakan semesta membuang simbol yang **median `stop_frac` < 0,004** — turunan aritmetis, karena biaya bolak-balik 0,002 dari harga berarti tepat 0,5R pada `stop_frac` 0,004; (b) mesin menolak entri yang biayanya melampaui **0,5R**, sebagai pagar risiko sejenis `maks_carry_R`, bukan knob yang dicari, dan penolakannya wajib tercatat sebagai alasan tersendiri di laporan. Kriteria utama: **ekspektasi berbobot perdagangan pada periode waktu luar sampel yang dibekukan**, karena himpunan simbol tertahan sudah habis. Urutan wajib: modul + pengujian hijau lebih dulu, workflow dibalik sesudahnya.

2. **Uji yang memisahkan sinyal dari geometri keluar.** Skor entri acak turun 56,8% di H-010, jadi kemungkinan seluruh keunggulan ada di sisi keluar. Rancangannya belum ada dan wajib punya ADR sendiri. Ini pertanyaan paling penting yang tersisa selain H-012.

3. **Horizon 4h.** Prasyarat mutlak: jalankan `validate.yml` untuk 4h. Ini juga satu-satunya kerangka waktu yang masih benar-benar bersih.

4. **Funding sebagai sinyal.** Belum pernah diuji kandungan informasi arahnya.

**Yang DILARANG:** menyatakan sistem siap dagang; mengutip +0,060163R sebagai kelulusan; membuang USDCUSDT atau simbol lain sebagai penyelamatan pasca-hasil (perbaikan hanya lewat kriteria kelayakan yang dipra-registrasi dan berlaku seragam); menyebut H-012 sebagai "H-010 setelah perbaikan"; mematok `imbalan_R` ke 8,0; menurunkan `--ulangan`; menaikkan `maks_umur_bar` dari 168; membuang simbol merugi (naik ke ±0,0752R, survivorship bias telanjang); memakai gerbang `konsentrasi` atau `funding_ekor` sebagai penyaring simbol; saringan berbasis umur simbol; membuang AIOTUSDT; melombakan ambang pengaman; menghitung ulang hipotesis yang sudah divonis; melonggarkan `invarian_risiko` dari −1,5R; melonggarkan ambang ADR-011; menaikkan atau menurunkan lantai 0,004 dan pagar 0,5R setelah hasil H-012 terlihat; **menurunkan maupun menaikkan ambang ekspektasi 0,05R**.

Sisanya, tidak memblokir:

5. Perketat `lux/funding.py::gerbang_lulus`, masih terlalu longgar dan berdiri di jalur ingest. Utang ADR-011.
6. Diff terhadap Dataset G lama (528 simbol). **Satu-satunya butir dari daftar tugas awal pengguna yang benar-benar masih terbuka.**
7. `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md`; salin ADR-001 dan ADR-002 ke `decisions/`.
8. Pelapor Notion (`NOTION_TOKEN`); instruksi Gatekeeper masih menyebut sembilan gerbang.
9. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, dengan ≥24 shard.

**Lunas di S13:** utang `std_R` / `galat_baku_R` (ADR-013 §7) lewat `lux/analisis/sebaran.py`; docstring `lux/costs.py` (`c80cf6d3`) — dan cacatnya ternyata bukan "pembagi 8 jam" melainkan kebisuan modul itu soal fakta bahwa pembagi tetapnya **bukan jalur kritis**, padahal 295 dari 447 simbol berjadwal funding pernah berada di lebih dari satu rezim interval.

---

## 7. Pengawasan otonom

Agen **LUX Gatekeeper** aktif di Notion. Terpicu saat runner membuat baris di database Run Results, menilai hasil terhadap gerbang mutu. Sudah diuji dengan baris sintetis bercacat dan menolak dengan benar. **Verdict Ditolak menghentikan pipeline.** Instruksinya masih menyebut sembilan gerbang dan perlu disesuaikan menjadi sebelas bila pelapor Notion diaktifkan.

---

## 8. Peta repo

| Path | Isi |
|---|---|
| `config/lux.yaml` | seluruh parameter yang memengaruhi hasil; **kriteria kelayakan semesta di sini yang cacat karena tanpa lantai volatilitas** |
| `lux/binance_vision.py` | klien arsip: listing S3, unduhan, checksum, percent-encoding |
| `lux/universe.py` | universe point-in-time dan klasifikasi jenis kontrak |
| `lux/ingest.py` | ingest Tier B dengan validasi per simbol |
| `lux/backfill_daily.py` | penutup celah ekor dari arsip harian |
| `lux/validate.py` · `lux/validate_run.py` | integritas OHLCV, kelayakan universe, penolak aset `_retry` |
| `lux/funding.py` · `lux/funding_check.py` | ingest funding rate dan metrik kisinya; `gerbang_lulus` masih terlalu longgar |
| `lux/funding_model.py` | jadwal funding nyata, penagihan, carry terproyeksi dan terealisasi |
| `lux/costs.py` | model biaya dalam satuan R; **aproksimasi interval tetap, BUKAN jalur kritis, tertulis eksplisit sejak `c80cf6d3`** |
| `lux/diag_datar.py` · `lux/potong_ekor.py` | diagnosis dan pemangkasan ekor datar (ADR-003) |
| `lux/praregistrasi.py` | hipotesis sekali tulis dan penilaian terhadap kriteria |
| `lux/analisis/titik_impas.py` | aritmetika titik impas atas laporan yang sudah dikomit |
| `lux/analisis/sebaran.py` | **std, galat baku, kuartil, jarak ambang. Bukan gerbang. Galat bakunya taksiran bawah** |
| `lux/strategi/breakout_atr.py` | sinyal kelanjutan (H-001b, H-002, H-007–H-011) |
| `lux/strategi/reversi_zskor.py` | sinyal pembalikan (H-003) |
| `lux/strategi/rezim_adx.py` | ADX Wilder dan saringan rezim (H-004) |
| `lux/strategi/retest.py` | entri retest, "sniper entry" mekanis (H-005) |
| `lux/strategi/smc.py` | sapuan likuiditas, bagian SMC yang dapat dikodekan (H-006) |
| `lux/backtest/engine.py` | mesin eksekusi: stop, target, batas umur, saringan carry, pengaman carry terealisasi. **Belum punya pagar biaya per perdagangan — tugas H-012** |
| `lux/backtest/gerbang.py` | sembilan gerbang pertama + `NAMA_GERBANG` sebelas nama; `semua_lulus` memakai `len(NAMA_GERBANG)` |
| `lux/backtest/konsentrasi.py` | gerbang kesepuluh |
| `lux/backtest/funding_ekor.py` | gerbang kesebelas |
| `lux/backtest/walk_forward.py` | pemilihan parameter dalam sampel; konfig per kandidat opsional (ADR-007) |
| `lux/backtest/run_wf.py` | orkestrator H-001b — **jangan disunting**; sumber `rincian_R`, `diagnosa_biaya`, `ringkas_gabungan` |
| `lux/backtest/run_h002.py` · `run_h003.py` | orkestrator beku; hanya sembilan gerbang |
| `lux/backtest/runner.py` | **runner bersama**: muat sekali, jalankan, nilai sebelas gerbang, tulis jackknife, ekor funding, **dan sebaran** |
| `lux/backtest/run_keluarga.py` | keluarga ADR-006 (H-004, H-005, H-006) |
| `lux/backtest/run_h007.py` | **sumber grid bersama, HARAM disunting** |
| `lux/backtest/run_h008.py` · `run_h009.py` | dibekukan; `run_h009` sumber `buat_konfig` dan `AMBANG_CARRY_KERAS` |
| `lux/backtest/run_h010.py` | H-010, satu-satunya hipotesis yang lulus |
| `lux/backtest/run_h011.py` | **H-011, semesta penuh; `BATAS_H010 = 40` satu-satunya angka tulis tangan** |
| `tests/` | **542** pengujian tanpa jaringan, wajib hijau sebelum unduhan |
| `reports/` | keluaran mesin tiap run. `umur_simbol.md` pengecualian: dihitung di sandbox, provenansnya tertulis di dalamnya |
| `hipotesis/` | pendaftaran sekali tulis: `H-001b` … **`H-011`** |
| `decisions/` | ADR-003 … **ADR-014** |
| `journal/` | riwayat per sesi, sampai `2026-07-26-09.md` |

**Workflow aktif (10):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`. `backtest.yml` sekarang menjalankan **`lux.backtest.run_h011`** dengan `limit` 0 dan `ulangan` 300, dan memuat penjaga pra-terbang ADR-009 + ADR-012 + ADR-013 yang berhenti dalam hitungan detik.

**Dihapus di S7:** `analyze_tail.yml` (`07860a7`), `diagnose.yml` (`f4af734`), `diag_datar.yml` (`41ca693`), `retry_failed.yml` (`3a206c6`).

Release **`tier-b-v1`** memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`. Pola unduh backtest wajib `ohlcv_1h_*.parquet`.
