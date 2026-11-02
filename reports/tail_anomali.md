# Anomali backfill ekor

| Interval | Simbol | Hari | Baris | Diharapkan | Terisi | Celah/simbol |
|---|---|---|---|---|---|---|
| 1h | 748 | 5,583 | 133,992 | 133,992 | 1.0 | 0.22 |
| 4h | 748 | 5,163 | 30,978 | 30,978 | 1.0 | 0.2 |

## Perbandingan interval

- Hari ditambal 1h: 5,583, 4h: 5,163
- Rasio baris 1h:4h = 4.3254 (seharusnya 4,0)
- Diagnosis: **arsip harian tidak simetris antar interval**
