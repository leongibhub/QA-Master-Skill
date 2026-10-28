# CR-037 initial local package delivery failure

Evidence status: `OBSERVED` from the root delivery readback.

- Attempt: `uv` force-install session `11491`.
- Tool exit: `0`.
- Isolated Python `-I` resource check: new `readable-artifacts.md` resource was
  absent and the canonical entry did not contain the new required rule.
- Interpretation: an old wheel/resource cache was reused; exit `0` did not prove
  the requested package content was installed.
- Managed user-skill update: not attempted after this failed content check.

TC-READ-005 is `FAIL` for this initial delivery attempt. The failure is limited
to local package freshness/content delivery; it is not business test execution
and does not invalidate the frozen source or synthetic authoring observations.
