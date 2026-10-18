describe('business payment oracle', () => {
  for (const user of ['A','B']) it(`isolated ${user}`, () => {
    cy.visit(`/?user=${user}&order=${user}-1&mode=${Cypress.env('MODE') || 'good'}`);
    cy.get('[data-testid="pay"]').click();
    cy.get('[data-testid="state"]').should('have.text','paid');
    cy.get('[data-testid="principal"]').should('have.text',user);
    cy.window().then(win => {expect(win.fixtureRecord()).to.deep.equal({principal:user,orderId:`${user}-1`,amount:20,state:'paid'});});
  });
  afterEach(() => cy.clearLocalStorage());
});
