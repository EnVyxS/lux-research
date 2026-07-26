# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-27 01:40 WIB (versi 23)

**Tahap sekarang:** S18 — **H-013 sudah berjalan penuh, dan putusannya DITAHAN.** Run `30214203863` menyelesaikan keempat sel dan melaporkan sumbangan sinyal **+0,054842R** terhadap ambang 0,020R, lalu mencetak **LULUS**. Putusan itu **tidak sah** (ADR-024): `kontribusi()` hanya memeriksa separuh kriteria utama ADR-015 — besaran selisih — sementara **p permutasi ≤ 0,05 pada ≥ 300 ulangan atas selisih SS − AS tidak pernah dihitung**, dan sel SS **gagal dua gerbang** (`invarian_risiko`, `checksum`) padahal ADR-015 menuntut kesebelasnya lulus di sana. Ambang tidak digeser satu pun. **Status H-013: BELUM DAPAT DINILAI.**

**Tahap berikutnya:** ADR-024 **Jalur A** — uji berpasangan per jendela atas SS − AS, dihitung dari empat berkas laporan yang **sudah dikomit**, tanpa run baru. Jalur A dapat menjatuhkan Jalur B, jadi ia lebih dulu.

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
21. (S13) **Kecurigaan wajib naik, bukan turun, ketika hasilnya menyenangkan.** Dipakai empat kali di S16–S17 atas run yang terasa terlalu cepat (validasi 4h 36s, potong-ekor 4h 27s, 702 uji 2,03s, 709 uji 2,80s); keempatnya **tak berdasar** sesudah log dan blob diperiksa. Dipakai kelima kali di S18 atas +0,054842R, dan kali ini ia **berdasar** (ADR-024).
22. (S13, ADR-014) **Menuntut kesamaan bit pada agregat pecahan adalah pengujian yang menyala pada perilaku yang benar.** Di dalam satu fungsi murni, kesamaan bit tetap sah.
23. (S13, ADR-014) **Pagar yang memastikan masukan identik tidak memastikan masukan sah.** Diperluas di S17: **kesamaan hasil lintas dua run berbeda dilarang diterima tanpa pemeriksaan.** Semesta 4h yang persis 447 lalu persis 438 seperti 1h wajib dibandingkan simbol per simbol lebih dulu — dan sesudah dibandingkan, ia memang identik.
24. (S13, ADR-014) **Satu simbol dapat mendominasi agregat 438 simbol.**
25. (S13, ADR-014) **Himpunan tertahan habis pada saat pertama kali dilihat.**
26. (S13, ADR-014) **Cacat yang membalik tanda hasil tidak boleh diperbaiki di dalam hipotesis yang sama.**
27. (S13, ADR-014) **Eksperimen yang tercemar tidak informatif ke arah mana pun.**
28. (S13, ADR-014) **Saringan yang menolak entri juga menolak saat pemilihan.** Terbukti kuantitatif di H-012: hanya **62** entri ditolak pengaman.
29. (S14) **Pra-registrasi wajib diperiksa terhadap apa yang benar-benar dapat dihitung dari laporan.** Aturan ini **tidak dijalankan** atas modul H-013 sebelum run, dan akibatnya adalah cacat kelas kesembilan.
30. (S14) **Kriteria utama dihitung dari berkas laporan yang dikomit, bukan dari nilai yang beredar di memori run.**
31. (S15) **Pagar yang menyalin baris dari kode yang dijaganya tidak menjaga apa pun.**
32. (S15) **Aritmetika yang hidup di dalam `main` tidak dapat diuji.** `biaya_bolak_balik_R`, `harga_stop_terisi`, dan `lux/kerangka.py` seluruhnya lahir dari aturan ini.
33. (S15) **Setiap langkah workflow wajib `tee` ke `logs/` dan seluruh `logs/` disalin ke `reports/` dengan `if: always()`.**
34. (S15) **Lingkungan pagar wajib memasang dependensi yang sama dengan `tests.yml`.**
35. (S16) **Muatan tulis yang panjang wajib dibaca ulang utuh sebelum dikirim, dan jumlah pengujian dicacah dari muatan yang benar-benar dikirim, bukan dari rencana.** Sejak aturan ini dipatuhi, dua belas ramalan cacah berturut-turut tepat.
36. (S16, ADR-016) **Ramalan yang dijamin benar oleh konstruksi bukan ramalan.** Sebelum menghitung sebuah ramalan lulus, tunjukkan keadaan yang membuatnya gagal.
37. (S17, ADR-017–019) **Angka yang benar untuk satu interval tidak berubah nilai ketika dipakai di interval lain — ia berubah MAKNA, dan diam.** Setiap besaran yang berarti "satu hari", "satu minggu", atau "sekian jam" wajib diturunkan dari interval lewat `lux.kerangka`, tidak pernah dari literal.
38. (S17) **Dua definisi atas satu dataset selalu dimenangkan oleh yang tidak terlihat.** Pada cacat kelima, laporan mencetak semesta 438 yang benar sementara mesin memperdagangkan bar yang menurut semesta itu sudah tidak ada.
39. (S18) **Angka dapat hidup di berkas konfigurasi tanpa pernah masuk ke dalam program.** Cacat kelas kedelapan: `maks_biaya_masuk_R: 0.5` dan `stop_hormati_celah: true` tertulis rapi di `config/lux.yaml` dan tidak pernah dipetakan oleh `muat_konfig_h002`. Ia lebih sulit terlihat daripada angka yang salah, sebab berkasnya tampak benar. **Kode wajib dibandingkan terhadap berkas, bukan hanya dibaca.**
40. (S18, ADR-024) **Putusan yang dihitung dari separuh kriteria pra-registrasi adalah putusan palsu, dan ia paling berbahaya ketika angkanya menyenangkan.** Cacat kelas kesembilan: kriteria utama ADR-015 memuat dua syarat dalam satu kalimat — besaran **dan** p — sementara `kontribusi()` hanya menguji besaran. Ambangnya tidak digeser; yang hilang adalah sambungan antara ambang dan putusan. **Setiap ambang di dalam kriteria wajib punya baris kode yang memeriksanya, dan pemetaan itu wajib diperiksa sebelum run.**
41. (S18, ADR-024) **Prosa kesimpulan yang dipatok di dalam kode bukan kesimpulan.** Cacat kelas kesepuluh: `kontribusi.md` mencetak "sumbangan geometri lebih besar daripada sumbangan sinyal" pada nilai apa pun, dan pada run `30214203863` angkanya justru sebaliknya. **Kalimat yang menafsirkan angka wajib bergantung pada angka itu, dan arahnya wajib diuji.**

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa. Seluruh komputasi berjalan di GitHub Actions.

