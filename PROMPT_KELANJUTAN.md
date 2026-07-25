# Prompt kelanjutan — LUX

Salin blok di bawah ini ke sesi baru.

---

Sebelum melakukan apa pun, baca `STATE.md` di repositori GitHub publik **EnVyxS/lux-research**. Berkas itu adalah jurnal tunggal dan satu-satunya sumber kebenaran tentang posisi riset. **Jangan membaca `journal/` secara utuh.**

Lanjutkan pengembangan riset LUX. Jangan memulai dari awal dan jangan mengulang pekerjaan yang sudah selesai. Sebelum menjalankan workflow berikutnya, periksa kembali workflow sebelumnya; hapus yang sudah tidak diperlukan.

## Konteks

Sistem trading kuantitatif untuk Binance USD-M Futures, dibangun dari nol. Seluruh pengetahuan dari upaya sebelumnya, termasuk log sinyal bot v8.4, sengaja dibuang karena tercemar survivorship bias dan overfitting. Mesin lokal tidak sanggup backtest penuh dan tidak ada VM cloud, jadi **seluruh komputasi berjalan di GitHub Actions** dan repo GitHub adalah penyimpanan data sekaligus jurnal riset.

## Batas alat yang harus dipahami sejak awal

- Sandbox agen tidak punya akses jaringan. Semua pengambilan data terjadi di runner Actions.
- Agen tidak bisa membaca log workflow. Setiap workflow menulis hasil ke `reports/` lalu commit balik; agen membacanya lewat API biasa.
- Agen tidak bisa memicu workflow manual. Setiap workflow punya filter `paths` pada berkasnya sendiri, jadi **menyunting berkas workflow itulah yang memicunya**.
- Agen tidak bisa membuat atau mengunggah rilis. Runner melakukannya lewat `gh release upload`.
- REST `fapi.binance.com` mengembalikan HTTP 451 dari runner. Jangan taruh di jalur kritis.
- Berkas laporan yang belum ada selama run berarti **sedang berjalan**. Konfirmasi lewat `list_commits`, jangan diasumsikan. Sha laporan yang tidak berubah berarti **belum ditulis**, bukan berhasil.

## Posisi riset

Data sudah selesai dan sah: 14.545.679 bar 1h, 790 simbol, 438 simbol layak setelah ADR-003, funding nyata 1.982.017 baris. Mesin backtest lengkap dengan sembilan gerbang mutu, pra-registrasi sekali tulis, dan walk-forward. 382 pengujian hijau.

**Tujuh hipotesis sudah divonis, seluruhnya DITOLAK:**

| ID | Mekanisme | Ekspektasi R |
|---|---|---|
| H-001b | Donchian polos | 0,03086 |
| H-002 | Donchian + saringan carry | 0,03159 |
| H-003 | pembalikan skor-z | −0,24782 |
| H-004 | Donchian + ADX ≥ 30 | −0,01818 |
| H-005 | entri retest ("sniper") | −0,03571 |
| H-006 | sapuan likuiditas (SMC) | −0,13449 |
| **H-007** | **imbalan dipilih walk-forward** | **0,04044 — terbaik** |

Enam percobaan pada sisi **masuk** menghasilkan nol perbaikan. Satu percobaan pada sisi **keluar** menaikkan ekspektasi 28% dalam satu langkah. H-007 gagal karena dua hal: 0,0404R masih di bawah ambang 0,05R, dan gerbang `invarian_risiko` gagal pada −1,977R karena target yang lebih jauh menahan posisi lebih lama sehingga funding menumpuk.

## Pekerjaan berikutnya

**ADR-008 — pengaman carry yang keras, lalu H-008.** `invarian_risiko` sudah menjatuhkan empat dari tujuh hipotesis, termasuk yang terbaik. Saringan ADR-004 menilai carry **terproyeksi** saat entri dan tidak pernah menilai ulang. Yang belum diuji: **keluar paksa saat carry terealisasi melewati batas selama posisi berjalan.** Ini mesin keluar, bukan sinyal, jadi tidak melanggar larangan sinyal harga ketujuh di ADR-006.

Sesudahnya: horizon 4h (prasyarat mutlak: jalankan `validate.yml` untuk 4h lebih dulu), lalu funding sebagai sinyal arah. Satu-satunya butir lama yang masih terbuka adalah diff terhadap Dataset G (528 simbol).

**Dilarang:** menyetel `imbalan_R` ke 4,0 lalu menjalankan ulang. Nilai itu menang setelah hasil terlihat; mengunci pemenang pasca-hoc mengubah walk-forward menjadi teater. Hipotesis berikutnya wajib membiarkan imbalan dipilih walk-forward seperti H-007. Hipotesis yang sudah ditolak tidak pernah dihitung ulang dan tidak ada ambang yang diturunkan.

## Cara saya ingin kamu bekerja

- Ketika saya menulis "lanjut", teruskan langsung dari titik terakhir tanpa konfirmasi dan tanpa mengulang penjelasan.
- Pisahkan fakta terverifikasi dari asumsi. Asumsi hanya naik jadi fakta bila ada bukti terlampir berupa commit, run ID, atau kutipan sumber.
- Katakan bila saya salah, dan katakan bila kamu sendiri salah.
- Perbarui `STATE.md` setiap kali posisi riset berubah, tambahkan entri `journal/` tiap sesi.
- Sebelum konteks penuh, perbarui `PROMPT_KELANJUTAN.md`.

## Aturan yang dibayar mahal

1. Jalankan pytest sebelum unduhan apa pun. Di sesi terakhir gerbang ini menangkap galat sintaks dalam 1,53 detik.
2. Workflow yang memicu dirinya sendiri didorong **hanya setelah** semua modul yang dipanggilnya ada di repo.
3. Hijau bukan berarti berhasil — baca laporan yang dikomit.
4. Keputusan metodologi dikomit sebagai ADR **sebelum** kodenya ditulis.
5. Ambang pra-registrasi tidak pernah berubah setelah hasil terlihat. Hipotesis serentak wajib memakai koreksi multiplisitas yang ditetapkan di muka.
6. Tiga salinan orkestrator adalah batas wajar; yang keempat menuntut runner bersama lebih dulu.
7. **Periksa apakah dugaanmu mungkin secara konstruksi sebelum menjadwalkannya sebagai penelitian.**
