# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-26 23:30 WIB (versi 21)

**Tahap sekarang:** S16 — **H-012 tetap DITOLAK, dan sesi ini menemukan cacat mesin yang lebih penting daripada vonis itu.** Diagnostik geometri keluar (run **`30209272338`**) membuktikan kerugian terburuk −21,3131R keluar lewat **`carry`**, bukan `stop`. Pembacaan `engine.py` kemudian membuktikan sebabnya: **stop selalu diisi tepat pada harga stop, bahkan ketika bar MEMBUKA jauh melewatinya.** Mesin karena itu mustahil melahirkan stop lebih buruk dari sekitar 1R ditambah biaya. Perbaikannya sudah terpasang dan hijau: `Konfig.stop_hormati_celah` (`955b419a`, **673 pengujian**), dinyalakan di config (`fb710521`).

**Tahap berikutnya:** `validate.yml` untuk interval **4h** — prasyarat mutlak, dan satu-satunya dimensi yang masih benar-benar bersih. Sesudahnya modul H-013 (ADR-015 Bagian B), lalu `backtest.yml` dibalik **paling akhir**.

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
21. (S13) **Kecurigaan wajib naik, bukan turun, ketika hasilnya menyenangkan.**
22. (S13, ADR-014) **Menuntut kesamaan bit pada agregat pecahan adalah pengujian yang menyala pada perilaku yang benar.** Di dalam satu fungsi murni, kesamaan bit tetap sah dan dipakai `test_tanpa_celah_identik_bit_demi_bit`.
23. (S13, ADR-014) **Pagar yang memastikan masukan identik tidak memastikan masukan sah.**
24. (S13, ADR-014) **Satu simbol dapat mendominasi agregat 438 simbol.**
25. (S13, ADR-014) **Himpunan tertahan habis pada saat pertama kali dilihat.** Periode waktu tertahan kini juga sudah dibelanjakan.
26. (S13, ADR-014) **Cacat yang membalik tanda hasil tidak boleh diperbaiki di dalam hipotesis yang sama.**
27. (S13, ADR-014) **Eksperimen yang tercemar tidak informatif ke arah mana pun.**
28. (S13, ADR-014) **Saringan yang menolak entri juga menolak saat pemilihan.** Terbukti kuantitatif di H-012: hanya **62** entri ditolak pengaman.
29. (S14) **Pra-registrasi wajib diperiksa terhadap apa yang benar-benar dapat dihitung dari laporan.**
30. (S14) **Kriteria utama dihitung dari berkas laporan yang dikomit, bukan dari nilai yang beredar di memori run.**
31. (S15) **Pagar yang menyalin baris dari kode yang dijaganya tidak menjaga apa pun.** Pagar hanya berguna bila dibaca dari **definisi** (`dataclasses.fields`) atau bila ia **memanggil fungsi yang sama** dengan produksi.
32. (S15) **Aritmetika yang hidup di dalam `main` tidak dapat diuji.** Perhitungan yang bisa salah wajib menjadi fungsi tingkat modul; `biaya_bolak_balik_R` dan `harga_stop_terisi` lahir dari aturan ini.
33. (S15) **Setiap langkah workflow wajib `tee` ke `logs/` dan seluruh `logs/` disalin ke `reports/` dengan `if: always()`.**
34. (S15) **Lingkungan pagar wajib memasang dependensi yang sama dengan `tests.yml`.**
35. (S16) **Muatan tulis yang panjang wajib dibaca ulang utuh sebelum dikirim, dan jumlah pengujian dicacah dari muatan yang benar-benar dikirim, bukan dari rencana.** Dua ramalan salah (635 lawan 638, 662 lawan 665) sebabnya identik: mencacah dari niat. Dua commit cacat berturut (`953ce24a` sisa baris percobaan, `2a0f8545` `}` liar yang menjatuhkan **seluruh** koleksi pytest) sebabnya juga identik: menulis berkas panjang satu tarikan tanpa membaca ulang.
36. (S16, ADR-016) **Ramalan yang dijamin benar oleh konstruksi bukan ramalan.** Sebelum menghitung sebuah ramalan lulus, tunjukkan keadaan yang membuatnya gagal. Ramalan 2 ADR-015 benar secara sepele: ia meramalkan tidak ada stop di bawah −1,5R terhadap mesin yang **mustahil** menghasilkannya.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa. Seluruh komputasi berjalan di GitHub Actions.

---

## 3. Fakta terverifikasi

### TEMUAN S16 — mesin buta terhadap celah harga pada jalur stop

**Rantai buktinya, bukan dugaannya:**

