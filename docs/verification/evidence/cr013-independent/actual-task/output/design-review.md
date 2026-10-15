# Document release policy: offline QA design draft

Status: DRAFT_UNAPPROVED / AGENT_REVIEW_ONLY / NOT_EXECUTED. These are policy-level drafts with explicit execution gaps, not runnable product tests. No human baseline or approval record has been created.

## Source and method review

Sole product source: supplied source-facts.md, F-01 through F-07; current byte digest in read-audit.json. Owner described as product owner; named owner/date/version not supplied. Logical source-facts/F-xx locators in input are declared references into this file, not physical files read by the helper. No conflicting rule was observed in the supplied facts. No external source or implementation was consulted. The packaged example was NOT read. Source facts did supply semantic rules and source IDs for policy acceptance; missing legacy projection fields therefore do not mean the source lacked those facts. A dated/versioned approved baseline and interface-level acceptance were not supplied.

functional-api.md guided boundary partitions, state effects and negative invariants. requirements-review.md guided atomic rule extraction and separation of fact from missing interface, response and authorization rules. design-methods.md supplied strict schemas. work-protocol.md supplied case fields and handoff. domains.md prevented invented API/status/selector details. Exact installed documents and byte hashes are in read-audit.json.

## Draft cases

Every row inherits the explicit preconditions, actions, cleanup, automation limits and typed gaps in draft-cases.json. F-07 causes GAP-01 through GAP-05 for every case. All expectations are supplied draft policy, not approved acceptance criteria.

| Case | Source | Input/action | Expected policy result | Helper candidate |
|---|---|---|---|---|
| TC-B-01 | F-01 | Supply integer batch size 1 to the batch-size validation operation once its interface is defined. Observe the size acceptance classification through the agreed observable. | Batch size 1 is invalid (outside inclusive 2..6). | TC-MD-42B0E4AC96285095FDE3 |
| TC-B-02 | F-01 | Supply integer batch size 2 to the batch-size validation operation once its interface is defined. Observe the size acceptance classification through the agreed observable. | Batch size 2 is valid (inside inclusive 2..6). | TC-MD-9978AFFE135349E1F3A1 |
| TC-B-03 | F-01 | Supply integer batch size 3 to the batch-size validation operation once its interface is defined. Observe the size acceptance classification through the agreed observable. | Batch size 3 is valid (inside inclusive 2..6). | TC-MD-1B13D0E1DE6C9B79F4B7 |
| TC-B-05 | F-01 | Supply integer batch size 5 to the batch-size validation operation once its interface is defined. Observe the size acceptance classification through the agreed observable. | Batch size 5 is valid (inside inclusive 2..6). | TC-MD-26EEC46FCEE4969A52B8 |
| TC-B-06 | F-01 | Supply integer batch size 6 to the batch-size validation operation once its interface is defined. Observe the size acceptance classification through the agreed observable. | Batch size 6 is valid (inside inclusive 2..6). | TC-MD-23EA5A0F21F4FD29094E |
| TC-B-07 | F-01 | Supply integer batch size 7 to the batch-size validation operation once its interface is defined. Observe the size acceptance classification through the agreed observable. | Batch size 7 is invalid (outside inclusive 2..6). | TC-MD-DC273814BFFF88B81260 |
| TC-D-00 | F-02 | Set member=false and settled=false. Request the rebate decision through the future agreed interface; observe whether rebate is allowed. | No rebate. | TC-MD-6DCA6333DA6F3C2499BF |
| TC-D-01 | F-02 | Set member=false and settled=true. Request the rebate decision through the future agreed interface; observe whether rebate is allowed. | No rebate. | TC-MD-AC2F0582BC7FFCCF623F |
| TC-D-10 | F-02 | Set member=true and settled=false. Request the rebate decision through the future agreed interface; observe whether rebate is allowed. | No rebate. | TC-MD-87CEAA6F4504AF327797 |
| TC-D-11 | F-02 | Set member=true and settled=true. Request the rebate decision through the future agreed interface; observe whether rebate is allowed. | Rebate is allowed. | TC-MD-20E450973DFD95647F4E |
| TC-S-01 | F-03, F-04 | Observe initial status DRAFT. Trigger submit while status is DRAFT. Observe document status through the agreed status observable. | Status becomes REVIEW (F-04). | TC-MD-5F07D40238F2B68078A9 |
| TC-S-02 | F-03, F-05, F-04 | Observe initial status DRAFT. Trigger submit, then observe status REVIEW (F-04). Trigger publish while status is REVIEW. Observe document status through the agreed status observable. | Status becomes PUBLISHED (F-05). | TC-MD-B39F31CBBC34C6198B3E |
| TC-S-03 | F-03, F-06 | Observe initial status DRAFT. Trigger publish while status is DRAFT. Observe document status through the agreed status observable. | Transition is invalid; document status remains DRAFT (F-06). No particular error signal or persisted-data effect is asserted. | TC-MD-5E4CF69890F62C14DA68 |

## Additional source obligations beyond helper candidates

- F-01 strict integer: fractional 2.5 is outside the integer domain; GAP-09 records unresolved type representation and observable. Do not infer coercion rules for 2.0, string 2, booleans, null or omission.
- F-03 initial state: each state draft observes DRAFT before events. The establishment mechanism remains GAP-03.
- F-03 terminal: PUBLISHED has no valid outgoing state transition in the declared model. Event-level checks for submit/publish in PUBLISHED remain GAP-08; a terminal declaration does not define an error or persisted side effects.
- F-06 unspecified REVIEW/submit and PUBLISHED event pairs remain open; closed_world=false deliberately prevents invented invalid cases.

## Typed gaps

