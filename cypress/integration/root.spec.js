describe('Landing Page Tests', function() {
    it('Basic header label', function() {
        cy.visit('http://localhost:6543');
        cy.get('header img').should('have.attr', 'alt', 'Are we amused? | The Old Joke Archive')
    });
});
