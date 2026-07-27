# PROMPT KELANJUTAN — Riset LUX (v4)

> Berkas ini adalah **titik masuk sesi baru**. Dibuat 2026-07-27 pada commit induk `2e191e5fc60f35431c49e5e0d88e39c119a19449` (jurnal 39). Menggantikan v3 (blob `9bba28e874a78edd6ba8abe745b1bd1736d29ce4`).

---

## 0. Urutan membaca, mengikat

Jangan mulai dari awal. Jangan mengulang pekerjaan yang sudah selesai. Baca dalam urutan ini, **utuh**, bukan sekilas:

1. **`STATE.md`** — posisi riset. Termasuk **58 aturan bernomor** di bagian 1. **JANGAN menulis ulang aturan dari ingatan.** Perhatikan: pada saat berkas ini ditulis, STATE masih **v31** (`bfc5bef7`) dan **belum memuat H-015 berkode**; lihat §2 butir 0.
2. **`STATE_LAMPIRAN.md`** — arsip rinci: peta repo, inventaris modul, audit workflow, batas alat, papan ramalan, angka H-012/H-013. STATE dan lampirannya adalah **satu dokumen yang dipecah dua** karena muatan dorongan pernah terpotong; membaca salah satu saja berarti membaca separuh posisi.
3. **`decisions/ADR-037.md`** — pra-registrasi H-015. Ini yang paling menentukan apa yang boleh ditulis selanjutnya.
4. **`decisions/ADR-036.md`** — cacat 18, anomali SH ≠ SH′.
5. **Dua jurnal terakhir**: `journal/2026-07-27-38.md` dan `journal/2026-07-27-39.md`. **JANGAN membaca `journal/` seluruhnya.**

Bila sesuatu tidak tercatat di STATE atau lampirannya, **anggap belum diketahui**.

---

## 1. Posisi dalam satu paragraf

Empat belas hipotesis dinilai, **empat belas ditolak**, nol kandidat bertahan. H-014 ditolak (ADR-035) dan kemudian ketahuan berjalan dengan pengaman risiko **mati** (cacat 18, ADR-036) — putusannya **tidak berubah**, yang gugur adalah kesebandingan lintas hipotesis. **H-015 terdaftar (ADR-037) dan kini BERKODE LENGKAP serta hijau**, tetapi **belum menjalankan satu bar pun**: aturan 42 berlaku penuh atasnya. Repo memuat **58 aturan**, **19 kelas cacat**, **942 uji**.

### Keadaan terverifikasi pada penyerahan

| Butir | Nilai | Bukti |
|---|---|---|
| HEAD | `2e191e5fc60f35431c49e5e0d88e39c119a19449` | commit jurnal 39 |
| Uji | **942 lulus, kode keluar 0**, 3,13 s | run `30246906896`, laporan `8bb57075` |
| `lux/backtest/saringan_funding.py` | 12.738 B | `7227647fad46950aea6e120faeb06a187395da2f` |
| `lux/backtest/run_h015.py` | 26.917 B | `aedd23b1716fbc0c23041240690b9f7021e9757c` |
| `lux/backtest/konfig_audit.py` | 7.759 B | `75a5334620befcd4c85fcfc57220ad82618d33f1` |
| `config/lux.yaml` | `maks_carry_R: 0.25` | `8a66f15cf559f64dbebb523a29f21357a9300607` |
| `STATE.md` | v31, 41.900 B | `53e48c0f…` — **usang** |

---

## 2. Tugas berikutnya, berurutan

