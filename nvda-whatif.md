# NVIDIA (NVDA) — Taking the Base Case Apart

**Part 2 of the pro-forma work.** The base case in [`nvda-proforma.md`](nvda-proforma.md) gave one answer: **$123.05** a share on free cash flow to equity at 12% / 3%, with 67.7% of the value after FY2031. The shares closed at **$227.38** on 21 Sep 2026. This file takes that answer apart: the discount rate measured, every operating assumption shocked one at a time and then together, what today's price is paying for, three pictures, and the conversation with colleagues.

Script: [`nvda_whatif.py`](nvda_whatif.py) (standard library only; imports the base-case engine and reruns it with assumptions swapped; writes the three charts to [`charts/`](charts/)). Every number below is a full rerun of the five-year statements. The balance and cash-floor checks run on every case; a case that failed them would print "not valued", never a patched number.

USD millions unless stated. Learning demonstration, not investment advice.

| Where Part 1 left us | |
|---|---|
| Value per share, base case | $123.05 |
| … of which after FY2031 | 67.7% |
| Share price, 21 Sep 2026 | $227.38 (dated marker, not a model output; 24.1bn shares on both sides) |
| Question for today | which assumptions would have to be wrong, and by how much? |

## 1. The discount rate, taken apart

**Beta.** [`beta.py`](beta.py) regresses NVIDIA's periodic returns on the market's (prices cached in [`src/beta_prices/`](src/beta_prices/), windows ending 24 Sep 2026). Beta = covariance ÷ market variance: how much NVDA moves when the market moves 1%.

| Regression | Beta | s.e. | Two s.e. span | R² | Blume | Stock / market vol per period |
|---|---:|---:|---|---:|---:|---|
| NVDA monthly, 5y vs SPY | 2.21 | 0.30 | 1.61 to 2.81 | 0.48 | 1.81 | 14.5% / 4.6% |
| NVDA weekly, 2y vs SPY | 1.86 | 0.19 | 1.48 to 2.24 | 0.49 | 1.57 | 5.6% / 2.1% |
| NVDA monthly, 5y vs QQQ | 1.88 | 0.19 | 1.49 to 2.27 | 0.62 | 1.59 | 14.5% / 6.0% |
| AMD monthly, 5y vs SPY | 2.46 | 0.48 | 1.50 to 3.42 | 0.31 | 1.97 | 20.0% / 4.6% |
| AVGO monthly, 5y vs SPY | 1.45 | 0.29 | 0.86 to 2.03 | 0.30 | 1.30 | 12.0% / 4.6% |
| MRVL monthly, 5y vs SPY | 2.24 | 0.47 | 1.30 to 3.17 | 0.28 | 1.82 | 19.1% / 4.6% |

Read it the way the tutorial reads a beta. NVIDIA's monthly volatility is 14.5% against the market's 4.6%, three times the market, and unlike a car dealer the co-movement is real: R² of 0.48 means the market explains about half of NVIDIA's monthly moves. The observed beta of 2.21 carries a standard error of 0.30, so two standard errors span 1.61 to 2.81. The weekly two-year window and the Nasdaq-100 proxy both come in lower, near 1.9. The Blume adjustment (⅔ × beta + ⅓) shrinks the monthly figure to 1.81, the number a data vendor would quote.

**Bottom-up cross-check.** Three peers that sell into the same data-centre racks, AMD, Broadcom and Marvell, regress at 2.46, 1.45 and 2.24; the average is 2.05. The tutorial unlevers and relevers; here the step is omitted on purpose: NVIDIA's notes are $8.5bn against a market value near $5.5tn, and the peers also carry little debt relative to their market values, so the leverage adjustment would move the average by less than its standard error. Three noisy estimates averaged still beat one.

**From beta to a cost of equity.** CAPM: risk-free rate + beta × equity risk premium, with the course convention of a 5.00% ten-year Treasury and the 4.42% implied premium (July 2026).

