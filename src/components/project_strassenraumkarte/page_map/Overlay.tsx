import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/react'
import { ChevronRightIcon } from '@heroicons/react/24/outline'
import { useState } from 'react'
import { twJoin } from 'tailwind-merge'
import type { HashLocation } from './hash'
import { formatDataDate, layerTitle, type MapLayerConfig } from './layers'
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

  return (
    <nav
      aria-label="Karte und Datenstand auswählen"
      className="absolute top-3 left-3 flex max-h-[calc(100%-3rem)] max-w-[calc(100%-4.5rem)] flex-col overflow-y-auto rounded-md bg-white shadow-sm lg:top-6 lg:left-6"
    >
      <Disclosure defaultOpen={defaultOpen}>
        {({ open }) => (
          <>
            <DisclosureButton className="flex cursor-pointer items-center gap-1 px-2 py-2 text-left text-sm hover:bg-blue-50">
              <ChevronRightIcon
                className={twJoin('h-5 w-5 flex-none transition-transform', open && 'rotate-90')}
              />
              <span>
                <span className="font-medium">{layerTitle(selectedLayer)}</span>
                {selectedLayer.dataDate &&
                  ` – Datenstand ${formatDataDate(selectedLayer.dataDate)}`}
              </span>
            </DisclosureButton>
            <DisclosurePanel>
              <OverlayLayerSelection
                layers={layers}
                selectedLayer={selectedLayer}
                onSelect={onSelectLayer}
              />
              <OverlayLinks location={location} />
            </DisclosurePanel>
          </>
        )}
      </Disclosure>
    </nav>
  )
}
