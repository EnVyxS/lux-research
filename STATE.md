# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-26 05:40 WIB (versi 12)
**Tahap sekarang:** S12 — penyebab kegagalan `invarian_risiko` **sudah diketahui dan terukur**: funding pada ekor, bukan pada rerata
**Tahap berikutnya:** H-009 menurut ADR-009 — pengaman carry dipatok menyala, tidak dilombakan

> **KOREKSI TERHADAP STATE v11.** Versi 11 menyatakan sebagai fakta bahwa "funding bukan penyebab kerugian ekor". **Itu salah dan sudah ditarik.** Funding justru penyumbang terbesarnya: 0,9228R dari kerugian terburuk 1,9769R. Kekeliruan itu berasal dari memakai rerata (0,0004R) untuk menyimpulkan sesuatu tentang ekor, sementara sebarannya tersedia di berkas yang sama. Rinciannya di ADR-009.

---

## 1. Aturan membaca berkas ini

Bagian 3 adalah **fakta**: setiap baris punya bukti berupa commit, run ID, atau kutipan dokumentasi. Bagian 4 adalah **asumsi**: belum diukur, dan dilarang diperlakukan sebagai fakta. Memindahkan baris dari Bagian 4 ke Bagian 3 hanya boleh dengan bukti terlampir.

Lima aturan yang lahir dari kesalahan nyata, bukan dari teori:

1. **Angka yang lulus gerbang belum tentu benar.** Rasio 1h:4h 4,014 pernah dicatat sebagai uji silang yang lulus, padahal sedang melaporkan bug.
2. **Sha laporan yang tidak berubah bukan tanda pekerjaan masih berjalan.**
3. **Penjelasan yang membuat anomali terasa wajar harus dicurigai lebih keras daripada anomalinya.**
4. **Lihat sebaran mentah sebelum berteori.** Metrik celah funding gagal lima putaran; satu tabel histogram di awal akan menyelesaikannya dalam satu putaran.
5. **Hipotesis yang ditolak tetap ditolak.** Ambang tidak disetel ulang setelah hasil terlihat.

Aturan keenam (S8): **percobaan yang dirancang agar informatif ke dua arah lebih berharga daripada percobaan yang dirancang agar berhasil.**

Aturan ketujuh (S9): **saringan yang membuang perdagangan tidak otomatis membuang perdagangan yang buruk.**

Aturan kedelapan (S10): **periksa apakah dugaanmu mungkin secara konstruksi sebelum menjadwalkannya sebagai penelitian.**

Aturan kesembilan (S11): **sebelum menjadwalkan percobaan, periksa apakah laporan yang sudah dikomit sudah menjawabnya.** Terbayar dua kali dalam satu sesi — ADR-008 seharusnya tidak pernah dijalankan, dan run diagnosis ADR-009 tidak pernah perlu dijalankan.

Aturan kesepuluh (S11): **gerbang yang kegagalannya tidak tertulis ke `reports/` bukan gerbang, melainkan titik buta yang menyamar sebagai gerbang.**

Aturan kesebelas (S12, ADR-009): **rerata tidak mengatakan apa pun tentang ekor.** Gerbang yang menilai nilai ekstrem hanya boleh dibantah dengan nilai ekstrem. Rerata funding 0,0004R dan funding terburuk 0,9228R keduanya benar; yang satu tidak membatasi yang lain.

Aturan kedua belas (S12, ADR-009): **batas risiko tidak dilombakan.** Menaruh pengaman ke dalam grid pemilihan berarti menyerahkan keputusan risiko kepada fungsi tujuan yang tidak melihat risiko.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa.

Seluruh komputasi berjalan di GitHub Actions. Mesin lokal pengguna tidak sanggup melakukan backtest penuh, dan tidak ada VM cloud karena kendala kartu kredit.

---

## 3. Fakta terverifikasi

### PENYEBAB KEGAGALAN `invarian_risiko` — TERUKUR, BUKAN LAGI DUGAAN

Sumber: blok `diagnosa_biaya.terburuk` di `reports/backtest_h008_carry_keras.json`, run **`30177253467`**. Sepuluh perdagangan terburuk:

