# Prompt kelanjutan — tempel ini di sesi baru

> Disegarkan 2026-07-26 15:35 WIB, sesudah commit `102c297c` (STATE versi 17, tahap S13).
> Berkas ini hanya jembatan. **Sumber kebenaran tunggal tetap `STATE.md`.**

---

## Tempel mulai dari sini

Sebelum melakukan apa pun, baca `STATE.md` di repositori GitHub publik **EnVyxS/lux-research**. Itu jurnal tunggal dan satu-satunya sumber kebenaran tentang posisi riset. **Jangan membaca `journal/` secara utuh** — hanya bila ada rujukan spesifik. Lanjutkan dari titik terakhir; jangan mulai dari awal dan jangan mengulang pekerjaan yang sudah selesai.

Selama proses, periksa kembali workflow sebelumnya sebelum menjalankan yang berikutnya, dan hapus workflow yang sudah tidak diperlukan agar repo tetap bersih.

### Konteks

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun ulang dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang karena tercemar survivorship bias dan overfitting. Mesin lokal tidak sanggup backtest penuh dan tidak ada VM cloud, jadi **seluruh komputasi berjalan di GitHub Actions** dan repo GitHub adalah penyimpanan data sekaligus jurnal riset.

### Batas alat yang harus dipahami sejak awal

- Sandbox agen **tidak punya jaringan**. Semua pengambilan data terjadi di runner Actions.
- Agen **tidak bisa membaca log workflow**, dan daftar alat GitHub yang tersedia **tidak memuat satu pun fungsi Actions**. Solusi yang sudah berjalan: setiap workflow menulis hasil ke `reports/` lalu commit balik; agen membacanya lewat API biasa.
- Agen **tidak bisa memicu workflow manual**. Setiap workflow punya filter `paths` pada berkasnya sendiri, jadi push ke berkas itu yang memicunya. `tests.yml` memfilter `lux/**` dan `tests/**`; `backtest.yml` memfilter dirinya sendiri.
- Agen tidak bisa membuat atau mengunggah rilis; runner melakukannya lewat `gh release upload`.
- REST `fapi.binance.com` mengembalikan **HTTP 451** dari runner. Jangan taruh di jalur kritis. CDN `data.binance.vision` normal.
- `search_code` **tidak berguna di repo ini** — indeks GitHub belum memuatnya dan mengembalikan nol hasil untuk berkas yang jelas ada. Baca berkas langsung.
- Untuk menulis, **pakai `push_files`**, bukan `create_or_update_file`: SHA blob basi begitu ada tulisan. Bentuk argumennya `{ toolName, toolArguments: { owner, repo, branch, message, files } }` — jangan menaruh `owner`/`repo`/`branch` di tingkat atas.
- Runner tidak punya `scipy`. Statistik memakai numpy dan pendekatan normal.

### Posisi sekarang, ringkas

- **Sebelas hipotesis didaftarkan. Sembilan ditolak, satu DITERIMA, satu sedang berjalan.**
- **H-010 LULUS** (run `30193898133`, laporan commit `c035dcee`, sidik `14b2f3bfa8a754b5`): ekspektasi **+0,053028R**, 11.734 perdagangan, 40 simbol, **sebelas gerbang lulus**. Mekanismenya menggeser dinding grid imbalan dari `[1,2,3,4]` ke `[2,4,6,8]` (ADR-012).
- **Kelulusan itu WAJIB dicurigai, dan alasannya tercatat di ADR-013:**
  1. `entri_acak` p **0,049505** lawan ambang 0,05 — jarak tepat **satu satuan resolusi** pada 100 permutasi. Satu permutasi berbeda saja memberi 0,059406 dan H-010 gagal.
  2. Ekspektasi naik **sebagian karena berdagang lebih sedikit**: perdagangan turun 21,4% dan total R hanya naik 0,80%. Laba agregat kotor justru **turun** 7,6%.
  3. Skor entri acak jatuh 56,8% (0,10781 → 0,04661), yang membuka kemungkinan sebagian keunggulan berasal dari **geometri keluar**, bukan dari sinyal.
  4. Tiga dari lima ramalan meleset, **ketiganya ke arah yang menguntungkan hipotesis**. Itu justru alasan kecurigaan naik (aturan 21), bukan turun.
