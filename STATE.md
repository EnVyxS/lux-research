# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-26 05:00 WIB (versi 10)
**Tahap sekarang:** S10 **SELESAI** — tujuh hipotesis divonis; **H-007 adalah hasil terbaik yang pernah diukur (+0,0404R)** dan tetap DITOLAK
**Tahap berikutnya:** S11 — arah leverage sudah ditemukan (struktur keluar), yang menghalangi kini gerbang `invarian_risiko`, bukan ekspektasi

---

## 1. Aturan membaca berkas ini

Bagian 3 adalah **fakta**: setiap baris punya bukti berupa commit, run ID, atau kutipan dokumentasi. Bagian 4 adalah **asumsi**: belum diukur, dan dilarang diperlakukan sebagai fakta. Memindahkan baris dari Bagian 4 ke Bagian 3 hanya boleh dengan bukti terlampir.

Lima aturan yang lahir dari kesalahan nyata, bukan dari teori:

1. **Angka yang lulus gerbang belum tentu benar.** Rasio 1h:4h 4,014 pernah dicatat sebagai uji silang yang lulus, padahal sedang melaporkan bug. Gerbang hanya menangkap cacat yang bentuknya sudah dibayangkan.
2. **Sha laporan yang tidak berubah bukan tanda pekerjaan masih berjalan.** Sekali disimpulkan ingest "masih berjalan" padahal job sudah mati merah 21 menit sebelumnya, dan yang menemukan pengguna.
3. **Penjelasan yang membuat anomali terasa wajar harus dicurigai lebih keras daripada anomalinya.**
4. **Lihat sebaran mentah sebelum berteori.** Metrik celah funding gagal lima putaran; satu tabel histogram di awal akan menyelesaikannya dalam satu putaran.
5. **Hipotesis yang ditolak tetap ditolak.** Ambang tidak disetel ulang setelah hasil terlihat; yang boleh dilakukan hanyalah mendaftarkan hipotesis baru dengan ID baru.

Aturan keenam (S8): **percobaan yang dirancang agar informatif ke dua arah lebih berharga daripada percobaan yang dirancang agar berhasil.**

Aturan ketujuh (S9): **saringan yang membuang perdagangan tidak otomatis membuang perdagangan yang buruk.** ADX ≥ 30 membuang 58% perdagangan H-002 dan menjungkirkan tandanya.

Aturan kedelapan, lahir di S10 dan yang paling memalukan sejauh ini: **periksa apakah dugaanmu mungkin secara konstruksi sebelum menjadwalkannya sebagai penelitian.** STATE v9 menulis bahwa keunggulan Donchian mungkin berasal dari segelintir perdagangan berekor panjang, lalu menjadikannya tindakan berikutnya. Mesin ini keluar pada target atau stop, sehingga sisi kanan sebarannya **terpotong secara desain** dan ekor panjang mustahil ada. Dugaan itu dapat dijatuhkan oleh aritmetika di atas angka yang sudah dikomit, tanpa run apa pun. Yang menyelamatkan sesi ini bukan pengukuran baru, melainkan membaca ulang mesin sendiri.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa.

Seluruh komputasi berjalan di GitHub Actions. Mesin lokal pengguna tidak sanggup melakukan backtest penuh, dan tidak ada VM cloud karena kendala kartu kredit.

---

## 3. Fakta terverifikasi

### HASIL RISET TERBARU — H-007 DITOLAK, TETAPI TERBAIK DARI TUJUH

Sumber: `reports/backtest_h007_keluar.{md,json}`, `reports/titik_impas.{md,json}`, run **`30176317156`**, commit kode `e81e34e`, commit workflow `1970f6b`, commit laporan `af72991`. ADR-007. Sidik `7f5e7aeeaa29284b`, 12 kombinasi, 51,5 detik.

**Ekspektasi +0,04044R**, total **+605,10R**, 14.962 perdagangan, **199/356** jendela positif. Alasan keluar: target 4.125, stop 10.276, `umur` 371, `akhir_data` 190.

Ditolak karena dua hal, dan keduanya harus dinyatakan terpisah:

