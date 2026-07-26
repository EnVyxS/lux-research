# Prompt kelanjutan — tempel ini di sesi baru

> Disegarkan 2026-07-27 02:55 WIB, sesudah commit `af470704` (**811 pengujian lulus**; ADR-025 s.d. ADR-030 selesai; **Jalur B sedang berjalan**).
> Berkas ini hanya jembatan. **Sumber kebenaran tunggal tetap `STATE.md`** (versi 24; v25 ditahan sampai Jalur B memvonis).

---

## Tempel mulai dari sini

Sebelum melakukan apa pun, baca `STATE.md` di repositori GitHub publik **EnVyxS/lux-research**, lalu berkas ini. **Jangan membaca `journal/` secara utuh** — hanya bila ada rujukan spesifik. Lanjutkan dari titik terakhir; jangan mulai dari awal dan jangan mengulang pekerjaan yang sudah selesai.

**TUGAS PERTAMA, SEBELUM APA PUN: periksa status Jalur B.** Sepuluh pekerjaan pecahan dipicu oleh commit `97b36c19` pada 2026-07-26T19:45:13Z. Periksa lewat `list_commits`, **jangan mengasumsikan**. Yang dicari, berurutan:

1. Sepuluh commit `chore(h013b): pecahan seed <lo>-<hi> run <ID>` — cakupan wajib `0-30` sampai `270-300` **tanpa lubang**.
2. Satu commit `chore(h013b): laporan p Jalur B run <ID>` dari pekerjaan penggabung.
3. Baca **`reports/h013b_p.md`**. Itu satu-satunya berkas yang boleh melahirkan putusan H-013.

Bila sebuah pecahan hilang, sebabnya mungkin **lomba dorong**, bukan backtest — lihat `reports/h013b_log_<lo>_<hi>.md`. Bila `reports/h013b_p.json` tidak ada, penggabung menolak melahirkan putusan; sebabnya tercetak di `reports/h013b_gabung_log.md` beserta kode keluarnya.

### Konteks

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang karena tercemar survivorship bias dan overfitting. Mesin lokal tidak sanggup backtest penuh dan tidak ada VM cloud, jadi **seluruh komputasi berjalan di GitHub Actions** dan repo GitHub adalah penyimpanan data sekaligus jurnal riset.

### Batas alat yang harus dipahami sejak awal

- Sandbox agen **tidak punya jaringan**. Semua pengambilan data terjadi di runner Actions.
- Agen **tidak bisa membaca log workflow**, dan daftar alat GitHub **tidak memuat satu pun fungsi Actions**. Diverifikasi ulang di S19. Solusinya: setiap workflow menulis hasil ke `reports/` lalu commit balik.
- Agen **tidak bisa memicu workflow manual**. Setiap workflow punya filter `paths` pada berkasnya sendiri, jadi push ke berkas itu yang memicunya. `tests.yml` memfilter `lux/**` dan `tests/**` — jadi perubahan pada `config/`, `journal/`, `decisions/`, `STATE.md`, dan berkas ini **tidak** memicu pengujian, dan ramalan cacah atas commit semacam itu **tidak dapat diadili**.
- **BARU DI S19: sepuluh pekerjaan yang mengomit ke satu cabang menuntut lingkaran ulang dorong.** `git pull --rebase --autostash` sekali — pola yang lulus di dua belas workflow lain — tidak cukup pada matriks. Dua pekerjaan yang mendorong pada detik yang sama membuat salah satunya kalah, dan **yang kalah hilang tanpa suara** lalu menyamar sebagai cakupan data yang bolong. `h013b.yml` mengulang sampai sepuluh kali dengan jeda acak.
- Pekerjaan matriks yang bergantung pada keluaran pekerjaan lain **wajib `git fetch` + `git checkout origin/main -- reports`**. Checkout bawaan berada pada SHA pemicu, yang **mendahului** seluruh commit pecahan; tanpa penarikan itu penggabung melihat nol pecahan dan menolak dengan sebab yang sama sekali salah.
- Agen tidak bisa membuat atau mengunggah rilis; runner melakukannya lewat `gh release upload`.
- REST `fapi.binance.com` mengembalikan **HTTP 451** dari runner. CDN `data.binance.vision` normal.
- `search_code` **nol hasil di repo ini**. Baca berkas langsung.
- `get_file_contents` menuntut SHA 40 karakter penuh **atau** nama branch; `ref: "main"` bekerja dan itu cara termurah mengambil versi berlaku.
- Untuk menulis, **pakai `push_files`**: `{ toolName, toolArguments: { owner, repo, branch, message, files } }` — jangan menaruh `owner`/`repo`/`branch` di tingkat atas.
- **`push_files` mengganti seluruh isi berkas.** Baca berkas utuh sebelum menulis ulang; untuk berkas panjang salin hasil bacaan apa adanya lalu sunting hanya bagian yang dituju. Teks Python di repo ini memuat escape Unicode literal (`\u00b7`, `\u2014`) dan f-string berkutip bersarang.
- Runner tidak punya `scipy` dan tidak punya `requests`. Statistik memakai numpy; HTTP memakai `urllib.request`.
- **Kabar buruk datang dalam 23–32 detik; kabar baik 10–20 menit** — kecuali `tests.yml`, yang memberi kabar **baik** dalam ~23 detik juga. Jangan membaca cepatnya laporan uji sebagai kegagalan; **baca isinya**.
- **Commit laporan tanpa berkas hasil = run GAGAL. Blob laporan yang SHA-nya tidak berubah = belum ditulis.** Berkas yang belum lahir memberi "path does not point to a file", dan itu **bukan** galat alat.
- **`backfill_daily.yml` berjadwal mingguan** (`cron: '0 2 * * 1'`), jadi tidak setiap perubahan blob berasal dari saya.
- Analisis atas laporan yang sudah dikomit bisa dikerjakan di sandbox tanpa jaringan. **Begitulah cacat terbesar riset ini ditemukan** — bukan oleh run baru, melainkan dengan menghitung ulang `per_simbol` sendiri.

