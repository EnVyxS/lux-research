# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-26 19:05 WIB (versi 20)

**Tahap sekarang:** S15 — **H-012 DITOLAK.** Run **`30200123505`** selesai dalam **1220,6 detik**, berkas hasil ada, sidik **`75f9c7ccd65ec30f`**. Kriteria utama ADR-014 §8: ekspektasi periode tahan sejak `2026-01` = **0,041713R** atas **22.117 perdagangan**, terhadap ambang **0,05R** yang tidak bergerak. **GAGAL, dan dapat dinilai.** Gerbang gagal: `entri_acak` p 0,0631 · `invarian_risiko` −21,3131R · `funding_ekor` lewat `funding_maks_R` 0,6601.

**Tahap berikutnya:** memeriksa **alasan keluar perdagangan terburuk (−21,3131R)** dari `backtest_h012_periode_tertahan.json`, karena `invarian_risiko` yang tetap gagal sesudah lantai 0,004 menunjuk cacat **geometri keluar**, bukan cacat satuan R. Lalu ADR-015: memisahkan sinyal dari geometri keluar.

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
16. (S12) **Proksi yang berkorelasi 0,97 dengan hal lain bukan proksi.**
17. (S12) **Gerbang yang memberi jawaban sama pada dua keadaan bertolak belakang tidak memuat informasi.**
18. (S12) **Angka jumlah yang ditulis tangan hanya boleh ada di satu tempat, yaitu pengujian tripwire.**
19. (S13) **Margin setipis satu satuan resolusi bukan margin.** `entri_acak` H-010 lulus p 0,049505 pada 100 permutasi; pada 300 permutasi mekanisme yang sama memberi **0,0631** dan **gagal**. Dikonfirmasi ulang di H-012: **0,06312292358803986**.
20. (S13) **Ekspektasi yang naik karena penyebutnya menyusut bukan keunggulan yang membesar.**
21. (S13) **Kecurigaan wajib naik, bukan turun, ketika hasilnya menyenangkan.** Di H-012 kedua ramalan yang salah justru **merugikan** hipotesis dan rancangan saya sendiri; itu tanda pra-registrasinya bekerja, bukan tanda boleh lengah.
22. (S13, ADR-014) **Menuntut kesamaan bit pada agregat pecahan adalah pengujian yang menyala pada perilaku yang benar.**
23. (S13, ADR-014) **Pagar yang memastikan masukan identik tidak memastikan masukan sah.**
24. (S13, ADR-014) **Satu simbol dapat mendominasi agregat 438 simbol.**
25. (S13, ADR-014) **Himpunan tertahan habis pada saat pertama kali dilihat.** Ia hanya bisa dibelanjakan sekali. **Periode waktu tertahan kini juga sudah dibelanjakan.**
26. (S13, ADR-014) **Cacat yang membalik tanda hasil tidak boleh diperbaiki di dalam hipotesis yang sama.**
27. (S13, ADR-014) **Eksperimen yang tercemar tidak informatif ke arah mana pun.**
28. (S13, ADR-014) **Saringan yang menolak entri juga menolak saat pemilihan.** Terbukti secara kuantitatif di H-012: hanya **62** entri ditolak pengaman, seluruhnya dari enam simbol yang berubah degenerat di tengah jalan (PAXGUSDT 42, BTCDOMUSDT 11, MASKUSDT 4, BNBUSDT 3, BTCUSDT 1, TRXUSDT 1). USDCUSDT menyumbang **nol** penolakan karena ia dibuang lantai lebih dulu.
29. (S14) **Pra-registrasi wajib diperiksa terhadap apa yang benar-benar dapat dihitung dari laporan.**
30. (S14) **Kriteria utama dihitung dari berkas laporan yang dikomit, bukan dari nilai yang beredar di memori run.** Terbukti bekerja di H-012: `agregat_tahan` membaca blok `agregat_periode` dari JSON yang baru ditulis, sehingga 0,041713R dapat dihitung ulang tangan oleh siapa pun.
31. (S15) **Pagar yang menyalin baris dari kode yang dijaganya tidak menjaga apa pun.** Run `30198942815` lulus kedelapan kelompok pagar lalu mati di `run_h012.main` dengan `AttributeError` yang **identik** dengan yang baru saja diperbaiki di pagar, sebab pagar 4 menyalin baris beserta salah namanya. Pagar hanya berguna bila dibaca dari **definisi** (`dataclasses.fields`) atau bila ia **memanggil fungsi yang sama** dengan yang dipakai produksi.
32. (S15) **Aritmetika yang hidup di dalam `main` tidak dapat diuji.** 615 pengujian hijau tidak menangkap bug di `run_h012.main` karena `main` menuntut dataset 559 MB. Perhitungan yang bisa salah wajib menjadi fungsi tingkat modul; `biaya_bolak_balik_R` lahir dari aturan ini.
33. (S15) **Setiap langkah workflow wajib `tee` ke `logs/` dan seluruh `logs/` disalin ke `reports/` dengan `if: always()`.** Run `30198306280` gagal dan buktinya **hilang** karena hanya `logs/backtest.log` yang disalin — berkas yang belum pernah ada bila kegagalannya mendahului langkah `jalan`. Satu putaran penuh terbuang dan yang dihasilkannya cuma dugaan keliru.
34. (S15) **Lingkungan pagar wajib memasang dependensi yang sama dengan `tests.yml`.** `backtest.yml` memanggil pytest tanpa memasangnya; `requirements.txt` tidak memuat pytest. Bersaudara dengan aturan 24: laporan hijau dari workflow lain **bukan** bukti tentang lingkungan ini.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa. Seluruh komputasi berjalan di GitHub Actions.

---

## 3. Fakta terverifikasi

### H-012 — DITOLAK (ADR-014 §8)

