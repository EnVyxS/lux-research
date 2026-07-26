# Prompt kelanjutan — tempel ini di sesi baru

> Disegarkan 2026-07-27 04:10 WIB, sesudah commit `49782044` (**819 pengujian lulus**; ADR-025 s.d. ADR-031 selesai; **Jalur B SELESAI dan H-013 DITOLAK**).
> Berkas ini hanya jembatan. **Sumber kebenaran tunggal tetap `STATE.md`** (versi **26**, 51 aturan bernomor).

---

## Tempel mulai dari sini

Sebelum melakukan apa pun, baca `STATE.md` di repositori GitHub publik **EnVyxS/lux-research**, lalu berkas ini. **Jangan membaca `journal/` secara utuh** — hanya bila ada rujukan spesifik; entri terakhir `journal/2026-07-27-27.md`. Lanjutkan dari titik terakhir; jangan mulai dari awal dan jangan mengulang pekerjaan yang sudah selesai.

**TIDAK ADA RUN YANG BERJALAN.** Tidak ada yang perlu diperiksa statusnya sebelum bekerja — posisi terakhir sudah tuntas terverifikasi sampai commit `49782044` (STATE v26). Bila ragu, `list_commits` dengan `perPage: 5` cukup untuk memastikan HEAD.

### Konteks

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang karena tercemar survivorship bias dan overfitting. Mesin lokal tidak sanggup backtest penuh dan tidak ada VM cloud, jadi **seluruh komputasi berjalan di GitHub Actions** dan repo GitHub adalah penyimpanan data sekaligus jurnal riset.

### Batas alat yang harus dipahami sejak awal

- Sandbox agen **tidak punya jaringan**. Semua pengambilan data terjadi di runner Actions.
- Agen **tidak bisa membaca log workflow**, dan daftar alat GitHub **tidak memuat satu pun fungsi Actions**. Diverifikasi ulang di S20. Solusinya: setiap workflow menulis hasil ke `reports/` lalu commit balik.
- Agen **tidak bisa memicu workflow manual**. Setiap workflow punya filter `paths` pada berkasnya sendiri, jadi push ke berkas itu yang memicunya. `tests.yml` memfilter `lux/**` dan `tests/**` — jadi perubahan pada `config/`, `journal/`, `decisions/`, `STATE.md`, dan berkas ini **tidak** memicu pengujian, dan ramalan cacah atas commit semacam itu **tidak dapat diadili**.
- **Dua dorongan berurutan ke `lux/**` melahirkan DUA run `tests.yml`**, dan keduanya wajib diadili terpisah. Laporan run yang lebih dulu **tertimpa** oleh run berikutnya di `main`, tetapi masih terbaca dengan `get_file_contents` memakai **SHA commit laporan itu** (aturan 51).
- Sepuluh pekerjaan yang mengomit ke satu cabang menuntut **lingkaran ulang dorong**. `git pull --rebase --autostash` sekali — pola yang lulus di dua belas workflow lain — tidak cukup pada matriks; yang kalah lomba **hilang tanpa suara** lalu menyamar sebagai cakupan data yang bolong. `h013b.yml` mengulang sampai sepuluh kali dengan jeda acak.
- Pekerjaan matriks yang bergantung pada keluaran pekerjaan lain **wajib `git fetch` + `git checkout origin/main -- reports`**. Checkout bawaan berada pada SHA pemicu, yang **mendahului** seluruh commit pecahan.
- Agen tidak bisa membuat atau mengunggah rilis; runner melakukannya lewat `gh release upload`.
- REST `fapi.binance.com` mengembalikan **HTTP 451** dari runner. CDN `data.binance.vision` normal.
- `search_code` **nol hasil di repo ini**. Baca berkas langsung.
- `get_file_contents` menuntut SHA 40 karakter penuh **atau** nama branch; `ref: "main"` bekerja dan itu cara termurah mengambil versi berlaku. Pada **direktori** ia memberi ukuran berkas — itulah cara mengadili ramalan ukuran tanpa menarik isinya.
- Untuk menulis, **pakai `push_files`**: `{ toolName, toolArguments: { owner, repo, branch, message, files } }` — jangan menaruh `owner`/`repo`/`branch` di tingkat atas.
- **`push_files` mengganti seluruh isi berkas.** Baca berkas utuh sebelum menulis ulang; untuk berkas panjang salin hasil bacaan apa adanya lalu sunting hanya bagian yang dituju. Teks Python di repo ini memuat escape Unicode literal (`\u00b7`, `\u2014`) dan f-string berkutip bersarang.
- Runner tidak punya `scipy` dan tidak punya `requests`. Statistik memakai numpy; HTTP memakai `urllib.request`.
- **Kabar buruk datang dalam 23–32 detik; kabar baik 10–45 menit** — kecuali `tests.yml`, yang memberi kabar **baik** dalam ~23 detik juga. Jangan membaca cepatnya laporan uji sebagai kegagalan; **baca isinya**.
- **Commit laporan tanpa berkas hasil = run GAGAL. Blob laporan yang SHA-nya tidak berubah = belum ditulis.** Berkas yang belum lahir memberi "path does not point to a file", dan itu **bukan** galat alat.
- **`backfill_daily.yml` berjadwal mingguan** (`cron: '0 2 * * 1'`), jadi tidak setiap perubahan blob berasal dari saya.
- Analisis atas laporan yang sudah dikomit bisa dikerjakan di sandbox tanpa jaringan. **Begitulah cacat terbesar riset ini ditemukan** — bukan oleh run baru, melainkan dengan menghitung ulang `per_simbol` sendiri.

