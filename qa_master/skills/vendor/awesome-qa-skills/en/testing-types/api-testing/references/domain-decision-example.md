# Domain Decision Example

This sanitized synthetic fixture calibrates analysis for this Skill; it is not a real project run or business acceptance record. Numbers and protocols belong to this example only.

## Input

Contract v2: REST refund returns 200 and refunds 20 once; nonempty GraphQL errors means that field failed; cleanup deletes refunds before orders. A-1: refund 200 but GET order cumulative refund=0. A-2: same refund_id returns 200 twice, read-back=20, one ledger entry. A-3: GraphQL HTTP 200 with data.refund=null and nonempty errors. A-4: only a gRPC name, no proto/results. Decide FAIL/PASS/UNKNOWN with business postconditions and cleanup order.

## Per-Item Oracle

| ID | DECISION |
| --- | --- |
| A-1 | FAIL |
| A-2 | PASS |
| A-3 | FAIL |
| A-4 | UNKNOWN |

## Verification Method

1. Branch only for confirmed protocols: REST method/status/schema/idempotency; GraphQL data+errors/null/field permissions; gRPC status/metadata/deadline/stream termination; WebSocket handshake/message IDs/order/reconnect; SOAP WSDL/namespaces/Fault. Do not require unused protocols.
2. Separate contract checks from cross-request business postconditions: create/update→read-back→permission view→repeat/downstream effects. Preserve request IDs, business keys, versions, and evidence.
3. Correct status with wrong persisted balance/state/relationships is a business failure. For asynchronous effects apply project consistency windows, never invented delays.
4. Prepare isolated namespaces/unique business keys, clean in reverse dependency order, and record residuals. Missing authority or real-effect constraints stay blocked.