- **GAP-01 TARGET_MISSING** (All cases): Target interface and environment absent (F-07); no endpoint or UI interaction can be supplied.
- **GAP-02 OBSERVABLE_MISSING** (All cases): Actual acceptance, decision and status observation mechanisms/locators absent (F-01,F-07).
- **GAP-03 SETUP_MISSING** (All cases): No fixtures or means to create fresh documents and set rebate conditions supplied (F-07).
- **GAP-04 CLEANUP_MISSING** (All cases): Cleanup obligations/permissions absent; do not assume deletion is safe or no cleanup is necessary (F-07).
- **GAP-05 AUTH_POLICY_UNCONFIRMED** (All cases): Actor and authorization mechanics absent; no inferred role restrictions or credential tests (F-07).
- **GAP-06 CONTRACT_MISSING** (Invalid size; DRAFT publish): Error signal/code/message unspecified (F-01,F-06); only policy invalidity or DRAFT state invariant can be asserted.
- **GAP-07 EFFECT_ORACLE_MISSING** (DRAFT publish): No persisted-data side-effect rule (F-06). Do not assert no writes, no audit event, or no other effects.
- **GAP-08 TRANSITION_RULE_UNSPECIFIED** (REVIEW/submit; PUBLISHED/submit; PUBLISHED/publish): F-06 leaves other pairs unspecified. F-03 terminal prohibits valid outgoing state transitions, but does not establish error, ignored-event or retry/idempotency behavior. No closed-world denials added.
- **GAP-09 TYPE_CONTRACT_MISSING** (Strict integer batch inputs): F-01 excludes nonintegers at policy level. Representation/coercion rules for 2.0, string 2, boolean, null or omitted input need an interface contract; fractional 2.5 is outside strict integer domain. Helper integer grid does not cover this obligation.
- **GAP-10 THRESHOLD_AND_WORKLOAD_MISSING** (Performance/load/stress/stability): F-07 supplies no workload, target, duration or thresholds; these dimensions are deferred, no passing judgement available.
- **GAP-11 BASELINE_UNAPPROVED** (All cases): Source facts explicitly draft-only. This artifact is AGENT_REVIEW_ONLY; formal case baseline remains unapproved.

## Applicability and remaining work

Functional boundary/decision/state and source-defined negative policy drafts are provided above. API design remains CONTRACT_MISSING: no interface established, so no API contract matrix is populated. Security/auth-negative design remains AUTH_POLICY_UNCONFIRMED: no roles or auth mechanics supplied. White-box and integration applicability cannot be established without implementation and component boundaries; no code coverage claim. Performance, load/stress and stability are deferred with GAP-10; defining actions or metrics would require a target and workload, so no such scenario is claimed designed. Compatibility is deferred until supported configurations are supplied. Recovery is deferred until failure behavior and recovery contract are supplied. Regression selection is deferred until a change/build baseline exists. Linux and AI-specific profiles are N/A to the supplied document-policy object; no hardware/OS/AI behavior is specified.

## Helper completion and documentation issues

The actual command is preserved in command.txt and command-evidence.json, with stdout.txt and stderr.txt. System Python -I exited 0 and generated three models / 13 candidates: six boundary points (1,2,3,5,6,7), four boolean assignments, and three explicitly declared transitions. No finite-model obligation was reported. These counts describe only the declared model and do not establish product coverage.

Both method_design and installed_design were reviewed. installed_design retains METHOD_OUTPUT_REQUIRES_CASE_COMPLETION and usable/executable_case_claim=false. Candidates used generic preparation and satisfy-oracle text. The draft cases replace those with source-determined inputs, triggers, before/after statuses, actual policy outcomes, setup routes and scoped limitations. Missing concrete interfaces, observation mechanisms and cleanup are explicit typed gaps; no candidate has become executable. Source mapping is DECLARED, not independently verified by the helper.

Unresolved installed-document issue: design-methods.md documents only requirement id, non-secret data and dimension; it does not specify the fields the legacy requirement-review projection expects. Authored requirements used id/title/dimension/approved=false. The accepted input therefore produced EMPTY_REQUIREMENT, NO_PROVENANCE and NO_ACCEPTANCE legacy findings, and ORACLE_MISSING legacy coverage gaps despite separately declared method oracles. They are retained rather than hidden. The wrapper case_review.pass=true applies to an empty legacy test_cases array and is not an approval or test result. No second attempt guessed undocumented fields; no code inspection was used to discover them. Installed helper command/parser/runtime error: none observed; stderr was empty. The agent artifact-writing script initially failed with UnicodeDecodeError because Windows default GBK decoded the UTF-8 helper report; explicit UTF-8 decoding fixed that local script. The installed helper was not rerun and its original input/report remain unchanged. See artifact-authoring-error.txt.

The functional guide calls its status NOT_RUN while the design command uses NOT_EXECUTED; this packet uses NOT_EXECUTED consistently to mean no product execution. The guide requests approved inputs, while SKILL.md and the work protocol explicitly allow draft design pending human baseline. The task remains draft-only.

## Agent review and handoff

AGENT_REVIEW_ONLY: all four F-02 combinations are represented without excluded combinations or default-rule overlap; boundaries derive from step 1 and inclusive endpoints; only explicit transitions were encoded; invalid publish asserts DRAFT only, not no persisted side effects. No fabricated role, guard, code, message, endpoint or cleanup was introduced. Source-defined initial/type/terminal obligations omitted by candidate generation were exposed separately. Remaining readiness gaps prevent execution and formal baselining. No product tests, network operations, external writes, campaign/approval mutation or comparison claims occurred.

See handoff.json for actual source/artifact hashes and next design action: resolve typed gaps and obtain bounded human baseline review before any separately authorized product execution.
