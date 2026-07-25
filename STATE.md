# STATE — Posisi Riset LUX

> **Sesi baru mulai dari sini.** Berkas ini ditulis ulang setiap sesi. Ia menggantikan kebutuhan membaca Notion atau arsip jurnal. Jika sesuatu tidak tercatat di sini, anggap belum diketahui.

**Diperbarui:** 2026-07-26 04:45 WIB (versi 9)
**Tahap sekarang:** S9 **SELESAI** — enam hipotesis sinyal harga sudah divonis; **tidak satu pun** punya ekspektasi yang memadai, dan yang terbaik tetap Donchian polos
**Tahap berikutnya:** S10 — berhenti mencari sinyal harga; serang horizon atau funding sebagai sinyal

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

Aturan ketujuh, lahir di S9: **saringan yang membuang perdagangan tidak otomatis membuang perdagangan yang buruk.** ADX ≥ 30 membuang 58% perdagangan H-002 dan menjungkirkan tandanya. Sebelum sesi ini, "saring saat tidak tren" terdengar seperti perbaikan gratis. Ia bukan perbaikan gratis, dan hanya pengukuran yang bisa menunjukkannya.

---

## 2. Apa yang sedang dibangun

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang. Hanya data mentah dan pelajaran metodologis yang dibawa.

Seluruh komputasi berjalan di GitHub Actions. Mesin lokal pengguna tidak sanggup melakukan backtest penuh, dan tidak ada VM cloud karena kendala kartu kredit.

---

## 3. Fakta terverifikasi

### HASIL RISET TERBARU — KELUARGA ADR-006 DITOLAK BERTIGA

Sumber: `reports/keluarga_adr006.{md,json}`, `reports/backtest_h00{4_adx,5_retest,6_smc}.{md,json}`, run **`30175665060`**, commit kode `1aedb84`, commit workflow `ae3df8c`, commit laporan `c0636bf`. ADR-006.

Tiga usulan pengguna — SMC, sniper entry, trend breakout, ADX 30 — dipilah lebih dulu. **Trend breakout tidak diuji ulang** karena itu persis H-001b dan H-002. Tiga sisanya didaftarkan sebagai hipotesis baru dan dijalankan serentak dalam satu run, dengan data dimuat sekali sehingga ketiganya melihat kumpulan berkas yang identik.

Karena tiga percobaan dilakukan serentak, ambang `p entri acak` **diperketat ke 0,0167 (Bonferroni 0,05/3) sebelum satu angka pun terlihat**. Ambang lain tidak diubah.

| Hipotesis | Mekanisme | Sidik | Ekspektasi R | Total R | Trade | Jendela + | p acak | Putusan |
|---|---|---|---|---|---|---|---|---|
| H-004 | breakout + ADX(14) ≥ 30 | `98d6a5e15b2cc08b` | **−0,01818** | −143,63 | 7.899 | 154/356 | 0,0099 | DITOLAK |
| H-005 | entri retest ("sniper") | — | **−0,03571** | −435,49 | 12.194 | 151/356 | 0,0396 | DITOLAK |
| H-006 | sapuan likuiditas (SMC) | — | **−0,13449** | −2.741,51 | 20.385 | 76/356 | 1,0000 | DITOLAK |

Gerbang gagal: H-004 **tidak ada** (sembilan gerbang lulus, ditolak murni karena kriteria pra-registrasi); H-005 `invarian_risiko`; H-006 `entri_acak` dan `invarian_risiko`.

### Temuan utama S9: saringan tren membuang perdagangan yang menguntungkan

H-004 adalah hasil paling informatif sesi ini, dan hasilnya berlawanan dengan intuisi yang hampir universal di kalangan praktisi.

Kerangka, dataset, universe, limit 40 simbol, dan kode penilaian H-004 **identik dengan H-002**. Satu-satunya perbedaan adalah saringan ADX ≥ 30. Efeknya:

| | H-002 | H-004 |
|---|---|---|
| Perdagangan | 18.883 | **7.899** (−58%) |
| Ekspektasi R | **+0,03159** | **−0,01818** |
| Total R | +596,44 | −143,63 |
| Jendela positif | 212/356 | 154/356 |
| Rerata biaya transaksi | 0,0345R | 0,0313R |

Saringan itu **berhasil** menurunkan biaya per perdagangan (0,0345R → 0,0313R) dan **berhasil** membuang lebih dari separuh perdagangan. Meski begitu ekspektasinya jatuh menembus nol. Kesimpulan yang dipaksakan aritmetika: **perdagangan yang dibuang saringan itu, secara agregat, adalah perdagangan yang menguntungkan.** Penembusan yang terjadi saat ADX masih rendah — yaitu saat tren baru mulai terbentuk — justru penyumbang keunggulan; saat ADX sudah di atas 30, sebagian besar pergerakan sudah terjadi.

`entri_acak` H-004 tetap lulus pada p 0,0099. Sinyalnya masih memuat informasi, tetapi informasi itu kini bertanda salah setelah biaya.

### Sapuan likuiditas mengonfirmasi temuan H-003, bukan menambah temuan baru

H-006 gagal dengan pola yang sama persis dengan H-003: p entri acak **1,0000**, hanya 76 dari 356 jendela positif. Keduanya adalah pembalikan-di-level. Dengan dua mekanisme pembalikan yang independen secara konstruksi kini gagal dengan tanda dan pola yang sama, pernyataan berikut naik dari asumsi menjadi fakta: **pada 1h perpetual USDT, keluarga mekanisme pembalikan jangka pendek punya ekspektasi negatif yang sistematis, bukan kebetulan sampel.**

Itu sekaligus menutup perdebatan SMC dalam batas yang jujur: bagian SMC yang **dapat dikodekan tanpa penafsiran** sudah diukur dan rugi telak. Bagian lainnya (order block, fair value gap, BOS/CHoCH) tidak diuji karena tidak punya definisi yang dapat diuji — dan sesuatu yang tidak dapat didefinisikan secara mekanis tidak dapat difalsifikasi, sehingga tidak dapat dipercaya maupun dibantah oleh mesin ini.

### Menunda entri tidak menyelamatkan keunggulan yang tipis

H-005 menguji dugaan yang lahir dari S8: biaya rerata 0,0345R hampir menelan keunggulan 0,032R, jadi masuk lebih dekat ke level seharusnya memperkecil biaya per R. Dugaan itu **salah dalam praktik**. Menunggu retest memang membuang perdagangan, tetapi yang hangus adalah penembusan yang langsung lari — yaitu justru yang paling menguntungkan. Ekspektasi jatuh ke −0,0357R.

H-004 dan H-005 gagal karena sebab yang sama dan itu bukan kebetulan: **keduanya adalah saringan yang mengurangi jumlah perdagangan, dan keduanya membuang sisi kanan sebaran.** Keunggulan Donchian tampaknya berasal dari sedikit perdagangan berekor panjang, bukan dari rerata yang sehat.

### Papan skor enam hipotesis

| ID | Mekanisme | Ekspektasi R | Putusan |
|---|---|---|---|
| H-001b | Donchian polos | 0,03086 | DITOLAK |
| **H-002** | **Donchian + saringan carry** | **0,03159** | **DITOLAK, terbaik sejauh ini** |
| H-003 | pembalikan skor-z | −0,24782 | DITOLAK |
| H-004 | Donchian + ADX ≥ 30 | −0,01818 | DITOLAK |
| H-005 | entri retest | −0,03571 | DITOLAK |
| H-006 | sapuan likuiditas | −0,13449 | DITOLAK |

Seluruhnya pada dataset, kriteria, limit 40 simbol, dan kode penilaian yang identik. Itulah yang membuat tabel ini sah dibandingkan.

**Kesimpulan struktural S9:** enam mekanisme sinyal harga pada 1h sudah diukur, dan yang terbaik pun hanya 0,032R terhadap biaya 0,0345R. Ambang 0,05R tidak pernah didekati. Melanjutkan pencarian sinyal harga ketujuh pada horizon 1h adalah pengulangan, bukan penelitian.

