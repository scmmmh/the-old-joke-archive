describe('User Session Test', function() {
    it('Login', function() {
        cy.visit('http://localhost:6543/users/login');
    });
    it('Logout', function() {
        cy.visit('http://localhost:6543/users/logout');
    });
    it('Register', function() {
        cy.visit('http://localhost:6543/users/register');
    });
    it('Forgotten Password', function() {
        cy.visit('http://localhost:6543/users/forgotten_password');
    });
});
