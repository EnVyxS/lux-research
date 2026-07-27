# STATE — LAMPIRAN ARSIP

> Pendamping wajib `STATE.md`. Berkas ini memuat arsip rinci yang tidak berubah tiap sesi: inventaris modul, papan ramalan, angka hipotesis lama, audit workflow, batas alat, peta repo, dan rantai commit. **Dipisahkan pada v28** sesudah muatan `STATE.md` v28 pertama terpotong saat didorong (commit `56633f80`, pelanggaran aturan 35). Tidak ada angka yang dibuang saat pemisahan.

**Diperbarui:** 2026-07-27 (S22).

---

## 1. Papan ramalan jumlah pengujian

| Commit | Ramalan | Nyata | Putusan |
|---|---|---|---|
| `864da2ec` | 635 | **638** | SALAH |
| `3880408f` · `b4b1963c` | 642 · 643 | sama | TEPAT |
| `eae7eb3a` | 662 | **665** | SALAH |
| `955b419a` | 673 | 673 | TEPAT |
| `fb710521` | 673 tetap | — | TIDAK DAPAT DIADILI |
| `02933b85` · `fe7fd30e` | 679 · 683 | sama | TEPAT |
| `6aacef40` | **693** | **694** | SALAH |
| `47ef9a90` … `409343f3` | 702 … 714 | sama | TEPAT |
| ADR-020 langkah 1–3 | 716 · 721 · 734 | sama | TEPAT |
| `8bda1473` · `ab3e9792` | 737 · 739 | sama | TEPAT |
| `48cf1b9f` · `fb128c93` · `43cd4eed` | 749 · 758 · 761 | sama | TEPAT |
| `b0e79220` | 767 | 767 | TEPAT |
| `05df8b78` · `4f09c8d5` · `0859e8dd` | 779 · 795 · 811 | sama | TEPAT |
| `6ae83062` (R-E1b) | 811 | 811 (run `30219837959`) | TEPAT |
| `5bd73fbf` (R-E1a) | 819 | 819 (run `30219885271`) | TEPAT |
| **`4af21176` (R-H1)** | **850** | **855 passed in 3,06s** (run `30221837845`) | **MELESET** |

Jejak: 444 → … → 811 → 819 → **855**. Deret 21 ramalan tepat berturut-turut **putus** pada `4af21176` (rencana 17+14 lawan berkas 20+16; aturan 54). Blob `reports/tests.md`: `d768d55f` (811) → `0e480f90` (819) → **`94e5096e2f989edc13d3f1a95daa84b6b512331e`** (855). Berkas markdown tidak memicu `tests.yml`. Run `30221967019` mengulang **`855 passed in 2.98s`** di sisi runner sebelum unduhan.

**Papan ramalan perilaku sistem:** S18 nol dari enam; S19 empat dari enam; S20 tiga dari lima; **S21–S22:** R-H1 MELESET · R-G1 SEPARUH · R-G2a TEPAT · R-G2b TEPAT · R-G3 TEPAT · R-G4 MELESET JAUH · R-H2 TEPAT · R-H3 TEPAT tetapi tidak berguna · R-B1 separuh pertama TEPAT. Gabungan sebelas ramalan angka H-013: sembilan meleset.

### Adjudikasi ramalan S22 (ADR-035 §6)

| Kode | Isi | Nyata | Putusan |
|---|---|---|---|
| R-G1 | SS′ − SH′ < +0,029481R; taksiran 0,010–0,025R | agregat **+0,027654R** | **SEPARUH** (arah tepat, taksiran meleset ke atas) |
| R-G2a | p bulanan > 0,05 → DITOLAK; taksiran 0,15–0,60 | **0,375962** | **TEPAT** |
| R-G2b | bootstrap 95% memuat nol | **[−0,090679, +0,029104]R** | **TEPAT** |
| R-G3 | trade SS′ melampaui SH′ ≥ 20% | **+33,2%** | **TEPAT** |
| R-G4 | > 80% trade SH′ keluar lewat `umur` | **32,4%** (14.426/44.538); `stop` **62,9%** | **MELESET JAUH** |
| R-H2 | pagar pra-terbang lulus percobaan pertama | delapan butir OK | **TEPAT** |
| R-H3 | run selesai < 25 menit | **2 menit 19 detik** | **TEPAT tetapi TIDAK BERGUNA** (aturan 36) |
| R-B1 separuh 1 | run 4h pertama melapor `checksum` "tidak dapat dinilai: manifest baru ditulis pada run ini" | kalimat itu persis | **TEPAT** |
| R-B1 separuh 2 | run 4h kedua lulus `checksum` | — | **MUSTAHIL sampai cacat 17 ditutup** |

