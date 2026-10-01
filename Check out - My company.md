# Lab 12 Checkout — Presenter Notes: My Company (NVIDIA, NVDA)

**My role:** presenter of my own NVIDIA analysis. My review of my partner's company (Apple) is in [`Check out - Partner's company.md`](Check%20out%20-%20Partner's%20company.md).

Items marked _[fill in]_ are recorded live in class; they are left blank rather than guessed.
**Conclusion presented:** base case **$123.05 per share** (FCFE, 12% cost of equity, 3% terminal growth, 24.1bn shares, USD) against a market price of **$225.51** (close, 23 Sep 2026). Posture: watch / defer — the price is paying for AI growth that keeps compounding, which the filings do not yet show.

**Why I chose NVIDIA:** Over the summer I interned in commodity operations and saw how volatile copper prices were. Commodity houses do not file 10-Ks, so I looked for a public company tied to the same demand. Copper is a key input for AI data centers, which are being built now, and NVIDIA is a large company at the centre of that build-out, developing and funding it. NVIDIA let me follow the AI data-center theme through audited filings. My initial view was watch / defer: strong operating results, but no evidence yet that the price offered an adequate return.

## How NVIDIA makes money

NVIDIA designs accelerated-computing chips and systems (GPUs, networking and full data-center racks) together with the CUDA software that developers build on. It is fabless: it designs the chips and outsources manufacturing to foundries such as TSMC and Samsung (FY2026 10-K, Item 1, "Manufacturing", p. 8), so it needs little capital of its own (capex was 2.8% of revenue in FY2026).

| FY2026 (year ended 25 Jan 2026), USD millions | Value | Source |
|---|---:|---|
| Revenue | 215,938 | FY2026 10-K, income statement p. 51 |
| Data Center revenue | 193,737 (~90%) | Note 17, revenue by market platform |
| Other platforms (Gaming, Professional Visualization, Automotive, OEM & Other) | 22,201 (~10%) | revenue less Data Center |
| Gross margin | 71.1% (73.2% excluding the $4.5bn H20 export charge) | income statement; MD&A p. 41 |
| Operating margin | 60.4% | income statement |
| Two largest direct customers | 22% + 14% of revenue | MD&A p. 41 |

- **Data Center is the business.** Cloud providers and AI companies buy NVIDIA systems to train and run AI models, so revenue follows their capex budgets.
- **Pricing power comes from CUDA.** The 10-K describes CUDA as the foundational development platform that runs on all NVIDIA GPUs, and says the large and growing number of developers strengthens its ecosystem and the value of its platform (Item 1, p. 4; full-stack software platform, p. 6). That CUDA lock-in is why gross margin stays above 70% is my judgment, not a filing claim.
- **The risk is concentration.** Two customers are 36% of revenue, and supply commitments of $95.2bn (Note 12) say NVIDIA is betting that demand continues.
- **Reporting change:** from Q1 FY2027, NVIDIA reports two platforms (Data Center and Edge Computing) instead of five; my history uses the 10-K's five-platform figures.

## Route and evidence shown

| Stop | File |
|---|---|
| Target selection | Rationale above; initial watch-defer call in [`NVDA_2026-09-03_report.md`](NVDA_2026-09-03_report.md) |
| Company and evidence | [`nvda-proforma.md`](nvda-proforma.md) R.1 history grid (FY2024–FY2026 10-Ks, USD millions) |
| Pro-forma | [`nvda-proforma.md`](nvda-proforma.md), [`nvda_proforma.py`](nvda_proforma.py) — assumption set, check block, `--break` |
| Valuation | [`nvda-proforma.md`](nvda-proforma.md) V.2–V.3; DCF and peer P/E in [`nvda-dcf-inputs.md`](nvda-dcf-inputs.md) ($64.31 placeholder FCFF DCF; $341–$390 peer-implied, 25 Feb 2026); reverse DCF in [`archive/nvda-whatif.md`](archive/nvda-whatif.md) §3 |
| Sensitivity | [`nvda-sensitivity.md`](nvda-sensitivity.md), [`nvda_sensitivity.py`](nvda_sensitivity.py) — growth span $32.89 vs gross margin $12.65 |
| Interpretation | kill triggers in [`archive/nvda-whatif.md`](archive/nvda-whatif.md) §2 |

**My three valuation files (all NVIDIA; not averaged):**

| File | What it is | Result |
|---|---|---|
| [`dcf.py`](dcf.py) / [`nvda-dcf-inputs.md`](nvda-dcf-inputs.md) | Early first-pass FCFF DCF: FY2026 FCFF, placeholder growth 8/6/5/4/3%, 10% WACC, 3% terminal; cash and debt bridge | $64.31 per diluted share (USD, 24,514m shares) vs $195.56 on 25 Feb 2026 |
| [`peer_valuation.py`](peer_valuation.py) | Trailing GAAP P/E of AMD and AVGO applied to NVIDIA's $4.90 EPS | $341–$390 per share, 25 Feb 2026 |
| [`nvda_proforma.py`](nvda_proforma.py) | Final model: three-statement pro-forma, FCFE at 12% / 3% | **$123.05** per share (USD, 24.1bn shares) vs $225.51 on 23 Sep 2026 |
| [`archive/nvda_whatif.py`](archive/nvda_whatif.py) | Reverse DCF on the pro-forma: holds other inputs at base and solves for the $227.38 price (21 Sep 2026) | Implied cost of equity 7.93%, or terminal growth 7.82%, or ~24pp more growth a year |

Why they differ: the early DCF starts from FY2026 and uses placeholder growth, so it misses the FY2027 revenue jump; the pro-forma builds that jump in from guidance. Peer P/E uses AMD and AVGO's elevated trailing multiples, so it tells me what the market pays for AI-chip earnings, not what the cash flows support. The pro-forma is my supported value; the others are cross-checks.

## Questions received and my answers

| Area | Question from my partner | My answer / unresolved gap |
|---|---|---|
| Selection and evidence | _[fill in]_ | _[fill in]_ |
| Model and valuation | _[fill in]_ | _[fill in]_ |
| Sensitivity and interpretation | _[fill in]_ | _[fill in]_ |

## Partner's explain-back and feedback

- Explain-back (conclusion / driver / limitation): _[fill in]_ — my correction, if any: _[fill in]_
- Strength: _[fill in]_
- Improvement: _[fill in]_

## Keep / revise / investigate

- **Keep:** the base case and its labelled assumptions; the sensitivity ranking (growth over margin, qualified by the ±5pp / ±3pp ranges), because it is traced through the statements and the checks pass.
- **Revise:** state the methods separately rather than averaging — the pro-forma FCFE ($123.05), the placeholder FCFF DCF ($64.31) and peer P/E ($341–$390) use different cash-flow bases and dates; the peer multiples are elevated trailing P/Es, which is why they disagree.
- **Investigate:** a sustained AI-downturn scenario (revenue falling, gross margin toward FY2023's 56.9%), which none of my cases models; the measured cost of equity (13–14.8%) versus my 12%; adding the $24.9bn of Q2 FY2027 notes. Not yet run.
- **Effect on conclusion:** watch / defer unchanged; the review raises the AI-downturn case to the top research priority.

**How my view changed since selecting NVIDIA:** I started from the demand story I saw in copper: AI data centers are being built, and NVIDIA is at the centre of them. My first report already flagged one copper-related claim for follow-up (consumer RTX cards moving to lower voltages, reducing copper demand), unverified by the 10-K. After building the model, my question has shifted from whether the demand exists to whether it lasts. A data-center slowdown would hit copper demand and NVIDIA's revenue together, and that is the scenario my analysis has not yet tested.

## Reflect

- **Question that made me reconsider:** Apple limits its AI exposure so that it stays stable if AI collapses. That made me ask the opposite about NVIDIA: my base case is $123.05 per share (FCFE, 12% / 3%, 24.1bn shares) against a market price of $225.51 (23 Sep 2026), and the gap is driven almost entirely by AI. Given the massive hyperscaler capex and the risk of an AI bubble, is that growth sustainable, and is my analysis too optimistic because it never considers AI stalling or collapsing?
- **What I now understand better about NVIDIA:** I am below the market, but my base case still assumes AI keeps growing. Revenue never falls, gross margin only drifts to 70% (it was 56.9% in FY2023), two customers are 36% of revenue, and my bear and digestion cases both recover. A collapse is not a ±5pp sensitivity shock; it is a separate scenario. Apple and NVIDIA sit on opposite sides of the same AI trade: Apple gives up growth for stability, while NVIDIA's value depends on how long AI data-center spending lasts.
- **Effect on my conclusion:** Watch / defer is unchanged, but the review moves a sustained AI-downturn scenario to the top of my research priorities (not yet run).
