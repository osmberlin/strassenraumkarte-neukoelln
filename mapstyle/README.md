# Straßenraumkarte – MapStyle

Die [Straßenraumkarte](https://strassenraumkarte.osm-berlin.org/?map=micromap) ist ein Kartenstil mit besonderem Fokus auf die räumliche Aufteilung des Stadt- und Straßenraums, insbesondere der Fahrbahnen und Objekte im öffentlichen Raum oder der urbanen Landnutzung. Sie wurde als Kartengrundlage für OpenStreetMap-Projekte in Berlin-Neukölln entwickelt, kann mit etwas Aufwand inzwischen aber auch an anderen Orten erzeugt werden.

Der Reiz des Kartenstils, der ästhetisch an Architektur-Pläne angeleht ist, besteht in der detaillierten Darstellung städtischer Umgebungen. Im Fokus stehen z.B. Fahrbahnflächen, Stadtmöbel, Gebäude, Landnutzungsdetails oder parkenden Autos im Straßenraum. Sollen diese Dinge an einem Ort dargestellt werden, ist es in den meisten Fällen zunächst notwendig, diese in OpenStreetMap zu erfassen, was ein aufwendiger Prozess sein kann (mehr dazu siehe unten).

Der Kartenstil besteht aus einem QGIS-Projekt und einem Pre-Processing-Script für Python in QGIS. Die Kartendaten können einfach über Overpass-Abfragen als geojson erzeugt und hinterlegt werden. Die Prozessierung der Kartendaten ist auf Experimente und Details ausgelegt, nicht auf die Erzeugung großflächiger Karten. Ziel des Kartenstils ist also zunächst, Kartendarstellungen für einzelne Stadtgebiete von höchstens einigen Quadratkilometern Größe zu ermöglichen, nicht für ganze Länder oder die Welt. Dafür ist die Technologie der Karte nicht ausgelegt und zu laienhaft aufgebaut.

### Weitergehende Informationen zur Karte (jeweils in deutscher Sprache):
* Beitrag in den Kartographischen Nachrichten / Info und Praxis 3/2022: ["Die Neuköllner Straßenraumkarte – Ein detaillierter Plan des öffentlichen Raumes auf Basis freier OpenStreetMap-Geodaten"](https://static-content.springer.com/esm/art%3A10.1007%2Fs42489-022-00119-1/MediaObjects/42489_2022_119_MOESM1_ESM.pdf) (ab Seite 5 / A-10)
* Lightning Talk auf der FOSSGIS-Konferenz 2022 (5 Minuten): ["Die Neuköllner Straßenraumkarte – ein hochaufgelöster OSM-Mikro-Mapping-Kartenstil"](https://media.ccc.de/v/fossgis2022-14180-die-neukllner-straenraumkarte-ein-hochaufgelster-osm-mikro-mapping-kartenstil
)

![grafik](https://github.com/SupaplexOSM/strassenraumkarte-neukoelln/blob/main/images/sample_image.jpg)

--------------------

## Wie kann ich die Straßenraumkarte für meine Stadt generieren?

Das ist leider nicht so einfach, denn eine optimale Kartendarstellung der Straßenraumkarte erfordert ein hohes Maß an Micromapping in OSM und eine kartographische Datengrundlage, die nur an wenigen Orten bereits vorhanden ist (insbesondere Fahrbahnflächen und straßenbegleitendes Parken). Darüber hinaus bezieht die Neuköllner Straßenraumkarte manuell nachbearbeitete Daten zum Parken im Straßenraum ein – auch das kannst du in deiner Stadt machen, aber es ist wahrscheinlich aufwendig. Natürlich kann die Straßenraumkarte auch dort gerendert werden, wo diese Daten nicht vorhanden sind, aber sie sieht dann weniger ansprechend aus. Zu den wichtigsten Daten für ein optimales Rendering der Straßenraumkarte gehören:
* Fahrbahnflächen (-> [area:highway](https://wiki.openstreetmap.org/wiki/Proposal:Area_highway/mapping_guidelines))
* Parkstreifen (-> [Street Parking](https://wiki.openstreetmap.org/wiki/Street_parking))
* Gehwegnetze (-> [Mapping-Guide für Berlin](https://wiki.openstreetmap.org/wiki/Berlin/Verkehrswende/Gehwege))
* Gebäude
* Landnutzungsflächen (auch kleinräumige, z.B. Grasflächen und Gebüsche)
* Bäume

Darüber hinaus enthält das Post-Prozessing der OSM-Daten eine aufwendige Generierung von Straßenmarkierungen, die auf einer detaillierten Erfassung von Fahrspurattributen basiert (z.B. lanes, turn:lanes, lane_markings, width, width:lanes, placement, cycleway:*). Sind diese Fahrspurattribute nicht ausreichend oder ungenau erfasst, werden die Straßenmarkierungen unsauber generiert – oder sollten dann besser ganz deaktiviert werden.

Viele weitere Dinge werden in der Kartendarstellung dargestellt, z.B. Straßenmöbel wie Schaltkästen oder Straßenlaternen, Barrieren wie Zäune und Tore oder auch überhängende Gebäudeteile, wenn diese als building:parts definiert sind. Letztendlich ist die Straßenraumkarte ein Kartenstil für lagegenaues urbanes Micromapping, um die Fülle der Dinge im Raum und ihrer Eigenschaften möglichst weitreichend sichtbar zu machen.

--------------------

## Schritt für Schritt-Anleitung zur eigenen Straßenraumkarte

_Versionshinweis: Die aktuelle Version der Straßenraumkarte wurde mit QGIS 3.22.4-Białowieża erzeugt. Mit älteren oder neueren Versionen könnte es evtl. zu Fehlern bei der Scriptausführung oder Kartendarstellung kommen._

__0.) OSM-Micromapping in der Umgebung__, siehe oben :)

__1.) Daten für das gewünschte Gebiet herunterladen.__ Das funktioniert zur Zeit etwas umständlich über etwa 20 verschiedene Overpass-Turbo-Abfragen für verschiedene Layer, z.B. Gebäude, Straßen, Straßenflächen oder Landnutzung. Jede Abfrage enthält zu Beginn eine Bounding Box, die an das Zielgebiet angepasst werden kann (für Berlin-Neukölln ist diese Bounding Box voreingestellt als [bbox:52.4543246009110788,13.3924347464750326,52.5009195009107046,13.4859782]). Die Abfragen ausführen und die Daten unter "layer/geojson/" als GeoJSON mit dem passenden Dateinamen abspeichern:

[amenity.geojson](https://overpass-turbo.eu/s/1CCd) | [area_highway.geojson](http://overpass-turbo.eu/s/1erF) | [barriers.geojson](http://overpass-turbo.eu/s/1cZw) | [bridge.geojson](http://overpass-turbo.eu/s/1cTT) | [building_part.geojson](http://overpass-turbo.eu/s/1cZv)
[buildings.geojson](http://overpass-turbo.eu/s/1cZx) | [entrance.geojson](http://overpass-turbo.eu/s/1cTV) | [highway.geojson](http://overpass-turbo.eu/s/1cLL) | [housenumber.geojson](http://overpass-turbo.eu/s/1cTN) | [landuse.geojson](http://overpass-turbo.eu/s/1cTF) | [leisure.geojson](http://overpass-turbo.eu/s/1cTL) | [man_made.geojson](https://overpass-turbo.eu/s/1qyx) | [motorway.geojson](http://overpass-turbo.eu/s/1cTO) | [natural.geojson](http://overpass-turbo.eu/s/1cTD) | [path.geojson](http://overpass-turbo.eu/s/1eG0) | [place.geojson](http://overpass-turbo.eu/s/1cTR) | [playground.geojson](https://overpass-turbo.eu/s/1iMm) | [railway.geojson](https://overpass-turbo.eu/s/1izr) | [routes.geojson](http://overpass-turbo.eu/s/1eG1) | [waterway.geojson](http://overpass-turbo.eu/s/1cTP)

__2.) QGIS installieren/starten__ und die Python-Konsole öffnen ("Erweiterungen > Python-Konsole").

__3.) Wenn gewünscht, Parkraumdaten generieren__ und manuell nachbearbeiten. Dafür müssen Parkraumdaten in OSM in möglichst hohem Detailgrad erfasst sein – Infos dazu gibt es im [OSM-Wiki](https://wiki.openstreetmap.org/wiki/DE:Street_parking) sowie beim [OSM-Parkraumprojekt](https://parkraum.osm-verkehrswende.org/participate/). Mit diesem Script lassen sich passende Parkraumdaten generieren: [street_parking.py](https://github.com/SupaplexOSM/street_parking.py) (Infos zu benötigten Daten und zur Ausführung sind dort zu finden). Ergebnis unter "layer/geojson/parking/street_parking_lines.geojson" speichern.
Die generierten Parkraumdaten sind jedoch noch nicht sehr lagegenau. Es lohnt sich, diese in QGIS manuell nachzubearbeiten, Fehler zu bereinigen und insbesondere an realen Bordsteinkanten auszurichten (z.B. durch Snapping oder manuelles verschieben/einrasten).

__4.) Ortsspezifische Layer anpassen.__ Der Kartenstil enthält einzelne Layer, deren Ausdehnung/Beschaffenheit auf die Verwendung im ursprünglichen Kartengebiet Berlin/Ortsteil Neukölln ausgerichtet sind. Diese können bei Bedarf an das eigene Gebiet angepasst werden, sind aber ansonsten auch verzichtbar. Dazu gehören die Layer:
* "map_extent" (unter "layer/geojson/map_extent/map_extent.geojson"): Kann später benutzt werden, um das Gebiet zu definieren, in dem Kartenkacheln erzeugt werden sollen.
* "map_fog_square" ("layer/geojson/fog/map_fog_square.geojson"): Ein Rahmen um das Kartengebiet in der Hintergrundfarbe, um dahinterliegende Gebiete zu verdecken.
* "kerb_street_areas" und "kerbs (ways, from street_areas)" ("layer/geojson/kerb/kerb_street_areas.geojson"): Ein externer Datensatz mit Straßenflächen, z.B. aus ALKIS. Kann ergänzend zu area:highway-Flächen aus OSM zur Darstellung der Fahrbahnflächen herangezogen werden.

__5.) Das Post-Prozessing-Script ("post_processing.py") in QGIS öffnen und ausführen.__ Das Post-Prozessing-Script enthält eine ganze Reihe von Schritten, die die Kartendarstellung verbessern, z.B. Geometrieanpassungen und vor allem die Erzeugung von Layern für spezielle Darstellungen. Den größten Teil des Scripts macht die Generierung der Fahrbahnmarkierungen aus. Je nach Größe des Gebiets und verfürbarer Rechenleistung kann die Durchführung aller Schritte einige Zeit dauern. Die einzelnen Prozessierungs-Schritte können einzeln (de)aktiviert werden (durch setzen von 0 oder 1 gleich zu Beginn des Scripts) und lassen sich so auch in kleineren "Päckchen" oder einzeln ausführen, falls es z.B. zu Speicher- oder Darstellungsproblemen bei der Generierung kommt. Bei Bedarf können so auch nicht benötigte Prozessierungsschritte ausgelassen werden, z.B. wenn keine Parkraumdaten vorliegen (siehe Schritt 3). Vor Scriptausführung nochmal das Koordinatenbezugssystem prüfen (siehe nächster Schritt).

__6.) Koordinatenbezugssystem prüfen.__ Die Straßenraumkarte nutzt für viele Layer und geometrische Operationen metrische Koordinatenbezugssysteme, um die Dinge im Raum (zenti)metergenau darstellen zu können. Die Vorsteinstellung des Kartenstils geht davon aus, dass sich das dargestellte Gebiet in der UTM-Zone 32 befindet, was z.B. für Städte in Deutschland ganz gut passen sollte (auch wenn sich einige Städte in der Nachbarzone befinden).
Falls das Zielgebiet in einer anderen Weltregion liegt, muss ein passendes Bezugssystem gewählt werden. In diesem Fall muss bei der Ausführung des Post-Prozessing-Scripts (Schritt 5) nicht nur die Scriptzeile 'crs_to = "EPSG:25833"' vor Scriptausführung angepasst werden, sondern im nächsten Schritt müssen ggf. auch die Bezugssysteme aller Kartenlayer, die in EPSG:25833 vorliegen, angepasst werden.
Liegt das Zielgebiet auf einem signifkant anderen Breitengrad als Berlin (52° N), muss später außerdem noch ein Skalierungsfaktor angepasst werden, da die metrischen Darstellungen sonst verzerrt dargestellt werden (die Karte selbst liegt in WGS 84 / Pseudo-Mercator (EPSG:3857) vor, um das Rendern von MapTiles zu ermöglichen). Die Formel für diesen Skalierungsfaktor ist: 1 / cos(Breitengrad), für Berlin z.B. 1 / cos(52°) = 1.62. Weicht dieser Faktor in deinem Zielgebiet signifikant davon ab (z.B. um mehr als 0.1), passe den Faktor im nächsten Schritt in QGIS an: "Projekt > Eigenschaften > Variablen > "scale_factor = '1.62'"

__7.) Den Kartenstil in QGIS öffnen__ ("strassenraumkarte.qgz"). Wenn alles gut gegangen ist, werden alle Layer geladen und dargestellt. Ggf. den Breitengrad-abhängigen Skalierungsfaktor anpassen (siehe Schritt 6). Die Karte kann nun exportiert oder MapTiles daraus generiert werden. Tipp zur Generierung von Tiles in QGIS: Der native Renderer gibt möglicherweise die Farben der Straßenraumkarte nicht korrekt wieder. Es gibt zwei gute QGIS-Erweiterungen zur Generierung von Kartelkacheln: "QTiles" und "QMetaTiles". "QMetaTiles" hat den Vorteil, dass es MetaTiling beherrscht, was die Darstellung von Symbolen und Labeln an Kachelgrenzen erheblich verbessert. Diese Erweiterung scheint jedoch nicht mit Variablen zurechtzukommen, sodass der Skalierungsfaktor nicht berücksichtigt wird und Symbole sowie Taxturen nicht geladen werden. Mein Workaround: Das QGIS-Projekt als *.qgs-Datei speichern (xml), in einem Editor öffnen und die Variablen "@scale_factor" sowie "@project_folder" durch den Skalierungsfaktor sowie einen absoluten Dateipfad ersetzen.
