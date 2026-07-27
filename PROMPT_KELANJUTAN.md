# PROMPT KELANJUTAN — Riset LUX (v5)

> Titik masuk sesi baru. Dibuat 2026-07-27 pada commit induk `049fb009e4729760f5e76994e30de5498a11bf6f` (jurnal 43). Menggantikan v4 (blob `252fd79aab5ccaeae356626a380a816e43def928`), yang **usang di bagian paling menentukan**: v4 menyuruh "jalankan H-015" dan menyebutnya hijau-belum-dijalankan. H-015 **sudah** dijalankan, putusannya **TIDAK DAPAT DINILAI**, dan run kedua kini **dilarang**.

---

## 0. Urutan membaca, mengikat

Jangan mulai dari awal. Jangan mengulang pekerjaan yang sudah selesai. Baca **utuh**, bukan sekilas, dalam urutan ini:

1. **`decisions/ADR-038.md`** — "Arti `invarian_risiko` merah bagi seluruh jalur". **Ini yang paling menentukan apa yang boleh dikerjakan.** Ia membekukan adjudikasi dan melarang run H-015 kedua. Baca sebelum menyentuh apa pun.
2. **`STATE.md`** (v33, 44.196 B, `6955d3d4b4857f658f18e2629af24e3922535ecf`) — posisi riset, termasuk **60 aturan bernomor**. **JANGAN menulis ulang aturan dari ingatan.**
3. **`STATE_LAMPIRAN_ANGKA.md`** (14.769 B, `a72f0a04cc87f71235158b59d0ca2a805910d6de`) — seluruh tabel angka H-011…H-015. Dipisahkan dari STATE pada v33 supaya STATE berhenti tumbuh.
4. **`STATE_LAMPIRAN.md`** (25.016 B, `7b68ee633890247dc0072cd34106fa80ca116371`) — peta repo, inventaris modul, audit workflow, batas alat, papan ramalan. **Belum dibaca sejak lama; ia mungkin memuat pernyataan usang.**
5. **`decisions/ADR-037.md`** — pra-registrasi H-015. Masih mengikat untuk apa yang boleh diklaim.
6. **Dua jurnal terakhir**: `journal/2026-07-27-42.md` dan `journal/2026-07-27-43.md`. **JANGAN membaca `journal/` seluruhnya.**

Ketiga berkas STATE adalah **satu dokumen yang dipecah tiga**. Membaca satu saja berarti membaca sepertiga posisi. Bila sesuatu tidak tercatat di sana, **anggap belum diketahui**.

---

## 1. Posisi dalam satu paragraf

Lima belas hipotesis diselesaikan: **empat belas DITOLAK, satu (H-015) TIDAK DAPAT DINILAI**, nol kandidat bertahan. H-015 berjalan penuh tiga sel pada run `30249117960`, tetapi **ketiga selnya gagal `invarian_risiko` dan `checksum`**, sehingga seluruh besarannya kehilangan kewenangan (ADR-038 §5.3). Yang sekarang dipertanyakan bukan lagi funding, melainkan **apakah satuan R pada jalur ini berarti sesuatu**: tidak ada satu pun hasil, pada interval apa pun, yang pernah lolos sebelas gerbang. Repo memuat **60 aturan**, **21 kelas cacat**, **1012 uji**.

### Keadaan terverifikasi pada penyerahan

| Butir | Nilai | Bukti |
|---|---|---|
| HEAD | `049fb009e4729760f5e76994e30de5498a11bf6f` | commit jurnal 43 |
| Uji | **1012 lulus, kode keluar 0**, 3,44 s | `reports/tests.md` blob `3112a5438b03c623b0dcc197d116a2b2d94295bf`, commit `e21f0628` |
| Run H-015 | `30249117960`, **MERAH**, 8 m 52 s | laporan dikomit `5b2f70b6` |
| `lux/diagnostik/pelanggaran_risiko.py` | baru, ADR-038 §5.4 | `e21f0628` |
| `lux/backtest/engine.py` | 27.755 B | `81c1db8ad147dae149795db1d1166476efd210a9` |
| `lux/backtest/gerbang.py` | 20.353 B | `9bddf8d36e3446219c3b234e20b57b1d1bb3dd72` |
| `config/lux.yaml` | `stop_hormati_celah: true` | `8a66f15cf559f64dbebb523a29f21357a9300607` |

