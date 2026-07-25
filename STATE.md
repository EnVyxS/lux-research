# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-26 05:30 WIB (versi 11)
**Tahap sekarang:** S11 **SELESAI** — delapan hipotesis divonis; H-007 tetap terbaik (+0,0404R) dan tetap DITOLAK; **diagnosis carry difalsifikasi**
**Tahap berikutnya:** S12 — penyebab `invarian_risiko` jatuh **belum diketahui** dan harus **diukur**, bukan ditebak lagi

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

Aturan kedelapan (S10): **periksa apakah dugaanmu mungkin secara konstruksi sebelum menjadwalkannya sebagai penelitian.** Dugaan ekor gemuk mustahil karena mesin memotong kedua sisi sebaran; ia dapat dijatuhkan tanpa run apa pun.

Aturan kesembilan, lahir di S11 dan merupakan versi mahal dari aturan kedelapan: **sebelum menjadwalkan percobaan, periksa apakah laporan yang sudah dikomit sudah menjawabnya.** ADR-008 menuduh carry funding sebagai penyebab kerugian ekor, padahal laporan H-007 yang sudah dibaca memuat dua baris yang meruntuhkannya — rerata biaya funding 0,0004R, dan nol perdagangan dengan biaya melewati 1R. Biayanya satu run, dua siklus workflow, dan enam berkas kode.

Aturan kesepuluh (S11), soal alat bukan soal riset: **gerbang yang kegagalannya tidak tertulis ke `reports/` bukan gerbang, melainkan titik buta yang menyamar sebagai gerbang.**

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa.

Seluruh komputasi berjalan di GitHub Actions. Mesin lokal pengguna tidak sanggup melakukan backtest penuh, dan tidak ada VM cloud karena kendala kartu kredit.

---

## 3. Fakta terverifikasi

### HASIL RISET TERBARU — H-008 DITOLAK, DAN DIAGNOSISNYA IKUT GUGUR

Sumber: `reports/backtest_h008_carry_keras.{md,json}`, run **`30177253467`**, commit kode `141c08ab`, commit workflow `245747ee`, commit laporan `9819dcb0`. ADR-008. Sidik `dfeeea04fd4107f6`, 36 kombinasi, 208,6 detik.

**Ekspektasi +0,04126R**, total **+616,20R**, 14.933 perdagangan, **198/356** jendela positif. Alasan keluar: stop 10.254, target 4.117, `umur` 371, `akhir_data` 189, **`carry` 2**.

Ditolak karena dua hal:

- Kriteria pra-registrasi: **0,0413R < 0,05R**.
- Gerbang **`invarian_risiko` GAGAL** pada **−1,9769R** terhadap ambang −1,5R.

**Angka kerugian terburuk itu identik sampai empat desimal dengan H-007.** Pengaman carry menembak dua kali dari 14.933 perdagangan dan tidak menyentuh perdagangan terburuk sama sekali. Kenaikan ekspektasi sebesar 0,00082R adalah derau dari 22 jendela, bukan perbaikan.

### Walk-forward menolak mekanismenya sendiri

Grid memuat tiga ambang; 0,0 disertakan **sebelum** hasil terlihat, tepatnya agar percobaan bisa mengatakan "mekanisme ini tidak berguna".

| Ambang `maks_carry_realisasi_R` | Jendela memilihnya |
|---|---|
| 0,0 — pengaman mati | **334** dari 356 |
| 0,25 | 22 |
| 0,50 | **0** |

93,8% jendela mematikan pengaman itu di dalam sampel, tanpa melihat data penilaian. Ambang paling longgar tidak pernah terpilih satu kali pun.

### Funding sudah gugur sebagai penyebab kerugian ekor — ini fakta, bukan tafsiran

Dari `reports/backtest_h008_carry_keras.md`, dan baris yang sama sudah ada di laporan H-007:

- Rerata biaya funding: **0,0004R** (biaya transaksi 0,0343R, delapan puluh kali lebih besar)
- Perdagangan dengan biaya melebihi 1R: **0** dari 14.933
- Gerbang `funding` **lulus**

Perdagangan terburuk bertahan melewati pengaman carry 0,25R, artinya carry terealisasinya tidak pernah mencapai 0,25R. **Kerugian −1,977R itu bukan disebabkan funding.** Diagnosis ADR-008 salah.

### Penyebab −1,977R — BELUM DIKETAHUI, dua kandidat, keduanya belum diukur