| Simbol | R | Kotor R | Transaksi R | **Funding R** | Lebar stop | Jam | Alasan |
|---|---|---|---|---|---|---|---|
| AIOTUSDT | **−1,9769** | −1,0182 | 0,0359 | **0,9228** | 2,83% | 29 | stop |
| ALGOUSDT | −1,4067 | −1,0065 | 0,0135 | 0,3866 | 7,13% | 81 | stop |
| 1000XECUSDT | −1,3869 | −1,0260 | 0,0526 | 0,3083 | 1,88% | 107 | stop |
| AAVEUSDT | −1,3637 | −1,0116 | 0,0236 | 0,3285 | 4,14% | 156 | stop |
| 1000XECUSDT | −1,3215 | −1,0164 | 0,0323 | 0,2728 | 3,15% | 41 | stop |
| ADAUSDT | −1,2698 | −1,0198 | 0,0401 | 0,2098 | 2,46% | 94 | stop |
| 1000FLOKIUSDT | −1,2614 | −1,0211 | 0,0418 | 0,1985 | 2,42% | 93 | stop |
| 1000WHYUSDT | −1,2362 | −1,0189 | 0,0384 | 0,1789 | 2,57% | 50 | stop |
| 1000XECUSDT | −1,2282 | −1,0097 | 0,0190 | 0,1996 | 5,42% | 41 | stop |
| 1000FLOKIUSDT | −1,2154 | −1,0148 | 0,0292 | 0,1714 | 3,49% | 34 | stop |

Aritmetika tertutup rapat: −1,0182 − 0,0359 − 0,9228 = −1,9769, persis nilai gerbang.

**Fakta yang mengikutinya:**

- **Funding menyumbang 46,7% kerugian terburuk**, dan merupakan komponen biaya terbesar di kesepuluhnya — antara 5 sampai 26 kali biaya transaksi.
- **Stop bekerja sempurna.** Kesepuluhnya beralasan `stop` dengan kotor −1,0065 sampai −1,0260, yaitu tepat 1R ditambah slippage. **Tidak ada harga yang menganga melewati stop.**
- **Stop rapat bukan penyebabnya.** Lebar stop terburuk 2,83% terhadap rerata 3,61%; biaya transaksinya 0,0359R.
- **Perdagangan terburuk terbukti berjalan dengan pengaman ADR-008 mati.** Ia keluar beralasan `stop`, bukan `carry`, padahal carry 0,9228R melewati ambang teraktif mana pun di grid (maksimum 0,50). Ini deduksi, bukan dugaan. AIOTUSDT punya dua jendela, satu memilih 0,0 dan satu memilih 0,25.

### Mengapa ADR-008 gagal — mekanismenya benar, cara memilihnya yang salah

Walk-forward memaksimalkan ekspektasi **dalam sampel**. Gerbang `invarian_risiko` dinilai **setelahnya** dan tidak pernah masuk fungsi tujuan. Pengaman risiko memotong posisi sebelum sempat pulih, jadi ia memakan ekspektasi, jadi pemaksimal ekspektasi **selalu** mematikannya bila diberi pilihan.

| Ambang `maks_carry_realisasi_R` | Jendela memilihnya |
|---|---|
| 0,0 — mati | **334** dari 356 |
| 0,25 | 22 |
| 0,50 | **0** |

H-008 karena itu bukan uji terhadap pengaman carry, melainkan uji terhadap kesediaan pemaksimal ekspektasi memakai pengaman risiko. Jawabannya tidak. **Percobaan itu tidak bisa menjawab pertanyaan yang dimaksudkan.** Diperbaiki oleh ADR-009.

### H-008 — DITOLAK

Sumber: `reports/backtest_h008_carry_keras.{md,json}`, run **`30177253467`**, kode `141c08ab`, workflow `245747ee`, laporan `9819dcb0`. Sidik `dfeeea04fd4107f6`, 36 kombinasi, 208,6 detik.

Ekspektasi **+0,04126R**, total **+616,20R**, 14.933 perdagangan, **198/356** jendela positif. Alasan keluar: stop 10.254, target 4.117, `umur` 371, `akhir_data` 189, **`carry` 2**. Ditolak karena ekspektasi 0,0413R < 0,05R dan `invarian_risiko` **−1,9769R** — identik sampai empat desimal dengan H-007. Kenaikan 0,00082R adalah derau dari 22 jendela, bukan perbaikan.

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
| H-008 | pengaman carry dilombakan | 0,04126 | DITOLAK, pengaman dimatikan pemilih |

