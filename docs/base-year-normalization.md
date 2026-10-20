# Base-year normalization — the Week 2 contamination catalog applied to NVIDIA's FY2026

The pro-forma's base year is FY2026 (ended 25 Jan 2026, 10-K accession 0001045810-26-000021). Every row below is an
honest, audited number that still cannot enter the forecast unlabeled. Each is classified as the catalog asks
(one-time item, basis change, or mechanical), with the test applied, the direction it pushes the base year, how the
model treats it, and the filing note. Facts are from the filings; "treatment" is my decision.

## One-time items — will this item, at roughly this size, be in next year's number?

| Item | FY2026 amount | Where it sits | Direction | Test | Treatment in the model | Source |
|---|---|---|---|---|---|---|
| H20 export-licence charge (inventory and purchase-commitment write-down after the April 2025 licence requirement) | 4,500 in cost of revenue; gross margin 71.1% reported vs 73.2% excluding it (2.1 pp) | FY2026 cost of revenue | punishes the base year | No: a licensing-rule charge, not a recurring cost | **Normalized by construction.** The forecast gross-margin path starts from H1 FY2027 actual 75.0% and the Q3 guide 74.0%, not from the reported 71.1%. Historical ratios that use FY2026 cost of revenue (inventory days 125.0, payable days 57.3) are computed on the reported figure; ex-charge inventory days would be 134.7 (21,403 ÷ 57,975 × 365), a difference worth under $2 per share in the Lab 12 one-way study. Left on the reported basis and labelled | 10-K MD&A p. 41 |
| Gains on equity securities (unrealised marks on publicly held stakes) | 9,022 in other income, net; 23,707 more in H1 FY2027 | below operating income | flatters net income (and the 15.1% effective rate was computed on it) | No: a mark, not a cash flow; FY2027 H1 shows how volatile it is | **Excluded.** `other_income = 0` in `nvda_proforma.py`; the FCFF starts from operating income, so the gains never enter value. The stakes themselves enter the bridge at fair value (marketable 12,886) or are excluded (non-marketable 22,251) | 10-K Note 7–8; Q2 FY2027 10-Q p. 15 |
| Acquisition-related items (purchased intangibles 3,306; acquisitions net of cash 1,535) | small | balance sheet; cash flow | neutral to EBIT | Recurring but immaterial | Carried inside "other assets" and PP&E + intangibles; amortised at the equipment rate (noted limitation) | 10-K cash flow p. 55; Q2 FY2027 10-Q Note 4 |

## Basis changes — is this year measured on the same basis as the years I compare it to or forecast from?

| Item | What changed | Effect | Treatment in the model | Source |
|---|---|---|---|---|
| 53-week fiscal year FY2027 (14-week Q4) | FY2027 has one more week than FY2026 and FY2028–FY2031 | FY2027E revenue (400,837) includes about 1/53 of an extra week; the base carries it into later years through the growth path | **Labelled, not removed:** normalising FY2027E to 52 weeks (growth 82.1% instead of 85.6%) is worth about −$2 per share (archive/nvda-whatif.md); the FY2027E revenue slider (±10%) covers it | Q2 FY2027 10-Q Note 1 |
| Segment reporting changed from five market platforms to two (Data Center, Edge Computing) from Q1 FY2027 | the Data Center growth history (142% / 68%) is on the old definition | the "Data Center ≈ 90% of revenue" framing uses FY2026's five-platform note | **Used only as history;** the model forecasts total revenue, so the forecast is basis-independent | 10-K Note 17; Q1 FY2027 10-Q |
| Operating leases (ASC 842) | lease liabilities 2,572 long-term at FY2026; 4,985 at Q2 FY2027 after new data-center leases | debt-like if treated so | **Not treated as debt** in the bridge; lease cost stays inside operating expenses, so FCFF and the bridge are consistent (one lease policy, labelled) | 10-K balance sheet p. 53; Q2 FY2027 10-Q |
| Effective tax rate 12.0% → 13.3% → 15.1% (FY2024–FY2026) as FDDEI and SBC benefits shrink | not an accounting change, but the base-year rate is not a steady state | a rate carried from FY2026 would understate tax | **Guidance basis:** 17% (FY2027 GAAP 16–18%) for all years, bounded 12–21% | Q2 FY2027 release; 10-K MD&A p. 42 |
| Debt: $25.0bn of notes issued June 2026 | the opening balance sheet carries 8,468 of notes; the July 2026 sheet carries 33,366 | would change the bridge if mixed with the opening-date cash flows | **Kept on the opening basis;** the July sheet is a flagged reference in the app (the check panel fails red if it is used with full FY2027E cash flows) | Q2 FY2027 10-Q Note 9 |

## Mechanical contamination — wrong numbers that look right

| Risk | Where it could enter | Check performed | Result |
|---|---|---|---|
| Units and scale | XBRL values are in dollars; the model is in USD millions | every ledger row converted and compared with the filing text | agree |
| Period | FY2026 (ends January) vs calendar 2025; peers' fiscal years differ (AMD December, Broadcom November) | trailing-twelve-month construction documented per company in `engine.PEERS` | consistent TTM to each company's latest 10-Q |
| Basic vs diluted shares | cover count 24,100m is basic outstanding; the EPS note's diluted weighted average is 24,285m | diluted point-in-time count = 24,100 + (24,285 − 24,190) = 24,195 | used for value per share; the cover count alone would overstate value by 0.4% |
| Provider label vs filing definition | `RevenueFromContractWithCustomerExcludingAssessedTax` is stale for NVIDIA (last FY2022); `MarketableSecuritiesCurrent` stops in FY2026 | revenue read from the `Revenues` tag and the filing text; marketable securities decomposed from the 10-Q comparative column (39,065 debt + 12,886 equity = 51,951) | agree |
| Missing data silently filled | AVGO reports `ProfitLoss`, not `NetIncomeLoss`; AMD reports no `LongTermDebt` total | comps use EPS and EBIT (both present for every peer); debt summed from current + noncurrent | no silent fill |
| Currency | all companies report in USD | none needed | — |

The evidence ledger (`docs/evidence-ledger.csv`) carries the `type` column (fact / guidance / judgment / calculation)
that the catalog asks for; this file is the normalization layer between the ledger and the model.
