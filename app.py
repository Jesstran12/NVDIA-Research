"""NVIDIA pro-forma workbench — the semi-adjustable product over analysis.py / engine.py.

Locked: the three-statement engine, the provenance (opening balance sheet, bridge), the checks.
Exposed: the nine bounded drivers in the sidebar, three toggles, a base reset and a stress mode
that unlocks the bounds and flags every result outside them.
Run:  streamlit run app.py
The frozen tab renders output/visible_output.json (written by `python analysis.py`) without recomputing it.
"""
import json
import os

import pandas as pd
import streamlit as st

import analysis
import engine as e

HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN = os.path.join(HERE, 'output', 'visible_output.json')

st.set_page_config(page_title='NVDA pro-forma workbench', layout='wide')


def fmt_driver(d, v):
    return f'{v * 100:+.1f} pp' if d['fmt'] == 'pp' else f'{v * 100:.2f}%'


def init_state():
    for d in e.DRIVERS:
        st.session_state.setdefault(d['key'], float(d['base']))
    for t in e.TOGGLES:
        st.session_state.setdefault(t['key'], bool(t['base']))
    st.session_state.setdefault('stress', False)


def reset_base():
    for d in e.DRIVERS:
        st.session_state[d['key']] = float(d['base'])
    for t in e.TOGGLES:
        st.session_state[t['key']] = bool(t['base'])
    st.session_state['stress'] = False


init_state()

# ---------------------------------------------------------------------------
# Sidebar: the driver panel
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title('Driver panel')
    st.caption('Every control is bounded; the bound and its reason are in the assumption record tab. '
               'Move one driver, read the result against the restored base.')
    st.button('Reset to base', on_click=reset_base, type='primary', width='stretch')
    st.checkbox('Stress mode: unlock the bounds (results flagged, not defensible)', key='stress')
    for d in e.DRIVERS:
        lo, hi = (e.STRESS_RANGES[d['key']] if st.session_state['stress'] else (d['lo'], d['hi']))
        scale = 100.0
        cur = float(st.session_state[d['key']])
        cur = min(max(cur, lo), hi)
        st.session_state[d['key']] = cur
        val = st.slider(d['label'], min_value=lo * scale, max_value=hi * scale, value=cur * scale,
                        step=d['step'] * scale, format='%.2f', key=f"slider_{d['key']}",
                        help=f"{d['basis']}: {d['value_note']}. Bounds: {d['bound_reason']}")
        st.session_state[d['key']] = val / scale
    st.markdown('**Conventions**')
    for t in e.TOGGLES:
        st.checkbox(t['label'], key=t['key'], help=t['reason'])

inputs = {d['key']: st.session_state[d['key']] for d in e.DRIVERS} | {t['key']: st.session_state[t['key']] for t in e.TOGGLES}
live = e.valuation(inputs, allow_out_of_bounds=st.session_state['stress'])
base = e.valuation({})
changed = [d for d in e.DRIVERS if abs(inputs[d['key']] - d['base']) > 1e-12] + \
          [t for t in e.TOGGLES if inputs[t['key']] != t['base']]

# ---------------------------------------------------------------------------
# Header: the answer, the price, the checks
# ---------------------------------------------------------------------------
st.title('NVIDIA (NVDA) — pro-forma workbench')
st.caption(f"Valuation date {e.MARKET['price_date']} · price ${e.MARKET['price']:,.2f} · USD millions, per-share in USD · "
           'FCFF DCF driven by the Lab 10 three-statement pro-forma · learning demonstration, not investment advice')

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric('Value per share (this run)', f"${live['per_share']:,.2f}" if live['per_share'] else 'refused',
          None if not live['per_share'] else f"{live['per_share'] - base['per_share']:+,.2f} vs base")
c2.metric('Base case (restored)', f"${base['per_share']:,.2f}")
c3.metric('Market price', f"${e.MARKET['price']:,.2f}", f"{live['upside']:+.1%} value vs price" if live['upside'] is not None else None)
c4.metric('WACC', f"{live['wacc']['wacc']:.2%}")
c5.metric('Checks', 'all pass' if live['valid'] else f"{len(live['checks_failed'])} FAILED",
          delta=None if live['valid'] else 'red', delta_color='inverse')

if changed:
    st.info('Changed from base: ' + '; '.join(
        (f"{d['label']} = {fmt_driver(d, inputs[d['key']])}" if 'fmt' in d else f"{d['label']} = {inputs[d['key']]}") for d in changed))
else:
    st.success('All drivers at base. The value above is the restored base case.')