`invarian_risiko` menjatuhkan **lima** dari delapan: H-001b (−2,5853), H-003 (−1,8637), H-005 (−1,9122), H-007 (−1,9769), H-008 (−1,9769).

**Kesimpulan struktural:** enam percobaan pada sisi masuk menghasilkan nol perbaikan; satu percobaan pada sisi keluar menghasilkan +28%. Sisi keluar adalah arah yang punya leverage.

### Temuan S10 yang tetap berlaku: yang salah adalah titik impasnya, bukan sinyalnya

| Hipotesis | Laju kena target | Kotor `3p−1` | Bersih tercatat | Seretan |
|---|---|---|---|---|
| H-002 | **0,36028** | +0,08084 | **+0,03159** | 0,04926 |
| H-004 | 0,34151 | +0,02453 | −0,01818 | 0,04272 |
| H-005 | 0,33755 | +0,01265 | −0,03571 | 0,04836 |
| H-006 | 0,30122 | −0,09633 | −0,13449 | 0,03815 |
| H-003 | 0,26326 | −0,21021 | −0,24782 | 0,03761 |

Titik impas kotor `1/(1+imbalan)`: 1R 0,5000 · 2R 0,3333 · 3R 0,2500 · 4R 0,2000, dikunci `tests/test_titik_impas.py`. H-007 memanfaatkannya tanpa menyentuh sinyal: 83% jendela memilih 3R atau 4R, laju kena target turun ke 0,2864 seperti diramalkan.

### H-007 — hasil terbaik yang pernah diukur

Sumber: `reports/backtest_h007_keluar.{md,json}`, run **`30176317156`**, kode `e81e34e`, laporan `af72991`. Sidik `7f5e7aeeaa29284b`.

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

`reports/backtest_h003.md`, run **`30175179866`**, laporan `15162e7`. −0,24782R, 28.959 perdagangan, 25/356 jendela positif, `entri_acak` p 1,0000. Dengan H-006 gagal serupa: **pada 1h perp USDT, pembalikan jangka pendek rugi sistematis.**

### H-002 dan H-001b

H-002: run `30174642490`, laporan `858eedc`. 0,03159R, sembilan gerbang lulus. H-001b: run `30172926477`, commit `88746cf`. 0,0309R; `invarian_risiko` −2,5853R; perdagangan terburuk ANIMEUSDT `funding_R` 1,545 atas posisi 130 jam — bukti yang melahirkan ADR-004. **Catatan S12:** kasus ANIMEUSDT itu ternyata bukan pengecualian melainkan pola. Pembongkaran H-008 menunjukkan funding mendominasi ekor kerugian secara konsisten.

### MESIN BACKTEST — sembilan gerbang terpasang dan terbukti bisa gagal

`lux/backtest/`: `engine.py`, `gerbang.py`, `walk_forward.py`, `run_wf.py` (H-001b), `run_h002.py`, `run_h003.py`, `runner.py`, `run_keluarga.py`, `run_h007.py`, `run_h008.py`. Gerbang: `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`. **Gerbang yang tidak dapat dinilai berarti GAGAL.**

Lima alasan keluar: `stop`, `target`, `umur`, `carry`, `akhir_data`. Urutan per bar: umur → carry → stop/target → entri → ekuitas. `ALASAN_TIDAK_SELESAI = ("umur", "akhir_data", "carry")`.

**Catatan penting tentang gerbang `funding`:** ia menilai total funding mutlak, bukan ekor. Ia **lulus** di H-008 (10.253,97) sementara funding justru penyebab kegagalan `invarian_risiko`. Gerbang itu tidak salah, ia hanya menjawab pertanyaan lain.

Pra-registrasi bersifat **sekali tulis**; nilai saringan ikut masuk ke sidik hipotesis.

### DATASET TIER B PUTARAN 2 — SAH

