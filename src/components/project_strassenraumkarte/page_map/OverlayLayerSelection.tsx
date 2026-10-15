import { Description, Label, Radio, RadioGroup } from '@headlessui/react'
import { twJoin } from 'tailwind-merge'
import { formatDataDate, type MapGroup, type MapLayerConfig } from './layers'

type Props = {
  layers: MapLayerConfig[]
  selectedLayer: MapLayerConfig
  onSelect: (layerId: string) => void
}

const groupOrder: MapGroup[] = ['micromap', 'parkingmap', 'debugmap', 'background']

export const OverlayLayerSelection = ({ layers, selectedLayer, onSelect }: Props) => {
  // Hidden layers (debug) are only listed when they are selected via URL
  const visibleLayers = groupOrder.flatMap((group) =>
    layers.filter(
      (layer) => layer.group === group && (!layer.hidden || layer.id === selectedLayer.id),
    ),
  )

  return (
    <RadioGroup value={selectedLayer.id} onChange={onSelect} aria-label="Karte wechseln">
      {visibleLayers.map((layer, index) => {
        // A thin divider between the maps (Straßenraumkarte, Parkraumkarte, …) and the backgrounds
        const startsGroup = index > 0 && visibleLayers[index - 1]?.group !== layer.group
        return (
          <Radio
            key={layer.id}
            value={layer.id}
            className={({ checked }) =>
              twJoin(
                startsGroup && 'border-t border-gray-200',
                checked ? 'bg-emerald-50' : 'hover:bg-blue-50',
                'flex w-full cursor-pointer gap-2 px-3 py-1.5 focus:outline-hidden',
              )
            }
          >
            {({ focus, checked }) => (
              <>
                <span
                  className={twJoin(
                    checked ? 'border-transparent bg-emerald-600' : 'border-gray-300 bg-white',
                    focus ? 'ring-2 ring-emerald-600 ring-offset-1' : '',
                    'mt-0.5 flex h-3.5 w-3.5 shrink-0 items-center justify-center rounded-full border',
                  )}
                  aria-hidden="true"
                >
                  <span className="h-1.5 w-1.5 rounded-full bg-white" />
                </span>
                <span className="flex flex-col leading-tight">
                  <Label
                    as="span"
                    className={twJoin(
                      checked ? 'font-medium text-emerald-900' : 'text-gray-900',
                      'text-sm',
                    )}
                  >
                    {layer.title}
                  </Label>
                  {checked && (layer.dataDate || layer.note) && (
                    <Description as="span" className="mt-0.5 text-xs text-emerald-700">
                      {layer.dataDate && `Datenstand ${formatDataDate(layer.dataDate)}`}
                      {layer.note && <span className="block">{layer.note}</span>}
                    </Description>
                  )}
                </span>
              </>
            )}
          </Radio>
        )
      })}
    </RadioGroup>
  )
}
