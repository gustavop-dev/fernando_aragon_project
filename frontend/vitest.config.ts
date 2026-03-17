/// <reference types="vitest" />
import { defineConfig } from 'vitest/config'
import path from 'path'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/__tests__/setup.ts'],
    include: ['src/**/*.{test,spec}.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'text-summary', 'json-summary'],
      include: ['src/app/**/*.{ts,tsx}'],
      exclude: [
        'src/app/components/ui/**',
        'src/**/*.{test,spec}.{ts,tsx}',
        'src/__tests__/**',
      ],
    },
  },
})
