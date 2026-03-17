import { describe, it, expect } from 'vitest'
import { router } from '@/app/routes'

describe('router configuration', () => {
  it('defines routes array', () => {
    expect(router).toBeDefined()
    expect(router.routes).toBeDefined()
    expect(router.routes.length).toBeGreaterThan(0)
  })

  it('has a root layout route at /', () => {
    const root = router.routes.find((r) => r.path === '/')
    expect(root).toBeDefined()
  })

  it('has child routes for home, ingles, and dynamic slug', () => {
    const root = router.routes.find((r) => r.path === '/')
    expect(root).toBeDefined()
    const children = root!.children ?? []

    const hasIndex = children.some((c) => c.index === true)
    const hasIngles = children.some((c) => c.path === 'ingles')
    const hasSlug = children.some((c) => c.path === ':slug')

    expect(hasIndex).toBe(true)
    expect(hasIngles).toBe(true)
    expect(hasSlug).toBe(true)
  })
})