R-G4 salah pada **mekanismenya**: menghapus target tidak membuat posisi "dipegang sampai waktu habis", ia membuatnya "dipegang sampai stop kena, dan stop biasanya kena lebih dulu". Itu menjelaskan std yang melebar (2,20818R lawan 1,37827R) dan retensi drop-1 yang jatuh (0,9047 lawan 0,9872).

### Ramalan beku yang masih belum teradili

| Kode | Isi | Sumber |
|---|---|---|
| R-B1 separuh kedua | run 4h **kedua** lulus `checksum` | ADR-027 §7 — mustahil sampai cacat 17 ditutup |
| R-B4 | pemasangan bulanan **berbobot trade** tetap p > 0,05 | ADR-027 §7 |
| ADR-016 ramalan 5 | ekspektasi R dengan `stop_hormati_celah` menyala lebih rendah | ADR-016 |

**DIBATALKAN, tidak akan pernah punya angka:** R-F1…R-F5 (ADR-032).

---

## 2. H-013 — angka run sel (`30214203863`)

Mesin commit `93a4309b`, laporan `e060749c` pada 2026-07-26T18:21:35Z. 438 simbol dimuat, **437 layak** sesudah lantai membuang **USDCUSDT** (median `stop_frac` 3,799992e−04), 4.082 jendela per sel.

| Sel | Sinyal | Target | Umur (bar 4h) | Trade | Ekspektasi R | p entri acak | Gerbang gagal |
|---|---|---|---|---|---|---|---|
| SS | sungguhan | ya | **42** | 60.018 | **+0,066648** | 0,0166 | `invarian_risiko`, `checksum` |
| SH | sungguhan | tidak | **48** | 44.614 | +0,037167 | 0,2259 | `entri_acak`, `invarian_risiko`, `checksum`, `funding_ekor` |
| AS | permutasi seed 42 | ya | **42** | 55.927 | +0,011806 | 0,3588 | `entri_acak`, `lookahead`, `invarian_risiko`, `checksum`, `konsentrasi` |
| AH | permutasi | tidak | **48** | 45.378 | +0,058170 | 0,1993 | `entri_acak`, `lookahead`, `invarian_risiko`, `checksum`, `funding_ekor` |

Sidik: SS `06c3805bdd7ad4de` · SH `af1145aab7f13567` · AS `5ee4b130f9ed228d` · AH `4ada4587abede644`.

Tiga selisih: sinyal (SS − AS) **+0,054842R** terhadap seed 42 / **+0,043732R** terhadap rerata nol · "geometri" (SS − SH) **+0,029481R — MENCAMPUR DUA MEDAN** · interaksi +0,075846R · SH − AH **−0,021004R**.

`parameter_beku`: `imbalan_R` 2,0 · `h_bar` 48 · `umur_sel_stop` 42 · `lookback` [20,55,100] · `seed_permutasi` 42 · `ulangan` 300 · `min_median_stop_frac` 0,004 · `maks_biaya_masuk_R` 0,5 · `stop_hormati_celah` true · `jendela_bar` {1080,540,42} · `pemanasan` 200 · `bar_dibutuhkan` 1862.

Pemilihan lookback per sel — H-013: SS 20→1682, 55→846, 100→1554 · SH 20→1987, 55→1069, 100→1026 · AS 20→1408, 55→1089, 100→1585 · AH 20→1392, 55→1073, 100→1617. **H-014:** SS′ 20→1711, 55→836, 100→1535 · SH′ 20→1995, 55→1073, 100→1014.

**Medan `lulus` di `backtest_h013_kontribusi.json` TIDAK SAH.** Putusan H-013 yang sah hanya dari `reports/h013b_p.json`.

---

## 3. H-012 — DITOLAK (ADR-014 §8)

Run `30200123505`, commit `56a325d2`, sidik `75f9c7ccd65ec30f`, 437 dari 438 simbol, 4.081 jendela.

