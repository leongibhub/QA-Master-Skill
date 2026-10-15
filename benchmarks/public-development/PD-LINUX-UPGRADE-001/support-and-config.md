# DocSync Server support and configuration reference

Classification: `PUBLIC_DEVELOPMENT`; execution state: `NOT_EXECUTED`.

## Supported platform and service facts

The supported server combinations are:

| Server version | OS | Kernel | Architecture |
|---|---|---|---|
| 2.3.6 | Ubuntu 22.04 | 5.15 | x86_64 |
| 2.4.0 | Ubuntu 22.04 | 5.15 | x86_64 |
| 2.3.6 | Rocky Linux 9 | 5.14 | x86_64 |
| 2.4.0 | Rocky Linux 9 | 5.14 | x86_64 |

The cluster has exactly three voting members.  This document does not specify
leader election, network-partition behavior, replication factor, write
consistency, membership metadata format, capacity limits, or degraded-service
behavior.

## Configuration v2 fields

Schema v2 requires `storage.path` and `listen.port`.  It accepts an optional
`metrics.enabled` boolean.  The reference says 2.4.0 rejects a configuration
that omits either required field, but it does not state the resulting log,
error code, service state, or whether the prior configuration remains usable.

`DOCSYNC_LISTEN_PORT`, if set, takes precedence over `listen.port`; the
reference does not define a default value or an inspection command for the
effective value.  It does not state config-file ownership, file permissions,
SELinux policy, storage free-space/inode requirements, or migration locking
when two operators act concurrently.

## Observable service data

`GET /healthz` returns HTTP 200 and `{"ready": true}` only for a ready member.
No endpoint or log format is documented for schema version, membership metadata,
configuration migration progress, persisted documents, backup contents, or
client protocol negotiation.
