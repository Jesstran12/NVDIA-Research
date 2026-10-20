# Decision memo — NVIDIA Corporation (NASDAQ: NVDA)

**To:** the investment committee (no current position) · **From:** [student name], AI task-force analyst, sector group ·
**Valuation date:** 23 Sep 2026 (close $225.51) · **Information cutoff:** Q2 FY2027 10-Q, filed 26 Aug 2026 ·
**Currency / share basis:** USD; 24,195m diluted shares (24,100m outstanding at 21 Aug 2026 + 95m dilutive awards) ·
**Repository:** github.com/Jesstran12/NVDIA-Research (commit [fill in at freeze]) · *Learning exercise for FIN 43900; not investment advice.*

## 1. Decision and committee ask

**Do not initiate at $225.51; keep NVIDIA on watch.** The FCFF DCF driven by my five-year pro-forma gives
**$124 per share in the base case and $80–$187 across the causal low and high cases**; the price sits above the high case.
The market is paying for about **24 points a year more revenue growth in FY2028–FY2031** than the filings and guidance
support (a path near 49 / 36 / 31 / 28% instead of 25 / 12 / 7 / 4%), or for a cost of equity near 8% on a stock whose
measured beta is above 1.8. Neither is in the evidence yet; both are testable within two quarterly reports.

**Ask:** approve the watch posture with no position; authorise a re-review within one week of the Q3 FY2027 report
(November 2026), with this tool re-run on the new filing. **Initiate** if the price falls below the base case with the
checks still passing, or if two quarters of Data Center growth and margin evidence lift the high case above the price.

## 2. Evidence and as-of date

| Evidence | Value | Source |
|---|---|---|
| FY2026 revenue / operating income / net income | 215,938 / 130,387 / 120,067 | 10-K FY2026, income statement p. 51 (accession 0001045810-26-000021) |
| H1 FY2027 revenue (+96% y/y) / operating income | 177,837 / 117,270 | 10-Q Q2 FY2027, p. 3 (accession 0001045810-26-000075) |
| Q3 FY2027 outlook | revenue $108.0bn ±2%; gross margin 74.0%; opex ≈ $9.2bn; FY tax 16–18% | Q2 FY2027 release, 26 Aug 2026 |
| Customer concentration | two direct customers = 36% of FY2026 revenue | 10-K MD&A p. 41 |
| Opening balance sheet (bridge) | cash 10,605; marketable debt 39,065; marketable equity 12,886; debt 8,468 | 10-K p. 53; 10-Q comparative column |
| Supply and purchase commitments | $279bn, $92bn due in the rest of FY2027 | 10-Q Note 10 |
| Measured beta | 2.21 raw (s.e. 0.30), 1.81 Blume; CAPM 13.0–14.8% | `beta.py`, 60 monthly returns to Sep 2026 |

Facts are from the filings; FY2027E is guidance plus one quarter of judgment; everything after FY2027 is my
assumption, labelled as such in the model. Every input, locator and check is in `docs/evidence-ledger.csv`.

## 3. Valuation (USD millions; FCFF, five explicit years, Gordon terminal; checks all pass)

| | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E |
|---|---:|---:|---:|---:|---:|
| Revenue (growth 85.6 / 25 / 12 / 7 / 4%) | 400,781 | 500,976 | 561,093 | 600,370 | 624,385 |
| Operating income (gross margin 74.5 → 70%; opex 8.7 → 12.5%) | 263,714 | 318,120 | 345,072 | 357,220 | 359,021 |
| FCFF = EBIT(1 − 17%) + D&A + SBC − capex − ΔWC | 201,158 | 256,256 | 286,205 | 300,892 | 305,970 |

PV of explicit FCFF 952,816 + PV of terminal value 1,991,557 (3% growth; 67.6% of EV) = **enterprise value 2,944,373**;
+ cash and marketable securities 62,556 − debt 8,468 = **equity 2,998,461**; ÷ 24,195m = **$123.93**. WACC 11.99%
(cost of equity 12%, debt weight 0.16%). The Lab 10 FCFE cross-check gives $123.05. Balance sheet balances, cash
ties, base year reconciles to the 10-K, bridge reconciles, value falls monotonically as WACC rises.

**Cases (full reruns, never sums of shocks):** low $80 (growth path 15 / 2 / −3 / −6, gross margin −3 pp, opex +1 pp,
13% cost of equity: capex digestion plus custom-silicon share loss) · base $124 · high $187 (growth 35 / 22 / 17 / 14,
gross margin +1.5 pp, 11%: the cycle compounds and CUDA holds price).

**Cross-checks that disagree, not averaged:** NVIDIA trades at 28.5x trailing GAAP earnings and 27.4x trailing EBIT;
Broadcom's 45.3x / 40.4x applied to NVIDIA imply $358 / $332; AMD's 158x / 153x are reported but not meaningful under the
pre-declared rule (its 16% operating margin is a recovery being capitalised). Multiples capitalise last year's
earnings at the growth the market expects; the DCF capitalises the growth the filings support. The gap is the
disagreement, and the reverse DCF puts it in operating language: +24 pp growth a year, or 8% cost of equity, or 7.8%
terminal growth; no margin or cost assumption inside the defended bounds reaches $225.

## 4. Material assumptions and sensitivities

One driver at a time at its defended bounds (base $123.93): growth path FY2028–31 −25/+25 pp → $63 / $233 (span
$170); cost of equity 16% / 9% → $86 / $186 ($101); gross margin −13/+4 pp → $97 / $132 ($36); terminal growth 0 / 4%
→ $102 / $135 ($34); FY2027E revenue ±10% → $112 / $136 ($24); opex, tax, SBC, capex under $17 each. The ranking's
top driver is the same at half the bounds and at the Lab 11 ranges; the middle order depends on the bounds. **Locked
Changed-Input Record (Lab 11, committed 29 Sep 2026 before the run):** predicted growth would move value about three
times as much as margin; result $32.77 vs $12.57 (2.6×), direction and order right, size of the growth effect smaller
than predicted (−12.6% vs −15 to −20%). Full record in `docs/validation-and-ai-use.md`.

## 5. Principal risks, failure conditions and monitoring triggers

| Trigger (metric · threshold · window) | Effect on the case |
|---|---|
| Data Center revenue falls quarter on quarter · any decline · next two reports (Nov 2026, Feb 2027) | withdraw the base; rebuild as the low case (about $80) |
| Gross-margin guidance below 72% and falling · next two reports | gross-margin path −3 pp (about −$12) |
| Operating expenses grow faster than revenue · two consecutive quarters | opex path +2 pp (about −$5) |
| Bridge fails to reconcile after the next 10-Q (debt, buybacks, securities) · each filing | reject the per-share conclusion until it reconciles |
| Price falls below $124 with checks passing · any day | re-open the initiation question |

Known limitations: values struck at the opening balance-sheet date and compared with a price eight months later
(rolling forward adds about 8% before distributions); FY2027 is a 53-week year; SBC is added back (cash-cost
alternative −$6); the terminal year reinvests only 2.5% of net income while growing 3%.

## 6. Action requested and next review point

Approve **watch / defer — no position at $225.51**. Monitoring owner: the analyst, re-running this tool on each
filing; the sector analysts own the demand view. Next review: within one week of the Q3 FY2027 report. AI assistance
and every material check are recorded once, in `docs/validation-and-ai-use.md`.