- **Gerbang sebelas**, semuanya terkodekan dan hijau: `konsentrasi` (ADR-010) dan `funding_ekor` (ADR-011) mengikat mulai H-010, tidak diterapkan ke belakang.
- **Utang statistik sudah lunas (ADR-013).** Modul `lux/analisis/sebaran.py` hijau sendiri di `2650ae32`, disambung ke `runner.py` di `485694e1`. Setiap laporan kini memuat simpangan baku, galat baku, kuartil, dan jarak ke ambang dalam satuan galat baku. **Galat baku itu taksiran BAWAH** karena perdagangan tidak saling bebas: sah untuk menjatuhkan klaim, tidak sah untuk menegakkannya.
- **542 pengujian lulus**, laporan pada commit `e22745aa`.
- Dataset Tier B sah: 14.545.679 bar 1h, 790 simbol, universe layak v2 **438 simbol**, funding 1.982.017 baris.

### Yang sedang berjalan saat berkas ini ditulis

**H-011** — didorong di `102c297c`, hasil belum ada. Ia menguji asumsi paling rapuh dalam seluruh riset: **seluruh hasil sejak H-001b diukur pada 40 simbol pertama secara alfabet**, dan daftar itu bukan sampel acak — ia sarat token ber-pengali 1000. Mekanismenya identik H-010 dan run menolak berjalan bila menyimpang; yang berubah hanya `limit` 40 → 0 dan `ulangan` 100 → 300 (peningkatan resolusi p, bukan pelonggaran ambang).

Kriteria utamanya **bukan** blok `putusan` di laporan, melainkan **ekspektasi berbobot perdagangan atas 398 simbol tertahan**, dicetak terpisah oleh `run_h011`. Ramalan tertulis sebelum run, merugikan hipotesis sendiri: **0,020–0,045, jadi gagal**.

Bila hasilnya sudah ada, baca `reports/backtest_h011_semesta_penuh.json` dan `reports/backtest_log.md`. **Blob yang tidak berubah berarti belum ditulis, bukan berhasil.**

### Tindakan berikutnya sesudah H-011

1. **Adjudikasi H-011 terhadap tujuh ramalan ADR-013 bagian 8**, lalu ADR-014 dan STATE v18.
2. **Pisahkan sinyal dari geometri keluar.** Skor entri acak jatuh 56,8%; selama ini tidak terpisah, klaim "ada keunggulan sinyal" belum berdiri. Butuh ADR sendiri.
3. Perketat `lux/funding.py::gerbang_lulus` (utang ADR-011 bagian 6, ADR-012 bagian 7).
4. Perbaiki docstring `lux/costs.py` yang masih menyebut pembagi funding tetap 8 jam.
5. Horizon 4h — prasyaratnya `validate.yml` untuk 4h. Lalu funding sebagai sinyal berarah. Masing-masing butuh ADR.
6. **Uji silang Dataset G lama (528 simbol)** — satu-satunya butir yang masih terbuka dari daftar tugas awal.
7. `lux/manifest.py`, `Makefile`, `docs/PIPELINE.md`; salin ADR-001 dan ADR-002 ke `decisions/`; reporter Notion butuh Secret `NOTION_TOKEN`; instruksi Gatekeeper masih menyebut sembilan gerbang.
8. Tier A (1m) hanya setelah seluruh gerbang Tier B lulus.

### Cara saya ingin kamu bekerja

- Ketika saya menulis "lanjut", teruskan langsung dari titik terakhir tanpa konfirmasi dan tanpa mengulang penjelasan.
- **Pisahkan fakta terverifikasi dari asumsi.** Asumsi hanya naik jadi fakta bila ada bukti terlampir berupa commit, run ID, atau kutipan sumber.
- Katakan bila saya salah, dan katakan bila kamu sendiri salah.
- Perbarui `STATE.md` setiap kali posisi riset berubah, tambahkan entri `journal/` tiap sesi.
- Sebelum konteks penuh, perbarui berkas ini.

---

## Aturan kerja yang dibayar mahal — jangan pelajari ulang

