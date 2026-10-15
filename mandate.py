"""Check candidate portfolios against Meridian Foundation's checkable mandate rules."""

from collections import defaultdict


# Editable mandate inputs
RESERVE_SIZE_USD_MILLIONS = 100.0
QUARTERLY_DISTRIBUTION_USD_MILLIONS = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW_BUSINESS_DAYS = 5
MINIMUM_LIQUID_SHARE_PERCENT = 90.0
ISSUER_LIMIT_PERCENT = 8.0
ISSUER_LIMIT_EXEMPTIONS = {"none", "U.S. Treasury", "diversified fund"}

HOLDINGS = {
    "Cash": {
        "issuer": "none",
        "business_days_to_redeem": 0,
        "reserve_eligible": True,
    },
    "Treasury bills": {
        "issuer": "U.S. Treasury",
        "business_days_to_redeem": 1,
        "reserve_eligible": True,
    },
    "Treasury 10-year note": {
        "issuer": "U.S. Treasury",
        "business_days_to_redeem": 1,
        "reserve_eligible": True,
    },
    "Global equity index fund": {
        "issuer": "diversified fund",
        "business_days_to_redeem": 2,
        "reserve_eligible": False,
    },
    "Investment-grade bond fund": {
        "issuer": "diversified fund",
        "business_days_to_redeem": 3,
        "reserve_eligible": False,
    },
    "Private real estate fund": {
        "issuer": "diversified fund",
        "business_days_to_redeem": 90,
        "reserve_eligible": False,
    },
    "Acme Corp bonds": {
        "issuer": "Acme Corp",
        "business_days_to_redeem": 4,
        "reserve_eligible": False,
    },
    "Acme Corp stock": {
        "issuer": "Acme Corp",
        "business_days_to_redeem": 1,
        "reserve_eligible": False,
    },
}

CANDIDATES = {
    "A": {
        "Cash": 2.0,
        "Treasury bills": 2.0,
        "Treasury 10-year note": 10.0,
        "Global equity index fund": 60.0,
        "Investment-grade bond fund": 26.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 0.0,
    },
    "B": {
        "Cash": 1.0,
        "Treasury bills": 0.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 55.0,
        "Investment-grade bond fund": 20.0,
        "Private real estate fund": 15.0,
        "Acme Corp bonds": 5.0,
        "Acme Corp stock": 4.0,
    },
    "C": {
        "Cash": 1.0,
        "Treasury bills": 1.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 70.0,
        "Investment-grade bond fund": 20.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 8.0,
    },
    # AI-proposed attack portfolio: it passes every coded rule but may be unsuitable
    # because its equity concentration conflicts with the spirit of S4 and exposes S9.
    "D": {
        "Cash": 0.0,
        "Treasury bills": 3.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 97.0,
        "Investment-grade bond fund": 0.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 0.0,
    },
}


def pass_label(passes: bool) -> str:
    return "pass" if passes else "FAIL"


def check_candidate(weights: dict[str, float], reserve_minimum: float) -> list[bool]:
    """Measure and print every checkable rule for one candidate."""
    unknown_holdings = set(weights) - set(HOLDINGS)
    missing_holdings = set(HOLDINGS) - set(weights)
    if unknown_holdings or missing_holdings:
        raise ValueError(
            f"Candidate holdings must match HOLDINGS; unknown={sorted(unknown_holdings)}, "
            f"missing={sorted(missing_holdings)}"
        )

    total_weight = sum(weights.values())
    lowest_weight = min(weights.values())
    reserve_weight = sum(
        weights[name] for name, details in HOLDINGS.items() if details["reserve_eligible"]
    )
    liquid_weight = sum(
        weights[name]
        for name, details in HOLDINGS.items()
        if details["business_days_to_redeem"] <= LIQUIDITY_WINDOW_BUSINESS_DAYS
    )

    company_weights: defaultdict[str, float] = defaultdict(float)
    for name, weight in weights.items():
        issuer = HOLDINGS[name]["issuer"]
        if issuer not in ISSUER_LIMIT_EXEMPTIONS:
            company_weights[issuer] += weight
    largest_company_weight = max(company_weights.values(), default=0.0)

    checks = [
        abs(total_weight - 100.0) < 1e-9,
        lowest_weight >= 0.0,
        reserve_weight + 1e-9 >= reserve_minimum,
        liquid_weight + 1e-9 >= MINIMUM_LIQUID_SHARE_PERCENT,
        largest_company_weight <= ISSUER_LIMIT_PERCENT + 1e-9,
    ]

    print(f"  Weights sum to 100: {total_weight:.1f} {pass_label(checks[0])}")
    print(f"  Long-only (lowest weight): {lowest_weight:.1f} {pass_label(checks[1])}")
    print(
        f"  Reserve >= {reserve_minimum:.1f}%: "
        f"{reserve_weight:.1f} {pass_label(checks[2])}"
    )
    print(
        f"  Redeemable in {LIQUIDITY_WINDOW_BUSINESS_DAYS} days "
        f">= {MINIMUM_LIQUID_SHARE_PERCENT:.1f}%: "
        f"{liquid_weight:.1f} {pass_label(checks[3])}"
    )
    print(
        f"  Largest single company <= {ISSUER_LIMIT_PERCENT:.1f}%: "
        f"{largest_company_weight:.1f} {pass_label(checks[4])}"
    )
    print("  Calendar-year loss: requires CIO clarification")
    return checks


def main() -> None:
    reserve_minimum = (
        QUARTERS_TO_COVER
        * QUARTERLY_DISTRIBUTION_USD_MILLIONS
        / RESERVE_SIZE_USD_MILLIONS
        * 100.0
    )
    print(f"Reserve minimum: {reserve_minimum:.1f}%")

    for candidate_name, weights in CANDIDATES.items():
        print(f"\nCandidate {candidate_name}")
        checks = check_candidate(weights, reserve_minimum)
        failures = checks.count(False)
        if failures == 0:
            print("  Verdict: passes every checkable rule")
        else:
            print(f"  Verdict: fails {failures} rule(s)")


if __name__ == "__main__":
    main()