Run **`30200123505`**, commit **`56a325d2`**, laporan **`b3399b39`**, sidik **`75f9c7ccd65ec30f`**, **1220,6 detik**, 437 simbol dari 438 dinilai, 12 kombinasi, 4.081 jendela. Berkas `reports/backtest_h012_periode_tertahan.{md,json}` ada, jadi run sah diadili (aturan 5).

**Kriteria utama, dihitung dari blok `agregat_periode` di laporan yang dikomit:**

| Sisi batas | Bulan | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|
| **Tahan (sejak `2026-01`)** | 7 | **22.117** | +922,56 | **+0,041713** |
| Sebelum `2026-01` | 66 | 113.564 | +7.168,96 | +0,063127 |
| Seluruh riwayat | 73 | 135.681 | +8.091,52 | +0,059636 |

Selisih tahan − sebelum: **−0,021414R**. Periode tahan memuat 22.117 perdagangan, jauh di atas syarat 100, jadi ia **DAPAT dinilai**: ini kegagalan karena sinyal, bukan kegagalan karena kekurangan data. **0,041713R < 0,05R → GAGAL.**

**Lantai semesta bekerja dan tidak membatalkan apa pun.** 438 dinilai, 437 layak, **1 dibuang**: USDCUSDT dengan median `stop_frac` **1,293930e−04** dan biaya masuk **15,46R**. Satu jauh di bawah `BATAS_VOID` 20, jadi semesta yang diuji masih semesta yang dipra-registrasi.

**Sebelas gerbang:**

| Gerbang | Putusan | Nilai | Ambang |
|---|---|---|---|
| forward_fill | lulus | 0,0013 | 0,3 |
| buy_and_hold | lulus | 0,8401 (unggul 394/437) | 0,0 |
| **entri_acak** | **GAGAL** | **p 0,06312292358803986** (18/300) | 0,05 |
| lookahead | lulus | 0,0000 | 0,0 |
| **invarian_risiko** | **GAGAL** | **−21,3131R** | −1,5 |
| funding | lulus | 153.788,1322 | 0,0 |
| overlap | lulus | 0,0000 | 0,0 |
| checksum | lulus | 0,0000 | 0,0 |
| survivorship | lulus | 0,1465 diuji vs 0,1465 universe | 0,5 |
| konsentrasi | lulus | retensi 0,9849 | 0,6 |
| **funding_ekor** | **GAGAL** | `funding_maks_R` **0,6601** | 0,50 |

Skor entri acak nyata **0,04661R** — **persis angka H-010**, jadi geometri keluar menghasilkan hampir seluruh ekspektasi juga di semesta penuh berlantai.

**Konsentrasi sehat, dan itu sungguhan:** 306 untung / 131 rugi dari 437; drop-1 0,05873R (retensi **0,9849**, jauh di atas 0,857845 milik H-010); drop-22 0,04497R; median per simbol +0,06285R; porsi bruto teratas **0,0142** (FLMUSDT), setara **174,3 simbol**. Semesta 437 simbol menghapus keberatan konsentrasi yang menghantui H-009 dan H-010 — tetapi tidak menyelamatkan hipotesisnya.

**Sebaran (ADR-013):** std per perdagangan **2,22746R** (ddof=1, n 135.681), galat baku **0,006047R**, selang 95% **[0,047784, 0,071489]R**, jarak ke ambang **+0,009636R = +1,59 galat baku**. Kuartil: min −21,3131 · Q1 −1,0632 · median −1,0401 · Q3 −0,4209 · maks 12,9076. Selang itu memuat 0,05, jadi bahkan angka seluruh riwayat tidak memisahkan diri dari ambang — dan galat baku ini **taksiran bawah**.

**Biaya sehat, dan ini yang membuat `invarian_risiko` menarik:** rerata biaya transaksi **0,0359R**, rerata funding **−0,0010R**, rerata jarak stop terhadap harga **3,507%**, dan **nol** perdagangan berbiaya di atas 1R dari 135.681. Bandingkan H-011: 0,12552R dan 478 perdagangan di atas 1R. Lantai 0,004 **memang** menutup jalan masuk degenerasi biaya.

Alasan keluar: stop 101.417 · target 21.658 · umur 9.699 · akhir_data 2.479 · carry 428. Jendela positif 2.246/4.081 = 0,55036, di atas 0,5. Parameter terpilih masih dipimpin imbalan 8,0 (655+574+496 = 1.725 dari 4.081 = **42,27%**), sama seperti H-011 (42,25%), jadi optimum tetap di dalam grid.

**Adjudikasi tujuh ramalan ADR-014 §8 — lima tepat, dua salah:**

| # | Ramalan | Hasil | Putusan |
|---|---|---|---|
| 1 | 1–6 simbol dibuang lantai | **1** (USDCUSDT) | **BENAR**, di batas bawah |
| 2 | ekspektasi seluruh riwayat 0,050–0,065 | **0,059636** | **BENAR** (haram jadi bukti) |
| 3 | ekspektasi periode tahan 0,010–0,045 → GAGAL | **0,041713** | **BENAR** |
| 4 | p entri acak 0,01–0,20 | **0,063123** | **BENAR**, dan menjatuhkan |
| 5 | 500–5.000 entri ditolak pengaman | **62** | **SALAH**, 8×–80× terlalu tinggi |
| 6 | `invarian_risiko` LULUS | **GAGAL −21,3131R** | **SALAH** |
| 7 | durasi 10–60 menit | **20,3 menit** | **BENAR** |

**Ramalan 6 adalah temuan terpenting sesi ini, dan ia merugikan rancangan saya sendiri.** Kalimat yang saya bekukan sebelum run berbunyi: bila `invarian_risiko` masih gagal, lantai 0,004 belum menutup jalan masuk degenerasi dan seluruh ADR-014 keliru. Yang terverifikasi sekarang lebih sempit dan lebih tajam:

