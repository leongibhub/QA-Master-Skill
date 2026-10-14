# QA Master Skill (v0.1 prototype)

Original QA orchestration prototype, designed to run alongside [naodeng/awesome-qa-skills](https://github.com/naodeng/awesome-qa-skills) without redistributing upstream skills.

Current capabilities: task intent routing, phase and approval gates, persisted campaign state, missing-information tracking, and 13-dimension coverage checks. GitLab/Jira/Confluence/SynapseRT/remote execution adapters are NOT implemented in v0.1.

## Installation

Download the complete v0.1 ZIP from the ChatGPT conversation until all files have been migrated here. Run `python -m unittest discover -s tests -v` in the extracted project folder. `skills/qa-master/SKILL.md` is the master-agent guidance.

## Upstream skill library

Install upstream skills **separately** after verifying license compatibility for your usage. QA Master selects and orchestrates compatible skills; it does not replace their specialized expertise. Upstream source code is not included.

Do not commit usernames, passwords, personal tokens, or remote-machine secrets.

This repository is a work in progress, not a finished automated testing platform.
