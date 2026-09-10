"""Five-year discounted cash flow valuation."""


# Edit these inputs by hand.
STARTING_FCFF = 96895.9  # USD millions; FY2026 CFO - capex + after-tax interest
GROWTH_RATES = [0.08, 0.06, 0.05, 0.04, 0.03]  # PLACEHOLDER: forward-growth forecast unresolved
WACC = 0.10  # PLACEHOLDER: company-specific WACC unresolved
TERMINAL_GROWTH = 0.03  # PLACEHOLDER: long-run macro growth assumption unresolved
NON_OPERATING_CASH = 10605.0  # USD millions; cash and cash equivalents, Jan. 25, 2026
DEBT = 8468.0  # USD millions; net carrying amount, Jan. 25, 2026
DILUTED_SHARES = 24514.0  # millions; FY2026 diluted weighted-average shares


def main():
    if TERMINAL_GROWTH >= WACC:
        print("Error: terminal growth must be less than WACC.")
        return

    fcff = []
    prior_fcff = STARTING_FCFF
    for growth_rate in GROWTH_RATES:
        prior_fcff *= 1 + growth_rate
        fcff.append(prior_fcff)

    present_value_explicit_fcff = sum(
        cash_flow / (1 + WACC) ** year
        for year, cash_flow in enumerate(fcff, start=1)
    )
    terminal_value = fcff[-1] * (1 + TERMINAL_GROWTH) / (WACC - TERMINAL_GROWTH)
    present_value_terminal_value = terminal_value / (1 + WACC) ** len(fcff)
    enterprise_value = present_value_explicit_fcff + present_value_terminal_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    value_per_diluted_share = equity_value / DILUTED_SHARES
    terminal_value_share = present_value_terminal_value / enterprise_value * 100

    for year, cash_flow in enumerate(fcff, start=1):
        print(f"FCFF Year {year}: {cash_flow:.4f}")
    print(f"Present value of explicit FCFF: {present_value_explicit_fcff:.4f}")
    print(f"Terminal value at Year 5: {terminal_value:.4f}")
    print(f"Present value of terminal value: {present_value_terminal_value:.4f}")
    print(f"Enterprise value: {enterprise_value:.4f}")
    print(f"Equity value: {equity_value:.4f}")
    print(f"Value per diluted share: {value_per_diluted_share:.4f}")
    print(f"PV of terminal value as % of enterprise value: {terminal_value_share:.4f}%")


if __name__ == "__main__":
    main()