- Lantai **bekerja besar-besaran**: kerugian terburuk satu perdagangan **−470,0612R → −21,3131R** (turun 95,5%), rerata biaya 0,12552R → 0,0359R, perdagangan berbiaya di atas 1R 478 → **0**.
- Lantai **tidak** membuat gerbangnya lulus: −21,3131R masih 14 kali ambang −1,5R.
- Perdagangan terburuk itu **bukan** gejala satuan R yang runtuh: funding-nya hanya 0,4825R (porsi 0,0226) dan biayanya di bawah 1R. Sesuatu yang lain membayar 20R.

Jadi ADR-014 tidak seluruhnya keliru; ia menutup **satu** jalan masuk dan membuka pandangan ke jalan masuk **kedua** yang belum pernah dinamai. Penyebab pastinya **belum terverifikasi** dan dicatat sebagai asumsi di bagian 4.

**Yang haram dilakukan terhadap hasil ini:** mengutip 0,059636R sebagai kelulusan (seluruh riwayat sudah dipakai memilih segalanya sejak H-001b; ramalan 2 menyatakannya haram sebelum angkanya dilihat) · memilih bulan terbaik dari tabel 73 bulan · menyatakan H-012 "hampir lulus" karena +1,59 galat baku · menurunkan ambang 0,05R · melonggarkan −1,5R.

### Lima run gagal sebelum H-012 berhasil — dan polanya satu

| Run | Durasi | Mati di | Sebab |
|---|---|---|---|
| `30198306280` | 25 s | langkah `uji` | **buktinya hilang**: hanya `logs/backtest.log` disalin, dan berkas itu belum pernah ada |
| `30198631730` | 23 s | langkah `uji` | `No module named pytest`; `requirements.txt` tidak memuatnya |
| `30198840830` | 25 s | pagar 4 | `'Konfig' object has no attribute 'fee_efektif'` |
| `30198942815` | 32 s | `run_h012.main` baris 327 | `fee_efektif` yang **sama**, kali ini di orkestrator; pagar 4 telah menyalinnya |
| `30200123505` | 1220,6 s | — | **SELESAI** |

Keempat kegagalan mati **sebelum** langkah `jalan` menghasilkan komputasi, jadi nol kuota berat terbuang; yang terbuang adalah satu putaran buta yang melahirkan diagnosis keliru. Empat kelas kesalahan, semuanya kini beraturan: nama ditebak alih-alih dibaca dari definisi (aturan 31), aritmetika tersembunyi di `main` (32), log tidak disalin seluruhnya (33), lingkungan pagar berbeda dari `tests.yml` (34).

**Diagnosis saya yang salah dan sudah ditarik:** saya menuduh tiga baris pagar penebak konstruktor sebagai penyebab `30198306280`, padahal pagar itu tidak pernah dieksekusi — run mati di langkah `uji`. Alasan saya menyingkirkan `uji` juga cacat: saya bersandar pada `reports/tests.md` yang lahir dari `tests.yml`, lingkungan yang berbeda. Itu tepat kelas kesalahan aturan 24.

### Enam commit ADR-014 dan dua commit perbaikan CI

| Commit | Isi | Pengujian |
|---|---|---|
| `bfb5f2d9` | `runner.py`: lantai semesta, `entri_ditolak_biaya`, simbol dibuang + `median_stop_frac` + `tests/test_runner_lantai.py` | 578 → **589** |
| `81b213b2` | `config/lux.yaml`: `min_median_stop_frac: 0.004`, `maks_biaya_masuk_R: 0.5` | 589 |
| `0684bca0` | `lux/analisis/periode.py` + pengujiannya, hijau sendiri lebih dulu | 589 → **601** |
| `f6efbd7a` | sambungan `periode` ke `runner.jalankan_spek` | **601** |
| `884d6c8e` | `lux/backtest/run_h012.py` + `tests/test_run_h012.py` | 601 → **615** |
| `f7da5cf3` | `backtest.yml` dibalik ke H-012 — memicu run | — |
| `7912758f` | instrumentasi log: `tee` tiap langkah, salin lima log `if: always()` | 615 |
| `07c8541e` | pasang `pytest` di `backtest.yml` | 615 |
| `1637d035` | pagar 4 memakai `Konfig.fee` | 615 |
| `56a325d2` | `run_h012.biaya_bolak_balik_R`, pagar 4 memanggilnya alih-alih menyalinnya — memicu run yang berhasil | **615** |

**Pengujian terverifikasi:** 615 lulus, kode keluar 0, di `tests.yml` (run `30198241082`) **dan** di dalam `backtest.yml` sendiri (2,47–2,75 detik pada empat run terakhir). Ketiga ramalan jumlah pengujian S14 tepat (589, 601, 615) — tepat kesepuluh berturut-turut.

**Yang dipatok sebelum run dan tidak bergerak sesudahnya:** lantai 0,004 · pengaman 0,5R · `PERIODE_TAHAN_MS` 1767225600000 (`2026-01`, titik batas milik periode tahan) · `BATAS_VOID` 20 · kriteria 0,05R / 100 trade / p ≤ 0,05 / ≥ 0,5 · `--ulangan` 300 · grid identik H-010/H-009. Aritmetika lantai–pengaman **dihitung**, bukan dipercaya sebagai label: `2×(fee + slippage)` = 0,002 dari harga = tepat 0,5R pada jarak stop 0,004, dan sejak `56a325d2` pagar dan orkestrator memakai **fungsi yang sama** untuk menghitungnya.

**Batas kejujuran yang wajib ikut dikutip.** Periode tahan **tidak** sebersih himpunan simbol tertahan sebelum H-011: riwayat yang sudah dilihat memuat periode itu di dalam agregatnya, dan yang belum pernah dilihat hanyalah **angkanya secara terpisah**. Perdagangan yang dibuka sesaat sebelum batas dapat ditutup sesudahnya; rembesan itu terbatas `maks_umur_bar` 168 bar = tujuh hari, arahnya tidak diketahui.

