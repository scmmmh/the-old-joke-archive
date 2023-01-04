import { Selector } from 'testcafe';
import { setupStandardDatabase, getAllRecords, getRecord } from '../database';
import { sessionStoreValue } from '../local-persistence';

fixture('Source Deleting')
    .page `http://localhost:6543/`

test('Delete a source', async t => {
    const objs = await setupStandardDatabase();
    await sessionStoreValue('auth.id', objs.users.provider._id);
    await sessionStoreValue('auth.token', objs.users.provider.tokens[0].token);
    await t
        .navigateTo('http://localhost:6543/')
        .click(Selector('a').withText('Contribute'))
        .click(Selector('a').withText('Contribute Source Data'));
    await t
        .click(Selector('h2').withText('THE DAILY JOKE').parent('li').find('button[aria-label="Delete this source"]'))
        .click(Selector('button').withText('Delete'))
        .expect(Selector('h2').withText('THE DAILY JOKE').exists).notOk();
    const allSources = await getAllRecords('sources');
    await t
        .expect(allSources.obj_rows.length).eql(1);
    let dbSource = null;
    for (let sourceEntry of allSources.obj_rows) {
        const source = await getRecord('sources', sourceEntry.id);
        if (source.title === 'The Daily Joke' && source.creator == objs.users.provider._id) {
            dbSource = source;
        }
    }
    await t
        .expect(dbSource).eql(null);
});

test('Cancel deleting a source', async t => {
    const objs = await setupStandardDatabase();
    await sessionStoreValue('auth.id', objs.users.provider._id);
    await sessionStoreValue('auth.token', objs.users.provider.tokens[0].token);
    await t
        .navigateTo('http://localhost:6543/')
        .click(Selector('a').withText('Contribute'))
        .click(Selector('a').withText('Contribute Source Data'));
    await t
        .click(Selector('h2').withText('THE DAILY JOKE').parent('li').find('button[aria-label="Delete this source"]'))
        .click(Selector('button').withText("Don't delete"))
        .expect(Selector('h2').withText('THE DAILY JOKE').exists).ok();
    const allSources = await getAllRecords('sources');
    await t
        .expect(allSources.obj_rows.length).eql(2);
    let dbSource = null;
    for (let sourceEntry of allSources.obj_rows) {
        const source = await getRecord('sources', sourceEntry.id);
        if (source.title === 'The Daily Joke' && source.creator == objs.users.provider._id) {
            dbSource = source;
        }
    }
    await t
        .expect(dbSource).notEql(null);
});
