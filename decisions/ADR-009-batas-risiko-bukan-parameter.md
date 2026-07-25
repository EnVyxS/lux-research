# ADR-009 — Batas risiko bukan parameter

**Status:** diterima
**Tanggal:** 2026-07-26
**Menggantikan sebagian:** ADR-008 (mekanismenya dipertahankan, cara memilihnya dibatalkan)

---

## Konteks

H-008 ditolak. Saya menyimpulkan dari rerata biaya funding 0,0004R bahwa funding bukan penyebab kegagalan gerbang `invarian_risiko`, dan menulis kesimpulan itu ke STATE v11 sebagai fakta.

Kesimpulan itu salah, dan bantahannya ada di berkas yang sama yang saya kutip. `reports/backtest_h008_carry_keras.json` memuat blok `diagnosa_biaya.terburuk`, sepuluh perdagangan terburuk dengan pembongkaran penuh:

| Simbol | R | Kotor R | Transaksi R | **Funding R** | Lebar stop | Jam | Alasan |
|---|---|---|---|---|---|---|---|
| AIOTUSDT | **−1,9769** | −1,0182 | 0,0359 | **0,9228** | 2,83% | 29 | stop |
| ALGOUSDT | −1,4067 | −1,0065 | 0,0135 | 0,3866 | 7,13% | 81 | stop |
| 1000XECUSDT | −1,3869 | −1,0260 | 0,0526 | 0,3083 | 1,88% | 107 | stop |
| AAVEUSDT | −1,3637 | −1,0116 | 0,0236 | 0,3285 | 4,14% | 156 | stop |
| 1000XECUSDT | −1,3215 | −1,0164 | 0,0323 | 0,2728 | 3,15% | 41 | stop |
| ADAUSDT | −1,2698 | −1,0198 | 0,0401 | 0,2098 | 2,46% | 94 | stop |
| 1000FLOKIUSDT | −1,2614 | −1,0211 | 0,0418 | 0,1985 | 2,42% | 93 | stop |
| 1000WHYUSDT | −1,2362 | −1,0189 | 0,0384 | 0,1789 | 2,57% | 50 | stop |
| 1000XECUSDT | −1,2282 | −1,0097 | 0,0190 | 0,1996 | 5,42% | 41 | stop |
| 1000FLOKIUSDT | −1,2154 | −1,0148 | 0,0292 | 0,1714 | 3,49% | 34 | stop |

Aritmetikanya tertutup rapat: −1,0182 − 0,0359 − 0,9228 = −1,9769, persis nilai gerbang.

**Funding menyumbang 46,7% dari kerugian terburuk.** Pada kesepuluh perdagangan itu, funding adalah komponen biaya terbesar, antara 5 sampai 26 kali lipat biaya transaksi.

### Dua kandidat yang saya ajukan, keduanya gugur

1. **Keluar di pembukaan bar yang menganga.** Gugur. Kesepuluhnya beralasan `stop`, dan kotornya berkisar −1,0065 sampai −1,0260 — tepat satu R ditambah slippage. Stop bekerja persis sebagaimana dirancang. Tidak ada yang menganga.
2. **Stop yang sangat rapat.** Gugur. Lebar stop terburuk 2,83% terhadap rerata 3,61%, dan biaya transaksinya 0,0359R. Fee bukan apa-apa di sini.

Kesalahan penalaran saya spesifik dan dapat dinamai: **saya memakai rerata untuk menyimpulkan sesuatu tentang ekor.** Rerata funding 0,0004R dan funding terburuk 0,9228R keduanya benar; yang satu tidak membatasi yang lain. Aturan keempat repo ini — lihat sebaran mentah sebelum berteori — ditulis persis untuk kesalahan ini, dan saya melanggarnya sambil mengutip berkas yang memuat sebarannya.

### Lalu mengapa pengaman ADR-008 tidak menangkapnya?

Bukan karena ambangnya terlalu longgar. Ambang terketat yang dilombakan adalah 0,25R; carry 0,9228R melewatinya hampir empat kali lipat. Bila pengaman aktif, perdagangan itu **pasti** tertutup jauh lebih awal.

Karena ia keluar dengan alasan `stop`, bukan `carry`, maka ia **terbukti berjalan di bawah konfigurasi dengan `maks_carry_realisasi_R = 0,0`**. Ini deduksi, bukan dugaan: tidak ada ambang aktif di grid yang bisa dilewati 0,9228R tanpa memicu keluar. AIOTUSDT punya dua jendela, satu memilih 0,0 dan satu memilih 0,25; perdagangan itu berada di yang pertama.

### Temuan sebenarnya: tujuan pemilih tidak sejalan dengan kriteria gerbang

Walk-forward memilih parameter dengan memaksimalkan skor **dalam sampel**, dan skor itu adalah ekspektasi. Gerbang `invarian_risiko` dinilai **setelahnya**, di luar sampel, dan tidak pernah masuk ke fungsi tujuan.

Pengaman risiko, menurut definisinya, memotong posisi sebelum ia sempat pulih. Itu memakan ekspektasi. Maka pemilih yang hanya melihat ekspektasi akan **selalu** mematikannya bila diberi pilihan. Itulah yang terjadi, dan angkanya tidak ambigu:

| Ambang | Jendela memilihnya |
|---|---|
| 0,0 — mati | **334** dari 356 |
| 0,25 | 22 |
| 0,50 | **0** |