Nomor ADR bebas berikutnya: **ADR-039**. Jurnal berikutnya: **`journal/2026-07-27-44.md`**.

---

## 2. Yang DILARANG lebih dahulu, sebelum daftar tugas

ADR-038 memasang lima larangan permanen. Daftar tugas di bawah tidak berarti apa pun bila ini dilewati.

1. **Jangan memaklumi `invarian_risiko`** untuk sel, hipotesis, atau jalur mana pun.
2. **Jangan menggeser ambang −1,5R.**
3. **Jangan menaikkan lantai `min_median_stop_frac` 0,004** agar gerbang menjadi hijau.
4. **Jangan membuang perdagangan ekor** dari perhitungan.
5. **Jangan menghidupkan angka lama** dengan gerbang atau definisi baru.

Dan satu larangan operasional:

6. **RUN H-015 KEDUA BELUM BOLEH DIMULAI** (ADR-038 §6). Ia hanya akan menghijaukan `checksum` — cacat 17 sudah dibayar, `reports/manifest_aset_4h.json` (1.198 B, `b8f7b042…`) sudah ada di `main` — sementara `invarian_risiko` tetap merah. Hanya **diagnostik** yang boleh dijalankan sampai ADR lanjutannya ada.

---

## 3. Tugas berikutnya, berurutan

1. **Sambungkan diagnostik ke sisi runner sel K.** `lux/diagnostik/pelanggaran_risiko.py` sudah ada dan hijau, tetapi **belum dipanggil siapa pun**. Penyambungan menuntut `lux/backtest/runner.py` (40.322 B, `4ce34a3c…`) dan `lux/backtest/run_h015.py` (26.917 B, `aedd23b1…`) **dibaca utuh lebih dahulu** — jangan menebak titik sambungnya, itu cacat kelas 12 lagi. Keluarannya: satu laporan `reports/` per sel. **Jangan menarik JSON 432 KB ke konteks.**
2. **Adjudikasi R-P1, R-P2, R-P3, R-Q3** dari laporan itu. Inilah yang menentukan apakah −11,4736R berasal dari celah harga (jujur, mesin benar) atau dari sizing (mesin jatuh, seluruh papan skor batal).
3. **Tulis ADR-039** atas hasil diagnostik. Baru sesudah ADR-039 ada, pertanyaan "run H-015 kedua" boleh dibuka lagi.
4. **R-L1** — instrumentasi penolakan saringan menurut arah, atau **cabut R-L1** sebagai ramalan. Ia tak dapat dinilai karena kodenya tidak pernah memancarkan besarannya (cacat kelas 21).
5. **Verifikasi cabang `runner.py`** yang memancarkan *"manifest baru ditulis pada run ini"*. Cacat 17 dinyatakan dibayar tanpa cabang itu pernah dibaca. **Ini memerlukan verifikasi.**
6. **Cacat 19** — medan satuan / pembobotan / p bulanan pada `praregistrasi.Kriteria`.
7. **Uji ke-17** — satu dorongan yang **hanya** menyentuh `tests/`, lalu bandingkan delta cacah.
8. **R-J1** — cacah keluar `carry` sel SH dari `reports/backtest_h013_sh_sinyal_horizon.json` lewat skrip sisi runner.

---

## 4. Ambang beku — tidak digeser, tidak ditawar

lantai 0,004 · pengaman biaya masuk 0,5R · `BATAS_VOID` 20 · potong 2026-01-01 · besaran antar sel 0,020R · **p ≤ 0,05 pada satuan bulan kalender UTC** · ≥300 ulangan · ≥100 trade per sel · `MAKS_RASIO_DATAR` 0,10 · rasio bar datar 0,30 · ekspektasi 0,05R · **`invarian_risiko` −1,5R** · `maks_umur_bar` ≤ 168 · gerbang kesebelas 0,35 / 0,50R / 0,005.

