"""Project 1 valuation engine for NVIDIA (NVDA) — the layer between the Lab 10 pro-forma and the product.

Standard library only. The three-statement engine is `nvda_proforma.py` (Lab 10), used
unchanged: this module sets its labelled assumptions, runs it, restores the base, and reads the
projected years back. On top of that it adds what Project 1 requires:

  * the exposed driver panel (DRIVERS): every load-bearing assumption with value, basis,
    bounds, the reason for the bounds, the challenge it faces and the evidence that would move it;
  * free cash flow to the firm (FCFF) from the pro-forma, WACC, a Gordon terminal value and the
    enterprise-to-equity bridge to one value per diluted share;
  * the checks (articulation, bridge, monotonicity, boundaries, historical bands) that can fail loudly;
  * one-at-a-time sensitivities, a WACC x growth grid, causal low/base/high cases, a reverse DCF
    and the comparable-company multiples under a policy frozen before the numbers.

USD millions unless stated. Learning demonstration, not investment advice.
"""
import copy
import math

import nvda_proforma as pf

# ---------------------------------------------------------------------------
# Provenance: the facts the valuation stands on. Every number carries its locator.
# ---------------------------------------------------------------------------
TARGET = dict(company='NVIDIA Corporation', ticker='NVDA', exchange='NASDAQ', cik='0001045810',
              currency='USD', units='USD millions; per-share values in USD',
              fiscal_year_note='Fiscal year ends the last Sunday in January; FY2026 ended 25 Jan 2026. '
                               'FY2027 has a 14-week fourth quarter (Q2 FY2027 10-Q, Note 1).')

MARKET = dict(price=225.51, price_date='2026-09-23',
              price_source='Nasdaq historical close, cached in src/beta_prices/NVDA_2021-09-24_2026-09-24_nasdaq_historical_raw.json',
              rf=0.05, erp=0.0442,
              rf_source='course convention: 10-year Treasury 5.00%, implied equity risk premium 4.42% (July 2026), Week 5 tutorial')

# Opening balance sheet = FY2026 10-K, p. 53 (accession 0001045810-26-000021, filed 2026-02-25).
# The pro-forma's five years start from it, so the bridge that is CONSISTENT with the cash flows
# is the one at the same date: every FY2027E cash flow is still ahead of it.
BRIDGE_FY2026 = dict(
    as_of='2026-01-25', label='FY2026 10-K balance sheet (consistent with the pro-forma opening date)',
    source='Form 10-K FY2026, accession 0001045810-26-000021, balance sheet p. 53; Q2 FY2027 10-Q comparative column',
    cash=10605.0, marketable_debt=39065.0, marketable_equity=12886.0,
    debt=999.0 + 7469.0, debt_note='short-term 999 + long-term 7,469; Note 11 pp. 69-70',
    cost_of_debt=0.0292, cost_of_debt_note='principal-weighted effective rate of the seven note series outstanding at 25 Jan 2026 (Q2 FY2027 10-Q Note 9): 2.92%',
    non_marketable_equity=22251.0, operating_leases=0.0,
)
# Latest filed balance sheet before the valuation date. Shown for reference: using it with full
# FY2027E cash flows would double count the first half of FY2027 (already inside its cash line).
BRIDGE_Q2FY2027 = dict(
    as_of='2026-07-26', label='Q2 FY2027 10-Q balance sheet (latest filed; reference only, timing inconsistent)',
    source='Form 10-Q for the quarter ended 26 Jul 2026, accession 0001045810-26-000075, filed 2026-08-26, balance sheet p. 4',
    cash=22443.0, marketable_debt=34143.0, marketable_equity=42783.0,
    debt=1000.0 + 32366.0, debt_note='short-term 1,000 + long-term 32,366 carrying; $33.5bn principal of senior notes',
    cost_of_debt=0.0441, cost_of_debt_note='principal-weighted effective rate of the fourteen note series outstanding at 26 Jul 2026 (10-Q Note 9): 4.41%',
    non_marketable_equity=51157.0, operating_leases=509.0 + 4985.0,
)

SHARES = dict(outstanding=24100.0, outstanding_source='10-Q cover, shares outstanding at 21 Aug 2026 (accession 0001045810-26-000075), to the nearest 0.1bn',
              basic_wavg_q2=24190.0, diluted_wavg_q2=24285.0,
              wavg_source='Q2 FY2027 10-Q, Note 4 (net income per share), quarter ended 26 Jul 2026',
              # Point-in-time diluted count: outstanding plus the quarter's dilutive increment (RSUs, ESPP).
              diluted=24100.0 + (24285.0 - 24190.0))

