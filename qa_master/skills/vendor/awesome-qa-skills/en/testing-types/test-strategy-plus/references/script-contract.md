# Input preparation script contract

Optional `scripts/run_*.py` prepare parsed evidence or source candidates with `NOT_ASSESSED`. They do not call a model, execute the main prompt, or produce semantic conclusions, risk priorities, complete cases, or approval. An agent performs the main prompt. Read `references/script-contract.md` before running helpers.

Required sources must be nonempty. Preserve all parsed text, line numbers, SHA-256, and source labels. A hash identifies parsed material; it does not establish original-document authority. Missing versions remain `UNKNOWN`. Keywords are not confirmed requirements, candidates are not executable cases, and no semantic result does not mean zero defects.

Use password length 12–64, calculator, and text-editor controls. No unrelated promotion, inventory, or payment findings may appear. Preserve Markdown underscores, minus signs, and comparison operators. Export formats change presentation only; Word/TSV retain `NOT_ASSESSED` and sources.

After preparation, give material to an agent executing the main prompt under `prompts/` to derive observable business outcomes, risk, and pending human decisions.
