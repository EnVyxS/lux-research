# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-26 15:20 WIB (versi 17)
**Tahap sekarang:** S13 — **H-010 LULUS.** Hipotesis pertama dari sepuluh yang melewati seluruh kriteria dan sebelas gerbang sekaligus: ekspektasi **0,053028R** pada run `30193898133`. Lulus dengan tiga margin tipis, jadi ia belum sistem yang terbukti melainkan hipotesis yang belum berhasil dijatuhkan.
**Tahap berikutnya:** **H-011** — uji semesta penuh `--limit 0`, diadjudikasi pada **398 simbol tertahan**. Sudah didaftarkan di ADR-013 §8 dengan ambang dan ramalan dibekukan.

---

## 1. Aturan membaca berkas ini

Bagian 3 adalah **fakta**: setiap baris punya bukti berupa commit, run ID, atau kutipan dokumentasi. Bagian 4 adalah **asumsi**: belum diukur, dan dilarang diperlakukan sebagai fakta. Memindahkan baris dari Bagian 4 ke Bagian 3 hanya boleh dengan bukti terlampir.

Aturan yang lahir dari kesalahan nyata, bukan dari teori:

1. **Angka yang lulus gerbang belum tentu benar.** Rasio 1h:4h 4,014 pernah dicatat sebagai uji silang yang lulus, padahal sedang melaporkan bug.
2. **Sha laporan yang tidak berubah bukan tanda pekerjaan masih berjalan.**
3. **Penjelasan yang membuat anomali terasa wajar harus dicurigai lebih keras daripada anomalinya.**
4. **Lihat sebaran mentah sebelum berteori.** Metrik celah funding gagal lima putaran; satu tabel histogram di awal akan menyelesaikannya dalam satu putaran.
5. **Hipotesis yang ditolak tetap ditolak.** Ambang tidak disetel ulang setelah hasil terlihat.
6. (S8) **Percobaan yang dirancang agar informatif ke dua arah lebih berharga daripada percobaan yang dirancang agar berhasil.**
7. (S9) **Saringan yang membuang perdagangan tidak otomatis membuang perdagangan yang buruk.**
8. (S10) **Periksa apakah dugaanmu mungkin secara konstruksi sebelum menjadwalkannya sebagai penelitian.**
9. (S11) **Sebelum menjadwalkan percobaan, periksa apakah laporan yang sudah dikomit sudah menjawabnya.**
10. (S11) **Gerbang yang kegagalannya tidak tertulis ke `reports/` bukan gerbang, melainkan titik buta yang menyamar sebagai gerbang.**
11. (S12, ADR-009) **Rerata tidak mengatakan apa pun tentang ekor.** Gerbang yang menilai nilai ekstrem hanya boleh dibantah dengan nilai ekstrem.
12. (S12, ADR-009) **Batas risiko tidak dilombakan.** Menaruh pengaman ke dalam grid pemilihan berarti menyerahkan keputusan risiko kepada fungsi tujuan yang tidak melihat risiko.
13. (S12, H-009) **Peristiwa yang terlalu jarang tidak dapat dipilih oleh pemilih dalam sampel, seberapa pun bergunanya.** Pengaman carry menyala 16 kali dari 14.925 perdagangan, yaitu 0,107%. Kelangkaan, bukan biaya, yang membuatnya ditolak 334 lawan 22 di H-008.
14. (S12, H-009) **Ramalan yang salah lebih murah daripada ramalan yang tidak pernah ditulis.**
15. (S12, ADR-010) **Porsi terhadap nilai bersih bukan ukuran konsentrasi.** Konsentrasi diukur dengan **jackknife** dan dengan penyebut **bruto**. Aturan 8 seharusnya sudah menangkap ini; kekeliruan versi 13 membuktikan aturan yang diketahui tidak otomatis diterapkan.
16. (S12, ramalan umur) **Proksi yang berkorelasi 0,97 dengan hal lain bukan proksi.** Umur simbol dan jumlah perdagangan berkorelasi Spearman +0,9668.
17. (S12, ADR-011) **Gerbang yang memberi jawaban sama pada dua keadaan yang bertolak belakang tidak memuat informasi.** Syarat kelayakan gerbang baru bukan "lulus di kasus baik", melainkan "memisahkan dua keadaan yang sudah diketahui berbeda", dan syarat itu wajib jadi pengujian.
18. (S12, ADR-011) **Angka jumlah yang ditulis tangan hanya boleh ada di satu tempat, dan tempat itu adalah pengujian yang sengaja jadi tripwire.**
19. (S13, H-010) **Margin setipis satu satuan resolusi bukan margin.** `entri_acak` H-010 lulus dengan p 0,049505, yaitu 4 dari 100 permutasi; satu permutasi lagi memberi 0,059406 dan menjatuhkannya. Ketika sebuah kriteria lulus dengan jarak sebesar resolusi alat ukurnya, yang terukur adalah resolusinya, bukan keunggulannya. Perbaikannya menaikkan resolusi **sebelum** hasil berikutnya terlihat, bukan sesudahnya.
20. (S13, H-010) **Ekspektasi per perdagangan yang naik karena penyebutnya menyusut bukan keunggulan yang membesar.** H-010 menaikkan ekspektasi 28,2% sementara laba total hanya naik 0,80% dan jumlah perdagangan turun 21,4%. Kedua pernyataan itu benar sekaligus, dan hanya yang pertama yang diukur oleh kriteria. Sebelum menyebut suatu perbaikan sebagai keunggulan, pisahkan perubahan pembilang dari perubahan penyebut.
21. (S13) **Standar kecurigaan wajib naik, bukan turun, ketika hasilnya menyenangkan.** Tiga dari lima ramalan H-010 salah dan **ketiganya salah ke arah yang menguntungkan hipotesis**. Itu justru keadaan ketika penjagaan paling mudah melemah.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa.

Seluruh komputasi berjalan di GitHub Actions. Mesin lokal pengguna tidak sanggup melakukan backtest penuh, dan tidak ada VM cloud karena kendala kartu kredit.

---

## 3. Fakta terverifikasi

### H-010 — LULUS (ADR-012, adjudikasi di ADR-013)

