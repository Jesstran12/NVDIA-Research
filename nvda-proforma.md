# NVIDIA (NVDA) — Pro-Forma Valuation, Base Case

**Lab 10 — your company through it.** NVIDIA's filings become a labelled assumption set, five projected fiscal years (FY2027E–FY2031E) of statements that balance, and one value per share.

Model: [`nvda_proforma.py`](nvda_proforma.py) (standard library only; `python3 nvda_proforma.py`, and `--break` to watch the check refuse). Part 2, taking the base case apart: [`nvda_whatif.py`](nvda_whatif.py) and [`nvda-whatif.md`](nvda-whatif.md). The engine was checked against the course tutorial's published known answer to the cent before NVIDIA's inputs went in.

USD millions unless stated. NVIDIA's fiscal year ends on the last Sunday in January: FY2026 ended 25 Jan 2026, so the five projected years are FY2027E–FY2031E. Learning demonstration, not investment advice.

## The line that makes NVIDIA different

**NVIDIA has no floor plan and almost no debt; the line to model is stock-based compensation together with a self-funded working-capital build.** A dealer's inventory is funded by lenders. NVIDIA's $27 billion FY2026 increase in receivables and inventory was funded from its own operating cash, and its recurring non-cash charge is not an impairment but $6.4 billion of stock-based compensation (SBC): inside operating expenses in the income statement, added back in the cash flow, credited to paid-in capital on the balance sheet, and paid for in cash through buybacks. Three smaller differences follow from the filings and are modelled consistently:

- **Investment portfolio.** $62.6 billion of cash and marketable securities earns interest income ($2.3 billion in FY2026). Marketable securities are held flat; surplus cash lands in the cash line and earns 3.5%.
- **Equity-stake gains are not projected.** Other income was $9.0 billion in FY2026 and $23.7 billion in H1 FY2027, almost all unrealised gains on equity securities (Note 7–8, and the Q1/Q2 FY2027 releases). A gain is not a forecast.
- **Depreciation is not a separate line.** NVIDIA reports D&A inside cost of revenue and operating expenses, so operating income is gross profit less operating expenses; D&A appears only in the cash-flow add-back and the PP&E roll-forward. Debt repays on the Note 11 maturity ladder instead of a flat amount; the $25 billion commercial-paper program is the backstop line.

## R.1 History grid — three years from the filings

| Line | FY2024 (28 Jan 2024) | FY2025 (26 Jan 2025) | FY2026 (25 Jan 2026) | Where it comes from |
|---|---:|---:|---:|---|
| Revenue | 60,922 | 130,497 | 215,938 | Consolidated Statements of Income, FY2026 10-K p. 51 (three years shown) |
| Gross profit | 44,301 | 97,858 | 153,463 | Income statement, p. 51 |
| Operating expenses (R&D + SG&A) | 11,329 | 16,405 | 23,076 | Income statement, p. 51 — NVIDIA's cost line; it has no separate SG&A-to-gross-profit habit |
| Net income | 29,760 | 72,880 | 120,067 | Income statement, p. 51 |
| Inventory | 5,282 ᵖ | 10,080 | 21,403 | Balance sheet, p. 53 (FY2025, FY2026); FY2024 from the SEC XBRL companyfacts feed of the FY2025 10-K |
| Property & equipment, net | 3,914 ᵖ | 6,283 | 10,383 | Balance sheet, p. 53; FY2024 as above |
| Shareholders' equity | 42,978 | 79,327 | 157,293 | Balance sheet, p. 53; FY2024 from the Statement of Shareholders' Equity, p. 54 ("Balances as of Jan 28, 2024") |
| Accounts receivable | 9,999 ᵖ | 23,065 | 38,466 | Balance sheet, p. 53; FY2024 as above |
| Cash and cash equivalents | 7,280 | 8,589 | 10,605 | Cash flow statement, p. 55 (end-of-period cash, three years) |
| Marketable securities | 18,704 ᵖ | 34,621 | 51,951 | Balance sheet, p. 53; FY2024 as above |
| Depreciation & amortization | 1,508 | 1,864 | 2,843 | Cash flow statement, p. 55 |
| Stock-based compensation | 3,549 | 4,737 | 6,386 | Cash flow statement, p. 55 |
| Capital spending (PP&E and intangibles) | 1,069 | 3,236 | 6,042 | Cash flow statement, p. 55 |
| Repurchases + employee-tax settlement + dividends | 12,711 | 41,470 | 49,008 | Cash flow statement, p. 55, three lines summed |
| Notes payable (carrying amount) | 9,709 | 8,463 | 8,468 | Note 11 — Debt, pp. 69–70; FY2024 = 1,250 current + 8,459 long-term ᵖ |
| Data Center revenue | 47,525 | 115,186 | 193,737 | Note 17, revenue by market platform |

