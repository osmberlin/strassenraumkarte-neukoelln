import { getCollection } from 'astro:content'
import type { MapLayerConfig } from './layers'

/** Releases from `src/content/releases/*.json`, newest first */
export const getReleaseLayers = async () => {
  const releases = await getCollection('releases')

  // Fail the build when a map has no (or more than one) default release
  for (const map of ['micromap', 'parkingmap', 'debugmap'] as const) {
    const defaults = releases.filter((release) => release.data.map === map && release.data.default)
    if (defaults.length !== 1) {
      throw new Error(
        `src/content/releases: "${map}" needs exactly one release with "default": true, found ${defaults.length}`,
      )
    }
  }

  return releases
    .sort((a, b) => b.data.dataDate.valueOf() - a.data.dataDate.valueOf())
    .map(({ id, data }): MapLayerConfig => ({
      id,
      group: data.map,
      title: data.title,
      tiles: data.tiles,
      minNativeZoom: data.minNativeZoom,
      maxNativeZoom: data.maxNativeZoom,
      bounds: data.bounds,
      attribution: data.attribution,
      dataDate: data.dataDate.toISOString().slice(0, 10),
      note: data.note,
      aliases: data.aliases,
      default: data.default,
      hidden: data.hidden,
    }))
}
