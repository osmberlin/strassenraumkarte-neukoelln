# Straßenraumkarte Neukölln

---

***Update 2026-08:* There is a new, modernised version of the Straßenraumkarte style and processing** based on an osm2pgsql / SQL / QGIS workflow, living at [osmberlin/strassenraumkarte](https://github.com/osmberlin/strassenraumkarte).

---

Die Straßenraumkarte ist ein Kartenstil mit besonderem Fokus auf die räumliche Aufteilung des Stadt- und Straßenraums, insbesondere der Fahrbahnen und Objekte im öffentlichen Raum oder der urbanen Landnutzung. Sie wurde als Kartengrundlage für OpenStreetMap-Projekte in Berlin-Neukölln entwickelt, kann mit etwas Aufwand inzwischen aber auch an anderen Orten erzeugt werden.

Der Reiz des Kartenstils, der ästhetisch an Architektur-Pläne angeleht ist, besteht in der detaillierten Darstellung städtischer Umgebungen. Im Fokus stehen z.B. Fahrbahnflächen, Stadtmöbel, Gebäude, Landnutzungsdetails oder parkenden Autos im Straßenraum. Sollen diese Dinge an einem Ort dargestellt werden, ist es in den meisten Fällen zunächst notwendig, diese in OpenStreetMap zu erfassen, was ein aufwendiger Prozess sein kann. Mehr dazu siehe im Unterordner zum [MapStyle der Straßenraumkarte](https://github.com/SupaplexOSM/strassenraumkarte-neukoelln/tree/main/mapstyle).

_[>> Zur Straßenraumkarte](https://strassenraumkarte.osm-berlin.org/?map=micromap)_

Die Neuköllner Parkraumkarte ergänzt diese Kartengrundlage um Daten zum Kfz-Parken.

_[>> Zur Parkraumkarte](https://parkraum.osm-verkehrswende.org/project-prototype-neukoelln/?map=parkingmap)_
- [Parkraumkarte Zoomlevel 15: Stellplatzdichte – Parking Space Density](https://parkraum.osm-verkehrswende.org/project-prototype-neukoelln/?map=parkingmap#15/52.4772/13.4393)
- [Parkraumkarte Zoomlevel 16: Flächenverbrauch – Land Consumption](https://parkraum.osm-verkehrswende.org/project-prototype-neukoelln/?map=parkingmap#16/52.4820/13.4333)
- [Parkraumkarte Zoomlevel 17: Parkstreifen / Parken im Straßenraum – Street Parking](https://parkraum.osm-verkehrswende.org/project-prototype-neukoelln/?map=parkingmap#17/52.48085/13.43278)
- [Parkraumkarte Zoomlevel 18-19: Parkstreifen- und Stellplatzdetails – Parking Details](https://parkraum.osm-verkehrswende.org/project-prototype-neukoelln/?map=parkingmap#18/52.48090/13.43234)

![grafik](https://github.com/SupaplexOSM/strassenraumkarte-neukoelln/blob/main/images/sample_image.jpg)

## FAQ: Kann ich die Straßenraumkarte auch für meine Stadt generieren?

Das ist leider nicht so einfach, wie es vielleicht aussieht. Mehr dazu siehe im Unterordner zum [MapStyle der Straßenraumkarte](https://github.com/SupaplexOSM/strassenraumkarte-neukoelln/tree/main/mapstyle).

# Development (project page)

This page is built with [Astro](https://astro.build/), aligned with [www.osm-verkehrswende.org](https://github.com/osmberlin/www.osm-verkehrswende.org): `.astro` files for layouts and pages, MDX for posts, React for the map ([react-map-gl](https://visgl.github.io/react-map-gl/) with MapLibre), Tailwind CSS.

Use [Bun](https://bun.sh/) for installs and scripts:

- `bun install`
- `bun run dev` – local dev server
- `bun run build` – static build into `dist/`
- `bun run check` – type-check, format, lint

## Deploy

Push to `main`. The GitHub Action (`.github/workflows/deploy.yml`) builds the page and deploys it to GitHub Pages.

## Map and tile releases

Every rendered data state of a map is a "release" with its own folder on the tile server, e.g. `https://tiles.osm-berlin.org/release01/{z}/{x}/{y}.webp`.
Each release is one JSON file in `src/content/releases/` (schema: `src/content.config.ts`). The file name is the release id.

To add a release:

1. Upload the tiles to a new folder (e.g. `release02/`) on the tile server.
2. Add `src/content/releases/release02.json` with `map`, `title`, `dataDate` (Datenstand), `tiles` and optionally `bounds` and `note`.
3. To make it the default, move `"default": true` from the old release to the new one. Each map (`micromap`, `parkingmap`, `debugmap`) needs exactly one default release; the build fails otherwise.

URLs:

- `?map=<release id>` (e.g. `?map=release01`) opens a specific release; `?map=osm|luftbild2020|luftbild2024` the background maps.
- `?map=micromap|parkingmap|debugmap` opens the default release of that map. Old links keep working that way.
- `#<zoom>/<lat>/<lng>` is the map position (same format and zoom levels as the old Leaflet page).
- Old Jekyll URLs (`/posts/…`, `*.html` pages of the Parkraumkarte) redirect via `redirects` in `astro.config.mjs` and the static files in `public/`.