HISTORY_BANDS = dict(   # from the R.2 ratio table in nvda-proforma.md (FY2024-FY2026 10-Ks) plus FY2023
    gross_margin=(0.569, 0.785, 'FY2023 56.9% trough (FY2024 10-K) to 78.5%, 3.5 points above the best quarter reported (75.0%, Q2 FY2027)'),
    opex_ratio=(0.065, 0.186, 'the FY2027E run-rate 8.7% less 2 points (NVIDIA has never filed a year below 10.7%) to FY2024 18.6%'),
    tax_rate=(0.12, 0.21, 'FY2024 12.0% to the 21% statutory rate'),
    capex_ratio=(0.015, 0.06, 'FY2024 1.8%; MD&A says capex rises in FY2027'),
    sbc_ratio=(0.015, 0.06, 'H1 FY2027 2.2% to FY2024 5.8%'),
)

# ---------------------------------------------------------------------------
# The exposed driver panel. Locked: the engine, the provenance, the checks. Exposed: these.
# ---------------------------------------------------------------------------
DRIVERS = [
    dict(key='growth_shift', label='Revenue growth FY2028E-FY2031E, shift (pp)', unit='percentage points added to each year',
         base=0.0, lo=-0.25, hi=0.25, step=0.01, fmt='pp',
         value_note='base path 25 / 12 / 7 / 4 %', basis='judgment',
         bound_reason='-25 pp makes FY2028E flat (0%) and the later years shrink: the "AI capex stops" case. '
                      '+25 pp is one point above the growth the market price implies (reverse DCF); nothing in the filings supports more.',
         challenge='Two customers are 36% of revenue (FY2026 10-K MD&A p. 41); hyperscaler capex cannot compound at 65-85% for long.',
         evidence='Data Center revenue growth in the next two quarterly reports; hyperscaler capex guidance.'),
    dict(key='fy27_revenue_pct', label='FY2027E revenue vs base (Q4 judgment), %', unit='percent of base FY2027E revenue 400,837',
         base=0.0, lo=-0.10, hi=0.10, step=0.01, fmt='pct',
         value_note='H1 actual 177,837 + Q3 outlook 108,000 + Q4 judgment 115,000', basis='guidance + judgment',
         bound_reason='Q3 is guided within +/-2%; only Q4 (14 weeks) is judgment, so +/-10% of the year is the widest a miss or beat could plausibly reach.',
         challenge='Q4 FY2027 has no guidance yet; export controls on China Data Center compute remain in the outlook.',
         evidence='Q3 FY2027 results and the Q4 outlook (expected November 2026).'),
    dict(key='gross_margin_shift', label='Gross margin, shift (pp, all years)', unit='percentage points',
         base=0.0, lo=-0.13, hi=0.04, step=0.005, fmt='pp',
         value_note='base path 74.5 -> 70.0 %', basis='judgment',
         bound_reason='-13 pp takes FY2031E to 57.0%, FY2023\'s 56.9% trough (the last cycle low, FY2024 10-K); +4 pp caps the first year at 78.5%, above any quarter NVIDIA has reported.',
         challenge='Custom silicon (Broadcom-built accelerators) and AMD compete for the same racks; CUDA lock-in is a judgment, not a filing claim.',
         evidence='Gross-margin guidance below 72% and falling; Data Center pricing disclosures.'),
    dict(key='opex_shift', label='Operating expenses / revenue, shift (pp, all years)', unit='percentage points',
         base=0.0, lo=-0.02, hi=0.06, step=0.005, fmt='pp',
         value_note='base path 8.7 -> 12.5 %', basis='judgment',
         bound_reason='-2 pp is below the H1 FY2027 run-rate of 9.0%; +6 pp returns FY2031E to FY2024\'s 18.6%.',
         challenge='Opex grew 41% in FY2026 (compensation, compute, infrastructure); the one-year product cadence keeps R&D rising.',
         evidence='Opex growing faster than revenue for two consecutive quarters.'),
    dict(key='tax_rate', label='Tax rate (all years)', unit='fraction',
         base=0.17, lo=0.12, hi=0.21, step=0.005, fmt='pct',
         value_note='Q2 FY2027 release: FY2027 GAAP rate 16-18%', basis='guidance',
         bound_reason='FY2024 was 12.0%; 21% is the statutory rate with no FDDEI, SBC or R&D benefit.',
         challenge='FDDEI and SBC benefits shrink as the mix changes; the rate rose each of the last three years.',
         evidence='Effective rate in the next 10-K; tax-law changes.'),
    dict(key='capex_ratio', label='Capital spending / revenue', unit='fraction',
         base=6042.0 / 215938.0, lo=0.015, hi=0.06, step=0.0025, fmt='pct',
         value_note='FY2026 2.8%', basis='history',
         bound_reason='FY2024 1.8% is the low; 6% is double the FY2026 ratio, the most a fabless company has needed.',
         challenge='MD&A says capex will increase in FY2027; a ratio on 86% revenue growth already delivers 11.2bn.',
         evidence='Purchases of property and equipment in the cash flow statement; any move to own fabs.'),
    dict(key='sbc_ratio', label='Stock-based compensation / revenue', unit='fraction',
         base=0.025, lo=0.015, hi=0.06, step=0.0025, fmt='pct',
         value_note='FY2026 3.0%, H1 FY2027 2.2%', basis='judgment',
         bound_reason='H1 FY2027 2.2% is the low; FY2024 5.8% is the high of the three filed years.',
         challenge='SBC is added back as non-cash; treat it as a cash cost (toggle) and value falls.',
         evidence='SBC line in the cash flow statement; share count after buybacks.'),
    dict(key='cost_of_equity', label='Cost of equity', unit='fraction',
         base=0.12, lo=0.09, hi=0.16, step=0.0025, fmt='pct',
         value_note='judgment between the tutorial 10% and the measured CAPM 13-14.8%', basis='judgment',
         bound_reason='9% is a beta of about 0.9 (below the market); 16% is the observed beta 2.21 plus one standard error (2.5) at rf 5% + ERP 4.42%.',
         challenge='beta.py measures 2.21 raw (s.e. 0.30), 1.81 Blume; CAPM gives 13.0-14.8%, so 12% is the generous end.',
         evidence='Re-estimated beta each quarter; the ten-year Treasury yield.'),
    dict(key='terminal_growth', label='Terminal growth after FY2031E', unit='fraction',
         base=0.03, lo=0.0, hi=0.04, step=0.0025, fmt='pct',
         value_note='long-run nominal growth', basis='judgment',
         bound_reason='0% is a flat industry after the build-out; 4% is about nominal GDP, the most a going concern can hold forever.',
         challenge='In FY2031E the model reinvests 2.5% of net income and grows 3% forever, a 118% return on retained cash.',
         evidence='Terminal growth must stay below the discount rate; the check refuses otherwise.'),
]
TOGGLES = [
    dict(key='sbc_as_cash_cost', label='Treat stock-based compensation as a cash cost (no add-back)', base=False,
         reason='The honest alternative: SBC is a real cost to owners through dilution.'),
    dict(key='include_marketable_equity', label='Add marketable equity securities to the bridge', base=True,
         reason='Publicly held equity stakes at fair value (10-Q Note 7); liquid but strategic, so switchable.'),
    dict(key='bridge_latest', label='Use the Q2 FY2027 balance sheet for the bridge (reference only)', base=False,
         reason='Timing-inconsistent with full FY2027E cash flows; shown so the newer debt and cash are visible.'),
]
STRESS_RANGES = dict(   # unlocked only in the app's stress mode; anything outside the defended bounds is flagged red
    growth_shift=(-0.60, 0.60), fy27_revenue_pct=(-0.30, 0.30), gross_margin_shift=(-0.40, 0.10), opex_shift=(-0.08, 0.20),
    tax_rate=(0.0, 0.35), capex_ratio=(0.0, 0.15), sbc_ratio=(0.0, 0.12), cost_of_equity=(0.04, 0.25), terminal_growth=(-0.02, 0.12))
