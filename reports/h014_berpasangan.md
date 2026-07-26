# H-014 — geometri keluar dengan umur pegangan disetarakan

> Putusan H-014 hanya dapat DITOLAK atau TIDAK DAPAT DINILAI; tidak ada cabang LULUS di modul ini, dan pengujian menuntut ketiadaannya (ADR-034). SS' dan SH' BUKAN sel SS dan SH run 30214203863: kedua sel di sana berbeda pada DUA medan sekaligus (ada-tidaknya target DAN umur 42 lawan 48), sehingga +0,029481R tidak boleh dipakai sebagai pembanding maupun sebagai 'versi sebelum perbaikan'. Berkas md tiap sel mencetak LULUS atau DITOLAK milik pra-registrasi PER SEL dari runner; itu bukan putusan H-014.

## Putusan

**DITOLAK**

- rerata selisih bulanan -0.027715128544164157 < 0.02R
- p uji tanda bulanan 0.37596240375962403 > 0.05

## Besaran, dilaporkan dua kali (aturan 49)

- Rerata selisih bulanan: **-0.027715R**
- Selisih agregat: **+0.027654R**
- Ambang besaran: 0.02R — ambang **BARU**, dibekukan 2026-07-27 (ADR-034, aturan 53), bukan kutipan ADR-015 pasal 4.4 yang membekukan ambang bagi kaki sinyal.

Dua besaran dilaporkan sebab keduanya tidak identik (aturan 49). Pembanding terhadap rerata sebaran nol TIDAK ADA di uji ini: nol permutasi geometri belum dirancang.

## Signifikansi pada satuan bulan (ADR-028)

- Pasangan bulan: **73**
- p uji tanda: **+0.375962** (10000 ulangan, seed 20260727), ambang 0.05
- Selang bootstrap 95%: **[-0.090679, +0.029104]R**
- Fraksi bulan positif: 0.5616438356164384
- Trade sel A / sel B: **59,324** / **44,538**, lantai 100
- Memenuhi ADR-015 pasal 4.4: **TIDAK**

## Yang tidak dijawab laporan ini

Putusan LULUS tidak mungkin dihasilkan uji ini dan tidak ada cabang kodenya. Kelulusan kaki geometri menuntut sebaran nol permutasi **geometri** yang belum dirancang; ADR-033 pasal 3 membuktikan bahwa nol jarak stop menuntut bedah `engine.jalankan` yang dipakai tiga belas hipotesis, dan bedah itu tidak dibeli.