### Posisi sekarang, ringkas

- **TIGA BELAS hipotesis dinilai, TIGA BELAS DITOLAK. Nol kandidat bertahan.** Yang pernah "lulus" (H-010) lulus pada 100 permutasi dan gagal pada 300 (p 0,0631).
- **H-013 DITOLAK (ADR-031).** Run `30217516013` menghitung untuk **pertama kalinya dalam tiga belas hipotesis** kedua syarat ADR-015 §4.4 atas run yang sama: besaran SS − AS **+0,054842R ≥ 0,020R** terpenuhi, tetapi **p = 0,205980 pada satuan bulan > 0,05** GAGAL, atas 300 ulangan dengan trade terkecil 54.812. Berkas putusan satu-satunya: `reports/h013b_p.json`.
- **Temuan terpenting bukan putusannya, melainkan satuannya.** Run yang sama memberi **p 0,003322 per perdagangan** dan **0,205980 per bulan** — faktor 62, arah berlawanan. Yang membuat satuan bulan sah bukan besarnya melainkan bahwa ADR-028 membekukannya **sebelum** kedua angka ini ada. **Bila satuan boleh dipilih sesudah hasil terlihat, H-013 lulus hari ini.**
- **Jalur A membenarkannya dengan mesin berbeda:** uji tanda berpasangan bulanan p **0,365363**, bootstrap 95% **[−0,027040, +0,073620]R memuat nol**. Pada tingkat simbol p kecil (0,001100), tetapi satuan resminya bulan.
- **Cacat kelas ketiga belas (aturan 49):** besaran +0,054842R diukur terhadap **satu** undian nol (AS seed 42, +0,011806R) yang ternyata ~0,98 simpangan baku **di bawah** rerata sebaran nol +0,022916R. Terhadap rerata nol besarannya **+0,043732R**, dua puluh persen lebih kecil. Putusan tidak berubah; angka yang dikutip selama ini terlalu bagus. **Sejak `6ae83062` aturan ini dijalankan oleh alat, bukan oleh niat.**
- **Anomali SH < AH TURUN PANGKAT menjadi derau** (p 0,777622 dan 0,280372, bootstrap memuat nol di dua tingkat). Ia bukan temuan dan tidak menuntut penjelasan.
- **819 pengujian lulus**, laporan pada commit `7aa761ec`, run `30219885271`.