- Kriteria pra-registrasi: **0,0404R < 0,05R**.
- Gerbang **`invarian_risiko` GAGAL** pada −1,977R terhadap ambang −1,5R.

Delapan gerbang lain lulus, termasuk `entri_acak` p **0,0099** dan `buy_and_hold` unggul di **36 dari 40** simbol — keunggulan terhadap beli-dan-tahan yang terbaik yang pernah tercatat.

### Temuan utama S10: yang salah selama ini adalah titik impasnya, bukan sinyalnya

Enam hipotesis pertama semuanya menggeser laju kena target sambil membiarkan stop 1R dan target 2R tidak tersentuh. Dibongkar dari histogram alasan keluar yang sudah dikomit — **tanpa satu run pun** — keenam hasilnya terurut sempurna menurut satu angka saja:

| Hipotesis | Laju kena target | Kotor `3p−1` | Bersih tercatat | Seretan |
|---|---|---|---|---|
| H-002 | **0,36028** | +0,08084 | **+0,03159** | 0,04926 |
| H-004 | 0,34151 | +0,02453 | −0,01818 | 0,04272 |
| H-005 | 0,33755 | +0,01265 | −0,03571 | 0,04836 |
| H-006 | 0,30122 | −0,09633 | −0,13449 | 0,03815 |
| H-003 | 0,26326 | −0,21021 | −0,24782 | 0,03761 |

Titik impas kotor pada imbalan 2R adalah tepat **1/3**. H-002 melampauinya hanya **2,70 poin persen**, dan untuk mencapai 0,05R dibutuhkan **0,61 poin persen** lagi — sekitar 114 pemenang tambahan dari 18.616 perdagangan yang selesai. Aritmetika ini dikunci pengujian di `tests/test_titik_impas.py`, bukan sekadar ditulis di prosa.

Karena titik impas kotor adalah `1/(1+imbalan)`, ia dapat digeser langsung: 3R menurunkannya ke 0,250, 4R ke 0,200. Itulah yang diuji H-007, **tanpa menyentuh sinyal sama sekali**.

### Hasilnya searah dengan ramalan, dan pemilihan dalam sampel menegaskannya sendiri

Walk-forward bebas memilih dari 12 kombinasi. Yang dipilihnya:

| Imbalan | Jendela memilihnya |
|---|---|
| 4,0R | **194** dari 356 |
| 3,0R | 101 |
| 2,0R | 38 |
| 1,0R | 23 |

**83% jendela memilih 3R atau 4R.** Pemilihan itu terjadi di dalam sampel, tanpa melihat data penilaian, dan hasilnya di luar sampel ikut membaik. Laju kena target turun ke **0,2864** persis seperti diramalkan ADR-007, tetapi titik impasnya turun lebih cepat.

Dibandingkan H-002 pada kerangka, dataset, universe, dan kode penilaian yang identik:

| | H-002 | H-007 |
|---|---|---|
| Ekspektasi R | +0,03159 | **+0,04044** (+28%) |
| Total R | +596,44 | **+605,10** |
| Perdagangan | 18.883 | 14.962 |
| Jendela positif | 212/356 | 199/356 |
| Unggul vs beli-tahan | 34/40 | **36/40** |
| Rerata biaya transaksi | 0,0345R | 0,0343R |

**Total R yang lebih besar dari 21% lebih sedikit perdagangan.** Untuk pertama kalinya sesuatu benar-benar menaikkan keunggulan, dan yang menaikkannya bukan sinyal baru melainkan mesin keluar.

### Harga yang dibayar, dan mengapa ia menjatuhkan gerbang

Target yang lebih jauh menahan posisi lebih lama. Keluar karena `umur` melonjak dari 103 (H-002) ke **371**, dan `akhir_data` dari 164 ke **190**. Posisi yang dipegang lebih lama menagih funding lebih banyak, dan kerugian terburuk membesar ke **−1,977R** — melewati ambang `invarian_risiko`.

Ini bukan kejutan acak melainkan konsekuensi mekanis: **menurunkan titik impas dengan target yang lebih jauh memindahkan tekanan dari laju kena target ke lama pegang, dan lama pegang adalah tepat jalur yang membuat ADR-004 gagal sebelumnya.** Saringan carry ADR-004 tetap aktif di H-007 dan tetap tembus, karena ia adalah **proyeksi rerata 30 hari, bukan jaminan**.

