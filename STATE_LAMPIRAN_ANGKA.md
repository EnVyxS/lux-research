# STATE LAMPIRAN ANGKA — arsip besaran H-012 sampai H-015

> Dipisahkan dari `STATE.md` pada v33 (2026-07-27) sebagai mitigasi **aturan 35**: v32 tumbuh menjadi 48.058 B, dan berkas sepanjang itu tidak dapat dibaca ulang utuh lalu ditulis penggantinya dalam satu jendela konteks. Isi berkas ini **dipindahkan verbatim** dari v32; tidak ada angka yang diubah, dihapus, atau dibulatkan.
>
> **PERINGATAN YANG BERLAKU ATAS SELURUH BERKAS INI (ADR-038 §5.3).** Setiap besaran di bawah lahir pada run yang **gagal gerbang `invarian_risiko`**, dan sebagian juga gagal `checksum` dan `funding_ekor`. Putusan DITOLAK-nya tetap berlaku; **kewenangan besarannya dibatalkan**. Angka-angka ini disimpan sebagai catatan sejarah dan bahan diagnostik, **bukan** sebagai bukti tentang perilaku strategi.

## 1. Audit gerbang lintas hipotesis (BARU di v33, ADR-038 §2)

| Hipotesis | Interval | Lantai ADR-014 | `invarian_risiko` | Kerugian terburuk | SHA laporan |
|---|---|---|---|---|---|
| H-011 semesta penuh | 1h | tidak | **GAGAL** | **−470.0612R** | `306d60ea` |
| H-012 periode tertahan | 1h | ya | **GAGAL** | **−21.3131R** | `182b1622` |
| H-013 SS sinyal stop | 4h | ya | **GAGAL** | **−11.4736R** | `4c2ae97b` |
| H-014 SSp / SHp | 4h | ya | **GAGAL** | (json) | `5642b7cf` |
| H-015 K kontrol | 4h | ya | **GAGAL** | **−11.4736R** | `b1c63c36` |
| H-015 F saringan | 4h | ya | **GAGAL** | **−11.4736R** | `1abe91cb` |
| H-015 A acak | 4h | ya | **GAGAL** | **−11.4736R** | `4d3e4fa5` |

**Tidak ada satu pun hasil, pada interval apa pun, yang pernah lolos sebelas gerbang.** H-011 dan H-012 lulus `checksum` ("hilang 0, asing 0, tidak cocok 0") karena `reports/manifest_aset.json` (1h) sudah ada sebelum run.

Bentuk ekor berbeda antara kedua interval:

| | H-012 (1h) | H-015 F (4h) |
|---|---|---|
| terburuk ke-1 | −21.3131 | −11.4736 |
| terburuk ke-2 | **−1.4966** | **−8.3672** |
| terburuk ke-3 | −1.4246 | −7.3796 |
| terburuk ke-10 | −1.3865 | −4.1287 |

Pada H-012 hanya **satu** perdagangan melewati 1,5R. Pada H-015 sekurangnya **sepuluh** melewati 4R. Pada 4h ini satu **kelas** kejadian, bukan kejadian tunggal.

## 2. H-015 — TIDAK DAPAT DINILAI (run `30249117960`)

Seluruh angka di bawah **haram** dipakai untuk menegakkan atau menjatuhkan klaim tentang strategi.

| Besaran | Nilai |
|---|---|
| rerata selisih bulanan F − A (**mengikat**) | +0,008903082974700181R |
| agregat F − A | +0,0021820117172933196R |
| F − K bulanan (**haram**) | −0,01571883629037982R |
| F − K ekspektasi run (**haram**) | +0,01348362637647535R |
| p uji tanda bulanan | 0,1872812718728127 (m 1872, 10000 ulangan, seed 20260727) |
| bootstrap 95% | [−0,003112849756744765, +0,02188788728847709]R (seed 20260728) |
| fraksi bulan positif | 0,589041095890411 |
| rerata berbobot | 0,001667219936026623 |
| median selisih | 0,002404502189742308 |
| pasangan bulan | 73 |
| `pengaman_mati` | {} |

