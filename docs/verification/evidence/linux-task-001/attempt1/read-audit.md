# Read audit

Every file actually read while producing this package, with the SHA256 hash
computed from the file's actual bytes (uppercase hex) at read time. No other
file inside or outside `D:\QA-Master-PR2` was read for this task. Directory
listings of the skill folder were used only to locate installed guide files
(no other file contents were opened).

## Task definition (1 file)

| # | Full path | SHA256 |
|---|---|---|
| 1 | D:\QA-Master-PR2\.qa-master\linux-task-001\participant\inputs\participant-task.md | 9EF1D4EEC587B34471B6A56A179FD99734A1A3DDED161D6BC80FE05E5DCF45E5 |

## Input source documents (4 files)

| # | Full path | SHA256 |
|---|---|---|
| 2 | D:\QA-Master-PR2\.qa-master\linux-task-001\participant\inputs\release-notes.md | FA1481EFE9420EBA9C23FF5144F8AB39B8C31E1FF677618BBC1DDF486F528F4F |
| 3 | D:\QA-Master-PR2\.qa-master\linux-task-001\participant\inputs\upgrade-runbook.md | A7621F2401646CAE76E33024D8F857D742EA169A6C0D172F3619778177797C32 |
| 4 | D:\QA-Master-PR2\.qa-master\linux-task-001\participant\inputs\support-and-config.md | 1C2DBBEA6050B115C1CF30A016258EA0F8D8F845F032D419EDB98ED5357E8B8C |
| 5 | D:\QA-Master-PR2\.qa-master\linux-task-001\participant\inputs\incident-excerpts.md | F527DB21D24F5F3624E376C6C555E1B714B7584B1FD2D00D26B6136B9611E569 |

## Installed QA Master Skill files (10 files)

| # | Full path | SHA256 |
|---|---|---|
| 6 | D:\QA-Master-PR2\.qa-master\linux-task-001\participant\.agents\skills\qa-master\SKILL.md | 626E0506A5B5E4992057596FC57EC69676C1A86B0A99943504A8DDBD7E4DDD6F |
| 7 | D:\QA-Master-PR2\.qa-master\linux-task-001\participant\.agents\skills\qa-master\references\work-protocol.md | BA232063489DB733EEEA68C46BD4B812A33C982BA36E7440149B1E7DECA549EC |
| 8 | D:\QA-Master-PR2\.qa-master\linux-task-001\participant\.agents\skills\qa-master\references\domains.md | 5B4FF7B66ED7D7B7503EA11D8E30699B09B20D8EE6C8704238FA4260ABE9C9C1 |
| 9 | D:\QA-Master-PR2\.qa-master\linux-task-001\participant\.agents\skills\qa-master\references\design-methods.md | 128DF839DA4B48DF2B40DE1B943EE0E1C1B76573FDAAAEF2717E5E8087F4265F |
| 10 | D:\QA-Master-PR2\.qa-master\linux-task-001\participant\.agents\skills\qa-master\scripts\qa_master\skills\professional\requirements-review.md | 31F7FB509154D9D9756CFE43ED1C027A6470B15C6CAB6BDB526B215FC3BF3C76 |
| 11 | D:\QA-Master-PR2\.qa-master\linux-task-001\participant\.agents\skills\qa-master\scripts\qa_master\skills\professional\functional-api.md | 28AE23AB80D819157F0630AA6E4579DD9D7FA21D54D7B8F40B6B583C4471207E |
| 12 | D:\QA-Master-PR2\.qa-master\linux-task-001\participant\.agents\skills\qa-master\scripts\qa_master\skills\professional\structural-integration.md | 3E393E1775242E807A3244DBAA2F56553C5C6A88564E6E2228EC12DF4BC97615 |
| 13 | D:\QA-Master-PR2\.qa-master\linux-task-001\participant\.agents\skills\qa-master\scripts\qa_master\skills\professional\nonfunctional-compatibility.md | 352AB77DBCBF8029F33FD316030226614E92042A35CBC2F8217A8A250E69BEF2 |
| 14 | D:\QA-Master-PR2\.qa-master\linux-task-001\participant\.agents\skills\qa-master\scripts\qa_master\skills\professional\security-recovery.md | DCC0FCFFA0F2D16B3952F91296DAC0D71311C3DE173DCCFC9956259532CFBB59 |
| 15 | D:\QA-Master-PR2\.qa-master\linux-task-001\participant\.agents\skills\qa-master\scripts\qa_master\skills\professional\regression-evidence.md | C11547B88CCFB79551229390B8147D4C395E7F23548E04F40F5C28942DDB6619 |

## Notes

- The installed offline helper `scripts/qa.py` was **not** executed; only the
  guide files it bundles were read. Its use as a possible future finite-model
  helper is noted in `01-review-and-strategy.md` §4 and
  `03-review-and-handoff.md` §4.
- Files deliberately **not** read, per participant-task restrictions:
  anything else in `D:\QA-Master-PR2` outside
  `.qa-master\linux-task-001\participant\`, including
  `benchmarks/public-development/PD-LINUX-UPGRADE-001/` contents (other than
  the input copies), `audit-ledger.md`, `expected-review-checklist.md`, the
  evaluation plan, and `source-freeze.md`.
- Hashes were computed with PowerShell `Get-FileHash -Algorithm SHA256` from
  the actual bytes on disk, immediately before drafting the deliverables.
