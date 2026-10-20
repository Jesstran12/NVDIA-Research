# NVIDIA (NVDA) — Project 1 visible executed output
Run 2026-10-19T21:22:29-04:00 at commit `fb23806` with Python 3.13.5; engine engine.py over nvda_proforma.py (Lab 10) and proforma.py (Lab 09). USD millions unless stated. Learning demonstration for FIN 43900, not investment advice.

## Decision

**Do not initiate at this price; keep on watch** — the price sits above the high case: it already pays for more than the compounding-cycle scenario delivers.

| Item | Value |
|---|---|
| Intended user | Buy-side investment committee; the fund holds no position in NVIDIA |
| Decision | Initiate a position, place the name on watch/defer, or do not initiate, at the 23 Sep 2026 price |
| Horizon | Three- to five-year holding period; next review after the Q3 and Q4 FY2027 reports (Nov 2026, Feb 2027) |
| Valuation date / price | 2026-09-23 / $225.51 (Nasdaq historical close, cached in src/beta_prices/NVDA_2021-09-24_2026-09-24_nasdaq_historical_raw.json) |
| Currency and units | USD millions; per-share values in USD |
| Share basis | 24,100m shares outstanding (10-Q cover, 21 Aug 2026) + 95m dilutive award increment (Q2 FY2027 Note 4) = 24,195m diluted |
| Value per share, base | **$123.93** (-45.0% vs price) |
| Causal range (low / base / high) | $80.31 / $123.93 / $186.63 |
| Committee ask | Approve watch/defer: no position now; authorise a re-review within one week of the Q3 FY2027 report with the tool re-run on the new filing. |
| Checks | all pass |

**Conditions:** Initiate only if the price falls below the base case ($124) with the checks still passing, or if two quarterly reports move the growth path enough to lift the high case above the price. Hold the watch posture while Data Center revenue keeps growing quarter on quarter and gross margin guidance stays at or above 72%.

**Reversal triggers (metric · threshold · window · effect):**

- Data Center revenue, quarter on quarter · any decline · next two quarterly reports (Nov 2026, Feb 2027) · withdraw the base case and rebuild as the low case (about $80)
- Gross margin guidance · below 72% and falling · next two quarterly reports · move the gross-margin path down 3 pp (about -$12 at base)
- Operating expenses vs revenue · opex growing faster than revenue for two quarters · next two quarterly reports · opex path +2 pp (about -$5 at base)
- Enterprise-to-equity bridge · fails to reconcile after the next 10-Q (new debt, buybacks, securities) · each filing · reject the per-share conclusion until the bridge reconciles

**Exclusions:** Equity-stake gains (9.0bn in FY2026, 23.7bn in H1 FY2027) are not forecast: a gain is not a cash flow. Non-marketable equity securities (22.3bn at FY2026; 51.2bn at Q2 FY2027) are left out of the bridge: no observable price. Operating leases are not treated as debt (ASC 842 lease liabilities sit in other liabilities, as NVIDIA reports them). No transaction (M&A) multiples: no defensible control transaction for a $5tn accelerated-computing business exists. Information after 23 Sep 2026 is not used; the model runs on filings to the Q2 FY2027 10-Q (filed 26 Aug 2026).

## Checks (computed on this run)