**14.545.679 bar 1h dan 3.636.733 bar 4h**, 790 simbol, 112 celah kisi, rasio 1h:4h **3,9996**, sekitar 703 MB. Validasi 1h: 0 pelanggaran fatal, **447 simbol layak** (`2356684`). ADR-003 memangkas 141 simbol berekor datar, 1.081.920 bar (7,4%), universe layak v2 = **438**. Funding: 1.982.017 baris, 447 simbol, 3 celah sejati, 79,1% positif, jitter maksimum 47 ms, 295 dari 447 simbol hidup di lebih dari satu rezim kisi. Carry ekstrem: 1000WHYUSDT +60,7%/tahun, AERGOUSDT −102,6%, MYXUSDT −533,9%.

### Pengujian — `reports/tests.md`

**411 pengujian hijau** pada commit `141c08ab` (run `30177082103`), kode keluar 0, 1,95 detik, tanpa jaringan.

### Kapasitas runner dan konektivitas

4 vCPU, 15 GB RAM, 88 GB disk. **Batas 6 jam per job yang menjadi kendala, bukan disk.** H-008 selesai 208,6 detik untuk 40 simbol. CDN `data.binance.vision` 200; REST `fapi.binance.com` **451 permanen**.

### Batas alat agen dan solusinya

- Daftar alat GitHub yang tersedia **tidak memuat satu pun fungsi Actions** — tidak ada pembacaan run, job, langkah, atau log. **Diverifikasi di S11.**
- Agen tidak bisa membuat rilis, memicu workflow manual, atau mengunduh artifact.
- Setiap workflow diberi filter `paths` pada berkasnya sendiri; **menyunting workflow adalah satu-satunya cara memicunya.**
- **Setiap langkah yang bisa gagal wajib menulis hasilnya ke `reports/`** dengan `if: always()`. Sejak `245747ee`, tiap langkah pra-terbang `backtest.yml` punya id dan hasilnya dicetak ke `reports/backtest_log.md`.
- Sandbox agen **tidak punya jaringan**. Gerbang `pytest` wajib berjalan **sebelum** unduhan.
- **Commit laporan tanpa berkas hasil berarti run GAGAL, bukan sedang berjalan.** Run `30177134015` mati 30 detik setelah didorong.
- Blob laporan yang tidak berubah berarti **belum ditulis**, bukan berhasil. **SHA blob juga basi begitu ada tulisan** — jangan pakai ulang SHA lama saat memperbarui berkas.

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1** (`5f222e8`): `header=0` + `skiprows=1` menghilangkan satu bar per berkas.
- **Parser 2 dan 3** (`16638b4`): BOM UTF-8; satu baris sampah menggagalkan seluruh berkas.
- **URL non-ASCII**: percent-encoding lewat `bv.seg()`.
- **Metrik celah funding**: gagal lima putaran karena mengira kisi funding tetap.
- **Circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`).
- **S10:** kurung kurawal liar di `tests/test_run_h007.py` (`c48a785`) menjatuhkan pengumpulan pytest; diperbaiki `e81e34e`.
- **S11:** langkah pra-terbang `backtest.yml` bisu; diperbaiki `245747ee`.
- **S12:** STATE v11 menaikkan kekeliruan analitis menjadi fakta ("funding bukan penyebab kerugian ekor"). Ditarik di v12. Penyebabnya memakai rerata untuk menyimpulkan tentang ekor.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| Pengaman carry yang dipatok menyala membuat `invarian_risiko` lulus | H-009 menurut ADR-009 |
| Biaya menjaga risiko itu memakan ekspektasi di bawah 0,05R | ekspektasi H-009 terhadap 0,04126R |
| Keunggulan kelanjutan membesar pada horizon lebih panjang (4h) | jalankan hipotesis baru pada 4h setelah validasi 4h |
| Funding sebagai **sinyal** memuat informasi arah, bukan hanya biaya | uji hipotesis berbasis funding, belum pernah dilakukan |
| Integritas 4h sama bersihnya dengan 1h | jalankan `validate.yml` untuk interval 4h |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap universe layak v2 438 |
| Hasil 40 simbol pertama mewakili 438 simbol | jalankan `--limit 0` sekali, hanya untuk hipotesis yang layak |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |

**Turun menjadi fakta di S9:** saringan rezim tren memperbaiki breakout (**salah**, H-004); retest memperkecil biaya per R secara menguntungkan (**salah**, H-005); SMC yang dapat dikodekan punya keunggulan (**salah**, H-006).

**Terbukti di S10:** menurunkan titik impas lewat imbalan lebih besar menaikkan ekspektasi (**benar**, +28%), dan menaikkan lama pegang sehingga kerugian ekor membesar (**benar**).

**Difalsifikasi di S12, dua-duanya milik saya sendiri:**

- "Kerugian ekor berasal dari keluar di pembukaan bar yang menganga" — **salah.** Kesepuluh perdagangan terburuk beralasan `stop` dengan kotor tepat −1R.
- "Kerugian ekor berasal dari stop yang sangat rapat" — **salah.** Lebar stop terburuk 2,83% terhadap rerata 3,61%.

**Ditarik di S12 karena keliru:** "funding bukan penyebab kerugian ekor" (STATE v11). Funding menyumbang 46,7% kerugian terburuk.

**Dihapus di S10 karena keliru secara konstruksi:** "keunggulan Donchian berasal dari sedikit perdagangan berekor panjang".

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 (14.076.257 baris 1h, 3.506.060 baris 4h, 17.169 celah, rasio 4,014); metrik celah funding putaran 1–4 (1.380.741 · 1.193.209 · 587.131 · 266.612); seluruh run pilot H-001 termasuk `30170073890`.

---

## 5. Penghalang aktif

Tidak ada yang menghentikan pekerjaan.

Dibutuhkan dari pengguna, belum memblokir: **token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`.