1. **Keluar di pembukaan bar yang menganga.** Urutan loop mesin: `umur` → `carry` → stop/target. Ketiga keluar `umur`, `carry`, `akhir_data` terjadi pada **harga pembukaan bar**, sebelum stop diperiksa. Bila harga menganga melewati stop, posisi ditutup di pembukaan yang sudah jauh di bawah stop. Bukti tak langsung: H-002 punya 103 keluar `umur` dan lulus gerbang ini; H-007 dan H-008 punya 371 dan gagal.
2. **Stop yang sangat rapat.** Biaya dalam R berbanding terbalik dengan lebar stop. Rerata lebar stop **3,606%**, tetapi pada stop yang jauh lebih rapat, fee dan slippage saja bisa mendekati 1R — dan laporan hanya menjamin biaya tidak *melewati* 1R.

Keduanya cukup untuk menjelaskan besaran yang diamati. **Dilarang memilih salah satunya tanpa pengukuran.**

### Papan skor delapan hipotesis

| ID | Mekanisme | Ekspektasi R | Putusan |
|---|---|---|---|
| H-001b | Donchian polos | 0,03086 | DITOLAK |
| H-002 | Donchian + saringan carry | 0,03159 | DITOLAK |
| H-003 | pembalikan skor-z | −0,24782 | DITOLAK |
| H-004 | Donchian + ADX ≥ 30 | −0,01818 | DITOLAK |
| H-005 | entri retest | −0,03571 | DITOLAK |
| H-006 | sapuan likuiditas | −0,13449 | DITOLAK |
| **H-007** | **imbalan dipilih walk-forward** | **0,04044** | **DITOLAK, terbaik sejauh ini** |
| H-008 | pengaman carry terealisasi | 0,04126 | DITOLAK, mekanisme inert |

Seluruhnya pada dataset, kriteria, limit 40 simbol, dan kode penilaian yang identik. `invarian_risiko` kini menjatuhkan **lima** dari delapan: H-001b (−2,5853), H-003 (−1,8637), H-005 (−1,9122), H-007 (−1,9769), H-008 (−1,9769).

**Kesimpulan struktural yang bertahan dari S10:** enam percobaan pada sisi masuk menghasilkan nol perbaikan; satu percobaan pada sisi keluar menghasilkan +28%. Sisi keluar tetap arah yang punya leverage. Yang ditambahkan S11: **sisi keluar yang bermasalah adalah mekanika eksekusinya, bukan biayanya.**

### Temuan S10 yang tetap berlaku: yang salah adalah titik impasnya, bukan sinyalnya

Enam hipotesis pertama menggeser laju kena target sambil membiarkan stop 1R dan target 2R. Terurut sempurna menurut satu angka saja:

| Hipotesis | Laju kena target | Kotor `3p−1` | Bersih tercatat | Seretan |
|---|---|---|---|---|
| H-002 | **0,36028** | +0,08084 | **+0,03159** | 0,04926 |
| H-004 | 0,34151 | +0,02453 | −0,01818 | 0,04272 |
| H-005 | 0,33755 | +0,01265 | −0,03571 | 0,04836 |
| H-006 | 0,30122 | −0,09633 | −0,13449 | 0,03815 |
| H-003 | 0,26326 | −0,21021 | −0,24782 | 0,03761 |

Titik impas kotor adalah `1/(1+imbalan)`: 1R 0,5000 · 2R 0,3333 · 3R 0,2500 · 4R 0,2000. Aritmetika ini dikunci `tests/test_titik_impas.py`. H-007 memanfaatkannya tanpa menyentuh sinyal: 83% jendela memilih 3R atau 4R, laju kena target turun ke 0,2864 persis seperti diramalkan, dan titik impasnya turun lebih cepat.

### H-007 — hasil terbaik yang pernah diukur

Sumber: `reports/backtest_h007_keluar.{md,json}`, run **`30176317156`**, commit `e81e34e`, laporan `af72991`. Sidik `7f5e7aeeaa29284b`.

| | H-002 | H-007 |
|---|---|---|
| Ekspektasi R | +0,03159 | **+0,04044** (+28%) |
| Total R | +596,44 | +605,10 |
| Perdagangan | 18.883 | 14.962 |
| Jendela positif | 212/356 | 199/356 |
| Unggul vs beli-tahan | 34/40 | **36/40** |
| Keluar `umur` | 103 | 371 |

`entri_acak` p **0,0099**. Delapan gerbang lulus; hanya `invarian_risiko` jatuh.

### KELUARGA ADR-006 — DITOLAK BERTIGA

