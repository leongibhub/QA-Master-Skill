# CR-037 strict ordinary and schema probes — independent classification

`strict-login-output.md` SHA-256 `90d1dad68e71496c6864a930b72f927eac45feaadbfb616a8bc7b97183fa50a9`: PASS STRICT-WRITE-01, 02 and 04–06. Every login action has its own supplied expected result; no unsolicited raw machine field occurs; actual bug behavior is attributed to the supplied report and unknown facts stay pending.

`strict-schema-output.md` SHA-256 `bd525ed02de3ad3c199ac392a4862ad5dc162c756e5654383a949218c30dddc5`: PASS STRICT-WRITE-01–03, 05 and 06; STRICT-WRITE-04 is not applicable. Human expected result retains supplied response fields `source_role=member` and `Trace=trace-demo-01`. Parsed separate JSON exactly has keys `id`, `source_role`, `Trace`, `execution`, `steps`, with `TC-PROFILE-01`, `direct_input`, `[REQ-PROFILE-01]`, `NOT_RUN`, and one `GET /profile` step. No execution or external write is claimed.
