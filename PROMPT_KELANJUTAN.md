# PROMPT KELANJUTAN — LUX

Disegarkan pada commit sesudah `a25160ca4a238fbb5b652bd4839ed9917183dcba` (ADR-035, putusan H-014).
Dikoreksi pada commit ini sesudah pembacaan retroaktif atas `8feef37b` (lihat bagian 11).
Waktu penulisan: 2026-07-27 ~05:27 WIB.

Berkas ini adalah **penyerahan lintas-sesi dan lintas-akun**. Sesi berikutnya mungkin dijalankan oleh
akun yang tidak memiliki riwayat percakapan apa pun. Karena itu berkas ini harus cukup berdiri sendiri.

---

## 0. Cara memakai berkas ini

Tempelkan ke sesi baru:

> Baca `PROMPT_KELANJUTAN.md` lalu `STATE.md` di repo publik GitHub `EnVyxS/lux-research` (branch `main`)
> **secara utuh** sebelum melakukan apa pun. Jangan membaca `journal/` seluruhnya — hanya dua entri
> terakhir. Jangan mulai dari awal. Jangan mengulang pekerjaan yang sudah selesai. Lanjutkan dari
> bagian 6 berkas ini.

**Urutan wajib**: `PROMPT_KELANJUTAN.md` → `STATE.md` (38+ aturan bernomor di bagian 1 — **jangan** menulis
ulang dari ingatan) → dua jurnal terakhir → dua ADR terakhir. Baru bekerja.

---

## 1. Proyek

Sistem dagang kuantitatif untuk **Binance USD-M Futures**, dibangun ulang dari nol. Seluruh pengetahuan
dari upaya sebelumnya (termasuk log sinyal bot v8.4) **sengaja dibuang** karena tercemar survivorship
bias dan overfitting. Mesin lokal tidak sanggup backtest penuh dan tidak ada VM cloud, jadi:

- **seluruh komputasi berjalan di GitHub Actions**;
- **repo GitHub adalah penyimpanan data sekaligus jurnal riset**.

## 2. Batas alat (semua masih berlaku, semua terbukti)

- Sandbox tanpa jaringan. Log workflow **tidak terbaca** dan **tidak ada satu pun fungsi Actions** di
  alat GitHub. Karena itu setiap workflow **menulis hasil ke `reports/` lalu commit balik**.
- Workflow dipicu lewat **filter `paths` pada berkasnya sendiri**: menyentuh `.github/workflows/x.yml`
  langsung memulai run x. Konsekuensi: **jangan** menyentuh berkas workflow hanya untuk memperbaiki
  kosmetik — perbaikan harus **menumpang** run berikutnya yang memang dikehendaki.
- `search_code` **nol hasil** di repo ini. `get_file_contents` menuntut SHA 40 karakter penuh tetapi
  menerima `ref:"main"` dan menerima path direktori untuk daftar isi. **Pada direktori ia memberi
  ukuran tiap berkas tanpa menarik isinya** — cara termurah mengadili ramalan ukuran laporan.
- Menulis memakai `push_files`, yang **MENGGANTI SELURUH ISI BERKAS** → **baca dulu sebelum menulis
  ulang**. **Bentuk panggilan yang benar**: `{ toolName: "push_files", toolArguments: { owner, repo,
  branch, message, files } }` — `owner`/`repo`/`branch` masuk **di dalam** `toolArguments`, bukan di
  tingkat atas panggilan. Teks Python di repo ini memuat escape Unicode literal (`\u00b7`, `\u2014`)
  dan f-string berkutip bersarang — salin apa adanya saat membaca ulang sebelum menyunting.
- `fapi.binance.com` HTTP **451 permanen**; CDN `data.binance.vision` tetap 200.
- Runner: python 3.12.13, numpy 2.5.1, pytest 9.1.1, pandas 2.2.3, pyarrow 17.0.0. **Tanpa scipy,
  tanpa requests.** 4 vCPU / 15 GB, batas 6 jam per job.