Sumber: `reports/keluarga_adr006.{md,json}`, run **`30175665060`**, kode `1aedb84`, laporan `c0636bf`. Ambang p diperketat ke **0,0167 (Bonferroni 0,05/3) sebelum satu angka pun terlihat**. Trend breakout **tidak diuji ulang** karena itu persis H-001b dan H-002.

| Hipotesis | Mekanisme | Ekspektasi R | Trade | p acak | Gerbang gagal |
|---|---|---|---|---|---|
| H-004 | breakout + ADX(14) ≥ 30 | −0,01818 | 7.899 | 0,0099 | **tidak ada** |
| H-005 | entri retest ("sniper") | −0,03571 | 12.194 | 0,0396 | `invarian_risiko` |
| H-006 | sapuan likuiditas (SMC) | −0,13449 | 20.385 | 1,0000 | `entri_acak`, `invarian_risiko` |

**Koreksi multiplisitas terbukti bergigi:** p H-005 0,0396 akan lolos ambang biasa 0,05. H-004 membuang 58% perdagangan dan menurunkan biaya, tetapi **perdagangan yang dibuang secara agregat adalah yang menguntungkan.** Bagian SMC lain (order block, FVG, BOS/CHoCH) tidak diuji karena tidak punya definisi mekanis.

### H-003 — pembalikan skor-z, DITOLAK telak

`reports/backtest_h003.md`, run **`30175179866`**, laporan `15162e7`. −0,24782R, 28.959 perdagangan, 25/356 jendela positif, `entri_acak` p 1,0000. Rerata `funding_R` −0,0017: posisi pembalikan rata-rata **menerima** funding dan tetap rugi telak. Dengan H-006 gagal serupa, ini fakta: **pada 1h perp USDT, pembalikan jangka pendek rugi sistematis.**

### H-002 dan H-001b

H-002: run `30174642490`, laporan `858eedc`. 0,03159R, sembilan gerbang lulus. H-001b: run `30172926477`, commit `88746cf`. 0,0309R; `invarian_risiko` −2,5853R; perdagangan terburuk ANIMEUSDT `funding_R` 1,545 atas posisi 130 jam — bukti yang melahirkan ADR-004. **Catatan S11:** kasus ANIMEUSDT itu nyata, tetapi menggeneralisasikannya ke seluruh kegagalan `invarian_risiko` adalah kekeliruan yang baru saja terbayar.

### MESIN BACKTEST — sembilan gerbang terpasang dan terbukti bisa gagal

`lux/backtest/`: `engine.py`, `gerbang.py`, `walk_forward.py`, `run_wf.py` (H-001b), `run_h002.py`, `run_h003.py`, `runner.py`, `run_keluarga.py`, `run_h007.py`, **`run_h008.py`**. Gerbang: `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`. **Gerbang yang tidak dapat dinilai berarti GAGAL.**

Mesin kini punya lima alasan keluar: `stop`, `target`, `umur`, `carry`, `akhir_data`. Urutan per bar: umur → carry → stop/target → entri → ekuitas. `ALASAN_TIDAK_SELESAI = ("umur", "akhir_data", "carry")` dipakai aritmetika titik impas.

Pra-registrasi bersifat **sekali tulis**; nilai saringan ikut masuk ke sidik hipotesis.

### DATASET TIER B PUTARAN 2 — SAH

**14.545.679 bar 1h dan 3.636.733 bar 4h**, 790 simbol, 112 celah kisi, rasio 1h:4h **3,9996**, sekitar 703 MB. Validasi 1h: 0 pelanggaran fatal, **447 simbol layak** (`2356684`). ADR-003 memangkas 141 simbol berekor datar, 1.081.920 bar (7,4%), universe layak v2 = **438**. Funding: 1.982.017 baris, 447 simbol, 3 celah sejati, 79,1% positif, jitter maksimum 47 ms, 295 dari 447 simbol hidup di lebih dari satu rezim kisi.

### Pengujian — `reports/tests.md`

**411 pengujian hijau** pada commit `141c08ab` (run `30177082103`), kode keluar 0, 1,95 detik, seluruhnya tanpa jaringan. Naik dari 382 lewat `test_carry_keras.py` (12) dan `test_run_h008.py` (17).

### Kapasitas runner dan konektivitas

4 vCPU, 15 GB RAM, 88 GB disk. **Batas 6 jam per job yang menjadi kendala, bukan disk.** H-008 selesai 208,6 detik untuk 40 simbol; Tier A butuh ≥24 shard. CDN `data.binance.vision` 200; REST `fapi.binance.com` **451 permanen**.

