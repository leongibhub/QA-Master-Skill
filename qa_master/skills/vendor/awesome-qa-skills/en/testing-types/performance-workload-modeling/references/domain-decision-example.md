# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Daily volume is 600000 requests over 86400 seconds. A peak block contains 120000 requests but has no duration. W-1 claims peak 1000 RPS from daily total. W-2 additionally supplies a 600-second peak block; calculate its average RPS. W-3 has steady arrival 50 requests/s and mean system time 0.4s; calculate mean in-system requests. W-4 has 100 sessions: 60% browsing with 2 requests each, 40% checkout with 5 each, no retries. Decide UNSUPPORTED/CALCULABLE and compute W-2/W-3/W-4 without calling averages instantaneous peaks.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| W-1 | UNSUPPORTED |
| W-2 | CALCULABLE |
| W-3 | CALCULABLE |
| W-4 | CALCULABLE |

| METRIC | VALUE |
| --- | --- |
| peak_window_average_rps | 200 |
| mean_in_system_requests | 20 |
| total_requests | 320 |

## Verification Method

1. Describe each input with value, unit, timezone/window, source, and coverage. Requests/transactions/sessions/users are distinct; convert through transaction mix and requests per transaction with retries/background traffic noted.
2. Daily volume gives an all-day average only. Peak rate requires peak-share volume and window width; missing width yields a conditional formula/range, never invented peak duration/multipliers.
3. Choose open arrival or closed concurrency explicitly. Use Little's Law L=λW only within a steady window and consistent units; online/daily-active users are not concurrency.
4. Provide candidate curves, sourced session lengths/think times, and verification. Check observed arrivals/completions/mix; unconfirmed values are no production-capacity conclusion.
