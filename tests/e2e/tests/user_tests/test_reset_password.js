import { Selector } from 'testcafe';
import { setupStandardDatabase, getRecord } from '../database';

fixture('Reset password')
    .page `http://localhost:6543/`

test('Reset password', async t => {
    const objs = await setupStandardDatabase();
    await t
        .click(Selector('a').withText('Log in'))
        .click(Selector('a').withText('Reset your password'))
        .typeText(Selector('label').withText('E-Mail Address'), 'user1@example.com')
        .click(Selector('button').withText('Reset password'))
        .expect(Selector('p').withText('Your password has been reset').exists).ok();
    const dbUser = await getRecord('users', objs.users.user1._id);
    await t
        .expect(dbUser.tokens[0].token).notEql(objs.users.user1.tokens[0].token)
        .expect(dbUser.tokens.length).eql(1)
    await t
        .navigateTo('http://localhost:6543/app/user/confirm?id=' + dbUser._id + '&token=' + dbUser.tokens[0].token + '&action=reset-password')
        .typeText(Selector('label').withText('Password'), 'newPassword')
        .typeText(Selector('label').withText('Confirm Password'), 'newPassword')
        .click(Selector('button').withText('Set your password'))
        .expect(Selector('a').withText('User One').exists).ok();
});

test('Reset password fails invalid password', async t => {
    const objs = await setupStandardDatabase();
    await t
        .click(Selector('a').withText('Log in'))
        .click(Selector('a').withText('Reset your password'))
        .typeText(Selector('label').withText('E-Mail Address'), 'user1@example.com')
        .click(Selector('button').withText('Reset password'))
        .expect(Selector('p').withText('Your password has been reset').exists).ok();
    const dbUser = await getRecord('users', objs.users.user1._id);
    await t
        .expect(dbUser.tokens[0].token).notEql(objs.users.user1.tokens[0].token)
        .expect(dbUser.tokens.length).eql(1)
    await t
        .navigateTo('http://localhost:6543/app/user/confirm?id=' + dbUser._id + '&token=' + dbUser.tokens[0].token + '&action=reset-password')
        .click(Selector('button').withText('Set your password'))
        .expect(Selector('span').withText('Empty values not allowed').exists).ok();
});

test('Reset password fails incorrect confirmation', async t => {
    const objs = await setupStandardDatabase();
    await t
        .click(Selector('a').withText('Log in'))
        .click(Selector('a').withText('Reset your password'))
        .typeText(Selector('label').withText('E-Mail Address'), 'user1@example.com')
        .click(Selector('button').withText('Reset password'))
        .expect(Selector('p').withText('Your password has been reset').exists).ok();
    const dbUser = await getRecord('users', objs.users.user1._id);
    await t
        .expect(dbUser.tokens[0].token).notEql(objs.users.user1.tokens[0].token)
        .expect(dbUser.tokens.length).eql(1)
    await t
        .navigateTo('http://localhost:6543/app/user/confirm?id=' + dbUser._id + '&token=' + dbUser.tokens[0].token + '&action=reset-password')
        .typeText(Selector('label').withText('Password'), 'newPassword')
        .typeText(Selector('label').withText('Confirm Password'), 'incorrectPassword')
        .click(Selector('button').withText('Set your password'))
        .expect(Selector('span').withText('The two passwords do not match').exists).ok();
});
