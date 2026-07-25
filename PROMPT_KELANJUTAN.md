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
| OHLCV 1h | 14.545.679 baris, 790 simbol, 112 celah, rasio 3,9996 |
| OHLCV 4h | 3.636.733 baris (validasi 4h BELUM dijalankan) |
| Funding | 1.982.017 baris, 447 simbol, 3 celah sejati, jitter maks 47 ms |
| **Universe layak v2 (ADR-003)** | **438** — `reports/universe_layak_v2.json` |

## Posisi riset: tiga hipotesis selesai, ketiganya DITOLAK

| | H-001b | H-002 | H-003 |
|---|---|---|---|
| Run | `30172926477` | `30174642490` | `30175179866` |
| Mekanisme | Donchian | Donchian + saringan carry (ADR-004) | pembalikan skor-z (ADR-005) |
| Ekspektasi R | 0,03086 | **0,03159** | **−0,24782** |
| Perdagangan | 19.093 | 18.883 | 28.959 |
| Jendela positif | 208/356 | 212/356 | 25/356 |
| Gerbang gagal | `invarian_risiko` −2,5853 | — (sembilan lulus) | `buy_and_hold`, `entri_acak` p 1,0, `invarian_risiko` −1,8637 |

Dataset, kriteria, limit 40 simbol, dan kode penilaian identik pada ketiganya.

**Temuan terpenting sampai hari ini bukan salah satu putusan, melainkan jarak di
antara keduanya.** Pada kerangka eksekusi yang identik, kelanjutan memberi
+0,0316R dan pembalikan memberi −0,2478R. Rentang 0,28R itu membuktikan kerangka
stop 2×ATR / target 2R **meneruskan** informasi arah, jadi ia bukan penyebab
kegagalan. Keunggulan tipis Donchian nyata (p entri acak 0,0099), hanya terlalu
kecil untuk menutup biaya transaksi rerata 0,0345R per perdagangan.

**Cacat yang ditemukan H-003:** saringan carry ADR-004 bisa tembus.
`carry_terproyeksi_R` adalah proyeksi rerata 30 hari, bukan jaminan; AKTUSDT
membayar `funding_R` 0,833 atas 77 jam dengan stop 5,064% dari harga. Gerbang
yang lulus pada satu hipotesis belum tentu tidak bisa gagal pada hipotesis lain.

**Yang DILARANG:** menyetel ulang saringan atau ambang untuk mengejar 0,05R;
menjalankan ulang H-001b, H-002, atau H-003; membalik tanda H-003 dan
menjalankannya sebagai "perbaikan" alih-alih sebagai hipotesis baru berlabel ID
baru dengan ADR-nya sendiri; mendaftarkan hipotesis sinyal harga keempat sebagai
reaksi langsung atas kegagalan H-003 (ADR-005).

## PEKERJAAN BERIKUTNYA (urutan wajib)

1. **Pilih satu dari dua arah, tulis ADR-006 lebih dulu, baru kodenya.**
   - **Horizon.** Biaya 0,0345R hampir menelan keunggulan 0,032R. Bar 4h membagi
     biaya yang sama ke pergerakan lebih besar. **Prasyarat mutlak: validasi 4h
     lewat `validate.yml`,** yang belum pernah dijalankan.
   - **Funding sebagai sinyal.** Selama ini hanya diperlakukan sebagai biaya.
     79,1% penagihan positif dan carry ekstrem sampai −533,9%/tahun adalah
     struktur yang belum pernah diuji kandungan informasi arahnya.
2. Perketat `gerbang_lulus` di `lux/funding.py` (celah dan jitter ikut menilai).
3. Perbaiki docstring `lux/costs.py` yang masih menyebut pembagi funding 8 jam.
4. Diff terhadap Dataset G lama (528 simbol) sebagai uji silang survivorship.
5. `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md`, salin ADR-001 dan ADR-002.
6. Pelapor Notion (`NOTION_TOKEN`) untuk LUX Gatekeeper.
7. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, ≥24 shard.

## Peta orkestrator

- `lux/backtest/run_wf.py` — H-001b. **Jangan disunting.**
- `lux/backtest/run_h002.py` — H-002. Dibekukan.
- `lux/backtest/run_h003.py` — H-003. Dibekukan.
- Semuanya mengimpor fungsi pemuatan dan penilaian dari `run_wf`, sehingga ketiga
  hipotesis dinilai kode yang sama. **Tiga salinan adalah batas wajar;
  orkestrator keempat harus didahului ekstraksi runner bersama.**
- `.github/workflows/backtest.yml` — satu-satunya pemicu. Menyunting berkas ini
  menjalankan backtest. `--limit 40` wajib tetap agar hasil dapat dibandingkan.

## Workflow aktif (10)

`tests`, `backtest`, `validate`, `potong_ekor`, `ingest_tier_b`,
`backfill_daily`, `funding`, `funding_check`, `universe`, `doctor`.

Dihapus di S7: `analyze_tail.yml`, `diagnose.yml`, `diag_datar.yml` — masukannya
artifact yang kedaluwarsa 90 hari sementara keluarannya sudah permanen di
`reports/`. Modul Python-nya tetap ada.

## Aturan kerja yang sudah dibayar mahal

- **Gerbang pra-terbang `pytest` sebelum langkah unduh.**
- **Workflow yang memicu dirinya sendiri harus didorong SESUDAH seluruh modul
  yang dipanggilnya.**
- **Hijau bukan berarti berhasil.** Selalu baca laporan yang dikomit balik.
- **Sha berkas basi segera setelah `push_files` menyentuhnya.**
- **Penjelasan yang membuat anomali terasa wajar harus dicurigai lebih keras
  daripada anomalinya sendiri.**
- **Durasi run tidak boleh dipakai sebagai bukti diagnosis.**
- **Keputusan metodologis ditulis dan dikomit sebelum kodenya ada.**
- **Rancang percobaan yang informatif ke dua arah.** H-003 gagal telak dan justru
  karena itu ia menjawab pertanyaan yang tidak terjawab oleh keberhasilan.
- Ambang pra-registrasi **tidak boleh** diubah setelah melihat hasil, dan
  hipotesis yang ditolak tidak dihitung ulang.

## Angka yang DILARANG dikutip

Seluruh hasil ingest putaran 1 (14.076.257 baris 1h, 17.169 celah, rasio 4,014),
metrik celah funding putaran 1–4 (1.380.741 · 1.193.209 · 587.131 · 266.612),
dan seluruh run pilot H-001 termasuk `30170073890`.