- **Kabar buruk datang cepat, kabar baik datang lambat**: gagal dalam 23–32 detik, lulus ±20 menit
  untuk 1h (kecuali `tests.yml`, yang memberi kabar **baik** dalam ~23 detik juga — jangan membaca
  cepatnya laporan uji sebagai kegagalan, baca isinya). Diamnya laporan **bukan** tanda lolos. Commit
  laporan tanpa berkas hasil = run **GAGAL**. Blob laporan yang SHA-nya tidak berubah = belum ditulis,
  run belum selesai. **Verifikasi lewat `list_commits`, jangan berasumsi.**
- **Dua dorongan berurutan ke `lux/**` melahirkan DUA run `tests.yml`**, dan keduanya wajib diadili
  terpisah. Laporan run yang lebih dulu **tertimpa** oleh run berikutnya di `main`, tetapi masih
  terbaca dengan `get_file_contents` memakai **SHA commit laporan itu**, bukan `ref:"main"`.
- **Pekerjaan matriks yang bergantung pada keluaran pekerjaan lain wajib `git fetch` +
  `git checkout origin/main -- reports`.** Checkout bawaan berada pada SHA pemicu, yang **mendahului**
  seluruh commit pecahan — pelajaran mahal dari `h013b.yml`, relevan lagi bila pola matriks dipakai
  ulang (mis. riset funding atau geometri lanjutan).
- **Peringatan waktu (dipelajari 2026-07-27):** H-014 dua sel 4h selesai dalam **2 menit 19 detik**.
  Waktu run 1h yang lama didominasi **unduhan**, bukan komputasi. Jangan menyimpulkan "terlalu cepat =
  gagal" — saya melakukan itu dan **salah**. Baca lognya.
- Rilis diunggah runner. Rilis aktif: **`tier-b-v1`**, id `359778114`; berkas 4h: 12 berkas,
  157.628.619 B (run mengunduh 16 berkas / 157M).

## 3. Posisi riset — 14 hipotesis dinilai, **14 DITOLAK**

| Hipotesis | Putusan |
|---|---|
| H-001b … H-009, H-011 | DITOLAK (11 buah). H-011 juga **tercemar** — seluruh angkanya dari satu simbol `USDCUSDT` |
| H-010 | lulus pada 40 simbol dengan empat keberatan, lalu p-value **gagal** pada 300 permutasi (0,0631) |
| H-012 | DITOLAK (0,041713R < 0,05R) |
| H-013 | DITOLAK (Jalur B, run 30217516013): besaran +0,054842R tetapi **p bulanan 0,205980** |
| **H-014** | **DITOLAK** (run 30221967019): rerata selisih bulanan **−0,027715R** < 0,020R, **p 0,375962** > 0,05 |

Himpunan hipotesis tertahan **sudah habis**. Dimensi bersih yang tersisa: **kerangka 4h** (sudah dipakai
H-014) dan **funding sebagai SINYAL** (belum pernah diuji sama sekali).

### Angka H-013 (run 30214203863, empat sel)

`SS +0.06664781299919262` (60.018 trade) · `SH +0.037166633609032385` (44.614) ·
`AS +0.01180570125176449` (55.927) · `AH +0.05817042814276683` (45.378).
`sumbangan_sinyal_R 0.05484211174742813` · `sumbangan_geometri_R 0.029481179390160234` ·
interaksi `0.07584590628116258` · `SH−AH −0.021004`.

### Angka H-014 (run 30221967019, pemicu `52c64ac5`, laporan `603477ce`, log blob `03e0c35c`)

- **SS′** (`pakai_target True`, umur 48), 56,9 s: ekspektasi **0.06725203533326735**, trade **59.324**,
  jendela positif 2229/4082, keluar `{target 18667, stop 33748, umur 5174, akhir_data 1735}`, 73 bulan,
  gerbang gagal `['invarian_risiko','checksum','funding_ekor']`, entri acak nyata 0.07085R p 0.016611,
  std 1.37827R, galat baku 0.005659R (+3,05 SE), drop-1 0.06639R (retensi 0.9872), drop-22 0.05419R,
  median simbol +0.06789R, porsi bruto teratas 0.0139 (SANDUSDT), 309 untung/128 rugi,
  funding maks 0.8285R, parameter terpilih {55:836, 20:1711, 100:1535}, sidik `197c10e3f0d2`.
