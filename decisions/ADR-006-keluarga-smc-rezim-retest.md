# ADR-006 — H-004, H-005, H-006: rezim ADX, entri retest, sapuan likuiditas

**Status:** diterima · ditulis sebelum kodenya dijalankan
**Tanggal:** 2026-07-26
**Terkait:** ADR-004, ADR-005, H-001b/H-002/H-003 semuanya DITOLAK

## Konteks

Pengguna mengusulkan empat hal: SMC, sniper entry, trend breakout, dan ADX 30.
Keempatnya harus dipilah lebih dulu, karena tidak semuanya ide yang berbeda.

| Usulan | Status jujur |
|---|---|
| **Trend breakout** | **Sudah diuji dua kali.** Itu persis H-001b dan H-002: Donchian 20/55/100 pada 1h. Ekspektasi 0,032R, di bawah ambang 0,05R. Menjalankannya lagi bukan percobaan, melainkan pengulangan. |
| **ADX 30** | **Baru, tetapi bukan mekanisme** — ini saringan rezim di atas breakout yang sama. Sah diuji karena 30 adalah angka konvensional yang ditetapkan di muka, bukan hasil coba-coba. |
| **Sniper entry** | Bukan istilah teknis. Dapat dijadikan mekanisme bila diterjemahkan: **masuk pada retest**, bukan pada bar penembusan. |
| **SMC** | Sebagian besar tidak punya definisi formal dan tidak punya bukti publik yang kredibel. Bagian yang **dapat dikodekan tanpa penafsiran** adalah sapuan likuiditas: sumbu menembus ekstrem sebelumnya lalu penutupan kembali ke dalam. |

Satu peringatan yang harus dicatat sebelum hasil ada: **H-003 sudah membuktikan
pembalikan jangka pendek rugi telak (−0,2478R, p entri acak 1,0)**. Sapuan
likuiditas adalah pembalikan di level tertentu. Prior-nya buruk. Itu bukan alasan
untuk tidak mengujinya — justru sebaliknya, karena satu-satunya cara mengakhiri
perdebatan tentang SMC adalah mengukurnya dengan gerbang yang sama.

## Keputusan

Mendaftarkan tiga hipotesis sekaligus, dengan kerangka eksekusi identik H-002.

| ID | Mekanisme | Ruang parameter | Menjawab |
|---|---|---|---|
| **H-004** | Breakout Donchian yang hanya aktif saat ADX(14) ≥ 30 | `lookback` ∈ {20, 55, 100}, `adx_min` 30 tetap | "trendbreak out, adx 30" |
| **H-005** | Penembusan Donchian 55, entri hanya bila harga kembali menyentuh level yang ditembus lalu menutup di sisi penembusan | `jendela_retest` ∈ {6, 12, 24} bar | "sniper entry" |
| **H-006** | Sapuan likuiditas: sumbu menembus ekstrem `N` bar sebelumnya, penutupan kembali ke dalam, masuk berlawanan arah sapuan | `N` ∈ {20, 50, 100} | "SMC" |

Masing-masing tiga kombinasi. Semua sinyal kausal secara struktural.

## Koreksi multiplisitas — ditetapkan sebelum hasil terlihat

Menguji tiga hipotesis sekaligus melipatgandakan peluang salah satu terlihat
bagus secara kebetulan. Dengan ambang p 0,05 dan tiga percobaan, peluang minimal
satu positif palsu naik ke sekitar 14%.

Karena itu `maks_p_entri_acak` diperketat menjadi **0,0167 (0,05 / 3)** untuk
ketiganya, ditulis di sini sebelum satu angka pun ada. Ambang lain tidak berubah:
ekspektasi 0,05R, minimal 100 perdagangan luar sampel, rasio jendela positif 0,5.

Gerbang `entri_acak` di `gerbang.py` tetap memakai 0,05; yang mengikat adalah
kriteria pra-registrasi yang lebih ketat. Sebuah hipotesis bisa meluluskan
gerbang tetapi tetap ditolak pra-registrasi, dan itu memang perilaku yang
diinginkan.

## Yang dilarang

- **Memilih pemenang setelah melihat hasil.** Bila satu dari tiga lulus dan dua
  gagal, yang lulus **tetap harus dianggap terdampak multiplisitas** dan wajib
  dikonfirmasi ulang pada 438 simbol penuh sebelum dipercaya. Ketiganya sudah
  didaftarkan, jadi tidak ada percobaan tersembunyi.
- Menyetel ulang `adx_min`, `jendela_retest`, atau `N` setelah hasil terlihat.
- Menjalankan ulang H-001b, H-002, atau H-003.
- Menambahkan definisi SMC lain (order block, fair value gap, BOS/CHoCH) setelah
  H-006 gagal. Bila sapuan likuiditas gagal telak seperti H-003, pertanyaannya
  bukan "definisi SMC mana yang benar", melainkan apakah keluarga mekanisme
  pembalikan-di-level punya tanda positif sama sekali pada dataset ini.

## Utang teknis yang dibayar lebih dulu

ADR-005 mensyaratkan **ekstraksi runner bersama sebelum orkestrator keempat**.
Syarat itu dipenuhi di commit yang sama: `lux/backtest/runner.py` memuat seluruh
badan generik (muat data sekali, jalankan walk-forward, susun sembilan gerbang,
tulis laporan), dan `run_keluarga.py` hanya mendaftarkan tiga spesifikasi.

`run_wf.py`, `run_h002.py`, dan `run_h003.py` **tidak disentuh**, sehingga ketiga
hasil lama tetap dapat diulang bita demi bita. Runner bersama mengimpor fungsi
penilaian dari `run_wf`, jadi keenam hipotesis dinilai oleh kode yang sama.

Data dimuat **satu kali** untuk ketiga hipotesis. Itu bukan sekadar penghematan
waktu: ia menjamin ketiganya melihat kumpulan berkas yang identik, sehingga
gerbang `checksum` cukup dinilai sekali dan perbandingannya sah.
