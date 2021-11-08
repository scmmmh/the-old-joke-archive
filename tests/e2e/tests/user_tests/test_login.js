import { Selector } from 'testcafe';
import { setupStandardDatabase, getRecord } from '../database';
import { localLoadValue, sessionLoadValue } from '../local-persistence';

fixture('User Log In')
    .page `http://localhost:6543/`

test('Login flow (remember)', async t => {
    const objs = await setupStandardDatabase();
    await t
        .click(Selector('a').withText('Log in'))
        .typeText(Selector('label').withText('E-Mail Address'), 'test1@example.com')
        .click(Selector('label').withText('Remember me'))
        .click(Selector('button').withText('Log in'))
        .expect(Selector('h1').withText('Logged in to').exists).ok();
    const dbUser = await getRecord('users', objs.user1.id);
    await t.
        expect(dbUser.token).notEql(objs.user1.token);
    await t
        .navigateTo('http://localhost:6543/app/user/log-in?email=' + dbUser.email + '&token=' + dbUser.token + '&remember=true')
        .expect(Selector('a').withText('User One').exists).ok();
    await t
        .expect(await localLoadValue('auth.token')).eql(dbUser.token)
        .expect(await sessionLoadValue('auth.token')).eql(undefined);
});

test('Login flow (do not remember)', async t => {
    const objs = await setupStandardDatabase();
    await t
        .click(Selector('a').withText('Log in'))
        .typeText(Selector('label').withText('E-Mail Address'), 'test1@example.com')
        .click(Selector('button').withText('Log in'))
        .expect(Selector('h1').withText('Logged in to').exists).ok();
    const dbUser = await getRecord('users', objs.user1.id);
    await t.
        expect(dbUser.token).notEql(objs.user1.token);
    await t
        .navigateTo('http://localhost:6543/app/user/log-in?email=' + dbUser.email + '&token=' + dbUser.token + '&remember=false')
        .expect(Selector('a').withText('User One').exists).ok();
    await t
        .expect(await localLoadValue('auth.token')).eql(undefined)
        .expect(await sessionLoadValue('auth.token')).eql(dbUser.token);
});

test('Login step 1 fail missing e-mail', async t => {
    await setupStandardDatabase();
    await t
        .click(Selector('a').withText('Log in'))
        .typeText(Selector('label').withText('E-Mail Address'), 'does-not-exist@example.com')
        .click(Selector('button').withText('Log in'))
        .expect(Selector('span').withText('This e-mail address is not registered or the token is no longer valid').exists).ok();
});

test('Login step 2 fail missing e-mail', async t => {
    const objs = await setupStandardDatabase();
    await t
        .navigateTo('http://localhost:6543/app/user/log-in?email=does-not-exist@example.com&token=' + objs.user1.token + '&remember=false')
        .expect(Selector('span').withText('The e-mail address does not exist or the token is no longer valid').exists).ok();
});

test('Login step 2 fail incorrect token', async t => {
    const objs = await setupStandardDatabase();
    await t
        .navigateTo('http://localhost:6543/app/user/log-in?email=' + objs.user1.id + '&token=incorrect-token&remember=false')
        .expect(Selector('span').withText('The e-mail address does not exist or the token is no longer valid').exists).ok();
});
