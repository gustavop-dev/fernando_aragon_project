import { test, expect } from '@playwright/test'

/**
 * @flow:home-page-load
 */
test.describe('Home Page Load', () => {
  test('renders the home page with navigation and footer', async ({ page }) => {
    await page.goto('/')

    await expect(page.getByRole('navigation')).toBeVisible()
    await expect(page.getByRole('contentinfo')).toBeVisible()
  })

  test('displays program cards on the home page', async ({ page }) => {
    await page.goto('/')

    // The home page shows program links — at least one should be visible
    const programLinks = page.getByRole('link').filter({ hasText: /programa|inglés/i })
    await expect(programLinks.first()).toBeVisible({ timeout: 10_000 })
  })

  test('displays statistics section', async ({ page }) => {
    await page.goto('/')

    // Stats section shows numbers like "15+", "2500+", etc.
    await expect(page.getByText('Programas Ofertados')).toBeVisible({ timeout: 10_000 })
  })
})
