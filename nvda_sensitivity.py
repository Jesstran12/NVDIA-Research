"""Lab 11 — one-at-a-time sensitivity of the NVIDIA pro-forma (nvda_proforma.py).

For each driver, the whole linked five-year model is rerun at its lower, base and
higher values, changing only that driver in the stated years. Every other
independent assumption is reset to a fresh copy of the base before each run;
linked quantities (revenue, working capital, cash, equity) recalculate.

Outputs, the same for every run:
  * FY2031E operating income
  * FY2031E free cash flow to equity (FCFE — the model values equity, not the firm)
  * value per share (FCFE discounted at the model's cost of equity)

A run whose balance or cash-floor check fails is flagged INVALID and left out of
the spans. The base is restored and rerun at the end and compared with the first run.

Ranges are the student's own (see nvda-sensitivity.md); this script does not choose them.
Usage:  python3 nvda_sensitivity.py      (from the NVDIA-Research folder)
USD millions unless stated. Learning demonstration, not investment advice.
"""
import contextlib
import copy
import io

import nvda_proforma as m

# Independent inputs this script may change, and a frozen copy of their base values.
INPUTS = ['growth', 'gross_margin']
BASE = {k: copy.deepcopy(getattr(m, k)) for k in INPUTS}
YEARS = ['FY2027E', 'FY2028E', 'FY2029E', 'FY2030E', 'FY2031E']
TOL = 0.5   # USD millions: the model's own balance tolerance, also used for the restored-base check


def shifted(path, years, d):
    """Copy of a five-year path with d (percentage points as a fraction) added to the listed year indexes."""
    return [x + d if i in years else x for i, x in enumerate(path)]


# ---------------------------------------------------------------------------
# Drivers and ranges: lower / base / higher, as the same percentage-point shift to each affected year.
# Driver 1 — AI Data Center demand (about 90% of revenue) -> revenue growth, FY2028E-FY2031E, +/-5 pp.
#   FY2027E (guidance + Q4 judgment) is held at base.
# Driver 2 — CUDA pricing power -> gross margin, FY2027E-FY2031E, +/-3 pp.
# Ranges and reasons: nvda-sensitivity.md (Locked Changed-Input Record).
# ---------------------------------------------------------------------------
DRIVERS = [
    dict(name='Revenue growth FY28-31 (AI Data Center demand)', key='growth', years=[1, 2, 3, 4], step=0.05),
    dict(name='Gross margin FY27-31 (CUDA pricing power)', key='gross_margin', years=[0, 1, 2, 3, 4], step=0.03),
]


def run(changes):
    """Fresh base copy -> apply changes -> full rerun -> checks -> valuation. Base is always restored."""
    for k in INPUTS:
        setattr(m, k, copy.deepcopy(BASE[k]))
    for k, v in changes.items():
        setattr(m, k, copy.deepcopy(v))
    try:
        years = m.project()
        result = dict(years=years, inputs={k: copy.deepcopy(getattr(m, k)) for k in INPUTS})
        try:
            with contextlib.redirect_stdout(io.StringIO()):   # m.value prints "balanced, 5 year(s)"
                v = m.value(years)
            result.update(valid=True, check='pass', per_share=v['per_share'], terminal_share=v['terminal_share'])
        except ValueError as e:
            result.update(valid=False, check=f'INVALID: {e}', per_share=None, terminal_share=None)
    finally:
        for k in INPUTS:
            setattr(m, k, copy.deepcopy(BASE[k]))
    last = result['years'][-1]
    result['op_income'] = last['operating_income']
    result['fcfe'] = last['fcfe']
    result['max_check'] = max(abs(y[c]) for y in result['years']
                              for c in ('check_balance', 'check_cash', 'check_ppe', 'check_debt', 'check_floor'))
    return result


def fmt(x, spec='{:,.1f}'):
    return 'n/a' if x is None else spec.format(x)


def signed(x, b, spec='{:+,.1f}'):
    return 'n/a' if x is None or b is None else spec.format(x - b)