### Empat berkas Jalur B dan perannya

| Berkas | Peran | Commit |
|---|---|---|
| `lux/analisis/sebaran_nol.py` | aritmetika `p`; `p_bulanan` **mengikat**, `p_per_perdagangan` **taksiran bawah** | `05df8b78` (779) |
| `lux/backtest/run_h013b.py` | satu pecahan 30 seed; `NAMA_SPEK="h013b_as_seed"`; gerbang `entri_acak` MATI | `4f09c8d5` (795) |
| `lux/backtest/gabung_h013b.py` | **satu-satunya berkas yang boleh melahirkan putusan H-013**; sejak `6ae83062` ia juga menegakkan aturan 49 dan 50 | `0859e8dd` (811) → `6ae83062` → `5bd73fbf` (819) |
| `.github/workflows/h013b.yml` | matriks 10 pecahan + penggabung; menyentuhnya memulai sebelas pekerjaan | `97b36c19` |

**Penggabung MENOLAK melahirkan putusan dalam empat keadaan** (ADR-030): cakupan seed tidak utuh; himpunan bulan antar seed dan sel SS berbeda (kode keluar 4, laporan tetap ditulis); pecahan tidak menyatakan gerbang mati; R-D5 tidak terbukti. **DITOLAK berkode keluar 0** — run yang menjatuhkan hipotesis bekerja dengan benar.

### Ramalan yang SUDAH teradili di S20 — jangan diadili ulang

| Kode | Isi | Putusan |
|---|---|---|
| R-B2 / R-C1 | per-perdagangan p ≤ 0,05 tetapi menyesatkan (0,003322) | TEPAT |
| R-B3 / R-C2 | satuan bulan p > 0,05 sehingga H-013 DITOLAK (0,205980) | TEPAT |
| R-C3 | selisih dua satuan lebih dari satu orde besaran (faktor 62) | TEPAT |
| R-D1 | satu pecahan selesai < 40 menit | **MELESET** (43 menit 2 detik; tipis tetap meleset) |
| R-D2 | satu pecahan < 1 MB (370,5 kB) | TEPAT |
| R-D3 | ≥ 1 seed melampaui +0,0666R | **MELESET** (tertinggi +0,057394R), **dan alasannya ikut terbantah**: permutasinya sehat, +0,066648R terletak ~3,8 simpangan baku di atas rerata nol |
| R-D4 | simpangan baku antar seed > 0,005570R (0,011377R) | TEPAT |
| R-D5 | seed 42 mereproduksi +0,01180570125176449R | TEPAT |
| R-E1a / R-E1b | cacah uji 819 untuk `5bd73fbf`, 811 untuk `6ae83062` | TEPAT keduanya |

### Ramalan beku yang MASIH belum teradili — jangan menulis ramalan baru sesudah angkanya terlihat

| Kode | Isi |
|---|---|
| R-B1 | run 4h pertama sesudah ADR-025 melapor `checksum` "tidak dapat dinilai"; run kedua **lulus** dengan dua belas `ohlcv_4h_*` |
| R-B4 | pemasangan bulanan **berbobot trade** tetap p > 0,05 (Jalur B tidak menghitung varian berbobot) |
| ADR-016 ramalan 5 | ekspektasi R dengan `stop_hormati_celah` menyala lebih rendah daripada dengan medan mati |

### Tindakan berikutnya, urutannya wajib