### Papan skor tujuh hipotesis

| ID | Mekanisme | Ekspektasi R | Putusan |
|---|---|---|---|
| H-001b | Donchian polos | 0,03086 | DITOLAK |
| H-002 | Donchian + saringan carry | 0,03159 | DITOLAK |
| H-003 | pembalikan skor-z | −0,24782 | DITOLAK |
| H-004 | Donchian + ADX ≥ 30 | −0,01818 | DITOLAK |
| H-005 | entri retest | −0,03571 | DITOLAK |
| H-006 | sapuan likuiditas | −0,13449 | DITOLAK |
| **H-007** | **imbalan dipilih walk-forward** | **0,04044** | **DITOLAK, terbaik sejauh ini** |

Seluruhnya pada dataset, kriteria, limit 40 simbol, dan kode penilaian yang identik.

**Kesimpulan struktural S10:** enam percobaan pada sisi masuk menghasilkan nol perbaikan; satu percobaan pada sisi keluar menghasilkan +28% dalam satu langkah. Sisi keluar adalah arah yang punya leverage, dan sisi masuk sudah cukup diperiksa.

### KELUARGA ADR-006 — DITOLAK BERTIGA

Sumber: `reports/keluarga_adr006.{md,json}`, run **`30175665060`**, commit kode `1aedb84`, commit laporan `c0636bf`.

Usulan pengguna dipilah lebih dulu; **trend breakout tidak diuji ulang** karena itu persis H-001b dan H-002. Ambang `p entri acak` diperketat ke **0,0167 (Bonferroni 0,05/3) sebelum satu angka pun terlihat**.

| Hipotesis | Mekanisme | Ekspektasi R | Trade | p acak | Gerbang gagal |
|---|---|---|---|---|---|
| H-004 | breakout + ADX(14) ≥ 30 | −0,01818 | 7.899 | 0,0099 | **tidak ada** |
| H-005 | entri retest ("sniper") | −0,03571 | 12.194 | 0,0396 | `invarian_risiko` |
| H-006 | sapuan likuiditas (SMC) | −0,13449 | 20.385 | 1,0000 | `entri_acak`, `invarian_risiko` |

**Koreksi multiplisitas terbukti bergigi:** p H-005 sebesar 0,0396 akan lolos ambang biasa 0,05. Yang menolaknya adalah ambang Bonferroni yang ditetapkan di muka.

H-004 identik dengan H-002 kecuali satu saringan. Saringan itu **berhasil** menurunkan biaya (0,0345R → 0,0313R) dan membuang 58% perdagangan, namun ekspektasinya menembus nol: **perdagangan yang dibuang, secara agregat, adalah yang menguntungkan.** Penembusan saat ADX masih rendah justru penyumbang keunggulan.

H-006 gagal dengan pola identik H-003 (p 1,0000). Dengan dua mekanisme pembalikan independen gagal serupa, ini fakta: **pada 1h perp USDT, pembalikan jangka pendek rugi sistematis, bukan kebetulan sampel.** Bagian SMC lain (order block, FVG, BOS/CHoCH) tidak diuji karena tidak punya definisi mekanis, sehingga tidak dapat difalsifikasi mesin ini.

### H-003 — pembalikan skor-z, DITOLAK telak

Sumber: `reports/backtest_h003.md`, run **`30175179866`**, commit laporan `15162e7`. ADR-005. Ekspektasi **−0,24782R**, 28.959 perdagangan, **25/356** jendela positif, `entri_acak` **p 1,0000**.

**Asimetri 0,28R** antara kelanjutan dan pembalikan pada kerangka identik memfalsifikasi tafsiran bahwa kerangka stop/target-lah yang membatasi. Rerata `funding_R` **−0,0017**: posisi pembalikan rata-rata **menerima** funding dan tetap rugi telak.

### Cacat pada saringan ADR-004 — masih terbuka, kini menjadi penghalang utama

