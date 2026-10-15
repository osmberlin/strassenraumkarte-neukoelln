import mdx from '@astrojs/mdx'
import react from '@astrojs/react'
import sitemap from '@astrojs/sitemap'
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'astro/config'
import { homedir } from 'node:os'
import { join } from 'node:path'

// CONFIG: https://astro.build/config (aligned with www.osm-verkehrswende.org and parkraum.osm-verkehrswende.org)
export default defineConfig({
  site: 'https://strassenraumkarte.osm-berlin.org/',
  integrations: [
    react({
      babel: {
        plugins: [['babel-plugin-react-compiler', { target: '19' }]],
      },
    }),
    // Astro 6.4 leaves `markdown.gfm` undefined, which @astrojs/mdx reads as "off" (no footnotes, autolinks)
    mdx({ gfm: true }),
    // Like the old Jekyll pages, the map, about, contact and posts index are `noindex`
    sitemap({
      filter: (page) => {
        const path = new URL(page).pathname.replace(/^\/|\/$/g, '')
        return !['', 'about', 'contact', 'posts'].includes(path)
      },
    }),
  ],
  // `preserve` keeps the Jekyll URLs: /posts/foo.html (served for /posts/foo) and /posts/index.html
  build: { format: 'preserve' },
  vite: {
    plugins: [tailwindcss()],
    server: {
      fs: {
        // Bun's global store links packages into ~/.bun/install/cache/links (keep the project root allowed)
        allow: [process.cwd(), join(homedir(), '.bun/install/cache/links')],
      },
    },
  },
  // Old URLs (jekyll-redirect-from). Redirects for `*.html` URLs live as static files in `public/`.
  redirects: {
    '/posts/2022-01-17-parkraumkarte-verschoben': '/posts/2022-07-01-parkraumkarte-verschoben',
    '/posts/2021-03-10-parkraumanalyse':
      'https://parkraum.osm-verkehrswende.org/posts/2021-03-12-parkraumanalyse',
    '/posts/2021-03-13-opendata': 'https://parkraum.osm-verkehrswende.org/posts/2021-03-13-opendata',
    '/posts/2021-03-17-parkplatzanalyse-vorgehen':
      'https://parkraum.osm-verkehrswende.org/posts/2021-03-17-parkplatzanalyse-vorgehen',
    '/posts/2021-06-08-vortrag-fossgis':
      'https://parkraum.osm-verkehrswende.org/posts/2021-06-08-vortrag-fossgis',
    '/posts/2021-12-13-evaluate-tradeoffs-in-data-quality-vs-mapping-details':
      'https://parkraum.osm-verkehrswende.org/posts/2021-12-13-evaluate-tradeoffs-in-data-quality-vs-mapping-details',
  },
})