0. **STATE v32 — UTANG PALING TUA, KERJAKAN LEBIH DAHULU.** v31 masih menyatakan H-015 belum berkode dan mencatat 872 uji. v32 wajib memuat: `saringan_funding.py` + `run_h015.py` beserta blob dan ukurannya, cacah **942**, dua run merah sesi ini beserta akar tunggalnya, adjudikasi empat ramalan cacah, R-L4 **terpenuhi**, ramalan baru **R-M1** dan **R-M2**, serta jurnal 39. **Baca blob v31 UTUH lebih dahulu** — jangan menulis dari ingatan, dan **jangan mencoba membaca v31 lalu menulis v32 di jendela konteks yang sama**: itu persis keadaan yang melahirkan v28 terpotong.
1. **Cacat 17** — sunting daftar `git add` di workflow **bersamaan** run 4h H-015, **tidak digabung** ke commit kode. Lalu adjudikasi paruh kedua R-B1.
2. **Jalankan H-015 4 jam**, lalu adjudikasi R-L1…R-L5 dan R-M1. Ingat: menyentuh berkas workflow **memulai run 4 jam** — satu sentuhan, sekali jalan.
3. **R-J1** — cacah keluar `carry` sel SH dari `reports/backtest_h013_sh_sinyal_horizon.json` lewat skrip sisi runner. **Jangan menarik JSON 432 KB ke konteks.**
4. **Uji ke-17** — satu dorongan yang **hanya** menyentuh `tests/`, lalu bandingkan delta.
5. **Cacat 19** — medan satuan/pembobotan/p bulanan pada `praregistrasi.Kriteria`. **Sesudah** H-015 berjalan.

Nomor ADR bebas berikutnya: **ADR-038**. Jurnal berikutnya: **`journal/2026-07-27-40.md`**.

---

## 3. Ambang beku — tidak digeser, tidak ditawar

lantai 0,004 · pagar 0,5R · `BATAS_VOID` 20 · potong tanggal 2026-01-01 · besaran antar sel 0,020R · **p ≤ 0,05 pada satuan bulan kalender UTC** · ≥300 ulangan · ≥100 trade per sel · `MAKS_RASIO_DATAR` 0,10 · rasio 0,30 · ekspektasi 0,05R · `invarian_risiko` −1,5R · `maks_umur_bar` ≤ 168 · gerbang kesebelas 0,35 / 0,50R / 0,005.

**Pengaman carry `maks_carry_realisasi_R` = 0,25**, dan asal-usulnya berlapis tiga — catat ini, sebab saya sudah salah **dua kali** di sini:

| Lapisan | Dokumen |
|---|---|
| Medan dan mekanismenya (bawaan `0.0` = MATI) | **ADR-008** |
| 0,25 dipatok sebagai batas yang **tidak dilombakan** | **ADR-009** |
| Asal angka 0,25 (`config/lux.yaml` v2) | **ADR-004** |

Dari ADR-037: **`AMBANG_RATE` = 0,0001**, **`MIN_PENAGIHAN` = 30**, seed `SEED_ACAK_H015` = 20260727 — dibekukan 2026-07-27.

**Ambang 0,020R dibandingkan dengan float telanjang, dan itu disengaja.** `0.06 - 0.04` bernilai `0.019999999999999997` dan karenanya **TIDAK** lulus. Ada uji yang mengunci perilaku ini. Jangan "memperbaikinya" dengan pembulatan — itu menggeser ambang beku ke bawah, dilarang ADR-037 §10. Selisih 3 × 10⁻¹⁸ tidak akan pernah menentukan putusan; nilainya ada pada disiplinnya.

---

## 4. Angka yang HARAM dikutip sebagai kelulusan

`+0,029481R` · `+0,027654R` sebagai besaran lulus · `+0,054842R` / `+0,043732R` / `+0,066648R` sebagai kelulusan · `+0,060163R` · `+0,059636R` · p 0,001100 (satuan simbol) · p 0,003322 dan "+2,99 galat baku" · kata "LULUS" di `reports/backtest_h013_kontribusi.md` · prosa R-D3 di `reports/h013b_p.md` · ambang ADR-015 §4.4 sebagai pra-registrasi geometri · "226 jendela / 63,5%" (benar 194 / 54,5%) · **angka H-014 dibandingkan langsung dengan H-013** · **angka H-015 dibandingkan langsung dengan H-014** · **F − K sebagai dasar kelulusan H-015**.

**Larangan permanen:** jangan menyatakan sistem siap diperdagangkan · jangan menambah cabang `LULUS` ke H-014 · jangan menambal `berpasangan.py` · jangan menjalankan ulang H-014 dengan pengaman carry dinyalakan · jangan menggeser `AMBANG_RATE`, `MIN_PENAGIHAN`, atau seed H-015 sesudah hasil terlihat · jangan menulis aritmetika funding kedua di luar `funding_model` · jangan menyentuh `lux/strategi/`.

---

## 5. Batas alat, terverifikasi