| Sisi batas | Bulan | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|
| **Tahan (sejak `2026-01`)** | 7 | **22.117** | +922,56 | **+0,041713** |
| Sebelum `2026-01` | 66 | 113.564 | +7.168,96 | +0,063127 |
| Seluruh riwayat | 73 | 135.681 | +8.091,52 | +0,059636 |

**0,041713R < 0,05R → GAGAL.** `entri_acak` GAGAL p 0,06312292358803986 · `invarian_risiko` GAGAL −21,3131R · `funding_ekor` GAGAL 0,6601. Entri ditolak pengaman **62**.

**Titik impas** `1/(1+imbalan)`: 1R 0,5000 · 2R 0,3333 · 4R 0,2000 · 6R 0,1429 · 8R 0,1111. Di H-009, **194 dari 356 jendela (54,5%)** memilih imbalan 4,0 — versi 16 menulis 226 dan 63,5%; **itu salah**. Seretan: H-002 0,04926 · H-009 0,034614 · H-010 0,036220 · H-012 **0,035900**.

---

## 4. Mesin backtest dan inventaris modul

**`engine.Konfig`** (blob `81c1db8a`): `fee` 0,0005 · `slippage` 0,0005 · `atr_periode` 14 · `atr_pengali_stop` 2,0 · `risiko_per_trade` 0,005 · `imbalan_R` 2,0 · `modal_awal` 10.000 · `izinkan_short` True · `maks_umur_bar` 0 · `maks_carry_R` 0,0 · `jendela_carry_hari` 30 · `maks_carry_realisasi_R` 0,0 · `maks_biaya_masuk_R` 0,0 · **`stop_hormati_celah` False** · `pakai_target` True. `__post_init__` **menolak** `not pakai_target and maks_umur_bar <= 0`. `Perdagangan.R = laba / (jarak_stop * ukuran)`; `jarak = k.atr_pengali_stop * atr_t` **di kedua jenis sel**; `target = masuk + s*jarak*k.imbalan_R` bila bertarget, `nan` bila tidak. Alasan keluar: `umur`, `carry`, `stop`, `target`, `akhir_data`. **`_boleh_masuk` memakai `umur_ms = k.maks_umur_bar * interval_ms`** — sebab cacat 14. Urutan per bar: umur → carry realisasi → stop/target → entri → ekuitas.

**Sebelas gerbang:** `forward_fill`, `buy_and_hold`, `entri_acak`, `lookahead`, `invarian_risiko`, `funding`, `overlap`, `checksum`, `survivorship`, `konsentrasi`, `funding_ekor`. **Tidak dapat dinilai = GAGAL.**

**`runner.Opsi`** (blob `4ce34a3c`, pembanding `fc79e070`): `dir_aset`, `out=reports`, `interval="1h"`, `universe`, `akhir_sejati`, `limit=40`, `panjang_latih=4320`, `panjang_uji=2160`, `embargo=168`, `pemanasan=200`, `ulangan=100`, `sampel_permutasi=10`, `min_median_stop_frac=0.0`. `Spek(h, sinyal, kandidat, nama, params_lookahead, buat_konfig)`. `muat_konteks` memakai `jalur_manifest(opsi.interval, opsi.out)`; `sampel = set(sorted(bingkai)[:opsi.sampel_permutasi])`; bila manifest belum ada ia **menulisnya** lalu memancarkan gerbang `checksum` "tidak dapat dinilai" (dasar cacat 17).

**`jalankan_spek` mengembalikan** `id, nama, sidik, ekspektasi_R, total_R, trade, jendela_positif, jumlah_jendela, p_entri_acak, gerbang_gagal, lulus, alasan, alasan_keluar, entri_ditolak_biaya, simbol_dibuang_lantai, bulan_dengan_trade (CACAH saja), rerata_transaksi_R, retensi_drop_1, porsi_funding_ekor_maks, std_R, galat_baku_R, jarak_galat_baku, detik`; menulis `out/backtest_{spek.nama}.{json,md}` dengan **nama sama setiap panggilan**; mendaftarkan `hipotesis/{spek.h.id}.json`; blok `agregat_periode` per bulan kalender UTC sudah ditulisnya. **Terverifikasi S22:** md-nya mencetak `**LULUS**` bila `putusan.lulus and laporan.semua_lulus` — perangkap yang membuat berkas md sel mencetak putusan yang bukan putusan hipotesisnya.

