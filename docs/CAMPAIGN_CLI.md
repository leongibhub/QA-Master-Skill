# Offline QA Campaign CLI

This is the first combined, one-command path that actually wires the existing requirement quality checker, case generation engine, coverage matrix and case reviewer together. It is **not** an LLM, an API connector, or an automated test executor.

## Run (Windows / Linux)

```bash
python -m qa_master.campaign_cli --input examples/campaign.json --output campaign-report.json
python -m unittest discover -s tests -q
```

Review `campaign-report.json`:
- `requirement_review.findings`: source problems, ambiguity and acceptance gaps
- `test_cases`: structured **draft** cases with requirement trace IDs
- `case_review`: case quality issues and trace matrix
- `coverage`: 13 test dimensions explicitly marked DRAFT, BLOCKED, UNASSESSED or N/A
- `unresolved.design_gaps`: missing oracle/threshold/approval
- `workflow`: no execution or SynapseRT write authorized

## Safety boundary

The CLI reads one local JSON bundle of no more than 5 MB and writes a local JSON output atomically. It never connects to Jira, GitLab, SynapseRT or remote machines, never issues PASS, and never approves a requirements baseline. It does not perform semantic extraction of natural language requirements; inputs must be structured and any acceptance oracle must be supplied.

## Tests

An independent local run from the project workspace passed **151 tests** including eight CLI integration tests. The GitHub copy is independently provided; GitHub Actions needs to be verified separately for the latest commit. The local source and remote-published source were produced in this session; changes in one should not be assumed synchronized beyond the files just committed.

## Next release gates

Real integration work, an AI semantic requirements analyst, expert test design for each domain, credential vault, authenticated approvals, remote execution, SynapseRT writeback and the head-to-head Awesome QA Skills evaluation remain unfulfilled.
