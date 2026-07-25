# Laporan doctor

Run `30161543831` pada commit `b8722a5d70687367620b84df9bda076eb38d88a9`, 2026-07-25T14:23:36Z.

## Kapasitas runner

| Sumber daya | Nilai |
|---|---|
| vCPU | 4 |
| RAM | 15Gi |
| Disk bebas di workspace | 88 GB |
| Model CPU | AMD EPYC 7763 64-Core Processor |

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       145G   58G   88G  40% /
/dev/sda16      881M   64M  756M   8% /boot
/dev/sda15      105M  6.2M   99M   6% /boot/efi
```

## Binance Vision CDN

- HEAD: `200`
- Terunduh: 38890 byte dalam 0.406569 detik
- Checksum cocok: false
- CSV hasil bongkar: 91706 byte, 745 baris
- Rasio zip: 2.36x
- Baris pertama CSV:
```
open_time,open,high,low,close,volume,close_time,quote_volume,count,taker_buy_volume,taker_buy_quote_volume,ignore
```
- Keluaran sha256sum:
```
sha256sum: BTCUSDT-1h-2024-01.zip: No such file or directory
BTCUSDT-1h-2024-01.zip: FAILED open or read
sha256sum: WARNING: 1 listed file could not be read
```

## Endpoint S3 listing

- HTTP: `200`, berisi CommonPrefixes: true
- Prefix contoh: <Prefix>data/futures/um/monthly/klines/</Prefix> <Prefix>data/futures/um/monthly/klines/0GUSDT/</Prefix> <Prefix>data/futures/um/monthly/klines/1000000BOBUSDT/</Prefix> <Prefix>data/futures/um/monthly/klines/1000000MOGUSDT/</Prefix> <Prefix>data/futures/um/monthly/klines/1000BONKUSDC/</Prefix> <Prefix>data/futures/um/monthly/klines/1000BONKUSDT/</Prefix> 
```xml
<?xml version="1.0" encoding="UTF-8"?>
<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Name>data.binance.vision</Name><Prefix>data/futures/um/monthly/klines/</Prefix><NextContinuationToken>1vtlduUMizIyQD/6/A3c8up6AL3k5qpkwFua49VoycjWcV3WiCRfVhIYUWxGaTKYMDKt1oX8g/yEuBAsq2UbVEUIU8F4U8vJl</NextContinuationToken><KeyCount>20</KeyCount><MaxKeys>20</MaxKeys><Delimiter>/</Delimiter><IsTruncated>true</IsTruncated><CommonPrefixes><Prefix>data/futures/um/monthly/klines/0GUSDT/</Prefix></CommonPrefixes><CommonPrefixes><Prefix>data/futures/um/monthly/klines/1000000BOBUSDT/</Prefix></Com
```

## REST exchangeInfo

- HTTP: `451`, jumlah simbol: null
- Cuplikan respons:
```
{  "code": 0,  "msg": "Service unavailable from a restricted location according to 'b. Eligibility' in https://www.binance.com/en/terms. Please contact customer service if you believe you received this message in error."}
```

## Probe simbol delisted

Kode 200 berarti Binance masih mengarsipkan data simbol yang sudah delisted, yang menentukan apakah universe bebas survivorship bias dapat dibangun.

```
 SRMUSDT=200 FTTUSDT=404 COCOSUSDT=404
```

## Versi alat
```
Python 3.12.3
gh version 2.96.0 (2026-07-02)
git version 2.54.0
```
