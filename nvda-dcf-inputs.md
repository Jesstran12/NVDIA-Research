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

NVDA: **$218.07 per share** on **September 10, 2026** (reported closing/last price). Source: [Investing.com historical data](https://www.investing.com/equities/nvidia-corp-historical-data?symbol=NVDA). This market price is recorded for comparison only and is not an input to the current `dcf.py` script.

## DCF Calculation Results

The historical starting values below are sourced from the saved NVIDIA FY2026 10-K materials in `nvda-20260125_files` (as documented in the input table above). The five growth rates, 10.0% WACC, and 3.0% terminal-growth rate are model assumptions, so the outputs are an illustrative valuation rather than a filing-reported result. Dollar amounts are USD millions except per-share amounts.

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

| Scenario | FCFF growth, Years 1–5 | WACC | Terminal growth | Implied value per share | Difference vs. $218.07 market-price reference |
|---|---|---:|---:|---:|---:|
| Downside | 5%, 4%, 3%, 3%, 3% | 11.0% | 2.5% | $50.15 | ($167.92) |
| Base | 8%, 6%, 5%, 4%, 3% | 10.0% | 3.0% | $64.31 | ($153.76) |
| Upside | 15%, 12%, 10%, 8%, 6% | 8.5% | 3.0% | $101.46 | ($116.61) |
| Bull | 20%, 20%, 20%, 20%, 20% | 8.0% | 3.0% | $165.39 | ($52.68) |

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
