// frontend/vite.config.ts
import path from "path"
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite' // Make sure this is imported

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(), // Add the plugin here
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})