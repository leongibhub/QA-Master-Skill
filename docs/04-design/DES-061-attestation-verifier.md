# DES-061 — Strict-profile attestation verifier port

- Artifact ID: `DES-061`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Change / task: `CR-015` / `TASK-076`
- Requirements: `REQ-011` claim boundary; `REQ-024` (unknown provider revision
  may only create `EXPLORATORY_CONFIGURED_SAME_MODEL`); supports Phase 3
  readiness of DRAFT `REQ-025`/`NFR-009` without completing them
- Inputs: `DES-040` v1 (§4 runtime object, §9 trusted attestation and
  strict-profile boundary, §12 verification mapping),
  `DOC-PAIRED-EVALUATION-PLAN-001` v1, `DOC-HOLDOUT-REGISTER-PROCEDURE-001` v1
- Evidence boundary: this is an implementable design candidate. It records no
  model run, pair, score, rating, superiority, approval, acceptance, release,
  or Gate result, and authorizes no holdout release.

## 1. Scope and component boundary

Add a strict-profile attestation path to the existing
`qa_master.paired_evaluation` module (DES-040) as an additive port:

1. `TrustRegistry` loads an administrator-controlled local registry file that
   names trusted attestation issuers and their public verification keys.
2. `AttestationVerifier` validates locally held provider-signed evidence files
   (detached signatures) against that registry and returns a typed verdict.
3. The strict preflight path accepts `STRICT_COMPARISON_CANDIDATE` manifests
   and `VERIFIED` attestation records only when the verifier confirms both the
   provider revision and the system baseline for both arms before any
   participant call; otherwise it fails closed with the existing codes.
4. `run_pair`/`materialize`/`validate` remain unchanged for exploratory
   manifests; the default runtime still configures no registry or verifier.

Everything else in DES-040 keeps its boundary: the executor, materializer,
parsers, grader, and historical evidence are untouched; human rating, holdout
release, aggregation, and any superiority decision remain outside.

## 2. Trust registry (administrator-controlled, local)

A single JSON file, supplied by an explicit path argument on the strict
commands only (`--trust-registry`). It is never read implicitly, never
packaged, and never committed to the repository. Exact object:

```json
{
  "schema_version": 1,
  "registry_id": "REG-LOCAL-001",
  "created_at_utc": "2026-10-16T00:00:00Z",
  "issuers": [
    {
      "issuer_id": "ISSUER-EXAMPLE-001",
      "subject": "provider_revision",
      "algorithm": "ED25519",
      "public_key_multibase": "..."
    }
  ]
}
```

Rules (all validated by `strict_json` + `exact` key sets, fail codes in §6):

- `registry_id` and `issuer_id` satisfy the existing `identifier` grammar.
- `subject` is exactly `provider_revision` or `system_baseline`.
- `algorithm` is exactly `ED25519` in v1; any other value rejects the registry.
- `public_key_multibase` is a nonempty text of 8–512 characters.  v1 stores it
  as an opaque trust anchor; the verifier compares signature validity through
  the cryptography library, not by re-deriving the key text.
- The registry contains no secret, no private key, and no attestation values.
  It names only who is trusted to sign which subject.

The registry path is recorded in preflight output by its file digest, not its
content. A registry whose bytes change between preflight and run is
`TRUST_REGISTRY_DRIFT` and fails the run before participant calls.

## 3. Attestation evidence files (provider-signed, locally held)

Each attestation subject (`provider_revision`, `system_baseline`) for each arm
is supplied as a pair of files in a caller-supplied evidence directory outside
the manifest directory, both arm roots, and the output root:

- `<subject>-<arm_id>.json` — the attestation document:

```json
{
  "schema_version": 1,
  "subject": "provider_revision",
  "arm_id": "A",
  "value": "gpt-6-astra@2026-10-01 rev 88f...",
  "observed_at_utc": "2026-09-30T12:00:00Z",
  "issuer_id": "ISSUER-EXAMPLE-001",
  "statement": "The participant arm used exactly this model revision."
}
```

- `<subject>-<arm_id>.sig` — the detached signature over the canonical UTF-8
  bytes of the document.

Rules: `subject` must match the file name; `arm_id` is `A` or `B`; `value` is
nonempty text ≤ 20000 bytes; `observed_at_utc` is whole-second RFC 3339 UTC
with `Z`; `statement` is text ≤ 20000 bytes; the document has no `rating`,
`score`, `winner`, or claim member (existing `check_keys` prohibition).

## 4. Verifier interface and typed verdict

```python
def verify_attestations(trust_registry_path, evidence_dir, manifest) -> dict
```

Called only from the strict preflight path. For each arm and each subject it:

1. Loads and validates the registry (§2).
2. Reads the document/signature pair (§3) through `no_links`/`contained`
   guards; symlinks/reparse points reject.
