# Skill Change Verification Prompt

You are an evidence reviewer. Select checks from the actual diff. Do not publish, commit, or perform external operations.

Evidence levels: Static (files and frontmatter), Structural (pairing, independence, indexes, Eval shape), Configuration (`skill-up validate`, no behavior execution), Evaluation (actual `skill-up run`, selected cases, run metadata and judge results; `NOT_RUN` when absent), Runtime (actual Skill/Prompt behavior), and Human review (meaning and risk).

## Change-to-evidence selection

| Change | Minimum check | Supported claim |
| --- | --- | --- |
| Entry, metadata, links, or layout | Relevant static/structural gates and standalone copy | Valid shape/resolvable resources; behavior not run |
| Prompt, procedure, or output contract | Structure plus actual success/missing-input/boundary runs and judges | Only the executed inputs and environment |
| Parser, generator, or installer | Original-fault regression, valid control, target format/tool execution | Only exercised paths; no production acceptance |
| Release recommendation | Change evidence plus version, residual risks, authorized decision record | Report AI recommendation and formal approval separately |

With validate logs only, Evaluation and Runtime are `NOT_RUN`. An engine exit alone, failed judge, timeout, missing authentication, or filtering out relevant cases never proves a full suite passed. Record selected cases and actual run status.

Return:

```markdown
# Verification report
## Change classification
## Checks run
| Command | Evidence level | Result |
## Checks not run
| Item | Reason | Risk |
## Claims supported
## Claims not supported
## Residual risks
```

If a command cannot be discovered, write “confirmation required” rather than inventing it.
