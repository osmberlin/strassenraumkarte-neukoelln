import { unified } from '@astrojs/markdown-remark'
import mdx from '@astrojs/mdx'
import react from '@astrojs/react'
import sitemap from '@astrojs/sitemap'
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'astro/config'
import { homedir } from 'node:os'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'

const appRoot = fileURLToPath(new URL('.', import.meta.url))

// CONFIG: https://astro.build/config (aligned with www.osm-verkehrswende.org and parkraum.osm-verkehrswende.org)
export default defineConfig({
  site: 'https://strassenraumkarte.osm-berlin.org/',
  integrations: [
    react({ compiler: true }),
    mdx(),
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
  // Stay on the remark/rehype pipeline: Astro 7's default Sätteri MDX parser fails on our multi-line JSX tags (`<Image\n  src=…`)
  markdown: { processor: unified() },
  vite: {
    plugins: [tailwindcss()],
    server: {
      // Bun globalStore (bunfig.toml) symlinks realpath outside the project (~/.bun/install/cache/links/).
      // Extend (not replace) Vite's default fs.allow — setting allow alone drops the project root.
      // @see https://bun.com/docs/pm/global-store
      // @see https://vite.dev/config/server-options.html#server-fs-allow
      fs: {
        allow: [appRoot, join(homedir(), '.bun/install/cache/links')],
      },
    },
  },
  // Old URLs (jekyll-redirect-from). Redirects for `*.html` URLs live as static files in `public/`.
  redirects: {
    '/posts/2022-01-17-parkraumkarte-verschoben': '/posts/2022-07-01-parkraumkarte-verschoben',
    '/posts/2021-03-10-parkraumanalyse':
      'https://parkraum.osm-verkehrswende.org/posts/2021-03-10-parkraumanalyse',
    '/posts/2021-03-13-opendata': 'https://parkraum.osm-verkehrswende.org/posts/2021-03-13-opendata',
    '/posts/2021-03-17-parkplatzanalyse-vorgehen':
      'https://parkraum.osm-verkehrswende.org/posts/2021-03-17-parkplatzanalyse-vorgehen',
    '/posts/2021-06-08-vortrag-fossgis':
      'https://parkraum.osm-verkehrswende.org/posts/2021-06-08-vortrag-fossgis',
    '/posts/2021-12-13-evaluate-tradeoffs-in-data-quality-vs-mapping-details':
      'https://parkraum.osm-verkehrswende.org/posts/2021-12-13-evaluate-tradeoffs-in-data-quality-vs-mapping-details',
  },
})