---

## 3. Fakta terverifikasi

### H-013 — SUDAH BERJALAN, PUTUSAN DITAHAN (ADR-024)

Run **`30214203863`**, mesin commit **`93a4309b`**, laporan dikomit **`e060749c`** pada 2026-07-26T18:21:35Z, sekitar **sepuluh menit** sesudah push. Blob `reports/backtest_log.md` berubah `cf4038f4` → **`4f272fab`**; `backtest_h013_kontribusi.json` **ada** (4.318 B) sehingga run **tidak** gagal. Delapan butir pagar pra-terbang **lulus**, 739 uji hijau di runner, 157 MB aset 4h terunduh, 438 simbol dimuat, **437 layak** sesudah lantai membuang **USDCUSDT** (median `stop_frac` 3,799992e−04), 4.082 jendela per sel.

| Sel | Sinyal | Target | Umur (bar 4h) | Trade | Ekspektasi R | p entri acak | Gerbang gagal |
|---|---|---|---|---|---|---|---|
| SS | sungguhan | ya | 42 | 60.018 | **+0,066648** | 0,0166 | `invarian_risiko`, `checksum` |
| SH | sungguhan | tidak | 48 | 44.614 | +0,037167 | 0,2259 | `entri_acak`, `invarian_risiko`, `checksum`, `funding_ekor` |
| AS | permutasi | ya | 42 | 55.927 | +0,011806 | 0,3588 | `entri_acak`, `lookahead`, `invarian_risiko`, `checksum`, `konsentrasi` |
| AH | permutasi | tidak | 48 | 45.378 | +0,058170 | 0,1993 | `entri_acak`, `lookahead`, `invarian_risiko`, `checksum`, `funding_ekor` |

Sidik: SS `06c3805bdd7ad4de` · SH `af1145aab7f13567` · AS `5ee4b130f9ed228d` · AH `4ada4587abede644`.

Tiga selisih: **sinyal (SS − AS) +0,054842R** · **geometri (SS − SH) +0,029481R** · **interaksi +0,075846R**. Turunan yang wajib ikut dikutip: **SH − AH = −0,021004R**, yakni tanpa target, sinyal sungguhan **kalah** dari sinyal permutasi.

**Mengapa ini BUKAN kelulusan** — tiga sebab, seluruhnya di ADR-024:

1. **Kriteria utama hanya separuh dihitung.** ADR-015 §4.4 menuntut "SS − AS ≥ 0,020R **dengan p permutasi ≤ 0,05 pada ≥ 300 ulangan**". `run_h013.kontribusi` menghitung `"lulus": sinyal >= AMBANG_KONTRIBUSI_SINYAL` dan tidak pernah menyentuh p. `p_entri_acak` yang tercetak adalah **uji lain** (mengacak entri **di dalam** satu sel, tidak pernah membandingkan SS terhadap AS), dan `"ulangan": 300` di `parameter_beku` adalah milik gerbang `entri_acak`. Sel AS memakai **satu** seed (`SEED_PERMUTASI = 42`), jadi +0,054842R adalah selisih terhadap **satu tarikan acak**, tanpa sebaran dan tanpa galat baku — kelas kesalahan aturan 19.
2. **Sel SS gagal dua gerbang**, `invarian_risiko` dan `checksum`, sementara ADR-015 §4.4 menuntut kesebelas gerbang lulus di SS. Keduanya **di luar** pengecualian konstruksi ADR-021 (yang hanya menutupi `lookahead` dan `entri_acak` pada AS/AH).
3. **Prosa `kontribusi.md` dipatok di kode** dan pada run ini ia membantah datanya sendiri (aturan 41).

**Adjudikasi ramalan H-013 — empat dari empat SALAH**, ditambah satu ramalan gerbang yang juga salah:

| Ramalan | Isi | Nyata | Putusan |
|---|---|---|---|
| ADR-015 §4.5 no. 1 | SS − AS di 0,000–0,015R sehingga GAGAL | **+0,054842R** | **SALAH** |
| ADR-015 §4.5 no. 2 | SS − SH lebih besar daripada SS − AS | +0,029481 lawan +0,054842 | **SALAH** |
| ADR-015 §4.5 no. 3 | AH sel terburuk, mungkin negatif | AH +0,058170 (kedua terbaik); **AS** terburuk | **SALAH** |
| ADR-015 §4.5 no. 4 | interaksi di −0,010…+0,010R | **+0,075846R** | **SALAH** |
| `RAMALAN["invarian_risiko"]` | lulus atau hampir lulus pada SS | **gagal** pada SS | **SALAH** |

Satu-satunya yang "tepat" — `lookahead` dan `entri_acak` gagal pada AS/AH — **bukan ramalan** menurut aturan 36.

**Konsekuensi yang tidak boleh dilunakkan:** ADR-015 §6 sudah menyatakan di muka bahwa bila SS − AS besar, dugaan pokoknya keliru dan sepuluh penolakan sisi masuk kembali menjadi teka-teki. Kalimat itu kini **berlaku bersyarat** — syaratnya p yang belum ada.

### Anggaran Jalur B sudah dihitung, dan ia TIDAK muat dalam satu job

Sel AS memakan sekitar **75 detik** pada 437 simbol (log run: `[437/437] ZRXUSDT: 271 trade, 75s`). 300 seed permutasi menuntut sekitar **6,25 jam** — di atas batas **6 jam** per job. Jalur B karena itu wajib berupa matriks job atau caching indikator; **bukan** pengurangan simbol dan **bukan** pengurangan seed. Jalur A dikerjakan lebih dulu karena ia dapat menjatuhkan Jalur B.

### AUDIT TUJUH WORKFLOW — SELESAI

Diperiksa satu per satu dari sumber, bukan diingat.

| Workflow | `git pull --rebase --autostash` | Catatan |
|---|---|---|
| `tests.yml` | **ada** | filter `lux/**`, `tests/**`, dirinya sendiri |
| `funding.yml` | **ada** (job `gabung`) | masih memakai `reports/universe_layak.json` (447 pra-lantai) |
| `funding_check.yml` | **ada** | masukan sama, `universe_layak.json` |
| `universe.yml` | **ada** | gerbang ditegakkan **sesudah** commit, disengaja |
| `doctor.yml` | **ada** | `set +e` disengaja: kegagalan probe adalah data |
| `backfill_daily.yml` | **ada** | **satu-satunya berjadwal**: `cron: '0 2 * * 1'` |
| `notion_asap.yml` | **TIDAK ADA** | `git push` polos, dan `git commit ... \|\| echo` sehingga kegagalan tidak menghentikan langkah |