DRIVER_KEYS = [d['key'] for d in DRIVERS]
BASE_INPUTS = {d['key']: d['base'] for d in DRIVERS} | {t['key']: t['base'] for t in TOGGLES}

PF_KEYS = ['growth', 'gross_margin', 'opex_ratio', 'sbc_ratio', 'capex_ratio', 'tax_rate',
           'cost_of_equity', 'terminal_growth']
PF_BASE = {k: copy.deepcopy(getattr(pf, k)) for k in PF_KEYS}


def clamp_report(inputs, allow_out_of_bounds=False):
    """Return the inputs with every driver inside its bounds (unless stress mode allows it) and the offenders."""
    out, offenders = dict(inputs), []
    for d in DRIVERS:
        v = out.get(d['key'], d['base'])
        if v < d['lo'] - 1e-12 or v > d['hi'] + 1e-12:
            offenders.append(f"{d['label']}: {v:g} outside the defended bounds [{d['lo']:g}, {d['hi']:g}]")
            if not allow_out_of_bounds:
                out[d['key']] = min(max(v, d['lo']), d['hi'])
    return out, offenders


def proforma_assumptions(inputs):
    """Translate the driver panel into the Lab 10 module's labelled assumptions."""
    a = copy.deepcopy(PF_BASE)
    a['growth'] = [a['growth'][0]] + [g + inputs['growth_shift'] for g in a['growth'][1:]]
    a['growth'][0] = (1 + a['growth'][0]) * (1 + inputs['fy27_revenue_pct']) - 1
    a['gross_margin'] = [m + inputs['gross_margin_shift'] for m in a['gross_margin']]
    a['opex_ratio'] = [o + inputs['opex_shift'] for o in a['opex_ratio']]
    for k in ('tax_rate', 'capex_ratio', 'sbc_ratio', 'cost_of_equity', 'terminal_growth'):
        a[k] = inputs[k]
    return a


def run_proforma(inputs):
    """Set the Lab 10 assumptions, project five years, always restore the base. Never raises on a bad sheet."""
    a = proforma_assumptions(inputs)
    for k, v in a.items():
        setattr(pf, k, copy.deepcopy(v))
    try:
        years = pf.project()
    finally:
        for k in PF_KEYS:
            setattr(pf, k, copy.deepcopy(PF_BASE[k]))
    return years, a


