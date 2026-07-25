# Laporan doctor

Run `30161624965` pada commit `f5de07aa561fe128dfc9c369b2888ce6af82db5d`, 2026-07-25T14:26:14Z.

## Kapasitas runner

| Sumber daya | Nilai |
|---|---|
| vCPU | 4 |
| RAM | 15Gi |
| Disk bebas | 88 GB |
| CPU | AMD EPYC 9V74 80-Core Processor |

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       145G   58G   88G  40% /
/dev/sda16      881M   64M  756M   8% /boot
/dev/sda15      105M  6.2M   99M   6% /boot/efi
```

## Binance Vision CDN

- HEAD: `200`
- Berkas 1h: 38890 byte dalam 0.923196 detik
- Checksum cocok: **true**
- Berkas 1m: 1898532 byte dalam 1.390325 detik, throughput 1.30 MiB/s
- CSV hasil bongkar: 91706 byte, 745 baris, rasio 2.36x
- Baris pertama CSV:
```
open_time,open,high,low,close,volume,close_time,quote_volume,count,taker_buy_volume,taker_buy_quote_volume,ignore
```
- Keluaran sha256sum:
```
BTCUSDT-1h-2024-01.zip: OK
```

## REST exchangeInfo

- HTTP `451`, simbol: null
- Kode 451 berarti diblokir atas dasar hukum. Runner GitHub berbasis di AS.
