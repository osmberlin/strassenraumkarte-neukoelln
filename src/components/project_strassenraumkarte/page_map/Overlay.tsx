import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/react'
import { ChevronRightIcon } from '@heroicons/react/24/outline'
import { useState } from 'react'
import { useMap } from 'react-map-gl/maplibre'
import { twJoin } from 'tailwind-merge'
import { clamp, type HashLocation } from './hash'
import type { MapLayerConfig } from './layers'
import { OverlayLayerSelection } from './OverlayLayerSelection'
import { OverlayLinks } from './OverlayLinks'

type Props = {
  layers: MapLayerConfig[]
  selectedLayer: MapLayerConfig
  onSelectLayer: (layerId: string) => void
  location: HashLocation
}

export const Overlay = ({ layers, selectedLayer, onSelectLayer, location }: Props) => {
  // Collapsed on small screens so the map stays visible
  const [defaultOpen] = useState(() => window.matchMedia('(min-width: 1024px)').matches)
  const { current: map } = useMap()

  const handleSelectLayer = (layerId: string) => {
    // Layers have different areas (e.g. Release 01 only Neukölln). When the view is outside the new
    // layer's area, move inside first; `jumpTo` fires `moveend`, which keeps the URL hash in sync.
    const layer = layers.find((layer) => layer.id === layerId)
    const center = map?.getCenter()
    if (map && layer && center) {
      const [west, south, east, north] = layer.bounds
      const longitude = clamp(center.lng, west, east)
      const latitude = clamp(center.lat, south, north)
      if (longitude !== center.lng || latitude !== center.lat) {
        map.jumpTo({ center: [longitude, latitude] })
      }
    }
    onSelectLayer(layerId)
  }

  return (
    <nav
      aria-label="Karte wechseln"
      className="absolute top-3 left-3 flex max-h-[calc(100%-3rem)] w-56 max-w-[calc(100%-4.5rem)] flex-col overflow-y-auto rounded-md bg-white shadow-sm lg:top-4 lg:left-4"
    >
      <Disclosure defaultOpen={defaultOpen}>
        {({ open }) => (
          <>
            <DisclosureButton className="flex cursor-pointer items-center gap-1 px-2 py-1.5 text-left text-sm font-medium hover:bg-blue-50">
              <ChevronRightIcon
                className={twJoin('h-4 w-4 flex-none transition-transform', open && 'rotate-90')}
              />
              Karte wechseln
            </DisclosureButton>
            <DisclosurePanel>
              <OverlayLayerSelection
                layers={layers}
                selectedLayer={selectedLayer}
                onSelect={handleSelectLayer}
              />
              <OverlayLinks location={location} />
            </DisclosurePanel>
          </>
        )}
      </Disclosure>
    </nav>
  )
}
