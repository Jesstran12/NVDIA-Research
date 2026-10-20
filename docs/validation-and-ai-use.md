# Validation and AI Use — NVIDIA (NVDA), Project 1

## Decision, version, and as-of boundary

| | |
|---|---|
| Decision / user | Do not initiate at $225.51; keep on watch — for the buy-side investment committee (no position) |
| Repository | github.com/sonha2409/NVIDIA-RESEARCH-JESS, commit `dacdfea` (analysis run); the frozen version is HEAD at push (the frozen commit is also printed in `output/visible_output.json` → `run.commit`) |
| Run timestamp | printed in `output/visible_output.json` → `run.timestamp` |
| Source cutoffs | Filings to the Q2 FY2027 10-Q (filed 26 Aug 2026); prices to the 23 Sep 2026 close; peer filings to Broadcom's Q3 FY2026 10-Q (10 Sep 2026). Nothing after 23 Sep 2026 |
| Environment | Python 3.13 (3.11+ works), standard library for the engine; pandas 2.3, Streamlit 1.66, pytest 8 for the interface and tests (`requirements.txt`); macOS 15 |

## Data and convention ledger

The complete ledger (33 inputs with locator, type, independent check and risk) is `docs/evidence-ledger.csv`; the
base-year normalization (one-time items, basis changes, mechanical checks) is `docs/base-year-normalization.md`. The
load-bearing rows:

| Material input | Source | As-of | Definition / units | Transformation / exclusion | Risk |
|---|---|---|---|---|---|
| Revenue, gross profit, opex, operating income, net income FY2026 | 10-K FY2026 p. 51 (0001045810-26-000021) | 25 Jan 2026 | GAAP, USD millions | base year of the pro-forma; H20 charge noted (2.1 pp of gross margin) | provider revenue tag stale since FY2022 |
| Opening balance sheet | 10-K FY2026 p. 53 | 25 Jan 2026 | USD millions | reconciled line by line; totals 206,803 / 49,510 / 157,293 | none |
| Bridge: cash 10,605; marketable debt 39,065; marketable equity 12,886; debt 8,468 | 10-K p. 53; 10-Q comparative column; Note 11 | 25 Jan 2026 | carrying amounts | non-marketable securities (22,251) excluded; leases not debt | marketable equity switchable (−$0.53) |
| H1 FY2027 actuals; Q3 outlook | 10-Q Q2 FY2027 p. 3; 8-K 26 Aug 2026 | 26 Jul 2026 | GAAP; guidance | FY2027E = H1 + Q3 guide + Q4 judgment | Q4 is judgment (±10% bound) |
| Shares 24,100m + 95m dilution | 10-Q cover (21 Aug 2026); Note 4 | Aug 2026 | basic outstanding + dilutive increment | diluted 24,195m | cover count rounded to 0.1bn |
| Price $225.51 | Nasdaq close cached in `src/beta_prices/` | 23 Sep 2026 | unadjusted close | reverse-DCF target; market cap | none |
| Cost of equity 12% | judgment; `beta.py` 2.21 raw / 1.81 Blume; rf 5.00%, ERP 4.42% (course) | Sep 2026 | CAPM cross-check 13.0–14.8% | bounds 9–16% | 12% is the generous end |
| Cost of debt 2.92% | 10-Q Note 9 effective rates, principal-weighted over the Jan 2026 series | 25 Jan 2026 | pre-tax | after-tax at 17% | immaterial (debt weight 0.16%) |
| Peers: AMD, AVGO trailing GAAP EPS / EBIT, cash, debt, shares | SEC XBRL companyfacts, accessions in the ledger | Jun–Aug 2026 | TTM GAAP | policy frozen before the numbers; >100x not meaningful | acquired-intangible amortisation depresses GAAP |

## Validation register

