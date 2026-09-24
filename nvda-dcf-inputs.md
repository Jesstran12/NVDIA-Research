# NVIDIA DCF Inputs

All dollar values are USD millions unless noted otherwise. Filing data is from NVIDIA's Form 10-K for the fiscal year ended January 25, 2026.

| DCF input | Value entered in `dcf.py` | As-of date | Source / locator | Status |
|---|---:|---|---|---|
| Starting FCFF | 96,895.9 | FY ended Jan. 25, 2026 | Consolidated Statements of Cash Flows, p. 55: operating cash flow 102,718 less capex 6,042, plus after-tax interest 219.9 (interest expense 259; 15.1% effective tax rate) | Sourced calculation |
| Growth, Years 1-5 | 8%, 6%, 5%, 4%, 3% | N/A | Item 7, Management's Discussion and Analysis, begins p. 36; it provides context but no quantitative five-year forecast | **PLACEHOLDER** |
| WACC | 10.0% | N/A | No company WACC is reported in the 10-K | **PLACEHOLDER** |
| Terminal growth | 3.0% | N/A | Long-run macroeconomic assumption; not company guidance | **PLACEHOLDER** |
| Non-operating cash | 10,605 | Jan. 25, 2026 | Consolidated Balance Sheets, p. 53: cash and cash equivalents | Sourced |
| Debt | 8,468 | Jan. 25, 2026 | Note 11 -- Debt, p. 70: net carrying amount | Sourced |
| Diluted shares | 24,514 | FY ended Jan. 25, 2026 | Note 4 -- Net Income Per Share, p. 62: diluted weighted-average shares | Sourced |

## Market Price

NVDA: **$195.56 per share** on **February 25, 2026** (reported closing/last price). Source: [Nasdaq historical-data extract](src/nasdaq_historical_2026-02-25/matched_trading_date.csv). This price matches the report's valuation date and is recorded for comparison only; it is not an input to the current `dcf.py` script.

## Peer P/E source table

**Frozen convention.** For every company, use Nasdaq's February 25, 2026 closing/last price and the latest **GAAP full-year diluted EPS publicly available on or before February 25, 2026**. The price numerator and EPS denominator are therefore not a forward-P/E convention. The `peer_valuation.py` model uses only the two candidates marked *included (qualified)* below.

