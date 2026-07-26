# ADR-012 - Dinding grid imbalan adalah dinding yang dipilih, bukan dinding yang ditemukan

**Status:** diterima, mendahului kode H-010
**Tanggal:** 2026-07-26
**Konteks commit:** ditulis di atas `ebfbfcb7` (STATE versi 16, sebelas gerbang, 494 pengujian hijau)
**Revisi:** angka pada bagian 1 dikoreksi; lihat bagian 8.

---

## 1. Pengamatan yang memicu keputusan ini

`reports/backtest_h009_carry_dipatok.json`, blok `parameter_terpilih`, run `30186730437`. Dua belas baris kombinasi dijumlahkan per imbalan:

| Imbalan terpilih | Jendela | Porsi dari 356 |
|---|---|---|
| **4,0** | 82 + 64 + 48 = **194** | **54,5%** |
| 3,0 | 42 + 32 + 27 = 101 | 28,4% |
| 2,0 | 14 + 12 + 12 = 38 | 10,7% |
| 1,0 | 11 + 7 + 5 = 23 | 6,5% |
| **jumlah** | **356** | **100%** |

`IMBALAN = [1.0, 2.0, 3.0, 4.0]` di `lux/backtest/run_h009.py`, diimpor dari `run_h007`. Nilai 4,0 adalah **batas atas grid**, dan lebih dari separuh jendela memilihnya. Pola yang sama ada di H-007, tempat grid itu pertama dipakai, dan di H-008.

Saya mencatat pola itu tiga kali sebagai "83% jendela memilih 3R atau 4R" dan memperlakukannya sebagai bukti bahwa menurunkan titik impas berhasil. Itu benar, tetapi ada tafsiran kedua yang tidak pernah saya periksa: **optimum mungkin berada di luar grid, dan yang saya ukur hanya batas grid.** Selama batasnya tidak digeser, kedua tafsiran itu tidak dapat dibedakan.

Ini **cacat rancangan H-007**, bukan hipotesis baru. Pemilih yang menempel di dinding adalah gejala klasik grid terpotong, dan gejala itu terlihat sejak laporan H-007 dikomit.

## 2. Keputusan

H-010 mengubah **tepat satu hal** terhadap H-009: batas atas grid imbalan digeser ke luar.

| | H-009 | **H-010** |
|---|---|---|
| `IMBALAN` | `[1.0, 2.0, 3.0, 4.0]` | **`[2.0, 4.0, 6.0, 8.0]`** |
| `LOOKBACK` | `[20, 55, 100]` | `[20, 55, 100]` tidak berubah |
| Jumlah kombinasi | 12 | **12, sengaja identik** |
| `maks_carry_realisasi_R` | dipatok 0,25 | dipatok 0,25, tidak dilombakan (ADR-009) |
| Sinyal, biaya, universe, jendela | - | tidak berubah |

Alasan bentuk grid ini:

- **2,0 dan 4,0 dipertahankan sebagai jangkar.** Bila keduanya hilang, hasil H-010 tidak dapat dibandingkan langsung dengan H-009.
- **1,0 dan 3,0 dibuang, bukan ditambahkan.** Menambah nilai berarti 18 kombinasi dan multiplisitas berbeda dari H-009; multiplisitas identik lebih berharga daripada mempertahankan nilai yang hampir tidak pernah dipilih (1,0 hanya 6,5% jendela). Ini pilihan yang bisa saya salahkan nanti, jadi alasannya ditulis sekarang.
- **Satuan R tidak berubah** karena jarak stop tetap ATR x 2,0. Ekspektasi R H-009 dan H-010 sebanding apa adanya.

**Batasan implementasi yang ditemukan saat membaca kode, bukan saat menulis ADR ini:** `run_h009.py` mengimpor grid dari `run_h007` dan memasang penjaga yang menolak berjalan bila keduanya berbeda. Karena itu H-010 **wajib** mendefinisikan gridnya sendiri dan `run_h007.IMBALAN` **haram** disentuh - mengubahnya akan membatalkan penjaga H-009 dan mengubah arti laporan yang sudah dikomit. Sebagai gantinya, H-010 mengimpor `buat_konfig`, `DATASET`, `KUNCI_TERLARANG`, dan `AMBANG_CARRY_KERAS` dari `run_h009` apa adanya, sehingga pematokan pengaman carry dijalankan oleh kode yang sama persis, bukan oleh salinan yang bisa melenceng.

## 3. Aritmetika titik impas, dihitung sebelum run

`titik_impas(imbalan) = 1/(1+imbalan)`, dikunci `tests/test_titik_impas.py`:

| Imbalan | Titik impas kotor |
|---|---|
| 2,0 | 0,3333 |
| 4,0 | 0,2000 |
| 6,0 | 0,1429 |
| 8,0 | 0,1111 |

H-009 mencatat 4.111 target dari 14.925 perdagangan, yaitu **0,27544** - margin 0,0754 di atas titik impas 4R. Pertanyaan H-010 murni aritmetika: **apakah laju kena target turun lebih lambat daripada titik impasnya?** Bila laju turun ke 0,15 pada 8R, titik impas 0,1111 masih terlampaui dan ekspektasi naik. Bila turun ke 0,10, ia gagal.

Saya tidak tahu jawabannya, dan itu sebabnya percobaan ini informatif ke dua arah.

## 4. Bahaya yang sudah terlihat sebelum run

Target lebih jauh butuh waktu lebih lama. Tiga akibat yang saling berkait, ketiganya kini punya gerbang:

1. **Perdagangan tak selesai membengkak.** `maks_umur_bar = 168` tidak berubah. H-009 mencatat `umur` 368 dan `akhir_data` 188, yaitu 3,7% perdagangan berakhir tanpa keputusan stop atau target. Pada 8R porsi itu **harus** naik. `ALASAN_TIDAK_SELESAI = ("umur", "akhir_data", "carry")` sudah terdefinisi di `lux/analisis/titik_impas.py`, jadi porsinya wajib dicetak dan dibaca **sebelum** ekspektasi ditafsirkan. Bila mayoritas perdagangan berakhir karena batas umur, yang diukur bukan lagi struktur keluar melainkan batas umur.
2. **Carry membesar.** Pegangan lebih lama berarti penagihan funding lebih banyak. Inilah hipotesis pertama tempat **gerbang kesebelas mengikat**, dan ia mengikat pada arah yang benar-benar berisiko dilanggar.
3. **Pengaman carry lebih sering menyala.** Di H-009 ia menyala 16 kali (0,107%). Bila melonjak, sebagian keuntungan target jauh dipotong sebelum sampai - dan itu **fitur, bukan bug**: ADR-009 memilih menjaga ekor daripada mengejar ekspektasi.

**Dilarang bila hasilnya buruk:** melonggarkan `maks_umur_bar`, mematikan pengaman carry, atau melonggarkan ambang ADR-011 agar H-010 lulus. Ketiganya mengubah percobaan ini menjadi pencarian konfigurasi yang lulus.

## 5. Ramalan, ditulis sebelum run

Ditulis sekarang supaya bisa salah dengan jujur.

1. **Jendela akan menempel lagi di dinding baru.** Imbalan 8,0 dipilih **30-55%** jendela: lebih rendah daripada 54,5% milik 4,0, tetapi tetap porsi terbesar. Bila 8,0 dipilih **lebih dari 54,5%**, itu bukti kuat bahwa penempelan bersifat **mekanis**, bukan informatif - pemilih menyukai target yang jarang tercapai karena perdagangan tak selesai tidak dihukum setara dengan kerugian. Bila 8,0 dipilih **kurang dari 25%**, dinding H-007 memang bukan dinding dan tafsiran lama saya benar.
2. **Laju kena target turun ke 0,13-0,20**, dan porsi perdagangan tak selesai naik dari 3,7% ke **lebih dari 12%**.
3. **`porsi_funding_ekor_maks` naik di atas 0,165 milik H-009, ke kisaran 0,20-0,35.** Bila melewati 0,35, gerbang kesebelas **GAGAL dan H-010 ditolak karena itu** - dan itu justru pembuktian bahwa gerbang kesebelas layak dibangun.
4. **Ekspektasi tidak akan mencapai 0,05R.** Taksiran **0,030-0,048R**, jadi H-010 kemungkinan besar menjadi penolakan kesepuluh. Ditulis terang-terangan supaya tidak ada ruang menafsirkan hasil datar sebagai kemajuan.

**Ramalan mana pun yang salah dicatat sebagai salah di jurnal, bukan diperhalus.**

## 6. Kriteria putusan

Tidak berubah: ekspektasi luar sampel **> 0,05R**, minimum 100 perdagangan, `entri_acak` p **< 0,05** (hipotesis tunggal, jadi tanpa koreksi Bonferroni - berbeda dari keluarga ADR-006 yang memakai 0,0167), dan **sebelas gerbang lulus**. Gerbang yang tidak dapat dinilai berarti gagal.

H-010 adalah hipotesis pertama yang ambang ADR-010 dan ADR-011 mengikat penuh, sesuai janji tertulis di kedua ADR.

## 7. Utang yang diakui

- `lux/funding.py::gerbang_lulus` masih terlalu longgar (utang ADR-011).
- Grid `LOOKBACK` belum pernah diuji terhadap dindingnya sendiri. Nilai 100 adalah batas atas dan H-009 mencatatnya dipilih 82 + 32 + 12 + 7 = **133 dari 356 jendela** (37,4%) - penempelan jauh lebih lemah daripada imbalan, tetapi ada. Bila H-010 menunjukkan penempelan imbalan bersifat mekanis, dinding `LOOKBACK` wajib diperiksa dengan cara yang sama. Dicatat sebagai utang, bukan dikerjakan sekarang.

## 8. Koreksi terhadap versi pertama ADR ini

Versi pertama, dikomit `de9ac0e7`, menyatakan imbalan 4,0 dipilih **226 jendela (63,5%)** dan menambahkan catatan bahwa jumlah baris "melewati 356 karena tabel memecah per kombinasi". **Keduanya salah.** Penjumlahan yang benar 82 + 64 + 48 = 194 (54,5%), dan keempat imbalan berjumlah tepat 356 sehingga tidak ada pemecahan ganda yang perlu dijelaskan.

Kesalahan ini kelas yang sama dengan "26 simbol positif" dan "16 pengujian": angka ditulis dari ingatan tanpa dijumlahkan ulang, lalu dipakai sebagai dasar. Yang menangkapnya adalah pembacaan `parameter_terpilih` saat menyiapkan kode, bukan kewaspadaan.

Arah kesimpulan tidak berubah - 54,5% tetap porsi terbesar dan tetap berada di dinding grid - tetapi ambang ramalan 1 digeser dari 63,5% ke 54,5%. Ambang ramalan yang berubah setelah angkanya diperbaiki tetap sah karena perbaikan terjadi **sebelum** run, dan versi pertama tetap tersimpan di riwayat git untuk diperiksa.
