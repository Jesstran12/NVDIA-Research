"""Project 1 analysis boundary: every material finance result is computed here, not in the interface.

    python3 analysis.py            # runs the full analysis at the base inputs and writes
                                   #   output/visible_output.json  (the frozen interface contract)
                                   #   output/visible_output.md    (the visible executed output a grader reads)
    python3 analysis.py --break    # the Lab 10 loud-failure demonstration (typed cash line; the model must refuse)

`run_analysis(inputs)` is the function the app and the tests call. Standard library only.
USD millions unless stated. Learning demonstration, not investment advice.
"""
import datetime as dt
import json
import os
import subprocess
import sys

import engine as e
import nvda_proforma as pf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, 'output')

DECISION = dict(
    user='Buy-side investment committee; the fund holds no position in NVIDIA',
    role='AI task-force analyst embedded in the sector analyst group',
    question='Initiate a position, place the name on watch/defer, or do not initiate, at the 23 Sep 2026 price',
    horizon='Three- to five-year holding period; next review after the Q3 and Q4 FY2027 reports (Nov 2026, Feb 2027)',
    target='NVIDIA Corporation common stock (NASDAQ: NVDA)',
    valuation_date='2026-09-23', currency='USD', units='USD millions; per-share values in USD',
    share_basis='24,100m shares outstanding (10-Q cover, 21 Aug 2026) + 95m dilutive award increment (Q2 FY2027 Note 4) = 24,195m diluted',
    exclusions=['Equity-stake gains (9.0bn in FY2026, 23.7bn in H1 FY2027) are not forecast: a gain is not a cash flow.',
                'Non-marketable equity securities (22.3bn at FY2026; 51.2bn at Q2 FY2027) are left out of the bridge: no observable price.',
                'Operating leases are not treated as debt (ASC 842 lease liabilities sit in other liabilities, as NVIDIA reports them).',
                'No transaction (M&A) multiples: no defensible control transaction for a $5tn accelerated-computing business exists.',
                'Information after 23 Sep 2026 is not used; the model runs on filings to the Q2 FY2027 10-Q (filed 26 Aug 2026).'],
)


def _committee_action(price, low, base, high):
    """The decision rule, written before the numbers: compare the price with the causal case range."""
    if price <= low:
        return ('Initiate', 'the price sits at or below the low case: the market pays for less than the downside scenario delivers')
    if price <= base:
        return ('Watch / defer, leaning initiate', 'the price sits between the low case and the base case')
    if price <= high:
        return ('Watch / defer', 'the price sits inside the base-to-high range; initiation needs evidence that moves the base')
    return ('Do not initiate at this price; keep on watch',
            'the price sits above the high case: it already pays for more than the compounding-cycle scenario delivers')


