# Lab 12 Checkout — Presenter Notes: My Company (NVIDIA, NVDA)

**My role:** presenter of my own NVIDIA analysis. My review of my partner's company (Apple) is in [`Check out - Partner's company.md`](Check%20out%20-%20Partner's%20company.md).

Items marked _[fill in]_ are recorded live in class; they are left blank rather than guessed.
**Conclusion presented:** base case **$123.05 per share** (FCFE, 12% cost of equity, 3% terminal growth, 24.1bn shares, USD) against a market price of **$225.51** (close, 23 Sep 2026). Posture: watch / defer — the price is paying for AI growth that keeps compounding, which the filings do not yet show.

**Why I chose NVIDIA:** Over the summer I interned in commodity operations and saw how volatile copper prices were. Commodity houses do not file 10-Ks, so I looked for a public company tied to the same demand. Copper is a key input for AI data centers, which are being built now, and NVIDIA is a large company at the centre of that build-out, developing and funding it. NVIDIA let me follow the AI data-center theme through audited filings. My initial view was watch / defer: strong operating results, but no evidence yet that the price offered an adequate return.

## Route and evidence shown

| Stop | File |
|---|---|
| Target selection | Rationale above; initial watch-defer call in [`NVDA_2026-09-03_report.md`](NVDA_2026-09-03_report.md) |
| Company and evidence | [`nvda-proforma.md`](nvda-proforma.md) R.1 history grid (FY2024–FY2026 10-Ks, USD millions) |
| Pro-forma | [`nvda-proforma.md`](nvda-proforma.md), [`nvda_proforma.py`](nvda_proforma.py) — assumption set, check block, `--break` |
| Valuation | [`nvda-proforma.md`](nvda-proforma.md) V.2–V.3; DCF and peer P/E in [`nvda-dcf-inputs.md`](nvda-dcf-inputs.md) ($64.31 placeholder FCFF DCF; $341–$390 peer-implied, 25 Feb 2026); reverse DCF in [`archive/nvda-whatif.md`](archive/nvda-whatif.md) §3 |
| Sensitivity | [`nvda-sensitivity.md`](nvda-sensitivity.md), [`nvda_sensitivity.py`](nvda_sensitivity.py) — growth span $32.89 vs gross margin $12.65 |
| Interpretation | kill triggers in [`archive/nvda-whatif.md`](archive/nvda-whatif.md) §2 |

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
