# Prompt kelanjutan — tempel ini di sesi baru

> Disegarkan 2026-07-27 00:50 WIB, sesudah commit `f12e6bd3` (**714 pengujian lulus**; ADR-017, ADR-018, dan ADR-019 selesai seluruhnya).
> Berkas ini hanya jembatan. **Sumber kebenaran tunggal tetap `STATE.md`** (versi 22).

---

## Tempel mulai dari sini

Sebelum melakukan apa pun, baca `STATE.md` di repositori GitHub publik **EnVyxS/lux-research**, lalu berkas ini. `STATE.md` (versi 22) adalah satu-satunya sumber kebenaran tentang posisi riset. **Jangan membaca `journal/` secara utuh** — hanya bila ada rujukan spesifik. Lanjutkan dari titik terakhir; jangan mulai dari awal dan jangan mengulang pekerjaan yang sudah selesai.

Selama proses, pastikan tidak ada error. Sebelum menjalankan workflow berikutnya, periksa kembali workflow sebelumnya untuk memastikan semuanya berjalan benar — ada kemungkinan error terlewat, atau ada workflow yang sudah tidak diperlukan sehingga sebaiknya dihapus agar repo tetap bersih.

### Konteks

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang karena tercemar survivorship bias dan overfitting. Mesin lokal tidak sanggup backtest penuh dan tidak ada VM cloud, jadi **seluruh komputasi berjalan di GitHub Actions** dan repo GitHub adalah penyimpanan data sekaligus jurnal riset.

### Batas alat yang harus dipahami sejak awal

- Sandbox agen **tidak punya jaringan**. Semua pengambilan data terjadi di runner Actions.
- Agen **tidak bisa membaca log workflow**, dan daftar alat GitHub **tidak memuat satu pun fungsi Actions**. Diverifikasi ulang di S16. Solusi yang berjalan: setiap workflow menulis hasil ke `reports/` lalu commit balik; agen membacanya lewat API biasa.
- Agen **tidak bisa memicu workflow manual**. Setiap workflow punya filter `paths` pada berkasnya sendiri, jadi push ke berkas itu yang memicunya. `tests.yml` memfilter `lux/**` dan `tests/**` — jadi perubahan pada `config/`, `journal/`, `decisions/`, dan `STATE.md` **tidak** memicu pengujian, dan ramalan jumlah uji atas commit semacam itu **tidak dapat diadili**.
- Agen tidak bisa membuat atau mengunggah rilis; runner melakukannya lewat `gh release upload`.
- REST `fapi.binance.com` mengembalikan **HTTP 451** dari runner. Jangan taruh di jalur kritis. CDN `data.binance.vision` normal.
- `search_code` **nol hasil di repo ini**. Baca berkas langsung.
- `get_file_contents` menuntut SHA 40 karakter penuh **atau** nama branch; `ref: "main"` bekerja dan itu cara termurah mengambil versi berlaku.
- Untuk menulis, **pakai `push_files`**, bukan `create_or_update_file`. Bentuk argumennya `{ toolName, toolArguments: { owner, repo, branch, message, files } }` — jangan menaruh `owner`/`repo`/`branch` di tingkat atas.
- **`push_files` mengganti seluruh isi berkas.** Karena itu **baca berkas utuh sebelum menulis ulang**, dan untuk berkas panjang salin teks hasil bacaan apa adanya lalu sunting hanya bagian yang dituju. Teks sumber Python di repo ini memuat escape Unicode literal (`\u00b7`, `\u2014`) dan f-string berkutip bersarang; menyalin bentuk escaped-nya apa adanya jauh lebih aman daripada mengetik ulang.
- Runner tidak punya `scipy` dan tidak punya `requests`. Statistik memakai numpy; HTTP memakai `urllib.request`.
- Analisis atas laporan yang sudah dikomit bisa dikerjakan di sandbox tanpa jaringan. **Begitulah cacat terbesar riset ini ditemukan** — bukan oleh run baru, melainkan dengan menghitung ulang `per_simbol` sendiri.

