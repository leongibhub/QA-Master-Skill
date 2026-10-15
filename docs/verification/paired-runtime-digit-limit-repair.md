# TASK-049 follow-up: deterministic integer limits

Reviewer found that native INTEGER decoding inherited Python's configurable
integer conversion limit. The original 4,301-digit canonical token therefore
failed despite having no declared contract limit. This P2 is preserved as a
review finding rather than concealed by the later design correction.

The architect now specifies 1–34 magnitude digits, excluding sign, matching the
finite-method engine. The shared strict JSON decoder applies this limit to every
integer token, including nested JSON values, before conversion. INTEGER values
also have explicit mathematical range checks and matching fixed schema bounds;
the common prompt states the limit. The implementation does not mutate Python's
global integer settings.

Developer `/root` ran `python -m unittest tests.test_paired_value_contract -q`:
5 tests passed (0.007 seconds). The boundary case checks positive/negative 34/35
digits under Python limits 640 and disabled, verifies globals were not mutated
by the parser, and restores test configuration. This is developer evidence only.

Repaired contract working-file SHA-256:
`4D8ADA7CD03E62CE1BEBCA5865E878EF895C9FCF33847BB41E1495D92F3BD235`.
Final design clarification SHA-256:
`BD58F2D722A8F355D6302FFBCBA486DA9F08CD19D2D97B4D22502342C7507B92`.
Earlier native-value repair and old DES failure remain in their original records.
Fresh independent source-bound retest/review and regenerated pilot commitments
are required; no pilot or superiority result is asserted here.
