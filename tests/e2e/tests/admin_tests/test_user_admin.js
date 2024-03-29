import { Selector } from 'testcafe';
import { setupStandardDatabase, getRecord } from '../database';
import { sessionStoreValue } from '../local-persistence';

fixture('User Administration')
    .page `http://localhost:6543/`

test('Test edit user', async t => {
    const objs = await setupStandardDatabase();
    await sessionStoreValue('auth.id', objs.users.admin._id);
    await sessionStoreValue('auth.token', objs.users.admin.tokens[0].token);
    await t
        .navigateTo('http://localhost:6543/app')
        .click(Selector('a').withExactText('Admin'))
        .click(Selector('a').withExactText('User Administration'))
        .expect(Selector('table td').withText('user1@oldjokearchive.com').exists).ok()
        .click(Selector('table td').withText('user1@oldjokearchive.com').parent('tr').find('button[aria-label="Edit this user"]'))
        .typeText(Selector('table td label').withText('E-Mail Address').parent('td').find('input'), 'user2@oldjokearchive.com', {replace: true})
        .typeText(Selector('table td label').withText('Name').parent('td').find('input'), 'Updated', {replace: true})
        .click(Selector('table td label').withText('Superuser'))
        .click(Selector('table td label').withText('Status'))
        .click(Selector('option[value="inactive"]'))
        .click(Selector('table td label').withText('E-Mail Address').parent('tr').find('button[aria-label="Save changes"]'))
        .expect(Selector('table td').withText('user2@oldjokearchive.com').exists).ok();
    const user1 = await getRecord('users', objs.users.one._id);
    await t
        .expect(user1.email).eql('user2@oldjokearchive.com')
        .expect(user1.name).eql('Updated')
        .expect(user1.groups).eql(['admin'])
        .expect(user1.status).eql('inactive');
});


test('Test delete user', async t => {
    const objs = await setupStandardDatabase();
    await sessionStoreValue('auth.id', objs.users.admin._id);
    await sessionStoreValue('auth.token', objs.users.admin.tokens[0].token);
    await t
        .navigateTo('http://localhost:6543/app')
        .click(Selector('a').withExactText('Admin'))
        .click(Selector('a').withExactText('User Administration'))
        .expect(Selector('table td').withText('user1@oldjokearchive.com').exists).ok()
        .click(Selector('table td').withText('user1@oldjokearchive.com').parent('tr').find('button[aria-label="Delete this user"]'))
        .expect(Selector('table td').withText('user1@oldjokearchive.com').exists).notOk()
    try {
        await getRecord('users', objs.users.one._id);
        await t
            .expect(true).eql(false);
    } catch {
        await t
            .expect(true).eql(true);
    }
});
