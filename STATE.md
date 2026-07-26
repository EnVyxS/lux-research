# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-27 00:40 WIB (versi 22)

**Tahap sekarang:** S17 — **kerangka 4h siap dipakai, dan jalan menuju ke sana ternyata memuat lima cacat yang semuanya sejenis.** ADR-017, ADR-018, dan ADR-019 selesai seluruhnya. Semesta 4h berdiri sendiri: **447 simbol valid** (run `30211176709`) dan **438 layak** sesudah ekor datar dipangkas (run `30211673239`), keduanya **identik simbol per simbol dengan 1h** — dan kesamaan itu **diperiksa**, bukan disyukuri (aturan 23). Pengujian **714 hijau**.

**Tahap berikutnya:** **modul H-013** (ADR-015 Bagian B / ADR-016 langkah 4), berdiri hijau sendiri lebih dulu. Lalu `backtest.yml` dibalik ke 4h **paling akhir**. Larangan ADR-019 sudah tidak mengikat lagi: langkah 1–4 selesai.

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
19. (S13) **Margin setipis satu satuan resolusi bukan margin.** `entri_acak` H-010 lulus p 0,049505 pada 100 permutasi; pada 300 permutasi mekanisme yang sama memberi **0,0631** dan **gagal**. Dikonfirmasi ulang di H-012: **0,06312292358803986**.
20. (S13) **Ekspektasi yang naik karena penyebutnya menyusut bukan keunggulan yang membesar.**
21. (S13) **Kecurigaan wajib naik, bukan turun, ketika hasilnya menyenangkan.** Dipakai empat kali di S16–S17 atas run yang terasa terlalu cepat (validasi 4h 36s, potong-ekor 4h 27s, 702 uji 2,03s, 709 uji 2,80s); keempatnya **tak berdasar** sesudah log dan blob diperiksa.
22. (S13, ADR-014) **Menuntut kesamaan bit pada agregat pecahan adalah pengujian yang menyala pada perilaku yang benar.** Di dalam satu fungsi murni, kesamaan bit tetap sah.
23. (S13, ADR-014) **Pagar yang memastikan masukan identik tidak memastikan masukan sah.** Diperluas di S17: **kesamaan hasil lintas dua run berbeda dilarang diterima tanpa pemeriksaan.** Semesta 4h yang persis 447 lalu persis 438 seperti 1h wajib dibandingkan simbol per simbol lebih dulu — dan sesudah dibandingkan, ia memang identik.
24. (S13, ADR-014) **Satu simbol dapat mendominasi agregat 438 simbol.**
25. (S13, ADR-014) **Himpunan tertahan habis pada saat pertama kali dilihat.**
26. (S13, ADR-014) **Cacat yang membalik tanda hasil tidak boleh diperbaiki di dalam hipotesis yang sama.**
27. (S13, ADR-014) **Eksperimen yang tercemar tidak informatif ke arah mana pun.**
28. (S13, ADR-014) **Saringan yang menolak entri juga menolak saat pemilihan.** Terbukti kuantitatif di H-012: hanya **62** entri ditolak pengaman.
29. (S14) **Pra-registrasi wajib diperiksa terhadap apa yang benar-benar dapat dihitung dari laporan.**
30. (S14) **Kriteria utama dihitung dari berkas laporan yang dikomit, bukan dari nilai yang beredar di memori run.**
31. (S15) **Pagar yang menyalin baris dari kode yang dijaganya tidak menjaga apa pun.**
32. (S15) **Aritmetika yang hidup di dalam `main` tidak dapat diuji.** `biaya_bolak_balik_R`, `harga_stop_terisi`, dan `lux/kerangka.py` seluruhnya lahir dari aturan ini.
33. (S15) **Setiap langkah workflow wajib `tee` ke `logs/` dan seluruh `logs/` disalin ke `reports/` dengan `if: always()`.**
34. (S15) **Lingkungan pagar wajib memasang dependensi yang sama dengan `tests.yml`.**
35. (S16) **Muatan tulis yang panjang wajib dibaca ulang utuh sebelum dikirim, dan jumlah pengujian dicacah dari muatan yang benar-benar dikirim, bukan dari rencana.** Sejak aturan ini dipatuhi, tujuh ramalan berturut-turut tepat.
36. (S16, ADR-016) **Ramalan yang dijamin benar oleh konstruksi bukan ramalan.** Sebelum menghitung sebuah ramalan lulus, tunjukkan keadaan yang membuatnya gagal.
37. (S17, ADR-017–019) **Angka yang benar untuk satu interval tidak berubah nilai ketika dipakai di interval lain — ia berubah MAKNA, dan diam.** Lima cacat sejenis ditemukan berurutan, semuanya berbentuk konstanta bar yang mengaku sebagai satuan waktu. Setiap besaran yang berarti "satu hari", "satu minggu", atau "sekian jam" wajib diturunkan dari interval lewat `lux.kerangka`, tidak pernah dari literal.
38. (S17) **Dua definisi atas satu dataset selalu dimenangkan oleh yang tidak terlihat.** Pada cacat kelima, laporan mencetak semesta 438 yang benar sementara mesin memperdagangkan bar yang menurut semesta itu sudah tidak ada.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa. Seluruh komputasi berjalan di GitHub Actions.

---

## 3. Fakta terverifikasi

