# Source freeze: Collaborator Document API public-development scenario

- Artifact ID: `DOC-PUBLIC-API-QA-FREEZE-001`
- Scenario: `PD-API-COLLAB-001`
- Classification: `PUBLIC_DEVELOPMENT`; non-holdout; non-comparative.
- Evidence Status: `PENDING`
- Frozen at product revision: `40908ea`

This records the exact bytes proposed for a later registered task.  It does
not record a participant invocation, test execution, result, approval, score,
or acceptance.  A changed listed byte creates a new scenario revision.

## Proposed participant-visible files

| Relative path | SHA-256 | Byte count |
|---|---|---:|
| `requirements.md` | `C2EDCB918F408F88091C1CA1217D269B6D8FCA4F0A9D9ABF6B46F63F43883D47` | 2,618 |
| `openapi.yaml` | `6D83F43C638E4F8481F3EE405F18B21B1BCC23858D2B6D46BCECAA498D7EA007` | 6,091 |
| `participant-task.md` | `141BF089F672D6A20C6E9E4D8B54E896F0329CDEFC3FA1E188A89F9A98E3BAED` | 1,494 |

## Audit-only files

| Relative path | SHA-256 | Byte count |
|---|---|---:|
| `audit-ledger.md` | `CB32C5AA7B565FD258E673AA6F2BBF092665F2D20CDE8E5413EA94D352BEA41D` | 4,612 |
| `expected-review-checklist.md` | `0647D3A8C24B323E39D47BFB9DE8EA4B2FF1789D3C0DB24266E089941D906FE5` | 2,880 |
| `docs/01-research/public-development-api-qa-evaluation-plan.md` | `5BDFA20AF87583DBB4E917EDD2BE77924363BDD91A1A42494323E72C89A80C35` | 7,856 |

The later participant's allowed paths are only the three participant-visible
files and the exact installed QA Master Skill files recorded by the runner.
It may not read this freeze record, the audit-only files, private holdout
material, comparator material, or repository files outside the declared Skill
and trial output root.  Later tester and reviewer work receive the audit-only
files only after the participant output is frozen.
