import { test, expect } from '@playwright/test';

test('Has the correct application title ', async ({ page }) => {
  await page.goto('http://localhost:6543');
  await expect(page).toHaveTitle('The Old Joke Archive');
});

test('Has the correct page title', async ({ page }) => {
  await page.goto('http://localhost:6543');
  await expect(page.getByRole('heading', { name: 'Welcome to The Old Joke Archive' })).toBeVisible();
});