def run_analysis(inputs=None, full=True):
    """Return every material output as one dictionary. `full=False` skips the slow sweeps (used by the app for live runs)."""
    inputs = {**e.BASE_INPUTS, **(inputs or {})}
    v = e.valuation(inputs)
    res = dict(decision=DECISION, target=e.TARGET, market=e.MARKET, shares=e.SHARES, inputs=inputs, assumptions=v['assumptions'],
               statements=[{k: y[k] for k in y} for y in v['years']], fcff_rows=v['fcff_rows'], wacc=v['wacc'],
               bridge=v['bridge'], dcf={k: x for k, x in (v['dcf'] or {}).items() if k != 'discount_factors'},
               fcfe_cross_check=v['fcfe'], per_share=v['per_share'], price=e.MARKET['price'], upside=v['upside'],
               checks=v['checks'], checks_failed=v['checks_failed'], valid=v['valid'], clamped=v['clamped'])
    if not full:
        return res
    res['cases'] = e.cases()
    res['grid'] = e.grid()
    res['sensitivity'] = e.one_at_a_time()
    res['ranking_test'] = e.ranking_depends_on_ranges()
    res['reverse_dcf'] = e.reverse_dcf()
    res['flip_scenario'] = e.flip_scenario()
    res['comps'] = e.comps()
    res['drivers'] = e.DRIVERS
    res['toggles'] = e.TOGGLES
    low, base, high = (c['per_share'] for c in res['cases'])
    action, why = _committee_action(e.MARKET['price'], low, base, high)
    res['recommendation'] = dict(
        action=action, why=why, range_low=low, range_base=base, range_high=high, price=e.MARKET['price'],
        conditions=[
            f'Initiate only if the price falls below the base case (${base:,.0f}) with the checks still passing, or if two quarterly reports move the growth path enough to lift the high case above the price.',
            'Hold the watch posture while Data Center revenue keeps growing quarter on quarter and gross margin guidance stays at or above 72%.',
        ],
        reversal_triggers=[
            dict(metric='Data Center revenue, quarter on quarter', threshold='any decline', window='next two quarterly reports (Nov 2026, Feb 2027)',
                 effect='withdraw the base case and rebuild as the low case (about $80)'),
            dict(metric='Gross margin guidance', threshold='below 72% and falling', window='next two quarterly reports',
                 effect='move the gross-margin path down 3 pp (about -$12 at base)'),
            dict(metric='Operating expenses vs revenue', threshold='opex growing faster than revenue for two quarters', window='next two quarterly reports',
                 effect='opex path +2 pp (about -$5 at base)'),
            dict(metric='Enterprise-to-equity bridge', threshold='fails to reconcile after the next 10-Q (new debt, buybacks, securities)', window='each filing',
                 effect='reject the per-share conclusion until the bridge reconciles'),
        ],
        committee_ask='Approve watch/defer: no position now; authorise a re-review within one week of the Q3 FY2027 report with the tool re-run on the new filing.',
        monitoring_owner='the analyst (this tool re-run on each filing); sector analysts own the demand view',
    )
    res['method_disagreement'] = _method_disagreement(res)
    res['run'] = dict(timestamp=dt.datetime.now().astimezone().isoformat(timespec='seconds'), commit=_git_commit(),
                      python=sys.version.split()[0], engine='engine.py over nvda_proforma.py (Lab 10) and proforma.py (Lab 09)')
    return res


def _method_disagreement(res):
    c = res['comps']
    avgo = next(p for p in c['peers'] if p.get('ticker') == 'AVGO')
    amd = next(p for p in c['peers'] if p.get('ticker') == 'AMD')
    imp = next(i for i in c['implied'] if i['ticker'] == 'AVGO')
    rd = res['reverse_dcf']
    return [
        f"FCFF DCF (base ${res['per_share']:,.0f}; causal range ${res['cases'][0]['per_share']:,.0f}-${res['cases'][2]['per_share']:,.0f}) values the cash flows the filings and guidance support; it assumes growth decelerates from 25% to 4% after FY2027 and a 12% cost of equity.",
        f"The FCFE cross-check from Lab 10 gives ${res['fcfe_cross_check']['per_share']:,.2f}: the two cash-flow definitions agree within a dollar because NVIDIA carries almost no net debt.",
        f"Trailing GAAP multiples disagree with the DCF in both directions. NVIDIA itself trades at {c['nvda']['pe']:.1f}x trailing earnings and {c['nvda']['ev_ebit']:.1f}x trailing EBIT; Broadcom at {avgo['pe']:.1f}x and {avgo['ev_ebit']:.1f}x, which applied to NVIDIA's trailing figures implies ${imp['pe_implied']:,.0f} (P/E) and ${imp['ev_ebit_implied']:,.0f} (EV/EBIT). AMD's {amd['pe']:.0f}x P/E and {amd['ev_ebit']:.0f}x EV/EBIT are reported but not meaningful: its {amd['operating_margin']:.0%} operating margin against NVIDIA's {c['nvda']['operating_margin']:.0%} means the market is capitalising a recovery, not current earnings.",
        "Why they disagree: a trailing multiple capitalises last year's earnings at whatever growth the market expects of the peer; the DCF capitalises my explicit growth path. The peer multiples say the market expects NVIDIA's earnings to keep compounding well past FY2028; the DCF says the filings do not yet show that. The methods are not averaged: the DCF is the supported value, the multiples describe what the price is paying for.",
        f"Reverse DCF puts the disagreement in operating language: the price needs about {rd['growth_shift']['solved'] * 100:+.0f} pp more growth in each of FY2028-FY2031 (a path near {', '.join(f'{(g + rd['growth_shift']['solved']) * 100:.0f}%' for g in e.PF_BASE['growth'][1:])}), or a cost of equity near {rd['cost_of_equity']['solved']:.1%}, or terminal growth near {rd['terminal_growth']['solved']:.1%}; no gross-margin or opex assumption inside the defended bounds reaches it.",
    ]


