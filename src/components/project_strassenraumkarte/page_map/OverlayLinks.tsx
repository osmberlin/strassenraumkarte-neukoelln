import type { HashLocation } from './hash'

const linkClasses = 'text-sm text-blue-600 underline hover:text-blue-800'

type Props = { location: HashLocation }

/** Links to edit/inspect the current map view elsewhere. `location.zoom` is in Leaflet zoom. */
export const OverlayLinks = ({ location }: Props) => {
  const zoom = Math.round(location.zoom)
  const precision = Math.max(0, Math.ceil(Math.log(zoom) / Math.LN2))
  const lat = location.latitude.toFixed(precision)
  const lng = location.longitude.toFixed(precision)

  return (
    <div className="flex gap-4 border-t border-gray-200 px-4 py-2">
      <a
        // Will pick the default editor based on user preferences. Add ?editor=id to force iD.
        href={`https://www.openstreetmap.org/edit#map=${zoom}/${lat}/${lng}`}
        className={linkClasses}
        target="_blank"
        rel="noopener noreferrer"
      >
        In OSM bearbeiten
      </a>
      <a
        href={`https://www.mapillary.com/app/?z=${zoom}&lat=${lat}&lng=${lng}&focus=map&dateFrom=2020-01-01`}
        className={linkClasses}
        target="_blank"
        rel="noopener noreferrer"
      >
        Mapillary
      </a>
    </div>
  )
}
