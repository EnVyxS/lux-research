# ADR-013 — H-010 lulus, dan justru karena itu wajib dicurigai

**Status:** diterima sebagai catatan putusan. **Bukan** izin dagang, bukan pembenaran menaikkan ukuran posisi, bukan alasan menghentikan pengujian.

**Tanggal:** 2026-07-26

---

## 1. Bukti

Run **`30193898133`** · commit kode **`0a30ced4`** · commit laporan **`c035dcee`** · sidik hipotesis **`14b2f3bfa8a7`** · 117,5 detik · 40 simbol · 12 kombinasi · 510 pengujian hijau di pra-terbang.

Laporan: `reports/backtest_h010_imbalan_diperluas.{md,json}`, log `reports/backtest_log.md`.

| | H-009 | **H-010** | Perubahan |
|---|---|---|---|
| Grid imbalan | {1, 2, 3, 4} | **{2, 4, 6, 8}** | dinding digeser ke luar |
| Ekspektasi R | 0,041359 | **0,053028** | **+28,2%** |
| Total R | 617,2774 | **622,2348** | **+0,80%** |
| Perdagangan luar sampel | 14.925 | **11.734** | **−21,4%** |
| Jendela positif | 198/356 = 0,556180 | 188/356 = **0,528090** | −5,0% |
| Laju kena target | 0,27544 | **0,15672** | −43,1% |
| Porsi tak selesai | 0,03832 | **0,09536** | 2,5x |
| `invarian_risiko` | −1,2698 | **−1,2733** | tak berubah |
| `entri_acak` p | **0,009901** | **0,049505** | **5x lebih buruk** |
| `entri_acak` skor nyata | 0,10781R | **0,04661R** | **−56,8%** |
| `funding_ekor` porsi ekor maks | 0,165 † | **0,16749** | tak berubah |
| `konsentrasi` retensi drop-1 | 0,8695 † | **0,857845** | sedikit lebih buruk |
| Gerbang gagal | 0 dari 9 | **0 dari 11** | — |
| **Putusan** | DITOLAK | **LULUS** | — |

† nilai H-009 bersifat deskriptif; kedua gerbang itu baru mengikat mulai H-010.

## 2. Putusan formal

Seluruh kriteria pra-registrasi, yang tidak pernah diubah sejak H-002:

| Kriteria | Ambang | Nilai | Putusan |
|---|---|---|---|
| `min_ekspektasi_R` | ≥ 0,05 | **0,053028** | lulus |
| `min_trade_luar_sampel` | ≥ 100 | 11.734 | lulus |
| `maks_p_entri_acak` | ≤ 0,05 | **0,049505** | lulus, **satu satuan resolusi** |
| `min_jendela_positif_rasio` | ≥ 0,50 | **0,528090** | lulus |

Sebelas gerbang lulus, `putusan.lulus = true`, `alasan: []`. **H-010 adalah hipotesis pertama dari sepuluh yang lulus,** dan hipotesis pertama yang dinilai sebelas gerbang penuh.

## 3. Vonis lima ramalan: dua benar, tiga salah

| Ramalan ADR-012 | Rentang | Hasil | Putusan |
|---|---|---|---|
| 1. Porsi jendela memilih imbalan 8,0 | 30–55% | **45,51%** (162/356) | **BENAR** |
| 2. Laju kena target | 0,13–0,20 | **0,15672** | **BENAR** |
| 3. Porsi tak selesai | > 12% | **9,54%** | **SALAH** |
| 4. `porsi_funding_ekor_maks` | 0,20–0,35 | **0,16749** | **SALAH** |
| 5. Ekspektasi | 0,030–0,048 | **0,053028** | **SALAH** |

**Ketiga ramalan yang salah, salah ke arah yang menguntungkan hipotesis ini.** Itu keadaan paling berbahaya yang pernah dihadapi riset ini, karena standar kecurigaan cenderung melemah tepat ketika hasilnya menyenangkan.

Satu pengakuan tentang timbangan. Saya menolak selisih +0,00082R milik H-008 sebagai derau. Kenaikan H-010 adalah **+0,011670R**, yaitu **empat belas kali** lebih besar, jadi ia tidak dapat dibuang sebagai derau dengan timbangan yang sama. Itu argumen yang mendukung H-010, dan saya tuliskan justru supaya terlihat bahwa timbangannya tidak diganti di tengah jalan.

**Tiga ramalan ADR-011 semuanya BENAR,** dan itu satu-satunya bagian yang boleh dibanggakan hari ini: porsi ekor mendarat di 0,14–0,20 (**0,16749**), `porsi_di_atas_pengaman` di antara 0,00107 dan 0,005 (**0,002216**, 26 dari 11.734), `funding_maks_R` di antara 0,25 dan 0,50 (**0,414441**). Gerbang yang ambangnya ditulis dengan curiga berperilaku persis seperti yang diramalkan.

