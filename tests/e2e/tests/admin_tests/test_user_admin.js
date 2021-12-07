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
        .expect(Selector('table td').withText('user1@example.com').exists).ok();
    await t
        .click(Selector('table td').withText('user1@example.com').parent('tr').find('button[aria-label="Edit this user"]'))
        .typeText(Selector('table td label').withText('E-Mail Address').parent('tr').find('input'), 'user2@example.com', {replace: true})
        .click(Selector('table td label').withText('E-Mail Address').parent('tr').find('button[aria-label="Save changes"]'))
        .expect(Selector('table td').withText('user2@example.com').exists).ok();
    const user1 = await getRecord('users', objs.users.user1._id);
    await t
        .expect(user1.email).eql('user2@example.com');
});
