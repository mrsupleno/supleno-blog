import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://supleno.com',
  base: '/blog',
  output: 'static',
  build: {
    format: 'directory'
  },
  redirects: {},
  markdown: {
    shikiConfig: {},
    remarkPlugins: [],
    rehypePlugins: []
  }
});
