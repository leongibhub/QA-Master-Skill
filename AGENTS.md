# QA Master — single-repository agent contract

Read `skills/qa-master/SKILL.md`. Treat QA Master as a self-contained, original product. Do not tell the user to install a separate QA Skills repository. Only invoke specialist implementations that actually exist inside this repository or connected built-in executors that have been verified. If a capability is still unimplemented, state it clearly and never fabricate its output.

Keep approvals, test evidence, requirements provenance, version and environment records. A request to generate cases must not trigger remote execution or create Jira/SynapseRT objects. Never commit passwords, API keys or SSH secrets.
