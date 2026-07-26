# ADR-014 — H-011 ditolak, dan satuan R yang degenerat

Status: DITERIMA
Tanggal: 2026-07-26 (sesi S13)
Bukti: run `30194733599`, komit laporan `2bb7b963af0096656d2a796633b4f018c77903d4`, sidik `8a6efde6d333d8b5`, 838,1 detik
Berkas: `reports/backtest_h011_semesta_penuh.{json,md}`

## 1. Putusan

**H-011 DITOLAK.** Penolakan ini permanen (aturan 5: hipotesis yang ditolak tetap ditolak).

Kriteria utama yang dibekukan di ADR-013 §8 adalah ekspektasi berbobot perdagangan atas 398 simbol tertahan. Saya menghitungnya sendiri dari `per_simbol`, bukan menerima blok `putusan`:

| Kelompok | n simbol | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|
| Teruji (40 pertama alfabet) | 40 | 11.734 | +622,2348 | **+0,053028** |
| **Tertahan (398)** | 398 | 124.603 | **−11.403,5584** | **−0,091519** |
| Seluruh semesta | 438 | 136.337 | −10.781,3236 | −0,079078 |

Baris teruji **identik bit-per-bit** dengan H-010 (`total_R` 622,2348185492804, 11.734 perdagangan, ekspektasi 0,05302836360569971). Itu bukti kuat bahwa mekanisme benar-benar diimpor tanpa satu perubahan pun; satu-satunya yang berbeda antara H-010 dan H-011 adalah semesta. Pagar pra-terbang `run_h011` bekerja.

Jarak ke ambang: **−0,129078R = −11,22 galat baku** (std per perdagangan 4,24670, galat baku 0,011501, n 136.337). Ini pemakaian galat baku yang sah menurut ADR-013: dipakai untuk **menjatuhkan** klaim, bukan menegakkannya. Selang 95% [−0,101621, −0,056536] tidak menyentuh nol, apalagi 0,05.

Gerbang yang gagal: `entri_acak` (p 0,0631; 18 dari 300 permutasi menyamai atau melampaui), `invarian_risiko` (−470,0612R), `konsentrasi` (tak dapat dinilai), `funding_ekor` (`funding_maks_R` 2,3900 > 0,50).

## 2. Adjudikasi tujuh ramalan beku ADR-013 §8

| # | Ramalan | Hasil | Putusan |
|---|---|---|---|
| 1 | ekspektasi tertahan 0,020–0,045 | −0,091519 | **SALAH** — arah benar (gagal), besaran jauh di luar rentang |
| 2 | ≥0,05 = bukti terkuat | tidak terjadi | cabang tak aktif |
| 3 | <0,020 = hasil 40 simbol adalah derau seleksi | terpicu | **TERPICU** |
| 4 | p entri acak 0,01–0,15; p>0,05 menolak apa pun yang lain | 0,0631 | **BENAR**, dan menolak |
| 5 | trade 100.000–160.000 | 136.337 | **BENAR** (taksiran titik saya 128.487, keliru +6,1%) |
| 6 | retensi_drop_1 ≥ 0,95 | tak dapat dinilai | **TAK TERSELESAIKAN** |
| 7 | durasi 15–60 menit | 838,1 s = **13,97 menit** | **SALAH** — lebih cepat dari lantai yang saya tulis |

Dua benar, dua salah, satu tak terselesaikan. Ramalan 6 cacat sejak ditulis: retensi hanya bermakna bila ekspektasi gabungan positif, jadi saya menulis ramalan yang tidak mungkin dinilai bila hipotesisnya gagal. Itu kesalahan desain ramalan, bukan kelulusan.

## 3. Sebab sesungguhnya: satu simbol, dan satuan R yang runtuh

Angka −0,091519 **tidak** dihasilkan oleh sinyal yang memburuk. Ia dihasilkan oleh satu simbol:

```
USDCUSDT: 29.527 bar, 11 jendela, 649 perdagangan,
          total_R -18.861,0596, ekspektasi_R -29,06173
```