1. Gerbang `invarian_risiko` H-012 gagal pada **−21,3131R** terhadap ambang −1,5R.
2. Diagnostik `lux/analisis/geometri_keluar.py` atas `reports/backtest_h012_periode_tertahan.json`, run **`30209272338`**, laporan dikomit **`06841a30`**, log `logs/uji.log` = `22 passed in 0.08s`: perdagangan itu **STGUSDT**, `alasan` keluar **`carry`**, `transaksi_R` 0,0559, `funding_R` 0,4825, pelampauan di luar biaya **20,3131R**, `stop_frac` 2,197%, `jam` **1,0**.
3. Tidak satu pun keluar `stop` di bawah −1,5R; stop terburuk **−1,4966R**; median pelampauan pada jalur stop hanya **0,410263R**.
4. Pembacaan `lux/backtest/engine.py` (blob **`621298a8`**) menjelaskan mengapa: di blok stop/target, `harga = stop if kena_stop else target`. **Harga bar tidak pernah dipakai.** Stop karena itu selalu terisi sempurna.

**Konsekuensi yang wajib ikut dikutip setiap kali angka R lama disebut:**

- Gerbang `invarian_risiko` **praktis tidak punya daya pada jalur stop**. Ia hanya dapat dijatuhkan oleh `umur`, `carry`, dan `akhir_data` — tiga jalur yang mengisi pada `o[t]` atau `c[-1]`, yaitu harga bar sungguhan.
- Seluruh **dua belas** hipotesis dinilai oleh mesin yang **optimistis terhadap risiko celah**.
- Arah biasnya **melawan penolakan**: seandainya celah dihormati, penolakan akan lebih tegas. **Tidak ada vonis yang perlu dibalik.** Tetapi tidak satu pun angka R lama boleh disebut konservatif.
- Jalur `carry` **bukan** pihak yang cacat. −21,3131R adalah angka jujur, dan justru satu-satunya jendela kejujuran yang tersisa.

**Klaim saya yang DITARIK:** "mekanisme stop sendiri sehat" (ditulis sesudah ramalan 2 terbukti). Salah, dan penarikannya resmi di `decisions/ADR-016.md` bagian 2.

### ADR-016 — perbaikan yang memperburuk hasil, dan itu alasan ia dikerjakan

Ditulis **sebelum** sebaris kode perbaikan, commit **`05339d3d`**. Delapan bagian: fakta terverifikasi, penarikan klaim, sebab sebenarnya, batas dugaan, keputusan, lima ramalan beku, tujuh langkah, dua usul aturan.

**Pelaksanaan langkah 1 — commit `955b419a`:**

- `Konfig.stop_hormati_celah: bool = False`, diletakkan **paling akhir**, bawaan **MATI** (aturan 9).
- Fungsi tingkat modul `harga_stop_terisi(stop, buka_bar, arah)`: long `min(stop, buka)`, short `max(stop, buka)` (aturan 32).
- **Target sengaja TIDAK simetris** — ia tetap terisi di harga target walau bar membuka melewatinya, sebab celah yang menguntungkan adalah hadiah atas ketidaktahuan.
- `tests/test_stop_celah.py`, delapan pengujian, angka sengaja bulat (fee 0, slippage 0, ATR 1,0): long celah turun **−1,0R** ketika mati lawan **−5,25R** ketika menyala; short celah naik **−1,0R** lawan **−7,25R**; bar tanpa celah **identik bit demi bit**.

**Pengujian: `673 passed in 2,69s`, kode keluar `0`**, run **`30209850366`**, laporan dikomit **`311d2a86`**, blob **`c9aeb95d`**. **Ramalan 1 ADR-016 BENAR:** 665 pengujian lama lulus **tanpa satu pun disunting** — bukti bahwa medan itu benar-benar bawaan mati.

**Langkah 2 — commit `fb710521`:** `config/lux.yaml` memuat `risiko.stop_hormati_celah: true`. Bawaan mesin tetap mati dan dikunci pengujian; angka config hanya berlaku bila orkestrator hipotesis memasangnya eksplisit, pola yang sama dengan `maks_biaya_masuk_R`. `versi` **tetap 2**; `praregistrasi.py` terverifikasi tidak membaca config sama sekali (blob `98a2806e`). Commit ini **tidak memicu workflow apa pun** karena `tests.yml` memfilter `lux/**` dan `tests/**`, jadi ramalan "673 tetap" **tidak dapat diadili** dan tidak dihitung.

**Hasil H-001b sampai H-012 TIDAK dihitung ulang.** Menghitung ulang vonis dengan mesin berbeda akan mencampur dua mesin di dalam satu papan skor.

### ADR-015 Bagian A — teradili tanpa satu run backtest

Empat ramalan dibekukan di `c6049fa7` dengan ambang −1,5R, lalu diadili dari laporan yang sudah dikomit:

| # | Ramalan | Hasil | Putusan |
|---|---|---|---|
| 1 | perdagangan terburuk keluar lewat `umur`/`carry`/`akhir_data`, bukan `stop` | `carry` | **BENAR** |
| 2 | tidak ada keluar `stop` di bawah −1,5R | tidak ada; terburuk −1,4966R | **BENAR, tetapi sepele** (aturan 36) |
| 3 | porsi bukan-stop di sepuluh terburuk ≥ 0,5 | **0,1000** | **SALAH** |
| 4 | keluar `umur` mendominasi ekor | tak ada `umur` di ekor | **TIDAK DAPAT DINILAI** |

Sepuluh perdagangan terburuk: STGUSDT −21,3131 (`carry`) lalu sembilan keluar `stop` antara −1,4966 dan −1,3865 (TRXUSDT ×4, SUNUSDT ×2, BTCDOMUSDT ×2, PAXGUSDT ×1). Median pelampauan: `carry` **20,313091R**, `stop` **0,410263R** — dua orde besaran, dan itu tepat bentuk yang diperkirakan oleh temuan di atas.

Modul: `lux/analisis/geometri_keluar.py` + `tests/test_geometri_keluar.py`, **22 pengujian**, hijau di `eae7eb3a` (**665 passed**, run `30208582479`). Workflow `geometri.yml` (`51758f36`) berdiri sendiri, memfilter berkasnya sendiri, dan **sudah memuat `git pull --rebase --autostash origin main`** sebelum `git push` — workflow pertama yang membayar utang itu.

### Pelapor Notion — hijau dan kredensialnya terverifikasi

`lux/notion_reporter.py` memakai `urllib.request` sebab runner tanpa `requests`. Kredensial CI **terverifikasi bekerja**, bukan diasumsikan: run asap **`30207584722`** mencatat `baris Notion dibuat, kode 200`, laporan dikomit `5e29432a`, dan barisnya dikonfirmasi dari sisi Notion (page `3a9d5df0-96f9-81df-90a7-f6075d071680`). Secret `NOTION_TOKEN`, variable `NOTION_DB_RUN_RESULTS = 42052623cef043098f13a6f46baf7f3b`.

Satu run merah mendahuluinya (`30207492404`, `1 failed, 641 passed`) karena pengujian menuntut token yang saat itu belum ada; sejak `b4b1963c` pengujian melewatkan diri sendiri tanpa kredensial.

### Papan ramalan jumlah pengujian

| Commit | Ramalan | Nyata | Putusan |
|---|---|---|---|
| `864da2ec` | 635 | **638** | SALAH |
| `3880408f` | 642 | 642 | TEPAT |
| `b4b1963c` | 643 | 643 | TEPAT |
| `eae7eb3a` | 662 | **665** | SALAH |
| `955b419a` | **673** | **673** | TEPAT |

Jejak lengkap: 444 → 462 → 467 → 488 → 494 → 510 → 525 → 542 → 563 → 574 → 578 → 589 → 601 → 615 → 638 → 642 → 643 → 665 → **673**.

### H-012 — DITOLAK (ADR-014 §8)

Run **`30200123505`**, commit **`56a325d2`**, laporan **`b3399b39`**, sidik **`75f9c7ccd65ec30f`**, **1220,6 detik**, 437 simbol dari 438 dinilai, 12 kombinasi, 4.081 jendela.

| Sisi batas | Bulan | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|
| **Tahan (sejak `2026-01`)** | 7 | **22.117** | +922,56 | **+0,041713** |
| Sebelum `2026-01` | 66 | 113.564 | +7.168,96 | +0,063127 |
| Seluruh riwayat | 73 | 135.681 | +8.091,52 | +0,059636 |

Selisih tahan − sebelum **−0,021414R**. 22.117 perdagangan jauh di atas syarat 100, jadi ini kegagalan karena **sinyal**, bukan karena kekurangan data. **0,041713R < 0,05R → GAGAL.**

Lantai semesta membuang **1** simbol: USDCUSDT, median `stop_frac` **1,293930e−04**, biaya masuk **15,46R** — jauh di bawah `BATAS_VOID` 20, jadi semesta yang diuji masih semesta yang dipra-registrasi.

**Sebelas gerbang:** forward_fill 0,0013 lulus · buy_and_hold 0,8401 lulus (unggul 394/437) · **entri_acak GAGAL p 0,06312292358803986** (18/300) · lookahead 0,0000 lulus · **invarian_risiko GAGAL −21,3131R** · funding lulus · overlap lulus · checksum lulus · survivorship 0,1465 lulus · konsentrasi retensi 0,9849 lulus · **funding_ekor GAGAL `funding_maks_R` 0,6601**.

Skor entri acak nyata **0,04661R** — **persis angka H-010**.