### TEMUAN S17 — lima cacat buta-interval, semuanya sejenis, semuanya ditutup

Seluruhnya ditemukan saat menyiapkan kerangka 4h, dan tidak satu pun berupa galat yang berbunyi.

| # | Cacat | Akibat bila 4h dijalankan apa adanya | Ditutup di |
|---|---|---|---|
| 1 | `validate_run` menulis `universe_layak.json` tanpa interval | keluaran 4h menimpa masukan 1h | `02933b85` |
| 2 | `muat_ambang` membaca `min_bar_1h` untuk interval apa pun | lantai riwayat 8.760 bar dipakai untuk 4h (= 4 tahun) | `fe7fd30e` |
| 3 | `MIN_PANJANG` / `MIN_BAR` buta interval di `potong_ekor` | ekor 1–3 hari lolos pada 4h | `6aacef40` |
| 4 | keluaran `potong_ekor` 4h menimpa masukan backtest 1h | dataset H-012 tertimpa tanpa pesan galat | `6aacef40` + pagar `5296162d` |
| 5 | **`muat_ohlcv` memangkas ekor dengan ambang 1h** | **dua definisi ekor atas satu dataset; yang menentukan hasil adalah yang salah** | `409343f3` |

Cacat kelima yang paling berbahaya, dan ia sengaja dicatat begitu. Empat cacat pertama menyusutkan atau menimpa **berkas**, sehingga meninggalkan jejak di disk. Yang kelima tidak meninggalkan jejak apa pun: workflow pemangkasan menyatakan 438 simbol layak atas dasar ekor ≥ 6 bar, sementara jalur muat backtest memangkas hanya ekor ≥ 24 bar, sehingga simbol yang sudah dinyatakan bersih dibaca **bersama ekor palsunya** — dan laporan tetap mencetak 438 dengan benar.

### ADR-019 — satuan hari, dilaksanakan lima commit, lima ramalan tepat

ADR ditulis **sebelum** sebaris kode, commit **`8c567c7b`**, sesudah membaca `gerbang.py`, `walk_forward.py`, `runner.py`, dan `run_wf.py` utuh.

| Langkah | Commit | Isi | Ramalan | Nyata |
|---|---|---|---|---|
| 1 | `47ef9a90` | `lux/kerangka.py` + 8 uji | 702 | **702** |
| 2 | `ba42a401` | `potong_ekor` memakai `kerangka` + tripwire | 703 | **703** |
| 3a | `e7697300` | `gerbang_forward_fill(interval=…)` + 6 uji | 709 | **709** |
| 3b | `1a3e1e5d` | `runner` memasok interval + 2 uji | 711 | **711** |
| 3c | `409343f3` | `muat_ohlcv` meneruskan interval + 3 uji | 714 | **714** |

Adjudikasi lengkap di `journal/2026-07-26-16.md`, commit `9a3f08dd`.

**`lux/kerangka.py` adalah modul daun dan itu syarat mutlak, bukan selera:** ia tidak mengimpor apa pun dari `lux`. Rantai `gerbang → potong_ekor → diag_datar → run_wf → gerbang` sudah pernah melahirkan impor sirkular pada commit `4b77617`, dan menaruh aritmetika "satu hari berapa bar" di `potong_ekor` akan melahirkannya kembali. Isinya: `JAM_SEHARI = 24`, `INTERVAL_JAM = {"1h": 1, "4h": 4}`, `interval_dikenal()`, `jam_interval()`, `bar_per_hari()` — keduanya terakhir **gagal keras** untuk interval tak dikenal atau yang tidak membagi rata.

**Ramalan 2 ADR-019 bertahan penuh: tak satu pun pengujian lama berubah hasilnya** (702 → 703 → 709 → 711 → 714, nol `failed`). Itu bukti terkuat yang tersedia bahwa jalur 1h **bit-identik**, sebab `bar_per_hari("1h") == 24` sama dengan kedua bawaan lama. Bobotnya melampaui kerapian angka: dua dari commit itu menulis ulang berkas panjang secara **utuh** (`runner.py`, `run_wf.py`) karena `push_files` hanya bisa mengganti seluruh isi berkas, jadi satu baris yang tercecer akan menjatuhkan puluhan uji lama. Tidak ada yang jatuh.

**Yang sengaja TIDAK diubah:** `gerbang_forward_fill(df)` di `run_wf.main` tetap tanpa interval. `run_wf` adalah orkestrator H-001b yang dibekukan dan hanya pernah dijalankan pada 1h, di mana bawaan 24 memang berarti satu hari.

### UTANG TEKNIS YANG WAJIB DIINGAT — config bar datar tidak pernah dibaca

`config/lux.yaml` memuat `universe.maks_rasio_bar_datar: 0.30`, tetapi **gerbang backtest tidak pernah membacanya**. Angka 0,30 hidup sebagai bawaan fungsi di `gerbang.py` dan sebagai literal di `runner.py` serta `run_wf.py`, keduanya hanya sebagai `ambang` yang **dilaporkan**. Konsekuensinya harus dinyatakan terang: **menyunting angka itu di config tidak mengubah perilaku apa pun, sementara laporan tetap mencetak 0,30 dan tampak konsisten.** ADR-019 bagian 3 butir 5 memutuskan hanya mencatatnya, sebab menyambungkannya akan mengubah perilaku sebelas hipotesis lama.