Sumber: `reports/backtest_h010_imbalan_diperluas.{md,json}`, run **`30193898133`**, commit kode **`0a30ced4`**, commit laporan **`c035dcee`**, sidik **`14b2f3bfa8a7`**, **117,5 detik**, 40 simbol, 12 kombinasi.

Mekanisme: identik H-009 kecuali **satu** hal — grid imbalan {1, 2, 3, 4} digeser menjadi **{2, 4, 6, 8}**, jumlah kombinasi tetap 12, jangkar 2,0 dan 4,0 dipertahankan. Tidak satu baris pun ditulis di `lux/strategi/`.

| Kriteria pra-registrasi | Ambang | Nilai | Putusan |
|---|---|---|---|
| `min_ekspektasi_R` | ≥ 0,05 | **0,053028** | lulus |
| `min_trade_luar_sampel` | ≥ 100 | 11.734 | lulus |
| `maks_p_entri_acak` | ≤ 0,05 | **0,049505** | lulus, **satu satuan resolusi** |
| `min_jendela_positif_rasio` | ≥ 0,50 | **0,528090** | lulus |

Sebelas gerbang: `forward_fill` 0,000253 · `buy_and_hold` 0,798562 unggul 36/40 · **`entri_acak` p 0,049505, skor nyata 0,04661R** · `lookahead` 0,0 · `invarian_risiko` **−1,273250** vs −1,5 · `funding` 11.523,31 · `overlap` 0,0 · `checksum` 0,0 · `survivorship` 0,855469 · **`konsentrasi` 0,857845** vs 0,60 · **`funding_ekor` 0,167491** vs 0,35. **Gerbang gagal: nol.**

Alasan keluar: stop 8.776 · target 1.839 · **umur 879** · akhir_data 214 · carry 26. Laju kena target **0,15672**, porsi tak selesai **0,09536**.

**Tiga margin tipis, dan ini bagian terpenting dari seluruh hasil:**

1. `entri_acak` p = (4+1)/(100+1) = **0,049505**. Satu permutasi lagi memberi 6/101 = 0,059406 dan H-010 **GAGAL**. Aturan 19.
2. Skor nyata entri acak turun **0,10781R → 0,04661R (−56,8%)**. Entri acak memakai geometri keluar yang identik, jadi apa pun yang diperbaiki target 8R juga dinikmati entri acak. Tafsiran paling tidak menyenangkan: sebagian besar perbaikan berasal dari **geometri keluar**, bukan dari kandungan informasi sinyal.
3. Jendela positif **0,528090** vs ambang 0,50, turun dari 0,556180.

**Dekomposisi eksak, identitasnya tertutup sampai tujuh desimal:**

| Per perdagangan | H-009 | H-010 | Perubahan |
|---|---|---|---|
| Kotor R | 0,0759727 | **0,0892483** | **+17,5%** |
| Biaya transaksi | 0,0342866 | 0,0353377 | +3,1% |
| Biaya funding | 0,0003276 | 0,0008823 | **+169%** |
| **Bersih R** | **0,0413585** | **0,0530283** | **+28,2%** |

| Agregat | H-009 | H-010 |
|---|---|---|
| Kotor R total | 1.133,89 | **1.047,24** (−7,6%) |
| Biaya total R | 516,62 | 425,01 (−17,7%) |
| **Bersih R total** | 617,28 | **622,23** (+0,80%) |
| Perdagangan | 14.925 | **11.734** (−21,4%) |

Kotor per perdagangan memang naik 17,5%, jadi ini bukan semata penghematan biaya. Tetapi **laba total nyaris tidak bergerak** sementara jumlah perdagangan turun 21,4%. Kriteria yang didaftarkan adalah ekspektasi per perdagangan, jadi H-010 lulus secara sah — namun "lebih banyak per perdagangan dengan berdagang lebih jarang" bukan hal yang sama dengan "keunggulannya membesar". Aturan 20.

**Dinding grid, pertanyaan pokok ADR-012:**

| Imbalan | Jendela | Porsi | Titik impas |
|---|---|---|---|
| **8,0** | **162** | **45,51%** | 0,1111 |
| 6,0 | 96 | 26,97% | 0,1429 |
| 4,0 | 59 | 16,57% | 0,2000 |
| 2,0 | 39 | 10,96% | 0,3333 |

Jumlah 162 + 96 + 59 + 39 = 356, tepat. Batas atas tetap modal tetapi porsinya **45,51%, di bawah 54,5%** milik H-009. Menurut ambang yang ditulis sebelum run: penempelan **bukan** mekanis, dan dinding H-007 **memang** dinding. Rata-rata imbalan terpilih 6,140, titik impasnya 0,1400 terhadap laju nyata 0,15672.

**Temuan tak terduga: dinding `lookback` larut.** H-009 memilih 100 sebanyak 133 jendela; H-010 memberi 20 → 124, 55 → 116, 100 → 116, hampir seragam. Menggeser satu sumbu mengubah pilihan pada sumbu lain, jadi kedua sumbu tidak dapat ditafsirkan sendiri-sendiri.

**Adjudikasi lima ramalan ADR-012 — dua benar, tiga salah:**

| Ramalan | Rentang | Hasil | Putusan |
|---|---|---|---|
| Porsi jendela imbalan 8,0 | 30–55% | 45,51% | **BENAR** |
| Laju kena target | 0,13–0,20 | 0,15672 | **BENAR** |
| Porsi tak selesai | > 12% | 9,54% | **SALAH** |
| `porsi_funding_ekor_maks` | 0,20–0,35 | 0,16749 | **SALAH** |
| Ekspektasi | 0,030–0,048 | 0,053028 | **SALAH** |

Ketiga yang salah, salah ke arah yang **menguntungkan** hipotesis. Aturan 21.

**Adjudikasi tiga ramalan ADR-011 — semuanya BENAR:** porsi ekor 0,14–0,20 → **0,167491** · `porsi_di_atas_pengaman` 0,00107–0,005 → **0,002216** (26 dari 11.734) · `funding_maks_R` 0,25–0,50 → **0,414441**. Gerbang yang ambangnya ditulis dengan curiga berperilaku persis seperti diramalkan.