Filing: Form 10-K for the fiscal year ended 25 Jan 2026, accession 0001045810-26-000021, filed 25 Feb 2026 (saved locally in [`src/10-K_FY2026/`](src/10-K_FY2026/)). The FY2026 10-K carries three years of income statement and cash flow but only two balance sheets; ᵖ marks the four FY2024 balance-sheet items that come from a data provider (SEC XBRL companyfacts, tags `InventoryNet`, `PropertyPlantAndEquipmentNet`, `AccountsReceivableNetCurrent`, `MarketableSecuritiesCurrent`, `LongTermDebtNoncurrent`, period end 2024-01-28) and were **not confirmed by hand against the FY2025 10-K**. They inform the ratio table only; the model's opening balance sheet uses FY2026 figures, every one of which is in the saved filing.

**Checked by hand (two):** revenue 215,938 on p. 51 and inventory 21,403 on p. 53 of the saved 10-K, and the balance sheet foots: total assets 206,803 = total liabilities 49,510 + equity 157,293.

**Provider trap, for the record.** The FY2026 capex tag (`PaymentsToAcquireProductiveAssets`, 6,042) matches the filing; MD&A p. 44 rounds it to "$6.1 billion". But the revenue tag many providers still map, `RevenueFromContractWithCustomerExcludingAssessedTax`, was last filed by NVIDIA for FY2022 (26,914) — a feed keyed to that tag shows a stale number or nothing. Every provider number above was checked back to the filing text before use.

## R.2 Ratio table — what the history says

| Ratio | FY2024 | FY2025 | FY2026 | How |
|---|---:|---:|---:|---|
| Reported revenue growth | — | 114.2% | 65.5% | this year ÷ last year − 1 |
| Data Center revenue growth | — | 142.4% | 68.2% | the segment that is 90% of revenue |
| Organic vs bought growth | all organic | all organic | all organic | Acquisitions net of cash were 83 / 1,007 / 1,535; the 10-K discloses no acquired-revenue contribution. NVIDIA reports no same-store figure; its analog is the customer concentration below |
| Two largest direct customers | 13% | 12% + 11% + 11% | 22% + 14% | MD&A p. 41 — the "organic" question for NVIDIA is how durable these buyers' spending is |
| Gross margin | 72.7% | 75.0% | 71.1% | gross profit ÷ revenue. FY2026 carries a 4.5bn H20 export-licence charge = 2.1 points; ex-charge 73.2% (MD&A p. 41) |
| Operating expenses ÷ revenue | 18.6% | 12.6% | 10.7% | R&D + SG&A (incl. SBC) ÷ revenue; opex +41% in FY2026 (compensation, compute and infrastructure) |
| Operating margin | 54.1% | 62.4% | 60.4% | operating income ÷ revenue |
| Effective tax rate | 12.0% | 13.3% | 15.1% | tax ÷ pretax; below 21% because of FDDEI, SBC and R&D credits (MD&A p. 42); rising each year |
| Receivable days | 59.9 | 64.5 | 65.0 | receivables ÷ revenue × 365 |
| Inventory days | 116.0 | 112.7 | 125.0 | inventory ÷ cost of revenue × 365 |
| Payable days | 59.3 | 70.6 | 57.3 | payables ÷ cost of revenue × 365 |
| Accrued & other current liabilities ÷ revenue | 11.0% | 9.0% | 9.9% | |
| D&A ÷ opening PP&E + intangibles | — | 37.1% | 40.1% | short lives (2–7 years, Note 1) on a mostly equipment base |
| Capital spending (filing) ÷ revenue | 1.8% | 2.5% | 2.8% | cash flow statement; MD&A: capex "will increase in FY2027" |
| Capital spending (data-provider tag) | 1,069 | 3,236 | 6,042 | `PaymentsToAcquireProductiveAssets` — matches the filing in all three years |
| SBC ÷ revenue | 5.8% | 3.6% | 3.0% | the recurring non-cash charge |
| Interest income ÷ opening cash + securities | — | 6.9% | 5.3% | opening-balance convention overstates the yield when the balance grows fast |
| Interest expense ÷ opening notes | — | 2.5% | 3.1% | fixed-coupon notes, 1.55%–3.70% (Note 11) |
| Distributions ÷ FCFE-style cash flow | — | 63% | 45% | 41,470 ÷ 65,797 and 49,008 ÷ 109,647 (NI + D&A + SBC − capex − WC build − repayment) |

