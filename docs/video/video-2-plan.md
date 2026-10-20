# Video 2 — Codebase walkthrough and highest-risk test (max 5:00)

Screen: VS Code with the repository open and a terminal. Webcam on. Reading the README or showing only the UI is not enough:
explain the architecture, the data flow, the financial logic and reproduce the output.

| Time | Required element | What to show and say |
|---|---|---|
| 0:00–0:30 | Architecture | README repository map. "Evidence → analysis → tests → frozen output → app. The engine is standard library; Streamlit only renders." |
| 0:30–1:30 | Data flow and key files | `nvda_proforma.py` top block: labelled assumptions, opening balance sheet from the 10-K p. 53. `engine.py`: `DRIVERS` (bounds with reasons), `run_proforma` (sets, runs, restores), `fcff_rows`, `dcf`, `bridge_for`, `run_checks`. `analysis.py`: `run_analysis` and the recommendation rule. |
| 1:30–2:15 | Financial logic | In `engine.py`: FCFF = EBIT(1 − t) + D&A + SBC − capex − ΔWC; WACC with market weights; Gordon terminal; bridge at the opening date (say why: no double counting). |
| 2:15–3:00 | Reproduce the output | Terminal: `python -m pytest -q` (17 pass) then `python analysis.py` → base $123.93, low $80.31, high $186.63, checks all pass; open `output/visible_output.md`. |
| 3:00–4:10 | Highest-risk test (required) | "The highest-risk claim is that the price pays for growth the filings do not show. The test is the reverse DCF: `engine.solve('growth_shift')` → +23.7 pp a year, inside the +25 pp bound by 1.3 pp. The call survives, but barely: this is the risk I report." Then the loud failure: `python analysis.py --break` → "Model refused … −10,088 = the year's change in cash with the sign flipped." |
| 4:10–4:45 | Failure mode / unresolved risk | "Values are struck at 25 Jan 2026 against a price eight months later (about +8% if rolled forward); FY2027 is a 53-week year; SBC is added back (toggle −$6). The growth bound is one judgment away from the market." |
| 4:45–5:00 | Close | "Everything on screen came from `python analysis.py`; the frozen JSON the app shows is that run." |

Timestamp index for the manifest: architecture [mm:ss], financial logic [mm:ss], reproduction command and output [mm:ss],
highest-risk test [mm:ss], loud failure [mm:ss], limitation [mm:ss].
