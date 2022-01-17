# OSM Straßen- und Parkraumkarte Neukölln

Die Straßenraumkarte bietet eine detaillierte Kartengrundlage für den Berliner Ortsteil Neukölln auf Basis von OpenStreetMap-Daten. Die Parkraumkarte ergänzt diese Kartengrundlage um Daten zum Kfz-Parken.

* [Straßenraumkarte](https://supaplexosm.github.io/strassenraumkarte-neukoelln/?map=micromap#15/52.4772/13.4393)
* [Parkraumkarte Zoomlevel 15: Stellplatzdichte – Parking Space Density](https://supaplexosm.github.io/strassenraumkarte-neukoelln/?map=parkingmap#15/52.4772/13.4393)
* [Parkraumkarte Zoomlevel 16: Flächenverbrauch – Land Consumption](https://supaplexosm.github.io/strassenraumkarte-neukoelln/?map=parkingmap#16/52.4820/13.4333)
* [Parkraumkarte Zoomlevel 17: Parkstreifen / Parken am Fahrbahnrand – Lane Parking](https://supaplexosm.github.io/strassenraumkarte-neukoelln/?map=parkingmap#17/52.48085/13.43278)
* [Parkraumkarte Zoomlevel 18-19: Parkstreifen- und Stellplatzdetails – Parking Details](https://supaplexosm.github.io/strassenraumkarte-neukoelln/?map=parkingmap#18/52.48090/13.43234)


## Kann ich die Straßenraumkarte auch für meine Stadt generieren?

Das ist leider sehr kompliziert und zur Zeit vielleicht unmöglich - aus verschiedenen Gründen:
* Die Neuköllner Straßenraumkarte lebt von der detaillierten Darstellung der Fahrbahnflächen und Parkplätze am Straßenrand. Diese beiden Datenebenen direkt aus OSM zu rendern, ist zur Zeit eher Theorie - in der Praxis verwendet die Neuköllner Karte dafür "handgebaute" Datenlayer aus ALKIS- und OSM-Daten, die extra für die Straßenraumkarte erzeugt wurden und weiter gepflegt werden. Unter erheblichem Informationsverlust könnten die exakten Fahrbahnflächen durch generische Linien aus den OSM-Straßendaten ersetzt werden, was im Vergleich zum Detail- und Präzisionsanspruch der Darstellung aber nur unbefriedigende Ergebnisse liefern dürfte. Der straßenbegeleitende Parkraum ist außerdem nur an sehr wenigen Orten in OSM kartiert. 
* Die Straßenraumkarte lebt darüber hinaus von dem sehr hohen Detailgrad der OSM-Daten in Berlin Neukölln. Diese sind zum Teil seit Jahren aufwendig gemappt worden, auch unter Einbezug der sehr guten externen Datenquellen, die in Berlin OSM-kompatibel zur Verfügung stehen (z.B. jährlich neue Luftbilder in hoher Auflösung oder zentimetergenaue ALKIS-Daten). Insbesondere für das [Radweg- und Fahrspur-Rendering](https://supaplexosm.github.io/strassenraumkarte-neukoelln/posts/2021-12-31-micromap-update) berücksichtigt die Straßenraumkarte außerdem Taggings, die vielerorts nicht gemappt sind und einen besonders hohen Präzisionsgrad erfordern.
* Die "Architektur" der Straßenraumkarte ist zur Zeit eher laienhaft angelegt, da sie organisch und ohne tiefere Kenntnisse über die Materie der Kartendarstellung gewachsen ist und ursprünglich nur als "einfache Kartengrundlage" zur [Neuköllner Parkraumanalyse](https://supaplexosm.github.io/strassenraumkarte-neukoelln/parkraumkarte/report) gedacht war. Die Straßenraumkarte ist im Hintergrund derzeit nichts anderes als eine QGIS-Datei mit einer großen Anzahl absoluter Dateipfade und einigen quick-and-dirty workarounds, um mit unterschiedlichen Projektionen der zu Grunde liegenden Layer umzugehen (darunter bislang der Berlin-spezifischen Projektion ETRS89 / UTM Zone 33N). Diese Architektur so umzugestalten, dass auch andere etwas damit anfangen könnten, ist leider nicht nur aufwendig, sondern bislang auch gescheitert. Daher enthält das Repository noch keine Stil-Dateien o.ä. zum Erzeugen der Straßenraumkarte.


# Development (project page)

* We use Jekyll to generate the pages – https://jekyllrb.com/
* We use TailwindCSS in JIT mode to generate the css file – https://tailwindcss.com/docs/just-in-time-mode

## Installation

`npm install`

Will install Jekyll, TailwindCSS and other required plugins.

## Development

`npm run dev`

Will run TailwindCSS JIT in parallel with Jekyll. Both use live reloading.

## Deploy

_Did CSS change?_

* _Yes, CSS did change?_ – Run `npm run build`, then commit changes to the `css/tailwind.css`.
* _No, CSS did not change?_ – Commit changes, Github pages will build and update the page.


## Useful links

* Jekyll template language reference – https://shopify.github.io/liquid/basics/introduction/ Liquid Template Language
* HTML to Markdown copy-paste https://euangoddard.github.io/clipboard2markdown/
* Google Doc/Word to HTML-Table copy-paste https://www.gdoctohtml.com/
