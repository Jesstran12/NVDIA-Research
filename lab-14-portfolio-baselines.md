# Lab 14: Portfolio Baselines (Meridian Foundation Reserve)

**D: the question.** What does each simple portfolio earn and risk, and does any of them meet the
Meridian mandate?

**Short answer.** Only the **benchmark** (40% IG bonds, 60% equity) reaches the 6.5% objective, at
6.80%, but it holds **0.0%** in reserve-eligible sleeves, so it fails Lab 13's 3.0% reserve rule.
Equal weight and inverse volatility pass the reserve rule easily but miss the objective. None of
the three baselines meets the mandate. The client's own benchmark breaks the client's mandate.

Files: [`portfolio.py`](portfolio.py) (the risk engine) and [`mandate.py`](mandate.py) (Lab 13
checker, now with candidate E). Run them with `python3 portfolio.py` and `python3 mandate.py`.

## R: the inputs

Course-authored training values, not market estimates.

| Sleeve | Expected return | Volatility | Reserve-eligible |
| --- | ---: | ---: | --- |
| Treasury bills | 3.5% | 0.5% | yes |
| Treasury 10-year note | 4.3% | 7.0% | yes |
| Investment-grade bond fund | 5.0% | 6.0% | no |
| Global equity index fund | 8.0% | 16.0% | no |

| Correlation | Bills | 10-year | IG bonds | Equity |
| --- | ---: | ---: | ---: | ---: |
| Bills | 1.00 | 0.10 | 0.05 | 0.00 |
| 10-year | 0.10 | 1.00 | 0.80 | −0.10 |
| IG bonds | 0.05 | 0.80 | 1.00 | 0.25 |
| Equity | 0.00 | −0.10 | 0.25 | 1.00 |

Objective: CPI + 4%, with CPI taken as 2.5% (a labelled estimate), so **6.5%**.

## I: the engine

`portfolio.py` uses only the standard library. The sleeves, correlation table, objective and
benchmark are editable constants at the top, and every result is computed from them. Each
calculation is its own function so Thursday's app can import it:

| Function | What it does |
| --- | --- |
| `validate_correlation` | refuses a table that is not 4 × 4, not symmetric, has a diagonal other than 1, or has any value outside −1 to 1 |
| `covariance_matrix` | covariance = correlation × volatility × volatility |
| `benchmark_weights`, `equal_weights`, `inverse_vol_weights` | the three baselines |
| `expected_return` | wᵀμ |
| `volatility` | √(wᵀΣw), summing every pair, so the correlation terms are included |
| `reserve_eligible_weight` | bills plus the 10-year note |

## V: proof on the known answer

| Portfolio | Weights: bills / 10-year / IG / equity | Return | Volatility | Reserve-eligible | Meets 6.5%? |
| --- | --- | ---: | ---: | ---: | --- |
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80 | 10.46 | 0.0 | yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20 | 5.21 | 50.0 | no |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77 | 1.05 | 90.3 | no |

Every value matches the lab's table.

**Prove it computes.** With the IG–equity correlation set to 0.50 in both cells, the benchmark's
volatility rose from 10.46 to **11.00**. I then set it back to 0.25.

**Break it.** With the IG–equity correlation set to 1.3, the engine refused:
`Refusing to run: Correlation [3][4] = 1.3 is outside -1 to 1`. Making only one cell different
(0.70 against 0.80) also refused: `Correlation table is not symmetric`. I then undid both changes.

**Read it: candidate E in the mandate checker.**

```
Candidate E
  Weights sum to 100                  100.0  pass
  Long-only (lowest weight)             0.0  pass
  Reserve-eligible >= 3.0%              0.0  FAIL
  Redeemable in 5 days >= 90%         100.0  pass
  Largest single company <= 8%          0.0  pass
  Calendar-year loss <= 10%                  requires CIO clarification
  Verdict: fails 1 rule(s)
```

The benchmark fails only the reserve rule (S3): it holds no cash or Treasuries at all.

## Diversification: learn on my own

1. **What it is.** Diversification means holding assets that do not move in lockstep, so that a
   loss in one is partly offset by the others.
2. **How it works.** Portfolio variance is not just the weighted variances. It adds a term for
   every pair: 2 × w₁ × w₂ × correlation × σ₁ × σ₂. When the correlation is below +1, that term is
   smaller than it would be for assets that move together, so the portfolio's volatility is below
   the weighted average of the sleeves' volatilities. At +1 there is no offset, and the portfolio's
   volatility is exactly the weighted average.
3. **The benchmark by hand.**

   | Term | Calculation | Value |
   | --- | --- | ---: |
   | IG variance | 0.40² × 6.0² = 0.16 × 36 | 5.76 |
   | Equity variance | 0.60² × 16.0² = 0.36 × 256 | 92.16 |
   | Correlation term | 2 × 0.40 × 0.60 × 0.25 × 6.0 × 16.0 | 11.52 |
   | Portfolio variance | 5.76 + 92.16 + 11.52 | 109.44 |
   | Portfolio volatility | √109.44 | **10.46%** |

   The weighted average of the two volatilities is 0.40 × 6 + 0.60 × 16 = 12.00%, so
   diversification saves about 1.5 points. Leaving out the correlation term gives √97.92 = 9.90%,
   the classic error the lab warns about.

## Reflect

1. **Why inverse volatility piles into bills.** Each weight is 1 ÷ volatility, and bills have a
   volatility of 0.5%, so their raw score is 1 ÷ 0.5 = 2.0. The next highest is IG bonds, at
   1 ÷ 6 ≈ 0.17. After scaling, bills take 84.3% of the portfolio. The rule looks only at each
   sleeve's own risk, ignoring return and correlation, so it buys the safest asset and its expected
   return falls to 3.77%, far below the 6.5% objective.
2. **Which baseline I would show the CIO first.** The **benchmark**, because it is the CIO's own
   yardstick (S4) and the only baseline that meets the return objective. It also exposes the
   conflict the CIO has to resolve: the mandate's own benchmark fails its reserve rule. Moving even
   3% from the bond fund into bills or the 10-year note would fix that, but how far equity can rise
   still depends on the unanswered loss question from Lab 13 (S9).
