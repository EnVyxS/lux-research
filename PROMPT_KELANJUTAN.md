# Prompt kelanjutan

Salin isi berkas ini ke sesi baru bila konteks sesi sekarang habis.

---

Baca `STATE.md` di repositori GitHub publik **EnVyxS/lux-research** lebih dulu. Berkas itu jurnal tunggal dan satu-satunya sumber kebenaran tentang posisi riset. Jangan membaca `journal/` secara utuh.

## Posisi saat ini

STATE.md versi 9. Tahap S9 selesai. **Enam hipotesis sinyal harga sudah divonis, semuanya DITOLAK.**

| ID | Mekanisme | Ekspektasi R | Putusan |
|---|---|---|---|
| H-001b | Donchian polos | 0,03086 | DITOLAK |
| **H-002** | **Donchian + saringan carry** | **0,03159** | **DITOLAK, terbaik sejauh ini** |
| H-003 | pembalikan skor-z | −0,24782 | DITOLAK |
| H-004 | Donchian + ADX ≥ 30 | −0,01818 | DITOLAK |
| H-005 | entri retest ("sniper") | −0,03571 | DITOLAK |
| H-006 | sapuan likuiditas (SMC) | −0,13449 | DITOLAK |

Seluruhnya pada dataset, kriteria, limit 40 simbol, dan kode penilaian identik. Ambang lulus 0,05R tidak pernah didekati.

## Tiga temuan yang jangan diuji ulang

1. **Kerangka eksekusi bukan tertuduh.** Kelanjutan +0,0316R dan pembalikan −0,2478R pada kerangka identik; rentang 0,28R itu membuktikan kerangka meneruskan informasi arah dengan baik.
2. **Saringan yang mengurangi perdagangan justru merusak.** ADX ≥ 30 membuang 58% perdagangan, menurunkan biaya rerata ke 0,0313R, dan tetap menjungkirkan tanda ekspektasi. Menunggu retest melakukan hal serupa. Keduanya membuang sisi kanan sebaran.
3. **Pembalikan jangka pendek rugi sistematis pada 1h perp.** Dua mekanisme independen (skor-z dan sapuan likuiditas) gagal dengan pola sama, keduanya dengan p entri acak buruk.

## Pekerjaan berikutnya

1. **Periksa sebaran R H-002 dari `reports/backtest_h002.json`.** Murah, tanpa run baru. Bila keunggulan berasal dari segelintir perdagangan berekor panjang, tertuduhnya adalah target 2R yang memotong pemenang — pertanyaan tentang struktur keluar, bukan sinyal masuk. Ini pintu paling menjanjikan yang tersisa.
2. **Horizon 4h.** Wajib didahului `validate.yml` untuk 4h; interval itu belum pernah divalidasi.
3. **Funding sebagai sinyal**, bukan hanya biaya. Belum pernah diuji.
4. Perketat `gerbang_lulus` di `lux/funding.py`; perbaiki docstring `lux/costs.py`; diff Dataset G lama (528 simbol).

**Hipotesis sinyal harga ketujuh pada horizon 1h dilarang** oleh ADR-006, didukung enam titik data.

## Cara bekerja

- "lanjut" berarti teruskan dari titik terakhir tanpa konfirmasi dan tanpa mengulang penjelasan.
- Pisahkan fakta dari asumsi; asumsi naik jadi fakta hanya dengan commit, run ID, atau kutipan sumber.
- Katakan bila pengguna salah, dan katakan bila kamu sendiri salah.
- Perbarui `STATE.md` setiap kali posisi riset berubah; tambahkan entri `journal/` tiap sesi; perbarui berkas ini sebelum konteks penuh.

## Aturan operasional yang dibayar mahal

- `pytest` wajib hijau **sebelum** unduhan di setiap workflow.
- Workflow yang memicu dirinya sendiri didorong **sesudah** seluruh modul yang dipanggilnya ada.
- Hijau bukan berarti berhasil — baca laporan yang dikomit.
- **Sha laporan yang tidak berubah berarti "belum ditulis", tidak pernah berarti "berhasil".**
- Pra-registrasi sekali tulis; ambang tidak pernah diubah setelah hasil terlihat; hipotesis yang ditolak tidak pernah dihitung ulang.
- Keputusan metodologis dikomit sebelum kodenya.
- Menguji beberapa hipotesis serentak wajib disertai koreksi multiplisitas yang ditetapkan di muka.
- Orkestrator baru memakai `lux/backtest/runner.py`; `run_wf.py`, `run_h002.py`, `run_h003.py` beku.
