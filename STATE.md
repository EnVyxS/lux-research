# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-26 14:35 WIB (versi 15)
**Tahap sekarang:** S12 — **gerbang kesepuluh `konsentrasi` sudah dikodekan, tersambung, dan hijau (467 pengujian).** Ramalan ketiga ADR-010 diuji dan **difalsifikasi**.
**Tahap berikutnya:** gerbang funding yang sadar ekor, lalu H-010 sebagai hipotesis pertama yang dinilai sepuluh gerbang

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
13. (S12, H-009) **Peristiwa yang terlalu jarang tidak dapat dipilih oleh pemilih dalam sampel, seberapa pun bergunanya.** Pengaman carry menyala 16 kali dari 14.925 perdagangan, yaitu 0,107%. Satu jendela latih tipikal memuat nol atau satu peristiwa semacam itu, jadi pemilih hanya melihat pemenang yang terpotong dan tidak pernah melihat bencana yang dihindari. Kelangkaan, bukan biaya, yang membuat pengaman itu ditolak 334 lawan 22 di H-008.
14. (S12, H-009) **Ramalan yang salah lebih murah daripada ramalan yang tidak pernah ditulis.** Dua dari tiga ramalan H-009 salah, dan justru dari kesalahan itulah aturan 13 lahir.
15. (S12, ADR-010) **Porsi terhadap nilai bersih bukan ukuran konsentrasi.** Bila ada penyumbang negatif, porsi penyumbang teratas terhadap total bersih hampir pasti melewati 100% tanpa ada konsentrasi sama sekali, karena penyebutnya sudah dikurangi kerugian. Konsentrasi diukur dengan **jackknife** dan dengan penyebut **bruto**. Aturan 8 seharusnya sudah menangkap ini; kekeliruan versi 13 membuktikan aturan yang diketahui tidak otomatis diterapkan.
16. (S12, ramalan umur) **Proksi yang berkorelasi 0,97 dengan hal lain bukan proksi.** Umur simbol dan jumlah perdagangan berkorelasi Spearman +0,9668, sehingga dengan 40 titik keduanya tidak dapat dipisahkan; ditambah periode kalender listing dan jenis aset yang ikut menempel. Sebelum menafsirkan korelasi antar simbol, daftar dulu apa saja yang berkorelasi dengan proksinya. Bila daftarnya panjang, hasil apa pun tidak menerangkan mekanisme.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa.

Seluruh komputasi berjalan di GitHub Actions. Mesin lokal pengguna tidak sanggup melakukan backtest penuh, dan tidak ada VM cloud karena kendala kartu kredit.

---

## 3. Fakta terverifikasi

### GERBANG KESEPULUH SUDAH HIDUP

`lux/backtest/konsentrasi.py` dan `tests/test_konsentrasi.py` dikomit di **`211fb3bd`**; penyambungan ke `gerbang.py`, `runner.py`, dan `tests/test_gerbang_kesepuluh.py` di **`8cf70f08`**. Laporan pengujian **`10732424`**: **467 lulus**, kode keluar 0, 2,27 detik. Modul berdiri hijau lebih dulu (462 lulus di `211fb3bd`), penyambungan menyusul — urutan itu disengaja.

| Yang berubah | Isinya |
|---|---|
| `NAMA_GERBANG` | sepuluh nama, `konsentrasi` di ujung |
| `LaporanGerbang.semua_lulus` | `len(self.gerbang) == len(NAMA_GERBANG)`, **bukan lagi literal `9`** |
| `runner.py` | menilai gerbang dari `ringkasan_simbol` yang belum dibulatkan, menulis tabel jackknife ke md dan `jackknife` ke JSON |
| letak gerbang | modul sendiri, sebab `konsentrasi` mengimpor `Gerbang` sehingga impor balik akan menutup siklus seperti cacat `4b77617` |

**Mengapa literal `9` berbahaya:** bila ia tertinggal saat daftar gerbang bertambah, ketertinggalannya berbentuk **kelulusan**, bukan kegagalan. Sekarang tidak mungkin lagi.

**Konsekuensi yang diterima sadar:** tiga orkestrator beku (`run_wf`, `run_h002`, `run_h003`) hanya menyusun sembilan gerbang, jadi bila dijalankan lagi laporannya gagal pada `konsentrasi`. Itu pernyataan yang benar — orkestrator itu memang tidak mengukur konsentrasi. Angka lama di `reports/` tidak berubah.

Ambang tetap ADR-010, **mengikat mulai H-010**: `drop_1_positif` > 0 · `drop_5persen_positif` > 0 atas ⌈0,05·N⌉ · `retensi_drop_1` ≥ 0,60 · `median_simbol_positif` > 0 · `porsi_bruto_teratas` ≤ 0,25 dengan penyebut laba bruto. Sub-uji yang tidak dapat dinilai berarti GAGAL.

### RAMALAN 3 ADR-010 — DIFALSIFIKASI: umur simbol tidak menerangkan apa pun

Sumber: `reports/umur_simbol.md`, commit **`bce8cf89`**. Dihitung di sandbox agen dari `per_simbol` H-009 yang sudah dikomit — nol run baru, aturan 9 terbayar keempat kalinya. Proksi umur adalah jumlah jendela walk-forward, yang ditentukan sepenuhnya oleh panjang riwayat.