### H-003 — pembalikan skor-z, DITOLAK telak

Sumber: `reports/backtest_h003.md`, run **`30175179866`**, commit laporan `15162e7`. ADR-005. Sidik `3a1cdc867f61bf67`. Ekspektasi **−0,24782R**, total −7.176,60R, 28.959 perdagangan, **25/356** jendela positif, `entri_acak` **p 1,0000**. Gerbang gagal: `buy_and_hold`, `entri_acak`, `invarian_risiko`.

**Asimetri 0,28R** antara kelanjutan (+0,0316R) dan pembalikan (−0,2478R) pada kerangka identik memfalsifikasi tafsiran bahwa kerangka stop/target-lah yang membatasi. Kerangka ini meneruskan informasi arah dengan baik. Arah taruhan Donchian nyata, hanya terlalu tipis.

Rerata `funding_R` H-003 **−0,0017** — posisi pembalikan rata-rata justru **menerima** funding, dan tetap rugi telak. Funding bukan penyebab kegagalannya.

### Cacat yang ditemukan pada saringan ADR-004, masih terbuka

`invarian_risiko` gagal pada **−1,8637R** di H-003 dan gagal lagi di H-005, meski saringan carry aktif. `carry_terproyeksi_R` adalah **proyeksi rerata 30 hari, bukan jaminan**: ketika rate melonjak setelah entri, atau stop sangat lebar sehingga funding per R membesar, saringan itu tembus. H-002 dan H-004 kebetulan tidak punya kasus penembus. **Lulusnya gerbang pada satu hipotesis bukan bukti gerbang itu tidak bisa gagal pada hipotesis lain.**

### H-002 — DITOLAK, sembilan gerbang lulus

Sumber: `reports/backtest_h002.md`, run **`30174642490`**, commit laporan `858eedc`. Ekspektasi **0,03159R** < 0,05R. 18.883 perdagangan, 596,44R, 212/356 jendela positif. Saringan ADR-004: umur maksimum 168 bar, carry terproyeksi maksimum 0,25R atas jendela 30 hari. Alasan keluar: stop 11.909, target 6.707, `akhir_data` 164, `umur` 103.

### H-001b — DITOLAK, tidak dihitung ulang selamanya

Sumber: `reports/backtest_h001.md`, run `30172926477`, commit `88746cf`. Ekspektasi 0,0309R; `invarian_risiko` gagal pada −2,5853R. Sidik `e458f4c82abf6735`. Perdagangan terburuk ANIMEUSDT: `funding_R` **1,545** atas posisi 130 jam — bukti yang melahirkan ADR-004.

### MESIN BACKTEST — sembilan gerbang terpasang dan terbukti bisa gagal

`lux/backtest/engine.py`, `gerbang.py`, `walk_forward.py`, `run_wf.py` (H-001b), `run_h002.py`, `run_h003.py`, **`runner.py` (runner bersama)**, **`run_keluarga.py` (H-004–H-006)**. Gerbang: `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`. **Gerbang yang tidak dapat dinilai berarti GAGAL.**

Bukti bahwa gerbangnya bukan hiasan, kini dari enam hipotesis: `invarian_risiko` menjatuhkan H-001b, H-003, dan H-005; `entri_acak` menjatuhkan H-003 dan H-006; `buy_and_hold` menjatuhkan H-003; `checksum` pernah menemukan empat aset asing akibat pola unduh yang dipersempit; `forward_fill` menjatuhkan run pilot lewat panjang deret bar datar sementara rasionya lolos.

Pra-registrasi bersifat **sekali tulis**. Nilai saringan ikut masuk ke sidik hipotesis, sehingga percobaan diam-diam dengan nilai lain akan tertolak.

**Utang orkestrator sudah dibayar.** ADR-005 mensyaratkan ekstraksi runner bersama sebelum orkestrator keempat; `lux/backtest/runner.py` memenuhinya sebelum H-004 ditulis. `run_wf.py`, `run_h002.py`, dan `run_h003.py` tidak disentuh, sehingga hasil lama tetap dapat diulang bita demi bita. Hipotesis baru kini cukup mendaftarkan satu `Spek`.

