import { languages } from '@layouts/languages'
import { z } from 'astro/zod'
import { defineCollection } from 'astro:content'
import { loader } from './utils/loader'

export const contentBase = 'src/content/posts'

export const astroPostsDefinition = defineCollection({
  loader: loader(contentBase, 'mdx'),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      menuTitle: z.string(),
      // `coerce` rejects invalid dates at load time (with the file name) instead of failing later in a layout
      pubDate: z.coerce.date(),
      updatedDate: z.coerce.date().optional(),
      author: z.string(),
      description: z.string().optional(),
      inMenu: z.boolean(),
      noindex: z.boolean().optional(),
      language: z.enum(languages).optional(),
      image: image().nullish(),
      imageAlt: z.string().optional(),
      showToc: z.boolean().optional(),
      canonicalUrl: z.url().optional(),
    }),
})
