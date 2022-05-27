# OSM Straßen- und Parkraumkarte Neukölln

Die Straßenraumkarte bietet eine detaillierte Kartengrundlage für den Berliner Ortsteil Neukölln auf Basis von OpenStreetMap-Daten. Die Parkraumkarte ergänzt diese Kartengrundlage um Daten zum Kfz-Parken.

- [Straßenraumkarte](https://supaplexosm.github.io/strassenraumkarte-neukoelln/?map=micromap#15/52.4772/13.4393)
- [Parkraumkarte Zoomlevel 15: Stellplatzdichte – Parking Space Density](https://supaplexosm.github.io/strassenraumkarte-neukoelln/?map=parkingmap#15/52.4772/13.4393)
- [Parkraumkarte Zoomlevel 16: Flächenverbrauch – Land Consumption](https://supaplexosm.github.io/strassenraumkarte-neukoelln/?map=parkingmap#16/52.4820/13.4333)
- [Parkraumkarte Zoomlevel 17: Parkstreifen / Parken am Fahrbahnrand – Lane Parking](https://supaplexosm.github.io/strassenraumkarte-neukoelln/?map=parkingmap#17/52.48085/13.43278)
- [Parkraumkarte Zoomlevel 18-19: Parkstreifen- und Stellplatzdetails – Parking Details](https://supaplexosm.github.io/strassenraumkarte-neukoelln/?map=parkingmap#18/52.48090/13.43234)

## FAQ: Kann ich die Straßenraumkarte auch für meine Stadt generieren?

[Das ist leider sehr kompliziert und zur Zeit vielleicht unmöglich. – Mehr dazu…](https://supaplexosm.github.io/strassenraumkarte-neukoelln/posts/2022-01-17-meine-stadt)

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
