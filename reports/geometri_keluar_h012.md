# Geometri keluar H-012 (ADR-015 Bagian A)

Dihitung dari laporan yang **sudah dikomit**, bukan dari run baru. Tidak ada mesin yang dijalankan dan tidak ada angka baru yang diproduksi bagi hipotesis yang sudah divonis DITOLAK.

Ambang gerbang `invarian_risiko`: **-1.5R**, tidak bergerak.

## Batas bukti

Laporan hanya menyimpan **sepuluh** perdagangan terburuk, jadi tidak semua pertanyaan dapat dijawab darinya. Pertanyaan tentang perdagangan di bawah ambang dapat dijawab dengan pasti hanya bila perdagangan paling ringan di dalam ekor sudah berada di atas ambang, sebab dengan begitu mustahil ada pelanggar di luar ekor.

- Ekor memuat semua pelanggar: **ya**
- Perdagangan di bawah ambang: **1**

## 10 perdagangan terburuk

| Simbol | R | Alasan | Transaksi R | Funding R | R terlampaui | Celah R | Stop % harga | Jam |
|---|---|---|---|---|---|---|---|---|
| STGUSDT | -21.3131 | carry | 0.0559 | 0.4825 | 20.3131 | +19.7747 | 2.197 | 1.0 |
| TRXUSDT | -1.4966 | stop | 0.2123 | 0.1779 | 0.4966 | +0.1064 | 0.472 | 50.0 |
| TRXUSDT | -1.4246 | stop | 0.1979 | 0.1280 | 0.4246 | +0.0987 | 0.504 | 81.0 |
| TRXUSDT | -1.4176 | stop | 0.1751 | 0.1547 | 0.4176 | +0.0878 | 0.573 | 60.0 |
| BTCDOMUSDT | -1.4159 | stop | 0.1588 | 0.1774 | 0.4159 | +0.0796 | 0.632 | 109.0 |
| SUNUSDT | -1.4103 | stop | 0.1142 | 0.2387 | 0.4103 | +0.0573 | 0.880 | 59.0 |
| TRXUSDT | -1.4068 | stop | 0.1505 | 0.1813 | 0.4068 | +0.0750 | 0.662 | 96.0 |
| SUNUSDT | -1.4061 | stop | 0.1729 | 0.1466 | 0.4061 | +0.0867 | 0.580 | 50.0 |
| PAXGUSDT | -1.3870 | stop | 0.1778 | 0.1206 | 0.3870 | +0.0887 | 0.561 | 102.0 |
| BTCDOMUSDT | -1.3865 | stop | 0.2274 | 0.0456 | 0.3865 | +0.1135 | 0.439 | 11.0 |

## Median R terlampaui menurut alasan keluar

| Alasan | Median R terlampaui |
|---|---|
| carry | 20.313091 |
| stop | 0.410263 |

## Adjudikasi ramalan Bagian A

| Ramalan | Hasil | Bukti |
|---|---|---|
| 1 | **BENAR** | perdagangan terburuk -21.3131R pada STGUSDT beralasan keluar 'carry', bukan 'stop' |
| 2 | **BENAR** | tidak ada keluar 'stop' di bawah -1.5R, dan ekor terbukti memuat semua pelanggar |
| 3 | **SALAH** | porsi bukan-stop di 10 terburuk = 0.1000 (1 dari 10) |
| 4 | **TIDAK DAPAT DINILAI** | tidak ada keluar 'umur' di dalam ekor |