USDCUSDT adalah pasangan stablecoin terhadap stablecoin. ATR-nya terhadap harga hampir nol, sehingga `stop_frac` yang tercatat pada perdagangan terburuk adalah **3,1984e−06**. Biaya dalam satuan R berbanding balik dengan `stop_frac`, jadi biaya transaksi satu perdagangan membengkak ke orde ratusan R: laporan mencatat `transaksi_R` **312,7333** pada perdagangan dengan `R` **−470,0612** dan `kotor_R` hanya −157,3278. Sepuluh perdagangan terburuk di seluruh semesta 438 simbol **seluruhnya** milik USDCUSDT.

Akibatnya di tingkat agregat: rerata biaya transaksi naik dari 0,03534R (H-010) ke **0,12552R**, yakni **3,55 kali**, dan 478 perdagangan berbiaya lebih dari 1R.

Ini bukan temuan pasar. Ini **cacat pengukuran**: ketika ATR/harga menuju nol, R berhenti menjadi satuan risiko yang bermakna, dan setiap besaran yang dinyatakan dalam R menjadi tak terbatas. Mesin dengan patuh menghasilkan angka, dan angka itu tidak berarti apa-apa.

Gerbang `invarian_risiko` menangkapnya (−470,06R vs ambang −1,5). Gerbang bekerja sebagaimana dirancang. Yang gagal adalah **definisi semesta**.

## 4. Godaan yang harus ditolak, dan angka yang mengharamkannya

Diagnostik berikut saya hitung dan catat justru **agar tidak dipakai**:

| Hitungan diagnostik | Nilai |
|---|---|
| Tertahan 398 | −0,091519 |
| Tertahan 397 (tanpa USDCUSDT) | **+0,060163** (123.954 trade, +7.457,5012) |
| Seluruh 437 (tanpa USDCUSDT) | +0,059546 (135.688 trade, +8.079,7360) |
| Simbol tertahan bertotal R positif | 281 dari 398 |
| Median ekspektasi per simbol tertahan | +0,06343 (Q1 −0,02212, Q3 +0,16414) |

**Angka +0,060163 BUKAN hasil dan tidak boleh dikutip sebagai keunggulan yang lolos.** Menghapus USDCUSDT setelah melihat hasilnya adalah penyubsetan simbol pasca-hasil, yang secara eksplisit dilarang di ADR-013 §8. Bila angka itu muncul di mana pun sebagai bukti H-010 atau H-011 sesungguhnya lulus, itu pelanggaran, bukan temuan.

Sekaligus: mengabaikan cacat ini dan menyimpulkan "strategi mati" juga salah. Yang benar dan satu-satunya yang benar: **H-011 ditolak, dan penolakannya tidak memberi informasi tentang sinyal**, karena kriterianya tercemar oleh satuan pengukuran yang runtuh pada satu simbol. Sebuah eksperimen yang tercemar tidak informatif ke arah mana pun. Itu memakan satu hipotesis tanpa membayar pengetahuan.

Koreksi atas diri saya sendiri di paragraf ini: saringan pola nama yang saya pakai untuk mencari pasangan stablecoin lain menangkap `BUSDT` dan `TUSDT`, dan keduanya hampir pasti token bernama "B" dan "T", bukan stablecoin. Jadi angka "tanpa stabil" (+0,060168) berlabel salah dan saya buang. Hanya USDCUSDT yang terbukti degenerat lewat `stop_frac`-nya, dan pembuktian harus lewat `stop_frac`, bukan lewat ejaan nama.

## 5. Apa yang sebenarnya didakwa: ADR-003

Kriteria kelayakan semesta (`config/lux.yaml`, versi 2) adalah:

- `min_bar_1h` 8760
- `min_median_quote_volume_harian` 1.000.000
- `maks_rasio_bar_datar` 0,30

Tidak ada satu pun yang menyentuh volatilitas. USDCUSDT lolos ketiganya dengan mudah: umurnya panjang, volumenya besar sekali, dan barnya tidak datar dalam arti harga-tak-berubah karena masih bergerak beberapa satuan terakhir. Saringan volume bahkan **menarik** simbol seperti ini masuk.

