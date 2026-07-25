# Backtest H-001 — breakout Donchian 1 jam

> Penembusan Donchian pada penutupan bar 1 jam menghasilkan ekspektasi positif setelah fee, slippage, dan funding nyata, pada perp USDT yang lolos ambang kelayakan, dinilai hanya di luar sampel.

Sidik hipotesis `f172b1ba07f25717` · ruang 3 kombinasi · 40 simbol · 30.3s

## Putusan

**DITOLAK**

Kriteria pra-registrasi yang tidak terpenuhi:

- ekspektasi 0.0349R < 0.05R

Gerbang gagal: forward_fill, invarian_risiko, checksum

## Hasil luar sampel

- Perdagangan: **18,524**
- Total R: **647.11**
- Ekspektasi: **0.03493361462253073**
- Jendela positif: 204/349

## Sembilan gerbang

| Gerbang | Putusan | Nilai | Ambang | Catatan |
|---|---|---|---|---|
| forward_fill | GAGAL | 0.1813 | 0.3 | 4 dari 40 simbol gagal |
| buy_and_hold | lulus | 0.8007 | 0.0 | median selisih 0.8007; unggul di 36/40 simbol |
| entri_acak | lulus | 0.0099 | 0.05 | 0 dari 100 permutasi menyamai atau melampaui |
| lookahead | lulus | 0.0000 | 0.0 | 0 sinyal berubah saat data masa depan dihapus |
| invarian_risiko | GAGAL | -2.5853 | -1.5 | kerugian terburuk -2.585R dari 18524 perdagangan |
| funding | lulus | 10995.5246 | 0.0 | total funding mutlak 10995.524564 atas 18524 trade |
| overlap | lulus | 0.0000 | 0.0 | 0 dari 40 simbol gagal |
| checksum | GAGAL | — | — | tidak dapat dinilai: manifest baru ditulis pada run ini; run berikutnya akan membandingkannya |
| survivorship | lulus | 0.7982 | 0.5 | porsi delisted diuji 0.0250 vs universe 0.0313 |

## Sepuluh simbol dengan total R tertinggi

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| ALGOUSDT | 52,935 | 22 | 1215 | 66.48 | 0.05471 |
| 1000PEPEUSDT | 27,656 | 10 | 502 | 59.74 | 0.11901 |
| ADAUSDT | 56,224 | 23 | 1246 | 59.34 | 0.04763 |
| 1000BONKUSDT | 22,834 | 8 | 335 | 54.54 | 0.1628 |
| 1000CHEEMSUSDT | 13,981 | 4 | 253 | 51.73 | 0.20446 |
| AIOTUSDT | 10,236 | 2 | 78 | 49.48 | 0.63442 |
| 1000CATUSDT | 14,820 | 4 | 216 | 48.84 | 0.2261 |
| ALPHAUSDT | 49,097 | 20 | 919 | 47.82 | 0.05203 |
| AAVEUSDT | 50,009 | 21 | 1041 | 45.12 | 0.04334 |
| AIUSDT | 21,708 | 7 | 299 | 42.28 | 0.14142 |

## Sepuluh simbol dengan total R terendah

| Simbol | Bar | Jendela | Trade | Total R | Ekspektasi R |
|---|---|---|---|---|---|
| AIXBTUSDT | 13,374 | 4 | 249 | -26.46 | -0.10626 |
| AERGOUSDT | 15,793 | 5 | 274 | -24.28 | -0.08863 |
| ANIMEUSDT | 12,559 | 3 | 187 | -23.27 | -0.12443 |
| AGTUSDT | 9,758 | 2 | 115 | -14.07 | -0.12231 |
| AGLDUSDT | 25,630 | 9 | 470 | -13.00 | -0.02765 |
| ALPINEUSDT | 10,095 | 2 | 102 | -10.30 | -0.10096 |
| 1000XECUSDT | 41,949 | 17 | 983 | -9.35 | -0.00951 |
| AINUSDT | 8,534 | 1 | 50 | -8.45 | -0.16899 |
| ACHUSDT | 29,386 | 11 | 658 | -8.27 | -0.01257 |
| AKROUSDT | 11,835 | 3 | 186 | -6.48 | -0.03483 |
