"""Five-year pro-forma of Asbury Automotive Group (ABG) — Lab 09, the engine and the known answer.

Built from the Lab 09 instruction, standard library only: five projected years (2026-2030)
of income statement, balance sheet and cash flow from an opening balance sheet and a labelled
assumption set, computed in the order the instruction gives, with cash the last line. A check
block prints every year, assert_balanced refuses to value a sheet that does not balance, and
free cash flow to equity is discounted to one value per share.

Known answer (Lab 09, from Part 1 of the video): FY2026E revenue 18,323.0, operating income
844.2, net income 413.6, FCFE 211.4, cash 101.8; FY2030E revenue 19,678.3, operating income
971.4, net income 527.5, FCFE 342.3, cash 719.8; value per share $291.75; about 80% of value
after 2030.

USD millions unless stated. Learning demonstration, not investment advice.
Usage:  python3 proforma.py          # the ABG base case
        python3 proforma.py --break  # type 2026 cash at the opening 40.4; the model must refuse
"""
import sys

# ---------------------------------------------------------------------------
# Assumptions. Label: history / guidance / judgment / fact.
# ---------------------------------------------------------------------------
growth        = 0.018                                    # judgment — organic revenue growth a year
gross_margin  = 0.1705                                   # judgment
sga_ratio     = [0.665, 0.655, 0.645, 0.645, 0.645]      # judgment — SG&A ÷ gross profit, 2026 → 2030
dep_ratio     = 82.4 / 3070.4                            # history — FY2025 depreciation ÷ year-end PP&E
impairment    = 120.0                                    # judgment — non-cash, a year
capex         = 250.0                                    # guidance — a year
tax_rate      = 0.255                                    # judgment
inventory_days = 2135.8 / (17999.0 - 3071.7) * 365       # history — FY2025 inventory ÷ cost of sales × 365
floor_ratio   = 2027.0 / 2135.8                          # history — floor plan ÷ inventory, FY2025
other_wc      = 0.008                                    # judgment — other working capital, share of the change in revenue
min_cash      = 25.0                                     # history
revolver_limit = 850.0                                   # judgment
rate_revolver = 0.06                                     # judgment
repayment     = 150.0                                    # judgment — term debt repaid a year
buyback       = 150.0                                    # judgment — share buyback a year
rate_floor    = 0.0467                                   # history — interest on floor plan
rate_debt     = 0.0544                                   # history — interest on term debt
cost_of_equity  = 0.10                                   # judgment
terminal_growth = 0.025                                  # judgment
SHARES        = 17.951349                                # fact — 10-Q, 30 June 2026, millions

# Opening balance sheet, FY2025 (USD millions).
opening = dict(year=2025, revenue=17999.0, cash=40.4, inventory=2135.8, ppe=3070.4, other_assets=6371.6,
               floor_plan=2027.0, debt=3572.0, revolver=0.0, other_liabilities=2127.5, equity=3891.7)


def project_year(prev, i):
    """One projected year, in the order the instruction gives; cash is computed last."""
    y = {'year': prev['year'] + 1}
    # income statement
    y['revenue']      = prev['revenue'] * (1 + growth)
    y['gross_profit'] = y['revenue'] * gross_margin
    y['sga']          = y['gross_profit'] * sga_ratio[i]
    y['depreciation'] = prev['ppe'] * dep_ratio
    y['impairment']   = impairment
    y['operating_income'] = y['gross_profit'] - y['sga'] - y['depreciation'] - y['impairment']
    y['interest'] = prev['floor_plan'] * rate_floor + prev['debt'] * rate_debt + prev['revolver'] * rate_revolver
    y['pretax']   = y['operating_income'] - y['interest']
    y['tax']      = max(0.0, y['pretax']) * tax_rate
    y['net_income'] = y['pretax'] - y['tax']
    # balance sheet, everything except cash
    delta_revenue      = y['revenue'] - prev['revenue']
    y['inventory']     = (y['revenue'] - y['gross_profit']) * inventory_days / 365
    y['floor_plan']    = y['inventory'] * floor_ratio
    y['capex']         = capex
    y['ppe']           = prev['ppe'] + y['capex'] - y['depreciation']
    y['delta_other_wc'] = other_wc * delta_revenue
    y['other_assets']  = prev['other_assets'] + y['delta_other_wc'] - y['impairment']
    y['repayment']     = repayment
    y['debt']          = prev['debt'] - y['repayment']
    y['other_liabilities'] = prev['other_liabilities']
    y['buyback']       = buyback
    y['equity']        = prev['equity'] + y['net_income'] - y['buyback']
    # free cash flow to equity, then cash as the RESULT
    y['delta_inventory']  = y['inventory'] - prev['inventory']
    y['delta_floor_plan'] = y['floor_plan'] - prev['floor_plan']
    y['fcfe'] = (y['net_income'] + y['depreciation'] + y['impairment'] - y['capex']
                 - y['delta_inventory'] - y['delta_other_wc'] + y['delta_floor_plan'] - y['repayment'])
    cash_before = prev['cash'] + y['fcfe'] - y['buyback']
    y['draw']  = min(max(0.0, min_cash - cash_before), max(0.0, revolver_limit - prev['revolver']))
    y['repay'] = min(prev['revolver'], max(0.0, cash_before - min_cash))
    y['revolver'] = prev['revolver'] + y['draw'] - y['repay']
    y['cash']  = cash_before + y['draw'] - y['repay']
    y['total_assets'] = y['cash'] + y['inventory'] + y['ppe'] + y['other_assets']
    y['total_liabilities_equity'] = (y['floor_plan'] + y['debt'] + y['revolver']
                                     + y['other_liabilities'] + y['equity'])
    # checks, computed every year and printed below
    y['check_balance'] = y['total_assets'] - y['total_liabilities_equity']
    y['check_floor']   = min(0.0, y['cash'] - min_cash)
    return y