**Konsentrasi H-010, kini mengikat:** 26 untung / 14 rugi dari 40 simbol · drop-1 0,04549R (retensi **0,857845**) · drop-2 0,03924R · median simbol **+0,04604R** · porsi bruto teratas 0,1346 (ADAUSDT) · setara 14,9 simbol. Jackknife lanjut: k=3 0,035104 · k=4 0,028803 (retensi 0,5432) · k=5 0,022450 (0,4234). Semua sub-uji lulus, tetapi tiap ukuran sedikit **lebih buruk** daripada H-009 kecuali median.

**Pencilan yang wajib diingat:** AIOTUSDT 32 perdagangan, ekspektasi **+1,79837R**. Dilarang dibuang, dan dilarang dijadikan bukti apa pun.

**Utang yang menghalangi kesimpulan statistik:** laporan tidak memuat sebaran R per perdagangan, hanya rerata dan sepuluh terburuk. **Galat baku ekspektasi tidak dapat dihitung**, jadi tidak dapat dikatakan apakah 0,053028 berbeda secara berarti dari 0,041359 atau dari 0,05. Angkanya tidak dikarang. `ringkas_gabungan` wajib memuat `std_R` dan `galat_baku_R` sebelum hipotesis berikutnya diadjudikasi.

### GERBANG KESEBELAS `funding_ekor` — HIDUP (ADR-011)

| Commit | Isi | Pengujian |
|---|---|---|
| `446a3732` | ADR-011, ambang ditulis sebelum kode | — |
| `163a7bad` | `lux/backtest/funding_ekor.py` + 21 pengujian | **488 hijau** (laporan `1a8ee96f`) |
| `114b0d7e` | `NAMA_GERBANG` sebelas, runner menilai dan melaporkan | **494 hijau** (laporan `ad691072`) |

**Masalah yang diselesaikan.** Gerbang `funding` menilai total funding mutlak:

| | H-008 | H-009 | Selisih |
|---|---|---|---|
| Nilai gerbang `funding` | 10.253,97 | 10.199,59 | **−0,53%** |
| Putusan | LULUS | LULUS | sama |
| Funding pada perdagangan terburuk | **0,9228R (46,7%)** | 0,2098R (16,5%) | **−4,4x** |
| Putusan `invarian_risiko` | GAGAL | LULUS | berbalik |

Selama H-007 dan H-008 ia titik buta yang menyamar sebagai gerbang. Aturan 17.

**Ambang tetap, empat sub-uji, semuanya harus lulus:** `porsi_funding_ekor_maks` ≤ **0,35** · `funding_maks_R` ≤ **0,50** · `porsi_trade_di_atas_pengaman` ≤ **0,005** · `jadwal_dimuat` wajib. Turunan 0,35: stop kehilangan ~1,00R kotor, transaksi 0,034R, pengaman 0,25R, jadi batas sah 0,25/1,284 = 0,195; 0,35 adalah 1,8 kali batas itu untuk kelewatan satu bar. **Pengungkapan:** 0,35 duduk di antara dua nilai yang sudah terlihat (0,467 dan 0,165), jadi gerbang ini **mengikat mulai H-010** dan tidak diterapkan ke belakang.

**Bukti bergigi, dikunci sebagai pengujian:** sepuluh terburuk H-008 memberi 0,467 dan **GAGAL**; enam terburuk H-009 memberi 0,165 dan lulus. Di H-010 ia memberi 0,167491 dan lulus.

**Gerbang `funding` lama tidak dihapus,** hanya diturunkan pangkat menjadi pemeriksaan kebersihan.

### GERBANG KESEPULUH `konsentrasi` (ADR-010)

Modul di `211fb3bd` (18 pengujian, 462 hijau), penyambungan di `8cf70f08` (5 pengujian, 467 hijau, laporan `10732424`). `semua_lulus` memakai `len(NAMA_GERBANG)`, bukan literal.

Ambang tetap, **mengikat mulai H-010**: `drop_1_positif` > 0 · `drop_5persen_positif` > 0 atas ⌈0,05·N⌉ · `retensi_drop_1` ≥ 0,60 · `median_simbol_positif` > 0 · `porsi_bruto_teratas` ≤ 0,25 dengan penyebut bruto. Sub-uji yang tidak dapat dinilai berarti GAGAL.

**Konsekuensi diterima sadar:** tiga orkestrator beku (`run_wf`, `run_h002`, `run_h003`) hanya menyusun sembilan gerbang, jadi bila dijalankan lagi laporannya gagal pada `konsentrasi` dan `funding_ekor`. Angka lama di `reports/` tidak berubah.

### RAMALAN 3 ADR-010 — DIFALSIFIKASI: umur simbol tidak menerangkan apa pun

Sumber: `reports/umur_simbol.md`, commit **`bce8cf89`**, dihitung di sandbox dari `per_simbol` H-009 — nol run baru.

| Ukuran | Nilai |
|---|---|
| Spearman(umur, ekspektasi) | **−0,0336** |
| p dua sisi, 20.000 permutasi, seed 42 | **0,8351** |
| Spearman(umur, jumlah trade) | +0,9668 |

Per ember umur pola **tidak monoton**: 2–4 jendela +0,056342 · 5–9 **+0,068240** · 10–19 +0,026059 · 20–24 +0,035878. **Membuang simbol muda justru menurunkan ekspektasi** ke 0,038970. Asal kekeliruan: dua pencilan, AIOTUSDT dan 1000000BOBUSDT — penalaran dari ekor sebaran, bukan dari sebarannya.

### H-009 — DITOLAK, tetapi sembilan gerbang lulus untuk pertama kalinya

Sumber: run **`30186730437`**, kode **`d5f18c6f`**, laporan **`77b7492c`**, sidik `eac6c83305bd1069`, 155,4 detik.

| | H-007 | H-008 | **H-009** |
|---|---|---|---|
| Ekspektasi R | +0,04044 | +0,04126 | **+0,041359** |
| Total R | +605,10 | +616,20 | **+617,28** |
| Perdagangan | 14.962 | 14.933 | **14.925** |
| Keluar `carry` | — | 2 | **16** |
| `invarian_risiko` | −1,9769 GAGAL | −1,9769 GAGAL | **−1,2698 LULUS** |