Dengan empat yang sudah diketahui (`validate.yml`, `potong_ekor.yml`, `backtest.yml`, `ingest_tier_b.yml`) dan `geometri.yml`, maka **sebelas dari dua belas** workflow memakai pola itu; `notion_asap.yml` satu-satunya yang tidak.

**Temuan yang tidak dicari dan lebih penting:** `backfill_daily.yml` berjalan **setiap Senin 02:00 UTC** tanpa dipicu manusia, mengunggah Parquet ke rilis `tier-b-v1` dengan `--clobber`, dan mengomit ke `reports/`. Jadi ada proses yang dapat mengubah aset dan laporan **tanpa** saya memicunya, dan itu wajib diketahui sebelum menafsirkan blob yang berubah sendiri (aturan 2 bekerja ke dua arah).

### TEMUAN S17 — lima cacat buta-interval, semuanya sejenis, semuanya ditutup

| # | Cacat | Akibat bila 4h dijalankan apa adanya | Ditutup di |
|---|---|---|---|
| 1 | `validate_run` menulis `universe_layak.json` tanpa interval | keluaran 4h menimpa masukan 1h | `02933b85` |
| 2 | `muat_ambang` membaca `min_bar_1h` untuk interval apa pun | lantai riwayat 8.760 bar dipakai untuk 4h (= 4 tahun) | `fe7fd30e` |
| 3 | `MIN_PANJANG` / `MIN_BAR` buta interval di `potong_ekor` | ekor 1–3 hari lolos pada 4h | `6aacef40` |
| 4 | keluaran `potong_ekor` 4h menimpa masukan backtest 1h | dataset H-012 tertimpa tanpa pesan galat | `6aacef40` + pagar `5296162d` |
| 5 | **`muat_ohlcv` memangkas ekor dengan ambang 1h** | **dua definisi ekor atas satu dataset; yang menentukan hasil adalah yang salah** | `409343f3` |

**Cacat keenam dan ketujuh (S18):** ADR-020 menutup `maks_umur_bar` 168 yang pada 4h berarti 28 hari; **ADR-023** (`4007e189`, dilaksanakan `8bda1473`) menutup jendela walk-forward — `panjang_latih` 4320, `panjang_uji` 2160, `embargo` 168 adalah satuan **waktu** milik 1h, dan pada 4h ketiganya menuntut **6.848 bar** (~3,1 tahun) sementara dataset 4h hanya ~4.600 bar per simbol dengan lantai 2.190. Sesudah konversi: **1.080 / 540 / 42**, satu jendela **1.862 bar**, di bawah lantai. `pemanasan` **200 tidak dikonversi** dengan sengaja (lookback 100 + ATR 14 adalah kebutuhan bar, bukan waktu), dan ketidaksimetrisan itu dijaga pengujian. Terbukti di run: **4.082 jendela per sel**, bukan nol.

### CACAT KELAS KEDELAPAN — angka di config yang tidak pernah dibaca program

Run H-013 **pertama** (`30213913942`, commit `135b159c`) mati di pagar pra-terbang butir 3: `assert dasar.maks_biaya_masuk_R == AMBANG_BIAYA_MASUK_R`. Sebabnya dibaca verbatim dari `run_h002.py` (blob `8bf480da`): **`muat_konfig_h002` memetakan delapan kunci saja** — `fee`, `slippage`, `atr_periode`, `atr_pengali_stop`, `risiko_per_trade`, `maks_umur_bar`, `maks_carry_R`, `jendela_carry_hari`. `maks_biaya_masuk_R` dan `stop_hormati_celah` **tidak** ada di sana, meski keduanya tertulis di `config/lux.yaml` sebagai `0.5` dan `true`.

**Perbaikannya tidak menyentuh pemuat lama** (dipakai dua belas hipotesis; mengubahnya mengubah arti laporan yang sudah dikomit). Sebagai gantinya `run_h013.dasar_riset` memasang kedua medan eksplisit dari `lux.degenerasi.AMBANG_BIAYA_MASUK_R` dan `True` — commit **`ab3e9792`**, **739 uji, ramalan tepat**, blob `reports/tests.md` `5f60216a`. Satu uji **mengunci cacatnya sebagai perilaku**: config uji yang memuat `0.5` tetap wajib menghasilkan `0.0`, sehingga perbaikan diam-diam di masa depan akan menjatuhkan uji itu dan memaksa penjurnalan.

Pagar butir 3 **diperkuat, bukan diturunkan** (commit **`93a4309b`**): kini ia menuntut config dan `degenerasi` sepakat pada 0,004 dan 0,5R, **dan** pemuat config tetap tidak memetakan kedua kunci itu, **dan** `dasar_riset` yang memasangnya. Log run kedua mengonfirmasi: `3. angka kembar, pengaman DIPASANG dasar_riset: OK`.

**H-012 tidak terkena** cacat ini: ia memasang pengaman lewat `replace` dari konstanta `degenerasi`, dan log run `30200123505` mencetak `pengaman 0.5R` dari sumber itu.

### UTANG TEKNIS — tiga kunci config yang tidak pernah dibaca

Tiga temuan sejenis berarti ini **pola**, bukan kebetulan:

1. `universe.maks_rasio_bar_datar: 0.30` — **tidak dibaca gerbang backtest**. Angka 0,30 hidup sebagai bawaan fungsi di `gerbang.py` dan literal di `runner.py`/`run_wf.py`, hanya sebagai `ambang` yang **dilaporkan**. Menyuntingnya di config tidak mengubah perilaku apa pun sementara laporan tetap mencetak 0,30.
2. `risiko.maks_biaya_masuk_R: 0.5` — tidak dipetakan `muat_konfig_h002`.
3. `risiko.stop_hormati_celah: true` — tidak dipetakan `muat_konfig_h002`.

Keberatan ADR-018 yang masih berdiri: `MAKS_RASIO_DATAR = 0.10` dipakai untuk kedua interval padahal rasio bar datar 4h mekanis lebih kecil, jadi gerbang itu **lebih longgar** di 4h. Menggesernya sesudah melihat hasil 4h melanggar aturan 13.

