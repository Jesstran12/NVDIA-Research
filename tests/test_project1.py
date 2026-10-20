"""Project 1 validation suite: known answers, articulation, boundaries, monotonicity, bridge, loud failure.

Run from the repository root:  python -m pytest -q
Every test states its expected result before the run; a failing test stays visible, never patched.
"""
import contextlib
import copy
import io
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import engine as e            # noqa: E402
import nvda_proforma as pf    # noqa: E402
import proforma as abg        # noqa: E402


# --- known answers -----------------------------------------------------------------------------
def test_training_case_dcf_known_answer():
    """Lab 05 training case: FCFF 100, growth 8/6/5/4/3, WACC 10%, g 3%, cash 50, debt 300, 50 shares."""
    fcffs, f = [], 100.0
    for g in (0.08, 0.06, 0.05, 0.04, 0.03):
        f *= 1 + g
        fcffs.append(f)
    d = e.dcf(fcffs, 0.10, 0.03, 50.0, 300.0, 50.0)
    assert [round(x, 4) for x in fcffs] == [108.0, 114.48, 120.204, 125.0122, 128.7625]
    assert round(d['pv_explicit'], 4) == 448.4408
    assert round(d['terminal_value'], 4) == 1894.6486
    assert round(d['pv_terminal'], 4) == 1176.4277
    assert round(d['enterprise_value'], 4) == 1624.8685
    assert round(d['equity_value'], 4) == 1374.8685
    assert round(d['per_share'], 4) == 27.4974
    assert round(d['terminal_share'], 4) == 0.7240


def test_training_case_wacc_11_percent():
    """Lab 05 changed-input: WACC 10% -> 11% must give about 23.41 per share."""
    fcffs, f = [], 100.0
    for g in (0.08, 0.06, 0.05, 0.04, 0.03):
        f *= 1 + g
        fcffs.append(f)
    assert round(e.dcf(fcffs, 0.11, 0.03, 50.0, 300.0, 50.0)['per_share'], 2) == 23.41


def test_abg_engine_known_answer():
    """Lab 09: the ABG engine must give $291.75 per share and about 80% of value after 2030."""
    years = abg.project()
    with contextlib.redirect_stdout(io.StringIO()):
        v = abg.value(years)
    assert round(v['per_share'], 2) == 291.75
    assert round(years[0]['revenue'], 1) == 18323.0 and round(years[0]['fcfe'], 1) == 211.4
    assert round(years[-1]['cash'], 1) == 719.8
    assert 0.79 < v['terminal_share'] < 0.81


def test_nvda_fcfe_base_reproduced_through_wrapper():
    """Lab 10 base case: $123.05 per share on FCFE at 12% / 3%, reproduced through engine.run_proforma."""
    v = e.valuation({})
    assert round(v['fcfe']['per_share'], 2) == 123.05
    assert round(v['years'][-1]['net_income'], 1) == 301173.2


# --- articulation and base-year reconciliation -------------------------------------------------
def test_base_checks_all_pass():
    v = e.valuation({})
    assert v['valid'] and v['checks_failed'] == [] and v['checks_warned'] == []


def test_statements_articulate_every_year_under_shocks():
    for shock in ({}, {'growth_shift': -0.25}, {'gross_margin_shift': -0.15, 'opex_shift': 0.06}, {'fy27_revenue_pct': 0.10}):
        v = e.valuation(shock)
        for y in v['years']:
            assert abs(y['check_balance']) <= 0.5
            assert abs(y['check_cash']) <= 0.5
            assert abs(y['check_ppe']) <= 0.5
            assert abs(y['check_debt']) <= 0.5


def test_opening_balance_sheet_reconciles_to_filing():
    rec = e.opening_reconciliation()
    assert all(abs(g) <= 0.5 for g in rec['gaps'].values())


