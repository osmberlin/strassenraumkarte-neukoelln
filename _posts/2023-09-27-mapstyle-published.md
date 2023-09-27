---
title: "Kartenstil der Straßenraumkarte endlich veröffentlicht"
menu_title: "Mapstyle"
menu_highlight: mapstyle
date: 2023-09-26 13:00:00 +0100
author: Alex Seidel @Supaplex030
layout: post
description: Der Kartenstil der Straßenraumkarte ist nun als QGIS-Projekt frei verfügbar.
---

_English below._

Vor einiger Zeit [haben wir beschrieben](/posts/2022-01-17-meine-stadt), warum es sehr aufwendig oder vielleicht sogar unmöglich ist, die [Neuköllner Straßenraumkarte](https://strassenraumkarte.osm-berlin.org/?map=micromap) für andere Städte oder Stadtteile aufzusetzen. Das lag zum Beispiel daran, dass die Straßenraumkarte ursprünglich nur als Kartengrundlage für OSM-Projekte im Berliner Ortsteil Neukölln gedacht war und einige essentielle Kartenlayer nutzte, die speziell für diesen Ort erstellt wurden – insbesondere die Fahrbahnflächen und die Daten zum Parken im Straßenraum. Außerdem sind für einige Kartenaspekte sehr detaillierte Micromapping-Methoden notwendig, damit beispielsweise die Fahrbahnmarkierungen realistisch aussehen. All das ist aber mit OSM sowie von uns bereitgestellten Scripten zur Datenprozessierung möglich und sollte inzwischen keine unüberwindbare Hürde mehr darstellen.

Zum anderen basierte die Karte aber auch auf einem laienhaften technischen Hintergrundwissen. Das machte es bislang unmöglich, den Kartenstil einfach zu veröffentlichen, denn die Daten hätten nicht reproduzierbar eingeladen und dargestellt werden können. Zu viele lokale Verweise und Workarounds versteckten sich dafür im Unterbau. Hier wurde aber inzwischen etwas aufgeräumt, sodass der Kartenstil nun auch woanders laufen kann.

Daher steht der Kartenstil der Straßenraumkarte nun als QGIS-Projekt zur freien Verfügung und kann gern für Experimente an anderen Orten genutzt werden. Informationen und eine Schritt-für-Schritt-Anleitung gibt es [im Repository auf einer eigenen Unterseite](https://github.com/SupaplexOSM/strassenraumkarte-neukoelln/tree/main/mapstyle).

---

Some time ago [we explained](/posts/2022-01-17-meine-stadt) why it is very difficult or even impossible to set up the [Straßenraumkarte Neukölln](https://strassenraumkarte.osm-berlin.org/?map=micromap) for other cities or districts. This was due to the fact that this map was originally only intended as a base map for OSM projects in the Berlin district of Neukölln and used some essential map layers that were created specifically for this location - in particular the carriageway areas and the data for on street parking. In addition, some aspects of the map require very detailed micromapping methods so that, for example, the road markings look realistic. However, all this is possible with OSM and the scripts we provide for data processing and should no longer be an impassable hurdle.

On the other hand, the map was also based on an amateurish technical background knowledge. So far, this made it impossible to simply publish the map style, because the data would not have been reproducibly loaded and displayed. Too many local references and workarounds were hidden in the background. In the meantime, however, this has been tidied up somewhat, so that the map style can now also be used in other places.

So now the map style of the Straßenraumkarte is freely available as a QGIS project and is welcome to be used for experiments in other locations. More information and step-by-step instructions are available [in the repository on a separate subpage](https://github.com/SupaplexOSM/strassenraumkarte-neukoelln/tree/main/mapstyle).
