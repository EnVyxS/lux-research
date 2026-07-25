# LUX Research

Pipeline riset kuantitatif untuk sistem trading LUX. Ingest data, validasi, dan backtest dijalankan sepenuhnya di GitHub Actions.

## Cara memulai sesi baru

Baca **[`STATE.md`](STATE.md)** lebih dulu. Berkas itu adalah satu-satunya sumber kebenaran tentang posisi riset saat ini. Jangan membaca `journal/` secara utuh — arsip itu hanya untuk menelusuri alasan di balik keputusan lama.

## Struktur

| Path | Sifat | Kegunaan |
|---|---|---|
| `STATE.md` | ditulis ulang tiap sesi | pintu masuk tunggal, batas keras ~400 baris |
| `journal/YYYY-MM-DD-NN.md` | hanya ditambah | riwayat lengkap, tidak pernah diedit |
| `decisions/ADR-NNN.md` | beku setelah diterima | keputusan arsitektur, diganti ADR baru |
| `lux/` | kode | pustaka pipeline |
| `config/` | kode | parameter, dibekukan sebelum backtest |
| `.github/workflows/` | kode | seluruh komputasi berjalan di sini |

## Prinsip yang mengikat

Riset ini dijalankan di bawah aturan yang melarang penyesuaian metrik setelah hasil terlihat. Setiap eksperimen dipra-registrasi sebelum dijalankan, dan setiap hasil harus melewati gerbang mutu sebelum diterima. Hasil yang gagal gerbang tetap dicatat, tidak dihapus.