Keberatan ADR-018 yang juga masih berdiri: `MAKS_RASIO_DATAR = 0.10` dipakai untuk kedua interval, padahal rasio bar datar 4h mekanis lebih kecil — jadi gerbang itu **lebih longgar** di 4h. Menggesernya sesudah melihat hasil 4h akan melanggar aturan 13.

### KERANGKA 4h — semesta berdiri sendiri, dan kesamaannya diperiksa

**Validasi 4h**, run **`30211176709`**, ADR-017 (`494c9bbc`) langkah 1–3 (`fe7fd30e` 683 hijau, `429c8f4d` workflow): **3.636.733 baris / 790 simbol**; **layak 447**; tidak layak 343 (riwayat pendek 277, bar datar 74, likuiditas 77); celah 112; duplikat **0**. Keempat ramalan ADR-017 benar.

**Pemangkasan ekor 4h**, run **`30211673239`**, ADR-018 (`30a6d228`) langkah 1–4 (`6aacef40` 694 hijau, `5296162d` workflow): ambang **6 bar**, lantai 2.190, maks rasio 0,1; **790 dipindai** · **141 berekor datar** · **270.398 bar dipangkas** · 447 → **438 layak / 9 ditolak** · **nol** penolakan gerbang `maks_rasio`. Kelima ramalan ADR-018 bagian 6 **benar**; selisih ramalan bar 270.480 lawan nyata 270.398 adalah **−82 bar = 0,030%**, dan seluruhnya terhitung habis oleh pembulatan kisi (RENUSDT 3.591,5→3.591; BLZUSDT 3.471,75→3.471; TOMOUSDT 1.175,75→1.175; DFUSDT 1.011,75→1.011; 82 ÷ 141 = 0,58 bar per simbol).

**Aturan 23 dijalankan dua kali, bukan sekali:** semesta 4h persis **447** lalu persis **438** seperti 1h. Keduanya dibandingkan **simbol per simbol** — 438 simbol di blob `e7d0f5ca` (`universe_layak_v2_4h.json`) lawan 438 simbol 1h — dan hasilnya **identik**. Itu wajar: kriteria kelayakan menyaring simbol, dan simbol yang riwayatnya pendek pada 1h juga pendek pada 4h.

**Pagar legasi terbukti di disk, bukan diasumsikan:** blob `universe_layak_v2.json` **identik** pada ref sebelum dan sesudah run 4h (`a484670f` pada `7c68431a` dan pada `80a8f3a5`). Jadi run 4h secara konstruksi tidak dapat menimpa masukan backtest 1h.

**ASET 4h TERVERIFIKASI ADA** di rilis `tier-b-v1` (id `359778114`): 12 berkas, 157.628.619 B. **Koreksi atas v21:** daftar aset di sana lahir dari cacat pengamatan — `ls -la aset` disaring pola `ohlcv_1h_*` sehingga berkas 4h tampak tidak ada. Aset 4h sudah ada sejak 2026-07-25.

### KOREKSI ATAS STATE v21 — utang `git pull --rebase` jauh lebih kecil

v21 menyatakan `geometri.yml` **satu-satunya** workflow yang memakai `git pull --rebase --autostash origin main` sebelum `git push`. **Itu salah.** `validate.yml`, `potong_ekor.yml`, `backtest.yml`, dan `ingest_tier_b.yml` juga memilikinya. Yang belum diperiksa satu per satu: `funding.yml`, `funding_check.yml`, `universe.yml`, `doctor.yml`, `backfill_daily.yml`, `notion_asap.yml`, `tests.yml`.

### TEMUAN S16 — mesin buta terhadap celah harga pada jalur stop

1. Gerbang `invarian_risiko` H-012 gagal pada **−21,3131R** terhadap ambang −1,5R.
2. Diagnostik `lux/analisis/geometri_keluar.py`, run **`30209272338`**: perdagangan itu **STGUSDT**, keluar lewat **`carry`**, `transaksi_R` 0,0559, `funding_R` 0,4825, pelampauan di luar biaya **20,3131R**, `stop_frac` 2,197%, `jam` **1,0**.
3. Tidak satu pun keluar `stop` di bawah −1,5R; stop terburuk **−1,4966R**; median pelampauan jalur stop **0,410263R**.
4. `engine.py` (blob `621298a8`): di blok stop/target, `harga = stop if kena_stop else target`. **Harga bar tidak pernah dipakai.**

**Konsekuensi yang wajib ikut dikutip setiap kali angka R lama disebut:** gerbang `invarian_risiko` **praktis tidak berdaya pada jalur stop**; seluruh **dua belas** hipotesis dinilai oleh mesin yang **optimistis terhadap risiko celah**; arah biasnya **melawan penolakan**, jadi **tidak ada vonis yang perlu dibalik**, tetapi **tidak satu pun angka R lama boleh disebut konservatif**. Jalur `carry` **bukan** yang cacat.

**Klaim yang DITARIK:** "mekanisme stop sendiri sehat". Penarikannya resmi di `decisions/ADR-016.md` bagian 2.

Perbaikannya terpasang dan hijau: `Konfig.stop_hormati_celah` bawaan **MATI** + `harga_stop_terisi` (`955b419a`, 673 uji), dinyalakan di config (`fb710521`). Target sengaja **tidak** simetris. **Hasil H-001b sampai H-012 TIDAK dihitung ulang** — itu akan mencampur dua mesin dalam satu papan skor.