- **Tidak ada fungsi GitHub Actions.** Run dipicu dengan **menyentuh berkas workflow**; verifikasi lewat `list_commits`.
- **Menyentuh `h014.yml` / `backtest.yml` / `h013b.yml` memulai run 4h.** Jangan menyentuhnya untuk perbaikan kecil sendirian.
- `tests.yml` selesai ~23–30 detik dan **memicu hanya untuk** `lux/**`, `tests/**`, dan `tests.yml` sendiri; laporan dikomit oleh `lux-tests` dengan `[skip ci]`. Alurnya: `set +e` → pytest → tulis `reports/tests.md` → **laporan tetap dikomit meski merah** → langkah "Tegakkan hasil" `exit 1`. Karena itu **laporan merah pun terbaca**, dan itulah cara termurah memeriksa hasil.
- `STATE.md`, `STATE_LAMPIRAN.md`, `journal/`, `decisions/` **tidak** memicu `tests.yml`.
- `search_code` mengembalikan nihil pada repo ini — pakai `get_file_contents` atas jalur direktori (menerima `"/"`, mengembalikan ukuran + SHA per berkas).
- Bentuk panggilan yang bekerja: `push_files` `{owner, repo, branch, message, files:[{path, content}]}` — **penggantian berkas utuh**; `get_file_contents` `{owner, repo, path, ref}` (`ref` menerima `"main"`, SHA commit, jalur direktori); `list_commits` `{owner, repo, sha, path?, perPage}`.
- Runner: python 3.12.13, numpy 2.5.1, pytest 9.1.1, pandas 2.2.3, pyarrow 17.0.0, **tanpa scipy/requests**; 4 vCPU / 15 GB; batas 6 jam.
- `fapi.binance.com` → 451; `data.binance.vision` → 200. Rilis `tier-b-v1` id `359778114`, aset 4h 12 berkas / 157.628.619 B.
- `backfill_daily.yml` cron `'0 2 * * 1'` — tetapi commit `09ba5545` mendarat 06:07 UTC. Isinya belum dibaca. **Ini memerlukan verifikasi.**

### BATAS MUATAN DORONGAN — pelanggaran nyata, bukan teori

Muatan `push_files` yang panjang **dapat terpotong diam-diam** dan tetap dikomit. Itu terjadi pada `STATE.md` v28 (commit `56633f80`), yang menyimpan posisi tak lengkap di `main` selama ~3,5 jam. Percobaan mendorong ulang seluruh `STATE.md` sekali muat pernah dibalas **"The tool call was canceled by the user."**

**Mitigasi wajib (aturan 35):**
1. Berkas panjang **dipecah** — itulah sebab `STATE_LAMPIRAN.md` ada.
2. Setiap dorongan panjang **dibaca ulang dari `main` sesudah dikirim**, dua lapis: daftar direktori untuk ukuran, lalu **pembacaan utuh** untuk memastikan **ekornya hadir**. Ukuran saja tidak cukup.
3. **Jangan membaca berkas 40 KB lalu menulis penggantinya dalam jendela konteks yang sama.**

### PERINGATAN MASUK — uji ditulis dari ringkasan

Dua run merah berturut-turut pada sesi 2026-07-27, akar tunggal: **uji ditulis terhadap ringkasan API saya sendiri, bukan terhadap badan fungsinya.**

1. Boneka `JadwalBoneka` tanpa `__len__` → `TypeError` di `funding_model.py:199`, sebab `ambil_jadwal` memanggil `len(j)` **sebelum** melempar `KeyError`.
2. Fixture membangun konfig dari bawaan `Konfig()` (`maks_carry_R = 0.0`) alih-alih dari `config/lux.yaml` (0,25) → audit benar melaporkan pengaman mati, pada konfig yang tidak pernah dipakai siapa pun.

Keduanya diperbaiki pada **ujinya**, bukan pada modulnya — melonggarkan modul akan membuka kembali lubang yang mematikan H-014. **Baca badan fungsi sebelum menulis boneka atau fixture atasnya.** Di pytest ongkos kesalahan ini tiga detik; di runner 4 jam.

---

## 6. Cacat yang masih terbuka

