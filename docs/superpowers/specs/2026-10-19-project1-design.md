# Project 1 design — NVIDIA pro-forma workbench

Date: 2026-10-19. Author of the design choices: Claude Code (Claude Fable 5.1), drafted for the
student to accept, change or reject. The valuation judgments stay the student's.

## Intent

Turn the Lab 3–13 NVIDIA work in this repository into the Project 1 package the course asks
for: a locally runnable, semi-adjustable pro-forma workbench, an FCFF DCF driven by the
pro-forma, a committee recommendation as a range with conditions, and the seven-part
submission bundle (Edition A unchanged, Edition B, repository with visible output, memo,
validation and AI-use record, three video plans and transcript stubs, manifest).

## Goals

- Satisfy the ten "Required finance system" items of the Project 1 brief.
- Reuse the Lab 10 engine (`nvda_proforma.py`) unchanged; it is the known, checked model.
- A grader can read every material number without running code (`output/visible_output.md`).
- A teammate can move one bounded driver in the app and watch a check fail loudly.

## Non-goals and anti-goals

- No hosting, no credentials, no network at run time (SEC fetch script is optional and cached).
- No interface polish beyond what the rubric reads (bounds, checks, reset).
- Never average methods; never present a point estimate as the answer.
- Never invent a number: unverifiable items stay `[fill in]` or `unresolved`.

## Constraints and decisions

| Decision | Choice | Why |
|---|---|---|
| Valuation date | 23 Sep 2026, close $225.51 | latest Nasdaq close cached in `src/beta_prices/`; same date as the Lab 10/11 work |
| Bridge balance sheet | 26 Jul 2026 10-Q (Q2 FY2027) | the newest filed balance sheet before the valuation date; carries the $24.9bn of new notes the Lab 10 base case left out |
| Share basis | 24,100m outstanding (10-Q cover, 21 Aug 2026) plus the Q2 FY2027 dilutive increment | point-in-time count, diluted for RSUs |
| Cash-flow definition | FCFF = EBIT × (1 − t) + D&A + SBC − capex − ΔWC, from the pro-forma years | brief requires FCFF/WACC; the FCFE engine stays as a cross-check |
| Discount rate | WACC from CAPM cost of equity (base 12%, the student's Lab 10 judgment) and the filed cost of debt, market-value weights | course convention; debt weight is under 1% so WACC ≈ cost of equity |
| Terminal | Gordon growth on FY2032 FCFF, base 3% | course convention |
| Product shape | Streamlit app (`app.py`) over `analysis.py`; standard-library engine | course starter shape; pandas/streamlit only in the interface |
| Exposed drivers | 9 bounded controls, each with a defended bound in `engine.py` | "an unbounded slider is an unmade decision" |
| Locked | accounting engine, provenance (opening balance sheet, bridge), checks | they have right answers |
| Peers | AMD (use, qualified) and Broadcom (qualified), policy frozen before the numbers; prices 23 Sep 2026; trailing GAAP from each company's latest 10-Q | Lab 7–8 policy carried forward to the valuation date |
| Locked Changed-Input Record | the Lab 11 prediction committed 2026-09-29 (`3bcbdde`) before the results | human-authored, AI-off, pre-run |

## Parts

1. `engine.py` — pro-forma wrapper, FCFF, WACC, DCF, bridge, grid, reverse DCF, cases, comps, checks, driver specification with bounds.
2. `analysis.py` — `run_analysis(inputs)`; CLI writes `output/visible_output.json` and `output/visible_output.md`.
3. `app.py` — driver panel, checks panel, statements, valuation, sensitivity, frozen-output tab.
4. `tests/` — known answers (training DCF, ABG engine, NVDA FCFE $123.05), articulation, monotonicity, bridge, loud failure.
5. `docs/` — decision memo, validation and AI use, research evolution, evidence ledger, assumption-challenge record, manifest, video plans, transcript stubs.
6. `fetch_sec_facts.py` + `src/sec_xbrl/` — reproducible SEC XBRL extraction with the as-of date.

## Left to the student

Edition A receipt identifier, in-class partner notes, video recording and transcripts, the
accept/modify/reject verdict on every AI-use row, and the final wording of the committee ask.