| | Cost of equity | Value per share | After FY2031 | vs base | Note |
|---|---:|---:|---:|---:|---|
| Tutorial round number | 10.00% | 159.2 | 73.6% | +36.1 | a market-average-plus stock; beta implied 1.13 |
| Beta = 1 (the market) | 9.42% | 173.8 | 75.5% | +50.8 | what an average stock earns |
| Base judgment 12% | 12.00% | 123.1 | 67.7% | +0.0 | beta implied 1.58 |
| Blume-adjusted 1.81 | 12.99% | 110.6 | 65.0% | -12.5 | the vendor convention |
| Weekly 2y beta 1.86 | 13.22% | 108.0 | 64.4% | -15.0 | 104 observations, s.e. 0.19 |
| Peer average 2.05 (AMD, AVGO, MRVL) | 14.05% | 99.7 | 62.2% | -23.4 | bottom-up; leverage adjustment omitted, all four carry little debt |
| Observed monthly beta 2.21 | 14.77% | 93.4 | 60.4% | -29.7 | s.e. 0.30; two s.e. span 1.61 to 2.81 |

The base case's 12% quietly assumed a beta of 1.58, **below every measurement of NVIDIA on this screen**. Where the dealer tutorial's round number turned out conservative, ours turned out generous: the measured range is 13% to 14.8% and worth $93 to $111 a share. The spread across defensible rates is about $80 a share; that is larger than most operating disagreements below, so when someone asks why the number moved, look here first.

**Cost of equity × terminal growth, $ per share** (the same five years of statements in every cell; base in bold):

| | g = 2.0% | g = 2.5% | g = 3.0% | g = 3.5% | g = 4.0% |
|---|---:|---:|---:|---:|---:|
| r = 10% | 143.5 | 150.8 | 159.2 | 168.8 | 180.0 |
| r = 11% | 127.1 | 132.6 | 138.8 | 145.9 | 153.9 |
| r = 12% | 114.0 | 118.3 | **123.1** | 128.4 | 134.4 |
| r = 13% | 103.3 | 106.7 | 110.4 | 114.6 | 119.2 |
| r = 14% | 94.4 | 97.1 | 100.1 | 103.4 | 107.0 |
| r = 15% | 86.8 | 89.1 | 91.5 | 94.2 | 97.1 |

Down a column, half a point of terminal growth is worth about $5 at 12%; across a row, a point of discount rate is worth $13 to $20. Both are judgments. Neither is in a filing. Show them as a grid, never as a point. Picture: [`charts/rate-growth-grid.svg`](charts/rate-growth-grid.svg).

**What the terminal value assumes, and what each alternative is worth.**

| Convention | $/share | vs base | Reading |
|---|---:|---:|---|
| Base: FY31 note repayment (1,500) added back; SBC added back; interest on cash in FCFE | 123.1 | +0.0 | the settled convention from the tutorial |
| No repayment add-back after FY31 | 122.6 | -0.4 | the FY31 maturity is trivial next to NVIDIA's cash flow |
| SBC treated as a cash cost (not added back), every year and in the terminal | 116.9 | -6.2 | the honest alternative: SBC is a real cost to owners through dilution; the add-back is offset only if buybacks retire the shares issued |
| Interest on cash and securities excluded from FCFE (after tax) | 121.8 | -1.3 | a purer operating cash flow; the cash pile is small because 95% is paid out |
| Terminal growth 0%: a flat industry after FY31 | 100.4 | -22.6 | AI infrastructure spending stops growing after FY2031 |
| Terminal growth -2%: a shrinking one | 90.7 | -32.4 | the market-implied table below points the other way |
| FY27 normalised to 52 weeks (revenue x 52/53; growth 82.1%) | 120.8 | -2.3 | FY2027 has 14 weeks in Q4 (Note 1); the base carries the extra week into every later year |

One caveat the tutorial insists on disclosing: in FY2031 the model reinvests 7,627 (capex less D&A plus working capital) out of 301,173 of net income, 2.5%, and grows the cash flow at 3% forever. That implies a 118% return on what is retained. NVIDIA's fabless model does earn extraordinary returns on capital (FY2026 net income of 120,067 on opening equity of 79,327), so the number is not absurd, but it is aggressive: growth with almost no reinvestment. Terminal growth of 0% is the alternative, and it costs $23 a share.

## 2. Operating what-ifs, one at a time

Each assumption moved by a plausible amount in the bad and the good direction, everything else at base, the model rerun each time, sorted by how much it matters.

