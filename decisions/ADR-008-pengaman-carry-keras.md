# ADR-008 — Pengaman carry yang keras, dinilai ulang sepanjang posisi

**Status:** diterima
**Tanggal:** 2026-07-26
**Konteks:** setelah H-007 (`reports/backtest_h007_keluar.md`, run `30176317156`)

## Masalah

`invarian_risiko` sudah menjatuhkan **empat dari tujuh** hipotesis: H-001b (−2,5853R), H-003 (−1,8637R), H-005 (−1,9122R), dan H-007 (−1,9769R). Ambangnya −1,5R, yang berarti tidak satu pun perdagangan boleh rugi lebih dari 1,5 kali risiko yang dipertaruhkan.

Stop berjarak 1R. Sebuah perdagangan hanya dapat rugi jauh melampaui 1R kalau ada biaya yang menumpuk di luar kendali stop. Biaya itu adalah funding.

ADR-004 sudah mencoba menutupnya lewat `maks_carry_R`, dan saringan itu **tetap aktif di H-007 dan tetap tembus**. Penyebabnya struktural, bukan penyetelan yang kurang ketat:

1. `carry_terproyeksi_R` adalah **proyeksi**, disusun dari rerata rate 30 hari terakhir dan kerapatan penagihan pada jendela yang berakhir tepat di saat entri.
2. Proyeksi itu dihitung **sekali**, di saat entri, dan **tidak pernah dinilai ulang**. Setelah posisi terbuka, tidak ada apa pun yang memeriksa berapa yang sudah benar-benar terbayar.

Akibatnya, dua keadaan lolos begitu saja: rate yang melonjak **setelah** entri, dan posisi yang dipegang jauh lebih lama daripada yang diandaikan proyeksi. H-007 memperparah keduanya sekaligus. Target 3R dan 4R membuat posisi bertahan lebih lama — keluar karena `umur` melonjak dari 103 di H-002 menjadi **371** — sehingga penagihan funding menumpuk pada posisi yang justru paling lama hidup.

Ini menempatkan riset pada posisi yang tidak nyaman dan harus dinyatakan terus terang: **hasil terbaik yang pernah diukur dijatuhkan oleh gerbang risiko, bukan oleh ekspektasinya.** Menurunkan ambang gerbang adalah jawaban yang dilarang. Yang belum pernah dicoba adalah memperbaiki mesinnya.

## Keputusan

Tambahkan pengaman kedua yang sifatnya berlawanan dengan yang pertama: **keluar paksa saat carry yang sudah TEREALISASI melewati ambang**, dinilai ulang pada pembukaan setiap bar selama posisi berjalan.

Perbedaannya dengan ADR-004 adalah inti dari ADR ini:

| | ADR-004 `maks_carry_R` | ADR-008 `maks_carry_realisasi_R` |
|---|---|---|
| Yang diukur | perkiraan biaya ke depan | biaya yang sudah tertagih |
| Sumber angka | rerata rate 30 hari terakhir | penjumlahan penagihan nyata |
| Kapan dinilai | sekali, di saat entri | tiap bar, sepanjang posisi |
| Tindakan | menolak entri | menutup posisi |
| Bisa salah karena | masa depan berbeda dari masa lalu | — tidak menebak apa pun |

Yang kedua tidak menggantikan yang pertama. Keduanya menjawab pertanyaan berbeda: satu mencegah posisi mahal dibuka, satu lagi menghentikan posisi yang **ternyata** mahal.

### Rincian mekanis

- Medan baru `Konfig.maks_carry_realisasi_R`, bawaan **0.0 yang berarti MATI**. Selama nol, mesin berperilaku persis seperti sebelum ADR-008, dan itu dikunci pengujian, bukan diandaikan. H-001b sampai H-007 tetap dapat diulang bita demi bita.
- Carry terealisasi dihitung lewat `lux.funding_model.funding_dalam_R`, fungsi yang sudah ada dan tandanya sudah diuji tersendiri. **Tidak ada aritmetika funding kedua yang ditulis.** Dua implementasi dari besaran yang sama adalah cara paling andal melahirkan selisih tanda yang tak terdeteksi.
- Pemeriksaan dilakukan pada **pembukaan bar**, dan keluar pada pembukaan bar itu juga dengan slippage yang melawan posisi, alasan keluar `"carry"`.
- Pemeriksaan hanya membaca penagihan sampai pembukaan bar berjalan, sehingga tidak ada lookahead. Batas penagihan mengikuti aturan yang sudah ditetapkan `funding_model`: lebih besar dari waktu masuk, tidak melebihi waktu keluar.
- **Urutan pemeriksaan: umur lebih dulu, baru carry.** Bila keduanya terpicu di bar yang sama, keluarnya di harga yang sama sehingga labanya identik; hanya labelnya yang berbeda. Umur didahulukan supaya semantik ADR-004 tidak bergeser sedikit pun.
- Bila pengaman menyala tetapi jadwal funding tidak ada, **entri ditolak**, sama seperti ADR-004. Menganggap simbol tanpa jadwal berbiaya nol adalah kelalaian yang menyamar sebagai kelulusan.
- Pengaman ini **tidak** menuntut `maks_umur_bar` positif, berbeda dengan saringan proyeksi yang membutuhkannya untuk mendefinisikan umur.