1. **Uji geometri keluar SENDIRI dengan mesin p bulanan** (SS − SH = +0,029481R). Mesinnya sudah ada dan belum pernah diarahkan ke sana; tanpa itu "pemisahan sinyal dari geometri keluar" hanya separuh dijawab. **Pra-registrasi dikomit lebih dulu** (keputusan metodologi mendahului kode), besaran wajib dilaporkan **dua kali** — terhadap sel pembanding dan terhadap rerata sebaran nol (aturan 49).
2. **Baca `reports/backtest_h013_ss_sinyal_stop.json`** untuk nilai `invarian_risiko` SS — lewat skrip sisi runner yang mencetak ringkasan ke `reports/`, **jangan** menarik 432 KB ke konteks. Pada H-013 `stop_hormati_celah` menyala dan gerbang itu **tetap gagal di keempat sel**, jadi kebutaan celah bukan penjelasannya dan besarnya belum dibaca.
3. **Selesaikan pertanyaan bar datar 1h lawan 4h:** bandingkan `reports/diag_datar.json` terhadap perhitungan 4h. Bar 4h datar hanya bila keempat bar 1h datar, jadi penolakan 4h semestinya **≤ 74**. Angka 74 yang identik pada dua interval belum berarti cacat, tetapi belum berpenjelasan.
4. **Nasib `notion_asap.yml`** (`git push` polos, `git commit || echo` yang menelan kegagalan) dan **`backfill_daily.yml`** (cron mingguan + `--clobber`, mengancam ADR-025 R4). Perbaiki atau hapus **dengan keputusan tertulis**. Tinjau juga `funding.yml`, `funding_check.yml` (keduanya masih memakai `reports/universe_layak.json` pra-lantai), `doctor.yml`, `universe.yml`. **Jangan hapus tanpa keputusan tertulis.**
5. **Program riset lanjutan: funding sebagai SINYAL** — satu-satunya dimensi bersih yang tersisa, belum pernah diuji sekali pun, datanya sudah ada di rilis `tier-b-v1`. **Pra-registrasi lengkap wajib ditulis dan dikomit sebelum satu baris kode**, dengan **p bulanan sebagai gerbang** (ADR-031 keputusan 5). ADR-015 §4.5 butir 5 tampak terbalik dan §6 sudah berjanji mengakuinya.
6. **Utang teknis:** sambungkan `maks_rasio_bar_datar` config ke gerbang · periksa kunci config lain yang tak pernah dibaca (aturan 39) · bandingkan `runner.py` terhadap blob `fc79e070` dan `run_h013.py` terhadap `418f6084` untuk pergeseran prosa komentar · `hasattr`/`__import__` di `test_run_h012.py` · pengujian `biaya_bolak_balik_R` · `pytest` ke `requirements-dev.txt` · tripwire tekstual `inspect.getsource` (lemah, dicatat sebagai lemah) · pemetaan `dari_laporan` pelapor Notion · perketat `lux/funding.py::gerbang_lulus` · salin ADR-001/ADR-002 ke `decisions/` · naikkan `versi` config sesudah seluruh pembacanya diperiksa.
7. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, dengan ≥24 shard.

**Sudah lunas, jangan dikerjakan ulang:** modul degenerasi · pengaman biaya masuk · perambatan walk-forward · lantai semesta · agregat per bulan · `sebaran.py` · `geometri_keluar.py` · pelapor Notion · `stop_hormati_celah` · `validate`/`potong_ekor` berinterval · `lux/kerangka.py` · ADR-019 · **audit empat belas workflow** · **ADR-025 manifest per interval** (`fb128c93` + `43cd4eed`) · **Jalur A** · **ADR-028 satuan penarikan** · **`prosa_kontribusi`** · **ketiga modul Jalur B** · **run Jalur B dan adjudikasinya (ADR-031)** · **koreksi prosa R-D3 dan pemasangan aturan 49 ke alat** (`6ae83062` + `5bd73fbf`).

**DIBATALKAN atas keputusan pengguna:** agen **LUX Gatekeeper** dan **LUX Gatekeeper Reporter** tidak dipakai lagi. Kolom `Verdict` di database Notion **LUX — Run Results** menjadi kolom **manusia**.

### Godaan yang wajib ditolak