**Sebaran (ADR-013):** std 2,22746R, galat baku 0,006047R, CI95 **[0,047784, 0,071489]R** yang **memuat** 0,05. Kuartil: min −21,3131 · Q1 −1,0632 · median −1,0401 · Q3 −0,4209 · maks 12,9076. Biaya: rerata transaksi **0,0359R**, funding −0,0010R, jarak stop 3,507%, **nol** perdagangan berbiaya di atas 1R dari 135.681. Alasan keluar: stop 101.417 · target 21.658 · umur 9.699 · akhir_data 2.479 · carry 428. Jendela positif 2.246/4.081 = 0,55036. Entri ditolak pengaman **62** (PAXGUSDT 42, BTCDOMUSDT 11, MASKUSDT 4, BNBUSDT 3, BTCUSDT 1, TRXUSDT 1).

**Adjudikasi tujuh ramalan ADR-014 §8 — lima tepat, dua salah:** 1 BENAR (1 simbol dibuang, di batas bawah) · 2 BENAR (0,059636, haram jadi bukti) · 3 BENAR (0,041713 → GAGAL) · 4 BENAR (0,063123, dan menjatuhkan) · **5 SALAH** (62 lawan ramalan 500–5.000) · **6 SALAH** (`invarian_risiko` GAGAL, bukan lulus) · 7 BENAR (20,3 menit).

Ramalan 6 adalah pintu masuk seluruh temuan S16. Lantai 0,004 **bekerja besar-besaran** (−470,0612R → −21,3131R, turun 95,5%; biaya 0,12552R → 0,0359R; perdagangan di atas 1R 478 → **0**) tetapi **tidak** membuat gerbangnya lulus — dan sekarang diketahui sebabnya bukan satuan R melainkan mesin yang buta celah.

**Yang haram dilakukan terhadap hasil ini:** mengutip 0,059636R sebagai kelulusan · memilih bulan terbaik dari tabel 73 bulan · menyatakan H-012 "hampir lulus" karena +1,59 galat baku · menurunkan ambang 0,05R · melonggarkan −1,5R.

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

**Kesimpulan struktural:** enam percobaan pada sisi **masuk** menghasilkan nol perbaikan; empat pada sisi **keluar** menghasilkan seluruh kemajuan. Skor entri acak **identik** 0,04661R di H-010 dan H-012 adalah bukti terkuat bahwa keunggulan yang terukur mungkin **seluruhnya** milik geometri keluar. Temuan S16 menambahkan lapisan yang tidak nyaman: sebagian geometri keluar itu ternyata **artefak mesin**, bukan perilaku pasar.

### H-011 — DITOLAK dan TERCEMAR

Run `30194733599`, sidik `8a6efde6d333d8b5`, 838,1 detik. Teruji 40 simbol +0,053028R identik bit-per-bit dengan H-010; tertahan 398 simbol **−0,091519R**; seluruh semesta −0,079078R. **Penyebab tunggal USDCUSDT**: 649 perdagangan, total −18.861,0596R, `stop_frac` terburuk **3,1984e−06**, `transaksi_R` **312,7333** pada satu perdagangan ber-`R` **−470,0612**. Cacat pengukuran, bukan temuan pasar. Tetap ditolak dan tidak direhabilitasi (aturan 27).

### SEMESTA, HIMPUNAN TERTAHAN, TITIK IMPAS

Kriteria lama tidak satu pun menyentuh volatilitas; sejak `81b213b2` config memuat lantai 0,004 dan pagar 0,5R. **Himpunan tertahan HABIS**: hasil per simbol untuk 438 simbol sudah dilihat (H-011) dan tabel 73 bulan sudah dilihat (H-012). Dimensi yang masih bersih hanya **kerangka 4h** dan **pemisahan sinyal dari geometri keluar**.

Titik impas `1/(1+imbalan)`: 1R 0,5000 · 2R 0,3333 · 3R 0,2500 · 4R 0,2000 · 6R 0,1429 · 8R 0,1111. Di H-009, **194 dari 356 jendela (54,5%)** memilih imbalan 4,0 — **versi 16 menulis 226 dan 63,5%; itu salah.** Seretan: H-002 0,04926 · H-009 0,034614 · H-010 0,036220 · H-011 0,125520 (tercemar) · H-012 **0,035900**.

### MESIN BACKTEST

`lux/backtest/`: `engine.py`, `gerbang.py`, `konsentrasi.py`, `funding_ekor.py`, `walk_forward.py`, `run_wf.py`, `run_h002.py`, `run_h003.py`, `runner.py`, `run_keluarga.py`, `run_h007.py`–`run_h012.py`. Analisis: `lux/analisis/{titik_impas,sebaran,periode,geometri_keluar}.py`.

