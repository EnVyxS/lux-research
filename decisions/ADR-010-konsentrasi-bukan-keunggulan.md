# ADR-010 — Konsentrasi bukan keunggulan

**Status:** diterima, berlaku **mulai H-010**
**Tanggal:** 2026-07-26 (S12)
**Konteks:** H-009 lulus kesembilan gerbang dan ditolak hanya oleh ambang 0,05R. Sebelum mencari 20,9% ekspektasi tambahan, keunggulan yang sudah ada harus diperiksa apakah ia milik strategi atau milik beberapa simbol.

---

## 0. KOREKSI TERLEBIH DAHULU — klaim saya sendiri, ditarik

Di akhir S12 saya menyatakan sebagai temuan yang mengkhawatirkan bahwa **"sepuluh dari 40 simbol menghasilkan 101,2% laba dan 30 sisanya merugi"**, dan menyebutnya fragilitas terbesar yang tersisa. Angkanya benar. **Tafsirannya menyesatkan, dan menyesatkan secara konstruksi.**

Bila sebuah portofolio memuat simbol yang merugi, maka porsi penyumbang teratas terhadap **laba bersih** hampir pasti melewati 100%, tanpa perlu ada konsentrasi sama sekali. Aritmetikanya:

| | Jumlah simbol | R |
|---|---|---|
| Simbol laba | **28** | **+883,62** |
| Simbol rugi | **12** | **−266,35** |
| Bersih | 40 | **+617,28** |

Pembilang "624,89R" diukur terhadap penyebut yang sudah dikurangi 266,35R kerugian. Statistik itu akan menyalakan alarm pada portofolio mana pun yang punya pecundang, termasuk portofolio yang sangat terdiversifikasi. **Ini persis aturan 8: periksa apakah sebuah angka mungkin secara konstruksi sebelum memperlakukannya sebagai temuan.** Saya melanggarnya dalam pesan yang sama di mana saya mengutip aturan 9 dengan benar.

Angka yang tidak menyesatkan, dari `per_simbol` yang sama:

- **28 dari 40 simbol menguntungkan (70%)**, bukan sepuluh.
- **Median ekspektasi per simbol +0,0325R — positif.** Simbol tipikal menguntungkan, bukan simbol terpilih.
- **HHI atas porsi laba bruto 0,0621**, setara **16,1 simbol berbobot sama** dari 28 penyumbang. Itu bukan konsentrasi ekstrem.
- Kuartil ekspektasi per simbol: −0,0170 · median +0,0325 · +0,1401.

Jadi keunggulan H-009 **jauh lebih tersebar daripada yang saya katakan.** Saya menaikkan sebuah artefak aritmetika menjadi "fragilitas paling besar yang tersisa" dan menaruhnya di `STATE.md` v13 sebagai tindakan berikutnya nomor satu. Itu keliru dan diperbaiki di sini.

---

## 1. Yang tetap menjadi kekhawatiran sah

Satu statistik gugur, tetapi pertanyaannya tidak. Ukuran yang benar bukan porsi melainkan **jackknife**: buang penyumbang teratas dan hitung ulang ekspektasi dari nol.

| Dibuang | Simbol terakhir dibuang | Sisa trade | Sisa R | Ekspektasi | Retensi |
|---|---|---|---|---|---|
| 0 | — | 14.925 | 617,28 | **+0,041359** | 100% |
| 1 | ADAUSDT | 14.014 | 503,97 | **+0,035962** | **87,0%** |
| 2 | ALGOUSDT | 13.037 | 430,22 | +0,033000 | 79,8% |
| 3 | 1000FLOKIUSDT | 12.648 | 359,46 | +0,028420 | 68,7% |
| 4 | ALPHAUSDT | 11.966 | 293,64 | +0,024540 | 59,3% |
| 5 | AIOTUSDT | 11.922 | 233,56 | +0,019590 | 47,4% |
| 8 | 1000PEPEUSDT | 11.098 | 78,00 | +0,007028 | 17,0% |
| 10 | — | — | — | **≤ 0** | 0% |

Bacaan yang jujur: **membuang satu simbol terbaik dari empat puluh memangkas 13% ekspektasi, dan itu wajar.** Membuang lima memangkas 53%, dan itu mulai mengkhawatirkan. Ekspektasi baru menjadi nol setelah sepuluh dibuang. Untuk 40 simbol, ini **kerapuhan sedang**, bukan bencana dan bukan pula kesehatan.

Satu pencilan tetap menonjol dan bukan artefak: **AIOTUSDT, ekspektasi +1,36566R per perdagangan** atas 44 perdagangan di 2 jendela — tiga puluh tiga kali rerata portofolio. Simbol berikutnya, 1000000BOBUSDT, +0,43957R atas 58 perdagangan di 2 jendela. Keduanya bersejarah pendek. **Dugaan yang belum diuji:** simbol yang baru terdaftar melewati fase volatilitas awal yang sangat menguntungkan strategi kelanjutan, dan fase itu tidak akan terulang. Bila benar, ekspektasi gabungan mengandung komponen yang tidak dapat diandalkan ke depan. Cara mengujinya ada di data yang sudah dikomit: bandingkan ekspektasi terhadap umur simbol pada saat jendela uji, bukan terhadap simbolnya.

---

## 2. Keputusan

Tambahkan gerbang kesepuluh, **`konsentrasi`**, ke `lux/backtest/gerbang.py`. Ia dinilai dari agregat per simbol yang sudah dihasilkan runner, jadi biayanya nol dan tidak menambah satu detik pun waktu run.

