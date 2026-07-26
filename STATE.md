# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-26 14:55 WIB (versi 16)
**Tahap sekarang:** S12 — **gerbang menjadi sebelas.** `konsentrasi` (ADR-010) dan `funding_ekor` (ADR-011) terkodekan, tersambung, dan hijau: **494 pengujian** pada `114b0d7e`.
**Tahap berikutnya:** H-010 — hipotesis pertama yang dinilai sebelas gerbang. Mekanismenya belum diputuskan dan wajib punya ADR lebih dulu.

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
17. (S12, ADR-011) **Gerbang yang memberi jawaban sama pada dua keadaan yang bertolak belakang tidak memuat informasi.** Gerbang `funding` memberi 10.253,97 dan 10.199,59 — selisih setengah persen — pada dua run yang ekornya berbeda 4,4 kali dan yang gerbang risikonya berbalik. Karena itu **syarat kelayakan gerbang baru bukan "lulus di kasus baik", melainkan "memisahkan dua keadaan yang sudah diketahui berbeda"**, dan syarat itu wajib jadi pengujian, bukan sekadar keyakinan.
18. (S12, ADR-011) **Angka jumlah yang ditulis tangan hanya boleh ada di satu tempat, dan tempat itu adalah pengujian yang sengaja jadi tripwire.** Berkas pengujian gerbang kesepuluh memakai `== 10` di tiga tempat — literal yang persis dilarang oleh kode yang diujinya — dan pecah begitu gerbang kesebelas masuk. Yang benar: kode memakai `len(NAMA_GERBANG)`, pengujian memakai satu literal tunggal yang harus diubah dengan sadar.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa.

Seluruh komputasi berjalan di GitHub Actions. Mesin lokal pengguna tidak sanggup melakukan backtest penuh, dan tidak ada VM cloud karena kendala kartu kredit.

---

## 3. Fakta terverifikasi

### GERBANG KESEBELAS `funding_ekor` — HIDUP (ADR-011)

| Commit | Isi | Pengujian |
|---|---|---|
| `446a3732` | ADR-011, ambang ditulis sebelum kode | — |
| `163a7bad` | `lux/backtest/funding_ekor.py` + 21 pengujian | **488 hijau** (laporan `1a8ee96f`) |
| `114b0d7e` | `NAMA_GERBANG` sebelas, runner menilai dan melaporkan | **494 hijau** (laporan `ad691072`) |

Kedua ramalan jumlah pengujian ditulis sebelum laporan dibaca dan keduanya tepat: 467 + 21 = 488, lalu 488 + 6 = 494.

**Masalah yang diselesaikan.** Gerbang `funding` menilai total funding mutlak:

| | H-008 | H-009 | Selisih |
|---|---|---|---|
| Nilai gerbang `funding` | 10.253,97 | 10.199,59 | **−0,53%** |
| Putusan | LULUS | LULUS | sama |
| Funding pada perdagangan terburuk | **0,9228R (46,7%)** | 0,2098R (16,5%) | **−4,4×** |
| Putusan `invarian_risiko` | GAGAL | LULUS | berbalik |

Selama H-007 dan H-008, funding adalah penyebab terukur kegagalan `invarian_risiko` sementara gerbang funding melaporkan sehat. Selama dua hipotesis ia titik buta yang menyamar sebagai gerbang. Aturan 17.

**Ambang tetap, empat sub-uji, semuanya harus lulus:**

| Sub-uji | Ambang | Dasar |
|---|---|---|
| `porsi_funding_ekor_maks` | ≤ **0,35** | porsi funding terhadap kerugian, maksimum atas sepuluh terburuk |
| `funding_maks_R` | ≤ **0,50** | dua kali pengaman 0,25R, ruang satu bar kelewatan |
| `porsi_trade_di_atas_pengaman` | ≤ **0,005** | penyalaan pengaman 16/14.925 = 0,107%, kelonggaran lima kali |
| `jadwal_dimuat` | wajib | tanpa jadwal nyata ketiga besaran di atas tak berarti |