Putusan DITOLAK, alasan tunggal `ekspektasi 0.0414R < 0.05R`. `entri_acak` p **0,0099**, skor nyata 0,10781R. Alasan keluar: stop 10.242, target 4.111, umur 368, akhir_data 188, carry 16.

### Bukti bahwa pengaman memotong tepat sasaran

| H-008 | funding R | Nasib di H-009 |
|---|---|---|
| AIOTUSDT −1,9769 | **0,9228** | hilang — di atas ambang |
| ALGOUSDT −1,4067 | **0,3866** | hilang — di atas ambang |
| 1000XECUSDT −1,3869 | **0,3083** | hilang — di atas ambang |
| AAVEUSDT −1,3637 | **0,3285** | hilang — di atas ambang |
| 1000XECUSDT −1,3215 | **0,2728** | hilang — di atas ambang |
| ADAUSDT −1,2698 | 0,2098 | **bertahan, R identik** |
| 1000FLOKIUSDT −1,2614 | 0,1985 | **bertahan, R identik** |
| 1000WHYUSDT −1,2362 | 0,1789 | **bertahan, R identik** |
| 1000XECUSDT −1,2282 | 0,1996 | **bertahan, R identik** |
| 1000FLOKIUSDT −1,2154 | 0,1714 | **bertahan, R identik** |

Kelima yang hilang adalah **tepat** kelima yang carry-nya melewati 0,25R; kelima yang bertahan sama sampai belasan desimal (ADAUSDT `-1.2697928364736204` di kedua run). **Nol korban sampingan.** Tabel inilah kasus uji gerbang kesebelas.

### Adjudikasi ramalan H-009 — dua dari tiga SALAH

| Ramalan | Hasil | Putusan |
|---|---|---|
| Keluar `carry` melonjak ke **ratusan** | **16** | **SALAH** |
| Kerugian terburuk di bawah 1,5R | −1,2698 lulus | **BENAR** |
| Ekspektasi **turun** di bawah 0,04126R | naik ke 0,041359 | **SALAH** |

Selisih +0,041359 lawan +0,04126 adalah 0,00009R. Menyebutnya perbaikan berarti memakai dua timbangan; **ekspektasi H-009 tidak berubah**, yang berubah hanya ekornya. Bandingkan dengan H-010: +0,011670R, empat belas kali lebih besar daripada selisih yang pernah saya tolak sebagai derau.

### Mengapa pemilih menolak pengaman yang ternyata gratis

Klaim ADR-009 bahwa pengaman memakan ekspektasi **separuhnya terbantah**: di luar sampel ia tidak memakan ekspektasi sama sekali. Yang tetap fakta: pemilih mematikannya **334 dari 356 jendela**. Penjelasan yang benar adalah **kelangkaan**, bukan biaya. Aturan 13. Konsekuensinya luas: **setiap pengaman yang menargetkan peristiwa langka akan selalu ditolak oleh pemilihan dalam sampel.**

### KONSENTRASI LABA — klaim versi 13 DITARIK

Versi 13 menyebut sebagai fragilitas terbesar bahwa "sepuluh dari 40 simbol menghasilkan 101,2% laba". Angkanya benar, tafsirannya menyesatkan **secara konstruksi**, karena penyebutnya sudah dipotong kerugian.

| | Jumlah simbol | R |
|---|---|---|
| Simbol laba | **28** | **+883,62** |
| Simbol rugi | **12** | **−266,35** |
| Bersih | 40 | **+617,28** |

Angka yang tidak menyesatkan (H-009): 28/40 menguntungkan · median +0,0325R · kuartil −0,0170 / +0,0325 / +0,1401 · rentang −0,21618 sampai +1,36566 · **HHI 0,0621, setara 16,1 simbol**.

| Dibuang | Simbol | Sisa R | Ekspektasi | Retensi |
|---|---|---|---|---|
| 0 | — | 617,28 | **+0,041359** | 100% |
| 1 | ADAUSDT | 503,97 | **+0,035962** | **87,0%** |
| 2 | ALGOUSDT | 430,22 | +0,033000 | 79,8% |
| 3 | 1000FLOKIUSDT | 359,46 | +0,028420 | 68,7% |
| 4 | ALPHAUSDT | 293,64 | +0,024540 | 59,3% |
| 5 | AIOTUSDT | 233,56 | +0,019590 | 47,4% |
| 8 | 1000PEPEUSDT | 78,00 | +0,007028 | 17,0% |
| 10 | — | — | **≤ 0** | 0% |

**Dilarang tegas:** membuang 12 simbol merugi menaikkan ekspektasi ke sekitar **0,0752R** dan melewati ambang. Survivorship bias telanjang — dicatat agar dikenali sebagai jebakan.

### Papan skor sepuluh hipotesis

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
| H-009 | pengaman carry dipatok 0,25 | 0,041359 | tidak ada | DITOLAK, hanya oleh ambang 0,05R |
| **H-010** | **grid imbalan {2,4,6,8}** | **0,053028** | **tidak ada dari sebelas** | **LULUS** |

**Kesimpulan struktural yang bertahan dan kini diperkuat:** enam percobaan pada sisi **masuk** menghasilkan nol perbaikan; empat percobaan pada sisi **keluar** menghasilkan +28% (H-007), penutupan gerbang risiko (H-009), dan +28% lagi (H-010). **Sisi keluar adalah satu-satunya arah yang pernah memberi leverage.** Sisi masuk tetap belum terbukti memuat informasi — dan skor entri acak H-010 yang turun 56,8% adalah bukti terkuat sejauh ini bahwa keunggulannya mungkin **seluruhnya** ada di sisi keluar.

### PENYEBAB KEGAGALAN `invarian_risiko` — TERUKUR DAN TERTUTUP

