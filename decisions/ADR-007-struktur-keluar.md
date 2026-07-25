# ADR-007 — H-007: yang diuji adalah titik impas, bukan sinyal

**Status:** diterima · ditulis sebelum kodenya dijalankan
**Tanggal:** 2026-07-26
**Terkait:** ADR-006 (melarang hipotesis sinyal harga ketujuh pada 1h)

## Koreksi terhadap catatan sesi sebelumnya

STATE v9 mencatat dugaan bahwa keunggulan Donchian berasal dari **segelintir
perdagangan berekor panjang**, dan menjadikannya pekerjaan berikutnya.

**Dugaan itu salah, dan salahnya dapat dibuktikan tanpa menjalankan apa pun.**
Mesin ini keluar pada target 2R atau stop 1R. Sisi kanan sebaran **dipotong di
2R secara desain**. Ekor panjang tidak mungkin ada, karena tidak ada mekanisme
yang membiarkan satu perdagangan pun melampauinya. Seharusnya itu terlihat dari
konstruksi mesinnya sendiri, bukan diusulkan sebagai penelitian.

Dengan payoff terpotong, seluruh ekspektasi ditentukan oleh **satu angka**: laju
kena target. Dan angka itu sudah tercatat di setiap laporan yang pernah dibuat.

## Bukti: enam hipotesis terurut sempurna menurut satu angka

Dengan stop 1R dan target 2R, ekspektasi kotor adalah `3p − 1`, dan titik impas
kotor berada tepat di **p = 1/3**. Dihitung dari histogram alasan keluar yang
sudah dikomit, tanpa run baru:

| Hipotesis | Target | Stop | Laju kena target | Kotor `3p−1` | Bersih tercatat | Seretan biaya |
|---|---|---|---|---|---|---|
| **H-002** Donchian + carry | 6.707 | 11.909 | **0,36028** | +0,08084 | **+0,03159** | 0,04926 |
| H-004 + ADX ≥ 30 | 2.659 | 5.127 | 0,34151 | +0,02453 | −0,01818 | 0,04272 |
| H-005 entri retest | 4.057 | 7.962 | 0,33755 | +0,01265 | −0,03571 | 0,04836 |
| H-006 sapuan likuiditas | 6.032 | 13.993 | 0,30122 | −0,09633 | −0,13449 | 0,03815 |
| H-003 pembalikan skor-z | 7.503 | 20.997 | 0,26326 | −0,21021 | −0,24782 | 0,03761 |

Urutannya sempurna. Seretan biaya nyaris konstan di 0,038–0,049R. **Tidak ada
satu pun hipotesis yang gagal karena alasan yang unik**; semuanya adalah satu
variabel yang sama, digeser sedikit ke sana kemari.

H-002 melampaui titik impas hanya **2,70 poin persen**. Untuk mencapai ambang
lulus 0,05R dengan seretan yang sama, laju kena target harus 0,36642 — **0,61
poin persen** di atas capaiannya, setara sekitar **114 pemenang tambahan** dari
18.616 perdagangan. Sedekat itu, dan tetap gagal.

## Keputusan

Seluruh riset sejauh ini menggeser `p` sambil membiarkan titik impasnya tetap di
1/3. Yang belum pernah disentuh adalah **titik impasnya sendiri**, padahal titik
impas adalah fungsi langsung dari rasio imbalan:

| Imbalan | Titik impas kotor |
|---|---|
| 1R | 0,5000 |
| 2R (dipakai selama ini) | 0,3333 |
| 3R | 0,2500 |
| 4R | 0,2000 |

**H-007** menguji struktur keluar dengan sinyal yang **tidak diubah sama sekali**
(Donchian, persis H-002). Ruang parameter: `lookback` ∈ {20, 55, 100} ×
`imbalan_R` ∈ {1,0, 2,0, 3,0, 4,0} = **12 kombinasi**, dipilih walk-forward di
dalam sampel dan dinilai di luar sampel seperti biasa.

Ini **bukan** pelanggaran ADR-006. Yang dilarang di sana adalah sinyal harga
ketujuh. H-007 memakai sinyal yang sudah ada dan mengubah mesin keluarnya. Untuk
menegaskan hal itu, `lux/strategi/` tidak disentuh sama sekali oleh ADR ini.

## Yang sudah dapat diramalkan, dan mengapa itu bukan alasan tidak menguji

Menaikkan imbalan hampir pasti **menurunkan** laju kena target: target yang lebih
jauh lebih jarang tercapai sebelum stop tersentuh. Pertanyaan yang sesungguhnya
adalah apakah penurunannya lebih lambat atau lebih cepat daripada penurunan titik
impas. Bila 3R menurunkan `p` dari 0,360 ke sekitar 0,28 sementara titik impas
turun ke 0,250, ekspektasi kotor naik dari 0,081 ke 0,120. Bila `p` jatuh ke
0,240, ekspektasi kotor menjadi negatif. **Arah taruhannya tidak dapat diketahui
tanpa mengukur**, dan itulah definisi percobaan yang layak dijalankan.

Satu keuntungan mekanis yang dapat dinyatakan di muka: imbalan yang lebih besar
menghasilkan lebih **sedikit** perdagangan per satuan waktu, sehingga seretan
biaya per R mengecil. Itu ramalan yang ikut diuji, bukan pembenaran hasil.

## Perubahan mesin yang diperlukan

`jalankan_walk_forward` selama ini memakai satu `Konfig` untuk seluruh kandidat,
sehingga parameter keluar tidak dapat ikut dipilih. Ditambahkan argumen opsional
`buat_konfig(params, konfig_dasar) -> Konfig`.

**Tanpa argumen itu, perilakunya identik dengan sebelumnya.** Itu syarat mutlak:
`run_wf.py`, `run_h002.py`, dan `run_h003.py` tidak boleh berubah hasilnya, dan
pengujian mengunci hal ini secara langsung dengan membandingkan hasil jalur lama
dan jalur baru.

## Yang dilarang

- Menambah nilai `imbalan_R` setelah hasil terlihat. Empat nilai, sekali jalan.
- Mengubah stop 2×ATR pada ADR ini. Bila stop ikut dijadikan parameter, ruang
  pencarian menjadi 36 kombinasi dan hasil apa pun akan sulit dipercaya. Stop
  adalah hipotesis terpisah bila memang perlu.
- Menjalankan ulang H-001b sampai H-006, atau menyetel ulang ambang mana pun.
- Menyimpulkan bahwa titik impas yang lebih rendah "lebih baik" tanpa melihat
  laju kena target yang menyertainya. Keduanya bergerak bersama; hanya
  ekspektasi bersih di luar sampel yang menjadi putusan.