Turunan 0,35 dari konstruksi: stop kehilangan ~1,00R kotor, transaksi rerata 0,034R, pengaman mengizinkan 0,25R, jadi batas sah `0,25 / 1,284 = 0,195`; 0,35 adalah 1,8 kali batas itu untuk menampung kelewatan satu bar. **Pengungkapan wajib:** 0,35 duduk di antara dua nilai yang sudah saya lihat (0,467 H-008 dan 0,165 H-009), jadi gerbang ini **mengikat mulai H-010** dan tidak diterapkan ke belakang — perlakuan identik dengan ADR-010.

**Bukti bergigi, dikunci sebagai pengujian, bukan sebagai keyakinan:** sepuluh terburuk H-008 memberi 0,467 dan **GAGAL**; enam terburuk H-009 yang angkanya diterbitkan memberi 0,165 dan lulus.

**Tiga ramalan ADR-011, dinilai terhadap H-010:** porsi ekor H-009 akan mendarat 0,14–0,20 · `porsi_di_atas_pengaman` antara 0,00107 dan 0,005 (**sub-uji ini berisiko gagal dan itu disengaja**; bila jumlah perdagangan yang berakhir di atas 0,25R jauh melebihi penyalaan pengaman, pengamannya bocor) · `funding_maks_R` antara 0,25 dan 0,50 (di atas 0,50 berarti cacat mesin, bukan cacat gerbang).

**Yang tidak dapat diperiksa lebih awal:** sebaran funding per perdagangan **tidak ada** di laporan yang dikomit — hanya rerata dan sepuluh terburuk. Aturan 9 sudah diperiksa dan jawabannya tidak; karena itu gerbang ini memang butuh run. Berbeda dengan konsentrasi dan umur simbol yang seluruhnya dapat dihitung di sandbox.

**Gerbang `funding` lama tidak dihapus,** hanya diturunkan pangkat menjadi pemeriksaan kebersihan: ia memastikan jadwal funding nyata terpakai. Menghapusnya akan mengubah arti nama gerbang di seluruh laporan yang sudah dikomit.

### GERBANG KESEPULUH `konsentrasi` (ADR-010)

Modul di `211fb3bd` (18 pengujian, 462 hijau), penyambungan di `8cf70f08` (5 pengujian, 467 hijau, laporan `10732424`). `semua_lulus` memakai `len(NAMA_GERBANG)`, bukan literal — keuntungannya langsung terbukti saat gerbang kesebelas masuk: bagian itu tidak perlu disentuh sama sekali.

Ambang tetap ADR-010, **mengikat mulai H-010**: `drop_1_positif` > 0 · `drop_5persen_positif` > 0 atas ⌈0,05·N⌉ · `retensi_drop_1` ≥ 0,60 · `median_simbol_positif` > 0 · `porsi_bruto_teratas` ≤ 0,25 dengan penyebut laba bruto. Sub-uji yang tidak dapat dinilai berarti GAGAL.

**Konsekuensi kedua penambahan, diterima sadar:** tiga orkestrator beku (`run_wf`, `run_h002`, `run_h003`) hanya menyusun sembilan gerbang, jadi bila dijalankan lagi laporannya gagal pada `konsentrasi` dan `funding_ekor`. Itu pernyataan yang benar — orkestrator itu memang tidak mengukur keduanya. Angka lama di `reports/` tidak berubah.

### RAMALAN 3 ADR-010 — DIFALSIFIKASI: umur simbol tidak menerangkan apa pun

Sumber: `reports/umur_simbol.md`, commit **`bce8cf89`**. Dihitung di sandbox agen dari `per_simbol` H-009 yang sudah dikomit — nol run baru. Proksi umur adalah jumlah jendela walk-forward, yang ditentukan sepenuhnya oleh panjang riwayat.

| Ukuran | Nilai |
|---|---|
| Spearman(umur, ekspektasi) | **−0,0336** |
| p dua sisi, 20.000 permutasi, seed 42 | **0,8351** |
| Spearman(umur, jumlah trade) | +0,9668 |

Delapan puluh tiga persen pengacakan menghasilkan hubungan sekuat atau lebih kuat. Ini bukan efek lemah, ini ketiadaan efek. Per ember umur polanya **tidak monoton**: muda 2–4 jendela +0,056342 · menengah 5–9 **+0,068240** · tua 10–19 +0,026059 · tertua 20–24 +0,035878. Tertinggi adalah ember menengah.

**Membuang simbol muda justru menurunkan ekspektasi** dari 0,041359 ke 0,038970, makin jauh dari 0,05. Tidak ada godaan yang perlu ditahan di sini.

