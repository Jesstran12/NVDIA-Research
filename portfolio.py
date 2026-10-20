"""Meridian Foundation Reserve: baseline portfolios.

Standard library only. Edit the inputs at the top; everything below is computed from them.
Run: python3 portfolio.py
"""

import math

# ---------------------------------------------------------------- editable inputs
# sleeve: (expected return %, volatility %, reserve-eligible)
SLEEVES = {
    "Treasury bills":             (3.5,  0.5, True),
    "Treasury 10-year note":      (4.3,  7.0, True),
    "Investment-grade bond fund": (5.0,  6.0, False),
    "Global equity index fund":   (8.0, 16.0, False),
}

# rows and columns in the same order as SLEEVES
CORRELATION = [
    [1.00,  0.10, 0.05,  0.00],
    [0.10,  1.00, 0.80, -0.10],
    [0.05,  0.80, 1.00,  0.25],
    [0.00, -0.10, 0.25,  1.00],
]

OBJECTIVE_RETURN = 6.5  # percent

# benchmark, percent weights (sleeves left out are 0)
BENCHMARK = {"Investment-grade bond fund": 40, "Global equity index fund": 60}
# ---------------------------------------------------------------- end of inputs


def validate_correlation(corr, n):
    """Raise ValueError unless corr is n x n, symmetric, unit-diagonal and within [-1, 1]."""
    if len(corr) != n or any(len(row) != n for row in corr):
        raise ValueError(f"Correlation table must be {n} x {n}, one row and column per sleeve")
    for i in range(n):
        if abs(corr[i][i] - 1) > 1e-9:
            raise ValueError(f"Correlation diagonal must be 1.00; row {i + 1} has {corr[i][i]}")
        for j in range(n):
            if not -1 <= corr[i][j] <= 1:
                raise ValueError(f"Correlation [{i + 1}][{j + 1}] = {corr[i][j]} is outside -1 to 1")
            if abs(corr[i][j] - corr[j][i]) > 1e-9:
                raise ValueError(f"Correlation table is not symmetric: [{i + 1}][{j + 1}] = "
                                 f"{corr[i][j]} but [{j + 1}][{i + 1}] = {corr[j][i]}")


def covariance_matrix(vols, corr):
    """Covariance[i][j] = correlation[i][j] x vol[i] x vol[j], in decimal units."""
    v = [x / 100 for x in vols]
    return [[corr[i][j] * v[i] * v[j] for j in range(len(v))] for i in range(len(v))]


def benchmark_weights(names, benchmark):
    return [benchmark.get(name, 0) / 100 for name in names]


def equal_weights(n):
    return [1 / n] * n


def inverse_vol_weights(vols):
    raw = [1 / v for v in vols]
    total = sum(raw)
    return [r / total for r in raw]


def expected_return(weights, returns):
    """Percent."""
    return sum(w * r for w, r in zip(weights, returns))


def volatility(weights, cov):
    """Percent: sqrt(w' Cov w)."""
    n = len(weights)
    variance = sum(weights[i] * cov[i][j] * weights[j] for i in range(n) for j in range(n))
    return math.sqrt(variance) * 100


def reserve_eligible_weight(weights, eligible):
    """Percent of the portfolio in reserve-eligible sleeves."""
    return sum(w for w, e in zip(weights, eligible) if e) * 100


def main():
    names = list(SLEEVES)
    returns = [SLEEVES[n][0] for n in names]
    vols = [SLEEVES[n][1] for n in names]
    eligible = [SLEEVES[n][2] for n in names]

    unknown = set(BENCHMARK) - set(names)
    if unknown:
        raise SystemExit(f"Benchmark names unknown sleeves: {unknown}")
    try:
        validate_correlation(CORRELATION, len(names))
    except ValueError as err:
        raise SystemExit(f"Refusing to run: {err}")

    cov = covariance_matrix(vols, CORRELATION)
    portfolios = {
        "Benchmark 40/60": benchmark_weights(names, BENCHMARK),
        "Equal weight": equal_weights(len(names)),
        "Inverse volatility": inverse_vol_weights(vols),
    }

    print(f"Objective return: {OBJECTIVE_RETURN:.2f}%\n")
    for label, weights in portfolios.items():
        er = expected_return(weights, returns)
        print(label)
        for name, w in zip(names, weights):
            print(f"  {name:<28} {w * 100:5.1f}%")
        print(f"  {'Weights total':<28} {sum(weights) * 100:5.1f}%")
        print(f"  Expected return   {er:6.2f}%")
        print(f"  Volatility        {volatility(weights, cov):6.2f}%")
        print(f"  Reserve-eligible  {reserve_eligible_weight(weights, eligible):6.1f}%  "
              "(bills + 10-year note)")
        print(f"  Meets {OBJECTIVE_RETURN}% objective: "
              f"{'yes' if er >= OBJECTIVE_RETURN else 'no'}\n")


if __name__ == "__main__":
    main()
