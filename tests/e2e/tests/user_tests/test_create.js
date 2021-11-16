import { Selector, ClientFunction } from 'testcafe';
import { setupEmptyDatabase, setupMinimalDatabase, getAllRecords, getRecord } from '../database';

const getLocation = ClientFunction(() => document.location.href);

fixture('User Sign Up')
    .page `http://localhost:6543/`

test('Create a first user', async t => {
    await setupEmptyDatabase();
    await t
        .click(Selector('a').withText('Sign Up'))
        .typeText(Selector('label').withText('E-Mail Address'), 'test@example.com')
        .typeText(Selector('label').withText('Name'), 'A Tester')
        .click(Selector('button').withText('Sign up'))
        .expect(Selector('h1').withText('Signed up to').exists).ok();
    const allUsers = await getAllRecords('users');
    await t
        .expect(allUsers.total_rows).eql(1);
    let dbUser = await getRecord('users', allUsers.rows[0].id);
    await t
        .expect(dbUser.email).eql('test@example.com')
        .expect(dbUser.name).eql('A Tester')
        .expect(dbUser.groups).eql(['admin'])
        .expect(dbUser.status).eql('new');
    await t
        .navigateTo('http://localhost:6543/app/user/confirm?id=' + dbUser._id + '&token=' + dbUser.token)
        .expect(Selector('h1').withText('account confirmed').exists).ok()
        .typeText(Selector('label').withExactText('Password'), 'test')
        .typeText(Selector('label').withText('Confirm Password'), 'test')
        .click(Selector('button').withText('Set your password'))
        .expect(getLocation()).eql('http://localhost:6543/app');
    dbUser = await getRecord('users', allUsers.rows[0].id);
        await t
            .expect(dbUser.status).eql('active');
    });

test('Create a second user', async t => {
    const objs = await setupMinimalDatabase();
    await t
        .click(Selector('a').withText('Sign Up'))
        .typeText(Selector('label').withText('E-Mail Address'), 'test@example.com')
        .typeText(Selector('label').withText('Name'), 'A Tester')
        .click(Selector('button').withText('Sign up'))
        .expect(Selector('h1').withText('Signed up to').exists).ok();
    const allUsers = await getAllRecords('users');
    await t
        .expect(allUsers.total_rows).eql(2);
    let dbUser = null;
    for (const row of allUsers.rows) {
        if (row.id !== objs.admin.id) {
            dbUser = await getRecord('users', row.id);
            break;
        }
    }
    await t
        .expect(dbUser.email).eql('test@example.com')
        .expect(dbUser.name).eql('A Tester')
        .expect(dbUser.groups).eql([])
        .expect(dbUser.status).eql('new');
    await t
        .navigateTo('http://localhost:6543/app/user/confirm?id=' + dbUser._id + '&token=' + dbUser.token)
        .expect(Selector('h1').withText('account confirmed').exists).ok()
        .typeText(Selector('label').withExactText('Password'), 'test')
        .typeText(Selector('label').withText('Confirm Password'), 'test')
        .click(Selector('button').withText('Set your password'))
        .expect(getLocation()).eql('http://localhost:6543/app');
    for (const row of allUsers.rows) {
        if (row.id !== objs.admin.id) {
            dbUser = await getRecord('users', row.id);
            break;
        }
    }
    await t
        .expect(dbUser.status).eql('active');
});

test('Fail to create duplicate user', async t => {
    const objs = await setupMinimalDatabase();
    await t
        .click(Selector('a').withText('Sign Up'))
        .typeText(Selector('label').withText('E-Mail Address'), 'admin@example.com')
        .typeText(Selector('label').withText('Name'), 'A Tester')
        .click(Selector('button').withText('Sign up'))
        .expect(Selector('h1').withText('Signed up to').exists).notOk()
        .expect(Selector('span').withText('This e-mail address is already registered').exists).ok();
});

test('Fail to create with an empty e-mail address', async t => {
    await setupEmptyDatabase();
    await t
        .click(Selector('a').withText('Sign Up'))
        .typeText(Selector('label').withText('Name'), 'A Tester')
        .click(Selector('button').withText('Sign up'))
        .expect(Selector('h1').withText('Signed up to').exists).notOk()
        .expect(Selector('span').withText('Empty values not allowed').exists).ok();
});

test('Fail to create with an empty name', async t => {
    await setupEmptyDatabase();
    await t
        .click(Selector('a').withText('Sign Up'))
        .typeText(Selector('label').withText('E-Mail Address'), 'test@example.com')
        .click(Selector('button').withText('Sign up'))
        .expect(Selector('h1').withText('Signed up to').exists).notOk()
        .expect(Selector('span').withText('Empty values not allowed').exists).ok();
});

test('Fail to set mismatching password', async t => {
    await setupEmptyDatabase();
    await t
        .click(Selector('a').withText('Sign Up'))
        .typeText(Selector('label').withText('E-Mail Address'), 'test@example.com')
        .typeText(Selector('label').withText('Name'), 'A Tester')
        .click(Selector('button').withText('Sign up'))
        .expect(Selector('h1').withText('Signed up to').exists).ok();
    const allUsers = await getAllRecords('users');
    await t
        .expect(allUsers.total_rows).eql(1);
    let dbUser = await getRecord('users', allUsers.rows[0].id);
    await t
        .expect(dbUser.email).eql('test@example.com')
        .expect(dbUser.name).eql('A Tester')
        .expect(dbUser.groups).eql(['admin'])
        .expect(dbUser.status).eql('new');
    await t
        .navigateTo('http://localhost:6543/app/user/confirm?id=' + dbUser._id + '&token=' + dbUser.token)
        .expect(Selector('h1').withText('account confirmed').exists).ok()
        .typeText(Selector('label').withExactText('Password'), 'test')
        .typeText(Selector('label').withText('Confirm Password'), 'testing')
        .click(Selector('button').withText('Set your password'))
        .expect(Selector('span').withText('The two passwords do not match').exists).ok();
});

test('Fail to set empty password', async t => {
    await setupEmptyDatabase();
    await t
        .click(Selector('a').withText('Sign Up'))
        .typeText(Selector('label').withText('E-Mail Address'), 'test@example.com')
        .typeText(Selector('label').withText('Name'), 'A Tester')
        .click(Selector('button').withText('Sign up'))
        .expect(Selector('h1').withText('Signed up to').exists).ok();
    const allUsers = await getAllRecords('users');
    await t
        .expect(allUsers.total_rows).eql(1);
    let dbUser = await getRecord('users', allUsers.rows[0].id);
    await t
        .expect(dbUser.email).eql('test@example.com')
        .expect(dbUser.name).eql('A Tester')
        .expect(dbUser.groups).eql(['admin'])
        .expect(dbUser.status).eql('new');
    await t
        .navigateTo('http://localhost:6543/app/user/confirm?id=' + dbUser._id + '&token=' + dbUser.token)
        .expect(Selector('h1').withText('account confirmed').exists).ok()
        .click(Selector('button').withText('Set your password'))
        .expect(Selector('span').withText('Empty values not allowed').exists).ok();
});