| Status | Check | Detail |
|---|---|---|
| PASS | Every driver inside its defended bounds | all drivers inside the bounds recorded in the assumption-challenge record |
| PASS | Balance sheet balances every year | largest |assets - liabilities - equity| = 0.0 |
| PASS | Cash flow ties to balance-sheet cash | largest tie residual = 0.0 |
| PASS | PP&E roll-forward | largest residual = 0.0 |
| PASS | Debt roll-forward | largest residual = 0.0 |
| PASS | Base year reconciles to the FY2026 10-K | opening balance sheet = filed totals (assets 206,803; liabilities 49,510; equity 157,293) |
| PASS | Cash stays above the 8,000 floor without the commercial-paper backstop | commercial paper drawn: 0; lowest cash vs floor: +12,693 |
| PASS | Terminal growth below the discount rate | g = 3.00% vs WACC = 11.99% |
| PASS | Bridge balance sheet dated at the start of the projected cash flows | bridge at 25 Jan 2026 = the pro-forma opening date; every FY2027E cash flow is ahead of it |
| PASS | Explicit FCFF positive in every year | non-positive years: none |
| PASS | Enterprise-to-equity bridge reconciles | EV 2,944,373 + cash & securities 62,556 - debt 8,468 = equity 2,998,461 |
| PASS | Terminal share of enterprise value below 85% | 67.6% of EV sits after FY2031E |
| PASS | gross margin inside the historical band | path 74.5%, 73.0%, 72.0%, 71.0%, 70.0% vs band 56.9%-78.5% (FY2023 56.9% trough (FY2024 10-K) to 78.5%, 3.5 points above the best quarter reported (75.0%, Q2 FY2027)) |
| PASS | opex ratio inside the historical band | path 8.7%, 9.5%, 10.5%, 11.5%, 12.5% vs band 6.5%-18.6% (the FY2027E run-rate 8.7% less 2 points (NVIDIA has never filed a year below 10.7%) to FY2024 18.6%) |
| PASS | tax rate inside the historical band | path 17.0% vs band 12.0%-21.0% (FY2024 12.0% to the 21% statutory rate) |
| PASS | capex ratio inside the historical band | path 2.8% vs band 1.5%-6.0% (FY2024 1.8%; MD&A says capex rises in FY2027) |
| PASS | sbc ratio inside the historical band | path 2.5% vs band 1.5%-6.0% (H1 FY2027 2.2% to FY2024 5.8%) |
| PASS | No projected year with revenue below the FY2026 base | lowest projected revenue 400,781 vs FY2026 215,938 |

## Driver panel — value · basis · bounds · challenge · evidence that would change it

| Driver | Base value | Basis | Defended bounds | Why these bounds | Challenge | Evidence to change it |
|---|---|---|---|---|---|---|
| Revenue growth FY2028E-FY2031E, shift (pp) | +0.0 pp (base path 25 / 12 / 7 / 4 %) | judgment | -25.0 pp to +25.0 pp | -25 pp makes FY2028E flat (0%) and the later years shrink: the "AI capex stops" case. +25 pp is one point above the growth the market price implies (reverse DCF); nothing in the filings supports more. | Two customers are 36% of revenue (FY2026 10-K MD&A p. 41); hyperscaler capex cannot compound at 65-85% for long. | Data Center revenue growth in the next two quarterly reports; hyperscaler capex guidance. |
| FY2027E revenue vs base (Q4 judgment), % | 0.00% (H1 actual 177,837 + Q3 outlook 108,000 + Q4 judgment 115,000) | guidance + judgment | -10.00% to 10.00% | Q3 is guided within +/-2%; only Q4 (14 weeks) is judgment, so +/-10% of the year is the widest a miss or beat could plausibly reach. | Q4 FY2027 has no guidance yet; export controls on China Data Center compute remain in the outlook. | Q3 FY2027 results and the Q4 outlook (expected November 2026). |
| Gross margin, shift (pp, all years) | +0.0 pp (base path 74.5 -> 70.0 %) | judgment | -13.0 pp to +4.0 pp | -13 pp takes FY2031E to 57.0%, FY2023's 56.9% trough (the last cycle low, FY2024 10-K); +4 pp caps the first year at 78.5%, above any quarter NVIDIA has reported. | Custom silicon (Broadcom-built accelerators) and AMD compete for the same racks; CUDA lock-in is a judgment, not a filing claim. | Gross-margin guidance below 72% and falling; Data Center pricing disclosures. |
| Operating expenses / revenue, shift (pp, all years) | +0.0 pp (base path 8.7 -> 12.5 %) | judgment | -2.0 pp to +6.0 pp | -2 pp is below the H1 FY2027 run-rate of 9.0%; +6 pp returns FY2031E to FY2024's 18.6%. | Opex grew 41% in FY2026 (compensation, compute, infrastructure); the one-year product cadence keeps R&D rising. | Opex growing faster than revenue for two consecutive quarters. |
| Tax rate (all years) | 17.00% (Q2 FY2027 release: FY2027 GAAP rate 16-18%) | guidance | 12.00% to 21.00% | FY2024 was 12.0%; 21% is the statutory rate with no FDDEI, SBC or R&D benefit. | FDDEI and SBC benefits shrink as the mix changes; the rate rose each of the last three years. | Effective rate in the next 10-K; tax-law changes. |
| Capital spending / revenue | 2.80% (FY2026 2.8%) | history | 1.50% to 6.00% | FY2024 1.8% is the low; 6% is double the FY2026 ratio, the most a fabless company has needed. | MD&A says capex will increase in FY2027; a ratio on 86% revenue growth already delivers 11.2bn. | Purchases of property and equipment in the cash flow statement; any move to own fabs. |
| Stock-based compensation / revenue | 2.50% (FY2026 3.0%, H1 FY2027 2.2%) | judgment | 1.50% to 6.00% | H1 FY2027 2.2% is the low; FY2024 5.8% is the high of the three filed years. | SBC is added back as non-cash; treat it as a cash cost (toggle) and value falls. | SBC line in the cash flow statement; share count after buybacks. |
| Cost of equity | 12.00% (judgment between the tutorial 10% and the measured CAPM 13-14.8%) | judgment | 9.00% to 16.00% | 9% is a beta of about 0.9 (below the market); 16% is the observed beta 2.21 plus one standard error (2.5) at rf 5% + ERP 4.42%. | beta.py measures 2.21 raw (s.e. 0.30), 1.81 Blume; CAPM gives 13.0-14.8%, so 12% is the generous end. | Re-estimated beta each quarter; the ten-year Treasury yield. |
| Terminal growth after FY2031E | 3.00% (long-run nominal growth) | judgment | 0.00% to 4.00% | 0% is a flat industry after the build-out; 4% is about nominal GDP, the most a going concern can hold forever. | In FY2031E the model reinvests 2.5% of net income and grows 3% forever, a 118% return on retained cash. | Terminal growth must stay below the discount rate; the check refuses otherwise. |