| Claim / output | Failure mode | Test and expected result | Actual result | Disposition | Evidence |
|---|---|---|---|---|---|
| The DCF arithmetic is right | discounting, terminal, bridge errors | **Known answer (training case):** FCFF 100; 8/6/5/4/3; 10%; 3%; 50/300/50 → twelve lines incl. PV explicit 448.4408, TV 1,894.6486, EV 1,624.8685, $27.4974, 72.40% | all twelve match to four decimals; WACC 11% → $23.41 | pass | `tests/test_project1.py::test_training_case_dcf_known_answer` |
| The three-statement engine is right | unlinked lines | **Known answer (ABG, Lab 09):** $291.75, FY2026E FCFE 211.4, FY2030E cash 719.8, ~80% terminal | $291.75; 211.4; 719.8; 79.8% | pass | `test_abg_engine_known_answer`; `abg-proforma.md` |
| The Project 1 wrapper does not change the Lab 10 model | wrapper drift | FCFE through `engine.run_proforma` = $123.05 | $123.05 | pass | `test_nvda_fcfe_base_reproduced_through_wrapper` |
| Statements articulate | balance / cash / roll-forward breaks | every year, every run: assets − liabilities − equity = 0; cash BS = CF; PP&E and debt rolls = 0, under shocks too | all residuals 0.0 | pass | `test_statements_articulate_every_year_under_shocks`; app checks panel |
| Base year reconciles to the filing | typed opening sheet | model opening totals = 10-K p. 53 | gaps 0.0 | pass | `test_opening_balance_sheet_reconciles_to_filing` |
| Independent source / definition check on a load-bearing input | wrong definition | FY2026 revenue 215,938 and FY2026 debt 8,468 read from the filing text, then from the SEC XBRL API (`Revenues`, `LongTermDebt`); marketable securities 51,951 (10-K) decomposed as 39,065 debt + 12,886 equity from the 10-Q comparative column | all agree; decomposition sums exactly | pass | `docs/evidence-ledger.csv`; `src/sec_xbrl/companyfacts_extract.csv` |
| Directional changed-input test, written before execution | monotonicity | **Prediction:** raising the cost of equity from 12% to 13% lowers value per share by roughly a tenth, because every discount factor shrinks and the terminal denominator widens from 9% to 10% | $123.93 → $111.46 (−10.1%); value strictly falls across 9–16% and rises with terminal growth 0–4% | pass, as predicted | `test_value_falls_as_cost_of_equity_rises`; `output/visible_output.md` grid |
| Boundary: g ≥ WACC refused | infinite value | `dcf()` returns None at g = WACC and g > WACC; the app shows the refusal in red | None; red check "Terminal growth below the discount rate" | pass | `test_terminal_growth_at_or_above_wacc_is_refused` |
| Enterprise-to-equity bridge | double counting; wrong shares | EV + cash & securities − debt = equity to the cent; diluted point-in-time shares; bridge dated at the cash-flow start | 2,944,373 + 62,556 − 8,468 = 2,998,461; 24,195m; dated 25 Jan 2026 | pass | `test_bridge_reconciles_and_uses_diluted_point_in_time_shares` |
| Peer-policy and multiple-definition consistency | mixed dates / definitions | same price date for all; EV = market cap + carrying debt − cash & STI; TTM GAAP; >100x flagged | consistent; AMD 158x / 153x flagged not meaningful | pass | `test_comps_policy_consistency` |
| **Highest-risk failure test:** the FY2028–31 growth path is the valuation | the conclusion rests on one judgment | If the price can be reached inside the defended growth bound, the "do not initiate" call is only as strong as the bound. Reverse DCF: solve the growth shift for $225.51 | +23.7 pp a year (path ≈ 49 / 36 / 31 / 28%) — inside the +25 pp bound by 1.3 pp; the high case (+10 pp) gives $187 | **qualified:** the call survives, but only because the bound stops one point above the implied path. Reported as the main risk; the trigger table makes it reviewable each quarter | `output/visible_output.md` reverse DCF; `docs/decision-memo.md` §5 |
| Loud failure on a typed cash line | silent error | `python analysis.py --break`: cash typed at the opening value; the model must refuse and name the gap | "Model refused: FY2027E does not balance: assets − liabilities − equity = −10,088.0" | pass | `test_broken_cash_line_is_refused` |
| Base restored after every shocked run | state leakage | module assumptions identical before and after sweeps; base value identical | identical; $123.93 both times | pass | `test_base_restored_after_shocked_runs`; `nvda_sensitivity.py` restored-base PASS (difference 0.000000) |
| Out-of-bounds input is clamped and reported | silent extrapolation | cost of equity 50% → clamped to 16% and listed | clamped, reported | pass | `test_out_of_bounds_input_is_clamped_and_reported` |
| Ranking depends on the ranges? | false precision in the driver ranking | rank at full bounds, half bounds, Lab 11 ranges | growth path first in all three; middle order changes with the bounds | reported as "over these ranges" | `output/visible_output.md` sensitivity |
| **Cold run** (fresh environment, README only) | hidden dependency | clone → venv → `pip install -r requirements.txt` → `pytest` → `python analysis.py` → `streamlit run app.py` | no failure; 17 tests passed; visible output written 22 s after the clone; app answered HTTP 200 (commit `145e5d7`) | pass | `docs/cold-run-log.md` |

