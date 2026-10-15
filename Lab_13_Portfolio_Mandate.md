# Lab 13 — Portfolio Mandate Defense

**Case:** Meridian Foundation Reserve  
**Checker:** [`mandate.py`](mandate.py)  
**Official instructions:** [FIN43900 Lab 13](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-08/lab-13-portfolio-mandate.md)

## D — Decision question

Which of portfolios A, B, and C does the Meridian Foundation's mandate permit, and what must the CIO answer before anyone optimizes?

## R — Statement classification

The classifications below were completed by the student without AI. Grammar and formatting were subsequently reviewed with AI assistance.

| Statement | Classification | One-line reason |
|---|---|---|
| S1 | Hard constraint | It establishes the portfolio's time horizon and rebalancing schedule. |
| S2 | Objective | It states the portfolio's return goal. |
| S3 | Unverifiable promise | The exact dollar payout cannot be guaranteed. |
| S4 | Preference | The benchmark allocation may change with market movements and rebalancing. |
| S5 | Hard constraint | It establishes which types of trades are permitted. |
| S6 | Hard constraint | It limits the portfolio's exposure to a single issuer. |
| S7 | Hard constraint | Exceeding the turnover limit requires committee approval. |
| S8 | Unverifiable promise | Redemption within the stated period cannot be guaranteed. |
| S9 | Unverifiable promise | Market conditions cannot be controlled, so the stated loss ceiling cannot be guaranteed as written. |
| S10 | Missing | The phrase "nobody has said" indicates that the optimization objective has not been defined. |

Allowed classifications: objective, hard constraint, preference, unverifiable promise, or missing.

## I/V — Checker and validation

Run:

```bash
python3 ColinSpensley/MSFT/mandate.py
```

Base-case result:

| Rule | A | B | C |
|---|---:|---:|---:|
| Weights sum to 100 | 100.0 pass | 100.0 pass | 100.0 pass |
| Long-only (lowest weight) | 0.0 pass | 0.0 pass | 0.0 pass |
| Reserve ≥ 3.0% | 14.0 pass | 1.0 FAIL | 2.0 FAIL |
| Redeemable in 5 days ≥ 90% | 100.0 pass | 85.0 FAIL | 100.0 pass |
| Largest single company ≤ 8% | 0.0 pass | 9.0 FAIL | 8.0 pass |
| Calendar-year loss | requires CIO clarification | requires CIO clarification | requires CIO clarification |
| Verdict | passes every checkable rule | fails 3 rule(s) | fails 1 rule(s) |

The required negative-weight probe was performed by temporarily changing A's cash weight to −2% and its global equity weight to 64%. The checker reported a −2.0% lowest weight and one failed rule, while the reserve remained 10.0%. The original 2% cash and 60% global equity weights were then restored.

## E — Attack the checker

### AI-proposed candidate D

Candidate D is 3% Treasury bills and 97% global equity index fund, with 0% in every other holding. It uses only permitted holdings and should pass every rule coded in `mandate.py`.

The checker confirmed that D totals 100.0%, has no negative weights, holds the required 3.0% reserve, is 100.0% redeemable within five business days, has 0.0% single-company exposure, and passes every checkable rule.

### Student judgment

1. The objection to candidate D does not hold because the 60/40 allocation is identified as a benchmark rather than a hard constraint.
2. Statement S4 determines this conclusion because it identifies 60/40 as the benchmark, not as a required allocation.

## One question for the CIO

**Question:** Should the pilot minimize tracking error relative to the 60/40 benchmark?  
**Design-changing answer:** If the CIO prioritizes minimizing tracking error, the portfolio would remain close to the 60/40 benchmark and rebalance annually in accordance with S1.


## AI-use record

AI generated and debugged the standard-library mandate checker and proposed candidate D, as the lab permits. The student independently completed the classification, candidate-D judgment, and CIO-question sections; AI subsequently reviewed their grammar and formatting.