| Ukuran | Nilai |
|---|---|
| Spearman(umur, ekspektasi) | **−0,0336** |
| p dua sisi, 20.000 permutasi, seed 42 | **0,8351** |
| Spearman(umur, jumlah trade) | +0,9668 |

Delapan puluh tiga persen pengacakan menghasilkan hubungan sekuat atau lebih kuat. Ini bukan efek lemah, ini ketiadaan efek. Per ember umur polanya **tidak monoton**: muda 2–4 jendela +0,056342 · menengah 5–9 **+0,068240** · tua 10–19 +0,026059 · tertua 20–24 +0,035878. Tertinggi adalah ember menengah.

**Membuang simbol muda justru menurunkan ekspektasi** dari 0,041359 ke 0,038970, makin jauh dari 0,05. Jadi tidak ada godaan yang perlu ditahan di sini.

**Asal kekeliruan dugaan ini:** dua simbol, AIOTUSDT +1,36566R atas 44 perdagangan dan 1000000BOBUSDT +0,43957R atas 58 perdagangan. Keduanya muda dan ekstrem, lalu saya menyimpulkan muda berarti untung. Itu penalaran dari **ekor sebaran**, bukan dari sebarannya — kelas yang sama dengan "rerata funding 0,0004R berarti funding tidak bersalah" dan dengan "porsi 101,2%". **Tiga kekeliruan membaca sebaran dalam satu sesi.** Bedanya, yang ketiga mati sebelum masuk STATE sebagai fakta.

### H-009 — DITOLAK, tetapi SEMBILAN GERBANG LULUS untuk pertama kalinya

Sumber: `reports/backtest_h009_carry_dipatok.{md,json}`, run **`30186730437`**, commit kode **`d5f18c6f`**, commit laporan **`77b7492c`**. Sidik `eac6c83305bd1069`, 12 kombinasi, 40 simbol, **155,4 detik**. H-009 dinilai oleh sembilan gerbang; `konsentrasi` belum ada saat itu dan **tidak diterapkan ke belakang**.

| | H-007 | H-008 | **H-009** |
|---|---|---|---|
| Ekspektasi R | +0,04044 | +0,04126 | **+0,041359** |
| Total R | +605,10 | +616,20 | **+617,28** |
| Perdagangan | 14.962 | 14.933 | **14.925** |
| Jendela positif | 199/356 | 198/356 | **198/356** |
| Keluar `carry` | — | 2 | **16** |
| `invarian_risiko` | −1,9769 GAGAL | −1,9769 GAGAL | **−1,2698 LULUS** |
| Gerbang gagal | 1 | 1 | **0** |

**Putusan: DITOLAK**, alasan tunggal `ekspektasi 0.0414R < 0.05R`. Untuk pertama kalinya dalam sembilan hipotesis, tidak ada satu pun gerbang mutu yang mengajukan keberatan. Yang menjatuhkan H-009 hanyalah ambang profitabilitas.

Sembilan gerbang: `forward_fill` 0,00025/0,3 · `buy_and_hold` 0,7333 unggul 36/40 · `entri_acak` p **0,0099** · `lookahead` 0,0 · **`invarian_risiko` −1,2698 vs −1,5** · `funding` 10.199,59 · `overlap` 0,0 · `checksum` 0,0 · `survivorship` 0,8555 (delisted 0,1250 vs 0,1461).

Alasan keluar: stop 10.242, target 4.111, `umur` 368, `akhir_data` 188, **`carry` 16**. Biaya: transaksi 0,0343R, funding 0,0003R, lebar stop 3,605%, perdagangan berbiaya melewati 1R **0** dari 14.925.

### Bukti bahwa pengaman memotong tepat sasaran, bukan menebang sembarangan

Pengaman memaksa keluar bila carry **terealisasi** melewati 0,25R. Bandingkan sepuluh terburuk H-008 dengan sepuluh terburuk H-009:

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

Kelima perdagangan yang hilang adalah **tepat** kelima yang carry-nya melewati 0,25R. Kelima yang bertahan punya carry di bawah ambang dan nilai R-nya sama sampai belasan desimal — ADAUSDT tercatat `-1.2697928364736204` di kedua run. **Nol korban sampingan.** Gerbang `invarian_risiko` sekarang bernilai persis nilai perdagangan terburuk yang carry-nya sah, yaitu −1,2698R. Ini bukan tafsiran; ini keterbacaan langsung dari dua blok `diagnosa_biaya.terburuk` yang sudah dikomit.

### Adjudikasi ramalan H-009 — dua dari tiga SALAH

Ketiga ramalan ditulis di ADR-009, di `RAMALAN`, dan di log run sebelum satu angka pun terlihat.

| Ramalan | Hasil | Putusan |
|---|---|---|
| Keluar `carry` melonjak dari 2 ke **ratusan** | **16** | **SALAH** |
| Kerugian terburuk turun di bawah 1,5R sehingga gerbang lulus | −1,2698 lulus | **BENAR** |
| Ekspektasi **turun** di bawah 0,04126R | naik ke 0,041359 | **SALAH** |