**`walk_forward.jalankan_walk_forward`** (blob `5a686e229c0292bdea2219278a318b96fa675637`, dibaca utuh S22): `konfig_untuk(params) = buat_konfig(params, k) if buat_konfig is not None else k`, dipakai **di dalam lingkaran pemilihan kandidat** dan untuk jendela uji; `HasilJendela.konfig` menyimpan konfig yang benar-benar dipakai; `_skor_baku` memberi `-inf` bila trade latih < `min_trade_latih` (bawaan 10); jendela tanpa kandidat layak **dilewati**; sinyal bar pemanasan **dipaksa nol**; `entri_ditolak_biaya` dijumlahkan **hanya dari jendela uji**. Docstring menjanjikan `buat_konfig=None` ≡ perilaku sebelum ADR-007.

**Modul H-013** (`run_h013.py`, blob `239b88d0`, pembanding `418f6084`): `NAMA_SEL` · `NAMA_LAPORAN` · `dasar_riset` · `jendela_bar` · `bar_dibutuhkan` · `kandidat` · `pakai_target_sel` · **`umur_sel` (42 lawan 48 — cacat 14)** · `permutasi_sinyal` · `sinyal_acak` · `sinyal_sel` · **`buat_konfig_sel`** · `hipotesis_h013` · `spek_sel` · `kontribusi` · `prosa_kontribusi`. Beku: `IMBALAN_BEKU` 2,0 · `H_BAR` 48 · `UMUR_SEL_STOP` 42 · `SEED_PERMUTASI` 42 · `AMBANG_KONTRIBUSI_SINYAL` 0,020 · `MIN_ULANGAN` 300 · `MIN_TRADE_SEL` 100 · `PEMANASAN` 200 · `SKOR_ACAK_TERDAHULU` 0,04661 · `LOOKBACK` [20,55,100].

**Modul H-014** (`run_h014.py` + `gabung_h014.py`, `4af21176`): `NAMA_SEL=("SSp","SHp")` · `NAMA_LAPORAN_H014` · `UMUR_SETARA=48` · `AMBANG_BESARAN_R=0.020` · `AMBANG_P=0.05` · `CATATAN_AMBANG` · `PUTUSAN_MUNGKIN` · `pakai_target_h014` · `umur_sel_h014` · **`konfig_sel_h014`** · **`medan_berbeda`** · `sinyal_nyata` · `hipotesis_h014` · `spek_h014` · `opsi_h014` · `jalur_manifes` · `jalur_sel` · **`periksa_nama`**; penggabung: `muat_sel` · `trade_sel` · **`adjudikasi`** (dua putusan saja, membaca `rerata_selisih`) · `tulis_laporan` · `main` (keluar 0/4/2).

**Jalur A** (`berpasangan.py`, blob `a9fba624`): `NAMA="berpasangan"`, `SEED=20260727`, `ULANGAN=10000`, `PEMBATAS`, `pasangkan`, `pasangan_simbol`, `pasangan_bulan`, `uji_tanda` (`p=(1+m)/(1+ulangan)`), `bootstrap` (seed+1), `ringkas` (**selalu** `memenuhi_adr015: False`), `tulis_laporan`, `main`. `_nilai` melempar pada nilai tak finit. **Tidak ada R per jendela di laporan mana pun.**

**Jalur B:** `lux/analisis/sebaran_nol.py` (`05df8b78`, 779) — `p_ekor_atas` (`p=(1+cacah)/(1+n)`), `p_per_perdagangan` (`mengikat: False`), `p_bulanan` (`mengikat: True`); `run_h013b.py` (`4f09c8d5`, 795) — `NAMA_SPEK="h013b_as_seed"`, 30 seed per pecahan; `gabung_h013b.py` (`0859e8dd` → `6ae83062` → `5bd73fbf`, 811 → 819) — `BUNYI_ASLI_R_D3`, aturan 49 di alat.

