# CR-022 fresh-set paired verification — report skeleton (pre-registered, data-pending)

- Classification: `PUBLIC_DEVELOPMENT` / `DRAFT_UNAPPROVED`
- Run id: `CR022-FRESH-VERIFICATION-001`
- Prepared by: comparison researcher (same agent family as the scenario and
  instruction author — disclosed; not an independent holdout)
- Date: 2026-10-17 (before execution; execution blocked on upstream model
  quota, recovery 2026-10-22)
- Status: `SKELETON_PRE_REGISTERED` — every outcome cell below is empty by
  design. Structure, columns, check-to-class mapping and status vocabularies
  were fixed and mechanically derived from the frozen oracle bytes before any
  CR-022 model call. T1 check order follows the frozen oracle; each check lists
  every pre-declared class it belongs to (multi-membership is intended).
  One plan-vs-oracle deviation was found and disclosed at build time (see T2).

## Pre-registered bindings (re-verified at skeleton build time)

| Artifact | Value |
|---|---|
| Run manifest canonical digest (bound into assertion bundle) | `d102763f6a1f118bc8b41f247c56b590b94845ff8ca5846cfb86227711e9aed1` |
| Assertion bundle sha256 (live) | `466b71efb936d45ba0c1a9c5d4e914ea5764ed7d16850c10b90bb1421c32d28e` |
| Semantic rules sha256 (live) | `89ea6b6242c57d21267350cf26087c97e5be1126187cf5a1cbcabe1cb77ada77` |
| Arm A commit | `fa84f489abe62cbf7cfe9185729fc480466a80d3` (post CR-018 + CR-021) |
| Arm B commit (pinned) | `1a8c57c` byte-identical to CR-017/CR-019 upstream arm |
| codex.exe sha256 (pinned; path re-verified 2026-10-17, still matching) | `9ecb9df2ecafcc00542ef0966c6f1737a81397dc9531b0a4b178238e2bf4a46d` |

## Pre-registered reporting plan (verbatim from `cr022-semantic-rules-v1.md`)

Per arm: (a) exact layer; (b) semantic layer (rules S1–S5; S6 explicitly not
adopted). Per upgrade class: multi-part completeness (Q-FS-021/031/051/052),
label minimality and family consistency (Q-FS-053/061/071), row-universe
discipline (Q-FS-041/071/081), engine vocabulary alignment (Q-FS-031/081),
precision and scale-violation persistence (Q-FS-021/022), interior-neighbour
persistence (Q-FS-011/012), provenance specificity
(Q-FS-032/033/042/062/072/082/083). Embedded-ambiguity gap behaviour (FS-04,
FS-07) reported descriptively, not as pass/fail. R-03a linkage disclosure
carried in every report.

## T1 — Per-check exact and semantic outcomes per arm (18 checks)

Exact layer vocabulary: `SATISFIED` / `VIOLATED` / `UNSCORABLE` (mechanical
grader). Semantic layer vocabulary: `SEMANTIC_SATISFIED` /
`SEMANTIC_VIOLATED` / `SEMANTIC_ABSENT` (rules S1–S5 applied identically to
both arms; per-check application notes required where invoked).

| Scenario | Check | Classes (pre-declared) | A exact | B exact | A semantic | B semantic |
|---|---|---|---|---|---|---|
| FS-01 | Q-FS-011 | interior-neighbour persistence | | | | |
| FS-01 | Q-FS-012 | interior-neighbour persistence | | | | |
| FS-02 | Q-FS-021 | multi-part completeness; precision and scale-violation persistence | | | | |
| FS-02 | Q-FS-022 | precision and scale-violation persistence | | | | |
| FS-03 | Q-FS-031 | multi-part completeness; engine vocabulary alignment | | | | |
| FS-03 | Q-FS-032 | provenance specificity | | | | |
| FS-03 | Q-FS-033 | provenance specificity | | | | |
| FS-04 | Q-FS-041 | row-universe discipline | | | | |
| FS-04 | Q-FS-042 | provenance specificity | | | | |
| FS-05 | Q-FS-051 | multi-part completeness | | | | |
| FS-05 | Q-FS-052 | multi-part completeness | | | | |
| FS-06 | Q-FS-061 | label minimality and family consistency | | | | |
| FS-06 | Q-FS-062 | provenance specificity | | | | |
| FS-07 | Q-FS-071 | label minimality and family consistency; row-universe discipline | | | | |
| FS-07 | Q-FS-072 | provenance specificity | | | | |
| FS-08 | Q-FS-081 | row-universe discipline; engine vocabulary alignment | | | | |
| FS-08 | Q-FS-082 | provenance specificity | | | | |
| FS-08 | Q-FS-083 | provenance specificity | | | | |