---

## 6. Tindakan berikutnya

1. **H-009 menurut ADR-009 — pengaman carry dipatok menyala.** `maks_carry_realisasi_R = 0,25` konstan, **dikeluarkan dari ruang parameter**. Grid kembali persis ke grid H-007: `lookback` 20/55/100 × `imbalan_R` 1/2/3/4 = **12 kombinasi**. Nilai 0,25 berasal dari `config/lux.yaml` v2 sejak ADR-004, ditetapkan sebelum H-002 dijalankan — bukan pemenang pasca-hoc; di H-008 ia justru kalah 22 lawan 334.

   Ramalan yang sudah ditulis di ADR-009 sebelum run: keluar `carry` melonjak dari 2 ke ratusan; kerugian terburuk turun di bawah 1,5R dan gerbang lulus; **ekspektasi turun di bawah 0,04126R**, sehingga H-009 kemungkinan besar tetap ditolak, kali ini oleh kriteria 0,05R.

2. **Horizon 4h.** **Prasyarat mutlak: jalankan `validate.yml` untuk 4h.**

3. **Funding sebagai sinyal.** Belum pernah diuji kandungan informasi arahnya.

**Yang DILARANG:** melombakan ambang pengaman dalam bentuk apa pun; mematok `imbalan_R` ke 4,0; menghitung ulang hipotesis yang sudah divonis; melonggarkan ambang `invarian_risiko` dari −1,5R.

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
| `lux/backtest/run_h007.py` | H-007 struktur keluar (ADR-007) |
| `lux/backtest/run_h008.py` | H-008 pengaman carry dilombakan (ADR-008) — dibekukan |
| `tests/` | **411** pengujian tanpa jaringan, wajib hijau sebelum unduhan |
| `reports/` | keluaran mesin tiap run, sumber bukti Bagian 3 |
| `hipotesis/` | pendaftaran sekali tulis: `H-001b` … `H-008` |
| `decisions/` | ADR-003 (ekor datar), ADR-004 (carry funding), ADR-005 (pembalikan), ADR-006 (keluarga), ADR-007 (struktur keluar), ADR-008 (pengaman carry keras), **ADR-009 (batas risiko bukan parameter)** |
| `journal/` | riwayat per sesi |

**Workflow aktif (10):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`. `backtest.yml` masih menjalankan `lux.backtest.run_h008`; wajib diarahkan ke `run_h009` saat H-009 didorong.

**Dihapus di S7:** `analyze_tail.yml` (`07860a7`), `diagnose.yml` (`f4af734`), `diag_datar.yml` (`41ca693`), `retry_failed.yml` (`3a206c6`).

Release **`tier-b-v1`** memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`. Pola unduh backtest wajib `ohlcv_1h_*.parquet`.