### Papan ramalan jumlah pengujian

| Commit | Ramalan | Nyata | Putusan |
|---|---|---|---|
| `864da2ec` | 635 | **638** | SALAH |
| `3880408f` | 642 | 642 | TEPAT |
| `b4b1963c` | 643 | 643 | TEPAT |
| `eae7eb3a` | 662 | **665** | SALAH |
| `955b419a` | 673 | 673 | TEPAT |
| `fb710521` | 673 tetap | — | **TIDAK DAPAT DIADILI** (`tests.yml` memfilter `lux/**`+`tests/**`) |
| `02933b85` | 679 | 679 | TEPAT |
| `fe7fd30e` | 683 | 683 | TEPAT |
| `6aacef40` | **693** | **694** | **SALAH** |
| `47ef9a90` | 702 | 702 | TEPAT |
| `ba42a401` | 703 | 703 | TEPAT |
| `e7697300` | 709 | 709 | TEPAT |
| `1a3e1e5d` | 711 | 711 | TEPAT |
| `409343f3` | 714 | 714 | TEPAT |

Ramalan 693 salah **di dalam commit yang mengutip aturan 35**: berkas yang dikirim memuat **sebelas** fungsi uji, bukan sepuluh. Sebabnya bukan uji hantu melainkan salah mencacah muatan sendiri. Sesudah itu tujuh ramalan berturut-turut tepat.

Jejak: 444 → … → 638 → 642 → 643 → 665 → 673 → 679 → 683 → 694 → 702 → 703 → 709 → 711 → **714**.

### H-012 — DITOLAK (ADR-014 §8)

Run **`30200123505`**, commit **`56a325d2`**, sidik **`75f9c7ccd65ec30f`**, **1220,6 detik**, 437 dari 438 simbol dinilai, 4.081 jendela.

| Sisi batas | Bulan | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|
| **Tahan (sejak `2026-01`)** | 7 | **22.117** | +922,56 | **+0,041713** |
| Sebelum `2026-01` | 66 | 113.564 | +7.168,96 | +0,063127 |
| Seluruh riwayat | 73 | 135.681 | +8.091,52 | +0,059636 |

Selisih tahan − sebelum **−0,021414R**. 22.117 perdagangan jauh di atas syarat 100, jadi ini kegagalan karena **sinyal**, bukan kekurangan data. **0,041713R < 0,05R → GAGAL.** Lantai semesta membuang **1** simbol: USDCUSDT (median `stop_frac` **1,293930e−04**, biaya masuk **15,46R**, di bawah `BATAS_VOID` 20).

**Sebelas gerbang:** forward_fill 0,0013 lulus · buy_and_hold 0,8401 lulus (394/437) · **entri_acak GAGAL p 0,06312292358803986** (18/300) · lookahead lulus · **invarian_risiko GAGAL −21,3131R** · funding lulus · overlap lulus · checksum lulus · survivorship 0,1465 lulus · konsentrasi 0,9849 lulus · **funding_ekor GAGAL `funding_maks_R` 0,6601**.

Skor entri acak nyata **0,04661R** — **persis angka H-010**.

**Sebaran:** std 2,22746R, galat baku 0,006047R, CI95 **[0,047784, 0,071489]R** yang **memuat** 0,05. Biaya: transaksi **0,0359R**, funding −0,0010R, jarak stop 3,507%, **nol** perdagangan berbiaya di atas 1R dari 135.681. Alasan keluar: stop 101.417 · target 21.658 · umur 9.699 · akhir_data 2.479 · carry 428. Jendela positif 2.246/4.081 = 0,55036. Entri ditolak pengaman **62**.

**Adjudikasi tujuh ramalan — lima tepat, dua salah:** **5 SALAH** (62 lawan ramalan 500–5.000) dan **6 SALAH** (`invarian_risiko` GAGAL, bukan lulus). Ramalan 6 adalah pintu masuk seluruh temuan S16. Lantai 0,004 **bekerja besar-besaran** (−470,0612R → −21,3131R, turun 95,5%; biaya 0,12552R → 0,0359R; perdagangan di atas 1R 478 → **0**) tetapi **tidak** meloloskan gerbangnya — sebabnya bukan satuan R melainkan mesin yang buta celah.

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
| H-008 | pengaman carry dilombakan | 0,04126 | `invarian_risiko` −1,9769 | DITOLAK |
| H-009 | pengaman carry dipatok 0,25 | 0,041359 | tidak ada | DITOLAK oleh ambang 0,05R |
| H-010 | grid imbalan {2,4,6,8}, 40 simbol | 0,053028 | tidak ada dari sebelas | LULUS, empat keberatan; **p 0,0631 pada 300 permutasi** |
| H-011 | mekanisme H-010 atas 438 simbol | −0,079078 | empat gerbang | **DITOLAK, dan TERCEMAR** |
| **H-012** | semesta berlantai 0,004 + pagar 0,5R, dinilai sejak 2026-01-01 | **0,041713 (periode tahan)** | `entri_acak` · `invarian_risiko` · `funding_ekor` | **DITOLAK** |

