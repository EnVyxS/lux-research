# PROMPT KELANJUTAN — Riset LUX (v3)

> Berkas ini adalah **titik masuk sesi baru**. Dibuat 2026-07-27 pada commit induk `bfc5bef7f05419045ad6cc06c19b2a9be3f65dda` (STATE v31). Menggantikan v2 (blob `f9223c30294bfa93ac12daab3dcf8ad329125220`).

---

## 0. Urutan membaca, mengikat

Jangan mulai dari awal. Jangan mengulang pekerjaan yang sudah selesai. Baca dalam urutan ini, **utuh**, bukan sekilas:

1. **`STATE.md`** — posisi riset. Termasuk **58 aturan bernomor** di bagian 1. **JANGAN menulis ulang aturan dari ingatan.**
2. **`STATE_LAMPIRAN.md`** — arsip rinci: peta repo, inventaris modul, audit workflow, batas alat, papan ramalan, angka H-012/H-013. STATE dan lampirannya adalah **satu dokumen yang dipecah dua** karena muatan dorongan pernah terpotong; membaca salah satu saja berarti membaca separuh posisi.
3. **`decisions/ADR-037.md`** — pra-registrasi H-015 yang **sedang berjalan sebagai pekerjaan berikutnya**. Ini yang paling menentukan apa yang boleh ditulis selanjutnya.
4. **`decisions/ADR-036.md`** — cacat 18, anomali SH ≠ SH′.
5. **Dua jurnal terakhir**: `journal/2026-07-27-36.md` dan `journal/2026-07-27-37.md`. **JANGAN membaca `journal/` seluruhnya.**

Bila sesuatu tidak tercatat di STATE atau lampirannya, **anggap belum diketahui**.

---

## 1. Posisi dalam satu paragraf

Empat belas hipotesis dinilai, **empat belas ditolak**, nol kandidat bertahan. H-014 ditolak (ADR-035) dan kemudian ketahuan berjalan dengan pengaman risiko **mati** (cacat 18, ADR-036) — putusannya **tidak berubah**, yang gugur adalah kesebandingan lintas hipotesis. **H-015 sudah TERDAFTAR lewat ADR-037** tetapi **belum ada satu baris kodenya**. Repo memuat **58 aturan**, **19 kelas cacat**, **872 uji**.

---

## 2. Tugas berikutnya, berurutan

1. **Tulis kode H-015 menurut ADR-037** — saringan funding lewat `Jadwal.statistik_trailing`, tiga sel **K / F / A**, penolakan acak setara berseed, dan runner yang **wajib**: memanggil `konfig_audit.laporan_kesebandingan` dengan `pengaman_wajib = {"maks_carry_realisasi_R": 0.25, "maks_carry_R": 0.25}`, menaruh `asdict(konfig)` **utuh** per sel di manifes, dan **berhenti berkode keluar bukan nol** bila `pengaman_mati` tidak kosong. Sumber dan pengujiannya **satu commit** (aturan 51). Ramalan cacah uji berbunyi **"paling sedikit 884"** (aturan 58).
2. **Cacat 17** — sunting daftar `git add` di workflow **bersamaan** run 4h H-015, **tidak digabung** ke commit kode. Lalu adjudikasi paruh kedua R-B1.
3. **R-J1** — cacah keluar `carry` sel SH dari `reports/backtest_h013_sh_sinyal_horizon.json` lewat skrip sisi runner. **Jangan menarik JSON 432 KB ke konteks.**
4. **Uji ke-17** — satu dorongan yang **hanya** menyentuh `tests/`, lalu bandingkan delta.
5. **Cacat 19** — medan satuan/pembobotan/p bulanan pada `praregistrasi.Kriteria`. **Sesudah** H-015 berjalan.

Nomor ADR bebas berikutnya: **ADR-038**. Jurnal berikutnya: **`journal/2026-07-27-38.md`**.

---

## 3. Ambang beku — tidak digeser, tidak ditawar

lantai 0,004 · pagar 0,5R · `BATAS_VOID` 20 · potong tanggal 2026-01-01 · besaran antar sel 0,020R · **p ≤ 0,05 pada satuan bulan kalender UTC** · ≥300 ulangan · ≥100 trade per sel · `MAKS_RASIO_DATAR` 0,10 · rasio 0,30 · ekspektasi 0,05R · `invarian_risiko` −1,5R · `maks_umur_bar` ≤ 168 · gerbang kesebelas 0,35 / 0,50R / 0,005.

