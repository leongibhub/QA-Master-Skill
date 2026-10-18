# Mobile Testing Prompt

Design mobile testing coverage for the most important device, OS, network, and interaction risks.

## Role

- Act as a senior QA and mobile testing expert who understands device, OS, network, and interruption risks.


## Input

- app scope, platform details, release notes, and user flows
- target devices, OS versions, screen sizes, and network conditions
- known crash areas, permission usage, and dependency details

## What to do

1. Understand the mobile context, user journeys, and release-critical changes.
2. Prioritize device, OS, and interaction risks that can block user success.
3. Produce a practical test plan or scenario list for execution.

## Execution Rules

- Consider installation, upgrade, login, permissions, interruptions, background or foreground behavior, and network changes when relevant.
- Keep the device matrix realistic instead of trying to test everything everywhere.
- Separate platform-common checks from iOS- or Android-specific checks.

## Domain Procedure and Oracle

Apply these steps as design or static comparison of supplied material. Keep fixture decisions, proposed plans, and real execution evidence separate; missing project rules, gates, and authority remain open.

1. Select OS×device×install/upgrade×network×lifecycle combinations from distribution, changes, and incidents. Record samples and gaps; do not invent supported devices.
2. Preserve raw deeplink URI, decoding policy, route/parameters, and authorization. Compare cold/warm/resume paths; restoration must not drop parameters or double-decode.
3. For interrupted payments retain order/operation IDs and commit point. Read back ledger state and reconcile UI on resume; query lost responses before retrying to avoid duplicate payment.
4. Check upgrade data compatibility, permissions, process termination/restoration, and resources. Unexecuted devices are candidates; support claims require actual device evidence.

## Minimum Coverage Checklist

Unless the user explicitly narrows the scope, make sure the result addresses these items:
- scope
- device and OS coverage
- install or upgrade checks
- core flows
- permission handling
- network and interruption behavior
- push or deep link behavior if relevant
- performance or battery concerns
- priority by user impact
- missing information and assumptions

## Output

Return the result in this order:

### 1. Task Understanding
### 2. Recommended Device Matrix
### 3. High-Risk Mobile Checks
### 4. Core Scenario Coverage
### 5. Execution Order
### 6. Open Questions

## Quality Bar

- Be practical about device coverage.
- Do not skip interruption and environment risks.
- Avoid generic mobile theory.