- **Cacat 18 — dibayar sebagian.** `konfig_audit.py` kini **dipanggil** oleh `run_h015.py`, tetapi runner itu belum berjalan. Penutupnya adalah **R-L5**: alasan keluar `carry` harus muncul dengan cacah bukan nol. Bila tetap nol, cacat 18 terbuka penuh lagi meski `konfig_audit` melaporkan hijau.
- **Cacat 17 — terbuka.** `reports/manifest_aset_4h.json` tidak pernah dikomit, sehingga gerbang `checksum` pada 4h mustahil lulus. Sampai diperbaiki, kegagalannya wajib dibaca sebagai **cacat alat**. Ini dasar utama R-M1.
- **Cacat 19 — terbuka.** `praregistrasi.Kriteria` tidak dapat menyatakan satuan penarikan, pembobotan mengikat, maupun p bulanan.
- **Uji ke-17 — belum terjelaskan.** 872 nyata lawan 871 yang diramalkan. **Ini memerlukan verifikasi.**
- `AH = +0,05817042814276683R` tak terjelaskan · rasio bar datar 4h belum dibaca · `notion_asap.yml` tanpa `git pull --rebase --autostash` · tiga kunci `config/lux.yaml` tidak dibaca program · utang audit config aturan 39.

---

## 7. Ramalan aktif

Ditulis **sebelum** run. Jangan menghaluskan yang meleset, jangan mengaku sudah menduga sesudahnya.

### Dibekukan di ADR-037 §9

- **R-L1** F menolak long >3× short — *dijamin konstruksi, tidak bernilai, ditandai begitu di muka*.
- **R-L2** **H-015 DITOLAK** (rerata bulanan F−A < +0,020R).
- **R-L3** |F−A| < |F−K| — bila **salah**, funding memuat informasi arah dan itu lebih berharga daripada H-015 yang lulus.
- **R-L4** cacah uji ≥ 884 — **TERPENUHI** pada 907, sebelum runner ditulis.
- **R-L5** keluar `carry` bukan nol pada ketiga sel.

### Dibekukan di jurnal 39 §6

- **R-M1** run 4 jam **pertama** H-015 gagal karena sebab **operasional** (jalur, argumen, manifes aset, daftar `git add`), bukan karena putusan ilmiahnya.
- **R-M2** H-015 juga **DITOLAK** — 15 dari 15.

### Catatan adjudikasi cacah uji

Empat ramalan cacah berturut-turut **tepat persis** (905, 907, 940, 942). **Aturan 58 tetap berdiri**: dua bukti tandingan lama (850→855, 871→872) belum terbantah, dan keempat ketepatan itu terjadi pada berkas yang saya tulis sendiri tanpa parametrisasi — itu menghitung, bukan meramal. Dua di antaranya bahkan terjadi pada run yang **gagal**: benar dan tak berharga.

---

## 8. Aturan kerja dengan pengguna

- Bila pengguna menulis **"lanjut"** atau **"lanjutkan"**, teruskan **tanpa meminta konfirmasi**.
- Pisahkan **fakta terverifikasi** (punya commit / run ID / kutipan) dari **asumsi**; bila belum terverifikasi, katakan **"Ini memerlukan verifikasi."**
- Katakan bila pengguna salah. Katakan bila **kamu sendiri** salah — termasuk bila **koreksimu sendiri** ternyata salah; itu sudah terjadi (jurnal 37).
- Jangan menghaluskan ramalan yang meleset.
- Perbarui `STATE.md` tiap posisi berubah; tambah satu entri `journal/` tiap sesi, **ditulis sebelum hasil run terlihat** bila membahas ramalan; segarkan berkas ini sebelum konteks penuh.

---

## 9. Rantai commit terakhir

`08e21b3f` (ADR-037) → `bfc5bef7` (**STATE v31**) → `2f9c577e` (PROMPT v3) → `ac260865` (jurnal 38) → `499c64c7` (**`saringan_funding.py`** + uji) → `bad6fdc3` (laporan merah) → `a04478a7` (perbaikan boneka) → `1bf29f21` (**907 uji**) → `4e6a6584` (**`run_h015.py`** + uji) → `0fbd4edb` (laporan merah, 937) → `bccaa55f` (perbaikan fixture) → `8bb57075` (**942 uji, hijau**) → **`2e191e5f` (jurnal 39)**.

**Posisi: 14 hipotesis dinilai, 14 DITOLAK, 1 berkode lengkap dan hijau tetapi belum dijalankan. 58 aturan. 19 kelas cacat. 942 uji.**