**Asal kekeliruan dugaan ini:** dua simbol, AIOTUSDT +1,36566R atas 44 perdagangan dan 1000000BOBUSDT +0,43957R atas 58 perdagangan. Penalaran dari **ekor sebaran**, bukan dari sebarannya — kelas yang sama dengan "rerata funding 0,0004R berarti funding tidak bersalah" dan dengan "porsi 101,2%". **Tiga kekeliruan membaca sebaran dalam satu sesi.** Yang ketiga mati sebagai asumsi, bukan sebagai fakta.

### H-009 — DITOLAK, tetapi SEMBILAN GERBANG LULUS untuk pertama kalinya

Sumber: `reports/backtest_h009_carry_dipatok.{md,json}`, run **`30186730437`**, commit kode **`d5f18c6f`**, commit laporan **`77b7492c`**. Sidik `eac6c83305bd1069`, 12 kombinasi, 40 simbol, **155,4 detik**. H-009 dinilai oleh sembilan gerbang; `konsentrasi` dan `funding_ekor` belum ada saat itu dan **tidak diterapkan ke belakang**.

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

Kelima perdagangan yang hilang adalah **tepat** kelima yang carry-nya melewati 0,25R. Kelima yang bertahan punya carry di bawah ambang dan nilai R-nya sama sampai belasan desimal — ADAUSDT tercatat `-1.2697928364736204` di kedua run. **Nol korban sampingan.** Ini bukan tafsiran; ini keterbacaan langsung dari dua blok `diagnosa_biaya.terburuk` yang sudah dikomit. Tabel inilah yang menjadi kasus uji gerbang kesebelas.

### Adjudikasi ramalan H-009 — dua dari tiga SALAH

| Ramalan | Hasil | Putusan |
|---|---|---|
| Keluar `carry` melonjak dari 2 ke **ratusan** | **16** | **SALAH** |
| Kerugian terburuk turun di bawah 1,5R sehingga gerbang lulus | −1,2698 lulus | **BENAR** |
| Ekspektasi **turun** di bawah 0,04126R | naik ke 0,041359 | **SALAH** |

Ramalan pertama salah karena saya menaksir jumlah peristiwa ekor dari intuisi, padahal sebaran yang dibutuhkan sudah ada di laporan H-008. **Aturan 11 dilanggar dari arah sebaliknya:** setelah belajar bahwa rerata tidak membatasi ekor, saya lalu memakai ekor untuk menaksir frekuensi. Keduanya salah dengan cara yang sama.

Ramalan ketiga salah, dan penanganannya sudah dikunci di muka: bila ekspektasi naik, **curigai pengamannya tidak memicu**. Kecurigaan itu diperiksa dan **gugur** — pengaman memicu 16 kali pada perdagangan yang tepat.

**Tentang ekspektasi, dengan jujur:** +0,041359 terhadap +0,04126 adalah selisih 0,00009R. Saya menolak +0,00082R milik H-008 sebagai derau; menerima 0,00009R sebagai perbaikan berarti memakai dua timbangan. **Ekspektasi H-009 tidak berubah.** Yang berubah nyata hanyalah ekor.

### Mengapa pemilih menolak pengaman yang ternyata gratis

Klaim struktural ADR-009 — pengaman risiko memakan ekspektasi — **separuhnya terbantah**: di luar sampel pengaman itu tidak memakan ekspektasi sama sekali. Yang tetap fakta: pemilih mematikannya **334 dari 356 jendela**. Penjelasan yang benar bukan biaya melainkan **kelangkaan**: 16 peristiwa pada 14.925 perdagangan, jendela latih tipikal memuat nol atau satu. Aturan 13.

Konsekuensinya lebih luas daripada carry: **setiap pengaman yang menargetkan peristiwa langka akan selalu ditolak oleh pemilihan dalam sampel.** ADR-009 tetap berlaku, bahkan lebih kuat, dengan alasan yang diperbaiki.

### KONSENTRASI LABA — klaim versi 13 DITARIK, ukuran yang benar jauh lebih tenang

Versi 13 menyatakan sebagai fragilitas terbesar bahwa **"sepuluh dari 40 simbol menghasilkan 101,2% laba"**. Angkanya benar, tafsirannya menyesatkan **secara konstruksi**. Sebabnya ada di penyebut:

| | Jumlah simbol | R |
|---|---|---|
| Simbol laba | **28** | **+883,62** |
| Simbol rugi | **12** | **−266,35** |
| Bersih | 40 | **+617,28** |

Porsi 624,89/617,28 mengukur laba sepuluh teratas terhadap penyebut yang sudah dipotong 266,35R kerugian; statistik itu melewati 100% pada portofolio mana pun yang punya penyumbang negatif. Aturan 15.

Angka yang tidak menyesatkan, diuji silang terhadap agregat yang dikomit (trade 14.925 tepat, jendela 356 tepat, R 617,2769 lawan 617,2774 karena pembulatan):

- **28 dari 40 simbol menguntungkan (70%).**
- **Median ekspektasi per simbol +0,0325R — positif.**
- Kuartil: −0,0170 · +0,0325 · +0,1401. Rentang −0,21618 sampai +1,36566.
- **HHI atas porsi laba bruto 0,0621**, setara **16,1 simbol berbobot sama**.

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

Membuang satu simbol terbaik memangkas 13%; lima memangkas 53%; sepuluh menghabiskannya. Kerapuhan **sedang**.

Pencilan yang bertahan sebagai masalah: **AIOTUSDT +1,36566R** atas 44 perdagangan, lalu **1000000BOBUSDT +0,43957R** atas 58 perdagangan. Keduanya bersejarah pendek, dan uji umur menunjukkan kependekan riwayat itu **bukan** penjelasannya. Terburuk: AIXBTUSDT −0,21618 · ANTUSDT −0,19240 · ACXUSDT −0,09959.

**Dilarang tegas:** membuang 12 simbol merugi menaikkan ekspektasi ke sekitar **0,0752R dan melewati ambang 0,05R.** Survivorship bias telanjang — dicatat agar dikenali sebagai jebakan, bukan sasaran.

Nilai deskriptif H-009 (bukan vonis): `drop_1_positif` +0,03596 · `drop_5persen_positif` +0,03300 · `retensi_drop_1` 0,8695 · `median_simbol_positif` +0,0325 · `porsi_bruto_teratas` 0,1282. Kelimanya akan lulus, dan justru karena itu ambangnya tidak berlaku ke belakang.

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

**Jarak menuju kelayakan:** 0,05000 − 0,041359 = **0,008641R**, yaitu ekspektasi harus naik **20,9%** tanpa merusak satu pun gerbang — sekarang sebelas gerbang.

**Kesimpulan struktural yang bertahan:** enam percobaan pada sisi masuk menghasilkan nol perbaikan; percobaan pada sisi keluar menghasilkan +28% (H-007) lalu menutup gerbang risiko (H-009). Sisi keluar adalah arah yang punya leverage.

### PENYEBAB KEGAGALAN `invarian_risiko` — TERUKUR DAN KINI TERTUTUP

Sumber: `diagnosa_biaya.terburuk` di `reports/backtest_h008_carry_keras.json`, run `30177253467`. Perdagangan terburuk AIOTUSDT: R −1,9769 = kotor −1,0182 − transaksi 0,0359 − **funding 0,9228**. **Funding menyumbang 46,7% kerugian terburuk** dan merupakan komponen biaya terbesar di kesepuluh perdagangan terburuk, antara 5 sampai 26 kali biaya transaksi.

Dua kandidat penjelasan saya sendiri **terbantah** oleh data yang sama: stop bekerja sempurna (kesepuluhnya beralasan `stop`, kotor −1,0065 sampai −1,0260), dan stop rapat bukan penyebabnya (lebar stop terburuk 2,83% terhadap rerata 3,61%).

H-009 **mengonfirmasi diagnosis itu secara kausal**: memotong tepat perdagangan yang carry-nya melewati 0,25R memindahkan gerbang dari −1,9769R ke −1,2698R tanpa mengubah apa pun yang lain.

### Mengapa ADR-008 gagal

Walk-forward memaksimalkan ekspektasi **dalam sampel**; `invarian_risiko` dinilai **setelahnya** dan tidak pernah masuk fungsi tujuan.

| Ambang `maks_carry_realisasi_R` di H-008 | Jendela memilihnya |
|---|---|
| 0,0 — mati | **334** dari 356 |
| 0,25 | 22 |
| 0,50 | **0** |