### MODEL FUNDING NYATA — `lux/funding_model.py`

`Jadwal` per simbol dari `funding_shard*.parquet`; penagihan dihitung dari stempel nyata, bukan kisi 8 jam tetap. `statistik_trailing` merangkum rerata rate pada jendela yang **berakhir tepat di saat entri**; `carry_terproyeksi_R` menskalakannya dengan kepadatan penagihan. `biaya.funding_interval_jam` sudah dihapus dari `config/lux.yaml`, diganti `funding_dari_jadwal_nyata: true` (`5341871`).

### DATASET TIER B PUTARAN 2 — SAH, dasar semua pekerjaan selanjutnya

Sumber: `reports/ingest_tier_b.md` pada `16638b4`, `reports/backfill_daily.md` dan `reports/tail_anomali.md` pada `fbead60`.

| Interval | Baris bulanan | Ekor harian | Simbol OK | Gagal | Duplikat | Celah kisi |
|---|---|---|---|---|---|---|
| 1h | **14.106.623** | 439.056 | 790 | 0 | 0 | **112** |
| 4h | **3.526.969** | 109.764 | 790 | 0 | 0 | **112** |

**Total 14.545.679 bar 1h dan 3.636.733 bar 4h, sekitar 703 MB, 790 dari 790 simbol tanpa satu pun kegagalan.** Rasio 1h:4h **3,9996**.

### VALIDASI S5 — `reports/validate_1h.md`, commit `2356684`

14.545.679 baris, 790 simbol, **0 pelanggaran fatal**, 0 duplikat, 112 celah kisi, **447 simbol layak**, 343 ditolak. Selisih 12.593 baris dijelaskan tuntas: aset `_retry` usang, kini ditolak `POLA_DILARANG`.

### ADR-003 EKOR DATAR — universe layak v2

141 dari 790 simbol berekor datar, 1.081.920 bar dipangkas (7,4%), universe layak 447 → **438** (`reports/universe_layak_v2.json`). Pemangkasan diterapkan saat muat lewat `lux/potong_ekor.potong`; aset Parquet tidak pernah ditulis ulang.

### FUNDING RATE S5b — `reports/funding_check.md`, commit `0448a67`

1.982.017 baris, 447 dari 447 simbol layak, 2020-01-01 → 2026-06-30, 0 duplikat, **3 celah sejati**, funding positif **79,1%**. **295 dari 447 simbol hidup di lebih dari satu rezim kisi.** Jitter stempel maksimum **47 ms**.

Carry ekstrem bagi long: 1000WHYUSDT 60,7%/tahun, 1000000BOBUSDT 60,1%, BROCCOLIF3BUSDT 57,0%; AERGOUSDT −102,6%/tahun bagi short.

### Cacat yang sudah ditutup dan tidak boleh terulang

- **Parser 1** (`5f222e8`): `header=0` + `skiprows=1` menghilangkan satu bar per berkas; menyamar sebagai rasio 4,014.
- **Parser 2 dan 3** (`16638b4`): BOM UTF-8 (kini `utf-8-sig`); satu baris sampah menggagalkan seluruh berkas (kini `errors="coerce"`).
- **URL non-ASCII**: percent-encoding lewat `bv.seg()`.
- **Metrik celah funding**: gagal lima putaran karena mengira kisi funding tetap; penyebabnya jitter 47 ms yang disembunyikan pembulatan empat desimal. **Alat diagnosisnya sendiri yang membutakan.**
- **Circular import** `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`), diputus dengan import lazy.

### Universe — `reports/universe.json`

937 simbol pernah ada; **790 perpetual USDT** jadi universe riset; 761 aktif, 29 delisted; 447 layak, **438 setelah ADR-003**. Dataset lama 528 simbol berarti 262 hilang, dan yang hilang bukan sampel acak melainkan simbol yang mati.

