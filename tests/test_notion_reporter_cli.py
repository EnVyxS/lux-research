"""Pengujian CLI pelapor Notion. Tidak menyentuh jaringan dan tidak memakai
kredensial nyata: token dan pengirim keduanya disuntik."""

from __future__ import annotations

import json

import pytest

from lux import notion_reporter as pelapor

SHA = "3880408fabaf73947c966ac6ab32d39effb07e27"
DB = "42052623cef043098f13a6f46baf7f3b"
TOKEN_UJI = "token-uji-bukan-kredensial-nyata"
URL_PALSU = "url-baris-notion-palsu"

ARGV = [
    "--run-id",
    "asap-notion-2026-07-26T15:06Z",
    "--tahap",
    "Lainnya",
    "--status",
    "Sukses",
    "--commit",
    SHA,
    "--ringkasan",
    '{"jenis":"asap"}',
]


def test_argumen_membaca_wajib_dan_opsional():
    opsi = pelapor.argumen(ARGV + ["--durasi", "1220.6", "--simbol", "437"])
    assert opsi.tahap == "Lainnya"
    assert opsi.commit == SHA
    assert opsi.durasi == pytest.approx(1220.6)
    assert opsi.simbol == 437
    assert opsi.gerbang == []


def test_argumen_menolak_tahap_di_luar_skema():
    with pytest.raises(SystemExit):
        pelapor.argumen(
            [
                "--run-id",
                "x",
                "--tahap",
                "S9 Live",
                "--status",
                "Sukses",
                "--commit",
                SHA,
                "--ringkasan",
                "{}",
            ]
        )


def test_main_mengirim_satu_baris_tanpa_jaringan(capsys):
    dilihat = {}

    def pengirim(url, badan, kepala):
        dilihat["badan"] = json.loads(badan.decode("utf-8"))
        return 200, json.dumps({"url": URL_PALSU})

    kode = pelapor.main(
        ARGV, pengirim=pengirim, database_id=DB, token=TOKEN_UJI
    )
    assert kode == 0
    badan = dilihat["badan"]
    assert badan["parent"]["database_id"] == DB
    assert badan["properties"]["Verdict"]["status"]["name"] == "Menunggu Penilaian"
    assert URL_PALSU in capsys.readouterr().out


def test_main_meneruskan_token_suntikan_ke_header(monkeypatch):
    """Token suntikan wajib sampai ke header, dan lingkungan tidak dipakai."""
    monkeypatch.setenv(pelapor.NAMA_ENV_TOKEN, "token-lingkungan-yang-salah")
    dilihat = {}

    def pengirim(url, badan, kepala):
        dilihat["otorisasi"] = kepala["Authorization"]
        return 200, "{}"

    pelapor.main(ARGV, pengirim=pengirim, database_id=DB, token=TOKEN_UJI)
    assert dilihat["otorisasi"] == f"Bearer {TOKEN_UJI}"


def test_main_gagal_bila_database_id_kosong():
    with pytest.raises(ValueError):
        pelapor.main(
            ARGV, pengirim=lambda *_: (200, "{}"), database_id="", token=TOKEN_UJI
        )
