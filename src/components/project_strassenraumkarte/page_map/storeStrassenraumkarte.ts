import { createSearchParams } from '@components/store/createSearchParams'

/**
 * `?map=<layer>` selects the layer: a release id (`release01`), a background (`osm`)
 * or a map alias (`micromap`, `parkingmap`, `debugmap`) which points to the latest release.
 * Old values (map names, aliases) are rewritten to the release id on load.
 * Unlike the other osm-verkehrswende.org maps, `?map` is not the camera position;
 * that lives in the `#zoom/lat/lng` hash to keep old links working.
 */
export type SearchParamsStrassenraumkarte = {
  map?: string
}

export const $searchParams = createSearchParams()
