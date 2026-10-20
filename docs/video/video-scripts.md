# Video scripts — NVIDIA (NVDA) Project 1

Spoken word-for-word scripts at about 140 words a minute, with the screen action in **[brackets]**. Every number
matches `output/visible_output.md` at the frozen commit; if you rerun the analysis after changing an input, re-check
the numbers before recording. Replace *[your name]* and *[partner]* before you start. Webcam on in all three.

---

## Video 1 — Research evolution and AI-output check (target 2:40, limit 3:00)

**[Screen: `docs/research-evolution.md` open at the top. Webcam on.]**

**[0:00]** I'm *[your name]*. This is the research evolution for my Project 1 on NVIDIA, ticker NVDA.

**[Scroll to Edition A.]** This is Edition A, submitted on the third of September before any valuation AI work,
unchanged. My call then was watch-defer, and the reason was simple: nothing was measured yet. I had the FY2026
10-K, revenue of 216 billion, operating income of 130 billion, but no verified price, no diluted share count, and no
forecast. I listed those as unknowns and wrote a research plan.

**[0:35] [Scroll to the A-to-B table.]** Edition B keeps the same posture but the evidence underneath it is
completely different. The action is: do not initiate at 225 dollars 51, keep the name on watch. The value per share
is 124 dollars in the base case, 80 in the low case and 187 in the high case, so the price sits above even the high
case.

Three things drove the change, and I keep them separate. First, course instruction: the FCFF and WACC architecture,
the pro-forma as a labelled assumption set with checks, and the frozen peer policy. Second, my own analysis: the
FY2027 build from guidance, the growth deceleration from 25 to 4 percent, the margin drift, and the 12 percent cost of
equity against a measured 13 to 15. Third, peer challenge: *[partner]* asked what happens to NVIDIA if AI stalls,
and that question turned a small sensitivity into the low case, where growth, margin, opex and the discount rate all
move together.

**[1:25] [Switch to `output/visible_output.md`, the reverse DCF table.]** Why was that evidence enough to move
from "not measured" to "do not initiate"? The reverse DCF. Holding everything else at base, the price needs about
24 percentage points more growth in every year from FY2028 to FY2031, roughly 49, 36, 31, 28 percent, or a cost of
equity near 8 percent on a stock whose measured beta is above 1.8. Both are testable in the next two quarterly
reports, so the call comes with triggers, not a point.

**[1:55] [Switch to `docs/validation-and-ai-use.md`, the AI-use register, the "Bridge balance sheet" row.]**
Now the AI check. When the Project 1 layer was built with Claude Code, the AI proposed using the newest balance
sheet, July 2026, for the enterprise-to-equity bridge: 22 billion of cash, 77 billion of securities, 33 billion of
debt after the new notes. I checked the dates. The pro-forma starts at the FY2026 balance sheet, the 25th of
January, and the first year of cash flow is all of FY2027. The July sheet already contains the first half of
FY2027's cash, so using it would count that half-year twice. I corrected it: the bridge is dated at the opening
balance sheet, and the July sheet is kept as a toggle that turns the checks panel red. The difference was about one
dollar a share, but the principle is what matters: the machine proposes, the dates decide.

**[2:35]** So Edition B is the same posture with a measured range, conditions and triggers, and every AI proposal and
my verdict on it is in one file. Thank you.

---

## Video 2 — Codebase walkthrough and highest-risk test (target 4:40, limit 5:00)

**[Screen: VS Code with the repository open; README visible; a terminal at the bottom with the virtual environment
activated. Webcam on.]**

**[0:00]** I'm *[your name]*. This is the code walkthrough for my NVIDIA valuation workbench.

**[Scroll README to the repository map.]** The architecture is one direction: evidence, then analysis, then tests,
then a frozen visible output, then the app. The engine is standard-library Python. Pandas and Streamlit only render.

**[0:25] [Open `nvda_proforma.py`, top of file.]** This is the Lab 10 engine, unchanged. Every assumption sits at the
top with a label: history, guidance or judgment. Growth 85.6 percent in FY2027 from guidance plus one quarter of
judgment, then 25, 12, 7, 4. Gross margin 74.5 drifting to 70. **[Scroll to `opening`.]** The opening balance sheet is
the FY2026 10-K, page 53, line by line. **[Scroll to `project_year`.]** Each year computes the income statement, then
the balance sheet except cash, then cash flow, and cash last, as the residual. **[Point at `assert_balanced`.]** This
function refuses to value a sheet that does not balance.

**[1:15] [Open `engine.py`, scroll to `DRIVERS`.]** The Project 1 layer. Nine exposed drivers, each with a defended
bound and the reason for the bound. Growth shift from minus 25 to plus 25 points: minus 25 is "AI capex stops", plus
25 is one point above what the price implies. **[Scroll to `fcff_rows`.]** Free cash flow to the firm is EBIT times
one minus tax, plus D&A, plus stock compensation, minus capex, minus the working-capital build. **[Scroll to
`wacc_inputs` and `dcf`.]** WACC uses market weights; debt is 0.16 percent of capital, so WACC is 11.99 percent.
Five explicit years, a Gordon terminal value, then the bridge: enterprise value plus cash and marketable securities
minus debt, over 24,195 million diluted shares. **[Scroll to `bridge_for` and `BRIDGE_FY2026`.]** The bridge is dated
at the opening balance sheet so no cash flow is counted twice. **[Scroll to `run_checks`.]** Eighteen checks run on
every call; failures come back as a list, never as an exception that hides.

**[2:20] [Open `analysis.py`, `run_analysis`.]** `analysis.py` computes every material result and writes the frozen
output; the recommendation rule is here, not in the interface.

**[2:35] [Terminal.]** Reproduce it.

```
python -m pytest -q
```

