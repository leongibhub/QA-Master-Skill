# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Query Q belongs to tenant A; known relevant documents are {d1,d2,d3}; k=2 with no duplicates. R-1 retrieves current tenant-A d1/d2. R-2 retrieves d1 and unauthorized tenant-B d9 even if relevant. R-3 retrieves old d1 when latest is required. R-4 retrieves correct d1/d2 but generation changes 14 days to 30. R-5 claims full recall without complete labels. Decide RETRIEVAL_VALID/AUTHORIZATION_FAIL/STALE/GENERATION_FAIL/UNKNOWN and calculate R-1 precision/recall numerators and denominators.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| R-1 | RETRIEVAL_VALID |
| R-2 | AUTHORIZATION_FAIL |
| R-3 | STALE |
| R-4 | GENERATION_FAIL |
| R-5 | UNKNOWN |

| METRIC | VALUE |
| --- | --- |
| precision_numerator | 2 |
| precision_denominator | 2 |
| recall_numerator | 2 |
| recall_denominator | 3 |

## Verification Method

1. Version queries, relevance annotations, document/chunk units, labelers and corpus. Recall@k uses the known relevant set; Precision@k uses actual returns with the supplied duplicate policy.
2. Check rank, relevance, permission/tenant filters, freshness and version for each hit. Relevant but unauthorized hits are failures; high scores cannot cure stale content.
3. Compare configurations under matched queries, index, filters and resources. Incomplete relevant sets allow proxy measurements, not claims of complete recall.
4. Distinguish missing retrieval from correct retrieval followed by wrong generation. Missing generation output cannot locate its failure; absent labels leave UNKNOWN.
