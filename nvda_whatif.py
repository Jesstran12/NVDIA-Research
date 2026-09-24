"""Take the NVIDIA base case apart — Part 2 of the pro-forma work.

Runs the base-case engine in nvda_proforma.py with one assumption changed at a
time, then several together, and answers five questions:
  1. What discount rate does the measured beta justify, and what is each rate worth?
  2. What does every operating assumption move, one at a time (tornado) and together?
  3. What would have to be true for today's share price to be the right value?
  4. Which conventions hide inside the terminal value, and what is each worth?
  5. What would make us withdraw the case (review triggers)?

Standard library only. Charts are written as SVG to charts/. Every number comes from
a full rerun of the five-year statements; the balance and cash-floor checks run on
every case, and a case that fails them is reported as "not valued", never patched.

Usage: python3 nvda_whatif.py            (from the NVDIA-Research folder)
Learning demonstration, not investment advice. USD millions unless stated.
"""
import copy
import datetime as dt
import os

import nvda_proforma as m
from beta import compute_beta

PRICE = 227.38                 # Nasdaq close, 21 Sep 2026 (src/beta_prices cache) — a dated marker
PRICE_DATE = '21 Sep 2026'
RF, ERP = 0.05, 0.0442         # course convention: 10-year Treasury 5.00%, implied equity risk premium 4.42% (July 2026)
AS_OF = dt.date(2026, 9, 24)   # end of the beta windows cached in src/beta_prices
CHART_DIR = 'charts'

KEYS = ['growth', 'gross_margin', 'opex_ratio', 'da_ratio', 'sbc_ratio', 'capex_ratio', 'tax_rate',
        'other_income', 'ar_days', 'inventory_days', 'ap_days', 'accrued_ratio', 'min_cash',
        'debt_paydown', 'payout', 'revolver_limit', 'rate_cash', 'rate_debt', 'rate_revolver',
        'cost_of_equity', 'terminal_growth']
BASE = {k: copy.deepcopy(getattr(m, k)) for k in KEYS}


# ---------------------------------------------------------------------------
# Engine wrappers
# ---------------------------------------------------------------------------
def run(**changes):
    """Project five years with some assumptions replaced; always restore the base afterwards."""
    for k, v in changes.items():
        if k not in KEYS:
            raise KeyError(k)
        setattr(m, k, copy.deepcopy(v))
    try:
        years = m.project()
    finally:
        for k in KEYS:
            setattr(m, k, copy.deepcopy(BASE[k]))
    return years


def dcf(years, r, g, adj=lambda y: 0.0):
    """FCFE discounted at r with terminal growth g; adj(y) adds to each year's FCFE (convention tests)."""
    if g >= r:
        raise ValueError(f'terminal growth {g:.1%} must be below the cost of equity {r:.1%}')
    factors = [1 / (1 + r) ** n for n in range(1, len(years) + 1)]
    flows = [y['fcfe'] + adj(y) for y in years]
    pv_explicit = sum(f * d for f, d in zip(flows, factors))
    terminal_cf = (flows[-1] + years[-1]['paydown']) * (1 + g)
    pv_terminal = terminal_cf / (r - g) * factors[-1]
    equity = pv_explicit + pv_terminal
    return dict(per_share=equity / m.SHARES, equity=equity, pv_explicit=pv_explicit,
                pv_terminal=pv_terminal, terminal_share=pv_terminal / equity, terminal_cf=terminal_cf)


def value(r=None, g=None, adj=lambda y: 0.0, **changes):
    """Full rerun -> checks -> DCF. Returns the DCF dict plus the peak revolver draw, or an error string."""
    years = run(**changes)
    try:
        m.assert_balanced(years)
    except ValueError as e:
        return dict(error=str(e), per_share=float('nan'))
    r = BASE['cost_of_equity'] if r is None else r
    g = BASE['terminal_growth'] if g is None else g
    out = dcf(years, r, g, adj)
    out['revolver_peak'] = max(y['revolver'] for y in years)
    out['years'] = years
    return out


def shift(path, d):
    return [x + d for x in path]


def money(x):
    return f'{x:,.1f}'