### Pengujian — `reports/tests.md`

**354 pengujian hijau** pada commit `1aedb84` (run `30175618453`), kode keluar 0, 2,03 detik, seluruhnya tanpa jaringan. Naik dari 318 (`5dda655`) lewat `test_rezim_adx.py` (8), `test_retest.py` (10), `test_smc.py` (9), `test_run_keluarga.py` (9).

### Kapasitas runner — `reports/doctor.json`

4 vCPU, 15 GB RAM, 88 GB disk bebas. **Batas 6 jam per job, bukan disk, yang menjadi kendala utama.** Tiga hipotesis 40 simbol selesai dalam satu run singkat; **Tier A butuh minimal 24 shard**.

### Konektivitas

CDN `data.binance.vision` 200; S3 listing 200; REST `fapi.binance.com` **451 permanen**; checksum SHA256 cocok.

### Batas alat agen dan solusinya

- Agen **tidak bisa** membuat rilis, memicu workflow manual, membaca log, mengunduh artifact, atau melihat status run.
- Setiap workflow diberi filter `paths` pada berkasnya sendiri; **menyunting workflow adalah satu-satunya cara memicunya.**
- **Setiap workflow wajib menulis hasil ke `reports/` dan meng-commit balik** dengan `if: always()`.
- Sandbox agen **tidak punya jaringan**. Gerbang `pytest` wajib berjalan **sebelum** unduhan di setiap workflow.

---

## 4. Asumsi belum terverifikasi

| Asumsi | Cara memverifikasi |
|---|---|
| Keunggulan kelanjutan membesar pada horizon lebih panjang (4h) | jalankan hipotesis baru pada 4h setelah validasi 4h |
| Funding sebagai **sinyal** memuat informasi arah, bukan hanya biaya | uji hipotesis berbasis funding, belum pernah dilakukan |
| Keunggulan Donchian berasal dari sedikit perdagangan berekor panjang | periksa sebaran R H-002; didukung H-004 dan H-005 tetapi belum diukur langsung |
| Integritas 4h sama bersihnya dengan 1h | jalankan `validate.yml` untuk interval 4h |
| Dataset G lama (528 simbol) konsisten dengan data baru | diff terhadap universe layak v2 438 |
| Hasil 40 simbol pertama mewakili 438 simbol | jalankan `--limit 0` sekali, hanya untuk hipotesis yang layak |
| Throughput cukup untuk Tier A dalam 6 jam per shard | ukur ulang dengan ≥24 shard |

**Sudah turun dari asumsi menjadi fakta di S9:** saringan rezim tren memperbaiki keunggulan breakout (**salah**, H-004); menunda entri sampai retest memperkecil biaya per R secara menguntungkan (**salah**, H-005); SMC yang dapat dikodekan punya keunggulan (**salah**, H-006).

**Angka yang dilarang dikutip:** seluruh hasil ingest putaran 1 (14.076.257 baris 1h, 3.506.060 baris 4h, 17.169 celah, rasio 4,014); metrik celah funding putaran 1–4 (1.380.741 · 1.193.209 · 587.131 · 266.612); seluruh run pilot H-001 termasuk `30170073890` (0,0317R, 19.060 perdagangan, 604,26R) karena datanya memuat ekor palsu.

---

## 5. Penghalang aktif

Tidak ada yang menghentikan pekerjaan.

Dibutuhkan dari pengguna, belum memblokir: **token integrasi Notion** sebagai GitHub Secret `NOTION_TOKEN`, agar runner dapat menulis ke database Run Results dan membangunkan agen pengawas.

---

## 6. Tindakan berikutnya

Enam hipotesis sinyal harga pada 1h sudah divonis. **Hipotesis harga ketujuh pada horizon 1h dilarang** — ADR-006 melarangnya secara eksplisit, dan enam titik data mendukung larangan itu, bukan hanya satu.

Dua arah yang sah, masing-masing wajib didahului ADR sebelum kodenya ditulis:

