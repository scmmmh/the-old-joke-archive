import { Selector } from 'testcafe';
import { setupStandardDatabase, getRecord } from '../database';

fixture('User Log Out')
    .page `http://localhost:6543/`

test('Log the user out', async t => {
    const objs = await setupStandardDatabase();
    await t
        .click(Selector('a').withText('Log in'))
        .typeText(Selector('label').withText('E-Mail Address'), 'user1@oldjokearchive.com')
        .typeText(Selector('label').withText('Password'), 'user1pwd')
        .click(Selector('label').withText('Remember me'))
        .click(Selector('button').withText('Log in'))
        .expect(Selector('a').withText('User One').exists).ok()
        .click(Selector('button').withText('Log out'))
        .expect(Selector('a').withText('User One').exists).notOk();
});
