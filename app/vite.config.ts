import { fileURLToPath, URL } from 'node:url'

import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { defineConfig } from 'vite'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    Components({
      dirs: ['src/components/ui'],
      dts: 'src/components.d.ts'
    }),
    AutoImport({
      imports: [
        'vue',
        'vue-router',
        'pinia'
      ],
      dirs: ['src/lib/toast'],
      dts: 'src/auto-imports.d.ts',
      viteOptimizeDeps: true
    }),
    vueDevTools(),
    vue()
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://api.viot.local',
        changeOrigin: true,
        secure: true,
        rewrite: path => path.replace(/^\/api/, '/v1'),
        cookieDomainRewrite: {
          '*': 'localhost'
        }
      }
    }
  }
})
