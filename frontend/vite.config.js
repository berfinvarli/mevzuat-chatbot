import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api/v1': process.env.VITE_BACKEND_PROXY_URL || 'http://localhost:8001',
    },
  },
})
