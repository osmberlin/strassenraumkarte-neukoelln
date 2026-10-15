import { z } from 'astro/zod'
import { defineCollection } from 'astro:content'
import { loader } from './utils/loader'

export const contentBase = 'src/content/releases'

// One JSON file per rendered data state ("release") of a map.
// The file name is the release id, which is also the `?map=<id>` URL param.
export const astroReleasesDefinition = defineCollection({
  loader: loader(contentBase, 'json'),
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
    /** @desc Old `?map=` values that should open this release, e.g. `micromap_preview` */
    aliases: z.array(z.string()).default([]),
    /** @desc The release `?map=<map>` points to; exactly one per map */
    default: z.boolean().default(false),
    /** @desc Only listed in the layer picker when selected via URL */
    hidden: z.boolean().default(false),
    attribution: z.string(),
  }),
})