**What the history does not say.** FY2026 growth was 65% and the first half of FY2027 (10-Qs filed 20 May and 26 Aug 2026) ran at 177,837 of revenue, 75.0% gross margin, 9.0% opex ratio and a 16.5% tax rate. Extrapolating any of these forward is the assumption, not the history.

## R.3 Assumption set — value, label, reason

### Operating

| Assumption | Value | Label | Reason (in my words) |
|---|---|---|---|
| Revenue growth FY2027 | +85.6% (to 400,837) | guidance + judgment | H1 FY2027 actual 177,837 + Q3 outlook 108,000 (Q2 release, 26 Aug 2026) + Q4 judgment 115,000 (14-week quarter; Q3 guide +6.5%). No China Data Center compute revenue, as the outlook assumes |
| Revenue growth FY2028–FY2031 | 25% → 12% → 7% → 4% | judgment | Hyperscaler capex cannot compound at 65–85% for long; the path halves growth each year toward nominal GDP. Two customers are 36% of revenue. The biggest judgment in the model; Week 6 tests it |
| Gross margin | 74.5% → 73.0% → 72.0% → 71.0% → 70.0% | judgment | H1 FY2027 75.0%, Q3 outlook 74.0%. Custom silicon and AMD compete for the same racks; FY2024 was 72.7% and FY2023 56.9%. Drift down, not collapse |
| Operating expenses ÷ revenue | 8.7% → 9.5% → 10.5% → 11.5% → 12.5% | judgment | FY2027 = H1 actual 16,029 + Q3 guide 9,200 + Q4 judgment 9,800 over 400,837. Then back toward FY2025's 12.6% as revenue slows and R&D (one-year product cadence, Rubin) keeps growing |
| D&A ÷ opening PP&E + intangibles | 40.1% | history | FY2026 ratio; appears only in the cash-flow add-back and PP&E roll because NVIDIA embeds D&A in COGS and opex |
| SBC ÷ revenue | 2.5% | judgment | FY2026 3.0%, H1 FY2027 2.2%; non-cash in earnings, added back in cash flow, credited to equity |
| Capital spending ÷ revenue | 2.8% | history | FY2026 ratio; MD&A says FY2027 capex rises in dollars, which a ratio on 86% revenue growth delivers (11.2bn). H1 FY2027 ran 2.5% |
| Tax rate | 17.0% | guidance | Q2 FY2027 release: FY2027 GAAP tax rate 16%–18%; midpoint carried five years by judgment as FDDEI and SBC benefits keep shrinking |
| Other income (equity gains) | 0 | judgment | 9,022 in FY2026, 23,707 in H1 FY2027, unrealised and unrepeatable on purpose; a gain is not a forecast |

### Balance sheet and financing