Sidik: H-001b `e458f4c82abf6735` · H-002 `16fb57692a6f0888` · H-003 `3a1cdc867f61bf67` · H-004 `98d6a5e15b2cc08b` · H-005 `9c4b6324e79569eb` · H-006 `e503a9a833182b25` · H-007 `7f5e7aeeaa29284b` · H-008 `dfeeea04fd4107f6` · H-009 `eac6c83305bd1069` · H-010 `14b2f3bfa8a754b5` · H-011 `8a6efde6d333d8b5` · H-012 `75f9c7ccd65ec30f`.

**Sebelas dari dua belas ditolak.** Yang satu itu lulus pada 100 permutasi dan gagal pada 300.

**Kesimpulan struktural:** enam percobaan pada sisi **masuk** menghasilkan nol perbaikan; empat pada sisi **keluar** menghasilkan seluruh kemajuan. Skor entri acak **identik** 0,04661R di H-010 dan H-012 adalah bukti terkuat bahwa keunggulan yang terukur mungkin **seluruhnya** milik geometri keluar — dan temuan S16 menambahkan bahwa sebagian geometri keluar itu **artefak mesin**.

### H-011 — DITOLAK dan TERCEMAR

Run `30194733599`, 838,1 detik. Teruji 40 simbol +0,053028R identik bit-per-bit dengan H-010; tertahan 398 simbol **−0,091519R**. **Penyebab tunggal USDCUSDT**: 649 perdagangan, total −18.861,0596R, `stop_frac` terburuk **3,1984e−06**, `transaksi_R` **312,7333** pada satu perdagangan ber-`R` **−470,0612**. Cacat pengukuran, bukan temuan pasar. Tidak direhabilitasi (aturan 27).

### SEMESTA, HIMPUNAN TERTAHAN, TITIK IMPAS

**Himpunan tertahan HABIS**: hasil per simbol 438 simbol sudah dilihat (H-011) dan tabel 73 bulan sudah dilihat (H-012). Dimensi yang masih bersih hanya **kerangka 4h** — dan kini ia siap — serta **pemisahan sinyal dari geometri keluar**.

Titik impas `1/(1+imbalan)`: 1R 0,5000 · 2R 0,3333 · 4R 0,2000 · 6R 0,1429 · 8R 0,1111. Di H-009, **194 dari 356 jendela (54,5%)** memilih imbalan 4,0 — versi 16 menulis 226 dan 63,5%; **itu salah**. Seretan: H-002 0,04926 · H-009 0,034614 · H-010 0,036220 · H-011 0,125520 (tercemar) · H-012 **0,035900**.

### MESIN BACKTEST

**`engine.Konfig` — nama medan terverifikasi dari sumber:** `fee` (0,0005), `slippage` (0,0005), `atr_periode` (14), `atr_pengali_stop` (2,0), `risiko_per_trade` (0,005), `imbalan_R` (2,0), `modal_awal` (10.000), `izinkan_short` (True), `maks_umur_bar` (0), `maks_carry_R` (0,0), `jendela_carry_hari` (30), `maks_carry_realisasi_R` (0,0), `maks_biaya_masuk_R` (0,0), **`stop_hormati_celah` (False)**. **Tidak ada medan bernama `fee_efektif`** — itu kunci YAML. Lima medan terakhir bawaan **MATI** dan dikunci pengujian serta pagar `dataclasses.fields`.

**Urutan pemeriksaan per bar:** umur → carry realisasi → stop/target → entri (pengaman biaya lalu carry proyeksi) → ekuitas. `umur` dan `carry` mengisi pada `o[t]`, `akhir_data` pada `c[-1]` — ketiganya jujur terhadap celah.

Gerbang (11): `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`, `konsentrasi`, `funding_ekor`. **Tidak dapat dinilai = GAGAL.** `gerbang_forward_fill` kini menerima `interval`, dan bila dipasok ia **menang** atas `maks_deret_datar` eksplisit.

### DATASET TIER B PUTARAN 2

**14.545.679 bar 1h dan 3.636.733 bar 4h**, 790 simbol, rasio 3,9996, ~703 MB. 1h: 447 valid → v2 **438** → berlantai **437**. 4h: 447 valid → v2 **438** (identik 1h, terperiksa). Funding 1.982.017 baris, 3 celah sejati, 79,1% positif.

### Kapasitas runner dan konektivitas

4 vCPU, 15 GB RAM. **Batas 6 jam per job yang mengikat, bukan disk.** H-012 memakai 1220,6 s dari 21.600 s. python 3.12.13, numpy 2.5.1, pytest 9.1.1, pandas 2.2.3, pyarrow 17.0.0, **tanpa scipy**, **tanpa requests**. CDN `data.binance.vision` 200; REST `fapi.binance.com` **451 permanen**. Timeout: backtest 330, validate 120, potong_ekor 60, ingest 330.

### Batas alat agen dan solusinya