**Pengaman carry `maks_carry_realisasi_R` = 0,25**, dan asal-usulnya berlapis tiga — catat ini, sebab saya sudah salah **dua kali** di sini:

| Lapisan | Dokumen |
|---|---|
| Medan dan mekanismenya (bawaan `0.0` = MATI) | **ADR-008** |
| 0,25 dipatok sebagai batas yang **tidak dilombakan** | **ADR-009** |
| Asal angka 0,25 (`config/lux.yaml` v2) | **ADR-004** |

Baru di ADR-037: **`AMBANG_RATE` = 0,0001** dan **`MIN_PENAGIHAN` = 30**, dibekukan 2026-07-27.

---

## 4. Angka yang HARAM dikutip sebagai kelulusan

`+0,029481R` · `+0,027654R` sebagai besaran lulus · `+0,054842R` / `+0,043732R` / `+0,066648R` sebagai kelulusan · `+0,060163R` · `+0,059636R` · p 0,001100 (satuan simbol) · p 0,003322 dan "+2,99 galat baku" · kata "LULUS" di `reports/backtest_h013_kontribusi.md` · prosa R-D3 di `reports/h013b_p.md` · ambang ADR-015 §4.4 sebagai pra-registrasi geometri · "226 jendela / 63,5%" (benar 194 / 54,5%) · **angka H-014 dibandingkan langsung dengan H-013** · **angka H-015 dibandingkan langsung dengan H-014** · **F − K sebagai dasar kelulusan H-015**.

**Larangan permanen:** jangan menyatakan sistem siap diperdagangkan · jangan menambah cabang `LULUS` ke H-014 · jangan menambal `berpasangan.py` · jangan menjalankan ulang H-014 dengan pengaman carry dinyalakan · jangan menggeser `AMBANG_RATE`, `MIN_PENAGIHAN`, atau seed H-015 sesudah hasil terlihat · jangan menulis aritmetika funding kedua di luar `funding_model` · jangan menyentuh `lux/strategi/`.

---

## 5. Batas alat, terverifikasi

- **Tidak ada fungsi GitHub Actions.** Run dipicu dengan **menyentuh berkas workflow**; verifikasi lewat `list_commits`.
- **Menyentuh `h014.yml` / `backtest.yml` / `h013b.yml` memulai run 4h.** Jangan menyentuhnya untuk perbaikan kecil sendirian.
- `tests.yml` selesai ~23 detik; laporan dikomit oleh `lux-tests` dengan `[skip ci]`.
- `STATE.md`, `STATE_LAMPIRAN.md`, `journal/`, `decisions/` **tidak** memicu `tests.yml`.
- `search_code` mengembalikan nihil pada repo ini — pakai `get_file_contents` atas jalur direktori (menerima `"/"`, mengembalikan ukuran + SHA per berkas).
- Bentuk panggilan yang bekerja: `push_files` `{owner, repo, branch, message, files:[{path, content}]}` — **penggantian berkas utuh**; `get_file_contents` `{owner, repo, path, ref}` (`ref` menerima `"main"`, SHA commit, jalur direktori); `list_commits` `{owner, repo, sha, path?, perPage}` — `path` bekerja sebagai saringan lintasan.
- Runner: python 3.12.13, numpy 2.5.1, pytest 9.1.1, pandas 2.2.3, pyarrow 17.0.0, **tanpa scipy/requests**; 4 vCPU / 15 GB; batas 6 jam.
- `fapi.binance.com` → 451; `data.binance.vision` → 200. Rilis `tier-b-v1` id `359778114`, aset 4h 12 berkas / 157.628.619 B.
- `backfill_daily.yml` cron `'0 2 * * 1'`.

### BATAS MUATAN DORONGAN — pelanggaran nyata, bukan teori

Muatan `push_files` yang panjang **dapat terpotong diam-diam** dan tetap dikomit. Itu terjadi pada `STATE.md` v28 (commit `56633f80`), yang menyimpan posisi tak lengkap di `main` selama ~3,5 jam. Percobaan mendorong ulang seluruh `STATE.md` sekali muat pernah dibalas **"The tool call was canceled by the user."**