| Assumption | Value | Label | Reason |
|---|---|---|---|
| Receivable days | 65.0 | history | FY2026 |
| Inventory days | 125.0 | history | FY2026; supply commitments of 95.2bn (Note 12) say inventory stays heavy |
| Payable days | 57.3 | history | FY2026 |
| Accrued & other current ÷ revenue | 9.9% | history | FY2026 |
| Marketable securities | 51,951, held flat | judgment | surplus lands in cash, where the floor check can see it |
| Interest rate on cash + securities | 3.5% | judgment | FY2026 ÷ opening 5.3%, ÷ average ~4.4%; H1 FY2027 annualised ~3.3% as rates fell |
| Interest rate on notes | 3.06% | history | FY2026 interest expense ÷ opening notes |
| Notes repaid | 1,000 / 0 / 1,250 / 0 / 1,500 | history | Note 11 ladder: 3.20% notes due 2026 (FY2027), 1.55% due 2028 (FY2029), 2.85% due 2030 (FY2031) |
| Minimum cash | 8,000 | history | lowest year-end of the three years was 7,280 (FY2024) |
| Backstop line | 25,000 at 4.5% | history / judgment | commercial-paper program enlarged to $25.0bn in Jan 2026 (Note 11), none drawn; rate is judgment; never drawn in the base case |
| Buybacks + net share settlement + dividends | 95% of each year's FCFE | judgment | A distribution, not part of what we value. Tied to FCFE so cash does not pile up and earn interest the owners never see. FY2026 actual 49,008 on 109,647 of FCFE-style cash flow (45%); H1 FY2027 ~48,000 on ~74,000 (65%); $99bn authorisation left and the dividend raised to $0.25/quarter |

### Valuation

| Assumption | Value | Label | Reason |
|---|---|---|---|
| Cost of equity | 12.0% | judgment | Above the tutorial's round 10%: `beta.py` measures a raw beta of 2.21 (1.81 Blume-adjusted) against SPY, 60 monthly returns to Sep 2026, so a CAPM at ~4% + 1.81 × 5% is ~13%. Week 6 replaces the round number with the measured one |
| Terminal growth | 3.0% | judgment | long-run nominal growth; must stay below the cost of equity |
| Shares outstanding | 24,100 million | fact | 10-Q cover, 21 Aug 2026 (accession 0001045810-26-000075), filed to the nearest 0.1bn (±0.2% on value per share); 24,304 million at FY2026 year-end, buybacks since |

Twenty-two assumptions: nine history, two guidance, ten judgment, one mixed (the backstop line: filed size, judged rate), plus one fact. All of them sit at the top of `nvda_proforma.py`.

### Opening balance sheet (FY2026 as filed, p. 53)

| Assets | | Liabilities & equity | |
|---|---:|---|---:|
| Cash | 10,605 | Accounts payable | 9,812 |
| Marketable securities | 51,951 | Accrued and other current | 21,352 |
| Accounts receivable | 38,466 | Notes (999 current + 7,469 long-term) | 8,468 |
| Inventory | 21,403 | Other liabilities (leases 2,572 + other 7,306) | 9,878 |
| PP&E 10,383 + intangibles 3,306 | 13,689 | Shareholders' equity | 157,293 |
| Other assets (prepaids, leases, goodwill, deferred tax, non-marketable equity, other) | 70,689 | | |
| **Total** | **206,803** | **Total** | **206,803** |

## The five years

| | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E |
|---|---:|---:|---:|---:|---:|
| Revenue | 400,781 | 500,976 | 561,093 | 600,370 | 624,385 |
| Gross profit | 298,582 | 365,713 | 403,987 | 426,263 | 437,069 |
| Operating expenses | 34,868 | 47,593 | 58,915 | 69,043 | 78,048 |
| Operating income | 263,714 | 318,120 | 345,072 | 357,220 | 359,021 |
| Interest income − interest expense | 1,930 | 2,314 | 2,766 | 3,307 | 3,838 |
| Tax | 45,160 | 54,474 | 59,132 | 61,290 | 61,686 |
| **Net income** | **220,485** | **265,960** | **288,706** | **299,237** | **301,173** |
| Cash (the result) | 20,693 | 33,602 | 47,964 | 63,146 | 78,529 |
| Accounts receivable | 71,393 | 89,241 | 99,950 | 106,947 | 111,224 |
| Inventory | 35,012 | 46,339 | 53,822 | 59,647 | 64,171 |
| PP&E and intangibles | 19,414 | 25,647 | 31,062 | 35,405 | 38,679 |
| Total assets | 269,152 | 317,469 | 355,439 | 387,784 | 415,243 |
| Notes | 7,468 | 7,468 | 6,218 | 6,218 | 4,718 |
| Commercial paper drawn | 0 | 0 | 0 | 0 | 0 |
| Equity | 196,125 | 229,342 | 259,187 | 284,979 | 309,489 |
| Total liabilities & equity | 269,152 | 317,469 | 355,439 | 387,784 | 415,243 |
| Net income | 220,485 | 265,960 | 288,706 | 299,237 | 301,173 |
| + D&A + SBC | 15,509 | 20,309 | 24,311 | 27,465 | 29,807 |
| − Capital spending | -11,214 | -14,017 | -15,700 | -16,799 | -17,470 |
| − Working-capital build | -22,020 | -14,075 | -8,817 | -6,267 | -4,354 |
| − Notes repaid | -1,000 | 0 | -1,250 | 0 | -1,500 |
| **Free cash flow to equity** | **201,760** | **258,176** | **287,250** | **303,636** | **307,656** |
| − Buybacks and dividends (95% of FCFE) | -191,672 | -245,268 | -272,888 | -288,455 | -292,273 |

