"""Pro-forma valuation of NVIDIA Corporation (NVDA) — Lab 10, your company through it.

Five projected fiscal years (FY2027E-FY2031E; NVIDIA's FY2027 ends in late
January 2027) of income statement, balance sheet and cash flow that tie to
each other, a check block that refuses to let an unbalanced sheet be valued,
and free cash flow to equity discounted to one value per share.
Standard library only. The engine follows the course tutorial's three-statement
structure and was checked against its published known answer before the
NVIDIA opening balance sheet, assumptions and company-specific lines went in. Sources and reasons: nvda-proforma.md.

The lines that make NVIDIA different from the course tutorial's dealer template:
  * no floor plan and almost no debt: a $27bn-a-year working-capital build
    (receivables + inventory) is funded from the company's own cash;
  * stock-based compensation (SBC) is the recurring non-cash charge: inside
    operating expenses, added back in cash flow, credited to equity, and paid
    for through buybacks;
  * a large investment portfolio (cash + marketable securities) that earns
    interest income; equity-stake gains ($9.0bn in FY2026) are NOT projected;
  * depreciation sits inside cost of revenue and operating expenses (not a
    separate line), so it appears only in the cash-flow add-back and the
    PP&E roll-forward; the bond ladder repays on its filed maturity dates.

USD millions unless stated. Learning demonstration, not investment advice.
Usage:  python3 nvda_proforma.py          # base case
        python3 nvda_proforma.py --break  # type cash instead of linking it; the model must refuse
"""
import sys

# ---------------------------------------------------------------------------
# Operating assumptions. Label: history / guidance / judgment.  Reasons: nvda-proforma.md.
# ---------------------------------------------------------------------------
growth       = [0.856, 0.25, 0.12, 0.07, 0.04]        # FY27 guidance+judgment: H1 actual 177,837 + Q3 outlook 108,000 + Q4 judgment 115,000 = 400,837 = +85.6%; then judgment — deceleration
gross_margin = [0.745, 0.730, 0.720, 0.710, 0.700]    # judgment — H1 FY27 75.0%, Q3 outlook 74.0%; then drift toward FY2024's 72.7% and below
opex_ratio   = [0.087, 0.095, 0.105, 0.115, 0.125]    # judgment — R&D + SG&A (incl. SBC) ÷ revenue: 8.7% at FY27 run-rate, rising back toward FY2025's 12.6% as growth slows
da_ratio     = 2843.0 / (6283.0 + 807.0)              # history — FY2026 D&A ÷ opening PP&E + intangibles = 40.1%
sbc_ratio    = 0.025                                  # judgment — SBC ÷ revenue: FY26 3.0%, H1 FY27 2.2%
capex_ratio  = 6042.0 / 215938.0                      # history — FY2026 purchases of PP&E and intangibles ÷ revenue = 2.8%; MD&A: capex rises in FY27
tax_rate     = 0.17                                   # guidance — FY2027 GAAP tax rate 16%-18% (Q2 FY27 release); midpoint carried five years by judgment
other_income = 0.0                                    # judgment — equity-stake gains (9,022 in FY26; 23,707 in H1 FY27) are not forecast

