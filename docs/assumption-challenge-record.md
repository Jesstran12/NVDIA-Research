# Assumption-challenge record — NVIDIA (NVDA) pro-forma

Every load-bearing driver: **value · basis · defended bounds · challenge · evidence that would change it**, plus its
one-way impact on value per share at the bounds (everything else at base; base $123.93). The same record drives the
app's slider bounds (`engine.DRIVERS`), so what a teammate can move is exactly what is recorded here. Spans are "over
these ranges": a wider bound gives a wider span, so the ranking below the top driver depends on the bounds chosen.

| # | Driver | Base value | Basis | Defended bounds (why) | $/share at low → high bound | Challenge | Evidence that would change it |
|---|---|---|---|---|---|---|---|
| 1 | Revenue growth FY2028E–FY2031E (shift to the path 25 / 12 / 7 / 4 %) | 0 pp | judgment | −25 to +25 pp. −25 pp makes FY2028E flat and later years shrink (the "AI capex stops" case); +25 pp is one point above what the market price implies, and nothing in the filings supports more | $62.73 → $232.54 (span $169.81) | Two customers are 36% of revenue (FY2026 10-K MD&A p. 41); hyperscaler capex cannot compound at 65–85% for long. Partner fresh-eyes challenge (Lab 10, [fill in name]): "why decelerate when H1 FY2027 ran at +106%?" — answer: FY2027E already carries the guided jump; the path is the assumption the market disagrees with | Data Center revenue growth in the Q3 and Q4 FY2027 reports; hyperscaler capex guidance for calendar 2027 |
| 2 | FY2027E revenue (Q4 judgment) | 400,837 (H1 actual 177,837 + Q3 outlook 108,000 + Q4 judgment 115,000) | guidance + judgment | ±10% of the year. Q3 is guided ±2%; only Q4 (14 weeks) is judgment | $111.93 → $135.93 (span $24.01) | No Q4 guidance yet; China Data Center compute revenue is excluded from the outlook | Q3 FY2027 results and the Q4 outlook (November 2026) |
| 3 | Gross margin (shift to 74.5 → 70.0 %) | 0 pp | judgment | −13 to +4 pp. −13 pp takes FY2031E to 57%, FY2023's 56.9% trough; +4 pp caps FY2027E at 78.5%, above any quarter reported | $96.69 → $132.31 (span $35.62) | Custom silicon (Broadcom-built accelerators) and AMD compete for the same racks; CUDA lock-in is my judgment, not a filing claim. Partner challenge (Lab 11, [fill in name]): "the margin shock understates CUDA — if the moat erodes, volume goes too" — accepted: that is why the low case moves growth and margin together | Gross-margin guidance below 72% and falling; Data Center pricing commentary |
| 4 | Operating expenses / revenue (shift to 8.7 → 12.5 %) | 0 pp | judgment | −2 to +6 pp. −2 pp sits below the H1 FY2027 run-rate of 9.0%; +6 pp returns FY2031E to FY2024's 18.6% | $128.02 → $111.67 (span $16.35) | Opex grew 41% in FY2026; a one-year product cadence keeps R&D rising | Opex growing faster than revenue for two consecutive quarters |
| 5 | Tax rate | 17.0% | guidance (FY2027 GAAP 16–18%, Q2 FY2027 release) | 12–21%. FY2024 was 12.0%; 21% is the statutory rate with no FDDEI, SBC or R&D benefit | $131.16 → $118.14 (span $13.02) | The rate rose each of the last three years as benefits shrank | Effective rate in the FY2027 10-K; tax-law changes |
| 6 | Capital spending / revenue | 2.8% (FY2026) | history | 1.5–6%. FY2024 1.8% is the low; 6% doubles the FY2026 ratio | $124.97 → $121.35 (span $3.63) | MD&A says capex rises in FY2027; the ratio on 86% revenue growth already delivers 11.2bn | Purchases of property and equipment; any move to own fabs |
| 7 | Stock-based compensation / revenue | 2.5% | judgment (FY2026 3.0%, H1 FY2027 2.2%) | 1.5–6%. H1 FY2027 2.2% is the low; FY2024 5.8% the high of the three filed years | $121.47 → $132.55 (span $11.08; runs "backwards" because SBC is added back) | SBC is non-cash in FCFF; treat it as a cash cost (app toggle) and the base falls about $6 | SBC line in the cash flow statement; share count after buybacks |
| 8 | Cost of equity | 12.0% | judgment, between the tutorial 10% and the measured CAPM 13.0–14.8% | 9–16%. 9% is a beta near 0.9; 16% is the observed beta 2.21 plus one standard error at rf 5% + ERP 4.42% | $186.35 → $85.59 (span $100.77) | `beta.py`: 2.21 raw (s.e. 0.30), 1.81 Blume, peers 2.05; 12% is the generous end, not the conservative one | Re-estimated beta each quarter; the ten-year Treasury yield |
| 9 | Terminal growth | 3.0% | judgment (long-run nominal growth) | 0–4%. 0% is a flat industry after the build-out; 4% is about nominal GDP | $101.53 → $135.14 (span $33.61) | In FY2031E the model reinvests 2.5% of net income and grows 3% forever: a 118% return on retained cash | Must stay below the discount rate; the check refuses otherwise |