- **SH′** (`pakai_target False`, umur 48), 52,6 s: ekspektasi **0.03959765698185091**, trade **44.538**,
  jendela positif 1982/4082, keluar `{umur 14426, stop 28013, akhir_data 2099}`, 73 bulan, gerbang gagal
  `['entri_acak','invarian_risiko','checksum','funding_ekor']`, entri acak nyata 0.06363R p 0.219269,
  std 2.20818R, galat baku 0.010463R (−0,99 SE), drop-1 0.03583R (retensi 0.9047), drop-22 0.01225R,
  median simbol +0.02710R, porsi bruto teratas 0.0431 (VELVETUSDT), 234 untung/203 rugi,
  funding maks 2.9000R (juga gagal `porsi_trade_di_atas_pengaman`), parameter {55:1073, 20:1995, 100:1014},
  sidik `5721a88e59eb`.
- **Adjudikasi**: `besaran_rerata_bulanan_R` **−0.027715128544164157**, `besaran_agregat_R`
  **+0.027654378351416438**, `rerata_berbobot` **−0.012499029724652699**, `median_selisih`
  **+0.03495217650445759**, `fraksi_positif` 0.5616438356164384, `p` **0.37596240375962403**
  (m 3759, ulangan 10000, seed 20260727), bootstrap **[−0.09067851377334449, +0.029103950604927244]**
  (seed 20260728), n_pasangan 73, `memenuhi_adr015: false`.

### Temuan paling penting dari H-014 (lebih penting daripada putusannya)

**Tanda besaran bergantung pada pembobotan.** Satu himpunan 73 bulan yang sama: agregat **+0,027654R**
(positif), rerata bulanan **−0,027715R** (negatif), berbobot trade −0,012499R (negatif), median bulanan
+0,034952R (positif). Bila pemilihan pembobotan dibiarkan bebas, H-014 **melewati** ambang besaran.
Yang mencegahnya bukan kehati-hatian, melainkan bahwa `adjudikasi` membaca `rerata_selisih` dan kode itu
dikomit **sebelum** ada satu angka pun. **Cacat kelas keenam belas. Aturan 55.**

## 4. Ambang pra-registrasi (BEKU — jangan digeser)

**ADR-015 (kaki sinyal):** `SS − AS ≥ 0,020R`, `p ≤ 0,05`, `≥300 ulangan`, `≥100 trade per sel`.
Kurang dari itu = **TIDAK DAPAT DINILAI**, bukan gagal.

**Kaki geometri (BARU, dibekukan 2026-07-27, ADR-034):** ambang besaran 0,020R, ambang p 0,05,
satuan penarikan **bulan**, ulangan 10000, seed 20260727. Putusan yang mungkin **hanya** `DITOLAK` atau
`TIDAK DAPAT DINILAI` — H-014 **tidak dapat lulus secara desain** (`PEMBATAS`), karena +0,029481R yang
hendak dilampauinya sendiri sudah tercemar (cacat 14).

Kegagalan gerbang `lookahead`+`entri_acak` di sel AS/AH dan `invarian_risiko` di SH/AH **BUKAN temuan**
(ADR-021). Kegagalan `checksum` pada 4h saat ini **mustahil lulus** (cacat 17, lihat bagian 6).

## 5. Aturan kerja dengan saya

- Ketika saya menulis "lanjut" / "lanjutkan", **teruskan langsung tanpa konfirmasi**.
- **Pisahkan fakta terverifikasi** (punya commit / run ID / kutipan) **dari asumsi**. Bila belum
  terverifikasi, katakan: **"Ini memerlukan verifikasi."**
- Katakan bila saya salah. Katakan bila kamu sendiri salah. **Jangan menghaluskan ramalan yang meleset.**
- **Perbarui `STATE.md` tiap kali posisi berubah.** Tambah entri `journal/` **tiap sesi**, ditulis
  **SEBELUM** hasil run terlihat bila membahas ramalan. Segarkan berkas ini sebelum konteks penuh.