| Sel | Trade | Ekspektasi R | Total R | Jendela positif | detik |
|---|---|---|---|---|---|
| K kontrol | 59.306 | 0,06773132069859376 | 4016,8737053508016 | 2228 / 4085 | 70 |
| F saringan | 53.025 | 0,08121494707506911 | 4306,42256865554 | 2269 / 4083 | 74 |
| A acak | 53.904 | 0,07903293535777578 | 4260,191347525546 | 2260 / 4083 | 162 |

Alasan keluar — K `{target 18643, stop 33703, carry 82, umur 5149, akhir_data 1729}` · F `{target 16706, stop 29835, umur 4881, akhir_data 1576, carry 27}` · A `{target 16956, stop 30395, umur 4937, akhir_data 1590, carry 26}`. **Carry bukan nol pada ketiga sel — R-L5 TEPAT, cacat 18 ditutup.**

`gerbang_gagal` ketiga sel: `["invarian_risiko", "checksum"]`. Sidik K `61dc0acf646d5b69` · F `f4b823362d12c27b` · A `96fa54b7cca7abb1`. 9 kombinasi. 437 simbol layak dari 438; dibuang `USDCUSDT` (median_stop_frac 3.797195e-04).

Sebelas gerbang sel K: `forward_fill` lulus 0.0014/0.3 · `buy_and_hold` lulus 0.8150 · `entri_acak` lulus 0.0100/0.05 · `lookahead` lulus 0.0000 · **`invarian_risiko` GAGAL −11.4736 / −1.5** · `funding` lulus 55925.6083 · `overlap` lulus 0 · **`checksum` GAGAL "tidak dapat dinilai: manifest baru ditulis pada run ini"** · `survivorship` lulus 1.0000/0.5 · `konsentrasi` lulus 0.9873/0.6 · `funding_ekor` lulus 0.0273/0.35.

Statistik: K std 1.37780R (ddof=1, n=59.306), galat baku 0.005658R, +0.017731R = +3.13 galat baku, kuartil min −11.4736 Q1 −1.0289 median −1.0095 Q3 1.9521 maks 3.9173 · F std 1.37651R, galat baku 0.005978R, +0.031215R = +5.22 galat baku · A std 1.37635R, galat baku 0.005928R, +0.029033R = +4.90 galat baku.

Konsentrasi: K 308 untung / 129 rugi, drop-1 0.06687R (retensi 0.9873), porsi bruto teratas 0.0139 (SANDUSDT), setara 181.0 simbol · F 314/123, drop-1 0.08018R (0.9873), 0.0155 (XLMUSDT), 189.6 simbol · A 321/116, drop-1 0.07817R (0.9890), 0.0132 (RUNEUSDT), 193.5 simbol.

Funding ekor: porsi ekor maks 0.0273 di ketiga sel; funding maks K 0.4243R (84/59306), F 0.3531R (27/53025), A 0.3531R (26/53904). Entri acak nyata K 0.07311R / F 0.08720R / **A 0.10723R** — **belum terjelaskan, memerlukan verifikasi**.

`audit_konfig` ketiga sel: `menghalangi false`, `pengaman_mati []`, selisih terhadap H-013 SS hanya `maks_umur_bar 48 lawan 42`.

Sembilan pagar pra-terbang LULUS (v32 dan jurnal 40/41 salah mencatat **delapan**): cabang LULUS tercapai atas masukan sintetis (0.010989) · cabang LULUS tetap memancarkan `memenuhi_adr015` False · larangan F − K dan +0,029481R ikut tercetak · lookahead dimaklumi di A dan TIDAK di F · ambang tidak bergeser dari ADR-037 · nama laporan tidak menimpa laporan yang dikomit · pengaman carry MENYALA di ketiga sel · ketiga sel berkonfig identik · semesta dan akhir sejati 4h ada.

## 3. H-014 — DITOLAK (ADR-035, run `30221967019`)