def assert_balanced(years, tol=0.05):
    """Refuse to go on if a sheet does not balance or cash breaks the floor; name the year and the gap."""
    for y in years:
        gap = y['total_assets'] - y['total_liabilities_equity']
        if abs(gap) > tol:
            raise ValueError(f"FY{y['year']}E does not balance: assets − liabilities − equity = {gap:,.1f}")
        if y['cash'] < min_cash - tol:
            raise ValueError(f"FY{y['year']}E cash {y['cash']:,.1f} is below the {min_cash:,.0f} minimum")
    return f'balanced, {len(years)} year(s)'


def value(years):
    """PV of the five FCFE at the cost of equity plus a terminal value; only after the checks pass."""
    print(assert_balanced(years))
    r, g = cost_of_equity, terminal_growth
    if g >= r:
        raise ValueError(f"terminal growth {g:.1%} must be below the cost of equity {r:.1%}")
    factors = [1 / (1 + r) ** n for n in range(1, len(years) + 1)]
    pv_explicit = sum(y['fcfe'] * f for y, f in zip(years, factors))
    terminal_value = (years[-1]['fcfe'] + years[-1]['repayment']) * (1 + g) / (r - g)
    pv_terminal = terminal_value * factors[-1]
    equity_value = pv_explicit + pv_terminal
    return dict(pv_explicit=pv_explicit, terminal_value=terminal_value, pv_terminal=pv_terminal,
                equity_value=equity_value, terminal_share=pv_terminal / equity_value,
                per_share=equity_value / SHARES)


def project(n=5):
    years, prev = [], opening
    for i in range(n):
        prev = project_year(prev, i)
        years.append(prev)
    return years


def row(label, years, key):
    print(f"{label:<34}" + ''.join(f"{(y[key] if abs(y[key]) >= 0.05 else 0.0):>11,.1f}" for y in years))


def main():
    years = project()
    print(f"{'':<34}" + ''.join(f"{'FY' + str(y['year']) + 'E':>11}" for y in years))
    print("-- income statement")
    for label, key in [('Revenue', 'revenue'), ('Gross profit', 'gross_profit'), ('SG&A', 'sga'),
                       ('Depreciation', 'depreciation'), ('Impairment', 'impairment'),
                       ('Operating income', 'operating_income'), ('Interest', 'interest'),
                       ('Pretax income', 'pretax'), ('Tax', 'tax'), ('Net income', 'net_income')]:
        row(label, years, key)
    print("-- balance sheet")
    for label, key in [('Cash (the result)', 'cash'), ('Inventory', 'inventory'), ('PP&E', 'ppe'),
                       ('Other assets', 'other_assets'), ('Total assets', 'total_assets'),
                       ('Floor plan', 'floor_plan'), ('Term debt', 'debt'), ('Revolver', 'revolver'),
                       ('Other liabilities', 'other_liabilities'), ('Equity', 'equity'),
                       ('Total liabilities & equity', 'total_liabilities_equity')]:
        row(label, years, key)
    print("-- cash flow to equity")
    for label, key in [('Net income', 'net_income'), ('+ Depreciation', 'depreciation'),
                       ('+ Impairment', 'impairment'), ('− Capital spending', 'capex'),
                       ('− Change in inventory', 'delta_inventory'), ('− Change in other WC', 'delta_other_wc'),
                       ('+ Change in floor plan', 'delta_floor_plan'), ('− Debt repayment', 'repayment'),
                       ('Free cash flow to equity', 'fcfe'), ('− Buyback', 'buyback')]:
        row(label, years, key)
    print("-- checks (must read 0.0 in every year)")
    row('Assets − liabilities − equity', years, 'check_balance')
    row(f'Cash at or above the {min_cash:,.0f} minimum', years, 'check_floor')

    v = value(years)
    print(f"Equity value:                     {v['equity_value']:>12,.1f}")
    print(f"Share of value after FY{years[-1]['year']}:      {v['terminal_share']:>11.1%}")
    print(f"Shares (millions):                {SHARES:>12,.6f}")
    print(f"Value per share:                  ${v['per_share']:>11,.2f}")


def demo_break():
    """Swap and break: 2026 cash typed at the opening 40.4 instead of computed. The model must refuse."""
    years = project(1)
    broken = dict(years[0])
    broken['cash'] = opening['cash']
    broken['total_assets'] = broken['cash'] + broken['inventory'] + broken['ppe'] + broken['other_assets']
    try:
        assert_balanced([broken])
        print("the check did not fire — that is the bug")
    except ValueError as e:
        print(f"Model refused: {e}")
        print(f"(the year's change in cash with the sign flipped: {opening['cash'] - years[0]['cash']:,.1f})")


if __name__ == '__main__':
    demo_break() if '--break' in sys.argv else main()
