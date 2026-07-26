# Uji berpasangan h013_berpasangan_sh_ah (ADR-026, Jalur A)

> p di sini mengukur ketidakpastian PENARIKAN SIMBOL/BULAN, bukan sebaran permutasi sinyal. Ia TIDAK memenuhi ADR-015 pasal 4.4 yang menuntut p atas minimal 300 permutasi sinyal. Angka ini sah dipakai untuk MENJATUHKAN klaim selisih antar sel, dan tidak sah dipakai untuk MENEGAKKANNYA.

Sel A `reports/backtest_h013_sh_sinyal_horizon.json` terhadap sel B `reports/backtest_h013_ah_acak_horizon.json`.

## Hasil

### Tingkat simbol

- Pasangan: **437**
- Rerata selisih: **-0.010358R**
- Rerata berbobot trade: **-0.023331R**
- Selisih agregat (pembanding): **-0.021004R**
- Median selisih: **-0.009670R**
- Fraksi pasangan positif: **0.4760**
- p uji tanda (10,000 ulangan, seed 20260727): **0.777622**
- Selang bootstrap 95%: **[-0.052779, +0.046846]R**
- Melewati ambang besaran 0.02R: **tidak**
- Memenuhi ADR-015 pasal 4.4: **TIDAK**

### Tingkat bulan

- Pasangan: **73**
- Rerata selisih: **-0.029960R**
- Rerata berbobot trade: **-0.028521R**
- Selisih agregat (pembanding): **-0.021004R**
- Median selisih: **-0.072371R**
- Fraksi pasangan positif: **0.4110**
- p uji tanda (10,000 ulangan, seed 20260727): **0.280372**
- Selang bootstrap 95%: **[-0.084772, +0.024341]R**
- Melewati ambang besaran 0.02R: **tidak**
- Memenuhi ADR-015 pasal 4.4: **TIDAK**

## Yang tidak dijawab laporan ini

Putusan sah H-013 menuntut sebaran permutasi **sinyal** atas minimal 300 seed pada sel pembanding (Jalur B ADR-026). Laporan ini hanya menentukan apakah Jalur B layak dibeli.

