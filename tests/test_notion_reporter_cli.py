"""Pengujian CLI pelapor Notion. Tidak menyentuh jaringan sama sekali."""

from __future__ import annotations

import json

import pytest

from lux import notion_reporter as pelapor

SHA = "864da2ec4c84bb1ba5abfe396e18a1844b9d37f6"

ARGV = [
    "--run-id",
    "asap-notion-2026-07-26T12:40Z",
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
        return 200, json.dumps({"url": "https://notion.so/baris"})

    kode = pelapor.main(
        ARGV, pengirim=pengirim, database_id="42052623cef043098f13a6f46baf7f3b"
    )
    assert kode == 0
    badan = dilihat["badan"]
    assert badan["parent"]["database_id"] == "42052623cef043098f13a6f46baf7f3b"
    assert badan["properties"]["Verdict"]["status"]["name"] == "Menunggu Penilaian"
    assert "https://notion.so/baris" in capsys.readouterr().out


def test_main_gagal_bila_database_id_kosong():
    with pytest.raises(ValueError):
        pelapor.main(ARGV, pengirim=lambda *_: (200, "{}"), database_id="")