def fcfe_value(years, a):
    """The Lab 10 FCFE valuation (cross-check), computed without printing and without raising."""
    r, g = a['cost_of_equity'], a['terminal_growth']
    if g >= r:
        return None
    factors = [1 / (1 + r) ** n for n in range(1, len(years) + 1)]
    pv = sum(y['fcfe'] * f for y, f in zip(years, factors))
    tv = (years[-1]['fcfe'] + years[-1]['paydown']) * (1 + g) / (r - g)
    equity = pv + tv * factors[-1]
    return dict(equity_value=equity, per_share=equity / pf.SHARES, terminal_share=tv * factors[-1] / equity)


# ---------------------------------------------------------------------------
# FCFF, WACC, DCF, bridge
# ---------------------------------------------------------------------------
def fcff_rows(years, tax_rate, sbc_as_cash_cost=False):
    rows = []
    for y in years:
        nopat = y['operating_income'] * (1 - tax_rate)
        sbc_addback = 0.0 if sbc_as_cash_cost else y['sbc']
        fcff = nopat + y['da'] + sbc_addback - y['capex'] - y['delta_wc']
        rows.append(dict(year=y['year'], ebit=y['operating_income'], nopat=nopat, da=y['da'], sbc_addback=sbc_addback,
                         capex=y['capex'], delta_wc=y['delta_wc'], fcff=fcff))
    return rows


def wacc_inputs(cost_of_equity, tax_rate, price=MARKET['price'], shares=SHARES['outstanding'],
                debt=BRIDGE_FY2026['debt'], cost_of_debt=BRIDGE_FY2026['cost_of_debt']):
    """Market-value weights (price x shares outstanding vs carrying debt). Cost of debt = the
    principal-weighted effective rate of the notes outstanding at the bridge date (10-Q Note 9)."""
    e, d = price * shares, debt
    we, wd = e / (e + d), d / (e + d)
    wacc = we * cost_of_equity + wd * cost_of_debt * (1 - tax_rate)
    return dict(equity_value_market=e, debt=d, weight_equity=we, weight_debt=wd, cost_of_equity=cost_of_equity,
                cost_of_debt_pretax=cost_of_debt, cost_of_debt_after_tax=cost_of_debt * (1 - tax_rate), wacc=wacc)


def dcf(fcffs, wacc, g, cash, debt, shares, other_assets=0.0):
    """Five explicit end-of-year FCFF, Gordon terminal at the end of the last year, bridge to per share.
    Returns None when g >= wacc (the boundary the model refuses)."""
    if g >= wacc:
        return None
    n = len(fcffs)
    factors = [1 / (1 + wacc) ** t for t in range(1, n + 1)]
    pv_explicit = sum(f * d for f, d in zip(fcffs, factors))
    terminal_cf = fcffs[-1] * (1 + g)
    terminal_value = terminal_cf / (wacc - g)
    pv_terminal = terminal_value * factors[-1]
    ev = pv_explicit + pv_terminal
    equity = ev + cash + other_assets - debt
    return dict(pv_explicit=pv_explicit, terminal_cash_flow=terminal_cf, terminal_value=terminal_value,
                pv_terminal=pv_terminal, enterprise_value=ev, terminal_share=pv_terminal / ev if ev else float('nan'),
                cash=cash, other_assets=other_assets, debt=debt, equity_value=equity, shares=shares,
                per_share=equity / shares, discount_factors=factors)


def bridge_for(inputs):
    b = BRIDGE_Q2FY2027 if inputs.get('bridge_latest') else BRIDGE_FY2026
    other = b['marketable_equity'] if inputs.get('include_marketable_equity', True) else 0.0
    return b, dict(cash_and_marketable_debt=b['cash'] + b['marketable_debt'], marketable_equity=other, debt=b['debt'])


# ---------------------------------------------------------------------------
# Checks: computed on every run, printed red or green, never silently patched.
# ---------------------------------------------------------------------------
def opening_reconciliation():
    o = pf.opening
    assets = o['cash'] + o['securities'] + o['receivables'] + o['inventory'] + o['ppe'] + o['other_assets']
    liab_eq = o['payables'] + o['accrued'] + o['debt'] + o['revolver'] + o['other_liabilities'] + o['equity']
    filed = dict(total_assets=206803.0, total_liabilities=49510.0, equity=157293.0, revenue=215938.0, cash=10605.0,
                 securities=51951.0, inventory=21403.0, receivables=38466.0)
    return dict(model_assets=assets, model_liab_eq=liab_eq, filed=filed,
                gaps=dict(assets=assets - filed['total_assets'], liab_eq=liab_eq - (filed['total_liabilities'] + filed['equity']),
                          revenue=o['revenue'] - filed['revenue'], cash=o['cash'] - filed['cash'],
                          securities=o['securities'] - filed['securities'], inventory=o['inventory'] - filed['inventory'],
                          receivables=o['receivables'] - filed['receivables']))