| | Worse case $/sh | Better case $/sh | Swing $/sh |
|---|---:|---:|---:|
| Growth FY28-31 +/-5 pts a year | 107.6 | 140.4 | 32.9 |
| FY27 revenue +/-5% (the Q4 judgment) | 117.0 | 129.1 | 12.1 |
| Gross margin path +/-2 pts | 118.8 | 127.3 | 8.4 |
| Tax rate +/-2 pts | 120.1 | 126.0 | 5.9 |
| Opex ratio path +/-1 pt | 121.0 | 125.1 | 4.1 |
| Payout 75% vs 100% of FCFE (a distribution, not value) | 125.1 | 122.5 | -2.5 |
| SBC +/-0.5 pt of revenue (add-back runs backwards) | 121.8 | 124.3 | 2.5 |
| Capex +/-1 pt of revenue | 122.2 | 123.9 | 1.6 |
| Receivable days +/-10 | 122.3 | 123.8 | 1.6 |
| Inventory days +/-20 | 122.5 | 123.6 | 1.1 |
| Yield on cash +/-1 pt | 122.7 | 123.4 | 0.7 |

Picture: [`charts/tornado.svg`](charts/tornado.svg). Three things to read off it. **Growth after FY2027 is the valuation.** Five points a year on the FY2028–31 path is worth $33 a share, more than every other bar together; for the dealer in the tutorial, gross margin and capex led and growth was a distant third, because floor plan funded its working capital. Here revenue growth flows almost straight to cash: 74% gross margin, 9% opex, 2.8% capex. **Margin matters less than you would think.** Two points of gross margin either way is $8, because the base already drifts margins down 4.5 points over five years. **Two bars run backwards.** More SBC raises value because it is a non-cash add-back, and a higher payout lowers it because less cash sits earning interest; both are artefacts of the FCFE convention, not economics, and both are small.

**Growth after FY2027: what each path is worth.**

| Path for FY2028–31 | FY2031E revenue | $/share | vs base |
|---|---:|---:|---:|
| Flat after FY27 (0% x 4) | 400,781 | 85.8 | -37.2 |
| Half the base path (12.5 / 6 / 3.5 / 2) | 504,552 | 103.3 | -19.8 |
| Base (25 / 12 / 7 / 4) | 624,385 | 123.1 | +0.0 |
| Base +5 pts a year (30 / 17 / 12 / 9) | 744,185 | 140.4 | +17.4 |
| Compounding capex cycle (40 / 25 / 15 / 10) | 887,229 | 163.4 | +40.4 |

If Data Center spending simply stops growing after FY2027, the value is $86. If the capex cycle keeps compounding at 40% then 25%, it is $163, and revenue reaches $887 billion in FY2031. Each five points a year on the path is worth about $17 a share.

**Gross margin path × growth path, $ per share.**

| | growth −5 pts/yr | growth as set | growth +5 pts/yr |
|---|---:|---:|---:|
| margin -3% pts | 102.2 | 116.7 | 133.1 |
| margin +0% pts | 107.6 | 123.1 | 140.4 |
| margin +3% pts | 113.0 | 129.4 | 147.8 |

Corner to corner is $102 to $148. This grid is what you hand to the colleague who says "margins are going lower and the cycle is turning": point to a cell instead of arguing.

**Named cases: several assumptions moved together.** Single shocks are how you understand the model; named cases are how you talk about the company.

| Case | What moves | $/share | After FY2031 | Balance | Revolver peak |
|---|---|---:|---:|---|---:|
| Bear: custom silicon takes share | gross margin 74.5 → 60% by FY31; growth 10 / 0 / −5 / 0; opex ratio to 15% | 74.2 | 60.6% | OK 0.0 | 0.0 |
| Digestion: AI capex pauses in FY2028 | growth −20 / 0 / +10 / +5; gross margin 70%; opex ratio 12–13% | 76.1 | 65.0% | OK 0.0 | 0.0 |
| **Base** | | **123.1** | 67.7% | OK 0.0 | 0.0 |
| Bull: AI capex keeps compounding | growth 40 / 25 / 15 / 10; gross margin holds ~74% | 171.4 | 71.2% | OK 0.0 | 0.0 |

Every case is a full rerun and every balance sheet balances; because distributions are 95% of each year's cash flow, none of them touches the commercial-paper backstop. Note that even the bull case, $171, sits below the $227 price.

If you had added the digestion case's three single shocks instead of rerunning, you would have written $75.2; the model says $76.1. Shocks interact (lower revenue means lower receivables means lower working-capital build, and so on through every link). Never add sensitivities. Rerun the model.

