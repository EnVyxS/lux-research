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

## Posisi riset: dua hipotesis selesai, keduanya DITOLAK

**H-001b** (run `30172926477`): ekspektasi 0,0309R < 0,05R, gerbang
`invarian_risiko` GAGAL pada −2,5853R. Penyebabnya carry funding, bukan fee:
perdagangan terburuk memuat `funding_R` 1,545 atas posisi 130 jam.

**H-002** (run `30174642490`, ADR-004, saringan umur 168 bar + carry 0,25R):
**sembilan gerbang lulus**, `invarian_risiko` pulih ke −1,3215R, tetapi
ekspektasi 0,03159R tetap di bawah 0,05R. 18.883 perdagangan, 596,44R, 212/356
jendela positif.

Tafsiran yang sudah dikunci ADR-004 **sebelum** angkanya terlihat: breakout
Donchian 1 jam tidak punya keunggulan yang memadai pada dataset ini. Gerbang
`entri_acak` lulus dengan p 0,0099, jadi sinyalnya memang mengalahkan entri
acak — besarnya saja yang terlalu kecil setelah biaya nyata.

**Yang DILARANG:** menyetel ulang `maks_umur_bar` atau `maks_carry_R` untuk
mengejar 0,05R, menurunkan ambang, atau menjalankan ulang H-001b/H-002.

## PEKERJAAN BERIKUTNYA (urutan wajib)

1. **H-003 — keluarga strategi baru.** Mekanisme berbeda dari breakout Donchian
   (misalnya pembalikan rerata, atau breakout dengan saringan rezim), ruang
   parameter kecil, didaftarkan lewat `lux/praregistrasi.py` sebelum dijalankan,
   dengan orkestrator sendiri seperti `run_h002.py` agar hasil lama tetap dapat
   diulang.
2. Perketat `gerbang_lulus` di `lux/funding.py` (celah dan jitter ikut menilai).
3. Validasi interval 4h lewat `validate.yml`.
4. Diff terhadap Dataset G lama (528 simbol) sebagai uji silang survivorship.
5. `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md`, salin ADR-001 dan ADR-002.
6. Pelapor Notion (`NOTION_TOKEN`) untuk LUX Gatekeeper.
7. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, ≥24 shard.

## Peta orkestrator

- `lux/backtest/run_wf.py` — H-001b. **Jangan disunting.** Menyuntingnya membuat
  angka H-001b tidak lagi dapat diulang.
- `lux/backtest/run_h002.py` — H-002. Mengimpor seluruh fungsi pemuatan dan
  penilaian dari `run_wf`, jadi perbandingan antar hipotesis tetap sah.
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
- Ambang pra-registrasi **tidak boleh** diubah setelah melihat hasil, dan
  hipotesis yang ditolak tidak dihitung ulang.

## Angka yang DILARANG dikutip

Seluruh hasil ingest putaran 1 (14.076.257 baris 1h, 17.169 celah, rasio 4,014),
metrik celah funding putaran 1–4 (1.380.741 · 1.193.209 · 587.131 · 266.612),
dan seluruh run pilot H-001 termasuk `30170073890`.
