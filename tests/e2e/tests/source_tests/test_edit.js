import { Selector } from 'testcafe';
import { setupStandardDatabase, getAllRecords, getRecord } from '../database';
import { sessionStoreValue } from '../local-persistence';

fixture('Source Editing')
    .page `http://localhost:6543/`

test('Edit a source', async t => {
    const objs = await setupStandardDatabase();
    await sessionStoreValue('auth.id', objs.users.provider._id);
    await sessionStoreValue('auth.token', objs.users.provider.tokens[0].token);
    await t
        .navigateTo('http://localhost:6543/')
        .click(Selector('a').withText('Contribute'))
        .click(Selector('a').withText('Contribute Source Data'));
    await t
        .click(Selector('h2').withText('THE DAILY JOKE').parent('li').find('button[aria-label="Edit this source"]'))
        .click(Selector('ul form label').withText('Publication Type'))
        .click(Selector('ul form option').withText('Book'))
        .typeText(Selector('ul form label').withText('Publication Title'), 'The Big Book of Bad Jokes', {replace: true})
        .typeText(Selector('ul form label').withText('Column / Chapter Title'), 'Nothing as bad as a bad laugh', {replace: true})
        .typeText(Selector('ul form label').withText('Publication Date'), '1860-06', {replace: true})
        .typeText(Selector('ul form label').withText('Publisher'), 'Groan Publishing', {replace: true})
        .typeText(Selector('ul form label').withText('Publication Location'), 'London, UK', {replace: true})
        .typeText(Selector('ul form label').withText('Page Numbers'), '75', {replace: true})
        .click(Selector('ul button[aria-label="Save changes"]'))
        .expect(Selector('h2').withText('THE BIG BOOK OF BAD JOKES').exists).ok();
    const allSources = await getAllRecords('sources');
    await t
        .expect(allSources.obj_rows.length).eql(2);
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

test('Cancel editing a source', async t => {
    const objs = await setupStandardDatabase();
    await sessionStoreValue('auth.id', objs.users.provider._id);
    await sessionStoreValue('auth.token', objs.users.provider.tokens[0].token);
    await t
        .navigateTo('http://localhost:6543/')
        .click(Selector('a').withText('Contribute'))
        .click(Selector('a').withText('Contribute Source Data'));
    await t
        .click(Selector('h2').withText('THE DAILY JOKE').parent('li').find('button[aria-label="Edit this source"]'))
        .click(Selector('ul form label').withText('Publication Type'))
        .click(Selector('ul form option').withText('Book'))
        .typeText(Selector('ul form label').withText('Publication Title'), 'The Big Book of Bad Jokes', {replace: true})
        .typeText(Selector('ul form label').withText('Column / Chapter Title'), 'Nothing as bad as a bad laugh', {replace: true})
        .typeText(Selector('ul form label').withText('Publication Date'), '1860-06', {replace: true})
        .typeText(Selector('ul form label').withText('Publisher'), 'Groan Publishing', {replace: true})
        .typeText(Selector('ul form label').withText('Publication Location'), 'London, UK', {replace: true})
        .typeText(Selector('ul form label').withText('Page Numbers'), '75', {replace: true})
        .click(Selector('ul button[aria-label="Discard changes"]'))
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
        .expect(dbSource.type).eql('newspaper')
        .expect(dbSource.subtitle).eql('')
        .expect(dbSource.date).eql('1872-04-13')
        .expect(dbSource.publisher).eql('')
        .expect(dbSource.location).eql('')
        .expect(dbSource.page_numbers).eql('');
});

test('Update a source image', async t => {
    const objs = await setupStandardDatabase();
    await sessionStoreValue('auth.id', objs.users.provider._id);
    await sessionStoreValue('auth.token', objs.users.provider.tokens[0].token);
    await t
        .navigateTo('http://localhost:6543/')
        .click(Selector('a').withText('Contribute'))
        .click(Selector('a').withText('Contribute Source Data'));
    await t
        .click(Selector('h2').withText('THE DAILY JOKE').parent('li').find('button[aria-label="Edit this source"]'))
        .setFilesToUpload(Selector('ul form label').withText('New Source Image').find('input'), ['../../../toja/server/handlers/test/example-source1.png'])
        .click(Selector('ul form label').withText('Please confirm'))
        .click(Selector('ul button[aria-label="Save changes"]'))
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
            .expect(dbSource.updated).ok();
    });

test('Fail updating a source image without license consent', async t => {
    const objs = await setupStandardDatabase();
    await sessionStoreValue('auth.id', objs.users.provider._id);
    await sessionStoreValue('auth.token', objs.users.provider.tokens[0].token);
    await t
        .navigateTo('http://localhost:6543/')
        .click(Selector('a').withText('Contribute'))
        .click(Selector('a').withText('Contribute Source Data'));
    await t
        .click(Selector('h2').withText('THE DAILY JOKE').parent('li').find('button[aria-label="Edit this source"]'))
        .setFilesToUpload(Selector('ul form label').withText('New Source Image').find('input'), ['../../../toja/server/handlers/test/example-source1.png'])
        .click(Selector('ul button[aria-label="Save changes"]'))
        .expect(Selector('span').withText('Please confirm that you are permitted to upload the file under the given license').exists).ok();
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
            .expect(dbSource.updated).notOk();
});

test('Fail edit with invalid data', async t => {
    const objs = await setupStandardDatabase();
    await sessionStoreValue('auth.id', objs.users.provider._id);
    await sessionStoreValue('auth.token', objs.users.provider.tokens[0].token);
    await t
        .navigateTo('http://localhost:6543/')
        .click(Selector('a').withText('Contribute'))
        .click(Selector('a').withText('Contribute Source Data'));
    await t
        .click(Selector('h2').withText('THE DAILY JOKE').parent('li').find('button[aria-label="Edit this source"]'))
        .click(Selector('ul form label').withText('Publication Type'))
        .click(Selector('ul form option').withText('Book'))
        .click(Selector('ul form label').withText('Publication Title'))
        .pressKey('ctrl+a delete')
        .click(Selector('ul form label').withText('Publication Date'))
        .pressKey('ctrl+a delete')
        .click(Selector('ul button[aria-label="Save changes"]'))
        .expect(Selector('span').withText('Empty values not allowed').exists).ok()
        .expect(Selector('span').withText('Empty values not allowed').count).eql(2);
});
