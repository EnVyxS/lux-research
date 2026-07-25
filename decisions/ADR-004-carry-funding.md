# ADR-004 — Batas umur posisi dan saringan carry funding

Status: diterima · 2026-07-26 · menggantikan tidak ada

## Konteks

Run H-001b (`3eea9ee`, laporan `reports/backtest_h001.md`) ditolak oleh dua hal
sekaligus: ekspektasi 0,0309R di bawah ambang 0,05R, dan gerbang
`invarian_risiko` gagal pada kerugian terburuk **-2,585R**.

Pembongkaran biaya per perdagangan menutup satu tafsiran dan hanya menyisakan
satu. Perdagangan terburuk itu (ANIMEUSDT) memuat `kotor_R` -1,013,
`transaksi_R` 0,026, dan `funding_R` **1,545**, dengan posisi dipegang 130 jam.
Biaya transaksi bukan penyebabnya; besarnya hanya 1,7% dari kelebihan kerugian.
Delapan dari sepuluh perdagangan terburuk berpola sama: kotor mendekati -1R,
transaksi di bawah 0,08R, sisanya funding.

Mesin mengisi stop tepat di harga stop, sehingga kerugian yang bersumber dari
harga tidak dapat melewati 1R. Kerugian di luar itu wajib berasal dari biaya.
Karena transaksi terlalu kecil untuk menjelaskannya, yang tersisa adalah
funding, dan funding tumbuh sepenuhnya sebagai fungsi lama posisi dipegang.

Strategi breakout Donchian tidak punya batas waktu sama sekali. Sebuah posisi
dapat menggantung ratusan jam di antara stop dan target sambil membayar funding
tiap empat atau delapan jam. Pada simbol bercarry ekstrem — 1000WHYUSDT 60,7%
per tahun, 1000000BOBUSDT 60,1%, BROCCOLIF3BUSDT 57,0% (`reports/funding_check.md`
@ `0448a67`) — biaya menahan posisi seminggu saja sudah melampaui risiko yang
dipertaruhkan.

## Yang TIDAK boleh dilakukan

Ambang `invarian_risiko` **tidak** dilonggarkan dari -1,5R. Kriteria
pra-registrasi H-001b **tidak** disunting. Keduanya akan mengubah gerbang
menjadi angka yang dapat dinegosiasikan, dan sembilan gerbang di proyek ini
dibangun justru untuk menolak negosiasi semacam itu.

H-001b tetap **DITOLAK** selamanya. Hasilnya tidak dihapus dan tidak dihitung
ulang.

## Keputusan

Dua saringan kelayakan perdagangan didaftarkan sebagai **hipotesis baru H-002**,
bukan sebagai perbaikan H-001b.

1. **Batas umur posisi** (`maks_umur_bar`). Posisi yang mencapai umur maksimum
   ditutup pada **pembukaan bar berikutnya**, bukan pada penutupan bar saat
   umur tercapai. Pembukaan bar mendahului pergerakan intrabar, sehingga
   penutupan karena umur dinilai sebelum stop dan target bar itu diuji. Urutan
   sebaliknya akan memberi posisi satu bar gratis untuk menyentuh target.

2. **Saringan carry terproyeksi** (`maks_carry_R`). Sebelum posisi dibuka,
   ongkos funding yang diperkirakan selama umur maksimum dibandingkan dengan
   risiko yang dipertaruhkan. Bila melebihi ambang, entri dibatalkan.

   Proyeksinya **hanya memakai data masa lalu**: rerata rate dan jumlah
   penagihan pada jendela 30 hari yang berakhir tepat di waktu masuk. Memakai
   funding yang benar-benar terjadi selama posisi dipegang akan menjadi
   lookahead paling telanjang yang mungkin ada di sistem ini — menolak entri
   karena mengetahui biaya yang belum terjadi.

   Jendela kosong (bursa tidak menerbitkan penagihan sama sekali) menghasilkan
   proyeksi nol, bukan penolakan. Ini konsisten dengan `lux/funding_model.py`:
   yang dijumlahkan adalah peristiwa, dan ketiadaan peristiwa berarti nol,
   bukan ketidaktahuan.

   Bila saringan dinyalakan tetapi jadwal funding tidak tersedia, entri
   **ditolak**. Menganggapnya berbiaya nol adalah bentuk kelalaian yang menyamar
   sebagai kelulusan.

## Nilai yang dipilih dan alasannya

| Parameter | Nilai | Alasan |
|---|---|---|
| `maks_umur_bar` | 168 (7 hari pada 1h) | Perdagangan terburuk H-001b dipegang 130 jam. 168 memotong ekor itu tanpa memotong mayoritas: pada H-001b hanya sebagian kecil perdagangan melewati seminggu. |
| `maks_carry_R` | 0,25 | Seperempat risiko adalah batas di mana funding masih dapat ditutup oleh target 2R. Di atas itu, winrate impas naik lebih cepat daripada yang dapat dikejar sinyal breakout. |
| `jendela_carry_hari` | 30 | Cukup panjang untuk memuat 90 penagihan pada kisi 8 jam dan 180 pada kisi 4 jam, cukup pendek untuk mengikuti perubahan rezim carry. |

Ketiganya ditulis di `config/lux.yaml`, bukan sebagai konstanta di kode, dan
ikut masuk ke dalam sidik hipotesis H-002 sehingga tidak dapat diubah diam-diam
setelah hasilnya terlihat.

## Konsekuensi

- `Konfig` bertambah tiga medan, semuanya **bawaan nol/mati**. Menjalankan
  ulang H-001b menghasilkan angka yang sama persis; ini dikunci oleh pengujian.
- `run_wf.py` (jalur H-001b) tidak disentuh sama sekali dan tidak membaca kunci
  baru di config. Orkestrator H-002 berdiri sebagai berkas terpisah,
  `lux/backtest/run_h002.py`.
- Perbandingan H-001b vs H-002 sah karena keduanya memakai dataset yang sama
  (`universe_layak_v2`, 438 simbol, 40 simbol pertama secara alfabet) dan
  ambang pra-registrasi yang sama. Satu-satunya perbedaan adalah dua saringan.
- Bila H-002 lulus `invarian_risiko` tetapi ekspektasinya tetap di bawah 0,05R,
  kesimpulannya adalah breakout Donchian memang tidak punya keunggulan pada
  dataset ini — bukan bahwa saringannya kurang ketat. Menaikkan ketat saringan
  sampai hasilnya lulus adalah pencarian yang tidak dihitung.