FCFE grows more slowly than net income after FY2028 because the working-capital build shrinks as growth slows while capex, tied to revenue, keeps rising. The commercial-paper line is never drawn.

## V.1 Check block — printed, not assumed

```
-- checks (must read 0.0 in every year)
                                          FY2027E    FY2028E    FY2029E    FY2030E    FY2031E
Assets − liabilities − equity                 0.0        0.0        0.0        0.0        0.0
Cash: balance sheet vs cash flow              0.0        0.0        0.0        0.0        0.0
PP&E roll-forward                             0.0        0.0        0.0        0.0        0.0
Debt roll-forward                             0.0        0.0        0.0        0.0        0.0
Cash at or above the 8,000 floor              0.0        0.0        0.0        0.0        0.0
balanced, 5 year(s)
```

`assert_balanced` runs first inside `value()`; the discounted cash flow cannot run on a sheet that does not balance. Cash stays above the 8,000 floor in every year, so no year draws the backstop line.

**Making it fail on purpose** (`python3 nvda_proforma.py --break`, cash typed at the opening 10,605 instead of linked):

```
Model refused: FY2027E does not balance: assets − liabilities − equity = -10,088.0
(the gap is the year's change in cash with the sign flipped: -10,088.0)
```

The gap is exactly the year's change in cash (FCFE 201,760 less the 95% paid out = 10,088) with the sign flipped: the fingerprint of an unlinked cash line. When a balance check fails by an amount that looks like a cash flow, that is where to look.

## From cash flows to a value

| | USD millions | How |
|---|---:|---|
| Present value of FY2027–FY2031 FCFE at 12% | 957,957 | discount factors 0.8929 … 0.5674 |
| Cash flow in FY2032 | 318,430 | (307,656 FCFE + 1,500 repayment that ends) × 1.03 |
| Value at end-FY2031 of everything after | 3,538,114 | ÷ (12% − 3%) |
| … discounted to today | 2,007,621 | × 0.5674 |
| **Equity value** | **2,965,578** | explicit + terminal |
| Share of value sitting after FY2031 | 67.7% | five years of very large near-term cash flows carry more weight than in a slow-growth company, where the terminal share is typically ~80% |
| Shares outstanding, millions | 24,100 | 10-Q cover, 21 Aug 2026 |
| **Value per share, base case** | **$123.05** | one assumption set, one answer |

## V.2 The model and the market

The model says **$123.05**; the market said **$227.38** at the close on 21 September 2026 (Nasdaq historical data, cached in [`src/beta_prices/`](src/beta_prices/), file `NVDA_2024-09-22_2026-09-22_nasdaq_historical_raw.json`), on the same 24.1 billion shares. No recommendation; a question: which of the twenty-two assumptions would have to be wrong, and by how much, for $227 to be right? Holding every operating line fixed, the cost of equity that reproduces the market price is 7.9%; at the tutorial's round 10% the model gives $159, at a CAPM-style 13% it gives $110. So the gap is not mainly a discount-rate argument; the market is paying for growth after FY2028 well above the 25% → 4% path, or for margins that never drift down, or both. Part 2, [`nvda-whatif.md`](nvda-whatif.md), takes those apart one at a time: no margin or cost assumption reaches the price; only growth about 24 points a year above the path, or a cost of equity near 7.9%, does.

