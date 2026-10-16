# Typed observation conventions

These conventions govern every typed observation a QA Master deliverable
reports — whether in a neutral response envelope, a case table or a review
packet. They exist so that two independent readers (human or grader) obtain
the same value from the same source material.

## Source tokens are literal

When a fact, contract or source document names a category, state, event or
outcome with a specific token (for example `INTERNATIONAL`, `STANDARD`,
`FINAL_SALE`), copy that token byte-for-byte into the observation. Do not
re-case, translate, expand or abbreviate a token that the source already
fixes. If two sources use different tokens for the same concept, record the
conflict as a gap instead of silently picking one.

## Synthesized labels are uppercase-underscore

When no source token exists and a label must be synthesized (an equivalence
band, a derived event name, a guard condition), build it from uppercase
letters, digits and single underscores: `BELOW_1000`, `AT_OR_ABOVE_1000`,
`PAYMENT_NOT_CONFIRMED`, `THIRD_CONSECUTIVE_WRONG_PASSWORD`. Prefer the
source's own phrasing collapsed to that form over invented vocabulary. Keep
the synthesized label list part of the deliverable so a reviewer can map each
label back to the phrase it came from.

## Observation values are minimal

A typed observation value carries exactly the members needed to answer its
check — nothing more. Supporting detail, source references, classifications
and audit notes belong in the case table or gap records, not inside the
observation value. An observation that a grader must compare for equality
fails when it carries extra members (`source_refs`, `step`, `expectation_scope`,
runtime commentary) inside the value. Keep the value a clean carrier of the
answered fact.

## Declared precision is preserved

Numeric text observations (decimals, monetary values, rates) must appear in
the precision the rule declares. When the rule states hundredths, write
`0.50`, never `0.5` or `0.50 EUR`. Integers stay integers (`100`, not
`100.00`). If the rule's precision is unstated, record that as a gap rather
than choosing a display precision silently.

## Every check answers every part

A check that asks for accepted and rejected candidates must supply both
classes. A check that asks for defined combinations must enumerate exactly
the combinations the facts define — undefined ones become gaps, not invented
rows, and correct-but-extra rows belong in the case table, not the typed
answer, unless the check asks for the full universe.