**Utang teknis yang masih terbuka:**

1. `runner.median_stop_frac_bingkai` memakai ATR bar `t` dibagi **close** bar `t`; mesin memakai ATR bar `t−1` terhadap **open** bar `t` ber-slippage. Selisih per mil terhadap kriteria yang berselisih tiga orde besaran, jadi ia tidak dapat memindahkan satu simbol pun melewati lantai. Tertulis di docstring.
2. `tests/test_run_h012.py::test_kriteria_tidak_bergerak` memakai satu baris `hasattr` + `__import__` yang rapuh secara gaya. Hijau, tetapi wajib dirapikan menjadi impor `engine.Konfig` biasa.
3. `pytest` belum masuk `requirements.txt` maupun `requirements-dev.txt`; aturan 34 masih dijaga tangan.

### H-011 — DITOLAK, dan yang terbongkar adalah cacat semesta (ADR-014)

Run **`30194733599`**, laporan **`2bb7b963`**, sidik **`8a6efde6d333d8b5`**, **838,1 detik**, 438 simbol.

| Kelompok | n simbol | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|
| Teruji (40 pertama alfabet) | 40 | 11.734 | +622,2348 | **+0,053028** |
| **Tertahan (398)** | 398 | 124.603 | **−11.403,5584** | **−0,091519** |
| Seluruh semesta | 438 | 136.337 | −10.781,3236 | −0,079078 |

Baris teruji **identik bit-per-bit** dengan H-010. **Penyebab tunggal:** `USDCUSDT` — 649 perdagangan, total_R **−18.861,0596**, ekspektasi **−29,06173**, `stop_frac` terburuk **3,1984170825288993e−06**, `transaksi_R` **312,7333** pada satu perdagangan ber-`R` **−470,0612**. Cacat pengukuran, bukan temuan pasar. Gerbang gagal: `entri_acak` 0,0631 · `invarian_risiko` −470,0612R · `konsentrasi` tak dapat dinilai · `funding_ekor` `funding_maks_R` 2,3900.

H-012 kini memberi pembanding yang bersih untuk klaim itu: dengan simbol yang sama dibuang oleh **kriteria seragam yang dipra-registrasi**, ekspektasi 437 simbol menjadi **+0,059636R**. Itu **bukan** kelulusan dan bukan rehabilitasi H-011 — H-011 tetap tercemar dan tetap ditolak (aturan 27) — tetapi ia memisahkan "semesta penuh rugi" dari "satu simbol merusak satuan ukurannya".

### SEMESTA LAYAK v2 — CACAT LAMA, KINI BERLANTAI

Kriteria lama (`min_bar_1h` 8760, `min_median_quote_volume_harian` 1.000.000, `maks_rasio_bar_datar` 0,30) **tidak satu pun menyentuh volatilitas**; USDCUSDT lolos ketiganya dan saringan volume justru menariknya masuk. Sejak `81b213b2` berkas memuat `universe.min_median_stop_frac: 0.004` dan `risiko.maks_biaya_masuk_R: 0.5`. Nomor `versi` **tetap 2**, sengaja, karena belum seluruh pembacanya diperiksa. Terverifikasi: `muat_konfig_h002` memakai `yaml.safe_load` lalu hanya mengambil kunci yang disebutnya, jadi penambahan ini tidak menjatuhkan pembacaan lama — dan kini terbukti di run nyata.

### HIMPUNAN TERTAHAN — HABIS, DAN PERIODE TAHAN JUGA

Hasil per simbol untuk seluruh 438 simbol pada 1h sudah dilihat (H-011), dan tabel 73 bulan sudah dilihat (H-012). Dimensi yang masih bersih hanya **kerangka 4h** dan **pemisahan sinyal dari geometri keluar**.

### H-010 — LULUS pada 40 simbol dengan empat keberatan; TIDAK DIREHABILITASI

Run **`30193898133`**, sidik **`14b2f3bfa8a754b5`**, 117,5 detik, 40 simbol. Kriteria: ekspektasi **0,053028** · 11.734 trade · p **0,049505** · jendela positif **0,528090**.

**Empat keberatan, dan tiga di antaranya kini diperkuat H-012:** (1) p 0,049505 = (4+1)/(100+1), dan pada 300 permutasi mekanisme yang sama memberi **0,0631** di H-010, **0,0631** di H-011, dan **0,063123** di H-012 — tiga kali, tiga semesta, angka yang sama; (2) skor nyata entri acak **0,10781R → 0,04661R (−56,8%)**, dan H-012 mengulang **0,04661R** persis, jadi tafsiran "keunggulan mungkin seluruhnya milik geometri keluar" makin sulit dihindari; (3) jendela positif 0,528090; (4) semesta yang kini diketahui cacat — keberatan ini **selesai** dijawab H-012.

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
| H-011 | mekanisme H-010 atas 438 simbol | −0,079078 | `entri_acak`, `invarian_risiko`, `konsentrasi`, `funding_ekor` | **DITOLAK, dan TERCEMAR** |
| **H-012** | semesta berlantai 0,004 + pagar 0,5R, dinilai sejak 2026-01-01 | **0,041713 (periode tahan)** | `entri_acak` 0,0631 · `invarian_risiko` −21,3131 · `funding_ekor` 0,6601 | **DITOLAK** |

Sidik: H-001b `e458f4c82abf6735` · H-002 `16fb57692a6f0888` · H-003 `3a1cdc867f61bf67` · H-004 `98d6a5e15b2cc08b` · H-005 `9c4b6324e79569eb` · H-006 `e503a9a833182b25` · H-007 `7f5e7aeeaa29284b` · H-008 `dfeeea04fd4107f6` · H-009 `eac6c83305bd1069` · H-010 `14b2f3bfa8a754b5` · H-011 `8a6efde6d333d8b5` · **H-012 `75f9c7ccd65ec30f`**.

