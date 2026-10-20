# Cold-run log

Fresh clone, fresh virtual environment, README instructions only, run by `scripts/cold_run.sh` (the full console
output is reproduced below). A second cold run on a different machine by a partner should be added to this table.

| Field | Value |
|---|---|
| Date / machine | 2026-10-19 21:11 (−04:00) / macOS 15.6, Python 3.13 via `python3 -m venv` |
| Commit cloned | `145e5d7` |
| Steps followed | README "Setup and run": clone → venv → `pip install -r requirements.txt` → `python -m pytest -q` → `python analysis.py` → `python analysis.py --break` → `streamlit run app.py` |
| First failure | none (pip printed a new-release notice only) |
| Resolution / limitation | not applicable; the only known environment dependency is Streamlit ≥ 1.49 for the `width='stretch'` argument |
| Time to visible output | 22 s from clone to `output/visible_output.md` written |
| Tests | 17 passed |
| App started | HTTP 200 on the first probe, 1 s after launch; total cold run 24 s |
| Partner README-only cold run (Week 7 studio) | [fill in: first failure, elapsed time, who ran it] |

```
== cold run started 2026-10-19T21:11
commit: 145e5d7
.................                                                        [100%]
17 passed in 0.06s
NVIDIA (NVDA) as of 2026-09-23: price $225.51
Value per share: base $123.93 | low $80.31 | high $186.63 | FCFE cross-check $123.05
WACC 11.99% | terminal share 67.6% | checks all pass
Action: Do not initiate at this price; keep on watch
Wrote output/visible_output.json, output/visible_output.md, output/analysis_full.json
Model refused: FY2027E does not balance: assets − liabilities − equity = -10,088.0
(the gap is the year's change in cash with the sign flipped: -10,088.0)
== visible output ready after 22 s
app answered HTTP 200 after 1 s
== cold run finished after 24 s
```
