# kfz_lor_planungsraum.geojson

* Beschreibung: LOR-Planungsräume (Polygone) mit Quote zugelassener Kfz und Pkw
* Bezugsraum: Berlin
* Quelle: nach © Amt für Statistik Berlin-Brandenburg, Potsdam, 2020: „Melderechtlich registrierte Einwohnerinnen
  und Einwohner am Ort der Hauptwohnung in Berlin am 30.06.2020 nach Planungsräumen und KfZ-Bestand“ –
  Vervielfältigung und Verbreitung, auch auszugsweise, mit Quellenangabe gestattet

|Attribut | Erläuterung |
|---|---|
|Schlüssel | Schlüsselnummer des LOR-Planungsraums |
|Bezirk | Bezirk, dem der Planungsraum zugehört
|Planungsraum | Name des Planungsraums|
|Bezirksregion | LOR-Bezirksregion, der der Planungsraum zugehört|
|Prognoseraum | LOR-Prognoseraum, dem der Planungsraum zugehört|
|Flächengröße in m² | Fläche des Planungsraums|
|Einwohner insgesamt | Bevölkerungszahl im Planungsraum|
|darunter 18 Jahre und älter | Anzahl volljähriger Einwohnerinnen und Einwohner|
|Kraftfahrzeuge insgesamt | Anzahl zugelassener Kfz im Planungsraum|
|darunter Pkw | Anzahl zugelassener Pkw im Planungsraum|
|Kfz pro 1000 EW | Kfz-Quote im Planungsraum (abgerundet, so aus Originalquelle übernommen)|
|Pkw pro 1000 EW | Pkw-Quote im Planungsraum (abgerundet, so aus Originalquelle übernommen)|

# kfz_points.geojson

* Beschreibung: Punktwolke zugelassener Kraftfahrzeuge (interpoliert)
* Bezugsraum: Berliner Ortsteil Neukölln und Puffer von 500m außerhalb der Ortsteilgrenze
* Quelle: Berechnet auf Grundlage von © Amt für Statistik Berlin-Brandenburg, Potsdam, 2020 (siehe unten)

|Attribut | Erläuterung |
|--|--|
|id | Eindeutige Referenznummer|
|Bezirk | Bezirk, in dem sich der Punkt befindet|
|Planungsraum | LOR-Planungsraum, in dem sich der Punkt befindet|

# parking_area.geojson

* Beschreibung: Stellplatzflächen (Polygone) abseits des Straßenraums
* Bezugsraum: Berliner Ortsteil Neukölln und Puffer von 500m außerhalb der Ortsteilgrenze
* Quelle: © OpenStreetMap und Mitwirkende, OpenData gemäß ODbL, eigene Ergänzungen

|Attribut | Erläuterung |
|---|---|
|id | Eindeutige Referenznummer|
|osm_id | OSM-Objektreferenz (fehlt bei Tiefgaragen, die aus anderer Datenquelle übernommen wurden)|
|parking | Stellplatztyp (entsprechend des OSM-„parking“-Keys, außer dem Wert „level“ für Parkdecks in Gebäuden, für die es keine etablierte Entsprechung im OSM-Schema gibt)|
|capacity | Stellplatzanzahl|
|access | Zugangsbeschränkung (entsprechend des OSM-„access“-Keys)|
|building | Spezifikation, wenn Stellplatzobjekt ein Gebäude oder Gebäudeteil ist|
|status | „disused“ für ungenutzte/leerstehende Objekte|
|fee | „yes“ für gebührenpflichtige Objekte|
|maxstay | Höchstparkdauer|
|parking:level | Anzahl Stockwerke bei mehrstöckigen Stellplatzobjekten|
|area | Flächeninhalt (Grundfläche der Objektgeometrie) in Quadratmetern|
|area:levels | Geschossflächenzahl (Grundfläche * Anzahl Stockwerke) in Quadratmetern|
|source | Quelle der Geometrie:<br>- „OSM“: Aus OSM übernommen,<br>- „ALKIS“: Aus ALKIS übernommen,<br>- „document“: Aus einem Dokument (z.B. Planwerk) übernommen,<br>- „estimated“: Auf Grundlage baulicher Merkmale geschätzt,<br>- survey: Vor-Ort-Beobachtung.|
|source:capacity | Quelle der Stellplatzanzahl:<br>- „aerial imagery“: Gezählt auf Luftbild,<br>- „document“: Angabe aus Planwerk o.ä.,<br>- „estimated“: Aus Geometrie interpoliert,<br>- „OSM“: Aus OSM übernommen,<br>- „request“: Anfrage bei Eigentümer/(Ver-)Mieter,<br>- „survey“: Vor-Ort-Beobachtung,<br>- „syntax“: Aus Attribut abgeleitet („parking=garage“ entspricht einem Stellplatz).|

# parking_way.geojson

* Beschreibung: Parkstreifen (Linien) im Straßenraum/am Straßenrand
* Bezugsraum: Berliner Ortsteil Neukölln und Puffer von 500m außerhalb der Ortsteilgrenze
* Quelle: © OpenStreetMap und Mitwirkende, OpenData gemäß ODbL

|Attribut | Erläuterung |
|---|---|
|id | Eindeutige Referenznummer|
|osm_id | OSM-Objektreferenz|
|parking | Parkstreifentyp (entsprechend des OSM-“parking“-Keys:<br>„lane“: Fahrbahn,<br>„street_side“: Parkbucht.|
|orientation | Parkausrichtung („parallel“, „diagonal“, „perpendicular“)|
|position | Position geparkter Fahrzeuge („on_street“, „on_kerb“, „half_on_kerb“, „shoulder“ (= Seitenstreifen), „street_side“ (= Parkbucht))|
|capacity | Stellplatzanzahl|
|condition | Zugangsbeschränkungen|
|condition:other | Temporär abweichende Zugangsbeschränkungen|
|condition:other:time | Zeitraum temporär abweichender Zugangsbeschränkungen|
|maxstay | Höchstparkdauer|
|highway | Straßenkategorie|
|highway:name | Straßenname|
|oneway_direction | „true“, wenn Ausrichtung geparkter Fahrzeuge durch Einbahnstraße invertiert|
|osm-location | Ursprung der Parkstreifeninformation in der OSM-Datenbank:<br>„left“ / „right“ für linke bzw. rechte Seite des Straßenlinienobjekts,<br>„separate“ für separat erfasste Objekte (insbesondere Parkbuchten).|
|source:capacity | Quelle der Stellplatzanzahl:<br>„estimated“: Aus Geometrie interpoliert,<br>„OSM“: Aus OSM übernommen.|
|length | Länge des Parkstreifensegments in Metern|
