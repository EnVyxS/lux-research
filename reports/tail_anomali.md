# Anomali backfill ekor

| Interval | Simbol | Hari | Baris | Diharapkan | Terisi | Celah/simbol |
|---|---|---|---|---|---|---|
| 1h | 763 | 7,672 | 184,128 | 184,128 | 1.0 | 0.01 |
| 4h | 763 | 7,674 | 46,044 | 46,044 | 1.0 | 0.01 |

## Perbandingan interval

- Hari ditambal 1h: 7,672, 4h: 7,674
- Rasio baris 1h:4h = 3.999 (seharusnya 4,0)
- Diagnosis: **arsip harian tidak simetris antar interval**