## 4. Tiga margin setipis rambut

**a. `entri_acak` lulus dengan jarak satu satuan resolusi.** p dihitung `(sebanding + 1)/(ulangan + 1)`. Hasilnya 4 dari 100 permutasi menyamai atau melampaui, jadi p = 5/101 = **0,049505**. Bila satu permutasi lagi menyamai, p = 6/101 = **0,059406** dan H-010 **GAGAL**. Resolusi pada 100 ulangan adalah 0,0099; jarak antara lulus dan gagal **tepat satu satuan resolusi**.

**b. Keunggulan atas entri acak menyusut lebih dari separuh.** Skor nyata turun dari 0,10781R (H-009) ke **0,04661R**. Entri acak memakai geometri keluar yang **identik**, jadi apa pun yang diperbaiki oleh target 8R juga dinikmati oleh entri acak. Tafsiran paling tidak menyenangkan dan paling konsisten dengan angka: sebagian besar perbaikan H-010 berasal dari **geometri keluar**, bukan dari kandungan informasi sinyalnya.

**c. Jendela positif 0,528090** terhadap ambang 0,50, turun dari 0,556180 milik H-009.

Lulus dengan tiga margin tipis pada satu run 40 simbol bukan sistem yang terbukti. Ia hipotesis yang belum berhasil dijatuhkan.

## 5. Dekomposisi eksak: dari mana kenaikan itu datang

Seluruh angka di bawah dihitung dari `gabungan` dan `diagnosa_biaya` yang sudah dikomit. Identitasnya tertutup sampai tujuh desimal, jadi ia dapat diperiksa tangan.

| Per perdagangan | H-009 | H-010 | Perubahan |
|---|---|---|---|
| Kotor R | 0,0759727 | **0,0892483** | **+17,5%** |
| Biaya transaksi | 0,0342866 | 0,0353377 | +3,1% |
| Biaya funding | 0,0003276 | 0,0008823 | **+169%** |
| Biaya total | 0,0346142 | 0,0362200 | +4,6% |
| **Bersih R** | **0,0413585** | **0,0530283** | **+28,2%** |

Uji identitas: 0,0759727 − 0,0346142 = 0,0413585 lawan 0,041359 tercatat; 0,0892483 − 0,0362200 = 0,0530283 lawan 0,0530284 tercatat. Cocok.

| Agregat | H-009 | H-010 | Perubahan |
|---|---|---|---|
| Kotor R total | 1.133,89 | **1.047,24** | **−7,6%** |
| Biaya total R | 516,62 | 425,01 | −17,7% |
| **Bersih R total** | 617,28 | **622,23** | **+0,80%** |

**Bacaan yang jujur.** Kotor per perdagangan naik 17,5%, jadi ini bukan semata penghematan biaya. Tetapi **laba total nyaris tidak bergerak** (+0,80%) sementara jumlah perdagangan turun 21,4%. Kriteria yang didaftarkan adalah ekspektasi **per perdagangan**, jadi H-010 lulus secara sah dan angkanya bukan tipuan. Namun "menghasilkan lebih banyak per perdagangan dengan berdagang jauh lebih jarang" bukan pernyataan yang sama dengan "keunggulannya membesar". Bagi akun nyata dengan modal terbatas, yang pertama tetap perbaikan nyata; bagi klaim tentang adanya keunggulan pasar, ia jauh lebih lemah daripada kenaikan 28,2% itu terdengar.

Biaya funding per perdagangan naik 169% karena pegangan memanjang, persis seperti diramalkan, tetapi tetap kecil terhadap 1R.

## 6. Dinding grid: pertanyaannya terjawab, jawabannya bernuansa

| Imbalan | Jendela | Porsi | Titik impas kotor |
|---|---|---|---|
| **8,0** | **162** | **45,51%** | 0,1111 |
| 6,0 | 96 | 26,97% | 0,1429 |
| 4,0 | 59 | 16,57% | 0,2000 |
| 2,0 | 39 | 10,96% | 0,3333 |

Jumlah 162 + 96 + 59 + 39 = 356, tepat.

Batas atas tetap pilihan modal, tetapi porsinya **45,51%, di bawah 54,5% milik H-009**. Menurut ambang yang ditulis sebelum run: penempelan **bukan** mekanis, dan dinding H-007 **memang** dinding. Rata-rata imbalan terpilih berbobot jendela 6,140, titik impasnya 0,1400 terhadap laju nyata 0,15672 — marginnya nyata tetapi tipis.