def main():
    first_base = run({})
    print('NVIDIA pro-forma — one-at-a-time sensitivity (USD millions; value per share in USD)')
    print(f"Base: FY2031E operating income {first_base['op_income']:,.1f} | FY2031E FCFE {first_base['fcfe']:,.1f} | "
          f"value per share ${first_base['per_share']:,.2f} | checks {first_base['check']} "
          f"(largest check residual {first_base['max_check']:.3f})")
    print(f"Base growth path: {' / '.join(f'{g:.1%}' for g in BASE['growth'])}")
    print(f"Base gross margin path: {' / '.join(f'{g:.1%}' for g in BASE['gross_margin'])}\n")

    spans = []
    for d in DRIVERS:
        affected = ', '.join(YEARS[i] for i in d['years'])
        print(f"== {d['name']}: {-d['step'] * 100:+.0f} / 0 / {d['step'] * 100:+.0f} pp applied to {affected}; "
              f"all other inputs at base")
        results = []
        for label, dd in (('lower', -d['step']), ('base', 0.0), ('higher', d['step'])):
            path = shifted(BASE[d['key']], d['years'], dd)
            print(f"  {label:<7} {d['key']:<13} " + ' / '.join(f'{x:.1%}' for x in path))
            results.append((label, dd, run({d['key']: path})))
        print()
        b = next(r for label, _, r in results if label == 'base')
        head = f"{'case':<8}{'shift':>9}{'FY31 op income':>16}{'change':>11}{'FY31 FCFE':>13}{'change':>11}{'$/share':>10}{'change':>9}  checks"
        print(head)
        print('-' * len(head))
        for label, v, r in results:
            print(f"{label:<8}{v * 100:>+7.0f}pp{r['op_income']:>16,.1f}{signed(r['op_income'], b['op_income']):>11}"
                  f"{r['fcfe']:>13,.1f}{signed(r['fcfe'], b['fcfe']):>11}"
                  f"{fmt(r['per_share'], '{:,.2f}'):>10}{signed(r['per_share'], b['per_share'], '{:+,.2f}'):>9}  {r['check']}")
        # Trace lines: the path from the changed input through the statements, per case.
        print('\n  trace (USD millions)        ' + ''.join(f'{label:>14}' for label, _, _ in results))
        for tlabel, yi, key in [('FY2028E revenue', 1, 'revenue'), ('FY2031E revenue', 4, 'revenue'),
                                ('FY2031E gross profit', 4, 'gross_profit'), ('FY2031E opex', 4, 'opex'),
                                ('FY2031E operating income', 4, 'operating_income'),
                                ('FY2031E net income', 4, 'net_income'),
                                ('FY2031E working-capital build', 4, 'delta_wc'),
                                ('FY2031E FCFE', 4, 'fcfe')]:
            print(f'  {tlabel:<28}' + ''.join(f"{r['years'][yi][key]:>14,.1f}" for _, _, r in results))
        valid = [r for _, _, r in results if r['valid']]
        invalid = [label for label, _, r in results if not r['valid']]
        span = dict(name=d['name'],
                    op=max(r['op_income'] for r in valid) - min(r['op_income'] for r in valid),
                    fcfe=max(r['fcfe'] for r in valid) - min(r['fcfe'] for r in valid),
                    ps=max(r['per_share'] for r in valid) - min(r['per_share'] for r in valid))
        spans.append(span)
        note = f"  (invalid, excluded: {', '.join(invalid)})" if invalid else ''
        print(f"\n  span (max - min over valid runs): op income {span['op']:,.1f} | FCFE {span['fcfe']:,.1f} | "
              f"$/share {span['ps']:,.2f}{note}\n")

    print('== Output spans over these ranges (a wider input range gives a wider span)')
    print(f"{'driver':<50}{'op income':>12}{'FCFE':>12}{'$/share':>10}")
    for s in spans:
        print(f"{s['name']:<50}{s['op']:>12,.1f}{s['fcfe']:>12,.1f}{s['ps']:>10,.2f}")

    # Restore the base and rerun: must match the first run.
    for k in INPUTS:
        setattr(m, k, copy.deepcopy(BASE[k]))
    restored = run({})
    same_inputs = restored['inputs'] == first_base['inputs']
    diffs = [abs(restored['op_income'] - first_base['op_income']), abs(restored['fcfe'] - first_base['fcfe']),
             abs(restored['per_share'] - first_base['per_share'])]
    ok = same_inputs and max(diffs) <= TOL
    print(f"\n== Restored base: inputs identical {same_inputs}; op income {restored['op_income']:,.1f}, "
          f"FCFE {restored['fcfe']:,.1f}, ${restored['per_share']:,.2f}; largest difference from first run "
          f"{max(diffs):.6f} -> {'PASS' if ok else 'FAIL'} (tolerance {TOL})")


if __name__ == '__main__':
    main()