`invarian_risiko` gagal di H-001b, H-003, H-005, dan sekarang **H-007**. `carry_terproyeksi_R` adalah proyeksi rerata 30 hari; ketika rate melonjak setelah entri, atau stop lebar sehingga funding per R membesar, saringan tembus. H-002, H-004, dan H-006 kebetulan tidak punya kasus penembus pada H-006 hanya untuk gerbang ini.

Sampai S9 ini cacat sampingan. Setelah H-007, **ia adalah satu-satunya gerbang yang menghalangi hasil terbaik yang pernah diukur**, dan statusnya naik menjadi pekerjaan utama.

### H-002 dan H-001b

H-002: `reports/backtest_h002.md`, run `30174642490`, commit `858eedc`. 0,03159R, 18.883 perdagangan, sembilan gerbang lulus. Saringan ADR-004: umur maksimum 168 bar, carry maksimum 0,25R atas jendela 30 hari.

H-001b: run `30172926477`, commit `88746cf`. 0,0309R; `invarian_risiko` gagal −2,5853R. Perdagangan terburuk ANIMEUSDT `funding_R` **1,545** atas posisi 130 jam — bukti yang melahirkan ADR-004.

### MESIN BACKTEST — sembilan gerbang terpasang dan terbukti bisa gagal

`lux/backtest/`: `engine.py`, `gerbang.py`, `walk_forward.py`, `run_wf.py` (H-001b), `run_h002.py`, `run_h003.py`, `runner.py` (runner bersama), `run_keluarga.py` (H-004–H-006), **`run_h007.py`** (ADR-007). Gerbang: `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`. **Gerbang yang tidak dapat dinilai berarti GAGAL.**

Bukti bahwa gerbangnya bukan hiasan, kini dari tujuh hipotesis: `invarian_risiko` menjatuhkan H-001b, H-003, H-005, dan H-007; `entri_acak` menjatuhkan H-003 dan H-006; `buy_and_hold` menjatuhkan H-003; `checksum` pernah menemukan empat aset asing akibat pola unduh yang dipersempit.

**Parameter keluar kini dapat dipilih walk-forward.** `jalankan_walk_forward` menerima `buat_konfig(params, konfig_dasar)` opsional; tanpa argumen itu jalurnya identik dengan sebelumnya, dan `tests/test_konfig_kandidat.py` mengunci kesamaan itu dengan membandingkan hasil kedua jalur secara langsung. `run_wf.py`, `run_h002.py`, dan `run_h003.py` tidak disentuh.

**Aritmetika titik impas kini berupa kode, bukan prosa.** `lux/analisis/titik_impas.py` menurunkan laju kena target, ekspektasi kotor, seretan tersirat, dan laju yang dibutuhkan dari histogram alasan keluar. Modul itu tidak membaca data pasar dan tidak menghasilkan putusan.

Pra-registrasi bersifat **sekali tulis**; nilai saringan ikut masuk ke sidik hipotesis.

### MODEL FUNDING NYATA — `lux/funding_model.py`

`Jadwal` per simbol dari `funding_shard*.parquet`; penagihan dihitung dari stempel nyata, bukan kisi 8 jam tetap. `carry_terproyeksi_R` menskalakan rerata rate trailing dengan kepadatan penagihan.

### DATASET TIER B PUTARAN 2 — SAH, dasar semua pekerjaan selanjutnya

| Interval | Baris bulanan | Ekor harian | Simbol OK | Gagal | Duplikat | Celah kisi |
|---|---|---|---|---|---|---|
| 1h | **14.106.623** | 439.056 | 790 | 0 | 0 | **112** |
| 4h | **3.526.969** | 109.764 | 790 | 0 | 0 | **112** |

**Total 14.545.679 bar 1h dan 3.636.733 bar 4h, sekitar 703 MB.** Rasio 1h:4h **3,9996**.

### VALIDASI S5 — `reports/validate_1h.md`, commit `2356684`

14.545.679 baris, 790 simbol, **0 pelanggaran fatal**, 112 celah kisi, **447 simbol layak**. Aset `_retry` usang ditolak `POLA_DILARANG`.

### ADR-003 EKOR DATAR — universe layak v2