1. **Horizon 4h.** Keunggulan terbaik yang pernah diukur adalah 0,032R terhadap biaya 0,0345R. Biaya per perdagangan menelan hampir seluruh keunggulan, dan S9 membuktikan bahwa mengurangi jumlah perdagangan lewat saringan justru merusak. Yang belum dicoba adalah membiarkan jumlah perdagangan turun secara **struktural** lewat horizon yang lebih panjang, sehingga biaya yang sama dibagi ke pergerakan yang lebih besar. **Prasyarat mutlak: jalankan `validate.yml` untuk 4h.** Tanpa itu hasil 4h tidak boleh dipercaya.
2. **Funding sebagai sinyal.** Belum pernah diuji kandungan informasi arahnya. 79,1% penagihan positif dan carry ekstrem sampai −533,9%/tahun adalah struktur nyata, dan H-003 menunjukkan funding kadang mengalir ke arah yang berlawanan dengan dugaan.

Sebelum keduanya, satu pekerjaan diagnostik yang murah dan berpotensi mengubah arah:

3. **Periksa sebaran R H-002.** Bila keunggulan benar-benar berasal dari segelintir perdagangan berekor panjang, maka target 2R yang memotong pemenang lebih awal adalah tertuduh utama, dan itu pertanyaan tentang **struktur keluar**, bukan tentang sinyal masuk. Data untuk ini sudah ada di `reports/backtest_h002.json`; tidak perlu run baru.

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
| `lux/strategi/breakout_atr.py` | sinyal kelanjutan (H-001b, H-002) |
| `lux/strategi/reversi_zskor.py` | sinyal pembalikan (H-003) |
| `lux/strategi/rezim_adx.py` | ADX Wilder dan saringan rezim (H-004) |
| `lux/strategi/retest.py` | entri retest, "sniper entry" mekanis (H-005) |
| `lux/strategi/smc.py` | sapuan likuiditas, bagian SMC yang dapat dikodekan (H-006) |
| `lux/backtest/engine.py` | mesin eksekusi: stop, target, batas umur, saringan carry |
| `lux/backtest/gerbang.py` | sembilan gerbang mutu |
| `lux/backtest/walk_forward.py` | pemilihan parameter dalam sampel, penilaian di luar sampel |
| `lux/backtest/run_wf.py` | orkestrator H-001b — **jangan disunting** |
| `lux/backtest/run_h002.py` | orkestrator H-002 (ADR-004) — dibekukan |
| `lux/backtest/run_h003.py` | orkestrator H-003 (ADR-005) — dibekukan |
| `lux/backtest/runner.py` | **runner bersama**: muat sekali, jalankan, nilai, laporkan |
| `lux/backtest/run_keluarga.py` | keluarga ADR-006 (H-004, H-005, H-006) |
| `tests/` | **354** pengujian tanpa jaringan, wajib hijau sebelum unduhan |
| `reports/` | keluaran mesin tiap run, sumber bukti Bagian 3 |
| `hipotesis/` | pendaftaran sekali tulis: `H-001b`, `H-002`, `H-003`, `H-004`, `H-005`, `H-006` |
| `decisions/` | ADR-003 (ekor datar), ADR-004 (carry funding), ADR-005 (pembalikan), ADR-006 (keluarga) |
| `journal/` | riwayat per sesi |

**Workflow aktif (10):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`. `backtest.yml` kini menjalankan `lux.backtest.run_keluarga`.

**Dihapus di S7** karena masukannya artifact yang kedaluwarsa 90 hari sementara keluarannya sudah permanen di `reports/`: `analyze_tail.yml` (`07860a7`), `diagnose.yml` (`f4af734`), `diag_datar.yml` (`41ca693`). `retry_failed.yml` dihapus lebih dulu di `3a206c6`. Modul Python-nya tetap ada.

Release **`tier-b-v1`** memuat `ohlcv_{interval}_shard{NN}.parquet`, `..._tail_shard{NN}.parquet`, dan `funding_shard{00..03}.parquet`. Pola unduh backtest wajib `ohlcv_1h_*.parquet`.
