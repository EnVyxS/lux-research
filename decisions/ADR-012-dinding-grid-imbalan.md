# ADR-012 — Dinding grid imbalan adalah dinding yang dipilih, bukan dinding yang ditemukan

**Status:** diterima, mendahului kode H-010
**Tanggal:** 2026-07-26
**Konteks commit:** ditulis di atas `ebfbfcb7` (STATE versi 16, sebelas gerbang, 494 pengujian hijau)

---

## 1. Pengamatan yang memicu keputusan ini

`reports/backtest_h009_carry_dipatok.json`, blok `parameter_terpilih`, run `30186730437`:

| Imbalan terpilih | Jumlah jendela | Porsi |
|---|---|---|
| **4,0** | **226** | **63,5%** |
| 3,0 | 101 | 28,4% |
| 2,0 | 38 | 10,7% |
| 1,0 | 23 | 6,5% |

(Jumlah melewati 356 karena tabel di laporan memecah per kombinasi imbalan×lookback; agregat per imbalan dihitung dari dua belas baris yang sama.)

`IMBALAN = [1.0, 2.0, 3.0, 4.0]` di `lux/backtest/run_h009.py`. Nilai 4,0 adalah **batas atas grid**, dan hampir dua pertiga jendela memilihnya. Pola yang sama sudah ada di H-007, tempat grid itu pertama dipakai, dan di H-008.

Saya mencatat pola itu tiga kali sebagai "83% jendela memilih 3R atau 4R" dan memperlakukannya sebagai bukti bahwa menurunkan titik impas berhasil. Itu benar, tetapi ada tafsiran kedua yang tidak pernah saya periksa: **optimum mungkin berada di luar grid, dan yang saya ukur hanya batas grid.** Selama batasnya tidak digeser, kedua tafsiran itu tidak dapat dibedakan.

Ini **cacat rancangan H-007**, bukan hipotesis baru. Saya menyatakannya sebagai cacat karena memang begitu: pemilih yang menempel di dinding adalah gejala klasik grid yang terpotong, dan gejala itu terlihat sejak laporan H-007 dikomit.

## 2. Keputusan

H-010 mengubah **tepat satu hal** terhadap H-009: batas atas grid imbalan digeser.

| | H-009 | **H-010** |
|---|---|---|
| `IMBALAN` | `[1.0, 2.0, 3.0, 4.0]` | **`[2.0, 4.0, 6.0, 8.0]`** |
| `LOOKBACK` | `[20, 55, 100]` | `[20, 55, 100]` tidak berubah |
| Jumlah kombinasi | 12 | **12, sengaja identik** |
| `maks_carry_realisasi_R` | dipatok 0,25 | dipatok 0,25, tidak dilombakan (ADR-009) |
| Sinyal, biaya, universe, jendela | — | tidak berubah |

Alasan bentuk grid ini:

- **2,0 dan 4,0 dipertahankan sebagai jangkar.** Bila keduanya hilang, hasil H-010 tidak dapat dibandingkan dengan H-009 secara langsung.
- **1,0 dan 3,0 dibuang, bukan ditambahkan ke grid.** Menambah nilai berarti 18 kombinasi dan multiplisitas yang berbeda dari H-009; membuat multiplisitas identik lebih berharga daripada mempertahankan dua nilai yang hampir tidak pernah dipilih (1,0 hanya 6,5% jendela). Ini pilihan yang bisa saya salahkan nanti, jadi saya tulis alasannya sekarang.
- **Satuan R tidak berubah** karena jarak stop tetap ATR×2,0. Ekspektasi R H-009 dan H-010 sebanding apa adanya.

## 3. Aritmetika titik impas — dihitung sebelum run

`titik_impas(imbalan) = 1/(1+imbalan)`, dikunci `tests/test_titik_impas.py`:

| Imbalan | Titik impas kotor | Laju kena target H-009 |
|---|---|---|
| 2,0 | 0,3333 | — |
| 4,0 | 0,2000 | **0,27544 tercatat** |
| 6,0 | 0,1429 | ? |
| 8,0 | 0,1111 | ? |

H-009 mencatat 4.111 target dari 14.925 perdagangan, yaitu **0,27544** — margin 0,0754 di atas titik impas 4R. Pertanyaan H-010 adalah pertanyaan aritmetika murni: **apakah laju kena target turun lebih lambat daripada titik impasnya?** Bila laju turun ke 0,15 di 8R, titik impas 0,1111 masih terlampaui dan ekspektasi naik. Bila turun ke 0,10, ia gagal.

Saya tidak tahu jawabannya, dan itu sebabnya percobaan ini informatif ke dua arah.

## 4. Bahaya yang sudah terlihat sebelum run, dan cara menanganinya

Target yang lebih jauh butuh waktu lebih lama. Itu punya tiga akibat yang saling berkait, dan ketiganya kini punya gerbang:

1. **Perdagangan tak selesai membengkak.** `maks_umur_bar = 168` tidak berubah. H-009 sudah mencatat `umur` 368 dan `akhir_data` 188, yaitu 3,7% perdagangan berakhir tanpa keputusan stop atau target. Pada 8R porsi itu **harus** naik. `ALASAN_TIDAK_SELESAI = ("umur", "akhir_data", "carry")` sudah terdefinisi di `lux/analisis/titik_impas.py`, jadi porsinya wajib dilaporkan dan dibaca **sebelum** ekspektasi ditafsirkan. Bila mayoritas perdagangan berakhir karena batas umur, yang diukur bukan lagi struktur keluar melainkan batas umur.
2. **Carry membesar.** Pegangan lebih lama berarti penagihan funding lebih banyak. Inilah hipotesis pertama tempat **gerbang kesebelas mengikat**, dan ia mengikat pada arah yang benar-benar berisiko dilanggar.
3. **Pengaman carry akan lebih sering menyala.** Di H-009 ia menyala 16 kali (0,107%). Bila di H-010 penyalaan melonjak, sebagian keuntungan target jauh akan dipotong sebelum sampai — dan itu **fitur, bukan bug**: ADR-009 memilih menjaga ekor daripada mengejar ekspektasi.

**Yang dilarang bila hasilnya buruk:** melonggarkan `maks_umur_bar`, mematikan pengaman carry, atau melonggarkan ambang ADR-011 agar H-010 lulus. Ketiganya akan mengubah percobaan ini menjadi pencarian konfigurasi yang lulus, bukan uji terhadap mekanisme.

## 5. Ramalan, ditulis sebelum run

Ditulis sekarang supaya bisa salah dengan jujur. Dua dari tiga ramalan H-009 salah, dan dari kesalahan itu lahir aturan 13.

1. **Jendela akan menempel lagi di dinding baru.** Saya meramalkan imbalan 8,0 dipilih oleh **35–60%** jendela — lebih rendah daripada 63,5% milik 4,0, tetapi tetap porsi terbesar. Bila 8,0 dipilih **lebih dari 63,5%**, itu bukti kuat bahwa penempelan di dinding bersifat **mekanis**, bukan informatif: pemilih menyukai target yang jarang tercapai karena perdagangan yang tidak selesai tidak dihukum setara dengan kerugian. Bila 8,0 dipilih **kurang dari 25%**, dinding H-007 memang bukan dinding dan tafsiran lama saya benar.
2. **Laju kena target turun ke 0,13–0,20**, dan porsi perdagangan tak selesai naik dari 3,7% ke **lebih dari 12%**.
3. **`porsi_funding_ekor_maks` naik di atas nilai H-009 0,165, ke kisaran 0,20–0,35.** Bila ia melewati 0,35, gerbang kesebelas **GAGAL dan H-010 ditolak karena itu** — dan itu justru pembuktian bahwa gerbang kesebelas layak dibangun.
4. **Ekspektasi akhir tidak akan mencapai 0,05R.** Taksiran saya **0,030–0,048R**, jadi H-010 kemungkinan besar menjadi penolakan kesepuluh. Saya menulis ini terang-terangan supaya tidak ada ruang menafsirkan hasil datar sebagai kemajuan.

**Ramalan mana pun yang salah dicatat sebagai salah di jurnal, bukan diperhalus.**

## 6. Kriteria putusan

Tidak berubah dan tidak boleh berubah: ekspektasi luar sampel **> 0,05R**, minimum 100 perdagangan, `entri_acak` p **< 0,05** (hipotesis tunggal, jadi tanpa koreksi Bonferroni — berbeda dari keluarga ADR-006 yang memakai 0,0167), dan **sebelas gerbang lulus**. Gerbang yang tidak dapat dinilai berarti gagal.

H-010 adalah hipotesis pertama yang ambang ADR-010 dan ADR-011 mengikat penuh, sesuai janji tertulis di kedua ADR bahwa ambang yang ditulis setelah sebagian data terlihat hanya berlaku ke depan.

## 7. Utang yang diakui

- `lux/funding.py::gerbang_lulus` masih terlalu longgar (utang dari ADR-011). Tidak dikerjakan bersamaan agar satu perubahan menguji satu hal.
- Grid `LOOKBACK` belum pernah diuji terhadap dindingnya sendiri. Nilai 100 adalah batas atas dan H-009 mencatatnya dipilih 133 dari 356 jendela — penempelan yang jauh lebih lemah daripada imbalan, tetapi ada. Bila H-010 menunjukkan penempelan imbalan bersifat mekanis, dinding `LOOKBACK` wajib diperiksa dengan cara yang sama. Dicatat sebagai utang, bukan dikerjakan sekarang.