Temuan sampingan yang tidak diramalkan: **dinding `lookback` justru larut.** Di H-009 nilai 100 dipilih 133 jendela; di H-010 sebarannya 20 → 124, 55 → 116, 100 → 116, hampir seragam. Menggeser satu sumbu mengubah pilihan pada sumbu lain, jadi kedua sumbu itu tidak dapat ditafsirkan sendiri-sendiri. Utang ADR-012 §7 tentang dinding `lookback` dengan demikian **hangus**, bukan terselesaikan.

## 7. Utang yang menghalangi kesimpulan statistik

Laporan **tidak memuat sebaran R per perdagangan**, hanya rerata dan sepuluh terburuk. Tanpa simpangan baku, **galat baku ekspektasi tidak dapat dihitung**, sehingga tidak dapat dikatakan apakah 0,053028 berbeda secara berarti dari 0,041359 atau dari ambang 0,05. Saya tidak akan mengarang angka itu. Aturan 4 dan 11 keduanya menunjuk ke arah yang sama.

**Utang:** `ringkas_gabungan` wajib memuat `std_R` dan `galat_baku_R`, plus histogram R kasar. Dikerjakan sebelum hipotesis berikutnya diadjudikasi, bukan sesudahnya.

## 8. H-011 didaftarkan sekarang, sebelum satu angka pun dilihat

**Klaim yang diuji:** hasil 40 simbol pertama secara alfabet mewakili 438 simbol layak. Asumsi ini sudah berdiri sejak H-001b dan belum pernah diuji sekali pun; ADR-010 ramalan 2 sudah menyatakan ekspektasi akan **turun** pada `--limit 0`.

**Rancangan.** `lux/backtest/run_h011.py` mengimpor `LOOKBACK`, `IMBALAN`, `buat_konfig`, `DATASET`, `KUNCI_TERLARANG`, `AMBANG_CARRY_KERAS` dari `run_h010` **apa adanya**, tanpa satu pun nilai diketik ulang. Mekanismenya identik; yang berubah hanya semestanya. `--limit 0` (438 simbol) dan `--ulangan 300`.

Menaikkan ulangan dari 100 ke 300 adalah **peningkatan resolusi**, bukan pelonggaran ambang: ambang p tetap 0,05, resolusinya membaik dari 0,0099 ke 0,00332. Ditetapkan sekarang, sebelum hasil terlihat, justru karena H-010 lulus dengan jarak satu satuan resolusi.

**Kriteria utama:** ekspektasi berbobot perdagangan atas **398 simbol tertahan** (438 dikurangi 40 yang sudah diuji), dihitung tangan dari blok `per_simbol` di laporan. Tidak ada perubahan kode yang dibutuhkan untuk itu, sehingga tidak ada kode baru yang bisa menyelundupkan asumsi.

**Ramalan, dibekukan sekarang:**

1. Ekspektasi 398 simbol tertahan mendarat **0,020–0,045**, yaitu saya ramalkan **TURUN di bawah 0,05** dan H-011 **gagal**.
2. Bila ≥ 0,05 pada 398 simbol yang belum pernah disentuh, itu **bukti terkuat yang pernah dihasilkan riset ini**.
3. Bila < 0,020, hasil 40 simbol adalah **derau seleksi** dan H-010 harus diperlakukan sebagai kebetulan.
4. `entri_acak` p pada 438 simbol dengan 300 ulangan: **0,01–0,15**. p > 0,05 menjatuhkan H-011 **meskipun** ekspektasinya tinggi.
5. Perdagangan luar sampel **100.000–160.000** (penskalaan 11.734 x 438/40 = 128.487).
6. `retensi_drop_1` **≥ 0,95**: dengan 438 simbol, membuang satu simbol tidak boleh berarti banyak.
7. Durasi **15–60 menit**. Bila melewati batas 330 menit, itu timeout dan itu informasi; fallback `--ulangan 100` dan bukan pengurangan semesta.

## 9. Yang dilarang setelah hasil ini

- Menurunkan `--ulangan` bila `entri_acak` gagal di H-011. Resolusi ditetapkan sebelum melihat hasil.
- Mematok `imbalan_R` ke 8,0. Ia menang pasca-hoc, dan ADR-012 melarangnya tepat karena alasan itu.
- Menaikkan `maks_umur_bar` dari 168 untuk memperbaiki porsi tak selesai 9,54%.
- Membuang simbol merugi, membuang simbol muda, atau memakai gerbang mana pun sebagai penyaring simbol.
- Menyatakan sistem ini siap dagang. Ia lulus satu kali, pada 40 simbol, dengan tiga margin tipis, tanpa galat baku, tanpa uji semesta penuh, tanpa horizon lain, tanpa biaya dampak pasar, dan tanpa satu pun perdagangan nyata.
