---
title: Methodenbericht zur Parkraumanalyse für den Berliner Ortsteil Neukölln
layout: page
description: Methoden- und Ergebnisbericht der Parkraumanalyse der Berliner OpenStreetMap Community für den Berliner Ortsteil Neukölln
image:
  path: images/report/social-sharing.jpg
  alt:
show_legend: true
menu_highlight: report
download:
  path: methodenbericht-2021-03.pdf
  link_text: Methodenbericht downloaden (PDF 1,1 MB)
---

# Parkraumanalyse für den Berliner Ortsteil Neukölln – Methoden- und Ergebnisbericht

Stand: März 2021

## Autoren und Hintergrund
{: class="mt-5 mb-4" }

Alexander Seidel, M.A.
und OpenStreetMap-Beitragende

*Diese Parkraumanalyse entstand im Rahmen einer Mobilitäts- und Verkehrswende-Initiative der Berliner OpenStreetMap-Community (OSM) und wurde als ehrenamtliches Projekt durchgeführt. Ein großer Teil der Datenauswertung und Datenerhebung geht auf Alexander Seidel, Sozial- und Stadtgeograf und OSM-Beitragender, zurück und mündete gemeinsam mit den Beiträgen vieler anderer OSM-Beitragender in den hier vorgestellten Ergebnissen.*

## 1. Einführung
{: class="mt-5 mb-4" }

Daten über die Anzahl und Verteilung von Kfz-Parkplätzen im Stadtraum stellen eine wertvolle Ressource dar. So wird der Verkehrsraum im Zuge der Verkehrswende zunehmend neu verteilt oder zumindest politisch darüber gestritten und die Reduzierung des ruhenden Verkehrs in diesem Zusammenhang als wichtiger Ansatzpunkt für mehr Flächengerechtigkeit identifiziert. Gleichzeitig finden Verkehr und Mobilität unter Einbeziehung geographischer Daten immer zielgerichteter statt, sodass beispielsweise unnötige Wege oder innenstädtischer Verkehr verhindert werden können – auch hier können Parkplatz- und Stellplatzdaten einen Beitrag leisten.

Vielerorts gibt es jedoch noch gar kein systematisches Wissen, wo es wie viele Parkplätze gibt. In aufwendigen Studien müssen diese Daten bei Bedarf erfasst werden – und meist sind diese Daten anschließend nicht für die Öffentlichkeit zugänglich. Im Gegensatz dazu stellt die freie Geodatenbank OpenStreetMap (OSM) eine optimale Umgebung dar, in der solche Daten frei zugänglich erfasst und analysierbar gemacht werden können.

Diese Parkraumanalyse demonstriert am Beispiel des Berliner Ortsteils Neukölln, wie urbaner Parkraum systematisch auf OSM-Basis kartiert und mit Geoinformationssystemen (GIS) und unter Einbezug weiterer offener Daten hochaufgelöst ausgewertet werden kann. Ziel des Projektes ist es,

* eine Methode zur Erhebung und Verarbeitung parkraumbezogener Geodaten zu demonstrieren,
* Standorte und Stellplatzzahlen aller Parkmöglichkeiten -- sowohl im öffentlichen Straßenraum als auch im privaten Raum -- zu ermitteln,
* Stellplatzdichten unter Einbeziehung von Kfz- und Bevölkerungsdaten zu berechnen,
* Angaben zum Flächenverbrauch durch geparkte Fahrzeuge zu machen,
* die Daten für das Untersuchungsgebiet zur freien Verwendung bereit zu stellen.

Der vorliegende Bericht stellt die Herangehensweise und Methodik der Parkraumanalyse dar und geht kurz auf zentrale Ergebnisse ein.



## 2. Methodik
{: class="mt-5 mb-4" }

### 2.1. Allgemeine Herangehensweise
{: class="mt-5 mb-4" }

Die dieser Auswertung zugrunde liegenden Parkplatzdaten wurden systematisch für dieses Projekt in der **OSM-Datenbank** erfasst bzw. vervollständigt, mit offenen Daten aus weiteren Quellen angereichert und mit der Software QGIS ausgewertet. Zwar umfasst OSM immer umfangreichere und zunehmend hochspezialisierte Geoinformationen und bietet insbesondere in Mitteleuropa einen nahezu lückenlosen Datensatz zum Straßennetz, die Detailtiefe der Informationen ist jedoch regional unterschiedlich ausgeprägt und abhängig von den Aktivitäten und Interessen lokaler Communities und ihren Beitragenden. So gehören Daten zu straßenbegleitendem Parken beispielsweise derzeit noch nicht zu den „Standardinformationen" und sind vielerorts lediglich rudimentär erfasst. Eine Übertragung der hier demonstrierten Analyse auf andere Orte wird daher zur Zeit meist an die Bedingung geknüpft sein, die notwendigen Daten zuvor zu erheben bzw. zu vervollständigen. Darüber hinaus stellt die angewandte Methodik hohe Ansprüche an die Präzision und Lagegenauigkeit der Daten, da aus diesen Geometrien weitere Werte wie Stellplatzkapazitäten oder Halteverbote abgeleitet werden. Je genauer und vollständiger die Daten dabei vorliegen, desto präzisere Ergebnisse können anschließend daraus ermittelt werden.[^1]

