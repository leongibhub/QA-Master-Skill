# Minimum Application and Business-Failure Control

This fixture uses local synthetic orders without a payment service. Use the project-locked framework/Node/browser dependencies; do not implicitly install or upgrade. Specs are for review and explicit execution, never Skill installation.

Start `node server.mjs` in a separate terminal in this directory and stop it with Ctrl-C after checks. Port4173 belongs to this fixture only; keep server and spec addresses aligned if changed.

```sh
MODE=good npx testcafe chrome:headless checkout.test.js
MODE=bug npx testcafe chrome:headless checkout.test.js
```

good should pass; bug keeps title Checkout while order stays pending and should exit nonzero. timeout never updates state and should fail. A/B use distinct business keys; specs check persisted amount/principal/state and clean up. Wait limits such as3s belong to fixture mechanics, not product SLOs.

Runtime evidence separately records actual framework/browser versions, command/exit, failure artifacts and resource cleanup. Syntax checks are not framework execution.

API reference: [Official documentation](https://testcafe.io/documentation/402655/reference/testcafe-api/runner/run).