def test_broken_cash_line_is_refused():
    """Lab 10 --break: cash typed instead of linked; assert_balanced must raise with the cash-flow fingerprint."""
    years = pf.project(1)
    broken = dict(years[0])
    broken['cash'] = pf.opening['cash']
    broken['total_assets'] = (broken['cash'] + broken['securities'] + broken['receivables'] + broken['inventory']
                              + broken['ppe'] + broken['other_assets'])
    with pytest.raises(ValueError, match='does not balance'):
        pf.assert_balanced([broken])


# --- boundaries, monotonicity, bridge ----------------------------------------------------------
def test_terminal_growth_at_or_above_wacc_is_refused():
    assert e.dcf([1, 1, 1, 1, 1], 0.10, 0.10, 0, 0, 1) is None
    assert e.dcf([1, 1, 1, 1, 1], 0.10, 0.11, 0, 0, 1) is None


def test_value_falls_as_cost_of_equity_rises():
    values = [e.valuation({'cost_of_equity': r})['per_share'] for r in (0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16)]
    assert all(a > b for a, b in zip(values, values[1:]))


def test_value_rises_with_terminal_growth_and_revenue_growth():
    values = [e.valuation({'terminal_growth': g})['per_share'] for g in (0.0, 0.01, 0.02, 0.03, 0.04)]
    assert all(a < b for a, b in zip(values, values[1:]))
    values = [e.valuation({'growth_shift': s})['per_share'] for s in (-0.25, -0.10, 0.0, 0.10, 0.25)]
    assert all(a < b for a, b in zip(values, values[1:]))


def test_bridge_reconciles_and_uses_diluted_point_in_time_shares():
    v = e.valuation({})
    d = v['dcf']
    assert abs(d['enterprise_value'] + d['cash'] + d['other_assets'] - d['debt'] - d['equity_value']) < 1e-6
    assert d['shares'] == 24100.0 + (24285.0 - 24190.0)
    assert d['cash'] == 10605.0 + 39065.0 and d['debt'] == 999.0 + 7469.0


def test_base_restored_after_shocked_runs():
    before = {k: copy.deepcopy(getattr(pf, k)) for k in e.PF_KEYS}
    e.valuation({'growth_shift': 0.25, 'gross_margin_shift': -0.15, 'cost_of_equity': 0.16})
    e.one_at_a_time(scale=0.25)
    after = {k: copy.deepcopy(getattr(pf, k)) for k in e.PF_KEYS}
    assert before == after
    assert round(e.valuation({})['per_share'], 6) == round(e.valuation({})['per_share'], 6)


def test_out_of_bounds_input_is_clamped_and_reported():
    v = e.valuation({'cost_of_equity': 0.50})
    assert v['clamped'] and v['inputs']['cost_of_equity'] == 0.16


# --- reverse DCF, cases, comps -------------------------------------------------------------------
def test_reverse_dcf_growth_shift_reproduces_the_price():
    r = e.solve('growth_shift')
    assert r['reachable']
    assert abs(e.valuation({'growth_shift': r['solved']})['per_share'] - e.MARKET['price']) < 0.01


def test_cases_are_ordered_and_valid():
    c = e.cases()
    assert all(x['valid'] for x in c)
    assert c[0]['per_share'] < c[1]['per_share'] < c[2]['per_share']


def test_comps_policy_consistency():
    c = e.comps()
    used = [p for p in c['peers'] if 'pe' in p]
    assert {p['ticker'] for p in used} == {'AMD', 'AVGO'}
    for p in used:
        assert p['enterprise_value'] == pytest.approx(p['market_cap'] + next(q for q in e.PEERS if q['ticker'] == p['ticker'])['debt']
                                                       - next(q for q in e.PEERS if q['ticker'] == p['ticker'])['cash'])
        assert p['pe'] == pytest.approx(p['price'] / p['ttm_eps'])
    amd = next(p for p in used if p['ticker'] == 'AMD')
    assert not amd['pe_meaningful']   # 157x: reported, marked not meaningful under the pre-declared rule
    assert c['nvda']['pe'] == pytest.approx(225.51 / 7.91, rel=1e-6)
