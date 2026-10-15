import { Description, Label, Radio, RadioGroup } from '@headlessui/react'
import { Fragment } from 'react'
import { twJoin } from 'tailwind-merge'
import { formatDataDate, groupTitles, type MapGroup, type MapLayerConfig } from './layers'

type Props = {
  layers: MapLayerConfig[]
  selectedLayer: MapLayerConfig
  onSelect: (layerId: string) => void
}

const groupOrder: MapGroup[] = ['micromap', 'parkingmap', 'debugmap', 'background']

export const OverlayLayerSelection = ({ layers, selectedLayer, onSelect }: Props) => {
  // Hidden layers (debug) are only listed when they are selected via URL
  const visibleLayers = layers.filter((layer) => !layer.hidden || layer.id === selectedLayer.id)

  return (
    <RadioGroup value={selectedLayer.id} onChange={onSelect} aria-label="Karte auswählen">
      {groupOrder.map((group) => {
        const groupLayers = visibleLayers.filter((layer) => layer.group === group)
        if (!groupLayers.length) return null
        return (
          <Fragment key={group}>
            <div className="-mx-px -mt-px border border-gray-200 bg-gray-50 px-4 pt-2.5 pb-1 text-xs font-semibold tracking-wide text-gray-500 uppercase">
              {groupTitles[group]}
            </div>
            {groupLayers.map((layer) => (
              <Radio
                key={layer.id}
                value={layer.id}
                className={({ checked }) =>
                  twJoin(
                    '-mx-px -mt-px',
                    checked ? 'z-10 border-emerald-200 bg-emerald-50' : 'border-gray-200',
                    'relative flex w-full min-w-[17em] cursor-pointer border px-4 py-2 hover:bg-blue-50 focus:outline-hidden',
                  )
                }
              >
                {({ focus, checked }) => (
                  <>
                    <span
                      className={twJoin(
                        checked ? 'border-transparent bg-emerald-600' : 'border-gray-300 bg-white',
                        focus ? 'ring-2 ring-emerald-600 ring-offset-2' : '',
                        'mt-0.5 flex h-4 w-4 shrink-0 cursor-pointer items-center justify-center rounded-full border',
                      )}
                      aria-hidden="true"
                    >
                      <span className="h-1.5 w-1.5 rounded-full bg-white" />
                    </span>
                    <span className="ml-3 flex flex-col">
                      <Label
                        as="div"
                        className={twJoin(
                          checked ? 'font-medium text-emerald-900' : 'font-normal text-gray-900',
                          'text-sm',
                        )}
                      >
                        {layer.dataDate
                          ? `Datenstand ${formatDataDate(layer.dataDate)}`
                          : layer.title}
                        {layer.default && <span className="text-gray-500"> (Standard)</span>}
                      </Label>
                      {layer.note && (
                        <Description
                          as="span"
                          className={twJoin(
                            checked ? 'text-emerald-700' : 'text-gray-500',
                            'block text-xs',
                          )}
                        >
                          {layer.note}
                        </Description>
                      )}
                    </span>
                  </>
                )}
              </Radio>
            ))}
          </Fragment>
        )
      })}
    </RadioGroup>
  )
}