### KERANGKA 4h — semesta berdiri sendiri, dan kesamaannya diperiksa

**Validasi 4h**, run **`30211176709`**, ADR-017 (`494c9bbc`): **3.636.733 baris / 790 simbol**; **layak 447**; tidak layak 343 (riwayat pendek 277, bar datar 74, likuiditas 77); celah 112; duplikat **0**. Keempat ramalan ADR-017 benar.

**Pemangkasan ekor 4h**, run **`30211673239`**, ADR-018 (`30a6d228`): ambang **6 bar**, lantai 2.190; **790 dipindai** · **141 berekor datar** · **270.398 bar dipangkas** · 447 → **438 layak / 9 ditolak** · **nol** penolakan gerbang `maks_rasio`. Kelima ramalan benar; selisih ramalan bar 270.480 lawan nyata 270.398 = **−82 bar (0,030%)**, terhitung habis oleh pembulatan kisi.

**Aturan 23 dijalankan dua kali:** 438 simbol 4h (blob `e7d0f5ca`, `universe_layak_v2_4h.json`) dibandingkan **simbol per simbol** dengan 438 simbol 1h — **identik**. **Pagar legasi terbukti di disk:** blob `universe_layak_v2.json` identik sebelum dan sesudah run 4h (`a484670f` pada `7c68431a` dan pada `80a8f3a5`).

**ASET 4h TERVERIFIKASI ADA** di rilis `tier-b-v1` (id `359778114`): 12 berkas, 157.628.619 B; log unduh run H-013 mencetak `157M aset` dan dua belas berkas `ohlcv_4h_*`.

### Papan ramalan jumlah pengujian

| Commit | Ramalan | Nyata | Putusan |
|---|---|---|---|
| `864da2ec` | 635 | **638** | SALAH |
| `3880408f` | 642 | 642 | TEPAT |
| `b4b1963c` | 643 | 643 | TEPAT |
| `eae7eb3a` | 662 | **665** | SALAH |
| `955b419a` | 673 | 673 | TEPAT |
| `fb710521` | 673 tetap | — | **TIDAK DAPAT DIADILI** |
| `02933b85` | 679 | 679 | TEPAT |
| `fe7fd30e` | 683 | 683 | TEPAT |
| `6aacef40` | **693** | **694** | **SALAH** |
| `47ef9a90` | 702 | 702 | TEPAT |
| `ba42a401` | 703 | 703 | TEPAT |
| `e7697300` | 709 | 709 | TEPAT |
| `1a3e1e5d` | 711 | 711 | TEPAT |
| `409343f3` | 714 | 714 | TEPAT |
| ADR-020 langkah 1 | 716 | 716 | TEPAT |
| ADR-020 langkah 2 | 721 | 721 | TEPAT |
| ADR-020 langkah 3 | 734 | 734 | TEPAT |
| `8bda1473` | 737 | 737 | TEPAT |
| `ab3e9792` | 739 | **739** | TEPAT |

Jejak: 444 → … → 714 → 716 → 721 → 734 → 737 → **739**. **Dua belas ramalan cacah berturut-turut tepat.**

**Papan ramalan perilaku sistem, S18: nol dari enam tepat** (pagar butir mana yang jatuh; empat ramalan angka H-013; `invarian_risiko` pada SS). Polanya konsisten dan wajib diingat: **yang dapat dicacah bisa diramalkan; yang menuntut membaca kode atau menuntut data tidak.**

### H-012 — DITOLAK (ADR-014 §8)

Run **`30200123505`**, commit **`56a325d2`**, sidik **`75f9c7ccd65ec30f`**, **1220,6 detik**, 437 dari 438 simbol, 4.081 jendela.

| Sisi batas | Bulan | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|
| **Tahan (sejak `2026-01`)** | 7 | **22.117** | +922,56 | **+0,041713** |
| Sebelum `2026-01` | 66 | 113.564 | +7.168,96 | +0,063127 |
| Seluruh riwayat | 73 | 135.681 | +8.091,52 | +0,059636 |

Selisih tahan − sebelum **−0,021414R**. **0,041713R < 0,05R → GAGAL.** Sebelas gerbang: **entri_acak GAGAL p 0,06312292358803986** · **invarian_risiko GAGAL −21,3131R** · **funding_ekor GAGAL `funding_maks_R` 0,6601**; sisanya lulus. Skor entri acak nyata **0,04661R** — persis angka H-010. Sebaran: std 2,22746R, galat baku 0,006047R, CI95 **[0,047784, 0,071489]R** yang **memuat** 0,05. Entri ditolak pengaman **62**.

### Papan skor hipotesis

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
| H-012 | semesta berlantai 0,004 + pagar 0,5R, sejak 2026-01-01 | **0,041713 (periode tahan)** | `entri_acak` · `invarian_risiko` · `funding_ekor` | **DITOLAK** |
| **H-013** | faktorial 2x2 sinyal × geometri keluar, 4h | SS **+0,066648**; **SS − AS +0,054842** | SS: `invarian_risiko`, `checksum` | **BELUM DAPAT DINILAI** (p atas selisih tak pernah dihitung; dua gerbang SS gagal) |

Sidik dua belas hipotesis pertama: H-001b `e458f4c82abf6735` · H-002 `16fb57692a6f0888` · H-003 `3a1cdc867f61bf67` · H-004 `98d6a5e15b2cc08b` · H-005 `9c4b6324e79569eb` · H-006 `e503a9a833182b25` · H-007 `7f5e7aeeaa29284b` · H-008 `dfeeea04fd4107f6` · H-009 `eac6c83305bd1069` · H-010 `14b2f3bfa8a754b5` · H-011 `8a6efde6d333d8b5` · H-012 `75f9c7ccd65ec30f`.

**Sebelas dari dua belas ditolak.** Yang satu itu lulus pada 100 permutasi dan gagal pada 300. Yang ketiga belas **belum dinilai**.

**Kesimpulan struktural — kini DIPERTANYAKAN, bukan dibatalkan:** sampai S17, enam percobaan sisi masuk menghasilkan nol perbaikan sementara empat percobaan sisi keluar menghasilkan seluruh kemajuan, dan skor entri acak identik 0,04661R di H-010 dan H-012 dibaca sebagai bukti bahwa keunggulan seluruhnya milik geometri keluar. Run H-013 memberi angka yang **berlawanan** (sinyal +0,054842 lawan geometri +0,029481). Sampai p ada, **tidak satu pun dari dua bacaan itu boleh dinyatakan sebagai posisi**.

