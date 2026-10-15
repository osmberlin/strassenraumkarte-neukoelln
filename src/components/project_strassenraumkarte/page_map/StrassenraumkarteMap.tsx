import { useStore } from '@nanostores/react'
import 'maplibre-gl/dist/maplibre-gl.css'
import { useEffect, useState } from 'react'
import {
  AttributionControl,
  Layer,
  Map,
  MapProvider,
  NavigationControl,
  Source,
  useMap,
  type LngLatBoundsLike,
  type StyleSpecification,
  type ViewStateChangeEvent,
} from 'react-map-gl/maplibre'
import { LEAFLET_ZOOM_OFFSET, parseHash, replaceHash, type HashLocation } from './hash'
import { DEFAULT_MAP_PARAM, resolveLayer, type MapLayerConfig } from './layers'
import { Overlay } from './Overlay'
import { $searchParams, type SearchParamsStrassenraumkarte } from './storeStrassenraumkarte'

const MAP_ID = 'strassenraumkarte'

// Zoom values in Leaflet zoom levels, like in the URL hash
const fallbackLocation: HashLocation = { zoom: 18, latitude: 52.47379, longitude: 13.44164 }

// Only raster tiles, so the style itself is just a background
const mapStyle: StyleSpecification = {
  version: 8,
  sources: {},
  layers: [{ id: 'background', type: 'background', paint: { 'background-color': '#f3f4f6' } }],
}

const toLocation = ({ zoom, latitude, longitude }: ViewStateChangeEvent['viewState']) => ({
  zoom: zoom + LEAFLET_ZOOM_OFFSET,
  latitude,
  longitude,
})

/** Follow manual edits of the `#zoom/lat/lng` hash, like leaflet-hash did */
const HashChangeListener = () => {
  const { [MAP_ID]: map } = useMap()

  useEffect(() => {
    if (!map) return
    const handleHashChange = () => {
      const location = parseHash(window.location.hash)
      if (!location) return
      map.jumpTo({
        center: [location.longitude, location.latitude],
        zoom: location.zoom - LEAFLET_ZOOM_OFFSET,
      })
    }
    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [map])

  return null
}

type Props = {
  layers: MapLayerConfig[]
  maxBounds: LngLatBoundsLike
  /** In Leaflet zoom levels */
  minZoom: number
  /** In Leaflet zoom levels */
  maxZoom: number
}

const MapView = ({ layers, maxBounds, minZoom, maxZoom }: Props) => {
  const params = useStore($searchParams) as SearchParamsStrassenraumkarte
  const selectedLayer = resolveLayer(layers, params.map)
  const [location, setLocation] = useState(
    () => parseHash(window.location.hash) ?? fallbackLocation,
  )

  // Make the current state shareable right away, like the old page did.
  // Not in `onLoad` which only fires after the first render frame (never in background tabs).
  useEffect(() => {
    replaceHash(location)
    $searchParams.open({ ...params, map: params.map || DEFAULT_MAP_PARAM }, true)
    // oxlint-disable-next-line react-hooks/exhaustive-deps -- only once on mount
  }, [])

  const handleMoveEnd = (event: ViewStateChangeEvent) => {
    const newLocation = toLocation(event.viewState)
    setLocation(newLocation)
    replaceHash(newLocation)
  }

  const handleSelectLayer = (layerId: string) => {
    $searchParams.open({ ...params, map: layerId })
  }

  return (
    <Map
      id={MAP_ID}
      initialViewState={{
        longitude: location.longitude,
        latitude: location.latitude,
        zoom: location.zoom - LEAFLET_ZOOM_OFFSET,
      }}
      minZoom={minZoom - LEAFLET_ZOOM_OFFSET}
      maxZoom={maxZoom - LEAFLET_ZOOM_OFFSET}
      maxBounds={maxBounds}
      mapStyle={mapStyle}
      style={{ width: '100%', height: '100%' }}
      dragRotate={false}
      pitchWithRotate={false}
      touchPitch={false}
      attributionControl={false}
      onMoveEnd={handleMoveEnd}
    >
      {/* `key` remounts source and layer when switching, so tiles of the old layer never mix in */}
      <Source
        key={selectedLayer.id}
        id={selectedLayer.id}
        type="raster"
        tiles={[selectedLayer.tiles]}
        tileSize={256}
        minzoom={selectedLayer.minNativeZoom}
        maxzoom={selectedLayer.maxNativeZoom}
        attribution={selectedLayer.attribution}
        {...(selectedLayer.bounds ? { bounds: selectedLayer.bounds } : {})}
      />
      <Layer
        key={`${selectedLayer.id}-layer`}
        id={`${selectedLayer.id}-layer`}
        type="raster"
        source={selectedLayer.id}
      />

      <NavigationControl showCompass={false} position="top-right" />
      <AttributionControl compact={false} position="bottom-right" />
      <HashChangeListener />

      <Overlay
        layers={layers}
        selectedLayer={selectedLayer}
        onSelectLayer={handleSelectLayer}
        location={location}
      />
    </Map>
  )
}

export const StrassenraumkarteMap = (props: Props) => {
  return (
    <MapProvider>
      <MapView {...props} />
    </MapProvider>
  )
}