**Ranking over these ranges:** growth path > cost of equity > gross margin > terminal growth > FY2027E revenue > opex >
tax > SBC > capex. At half the bounds the order is identical; at the Lab 11 ranges (±5 pp growth, ±3 pp gross margin)
growth still leads margin, $32.77 to $12.57. The top driver does not depend on the range choice; the order of the
middle drivers does.

## Locked assumptions (not adjustable in the app; change them in `nvda_proforma.py` with a new source)

| Assumption | Value | Basis | Why locked |
|---|---|---|---|
| Opening balance sheet | FY2026 10-K p. 53 | fact | base-year reconciliation check depends on it |
| Receivable / inventory / payable days | 65.0 / 125.0 / 57.3 | history (FY2026) | one-way impact under $2 per share (archive/nvda-whatif.md); supply commitments of $279bn (Q2 FY2027 10-Q Note 10) keep inventory heavy |
| Accrued and other current ÷ revenue | 9.9% | history | small |
| D&A ÷ opening PP&E and intangibles | 40.1% | history | short asset lives; appears only in the add-back and PP&E roll |
| Marketable securities | 51,951 held flat | judgment | surplus lands in cash where the floor check can see it |
| Interest on cash / notes / commercial paper | 3.5% / 3.06% / 4.5% | judgment / history / judgment | under $1 per share |
| Note repayments | 1,000 / 0 / 1,250 / 0 / 1,500 | Note 11 ladder | filed maturities |
| Minimum cash / backstop | 8,000 / 25,000 CP program | history | the cash-floor check |
| Payout | 95% of FCFE | judgment | a distribution, not value; keeps cash from piling up |
| Shares | 24,100m outstanding + 95m dilution | fact | 10-Q cover and Note 4 |
| Bridge | FY2026 10-K balance sheet (cash 10,605; marketable debt 39,065; marketable equity 12,886; debt 8,468) | fact | dated at the start of the projected cash flows; the Q2 FY2027 sheet is a flagged reference |

## Partner fresh-eyes challenges (credited to the challenger)

Record here, with the partner's name, the challenge from the Lab 10–12 reviews and the disposition:

| Lab | Challenger | Challenge (their words) | Disposition and effect |
|---|---|---|---|
| 10 | [fill in] | [record] | [accept / modify / reject, with the number] |
| 11 | [fill in] | [record] | [accept / modify / reject, with the number] |
| 12 | [fill in — partner reviewing from the Apple side] | "Apple limits its AI exposure so it stays stable if AI collapses; is the NVIDIA base case too optimistic because it never considers AI stalling?" (from `Check out - My company.md`) | Accepted: the low case now moves growth, margin, opex and the discount rate together ($80); the growth lower bound (−25 pp) is the "AI capex stops" case |