**+0,060163R** (H-010 tanpa USDCUSDT) dan **+0,059636R** (H-012 seluruh riwayat) haram dipakai sebagai kelulusan — keduanya pemilihan pasca-hasil. **+0,054842R**, **+0,043732R**, dan **+0,066648R** haram dikutip sebagai kelulusan atau kelayakan H-013; **+0,054842R juga haram dikutip sebagai besaran apa pun tanpa menyebut seed 42**. Kata **LULUS** pada `backtest_h013_kontribusi.md` haram dikutip. **p 0,001100 tingkat simbol** haram dikutip sebagai keberartian. **Setiap p atau galat baku per perdagangan** haram dipakai sebagai bukti keberartian, termasuk **0,003322** dan "+2,99 galat baku". **Prosa R-D3 di `reports/h013b_p.md` haram dipakai sebagai penilaian atas kesehatan permutasi** — ia terbantah dan sengaja tidak ditulis ulang.

**Dilarang memilih satuan penarikan sesudah hasil terlihat.** **Dilarang menyebut H-012 atau H-013 "H-010 setelah perbaikan".** **Dilarang menandai putusan DITOLAK sebagai kegagalan pekerjaan.** Dilarang menyatakan sistem siap dagang.

### Cara saya ingin kamu bekerja

- Ketika saya menulis "lanjut", teruskan langsung dari titik terakhir tanpa konfirmasi dan tanpa mengulang penjelasan.
- **Pisahkan fakta terverifikasi dari asumsi.** Asumsi naik jadi fakta hanya dengan commit, run ID, atau kutipan sumber.
- Katakan bila saya salah, dan katakan bila kamu sendiri salah — jangan menghaluskan ramalan yang meleset.
- Perbarui `STATE.md` setiap kali posisi berubah, tambah entri `journal/` tiap sesi (**ditulis sebelum hasil run terlihat** bila membahas ramalan), dan segarkan berkas ini sebelum konteks penuh.

---

## Aturan kerja yang dibayar mahal — jangan pelajari ulang

Delapan aturan pertama dari kesalahan lama; nomor 39–51 lahir di S18–S20. Daftar bernomor lengkap ada di `STATE.md` bagian 1 (**51 aturan**) dan itulah versi yang mengikat.

