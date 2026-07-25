# Prompt kelanjutan riset LUX

Kalimat pembuka sesi baru: **"Baca `STATE.md` dan `PROMPT_KELANJUTAN.md` di repo
`EnVyxS/lux-research`, lalu lanjutkan."**

## Konteks singkat

Membangun sistem trading kuantitatif dari nol dengan disiplin pra-registrasi.
Seluruh komputasi berjalan di GitHub Actions (repo publik, menit tak terbatas);
sandbox agen tidak punya jaringan. Data mentah dari `data.binance.vision`
(prefix `data/` wajib), disimpan sebagai Parquet di GitHub Release `tier-b-v1`.

Tidak ada tool MCP untuk membaca log atau status run. Karena itu setiap workflow
mengomit lognya sendiri kembali ke `reports/` dengan `if: always()`. Cara memicu
run dari MCP hanya satu: menyunting berkas workflow itu sendiri.

## Keadaan data

| Aset | Nilai |
|---|---|
| OHLCV 1h | 14.545.679 baris, 790 simbol |
| OHLCV 4h | 3.636.733 baris (validasi 4h BELUM dijalankan) |
| Funding | 1.982.017 baris, 447 simbol |
| Universe layak lama | 447 |
| **Universe layak v2 (ADR-003)** | **438** — `reports/universe_layak_v2.json` |

## Temuan terbesar sampai kini: ekor datar simbol mati

Diagnostik `lux/diag_datar.py` (run `30170633590`) membuktikan 62 dari 447
simbol layak berakhir dengan blok bar datar **berharga tunggal** yang membentang
sampai bar terakhir dataset (2026-07-24). RENUSDT beku sejak 2024-12-03
sepanjang 14.366 bar. 69 dari 69 blok berharga satu nilai; 61 bervolume nol;
0 berada di awal riwayat. Tafsiran padding pra-listing dan pasar tidak likuid
keduanya tertutup: **harga terakhir simbol mati disalin sampai ujung dataset.**

Akibat terpenting bukan bar palsu yang dapat diperdagangkan, melainkan bahwa
**gerbang survivorship kehilangan kemampuannya untuk gagal**, karena simbol mati
dikenali dari stempel bar terakhirnya dan stempel itu palsu.

Pemangkasan (`lux/potong_ekor.py`, run `30170823380`) atas seluruh 790 simbol:

| Ukuran | Nilai |
|---|---|
| Simbol berekor datar | **141 dari 790** (bukan 29 seperti dugaan lama) |
| Total bar dipangkas | **1.081.920** (7,4% dari seluruh bar 1h) |
| Kandidat layak 447 -> | **438 layak, 9 ditolak** |
| Rasio bar datar sesudah pangkas | hampir seluruhnya **0,0000** |

Rasio sisa yang jatuh ke nol adalah konfirmasi terkuat: bar datar itu memang
**hanya** ada di ekor, tidak tersebar di riwayat nyata.

Sembilan yang ditolak: tujuh karena blok datar di tengah riwayat (tidak dapat
dipangkas tanpa menyambung dua periode terpisah — 9447, 7815, 6351, 2390, 1982,
639, 470 bar) dan dua karena riwayat tersisa di bawah 8.760 bar (7.394 dan
8.425).

## PEKERJAAN BERIKUTNYA (urutan wajib)

1. **Sambungkan hasil ADR-003 ke orkestrator `lux/backtest/run_wf.py`:**
   - `muat_ohlcv` memanggil `lux.potong_ekor.potong` per simbol saat muat
   - `akhir_per_simbol` membaca `reports/akhir_sejati.json`, bukan stempel bar
     terakhir mentah (inilah inti perbaikan survivorship)
   - CLI `--universe` diarahkan ke `reports/universe_layak_v2.json`
   - Tambah uji yang membuktikan simbol berekor palsu kini terhitung mati
2. **Jalankan ulang H-001 dari awal** atas universe v2. Hasil run pilot pertama
   sampai keempat **tidak dapat dibandingkan** dengannya karena datanya berbeda.
3. **Tindak lanjut `invarian_risiko`** — penyebabnya **funding, bukan fee**
   (terburuk −2,585R: `transaksi_R` 0,026 vs `funding_R` 1,545 pada posisi 130
   jam). Opsi sah = saringan kelayakan perdagangan yang didaftarkan sebagai
   **H-002** (batas umur posisi, atau batas funding terproyeksi terhadap R, atau
   menolak simbol bercarry ekstrem seperti AERGOUSDT −102,6%/tahun).
   **Bukan** pelonggaran ambang gerbang, **bukan** penyuntingan kriteria H-001.
4. **Gerbang `checksum`** perlu satu run lagi agar benar-benar membandingkan.
5. `config/lux.yaml`: ganti `funding_interval_jam: 8` jadi rujukan jadwal per
   simbol; sesuaikan docstring `lux/costs.py`.
6. Perketat `gerbang_lulus` di `lux/funding.py` (celah dan jitter ikut menilai).
7. Validasi interval 4h (baru 1h yang dijalankan).
8. STATE v7; salin ADR-001 & ADR-002 ke `decisions/`; `Makefile`;
   `docs/PIPELINE.md`; `lux/manifest.py`; pelapor Notion (`NOTION_TOKEN`).
9. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus — perkiraan >=24 shard.

## Hasil H-001 terakhir (run pilot keempat, `30170073890`) — SUDAH USANG

**DITOLAK**: ekspektasi 0,0317R < 0,05R. 19.060 perdagangan, 604,26R, 208/359
jendela positif. Gerbang gagal: `forward_fill`, `invarian_risiko`, `checksum`.
Angka ini dihitung atas data yang memuat ekor palsu, jadi **tidak boleh dikutip
lagi** setelah ADR-003 disambungkan.

## Aturan kerja yang sudah dibayar mahal

- **Gerbang pra-terbang `pytest` sebelum langkah unduh.** Sudah sepuluh kali
  menghentikan run dalam hitungan detik alih-alih membakar unduhan ratusan MB.
- **Workflow yang memicu dirinya sendiri harus didorong SESUDAH seluruh modul
  yang dipanggilnya.**
- **Hijau bukan berarti berhasil.** Selalu baca laporan yang dikomit balik.
- **Sha berkas basi segera setelah `push_files` menyentuhnya.**
- **Penjelasan yang membuat anomali terasa wajar harus dicurigai lebih keras
  daripada anomalinya sendiri.** Aturan inilah yang menolak menerima deret
  7.310 bar sebagai "pasar sepi" dan berujung pada ADR-003.
- **Durasi run tidak boleh dipakai sebagai bukti diagnosis** — perkiraan sudah
  meleset berkali-kali di kedua arah.
- **Keputusan metodologis ditulis dan dikomit sebelum kodenya ada** (ADR-003
  adalah contohnya), supaya aturan tidak terbentuk mengikuti hasil.
- Ambang pra-registrasi **tidak boleh** diubah setelah melihat hasil.

## Angka yang DILARANG dikutip

Seluruh hasil ingest putaran 1 (14.076.257 baris 1h, 17.169 celah, rasio 4,014)
dan metrik celah funding putaran 1–4 (1.380.741 · 1.193.209 · 587.131 ·
266.612). Angka sah: **14.545.679 baris, 112 celah, rasio 3,9996**; funding
**3 celah sejati, jitter maks 47 ms**.