**`lux/praregistrasi.py`** (blob `98a2806e`): `Kriteria(min_ekspektasi_R=0.05, min_trade_luar_sampel=100, maks_p_entri_acak=0.05, min_jendela_positif_rasio=0.5)` · `Hipotesis(…)` dengan `sidik()` yang **mengecualikan waktu** · **`simpan` menolak id sama dengan isi berbeda** · `nilai(…)` mengumpulkan **seluruh** alasan kegagalan.

---

## 5. Audit lima belas workflow

| Workflow | `git pull --rebase --autostash` | Catatan |
|---|---|---|
| `tests.yml` | ada | filter `lux/**`, `tests/**`, dirinya sendiri |
| `funding.yml` · `funding_check.yml` | ada | masih memakai `reports/universe_layak.json` (447 pra-lantai) |
| `universe.yml` | ada | gerbang ditegakkan **sesudah** commit, disengaja |
| `doctor.yml` | ada | `set +e` disengaja |
| `backfill_daily.yml` | ada | **satu-satunya berjadwal**: `cron: '0 2 * * 1'`, `--clobber` |
| `notion_asap.yml` | **TIDAK ADA** | `git push` polos; `git commit … \|\| echo` menelan kegagalan |
| `h013b.yml` | ada, di dalam lingkaran ulang | sepuluh penulis satu cabang; satu-satunya matriks |
| **`h014.yml`** | ada, lingkaran ulang delapan kali | satu pekerjaan; kedua laporan sel dikomit; **daftar `git add` cacat — cacat 17** |

Ditambah `validate.yml`, `potong_ekor.yml`, `backtest.yml`, `ingest_tier_b.yml`, `geometri.yml`, `berpasangan.yml` — **empat belas dari lima belas** memakai pola `git pull --rebase --autostash`.

**Temuan yang tidak dicari:** `backfill_daily.yml` berjalan tiap Senin 02:00 UTC tanpa dipicu manusia dan mengancam manifest keutuhan (ADR-025 R4).

---

## 6. Kerangka 4h, dataset, kapasitas

**Validasi 4h** run `30211176709` (ADR-017): 3.636.733 baris / 790 simbol; layak 447; celah 112; duplikat 0. **Pemangkasan ekor 4h** run `30211673239` (ADR-018): ambang 6 bar, 447 → **438 layak**, nol penolakan `maks_rasio`. 438 simbol 4h dibandingkan **simbol per simbol** dengan 438 simbol 1h — **identik**. `universe_layak_v2_4h.json`: `"interval":"4h"`, `"min_bar":2190`, `"min_panjang":6`. **Kelayakan 1h lawan 4h identik (447/74/112) BELUM dijelaskan — memerlukan verifikasi.**

**Dataset Tier B putaran 2:** 14.545.679 bar 1h dan 3.636.733 bar 4h, 790 simbol, rasio 3,9996, ~703 MB. 1h: 447 valid → v2 **438** → berlantai **437**. 4h: sama, **437** pada H-013 dan H-014. Funding 1.982.017 baris, 3 celah sejati, 79,1% positif. Rilis **`tier-b-v1`** id `359778114`; aset 4h **12 berkas, 157.628.619 B**.

**Kapasitas runner:** 4 vCPU, 15 GB RAM, **batas 6 jam per job**. H-012 1220,6 s; H-013 empat sel ~sepuluh menit termasuk unduhan; satu pecahan Jalur B mengomit 28–43 menit sesudah pemicu; **H-014 dua sel 4h: 109,5 detik komputasi, 2 menit 19 detik dinding** — jadi **waktu run 1h yang lama didominasi UNDUHAN, bukan komputasi**. python 3.12.13, numpy 2.5.1, pytest 9.1.1, pandas 2.2.3, pyarrow 17.0.0, **tanpa scipy, tanpa requests**. CDN `data.binance.vision` 200; REST `fapi.binance.com` **451 permanen**. Timeout: backtest 330, validate 120, potong_ekor 60, ingest 330, berpasangan 20, h013b 180/30, h014 180.

---

## 7. Batas alat agen dan solusinya

