import { Selector } from 'testcafe';
import { setupStandardDatabase } from '../database';
import { sessionStoreValue } from '../local-persistence';

fixture('Administration Access')
    .page `http://localhost:6543/`

test('Test admin access', async t => {
    const objs = await setupStandardDatabase();
    await sessionStoreValue('auth.id', objs.admin._id);
    await sessionStoreValue('auth.token', objs.admin.tokens[0].token);
    await t
        .navigateTo('http://localhost:6543/app')
        .expect(Selector('a').withText('Admin User').exists).ok()
        .click(Selector('a').withExactText('Admin'))
        .expect(Selector('h1').withText('Admin').exists).ok();
});
