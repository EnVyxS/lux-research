# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-26 12:40 WIB (versi 13)
**Tahap sekarang:** S12 — **`invarian_risiko` LULUS untuk pertama kalinya.** H-009 ditolak hanya oleh ambang ekspektasi 0,05R
**Tahap berikutnya:** ADR-010 — gerbang konsentrasi. Fragilitas terbesar sekarang bukan ekor kerugian, melainkan bahwa 10 dari 40 simbol menghasilkan lebih dari 100% laba

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
14. (S12, H-009) **Ramalan yang salah lebih murah daripada ramalan yang tidak pernah ditulis.** Dua dari tiga ramalan H-009 salah, dan justru dari kesalahan itulah aturan 13 lahir. Ramalan yang tidak ditulis tidak dapat salah, dan karena itu tidak mengajarkan apa pun.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa.

Seluruh komputasi berjalan di GitHub Actions. Mesin lokal pengguna tidak sanggup melakukan backtest penuh, dan tidak ada VM cloud karena kendala kartu kredit.

---

## 3. Fakta terverifikasi

### H-009 — DITOLAK, tetapi SEMBILAN GERBANG LULUS untuk pertama kalinya

Sumber: `reports/backtest_h009_carry_dipatok.{md,json}`, run **`30186730437`**, commit kode **`d5f18c6f`**, commit laporan **`77b7492c`**. Sidik `eac6c83305bd1069`, 12 kombinasi, 40 simbol, **155,4 detik**.

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

### FRAGILITAS BARU YANG TERUKUR — konsentrasi laba, tidak dijaga gerbang mana pun

Dari `per_simbol` di `reports/backtest_h009_carry_dipatok.json`:

| | Total R | Porsi dari +617,28 |
|---|---|---|
| ADAUSDT | 113,30 | 18,4% |
| AIOTUSDT | 60,09 | 9,7% |
| **Sepuluh simbol teratas** | **624,89** | **101,2%** |
| **Tiga puluh simbol sisanya** | **−7,61** | **−1,2%** |

**Sepuluh dari 40 simbol menghasilkan lebih dari seluruh laba; 30 sisanya secara agregat merugi.** AIOTUSDT menyumbang 60,09R dari **44 perdagangan** di **2 jendela**, ekspektasi 1,36566R per perdagangan — tiga puluh tiga kali rerata portofolio. Terburuk: ANTUSDT −61,95, ANKRUSDT −53,28, AIXBTUSDT −37,40.

**Tidak satu pun dari sembilan gerbang menilai konsentrasi.** `buy_and_hold` menghitung median per simbol dan `survivorship` menghitung porsi delisted; keduanya buta terhadap fakta bahwa keunggulan bertumpu pada beberapa simbol. Sebuah strategi yang keunggulannya lenyap bila dua simbol dibuang bukan strategi, melainkan dua perdagangan yang beruntung. Ini yang harus diukur berikutnya, dan ia **tidak butuh run baru** — datanya sudah dikomit (aturan 9).

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

**Jarak menuju kelayakan sekarang tunggal dan terukur:** 0,05000 − 0,041359 = **0,008641R**, yaitu ekspektasi harus naik **20,9%** tanpa merusak satu pun dari sembilan gerbang.

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

### MESIN BACKTEST — sembilan gerbang terpasang dan terbukti bisa lulus maupun gagal

`lux/backtest/`: `engine.py`, `gerbang.py`, `walk_forward.py`, `run_wf.py` (H-001b), `run_h002.py`, `run_h003.py`, `runner.py`, `run_keluarga.py`, `run_h007.py`, `run_h008.py`, **`run_h009.py`**. Gerbang: `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`. **Gerbang yang tidak dapat dinilai berarti GAGAL.**

Lima alasan keluar: `stop`, `target`, `umur`, `carry`, `akhir_data`. Urutan per bar: umur → carry → stop/target → entri → ekuitas. `ALASAN_TIDAK_SELESAI = ("umur", "akhir_data", "carry")`.

**Catatan tentang gerbang `funding`:** ia menilai total funding mutlak, bukan ekor. Ia lulus di H-008 (10.253,97) sementara funding justru penyebab kegagalan `invarian_risiko`, dan lulus lagi di H-009 (10.199,59) setelah penyebab itu dicabut. **Nilainya hampir tidak bergerak sementara ekor berubah drastis — bukti langsung bahwa gerbang itu buta terhadap ekor.** Perlu gerbang funding yang sadar ekor.

Pra-registrasi bersifat **sekali tulis**; nilai saringan ikut masuk ke sidik hipotesis. `hipotesis/H-009.json` terdaftar dengan sidik `eac6c83305bd`, dan ambang 0,25 ikut masuk sidik lewat `ruang_parameter.maks_carry_realisasi_R = [0.25]` meski bukan sumbu pencarian.

### DATASET TIER B PUTARAN 2 — SAH