- Daftar alat GitHub **tidak memuat satu pun fungsi Actions**. Log workflow **tidak terbaca**. Karena itu setiap workflow menulis hasil ke `reports/` lalu commit balik.
- `search_code` **nol hasil di repo ini**. `get_file_contents` menuntut SHA 40 karakter penuh, tetapi **menerima `ref: "main"`**, pada direktori memberi **ukuran berkas**, dan menerima **SHA commit apa pun** — cara mengadili laporan yang sudah tertimpa.
- `push_files` **mengganti seluruh isi berkas**; baca dulu, dan baca ulang muatannya sebelum mengirim (aturan 35, 54). Tidak ada mode tambal. Bentuk panggilan benar: `owner`/`repo`/`branch`/`message`/`files` seluruhnya **di dalam** `toolArguments`. **Batas panjang muatan nyata:** muatan `STATE.md` v28 pertama **terpotong** dan tetap terkomit (`56633f80`) — berkas panjang wajib dipecah.
- Filter `paths` per berkas: menyentuh `backtest.yml`, `h013b.yml`, atau `h014.yml` **langsung memulai run**. `tests.yml` memfilter `lux/**` dan `tests/**`, jadi `config/`, `journal/`, `decisions/`, `STATE.md`, dan `STATE_LAMPIRAN.md` **tidak** memicunya.
- **Kabar buruk 23–32 detik; kabar baik 10–45 menit** — kecuali `tests.yml` (~23 detik) dan run 4h yang komputasinya memang pendek. **Baca isinya, bukan kecepatannya.**
- **Kegagalan pagar pra-terbang tidak meninggalkan commit sama sekali.** Diam bukan tanda lulus dan bukan tanda gagal.
- **Commit laporan tanpa berkas hasil = run GAGAL. Blob laporan yang SHA-nya tidak berubah = belum ditulis.** Verifikasi lewat `list_commits`.
- **Dua dorongan berurutan ke `lux/**` melahirkan DUA run `tests.yml`**; laporan run pertama tertimpa tetapi tetap terbaca lewat SHA commit laporan itu.
- **Pekerjaan matriks yang bergantung pada keluaran pekerjaan lain wajib `git fetch` + `git checkout origin/main -- reports`** — pelajaran `h013b.yml`.
- **`backfill_daily.yml` berjadwal mingguan**, jadi tidak setiap perubahan blob berasal dari saya.

---

## 8. Cacat lama dan utang teknis

### Lima cacat buta-interval S17 — semuanya ditutup

| # | Cacat | Ditutup di |
|---|---|---|
| 1 | `validate_run` menulis `universe_layak.json` tanpa interval | `02933b85` |
| 2 | `muat_ambang` membaca `min_bar_1h` untuk interval apa pun | `fe7fd30e` |
| 3 | `MIN_PANJANG`/`MIN_BAR` buta interval di `potong_ekor` | `6aacef40` |
| 4 | keluaran `potong_ekor` 4h menimpa masukan 1h | `6aacef40` + `5296162d` |
| 5 | `muat_ohlcv` memangkas ekor dengan ambang 1h | `409343f3` |

Cacat keenam ADR-020 · ketujuh ADR-023 · kedelapan aturan 39 · kesembilan/kesepuluh ADR-024 · kesebelas ADR-025 · kedua belas ADR-028 · ketiga belas ADR-031 · keempat belas ADR-033 · kelima belas ADR-034 · **keenam belas dan ketujuh belas ADR-035**.

### Cacat kelas kedelapan — angka di config yang tidak pernah dibaca program

Run H-013 pertama (`30213913942`, `135b159c`) mati di pagar butir 3: **`muat_konfig_h002` memetakan delapan kunci saja**; `maks_biaya_masuk_R` dan `stop_hormati_celah` tidak ada di sana meski tertulis di `config/lux.yaml` sebagai `0.5` dan `true`. Perbaikan `ab3e9792` (739) memasangnya di `dasar_riset`; satu uji **mengunci cacatnya sebagai perilaku**. Pagar diperkuat `93a4309b`; pagar `h014.yml` butir 6 mengunci bentuk yang sama.

### Utang teknis — kunci config yang tidak pernah dibaca

1. `universe.maks_rasio_bar_datar: 0.30` — **tidak dibaca gerbang backtest**.
2. `risiko.maks_biaya_masuk_R: 0.5` — tidak dipetakan `muat_konfig_h002`.
3. `risiko.stop_hormati_celah: true` — sama.

Keberatan ADR-018 yang masih berdiri: `MAKS_RASIO_DATAR = 0.10` dipakai untuk kedua interval, jadi gerbang itu **lebih longgar** di 4h.

