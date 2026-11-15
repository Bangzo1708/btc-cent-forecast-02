# btc-cent-forecast-01 entry v2 (Python 3.13, standard library only): heavily-shrunk
# short-window mean-reversion point forecast of BTC's US-dollar price 240
# minutes after each checkpoint.
#
# Method (two numbers, fixed in advance from a 60-day backtest; nothing fitted
# to the practice answers):
#   guess = last + 0.05 * (mean of the last 360 closes - last)
#
# For mean absolute error the optimal point forecast is the conditional median,
# and the last price (persistence) is the natural median — BTC's 4 h-ahead
# price is a near-random walk, so any pull away from persistence must be
# tiny or it loses. What survives is a small pull toward the recent 6 h mean:
# 1-minute closes carry short-lived noise that partly reverts within hours,
# while a 6 h anchor (unlike a 24 h one) barely moves in a trend, so the
# worst case stays a near-tie with persistence instead of a blow-up.
#
# Evidence (Binance BTC/USDT 1-minute closes, 60 days, 16 Sep - 15 Nov 2026;
# 1,365 checkpoints every 60 min, each with 72 h of history, target +240 min):
#   persistence            MAE 42,148 cents
#   v1 (K=0.10, 24 h mean) MAE 42,694 cents  (+1.30% — WORSE than persistence;
#                                              v1's -3.2% came from one lucky
#                                              range-bound practice window)
#   v2 (K=0.05, 6 h mean)  MAE 42,077 cents  (-0.17%; wins 724/1,365 trials)
#   v2 split-half check: -0.23% on the older 30 days, -0.11% on the recent
#   30 days — the edge is small but it points the same way in both halves,
#   while v1 loses in both. A fine grid (K 0.03-0.07 x window 300-480 min)
#   finds a flat plateau at -0.12% to -0.17% with K=0.05, w=360 on top, so
#   the constants are not a cherry-picked spike. Longer windows, median and
#   10%-trimmed anchors (tied with the mean to within 2 cents), EWMA anchors,
#   drift extrapolation, trend gates and hour-of-day effects were all tested
#   and rejected (each worse than persistence or no better than noise).
#   The pull itself is inherently tiny — the 6 h mean sits within 0.23% of
#   the last price at the median checkpoint — so no extra cap is needed.
#
# Deterministic: pure function of the case file, no randomness, no wall-clock,
# no network. Reads $MAKEFUN_INPUT_DIR (else /input), writes
# $MAKEFUN_OUTPUT_DIR (else /output), one
# {"forecasts":[{"case":"<id>","price":<number>}]} row per case.

import json
import math
import os
from pathlib import Path

INPUT_DIR = os.environ.get("MAKEFUN_INPUT_DIR", "/input")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

# The smallest positive price on the grid: one unit of its 5 decimals.
MIN_PRICE = 0.00001
# The largest grid price below the scorer's exclusive 10,000,000-dollar cap.
MAX_PRICE = 9_999_999.99999

# Minutes of closes averaged for the reversion anchor: six hours.
MEAN_WINDOW_MINUTES = 360
# Fraction of the gap between the last close and its 6 h mean that the guess closes.
REVERSION_K = 0.05


def price5(x):
    """x kept on the grid's 5 decimals and inside the scorer's (0, 10,000,000)."""
    return round(min(MAX_PRICE, max(MIN_PRICE, x)) * 1e5) / 1e5


def recent_mean(prices, window):
    """Mean of the last `window` closes (or of all closes when fewer exist)."""
    w = min(window, len(prices))
    return sum(prices[len(prices) - w:]) / w


def forecast(prices):
    """One market's 4 h-ahead point forecast: last close pulled 5% toward
    its 6 h mean."""
    if not prices:
        raise ValueError("market has no prices")
    last = prices[-1]
    if isinstance(last, bool) or not isinstance(last, (int, float)) or not math.isfinite(last):
        raise ValueError("market's last price is not a finite number")
    anchor = recent_mean(prices, MEAN_WINDOW_MINUTES)
    # A non-finite anchor (a bad price somewhere in the window) must not poison
    # the guess into NaN -- fall back to the last close, i.e. persistence.
    if not math.isfinite(anchor):
        return price5(last)
    return price5(last + REVERSION_K * (anchor - last))


def main():
    out_dir = Path(OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    # Every case file, in name order, so two runs write the same bytes.
    inputs = sorted(Path(INPUT_DIR).glob("*.in"))
    for path in inputs:
        case_id = path.name[: -len(".in")]
        case = json.loads(path.read_text(encoding="utf-8"))
        markets = case.get("markets")
        if not isinstance(markets, list) or len(markets) != 1:
            raise ValueError(f"{path.name} does not hold exactly one market")
        price = forecast(markets[0].get("prices"))
        out = {"forecasts": [{"case": case_id, "price": price}]}
        (out_dir / f"{case_id}.out").write_text(json.dumps(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