141 dari 790 simbol berekor datar, 1.081.920 bar dipangkas (7,4%), universe 447 → **438**. Pemangkasan diterapkan saat muat; aset Parquet tidak pernah ditulis ulang.

### FUNDING RATE S5b — `reports/funding_check.md`, commit `0448a67`

1.982.017 baris, 447 simbol, **3 celah sejati**, funding positif **79,1%**, **295 dari 447 simbol hidup di lebih dari satu rezim kisi**, jitter maksimum **47 ms**. Carry ekstrem: 1000WHYUSDT +60,7%/tahun, AERGOUSDT −102,6%, MYXUSDT −533,9%.

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1** (`5f222e8`): `header=0` + `skiprows=1` menghilangkan satu bar per berkas; menyamar sebagai rasio 4,014.
- **Parser 2 dan 3** (`16638b4`): BOM UTF-8 (kini `utf-8-sig`); satu baris sampah menggagalkan seluruh berkas (kini `errors="coerce"`).
- **URL non-ASCII**: percent-encoding lewat `bv.seg()`.
- **Metrik celah funding**: gagal lima putaran karena mengira kisi funding tetap. **Alat diagnosisnya sendiri yang membutakan.**
- **Circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`).
- **S10:** `tests/test_run_h007.py` didorong dengan kurung kurawal liar di ujungnya (`c48a785`), menjatuhkan pengumpulan pytest seluruhnya. Ditemukan gerbang pra-terbang dalam 1,53 detik, diperbaiki di `e81e34e`. Biayanya satu siklus, bukan satu run panjang — itulah gunanya gerbang itu.

### Universe — `reports/universe.json`

937 simbol pernah ada; **790 perpetual USDT** jadi universe riset; 447 layak, **438 setelah ADR-003**. Dataset lama 528 simbol berarti 262 hilang, dan yang hilang bukan sampel acak melainkan simbol yang mati.

### Pengujian — `reports/tests.md`

**382 pengujian hijau** pada commit `e81e34e` (run `30176262367`), kode keluar 0, 1,55 detik, seluruhnya tanpa jaringan. Naik dari 354 lewat `test_titik_impas.py` (11), `test_konfig_kandidat.py` (5), `test_run_h007.py` (12).

### Kapasitas runner — `reports/doctor.json`

4 vCPU, 15 GB RAM, 88 GB disk bebas. **Batas 6 jam per job yang menjadi kendala, bukan disk.** H-007 selesai dalam 51,5 detik untuk 40 simbol; **Tier A butuh minimal 24 shard**.

### Konektivitas

CDN `data.binance.vision` 200; S3 listing 200; REST `fapi.binance.com` **451 permanen**; checksum SHA256 cocok.

### Batas alat agen dan solusinya

- Agen **tidak bisa** membuat rilis, memicu workflow manual, membaca log, mengunduh artifact, atau melihat status run.
- Setiap workflow diberi filter `paths` pada berkasnya sendiri; **menyunting workflow adalah satu-satunya cara memicunya.**
- **Setiap workflow wajib menulis hasil ke `reports/` dan meng-commit balik** dengan `if: always()`.
- Sandbox agen **tidak punya jaringan**. Gerbang `pytest` wajib berjalan **sebelum** unduhan.
- Berkas laporan yang belum ada selama run berarti **sedang berjalan**, dikonfirmasi lewat `list_commits`, bukan diasumsikan. Kali ini butuh sembilan jajakan.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| Keunggulan kelanjutan membesar pada horizon lebih panjang (4h) | jalankan hipotesis baru pada 4h setelah validasi 4h |
| Funding sebagai **sinyal** memuat informasi arah, bukan hanya biaya | uji hipotesis berbasis funding, belum pernah dilakukan |
| Pengaman carry yang keras (bukan proyeksi) dapat menyelamatkan `invarian_risiko` tanpa memakan ekspektasi | hipotesis baru dengan mekanisme keluar paksa saat carry terealisasi melewati batas |
| Integritas 4h sama bersihnya dengan 1h | jalankan `validate.yml` untuk interval 4h |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap universe layak v2 438 |
| Hasil 40 simbol pertama mewakili 438 simbol | jalankan `--limit 0` sekali, hanya untuk hipotesis yang layak |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |

**Sudah turun dari asumsi menjadi fakta di S9:** saringan rezim tren memperbaiki keunggulan breakout (**salah**, H-004); menunda entri sampai retest memperkecil biaya per R secara menguntungkan (**salah**, H-005); SMC yang dapat dikodekan punya keunggulan (**salah**, H-006).

**Dihapus di S10 karena keliru secara konstruksi, bukan karena belum diukur:** "keunggulan Donchian berasal dari sedikit perdagangan berekor panjang". Mesin keluar pada target atau stop, sehingga sebarannya terpotong di kedua sisi dan ekor panjang mustahil ada. Dugaan ini sempat dijadwalkan sebagai penelitian di STATE v9; ia seharusnya gugur saat mesinnya dibaca.

**Terbukti di S10:** menurunkan titik impas lewat imbalan yang lebih besar menaikkan ekspektasi (**benar**, +28%), dan menaikkan lama pegang sehingga kerugian ekor membesar (**benar**, `invarian_risiko` −1,977R).

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 (14.076.257 baris 1h, 3.506.060 baris 4h, 17.169 celah, rasio 4,014); metrik celah funding putaran 1–4 (1.380.741 · 1.193.209 · 587.131 · 266.612); seluruh run pilot H-001 termasuk `30170073890` (0,0317R, 19.060 perdagangan, 604,26R) karena datanya memuat ekor palsu.

---

## 5. Penghalang aktif

Tidak ada yang menghentikan pekerjaan.

Dibutuhkan dari pengguna, belum memblokir: **token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`, agar runner dapat menulis ke database Run Results dan membangunkan agen pengawas.

