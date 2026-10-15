import { glob } from 'astro/loaders'

export const loader = (contentBase: string, format: 'mdx' | 'json' | 'yaml') => {
  const base = contentBase.startsWith('/') ? `.${contentBase}` : contentBase
  return glob({
    base: base,
    pattern: `**/[^_]*.${format}`,
  })
}
