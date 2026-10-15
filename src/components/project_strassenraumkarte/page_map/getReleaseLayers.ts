import { getCollection } from 'astro:content'
import { backgroundLayers, groupTitles, type MapLayerConfig } from './layers'

const releasesPath = 'src/content/releases'

/** Fail the build on release files that would make `?map=` ambiguous */
const validateReleases = (releases: MapLayerConfig[]) => {
  for (const map of ['micromap', 'parkingmap', 'debugmap'] as const) {
    const defaults = releases.filter((release) => release.group === map && release.default)
    if (defaults.length !== 1) {
      throw new Error(
        `${releasesPath}: "${map}" needs exactly one release with "default": true, found ${defaults.length}`,
      )
    }
  }

  // Every `?map=` value (release id, alias, background id, map name) must point to exactly one layer
  const owners = new Map<string, string>()
  for (const name of Object.keys(groupTitles)) owners.set(name, `map name "${name}"`)
  for (const layer of backgroundLayers) owners.set(layer.id, `background layer "${layer.id}"`)
  for (const release of releases) {
    for (const value of [release.id, ...(release.aliases ?? [])]) {
      const owner = owners.get(value)
      if (owner) {
        throw new Error(
          `${releasesPath}/${release.id}.json: "${value}" is already used by ${owner}`,
        )
      }
      owners.set(value, `release "${release.id}"`)
    }
  }
}

let releaseLayers: Promise<MapLayerConfig[]> | undefined

const loadReleaseLayers = async () => {
  const releases = (await getCollection('releases'))
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
  validateReleases(releases)
  return releases
}

/** Releases from `src/content/releases/*.json`, newest first; loaded and validated once per build */
export const getReleaseLayers = () => {
  // Re-read in dev so edits to the JSON files show up without a restart
  if (import.meta.env.DEV) return loadReleaseLayers()
  releaseLayers ??= loadReleaseLayers()
  return releaseLayers
}
