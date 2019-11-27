describe('Error Pages Test', function() {
    it('404', function() {
        cy.request({url: 'http://localhost:6543/missing', failOnStatusCode: false}).then((response) => {
            expect(response.status).to.eq(404);
        });
    });
    /*it('403', function() {
        cy.request({url: 'http://localhost:6543/admin', failOnStatusCode: false}).then((response) => {
            expect(response.status).to.eq(403);
        });
    });*/
});