def run_checks(years, a, inputs, valuation, tol=0.5, offenders=()):
    checks = []

    def add(name, ok, detail, warn=False):
        checks.append(dict(name=name, status='pass' if ok else ('warn' if warn else 'fail'), detail=detail))

    add('Every driver inside its defended bounds', not offenders,
        '; '.join(offenders) if offenders else 'all drivers inside the bounds recorded in the assumption-challenge record')

    worst = {k: max(abs(y[k]) for y in years) for k in ('check_balance', 'check_cash', 'check_ppe', 'check_debt')}
    add('Balance sheet balances every year', worst['check_balance'] <= tol,
        f"largest |assets - liabilities - equity| = {worst['check_balance']:,.1f}")
    add('Cash flow ties to balance-sheet cash', worst['check_cash'] <= tol, f"largest tie residual = {worst['check_cash']:,.1f}")
    add('PP&E roll-forward', worst['check_ppe'] <= tol, f"largest residual = {worst['check_ppe']:,.1f}")
    add('Debt roll-forward', worst['check_debt'] <= tol, f"largest residual = {worst['check_debt']:,.1f}")
    rec = opening_reconciliation()
    add('Base year reconciles to the FY2026 10-K', max(abs(v) for v in rec['gaps'].values()) <= tol,
        'opening balance sheet = filed totals (assets 206,803; liabilities 49,510; equity 157,293)')
    floor_breach = min(y['cash'] - pf.min_cash for y in years)
    drawn = max(y['revolver'] for y in years)
    add('Cash stays above the 8,000 floor without the commercial-paper backstop', drawn <= tol and floor_breach >= -tol,
        f"commercial paper drawn: {drawn:,.0f}; lowest cash vs floor: {floor_breach:+,.0f}")
    add('Terminal growth below the discount rate', a['terminal_growth'] < valuation['wacc']['wacc'],
        f"g = {a['terminal_growth']:.2%} vs WACC = {valuation['wacc']['wacc']:.2%}"
        + ('' if a['terminal_growth'] < valuation['wacc']['wacc'] else ' — the model refuses to value a perpetuity that grows faster than it is discounted'))
    add('Bridge balance sheet dated at the start of the projected cash flows', not inputs.get('bridge_latest'),
        'bridge at 25 Jan 2026 = the pro-forma opening date; every FY2027E cash flow is ahead of it' if not inputs.get('bridge_latest')
        else 'bridge at 26 Jul 2026 but the cash flows start at 25 Jan 2026: the first half of FY2027 is counted twice (in the cash line and in FY2027E FCFF)')
    neg = [r['year'] for r in valuation['fcff_rows'] if r['fcff'] <= 0]
    add('Explicit FCFF positive in every year', not neg, f"non-positive years: {neg or 'none'}")
    if valuation['dcf']:
        d = valuation['dcf']
        add('Enterprise-to-equity bridge reconciles', abs(d['enterprise_value'] + d['cash'] + d['other_assets'] - d['debt'] - d['equity_value']) <= 1e-6,
            f"EV {d['enterprise_value']:,.0f} + cash & securities {d['cash'] + d['other_assets']:,.0f} - debt {d['debt']:,.0f} = equity {d['equity_value']:,.0f}")
        add('Terminal share of enterprise value below 85%', d['terminal_share'] < 0.85,
            f"{d['terminal_share']:.1%} of EV sits after FY2031E", warn=True)
    for key, (lo, hi, why) in HISTORY_BANDS.items():
        path = a[key] if isinstance(a[key], list) else [a[key]]
        inside = all(lo - 1e-9 <= v <= hi + 1e-9 for v in path)
        add(f'{key.replace("_", " ")} inside the historical band', inside,
            f"path {', '.join(f'{v:.1%}' for v in path)} vs band {lo:.1%}-{hi:.1%} ({why})")
    g = a['growth']
    add('No projected year with revenue below the FY2026 base', all(x > -0.5 for x in g) and min(_revenue_path(g)) >= 215938.0,
        f"lowest projected revenue {min(_revenue_path(g)):,.0f} vs FY2026 215,938", warn=True)
    return checks


def _revenue_path(growth):
    out, r = [], 215938.0
    for x in growth:
        r *= 1 + x
        out.append(r)
    return out


# ---------------------------------------------------------------------------
# One full valuation run
# ---------------------------------------------------------------------------
def valuation(inputs, allow_out_of_bounds=False):
    inputs, offenders = clamp_report({**BASE_INPUTS, **inputs}, allow_out_of_bounds)
    years, a = run_proforma(inputs)
    rows = fcff_rows(years, a['tax_rate'], inputs['sbc_as_cash_cost'])
    b, br = bridge_for(inputs)
    w = wacc_inputs(a['cost_of_equity'], a['tax_rate'], debt=b['debt'], cost_of_debt=b['cost_of_debt'])
    d = dcf([r['fcff'] for r in rows], w['wacc'], a['terminal_growth'], br['cash_and_marketable_debt'], br['debt'],
            SHARES['diluted'], br['marketable_equity'])
    out = dict(inputs=inputs, clamped=[] if allow_out_of_bounds else offenders, offenders=offenders,
               assumptions=a, years=years, fcff_rows=rows, wacc=w,
               bridge=dict(balance_sheet=b, **br), dcf=d, fcfe=fcfe_value(years, a),
               per_share=d['per_share'] if d else None, price=MARKET['price'],
               upside=(d['per_share'] / MARKET['price'] - 1) if d else None)
    out['checks'] = run_checks(years, a, inputs, out, offenders=offenders if allow_out_of_bounds else ())
    out['checks_failed'] = [c['name'] for c in out['checks'] if c['status'] == 'fail']
    out['checks_warned'] = [c['name'] for c in out['checks'] if c['status'] == 'warn']
    out['valid'] = not out['checks_failed'] and d is not None
    return out