Ramalan pertama salah karena saya menaksir jumlah peristiwa ekor dari intuisi, padahal sebaran yang dibutuhkan sudah ada di laporan H-008: hanya lima dari sepuluh perdagangan terburuk yang melewati 0,25R, dan rerata funding 0,0004R. Carry di atas 0,25R itu langka. **Ini aturan 11 yang saya langgar dari arah sebaliknya:** setelah belajar bahwa rerata tidak membatasi ekor, saya lalu memakai ekor untuk menaksir frekuensi. Keduanya salah dengan cara yang sama.

Ramalan ketiga salah, dan saya sudah mengunci penanganannya di muka: bila ekspektasi naik, **curigai pengamannya tidak memicu**, jangan bersorak. Kecurigaan itu sudah diperiksa dan **gugur** — pengaman memicu 16 kali, dan tabel di atas membuktikan ia memicu pada perdagangan yang tepat.

**Yang harus dikatakan dengan jujur tentang ekspektasi:** +0,041359 terhadap +0,04126 milik H-008 adalah selisih 0,00009R. Saya menolak +0,00082R milik H-008 sebagai derau; menerima 0,00009R sebagai perbaikan berarti memakai dua timbangan. **Jadi: ekspektasi H-009 tidak berubah, tetap dalam derau.** Yang berubah nyata hanyalah ekor, dan itu nyata justru karena bisa dilacak perdagangan per perdagangan, bukan karena selisih desimalnya.

### Mengapa pemilih menolak pengaman yang ternyata gratis

Ramalan ketiga bertumpu pada klaim struktural ADR-009: pengaman risiko memakan ekspektasi, jadi pemaksimal ekspektasi selalu mematikannya. **Separuh klaim itu kini terbantah.** Di luar sampel pengaman itu **tidak memakan ekspektasi sama sekali** — biayanya nol dalam batas derau, sementara imbalannya adalah gerbang risiko yang tertutup.

Yang tetap fakta: pemilih memang mematikannya, **334 dari 356 jendela**, dan itu diukur. Penjelasan yang benar bukan biaya melainkan **kelangkaan**. Dengan 16 peristiwa pada 14.925 perdagangan, jendela latih tipikal memuat nol atau satu. Pengaman yang tidak pernah menyelamatkan apa pun di dalam sampel hanya tampak sebagai pemotong pemenang. Ini aturan 13.

Konsekuensinya lebih luas daripada carry: **setiap pengaman yang menargetkan peristiwa langka akan selalu ditolak oleh pemilihan dalam sampel.** Karena itu ADR-009 tetap berlaku bahkan lebih kuat, tetapi alasannya diperbaiki.

### KONSENTRASI LABA — klaim versi 13 DITARIK, ukuran yang benar jauh lebih tenang

Versi 13 berkas ini menyatakan sebagai fragilitas terbesar bahwa **"sepuluh dari 40 simbol menghasilkan 101,2% laba dan 30 sisanya merugi"**. Angkanya benar, tafsirannya menyesatkan **secara konstruksi**, dan ADR-010 menariknya. Sebabnya ada di penyebut:

| | Jumlah simbol | R |
|---|---|---|
| Simbol laba | **28** | **+883,62** |
| Simbol rugi | **12** | **−266,35** |
| Bersih | 40 | **+617,28** |

Porsi 624,89/617,28 mengukur laba sepuluh teratas terhadap penyebut yang sudah dipotong 266,35R kerugian. Statistik itu melewati 100% pada portofolio mana pun yang punya penyumbang negatif, termasuk yang sangat terdiversifikasi. Aturan 15.

Angka yang tidak menyesatkan, dari `per_simbol` yang sama, dihitung ulang dan diuji silang terhadap agregat yang dikomit (jumlah trade 14.925 tepat, jumlah jendela 356 tepat, jumlah R 617,2769 lawan 617,2774 karena pembulatan empat desimal per simbol):

- **28 dari 40 simbol menguntungkan (70%).**
- **Median ekspektasi per simbol +0,0325R — positif.** Simbol tipikal untung; keunggulan bukan milik ekor.
- Kuartil ekspektasi per simbol: −0,0170 · median +0,0325 · +0,1401. Rentang −0,21618 sampai +1,36566.
- **HHI atas porsi laba bruto 0,0621**, setara **16,1 simbol berbobot sama** dari 28 penyumbang.

**Ukuran yang benar adalah jackknife** — buang penyumbang teratas dan hitung ekspektasi dari nol:

| Dibuang | Simbol terakhir dibuang | Sisa trade | Sisa R | Ekspektasi | Retensi |
|---|---|---|---|---|---|
| 0 | — | 14.925 | 617,28 | **+0,041359** | 100% |
| 1 | ADAUSDT | 14.014 | 503,97 | **+0,035962** | **87,0%** |
| 2 | ALGOUSDT | 13.037 | 430,22 | +0,033000 | 79,8% |
| 3 | 1000FLOKIUSDT | 12.648 | 359,46 | +0,028420 | 68,7% |
| 4 | ALPHAUSDT | 11.966 | 293,64 | +0,024540 | 59,3% |
| 5 | AIOTUSDT | 11.922 | 233,56 | +0,019590 | 47,4% |
| 8 | 1000PEPEUSDT | 11.098 | 78,00 | +0,007028 | 17,0% |
| 10 | — | — | — | **≤ 0** | 0% |