### Posisi sekarang, ringkas

- **Tiga belas hipotesis. Sebelas DITOLAK, satu (H-010) gagal pada 300 permutasi (p 0,0631), satu (H-013) BELUM DAPAT DINILAI.**
- **H-013 BUKAN lulus, dan inilah sebab terpenting yang harus dipahami sejak awal:** run `30214203863` menghitung **besaran** SS − AS = **+0,054842R** dan laporannya mencetak `**LULUS**` serta `"lulus": true` — dari **satu perbandingan besaran belaka**. ADR-015 §4.4 menuntut **dua** syarat: besaran ≥ 0,020R **dan** `p` ≤ 0,05 atas ≥300 ulangan permutasi sinyal. Syarat kedua **belum pernah dihitung dalam tiga belas hipotesis**. `p_entri_acak` adalah uji lain sama sekali.
- **Jalur A (ADR-026/027) selesai dan MENJATUHKAN keberartian pada satuan resmi:** uji tanda berpasangan pada tingkat **bulan** memberi `p = 0,365363` dengan bootstrap 95% **[−0,027040, +0,073620]R yang MEMUAT NOL**. Pada tingkat simbol p kecil (0,001100), tetapi ADR-028 menetapkan **bulan** sebagai satuan penarikan resmi.
- **Jalur B sedang berjalan** (`97b36c19`): sepuluh pecahan × 30 seed = 300 permutasi sinyal pada sel AS, lalu penggabung menghitung `p`.
- **Anomali SH < AH TURUN PANGKAT menjadi derau** (p 0,777622 dan 0,280372, bootstrap memuat nol di dua tingkat). Ia bukan temuan dan tidak menuntut penjelasan.
- **811 pengujian lulus**, laporan pada commit `56a27110`.

### Empat berkas Jalur B dan perannya

| Berkas | Peran | Commit |
|---|---|---|
| `lux/analisis/sebaran_nol.py` | aritmetika `p`; `p_bulanan` **mengikat**, `p_per_perdagangan` **taksiran bawah** | `05df8b78` (779) |
| `lux/backtest/run_h013b.py` | satu pecahan 30 seed; `NAMA_SPEK="h013b_as_seed"`; gerbang `entri_acak` MATI | `4f09c8d5` (795) |
| `lux/backtest/gabung_h013b.py` | **satu-satunya berkas yang boleh melahirkan putusan H-013** | `0859e8dd` (811) |
| `.github/workflows/h013b.yml` | matriks 10 pecahan + penggabung; menyentuhnya memulai sebelas pekerjaan | `97b36c19` |