Perdagangan terburuk H-008 AIOTUSDT: R −1,9769 = kotor −1,0182 − transaksi 0,0359 − **funding 0,9228**. **Funding 46,7% kerugian terburuk**, komponen biaya terbesar di kesepuluh terburuk. Dua kandidat penjelasan saya sendiri terbantah oleh data yang sama: stop bekerja sempurna (kotor −1,0065 sampai −1,0260) dan stop rapat bukan penyebabnya (lebar terburuk 2,83% terhadap rerata 3,61%). H-009 mengonfirmasi diagnosis secara kausal. Di H-010 kerugian terburuk **−1,273250**, praktis tak bergerak dari H-009.

### Mengapa ADR-008 gagal

| Ambang `maks_carry_realisasi_R` di H-008 | Jendela memilihnya |
|---|---|
| 0,0 — mati | **334** dari 356 |
| 0,25 | 22 |
| 0,50 | **0** |

H-008 bukan uji terhadap pengaman carry, melainkan uji terhadap kesediaan pemaksimal ekspektasi memakai pengaman yang peristiwanya langka. Jawabannya tidak.

### Titik impas: yang salah adalah aritmetikanya, bukan sinyalnya

Titik impas kotor `1/(1+imbalan)`: 1R 0,5000 · 2R 0,3333 · 3R 0,2500 · 4R 0,2000 · 6R 0,1429 · 8R 0,1111, dikunci `tests/test_titik_impas.py`. Di H-009, **194 dari 356 jendela (54,5%) memilih imbalan 4,0** dan 101 memilih 3,0; angka itu terverifikasi tiga kali — dari `parameter_terpilih` yang dikomit, dari komentar `backtest.yml`, dan dari penjumlahan tangan 82 + 64 + 48. **Versi 16 menulis 226 dan 63,5%; itu salah dan sudah diperbaiki di sini.**

| Hipotesis | Laju kena target | Kotor `3p−1` | Bersih tercatat | Seretan |
|---|---|---|---|---|
| H-002 | 0,36028 | +0,08084 | +0,03159 | 0,04926 |
| H-004 | 0,34151 | +0,02453 | −0,01818 | 0,04272 |
| H-005 | 0,33755 | +0,01265 | −0,03571 | 0,04836 |
| H-006 | 0,30122 | −0,09633 | −0,13449 | 0,03815 |
| H-003 | 0,26326 | −0,21021 | −0,24782 | 0,03761 |
| H-009 | 0,27544 | — | +0,041359 | 0,034614 |
| **H-010** | **0,15672** | — | **+0,053028** | **0,036220** |

### KELUARGA ADR-006 — DITOLAK BERTIGA

Run `30175665060`, kode `1aedb84`, laporan `c0636bf`. Ambang p diperketat ke **0,0167 (Bonferroni 0,05/3) sebelum satu angka pun terlihat**, dan itu terbukti bergigi: p H-005 0,0396 akan lolos ambang biasa 0,05. Trend breakout tidak diuji ulang karena itu persis H-001b dan H-002. Bagian SMC lain (order block, FVG, BOS/CHoCH) tidak diuji karena tidak punya definisi mekanis.

### H-003 — pembalikan skor-z, DITOLAK telak

Run `30175179866`. −0,24782R, 28.959 perdagangan, 25/356 jendela positif, `entri_acak` p 1,0000. Dengan H-006 gagal serupa: **pada 1h perp USDT, pembalikan jangka pendek rugi sistematis.**

### MESIN BACKTEST — sebelas gerbang, terbukti bisa lulus maupun gagal

`lux/backtest/`: `engine.py`, `gerbang.py`, `konsentrasi.py`, `funding_ekor.py`, `walk_forward.py`, `run_wf.py` (H-001b), `run_h002.py`, `run_h003.py`, `runner.py`, `run_keluarga.py`, `run_h007.py`, `run_h008.py`, `run_h009.py`, **`run_h010.py`**.

**`run_h010.py` tidak menyalin satu nilai pun:** `LOOKBACK = list(LOOKBACK_H007)` dan `buat_konfig`, `DATASET`, `KUNCI_TERLARANG`, `AMBANG_CARRY_KERAS` diimpor **dari `run_h009` apa adanya**; hanya `IMBALAN` yang didefinisikan sendiri. `run_h009` mengimpor gridnya dari `run_h007` dan memasang `assert` bahwa keduanya identik, jadi **`run_h007.IMBALAN` haram disunting** — menyuntingnya akan membatalkan penjaga itu dan mengubah arti laporan yang sudah dikomit. Penjaga pra-terbang `backtest.yml` menolak run bila dinding digeser ke dalam, bila jumlah kombinasi berubah, bila jangkar hilang, atau bila `buat_konfig` bukan fungsi H-009 yang sama.

Gerbang: `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`, `konsentrasi`, `funding_ekor`. **Gerbang yang tidak dapat dinilai berarti GAGAL.**

Lima alasan keluar: `stop`, `target`, `umur`, `carry`, `akhir_data`. Urutan per bar: umur → carry → stop/target → entri → ekuitas. `ALASAN_TIDAK_SELESAI = ("umur", "akhir_data", "carry")`.

Pra-registrasi **sekali tulis**; nilai saringan ikut masuk sidik. `hipotesis/H-010.json` terdaftar dengan sidik `14b2f3bfa8a7`, dan ambang carry 0,25 ikut masuk sidik lewat `ruang_parameter.maks_carry_realisasi_R = [0.25]` meski bukan sumbu pencarian.

### DATASET TIER B PUTARAN 2 — SAH

**14.545.679 bar 1h dan 3.636.733 bar 4h**, 790 simbol, 112 celah kisi, rasio 1h:4h **3,9996**, sekitar 703 MB. Validasi 1h: 0 pelanggaran fatal, **447 simbol layak**. ADR-003 memangkas 141 simbol berekor datar, 1.081.920 bar (7,4%), universe layak v2 = **438**. Funding: 1.982.017 baris, 447 simbol, 3 celah sejati, 79,1% positif, jitter maksimum 47 ms, 295 dari 447 simbol hidup di lebih dari satu rezim kisi. Carry ekstrem: 1000WHYUSDT +60,7%/tahun, AERGOUSDT −102,6%, MYXUSDT −533,9%.

**Yang belum pernah diuji:** 398 dari 438 simbol layak. Setiap hasil dari H-001b sampai H-010 berdiri di atas **40 simbol pertama secara alfabet**. H-011 menguji tepat asumsi ini.