st.subheader('Checks panel')
cols = st.columns(3)
for i, c in enumerate(live['checks']):
    box = cols[i % 3]
    if c['status'] == 'pass':
        box.success(f"**{c['name']}** — {c['detail']}")
    elif c['status'] == 'warn':
        box.warning(f"**{c['name']}** — {c['detail']}")
    else:
        box.error(f"**{c['name']}** — {c['detail']}")
if not live['valid']:
    st.error('The model is telling you what it believes: this input combination is incoherent or outside the evidence. '
             'The value above is shown only if the arithmetic allows it; it is not defensible. Press **Reset to base** to recover.')

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tabs = st.tabs(['Statements', 'FCFF, WACC, bridge', 'Sensitivity', 'Grid and cases', 'Reverse DCF and comps',
                'Assumption record', 'Frozen output'])

years = live['years']
cols_y = [f"FY{y['year']}E" for y in years]


def table(rows, keys_labels, nd=0):
    data = {label: [f'{(rows_i[key] if abs(rows_i[key]) >= 0.05 else 0.0):,.{nd}f}' for rows_i in rows] for label, key in keys_labels}
    return pd.DataFrame(data, index=cols_y).T


def fmt_df(df, spec):
    """Format the columns of a DataFrame as strings (no matplotlib or Styler needed)."""
    out = df.copy()
    for col, f in spec.items():
        if col in out.columns:
            out[col] = out[col].map(lambda x: 'n/a' if x is None or (isinstance(x, float) and x != x) else f.format(x))
    return out


with tabs[0]:
    st.markdown('**Income statement**')
    st.dataframe(table(years, [('Revenue', 'revenue'), ('Gross profit', 'gross_profit'), ('Operating expenses', 'opex'),
                              ('Operating income', 'operating_income'), ('Interest income', 'interest_income'),
                              ('Interest expense', 'interest_expense'), ('Tax', 'tax'), ('Net income', 'net_income')]), width='stretch')
    st.markdown('**Balance sheet**')
    st.dataframe(table(years, [('Cash (the result)', 'cash'), ('Marketable securities', 'securities'), ('Receivables', 'receivables'),
                              ('Inventory', 'inventory'), ('PP&E and intangibles', 'ppe'), ('Other assets', 'other_assets'),
                              ('Total assets', 'total_assets'), ('Payables', 'payables'), ('Accrued', 'accrued'), ('Notes', 'debt'),
                              ('Commercial paper', 'revolver'), ('Other liabilities', 'other_liabilities'), ('Equity', 'equity'),
                              ('Total liabilities & equity', 'total_liabilities_equity')]), width='stretch')
    st.markdown('**Cash flow to equity and the check block**')
    st.dataframe(table(years, [('Net income', 'net_income'), ('+ D&A', 'da'), ('+ SBC', 'sbc'), ('− Capex', 'capex'),
                              ('− Working-capital build', 'delta_wc'), ('− Notes repaid', 'paydown'), ('FCFE', 'fcfe'),
                              ('− Buybacks and dividends', 'buyback'), ('Assets − liabilities − equity', 'check_balance'),
                              ('Cash: BS vs CF', 'check_cash'), ('PP&E roll', 'check_ppe'), ('Debt roll', 'check_debt')], nd=1), width='stretch')
    a = live['assumptions']
    st.caption('Paths this run: growth ' + ' / '.join(f'{g:.1%}' for g in a['growth']) + ' · gross margin ' +
               ' / '.join(f'{g:.1%}' for g in a['gross_margin']) + ' · opex ratio ' + ' / '.join(f'{g:.1%}' for g in a['opex_ratio']))

