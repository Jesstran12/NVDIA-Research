"""Regression beta for NVIDIA against the S&P 500 (SPY proxy).

Beta is the slope of a least-squares regression of the stock's periodic
returns on the market's periodic returns:

    beta = Cov(R_stock, R_market) / Var(R_market)

Standard library only, like dcf.py. Prices come from the same Nasdaq
historical endpoint used for src/nasdaq_historical_2026-02-25/. Each raw
response is cached in src/beta_prices/ so the regression is reproducible
without a network connection; delete a cached file to refresh it.

Usage:
    python3 beta.py                 # 5 years of monthly returns (default)
    python3 beta.py --weekly        # 2 years of weekly returns
    python3 beta.py --years 3       # override the look-back window
    python3 beta.py --market QQQ    # Nasdaq-100 proxy instead of SPY
"""

import argparse
import datetime as dt
import json
import math
import os
import urllib.request


# Edit these inputs by hand.
STOCK = "NVDA"
MARKET = "SPY"  # ETF proxy for the S&P 500; Nasdaq's index endpoint is not public
MARKET_ASSET_CLASS = "etf"
YEARS = 5  # look-back window for monthly returns
WEEKLY_YEARS = 2  # look-back window for weekly returns
AS_OF = dt.date.today()  # end of the estimation window

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "beta_prices")
NASDAQ_URL = (
    "https://api.nasdaq.com/api/quote/{ticker}/historical"
    "?assetclass={asset_class}&fromdate={start}&todate={end}&limit=5000"
)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept": "application/json",
}


def fetch_prices(ticker, asset_class, start, end):
    """Return {date: close} for the ticker, reading the cache first."""
    os.makedirs(DATA_DIR, exist_ok=True)
    cache_path = os.path.join(DATA_DIR, f"{ticker}_{start}_{end}_nasdaq_historical_raw.json")
    if os.path.exists(cache_path):
        with open(cache_path) as handle:
            payload = json.load(handle)
    else:
        url = NASDAQ_URL.format(ticker=ticker, asset_class=asset_class, start=start, end=end)
        request = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
        with open(cache_path, "w") as handle:
            json.dump(payload, handle)

    rows = ((payload.get("data") or {}).get("tradesTable") or {}).get("rows") or []
    if not rows:
        raise SystemExit(f"No price rows returned for {ticker}; check the ticker and asset class.")

    prices = {}
    for row in rows:
        date = dt.datetime.strptime(row["date"], "%m/%d/%Y").date()
        prices[date] = float(row["close"].replace("$", "").replace(",", ""))
    return prices


def period_end_prices(prices, frequency):
    """Keep the last available close in each calendar month or ISO week."""
    if frequency == "monthly":
        key = lambda date: (date.year, date.month)
    else:
        key = lambda date: date.isocalendar()[:2]
    last_close = {}
    for date in sorted(prices):
        last_close[key(date)] = (date, prices[date])
    return [last_close[period] for period in sorted(last_close)]


def simple_returns(series):
    """Percentage change between consecutive period-end closes."""
    return [
        (series[i][0], series[i][1] / series[i - 1][1] - 1)
        for i in range(1, len(series))
    ]


def align(stock_returns, market_returns):
    """Pair returns whose period-end dates match on both sides."""
    market_by_period = {date: value for date, value in market_returns}
    pairs = [(value, market_by_period[date]) for date, value in stock_returns if date in market_by_period]
    return [pair[0] for pair in pairs], [pair[1] for pair in pairs]


def regress(y, x):
    """Ordinary least squares of y on x. Returns slope, intercept, R^2, standard error of slope."""
    n = len(x)
    if n < 3:
        raise SystemExit("Not enough overlapping returns to run a regression.")
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    covariance = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / (n - 1)
    variance_x = sum((xi - mean_x) ** 2 for xi in x) / (n - 1)
    slope = covariance / variance_x
    intercept = mean_y - slope * mean_x
    residual_ss = sum((yi - intercept - slope * xi) ** 2 for xi, yi in zip(x, y))
    total_ss = sum((yi - mean_y) ** 2 for yi in y)
    r_squared = 1 - residual_ss / total_ss if total_ss else float("nan")
    standard_error = math.sqrt(residual_ss / (n - 2) / (variance_x * (n - 1)))
    return slope, intercept, r_squared, standard_error


def compute_beta(stock, market, market_asset_class, frequency, years, as_of):
    start = as_of.replace(year=as_of.year - years)
    stock_prices = fetch_prices(stock, "stocks", start.isoformat(), as_of.isoformat())
    market_prices = fetch_prices(market, market_asset_class, start.isoformat(), as_of.isoformat())

    stock_returns = simple_returns(period_end_prices(stock_prices, frequency))
    market_returns = simple_returns(period_end_prices(market_prices, frequency))
    y, x = align(stock_returns, market_returns)

    beta, alpha, r_squared, standard_error = regress(y, x)
    return {
        "frequency": frequency,
        "start": min(stock_prices),
        "end": max(stock_prices),
        "observations": len(x),
        "beta": beta,
        "alpha": alpha,
        "r_squared": r_squared,
        "standard_error": standard_error,
        "adjusted_beta": 2 / 3 * beta + 1 / 3,  # Blume adjustment toward 1.0
        "stock_volatility": math.sqrt(sum((v - sum(y) / len(y)) ** 2 for v in y) / (len(y) - 1)),
        "market_volatility": math.sqrt(sum((v - sum(x) / len(x)) ** 2 for v in x) / (len(x) - 1)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--weekly", action="store_true", help="use weekly returns (default window: 2 years)")
    parser.add_argument("--years", type=int, help="look-back window in years")
    parser.add_argument("--market", default=MARKET, help="market proxy ticker (default SPY)")
    parser.add_argument("--stock", default=STOCK, help="stock ticker (default NVDA)")
    args = parser.parse_args()

    frequency = "weekly" if args.weekly else "monthly"
    years = args.years or (WEEKLY_YEARS if args.weekly else YEARS)
    result = compute_beta(args.stock, args.market, MARKET_ASSET_CLASS, frequency, years, AS_OF)

    print(f"{args.stock} beta versus {args.market}, {result['frequency']} returns")
    print(f"Window: {result['start']} to {result['end']} ({result['observations']} return observations)")
    print(f"Raw regression beta: {result['beta']:.4f}")
    print(f"Standard error of beta: {result['standard_error']:.4f}")
    print(f"95% confidence range: {result['beta'] - 1.96 * result['standard_error']:.4f} to "
          f"{result['beta'] + 1.96 * result['standard_error']:.4f}")
    print(f"Blume adjusted beta (2/3 raw + 1/3): {result['adjusted_beta']:.4f}")
    print(f"Alpha per period: {result['alpha']:.4f}")
    print(f"R-squared: {result['r_squared']:.4f}")
    print(f"Stock volatility per period: {result['stock_volatility']:.4f}")
    print(f"Market volatility per period: {result['market_volatility']:.4f}")


if __name__ == "__main__":
    main()