## T2 — Per-class tallies per arm (computed from T1 only)

**Plan-vs-oracle deviation disclosure (found at skeleton build time, before
any model call):** the pre-declared reporting plan names `Q-FS-053` under
label minimality and family consistency, but the frozen 18-check oracle
contains no `Q-FS-053` (FS-05 contributes `Q-FS-051`/`Q-FS-052` only). The
pre-registered validity script (131/131) validated oracle internal
consistency, not plan-membership existence. Handling, fixed now before
execution: the class tallies over the checks that actually exist
(`Q-FS-061`, `Q-FS-071`); `Q-FS-053` is retained in the table below as a
named-but-absent member and can never be counted. No re-authoring of the
frozen oracle or the pre-declared rules is permitted at this point.

| Class | Checks | A exact | B exact | A semantic | B semantic |
|---|---|---|---|---|---|
| multi-part completeness | Q-FS-021, Q-FS-031, Q-FS-051, Q-FS-052 | | | | |
| label minimality and family consistency | Q-FS-053 (absent from frozen oracle), Q-FS-061, Q-FS-071 | | | | |
| row-universe discipline | Q-FS-041, Q-FS-071, Q-FS-081 | | | | |
| engine vocabulary alignment | Q-FS-031, Q-FS-081 | | | | |
| precision and scale-violation persistence | Q-FS-021, Q-FS-022 | | | | |
| interior-neighbour persistence | Q-FS-011, Q-FS-012 | | | | |
| provenance specificity | Q-FS-032, Q-FS-033, Q-FS-042, Q-FS-062, Q-FS-072, Q-FS-082, Q-FS-083 | | | | |

Tallies are counts of `SATISFIED` (exact) and `SEMANTIC_SATISFIED` (semantic)
over the class member list. The CR-019 noise-floor disclosure (±1 on counts)
carries forward and must be stated next to any between-arm difference.

## T3 — Process layer (both arms)

Per scenario per arm: `COMPLETE` / `PARTIAL` / `FAILED` / `NOT_EXECUTED`
(from the run document attempts; NOT_EXECUTED requires a stated cause, as in
the CR-019 PE-STT-004 quota event).

| Scenario | Arm A process | Arm B process | Notes |
|---|---|---|---|
| FS-01 | | | |
| FS-02 | | | |
| FS-03 | | | |
| FS-04 | | | |
| FS-05 | | | |
| FS-06 | | | |
| FS-07 | | | |
| FS-08 | | | |

## T4 — Embedded-ambiguity gap behaviour (descriptive, not pass/fail)

FS-04 (ticket priority) and FS-07 (elevator retry) embed intentional
ambiguity. Describe what each arm did with the ambiguity — which rows were
produced, how gaps were labelled, whether the ambiguity was flagged — without
scoring it. Structure:

| Scenario | Arm | Rows produced | Gap handling | Ambiguity flagged? |
|---|---|---|---|---|
| FS-04 | A | | | |
| FS-04 | B | | | |
| FS-07 | A | | | |
| FS-07 | B | | | |

## R-03a linkage disclosure (fixed wording, carried in every report)

Arm-A instructions at commit `fa84f48` embed the CR-018 and CR-021 upgrades,
which were derived from the CR-017/CR-019 failure modes of the prior oracle.
The CR-022 set is fresh material authored AFTER those upgrades, targeting the
same upgrade classes with new domains; the scenario author is the same agent
family as the instruction author (not independent). Results are exploratory
public-development evidence. No superiority, quality, acceptance, Gate or
release claim is authorized by this run; the formal claim path (strict profile,
human ratings, independent holdout) remains `NOT_AVAILABLE`.

## Status legend

- Exact: `SATISFIED` = mechanical grader matched expected value and evidence
  refs; `VIOLATED` = mismatch; `UNSCORABLE` = no single retained observation
  for the check.
- Semantic: `SEMANTIC_SATISFIED`/`SEMANTIC_VIOLATED` = equivalent after S1–S5
  normalization (rule cited per use); `SEMANTIC_ABSENT` = no retained
  observation to normalize.
- Process: `COMPLETE` / `PARTIAL` / `FAILED` / `NOT_EXECUTED`.
