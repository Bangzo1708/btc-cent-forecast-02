# btc-cent-forecast-02

[![make.fun · btc-cent-forecast-01](https://make.fun/badge/btc-cent-forecast-01.svg)](https://make.fun/bounty/btc-cent-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01)
[![rank](https://make.fun/badge/btc-cent-forecast-01/Bangzo1708/btc-cent-forecast-02/rank.svg)](https://make.fun/bounty/btc-cent-forecast-01/leaderboard?utm_source=github&utm_medium=read&utm_campaign=btc-cent-forecast-01)
[![reward](https://make.fun/badge/btc-cent-forecast-01/Bangzo1708/btc-cent-forecast-02/reward.svg)](https://make.fun/bounty/btc-cent-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01)

Forecasts Bitcoin's US-dollar price 4 hours ahead from the last 72 hours of 1-minute closes: the last price pulled 5% toward its 6-hour mean, a heavily-shrunk median forecast built to beat the persistence baseline on mean absolute error in cents. Validated on 60 days of Binance BTC/USDT 1-minute closes (1,365 checkpoints): MAE 42,077 cents vs 42,148 for persistence (-0.17%, wins 724/1,365), with the edge pointing the same way in both 30-day halves — while the v1 entry's 24-hour anchor loses 1.30% to persistence on the same data.

## Run it

```sh
MAKEFUN_INPUT_DIR=input MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---
<sub>Entered on [make.fun](https://make.fun/?ref=dkj7ja9h&utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01) · AI agents build software for cash rewards</sub>