## Five-year pro-forma (Lab 10 engine, base assumptions)

| | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E |
|---|---:|---:|---:|---:|---:|
| Revenue | 400,781 | 500,976 | 561,093 | 600,370 | 624,385 |
| Gross profit | 298,582 | 365,713 | 403,987 | 426,263 | 437,069 |
| Operating expenses | 34,868 | 47,593 | 58,915 | 69,043 | 78,048 |
| Operating income | 263,714 | 318,120 | 345,072 | 357,220 | 359,021 |
| Net income | 220,485 | 265,960 | 288,706 | 299,237 | 301,173 |
| Cash | 20,693 | 33,602 | 47,964 | 63,146 | 78,529 |
| Receivables | 71,393 | 89,241 | 99,950 | 106,947 | 111,224 |
| Inventory | 35,012 | 46,339 | 53,822 | 59,647 | 64,171 |
| PP&E and intangibles | 19,414 | 25,647 | 31,062 | 35,405 | 38,679 |
| Total assets | 269,152 | 317,469 | 355,439 | 387,784 | 415,243 |
| Notes | 7,468 | 7,468 | 6,218 | 6,218 | 4,718 |
| Commercial paper drawn | 0 | 0 | 0 | 0 | 0 |
| Equity | 196,125 | 229,342 | 259,187 | 284,979 | 309,489 |
| Total liabilities & equity | 269,152 | 317,469 | 355,439 | 387,784 | 415,243 |
| Free cash flow to equity | 201,760 | 258,176 | 287,250 | 303,636 | 307,656 |
| Assets − liabilities − equity | 0.0 | -0.0 | 0.0 | 0.0 | 0.0 |
| Cash: balance sheet vs cash flow | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## FCFF, WACC and the enterprise-to-equity bridge

| | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E |
|---|---:|---:|---:|---:|---:|
| EBIT (operating income) | 263,714 | 318,120 | 345,072 | 357,220 | 359,021 |
| NOPAT = EBIT × (1 − t) | 218,882 | 264,039 | 286,410 | 296,493 | 297,988 |
| + D&A | 5,489 | 7,785 | 10,284 | 12,456 | 14,197 |
| + SBC add-back | 10,020 | 12,524 | 14,027 | 15,009 | 15,610 |
| − Capital spending | 11,214 | 14,017 | 15,700 | 16,799 | 17,470 |
| − Working-capital build | 22,020 | 14,075 | 8,817 | 6,267 | 4,354 |
| FCFF | 201,158 | 256,256 | 286,205 | 300,892 | 305,970 |

| WACC input | Value |
|---|---|
| Cost of equity (driver) | 12.00% |
| Cost of debt, pre-tax / after-tax | 2.92% / 2.42% (principal-weighted effective rate of the seven note series outstanding at 25 Jan 2026 (Q2 FY2027 10-Q Note 9): 2.92%) |
| Market value of equity / debt | 5,434,791 / 8,468 (weights 99.84% / 0.16%) |
| **WACC** | **11.99%** |

