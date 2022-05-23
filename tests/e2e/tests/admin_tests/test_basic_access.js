import { Selector } from 'testcafe';
import { setupMinimalDatabase } from '../database';
import { sessionStoreValue } from '../local-persistence';

fixture('Administration Access')
    .page `http://localhost:6543/`

test('Test admin access', async t => {
    const objs = await setupMinimalDatabase();
    await sessionStoreValue('auth.id', objs.users.admin._id);
    await sessionStoreValue('auth.token', objs.users.admin.tokens[0].token);
    await t
        .navigateTo('http://localhost:6543/app')
        .expect(Selector('a').withText('The Admin').exists).ok()
        .click(Selector('a').withExactText('Admin'))
        .expect(Selector('h1').withText('Admin').exists).ok();
});

test('Test user admin access', async t => {
    const objs = await setupMinimalDatabase();
    await sessionStoreValue('auth.id', objs.users.admin._id);
    await sessionStoreValue('auth.token', objs.users.admin.tokens[0].token);
    await t
        .navigateTo('http://localhost:6543/app')
        .click(Selector('a').withExactText('Admin'))
        .click(Selector('a').withExactText('User Administration'))
        .expect(Selector('table thead th').withText('E-Mail').exists).ok()
        .expect(Selector('table td').withText('admin@oldjokearchive.com').exists).ok();
});