**Review triggers (kill criteria).** Written down in advance, each tied to a number the next two quarterly reports will confirm or deny.

| Trigger | $/share | Change |
|---|---:|---:|
| Gross margin guided below 72% and keeps falling (path 72 / 68 / 66 / 65 / 65) | 112.8 | -10.2 |
| Data Center revenue falls quarter on quarter (FY28 growth 10%, not 25%) | 109.6 | -13.5 |
| Operating expenses grow faster than revenue (opex path +2 pts) | 118.9 | -4.1 |

If the next two quarters show any of these, the base case is withdrawn and rebuilt as a combined case, not patched one number at a time.

## 3. What today's price is paying for

Hold the other assumptions at base, move one, and search (bisection) for the value that makes the model equal $227.38.

| | Base | Implied by the price |
|---|---|---|
| Cost of equity | 12.00% | 7.93% |
| Terminal growth | 3.00% | 7.82% |
| Gross margin, every year (shift) | 74.5% -> 70.0% | not reachable: even +20.0% pts gives $165 |
| Growth FY28-31, every year (shift) | 25 / 12 / 7 / 4 | +24.2% pts |
| Opex ratio, every year (shift) | 8.7% -> 12.5% | not reachable: even +10.0% pts gives $102 |

Read it the right way. The implied cost of equity, 7.93%, is a CAPM beta of 0.66 for a stock whose measured beta is above 1.8 on every window. The implied terminal growth, 7.82%, is a company growing faster than the economy forever. No gross margin reaches the price, not even 94.5%, and neither does an opex ratio of zero. The one operating lever that gets there is growth: **about 24 points a year more than the base path for four years**, roughly 49% / 36% / 31% / 28%, which puts FY2031 revenue near $1.4 trillion. That is the disagreement in operating language. The market is not pricing a slightly better NVIDIA; it is pricing a compute build-out that compounds at 30%-plus for the rest of the decade, or a discount rate that treats NVIDIA as a utility. Both are claims the next two quarters can start to test, and the posture is to wait for that evidence.

## 4. Draw it

Three pictures carry the story, all drawn from the same function that printed the grids, one number per picture:

- [`charts/tornado.svg`](charts/tornado.svg): one assumption at a time; red the bad direction, blue the good, the line the base. The eye goes to the top bar, and it should.
- [`charts/one-axis.svg`](charts/one-axis.svg): price, bear, digestion, base, bull and the base at the tutorial's 10%, on one line. Anyone can see in a second that the price sits above the bull case.
- [`charts/rate-growth-grid.svg`](charts/rate-growth-grid.svg): the cost-of-equity × terminal-growth surface as a heat map; the two inputs trade off along the diagonal.

Open any of them in a browser. They are SVG written by the script itself; no plotting library is needed.

## 5. Informing colleagues

**The two-line message**, sent before anyone asks:

> NVDA base case $123 a share on free cash flow to equity at 12% / 3%; shares near $227. Even the bull case (growth 40 → 10%, margins held) is $171; the price needs either growth of ~24 pts a year above our path for four years or a cost of equity of 7.93%. Posture: the price is paying for a compute cycle we cannot yet see in the filings; wait for the next two quarters' Data Center growth and gross-margin guidance.

**The one page** to attach: the labelled assumption grids; the five-year statements with the check block under them; the seven-rate table; the tornado; the what-would-have-to-be-true table; the three triggers; "learning demonstration, not investment advice".

**The fifteen-minute walk-through**, in this order: posture → the answer and the price → the three judgments that carry it (growth after FY2027, gross-margin drift, cost of equity) → what breaks it → what we are watching → questions. Posture first, always.

## 6. Their questions, and the number for each