**Membuang simbol terbaik dari empat puluh memangkas 13% ekspektasi. Membuang lima memangkas 53%. Ekspektasi menjadi nol setelah sepuluh dibuang.** Untuk 40 simbol ini kerapuhan **sedang** — bukan bencana seperti yang saya tulis di versi 13, bukan pula kesehatan.

Satu pencilan bertahan sebagai masalah nyata: **AIOTUSDT ekspektasi +1,36566R** atas 44 perdagangan di 2 jendela, 33 kali rerata portofolio; lalu **1000000BOBUSDT +0,43957R** atas 58 perdagangan di 2 jendela. Keduanya bersejarah pendek, dan uji umur di atas menunjukkan kependekan riwayat itu **bukan** penjelasannya. Terburuk: AIXBTUSDT −0,21618 · ANTUSDT −0,19240 · ACXUSDT −0,09959.

**Yang secara tegas dilarang oleh ADR-010:** membuang 12 simbol yang merugi menaikkan ekspektasi ke sekitar **0,0752R dan langsung melewati ambang 0,05R.** Itu survivorship bias telanjang — pemilihan berdasarkan hasil yang tidak dapat diketahui di muka, persis cacat yang membuat pengetahuan bot v8.4 dibuang. Angka itu dicatat agar dikenali sebagai jebakan, bukan sasaran.

Nilai H-009 bersifat deskriptif dan **tidak** menjadi vonis: `drop_1_positif` +0,03596 · `drop_5persen_positif` +0,03300 · `retensi_drop_1` 0,8695 · `median_simbol_positif` +0,0325 · `porsi_bruto_teratas` 0,1282. Seluruh lima akan lulus, dan justru karena itu ambangnya tidak boleh berlaku ke belakang.

### Papan skor sembilan hipotesis

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
| **H-009** | **pengaman carry dipatok 0,25** | **0,041359** | **tidak ada** | **DITOLAK, hanya oleh ambang 0,05R** |

**Jarak menuju kelayakan sekarang tunggal dan terukur:** 0,05000 − 0,041359 = **0,008641R**, yaitu ekspektasi harus naik **20,9%** tanpa merusak satu pun gerbang.

**Kesimpulan struktural yang bertahan:** enam percobaan pada sisi masuk menghasilkan nol perbaikan; percobaan pada sisi keluar menghasilkan +28% (H-007) lalu menutup gerbang risiko (H-009). Sisi keluar adalah arah yang punya leverage.

### PENYEBAB KEGAGALAN `invarian_risiko` — TERUKUR DAN KINI TERTUTUP

Sumber: `diagnosa_biaya.terburuk` di `reports/backtest_h008_carry_keras.json`, run `30177253467`. Perdagangan terburuk AIOTUSDT: R −1,9769 = kotor −1,0182 − transaksi 0,0359 − **funding 0,9228**. **Funding menyumbang 46,7% kerugian terburuk** dan merupakan komponen biaya terbesar di kesepuluh perdagangan terburuk, antara 5 sampai 26 kali biaya transaksi.

Dua kandidat penjelasan saya sendiri **terbantah** oleh data yang sama: stop bekerja sempurna (kesepuluhnya beralasan `stop` dengan kotor −1,0065 sampai −1,0260, tidak ada harga yang menganga), dan stop rapat bukan penyebabnya (lebar stop terburuk 2,83% terhadap rerata 3,61%).

H-009 kini **mengonfirmasi diagnosis itu secara kausal, bukan korelasional**: memotong tepat perdagangan yang carry-nya melewati 0,25R memindahkan gerbang dari −1,9769R ke −1,2698R, dan tidak mengubah apa pun yang lain.

### Mengapa ADR-008 gagal

Walk-forward memaksimalkan ekspektasi **dalam sampel**; `invarian_risiko` dinilai **setelahnya** dan tidak pernah masuk fungsi tujuan.

| Ambang `maks_carry_realisasi_R` di H-008 | Jendela memilihnya |
|---|---|
| 0,0 — mati | **334** dari 356 |
| 0,25 | 22 |
| 0,50 | **0** |

H-008 karena itu bukan uji terhadap pengaman carry, melainkan uji terhadap kesediaan pemaksimal ekspektasi memakai pengaman yang peristiwanya langka. Jawabannya tidak. Diperbaiki oleh ADR-009, dan H-009 membuktikan mekanismenya benar sejak awal.

### Temuan S10 yang tetap berlaku: yang salah adalah titik impasnya, bukan sinyalnya

Titik impas kotor `1/(1+imbalan)`: 1R 0,5000 · 2R 0,3333 · 3R 0,2500 · 4R 0,2000, dikunci `tests/test_titik_impas.py`. H-007 memanfaatkannya tanpa menyentuh sinyal: 83% jendela memilih 3R atau 4R. Di H-009 polanya bertahan — 226 dari 356 jendela memilih imbalan 4,0, dan 101 memilih 3,0.