## What has changed since the opening balance sheet (challenges, not yet replacements)

- **$24.9 billion of new notes** were issued in Q2 FY2027 (long-term debt 32,366 at 26 Jul 2026, up from 7,469). The base case keeps the FY2026 ladder; adding the notes raises interest expense by roughly $1 billion a year and cash by $25 billion, a wash for FCFE except the spread. Week 6 what-if.
- **Distributions accelerated:** ~$46 billion returned in H1 FY2027 and the quarterly dividend rose from $0.01 to $0.25. The 95% payout above assumes distributions keep rising with cash flow.
- **Equity-stake gains** of $23.7 billion in H1 FY2027 are excluded on purpose; they are also why H1 GAAP net income (118,010) overstates operating earnings.
- **Two-platform reporting** (Data Center and Edge Computing) replaced the five market platforms from Q1 FY2027; the Data Center growth ratios above use the old definitions from the 10-K.

## Known limitations of the base case

- Cash that accumulates earns 3.5% and that interest flows into later FCFE, a small double count; paying out 95% of FCFE keeps it small (interest income is 1.1% of FY2031E pretax income). What-if runs in `nvda_whatif.py` show the payout ratio moves value by about $2 either way.
- D&A is applied to PP&E plus intangibles, so acquired intangibles amortise at the equipment rate; intangibles are 3,306 of a 206,803 balance sheet.
- Gains and losses on the $22 billion non-marketable and $13 billion marketable equity portfolio are set to zero; the portfolio is carried flat inside other assets.
- The share count on the 10-Q cover is rounded to 0.1 billion; the exact balance-sheet count in the July 2026 10-Q would move value per share by up to ±0.2%.

## E. Partner review — to be completed in class

> Record your partner's attack on **one** judgment label, and your two-sentence answer, here. The two judgments most exposed are the FY2028–FY2031 growth path and the gross-margin drift; expect the attack there.

**Partner's attack (their words):** _[record in class]_

**My answer (two sentences, with reasons):** _[record in class]_

**My attack on my partner's model (be specific: name the line, the number, and what would change it):** _[record in class]_

## Sources

- NVIDIA Corporation, Form 10-K for the fiscal year ended 25 January 2026, accession 0001045810-26-000021, filed 25 February 2026. Income statement p. 51, balance sheet p. 53, equity statement p. 54, cash flow statement p. 55, MD&A pp. 39–46, Note 11 (Debt) pp. 69–70, Note 12 (Commitments) p. 70, Note 17 (Segments). https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm
- NVIDIA Form 10-Q for the quarter ended 26 April 2026 (accession 0001045810-26-000052, filed 20 May 2026) and for the quarter ended 26 July 2026 (accession 0001045810-26-000075, filed 26 Aug 2026), via the SEC XBRL companyfacts API (`https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json`), used for H1 FY2027 actuals, the FY2024 balance-sheet items marked ᵖ, and the 21 Aug 2026 share count.
- NVIDIA press releases, "NVIDIA Announces Financial Results for First Quarter Fiscal 2027" (20 May 2026) and "… Second Quarter Fiscal 2027" (26 Aug 2026), investor.nvidia.com — Q3 FY2027 outlook (revenue $108.0bn ± 2%, gross margin 74.0% ± 50 bp, GAAP opex ≈ $9.2bn, FY2027 tax rate 16%–18%), Data Center revenue, capital returns, debt issuance.
- Nasdaq historical prices for NVDA and SPY, cached in [`src/beta_prices/`](src/beta_prices/); regression in [`beta.py`](beta.py) (raw beta 2.21, standard error 0.30, Blume-adjusted 1.81, 60 monthly observations to 23 Sep 2026).
- Course tutorial, FIN 43900 Week 5, Video 1: the three-statement engine, the check rule and the known answer used to verify it.

Written for FIN 43900 (Purdue) as a learning exercise. Not investment research and not financial advice. AI assistance: model and write-up drafted with Claude Code from my filings, data and beta work; the judgments and their reasons are mine to defend.
