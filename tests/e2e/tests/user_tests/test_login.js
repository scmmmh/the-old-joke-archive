import { Selector } from 'testcafe';
import { setupStandardDatabase, getRecord } from '../database';
import { localLoadValue, sessionLoadValue } from '../local-persistence';

fixture('User Log In')
    .page `http://localhost:6543/`

test('Login user (remember)', async t => {
    const objs = await setupStandardDatabase();
    await t
        .click(Selector('a').withText('Log in'))
        .typeText(Selector('label').withText('E-Mail Address'), 'user1@oldjokearchive.com')
        .typeText(Selector('label').withText('Password'), 'user1pwd')
        .click(Selector('label').withText('Remember me'))
        .click(Selector('button').withText('Log in'))
        .expect(Selector('a').withText('User One').exists).ok();
    const dbUser = await getRecord('users', objs.users.one._id);
    await t.
        expect(dbUser.tokens[0].token).notEql(objs.users.one.tokens[0].token);
    await t
        .expect(await localLoadValue('auth.token')).eql(dbUser.tokens[0].token)
        .expect(await sessionLoadValue('auth.token')).notOk();
});

test('Login user (do not remember)', async t => {
    const objs = await setupStandardDatabase();
    await t
        .click(Selector('a').withText('Log in'))
        .typeText(Selector('label').withText('E-Mail Address'), 'user1@oldjokearchive.com')
        .typeText(Selector('label').withText('Password'), 'user1pwd')
        .click(Selector('button').withText('Log in'))
        .expect(Selector('a').withText('User One').exists).ok();
    const dbUser = await getRecord('users', objs.users.one._id);
    await t.
        expect(dbUser.tokens[0].token).notEql(objs.users.one.tokens[0].token);
    await t
        .expect(await localLoadValue('auth.token')).notOk()
        .expect(await sessionLoadValue('auth.token')).eql(dbUser.tokens[0].token);
});


test('Login fail missing e-mail', async t => {
    await setupStandardDatabase();
    await t
        .click(Selector('a').withText('Log in'))
        .typeText(Selector('label').withText('Password'), 'user1pwd')
        .click(Selector('button').withText('Log in'))
        .expect(Selector('span').withText('This e-mail address is not registered, the password is incorrect, or the account is locked due to inactivity.').exists).ok();
});

test('Login fail missing password', async t => {
    await setupStandardDatabase();
    await t
        .click(Selector('a').withText('Log in'))
        .typeText(Selector('label').withText('E-Mail Address'), 'user1@oldjokearchive.com')
        .click(Selector('button').withText('Log in'))
        .expect(Selector('span').withText('This e-mail address is not registered, the password is incorrect, or the account is locked due to inactivity.').exists).ok();
});

test('Login fail incorrect e-mail', async t => {
    await setupStandardDatabase();
    await t
        .click(Selector('a').withText('Log in'))
        .typeText(Selector('label').withText('E-Mail Address'), 'incorrect-email@oldjokearchive.com')
        .typeText(Selector('label').withText('Password'), 'user1pwd')
        .click(Selector('button').withText('Log in'))
        .expect(Selector('span').withText('This e-mail address is not registered, the password is incorrect, or the account is locked due to inactivity.').exists).ok();
});

test('Login fail incorrect password', async t => {
    await setupStandardDatabase();
    await t
        .click(Selector('a').withText('Log in'))
        .typeText(Selector('label').withText('E-Mail Address'), 'user1@oldjokearchive.com')
        .typeText(Selector('label').withText('Password'), 'user2pwd')
        .click(Selector('button').withText('Log in'))
        .expect(Selector('span').withText('This e-mail address is not registered, the password is incorrect, or the account is locked due to inactivity.').exists).ok();
});

test('Login fail new user', async t => {
    await setupStandardDatabase();
    await t
        .click(Selector('a').withText('Log in'))
        .typeText(Selector('label').withText('E-Mail Address'), 'user_new@oldjokearchive.com')
        .typeText(Selector('label').withText('Password'), 'userNewpwd')
        .click(Selector('button').withText('Log in'))
        .expect(Selector('span').withText('This e-mail address is not registered, the password is incorrect, or the account is locked due to inactivity.').exists).ok();
});

test('Login fail locked user', async t => {
    await setupStandardDatabase();
    await t
        .click(Selector('a').withText('Log in'))
        .typeText(Selector('label').withText('E-Mail Address'), 'user_locked@oldjokearchive.com')
        .typeText(Selector('label').withText('Password'), 'userLockedpwd')
        .click(Selector('button').withText('Log in'))
        .expect(Selector('span').withText('This e-mail address is not registered, the password is incorrect, or the account is locked due to inactivity.').exists).ok();
});

test('Login fail blocked user', async t => {
    await setupStandardDatabase();
    await t
        .click(Selector('a').withText('Log in'))
        .typeText(Selector('label').withText('E-Mail Address'), 'user_blocked@oldjokearchive.com')
        .typeText(Selector('label').withText('Password'), 'userBlockedpwd')
        .click(Selector('button').withText('Log in'))
        .expect(Selector('span').withText('This e-mail address is not registered, the password is incorrect, or the account is locked due to inactivity.').exists).ok();
});
