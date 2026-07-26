"""Pengujian pelapor Notion. Tidak menyentuh jaringan sama sekali."""

from __future__ import annotations

import json

import pytest

from lux import notion_reporter as pelapor

SHA = "b69b632339b93a8e0c2f81fd472cb5353b517d97"


def baris_sah(**ganti):
    argumen = dict(
        run_id="S8-h012-2026-07-26T11:47Z",
        tahap="S8 Walk-Forward OOS",
        status_eksekusi="Sukses",
        commit=SHA,
        ringkasan={"ekspektasi_R": 0.04171275623950187},
    )
    argumen.update(ganti)
    return pelapor.properti_baris(**argumen)


def test_sebelas_gerbang_terdaftar():
    assert len(pelapor.NAMA_GERBANG_NOTION) == pelapor.JUMLAH_GERBANG == 11


def test_gerbang_baru_ada_di_peta():
    assert pelapor.NAMA_GERBANG_NOTION["konsentrasi"] == "Konsentrasi"
    assert pelapor.NAMA_GERBANG_NOTION["funding_ekor"] == "Funding ekor"


def test_nama_gerbang_mesin_dipetakan_ke_ejaan_notion():
    assert pelapor.nama_gerbang("invarian_risiko") == "Invariant risiko"
    assert pelapor.nama_gerbang("entri_acak") == "Entry acak"


def test_gerbang_asing_ditolak():
    with pytest.raises(ValueError):
        pelapor.nama_gerbang("gerbang_kedua_belas")


def test_potong_di_bawah_batas_tidak_mengubah():
    assert pelapor.potong("pendek") == "pendek"


def test_potong_menghormati_batas():
    hasil = pelapor.potong("x" * 5000)
    assert len(hasil) == pelapor.BATAS_AMAN
    assert len(hasil) < pelapor.BATAS_RICH_TEXT


def test_potong_menandai_dirinya():
    assert pelapor.potong("x" * 5000).endswith(pelapor.PENANDA_POTONG)


def test_potong_menolak_batas_mustahil():
    with pytest.raises(ValueError):
        pelapor.potong("apa pun", batas=3)


def test_run_id_menjadi_judul():
    properti = baris_sah()
    assert properti["Run ID"]["title"][0]["text"]["content"].startswith("S8-h012")


def test_run_id_kosong_ditolak():
    with pytest.raises(ValueError):
        baris_sah(run_id="")


def test_tahap_asing_ditolak():
    with pytest.raises(ValueError):
        baris_sah(tahap="S9 Live")


def test_status_asing_ditolak():
    with pytest.raises(ValueError):
        baris_sah(status_eksekusi="Lulus")


def test_verdict_selalu_menunggu_penilaian():
    assert baris_sah()["Verdict"]["status"]["name"] == "Menunggu Penilaian"


def test_verdict_tidak_dapat_disetel_workflow():
    with pytest.raises(TypeError):
        pelapor.properti_baris(
            run_id="x",
            tahap="Lainnya",
            status_eksekusi="Sukses",
            commit=SHA,
            ringkasan="{}",
            verdict="Lulus",
        )


def test_commit_pendek_ditolak():
    with pytest.raises(ValueError):
        baris_sah(commit="b69b632")


def test_gerbang_kosong_berarti_semua_lulus():
    assert baris_sah()["Gerbang Gagal"]["multi_select"] == []


def test_gerbang_gagal_ditulis_sebagai_opsi():
    properti = baris_sah(gerbang_gagal=["invarian_risiko", "funding_ekor"])
    nama = [opsi["name"] for opsi in properti["Gerbang Gagal"]["multi_select"]]
    assert nama == ["Invariant risiko", "Funding ekor"]


def test_angka_dan_tanggal_dipakai_bila_ada():
    properti = baris_sah(
        baris_diproses=135681,
        simbol_diproses=437,
        durasi_detik=1220.6,
        selesai_iso="2026-07-26T11:47:26Z",
        lokasi_artefak="tier-b-v1",
    )
    assert properti["Baris Diproses"]["number"] == 135681
    assert properti["Simbol Diproses"]["number"] == 437
    assert properti["Durasi (detik)"]["number"] == pytest.approx(1220.6)
    assert properti["Selesai"]["date"]["start"] == "2026-07-26T11:47:26Z"
    assert "Lokasi Artefak" in properti


def test_ringkasan_besar_dipotong_bukan_ditolak():
    besar = {f"kunci_{i}": i for i in range(500)}
    isi = baris_sah(ringkasan=besar)["Ringkasan JSON"]["rich_text"][0]["text"][
        "content"
    ]
    assert len(isi) <= pelapor.BATAS_AMAN


def test_payload_menolak_database_id_kosong():
    with pytest.raises(ValueError):
        pelapor.payload_baris("", baris_sah())


def test_kirim_memakai_pengirim_suntikan_tanpa_jaringan():
    dilihat = {}

    def pengirim(url, badan, kepala):
        dilihat["url"] = url
        dilihat["badan"] = json.loads(badan.decode("utf-8"))
        dilihat["kepala"] = dict(kepala)
        return 200, "{}"

    payload = pelapor.payload_baris("db-uuid", baris_sah())
    kode, _ = pelapor.kirim(payload, token="rahasia", pengirim=pengirim)
    assert kode == 200
    assert dilihat["url"] == pelapor.URL_API
    assert dilihat["badan"]["parent"]["database_id"] == "db-uuid"
    assert dilihat["kepala"]["Notion-Version"] == pelapor.VERSI_API


def test_kirim_tanpa_token_gagal_terbuka(monkeypatch):
    monkeypatch.delenv("NOTION_TOKEN", raising=False)
    payload = pelapor.payload_baris("db-uuid", baris_sah())
    with pytest.raises(pelapor.GalatPelapor):
        pelapor.kirim(payload, pengirim=lambda *_: (200, "{}"))


def test_kirim_menaikkan_galat_pada_penolakan_notion():
    payload = pelapor.payload_baris("db-uuid", baris_sah())
    with pytest.raises(pelapor.GalatPelapor):
        pelapor.kirim(
            payload, token="rahasia", pengirim=lambda *_: (400, "validation_error")
        )