### Pengujian — `reports/tests.md`

**510 pengujian hijau** pada commit `3fa9f58c` (laporan `53c6684c`), kode keluar 0, 2,51 detik, tanpa jaringan. Jejak aritmetisnya utuh dan setiap langkahnya diramalkan lebih dulu: 444 → **462** (+18 `test_konsentrasi.py`) → **467** (+5 `test_gerbang_kesepuluh.py`) → **488** (+21 `test_funding_ekor.py`) → **494** (+6 `test_gerbang_kesebelas.py`) → **510** (+16 `test_run_h010.py`). Lima ramalan jumlah pengujian berturut-turut, kelimanya tepat.

### Kapasitas runner dan konektivitas

4 vCPU, 15 GB RAM, 88 GB disk. **Batas 6 jam per job yang menjadi kendala, bukan disk.** H-010 selesai **117,5 detik** untuk 40 simbol dan 12 kombinasi (H-009 155,4 detik; lebih cepat karena 21% lebih sedikit perdagangan). Penskalaan kasar ke 438 simbol: sekitar 21 menit sebelum memperhitungkan kenaikan ulangan permutasi. Aset 559 MB. CDN `data.binance.vision` 200; REST `fapi.binance.com` **451 permanen**.

### Batas alat agen dan solusinya

- Daftar alat GitHub yang tersedia **tidak memuat satu pun fungsi Actions** — tidak ada pembacaan run, job, langkah, atau log. Diverifikasi di S11.
- `search_code` **tidak berguna di repo ini**; indeksnya belum memuat repo muda. Baca berkas langsung.
- Agen tidak bisa membuat rilis, memicu workflow manual, atau mengunduh artifact.
- Setiap workflow diberi filter `paths` pada berkasnya sendiri. `tests.yml` memfilter `lux/**` dan `tests/**`.
- **Setiap langkah yang bisa gagal wajib menulis hasilnya ke `reports/`** dengan `if: always()`.
- **Gerbang yang bisa gagal ditaruh sebelum unduhan.** Penjaga ADR-012 di `backtest.yml` berjalan dalam hitungan detik, bukan setelah 559 MB.
- Sandbox agen **tidak punya jaringan**. Gerbang `pytest` wajib berjalan **sebelum** unduhan.
- **Commit laporan tanpa berkas hasil berarti run GAGAL, bukan sedang berjalan.**
- Blob laporan yang tidak berubah berarti **belum ditulis**, bukan berhasil. Penyambungan gerbang kesebelas butuh **tiga** pengambilan; laporan H-010 butuh **sebelas**. **SHA blob juga basi begitu ada tulisan**; `push_files` lebih aman daripada `create_or_update_file`.
- **Modul baru berdiri hijau sendiri lebih dulu, penyambungan menyusul.** Dipakai tiga kali: `konsentrasi.py` (462 lalu 467), `funding_ekor.py` (488 lalu 494), dan `run_h010.py` (510 lalu workflow dibalik).
- **Sebelum menulis kode terhadap modul lain, baca modulnya.** Pembacaan `run_h009.py` menemukan `assert` grid beku yang akan pecah bila `run_h007` disunting; pembacaan `backtest.yml` menemukan angka 194 yang membuktikan "226" salah.
- **Analisis atas laporan yang sudah dikomit dapat dikerjakan di sandbox tanpa jaringan** — tetapi tidak selalu bisa: sebaran R dan sebaran funding per perdagangan tidak ada di laporan.

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1** (`5f222e8`): `header=0` + `skiprows=1` menghilangkan satu bar per berkas.
- **Parser 2 dan 3** (`16638b4`): BOM UTF-8; satu baris sampah menggagalkan seluruh berkas.
- **URL non-ASCII**: percent-encoding lewat `bv.seg()`.
- **Metrik celah funding**: gagal lima putaran karena mengira kisi funding tetap.
- **Circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`). Alasan terdokumentasi mengapa `konsentrasi.py` dan `funding_ekor.py` berdiri sebagai modul sendiri.
- **S10:** kurung kurawal liar di `tests/test_run_h007.py` (`c48a785`); diperbaiki `e81e34e`.
- **S11:** langkah pra-terbang `backtest.yml` bisu; diperbaiki `245747ee`.
- **S12:** STATE v11 menaikkan kekeliruan analitis menjadi fakta ("funding bukan penyebab kerugian ekor"). Ditarik di v12. Penyebabnya memakai rerata untuk menyimpulkan tentang ekor.
- **S12:** STATE v13 menaikkan artefak aritmetika ("sepuluh simbol menghasilkan 101,2% laba") menjadi fragilitas terbesar. Ditarik di ADR-010 dan v14. Penyebabnya penyebut bersih.
- **S12:** dugaan "simbol muda lebih menguntungkan" lahir dari dua pencilan; difalsifikasi di v15.
- **S12:** `tests/test_gerbang_kesepuluh.py` memakai literal `== 10` di tiga tempat, di berkas yang menguji kode yang justru melarang literal semacam itu. Pecah saat gerbang kesebelas masuk; diperbaiki di `114b0d7e`. Aturan 18.
- **S13:** ADR-012 versi pertama dan STATE v16 menulis **"226 dari 356 jendela (63,5%) memilih imbalan 4,0"** plus catatan palsu bahwa jumlah per kombinasi "melewati 356". Nilai benarnya **194 (54,5%)** dan jumlahnya tepat 356. Angka benar sudah ada di **tiga** tempat di repo — `parameter_terpilih` yang dikomit, komentar `backtest.yml`, dan log run — dan tetap dikarang dari ingatan. Diperbaiki di ADR-012 (dengan bagian koreksi eksplisit) dan di v17. **Kelas kesalahan yang sama dengan "26 simbol positif" dan label "16 pengujian": jumlah yang tidak dijumlah ulang. Tiga kali dalam dua sesi.**

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| **Hasil 40 simbol pertama mewakili 438 simbol** | **H-011, sudah didaftarkan di ADR-013 §8; ramalan saya: ekspektasi TURUN ke 0,020–0,045** |
| Keunggulan H-010 bukan seluruhnya milik geometri keluar | skor entri acak turun 56,8%; butuh uji yang memisahkan sinyal dari geometri keluar, dan uji itu belum dirancang |
| Keunggulan kelanjutan membesar pada horizon lebih panjang (4h) | jalankan hipotesis baru pada 4h setelah validasi 4h |
| Funding sebagai **sinyal** memuat informasi arah, bukan hanya biaya | uji hipotesis berbasis funding, belum pernah dilakukan |
| Integritas 4h sama bersihnya dengan 1h | jalankan `validate.yml` untuk interval 4h |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap universe layak v2 438 |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |

**Turun menjadi fakta di S9:** saringan rezim tren memperbaiki breakout (**salah**, H-004); retest memperkecil biaya per R secara menguntungkan (**salah**, H-005); SMC yang dapat dikodekan punya keunggulan (**salah**, H-006).

**Terbukti di S10:** menurunkan titik impas lewat imbalan lebih besar menaikkan ekspektasi (**benar**, +28%), dan menaikkan lama pegang sehingga kerugian ekor membesar (**benar**).

**Diselesaikan di S12:** pengaman carry dipatok membuat `invarian_risiko` lulus (**benar**, −1,9769 → −1,2698) · "biaya menjaga risiko memakan ekspektasi" (**salah**, biayanya nol dalam batas derau) · keunggulan bertahan bila penyumbang terbesar dibuang (**benar**, retensi 87,0%) · "ekspektasi bergantung umur simbol" (**salah**, difalsifikasi) · "kerugian ekor dari bar menganga" (**salah**) · "dari stop sangat rapat" (**salah**) · "funding bukan penyebab kerugian ekor" (**ditarik**, 46,7%) · "laba terkonsentrasi pada sepuluh simbol" (**ditarik**) · "gerbang funding memantau biaya funding" (**salah**).

**Diselesaikan di S13:**

- "Optimum imbalan berada di luar grid H-007" — **BENAR sebagian.** Batas atas baru 8,0 dipilih 45,51% jendela, jadi grid lama memang membatasi; tetapi porsinya lebih rendah daripada 54,5% milik batas lama, jadi optimumnya kini berada **di dalam** grid.
- "Dinding `lookback` juga perlu digeser" — **hangus.** Menggeser dinding imbalan melarutkan dinding lookback dengan sendirinya (133 → 116, sebaran hampir seragam). Utang ADR-012 §7 gugur, bukan terselesaikan.
- "Target lebih jauh membesarkan porsi funding di ekor" — **SALAH.** 0,16749 lawan 0,165, praktis tak bergerak, meski funding per perdagangan naik 169%.
- "H-010 akan menjadi penolakan kesepuluh" — **SALAH.** Ia lulus.

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 (14.076.257 baris 1h, 3.506.060 baris 4h, 17.169 celah, rasio 4,014); metrik celah funding putaran 1–4 (1.380.741 · 1.193.209 · 587.131 · 266.612); seluruh run pilot H-001 termasuk `30170073890`; **porsi "101,2%" sebagai bukti konsentrasi**; **selisih ekspektasi muda-lawan-tua +0,017 sampai +0,033R sebagai efek umur**; **nilai gerbang `funding` (10.253,97 / 10.199,59) sebagai bukti funding aman**; **"226 jendela / 63,5% memilih imbalan 4,0" — angka karangan, yang benar 194 / 54,5%**; **ekspektasi H-010 0,053028R sebagai bukti sistem layak dagang** — ia satu run, 40 simbol, tiga margin tipis, tanpa galat baku.

---

## 5. Penghalang aktif

Tidak ada yang menghentikan pekerjaan.

Dibutuhkan dari pengguna, belum memblokir: **token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`.