**`maks_carry_realisasi_R` = 0,25**, asal-usulnya berlapis tiga — catat, sebab sudah salah **dua kali** di sini:

| Lapisan | Dokumen |
|---|---|
| Medan dan mekanismenya (bawaan `0.0` = MATI) | **ADR-008** |
| 0,25 dipatok sebagai batas yang **tidak dilombakan** | **ADR-009** |
| Asal angka 0,25 (`config/lux.yaml` v2) | **ADR-004** |

Dari ADR-037: **`AMBANG_RATE` = 0,0001**, **`MIN_PENAGIHAN` = 30**, seed `SEED_ACAK_H015` = 20260727 — dibekukan 2026-07-27, dan **tidak boleh digeser sesudah hasil terlihat**.

**Ambang 0,020R dibandingkan dengan float telanjang, dan itu disengaja.** `0.06 - 0.04` bernilai `0.019999999999999997` dan karenanya **TIDAK** lulus. Ada uji yang mengunci perilaku ini. Jangan "memperbaikinya" dengan pembulatan — dilarang ADR-037 §10.

**Ambang diagnostik tidak ditulis tangan.** `lux.diagnostik.pelanggaran_risiko.AMBANG_KERUGIAN_R` dibaca dari nilai bawaan `gerbang_invarian_risiko` lewat `inspect.signature`. Jangan menyalinnya menjadi konstanta baru.

---

## 5. Angka yang HARAM dikutip sebagai kelulusan

**Seluruh angka H-011 sampai H-015 sebagai penegak klaim apa pun** (ADR-038 §5.3) — termasuk seluruh angka run `30249117960` pada ketiga sel. Selain itu: `+0,029481R` · `+0,027654R` sebagai besaran lulus · `+0,054842R` / `+0,043732R` / `+0,066648R` · `+0,060163R` · `+0,059636R` · p 0,001100 · p 0,003322 dan "+2,99 galat baku" · kata "LULUS" di `reports/backtest_h013_kontribusi.md` · prosa R-D3 di `reports/h013b_p.md` · ambang ADR-015 §4.4 sebagai pra-registrasi geometri · "226 jendela / 63,5%" (benar 194 / 54,5%) · angka H-014 dibandingkan langsung dengan H-013 · angka H-015 dibandingkan langsung dengan H-014 · **F − K sebagai dasar kelulusan H-015**.

**Larangan permanen tambahan:** jangan menyatakan sistem siap diperdagangkan · jangan menambah cabang `LULUS` ke H-014 · jangan menambal `berpasangan.py` · jangan menjalankan ulang H-014 · jangan menulis aritmetika funding kedua di luar `funding_model` · jangan menyentuh `lux/strategi/`.

---

## 6. Batas alat, terverifikasi

- **Tidak ada fungsi GitHub Actions.** Run dipicu dengan **menyentuh berkas workflow**; verifikasi lewat `list_commits` dan lewat laporan yang dikomit.
- **Menyentuh `h014.yml` / `h015.yml` / `backtest.yml` / `h013b.yml` memulai run 4h.** Jangan menyentuhnya untuk perbaikan kecil sendirian. Run H-015 tiga sel: **8 m 52 s** total (K 70 s, F 74 s, A 162 s).
- `tests.yml` selesai ~23–30 s dan memicu **hanya** untuk `lux/**`, `tests/**`, dan `tests.yml`. Alurnya: `set +e` → pytest → tulis `reports/tests.md` → **laporan tetap dikomit meski merah** → langkah "Tegakkan hasil" `exit 1`. **`reports/tests.md` adalah cara termurah membaca hasil run**, dan ia memuat commit + kode keluar + cacah.
- `STATE*.md`, `PROMPT_KELANJUTAN.md`, `journal/`, `decisions/` **tidak** memicu `tests.yml`.
- `search_code` mengembalikan nihil pada repo ini — pakai `get_file_contents` atas jalur direktori (menerima `"/"` dan jalur berakhiran `/`, mengembalikan ukuran + SHA per berkas).
- Bentuk panggilan yang bekerja: `push_files` `{owner, repo, branch, message, files:[{path, content}]}` — **penggantian berkas utuh**; `get_file_contents` `{owner, repo, path, ref}` (`ref` menerima `"main"` atau SHA commit); `list_commits` `{owner, repo, sha, path?, perPage}`.
- **Jalur modul yang benar:** `lux/backtest/gerbang.py`, bukan `lux/gerbang.py`. Menebak jalur memboroskan satu panggilan; sudah terjadi.
- Runner: python 3.12.13, numpy 2.5.1, pytest 9.1.1, pandas 2.2.3, pyarrow 17.0.0, **tanpa scipy/requests**; 4 vCPU / 15 GB; batas 6 jam.
- `fapi.binance.com` → 451; `data.binance.vision` → 200. Rilis `tier-b-v1` id `359778114`, aset 4h 12 berkas / 157.628.619 B.
- `backfill_daily.yml` cron `'0 2 * * 1'` — tetapi commit `09ba5545` mendarat 06:07 UTC. Isinya belum dibaca. **Ini memerlukan verifikasi.**

