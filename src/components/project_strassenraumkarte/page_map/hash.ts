// The camera position lives in the URL hash `#<zoom>/<lat>/<lng>`, like on the old Leaflet page
// (leaflet-hash format, zoom in *Leaflet* zoom levels).
//
// MapLibre zoom levels are offset by one (512px vs. 256px world), so we convert at the boundary
// and keep writing Leaflet zoom to the hash so links stay interchangeable with old links.
export const LEAFLET_ZOOM_OFFSET = 1

export type HashLocation = { zoom: number; latitude: number; longitude: number }

export const parseHash = (hash: string): HashLocation | undefined => {
  const parts = hash.replace(/^#/, '').split('/')
  if (parts.length !== 3) return undefined
  const [zoom, latitude, longitude] = parts.map(Number)
  if (zoom === undefined || latitude === undefined || longitude === undefined) return undefined
  if ([zoom, latitude, longitude].some((value) => Number.isNaN(value))) return undefined
  return { zoom, latitude, longitude }
}

export const formatHash = ({ zoom, latitude, longitude }: HashLocation) => {
  const roundedZoom = Math.round(zoom * 100) / 100
  // Same precision as leaflet-hash
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
