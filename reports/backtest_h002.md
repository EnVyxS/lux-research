# Backtest H-002 — batas umur posisi dan saringan carry (ADR-004)

> Penembusan Donchian pada penutupan bar 1 jam menghasilkan ekspektasi positif setelah fee, slippage, dan funding nyata, bila posisi dibatasi umurnya dan entri dengan carry funding terproyeksi berlebihan ditolak, pada perp USDT yang lolos ambang kelayakan, dinilai hanya di luar sampel.

Sidik hipotesis `16fb57692a6f0888` · ruang 3 kombinasi · 40 simbol · 32.6s

Saringan: umur maksimum **168 bar**, carry terproyeksi maksimum **0.25R** atas jendela 30 hari.

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- ekspektasi 0.0316R < 0.05R

## Hasil luar sampel

- Perdagangan: **18,883**
- Total R: **596.44**
- Ekspektasi: **0.03158622537199252**
- Jendela positif: 212/356
- Alasan keluar: {'target': 6707, 'stop': 11909, 'akhir_data': 164, 'umur': 103}

## Perbandingan dengan H-001b

Dataset, ambang, dan seluruh kode penilaian identik. Satu-satunya perbedaan adalah kedua saringan.

| Besaran | H-001b | H-002 |
|---|---|---|
| Ekspektasi R | 0.030857864162317453 | 0.03158622537199252 |
| Total R | 589.1692004511272 | 596.44 |
| Trade luar sampel | 19093 | 18883 |
| Kerugian terburuk (R) | None | -1.3215361406058381 |
| Putusan pra-registrasi | False | False |

## Sembilan gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | lulus | 0.0003 | 0.3 | 0 dari 40 simbol gagal |
| buy_and_hold | lulus | 0.8148 | 0.0 | median selisih 0.8148; unggul di 35/40 simbol |
| entri_acak | lulus | 0.0099 | 0.05 | 0 dari 100 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | lulus | -1.3215 | -1.5 | kerugian terburuk -1.322R dari 18883 perdagangan |
| funding | lulus | 9582.3826 | 0.0 | total funding mutlak 9582.382645 atas 18883 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 40 simbol gagal |
| checksum | lulus | 0.0000 | 0.0 | hilang 0, asing 0, tidak cocok 0 |
| survivorship | lulus | 0.8555 | 0.5 | porsi delisted diuji 0.1250 vs universe 0.1461 |

## Pembongkaran biaya

- Rerata biaya transaksi: **0.0345R**
- Rerata biaya funding: **0.0005R**
- Rerata jarak stop terhadap harga: **3.561%**
- Perdagangan dengan biaya melebihi 1R: **0** dari 18,883

| Simbol | R | Kotor R | Transaksi R | Funding R | Stop % harga | Jam | Alasan |
|---|---|---|---|---|---|---|---|
| 1000XECUSDT | -1.322 | -1.016 | 0.032 | 0.273 | 3.146 | 41.0 | stop |
| ACTUSDT | -1.295 | -1.011 | 0.022 | 0.262 | 4.666 | 16.0 | stop |
| 1000WHYUSDT | -1.293 | -1.006 | 0.012 | 0.276 | 7.929 | 41.0 | stop |
| ADAUSDT | -1.270 | -1.020 | 0.040 | 0.210 | 2.460 | 94.0 | stop |
| 1000FLOKIUSDT | -1.270 | -1.022 | 0.043 | 0.205 | 2.350 | 94.0 | stop |
| 1000WHYUSDT | -1.236 | -1.019 | 0.038 | 0.179 | 2.572 | 50.0 | stop |
| 1000SHIBUSDT | -1.236 | -1.032 | 0.064 | 0.141 | 1.561 | 49.0 | stop |
| AGTUSDT | -1.231 | -1.009 | 0.018 | 0.204 | 5.296 | 97.0 | stop |
| 1000XECUSDT | -1.228 | -1.010 | 0.019 | 0.200 | 5.419 | 41.0 | stop |
| 1000WHYUSDT | -1.205 | -1.015 | 0.030 | 0.161 | 3.328 | 91.0 | stop |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| ALGOUSDT | 53,511 | 22 | 1205 | 85.72 | 0.07113 |
| ADAUSDT | 56,800 | 24 | 1282 | 66.47 | 0.05185 |
| ALPHAUSDT | 42,363 | 17 | 879 | 58.67 | 0.06675 |
| 1000CHEEMSUSDT | 14,557 | 4 | 253 | 53.07 | 0.20978 |
| 1000PEPEUSDT | 28,232 | 10 | 426 | 53.05 | 0.12453 |
| AIOTUSDT | 10,812 | 2 | 98 | 52.98 | 0.54064 |
| 1000BONKUSDT | 23,410 | 8 | 338 | 51.27 | 0.15169 |
| AIUSDT | 20,183 | 7 | 301 | 42.20 | 0.14019 |
| 1000CATUSDT | 15,396 | 5 | 263 | 41.05 | 0.15609 |
| 1000FLOKIUSDT | 28,208 | 10 | 510 | 36.03 | 0.07065 |

## Sepuluh simbol dengan total R terendah

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| ANTUSDT | 19,829 | 7 | 373 | -42.24 | -0.11325 |
| AIXBTUSDT | 13,950 | 4 | 248 | -25.39 | -0.10239 |
| ANIMEUSDT | 13,135 | 4 | 168 | -23.08 | -0.1374 |
| ANKRUSDT | 48,137 | 20 | 1077 | -22.71 | -0.02108 |
| ACHUSDT | 29,962 | 11 | 608 | -21.54 | -0.03543 |
| ACXUSDT | 14,289 | 4 | 162 | -17.59 | -0.10861 |
| ALPINEUSDT | 10,671 | 2 | 102 | -10.30 | -0.10096 |
| 1INCHUSDT | 48,902 | 20 | 1277 | -7.25 | -0.00568 |
| AGLDUSDT | 26,206 | 10 | 505 | -7.24 | -0.01433 |
| AGTUSDT | 10,334 | 2 | 102 | -6.67 | -0.06537 |