- Setiap sesi harus membekukan **ramalan bernomor** sebelum run, lalu **mengadjudikasinya** sesudah.

## 6. Tugas tertunda, menurut prioritas

1. **`STATE.md` v28 belum ditulis.** v27 = `a3355294`; ia masih menyatakan run H-014 sedang berjalan.
   v28 harus memuat: putusan H-014, aturan **55** dan **56**, cacat kelas **16** dan **17**, ADR-035,
   jurnal 32, dan pembatalan sebagian klaim ADR-033. **Baca blob v27 UTUH lebih dahulu.**
2. **Cacat 17 — perbaiki daftar `git add` di `.github/workflows/h014.yml`** agar memuat
   `reports/manifest_aset_4h.json`. Berkas itu **dilahirkan run tetapi tidak ada di `main`** (terbukti:
   "The path does not point to a file or directory"), sehingga gerbang `checksum` pada 4h **mustahil
   lulus selamanya**. **Jangan** didorong sendirian (memicu run) — **tumpangkan** pada run 4h berikutnya.
   Sesudah itu adjudikasi **paruh kedua R-B1**.
3. **Anomali `buat_konfig`** — SH (H-013) dan SH′ (H-014) **nominal identik** (sinyal nyata, tanpa
   target, umur 48) tetapi memberi 44.614/+0,037167R lawan 44.538/+0,039598R, dan cacah lookback
   terpilih bergeser (1987/1069/1026 lawan 1995/1073/1014). Satu-satunya beda jalur kode:
   `buat_konfig=buat_konfig_sel(sel)` lawan `None`. Jadi jalur itu **bukan no-op**.
   **Ini memerlukan verifikasi. Baca `walk_forward.py` dan `run_wf.py` UTUH sebelum menduga apa pun.**
   Sampai terjawab, SS′ − SH′ **tidak boleh** disebut "SS − SH yang sudah diperbaiki".
4. **`AH = +0,05817042814276683R` masih TIDAK TERJELASKAN.** Keberatan B ADR-032 (penjelasan penyebut)
   sudah **difalsifikasi** oleh `engine.py`. Entri acak seharusnya tidak menghasilkan +0,058R.
5. **Funding sebagai SINYAL** — belum pernah diuji. Datanya sudah ada di `tier-b-v1`. Pra-registrasi
   penuh **sesudah** membaca setiap modul yang disebutnya (jangan ulangi kesalahan merancang di atas
   modul yang belum dibaca — itu sudah terjadi **tiga kali**). Gerbang p bulanan **wajib** (ADR-031 §5).
6. **Selidiki kegagalan `invarian_risiko` + `checksum` + `funding_ekor`** lewat skrip ringkasan di sisi
   runner. **Jangan** menarik JSON 432 KB ke dalam konteks.
7. **Selesaikan soal bar datar 1h lawan 4h**: `reports/diag_datar.json` lawan perhitungan 4h; penolakan
   4h seharusnya **≤ 74**. `maks_rasio_bar_datar` **belum tersambung** ke gerbang (aturan 39: audit
   kunci config lain yang tidak pernah dibaca — itu cacat kelas kedelapan).
8. **Hapus komentar yang salah indentasi** di `run_h014.medan_berbeda` — **selalu menumpang**, jangan
   didorong sendirian.
9. **Nasib workflow**: `notion_asap.yml` satu-satunya tanpa `git pull --rebase --autostash`;
   `backfill_daily.yml` satu-satunya terjadwal (`cron: '0 2 * * 1'`). Tinjau `funding.yml`,
   `funding_check.yml`, `doctor.yml`, `universe.yml`. **Tidak ada penghapusan tanpa keputusan tertulis.**
