# DocSync Server 2.4.0 release notes

Classification: `PUBLIC_DEVELOPMENT`; execution state: `NOT_EXECUTED`.
This is original scenario material for offline QA design.  It is not a record
of a deployed release, an approved production change, or operational evidence.

## Change scope

DocSync Server 2.4.0 changes the on-disk service configuration from schema v1
to schema v2.  The change affects the `docsyncd` service process, its local
configuration files, and clustered membership metadata.  The release is for
three-member clusters only; it does not describe a single-node procedure.

## Supported upgrade path

- Upgrade is supported from DocSync Server 2.3.6 to 2.4.0 on x86_64 Ubuntu
  22.04 with kernel 5.15, and on x86_64 Rocky Linux 9 with kernel 5.14.
- Two remaining 2.3.6 members may communicate with one 2.4.0 member while a
  three-member rolling upgrade is in progress.  The document does not state
  compatibility with any other server version.
- Take one member out of service, upgrade it, wait for it to report ready, and
  return it to service before beginning the next member.  At least two voting
  members must remain ready during this procedure.
- A ready upgraded member exposes `GET /healthz` with HTTP 200 and JSON member
  `ready: true`.  No latency, error-rate, disk, inode, memory, CPU, or network
  threshold is supplied.

## Migration and rollback boundary

- At first 2.4.0 start, the service reads `config/doc-sync.yaml` schema v1 and
  writes a schema-v2 copy at `data/config-v2.yaml`.  It preserves the v1 input
  file and does not state whether other local files are changed.
- Rolling back an upgraded member is supported only before that member has
  migrated membership metadata.  The operator restores the saved v1
  configuration, reinstalls 2.3.6, and restarts that member.
- The release does not define rollback after membership metadata migration,
  backup integrity verification, a data reconciliation query, or an RPO/RTO.

## Client and evidence boundary

- The 2.4.0 server supports DocSync CLI 2.3 and 2.4 on the listed operating
  systems.  Browser, database, proxy and third-party client support is not
  stated.
- This release note does not authorize an SSH command, restart, config write,
  backup restore, traffic drain, network partition, disk-fill exercise, or a
  test result.