# Balance-sheet and financing assumptions.
ar_days        = 38466.0 / 215938.0 * 365             # history — FY2026 receivables ÷ revenue × 365 = 65.0 days
inventory_days = 21403.0 / 62475.0 * 365              # history — FY2026 inventory ÷ cost of revenue × 365 = 125.0 days
ap_days        = 9812.0 / 62475.0 * 365               # history — FY2026 payables ÷ cost of revenue × 365 = 57.3 days
accrued_ratio  = 21352.0 / 215938.0                   # history — FY2026 accrued and other current liabilities ÷ revenue = 9.9%
min_cash       = 8000.0                               # history — lowest year-end cash of the three years was 7,280 (FY2024)
debt_paydown   = [1000.0, 0.0, 1250.0, 0.0, 1500.0]   # history — Note 11 maturity ladder: notes due 2026, 2028, 2030 fall in FY27, FY29, FY31
payout         = 0.95                                 # judgment — buybacks + net share settlement + dividends = 95% of each year's FCFE, so cash does not pile up; FY26 actual 49.0bn on 109.6bn (45%), H1 FY27 ~48bn on ~74bn (65%)
revolver_limit = 25000.0                              # history — commercial paper program enlarged to $25.0bn in Jan 2026 (Note 11); backstop only
rate_cash, rate_debt, rate_revolver = 0.035, 259.0 / 8463.0, 0.045   # judgment 3.5% on cash+securities (FY26 ÷ opening 5.3%, H1 FY27 ~3.3%); history 3.06% on notes; judgment on CP

# Valuation assumptions.
cost_of_equity  = 0.12      # judgment — above the tutorial's 10%: beta.py measures 2.21 raw / 1.81 adjusted; a CAPM at ~4% + 1.81 × 5% gives ~13%; Week 6 tests it
terminal_growth = 0.03      # judgment — long-run nominal growth, below the cost of equity
SHARES          = 24100.0   # fact — 10-Q cover, shares outstanding at 21 Aug 2026, millions (filed to the nearest 0.1bn)

# Opening balance sheet: FY2026 (25 Jan 2026) as filed in the 10-K, pp. 53.
opening = dict(year=2026, revenue=215938.0, cash=10605.0, securities=51951.0, receivables=38466.0,
               inventory=21403.0, ppe=10383.0 + 3306.0,                       # PP&E + intangibles
               other_assets=206803.0 - 10605.0 - 51951.0 - 38466.0 - 21403.0 - (10383.0 + 3306.0),
               payables=9812.0, accrued=21352.0, debt=999.0 + 7469.0, revolver=0.0,
               other_liabilities=49510.0 - 9812.0 - 21352.0 - (999.0 + 7469.0),
               equity=157293.0)