**Penggabung MENOLAK melahirkan putusan dalam empat keadaan** (ADR-030): cakupan seed tidak utuh; himpunan bulan antar seed dan sel SS berbeda (kode keluar 4, laporan tetap ditulis); pecahan tidak menyatakan gerbang mati; R-D5 tidak terbukti. **DITOLAK berkode keluar 0** — run yang menjatuhkan hipotesis bekerja dengan benar.

### Ramalan beku yang belum teradili — jangan menulis ramalan baru sesudah angkanya terlihat

| Kode | Isi |
|---|---|
| R-B1 | run 4h pertama sesudah ADR-025 melapor `checksum` "tidak dapat dinilai"; run kedua **lulus** dengan dua belas `ohlcv_4h_*` |
| R-B2 / R-C1 | Jalur B per-perdagangan memberi p ≤ 0,05 tetapi **menyesatkan** |
| R-B3 / R-C2 | Jalur B pada satuan bulan memberi p > 0,05 sehingga H-013 **DITOLAK** |
| R-B4 | pemasangan bulanan berbobot trade tetap p > 0,05 |
| R-C3 | selisih p per-perdagangan lawan p bulanan lebih dari satu orde besaran |
| R-D1 | satu pecahan 30 seed selesai di bawah 40 menit |
| R-D2 | satu berkas pecahan di bawah 1 MB; sepuluh di bawah 10 MB |
| R-D3 | sedikitnya satu seed melampaui +0,0666R; bila tidak, **permutasinya cacat** |
| R-D4 | simpangan baku antar seed **melampaui** galat baku per perdagangan 0,005570R |
| R-D5 | seed 42 mereproduksi **+0,01180570125176449R** dalam 1e-12 |

### Tindakan berikutnya, urutannya wajib

1. **Periksa dan adjudikasi Jalur B** (lihat tugas pertama di atas). Adili R-D1–R-D5 dan R-B2/R-B3/R-B4/R-C1/R-C2/R-C3 **apa adanya**; jangan menghaluskan yang meleset.
2. **`STATE.md` v25** — dibaca utuh lebih dulu. Butuh: ADR-029, ADR-030, journal-23/24/25, aturan baru, cacah **811**, hasil Jalur B, dan berkas-berkas Jalur B.
3. **Baca `reports/backtest_h013_ss_sinyal_stop.json`** untuk nilai `invarian_risiko` SS — lewat skrip sisi runner yang mencetak ringkasan ke `reports/`, **jangan** menarik 432 KB ke konteks.
4. **Selesaikan pertanyaan bar datar 1h lawan 4h:** bandingkan `reports/diag_datar.json` terhadap perhitungan 4h. Bar 4h datar hanya bila keempat bar 1h datar, jadi penolakan 4h semestinya **≤ 74**. Angka 74 yang identik pada dua interval belum berarti cacat, tetapi belum berpenjelasan.
5. **Nasib `notion_asap.yml`** (`git push` polos, `git commit || echo` yang menelan kegagalan) dan **`backfill_daily.yml`** (cron mingguan + `--clobber`, mengancam ADR-025 R4). Perbaiki atau hapus **dengan keputusan tertulis**. Tinjau juga `funding.yml`, `funding_check.yml` (keduanya masih memakai `reports/universe_layak.json` pra-lantai), `doctor.yml`, `universe.yml`. **Jangan hapus tanpa keputusan tertulis.**
6. **Prosa `kontribusi.md`** sudah dibuat bergantung angka (`b0e79220`, `prosa_kontribusi`) — cacat kelas kesepuluh **DITUTUP**; yang belum adalah medan `lulus` itu sendiri, dan itu tugas Jalur B.
7. **Program riset lanjutan:** pemisahan sinyal dari geometri keluar sesudah Jalur B memvonis; **funding sebagai sinyal** (belum pernah diuji sekali pun); ADR-015 §4.5 butir 5 tampak terbalik dan §6 sudah berjanji mengakuinya.
8. **Utang teknis:** sambungkan `maks_rasio_bar_datar` config ke gerbang · periksa kunci config lain yang tak pernah dibaca (aturan 39) · bandingkan `runner.py` terhadap blob `fc79e070` dan `run_h013.py` terhadap `418f6084` untuk pergeseran prosa komentar · `hasattr`/`__import__` di `test_run_h012.py` · pengujian `biaya_bolak_balik_R` · `pytest` ke `requirements-dev.txt` · tripwire tekstual `inspect.getsource` (lemah, dicatat sebagai lemah) · pemetaan `dari_laporan` pelapor Notion · perketat `lux/funding.py::gerbang_lulus` · salin ADR-001/ADR-002 ke `decisions/` · naikkan `versi` config sesudah seluruh pembacanya diperiksa.
9. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, dengan ≥24 shard.

