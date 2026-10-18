import puppeteer from 'puppeteer';
import assert from 'node:assert/strict';
const browser = await puppeteer.launch({headless:true});
try {
  for (const user of ['A','B']) {
    const context = await browser.createBrowserContext();
    try {
      const page = await context.newPage();
      page.setDefaultTimeout(3000);
      const response = await page.goto(`http://127.0.0.1:4173/?user=${user}&order=${user}-1&mode=${process.env.MODE || 'good'}`);
      assert.ok(response.ok(),'fixture navigation failed');
      await page.click('[data-testid="pay"]');
      try {
        await page.waitForFunction(() => document.querySelector('[data-testid="state"]').textContent === 'paid');
        assert.deepEqual(await page.evaluate(() => window.fixtureRecord()),{principal:user,orderId:`${user}-1`,amount:20,state:'paid'});
        const popup = browser.waitForTarget(target => target.opener() === page.target());
        await page.click('[data-testid="receipt"]');
        const receipt = await (await popup).page();
        await receipt.waitForFunction(() => document.querySelector('[data-testid="receipt-state"]')?.textContent.endsWith(':paid:20'));
        await receipt.close();
      } catch (error) {await page.screenshot({path:`failure-${user}.png`}); console.error(page.url()); throw error;}
    } finally {await context.close();}
  }
} finally {await browser.close();}