Pemicu `52c64ac576e81883cd516316437edfff1d596ac4` (2026-07-26T21:52:25Z); laporan `603477ce8b9b55e2a67d9a7a0e7c3c843c2be379` (21:54:44Z); log blob `03e0c35c54134d9906515e2df515eb5f1c939b6c`. `855 passed in 2.98s` sebelum satu berkas diunduh. 157 MB aset 4h, 438 simbol dimuat, 437 layak. SS′ 56,9 s, SH′ 52,6 s, seluruh run 2 menit 19 detik.

| Syarat (BARU, dibekukan 2026-07-27, ADR-034) | Nilai | Ambang | Terpenuhi |
|---|---|---|---|
| rerata selisih bulanan SS′ − SH′ | **−0,027715128544164157R** | ≥ 0,020R | **TIDAK** |
| p uji tanda berpasangan bulanan | **0,37596240375962403** | ≤ 0,05 | **TIDAK** |
| pasangan bulan | 73 | ≥ 2 | ya |
| trade sel A / sel B | 59.324 / 44.538 | ≥ 100 | ya |

`p` dengan m 3759, ulangan 10000, seed 20260727. Bootstrap 95% [−0,09067851377334449, +0,029103950604927244] (seed 20260728) — memuat nol. `memenuhi_adr015` false. Penggabung keluar berkode 0 (aturan 48).

| Sel | `pakai_target` | `maks_umur_bar` | Trade | Ekspektasi R | Jendela positif | p entri acak | Gerbang gagal |
|---|---|---|---|---|---|---|---|
| SS′ | **True** | 48 | 59.324 | +0,06725203533326735 | 2229 / 4082 | 0,016611295681063124 | `invarian_risiko`, `checksum`, `funding_ekor` |
| SH′ | **False** | 48 | 44.538 | +0,03959765698185091 | 1982 / 4082 | 0,21926910299003322 | `entri_acak`, `invarian_risiko`, `checksum`, `funding_ekor` |

Alasan keluar SS′: `stop` 33.748 · `target` 18.667 · `umur` 5.174 · `akhir_data` 1.735. SH′: `stop` 28.013 · `umur` 14.426 · `akhir_data` 2.099. **Nol `carry` pada keduanya** — cacat 18.

SS′: 309 untung / 128 rugi, drop-1 0,06639R (retensi 0,9872), drop-22 0,05419R, median simbol +0,06789R, porsi bruto teratas 0,0139 (SANDUSDT), funding maks 0,8285R, std 1,37827R, galat baku 0,005659R (+3,05 SE), parameter {55:836, 20:1711, 100:1535}, sidik `197c10e3f0d2`.
SH′: 234 untung / 203 rugi, drop-1 0,03583R (retensi 0,9047), drop-22 0,01225R, median simbol +0,02710R, porsi bruto teratas 0,0431 (VELVETUSDT), funding maks 2,9000R, std 2,20818R, galat baku 0,010463R (−0,99 SE), parameter {55:1073, 20:1995, 100:1014}, sidik `5721a88e59eb`. 73 bulan pada kedua sel.

Kode H-014: commit `4af2117639c15ace7ba4a442ce2841091a1e25fb`; `reports/tests.md` blob `94e5096e2f989edc13d3f1a95daa84b6b512331e`, run `30221837845`, `855 passed in 3.06s`. Workflow `h014.yml` commit `52c64ac5`: `timeout-minutes: 180`, daftar `git add` cacat (cacat 17).

H-014 tidak pernah dapat LULUS, dan itu dipra-registrasi (ADR-034 §2): `PUTUSAN_MUNGKIN = ("DITOLAK", "TIDAK DAPAT DINILAI")`.

### Cacat kelas keenam belas — tanda besaran bergantung pada pembobotan (ADR-035 §2, aturan 55)

| Cara membobot | Nilai | Tanda |
|---|---|---|
| selisih **agregat** | **+0,027654378351416438R** | **POSITIF** |
| **rerata** selisih bulanan | **−0,027715128544164157R** | **NEGATIF** |
| rerata berbobot trade | −0,012499029724652699R | NEGATIF |
| median selisih bulanan | +0,03495217650445759R | POSITIF |
| fraksi bulan positif | 0,5616438356164384 | — |

