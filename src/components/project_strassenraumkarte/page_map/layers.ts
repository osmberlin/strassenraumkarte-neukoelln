export type MapGroup = 'micromap' | 'parkingmap' | 'debugmap' | 'background'

/** [west, south, east, north] */
export type LayerBounds = [number, number, number, number]

/** Serializable layer definition, passed from Astro to the React island */
export type MapLayerConfig = {
  /** @desc Also the `?map=<id>` URL param */
  id: string
  group: MapGroup
  /** @desc Shown in the layer picker, e.g. "Straßenraumkarte 2026/10" */
  title: string
  tiles: string
  minNativeZoom: number
  maxNativeZoom: number
  /** @desc Rendered area. No tiles are requested outside and the map stays inside while this layer is shown. */
  bounds: LayerBounds
  attribution: string
  /** @desc ISO date (YYYY-MM-DD) of the OSM data, only for our own renders */
  dataDate?: string | undefined
  note?: string | undefined
  /** @desc Old `?map=` values that should open this layer, e.g. `micromap_preview` */
  aliases?: string[] | undefined
  /** @desc Newest release of its map; `?map=<map>` and old URLs open it */
  latest: boolean
  hidden: boolean
}

export const berlinBounds: LayerBounds = [13.07356, 52.33319, 13.76454, 52.68261]

const osmAttribution = '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'

/**
 * Aerial images straight from the Geoportal Berlin WMS. The tiles.codefor.de mirror (used by the old
 * page and the OSM Editor Layer Index) answers 502 for all years.
 */
const berlinAerial = (year: number): MapLayerConfig => ({
  id: `luftbild${year}`,
  group: 'background',
  title: `Luftbild ${year}`,
  tiles: `https://gdi.berlin.de/services/wms/truedop_${year}?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&LAYERS=truedop_${year}&STYLES=&CRS=EPSG:3857&BBOX={bbox-epsg-3857}&WIDTH=512&HEIGHT=512&FORMAT=image/png`,
  minNativeZoom: 0,
  maxNativeZoom: 20,
  bounds: berlinBounds,
  attribution: `<a href="https://gdi.berlin.de/geonetwork/srv/ger/catalog.search#/search?any=truedop_${year}">Geoportal Berlin / Digitale farbige TrueOrthophotos ${year}</a>`,
  latest: false,
  hidden: false,
})

export const backgroundLayers: MapLayerConfig[] = [
  {
    id: 'osm',
    group: 'background',
    title: 'OpenStreetMap',
    tiles: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
    minNativeZoom: 0,
    maxNativeZoom: 19,
    bounds: berlinBounds,
    attribution: osmAttribution,
    latest: false,
    hidden: false,
  },
  // The newest year Geoportal Berlin offers, plus 2024 (old `?map=luftbild2020` links open 2024)
  berlinAerial(2026),
  { ...berlinAerial(2024), aliases: ['luftbild2020'] },
]

export const groupTitles: Record<MapGroup, string> = {
  micromap: 'Straßenraumkarte',
  parkingmap: 'Parkraumkarte',
  debugmap: 'Debug-Modus',
  background: 'Hintergrund',
}

/** `?map=micromap` (and an empty `?map`) shows the latest release of the Straßenraumkarte */
export const DEFAULT_MAP_PARAM = 'micromap'

const isGroup = (value: string): value is MapGroup => Object.hasOwn(groupTitles, value)

/** All `?map=` values that open this layer */
export const mapParamsForLayer = (layer: MapLayerConfig) => [
  layer.id,
  ...(layer.aliases ?? []),
  ...(layer.latest ? [layer.group] : []),
]

/**
 * Resolve a `?map=` value to a layer.
 * Accepts a release/layer id (`release01`, `osm`), an alias of a release (`micromap_preview`)
 * or a map name (`micromap`, `parkingmap`, `debugmap`) which points to the latest release of that map.
 */
export const resolveLayer = (layers: MapLayerConfig[], mapParam: string | null | undefined) => {
  const param = mapParam || DEFAULT_MAP_PARAM
  const byIdOrAlias = layers.find((layer) => layer.id === param || layer.aliases?.includes(param))
  if (byIdOrAlias) return byIdOrAlias
  const group = isGroup(param) ? param : DEFAULT_MAP_PARAM
  const byGroup = layers.find((layer) => layer.group === group && layer.latest)
  return byGroup ?? layers.find((layer) => layer.group === DEFAULT_MAP_PARAM && layer.latest)!
}

export const formatDataDate = (isoDate: string) => {
  const [year, month, day] = isoDate.split('-')
  return `${day}.${month}.${year}`
}
