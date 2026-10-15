# Draft DocSync Server rolling-upgrade runbook

Classification: `PUBLIC_DEVELOPMENT`; `DRAFT_UNAPPROVED`; `NOT_EXECUTED`.
This is ordinary operational source material, not an approved production runbook.

## Intended sequence

1. Record the cluster member name, installed server version, supported
   operating-system and kernel version, and the identity of the available v1
   configuration backup for the selected member.
2. Confirm that two other voting members are ready before removing the selected
   member from service.  The source does not define a command, traffic-drain
   mechanism, quorum query, or leader-election observer.
3. Install 2.4.0 on the selected member and start `docsyncd`.
4. Treat that member as ready only after its documented `/healthz` response is
   HTTP 200 with `ready: true`; then return it to service and proceed to the
   next member.
5. If the member cannot reach the documented ready state before membership
   metadata migration, restore the saved v1 configuration, reinstall 2.3.6,
   and restart the member.  The source gives no post-rollback health or data
   reconciliation oracle.

## Configuration statement

The operational team must run `docsync config-migrate` before starting a 2.4.0
member.  The command is said to create `data/config-v2.yaml` from
`config/doc-sync.yaml`.  The runbook does not state whether `docsyncd` performs
the same migration automatically, how the command is authorized, its exit-code
meaning, or what happens after a partial migration.

## Configuration precedence and access boundary

For an upgraded member, `DOCSYNC_LISTEN_PORT` takes precedence over
`listen.port` in `config/doc-sync.yaml`.  No default port is specified.  No
source states how environment values are supplied, who may change them, or how
the effective configuration is observed.

No target, account, host list, SSH credential, maintenance window, abort owner,
backup location, data classification, stop condition, or operator authorization
is supplied.  Do not execute any listed activity from this document.