Dua angka pertama hampir sama besar dan berlawanan tanda. Bila pembobotan bebas dipilih, H-014 melewati ambang besaran dengan agregat +0,0277R. Yang mencegahnya bukan kehati-hatian saya melainkan `gabung_h014.adjudikasi` membaca `rerata_selisih`, dan kode itu dikomit **sebelum** satu angka pun ada. p 0,376 menjatuhkan hipotesis pada pembobotan mana pun.

**Terulang di H-015 (v33):** F − K bulanan −0,0157R lawan F − K ekspektasi run +0,0135R — berlawanan tanda lagi.

### Klaim ADR-033 dibatalkan sebagian — umur 42 lawan 48 bukan sebab utama (ADR-035 §4)

| Sel | Umur | Trade |
|---|---|---|
| SS (H-013) | 42 | 60.018 |
| SS′ (H-014) | 48 | 59.324 |
| SH (H-013) | 48 | 44.614 |
| SH′ (H-014) | 48 | 44.538 |

Efek 42 → 48 pada sel bertarget: −694 perdagangan, −1,2%. Jarak antar sel dengan umur disetarakan: +33,2% — hampir seluruhnya `pakai_target`. Aturan 52 tidak dibatalkan; +0,029481R tetap haram. Catatan ADR-036: baris SH lawan SH′ juga memuat efek pengaman carry yang mati.

## 4. H-013 — DITOLAK (ADR-031, run `30217516013`)

Pemicu `97b36c19`; sepuluh pecahan 20:13:43Z–20:28:15Z; laporan p `1d746879`. Seed utuh 300 pada [0,300), 73 bulan pada SS, keluar 0.

| Syarat ADR-015 §4.4 | Nilai | Ambang | Terpenuhi |
|---|---|---|---|
| besaran SS − AS | +0,054842R | 0,020R | ya |
| **p satuan bulan** | **0,205980** | 0,05 | **TIDAK** |
| ulangan | 300 | 300 | ya |
| trade terkecil antar sel | 54.812 | 100 | ya |

Sebaran nol 300 seed: rerata +0,022916R · sd +0,011377R · rentang −0,004632R … +0,057394R · sel SS +0,066648R. p satuan perdagangan 0,003322 — haram menegakkan (aturan 45). Jalur A: p bulanan berpasangan 0,365363, bootstrap memuat nol.

Cacat kelas ketiga belas (ADR-031): +0,054842R dihitung terhadap satu sel nol seed 42; terhadap rerata nol ia +0,043732R. Dibayar di sumber lewat `6ae83062` dan `5bd73fbf`. `reports/h013b_p.md` tetap memuat prosa R-D3 yang salah (aturan 50).

### Jalur A — keberartian jatuh pada satuan bulan

**SS lawan AS:**

| Besaran | simbol (437) | bulan (73) |
|---|---|---|
| rerata selisih | +0,035625R | +0,023327R |
| rerata berbobot trade | +0,053518R | +0,047950R |
| selisih agregat | +0,054842R | +0,054842R |
| median selisih | +0,050280R | +0,036628R |
| fraksi positif | 0,6293 | **0,5342** |
| p uji tanda | **0,001100** | **0,365363** |
| bootstrap 95% | [+0,015182, +0,055725]R | **[−0,027040, +0,073620]R — MEMUAT NOL** |

**SH lawan AH:** simbol — rerata −0,010358R, berbobot −0,023331R, agregat −0,021004R, fraksi 0,4760, p 0,777622. Bulan — rerata −0,029960R, berbobot −0,028521R, median −0,072371R, fraksi 0,4110, p 0,280372. Anomali SH < AH turun pangkat menjadi derau. R-A1…R-A6: empat tepat, R-A4 MELESET, R-A5 MELESET JAUH.

### ADR-032 dibatalkan sebagian (ADR-033 §2)

Keberatan B ADR-032 ("tanpa stop, penyebut R adalah jarak nosional") **SALAH**: `engine.jalankan` mengevaluasi `kena_stop` tanpa syarat, `pakai_target=False` hanya mematikan target, jadi penyebut R dibangun identik. Akibatnya `AH = +0,05817042814276683R` kembali TIDAK TERJELASKAN — **ini memerlukan verifikasi**. R-F1…R-F5 DIBATALKAN.

