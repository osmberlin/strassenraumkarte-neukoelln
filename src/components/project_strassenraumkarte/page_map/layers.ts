export type MapGroup = 'micromap' | 'parkingmap' | 'debugmap' | 'background'

/** Serializable layer definition, passed from Astro to the React island */
export type MapLayerConfig = {
  /** @desc Also the `?map=<id>` URL param */
  id: string
  group: MapGroup
  title: string
  tiles: string
  minNativeZoom: number
  maxNativeZoom: number
  bounds?: [number, number, number, number] | undefined
  attribution: string
  /** @desc ISO date (YYYY-MM-DD) of the OSM data, only for our own renders */
  dataDate?: string | undefined
  note?: string | undefined
  /** @desc Old `?map=` values that should open this layer, e.g. `micromap_preview` */
  aliases?: string[] | undefined
  default: boolean
  hidden: boolean
}

const osmAttribution = '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'

export const backgroundLayers: MapLayerConfig[] = [
  {
    id: 'osm',
    group: 'background',
    title: 'OpenStreetMap',
    tiles: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
    minNativeZoom: 0,
    maxNativeZoom: 19,
    attribution: osmAttribution,
    default: false,
    hidden: false,
  },
  {
    id: 'luftbild2020',
    group: 'background',
    title: 'Luftbilder 2020',
    tiles: 'https://tiles.codefor.de/berlin-2020-truedop20rgb/{z}/{x}/{y}.png',
    minNativeZoom: 0,
    maxNativeZoom: 19,
    attribution:
      '<a href="https://fbinter.stadt-berlin.de/fb/index.jsp?loginkey=zoomStart&mapId=k_luftbild2020_true_rgb@senstadt&bbox=388712,5818615,394579,5822445">Geoportal Berlin / Digitale farbige TrueOrthophotos 2020 (TrueDOP20RGB) - Sommerbefliegung</a>',
    default: false,
    hidden: false,
  },
  {
    id: 'luftbild2024',
    group: 'background',
    title: 'Luftbilder 2024',
    tiles: 'https://tiles.codefor.de/berlin-2024-dop20rgbi/{z}/{x}/{y}.png',
    minNativeZoom: 0,
    maxNativeZoom: 19,
    attribution:
      '<a href="https://fbinter.stadt-berlin.de/fb/index.jsp?loginkey=zoomStart&mapId=k_luftbild2024_true_rgbi@senstadt&bbox=388712,5818615,394579,5822445">Geoportal Berlin / Digitale farbige TrueOrthophotos 2024 (DOP20RGBI)</a>',
    default: false,
    hidden: false,
  },
]

export const groupTitles: Record<MapGroup, string> = {
  micromap: 'Straßenraumkarte',
  parkingmap: 'Parkraumkarte',
  debugmap: 'Debug-Modus',
  background: 'Hintergrund',
}

/** `?map=micromap` (and an empty `?map`) shows the default release of the Straßenraumkarte */
export const DEFAULT_MAP_PARAM = 'micromap'

const isGroup = (value: string): value is MapGroup => value in groupTitles

/** All `?map=` values that open this layer */
export const mapParamsForLayer = (layer: MapLayerConfig) => [
  layer.id,
  ...(layer.aliases ?? []),
  ...(layer.default ? [layer.group] : []),
]

/**
 * Resolve a `?map=` value to a layer.
 * Accepts a release/layer id (`release01`, `osm`), an alias of a release (`micromap_preview`)
 * or a map name (`micromap`, `parkingmap`, `debugmap`) which points to the release flagged `default` for that map.
 */
export const resolveLayer = (layers: MapLayerConfig[], mapParam: string | null | undefined) => {
  const param = mapParam || DEFAULT_MAP_PARAM
  const byIdOrAlias = layers.find((layer) => layer.id === param || layer.aliases?.includes(param))
  if (byIdOrAlias) return byIdOrAlias
  const group = isGroup(param) ? param : DEFAULT_MAP_PARAM
  const byGroup = layers.find((layer) => layer.group === group && layer.default)
  return byGroup ?? layers.find((layer) => layer.group === DEFAULT_MAP_PARAM && layer.default)!
}

/** "Straßenraumkarte Release 02", "Parkraumkarte", "OpenStreetMap" */
export const layerTitle = (layer: MapLayerConfig) =>
  layer.group === 'micromap' ? `${groupTitles.micromap} ${layer.title}` : layer.title

export const formatDataDate = (isoDate: string) => {
  const [year, month, day] = isoDate.split('-')
  return `${day}.${month}.${year}`
}
