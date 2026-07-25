# Keluarga ADR-006 — H-004, H-005, H-006

Tiga hipotesis dijalankan serentak pada kerangka eksekusi identik H-002. Ambang `p entri acak` diperketat ke **0.0167** (Bonferroni 0,05/3) sebelum hasil terlihat.

| Hipotesis | Mekanisme | Ekspektasi R | Total R | Trade | Jendela + | p acak | Putusan |
|---|---|---|---|---|---|---|---|
| H-004 | breakout + ADX ≥ 30 | -0.01818 | -143.63 | 7,899 | 154/356 | 0.0099 | DITOLAK |
| H-005 | entri retest (sniper) | -0.03571 | -435.49 | 12,194 | 151/356 | 0.0396 | DITOLAK |
| H-006 | sapuan likuiditas (SMC) | -0.13449 | -2741.51 | 20,385 | 76/356 | 1.0000 | DITOLAK |

## Alasan penolakan

**H-004** — breakout + ADX ≥ 30
- ekspektasi -0.0182R < 0.05R
- jendela positif 0.43 < 0.5

**H-005** — entri retest (sniper)
- Gerbang gagal: invarian_risiko
- ekspektasi -0.0357R < 0.05R
- p entri acak 0.0396 > 0.0167
- jendela positif 0.42 < 0.5

**H-006** — sapuan likuiditas (SMC)
- Gerbang gagal: entri_acak, invarian_risiko
- ekspektasi -0.1345R < 0.05R
- p entri acak 1.0000 > 0.0167
- jendela positif 0.21 < 0.5

## Pembanding tetap

| Hipotesis | Ekspektasi R | Putusan |
|---|---|---|
| H-001b Donchian | 0,03086 | DITOLAK |
| H-002 Donchian + saringan carry | 0,03159 | DITOLAK |
| H-003 pembalikan skor-z | −0,24782 | DITOLAK |

Angka pembanding disalin dari laporan yang sudah dikomit; ketiganya tidak dijalankan ulang.