H-008 bukan uji terhadap pengaman carry, melainkan uji terhadap kesediaan pemaksimal ekspektasi memakai pengaman yang peristiwanya langka. Jawabannya tidak.

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

### MESIN BACKTEST — sebelas gerbang terpasang dan terbukti bisa lulus maupun gagal

`lux/backtest/`: `engine.py`, `gerbang.py`, `konsentrasi.py`, **`funding_ekor.py`**, `walk_forward.py`, `run_wf.py` (H-001b), `run_h002.py`, `run_h003.py`, `runner.py`, `run_keluarga.py`, `run_h007.py`, `run_h008.py`, `run_h009.py`.

Gerbang: `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`, `konsentrasi`, **`funding_ekor`**. **Gerbang yang tidak dapat dinilai berarti GAGAL.**

Lima alasan keluar: `stop`, `target`, `umur`, `carry`, `akhir_data`. Urutan per bar: umur → carry → stop/target → entri → ekuitas. `ALASAN_TIDAK_SELESAI = ("umur", "akhir_data", "carry")`.

Laporan runner sekarang memuat bagian **Sebelas gerbang**, **Jackknife konsentrasi (ADR-010)**, dan **Ekor funding (ADR-011)**; JSON memuat `jackknife` dan `ekor_funding`. Gerbang kesebelas memakai `rincian_R` yang sama dengan `diagnosa_biaya`, sehingga angkanya dapat diperiksa tangan terhadap blok terburuk di laporan yang sama.

Pra-registrasi bersifat **sekali tulis**; nilai saringan ikut masuk ke sidik hipotesis. `hipotesis/H-009.json` terdaftar dengan sidik `eac6c83305bd`, dan ambang 0,25 ikut masuk sidik lewat `ruang_parameter.maks_carry_realisasi_R = [0.25]` meski bukan sumbu pencarian.

### DATASET TIER B PUTARAN 2 — SAH

**14.545.679 bar 1h dan 3.636.733 bar 4h**, 790 simbol, 112 celah kisi, rasio 1h:4h **3,9996**, sekitar 703 MB. Validasi 1h: 0 pelanggaran fatal, **447 simbol layak**. ADR-003 memangkas 141 simbol berekor datar, 1.081.920 bar (7,4%), universe layak v2 = **438**. Funding: 1.982.017 baris, 447 simbol, 3 celah sejati, 79,1% positif, jitter maksimum 47 ms, 295 dari 447 simbol hidup di lebih dari satu rezim kisi. Carry ekstrem: 1000WHYUSDT +60,7%/tahun, AERGOUSDT −102,6%, MYXUSDT −533,9%.

### Pengujian — `reports/tests.md`

**494 pengujian hijau** pada commit `114b0d7e` (laporan `ad691072`), kode keluar 0, 1,90 detik, tanpa jaringan. Jejak aritmetisnya utuh dan setiap langkahnya diramalkan lebih dulu: 444 (H-009) → **462** (+18 `test_konsentrasi.py`) → **467** (+5 `test_gerbang_kesepuluh.py`) → **488** (+21 `test_funding_ekor.py`) → **494** (+6 `test_gerbang_kesebelas.py`).

### Kapasitas runner dan konektivitas

4 vCPU, 15 GB RAM, 88 GB disk. **Batas 6 jam per job yang menjadi kendala, bukan disk.** H-009 selesai **155,4 detik** untuk 40 simbol dan 12 kombinasi; H-008 butuh 208,6 detik untuk 36 kombinasi. Aset 559 MB. CDN `data.binance.vision` 200; REST `fapi.binance.com` **451 permanen**.

### Batas alat agen dan solusinya

