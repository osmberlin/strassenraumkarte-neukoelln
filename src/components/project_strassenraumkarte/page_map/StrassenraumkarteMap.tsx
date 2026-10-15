import { useStore } from '@nanostores/react'
import 'maplibre-gl/dist/maplibre-gl.css'
import { Fragment, useEffect, useState } from 'react'
import {
  AttributionControl,
  Layer,
  Map,
  NavigationControl,
  Source,
  useMap,
  type MapEvent,
  type StyleSpecification,
  type ViewStateChangeEvent,
} from 'react-map-gl/maplibre'
import {
  clampLocation,
  LEAFLET_ZOOM_OFFSET,
  parseHash,
  replaceHash,
  type HashLocation,
  type MapLimits,
} from './hash'
import { DEFAULT_MAP_PARAM, resolveLayer, type MapLayerConfig } from './layers'
import { Overlay } from './Overlay'
import { $searchParams, type SearchParamsStrassenraumkarte } from './storeStrassenraumkarte'

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

type HashChangeListenerProps = { mapLoaded: boolean; limits: MapLimits }

/** Follow manual edits of the `#zoom/lat/lng` hash, like leaflet-hash did */
const HashChangeListener = ({ mapLoaded, limits }: HashChangeListenerProps) => {
  const { current: map } = useMap()

  useEffect(
    function subscribeToHashChanges() {
      if (!map || !mapLoaded) return
      const handleHashChange = () => {
        const location = parseHash(window.location.hash)
        if (!location) return
        const { zoom, latitude, longitude } = clampLocation(location, limits)
        map.jumpTo({ center: [longitude, latitude], zoom: zoom - LEAFLET_ZOOM_OFFSET })
      }
      window.addEventListener('hashchange', handleHashChange)
      return function unsubscribeFromHashChanges() {
        window.removeEventListener('hashchange', handleHashChange)
      }
    },
    [map, mapLoaded, limits],
  )

  return null
}

type Props = { layers: MapLayerConfig[] } & MapLimits

export const StrassenraumkarteMap = ({ layers, maxBounds, minZoom, maxZoom }: Props) => {
  const limits = { maxBounds, minZoom, maxZoom }
  const params = useStore($searchParams) as SearchParamsStrassenraumkarte
  const selectedLayer = resolveLayer(layers, params.map)
  const [mapLoaded, setMapLoaded] = useState(false)
  const [location, setLocation] = useState(() =>
    clampLocation(parseHash(window.location.hash) ?? fallbackLocation, limits),
  )

  // Make the current state shareable right away, like the old page did.
  // Not in `onLoad` which only fires after the first render frame (never in background tabs).
  useEffect(function writeInitialUrlState() {
    replaceHash(location)
    const currentParams = $searchParams.get()
    $searchParams.open({ ...currentParams, map: currentParams.map || DEFAULT_MAP_PARAM }, true)
  }, [])

  const handleLoad = (event: MapEvent) => {
    // The hash has no bearing, so rotation would be lost on reload (and there is no compass to reset it)
    event.target.touchZoomRotate.disableRotation()
    event.target.keyboard.disableRotation()
    setMapLoaded(true)
  }

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
      RTLTextPlugin={false}
      locale={{
        'NavigationControl.ZoomIn': 'Hineinzoomen',
        'NavigationControl.ZoomOut': 'Herauszoomen',
      }}
      onLoad={handleLoad}
      onMoveEnd={handleMoveEnd}
    >
      {/* All layers stay mounted so switching (e.g. comparing releases) keeps their tiles warm.
          MapLibre only requests tiles (and shows attribution) for visible layers. */}
      {layers.map((layer) => (
        <Fragment key={layer.id}>
          <Source
            id={layer.id}
            type="raster"
            tiles={[layer.tiles]}
            tileSize={256}
            minzoom={layer.minNativeZoom}
            maxzoom={layer.maxNativeZoom}
            attribution={layer.attribution}
            {...(layer.bounds ? { bounds: layer.bounds } : {})}
          />
          <Layer
            id={`${layer.id}-layer`}
            type="raster"
            source={layer.id}
            layout={{ visibility: layer.id === selectedLayer.id ? 'visible' : 'none' }}
          />
        </Fragment>
      ))}

      <NavigationControl showCompass={false} position="top-right" />
      <AttributionControl compact={false} position="bottom-right" />
      <HashChangeListener mapLoaded={mapLoaded} limits={limits} />

      <Overlay
        layers={layers}
        selectedLayer={selectedLayer}
        onSelectLayer={handleSelectLayer}
        location={location}
      />
    </Map>
  )
}
