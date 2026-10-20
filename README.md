# NVIDIA (NVDA) — Project 1: pro-forma valuation workbench

**FIN 43900, Fall 2026 — Corporate Finance Application.** A locally runnable, semi-adjustable
pro-forma valuation tool for NVIDIA, built on the Lab 10 three-statement engine, with an FCFF
DCF, comparable-company multiples, one-at-a-time sensitivities, a reverse DCF and checks that
fail loudly. Learning demonstration for a course; not investment research and not investment advice.

## Finance decision and intended user

| | |
|---|---|
| Intended user | Buy-side investment committee; the fund holds no position in NVIDIA |
| Decision | Initiate, watch/defer, or do not initiate NVIDIA common stock (NASDAQ: NVDA) at the 23 Sep 2026 price of $225.51 |
| Horizon | Three- to five-year holding period; next review after the Q3 FY2027 report (November 2026) |
| Valuation date | 23 Sep 2026 (latest Nasdaq close cached in `src/beta_prices/`); information cutoff: the Q2 FY2027 10-Q filed 26 Aug 2026 |
| Currency and units | USD; USD millions in the statements; USD per share for values |
| Share basis | 24,100m shares outstanding (10-Q cover, 21 Aug 2026) plus the 95m dilutive award increment from the Q2 FY2027 EPS note = 24,195m diluted |
| Exclusions | Equity-stake gains are not forecast; non-marketable securities are left out of the bridge; operating leases are not debt; no transaction multiples; nothing after 23 Sep 2026 |

**Result (base case, all checks passing):** value per share **$123.93** on an FCFF DCF at an 11.99% WACC
and 3% terminal growth, causal range **$80 (low) – $187 (high)**, against a price of **$225.51**.
**Committee action: do not initiate at this price; keep on watch.** The price sits above the high
case: it pays for roughly 24 points a year more growth in FY2028–FY2031 than the filings and guidance
support, or a cost of equity near 8%. Conditions, reversal triggers and the committee ask are in
[`output/visible_output.md`](output/visible_output.md) and [`docs/decision-memo.md`](docs/decision-memo.md).

## Visible result (no code needed)

- [`output/visible_output.md`](output/visible_output.md) — the executed output: decision, checks,
  driver panel with bounds, five-year statements, FCFF / WACC / bridge, cases, grid, sensitivities,
  reverse DCF, comparables, why the methods disagree, sources.
- [`output/visible_output.json`](output/visible_output.json) — the frozen interface contract the app renders.
- [`docs/screenshots/`](docs/screenshots/) — the workbench at base and with a check failing.

## Setup and run

```
git clone https://github.com/sonha2409/NVDIA-Research.git
cd NVDIA-Research
python3 -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q            # 17 checks: known answers, articulation, monotonicity, bridge, loud failure
python analysis.py             # recompute everything; writes output/visible_output.{json,md}
python analysis.py --break     # the loud-failure demonstration: typed cash line, the model refuses
streamlit run app.py           # the workbench (opens http://localhost:8501)
```

The engine (`engine.py`, `nvda_proforma.py`, `proforma.py`, `analysis.py`) uses only the Python
standard library; pandas and Streamlit are needed only for the interface and pytest for the tests.
No credentials, no `.env`, no network at run time (`fetch_sec_facts.py` refreshes the SEC extract and
is optional). Python 3.11 or later.

## Repository map

| Path | What it is |
|---|---|
| `nvda_proforma.py` | **Lab 10 engine, unchanged.** Labelled assumptions, five projected years, check block, FCFE value ($123.05). `--break` shows the refusal. |
| `proforma.py` | Lab 09 engine on the ABG training case (known answer $291.75). |
| `engine.py` | Project 1 layer: the driver panel with bounds (`DRIVERS`), FCFF, WACC, DCF, bridge, checks, sensitivities, grid, cases, reverse DCF, comparables with the frozen peer policy. |
| `analysis.py` | `run_analysis()` computes every material result; the CLI writes `output/`. The recommendation rule lives here. |
| `app.py` | Streamlit workbench: bounded sliders, base reset, stress mode, checks panel, statements, valuation, sensitivity, grid, cases, reverse DCF, comps, assumption record, frozen output. |
| `tests/test_project1.py` | The validation suite (`python -m pytest -q`). |
| `output/` | Visible executed output (Markdown, JSON) and the full result dump. |
| `docs/` | Decision memo, validation and AI-use record, research evolution (Edition A unchanged + Edition B), evidence ledger, base-year normalization (contamination catalog), assumption-challenge record, manifest, video plans and transcript stubs. |
| `src/` | Saved filings (FY2024–FY2026 10-Ks), Nasdaq price caches, the SEC XBRL extract (`src/sec_xbrl/companyfacts_extract.csv`). |
| `nvda-proforma.md`, `nvda-sensitivity.md`, `nvda-dcf-inputs.md`, `abg-proforma.md` | Lab write-ups the project builds on (history grid, assumption reasons, Lab 11 locked prediction, Lab 7–8 peer policy). |
| `archive/` | Lab 12 what-if study (betas, tornado, named cases, reverse DCF at the 21 Sep 2026 price). |
| `beta.py`, `dcf.py`, `peer_valuation.py`, `mandate.py` | Earlier lab scripts kept for provenance. |

