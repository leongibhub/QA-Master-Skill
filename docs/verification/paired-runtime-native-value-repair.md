# TASK-049 native-value contract repair

Developer: `/root`. Change: CR-011. Requirements: REQ-020/023, NFR-006/007/008.
Design: `DOC-PAIRED-VALUE-ENCODING-CLARIFICATION-001` (DRAFT).

The independent TC-PE-221 failed against DES-040 v1's string-only encoding.
That failure is retained; it is not recast as a passing test. The architect
compared alternatives and selected native JSON values prospectively because this
profile validates locally rather than using an unverified provider output schema.
The public oracle already uses that representation and is unchanged.

The repaired contract rejects lexical integer `-0` before parsing loses its sign.
It checks native JSON depth (16) and total nodes (4,096, including object keys)
iteratively, bounding the pending traversal before allocation. The fixed common
schema now associates each discriminator with its native primitive/container
type, and the prompt states the representation and limits. Local validation still
enforces constraints that JSON Schema cannot express, with no coercion.

Exact repaired input hashes are in `paired-runtime-repair-source-manifest.json`.
Developer verification is retained in `evidence/cr011-repair/developer-36.txt`.
Independent retest and formal review are separate TASK-042/TASK-043 work; this
record does not claim either, a model call, comparison, approval, or Gate result.

The common prompt/schema byte hashes changed, so pre-repair prepared pilot
manifests must be regenerated before use. Visible fixtures and oracle values do
not change; extract their locked Git blob bytes to avoid checkout newline drift.
