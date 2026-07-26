# ADR-011 — Gerbang funding yang sadar ekor

**Status:** diterima
**Tanggal:** 2026-07-26
**Berlaku mulai:** H-010. Vonis H-001b sampai H-009 **tidak berubah**.
**Menggantikan:** tidak ada. Melengkapi gerbang `funding` yang sudah ada, dan menurunkan pangkatnya menjadi pemeriksaan kebersihan.

---

## 1. Masalah

Gerbang `funding` yang berjalan sejak H-001b menilai **total funding mutlak** seluruh perdagangan. Dua keadaan berikut sudah dikomit dan dapat dibaca siapa pun:

| | H-008 | H-009 | Selisih |
|---|---|---|---|
| Nilai gerbang `funding` | 10.253,97 | 10.199,59 | **−0,53%** |
| Putusan gerbang `funding` | LULUS | LULUS | sama |
| Perdagangan terburuk | **−1,9769R** | **−1,2698R** | **+36%** |
| Funding pada perdagangan terburuk | **0,9228R (46,7%)** | 0,2098R (16,5%) | **−4,4×** |
| Putusan gerbang `invarian_risiko` | GAGAL | LULUS | berubah |

Antara kedua run itu, funding berhenti menjadi penyebab kegagalan gerbang risiko. Gerbang funding **tidak bergerak sama sekali** — setengah persen, jauh di dalam derau. Ia lulus ketika funding memakan 46,7% kerugian terburuk, dan lulus lagi ketika tidak.

**Gerbang yang memberi jawaban sama pada dua keadaan yang bertolak belakang tidak memuat informasi.** Ini aturan 11 dalam bentuk paling telanjang: total adalah rerata dikali jumlah, dan rerata tidak mengatakan apa pun tentang ekor. Rerata funding H-009 adalah 0,000328R per perdagangan; perdagangan terburuk H-008 membayar 0,9228R, yaitu **2.813 kali** rerata itu. Tidak ada agregat yang bisa melihat rasio semacam itu.

Biaya kekeliruan ini sudah nyata: selama H-007 dan H-008, funding merupakan penyebab terukur kegagalan `invarian_risiko` sementara gerbang funding melaporkan sehat. Selama dua hipotesis, gerbang itu adalah titik buta yang menyamar sebagai gerbang — aturan 10.

## 2. Keputusan

Tambahkan gerbang **kesebelas** bernama `funding_ekor`, dan **jangan hapus** gerbang `funding`.

**Mengapa yang lama tetap tinggal.** Satu-satunya hal yang benar-benar dipastikan gerbang `funding` adalah bahwa jadwal funding nyata betul-betul dimuat dan dipakai, bukan diganti pembagi delapan jam tetap. Itu tetap layak diperiksa. Menghapusnya juga akan mengubah arti nama gerbang di seluruh laporan yang sudah dikomit, dan laporan lama tidak boleh berubah maknanya secara retroaktif. Jadi `funding` bertahan sebagai pemeriksaan kebersihan, dengan tugasnya dinyatakan ulang secara jujur: **ia memastikan jadwal dipakai, bukan memastikan biaya funding aman.**

**Letak kode.** Modul terpisah `lux/backtest/funding_ekor.py`, sama seperti `konsentrasi.py`. Alasannya identik dan sudah dibayar mahal: gerbang baru mengimpor `Gerbang` dan `_gagal_tak_ternilai` dari `gerbang.py`, jadi impor balik dari `gerbang.py` akan menutup siklus seperti cacat `4b77617`. `NAMA_GERBANG` tetap satu-satunya daftar resmi dan menjadi **sebelas** nama.

## 3. Ukuran dan ambang — ditetapkan sebelum kode ditulis

Satuan seluruh besaran adalah R, yaitu funding dibagi risiko nominal perdagangan, sama seperti `rincian_R` yang sudah dipakai `diagnosa_biaya`.

| Sub-uji | Ambang | Dasar penetapan |
|---|---|---|
| `porsi_funding_ekor_maks` | **≤ 0,35** | porsi funding terhadap total kerugian, diambil **maksimum atas sepuluh perdagangan terburuk**; lihat turunan di bawah |
| `funding_maks_R` | **≤ 0,50** | dua kali ambang pengaman 0,25R, memberi ruang satu bar kelewatan |
| `porsi_trade_di_atas_pengaman` | **≤ 0,005** | pengaman menyala 16 dari 14.925 = 0,107%; ambang memberi kelonggaran lima kali |
| `jadwal_dimuat` | wajib benar | tanpa jadwal nyata, ketiga besaran di atas tidak berarti |

**Nilai yang dilaporkan `Gerbang.nilai` adalah `porsi_funding_ekor_maks`,** karena hanya besaran itu yang membedakan H-008 dari H-009. Empat sub-uji dilaporkan lengkap di `catatan`, dan nama sub-uji yang gagal ikut ditulis — gerbang yang meringkas empat sub-uji menjadi satu angka tanpa menyebut yang mana yang jatuh menyembunyikan tiga per empat alasannya.

**Sub-uji yang tidak dapat dinilai berarti GAGAL,** tanpa pengecualian, sesuai doktrin yang sudah berlaku.

### Turunan ambang 0,35 — dari konstruksi, bukan dari selera

Perdagangan yang mati di stop kehilangan sekitar 1,00R kotor; biaya transaksi rerata 0,034R. Pengaman ADR-009 mengizinkan carry terealisasi sampai 0,25R. Maka batas atas porsi funding pada perdagangan stop yang **sah menurut pengaman** adalah

```
0,25 / (1,00 + 0,25 + 0,034) = 0,195
```

