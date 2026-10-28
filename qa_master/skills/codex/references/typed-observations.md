# Typed observation conventions

Apply this reference only when the task explicitly requests typed observations
or graded answers. It does not rewrite ordinary human-facing case or bug prose;
when active, retain the literal-token, synthesized-label and declared-precision
rules below in the required typed field or payload.

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

## Synthesized labels are uppercase-underscore and minimal

When no source token exists and a label must be synthesized (an equivalence
band, a derived event name, a guard condition), build it from uppercase
letters, digits and single underscores: `BELOW_1000`, `AT_OR_ABOVE_1000`,
`PAYMENT_NOT_CONFIRMED`, `THIRD_CONSECUTIVE_WRONG_PASSWORD`. Prefer the
source's own phrasing collapsed to that form over invented vocabulary.

A synthesized label is **minimal**: it names exactly one condition, event or
class — the shortest form the source phrasing supports. Do not stack
qualifiers into the label when the source states them as separate events or
separate conditions (`WRONG_PASSWORD`, not
`WRONG_PASSWORD_BEFORE_THE_THIRD_ONE`, when the source names a wrong-password
event and a third-consecutive-wrong-password event separately). Guards and
conditions belong in their own field, never folded into the event name.

Synthesized labels are **family-consistent**: events or classes that the
source presents as a family around one concept (an event and its negation, a
guarded and an unguarded variant, successive members of one sequence) derive
from one canonical phrasing of that concept so the family stays structurally
parallel — `PAYMENT_CONFIRMED` beside `PAYMENT_NOT_CONFIRMED`, not
`CONFIRMED_PAYMENT` beside `PAYMENT_NOT_CONFIRMED`. When choosing the family
stem, prefer the phrasing that appears in the most family members or that
the source names as the concept itself; when equal, prefer the grammatically
complete phrase ("confirmed payment" → `PAYMENT_CONFIRMED` treats
"payment" as the concept and "confirmed" as its state). Keep the synthesized
label list part of the deliverable so a reviewer can map each label back to
the phrase it came from.

## Classification tokens mirror the engine

When a typed observation classifies rows (rule conflicts, excluded
combinations, coverage gaps), use the same classification vocabulary the
deterministic design engine emits — `CONFLICT` for rules assigning different
outcomes to the same combination, `EXCLUDED` for combinations the facts rule
out of the legal universe, `GAP` for combinations no rule covers — rather
than inventing variants (`CONFLICTING`, `UNSUPPORTED_EXCLUDED`,
`UNRESOLVED`). One vocabulary across the behavioral and deterministic paths
is itself a product guarantee: a reviewer who reads both outputs must never
need a translation table.

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
classes. A check that asks for two kinds of rows (valid and invalid
transitions, legal and excluded combinations) supplies one member per kind —
missing an asked-for member is an incomplete answer, not a concise one. A
check that asks for defined combinations must enumerate exactly the
combinations the facts define — undefined ones become gaps, not invented
rows, and correct-but-extra rows belong in the case table, not the typed
answer, unless the check asks for the full universe. When the question names
the row keys, use exactly those keys per row — no extra fields, no
renames. When a check scopes its answer to items the facts state explicitly —
"invalid transition candidates explicitly stated", "exclusions explicitly
listed", "cases the facts name as blocked" — list exactly those stated items,
one member per stated item, and do not derive additional candidates from
general rules (a "no event leaves a terminal state" rule, an implied negation,
or a symmetric inference). Derived-but-unstated candidates belong in the case
table, not the typed answer.

## Evidence cites the exhaustive-universe fact

When a check asks for a list drawn from a bounded universe (all transitions,
all defined combinations) and the facts include a statement that enumerates
that universe (for example "the only states are DRAFT, ACTIVE, CLOSED"), cite
that exhaustive-universe fact as a source reference together with
each item-defining fact. The exhaustive-universe fact is what makes the
enumeration provably complete; listing correct items without it leaves the
answer unsourced at the universe level.
