import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5000,
    strictPort: true,
    cors: true,
  },
  preview: {
    host: '0.0.0.0',
    port: 5000,
    strictPort: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          api: ['axios'],
        },
      },
    },
  },
  resolve: {
    alias: {
      '@': '/src',
      '@assets': '/src/assets',
    },
  },
  define: {
    // Ensure environment variables are available at build time
    'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development'),
  },
})
