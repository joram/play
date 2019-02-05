const qaAttr = (selector) => {
  return `[data-cy="${selector}"]`
}

describe('First Battlesnake test', () => {
  it('should show the page to login', () => {
    cy.visit('/')
    cy.getCookie('sessionid').should('not.exist')
    cy.url().should('contain', '/login/')
    cy.get(qaAttr('button-login')).should('have.attr', 'href', '/oauth/login/github/')
  })
})