### Posisi sekarang, ringkas

- **Dua belas hipotesis: sebelas DITOLAK.** Yang satu (H-010) lulus pada 100 permutasi dan **gagal pada 300** (p 0,0631), jadi ia tidak direhabilitasi.
- **H-012 DITOLAK**, run `30200123505`, sidik `75f9c7ccd65ec30f`. Kriteria utama: ekspektasi periode tahan-waktu **+0,041713R** atas 22.117 perdagangan, di bawah ambang 0,05R. Tiga gerbang gagal: `entri_acak` p **0,06312292358803986**, `invarian_risiko` **−21,3131R**, `funding_ekor` `funding_maks_R` **0,6601**. **Ramalan saya bahwa H-012 gagal, ditulis sebelum run, benar.**
- **Temuan yang lebih penting daripada vonis itu:** mesin **buta terhadap celah harga pada jalur stop** — `harga = stop if kena_stop else target`, harga bar tidak pernah dipakai. Akibatnya `invarian_risiko` praktis tak berdaya pada jalur stop, dan **seluruh dua belas hipotesis dinilai oleh mesin yang optimistis terhadap risiko celah**. Arah biasnya melawan penolakan, jadi **tidak ada vonis yang perlu dibalik**, tetapi **tidak satu pun angka R lama boleh disebut konservatif**. Perbaikannya terpasang bawaan MATI (`stop_hormati_celah`) dan **hasil lama tidak dihitung ulang**.
- **Himpunan tertahan HABIS.** Hasil per simbol 438 simbol sudah dilihat (H-011) dan tabel 73 bulan sudah dilihat (H-012). Dimensi yang masih bersih: **kerangka 4h** — yang kini siap — dan **pemisahan sinyal dari geometri keluar**.
- **714 pengujian lulus**, laporan pada commit `409343f3`.

### Kerangka 4h sudah siap — dan jalan menuju ke sana memuat lima cacat sejenis

ADR-017, ADR-018, ADR-019 selesai. Semesta 4h berdiri sendiri: **447 valid** (run `30211176709`), **438 layak** sesudah ekor datar dipangkas (run `30211673239`, 141 simbol berekor, 270.398 bar dipangkas). Keduanya **identik simbol per simbol dengan 1h**, dan kesamaan itu **diperiksa**, bukan disyukuri.

Lima cacat yang ditemukan, semuanya berbentuk konstanta bar yang mengaku sebagai satuan waktu, dan **tidak satu pun berbunyi sebagai galat**:

1. `validate_run` menulis `universe_layak.json` tanpa interval → keluaran 4h menimpa masukan 1h (`02933b85`).
2. `muat_ambang` membaca `min_bar_1h` untuk interval apa pun (`fe7fd30e`).
3. `MIN_PANJANG`/`MIN_BAR` buta interval di `potong_ekor` (`6aacef40`).
4. Keluaran `potong_ekor` 4h menimpa masukan backtest 1h (`6aacef40` + pagar `5296162d`).
5. **`muat_ohlcv` memangkas ekor dengan ambang 1h** (`409343f3`) — yang paling berbahaya, sebab ia tidak meninggalkan jejak: laporan mencetak semesta 438 yang benar sementara mesin memperdagangkan bar yang menurut semesta itu sudah tidak ada.

Sekarang aritmetika "satu hari berapa bar" hanya hidup di satu tempat: **`lux/kerangka.py`**, modul daun yang tidak mengimpor apa pun dari `lux` — syarat mutlak, sebab rantai `gerbang → potong_ekor → diag_datar → run_wf → gerbang` sudah pernah melahirkan impor sirkular (`4b77617`).

### Utang yang wajib diketahui sebelum menyentuh gerbang bar datar