**Sudah lunas, jangan dikerjakan ulang:** modul degenerasi · pengaman biaya masuk · perambatan walk-forward · lantai semesta · agregat per bulan · `sebaran.py` · `geometri_keluar.py` · pelapor Notion · `stop_hormati_celah` · `validate`/`potong_ekor` berinterval · `lux/kerangka.py` · ADR-019 · **audit tujuh workflow** · **ADR-025 manifest per interval** (`fb128c93` + `43cd4eed`) · **Jalur A** · **ADR-028 satuan penarikan** · **`prosa_kontribusi`** · **ketiga modul Jalur B**.

**DIBATALKAN atas keputusan pengguna:** agen **LUX Gatekeeper** dan **LUX Gatekeeper Reporter** tidak dipakai lagi. Kolom `Verdict` di database Notion **LUX — Run Results** menjadi kolom **manusia**.

### Godaan yang wajib ditolak

**+0,060163R** (H-010 tanpa USDCUSDT) dan **+0,059636R** (H-012 seluruh riwayat) haram dipakai sebagai kelulusan — keduanya pemilihan pasca-hasil. **+0,054842R** dan **+0,066648R** haram dikutip sebagai kelulusan atau kelayakan H-013. Kata **LULUS** pada `backtest_h013_kontribusi.md` haram dikutip. **p 0,001100 tingkat simbol** haram dikutip sebagai keberartian — satuan resminya bulan. **Setiap p atau galat baku per perdagangan** haram dipakai sebagai bukti keberartian, termasuk "+2,99 galat baku".

**Dilarang menyebut H-012 atau H-013 "H-010 setelah perbaikan".** Dilarang menyatakan sistem siap dagang.

### Cara saya ingin kamu bekerja

- Ketika saya menulis "lanjut", teruskan langsung dari titik terakhir tanpa konfirmasi dan tanpa mengulang penjelasan.
- **Pisahkan fakta terverifikasi dari asumsi.** Asumsi naik jadi fakta hanya dengan commit, run ID, atau kutipan sumber.
- Katakan bila saya salah, dan katakan bila kamu sendiri salah — jangan menghaluskan ramalan yang meleset.
- Perbarui `STATE.md` setiap kali posisi berubah, tambah entri `journal/` tiap sesi (**ditulis sebelum hasil run terlihat** bila membahas ramalan), dan segarkan berkas ini sebelum konteks penuh.

---

## Aturan kerja yang dibayar mahal — jangan pelajari ulang

Delapan aturan pertama dari kesalahan lama; nomor 39–46 lahir di S18–S19 dan **tidak ada di versi berkas ini sebelumnya**.