with tabs[1]:
    st.dataframe(table(live['fcff_rows'], [('EBIT', 'ebit'), ('NOPAT', 'nopat'), ('+ D&A', 'da'), ('+ SBC add-back', 'sbc_addback'),
                                           ('− Capex', 'capex'), ('− Working-capital build', 'delta_wc'), ('FCFF', 'fcff')]), width='stretch')
    w, d, b = live['wacc'], live['dcf'], live['bridge']
    left, right = st.columns(2)
    with left:
        st.markdown('**WACC**')
        st.table(pd.DataFrame({'value': [f"{w['cost_of_equity']:.2%}", f"{w['cost_of_debt_pretax']:.2%} / {w['cost_of_debt_after_tax']:.2%}",
                                         f"{w['weight_equity']:.2%} / {w['weight_debt']:.2%}", f"{w['wacc']:.2%}"]},
                              index=['Cost of equity', 'Cost of debt pre / after tax', 'Weights equity / debt', 'WACC']))
    with right:
        st.markdown(f"**Bridge — {b['balance_sheet']['label']}**")
        if d:
            st.table(pd.DataFrame({'USD millions': [f"{d['pv_explicit']:,.0f}", f"{d['pv_terminal']:,.0f} ({d['terminal_share']:.1%} of EV)",
                                                    f"{d['enterprise_value']:,.0f}", f"{b['cash_and_marketable_debt']:,.0f}",
                                                    f"{b['marketable_equity']:,.0f}", f"{b['debt']:,.0f}", f"{d['equity_value']:,.0f}",
                                                    f"{d['shares']:,.0f}", f"${d['per_share']:,.2f}"]},
                                  index=['PV explicit FCFF', 'PV terminal value', 'Enterprise value', '+ cash and marketable debt securities',
                                         '+ marketable equity securities', '− debt (carrying)', 'Equity value', 'Diluted shares (m)', 'Value per share']))
        else:
            st.error('No valuation: terminal growth is at or above the discount rate.')
    if live['fcfe']:
        st.caption(f"Lab 10 FCFE cross-check at this run's cost of equity and terminal growth: ${live['fcfe']['per_share']:,.2f} per share on 24,100m shares.")


@st.cache_data(show_spinner='Rerunning the model at each bound…')
def cached_sensitivity(inputs_key):
    return e.one_at_a_time(dict(inputs_key))


with tabs[2]:
    st.markdown('One driver at a time at its defended bounds, everything else at **this run\'s** values; '
                'the span is max − min of value per share. Over these ranges only: a wider bound gives a wider span.')
    key = tuple(sorted((k, v) for k, v in inputs.items()))
    sens = cached_sensitivity(key)
    rows = [dict(driver=r['label'], low=r['lo']['per_share'], high=r['hi']['per_share'], span=r['span_per_share'],
                 span_op_income=r['span_op_income'], span_fcff=r['span_fcff']) for r in sens['rows']]
    df = pd.DataFrame(rows).set_index('driver')
    st.bar_chart(df['span'], horizontal=True, width='stretch')
    st.dataframe(fmt_df(df, {'low': '{:,.2f}', 'high': '{:,.2f}', 'span': '{:,.2f}', 'span_op_income': '{:,.0f}', 'span_fcff': '{:,.0f}'}),
                 width='stretch')
    if changed:
        st.markdown('**Trace of this run against the restored base (FY2031E, USD millions)**')
        bl, lv = base['years'][-1], live['years'][-1]
        bf, lf = base['fcff_rows'][-1], live['fcff_rows'][-1]
        trace = pd.DataFrame({'base': [bl['revenue'], bl['gross_profit'], bl['opex'], bl['operating_income'], bl['net_income'], bl['delta_wc'], bf['fcff'], base['per_share']],
                              'this run': [lv['revenue'], lv['gross_profit'], lv['opex'], lv['operating_income'], lv['net_income'], lv['delta_wc'], lf['fcff'], live['per_share'] or float('nan')]},
                             index=['Revenue', 'Gross profit', 'Opex', 'Operating income', 'Net income', 'Working-capital build', 'FCFF', 'Value per share'])
        trace['change'] = trace['this run'] - trace['base']
        st.dataframe(fmt_df(trace, {c: '{:,.1f}' for c in trace.columns}), width='stretch')

with tabs[3]:
    g = e.grid(base_inputs=inputs)
    gdf = pd.DataFrame(g['cells'], index=[f'{r:.0%}' for r in g['rates']], columns=[f'g = {x:.0%}' for x in g['growths']])
    st.markdown('**Cost of equity × terminal growth, $ per share** (other drivers at this run\'s values; invalid cells are blank)')
    st.dataframe(fmt_df(gdf, {c: '{:,.1f}' for c in gdf.columns}).replace('n/a', 'invalid'), width='stretch')
    st.markdown('**Causal cases** (each a full rerun from base; never a sum of single shocks)')
    cs = e.cases()
    st.dataframe(fmt_df(pd.DataFrame([dict(case=c['name'], story=c['story'], per_share=c['per_share'], fy2031_revenue=c['fy2031_revenue'],
                                           terminal_share=c['terminal_share'], checks='pass' if c['valid'] else 'FAIL') for c in cs]).set_index('case'),
                        {'per_share': '${:,.2f}', 'fy2031_revenue': '{:,.0f}', 'terminal_share': '{:.1%}'}), width='stretch')

