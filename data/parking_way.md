# parking_way.geojson

* Beschreibung: Parkstreifen (Linien) im Straßenraum/am Straßenrand
* Bezugsraum: Berliner Ortsteil Neukölln und Puffer von 500m außerhalb der Ortsteilgrenze
* Quelle: © OpenStreetMap und Mitwirkende, OpenData gemäß ODbL

|id | Eindeutige Referenznummer|
|---|---|
|osm_id | OSM-Objektreferenz|
|parking | Parkstreifentyp (entsprechend des OSM-“parking“-Keys:<br>„lane“: Fahrbahn,<br>„street_side“: Parkbucht.|
|orientation | Parkeinschränkungen|
|position | Position geparkter Fahrzeuge|
|capacity | Stellplatzanzahl|
|condition | Zugangsbeschränkungen|
|condition:other | Temporär abweichende Zugangsbeschränkungen|
|condition:other:time | Zeitraum temporär abweichender Zugangsbeschränkungen|
|maxstay | Höchstparkdauer|
|highway | Straßentyp|
|highway:name | Straßenname|
|oneway_direction | „true“, wenn Ausrichtung geparkter Fahrzeuge durch Einbahnstraße invertiert|
|osm-location | Ursprung der Parkstreifeninformation in der OSM-Datenbank:<br>„left“ / „right“ für linke bzw. rechte Seite des Straßenlinienobjekts,<br>„separate“ für separat erfasste Objekte (insbesondere Parkbuchten).|
|source:capacity | Quelle der Stellplatzanzahl:<br>„estimated“: Aus Geometrie interpoliert,<br>„OSM“: Aus OSM übernommen.|
|length | Länge des Parkstreifensegments in Metern|
