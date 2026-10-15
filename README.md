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

Every rendered data state of a map is a "release", e.g. `release01` (jpg, Datenstand 2024-04-02) and `release02` (webp, new renderer, Datenstand 2026-10-14).
Each release is one JSON file in `src/content/releases/` (schema: `cms/releasesAstro.ts`). The file name is the release id.

**There is always one latest release per map**: the one with the newest `dataDate`. The map and all old URLs open the latest release; older releases stay available in the layer picker of the map ("Karte wechseln") and via `?map=<release id>`.

Each release has its own `bounds` (`[west, south, east, north]`): no tiles are requested outside, and the map can not be moved outside while that release is shown (e.g. `release02` all of Berlin, `release01` only Neukölln).

For now both Straßenraumkarte releases still load from `https://tiles.osm-berlin.org/strassenraumkarte/` (jpg and webp side by side). New releases should get their own folder on the tile server (e.g. `release03/`); moving an existing release is a one-line change of `tiles` in its JSON file.

To add a release:

1. Upload the tiles to a new folder (e.g. `release03/`) on the tile server.
2. Add `src/content/releases/release03.json` with `map`, `dataDate` (Datenstand), `tiles`, `bounds` and optionally `note` and `aliases` (old `?map=` values).
3. That's it: with the newest `dataDate` it becomes the latest release. Two releases of one map with the same newest `dataDate` fail the build.

Background layers (OpenStreetMap, aerial images 2024 and 2026 from the Geoportal Berlin WMS) are defined in `src/components/project_strassenraumkarte/page_map/layers.ts`.

URLs:

- `?map=<release id>` (e.g. `?map=release01`) opens a specific release; `?map=osm|luftbild2024|luftbild2026` the background maps.
- Old values are redirected to the release id on load: no `?map`, `?map=micromap|parkingmap|debugmap` → the latest release of that map; `?map=micromap_preview` → `release02`; `?map=luftbild2020` → `luftbild2024`.
- `#<zoom>/<lat>/<lng>` is the map position (same format and zoom levels as the old Leaflet page).
- Old Jekyll URLs (`/posts/…`, `*.html` pages of the Parkraumkarte) redirect via `redirects` in `astro.config.mjs` and the static files in `public/`.
