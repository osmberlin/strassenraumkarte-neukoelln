import { getCollection } from 'astro:content'
import { backgroundLayers, groupTitles, type MapLayerConfig } from './layers'

const releasesPath = 'src/content/releases'

/** Fail the build on release files that would make `?map=` ambiguous */
const validateReleases = (releases: MapLayerConfig[]) => {
  for (const map of ['micromap', 'parkingmap', 'debugmap'] as const) {
    const [latest, previous] = releases.filter((release) => release.group === map)
    if (!latest) throw new Error(`${releasesPath}: "${map}" needs at least one release`)
    // The newest `dataDate` is the latest release, so it has to be unique
    if (previous?.dataDate === latest.dataDate) {
      throw new Error(
        `${releasesPath}: "${latest.id}" and "${previous.id}" share the newest dataDate ${latest.dataDate}, so the latest "${map}" release is ambiguous`,
      )
    }
  }

  // Every `?map=` value (release id, alias, background id, map name) must point to exactly one layer
  const owners = new Map<string, string>()
  for (const name of Object.keys(groupTitles)) owners.set(name, `map name "${name}"`)
  for (const layer of backgroundLayers) {
    for (const value of [layer.id, ...(layer.aliases ?? [])]) {
      owners.set(value, `background layer "${layer.id}"`)
    }
  }
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
    .map(({ id, data }, index, sorted): MapLayerConfig => ({
      id,
      group: data.map,
      // "Straßenraumkarte 2026/10"
      title: `${groupTitles[data.map]} ${data.dataDate.toISOString().slice(0, 7).replace('-', '/')}`,
      tiles: data.tiles,
      minNativeZoom: data.minNativeZoom,
      maxNativeZoom: data.maxNativeZoom,
      bounds: data.bounds,
      attribution: data.attribution,
      dataDate: data.dataDate.toISOString().slice(0, 10),
      note: data.note,
      aliases: data.aliases,
      // Sorted newest first, so the first release of each map is its latest
      latest: sorted.findIndex((release) => release.data.map === data.map) === index,
      hidden: data.hidden,
    }))
  validateReleases(releases)
  return releases
}

/** Releases from `src/content/releases/*.json`, newest first (the first per map is `latest`); loaded and validated once per build */
export const getReleaseLayers = () => {
  // Re-read in dev so edits to the JSON files show up without a restart
  if (import.meta.env.DEV) return loadReleaseLayers()
  releaseLayers ??= loadReleaseLayers()
  return releaseLayers
}