**14.545.679 bar 1h dan 3.636.733 bar 4h**, 790 simbol, 112 celah kisi, rasio 1h:4h **3,9996**, sekitar 703 MB. Validasi 1h: 0 pelanggaran fatal, **447 simbol layak**. ADR-003 memangkas 141 simbol berekor datar, 1.081.920 bar (7,4%), universe layak v2 = **438**. Funding: 1.982.017 baris, 447 simbol, 3 celah sejati, 79,1% positif, jitter maksimum 47 ms, 295 dari 447 simbol hidup di lebih dari satu rezim kisi. Carry ekstrem: 1000WHYUSDT +60,7%/tahun, AERGOUSDT −102,6%, MYXUSDT −533,9%.

### Pengujian — `reports/tests.md`

**444 pengujian hijau** pada commit `90c550fa` (laporan `ea84ebb2`), kode keluar 0, 2,02 detik, tanpa jaringan. Diverifikasi aritmetis: 411 + 33 = 444, dan 33 tepat jumlah pengujian H-009 (21 bernama + 12 terparametrisasi), jadi tidak ada berkas yang gagal dikumpulkan secara diam-diam. Pra-terbang run H-009 mengulanginya: 444 lolos, 2,24 detik.

### Kapasitas runner dan konektivitas

4 vCPU, 15 GB RAM, 88 GB disk. **Batas 6 jam per job yang menjadi kendala, bukan disk.** H-009 selesai **155,4 detik** untuk 40 simbol dan 12 kombinasi; H-008 butuh 208,6 detik untuk 36 kombinasi. Aset 559 MB. CDN `data.binance.vision` 200; REST `fapi.binance.com` **451 permanen**.

### Batas alat agen dan solusinya

- Daftar alat GitHub yang tersedia **tidak memuat satu pun fungsi Actions** — tidak ada pembacaan run, job, langkah, atau log. **Diverifikasi di S11.**
- Agen tidak bisa membuat rilis, memicu workflow manual, atau mengunduh artifact.
- Setiap workflow diberi filter `paths` pada berkasnya sendiri; **menyunting workflow adalah satu-satunya cara memicunya.**
- **Setiap langkah yang bisa gagal wajib menulis hasilnya ke `reports/`** dengan `if: always()`. Terbayar di H-009: tabel lima langkah plus log pra-terbang membuat run terbaca penuh tanpa akses log.
- **Gerbang yang bisa gagal ditaruh sebelum unduhan, bukan sesudahnya.** Tiga pernyataan ADR-009 di langkah `impor` berjalan sebelum 559 MB diunduh.
- Sandbox agen **tidak punya jaringan**. Gerbang `pytest` wajib berjalan **sebelum** unduhan.
- **Commit laporan tanpa berkas hasil berarti run GAGAL, bukan sedang berjalan.**
- Blob laporan yang tidak berubah berarti **belum ditulis**, bukan berhasil. **SHA blob juga basi begitu ada tulisan** — `push_files` lebih aman daripada `create_or_update_file` untuk penggantian berkas utuh.

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1** (`5f222e8`): `header=0` + `skiprows=1` menghilangkan satu bar per berkas.
- **Parser 2 dan 3** (`16638b4`): BOM UTF-8; satu baris sampah menggagalkan seluruh berkas.
- **URL non-ASCII**: percent-encoding lewat `bv.seg()`.
- **Metrik celah funding**: gagal lima putaran karena mengira kisi funding tetap.
- **Circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`).
- **S10:** kurung kurawal liar di `tests/test_run_h007.py` (`c48a785`) menjatuhkan pengumpulan pytest; diperbaiki `e81e34e`.
- **S11:** langkah pra-terbang `backtest.yml` bisu; diperbaiki `245747ee`.
- **S12:** STATE v11 menaikkan kekeliruan analitis menjadi fakta ("funding bukan penyebab kerugian ekor"). Ditarik di v12, dan jurnal S11 dikoreksi di v13. Penyebabnya memakai rerata untuk menyimpulkan tentang ekor.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| Keunggulan bertahan bila simbol penyumbang terbesar dibuang | ADR-010, hitung ulang dari `per_simbol` yang sudah dikomit |
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
- "Kerugian ekor berasal dari keluar di pembukaan bar yang menganga" — **salah.** Kesepuluh perdagangan terburuk beralasan `stop` dengan kotor tepat −1R.
- "Kerugian ekor berasal dari stop yang sangat rapat" — **salah.** Lebar stop terburuk 2,83% terhadap rerata 3,61%.
- "Funding bukan penyebab kerugian ekor" (STATE v11) — **ditarik.** Funding menyumbang 46,7% kerugian terburuk.

**Dihapus di S10 karena keliru secara konstruksi:** "keunggulan Donchian berasal dari sedikit perdagangan berekor panjang".

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 (14.076.257 baris 1h, 3.506.060 baris 4h, 17.169 celah, rasio 4,014); metrik celah funding putaran 1–4 (1.380.741 · 1.193.209 · 587.131 · 266.612); seluruh run pilot H-001 termasuk `30170073890`.

---

## 5. Penghalang aktif

Tidak ada yang menghentikan pekerjaan.

Dibutuhkan dari pengguna, belum memblokir: **token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`.

