"""NVIDIA peer P/E valuation using date-matched GAAP diluted EPS."""


# Valuation convention: February 25, 2026 Nasdaq closing/last prices divided
# by the latest GAAP full-year diluted EPS publicly available on that date.
# Inclusion and exclusion support is recorded in nvda-dcf-inputs.md.
# Use None when a value is missing rather than substituting an adjusted EPS.
TARGET = {
    "name": "NVIDIA (NVDA)",
    "report_name": "NVIDIA",
    "price": 195.56,
    "diluted_eps": 4.90,
}

PEERS = [
    {
        "name": "Advanced Micro Devices (AMD)",
        "report_name": "AMD",
        "price": 210.86,
        "diluted_eps": 2.65,
    },
    {
        "name": "Broadcom (AVGO)",
        "report_name": "Broadcom",
        "price": 332.31,
        "diluted_eps": 4.77,
    },
]


def positive_number(value):
    return isinstance(value, (int, float)) and value > 0


def peer_pe(peer):
    price = peer.get("price")
    diluted_eps = peer.get("diluted_eps")
    if not positive_number(price) or not positive_number(diluted_eps):
        return None
    return price / diluted_eps


def median(values):
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def money(value):
    return "not meaningful" if value is None else f"${value:,.2f}"


def display_name(name):
    """Remove a parenthetical ticker from a company name for report labels."""
    return str(name).split("(", 1)[0].strip()


def ticker(name):
    """Return a parenthetical ticker, falling back to the full supplied name."""
    name = str(name)
    if "(" in name and ")" in name:
        return name.split("(", 1)[1].split(")", 1)[0].strip()
    return name


def unique_peers(peers, target_name):
    target_key = target_name.strip().casefold()
    seen = set()
    result = []
    for peer in peers:
        name = str(peer.get("name", "")).strip()
        key = name.casefold()
        if not key or key == target_key or key in seen:
            continue
        seen.add(key)
        result.append(peer)
    return result


def implied_median_price(peer_results, target_eps):
    multiples = [multiple for _, multiple in peer_results if multiple is not None]
    if not multiples or not positive_number(target_eps):
        return None
    return median(multiples) * target_eps


def print_table(rows):
    """Print a compact two-column report without hard-coding calculated results."""
    check_width = max(len(check) for check, _ in rows)
    result_width = max(len(result) for _, result in rows)
    border = f"+-{'-' * check_width}-+-{'-' * result_width}-+"
    print(border)
    print(f"| {'Check'.ljust(check_width)} | {'Result'.rjust(result_width)} |")
    print(border)
    for check, result in rows:
        print(f"| {check.ljust(check_width)} | {result.rjust(result_width)} |")
    print(border)


def main():
    target_name = str(TARGET.get("name", "Target")).strip() or "Target"
    target_eps = TARGET.get("diluted_eps")
    peers = unique_peers(PEERS, target_name)
    peer_results = [(peer, peer_pe(peer)) for peer in peers]
    valid_multiples = [multiple for _, multiple in peer_results if multiple is not None]

    if not valid_multiples:
        print_table([("Peer valuation", "no usable peers")])
        return

    peer_median = median(valid_multiples)
    full_peer_price = implied_median_price(peer_results, target_eps)
    rows = []
    for peer, multiple in peer_results:
        label = peer.get("report_name") or display_name(peer.get("name"))
        rows.append((f"{label} P/E", "not meaningful" if multiple is None else f"{multiple:.6f}x"))
    rows.append(("Peer median P/E", f"{peer_median:.6f}x"))

    if not positive_number(target_eps) or full_peer_price is None:
        rows.extend([
            (f"{display_name(target_name)} peer-implied range", "not meaningful"),
            (f"{display_name(target_name)} at peer median", "not meaningful"),
        ])
        print_table(rows)
        return

    implied_low = min(valid_multiples) * target_eps
    implied_high = max(valid_multiples) * target_eps
    target_label = TARGET.get("report_name") or display_name(target_name)
    rows.extend([
        (f"{target_label} peer-implied range", f"{money(implied_low)}–{money(implied_high)}"),
        (f"{target_label} at peer median", money(full_peer_price)),
    ])

    # Stress the result by removing the peer with the highest P/E.  This is
    # calculated from the inputs, so the report remains valid if inputs change.
    removed_peer, _ = max(peer_results, key=lambda item: item[1] if item[1] is not None else float("-inf"))
    remaining = [(peer, multiple) for peer, multiple in peer_results if peer is not removed_peer]
    remaining_price = implied_median_price(remaining, target_eps)
    if remaining_price is not None:
        remaining_peer = remaining[0][0] if len(remaining) == 1 else None
        if remaining_peer is not None:
            label = f"Remove {ticker(removed_peer.get('name'))}: remaining {ticker(remaining_peer.get('name'))} estimate"
        else:
            label = f"Remove {ticker(removed_peer.get('name'))}: remaining-peer estimate"
        rows.append((label, money(remaining_price)))
        change = remaining_price - full_peer_price
        rows.append(("Change from two-peer midpoint", f"{'-' if change < 0 else '+'}{money(abs(change))}"))

    print_table(rows)


if __name__ == "__main__":
    main()