| Candidate | Disposition | Price on Feb. 25, 2026 | GAAP diluted EPS used | Earnings period / availability | Reason and limitation | Sources |
|---|---|---:|---:|---|---|---|
| NVIDIA (NVDA) | Target | $195.56 | $4.90 | FY2026 ended Jan. 25, 2026; reported Feb. 25, 2026 | Target. FY diluted EPS is a trailing earnings measure, not a point-in-time share count. | [Nasdaq extract](src/nasdaq_historical_2026-02-25/matched_trading_date.csv); [NVIDIA FY2026 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/) |
| Advanced Micro Devices (AMD) | Included (qualified) | $210.86 | $2.65 | FY2025; reported Feb. 3, 2026 | Competes in data-center CPUs and AI accelerators. Qualified because its client, gaming, and embedded businesses make its earnings mix broader than NVIDIA's. | [Nasdaq extract](src/nasdaq_historical_2026-02-25/matched_trading_date.csv); [AMD FY2025 results](https://ir.amd.com/news-events/press-releases/detail/1276/amd-reports-fourth-quarter-and-full-year-2025-financial-results) |
| Broadcom (AVGO) | Included (qualified) | $332.31 | $4.77 | FY2025 ended Nov. 2, 2025; reported Dec. 11, 2025 | Supplies AI custom accelerators and networking to data centers. Qualified because infrastructure software is also a material part of its business. | [Nasdaq extract](src/nasdaq_historical_2026-02-25/matched_trading_date.csv); [Broadcom FY2025 results](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-fourth-quarter-and-fiscal-year-2025) |
| Marvell Technology (MRVL) | Excluded | $80.92 | — | Latest pre-cutoff release: Q3 FY2026, reported Dec. 2, 2025 | Data-center interconnect exposure passes the business screen, but its GAAP EPS includes a pre-tax $1.8bn gain on the sale of the automotive Ethernet business. Its next full-year result was not available by the cutoff, so it fails the frozen clean, full-year GAAP-EPS rule. | [Nasdaq extract](src/nasdaq_historical_2026-02-25/matched_trading_date.csv); [Marvell Q3 FY2026 results](https://investor.marvell.com/news-events/press-releases/detail/999/marvell-technology-inc-reports-third-quarter-of-fiscal-year-2026-financial-results) |

## Peer Valuation Calculation Results

The results below are produced by `peer_valuation.py` using the frozen February 25, 2026 Nasdaq closing prices and the latest available trailing GAAP full-year diluted EPS from the peer source table above.

| Check | Result |
|---|---:|
| AMD P/E | 79.569811x |
| Broadcom P/E | 69.666667x |
| Peer median P/E | 74.618239x |
| NVIDIA peer-implied range | $341.37–$389.89 |
| NVIDIA at peer median | $365.63 |
| Remove AMD: remaining AVGO estimate | $341.37 |
| Change from two-peer midpoint | -$24.26 |

Applying the peer median multiple (74.62x) to NVIDIA's FY2026 GAAP diluted EPS ($4.90) yields an implied equity value of **$365.63 per share**. In the single-peer stress test, removing AMD (the peer with the highest multiple) leaves Broadcom as the sole comparable, which yields an implied value of **$341.37 per share** (-$24.26 vs. midpoint). Both peer-implied values sit well above NVIDIA's observed market price of **$195.56** (which corresponds to an unadjusted trailing P/E of 39.91x).

## DCF Calculation Results

The historical starting values below are sourced from the saved NVIDIA FY2026 10-K materials in `src/10-K_FY2026/` (as documented in the input table above). The five growth rates, 10.0% WACC, and 3.0% terminal-growth rate are model assumptions, so the outputs are an illustrative valuation rather than a filing-reported result. Dollar amounts are USD millions except per-share amounts.

| Title | Result |
|---|---:|
| FCFF Year 1 | $104,647.5720 |
| FCFF Year 2 | $110,926.4263 |
| FCFF Year 3 | $116,472.7476 |
| FCFF Year 4 | $121,131.6575 |
| FCFF Year 5 | $124,765.6073 |
| PV of explicit FCFF | $434,520.7660 |
| Terminal value, Year 5 | $1,835,836.7927 |
| PV of terminal value | $1,139,910.2102 |
| Enterprise value | $1,574,430.9762 |
| Equity value | $1,576,567.9762 |
| Value per share | $64.3130 |
| PV of TV ÷ enterprise value | 72.4014% |

## Scenario Analysis

This scenario analysis appears below, and does not alter, the DCF Results above. Each case uses the same sourced starting FCFF, cash, debt, and diluted-share inputs. Amounts are USD per share.

| Scenario | FCFF growth, Years 1–5 | WACC | Terminal growth | Implied value per share | Difference vs. $195.56 market-price reference |
|---|---|---:|---:|---:|---:|
| Downside | 5%, 4%, 3%, 3%, 3% | 11.0% | 2.5% | $50.15 | ($145.41) |
| Base | 8%, 6%, 5%, 4%, 3% | 10.0% | 3.0% | $64.31 | ($131.25) |
| Upside | 15%, 12%, 10%, 8%, 6% | 8.5% | 3.0% | $101.46 | ($94.10) |
| Bull | 20%, 20%, 20%, 20%, 20% | 8.0% | 3.0% | $165.39 | ($30.17) |

### WACC and Terminal-Growth Sensitivity

This table holds the base FCFF-growth path (8%, 6%, 5%, 4%, 3%) constant and varies only WACC and terminal growth. Each cell is the implied value per share.

| WACC \ Terminal growth | 2.0% | 3.0% | 4.0% |
|---|---:|---:|---:|
| 8.0% | $77.67 | $90.14 | $108.85 |
| 9.0% | $66.49 | $75.07 | $87.09 |
| 10.0% | $58.11 | $64.31 | $72.59 |
| 11.0% | $51.59 | $56.24 | $62.23 |
| 12.0% | $46.37 | $49.97 | $54.46 |

The current market-price reference is above every illustrative scenario. That gap means the price may reflect stronger or more durable cash-flow expectations, a lower required return, different cash-flow normalization, or a combination of these. This is an educational sensitivity analysis, not a price target or investment recommendation.
