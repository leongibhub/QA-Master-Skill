"""Byte-level regression guard for the CR-018/CR-021 instruction conventions.

These tests pin the delivered state of the instruction upgrades measured by
the CR-019 paired comparison and pending CR-022 verification: if any clause
is deleted or mutated in the packaged skill assets, the suite fails here
before the change can silently regress the product's measured advantage.

They assert clause presence in the packaged bytes only. Behavioural effect is
verified separately (CR-022 fresh-set run, quota-blocked until 2026-10-22);
the GRANTED/ALLOWED absence guard enforces audit OA-3: arm instructions must
never be tuned to oracle-synthesized tokens the facts do not fix.
"""
import unittest

from qa_master.codex_skill import skill_bundle


def _asset(name: str) -> str:
    bundle = skill_bundle()
    if name not in bundle:
        raise KeyError(f'packaged asset missing: {name}')
    return bundle[name].decode('utf-8')


def _flat(text: str) -> str:
    """Whitespace-normalized view for line-wrap-insensitive matching.

    TASK-097 lesson: raw substring checks false-fail when a clause wraps
    across lines in the Markdown source. Normalizing all whitespace runs to
    single spaces makes the assertions robust to future re-wrapping.
    """
    return ' '.join(text.split())


TYPED_OBSERVATIONS = _flat(_asset('references/typed-observations.md'))
SKILL = _flat(_asset('SKILL.md'))


class CR018Conventions(unittest.TestCase):
    """CR-018 first instruction round: typed observation conventions."""

    def test_literal_source_tokens_clause(self):
        self.assertIn('copy that token byte-for-byte into the observation', TYPED_OBSERVATIONS)

    def test_synthesized_labels_clause(self):
        self.assertIn('uppercase letters, digits and single underscores', TYPED_OBSERVATIONS)

    def test_declared_precision_and_scale_violation_clause(self):
        # typed-observations.md: precision preservation
        self.assertIn('must appear in the precision the rule declares', TYPED_OBSERVATIONS)
        # functional-api.md: scale-violation candidate requirement (CR-018
        # targeted the 0.505-class miss; the clause lives in the
        # boundary-method guide, not the conventions reference)
        functional_api = _flat(_asset('scripts/qa_master/skills/professional/functional-api.md'))
        self.assertIn('violates the scale by one place beyond it', functional_api)

    def test_both_classes_answered_clause(self):
        self.assertIn('accepted and rejected candidates must supply both classes', TYPED_OBSERVATIONS)


class CR021Conventions(unittest.TestCase):
    """CR-021 second round: completeness, minimality, universe, vocabulary."""

    def test_multi_part_completeness_clause(self):
        self.assertIn('one member per kind', TYPED_OBSERVATIONS)
        self.assertIn('missing an asked-for member is an incomplete answer', TYPED_OBSERVATIONS)
        self.assertIn('no extra fields, no renames', TYPED_OBSERVATIONS)

    def test_label_minimality_clause(self):
        self.assertIn('shortest form the source phrasing supports', TYPED_OBSERVATIONS)
        self.assertIn('never folded into the event name', TYPED_OBSERVATIONS)

    def test_family_consistency_clause(self):
        # R-01 repair: the canonical and anti-example pair must both stay.
        self.assertIn('Synthesized labels are **family-consistent**', TYPED_OBSERVATIONS)
        self.assertIn('PAYMENT_CONFIRMED` beside `PAYMENT_NOT_CONFIRMED`', TYPED_OBSERVATIONS)
        self.assertIn('CONFIRMED_PAYMENT` beside `PAYMENT_NOT_CONFIRMED`', TYPED_OBSERVATIONS)

    def test_classification_vocabulary_mirrors_engine(self):
        self.assertIn('CONFLICT` for rules assigning different outcomes to the same combination',
                      TYPED_OBSERVATIONS)
        self.assertIn('EXCLUDED` for combinations the facts rule out of the legal universe',
                      TYPED_OBSERVATIONS)
        self.assertIn('GAP` for combinations no rule covers', TYPED_OBSERVATIONS)

    def test_skill_md_engine_discipline_wiring(self):
        flat = SKILL
        self.assertIn('mirror its output discipline', flat)
        self.assertIn('classify conflicts as `CONFLICT`', flat)
        self.assertIn('extra candidate ideas in the case table rather than the typed answer', flat)

    def test_skill_md_typed_observations_wiring(self):
        self.assertIn('references/typed-observations.md', SKILL)


class CR025Conventions(unittest.TestCase):
    """CR-025 third round: explicit-scope discipline + exhaustive-universe provenance."""

    def test_explicitly_stated_scope_clause(self):
        self.assertIn('list exactly those stated items', TYPED_OBSERVATIONS)
        self.assertIn('do not derive additional candidates from general rules', TYPED_OBSERVATIONS)

    def test_exhaustive_universe_provenance_clause(self):
        self.assertIn('exhaustive-universe fact', TYPED_OBSERVATIONS)
        self.assertIn('enumeration provably complete', TYPED_OBSERVATIONS)


class OA3NonGoalGuard(unittest.TestCase):
    """Audit OA-3: never tune arm instructions to oracle-synthesized tokens."""

    def test_no_granted_or_allowed_tokens(self):
        for text, name in ((TYPED_OBSERVATIONS, 'typed-observations.md'), (SKILL, 'SKILL.md')):
            self.assertNotIn('GRANTED', text, f'{name} must not prescribe GRANTED')
            self.assertNotIn('ALLOWED', text, f'{name} must not prescribe ALLOWED')


if __name__ == '__main__':
    unittest.main()
