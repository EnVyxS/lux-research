# H-015 — informasi funding atau kecondongan arah?

> Putusan H-015 dapat LULUS, DITOLAK, atau TIDAK DAPAT DINILAI. LULUS di sini berarti LULUS KRITERIA PRA-REGISTRASI ADR-037 pasal 5, dan BUKAN kelulusan ADR-015 pasal 4.4: p yang dipakai berasal dari penarikan bulan kalender UTC (ADR-028), bukan dari sebaran permutasi sinyal, sehingga medan memenuhi_adr015 tetap False bahkan pada cabang LULUS. Yang mengikat hanya F - A. Selisih F - K ikut dicetak dan HARAM dipakai sebagai dasar kelulusan: funding positif pada 79,1% periode membuat saringan apa pun mengalahkan kontrol tanpa memuat setitik pun informasi. Angka +0,029481R milik H-014 bukan pembanding H-015 dalam bentuk apa pun.

> p di sini mengukur ketidakpastian PENARIKAN SIMBOL/BULAN, bukan sebaran permutasi sinyal. Ia TIDAK memenuhi ADR-015 pasal 4.4 yang menuntut p atas minimal 300 permutasi sinyal. Angka ini sah dipakai untuk MENJATUHKAN klaim selisih antar sel, dan tidak sah dipakai untuk MENEGAKKANNYA.

## Putusan

**TIDAK DAPAT DINILAI**

- gerbang gagal tanpa pemakluman: {'A': ['checksum', 'invarian_risiko'], 'F': ['checksum', 'invarian_risiko'], 'K': ['checksum', 'invarian_risiko']}. Gerbang ada supaya angkanya tidak dipercaya, jadi angkanya tidak dipakai untuk menjatuhkan maupun menegakkan apa pun

## Besaran, dilaporkan dua kali (aturan 49)

- Rerata selisih bulanan F - A (MENGIKAT): **+0.008903R**
- Selisih agregat F - A: **+0.002182R**
- Ambang besaran: 0.02R, dibekukan ADR-037 dan tidak digeser sesudah hasil terlihat (ADR-037 pasal 10).

Dua besaran dilaporkan sebab keduanya tidak identik (aturan 49). Yang MENGIKAT adalah rerata bulanan, sebab satuan penarikan H-015 adalah bulan kalender UTC (ADR-028). H-014 mati dengan kedua angka ini berlawanan tanda, dan itu tercatat sebagai cacat kelas 16.

- Selisih F - K: **-0.015719R** — Selisih F - K TIDAK MENGIKAT dalam bentuk apa pun dan haram dipakai sebagai dasar kelulusan.

## Signifikansi pada satuan bulan (ADR-028)

- Pasangan bulan: **73**
- p uji tanda: **+0.187281** (10000 ulangan, seed 20260727), ambang 0.05
- Selang bootstrap 95%: **[-0.003113, +0.021888]R**
- Fraksi bulan positif: 0.589041095890411
- Trade sel F / sel A: **53,025** / **53,904**, lantai 100
- Ulangan permutasi run: **300**, lantai 300
- Pengaman mati: tidak ada
- Gerbang gagal tanpa pemakluman: {'A': ['checksum', 'invarian_risiko'], 'F': ['checksum', 'invarian_risiko'], 'K': ['checksum', 'invarian_risiko']}
- Gerbang dimaklumi (aturan 36): {'A': ['lookahead']}
- Memenuhi ADR-015 pasal 4.4: **TIDAK**

## Yang tidak dijawab laporan ini

Bahkan pada cabang LULUS, laporan ini tidak menyatakan bahwa saringan funding memenuhi ADR-015 pasal 4.4, dan tidak menyatakan bahwa sistem siap diperdagangkan. Kelulusan ADR-015 menuntut sebaran nol permutasi sinyal atas minimal 300 seed; yang dihitung di sini adalah penarikan bulan kalender UTC.

