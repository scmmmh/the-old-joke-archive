import { Selector } from 'testcafe';
import { setupEmptyDatabase } from '../database';

fixture('Landing Page').beforeEach(async (test) => {
    await test
        .navigateTo('http://localhost:6543/')
        .resizeWindow(1024, 768);
});

test('Has the app title', async (test) => {
    await setupEmptyDatabase();
    await test
        .expect(Selector('h1').innerText).eql('Welcome to The Old Joke Archive');
});