- Daftar alat GitHub yang tersedia **tidak memuat satu pun fungsi Actions** — tidak ada pembacaan run, job, langkah, atau log. **Diverifikasi di S11.**
- `search_code` **tidak berguna di repo ini**: kueri atas berkas yang jelas-jelas ada mengembalikan nol hasil, indeksnya belum memuat repo muda. Baca berkas langsung.
- Agen tidak bisa membuat rilis, memicu workflow manual, atau mengunduh artifact.
- Setiap workflow diberi filter `paths` pada berkasnya sendiri. `tests.yml` memfilter `lux/**` dan `tests/**`, jadi push kode selalu menguji dirinya sendiri.
- **Setiap langkah yang bisa gagal wajib menulis hasilnya ke `reports/`** dengan `if: always()`.
- **Gerbang yang bisa gagal ditaruh sebelum unduhan, bukan sesudahnya.**
- Sandbox agen **tidak punya jaringan**. Gerbang `pytest` wajib berjalan **sebelum** unduhan.
- **Commit laporan tanpa berkas hasil berarti run GAGAL, bukan sedang berjalan.**
- Blob laporan yang tidak berubah berarti **belum ditulis**, bukan berhasil — penyambungan gerbang kesebelas butuh **tiga** pengambilan sebelum laporannya muncul. **SHA blob juga basi begitu ada tulisan**; `push_files` lebih aman daripada `create_or_update_file`.
- **Modul baru berdiri hijau sendiri lebih dulu, penyambungan menyusul.** Dipakai dua kali: `konsentrasi.py` (462 lalu 467) dan `funding_ekor.py` (488 lalu 494).
- **Sebelum menulis kode terhadap modul lain, baca modulnya.** Untuk gerbang kesebelas: `gerbang.py`, `runner.py`, `run_wf.py`, dan `test_gerbang_kesepuluh.py` dibaca **sebelum** satu baris ditulis. Pembacaan terakhir itulah yang menemukan literal `== 10` yang akan pecah.
- **Analisis atas laporan yang sudah dikomit dapat dikerjakan di sandbox agen tanpa jaringan** — tetapi tidak selalu bisa: sebaran funding per perdagangan tidak ada di laporan, hanya rerata dan sepuluh terburuk, jadi gerbang kesebelas memang menunggu run.

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1** (`5f222e8`): `header=0` + `skiprows=1` menghilangkan satu bar per berkas.
- **Parser 2 dan 3** (`16638b4`): BOM UTF-8; satu baris sampah menggagalkan seluruh berkas.
- **URL non-ASCII**: percent-encoding lewat `bv.seg()`.
- **Metrik celah funding**: gagal lima putaran karena mengira kisi funding tetap.
- **Circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`). **Alasan terdokumentasi mengapa `konsentrasi.py` dan `funding_ekor.py` berdiri sebagai modul sendiri.**
- **S10:** kurung kurawal liar di `tests/test_run_h007.py` (`c48a785`); diperbaiki `e81e34e`.
- **S11:** langkah pra-terbang `backtest.yml` bisu; diperbaiki `245747ee`.
- **S12:** STATE v11 menaikkan kekeliruan analitis menjadi fakta ("funding bukan penyebab kerugian ekor"). Ditarik di v12. Penyebabnya memakai rerata untuk menyimpulkan tentang ekor.
- **S12:** STATE v13 menaikkan artefak aritmetika ("sepuluh simbol menghasilkan 101,2% laba") menjadi fragilitas terbesar. Ditarik di ADR-010 dan v14. Penyebabnya penyebut bersih.
- **S12:** dugaan "simbol muda lebih menguntungkan" lahir dari dua pencilan, terdaftar sebagai asumsi prioritas di v14, difalsifikasi di v15.
- **S12:** `tests/test_gerbang_kesepuluh.py` yang saya tulis sendiri memakai literal `== 10` di tiga tempat, di berkas yang menguji kode yang justru melarang literal semacam itu. Pecah saat gerbang kesebelas masuk, ditemukan lewat pembacaan sebelum menulis, diperbaiki di `114b0d7e`. Aturan 18.

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
| Sub-uji `porsi_trade_di_atas_pengaman` ≤ 0,005 dapat dipenuhi mesin sekarang | ramalan ADR-011, dinilai pada run H-010 |

**Turun menjadi fakta di S9:** saringan rezim tren memperbaiki breakout (**salah**, H-004); retest memperkecil biaya per R secara menguntungkan (**salah**, H-005); SMC yang dapat dikodekan punya keunggulan (**salah**, H-006).

**Terbukti di S10:** menurunkan titik impas lewat imbalan lebih besar menaikkan ekspektasi (**benar**, +28%), dan menaikkan lama pegang sehingga kerugian ekor membesar (**benar**).

**Diselesaikan di S12:**

- "Pengaman carry yang dipatok menyala membuat `invarian_risiko` lulus" — **BENAR, terukur.** −1,9769 → −1,2698.
- "Biaya menjaga risiko memakan ekspektasi" — **SALAH.** Biayanya nol dalam batas derau.
- "Keunggulan bertahan bila simbol penyumbang terbesar dibuang" — **BENAR, terukur.** Retensi drop-1 87,0%. Runtuh setelah sepuluh dibuang.
- "Ekspektasi bergantung pada umur simbol" — **SALAH, difalsifikasi.** Spearman −0,0336, p 0,8351, pola tidak monoton. Asumsi **dihapus**.
- "Kerugian ekor berasal dari keluar di pembukaan bar yang menganga" — **salah.**
- "Kerugian ekor berasal dari stop yang sangat rapat" — **salah.**
- "Funding bukan penyebab kerugian ekor" (STATE v11) — **ditarik.** 46,7% kerugian terburuk.
- "Laba terkonsentrasi pada sepuluh simbol dan itu fragilitas terbesar" (STATE v13) — **ditarik.**
- "Gerbang funding yang ada memantau biaya funding" — **salah.** Ia hanya memastikan funding dihitung; ADR-011 menyatakan batas itu tegas dan menambahkan gerbang yang benar-benar menilai ekor.

**Dihapus di S10 karena keliru secara konstruksi:** "keunggulan Donchian berasal dari sedikit perdagangan berekor panjang".

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 (14.076.257 baris 1h, 3.506.060 baris 4h, 17.169 celah, rasio 4,014); metrik celah funding putaran 1–4 (1.380.741 · 1.193.209 · 587.131 · 266.612); seluruh run pilot H-001 termasuk `30170073890`; **porsi "101,2%" sebagai bukti konsentrasi**; **selisih ekspektasi muda-lawan-tua +0,017 sampai +0,033R sebagai efek umur**; **nilai gerbang `funding` (10.253,97 / 10.199,59) sebagai bukti funding aman.**

---

## 5. Penghalang aktif

Tidak ada yang menghentikan pekerjaan.

Dibutuhkan dari pengguna, belum memblokir: **token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`.

