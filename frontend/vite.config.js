import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000, // Optional: define a port for the dev server
    strictPort: true, // Optional: fail if port is already in use
  }
})
