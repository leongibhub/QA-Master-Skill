# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Classify these complete contracts/code summaries without syntax-based false positives. T-1: real price(total,taxClient), only external taxClient mocked to 2, independent price(10)=12 assertion; ignoring tax fails. T-2: real serializeOrder {id,status,total}, Human-reviewed snapshot retains all business fields; paid→pending fails. T-3: /health's sole contract is 503 for unavailable dependency, no body/write obligation; real handler with disconnected dependency asserts 503. T-4: subject price itself mocked to 12, then 12 asserted; production price never executes. Give STRONG/WEAK/FAKE and a concrete mutation rationale per test.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| T-1 | STRONG |
| T-2 | STRONG |
| T-3 | STRONG |
| T-4 | FAKE |

## Verification Method

1. Evaluate assertions against the actual contract; mock, snapshot, or status-only syntax alone does not imply WEAK/FAKE.
2. A boundary mock may replace a confirmed external dependency while real production logic executes. Mocking the subject itself and asserting its preset return offers no protection.
3. A reviewed, independent snapshot of stable business structure can detect meaningful mutations. A snapshot that discards all business fields cannot. A status assertion can be STRONG when status fully expresses the supplied contract; persistence obligations require business postconditions.
4. Support each classification with a concrete escaping/detected mutation and contract source. Retain confidence/gaps when evidence is missing, using the same bilingual rationale.