1. **Pytest hijau sebelum unduhan apa pun.** Gerbang yang bisa gagal ditaruh sebelum langkah panjang.
2. **Modul baru berdiri hijau sendiri lebih dulu, penyambungan menyusul.** Dipakai empat belas kali; terakhir tiga modul Jalur B (779, 795, 811) sebelum workflow-nya dibalik.
3. **Tulis ramalan jumlah pengujian sebelum membaca laporan**, dan cacah dari muatan yang benar-benar dikirim. **Dua puluh satu berturut-turut tepat**: … 737, 739, 749, 758, 761, 767, 779, 795, 811, 811, 819.
4. **Blob laporan yang tidak berubah berarti belum ditulis** — bukan berhasil, bukan gagal.
5. **Commit laporan tanpa berkas hasil berarti run GAGAL.**
6. **Baca modulnya sebelum menulis kode terhadapnya, dan baca berkasnya utuh sebelum menulis ulang.** Pembacaan ulang `runner.py` di S20 menemukan bahaya yang tidak ditemukan pengujian mana pun: nama laporan yang akan **menimpa** laporan sel AS run `30214203863`, satu-satunya pembanding sah.
7. **Jangan menyunting modul beku** — `run_wf`, `run_h002`, `run_h003`, `run_h007`, `run_h008`, `run_h009`.
8. **Jangan mengimpor ke arah yang bisa menutup siklus.** `lux/analisis` tidak boleh mengimpor `lux/backtest`; itu sebabnya `gabung_h013b.py` berdiri di `lux/backtest` meski pekerjaannya analisis (ADR-030 R5).
9. **Medan `Konfig` baru diletakkan paling akhir dan bawaannya MATI.**
10. **Jangan menulis angka jumlah dengan tangan.** Satu literal tripwire per hal yang dijaga.
11. **Periksa setiap hitungan secara aritmetis dan jangan percaya label buatan sendiri.** "226 jendela / 63,5%" sesungguhnya **194 / 54,5%**. **Cari di repo sebelum memercayai ingatan.**
12. **Keputusan metodologi dikomit sebelum kodenya.** ADR-029 dan ADR-030 mendahului seluruh kode Jalur B.
13. **Ambang pra-registrasi tidak berubah setelah hasil terlihat**, dan sesudah kelulusan ia juga tidak boleh diperketat.
14. **Hipotesis yang ditolak tidak dihitung ulang**, dan tidak dengan mesin, satuan, maupun aturan besaran yang berbeda.
15. **Rerata bukan ekor. Porsi terhadap nilai bersih bukan konsentrasi. Pencilan bukan sebaran.**
16. **Gerbang yang memberi jawaban sama pada dua keadaan bertolak belakang tidak memuat informasi.**
17. **Aturan yang diketahui bukan aturan yang diterapkan.** Karena itu aturan 49 dan 50 dipasang ke dalam `gabung_h013b.py` sebagai medan dan pengujian, bukan sebagai catatan.
18. **Batas risiko bukan parameter yang dilombakan.** `stop_hormati_celah` adalah sakelar kejujuran, bukan ambang.
19. **Margin sesempit resolusi alat ukur bukan margin.** Diperluas di S20: **R-D1 meleset tiga menit dua detik dan tetap dicatat MELESET.**
20. **Ekspektasi yang naik karena penyebutnya menyusut bukan keunggulan yang lebih besar.**
21. **Kecurigaan harus NAIK ketika hasilnya menyenangkan.** Empat kali di S16–S17 tak berdasar; kelima di S18 atas +0,054842R **berdasar**; keenam di S19 atas p simbol 0,001100 **berdasar**; ketujuh di S20 atas p per-perdagangan 0,003322 **berdasar**.
22. **Galat baku di bawah andaian kebebasan yang salah hanya boleh menjatuhkan klaim.**
23. **Jangan menuntut kesamaan bit pada agregat pecahan**, dan **kesamaan hasil lintas dua run berbeda dilarang diterima tanpa pemeriksaan**.
24. **Pagar yang memastikan masukan identik tidak memastikan masukan sah.**
25. **Satu simbol dapat mendominasi agregat 438 simbol.** Biaya yang dibagi penyebut mendekati nol adalah biaya tak terbatas.
26. **Himpunan tertahan habis pada saat pertama kali dilihat.**
27. **Cacat yang membalik tanda hasil tidak boleh diperbaiki di dalam hipotesis yang sama.**
28. **Eksperimen yang tercemar tidak informatif ke arah mana pun.**
29. **Saringan yang menolak entri juga menolaknya saat pemilihan parameter.**
30. **Jangan pernah menekan hasil negatif, membuang simbol merugi, mematok parameter yang menang belakangan, menurunkan ambang, atau menyebut sistem layak diperdagangkan.**
31. **Pagar yang menyalin baris dari kode yang dijaganya tidak menjaga apa pun.** Pagar wajib membaca dari **definisi** (`dataclasses.fields`) atau **memanggil fungsi yang sama** dengan produksi.
32. **Aritmetika yang hidup di dalam `main` tidak dapat diuji.**
33. **Setiap langkah workflow wajib `tee` ke `logs/` dan seluruh `logs/` disalin ke `reports/` dengan `if: always()`.**
34. **Lingkungan pagar wajib memasang dependensi yang sama dengan `tests.yml`.**
35. **Muatan tulis yang panjang wajib dibaca ulang utuh sebelum dikirim.** Dua commit cacat lahir dari melewatkan ini (`953ce24a`, `2a0f8545`).
36. **Ramalan yang dijamin benar oleh konstruksi bukan ramalan.** Sebelum menghitung sebuah ramalan lulus, tunjukkan keadaan yang membuatnya gagal.
37. **Angka yang benar untuk satu interval tidak berubah nilai ketika dipakai di interval lain — ia berubah MAKNA, dan diam.** Turunkan lewat `lux.kerangka`, tidak pernah dari literal.
38. **Dua definisi atas satu dataset selalu dimenangkan oleh yang tidak terlihat.**
39. **(S18) Angka dapat hidup di berkas konfigurasi tanpa pernah masuk ke dalam program.** Cacat kelas kedelapan; `muat_konfig_h002` memetakan **delapan** kunci saja. **Kode wajib dibandingkan terhadap berkas, bukan hanya dibaca.**
40. **(S18, ADR-024) Putusan yang dihitung dari separuh kriteria pra-registrasi adalah putusan palsu**, dan ia paling berbahaya ketika angkanya menyenangkan. Cacat kelas kesembilan — inilah keadaan medan `lulus` H-013, dan ia baru diganti oleh `reports/h013b_p.json`.
41. **(S18, ADR-024) Prosa kesimpulan yang dipatok di dalam kode bukan kesimpulan.** Cacat kelas kesepuluh; **DITUTUP** di `b0e79220`.
42. **(S19, ADR-025) Gerbang yang tidak mungkin lulus tidak menjaga apa pun, dan ia terlihat seperti gerbang yang bekerja.** Cacat kelas kesebelas.
43. **(S19, ADR-026) Rencana analisis wajib diperiksa terhadap struktur berkas laporan sebelum dijadwalkan.** Bentuk kekeliruannya berulang: **saya menganggap angka tersedia karena namanya muncul.**
44. **(S19, ADR-028) Ambang statistik tanpa satuan penarikan bukan ambang.** Cacat kelas kedua belas. Satuan resmi **bulan kalender UTC**. **Dibuktikan telanjang di S20:** satu run, p 0,003322 lawan 0,205980.
45. **(S19, ADR-028) `p` sah hanya untuk MENJATUHKAN, tidak untuk MENEGAKKAN.**
46. **(S19) Ramalan saya tepat ketika menyangkut kode saya sendiri dan meleset ketika menyangkut pasar.** Dua puluh satu ramalan cacah uji berturut tepat; dari sebelas ramalan angka H-013 sembilan meleset, dari lima ramalan Jalur B dua meleset. **Sebelum membekukan ramalan angka, sebutkan asumsi yang menopangnya dan tandai mana yang belum diperiksa.**
47. **(S19–S20, ADR-030) Alat yang selalu menghasilkan angka tidak menjaga apa pun.** Penggabung menolak melahirkan putusan dalam empat keadaan; penolakan terpenting adalah **himpunan bulan yang tidak sama**. Berhenti adalah keluaran yang sah.
48. **(S20, ADR-030) Hasil yang menjatuhkan hipotesis wajib berkode keluar 0.** Merah hanya untuk mesin yang rusak, bukan untuk hipotesis yang mati.
49. **(S20, ADR-031) Besaran tidak boleh diukur terhadap satu undian nol.** Wajib dilaporkan juga terhadap **rerata** sebaran nol; besaran terhadap satu seed hanya boleh dikutip bila nomor seed-nya ikut ditulis. Dijalankan oleh `ringkas()` sejak `6ae83062`.
50. **(S20, ADR-031) Ramalan yang terbukti salah alasannya dikoreksi sebagai PROSA di sumbernya, dan jejak bunyi aslinya tidak dihapus.** Laporan yang sudah dikomit tidak ditulis ulang untuk menutupi ramalan yang meleset. `BUNYI_ASLI_R_D3` menyimpan bunyi terbantah verbatim dan satu pengujian menuntutnya tetap ada.
51. **(S20) Sumber dan pagarnya adalah satu commit.** `6ae83062` mengubah `gabung_h013b.py` tanpa membawa pengujiannya, padahal pesan commit itu sendiri meramalkan 819; `main` sempat memuat alat yang belum dijaga dan pesan commit membantah dirinya sendiri. **Ramalan cacah wajib menyebut commit mana yang diramalkan.**