| Hipotesis | Laju kena target | Kotor `3p−1` | Bersih tercatat | Seretan |
|---|---|---|---|---|
| H-002 | 0,36028 | +0,08084 | +0,03159 | 0,04926 |
| H-004 | 0,34151 | +0,02453 | −0,01818 | 0,04272 |
| H-005 | 0,33755 | +0,01265 | −0,03571 | 0,04836 |
| H-006 | 0,30122 | −0,09633 | −0,13449 | 0,03815 |
| H-003 | 0,26326 | −0,21021 | −0,24782 | 0,03761 |

### KELUARGA ADR-006 — DITOLAK BERTIGA

Sumber: `reports/keluarga_adr006.{md,json}`, run `30175665060`, kode `1aedb84`, laporan `c0636bf`. Ambang p diperketat ke **0,0167 (Bonferroni 0,05/3) sebelum satu angka pun terlihat**. Trend breakout **tidak diuji ulang** karena itu persis H-001b dan H-002.

**Koreksi multiplisitas terbukti bergigi:** p H-005 0,0396 akan lolos ambang biasa 0,05. H-004 membuang 58% perdagangan dan menurunkan biaya, tetapi perdagangan yang dibuang secara agregat justru yang menguntungkan. Bagian SMC lain (order block, FVG, BOS/CHoCH) tidak diuji karena tidak punya definisi mekanis.

### H-003 — pembalikan skor-z, DITOLAK telak

`reports/backtest_h003.md`, run `30175179866`. −0,24782R, 28.959 perdagangan, 25/356 jendela positif, `entri_acak` p 1,0000. Dengan H-006 gagal serupa: **pada 1h perp USDT, pembalikan jangka pendek rugi sistematis.**

### MESIN BACKTEST — sepuluh gerbang terpasang dan terbukti bisa lulus maupun gagal

`lux/backtest/`: `engine.py`, `gerbang.py`, **`konsentrasi.py`**, `walk_forward.py`, `run_wf.py` (H-001b), `run_h002.py`, `run_h003.py`, `runner.py`, `run_keluarga.py`, `run_h007.py`, `run_h008.py`, **`run_h009.py`**. Gerbang: `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`, **`konsentrasi`**. **Gerbang yang tidak dapat dinilai berarti GAGAL.**

Lima alasan keluar: `stop`, `target`, `umur`, `carry`, `akhir_data`. Urutan per bar: umur → carry → stop/target → entri → ekuitas. `ALASAN_TIDAK_SELESAI = ("umur", "akhir_data", "carry")`.

**Catatan tentang gerbang `funding`:** ia menilai total funding mutlak, bukan ekor. Ia lulus di H-008 (10.253,97) sementara funding justru penyebab kegagalan `invarian_risiko`, dan lulus lagi di H-009 (10.199,59) setelah penyebab itu dicabut. **Nilainya hampir tidak bergerak sementara ekor berubah drastis — bukti langsung bahwa gerbang itu buta terhadap ekor.** Perlu gerbang funding yang sadar ekor. **Ini tindakan berikutnya nomor satu.**

Pra-registrasi bersifat **sekali tulis**; nilai saringan ikut masuk ke sidik hipotesis. `hipotesis/H-009.json` terdaftar dengan sidik `eac6c83305bd`, dan ambang 0,25 ikut masuk sidik lewat `ruang_parameter.maks_carry_realisasi_R = [0.25]` meski bukan sumbu pencarian.

### DATASET TIER B PUTARAN 2 — SAH

**14.545.679 bar 1h dan 3.636.733 bar 4h**, 790 simbol, 112 celah kisi, rasio 1h:4h **3,9996**, sekitar 703 MB. Validasi 1h: 0 pelanggaran fatal, **447 simbol layak**. ADR-003 memangkas 141 simbol berekor datar, 1.081.920 bar (7,4%), universe layak v2 = **438**. Funding: 1.982.017 baris, 447 simbol, 3 celah sejati, 79,1% positif, jitter maksimum 47 ms, 295 dari 447 simbol hidup di lebih dari satu rezim kisi. Carry ekstrem: 1000WHYUSDT +60,7%/tahun, AERGOUSDT −102,6%, MYXUSDT −533,9%.

### Pengujian — `reports/tests.md`

**467 pengujian hijau** pada commit `8cf70f08` (laporan `10732424`), kode keluar 0, 2,27 detik, tanpa jaringan. Jejak aritmetisnya utuh: 444 (H-009) → **462** setelah 18 pengujian `test_konsentrasi.py` (`211fb3bd`) → **467** setelah 5 pengujian `test_gerbang_kesepuluh.py` (`8cf70f08`). Saya sempat menyebut "16 pengujian" untuk berkas yang berisi 18; hitungan 462 − 444 = 18 yang membetulkan label itu, bukan sebaliknya.

### Kapasitas runner dan konektivitas

4 vCPU, 15 GB RAM, 88 GB disk. **Batas 6 jam per job yang menjadi kendala, bukan disk.** H-009 selesai **155,4 detik** untuk 40 simbol dan 12 kombinasi; H-008 butuh 208,6 detik untuk 36 kombinasi. Aset 559 MB. CDN `data.binance.vision` 200; REST `fapi.binance.com` **451 permanen**.

### Batas alat agen dan solusinya

