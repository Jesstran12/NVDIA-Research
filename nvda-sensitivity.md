# Lab 11 — NVIDIA Pro-Forma Sensitivity

**Question:** Which assumptions drive my company's forecast and value, and what explains their effects?

Model: `nvda_proforma.py` (Lab 10), unchanged. Sensitivity script: `nvda_sensitivity.py`.
Outputs for every run: FY2031E operating income, FY2031E free cash flow to equity (FCFE), value per share.
USD millions unless stated.

## Drivers and ranges

| Driver | Model input | Base | Lower | Higher | Years affected | Units |
|---|---|---|---|---|---|---|
| AI Data Center demand | `growth` | 25 / 12 / 7 / 4 | 20 / 7 / 2 / −1 | 30 / 17 / 12 / 9 | FY2028E–FY2031E (FY2027E held at 85.6%) | % revenue growth; ±5 percentage points each year |
| CUDA competitive advantage (pricing power) | `gross_margin` | 74.5 / 73.0 / 72.0 / 71.0 / 70.0 | 71.5 / 70.0 / 69.0 / 68.0 / 67.0 | 77.5 / 76.0 / 75.0 / 74.0 / 73.0 | FY2027E–FY2031E | % of revenue; ±3 percentage points each year |

Why these inputs: Data Center is about 90% of NVIDIA's revenue, so the growth path stands in for
Data Center demand. CUDA lock-in shows up as pricing power, which the model carries in gross margin.
Supply capacity (TSMC/packaging) limits volume, not price, so it is a risk noted here, not a separate driver.

## Locked Changed-Input Record

I expect revenue growth to move NVIDIA's value more than gross margin, by roughly three times.

AI Data Center is about 90% of revenue, so the FY28–FY31 growth path is effectively a bet on Data Center demand. Growth compounds. Cutting each year by 5pp (25/12/7/4 becomes 20/7/2/−1) leaves FY31 revenue about 17% below base. Since most of a DCF's value sits in the terminal year, I expect value to fall by a similar amount, roughly 15–20%.

Gross margin stands in for CUDA's moat. If the lock-in erodes, AMD and custom chips force price cuts and margin falls. A 3pp drop on a ~70% gross margin is only about a 4% cut to gross profit. Operating expenses don't scale down with it, so operating profit falls a bit more, around 5%. That margin cut doesn't compound, so I expect value to fall about 5%.

I expect both effects to be roughly symmetric: the upside case should move value by about the same amount as the downside.

This test understates CUDA's importance. If the moat really erodes, NVIDIA loses volume as well as price, which would hit growth too. The one-at-a-time test only captures the margin channel, so a small margin result shouldn't be read as "CUDA doesn't matter."

I'd be wrong if the margin shock moves value as much as the growth shock. That would mean the model's operating leverage is higher than I assumed, or that FY27, which I held fixed, carries more of the value than the later years.

## Results

Run: `python3 nvda_sensitivity.py` (full output saved in [`output/lab11_sensitivity_run.txt`](output/lab11_sensitivity_run.txt)). Base $123.05; every run's checks pass; restored base identical to the first run (largest difference 0.000000, PASS).

| Driver | Case | Input | FY2031E operating income | change | FY2031E FCFE | change | $/share | change |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Revenue growth FY28–31 | lower | 20 / 7 / 2 / −1 % | 298,796.3 | −60,224.8 | 260,739.2 | −46,916.4 | 107.55 | −15.50 |
| | base | 25 / 12 / 7 / 4 % | 359,021.2 | 0 | 307,655.6 | 0 | 123.05 | 0 |
| | higher | 30 / 17 / 12 / 9 % | 427,906.2 | +68,885.1 | 360,696.3 | +53,040.7 | 140.44 | +17.39 |
| Gross margin FY27–31 | lower | 71.5 → 67.0 % | 340,289.6 | −18,731.5 | 291,895.1 | −15,760.5 | 116.73 | −6.33 |
| | base | 74.5 → 70.0 % | 359,021.2 | 0 | 307,655.6 | 0 | 123.05 | 0 |
| | higher | 77.5 → 73.0 % | 377,752.7 | +18,731.5 | 323,416.1 | +15,760.5 | 129.37 | +6.32 |

Spans (max − min over valid runs): growth — operating income 129,109.9, FCFE 99,957.1, $32.89 per share; gross margin — 37,463.1, 31,521.0, $12.65.

**Against the prediction.** Direction and order right: growth moves value 2.6 times as much as margin (predicted about 3×). Size: the growth cut moved value −12.6%, less than the 15–20% predicted, because FY2027E (held fixed) carries about a third of the explicit-period value and a slower path shrinks the working-capital build, which partly offsets lower profit in FCFE. The margin result (−5.1%) matched the ~5% predicted. Roughly symmetric, as predicted (−15.50 vs +17.39). Conclusion unchanged: watch/defer; the growth path after FY2027 is the first research priority, and in Project 1 it is the first slider in the product.

**Over these ranges only:** ±5 pp of growth and ±3 pp of margin are my choices; Project 1 reruns the ranking at the defended bounds (−25/+25 pp and −13/+4 pp) and at half of them — growth leads in every case.

## Partner notes

_Question received and my response; the check I performed on my partner's analysis._