10. **Belum diadjudikasi**: R-B4 (p bulanan berbobot trade), ADR-016 ramalan 5.
11. **Bandingkan** `runner.py` lawan `fc79e070` dan `run_h013.py` lawan `418f6084` untuk prosa yang melapuk.
12. Utang ekor panjang: `hasattr`/`__import__` di `test_run_h012.py`; uji `biaya_bolak_balik_R`;
    `pytest` ke `requirements-dev.txt`; tripwire `inspect.getsource` yang lemah; pemetaan `dari_laporan`
    pelapor Notion; perketat `lux/funding.py::gerbang_lulus`; salin ADR-001/002 ke `decisions/`;
    naikkan `versi` config; **Tier A (1m) hanya sesudah semua gerbang Tier B lulus dengan ≥24 pecahan**.

## 7. Larangan (jangan dilanggar, semuanya berdasar)

- **Jangan menyatakan sistem siap dagang.** Empat belas hipotesis, empat belas ditolak.
- Jangan mengutip `+0,060163R` (H-010 tanpa USDCUSDT) atau `+0,059636R` (H-012 seluruh riwayat) sebagai
  kelulusan — keduanya pemilihan pasca-hasil.
- Jangan mengutip `+0,054842R`, `+0,043732R`, atau `+0,066648R` sebagai kelulusan atau kelayakan H-013;
  `+0,054842R` juga haram dikutip sebagai besaran apa pun **tanpa menyebut seed 42**. Jangan mengutip
  `+0,029481R` sebagai kelulusan geometri — ia tercemar (cacat 14).
- Kata **LULUS** pada `reports/backtest_h013_kontribusi.md` haram dikutip. **p 0,001100** tingkat simbol
  haram dikutip sebagai keberartian. **Setiap p atau galat baku per perdagangan** haram dipakai sebagai
  bukti keberartian, termasuk **0,003322** dan "+2,99 galat baku". **Prosa R-D3 di `reports/h013b_p.md`
  haram dipakai sebagai penilaian atas kesehatan permutasi** — ia terbantah dan sengaja tidak ditulis ulang.
- Jangan menyebut H-012/H-013/H-014 sebagai "H-010 sesudah perbaikan".
- Jangan menghitung ulang H-001b … H-012 dengan mesin ADR-016.
- Jangan membuang simbol atau memilih bulan **sesudah** melihat hasil. Jangan membuang simbol merugi.
  Jangan memilih satuan penarikan sesudah hasil terlihat.
- Jangan memakai gerbang konsentrasi / `funding_ekor` sebagai penyaring simbol.
- Jangan melombakan ambang pengaman. Jangan menjadikan `stop_hormati_celah` parameter yang dilombakan.
- **Jangan menggeser**: lantai 0,004 · pagar 0,5R · `BATAS_VOID` 20 · batas tanggal 2026-01-01 ·
  ambang SS−AS 0,020R · `MAKS_RASIO_DATAR` 0,10 · ambang rasio 0,30 · ambang ekspektasi 0,05R ·
  `invarian_risiko` −1,5R.
- Jangan mematok `imbalan_R` ke 8,0. Jangan menurunkan `--ulangan` dari 300. Jangan menaikkan
  `maks_umur_bar` dari 168.
- Jangan menandai putusan DITOLAK sebagai kegagalan pekerjaan — hasil yang menjatuhkan hipotesis dengan
  kode keluar 0 adalah alat yang bekerja benar (aturan 48).
- Agen otonom "LUX Gatekeeper" dan "LUX Gatekeeper Reporter" **tidak dipakai lagi**. Kolom Verdict di
  database Notion "LUX — Run Results" sekarang **kolom manusia**.

## 8. Aturan 47–56 (ringkas; 1–46 ada di `STATE.md` bagian 1 — itulah versi yang mengikat)

47. Alat yang selalu menghasilkan angka tidak menjaga apa pun.
48. Hasil yang membunuh hipotesis keluar dengan kode 0.
49. Besaran juga dilaporkan terhadap rerata null, dan dilaporkan dua kali.
50. Prosa yang difalsifikasi diperbaiki di sumbernya; artefak yang sudah dikomit tidak pernah ditulis ulang.
51. Sumber dan pengujiannya adalah satu commit.
52. Sel pembanding boleh berbeda dalam **tepat SATU** medan.
53. Ambang boleh disebut beku hanya bila ia beku **untuk besaran yang sedang diuji**.
54. Ramalan cacah uji dihitung dari **berkas yang benar-benar didorong**; bila ramalan dan berkas
    berselisih, yang salah **selalu** ramalannya.
