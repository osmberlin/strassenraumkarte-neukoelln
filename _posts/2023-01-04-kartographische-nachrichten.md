---
title: Beitrag über die Neuköllner Straßenraumkarte in den Kartographischen Nachrichten
menu_title: Kartographischen Nachrichten
date: 2023-01-05 12:00:00 +0100
author: Alex Seidel @SupaplexOSM
layout: post
description: Beitrag über die Neuköllner Straßenraumkarte in den Kartographischen Nachrichten / KN – Info und Praxis 3(2022) 72, S. A-10 bis A-17.
---

<div class="notice mb-7">

An dieser Stelle dokumentieren wir einen Beitrag über die Neuköllner Straßenraumkarte in der kartographischen Fachzeitschrift [„KN – Journal of Cartography and Geographic Information“ – Info und Praxis 3 (2022) 72 (PDF, OpenAccess)](https://static-content.springer.com/esm/art%3A10.1007%2Fs42489-022-00119-1/MediaObjects/42489_2022_119_MOESM1_ESM.pdf).

</div>

# Die Neuköllner Straßenraumkarte

## Ein detaillierter Plan des öffentlichen Raumes auf Basis freier OpenStreetMap-Geodaten

_Alex Seidel_[^1]

## Zusammenfassung

Die Neuköllner Straßenraumkarte ist ein freier Online-Stadtplan für den Berliner Ortsteil Neukölln, der Details des öffentlichen Raumes wie Fahrbahnen, parkende Fahrzeuge oder Grünflächen in großem Maßstab darstellt. Die Karte dient als Grundlage für die Visualisierung örtlicher thematischer Karten (derzeit primär einer Parkraumanalyse) und wird von Akteuren der lokalen Zivilgesellschaft und Verwaltung in Stadt- und Verkehrsplanungsprozessen genutzt. Als Datengrundlage dienen OpenStreetMap-Daten, die vor Ort durch eine aktive lokale Community in hoher Präzision erfasst und für die Kartendarstellung teilautomatisiert mit QGIS aufbereitet werden. Die an Architekturpläne erinnernde ästhetische Gestaltung und der Fokus der Karte auf Details des öffentlichen Raumes heben sich von anderen Kartenwerken insbesondere aus dem OpenStreetMap-Umfeld ab, wobei die Karte bestehende Konventionen in Frage stellt und neue Möglichkeiten aufzeigt.

## Schlüsselwörter

OpenStreetMap, VGI, Stadtplan, Fahrbahn, Parkraum, Öffentlicher Raum

## 1. Einleitung

Möchte man sich ein Bild von einer Straßensituation machen – sei es, weil man sich dort mit einem Stadt- oder Verkehrsplanungsprojekt befasst oder einfach nur den Weg zu einem Treffpunkt mit Freunden sucht – liegt ein Blick auf eine Karte nahe. Im Online-Zeitalter sind digitale Stadtpläne zu einem alltäglichen Hilfsmittel geworden, die uns einen Eindruck vom Raum vermitteln und uns durch ihn hindurchleiten. Im Gegensatz zu traditionellen „analogen“ Stadtplänen erlauben sie eine freie Maßstabswahl, bieten Möglichkeiten der Interaktion und warten meist mit einem (un-)übersichtlichen Angebot an mehr oder weniger aktuellen Points of Interests auf.

Doch wer sich für die Details eines Raumes interessiert, und nicht nur für den schnellsten Weg zum nächsten Restaurant, stößt schnell an die Grenzen moderner Kartenwerke. Diejenigen, die sich professionell mit der gesuchten Straßensituation befassen, sind vielleicht noch in der Lage, einen Blick in ALKIS zu werfen oder einen unübersichtlichen Vermessungsplan einzusehen. Man kann auch zu einem Luftbild greifen, aber häufig bilden diese die Details, für die man sich interessiert, schlicht nicht ab. Und selbst wer nur nach dem Treffpunkt mit den Freunden schaut, muss dann vor Ort noch weiter suchen. Oft hilft also nur ein Blick auf die Realität vor Ort.

Der Bedarf nach detaillierten räumlichen Repräsentationen ist also groß, erst recht, da Stadtplanungsprozesse immer partizipativer werden und sich allerorts zunehmend auch zivilgesellschaftliche Akteure an der Gestaltung und „Reproduktion“ des Raumes beteiligen. Die Bedeutung grafischer Darstellungen von (Planungs-)Ideen ist hoch, um im öffentlichen Diskurs angemessene Wahrnehmung zu finden.

Die Neuköllner Straßenraumkarte[^2] ist ein Versuch, eine solche detaillierte Kartengrundlage des öffentlichen Raumes anzubieten (siehe Abb. 1). Sie ist ein auf OpenStreetMap-Daten (OSM) basierender Stadtplan in großem Maßstab für den Berliner Ortsteil Neukölln, der den öffentlichen Raum mit seinen Fahrbahnen, Gehwegen und parkenden Fahrzeugen in den Fokus nimmt, aber auch detaillierte Landnutzungen sowie die Straßenmöbel im urbanen Raum – vom Straßenbaum und der Straßenlaterne über Sitzbänke und Fahrradständer bis hin zum Schaltkasten oder Schutzpoller darstellt.

{% include image.html
src="images/posts/kartographische-nachrichten/Abbildung01.jpg"
caption="Abb. 1: Ausschnitt der Neuköllner Straßenraumkarte mit Fahrbahnen, parkenden Fahrzeugen, Gebäuden und Landnutzungsdetails. © Kartendaten: OpenStreetMap-Beitragende."
%}

## 2. Der Entstehungshintergrund: Von der Parkraum- zur Straßenraumkarte

Die Straßenraumkarte entstand zunächst als Kartengrundlage für die Darstellung der Ergebnisse einer Parkraumanalyse für den Stadtteil Neukölln. Im Rahmen dieser Analyse wurde eine geodatenbasierte Methode zur Zählung von parkenden Fahrzeugen im Straßenraum demonstriert, die vom Autoren dieses Artikels mit Unterstützung weiterer Mitglieder der Berliner OpenStreetMap-Community auf OSM-Basis durchgeführt und im Frühjahr 2021 veröffentlicht wurde.[^3] Ein Ergebnis der Analyse war ein Datensatz mit etwa 30.000 einzelnen Kfz-Stellplätzen im Straßenraum, die kartographisch dargestellt werden sollten. Dafür war ein Datensatz mit Fahrbahnbegrenzungslinien bzw. Fahrbahn-Polygonen notwendig.

Als Open Data frei verfügbare Geodaten zu Fahrbahnbegrenzungen (in einer Stadt wie Berlin üblicherweise durch Bordsteine definiert) boten sich an:

- das Amtliche Liegenschaftskatasterinformationssystem (ALKIS), das Bordsteinkanten in hoher räumlicher Präzision enthält, die allerdings seit der ALK-Umstellung nicht mehr systematisch gepflegt werden und daher zunehmend veralten,

- Daten einer vermessungstechnischen Straßenbefahrung aus dem Jahr 2014, die allerdings zum Teil mit einem Versatz von mehreren Dezimetern vorliegen und ebenso bereits mehrere Jahre alt sind,

- OpenStreetMap-Daten, in denen Bordsteinkanten jedoch nur selektiv und in uneinheitlicher Genauigkeit erfasst sind.

{% include image.html
src="images/posts/kartographische-nachrichten/Abbildung02.jpg"
caption="Abb. 2: Fahrbahn- und Parkstreifendarstellung in der Neuköllner Straßenraumkarte. © Kartendaten: ALKIS, OpenStreetMap-Beitragende."
%}

Für die Darstellung herangezogen wurde schließlich ein Fahrbahndatensatz auf Basis von ALKIS-Daten, die im Bereich baulicher Veränderungen mit OSM-Daten angereichert und somit kontinuierlich „aktualisiert“ werden. In einer Stadt wie Berlin, in der es – gerade in Zeiten der Verkehrswende – permanent bauliche Veränderungen gibt, ist Aktualität ein wichtiger Faktor. Die Parkplatzdaten der Parkraumanalyse wurden durch Snapping (automatisierte Überlagerung mit den Bordsteinkanten) und manuelle Nachkorrektur an diese Fahrbahndaten angepasst und bilden seitdem gemeinsam mit den Fahrbahnflächen den Kern der Straßenraumkarte (siehe Abb. 2). Andere in OSM erfasste Daten wie Zufahrten, Straßenbäume, Gebäude, Landnutzungen oder Barrieren wie Zäune und Mauern wurden in die Darstellung integriert.

Das Ergebnis der Parkraumanalyse und ihre kartographische Darstellung stießen auf großes Interesse, sowohl in Teilen der OSM-Community als auch der lokalen Zivilgesellschaft und Stadtplanung. Initiativen nutzen die Karte beispielsweise zur Visualisierung ihrer Planungsideen und Verwaltungsakteure werfen bisweilen einen Blick darauf. Daher wurde die Straßenraumkarte als separates Projekt weiterentwickelt. Mit der Zeit wurden weitere Elemente in der Darstellung ergänzt, wie Straßenmöbel (für deren Erfassung in OSM die Straßenraumkarte eine große Motivation darstellt, siehe letzter Abschnitt) oder Fahrbahnmarkierungen (was eine aufwendige Daten-Prozessierung erfordert, siehe Abschnitt 5).

## 3. Die Datengrundlage: Micro-Mapping in OpenStreetMap

Als ein paar Enthusiasten um das Jahr 2006 begannen, freie Geodaten im OpenStreetMap-Projekt zu sammeln, ahnte wohl noch niemand, dass das digitale Kartenwerk schon wenige Jahre später in einigen Regionen der Erde an die Grenzen kartierbarer physischer Raummerkmale stoßen würde. Der Datenbestand ist in den letzten Jahren sowohl quantitativ als auch qualitativ stark gewachsen. Während es – wie der Name des Projekts noch immer verrät – anfangs vor allem um die Erstellung einer frei verfügbaren Straßenkarte ging, haben sich die Schwerpunkte für viele Beitragende mit der Zeit verschoben. Die OSM-Datenbank vereinigt inzwischen – je nach Interessen der Beitragenden – verschiedenste „Welten“: Von den klassischen Straßen- und Adressinformationen und Points of Interest (z. B. Ladenstandorten und ihren Öffnungszeiten) über Eisenbahnstrecken, ÖPNV-Linien und den Details zugehöriger Infrastrukturen oder 3D-Gebäudeinformationen bis hin zu Obstbaumkarten von Kleingartenvereinen.

In Ländern wie Deutschland, in denen es seit Beginn an eine enthusiastische und große OSM-Community gibt, lässt sich zunehmend beobachten, dass der Datenbestand eine gewisse „Vollständigkeit“ wesentlicher physisch-räumlicher Merkmale annimmt und sich die Aktivitäten daher zunehmend in Richtung von Detailerfassungen verschieben. Fehlten vor zehn Jahren in Deutschland vereinzelt noch ganze Straßen und Dörfer in OSM, ist es inzwischen schwer geworden, noch fehlende Gebäudegeometrien zu finden. Statt dem räumlichen Verlauf von Straßen rücken ihre Attribute wie Straßenbeleuchtung oder Spurattribute (Anzahl der Fahrspuren, Abbiegespuren, Richtungsanzeiger…) in den Fokus. Ist der Verlauf eines Radwegs einmal kartiert, folgen im nächsten Schritt wichtige Attribute wie seine Breite oder Oberflächenbeschaffenheit.

In einzelnen, vor allem urbanen Gegenden nimmt diese Detailerfassung des physischen öffentlichen Raumes in Form sogenannten „Micro-Mappings“ weitreichende Formen an. Landnutzungen wie Hecken-, Rasen- oder Parkplatzflächen werden dann durchaus dezimetergenau erfasst, genauso wie die Verläufe von Bordsteinkanten oder Standorte und Details von Straßenbäumen und Straßenmöbeln (von Laternen und Bänken über Schaltkästen bis hin zu einzelnen Blumenkübeln). Der Berliner Ortsteil Neukölln ist ein solches hoch detailliert kartiertes Gebiet. Die ehrenamtlichen OSM-Mapper profitieren in Berlin dabei von einem guten OpenData-Angebot wie jährlich neuen hochaufgelösten Luftbildaufnahmen oder den ALKIS-Daten, die bei der OSM-Kartierung als Referenz herangezogen werden dürfen. Ebenso hilfreich sind große Mengen aktueller Straßenfotos, die von Mitgliedern der OSM-Community auf entsprechenden Portalen verfügbar gemacht werden.

## 4. Das Design: Architekturpläne als ästhetisches Vorbild

Dieses Micro-Mapping bildet die Grundlage für die detaillierte Kartendarstellung der Straßenraumkarte. Aus einer strengen kartographischen Perspektive ist sie weniger eine Karte, als vielmehr ein Plan, da sie für große Maßstäbe ausgelegt ist und weitgehend auf Generalisierung verzichten kann. Sie versucht die Dimensionen des Straßenraums und der darin enthaltenen physischen Elemente wirklichkeitsgetreu darzustellen, womit sie sich von vielen anderen Kartenwerken unterscheidet, insbesondere den typischen OSM-basierten.

Auch ästhetisch schlägt die Straßenraumkarte einen anderen Weg ein. Die Verwendung von Schatten und Texturen, die ein eher realistisches Erscheinungsbild und räumliche Tiefe vermitteln, gehört eher selten zum kartographischen Werkzeugkasten. Eine Ausnahme, in denen solche Effekte zum Standard gehören, sind Plandarstellungen in der (Landschafts-)Architektur, die nicht selten schon fast an ein Luftbild erinnern. Die großen Maßstäbe und der weitgehende Verzicht auf Generalisierungen bieten dabei den Raum, die Darstellung der Elemente an ihre reale Erscheinungsform anzupassen.

Die Neuköllner Straßenraumkarte orientiert sich ästhetisch an solchen Architekturplänen. Zwar ist die Repräsentation von Gebäuden und Grundstücken (die einen großen Teil des Raumes einnehmen) noch eher monoton, da diese nicht im Fokus der Karte stehen und Informationen wie Dachformen und -farben oder räumliche Strukturen auf (privaten) Grundstücken fehlen. Die Darstellung des Straßenraums und öffentlicher Grünflächen greift aber gestalterische Ideen solcher Pläne auf (siehe Abb. 3). So sind Wiesen und Gebüsche texturiert statt einfarbig, am Rand von Wegen stehen kleine symbolische Bänke, die in Blickrichtung ausgerichtet sind. Die Fahrbahnränder werden im Bereich von Parkstreifen von kleinen Automodellen gesäumt, auf Spielplätzen sind die einzelnen Spielgeräte oder auf Sportplätzen Markierungslinien angedeutet. Bäume heben sich transparent, aber dezent räumlich geschummert und – falls in OSM kartiert – mit ihrem realen Kronendurchmesser von der Grundebene ab. Wälder erzeugen durch generisch erzeugte Symbole den Eindruck, als würden sie aus Einzelbäumen bestehen (siehe auch den nachfolgenden Abschnitt).

{% include image.html
src="images/posts/kartographische-nachrichten/Abbildung03.jpg"
caption="Abb. 3: An Architekturpläne angelehnte Darstellung, hier einer Grünanlage und eines Spielplatzes mit Landnutzungstexturen, Baumkronendurchmessern, Sportfeldmarkierungen und angedeuteten Spielgeräten. © Kartendaten: OpenStreetMap-Beitragende."
%}

Die gewählte Form der Darstellung – lage- und größengetreu, an der realen Erscheinung orientiert, ohne Generalisierung und Signaturen – kommt zudem mit einer sparsamen Verwendung von Beschriftungen aus: Lediglich Straßennamen sowie größere Parks und Gewässer sind in größeren Maßstäben der digitalen Karte zur leichteren Orientierung dezent beschriftet. Je nach Maßstab ergibt sich der Eindruck eines „Vogelflugs“ über den Stadtteil oder eines Spaziergangs entlang der Straße. Diese Darstellungsform macht die öffentliche Raumstruktur direkt sichtbar und kann somit auch hilfreich sein, planerische Erfordernisse wie ungünstige Raumaufteilungen oder fehlende Infrastrukturen zu illustrieren – wohl aber weniger, solche zu identifizieren. Denn letztendlich handelt es sich lediglich um die zweidimensionale Darstellung eines „leeren“ öffentlichen Raumes bzw. seiner physischen, beständigen Hülle, ohne Verkehrsflüsse, Umweltfaktoren oder Menschen, die ihn nutzen. Erst Wissen über solche Nutzungsmuster und Funktionen kann die Grundlage für Planungsentscheidungen bilden.

Wie eingangs erwähnt ist die Straßenraumkarte auch als Kartengrundlage für Themenkarten für den Stadtteil Neukölln konzipiert, bisher aber vor allem für die Parkraumkarte. Diese veranschaulicht in einzelnen Maßstabsstufen verschiedene Daten zum Thema Parkplätze für den Kfz-Verkehr und reicht vom einzelnen Stellplatz über Stellplatzzahlen im Verlauf eines Straßenzugs und Parkflächen abseits des Straßennetzes bis hin zu Informationen über den Flächenverbrauch und einer Berechnung von Stellplatzdichten (siehe Abb. 4). Neben der Parkraumkarte sind weitere thematische Karten als ergänzende Datenlayer geplant: In Arbeit ist eine Radinfrastruktur-Karte, die physische Merkmale und Qualität des Radverkehrsnetzes veranschaulichen soll. Ähnliches könnte sich für den Fußverkehr anschließen. Möglich wären beispielsweise aber auch eine Rettungskarte mit einem Fokus auf Rettungswegen und Notfall-Infrastrukturen, eine Karte mit Informationen zur Qualität und Ausstattung von Grünflächen und Spielplätzen oder eine Themenkarte zu historischen (Gedenk-)Orten im öffentlichen Raum.

{% include image.html
src="images/posts/kartographische-nachrichten/Abbildung04.jpg"
caption="Abb. 4: Ausschnitte der Parkraumkarte in verschiedenen Maßstäben (Zoomstufen): Darstellung von einzelnen Stellplätzen (links), Stellplatzzahlen ganzer Straßensegmente (Mitte) und Stellplatzdichten (rechts). Der Maßstab der verschiedenen Kartenebenen reicht in der Webkarte von etwa 1 : 500 auf der detailliertesten Zoomstufe bis etwa 1 : 15.000 auf der höchsten Ebene. © Kartendaten: OpenStreetMap-Beitragende, Berechnungen der Neuköllner Parkraumanalyse."
%}

## 5. Die Technik: Aus der Geo-Datenbank über die Datenprozessierung zur gestalteten Straßenraumkarte

Technisch basiert die Karte bislang schlicht auf einem individuellen QGIS-Kartenstil, der mit OSM-Rohdaten gespeist wird, welche über die Overpass-API (einem Service für selektive Datenabfragen aus der OSM-Datenbank) abgerufen werden. Dieser Aufbau ist derzeit noch sehr ineffizient, benötigt bei einer Aktualisierung der Karte einige manuelle Eingriffe und ist kaum auf andere oder größere Gebiete übertragbar. Bislang stand die Kartendarstellung an sich im Fokus der Entwicklung; die Verbesserung und Übertragbarkeit der technischen Basis soll sich in Zukunft anschließen.

Der Kartendarstellung ist eine Aufbereitung der OSM-Daten vorgelagert, welches über ein Python-Skript erfolgt. Dieses Skript übernimmt beispielsweise die Generierung der Fahrbahnmarkierungen, die aus Attributen der OSM-Datenobjekte abgeleitet werden, aber sorgt auch für weitere Optimierungen in der Darstellung einzelner Elemente wie Gebäuden oder Wäldern. Im Folgenden sollen einzelne der dabei durchgeführten Arbeitsschritte und ihre kartographischen Effekte kurz skizziert werden.

Die wohl größte Herausforderung bei der Darstellung sind die Fahrbahnmarkierungen bzw. die Prozessierung der Fahrspurattribute: Dazu gehören vor allem Mittellinien, Abbiegespuren, Radfahrstreifen, Zebrastreifen und andere Querungsstellen für den Fußverkehr oder auch Haltelinien an Kreuzungen (siehe Abb. 5). Vielerorts wurden diese Attribute in OSM erst im Zuge der Entwicklung der Straßenraumkarte erfasst oder verbessert, da es ansonsten nur wenige Möglichkeiten gibt, diese aus der abstrakten Datenbankstruktur heraus überhaupt „sichtbar“ zu machen.

{% include image.html
src="images/posts/kartographische-nachrichten/Abbildung05.png"
caption="Abb. 5: Darstellung von Abbiegespuren, Radfahrstreifen, Querungsstellen und Haltelinien an einer Kreuzung. © Kartendaten: OpenStreetMap-Beitragende."
%}

Die Attribute der Datenobjekte in der OSM-Datenbank liegen in „Schlüssel-Wert-Paaren“ vor und folgen bestimmten Konventionen – den in der OSM-Community diskutierten und dokumentierten „Mapping-Schemata“. Im Fall einer Straße bzw. Fahrbahn ist das Datenobjekt beispielsweise eine Linie, welche die gesamte Fahrbahn mit all ihren Eigenschaften und einzelnen Spuren repräsentiert. Im Fall des in Abbildung 5 gezeigten Kartenausschnitts gehören dazu z. B. die Anzahl der Fahrspuren, ihre Widmung für den Kfz-, Rad- oder Busverkehr, in welche Richtung sie führen, wie breit sie sind oder, im Fall des Radstreifens, welche Markierungen sie begrenzen und welche Farbe die Oberfläche hat. Informationen zu einzelnen, auch gegenläufigen Fahrspuren oder Radstreifen auf der Fahrbahn sind also alle in einem einzelnen Geoobjekt vereinigt und müssen für die Kartendarstellung interpretiert, geometrisch erzeugt und versetzt und passend dargestellt werden.

Schon die Interpretation ist nicht immer eindeutig, da es in der offenen OSM-Datenbankstruktur zum Teil verschiedene Konventionen zur Erfassung eines Elements gibt, z. B. allein drei konkurrierende Schemata zur Erfassung von Busspuren. Darüber hinaus werden manche Schemata bislang nur selten mit einem so hohem Detailanspruch wie für die Straßenraumkarte verwendet, sie können also durchaus Lücken oder sogar Widersprüche enthalten. Nicht zuletzt sind die OSM-Daten wie eingangs erwähnt vielerorts unvollständig oder können fehlerhaft sein.

Um aus den linienhaft vorliegenden Fahrbahnattributen in der Karte einen „flächenhaften“ Eindruck zu vermitteln (schließlich sind Fahrbahnen in der Realität Flächen), werden die Liniengeometrien der Straßensegmente entsprechend der Anzahl und Breite der Fahrspuren vervielfältigt und versetzt. In der Karte dargestellt werden vor allem die Begrenzungen (z. B. Mittellinien) oder Symbole (Abbiegepfeile, Rad- oder Busspur-Embleme) der Fahrspuren. Die Fahrbahnflächen selbst sind durch darunter liegende Polygone repräsentiert (siehe auch Abschnitt 2).[^4]

Während der Datenaufbereitung werden darüber hinaus weitere Berechnungen vorgenommen, um die Darstellung bestimmter Elemente in der Straßenraumkarte zu ermöglichen oder zu verbessern. So wird die Lage von Fußgängerüberwegen oder Haltelinien aus – zumindest in Neukölln – separat in OSM erfassten Fußverkehrsinformationen und Knotenpunktgeometrien abgeleitet. In einem anderen Arbeitsschritt werden die in OSM enthaltenen Stockwerksinformationen von Gebäuden verarbeitet, um unterschiedlich hohe oder „schwebende“ Gebäudeteile zu ermitteln und in der Kartendarstellung dezent voneinander abzugrenzen (siehe Abb. 6a). Ein anderes Beispiel sind Waldflächen, die nicht in einer einheitlichen Farbe oder Texturierung dargestellt werden, sondern durch virtuelle Einzelbäume repräsentiert werden: Um diese optisch ansprechend zu verteilen, wird in den Flächen ein hexagonales Gitter mit Innenabständen erzeugt und in jedem Gitterfeld an zufälligem Standort ein Einzelbaumsymbol generiert (siehe Abb. 6b).

{% include image.html
src="images/posts/kartographische-nachrichten/Abbildung06.png"
caption="Abb. 6a und b: Beispiele für Ergebnisse der Datenaufbereitung: Unterscheidung von Gebäudeteilen unterschiedlicher Gebäudehöhe und von schwebenden, nicht auf dem Boden aufsetzenden Gebäudeteilen (links); Erzeugung eines hexagonalen Gitters in Waldflächen als Hilfsmittel und Zwischenschritt zur Platzierung virtueller Einzelbäume zur realistischeren Darstellung von Wäldern (rechts)."
%}

## 6. Der Ausblick: OpenStreetMap an der Grenze zwischen Karte und Plan

Im Gegensatz zu großmaßstäblichen Planwerken wie Vermessungsplänen, Liegenschaftskarten oder den genannten Architekturplänen sind OpenStreetMap-Daten ursprünglich nicht dafür gedacht bzw. nicht dafür optimiert, detaillierte flächenhafte Darstellungen zu erzielen. Insbesondere Straßen werden in der gegenwärtigen OSM-Datenstruktur vorwiegend als abstrakte Linien verstanden und werden dementsprechend auf OSM-basierten Karten üblicherweise auch linienhaft dargestellt. Zwar gibt es Diskussionen und ausgearbeitete, an einzelnen Orten erprobte Schemata, um Fahrbahnen als Flächen zu erfassen, eine größere Verbreitung hat dieser Ansatz in der OSM-Community aber bislang noch nicht erfahren. Da die Routingfähigkeit ein zentraler Anspruch an OSM-Daten ist und Liniengeometrien dabei große – wohl unschlagbare – Vorteile gegenüber Polygonen aufweisen, müssten Linien- neben Flächengeometrien außerdem auf absehbare Zeit gleichzeitig existieren.

Die Straßenraumkarte zeigt aber, dass großmaßstäbliche Plandarstellungen auf OSM-Basis möglich sind, wenn die Daten dafür in ausreichender Genauigkeit erfasst und in der OSM-Datenbank vorgehalten werden. Da es sich bei OSM generell nicht um ein vermessungstechnisches Werk mit einheitlichem Erfassungsstandard handelt, sind Ansprüche an die Genauigkeit und Vollständigkeit der Daten zu überdenken oder hängen zumindest von lokalen Kartierungsaktivitäten und verfügbaren Datenquellen ab. Zumindest auf lokaler Ebene erscheint es aber denkbar, Geodaten in ausreichender Genauigkeit erfassen, verbessern und pflegen zu können, um Darstellungen wie die Straßenraumkarte zu ermöglichen und diese vor Ort beispielsweise in Planungs- oder Beteiligungsprozessen zu nutzen.

OSM auf breiter Ebene in diese Maßstabsebene zu „heben“ wird allerdings durch verschiedene Faktoren erschwert und erscheint daher gegenwärtig eher unrealistisch. Dazu gehören die bereits erwähnten Grenzen bestehender OSM-Kartierungs-Konventionen, die weiter diskutiert, vereinheitlicht, erweitert und besser dokumentiert werden müssen. Zu den Hürden gehört aber auch das gewachsene „Selbstverständnis“ und teils gegensätzliche „Kartierungskulturen“ in der OSM-Community. So stößt das ausgiebige Kartieren von Objekt- oder Landnutzungsdetails (Micro-Mapping) bei einzelnen Mitgliedern auf „puristische“ Widerstände, wobei z. B. argumentiert wird, dass unnötig große Datenmengen mit zweifelhaftem Nutzwert angehäuft werden.

Tatsächlich gehört der hohe Arbeits- und Kartierungsaufwand, der für die genaue und weitreichende Erfassung von Objekten im öffentlichen Raum oder von Fahrspur- oder kleinen Landnutzungsdetails nötig ist, wohl zu den größten Hindernissen – und noch entscheidender der Aspekt der Datenpflege: Je mehr Details kartographisch erfasst sind, desto schneller drohen die Daten zu veralten bzw. desto größer ist der Aufwand, diese Daten kontinuierlich zu aktualisieren. Auch müssen Referenzdaten zum Abgleich verfügbar sein, um hohe Genauigkeiten zu erreichen (wie hochaufgelöste Luftbilder oder ALKIS-Daten in freier Lizenz).

Andererseits stellen Kartendarstellungen erfahrungsgemäß wichtige „Feedbacks“ und damit eine entscheidende Motivation insbesondere für ehrenamtliche OSM-Mapper dar, da sie ihre Beiträge dadurch direkt sehen und kontrollieren können und leichter vorstellbar wird, für welche Zwecke die erfassten Daten nutzbar sind. Die Neuköllner Straßenraumkarte wird von lokalen OSM-Aktiven im Stadtteil beispielsweise genutzt, um fehlende oder veraltete Detailinformationen direkt erkennen zu können, wovon die Karte wiederum direkt profitiert. Auf herkömmlichen OSM-Karten bleiben viele Details wie Bordsteinkanten oder Fahrbahnattribute dagegen unsichtbar und werden daher selten kartiert. Daran schließt sich eine weitere Hürde an: Fehlende intuitive und grafisch gestützte Editoren für Detailinformationen wie z. B. Fahrbahnattribute, wodurch deren Erfassung selbst für erfahrene Mapper stets aufwendig und fehleranfällig ist. Doch auch hierfür entwickeln sich erste Projekte im OSM-Umfeld wie die osm2lanes-Bibliothek.[^5]

Die Neuköllner Straßenraumkarte ist somit auch ein Beitrag, um die Grenzen von OSM zu testen und zu deren Verschiebung anzuregen. Der große Anklang, den die Karte im Stadtteil und darüber hinaus erfährt, zeigt den Bedarf nach ästhetisch ansprechenden und frei zugänglichen Stadtplänen mit großem Maßstab. Die dafür erforderlichen Kartendaten sind nicht nur interessant für Kartendarstellungen und deren Nutzung z. B. in Planungsprozessen, sondern eröffnen darüber hinaus interessante Analysemöglichkeiten: Die genannte Parkraumanalyse oder die Bewertung der Qualität von Radverkehrsinfrastrukturen sind zwei davon; andere Beispiele sind Schattenberechnungen für Grünanlagen und Spielplätze oder schlicht eine Verbesserung von Wegeberechnungen beim Routing aufgrund genauerer Straßen- und Wegedaten. Vielleicht können diese großen Potentiale dazu führen, dass „urbanes Präzisionsmapping“ und Darstellungen wie die Straßenraumkarte schon in wenigen Jahren zu einem gewohnten Anblick im OSM-Umfeld gehören.

## Fußnoten

[^1]: Alex Seidel, OpenStreetMap-Community Berlin, E-Mail: alex@osm-berlin.org
[^2]: Die Neuköllner Straßenraumkarte ist online unter [https://strassenraumkarte.osm-berlin.org/?map=micromap](https://strassenraumkarte.osm-berlin.org/?map=micromap) verfügbar.
[^3]: Ein Bericht zu den Ergebnissen dieser Parkraumanalyse findet sich hier: [https://parkraum.osm-verkehrswende.org/posts/2021-03-12-parkraumanalyse](https://parkraum.osm-verkehrswende.org/posts/2021-03-12-parkraumanalyse)
[^4]: Zu technischen Einzelheiten des Fahrspur-Processings siehe den Lightning Talk zur Neuköllner Straßenraumkarte auf der FOSSGIS-Konferenz 2022 ([https://pretalx.com/fossgis2022/talk/ERAZ9G/](https://pretalx.com/fossgis2022/talk/ERAZ9G/)) und diesen englischsprachigen Blogartikel: [https://strassenraumkarte.osm-berlin.org/posts/2021-12-31-micromap-update](https://strassenraumkarte.osm-berlin.org/posts/2021-12-31-micromap-update)
[^5]: Für das osm2lanes-Projekt siehe [https://github.com/a-b-street/osm2lanes](https://github.com/a-b-street/osm2lanes).
