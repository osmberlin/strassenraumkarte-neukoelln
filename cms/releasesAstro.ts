import { z } from 'astro/zod'
import { defineCollection } from 'astro:content'
import { loader } from './utils/loader'

export const contentBase = 'src/content/releases'

// One JSON file per rendered data state ("release") of a map.
// The file name is the release id, which is also the `?map=<id>` URL param.
export const astroReleasesDefinition = defineCollection({
  loader: loader(contentBase, 'json'),
  schema: z.object({
    /** @desc Which map this release belongs to; `?map=micromap|parkingmap|debugmap` resolves to its latest release (newest `dataDate`) */
    map: z.enum(['micromap', 'parkingmap', 'debugmap']),
    /** @desc Date of the OSM data used for this render */
    dataDate: z.coerce.date(),
    /** @desc XYZ template, e.g. https://tiles.osm-berlin.org/release01/{z}/{x}/{y}.webp */
    tiles: z.string().includes('{z}/{x}/{y}'),
    minNativeZoom: z.number().int().default(0),
    maxNativeZoom: z.number().int().default(20),
    /** @desc [west, south, east, north] of the rendered area. No tiles are requested outside and the map can not be moved outside while this release is shown. */
    bounds: z.tuple([z.number(), z.number(), z.number(), z.number()]),
    /** @desc Short hint shown below the selected release in the layer picker */
    note: z.string().optional(),
    /** @desc Old `?map=` values that should open this release, e.g. `micromap_preview` */
    aliases: z.array(z.string()).default([]),
    /** @desc Only listed in the layer picker when selected via URL */
    hidden: z.boolean().default(false),
    attribution: z.string(),
  }),
})