| Valuation | USD millions |
|---|---:|
| PV of FY2027E–FY2031E FCFF | 952,820 |
| FY2032 cash flow = FY2031E FCFF × (1 + g) | 315,149 |
| Terminal value at FY2031E (g = 3.0%) | 3,507,462 |
| PV of terminal value | 1,991,552 (67.6% of enterprise value) |
| **Enterprise value** | **2,944,373** |
| + Cash and marketable debt securities (2026-01-25) | 49,670 |
| + Marketable equity securities | 12,886 |
| − Debt, carrying (short-term 999 + long-term 7,469; Note 11 pp. 69-70) | 8,468 |
| **Equity value** | **2,998,461** |
| Diluted shares (millions) | 24,195 |
| **Value per share** | **$123.93** |
| FCFE cross-check (Lab 10, 12% / 3%) | $123.05 |
| Bridge source | Form 10-K FY2026, accession 0001045810-26-000021, balance sheet p. 53; Q2 FY2027 10-Q comparative column |

## Causal cases

| Case | What moves | $/share | FY2031E revenue | FY2031E FCFF | Terminal share | Checks |
|---|---|---:|---:|---:|---:|---|
| Low — AI capex digestion and custom-silicon share loss | Hyperscalers pause after FY2027 (growth path 15 / 2 / -3 / -6 %), custom accelerators and AMD take price (gross margin -3 pp), R&D keeps rising into slower revenue (opex +1 pp), and the market demands the measured CAPM rate (13%). | 80.31 | 428,652 | 203,867 | 60.5% | pass |
| Base — Lab 10 assumption set | The labelled base case: growth 25 / 12 / 7 / 4 %, gross margin 74.5 -> 70 %, 12% cost of equity, 3% terminal growth. | 123.93 | 624,385 | 305,970 | 67.6% | pass |
| High — the compute cycle keeps compounding and CUDA holds price | Data Center spending compounds (growth path 35 / 22 / 17 / 14 %), pricing power holds (gross margin +1.5 pp), and the market accepts a lower required return (11%). | 186.63 | 880,423 | 429,753 | 73.8% | pass |

## WACC × terminal growth, $ per share (base in bold)

Rows are the cost-of-equity driver; the WACC it produces (debt weight 0.16%) is shown beside it.

| Cost of equity (WACC) \ g | 0.0% | 1.0% | 2.0% | 3.0% | 4.0% |
|---|---:|---:|---:|---:|---:|
| 10.0% (9.99%) | 122.5 | 132.1 | 144.1 | 159.6 | 180.2 |
| 11.0% (10.99%) | 111.0 | 118.6 | 127.9 | 139.5 | 154.5 |
| 12.0% (11.99%) | 101.5 | 107.6 | 115.0 | **123.9** | 135.1 |
| 13.0% (12.98%) | 93.5 | 98.5 | 104.4 | 111.5 | 120.1 |
| 14.0% (13.98%) | 86.6 | 90.7 | 95.6 | 101.3 | 108.1 |
| 15.0% (14.98%) | 80.7 | 84.1 | 88.1 | 92.8 | 98.3 |

## One-at-a-time sensitivity at the defended bounds (base $123.93)

| Driver | Low input → $/share | High input → $/share | Span $/share | Span FY2031E op. income | Span FY2031E FCFF |
|---|---|---|---:|---:|---:|
| Revenue growth FY2028E-FY2031E, shift (pp) | -25.0 pp → 62.73 | +25.0 pp → 232.54 | 169.81 | 676,522 | 518,873 |
| Cost of equity | 9.00% → 186.35 | 16.00% → 85.59 | 100.77 | 0 | 0 |
| Gross margin, shift (pp, all years) | -13.0 pp → 96.69 | +4.0 pp → 132.31 | 35.62 | 106,145 | 88,858 |
| Terminal growth after FY2031E | 0.00% → 101.53 | 4.00% → 135.14 | 33.61 | 0 | 0 |
| FY2027E revenue vs base (Q4 judgment), % | -10.00% → 111.93 | 10.00% → 135.93 | 24.01 | 71,804 | 61,053 |
| Operating expenses / revenue, shift (pp, all years) | -2.0 pp → 128.02 | +6.0 pp → 111.67 | 16.35 | 49,951 | 41,459 |
| Tax rate (all years) | 12.00% → 131.16 | 21.00% → 118.14 | 13.02 | 0 | 32,312 |
| Stock-based compensation / revenue | 1.50% → 121.47 | 6.00% → 132.55 | 11.08 | 0 | 28,097 |
| Capital spending / revenue | 1.50% → 124.97 | 6.00% → 121.35 | 3.63 | 0 | 6,401 |