**`engine.Konfig` — nama medan terverifikasi dari sumber:** `fee` (0,0005), `slippage` (0,0005), `atr_periode` (14), `atr_pengali_stop` (2,0), `risiko_per_trade` (0,005), `imbalan_R` (2,0), `modal_awal` (10.000), `izinkan_short` (True), `maks_umur_bar` (0), `maks_carry_R` (0,0), `jendela_carry_hari` (30), `maks_carry_realisasi_R` (0,0), `maks_biaya_masuk_R` (0,0), **`stop_hormati_celah` (False)**. **Tidak ada medan bernama `fee_efektif`** — itu kunci YAML yang dipetakan `muat_konfig_h002` menjadi `fee`. Lima medan terakhir bawaan **MATI** dan dikunci pengujian serta pagar `dataclasses.fields`.

**Urutan pemeriksaan per bar di `engine.jalankan`:** umur → carry realisasi → stop/target → entri (pengaman biaya lalu carry proyeksi) → ekuitas. Umur dan carry dinilai pada pembukaan bar, **sebelum** stop bar itu diuji. `umur` dan `carry` mengisi pada `o[t]`, `akhir_data` pada `c[-1]` — ketiganya jujur terhadap celah. Stop dan target mengisi pada harga stop/target; sejak ADR-016 stop dapat dibuat jujur dengan `stop_hormati_celah`.

Gerbang: `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`, `konsentrasi`, `funding_ekor`. **Tidak dapat dinilai = GAGAL.** `ALASAN_TIDAK_SELESAI = ("umur", "akhir_data", "carry")`.

### DATASET TIER B PUTARAN 2

**14.545.679 bar 1h dan 3.636.733 bar 4h**, 790 simbol, rasio 1h:4h **3,9996**, ~703 MB. Validasi 1h: 0 pelanggaran fatal, 447 simbol layak; ADR-003 memangkas 141, universe layak v2 = **438**, berlantai **437**. Funding 1.982.017 baris, 3 celah sejati, 79,1% positif. Unduhan run: 16 berkas, 559 MB.

### Kapasitas runner dan konektivitas

4 vCPU, 15 GB RAM, 88 GB disk. **Batas 6 jam per job yang mengikat, bukan disk.** H-012 memakai 1220,6 s dari 21.600 s. python 3.12.13, numpy 2.5.1, pytest 9.1.1, pandas 2.2.3, pyarrow 17.0.0, **tanpa scipy**, **tanpa requests**. CDN `data.binance.vision` 200; REST `fapi.binance.com` **451 permanen**.

### Batas alat agen dan solusinya