55. **Besaran yang tandanya bergantung pada pembobotan bukan besaran.** Agregat, rerata, berbobot, dan
    median **semuanya** wajib dilaporkan, dan putusan wajib menyebut **yang mana yang mengikat**.
56. **Berkas yang dibutuhkan sebuah gerbang agar dapat lulus wajib ada di daftar `git add`.**
    Daftar `git add` adalah bagian dari gerbang.

## 9. Rantai commit terakhir (naik)

`d8cc4ecc` (ADR-034+j30) → `4af21176` (kode H-014, 855 uji) → `4795767b` (laporan uji, run 30221837845)
→ `17ef54f7` (jurnal 31, aturan 54) → `52c64ac5` (`h014.yml`, memicu run **30221967019**)
→ `603477ce` (laporan H-014, 21:54:44Z) → `a3355294` (STATE v27) →
`a25160ca4a238fbb5b652bd4839ed9917183dcba` (ADR-035 + jurnal 32) → `d49aab94` (berkas ini, v1) →
**berkas ini (v2, dikoreksi)**.

**Berikutnya bebas:** `decisions/ADR-036.md` · `journal/2026-07-27-33.md` · `STATE.md` v28.
Penamaan ADR: `ADR-0NN.md` telanjang sejak 015. Cacah uji sekarang **855**.

## 10. Kesalahan saya sendiri yang paling mahal, supaya tidak terulang

- **Merancang di atas modul yang belum dibaca — tiga kali.** Dijurnalkan di jurnal 30 apa adanya:
  "Pelajaran yang dijurnalkan tanpa mengubah urutan kerja bukan pelajaran." **Baca modulnya dahulu,
  baru sebut namanya di ADR.**
- **Menyimpulkan "2 menit 19 detik berarti run gagal".** Run itu berhasil.
- **R-H1 meleset karena aritmetika saya sendiri**, bukan karena runner: 850 diramal (819+31) padahal
  berkas yang didorong memuat 20+16=36 → 855. Dapat ditemukan tanpa menjalankan apa pun.
  Deret 21 ramalan tepat berturut-turut **putus**.
- **R-G4 meleset jauh**: saya meramal >80% trade SH′ keluar lewat `umur`; nyatanya 32,4%, dan `stop`
  tetap penguasa 62,9%. Menghapus target tidak membuat posisi dipegang sampai waktu habis — ia membuat
  posisi dipegang sampai stop kena, dan stop biasanya kena lebih dahulu.
- **"226 jendela / 63,5%"** yang nyatanya **194 / 54,5%** — ditulis dari ingatan. Jangan mengutip angka
  dari ingatan; kutip dari blob.
- **Menulis ulang berkas ini (v1, `d49aab94`) tanpa membaca `8feef37b` lebih dahulu**, melanggar aturan
  push_files sendiri. Lihat bagian 11.

## 11. Koreksi retroaktif (dicatat, bukan disembunyikan)

Commit `d49aab94` (v1 berkas ini) ditulis **tanpa** membaca `8feef37b` (versi sebelumnya) lebih dahulu.
Saya beralasan saat itu bahwa berkas ini memang harus diganti seluruhnya dengan posisi terkini — alasan
yang salah, karena itu justru argumen untuk membaca dulu, bukan melewatkannya: saya tidak tahu apakah
versi lama memuat sesuatu yang unik. Pengguna mempertanyakannya secara langsung. Pembacaan retroaktif
atas blob `8feef37b4edc8e862cafe97eb745a0dfeae22619` menemukan **lima kehilangan nyata**, semuanya
dikembalikan pada commit ini (lihat bagian 2 dan 7). Mitigasi yang membuat ini bisa diperbaiki:
`push_files` menimpa `main`, tetapi commit lama tetap ada di riwayat git — tidak ada yang musnah, hanya
sempat tidak terlihat.
