# Uji berpasangan h013_berpasangan_ss_as (ADR-026, Jalur A)

> p di sini mengukur ketidakpastian PENARIKAN SIMBOL/BULAN, bukan sebaran permutasi sinyal. Ia TIDAK memenuhi ADR-015 pasal 4.4 yang menuntut p atas minimal 300 permutasi sinyal. Angka ini sah dipakai untuk MENJATUHKAN klaim selisih antar sel, dan tidak sah dipakai untuk MENEGAKKANNYA.

Sel A `reports/backtest_h013_ss_sinyal_stop.json` terhadap sel B `reports/backtest_h013_as_acak_stop.json`.

## Hasil

### Tingkat simbol

- Pasangan: **437**
- Rerata selisih: **+0.035625R**
- Rerata berbobot trade: **+0.053518R**
- Selisih agregat (pembanding): **+0.054842R**
- Median selisih: **+0.050280R**
- Fraksi pasangan positif: **0.6293**
- p uji tanda (10,000 ulangan, seed 20260727): **0.001100**
- Selang bootstrap 95%: **[+0.015182, +0.055725]R**
- Melewati ambang besaran 0.02R: **ya**
- Memenuhi ADR-015 pasal 4.4: **TIDAK**

### Tingkat bulan

- Pasangan: **73**
- Rerata selisih: **+0.023327R**
- Rerata berbobot trade: **+0.047950R**
- Selisih agregat (pembanding): **+0.054842R**
- Median selisih: **+0.036628R**
- Fraksi pasangan positif: **0.5342**
- p uji tanda (10,000 ulangan, seed 20260727): **0.365363**
- Selang bootstrap 95%: **[-0.027040, +0.073620]R**
- Melewati ambang besaran 0.02R: **ya**
- Memenuhi ADR-015 pasal 4.4: **TIDAK**

## Yang tidak dijawab laporan ini

Putusan sah H-013 menuntut sebaran permutasi **sinyal** atas minimal 300 seed pada sel pembanding (Jalur B ADR-026). Laporan ini hanya menentukan apakah Jalur B layak dibeli.