- Daftar alat GitHub **tidak memuat satu pun fungsi Actions**. Diverifikasi ulang di S16.
- `search_code` **nol hasil di repo ini**. `get_file_contents` menuntut SHA 40 karakter penuh; `list_commits` dipakai memperolehnya.
- `push_files` **mengganti seluruh isi berkas**, jadi baca dulu sebelum menulis ulang — dan baca ulang muatannya sebelum mengirim (aturan 35).
- Filter `paths` per berkas: menyentuh `.github/workflows/backtest.yml` **langsung memulai run**, jadi ia dibalik paling akhir. `tests.yml` memfilter `lux/**` dan `tests/**`, jadi perubahan `config/`, `journal/`, `decisions/`, dan `STATE.md` **tidak** memicunya.
- **Kabar buruk datang dalam 23–32 detik; kabar baik 20 menit.** Komit laporan dapat muncul beberapa detik sesudah pemeriksaan, jadi **diamnya laporan bukan tanda lolos**.
- **Commit laporan tanpa berkas hasil berarti run GAGAL.** Blob laporan yang tidak berubah berarti **belum ditulis**.
- **Modul baru berdiri hijau sendiri lebih dulu.** **Baca modulnya sebelum menulis kode terhadapnya.**

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1–3**, **metrik celah funding**, **circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`).
- **S11:** langkah pra-terbang bisu; `245747ee`.
- **S12:** STATE v11 dan v13 menaikkan kekeliruan menjadi fakta; ditarik v12 dan v14.
- **S13:** "226 dari 356 jendela (63,5%)" padahal **194 (54,5%)**. Saringan nama menandai `BUSDT`/`TUSDT` sebagai stablecoin — **degenerasi wajib dibuktikan lewat `stop_frac`, bukan ejaan nama**.
- **S14:** pra-registrasi menetapkan kriteria yang laporannya tidak mampu menghasilkan.
- **S15:** empat run gagal berturut (`30198306280` bukti hilang · `30198631730` pytest tak terpasang · `30198840830` dan `30198942815` `fee_efektif` ditebak). Aturan 31–34.
- **S16:** dua commit cacat (`953ce24a`, `2a0f8545`) dan dua ramalan cacah salah. Aturan 35. Klaim "mekanisme stop sehat" **ditarik**. Aturan 36.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| **STGUSDT benar-benar bergerak melawan sekitar 46,8% dalam rentang kira-kira satu bar 1h** (aritmetika 21,3131 × 0,02197). Apakah barnya nyata atau cacat dataset **belum terbukti** | bar itu ada di rilis artefak, bukan di repo, dan sandbox tanpa jaringan. Kedua kemungkinan menuntut perbaikan yang sama, jadi pekerjaan tidak menunggu |
| Menyalakan `stop_hormati_celah` akan menjatuhkan `invarian_risiko` lewat **`stop`** sedikitnya sekali | ramalan 4 ADR-016; diadili pada H-013 |
| Ekspektasi R H-013 dengan medan menyala **lebih rendah** daripada dengan medan mati | ramalan 5 ADR-016. Bila ia **membaik**, yang ditemukan adalah cacat tanda, bukan keunggulan |
| Keunggulan H-010 bukan seluruhnya milik geometri keluar | **makin lemah**: skor entri acak nyata **0,04661R identik** di H-010 dan H-012 |
| Keunggulan kelanjutan membesar pada horizon 4h | ADR-015 Bagian B, **setelah** `validate.yml` untuk 4h |
| Integritas 4h sama bersihnya dengan 1h | jalankan `validate.yml` untuk interval 4h |
| Funding sebagai **sinyal** memuat informasi arah | belum pernah diuji |
| Balapan `git push` menelan laporan asap run pertama (`3880408f`) | tetap dugaan; mitigasi `git pull --rebase --autostash` sudah ada di `geometri.yml`, belum di workflow lain |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap universe layak v2 438 |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |

**Difalsifikasi sebelumnya:** saringan rezim tren memperbaiki breakout · retest memperkecil biaya per R · SMC yang dapat dikodekan punya keunggulan · "biaya menjaga risiko memakan ekspektasi" · "ekspektasi bergantung umur simbol" · "kerugian ekor dari bar menganga pada stop" · sinyal `breakout_atr` punya keunggulan yang bertahan di waktu pada 1h (H-012) · lantai 0,004 menutup **seluruh** jalan masuk degenerasi (difalsifikasi sebagian) · "hasil 40 simbol mewakili 438 simbol".

**Terbukti benar:** imbalan lebih besar menaikkan ekspektasi (+28%) · lama pegang membesarkan kerugian ekor · keunggulan bertahan bila penyumbang terbesar dibuang (retensi 0,9849 atas 437 simbol) · **"H-012 gagal", diramalkan sebelum run**.

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 · metrik celah funding putaran 1–4 · seluruh run pilot H-001 termasuk `30170073890` · porsi "101,2%" · nilai gerbang `funding` sebagai bukti funding aman · "226 jendela / 63,5%" (benar 194 / 54,5%) · ekspektasi H-010 0,053028R sebagai bukti sistem layak dagang · **+0,060163R** · **+0,059546R** · **+0,060168R** · **281 dari 398 simbol positif** dan median **+0,06343** · **−0,091519R** tanpa sebabnya · **+0,059636R** sebagai kelulusan · **+2.347,27R bulan 2026-01** atau bulan mana pun sebagai bukti.

---

## 5. Penghalang aktif

Tidak ada. Tidak ada run yang berjalan. Tidak ada yang dibutuhkan dari pengguna.

---

## 6. Tindakan berikutnya

Urutannya mengikuti ADR-016 bagian 7 dan **tidak boleh dibalik**.

1. ~~Medan `Konfig.stop_hormati_celah` + delapan pengujian~~ — **selesai**, `955b419a`, 673 hijau.
2. ~~`config/lux.yaml` menyalakannya + jurnal~~ — **selesai**, `fb710521`.
3. **`validate.yml` untuk interval 4h.** Prasyarat mutlak sebelum H-013, dan satu-satunya kerangka waktu yang masih bersih. Wajib dibaca utuh lebih dulu.
4. **Modul H-013** (ADR-015 Bagian B): empat sel SS/SH/AS/AH, `h=48` bar 4h, ambang **SS − AS ≥ 0,020R**, p ≤ 0,05, ≥300 ulangan, ≥100 trade per sel. Mekanisme diimpor tanpa perubahan dari `run_h010`/`run_h009`. Modul berdiri hijau sendiri lebih dulu (aturan 2). **Dilarang berjalan sebelum butir 3 hijau.**
5. **`backtest.yml` dibalik PALING AKHIR** — menyentuhnya langsung memulai run.
6. Tambahkan `git pull --rebase --autostash origin main` sebelum `git push` pada **semua** workflow lain; baru `geometri.yml` yang memilikinya.
7. **Segarkan `PROMPT_KELANJUTAN.md`** — belum dikerjakan sejak S13, dan kini tertinggal enam aturan (31–36). Wajib **dibaca utuh** lebih dulu; menulis ulang dari ingatan adalah kelas kesalahan "226 jendela".
8. Pemetaan `dari_laporan` pada pelapor Notion terhadap kunci JSON `runner.py`: `gabungan`, `alasan_keluar`, `entri_ditolak_biaya`, `lantai_semesta`, `agregat_periode`, `diagnosa_biaya`, `sebaran`, `jarak_ambang_ekspektasi`, `gerbang`, `jackknife`, `ekor_funding`, `putusan`, `per_simbol`, `detik`, `parameter_run`.
9. Utang teknis: `hasattr`/`__import__` di `test_run_h012.py` · pengujian untuk `biaya_bolak_balik_R` · `pytest` ke `requirements-dev.txt` · docstring `median_stop_frac_bingkai`.
10. **Funding sebagai sinyal.** Belum pernah diuji kandungan informasi arahnya.
11. Perketat `lux/funding.py::gerbang_lulus` (utang ADR-011) · diff Dataset G lama · `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md` · naikkan `versi` config sesudah seluruh pembacanya diperiksa · Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, ≥24 shard · pertimbangkan memangkas `potong_ekor.yml` sesudah Tier A diputuskan.

**Yang DILARANG:** menyatakan sistem siap dagang · mengutip +0,060163R atau +0,059636R sebagai kelulusan · membuang simbol atau memilih bulan sesudah melihat hasil · **menyebut H-012 sebagai "H-010 setelah perbaikan"** · menyebut angka R lama **konservatif** (mesinnya optimistis terhadap celah) · **menghitung ulang H-001b sampai H-012 dengan mesin ADR-016** · menggeser lantai 0,004, pagar 0,5R, `BATAS_VOID` 20, batas `2026-01-01`, atau ambang SS − AS 0,020R · mematok `imbalan_R` ke 8,0 · menurunkan `--ulangan` dari 300 · menaikkan `maks_umur_bar` dari 168 sebagai penyelamatan · membuang simbol merugi · memakai `konsentrasi` atau `funding_ekor` sebagai penyaring simbol · melombakan ambang pengaman · melonggarkan `invarian_risiko` dari −1,5R · **menurunkan maupun menaikkan ambang ekspektasi 0,05R** · menjadikan `stop_hormati_celah` parameter yang dilombakan (ia sakelar kejujuran, bukan ambang).

---

## 7. Pengawasan otonom — DIHENTIKAN

Agen **LUX Gatekeeper** dan **LUX Gatekeeper Reporter** **tidak dipakai lagi.** Keputusan pengguna, 2026-07-26: kreditnya kemungkinan habis sebelum riset selesai.

Keputusan itu sehat melampaui penghematan. Bukti dari sisi Notion (`viewVersionHistory` atas baris asap `3a9d5df0-96f9-81df-90a7-f6075d071680`): agen itu mengadili **setiap** baris secara otomatis dalam sekitar dua menit, termasuk baris yang secara eksplisit menyatakan `bukan_hasil_riset=true`, dan ia memakai `Ditolak` untuk "bukti tidak cukup" padahal `Ditolak` semestinya berarti hipotesis gagal. **Vonis yang salah arti lebih buruk daripada tidak ada vonis**, sebab ia menghentikan pipeline atas alasan yang tidak pernah terjadi.

Akibatnya: kolom `Verdict` di database `LUX — Run Results` menjadi kolom **manusia**. Pelapor Notion tetap dipertahankan sebagai papan hasil yang dapat dibaca dari ponsel; tidak ada perubahan kode yang diperlukan. Pekerjaan "selaraskan instruksi Gatekeeper dari sembilan ke sebelas gerbang" **dibatalkan** dan dihapus dari daftar tindakan.

---

## 8. Peta repo

| Path | Isi |
|---|---|
| `config/lux.yaml` | seluruh parameter yang memengaruhi hasil; lantai `min_median_stop_frac` 0,004, pagar `maks_biaya_masuk_R` 0,5, sakelar `stop_hormati_celah` true; `versi` masih 2 dengan alasan tertulis |
| `lux/binance_vision.py` | klien arsip: listing S3, unduhan, checksum, percent-encoding |
| `lux/universe.py` | universe point-in-time dan klasifikasi jenis kontrak |
| `lux/ingest.py` · `lux/backfill_daily.py` | ingest Tier B dan penutup celah ekor |
| `lux/validate.py` · `lux/validate_run.py` | integritas OHLCV, kelayakan universe, penolak aset `_retry` |
| `lux/funding.py` · `lux/funding_check.py` | ingest funding rate dan metrik kisinya; `gerbang_lulus` masih longgar |
| `lux/funding_model.py` | jadwal funding nyata, penagihan, carry terproyeksi dan terealisasi |
| `lux/costs.py` | model biaya dalam satuan R; **BUKAN jalur kritis** |
| `lux/degenerasi.py` | satuan R yang runtuh: ambang 0,004 dan 0,5R, kasus USDCUSDT, `saring_semesta` |
| `lux/notion_reporter.py` | pelapor baris hasil ke Notion lewat `urllib.request`; kredensial terverifikasi run `30207584722` |
| `lux/diag_datar.py` · `lux/potong_ekor.py` | diagnosis dan pemangkasan ekor datar (ADR-003) |
| `lux/praregistrasi.py` | hipotesis sekali tulis; **tidak membaca `config/lux.yaml`** |
| `lux/analisis/titik_impas.py` | aritmetika titik impas atas laporan yang sudah dikomit |
| `lux/analisis/sebaran.py` | std, galat baku, kuartil. Bukan gerbang. **Galat bakunya taksiran bawah** |
| `lux/analisis/periode.py` | agregat per bulan masuk; batas periode tahan |
| `lux/analisis/geometri_keluar.py` | bedah sepuluh perdagangan terburuk: `R_terlampaui`, `celah_R`, `ringkas`, `adili` |
| `lux/strategi/breakout_atr.py` | sinyal kelanjutan (H-001b, H-002, H-007–H-012) |
| `lux/strategi/reversi_zskor.py` · `rezim_adx.py` · `retest.py` · `smc.py` | H-003 · H-004 · H-005 · H-006 |
| `lux/backtest/engine.py` | mesin eksekusi; urutan per bar umur → carry → stop/target → entri; **lima saringan bawaan MATI**; `harga_stop_terisi` |
| `lux/backtest/gerbang.py` | sembilan gerbang pertama + `NAMA_GERBANG` sebelas nama |
| `lux/backtest/konsentrasi.py` · `funding_ekor.py` | gerbang kesepuluh dan kesebelas |
| `lux/backtest/walk_forward.py` | pemilihan parameter dalam sampel; konfig per kandidat (ADR-007) |
| `lux/backtest/run_wf.py` | orkestrator H-001b — **jangan disunting**; sumber `rincian_R` dan `diagnosa_biaya` |
| `lux/backtest/run_h002.py` · `run_h003.py` | orkestrator beku; `muat_konfig_h002` memetakan YAML `fee_efektif` → medan `fee` |
| `lux/backtest/runner.py` | runner bersama: muat sekali, lantai semesta, sebelas gerbang, jackknife, ekor funding, sebaran, penolakan biaya, agregat periode |
| `lux/backtest/run_keluarga.py` | keluarga ADR-006 (H-004, H-005, H-006) |
| `lux/backtest/run_h007.py` | **sumber grid bersama, HARAM disunting** |
| `lux/backtest/run_h008.py` · `run_h009.py` | dibekukan; `run_h009` sumber `buat_konfig` dan `AMBANG_CARRY_KERAS` |
| `lux/backtest/run_h010.py` | sumber grid imbalan {2,4,6,8} dan `kandidat()` |
| `lux/backtest/run_h011.py` | H-011, semesta penuh; `BATAS_H010 = 40` |
| `lux/backtest/run_h012.py` | H-012: `BATAS_VOID = 20`, `PERIODE_TAHAN_TANGGAL`, tujuh ramalan, `biaya_bolak_balik_R` |
| `tests/` | **673** pengujian tanpa jaringan, wajib hijau sebelum unduhan |
| `reports/` | keluaran mesin tiap run; `backtest_log.md`, `geometri_log.md`, `notion_asap.md` |
| `hipotesis/` | pendaftaran sekali tulis: `H-001b` … `H-012` |
| `decisions/` | ADR-003 … **ADR-016** |
| `journal/` | riwayat per sesi, sampai **`2026-07-26-12.md`** |

**Workflow aktif (12):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`, `notion_asap`, `geometri`. Semuanya idle di belakang filter `paths` dan tidak memakan kuota; tidak ada yang perlu dihapus. `backtest.yml` masih menjalankan `lux.backtest.run_h012` dengan `limit` 0 dan `ulangan` 300 — **jangan disentuh sampai butir 3 dan 4 selesai**. `geometri.yml` satu-satunya yang sudah memakai `git pull --rebase --autostash` sebelum `git push`.

**Dihapus di S7:** `analyze_tail.yml` (`07860a7`), `diagnose.yml` (`f4af734`), `diag_datar.yml` (`41ca693`), `retry_failed.yml` (`3a206c6`).

Release **`tier-b-v1`** memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`. Pola unduh backtest wajib `ohlcv_1h_*.parquet`.