### Temuan S16 — mesin buta terhadap celah harga pada jalur stop

`invarian_risiko` H-012 gagal pada **−21,3131R**; perdagangan **STGUSDT**, keluar lewat `carry`, pelampauan di luar biaya 20,3131R, `jam` 1,0. Blok stop/target lama memakai `harga = stop if kena_stop else target` — **harga bar tidak pernah dipakai**. Perbaikan `stop_hormati_celah` + `harga_stop_terisi` (`955b419a`), dinyalakan di config (`fb710521`) — dan S18 membuktikan penyalaan lewat config **tidak pernah bekerja** untuk pemuat H-002. Hasil H-001b–H-012 **tidak** dihitung ulang. Klaim "mekanisme stop sendiri sehat" **DITARIK**. Pada H-013 `stop_hormati_celah` menyala dan `invarian_risiko` **tetap gagal pada keempat sel**; pada H-014 pada **kedua** sel; **besarnya belum dibaca di keenam sel**.

### Cacat yang sudah ditutup dan tidak boleh terulang

- Parser 1–3 · metrik celah funding · circular import `run_wf → potong_ekor → diag_datar → run_wf` (`4b77617`).
- **S12:** STATE v11 dan v13 menaikkan kekeliruan menjadi fakta; ditarik v12 dan v14.
- **S13:** "226 dari 356 jendela (63,5%)" padahal **194 (54,5%)**.
- **S15:** empat run gagal berturut. Aturan 31–34.
- **S16:** dua commit cacat; dua ramalan cacah salah. Aturan 35–36.
- **S17:** lima cacat buta-interval; ramalan 693 salah. Aturan 37–38.
- **S18:** cacat kedelapan, kesembilan, kesepuluh. Aturan 39–41.
- **S19:** cacat kesebelas dan kedua belas. Aturan 42–46.
- **S20:** cacat ketiga belas; `6ae83062` mendorong sumber tanpa pagarnya. Aturan 47–51.
- **S21:** cacat keempat belas dan kelima belas; tiga koreksi diri dalam ~30 menit dengan satu akar sebab: **merancang di atas modul yang belum dibaca**; R-H1 meleset. Aturan 52–54.
- **S22:** cacat **keenam belas** dan **ketujuh belas**; kesimpulan salah "2 menit 19 detik berarti run gagal"; R-G4 meleset jauh; R-H3 tepat tetapi tidak berguna; **muatan STATE v28 pertama terpotong dan terkomit (`56633f80`)**. Aturan 55–56.

---

## 9. Peta repo