---

## 6. Tindakan berikutnya

1. **H-011 — uji semesta penuh.** Sudah didaftarkan di ADR-013 §8; ambang dan tujuh ramalan dibekukan. `lux/backtest/run_h011.py` mengimpor seluruh mekanisme dari `run_h010` apa adanya, `--limit 0` (438 simbol), `--ulangan 300`. Kriteria utama: ekspektasi berbobot perdagangan atas **398 simbol tertahan**, dihitung tangan dari `per_simbol` sehingga tidak ada kode baru yang bisa menyelundupkan asumsi. **Ramalan saya: ekspektasi turun ke 0,020–0,045 dan H-011 gagal.** Urutan wajib: modul + pengujian hijau lebih dulu, workflow dibalik sesudahnya.

2. **`std_R` dan `galat_baku_R` di `ringkas_gabungan`.** Tanpa keduanya tidak ada hipotesis yang bisa diadjudikasi secara statistik, termasuk H-010 yang sudah lulus. Utang ADR-013 §7.

3. **Uji yang memisahkan sinyal dari geometri keluar.** Skor entri acak turun 56,8% di H-010, jadi kemungkinan seluruh keunggulan ada di sisi keluar. Rancangannya belum ada dan wajib punya ADR sendiri.

4. **Horizon 4h.** Prasyarat mutlak: jalankan `validate.yml` untuk 4h.

5. **Funding sebagai sinyal.** Belum pernah diuji kandungan informasi arahnya.

**Yang DILARANG:** menyatakan sistem siap dagang karena H-010 lulus; mematok `imbalan_R` ke 8,0 (menang pasca-hoc); menurunkan `--ulangan` bila `entri_acak` gagal di H-011; menaikkan `maks_umur_bar` dari 168 untuk memperbaiki porsi tak selesai 9,54%; membuang simbol yang merugi (naik ke ±0,0752R, survivorship bias telanjang); memakai gerbang `konsentrasi` atau `funding_ekor` sebagai penyaring simbol; memasukkan saringan berbasis umur simbol; membuang AIOTUSDT karena ekspektasinya tampak mustahil (+1,79837R di H-010); melombakan ambang pengaman dalam bentuk apa pun; menghitung ulang hipotesis yang sudah divonis; melonggarkan ambang `invarian_risiko` dari −1,5R; melonggarkan ambang ADR-011; **menurunkan ambang ekspektasi 0,05R** — dan sekarang juga **menaikkannya** setelah H-010 lulus, karena keduanya sama-sama menyetel ambang terhadap hasil.

