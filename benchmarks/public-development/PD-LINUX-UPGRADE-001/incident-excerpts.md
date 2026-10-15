# Synthetic incident excerpts: DocSync upgrade evidence exercise

Classification: `PUBLIC_DEVELOPMENT`; `SYNTHETIC_SCENARIO_MATERIAL`;
`NOT_OPERATIONAL_EVIDENCE`; `NOT_EXECUTED`.

These are original synthetic excerpts for an offline regression/evidence-design
exercise.  They do not describe a real incident,
customer, host, build, outage, test execution, defect, recovery, or release.

## Excerpt A — maintenance note

```text
2026-09-18 02:10Z | host=lab-node-b | operator note: “member restarted during upgrade; cluster looked healthy afterwards”
```

## Excerpt B — log fragment

```text
2026-09-18 02:12Z | build=2.4.0-rc2 | docsyncd | migrated configuration to v2
2026-09-18 02:13Z | build=2.3.6     | docsyncd | service started
```

## Excerpt C — ticket note

```text
2026-09-18 02:20Z | ticket=SIM-42 | “configuration appeared to use port override”
```
