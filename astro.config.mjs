// @ts-check
import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://wittebol.be',
  prefetch: true,
  markdown: {
    shikiConfig: {
      theme: 'rose-pine-dawn',
    },
  },
  integrations: [svelte(), sitemap()],
  vite: {
    plugins: [tailwindcss()],
    cacheDir: '/tmp/vite-wittebol',
  },
});
