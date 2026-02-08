import { fileURLToPath, URL } from 'node:url'

import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

const backendPort = process.env.VITE_BACKEND_PORT || '8000'
const frontendDevPort = process.env.VITE_FRONTEND_PORT || process.env.FRONTEND_DEV_PORT || '5173'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: parseInt(frontendDevPort, 10),
    proxy: {
      '/api': {
        target: `http://localhost:${backendPort}`,
        changeOrigin: true,
      },
    },
  },
})
