# Vendored skills — awesome-qa-skills

This directory vendors the bilingual skill catalog from
[naodeng/awesome-qa-skills](https://github.com/naodeng/awesome-qa-skills)
(online catalog: <https://inaodeng.com/qaskills/>).

- **Upstream license:** [PolyForm Noncommercial License 1.0.0](./LICENSE)
- **Vendored content:** `en/` and `zh/` — `testing-workflows` (10),
  `testing-types` (150), `skill-engineering` (5).
- **Upstream README:** [UPSTREAM_README.md](./UPSTREAM_README.md)
- **Source snapshot:** [SOURCE_PROVENANCE.json](./SOURCE_PROVENANCE.json) pins the
  retrieved upstream commit, its Git tree, and a cross-platform canonical-content
  digest of the `en/` and `zh/` subtrees. It deliberately excludes QA Master
  wrapper files in this directory.

## Positioning

These are QA Master's *breadth leaves*. Each is a Markdown prompt workflow
(a `SKILL.md` with `name`/`description` frontmatter plus `prompts/`,
`references/`, `output-templates/`, `scripts/`, and `evals/`) and is **not**
executed by QA Master's deterministic engine. QA Master only discovers and
routes them: `plan` maps planning stages to canonical skill names
(`core.SKILLS` / `core.DIMENSION_SKILLS`) and selects the matching vendored
skill, reporting the result under `vendor_skills`.

QA Master adds its own conservative intent routing, `no_execution` gating,
a resumable state machine, source traceability
(`trace_matrix`), enterprise adapters, and a deterministic coverage-array
engine (`boundary` / `decision_table` / `state_transition` / `pairwise` /
`combinatorial`).
