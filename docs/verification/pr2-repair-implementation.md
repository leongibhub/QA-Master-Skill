# CR-012 installer repair implementation

- Developer: `/root`; task context: CR-012, TASK-047/048 validation.
- Imported source: contributor PR [#2](https://github.com/leongibhub/QA-Master-Skill/pull/2), commits `b18099a` and `0ae0ec0287a62d1b91e0c108c5d9def377cd70a2`.
- Frozen repaired `qa_master/codex_skill.py` working-file SHA-256: `E008FBD1263BD32CBE9E7C62C688F3D4CDAD3B15D2CAEB4BC21DDC24C1B3F93F`.

The original installer verified files before archiving them. Independent review
reproduced loss of a concurrent edit, deletion of an unknown file under
`__pycache__`, loss of the active directory when both publication and rollback
failed, and acceptance of a Windows junction. These are retained as BUG-009–012.

Updates now detach the old directory before archiving, verify it again after
archiving, and retain that directory permanently for late writes through open
handles. Standard `.agents/skills` installs retain it outside the discovery tree,
under `.agents/.qa-master-recovery`. The returned `recovery_directory` identifies
it; cleanup is deliberately manual. The ZIP includes generated caches, while
only `.pyc` cache files are ignored during managed-file verification. Unknown
non-cache files and Windows reparse points are rejected. Failed rollback reports
the preserved recovery path. This is not a filesystem lock or snapshot guarantee.

Developer observation: the original nine installer tests passed against the
repaired source (`unittest discover -s tests -p test_codex_skill.py -q`, Python
3.13.5, ResourceWarning treated as error; 4.518 seconds). Independent validation
and review are separately owned and recorded in `pr2-independent.md` and
`pr2-review.md`; this developer observation does not substitute for either.

README now points to the upstream development branch for integration. This
increment does not complete paired model evaluation, enterprise E2E, V1 acceptance,
release, or evidence that QA Master outperforms the upstream skill library.