**Sebelas dari dua belas ditolak.** Yang satu itu lulus pada 100 permutasi dan gagal pada 300.

**Kesimpulan struktural, diperkuat H-012:** enam percobaan pada sisi **masuk** menghasilkan nol perbaikan; empat pada sisi **keluar** menghasilkan seluruh kemajuan yang pernah ada. Skor entri acak yang **identik** (0,04661R) di H-010 dan H-012 adalah bukti terkuat sejauh ini bahwa keunggulan yang terukur mungkin **seluruhnya** milik geometri keluar, bukan milik sinyal kelanjutan.

### Titik impas

`1/(1+imbalan)`: 1R 0,5000 · 2R 0,3333 · 3R 0,2500 · 4R 0,2000 · 6R 0,1429 · 8R 0,1111. Di H-009, **194 dari 356 jendela (54,5%)** memilih imbalan 4,0. **Versi 16 menulis 226 dan 63,5%; itu salah.**

| Hipotesis | Laju target | Bersih tercatat | Seretan |
|---|---|---|---|
| H-002 | 0,36028 | +0,03159 | 0,04926 |
| H-009 | 0,27544 | +0,041359 | 0,034614 |
| H-010 | 0,15672 | +0,053028 | 0,036220 |
| H-011 | 0,15879 | −0,079078 | 0,125520 (tercemar) |
| **H-012** | **0,15963** | **+0,059636** | **0,035900** |

Seretan H-012 (0,0359R) hampir sama dengan H-010 (0,03622R) dan sepertiga H-011 — lantai memulihkan aritmetika biaya sepenuhnya.

### MESIN BACKTEST

`lux/backtest/`: `engine.py`, `gerbang.py`, `konsentrasi.py`, `funding_ekor.py`, `walk_forward.py`, `run_wf.py`, `run_h002.py`, `run_h003.py`, `runner.py`, `run_keluarga.py`, `run_h007.py`–`run_h012.py`. Analisis: `lux/analisis/{titik_impas,sebaran,periode}.py`. Degenerasi: `lux/degenerasi.py`.

**`engine.Konfig` — nama medan terverifikasi dari sumber:** `fee` (0,0005), `slippage` (0,0005), `atr_periode` (14), `atr_pengali_stop` (2,0), `risiko_per_trade` (0,005), `imbalan_R` (2,0), `modal_awal` (10.000), `izinkan_short` (True), `maks_umur_bar` (0), `maks_carry_R` (0,0), `jendela_carry_hari` (30), `maks_carry_realisasi_R` (0,0), `maks_biaya_masuk_R` (0,0). **Tidak ada medan bernama `fee_efektif`** — itu kunci YAML yang dipetakan `muat_konfig_h002` menjadi `fee`. Empat medan terakhir bawaan **MATI** dan dikunci pengujian serta pagar `dataclasses.fields`.

**`run_h012.biaya_bolak_balik_R(konfig)`** (`56a325d2`): satu-satunya tempat aritmetika `2×(fee + slippage)` hidup; memvalidasi keberadaan medan lewat `dataclasses.fields` dan dipanggil **baik** oleh `main` **maupun** oleh pagar 4 `backtest.yml`. Lahir dari aturan 31 dan 32.

**Urutan pemeriksaan per bar di `engine.jalankan`:** umur → carry realisasi → stop/target → entri (pengaman biaya lalu carry proyeksi) → ekuitas. **Umur dan carry dinilai pada pembukaan bar, sebelum stop bar itu diuji** — disengaja dan didokumentasikan, supaya posisi tidak mendapat satu bar gratis untuk menyentuh target. Konsekuensinya belum pernah diukur dan kini menjadi tersangka utama `invarian_risiko`.

**Laporan memuat** (sejak `bfb5f2d9` dan `f6efbd7a`): `entri_ditolak_biaya`, `entri_ditolak_biaya_per_simbol`, `lantai_semesta` beserta tabel simbol dibuang, `agregat_periode` per bulan masuk, `parameter_run.maks_biaya_masuk_R`, `parameter_run.min_median_stop_frac`. Penolakan pengaman **tidak** dijumlahkan ke `alasan_keluar`.

Gerbang: `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`, `konsentrasi`, `funding_ekor`. **Tidak dapat dinilai = GAGAL.** `ALASAN_TIDAK_SELESAI = ("umur", "akhir_data", "carry")`.

### DATASET TIER B PUTARAN 2

**14.545.679 bar 1h dan 3.636.733 bar 4h**, 790 simbol, rasio 1h:4h **3,9996**, ~703 MB. Validasi 1h: 0 pelanggaran fatal, 447 simbol layak; ADR-003 memangkas 141 simbol berekor datar, universe layak v2 = **438**, dan sejak H-012 **437** yang berlantai. Funding: 1.982.017 baris, 447 simbol, 3 celah sejati, 79,1% positif, jitter maks 47 ms. Unduhan run: **16 berkas, 559 MB** (delapan `ohlcv_1h_shard`, empat `tail_shard`, empat `funding_shard`).

### Pengujian — `reports/tests.md`

**615 hijau**, kode keluar 0, tanpa jaringan. Jejak: 444 → 462 → 467 → 488 → 494 → 510 → 525 → 542 → 563 → 574 → 578 → **589** → **601** → **615**. **Sepuluh ramalan jumlah pengujian berturut-turut tepat.** Tidak satu pun menjalankan `run_h012.main`, dan itu sebabnya bug `fee_efektif` lolos (aturan 32).

### Kapasitas runner dan konektivitas