with tabs[4]:
    st.markdown(f"**What ${e.MARKET['price']:,.2f} assumes** — one driver solved by bisection, all others at base; "
                'a value outside the defended bounds is reported because the gap is the finding.')
    rd = e.reverse_dcf()
    st.dataframe(pd.DataFrame([dict(driver=next(x for x in e.DRIVERS if x['key'] == k)['label'],
                                    implied=('not reachable' if r.get('solved') is None else fmt_driver(next(x for x in e.DRIVERS if x['key'] == k), r['solved'])),
                                    inside_bounds='yes' if r.get('within_defended_bounds') else 'no') for k, r in rd.items()]).set_index('driver'),
                 width='stretch')
    c = e.comps()
    st.markdown('**Comparable companies** — ' + c['policy']['frozen'])
    with st.expander('Peer policy (frozen before the numbers)'):
        for rule in c['policy']['rules']:
            st.markdown(f'- {rule}')
    n = c['nvda']
    prow = [dict(company='NVIDIA (target)', disposition='—', price=n['price'], ttm_eps=n['ttm_eps'], ttm_ebit=n['ttm_ebit'],
                 op_margin=n['operating_margin'], ev=n['enterprise_value'], pe=n['pe'], ev_ebit=n['ev_ebit'])]
    for p in c['peers']:
        if 'pe' in p:
            prow.append(dict(company=p['ticker'], disposition=p['disposition'], price=p['price'], ttm_eps=p['ttm_eps'], ttm_ebit=p['ttm_ebit'],
                             op_margin=p['operating_margin'], ev=p['enterprise_value'], pe=p['pe'], ev_ebit=p['ev_ebit']))
    st.dataframe(fmt_df(pd.DataFrame(prow).set_index('company'), {'price': '{:,.2f}', 'ttm_eps': '{:.2f}', 'ttm_ebit': '{:,.0f}', 'op_margin': '{:.1%}',
                                                                  'ev': '{:,.0f}', 'pe': '{:.1f}x', 'ev_ebit': '{:.1f}x'}), width='stretch')
    st.markdown('**NVIDIA value per share implied by each peer multiple** (not meaningful above 100x)')
    st.dataframe(fmt_df(pd.DataFrame(c['implied']).set_index('ticker'), {'pe_implied': '${:,.2f}', 'ev_ebit_implied': '${:,.2f}'})
                 .replace('n/a', 'not meaningful'), width='stretch')
    for p in c['peers']:
        st.caption(f"**{p['ticker']}** — {p['disposition']}: {p['reason']}")

with tabs[5]:
    st.markdown('**Assumption-challenge record** — value · basis · bounds · why · challenge · evidence that would change it')
    st.dataframe(pd.DataFrame([dict(driver=d['label'], base=fmt_driver(d, d['base']), note=d['value_note'], basis=d['basis'],
                                    bounds=f"{fmt_driver(d, d['lo'])} to {fmt_driver(d, d['hi'])}", why_these_bounds=d['bound_reason'],
                                    challenge=d['challenge'], evidence_to_change=d['evidence']) for d in e.DRIVERS]).set_index('driver'),
                 width='stretch', height=420)
    st.markdown('**Locked (not adjustable here):** the three-statement engine and its articulation checks; the opening balance sheet '
                '(FY2026 10-K p. 53); the bridge balance sheets (FY2026 10-K; Q2 FY2027 10-Q); receivable, inventory and payable days; '
                'the Note 11 maturity ladder; the 8,000 cash floor; the 95% payout; the share count. Change those in `nvda_proforma.py` with a new source.')

with tabs[6]:
    if os.path.exists(FROZEN):
        rec = json.loads(open(FROZEN, encoding='utf-8').read())
        st.markdown(f"**Frozen visible output** — written by `python analysis.py` at {rec['run']['timestamp']}, commit `{rec['run']['commit']}`. "
                    'This tab renders the file; it does not recompute anything.')
        st.subheader(rec['decision'])
        st.text(f"As of: {rec['as_of']} · price: ${rec['price']:,.2f} · units: {rec['units']}")
        st.text(f"Recommendation: {rec['recommendation']}")
        st.text(f"Reversal triggers: {rec['reversal_trigger']}")
        st.text(f"Committee ask: {rec['committee_ask']}")
        st.json(rec, expanded=False)
    else:
        st.warning('No output/visible_output.json yet. Run `python analysis.py` first.')
    st.info('The interface cannot establish finance quality; inspect the sources, conventions, tests and the frozen validation record in docs/.')