### Batas alat agen dan solusinya

- Daftar alat GitHub yang tersedia **tidak memuat satu pun fungsi Actions** — tidak ada pembacaan run, job, langkah, atau log. **Diverifikasi di S11**, bukan diwarisi sebagai asumsi.
- Agen tidak bisa membuat rilis, memicu workflow manual, atau mengunduh artifact.
- Setiap workflow diberi filter `paths` pada berkasnya sendiri; **menyunting workflow adalah satu-satunya cara memicunya.**
- **Setiap langkah yang bisa gagal wajib menulis hasilnya ke `reports/`** dengan `if: always()`. Sejak `245747ee`, tiap langkah pra-terbang `backtest.yml` punya id, menyalurkan keluaran ke `logs/preflight.log`, dan hasilnya dicetak ke `reports/backtest_log.md`.
- Sandbox agen **tidak punya jaringan**. Gerbang `pytest` wajib berjalan **sebelum** unduhan.
- **Commit laporan tanpa berkas hasil berarti run GAGAL, bukan sedang berjalan.** Run `30177134015` mati 30 detik setelah didorong dan sempat disangka masih terbang.

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1** (`5f222e8`): `header=0` + `skiprows=1` menghilangkan satu bar per berkas; menyamar sebagai rasio 4,014.
- **Parser 2 dan 3** (`16638b4`): BOM UTF-8; satu baris sampah menggagalkan seluruh berkas.
- **URL non-ASCII**: percent-encoding lewat `bv.seg()`.
- **Metrik celah funding**: gagal lima putaran karena mengira kisi funding tetap.
- **Circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`).
- **S10:** kurung kurawal liar di `tests/test_run_h007.py` (`c48a785`) menjatuhkan pengumpulan pytest; ditemukan gerbang pra-terbang dalam 1,53 detik, diperbaiki `e81e34e`.
- **S11:** langkah pra-terbang `backtest.yml` bisu; kegagalan tidak meninggalkan jejak terbaca. Diperbaiki `245747ee`.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| Kerugian ekor berasal dari keluar di pembukaan bar yang menganga | catat alasan keluar, lebar stop, dan biaya perdagangan terburuk per simbol |
| Kerugian ekor berasal dari stop yang sangat rapat | sebaran `jarak_stop/harga` terhadap R pada perdagangan terburuk |
| Keunggulan kelanjutan membesar pada horizon lebih panjang (4h) | jalankan hipotesis baru pada 4h setelah validasi 4h |
| Funding sebagai **sinyal** memuat informasi arah, bukan hanya biaya | uji hipotesis berbasis funding, belum pernah dilakukan |
| Integritas 4h sama bersihnya dengan 1h | jalankan `validate.yml` untuk interval 4h |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap universe layak v2 438 |
| Hasil 40 simbol pertama mewakili 438 simbol | jalankan `--limit 0` sekali, hanya untuk hipotesis yang layak |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |

**Turun dari asumsi menjadi fakta di S9:** saringan rezim tren memperbaiki breakout (**salah**, H-004); retest memperkecil biaya per R secara menguntungkan (**salah**, H-005); SMC yang dapat dikodekan punya keunggulan (**salah**, H-006).

**Terbukti di S10:** menurunkan titik impas lewat imbalan lebih besar menaikkan ekspektasi (**benar**, +28%), dan menaikkan lama pegang sehingga kerugian ekor membesar (**benar**).

**Difalsifikasi di S11:** "pengaman carry yang keras dapat menyelamatkan `invarian_risiko`". Pengaman itu menembak 2 kali dari 14.933 perdagangan, walk-forward mematikannya di 334 dari 356 jendela, dan kerugian terburuk tidak bergeser satu digit pun. **Funding bukan penyebab kerugian ekor.**

**Dihapus di S10 karena keliru secara konstruksi:** "keunggulan Donchian berasal dari sedikit perdagangan berekor panjang".

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 (14.076.257 baris 1h, 3.506.060 baris 4h, 17.169 celah, rasio 4,014); metrik celah funding putaran 1–4 (1.380.741 · 1.193.209 · 587.131 · 266.612); seluruh run pilot H-001 termasuk `30170073890`.

---

## 5. Penghalang aktif

Tidak ada yang menghentikan pekerjaan.

Dibutuhkan dari pengguna, belum memblokir: **token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`.

---

## 6. Tindakan berikutnya