`config/lux.yaml` memuat `universe.maks_rasio_bar_datar: 0.30`, tetapi **gerbang backtest tidak pernah membacanya**. Angka itu hidup sebagai bawaan fungsi di `gerbang.py` dan literal di `runner.py`/`run_wf.py`. **Menyuntingnya di config tidak mengubah perilaku apa pun, sementara laporan tetap mencetak 0,30 dan tampak konsisten.** Dicatat sebagai utang, sengaja tidak diperbaiki di ADR-019 karena menyambungkannya dapat mengubah perilaku sebelas hipotesis lama.

Juga masih berdiri: `MAKS_RASIO_DATAR = 0.10` dipakai untuk kedua interval, padahal rasio bar datar 4h mekanis lebih kecil — gerbang itu **lebih longgar** di 4h. Karena itu **nilai gerbang bar datar 4h haram dikutip sebagai bukti kebersihan data**, dan menggesernya sesudah melihat hasil 4h melanggar aturan 13.

### Tindakan berikutnya, urutannya wajib

1. **Modul H-013** (ADR-015 Bagian B / ADR-016 langkah 4): empat sel SS/SH/AS/AH, `h=48` bar 4h, ambang **SS − AS ≥ 0,020R**, p ≤ 0,05, ≥300 ulangan, ≥100 trade per sel. Mekanisme diimpor **tanpa perubahan** dari `run_h010`/`run_h009`; `stop_hormati_celah` menyala; masukan `reports/universe_layak_v2_4h.json` + `reports/akhir_sejati_4h.json`. **Modul berdiri hijau sendiri lebih dulu**, dan ramalan jumlah uji ditulis di pesan commit sebelum laporannya dibaca. ADR-nya sendiri wajib mendahului kodenya bila ada keputusan metodologi baru.
2. **`.github/workflows/backtest.yml` dibalik PALING AKHIR** — menyentuhnya **langsung memulai run**. Kini masih `ohlcv_1h_*` + `funding_shard*`, `--interval 1h`, `--universe reports/universe_layak_v2.json`, `--akhir-sejati reports/akhir_sejati.json`, timeout 330. Langkah `impor`-nya memaku identitas hipotesis lama dan harus ditulis ulang bersama tajuk penjelasnya.
3. Periksa `git pull --rebase --autostash origin main` pada tujuh workflow yang belum diperiksa (`funding`, `funding_check`, `universe`, `doctor`, `backfill_daily`, `notion_asap`, `tests`) dan tinjau apakah ada yang sudah tak diperlukan. **Yang sudah punya: `geometri`, `validate`, `potong_ekor`, `backtest`, `ingest_tier_b`** — STATE v21 salah menyatakan hanya `geometri.yml`.
4. Baca `reports/validate_1h.json` untuk mengukur asimetri gerbang bar datar 1h lawan 4h.
5. **Pisahkan sinyal dari geometri keluar.** Skor entri acak nyata **0,04661R identik** di H-010 dan H-012 — bukti terkuat bahwa keunggulan yang terukur mungkin seluruhnya milik geometri keluar. Butuh ADR sendiri. Pertanyaan paling penting yang tersisa.
6. **Funding sebagai sinyal.** Kandungan informasi arahnya belum pernah diuji.
7. Utang teknis: sambungkan `maks_rasio_bar_datar` ke gerbang · `hasattr`/`__import__` di `test_run_h012.py` · pengujian `biaya_bolak_balik_R` · `pytest` ke `requirements-dev.txt` · docstring `median_stop_frac_bingkai` · nama ganda legasi `potong_ekor` sampai `backtest.yml` berinterval · tripwire tekstual `inspect.getsource` di `test_runner_interval.py` (lemah, dan dicatat sebagai lemah) · perketat `lux/funding.py::gerbang_lulus` · diff Dataset G lama (528 simbol) · `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md` · salin ADR-001/ADR-002 ke `decisions/` · naikkan `versi` config sesudah seluruh pembacanya diperiksa.
8. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus, dengan ≥24 shard.

