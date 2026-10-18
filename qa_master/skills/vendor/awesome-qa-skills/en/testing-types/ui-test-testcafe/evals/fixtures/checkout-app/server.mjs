import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {dirname, join} from 'node:path';
const base = dirname(fileURLToPath(import.meta.url));
const port = Number(process.env.FIXTURE_PORT || 4173);
const server = createServer(async (req,res) => {
  const path = new URL(req.url,'http://127.0.0.1').pathname;
  if (path === '/unavailable') {res.writeHead(503); res.end('fixture load failure'); return;}
  const file = {'/':'index.html','/index.html':'index.html','/receipt.html':'receipt.html'}[path];
  if (!file) {res.writeHead(404); res.end('not found'); return;}
  try {res.writeHead(200,{'Content-Type':'text/html; charset=utf-8'}); res.end(await readFile(join(base,file)));}
  catch (error) {res.writeHead(500); res.end('fixture unavailable');}
});
server.listen(port,'127.0.0.1',() => console.log(`fixture http://127.0.0.1:${port}`));
for (const signal of ['SIGINT','SIGTERM']) process.on(signal,() => server.close(() => process.exit(0)));