### BATAS MUATAN DORONGAN — pelanggaran nyata, bukan teori

Muatan `push_files` yang panjang **dapat terpotong diam-diam** dan tetap dikomit. Itu terjadi pada `STATE.md` v28 (`56633f80`), yang menyimpan posisi tak lengkap di `main` ~3,5 jam. Percobaan mendorong ulang seluruh `STATE.md` sekali muat pernah dibalas **"The tool call was canceled by the user."**

**Mitigasi wajib (aturan 35):**
1. Berkas panjang **dipecah** — itulah sebab ada dua lampiran STATE.
2. Setiap dorongan panjang **dibaca ulang dari `main` sesudah dikirim**: daftar direktori untuk ukuran, lalu pembacaan utuh untuk memastikan **ekornya hadir**. Ukuran saja bukan bukti keutuhan; katakan begitu bila hanya ukuran yang diperiksa.
3. **Jangan membaca berkas 40 KB lalu menulis penggantinya dalam jendela konteks yang sama.**

### PERINGATAN MASUK — uji ditulis dari ringkasan

Dua run merah pada sesi 2026-07-27 punya akar tunggal: **uji ditulis terhadap ringkasan API saya sendiri, bukan terhadap badan fungsinya** (cacat 12, aturan 42). `JadwalBoneka` tanpa `__len__` → `TypeError`; fixture memakai `Konfig()` bawaan alih-alih `config/lux.yaml`. Keduanya diperbaiki pada **ujinya**, bukan pada modulnya. **Baca badan fungsi sebelum menulis boneka atau fixture atasnya.** Di pytest ongkosnya tiga detik; di runner sembilan menit.

---

## 7. Cacat yang masih terbuka

- **Cacat 19 — terbuka.** `praregistrasi.Kriteria` tidak dapat menyatakan satuan penarikan, pembobotan mengikat, maupun p bulanan.
- **Cacat 20 — adjudikator buta gerbang.** `gabung_h014` mengumumkan putusan tanpa memeriksa `gerbang_gagal`. Ditutup di tingkat dokumen oleh papan skor v33 yang membawa kolom gerbang; **belum** ditutup di tingkat kode untuk `gabung_h014`, dan itu **tidak boleh** ditutup dengan menyentuh H-014 (larangan permanen).
- **Cacat 21 — ramalan tak ternilai.** R-L1 dipra-registrasi atas besaran yang kodenya tidak pernah memancarkan. Aturan 60 kini menuntut setiap ramalan menyebut berkas dan medan pengadjudikasinya.
- **Cacat 16 masih hidup:** F − K ekspektasi run **+0,0135R** lawan F − K bulanan **−0,0157R** — berlawanan tanda. Keduanya haram.
- Belum terjelaskan: sel A **162 s** lawan K 70 s / F 74 s; entri acak nyata A **0,10723R** tertinggi dari ketiga sel; `AH = +0,05817042814276683R`; rasio bar datar 4h; uji ke-17 (872 nyata lawan 871 diramalkan); ADR-037 §5 lawan `berpasangan.PEMBATAS`; tiga kunci `config/lux.yaml` yang tidak dibaca program; utang audit config aturan 39.

---

