kfz_points.geojson
^^^^^^^^^^^^^^^^^^
Beschreibung: Punktwolke zugelassener Kraftfahrzeuge (interpoliert)
Bezugsraum: Berliner Ortsteil Neukölln und Puffer von 500m außerhalb der Ortsteilgrenze
Quelle: Berechnet auf Grundlage von © Amt für Statistik Berlin-Brandenburg, Potsdam, 2020 (siehe unten)
-----------------------+-----------------------------------------------------------------------------------------
id			Eindeutige Referenznummer
Bezirk			Bezirk, in dem sich der Punkt befindet
Planungsraum		LOR-Planungsraum, in dem sich der Punkt befindet
-----------------------+-----------------------------------------------------------------------------------------

kfz_lor_planungsraum.geojson
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Beschreibung: LOR-Planungsräume (Polygone) mit Quote zugelassener Kfz und Pkw
Bezugsraum: Berlin
Quelle: nach © Amt für Statistik Berlin-Brandenburg, Potsdam, 2020: „Melderechtlich registrierte Einwohnerinnen
und Einwohner am Ort der Hauptwohnung in Berlin am 30.06.2020 nach Planungsräumen und KfZ-Bestand“ –
Vervielfältigung und Verbreitung, auch auszugsweise, mit Quellenangabe gestattet
-----------------------+-----------------------------------------------------------------------------------------
Schlüssel		Schlüsselnummer des LOR-Planungsraums
Bezirk			Bezirk, dem der Planungsraum zugehört
Planungsraum		Name des Planungsraums
Bezirksregion		LOR-Bezirksregion, der der Planungsraum zugehört
Prognoseraum		LOR-Prognoseraum, dem der Planungsraum zugehört
Flächengröße in m²	Fläche des Planungsraums
Einwohner insgesamt	Bevölkerungszahl im Planungsraum
darunter 18 Jahre und älter	Anzahl volljähriger Einwohnerinnen und Einwohner
Kraftfahrzeuge insgesamt	Anzahl zugelassener Kfz im Planungsraum
darunter Pkw		Anzahl zugelassener Pkw im Planungsraum
Kfz pro 1000 EW		Kfz-Quote im Planungsraum (abgerundet, so aus Originalquelle übernommen)
Pkw pro 1000 EW		Pkw-Quote im Planungsraum (abgerundet, so aus Originalquelle übernommen)
-----------------------+-----------------------------------------------------------------------------------------