### Analysis-to-interface flow

1. Sourced inputs live in `engine.py` (provenance blocks), `nvda_proforma.py` (assumptions with labels) and `docs/evidence-ledger.csv`.
2. `analysis.py` computes every material result through `engine.py`; the app never computes a recommendation on its own.
3. `tests/` run the known-answer, changed-input, articulation, monotonicity and bridge checks.
4. `python analysis.py` exports the validated subset to `output/visible_output.json` with as-of date, units and limitations.
5. `app.py` renders the live model for exploration and the frozen file on its last tab; it formats, it does not replace the engine.

Direction: **evidence → analysis → tests → frozen visible output → app**.

## What is locked, what is exposed

- **Locked:** the three-statement engine and its articulation checks; the opening balance sheet (FY2026 10-K p. 53);
  the bridge balance sheets; working-capital days; the maturity ladder; the cash floor; the payout; the share count.
- **Exposed (bounded):** revenue growth FY2028–31 shift (−25 to +25 pp), FY2027E revenue (±10%), gross margin shift
  (−13 to +4 pp), opex ratio shift (−2 to +6 pp), tax rate (12–21%), capex ratio (1.5–6%), SBC ratio (1.5–6%),
  cost of equity (9–16%), terminal growth (0–4%). Each bound's reason, the challenge it faces and the evidence that
  would move it are in the app's assumption-record tab and in `docs/assumption-challenge-record.md`.
- **Failing loudly:** the checks panel turns red when a sheet does not balance, cash flow does not tie, the base
  year does not reconcile, terminal growth reaches the discount rate, the bridge date is inconsistent with the cash
  flows, the cash floor needs the commercial-paper backstop, or an input leaves its historical band. Stress mode
  unlocks the bounds so the user can see these failures on purpose; **Reset to base** recovers.

## Data sources and point-in-time boundary

NVIDIA Forms 10-K FY2024–FY2026 (accessions 0001045810-24-000029, -25-000023, -26-000021), Forms 10-Q Q1 and Q2
FY2027 (-26-000052, -26-000075), the Q2 FY2027 earnings release (8-K -26-000073, 26 Aug 2026), SEC XBRL companyfacts
for NVIDIA, AMD (CIK 0000002488) and Broadcom (CIK 0001730168), Nasdaq historical closes to 23 Sep 2026. Every
material input, its locator, its type (fact / guidance / judgment / calculation) and an independent check is in
[`docs/evidence-ledger.csv`](docs/evidence-ledger.csv); one-time items, basis changes and mechanical checks on the base
year are in [`docs/base-year-normalization.md`](docs/base-year-normalization.md). Nothing dated after 23 Sep 2026 is used.

## Financial conventions and assumptions

FCFF = EBIT × (1 − tax) + D&A + SBC − capex − working-capital build, from the pro-forma years; five explicit
end-of-year flows; Gordon terminal value at FY2031E; WACC with market-value weights (debt weight 0.16%); bridge at the
pro-forma opening date (25 Jan 2026) so no cash flow is counted twice; diluted point-in-time shares. The Lab 10 FCFE
value ($123.05) is kept as a cross-check. Multiples: trailing GAAP, same price date, policy frozen before the numbers.

## Validation and changed-input tests

`docs/validation-and-ai-use.md` holds the register: the training-case DCF (12 lines to four decimals), the ABG engine
($291.75), the NVIDIA base reproduced through the wrapper, articulation on every run, monotonicity in WACC and growth,
the bridge, the typed-cash refusal, the Locked Changed-Input Record (Lab 11 prediction committed 29 Sep 2026 before
the run), the highest-risk failure test, the cold run and the AI-use dispositions.

## Known limitations, monitoring and reversal triggers

- Values are struck at the opening balance-sheet date (25 Jan 2026) and compared with a price eight months later; rolling
  forward at the cost of equity adds about 8% before distributions paid since.
- FY2027E is a 53-week year; the extra week is carried into later years (about −$2 if normalised).
- SBC add-back (toggle shows the cash-cost alternative, about −$6).
- Peer GAAP earnings carry heavy acquired-intangible amortisation; AMD's trailing multiples are reported but not meaningful.
- Triggers: Data Center revenue down quarter on quarter → rebuild as the low case; gross-margin guidance below 72% and
  falling → −3 pp margin path; opex growing faster than revenue for two quarters → +2 pp opex path; bridge failing to
  reconcile on the next 10-Q → withdraw the per-share conclusion.

## AI use

Material AI use (Claude Code with Claude Fable 5.1, 19 Oct 2026; earlier labs with Claude Code and ChatGPT/Codex) is
disclosed with its disposition in `docs/validation-and-ai-use.md`. The judgments, bounds and the recommendation are
the student's to defend.
