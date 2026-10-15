// The camera position lives in the URL hash `#<zoom>/<lat>/<lng>`, like on the old Leaflet page
// (leaflet-hash format, zoom in *Leaflet* zoom levels).
//
// MapLibre zoom levels are offset by one (512px vs. 256px world), so we convert at the boundary
// and keep writing Leaflet zoom to the hash so links stay interchangeable with old links.
export const LEAFLET_ZOOM_OFFSET = 1

export type HashLocation = { zoom: number; latitude: number; longitude: number }

export type MapLimits = {
  /** [[west, south], [east, north]] */
  maxBounds: [[number, number], [number, number]]
  /** In Leaflet zoom levels */
  minZoom: number
  /** In Leaflet zoom levels */
  maxZoom: number
}

export const parseHash = (hash: string): HashLocation | undefined => {
  const parts = hash.replace(/^#/, '').split('/')
  if (parts.length !== 3) return undefined
  const [zoom, latitude, longitude] = // `parseFloat` like leaflet-hash, which ignored trailing text
    parts.map((part) => parseFloat(part))
  if (zoom === undefined || latitude === undefined || longitude === undefined) return undefined
  if ([zoom, latitude, longitude].some((value) => !Number.isFinite(value))) return undefined
  return { zoom, latitude, longitude }
}

const clamp = (value: number, min: number, max: number) => Math.min(Math.max(value, min), max)

/** Keep a (hash) location inside the map limits, so URL and edit links match what the map shows */
export const clampLocation = (
  location: HashLocation,
  { maxBounds, minZoom, maxZoom }: MapLimits,
) => {
  const [[west, south], [east, north]] = maxBounds
  return {
    zoom: clamp(location.zoom, minZoom, maxZoom),
    latitude: clamp(location.latitude, south, north),
    longitude: clamp(location.longitude, west, east),
  }
}

export const formatHash = ({ zoom, latitude, longitude }: HashLocation) => {
  const roundedZoom = Math.round(zoom * 10) / 10
  // Same lat/lng precision as leaflet-hash
  const precision = Math.max(0, Math.ceil(Math.log(roundedZoom) / Math.LN2))
  return `#${roundedZoom}/${latitude.toFixed(precision)}/${longitude.toFixed(precision)}`
}

export const replaceHash = (location: HashLocation) => {
  history.replaceState(
    history.state,
    '',
    `${window.location.pathname}${window.location.search}${formatHash(location)}`,
  )
}