## Locked Changed-Input Record — human prediction first; AI closed during execution

### Precommit before the run and before AI assistance on the prediction

| Precommit timestamp | Repository commit | Material input | Old → new value / units | Expected output direction | Expected decision effect |
|---|---|---|---|---|---|
| 2026-09-29 17:56:29 −04:00 | `3bcbdde` ("Lab 11": `nvda-sensitivity.md` with the prediction and an empty Results section) | Revenue growth FY2028E–FY2031E (AI Data Center demand) | 25 / 12 / 7 / 4 % → 20 / 7 / 2 / −1 % (−5 pp each year) and 30 / 17 / 12 / 9 % (+5 pp) | value per share falls about 15–20% on the lower path; roughly symmetric on the upper path; growth moves value about three times as much as gross margin | no change to watch/defer; confirms that the growth path after FY2027 is the assumption to research |
| same | same | Gross margin FY2027E–FY2031E (CUDA pricing power) | 74.5 → 70.0 % path → −3 pp and +3 pp each year | value falls about 5% on the lower path (a 3 pp cut on a ~70% margin is ~4% of gross profit; opex does not scale down) | no change |

The prediction text is the Locked Changed-Input Record section of `nvda-sensitivity.md` as committed in `3bcbdde`;
it was written with AI closed and before `nvda_sensitivity.py` was run.

### Preserved execution result

| Before / after output | Actual decision effect | Prediction reconciliation | Failure diagnosis or why the action did not change | Evidence path |
|---|---|---|---|---|
| Growth −5 pp: $123.05 → **$107.55** (−12.6%); FY2031E operating income 359,021 → 298,796; FCFE 307,656 → 260,739. Growth +5 pp: → **$140.44** (+14.1%). Span $32.89 | none: watch/defer kept; growth path confirmed as the first research priority and the first slider in the product | Direction right. Order right (growth > margin). Size: the growth effect was smaller than the 15–20% predicted (−12.6%) and the ratio was 2.6× rather than 3×. Symmetry roughly held (−15.50 vs +17.39) | The prediction assumed value falls as much as FY2031 revenue (−17%). It fell less because (1) FY2027E, held fixed, carries about a third of the explicit-period value, and (2) lower growth shrinks the working-capital build, which partly offsets lower profit in FCFE (the FY2028E build falls from 14,075 to 11,483 and the FY2031E build from 4,354 to 266). The margin prediction (−5%) matched −5.1% | `output/lab11_sensitivity_run.txt`; `nvda-sensitivity.md` Results; commit history of `nvda-sensitivity.md` |
| Gross margin −3 pp: $123.05 → **$116.73** (−5.1%); +3 pp → **$129.37** (+5.1%). Span $12.65 | none | matched the prediction | not applicable | same |

The Project 1 FCFF engine reproduces the same test (±5 pp growth → $108.48 / $141.25; ±3 pp margin → $117.64 /
$130.21), so the record holds under both cash-flow definitions.

## Named AI-use register

Dispositions are Jess Tran's. The rows dated 2026-10-19 were drafted by the AI with the evidence it used and adopted by the student after reading the checks; the student owns each verdict and its reason.