## 8. Ramalan aktif

Ditulis **sebelum** hasil terlihat. Jangan menghaluskan yang meleset, jangan mengaku sudah menduga sesudahnya.

### Dibekukan di ADR-038 §7 — belum dinilai

- **R-P1** perdagangan −11,4736R keluar pada harga pembukaan bar yang membuka di seberang stop. Bila bukan pembukaan maupun harga stop → mesinnya yang jatuh. Diadjudikasi oleh medan `harga_keluar_bruto` dan `celah_melewati_stop` pada laporan diagnostik.
- **R-P2** cacah perdagangan melewati −1,5R pada sel K antara **10 dan 500** dari 59.306. Diadjudikasi oleh `cacah_pelanggaran`.
- **R-P3** sekurangnya satu dari sepuluh terburuk sel F berasal dari simbol yang median `stop_frac`-nya hanya sedikit di atas 0,004. Diadjudikasi oleh medan `stop_frac` per baris.

### Dibekukan di jurnal 43 §4

- **R-Q1 — TEPAT.** Diramalkan 1012 butir dan kode 0; `reports/tests.md` (`3112a543…`) atas `e21f0628` mencatat **`1012 passed in 3.44s`**, kode keluar `0`. **Aturan 58 tetap berdiri:** ini menghitung, bukan meramal, dan dua bukti tandingan lama (850→855, 871→872) belum terbantah.
- **R-Q2 — tidak berlaku.** Ia bersyarat pada run merah; runnya hijau.
- **R-Q3 — belum dinilai.** `per_alasan` sel K akan didominasi `stop`, bukan `carry`. Bila `carry` yang terbesar, dugaan sizing hidup kembali dan ADR-038 §5.3 harus dibaca ulang.

### Papan lama

TEPAT: R-N1, R-L3, R-L4, R-L5, R-O3, R-Q1. MELESET: R-N2, R-L2, R-M1 (dua kali), R-K2, R-H1, R-G4, R-H3. **CACAT PENALARAN: R-O2** (dibangun atas klaim "ekor tunggal" yang dibantah sepuluh baris tabel ekor sel F). TAK TERNILAI: R-L1, R-J3. BELUM: R-M2, R-B1 paruh kedua, R-J1, R-J2, R-O1.

---

## 9. Aturan kerja dengan pengguna

- Bila pengguna menulis **"lanjut"** atau **"lanjutkan"**, teruskan **tanpa meminta konfirmasi**.
- Pisahkan **fakta terverifikasi** (punya commit / run ID / kutipan) dari **asumsi**; bila belum terverifikasi, katakan **"Ini memerlukan verifikasi."**
- Katakan bila pengguna salah. Katakan bila **kamu sendiri** salah — termasuk bila **koreksimu sendiri** ternyata salah; itu sudah terjadi (jurnal 37). Angka di pesan commit juga wajib benar; "27 uji" pada `e21f0628` salah dan dikoreksi di jurnal 43 §1.
- Jangan menghaluskan ramalan yang meleset.
- Perbarui `STATE.md` tiap posisi berubah; tambah satu entri `journal/` tiap sesi, **ditulis sebelum hasil run terlihat** bila membahas ramalan; segarkan berkas ini sebelum konteks penuh.

---

## 10. Rantai commit terakhir

`abed0edf` (977 hijau) → `16f4af2e` (jurnal 40) → `017e0ac3` (`h015.yml`) → `5b2f70b6` (**laporan H-015, run `30249117960` merah**) → `93d69c08` (jurnal 41) → `3d1d3e37` (jurnal 42) → `26ee4462` (**ADR-038**) → `12193543` (**STATE v33** + `STATE_LAMPIRAN_ANGKA.md`) → `e21f0628` (**diagnostik ADR-038 §5.4 + 35 butir uji → 1012 hijau**) → **`049fb009` (jurnal 43)**.

**Posisi: 15 hipotesis diselesaikan — 14 DITOLAK, 1 TIDAK DAPAT DINILAI. Nol kandidat. 60 aturan. 21 kelas cacat. 1012 uji. Adjudikasi dibekukan sampai diagnostik ekor −1,5R selesai.**