1. **Pytest hijau sebelum unduhan apa pun.** Gerbang yang bisa gagal ditaruh sebelum langkah panjang, bukan sesudahnya. Berlaku juga di dalam kode: `ukur_sebaran` melempar galat pada nilai tidak finit, jadi `runner.py` menangkapnya dan menulisnya ke laporan alih-alih menjatuhkan run 438 simbol di ujungnya.
2. **Modul baru berdiri hijau sendiri lebih dulu, penyambungan menyusul.** Dipakai empat kali: 462→467, 488→494, 494→510, 525→542.
3. **Tulis ramalan jumlah pengujian sebelum membaca laporan.** Empat ramalan terakhir tepat, termasuk yang tepat jumlahnya tetapi memuat satu kegagalan.
4. **Blob laporan yang tidak berubah berarti belum ditulis** — bukan berhasil, bukan gagal. Berkas hasil H-010 butuh **sebelas** pengambilan.
5. **Commit laporan tanpa berkas hasil berarti run GAGAL.** Hijau ≠ berhasil; baca laporan yang dikomit.
6. **Baca modulnya sebelum menulis kode terhadapnya.** Jangan pernah menebak nama simbol yang diimpor. `spek.h.kriteria.min_ekspektasi_R` diperoleh dengan membaca `praregistrasi.py`, bukan mengingat.
7. **Jangan menyunting modul yang dibekukan** — `run_wf`, `run_h002`, `run_h003`, `run_h007`, `run_h008`, `run_h009`. Utang `std_R` semula ditulis sebagai "tambahkan ke `ringkas_gabungan`", padahal fungsi itu berada di `run_wf` yang beku; karena itu perhitungannya berdiri sebagai modul sendiri.
8. **Jangan mengimpor ke arah yang bisa menutup siklus** (cacat `4b77617`). Itu sebabnya `konsentrasi.py`, `funding_ekor.py`, dan `sebaran.py` berdiri sebagai modul sendiri.
9. **Jangan menulis angka jumlah dengan tangan.** Satu literal tripwire diizinkan per hal yang dijaga: `test_gerbang_kesebelas.py` untuk jumlah gerbang, `BATAS_H010` untuk batas 40 simbol.
10. **Periksa setiap hitungan secara aritmetis dan jangan percaya label buatan sendiri.** Empat kekeliruan hitung sejauh ini: "26 simbol positif", label "16 pengujian", dan "226 jendela / 63,5%" yang seharusnya **194 / 54,5%** — angka benarnya sudah ada di tiga tempat di repo. **Cari di repo sebelum memercayai ingatan.**
11. **Keputusan metodologi dikomit sebelum kodenya** (ADR-011 → `funding_ekor.py`; ADR-012 → `run_h010.py`; ADR-013 → `sebaran.py` dan `run_h011.py`).
12. **Ambang pra-registrasi tidak berubah setelah hasil terlihat** — dan sesudah kelulusan ia juga **tidak boleh diperketat**. Keduanya sama-sama menyetel ambang terhadap hasil.
13. **Hipotesis yang ditolak tidak dihitung ulang.** Hipotesis serempak butuh koreksi multiplisitas yang dipatok di muka (p H-005 0,0396 lolos 0,05 tetapi gagal 0,0167).
14. **Rerata bukan ekor. Porsi terhadap nilai bersih bukan konsentrasi. Pencilan bukan sebaran. Proksi yang berkorelasi 0,97 dengan hal lain bukan proksi.** Empat kekeliruan membaca sebaran, semuanya nyata, semuanya sudah ditarik.
15. **Gerbang yang memberi jawaban sama pada dua keadaan bertolak belakang tidak memuat informasi.**
16. **Aturan yang diketahui bukan aturan yang diterapkan.**
17. **Batas risiko bukan parameter yang dilombakan.** Pemaksimal ekspektasi akan selalu mematikan pengaman yang menargetkan peristiwa langka (16 dari 14.925 = 0,107%).
18. **Margin sesempit resolusi alat ukur bukan margin.** p 0,049505 pada 100 permutasi adalah satu satuan dari kegagalan.
19. **Ekspektasi yang naik karena penyebutnya menyusut bukan keunggulan yang lebih besar.**
20. **Kecurigaan harus NAIK, bukan turun, ketika hasilnya menyenangkan.** Ramalan yang meleset ke arah yang menguntungkan layak diperiksa paling keras.
21. **Galat baku yang dihitung di bawah andaian kebebasan yang salah hanya boleh menjatuhkan klaim, tidak boleh menegakkannya.** Jangan pernah mengarang statistik yang tidak ada di laporan.
22. **Jangan pernah menekan hasil negatif, membuang simbol merugi, membuang simbol muda, mematok parameter yang menang belakangan, menurunkan ambang 0,05R, atau menyebut sistem layak diperdagangkan atas kekuatan satu kelulusan 40 simbol.**
