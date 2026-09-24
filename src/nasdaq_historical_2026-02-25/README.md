# Nasdaq matched historical data

The target valuation date in `NVDIA-Research/NVDA_2026-09-03_report.md` is February 25, 2026. `matched_trading_date.csv` contains the one regular trading-day observation on that exact date for the target (NVDA) and the selected Nasdaq-listed semiconductor peers: AMD, AVGO, and MRVL.

The `*_nasdaq_historical_raw.json` files preserve Nasdaq's downloaded historical responses. Each request began at `2026-02-25`; Nasdaq returned the date through the then-current trading day. The CSV is a normalized extract of the matching `02/25/2026` row from each response, with currency symbols and thousands separators removed for calculation.

Source endpoints (downloaded September 17, 2026):

- `https://api.nasdaq.com/api/quote/NVDA/historical?assetclass=stocks&fromdate=2026-02-25&limit=5000`
- `https://api.nasdaq.com/api/quote/AMD/historical?assetclass=stocks&fromdate=2026-02-25&limit=5000`
- `https://api.nasdaq.com/api/quote/AVGO/historical?assetclass=stocks&fromdate=2026-02-25&limit=5000`
- `https://api.nasdaq.com/api/quote/MRVL/historical?assetclass=stocks&fromdate=2026-02-25&limit=5000`

These are unadjusted daily market-activity fields as returned by Nasdaq. Peer membership is an analyst choice, not a Nasdaq classification; replace the peer tickers and repeat the matching-date pull if a different peer policy is adopted.
