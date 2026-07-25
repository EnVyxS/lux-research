"""Klien arsip data.binance.vision.

Empat aturan yang tidak boleh dilanggar, semuanya lahir dari kesalahan nyata:

1. Prefix ``data/`` WAJIB. Tanpa itu S3 mengembalikan ``NoSuchKey``. Kesalahan
   ini pernah terjadi dan menghabiskan satu putaran penuh.
2. Berkas HARUS disimpan dengan nama aslinya. Berkas ``.CHECKSUM`` memuat nama
   berkas, sehingga ``sha256sum -c`` mustahil cocok bila namanya diubah.
   Kesalahan ini juga pernah terjadi dan sempat terbaca sebagai data rusak.
3. REST ``fapi.binance.com`` mengembalikan HTTP 451 dari runner GitHub. Jangan
   pernah menaruhnya di jalur kritis. Arsip S3 adalah satu-satunya sumber.
4. Nama simbol WAJIB di-percent-encode saat menyusun URL CDN. Binance pernah
   mencatatkan perpetual dengan nama berhuruf Han seperti ``龙虾USDT``, dan
   ``urllib`` menolak URL dengan karakter non-ASCII. Listing S3 tetap lolos
   karena parameternya sudah dienkode oleh ``urlencode``, sehingga simbolnya
   muncul di universe namun setiap unduhannya gagal. Kegagalan asimetris
   semacam ini tampak seperti data hilang padahal murni cacat klien.
"""

from __future__ import annotations

import hashlib
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

S3_ENDPOINT = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision"
CDN = "https://data.binance.vision"
ROOT = "data/futures/um"
NS = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}

_UA = {"User-Agent": "lux-research/0.1 (riset kuantitatif)"}


def seg(teks: str) -> str:
    """Percent-encode satu segmen path URL.

    ``safe=""`` disengaja: nama simbol tidak boleh mengandung pemisah path,
    jadi setiap karakter istimewa memang harus dienkode.
    """
    return urllib.parse.quote(teks, safe="")


def _get(url: str, timeout: int = 90, retries: int = 5) -> bytes:
    """Ambil URL dengan backoff eksponensial.

    Kegagalan jaringan sementara adalah hal biasa saat mengambil ribuan berkas.
    Yang tidak boleh terjadi adalah kegagalan itu diam-diam menghasilkan data
    tidak lengkap, jadi kegagalan permanen dilempar sebagai exception.
    """
    delay = 1.0
    terakhir: Exception | None = None
    for _ in range(retries):
        try:
            req = urllib.request.Request(url, headers=_UA)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except Exception as exc:  # noqa: BLE001 - semua galat diperlakukan sama
            terakhir = exc
            time.sleep(delay)
            delay = min(delay * 2, 30.0)
    raise RuntimeError(f"gagal mengambil {url}: {terakhir}")


def _listing(prefix: str, delimiter: str = "/"):
    """Iterasi halaman listing S3, menangani pagination sampai habis."""
    token = None
    while True:
        q = {
            "list-type": "2",
            "max-keys": "1000",
            "prefix": prefix,
            "delimiter": delimiter,
        }
        if token:
            q["continuation-token"] = token
        root = ET.fromstring(_get(S3_ENDPOINT + "?" + urllib.parse.urlencode(q)))
        yield root
        if root.findtext("s3:IsTruncated", "false", NS) != "true":
            return
        token = root.findtext("s3:NextContinuationToken", None, NS)
        if not token:
            return


def list_prefixes(prefix: str) -> list[str]:
    hasil: list[str] = []
    for root in _listing(prefix):
        hasil += [e.text for e in root.findall("s3:CommonPrefixes/s3:Prefix", NS)]
    return hasil


def list_keys(prefix: str) -> list[str]:
    hasil: list[str] = []
    for root in _listing(prefix, delimiter=""):
        hasil += [e.text for e in root.findall("s3:Contents/s3:Key", NS)]
    return hasil


def list_symbols(period: str = "monthly", kind: str = "klines") -> list[str]:
    """Semua simbol yang PERNAH ada di arsip, termasuk yang sudah delisted."""
    base = f"{ROOT}/{period}/{kind}/"
    return sorted(p[len(base):].strip("/") for p in list_prefixes(base))


def list_months(symbol: str, interval: str, kind: str = "klines") -> list[str]:
    """Bulan yang tersedia untuk satu simbol, format ``YYYY-MM``."""
    base = f"{ROOT}/monthly/{kind}/{symbol}/{interval}/"
    bulan = set()
    for key in list_keys(base):
        nama = key.rsplit("/", 1)[-1]
        if not nama.endswith(".zip"):
            continue
        bagian = nama[:-4].split("-")
        if len(bagian) >= 2:
            bulan.add(f"{bagian[-2]}-{bagian[-1]}")
    return sorted(bulan)


def list_days(symbol: str, interval: str, kind: str = "klines") -> list[str]:
    """Tanggal yang tersedia di arsip harian, format ``YYYY-MM-DD``."""
    base = f"{ROOT}/daily/{kind}/{symbol}/{interval}/"
    hari = set()
    for key in list_keys(base):
        nama = key.rsplit("/", 1)[-1]
        if not nama.endswith(".zip"):
            continue
        bagian = nama[:-4].split("-")
        if len(bagian) >= 3:
            hari.add(f"{bagian[-3]}-{bagian[-2]}-{bagian[-1]}")
    return sorted(hari)


def klines_url(symbol: str, interval: str, month: str, kind: str = "klines") -> str:
    s = seg(symbol)
    return f"{CDN}/{ROOT}/monthly/{kind}/{s}/{interval}/{s}-{interval}-{month}.zip"


def daily_klines_url(symbol: str, interval: str, day: str, kind: str = "klines") -> str:
    s = seg(symbol)
    return f"{CDN}/{ROOT}/daily/{kind}/{s}/{interval}/{s}-{interval}-{day}.zip"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def verify(path: Path, url: str) -> bool:
    try:
        teks = _get(url + ".CHECKSUM", timeout=60).decode()
    except Exception:  # noqa: BLE001
        return False
    diharapkan = teks.split()[0].strip()
    return _sha256(path) == diharapkan


def download(url: str, dest_dir: str | Path, verify_checksum: bool = True) -> Path:
    """Unduh satu berkas arsip, resumable dan terverifikasi.

    Berkas yang sudah ada dan lolos checksum dilewati, sehingga job yang mati
    di tengah jalan dapat dilanjutkan tanpa mengunduh ulang semuanya.
    """
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    # Nama berkas dikembalikan ke bentuk aslinya agar direktori sementara tetap
    # terbaca manusia saat menelusuri kegagalan.
    dest = dest_dir / urllib.parse.unquote(url.rsplit("/", 1)[-1])

    if dest.exists():
        if not verify_checksum or verify(dest, url):
            return dest
        dest.unlink()

    dest.write_bytes(_get(url, timeout=300))

    if verify_checksum and not verify(dest, url):
        dest.unlink(missing_ok=True)
        raise RuntimeError(f"checksum tidak cocok untuk {url}")
    return dest