S11 menutup satu jalur dan membuka satu pertanyaan. Jalur yang ditutup: biaya funding. Pertanyaan yang terbuka: apa yang sebenarnya membuat satu perdagangan rugi 1,977R ketika stopnya 1R.

**Yang DILARANG:**

- Mematok `imbalan_R` ke 4,0 karena ia menang di H-007. Nilai itu terpilih setelah hasil terlihat.
- Mengusulkan mekanisme baru untuk `invarian_risiko` **sebelum** penyebabnya diukur. S11 sudah menunjukkan harga dari melewati langkah ini.
- Menghitung ulang hipotesis yang sudah divonis.

Urutan yang sah:

1. **ADR-009 — diagnosis kerugian ekor, bukan mekanisme.** Bongkar perdagangan terburuk: alasan keluar, lebar stop terhadap harga, pembongkaran biaya, dan apakah harga pembukaan bar keluar berada di luar stop. Ini pembacaan atas laporan dan hasil yang sudah ada; **ia tidak boleh menghasilkan putusan hipotesis** dan tidak butuh pra-registrasi. Baru setelah angkanya terlihat, mekanisme yang tepat bisa dirancang.
2. **Horizon 4h.** **Prasyarat mutlak: jalankan `validate.yml` untuk 4h.**
3. **Funding sebagai sinyal.** Kandungan informasi arahnya belum pernah diuji — dan S11 justru memperkuat alasannya, karena funding sudah terbukti bukan biaya yang berarti.

Sisanya, tidak memblokir:

4. Perketat `gerbang_lulus` di `lux/funding.py`.
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
| `config/lux.yaml` | seluruh parameter yang memengaruhi hasil |
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
| `lux/analisis/titik_impas.py` | aritmetika titik impas atas laporan yang sudah dikomit; tanpa data pasar, tanpa putusan |
| `lux/strategi/breakout_atr.py` | sinyal kelanjutan (H-001b, H-002, H-007, H-008) |
| `lux/strategi/reversi_zskor.py` | sinyal pembalikan (H-003) |
| `lux/strategi/rezim_adx.py` | ADX Wilder dan saringan rezim (H-004) |
| `lux/strategi/retest.py` | entri retest, "sniper entry" mekanis (H-005) |
| `lux/strategi/smc.py` | sapuan likuiditas, bagian SMC yang dapat dikodekan (H-006) |
| `lux/backtest/engine.py` | mesin eksekusi: stop, target, batas umur, saringan carry, **pengaman carry terealisasi (ADR-008)** |
| `lux/backtest/gerbang.py` | sembilan gerbang mutu |
| `lux/backtest/walk_forward.py` | pemilihan parameter dalam sampel; konfig per kandidat opsional (ADR-007) |
| `lux/backtest/run_wf.py` | orkestrator H-001b — **jangan disunting** |
| `lux/backtest/run_h002.py` | orkestrator H-002 (ADR-004) — dibekukan |
| `lux/backtest/run_h003.py` | orkestrator H-003 (ADR-005) — dibekukan |
| `lux/backtest/runner.py` | **runner bersama**: muat sekali, jalankan, nilai, laporkan |
| `lux/backtest/run_keluarga.py` | keluarga ADR-006 (H-004, H-005, H-006) |
| `lux/backtest/run_h007.py` | H-007 struktur keluar (ADR-007) |
| **`lux/backtest/run_h008.py`** | **H-008 pengaman carry keras (ADR-008)** |
| `tests/` | **411** pengujian tanpa jaringan, wajib hijau sebelum unduhan |
| `reports/` | keluaran mesin tiap run, sumber bukti Bagian 3 |
| `hipotesis/` | pendaftaran sekali tulis: `H-001b` … `H-008` |
| `decisions/` | ADR-003 (ekor datar), ADR-004 (carry funding), ADR-005 (pembalikan), ADR-006 (keluarga), ADR-007 (struktur keluar), **ADR-008 (pengaman carry keras)** |
| `journal/` | riwayat per sesi |

**Workflow aktif (10):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`. `backtest.yml` kini menjalankan `lux.backtest.run_h008` dan setiap langkah pra-terbangnya melaporkan diri.

**Dihapus di S7:** `analyze_tail.yml` (`07860a7`), `diagnose.yml` (`f4af734`), `diag_datar.yml` (`41ca693`), `retry_failed.yml` (`3a206c6`).

Release **`tier-b-v1`** memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`. Pola unduh backtest wajib `ohlcv_1h_*.parquet`.