### TEMUAN S16 — mesin buta terhadap celah harga pada jalur stop

1. Gerbang `invarian_risiko` H-012 gagal pada **−21,3131R** terhadap ambang −1,5R.
2. Diagnostik `lux/analisis/geometri_keluar.py`, run **`30209272338`**: perdagangan itu **STGUSDT**, keluar lewat **`carry`**, `transaksi_R` 0,0559, `funding_R` 0,4825, pelampauan di luar biaya **20,3131R**, `stop_frac` 2,197%, `jam` **1,0**.
3. Tidak satu pun keluar `stop` di bawah −1,5R; stop terburuk **−1,4966R**; median pelampauan jalur stop **0,410263R**.
4. `engine.py` (blob `621298a8`): di blok stop/target, `harga = stop if kena_stop else target`. **Harga bar tidak pernah dipakai.**

**Konsekuensi yang wajib ikut dikutip setiap kali angka R lama disebut:** gerbang `invarian_risiko` **praktis tidak berdaya pada jalur stop**; dua belas hipotesis pertama dinilai mesin yang **optimistis terhadap risiko celah**; arah biasnya **melawan penolakan**, jadi **tidak ada vonis yang perlu dibalik**, tetapi **tidak satu pun angka R lama boleh disebut konservatif**. Jalur `carry` **bukan** yang cacat. Klaim "mekanisme stop sendiri sehat" **DITARIK** (ADR-016 §2).

Perbaikannya terpasang dan hijau: `Konfig.stop_hormati_celah` bawaan **MATI** + `harga_stop_terisi` (`955b419a`, 673 uji), dinyalakan di config (`fb710521`) — dan S18 membuktikan penyalaan lewat config itu **tidak pernah bekerja** untuk pemuat H-002 (aturan 39); yang menyalakannya di H-013 adalah `dasar_riset`. **Hasil H-001b sampai H-012 TIDAK dihitung ulang.**

**Catatan baru dan penting:** pada H-013, `stop_hormati_celah` **menyala** dan `invarian_risiko` **tetap gagal pada keempat sel**, termasuk SS. Jadi kegagalan itu tidak lagi dapat dijelaskan sebagai kebutaan celah, dan besarnya **belum dibaca**.

### SEMESTA, HIMPUNAN TERTAHAN, TITIK IMPAS

**Himpunan tertahan HABIS**: hasil per simbol 438 simbol sudah dilihat (H-011) dan tabel 73 bulan sudah dilihat (H-012). Dimensi 4h kini **juga sudah terpakai** oleh H-013.

Titik impas `1/(1+imbalan)`: 1R 0,5000 · 2R 0,3333 · 4R 0,2000 · 6R 0,1429 · 8R 0,1111. Di H-009, **194 dari 356 jendela (54,5%)** memilih imbalan 4,0 — versi 16 menulis 226 dan 63,5%; **itu salah**. Seretan: H-002 0,04926 · H-009 0,034614 · H-010 0,036220 · H-011 0,125520 (tercemar) · H-012 **0,035900**.

Pemilihan lookback H-013 per sel (dari 4.082 jendela): SS 20→1682, 55→846, 100→1554 · SH 20→1987, 55→1069, 100→1026 · AS 20→1408, 55→1089, 100→1585 · AH 20→1392, 55→1073, 100→1617.

### MESIN BACKTEST

**`engine.Konfig` — nama medan terverifikasi dari sumber:** `fee` (0,0005), `slippage` (0,0005), `atr_periode` (14), `atr_pengali_stop` (2,0), `risiko_per_trade` (0,005), `imbalan_R` (2,0), `modal_awal` (10.000), `izinkan_short` (True), `maks_umur_bar` (0), `maks_carry_R` (0,0), `jendela_carry_hari` (30), `maks_carry_realisasi_R` (0,0), `maks_biaya_masuk_R` (0,0), **`stop_hormati_celah` (False)**, `pakai_target`. **Tidak ada medan bernama `fee_efektif`** — itu kunci YAML. Lima medan bawaan **MATI** dan dikunci pengujian serta pagar `dataclasses.fields`.

**Urutan pemeriksaan per bar:** umur → carry realisasi → stop/target → entri (pengaman biaya lalu carry proyeksi) → ekuitas. `umur` dan `carry` mengisi pada `o[t]`, `akhir_data` pada `c[-1]` — ketiganya jujur terhadap celah.

Gerbang (11): `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`, `konsentrasi`, `funding_ekor`. **Tidak dapat dinilai = GAGAL.**

**Modul H-013** (`lux/backtest/run_h013.py`): `NAMA_SEL` (SS, SH, AS, AH) · `dasar_riset` · `jendela_bar` · `bar_dibutuhkan` · `pakai_target_sel` · `umur_sel` · `sinyal_acak_sel` · `kandidat` · `permutasi_sinyal` · `sinyal_acak` · `buat_konfig_sel` · `hipotesis_h013` · `spek_sel` · `kontribusi`. Beku: `IMBALAN_BEKU` 2.0 (ADR-022), `H_BAR` 48, `UMUR_SEL_STOP` `bar_dari_hari(7, "4h")` = 42, `SEED_PERMUTASI` 42, `AMBANG_KONTRIBUSI_SINYAL` 0,020, `MIN_ULANGAN` 300, `MIN_TRADE_SEL` 100, `PEMANASAN` 200. Tripwire dataset **DIBALIK**: dataset wajib **berbeda** dari H-002/H-009 dan wajib menyebut `4h`.

### DATASET TIER B PUTARAN 2

**14.545.679 bar 1h dan 3.636.733 bar 4h**, 790 simbol, rasio 3,9996, ~703 MB. 1h: 447 valid → v2 **438** → berlantai **437**. 4h: 447 valid → v2 **438** (identik 1h, terperiksa) → berlantai **437** pada H-013. Funding 1.982.017 baris, 3 celah sejati, 79,1% positif; run H-013 memuat **447 jadwal funding** dan memindai **790 simbol** untuk survivorship.

### Kapasitas runner dan konektivitas

4 vCPU, 15 GB RAM. **Batas 6 jam per job yang mengikat, bukan disk.** H-012 memakai 1220,6 s; H-013 empat sel selesai dalam sekitar **sepuluh menit** total termasuk unduhan. python 3.12.13, numpy 2.5.1, pytest 9.1.1, pandas 2.2.3, pyarrow 17.0.0, **tanpa scipy**, **tanpa requests**. CDN `data.binance.vision` 200; REST `fapi.binance.com` **451 permanen**. Timeout: backtest 330, validate 120, potong_ekor 60, ingest 330.

