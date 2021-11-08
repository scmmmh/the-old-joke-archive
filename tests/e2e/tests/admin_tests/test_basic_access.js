import { Selector } from 'testcafe';
import { setupStandardDatabase, getRecord } from '../database';

fixture('User Log Out')
    .page `http://localhost:6543/`

test('Log the user out', async t => {
    const objs = await setupStandardDatabase();
    const dbUser = await getRecord('users', objs.admin.id);
    await t
        .navigateTo('http://localhost:6543/app/user/log-in?email=' + dbUser.email + '&token=' + dbUser.token + '&remember=true')
        .expect(Selector('a').withText('Admin User').exists).ok()
        .click(Selector('a').withExactText('Admin'))
        .expect(Selector('h1').withText('Admin').exists).ok();
});
