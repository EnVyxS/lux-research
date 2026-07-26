# Ekspektasi terhadap umur simbol — ramalan 3 ADR-010

**Putusan: ramalan DIFALSIFIKASI.** Tidak ada hubungan monoton antara umur
simbol dan ekspektasi per simbol.

## Provenans

Berkas ini **bukan** keluaran workflow. Ia dihitung di sandbox agen
(`/data/umur.py`) dari blok `per_simbol` pada
`reports/backtest_h009_carry_dipatok.json` yang sudah terkomit di
`77b7492ce0635a7ba9035509ccc28bc04bf3dd31`. Tidak ada data baru diunduh dan
tidak ada backtest dijalankan ulang. Aturan 9 berlaku: laporan yang sudah
terkomit sudah memuat jawabannya.

Proksi umur adalah **jumlah jendela walk-forward**, yang ditentukan sepenuhnya
oleh panjang riwayat bar (latih 4320 + embargo 168 + uji 2160 per jendela).
Simbol tertua punya 24 jendela, termuda hanya 2.

## Gerbang aritmetika

Dijalankan lebih dulu, sebelum satu kesimpulan pun ditarik:

| Besaran | Dihitung ulang | Terkomit |
|---|---|---|
| Simbol | 40 | 40 |
| Perdagangan | 14.925 | 14.925 |
| Jendela | 356 | 356 |
| Total R | 617,2769 | 617,2774 |
| Ekspektasi | 0,041359 | 0,041359 |

Selisih 0,0005R pada total berasal dari pembulatan empat desimal per simbol di
blok `per_simbol`, bukan dari kekeliruan.

## Hasil utama

| Ukuran | Nilai |
|---|---|
| Spearman(umur, ekspektasi) | **−0,0336** |
| p dua sisi, permutasi 20.000, seed 42 | **0,8351** |
| Permutasi yang menyamai atau melampaui \|rho\| | 16.702 dari 20.000 |

Delapan puluh tiga persen pengacakan menghasilkan hubungan sekuat atau lebih
kuat daripada yang teramati. Ini bukan efek lemah; ini ketiadaan efek.

## Per ember umur, ditimbang perdagangan

| Ember | Simbol | Trade | Total R | Ekspektasi | Median simbol |
|---|---|---|---|---|---|
| muda 2–4 jendela | 16 | 2.052 | +115,61 | +0,056342 | +0,041073 |
| menengah 5–9 | 10 | 2.831 | +193,19 | +0,068240 | +0,115302 |
| tua 10–19 | 9 | 5.277 | +137,52 | +0,026059 | +0,009169 |
| tertua 20–24 | 5 | 4.765 | +170,96 | +0,035878 | +0,031264 |

Polanya **tidak monoton**. Ember tertinggi adalah menengah, bukan termuda, dan
ember tertua lebih tinggi daripada ember tua. Sebuah hubungan yang naik lalu
turun lalu naik lagi pada empat titik dengan 40 simbol adalah derau.

## Belah dua pada tiga batas

Ketiga batas ditulis dalam satu skrip sebelum keluarannya dilihat.

| Batas | Muda | Ekspektasi muda | Tua | Ekspektasi tua | Selisih |
|---|---|---|---|---|---|
| < 5 jendela | 16 simbol, 2.052 trade | +0,056342 | 24 simbol, 12.873 trade | +0,038970 | +0,017372 |
| < 8 jendela | 21 simbol, 3.297 trade | +0,050253 | 19 simbol, 11.628 trade | +0,038837 | +0,011416 |
| < 10 jendela | 26 simbol, 4.883 trade | +0,063240 | 14 simbol, 10.042 trade | +0,030719 | +0,032521 |

Ketiganya menunjuk arah yang sama, dan itu satu-satunya isyarat yang tersisa.
Tetapi Spearman atas seluruh 40 titik nol, sehingga arah yang konsisten pada
tiga potongan yang saling bertumpang tindih **bukan** bukti tambahan — ketiga
potongan itu memakai data yang sebagian besar sama.

## Kendali yang membatalkan tafsir kausal

| | |
|---|---|
| Spearman(umur, jumlah trade) | **+0,9668** |
| Spearman(jumlah trade, ekspektasi) | −0,1685 |

Umur dan jumlah perdagangan hampir kolinear sempurna, sebagaimana mestinya:
riwayat lebih panjang berarti lebih banyak jendela dan lebih banyak entri.
Dengan 40 titik keduanya tidak dapat dipisahkan. Andaikan efeknya nyata, kita
tetap tidak akan tahu apakah yang berbicara adalah umur, jumlah sampel, periode
kalender listing, atau jenis aset — enam belas simbol termuda didominasi
listing meme dan AI 2024–2025, yang menjalani rezim pasar yang berbeda.

## Yang menghasilkan dugaan ini, dan kekeliruannya

Dugaan lahir dari dua simbol: AIOTUSDT +1,36566R per trade dengan 2 jendela dan
44 perdagangan, serta 1000000BOBUSDT +0,43957R dengan 2 jendela dan 58
perdagangan. Keduanya muda dan keduanya ekstrem, jadi saya menyimpulkan muda
berarti untung.

Itu penalaran dari **ekor sebaran**, bukan dari sebarannya. Empat puluh empat
perdagangan adalah sampel yang wajar menghasilkan +1,37R semata karena
keberuntungan bila ekspektasi sejatinya nol. Ini kelas kekeliruan yang sama
dengan "rerata funding 0,0004R berarti funding tidak bersalah" di S12 dan
dengan "porsi 101,2%" di S11: menyimpulkan bentuk sebaran dari satu ringkasan
yang tidak mengukur bentuk itu.

## Konsekuensi

1. Asumsi "ekspektasi bergantung pada umur simbol" **dihapus**, bukan
   diturunkan prioritasnya. Ia telah diuji dan gagal.
2. Tidak ada penyaringan berbasis umur yang boleh masuk ke konfigurasi. Bila
   nanti muncul, ia harus lahir dari mekanisme yang dinyatakan lebih dulu,
   bukan dari berkas ini.
3. Membuang simbol muda **menurunkan** ekspektasi dari 0,041359 ke 0,038970,
   makin jauh dari ambang 0,05. Jadi tidak ada godaan yang perlu ditahan di
   sini, dan itu justru kebetulan yang menguntungkan.
4. Simbol muda menyumbang 13,7% perdagangan dan 18,7% laba bersih. Angka kedua
   memakai penyebut bersih dan karena itu **tidak boleh** disebut ukuran
   konsentrasi (aturan 15). Ia dicatat hanya sebagai porsi, bukan sebagai bukti.