---

## 6. Tindakan berikutnya

Posisi berubah tajam di S10. Sebelumnya tidak ada satu pun arah yang menunjukkan perbaikan. Sekarang ada satu, dan yang menghalanginya adalah gerbang risiko, bukan ekspektasi.

**Yang DILARANG, dan godaannya nyata:** menyetel `imbalan_R` ke 4,0 lalu menjalankan ulang. Nilai itu terpilih **setelah** hasil terlihat, dan mengunci pemenang pasca-hoc persis seperti itulah cara walk-forward diubah menjadi teater. H-007 sudah divonis dan tidak dihitung ulang.

Urutan yang sah:

1. **ADR-008 — pengaman carry yang keras.** `invarian_risiko` sudah menjatuhkan empat dari tujuh hipotesis, dan kini menjatuhkan yang terbaik. Penyebabnya diketahui: saringan ADR-004 menilai carry **terproyeksi** di saat entri dan tidak pernah menilai ulang. Mekanisme yang belum pernah diuji adalah **keluar paksa saat carry terealisasi melewati batas selama posisi berjalan**. Ini perubahan mesin keluar, bukan sinyal, sehingga sejalan dengan temuan S10 dan tidak melanggar ADR-006. Wajib didaftarkan sebagai H-008 dengan imbalan yang **ikut dipilih walk-forward seperti H-007**, bukan dipatok pada nilai yang menang kemarin.
2. **Horizon 4h.** Perdagangan yang lebih sedikit secara struktural, biaya yang sama dibagi ke pergerakan yang lebih besar. **Prasyarat mutlak: jalankan `validate.yml` untuk 4h.** Tanpa itu hasil 4h tidak boleh dipercaya.
3. **Funding sebagai sinyal.** Belum pernah diuji kandungan informasi arahnya.

Sisanya, tidak memblokir:

4. Perketat `gerbang_lulus` di `lux/funding.py` supaya celah dan jitter ikut menilai.
5. Perbaiki docstring `lux/costs.py` yang masih menyebut pembagi funding 8 jam tetap.
6. Diff terhadap Dataset G lama (528 simbol). **Satu-satunya butir dari daftar tugas awal pengguna yang benar-benar masih terbuka.**
7. `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md`; salin ADR-001 dan ADR-002 ke `decisions/`.
8. Pelapor Notion (`NOTION_TOKEN`) agar LUX Gatekeeper menerima hasil run otomatis.
9. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, dengan ≥24 shard.