Sisanya, tidak memblokir:

6. Perketat `lux/funding.py::gerbang_lulus`, masih terlalu longgar dan berdiri di jalur ingest. Utang ADR-011.
7. Perbaiki docstring `lux/costs.py` yang masih menyebut pembagi funding 8 jam tetap.
8. Diff terhadap Dataset G lama (528 simbol). **Satu-satunya butir dari daftar tugas awal pengguna yang benar-benar masih terbuka.**
9. `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md`; salin ADR-001 dan ADR-002 ke `decisions/`.
10. Pelapor Notion (`NOTION_TOKEN`); instruksi Gatekeeper masih menyebut sembilan gerbang.
11. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, dengan ≥24 shard.

---

## 7. Pengawasan otonom

Agen **LUX Gatekeeper** aktif di Notion. Terpicu saat runner membuat baris di database Run Results, menilai hasil terhadap gerbang mutu. Sudah diuji dengan baris sintetis bercacat dan menolak dengan benar. **Verdict Ditolak menghentikan pipeline.** Instruksinya masih menyebut sembilan gerbang dan perlu disesuaikan menjadi sebelas bila pelapor Notion diaktifkan.

---

## 8. Peta repo

| Path | Isi |
|---|---|
| `config/lux.yaml` | seluruh parameter yang memengaruhi hasil; `maks_carry_R 0.25` asal-usul ambang H-009 dan acuan ADR-011 |
| `lux/binance_vision.py` | klien arsip: listing S3, unduhan, checksum, percent-encoding |
| `lux/universe.py` | universe point-in-time dan klasifikasi jenis kontrak |
| `lux/ingest.py` | ingest Tier B dengan validasi per simbol |
| `lux/backfill_daily.py` | penutup celah ekor dari arsip harian |
| `lux/validate.py` · `lux/validate_run.py` | integritas OHLCV, kelayakan universe, penolak aset `_retry` |
| `lux/funding.py` · `lux/funding_check.py` | ingest funding rate dan metrik kisinya; `gerbang_lulus` masih terlalu longgar |
| `lux/funding_model.py` | jadwal funding nyata, penagihan, carry terproyeksi dan terealisasi |
| `lux/costs.py` | model biaya dalam satuan R |
| `lux/diag_datar.py` · `lux/potong_ekor.py` | diagnosis dan pemangkasan ekor datar (ADR-003) |
| `lux/praregistrasi.py` | hipotesis sekali tulis dan penilaian terhadap kriteria |
| `lux/analisis/titik_impas.py` | aritmetika titik impas atas laporan yang sudah dikomit |
| `lux/strategi/breakout_atr.py` | sinyal kelanjutan (H-001b, H-002, H-007, H-008, H-009, **H-010**) |
| `lux/strategi/reversi_zskor.py` | sinyal pembalikan (H-003) |
| `lux/strategi/rezim_adx.py` | ADX Wilder dan saringan rezim (H-004) |
| `lux/strategi/retest.py` | entri retest, "sniper entry" mekanis (H-005) |
| `lux/strategi/smc.py` | sapuan likuiditas, bagian SMC yang dapat dikodekan (H-006) |
| `lux/backtest/engine.py` | mesin eksekusi: stop, target, batas umur, saringan carry, pengaman carry terealisasi |
| `lux/backtest/gerbang.py` | sembilan gerbang pertama + `NAMA_GERBANG` sebelas nama; `semua_lulus` memakai `len(NAMA_GERBANG)` |
| `lux/backtest/konsentrasi.py` | **gerbang kesepuluh**: `ukur_konsentrasi`, `tabel_jackknife`, `gerbang_konsentrasi` |
| `lux/backtest/funding_ekor.py` | **gerbang kesebelas**: `ukur_funding_ekor`, `tabel_ekor_funding`, `gerbang_funding_ekor` |
| `lux/backtest/walk_forward.py` | pemilihan parameter dalam sampel; konfig per kandidat opsional (ADR-007) |
| `lux/backtest/run_wf.py` | orkestrator H-001b — **jangan disunting**; sumber `rincian_R` dan `diagnosa_biaya` |
| `lux/backtest/run_h002.py` · `run_h003.py` | orkestrator beku; hanya sembilan gerbang |
| `lux/backtest/runner.py` | **runner bersama**: muat sekali, jalankan, nilai sebelas gerbang, tulis jackknife dan ekor funding. **Belum memuat `std_R`** |
| `lux/backtest/run_keluarga.py` | keluarga ADR-006 (H-004, H-005, H-006) |
| `lux/backtest/run_h007.py` | H-007 — **sumber grid bersama, HARAM disunting**; `run_h009` memasang assert atasnya |
| `lux/backtest/run_h008.py` · `run_h009.py` | dibekukan; `run_h009` sumber `buat_konfig` dan `AMBANG_CARRY_KERAS` |
| `lux/backtest/run_h010.py` | **H-010, satu-satunya hipotesis yang lulus**; grid imbalan sendiri, sisanya diimpor |
| `tests/` | **510** pengujian tanpa jaringan, wajib hijau sebelum unduhan. Jumlah gerbang ditulis sebagai angka **hanya** di `test_gerbang_kesebelas.py` |
| `reports/` | keluaran mesin tiap run. **`umur_simbol.md` pengecualian: dihitung di sandbox, provenansnya tertulis di dalamnya** |
| `hipotesis/` | pendaftaran sekali tulis: `H-001b` … **`H-010`** |
| `decisions/` | ADR-003 … **ADR-013** |
| `journal/` | riwayat per sesi |

**Workflow aktif (10):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`. `backtest.yml` sekarang menjalankan **`lux.backtest.run_h010`** dan memuat penjaga pra-terbang ADR-009 + ADR-012 yang berhenti dalam hitungan detik.

**Dihapus di S7:** `analyze_tail.yml` (`07860a7`), `diagnose.yml` (`f4af734`), `diag_datar.yml` (`41ca693`), `retry_failed.yml` (`3a206c6`).

Release **`tier-b-v1`** memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`. Pola unduh backtest wajib `ohlcv_1h_*.parquet`.
