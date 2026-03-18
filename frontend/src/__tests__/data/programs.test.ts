import { describe, it, expect } from 'vitest'
import { programs, type ProgramData } from '@/app/data/programs'

describe('programs data', () => {
  it('exports a non-empty array', () => {
    expect(Array.isArray(programs)).toBe(true)
    expect(programs.length).toBeGreaterThan(0)
  })

  it('every program has a unique slug', () => {
    const slugs = programs.map((p) => p.slug)
    const uniqueSlugs = new Set(slugs)
    expect(uniqueSlugs.size).toBe(slugs.length)
  })

  it('every program has required string fields', () => {
    const requiredFields: (keyof ProgramData)[] = [
      'slug',
      'name',
      'shortName',
      'description',
      'duration',
      'modules',
      'modality',
      'schedule',
      'certification',
      'objective',
      'profile',
    ]

    for (const program of programs) {
      for (const field of requiredFields) {
        expect(
          typeof program[field] === 'string' && (program[field] as string).length > 0,
          `${program.slug} missing ${field}`,
        ).toBe(true)
      }
    }
  })

  it('every program has an icon component', () => {
    for (const program of programs) {
      expect(program.icon).toBeDefined()
      expect(
        typeof program.icon === 'function' || typeof program.icon === 'object',
        `${program.slug} icon is not a valid component`,
      ).toBe(true)
    }
  })

  it('every program has a heroImage URL', () => {
    for (const program of programs) {
      expect(program.heroImage).toMatch(/^https?:\/\//)
    }
  })

  it('every program has functions and whyStudy arrays', () => {
    for (const program of programs) {
      expect(Array.isArray(program.functions)).toBe(true)
      expect(Array.isArray(program.whyStudy)).toBe(true)
      expect(program.whyStudy.length).toBeGreaterThan(0)
    }
  })

  it('at least one program is featured', () => {
    const featured = programs.filter((p) => p.featured)
    expect(featured.length).toBeGreaterThanOrEqual(1)
  })

  it('ingles program exists with expected slug', () => {
    const ingles = programs.find((p) => p.slug === 'ingles')
    expect(ingles).toBeDefined()
    expect(ingles!.name).toContain('Inglés')
  })
})
