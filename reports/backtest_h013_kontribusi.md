# H-013 — sumbangan sinyal terhadap sumbangan geometri keluar

Yang dinilai adalah **selisih antar sel**, bukan kelulusan satu sel. Sel SH, AS, dan AH adalah pembanding, bukan kandidat untuk didagangkan.

`lookahead` dan `entri_acak` **dijamin gagal** pada sel AS dan AH karena permutasi bergantung panjang array (ADR-021). Itu konsekuensi konstruksi dan bukan temuan tentang data.

Jendela walk-forward diturunkan dari hari (ADR-023): latih 1080 bar, uji 540, embargo 42, pemanasan 200 bar yang **tidak** dikonversi. Satu jendela menuntut 1862 bar.

Pengaman biaya masuk 0.5R dan `stop_hormati_celah` dipasang oleh `dasar_riset`, sebab pemuat config tidak pernah membaca kedua kunci itu.

## Empat sel

| Sel | Sinyal | Target | Umur (bar 4h) | Jendela | Trade | Ekspektasi R | p acak | Gerbang gagal |
|---|---|---|---|---|---|---|---|---|
| SS | sungguhan | ya | 42 | 4,082 | 60,018 | +0.066648 | 0.0166 | invarian_risiko, checksum |
| SH | sungguhan | tidak | 48 | 4,082 | 44,614 | +0.037167 | 0.2259 | entri_acak, invarian_risiko, checksum, funding_ekor |
| AS | permutasi | ya | 42 | 4,082 | 55,927 | +0.011806 | 0.3588 | entri_acak, lookahead, invarian_risiko, checksum, konsentrasi |
| AH | permutasi | tidak | 48 | 4,082 | 45,378 | +0.058170 | 0.1993 | entri_acak, lookahead, invarian_risiko, checksum, funding_ekor |

## Tiga selisih

- Sumbangan **sinyal** (SS − AS): **+0.054842R** terhadap ambang 0.02R
- Sumbangan **geometri** (SS − SH): **+0.029481R**
- **Interaksi** (SS−AS) − (SH−AH): **+0.075846R**

**LULUS**

Sumbangan geometri yang lebih besar daripada sumbangan sinyal berarti sepuluh hipotesis pertama mengukur struktur keluar, bukan kemampuan memilih momen. Itu hasil yang sah dan tidak boleh dibaca sebagai kegagalan mesin.

`invarian_risiko` yang jatuh pada sel tanpa target **bukan** bukti target lebih baik: jalur `umur` mengisi pada harga bar sungguhan, sedangkan jalur stop hanya seburuk celah pembukaan.