### Batas alat agen dan solusinya

- Daftar alat GitHub **tidak memuat satu pun fungsi Actions**. Diverifikasi ulang di S18.
- `search_code` **nol hasil di repo ini**. `get_file_contents` menuntut SHA 40 karakter penuh, tetapi **menerima `ref: "main"`**.
- `push_files` **mengganti seluruh isi berkas**, jadi baca dulu sebelum menulis ulang, dan baca ulang muatannya sebelum mengirim (aturan 35).
- Filter `paths` per berkas: menyentuh `.github/workflows/backtest.yml` **langsung memulai run**. `tests.yml` memfilter `lux/**` dan `tests/**`, jadi perubahan `config/`, `journal/`, `decisions/`, dan `STATE.md` **tidak** memicunya.
- **Kabar buruk datang dalam 23–32 detik; kabar baik 10–20 menit.** Run H-013 kedua memberi kabar baik dalam ~10 menit, jadi "20 menit" adalah batas atas, bukan patokan.
- **Commit laporan tanpa berkas hasil berarti run GAGAL. Blob laporan yang tidak berubah berarti belum ditulis.**
- **`backfill_daily.yml` berjadwal mingguan**, jadi tidak setiap perubahan blob berasal dari saya.
- **Modul baru berdiri hijau sendiri lebih dulu. Baca modulnya sebelum menulis kode terhadapnya.**

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1–3**, **metrik celah funding**, **circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`).
- **S12:** STATE v11 dan v13 menaikkan kekeliruan menjadi fakta; ditarik v12 dan v14.
- **S13:** "226 dari 356 jendela (63,5%)" padahal **194 (54,5%)**. **Degenerasi wajib dibuktikan lewat `stop_frac`, bukan ejaan.**
- **S15:** empat run gagal berturut (`30198306280` · `30198631730` · `30198840830` · `30198942815`). Aturan 31–34.
- **S16:** dua commit cacat (`953ce24a`, `2a0f8545`); dua ramalan cacah salah; klaim "mekanisme stop sehat" ditarik. Aturan 35–36.
- **S17:** lima cacat buta-interval; ramalan 693 salah; klaim v21 tentang `git pull --rebase` salah; daftar aset v21 lahir dari `ls` yang tersaring. Aturan 37–38.
- **S18:** cacat kelas kedelapan (config tak terbaca), kesembilan (putusan dari separuh kriteria), kesepuluh (prosa dipatok di kode). Aturan 39–41.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| **`checksum` gagal pada keempat sel H-013 karena manifes menyebut 12 berkas `ohlcv_1h_*` sementara yang diunduh 12 berkas `ohlcv_4h_*`** | pola `hilang 12, asing 12, tidak cocok 0` sesuai, tetapi belum dibuktikan dari sumber `checksum` maupun manifes. Sampai terbukti: tidak dapat dinilai = GAGAL |
| **Besar kegagalan `invarian_risiko` pada sel SS** | baca `reports/backtest_h013_ss_sinyal_stop.json` (432.200 B) |
| **Selisih SS − AS bertahan sesudah p dihitung** | ADR-024 Jalur A lalu Jalur B; sebelum itu +0,054842R bukan temuan |
| **SH − AH negatif (sinyal sungguhan kalah dari permutasi tanpa target) bukan artefak satu seed** | menuntut sebaran permutasi yang sama dengan Jalur B |
| STGUSDT benar-benar bergerak melawan ~46,8% dalam rentang ~satu bar 1h | bar itu di rilis artefak, dan sandbox tanpa jaringan |
| Ekspektasi R dengan `stop_hormati_celah` menyala lebih rendah daripada dengan medan mati | ramalan 5 ADR-016; **belum teradili** — H-013 tidak punya pasangan bermedan-mati untuk dibandingkan, dan membuatnya berarti menjalankan ulang |
| Gerbang bar datar 4h lebih longgar daripada 1h karena rasio mekanis lebih kecil | baca `reports/validate_1h.json` dan bandingkan sebaran rasio 1h lawan 4h |
| Funding sebagai **sinyal** memuat informasi arah | belum pernah diuji |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap universe layak v2 438 |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |

**Difalsifikasi sebelumnya:** saringan rezim tren memperbaiki breakout · retest memperkecil biaya per R · SMC yang dapat dikodekan punya keunggulan · "biaya menjaga risiko memakan ekspektasi" · "ekspektasi bergantung umur simbol" · "kerugian ekor dari bar menganga pada stop" · sinyal `breakout_atr` punya keunggulan yang bertahan di waktu pada 1h (H-012) · lantai 0,004 menutup **seluruh** jalan masuk degenerasi (sebagian) · "hasil 40 simbol mewakili 438 simbol" · dugaan bahwa `gabung_gerbang` membuang syarat deret datar · **"jendela walk-forward adalah jumlah bar"** (ADR-023) · **"nilai di `config/lux.yaml` sampai ke mesin"** (aturan 39).

**Terbukti benar:** imbalan lebih besar menaikkan ekspektasi (+28%) · lama pegang membesarkan kerugian ekor · keunggulan bertahan bila penyumbang terbesar dibuang (retensi 0,9849) · "H-012 gagal", diramalkan sebelum run · jalur 1h bit-identik sesudah ADR-019 · **konversi jendela ADR-023 menghasilkan 4.082 jendela per sel, bukan nol**.

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 · metrik celah funding putaran 1–4 · seluruh run pilot H-001 termasuk `30170073890` · porsi "101,2%" · nilai gerbang `funding` sebagai bukti funding aman · "226 jendela / 63,5%" · ekspektasi H-010 0,053028R sebagai bukti layak dagang · **+0,060163R** · **+0,059546R** · **+0,060168R** · **281 dari 398 simbol positif** dan median **+0,06343** · **−0,091519R** tanpa sebabnya · **+0,059636R** sebagai kelulusan · **+2.347,27R bulan 2026-01** atau bulan mana pun · gerbang bar datar 4h dan gerbang `maks_rasio` 4h sebagai bukti kebersihan data · **`+0,054842R` sebagai kelulusan H-013** · **`+0,066648R` sebagai bukti layak dagang** · **kata "LULUS" pada `reports/backtest_h013_kontribusi.md`** · **kalimat "sumbangan geometri lebih besar daripada sumbangan sinyal" pada berkas itu** (prosanya dipatok di kode dan datanya membantahnya).

---

## 5. Penghalang aktif

Tidak ada run yang berjalan. Tidak ada yang dibutuhkan dari pengguna. Satu hal yang wajib diingat: **`backfill_daily.yml` dapat berjalan sendiri setiap Senin 02:00 UTC.**

---

## 6. Tindakan berikutnya

1. ~~`stop_hormati_celah` + config~~ · ~~`validate.yml` 4h (ADR-017)~~ · ~~`potong_ekor` berinterval (ADR-018)~~ · ~~satuan hari (ADR-019)~~ · ~~kerangka H-013 4h (ADR-020)~~ · ~~sel pembanding (ADR-021)~~ · ~~imbalan beku (ADR-022)~~ · ~~jendela walk-forward (ADR-023)~~ · ~~modul H-013 hijau sendiri, 739~~ · ~~`backtest.yml` dibalik ke H-013~~ · ~~jalankan H-013~~ — **semuanya selesai**.
2. **ADR-024 Jalur A — p atas SS − AS dari laporan yang sudah dikomit.** Modul baru, hijau sendiri lebih dulu, tanpa run: pasangkan selisih **per jendela** dari `backtest_h013_ss_sinyal_stop.json` dan `backtest_h013_as_acak_stop.json`, lalu uji permutasi tanda atau bootstrap. **Wajib dinyatakan terang bahwa ini mengukur ketidakpastian sampling jendela, BUKAN sebaran permutasi sinyal**, sehingga ia **tidak** memenuhi ADR-015 §4.4 sendirian.
3. **Baca `reports/backtest_h013_ss_sinyal_stop.json`** untuk nilai `invarian_risiko` SS yang sebenarnya. Angkanya menentukan apakah kegagalan itu satu peristiwa (aturan 24) atau pola.
4. **Buktikan atau bantah dugaan `checksum`** (manifes 1h lawan aset 4h). Selama belum, kelulusan gerbang sel SS tidak dapat diklaim.
5. **Prosa `kontribusi.md` dibuat bergantung angka**, dengan pengujian yang mengunci arah kalimat terhadap tanda dan urutan besaran selisih (aturan 41). Menyentuh `lux/**` memicu `tests.yml`, dan itu memang yang diinginkan.
6. **ADR-024 Jalur B** hanya sesudah Jalur A: sebaran ≥300 seed permutasi pada sel AS, sebagai **matriks job** (anggaran ~6,25 jam melebihi batas 6 jam satu job) atau dengan caching indikator. **Bukan** pengurangan simbol, **bukan** pengurangan seed.
7. **Segarkan `PROMPT_KELANJUTAN.md`** — tertinggal sebelas aturan (31–41) dan seluruh S18. Wajib **dibaca utuh** lebih dulu; menulis ulang dari ingatan adalah kelas kesalahan "226 jendela".
8. **`notion_asap.yml`:** `git push` polos tanpa `git pull --rebase --autostash`, dan `git commit ... || echo` yang menelan kegagalan. Perbaiki atau hapus — ia sudah menuntaskan tugasnya membuktikan kredensial.
9. **Tinjau workflow yang mungkin tak lagi diperlukan:** `funding.yml` dan `funding_check.yml` (ingest funding selesai; keduanya masih memakai `reports/universe_layak.json` pra-lantai), `doctor.yml`, `universe.yml`. **Jangan hapus tanpa keputusan tertulis.**
10. Baca `reports/validate_1h.json` untuk mengukur asimetri gerbang bar datar 1h lawan 4h.
11. Utang teknis: **sambungkan `maks_rasio_bar_datar` config ke gerbang** · periksa kunci config lain yang mungkin tak pernah dibaca (aturan 39) · `hasattr`/`__import__` di `test_run_h012.py` · pengujian `biaya_bolak_balik_R` · `pytest` ke `requirements-dev.txt` · docstring `median_stop_frac_bingkai` · nama ganda legasi `potong_ekor` · tripwire tekstual `inspect.getsource` di `test_runner_interval.py` (lemah, dicatat sebagai lemah) · pemetaan `dari_laporan` pelapor Notion terhadap kunci JSON `runner.py`.
12. **Funding sebagai sinyal.** Belum pernah diuji kandungan informasi arahnya.
13. Perketat `lux/funding.py::gerbang_lulus` · diff Dataset G lama · `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md` · salin ADR-001/ADR-002 ke `decisions/` · naikkan `versi` config sesudah seluruh pembacanya diperiksa · Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, ≥24 shard.

**Yang DILARANG:** menyatakan sistem siap dagang · **menyebut H-013 lulus, atau mengutip +0,054842R / +0,066648R sebagai kelulusan atau kelayakan** · mengutip +0,060163R atau +0,059636R sebagai kelulusan · membuang simbol atau memilih bulan sesudah melihat hasil · **menyebut H-012 atau H-013 sebagai "H-010 setelah perbaikan"** · menyebut angka R lama **konservatif** · **menghitung ulang H-001b sampai H-012 dengan mesin ADR-016** · menggeser lantai 0,004, pagar 0,5R, `BATAS_VOID` 20, batas `2026-01-01`, **ambang SS − AS 0,020R**, **p ≤ 0,05**, **≥300 ulangan**, **≥100 trade per sel**, `MAKS_RASIO_DATAR` 0,10, atau ambang rasio 0,30 · mematok `imbalan_R` ke 8,0 · melombakan `imbalan_R` di H-013 · melombakan `h` atau `pakai_target` · menurunkan `--ulangan` dari 300 · menaikkan `maks_umur_bar` dari 168 sebagai penyelamatan · membuang simbol merugi · memakai `konsentrasi` atau `funding_ekor` sebagai penyaring simbol · melombakan ambang pengaman · melonggarkan `invarian_risiko` dari −1,5R · **menurunkan maupun menaikkan ambang ekspektasi 0,05R** · menjadikan `stop_hormati_celah` parameter yang dilombakan · **memperbaiki `muat_konfig_h002` tanpa ADR** · **menurunkan pagar pra-terbang yang menemukan cacat**.

---

## 7. Pengawasan otonom — DIHENTIKAN

Agen **LUX Gatekeeper** dan **LUX Gatekeeper Reporter** **tidak dipakai lagi.** Keputusan pengguna, 2026-07-26: kreditnya kemungkinan habis sebelum riset selesai.

Keputusan itu sehat melampaui penghematan. Bukti dari sisi Notion atas baris asap `3a9d5df0-96f9-81df-90a7-f6075d071680`: agen itu mengadili **setiap** baris otomatis dalam sekitar dua menit, termasuk baris yang menyatakan `bukan_hasil_riset=true`, dan memakai `Ditolak` untuk "bukti tidak cukup" padahal `Ditolak` semestinya berarti hipotesis gagal. **Vonis yang salah arti lebih buruk daripada tidak ada vonis** — dan S18 menambahkan bentuk kedua dari penyakit yang sama: **vonis benar arti yang dihitung dari separuh kriteria.**

Kolom `Verdict` di database `LUX — Run Results` karena itu menjadi kolom **manusia**. Pelapor Notion tetap dipertahankan sebagai papan hasil yang dapat dibaca dari ponsel. Pekerjaan "selaraskan instruksi Gatekeeper dari sembilan ke sebelas gerbang" **dibatalkan**.

---

## 8. Peta repo

| Path | Isi |
|---|---|
| `config/lux.yaml` | seluruh parameter yang memengaruhi hasil; `min_bar_1h` 8.760, `min_bar_4h` 2.190, lantai `min_median_stop_frac` 0,004, pagar `maks_biaya_masuk_R` 0,5, `stop_hormati_celah` true; **tiga kunci TIDAK DIBACA**: `maks_rasio_bar_datar`, `maks_biaya_masuk_R`, `stop_hormati_celah`; `versi` masih 2 |
| `lux/kerangka.py` | **modul daun**: `JAM_SEHARI`, `INTERVAL_JAM`, `bar_per_hari`, `jam_interval`, `interval_dikenal`, `bar_dari_hari`. Tidak mengimpor apa pun dari `lux` |
| `lux/binance_vision.py` | klien arsip: listing S3, unduhan, checksum |
| `lux/universe.py` | universe point-in-time dan klasifikasi kontrak |
| `lux/ingest.py` · `lux/backfill_daily.py` | ingest Tier B dan penutup celah ekor |
| `lux/validate.py` · `lux/validate_run.py` | integritas OHLCV; `muat_ambang(path, interval)` gagal keras; `nama_keluaran_universe` berinterval |
| `lux/funding.py` · `lux/funding_check.py` | ingest funding dan metrik kisinya; `gerbang_lulus` masih longgar |
| `lux/funding_model.py` | jadwal funding nyata, penagihan, carry |
| `lux/costs.py` | model biaya dalam satuan R; **BUKAN jalur kritis** |
| `lux/degenerasi.py` | satuan R yang runtuh: ambang 0,004 dan 0,5R, `saring_semesta`, `AMBANG_BIAYA_MASUK_R` |
| `lux/notion_reporter.py` | pelapor baris hasil lewat `urllib.request`; kredensial terverifikasi run `30207584722` |
| `lux/diag_datar.py` · `lux/potong_ekor.py` | diagnosis dan pemangkasan ekor datar; keluaran **berinterval**; memakai `lux.kerangka` |
| `lux/praregistrasi.py` | hipotesis sekali tulis; **tidak membaca config** |
| `lux/analisis/{titik_impas,sebaran,periode,geometri_keluar}.py` | aritmetika atas laporan yang sudah dikomit; galat baku **taksiran bawah** |
| `lux/strategi/breakout_atr.py` | sinyal kelanjutan (H-001b, H-002, H-007–H-013) |
| `lux/strategi/{reversi_zskor,rezim_adx,retest,smc}.py` | H-003 · H-004 · H-005 · H-006 |
| `lux/backtest/engine.py` | mesin eksekusi; **lima saringan bawaan MATI**; `harga_stop_terisi`; `pakai_target` |
| `lux/backtest/gerbang.py` | sembilan gerbang pertama; `gerbang_forward_fill(df, maks_rasio_datar, maks_deret_datar, interval)` |
| `lux/backtest/konsentrasi.py` · `funding_ekor.py` | gerbang kesepuluh dan kesebelas |
| `lux/backtest/walk_forward.py` | pemilihan parameter dalam sampel; tidak memanggil gerbang apa pun |
| `lux/backtest/run_wf.py` | orkestrator H-001b — **jangan disunting kecuali dengan ADR** |
| `lux/backtest/run_h002.py` · `run_h003.py` | orkestrator beku; **`muat_konfig_h002` memetakan DELAPAN kunci saja** dan tidak boleh diperbaiki tanpa ADR (aturan 39) |
| `lux/backtest/runner.py` | runner bersama: muat sekali, lantai semesta, sebelas gerbang, jackknife, ekor funding, sebaran, penolakan biaya, agregat periode |
| `lux/backtest/run_h007.py` | **sumber grid bersama, HARAM disunting** |
| `lux/backtest/run_h010.py` · `run_h011.py` · `run_h012.py` | grid imbalan {2,4,6,8} · `BATAS_H010 = 40` · `BATAS_VOID = 20`, `PERIODE_TAHAN_TANGGAL`, `kunci_config` |
| `lux/backtest/run_h013.py` | empat sel H-013; `dasar_riset`, `jendela_bar`, `bar_dibutuhkan`, `kontribusi` — **`kontribusi` hanya memeriksa separuh kriteria (ADR-024)** |
| `tests/` | **739** pengujian tanpa jaringan, wajib hijau sebelum unduhan |
| `reports/` | keluaran mesin tiap run; berkas 4h bernama berinterval; empat berkas sel H-013 masing-masing ~432 KB |
| `hipotesis/` | pendaftaran sekali tulis: `H-001b` … `H-012`, `H-013-SS/SH/AS/AH` |
| `decisions/` | ADR-003 … **ADR-024** |
| `journal/` | riwayat per sesi, sampai **`2026-07-27-19.md`** |

**Workflow aktif (12):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`, `notion_asap`, `geometri`. **Sebelas dari dua belas** memakai `git pull --rebase --autostash origin main` sebelum push; **`notion_asap.yml` tidak**. **`backfill_daily.yml` satu-satunya berjadwal** (`cron: '0 2 * * 1'`). `backtest.yml` kini memuat **H-013 empat sel pada 4h** dengan pagar pra-terbang delapan butir dan aset `ohlcv_4h_*`.

**Dihapus di S7:** `analyze_tail.yml` (`07860a7`), `diagnose.yml` (`f4af734`), `diag_datar.yml` (`41ca693`), `retry_failed.yml` (`3a206c6`).

Release **`tier-b-v1`** (id `359778114`) memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`. **Aset 4h ada: 12 berkas, 157.628.619 B**, dan run `30214203863` memakainya.
