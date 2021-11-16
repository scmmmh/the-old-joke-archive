import { Selector } from 'testcafe';
import { setupStandardDatabase, getRecord } from '../database';
import { sessionStoreValue } from '../local-persistence';

fixture('Administration Access')
    .page `http://localhost:6543/`

test('Test admin access', async t => {
    const objs = await setupStandardDatabase();
    const dbUser = await getRecord('users', objs.admin.id);
    await sessionStoreValue('auth.id', dbUser.email);
    await sessionStoreValue('auth.token', dbUser.token);
    await t
        .expect(Selector('a').withText('Admin User').exists).ok()
        .click(Selector('a').withExactText('Admin'))
        .expect(Selector('h1').withText('Admin').exists).ok();
});