3. Checks the issuer is in the registry for exactly that `subject`.
4. Verifies the detached signature against the issuer's registered public key.
5. Checks `observed_at_utc` is not after the manifest's `created_at_utc`
   (an attestation cannot attest the future).
6. Returns per-arm/per-subject:

```json
{
  "subject": "provider_revision",
  "arm_id": "A",
  "state": "VERIFIED",
  "value": "gpt-6-astra@2026-10-01 rev 88f...",
  "issuer_id": "ISSUER-EXAMPLE-001",
  "observed_at_utc": "2026-09-30T12:00:00Z",
  "evidence_sha256": "<digest of the attestation document>",
  "verifier_id": "ATTESTATION_VERIFIER_V1",
  "verification": "SIGNATURE_VALID"
}
```

`state` is `VERIFIED` only when every step succeeds; otherwise the verdict is
`REJECTED` and the run fails closed with the specific code (§6).  The verdict
never contains the signature bytes or the public key; those are re-verified,
not echoed.

In the run result, `runtime.model.provider_revision` and
`runtime.model.system_baseline` records are updated to `state: VERIFIED` with
the verified `value` and `evidence_sha256`, and the whole verdict list is
appended to the run result as `attestation_verdicts`.  The manifest's declared
`UNVERIFIED`/`NOT_AVAILABLE` values are preserved in the manifest record; the
verdict is a separate derived fact, so history remains inspectable.

## 5. Strict preflight path

`_prepare_unchecked` changes from unconditional `STRICT_PROFILE_NOT_SUPPORTED`
to:

1. If `profile == STRICT_COMPARISON_CANDIDATE` and no trust registry was
   supplied: fail `STRICT_PROFILE_NOT_SUPPORTED` (unchanged fail-closed
   default).
2. If a trust registry was supplied and `profile ==
   EXPLORATORY_CONFIGURED_SAME_MODEL`: fail `STRICT_PROFILE_MISMATCH` (an
   exploratory manifest never consumes a registry; it cannot silently upgrade).
3. If `profile == STRICT_COMPARISON_CANDIDATE` with a registry: run
   `verify_attestations` for both arms and both subjects before participant
   materialization or any call. Any rejected verdict fails the preflight with
   the specific code; no partial run is started.
4. Additionally require for strict manifests: `retry_count == 0` (already
   global), `temperature_state == NOT_AVAILABLE`, `seed_state ==
   NOT_AVAILABLE` (already enforced), and at least two schedule rows with both
   orders represented (DES-040 §4.2 already requires this for strict
   candidates; preflight now derives and checks it instead of trusting the
   declared profile).

`evidence_class` in the run result is `STRICT_COMPARABILITY_CANDIDATE` only
when: profile is strict, both attestations are `VERIFIED` for both arms,
`execution_backend == NATIVE_CODEX`, and pilot status is derived without
discretion exactly as today. Even then the result carries
`claim_status: NOT_ASSERTED`, `human_rating_status: NOT_EXECUTED`, and a new
`strict_eligibility: HOLDS_FOR_HOLDOUT_PROTOCOL_ONLY` marker stating that the
separate REQ-011 holdout/human protocol is still required. It is not fairness
proof or a superiority conclusion.

## 6. New failure codes (stable, public)

| Code | Meaning |
|---|---|
| `TRUST_REGISTRY_INVALID` | Registry schema/grammar/algorithm rejection. |
| `TRUST_REGISTRY_DRIFT` | Registry bytes changed between preflight and run. |
| `ATTESTATION_MISSING` | Document or signature file absent for a required subject/arm. |
| `ATTESTATION_INVALID` | Document schema/grammar rejection. |
| `ATTESTATION_SIGNATURE_INVALID` | Signature verification failed. |
| `ATTESTATION_ISSUER_UNKNOWN` | Issuer not registered for that subject. |
| `ATTESTATION_TIME_INVALID` | `observed_at_utc` after manifest `created_at_utc`. |
| `STRICT_PROFILE_MISMATCH` | Registry supplied with an exploratory profile. |
| `STRICT_ATTESTATION_INCOMPLETE` | A strict manifest lacks a required verdict. |

`ATTESTATION_NOT_SUPPORTED` remains the code for a manifest that merely
declares `VERIFIED` in `runtime.model` without going through the verifier; the
existing `_runtime` check stays, and the strict path now additionally checks
that the declared records match the verifier verdicts exactly (declared
`UNVERIFIED` + verdict `VERIFIED` is the only accepted combination).

## 7. CLI surface

```text
qa-master paired-evaluation validate --manifest M --trust-registry R --attestations D
qa-master paired-evaluation preview   --manifest M --trust-registry R --attestations D
qa-master paired-evaluation run       --manifest M --trust-registry R --attestations D --output-root O
```