def solve(f, lo, hi, target, n=60):
    """Bisection: find x in [lo, hi] with f(x) = target. f must be monotonic on the bracket."""
    flo = f(lo) - target
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = f(mid) - target
        if (flo < 0) == (fm < 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def row(cells, widths):
    print(''.join(f'{str(c):>{w}}' if i else f'{str(c):<{w}}' for i, (c, w) in enumerate(zip(cells, widths))))


# ---------------------------------------------------------------------------
# Charts — plain SVG, no dependencies
# ---------------------------------------------------------------------------
INK, INK2, SURF, GRID = '#0b0b0b', '#52514e', '#fcfcfb', '#dcdcd8'
BLUE, RED = '#2a78d6', '#e34948'
RAMP = ['#cde2fb', '#b7d3f6', '#9ec5f4', '#86b6ef', '#6da7ec', '#5598e7', '#3987e5', '#2a78d6',
        '#256abf', '#1c5cab', '#184f95', '#104281', '#0d366b']


def svg_write(name, w, h, body, title):
    os.makedirs(CHART_DIR, exist_ok=True)
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="13">'
            f'<rect width="{w}" height="{h}" fill="{SURF}"/>'
            f'<text x="24" y="30" font-size="17" font-weight="700" fill="{INK}">{title}</text>')
    path = os.path.join(CHART_DIR, name)
    with open(path, 'w') as fh:
        fh.write(head + body + '</svg>')
    return path