### Cacat kelas keempat belas dan kelima belas (ADR-033, ADR-034)

**Keempat belas:** `run_h013.umur_sel` memberi 42 untuk sel bertarget dan 48 untuk sel tanpa target, jadi SS − SH mencampur dua medan. Putusan H-013 tidak berubah — ia mati pada p bulanan 0,205980 kaki sinyal. Yang berubah: `+0,029481R` tidak mengukur apa yang namanya sebut.

**Kelima belas:** ADR-032 dan ADR-033 mengutip ambang ADR-015 §4.4 sebagai beku untuk kaki geometri, padahal §4.4 membekukannya untuk kaki sinyal. Ambang H-014 karena itu BARU, dibekukan 2026-07-27.

## 5. H-012 — DITOLAK (jalur 1h, sidik `75f9c7ccd65ec30f`)

437 simbol, 12 kombinasi, 1220,6 s. Putusan DITOLAK atas `p entri acak 0.0631 > 0.05`. Gerbang gagal: `entri_acak`, `invarian_risiko`, `funding_ekor`.

Perdagangan 135.681 · total R 8091,52 · ekspektasi **0,05963634457229065** · jendela positif 2246/4081 · alasan keluar `{stop 101417, umur 9699, target 21658, akhir_data 2479, carry 428}` · entri ditolak pengaman biaya 62 (PAXGUSDT 42, BTCDOMUSDT 11, MASKUSDT 4, BNBUSDT 3, BTCUSDT 1, TRXUSDT 1).

Simpangan baku 2,22746R (ddof=1, n=135.681) · galat baku 0,006047R · selang 95% [0,047784, 0,071489]R · kuartil min −21,3131 Q1 −1,0632 median −1,0401 Q3 −0,4209 maks 12,9076 · jarak ke ambang 0,05R = +0,009636R = +1,59 galat baku.

Gerbang: `forward_fill` lulus 0.0013 · `buy_and_hold` lulus 0.8401 (unggul 394/437) · **`entri_acak` GAGAL 0.0631** (18 dari 300 permutasi) · `lookahead` lulus 0.0000 · **`invarian_risiko` GAGAL −21.3131** · `funding` lulus 153788.1322 · `overlap` lulus 0.0000 · **`checksum` LULUS** (hilang 0, asing 0, tidak cocok 0) · `survivorship` lulus 1.0000 (delisted 0.1465 vs 0.1465) · `konsentrasi` lulus 0.9849 (306/131, drop-1 0.05873R, teratas 0.0142 FLMUSDT, setara 174.3 simbol) · **`funding_ekor` GAGAL 0.1693/0.35** atas `funding_maks_R` 0.6601R (430 dari 135.681 di atas pengaman).

Dibuang lantai: `USDCUSDT` (median stop_frac 1.293930e-04, biaya masuk 15,46R).

Parameter terpilih didominasi `imbalan_R 8.0` (655 + 574 + 496 jendela) — jauh dari `imbalan_R 2.0` yang dibekukan pada jalur 4h.

Ekor funding H-012: #1 −21.3131 (funding 0.4825, porsi 0.0226), #2 −1.4966, #3 −1.4246, #4 −1.4176, #5 −1.4159, #6 −1.4103, #7 −1.4068, #8 −1.4061, #9 −1.3870, #10 −1.3865.

Biaya: rerata transaksi 0,0359R · rerata funding −0,0010R · rerata jarak stop 3,507% · perdagangan berbiaya > 1R **0** dari 135.681.

## 6. H-011 — DITOLAK (jalur 1h, tanpa lantai ADR-014)

`invarian_risiko` **GAGAL −470,0612R** — kerugian terburuk terbesar yang pernah tercatat di seluruh riset ini, dan bukti terkuat bahwa lantai median `stop_frac` 0,004 bekerja (faktor 41 terhadap H-015). `checksum` **lulus**. Rincian lain ada di `reports/backtest_h011_semesta_penuh.md` (`306d60ea`).