def _git_commit():
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=HERE, text=True).strip()
    except Exception:
        return 'unknown'


# ---------------------------------------------------------------------------
# Visible executed output
# ---------------------------------------------------------------------------
def _m(x, nd=0):
    return 'n/a' if x is None else f'{x:,.{nd}f}'


def _p(x, nd=1):
    return 'n/a' if x is None else f'{x * 100:.{nd}f}%'


def _fmt_driver_value(d, v):
    return f'{v * 100:+.1f} pp' if d['fmt'] == 'pp' else f'{v * 100:.2f}%'


def to_markdown(res):
    L = []
    r = res['recommendation']
    L += [f"# NVIDIA (NVDA) — Project 1 visible executed output",
          f"Run {res['run']['timestamp']} at commit `{res['run']['commit']}` with Python {res['run']['python']}; engine {res['run']['engine']}. "
          f"USD millions unless stated. Learning demonstration for FIN 43900, not investment advice.", "",
          "## Decision", "",
          f"**{r['action']}** — {r['why']}.", "",
          "| Item | Value |", "|---|---|",
          f"| Intended user | {res['decision']['user']} |",
          f"| Decision | {res['decision']['question']} |",
          f"| Horizon | {res['decision']['horizon']} |",
          f"| Valuation date / price | {res['decision']['valuation_date']} / ${res['price']:,.2f} ({res['market']['price_source']}) |",
          f"| Currency and units | {res['decision']['units']} |",
          f"| Share basis | {res['decision']['share_basis']} |",
          f"| Value per share, base | **${res['per_share']:,.2f}** ({_p(res['upside'])} vs price) |",
          f"| Causal range (low / base / high) | ${r['range_low']:,.2f} / ${r['range_base']:,.2f} / ${r['range_high']:,.2f} |",
          f"| Committee ask | {r['committee_ask']} |",
          f"| Checks | {'all pass' if res['valid'] else 'FAILED: ' + ', '.join(res['checks_failed'])} |", ""]
    L += ["**Conditions:** " + ' '.join(r['conditions']), "", "**Reversal triggers (metric · threshold · window · effect):**", ""]
    L += [f"- {t['metric']} · {t['threshold']} · {t['window']} · {t['effect']}" for t in r['reversal_triggers']]
    L += ["", "**Exclusions:** " + ' '.join(res['decision']['exclusions']), ""]

    L += ["## Checks (computed on this run)", "", "| Status | Check | Detail |", "|---|---|---|"]
    L += [f"| {c['status'].upper()} | {c['name']} | {c['detail']} |" for c in res['checks']]

    L += ["", "## Driver panel — value · basis · bounds · challenge · evidence that would change it", "",
          "| Driver | Base value | Basis | Defended bounds | Why these bounds | Challenge | Evidence to change it |", "|---|---|---|---|---|---|---|"]
    for d in res['drivers']:
        L.append(f"| {d['label']} | {_fmt_driver_value(d, d['base'])} ({d['value_note']}) | {d['basis']} | {_fmt_driver_value(d, d['lo'])} to {_fmt_driver_value(d, d['hi'])} | {d['bound_reason']} | {d['challenge']} | {d['evidence']} |")

    ys = res['statements']
    hdr = '| | ' + ' | '.join(f"FY{y['year']}E" for y in ys) + ' |'
    sep = '|---|' + '---:|' * len(ys)
    L += ["", "## Five-year pro-forma (Lab 10 engine, base assumptions)", "", hdr, sep]
    for label, key in [('Revenue', 'revenue'), ('Gross profit', 'gross_profit'), ('Operating expenses', 'opex'),
                       ('Operating income', 'operating_income'), ('Net income', 'net_income'), ('Cash', 'cash'),
                       ('Receivables', 'receivables'), ('Inventory', 'inventory'), ('PP&E and intangibles', 'ppe'),
                       ('Total assets', 'total_assets'), ('Notes', 'debt'), ('Commercial paper drawn', 'revolver'),
                       ('Equity', 'equity'), ('Total liabilities & equity', 'total_liabilities_equity'),
                       ('Free cash flow to equity', 'fcfe'), ('Assets − liabilities − equity', 'check_balance'),
                       ('Cash: balance sheet vs cash flow', 'check_cash')]:
        L.append(f"| {label} | " + ' | '.join(_m(y[key], 1 if key.startswith('check') else 0) for y in ys) + ' |')

    L += ["", "## FCFF, WACC and the enterprise-to-equity bridge", "", hdr, sep]
    for label, key in [('EBIT (operating income)', 'ebit'), ('NOPAT = EBIT × (1 − t)', 'nopat'), ('+ D&A', 'da'),
                       ('+ SBC add-back', 'sbc_addback'), ('− Capital spending', 'capex'), ('− Working-capital build', 'delta_wc'), ('FCFF', 'fcff')]:
        L.append(f"| {label} | " + ' | '.join(_m(rw[key]) for rw in res['fcff_rows']) + ' |')
    w, d, b = res['wacc'], res['dcf'], res['bridge']
    L += ["", "| WACC input | Value |", "|---|---|",
          f"| Cost of equity (driver) | {_p(w['cost_of_equity'], 2)} |",
          f"| Cost of debt, pre-tax / after-tax | {_p(w['cost_of_debt_pretax'], 2)} / {_p(w['cost_of_debt_after_tax'], 2)} ({b['balance_sheet']['cost_of_debt_note']}) |",
          f"| Market value of equity / debt | {_m(w['equity_value_market'])} / {_m(w['debt'])} (weights {_p(w['weight_equity'], 2)} / {_p(w['weight_debt'], 2)}) |",
          f"| **WACC** | **{_p(w['wacc'], 2)}** |", "",
          "| Valuation | USD millions |", "|---|---:|",
          f"| PV of FY2027E–FY2031E FCFF | {_m(d['pv_explicit'])} |",
          f"| FY2032 cash flow = FY2031E FCFF × (1 + g) | {_m(d['terminal_cash_flow'])} |",
          f"| Terminal value at FY2031E (g = {_p(res['assumptions']['terminal_growth'])}) | {_m(d['terminal_value'])} |",
          f"| PV of terminal value | {_m(d['pv_terminal'])} ({_p(d['terminal_share'])} of enterprise value) |",
          f"| **Enterprise value** | **{_m(d['enterprise_value'])}** |",
          f"| + Cash and marketable debt securities ({b['balance_sheet']['as_of']}) | {_m(b['cash_and_marketable_debt'])} |",
          f"| + Marketable equity securities | {_m(b['marketable_equity'])} |",
          f"| − Debt, carrying ({b['balance_sheet']['debt_note']}) | {_m(b['debt'])} |",
          f"| **Equity value** | **{_m(d['equity_value'])}** |",
          f"| Diluted shares (millions) | {_m(d['shares'])} |",
          f"| **Value per share** | **${d['per_share']:,.2f}** |",
          f"| FCFE cross-check (Lab 10, 12% / 3%) | ${res['fcfe_cross_check']['per_share']:,.2f} |",
          f"| Bridge source | {b['balance_sheet']['source']} |"]

    L += ["", "## Causal cases", "", "| Case | What moves | $/share | FY2031E revenue | FY2031E FCFF | Terminal share | Checks |", "|---|---|---:|---:|---:|---:|---|"]
    for c in res['cases']:
        L.append(f"| {c['name']} | {c['story']} | {c['per_share']:,.2f} | {_m(c['fy2031_revenue'])} | {_m(c['fy2031_fcff'])} | {_p(c['terminal_share'])} | {'pass' if c['valid'] else 'FAIL: ' + ', '.join(c['checks_failed'])} |")

    g = res['grid']
    L += ["", "## WACC × terminal growth, $ per share (base in bold)", "",
          "Rows are the cost-of-equity driver; the WACC it produces (debt weight 0.16%) is shown beside it.", "",
          "| Cost of equity (WACC) \\ g | " + ' | '.join(_p(x) for x in g['growths']) + ' |', '|---|' + '---:|' * len(g['growths'])]
    for rate, row in zip(g['rates'], g['cells']):
        cells = []
        for gg, x in zip(g['growths'], row):
            s = 'invalid' if x is None else f'{x:,.1f}'
            cells.append(f'**{s}**' if abs(rate - 0.12) < 1e-9 and abs(gg - 0.03) < 1e-9 else s)
        L.append(f"| {_p(rate)} ({_p(e.wacc_inputs(rate, res['assumptions']['tax_rate'])['wacc'], 2)}) | " + ' | '.join(cells) + ' |')

    s = res['sensitivity']
    L += ["", f"## One-at-a-time sensitivity at the defended bounds (base ${s['base_per_share']:,.2f})", "",
          "| Driver | Low input → $/share | High input → $/share | Span $/share | Span FY2031E op. income | Span FY2031E FCFF |", "|---|---|---|---:|---:|---:|"]
    for row in s['rows']:
        d_ = next(x for x in res['drivers'] if x['key'] == row['key'])
        L.append(f"| {row['label']} | {_fmt_driver_value(d_, row['lo']['value'])} → {_m(row['lo']['per_share'], 2)} | {_fmt_driver_value(d_, row['hi']['value'])} → {_m(row['hi']['per_share'], 2)} | {_m(row['span_per_share'], 2)} | {_m(row['span_op_income'])} | {_m(row['span_fcff'])} |")
    rt = res['ranking_test']
    L += ["", f"Ranking at the full bounds: {' > '.join(rt['full'])}. At half the bounds: {' > '.join(rt['half'])}. "
          f"At the Lab 11 ranges (±5 pp growth, ±3 pp gross margin): {' > '.join(rt['lab11'])} "
          f"(spans ${rt['lab11_rows'][0]['span_per_share']:,.2f} and ${rt['lab11_rows'][1]['span_per_share']:,.2f}). "
          f"The top driver {'is the same under all three range choices' if rt['top_two_stable'] else 'changes with the range choice'}; "
          "over these ranges the growth path after FY2027 carries the value, and the ranking below it depends on how wide each bound is."]

    rd = res['reverse_dcf']
    L += ["", f"## Reverse DCF — what ${res['price']:,.2f} assumes, one driver at a time (all others at base)", "",
          "| Driver | Base | Implied by the price | Inside defended bounds? |", "|---|---|---|---|"]
    for key, rr in rd.items():
        d_ = next(x for x in res['drivers'] if x['key'] == key)
        sol = 'not reachable in ' + str(rr['bounds']) if rr.get('solved') is None else _fmt_driver_value(d_, rr['solved'])
        L.append(f"| {d_['label']} | {_fmt_driver_value(d_, d_['base'])} | {sol} | {'yes' if rr.get('within_defended_bounds') else 'no — ' + rr.get('note', '')} |")

    L += ["", "## What would reverse the call — the smallest change that lifts value to the price", "",
          "The downside cases cannot alter a do-not-initiate call; the scenario that would is on the upside. Each row is a full rerun with checks.", "",
          "| Scenario | Growth shift needed | Resulting FY2028E–FY2031E path | FY2031E revenue | $/share | Checks |", "|---|---|---|---:|---:|---|"]
    for f in res['flip_scenario']:
        if f['reachable']:
            L.append(f"| {f['name']} | {f['growth_shift'] * 100:+.1f} pp a year | {' / '.join(f'{g * 100:.0f}%' for g in f['growth_path'])} | {_m(f['fy2031_revenue'])} | {f['per_share']:,.2f} | {'pass' if f['valid'] else 'FAIL'} |")
        else:
            L.append(f"| {f['name']} | not reachable inside the defended bounds | — | — | — | — |")
    L += ["", "Monitoring: the Q3 and Q4 FY2027 reports show whether Data Center growth is tracking the +17 pp path (about 42% in FY2028E) or the base 25%; "
          "the call is reviewed on each report, with the tool re-run on the new filing."]
    c = res['comps']
    L += ["", "## Comparable companies (policy frozen before the numbers)", "", c['policy']['frozen'], ""]
    L += [f"- {rule}" for rule in c['policy']['rules']]
    L += ["", "| Company | Disposition | Price 23 Sep 2026 | TTM GAAP EPS | TTM EBIT | Op. margin | Enterprise value | P/E | EV/EBIT | Basis |", "|---|---|---:|---:|---:|---:|---:|---:|---:|---|"]
    n = c['nvda']
    L.append(f"| NVIDIA (target) | — | {n['price']:,.2f} | {n['ttm_eps']:.2f} | {_m(n['ttm_ebit'])} | {_p(n['operating_margin'])} | {_m(n['enterprise_value'])} | {n['pe']:.1f}x | {n['ev_ebit']:.1f}x | {n['period']} |")
    for p in c['peers']:
        if 'pe' in p:
            L.append(f"| {p['ticker']} | {p['disposition']} | {p['price']:,.2f} | {p['ttm_eps']:.2f} | {_m(p['ttm_ebit'])} | {_p(p['operating_margin'])} | {_m(p['enterprise_value'])} | {p['pe']:.1f}x{'' if p['pe_meaningful'] else ' (not meaningful)'} | {p['ev_ebit']:.1f}x{'' if p['ev_ebit_meaningful'] else ' (not meaningful)'} | {p['ttm_period']} |")
        else:
            L.append(f"| {p['ticker']} | {p['disposition']} | — | — | — | — | — | — | — | {p['reason']} |")
    L += ["", "| Peer | NVIDIA value implied by its P/E | by its EV/EBIT |", "|---|---:|---:|"]
    L += [f"| {i['ticker']} | {'$' + _m(i['pe_implied'], 2) if i['pe_implied'] else 'not meaningful'} | {'$' + _m(i['ev_ebit_implied'], 2) if i['ev_ebit_implied'] else 'not meaningful'} |" for i in c['implied']]
    L += ["", "Peer qualifications: " + ' '.join(f"**{p['ticker']}** — {p['reason']}" for p in c['peers'])]

    L += ["", "## Why the methods disagree (not averaged)", ""]
    L += [f"- {x}" for x in res['method_disagreement']]
    L += ["", "## Sources and as-of boundary", "",
          f"- {res['bridge']['balance_sheet']['source']}", f"- {res['market']['price_source']}; {res['market']['rf_source']}",
          "- FY2024-FY2026 10-Ks (accessions 0001045810-24-000029, -25-000023, -26-000021) for the history grid in nvda-proforma.md",
          "- Q1 and Q2 FY2027 10-Qs (0001045810-26-000052, -26-000075) and the Q2 FY2027 press release (8-K 0001045810-26-000073, 26 Aug 2026) for H1 actuals, the Q3 outlook and the share count",
          "- Peer figures: SEC XBRL companyfacts for AMD (CIK 0000002488) and Broadcom (CIK 0001730168), extracted to src/sec_xbrl/companyfacts_extract.csv; Nasdaq closes 23 Sep 2026 cached in src/beta_prices/",
          "- Full evidence ledger: docs/evidence-ledger.csv; base-year normalization (one-time items, basis changes, mechanical checks): docs/base-year-normalization.md"]
    return '\n'.join(L) + '\n'