Pengaman diperiksa pada batas bar, jadi satu bar terakhir dapat menambah carry sebelum keluar terlaksana. Ambang dinaikkan ke **0,35**, kira-kira 1,8 kali batas konstruksi, untuk menampung kelewatan itu tanpa menampung kebocoran.

**Pengungkapan yang wajib disertakan:** angka 0,35 duduk di antara dua keadaan yang **sudah saya lihat** — 0,467 milik H-008 dan 0,165 milik perdagangan terburuk H-009. Turunan konstruksi di atas memberinya alasan, tetapi saya tidak berpura-pura menetapkannya dalam keadaan buta. Justru karena itu gerbang ini **mengikat mulai H-010** dan **tidak** diterapkan ke belakang, persis perlakuan ADR-010. Ambang yang ditulis setelah melihat data hanya boleh menghakimi data yang belum ada.

### Bukti bahwa ukuran ini bergigi

Syarat minimum bagi gerbang pengganti: ia harus memisahkan dua keadaan yang gagal dipisahkan gerbang lama.

| | Gerbang lama | `funding_ekor` |
|---|---|---|
| H-008 | 10.253,97 LULUS | **0,467 GAGAL** |
| H-009 | 10.199,59 LULUS | 0,165 lulus † |

† Enam dari sepuluh perdagangan terburuk H-009 memuat nilai funding di laporan yang dikomit, dan porsinya 0% sampai 16,5%. **Empat sisanya tidak diterbitkan, jadi nilai H-009 yang sebenarnya belum diketahui dan hanya dapat dihitung oleh run.** Baris itu adalah ramalan, bukan fakta, dan ditandai demikian.

Jadi gerbang lama memberi selisih 0,5% pada dua keadaan yang berbeda 4,4 kali di ekor; gerbang baru memberi vonis berlawanan. Itu syarat yang harus dipenuhi, dan dipenuhi.

## 4. Ramalan — ditulis sebelum satu baris kode dan sebelum satu run

Aturan 14. Dua dari tiga ramalan H-009 salah, dan aturan 13 lahir dari kesalahan itu.

1. **`porsi_funding_ekor_maks` untuk H-009 akan mendarat antara 0,14 dan 0,20.** Enam nilai yang diterbitkan berkerumun di 0,141–0,165, dan pengaman memotong tepat yang di atas 0,25R. Bila ia melewati 0,35, berarti keempat perdagangan yang funding-nya tidak diterbitkan menyimpan sesuatu yang belum saya lihat, dan **diagnosis ADR-009 harus diperiksa ulang**, bukan ambangnya yang dilonggarkan.
2. **`porsi_trade_di_atas_pengaman` akan berada antara 0,00107 dan 0,005,** yaitu antara 16 dan 75 perdagangan dari 14.925. Batas bawahnya persis jumlah penyalaan pengaman. Sub-uji ini **berisiko gagal**, dan itu disengaja: bila jumlah perdagangan yang benar-benar berakhir di atas 0,25R jauh melebihi jumlah penyalaan pengaman, pengamannya bocor. Kegagalan di sini adalah temuan, bukan gangguan.
3. **`funding_maks_R` untuk H-009 akan berada antara 0,25 dan 0,50.** Bila ia melewati 0,50, ada perdagangan yang lolos dari pengaman sama sekali dan itu cacat mesin, bukan cacat gerbang.

Ketiganya dinilai terhadap run H-010, bukan terhadap H-009, karena H-009 sudah divonis dan tidak dihitung ulang. Yang dapat diperiksa lebih awal tanpa run: tidak ada. **Berbeda dengan konsentrasi dan umur simbol, sebaran funding per perdagangan tidak ada di laporan yang dikomit** — hanya rerata dan sepuluh terburuk. Aturan 9 sudah diperiksa dan jawabannya tidak; karena itu gerbang ini memang butuh run.

## 5. Yang tidak diputuskan di sini

- **Funding sebagai sinyal arah** tetap belum diuji dan bukan urusan ADR ini. Gerbang mengukur biaya, bukan kandungan informasi.
- **Ambang pengaman 0,25R tidak disentuh.** Melombakannya dalam bentuk apa pun tetap dilarang oleh ADR-009.
- **Ambang ekspektasi 0,05R tidak disentuh.** Gerbang tidak boleh menjadi jalan memutar menuju kelayakan.

## 6. Utang yang diakui

`lux/funding.py::gerbang_lulus` masih terlalu longgar dan berdiri di jalur ingest, bukan di jalur backtest. Ia tidak diperketat dalam ADR ini agar satu perubahan hanya menguji satu hal. Dicatat sebagai utang terbuka, bukan diabaikan.

## 7. Konsekuensi

- `NAMA_GERBANG` menjadi **sebelas**. `semua_lulus` sudah memakai `len(NAMA_GERBANG)`, jadi tidak ada literal yang perlu disentuh — keuntungan langsung dari penyambungan gerbang kesepuluh.
- Tiga orkestrator beku (`run_wf`, `run_h002`, `run_h003`) kini kurang dua gerbang dan laporannya akan gagal bila dijalankan lagi. Itu pernyataan yang benar: keduanya memang tidak mengukur apa pun tentang konsentrasi maupun ekor funding. Angka lama di `reports/` tidak berubah.
- Pengujian wajib sebelum penyambungan: perdagangan tanpa funding LULUS; satu perdagangan dengan porsi 0,50 GAGAL; daftar perdagangan kosong GAGAL, bukan lulus diam-diam; jadwal tidak dimuat GAGAL dengan sebab tertulis; perdagangan menguntungkan tidak boleh masuk perhitungan porsi kerugian.
- Modul berdiri hijau sendiri lebih dulu, penyambungan ke `NAMA_GERBANG` menyusul di push terpisah.