- Daftar alat GitHub yang tersedia **tidak memuat satu pun fungsi Actions** — tidak ada pembacaan run, job, langkah, atau log. **Diverifikasi di S11.**
- Agen tidak bisa membuat rilis, memicu workflow manual, atau mengunduh artifact.
- Setiap workflow diberi filter `paths` pada berkasnya sendiri; **menyunting workflow adalah satu-satunya cara memicunya.** `tests.yml` memfilter `lux/**` dan `tests/**`, jadi push kode selalu menguji dirinya sendiri.
- **Setiap langkah yang bisa gagal wajib menulis hasilnya ke `reports/`** dengan `if: always()`. Terbayar di H-009: tabel lima langkah plus log pra-terbang membuat run terbaca penuh tanpa akses log.
- **Gerbang yang bisa gagal ditaruh sebelum unduhan, bukan sesudahnya.** Tiga pernyataan ADR-009 di langkah `impor` berjalan sebelum 559 MB diunduh.
- Sandbox agen **tidak punya jaringan**. Gerbang `pytest` wajib berjalan **sebelum** unduhan.
- **Commit laporan tanpa berkas hasil berarti run GAGAL, bukan sedang berjalan.**
- Blob laporan yang tidak berubah berarti **belum ditulis**, bukan berhasil. **SHA blob juga basi begitu ada tulisan** — `push_files` lebih aman daripada `create_or_update_file` untuk penggantian berkas utuh.
- **Modul baru berdiri hijau sendiri lebih dulu, penyambungan menyusul.** Dipakai untuk `konsentrasi.py`: 462 hijau dulu di `211fb3bd`, baru `NAMA_GERBANG` disentuh di `8cf70f08`. Bila keduanya sekali push dan pytest merah, tidak akan jelas mana yang salah.
- **Sebelum menulis kode terhadap modul lain, baca modulnya.** Untuk gerbang kesepuluh: `gerbang.py`, `runner.py`, `test_gerbang.py`, `test_run_keluarga.py`, dan `test_run_wf.py` dibaca **sebelum** satu baris ditulis. Tiga berkas pengujian terakhir diperiksa khusus untuk mencari literal angka sembilan yang akan pecah; tidak ada.
- **Analisis atas laporan yang sudah dikomit dapat dikerjakan di sandbox agen tanpa jaringan.** Jackknife ADR-010 dan uji umur simbol dihitung seluruhnya dari `per_simbol`, tanpa satu pun run baru. Aturan 9 terbayar empat kali.

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1** (`5f222e8`): `header=0` + `skiprows=1` menghilangkan satu bar per berkas.
- **Parser 2 dan 3** (`16638b4`): BOM UTF-8; satu baris sampah menggagalkan seluruh berkas.
- **URL non-ASCII**: percent-encoding lewat `bv.seg()`.
- **Metrik celah funding**: gagal lima putaran karena mengira kisi funding tetap.
- **Circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`). **Alasan terdokumentasi mengapa `konsentrasi.py` berdiri sebagai modul sendiri.**
- **S10:** kurung kurawal liar di `tests/test_run_h007.py` (`c48a785`) menjatuhkan pengumpulan pytest; diperbaiki `e81e34e`.
- **S11:** langkah pra-terbang `backtest.yml` bisu; diperbaiki `245747ee`.
- **S12:** STATE v11 menaikkan kekeliruan analitis menjadi fakta ("funding bukan penyebab kerugian ekor"). Ditarik di v12, jurnal S11 dikoreksi di v13. Penyebabnya memakai rerata untuk menyimpulkan tentang ekor.
- **S12:** STATE v13 menaikkan artefak aritmetika ("sepuluh simbol menghasilkan 101,2% laba") menjadi fragilitas terbesar dan menaruhnya sebagai tindakan prioritas. Ditarik di ADR-010 dan di v14. Penyebabnya memakai penyebut bersih untuk mengukur konsentrasi.
- **S12:** dugaan "simbol muda lebih menguntungkan" lahir dari dua pencilan dan terdaftar sebagai asumsi prioritas dua di v14. Diuji di v15 dan **difalsifikasi** (rho −0,0336, p 0,8351). **Tiga kekeliruan membaca sebaran dalam satu sesi;** yang ini satu-satunya yang mati sebagai asumsi, bukan sebagai fakta.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| Keunggulan kelanjutan membesar pada horizon lebih panjang (4h) | jalankan hipotesis baru pada 4h setelah validasi 4h |
| Funding sebagai **sinyal** memuat informasi arah, bukan hanya biaya | uji hipotesis berbasis funding, belum pernah dilakukan |
| Integritas 4h sama bersihnya dengan 1h | jalankan `validate.yml` untuk interval 4h |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap universe layak v2 438 |
| Hasil 40 simbol pertama mewakili 438 simbol | jalankan `--limit 0` sekali, hanya untuk hipotesis yang layak |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |

**Turun menjadi fakta di S9:** saringan rezim tren memperbaiki breakout (**salah**, H-004); retest memperkecil biaya per R secara menguntungkan (**salah**, H-005); SMC yang dapat dikodekan punya keunggulan (**salah**, H-006).

**Terbukti di S10:** menurunkan titik impas lewat imbalan lebih besar menaikkan ekspektasi (**benar**, +28%), dan menaikkan lama pegang sehingga kerugian ekor membesar (**benar**).

**Diselesaikan di S12:**

- "Pengaman carry yang dipatok menyala membuat `invarian_risiko` lulus" — **BENAR, terukur.** −1,9769 → −1,2698.
- "Biaya menjaga risiko memakan ekspektasi" — **SALAH.** Biayanya nol dalam batas derau.
- "Keunggulan bertahan bila simbol penyumbang terbesar dibuang" — **BENAR, terukur.** Retensi drop-1 87,0%, ekspektasi tetap +0,03596R. Tetapi runtuh setelah sepuluh dibuang.
- "Ekspektasi bergantung pada umur simbol" — **SALAH, difalsifikasi.** Spearman −0,0336, p 0,8351, pola per ember tidak monoton. Asumsi **dihapus**, bukan diturunkan prioritasnya.
- "Kerugian ekor berasal dari keluar di pembukaan bar yang menganga" — **salah.** Kesepuluh perdagangan terburuk beralasan `stop` dengan kotor tepat −1R.
- "Kerugian ekor berasal dari stop yang sangat rapat" — **salah.** Lebar stop terburuk 2,83% terhadap rerata 3,61%.
- "Funding bukan penyebab kerugian ekor" (STATE v11) — **ditarik.** Funding menyumbang 46,7% kerugian terburuk.
- "Laba terkonsentrasi pada sepuluh simbol dan itu fragilitas terbesar" (STATE v13) — **ditarik.** 28 dari 40 simbol untung, median simbol +0,0325R, HHI setara 16,1 simbol.

**Dihapus di S10 karena keliru secara konstruksi:** "keunggulan Donchian berasal dari sedikit perdagangan berekor panjang".

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 (14.076.257 baris 1h, 3.506.060 baris 4h, 17.169 celah, rasio 4,014); metrik celah funding putaran 1–4 (1.380.741 · 1.193.209 · 587.131 · 266.612); seluruh run pilot H-001 termasuk `30170073890`; **porsi "101,2%" sebagai bukti konsentrasi**; **selisih ekspektasi muda-lawan-tua +0,017 sampai +0,033R sebagai efek umur** — Spearman atas 40 titik nol, dan ketiga potongan itu memakai data yang sebagian besar sama.

---

## 5. Penghalang aktif

Tidak ada yang menghentikan pekerjaan.

Dibutuhkan dari pengguna, belum memblokir: **token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`.