Ambang ditetapkan **sekarang, sebelum satu hipotesis pun dinilai olehnya**, dan diturunkan dari prinsip, bukan dari angka H-009:

| Sub-uji | Definisi | Ambang | Alasan prinsipnya |
|---|---|---|---|
| `drop_1_positif` | ekspektasi setelah membuang penyumbang bersih terbesar | **> 0** | strategi yang keunggulannya lenyap tanpa satu simbol bukan strategi |
| `drop_5persen_positif` | ekspektasi setelah membuang ⌈0,05·N⌉ penyumbang teratas | **> 0** | tidak ada pasar yang menjamin dua puluh simbol terbaikmu hadir lagi |
| `retensi_drop_1` | ekspektasi drop-1 dibagi ekspektasi penuh | **≥ 0,60** | satu simbol dari N tidak boleh memiliki lebih dari 40% keunggulan |
| `median_simbol_positif` | median ekspektasi per simbol | **> 0** | keunggulan harus milik simbol tipikal, bukan milik ekor |
| `porsi_bruto_teratas` | R simbol terbesar dibagi **laba bruto** | **≤ 0,25** | diukur terhadap laba bruto, bukan bersih, agar tidak menyesatkan seperti §0 |

Seluruh sub-uji harus lulus. **Sub-uji yang tidak dapat dinilai berarti GAGAL**, sama seperti sembilan gerbang lain.

Denominator `porsi_bruto_teratas` sengaja laba bruto. Itu satu-satunya pelajaran teknis dari kekeliruan di §0 yang perlu dikodekan: **jangan pernah membangun metrik konsentrasi di atas penyebut bersih.**

---

## 3. Mengapa gerbang ini TIDAK diterapkan ke H-009

Saya sudah melihat angka konsentrasi H-009 sebelum menulis ambang di atas. Menerapkan ambang yang ditulis sesudah data terlihat lalu menyebutnya "lulus" adalah tepat mekanisme yang meracuni bot v8.4. Karena itu:

- **`konsentrasi` mengikat mulai H-010.** Vonis H-001b sampai H-009 tidak berubah; seluruhnya tetap DITOLAK.
- Nilai H-009 dicatat sebagai **deskriptif, bukan putusan**: `drop_1_positif` +0,03596 · `drop_5persen_positif` (⌈2⌉) +0,03300 · `retensi_drop_1` 0,8695 · `median_simbol_positif` +0,0325 · `porsi_bruto_teratas` 113,30/883,62 = 0,1282.
- Kelimanya akan lulus. **Itu bukan bukti apa pun**, karena ambangnya ditulis dengan angka-angka itu terpampang. Ia hanya berarti gerbang ini tidak dikalibrasi untuk menjatuhkan pekerjaan yang sudah ada.

---

## 4. Yang secara tegas DILARANG oleh ADR ini

1. **Membuang simbol yang merugi dari universe.** Dua belas simbol merugi −266,35R. Membuangnya menaikkan ekspektasi dari 0,0414R ke sekitar 0,0752R dan **langsung melewati ambang 0,05R.** Itu bukan penemuan, itu survivorship bias murni — pemilihan berdasarkan hasil yang tidak dapat diketahui di muka. Inilah cacat yang membuat seluruh pengetahuan bot v8.4 dibuang. **Angka 0,0752R dicatat di sini justru agar ia dikenali sebagai jebakan, bukan sebagai sasaran.**
2. **Memakai gerbang `konsentrasi` sebagai penyaring simbol.** Ia mendiagnosis portofolio, ia tidak pernah memilih anggotanya.
3. **Membuang AIOTUSDT karena ekspektasinya tidak masuk akal.** Bila pencilan itu artefak, penyebabnya harus ditemukan dan diperbaiki untuk semua simbol; bila ia nyata, ia berhak ikut. Keduanya bukan alasan menghapus satu baris.
4. **Menurunkan ambang 0,05R.** Jarak 0,008641R harus ditutup oleh mekanisme, bukan oleh ambang.

---

## 5. Ramalan, ditulis sebelum kodenya ada

1. Gerbang `konsentrasi` **tidak akan menjatuhkan** hipotesis kelanjutan mana pun pada 40 simbol; kelima sub-ujinya lulus dengan margin lebar. Ia akan berguna nanti, saat `--limit 0` menaikkan universe ke 438 dan saat hipotesis dengan sedikit perdagangan muncul.
2. Bila `--limit 0` dijalankan, **ekspektasi akan turun**, bukan naik. Empat puluh simbol pertama urut abjad memuat proporsi meme-coin berumur pendek yang tinggi, dan pencilan seperti AIOTUSDT akan terlarutkan oleh 398 simbol lain.
3. Uji ekspektasi terhadap umur simbol akan menunjukkan **hubungan negatif**: simbol muda lebih menguntungkan. Bila hubungan itu ada, ia bukan keunggulan yang dapat diandalkan melainkan efek pasar baru.

Ramalan kedua dan ketiga adalah pekerjaan berikutnya, dan **yang ketiga dapat diuji dari laporan yang sudah dikomit**, sementara yang kedua butuh satu run `--limit 0`.

---

## 6. Konsekuensi

- `lux/backtest/gerbang.py` mendapat `gerbang_konsentrasi(per_simbol)` dan `NAMA_GERBANG` menjadi sepuluh nama.
- `lux/backtest/runner.py` meneruskan agregat per simbol ke penilai gerbang.
- Laporan `reports/backtest_*.md` mendapat tabel jackknife.
- Pengujian baru wajib: penyebut laba bruto, portofolio sintetis satu simbol harus GAGAL, portofolio rata harus LULUS, portofolio kosong harus GAGAL bukan lulus diam-diam.