4 vCPU, 15 GB RAM, 88 GB disk. **Batas 6 jam per job yang mengikat, bukan disk.** H-012: 437 simbol × 12 kombinasi × 300 ulangan = **1220,6 detik**, jadi masih ada ruang 17 kali lipat. python 3.12.13, numpy 2.5.1, pytest 9.1.1, **tanpa scipy**. CDN `data.binance.vision` 200; REST `fapi.binance.com` **451 permanen**.

### Batas alat agen dan solusinya

- Daftar alat GitHub **tidak memuat satu pun fungsi Actions**. Diverifikasi ulang di S14.
- `search_code` **nol hasil di repo ini**. `get_file_contents` menuntut SHA 40 karakter penuh; `list_commits` dipakai memperolehnya.
- `push_files` **mengganti seluruh isi berkas**, jadi baca dulu sebelum menulis ulang.
- Filter `paths` per berkas: menyentuh `.github/workflows/backtest.yml` **langsung memulai run**, jadi ia dibalik paling akhir. `tests.yml` memfilter `lux/**` dan `tests/**`.
- **Kabar buruk datang dalam 23–32 detik; kabar baik 20 menit.** Komit laporan dapat muncul beberapa detik sesudah pemeriksaan, jadi **diamnya laporan bukan tanda lolos** — kesalahan yang saya buat di S15 dan sudah ditarik.
- **Commit laporan tanpa berkas hasil berarti run GAGAL.** Blob laporan yang tidak berubah berarti **belum ditulis**.
- **Modul baru berdiri hijau sendiri lebih dulu.** **Baca modulnya sebelum menulis kode terhadapnya.**
- **Tulisan yang hanya menyentuh dokumen** (`STATE.md`, `PROMPT_KELANJUTAN.md`, `journal/`, `decisions/`) tidak memicu workflow apa pun.

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1–3**, **metrik celah funding**, **circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`).
- **S11:** langkah pra-terbang bisu; `245747ee`.
- **S12:** STATE v11 dan v13 menaikkan kekeliruan menjadi fakta; ditarik v12 dan v14. `test_gerbang_kesepuluh.py` memakai literal terlarang; `114b0d7e`.
- **S13:** "226 dari 356 jendela (63,5%)" padahal **194 (54,5%)**. `test_sebaran.py` menuntut kesamaan bit; `2650ae32`. Saringan nama menandai `BUSDT`/`TUSDT` sebagai stablecoin — **degenerasi wajib dibuktikan lewat `stop_frac`, bukan ejaan nama**.
- **S14:** pra-registrasi menetapkan kriteria yang laporannya tidak mampu menghasilkan; ditutup dua commit sebelum satu angka dilihat.
- **S15:** empat run gagal berturut karena nama ditebak, aritmetika tersembunyi di `main`, log tak disalin, dan lingkungan pagar berbeda. Aturan 31–34. Diagnosis pertama saya atas `30198306280` **salah** dan ditarik.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| **Kerugian −21,3131R lahir dari keluar `umur`/`carry` pada pembukaan bar yang menganga melewati stop** — dugaan, bukan fakta. Dasarnya: biaya per perdagangan sehat (0,0359R, nol di atas 1R), funding-nya 0,4825R, dan urutan mesin menilai umur/carry **sebelum** stop | baca `alasan_keluar`, `harga_masuk`, `harga_keluar`, dan `jarak_stop` perdagangan terburuk dari `backtest_h012_periode_tertahan.json`; bila benar, ini cacat **geometri keluar**, bukan cacat satuan R |
| Lantai 0,004 menutup **seluruh** jalan masuk degenerasi | **DIFALSIFIKASI SEBAGIAN.** Ia memotong −470,06R → −21,31R dan memulihkan aritmetika biaya, tetapi `invarian_risiko` tetap gagal 14× ambang |
| Keunggulan H-010 bukan seluruhnya milik geometri keluar | **makin lemah**: skor entri acak nyata **0,04661R identik** di H-010 dan H-012. Butuh uji yang memisahkan sinyal dari geometri keluar; belum dirancang, wajib punya ADR sendiri |
| Sinyal kelanjutan `breakout_atr` punya keunggulan yang bertahan di waktu pada 1h | **DIFALSIFIKASI** oleh H-012: 0,041713R pada periode tahan, p 0,063123 |
| Keunggulan kelanjutan membesar pada horizon 4h | jalankan hipotesis 4h **setelah** `validate.yml` untuk 4h |
| Funding sebagai **sinyal** memuat informasi arah | belum pernah diuji |
| Integritas 4h sama bersihnya dengan 1h | jalankan `validate.yml` untuk interval 4h |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap universe layak v2 438 |
| Throughput cukup untuk Tier A dalam 6 jam per shard | H-012 memakai 1220,6 s dari 21.600 s tersedia; ukur ulang dengan ≥24 shard |

**Diselesaikan sebelumnya:** saringan rezim tren memperbaiki breakout (**salah**) · retest memperkecil biaya per R (**salah**) · SMC yang dapat dikodekan punya keunggulan (**salah**) · imbalan lebih besar menaikkan ekspektasi (**benar**, +28%) · lama pegang membesarkan kerugian ekor (**benar**) · pengaman carry dipatok membuat `invarian_risiko` lulus (**benar** pada 40 simbol) · "biaya menjaga risiko memakan ekspektasi" (**salah**) · keunggulan bertahan bila penyumbang terbesar dibuang (**benar**, dan H-012 memperkuatnya: retensi 0,9849 atas 437 simbol) · "ekspektasi bergantung umur simbol" (**salah**) · "kerugian ekor dari bar menganga" dan "dari stop rapat" (**salah** — tetapi lihat asumsi pertama di atas: bar menganga kembali menjadi tersangka pada **keluar umur**, bukan pada stop) · "funding bukan penyebab kerugian ekor" (**ditarik**) · "laba terkonsentrasi pada sepuluh simbol" (**ditarik**) · "gerbang funding memantau biaya funding" (**salah**) · "optimum imbalan di luar grid H-007" (**benar sebagian**) · "target lebih jauh membesarkan porsi funding ekor" (**salah**) · "H-010 akan menjadi penolakan kesepuluh" (**salah**) · **"H-012 gagal" (benar, dan diramalkan sebelum run)**.

**"Hasil 40 simbol pertama mewakili 438 simbol" — kini TERJAWAB, dan jawabannya tidak.** Pada semesta berlantai 437 simbol, ekspektasi seluruh riwayat 0,059636R sedangkan periode tahan 0,041713R; `invarian_risiko` dan `funding_ekor` yang lulus pada 40 simbol **gagal** pada 437. H-011 tidak dapat menjawabnya karena tercemar; H-012 menjawabnya dengan kriteria seragam yang dipra-registrasi.

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 · metrik celah funding putaran 1–4 · seluruh run pilot H-001 termasuk `30170073890` · porsi "101,2%" · selisih muda-lawan-tua · nilai gerbang `funding` sebagai bukti funding aman · "226 jendela / 63,5%" (benar 194 / 54,5%) · ekspektasi H-010 0,053028R sebagai bukti sistem layak dagang · **+0,060163R** dan **+0,059546R** (penyubsetan pasca-hasil, ADR-013 §8) · **+0,060168R** · **281 dari 398 simbol positif** dan median **+0,06343** · **−0,091519R** sah hanya bersama sebabnya · **+0,059636R milik H-012** sebagai kelulusan atau bukti keunggulan — seluruh riwayat sudah dipakai memilih segalanya sejak H-001b, dan ramalan 2 menyatakannya haram **sebelum** angkanya dilihat · **+2.347,27R bulan 2026-01** atau bulan mana pun sebagai bukti.

---

## 5. Penghalang aktif

Tidak ada. H-012 selesai dan divonis; tidak ada run yang berjalan.

Dibutuhkan dari pengguna, belum memblokir: **token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`.

