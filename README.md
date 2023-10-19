# Straßenraumkarte Neukölln

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

- We use Jekyll to generate the pages – https://jekyllrb.com/
- We use Tailwind CSS in JIT mode to generate the css file – https://tailwindcss.com/docs/just-in-time-mode

## Installation

`npm install`

Will install Jekyll, Tailwind CSS and other required plugins.

## Development

`npm run dev`

Will run Tailwind CSS JIT in parallel with Jekyll. Both use live reloading.

## Deploy

_Did CSS change?_

- _Yes, CSS did change?_ – Run `npm run build`, then commit changes to the `css/tailwind.css`.
- _No, CSS did not change?_ – Commit changes, Github pages will build and update the page.

## Useful links

- Jekyll template language reference – https://shopify.github.io/liquid/basics/introduction/ Liquid Template Language
- HTML to Markdown copy-paste https://euangoddard.github.io/clipboard2markdown/
- Google Doc/Word to HTML-Table copy-paste https://www.gdoctohtml.com/
