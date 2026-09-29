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

_To be added after the run: the sensitivity table, the restored-base check, and the actual result against the prediction._

## Partner notes

_Question received and my response; the check I performed on my partner's analysis._