---

## 6. Tindakan berikutnya

1. **Gerbang funding yang sadar ekor.** Gerbang sekarang menilai total mutlak dan nyaris tidak bergerak (10.253,97 → 10.199,59) sementara ekor berubah dari −1,9769R ke −1,2698R. Ia lulus di kedua keadaan, jadi ia tidak memberi informasi. Perlu ADR lebih dulu, dengan ambang ditulis sebelum angka dilihat, dan berlaku mulai hipotesis sesudahnya. Sekalian perketat `gerbang_lulus` di `lux/funding.py`.

2. **H-010.** Hipotesis pertama yang dinilai **sepuluh** gerbang. Mekanismenya belum diputuskan dan **harus punya ADR sendiri lebih dulu**. Arah dengan leverage terbukti adalah sisi keluar, bukan sisi masuk. Jarak yang harus ditutup 0,008641R atau 20,9%.

3. **Horizon 4h.** **Prasyarat mutlak: jalankan `validate.yml` untuk 4h.**

4. **Funding sebagai sinyal.** Belum pernah diuji kandungan informasi arahnya. Diperkuat oleh S12: funding terbukti bermagnitudo nyata di ekor.

**Yang DILARANG:** membuang simbol yang merugi dari universe (naik ke ±0,0752R, survivorship bias telanjang); memakai gerbang `konsentrasi` sebagai penyaring simbol; memasukkan saringan berbasis umur simbol ke konfigurasi (sudah difalsifikasi, dan bila kelak muncul ia harus lahir dari mekanisme yang dinyatakan lebih dulu); membuang AIOTUSDT karena ekspektasinya tampak mustahil; melombakan ambang pengaman dalam bentuk apa pun; mematok `imbalan_R` ke 4,0; menghitung ulang hipotesis yang sudah divonis; melonggarkan ambang `invarian_risiko` dari −1,5R; **menurunkan ambang ekspektasi 0,05R karena H-009 nyaris mencapainya.**

Sisanya, tidak memblokir:

5. Perbaiki docstring `lux/costs.py` yang masih menyebut pembagi funding 8 jam tetap.
6. Diff terhadap Dataset G lama (528 simbol). **Satu-satunya butir dari daftar tugas awal pengguna yang benar-benar masih terbuka.**
7. `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md`; salin ADR-001 dan ADR-002 ke `decisions/`.
8. Pelapor Notion (`NOTION_TOKEN`).
9. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, dengan ≥24 shard.

---

## 7. Pengawasan otonom