Cacatnya berumur sejak ADR-003 dan tidak terlihat selama sepuluh hipotesis karena keempat puluh simbol pertama secara alfabet tidak memuat satu pun pasangan stablecoin. Ini contoh telanjang dari bahaya yang H-011 memang dirancang untuk mencari: sifat yang hanya tampak di luar 40 simbol itu. Dalam arti itu H-011 berhasil — bukan dengan mengukur keunggulan, melainkan dengan membongkar cacat yang lebih tua daripada dirinya.

## 6. Harga yang sudah terbayar dan tidak bisa ditarik kembali

**Himpunan tertahan sudah habis.** Saya sekarang telah melihat hasil per simbol untuk seluruh 438 simbol pada kerangka 1 jam. Tidak ada lagi simbol yang belum tersentuh di Tier B 1h. Setiap pengujian 1h berikutnya, apa pun bentuknya, bersifat dalam-sampel pada tingkat semesta.

Dimensi yang masih benar-benar bersih hanya dua: **waktu** (ekor harian yang belum masuk arsip bulanan, dan periode paling akhir yang bisa dibekukan sebagai luar sampel) dan **kerangka waktu** (4h, yang bahkan belum tervalidasi). Itu membatasi bentuk semua hipotesis berikutnya, dan pembatasan itu harus diterima, bukan diakali.

## 7. Keputusan

1. H-011 ditolak dan tidak pernah dihitung ulang.
2. `universe_layak_v2` dinyatakan **cacat**, bukan salah sedikit. Ia dipakai oleh H-002 sampai H-011, jadi seluruh papan skor sebelas hipotesis mewarisi cacat ini — tetapi hanya secara laten, karena keempat puluh simbol yang dipakai tidak memuat simbol degenerat. Papan skor tidak dihitung ulang (aturan 5); ia diberi catatan.
3. Lantai volatilitas ditambahkan sebagai **kriteria kelayakan semesta**, bukan sebagai parameter yang bisa dipilih, dan bukan sebagai saringan sinyal.
4. Batas biaya per perdagangan ditambahkan sebagai **pagar risiko** di mesin, sejenis dengan `maks_carry_R`: bukan knob yang dicari nilainya, melalui satu nilai yang dipatok sebelum eksperimen.
5. Karena butir 3 dan 4 mengubah mekanisme, hasilnya adalah **hipotesis baru**, bukan H-010 yang diselamatkan. Dilarang menyebutnya "H-010 setelah perbaikan".

## 8. Pra-registrasi H-012

**Pernyataan.** Keunggulan yang tampak pada H-010 diukur dengan satuan R yang, pada sebagian semesta, tidak bermakna. H-012 mengukur mekanisme yang sama di atas semesta yang setiap simbolnya punya satuan R bermakna, dan dinilai pada **periode waktu terakhir yang dibekukan sebagai luar sampel**, karena himpunan simbol tertahan sudah habis dipakai.

**Perubahan yang diizinkan, seluruhnya dipatok sebelum dijalankan.**

1. Kelayakan semesta: buang simbol yang **median `stop_frac`**-nya sepanjang riwayat berada di bawah **0,004**. Alasan aritmetis, bukan selera: biaya bolak-balik adalah 2·(fee+slippage) = 0,002 dari harga, sehingga pada `stop_frac` 0,004 biaya transaksi tepat 0,5R. Di bawah itu, biaya memakan lebih dari separuh satuan risiko dan tidak ada imbalan realistis yang bisa menutupnya.
2. Pagar mesin: tolak entri yang `stop_frac`-nya membuat biaya transaksi melampaui **0,5R**. Nilai ini sama dengan lantai butir 1 dan dipatok, bukan dicari. Ia harus tercatat sebagai alasan keluar/tolak tersendiri di laporan supaya jumlahnya terlihat.
3. Tidak ada perubahan lain. Grid tetap `lookback` [20, 55, 100] × `imbalan_R` [2, 4, 6, 8], `maks_carry_realisasi_R` 0,25, `maks_umur_bar` 168, ambang 0,05R, `min_trade_luar_sampel` 100, `maks_p_entri_acak` 0,05, `min_jendela_positif_rasio` 0,5.
4. `ulangan` permutasi 300.

**Kriteria utama.** Ekspektasi berbobot perdagangan pada periode luar sampel waktu yang dibekukan, dengan seluruh semesta layak yang baru.

