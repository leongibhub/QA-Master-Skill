# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Q-1 is a 180-day-old duplicate helper costing 1h/month with no high-risk protection gap. Q-2 is a one-day-old refund test that mocks its subject, missed duplicate debit yesterday and still exposes loss. Q-3 is an unfixed confirmed production defect. Q-4 closes a refactor ticket without behavior or maintenance evidence. Q-5 has changed code, independent regression, a maintenance sample and owner acceptance. Decide LOWER_PRIORITY/HIGHER_PRIORITY/PRODUCT_DEFECT/NOT_CLOSED/CLOSED without age-only ranking.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| Q-1 | LOWER_PRIORITY |
| Q-2 | HIGHER_PRIORITY |
| Q-3 | PRODUCT_DEFECT |
| Q-4 | NOT_CLOSED |
| Q-5 | CLOSED |

## Verification Method

1. Separate active product defects, test/architecture debt, exceptions and evidence gaps. Record source, impact, cause, age and current controls.
2. Explain accumulated risk through observed maintenance effort, exposure or detection delay. Missing rates yield qualitative or conditional estimates, not invented money.
3. Rank impact, exposure, detectability, dependencies and repayment effort/benefit; age is one signal. A new severe gap may precede old minor debt.
4. Closure requires changed assets, independent checks, removed debt effects and accountable acceptance. Tickets alone do not repay debt; accepted risk needs authority and expiry.