**Sudah lunas, jangan dikerjakan ulang:** modul degenerasi, pengaman biaya masuk, perambatan walk-forward, lantai semesta di runner, agregat per bulan, `sebaran.py`, `geometri_keluar.py`, pelapor Notion (kredensial **terverifikasi** run `30207584722`), `stop_hormati_celah`, `validate` 4h, `potong_ekor` berinterval, `lux/kerangka.py`, dan seluruh ADR-019.

**DIBATALKAN atas keputusan pengguna:** agen **LUX Gatekeeper** tidak dipakai (kredit kemungkinan habis sebelum riset selesai), termasuk pekerjaan "selaraskan instruksi dari sembilan ke sebelas gerbang". Kolom `Verdict` di database Notion menjadi kolom **manusia**.

### Godaan yang wajib ditolak

Membuang USDCUSDT menghasilkan **+0,060163R** pada 397 simbol tertahan. **Angka itu haram dipakai sebagai kelulusan atau sebagai bukti H-010 benar** — itu penyubsetan simbol pasca-hasil. Ia hanya boleh muncul berlabel diagnostik, selalu bersama larangannya. Demikian pula **+0,059636R** milik H-012 atas seluruh riwayat: kriteria yang dipra-registrasi adalah periode tahan-waktu, bukan seluruh riwayat, dan memilih yang kedua sesudah melihat keduanya adalah pemilihan periode pasca-hasil.

**Dilarang menyebut H-012 "H-010 setelah perbaikan".**

### Cara saya ingin kamu bekerja

- Ketika saya menulis "lanjut", teruskan langsung dari titik terakhir tanpa konfirmasi dan tanpa mengulang penjelasan.
- **Pisahkan fakta terverifikasi dari asumsi.** Asumsi hanya naik jadi fakta bila ada bukti terlampir berupa commit, run ID, atau kutipan sumber.
- Katakan bila saya salah, dan katakan bila kamu sendiri salah.
- Perbarui `STATE.md` setiap kali posisi riset berubah, tambahkan entri `journal/` tiap sesi, dan segarkan berkas ini sebelum konteks penuh.

---

## Aturan kerja yang dibayar mahal — jangan pelajari ulang