**Ramalan, ditulis sebelum menjalankan, dan merugikan hipotesis saya sendiri.**

1. Jumlah simbol yang tersingkir oleh lantai `stop_frac`: **1 sampai 6**. Bila lebih dari 20 simbol tersingkir, lantai itu terlalu tinggi dan H-012 harus dibatalkan sebelum dinilai, karena ia sudah berubah menjadi seleksi semesta yang agresif.
2. Ekspektasi seluruh semesta baru pada seluruh riwayat: **0,050–0,065**. Ini bukan hasil H-012; ini pemeriksaan konsistensi terhadap diagnostik §4 yang sudah saya lihat, dan karena itu **tidak boleh** dipakai sebagai bukti apa pun.
3. Ekspektasi pada periode luar sampel waktu: **0,010–0,045**, yakni saya meramalkan H-012 **GAGAL**. Alasannya: seluruh angka positif yang pernah saya lihat berasal dari periode yang sudah dilihat, dan tidak ada satu pun bukti bahwa keunggulan ini bertahan di periode yang belum dilihat.
4. p entri acak: **0,01–0,20**. Bila p > 0,05, H-012 ditolak apa pun ekspektasinya.
5. Perdagangan yang ditolak pagar biaya 0,5R: **500–5.000** dari orde 136.000. Bila nol, pagar tidak menyentuh apa pun dan butir 2 berarti seluruh cacat sudah terserap oleh lantai semesta.
6. `invarian_risiko` lulus, yakni kerugian terburuk lebih baik dari −1,5R. Bila masih gagal, masih ada simbol degenerat yang lolos lantai, dan itu temuan yang lebih penting daripada ekspektasinya.
7. Durasi 10–60 menit.

**Yang dilarang setelah hasil terlihat.** Menaikkan atau menurunkan lantai 0,004. Menurunkan pagar 0,5R. Menyubset simbol lagi dengan alasan apa pun. Memindahkan batas periode luar sampel. Menurunkan `ulangan`. Melonggarkan atau mengetatkan 0,05R. Menyebut H-012 sebagai kelanjutan yang sah dari H-010 bila ia lulus tanpa periode luar sampel waktu ikut lulus.

## 9. Aturan yang lahir dari sesi ini

- **22.** Menuntut kesamaan bit pada agregat pecahan adalah pengujian yang menyala pada perilaku yang benar.
- **23.** Pagar yang memastikan masukan **identik** tidak memastikan masukan **sah**. Seluruh pagar `run_h011` lulus, dan semestanya tetap mengandung simbol yang satuan risikonya runtuh.
- **24.** Satu simbol dapat mendominasi agregat 438 simbol. Sebelum sebuah agregat ditafsirkan, ia harus diperiksa terhadap nilai ekstremnya sendiri.
- **25.** Himpunan tertahan habis pada saat pertama kali dilihat. Ia hanya bisa dibelanjakan sekali, jadi ia harus dibelanjakan pada pertanyaan yang mekanismenya sudah bersih.
- **26.** Cacat yang membalik tanda hasil tidak boleh diperbaiki di dalam hipotesis yang sama. Perbaikannya melahirkan hipotesis baru.
- **27.** Eksperimen yang tercemar tidak informatif ke arah mana pun. Ia memakan satu hipotesis tanpa membayar pengetahuan, dan biaya itu harus dicatat sebagai kerugian, bukan sebagai kemajuan.

## 10. Angka terlarang

- **+0,060163R dan +0,059546R** — ekspektasi setelah USDCUSDT dibuang. Dilarang dikutip sebagai keunggulan, kelulusan, atau bukti bahwa H-010 benar. Ia hanya boleh muncul dengan label diagnostik dan larangannya sekalian.
- **+0,060168R** — angka "tanpa stablecoin" yang saringan namanya salah. Dibuang seluruhnya.
- **281 dari 398 simbol positif** dan **median per simbol +0,06343** — rerata setara-bobot per simbol, bukan kriteria yang dipra-registrasi. Dilarang menggantikan kriteria berbobot perdagangan.
- **−0,091519R** — sah dikutip hanya bersama sebabnya, yaitu satuan R yang degenerat. Dikutip sendirian, ia menyesatkan ke arah sebaliknya.