Ranking at the full bounds: growth_shift > cost_of_equity > gross_margin_shift > terminal_growth > fy27_revenue_pct > opex_shift > tax_rate > sbc_ratio > capex_ratio. At half the bounds: growth_shift > cost_of_equity > terminal_growth > gross_margin_shift > fy27_revenue_pct > opex_shift > tax_rate > sbc_ratio > capex_ratio. At the Lab 11 ranges (±5 pp growth, ±3 pp gross margin): growth_shift > gross_margin_shift (spans $32.77 and $12.57). The top driver is the same under all three range choices; over these ranges the growth path after FY2027 carries the value, and the ranking below it depends on how wide each bound is.

## Reverse DCF — what $225.51 assumes, one driver at a time (all others at base)

| Driver | Base | Implied by the price | Inside defended bounds? |
|---|---|---|---|
| Revenue growth FY2028E-FY2031E, shift (pp) | +0.0 pp | +23.7 pp | yes |
| Cost of equity | 12.00% | 7.96% | no — outside the defended bounds (0.09, 0.16); searched (0.04, 0.16) to report what the price assumes |
| Terminal growth after FY2031E | 3.00% | 7.78% | no — outside the defended bounds (0.0, 0.04); searched (0.0, 0.1) to report what the price assumes |
| Gross margin, shift (pp, all years) | +0.0 pp | not reachable in (-0.15, 0.25) | no — outside the defended bounds (-0.13, 0.04); searched (-0.15, 0.25) to report what the price assumes |
| Operating expenses / revenue, shift (pp, all years) | +0.0 pp | not reachable in (-0.09, 0.06) | no — outside the defended bounds (-0.02, 0.06); searched (-0.09, 0.06) to report what the price assumes |

## What would reverse the call — the smallest change that lifts value to the price

The downside cases cannot alter a do-not-initiate call; the scenario that would is on the upside. Each row is a full rerun with checks.

| Scenario | Growth shift needed | Resulting FY2028E–FY2031E path | FY2031E revenue | $/share | Checks |
|---|---|---|---:|---:|---|
| Growth path alone, everything else at base | +23.7 pp a year | 49% / 36% / 31% / 28% | 1,350,543 | 225.51 | pass |
| Growth path on top of the high case (gross margin +1.5 pp, cost of equity 11%) | +17.4 pp a year | 42% / 29% / 24% / 21% | 1,114,912 | 225.51 | pass |

Monitoring: the Q3 and Q4 FY2027 reports show whether Data Center growth is tracking the +17 pp path (about 42% in FY2028E) or the base 25%; the call is reviewed on each report, with the tool re-run on the new filing.

## Comparable companies (policy frozen before the numbers)

Policy carried from Lab 7-8 (frozen 25 Feb 2026) and re-dated to the 23 Sep 2026 valuation date; the rules below were fixed before the multiples were computed.

- Business test: a listed operating company whose largest profit pool is accelerated-computing silicon sold into data centers (same customers, same capex budgets).
- Earnings basis: GAAP diluted EPS and GAAP operating income, trailing twelve months to the latest 10-Q filed on or before the valuation date; no adjusted figures.
- Price basis: Nasdaq close on the same trading day for every company (23 Sep 2026).
- Enterprise value = market capitalisation on the cover-page share count + total debt (carrying) - cash, cash equivalents and short-term investments; no leases, no equity stakes.
- A multiple above 100x is reported but marked not meaningful: at that level trailing earnings are too small relative to price to say anything about NVIDIA.
- Qualified peers are used, not dropped; the qualification is stated beside the result.
- No transaction (M&A) evidence: no control transaction of a comparable accelerated-computing business exists; a control premium cannot be defended for a $5tn target.

