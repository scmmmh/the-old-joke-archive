import { Selector } from 'testcafe';
import { setupStandardDatabase, getAllRecords, getRecord } from '../database';
import { sessionStoreValue } from '../local-persistence';

fixture('Source Creation')
    .page `http://localhost:6543/`

test('Create a source', async t => {
    const objs = await setupStandardDatabase();
    await sessionStoreValue('auth.id', objs.users.provider._id);
    await sessionStoreValue('auth.token', objs.users.provider.tokens[0].token);
    await t
        .navigateTo('http://localhost:6543/')
        .click(Selector('a').withText('Contribute'))
        .click(Selector('a').withText('Contribute Source Data'))
        .click(Selector('label').withText('Publication Type'))
        .click(Selector('option').withText('Book'))
        .typeText(Selector('label').withText('Publication Title'), 'The Big Book of Bad Jokes')
        .typeText(Selector('label').withText('Column / Chapter Title'), 'Nothing as bad as a bad laugh')
        .typeText(Selector('label').withText('Publication Date'), '1860-06')
        .typeText(Selector('label').withText('Publisher'), 'Groan Publishing')
        .typeText(Selector('label').withText('Publication Location'), 'London, UK')
        .typeText(Selector('label').withText('Page Numbers'), '75')
        .setFilesToUpload(Selector('label').withText('Source Image').find('input'), ['../../../toja/server/handlers/test/example-source1.png'])
        .click(Selector('label').withText('Please confirm'))
        .click(Selector('button').withText('Add source'))
        .expect(Selector('h2').withText('THE BIG BOOK OF BAD JOKES').exists).ok();
    const allSources = await getAllRecords('sources');
    await t
        .expect(allSources.obj_rows.length).eql(3);
    let dbSource = null;
    for (let sourceEntry of allSources.obj_rows) {
        const source = await getRecord('sources', sourceEntry.id);
        if (source.title === 'The Big Book of Bad Jokes' && source.creator == objs.users.provider._id) {
            dbSource = source;
        }
    }
    await t
        .expect(dbSource.type).eql('book')
        .expect(dbSource.subtitle).eql('Nothing as bad as a bad laugh')
        .expect(dbSource.date).eql('1860-06')
        .expect(dbSource.publisher).eql('Groan Publishing')
        .expect(dbSource.location).eql('London, UK')
        .expect(dbSource.page_numbers).eql('75');
});

test('Fail to create a source without confirmation', async t => {
    const objs = await setupStandardDatabase();
    await sessionStoreValue('auth.id', objs.users.provider._id);
    await sessionStoreValue('auth.token', objs.users.provider.tokens[0].token);
    await t
        .navigateTo('http://localhost:6543/')
        .click(Selector('a').withText('Contribute'))
        .click(Selector('a').withText('Contribute Source Data'))
        .click(Selector('button').withText('Add source'))
        .expect(Selector('span').withText('Please confirm that you are permitted to upload the file under the given license').exists).ok();
});

test('Fail to create a source without metadata', async t => {
    const objs = await setupStandardDatabase();
    await sessionStoreValue('auth.id', objs.users.provider._id);
    await sessionStoreValue('auth.token', objs.users.provider.tokens[0].token);
    await t
        .navigateTo('http://localhost:6543/')
        .click(Selector('a').withText('Contribute'))
        .click(Selector('a').withText('Contribute Source Data'))
        .click(Selector('label').withText('Please confirm'))
        .click(Selector('button').withText('Add source'))
        .expect(Selector('span').withText('Empty values not allowed').exists).ok();
});