HARD_CHECKS = {'Balance sheet balances every year', 'Cash flow ties to balance-sheet cash', 'PP&E roll-forward', 'Debt roll-forward',
               'Base year reconciles to the FY2026 10-K', 'Terminal growth below the discount rate',
               'Bridge balance sheet dated at the start of the projected cash flows', 'Enterprise-to-equity bridge reconciles'}


def hard_valid(v):
    """True when the arithmetic holds even if an input sits outside its defended bounds or historical band."""
    return v['dcf'] is not None and not (set(v['checks_failed']) & HARD_CHECKS)


def per_share(inputs):
    v = valuation(inputs)
    return v['per_share'] if v['valid'] else None


# ---------------------------------------------------------------------------
# Sensitivity, grid, cases, reverse DCF
# ---------------------------------------------------------------------------
def one_at_a_time(base_inputs=None, scale=1.0):
    """Each driver at its lower and upper bound (times `scale` of the distance from base), everything else at base."""
    base_inputs = {**BASE_INPUTS, **(base_inputs or {})}
    base = valuation(base_inputs)
    rows = []
    for d in DRIVERS:
        lo = d['base'] + (d['lo'] - d['base']) * scale
        hi = d['base'] + (d['hi'] - d['base']) * scale
        res = {}
        for label, v in (('lo', lo), ('hi', hi)):
            r = valuation({**base_inputs, d['key']: v})
            last = r['years'][-1]
            res[label] = dict(value=v, per_share=r['per_share'] if r['valid'] else None, valid=r['valid'],
                              op_income=last['operating_income'], fcff=r['fcff_rows'][-1]['fcff'],
                              failed=r['checks_failed'])
        ps = [res[k]['per_share'] for k in ('lo', 'hi') if res[k]['per_share'] is not None]
        rows.append(dict(key=d['key'], label=d['label'], base=d['base'], lo=res['lo'], hi=res['hi'],
                         span_per_share=(max(ps + [base['per_share']]) - min(ps + [base['per_share']])) if ps else None,
                         span_op_income=abs(res['hi']['op_income'] - res['lo']['op_income']),
                         span_fcff=abs(res['hi']['fcff'] - res['lo']['fcff'])))
    rows.sort(key=lambda r: -(r['span_per_share'] or 0))
    return dict(base_per_share=base['per_share'], scale=scale, rows=rows)


def ranking_depends_on_ranges():
    """Rank the drivers at the full bounds, at half the bounds, and at the Lab 11 ranges; report whether the order holds."""
    full = one_at_a_time(scale=1.0)
    half = one_at_a_time(scale=0.5)
    lab11 = []
    for key, step in (('growth_shift', 0.05), ('gross_margin_shift', 0.03)):
        lo = valuation({key: -step})['per_share']
        hi = valuation({key: step})['per_share']
        lab11.append(dict(key=key, span_per_share=hi - lo, lo_per_share=lo, hi_per_share=hi))
    lab11.sort(key=lambda r: -r['span_per_share'])
    return dict(full=[r['key'] for r in full['rows']], half=[r['key'] for r in half['rows']],
                lab11=[r['key'] for r in lab11], lab11_rows=lab11,
                top_two_stable=full['rows'][0]['key'] == half['rows'][0]['key'] == lab11[0]['key'])


def grid(rates=(0.10, 0.11, 0.12, 0.13, 0.14, 0.15), growths=(0.0, 0.01, 0.02, 0.03, 0.04), base_inputs=None):
    base_inputs = {**BASE_INPUTS, **(base_inputs or {})}
    cells = []
    for r in rates:
        row = []
        for g in growths:
            v = valuation({**base_inputs, 'cost_of_equity': r, 'terminal_growth': g})
            row.append(v['per_share'] if v['valid'] else None)
        cells.append(row)
    return dict(rates=list(rates), growths=list(growths), cells=cells)


