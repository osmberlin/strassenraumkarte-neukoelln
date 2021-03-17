---
title: Was muss ich tun, um eine Parkplatzanalyse in meinem Kiez durchzuführen.
date: 2021-03-17 19:00:00 +0100
author: Tobias Jordans @tordans
layout: post
# menu_highlight:
# canonical_url:
---

```WIP. Dieser Artikel ist noch in Arbeit.```

## Es ist nicht mal eben schnell gemacht
{: class="mt-5 mb-4" }

Diese Parkraumanalyse basiert auf OpenStreetMap.
Jede*r kann sie in seinem eigenen Kiez oder Stadt selbst durchführen.
Dafür ist aber einiges zu tun, das ich hier auflisten möchte.

**Erwartungsmanagement**

Um die Daten für diese Analse zu erfassen (Norneukölln + 500 m in angrenzenden Bezirken) hat Alex ca. 120 Stunden (15 Vollzeittage) ehrenamtlich investiert.[^1]

Hinzu kommt die Zeit für die Entwicklung der Skripte, Analyse und das Schreiben der Dokumentation. Alles Sdinge, die bei dir sehr viel weniger Aufwand brauchen werden, wenn du auf die Vorarbeit hier zurückgreifst.

[^1]: Annahme: 2 Monate &times; 4,3 Wochen/Monat &times; 7 Tage/Woche &times; 2 Stunden/Tag = 120 Stunden.

## OpenStreetMap (OSM)
{: class="mt-5 mb-4" }

