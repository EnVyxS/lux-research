# ADR-005 — H-003: pembalikan jangka pendek sebagai mekanisme berlawanan

**Status:** diterima · ditulis sebelum kodenya dijalankan
**Tanggal:** 2026-07-26
**Terkait:** ADR-004 (carry funding), H-001b DITOLAK, H-002 DITOLAK

## Konteks

Dua hipotesis pertama menguji mekanisme yang sama: penembusan Donchian, yaitu
bertaruh bahwa harga yang keluar dari rentangnya akan **melanjutkan** arah.
Keduanya ditolak. H-002 ditolak dengan sembilan gerbang lulus, ekspektasi
0,03159R terhadap ambang 0,05R (run `30174642490`).

Satu angka dari H-002 yang tidak boleh diabaikan: gerbang `entri_acak` lulus
dengan p 0,0099. Sinyal Donchian **secara statistik** mengalahkan entri acak.
Jadi yang gagal bukan "tidak ada apa-apa di sana", melainkan "yang ada di sana
terlalu kecil".

Ada dua tafsiran yang sama-sama masuk akal, dan keduanya tidak dapat dipisahkan
oleh data yang sudah ada:

1. Arah taruhannya salah. Penembusan pada perp kripto 1 jam sudah tergerus, dan
   yang tersisa justru pembalikan.
2. Kerangkanya yang membatasi. Stop 2×ATR dengan target 2R, biaya nyata, dan
   batas umur 168 bar menyisakan terlalu sedikit ruang bagi mekanisme apa pun.

## Keputusan

Mendaftarkan **H-003: pembalikan jangka pendek**, dengan kerangka eksekusi yang
**sama persis** dengan H-002.

Sinyalnya adalah skor-z penutupan terhadap rerata dan simpangan baku `jendela`
bar **sebelum** bar berjalan. Penutupan yang jatuh `ambang` simpangan baku di
bawah rerata dibeli; yang melonjak `ambang` di atas rerata dijual. Ini kebalikan
arah dari Donchian pada informasi yang secara kasar sama.

**Mengapa mekanisme ini, bukan yang lain.** Pembalikan jangka pendek punya bukti
publik yang berdiri sendiri, terdokumentasi lintas pasar dan secara khusus pada
kripto (antara lain Grobys & Junttila 2021 pada *Journal of International
Financial Markets, Institutions and Money*, dan ringkasan Quantpedia untuk pasar
berjangka). Alasan yang lebih penting: **hasilnya informatif ke dua arah.**

- Bila H-003 lulus, tafsiran 1 benar dan arah taruhan H-001b memang keliru.
- Bila H-003 gagal **dengan pola yang mirip** — keunggulan statistik ada tetapi
  besarnya di bawah ambang — maka yang tertuduh adalah kerangka stop/target dan
  biaya, bukan arah sinyal. Itu temuan yang jauh lebih berharga daripada satu
  strategi lagi yang gugur, dan ia mengarahkan pekerjaan berikutnya ke horizon
  dan struktur keluar, bukan ke pencarian sinyal baru.

Dua percobaan yang berlawanan arah pada kerangka identik memberi jawaban yang
tidak bisa diberikan oleh dua percobaan searah, berapa pun jumlahnya.

## Yang ditetapkan di muka

| Butir | Nilai | Alasan |
|---|---|---|
| Ruang parameter | `jendela` ∈ {24, 72, 168} | satu hari, tiga hari, satu minggu pada bar 1 jam; tiga kombinasi, sama sedikitnya dengan H-001b |
| `ambang` | 2,0 tetap | dipilih sebagai angka baku statistik, bukan hasil coba-coba; tidak dicari |
| Kerangka eksekusi | identik H-002 | stop 2×ATR, target 2R, umur maks 168 bar, carry maks 0,25R |
| Kriteria kelulusan | identik H-001b | 0,05R · 100 trade · p 0,05 · rasio jendela 0,5 |
| Dataset | identik | `universe_layak_v2` 438 simbol, 40 simbol pertama, 1h |

## Yang dilarang

Sama seperti ADR-004, dan perlu diulang karena godaannya bertambah setiap kali
sebuah hipotesis gugur:

- Ambang tidak diturunkan. 0,05R ditulis sebelum data dilihat dan tetap 0,05R.
- `ambang` z dan `jendela` tidak disetel ulang setelah hasil terlihat.
- H-001b dan H-002 tidak dihitung ulang.
- Bila H-003 gagal, tidak ada H-004 berupa varian keempat dari sinyal harga.
  Kegagalan kedua mekanisme yang berlawanan arah pada kerangka yang sama adalah
  bukti tentang **kerangkanya**, dan pekerjaan berikutnya harus menyerang itu:
  horizon, struktur keluar, atau sumber data yang belum dipakai sama sekali
  (funding sebagai sinyal, bukan hanya sebagai biaya).

## Catatan rancangan

`run_h003.py` adalah orkestrator ketiga yang berdiri sendiri. Polanya sekarang
mapan: satu hipotesis, satu orkestrator, dibekukan setelah dijalankan, seluruh
fungsi pemuatan dan penilaian diimpor dari `run_wf` sehingga semua hipotesis
dinilai kode yang sama. Bila orkestrator keempat dibutuhkan, ekstrak runner
bersama lebih dulu — tiga salinan adalah batas wajar, empat adalah utang.