CASES = [
    dict(name='Low — AI capex digestion and custom-silicon share loss',
         story='Hyperscalers pause after FY2027 (growth path 15 / 2 / -3 / -6 %), custom accelerators and AMD take price '
               '(gross margin -3 pp), R&D keeps rising into slower revenue (opex +1 pp), and the market demands the measured CAPM rate (13%).',
         inputs=dict(growth_shift=-0.10, gross_margin_shift=-0.03, opex_shift=0.01, cost_of_equity=0.13)),
    dict(name='Base — Lab 10 assumption set', story='The labelled base case: growth 25 / 12 / 7 / 4 %, gross margin 74.5 -> 70 %, 12% cost of equity, 3% terminal growth.',
         inputs=dict()),
    dict(name='High — the compute cycle keeps compounding and CUDA holds price',
         story='Data Center spending compounds (growth path 35 / 22 / 17 / 14 %), pricing power holds (gross margin +1.5 pp), '
               'and the market accepts a lower required return (11%).',
         inputs=dict(growth_shift=0.10, gross_margin_shift=0.015, cost_of_equity=0.11)),
]


def cases():
    out = []
    for c in CASES:
        v = valuation(c['inputs'])
        out.append(dict(name=c['name'], story=c['story'], inputs=c['inputs'], per_share=v['per_share'], valid=v['valid'],
                        checks_failed=v['checks_failed'], terminal_share=v['dcf']['terminal_share'] if v['dcf'] else None,
                        fy2031_revenue=v['years'][-1]['revenue'], fy2031_fcff=v['fcff_rows'][-1]['fcff']))
    return out


def solve(key, target=MARKET['price'], base_inputs=None, lo=None, hi=None, iters=80):
    """Bisection on one driver, everything else at base: the value of `key` that prices the shares at `target`.
    Searches only inside the driver's bounds; reports 'not reachable' rather than returning a bound."""
    d = next(x for x in DRIVERS if x['key'] == key)
    lo = d['lo'] if lo is None else lo
    hi = d['hi'] if hi is None else hi
    base_inputs = {**BASE_INPUTS, **(base_inputs or {})}

    def f(v):
        r = valuation({**base_inputs, key: v}, allow_out_of_bounds=True)
        return (r['per_share'] - target) if hard_valid(r) else None

    flo, fhi = f(lo), f(hi)
    if flo is None or fhi is None or flo * fhi > 0:
        reach = dict(lo=flo + target if flo is not None else None, hi=fhi + target if fhi is not None else None)
        return dict(key=key, target=target, solved=None, reachable=False, bounds=(lo, hi), value_at_bounds=reach)
    for _ in range(iters):
        mid = (lo + hi) / 2
        fm = f(mid)
        if fm is None:
            hi = mid
            continue
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return dict(key=key, target=target, solved=(lo + hi) / 2, reachable=True, bounds=(d['lo'], d['hi']),
                held_fixed=[k for k in DRIVER_KEYS if k != key])


def reverse_dcf():
    """What the price assumes, one driver at a time. Each driver is first searched inside its defended
    bounds; if the price is not reachable there, a second search over a wider, flagged range reports
    the value anyway, because 'the price needs a cost of equity below 9%' is itself the finding."""
    out = {}
    wide = dict(cost_of_equity=(0.04, 0.16), terminal_growth=(0.0, 0.10), gross_margin_shift=(-0.15, 0.25),
                growth_shift=(-0.25, 0.60), opex_shift=(-0.09, 0.06))
    for key in ('growth_shift', 'cost_of_equity', 'terminal_growth', 'gross_margin_shift', 'opex_shift'):
        r = solve(key)
        r['within_defended_bounds'] = r['reachable']
        if not r['reachable'] and key in wide:
            lo, hi = wide[key]
            r2 = solve(key, lo=lo, hi=hi)
            r2['within_defended_bounds'] = False
            r2['note'] = f'outside the defended bounds {r["bounds"]}; searched {(lo, hi)} to report what the price assumes'
            r = r2
        out[key] = r
    return out


# ---------------------------------------------------------------------------
# Comparable companies — the policy is written before the numbers are looked at.
# ---------------------------------------------------------------------------
PEER_POLICY = dict(
    frozen='Policy carried from Lab 7-8 (frozen 25 Feb 2026) and re-dated to the 23 Sep 2026 valuation date; the rules below were fixed before the multiples were computed.',
    rules=[
        'Business test: a listed operating company whose largest profit pool is accelerated-computing silicon sold into data centers (same customers, same capex budgets).',
        'Earnings basis: GAAP diluted EPS and GAAP operating income, trailing twelve months to the latest 10-Q filed on or before the valuation date; no adjusted figures.',
        'Price basis: Nasdaq close on the same trading day for every company (23 Sep 2026).',
        'Enterprise value = market capitalisation on the cover-page share count + total debt (carrying) - cash, cash equivalents and short-term investments; no leases, no equity stakes.',
        'A multiple above 100x is reported but marked not meaningful: at that level trailing earnings are too small relative to price to say anything about NVIDIA.',
        'Qualified peers are used, not dropped; the qualification is stated beside the result.',
        'No transaction (M&A) evidence: no control transaction of a comparable accelerated-computing business exists; a control premium cannot be defended for a $5tn target.',
    ])

