# H-015 — informasi funding atau kecondongan arah?

Yang mengikat hanya **F − A**. Sel K adalah kontrol dan selisih terhadapnya **tidak mengikat dalam bentuk apa pun**.

| Sel | Peran | Jendela | Trade | Ekspektasi R | p acak | Gerbang gagal |
|---|---|---|---|---|---|---|
| K | kontrol | 4,085 | 59,306 | +0.067731 | 0.0100 | invarian_risiko, checksum |
| F | saringan funding | 4,083 | 53,025 | +0.081215 | 0.0100 | invarian_risiko, checksum |
| A | penolakan acak setara | 4,083 | 53,904 | +0.079033 | 0.0066 | invarian_risiko, checksum |

## Dua selisih

- **MENGIKAT** F − A: **+0.002182R** terhadap ambang 0.02R
- TIDAK mengikat F − K: +0.013484R

**GAGAL besaran**

## Bacaan angka

Selisih mengikat F − A (+0.002182R) **di bawah** ambang beku 0.02R, jadi separuh kriteria yang dapat dihitung sudah tidak terpenuhi. Ambang itu tidak digeser.

Selisih TIDAK mengikat F − K (+0.013484R) lebih besar dalam nilai mutlak daripada F − A (+0.002182R). Bacaan itu konsisten dengan funding positif 79,1%: sebagian keunggulan saringan terhadap kontrol adalah kecondongan arah, bukan informasi. Angka F − K tetap haram dipakai sebagai dasar kelulusan.

Medan `lulus` di berkas ini hanya menguji BESARAN F − A terhadap ambang 0,020R. Ia BUKAN kelulusan hipotesis: ADR-037 §5 menuntut besaran itu DAN p ≤ 0,05 atas satuan penarikan bulan kalender UTC (ADR-028), dan p tidak dihitung di berkas ini. Selisih F − K yang ikut tercetak TIDAK MENGIKAT dalam bentuk apa pun: funding positif pada 79,1% periode membuat saringan apa pun mengalahkan kontrol tanpa memuat informasi, sehingga memakainya sebagai dasar kelulusan ada di daftar angka haram.

