import { Selector } from 'testcafe';
import { setupStandardDatabase, getRecord } from '../database';
import { localLoadValue, sessionLoadValue } from '../local-persistence';

fixture('User Log Out')
    .page `http://localhost:6543/`

test('Log the user out', async t => {
    const objs = await setupStandardDatabase();
    const dbUser = await getRecord('users', objs.user1.id);
    await t
        .navigateTo('http://localhost:6543/app/user/log-in?email=' + dbUser.email + '&token=' + dbUser.token + '&remember=true')
        .expect(Selector('a').withText('User One').exists).ok()
        .click(Selector('button').withText('Log out'))
        .expect(Selector('a').withText('User One').exists).notOk();
});