Agen **LUX Gatekeeper** aktif di Notion. Terpicu saat runner membuat baris di database Run Results, menilai hasil terhadap gerbang mutu. Sudah diuji dengan baris sintetis bercacat dan menolak dengan benar. **Verdict Ditolak menghentikan pipeline.** Catatan: instruksinya masih menyebut sembilan gerbang dan perlu disesuaikan bila pelapor Notion diaktifkan.

---

## 8. Peta repo

| Path | Isi |
|---|---|
| `config/lux.yaml` | seluruh parameter yang memengaruhi hasil; `maks_carry_R 0.25` adalah asal-usul ambang H-009 |
| `lux/binance_vision.py` | klien arsip: listing S3, unduhan, checksum, percent-encoding |
| `lux/universe.py` | universe point-in-time dan klasifikasi jenis kontrak |
| `lux/ingest.py` | ingest Tier B dengan validasi per simbol |
| `lux/backfill_daily.py` | penutup celah ekor dari arsip harian |
| `lux/validate.py` · `lux/validate_run.py` | integritas OHLCV, kelayakan universe, penolak aset `_retry` |
| `lux/funding.py` · `lux/funding_check.py` | ingest funding rate dan metrik kisinya |
| `lux/funding_model.py` | jadwal funding nyata, penagihan, carry terproyeksi dan terealisasi |
| `lux/costs.py` | model biaya dalam satuan R |
| `lux/diag_datar.py` · `lux/potong_ekor.py` | diagnosis dan pemangkasan ekor datar (ADR-003) |
| `lux/praregistrasi.py` | hipotesis sekali tulis dan penilaian terhadap kriteria |
| `lux/analisis/titik_impas.py` | aritmetika titik impas atas laporan yang sudah dikomit |
| `lux/strategi/breakout_atr.py` | sinyal kelanjutan (H-001b, H-002, H-007, H-008, H-009) |
| `lux/strategi/reversi_zskor.py` | sinyal pembalikan (H-003) |
| `lux/strategi/rezim_adx.py` | ADX Wilder dan saringan rezim (H-004) |
| `lux/strategi/retest.py` | entri retest, "sniper entry" mekanis (H-005) |
| `lux/strategi/smc.py` | sapuan likuiditas, bagian SMC yang dapat dikodekan (H-006) |
| `lux/backtest/engine.py` | mesin eksekusi: stop, target, batas umur, saringan carry, pengaman carry terealisasi |
| `lux/backtest/gerbang.py` | **sembilan gerbang pertama + `NAMA_GERBANG` sepuluh nama**; `semua_lulus` memakai `len(NAMA_GERBANG)` |
| `lux/backtest/konsentrasi.py` | **gerbang kesepuluh**: `ukur_konsentrasi`, `tabel_jackknife`, `gerbang_konsentrasi`, `dari_ringkasan`, `dari_per_simbol`. Modul sendiri agar tidak ada impor sirkular |
| `lux/backtest/walk_forward.py` | pemilihan parameter dalam sampel; konfig per kandidat opsional (ADR-007) |
| `lux/backtest/run_wf.py` | orkestrator H-001b — **jangan disunting**; hanya sembilan gerbang |
| `lux/backtest/run_h002.py` | orkestrator H-002 (ADR-004) — dibekukan; hanya sembilan gerbang |
| `lux/backtest/run_h003.py` | orkestrator H-003 (ADR-005) — dibekukan; hanya sembilan gerbang |
| `lux/backtest/runner.py` | **runner bersama**: muat sekali, jalankan, nilai sepuluh gerbang, laporkan, tulis tabel jackknife |
| `lux/backtest/run_keluarga.py` | keluarga ADR-006 (H-004, H-005, H-006) |
| `lux/backtest/run_h007.py` | H-007 struktur keluar (ADR-007) — sumber grid bersama |
| `lux/backtest/run_h008.py` | H-008 pengaman carry dilombakan (ADR-008) — dibekukan |
| `lux/backtest/run_h009.py` | **H-009 pengaman carry dipatok (ADR-009) — dibekukan.** Grid diimpor dari `run_h007`, ambang konstan, kunci pengaman haram di kandidat |
| `tests/` | **467** pengujian tanpa jaringan, wajib hijau sebelum unduhan |
| `reports/` | keluaran mesin tiap run, sumber bukti Bagian 3. **`umur_simbol.md` adalah pengecualian: dihitung di sandbox agen, provenansnya tertulis di dalamnya** |
| `hipotesis/` | pendaftaran sekali tulis: `H-001b` … **`H-009`** |
| `decisions/` | ADR-003 (ekor datar), ADR-004 (carry funding), ADR-005 (pembalikan), ADR-006 (keluarga), ADR-007 (struktur keluar), ADR-008 (pengaman carry keras), ADR-009 (batas risiko bukan parameter), **ADR-010 (konsentrasi bukan keunggulan)** |
| `journal/` | riwayat per sesi |

**Workflow aktif (10):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`. `backtest.yml` sekarang menjalankan `lux.backtest.run_h009`.

**Dihapus di S7:** `analyze_tail.yml` (`07860a7`), `diagnose.yml` (`f4af734`), `diag_datar.yml` (`41ca693`), `retry_failed.yml` (`3a206c6`).

Release **`tier-b-v1`** memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`. Pola unduh backtest wajib `ohlcv_1h_*.parquet`.
