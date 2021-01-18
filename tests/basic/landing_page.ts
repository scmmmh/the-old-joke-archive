import { Selector } from 'testcafe';
import { request } from '../util';

fixture('Landing Page').beforeEach(async (test) => {
    await request('http://localhost:6543/tests/create');
    await test
        .navigateTo('http://localhost:6543/')
        .resizeWindow(1024, 768);
});

test('Has the app title', async (test) => {
    await test
        .expect(Selector('h1').innerText).eql('Find Something Funny')
        .expect(Selector('h2').innerText).eql('The Old Joke Archive');
});