---

## 6. Tindakan berikutnya

1. **ADR-010 — gerbang konsentrasi.** Sepuluh dari 40 simbol menghasilkan 101,2% laba dan 30 sisanya merugi −7,61R. Ini fragilitas paling besar yang tersisa dan **tidak dijaga satu pun dari sembilan gerbang**. Ukur dari `per_simbol` yang sudah dikomit — **tidak butuh run baru** (aturan 9). Ambang harus ditetapkan sebelum angkanya dihitung, dan bila keunggulan runtuh saat dua simbol teratas dibuang, maka H-007 sampai H-009 harus dibaca ulang sebagai hasil yang bertumpu pada dua simbol.

2. **Gerbang funding yang sadar ekor.** Gerbang sekarang menilai total mutlak dan nyaris tidak bergerak (10.253,97 → 10.199,59) sementara ekor berubah dari −1,9769R ke −1,2698R. Ia lulus di kedua keadaan, jadi ia tidak memberi informasi.

3. **Horizon 4h.** **Prasyarat mutlak: jalankan `validate.yml` untuk 4h.**

4. **Funding sebagai sinyal.** Belum pernah diuji kandungan informasi arahnya. Diperkuat oleh S12: funding terbukti bermagnitudo nyata di ekor, jadi ia bukan sekadar biaya kecil.

**Yang DILARANG:** melombakan ambang pengaman dalam bentuk apa pun; mematok `imbalan_R` ke 4,0; menghitung ulang hipotesis yang sudah divonis; melonggarkan ambang `invarian_risiko` dari −1,5R; **menurunkan ambang ekspektasi 0,05R karena H-009 nyaris mencapainya.**

Sisanya, tidak memblokir:

5. Perbaiki docstring `lux/costs.py` yang masih menyebut pembagi funding 8 jam tetap.
6. Diff terhadap Dataset G lama (528 simbol). **Satu-satunya butir dari daftar tugas awal pengguna yang benar-benar masih terbuka.**
7. `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md`; salin ADR-001 dan ADR-002 ke `decisions/`.
8. Pelapor Notion (`NOTION_TOKEN`).
9. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, dengan ≥24 shard.

---

## 7. Pengawasan otonom

Agen **LUX Gatekeeper** aktif di Notion. Terpicu saat runner membuat baris di database Run Results, menilai hasil terhadap sembilan gerbang mutu. Sudah diuji dengan baris sintetis bercacat dan menolak dengan benar. **Verdict Ditolak menghentikan pipeline.**

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
| `lux/backtest/gerbang.py` | sembilan gerbang mutu |
| `lux/backtest/walk_forward.py` | pemilihan parameter dalam sampel; konfig per kandidat opsional (ADR-007) |
| `lux/backtest/run_wf.py` | orkestrator H-001b — **jangan disunting** |
| `lux/backtest/run_h002.py` | orkestrator H-002 (ADR-004) — dibekukan |
| `lux/backtest/run_h003.py` | orkestrator H-003 (ADR-005) — dibekukan |
| `lux/backtest/runner.py` | **runner bersama**: muat sekali, jalankan, nilai, laporkan |
| `lux/backtest/run_keluarga.py` | keluarga ADR-006 (H-004, H-005, H-006) |
| `lux/backtest/run_h007.py` | H-007 struktur keluar (ADR-007) — sumber grid bersama |
| `lux/backtest/run_h008.py` | H-008 pengaman carry dilombakan (ADR-008) — dibekukan |
| `lux/backtest/run_h009.py` | **H-009 pengaman carry dipatok (ADR-009) — dibekukan.** Grid diimpor dari `run_h007`, ambang konstan, kunci pengaman haram di kandidat |
| `tests/` | **444** pengujian tanpa jaringan, wajib hijau sebelum unduhan |
| `reports/` | keluaran mesin tiap run, sumber bukti Bagian 3 |
| `hipotesis/` | pendaftaran sekali tulis: `H-001b` … **`H-009`** |
| `decisions/` | ADR-003 (ekor datar), ADR-004 (carry funding), ADR-005 (pembalikan), ADR-006 (keluarga), ADR-007 (struktur keluar), ADR-008 (pengaman carry keras), ADR-009 (batas risiko bukan parameter) |
| `journal/` | riwayat per sesi |

**Workflow aktif (10):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`. `backtest.yml` sekarang menjalankan `lux.backtest.run_h009`.

**Dihapus di S7:** `analyze_tail.yml` (`07860a7`), `diagnose.yml` (`f4af734`), `diag_datar.yml` (`41ca693`), `retry_failed.yml` (`3a206c6`).

Release **`tier-b-v1`** memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`. Pola unduh backtest wajib `ohlcv_1h_*.parquet`.
