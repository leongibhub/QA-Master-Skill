# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Fixture WebdriverIO8 async with matched browser. W1 config names a service package not installed; startup log identifies the missing module. W2 does not await click and checks no state. W3 paid assertion fails on pending with test/worker/session/browser version/stack and nonzero CI. W4 each worker has independent account/order, awaited actions, paid20/principal assertions, and cleanup. W5 catches command timeout then reportsPASS and exits0. Decide CONFIG_ERROR/REPAIR/EXPECTED_FAILURE/VALID/FAILURE_HIDDEN with original diagnostic evidence, without switching frameworks.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| W1 | CONFIG_ERROR |
| W2 | REPAIR |
| W3 | EXPECTED_FAILURE |
| W4 | VALID |
| W5 | FAILURE_HIDDEN |

## Verification Method

1. Fix WebdriverIO/Node, runner/framework, and browser/driver/service combinations. Check capabilities/services against installed packages, config, and remote support; names alone do not prove compatibility.
2. Generate version-compatible async specs/BDD steps and await every async command. Wait on observable business/element conditions; never catch command errors into a pass.
3. Isolate session, identity, and business keys per worker with setup/cleanup hooks. Cover supplied platform/browser matrix only; missing scope remains unknown.
4. Preserve test/worker/session/capability IDs, versions, URL, screenshot/logs, and original stack. Separate CONFIG_ERROR, business assertion failures, and environment errors, with diagnosis and CI propagation.