def project_year(prev, i):
    """One projected fiscal year from the prior year's balance sheet and the assumptions above."""
    y = {'year': prev['year'] + 1}
    # income statement (D&A and SBC sit inside gross profit and opex, as NVIDIA reports them)
    y['revenue']      = prev['revenue'] * (1 + growth[i])
    y['gross_profit'] = y['revenue'] * gross_margin[i]
    cost_of_revenue   = y['revenue'] - y['gross_profit']
    y['opex']         = y['revenue'] * opex_ratio[i]
    y['operating_income'] = y['gross_profit'] - y['opex']
    y['interest_income']  = (prev['cash'] + prev['securities']) * rate_cash
    y['interest_expense'] = prev['debt'] * rate_debt + prev['revolver'] * rate_revolver
    y['other_income'] = other_income
    y['pretax']       = y['operating_income'] + y['interest_income'] - y['interest_expense'] + y['other_income']
    y['tax']          = max(0.0, y['pretax']) * tax_rate
    y['net_income']   = y['pretax'] - y['tax']
    # non-cash charges and investment, from the assumptions
    y['da']    = prev['ppe'] * da_ratio
    y['sbc']   = y['revenue'] * sbc_ratio
    y['capex'] = y['revenue'] * capex_ratio
    # balance sheet, everything except cash
    y['receivables'] = y['revenue'] * ar_days / 365
    y['inventory']   = cost_of_revenue * inventory_days / 365
    y['securities']  = prev['securities']                       # held flat; surplus lands in cash
    y['ppe']         = prev['ppe'] + y['capex'] - y['da']
    y['other_assets'] = prev['other_assets']
    y['payables']    = cost_of_revenue * ap_days / 365
    y['accrued']     = y['revenue'] * accrued_ratio
    y['paydown']     = min(debt_paydown[i], prev['debt'])
    y['debt']        = prev['debt'] - y['paydown']
    y['other_liabilities'] = prev['other_liabilities']
    # cash flow to equity, the distribution it funds, then cash as the RESULT
    delta_wc = ((y['receivables'] - prev['receivables']) + (y['inventory'] - prev['inventory'])
                - (y['payables'] - prev['payables']) - (y['accrued'] - prev['accrued']))
    y['delta_wc'] = delta_wc
    y['fcfe'] = y['net_income'] + y['da'] + y['sbc'] - y['capex'] - delta_wc - y['paydown']
    y['buyback']     = max(0.0, y['fcfe']) * payout                    # a distribution, not part of what we value
    y['equity']      = prev['equity'] + y['net_income'] + y['sbc'] - y['buyback']   # SBC is credited to paid-in capital
    cash_before = prev['cash'] + y['fcfe'] - y['buyback']
    y['draw']  = min(max(0.0, min_cash - cash_before), max(0.0, revolver_limit - prev['revolver']))
    y['repay'] = min(prev['revolver'], max(0.0, cash_before - min_cash))
    y['revolver'] = prev['revolver'] + y['draw'] - y['repay']
    y['cash']  = cash_before + y['draw'] - y['repay']
    y['total_assets'] = (y['cash'] + y['securities'] + y['receivables'] + y['inventory']
                         + y['ppe'] + y['other_assets'])
    y['total_liabilities_equity'] = (y['payables'] + y['accrued'] + y['debt'] + y['revolver']
                                     + y['other_liabilities'] + y['equity'])
    # checks, computed every year and printed below
    y['check_balance'] = y['total_assets'] - y['total_liabilities_equity']
    y['check_cash']    = y['cash'] - (prev['cash'] + y['fcfe'] - y['buyback'] + y['draw'] - y['repay'])
    y['check_ppe']     = y['ppe'] - (prev['ppe'] + y['capex'] - y['da'])
    y['check_debt']    = y['debt'] - (prev['debt'] - y['paydown'])
    y['check_floor']   = min(0.0, y['cash'] - min_cash)
    return y


def assert_balanced(years, tol=0.5):
    """The rule, enforced: refuse to go on if a sheet does not balance or cash breaks the floor."""
    for y in years:
        gap = y['total_assets'] - y['total_liabilities_equity']
        if abs(gap) > tol:
            raise ValueError(f"FY{y['year']}E does not balance: assets − liabilities − equity = {gap:,.1f}")
        if y['cash'] < min_cash - tol:
            raise ValueError(f"FY{y['year']}E cash {y['cash']:,.1f} is below the {min_cash:,.0f} floor")
    return f'balanced, {len(years)} year(s)'


def value(years):
    """FCFE discounted at the cost of equity, plus a terminal value; only after the checks pass."""
    print(assert_balanced(years))
    r, g = cost_of_equity, terminal_growth
    if g >= r:
        raise ValueError(f"terminal growth {g:.1%} must be below the cost of equity {r:.1%}")
    factors = [1 / (1 + r) ** n for n in range(1, len(years) + 1)]
    pv_explicit = sum(y['fcfe'] * f for y, f in zip(years, factors))
    terminal_cash_flow = (years[-1]['fcfe'] + years[-1]['paydown']) * (1 + g)  # repayments end; owners keep it
    terminal_value = terminal_cash_flow / (r - g)
    pv_terminal = terminal_value * factors[-1]
    equity_value = pv_explicit + pv_terminal
    return dict(pv_explicit=pv_explicit, terminal_cash_flow=terminal_cash_flow, terminal_value=terminal_value,
                pv_terminal=pv_terminal, equity_value=equity_value,
                terminal_share=pv_terminal / equity_value, per_share=equity_value / SHARES)


def project(n=5):
    years, prev = [], opening
    for i in range(n):
        prev = project_year(prev, i)
        years.append(prev)
    return years


