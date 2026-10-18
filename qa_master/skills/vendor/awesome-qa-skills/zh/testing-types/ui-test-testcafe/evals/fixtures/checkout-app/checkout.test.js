import {Selector, ClientFunction} from 'testcafe';
const mode = process.env.MODE || 'good';
for (const user of ['A','B']) {
  fixture(`isolated ${user}`).page(`http://127.0.0.1:4173/?user=${user}&order=${user}-1&mode=${mode}`);
  test('paid business state',async t => {
    try {
      await t.click('[data-testid="pay"]');
      await t.expect(Selector('[data-testid="state"]').innerText).eql('paid');
      const readRecord = ClientFunction(() => window.fixtureRecord());
      await t.expect(await readRecord()).eql({principal:user,orderId:`${user}-1`,amount:20,state:'paid'});
    } finally {await ClientFunction(() => localStorage.clear())();}
  });
}
