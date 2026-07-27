"""Pagar untuk ``.github/workflows/tests.yml``.

Berkas workflow tidak diuji oleh apa pun sampai sekarang, dan itu berbahaya
secara khusus: satu-satunya sebab laporan run **merah** sampai ke repo adalah
URUTAN langkahnya - laporan dikomit sebelum hasil ditegakkan. Urutan itu tidak
kelihatan salah bila tertukar; ia hanya diam-diam berhenti bekerja, dan
kerusakannya baru terasa berbulan kemudian ketika sebuah run merah tidak
meninggalkan jejak apa pun.

Uji di sini sengaja memeriksa **teks** berkasnya, bukan menjalankan workflow.
Menjalankan workflow di dalam pytest mustahil di sini (tidak ada jaringan), dan
yang hendak dijaga memang sifat tekstual: perintah yang hadir dan urutan
langkah.

Uji ini TIDAK memeriksa hal-hal yang sengaja tidak dipakai (pytest-xdist, -x,
--tb=long) lewat larangan menyeluruh, sebab larangan semacam itu akan menolak
komentar yang menjelaskan mengapa keduanya tidak dipakai. Yang diperiksa adalah
bentuk perintah pytest yang benar-benar dijalankan.
"""

from __future__ import annotations

from pathlib import Path

import pytest

AKAR = Path(__file__).resolve().parents[1]
JALUR = AKAR / ".github" / "workflows" / "tests.yml"


@pytest.fixture(scope="module")
def teks() -> str:
    return JALUR.read_text(encoding="utf-8")


def test_workflow_ada() -> None:
    assert JALUR.is_file(), f"workflow hilang: {JALUR}"


def test_collect_only_hadir(teks: str) -> None:
    """Cacah butir uji wajib dapat dibaca dari berkas juga pada run merah."""
    assert "--collect-only" in teks
    assert "Butir terkumpul:" in teks


def test_komit_sebelum_penegakan(teks: str) -> None:
    """Membalik urutan ini membuat laporan run merah hilang tanpa jejak."""
    i_komit = teks.index("Commit laporan")
    i_tegak = teks.index("Tegakkan hasil")
    assert i_komit < i_tegak, "laporan harus dikomit sebelum hasil ditegakkan"


def test_skip_ci_hadir(teks: str) -> None:
    """Tanpa ini komit laporan memicu workflow yang menulis laporan lagi."""
    assert "[skip ci]" in teks


def test_pengaman_kode_keluar_utuh(teks: str) -> None:
    """pytest tidak boleh menjatuhkan job sebelum laporannya ditulis."""
    assert "set +e" in teks
    assert "kode=$?" in teks
    assert "git pull --rebase --autostash origin main" in teks
    assert "exit 1" in teks


def test_perintah_pytest_dan_ekor(teks: str) -> None:
    """-rf ada, --tb pendek, ekor 200 baris, tanpa -x dan tanpa xdist."""
    baris = [b.strip() for b in teks.splitlines() if "python -m pytest tests" in b]
    assert len(baris) == 2, f"perintah pytest tak terduga: {baris}"
    kumpul = [b for b in baris if "--collect-only" in b]
    jalan = [b for b in baris if "--collect-only" not in b]
    assert len(kumpul) == 1 and len(jalan) == 1
    perintah = jalan[0]
    assert "-rf" in perintah
    assert "--tb=short" in perintah
    assert "--tb=long" not in perintah
    assert " -x" not in perintah
    assert "-n auto" not in perintah
    assert "tail -n 200 /tmp/pytest.txt" in teks


def test_baris_gagal_tidak_dipotong(teks: str) -> None:
    """Seluruh baris FAILED/ERROR masuk laporan, bukan hanya ekornya."""
    assert "grep -E 'FAILED|ERROR' /tmp/pytest.txt > /tmp/gagal.txt" in teks
    assert "cat /tmp/gagal.txt" in teks