def row(label, years, key, fmt='{:>11,.1f}'):
    print(f"{label:<38}" + ''.join(fmt.format(y[key] if abs(y[key]) >= 0.05 else 0.0) for y in years))


def main():
    years = project()
    print(f"{'':<38}" + ''.join(f"{'FY' + str(y['year']) + 'E':>11}" for y in years))
    print("-- income statement")
    for label, key in [('Revenue', 'revenue'), ('Gross profit', 'gross_profit'),
                       ('Operating expenses (R&D + SG&A)', 'opex'), ('Operating income', 'operating_income'),
                       ('Interest income', 'interest_income'), ('Interest expense', 'interest_expense'),
                       ('Pretax income', 'pretax'), ('Tax', 'tax'), ('Net income', 'net_income')]:
        row(label, years, key)
    print("-- balance sheet")
    for label, key in [('Cash (the result)', 'cash'), ('Marketable securities', 'securities'),
                       ('Accounts receivable', 'receivables'), ('Inventory', 'inventory'),
                       ('PP&E and intangibles', 'ppe'), ('Other assets', 'other_assets'),
                       ('Total assets', 'total_assets'), ('Accounts payable', 'payables'),
                       ('Accrued and other current', 'accrued'), ('Notes (term debt)', 'debt'),
                       ('Commercial paper (revolver)', 'revolver'), ('Other liabilities', 'other_liabilities'),
                       ('Equity', 'equity'), ('Total liabilities & equity', 'total_liabilities_equity')]:
        row(label, years, key)
    print("-- cash flow to equity")
    for label, key in [('Net income', 'net_income'), ('+ Depreciation & amortization', 'da'),
                       ('+ Stock-based compensation', 'sbc'), ('− Capital spending', 'capex'),
                       ('− Working-capital build', 'delta_wc'), ('− Notes repaid', 'paydown'),
                       ('Free cash flow to equity', 'fcfe'), ('− Buybacks and dividends', 'buyback')]:
        row(label, years, key)
    print("-- checks (must read 0.0 in every year)")
    for label, key in [('Assets − liabilities − equity', 'check_balance'),
                       ('Cash: balance sheet vs cash flow', 'check_cash'),
                       ('PP&E roll-forward', 'check_ppe'), ('Debt roll-forward', 'check_debt'),
                       (f'Cash at or above the {min_cash:,.0f} floor', 'check_floor')]:
        row(label, years, key)

    v = value(years)
    print(f"PV of FY{years[0]['year']}-FY{years[-1]['year']} FCFE:        {v['pv_explicit']:>14,.1f}")
    print(f"Cash flow in FY{years[-1]['year'] + 1}:                  {v['terminal_cash_flow']:>14,.1f}")
    print(f"Terminal value at FY{years[-1]['year']}:             {v['terminal_value']:>14,.1f}")
    print(f"PV of terminal value:                  {v['pv_terminal']:>14,.1f}")
    print(f"Equity value:                          {v['equity_value']:>14,.1f}")
    print(f"Share of value after FY{years[-1]['year']}:          {v['terminal_share']:>13.1%}")
    print(f"Shares (millions):                     {SHARES:>14,.0f}")
    print(f"Value per share:                       ${v['per_share']:>13,.2f}")


def demo_break():
    """Break 1 from the tutorial: cash typed at the opening value instead of linked. The model must refuse."""
    years = project(1)
    broken = dict(years[0])
    broken['cash'] = opening['cash']
    broken['total_assets'] = (broken['cash'] + broken['securities'] + broken['receivables']
                              + broken['inventory'] + broken['ppe'] + broken['other_assets'])
    try:
        assert_balanced([broken])
        print("the check did not fire — that is the bug")
    except ValueError as e:
        print(f"Model refused: {e}")
        print(f"(the gap is the year's change in cash with the sign flipped: {opening['cash'] - years[0]['cash']:,.1f})")


if __name__ == '__main__':
    demo_break() if '--break' in sys.argv else main()
