# Source freeze: Linux rolling-upgrade public-development scenario

- Artifact ID: `DOC-PUBLIC-LINUX-QA-FREEZE-001`
- Scenario: `PD-LINUX-UPGRADE-001`
- Classification: `PUBLIC_DEVELOPMENT`; non-holdout; non-comparative.
- Evidence Status: `PENDING`
- Frozen at product revision: `36835ee`

This records exact proposed inputs for later registered work.  It does not
record a participant invocation, service action, test execution, recovery,
defect, approval, score, acceptance, release, or comparison result.  A changed
listed byte creates a new scenario revision.

## Proposed participant-visible files

| Relative path | SHA-256 | Byte count |
|---|---|---:|
| `release-notes.md` | `FA1481EFE9420EBA9C23FF5144F8AB39B8C31E1FF677618BBC1DDF486F528F4F` | 2,335 |
| `upgrade-runbook.md` | `A7621F2401646CAE76E33024D8F857D742EA169A6C0D172F3619778177797C32` | 2,055 |
| `support-and-config.md` | `1C2DBBEA6050B115C1CF30A016258EA0F8D8F845F032D419EDB98ED5357E8B8C` | 1,644 |
| `incident-excerpts.md` | `F527DB21D24F5F3624E376C6C555E1B714B7584B1FD2D00D26B6136B9611E569` | 876 |
| `participant-task.md` | `9EF1D4EEC587B34471B6A56A179FD99734A1A3DDED161D6BC80FE05E5DCF45E5` | 1,672 |

## Audit-only files

| Relative path | SHA-256 | Byte count |
|---|---|---:|
| `audit-ledger.md` | `3DABC312A4D11ED7AA329C3DD39AB815313810FEBFBCFEDF824CA6282DAEF353` | 4,061 |
| `expected-review-checklist.md` | `F9E0019CA54D173FC318498CFF1EABCC165039EAA25288B3029F33F50AE26BF5` | 2,167 |
| `docs/01-research/public-development-linux-qa-evaluation-plan.md` | `9CCB57577C1645677E9C729870F53DF4E24F1E8473A8000869305226818CC842` | 5,484 |

## Byte-preservation control

| Relative path | SHA-256 | Byte count |
|---|---|---:|
| `.gitattributes` | `178053EECF12F437A84EDB074D0AC3A06B472C2E1F1DCFA12049319924439D54` | 120 |

The later participant's allowed paths are only the five participant-visible
files and exact installed QA Master Skill files recorded by the runner.  It may
not read this record, audit-only files, comparator material, holdout material
or unrelated repository files.  Later tester and reviewer work receive audit
aids only after participant output freezes.
