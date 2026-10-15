import { glob } from 'astro/loaders'
import { z } from 'astro/zod'
import { defineCollection } from 'astro:content'
import { languages } from './layouts/languages'

const posts = defineCollection({
  loader: glob({ base: './src/content/posts', pattern: '**/[^_]*.mdx' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      menuTitle: z.string(),
      pubDate: z
        .string()
        .or(z.date())
        .transform((val) => new Date(val)),
      updatedDate: z
        .string()
        .or(z.date())
        .transform((val) => new Date(val))
        .optional(),
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

// One JSON file per rendered data state ("release") of a map.
// The file name is the release id, which is also the `?map=<id>` URL param.
const releases = defineCollection({
  loader: glob({ base: './src/content/releases', pattern: '*.json' }),
  schema: z.object({
    /** @desc Which map this release belongs to; `?map=micromap|parkingmap|debugmap` resolves to its default release */
    map: z.enum(['micromap', 'parkingmap', 'debugmap']),
    title: z.string(),
    /** @desc Date of the OSM data used for this render */
    dataDate: z.coerce.date(),
    /** @desc XYZ template, e.g. https://tiles.osm-berlin.org/release01/{z}/{x}/{y}.webp */
    tiles: z.string().includes('{z}/{x}/{y}'),
    minNativeZoom: z.number().int().default(0),
    maxNativeZoom: z.number().int().default(20),
    /** @desc [west, south, east, north] of the rendered area; no tiles are requested outside */
    bounds: z.tuple([z.number(), z.number(), z.number(), z.number()]).optional(),
    /** @desc Short hint shown in the layer picker, e.g. limited coverage */
    note: z.string().optional(),
    /** @desc The release `?map=<map>` points to; exactly one per map */
    default: z.boolean().default(false),
    /** @desc Only listed in the layer picker when selected via URL */
    hidden: z.boolean().default(false),
    attribution: z.string(),
  }),
})

export const collections = { posts, releases }