def visible_output_json(res):
    """The frozen interface contract: the validated subset the app renders, with as-of date, units and limitations."""
    r = res['recommendation']
    return dict(
        decision=f"{r['action']} — NVIDIA (NVDA) for the buy-side investment committee (no current position)",
        as_of=res['decision']['valuation_date'], price=res['price'], currency='USD', units=res['decision']['units'],
        share_basis=res['decision']['share_basis'],
        recommendation=f"{r['action']}: value per share ${r['range_low']:,.0f} (low) / ${r['range_base']:,.0f} (base) / ${r['range_high']:,.0f} (high) against ${res['price']:,.2f}. " + ' '.join(r['conditions']),
        reversal_trigger='; '.join(f"{t['metric']}: {t['threshold']} ({t['window']}) → {t['effect']}" for t in r['reversal_triggers']),
        committee_ask=r['committee_ask'], monitoring_owner=r['monitoring_owner'],
        per_share_base=res['per_share'], range_low=r['range_low'], range_high=r['range_high'], upside_base=res['upside'],
        wacc=res['wacc']['wacc'], terminal_growth=res['assumptions']['terminal_growth'], terminal_share=res['dcf']['terminal_share'],
        enterprise_value=res['dcf']['enterprise_value'], equity_value=res['dcf']['equity_value'], diluted_shares=res['dcf']['shares'],
        bridge=dict(as_of=res['bridge']['balance_sheet']['as_of'], cash_and_marketable_debt=res['bridge']['cash_and_marketable_debt'],
                    marketable_equity=res['bridge']['marketable_equity'], debt=res['bridge']['debt']),
        fcfe_cross_check=res['fcfe_cross_check']['per_share'],
        checks={c['name']: c['status'] for c in res['checks']}, checks_failed=res['checks_failed'],
        cases=[dict(name=c['name'], per_share=c['per_share']) for c in res['cases']],
        sensitivity_ranking=[dict(driver=x['label'], span_per_share=x['span_per_share']) for x in res['sensitivity']['rows']],
        reverse_dcf={k: dict(solved=v.get('solved'), within_defended_bounds=v.get('within_defended_bounds')) for k, v in res['reverse_dcf'].items()},
        flip_scenario=[dict(name=f['name'], growth_shift=f['growth_shift'], per_share=f['per_share']) for f in res['flip_scenario']],
        comps=dict(nvda_pe=res['comps']['nvda']['pe'], nvda_ev_ebit=res['comps']['nvda']['ev_ebit'],
                   peers=[dict(ticker=p['ticker'], pe=p.get('pe'), ev_ebit=p.get('ev_ebit'), disposition=p['disposition']) for p in res['comps']['peers']],
                   implied=res['comps']['implied']),
        limitations=[
            'The model values the equity at the pro-forma opening date (25 Jan 2026) with all FY2027E cash flows ahead; the 23 Sep 2026 price is eight months later. Rolling the value forward at the cost of equity would add about 8% before the distributions paid since (about 1% of value).',
            'FY2027E is a 53-week year (14-week Q4); the base carries the extra week into later years (about -$2 per share if normalised).',
            'SBC is added back as a non-cash charge; the toggle shows the cash-cost alternative.',
            'The $24.9bn of notes issued in June 2026 sit outside the opening balance sheet; they change the bridge only through timing, which the consistent (Jan 2026) bridge avoids.',
            'Peer multiples use trailing GAAP figures; both peers carry large acquired-intangible amortisation, which depresses their GAAP earnings and inflates their multiples.',
        ],
        run=res['run'], source_map='output/visible_output.md and docs/evidence-ledger.csv',
    )


def main():
    if '--break' in sys.argv:
        pf.demo_break()
        return
    res = run_analysis()
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, 'visible_output.json'), 'w') as fh:
        json.dump(visible_output_json(res), fh, indent=2)
    with open(os.path.join(OUT_DIR, 'analysis_full.json'), 'w') as fh:
        json.dump(res, fh, indent=1, default=str)
    with open(os.path.join(OUT_DIR, 'visible_output.md'), 'w') as fh:
        fh.write(to_markdown(res))
    r = res['recommendation']
    print(f"NVIDIA (NVDA) as of {res['decision']['valuation_date']}: price ${res['price']:,.2f}")
    print(f"Value per share: base ${res['per_share']:,.2f} | low ${r['range_low']:,.2f} | high ${r['range_high']:,.2f} | FCFE cross-check ${res['fcfe_cross_check']['per_share']:,.2f}")
    print(f"WACC {res['wacc']['wacc']:.2%} | terminal share {res['dcf']['terminal_share']:.1%} | checks {'all pass' if res['valid'] else 'FAILED ' + str(res['checks_failed'])}")
    print(f"Action: {r['action']}")
    print(f"Wrote output/visible_output.json, output/visible_output.md, output/analysis_full.json")


if __name__ == '__main__':
    main()
