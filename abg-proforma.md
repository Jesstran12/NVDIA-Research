# Asbury Automotive Group (ABG) — Pro-Forma Engine and the Known Answer

**Lab 09 — Pro-Forma Build: the Engine and the Known Answer.** The three-statement engine built from the Lab 09 instruction, proven on the ABG case from Part 1 of the video.

Engine: [`proforma.py`](proforma.py) (standard library only; `python3 proforma.py`, and `--break` to watch the check refuse). USD millions unless stated. Learning demonstration, not investment advice.

## D — the question

> **What are five years of a company's statements worth, built from assumptions you can defend, and how do you know the statements are right?**

**The three judgments that carry the ABG value:** organic growth of 1.8% a year (reported growth was 4.7%, but the stores the company already owned grew slower; acquisitions are bought, not earned), the 17.05% gross margin (a point either way is worth more than any other line), and the cost of equity of 10% (a round number the video calls conservative for a dealer). **Why cash is the last line the model computes:** every other line is set by an assumption; cash is what is left after the income statement, the working capital and the financing have all taken their share. If cash is typed instead of computed, the balance sheet has no way to tell you the other lines are wrong.

## R — the assumption set (value, label)

| Assumption | ABG value | Label |
|---|---|---|
| Organic revenue growth | 1.8% a year | judgment |
| Gross margin | 17.05% | judgment |
| SG&A ÷ gross profit, 2026 → 2030 | 66.5%, 65.5%, 64.5%, 64.5%, 64.5% | judgment |
| Depreciation ÷ opening PP&E | 82.4 ÷ 3,070.4 = 2.68% | history |
| Impairment, non-cash | 120 a year | judgment |
| Capital spending | 250 a year | guidance |
| Tax rate | 25.5% | judgment |
| Inventory days | 2,135.8 ÷ (17,999.0 − 3,071.7) × 365 = 52.2 | history |
| Floor plan ÷ inventory | 2,027.0 ÷ 2,135.8 = 94.9% | history |
| Other working capital | 0.8% of the change in revenue | judgment |
| Minimum cash / revolver limit / revolver rate | 25 / 850 / 6% | history / judgment / judgment |
| Debt repayment / share buyback | 150 / 150 a year | judgment |
| Interest: floor plan / term debt | 4.67% / 5.44% | history |
| Cost of equity / terminal growth | 10% / 2.5% | judgment |
| Shares outstanding | 17.951349 million | fact (10-Q, 30 June 2026) |

Opening balance sheet, FY2025: revenue 17,999.0 · inventory 2,135.8 · PP&E 3,070.4 · other assets 6,371.6 · cash 40.4 · floor plan 2,027.0 · term debt 3,572.0 · other liabilities 2,127.5 · equity 3,891.7.

**The line that makes a dealer different: floor plan.** Inventory loans from manufacturers' finance arms and banks. It rises with inventory, carries interest on the opening balance, and sits inside FCFE as an operating item. Take it out and the company has to fund $2 billion of cars from its own cash, which is why the video's cash goes to about −1.1 billion without it.

## I — the engine, from one request

The Lab 09 request was sent word for word with the table and the opening balance sheet under it; the returned code is `proforma.py`. Each year computes in the instruction's order: income statement, then the balance sheet except cash, then FCFE, then cash, drawing the revolver only if cash would fall below the minimum and repaying it first when cash is above it.

## V — the known answer

| Line | FY2026E known | FY2026E model | FY2030E known | FY2030E model |
|---|---:|---:|---:|---:|
| Revenue | 18,323.0 | 18,323.0 | 19,678.3 | 19,678.3 |
| Operating income | 844.2 | 844.2 | 971.4 | 971.4 |
| Net income | 413.6 | 413.6 | 527.5 | 527.5 |
| Free cash flow to equity | 211.4 | 211.4 | 342.3 | 342.3 |
| Cash, year end | 101.8 | 101.8 | 719.8 | 719.8 |
| Assets − liabilities − equity | 0.0 | 0.0 | 0.0 | 0.0 |
| Value per share | **$291.75** | **$291.75** | | |
| Share of value after 2030 | about 80% | 79.8% | | |

```
-- checks (must read 0.0 in every year)
                                      FY2026E    FY2027E    FY2028E    FY2029E    FY2030E
Assets − liabilities − equity             0.0        0.0        0.0        0.0        0.0
Cash at or above the 25 minimum           0.0        0.0        0.0        0.0        0.0
balanced, 5 year(s)
Equity value:                          5,237.3
Share of value after FY2030:            79.8%
Value per share:                  $     291.75
```

**Swap and break** (`python3 proforma.py --break`, FY2026 cash typed at the opening 40.4 instead of computed):

```
Model refused: FY2026E does not balance: assets − liabilities − equity = -61.4
(the year's change in cash with the sign flipped: -61.4)
```

The −61.4 is FY2026's change in cash (101.8 − 40.4) with the sign flipped. Before opening a single cell it says: one line on the balance sheet was typed, not linked, and it is the cash line. A model that does not refuse has not been checked.

## Reflect (to my partner)

1. Why the model computes cash last: it is the residual; computing it first hides every error downstream.
2. What −61.4 tells you before you open a cell: a balance gap that equals a cash flow is an unlinked cash line.

## Sources

- FIN 43900 Week 5, Lab 09 instruction and Part 1 of "Pro-Forma Valuation with AI" (the ABG assumption set, opening balance sheet and known answer).

Written for FIN 43900 (Purdue) as a learning exercise. Not investment research and not financial advice. AI assistance: the engine was generated from the Lab 09 request with Claude Code and checked against the known answer by me.
