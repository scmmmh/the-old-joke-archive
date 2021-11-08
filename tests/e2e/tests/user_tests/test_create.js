import { Selector } from 'testcafe';
import { setupEmptyDatabase, setupMinimalDatabase, getAllRecords, getRecord } from '../database';

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
    const dbUser = await getRecord('users', allUsers.rows[0].id);
    await t
        .expect(dbUser.email).eql('test@example.com')
        .expect(dbUser.name).eql('A Tester')
        .expect(dbUser.groups).eql(['admin'])
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
        for (const row of allUsers.rows) {
        if (row.id !== objs.admin.id) {
            const dbUser = await getRecord('users', row.id);
            await t
                .expect(dbUser.email).eql('test@example.com')
                .expect(dbUser.name).eql('A Tester')
                .expect(dbUser.groups).eql([])
        }
    }
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