Grundsätzlich gibt es zwei zenrale Datenquellen:
1. OSM – eine frei zugängliche und verfügbare Geodatenbank
2. Die KFZ-Anmeldedaten, die für ganz Berlin vorliegen ([unter "Daten"](../parkraumkarte/data#melderechtlich-reg-einwohner-berlin-mit-kfz))

**Aber**, OSM ist zwar grundsätzlich verfügbar, es heißt aber nicht, dass in deinem Untersuchungsbereich bereits die nötigen Daten eingetragen wurden.

In den aller meisten Fällen wirst du erstmal Daten in OSM ablegen müssen (Daten erfassen oder, wie wir sagen, "mappen"), damit sie dann für diese Auswertung verwendet werden können.

Es ist trotzdem sehr sinnvoll, OSM als Datenspeicher zu nutzen, da (a) bereits sehr viele der nötigen Umgebungsinformationen (Straßen, Häuser, Kreuzungen etc) vorhanden sind, (b) ein ausgearbeitets Erfassungsschema, (c) eine aktive Community an hilsbereiten Menschen, sowie Tools und Hilfedokumenten existieren und nicht zuletzte (d) alle davon profitieren, wenn OSM mit mehr guten Daten angereicht wird.

Ergänzung: Um es besonders hübsch zu machen, sind zusätzlich noch einige Arbeitsschritte nötig um gute Bordsteinkantendaten zu erhalten. Alex beschreibt im [Methodenbericht](../report) und
im (kommenden) Blogpost zur Straßenraumkarte (Link `TODO`)
gut, welchen Vorteil das hat, und welchen Aufwand. Außerdem hat er analysiert, dass diese zusätzliche Präzision optional ist, da sie nur wenig zusätzliche Genauigkeit liefert.

## Welche Daten in OSM erfasst werden müssen
{: class="mt-5 mb-4" }

Um eine präzise Auswertung durchzuführen, müssen diese Daten – aktuell und vollstäing – in OSM erfasst werden.

**Dimension 1: Parkspuren (1)**

An jeder Straße in OSM muss angegeben werden, wie dort geparkt werden darf.

**Dimension 2: Alles, was Parkraum wegnimmt**

Zusätzlich muss alles erfasst werden, was verhindert, dass ein Auto parken kann. Diese OSM-Daten können im Rahmen der Auswertung verwendet werden, um automatisch die Anzahl der verfügbaren Parkplätze zu reduzieren. Detail stehen im Methodenbericht.

* **(2) Kreuzunge** – in Kurven darf nicht geparkt werden; das Skript berücksichtigt die 5m-Schutzzone; Kreuzungen sind meist in OSM schon alle erfasst
* **(3) Häusereinfahrten** – vor Hauseinfahrten darf nicht geparkt werden darf; das Skript zieht automatisch Parkraum ab
* **(4) Gehwegübergänge** – an Ampeln, Zebrastreifen, vor Gehwegvorstreckungen etc. darf nicht geparkt werden; das Skritp zieht automatisch Parkraum ab
* **(5) Fahrradständer auf dem Parkstreifen** – dito
* (6) `TODO`

## Daten in OSM erfassen
{: class="mt-5 mb-4" }

Jetzt wird es kompliziert. Dieser Artikel kann dieses Thema nur anreißen. [Bitte melde dich, wenn du mehr erfahren möchtest](../contact).

### Zu 1: Parkspuren
{: class="mt-5 mb-4" }

**Wo sind schon Parspur-Daten erfasst?**

`TODO Overpass Query-Page: Straßen mit / ohne parking:lane-Daten`

**Welche Qualität haben diese Daten?**

`TODO Overpass Query-Page: Straßen mit parking:lane-Daten und ihre Vollständigkeit der Daten`

**Daten eintragen**

Es gibt in OSM sehr viele Methoden, um Daten in die Datenbank einzutragen. Sie brauchen unterschiedlich viel Einarbeitungszeit und sind unterschiedlich gut für Neulinge geeignet.

Ein Tool, das sich rein auf Parkspuren optimiert ist, ist [https://zlant.github.io/parking-lanes/](https://zlant.github.io/parking-lanes/#17/52.47906/13.42876). Aber auch das könnte einfacher zu bedienen sein.

`TODO: Erklärung Tool`

### Zu 2: Kreuzungen
{: class="mt-5 mb-4" }

Im Normalfall sind Kreuzungen bereits vollständig in OSM erfasst. Wir empfehlen, auf Basis der aktuellsten Luftbilder einmal zu überprüfen, ob die Geometrien der Straßen an den Kreuzungen optimiert werden kann.

Abgesehen davon ist nichts zu tun; OSM ist hier schon vollständig.

### Zu 3: Häusereinfahren
{: class="mt-5 mb-4" }

Berlin hat sehr viele Häusereinfahrten. Für diese Parkkraumanalse haben wir alle Straßen abgelaufen und alle Häusereinfahrten eingetragen, die dieser Definition entsprechen:

- Es gibt einen am Bürgersteig sichtbaren Zufahrtsweg zum Haus
- Es gibt einen abgesenkten Bordstein
- Es ist ein Abschleppen-Schild an der Einfahrt / am Tor angebracht

Das ist unser Regelfall. Einzelfälle müsst ihr vor Ort prüfen. Aber wenn bspw. ein abgesenkter Bordstein vorliegt aber eindeutig keine Autos mehr in das Tor fahren können, haben wir keine Einfahrt eingetragen.

**Daten eintragen**

`TODO Erklärung Vorgehen & Tagging ID`

## Zu 4: Gehwegübergänge
{: class="mt-5 mb-4" }

`TODO Kapitel; Referenz auf unsere Wiki-Seite; Beispeiel?; Erklären wie man es mappt.`

## Zu 5: Fahrradständer auf dem Parkstreifen
{: class="mt-5 mb-4" }

`TODO Kapitel; Referenz auf unsere Wiki-Seite; Beispeiel?; Erklären wie man es mappt.`

## Straßenfotos "Mapillary"
{: class="mt-5 mb-4" }

Ein großes Hilfsmittel bei einem Projekt wie diesem sind gute Straßenfotos. Google Maps-Daten und Google Streetview-Daten dürfen in OSM unter keinem Umständen verwendet werden – das ist ein Lizenz-Thema. Aber wir können können unser eigenes, aktuelle Streetview machen – das heißt ["Mapillary"](https://www.mapillary.com/).

Das sieht dann zum Beipsiel so aus:
![](https://tordans.github.io/flyingsparks-blog/images-for--openstreetmap-org-user-tordans-diary/2020-12-fahrradstativ/experiment-vor-dem-gesicht-result-1640px.jpeg){: class='img-fluid img-thumbnail' }

Solche Fotos haben viele Vorteile – zum beispiel:
- Man kann zu Hause Details mappen, präzisieren oder kontrollieren
- Eine Person kann die Fotos machen, jemand anderes übernimmt das Mappen

Mapillary hat einen eigene ["How to start Photomapping"-Artikel](https://blog.mapillary.com/update/2016/08/26/how-to-start-photo-mapping-mapillary-101.html), der eine gute Einführung gibt.

Wer ein besonder ausgefeiltes Foto-Erfassungs-Setup sehen möchte, kann [meinen Blogpost zu meinem selbstgebauten Fahrradstativ anschauen](https://www.openstreetmap.org/user/tordans/diary/395215). Darin findest du Links zu den Fotos, die ich für Neukölln gemacht habe.

## Fragen?
{: class="mt-5 mb-4" }

[Bitte melde dich, wenn du mehr erfahren möchtest](../contact).

## Fußnoten
{: class="mt-5 mb-4" }
