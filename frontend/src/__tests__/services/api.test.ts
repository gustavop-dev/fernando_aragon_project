import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { submitContactForm, type ContactFormData } from '@/app/services/api'

const VALID_PAYLOAD: ContactFormData = {
  name: 'Juan Pérez',
  email: 'juan@example.com',
  phone: '+57 300 1234567',
  program: 'Inglés',
}

describe('submitContactForm', () => {
  const originalFetch = globalThis.fetch

  beforeEach(() => {
    globalThis.fetch = vi.fn()
  })

  afterEach(() => {
    globalThis.fetch = originalFetch
  })

  it('sends POST request to /contact/submit/ with JSON body', async () => {
    const mockResponse = { success: true, detail: 'OK' }
    ;(globalThis.fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      json: () => Promise.resolve(mockResponse),
    })

    await submitContactForm(VALID_PAYLOAD)

    expect(globalThis.fetch).toHaveBeenCalledOnce()
    const [url, options] = (globalThis.fetch as ReturnType<typeof vi.fn>).mock.calls[0]
    expect(url).toContain('/contact/submit/')
    expect(options.method).toBe('POST')
    expect(options.headers['Content-Type']).toBe('application/json')
  })

  it('sends serialised payload as request body', async () => {
    ;(globalThis.fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      json: () => Promise.resolve({ success: true }),
    })

    await submitContactForm(VALID_PAYLOAD)

    const body = JSON.parse(
      (globalThis.fetch as ReturnType<typeof vi.fn>).mock.calls[0][1].body,
    )
    expect(body.name).toBe(VALID_PAYLOAD.name)
    expect(body.email).toBe(VALID_PAYLOAD.email)
    expect(body.phone).toBe(VALID_PAYLOAD.phone)
    expect(body.program).toBe(VALID_PAYLOAD.program)
  })

  it('returns parsed JSON response on success', async () => {
    const mockResponse = { success: true, detail: 'Mensaje enviado correctamente.' }
    ;(globalThis.fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      json: () => Promise.resolve(mockResponse),
    })

    const result = await submitContactForm(VALID_PAYLOAD)

    expect(result).toEqual(mockResponse)
  })

  it('returns error response when server returns validation errors', async () => {
    const errorResponse = {
      success: false,
      errors: { email: ['Enter a valid email address.'] },
    }
    ;(globalThis.fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      json: () => Promise.resolve(errorResponse),
    })

    const result = await submitContactForm({ ...VALID_PAYLOAD, email: 'bad' })

    expect(result.success).toBe(false)
    expect(result.errors).toBeDefined()
  })

  it('includes captcha_token when provided', async () => {
    ;(globalThis.fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      json: () => Promise.resolve({ success: true }),
    })

    await submitContactForm({ ...VALID_PAYLOAD, captcha_token: 'abc123' })

    const body = JSON.parse(
      (globalThis.fetch as ReturnType<typeof vi.fn>).mock.calls[0][1].body,
    )
    expect(body.captcha_token).toBe('abc123')
  })

  it('propagates network error from fetch', async () => {
    ;(globalThis.fetch as ReturnType<typeof vi.fn>).mockRejectedValue(
      new Error('Network error'),
    )

    await expect(submitContactForm(VALID_PAYLOAD)).rejects.toThrow('Network error')
  })
})
