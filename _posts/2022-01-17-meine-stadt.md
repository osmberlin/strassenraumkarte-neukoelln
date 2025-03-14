---
title: "FAQ: Kann ich die Straßenraumkarte auch für meine Stadt generieren?"
menu_title: "FAQ: Meine Stadt"
menu_highlight: mehr_details
date: 2022-01-17 23:00:00 +0100
author: Alex Seidel @Supaplex030
layout: post
description: Warum die Karte nicht ohne weiteres für andere Stadte gebaut werden kann.
---

<div class="notice mb-7">

_Nachtrag September 2023:_

Der Mapstyle der Straßenraumkarte ist inzwischen als QGIS-Projekt frei verfügbar und kann somit auch leichter für andere Städten genutzt werden. Kompliziert ist es aber immer noch. Mehr dazu auf der Unterseite zum [Mapstyle der Straßenraumkarte](https://github.com/SupaplexOSM/strassenraumkarte-neukoelln/tree/main/mapstyle).

</div>

Wir werden oft gefragt…

## Kann ich die Straßenraumkarte auch für meine Stadt generieren?

Das ist leider sehr kompliziert und zur Zeit vielleicht unmöglich - aus verschiedenen Gründen:

- Die Neuköllner Straßenraumkarte lebt von der detaillierten Darstellung der Fahrbahnflächen und Parkplätze am Straßenrand. Diese beiden Datenebenen direkt aus OSM zu rendern, ist zur Zeit eher Theorie - in der Praxis verwendet die Neuköllner Karte dafür "handgebaute" Datenlayer aus ALKIS- und OSM-Daten, die extra für die Straßenraumkarte erzeugt wurden und weiter gepflegt werden. Unter erheblichem Informationsverlust könnten die exakten Fahrbahnflächen durch generische Linien aus den OSM-Straßendaten ersetzt werden, was im Vergleich zum Detail- und Präzisionsanspruch der Darstellung aber nur unbefriedigende Ergebnisse liefern dürfte. Der straßenbegeleitende Parkraum ist außerdem nur an sehr wenigen Orten in OSM kartiert.
- Die Straßenraumkarte lebt darüber hinaus von dem sehr hohen Detailgrad der OSM-Daten in Berlin Neukölln. Diese sind zum Teil seit Jahren aufwendig gemappt worden, auch unter Einbezug der sehr guten externen Datenquellen, die in Berlin OSM-kompatibel zur Verfügung stehen (z.B. jährlich neue Luftbilder in hoher Auflösung oder zentimetergenaue ALKIS-Daten). Insbesondere für das [Radweg- und Fahrspur-Rendering](https://supaplexosm.github.io/strassenraumkarte-neukoelln/posts/2021-12-31-micromap-update) berücksichtigt die Straßenraumkarte außerdem Taggings, die vielerorts nicht gemappt sind und einen besonders hohen Präzisionsgrad erfordern.
- Die "Architektur" der Straßenraumkarte ist zur Zeit eher laienhaft angelegt, da sie organisch und ohne tiefere Kenntnisse über die Materie der Kartendarstellung gewachsen ist und ursprünglich nur als "einfache Kartengrundlage" zur [Neuköllner Parkraumanalyse](https://supaplexosm.github.io/strassenraumkarte-neukoelln/parkraumkarte/report) gedacht war. Die Straßenraumkarte ist im Hintergrund derzeit nichts anderes als eine QGIS-Datei mit einer großen Anzahl absoluter Dateipfade und einigen quick-and-dirty workarounds, um mit unterschiedlichen Projektionen der zu Grunde liegenden Layer umzugehen (darunter bislang der Berlin-spezifischen Projektion ETRS89 / UTM Zone 33N). Diese Architektur so umzugestalten, dass auch andere etwas damit anfangen könnten, ist leider nicht nur aufwendig, sondern bislang auch gescheitert. Daher enthält das Repository noch keine Stil-Dateien o.ä. zum Erzeugen der Straßenraumkarte.
