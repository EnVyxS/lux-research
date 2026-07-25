# ADR-003 — Ekor datar simbol mati diperlakukan sebagai padding, bukan data pasar

Status: **diterima** · Tanggal: 2026-07-25 · Bukti: `reports/diag_datar.md`
(run `30170633590`), `reports/backtest_h001.md` (run pilot keempat)

**Keputusan ini ditulis dan dikomit sebelum kodenya ada.** Urutan itu bukan
formalitas. Bila aturan pemangkasan disusun setelah dampaknya pada ekspektasi R
terlihat, aturan itu akan disusun — tanpa niat buruk sekalipun — sedemikian rupa
sehingga dampaknya menyenangkan.

## Temuan

Pemindaian 447 simbol layak pada interval 1 jam:

| Ukuran | Nilai |
|---|---|
| Simbol dengan blok bar datar >= 24 bar | 69 |
| Blok terpanjangnya berharga persis satu nilai | 69 dari 69 |
| Blok terpanjangnya bervolume nol | 61 dari 69 |
| >= 90% bar datarnya berada dalam satu blok | 69 dari 69 |
| Blok terpanjang menempel di akhir riwayat | 62 |
| Blok terpanjang di tengah riwayat | 7 |
| Blok terpanjang menempel di awal riwayat | 0 |

Keenam puluh dua blok "akhir" itu semuanya berhenti pada tanggal yang sama,
2026-07-24, yaitu bar terakhir dataset. Contoh terparah: RENUSDT beku sejak
2024-12-03 sepanjang 14.366 bar; BLZUSDT 13.887 bar; FTMUSDT 13.550 bar.

Tidak adanya blok di awal riwayat menutup tafsiran "padding pra-listing".
Harga tunggal dan volume nol menutup tafsiran "pasar sangat tidak likuid".
Yang tersisa hanya satu: **harga terakhir simbol yang berhenti diperdagangkan
disalin berulang sampai ujung dataset.**

## Mengapa ini lebih berbahaya daripada gerbang yang gagal

1. **Gerbang survivorship diberi makan kebohongan.** Simbol mati dikenali dari
   stempel bar terakhirnya (`simbol_mati_dari_akhir`). Untuk 62 simbol ini bar
   terakhirnya sama dengan simbol yang masih hidup, sehingga mereka terhitung
   hidup. Ini kedua kalinya gerbang survivorship kehilangan kemampuannya untuk
   gagal; yang pertama ada di orkestrator, yang ini ada di datanya.
2. **Ambang kelayakan nyaris menangkapnya.** `maks_rasio_bar_datar = 0.30`,
   sementara rasio mereka berdesakan tepat di bawahnya: DFUSDT 0,2950,
   MYROUSDT 0,2899, RENUSDT 0,2836, HIFIUSDT 0,2826. Ambang yang dipasang untuk
   menangkap kelas cacat ini meleset karena disetel sedikit terlalu longgar.
3. **Bar palsu dapat diperdagangkan.** Stop pada bar datar tidak pernah
   tersentuh, sehingga kerugian tampak lebih kecil daripada semestinya, dan
   posisi dapat tertahan berbulan-bulan sambil terus dibebani funding.

## Keputusan

1. **Ekor datar dipangkas, bukan simbolnya dibuang.** Bila deret bar datar
   menempel di bar terakhir simbol, berharga satu nilai, dan panjangnya >= 24
   bar, seluruh deret itu dihapus. Riwayat sebelum blok tetap sah: simbol itu
   benar-benar diperdagangkan sampai tanggal tersebut, dan membuang seluruh
   riwayatnya justru menambah bias survivorship yang sedang diperbaiki.
2. **Bar terakhir setelah pemangkasan adalah tanggal kematian simbol.**
   Survivorship dinilai ulang atasnya. Inilah alasan utama pemangkasan ini ada.
3. **Volume nol tidak dijadikan syarat pemangkasan.** Delapan dari 69 blok
   memuat volume kecil bukan nol (OMGUSDT 5.536 pada 3 transaksi selama 12.951
   bar). Mensyaratkan volume nol akan melewatkannya, sementara satu harga
   selama ribuan bar sudah cukup membuktikan tidak ada pasar.
4. **Blok di tengah riwayat TIDAK dipangkas.** Tujuh simbol memilikinya
   (CTKUSDT, LITUSDT, TLMUSDT, TOMOUSDT, SXPUSDT, dan dua lainnya). Lubang di
   tengah tidak dapat dihapus tanpa menyambung dua periode yang tidak
   bersebelahan dan menciptakan lompatan harga palsu. Simbol dengan blok datar
   >= 24 bar di tengah riwayat **dikeluarkan dari universe layak**.
5. **Simbol yang riwayat tersisanya turun di bawah `min_bar = 8760`
   dikeluarkan dari universe layak**, mengikuti aturan kelayakan yang sudah ada.
   Tidak ada pengecualian bagi simbol yang kebetulan menguntungkan.
6. **`maks_rasio_bar_datar` diturunkan dari 0,30 menjadi 0,10** setelah
   pemangkasan dijalankan. Sesudah ekor palsu hilang, rasio 30% bar tanpa
   transaksi bukan lagi toleransi yang masuk akal.

## Yang sengaja tidak diputuskan di sini

Dampak keputusan ini terhadap hasil H-001 belum diketahui saat dokumen ini
ditulis, dan **tidak boleh** menjadi alasan meninjau ulang butir 1 sampai 6.
Bila jumlah simbol layak turun tajam, itu konsekuensi yang benar dari data yang
sebelumnya salah dihitung, bukan alasan melonggarkan aturan.

H-001 harus **dijalankan ulang dari awal** atas universe hasil pemangkasan.
Hasil run pilot pertama sampai keempat tidak dapat dibandingkan dengannya,
karena datanya berbeda. Kriteria pra-registrasi H-001 tetap tidak berubah:
ekspektasi >= 0,05R, minimal 100 perdagangan luar sampel, p entri acak <= 0,05,
rasio jendela positif >= 0,5.