**Mitigasi wajib (aturan 35):**
1. Berkas panjang **dipecah** — itulah sebab `STATE_LAMPIRAN.md` ada.
2. Setiap dorongan panjang **dibaca ulang dari `main` sesudah dikirim**, dua lapis: daftar direktori untuk ukuran, lalu **pembacaan utuh** untuk memastikan **ekornya hadir**. Ukuran saja tidak cukup.

---

## 6. Cacat yang masih terbuka

- **Cacat 18 — dibayar sebagian.** `lux/backtest/konfig_audit.py` + 16 ujinya ada di `main` (`65916ec6`), tetapi **belum dipanggil satu run pun**; aturan 42 berlaku atas alat saya sendiri. Penutupnya adalah runner H-015, **dan buktinya adalah R-L5**: alasan keluar `carry` harus muncul dengan cacah bukan nol. Bila tetap nol, cacat 18 terbuka penuh lagi meski `konfig_audit` melaporkan hijau.
- **Cacat 17 — terbuka.** `reports/manifest_aset_4h.json` tidak pernah dikomit, sehingga gerbang `checksum` pada 4h mustahil lulus. Sampai diperbaiki, kegagalannya wajib dibaca sebagai **cacat alat**.
- **Cacat 19 — terbuka.** `praregistrasi.Kriteria` tidak dapat menyatakan satuan penarikan, pembobotan mengikat, maupun p bulanan; medan `min_jendela_positif_rasio` bahkan mengunci satuan yang sudah ditinggalkan.
- **Uji ke-17 — belum terjelaskan.** 872 nyata lawan 871 yang diramalkan; enam berkas uji dan `tests.yml` sudah dieliminasi. **Ini memerlukan verifikasi.**
- `AH = +0,05817042814276683R` tak terjelaskan · rasio bar datar 4h belum dibaca · `notion_asap.yml` tanpa `git pull --rebase --autostash` · tiga kunci `config/lux.yaml` tidak dibaca program.

---

## 7. Ramalan H-015 yang sudah dibekukan (ADR-037 §9)

Ditulis **sebelum** run. Jangan menghaluskan yang meleset, jangan mengaku sudah menduga sesudahnya.

- **R-L1** F menolak long >3× short — *dijamin konstruksi, tidak bernilai, ditandai begitu di muka*.
- **R-L2** **H-015 DITOLAK** (rerata bulanan F−A < +0,020R).
- **R-L3** |F−A| < |F−K| — bila **salah**, funding memuat informasi arah dan itu lebih berharga daripada H-015 yang lulus.
- **R-L4** cacah uji **paling sedikit 884**.
- **R-L5** keluar `carry` bukan nol pada ketiga sel.

---

## 8. Aturan kerja dengan pengguna

- Bila pengguna menulis **"lanjut"** atau **"lanjutkan"**, teruskan **tanpa meminta konfirmasi**.
- Pisahkan **fakta terverifikasi** (punya commit / run ID / kutipan) dari **asumsi**; bila belum terverifikasi, katakan **"Ini memerlukan verifikasi."**
- Katakan bila pengguna salah. Katakan bila **kamu sendiri** salah — termasuk bila **koreksimu sendiri** ternyata salah; itu sudah terjadi (jurnal 37).
- Jangan menghaluskan ramalan yang meleset.
- Perbarui `STATE.md` tiap posisi berubah; tambah satu entri `journal/` tiap sesi, **ditulis sebelum hasil run terlihat** bila membahas ramalan; segarkan berkas ini sebelum konteks penuh.

---

## 9. Rantai commit terakhir

`4af21176` (kode H-014, 855 uji) → `52c64ac5` (pemicu run `30221967019`) → `603477ce` → `a3355294` (v27) → `a25160ca` → `e34961f5` → `56633f80` (**v28 terpotong**) → `7869b7d5` (lampiran) → `f065fe92` (v28 utuh) → `03b5fc92` → `a9cbb4e8` (ADR-036) → `5474df2b` (v29) → `65916ec6` (`konfig_audit` + 16 uji) → `61504ef6` (**872 uji**) → `d62f2df9` → `11a0cafb` (v30) → `a326932a` (jurnal 37) → `08e21b3f` (**ADR-037**) → **`bfc5bef7` (STATE v31)**.

**Posisi: 14 hipotesis dinilai, 14 DITOLAK, 1 terdaftar belum dijalankan. 58 aturan. 19 kelas cacat. 872 uji.**
