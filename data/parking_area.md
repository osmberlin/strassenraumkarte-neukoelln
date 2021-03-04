# parking_area.geojson

* Beschreibung: Stellplatzflächen (Polygone) abseits des Straßenraums
* Bezugsraum: Berliner Ortsteil Neukölln und Puffer von 500m außerhalb der Ortsteilgrenze
* Quelle: © OpenStreetMap und Mitwirkende, OpenData gemäß ODbL, eigene Ergänzungen

|id | Eindeutige Referenznummer|
|---|---|
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
