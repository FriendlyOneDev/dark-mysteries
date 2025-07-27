import { defineConfig } from "vite";
import vue from '@vitejs/plugin-vue';
import svgLoader from 'vite-svg-loader';

export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
      },
      '/ws': {
        target: 'http://localhost:3000',
        ws: true
      }
    }
  },
  build: {
    outDir: '../server/static'
  },
  plugins: [vue(), svgLoader()]
});