---

## 6. Tindakan berikutnya

1. **H-010.** Hipotesis pertama yang dinilai **sebelas** gerbang. Mekanismenya belum diputuskan dan **wajib punya ADR sendiri lebih dulu**, dengan ramalan tertulis sebelum run. Arah dengan leverage terbukti adalah **sisi keluar**, bukan sisi masuk: enam percobaan sisi masuk memberi nol, dua percobaan sisi keluar memberi +28% dan menutup gerbang risiko. Jarak yang harus ditutup **0,008641R atau 20,9%**.

2. **Horizon 4h.** **Prasyarat mutlak: jalankan `validate.yml` untuk 4h.**

3. **Funding sebagai sinyal.** Belum pernah diuji kandungan informasi arahnya. Diperkuat oleh S12: funding bermagnitudo nyata di ekor.

**Yang DILARANG:** membuang simbol yang merugi dari universe (naik ke ±0,0752R, survivorship bias telanjang); memakai gerbang `konsentrasi` atau `funding_ekor` sebagai penyaring simbol; memasukkan saringan berbasis umur simbol (sudah difalsifikasi); membuang AIOTUSDT karena ekspektasinya tampak mustahil; melombakan ambang pengaman dalam bentuk apa pun; mematok `imbalan_R` ke 4,0; menghitung ulang hipotesis yang sudah divonis; melonggarkan ambang `invarian_risiko` dari −1,5R; **melonggarkan ambang ADR-011 bila salah satu sub-ujinya gagal di H-010** — kegagalan itu temuan tentang mesin, bukan tentang ambang; **menurunkan ambang ekspektasi 0,05R karena H-009 nyaris mencapainya.**

Sisanya, tidak memblokir:

4. Perketat `lux/funding.py::gerbang_lulus`, yang masih terlalu longgar dan berdiri di jalur ingest. Utang yang diakui ADR-011, sengaja tidak dikerjakan bersamaan agar satu perubahan menguji satu hal.
5. Perbaiki docstring `lux/costs.py` yang masih menyebut pembagi funding 8 jam tetap.
6. Diff terhadap Dataset G lama (528 simbol). **Satu-satunya butir dari daftar tugas awal pengguna yang benar-benar masih terbuka.**
7. `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md`; salin ADR-001 dan ADR-002 ke `decisions/`.
8. Pelapor Notion (`NOTION_TOKEN`).
9. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, dengan ≥24 shard.