---

## 6. Tindakan berikutnya

1. **Bedah perdagangan terburuk H-012.** Baca `backtest_h012_periode_tertahan.json` dan ambil `alasan_keluar` beserta harga perdagangan ber-`R` −21,3131. Ini pekerjaan sandbox tanpa jaringan dan tanpa run. Bila alasannya `umur`, `carry`, atau `akhir_data`, maka `invarian_risiko` selama dua belas hipotesis sedang melaporkan **cacat geometri keluar**, bukan cacat satuan R — dan itu menjelaskan mengapa ia gagal di H-001b (−2,5853), H-005, H-006, H-007 (−1,9769), dan H-008 dengan angka yang jauh lebih kecil daripada H-011.

2. **ADR-015: memisahkan sinyal dari geometri keluar.** Skor entri acak nyata **identik 0,04661R** di H-010 dan H-012, sedangkan skor sinyal nyata jatuh 56,8% ketika entri diacak. Ini **pertanyaan paling penting yang tersisa**, dan hasil butir 1 kemungkinan menjadi masukannya. Rancangannya belum ada.

3. **Rapikan tiga utang teknis:** `hasattr`/`__import__` di `test_run_h012.py`, `pytest` ke `requirements-dev.txt`, docstring `median_stop_frac_bingkai`.

4. **Segarkan `PROMPT_KELANJUTAN.md`** — belum dikerjakan sejak S13. Wajib **dibaca utuh lebih dulu**; `push_files` mengganti seluruh isinya, dan menulis ulang 34 aturan dari ingatan adalah kelas kesalahan "226 jendela".

5. **Horizon 4h.** Prasyarat mutlak `validate.yml` untuk 4h. Satu-satunya kerangka waktu yang masih benar-benar bersih.

6. **Funding sebagai sinyal.** Belum pernah diuji kandungan informasi arahnya.

**Yang DILARANG:** menyatakan sistem siap dagang · mengutip +0,060163R atau +0,059636R sebagai kelulusan · membuang simbol atau memilih bulan sesudah melihat hasil · **menyebut H-012 sebagai "H-010 setelah perbaikan"** · menggeser lantai 0,004, pagar 0,5R, `BATAS_VOID` 20, atau batas `2026-01-01` · mematok `imbalan_R` ke 8,0 · menurunkan `--ulangan` dari 300 · menaikkan `maks_umur_bar` dari 168 **sebagai penyelamatan** (mengubahnya sebagai hipotesis baru ber-ADR boleh) · membuang simbol merugi · memakai `konsentrasi` atau `funding_ekor` sebagai penyaring simbol · saringan berbasis umur simbol · melombakan ambang pengaman · menghitung ulang hipotesis yang sudah divonis · melonggarkan `invarian_risiko` dari −1,5R · melonggarkan ambang ADR-011 · **menurunkan maupun menaikkan ambang ekspektasi 0,05R**.

Sisanya, tidak memblokir:

7. Perketat `lux/funding.py::gerbang_lulus`. Utang ADR-011.
8. Diff terhadap Dataset G lama (528 simbol).
9. `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md`; salin ADR-001 dan ADR-002 ke `decisions/`.
10. Pelapor Notion (`NOTION_TOKEN`); instruksi Gatekeeper masih menyebut sembilan gerbang.
11. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, dengan ≥24 shard.
12. Naikkan `versi` di `config/lux.yaml` sesudah seluruh pembacanya diperiksa.
13. Pertimbangkan memangkas `potong_ekor.yml`: tugas ADR-003 tuntas dan hasilnya beku di `universe_layak_v2.json`. Ditahan sampai Tier A diputuskan; workflow idle tidak memakan kuota karena filter `paths`.

---

## 7. Pengawasan otonom

