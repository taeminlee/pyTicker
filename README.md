# pyTicker

python으로 만든 암호화폐 시세 확인 프로그램

a monitoring and normalization tool for cryptocurrency that is being handled in Republic of Korea

## 설치 및 실행 (Installation and execution)

### Windows

[다운로드](https://github.com/taeminlee/pyTicker/releases/) 후 pyTicker.exe 실행

[Download](https://github.com/taeminlee/pyTicker/releases/), execute pyTicker.exe

### Linux

```bash
git clone https://github.com/taeminlee/pyTicker
cd pyTicker
pip install requests prettytable babel pygame
python pyTicker.py
```

## 지원 화폐 목록 (list of supported cryptocurrency)

- BTC
- BHC
- ETH
- ETC
- XRP
- ZEC
- XMR
- QTUM
- EOS

## 지원 거래소 목록 (list of supported exchange)

- Bithumb
- Coinone
- CoinIs
- Poloniex
- Bitfinex
- Liqui.io

## pyTicker 파라미터 (pyTicker parameter)

|command|desc (KO)|desc (EN)|
|-------|----|----|
|-h |파라미터 확인 |help|
|-polo|poloniex 추적 끄기 |enable poloniex tracker|
|-bfx|bitfinex 추적 켜기 |enable bitfinex tracker|
|-bt|빗썸 추적 끄기 |disable bithumb tracker|
|-co|코인원 추적 끄기 |disable coinone tracker|
|-ci|코인이즈 추적 끄기 |disable coinis tracker|
|-liqui|리퀴 추적 끄기 |disable liqui tracker)
|-xrp|리플 추적 켜기 |enable xrp tracker|
|-alarm|(98%미만가) 알람 끄기 |disable alarm; <98%|

## 참고 포스트 (Related postings)

https://steemit.com/kr-dev/@tmkor/pyticker

https://steemit.com/coinkorea/@tmkor/pyticker-bch-xmr-bitfinex