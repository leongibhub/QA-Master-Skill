# Claude Code host integration requirements — 2026-10-20

- Artifact: `DOC-CLAUDE-CODE-HOST-INTEGRATION-REQ-001`
- Change: `CR-030`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `OBSERVED` — bounded installer and review evidence is retained
  for repaired subject `7d6929b`; target-session discovery remains `NOT_EXECUTED`.

## Purpose and boundary

The user requested a simpler installation path for QA staff using the Claude Code
extension in VS Code, with their organisation's chosen model configured in that
host. This change extends the existing self-contained `qa-master` installation;
it does not add a second QA product, configure a model provider, or collect API
credentials.

The user authorised the documentation and implementation work. TASK-124 delivered
the concise route, and TASK-125/126 retain bounded installer/path and independent
review evidence. Actual discovery of the installed Skill in the target VS Code
Claude Code session remains `NOT_EXECUTED`. No Gate, release, acceptance,
external test execution, or model-capability result is implied.

## REQ-027 — concise Claude Code installation route

| Item | Requirement |
| --- | --- |
| Priority | P1 |
| Expected behaviour | The existing package shall provide one documented Claude Code installation route for a user target and one for a project target. Each route installs the same self-contained `qa-master` bundle at the corresponding `.claude/skills/qa-master` location and reports the final target. The Skill entry remains `SKILL.md`; it must not require a separate upstream Skill installation. |
| Documentation | The quickstart shall distinguish the VS Code Claude Code host from the model selected by the host, show one short command per target type, and show one non-executing example prompt. It shall state that the user must start a new host session to discover the installed Skill. |
| Scope boundary | This requirement covers package installation and documentation only. It does not prove that a particular extension version discovers the path, that the configured DeepSeek or other model is available, that the model follows the Skill, or that any tests/external writes ran. |
| Measurable acceptance | (1) The documented commands resolve to a user or project `.claude/skills/qa-master` target without requiring manual copying. (2) The installed target contains `SKILL.md`, local helper and packaged assets required by the existing installer manifest. (3) The project route writes only in its named target and installer-owned staging, backup or recovery siblings beneath validated non-linked parent directories; the user route has the equivalent boundary beneath the current user's Claude Skill target. (4) Documentation contains no API token, password, cookie, provider endpoint, or claim that host discovery has occurred. |
| Verification | `TC-HOST-001` is `PASS` within the bounded installer/path/manifest scope in `EVID-CLAUDE-CODE-HOST-INSTALLATION-2026-10-20`, including the `7d6929b` ancestor-junction repair retest; `TC-HOST-002` target-session discovery remains `NOT_EXECUTED`. |

## NFR-011 — host and credential boundary

| Item | Requirement |
| --- | --- |
| Expected behaviour | Installation, README and help output shall keep host discovery, model selection and credentials separate. They shall not write, print, request or retain API tokens, passwords, cookies, private keys or provider configuration. Existing updater/backup/manifest integrity controls remain applicable to each Claude Code target. |
| Measurable acceptance | (1) A source and installed-package check finds no credential values or credential-input flags in the Claude Code route. (2) User and project target calculation is deterministic from the selected installation mode. (3) An existing managed target is handled through the established installer update/rollback contract. (4) Missing host-session observation is explicitly `NOT_EXECUTED`, never inferred from a filesystem copy or a successful command exit. |
| Verification | `TC-HOST-001` provides bounded installer evidence in `EVID-CLAUDE-CODE-HOST-INSTALLATION-2026-10-20`; `TC-HOST-003` attempt 2 is `PASS` at `7d6929b` after ancestor-link rejection and controlled update locations were independently reviewed. |

## Planned work and test cases

| ID | Work / check | Owner role | Current state |
| --- | --- | --- |
| TASK-124 | Implement and document the concise Claude Code user/project installation route using the existing self-contained installer and safeguards. | developer / documentation_manager | `OBSERVED`: documentation route at `053c287`; repaired ancestor-link safeguard at `7d6929b`. This is an implementation record, not host discovery. |
| TASK-125 | Independently validate ordinary disposable Claude targets, manifests/assets, idempotence, modified-target rejection and repaired ancestor-link containment. | tester | Bounded `PASS`: attempt 1 at `053c287` tested ordinary targets; attempt 2 at `7d6929b` rejects a real Windows ancestor junction before external-target write and accepts an ordinary target. `TC-HOST-002` remains `NOT_EXECUTED`. |
| TASK-126 | Independently review route clarity, target containment, credential boundary and claims against the frozen implementation and TASK-125 evidence. | reviewer | Attempt 1 `FAIL` at `053c287` (P1/P3). Attempt 2 `PASS` at `7d6929b`, P0–P3 open count 0, in `DOC-CR030-INDEPENDENT-REVIEW-001`. |
| TC-HOST-001 | Install to disposable user-like and project-like Claude targets; validate target calculation, manifest/assets and no unrelated writes. | tester | `PASS` (bounded; `EVID-CLAUDE-CODE-HOST-INSTALLATION-2026-10-20`, attempt 2 retests `7d6929b` ancestor-junction rejection) |
| TC-HOST-002 | In the supplied VS Code Claude Code environment, start a new session and observe whether `qa-master` is discoverable and manually callable. Record extension/host version if available. | tester | `NOT_EXECUTED` |
| TC-HOST-003 | Review source, installed files and docs for credential handling, provider configuration, path escape and unsupported host-discovery claims. | reviewer | `PASS` at `7d6929b`; attempt-1 P1/P3 resolved, P0–P3 open count 0 (`DOC-CR030-INDEPENDENT-REVIEW-001`) |

## Change impact

The onboarding documents, existing installer's ancestor-reparse safeguards and
installation tests changed. The current CLI's existing `--project`, `--user`
and explicit `--target` modes are reused; this increment does not require a new
installer command.
The packaged QA catalogue, model/provider configuration, evaluation results,
external systems and existing `.agents` installation route are outside this
increment unless a later scoped change records otherwise.