def chart_tornado(torn, base, title):
    w, h, left, right, top, rh = 1000, 60 + 34 * len(torn) + 50, 330, 40, 60, 34
    lo = min(min(a, b) for _, a, b in torn) - 5
    hi = max(max(a, b) for _, a, b in torn) + 5
    x = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    b = []
    for tick in range(int(lo // 20) * 20, int(hi) + 20, 20):
        if lo <= tick <= hi:
            b.append(f'<line x1="{x(tick):.1f}" y1="{top}" x2="{x(tick):.1f}" y2="{top + rh * len(torn)}" stroke="{GRID}"/>'
                     f'<text x="{x(tick):.1f}" y="{top + rh * len(torn) + 18}" text-anchor="middle" fill="{INK2}">${tick}</text>')
    b.append(f'<line x1="{x(base):.1f}" y1="{top - 6}" x2="{x(base):.1f}" y2="{top + rh * len(torn)}" stroke="{INK}" stroke-width="1.5"/>'
             f'<text x="{x(base):.1f}" y="{top - 10}" text-anchor="middle" fill="{INK}" font-weight="700">base ${base:,.0f}</text>')
    for i, (label, worse, better) in enumerate(torn):
        y = top + i * rh + 6
        for v, col in ((worse, RED), (better, BLUE)):
            x0, x1 = sorted((x(base), x(v)))
            b.append(f'<rect x="{x0:.1f}" y="{y}" width="{max(x1 - x0, 1):.1f}" height="{rh - 12}" fill="{col}" rx="3"/>')
        b.append(f'<text x="{left - 10}" y="{y + 16}" text-anchor="end" fill="{INK}">{label}</text>')
        b.append(f'<text x="{x(min(worse, better)) - 6:.1f}" y="{y + 16}" text-anchor="end" fill="{INK2}" font-size="12">${min(worse, better):,.0f}</text>')
        b.append(f'<text x="{x(max(worse, better)) + 6:.1f}" y="{y + 16}" fill="{INK2}" font-size="12">${max(worse, better):,.0f}</text>')
    b.append(f'<rect x="{left}" y="{h - 26}" width="12" height="12" fill="{RED}"/><text x="{left + 18}" y="{h - 16}" fill="{INK2}">worse case</text>'
             f'<rect x="{left + 120}" y="{h - 26}" width="12" height="12" fill="{BLUE}"/><text x="{left + 138}" y="{h - 16}" fill="{INK2}">better case</text>')
    return svg_write('tornado.svg', w, h, ''.join(b), title)


def chart_axis(points, title):
    """One axis: price and the named cases as dots on a single line of value per share."""
    w, h, left, right = 1000, 200, 60, 60
    vals = [v for _, v in points]
    lo, hi = min(vals) - 15, max(vals) + 15
    x = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    y0 = 110
    b = [f'<line x1="{left}" y1="{y0}" x2="{w - right}" y2="{y0}" stroke="{INK2}" stroke-width="2"/>']
    for tick in range(int(lo // 25) * 25, int(hi) + 25, 25):
        if lo <= tick <= hi:
            b.append(f'<line x1="{x(tick):.1f}" y1="{y0 - 5}" x2="{x(tick):.1f}" y2="{y0 + 5}" stroke="{INK2}"/>'
                     f'<text x="{x(tick):.1f}" y="{y0 + 24}" text-anchor="middle" fill="{INK2}" font-size="11">${tick}</text>')
    for i, (label, v) in enumerate(sorted(points, key=lambda p: p[1])):
        col = RED if label.startswith('Price') else BLUE
        up = i % 2 == 0
        ly = y0 - 26 if up else y0 + 48
        b.append(f'<circle cx="{x(v):.1f}" cy="{y0}" r="7" fill="{col}" stroke="{SURF}" stroke-width="2"/>')
        b.append(f'<text x="{x(v):.1f}" y="{ly}" text-anchor="middle" fill="{INK}" font-size="12">{label}</text>'
                 f'<text x="{x(v):.1f}" y="{ly + 14}" text-anchor="middle" fill="{INK2}" font-size="12">${v:,.0f}</text>')
    return svg_write('one-axis.svg', w, h, ''.join(b), title)


def chart_heatmap(rates, growths, grid, base_rg, title):
    w0, h0, cw, ch, left, top = 0, 0, 120, 44, 120, 70
    w, h = left + cw * len(growths) + 40, top + ch * len(rates) + 40
    vals = [v for rw in grid for v in rw]
    lo, hi = min(vals), max(vals)
    b = [f'<text x="{left + cw * len(growths) / 2:.0f}" y="{top - 26}" text-anchor="middle" fill="{INK2}">terminal growth</text>',
         f'<text x="18" y="{top + ch * len(rates) / 2:.0f}" fill="{INK2}" transform="rotate(-90 18 {top + ch * len(rates) / 2:.0f})" text-anchor="middle">cost of equity</text>']
    for j, g in enumerate(growths):
        b.append(f'<text x="{left + j * cw + cw / 2:.0f}" y="{top - 8}" text-anchor="middle" fill="{INK}">{g:.1%}</text>')
    for i, r in enumerate(rates):
        b.append(f'<text x="{left - 10}" y="{top + i * ch + ch / 2 + 5:.0f}" text-anchor="end" fill="{INK}">{r:.1%}</text>')
        for j, g in enumerate(growths):
            v = grid[i][j]
            k = int((v - lo) / (hi - lo + 1e-9) * (len(RAMP) - 1))
            fill = RAMP[k]
            ink = INK if k < 7 else '#ffffff'
            bold = ' font-weight="700"' if (r, g) == base_rg else ''
            stroke = f' stroke="{INK}" stroke-width="2"' if (r, g) == base_rg else f' stroke="{SURF}" stroke-width="2"'
            b.append(f'<rect x="{left + j * cw}" y="{top + i * ch}" width="{cw}" height="{ch}" fill="{fill}"{stroke}/>'
                     f'<text x="{left + j * cw + cw / 2:.0f}" y="{top + i * ch + ch / 2 + 5:.0f}" text-anchor="middle" fill="{ink}"{bold}>${v:,.0f}</text>')
    return svg_write('rate-growth-grid.svg', w, h, ''.join(b), title)


# ---------------------------------------------------------------------------
# The analysis
# ---------------------------------------------------------------------------
def main():
    base = value()
    print(f"Base case: ${base['per_share']:,.2f} per share at {BASE['cost_of_equity']:.1%} / {BASE['terminal_growth']:.1%}; "
          f"{base['terminal_share']:.1%} of value after FY2031. Price {PRICE} on {PRICE_DATE}.\n")

    # 1. The discount rate, taken apart -------------------------------------------------
    print('== 1. Beta and the cost of equity (CAPM: rf + beta x ERP, rf 5.00%, ERP 4.42%)')
    reg = {
        'NVDA monthly, 5y vs SPY': compute_beta('NVDA', 'SPY', 'etf', 'monthly', 5, AS_OF),
        'NVDA weekly, 2y vs SPY': compute_beta('NVDA', 'SPY', 'etf', 'weekly', 2, AS_OF),
        'NVDA monthly, 5y vs QQQ': compute_beta('NVDA', 'QQQ', 'etf', 'monthly', 5, AS_OF),
        'AMD monthly, 5y vs SPY': compute_beta('AMD', 'SPY', 'etf', 'monthly', 5, AS_OF),
        'AVGO monthly, 5y vs SPY': compute_beta('AVGO', 'SPY', 'etf', 'monthly', 5, AS_OF),
        'MRVL monthly, 5y vs SPY': compute_beta('MRVL', 'SPY', 'etf', 'monthly', 5, AS_OF),
    }
    W = (28, 8, 8, 8, 8, 10, 8)
    row(['regression', 'beta', 's.e.', 'R2', 'Blume', 'stock vol', 'mkt vol'], W)
    for k, v in reg.items():
        row([k, f"{v['beta']:.2f}", f"{v['standard_error']:.2f}", f"{v['r_squared']:.2f}", f"{v['adjusted_beta']:.2f}",
             f"{v['stock_volatility']:.1%}", f"{v['market_volatility']:.1%}"], W)
    nv = reg['NVDA monthly, 5y vs SPY']
    peers = [reg[k]['beta'] for k in ('AMD monthly, 5y vs SPY', 'AVGO monthly, 5y vs SPY', 'MRVL monthly, 5y vs SPY')]
    peer_avg = sum(peers) / len(peers)
    implied_beta_base = (BASE['cost_of_equity'] - RF) / ERP
    rates = [
        ('Tutorial round number', 0.10, 'a market-average-plus stock; beta implied ' + f'{(0.10 - RF) / ERP:.2f}'),
        ('Beta = 1 (the market)', RF + ERP, 'what an average stock earns'),
        ('Base judgment 12%', BASE['cost_of_equity'], f'beta implied {implied_beta_base:.2f}'),
        (f"Blume-adjusted {nv['adjusted_beta']:.2f}", RF + nv['adjusted_beta'] * ERP, 'the vendor convention'),
        (f"Weekly 2y beta {reg['NVDA weekly, 2y vs SPY']['beta']:.2f}", RF + reg['NVDA weekly, 2y vs SPY']['beta'] * ERP, '104 observations, s.e. ' + f"{reg['NVDA weekly, 2y vs SPY']['standard_error']:.2f}"),
        (f'Peer average {peer_avg:.2f} (AMD, AVGO, MRVL)', RF + peer_avg * ERP, 'bottom-up; leverage adjustment omitted, all four carry little debt'),
        (f"Observed monthly beta {nv['beta']:.2f}", RF + nv['beta'] * ERP, f"s.e. {nv['standard_error']:.2f}; two s.e. span {nv['beta'] - 2 * nv['standard_error']:.2f} to {nv['beta'] + 2 * nv['standard_error']:.2f}"),
    ]
    print('\n== Same statements, seven discount rates')
    W = (44, 12, 12, 12, 10)
    row(['', 'cost of eq', '$/share', 'after FY31', 'vs base'], W)
    rate_rows = []
    for label, r, note in rates:
        v = value(r=r)
        rate_rows.append((label, r, v['per_share'], v['terminal_share'], note))
        row([label, f'{r:.2%}', f"{v['per_share']:,.1f}", f"{v['terminal_share']:.1%}", f"{v['per_share'] - base['per_share']:+.1f}"], W)

    # r x g grid
    print('\n== Cost of equity x terminal growth, $ per share')
    R = [0.10, 0.11, 0.12, 0.13, 0.14, 0.15]
    G = [0.02, 0.025, 0.03, 0.035, 0.04]
    grid = [[value(r=r, g=g)['per_share'] for g in G] for r in R]
    row([''] + [f'g={g:.1%}' for g in G], (10,) + (12,) * len(G))
    for r, rw in zip(R, grid):
        row([f'r={r:.0%}'] + [f'{v:,.1f}' for v in rw], (10,) + (12,) * len(G))
    chart_heatmap(R, G, grid, (BASE['cost_of_equity'], BASE['terminal_growth']),
                  'Value per share: cost of equity x terminal growth (same five years of statements)')

    # Terminal-value conventions
    print('\n== What the terminal value assumes, and what each alternative is worth')
    last = base['years'][-1]
    conventions = [
        ('Base: FY31 note repayment (1,500) added back; SBC added back; interest on cash in FCFE', value()),
        ('No repayment add-back after FY31', dict(per_share=dcf(base['years'], BASE['cost_of_equity'], BASE['terminal_growth'])['per_share']
                                                   - (last['paydown'] * (1 + BASE['terminal_growth']) / (BASE['cost_of_equity'] - BASE['terminal_growth'])
                                                      / (1 + BASE['cost_of_equity']) ** 5) / m.SHARES)),
        ('SBC treated as a cash cost (not added back), every year and in the terminal', value(adj=lambda y: -y['sbc'])),
        ('Interest on cash and securities excluded from FCFE (after tax)', value(adj=lambda y: -y['interest_income'] * (1 - BASE['tax_rate']))),
        ('Terminal growth 0%: a flat industry after FY31', value(g=0.0)),
        ('Terminal growth -2%: a shrinking one', value(g=-0.02)),
        ('FY27 normalised to 52 weeks (revenue x 52/53; growth 82.1%)', value(growth=[(1 + BASE['growth'][0]) * 52 / 53 - 1] + BASE['growth'][1:])),
    ]
    W = (86, 12, 10)
    row(['', '$/share', 'vs base'], W)
    for label, v in conventions:
        row([label, f"{v['per_share']:,.1f}", f"{v['per_share'] - base['per_share']:+.1f}"], W)
    reinvest = last['capex'] - last['da'] + last['delta_wc']
    print(f"\nFY31 reinvestment (capex - D&A + working capital) {money(reinvest)} on net income {money(last['net_income'])} = "
          f"{reinvest / last['net_income']:.1%} retained; growing at {BASE['terminal_growth']:.1%} forever implies a "
          f"{BASE['terminal_growth'] / (reinvest / last['net_income']):.1%} return on what is retained.")

    # 2. Operating what-ifs ----------------------------------------------------------------
    print('\n== 2. One assumption at a time, everything else at base')
    gm, gr, ox = BASE['gross_margin'], BASE['growth'], BASE['opex_ratio']
    shocks = [
        ('Gross margin path +/-2 pts', dict(gross_margin=shift(gm, -0.02)), dict(gross_margin=shift(gm, +0.02))),
        ('Growth FY28-31 +/-5 pts a year', dict(growth=gr[:1] + shift(gr[1:], -0.05)), dict(growth=gr[:1] + shift(gr[1:], +0.05))),
        ('Opex ratio path +/-1 pt', dict(opex_ratio=shift(ox, +0.01)), dict(opex_ratio=shift(ox, -0.01))),
        ('FY27 revenue +/-5% (the Q4 judgment)', dict(growth=[(1 + gr[0]) * 0.95 - 1] + gr[1:]), dict(growth=[(1 + gr[0]) * 1.05 - 1] + gr[1:])),
        ('Capex +/-1 pt of revenue', dict(capex_ratio=BASE['capex_ratio'] + 0.01), dict(capex_ratio=BASE['capex_ratio'] - 0.01)),
        ('Tax rate +/-2 pts', dict(tax_rate=BASE['tax_rate'] + 0.02), dict(tax_rate=BASE['tax_rate'] - 0.02)),
        ('Receivable days +/-10', dict(ar_days=BASE['ar_days'] + 10), dict(ar_days=BASE['ar_days'] - 10)),
        ('Inventory days +/-20', dict(inventory_days=BASE['inventory_days'] + 20), dict(inventory_days=BASE['inventory_days'] - 20)),
        ('SBC +/-0.5 pt of revenue (add-back runs backwards)', dict(sbc_ratio=BASE['sbc_ratio'] - 0.005), dict(sbc_ratio=BASE['sbc_ratio'] + 0.005)),
        ('Yield on cash +/-1 pt', dict(rate_cash=BASE['rate_cash'] - 0.01), dict(rate_cash=BASE['rate_cash'] + 0.01)),
        ('Payout 75% vs 100% of FCFE (a distribution, not value)', dict(payout=0.75), dict(payout=1.0)),
    ]
    torn = []
    for label, worse, better in shocks:
        lo, hi = value(**worse), value(**better)
        torn.append((label, lo['per_share'], hi['per_share']))
    torn.sort(key=lambda t: -abs(t[2] - t[1]))
    W = (54, 14, 14, 12)
    row(['', 'worse $/sh', 'better $/sh', 'swing'], W)
    for label, lo, hi in torn:
        row([label, f'{lo:,.1f}', f'{hi:,.1f}', f'{hi - lo:,.1f}'], W)
    chart_tornado(torn, base['per_share'], 'One assumption at a time: value per share, worse and better case')

    print('\n== Growth after FY27: what each path is worth')
    paths = [
        ('Flat after FY27 (0% x 4)', [gr[0], 0, 0, 0, 0]),
        ('Half the base path (12.5 / 6 / 3.5 / 2)', [gr[0], 0.125, 0.06, 0.035, 0.02]),
        ('Base (25 / 12 / 7 / 4)', gr),
        ('Base +5 pts a year (30 / 17 / 12 / 9)', gr[:1] + shift(gr[1:], 0.05)),
        ('Compounding capex cycle (40 / 25 / 15 / 10)', [gr[0], 0.40, 0.25, 0.15, 0.10]),
    ]
    W = (46, 16, 12, 10)
    row(['', 'FY31 revenue', '$/share', 'vs base'], W)
    growth_rows = []
    for label, p in paths:
        v = value(growth=p)
        if 'error' in v:
            row([label, '', 'not valued', v['error'][:40]], W); continue
        growth_rows.append((label, v['years'][-1]['revenue'], v['per_share']))
        row([label, f"{v['years'][-1]['revenue']:,.0f}", f"{v['per_share']:,.1f}", f"{v['per_share'] - base['per_share']:+.1f}"], W)

    print('\n== Gross margin path x growth path, $ per share')
    GMs = [-0.03, 0.0, 0.03]
    GRs = [-0.05, 0.0, 0.05]
    two = [[value(gross_margin=shift(gm, a), growth=gr[:1] + shift(gr[1:], b))['per_share'] for b in GRs] for a in GMs]
    row([''] + [f'growth {b:+.0%}/yr' for b in GRs], (20, 16, 16, 16))
    for a, rw in zip(GMs, two):
        row([f'margin {a:+.0%}'] + [f'{v:,.1f}' for v in rw], (20, 16, 16, 16))

    print('\n== Named cases: several assumptions moved together (each a full rerun)')
    cases = {
        'Bear: custom silicon takes share': dict(gross_margin=[0.745, 0.70, 0.66, 0.63, 0.60], growth=[gr[0], 0.10, 0.0, -0.05, 0.0],
                                                 opex_ratio=[0.087, 0.11, 0.13, 0.14, 0.15]),
        'Digestion: AI capex pauses in FY28': dict(growth=[gr[0], -0.20, 0.0, 0.10, 0.05], gross_margin=[0.745, 0.70, 0.70, 0.70, 0.70],
                                                    opex_ratio=[0.087, 0.12, 0.13, 0.13, 0.13]),
        'Base': dict(),
        'Bull: AI capex keeps compounding': dict(growth=[gr[0], 0.40, 0.25, 0.15, 0.10], gross_margin=[0.745, 0.745, 0.74, 0.735, 0.73],
                                                 ),
    }
    W = (40, 12, 12, 14, 14)
    row(['', '$/share', 'after FY31', 'balance', 'revolver peak'], W)
    case_vals = {}
    for label, ch in cases.items():
        v = value(**ch)
        case_vals[label] = v
        if 'error' in v:
            row([label, 'not valued', '', v['error'][:40], ''], W)
        else:
            row([label, f"{v['per_share']:,.1f}", f"{v['terminal_share']:.1%}", 'OK 0.0', f"{v['revolver_peak']:,.1f}"], W)
    dig = cases['Digestion: AI capex pauses in FY28']
    parts = sum(value(**{k: v})['per_share'] - base['per_share'] for k, v in dig.items())
    print(f"Digestion case if you just added its three single shocks: {base['per_share'] + parts:,.1f} — "
          f"the model says {case_vals['Digestion: AI capex pauses in FY28']['per_share']:,.1f}. Shocks interact; always rerun.")

    print('\n== Review triggers (kill criteria): what the next two quarterly reports can confirm or deny')
    triggers = [
        ('Gross margin guided below 72% and keeps falling (path 72 / 68 / 66 / 65 / 65)', dict(gross_margin=[0.72, 0.68, 0.66, 0.65, 0.65])),
        ('Data Center revenue falls quarter on quarter (FY28 growth 10%, not 25%)', dict(growth=[gr[0], 0.10] + gr[2:])),
        ('Operating expenses grow faster than revenue (opex path +2 pts)', dict(opex_ratio=shift(ox, 0.02))),
    ]
    W = (76, 12, 10)
    row(['', '$/share', 'change'], W)
    trig_rows = []
    for label, ch in triggers:
        v = value(**ch)
        trig_rows.append((label, v['per_share']))
        row([label, f"{v['per_share']:,.1f}", f"{v['per_share'] - base['per_share']:+.1f}"], W)

    # 3. What the price is paying for -----------------------------------------------------
    print(f'\n== 3. What would have to be true for ${PRICE} to be the right value (one assumption at a time)')
    implied = [
        ('Cost of equity', lambda x: value(r=x)['per_share'], 0.05, 0.20, f"{BASE['cost_of_equity']:.2%}", '{:.2%}'),
        ('Terminal growth', lambda x: value(g=x)['per_share'], -0.05, 0.10, f"{BASE['terminal_growth']:.2%}", '{:.2%}'),
        ('Gross margin, every year (shift)', lambda x: value(gross_margin=shift(gm, x))['per_share'], -0.10, 0.20, '74.5% -> 70.0%', '{:+.1%} pts'),
        ('Growth FY28-31, every year (shift)', lambda x: value(growth=gr[:1] + shift(gr[1:], x))['per_share'], -0.30, 0.60, '25 / 12 / 7 / 4', '{:+.1%} pts'),
        ('Opex ratio, every year (shift)', lambda x: value(opex_ratio=shift(ox, x))['per_share'], -0.08, 0.10, '8.7% -> 12.5%', '{:+.1%} pts'),
    ]
    W = (40, 20, 44)
    row(['', 'base', 'implied by the price'], W)
    implied_rows = []
    for label, f, lo, hi, basetxt, fmt in implied:
        try:
            x = solve(f, lo, hi, PRICE)
            txt = fmt.format(x)
            if abs(f(x) - PRICE) > 1.0:
                txt = f'not reachable: even {fmt.format(hi)} gives ${f(hi):,.0f}'
        except ValueError as e:
            txt = f'not solvable: {e}'
        implied_rows.append((label, basetxt, txt))
        row([label, basetxt, txt], W)
    beta_at_price = ((solve(lambda x: value(r=x)['per_share'], 0.05, 0.20, PRICE)) - RF) / ERP
    print(f'The implied cost of equity corresponds to a CAPM beta of {beta_at_price:.2f}.')

    # 4. One-axis picture -----------------------------------------------------------------
    chart_axis([(f'Price {PRICE_DATE}', PRICE), ('Bear', case_vals['Bear: custom silicon takes share']['per_share']),
                ('Digestion', case_vals['Digestion: AI capex pauses in FY28']['per_share']), ('Base', base['per_share']),
                ('Bull', case_vals['Bull: AI capex keeps compounding']['per_share']),
                ('Base at 10%', value(r=0.10)['per_share'])],
               'Value per share on one axis: the price against the cases')
    print(f'\nCharts written to {CHART_DIR}/: tornado.svg, one-axis.svg, rate-growth-grid.svg')
    return dict(base=base, reg=reg, rate_rows=rate_rows, R=R, G=G, grid=grid, conventions=conventions,
                reinvest=reinvest, torn=torn, growth_rows=growth_rows, GMs=GMs, GRs=GRs, two=two,
                cases=cases, case_vals=case_vals, parts=base['per_share'] + parts, trig_rows=trig_rows,
                implied_rows=implied_rows, beta_at_price=beta_at_price, peer_avg=peer_avg)


if __name__ == '__main__':
    main()