Seventeen tests: the training-case DCF to four decimals, the ABG known answer of 291 dollars 75, my base reproduced
through the wrapper, articulation under shocks, monotonicity in WACC and growth, the bridge.

```
python analysis.py
```

Base 123 dollars 93, low 80 dollars 31, high 186 dollars 63, checks all pass. **[Open `output/visible_output.md`.]**
This file is what a grader reads without running anything.

**[3:20] [Scroll to the reverse DCF section.]** The highest-risk claim is that the price pays for growth the filings
do not show. The test is the reverse DCF: solve the growth shift that makes value equal 225 dollars 51. Answer: plus
23.7 points a year. My defended bound is plus 25. So the call survives by 1.3 points. That is the risk I report, not
hide: one judgment stands between my bound and the market's path. **[Scroll to "What would reverse the call".]** On
top of the high case it still takes 17 more points a year.

**[3:55] [Terminal.]** And the loud failure.

```
python analysis.py --break
```

The cash line is typed instead of linked, and the model refuses: FY2027 does not balance by minus 10,088, which is
exactly the year's change in cash with the sign flipped. The fingerprint of an unlinked cash line.

**[4:20]** Limitations I have not resolved: the value is struck at the January balance sheet and compared with a
September price, about eight percent of roll-forward; FY2027 is a 53-week year; stock compensation is added back,
and treating it as cash costs about six dollars. All three are in the validation record.

**[4:40]** Everything on screen came from `python analysis.py`, and the frozen JSON the app shows is that run.
Thank you.

---

## Video 3 — Investment-committee presentation with the live demo (target 4:45, limit 5:00)

**[Before recording: `streamlit run app.py` running in the browser, window wide enough that the sidebar shows,
base restored. Webcam on. Start on the app.]**

**[0:00]** I'm *[your name]*, the AI task-force analyst in the sector group. The fund holds no NVIDIA. My
recommendation: do not initiate at 225 dollars 51; keep the name on watch. Value per share 124 base, 80 to 187 across
the causal cases. Here is the tool the team keeps after this meeting.

**[0:15] [Sidebar: drag "Revenue growth FY2028E–FY2031E shift" to −10.]** Move one bounded driver. Growth after
FY2027 ten points lower each year. **[Point at the header.]** Value falls from 123 dollars 93 to about 95; the
change-from-base line shows minus 29. **[Click the Sensitivity tab; point at the trace table.]** The trace shows why:
FY2031 revenue drops, operating income drops, free cash flow drops, and the terminal value carries most of it. Every
check stays green, so this is a coherent downside.

**[0:45] [Sidebar: press "Reset to base".]** Reset. 123 dollars 93 again. The slider stops at minus 25 and plus 25
for a reason: minus 25 is "AI capex stops", plus 25 is one point above what the market price already assumes. An
unbounded slider would be an unmade decision.

**[1:05] [Sidebar: tick "Use the Q2 FY2027 balance sheet for the bridge".]** Now an incoherent input. The checks
panel goes red: the bridge is dated July 2026 but the cash flows start in January, so the first half of FY2027 would
be counted twice. The tool tells you what it believes before you present a number. **[Untick it, or press Reset.]**
Green again.

**[1:35] [Click "Grid and cases".]** The range. Low case, 80 dollars: hyperscalers pause, custom silicon takes
price, R&D keeps growing, 13 percent cost of equity. High case, 187: the compute cycle compounds at 35, 22, 17, 14,
margins hold, 11 percent. Each is a full rerun, never a sum of shocks. The price is above the high case.

**[Click "Reverse DCF and comps".]** What the price assumes: 24 points a year more growth than my base path, or an 8
percent cost of equity, or 7.8 percent terminal growth. No margin or cost assumption inside the bounds gets there.
Comparables: NVIDIA trades at 28 times trailing earnings; Broadcom at 45 times implies 358 dollars; AMD's 158 times
is reported but not meaningful under the policy I froze first. The multiples say what the market expects; the DCF
says what the filings support. I do not average them.

**[2:30] [Click "Assumption record".]** The three assumptions that carry the value. Growth after FY2027, which is
the valuation. Cost of equity at 12 percent, which is the generous end of a measured 13 to 15. Gross margin, 74.5
drifting to 70. *[Partner]*'s challenge, "what if AI stalls", built the low case. My locked prediction from Lab 11,
committed before the run, said growth would move value three times as much as margin; the result was 2.6 times, with
the direction and order right and the size reconciled.

**[3:20]** Risks and triggers, each with a metric, a threshold and a window. Data Center revenue down quarter on
quarter in either of the next two reports: withdraw the base and rebuild as the low case. Gross-margin guidance below
72 and falling: the margin path drops three points. Opex growing faster than revenue for two quarters: opex path up
two points. The bridge failing to reconcile on the next 10-Q: the per-share number is withdrawn until it does.

Conditions to initiate: the price falls below the base case of 124 with the checks passing, or two quarters of
Data Center growth lift the high case above the price. That would take a path near 42 percent in FY2028, not 25.

**[4:10]** The ask. Approve watch with no position. Authorise a re-review within one week of the Q3 FY2027 report in
November, with this tool re-run on the new filing. I own the monitoring; the sector team owns the demand view.

**[4:35]** Every AI proposal and my verdict on it is in the validation record; the judgments and the bounds are
mine. Thank you. I'll take questions.

---

### After recording, for each video

1. Upload to YouTube as unlisted or public, titled as in `docs/project-submission-manifest.csv`.
2. Paste the auto transcript into `docs/transcript-video-N.txt`; correct NVDA, AMD, AVGO, the dollar values above,
   "FCFF", "WACC", "10-Q", and add a timestamp at each bracketed moment.
3. Enter the URL, duration and timestamp index in the manifest, and confirm the link plays while logged out.