1. **Pytest hijau sebelum unduhan apa pun.** Gerbang yang bisa gagal ditaruh sebelum langkah panjang.
2. **Modul baru berdiri hijau sendiri lebih dulu, penyambungan menyusul.** Dipakai empat belas kali; terakhir tiga modul Jalur B (779, 795, 811) sebelum workflow-nya dibalik.
3. **Tulis ramalan jumlah pengujian sebelum membaca laporan**, dan cacah dari muatan yang benar-benar dikirim. **Sembilan belas berturut-turut tepat**: … 737, 739, 749, 758, 761, 767, 779, 795, 811.
4. **Blob laporan yang tidak berubah berarti belum ditulis** — bukan berhasil, bukan gagal.
5. **Commit laporan tanpa berkas hasil berarti run GAGAL.**
6. **Baca modulnya sebelum menulis kode terhadapnya, dan baca berkasnya utuh sebelum menulis ulang.** Pembacaan ulang `run_h013.py` di S19 menemukan bahaya yang tidak ditemukan pengujian mana pun: nama laporan yang akan **menimpa** laporan sel AS run `30214203863`, satu-satunya pembanding sah.
7. **Jangan menyunting modul beku** — `run_wf`, `run_h002`, `run_h003`, `run_h007`, `run_h008`, `run_h009`.
8. **Jangan mengimpor ke arah yang bisa menutup siklus.** `lux/analisis` tidak boleh mengimpor `lux/backtest`; itu sebabnya `gabung_h013b.py` berdiri di `lux/backtest` meski pekerjaannya analisis (ADR-030 R5).
9. **Medan `Konfig` baru diletakkan paling akhir dan bawaannya MATI.**
10. **Jangan menulis angka jumlah dengan tangan.** Satu literal tripwire per hal yang dijaga.
11. **Periksa setiap hitungan secara aritmetis dan jangan percaya label buatan sendiri.** "226 jendela / 63,5%" sesungguhnya **194 / 54,5%**. **Cari di repo sebelum memercayai ingatan.**
12. **Keputusan metodologi dikomit sebelum kodenya.** ADR-029 dan ADR-030 mendahului seluruh kode Jalur B.
13. **Ambang pra-registrasi tidak berubah setelah hasil terlihat**, dan sesudah kelulusan ia juga tidak boleh diperketat.
14. **Hipotesis yang ditolak tidak dihitung ulang**, dan tidak dengan mesin maupun satuan yang berbeda.
15. **Rerata bukan ekor. Porsi terhadap nilai bersih bukan konsentrasi. Pencilan bukan sebaran.**
16. **Gerbang yang memberi jawaban sama pada dua keadaan bertolak belakang tidak memuat informasi.**
17. **Aturan yang diketahui bukan aturan yang diterapkan.**
18. **Batas risiko bukan parameter yang dilombakan.** `stop_hormati_celah` adalah sakelar kejujuran, bukan ambang.
19. **Margin sesempit resolusi alat ukur bukan margin.** Diperluas di S19: **"meleset tipis" tetap meleset** — R-A4 meramal p ≤ 0,001 dan nyatanya 0,001100.
20. **Ekspektasi yang naik karena penyebutnya menyusut bukan keunggulan yang lebih besar.**
21. **Kecurigaan harus NAIK ketika hasilnya menyenangkan.** Empat kali di S16–S17 tak berdasar; kelima di S18 atas +0,054842R **berdasar**; keenam di S19 atas p simbol 0,001100 **berdasar**.
22. **Galat baku di bawah andaian kebebasan yang salah hanya boleh menjatuhkan klaim.**
23. **Jangan menuntut kesamaan bit pada agregat pecahan**, dan **kesamaan hasil lintas dua run berbeda dilarang diterima tanpa pemeriksaan**.
24. **Pagar yang memastikan masukan identik tidak memastikan masukan sah.**
25. **Satu simbol dapat mendominasi agregat 438 simbol.** Biaya yang dibagi penyebut mendekati nol adalah biaya tak terbatas.
26. **Himpunan tertahan habis pada saat pertama kali dilihat.**
27. **Cacat yang membalik tanda hasil tidak boleh diperbaiki di dalam hipotesis yang sama.**
28. **Eksperimen yang tercemar tidak informatif ke arah mana pun.**
29. **Saringan yang menolak entri juga menolaknya saat pemilihan parameter.** Tanyakan lebih dulu keadaan mana yang membuat angka sebuah saringan nol.
30. **Jangan pernah menekan hasil negatif, membuang simbol merugi, mematok parameter yang menang belakangan, menurunkan ambang, atau menyebut sistem layak diperdagangkan.**
31. **Pagar yang menyalin baris dari kode yang dijaganya tidak menjaga apa pun.** Pagar wajib membaca dari **definisi** (`dataclasses.fields`) atau **memanggil fungsi yang sama** dengan produksi.
32. **Aritmetika yang hidup di dalam `main` tidak dapat diuji.**
33. **Setiap langkah workflow wajib `tee` ke `logs/` dan seluruh `logs/` disalin ke `reports/` dengan `if: always()`.**
34. **Lingkungan pagar wajib memasang dependensi yang sama dengan `tests.yml`.**
35. **Muatan tulis yang panjang wajib dibaca ulang utuh sebelum dikirim.** Dua commit cacat lahir dari melewatkan ini (`953ce24a`, `2a0f8545`).
36. **Ramalan yang dijamin benar oleh konstruksi bukan ramalan.** Sebelum menghitung sebuah ramalan lulus, tunjukkan keadaan yang membuatnya gagal.
37. **Angka yang benar untuk satu interval tidak berubah nilai ketika dipakai di interval lain — ia berubah MAKNA, dan diam.** Turunkan lewat `lux.kerangka`, tidak pernah dari literal.
38. **Dua definisi atas satu dataset selalu dimenangkan oleh yang tidak terlihat.** Bila dua tempat menghitung hal yang sama, salah satunya wajib memanggil yang lain.
39. **(S18) Angka dapat hidup di berkas konfigurasi tanpa pernah masuk ke dalam program.** Cacat kelas kedelapan; `muat_konfig_h002` memetakan **delapan** kunci dan tidak pernah membaca `maks_biaya_masuk_R` maupun `stop_hormati_celah`. **Kode wajib dibandingkan terhadap berkas, bukan hanya dibaca.**
40. **(S18, ADR-024) Putusan yang dihitung dari separuh kriteria pra-registrasi adalah putusan palsu, dan ia paling berbahaya ketika angkanya menyenangkan.** Cacat kelas kesembilan — inilah keadaan medan `lulus` H-013.
41. **(S18, ADR-024) Prosa kesimpulan yang dipatok di dalam kode bukan kesimpulan.** Cacat kelas kesepuluh; **DITUTUP** di `b0e79220` oleh `prosa_kontribusi` yang menurunkan kalimatnya dari tanda dan urutan besaran.
42. **(S19, ADR-025) Gerbang yang tidak mungkin lulus tidak menjaga apa pun, dan ia terlihat seperti gerbang yang bekerja.** Cacat kelas kesebelas. **Setiap kegagalan gerbang wajib diperiksa apakah ia mungkin lulus sama sekali; kegagalan yang mustahil dihindari bukan temuan, melainkan cacat.**
43. **(S19, ADR-026) Rencana analisis wajib diperiksa terhadap struktur berkas laporan sebelum dijadwalkan.** ADR-024 menjadwalkan uji atas "4.082 jendela" padahal `per_simbol.jendela` adalah **cacah**. Bentuk kekeliruannya berulang di rancangan Jalur B pertama (`bulan_dengan_trade` juga cacah): **saya menganggap angka tersedia karena namanya muncul.**
44. **(S19, ADR-028) Ambang statistik tanpa satuan penarikan bukan ambang.** Cacat kelas kedua belas: galat bakunya dapat dikecilkan **hanya dengan menambah simbol**. Satuan resmi kini **bulan kalender UTC**.
45. **(S19, ADR-028) `p` sah hanya untuk MENJATUHKAN, tidak untuk MENEGAKKAN.** Peringatan "galat baku adalah taksiran bawah" sudah tercetak sejak ADR-013 dan tetap dilewati setiap kali angkanya menyenangkan — karena ia peringatan, bukan aturan.
46. **(S19) Ramalan saya tepat ketika menyangkut kode saya sendiri dan meleset ketika menyangkut pasar.** Sembilan belas ramalan cacah uji berturut tepat; dari sebelas ramalan angka H-013, **sembilan meleset**. **Sebelum membekukan ramalan angka, sebutkan asumsi yang menopangnya dan tandai mana yang belum diperiksa.**
47. **(S19, ADR-030) Alat yang selalu menghasilkan angka tidak menjaga apa pun.** Penggabung Jalur B menolak melahirkan putusan dalam empat keadaan, dan penolakan yang paling penting adalah **himpunan bulan yang tidak sama**: memotong ke irisan akan menghasilkan `p` yang tampak waras atas dua himpunan berbeda **tanpa satu pun tanda di laporannya**. Penyelarasan hanya lewat keputusan tertulis, bukan sebagai kelakuan bawaan sebuah fungsi.
48. **(S19, ADR-030) Hasil yang menjatuhkan hipotesis wajib berkode keluar 0.** Menandainya merah menciptakan dorongan tetap untuk mengutak-utik sampai papan hijau — dorongan yang menjadi asal seluruh pengetahuan yang sudah dibuang dari upaya sebelumnya.