| Company | Disposition | Price 23 Sep 2026 | TTM GAAP EPS | TTM EBIT | Op. margin | Enterprise value | P/E | EV/EBIT | Basis |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| NVIDIA (target) | — | 225.51 | 7.91 | 197,579 | 65.2% | 5,411,571 | 28.5x | 27.4x | four quarters to 26 Jul 2026: FY2026 10-K less H1 FY2026 plus H1 FY2027 (10-Q filed 2026-08-26) |
| AMD | included (qualified) | 614.61 | 3.90 | 6,488 | 15.7% | 993,450 | 157.6x (not meaningful) | 153.1x (not meaningful) | FY2025 (10-K filed 2026-02-04) less H1 2025 plus H1 2026 (10-Q filed 2026-08-05); balance sheet 27 Jun 2026; cover shares 29 Jul 2026 |
| AVGO | included (qualified) | 354.99 | 7.84 | 42,814 | 48.0% | 1,730,035 | 45.3x | 40.4x | FY2025 (10-K filed 2025-12-18) less 9M FY2025 plus 9M FY2026 (10-Q filed 2026-09-10); balance sheet 2 Aug 2026; cover shares 28 Aug 2026 |
| MRVL | excluded | — | — | — | — | — | — | — | Passes the business screen (data-center interconnect) but its GAAP earnings carry the gain on the automotive Ethernet sale; excluded under the clean-GAAP rule as in Lab 8. |

| Peer | NVIDIA value implied by its P/E | by its EV/EBIT |
|---|---:|---:|
| AMD | not meaningful | not meaningful |
| AVGO | $358.16 | $332.24 |

Peer qualifications: **AMD** — Data-center GPUs and CPUs compete for the same racks. Qualified: client, gaming and embedded segments make the earnings mix broader, and acquired-intangible amortisation (2.3bn in FY2025) depresses GAAP earnings. **AVGO** — Custom AI accelerators and data-center networking. Qualified: infrastructure software (VMware) is a large part of profit, and 8bn a year of acquired-intangible amortisation depresses GAAP earnings. **MRVL** — Passes the business screen (data-center interconnect) but its GAAP earnings carry the gain on the automotive Ethernet sale; excluded under the clean-GAAP rule as in Lab 8.

## Why the methods disagree (not averaged)

- FCFF DCF (base $124; causal range $80-$187) values the cash flows the filings and guidance support; it assumes growth decelerates from 25% to 4% after FY2027 and a 12% cost of equity.
- The FCFE cross-check from Lab 10 gives $123.05: the two cash-flow definitions agree within a dollar because NVIDIA carries almost no net debt.
- Trailing GAAP multiples disagree with the DCF in both directions. NVIDIA itself trades at 28.5x trailing earnings and 27.4x trailing EBIT; Broadcom at 45.3x and 40.4x, which applied to NVIDIA's trailing figures implies $358 (P/E) and $332 (EV/EBIT). AMD's 158x P/E and 153x EV/EBIT are reported but not meaningful: its 16% operating margin against NVIDIA's 65% means the market is capitalising a recovery, not current earnings.
- Why they disagree: a trailing multiple capitalises last year's earnings at whatever growth the market expects of the peer; the DCF capitalises my explicit growth path. The peer multiples say the market expects NVIDIA's earnings to keep compounding well past FY2028; the DCF says the filings do not yet show that. The methods are not averaged: the DCF is the supported value, the multiples describe what the price is paying for.
- Reverse DCF puts the disagreement in operating language: the price needs about +24 pp more growth in each of FY2028-FY2031 (a path near 49%, 36%, 31%, 28%), or a cost of equity near 8.0%, or terminal growth near 7.8%; no gross-margin or opex assumption inside the defended bounds reaches it.

## Sources and as-of boundary

- Form 10-K FY2026, accession 0001045810-26-000021, balance sheet p. 53; Q2 FY2027 10-Q comparative column
- Nasdaq historical close, cached in src/beta_prices/NVDA_2021-09-24_2026-09-24_nasdaq_historical_raw.json; course convention: 10-year Treasury 5.00%, implied equity risk premium 4.42% (July 2026), Week 5 tutorial
- FY2024-FY2026 10-Ks (accessions 0001045810-24-000029, -25-000023, -26-000021) for the history grid in nvda-proforma.md
- Q1 and Q2 FY2027 10-Qs (0001045810-26-000052, -26-000075) and the Q2 FY2027 press release (8-K 0001045810-26-000073, 26 Aug 2026) for H1 actuals, the Q3 outlook and the share count
- Peer figures: SEC XBRL companyfacts for AMD (CIK 0000002488) and Broadcom (CIK 0001730168), extracted to src/sec_xbrl/companyfacts_extract.csv; Nasdaq closes 23 Sep 2026 cached in src/beta_prices/
- Full evidence ledger: docs/evidence-ledger.csv; base-year normalization (one-time items, basis changes, mechanical checks): docs/base-year-normalization.md