- Daftar alat GitHub **tidak memuat satu pun fungsi Actions**. Diverifikasi ulang di S16.
- `search_code` **nol hasil di repo ini**. `get_file_contents` menuntut SHA 40 karakter penuh, tetapi **menerima `ref: "main"`**.
- `push_files` **mengganti seluruh isi berkas**, jadi baca dulu sebelum menulis ulang, dan baca ulang muatannya sebelum mengirim (aturan 35).
- Filter `paths` per berkas: menyentuh `.github/workflows/backtest.yml` **langsung memulai run**, jadi ia dibalik paling akhir. `tests.yml` memfilter `lux/**` dan `tests/**`, jadi perubahan `config/`, `journal/`, `decisions/`, dan `STATE.md` **tidak** memicunya.
- **Kabar buruk datang dalam 23–32 detik; kabar baik 20 menit.** Diamnya laporan bukan tanda lolos.
- **Commit laporan tanpa berkas hasil berarti run GAGAL. Blob laporan yang tidak berubah berarti belum ditulis** — dipakai dengan benar tiga kali pada langkah 3a–3c, ketika blob lama masih menyebut commit sebelumnya.
- **Modul baru berdiri hijau sendiri lebih dulu. Baca modulnya sebelum menulis kode terhadapnya.**

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1–3**, **metrik celah funding**, **circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`).
- **S12:** STATE v11 dan v13 menaikkan kekeliruan menjadi fakta; ditarik v12 dan v14.
- **S13:** "226 dari 356 jendela (63,5%)" padahal **194 (54,5%)**. Saringan nama menandai `BUSDT`/`TUSDT` — **degenerasi wajib dibuktikan lewat `stop_frac`, bukan ejaan**.
- **S15:** empat run gagal berturut (`30198306280` bukti hilang · `30198631730` pytest tak terpasang · `30198840830` dan `30198942815` `fee_efektif` ditebak). Aturan 31–34.
- **S16:** dua commit cacat (`953ce24a` loop `pass` sehingga tabel tak pernah ditulis, `2a0f8545` `}` liar yang menjatuhkan **seluruh** koleksi pytest); dua ramalan cacah salah; klaim "mekanisme stop sehat" ditarik. Aturan 35–36.
- **S17:** lima cacat buta-interval; ramalan 693 salah; klaim v21 tentang `git pull --rebase` salah; daftar aset v21 lahir dari `ls` yang tersaring. Aturan 37–38.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| **STGUSDT benar-benar bergerak melawan sekitar 46,8% dalam rentang kira-kira satu bar 1h** | bar itu ada di rilis artefak, bukan di repo, dan sandbox tanpa jaringan. Kedua kemungkinan menuntut perbaikan yang sama |
| Menyalakan `stop_hormati_celah` akan menjatuhkan `invarian_risiko` lewat **`stop`** sedikitnya sekali | ramalan 4 ADR-016; diadili pada H-013 |
| Ekspektasi R H-013 dengan medan menyala **lebih rendah** daripada dengan medan mati | ramalan 5 ADR-016. Bila ia **membaik**, yang ditemukan cacat tanda, bukan keunggulan |
| Keunggulan H-010 bukan seluruhnya milik geometri keluar | **makin lemah**: skor entri acak nyata **0,04661R identik** di H-010 dan H-012 |
| Keunggulan kelanjutan membesar pada horizon 4h | ADR-015 Bagian B; prasyaratnya kini **lunas** |
| Gerbang bar datar 4h lebih longgar daripada 1h karena rasio mekanis lebih kecil | baca `reports/validate_1h.json` dan bandingkan sebaran rasio 1h lawan 4h |
| Funding sebagai **sinyal** memuat informasi arah | belum pernah diuji |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap universe layak v2 438 |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |

**Difalsifikasi sebelumnya:** saringan rezim tren memperbaiki breakout · retest memperkecil biaya per R · SMC yang dapat dikodekan punya keunggulan · "biaya menjaga risiko memakan ekspektasi" · "ekspektasi bergantung umur simbol" · "kerugian ekor dari bar menganga pada stop" · sinyal `breakout_atr` punya keunggulan yang bertahan di waktu pada 1h (H-012) · lantai 0,004 menutup **seluruh** jalan masuk degenerasi (sebagian) · "hasil 40 simbol mewakili 438 simbol" · dugaan bahwa `gabung_gerbang` membuang syarat deret datar (ADR-019 §1).

**Terbukti benar:** imbalan lebih besar menaikkan ekspektasi (+28%) · lama pegang membesarkan kerugian ekor · keunggulan bertahan bila penyumbang terbesar dibuang (retensi 0,9849) · **"H-012 gagal", diramalkan sebelum run** · **jalur 1h bit-identik sesudah ADR-019**.

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 · metrik celah funding putaran 1–4 · seluruh run pilot H-001 termasuk `30170073890` · porsi "101,2%" · nilai gerbang `funding` sebagai bukti funding aman · "226 jendela / 63,5%" · ekspektasi H-010 0,053028R sebagai bukti layak dagang · **+0,060163R** · **+0,059546R** · **+0,060168R** · **281 dari 398 simbol positif** dan median **+0,06343** · **−0,091519R** tanpa sebabnya · **+0,059636R** sebagai kelulusan · **+2.347,27R bulan 2026-01** atau bulan mana pun · **gerbang bar datar 4h dan gerbang `maks_rasio` 4h sebagai bukti kebersihan data** (ambangnya lebih longgar di 4h).

---

## 5. Penghalang aktif

Tidak ada. Tidak ada run yang berjalan. Tidak ada yang dibutuhkan dari pengguna.

---

## 6. Tindakan berikutnya

Urutan mengikuti ADR-019 bagian 6 dan ADR-016 bagian 7. **Tidak boleh dibalik.**

1. ~~`stop_hormati_celah` + config~~ — **selesai** (`955b419a`, `fb710521`).
2. ~~`validate.yml` 4h (ADR-017)~~ — **selesai**, run `30211176709`, 447 layak.
3. ~~`potong_ekor` berinterval (ADR-018)~~ — **selesai**, run `30211673239`, 438 layak.
4. ~~Satuan hari untuk gerbang dan pemuatan (ADR-019 langkah 1–4)~~ — **selesai**, 714 hijau.
5. **Modul H-013** (ADR-015 Bagian B): empat sel SS/SH/AS/AH, `h=48` bar 4h, ambang **SS − AS ≥ 0,020R**, p ≤ 0,05, ≥300 ulangan, ≥100 trade per sel. Mekanisme diimpor **tanpa perubahan** dari `run_h010`/`run_h009`; `stop_hormati_celah` menyala; masukan `universe_layak_v2_4h.json` + `akhir_sejati_4h.json`. Modul berdiri hijau sendiri lebih dulu, dan ramalan jumlah uji ditulis di pesan commit.
6. **`backtest.yml` dibalik PALING AKHIR** — menyentuhnya langsung memulai run. Kini masih `ohlcv_1h_*` + `funding_shard*` dengan `--interval 1h`, `--universe reports/universe_layak_v2.json`, `--akhir-sejati reports/akhir_sejati.json`, timeout 330.
7. **Segarkan `PROMPT_KELANJUTAN.md`** — tertinggal delapan aturan (31–38). Wajib **dibaca utuh** lebih dulu; menulis ulang dari ingatan adalah kelas kesalahan "226 jendela".
8. Periksa `git pull --rebase --autostash` pada tujuh workflow yang belum diperiksa, dan tinjau apakah ada yang sudah tak diperlukan.
9. Baca `reports/validate_1h.json` untuk mengukur asimetri gerbang bar datar 1h lawan 4h.
10. Pemetaan `dari_laporan` pelapor Notion terhadap kunci JSON `runner.py`.
11. Utang teknis: **sambungkan `maks_rasio_bar_datar` config ke gerbang** · `hasattr`/`__import__` di `test_run_h012.py` · pengujian `biaya_bolak_balik_R` · `pytest` ke `requirements-dev.txt` · docstring `median_stop_frac_bingkai` · nama ganda legasi `potong_ekor` sampai `backtest.yml` berinterval · tripwire tekstual `inspect.getsource` di `test_runner_interval.py` (lemah, dicatat sebagai lemah).
12. **Funding sebagai sinyal.** Belum pernah diuji kandungan informasi arahnya.
13. Perketat `lux/funding.py::gerbang_lulus` · diff Dataset G lama · `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md` · salin ADR-001/ADR-002 ke `decisions/` · naikkan `versi` config sesudah seluruh pembacanya diperiksa · Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, ≥24 shard.

**Yang DILARANG:** menyatakan sistem siap dagang · mengutip +0,060163R atau +0,059636R sebagai kelulusan · membuang simbol atau memilih bulan sesudah melihat hasil · **menyebut H-012 sebagai "H-010 setelah perbaikan"** · menyebut angka R lama **konservatif** · **menghitung ulang H-001b sampai H-012 dengan mesin ADR-016** · menggeser lantai 0,004, pagar 0,5R, `BATAS_VOID` 20, batas `2026-01-01`, ambang SS − AS 0,020R, `MAKS_RASIO_DATAR` 0,10, atau ambang rasio 0,30 · mematok `imbalan_R` ke 8,0 · menurunkan `--ulangan` dari 300 · menaikkan `maks_umur_bar` dari 168 sebagai penyelamatan · membuang simbol merugi · memakai `konsentrasi` atau `funding_ekor` sebagai penyaring simbol · melombakan ambang pengaman · melonggarkan `invarian_risiko` dari −1,5R · **menurunkan maupun menaikkan ambang ekspektasi 0,05R** · menjadikan `stop_hormati_celah` parameter yang dilombakan · **menjalankan H-013 sebelum modulnya hijau sendiri**.

---

## 7. Pengawasan otonom — DIHENTIKAN

Agen **LUX Gatekeeper** dan **LUX Gatekeeper Reporter** **tidak dipakai lagi.** Keputusan pengguna, 2026-07-26: kreditnya kemungkinan habis sebelum riset selesai.

Keputusan itu sehat melampaui penghematan. Bukti dari sisi Notion atas baris asap `3a9d5df0-96f9-81df-90a7-f6075d071680`: agen itu mengadili **setiap** baris otomatis dalam sekitar dua menit, termasuk baris yang menyatakan `bukan_hasil_riset=true`, dan memakai `Ditolak` untuk "bukti tidak cukup" padahal `Ditolak` semestinya berarti hipotesis gagal. **Vonis yang salah arti lebih buruk daripada tidak ada vonis.**

Kolom `Verdict` di database `LUX — Run Results` karena itu menjadi kolom **manusia**. Pelapor Notion tetap dipertahankan sebagai papan hasil yang dapat dibaca dari ponsel. Pekerjaan "selaraskan instruksi Gatekeeper dari sembilan ke sebelas gerbang" **dibatalkan**.

---

## 8. Peta repo

| Path | Isi |
|---|---|
| `config/lux.yaml` | seluruh parameter yang memengaruhi hasil; `min_bar_1h` 8.760, `min_bar_4h` 2.190, lantai `min_median_stop_frac` 0,004, pagar `maks_biaya_masuk_R` 0,5, `stop_hormati_celah` true; **`maks_rasio_bar_datar` 0,30 TIDAK DIBACA gerbang**; `versi` masih 2 |
| `lux/kerangka.py` | **modul daun**: `JAM_SEHARI`, `INTERVAL_JAM`, `bar_per_hari`, `jam_interval`, `interval_dikenal`. Tidak mengimpor apa pun dari `lux`; satu-satunya pemilik aritmetika "satu hari berapa bar" |
| `lux/binance_vision.py` | klien arsip: listing S3, unduhan, checksum |
| `lux/universe.py` | universe point-in-time dan klasifikasi kontrak |
| `lux/ingest.py` · `lux/backfill_daily.py` | ingest Tier B dan penutup celah ekor |
| `lux/validate.py` · `lux/validate_run.py` | integritas OHLCV; `muat_ambang(path, interval)` gagal keras; `nama_keluaran_universe` berinterval |
| `lux/funding.py` · `lux/funding_check.py` | ingest funding dan metrik kisinya; `gerbang_lulus` masih longgar |
| `lux/funding_model.py` | jadwal funding nyata, penagihan, carry |
| `lux/costs.py` | model biaya dalam satuan R; **BUKAN jalur kritis** |
| `lux/degenerasi.py` | satuan R yang runtuh: ambang 0,004 dan 0,5R, `saring_semesta` |
| `lux/notion_reporter.py` | pelapor baris hasil lewat `urllib.request`; kredensial terverifikasi run `30207584722` |
| `lux/diag_datar.py` · `lux/potong_ekor.py` | diagnosis dan pemangkasan ekor datar; keluaran **berinterval**; memakai `lux.kerangka` |
| `lux/praregistrasi.py` | hipotesis sekali tulis; **tidak membaca config** |
| `lux/analisis/{titik_impas,sebaran,periode,geometri_keluar}.py` | aritmetika atas laporan yang sudah dikomit; galat baku **taksiran bawah** |
| `lux/strategi/breakout_atr.py` | sinyal kelanjutan (H-001b, H-002, H-007–H-012) |
| `lux/strategi/{reversi_zskor,rezim_adx,retest,smc}.py` | H-003 · H-004 · H-005 · H-006 |
| `lux/backtest/engine.py` | mesin eksekusi; **lima saringan bawaan MATI**; `harga_stop_terisi` |
| `lux/backtest/gerbang.py` | sembilan gerbang pertama; `gerbang_forward_fill(df, maks_rasio_datar, maks_deret_datar, interval)` |
| `lux/backtest/konsentrasi.py` · `funding_ekor.py` | gerbang kesepuluh dan kesebelas |
| `lux/backtest/walk_forward.py` | pemilihan parameter dalam sampel; tidak memanggil gerbang apa pun |
| `lux/backtest/run_wf.py` | orkestrator H-001b — **jangan disunting kecuali dengan ADR**; sumber `rincian_R`, `diagnosa_biaya`, `muat_ohlcv` (kini meneruskan interval ke pemangkas) |
| `lux/backtest/run_h002.py` · `run_h003.py` | orkestrator beku; `muat_konfig_h002` memetakan YAML `fee_efektif` → medan `fee` |
| `lux/backtest/runner.py` | runner bersama: muat sekali, lantai semesta, sebelas gerbang, jackknife, ekor funding, sebaran, penolakan biaya, agregat periode; memasok `interval` ke gerbang bar datar |
| `lux/backtest/run_h007.py` | **sumber grid bersama, HARAM disunting** |
| `lux/backtest/run_h010.py` · `run_h011.py` · `run_h012.py` | sumber grid imbalan {2,4,6,8} · `BATAS_H010 = 40` · `BATAS_VOID = 20` dan `PERIODE_TAHAN_TANGGAL` |
| `tests/` | **714** pengujian tanpa jaringan, wajib hijau sebelum unduhan |
| `reports/` | keluaran mesin tiap run; berkas 4h bernama berinterval |
| `hipotesis/` | pendaftaran sekali tulis: `H-001b` … `H-012` |
| `decisions/` | ADR-003 … **ADR-019** |
| `journal/` | riwayat per sesi, sampai **`2026-07-26-16.md`** |

**Workflow aktif (12):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`, `notion_asap`, `geometri`. Semuanya idle di belakang filter `paths` dan tidak memakan kuota. `validate.yml` dan `potong_ekor.yml` kini berparameter `interval` (bawaan `4h`), dan `potong_ekor.yml` memuat pagar **`Berkas legasi 1h tak tersentuh`**. **Koreksi v21:** yang memakai `git pull --rebase --autostash origin main` **bukan hanya `geometri.yml`** — `validate.yml`, `potong_ekor.yml`, `backtest.yml`, dan `ingest_tier_b.yml` juga.

**Dihapus di S7:** `analyze_tail.yml` (`07860a7`), `diagnose.yml` (`f4af734`), `diag_datar.yml` (`41ca693`), `retry_failed.yml` (`3a206c6`).

Release **`tier-b-v1`** (id `359778114`) memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`. **Aset 4h ada: 12 berkas, 157.628.619 B.** Pola unduh backtest masih `ohlcv_1h_*.parquet` sampai butir 6 dikerjakan.
