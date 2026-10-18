const {test, expect} = require('@playwright/test');
for (const user of ['A','B']) test(`isolated ${user}`, async ({page}) => {
  await page.goto(`http://127.0.0.1:4173/?user=${user}&order=${user}-1&mode=${process.env.MODE || 'good'}`);
  try {
    await page.getByRole('button',{name:'Pay',exact:true}).click();
    await expect(page.getByTestId('state')).toHaveText('paid');
    await expect(page.getByTestId('principal')).toHaveText(user);
    expect(await page.evaluate(() => window.fixtureRecord())).toEqual({principal:user,orderId:`${user}-1`,amount:20,state:'paid'});
  } finally {await page.evaluate(() => localStorage.clear());}
});