---

## 7. Pengawasan otonom

Agen **LUX Gatekeeper** aktif di Notion. Terpicu saat runner membuat baris di database Run Results, menilai hasil terhadap gerbang mutu. Sudah diuji dengan baris sintetis bercacat dan menolak dengan benar. **Verdict Ditolak menghentikan pipeline.** Catatan: instruksinya masih menyebut sembilan gerbang dan perlu disesuaikan menjadi sebelas bila pelapor Notion diaktifkan.

---

## 8. Peta repo

| Path | Isi |
|---|---|
| `config/lux.yaml` | seluruh parameter yang memengaruhi hasil; `maks_carry_R 0.25` adalah asal-usul ambang H-009 dan acuan ADR-011 |
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
| `lux/strategi/breakout_atr.py` | sinyal kelanjutan (H-001b, H-002, H-007, H-008, H-009) |
| `lux/strategi/reversi_zskor.py` | sinyal pembalikan (H-003) |
| `lux/strategi/rezim_adx.py` | ADX Wilder dan saringan rezim (H-004) |
| `lux/strategi/retest.py` | entri retest, "sniper entry" mekanis (H-005) |
| `lux/strategi/smc.py` | sapuan likuiditas, bagian SMC yang dapat dikodekan (H-006) |
| `lux/backtest/engine.py` | mesin eksekusi: stop, target, batas umur, saringan carry, pengaman carry terealisasi |
| `lux/backtest/gerbang.py` | sembilan gerbang pertama + `NAMA_GERBANG` sebelas nama; `semua_lulus` memakai `len(NAMA_GERBANG)` |
| `lux/backtest/konsentrasi.py` | **gerbang kesepuluh**: `ukur_konsentrasi`, `tabel_jackknife`, `gerbang_konsentrasi`, `dari_ringkasan` |
| `lux/backtest/funding_ekor.py` | **gerbang kesebelas**: `ukur_funding_ekor`, `tabel_ekor_funding`, `gerbang_funding_ekor`, `dari_rincian`, `porsi_funding` |
| `lux/backtest/walk_forward.py` | pemilihan parameter dalam sampel; konfig per kandidat opsional (ADR-007) |
| `lux/backtest/run_wf.py` | orkestrator H-001b — **jangan disunting**; sumber `rincian_R` dan `diagnosa_biaya` |
| `lux/backtest/run_h002.py` · `run_h003.py` | orkestrator beku; hanya sembilan gerbang |
| `lux/backtest/runner.py` | **runner bersama**: muat sekali, jalankan, nilai sebelas gerbang, tulis jackknife dan ekor funding |
| `lux/backtest/run_keluarga.py` | keluarga ADR-006 (H-004, H-005, H-006) |
| `lux/backtest/run_h007.py` | H-007 struktur keluar (ADR-007) — sumber grid bersama |
| `lux/backtest/run_h008.py` · `run_h009.py` | H-008 dan H-009 — dibekukan |
| `tests/` | **494** pengujian tanpa jaringan, wajib hijau sebelum unduhan. Jumlah gerbang ditulis sebagai angka **hanya** di `test_gerbang_kesebelas.py` |
| `reports/` | keluaran mesin tiap run. **`umur_simbol.md` adalah pengecualian: dihitung di sandbox agen, provenansnya tertulis di dalamnya** |
| `hipotesis/` | pendaftaran sekali tulis: `H-001b` … **`H-009`** |
| `decisions/` | ADR-003 … ADR-010, **ADR-011 (gerbang funding sadar ekor)** |
| `journal/` | riwayat per sesi |

**Workflow aktif (10):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`. `backtest.yml` sekarang menjalankan `lux.backtest.run_h009`.

**Dihapus di S7:** `analyze_tail.yml` (`07860a7`), `diagnose.yml` (`f4af734`), `diag_datar.yml` (`41ca693`), `retry_failed.yml` (`3a206c6`).

Release **`tier-b-v1`** memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`. Pola unduh backtest wajib `ohlcv_1h_*.parquet`.