[^1]: Welchen Einfluss eine geringere Genauigkeit und Vollständigkeit der OSM-Daten auf die Qualität des Ergebnisses insbesondere in Bezug auf das Straßenparken hätte, soll Gegenstand späterer Auswertungen sein, die [auf der Projektseite im OSM-Wiki dokumentiert](https://wiki.openstreetmap.org/wiki/Berlin/Verkehrswende/Parkraumanalyse_Neuk%C3%B6lln) werden.

Die Auswertung berücksichtigt verschiedene Arten von Park- und Stellplätzen, die auf unterschiedliche Weise erfasst und interpretiert werden. Den überwiegenden Anteil am Kfz-Parkraumangebot stellt in der Berliner Innenstadt das **Straßenparken** dar, also Parken im öffentlichen Straßenraum auf Parkstreifen am Fahrbahnrand. Basis des Datenmodells dieser Parkraumanalyse ist es, die Anzahl und Lage dieser Stellplätze aus der (geomterisch linienhaft erfassten) Information abzuleiten, auf welchen Abschnitten und mit welcher Ausrichtung (Längs, Schräg, Quer) entlang einer Straße geparkt werden kann. Streckenabschnitte, an denen nicht geparkt werden darf (Einfahrten, abgesenkte Bordsteine, Kreuzungsbereiche, Gehwegübergänge, Park- und Halteverbote etc.), werden automatisiert ermittelt und aus der Auswertung ausgeschlossen. Vergleiche zwischen berechneten/interpolierten und realen/gezählten Werten zeigen, dass diese Methode bei ausreichender Qualität der Datengrundlage präzise Ergebnisse liefert (vgl. Kapitel 3).

Darüber hinaus wurden Informationen zu (meist privaten) **Stellplätzen abseits des Straßenraums** erhoben und einbezogen, die geometrisch in flächenhafter Form vorliegen. Dazu zählen:
* allgemeine, meist ebenerdige Park- und Stellplätze,
* Tiefgaragen,
* Garagen und Carports,
* Parkhäuser.

Diese Objekte sind häufiger mit einer genauen Stellplatzzahl erfasst, da diese oft markiert und abzählbar sind. Aus ihrer Grundfläche (und, bei mehrstöckigen Objekten, ggf. unter Berücksichtigung ihrer horizontalen Ausdehnung) kann die Stellplatzkapazität aber auch abgeschätzt werden.

Die Stellplatzdaten enthalten zusätzliche Attribute wie zu Beschränkungen der Nutzung oder Zugänglichkeit (öffentlich/privat/Kunden etc., Gebühren, zeitliche Beschränkungen) und können auf dieser Grundlage gezielt ausgewertet werden.

### 2.2. Untersuchungsgebiet
{: class="mt-5 mb-4" }

Die vorliegende Parkraumanalyse bezieht sich auf den Berliner Ortsteil Neukölln. Das gesamte Untersuchungsgebiet, für das Parkplatzdaten erhoben wurden, umfasst das Gebiet innerhalb der Ortsteilgrenzen Neuköllns sowie einen Pufferbereich von 500 Metern außerhalb der Ortsteilgrenze, um insbesondere bei Aussagen zur Stellplatzdichte Verzerrungen an den Randbereichen zu vermeiden. Der Ortsteil Neukölln umfasst eine Fläche von 11,7 km² (gesamtes Untersuchungsgebiet: 20,6 km²).

Der Ortsteil Neukölln ist ein überwiegend von Wohnquartieren geprägter, dicht besiedelter und eng bebauter urbaner Raum mit 165.000 Einwohnerinnen und Einwohnern. Er ist durch eine vergleichsweise geringe Motorisierungsquote geprägt: Pro 1.000 Personen sind hier 219 Kraftfahrzeuge zugelassen.[^2] Das Gebiet des Ortsteils umfasst zwei Gewerbegebiete, die bei einigen Auswertungen nicht berücksichtigt wurden. Die in diesem Fall berücksichtigten Wohnquartiere erstrecken sich über eine Fläche von 7,4 km² (Kfz-Quote: 206 pro 1.000 Personen) und können für genauere Datenauswertungen in 16 Teilgebiete untergliedert werden, die den lokalen „Kiezen“ bzw. lebensweltlich orientierten Räumen entsprechen ([vgl. Anhang A](#anhang-a-verfügbare-stellplatzkapazitäten-in-verschiedenen-teilräumen)).

[^2]: Berechnet nach Amt für Statistik Berlin-Brandenburg: „Melderechtlich registrierte Einwohnerinnen und Einwohner am Ort der Hauptwohnung in Berlin am 30.06.2020 nach Planungsräumen und KfZ-Bestand", verfügbar auf der [Datenseite zu dieser Parkraumanalyse](https://supaplexosm.github.io/strassenraumkarte-neukoelln/parkraumkarte/data).

In Bezug auf die Parkraumsituation spielen zwar tagsüber insbesondere entlang der Hauptstraßen einzelhandelsbezogen vielerorts Lieferverkehr und Kurzzeitparken eine zentrale Rolle, in den Kiezen (und außerhalb der Geschäftszeiten) wird die lokale Parkraumsituation jedoch vom Parkverhalten der Anwohnenden bestimmt. Um die Parkraumsituation zu bewerten, sind daher vor allem Parkmöglichkeiten relevant, die sich zum dauerhaften Parken eignen. Kunden- oder Mitarbeiterparkplätze sind zwar im Datensatz enthalten, wurden aber bei der Ermittlung des regulären Stellplatzangebots und von Stellplatzdichten ausgeschlossen. Aufgrund ihrer teils großen Kapazitäten (insbesondere von Supermarkt-Parkplätzen) stellen sie dennoch eine wichtige Größe dar, die in der Diskussion um die zukünftige Gestaltung des Parkraums nicht vernachlässigt werden darf und in Modellen wie Anwohner-Nachtparken mancherorts bereits Berücksichtigung findet.

Gewerblich genutzte Parkplätze (z.B. für Transportfahrzeuge des Handwerks) sind in die Auswertungen eingeflossen, da die herangezogenen Vergleichsdaten zum tatsächlichen Fahrzeugbestand auch gewerbliche Fahrzeuge enthalten. Insgesamt spielen Stellplätze dieser Art in den Wohnquartieren – also außerhalb der Gewerbegebiete – aber nur eine geringe Rolle.

### 2.3. Datenerhebung, Datenquellen und Datensätze
{: class="mt-5 mb-4" }

Der überwiegende Anteil der Park- und Stellplatzdaten wurde durch systematische Begehungen des Untersuchungsgebiets zwischen Frühjahr und Herbst 2020 erfasst. Gegenstand dieser Kartierung war vor allem die Erhebung des Straßenparkens im Verlauf des etwa 170 km umfassenden Straßennetzes (davon 104 km im Ortsteil Neukölln) und die Vervollständigung von etwa 2.200 Gebäude- und Grundstückseinfahrten (davon etwa 1.400 im Ortsteil Neukölln), da vor diesen nicht geparkt werden darf.[^3] Darüber hinaus wurden Daten zu anderen Parkmöglichkeiten wie Garagen und Stellplätzen erhoben, soweit diese erreichbar oder sichtbar waren.

[^3]: Gebäudeeinfahrten wurden dann in die Auswertung einbezogen, wenn sie an der Fahrbahneinmündung eine Bordsteinabsenkung besitzen und als Einfahrt erkennbar oder ausgeschildert sind. Das ist in der überwiegenden Mehrheit der baulich angelegten Einfahrten der Fall. In selteneren Fällen werden solche Einfahrten trotz Bordsteinabsenkung aber offensichtlich nicht mehr genutzt (weder für Fahrzeuge noch bspw. für die Müllabfuhr) und sind auch nicht als Einfahrt gekennzeichnet, möglicherweise auch rechtlich nicht mehr als solche gewidmet.

Die Erhebungen vor Ort wurden durch weitere Auswertungen und Recherchen ergänzt:

* Auswertung von Luftbildern, um Stellplätze in nicht öffentlich zugänglichen Bereichen, insbesondere Hinterhöfen, zu ermitteln. Im Berliner Geoportal stehen jährlich erzeugte, meist im Frühjahr aufgenommene Orthophotos zur Verfügung; einbezogen wurden Aufnahmen von 2016 bis 2019.

* Ermittlung von Tiefgaragengrundflächen auf Grundlage des Amtlichen Liegenschaftskatasterinformationssystems (ALKIS) und Plausibilitätsprüfung mit Kartendaten und Luftbildern sowie vor Ort.[^4]

[^4]:	Da die ALKIS-Daten in manchen Fällen offensichtlich fehlerhaft sind oder Tiefgaragenteile fehlen, wurden einige Geometrien auf Grundlage von Kartendaten und Luftbildern korrigiert (insbesondere unter Berücksichtigung von Gebäudegrundflächen oder darüber liegenden Strukturen wie ebenerdigen Parkplätzen, Hängen und Eingängen). Drüber hinaus wurden vor Ort die Zufahrtswege zu den Tiefgaragen erfasst und Standorte ausgeschlossen, wenn keine Zufahrtswege aufgefunden werden konnten bzw. in selteneren Fällen Tiefgaragen mit geschätzten Grundflächen einbezogen, wenn diese vollständig in den ALKIS-Daten fehlten.

* Überprüfung von Gebäuden, die im ALKIS als Garage kategorisiert sind, auf ihren faktischen Status als Garage bzw. ihre Tauglichkeit zum Abstellen von Kraftfahrzeugen (vor Ort sowie auf Luft- und Schrägluftbildern).

* Recherche von Stellplatzkapazitäten von Parkhäusern und Tiefgaragen aus online zugänglichen Dokumenten (Websites, Berichte und Planungsunterlagen zu Bauprojekten, Bebauungspläne...) oder vereinzelt durch Nachfrage bei Vermietern und Eigentümern.

Für die anschließende Analyse wurden weitere Daten aufbereitet und einbezogen:

* Kfz-Bestand auf Ebene der LOR-Planungsräume (Lebensweltlich orientierte Räume) zur Ermittlung der Stellplatzdichte: „Melderechtlich registrierte Einwohnerinnen und Einwohner am Ort der Hauptwohnung in Berlin am 30.06.2020 nach Planungsräumen und KfZ-Bestand", auf Nachfrage zur Verfügung gestellt durch das Amt für Statistik Berlin-Brandenburg.

* Einwohnerdichte auf Ebene der Block- und Blockteilflächen (Stand 31.12.2019, verfügbar im Berliner Geoportal/Umweltatlas) und Gebäudedatensatz (ALKIS) zur Generierung eines gebäudebezogenen Bevölkerungsmodells (vgl. Kapitel 2.6).

* Die Blockflächen wurden außerdem herangezogen, um unter Einbeziehung von OSM-Daten die Fläche öffentlicher Verkehrsräume als Grundlage von Flächenverbrauchsberechnungen zu ermitteln (öffentliche Fahrbahn- und Gehwegbereiche, also der Raum zwischen den Gebäudefassaden bzw. Grundstücksgrenzen).

Generierung eines Bordsteinkanten- bzw. Fahrbahn-Datensatzes aus OSM- und ALKIS-Daten (Datensatz „Bauwerke, Anlage und Einrichtung in Siedlungsflächen und für den Verkehr"), um eine exakte Lagegenauigkeit der Parkstreifen zu erreichen. Dieser Bordsteinkanten- bzw. Fahrbahndatensatz bildet außerdem eine Grundlage für die Visualisierung der Straßen- und Parkraumkarte.

### 2.4. Datenverarbeitung zur Modellierung des Straßenparkens
{: class="mt-5 mb-4" }

Das OSM-Datenschema zur Erfassung von Parkstreifen („parking:lane"-Schema) sieht vor, einem Straßensegment jeweils Informationen zum Parken am linken und rechten Fahrbahnrand zuordnen zu können. Dazu gehören in erster Linie:

* Art des Parkens: Entweder Park- oder Halteverbote, oder die Anordnung/Ausrichtung der geparkten Fahrzeuge (insbes. Längs, Schräg, Quer).
* Position des Parkens: Die Fahrzeuge können auf der Fahrbahn, in einer Parkbucht, auf dem Gehweg, halb auf dem Gehweg oder auf dem Seitenstreifen stehen.
* Bedingungen und Einschränkungen: Stellplätze können insbesondere für bestimmte Nutzergruppen reserviert, zeitlich begrenzt nutzbar oder gebührenpflichtig sein.

Die Straßensegmente liegen geometrisch als Linienobjekte vor, die geteilt werden können, wenn sich Attribute im Straßenverlauf ändern. Besteht entlang eines Teilabschnitts einer Straße beispielsweise ein Parkverbot, kann dieses direkt über ein eigenes Straßensegment differenziert werden. Kleinteilige Einschränkungen wie Einfahrten oder Gehwegübergänge müssen (und sollen) nicht gesondert segmentiert werden, da sie aus den entsprechenden Daten im späteren Verlauf abgeleitet werden können. Abweichungen von signifikanter Länge, wie im Bereich längerer Gehwegvorstreckungen, wurden bei der Datenerfassung jedoch durch Teilung der Straßensegmente berücksichtigt.

Die eigentliche Datenverarbeitung fand weitestgehend automatisiert über Python-Scripte[^5] und Geoverarbeitungswerkzeuge in QGIS statt, wobei in groben Zügen diese Arbeitsschritte erfolgten:

[^5]: Online verfügbar auf der [Projektseite der Parkraumanalyse](https://github.com/SupaplexOSM/strassenraumkarte-neukoelln).

(1.) Entsprechend der Fahrbahnbreite, die entweder direkt am Straßenobjekt hinterlegt ist oder aus seinen Attributen abgeschätzt werden kann, können die räumlichen Verläufe der jeweils linken und rechten Parkstreifen abgeleitet werden.

(2.) Bereiche, in denen sich aus der Straßenverkehrsordnung (StVO) ein Park- bzw. Halteverbot ergibt oder die sich entsprechend ihrer baulichen Anlage nicht zum Parken eignen, und die nicht bereits durch beschilderte Park- und Halteverbote abgebildet sind, können anschließend aus den Daten ausgeschlossen werden, in dem dort Abschnitte mit einer vorbestimmten Länge abgetrennt werden. Die Länge ergibt sich aus der StVO, Richtwerten oder der typischen baulichen Anlage im Untersuchungsgebiet:

<div class="table-responsive">
<table class="table table-hover table-bordered table-sm caption-top">
  <caption>Tabelle 1: Abstandsdefinitionen zum Parken an verschiedenen baulichen Anlagen.</caption>
  <thead class="table-secondary">
    <tr>
        <th class="w-50">Objekt / bauliche Anlage</th>
        <th class="w-50">Länge / Abstand</th>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td>Kreuzung</td>
        <td>
        je 5 Meter vor Schnittpunkt der Bordsteinkanten
        <div class="text-muted"><small>Seit der StVO-Novelle aus dem Jahr 2020 erhöht sich dieser Abstand auf 8 Meter, wenn sich neben der Fahrbahn ein baulich angelegter Radweg befindet, was im Datenmodell jedoch noch nicht berücksichtigt wird – im Untersuchungsgebiet aber auch nur an vergleichsweise wenigen Kreuzungen der Fall ist.</small></div>
        </td>
    </tr>
    <tr>
        <td>Grundst&uuml;cks- und Gebäudeeinfahrten,abgesenkte Bordsteine</td>
        <td>Breite der Einfahrt, wenn bekannt, aber mindestens 4 Meter</td>
    </tr>
    <tr>
        <td>
          &Uuml;bergänge f&uuml;r andere Verkehrsteilnehmer:
          <ul>
            <li>Fu&szlig;gänger&uuml;berwege (Zebrastreifen)</li>
            <li>randseitige Markierungen oder Gehwegvorstreckungen</li>
            <li>Fu&szlig;gängerfurten und sonstige Markierungen</li>
          </ul>
        </td>
        <td>4 Meter und je 5 Meter davor6 Meter4 Meter und evtl. Ampeln</td>
    </tr>
    <tr>
        <td>Ampeln (nicht klar geregelt, faktisch kaum eingehalten)</td>
        <td>10 Meter davor</td>
    </tr>
    <tr>
        <td>Bushaltestellen</td>
        <td>15 Meter davor und dahinter</td>
    </tr>
  </tbody>
</table>
</div>


(3.) Objekte, die das Parken im Parkstreifenbereich verhindern, wurden vor der Auswertung systematisch erfasst bzw. vervollständigt und in einem separaten Arbeitsschritt mit Sicherheitsabständen von den Parkbereichen abgezogen. Dazu gehören Fahrradabstellanlagen, Straßenbäume, Laternen, Poller, Bordsteinstrukturen, Straßenschilder sowie insbesondere beim (halben) Parken auf Gehwegen auch Straßenmöbel und Gehweg-Einbauten (z.B. Verteilerkästen). Insgesamt betrifft das aber nur einen kleinen Anteil aller Straßen.

(4.) Die berechneten Parkstreifensegmente wurden anschließend einer (zum Teil manuell gesteuerten) Nachbearbeitung unterzogen: So wurden kurze Segmente und Artefakte entfernt und Fehler- und Plausibilitätsprüfungen durchgeführt (z.B. Korrektur von überlappenden oder angrenzenden, aber nicht verbundenen Segmenten).

(5.) Für die vorliegende Parkraumanalyse wurde zudem zusätzlich eine aufwendige manuelle Nachbearbeitung vorgenommen, insbesondere um die Parkstreifen an die exakten, realen Bordsteinkanten anzupassen.[^7] Die Präzision wurde dadurch zwar erheblich erhöht, da dieser Schritt lagegenaue Aussagen ermöglicht, die allgemeine Aussagekraft der Ergebnisse wäre ohne eine solche Nachbearbeitung jedoch kaum beeinträchtigt und ist bei Übertragung der Parkraumanalyse auf andere Orte daher verzichtbar.[^8]

(6.) Abschließend wurden Stellplatzkapazitäten für zusammenhängende Parkstreifensegmente berechnet (Quotient aus der Länge eines Segments und dem Abstand der dort geparkten Fahrzeuge, vgl. nachfolgender Abschnitt).

[^7]: Dafür wurde zunächst ein automatisiertes „Snapping“ und anschließend eine systematische Fehlerkorrektur und Nachkontrolle für jedes Einzelsegment vorgenommen, teils unter Verwendung von aktuellen Straßenfotos (Mapillary) und anderen Daten wie dem Verkehrszeichen- und Gehwegüberfahrten-Layer der Berliner Straßenbefahrung 2014 zur präziseren Ausrichtung von Park- und Halteverboten oder Einfahtsbereichen.
[^8]: Die Abweichung zwischen den rein automatisiert ermittelten Stellplatzzahlen und den nachbearbeiteten Daten beträgt für das Straßenparken lediglich 0,6 Prozent und ist damit geringer als die anderer Unsicherheitsfaktoren (vgl. Kapitel 3).


### 2.5. Interpolation von Stellplatzkapazitäten
{: class="mt-5 mb-4" }

#### 2.5.1. Straßenparken
{: class="mt-5 mb-4" }

Für 5,5 Prozent aller Parkstände im Straßenbereich des Untersuchungsgebiets lagen bereits in den OSM-Daten Kapazitätsangaben vor, insbesondere bei markierten Parkständen und Parkbuchten. Die fehlenden Werte mussten aus der Länge der Parkstreifensegmente abgeleitet werden.

Beim Parallelparken sind einzelne Stellplätze meist nicht markiert; die Anzahl der Fahrzeuge, die entlang eines Streckenabschnitts geparkt werden können, richtet sich vielmehr nach der Fahrzeuglänge und einem Rangier-/Sicherheitsabstand. Dabei wird in der Verkehrsplanungsliteratur ein mittlerer Abstand von 5,2 Metern zwischen den Fahrzeugen angenommen, der sich bei Zählungen im Untersuchungsgebiet weitestgehend bestätigen lässt ([vgl. auch Anhang B](#anhang-b-vergleich-interpolierter-und-gezählter-stellplätze-straßenparken)). Beim Schräg- und Querparken richtet sich die Anordnung der einzelnen Parkstände üblicherweise nach den Empfehlungen für Anlagen des ruhenden Verkehrs (EAR).[^9] Beim Schrägparken sind dabei verschiedene Aufstellwinkel möglich, die in verschiedenen Parkstandsbreiten resultieren -- hier wurde ein konstanter Aufstellwinkel von 60 gon (54 Grad) angenommen.[^10] Daraus ergeben sich folgende Abstände zwischen jeweils zwei geparkten Fahrzeugen:

[^9]:	Forschungsgesellschaft für Straßen- und Verkehrswesen e.V. (FGSV) (Hrsg.): Empfehlungen für Anlagen des ruhenden Verkehrs EAR 05, Ausgabe 2005. Köln: FGSV-Verlag.
[^10]: Dieser Wert entspricht dem Winkel, der bei den meisten Parkständen dieser Art aus Stichproben im Untersuchungsgebiet aus Orthophotos ermittelt werden konnte. Bei davon abweichenden Winkeln ist insgesamt nur eine marginale Abweichung in Bezug auf das Gesamtergebnis zu erwarten, daher wurde dieser Wert zur Vereinfachung der Berechnungen als konstant angenommen.


* Längsparken:  5,2 Meter,
* Schrägparken:  3,1 Meter,
* Querparken:  2,5 Meter.

Die Stellplatzkapazität ergibt sich aus dem Quotienten der Länge eines Parkstreifensegments und dem entsprechenden Abstand, abgerundet auf eine ganze Zahl.

<div class="max-w-prose bg-info p-3 pb-1 mt-1 mb-5">

**Ergebnis:**

Für den Ortsteil Neukölln ergeben sich insgesamt 27.335 Kfz-Stellplätze im öffentlichen Straßenraum. In den Wohnquartieren des Ortsteils, also abzüglich der Gewerbegebiete Ederstraße und Köllnische Heide, sind es 24.403 ([vgl. ausführlicher Anhang A](#anhang-a-verfügbare-stellplatzkapazitäten-in-verschiedenen-teilräumen)).

Die Parkraumkarte stellt die Stellplätze in verschiedenen Zoomstufen in unterschiedlichen Formen dar -- von einer straßenzugsorientierten Zählung bis zum einzelnen Stellplatz.

</div>

#### 2.5.2. Park- und Stellplätze abseits des Straßenbereichs
{: class="mt-5 mb-4" }

Für die geometrisch flächenhaft vorliegenden Park- und Stellplätze abseits des öffentlichen Straßenraums liegen häufiger genaue Stellplatzangaben vor, da diese oft markiert und abzählbar sind. Für etwa die Hälfte der Parkplätze liegen jedoch keine Angaben vor (vgl. 2); diese Stellplatzkapazitäten werden aus der Grundfläche der geometrischen Objekte abgeleitet (sowie bei mehrgeschossigen Objekten in einigen Fällen aus der Anzahl der Parkebenen). Dies betrifft vor allem Tiefgaragen: Für diese lagen auf Grund der eingeschränkten Zugänglichkeit nur für 36 von 221 einbezogenen Objekten genaue Stellplatzzahlen vor.[^11] Da das Daten- bzw. Interpolationsmodell hier nur an den wenigen realen, bekannten Fällen validiert werden konnte, unterliegen diese Daten auch einer größeren Unsicherheit (vgl. Kapitel 3).

[^11]: Die bekannten Stellplatzinformationen für Tiefgaragen basieren auf online zugänglichen Dokumenten wie Berichten und Planungsunterlagen zu Bauprojekten oder Inseraten auf Vermietungsportalen, Zählungen vor Ort sowie vereinzelt erfolgreichen Nachfragen bei Vermietern oder Eigentümern (vgl. auch Kapitel 2.3).

Aus den Objekten mit bekannten Stellplatzangaben wurde der Median der mittleren Fläche pro Stellplatz ermittelt – differenziert für verschiedene Stellflächentypen und unter Berücksichtigung evtl. mehrstöckiger Stellplatzobjekte (Geschossfläche). Die geschätzte Kapazität eines Stellplatzobjekts ergibt sich aus dem Quotienten der Geschossfläche der Objektgeometrie und diesem Medianwert. Die Differenzierung nach Stellflächentypen ist notwendig, da diese sich im Flächenbedarf pro Fahrzeug und der baulichen Gestalt unterscheiden: Beispielsweise enthalten Garagengeometrien üblicherweise keine Zufahrtswege, während diese bei Tiefgaragen ebenso wie Stützelemente, Ausgänge etc. in der Grundfläche enthalten sind. Ebenerdige Park- und Stellplätze wurden in eine kleinere und eine größere Kategorie geteilt, da kleinere Stellflächen meist ohne, größere überwiegend mit Zufahrtswegen in den OSM-Daten enthalten sind.[^12]

[^12]: Kleinere Parkplätze umfassen dabei weniger als acht Stellplätze, größere mindestens acht. Diese Grenze wurde aus den vorhandenen Objekten mit genauen Angaben zur Stellplatzkapazität abgeleitet, da in diesem Bereich ein signifikanter Sprung im Quotienten aus Fläche und Stellplatzanzahl zu beobachten war.

<div class="table-responsive">
<table class="table table-hover table-bordered table-sm caption-top">
  <caption>Tabelle 2: Berechnungsgrundlage für die Interpolation von Stellplatzkapazitäten geometrisch flächenhafter Parkraumobjekte.</caption>
  <thead class="table-secondary">
    <tr>
      <th rowspan=2>Stellfl&auml;chentyp</th>
      <th rowspan=2>Fl&auml;che pro Stellplatz [m&sup2;]</th>
      <th colspan=2>Anzahl Objekte im Datensatz *</th>
      <th rowspan=2>Anteil gesch&auml;tzter Stellpl&auml;tze</th>
    </tr>
    <tr>
      <th>gesamt</th>
      <th>mit bekannter Stellplatzzahl</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Carports</td>
      <td>14,9</td>
      <td>46</td>
      <td>38</td>
      <td>14 %</td>
    </tr>
    <tr>
      <td>Garagen</td>
      <td>16,8</td>
      <td>789</td>
      <td>578</td>
      <td>34 %</td>
    </tr>
    <tr>
      <td>Parkh&auml;user</td>
      <td>28,2</td>
      <td>9</td>
      <td>5</td>
      <td>8 %</td>
    </tr>
    <tr>
      <td>Parkpl&auml;tze (klein) **</td>
      <td>14,5</td>
      <td>537</td>
      <td>327</td>
      <td>42 %</td>
    </tr>
    <tr>
      <td>Parkpl&auml;tze (gro&szlig;)</td>
      <td>21,7</td>
      <td>472</td>
      <td>247</td>
      <td>48 %</td>
    </tr>
    <tr>
      <td>Tiefgaragen</td>
      <td>31,3</td>
      <td>221</td>
      <td>36</td>
      <td>81 %</td>
    </tr>
    <tr class="table-light">
      <td><strong>Summe</strong></td>
      <td><strong>-</strong></td>
      <td><strong>2074</strong></td>
      <td><strong>1231</strong></td>
      <td><strong>47 %</strong></td>
    </tr>
  </tbody>
</table>
</div>

\* Die *Anzahl* bezieht sich auf die Gesamtzahl der Objekte eines Stellflächentyps im Untersuchungsraum, also im Berliner Ortsteil Neukölln sowie einer Pufferzone von 500 Metern um dessen Ortsteilgrenzen.

\*\* Die Kategorie *„Parkplätze“* umfasst überwiegend klassische ebenerdige Park- und Stellplätze (N = 994), aber auch vereinzelt vorkommendes Dachparken (N = 6) und Parkdecks/Parkflächen im Erdgeschoss unter Gebäuden (N = 9).

<div class="max-w-prose bg-info p-3 pb-1 mt-1 mb-5">

**Ergebnis:**

Für den Ortsteil Neukölln ergeben sich daraus 12.226 (in den Wohnquartieren: 11.044) Stellplätze abseits des Straßenraums, die sich dauerhaft bzw. über Nacht zum Parken für Anwohnende eignen. Zusammen mit dem Straßenparken stehen somit insgesamt 39.561 (Wohnquartiere: 35.447) Stellplätze zur Verfügung, denen 36.266 (33.513) angemeldete Kfz gegenüber stehen, was einer theoretischen Stellplatzauslastung von 91,7 Prozent (94,5 Prozent) entspricht.

Darüber hinaus gibt es im Ortsteil Neukölln 8.105 (Wohnquartiere: 1.940) nicht zum dauerhaften Parken geeignete Stellplätze (insbesondere Mitarbeiter- und Kundenparkplätze), sowie 428 (219) ungenutzte Stellplätze, beispielsweise in leerstehenden Tiefgaragen.

Die Parkraumkarte stellt auch diese Stellplätze abseits des Straßenparkens dar, differenziert nach Stellflächentypen und Eignung zum Dauerparken.

</div>

### 2.6. Ermittlung von Stellplatzdichten mit gebäudegenauem Bevölkerungsmodell
{: class="mt-5 mb-4" }

Ein Ziel der Auswertung ist es, kleinräumige Stellplatzdichteverteilungen zu berechnen, also die Anzahl von Kfz-Stellplätzen in einem Gebiet mit der Anzahl der Einwohnerinnen und Einwohner bzw. der Anzahl der zugelassenen Kfz zu vergleichen. Dabei wird angenommen, dass die Anzahl der zugelassenen Fahrzeuge an einem Ort ein Indikator für tatsächlich an einem Ort geparkte Fahrzeuge ist, was zumindest für Wohngebiete naheliegt (vgl. Kapitel 3). Das Verhältnis von verfügbaren Stellplätzen zur Anzahl zugelassener Kraftfahrzeuge wird im Folgenden als „Stellplatzdichte" bezeichnet.

Für kleinräumige Aussagen, beispielsweise zur Bestimmung der Stellplatzdichte für einen bestimmten Straßenzug oder im Umfeld eines bestimmten Ortes, sind entsprechend hoch aufgelöste, adress-genaue Kfz-Daten notwendig, die im Rahmen dieses Projekts jedoch nicht zur Verfügung standen. Abhilfe schafft ein eigenes Datenmodell auf Grundlage von Bevölkerungsdaten auf Blockebene (323 Teilräume allein im Ortsteil Neukölln mit durchschnittlich je etwa 500 Einwohnerinnen und Einwohnern) und Kfz-Daten auf LOR-Planungsraumebene (18 Teilräume im Ortsteil Neukölln mit durchschnittlich je knapp 10.000 Einwohnerinnen und Einwohnern; zu den Datensätzen vgl. Kapitel 2.3).

Für das Bevölkerungsmodell wurde zunächst jedem Gebäude die statistisch erwartbare Anzahl von Bewohnenden zugeordnet. Dafür müssen zunächst Wohngebäude von anderen Gebäuden unterschieden[^15] und die jeweils zum Wohnen genutzten Gebäudestockwerke ermittelt werden.[^16] Die Gesamtbevölkerung einer Blockteilfläche wurde schließlich anteilig dieser „Wohngeschossflächenzahl" auf die Gebäude verteilt. Jede Bewohnerin und jeder Bewohner lässt sich auf diese Weise statistisch individuell am Wohnort darstellen und kann auf Basis der Kfz-Anmeldedaten mit einer entsprechenden Wahrscheinlichkeit als Kfz-Halter/in eingestuft werden.

[^15]: Die ALKIS-Gebäudedaten enthalten für jedes Gebäude eine Klassifikation seiner Funktion, sodass Wohngebäude beispielsweise von Büro-, Gewerbe- oder Industriegebäuden unterschieden werden können oder Mischnutzungen erkennbar sind.
[^16]: Für reine Wohngebäude wurden dabei alle Obergeschosse einbezogen. Für Gebäude der Kategorie „Wohngebäude mit Gewerbenutzung“ ist anzunehmen, dass ein Geschoss (Erdgeschoss) nicht zum Wohnen genutzt wird. Für die eher seltene Kategorie „Gewergegebäude mit Wohnnutzung“ wurde angenommen, dass die Hälfte aller Geschosse als Wohngeschosse genutzt werden.

Die resultierenden Kfz-Halterdaten lassen sich auf diese Weise -- ebenso wie die verfügbaren Stellplätze -- in Form von Punktwolken abbilden, wobei jeder Punkt einem Stellplatz bzw. einem zugelassenen Kfz entspricht. Für ein bestimmtes Gebiet lässt sich auf diese Weise leicht das Verhältnis aus verfügbaren Stellplätzen und angemeldeten Kfz ermitteln. Die Parkraumkarte stellt diese Stellplatzdichte auf niedrigeren Zoomstufen für das Nahumfeld eines Wohnortes dar, wobei eine fußläufige Distanz von 350 Metern (3 Minuten zu Fuß bei einer Laufgeschwindigkeit von 7 km/h bzw. knapp über 4 Minuten bei 5 km/h) zugrunde liegt. Die Stellplatzdichte für diese Distanz wurde jeweils für den Gittermittelpunkt eines 25 Meter großen hexagonalen Gitters berechnet auf Basis von Isochronen[^17] berechnet.

[^17]: Isochronen sind räumliche Linien gleicher Zeit, umgrenzen in diesem Fall also einen Raum, der innerhalb der angegebenen Zeit zu Fuß erreicht werden kann und sich dabei bis zu 350 Meter entfernt vom Ausgangspunkt erstreckt. Das Routing erfolgte über das OSM-Straßen- und Wegenetz.


<div class="max-w-prose bg-info p-3 pb-1 mt-1 mb-5">

**Ergebnis:**

Im Durchschnitt (Median) ergibt sich für die Neuköllner Wohnquartiere im Umkreis von 350 Metern Laufdistanz um einen Ort eine Anzahl von 835 Stellplätzen, eine Zahl von 759 zugelassenen Kraftfahrzeugen und eine theoretische Verfügbarkeit von 1,08 Stellplätzen pro Fahrzeug. Wird nur das Straßenparken berücksichtigt, stehen in diesem Umkreis 604 Stellplätze zur Verfügung (Median: 0,81 pro Fahrzeug).

Wie viele finden im Nahumfeld einen Parkplatz, wie viele müssen im Mittel weiter fahren?

Bei der Interpretation dieser Darstellung ist zu berücksichtigen, dass Räume und Objekte mit größerem Stellplatzüberangebot -- wie dünn besiedelte Gebiete oder Parkhäuser, die einen wichtigen Beitrag zur Stellplatzversorgung eines größeren Umfelds leisten können -- sich nur innerhalb dieser Nahdistanz auf das Ergebnis auswirken.

</div>

### 2.7. Flächenverbrauch
{: class="mt-5 mb-4" }

Aus der Lage und Länge der Parkstreifen im Straßenraum kann -- abhängig von der Ausrichtung der dort geparkten Fahrzeuge -- auf die Fläche geschlossen werden, die direkt von stehenden bzw. geparkten Fahrzeugen in Anspruch genommen wird. Die Breite eines Parkstreifens entspricht dabei:

* 2 Meter bei Längsparken,
* 4,5 Meter bei Schrägparken,
* 5 Meter bei Querparken.

Diese Fläche kann in Relation zur Fläche des öffentlichen Straßen- bzw. Verkehrsraumes gesetzt werden, also der Fläche zwischen den Gebäudefassaden oder Grundstücksgrenzen inklusive aller Straßenbestandteile wie Fahrbahnen, Mittelstreifen oder Geh- und Radwegen. Berechnungsgrundlage dafür ist die Einteilung der Blockflächen, wie sie im Berliner Geoportal beispielsweise für die Wiedergabe der Bevölkerungsdichte verwendet wird (vgl. Kapitel 2.3). In unbewohnten Räumen hat diese Blockflächeneinteilung Lücken, die auf Basis von OSM-Daten gefüllt wurden.

<div class="max-w-prose bg-info p-3 pb-1 mt-1 mb-5">

**Ergebnis:**

Allein für die Neuköllner Wohnquartiere ergibt sich daraus, dass Parkstreifen im öffentlichen Straßenraum eine Fläche von insgesamt 327.000 m² in Anspruch nehmen, was 19 Prozent des öffentlichen Verkehrsraumes und 4,4 Prozent der Gesamtfläche entspricht. Parkflächen und Stellplätze abseits des Straßenraumes beanspruchen darüber hinaus zusätzlich 171.000 m², ein Gesamtflächenanteil von 2,3 Prozent.

</div>

## 3. Bewertung von Unsicherheitsfaktoren
{: class="mt-5 mb-4" }

Die vorgestellte Parkraumanalyse basiert auf einem interpolativen Datenmodell, also aus geografischen Daten und empirischen Annahmen abgeleiteten Aussagen und Vereinfachungen, um die (komplexe) Realität modellhaft abzubilden und „berechenbar“ zu machen. Viele der zu Grunde liegenden Annahmen und Ergebnisse können in der tatsächlichen Realität überprüft, gezählt oder gemessen werden, andere unterliegen bestimmten Unsicherheiten, die sich kaum oder nur mit erheblichem empirischen Aufwand quantifizieren lassen. Wie viele Garagen werden beispielsweise tatsächlich zum Abstellen von Kfz genutzt, wie viele Falschparker gibt es oder wie viele Dienst- und Mietwagen bleiben in der Kfz-Statistik für das Untersuchungsgebiet unberücksichtigt? Und vor allem: Wie präzise ist die Wiedergabe der Stellplatzzahlen am Straßenrand? Unsicherheitsfaktoren wie diese sollen in diesem Abschnitt einer groben Schätzung unterzogen werden.

Da das Straßenparken die Parkraumsituation wesentlich prägt, ist sie das Kernstück des Datenmodells. Um diesen Aspekt des Datenmodells zu prüfen, wurden in zwei Testgebieten über 70 Straßenteilstücke mit verschiedenen Parkanordnungen (Längs/Schräg/Quer, Fahrbahn- und Bordsteinparken, gerade und kurvige Segmente, blockierende Objekte im Parkstreifenbereich etc.) abgelaufen und und die dort geparkten Fahrzeuge bzw. verfügbaren Stellplätze[^20] mit dem Datenmodell verglichen, um seine Aussagekraft zu belegen (vgl. Anhang B). Der Vergleich zeigt insgesamt eine hohe Übereinstimmung zwischen interpolierten und vor Ort gezählten Werten mit einer Gesamtabweichung von weniger als einem Prozent – allerdings sind Unterschiede zwischen den Ergebnissen bei Längs- sowie Schräg- und Querparken zu beobachten. Während beim Längsparken eine leichte Überschätzung von 1,1 Prozent auftritt, liegen die berechneten Werte beim Schräg- und Querparken um etwa 8 bis 9 Prozent unter den gezählten Stellplatzzahlen (was jedoch nur einen geringen Einfluss auf das Gesamtergebnis hat, da diese nur 13 Prozent aller Parkstreifen ausmachen und sich der Fehler mit dem Längspark-Ergebnis nahezu ausgleicht). Dieser signifikante Fehlerwert ist vor allem auf sehr hohe Abweichungen in drei einzelnen Straßenabschnitten zurückzuführen, in denen der Einfluss von Einfahrten und Objekten im Parkraum (Bäume, Straßenlaternen) deutlich überschätzt wurde, also tatsächlich wesentlich mehr Fahrzeuge abgestellt werden können als interpoliert. Beim Schrägparken kann zudem eine systematische Abweichung hinzukommen, da der reale Winkel der Parkstände von dem Festwert im Datenmodell abweichen kann.

[^20]: Gezählt wurden Fahrzeuge und Parklücken mit ausreichender Größe für einen Pkw, soweit ein ordnungskonformes Parken eingehalten wird, also insbesondere unter Einhaltung des 5-Meter-Abstands zu Kreuzungen und der Freihaltung von Einfahrten.

Die automatisiert erzeugten Parkstreifendaten der vorliegenden Parkraumanalyse wurden einer aufwendigen manuellen Nachbearbeitung unterzogen, wodurch ebenfalls eine (quantitativ jedoch ebenfalls eher vernachlässigbare) Fehlerkorrektur erfolgte: Die Stellplatzzahlen des Rohdatensatzes lagen 0,6 Prozent über denen des nachbearbeiteten Datensatzes (vgl. Kapitel 2.4).

Darüber hinaus gibt es eine Reihe anderer Faktoren, die zu einer Über- oder Unterschätzung der realen Parkraumsituation im Vergleich zum Datenmodell führen können. Sie lassen sich nur schwer bemessen und können daher nicht oder nur eingeschränkt in einem numerischen Datenmodell abgebildet werden. Für die Interpretation der Ergebnisse der Parkraumanalyse sind insbesondere diese Faktoren zu berücksichtigen:

* Das Datenmodell des Straßenparkens bildet eine juristische, StVO-konforme Situation ab; in der Realität ist im Untersuchungsraum jedoch häufiges Falschparken zu beobachten bis hin zu faktischen Parkstreifen in verkehrsberuhigten Bereichen, in denen dauerhaft falsch geparkt wird (z.B. Isar-/Neckarstraße). Darüber hinaus gibt es Graubereiche wie Diagonal- und Querparken, das eigentlich durch Beschilderung oder Markierungen angeordnet sein müsste, was vor Ort in manchen Fällen nicht (mehr) erkennbar ist -- in diesem Fall gibt das Modell die Situation wieder, wie sie vor Ort und in der Vergangenheit (Luftbildaufnahmen) dauerhaft zu beobachten war.

* Für zwei Szenarien wurde der Einfluss durch Falschparkverhalten quantifiziert:

  * Wird der mittlere Abstand geparkter Fahrzeuge zum Kreuzungsbereich von 5 auf 2,5 Meter halbiert, erhöht sich die Anzahl geparkter Fahrzeuge im Straßenraum um 3,3 Prozent.

  * Wird vor jeder zweiten Einfahrt geparkt, erhöht sich die Anzahl geparkter Fahrzeuge im Straßenraum um 2,6 Prozent.

* Bei der Berechnung von Stellplatzdichten unter Verwendung von Kfz-Anmeldedaten wird angenommen, dass die Anzahl angemeldeter Fahrzeuge an einem Ort ein Indikator für tatsächlich dort geparkte Fahrzeuge ist (vgl. Kapitel 2.6). Insbesondere in Wohnquartieren dürfte hier zumindest eine starke Korrelation bestehen -- die tatsächliche Anzahl geparkter Fahrzeuge könnte allerdings höher sein, insbesondere da:

  * Firmen-/Dienstwagen von einem Teil der Bevölkerung privat, also auch an ihrem Wohnort genutzt werden, die Fahrzeuge dort jedoch meist nicht angemeldet sind und daher statistisch unsichtbar bleiben. Dieser Wert lässt sich nur schwer quantifizieren, dürfte im Untersuchungsgebiet aber in einer Größenordnung von höchstens vier Prozent aller Kfz liegen.[^21]

  * Zunehmend sind in diesem Zusammenhang auch Fahrzeuge von Carsharing-Anbietern zu berücksichtigen, von denen in Berlin derzeit etwa 6.000 im Free-Floating-Segment bereitstehen. Im Untersuchungsgebiet dürfte der Anteil dieser Fahrzeuge etwa in einer Größenordnung von einem Prozent liegen.[^22] Zusätzlich beanspruchen stationsbasierte Anbieter vereinzelt Stellplätze beispielsweise in Tiefgaragen.

[^21]: Etwa vier Prozent der Autofahrer:innen in Deutschland geben an, dass ihr Erstfahrzeug ein Dienstwagen ist (vgl. Statista: [„Anzahl der Personen in Deutschland, deren Erstwagen ein Privat- bzw. Dienstwagen ist"](https://de.statista.com/statistik/daten/studie/172094/umfrage/dienstwagen-oder-privatwagen-als-erstwagen/)). Inwieweit sich diese Angaben auf die sozioökonomischen und geografischen Bedingungen des Untersuchungsgebiets übertragen lassen und wie Zweitwagen etc. und andere Faktoren diesen Wert beeinflussen, kann an dieser Stelle nicht bewertet werden.
[^22]:	Unter der Annahme, dass diese 6.000 Fahrzeuge alle innerhalb des S-Bahn-Rings abgestellt würden, wo es etwa 350.000 zugelassene Kfz gibt, ergäbe sich ein Anteil von 1,7 Prozent der dort zugelassenen Fahrzeuge. Der Geschäftsbereich vieler Anbieter erstreckt sich aber auch darüber hinaus.

* In Gebieten mit geringem Parkdruck kommen außerdem Fahrzeuge dazu, die dort auf Grund der günstigen Parkraumsituation länger und in größerer Entfernung zu ihrem eigentlichen Meldeort abgestellt werden (beispielsweise sporadisch genutzte Transporter oder Wohnmobile) -- dafür aber am eigentlichen Meldeort keinen Stellplatz in Anspruch nehmen. Phänomene wie Besuchsverkehr dürften dagegen bei der Bewertung der dauerhaften Parkraumsituation nur einen geringen Einfluss haben.

* Stellplatzangaben, die neben dem Straßenparken im öffentlichen Raum auch die (meist privaten) Stellplätze abseits des Straßenraums berücksichtigen, müssen als potentielle Aussagen verstanden werden, da die tatsächliche Auslastung von Stellplätzen unbekannt bleibt. Vor allem Garagen werden beispielsweise häufig anders genutzt als zum Abstellen eines Kfz. Unter der Annahme, dass jede zweite Garage nicht zum Abstellen eines Kfz genutzt wird, reduziert sich das Gesamt-Stellplatzangebot im Datenmodell um 3 Prozent. In Nachbarschaften mit hohem Garagenanteil, insbesondere dem Rollbergkiez, kann das im Einzelfall zu größeren Unsicherheiten führen.

* Alle Parkhäuser im Untersuchungsgebiet können auch von Anwohnerinnen und Anwohnern genutzt werden; sie tragen insgesamt fast 4 Prozent der Gesamtstellplatzkapazitäten im Datenmodell bei. Faktisch wird dieses Potential jedoch offenbar nicht ausgeschöpft, da ein großer Leerstand beobachtet werden kann. Zum Teil trifft dies auch auf andere, dauerhaft gering ausgelastete Stellplätze, Tiefgaragen etc. zu.

* Tiefgaragen tragen 7 Prozent aller verfügbaren Stellplätze bei, 81 Prozent dieser Tiefgaragenstellplätze basieren allerdings auf geschätzten Werten (vgl. Kapitel 2.5.2). Läge die tatsächliche Anzahl der geschätzten Tiefgaragenplätze 10 Prozent über oder unter den ermittelten Werten, würde sich das Gesamt-Stellplatzangebot im Datenmodell um 0,6 Prozent erhöhen bzw. reduzieren. Dieser Wert ist vergleichsweise gering; im Einzelfall könnten jedoch größere Abweichungen auftreten. So wird die Parkraumsituation rund um den Mariendorfer Weg im Datenmodell von zwei sehr großen Tiefgaragen dominiert, die zu einem großen Überangebot von Stellplätzen führen. Die reale Stellplatzzahl könnte hier unter Umständen erheblich geringer sein oder nicht für alle Anwohnenden zur Verfügung stehen.

* Baustellen und andere temporäre Halte- und Parkverbote finden keine Wiedergabe im Datenmodell, führen in der Realität aber permanent zu einer leichten Reduktion der tatsächlich nutzbaren Stellplatzkapazitäten.

Darüber hinaus gibt es weitere Faktoren, die im konkreten Fall zu Unsicherheiten führen können, in Relation zur Gesamtheit der Daten aber nur einen sehr geringen Teil betreffen und bei denen daher ein eher vernachlässigbarer Einfluss auf die allgemeine Aussagekraft angenommen werden kann:

* Es muss davon ausgegangen werden, dass nicht alle parkplatzrelevanten Objekte kartiert wurden und einige falsch oder nicht mehr aktuell klassifiziert sind. Fehlen dürften vor allem kleinere Stellplätze in schattigen Hinterhöfen oder auch Parkgaragen im Erdgeschoss von Gebäuden, die schwer aus dem öffentlichen Raum aus zugänglich oder einsehbar sind und auf Luftbildaufnahmen nicht erkennbar sind.

* Das Datenmodell umfasst nur Parkstreifen sowie Park- und Stellplätze, vernachlässigt jedoch beispielsweise das (teils ordnungswidrige) Parken auf Einfahrten, Wegen oder anderen nicht dafür angelegten Flächen.

* Den Stellplatzkapazitäten für Parkstreifen liegt eine pauschale Fahrzeuglänge bzw. ein fester Abstand zwischen zwei geparkten Fahrzeugen zu Grunde, basierend auf einer gemittelten Fahrzeuglänge. Tatsächliche Fahrzeuglängen sind natürlich variabel; es gibt zudem Fahrzeuge mit größerem (z.B. Transporter) oder kleinerem (z.B. Motorräder) Raumbedarf. Der für die Stellplatzdichte berücksichtigte Kfz-Datensatz umfasst zu 80 Prozent Pkw, der Rest teilt sich vor allem zu etwa gleichen Teilen auf Krafträder und Lastkraftwagen (wozu auch die meisten Kleintransporter zählen) auf.[^23]

[^23]: Für Berlin vgl. Amt für Statistik Berlin-Brandenburg: Kraftfahrzeugbestand im Land Berlin, hier online verfügbar.

* Die Abgrenzung von gewerblich genutzten Stellplätzen, beispielsweise für (meist an diesem Ort angemeldete) Transportfahrzeuge des Handwerks, und Mitarbeiter- oder Kundenparkplätzen, die nicht zum Dauerparken angelegt sind (und daher in einigen Auswertungen nicht berücksichtigt werden), ist im Einzelfall schwer oder durch Mischnutzung unmöglich, daher können diese teils falsch zugeordnet sein.

Einfahrten bzw. abgesenkte Bordsteine, für die in den OSM-Daten keine Breiten vermerkt sind, gehen mit einer pauschalen Breite von 4 Metern[^24] in das Datenmodell ein. Im Einzelfall können diese schmaler oder breiter sein, auch wenn besonders breite Einfahrten während der Datenerhebungsphase meist mit einer Breitenangabe versehen wurden oder die Parkstreifen in diesem Bereich in der manuellen Nachbearbeitung der Daten korrigiert wurden.

[^24]:  In der Rechtsprechung wird teils eine Breite von 3 Metern als ausreichend angesehen, was im Datenmodell insgesamt eine um 0,7 Prozent höhere Stellplatzzahl ergeben würde. Das einzelne Einfahrten breiter sind, aber nicht mit ihrer tatsächlichen Breite in das Modell einfließen, ist dabei jedoch noch nicht berücksichtigt.

## Anhang A: Verfügbare Stellplatzkapazitäten in verschiedenen Teilräumen
{: class="mt-5 mb-4" }

<iframe style="width: 100%; height: 660px" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vQ5p58km0xRVhNBoKrN2U9nmFEawl7fUUrngg1vart29LI6TVVXttqs45gz-pmaRC0btcBIPR4_UMaW/pubhtml?widget=true&amp;headers=false"></iframe>

## Anhang B: Vergleich interpolierter und gezählter Stellplätze (Straßenparken)
{: class="mt-5 mb-4" }

<iframe style="width: 100%; height: 1450px" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vTz-b9t4qHgk3yN-n7g1y8f9KszT-77AjJsDgGPi0d3E04hKCcB-GG1rd39LUcHHMErju3lQJSPEt4S/pubhtml?gid=670505529&amp;single=true&amp;widget=true&amp;headers=false"></iframe>

## Fußnoten
{: class="mt-5 mb-4" }
