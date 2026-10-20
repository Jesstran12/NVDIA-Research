# Video 3 — Investment-committee presentation with the live product demo (max 5:00)

**The demo is the main delivery and opens the video.** Screen: `streamlit run app.py` already running, base restored.
Webcam on. Lead with the decision, keep the tool on screen while defending it, end with the committee ask.

| Time | Required element | What to show and say |
|---|---|---|
| 0:00–0:15 | Decision first | "Do not initiate NVIDIA at $225.51; keep it on watch. Base $124, range $80–$187. Here is the tool the team can use after this meeting." |
| 0:15–0:45 | Demo 1 — move one bounded driver, read the result | Sidebar: drag **Revenue growth FY2028–31 shift** to −10 pp. Read the header: value falls from $123.93 to about $96; the change-from-base line; the checks stay green. Open the Sensitivity tab trace: revenue → operating income → FCFF → value. |
| 0:45–1:05 | Demo 2 — explain against the restored base | Press **Reset to base**. "$123.93 again. The bound is −25 to +25 pp because −25 is 'AI capex stops' and +25 is one point above what the price implies." |
| 1:05–1:35 | Demo 3 — a check failing loudly, then recover | Tick **Use the Q2 FY2027 balance sheet for the bridge**. The checks panel turns red: "bridge dated after the cash flows start: H1 FY2027 counted twice." (Alternative: tick Stress mode, push terminal growth to 12% → "terminal growth below the discount rate" fails; the model refuses to value.) Untick / Reset to base → green. |
| 1:35–2:30 | Defend the range and the evidence | Grid and cases tab: low $80 (digestion + custom silicon + 13%), high $187 (compounding cycle + CUDA holds + 11%). "The price is above the high case." Reverse DCF tab: +24 pp growth a year, 8% cost of equity, 7.8% terminal growth. Comps: NVIDIA 28.5x trailing, Broadcom 45x implies $358, AMD not meaningful — "the multiples say what the market expects, the DCF says what the filings support; I do not average them." |
| 2:30–3:30 | Material assumptions and the challenge record | Assumption record tab: growth path, cost of equity (12% is the generous end of a measured 13–14.8%), gross margin. Name the partner challenge that built the low case. State the locked prediction result in one sentence. |
| 3:30–4:20 | Risks, conditions, triggers | Read the four triggers with metric · threshold · window · effect. Conditions to initiate: price below $124 with checks passing, or two quarters that lift the high case above the price. |
| 4:20–4:50 | Committee ask | "Approve watch/defer with no position; authorise a re-review within a week of the Q3 FY2027 report with this tool re-run on the new filing. I own the monitoring; the sector team owns the demand view." |
| 4:50–5:00 | Close | AI-use pointer: "Every AI proposal and its disposition is in the validation record." |

Timestamp index for the manifest: decision [mm:ss], driver moved and result read [mm:ss], base restored [mm:ss], check
failing and recovered [mm:ss], range and evidence [mm:ss], triggers [mm:ss], committee ask [mm:ss].