### Akibat pada aritmetika titik impas

`laju_kena_target` menghitung `target / (target + stop)`. Perdagangan yang keluar karena `"carry"` tidak masuk penyebut, sama seperti `umur` dan `akhir_data`, karena hasilnya tidak terpotong di 1R maupun di imbalan. Ini sudah benar secara kebetulan pada kode yang ada; ADR ini menjadikannya **disengaja**, dinyatakan di docstring dan dikunci pengujian.

## Hipotesis H-008

> Dengan sinyal Donchian yang tidak diubah sama sekali, menambahkan keluar paksa saat carry terealisasi melewati ambang yang dipilih walk-forward menghasilkan ekspektasi bersih di luar sampel minimal 0,05R **dan** membuat `invarian_risiko` lulus.

Ruang parameter, **identik dengan H-007 ditambah satu sumbu**:

- `lookback` ∈ {20, 55, 100}
- `imbalan_R` ∈ {1,0, 2,0, 3,0, 4,0}
- `maks_carry_realisasi_R` ∈ {0,0, 0,25, 0,50}

36 kombinasi, satu percobaan, jadi tidak ada koreksi multiplisitas. Kriteria sama persis dengan H-002 dan H-007: ekspektasi ≥ 0,05R, ≥ 100 perdagangan luar sampel, p entri acak ≤ 0,05, jendela positif ≥ 0,5.

### Mengapa grid imbalan tidak dipersempit

H-007 menunjukkan 4R menang di 194 dari 356 jendela. Menghapus 1,0 dan 2,0 dari grid karena hasil itu berarti mempersempit ruang pencarian **setelah** melihat hasilnya, dan itu bentuk penyetelan pasca-hoc yang paling mudah dibela sekaligus paling merusak. Grid imbalan dibiarkan persis seperti H-007.

### Mengapa 0,0 ikut dimasukkan

Ambang 0,0 berarti pengaman ini **mati sepenuhnya**. Memasukkannya membuat percobaan informatif ke dua arah: bila walk-forward jarang memilih nilai selain 0,0, itu bukti bahwa pengaman ini merugikan di dalam sampel, dan bukti itu didapat dari run yang sama tanpa percobaan tambahan. Percobaan yang hanya bisa membenarkan gagasannya sendiri tidak layak dijalankan.

### Ramalan mekanis, ditulis sebelum hasilnya ada

1. Perdagangan yang keluar karena `"carry"` akan berjumlah kecil. Yang ditargetkan adalah ekor, bukan kebanyakan posisi.
2. Kerugian terburuk akan mengecil. Kalau tidak, dugaan bahwa funding-lah penyebab kerugian melampaui 1,5R **salah**, dan itu temuan yang lebih berharga daripada gerbang yang lulus.
3. Ekspektasi kemungkinan besar sedikit **turun** dibanding H-007, karena pengaman memotong posisi sebelum ia sempat menyentuh target. Bila ekspektasinya justru naik, berarti posisi ber-carry tinggi memang rugi secara sistematis, bukan sekadar berisiko.

Ketiganya dapat gagal. Itu memang gunanya ditulis lebih dulu.

## Yang dilarang oleh ADR ini

- Menurunkan ambang `invarian_risiko` dari −1,5R. Ambang ditetapkan sebelum hasil pertama terlihat dan tidak berubah karena hasilnya tidak menyenangkan.
- Menyetel `imbalan_R` langsung ke 4,0. Nilai itu menang setelah hasil H-007 terlihat.
- Menjalankan ulang H-001b sampai H-007 dengan mesin baru. Semuanya sudah divonis.
- Menyentuh `lux/strategi/`. ADR-006 melarang sinyal harga ketujuh, dan ADR-008 tidak membutuhkannya.
- Menambahkan sumbu parameter keempat pada run yang sama. 36 kombinasi sudah batas kewajaran untuk pemilihan dalam sampel; sumbu berikutnya menuntut ADR tersendiri.

## Konsekuensi

Bila H-008 lulus, ia menjadi hipotesis pertama yang lolos seluruh gerbang sekaligus melewati ambang ekspektasi, dan mesin keluar terbukti menjadi tempat keunggulan berada.

Bila H-008 ditolak karena ekspektasi tetapi `invarian_risiko` akhirnya lulus, cacat yang terbuka sejak H-001b tertutup dan pekerjaan berikutnya boleh pindah ke horizon 4h dengan mesin yang sudah bersih.

Bila `invarian_risiko` **tetap** gagal meski carry terealisasi dibatasi keras, maka penyebab kerugian melampaui 1,5R bukan funding. Kandidat berikutnya adalah lompatan harga yang melewati stop, dan itu pertanyaan tentang model eksekusi, bukan tentang biaya.