H-008 bukan uji terhadap pengaman carry. Ia adalah uji terhadap **pertanyaan apakah pemaksimal ekspektasi mau memakai pengaman risiko**, dan jawabannya tidak. Saya merancang percobaan yang tidak bisa menjawab pertanyaan yang saya maksudkan.

Ini cacat rancangan yang lebih umum daripada satu hipotesis: **menaruh batas risiko ke dalam grid pemilihan sama dengan meminta izin kepada pemaksimal keuntungan untuk membatasi kerugian.**

---

## Keputusan

**Batas risiko bukan parameter. Ia tidak dilombakan.**

H-009 menjalankan mekanisme ADR-008 yang persis sama, dengan satu perubahan tunggal: `maks_carry_realisasi_R` **dikeluarkan dari ruang parameter** dan dipatok menyala.

Nilai yang dipatok adalah **0,25**, dan asal-usulnya harus dinyatakan supaya tidak disangka dipilih pasca-hoc. Nilai itu sudah ada di `config/lux.yaml` versi 2 sebagai `risiko.maks_carry_R = 0.25` sejak ADR-004, ditetapkan sebelum H-002 dijalankan dan sebelum satu pun hasil H-007 atau H-008 terlihat. Ia bukan pemenang dari grid mana pun — di H-008 ia justru kalah 22 lawan 334.

Grid H-009 karena itu kembali persis ke grid H-007:

- `lookback`: 20, 55, 100
- `imbalan_R`: 1,0 · 2,0 · 3,0 · 4,0
- **12 kombinasi**, sama seperti H-007

Dengan `maks_carry_realisasi_R = 0,25` konstan di seluruh kandidat, dan saringan proyeksi ADR-004 tetap menyala seperti di H-002, H-007, dan H-008.

### Yang dilarang di ADR ini

- Melombakan ambang pengaman dalam bentuk apa pun. Bila 0,25 gagal, yang boleh dilakukan adalah mendaftarkan hipotesis baru dengan ID baru dan ambang yang dibenarkan **sebelum** hasilnya terlihat — bukan menggeser ambang sampai gerbangnya lulus.
- Mematok `imbalan_R` ke 4,0. Ia menang pasca-hoc di H-007 dan tetap dipilih walk-forward.
- Menghitung ulang H-007 atau H-008.
- Melonggarkan ambang `invarian_risiko` dari −1,5R.

---

## Ramalan yang dapat difalsifikasi

Ditulis sebelum run, dan ketiganya bisa salah:

1. **Keluar `carry` melonjak dari 2 menjadi ratusan.** Pengaman kini aktif di seluruh 356 jendela, bukan 22. Bila jumlahnya tetap puluhan ke bawah, berarti pemahaman saya tentang seberapa sering carry mencapai 0,25R masih keliru.
2. **Kerugian terburuk turun di bawah 1,5R dan `invarian_risiko` lulus.** Ini konsekuensi mekanis: tidak ada posisi yang boleh menagih lebih dari 0,25R carry, sehingga kerugian maksimum kira-kira 1R kotor + 0,25R carry + biaya transaksi. Bila gerbang tetap gagal, maka ada sumber kerugian ekor kedua yang belum saya lihat, dan diagnosis ADR ini tidak lengkap.
3. **Ekspektasi turun di bawah 0,04126R.** Pengaman memakan ekspektasi — itu tepat alasan pemilih membuangnya. Ramalan ini adalah pengakuan bahwa H-009 kemungkinan besar **tetap ditolak**, kali ini oleh kriteria 0,05R, bukan oleh gerbang.

Bila ramalan 2 benar dan ramalan 3 salah, H-009 menjadi hipotesis pertama yang lulus seluruhnya. Saya tidak memperkirakan itu, dan mengatakannya di muka supaya tidak bisa mengaku sudah menduga setelahnya.

---

## Konsekuensi

**Bila gerbang lulus dan ekspektasi ≥ 0,05R:** hipotesis pertama yang lulus sejak riset dimulai. Langkah berikutnya bukan perayaan melainkan `--limit 0` atas 438 simbol, karena seluruh angka sejauh ini berasal dari 40 simbol pertama menurut abjad.

**Bila gerbang lulus tetapi ekspektasi < 0,05R:** ini hasil yang paling saya perkirakan. Artinya keunggulan Donchian nyata tetapi tipis, dan biaya menjaga risikonya memakan sisa marginnya. Arah berikutnya menjadi horizon 4h, di mana biaya yang sama dibagi ke pergerakan yang lebih besar.

**Bila gerbang tetap gagal:** diagnosis ADR ini tidak lengkap dan ada sumber kerugian ekor kedua. Yang wajib dilakukan adalah membaca ulang `diagnosa_biaya.terburuk` dari laporan H-009, bukan mengarang mekanisme ketiga.

---

## Catatan metodologis yang dibawa ke seluruh riset

Dua aturan lahir di sini.

**Aturan kesebelas:** rerata tidak mengatakan apa pun tentang ekor. Setiap kali sebuah gerbang menilai nilai ekstrem, angka yang boleh dipakai untuk membantahnya hanya nilai ekstrem, tidak pernah rerata.

**Aturan kedua belas:** batas risiko tidak dilombakan. Apa pun yang dipilih oleh pemaksimal ekspektasi akan tunduk pada ekspektasi; menaruh pengaman ke dalam grid berarti menyerahkan keputusan risiko kepada fungsi tujuan yang tidak melihat risiko.
