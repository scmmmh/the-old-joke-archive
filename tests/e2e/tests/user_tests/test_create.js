import { Selector } from 'testcafe';
import axios from 'axios';

fixture('User Sign Up')
    .page `http://localhost:6543/`
    .beforeEach(async t => {
        try {
            await axios.delete('http://main:aiZiojoh7Eux@localhost:5984/users');
        } catch {}
        await axios.put('http://main:aiZiojoh7Eux@localhost:5984/users');
    })
    .afterEach(async t => {
        await axios.delete('http://main:aiZiojoh7Eux@localhost:5984/users');
    })

test('Create a first user', async t => {
    await t
        .click(Selector('a').withText('Sign Up'))
        .typeText(Selector('label').withText('E-Mail Address'), 'test@example.com')
        .typeText(Selector('label').withText('Name'), 'A Tester')
        .click(Selector('button').withText('Sign up'))
        .expect(Selector('h1').withText('Signed up to').exists).ok();
    let response = await axios.get('http://main:aiZiojoh7Eux@localhost:5984/users/_all_docs');
    await t
        .expect(response.data.total_rows).eql(1);
    response = await axios.get('http://main:aiZiojoh7Eux@localhost:5984/users/' + response.data.rows[0].id);
    await t
        .expect(response.data.email).eql('test@example.com')
        .expect(response.data.name).eql('A Tester')
        .expect(response.data.groups).eql(['admin'])
});

test('Create a second user', async t => {
    try {
        await axios.delete('http://main:aiZiojoh7Eux@localhost:5984/users');
    } catch {}
    await axios.put('http://main:aiZiojoh7Eux@localhost:5984/users');
    let response = await axios.post('http://main:aiZiojoh7Eux@localhost:5984/users', {'email': 'admin@example.com', 'name': 'Admin User', 'token': 'adminToken', 'groups': ['admin']});
    const admin_id = response.data.id;
    await t
        .click(Selector('a').withText('Sign Up'))
        .typeText(Selector('label').withText('E-Mail Address'), 'test@example.com')
        .typeText(Selector('label').withText('Name'), 'A Tester')
        .click(Selector('button').withText('Sign up'))
        .expect(Selector('h1').withText('Signed up to').exists).ok();
    response = await axios.get('http://main:aiZiojoh7Eux@localhost:5984/users/_all_docs');
    await t
        .expect(response.data.total_rows).eql(2);
    for (const row of response.data.rows) {
        if (row.id !== admin_id) {
            response = await axios.get('http://main:aiZiojoh7Eux@localhost:5984/users/' + row.id);
            await t
                .expect(response.data.email).eql('test@example.com')
                .expect(response.data.name).eql('A Tester')
                .expect(response.data.groups).eql([])
        }
    }
});

test('Fail to create duplicate user', async t => {
    try {
        await axios.delete('http://main:aiZiojoh7Eux@localhost:5984/users');
    } catch {}
    await axios.put('http://main:aiZiojoh7Eux@localhost:5984/users');
    let response = await axios.post('http://main:aiZiojoh7Eux@localhost:5984/users', {'email': 'admin@example.com', 'name': 'Admin User', 'token': 'adminToken', 'groups': ['admin']});
    await t
        .click(Selector('a').withText('Sign Up'))
        .typeText(Selector('label').withText('E-Mail Address'), 'admin@example.com')
        .typeText(Selector('label').withText('Name'), 'A Tester')
        .click(Selector('button').withText('Sign up'))
        .expect(Selector('h1').withText('Signed up to').exists).notOk()
        .expect(Selector('span').withText('This e-mail address is already registered').exists).ok();
});

test('Fail to create with an empty e-mail address', async t => {
    try {
        await axios.delete('http://main:aiZiojoh7Eux@localhost:5984/users');
    } catch {}
    await axios.put('http://main:aiZiojoh7Eux@localhost:5984/users');
    await t
        .click(Selector('a').withText('Sign Up'))
        .typeText(Selector('label').withText('Name'), 'A Tester')
        .click(Selector('button').withText('Sign up'))
        .expect(Selector('h1').withText('Signed up to').exists).notOk()
        .expect(Selector('span').withText('Empty values not allowed').exists).ok();
});

test('Fail to create with an empty name', async t => {
    try {
        await axios.delete('http://main:aiZiojoh7Eux@localhost:5984/users');
    } catch {}
    await axios.put('http://main:aiZiojoh7Eux@localhost:5984/users');
    await t
        .click(Selector('a').withText('Sign Up'))
        .typeText(Selector('label').withText('E-Mail Address'), 'test@example.com')
        .click(Selector('button').withText('Sign up'))
        .expect(Selector('h1').withText('Signed up to').exists).notOk()
        .expect(Selector('span').withText('Empty values not allowed').exists).ok();
});