PEERS = [
    dict(ticker='AMD', name='Advanced Micro Devices', disposition='included (qualified)',
         reason='Data-center GPUs and CPUs compete for the same racks. Qualified: client, gaming and embedded segments make the earnings mix broader, and acquired-intangible amortisation (2.3bn in FY2025) depresses GAAP earnings.',
         price=614.61, shares=1632.475, cash=5086.0 + 8025.0, debt=875.0 + 2351.0,
         ttm_eps=2.65 - 0.97 + 2.22, ttm_ebit=3694.0 - 672.0 + 3466.0, ttm_revenue=34639.0 - 15123.0 + 21789.0,
         ttm_period='FY2025 (10-K filed 2026-02-04) less H1 2025 plus H1 2026 (10-Q filed 2026-08-05); balance sheet 27 Jun 2026; cover shares 29 Jul 2026',
         source='SEC XBRL companyfacts, CIK 0000002488; src/sec_xbrl/companyfacts_extract.csv'),
    dict(ticker='AVGO', name='Broadcom', disposition='included (qualified)',
         reason='Custom AI accelerators and data-center networking. Qualified: infrastructure software (VMware) is a large part of profit, and 8bn a year of acquired-intangible amortisation depresses GAAP earnings.',
         price=354.99, shares=4773.630, cash=23975.0, debt=59419.0,
         ttm_eps=4.77 - 3.02 + 6.09, ttm_ebit=25484.0 - 17976.0 + 35306.0, ttm_revenue=63887.0 - 45872.0 + 71089.0,
         ttm_period='FY2025 (10-K filed 2025-12-18) less 9M FY2025 plus 9M FY2026 (10-Q filed 2026-09-10); balance sheet 2 Aug 2026; cover shares 28 Aug 2026',
         source='SEC XBRL companyfacts, CIK 0001730168; src/sec_xbrl/companyfacts_extract.csv'),
    dict(ticker='MRVL', name='Marvell Technology', disposition='excluded',
         reason='Passes the business screen (data-center interconnect) but its GAAP earnings carry the gain on the automotive Ethernet sale; excluded under the clean-GAAP rule as in Lab 8.',
         price=None, shares=None, cash=None, debt=None, ttm_eps=None, ttm_ebit=None, ttm_revenue=None, ttm_period='', source=''),
]

NVDA_TTM = dict(period='four quarters to 26 Jul 2026: FY2026 10-K less H1 FY2026 plus H1 FY2027 (10-Q filed 2026-08-26)',
                eps=4.90 - 1.84 + 4.85, ebit=130387.0 - 50078.0 + 117270.0, revenue=215938.0 - 90805.0 + 177837.0,
                net_income=120067.0 - 45197.0 + 118010.0)


def comps(not_meaningful_above=100.0):
    rows = []
    for p in PEERS:
        if p['price'] is None:
            rows.append(dict(ticker=p['ticker'], disposition=p['disposition'], reason=p['reason']))
            continue
        mcap = p['price'] * p['shares']
        ev = mcap + p['debt'] - p['cash']
        pe = p['price'] / p['ttm_eps']
        ev_ebit = ev / p['ttm_ebit']
        rows.append(dict(ticker=p['ticker'], disposition=p['disposition'], reason=p['reason'], price=p['price'],
                         market_cap=mcap, enterprise_value=ev, ttm_eps=p['ttm_eps'], ttm_ebit=p['ttm_ebit'],
                         ttm_revenue=p['ttm_revenue'], operating_margin=p['ttm_ebit'] / p['ttm_revenue'],
                         pe=pe, ev_ebit=ev_ebit, pe_meaningful=pe <= not_meaningful_above,
                         ev_ebit_meaningful=ev_ebit <= not_meaningful_above, ttm_period=p['ttm_period'], source=p['source']))
    b = BRIDGE_Q2FY2027   # the market multiple compares the 23 Sep price with the latest filed balance sheet
    mcap = MARKET['price'] * SHARES['outstanding']
    ev = mcap + b['debt'] - b['cash'] - b['marketable_debt']
    nvda = dict(price=MARKET['price'], market_cap=mcap, enterprise_value=ev, ttm_eps=NVDA_TTM['eps'], ttm_ebit=NVDA_TTM['ebit'],
                ttm_revenue=NVDA_TTM['revenue'], operating_margin=NVDA_TTM['ebit'] / NVDA_TTM['revenue'],
                pe=MARKET['price'] / NVDA_TTM['eps'], ev_ebit=ev / NVDA_TTM['ebit'], period=NVDA_TTM['period'])
    implied = []
    for r in rows:
        if 'pe' not in r:
            continue
        eq_from_ev = r['ev_ebit'] * NVDA_TTM['ebit'] - b['debt'] + b['cash'] + b['marketable_debt']
        implied.append(dict(ticker=r['ticker'], pe_implied=r['pe'] * NVDA_TTM['eps'] if r['pe_meaningful'] else None,
                            ev_ebit_implied=eq_from_ev / SHARES['outstanding'] if r['ev_ebit_meaningful'] else None))
    return dict(policy=PEER_POLICY, peers=rows, nvda=nvda, implied=implied,
                note='Implied values apply each peer multiple to NVIDIA\'s trailing GAAP EPS or EBIT; the EV multiple is bridged with the Q2 FY2027 balance sheet.')