---

## 7. Pengawasan otonom

Agen **LUX Gatekeeper** aktif di Notion. Terpicu saat runner membuat baris di database Run Results, menilai hasil terhadap sembilan gerbang mutu. Sudah diuji dengan baris sintetis bercacat dan menolak dengan benar. **Verdict Ditolak menghentikan pipeline.**

---

## 8. Peta repo

| Path | Isi |
|---|---|
| `config/lux.yaml` | seluruh parameter yang memengaruhi hasil |
| `lux/binance_vision.py` | klien arsip: listing S3, unduhan, checksum, percent-encoding |
| `lux/universe.py` | universe point-in-time dan klasifikasi jenis kontrak |
| `lux/ingest.py` | ingest Tier B dengan validasi per simbol |
| `lux/backfill_daily.py` | penutup celah ekor dari arsip harian |
| `lux/validate.py` · `lux/validate_run.py` | integritas OHLCV, kelayakan universe, penolak aset `_retry` |
| `lux/funding.py` · `lux/funding_check.py` | ingest funding rate dan metrik kisinya |
| `lux/funding_model.py` | jadwal funding nyata, penagihan, carry terproyeksi |
| `lux/costs.py` | model biaya dalam satuan R |
| `lux/diag_datar.py` · `lux/potong_ekor.py` | diagnosis dan pemangkasan ekor datar (ADR-003) |
| `lux/praregistrasi.py` | hipotesis sekali tulis dan penilaian terhadap kriteria |
| **`lux/analisis/titik_impas.py`** | **aritmetika titik impas atas laporan yang sudah dikomit; tanpa data pasar, tanpa putusan** |
| `lux/strategi/breakout_atr.py` | sinyal kelanjutan (H-001b, H-002, H-007) |
| `lux/strategi/reversi_zskor.py` | sinyal pembalikan (H-003) |
| `lux/strategi/rezim_adx.py` | ADX Wilder dan saringan rezim (H-004) |
| `lux/strategi/retest.py` | entri retest, "sniper entry" mekanis (H-005) |
| `lux/strategi/smc.py` | sapuan likuiditas, bagian SMC yang dapat dikodekan (H-006) |
| `lux/backtest/engine.py` | mesin eksekusi: stop, target, batas umur, saringan carry |
| `lux/backtest/gerbang.py` | sembilan gerbang mutu |
| `lux/backtest/walk_forward.py` | pemilihan parameter dalam sampel; **konfig per kandidat opsional (ADR-007)** |
| `lux/backtest/run_wf.py` | orkestrator H-001b — **jangan disunting** |
| `lux/backtest/run_h002.py` | orkestrator H-002 (ADR-004) — dibekukan |
| `lux/backtest/run_h003.py` | orkestrator H-003 (ADR-005) — dibekukan |
| `lux/backtest/runner.py` | **runner bersama**: muat sekali, jalankan, nilai, laporkan |
| `lux/backtest/run_keluarga.py` | keluarga ADR-006 (H-004, H-005, H-006) |
| **`lux/backtest/run_h007.py`** | **H-007 struktur keluar (ADR-007)** |
| `tests/` | **382** pengujian tanpa jaringan, wajib hijau sebelum unduhan |
| `reports/` | keluaran mesin tiap run, sumber bukti Bagian 3 |
| `hipotesis/` | pendaftaran sekali tulis: `H-001b` … `H-007` |
| `decisions/` | ADR-003 (ekor datar), ADR-004 (carry funding), ADR-005 (pembalikan), ADR-006 (keluarga), **ADR-007 (struktur keluar)** |
| `journal/` | riwayat per sesi |

**Workflow aktif (10):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`. `backtest.yml` kini menjalankan `lux.backtest.run_h007`.

**Dihapus di S7:** `analyze_tail.yml` (`07860a7`), `diagnose.yml` (`f4af734`), `diag_datar.yml` (`41ca693`), `retry_failed.yml` (`3a206c6`). Modul Python-nya tetap ada.

Release **`tier-b-v1`** memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`. Pola unduh backtest wajib `ohlcv_1h_*.parquet`.