| Question | Answer |
|---|---|
| Why 12%? | A judgment above the tutorial's 10% because the measured beta is 2.21 (s.e. 0.30); Blume 1.81, peers 2.05. CAPM gives 13.0% to 14.8%, worth $93 to $111. 12% is the generous end, not the conservative one. |
| 67.7% of the value is after FY2031. Isn't that a guess? | It is true of every DCF of a going concern, and lower here than for a slow grower because five years of very large near-term cash flows carry weight. That is why r and g are a grid, not a point, and why the operating shocks are tested separately. |
| Reported growth was 65% and H1 FY2027 ran at 106%. Why decelerate to 25% and then 4%? | Because two customers are 36% of revenue and their capital budgets cannot compound at 65% indefinitely. The FY2027 number is guidance plus one quarter of judgment; everything after is the assumption the market disagrees with, and the tornado shows it is the whole valuation. |
| Why is stock-based compensation added back? | It is the recurring non-cash charge, $10bn in FY2027E, credited to equity and paid for through buybacks. Treat it as a cash cost instead and the value is $117, $6 lower. Shown, not hidden. |
| Why free cash flow to equity, not to the firm? | NVIDIA has $8.5bn of notes against a $5.5tn market value and $62bn of cash and securities; the enterprise bridge is a rounding error, and FCFE with a levered beta prices the equity directly. |
| What is the market saying? | Hold everything else and $227 implies a cost of equity near 7.9% (beta 0.66), or growth about 24 points a year above our path, or terminal growth near 7.8%. No margin or cost assumption gets there. Each is a hypothesis to test, none is our base. |
| What would make you drop the case? | Data Center revenue down quarter on quarter → $110; gross margin guided below 72% and falling → $113; opex growing faster than revenue → $119. Any one triggers a rebuild as a combined case. |
| Why not use the data vendor's numbers? | The FY2024 balance-sheet items came from the SEC XBRL feed and are marked unconfirmed; the revenue tag many feeds still map stopped in FY2022. Every load-bearing number is checked against the 10-K text. |

## 7. The presentation, and defending it

**Six slides, in this order.**

1. **Posture**: the price is paying for a build-out the filings do not yet show; wait for two quarters of evidence. Not a recommendation.
2. **The answer and the price**: $123 base, $74 to $171 bear to bull, shares near $227.
3. **The three judgments**: growth 25 → 4% after FY2027, gross margin 74.5 → 70%, cost of equity 12% against a measured 13–14.8%, each with its evidence.
4. **What moves it**: the tornado and the r × g grid.
5. **What the price is paying for**: the implied table.
6. **What we are watching**: the three triggers and the next two quarterly disclosures.

**The two challenges you will always get.**

*"Your model says NVIDIA is worth half its price. Isn't the model wrong?"* The model is a set of labelled assumptions, and here is the one it would take: growth of roughly 49 / 36 / 31 / 28% for four years, FY2031 revenue near $1.4 trillion. If you believe that, say so and we will run it; the bull case at 40 / 25 / 15 / 10 gets to $171. If you do not, the price is paying for something other than cash flow to equity at a measured discount rate.

*"Your terminal value is the whole answer."* 67.7%, and the reinvestment caveat above says our terminal is generous, not stingy. Here is the r × g grid, and here is the operating case that has to hold for it: 70% gross margin, 12.5% opex, $17bn of capex and $359bn of operating income in FY2031, for a company that earned $130bn in FY2026. If those are reasonable, so is the terminal value. If not, name the line and we rerun it together.

## Before your next change: lock a prediction

Week 6 asks for a written prediction before every change. Use this table for the changes you make in class; fill the middle column before you run the script, then paste the result.

| Change | My prediction, before running | Result |
|---|---|---|
| | | |
| | | |

## Sources

- Base-case model and sources: [`nvda-proforma.md`](nvda-proforma.md); FY2026 10-K (accession 0001045810-26-000021), FY2027 10-Qs, Q1 and Q2 FY2027 press releases.
- Betas: [`beta.py`](beta.py) on Nasdaq historical closes cached in `src/beta_prices/` (NVDA, AMD, AVGO, MRVL, SPY, QQQ; windows to 24 Sep 2026).
- Market inputs for CAPM: 5.00% ten-year Treasury and 4.42% implied equity risk premium (July 2026), the course convention from the Week 5 tutorial.
- Share price $227.38 on 21 Sep 2026: Nasdaq historical data in `src/beta_prices/NVDA_2024-09-22_2026-09-22_nasdaq_historical_raw.json`.
- Method: FIN 43900 Week 5 tutorial, Video 2 (take the base case apart, and present it).

Written for FIN 43900 (Purdue) as a learning exercise. Not investment research and not financial advice. AI assistance: script and write-up drafted with Claude Code from my model, data and beta work; the judgments and their reasons are mine to defend.