`--trust-registry` and `--attestations` are optional and default to absent.
Absent + strict profile = `STRICT_PROFILE_NOT_SUPPORTED`. Absent + exploratory
profile = today's behavior, unchanged. The existing flags keep their names and
semantics.

## 7a. Failure-classification boundary

All new codes are preflight/validation rejections, not infrastructure
failures: they occur before any process spawn, are recorded with
`terminal_status: PRECHECK_REJECTED` when raised during `run`, and never
produce partial attempts, ledger rows for unstarted calls, or a
`pilot_status`. Validation (`validate`) returns them as normal
`PairedEvaluationError` codes; `run` wraps them exactly like existing preflight
failures.

## 8. Cryptography boundary

v1 uses Ed25519 through the `cryptography` package already required by the
repository's environment. Design decisions:

- Detached signatures over the canonical document bytes (the same
  `canonical()` + UTF-8 byte stream the module already uses for digests) avoid
  any ambiguity about signed content.
- No network verification, no CRL/OCSP, no key rotation in v1. A registry
  change is a new registry file digest and a new preflight; history stays
  inspectable because old run records keep the registry digest they used.
- No symmetric secrets, no passwords, no tokens; the registry is public-by-
  design trust anchor material and is checked by `redact()` unchanged.
- Signature verification uses a fixed library call with no caller-supplied
  algorithm selection; `algorithm` in the registry is a v1 constraint fixed to
  `ED25519`, not a plug-in selector.

If the `cryptography` package is unavailable at runtime, the strict path fails
closed with `ATTESTATION_VERIFIER_UNAVAILABLE` rather than degrading.

## 9. What this port does not change

1. Exploratory manifests: byte-for-byte unchanged behavior; no registry
   supplied means no new code path is even entered.
2. `qa_master.benchmark`, `qa_master.semantic_quality`, `design_methods`, and
   all historical CR-011/CR-013 evidence: untouched.
3. The holdout procedure: a strict-eligible run is a precondition for holdout
   release, never an authorization; `DOC-HOLDOUT-REGISTER-PROCEDURE-001`
   keeps its own release gate.
4. The grader and assertions: unchanged; grading remains evaluator-held and
   separate.
5. Human decisions: no rating, adjudication, aggregate, winner, or superiority
   output exists or can be derived from this port.

## 10. Verification mapping and handoff

Developer tests (stable `TC-SV` IDs) at minimum:

1. Registry: valid load; each invalid field/grammar/algorithm; drift between
   preflight and run; secret-pattern rejection; link/reparse rejection.
2. Attestation documents: each schema violation; subject/filename mismatch;
   missing sig; time-after-manifest; cross-arm substitution rejected.
3. Signature: valid Ed25519 round-trip; wrong key; tampered document; tampered
   signature; unsupported algorithm; library-unavailable fail-closed.
4. Preflight: strict without registry fails `STRICT_PROFILE_NOT_SUPPORTED`;
   exploratory with registry fails `STRICT_PROFILE_MISMATCH`; strict with all
   verdicts passes; any rejected verdict fails with the specific code and zero
   calls started; declared-VERIFIED without verifier still fails
   `ATTESTATION_NOT_SUPPORTED`; declared/verdict mismatch rejected.
5. Run result: `evidence_class` derivation `STRICT_COMPARABILITY_CANDIDATE`
   only under the full §5 conjunction; `strict_eligibility` marker present;
   `claim_status`/`human_rating_status` unchanged; manifest declared values
   preserved alongside verdicts.
6. CLI: flag defaults; exploratory path unchanged; strict path argument
   wiring; error codes stable in output.

Independent tester: re-runs the focused suite fresh-wheel, adds negative and
boundary cases not authored by the developer (per this matrix), and verifies
the no-registry default still behaves byte-for-byte as CR-011's frozen
exploratory path on the retained fixtures.

Independent reviewer: inspects the fail-closed ordering (registry →
attestations → materialization → calls), the fail code table, the unchanged
exploratory path, and confirms no superiority/Gate/holdout-release semantics
leaked into the port.

## 11. Alternatives and deferred decisions

- Online provider attestation endpoints were rejected: they add network
  dependency, credentials, and a remote trust decision to a local-only module.
- A general plugin verifier interface was rejected: v1 needs exactly one
  deterministic signature check; a plug-in surface would reintroduce
  caller-supplied executable code into a content/trust boundary.
- Key rotation/revocation lists were deferred: v1 has a single administrator
  registry; rotation is a new registry file and a new preflight, which history
  already supports.
- Recording attestation documents in the run ledger was deferred to the
  eventual strict run design: this port records verdicts and digests only, so
  no provider-issued text needs retention policy yet.

## 12. Current conclusion

`NOT_EXECUTED`. This design makes the DES-040 strict-profile path implementable
behind an administrator-controlled trust registry with detached Ed25519
signatures, failing closed everywhere. It authorizes no model call, no holdout
release, no rating, and no comparison or superiority conclusion.
