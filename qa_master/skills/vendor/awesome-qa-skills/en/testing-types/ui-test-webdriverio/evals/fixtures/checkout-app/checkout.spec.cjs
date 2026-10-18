const assert = require('node:assert/strict');
describe('business payment oracle', () => {
  for (const user of ['A','B']) it(`isolated ${user}`, async () => {
    await browser.reloadSession();
    await browser.url(`http://127.0.0.1:4173/?user=${user}&order=${user}-1&mode=${process.env.MODE || 'good'}`);
    try {
      await $('[data-testid="pay"]').click();
      await browser.waitUntil(async () => (await $('[data-testid="state"]').getText()) === 'paid',{timeout:3000,timeoutMsg:'payment did not reach paid'});
      assert.deepEqual(await browser.execute(() => window.fixtureRecord()),{principal:user,orderId:`${user}-1`,amount:20,state:'paid'});
    } catch (error) {await browser.saveScreenshot(`failure-${user}.png`); console.error(browser.sessionId); throw error;}
    finally {await browser.execute(() => localStorage.clear());}
  });
});