| Path | Isi |
|---|---|
| `config/lux.yaml` | seluruh parameter yang memengaruhi hasil; satu kunci masih **tidak dibaca gerbang**: `maks_rasio_bar_datar`; `versi` masih 2 |
| `lux/kerangka.py` | modul daun: `bar_per_hari`, `jam_interval`, `bar_dari_hari` |
| `lux/binance_vision.py` · `lux/universe.py` | arsip dan universe point-in-time |
| `lux/ingest.py` · `lux/backfill_daily.py` | ingest Tier B dan penutup celah ekor |
| `lux/validate.py` · `lux/validate_run.py` | integritas OHLCV; `muat_ambang(path, interval)` gagal keras |
| `lux/funding.py` · `lux/funding_check.py` | `gerbang_lulus` masih longgar |
| `lux/funding_model.py` · `lux/costs.py` · `lux/degenerasi.py` | jadwal funding · biaya · ambang 0,004 dan 0,5R |
| `lux/notion_reporter.py` | pelapor baris hasil lewat `urllib.request` |
| `lux/diag_datar.py` · `lux/potong_ekor.py` | keluaran **berinterval** |
| `lux/praregistrasi.py` | hipotesis **sekali tulis** |
| `lux/analisis/{titik_impas,sebaran,periode,geometri_keluar}.py` | aritmetika atas laporan; galat baku **taksiran bawah** |
| `lux/analisis/berpasangan.py` | Jalur A; **tidak pernah memancarkan kelulusan** |
| `lux/analisis/sebaran_nol.py` | Jalur B; `p_bulanan` mengikat |
| `lux/strategi/breakout_atr.py` | sinyal kelanjutan (H-001b, H-002, H-007–H-014) |
| `lux/backtest/engine.py` | mesin eksekusi; lima saringan bawaan MATI; `_boleh_masuk` memakai `maks_umur_bar` |
| `lux/backtest/gerbang.py` · `konsentrasi.py` · `funding_ekor.py` | sebelas gerbang |
| `lux/backtest/manifest.py` | modul daun: `jalur_manifest(interval, out)` |
| `lux/backtest/walk_forward.py` · `run_wf.py` | pemilihan dalam sampel · orkestrator H-001b (**jangan disunting kecuali dengan ADR**) |
| `lux/backtest/run_h002.py` · `run_h003.py` | beku; `muat_konfig_h002` memetakan **delapan** kunci saja |
| `lux/backtest/runner.py` | runner bersama; `jalankan_spek` menulis nama berkas yang sama setiap panggilan |
| `lux/backtest/run_h007.py` | sumber grid bersama, **haram disunting** |
| `lux/backtest/run_h010.py` · `run_h011.py` · `run_h012.py` | grid imbalan · `BATAS_H010 = 40` · `BATAS_VOID = 20` |
| `lux/backtest/run_h013.py` | empat sel H-013; `umur_sel` 42 lawan 48 — cacat 14 |
| `lux/backtest/run_h013b.py` · `gabung_h013b.py` | Jalur B pecahan dan penggabung |
| `lux/backtest/run_h014.py` · `gabung_h014.py` | dua sel satu medan; adjudikasi tanpa cabang `LULUS` |
| `tests/` | **855** pengujian tanpa jaringan |
| `reports/` | keluaran mesin; empat berkas sel H-013 ~432 KB; `h013b_p.json` satu-satunya berkas putusan H-013 yang sah; `manifest_aset.json` **hanya 1h**; **`manifest_aset_4h.json` TIDAK ADA — cacat 17** |
| `hipotesis/` | sekali tulis: `H-001b` … `H-012`, `H-013-SS/SH/AS/AH`, `H-014-SSp/SHp` |
| `decisions/` | ADR-003 … **ADR-035**; berkas ADR-015 ke atas bernama `ADR-0NN.md` polos |
| `journal/` | riwayat per sesi, sampai **`2026-07-27-33.md`** |

**Workflow aktif (15):** `tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`, `backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`, `notion_asap`, `geometri`, `berpasangan`, `h013b`, `h014`.

---

## 10. Rantai commit

**S18–S22 (naik):** `4007e189` → `8bda1473` → `135b159c` → `ab3e9792` → `93a4309b` → `9ca18373` → `e060749c` → `4a00f8e4` (v23) → `341c1486` → `48cf1b9f` (749) → `a4a4a46a` → `5970c136` → `e3309954` → `ae149fe9` → `fb128c93` (758) → `aa59afba` → `43cd4eed` (761) → `e544a952` → `48c83d59` → `43fc6052` (v24) → `b0e79220` (767) → `1566de0c` → `6c639275` → `d3f44f76` → `05df8b78` (779) → `e61be44f` → `4f09c8d5` (795) → `7ee531b3` → `0859e8dd` (811) → `56a27110` → `97b36c19` → `af470704` → `c849486f` → sepuluh commit pecahan → `1d746879` (H-013 DITOLAK) → `dc028faa` → `9a7c741b` (v25) → `6ae83062` → `5bd73fbf` (819) → `781d4a92` → `2ca7ceeb` → `7aa761ec` → `49782044` (v26) → `8feef37b` → `7269af2e` (ADR-032+j28) → `b9dc917d` (ADR-033+j29) → `d8cc4ecc` (ADR-034+j30) → `4af21176` (kode H-014, **855**) → `4795767b` (laporan uji) → `17ef54f7` (jurnal 31, aturan 54) → `52c64ac5` (`h014.yml`, pemicu run `30221967019`) → `603477ce` (laporan H-014) → `a3355294` (STATE v27) → `a25160ca` (ADR-035 + jurnal 32) → `d49aab94` (PROMPT v1) → `e34961f5` (PROMPT v2) → **`56633f80` (STATE v28 TERPOTONG)** → lampiran ini → STATE v28 utuh.

Penamaan ADR: `ADR-0NN.md` telanjang sejak 015. Cacah uji sekarang **855**.