1. **Pytest hijau sebelum unduhan apa pun.** Gerbang yang bisa gagal ditaruh sebelum langkah panjang, bukan sesudahnya. Berlaku juga di dalam kode: `ukur_sebaran` melempar galat pada nilai tidak finit, jadi `runner.py` menangkapnya dan menulisnya ke laporan alih-alih menjatuhkan run 438 simbol di ujungnya.
2. **Modul baru berdiri hijau sendiri lebih dulu, penyambungan menyusul.** Dipakai sebelas kali, terakhir `lux/kerangka.py` (702) sebelum `potong_ekor` memakainya (703).
3. **Tulis ramalan jumlah pengujian sebelum membaca laporan**, dan **cacah dari muatan yang benar-benar dikirim**. Tujuh ramalan terakhir tepat: 679, 683, 702, 703, 709, 711, 714.
4. **Blob laporan yang tidak berubah berarti belum ditulis** — bukan berhasil, bukan gagal, dan **bukan** "angka lama tetap". Dipakai dengan benar tiga kali pada ADR-019 langkah 3, ketika blob lama masih menyebut commit sebelumnya.
5. **Commit laporan tanpa berkas hasil berarti run GAGAL.** Hijau ≠ berhasil; baca laporan yang dikomit.
6. **Baca modulnya sebelum menulis kode terhadapnya, dan baca berkasnya utuh sebelum menulis ulang.** Jangan pernah menebak nama simbol yang diimpor maupun tanda tangan fungsi. Kesalahan `fee_efektif` yang menjatuhkan empat run berturut-turut lahir dari menebak nama medan.
7. **Jangan menyunting modul yang dibekukan** — `run_wf`, `run_h002`, `run_h003`, `run_h007`, `run_h008`, `run_h009`. `run_h009` memasang `assert` bahwa gridnya identik `run_h007`, jadi `run_h007.IMBALAN` haram disunting. `run_wf.muat_ohlcv` disunting di ADR-019 **hanya karena ADR memutuskannya lebih dulu** dan hanya dengan syarat 1h bit-identik.
8. **Jangan mengimpor ke arah yang bisa menutup siklus** (cacat `4b77617`). Itu sebabnya `konsentrasi.py`, `funding_ekor.py`, `sebaran.py`, `degenerasi.py`, dan `kerangka.py` berdiri sebagai modul sendiri di tingkat atas.
9. **Medan `Konfig` baru diletakkan paling akhir dan bawaannya MATI.** Lima saringan mesin bawaannya nol/False: `maks_umur_bar`, `maks_carry_R`, `maks_carry_realisasi_R`, `maks_biaya_masuk_R`, `stop_hormati_celah`. Itulah satu-satunya alasan hasil lama masih dapat diulang.
10. **Jangan menulis angka jumlah dengan tangan.** Satu literal tripwire per hal yang dijaga.
11. **Periksa setiap hitungan secara aritmetis dan jangan percaya label buatan sendiri.** Kekeliruan sejauh ini: "26 simbol positif", label "16 pengujian", "226 jendela / 63,5%" yang seharusnya **194 / 54,5%**, dan daftar aset rilis yang lahir dari `ls` tersaring pola `ohlcv_1h_*`. **Cari di repo sebelum memercayai ingatan.**
12. **Keputusan metodologi dikomit sebelum kodenya.** ADR-017, ADR-018, dan ADR-019 seluruhnya ditulis sebelum sebaris kode disentuh.
13. **Ambang pra-registrasi tidak berubah setelah hasil terlihat** — dan sesudah kelulusan ia juga tidak boleh diperketat.
14. **Hipotesis yang ditolak tidak dihitung ulang**, dan tidak dihitung ulang dengan mesin yang berbeda. Menghitung ulang H-001b–H-012 dengan mesin ADR-016 akan mencampur dua mesin dalam satu papan skor.
15. **Rerata bukan ekor. Porsi terhadap nilai bersih bukan konsentrasi. Pencilan bukan sebaran. Proksi yang berkorelasi 0,97 dengan hal lain bukan proksi.**
16. **Gerbang yang memberi jawaban sama pada dua keadaan bertolak belakang tidak memuat informasi.**
17. **Aturan yang diketahui bukan aturan yang diterapkan.**
18. **Batas risiko bukan parameter yang dilombakan.** Pemaksimal ekspektasi akan selalu mematikan pengaman yang menargetkan peristiwa langka (16 dari 14.925 = 0,107%). `stop_hormati_celah` adalah sakelar kejujuran, bukan ambang, jadi ia juga haram dilombakan.
19. **Margin sesempit resolusi alat ukur bukan margin.** p 0,049505 pada 100 permutasi satu satuan dari kegagalan; pada 300 permutasi ia memang gagal (0,0631).
20. **Ekspektasi yang naik karena penyebutnya menyusut bukan keunggulan yang lebih besar.**
21. **Kecurigaan harus NAIK, bukan turun, ketika hasilnya menyenangkan.** Termasuk terhadap run yang terasa terlalu cepat — tetapi periksa log dan blob lebih dulu sebelum menuduh: empat kecurigaan semacam itu di S16–S17 seluruhnya tak berdasar.
22. **Galat baku yang dihitung di bawah andaian kebebasan yang salah hanya boleh menjatuhkan klaim, tidak boleh menegakkannya.** Jangan pernah mengarang statistik yang tidak ada di laporan.
23. **Jangan menuntut kesamaan bit pada agregat pecahan** — penjumlahan pecahan tidak asosiatif. Di dalam satu fungsi murni ia tetap sah. **Dan kesamaan hasil lintas dua run berbeda dilarang diterima tanpa pemeriksaan:** semesta 4h yang persis 447 lalu persis 438 seperti 1h wajib dibandingkan simbol per simbol lebih dulu.
24. **Pagar yang memastikan masukan identik tidak memastikan masukan sah.** Semua pagar `run_h011` lulus dan semestanya tetap memuat simbol yang satuan risikonya runtuh.
25. **Satu simbol dapat mendominasi agregat 438 simbol.** **Biaya yang dibagi penyebut yang bisa mendekati nol adalah biaya tak terbatas** — satuan risiko butuh lantai yang dipra-registrasi, bukan pembuangan simbol pasca-hasil. **Degenerasi dibuktikan oleh `stop_frac`, bukan oleh ejaan nama simbol.**
26. **Himpunan tertahan habis pada saat pertama kali dilihat.** Belanjakan hanya pada pertanyaan yang mekanismenya sudah bersih.
27. **Cacat yang membalik tanda hasil tidak boleh diperbaiki di dalam hipotesis yang sama.** Perbaikannya melahirkan hipotesis baru.
28. **Eksperimen yang tercemar tidak informatif ke arah mana pun.** Catat sebagai kerugian, bukan kemajuan.
29. **Saringan yang menolak entri juga menolaknya saat pemilihan parameter.** Simbol yang selalu degenerat karena itu MENGHILANG dari hitungan penolakan alih-alih muncul di dalamnya — terbukti kuantitatif: hanya **62** entri ditolak di H-012, bukan 500–5.000 seperti diramalkan. Sebelum menafsirkan angka yang dihasilkan sebuah saringan, tanyakan lebih dulu keadaan mana yang membuat angka itu nol.
30. **Jangan pernah menekan hasil negatif, membuang simbol merugi, membuang simbol muda, mematok parameter yang menang belakangan, menurunkan ambang 0,05R, melonggarkan lantai 0,004 atau pengaman 0,5R, atau menyebut sistem layak diperdagangkan.**
31. **Pagar yang menyalin baris dari kode yang dijaganya tidak menjaga apa pun.** Pagar hanya berguna bila dibaca dari **definisi** (`dataclasses.fields`) atau bila ia **memanggil fungsi yang sama** dengan produksi.
32. **Aritmetika yang hidup di dalam `main` tidak dapat diuji.** Perhitungan yang bisa salah wajib menjadi fungsi tingkat modul — `biaya_bolak_balik_R`, `harga_stop_terisi`, dan seluruh `lux/kerangka.py` lahir dari aturan ini.
33. **Setiap langkah workflow wajib `tee` ke `logs/` dan seluruh `logs/` disalin ke `reports/` dengan `if: always()`.** Tanpa itu, run yang gagal tidak meninggalkan bukti apa pun yang dapat dibaca agen.
34. **Lingkungan pagar wajib memasang dependensi yang sama dengan `tests.yml`.**
35. **Muatan tulis yang panjang wajib dibaca ulang utuh sebelum dikirim.** Dua commit cacat berturut lahir dari melewatkan ini: `953ce24a` (loop `pass` sehingga tabel tak pernah ditulis) dan `2a0f8545` (`}` liar yang menjatuhkan **seluruh** koleksi pytest).
36. **Ramalan yang dijamin benar oleh konstruksi bukan ramalan.** Sebelum menghitung sebuah ramalan lulus, tunjukkan keadaan yang membuatnya gagal. Ramalan 2 ADR-015 benar secara sepele: ia meramalkan tidak ada stop di bawah −1,5R terhadap mesin yang **mustahil** menghasilkannya.
37. **Angka yang benar untuk satu interval tidak berubah nilai ketika dipakai di interval lain — ia berubah MAKNA, dan diam.** Setiap besaran yang berarti "satu hari", "satu minggu", atau "sekian jam" wajib diturunkan dari interval lewat `lux.kerangka`, tidak pernah dari literal. Lima cacat sejenis ditemukan berurutan di S17.
38. **Dua definisi atas satu dataset selalu dimenangkan oleh yang tidak terlihat.** Pada cacat kelima, laporan mencetak semesta 438 yang benar sementara mesin memperdagangkan bar yang menurut semesta itu sudah tidak ada. Bila dua tempat menghitung hal yang sama, salah satunya wajib memanggil yang lain.
