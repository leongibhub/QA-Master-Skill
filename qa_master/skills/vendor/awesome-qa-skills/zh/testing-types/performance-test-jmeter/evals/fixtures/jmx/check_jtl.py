import argparse, csv, math
p=argparse.ArgumentParser()
p.add_argument('jtl')
p.add_argument('--expected-samples',type=int,required=True)
p.add_argument('--p95-ms',type=float,required=True)
p.add_argument('--error-percent',type=float,required=True)
a=p.parse_args()
if a.expected_samples <= 0 or a.p95_ms <= 0 or not 0 <= a.error_percent <= 100:
    p.error('invalid project sample count or gates')
with open(a.jtl,newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
assert len(rows)==a.expected_samples, f'wrong sample count: {len(rows)} != {a.expected_samples}'
assert all(r['success'] in ('true','false') for r in rows),'invalid success field'
times=sorted(float(r['elapsed']) for r in rows)
p95=times[math.ceil(0.95*len(times))-1]
error=100*sum(r['success']=='false' for r in rows)/len(rows)
print(f'samples={len(rows)} p95_ms={p95} error_percent={error}')
assert p95 <= a.p95_ms, 'latency gate failed'
assert error <= a.error_percent, 'error gate failed'