| Tool / model surface and version | Interaction date | Material task | Output / claim used or considered | Independent check | Accept / modify / qualify / reject | Effect on decision |
|---|---|---|---|---|---|---|
| ChatGPT / Codex (Lab 03 session) | 2026-09-03 | Draft the Edition A report structure from the student's notes | report wording; UNSOURCED markers | sources gathered and checked by the student in the 10-K | accept (Edition A, before the project boundary) | none |
| Claude Code (Lab 09–12) | 2026-09-24 to 2026-10-01 | Generate the ABG engine from the Lab 09 request; port to NVIDIA; sensitivity and what-if scripts | `proforma.py`, `nvda_proforma.py`, `nvda_sensitivity.py`, `archive/nvda_whatif.py` | ABG known answer $291.75; check block 0.0 every year; `--break` refuses | accept after known-answer check | base case $123.05 |
| Claude Code, Claude Fable 5.1 | 2026-10-19 | Build the Project 1 layer (`engine.py`, `analysis.py`, `app.py`, tests, docs) | FCFF DCF, bridge, checks, sensitivities, comps, reverse DCF, the recommendation rule | training-case known answer to four decimals; FCFE cross-check $123.05 vs FCFF $123.93; 17 tests; articulation on every run | accept after the checks | the committee action and range |
| Claude Code, Claude Fable 5.1 | 2026-10-19 | Bridge balance sheet: AI first proposed the latest 10-Q (26 Jul 2026: cash 22,443; marketable 76,926; debt 33,366) | would have added the $24.9bn June 2026 notes and the H1 FY2027 cash build to the bridge | the pro-forma starts at 25 Jan 2026, so H1 FY2027 cash flow is already inside FY2027E FCFF: the July sheet double counts it (about +$0.99 per share) | **corrected:** bridge at the opening date; the July sheet kept as a flagged reference toggle that turns the checks panel red | none on the action; avoids a false +1% |
| Claude Code, Claude Fable 5.1 | 2026-10-19 | AI proposed including non-marketable securities (22,251) in the bridge as a non-operating asset | +$0.92 per share | no observable price; strategic stakes; 10-Q Note 7 carries them at cost less impairment | **rejected** | none |
| Claude Code, Claude Fable 5.1 | 2026-10-19 | AI computed AMD's trailing P/E (158x) and EV/EBIT (153x) and proposed excluding AMD | implied NVIDIA values of $617 / $582 | AMD's 15.7% operating margin vs NVIDIA's 65%: the multiple capitalises a recovery, not earnings | **qualified:** AMD stays in the table under the frozen policy, its multiples reported but marked not meaningful under the pre-declared >100x rule | none on the action; the comps disagreement is explained, not averaged |
| Claude Code, Claude Fable 5.1 | 2026-10-19 | AI drafted the committee action from the rule "price above the high case → do not initiate" | "do not initiate at this price; keep on watch" | the student's standing call since Lab 03 was watch/defer; the high case ($187) is a full rerun with checks passing; the reverse DCF puts the gap at +24 pp growth | accept: the committee hears "do not initiate at this price; keep on watch" | the headline |
| Claude Code (archive/nvda_whatif.py) | 2026-09-24 | AI proposed the 10% tutorial cost of equity as a comparison row | $159 per share | measured beta 2.21 → CAPM 13–14.8% | rejected as base; kept as a grid row | 12% stays, labelled generous |

Private prompts, credentials and trivial completions are not recorded. No credentials exist in this project.

## Cold-run log

See `docs/cold-run-log.md` (fresh clone, fresh virtual environment, README instructions only, first failure and time
to visible output recorded).

## Limitations, monitoring, and kill / escalation rules

- **Kill the base case** if Data Center revenue falls quarter on quarter in either of the next two reports; rebuild as the low case before any committee discussion.
- **Escalate** if the bridge fails to reconcile on the next 10-Q, if the balance sheet check fails on any input inside the bounds, or if the reverse-DCF growth shift moves inside the high case (+10 pp): the "do not initiate" call would then rest on a judgment the evidence no longer supports.
- **Known limitations:** valuation struck at 25 Jan 2026 against a 23 Sep 2026 price (roll-forward about +8% before distributions); 53-week FY2027; SBC add-back (−$6 if treated as cash); terminal reinvestment of 2.5% of net income at 3% growth; the course rf / ERP convention not re-sourced to September 2026; peer GAAP earnings depressed by amortisation; the cover share count rounded to 0.1bn.