Agen **LUX Gatekeeper** aktif di Notion. Terpicu saat runner membuat baris di database Run Results, menilai hasil terhadap gerbang mutu. Sudah diuji dengan baris sintetis bercacat dan menolak dengan benar. **Verdict Ditolak menghentikan pipeline.** Instruksinya masih menyebut sembilan gerbang dan perlu disesuaikan menjadi sebelas bila pelapor Notion diaktifkan.

---

## 8. Peta repo

| Path | Isi |
|---|---|
| `config/lux.yaml` | seluruh parameter yang memengaruhi hasil; memuat lantai `min_median_stop_frac` 0,004 dan pagar `maks_biaya_masuk_R` 0,5; `versi` masih 2 dengan alasan tertulis |
| `lux/binance_vision.py` | klien arsip: listing S3, unduhan, checksum, percent-encoding |
| `lux/universe.py` | universe point-in-time dan klasifikasi jenis kontrak |
| `lux/ingest.py` · `lux/backfill_daily.py` | ingest Tier B dan penutup celah ekor |
| `lux/validate.py` · `lux/validate_run.py` | integritas OHLCV, kelayakan universe, penolak aset `_retry` |
| `lux/funding.py` · `lux/funding_check.py` | ingest funding rate dan metrik kisinya; `gerbang_lulus` masih terlalu longgar |
| `lux/funding_model.py` | jadwal funding nyata, penagihan, carry terproyeksi dan terealisasi |
| `lux/costs.py` | model biaya dalam satuan R; aproksimasi interval tetap, **BUKAN jalur kritis** |
| `lux/degenerasi.py` | satuan R yang runtuh: ambang 0,004 dan 0,5R, kasus USDCUSDT, `saring_semesta` |
| `lux/diag_datar.py` · `lux/potong_ekor.py` | diagnosis dan pemangkasan ekor datar (ADR-003) |
| `lux/praregistrasi.py` | hipotesis sekali tulis dan penilaian terhadap kriteria |
| `lux/analisis/titik_impas.py` | aritmetika titik impas atas laporan yang sudah dikomit |
| `lux/analisis/sebaran.py` | std, galat baku, kuartil, jarak ambang. Bukan gerbang. **Galat bakunya taksiran bawah** |
| `lux/analisis/periode.py` | agregat per bulan masuk; batas periode tahan; kepemilikan menurut waktu masuk |
| `lux/strategi/breakout_atr.py` | sinyal kelanjutan (H-001b, H-002, H-007–H-012) |
| `lux/strategi/reversi_zskor.py` · `rezim_adx.py` · `retest.py` · `smc.py` | H-003 · H-004 · H-005 · H-006 |
| `lux/backtest/engine.py` | mesin eksekusi; **urutan per bar umur → carry → stop/target → entri**; empat saringan bawaan MATI |
| `lux/backtest/gerbang.py` | sembilan gerbang pertama + `NAMA_GERBANG` sebelas nama |
| `lux/backtest/konsentrasi.py` · `funding_ekor.py` | gerbang kesepuluh dan kesebelas |
| `lux/backtest/walk_forward.py` | pemilihan parameter dalam sampel; konfig per kandidat (ADR-007) |
| `lux/backtest/run_wf.py` | orkestrator H-001b — **jangan disunting** |
| `lux/backtest/run_h002.py` · `run_h003.py` | orkestrator beku; `muat_konfig_h002` memetakan YAML `fee_efektif` → medan `fee` |
| `lux/backtest/runner.py` | runner bersama: muat sekali, lantai semesta, sebelas gerbang, jackknife, ekor funding, sebaran, penolakan biaya, agregat periode |
| `lux/backtest/run_keluarga.py` | keluarga ADR-006 (H-004, H-005, H-006) |
| `lux/backtest/run_h007.py` | **sumber grid bersama, HARAM disunting** |
| `lux/backtest/run_h008.py` · `run_h009.py` | dibekukan; `run_h009` sumber `buat_konfig` dan `AMBANG_CARRY_KERAS` |
| `lux/backtest/run_h010.py` | sumber grid imbalan {2,4,6,8} dan `kandidat()` |
| `lux/backtest/run_h011.py` | H-011, semesta penuh; `BATAS_H010 = 40` |
| `lux/backtest/run_h012.py` | H-012: `BATAS_VOID = 20`, `PERIODE_TAHAN_TANGGAL`, tujuh ramalan, **`biaya_bolak_balik_R`** |
| `tests/` | **615** pengujian tanpa jaringan, wajib hijau sebelum unduhan |
| `reports/` | keluaran mesin tiap run, termasuk `backtest_log.md` berisi lima log lengkap |
| `hipotesis/` | pendaftaran sekali tulis: `H-001b` … **`H-012`** |
| `decisions/` | ADR-003 … **ADR-014** |
| `journal/` | riwayat per sesi, sampai **`2026-07-26-11.md`** |

**Workflow aktif (10):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`. Tidak ada yang perlu dihapus: semuanya idle di belakang filter `paths` dan tidak memakan kuota. `backtest.yml` menjalankan `lux.backtest.run_h012` dengan `limit` 0 dan `ulangan` 300; langkah `impor`-nya memuat delapan kelompok pagar dan pagar 4 **memanggil** `run_h012.biaya_bolak_balik_R` alih-alih menyalinnya (aturan 31); setiap langkah `tee` ke `logs/` dan seluruhnya disalin ke `reports/backtest_log.md` dengan `if: always()` (aturan 33).

**Dihapus di S7:** `analyze_tail.yml` (`07860a7`), `diagnose.yml` (`f4af734`), `diag_datar.yml` (`41ca693`), `retry_failed.yml` (`3a206c6`).

Release **`tier-b-v1`** memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`. Pola unduh backtest wajib `ohlcv_1h_*.parquet`.
