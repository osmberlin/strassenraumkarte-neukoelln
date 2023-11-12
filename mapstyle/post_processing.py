#---------------------------------------------------------------------------#
#   Straßenraumkarte / micromap post processing script                      #
#   --------------------------------------------------                      #
#   OSM data post-processing for QGIS/PyGIS for rendering the map at        #
#   https://strassenraumkarte.osm-berlin.org/                               #
#                                                                           #
#   > version/date: 2023-11-10                                              #
#---------------------------------------------------------------------------#

import os, processing, math, random, time

#-------------------------------------------------#
#   V a r i a b l e s   a n d   S e t t i n g s   #
#-------------------------------------------------#

#processing steps - set "1" for the needed step(s) befor running the script:
proc_crossings      = 0     # < # Fahrbahnbezogene Eigenschaften von Querungsstellen ermitteln und übertragen
proc_cr_markings    = 0     #   # Querungsstellen mit randseitigen Markierungen am Bordstein ausrichten
proc_cr_lines       = 0     #   # Linien markierter Gehweg-Querungsstellen erzeugen
proc_cr_tactile_pav = 0     #   # Taktile Bodenleitsysteme entlang von Bordsteinen und Wegen generieren
proc_lane_markings  = 0     # < # Straßenmarkierungen erzeugen
proc_highway_backup = 0     #   # Straßenlinien als Backup in fahrbahnfreien Bereichen erzeugen
proc_service        = 0     #   # service-Wege mit gleichen Eigenschaften zusammenführen, um Lücken zu vermeiden
proc_oneways        = 0     #   # Für Einbahnstraßen separate Linien zur Markierung erzeugen
proc_traffic_calming= 0     # < # Straßeneigenschaften auf Verkehrsberuhigungsmaßnahmen übertragen
proc_cycleways      = 0     #   # Radwege nachbearbeiten
proc_path_areas     = 0     #   # Vereinigt aneinander angrenzende Wegeflächen und erzeugt deren Outlines
proc_railways       = 0     #   # Separiert Schienensegmente mit Bahnübergängen, um diese über Fahrbahnflächen rendern zu können
proc_buildings      = 1     # < # Stockwerkszahl und schwebende Etagen für jedes Gebäudeteil/Gebäude auflösen, Gebäudegrundrisse verarbeiten
proc_housenumbers   = 0     #   # Hausnummern gleichmäßig zum Gebäudeumriss ausrichten
proc_water_body     = 0     #   # Gewässerkörper zu einem Einzelpolygon vereinigen
proc_landcover      = 0     #   # Bereiche mit "landcover=*" in Polygone umwandeln (werden nur als Linien erkannt)
proc_pitches        = 0     #   # Erzeugt Texturen für Sportfelder und richtet diese aus
proc_playgr_landuse = 0     #   # Gras-Flächen zur besseren Darstellung aus playground-Polygonen ausstanzen
proc_playgr_equip   = 0     #   # Geschlossene Linien bei Spielgeräten zu Polygonen umwandeln
proc_orient_man_made= 0     # < # Richtet bestimmte Straßenmöbel zur nächstgelegenen Straße hin aus (Straßenlaternen, Schaltkästen, BSR-Transportüberwege)
proc_trees          = 0     #   # Baumkronendurchmesser und Stammumfang abschätzen
proc_forests        = 0     #   # Waldbäume über ein hexagonales Gitter interpolieren
proc_cars           = 0     #   # Fahrzeuge auf Parkstreifen mit Farben und Fahrzeugmodellen generieren
proc_labels         = 0     #   # bessere Segmente zur Beschriftung von Straßennamen und Gewässern generieren

#processing steps for other map layers:
proc_parking_areas  = 0     # Erzeugt einen Layer mit Kiezflächen, denen Zahlen zu vorhandenen Stellplätzen aller Art zugeordnet sind
proc_protected_bl   = 0     # Filtert separat gemappte geschützte Radspuren und richtet sie an Straßenlinie aus

#project directory
from console.console import _console
project_dir = os.path.dirname(_console.console.tabEditorWidget.currentWidget().path) + '/'
data_dir = project_dir + 'layer/geojson/'
proc_dir = data_dir + 'post_processed/'

#directorys for special map layers
parking_dir = data_dir + 'parking/'

#Default road width (if no other value is mapped)
width_minor_street = 11
width_primary_street = 17
width_secondary_street = 15
width_tertiary_street = 13
width_service = 4
width_driveway = 2.5

#Default lane and cycleway width (if no other value is mapped)
lane_width_default = 3 #wenn nicht anders angegeben mit width:lanes*
cycleway_width_default = 1.5 #wenn nicht anders angegeben mit cycleway*:width oder width:lanes* in Mittellagen
parking_width_default = 2.2 #wenn nicht anders angegeben mit parking:<side>:width

#Liste von Attributen, die für den Straßenlayer bewahrt wird
#Achtung: Bestimmte Angaben sind für die Verarbeitung notwendig
street_key_list = [
'id',
'highway',
'name',
'oneway',
'surface',
'smoothness',
'ref',
'lanes',
'service',
'construction',
'width',
'width:carriageway',
'est_width',
'layer',
'location'
]

#Liste von highway-Tags abseits des allgemeinen Straßennetzes (insbes. Erschließungs-/Wirtschaftswege)
is_service_list = ['service', 'track', 'bus_guideway', 'footway', 'cycleway', 'path']

#Liste von Attributen, die für die Fahrspurdarstellung relevant sind
lanes_attributes = [
'id',
'highway',
'name',
'oneway',
'oneway:bicycle',
'dual_carriageway',
'lanes',
'lanes:unmarked',
'lanes:forward',
'lanes:forward:unmarked',
'lanes:backward',
'lanes:backward:unmarked',
'lanes:conditional',
'lanes:forward:conditional',
'lanes:backward:conditional',
'turn',
'turn:forward',
'turn:backward',
'turn:lanes',
'turn:lanes:forward',
'turn:lanes:backward',
'lanes:bus',
'lanes:bus:forward',
'lanes:bus:backward',
'lanes:psv',
'lanes:psv:forward',
'lanes:psv:backward',
'bus:lanes',
'bus:lanes:forward',
'bus:lanes:backward',
'psv:lanes',
'psv:lanes:forward',
'psv:lanes:backward',
'width:lanes',
'width:lanes:forward',
'width:lanes:forward:start',
'width:lanes:forward:end',
'width:lanes:backward',
'width:lanes:backward:start',
'width:lanes:backward:end',
'width:effective',
'lane_markings',
'lane_markings:junction',
'lane_markings:crossing',
'temporary:lane_markings',
'overtaking',
'change',
'change:lanes',
'change:lanes:forward',
'change:lanes:backward',
'placement',
'placement:forward',
'placement:backward',
'placement:start',
'placement:forward:start',
'placement:backward:start',
'placement:end',
'placement:forward:end',
'placement:backward:end',
'parking:both:width',
'parking:left:width',
'parking:right:width',
'cycleway',
'cycleway:both',
'cycleway:right',
'cycleway:left',
'cycleway:width',
'cycleway:both:width',
'cycleway:right:width',
'cycleway:left:width',
'cycleway:separation',
'cycleway:separation:left',
'cycleway:separation:right',
'cycleway:separation:both',
'cycleway:both:separation',
'cycleway:both:separation:left',
'cycleway:both:separation:right',
'cycleway:both:separation:both',
'cycleway:right:separation',
'cycleway:right:separation:left',
'cycleway:right:separation:right',
'cycleway:right:separation:both',
'cycleway:left:separation',
'cycleway:left:separation:left',
'cycleway:left:separation:right',
'cycleway:left:separation:both',
'cycleway:marking:left',
'cycleway:marking:right',
'cycleway:marking:both',
'cycleway:both:marking:left',
'cycleway:both:marking:right',
'cycleway:both:marking:both',
'cycleway:right:marking:left',
'cycleway:right:marking:right',
'cycleway:right:marking:both',
'cycleway:left:marking:left',
'cycleway:left:marking:right',
'cycleway:left:marking:both',
'cycleway:left:traffic_mode:left',
'cycleway:left:traffic_mode:right',
'cycleway:left:traffic_mode:both',
'cycleway:right:traffic_mode:left',
'cycleway:right:traffic_mode:right',
'cycleway:right:traffic_mode:both',
'cycleway:both:traffic_mode:left',
'cycleway:both:traffic_mode:right',
'cycleway:both:traffic_mode:both',
'cycleway:buffer',
'cycleway:buffer:left',
'cycleway:buffer:right',
'cycleway:buffer:both',
'cycleway:both:buffer',
'cycleway:both:buffer:left',
'cycleway:both:buffer:right',
'cycleway:both:buffer:both',
'cycleway:right:buffer',
'cycleway:right:buffer:left',
'cycleway:right:buffer:right',
'cycleway:right:buffer:both',
'cycleway:left:buffer',
'cycleway:left:buffer:left',
'cycleway:left:buffer:right',
'cycleway:left:buffer:both',
'cycleway:lane',
'cycleway:left:lane',
'cycleway:right:lane',
'cycleway:both:lane',
'cycleway:type',
'cycleway:both:type',
'cycleway:right:type',
'cycleway:left:type',
'cycleway:lanes',
'cycleway:lanes:forward',
'cycleway:lanes:backward',
'cycleway:surface:colour',
'cycleway:both:surface:colour',
'cycleway:right:surface:colour',
'cycleway:left:surface:colour',
'temporary:cycleway',
'temporary:cycleway:both',
'temporary:cycleway:left',
'temporary:cycleway:right'
]

#Liste von Attributen, die für den Gebäudelayer bewahrt wird
building_key_list = [
'id',
'building',
'building:part',
'addr:housenumber',
'addr:postcode',
'addr:street',
'addr:suburb',
'building:levels',
'roof:levels',
'building:min_level',
'min_height',
'layer',
'location'
]

#Leer-Variablen für evtl. einzulesende Rohdatenlayer
layer_raw_highway_points = layer_raw_man_made_points = NULL
layer_raw_highway_ways = layer_raw_path_ways = layer_raw_barrier_ways = layer_raw_waterway_ways = layer_raw_kerb_ways = NULL
layer_raw_kerb_street_areas_polygons = layer_raw_area_highway_polygons = layer_raw_buildings_polygons = layer_raw_barrier_polygons = layer_raw_landuse_polygons = layer_raw_leisure_polygons = layer_raw_natural_polygons = NULL

#Speicheroptionen für gewünschtes (metrisches) Ziel-KBS
crs_from = "EPSG:4326"
crs_to = "EPSG:25833"
transform_context = QgsCoordinateTransformContext()
transform_context.addCoordinateOperation(QgsCoordinateReferenceSystem(crs_from), QgsCoordinateReferenceSystem(crs_to), "")
coordinateTransformContext=QgsProject.instance().transformContext()
save_options = QgsVectorFileWriter.SaveVectorOptions()
save_options.driverName = 'GeoJSON'
save_options.ct = QgsCoordinateTransform(QgsCoordinateReferenceSystem(crs_from), QgsCoordinateReferenceSystem(crs_to), coordinateTransformContext)

#-------------------------------
#   V a r i a b l e s   E n d   
#-------------------------------



def createStreetAreaPolygons():
#-------------------------------------------------------------------------------------------
#   Extract a carriageway area dataset from area:highway polygons
#   +temporary: Merge OSM highway areas with an external dataset of carriageway areas
#-------------------------------------------------------------------------------------------
    print(time.strftime('%H:%M:%S', time.localtime()), '   Fahrbahnflächen generieren...')
    print(time.strftime('%H:%M:%S', time.localtime()), '      Lade Straßenflächen...')
    layer_area_highway_polygons = QgsVectorLayer(data_dir + 'area_highway.geojson|geometrytype=Polygon', 'area_highway (raw)', 'ogr')
    #extract carriageway areas
    layer_street_area_polygons = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_area_highway_polygons, 'EXPRESSION' : '"area:highway" IS \'primary\' OR "area:highway" IS \'primary_link\' OR "area:highway" IS \'secondary\' OR "area:highway" IS \'secondary_link\' OR "area:highway" IS \'tertiary\' OR "area:highway" IS \'tertiary_link\' OR "area:highway" IS \'residential\' OR "area:highway" IS \'unclassified\' OR "area:highway" IS \'living_street\' OR "area:highway" IS \'pedestrian\' OR "area:highway" IS \'road\'', 'OUTPUT': 'memory:'})['OUTPUT']
    print(time.strftime('%H:%M:%S', time.localtime()), '      Vereinige mit externen Daten...')
    #temporary: Merge OSM highway areas with an external dataset of carriageway areas
    layer_external_street_area_polygons = QgsVectorLayer(data_dir + 'kerb/kerb_street_areas.geojson|geometrytype=Polygon', 'Fahrbahnbereiche (extern, raw)', 'ogr')
    layer_street_area_polygons = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_external_street_area_polygons, layer_street_area_polygons], 'OUTPUT': 'memory:'})['OUTPUT']
    print(time.strftime('%H:%M:%S', time.localtime()), '      Datensatz auflösen...')
    #dissolve and clean up dataset
    layer_street_area_polygons = processing.run('native:dissolve', { 'INPUT' : layer_street_area_polygons, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_street_area_polygons = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_street_area_polygons, 'OUTPUT': 'memory:'})['OUTPUT']
    #delete all attributes (don't need any of them)
    layer_street_area_polygons.startEditing()
    attr_count = len(layer_street_area_polygons.attributeList())
    for id in range(attr_count - 1, 0, -1):
        layer_street_area_polygons.deleteAttribute(id)
    layer_street_area_polygons.updateFields()
    layer_street_area_polygons.commitChanges()

    return(layer_street_area_polygons)



def prepareLayers(layer_street, layer_path, layer_crossing):
#-------------------------------------------------------------------------------
#   Layer vorbereiten
#-------------------------------------------------------------------------------
    print(time.strftime('%H:%M:%S', time.localtime()), '   Füge Straßendaten ein...')

    #Straßen-Input in einen Straßen- und einen Einfahrtlayer teilen

    processing.run('native:reprojectlayer', { 'INPUT' : layer_raw_highway_ways, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT' : proc_dir + 'streets_processed.geojson' })
    processing.run('native:reprojectlayer', { 'INPUT' : layer_crossing, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT' : proc_dir + 'crossing.geojson' })
    layer_street = QgsProject.instance().addMapLayer(QgsVectorLayer(proc_dir + 'streets_processed.geojson', 'Straßen', 'ogr'), False)
    layer_crossing = QgsProject.instance().addMapLayer(QgsVectorLayer(proc_dir + 'crossing.geojson', 'Übergänge', 'ogr'), False)

    print(time.strftime('%H:%M:%S', time.localtime()), '   Datensatz bereinigen...')
    layer_street = clearAttributes(layer_street, street_key_list)

    #Attribute für crossings bereinigen
    attr_list = [
        'id',
        'highway',
        'crossing',
        'crossing_ref',
        'crossing:island',
        'crossing:markings',
        'crossing:kerb_extension',
        'crossing:buffer_marking',
        'tactile_paving',
        'kerb',
        'traffic_signals',
        'traffic_signals:sound',
        'traffic_signals:vibration',
        'supervised',
        'wheelchair',
        'mapillary',
        'direction',
        'traffic_signals:direction',
        'crossing:direction:angle',
        'stop_line',
        'stop_line:angle',
        'temporary'
    ]
    layer_crossing = clearAttributes(layer_crossing, attr_list)

    print(time.strftime('%H:%M:%S', time.localtime()), '   Breitenattribute ermitteln...')
    layer_street.startEditing()

    if layer_street.fields().indexOf('width:carriageway') == -1:
        layer_street.dataProvider().addAttributes([QgsField('width:carriageway', QVariant.String)])
    if layer_street.fields().indexOf('source:width') == -1:
        layer_street.dataProvider().addAttributes([QgsField('source:width', QVariant.String)])
    layer_street.updateFields()

    #Basisattribute ermitteln
    id_width = layer_street.fields().indexOf('width:carriageway')
    id_source_width = layer_street.fields().indexOf('source:width')

    #Fahrbahnbreite ermitteln
    for feature in layer_street.getFeatures():
        width = NULL
        source_width = NULL

        wd = layer_street.fields().indexOf('width')
        wd_car = layer_street.fields().indexOf('width:carriageway')
        wd_est = layer_street.fields().indexOf('est_width')
        constr = layer_street.fields().indexOf('construction')

        #Mögliche vorhandene Breitenattribute prüfen: width:carriageway, width, est_width
        if wd_car != -1:
            width = feature.attribute('width:carriageway')
            source_width = 'OSM (width:carriageway)'
        if width == NULL and wd != -1 :
            width = feature.attribute('width')
            source_width = 'OSM (width)'
        if width == NULL and wd_est != -1:
            if wd_est != -1:
                width = feature.attribute('est_width')
                source_width = 'OSM (est_width)'

        #Einheiten korrigieren
        if width != NULL:
            unit_list = ['cm', 'm', ' cm', ' m']
            for unit in unit_list:
                if unit in str(width):
                    width = width[:len(width) - len(unit)]
                    if 'cm' in unit:
                        width = int(width) / 100

        #Ansonsten Breite aus anderen Straßenattributen abschätzen
        else:
            source_width = 'estimated'
            highway = feature.attribute('highway')
            if highway == 'primary':
                width = width_primary_street
            if highway == 'secondary':
                width = width_secondary_street
            if highway == 'tertiary':
                width = width_tertiary_street
            #bei Hauptstraßen als Einbahnstraße: halbe Breite annehmen
            if layer_street.fields().indexOf('oneway') != -1:
                if feature.attribute('oneway') == 'yes' and width != NULL:
                    width = width / 2

            if highway in is_service_list:
                width = width_service
                if layer_street.fields().indexOf('service') != -1:
                    if feature.attribute('service') == 'driveway':
                        width = width_driveway
            if highway == 'construction':
                if constr:
                    construction = feature.attribute('highway')
                    if construction == 'primary':
                        width = width_primary_street
                    if construction == 'secondary':
                        width = width_secondary_street
                    if construction == 'tertiary':
                        width = width_tertiary_street
                    #bei Hauptstraßen als Einbahnstraße: halbe Breite annehmen
                    if layer_street.fields().indexOf('oneway') != -1:
                        if feature.attribute('oneway') == 'yes'  and width != NULL:
                            width = width / 2

                    if construction in is_service_list:
                        width = width_service

            if width == NULL:
                width = width_minor_street
        layer_street.changeAttributeValue(feature.id(), id_width, width)
        layer_street.changeAttributeValue(feature.id(), id_source_width, source_width)

    layer_street.commitChanges()

    return([layer_street, layer_path, layer_crossing])



def clearAttributes(layer, attributes):
#-------------------------------------------------------------------------------
#   Attributtabelle bereinigen
#-------------------------------------------------------------------------------
    layer = processing.run('native:retainfields', { 'INPUT' : layer, 'FIELDS' : attributes, 'OUTPUT': 'memory:'})['OUTPUT']
    return(layer)



def getDelimitedAttributes(attribute_string, deli_char, var_type):
#-------------------------------------------------------------------------------
#   Spurattribute mit Trennzeichen einzeln auslesen
#-------------------------------------------------------------------------------
    delimiters = [-1]
    for pos, char in enumerate(attribute_string):
        if(char == deli_char):
            delimiters.append(pos)
    #Start- (oben) und Endpunkte des strings ergänzen zur einfacheren Verarbeitung
    delimiters.append(len(attribute_string))

    #einzelne Abbiegespuren in Array speichern und zurückgeben
    attribute_array = []
    for i in range(len(delimiters) - 1):
        attribute = attribute_string[delimiters[i] + 1:delimiters[i + 1]]
        if var_type == 'float' or var_type == 'int':
            if attribute == '' or attribute == NULL:
                attribute = 0

            if var_type == 'float':
                attribute_array.append(float(attribute))
            if var_type == 'int':
                attribute_array.append(int(attribute))
        else:
            attribute_array.append(attribute)
    return(attribute_array)



def offsetVertex(layer_lanes, layer_lanes_single_carriageway, lane_dual, geom, vertex, vertex_x, vertex_y):
#-------------------------------------------------------------------------------
#   Spurführung an Verzweigungsstellen von Zweirichtungsfahrbahnen korrigieren
#   Wird für Straßensegmente mit "dual_carriageway=yes" aufgerufen ("dual"-
#   Segmente), die einen Verzweigungspunkt mit einem anderen solchen Segment
#   bzw. einem vereinigten Straßensegment ("single"-Segment) besitzen.
#-------------------------------------------------------------------------------
    #Winkel am Zweigpunkt des dual carriageways ermitteln
    angle_dual = math.degrees(geom.angleAtVertex(vertex))
    #Winkel des eigentlichen Straßenverlaufs am selben Punkt der gemeinsamen Fahrbahn (single-Segment) ermitteln
    layer_lanes.removeSelection()
    lane_id = lane_dual.id()
    layer_lanes.select(lane_id)
    width_lanes_dual = lanes_dict['width_lanes'][lane_dual.attribute('id')]
    #...dafür zunächst anschließendes (= berührendes) Einrichtungswegstück selektieren
    processing.run('native:selectbylocation', {'INPUT' : layer_lanes_single_carriageway, 'INTERSECT' : QgsProcessingFeatureSourceDefinition(layer_lanes.id(), selectedFeaturesOnly=True), 'METHOD' : 0, 'PREDICATE' : [4]})
    #Segmente deselektieren, die nicht an den zu versetzenden Vertex anschließen (kann bei Segmenten passieren, die beidseitig in einen Verzweigungspunkt münden)
    for lane_single in layer_lanes_single_carriageway.selectedFeatures():
        geom_single = lane_single.geometry()
        start_vertex_single_x = geom_single.vertexAt(0).x()
        start_vertex_single_y = geom_single.vertexAt(0).y()
        vertex_count_single = len(lane_single.geometry().asPolyline())
        end_vertex_single_x = geom_single.vertexAt(vertex_count_single - 1).x()
        end_vertex_single_y = geom_single.vertexAt(vertex_count_single - 1).y()
        if (start_vertex_single_x != vertex_x or start_vertex_single_y != vertex_y) and (end_vertex_single_x != vertex_x or end_vertex_single_y != vertex_y):
            layer_lanes_single_carriageway.deselect(lane_single.id())

    #...und dann Winkel dieses Wegstücks am selben Punkt ermitteln
    dual_carriageway_opposite_direction = NULL
    for lane_single in layer_lanes_single_carriageway.selectedFeatures():
        vertex_count_single = len(lane_single.geometry().asPolyline())
        geom_single = lane_single.geometry()
        start_vertex_single_x = geom_single.vertexAt(0).x()
        start_vertex_single_y = geom_single.vertexAt(0).y()
        if start_vertex_single_x == vertex_x and start_vertex_single_y == vertex_y:
            angle = math.degrees(geom_single.angleAtVertex(0))
            width_lanes_single = lanes_dict['width_lanes'][lane_single.attribute('id')]
            placement_single = lane_single.attribute('placement_abs')
            lanes_single = int(lane_single.attribute('lanes'))
            #Wenn beide Wegstücke an diesem Punkt beginnen, verlaufen sie gegensätzlich – entscheidend für Richtung des Linienversatzes
            if vertex == 0:
               dual_carriageway_opposite_direction = 1
            else:
               dual_carriageway_opposite_direction = 0
        else:
            end_vertex_single_x = geom_single.vertexAt(vertex_count_single - 1).x()
            end_vertex_single_y = geom_single.vertexAt(vertex_count_single - 1).y()
            if end_vertex_single_x == vertex_x and end_vertex_single_y == vertex_y:
                angle = math.degrees(geom_single.angleAtVertex(vertex_count_single - 1))
                width_lanes_single = lanes_dict['width_lanes'][lane_single.attribute('id')]
                placement_single = lane_single.attribute('placement_abs')
                lanes_single = int(lane_single.attribute('lanes'))
                if vertex == 0:
                    dual_carriageway_opposite_direction = 0
                else:
                    dual_carriageway_opposite_direction = 1

#    print("Dual:", lane_dual.attribute('name'), "(", lane_dual.attribute('id'), ")", ",", "Single:", lane_single.attribute('name'), "(", lane_single.attribute('id'), ")")

    #Distanz der Abweichung ermitteln, unter Berücksichtigung der Spuranzahl, Spurbreite und Spurlage (placement)
    i = len(placement_single) - placement_single.find(':') - 1
    placement_pos_single = placement_single[0:len(placement_single) - i]
    placement_lane_single = int(placement_single[len(placement_single) - i:len(placement_single)])
    placement_dual = lane.attribute('placement_abs')
    i = len(placement_dual) - placement_dual.find(':') - 1
    placement_pos_dual = placement_dual[0:len(placement_dual) - i]
    placement_lane_dual = int(placement_dual[len(placement_dual) - i:len(placement_dual)])
    lanes_dual = int(lane.attribute('lanes'))
    lanes_single_forward = int(lane_single.attribute('lanes:forward'))
    lanes_single_backward = int(lane_single.attribute('lanes:backward'))

    #relativen placement-Unterschied in Fahrtrichtung ermitteln und dabei eine normierte placement-Skala nutzen:
    #0 (links der linkesten/ersten Spur), 0.5 (Mitte der ersten Spur), 1 (rechts der ersten Spur), 1.5 (Mitte der zweiten Spur) etc.
    #oder auch: -0.5 (Mitte der entgegengesetzen Spur links der ersten Spur) etc.

    #normierten placement-Wert für das dual_carriageway-Segment ("dual*") ermitteln
    placement_dual = placement_lane_dual
    if placement_pos_dual == 'left_of:':
        placement_dual -= 1
    if placement_pos_dual == 'middle_of:':
        placement_dual -= 0.5

    #normierten placement-Wert für das vereinigte Segment ("single*") ermitteln (in der passenden Fahrtrichtung)
    if not dual_carriageway_opposite_direction: #Entweder für ablaufenden Zweig, falls gemeinsames Segment zum Zweigpunkt hinführt oder für zulaufenden Zweig, wenn gemeinsames Segment vom Zweigpunkt wegführt
        placement_single = placement_lane_single
        placement_single -= lanes_single_backward #da die zuvor ermittelten placement-Werte absolute Werte (unabhängig der Fahrtrichtung) darstellen, müssen sie für eine relative Betrachtung zunächst auf die betrachtete Fahrtrichtung bezogen werden

    else: #Entweder für ablaufenden Zweig, falls gemeinsames Segment vom Zweigpunkt wegführt oder für zulaufenden Zweig, wenn gemeinsames Segment zum Zweigpunkt hinführt
        #relative placement in Fahrtrichtung durch Invertierung der absoluten placement unter Ausschluss der backward-Spuren ermitteln
        placement_single = lanes_single_backward + 1 - placement_lane_single
        if placement_pos_single == 'left_of:':
            placement_pos_single = 'right_of:'
        elif placement_pos_single == 'right_of:':
            placement_pos_single = 'left_of:'
        angle += 180

    if placement_pos_single == 'left_of:':
        placement_single -= 1
    if placement_pos_single == 'middle_of:':
        placement_single -= 0.5

#    print("pos_dual:", placement_dual, "pos_single:", placement_single, "(=", placement_dual - placement_single, ")")

    #normierter placement-Unterschied zwischen dual- und single-Segment
    placement_diff = placement_dual - placement_single

    #Distanz der Abweichung ermitteln (unter Berücksichtigung hinterlegter Spurbreiten)
    width_lanes = []
    distance = 0
    if placement_diff > 0:
        if not dual_carriageway_opposite_direction:
            lanes_single_directed = lanes_single_forward
            width_lanes = width_lanes_single[lanes_single_backward:]
        else:
            lanes_single_directed = lanes_single_backward
            width_lanes = width_lanes_single[:lanes_single_backward][::-1]

        #Wenn das single-Segment in Fahrtrichtung weniger Spuren hat als das dual-Segment, muss die Spurbreitenliste ergänzt werden um die Breiten der "überhängenden" Spuren des dual-Segments
        if len(width_lanes) < placement_diff:
            width_lanes += width_lanes_dual[lanes_single_directed:]

        i = 0
        diff_forward = placement_diff
        if placement_single < 0:
            diff_forward -= abs(placement_single)
        while i < diff_forward:
            j = math.floor(i) #Liste in halben Spuren durchgehen und jeweilige (halbe) Breite addieren
            distance += width_lanes[j] / 2
            i += 0.5

    #Wenn highway-Linie im Gegenverkehr liegt (also der normierte placement-Wert des single-Segments negativ ist), die Distanz um die entsprechenden Spurbreiten erhöhen
    if placement_single < 0:
        width_lanes_single_reverse = width_lanes_single[:lanes_single_directed:-1]
        i = 0
        while i < abs(placement_single):
            j = math.floor(i)
            distance += width_lanes_single_reverse[j] / 2
            i += 0.5

#    print(width_lanes, distance)
#    print("-------------------------------------------------")

    #Versatz in x- und y-Richtung ermitteln
    xv = math.sin(math.radians(90 - angle)) * distance
    yv = math.cos(math.radians(90 + angle)) * distance

    return([xv, yv])



def offsetLaneTransition(layer, lane, distance, fix):
#--------------------------------------------------------------------------------------------------
#   Ein Wegsegment in eine Richtung zunehmend um eine Distanz verschieben (placement=transition)
#--------------------------------------------------------------------------------------------------
#    layer.startEditing()
    geom = lane.geometry()
    vertex_count = getVertexCount(geom)

    for vertex in range(vertex_count):
        vertex_x = geom.vertexAt(vertex).x()
        vertex_y = geom.vertexAt(vertex).y()
        #print(lane.attribute('id'), vertex_count, vertex, geom.distanceToVertex(vertex_count - 1), geom.distanceToVertex(vertex))

        angle = math.degrees(geom.angleAtVertex(vertex))
        lane_distance = geom.distanceToVertex(vertex_count - 1)

        #fix = 0: Segment bleibt am ersten Vertex verankert, fix = 1: Segment bleibt am letzten Vertex verankert
        if fix == 0:
            vertex_distance = geom.distanceToVertex(vertex)
        else:
            vertex_distance = lane_distance - geom.distanceToVertex(vertex)

        distance_part = vertex_distance / lane_distance

        #Versatz in x- und y-Richtung ermitteln
        xv = math.sin(math.radians(90 - angle)) * (distance * distance_part)
        yv = math.cos(math.radians(90 + angle)) * (distance * distance_part)

        layer.moveVertex(vertex_x + xv, vertex_y + yv, lane.id(), vertex)
#    layer.commitChanges()
    return(True)



def getConnectedSegments(layer, feature, vertex):
#-------------------------------------------------------------------------------------------------------
#   An einem bestimmten Vertex einer Linie angrenzende andere Liniensegmente eines Layers zurückgeben
#   Achtung: layer muss vorher bereits als MapLayer geadded worden sein!
#-------------------------------------------------------------------------------------------------------
    #mögliche Auswahl speichern, um diese am Ende wieder herzustellen/nicht zu ändern
    selection_ids = layer.selectedFeatureIds()
    layer.removeSelection()
    layer.select(feature.id())
    layer_vertex = processing.run('native:extractspecificvertices', { 'INPUT' : QgsProcessingFeatureSourceDefinition(layer.id(), selectedFeaturesOnly=True), 'VERTICES' : str(vertex), 'OUTPUT': 'memory:'})['OUTPUT']
    processing.run('native:selectbylocation', {'INPUT' : layer, 'INTERSECT' : layer_vertex, 'METHOD' : 0, 'PREDICATE' : [4]})
    #Ursprungsfeature selbst nicht mit auswählen/zurückgeben
    for connected_feature in layer.selectedFeatures():
        if connected_feature.id() == feature.id():
            layer.deselect(feature.id())
    connected_features = layer.selectedFeatures()
    #eventuelle ursprüngliche Layer-Auswahl wiederherstellen
    layer.removeSelection()
    layer.selectByIds(selection_ids)
    return connected_features



def getVertexCount(geom):
#------------------------------------------------------------
#   Gibt die Anzahl der Stützpunkte einer Geometrie zurück
#------------------------------------------------------------
    if geom.isMultipart():
        vertices = geom.asMultiPolyline()
        vertex_count = [len(v) for v in vertices][0]
    else:
        vertices = geom.asPolyline()
        vertex_count = len(vertices)
    return vertex_count



def getAbsolutePlacement(lanes, lanes_backward, placement, placement_forward, placement_backward, l_extra):
#---------------------------------------------------------------------
#   Ermittelt einen absoluten, richtungsunabhängigen placement-Wert
#---------------------------------------------------------------------

    l_f = l_b = 0
    if placement_forward:
        placement = placement_forward
        l_f = lanes_backward

    if placement_backward:
        if placement_backward.find(':') == -1:
            return(placement_backward)
        i = -(len(placement_backward) - placement_backward.find(':') - 1)

        placement = placement_backward
        l_b = int(placement_backward[i:])
        l_b = lanes_backward - (l_b - 1)
        if 'left_of:' in placement_backward:
            l_b += 1
        if 'right_of:' in placement_backward:
            l_b -= 1

    if placement == NULL:
        #ungerade Spurzahl
        if lanes % 2:
            placement = 'middle_of:' + str(round((lanes / 2) + 0.1)) #+0.1, da round() nicht "echt" rundet
        else:
            placement = 'left_of:' + str(int((lanes / 2) + 1))

    if placement.find(':') == -1:
        return(placement)
    i = -(len(placement) - placement.find(':') - 1)

    l = int(placement[i:])
    l += l_f
    if l_b:
        l = l_b

    l += l_extra

    placement = placement[0:i] + str(l)
    return(placement)



#--------------------------------
#      S c r i p t   S t a r t
#--------------------------------
print(time.strftime('%H:%M:%S', time.localtime()), 'Starte Post-processing:')

#------------------------------------------------------------------------------------------------
# Fahrbahnbezogene Eigenschaften von Querungsstellen mit Markierungen ermitteln und übertragen
#------------------------------------------------------------------------------------------------
if proc_crossings:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Verarbeite Querungsstellen...')
    #Straßenbezogene Layer einladen und vorbereiten

    print(time.strftime('%H:%M:%S', time.localtime()), '   Bereite Straßendaten vor...')
    if not layer_raw_highway_ways:
        layer_raw_highway_ways = QgsVectorLayer(data_dir + 'highway.geojson|geometrytype=LineString', 'highway (raw)', 'ogr')
    if not layer_raw_path_ways:
        layer_raw_path_ways = QgsVectorLayer(data_dir + 'path.geojson|geometrytype=LineString', 'path (raw)', 'ogr')
    if not layer_raw_highway_points:
        layer_raw_highway_points = QgsVectorLayer(data_dir + 'highway.geojson|geometrytype=Point', 'highway (raw)', 'ogr')
    layer_crossing = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_highway_points, 'EXPRESSION' : '"highway" IS \'crossing\' AND ("crossing" IS NOT \'unmarked\' OR "crossing:buffer_marking" IS NOT NULL)', 'OUTPUT': 'memory:'})['OUTPUT']

    layers = prepareLayers(layer_raw_highway_ways, layer_raw_path_ways, layer_crossing)
    if layers:
        layer_street = layers[0]
        layer_path = layers[1]
        layer_crossing = layers[2]

        #Straßen-Schnittpunkteigenschaften erheben
        layer_intersections = processing.run('native:lineintersections', {'INPUT': layer_street, 'INTERSECT': layer_path, 'INPUT_FIELDS' : ['highway'], 'INTERSECT_FIELDS_PREFIX': 'crossing:', 'OUTPUT': 'memory:'})['OUTPUT']

        #Winkel an Übergängen berechnen
        layer_vertices = processing.run('native:extractvertices', {'INPUT': layer_street, 'OUTPUT': 'memory:'})['OUTPUT']

        print(time.strftime('%H:%M:%S', time.localtime()), '   Eigenschaften auf Querungsstellen übertragen...')
        print(time.strftime('%H:%M:%S', time.localtime()), '      (1/3 Straßenbreite)...')
        #Straßenbreite
        layer_crossing = processing.run('native:joinattributesbylocation', {'INPUT': layer_crossing, 'JOIN' : layer_street, 'JOIN_FIELDS' : ['width:carriageway', 'oneway'], 'METHOD' : 1, 'OUTPUT': 'memory:'})['OUTPUT']
        print(time.strftime('%H:%M:%S', time.localtime()), '      (2/3 Straßeneigenschaften)...')
        #Straßeneigenschaften
        layer_crossing = processing.run('native:joinattributesbylocation', {'INPUT': layer_crossing, 'JOIN' : layer_intersections, 'JOIN_FIELDS' : ['crossing:highway'], 'OUTPUT': 'memory:'})['OUTPUT']
        print(time.strftime('%H:%M:%S', time.localtime()), '      (3/3 Winkel)...')
        #Winkel
        layer_crossing = processing.run('native:joinattributesbylocation', {'INPUT': layer_crossing, 'JOIN' : layer_vertices, 'JOIN_FIELDS' : ['angle'], 'OUTPUT': 'memory:'})['OUTPUT']

        print(time.strftime('%H:%M:%S', time.localtime()), '   Querungsstellendaten bereinigen...')
        crossing_attr_list = [
        'id',
        'highway',
        'crossing',
        'crossing_ref',
        'crossing:island',
        'crossing:markings',
        'crossing:kerb_extension',
        'crossing:buffer_marking',
        'tactile_paving',
        'kerb',
        'traffic_signals',
        'traffic_signals:sound',
        'traffic_signals:vibration',
        'supervised',
        'wheelchair',
        'mapillary',
        'direction',
        'traffic_signals:direction',
        'crossing:direction:angle',
        'stop_line:angle',
        'crossing:highway',
        'width:carriageway',
        'oneway',
        'angle',
        'temporary']
        layer_crossing = clearAttributes(layer_crossing, crossing_attr_list)
        layer_crossing = processing.run('native:deleteduplicategeometries', {'INPUT': layer_crossing, 'OUTPUT' : proc_dir + 'crossing.geojson' })

    del layers; del layer_crossing; del layer_intersections; del layer_path; del layer_street; del layer_vertices
    QgsProject.instance().clear()



#-------------------------------------------------------------------------
# Querungsstellen mit randseitigen Markierungen am Bordstein ausrichten
#-------------------------------------------------------------------------
#TODO: Eleganter lösen. Bei vorhandenen crossing-Ways auf jeweiliger Seite (left/right/both) nach kerbs suchen und dort einrasten, oder, falls nicht vorhanden, wie gehabt in die Richtung verschieben und dann am nächsten Punkt der kerb-Linie einrasten.

if proc_cr_markings:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Querungsstellen ausrichten...')
    layer_crossing = QgsVectorLayer(proc_dir + 'crossing.geojson|geometrytype=Point', 'Querungsstellen', 'ogr')
    layer_crossing = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_crossing, 'EXPRESSION' : '"crossing:buffer_marking" IS NOT NULL', 'OUTPUT': 'memory:'})['OUTPUT']
    if not layer_raw_path_ways:
        layer_raw_path_ways = QgsVectorLayer(data_dir + 'path.geojson|geometrytype=LineString', 'path (raw)', 'ogr')
    layer_crossing_ways = processing.run('native:reprojectlayer', { 'INPUT' : layer_raw_path_ways, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_ways = processing.run('native:extractbylocation', { 'INPUT' : layer_crossing_ways, 'INTERSECT' : layer_crossing, 'PREDICATE' : [0], 'OUTPUT': 'memory:'})['OUTPUT']
    print(time.strftime('%H:%M:%S', time.localtime()), '   Ausrichtungswinkel bestimmen...')
    #Schnittwinkel berechnen und auf crossings übertragen
    layer_vertices = processing.run('native:extractvertices', {'INPUT': layer_crossing_ways, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing = processing.run('native:joinattributesbylocation', {'INPUT': layer_crossing, 'JOIN' : layer_vertices, 'JOIN_FIELDS' : ['angle'], 'PREFIX' : 'crossing:', 'METHOD' : 1, 'PREDICATE' : [2], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing = processing.run('native:addfieldtoattributestable', {'INPUT': layer_crossing, 'FIELD_LENGTH' : 6, 'FIELD_NAME' : 'highway:angle', 'FIELD_PRECISION' : 3, 'FIELD_TYPE' : 1, 'OUTPUT': 'memory:'})['OUTPUT']

    with edit(layer_crossing):
        for crossing in layer_crossing.getFeatures():
            angle = NULL
            highway_angle = crossing.attribute("angle")
            crossing_angle = crossing.attribute("crossing:angle")
            #keine kreuzende Querungslinie? Straßenrichtung nehmen
            if crossing_angle == NULL:
                angle = highway_angle
            else:
                crossing_angle += 90
                if abs(crossing_angle - highway_angle) > 270:
                    crossing_angle -= 360
                if abs(crossing_angle - highway_angle) > 90:
                    crossing_angle += 180
                if crossing_angle >= 360:
                    crossing_angle -= 360
                angle = crossing_angle
            layer_crossing.changeAttributeValue(crossing.id(), layer_crossing.fields().indexOf('angle'), angle)
            layer_crossing.changeAttributeValue(crossing.id(), layer_crossing.fields().indexOf('crossing:angle'), crossing_angle)
            layer_crossing.changeAttributeValue(crossing.id(), layer_crossing.fields().indexOf('highway:angle'), highway_angle)

    #Querungsstellen nach Straßenseite herausfiltern (rechts, links, beide)
    print(time.strftime('%H:%M:%S', time.localtime()), '   Randseitige Markierungen versetzen...')
    layer_crossing_markings_left = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_crossing, 'EXPRESSION' : '"crossing:buffer_marking" = \'left\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_markings_right = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_crossing, 'EXPRESSION' : '"crossing:buffer_marking" = \'right\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_markings_both = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_crossing, 'EXPRESSION' : '"crossing:buffer_marking" = \'both\'', 'OUTPUT': 'memory:'})['OUTPUT']

    #crossing-Nodes entsprechend der Richtung der Markierungen in Richtung Bordstein versetzen
    #Versatz um 1/3 der Straßenbreite in Richtung Bordstein – genaue Ausrichtung dann später per Snapping
    #zunächst für einseitige Markierungen (links und rechts)
    layer_crossing_markings_left = processing.run('native:translategeometry', {'INPUT' : layer_crossing_markings_left, 'DELTA_X' : QgsProperty.fromExpression('-cos(angle * (pi() / 180)) * "width:carriageway" / 3'), 'DELTA_Y' : QgsProperty.fromExpression('sin(angle * (pi() / 180)) * "width:carriageway" / 3'), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_markings_left.setName('left')
    layer_crossing_markings_right = processing.run('native:translategeometry', {'INPUT' : layer_crossing_markings_right, 'DELTA_X' : QgsProperty.fromExpression('cos(angle * (pi() / 180)) * "width:carriageway" / 3'), 'DELTA_Y' : QgsProperty.fromExpression('-sin(angle * (pi() / 180)) * "width:carriageway" / 3'), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_markings_right.setName('right')
    #dann für beidseitige Markierungen (je nach links und rechts)
    layer_crossing_markings_both_left = processing.run('native:translategeometry', {'INPUT' : layer_crossing_markings_both, 'DELTA_X' : QgsProperty.fromExpression('-cos(angle * (pi() / 180)) * "width:carriageway" / 3'), 'DELTA_Y' : QgsProperty.fromExpression('sin(angle * (pi() / 180)) * "width:carriageway" / 3'), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_markings_both_left.setName('left')
    layer_crossing_markings_both_right = processing.run('native:translategeometry', {'INPUT' : layer_crossing_markings_both, 'DELTA_X' : QgsProperty.fromExpression('cos(angle * (pi() / 180)) * "width:carriageway" / 3'), 'DELTA_Y' : QgsProperty.fromExpression('-sin(angle * (pi() / 180)) * "width:carriageway" / 3'), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_markings_both_right.setName('right')

    #Punkte von einseitigen und beidseitigen Markierungen zusammenführen
    layer_crossing_buffer_markings = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_crossing_markings_left, layer_crossing_markings_right, layer_crossing_markings_both_left, layer_crossing_markings_both_right], 'OUTPUT': 'memory:'})['OUTPUT']

    #Punkte am Bordstein einrasten
    print(time.strftime('%H:%M:%S', time.localtime()), '   Randseitige Markierungen snappen (1/2)...')
    if not layer_raw_kerb_street_areas_polygons:
        #layer_raw_kerb_street_areas_polygons = QgsVectorLayer(data_dir + 'kerb/kerb_street_areas.geojson|geometrytype=Polygon', 'Fahrbahnbereiche (raw)', 'ogr')
        layer_raw_kerb_street_areas_polygons = createStreetAreaPolygons()
    layer_kerb_lines = processing.run('native:polygonstolines', { 'INPUT' : layer_raw_kerb_street_areas_polygons, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_buffer_markings_snapped = processing.run('native:snapgeometries', { 'BEHAVIOR' : 1, 'INPUT' : layer_crossing_buffer_markings, 'REFERENCE_LAYER' : layer_kerb_lines, 'TOLERANCE' : 8, 'OUTPUT': 'memory:'})['OUTPUT']

    #Wenn kein Snapping stattgefunden hat, noch einmal verschieben (betrifft seltene weit aufgefächerte Kreuzungen)
    print(time.strftime('%H:%M:%S', time.localtime()), '   Randseitige Markierungen snappen (2/2)...')
    layer_crossing_buffer_markings_unsnapped = processing.run('native:extractbylocation', { 'INPUT' : layer_crossing_buffer_markings_snapped, 'INTERSECT' : layer_crossing_buffer_markings, 'PREDICATE' : [3], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_buffer_markings_snapped = processing.run('native:extractbylocation', { 'INPUT' : layer_crossing_buffer_markings_snapped, 'INTERSECT' : layer_crossing_buffer_markings, 'PREDICATE' : [2], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_buffer_markings_unsnapped = processing.run('native:translategeometry', {'INPUT' : layer_crossing_buffer_markings_unsnapped, 'DELTA_X' : QgsProperty.fromExpression('if("layer" IS \'left\', -1 ,1) * cos(angle * (pi() / 180)) * 8'), 'DELTA_Y' : QgsProperty.fromExpression('if("layer" IS \'left\', 1 ,-1) * sin(angle * (pi() / 180)) * 8'), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_buffer_markings_unsnapped = processing.run('native:snapgeometries', { 'BEHAVIOR' : 1, 'INPUT' : layer_crossing_buffer_markings_unsnapped, 'REFERENCE_LAYER' : layer_kerb_lines, 'TOLERANCE' : 8, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_buffer_markings = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_crossing_buffer_markings_snapped, layer_crossing_buffer_markings_unsnapped], 'OUTPUT': 'memory:'})['OUTPUT']

    #Feinjustierung: An nahegelegenen kerbs einrasten
    print(time.strftime('%H:%M:%S', time.localtime()), '   Randseitige Markierungen feinjustieren (1/2)...')
    #Bordsteinlinienpunkte einladen ("kerb" werden - unabhängig von "barrier" - explizit im highway-Layer mitgeliefert)
    if not layer_raw_highway_points:
        layer_raw_highway_points = QgsVectorLayer(data_dir + 'highway.geojson|geometrytype=Point', 'highway (raw)', 'ogr')
    #Bordsteinpunkte herausfiltern
    layer_kerb_nodes = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_highway_points, 'EXPRESSION' : '"kerb" IS NOT NULL', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_kerb_nodes = processing.run('native:reprojectlayer', { 'INPUT' : layer_kerb_nodes, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_buffer_markings = processing.run('native:snapgeometries', { 'BEHAVIOR' : 1, 'INPUT' : layer_crossing_buffer_markings, 'REFERENCE_LAYER' : layer_kerb_nodes, 'TOLERANCE' : 2, 'OUTPUT': 'memory:'})['OUTPUT']

    #noch einmal an Bordsteinkanten einrasten (Fahrbahnlayer (noch) nicht mit OSM-Bordsteinlayer identisch, daher notwendig)
    print(time.strftime('%H:%M:%S', time.localtime()), '   Randseitige Markierungen feinjustieren (2/2)...')
    layer_crossing_buffer_markings = processing.run('native:snapgeometries', { 'BEHAVIOR' : 1, 'INPUT' : layer_crossing_buffer_markings, 'REFERENCE_LAYER' : layer_kerb_lines, 'TOLERANCE' : 2, 'OUTPUT': 'memory:'})['OUTPUT']
    #Winkel des Bordsteins an dieser Stelle ermitteln
    print(time.strftime('%H:%M:%S', time.localtime()), '   Bordsteinwinkel übertragen...')
    #Berechnung auf notwendige Bordsteinsegmente reduzieren
    layer_kerb_lines = processing.run('native:explodelines', { 'INPUT' : layer_kerb_lines, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_buffer_markings_buffer = processing.run('native:buffer', { 'INPUT' : layer_crossing_buffer_markings, 'DISTANCE' : 0.1, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_kerb_lines = processing.run('native:extractbylocation', { 'INPUT' : layer_kerb_lines, 'INTERSECT' : layer_crossing_buffer_markings_buffer, 'PREDICATE' : [0], 'OUTPUT': 'memory:'})['OUTPUT']
    #Bordsteinrichtung ermitteln und Winkel des nächsten Bordsteinsegments übertragen (durch snapping liegen die Punkte nicht exakt auf den Linien)
    layer_kerb_lines = processing.run('qgis:fieldcalculator', { 'INPUT': layer_kerb_lines, 'FIELD_NAME': 'angle', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 6, 'FIELD_PRECISION': 3, 'NEW_FIELD': True, 'FORMULA': 'line_interpolate_angle($geometry,0)', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_buffer_markings = processing.run('native:joinbynearest', {'INPUT': layer_crossing_buffer_markings, 'INPUT_2' : layer_kerb_lines, 'FIELDS_TO_COPY' : ['angle'], 'PREFIX' : 'kerb:', 'MAX_DISTANCE' : 0.1, 'NEIGHBORS' : 1, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_buffer_markings = clearAttributes(layer_crossing_buffer_markings, ['id', 'highway:angle', 'crossing:angle', 'kerb:angle', 'layer'])
    #QuickAndDirty Workaround: An gleicher Position entstandene Punkte löschen
    layer_crossing_buffer_markings = processing.run('native:deleteduplicategeometries', {'INPUT': layer_crossing_buffer_markings, 'OUTPUT' : proc_dir + 'crossing_buffer_markings.geojson' })

    del layer_crossing; del layer_crossing_buffer_markings; del layer_crossing_buffer_markings_buffer; del layer_crossing_buffer_markings_snapped; del layer_crossing_buffer_markings_unsnapped; del layer_crossing_markings_both; del layer_crossing_markings_both_left; del layer_crossing_markings_both_right; del layer_crossing_markings_left; del layer_crossing_markings_right; del layer_crossing_ways; del layer_kerb_lines; del layer_kerb_nodes; del layer_vertices
    QgsProject.instance().clear()



#-----------------------------------------------------
# Linien markierter Gehweg-Querungsstellen erzeugen
#-----------------------------------------------------
if proc_cr_lines:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Markierungen an Querungsstellen erzeugen...')
    print(time.strftime('%H:%M:%S', time.localtime()), '   Datensätze laden...')
    layer_crossing = QgsVectorLayer(proc_dir + 'crossing.geojson|geometrytype=Point', 'Querungsstellen', 'ogr')
    if not layer_raw_path_ways:
        layer_raw_path_ways = QgsVectorLayer(data_dir + 'path.geojson|geometrytype=LineString', 'path (raw)', 'ogr')
    layer_crossing_path = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_path_ways, 'EXPRESSION' : '"footway" = \'crossing\' AND "crossing" IS NOT \'unmarked\' AND "crossing:markings" IS NOT \'no\' AND "crossing:markings" IS NOT \'surface\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_path = processing.run('native:reprojectlayer', { 'INPUT' : layer_crossing_path, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']

    if not layer_raw_kerb_street_areas_polygons:
        #layer_raw_kerb_street_areas_polygons = QgsVectorLayer(data_dir + 'kerb/kerb_street_areas.geojson|geometrytype=Polygon', 'Fahrbahnbereiche (raw)', 'ogr')
        layer_raw_kerb_street_areas_polygons = createStreetAreaPolygons()
    layer_carriageway = layer_raw_kerb_street_areas_polygons

    #QgsProject.instance().addMapLayer(layer_carriageway, False)

    #bestimmte Straßen-/crossing-Eigenschaften an querende Linien übergeben (relevant zur späteren Darstellung spezieller Fälle wie schrägen Zebrastreifen oder Kürzung im Bereich von randseitigen Markierungen)
    layer_crossing_path = processing.run('native:joinattributesbylocation', {'INPUT': layer_crossing_path, 'JOIN' : layer_crossing, 'JOIN_FIELDS' : ['crossing', 'crossing:markings', 'crossing_ref', 'angle', 'crossing:buffer_marking'], 'PREFIX' : 'highway:', 'OUTPUT': 'memory:'})['OUTPUT']

    #noch einmal filtern und nur markierte Querungsstellen behalten (Ampeln, Zebrastreifen, sonstige "marked" crossings außer crossing:markings=surface)
    layer_crossing_path = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_crossing_path, 'EXPRESSION' : '"crossing" = \'marked\' OR "crossing" = \'traffic_signals\' OR "crossing" = \'zebra\' OR "crossing_ref" = \'zebra\' OR ("crossing:markings" IS NOT NULL AND "crossing:markings" IS NOT \'no\' AND "crossing:markings" IS NOT \'surface\') OR "highway:crossing" = \'marked\' OR "highway:crossing" = \'traffic_signals\' OR "highway:crossing" = \'zebra\' OR "highway:crossing_ref" = \'zebra\' OR ("highway:crossing:markings" IS NOT NULL AND "highway:crossing:markings" IS NOT \'no\' AND "highway:crossing:markings" IS NOT \'surface\')', 'OUTPUT': 'memory:'})['OUTPUT']

    QgsProject.instance().addMapLayer(layer_crossing, False)
    QgsProject.instance().addMapLayer(layer_crossing_path, False)

    #Tagging reduzieren und vereinheitlichen (crossing, crossing_ref, crossing:markings)
    print(time.strftime('%H:%M:%S', time.localtime()), '   Lineare Querungen ermitteln (Eigenschaften vereinheitlichen)...')

    id_crossing = layer_crossing_path.fields().indexOf('crossing')
    id_crossing_ref = layer_crossing_path.fields().indexOf('crossing_ref')
    id_crossing_markings = layer_crossing_path.fields().indexOf('crossing:markings')
    id_highway_crossing = layer_crossing_path.fields().indexOf('highway:crossing')
    id_highway_crossing_ref = layer_crossing_path.fields().indexOf('highway:crossing_ref')
    id_highway_crossing_markings = layer_crossing_path.fields().indexOf('highway:crossing:markings')

    with edit(layer_crossing_path):
        for path in layer_crossing_path.getFeatures():
            vanilla = crossing = crossing_ref = crossing_markings = highway_crossing = highway_crossing_ref = highway_crossing_markings = NULL
            if id_crossing != -1:
                vanilla = crossing = path.attribute('crossing')
            if id_crossing_ref != -1:
                crossing_ref = path.attribute('crossing_ref')
            if id_crossing_markings != -1:
                crossing_markings = path.attribute('crossing:markings')
            if id_highway_crossing != -1:
                highway_crossing = path.attribute('highway:crossing')
            if id_highway_crossing_ref != -1:
                highway_crossing_ref = path.attribute('highway:crossing_ref')
            if id_highway_crossing_markings != -1:
                highway_crossing_markings = path.attribute('highway:crossing:markings')

            if highway_crossing:
                crossing = highway_crossing
            if crossing != 'traffic_signals' and ((crossing_markings != NULL and crossing_markings != 'no') or (highway_crossing_markings != NULL and highway_crossing_markings != 'no')):
                crossing = 'marked'
            if vanilla == 'zebra' or highway_crossing == 'zebra' or crossing_ref == 'zebra' or highway_crossing_ref == 'zebra' or crossing_markings == 'zebra' or highway_crossing_markings == 'zebra':
                crossing = 'zebra'

            #Segmente löschen, die nicht ins Schema passen, falls welche übrig geblieben sind
            if crossing != 'marked' and crossing != 'traffic_signals' and crossing != 'zebra':
                layer_crossing_path.deleteFeature(path.id())
                continue
            if crossing_markings == 'surface' or highway_crossing_markings == 'surface':
                layer_crossing_path.deleteFeature(path.id())
                continue

            if vanilla != crossing:
                layer_crossing_path.changeAttributeValue(path.id(), layer_crossing_path.fields().indexOf('crossing'), crossing)

    print(time.strftime('%H:%M:%S', time.localtime()), '   Lineare Querungen ermitteln (Wegstücke ermitteln)...')

    layer_vertices = processing.run('native:extractvertices', {'INPUT': layer_crossing_path, 'OUTPUT': 'memory:'})['OUTPUT']
    QgsProject.instance().addMapLayer(layer_vertices, False)

    #alle crossing-Punkte auswählen, die für spätere Markierungen in Frage kommen
    layer_crossing = processing.run('qgis:extractbyexpression', {'INPUT' : layer_crossing, 'EXPRESSION' : '"crossing:highway" IS NOT \'cycleway\' and "crossing:markings" IS NOT \'no\' and "crossing:markings" IS NOT \'surface\' and ("crossing" = \'traffic_signals\' or "crossing" = \'marked\' or "crossing" = \'zebra\' or "crossing_ref" = \'zebra\' or "crossing:markings" IS NOT NULL)', 'OUTPUT': 'memory:'})['OUTPUT']
    QgsProject.instance().addMapLayer(layer_crossing, False)

    #Die Stützpunkte jedes Weges durchgehen und prüfen, ob die Linien über die crossing-Punkte hinausgehen (also vermutlich bis zum Bordstein)
    #für jeden Weg Anzahl der Stützpunkte = maximalen Stützpunkt-Index ermitteln
    #TODO: Einfachere und schnellere Möglichkeit: crossings explodieren und prüfen, ob an crossing-Nodes mehr als eine Linie anschließt

    with edit(layer_crossing_path):
        for path in layer_crossing_path.getFeatures():
            id = path.attribute('id')
            crossing = path.attribute('crossing')
            processing.run('qgis:selectbyattribute', {'INPUT' : layer_vertices, 'FIELD' : 'id', 'VALUE' : id })
            vertex_max_index = layer_vertices.selectedFeatureCount() - 1

            #Alle Stützpunkte des Weges auswählen, die auch crossing-Punkte sind
            processing.run('native:selectbylocation', {'INPUT' : layer_vertices, 'INTERSECT' : layer_crossing, 'METHOD' : 2, 'PREDICATE' : [3]})
            draw_lines = 1
            for vertex in layer_vertices.selectedFeatures():
                index = vertex.attribute('vertex_index')
                #Keine Markierungslinien aus Wegelinie ableiten, wenn diese nicht durchgängig ist (sondern an der Straßenlinie endet)
                if index == vertex_max_index or index == 0:
                    draw_lines = 0
                    #nach anschließenden Wegesegmenten mit gleichen Eigenschaften, aber anderer ID suchen, um Weg evtl. doch zu berücksichtigen
                    layer_crossing_path.removeSelection()
                    layer_crossing_path.select(path.id())
                    processing.run('native:selectbylocation', {'INPUT' : layer_crossing_path, 'INTERSECT' : QgsProcessingFeatureSourceDefinition(layer_crossing_path.id(), selectedFeaturesOnly=True), 'METHOD' : 0, 'PREDICATE' : [4]})
                    for ongoing_path in layer_crossing_path.selectedFeatures():
                        if crossing == ongoing_path.attribute('crossing'):
                            draw_lines = 1

            #print(id, ' | draw: ', draw_lines, ' | vertex: ', index, ' | vertex_max: ', vertex_max_index)

            if draw_lines == 1:
                #crossing-Punkte mit durchgängigen Wegelinien aus der Auswahl für spätere Linienerzeugung entfernen
                processing.run('native:selectbylocation', {'INPUT' : layer_crossing, 'INTERSECT' : QgsProcessingFeatureSourceDefinition(layer_vertices.id(), selectedFeaturesOnly=True), 'METHOD' : 3, 'PREDICATE' : [3]})
            else:
                #Nicht durchgängige Wegelinien entfernen
                layer_crossing_path.deleteFeature(path.id())

        #weitere crossing-Node-Eigenschaften auf Linien übertragen (z.Zt. nur "temporary"='yes')
        for attr in ['temporary']:
            if layer_crossing_path.fields().indexOf(attr) == -1:
                layer_crossing_path.dataProvider().addAttributes([QgsField(attr, QVariant.String)])
        layer_crossing_path.updateFields()
    layer_crossing_temporary = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_crossing, 'EXPRESSION' : '"temporary" = \'yes\'', 'OUTPUT': 'memory:'})['OUTPUT']

    processing.run('native:selectbylocation', {'INPUT' : layer_crossing_path, 'INTERSECT' : layer_crossing_temporary, 'METHOD' : 0, 'PREDICATE' : [0]})
    with edit(layer_crossing_path):
        for path in layer_crossing_path.selectedFeatures():
            layer_crossing_path.changeAttributeValue(path.id(), layer_crossing_path.fields().indexOf('temporary'), 'yes')

    #an Punkten ohne querende Linie: Querungslinie durch Versatz aus crossing-Node selbst erzeugen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Markierungslinien aus crossing-Nodes ableiten...')

    #alle crossing-Nodes auswählen, die nicht auf einer bereits erzeugten Linie liegen
    layer_crossing.selectAll()
    processing.run('native:selectbylocation', {'INPUT' : layer_crossing, 'INTERSECT' : layer_crossing_path, 'METHOD' : 3, 'PREDICATE' : [0]})

    crossing_line_markings_point1 = processing.run('native:translategeometry', {'INPUT' : QgsProcessingFeatureSourceDefinition(layer_crossing.id(), selectedFeaturesOnly=True), 'DELTA_X' : QgsProperty.fromExpression('-cos(if("crossing:direction:angle", "crossing:direction:angle" + 90, "angle") * (pi() / 180)) * (("width:carriageway" / 2) + 1)'), 'DELTA_Y' : QgsProperty.fromExpression('sin(if("crossing:direction:angle", "crossing:direction:angle" + 90, "angle") * (pi() / 180)) * (("width:carriageway" / 2) + 1)'), 'OUTPUT': 'memory:'})['OUTPUT']
    crossing_line_markings_point2 = processing.run('native:translategeometry', {'INPUT' : QgsProcessingFeatureSourceDefinition(layer_crossing.id(), selectedFeaturesOnly=True), 'DELTA_X' : QgsProperty.fromExpression('cos(if("crossing:direction:angle", "crossing:direction:angle" + 90, "angle") * (pi() / 180)) * (("width:carriageway" / 2) + 1)'), 'DELTA_Y' : QgsProperty.fromExpression('-sin(if("crossing:direction:angle", "crossing:direction:angle" + 90, "angle") * (pi() / 180)) * (("width:carriageway" / 2) + 1)'), 'OUTPUT': 'memory:'})['OUTPUT']

    #Punkte miteinander verbinden
    crossing_line_markings = processing.run('native:hublines', { 'HUBS' : crossing_line_markings_point1, 'HUB_FIELD' : 'id', 'HUB_FIELDS' : ['id'], 'SPOKES' : crossing_line_markings_point2, 'SPOKE_FIELD' : 'id', 'SPOKE_FIELDS' : ['crossing','crossing_ref','temporary'], 'OUTPUT': 'memory:'})['OUTPUT']

    #Einfache Geometrieprüfung: kurze Linien nicht weiter berücksichtigen
    with edit(crossing_line_markings):
        id_crossing = crossing_line_markings.fields().indexOf('crossing')
        id_crossing_ref = crossing_line_markings.fields().indexOf('crossing_ref')
        for line in crossing_line_markings.getFeatures():
            if line.geometry().length() < 1:
                crossing_line_markings.deleteFeature(line.id())

            #Zebra vereinheitlichen
            crossing = NULL
            if id_crossing_ref != -1:
                crossing_ref = line.attribute('crossing_ref')
            if crossing_ref == 'zebra':
                crossing_line_markings.changeAttributeValue(line.id(), id_crossing, 'zebra')

    #aus Node-Daten interpolierte Linien mit Wegelinien zusammenführen
    layer_crossing_lines = processing.run('native:mergevectorlayers', {'LAYERS': [crossing_line_markings, layer_crossing_path], 'OUTPUT': 'memory:'})['OUTPUT']

    #Verbundene Linien vereinigen, um getrennte OSM-Segmente zu vereinigen
    layer_crossing_lines = processing.run('native:dissolve', { 'FIELD' : ['highway', 'crossing', 'crossing_ref', 'temporary', 'width', 'highway:angle', 'highway:crossing:buffer_marking'], 'INPUT' : layer_crossing_lines, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_lines = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_crossing_lines, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_lines = processing.run('native:deleteduplicategeometries', {'INPUT': layer_crossing_lines, 'OUTPUT': 'memory:'})['OUTPUT']

    #Linien pauschal verlängern, um Lücken zu reduzieren
    layer_crossing_lines = processing.run('native:extendlines', { 'INPUT' : layer_crossing_lines, 'START_DISTANCE' : 3, 'END_DISTANCE' : 3, 'OUTPUT': 'memory:'})['OUTPUT']

    #Markierungslinien durch Versatz parallel zur Wegelinie erzeugen (außer Zebrastreifen)
    QgsProject.instance().addMapLayer(layer_crossing_lines, False)
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_crossing_lines, 'EXPRESSION' : '"crossing" IS NOT \'zebra\''})

    layer_crossing_lines1 = processing.run('native:offsetline', {'INPUT': QgsProcessingFeatureSourceDefinition(layer_crossing_lines.id(), selectedFeaturesOnly=True), 'DISTANCE' : QgsProperty.fromExpression('if("width", "width" / 2, 2.5)'), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_lines2 = processing.run('native:offsetline', {'INPUT': QgsProcessingFeatureSourceDefinition(layer_crossing_lines.id(), selectedFeaturesOnly=True), 'DISTANCE' : QgsProperty.fromExpression('if("width", -"width" / 2, -2.5)'), 'OUTPUT': 'memory:'})['OUTPUT']

    #Wegelinien nur als Mittellinien bei Zebrastreifen behalten
    with edit(layer_crossing_lines):
        layer_crossing_lines.deleteSelectedFeatures()

    layer_crossing_lines = processing.run('native:mergevectorlayers', {'LAYERS': [layer_crossing_lines, layer_crossing_lines1, layer_crossing_lines2], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_lines = clearAttributes(layer_crossing_lines, ['id', 'crossing', 'temporary', 'width', 'highway:angle', 'highway:crossing:buffer_marking'])

    print(time.strftime('%H:%M:%S', time.localtime()), '   Markierungslinien zuschneiden...')
    #Querungsmarkierungen beginnen erst 20cm vom Bordstein entfernt
    #Bordsteinlinien puffern und Fahrbahnbereich-Maske entsprechend verkleinern
    layer_kerbs = processing.run('native:polygonstolines', { 'INPUT' : layer_carriageway, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_kerbs = processing.run('native:reprojectlayer', { 'INPUT' : layer_kerbs, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_kerbs = processing.run('native:buffer', { 'INPUT' : layer_kerbs, 'DISTANCE' : 0.2, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_carriageway = processing.run('native:difference', {'INPUT' : layer_carriageway, 'OVERLAY' : layer_kerbs, 'OUTPUT': 'memory:'})['OUTPUT']

    layer_crossing_lines = processing.run('native:clip', {'INPUT': layer_crossing_lines, 'OVERLAY': layer_carriageway, 'OUTPUT': 'memory:'})['OUTPUT']

    #Linien im Bereich randseitiger Markierungen kürzen (betrifft insbes. Zebrastreifen, allerdings selten)
    #TODO: auch "crossing:buffer_protection" einbeziehen?
    layer_buffer_markings = QgsVectorLayer(proc_dir + 'crossing_buffer_markings.geojson|geometrytype=Point', 'randseitige Markierungen', 'ogr')
    layer_buffer_markings = processing.run('native:reprojectlayer', { 'INPUT' : layer_buffer_markings, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    QgsProject.instance().addMapLayer(layer_buffer_markings, False)
    layer_buffer_markings = processing.run('native:buffer', { 'INPUT' : layer_buffer_markings, 'DISTANCE' : 2.5, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_lines = processing.run('native:difference', {'INPUT' : layer_crossing_lines, 'OVERLAY' : layer_buffer_markings, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_lines = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_crossing_lines, 'OUTPUT': 'memory:'})['OUTPUT']

    #sehr kurze Segmente (evtl. Relikte) entfernen
    layer_crossing_lines = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_crossing_lines, 'EXPRESSION' : '$length > 1.25', 'OUTPUT' : proc_dir + 'crossing_line_markings.geojson' })

    QgsProject.instance().removeMapLayer(layer_buffer_markings); QgsProject.instance().removeMapLayer(layer_crossing); QgsProject.instance().removeMapLayer(layer_crossing_lines); QgsProject.instance().removeMapLayer(layer_crossing_path); QgsProject.instance().removeMapLayer(layer_vertices)
    del crossing_line_markings; del crossing_line_markings_point1; del crossing_line_markings_point2; del layer_buffer_markings; del layer_carriageway; del layer_crossing; del layer_crossing_lines; del layer_crossing_lines1; del layer_crossing_lines2; del layer_crossing_path; del layer_crossing_temporary; del layer_kerbs; del layer_vertices
    QgsProject.instance().clear()



#-------------------------------------------------------------------------
# Taktile Bodenleitsysteme entlang von Bordsteinen und Wegen generieren
#-------------------------------------------------------------------------
if proc_cr_tactile_pav:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Generiere taktile Bodenleitsysteme...')
    print(time.strftime('%H:%M:%S', time.localtime()), '   Filtere Bordsteinlinien mit Leitsystemen...')
    if not layer_raw_kerb_ways:
        #Bordsteinlinienlayer erzeugen: Da geschlossene Bordsteinlinien als Polygone interpretiert werden, falls sie mit anderen Features gemeinsam gemappt sind, diese zunächst zu Linien umwandeln
        if not layer_raw_barrier_ways:
            layer_raw_barrier_ways = QgsVectorLayer(data_dir + 'barriers.geojson|geometrytype=LineString', 'barrier (raw)', 'ogr')
        layer_kerb = processing.run('qgis:extractbyattribute', { 'INPUT' : layer_raw_barrier_ways, 'FIELD' : 'barrier', 'VALUE' : 'kerb', 'OUTPUT': 'memory:'})['OUTPUT']
        if not layer_raw_barrier_polygons:
            layer_raw_barrier_polygons = QgsVectorLayer(data_dir + 'barriers.geojson|geometrytype=Polygon', 'barrier (raw)', 'ogr')
        layer_kerb_outlines = processing.run('native:polygonstolines', { 'INPUT' : layer_raw_barrier_polygons, 'OUTPUT': 'memory:'})['OUTPUT']
        layer_kerb_outlines = processing.run('qgis:extractbyattribute', { 'INPUT' : layer_kerb_outlines, 'FIELD' : 'barrier', 'VALUE' : 'kerb', 'OUTPUT': 'memory:'})['OUTPUT']
        layer_kerb = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_kerb_outlines, layer_kerb], 'OUTPUT': 'memory:'})['OUTPUT']
        layer_kerb = processing.run('native:reprojectlayer', { 'INPUT' : layer_kerb, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    else:
        layer_kerb = layer_raw_kerb_ways
    layer_kerb = processing.run('native:reprojectlayer', { 'INPUT' : layer_kerb, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']

    #Bordsteinliniensegmente, an denen bereits tactile_paving angegeben ist, separieren
    layer_kerb_tactile_paving = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_kerb, 'EXPRESSION' : '"tactile_paving" = \'yes\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_kerb = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_kerb, 'EXPRESSION' : '"tactile_paving" IS NOT \'yes\'', 'OUTPUT': 'memory:'})['OUTPUT']

    #später benötigte Breiten- und Versatz-Attribute anlegen und füllen
    layer_kerb_tactile_paving = clearAttributes(layer_kerb_tactile_paving, ['barrier', 'highway'])
    layer_kerb_tactile_paving.dataProvider().addAttributes([QgsField('offset', QVariant.String)])
    layer_kerb_tactile_paving.dataProvider().addAttributes([QgsField('width', QVariant.String)])
    layer_kerb_tactile_paving.updateFields()
    layer_kerb_tactile_paving.startEditing()
    id_offset = layer_kerb_tactile_paving.fields().indexOf('offset')
    id_width = layer_kerb_tactile_paving.fields().indexOf('width')
    for kerb in layer_kerb_tactile_paving.getFeatures():
        layer_kerb_tactile_paving.changeAttributeValue(kerb.id(), id_offset, -0.5)
        layer_kerb_tactile_paving.changeAttributeValue(kerb.id(), id_width, 1)
    layer_kerb_tactile_paving.commitChanges()

    #Bordsteinlinienpunkte einladen ("kerb" werden - unabhängig von "barrier" - explizit im highway-Layer mitgeliefert)
    if not layer_raw_highway_points:
        layer_raw_highway_points = QgsVectorLayer(data_dir + 'highway.geojson|geometrytype=Point', 'highway (raw)', 'ogr')
    #Bordsteinpunkte mit Bodenleitsystemen herausfiltern
    layer_tactile_paving_nodes = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_highway_points, 'EXPRESSION' : '"tactile_paving" = \'yes\' and "kerb" IS NOT NULL', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_tactile_paving_nodes = processing.run('native:reprojectlayer', { 'INPUT' : layer_tactile_paving_nodes, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']

    print(time.strftime('%H:%M:%S', time.localtime()), '   Übertrage Wegebreite...')
    #Wege einladen (für Breite der Markierung und für Wegesegmente mit bordstein-unabhängigem Bodenleitsystem)
    if not layer_raw_path_ways:
        layer_raw_path_ways = QgsVectorLayer(data_dir + 'path.geojson|geometry=LineString', 'path (raw)', 'ogr')

    layer_ways = processing.run('native:reprojectlayer', { 'INPUT' : layer_raw_path_ways, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_ways = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_ways, 'EXPRESSION' : '"footway" = \'crossing\'', 'OUTPUT': 'memory:'})['OUTPUT']

    #Wegebreiten (Breiten der Querungsstellen) auf Punkte übertragen, um Bodenleitsysteme entsprechend breit zu zeichnen
    layer_tactile_paving_nodes = processing.run('native:joinattributesbylocation', {'INPUT': layer_tactile_paving_nodes, 'JOIN' : layer_ways, 'JOIN_FIELDS' : ['width'], 'PREDICATE' : [0], 'PREFIX' : 'highway:', 'OUTPUT': 'memory:'})['OUTPUT']
    if layer_tactile_paving_nodes.fields().indexOf('highway:width') != -1:
        layer_tactile_paving_nodes.startEditing()
        id_width = layer_tactile_paving_nodes.fields().indexOf('highway:width')
        for kerb in layer_tactile_paving_nodes.getFeatures():
            width = kerb.attribute('highway:width')
            if width == NULL:
                width = 5
                layer_tactile_paving_nodes.changeAttributeValue(kerb.id(), id_width, width)
        layer_tactile_paving_nodes.commitChanges()

        #Puffer im Umkreis der Querungsbreite ziehen
        layer_tactile_paving_nodes_buffer = processing.run('native:buffer', { 'INPUT' : layer_tactile_paving_nodes, 'DISTANCE' : QgsProperty.fromExpression('"highway:width" / 2'), 'OUTPUT': 'memory:'})['OUTPUT']
    else:
        #Puffer im Umkreis der Querungsbreite (default = 5 Meter) ziehen
        layer_tactile_paving_nodes_buffer = processing.run('native:buffer', { 'INPUT' : layer_tactile_paving_nodes, 'DISTANCE' : 2.5, 'OUTPUT': 'memory:'})['OUTPUT']

    #Den Bordsteinpunkt schneidende Bordsteinlinien innerhalb des Puffers ausstanzen
    layer_tactile_paving_lines = processing.run('native:clip', {'INPUT': layer_kerb, 'OVERLAY': layer_tactile_paving_nodes_buffer, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_tactile_paving_lines = processing.run('native:extractbylocation', { 'INPUT' : layer_tactile_paving_lines, 'INTERSECT' : layer_tactile_paving_nodes, 'PREDICATE' : [0], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_tactile_paving_lines = clearAttributes(layer_tactile_paving_lines, ['barrier', 'highway'])
    #Bodenleitsystem an Bordsteinkanten mit Versatz
    layer_tactile_paving_lines.dataProvider().addAttributes([QgsField('offset', QVariant.String)])
    layer_tactile_paving_lines.dataProvider().addAttributes([QgsField('width', QVariant.String)])
    layer_tactile_paving_lines.updateFields()
    layer_tactile_paving_lines.startEditing()
    id_offset = layer_tactile_paving_lines.fields().indexOf('offset')
    id_width = layer_tactile_paving_lines.fields().indexOf('width')
    for kerb in layer_tactile_paving_lines.getFeatures():
        layer_tactile_paving_lines.changeAttributeValue(kerb.id(), id_offset, -0.5)
        layer_tactile_paving_lines.changeAttributeValue(kerb.id(), id_width, 1)
    layer_tactile_paving_lines.commitChanges()

    print(time.strftime('%H:%M:%S', time.localtime()), '   Integriere Wegesegmente mit Leitsystemen...')

    #Wege mit separatem, bordstein-unabhängigem Bodenleitsystem herausfiltern
    layer_tactile_paving_ways = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_path_ways, 'EXPRESSION' : '"tactile_paving" = \'yes\' and "footway" IS NOT \'crossing\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_tactile_paving_ways = clearAttributes(layer_tactile_paving_ways, ['barrier', 'highway'])
    #Bodenleitsystem auf Wegen ohne Versatz
    layer_tactile_paving_ways.dataProvider().addAttributes([QgsField('offset', QVariant.String)])
    layer_tactile_paving_ways.dataProvider().addAttributes([QgsField('width', QVariant.String)])
    layer_tactile_paving_ways.updateFields()
    layer_tactile_paving_ways.startEditing()
    id_offset = layer_tactile_paving_ways.fields().indexOf('offset')
    id_width = layer_tactile_paving_ways.fields().indexOf('width')
    for way in layer_tactile_paving_ways.getFeatures():
        layer_tactile_paving_ways.changeAttributeValue(way.id(), id_offset, 0)
        layer_tactile_paving_ways.changeAttributeValue(way.id(), id_width, 0.4)
    layer_tactile_paving_ways.commitChanges()

    #verschiedene Layer vereinigen
    layer_tactile_paving = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_tactile_paving_lines, layer_kerb_tactile_paving, layer_tactile_paving_ways], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_tactile_paving = processing.run('native:dissolve', { 'FIELD' : ['barrier', 'highway', 'width', 'offset'], 'INPUT' : layer_tactile_paving, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_tactile_paving = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_tactile_paving, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_tactile_paving = clearAttributes(layer_tactile_paving, ['barrier', 'highway', 'width', 'offset'])
    qgis.core.QgsVectorFileWriter.writeAsVectorFormat(layer_tactile_paving, proc_dir + 'tactile_paving.geojson', 'utf-8', QgsCoordinateReferenceSystem(crs_from), 'GeoJson')



#--------------------------------
# Straßenmarkierungen erzeugen
#--------------------------------
if proc_lane_markings:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Erzeuge Straßenmarkierungen...')

    #Kreuzungsflächen laden, um dort später Straßenmarkierungen zu entfernen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Lade Knotenpunktbereiche...')

    if not layer_raw_area_highway_polygons:
        layer_raw_area_highway_polygons = QgsVectorLayer(data_dir + 'area_highway.geojson|geometrytype=Polygon', 'area_highway (raw)', 'ogr')

    layer_junction_areas = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_area_highway_polygons, 'EXPRESSION' : '"junction" = \'yes\' OR "crossing" = \'traffic_signals\' OR "crossing" = \'marked\' OR "crossing" = \'zebra\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_junction_areas = processing.run('native:reprojectlayer', { 'INPUT' : layer_junction_areas, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
#    QgsProject.instance().addMapLayer(layer_junction_areas, True)

    if not layer_raw_highway_points:
        layer_raw_highway_points = QgsVectorLayer(data_dir + 'highway.geojson|geometrytype=Point', 'highway (raw)', 'ogr')
    layer_stop_nodes = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_highway_points, 'EXPRESSION' : '"highway" = \'traffic_signals\' or "highway" = \'stop\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_stop_nodes = processing.run('native:reprojectlayer', { 'INPUT' : layer_stop_nodes, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_stop_nodes = clearAttributes(layer_stop_nodes, ['id', 'highway', 'traffic_signals:direction', 'direction', 'stop_line', 'stop_line:angle', 'temporary'])

    #Fahrbahnen mit Fahrspurmarkierungen oder Abbiegespuren einladen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Lade Straßennetz...')
    print(time.strftime('%H:%M:%S', time.localtime()), '      Markierte Straßensegmente...')
    if not layer_raw_highway_ways:
        layer_raw_highway_ways = QgsVectorLayer(data_dir + 'highway.geojson|geometrytype=LineString', 'highway (raw)', 'ogr')
    layer_lanes = processing.run('native:reprojectlayer', { 'INPUT' : layer_raw_highway_ways, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']

    print(time.strftime('%H:%M:%S', time.localtime()), '      Segmente an Ampeln und Stopschildern...')
    #Segmente an Ampeln und Stopschildern zur Generierung der Haltelinien ebenfalls einbeziehen
    layer_lanes_stop_lines = processing.run('native:extractbylocation', { 'INPUT' : layer_lanes, 'INTERSECT' : layer_stop_nodes, 'PREDICATE' : [0], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_lanes, 'EXPRESSION' : '"highway" IS NOT \'construction\' AND ("lane_markings" = \'yes\' OR "turn" IS NOT NULL OR "turn:forward" IS NOT NULL OR "turn:backward" IS NOT NULL OR "turn:lanes" IS NOT NULL OR "turn:lanes:forward" IS NOT NULL OR "turn:lanes:backward" IS NOT NULL OR "cycleway" = \'lane\' OR "cycleway:both" = \'lane\' OR "cycleway:right" = \'lane\' OR "cycleway:left" = \'lane\')', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_lanes, layer_lanes_stop_lines], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes = processing.run('native:deleteduplicategeometries', {'INPUT': layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']

    print(time.strftime('%H:%M:%S', time.localtime()), '   Vereinfache Straßeninformationen...')
#    layer_lanes = processing.run('native:dissolve', { 'FIELD' : lanes_attributes, 'INPUT' : layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']
#    Achtung: Sollte "dissolve" mit "lanes_attributes" irgendwann wieder verwendet werden, muss eine angepasste Liste ohne "id" verwendet werden!
#    layer_lanes = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes = clearAttributes(layer_lanes, lanes_attributes)


#    QgsProject.instance().addMapLayer(layer_lanes, True)


    print(time.strftime('%H:%M:%S', time.localtime()), '   Bereite Fahrspuren vor...')
    #Attribut für Versatz ergänzen
    layer_lanes.startEditing()

    for attr in ['lanes', 'lanes:forward', 'lanes:backward', 'oneway', 'oneway:bicycle', 'placement_abs', 'offset', 'offset_delta', 'turn', 'reverse', 'width', 'access', 'surface:colour', 'marking:left', 'marking:right', 'buffer:left', 'buffer:right', 'separation:left', 'separation:right', 'cw_lane', 'lanes_forward', 'lanes_backward', 'temporary', 'id_instance']:
        if layer_lanes.fields().indexOf(attr) == -1:
            layer_lanes.dataProvider().addAttributes([QgsField(attr, QVariant.String)])
    layer_lanes.updateFields()
    layer_lanes.commitChanges()

    #Spurattribute auslesen und ggf. in Integer umwandeln (NULL, wenn sie nicht existieren)
    layer_lanes.startEditing()
    lanes_dict = {}
    lanes_dict['width_lanes'] = {}
    lanes_dict['turn_lanes'] = {}
    lanes_dict['cycleway_lanes'] = {}
    lanes_dict['access_lanes'] = {}
    lanes_dict['colour_lanes'] = {}
    lanes_dict['buffer_left_lanes'] = {}
    lanes_dict['buffer_right_lanes'] = {}
    lanes_dict['separation_left_lanes'] = {}
    lanes_dict['separation_right_lanes'] = {}
    lanes_dict['marking_left_lanes'] = {}
    lanes_dict['marking_right_lanes'] = {}
    lanes_dict['cw_lane_lanes'] = {}
    lanes_dict['extra_offset_left'] = {}
    lanes_dict['extra_offset_right'] = {}
    lanes_dict['reverse_lanes'] = {}
    lanes_dict['placement'] = {}
    lanes_dict['segments_before'] = {}
    lanes_dict['segments_after'] = {}
    transition_dict = {}
    for lane in layer_lanes.getFeatures():
        oneway = oneway_bicycle = dual_carriageway = lane_markings = lanes = lanes_unmarked = lanes_forward = lanes_forward_unmarked = lanes_backward = lanes_backward_unmarked = lanes_conditional = lanes_forward_conditional = lanes_backward_conditional = bus_lanes = bus_lanes_forward = bus_lanes_backward = psv_lanes = psv_lanes_forward = psv_lanes_backward = NULL
        turn = turn_forward = turn_backward = turn_lanes = turn_lanes_forward = turn_lanes_backward = NULL
        cycleway_lanes = cycleway_lanes_forward = cycleway_lanes_backward = width_lanes = width_lanes_forward = width_lanes_backward = width_effective = overtaking = change = change_lanes = change_lanes_forward = change_lanes_backward = placement = placement_forward = placement_backward = placement_start = placement_forward_start = placement_backward_start = placement_end = placement_forward_end = placement_backward_end = parking_left_width = parking_right_width = cycleway = cycleway_both = cycleway_left = cycleway_right = cycleway_width = cycleway_both_width = cycleway_right_width = cycleway_left_width = NULL
        cycleway_buffer = cycleway_buffer_left = cycleway_buffer_right = cycleway_buffer_both = cycleway_both_buffer = cycleway_both_buffer_left = cycleway_both_buffer_right = cycleway_both_buffer_both = cycleway_right_buffer = cycleway_right_buffer_left = cycleway_right_buffer_right = cycleway_right_buffer_both = cycleway_left_buffer = cycleway_left_buffer_left = cycleway_left_buffer_right = cycleway_left_buffer_both = 0
        cycleway_separation = cycleway_separation_left = cycleway_separation_right = cycleway_separation_both = cycleway_both_separation = cycleway_both_separation_left = cycleway_both_separation_right = cycleway_both_separation_both = cycleway_right_separation = cycleway_right_separation_left = cycleway_right_separation_right = cycleway_right_separation_both = cycleway_left_separation = cycleway_left_separation_left = cycleway_left_separation_right = cycleway_left_separation_both = NULL
        cycleway_marking = cycleway_marking_left = cycleway_marking_right = cycleway_marking_both = cycleway_both_marking = cycleway_both_marking_left = cycleway_both_marking_right = cycleway_both_marking_both = cycleway_right_marking = cycleway_right_marking_left = cycleway_right_marking_right = cycleway_right_marking_both = cycleway_left_marking = cycleway_left_marking_left = cycleway_left_marking_right = cycleway_left_marking_both = NULL
        cycleway_left_traffic_mode_left = cycleway_left_traffic_mode_right = cycleway_left_traffic_mode_both = cycleway_right_traffic_mode_left = cycleway_right_traffic_mode_right = cycleway_right_traffic_mode_both = cycleway_both_traffic_mode_left = cycleway_both_traffic_mode_right = cycleway_both_traffic_mode_both = NULL
        cycleway_lane = cycleway_left_lane = cycleway_right_lane = cycleway_both_lane = NULL
        temporary_lane_markings = temporary_cycleway = temporary_cycleway_both = temporary_cycleway_left = temporary_cycleway_right = NULL
        lanes_bus = lanes_bus_forward = lanes_bus_backward = lanes_psv = lanes_psv_forward = lanes_psv_backward = 0

        #print(lane.attribute('id')) # Anzeigen, um fehlerhafte Segmente in den OSM-Daten zu finden, die Script-Error produzieren

        if layer_lanes.fields().indexOf('oneway') != -1:
            oneway = lane.attribute('oneway')
        if layer_lanes.fields().indexOf('oneway:bicycle') != -1:
            oneway_bicycle = lane.attribute('oneway:bicycle')
        if layer_lanes.fields().indexOf('dual_carriageway') != -1:
            dual_carriageway = lane.attribute('dual_carriageway')
        if layer_lanes.fields().indexOf('lane_markings') != -1:
            lane_markings = lane.attribute('lane_markings')
        if layer_lanes.fields().indexOf('lanes') != -1:
            lanes = lane.attribute('lanes')
            if lanes:
                lanes = int(lanes)
        if layer_lanes.fields().indexOf('lanes:unmarked') != -1:
            lanes_unmarked = lane.attribute('lanes:unmarked')
            if lanes_unmarked:
                lanes_unmarked = int(lanes_unmarked)
        if layer_lanes.fields().indexOf('lanes:forward') != -1:
            lanes_forward = lane.attribute('lanes:forward')
            if lanes_forward:
                lanes_forward = int(lanes_forward)
        if layer_lanes.fields().indexOf('lanes:forward:unmarked') != -1:
            lanes_forward_unmarked = lane.attribute('lanes:forward:unmarked')
            if lanes_forward_unmarked:
                lanes_forward_unmarked = int(lanes_forward_unmarked)
        if layer_lanes.fields().indexOf('lanes:backward:unmarked') != -1:
            lanes_backward_unmarked = lane.attribute('lanes:backward:unmarked')
            if lanes_backward_unmarked:
                lanes_backward_unmarked = int(lanes_backward_unmarked)
        if layer_lanes.fields().indexOf('lanes:backward') != -1:
            lanes_backward = lane.attribute('lanes:backward')
            if lanes_backward:
                lanes_backward = int(lanes_backward)
        if layer_lanes.fields().indexOf('lanes:conditional') != -1:
            lanes_conditional = lane.attribute('lanes:conditional')
            if lanes_conditional:
                lanes_conditional = int(lanes_conditional[0])
        if layer_lanes.fields().indexOf('lanes:forward:conditional') != -1:
            lanes_forward_conditional = lane.attribute('lanes:forward:conditional')
            if lanes_forward_conditional:
                lanes_forward_conditional = int(lanes_forward_conditional[0])
        if layer_lanes.fields().indexOf('lanes:backward:conditional') != -1:
            lanes_backward_conditional = lane.attribute('lanes:backward:conditional')
            if lanes_backward_conditional:
                lanes_backward_conditional = int(lanes_backward_conditional[0])
        if layer_lanes.fields().indexOf('turn') != -1:
            turn = lane.attribute('turn')
        if layer_lanes.fields().indexOf('turn:forward') != -1:
            turn_forward = lane.attribute('turn:forward')
        if layer_lanes.fields().indexOf('turn:backward') != -1:
            turn_backward = lane.attribute('turn:backward')
        if layer_lanes.fields().indexOf('turn:lanes') != -1:
            turn_lanes = lane.attribute('turn:lanes')
        if layer_lanes.fields().indexOf('turn:lanes:forward') != -1:
            turn_lanes_forward = lane.attribute('turn:lanes:forward')
        if layer_lanes.fields().indexOf('turn:lanes:backward') != -1:
            turn_lanes_backward = lane.attribute('turn:lanes:backward')
        if layer_lanes.fields().indexOf('lanes:bus') != -1:
            lanes_bus = lane.attribute('lanes:bus')
            if lanes_bus:
                lanes_bus = int(lanes_bus)
            else:
                lanes_bus = 0
        if layer_lanes.fields().indexOf('lanes:bus:forward') != -1:
            lanes_bus_forward = lane.attribute('lanes:bus:forward')
            if lanes_bus_forward:
                lanes_bus_forward = int(lanes_bus_forward)
            else:
                lanes_bus_forward = 0
        if layer_lanes.fields().indexOf('lanes:bus:backward') != -1:
            lanes_bus_backward = lane.attribute('lanes:bus:backward')
            if lanes_bus_backward:
                lanes_bus_backward = int(lanes_bus_backward)
            else:
                lanes_bus_backward = 0
        if layer_lanes.fields().indexOf('lanes:psv') != -1:
            lanes_psv = lane.attribute('lanes:psv')
            if lanes_psv:
                lanes_psv = int(lanes_psv)
            else:
                lanes_psv = 0
        if layer_lanes.fields().indexOf('lanes:psv:forward') != -1:
            lanes_psv_forward = lane.attribute('lanes:psv:forward')
            if lanes_psv_forward:
                lanes_psv_forward = int(lanes_psv_forward)
            else:
                lanes_psv_forward = 0
        if layer_lanes.fields().indexOf('lanes:psv:backward') != -1:
            lanes_psv_backward = lane.attribute('lanes:psv:backward')
            if lanes_psv_backward:
                lanes_psv_backward = int(lanes_psv_backward)
            else:
                lanes_psv_backward = 0
        if layer_lanes.fields().indexOf('bus:lanes') != -1:
            bus_lanes = lane.attribute('bus:lanes')
        if layer_lanes.fields().indexOf('bus:lanes:forward') != -1:
            bus_lanes_forward = lane.attribute('bus:lanes:forward')
        if layer_lanes.fields().indexOf('bus:lanes:backward') != -1:
            bus_lanes_backward = lane.attribute('bus:lanes:backward')
        if layer_lanes.fields().indexOf('psv:lanes') != -1:
            psv_lanes = lane.attribute('psv:lanes')
        if layer_lanes.fields().indexOf('psv:lanes:forward') != -1:
            psv_lanes_forward = lane.attribute('psv:lanes:forward')
        if layer_lanes.fields().indexOf('psv:lanes:backward') != -1:
            psv_lanes_backward = lane.attribute('psv:lanes:backward')
        if layer_lanes.fields().indexOf('width:lanes') != -1:
            width_lanes = lane.attribute('width:lanes')
        if layer_lanes.fields().indexOf('width:lanes:forward') != -1:
            width_lanes_forward = lane.attribute('width:lanes:forward')
        if not width_lanes_forward:
            if layer_lanes.fields().indexOf('width:lanes:forward:start') != -1:
                width_lanes_forward = lane.attribute('width:lanes:forward:start') # Workaround: width:lanes:start/end not supported jet
        if layer_lanes.fields().indexOf('width:lanes:backward') != -1:
            width_lanes_backward = lane.attribute('width:lanes:backward')
        if not width_lanes_backward:
            if layer_lanes.fields().indexOf('width:lanes:backward:end') != -1:
                width_lanes_backward = lane.attribute('width:lanes:backward:end') # Workaround: width:lanes:start/end not supported jet
        if layer_lanes.fields().indexOf('width:effective') != -1:
            width_effective = lane.attribute('width:effective')
        if layer_lanes.fields().indexOf('overtaking') != -1:
            overtaking = lane.attribute('overtaking')
        if layer_lanes.fields().indexOf('change') != -1:
            change = lane.attribute('change')
        if layer_lanes.fields().indexOf('change:lanes') != -1:
            change_lanes = lane.attribute('change:lanes')
        if layer_lanes.fields().indexOf('change:lanes:forward') != -1:
            change_lanes_forward = lane.attribute('change:lanes:forward')
        if layer_lanes.fields().indexOf('change:lanes:backward') != -1:
            change_lanes_backward = lane.attribute('change:lanes:backward')

        if layer_lanes.fields().indexOf('placement') != -1:
            placement = lane.attribute('placement')
        if layer_lanes.fields().indexOf('placement:forward') != -1:
            placement_forward = lane.attribute('placement:forward')
        if layer_lanes.fields().indexOf('placement:backward') != -1:
            placement_backward = lane.attribute('placement:backward')
        if layer_lanes.fields().indexOf('placement:start') != -1:
            placement_start = lane.attribute('placement:start')
        if layer_lanes.fields().indexOf('placement:forward:start') != -1:
            placement_forward_start = lane.attribute('placement:forward:start')
        if layer_lanes.fields().indexOf('placement:backward:start') != -1:
            placement_backward_start = lane.attribute('placement:backward:start')
        if layer_lanes.fields().indexOf('placement:end') != -1:
            placement_end = lane.attribute('placement:end')
        if layer_lanes.fields().indexOf('placement:forward:end') != -1:
            placement_forward_end = lane.attribute('placement:forward:end')
        if layer_lanes.fields().indexOf('placement:backward:end') != -1:
            placement_backward_end = lane.attribute('placement:backward:end')

        if layer_lanes.fields().indexOf('parking:both:width') != -1:
            parking_left_width = lane.attribute('parking:both:width')
            parking_right_width = lane.attribute('parking:both:width')
        if layer_lanes.fields().indexOf('parking:left:width') != -1:
            parking_left_width = lane.attribute('parking:left:width')
        if layer_lanes.fields().indexOf('parking:right:width') != -1:
            parking_right_width = lane.attribute('parking:right:width')

        if layer_lanes.fields().indexOf('cycleway') != -1:
            cycleway = lane.attribute('cycleway')
        if layer_lanes.fields().indexOf('cycleway:both') != -1:
            cycleway_both = lane.attribute('cycleway:both')
        if layer_lanes.fields().indexOf('cycleway:right') != -1:
            cycleway_right = lane.attribute('cycleway:right')
        if layer_lanes.fields().indexOf('cycleway:left') != -1:
            cycleway_left = lane.attribute('cycleway:left')
        if layer_lanes.fields().indexOf('cycleway:width') != -1:
            cycleway_width = lane.attribute('cycleway:width')
            if cycleway_width:
                cycleway_width = float(cycleway_width)
        if layer_lanes.fields().indexOf('cycleway:both:width') != -1:
            cycleway_both_width = lane.attribute('cycleway:both:width')
            if cycleway_both_width:
                cycleway_both_width = float(cycleway_both_width)
        if layer_lanes.fields().indexOf('cycleway:right:width') != -1:
            cycleway_right_width = lane.attribute('cycleway:right:width')
            if cycleway_right_width:
                cycleway_right_width = float(cycleway_right_width)
        if layer_lanes.fields().indexOf('cycleway:left:width') != -1:
            cycleway_left_width = lane.attribute('cycleway:left:width')
            if cycleway_left_width:
                cycleway_left_width = float(cycleway_left_width)
        if layer_lanes.fields().indexOf('cycleway:lanes') != -1:
            cycleway_lanes = lane.attribute('cycleway:lanes')
        if layer_lanes.fields().indexOf('cycleway:lanes:forward') != -1:
            cycleway_lanes_forward = lane.attribute('cycleway:lanes:forward')
        if layer_lanes.fields().indexOf('cycleway:lanes:backward') != -1:
            cycleway_lanes_backward = lane.attribute('cycleway:lanes:backward')

        if layer_lanes.fields().indexOf('cycleway:buffer') != -1:
            cycleway_buffer = lane.attribute('cycleway:buffer')
        if layer_lanes.fields().indexOf('cycleway:buffer:left') != -1:
            cycleway_buffer_left = lane.attribute('cycleway:buffer:left')
        if layer_lanes.fields().indexOf('cycleway:buffer:right') != -1:
            cycleway_buffer_right = lane.attribute('cycleway:buffer:right')
        if layer_lanes.fields().indexOf('cycleway:buffer:both') != -1:
            cycleway_buffer_both = lane.attribute('cycleway:buffer:both')
        if layer_lanes.fields().indexOf('cycleway:both:buffer') != -1:
            cycleway_both_buffer = lane.attribute('cycleway:both:buffer')
        if layer_lanes.fields().indexOf('cycleway:both:buffer:left') != -1:
            cycleway_both_buffer_left = lane.attribute('cycleway:both:buffer:left')
        if layer_lanes.fields().indexOf('cycleway:both:buffer:right') != -1:
            cycleway_both_buffer_right = lane.attribute('cycleway:both:buffer:right')
        if layer_lanes.fields().indexOf('cycleway:both:buffer:both') != -1:
            cycleway_both_buffer_both = lane.attribute('cycleway:both:buffer:both')
        if layer_lanes.fields().indexOf('cycleway:right:buffer') != -1:
            cycleway_right_buffer = lane.attribute('cycleway:right:buffer')
        if layer_lanes.fields().indexOf('cycleway:right:buffer:left') != -1:
            cycleway_right_buffer_left = lane.attribute('cycleway:right:buffer:left')
        if layer_lanes.fields().indexOf('cycleway:right:buffer:right') != -1:
            cycleway_right_buffer_right = lane.attribute('cycleway:right:buffer:right')
        if layer_lanes.fields().indexOf('cycleway:right:buffer:both') != -1:
            cycleway_right_buffer_both = lane.attribute('cycleway:right:buffer:both')
        if layer_lanes.fields().indexOf('cycleway:left:buffer') != -1:
            cycleway_left_buffer = lane.attribute('cycleway:left:buffer')
        if layer_lanes.fields().indexOf('cycleway:left:buffer:left') != -1:
            cycleway_left_buffer_left = lane.attribute('cycleway:left:buffer:left')
        if layer_lanes.fields().indexOf('cycleway:left:buffer:right') != -1:
            cycleway_left_buffer_right = lane.attribute('cycleway:left:buffer:right')
        if layer_lanes.fields().indexOf('cycleway:left:buffer:both') != -1:
            cycleway_left_buffer_both = lane.attribute('cycleway:left:buffer:both')

        if layer_lanes.fields().indexOf('cycleway:separation') != -1:
            cycleway_separation = lane.attribute('cycleway:separation')
        if layer_lanes.fields().indexOf('cycleway:separation:left') != -1:
            cycleway_separation_left = lane.attribute('cycleway:separation:left')
        if layer_lanes.fields().indexOf('cycleway:separation:right') != -1:
            cycleway_separation_right = lane.attribute('cycleway:separation:right')
        if layer_lanes.fields().indexOf('cycleway:separation:both') != -1:
            cycleway_separation_both = lane.attribute('cycleway:separation:both')
        if layer_lanes.fields().indexOf('cycleway:both:separation') != -1:
            cycleway_both_separation = lane.attribute('cycleway:both:separation')
        if layer_lanes.fields().indexOf('cycleway:both:separation:left') != -1:
            cycleway_both_separation_left = lane.attribute('cycleway:both:separation:left')
        if layer_lanes.fields().indexOf('cycleway:both:separation:right') != -1:
            cycleway_both_separation_right = lane.attribute('cycleway:both:separation:right')
        if layer_lanes.fields().indexOf('cycleway:both:separation:both') != -1:
            cycleway_both_separation_both = lane.attribute('cycleway:both:separation:both')
        if layer_lanes.fields().indexOf('cycleway:right:separation') != -1:
            cycleway_right_separation = lane.attribute('cycleway:right:separation')
        if layer_lanes.fields().indexOf('cycleway:right:separation:left') != -1:
            cycleway_right_separation_left = lane.attribute('cycleway:right:separation:left')
        if layer_lanes.fields().indexOf('cycleway:right:separation:right') != -1:
            cycleway_right_separation_right = lane.attribute('cycleway:right:separation:right')
        if layer_lanes.fields().indexOf('cycleway:right:separation:both') != -1:
            cycleway_right_separation_both = lane.attribute('cycleway:right:separation:both')
        if layer_lanes.fields().indexOf('cycleway:left:separation') != -1:
            cycleway_left_separation = lane.attribute('cycleway:left:separation')
        if layer_lanes.fields().indexOf('cycleway:left:separation:left') != -1:
            cycleway_left_separation_left = lane.attribute('cycleway:left:separation:left')
        if layer_lanes.fields().indexOf('cycleway:left:separation:right') != -1:
            cycleway_left_separation_right = lane.attribute('cycleway:left:separation:right')
        if layer_lanes.fields().indexOf('cycleway:left:separation:both') != -1:
            cycleway_left_separation_both = lane.attribute('cycleway:left:separation:both')

        if layer_lanes.fields().indexOf('cycleway:marking') != -1:
            cycleway_marking = lane.attribute('cycleway:marking')
        if layer_lanes.fields().indexOf('cycleway:marking:left') != -1:
            cycleway_marking_left = lane.attribute('cycleway:marking:left')
        if layer_lanes.fields().indexOf('cycleway:marking:right') != -1:
            cycleway_marking_right = lane.attribute('cycleway:marking:right')
        if layer_lanes.fields().indexOf('cycleway:marking:both') != -1:
            cycleway_marking_both = lane.attribute('cycleway:marking:both')
        if layer_lanes.fields().indexOf('cycleway:both:marking') != -1:
            cycleway_both_marking = lane.attribute('cycleway:both:marking')
        if layer_lanes.fields().indexOf('cycleway:both:marking:left') != -1:
            cycleway_both_marking_left = lane.attribute('cycleway:both:marking:left')
        if layer_lanes.fields().indexOf('cycleway:both:marking:right') != -1:
            cycleway_both_marking_right = lane.attribute('cycleway:both:marking:right')
        if layer_lanes.fields().indexOf('cycleway:both:marking:both') != -1:
            cycleway_both_marking_both = lane.attribute('cycleway:both:marking:both')
        if layer_lanes.fields().indexOf('cycleway:right:marking') != -1:
            cycleway_right_marking = lane.attribute('cycleway:right:marking')
        if layer_lanes.fields().indexOf('cycleway:right:marking:left') != -1:
            cycleway_right_marking_left = lane.attribute('cycleway:right:marking:left')
        if layer_lanes.fields().indexOf('cycleway:right:marking:right') != -1:
            cycleway_right_marking_right = lane.attribute('cycleway:right:marking:right')
        if layer_lanes.fields().indexOf('cycleway:right:marking:both') != -1:
            cycleway_right_marking_both = lane.attribute('cycleway:right:marking:both')
        if layer_lanes.fields().indexOf('cycleway:left:marking') != -1:
            cycleway_left_marking = lane.attribute('cycleway:left:marking')
        if layer_lanes.fields().indexOf('cycleway:left:marking:left') != -1:
            cycleway_left_marking_left = lane.attribute('cycleway:left:marking:left')
        if layer_lanes.fields().indexOf('cycleway:left:marking:right') != -1:
            cycleway_left_marking_right = lane.attribute('cycleway:left:marking:right')
        if layer_lanes.fields().indexOf('cycleway:left:marking:both') != -1:
            cycleway_left_marking_both = lane.attribute('cycleway:left:marking:both')

        if layer_lanes.fields().indexOf('cycleway:left:traffic_mode:left') != -1:
            cycleway_left_traffic_mode_left = lane.attribute('cycleway:left:traffic_mode:left')
        if layer_lanes.fields().indexOf('cycleway:left:traffic_mode:right') != -1:
            cycleway_left_traffic_mode_right = lane.attribute('cycleway:left:traffic_mode:right')
        if layer_lanes.fields().indexOf('cycleway:left:traffic_mode:both') != -1:
            cycleway_left_traffic_mode_both = lane.attribute('cycleway:left:traffic_mode:both')
        if layer_lanes.fields().indexOf('cycleway:right:traffic_mode:left') != -1:
            cycleway_right_traffic_mode_left = lane.attribute('cycleway:right:traffic_mode:left')
        if layer_lanes.fields().indexOf('cycleway:right:traffic_mode:right') != -1:
            cycleway_right_traffic_mode_right = lane.attribute('cycleway:right:traffic_mode:right')
        if layer_lanes.fields().indexOf('cycleway:right:traffic_mode:both') != -1:
            cycleway_right_traffic_mode_both = lane.attribute('cycleway:right:traffic_mode:both')
        if layer_lanes.fields().indexOf('cycleway:both:traffic_mode:left') != -1:
            cycleway_both_traffic_mode_left = lane.attribute('cycleway:both:traffic_mode:left')
        if layer_lanes.fields().indexOf('cycleway:both:traffic_mode:right') != -1:
            cycleway_both_traffic_mode_right = lane.attribute('cycleway:both:traffic_mode:right')
        if layer_lanes.fields().indexOf('cycleway:both:traffic_mode:both') != -1:
            cycleway_both_traffic_mode_both = lane.attribute('cycleway:both:traffic_mode:both')

        if layer_lanes.fields().indexOf('cycleway:lane') != -1:
            cycleway_lane = lane.attribute('cycleway:lane')
        if layer_lanes.fields().indexOf('cycleway:left:lane') != -1:
            cycleway_left_lane = lane.attribute('cycleway:left:lane')
        if layer_lanes.fields().indexOf('cycleway:right:lane') != -1:
            cycleway_right_lane = lane.attribute('cycleway:right:lane')
        if layer_lanes.fields().indexOf('cycleway:both:lane') != -1:
            cycleway_both_lane = lane.attribute('cycleway:both:lane')

        if layer_lanes.fields().indexOf('temporary:lane_markings') != -1:
            temporary_lane_markings = lane.attribute('temporary:lane_markings')
            if temporary_lane_markings:
                layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('temporary'), temporary_lane_markings)
        if layer_lanes.fields().indexOf('temporary:cycleway') != -1:
            temporary_cycleway_right = lane.attribute('temporary:cycleway')
            temporary_cycleway_left = lane.attribute('temporary:cycleway')
        if layer_lanes.fields().indexOf('temporary:cycleway:both') != -1:
            temporary_cycleway_right = lane.attribute('temporary:cycleway:both')
            temporary_cycleway_left = lane.attribute('temporary:cycleway:both')
        if layer_lanes.fields().indexOf('temporary:cycleway:left') != -1:
            temporary_cycleway_left = lane.attribute('temporary:cycleway:left')
        if layer_lanes.fields().indexOf('temporary:cycleway:right') != -1:
            temporary_cycleway_right = lane.attribute('temporary:cycleway:right')

        #benachbarte Segmente suchen – Segmente mit gleichem Namen und gemeinsamen Stützpunkten
        QgsProject.instance().addMapLayer(layer_lanes, False)
        lanes_before = getConnectedSegments(layer_lanes, lane, 0)
        lanes_after = getConnectedSegments(layer_lanes, lane, -1)
        list_lanes_before_id = []
        list_lanes_before_inverted = []
        list_lanes_after_id = []
        list_lanes_after_inverted = []
        lane_name = lane.attribute('name')
        lane_highway = lane.attribute('highway')
        geom_lane = lane.geometry()
        x_start = geom_lane.vertexAt(0).x()
        y_start = geom_lane.vertexAt(0).y()
        angle_start = math.degrees(geom_lane.angleAtVertex(0))
        x_end = geom_lane.vertexAt(len(geom_lane.asPolyline()) - 1).x()
        y_end = geom_lane.vertexAt(len(geom_lane.asPolyline()) - 1).y()
        angle_end = math.degrees(geom_lane.angleAtVertex(len(geom_lane.asPolyline()) - 1))
        #Nur für Linien mit Namen, da es primär um Straßenzüge (die üblicherweise einen Namen haben) geht
        lanes_dict['segments_before'][lane.attribute('id')] = {}
        lanes_dict['segments_after'][lane.attribute('id')] = {}
        if lane_name:
            for lane_before in lanes_before:
                #Nachbarsegmente nur bei gleichem Namen und gleicher Straßenkategorie speichern
                if lane_before.attribute('name') != lane_name or lane_before.attribute('highway') != lane_highway:
                    continue
                geom_lane_before = lane_before.geometry()
                xb_start = geom_lane_before.vertexAt(0).x()
                yb_start = geom_lane_before.vertexAt(0).y()
                inverted = 0
                if x_start == xb_start and y_start == yb_start:
                    inverted = 1

                #Winkelunterschied – bei zu großem Winkel nicht als Fortsetzung betrachten (z.B. bei dual-carriageway-Zweigungen)
                if inverted:
                    angle_before = math.degrees(geom_lane_before.angleAtVertex(0))
                else:
                    angle_before = math.degrees(geom_lane_before.angleAtVertex(len(geom_lane_before.asPolyline()) - 1))
                angle_diff = abs(angle_start - angle_before)
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff
                if inverted:
                    angle_diff = abs(angle_diff - 180) # -180 zum Ausgleich der entgegengesetzten Linienrichtung
                #Winkelunterschied zu groß – Ausschluss
                if angle_diff > 70:
                    continue

                #Linienrichtung dazu ermitteln: Wenn erster Vertex der Linie dem ersten Vertex der angrenzenden Linie entspricht, laufen die Linien auseinander (inverted = 1), ansonsten führen sie in die selbe Richtung (inverted = 0)
                list_lanes_before_id.append(lane_before.attribute('id'))
                if inverted:
                    list_lanes_before_inverted.append(1)
                else:
                    list_lanes_before_inverted.append(0)

            for lane_after in lanes_after:
                #Nachbarsegmente nur bei gleichem Namen und gleicher Straßenkategorie speichern
                if lane_after.attribute('name') != lane_name or lane_after.attribute('highway') != lane_highway:
                    continue
                geom_lane_after = lane_after.geometry()
                xa_end = geom_lane_after.vertexAt(len(geom_lane_after.asPolyline()) - 1).x()
                ya_end = geom_lane_after.vertexAt(len(geom_lane_after.asPolyline()) - 1).y()
                inverted = 0
                if x_end == xa_end and y_end == ya_end:
                    inverted = 1

                #Winkelunterschied – bei zu großem Winkel nicht als Fortsetzung betrachten (z.B. bei dual-carriageway-Zweigungen)
                if inverted:
                    angle_after = math.degrees(geom_lane_after.angleAtVertex(len(geom_lane_after.asPolyline()) - 1))
                else:
                    angle_after = math.degrees(geom_lane_after.angleAtVertex(0))

                angle_diff = abs(angle_end - angle_after)
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff
                if inverted:
                    angle_diff = abs(angle_diff - 180) # -180 zum Ausgleich der entgegengesetzten Linienrichtung
                #Winkelunterschied zu groß – Ausschluss
                if angle_diff > 70:
                    continue

                #Linienrichtung dazu ermitteln: Wenn erster Vertex der Linie dem ersten Vertex der angrenzenden Linie entspricht, laufen die Linien auseinander (inverted = 1), ansonsten führen sie in die selbe Richtung (inverted = 0)
                list_lanes_after_id.append(lane_after.attribute('id'))
                if inverted:
                    list_lanes_after_inverted.append(1)
                else:
                    list_lanes_after_inverted.append(0)
        lanes_dict['segments_before'][lane.attribute('id')]['id'] = list_lanes_before_id
        lanes_dict['segments_before'][lane.attribute('id')]['inverted'] = list_lanes_before_inverted
        lanes_dict['segments_after'][lane.attribute('id')]['id'] = list_lanes_after_id
        lanes_dict['segments_after'][lane.attribute('id')]['inverted'] = list_lanes_after_inverted

        #ggf. fehlende Spuranzahl aus Abbiegespur-Informationen ableiten (oder Fahrradspuren in die Anzahl einbeziehen)
        if lanes == NULL:
            if oneway and oneway != 'no':
                lanes = 1
            else:
                if lanes_unmarked:
                    lanes = lanes_unmarked
                else:
                    lanes = 2
            if turn_lanes:
                for pos, char in enumerate(turn_lanes):
                    if(char == '|'):
                        lanes += 1
            layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('lanes'), lanes)

        #forward- und backward-Spuren vervollständigen
        if lanes_forward == NULL:
            if lanes_backward:
                lanes_forward = lanes - lanes_backward
            else:
                if oneway == 'yes':
                    lanes_forward = lanes
                else:
                    lanes_forward = round(lanes / 2)
        if lanes_backward == NULL:
            if lanes_forward:
                lanes_backward = lanes - lanes_forward
            else:
                if oneway == '-1':
                    lanes_backward = lanes
                else:
                    lanes_backward = round(lanes / 2)
        lanes_marked = lanes
        lanes_forward_marked = lanes_forward
        lanes_backward_marked = lanes_backward

        #temporär höhere Spurzahl berücksichtigen (mit max. Spurzahl rechnen)
        if lanes < lanes_conditional:
            lanes = lanes_conditional
        if lanes_forward < lanes_forward_conditional:
            lanes_forward = lanes_forward_conditional
        if lanes_backward < lanes_backward_conditional:
            lanes_backward = lanes_backward_conditional

        #höhere, unmarkierte Spurzahl berücksichtigen
        if lanes_unmarked > lanes or lanes_forward_unmarked > lanes_forward or lanes_backward_unmarked > lanes_backward:
            if not lanes_unmarked:
                if lanes_forward_unmarked and lanes_backward_unmarked:
                    lanes_unmarked = lanes_forward_unmarked + lanes_backward_unmarked
                if lanes_forward_unmarked and not lanes_backward_unmarked:
                    lanes_unmarked = lanes_forward_unmarked + lanes_backward
                    lanes_backward_unmarked = lanes_unmarked - lanes_forward_unmarked
                if lanes_backward_unmarked and not lanes_forward_unmarked:
                    lanes_unmarked = lanes_backward_unmarked + lanes_forward
                    lanes_forward_unmarked = lanes_unmarked - lanes_backward_unmarked
            if not lanes_forward_unmarked:
                if not lanes_backward_unmarked:
                    lanes_forward_unmarked = int(lanes_unmarked / 2)
                else:
                    lanes_forward_unmarked = lanes_unmarked - lanes_backward_unmarked
            if not lanes_backward_unmarked:
                lanes_backward_unmarked = lanes_unmarked - lanes_forward_unmarked
            if lanes < lanes_unmarked:
                lanes = lanes_unmarked
            if lanes_forward < lanes_forward_unmarked:
                lanes_forward = lanes_forward_unmarked
            if lanes_backward < lanes_backward_unmarked:
                lanes_backward = lanes_backward_unmarked

        #Radfahrstreifen in Mittellage in Spurberechnung einbeziehen
        if cycleway_lanes:
            cycleway_lanes = getDelimitedAttributes(cycleway_lanes, '|', 'string')
            lanes += cycleway_lanes.count('lane')
            lanes_dict['cycleway_lanes'][lane.attribute('id')] = cycleway_lanes
        elif cycleway_lanes_forward or cycleway_lanes_backward:
            cycleway_lanes = []
            cyclelanes_forward = cyclelanes_backward = 0
            if cycleway_lanes_forward:
                cyclelanes_forward = getDelimitedAttributes(cycleway_lanes_forward, '|', 'string')
                cyclelanes_forward = cyclelanes_forward.count('lane')
                lanes_forward += cyclelanes_forward
                if cycleway_lanes_backward:
                    cycleway_lanes = list(reversed(getDelimitedAttributes(cycleway_lanes_backward, '|', 'string')))
                    cycleway_lanes += getDelimitedAttributes(cycleway_lanes_forward, '|', 'string')
                else:
                    if cycleway == 'lane' or cycleway_both == 'lane' or cycleway_left == 'lane':
                        cyclelanes_backward = 1
                        lanes_backward += cyclelanes_backward
                    for i in range(lanes_backward):
                        if i < cyclelanes_backward:
                            cycleway_lanes.append('lane')
                        else:
                            cycleway_lanes.append('no')
                    cycleway_lanes += getDelimitedAttributes(cycleway_lanes_forward, '|', 'string')
            if cycleway_lanes_backward:
                cyclelanes_backward = getDelimitedAttributes(cycleway_lanes_backward, '|', 'string')
                cyclelanes_backward = cyclelanes_backward.count('lane')
                lanes_backward += cyclelanes_backward
                if not cycleway_lanes_forward:
                    cycleway_lanes = list(reversed(getDelimitedAttributes(cycleway_lanes_backward, '|', 'string')))
                    if cycleway == 'lane' or cycleway_both == 'lane' or cycleway_right == 'lane':
                        cyclelanes_forward = 1
                        lanes_forward += cyclelanes_forward
                    for i in range(lanes_forward):
                        if cyclelanes_forward and i == lanes_forward - 1:
                            cycleway_lanes.append('lane')
                        else:
                            cycleway_lanes.append('no')

            lanes += cyclelanes_forward + cyclelanes_backward
        else:
            cycleway_lanes = []
            for i in range(lanes):
                cycleway_lanes.append('no')
        lanes_dict['cycleway_lanes'][lane.attribute('id')] = cycleway_lanes

        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('lanes'), lanes)
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('lanes:forward'), lanes_forward)
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('lanes:backward'), lanes_backward)

        #Markierungsattribute für jede Spur ergänzen
        #TODO overtaking:forward/backward einbeziehen
        marking_left_lanes = []
        marking_right_lanes = []
        for i in range(lanes):
            marking_left = marking_right = NULL
            #Überhol- oder Spurwechselverbote = durchgezogene Linie
            if change_lanes:
                change_lane = getDelimitedAttributes(change_lanes, '|', 'string')[i]
                if change_lane == 'no':
                    if i > 0: #on left lane, no change to left is possible
                        marking_left = 'solid_line'
                    if i < lanes: #on right lane, no change to right is possible
                        marking_right = 'solid_line'
                if change_lane == 'not_left':
                    marking_left = 'solid_line'
                if change_lane == 'not_right':
                    marking_right = 'solid_line'
            if change_lanes_forward and i >= lanes_backward:
                change_lane = getDelimitedAttributes(change_lanes_forward, '|', 'string')[i - lanes_backward]
                if change_lane == 'no':
                    marking_left = marking_right = 'solid_line'
                if change_lane == 'not_left':
                    marking_left = 'solid_line'
                if change_lane == 'not_right':
                    marking_right = 'solid_line'
            if change_lanes_backward and i < lanes_backward:
                change_lane = getDelimitedAttributes(change_lanes_backward, '|', 'string')[i]
                if change_lane == 'no':
                    marking_right = 'solid_line'
                    if i > 0: #on left lane, no change to left is possible
                        marking_left = 'solid_line'
                    if i < lanes: #on right lane, no change to right is possible
                        marking_right = 'solid_line'
                if change_lane == 'not_left':
                    marking_right = 'solid_line'
                if change_lane == 'not_right':
                    marking_left = 'solid_line'
            if change == 'no' or (overtaking == 'no' and i == lanes_backward):
                if i > 0: #on left lane, no change to left is possible
                    marking_left = 'solid_line'
                if i < lanes: #on right lane, no change to right is possible
                    marking_right = 'solid_line'
            if not marking_left:
                if lanes_unmarked:
                    if i < lanes_backward:
                        if not lanes_backward_unmarked:
                            if lanes_forward_unmarked:
                                lanes_backward_unmarked = lanes_unmarked - lanes_forward_unmarked
                            else:
                                lanes_backward_unmarked = lanes_unmarked / 2
                        diff_lanes_backward = lanes_backward_unmarked - lanes_backward_marked
                        if i < diff_lanes_backward:
                            marking_left = 'no'
                    else:
                        if i >= lanes_backward + lanes_forward_marked:
                            marking_left = 'no'
                else:
                    if lane_markings or turn or turn_forward or turn_backward or turn_lanes or turn_lanes_forward or turn_lanes_backward:
                        marking_left = 'unspecified'
                    else:
                        marking_left = 'no'
            if not marking_left:
                marking_left = 'unspecified'
            marking_left_lanes.append(marking_left)
            marking_right_lanes.append(marking_right)
        lanes_dict['marking_left_lanes'][lane.attribute('id')] = marking_left_lanes
        lanes_dict['marking_right_lanes'][lane.attribute('id')] = marking_right_lanes

        #Breitenattribute von Radspuren vereinheitlichen
        if not cycleway_right_width:
            if cycleway_width:
                cycleway_right_width = cycleway_width
            elif cycleway_both_width:
                cycleway_right_width = cycleway_both_width
            else:
                cycleway_right_width = cycleway_width_default
        if not cycleway_left_width:
            if cycleway_width:
                cycleway_left_width = cycleway_width
            elif cycleway_both_width:
                cycleway_left_width = cycleway_both_width
            else:
                cycleway_left_width = cycleway_width_default

        #Breitenattribute für alle Spuren von links nach rechts speichern
        if width_lanes:
            width_lanes = getDelimitedAttributes(width_lanes, '|', 'float')
            if len(width_lanes) < lanes:
                for i in range(lanes - len(width_lanes)):
                    width_lanes.append(lane_width_default)
            #leere Spurbreiten mit Default ersetzen
            if '' in width_lanes:
                for i in range(len(width_lanes)):
                    if width_lanes[i] == '':
                        width_lanes[i] = lane_width_default
        else:
            #Falls vorhanden Radwegbreite hinzufügen (außer bei Radstreifen in Mittellage, wo diese bereits mit gemappt werden)
            if width_lanes_backward:
                width_lanes_backward = getDelimitedAttributes(width_lanes_backward, '|', 'float')
                if((cycleway == 'lane' or cycleway_both == 'lane' or cycleway_left == 'lane') and not cycleway_lanes_backward and cycleway_lanes_forward):
                    width_lanes_backward.insert(0, cycleway_left_width)
#                if((cycleway == 'lane' or cycleway_both == 'lane' or cycleway_left == 'lane') and not cycleway_lanes_backward):
#                    width_lanes_backward.insert(0, cycleway_left_width)
            if width_lanes_forward:
                width_lanes_forward = getDelimitedAttributes(width_lanes_forward, '|', 'float')
                if((cycleway == 'lane' or cycleway_both == 'lane' or cycleway_right == 'lane') and not cycleway_lanes_forward and cycleway_lanes_backward):
                    width_lanes_forward.append(cycleway_right_width)
#                if((cycleway == 'lane' or cycleway_both == 'lane' or cycleway_right == 'lane') and not cycleway_lanes_forward):
#                    width_lanes_forward.append(cycleway_right_width)

                #Breitenattribute beider Richtungen zusammensetzen
                if width_lanes_backward:
                    width_lanes = list(reversed(width_lanes_backward)) + width_lanes_forward
                else:
                    width_lanes = []
                    for i in range(lanes_backward):
                        if cycleway_lanes[i] == 'lane':
                            width_lanes.append(cycleway_left_width)
                        else:
                            width_lanes.append(lane_width_default)
                    width_lanes += width_lanes_forward
            else:
                if width_lanes_backward:
                    width_lanes = list(reversed(width_lanes_backward))
                    for i in range(lanes_forward):
                        if cycleway_lanes[i] == 'lane':
                            width_lanes.append(cycleway_right_width)
                        else:
                            width_lanes.append(lane_width_default)
                else:
                    width_lanes = []
                    for i in range(lanes):
                        if cycleway_lanes[i] == 'lane':
                            if i == 0:
                                width_lanes.append(cycleway_left_width)
                            else:
                                width_lanes.append(cycleway_right_width)
                        else:
                            if width_effective:
                                width_lanes.append(float(width_effective) / lanes)
                            else:
                                width_lanes.append(lane_width_default)

        lanes_dict['width_lanes'][lane.attribute('id')] = width_lanes

        #Abbiegespur-Informationen für alle Spuren von links nach rechts speichern
        turn_lanes_vanilla = turn_lanes

        if turn and not turn_lanes:
            turn_lanes = turn
        if turn_forward and not turn_lanes_forward:
            turn_lanes_forward = turn_forward
        if turn_backward and not turn_lanes_backward:
            turn_lanes_backward = turn_backward
        if turn_lanes:
            turn_lanes = getDelimitedAttributes(turn_lanes, '|', 'string')
            if len(turn_lanes) < lanes:
                for i in range(lanes - len(turn_lanes)):
                    turn_lanes.append('none')
        else:
            if turn_lanes_forward:
                if turn_lanes_backward:
                    turn_lanes = list(reversed(getDelimitedAttributes(turn_lanes_backward, '|', 'string'))) + getDelimitedAttributes(turn_lanes_forward, '|', 'string')
                else:
                    turn_lanes = []
                    for i in range(lanes_backward):
                        turn_lanes.append('none')
                    turn_lanes += getDelimitedAttributes(turn_lanes_forward, '|', 'string')
                if len(turn_lanes) < lanes:
                    for i in range(lanes - len(turn_lanes)):
                        turn_lanes.append('none')
            else:
                if turn_lanes_backward:
                    if len(turn_lanes_backward) < lanes_backward:
                        for i in range(lanes_backward - len(turn_lanes_backward)):
                            turn_lanes_backward.append('none')
                    turn_lanes = list(reversed(getDelimitedAttributes(turn_lanes_backward, '|', 'string')))
                    for i in range(lanes_forward):
                        turn_lanes.append('none')
                else:
                    turn_lanes = []
                    for i in range(lanes):
                        turn_lanes.append('none')
        lanes_dict['turn_lanes'][lane.attribute('id')] = turn_lanes

        #Mittellinie zwischen Fahrbahnrichtungen im Bereich von Abbiegespuren üblicherweise durchgezogen
        if turn_lanes_vanilla or turn_lanes_forward or turn_lanes_backward:
            if lanes_backward:
                lanes_dict['marking_left_lanes'][lane.attribute('id')][lanes_backward - 1] = 'solid_line'
                if len(lanes_dict['marking_left_lanes'][lane.attribute('id')]) > lanes_backward:
                    lanes_dict['marking_left_lanes'][lane.attribute('id')][lanes_backward] = 'solid_line'

        #Busspur-Informationen für alle Spuren von links nach rechts speichern
        access_lanes = []

        #Busspurangaben ohne Richtungsangabe auf Zweirichtungswegen auf beide Seiten aufteilen
        if lanes_bus > 1 and oneway != 'yes' and oneway != -1 and not lanes_bus_forward and not lanes_bus_backward:
            lanes_bus_forward = round(lanes_bus / 2)
            lanes_bus_backward = lanes_bus - lanes_bus_forward
            lanes_bus = 0
        if lanes_psv > 1 and oneway != 'yes' and oneway != -1 and not lanes_psv_forward and not lanes_psv_backward:
            lanes_psv_forward = round(lanes_psv / 2)
            lanes_psv_backward = lanes_psv - lanes_psv_forward
            lanes_psv = 0

        #keine Unterscheidung zwischen bus und psv notwendig – alles als Busspur deklarieren
        lanes_bus += lanes_psv
        lanes_bus_forward += lanes_psv_forward
        lanes_bus_backward += lanes_psv_backward

        #Busspuren in Einzelspurnotation
        if bus_lanes:
            bus_lanes = getDelimitedAttributes(bus_lanes, '|', 'string')
        if psv_lanes:
            if not bus_lanes:
                bus_lanes = getDelimitedAttributes(psv_lanes, '|', 'string')
            else:
                for i in range(len(psv_lanes)):
                    if psv_lanes[i] == 'designated':
                        bus_lanes[i] = psv_lanes[i]

        if lanes_bus:
            if bus_lanes:
                for i in range(len(bus_lanes)):
                    if bus_lanes[i] == 'designated':
                        access_lanes.append('bus')
                    else:
                        access_lanes.append('vehicle')
            else:
                for i in range(lanes - lanes_bus):
                    access_lanes.append('vehicle')
                for i in range(lanes_bus):
                    access_lanes.append('bus')
        elif lanes_bus_forward:
            if lanes_bus_backward:
                for i in range(lanes_bus_backward):
                    access_lanes.append('bus')
                for i in range((lanes_backward - lanes_bus_backward) + (lanes_forward - lanes_bus_forward)):
                    access_lanes.append('vehicle')
                for i in range(lanes_bus_forward):
                    access_lanes.append('bus')
            else:
                for i in range(lanes_backward + (lanes_forward - lanes_bus_forward)):
                    access_lanes.append('vehicle')
                for i in range(lanes_bus_forward):
                    access_lanes.append('bus')
        elif lanes_bus_backward:
            for i in range(lanes_bus_backward):
                access_lanes.append('bus')
            for i in range(lanes - lanes_bus_backward):
                access_lanes.append('vehicle')
        else:
            for i in range(lanes):
                access_lanes.append('vehicle')

        lanes_dict['access_lanes'][lane.attribute('id')] = access_lanes

        if placement == 'transition' or placement_start or placement_forward_start or placement_backward_start:
            placement_after = NULL
            if placement_end or placement_forward_end or placement_backward_end:
                placement_after = getAbsolutePlacement(lanes, lanes_backward, placement_end, placement_forward_end, placement_backward_end, 0)
            #angrenzede Segmente ermitteln
            segment_before = getConnectedSegments(layer_lanes, lane, 0)
            segment_after = getConnectedSegments(layer_lanes, lane, -1)
            #Wenn keine Vorgänger- oder Nachfolger-Segmente und keine sonstigen Angaben: Vermutlich anzunehmen, dass einspurige, unmarkierte Abschnitte
            if not segment_before and not placement and not placement_forward and not placement_backward:
                placement = 'middle_of:1'
            if not segment_after and not placement_after:
                placement_after = 'middle_of:1'

            #Wenn mehrere Segmente angrenzen, dass erste mit gleichem Namen und gleicher Straßenklasse nehmen, sonst ignorieren
            #TODO: man könnte sicherheitshalber auch noch die gleiche Richtung prüfen
            if len(segment_before) > 1:
                for segment in segment_before:
                    if segment.attribute('name') == lane.attribute('name') and segment.attribute('highway') == lane.attribute('highway'):
                        segment_before = [segment]
            if len(segment_after) > 1:
                for segment in segment_after:
                    if segment.attribute('name') == lane.attribute('name') and segment.attribute('highway') == lane.attribute('highway'):
                        segment_after = [segment]
            if len(segment_before) > 1 or len(segment_after) > 1:
                layer_lanes.deleteFeature(lane.id())
                continue
            #lanes- und placement-Werte des Vorgängers und Nachfolgers auslesen
            #placement des Segments mit weniger Spuren übernehmen
            lanes_before = lanes_after = 1
            lanes_before_backward = lanes_after_backward = 0
            if segment_before:
                segment_before = segment_before[0]
                if layer_lanes.fields().indexOf('lanes') != -1:
                    lanes_before = segment_before.attribute('lanes')
                    if lanes_before:
                        lanes_before = int(lanes_before)
                if layer_lanes.fields().indexOf('lanes:backward') != -1:
                    lanes_before_backward = segment_before.attribute('lanes:backward')
                    if lanes_before_backward:
                        lanes_before_backward = int(lanes_before_backward)
                #manche Segmente wurden zuvor bereits prozessiert – hier die Radspuren nochmal herausnehmen
                segment_before_id = segment_before.attribute('id')
                if segment_before_id in lanes_dict['access_lanes']:
                    c = lanes_dict['access_lanes'][segment_before_id].count('bicycle')
                    if c:
                        cb = 0
                        for k in range(lanes_before):
                            if lanes_dict['access_lanes'][segment_before_id][k] == 'bicycle' and lanes_dict['reverse_lanes'][segment_before_id][k] == 1:
                                cb += 1
                        lanes_before -= c
                        lanes_before_backward -= cb
            if segment_after:
                segment_after = segment_after[0]
                if layer_lanes.fields().indexOf('lanes') != -1:
                    lanes_after = segment_after.attribute('lanes')
                    if lanes_after:
                        lanes_after = int(lanes_after)
                if layer_lanes.fields().indexOf('lanes:backward') != -1:
                    lanes_after_backward = segment_after.attribute('lanes:backward')
                    if lanes_after_backward:
                        lanes_after_backward = int(lanes_after_backward)
                    else:
                        lanes_after_backward = 0
                segment_after_id = segment_after.attribute('id')
                if segment_after_id in lanes_dict['access_lanes']:
                    c = lanes_dict['access_lanes'][segment_after_id].count('bicycle')
                    if c:
                        cb = 0
                        for k in range(lanes_after):
                            if lanes_dict['access_lanes'][segment_after_id][k] == 'bicycle' and lanes_dict['reverse_lanes'][segment_after_id][k] == 1:
                                cb += 1
                        lanes_after -= c
                        lanes_after_backward -= cb
            placement = placement_forward = placement_backward = NULL
            if lanes_before < lanes_after:
                if placement_start or placement_forward_start or placement_backward_start:
                    if placement_start:
                        placement = placement_start
                    if placement_forward_start:
                        placement_forward = placement_forward_start
                    if placement_backward_start:
                        placement_backward = placement_backward_start
                else:
                    if layer_lanes.fields().indexOf('placement') != -1:
                        placement = segment_before.attribute('placement')
                    if layer_lanes.fields().indexOf('placement:forward') != -1:
                        placement_forward = segment_before.attribute('placement:forward')
                    if layer_lanes.fields().indexOf('placement:backward') != -1:
                        placement_backward = segment_before.attribute('placement:backward')
                lanes_for_placement = lanes_before
                lanes_backward_for_placement = lanes_before_backward
                fix = 0
            else:
                if placement_end or placement_forward_end or placement_backward_end:
                    if placement_end:
                        placement = placement_end
                    if placement_forward_end:
                        placement_forward = placement_forward_end
                    if placement_backward_end:
                        placement_backward = placement_backward_end
                else:
                    if segment_after:
                        if layer_lanes.fields().indexOf('placement') != -1:
                            placement = segment_after.attribute('placement')
                        if layer_lanes.fields().indexOf('placement:forward') != -1:
                            placement_forward = segment_after.attribute('placement:forward')
                        if layer_lanes.fields().indexOf('placement:backward') != -1:
                            placement_backward = segment_after.attribute('placement:backward')
                    else:
                        placement = 'middle_of:1'
                lanes_for_placement = lanes_after
                lanes_backward_for_placement = lanes_after_backward
                fix = 1

            placement = getAbsolutePlacement(lanes_for_placement, lanes_backward_for_placement, placement, placement_forward, placement_backward, 0)

            #transition-Segmente für späteren Versatz vormerken
            transition_dict[lane.attribute('id')] = [placement_after, fix, placement_start]

        #Radstreifen in Mittellage als Spur mitzählen
        l_extra = 0
        if cycleway_lanes.count('lane') and placement:
            placement_lane = int(placement[len(placement)-1:len(placement)])
            for i in range(0, len(cycleway_lanes)):
                ln = cycleway_lanes[i]
                #TODO: Formel bisher nur auf einspurige Fahrbahnabschnitte ausgelegt
                if ln == 'lane' and i + 1 <= placement_lane:
                    l_extra = 1


#        if lane.attribute('id') == 'way/964618340':
#            print(lanes, lanes_forward, lanes_backward, ' | ', lanes_marked, lanes_forward_marked, lanes_backward_marked, ' | ', lanes_unmarked, lanes_forward_unmarked, lanes_backward_unmarked)

        if lanes_unmarked and not placement and not placement_forward and not placement_backward and lanes_forward_unmarked != lanes_backward_unmarked:
            placement = getAbsolutePlacement(lanes_marked, lanes_backward_marked, placement, placement_forward, placement_backward, l_extra)
        else:
            placement = getAbsolutePlacement(lanes, lanes_backward, placement, placement_forward, placement_backward, l_extra)
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('placement_abs'), placement)

        j = -(len(placement) - placement.find(':') - 1)
        l = int(placement[j:])

        #Versatz ermitteln, um Linie in die Mitte der linken Spur verschieben, um anschließend parallele Linien zu erzeugen
        offset = 0
        #linkeste Fahrspurkante ermitteln

        for i in range(l - 1):
            offset += float(width_lanes[i])
        if 'middle_of:' in placement:
            offset += float(width_lanes[l - 1]) / 2
        if 'right_of:' in placement:
            offset += float(width_lanes[l - 1])
        #Versatz an der Mitte der linkesten Spur ausrichten
        offset -= float(width_lanes[0]) / 2

        #Allgemeine Fahrradspuren in Spurberechnung einbeziehen
        cyclelanes_forward = cyclelanes_backward = 0
        if((cycleway == 'lane' or cycleway_both == 'lane' or cycleway_right == 'lane' or cycleway_left == 'lane') and cycleway_lanes.count('lane') == 0): #Radfahrstreifen in Mittellage werden bereits separat ausgewertet
            if cycleway_right == 'lane' or cycleway_both == 'lane':
                if temporary_cycleway_right != 'no':
                    cyclelanes_forward = 1
            if cycleway_left == 'lane' or cycleway_both == 'lane':
                if temporary_cycleway_left != 'no':
                    cyclelanes_backward = 1
            if cycleway == 'lane':
                if temporary_cycleway_right != 'no':
                    cyclelanes_forward = 1
                    if oneway != 'yes' and temporary_cycleway_left != 'no':
                        cyclelanes_backward = 1
            lanes += cyclelanes_forward + cyclelanes_backward
            lanes_forward += cyclelanes_forward
            lanes_backward += cyclelanes_backward

            cycleway_lanes = []
            for i in range(lanes):
                if (cycleway_left == 'lane' and i == 0) or (cycleway_right == 'lane' and i == lanes - 1):
                    cycleway_lanes.append('lane')
                else:
                    cycleway_lanes.append('no')

            lanes_dict['cycleway_lanes'][lane.attribute('id')] = cycleway_lanes

            #absolute placement anpassen: Befindet sich links ein Radweg, erhöhen sich alle Stellen um 1
            if cyclelanes_backward:
                l = int(placement[j])
                l += 1
                placement = placement[0:j] + str(l)
                layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('placement_abs'), placement)

            #Werte für Gesamtfahrbahn nachträglich anpassen:
            #lanes-Anzahl
            layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('lanes'), lanes)
            layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('lanes:forward'), lanes_forward)
            layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('lanes:backward'), lanes_backward)

            #turn, access und width-Listen
            if cyclelanes_forward:
                lanes_dict['turn_lanes'][lane.attribute('id')].append('none')
                lanes_dict['access_lanes'][lane.attribute('id')].append('bicycle')
                lanes_dict['width_lanes'][lane.attribute('id')].append(cycleway_right_width)
                #ob Radweg gestrichelte oder durchgezogene Linie hat, wird später individuell geklärt
                lanes_dict['marking_left_lanes'][lane.attribute('id')].append('unspecified')
                lanes_dict['marking_right_lanes'][lane.attribute('id')].append('unspecified')
            if cyclelanes_backward:
                lanes_dict['turn_lanes'][lane.attribute('id')].insert(0, 'none')
                lanes_dict['access_lanes'][lane.attribute('id')].insert(0, 'bicycle')
                lanes_dict['width_lanes'][lane.attribute('id')].insert(0, cycleway_left_width)
                lanes_dict['marking_left_lanes'][lane.attribute('id')].insert(0, 'unspecified')
                lanes_dict['marking_right_lanes'][lane.attribute('id')].insert(0, 'unspecified')
                offset += (float(lanes_dict['width_lanes'][lane.attribute('id')][1]) / 2) + (cycleway_left_width / 2)

        #buffer-Attribute von Radspuren vereinheitlichen
        if not cycleway_left_buffer_left:
            if cycleway_buffer:
                cycleway_left_buffer_left = cycleway_buffer
            if cycleway_buffer_left:
                cycleway_left_buffer_left = cycleway_buffer_left
            if cycleway_buffer_both:
                cycleway_left_buffer_left = cycleway_buffer_both
            if cycleway_both_buffer:
                cycleway_left_buffer_left = cycleway_both_buffer
            if cycleway_both_buffer_both:
                cycleway_left_buffer_left = cycleway_both_buffer_both
            if cycleway_both_buffer_left:
                cycleway_left_buffer_left = cycleway_both_buffer_left
            if cycleway_left_buffer:
                cycleway_left_buffer_left = cycleway_left_buffer
            if cycleway_left_buffer_both:
                cycleway_left_buffer_left = cycleway_left_buffer_both
        if not cycleway_right_buffer_left:
            if cycleway_buffer:
                cycleway_right_buffer_left = cycleway_buffer
            if cycleway_buffer_left:
                cycleway_right_buffer_left = cycleway_buffer_left
            if cycleway_buffer_both:
                cycleway_right_buffer_left = cycleway_buffer_both
            if cycleway_both_buffer:
                cycleway_right_buffer_left = cycleway_both_buffer
            if cycleway_both_buffer_both:
                cycleway_right_buffer_left = cycleway_both_buffer_both
            if cycleway_both_buffer_left:
                cycleway_right_buffer_left = cycleway_both_buffer_left
            if cycleway_right_buffer:
                cycleway_right_buffer_left = cycleway_right_buffer
            if cycleway_right_buffer_both:
                cycleway_right_buffer_left = cycleway_right_buffer_both
        if not cycleway_left_buffer_right:
            if cycleway_buffer_right:
                cycleway_left_buffer_right = cycleway_buffer_right
            if cycleway_buffer_both:
                cycleway_left_buffer_right = cycleway_buffer_both
            if cycleway_both_buffer_both:
                cycleway_left_buffer_right = cycleway_both_buffer_both
            if cycleway_both_buffer_right:
                cycleway_left_buffer_right = cycleway_both_buffer_right
            if cycleway_left_buffer_both:
                cycleway_left_buffer_right = cycleway_left_buffer_both
        if not cycleway_right_buffer_right:
            if cycleway_buffer_right:
                cycleway_right_buffer_right = cycleway_buffer_right
            if cycleway_buffer_both:
                cycleway_right_buffer_right = cycleway_buffer_both
            if cycleway_both_buffer_both:
                cycleway_right_buffer_right = cycleway_both_buffer_both
            if cycleway_both_buffer_right:
                cycleway_right_buffer_right = cycleway_both_buffer_right
            if cycleway_right_buffer_both:
                cycleway_right_buffer_right = cycleway_right_buffer_both

        buffer_default = 0.5 #Wert, der bei nicht genauer spezifiziertem Buffer angenommen wird
        if cycleway_left_buffer_left == 'no' or cycleway_left_buffer_left == NULL:
            cycleway_left_buffer_left = 0
        if cycleway_left_buffer_left == 'yes':
            cycleway_left_buffer_left = buffer_default
        if cycleway_right_buffer_left == 'no' or cycleway_right_buffer_left == NULL:
            cycleway_right_buffer_left = 0
        if cycleway_right_buffer_left == 'yes':
            cycleway_right_buffer_left = buffer_default
        if cycleway_left_buffer_right == 'no' or cycleway_left_buffer_right == NULL:
            cycleway_left_buffer_right = 0
        if cycleway_left_buffer_right == 'yes':
            cycleway_left_buffer_right = buffer_default
        if cycleway_right_buffer_right == 'no' or cycleway_right_buffer_right == NULL:
            cycleway_right_buffer_right = 0
        if cycleway_right_buffer_right == 'yes':
            cycleway_right_buffer_right = buffer_default

        #Geschützte Radstreifen und Bodenmarkierungen erkennen (cycleway:separation, cycleway:marking, cycleway:lane)
        if not cycleway_right_separation_left:
            if cycleway_separation:
                cycleway_right_separation_left = cycleway_separation
            if cycleway_separation_left:
                cycleway_right_separation_left = cycleway_separation_left
            if cycleway_separation_both:
                cycleway_right_separation_left = cycleway_separation_both
            if cycleway_both_separation:
                cycleway_right_separation_left = cycleway_both_separation
            if cycleway_both_separation_both:
                cycleway_right_separation_left = cycleway_both_separation_both
            if cycleway_both_separation_left:
                cycleway_right_separation_left = cycleway_both_separation_left
            if cycleway_right_separation:
                cycleway_right_separation_left = cycleway_right_separation
            if cycleway_right_separation_both:
                cycleway_right_separation_left = cycleway_right_separation_both
        if not cycleway_right_separation_right:
            if cycleway_separation_right:
                cycleway_right_separation_right = cycleway_separation_right
            if cycleway_separation_both:
                cycleway_right_separation_right = cycleway_separation_both
            if cycleway_both_separation_both:
                cycleway_right_separation_right = cycleway_both_separation_both
            if cycleway_both_separation_right:
                cycleway_right_separation_right = cycleway_both_separation_right
            if cycleway_right_separation_both:
                cycleway_right_separation_right = cycleway_right_separation_both
        if not cycleway_left_separation_left:
            if cycleway_separation:
                cycleway_left_separation_left = cycleway_separation
            if cycleway_separation_left:
                cycleway_left_separation_left = cycleway_separation_left
            if cycleway_separation_both:
                cycleway_left_separation_left = cycleway_separation_both
            if cycleway_both_separation:
                cycleway_left_separation_left = cycleway_both_separation
            if cycleway_both_separation_both:
                cycleway_left_separation_left = cycleway_both_separation_both
            if cycleway_both_separation_left:
                cycleway_left_separation_left = cycleway_both_separation_left
            if cycleway_left_separation:
                cycleway_left_separation_left = cycleway_left_separation
            if cycleway_left_separation_both:
                cycleway_left_separation_left = cycleway_left_separation_both
        if not cycleway_left_separation_right:
            if cycleway_separation_right:
                cycleway_left_separation_right = cycleway_separation_right
            if cycleway_separation_both:
                cycleway_left_separation_right = cycleway_separation_both
            if cycleway_both_separation_both:
                cycleway_left_separation_right = cycleway_both_separation_both
            if cycleway_both_separation_right:
                cycleway_left_separation_right = cycleway_both_separation_right
            if cycleway_left_separation_both:
                cycleway_left_separation_right = cycleway_left_separation_both

        if not cycleway_right_marking_left:
            if cycleway_marking:
                cycleway_right_marking_left = cycleway_marking
            if cycleway_marking_left:
                cycleway_right_marking_left = cycleway_marking_left
            if cycleway_marking_both:
                cycleway_right_marking_left = cycleway_marking_both
            if cycleway_both_marking:
                cycleway_right_marking_left = cycleway_both_marking
            if cycleway_both_marking_both:
                cycleway_right_marking_left = cycleway_both_marking_both
            if cycleway_both_marking_left:
                cycleway_right_marking_left = cycleway_both_marking_left
            if cycleway_right_marking:
                cycleway_right_marking_left = cycleway_right_marking
            if cycleway_right_marking_both:
                cycleway_right_marking_left = cycleway_right_marking_both
        if not cycleway_right_marking_right:
            if cycleway_marking_right:
                cycleway_right_marking_right = cycleway_marking_right
            if cycleway_marking_both:
                cycleway_right_marking_right = cycleway_marking_both
            if cycleway_both_marking_both:
                cycleway_right_marking_right = cycleway_both_marking_both
            if cycleway_both_marking_right:
                cycleway_right_marking_right = cycleway_both_marking_right
            if cycleway_right_marking_both:
                cycleway_right_marking_right = cycleway_right_marking_both
        if not cycleway_left_marking_left:
            if cycleway_marking:
                cycleway_left_marking_left = cycleway_marking
            if cycleway_marking_left:
                cycleway_left_marking_left = cycleway_marking_left
            if cycleway_marking_both:
                cycleway_left_marking_left = cycleway_marking_both
            if cycleway_both_marking:
                cycleway_left_marking_left = cycleway_both_marking
            if cycleway_both_marking_both:
                cycleway_left_marking_left = cycleway_both_marking_both
            if cycleway_both_marking_left:
                cycleway_left_marking_left = cycleway_both_marking_left
            if cycleway_left_marking:
                cycleway_left_marking_left = cycleway_left_marking
            if cycleway_left_marking_both:
                cycleway_left_marking_left = cycleway_left_marking_both
        if not cycleway_left_marking_right:
            if cycleway_marking_right:
                cycleway_left_marking_right = cycleway_marking_right
            if cycleway_marking_both:
                cycleway_left_marking_right = cycleway_marking_both
            if cycleway_both_marking_both:
                cycleway_left_marking_right = cycleway_both_marking_both
            if cycleway_both_marking_right:
                cycleway_left_marking_right = cycleway_both_marking_right
            if cycleway_left_marking_both:
                cycleway_left_marking_right = cycleway_left_marking_both

        if not cycleway_right_lane:
            if cycleway_lane:
                cycleway_right_lane = cycleway_lane
            if cycleway_both_lane:
                cycleway_right_lane = cycleway_both_lane
        if not cycleway_left_lane:
            if cycleway_lane:
                cycleway_left_lane = cycleway_lane
            if cycleway_both_lane:
                cycleway_left_lane = cycleway_both_lane

        buffer_left_lanes = []
        buffer_right_lanes = []
        separation_left_lanes = []
        separation_right_lanes = []
        marking_left_lanes = []
        marking_right_lanes = []
        cw_lane_lanes = []

        for i in range(lanes):
            if lanes_dict['access_lanes'][lane.attribute('id')][i] == 'bicycle' or lanes_dict['cycleway_lanes'][lane.attribute('id')][i] == 'lane':
                if i + 1 <= lanes_backward:
                    buffer_left_lanes.append(float(cycleway_left_buffer_left))
                    buffer_right_lanes.append(float(cycleway_left_buffer_right))
                    separation_left_lanes.append(cycleway_left_separation_left)
                    separation_right_lanes.append(cycleway_left_separation_right)
                    marking_left_lanes.append(cycleway_left_marking_left)
                    marking_right_lanes.append(cycleway_left_marking_right)
                    cw_lane_lanes.append(cycleway_left_lane)
                else:
                    buffer_left_lanes.append(float(cycleway_right_buffer_left))
                    buffer_right_lanes.append(float(cycleway_right_buffer_right))
                    separation_left_lanes.append(cycleway_right_separation_left)
                    separation_right_lanes.append(cycleway_right_separation_right)
                    marking_left_lanes.append(cycleway_right_marking_left)
                    marking_right_lanes.append(cycleway_right_marking_right)
                    cw_lane_lanes.append(cycleway_right_lane)
            else:
                buffer_left_lanes.append(0)
                buffer_right_lanes.append(0)
                separation_left_lanes.append(NULL)
                separation_right_lanes.append(NULL)
                marking_left_lanes.append(lanes_dict['marking_left_lanes'][lane.attribute('id')][i]) #marking kann bereits vorher durch change oder overtaking spezifiziert worden sein
                marking_right_lanes.append(lanes_dict['marking_right_lanes'][lane.attribute('id')][i])
                cw_lane_lanes.append(NULL)

        lanes_dict['buffer_left_lanes'][lane.attribute('id')] = buffer_left_lanes
        lanes_dict['buffer_right_lanes'][lane.attribute('id')] = buffer_right_lanes
        lanes_dict['separation_left_lanes'][lane.attribute('id')] = separation_left_lanes
        lanes_dict['separation_right_lanes'][lane.attribute('id')] = separation_right_lanes
        lanes_dict['marking_left_lanes'][lane.attribute('id')] = marking_left_lanes
        lanes_dict['marking_right_lanes'][lane.attribute('id')] = marking_right_lanes
        lanes_dict['cw_lane_lanes'][lane.attribute('id')] = cw_lane_lanes

        #Radstreifen rechts von parkenden Fahrzeugen: zusätzlichen Versatz durch dazwischenliegenden Parkstreifen berücksichtigen (extra_offset)
        extra_offset_left = extra_offset_right = 0
        if cycleway_left_traffic_mode_left:
            if 'parking' in cycleway_left_traffic_mode_left:
                extra_offset_left = 1
        if cycleway_right_traffic_mode_left:
            if 'parking' in cycleway_right_traffic_mode_left:
                extra_offset_right = 1
        if cycleway_both_traffic_mode_left:
            if 'parking' in cycleway_both_traffic_mode_left:
                extra_offset_left = 1
                extra_offset_right = 1
        if cycleway_both_traffic_mode_both:
            if 'parking' in cycleway_both_traffic_mode_both:
                extra_offset_left = 1
                extra_offset_right = 1

        if extra_offset_left:
            if parking_left_width:
                extra_offset_left = float(parking_left_width)
            else:
                extra_offset_left = parking_width_default
        if extra_offset_right:
            if parking_right_width:
                extra_offset_right = float(parking_right_width)
            else:
                extra_offset_right = parking_width_default
        lanes_dict['extra_offset_left'][lane.attribute('id')] = extra_offset_left
        lanes_dict['extra_offset_right'][lane.attribute('id')] = extra_offset_right

        #Offset/Position der linkesten Spur an evtl. vorhandene Puffer und extra-offset anpassen
        for i in range(lanes):
            if i <= lanes_backward:
                offset += buffer_left_lanes[i]
                if i > 0:
                   offset += buffer_right_lanes[i]
        offset += extra_offset_left

        #Richtung jeder einzelnen Spur ermitteln (mit oder entgegen des OSM-Liniensegments)
        reverse_list = []
        reverse_count = 0
        if oneway == '-1': #TODO: Berücksichtigt keine entgegengesetzten Radspuren für den Fall oneway=-1?
            reverse_count = lanes
        elif oneway != 'yes' or (oneway == 'yes' and oneway_bicycle == 'no'):
            if lanes_backward:
                reverse_count = lanes_backward
            elif lanes_forward:
                reverse_count = lanes - lanes_forward
            else:
                reverse_count = int(lanes / 2)
        for l in range(lanes):
            if l < reverse_count:
                reverse_list.append(1)
            else:
                reverse_list.append(0)
        lanes_dict['reverse_lanes'][lane.attribute('id')] = reverse_list
        lanes_dict['placement'][lane.attribute('id')] = placement
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('offset'), offset)

    layer_lanes.commitChanges()

    layer_highway_lanes = layer_lanes

    QgsProject.instance().addMapLayer(layer_lanes, False)
    layer_lanes.startEditing()
    #zusammenfallende Linien an Verzweigungspunkten von Zweirichtungsfahrbahnen durch Versatz entschärfen
    if layer_lanes.fields().indexOf('dual_carriageway') != -1:
        print(time.strftime('%H:%M:%S', time.localtime()), '   Korrigiere Verzweigungspunkte...')
#       #damit Zweirichtungsfahrbahnen mit gleichen Eigenschaften keine Ringe bilden, Segmente an Linienschnittpunkten teilen
#       layer_lanes = processing.run('native:splitwithlines', { 'INPUT' : layer_lanes, 'LINES' : layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']

        #Zweirichtungsfahrbahnen auswählen (dual_carriageway)
        layer_lanes_dual_carriageway = processing.run('qgis:extractbyattribute', { 'INPUT' : layer_lanes, 'FIELD' : 'dual_carriageway', 'VALUE' : 'yes', 'OUTPUT': 'memory:'})['OUTPUT']

#       layer_lanes_dual_carriageway = processing.run('native:dissolve', { 'FIELD' : lanes_attributes, 'INPUT' : layer_lanes_dual_carriageway, 'OUTPUT': 'memory:'})['OUTPUT']
#       Achtung: Sollte "dissolve" mit "lanes_attributes" irgendwann wieder verwendet werden, muss eine angepasste Liste ohne "id" verwendet werden!
#       layer_lanes_dual_carriageway = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_lanes_dual_carriageway, 'OUTPUT': 'memory:'})['OUTPUT']
#       layer_lanes_dual_carriageway = processing.run('native:splitwithlines', { 'INPUT' : layer_lanes_dual_carriageway, 'LINES' : layer_lanes_dual_carriageway, 'OUTPUT': 'memory:'})['OUTPUT']

        #Start- und End-Vertices auswählen
        layer_dual_carriageways_vertices = processing.run('native:extractspecificvertices', { 'INPUT' : layer_lanes_dual_carriageway, 'VERTICES' : '0,-1', 'OUTPUT': 'memory:'})['OUTPUT']
        #Stützpunkte mit Liniensegmenten ohne dual_carriageway verschneiden, um nur Verzweigungspunkte zu erhalten
        layer_lanes_single_carriageway = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_lanes, 'EXPRESSION' : '"dual_carriageway" IS NOT \'yes\' and ("lane_markings" IS \'yes\' or "turn_lanes" IS \'yes\')', 'OUTPUT': 'memory:'})['OUTPUT']
        processing.run('native:selectbylocation', {'INPUT' : layer_dual_carriageways_vertices, 'INTERSECT' : layer_lanes_single_carriageway, 'METHOD' : 0, 'PREDICATE' : [4]})
        #Stützpunkte in Kreuzungsbereichen (area_highway/junction) aus der Auswahl entfernen -> alle übriggebliebenen sollten (meist) Verzweigungspunkte sein
        #---diese Beschränkung ist eigentlich unnötig, daher auskommentiert – bzw. sollte, wenn überhaupt, auf Knotenpunktbereiche ohne "lane_markings=yes" beschränkt bleiben
        #processing.run('native:selectbylocation', {'INPUT' : layer_dual_carriageways_vertices, 'INTERSECT' : layer_junction_areas, 'METHOD' : 3, 'PREDICATE' : [6] })


#        QgsProject.instance().addMapLayer(layer_dual_carriageways_vertices, True)


        #Koordinaten der ausgewählten Punkte speichern
        vertex_list = []
        for vertex in layer_dual_carriageways_vertices.selectedFeatures():
            vertex_x = vertex.geometry().asPoint().x()
            vertex_y = vertex.geometry().asPoint().y()

            vertex_list.append([vertex_x, vertex_y])

        #alle Zweirichtungs-Segmente durchgehen und verzweigende Start-/End-Vertices versetzen
#        layer_lanes.startEditing()
        for lane in layer_lanes.getFeatures():
            #nur explizit getaggte Fahrspuren behandeln
            if lane.attribute('dual_carriageway') != 'yes':
                continue
            #nur Fahrspuren behandeln, die ein Vorgänger- oder Nachfolgersegment gleichen Namens ohne "dual_carriageway" haben
            layer_lanes.removeSelection()
            layer_lanes.select(lane.id())
            layer_connected_lanes = processing.run('native:extractbylocation', { 'INPUT' : layer_lanes, 'INTERSECT' : QgsProcessingFeatureSourceDefinition(layer_lanes.id(), selectedFeaturesOnly=True), 'PREDICATE' : [4], 'OUTPUT': 'memory:'})['OUTPUT']
            do_offset = 0
            for connected_lane in layer_connected_lanes.getFeatures():
                if connected_lane.attribute('name') == lane.attribute('name') and connected_lane.attribute('dual_carriageway') != 'yes':
                    do_offset = 1

            #nicht versetzen, wenn placement:start/:end verwendet wird
            if layer_lanes.fields().indexOf('placement:start') != -1:
                placement_start = lane.attribute('placement:start')
            if layer_lanes.fields().indexOf('placement:forward:start') != -1:
                placement_forward_start = lane.attribute('placement:forward:start')
            if layer_lanes.fields().indexOf('placement:backward:start') != -1:
                placement_backward_start = lane.attribute('placement:backward:start')
            if placement_start or placement_forward_start or placement_backward_start:
                do_offset = 0

            if not do_offset:
                continue
            vertex_count = len(lane.geometry().asPolyline())
            geom = lane.geometry()
            start_vertex_x = geom.vertexAt(0).x()
            start_vertex_y = geom.vertexAt(0).y()
            end_vertex_x = geom.vertexAt(vertex_count - 1).x()
            end_vertex_y = geom.vertexAt(vertex_count - 1).y()
            move_start_vertex = move_end_vertex = NULL
            if [start_vertex_x, start_vertex_y] in vertex_list:
                move_start_vertex = 1
            if [end_vertex_x, end_vertex_y] in vertex_list:
                move_end_vertex = 1

            if move_start_vertex != 1 and move_end_vertex != 1:
                continue

            if move_start_vertex == 1:
                offset = offsetVertex(layer_lanes, layer_lanes_single_carriageway, lane, geom, 0, start_vertex_x, start_vertex_y)
                xv = offset[0]
                yv = offset[1]
                layer_lanes.moveVertex(start_vertex_x + xv, start_vertex_y + yv, lane.id(), 0)

            if move_end_vertex == 1:
                offset = offsetVertex(layer_lanes, layer_lanes_single_carriageway, lane, geom, vertex_count - 1, end_vertex_x, end_vertex_y)
                xv = offset[0]
                yv = offset[1]
                layer_lanes.moveVertex(end_vertex_x + xv, end_vertex_y + yv, lane.id(), vertex_count - 1)

#    layer_lanes.commitChanges()
    layer_lanes.removeSelection()

    #placement=transition-Segmente passend verschieben
    print(time.strftime('%H:%M:%S', time.localtime()), '   Korrigiere placement transition...')
#    layer_lanes.startEditing()
    for lane in layer_lanes.getFeatures():
        id_lane = lane.attribute('id')
        id_lane_after = NULL
        if id_lane in transition_dict:
            #Start- und Ziel-Lage von placement=transition-Segmenten ermitteln
            placement_to = transition_dict[id_lane][0]
            placement_from = transition_dict[id_lane][2]
            if not placement_to:
                if len(lanes_dict['segments_after'][id_lane]['id']):
                    id_lane_after = lanes_dict['segments_after'][id_lane]['id'][0]
                    placement_to = lanes_dict['placement'][id_lane_after]
                else:
                    print('placement-transition-Prozess übersprungen - kein Anschlusssegment: ', id_lane)
                    continue

            fix = transition_dict[id_lane][1]
            if fix:
                id_lane_before = NULL
                if len(lanes_dict['segments_before'][id_lane]['id']):
                    id_lane_before = lanes_dict['segments_before'][id_lane]['id'][0]
                if id_lane_before:
                    if not placement_to:
                        if id_lane_after:
                            placement_to = lanes_dict['placement'][id_lane_after]
                        else:
                            placement_to = 'middle_of:1'
                    if not placement_from:
                        placement_from = lanes_dict['placement'][id_lane_before]
                elif not placement_from:
                    placement_from = 'middle_of:1'
            elif not placement_from:
                placement_from = lanes_dict['placement'][id_lane]

            i_from = -(len(placement_from) - placement_from.find(':') - 1)
            i_to = -(len(placement_to) - placement_to.find(':') - 1)
            placement_pos_from = placement_from[0:i_from]
            placement_pos_to = placement_to[0:i_to]
            placement_lane_from = placement_lane_from_value = int(placement_from[i_from:])
            placement_lane_to = placement_lane_to_value = int(placement_to[i_to:])

            #ein Ende des Segments versetzen (das Ende zur Richtung mit mehr Fahrspuren)
            #placement in einen Zahlwert umrechnen von 0 (linker Fahrbahnrand), 0.5 (Mitte der 1. Spur), 1 (rechts der 1. Spur) usw.
            if placement_pos_from == 'left_of:':
                placement_lane_from_value -= 1
            if placement_pos_from == 'middle_of:':
                placement_lane_from_value -= 0.5
            if placement_pos_to == 'left_of:':
                placement_lane_to_value -= 1
            if placement_pos_to == 'middle_of:':
                placement_lane_to_value -= 0.5

            #Linie entsprechend versetzen, ob die forward- oder backward-Spuren zunehmen
            #aber nur, wenn keine placement:start/:end angegeben
            if layer_lanes.fields().indexOf('placement:start') != -1:
                placement_start = lane.attribute('placement:start')
            if layer_lanes.fields().indexOf('placement:forward:start') != -1:
                placement_forward_start = lane.attribute('placement:forward:start')
            if layer_lanes.fields().indexOf('placement:backward:start') != -1:
                placement_backward_start = lane.attribute('placement:backward:start')
            if not placement_start and not placement_forward_start and not placement_backward_start:
                if len(lanes_dict['segments_before'][id_lane]['id']):
                    id_lane_before = lanes_dict['segments_before'][id_lane]['id'][0]
                    lanes_forward_before = lanes_dict['reverse_lanes'][id_lane_before].count(0)
                    lanes_backward_before = lanes_dict['reverse_lanes'][id_lane_before].count(1)
                else:
                    lanes_forward_before = 1
                    lanes_backward_before = 0
                if len(lanes_dict['segments_after'][id_lane]['id']):
                    id_lane_after = lanes_dict['segments_after'][id_lane]['id'][0]
                    lanes_forward_after = lanes_dict['reverse_lanes'][id_lane_after].count(0)
                    lanes_backward_after = lanes_dict['reverse_lanes'][id_lane_after].count(1)
                else:
                    lanes_forward_after = 1
                    lanes_backward_after = 0

                if lanes_backward_after > 0:
                    if fix:
                        if lanes_backward_before > lanes_backward_after:
                            lane_value_diff = placement_lane_from_value - placement_lane_to_value
                        else:
                            lane_value_diff = placement_lane_to_value - placement_lane_from_value
                    else:
                        if lanes_backward_after > lanes_backward_before:
                            lane_value_diff = placement_lane_to_value - placement_lane_from_value
                        else:
                            lane_value_diff = placement_lane_from_value - placement_lane_to_value
                else:
                    if fix:
                        lane_value_diff = placement_lane_to_value - placement_lane_from_value
                    else:
                        lane_value_diff = placement_lane_from_value - placement_lane_to_value
            else:
                if fix:
                    lane_value_diff = placement_lane_to_value - placement_lane_from_value
                else:
                    lane_value_diff = placement_lane_from_value - placement_lane_to_value
#            if (lanes_forward_after < lanes_forward_before and fix) or (lanes_forward_after > lanes_forward_before and not fix):
#                lane_value_diff = placement_lane_to_value - placement_lane_from_value
#            else:
#                lane_value_diff = placement_lane_from_value - placement_lane_to_value
            lane_value_min = min(placement_lane_from_value, placement_lane_to_value)
            lane_value_max = max(placement_lane_from_value, placement_lane_to_value)

            dist = 0
#            width_list = []
#            #die längere der beiden Breiten-Listen nehmen, falls unterschiedlich, um alle Spuren zu finden
            width_list = lanes_dict['width_lanes'][id_lane]
            lanes = len(width_list)
#            lanes_after = 1
#            if id_lane_after != NULL:
#                lanes_after = len(lanes_dict['width_lanes'][id_lane_after])
#                if lanes < lanes_after:
#                    width_list = lanes_dict['width_lanes'][id_lane_after]

            if lane_value_diff != 0:
                for j in range(lanes): # für jede Spur ermitteln, ob sie innerhalb der Versatzdifferenz liegt
                    if lane_value_min <= j: #wenn linker Versatzpunkt mindestens links der Spur liegt:
                        if lane_value_max - j > 0: #wenn rechter Versatzpunkt mindestens mittig der Spur oder rechts davon liegt:
                            dist += float(width_list[j]) * (min(lane_value_max - j, 1)) #um (halbe oder ganze) Spurbreite versetzen
                    elif lane_value_min == j + 0.5: #wenn linker Versatzpunkt mittig der Spur liegt...
                        if lane_value_max >= j + 1: #...und der rechte rechts der Spur:
                            dist += float(width_list[j]) / 2 #eine halbe Breite dieser Spur einbeziehen
                if lane_value_diff < 0:
                    dist = -dist

            #quick & dirty Workaround für seltene Situationen mit negativen placement-Attributen (z.B. placement:end=middle_of:-1)
            if placement_lane_from < 0 or placement_lane_to < 0:
                extra_dist_from = extra_dist_to = 0
                if placement_lane_from < 0:
                    extra_dist_from = abs(placement_lane_from)
                    if placement_pos_from == 'right_of:':
                        extra_dist_from -= 1
                    if placement_pos_from == 'middle_of:':
                        extra_dist_from -= 0.5
                if placement_lane_to < 0:
                    extra_dist_to = abs(placement_lane_to)
                    if placement_pos_to == 'right_of:':
                        extra_dist_to -= 1
                    if placement_pos_to == 'middle_of:':
                        extra_dist_to -= 0.5
                dist += (extra_dist_from + extra_dist_to) * 3 #TODO: statt default-Breite von 3m korrekte Spurbreiten aus Gegenrichtung auslesen

            #quick & dirty Workaround für seltene Situationen mit beidseitig wechselnden Spurattributen
            #TODO: generelle Gültigkeit unklar!
            if not placement_start and not placement_forward_start and not placement_backward_start:
                if lanes_forward_before < lanes_forward_after and lanes_backward_before > lanes_backward_after:
                    if lanes_dict['reverse_lanes'][id_lane].count(1) != lanes_backward_after:
                        if fix:
                            dist += width_list[lanes_forward_after - 1]
                        else:
                            dist -= width_list[lanes_forward_after - 1]

            offsetLaneTransition(layer_lanes, lane, dist, fix)

    layer_lanes.commitChanges()

    #Linie in die Mitte der linken Spur verschieben (im Layer auswählen, dann ausgewählte Spuren des Layers verschieben)
    layer_lanes = processing.run('native:offsetline', {'INPUT': layer_lanes, 'DISTANCE' : QgsProperty.fromExpression('"offset"'), 'JOIN_STYLE' : 1, 'OUTPUT': 'memory:'})['OUTPUT']

    #Einzellinien für jede Spur durch Versatz erzeugen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Erzeuge Fahrspuren...')
    layer_lanes = processing.run('native:arrayoffsetlines', {'INPUT': layer_lanes, 'COUNT' : QgsProperty.fromExpression('"lanes" - 1'), 'OFFSET' : - lane_width_default, 'JOIN_STYLE' : 1, 'OUTPUT': 'memory:'})['OUTPUT']

#    QgsProject.instance().addMapLayer(layer_lanes, True)

    #Spurattribute für Einzelspuren erzeugen
    layer_lanes.startEditing()

    for lane in layer_lanes.getFeatures():
        #Gruppen-/Fahrbahn-Attribute auslesen
        instance = int(lane.attribute('instance'))
        lanes = int(lane.attribute('lanes'))
        lanes_forward = int(lane.attribute('lanes:forward'))
        lanes_backward = int(lane.attribute('lanes:backward'))
        placement = lane.attribute('placement_abs')
        oneway = lane.attribute('oneway')
        oneway_bicycle = lane.attribute('oneway:bicycle')

        #individuellen Versatz entsprechend der Spurbreiten, Puffer und extra-offsets ermitteln und nachjustieren
        width_lanes = lanes_dict['width_lanes'][lane.attribute('id')]
        buffer_left_lanes = lanes_dict['buffer_left_lanes'][lane.attribute('id')]
        buffer_right_lanes = lanes_dict['buffer_right_lanes'][lane.attribute('id')]
        extra_offset_left = lanes_dict['extra_offset_left'][lane.attribute('id')]
        extra_offset_right = lanes_dict['extra_offset_right'][lane.attribute('id')]
        width_default = width_sum = offset_delta = buffer = 0
        i = 0
        if lanes > 1:
            width_default_offset = lane_width_default - float(width_lanes[0])
            for i in range(instance):
                if i == 0:
                    width_default += lane_width_default / 2
                    width_default += width_default_offset / 2
                    width_sum += float(width_lanes[i]) / 2
                    buffer += float(buffer_left_lanes[i])
                else:
                    width_default += lane_width_default
                    width_sum += float(width_lanes[i])
                    buffer += float(buffer_left_lanes[i]) + float(buffer_right_lanes[i])
            width_default += lane_width_default / 2
            width_sum += float(width_lanes[instance]) / 2
            width_sum += width_default_offset / 2
            offset_delta = width_default - width_sum - buffer
            #extra-offset (Sonderfall parkende Fahrzeuge links von Radstreifen) nicht bei der äußersten linken Spur anwenden
            if instance != 0:
                offset_delta -= extra_offset_left
            #extra-offset für rechteste Spur
            if instance == lanes - 1:
                offset_delta -= extra_offset_right + buffer_left_lanes[instance]

#            for i in range(instance):
#                if i == 0:
#                    width_default += lane_width_default / 2
#                    width_sum += float(width_lanes[i]) / 2
#                else:
#                    width_default += lane_width_default
#                    width_sum += float(width_lanes[i])
#            width_default += lane_width_default / 2
#            width_sum += float(width_lanes[instance]) / 2
#            offset_delta = width_default - width_sum
#

        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('offset_delta'), offset_delta)

        #Weitere Spurattribute individuell zuordnen:
        # > Spurrichtung
        reverse_lanes = lanes_dict['reverse_lanes'][lane.attribute('id')]
        reverse = reverse_lanes[instance]
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('reverse'), reverse)

        # > Abbiegespur-Richtung
        turn_lanes = lanes_dict['turn_lanes'][lane.attribute('id')]
        turn = turn_lanes[instance]
        #leere oder ungewöhnliche Werte normieren
        if turn == '':
            turn = 'none'
        if turn == 'slight_left' or turn == 'sharp_left' or turn == 'reverse':
            turn = 'left'
        if turn == 'slight_right' or turn == 'sharp_right':
            turn = 'right'
        if turn == 'through;left':
            turn = 'left;through'
        if turn == 'right;through':
            turn = 'through;right'
        if turn == 'slide_left':
            turn = 'merge_to_left'
        if turn == 'slide_right':
            turn = 'merge_to_right'
        if not turn in ['through', 'left', 'right', 'left;through', 'through;right', 'merge_to_left', 'merge_to_right']:
            turn = 'none'
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('turn'), turn)

        # > Breite
        width_lanes = lanes_dict['width_lanes'][lane.attribute('id')]
        width = width_lanes[instance]
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('width'), width)

        # > access (Kfz/Bus/Fahrrad)
        access_lanes = lanes_dict['access_lanes'][lane.attribute('id')]
        access = access_lanes[instance]
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('access'), access)

        # > Puffer
        buffer_left_lanes = lanes_dict['buffer_left_lanes'][lane.attribute('id')]
        buffer_left = buffer_left_lanes[instance]
        buffer_right_lanes = lanes_dict['buffer_right_lanes'][lane.attribute('id')]
        buffer_right = buffer_right_lanes[instance]
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('buffer:left'), buffer_left)
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('buffer:right'), buffer_right)

        # > separation
        separation_left_lanes = lanes_dict['separation_left_lanes'][lane.attribute('id')]
        separation_left = separation_left_lanes[instance]
        separation_right_lanes = lanes_dict['separation_right_lanes'][lane.attribute('id')]
        separation_right = separation_right_lanes[instance]
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('separation:left'), separation_left)
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('separation:right'), separation_right)

        # > Markierung der Linie (üblicherweise links der Spur)
        marking_left_lanes = lanes_dict['marking_left_lanes'][lane.attribute('id')]
        marking_left = marking_left_lanes[instance]
        marking_right_lanes = lanes_dict['marking_right_lanes'][lane.attribute('id')]
        marking_right = marking_right_lanes[instance]

        # > cycleway:lane
        cw_lane_lanes = lanes_dict['cw_lane_lanes'][lane.attribute('id')]
        cw_lane = cw_lane_lanes[instance]
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('cw_lane'), cw_lane)

        cycleway_lanes = lanes_dict['cycleway_lanes'][lane.attribute('id')]
        cycleway = cycleway_lanes[instance]
        if cycleway == 'lane':
            access = 'bicycle'
            layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('access'), access)
            lanes_dict['access_lanes'][lane.attribute('id')][instance] = access

        surface_colour = 'none'
        clr = NULL
        if access == 'bicycle':
            # > Oberflächenfarbe von Radwegen ermitteln
            if layer_lanes.fields().indexOf('cycleway:both:surface:colour') != -1:
                clr = lane.attribute('cycleway:both:surface:colour')
                if clr:
                    surface_colour = clr
            if surface_colour == 'none' and layer_lanes.fields().indexOf('cycleway:surface:colour') != -1:
                clr = lane.attribute('cycleway:surface:colour')
                if clr:
                    surface_colour = clr
            if instance + 1 > lanes_backward:
                if layer_lanes.fields().indexOf('cycleway:right:surface:colour') != -1:
                    clr = lane.attribute('cycleway:right:surface:colour')
                    if clr:
                        surface_colour = clr
            elif layer_lanes.fields().indexOf('cycleway:left:surface:colour') != -1:
                clr = lane.attribute('cycleway:left:surface:colour')
                if clr:
                    surface_colour = clr

            # > Art der Linienmarkierung ableiten
            #...in Linienrichtung
            if marking_left:
                if 'solid_line' in marking_left:
                    marking_left = 'solid_line'
                elif 'dashed_line' in marking_left:
                    marking_left = 'dashed_line'
                else:
                    marking_left = 'unspecified'
            #cycleway:lanes-Schema als Backup, falls keine Markierung angegeben ist
            if not marking_left or marking_left == 'unspecified':
                if cw_lane:
                    if cw_lane == 'exclusive':
                        marking_left = 'solid_line'
                    if cw_lane == 'advisory':
                        marking_left = 'dashed_line'
            if marking_right:
                if 'solid_line' in marking_right:
                    marking_right = 'solid_line'
                elif 'dashed_line' in marking_right:
                    marking_right = 'dashed_line'
                else:
                    marking_right = 'no'

            if marking_right != 'dashed_line' and marking_right != 'solid_line':
                #Radstreifen in Mittellage: Wenn nicht anders angegeben, von gestrichelter Linie ausgehen
                if instance != 0 and instance != lanes - 1:
                    if (not reverse and access_lanes[instance + 1] == 'vehicle') or (reverse and access_lanes[instance - 1] == 'vehicle'):
                        marking_right = 'dashed_line'

        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('surface:colour'), surface_colour)
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('marking:left'), marking_left)
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('marking:right'), marking_right)

        #eindeutige Kennung aus ID und Fahrspur-instance erzeugen, um später beispielsweise Nachbarspuren abzufragen
        id_instance = str(lane.attribute('id')) + '_' + str(lane.attribute('instance'))
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('id_instance'), id_instance)

    layer_lanes = processing.run('native:offsetline', {'INPUT': layer_lanes, 'DISTANCE' : QgsProperty.fromExpression('"offset_delta"'), 'JOIN_STYLE' : 1, 'OUTPUT': 'memory:'})['OUTPUT']

    #Mehrteilige Geometrien wieder zusammenfügen
    layer_lanes = processing.run('native:dissolve', { 'FIELD' : ['id_instance'], 'INPUT' : layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']

    QgsProject.instance().addMapLayer(layer_lanes, False)

    print(time.strftime('%H:%M:%S', time.localtime()), '   Bereite Fahrspuren auf...')

    #Spurrichtung anpassen (Segmente in Gegenrichtung umkehren und wieder mit nicht gedrehten Spuren zusammenführen)
    layer_lanes.removeSelection()
    for lane in layer_lanes.getFeatures():
        if lane.attribute('reverse') == '1':
            layer_lanes.select(lane.id())
    layer_lanes_reversed = processing.run('native:reverselinedirection', {'INPUT' : QgsProcessingFeatureSourceDefinition(layer_lanes.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']
    features = layer_lanes.getFeatures()
    ids = [ f.id() for f in features if f.attribute('reverse') == '1']
    with edit(layer_lanes):
        layer_lanes.deleteFeatures(ids)

    layer_lanes = processing.run('native:mergevectorlayers', {'LAYERS' : [layer_lanes, layer_lanes_reversed], 'OUTPUT': 'memory:'})['OUTPUT']

    #Spurversätze korrigieren durch Angleichung einer Spur an ihre Vorgängerspur
    with edit(layer_lanes):
        for lane in layer_lanes.getFeatures():
            segments_before = lanes_dict['segments_before'][lane.attribute('id')]
            num_segments_before = len(segments_before['id'])
            num_lanes = len(lanes_dict['width_lanes'][lane.attribute('id')])

            #keine angrenzenden Segmente: kein Handlungsbedarf
            if num_segments_before < 1:
                continue

            instance = lane.attribute('instance')
            geom_lane = lane.geometry()
            vertex_count = getVertexCount(geom_lane)

            if num_segments_before == 1:
                num_lanes_before = len(lanes_dict['width_lanes'][segments_before['id'][0]])
                processing.run('qgis:selectbyattribute', { 'INPUT' : layer_lanes, 'FIELD' : 'id', 'VALUE' : segments_before['id'][0]})

                #kein Handlungsbedarf, wenn Spurattribute gleich sind
                if num_lanes == num_lanes_before:
                    width_lanes = lanes_dict['width_lanes'][lane.attribute('id')]
                    width_lanes_before = lanes_dict['width_lanes'][segments_before['id'][0]]
                    if width_lanes == width_lanes_before:
                        #Segmente miteinander verbinden, wenn alle Spuren gleich sind
                        reverse_lanes = lanes_dict['reverse_lanes'][lane.attribute('id')]
                        if not segments_before['id'][0] in lanes_dict['reverse_lanes']:
                            continue
                        #außer bei entgegengesetzten Linien
                        if segments_before['inverted'][0] == 1:
                            continue
                        reverse_lanes_before = lanes_dict['reverse_lanes'][segments_before['id'][0]]
                        if reverse_lanes != reverse_lanes_before or lanes_dict['placement'][lane.attribute('id')] != lanes_dict['placement'][segments_before['id'][0]]:
                            continue
                        for lane_before in layer_lanes.getSelectedFeatures():
                            geom_lane_before = lane_before.geometry()
                            vertex_count_before = getVertexCount(geom_lane_before)
                            if lane.attribute('instance') == lane_before.attribute('instance'):
                                if lane.attribute('reverse') == '0':
                                    vertex = 0
                                    vertex_before = vertex_count_before - 1
                                else:
                                    vertex = vertex_count - 1
                                    if lane_before.attribute('reverse') == '0':
                                        vertex_before = vertex_count_before - 1
                                    else:
                                        vertex_before = 0
                                x_before = geom_lane_before.vertexAt(vertex_before).x()
                                y_before = geom_lane_before.vertexAt(vertex_before).y()
                                layer_lanes.moveVertex(x_before, y_before, lane.id(), vertex)
                        continue
#                #kein Handlungsbedarf bei gerader Differenz der Spurzahlen
#                if not abs(num_lanes - num_lanes_before) % 2:
#                    continue
                #TODO: kein Handlungsbedarf, wenn beide Segmente mit zueinander passenden placement-Attributen ausgestattet sind:
                #in placement_abs müsste dabei ein Versatz erkennbar sein von middle zu left/right
                #lanes_dict['placement'][id]

                #zueinander passende Fahrradspuren zusammenfügen: Vertex der Spur zum Vertex der Spur davor versetzen
                if lanes_dict['access_lanes'][lane.attribute('id')][instance] == 'bicycle':
                    for lane_before in layer_lanes.getSelectedFeatures():
                        #Nur Spuren miteinander vergleichen, die in die gleiche Richtung führen
                        if segments_before['inverted'][0] == 0:
                            if lane_before.attribute('reverse') != lane.attribute('reverse'):
                                continue
                        else:
                            if lane_before.attribute('reverse') == lane.attribute('reverse'):
                                continue
                        #TODO: Bei mehreren Fahrradspuren (Mittellage) zur mittleren Spur verknüpfen
                        if lanes_dict['access_lanes'][lane_before.attribute('id')][lane_before.attribute('instance')] == 'bicycle':
                            width_lane = float(lanes_dict['width_lanes'][lane.attribute('id')][lane.attribute('instance')])
                            width_lane_before = float(lanes_dict['width_lanes'][lane_before.attribute('id')][lane_before.attribute('instance')])
                            geom_lane_before = lane_before.geometry()
                            vertex_count_before = getVertexCount(geom_lane_before)

                            #Linien von der schmaleren zur breiteren Fahrbahn hin versetzen
                            if num_lanes < num_lanes_before:
                                if lane.attribute('reverse') == '0':
                                    vertex = vertex_count_before - 1
                                    vertex_before = 0
                                else:
                                    vertex = 0
                                    vertex_before = vertex_count - 1
                                x_before = geom_lane_before.vertexAt(vertex).x()
                                y_before = geom_lane_before.vertexAt(vertex).y()
                                #TODO: Prüfen, ob Koordinaten innerhalb einer Kreuzung sind - wenn ja, dann continue/nicht versetzen
                                if width_lane_before != width_lane:
                                    angle = math.degrees(geom_lane_before.angleAtVertex(vertex))
                                    distance = (width_lane - width_lane_before) / 2
                                    xv = math.sin(math.radians(90 - angle)) * distance
                                    yv = math.cos(math.radians(90 + angle)) * distance
                                    x_before += xv
                                    y_before += yv
                                layer_lanes.moveVertex(x_before, y_before, lane.id(), vertex_before)
                            else:
                                if lane.attribute('reverse') == '0':
                                    vertex = 0
                                    vertex_before = vertex_count_before - 1
                                else:
                                    vertex = vertex_count - 1
                                    vertex_before = 0
                                x = geom_lane.vertexAt(vertex).x()
                                y = geom_lane.vertexAt(vertex).y()
                                #TODO: Prüfen, ob Koordinaten innerhalb einer Kreuzung sind - wenn ja, dann continue/nicht versetzen
                                if width_lane_before != width_lane:
                                    angle = math.degrees(geom_lane_before.angleAtVertex(vertex))
                                    distance = (width_lane_before - width_lane) / 2
                                    xv = math.sin(math.radians(90 - angle)) * distance
                                    yv = math.cos(math.radians(90 + angle)) * distance
                                    x += xv
                                    y += yv
                                layer_lanes.moveVertex(x, y, lane_before.id(), vertex_before)
            #TODO: Schleifen für num_segments_before = 1 und >1 zusammenführen
            if num_segments_before > 1:
                if lanes_dict['access_lanes'][lane.attribute('id')][instance] == 'bicycle':
                    for j in range(0, num_segments_before):
                        processing.run('qgis:selectbyattribute', { 'INPUT' : layer_lanes, 'FIELD' : 'id', 'VALUE' : segments_before['id'][j]})
                        for lane_before in layer_lanes.getSelectedFeatures():
                            #Nur Spuren angleichen, die in die gleiche Richtung führen
                            if segments_before['inverted'][j] == 0:
                                if lane_before.attribute('reverse') != lane.attribute('reverse'):
                                    continue
                            else:
                                if lane_before.attribute('reverse') == lane.attribute('reverse'):
                                    continue

                            #TODO: Bei mehreren Fahrradspuren (Mittellage) zur mittleren Spur verknüpfen

                            if lane_before.attribute('access') == 'bicycle':
                                cyclelane_same_direction = cyclelane_before_same_direction = 0
                                reverse = lane.attribute('reverse')
                                for i in range(num_lanes):
                                    if lanes_dict['access_lanes'][lane.attribute('id')][i] == 'bicycle' and lanes_dict['reverse_lanes'][lane.attribute('id')][i] == reverse:
                                        cyclelane_same_direction += 1
                                num_lanes_before = len(lanes_dict['access_lanes'][segments_before['id'][j]])
                                reverse_before = lane_before.attribute('reverse')
                                for i in range(num_lanes_before):
                                    if lanes_dict['access_lanes'][lane_before.attribute('id')][i] == 'bicycle' and lanes_dict['reverse_lanes'][lane_before.attribute('id')][i] == reverse_before:
                                        cyclelane_before_same_direction += 1
                                if cyclelane_same_direction > 1 or cyclelane_before_same_direction > 1:
                                    #TODO: Umgang mit (seltener) Situation, wenn mehrere Radspuren pro Richtung aufeinandertreffen
                                    continue
                                else:
                                    if lane.attribute('reverse') == '0':
                                        vertex = 0
                                        geom_lane_before = lane_before.geometry()
                                        vertex_count_before = getVertexCount(geom_lane_before)
                                        vertex_before = vertex_count_before - 1
                                    else:
                                        vertex = vertex_count - 1
                                        vertex_before = 0
                                    x = geom_lane.vertexAt(vertex).x()
                                    y = geom_lane.vertexAt(vertex).y()
                                    if lane_before.attribute('width') != lane.attribute('width'):
                                        angle = math.degrees(geom_lane.angleAtVertex(vertex))
                                        distance = (float(lane.attribute('width')) - float(lane_before.attribute('width'))) / 2
                                        xv = math.sin(math.radians(90 - angle)) * distance
                                        yv = math.cos(math.radians(90 + angle)) * distance
                                        x += xv
                                        y += yv
                                    layer_lanes.moveVertex(x, y, lane_before.id(), vertex_before)

            #nur bei Radstreifen, zur besseren Verknüpfung untereinander:
            #prüfen, ob dieses Segment Folgesegmente gelistet hat, in denen dieses Segment nicht als Vorgänger auftaucht (relevant an Verzweigungspunkten mit Richtungswechsel)
            if lanes_dict['access_lanes'][lane.attribute('id')][instance] == 'bicycle':
                segments_after = lanes_dict['segments_after'][lane.attribute('id')]
                num_segments_after = len(segments_after['id'])
                if num_segments_after:
                    reciproc = 0
                    for i in range(0, num_segments_after):
                        processing.run('qgis:selectbyattribute', { 'INPUT' : layer_lanes, 'FIELD' : 'id', 'VALUE' : segments_after['id'][i]})
                        for lane_after in layer_lanes.getSelectedFeatures():

                            segments_before_of_segment_after = lanes_dict['segments_before'][lane_after.attribute('id')]
                            num_segments_before_of_segment_after = len(segments_before_of_segment_after['id'])
                            if num_segments_before_of_segment_after:
                                for j in range(0, num_segments_before_of_segment_after):
                                    if lanes_dict['segments_before'][lane_after.attribute('id')]['id'][j] == lane.attribute('id'):
                                        reciproc = 1
                    #bei diesen Segmenten auch zu den Nachfolgesegmenten verknüpfen
                    if not reciproc:
                        segments_after = lanes_dict['segments_after'][lane.attribute('id')]
                        num_segments_after = len(segments_after['id'])
                        if num_segments_after:
                            processing.run('qgis:selectbyattribute', { 'INPUT' : layer_lanes, 'FIELD' : 'id', 'VALUE' : segments_after['id'][0]})
                            for lane_after in layer_lanes.getSelectedFeatures():
                                #pragmatisch nur für die äußerste Spur anwenden, falls diese eine Radspur ist
                                if lane_after.attribute('access') == 'bicycle' and lane_after.attribute('reverse') and not lane_after.attribute('instance'):
                                    vertex = vertex_count - 1
                                    geom_lane_after = lane_after.geometry()
                                    vertex_count_after = getVertexCount(geom_lane_after)
                                    vertex_after = 0 #vertex_count_after - 1
                                    x = geom_lane_after.vertexAt(vertex_after).x()
                                    y = geom_lane_after.vertexAt(vertex_after).y()
                                    layer_lanes.moveVertex(x, y, lane.id(), vertex)
                                    continue

#TODO: Für Auflösung der Spuren nach gemeinsamen Merkmalen bräuchte es ein Attribut "is_middle_lane" o.ä., um Fahrspuren zu identifizieren, die an entgegengesetzte Fahrspuren angrenzen – das geht zur Zeit nur über lane und lane:forward – diese beiden Attribute beim Auflösen zu berücksichtigen, würde das Auflösen jedoch weitgehend unnütz machen
#    dissolve_attr = ['turn', 'reverse', 'width', 'access', 'surface:colour', 'lane_markings', 'marking:left', 'marking:right']
#    #für schönere/zusammenhängendere Markierungen nach gemeinsamen Merkmalen auflösen
#    layer_lanes = processing.run('native:dissolve', { 'FIELD' : dissolve_attr, 'INPUT' : layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']
#    layer_lanes = processing.run('native:multiparttosingleparts', {'INPUT' : layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']

    #Linien zur schöneren Darstellung noch einmal drehen (von der Kreuzung ausgehend beginnen – immer gleicher Markierungsabstand)
    layer_lanes = processing.run('native:reverselinedirection', {'INPUT' : layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']

    #Liste von Attributen, die an jeder Spur am Ende erhalten bleiben
#    list_lane_attributes = ['reverse', 'lane_markings', 'marking:left', 'marking:right', 'turn', 'width', 'access', 'surface:colour']
    list_lane_attributes = ['id', 'lanes', 'lanes:forward', 'id_instance', 'instance', 'reverse', 'lane_markings', 'marking:left', 'marking:right', 'buffer:left', 'buffer:right', 'separation:left', 'separation:right', 'cw_lane', 'turn', 'width', 'access', 'surface:colour', 'temporary']

    #Markierungen in Knotenpunktbereichen (in Kreuzungen) entfernen
    #Wenn "lane_markings:junction" = 'yes', "lane_markings:crossing" = 'yes' oder "cycleway:*type"='crossing' an der Straßenlinie, dann Markierungen dennoch darstellen
    #Wenn "lane_markings" = 'yes' an der Knotenpunktfläche, dann ebenfalls Markierungen dennoch darstellen
    QgsProject.instance().addMapLayer(layer_junction_areas, False)

    #Fahrradfurten in Knotenpunktbereichen separieren, um sie später wieder hinzuzufügen
    #aber Fahrradfurten ausschließen, die in Knotenpunkten mit genauer erfassten area:highway=cycleway-Flächen liegen
    layer_lanes_bicycle_crossing = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_lanes, 'EXPRESSION' : '"access" = \'bicycle\' and ("cycleway" = \'crossing\' or "cycleway:type" = \'crossing\' or "cycleway:both:type" = \'crossing\' or ("cycleway:right:type" = \'crossing\' and "reverse" = 0) or ("cycleway:left:type" = \'crossing\' and "reverse" = 1))', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_cycleway_junction_areas = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_area_highway_polygons, 'EXPRESSION' : '"area:highway" = \'cycleway\'', 'OUTPUT': 'memory:'})['OUTPUT']
    #Knotenpunktbereiche ohne Fahrradwegflächen auswählen und nur Fahrradfurten in solchen weiterverarbeiten
    processing.run('native:selectbylocation', {'INPUT' : layer_junction_areas, 'INTERSECT' : layer_cycleway_junction_areas, 'METHOD' : 0, 'PREDICATE' : [2]})
    layer_lanes_bicycle_crossing = processing.run('native:clip', {'INPUT': layer_lanes_bicycle_crossing, 'OVERLAY': QgsProcessingFeatureSourceDefinition(layer_junction_areas.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_junction_areas.removeSelection()

    processing.run('qgis:selectbyexpression', {'INPUT' : layer_junction_areas, 'EXPRESSION' : '"junction" = \'yes\' and "lane_markings" IS NOT \'yes\''})
    layer_lanes_no_junction_markings = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_lanes, 'EXPRESSION' : '"lane_markings:junction" IS NOT \'yes\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes_no_junction_markings = processing.run('native:difference', {'INPUT' : layer_lanes_no_junction_markings, 'OVERLAY' : QgsProcessingFeatureSourceDefinition(layer_junction_areas.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes_no_junction_markings = clearAttributes(layer_lanes_no_junction_markings, list_lane_attributes)
    layer_lanes_junction_markings = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_lanes, 'EXPRESSION' : '"lane_markings:junction" = \'yes\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_lanes_no_junction_markings, layer_lanes_junction_markings], 'OUTPUT': 'memory:'})['OUTPUT']

    processing.run('qgis:selectbyexpression', {'INPUT' : layer_junction_areas, 'EXPRESSION' : '"crossing" = \'traffic_signals\' or "crossing" = \'marked\' or "crossing" = \'zebra\''})
    layer_lanes_no_crossing_markings = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_lanes, 'EXPRESSION' : '"lane_markings:crossing" IS NOT \'yes\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes_no_crossing_markings = processing.run('native:difference', {'INPUT' : layer_lanes_no_crossing_markings, 'OVERLAY' : QgsProcessingFeatureSourceDefinition(layer_junction_areas.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes_no_crossing_markings = clearAttributes(layer_lanes_no_crossing_markings, list_lane_attributes)
    layer_lanes_crossing_markings = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_lanes, 'EXPRESSION' : '"lane_markings:crossing" = \'yes\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_lanes_no_crossing_markings, layer_lanes_crossing_markings, layer_lanes_bicycle_crossing], 'OUTPUT': 'memory:'})['OUTPUT']

    #Straßenmarkierungen an markierten Querungsstellen unterbrechen
    if not layer_raw_path_ways:
        layer_raw_path_ways = QgsVectorLayer(data_dir + 'path.geojson|geometrytype=LineString', 'path (raw)', 'ogr')
    layer_crossings = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_path_ways, 'EXPRESSION' : '"footway" = \'crossing\' and ("crossing" = \'traffic_signals\' or "crossing" = \'marked\' or "crossing" = \'zebra\')', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossings = processing.run('native:reprojectlayer', { 'INPUT' : layer_crossings, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossings_buffer = processing.run('native:buffer', { 'INPUT' : layer_crossings, 'DISTANCE' : QgsProperty.fromExpression('if("width", "width" / 2, 3)'), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes = processing.run('native:difference', {'INPUT' : layer_lanes, 'OVERLAY' : layer_crossings_buffer, 'OUTPUT': 'memory:'})['OUTPUT']

    #Bei separat gemappten Pufferflächen an Radwegen separation-Werte für Rendering anpassen
    #TODO: zur Zeit nur einfacher Test durch Überschneidung für bestimmte Situationen (kurze abgepollerte Verschwenkungen) - nicht allgemein anwendbar
    layer_prohibited = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_area_highway_polygons, 'EXPRESSION' : '"area:highway" = \'prohibited\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes.startEditing()
    processing.run('native:selectbylocation', {'INPUT' : layer_lanes, 'INTERSECT' : layer_prohibited, 'METHOD' : 0, 'PREDICATE' : [0]})
    for lane in layer_lanes.selectedFeatures():
        separation = lane.attribute('separation:left')
        if separation:
            separation = separation + ' (separate_buffer)'
        else:
            separation = 'separate_buffer'
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('separation:left'), separation)
    layer_lanes.commitChanges()

    #nach gemeinsamen Attributen auflösen (außer id), bereinigen und speichern
    #TODO: Neues Attribut für innerste Spur einer Fahrtrichtung anlegen, um auch "lanes", "lanes:forward", evtl. instance ignorieren zu können
    list_lane_attributes.remove('id_instance')
    list_lane_attributes.remove('id')
    layer_lanes = processing.run('native:dissolve', { 'FIELD' : list_lane_attributes, 'INPUT' : layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']
    list_lane_attributes.append('id_instance')
    list_lane_attributes.append('id')
    layer_lanes = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes = clearAttributes(layer_lanes, list_lane_attributes)
    qgis.core.QgsVectorFileWriter.writeAsVectorFormat(layer_lanes, proc_dir + 'marked_lanes.geojson', 'utf-8', QgsCoordinateReferenceSystem(crs_from), 'GeoJson')

    #--------------------------------------
    #Abschließend Haltelinien generieren
    #--------------------------------------
    print(time.strftime('%H:%M:%S', time.localtime()), '   Generiere Haltelinien...')
    print(time.strftime('%H:%M:%S', time.localtime()), '      Bereite Daten vor...')
    layer_raw_highway_ways_reproj = processing.run('native:reprojectlayer', { 'INPUT' : layer_raw_highway_ways, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_stop_nodes = processing.run('native:joinattributesbylocation', {'INPUT': layer_stop_nodes, 'JOIN' : layer_raw_highway_ways_reproj, 'JOIN_FIELDS' : lanes_attributes, 'METHOD' : 1, 'PREDICATE' : [0], 'PREFIX' : 'highway:', 'OUTPUT': 'memory:'})['OUTPUT']

    #Haltelinienpunkte und Knotenpunktbereiche in metrische KBS reprojizieren
    QgsProject.instance().addMapLayer(layer_stop_nodes, False)
    layer_junction_areas_outlines = processing.run('native:polygonstolines', { 'INPUT' : layer_junction_areas, 'OUTPUT': 'memory:'})['OUTPUT']

    #Bordsteinlinien erzeugen
    if not layer_raw_kerb_ways:
        #Bordsteinlinienlayer erzeugen: Da geschlossene Bordsteinlinien als Polygone interpretiert werden, falls sie mit anderen Features gemeinsam gemappt sind, diese zunächst zu Linien umwandeln
        if not layer_raw_barrier_ways:
            layer_raw_barrier_ways = QgsVectorLayer(data_dir + 'barriers.geojson|geometrytype=LineString', 'barrier (raw)', 'ogr')
        layer_kerb = processing.run('qgis:extractbyattribute', { 'INPUT' : layer_raw_barrier_ways, 'FIELD' : 'barrier', 'VALUE' : 'kerb', 'OUTPUT': 'memory:'})['OUTPUT']
        if not layer_raw_barrier_polygons:
            layer_raw_barrier_polygons = QgsVectorLayer(data_dir + 'barriers.geojson|geometrytype=Polygon', 'barrier (raw)', 'ogr')
        layer_kerb_outlines = processing.run('native:polygonstolines', { 'INPUT' : layer_raw_barrier_polygons, 'OUTPUT': 'memory:'})['OUTPUT']
        layer_kerb_outlines = processing.run('qgis:extractbyattribute', { 'INPUT' : layer_kerb_outlines, 'FIELD' : 'barrier', 'VALUE' : 'kerb', 'OUTPUT': 'memory:'})['OUTPUT']
        layer_kerb = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_kerb_outlines, layer_kerb], 'OUTPUT': 'memory:'})['OUTPUT']
        layer_kerb = processing.run('native:reprojectlayer', { 'INPUT' : layer_kerb, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    else:
        layer_kerb = layer_raw_kerb_ways

    #landuse-Layer einladen als Bordstein-Alternative
    if not layer_raw_landuse_polygons:
        layer_raw_landuse_polygons = QgsVectorLayer(data_dir + 'landuse.geojson|geometrytype=Polygon', 'landuse polygons (raw)', 'ogr')
    layer_landuse_polygons = processing.run('native:reprojectlayer', { 'INPUT' : layer_raw_landuse_polygons, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_landuse_polygons = processing.run('native:fixgeometries', { 'INPUT' : layer_landuse_polygons, 'OUTPUT': 'memory:'})['OUTPUT']

    #Knotenpunktlinie an Bordsteinkanten trennen (und landuse-Kanten, die als "Ersatz" für fehlende Bordsteinkanten angenommen werden können)
    layer_junction_areas_outlines = processing.run('native:difference', {'INPUT' : layer_junction_areas_outlines, 'OVERLAY' : layer_kerb, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_junction_areas_outlines = processing.run('native:difference', {'INPUT' : layer_junction_areas_outlines, 'OVERLAY' : layer_landuse_polygons, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_junction_areas_outlines = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_junction_areas_outlines, 'OUTPUT': 'memory:'})['OUTPUT']

    #Neuen Layer für Haltelinien erzeugen
    layer_stop_lines = QgsVectorLayer("LineString?crs=" + crs_to + "&field=road_marking:string&field=road_marking:left:string&field=road_marking:right:string&field=stop_line:string&field=temporary", "Haltelinien", "memory")
    provider = layer_stop_lines.dataProvider()
    layer_stop_lines.updateFields() 

    #Haltelinien erzeugen
    print(time.strftime('%H:%M:%S', time.localtime()), '      Erzeuge Haltelinien...')
    for stop_node in layer_stop_nodes.getFeatures():

        #TODO: Keine Haltelinie erzeugen, wenn ein passendes "road_marking"-Feature den Haltelinienpunkt berührt

        #keine Haltelinie erzeugen, wenn laut Tagging keine vorhanden ist
        if layer_stop_nodes.fields().indexOf('stop_line') != -1:
            if stop_node.attribute('stop_line') == 'no':
                continue

        stop_node_type = stop_node.attribute('highway')
        highway_id = stop_node.attribute('highway:id')
        #Fahrspurattribute für (ein) Staßensegment auslesen, auf dem der Punkt liegt

        #Falls das Haltelinienobjekt von keinem Straßensegment gequert wird, ignorieren
        if not highway_id in lanes_dict['placement']:
            continue

        placement = lanes_dict['placement'][highway_id]
        i = -(len(placement) - placement.find(':') - 1)
        placement_lane = int(placement[i:])
        placement_pos = placement[0:i]
        lanes_width = lanes_dict['width_lanes'][highway_id]
        lanes_reverse = lanes_dict['reverse_lanes'][highway_id]
        direction = NULL
        if layer_stop_nodes.fields().indexOf('direction') != -1:
            direction = stop_node.attribute('direction')
        if stop_node_type == 'traffic_signals' and layer_stop_nodes.fields().indexOf('traffic_signals:direction') != -1:
            direction = stop_node.attribute('traffic_signals:direction')
        temporary = NULL
        if layer_stop_nodes.fields().indexOf('temporary') != -1:
            temporary = stop_node.attribute('temporary')

        ow = 0
        if stop_node.fields().indexOf('highway:oneway') != -1:
            if stop_node.attribute('highway:oneway') == 'yes':
                ow = 1
        if stop_node.fields().indexOf('highway:oneway:bicycle') != -1:
            if stop_node.attribute('highway:oneway:bicycle') == 'no':
                ow = 0

        #Für jede Haltelinie berechnen, wo sie von der Fahrlinie aus gesehen beginnt und endet
        #len_empty: Leerraum nach rechts zwischen Fahrbahn und Beginn der Haltelinie (Haltelinienpunkt liegt im Gegenverkehr)
        #len_left: Länge der Haltelinie links des Haltelinienpunkt (in Straßenlinienrichtung aus gesehen)
        #len_right: Länge der Haltelinie rechts des Haltelinienpunkt
        #Annahme zunächst ein rechter Winkel zur Fahrlinie – Winkelanpassung später
        len_left = len_right = len_empty = 0
        right = empty = 0
        #Wenn Straßenlinie im Gegenverkehr liegt, beginnt die Linie erst weiter rechts nach einem Leerraum (in Richtung der Haltelinie gesehen). Links des Fahrbahnschnittpunkts gibt es dann keinen Haltelinienanteil.
        if (direction == 'backward' and lanes_reverse[placement_lane - 1] == 0 and placement_pos != 'left_of:') or (direction == 'forward' and lanes_reverse[placement_lane - 1] == 1 and placement_pos != 'right_of:'):
            #TODO: placement_pos nur in der 1. entgegengesetzten Spur relevant, sonst nicht
            empty = 1
            if direction == 'forward':
                right = 1

        for i in range(len(lanes_width)):
            if direction == 'backward':
                if lanes_reverse[i] == 0 and i + 1 > placement_lane and not right:
                    len_empty += float(lanes_width[i])
                if lanes_reverse[i] == 0 and i + 1 == placement_lane and not right:
                    if placement_pos == 'left_of:':
                        len_empty += float(lanes_width[i])
                    elif placement_pos == 'middle_of:':
                        len_empty += float(lanes_width[i]) / 2                    
                if i + 1 >= placement_lane or (i + 2 >= placement_lane and placement_pos == 'left_of:'):
                    right = 1
                if lanes_reverse[i] == 1:
                    if i + 1 == placement_lane or (i + 2 == placement_lane and placement_pos == 'left_of:'):
                        if placement_pos == 'left_of:':
                            len_left += float(lanes_width[i])
                        elif placement_pos == 'right_of:':
                            len_right += float(lanes_width[i])
                        else:
                            len_left += float(lanes_width[i]) / 2
                            len_right += float(lanes_width[i]) / 2
                    else:
                        if right:
                            len_right += float(lanes_width[i])
                        else:
                            len_left += float(lanes_width[i])
            elif direction == 'forward':
                if lanes_reverse[i] == 1 and i + 1 < placement_lane and right:
                    len_empty += float(lanes_width[i])
                if lanes_reverse[i] == 1 and i + 1 == placement_lane and right:
                    if placement_pos == 'left_of:':
                        len_empty += float(lanes_width[i])
                    elif placement_pos == 'middle_of:':
                        len_empty += float(lanes_width[i]) / 2
                if i + 1 >= placement_lane:
                    right = 1
                if lanes_reverse[i] == 0:
                    if i + 1 == placement_lane:
                        if placement_pos == 'left_of:':
                            len_right += float(lanes_width[i])
                        elif placement_pos == 'right_of:':
                            len_left += float(lanes_width[i])
                        else:
                            len_left += float(lanes_width[i]) / 2
                            len_right += float(lanes_width[i]) / 2
                    else:
                        if right:
                            len_right += float(lanes_width[i])
                        else:
                            len_left += float(lanes_width[i])
            else:
                #Wenn keine Richtung der Haltelinie angegeben ist, annehmen, dass sie über die gesamte Straßenbreite reicht
                if i + 1 == placement_lane or (i + 2 == placement_lane and placement_pos == 'left_of:'):
                    right = 1
                    if placement_pos == 'left_of:':
                        len_right += float(lanes_width[i])
                    elif placement_pos == 'right_of:':
                        len_left += float(lanes_width[i])
                    else:
                        len_left += float(lanes_width[i]) / 2
                        len_right += float(lanes_width[i]) / 2
                else:
                    if right:
                        len_right += float(lanes_width[i])
                    else:
                        len_left += float(lanes_width[i])

        #Koordinate des Haltelinienpunktes ermitteln
        node_geom = stop_node.geometry()
        node_point = node_geom.asPoint()
        node_x = node_point.x()
        node_y = node_point.y()


        #<<<<<<<< TODO: Auch (Rad-)Wege mit berücksichtigen, um auch dort Haltelinien anzuzeigen


        #Winkel an der kreuzenden Straßenlinie ermitteln
        highway_line = processing.run('qgis:extractbyattribute', { 'INPUT' : layer_highway_lanes, 'FIELD' : 'id', 'VALUE' : highway_id, 'OUTPUT': 'memory:'})['OUTPUT']
        if not len(highway_line):
            continue #Falls keine Straße durch die Ampel führt
        for highway_line in highway_line.getFeatures():
            highway_line_geom = highway_line.geometry()
            continue
        node_vertex_highway = highway_line_geom.closestVertexWithContext(node_point)
        angle_highway = angle_highway_vanilla = math.degrees(highway_line_geom.angleAtVertex(node_vertex_highway[1]))
        #Winkel meint den rechten Winkel zur Straßenlinie
        angle_highway -= 90
        if angle_highway < 0:
            angle_highway += 360

        #tatsächlichen Haltelinienwinkel ermitteln
        angle = angle_before = angle_after = NULL
        #Falls ein Haltelinienwinkel explizit im Tagging angegeben ist, diesen nehmen
        if layer_stop_nodes.fields().indexOf('stop_line:angle') != -1:
            stop_line_angle = stop_node.attribute('stop_line:angle')
            if stop_line_angle:
                angle = float(stop_line_angle)
                #Falls die Winkelangabe den Winkel nach rechts (in Fahrtrichtung) meint, Winkel nach links drehen
                if abs(angle_highway - angle) > 90 and abs(angle_highway - angle) < 270:
                    angle -= 180
                    if angle < 0:
                        angle += 360

        #ansonsten Winkel aus der Linie des Knotenpunktbereichs ableiten:
        #Wenn der Haltelinienpunkt von einer Knotenpunktbereichsfläche geschnitten wird, davon ausgehen, dass die Richtung der kreuzenden Kante der Richtung der Haltelinie entspricht
        line_from_junction = 0
        if angle == NULL:
            #Haltelinienpunkt markieren, um mit markiertem Punkt verknüpften Knotenpunktbereich zu ermitteln
            layer_stop_nodes.removeSelection()
            layer_stop_nodes.select(stop_node.id())

            layer_junction_line = NULL
            layer_junction_line = processing.run('native:extractbylocation', { 'INPUT' : layer_junction_areas_outlines, 'INTERSECT' : QgsProcessingFeatureSourceDefinition(layer_stop_nodes.id(), selectedFeaturesOnly=True), 'PREDICATE' : [0], 'OUTPUT': 'memory:'})['OUTPUT']

            if len(layer_junction_line):
                line_from_junction = 1
                for junction_line in layer_junction_line.getFeatures():
                    junction_line_geom = junction_line.geometry()
                    continue
                #Vertex der Knotenpunktgeometrie an der (nächsten) Stelle des Haltelinienpunktes ermitteln
                node_vertex_junction = junction_line_geom.closestVertexWithContext(node_point)[1]
                node_vertex_junction_dist = junction_line_geom.distanceToVertex(node_vertex_junction)

                angle = junction_line_angle = math.degrees(junction_line_geom.angleAtVertex(node_vertex_junction))
                angle_before = math.degrees(junction_line_geom.interpolateAngle(node_vertex_junction_dist - 0.1))
                angle_after = math.degrees(junction_line_geom.interpolateAngle(node_vertex_junction_dist + 0.1))

                #Falls Haltelinienpunkt genau auf einem Winkel der Knotenpunktgeometrie liegt, Winkel aus dem Schenkel ermitteln, der am ehesten dem Winkel an der Straßenlinie entspricht
                if abs(angle_before - angle_after) > 15:
                    if abs(angle_highway - angle_before) < 15:
                        angle = junction_line_angle = angle_before
                    elif abs(angle_highway - angle_after) < 15:
                        angle = junction_line_angle = angle_after
                    else:
                        if angle_before > 180:
                            angle_before -= 180
                        else:
                            angle_before += 180
                        if angle_after > 180:
                            angle_after -= 180
                        else:
                            angle_after += 180
                        if abs(angle_highway - angle_before) < 15:
                            angle = angle_before
                            junction_line_angle = angle - 180
                        elif abs(angle_highway - angle_after) < 15:
                            angle = angle_after
                            junction_line_angle = angle - 180
                        if junction_line_angle < 0:
                            junction_line_angle += 360

                #Linienrichtung ggf. korrigieren – Winkel soll immer nach links von Straßenlinienrichtung aus weisen
                angle_diff = abs(angle_highway - angle)
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff
                if angle_diff > 90:
                    angle = angle - 180
                    if angle < 0:
                        angle = 360 - abs(angle)
                
        #Rückfall-/Default-Option: Rechter Winkel zur Straßenlinie
        if angle == NULL:
            angle = angle_highway

        #Winkelabweichung zwischen rechtem Winkel zur Straßenlinie (default) und tatsächlicher Haltelinienrichtung berechnen
        angle_diff = abs(angle_highway - angle)
        if angle_diff > 180:
            angle_diff = 360 - angle_diff
        if angle_diff > 90:
            angle_diff = 180 - angle_diff

        #Länge der Haltelinie entsprechend des Winkelunterschieds verlängern
        len_stop_line_vanilla = len_left + len_right
        len_left = len_left / math.sin(math.radians(90 - angle_diff))
        len_right = len_right / math.sin(math.radians(90 - angle_diff))

        #Wenn kein Knotenpunktbereich definiert, Linie pauschal um 3 Meter nach rechts verlängern
        #in Einbahnstraßen auch nach links
        if not line_from_junction:
            if direction == 'backward':
                len_left += 3
                if ow:
                    len_right += 3
            else:
                len_right += 3
                if ow:
                    len_left += 3

            #Linie zur schöneren Darstellung auf jeder Seite um 12,5cm verlängern (25cm = Linienbreite Fahrbahnmarkierungen / 2)
            if direction == 'forward':
                len_right += 0.125
                if not empty:
                    len_left += 0.125
            elif direction == 'backward':
                len_left += 0.125
                if not empty:
                    len_right += 0.125
            else:
                len_left += 0.125
                len_right += 0.125

        #Haltelinien Start- und Endpunkte ermitteln
        xv_start = math.sin(math.radians(angle)) * len_left
        yv_start = math.cos(math.radians(angle)) * len_left
        xv_end = math.sin(math.radians(angle)) * len_right
        yv_end = math.cos(math.radians(angle)) * len_right
        if len_empty:
            if direction == 'backward':
                xv_end -= math.sin(math.radians(angle)) * len_empty
                yv_end -= math.cos(math.radians(angle)) * len_empty
            else:
                xv_start += math.sin(math.radians(angle)) * len_empty
                yv_start += math.cos(math.radians(angle)) * len_empty

        start_x = node_x + xv_start
        start_y = node_y + yv_start
        end_x = node_x - xv_end
        end_y = node_y - yv_end

        #Linie zeichnen, wenn diese nicht aus Knotenpunktgeometrie ableitbar ist
        if not line_from_junction:
            line_start = QgsPointXY(start_x, start_y)
            line_end = QgsPointXY(end_x, end_y)

            #Haltelinienobjekt zeichnen
            line = QgsFeature()
            line.setGeometry(QgsGeometry.fromPolylineXY([line_start, line_end]))
            line.setAttributes(['stop_line', NULL, NULL, 'solid_line', temporary])
            provider.addFeature(line)
            layer_stop_lines.updateExtents()

#            print(highway_id, direction, round(angle, 2), round(len_empty, 2), round(len_left, 2), round(len_right, 2))
#            print(highway_id, len_empty, len_left, len_right, ' | ', start_x, start_y, end_x, end_y)

        #falls vorhanden, Haltelinien aus Knotenpunkt-Geometrien ableiten
        else:
            #Wenn keine Einbahnstraße: Bereiche rechts der tatsächlichen Haltelinie/Fahrspur ausschließen
            if not ow:
                #Schnittlinie erzeugen: 100 Meter vor und hinter dem linken Haltelinienpunkt in Fahrbahnrichtung
                layer_split_line = QgsVectorLayer("LineString?crs=" + crs_to, "split_line", "memory")
                split_line_provider = layer_split_line.dataProvider()
                xv_start = math.sin(math.radians(angle_highway_vanilla)) * 100
                yv_start = math.cos(math.radians(angle_highway_vanilla)) * 100
                xv_end = math.sin(math.radians(angle_highway_vanilla)) * 100
                yv_end = math.cos(math.radians(angle_highway_vanilla)) * 100
                if direction == 'backward':
                    start_x = end_x
                    start_y = end_y
                split_line_start_x = start_x + xv_start
                split_line_start_y = start_y + yv_start
                split_line_end_x = start_x - xv_end
                split_line_end_y = start_y - yv_end
                split_line_start = QgsPointXY(split_line_start_x, split_line_start_y)
                split_line_end = QgsPointXY(split_line_end_x, split_line_end_y)
                split_line = QgsFeature()
                split_line.setGeometry(QgsGeometry.fromPolylineXY([split_line_start, split_line_end]))
                split_line_provider.addFeature(split_line)
                layer_split_line.updateExtents()

                #Knotenpunktlinie mit Schnittlinie in zwei Hälften zerteilen
                layer_junction_line = processing.run('native:splitwithlines', { 'INPUT' : layer_junction_line, 'LINES' : layer_split_line, 'OUTPUT': 'memory:'})['OUTPUT']

                #Schnittlinie leicht nach links (in Fahrtrichtung gesehen) versetzen und nur die Knotenpunktlinienhälfte behalten, den sie dann schneidet
                if direction == 'backward':
                    layer_split_line = processing.run('native:offsetline', {'INPUT': layer_split_line, 'DISTANCE' : -0.1, 'OUTPUT': 'memory:'})['OUTPUT']
                else:
                    layer_split_line = processing.run('native:offsetline', {'INPUT': layer_split_line, 'DISTANCE' : 0.1, 'OUTPUT': 'memory:'})['OUTPUT']

                layer_junction_line = processing.run('native:extractbylocation', { 'INPUT' : layer_junction_line, 'INTERSECT' : layer_split_line, 'PREDICATE' : [0], 'OUTPUT': 'memory:'})['OUTPUT']

            #passenden Knotenpunktbereich in Einzelsegmente umwandeln, Bearbeitung starten
            layer_junction_lines = processing.run('native:explodelines', { 'INPUT' : layer_junction_line, 'OUTPUT': 'memory:'})['OUTPUT']
            layer_junction_lines.startEditing()

            #Um Umkreis von 15 Metern (oder – wenn mehr – der "Normlinienlänge" plus Puffer) nach passenden Segmenten suchen
            #(recht große Distanzen, da vorgezogene Haltelinien viele Meter vor der Kfz-Haltelinie sein können)
            #(wenn dadurch zu viele Haltelinien-Artefakte entstehen, kann Distanz reduziert werden auf max((len_stop_line_vanilla / 2) + 3, 5))
            max_distance = max((len_stop_line_vanilla / 2) + 10, 15)
            #Suchradius um den Mittelpunkt der Normlinie ziehen
            if start_x < end_x:
                x_middle = abs(start_x - end_x) / 2 + start_x
            else:
                x_middle = abs(start_x - end_x) / 2 + end_x
            if start_y < end_y:
                y_middle = abs(start_y - end_y) / 2 + start_y
            else:
                y_middle = abs(start_y - end_y) / 2 + end_y
            middle_point_geom = QgsGeometry.fromPointXY(QgsPointXY(x_middle, y_middle))

            for junction_line in layer_junction_lines.getFeatures():
                junction_line_geom = junction_line.geometry()
                angle_check = math.degrees(junction_line_geom.angleAtVertex(0))
                if abs(angle_check - junction_line_angle) > 15:
                    #Nur Segmente behalten, die etwa in die gleiche Richtung weisen
                    layer_junction_lines.deleteFeature(junction_line.id())
                if junction_line_geom.distance(middle_point_geom) > max_distance:
                    #Nur Segmente behalten, die sich in der Nähe befinden
                    layer_junction_lines.deleteFeature(junction_line.id())

            layer_junction_lines.commitChanges()
            #Liniensegmente zur schöneren Darstellung auf jeder Seite um 12,5cm verlängern (25cm = Linienbreite Fahrbahnmarkierungen / 2)
            layer_junction_lines = processing.run('native:extendlines', { 'INPUT' : layer_junction_lines, 'START_DISTANCE' : 0.125, 'END_DISTANCE' : 0.125, 'OUTPUT': 'memory:'})['OUTPUT']
            #Liniensegmente zusammenführen und mit Basis-Attributen versehen
            layer_junction_lines = processing.run('native:dissolve', { 'INPUT' : layer_junction_lines, 'OUTPUT': 'memory:'})['OUTPUT']
            layer_junction_lines = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_junction_lines, 'OUTPUT': 'memory:'})['OUTPUT']
            for junction_line in layer_junction_lines.getFeatures():
                junction_line.setAttributes(['stop_line', NULL, NULL, 'solid_line', temporary])
                provider.addFeature(junction_line)
                layer_stop_lines.updateExtents()

#            QgsProject.instance().addMapLayer(layer_junction_lines, True)
    QgsProject.instance().addMapLayer(layer_junction_areas_outlines, False)

    print(time.strftime('%H:%M:%S', time.localtime()), '      Bereinige Daten...')

    #Segmente ausschließen, die sich auf anderen Fahrbahnbereichen befinden - insbesondere auf naheliegenden Gegenfahrbahnen von dual_carriageways
    #über Schnittpunkte von Straßen und Knotenpunktflächen ermittelt, gepuffert entsprechend der Fahrbahnbreite
    layer_junction_enter_nodes = processing.run('native:lineintersections', {'INPUT': QgsProcessingFeatureSourceDefinition(layer_junction_areas_outlines.id(), flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometrySkipInvalid), 'INTERSECT': layer_highway_lanes, 'INPUT_FIELDS' : ['junction'], 'INTERSECT_FIELDS' : ['id','name','highway', 'lanes'], 'INTERSECT_FIELDS_PREFIX': '', 'OUTPUT': 'memory:'})['OUTPUT']
    #Puffer von - grob geschätzt - 3,5 Metern pro Spur erzeugen und Haltelinienfragmente innerhalb des Puffers entfernen
    layer_junction_enter_nodes_buffer = processing.run('native:buffer', { 'INPUT' : layer_junction_enter_nodes, 'DISTANCE' : QgsProperty.fromExpression('(if("lanes", "lanes", 1.5) * 3.5) / 2'), 'OUTPUT': 'memory:'})['OUTPUT']
    #Puffer ausschließen, innerhalb derer ein Ampel-/Stopnode ist
    layer_junction_enter_nodes_buffer = processing.run('native:extractbylocation', { 'INPUT' : layer_junction_enter_nodes_buffer, 'INTERSECT' : layer_stop_nodes, 'PREDICATE' : [2], 'OUTPUT': 'memory:'})['OUTPUT']

    layer_stop_lines = processing.run('native:difference', {'INPUT' : layer_stop_lines, 'OVERLAY' : layer_junction_enter_nodes_buffer, 'OUTPUT': 'memory:'})['OUTPUT']

    layer_stop_lines = processing.run('native:fixgeometries', { 'INPUT' : layer_stop_lines, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_stop_lines = processing.run('native:deleteduplicategeometries', {'INPUT': layer_stop_lines, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_stop_lines = processing.run('native:difference', {'INPUT' : layer_stop_lines, 'OVERLAY' : layer_kerb, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_stop_lines = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_stop_lines, 'OUTPUT': 'memory:'})['OUTPUT']

    #Mit separat gemappten Straßenmarkierungen zusammenführen
    layer_road_markings_raw = QgsVectorLayer(data_dir + 'area_highway.geojson|geometrytype=LineString', 'area_highway (raw)', 'ogr')
    layer_road_markings_raw = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_road_markings_raw, 'EXPRESSION' : '"road_marking" IS NOT NULL or "road_marking:left" IS NOT NULL or "road_marking:right" IS NOT NULL', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_road_markings = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_stop_lines, layer_road_markings_raw], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_road_markings = clearAttributes(layer_road_markings, ['id', 'road_marking', 'road_marking:left', 'road_marking:right', 'stop_line', 'width', 'temporary'])

    #Linien auf Fahrbahnbereiche beschneiden
    if not layer_raw_kerb_street_areas_polygons:
        #layer_raw_kerb_street_areas_polygons = QgsVectorLayer(data_dir + 'kerb/kerb_street_areas.geojson|geometrytype=Polygon', 'Fahrbahnbereiche (raw)', 'ogr')
        layer_raw_kerb_street_areas_polygons = createStreetAreaPolygons()
    QgsProject.instance().addMapLayer(layer_road_markings, False)
    layer_road_markings = processing.run('native:clip', {'INPUT' : QgsProcessingFeatureSourceDefinition(layer_road_markings.id(), flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometrySkipInvalid), 'OVERLAY' : layer_raw_kerb_street_areas_polygons, 'OUTPUT': 'memory:'})['OUTPUT']
    #sehr kurze Segmente (Relikte bis 20 cm) entfernen
    layer_road_markings = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_road_markings, 'EXPRESSION' : '$length > 0.2', 'OUTPUT' : proc_dir + 'road_markings.geojson' })



#-----------------------------------------------------------------
# Straßenlinien als Backup in fahrbahnfreien Bereichen erzeugen
#-----------------------------------------------------------------
if proc_highway_backup:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Erzeuge Backup-Straßennetz...')
    if not layer_raw_highway_ways:
        layer_raw_highway_ways = QgsVectorLayer(data_dir + 'highway.geojson|geometrytype=LineString', 'highway (raw)', 'ogr')
    layer_highway = layer_raw_highway_ways
    layer_highway = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_highway, 'EXPRESSION' : '"highway" = \'primary_link\' OR "highway" = \'secondary_link\' OR "highway" = \'tertiary_link\' OR "highway" = \'residential\' OR "highway" = \'unclassified\' OR "highway" = \'living_street\' OR "highway" = \'pedestrian\' OR "highway" = \'road\'', 'OUTPUT': 'memory:'})['OUTPUT']

    layer_highway = clearAttributes(layer_highway, ['id', 'highway', 'name', 'oneway', 'width', 'width:carriageway', 'dual_carriageway'])

    if not layer_raw_kerb_street_areas_polygons:
        #layer_raw_kerb_street_areas_polygons = QgsVectorLayer(data_dir + 'kerb/kerb_street_areas.geojson|geometrytype=Polygon', 'Fahrbahnbereiche (raw)', 'ogr')
        layer_raw_kerb_street_areas_polygons = createStreetAreaPolygons()
    layer_kerbs = layer_raw_kerb_street_areas_polygons
    QgsProject.instance().addMapLayer(layer_kerbs, False)

    #Umweg über clip geht deutlich schneller als direkte difference aus kerb-layer
    layer_highway_clipped = processing.run('native:clip', {'INPUT': layer_highway, 'OVERLAY': layer_kerbs, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_highway = processing.run('native:difference', {'INPUT': layer_highway, 'OVERLAY': layer_highway_clipped, 'OUTPUT' : proc_dir + 'highway_backup.geojson' })



#----------------------------------------------------------------------------------
# service-Wege mit gleichen Eigenschaften zusammenführen, um Lücken zu vermeiden
#----------------------------------------------------------------------------------
if proc_service:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Vereinige service-Straßen...')
    if not layer_raw_highway_ways:
        layer_raw_highway_ways = QgsVectorLayer(data_dir + 'highway.geojson|geometrytype=LineString', 'highway (raw)', 'ogr')
    layer_highway = layer_raw_highway_ways
    layer_highway = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_highway, 'EXPRESSION' : '"highway" = \'service\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_highway_building_passages = layer_highway
    layer_highway = processing.run('native:dissolve', { 'FIELD' : ['highway', 'service', 'width', 'width:carriageway'], 'INPUT' : layer_highway, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_highway = clearAttributes(layer_highway, ['highway', 'service', 'width', 'width:carriageway'])
    processing.run('native:multiparttosingleparts', {'INPUT' : layer_highway, 'OUTPUT' : proc_dir + 'service.geojson' })
    #create a second layer for building passages
    layer_highway_building_passages = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_highway_building_passages, 'EXPRESSION' : '"tunnel" IS \'building_passage\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_highway_building_passages = processing.run('native:retainfields', { 'INPUT' : layer_highway_building_passages, 'FIELDS' : ['highway', 'service', 'width', 'width:carriageway', 'tunnel'], 'OUTPUT' : proc_dir + 'service_passages.geojson' })



#-----------------------------------------------
# Für Einbahnstraßen separate Linien erzeugen
#-----------------------------------------------
if proc_oneways:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Extrahiere Einbahnstraßen...')
    print(time.strftime('%H:%M:%S', time.localtime()), '   Lade Wegedaten...')
    if not layer_raw_highway_ways:
        layer_raw_highway_ways = QgsVectorLayer(data_dir + 'highway.geojson|geometrytype=LineString', 'highway (raw)', 'ogr')
    if not layer_raw_path_ways:
        layer_raw_path_ways = QgsVectorLayer(data_dir + 'path.geojson|geometrytype=LineString', 'path (raw)', 'ogr')

    #Einbahnstraßen herausfiltern
    print(time.strftime('%H:%M:%S', time.localtime()), '   Filtere Einbahnstraßen...')
    layer_raw_highway_ways = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_highway_ways, 'EXPRESSION' : '\"oneway\" = \'yes\' OR \"oneway\" = \'-1\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_raw_path_ways = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_path_ways, 'EXPRESSION' : '\"oneway\" = \'yes\' OR \"oneway\" = \'-1\'', 'OUTPUT': 'memory:'})['OUTPUT']
    print(time.strftime('%H:%M:%S', time.localtime()), '   Führe Wegedaten zusammen...')
    layer_ways = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_raw_highway_ways, layer_raw_path_ways], 'OUTPUT': 'memory:'})['OUTPUT']

    #In metrisches Koordinatensystem umwandeln, um Puffer in Metern erzeugen zu können
    print(time.strftime('%H:%M:%S', time.localtime()), '   Transformiere Koordinatensystem...')
    QgsVectorFileWriter.writeAsVectorFormatV2(layer_ways, proc_dir + 'oneways.geojson', transform_context, save_options)
    layer_ways = QgsVectorLayer(proc_dir + 'oneways.geojson|geometrytype=LineString', 'Einbahnstraßen', 'ogr')

    #Zusammenhängende Segmente (Straßenzüge) verbinden
    print(time.strftime('%H:%M:%S', time.localtime()), '   Füge Wege zusammen...')
    #Für Kreuzungsberechnung alle Wege nach Name und Klassifikation zusammenführen
    layer_ways_for_intersections = processing.run('native:dissolve', { 'FIELD' : ['highway', 'name'], 'INPUT' : layer_ways, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_ways_for_intersections = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_ways_for_intersections, 'OUTPUT': 'memory:'})['OUTPUT']
    #Für Einbahnstraßen-Prozessierung aber weitere Attribute zur besseren Darstellung berücksichtigen
    layer_ways = processing.run('native:dissolve', { 'FIELD' : ['highway', 'name', 'oneway', 'oneway:bicycle', 'dual_carriageway', 'turn:lanes'], 'INPUT' : layer_ways, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_ways = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_ways, 'OUTPUT': 'memory:'})['OUTPUT']

    #Knotenpunkte aller Wege ermitteln, um z.B. Zufahrten für bessere Darstellung zu kürzen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Erzeuge Kreuzungspunkte (alle Wege)...')
    layer_ways_all_intersections = processing.run('native:lineintersections', {'INPUT': layer_ways_for_intersections, 'INTERSECT': layer_ways_for_intersections, 'OUTPUT': 'memory:'})['OUTPUT']
    #Start- und End-Vertices hinzufügen, da diese meist ebenfalls Kreuzungspunkte sind
    layer_ways_all_vertices = processing.run('native:extractspecificvertices', { 'INPUT' : layer_ways_for_intersections, 'VERTICES' : '0,-1', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_ways_all_intersections = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_ways_all_intersections, layer_ways_all_vertices], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_ways_all_intersections = processing.run('native:deleteduplicategeometries', {'INPUT': layer_ways_all_intersections, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_ways_all_intersections = processing.run('native:buffer', { 'INPUT' : layer_ways_all_intersections, 'DISTANCE' : 11, 'OUTPUT': 'memory:'})['OUTPUT']

    #Knotenpunkte der Verkehrsstraßen ermitteln, um nur diese für bessere Darstellung zu kürzen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Erzeuge Kreuzungspunkte (Verkehrsstraßen)...')
    QgsProject.instance().addMapLayer(layer_ways_for_intersections, False)
    QgsProject.instance().addMapLayer(layer_ways, False)
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_ways_for_intersections, 'EXPRESSION' : '"highway" IS \'primary\' or "highway" IS \'secondary\' or "highway" IS \'tertiary\' or "highway" IS \'residential\' or "highway" IS \'unclassified\' or "highway" IS \'living_street\' or "highway" IS \'pedestrian\' or "highway" IS \'road\''})
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_ways, 'EXPRESSION' : '"highway" IS \'primary\' or "highway" IS \'secondary\' or "highway" IS \'tertiary\' or "highway" IS \'residential\' or "highway" IS \'unclassified\' or "highway" IS \'living_street\' or "highway" IS \'pedestrian\' or "highway" IS \'road\''})
    layer_roads_intersections = processing.run('native:lineintersections', {'INPUT': QgsProcessingFeatureSourceDefinition(layer_ways_for_intersections.id(), selectedFeaturesOnly=True), 'INTERSECT': QgsProcessingFeatureSourceDefinition(layer_ways_for_intersections.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']
    #Start- und End-Vertices hinzufügen, da diese meist ebenfalls Kreuzungspunkte sind
    layer_roads_vertices = processing.run('native:extractspecificvertices', { 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_ways_for_intersections.id(), selectedFeaturesOnly=True), 'VERTICES' : '0,-1', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_roads_intersections = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_roads_intersections, layer_roads_vertices], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_roads_intersections = processing.run('native:deleteduplicategeometries', {'INPUT': layer_roads_intersections, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_roads_intersections = processing.run('native:buffer', { 'INPUT' : layer_roads_intersections, 'DISTANCE' : 11, 'OUTPUT': 'memory:'})['OUTPUT']
    print(time.strftime('%H:%M:%S', time.localtime()), '   Kürze Verkehrsstraßen...')
    layer_roads_shortened = processing.run('native:difference', {'INPUT' : QgsProcessingFeatureSourceDefinition(layer_ways.id(), selectedFeaturesOnly=True), 'OVERLAY' : layer_roads_intersections, 'OUTPUT': 'memory:'})['OUTPUT']

    #Auswahl umkehren, um statt Verkehrsstraßen alle Zufahrtswege etc. zu erhalten und diese zu kürzen
    layer_ways.invertSelection()
    print(time.strftime('%H:%M:%S', time.localtime()), '   Kürze sonstige Wege...')
    layer_ways_all_shortened = processing.run('native:difference', {'INPUT' : QgsProcessingFeatureSourceDefinition(layer_ways.id(), selectedFeaturesOnly=True), 'OVERLAY' : layer_ways_all_intersections, 'OUTPUT': 'memory:'})['OUTPUT']

    print(time.strftime('%H:%M:%S', time.localtime()), '   Führe Daten zusammen...')
    oneways = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_roads_shortened, layer_ways_all_shortened], 'OUTPUT': 'memory:'})['OUTPUT']
    print(time.strftime('%H:%M:%S', time.localtime()), '   Bereinige Daten...')
    oneways = clearAttributes(oneways, ['id', 'highway', 'name', 'oneway', 'oneway:bicycle', 'width', 'width:carriageway', 'dual_carriageway', 'turn:lanes'])

    #Zusätzlich außerdem Straßensegmente in Knotenpunktbereichen kürzen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Lade Knotenpunktbereiche...')
    if not layer_raw_area_highway_polygons:
        layer_raw_area_highway_polygons = QgsVectorLayer(data_dir + 'area_highway.geojson|geometrytype=Polygon', 'area_highway (raw)', 'ogr')
    layer_junction_areas = layer_raw_area_highway_polygons
    layer_junction_areas = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_junction_areas, 'EXPRESSION' : '"junction" = \'yes\' OR "crossing" = \'traffic_signals\' OR "crossing" = \'marked\' OR "crossing" = \'zebra\'', 'OUTPUT': 'memory:'})['OUTPUT']
    print(time.strftime('%H:%M:%S', time.localtime()), '   Schließe Knotenpunktbereiche aus...')
    oneways = processing.run('native:difference', {'INPUT' : oneways, 'OVERLAY' : layer_junction_areas, 'OUTPUT' : proc_dir + 'oneways.geojson' })



#--------------------------------------------------------------------
# Straßeneigenschaften auf Verkehrsberuhigungsmaßnahmen übertragen
#--------------------------------------------------------------------
if proc_traffic_calming:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Verkehrsberuhigung verarbeiten...')
    print(time.strftime('%H:%M:%S', time.localtime()), '   Straßen und Wege einladen...')
    if not layer_raw_highway_ways:
        layer_raw_highway_ways = QgsVectorLayer(data_dir + 'highway.geojson|geometrytype=LineString', 'highway (raw)', 'ogr')
    if not layer_raw_path_ways:
        layer_raw_path_ways = QgsVectorLayer(data_dir + 'path.geojson|geometrytype=LineString', 'path (raw)', 'ogr')
    if not layer_raw_highway_points:
        layer_raw_highway_points = QgsVectorLayer(data_dir + 'highway.geojson|geometrytype=Point', 'highway (raw)', 'ogr')
    layer_traffic_calming = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_highway_points, 'EXPRESSION' : '"traffic_calming" IS NOT NULL', 'OUTPUT': 'memory:'})['OUTPUT']

    print(time.strftime('%H:%M:%S', time.localtime()), '   Eigenschaften übertragen...')
    #Straßen- und Wegesegmente auswählen, auf denen Verkehrsberuhigungen liegen
    layer_street_segments = processing.run('native:extractbylocation', { 'INPUT' : layer_raw_highway_ways, 'INTERSECT' : layer_traffic_calming, 'PREDICATE' : [0], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_way_segments = processing.run('native:extractbylocation', { 'INPUT' : layer_raw_path_ways, 'INTERSECT' : layer_traffic_calming, 'PREDICATE' : [0], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_street_segments = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_street_segments, layer_way_segments], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_street_segments = processing.run('native:reprojectlayer', { 'INPUT' : layer_street_segments, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    #Stützpunkte extrahieren (für Winkelangabe) und Winkel sowie andere potentiell relevante Straßeneigenschaften übertragen
    layer_street_nodes = processing.run('native:extractvertices', {'INPUT': layer_street_segments, 'OUTPUT': 'memory:'})['OUTPUT']
    #layer_street_nodes = processing.run('native:reprojectlayer', { 'INPUT' : layer_street_nodes, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    street_attributes = ['highway', 'oneway', 'lanes', 'lanes:forward', 'lanes:backward', 'placement', 'placement:forward', 'placement:backward', 'angle']
    traffic_calming_attributes = ['traffic_calming', 'direction', 'surface', 'width', 'length', 'description']
    prefix = 'highway:'
    layer_traffic_calming = processing.run('native:reprojectlayer', { 'INPUT' : layer_traffic_calming, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_traffic_calming = processing.run('native:joinattributesbylocation', {'INPUT': layer_traffic_calming, 'JOIN' : layer_street_nodes, 'JOIN_FIELDS' : street_attributes, 'METHOD' : 1, 'PREDICATE' : [2], 'PREFIX' : prefix, 'OUTPUT': 'memory:'})['OUTPUT']
    #Verkehrsberuhigung bereinigen und abspeichern
    for i in range(len(street_attributes)):
        street_attributes[i] = prefix + street_attributes[i]
    layer_traffic_calming = clearAttributes(layer_traffic_calming, street_attributes + traffic_calming_attributes)
    qgis.core.QgsVectorFileWriter.writeAsVectorFormat(layer_traffic_calming, proc_dir + 'traffic_calming.geojson', 'utf-8', QgsCoordinateReferenceSystem(crs_from), 'GeoJson')



#--------------------------
# Radwege nachbearbeiten
#--------------------------
if proc_cycleways:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Radwege nachbearbeiten...')
    if not layer_raw_path_ways:
        layer_raw_path_ways = QgsVectorLayer(data_dir + 'path.geojson|geometrytype=LineString', 'path (raw)', 'ogr')
    #Radwege auf und neben der Fahrbahn und markierte Querungsstellen herausfiltern und reprojizieren
    if not layer_raw_kerb_street_areas_polygons:
        #layer_raw_kerb_street_areas_polygons = QgsVectorLayer(data_dir + 'kerb/kerb_street_areas.geojson|geometrytype=Polygon', 'Fahrbahnbereiche (raw)', 'ogr')
        layer_raw_kerb_street_areas_polygons = createStreetAreaPolygons()
    print(time.strftime('%H:%M:%S', time.localtime()), '   Radwege vorbereiten...')
    layer_cycleways = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_path_ways, 'EXPRESSION' : '"highway" = \'cycleway\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_cycleways_on_carriageway = processing.run('native:clip', {'INPUT' : layer_cycleways, 'OVERLAY' : layer_raw_kerb_street_areas_polygons, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_cycleways_off_carriageway = processing.run('native:difference', {'INPUT' : layer_cycleways, 'OVERLAY' : layer_raw_kerb_street_areas_polygons, 'OUTPUT': 'memory:'})['OUTPUT']

    #für Differenzierung in der späteren Darstellung ein Attribut für Lage im Fahrbahnbereich ergänzen
    layer_cycleways_on_carriageway = processing.run('qgis:fieldcalculator', { 'INPUT': layer_cycleways_on_carriageway, 'FIELD_NAME': 'is_on_carriageway', 'FIELD_TYPE': 2, 'FIELD_LENGTH': 3, 'NEW_FIELD': True, 'FORMULA': "'yes'", 'OUTPUT': 'memory:'})['OUTPUT']

    #Radwege an markierten Querungsstellen unterbrechen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Radwege an Querungsstellen unterbrechen...')
    layer_crossings = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_path_ways, 'EXPRESSION' : '"footway" = \'crossing\' and ("crossing" = \'traffic_signals\' or "crossing" = \'marked\' or "crossing" = \'zebra\')', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossings = processing.run('native:reprojectlayer', { 'INPUT' : layer_crossings, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossings_buffer = processing.run('native:buffer', { 'INPUT' : layer_crossings, 'DISTANCE' : QgsProperty.fromExpression('if("width", "width" / 2, 3)'), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_cycleways_on_carriageway = processing.run('native:difference', {'INPUT' : layer_cycleways_on_carriageway, 'OVERLAY' : layer_crossings_buffer, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_cycleways = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_cycleways_on_carriageway, layer_cycleways_off_carriageway], 'OUTPUT': 'memory:'})['OUTPUT']

    #Radwege an Haltelinien aufspalten
    layer_stop_lines = QgsVectorLayer(proc_dir + 'road_markings.geojson|geometrytype=LineString', 'road markings', 'ogr')
    layer_stop_lines = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_stop_lines, 'EXPRESSION' : '"road_marking" = \'stop_line\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_cycleways = processing.run('native:splitwithlines', { 'INPUT' : layer_cycleways, 'LINES' : layer_stop_lines, 'OUTPUT': 'memory:'})['OUTPUT']

    #kurze Wegstücke entfernen
    layer_cycleways = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_cycleways, 'EXPRESSION' : '$length > 2.5', 'OUTPUT': 'memory:'})['OUTPUT']

    #Flächen für Radweg-Querungen im Fahrbahnbereich erzeugen, um überschneidende Linien zu überdecken
    #TODO: Begrenzungslinien besser durch Versatz erzeugen und überschneidende Linien ausschließen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Deckende Radwegflächen in Kreuzungsbereichen erzeugen...')
    layer_cycleways_crossings = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_cycleways, 'EXPRESSION' : '("cycleway" = \'crossing\' or "cycleway:type" = \'crossing\') and "surface:colour" IS NULL', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_cycleways_crossings = processing.run('native:reprojectlayer', { 'INPUT' : layer_cycleways_crossings, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_cycleways_crossings = processing.run('native:buffer', { 'INPUT' : layer_cycleways_crossings, 'DISTANCE' : QgsProperty.fromExpression('if("width", "width" / 2, 0.5)'), 'END_CAP_STYLE' : 1, 'OUTPUT': 'memory:'})['OUTPUT']
    #Flächen auf Fahrbahnbereiche beschneiden
    layer_cycleways_crossings = processing.run('native:clip', {'INPUT' : layer_cycleways_crossings, 'OVERLAY' : layer_raw_kerb_street_areas_polygons, 'OUTPUT' : proc_dir + 'cycleways_crossing.geojson' })

    #Radwege bereinigen und abspeichern
    layer_cycleways = clearAttributes(layer_cycleways, ['id', 'highway', 'name', 'oneway', 'cycleway', 'cycleway:type', 'crossing', 'crossing:markings', 'is_sidepath', 'width', 'surface', 'smoothness', 'surface:colour', 'separation', 'separation:left', 'separation:right', 'separation:both', 'buffer', 'buffer:left', 'buffer:right', 'buffer:both', 'lanes', 'turn:lanes', 'placement', 'is_on_carriageway'])
    qgis.core.QgsVectorFileWriter.writeAsVectorFormat(layer_cycleways, proc_dir + 'cycleways.geojson', 'utf-8', QgsCoordinateReferenceSystem(crs_from), 'GeoJson')



#---------------------------------------------------------------------------
# Vereinigt aneinander angrenzende Wegeflächen und erzeugt deren Outlines
#---------------------------------------------------------------------------
if proc_path_areas:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Verarbeite Wegeflächen...')
    layer_path_areas_raw = QgsVectorLayer(data_dir + 'path.geojson|geometrytype=Polygon', 'Wegeflächen', 'ogr')
    layer_path_areas = processing.run('native:dissolve', { 'FIELD' : ['highway'], 'INPUT' : layer_path_areas_raw, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_path_areas = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_path_areas, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_path_areas = clearAttributes(layer_path_areas, ['highway'])
    layer_path_areas = processing.run('native:polygonstolines', { 'INPUT' : layer_path_areas, 'OUTPUT' : proc_dir + 'path_areas_outlines.geojson' })



#--------------------------------------------------------------------------------------------------
# Separiert Schienensegmente mit Bahnübergängen, um diese über Fahrbahnflächen rendern zu können
#--------------------------------------------------------------------------------------------------
if proc_railways:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Verarbeite Bahnübergänge...')
    layer_railway_ways_raw = QgsVectorLayer(data_dir + 'railway.geojson|geometrytype=LineString', 'railway ways (raw)', 'ogr')
    layer_railway_nodes_raw = QgsVectorLayer(data_dir + 'railway.geojson|geometrytype=Point', 'railway nodes (raw)', 'ogr')
    layer_railway_crossings = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_railway_nodes_raw, 'EXPRESSION' : '"railway" = \'level_crossing\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_railway_crossing_ways = processing.run('native:extractbylocation', { 'INPUT' : layer_railway_ways_raw, 'INTERSECT' : layer_railway_crossings, 'PREDICATE' : [0], 'OUTPUT' : proc_dir + 'railway_crossings.geojson' })



#--------------------------------------------------------------------------------------------------------------
# Stockwerkszahl und schwebende Etagen für jedes Gebäudeteil/Gebäude auflösen, Gebäudegrundrisse verarbeiten
#--------------------------------------------------------------------------------------------------------------
if proc_buildings:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Verarbeite Gebäudeteile...')
    print(time.strftime('%H:%M:%S', time.localtime()), '   Lade Gebäudedaten...')
    layer_building_parts_raw = QgsVectorLayer(data_dir + 'building_part.geojson|geometrytype=Polygon', 'Gebäudeteile (roh)', 'ogr')
    layer_building_parts = processing.run('native:fixgeometries', { 'INPUT' : layer_building_parts_raw, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_parts = processing.run('native:reprojectlayer', { 'INPUT' : layer_building_parts, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_parts = clearAttributes(layer_building_parts, building_key_list)

    if not layer_raw_buildings_polygons:
        layer_raw_buildings_polygons = QgsVectorLayer(data_dir + 'buildings.geojson|geometrytype=Polygon', 'buildings (raw)', 'ogr')
    layer_buildings = processing.run('native:reprojectlayer', { 'INPUT' : layer_raw_buildings_polygons, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_buildings = clearAttributes(layer_buildings, building_key_list)

    QgsProject.instance().addMapLayer(layer_buildings, False)
    QgsProject.instance().addMapLayer(layer_building_parts, False)

    #Gebäudeteile ohne Stockwerksinformationen leiten diese von Gebäudeumriss ab
    print(time.strftime('%H:%M:%S', time.localtime()), '   Gebäudestockwerke differenzieren...')

    layer_building_parts_no_levels = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_building_parts, 'EXPRESSION' : '"building:levels" IS NULL', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_parts_no_levels = processing.run('native:deletecolumn', {'INPUT' : layer_building_parts_no_levels, 'COLUMN' : ['building:levels'], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_parts_no_levels = processing.run('native:joinattributesbylocation', {'INPUT': layer_building_parts_no_levels, 'JOIN' : layer_buildings, 'JOIN_FIELDS' : ['building:levels'], 'PREDICATE' : [0], 'METHOD' : 2, 'OUTPUT': 'memory:'})['OUTPUT']

    layer_building_parts_levels = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_building_parts, 'EXPRESSION' : '"building:levels" IS NOT NULL', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_parts_levels = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_building_parts_levels, layer_building_parts_no_levels], 'OUTPUT': 'memory:'})['OUTPUT']

    #Gebäude, die nicht von Gebäudeteilen abgedeckt sind, zum Gebäudeteilelayer hinzufügen
    layer_buildings_noparts = processing.run('native:difference', {'INPUT' : layer_buildings, 'OVERLAY' : layer_building_parts_levels, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_parts_levels = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_building_parts_levels, layer_buildings_noparts], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_parts_levels = clearAttributes(layer_building_parts_levels, ['building:levels'])

    #aneinander angrenzende Gebäudeteile mit gleicher Höhe auflösen
    layer_building_parts_levels = processing.run('native:dissolve', { 'INPUT' : layer_building_parts_levels, 'FIELD' : ['building:levels'], 'OUTPUT': 'memory:'})['OUTPUT']
    processing.run('native:multiparttosingleparts', { 'INPUT' : layer_building_parts_levels, 'OUTPUT' : proc_dir + 'building_parts.geojson' })

    #Gebäudegrundrisse erzeugen (Gebäudeflächen abzüglich aller Flächen mit min_level/min_height > 0 oder building=roof)
    print(time.strftime('%H:%M:%S', time.localtime()), '   Gebäudegrundrisse erzeugen...')
    layer_building_parts_min_level_1 = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_building_parts, 'EXPRESSION' : '\"building:min_level\" > 0 OR \"min_height\" > 0 OR \"building:part\" = \'roof\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_parts_min_level_0 = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_building_parts, 'EXPRESSION' : '((\"building:min_level\" <= 0 OR \"min_height\" <= 0) OR (\"building:min_level\" IS NULL AND \"min_height\" IS NULL)) AND \"building:part\" <> \'roof\'', 'OUTPUT': 'memory:'})['OUTPUT']
    QgsProject.instance().addMapLayer(layer_building_parts_min_level_1, False)
    QgsProject.instance().addMapLayer(layer_building_parts_min_level_0, False)

    #vorher Gebäudeteile ohne min_level von allen Gebäudeteilen abziehen, um Gebäudeteile innerhalb von (schwebenden) Gebäudeteilen zu berücksichtigen
    layer_building_parts_min_level = processing.run('native:difference', {'INPUT' : QgsProcessingFeatureSourceDefinition(layer_building_parts_min_level_1.id(), flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometrySkipInvalid), 'OVERLAY' : QgsProcessingFeatureSourceDefinition(layer_building_parts_min_level_0.id(), flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometrySkipInvalid), 'OUTPUT': 'memory:'})['OUTPUT']

    layer_building_footprints = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_buildings, 'EXPRESSION' : '\"building\" IS NOT \'roof\' AND ("building:min_level" <= 0 OR "building:min_level" IS NULL) AND ("min_height" <= 0 OR "min_height" IS NULL)', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_footprints = processing.run('native:difference', { 'INPUT': layer_building_footprints, 'OVERLAY' : layer_building_parts_min_level, 'OUTPUT': 'memory:'})['OUTPUT']

    #Linien für Gebäudegrundrisskanten erzeugen, je nach dem, ob sie unter schwebenden Gebäudeteilen verlaufen oder nicht
    print(time.strftime('%H:%M:%S', time.localtime()), '   Grundrisslinien differenzieren...')
    print(time.strftime('%H:%M:%S', time.localtime()), '      Grundrisslinien erzeugen...')
    layer_building_footprints_dissolved = processing.run('native:dissolve', { 'INPUT' : layer_building_footprints, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_footprint_lines = processing.run('native:polygonstolines', { 'INPUT' : layer_building_footprints_dissolved, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_footprint_lines = processing.run('native:explodelines', { 'INPUT' : layer_building_footprint_lines, 'OUTPUT': 'memory:'})['OUTPUT']
    #layer_building_footprint_lines = processing.run('native:deleteduplicategeometries', {'INPUT': layer_building_footprint_lines, 'OUTPUT': 'memory:'})['OUTPUT']

    print(time.strftime('%H:%M:%S', time.localtime()), '      Überdeckte Linien extrahieren...')
    layer_buildings_dissolved = processing.run('native:dissolve', { 'INPUT' : layer_buildings, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_buildings_dissolved = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_buildings_dissolved, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_footprint_lines_covered = processing.run('native:extractbylocation', { 'INPUT' : layer_building_footprint_lines, 'INTERSECT' : layer_buildings_dissolved, 'PREDICATE' : [6], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_footprint_lines_covered = processing.run('qgis:fieldcalculator', { 'INPUT': layer_building_footprint_lines_covered, 'FIELD_NAME': 'covered', 'FIELD_TYPE': 2, 'FIELD_LENGTH': 3, 'FIELD_PRECISION': 0, 'NEW_FIELD': True, 'FORMULA': "'yes'", 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_footprint_lines_covered = processing.run('native:deletecolumn', {'INPUT' : layer_building_footprint_lines_covered, 'COLUMN' : building_key_list, 'OUTPUT': 'memory:'})['OUTPUT']

    print(time.strftime('%H:%M:%S', time.localtime()), '      Übrige Gebäudekanten extrahieren...')
    layer_building_lines = processing.run('native:polygonstolines', { 'INPUT' : layer_building_footprints, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_lines = processing.run('native:explodelines', { 'INPUT' : layer_building_lines, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_lines = processing.run('native:deleteduplicategeometries', {'INPUT': layer_building_lines, 'OUTPUT': 'memory:'})['OUTPUT']
    processing.run('native:selectbylocation', {'INPUT' : layer_building_lines, 'INTERSECT' : layer_building_footprint_lines_covered, 'PREDICATE' : [3]})
    with edit(layer_building_lines):
        layer_building_lines.deleteSelectedFeatures()
    layer_building_lines = processing.run('qgis:fieldcalculator', { 'INPUT': layer_building_lines, 'FIELD_NAME': 'covered', 'FIELD_TYPE': 2, 'FIELD_LENGTH': 3, 'FIELD_PRECISION': 0, 'NEW_FIELD': True, 'FORMULA': "'no'", 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_lines = processing.run('native:deletecolumn', {'INPUT' : layer_building_lines, 'COLUMN' : building_key_list, 'OUTPUT': 'memory:'})['OUTPUT']

    layer_building_lines = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_building_footprint_lines_covered, layer_building_lines], 'OUTPUT': 'memory:'})['OUTPUT']
    processing.run('native:retainfields', { 'INPUT' : layer_building_lines, 'FIELDS' : ['covered'], 'OUTPUT' : proc_dir + 'building_lines.geojson' })



#--------------------------------------------------
# Hausnummern an inneren Gebäudeumring versetzen
#--------------------------------------------------
if proc_housenumbers:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Verarbeite Hausnummern...')
    #Gebäude und Hausnummern neu in metrischer Projektion abspeichern
    print(time.strftime('%H:%M:%S', time.localtime()), '   Wandle Daten in metrische Projektion...')
    if not layer_raw_buildings_polygons:
        layer_raw_buildings_polygons = QgsVectorLayer(data_dir + 'buildings.geojson|geometrytype=Polygon', 'buildings (raw)', 'ogr')
    layer_buildings = layer_raw_buildings_polygons
    layer_buildings = clearAttributes(layer_buildings, building_key_list)
    layer_housenumbers = QgsVectorLayer(data_dir + 'housenumber.geojson|geometrytype=Point', 'Hausnummern (Punktdaten, roh)', 'ogr')
    layer_housenumbers = clearAttributes(layer_housenumbers, ['id', 'addr:housenumber', 'addr:postcode', 'addr:street', 'addr:suburb'])

    QgsVectorFileWriter.writeAsVectorFormatV2(layer_buildings, proc_dir + 'buildings.geojson', transform_context, save_options)
    QgsVectorFileWriter.writeAsVectorFormatV2(layer_housenumbers, proc_dir + 'housenumber.geojson', transform_context, save_options)
    layer_buildings = QgsVectorLayer(proc_dir + 'buildings.geojson|geometrytype=Polygon', 'Gebäude', 'ogr')
    layer_housenumbers = QgsVectorLayer(proc_dir + 'housenumber.geojson|geometrytype=Point', 'Hausnummern (Punktdaten)', 'ogr')

    #Puffer um Gebäudegrenzen ziehen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Erzeuge Gebäudepuffer...')
    layer_buildings_buffer = processing.run('native:polygonstolines', { 'INPUT' : layer_buildings, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_buildings_buffer = processing.run('native:buffer', { 'INPUT' : layer_buildings_buffer, 'DISTANCE' : 2, 'OUTPUT': 'memory:'})['OUTPUT']

    layer_buildings_shrinked = processing.run('native:difference', {'INPUT' : layer_buildings, 'OVERLAY' : layer_buildings_buffer, 'OUTPUT': 'memory:'})['OUTPUT']

    #Hausnummern am Puffer ausrichten
    print(time.strftime('%H:%M:%S', time.localtime()), '   Richte Hausnummern aus...')
    layer_housenumbers = processing.run('native:snapgeometries', { 'BEHAVIOR' : 1, 'INPUT' : layer_housenumbers, 'REFERENCE_LAYER' : layer_buildings_shrinked, 'TOLERANCE' : 2.05, 'OUTPUT' : proc_dir + 'housenumber_snapped.geojson' })



#----------------------------------------------------
# Gewässerkörper zu einem Einzelpolygon vereinigen
#----------------------------------------------------
if proc_water_body:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Vereinige Wasserkörper...')
    if not layer_raw_natural_polygons:
        layer_raw_natural_polygons = QgsVectorLayer(data_dir + 'natural.geojson|geometrytype=Polygon', 'natural (polygon)', 'ogr')
    layer_water = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_natural_polygons, 'EXPRESSION' : '\"natural\" = \'water\' OR \"natural\" = \'wetland\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_water = clearAttributes(layer_water, ['natural'])
    processing.run('native:dissolve', { 'INPUT' : layer_water, 'OUTPUT' : proc_dir + 'water_body.geojson' })



#------------------------------------------------------------------------------------
# Bereiche mit "landcover=*" in Polygone umwandeln (werden nur als Linien erkannt)
#------------------------------------------------------------------------------------
if proc_landcover:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Wandel landcover-Objekte in Polygone um...')
    layer_landcover_lines = QgsVectorLayer(data_dir + 'landuse.geojson|geometrytype=LineString', 'landuse lines (raw)', 'ogr')
    QgsProject.instance().addMapLayer(layer_landcover_lines, False)
    if not layer_raw_landuse_polygons:
        layer_raw_landuse_polygons = QgsVectorLayer(data_dir + 'landuse.geojson|geometrytype=Polygon', 'landuse polygons (raw)', 'ogr')
    layer_landcover_polygons = layer_raw_landuse_polygons

    #nur geschlossene Linien zu Polygonen umwandeln
    layer_landcover_lines.selectAll()
    for f in layer_landcover_lines.getFeatures():
        geom = f.geometry()
        line = geom.asPolyline()
        if line[0].x() != line[-1].x() or line[0].y() != line[-1].y():
            layer_landcover_lines.deselect(f.id())

    lines_to_poly = processing.run('qgis:linestopolygons', { 'INPUT': QgsProcessingFeatureSourceDefinition(layer_landcover_lines.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']
    polygons = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_landcover_polygons, 'EXPRESSION' : '\"landcover\" IS NOT NULL', 'OUTPUT': 'memory:'})['OUTPUT']
    landcover = processing.run('native:mergevectorlayers', { 'LAYERS' : [lines_to_poly, polygons], 'OUTPUT': 'memory:'})['OUTPUT']
    landcover = clearAttributes(landcover, ['id', 'landcover'])
    QgsVectorFileWriter.writeAsVectorFormatV2(landcover, proc_dir + 'landcover.geojson', transform_context, save_options)



#----------------------------------------------------------
# Erzeugt Texturen für Sportfelder und richtet diese aus
#----------------------------------------------------------
if proc_pitches:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Erzeuge Texturen für Sportfelder...')

    #Sportfelder auswählen und deren Stützpunkte ermitteln
    layer_pitches = QgsVectorLayer(data_dir + 'leisure.geojson|geometrytype=Polygon', 'Sportfelder', 'ogr')
    layer_pitches = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_pitches, 'EXPRESSION' : '"leisure" = \'pitch\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_pitches = processing.run('native:reprojectlayer', { 'INPUT' : layer_pitches, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']

    layer_vertices = processing.run('native:extractvertices', {'INPUT': layer_pitches, 'OUTPUT': 'memory:'})['OUTPUT']

    #Mittelpunkte erzeugen, um dort später Spielfeld darzustellen
    layer_centroids = processing.run('native:centroids', {'INPUT': layer_pitches, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_centroids.startEditing()
    #unnötige Attribute löschen
    layer_centroids = clearAttributes(layer_centroids, ['id', 'leisure', 'sport', 'surface', 'name', 'capacity'])

    #neue Attribute für Länge, Breite und Ausrichtung anlegen
    for attribute in ['@pitch_dist_long', '@pitch_dist_short', '@pitch_direction']:
        if layer_centroids.dataProvider().fieldNameIndex(attribute) == -1:
            layer_centroids.dataProvider().addAttributes([QgsField(attribute, QVariant.Double)])

    layer_centroids.updateFields()
    layer_centroids.commitChanges()

    pitch_dict = {}

    #dict für alle Sportfelder mit ihren Stützpunkten und zugehörogen Abständen und Winkeln anlegen
    for pitch in layer_pitches.getFeatures():
        sport = pitch.attribute('sport')
        id = pitch.attribute('id')
        pitch_dict[id] = {}
        distance = distance_last = 0
        for vertex in layer_vertices.getFeatures():
            if vertex.attribute('id') != id:
                continue
            index = vertex.attribute('vertex_index')
            geom = vertex.geometry()
            coord = geom.asPoint()

            x = coord.x()
            y = coord.y()
            distance += vertex.attribute('distance') - distance_last
            distance_last = vertex.attribute('distance')
            angle = vertex.attribute('angle')

            pitch_dict[id][index] = { 'x': x, 'y': y, 'distance': distance, 'distance_edge': -1, 'angle': angle, 'edge': -1 }

    #Eckpunkte und daraus Eigenschaften für jedes Sportfeld ermitteln
    for pitch in pitch_dict:
        for vertex in pitch_dict[pitch]:
            angle = pitch_dict[pitch][vertex]['angle']
            vertex_max = max(pitch_dict[pitch])
            if vertex > 1:
                vertex_before = vertex - 1
            else:
                vertex_before = vertex_max
            angle_before = pitch_dict[pitch][vertex_before]['angle']

            if vertex < vertex_max:
                vertex_after = vertex + 1
            else:
                vertex_after = 1
            angle_after = pitch_dict[pitch][vertex_after]['angle']

            #Wenn vorheriger oder nachfolgender Vertex ähnliche Winkelangabe hat, dannliegt dieser Vertex mit diesen auf einer Linie und ist kein Eckvertex
            if vertex == 0 or abs(angle - angle_before) < 20 or abs(angle - angle_after) < 20:
                pitch_dict[pitch][vertex]['edge'] = 0
                continue
            else:
                pitch_dict[pitch][vertex]['edge'] = 1

        #Eck-Abstände ermitteln: Abstand zum jeweils vorherigen Eck-Vertex speichern
        distance_last_edge = 0
        distances = []
        angles = []
        #Für alle Eck-Vertices:
        for vertex in (vertex2 for vertex2 in pitch_dict[pitch] if pitch_dict[pitch][vertex2]['edge'] == 1):
            angles.append(pitch_dict[pitch][vertex]['angle'])
            if distance_last_edge == 0:
                distance_last_edge = pitch_dict[pitch][vertex]['distance']
                pitch_dict[pitch][vertex]['distance_edge'] = distance_last_edge
                distances.append(distance_last_edge)
            else:
                d = pitch_dict[pitch][vertex]['distance'] - distance_last_edge
                pitch_dict[pitch][vertex]['distance_edge'] = d
                distances.append(d)
                distance_last_edge = pitch_dict[pitch][vertex]['distance']

        #Gibt es 4 Ecken, handelt es sich um ein rechteckiges Feld
        #TODO: Prüfung, ob zwei lange und zwei kurze Distanzen je etwa gleich lang – sonst kein Rechteck
        if len(distances) != 4:
            continue
        distance1 = ((distances[0] + distances[2]) / 2)
        distance2 = ((distances[1] + distances[3]) / 2)
        if distance1 < distance2:
            distance_short = distance1
            distance_long = distance2
            angle1 = ((angles[0] + angles[1]) / 2)
            angle2 = ((angles[2] + angles[3]) / 2)
        else:
            distance_short = distance2
            distance_long = distance1
            angle1 = ((angles[1] + angles[2]) / 2)
            angle2 = ((angles[3] + angles[0]) / 2)

        if abs(angle1 - angle2) < 90:
            angle = (angle1 + angle2) / 2
        else:
            angle = (angle1 + angle2 - 180) / 2

        pitch_dict[pitch]['@pitch_dist_long'] = distance_long
        pitch_dict[pitch]['@pitch_dist_short'] = distance_short
        pitch_dict[pitch]['@pitch_direction'] = angle

    #Eigenschaften auf Sportfeld-Mittelpunkte übertragen
    layer_centroids.startEditing()
    index_long = layer_centroids.dataProvider().fieldNameIndex('@pitch_dist_long')
    index_short = layer_centroids.dataProvider().fieldNameIndex('@pitch_dist_short')
    index_dir = layer_centroids.dataProvider().fieldNameIndex('@pitch_direction')
    for pitch in layer_centroids.getFeatures():
        id = pitch.id()
        osm_id = pitch.attribute('id')
        if '@pitch_dist_long' in pitch_dict[osm_id]:
            layer_centroids.changeAttributeValue(pitch.id(), index_long, pitch_dict[osm_id]['@pitch_dist_long'])
            layer_centroids.changeAttributeValue(pitch.id(), index_short, pitch_dict[osm_id]['@pitch_dist_short'])
            layer_centroids.changeAttributeValue(pitch.id(), index_dir, pitch_dict[osm_id]['@pitch_direction'])
        else:
            layer_centroids.deleteFeature(id)

    layer_centroids.updateFields()
    layer_centroids.commitChanges()

    qgis.core.QgsVectorFileWriter.writeAsVectorFormat(layer_centroids, proc_dir + 'pitch_marker.geojson', 'utf-8', QgsCoordinateReferenceSystem(crs_from), 'GeoJson')



#-----------------------------------------------------------------------------
# Gras-Flächen zur besseren Darstellung aus playground-Polygonen ausstanzen
#-----------------------------------------------------------------------------
if proc_playgr_landuse:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Stanze Gras-Flächen aus Spielplatzflächen aus...')
    if not layer_raw_landuse_polygons:
        layer_raw_landuse_polygons = QgsVectorLayer(data_dir + 'landuse.geojson|geometrytype=Polygon', 'landuse polgons (raw)', 'ogr')
    layer_grass = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_landuse_polygons, 'EXPRESSION' : '"landuse" = \'grass\'', 'OUTPUT': 'memory:'})['OUTPUT']
    if not layer_raw_leisure_polygons:
        layer_raw_leisure_polygons = QgsVectorLayer(data_dir + 'leisure.geojson|geometrytype=Polygon', 'leisure polgons (raw)', 'ogr')
    layer_playgrounds = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_leisure_polygons, 'EXPRESSION' : '"leisure" = \'playground\'', 'OUTPUT': 'memory:'})['OUTPUT']
    #Grasflächen auswählen, die in Spielplätzen liegen oder diese überlappen
    layer_grass_overlay = processing.run('native:extractbylocation', { 'INPUT' : layer_grass, 'INTERSECT' : layer_playgrounds, 'PREDICATE' : [5,6], 'OUTPUT': 'memory:'})['OUTPUT']
    #ausgewählte Grasflächen von Spielplatzflächen abziehen
    layer_playgrounds = processing.run('native:difference', {'INPUT' : layer_playgrounds, 'OVERLAY' : layer_grass_overlay, 'OUTPUT' : proc_dir + 'playgrounds_clipped.geojson' })



#-----------------------------------------------------------------------------
# Geschlossene Linien bei Spielgeräten zu Polygonen umwandeln
#-----------------------------------------------------------------------------
if proc_playgr_equip:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Wandel playground-Objekte in Polygone um...')
    layer_playground_lines = QgsVectorLayer(data_dir + 'playground.geojson|geometrytype=LineString', 'playground lines (raw)', 'ogr')
    QgsProject.instance().addMapLayer(layer_playground_lines, False)
    layer_raw_playground_polygons = QgsVectorLayer(data_dir + 'playground.geojson|geometrytype=Polygon', 'playground polygons (raw)', 'ogr')
    layer_playground_polygons = layer_raw_playground_polygons

    #nur geschlossene Linien zu Polygonen umwandeln
    layer_playground_lines.selectAll()
    for f in layer_playground_lines.getFeatures():
        geom = f.geometry()
        line = geom.asPolyline()
        if line[0].x() != line[-1].x() or line[0].y() != line[-1].y():
            layer_playground_lines.deselect(f.id())

    lines_to_poly = processing.run('qgis:linestopolygons', { 'INPUT': QgsProcessingFeatureSourceDefinition(layer_playground_lines.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']
    polygons = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_playground_polygons, 'EXPRESSION' : '\"playground\" IS NOT NULL', 'OUTPUT': 'memory:'})['OUTPUT']
    playground = processing.run('native:mergevectorlayers', { 'LAYERS' : [lines_to_poly, polygons], 'OUTPUT': 'memory:'})['OUTPUT']
    playground = clearAttributes(playground, ['id', 'playground'])
    QgsVectorFileWriter.writeAsVectorFormatV2(playground, proc_dir + 'playground_equipment_areas.geojson', transform_context, save_options)



#----------------------------------------------------------------------------------------------------------------------------
# Richtet bestimmte Straßenmöbel zur nächstgelegenen Straße hin aus (Straßenlaternen, Schaltkästen, BSR-Transportüberwege)
#----------------------------------------------------------------------------------------------------------------------------
if proc_orient_man_made:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Straßenmöbel ausrichten...')
    print(time.strftime('%H:%M:%S', time.localtime()), '   Straßenreferenz einladen...')
    if not layer_raw_highway_ways:
        layer_raw_highway_ways = QgsVectorLayer(data_dir + 'highway.geojson|geometrytype=LineString', 'highway (raw)', 'ogr')
    if not layer_raw_path_ways:
        layer_raw_path_ways = QgsVectorLayer(data_dir + 'path.geojson|geometrytype=LineString', 'path (raw)', 'ogr')

    print(time.strftime('%H:%M:%S', time.localtime()), '   Straßenmöbel einladen...')
    if not layer_raw_man_made_points:
        layer_raw_man_made_points = QgsVectorLayer(data_dir + 'man_made.geojson|geometrytype=Point', 'man_made (raw)', 'ogr')

    #Straßenmöbel filtern, für die eine Richtung relevant sein kann (Straßenlaternen, Schaltkästen)
    layer_street_furniture_vanilla = processing.run('native:reprojectlayer', { 'INPUT' : layer_raw_man_made_points, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_street_furniture = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_street_furniture_vanilla, 'EXPRESSION' : '("highway" = \'street_lamp\' AND "lamp_mount" = \'bent_mast\') OR "man_made" = \'street_cabinet\' OR "amenity" = \'loading_ramp\'', 'OUTPUT': 'memory:'})['OUTPUT']

    #Puffer (12 Meter) um relevante Straßenmöbel erzeugen, um im Folgenden nur Straßen in diesem Bereich zu berücksichtigen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Relevante Straßen und Wege selektieren...')
    layer_street_furniture_buffer_12 = processing.run('native:buffer', { 'INPUT' : layer_street_furniture, 'DISTANCE' : 12, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_street_furniture_buffer_5 = processing.run('native:buffer', { 'INPUT' : layer_street_furniture, 'DISTANCE' : 5, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_next_streets = processing.run('native:intersection', { 'INPUT' : layer_raw_highway_ways, 'INPUT_FIELDS' : ['id','highway'], 'OVERLAY' : layer_street_furniture_buffer_12, 'OVERLAY_FIELDS' : ['man_made', 'amenity'], 'OVERLAY_FIELDS_PREFIX' : '', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_next_roads = processing.run('qgis:extractbyexpression', {'INPUT' : layer_next_streets, 'EXPRESSION' : '"highway" IS \'primary\' or "highway" IS \'secondary\' or "highway" IS \'tertiary\' or "highway" IS \'residential\' or "highway" IS \'unclassified\' or "highway" IS \'living_street\' or "highway" IS \'pedestrian\' or "highway" IS \'road\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_next_roads = processing.run('native:reprojectlayer', { 'INPUT' : layer_next_roads, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']

    layer_next_ways = processing.run('native:intersection', { 'INPUT' : layer_next_streets, 'INPUT_FIELDS' : ['id','highway'], 'OVERLAY' : layer_street_furniture_buffer_5, 'OVERLAY_FIELDS' : ['man_made', 'amenity'], 'OVERLAY_FIELDS_PREFIX' : '', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_next_ways = processing.run('qgis:extractbyexpression', {'INPUT' : layer_next_ways, 'EXPRESSION' : '"highway" IS NOT \'primary\' and "highway" IS NOT \'secondary\' and "highway" IS NOT \'tertiary\' and "highway" IS NOT \'residential\' and "highway" IS NOT \'unclassified\' and "highway" IS NOT \'living_street\' and "highway" IS NOT \'pedestrian\' and "highway" IS NOT \'road\'', 'OUTPUT': 'memory:'})['OUTPUT']

    layer_next_path = processing.run('native:intersection', { 'INPUT' : layer_raw_path_ways, 'INPUT_FIELDS' : ['id','highway'], 'OVERLAY' : layer_street_furniture_buffer_5, 'OVERLAY_FIELDS' : ['man_made', 'amenity'], 'OVERLAY_FIELDS_PREFIX' : '', 'OUTPUT': 'memory:'})['OUTPUT']

    #Sonstige Straßen/Zufahrten und Wege/Pfade zusammenführen
    layer_next_ways = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_next_ways, layer_next_path], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_next_ways = processing.run('native:reprojectlayer', { 'INPUT' : layer_next_ways, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']

    QgsProject.instance().addMapLayer(layer_next_roads, False)
    QgsProject.instance().addMapLayer(layer_next_ways, False)
    QgsProject.instance().addMapLayer(layer_street_furniture, False)
    QgsProject.instance().addMapLayer(layer_street_furniture_buffer_12, False)
    QgsProject.instance().addMapLayer(layer_street_furniture_buffer_5, False)

    #Zunächst Verbindung zu nächstgelegener Verkehrsstraße suchen
    print(time.strftime('%H:%M:%S', time.localtime()), '   An Verkehrsstraßen ausrichten...')
    #Diejenigen Pufferkreise auswählen, in denen Verkehrsstraßen liegen
    processing.run('native:selectbylocation', { 'INPUT' : layer_street_furniture_buffer_12, 'INTERSECT' : layer_next_roads, 'METHOD' : 0, 'PREDICATE' : [0] })

    id_list_roads = []

    #id's der Objekte speichern, in deren Umkreis sich Verkehrsstraßen befinden
    for street_furniture in layer_street_furniture_buffer_12.getSelectedFeatures():
        id = street_furniture.attribute('id')
        id_list_roads.append(id)

    #Objekte mit gespeicherten id's selectieren und auf Verkehrsstraßen snappen - aus Verbindungslinie kann anschließend die Richtung der nächsten Straße ermittelt werden
    layer_street_furniture.removeSelection()
    for street_furniture in layer_street_furniture.getFeatures():
        id = street_furniture.attribute('id')
        if id in id_list_roads:
            layer_street_furniture.select(street_furniture.id())

#    layer_street_furniture_snapped_roads = processing.run('native:snapgeometries', { 'BEHAVIOR' : 1, 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_street_furniture.id(), selectedFeaturesOnly=True), 'REFERENCE_LAYER' : layer_next_roads, 'TOLERANCE' : 12, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_street_furniture_snapped_roads = processing.run('native:geometrybyexpression', { 'EXPRESSION' : 'closest_point(aggregate(\'' + layer_next_roads.id() + '\', \'collect\', $geometry), $geometry)', 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_street_furniture.id(), selectedFeaturesOnly=True), 'OUTPUT_GEOMETRY' : 2, 'OUTPUT': 'memory:'})['OUTPUT']

    #Falls keine Verkehrsstraßen in der Nähe, an sonstigen Wegen ausrichten
    print(time.strftime('%H:%M:%S', time.localtime()), '   An sonstigen Wegen ausrichten...')
    #Diejenigen Pufferkreise auswählen, in denen sonstige Wege liegen
    processing.run('native:selectbylocation', { 'INPUT' : layer_street_furniture_buffer_5, 'INTERSECT' : layer_next_ways, 'METHOD' : 0, 'PREDICATE' : [0] })

    id_list_ways = []

    #id's der Objekte speichern, in deren Umkreis sich sonstige Wege befinden (außer sie wurden bereits an Verkehrsstraßen ausgerichtet)
    for street_furniture in layer_street_furniture_buffer_5.getSelectedFeatures():
        id = street_furniture.attribute('id')
        if id in id_list_roads:
            continue
        id_list_ways.append(id)

    #Objekte mit gespeicherten id's selektieren und auf sonstige Wege snappen - aus Verbindungslinie kann anschließend die Richtung der nächsten Straße ermittelt werden
    layer_street_furniture.removeSelection()
    for street_furniture in layer_street_furniture.getFeatures():
        id = street_furniture.attribute('id')
        if id in id_list_ways:
            layer_street_furniture.select(street_furniture.id())

    layer_street_furniture_snapped_ways = processing.run('native:geometrybyexpression', { 'EXPRESSION' : 'closest_point(aggregate(\'' + layer_next_ways.id() + '\', \'collect\', $geometry), $geometry)', 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_street_furniture.id(), selectedFeaturesOnly=True), 'OUTPUT_GEOMETRY' : 2, 'OUTPUT': 'memory:'})['OUTPUT']
#    layer_street_furniture_snapped_ways = processing.run('native:snapgeometries', { 'BEHAVIOR' : 1, 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_street_furniture.id(), selectedFeaturesOnly=True), 'REFERENCE_LAYER' : layer_next_ways, 'TOLERANCE' : 5, 'OUTPUT': 'memory:'})['OUTPUT']

    #gesnappte Punkte zusammenführen
    layer_street_furniture_snapped = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_street_furniture_snapped_roads, layer_street_furniture_snapped_ways], 'OUTPUT': 'memory:'})['OUTPUT']

    #Verbindungslinien zwischen Objekten und "ihren" gesnappten Geschwistern erzeugen
    layer_street_furniture_hublines = processing.run('native:hublines', { 'HUBS' : layer_street_furniture, 'HUB_FIELD' : 'id', 'SPOKES' : layer_street_furniture_snapped, 'SPOKE_FIELD' : 'id', 'OUTPUT': 'memory:'})['OUTPUT']

    #Richtung am ersten Vertex dieser Verbindungslinie entspricht dem Winkel zum nächstgelegenen Weg
    layer_street_furniture_oriented = processing.run('native:extractspecificvertices', { 'INPUT' : layer_street_furniture_hublines, 'VERTICES' : 0, 'OUTPUT': 'memory:'})['OUTPUT']

    #zweiten Vertex der Verbindungslinie ebenfalls extrahieren - befindet sich dieser am selben Ort wie das Objekt, hat kein snapping stattgefunden - also befindet sich kein Weg in Reichweite - in diesem Fall löschen/Ausrichtung = 0
    layer_street_furniture_vertex1 = processing.run('native:extractspecificvertices', { 'INPUT' : layer_street_furniture_hublines, 'VERTICES' : 1, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_street_furniture_oriented = processing.run('native:extractbylocation', { 'INPUT' : layer_street_furniture_oriented, 'INTERSECT' : layer_street_furniture_vertex1, 'METHOD' : 0, 'PREDICATE' : [2], 'OUTPUT': 'memory:'})['OUTPUT']

    #mit ursprünglichem man_made-Layer vereinigen (ursprüngliche Objekte an Positionen ausgerichteter Objekte ersetzen)
    print(time.strftime('%H:%M:%S', time.localtime()), '   Vereinige ausgerichtete Straßenmöbel...')
    layer_street_furniture = processing.run('native:extractbylocation', { 'INPUT' : layer_street_furniture_vanilla, 'INTERSECT' : layer_street_furniture_oriented, 'PREDICATE' : [2], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_street_furniture = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_street_furniture, layer_street_furniture_oriented], 'OUTPUT': 'memory:'})['OUTPUT']
    print(time.strftime('%H:%M:%S', time.localtime()), '   Bereinige Daten...')
    layer_street_furniture = clearAttributes(layer_street_furniture, ['id', 'man_made', 'highway', 'direction', 'angle', 'ref', 'street_cabinet', 'width', 'length', 'lamp_mount', 'amenity'])
    print(time.strftime('%H:%M:%S', time.localtime()), '   Speichere Daten...')

    qgis.core.QgsVectorFileWriter.writeAsVectorFormat(layer_street_furniture, proc_dir + 'street_furniture.geojson', 'utf-8', QgsCoordinateReferenceSystem(crs_from), 'GeoJson')



#------------------------------------------------
# Baumkronendurchmesser und Stammumfang abschätzen
#------------------------------------------------
if proc_trees:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Baumkronendurchmesser abschätzen...')
    #Bäume in separatem Layer speichern
    layer_trees = QgsVectorLayer(data_dir + 'natural.geojson|geometrytype=Point', 'Bäume', 'ogr')
    layer_trees = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_trees, 'EXPRESSION' : '"natural" = \'tree\' or "natural" = \'tree_stump\' or "natural" = \'shrub\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_trees = clearAttributes(layer_trees, ['id', 'natural', 'leaf_type', 'ref', 'tree:ref', 'height', 'diameter_crown', 'circumference', 'genus'])

    #Durchmesser und Umfang aus direkten oder indirekten Attributen ableiten (diameter_crown, height, circumference)
    layer_trees.startEditing()
    id_diameter = layer_trees.fields().indexOf('diameter_crown')
    id_circumference = layer_trees.fields().indexOf('circumference')
    for feature in layer_trees.getFeatures():
        diameter = feature.attribute('diameter_crown')
        circumference = feature.attribute('circumference')
        if feature.attribute('natural') == 'tree' or feature.attribute('natural') == 'shrub':
            if diameter == NULL:
                circumference = feature.attribute('circumference')
                height = feature.attribute('height')
                if circumference:
                    try:
                        diameter = float(circumference) * 7.5
                    except:
                        diameter = random.uniform(6, 9)
                if height:
                    try:
                        diameter = float(height) * 0.6
                    except:
                        diameter = random.uniform(6, 9)
                if circumference and height:
                    try:
                        diameter_c = float(circumference) * 7.5
                        diameter_h = float(height) * 0.6
                        diameter = (diameter_c + diameter_h) / 2
                    except:
                        diameter = random.uniform(6, 9)
                if feature.attribute('natural') == 'shrub':
                    if diameter > 8:
                        diameter = 8
                    if diameter == NULL:
                        diameter = random.uniform(3, 6)
                else:
                    if diameter > 24:
                        diameter = 24
                    if diameter == NULL:
                        diameter = random.uniform(6, 9)

                layer_trees.changeAttributeValue(feature.id(), id_diameter, "%.1f" % float(diameter))

        if circumference == NULL:
            circumference = random.uniform(0.7, 1.2)
            if diameter != NULL:
                try:
                    circumference = float(diameter) / 7.5
                except:
                    circumference = random.uniform(0.7, 1.2)

            layer_trees.changeAttributeValue(feature.id(), id_circumference, "%.1f" % float(circumference))

    layer_trees.updateFields()
    layer_trees.commitChanges()
    QgsVectorFileWriter.writeAsVectorFormatV2(layer_trees, proc_dir + 'trees.geojson', transform_context, save_options)



#-------------------------------------------------------
# Waldbäume über ein hexagonales Gitter interpolieren
#-------------------------------------------------------
if proc_forests:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Waldbäume interpolieren...')
    if not layer_raw_landuse_polygons:
        layer_raw_landuse_polygons = QgsVectorLayer(data_dir + 'landuse.geojson|geometrytype=Polygon', 'landuse polgons (raw)', 'ogr')
    if not layer_raw_natural_polygons:
        layer_raw_natural_polygons = QgsVectorLayer(data_dir + 'natural.geojson|geometrytype=Polygon', 'natural (polygon)', 'ogr')
    layer_raw_landcover_polygons = QgsVectorLayer(proc_dir + 'landcover.geojson|geometrytype=Polygon', 'landcover polygons (post processed)', 'ogr')

    layer_forest = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_landuse_polygons, 'EXPRESSION' : '"landuse" = \'forest\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_wood = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_natural_polygons, 'EXPRESSION' : '"natural" = \'wood\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_trees = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_landcover_polygons, 'EXPRESSION' : '"landcover" = \'trees\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_forest = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_forest, layer_wood, layer_trees], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_forest = clearAttributes(layer_forest, ['id', 'landuse', 'landcover', 'natural', 'name', 'leaf_type', 'leaf_cycle'])
    #Waldflächen um 1,5 Meter schrumpfen, damit Bäume nicht unmittelbar am Rand stehen
    layer_forest = processing.run('native:reprojectlayer', { 'INPUT' : layer_forest, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_forest = processing.run('native:buffer', { 'INPUT' : layer_forest, 'DISTANCE' : -1.5, 'SEGMENTS' : 5, 'OUTPUT': 'memory:'})['OUTPUT']

    #Hexagonales Gitter erzeugen und auf Wald beschneiden
    print(time.strftime('%H:%M:%S', time.localtime()), '   Erzeuge hexagonales Gitter...')

    extent = layer_forest.extent()
    xmin = extent.xMinimum()
    xmax = extent.xMaximum()
    ymin = extent.yMinimum()
    ymax = extent.yMaximum()
    coords = '%f,%f,%f,%f' %(xmin, xmax, ymin, ymax)
    coords = coords + ' [' + crs_to + ']'
    layer_forest_grid = processing.run('native:creategrid', { 'CRS' : QgsCoordinateReferenceSystem(crs_to), 'EXTENT' : coords, 'TYPE' : 4, 'HOVERLAY' : 0, 'VOVERLAY' : 0, 'HSPACING' : 6, 'VSPACING' : 6, 'OUTPUT': 'memory:'})['OUTPUT']

    print(time.strftime('%H:%M:%S', time.localtime()), '   Beschneide Gitter auf Waldflächen...')
    layer_forest_grid = processing.run('native:clip', {'INPUT': layer_forest_grid, 'OVERLAY': layer_forest, 'OUTPUT': 'memory:'})['OUTPUT']

    print(time.strftime('%H:%M:%S', time.localtime()), '   Schrumpfe Gitterfelder...')
    layer_forest_grid = processing.run('native:buffer', { 'INPUT' : layer_forest_grid, 'DISTANCE' : -0.75, 'SEGMENTS' : 1, 'OUTPUT': 'memory:'})['OUTPUT']

    print(time.strftime('%H:%M:%S', time.localtime()), '   Erzeuge zufällige Baumpunkte...')
    layer_tree_points = processing.run('qgis:randompointsinsidepolygons', { 'INPUT' : layer_forest_grid, 'STRATEGY' : 0, 'VALUE' : 1, 'OUTPUT': 'memory:'})['OUTPUT']

    print(time.strftime('%H:%M:%S', time.localtime()), '   Ermittle Baumeigenschaften...')
    #leaf_type aus Waldfläche übertragen
    layer_tree_points = processing.run('native:joinattributesbylocation', {'INPUT': layer_tree_points, 'JOIN' : layer_forest, 'JOIN_FIELDS' : ['leaf_type'], 'METHOD' : 1, 'PREDICATE' : [5], 'OUTPUT': 'memory:'})['OUTPUT']

    #Neue Attribute für Baumeigenschaften anlegen: Baumtyp, Baumkronendurchmesser, Drehwinkel
    layer_tree_points.startEditing()
    layer_tree_points.dataProvider().addAttributes([QgsField('@leaf_type', QVariant.String)])
    layer_tree_points.dataProvider().addAttributes([QgsField('@diameter_crown', QVariant.String)])
    layer_tree_points.dataProvider().addAttributes([QgsField('@rotation', QVariant.String)])
    layer_tree_points.updateFields()
    id_leaf_type = layer_tree_points.fields().indexOf('@leaf_type')
    id_diameter_crown = layer_tree_points.fields().indexOf('@diameter_crown')
    id_rotation = layer_tree_points.fields().indexOf('@rotation')

    #Bäume durchgehen und Attribute zufällig festlegen bzw. aus Waldeigenschaften ableiten
    leaf_types = ['broadleaved', 'needleleaved']
    for tree in layer_tree_points.getFeatures():
        leaf_type = tree.attribute('leaf_type')
        if leaf_type not in leaf_types:
            if leaf_type == 'mixed':
                #in einem Mischwald jeden vierten Baum als Nadelbaum darstellen
                rnd = 3
            else:
                #wenn Baumtyp unbekannt, 1 Nadelbaum auf 10 Laubbäume darstellen
                rnd = 10
            if random.randint(0, rnd):
                leaf_type = 'broadleaved'
            else:
                leaf_type = 'needleleaved'

        #Baumkronendurchmesser zufällig zwischen 6 und 11 Metern
        diameter_crown = round(random.uniform(6, 11), 1)
        #zufällige leichte Rotation zwischen -20 und 20 Grad, um Konformität zu vermeiden, aber auch Beleuchtungsrichtung (bei "3D"-Darstellung) zu bewahren
        rotation = random.randint(-20, 20)
        
        layer_tree_points.changeAttributeValue(tree.id(), id_leaf_type, leaf_type)
        layer_tree_points.changeAttributeValue(tree.id(), id_diameter_crown, diameter_crown)
        layer_tree_points.changeAttributeValue(tree.id(), id_rotation, rotation)
    layer_tree_points.updateFields()
    layer_tree_points.commitChanges()
    qgis.core.QgsVectorFileWriter.writeAsVectorFormat(layer_tree_points, proc_dir + 'trees_forest.geojson', 'utf-8', QgsCoordinateReferenceSystem(crs_from), 'GeoJson')



#-------------------------------------------------------------------------
# Fahrzeuge auf Parkstreifen mit Farben und Fahrzeugmodellen generieren
#-------------------------------------------------------------------------
if proc_cars:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Fahrzeugmodelle auf Parkstreifen generieren...')
    layer_parking = QgsVectorLayer(data_dir + 'parking/street_parking_lines.geojson|geometrytype=LineString', 'Parkstreifen', 'ogr')

    #layer aus historischen Gründen drehen (das war die ursprüngliche Linienrichtung zu Beginn - TODO drauf verzichten und Formeln anpassen)
    #layer_parking = processing.run('native:reverselinedirection', {'INPUT' : layer_parking, 'OUTPUT': 'memory:'})['OUTPUT']

    print(time.strftime('%H:%M:%S', time.localtime()), '   Erzeuge und verschiebe Punktdaten...')
    #Parkstreifen in einzelne Punkte unterteilen und diese zum Standort der realen Fahrzeugmitte versetzen
    layer_parking = processing.run('native:pointsalonglines', {'INPUT' : layer_parking,
        'DISTANCE' : QgsProperty.fromExpression('if("vehicle_designated" = \'bus\', 12, if("source:capacity" = \'estimated\', if("orientation" = \'diagonal\', 3.1, if("orientation" = \'perpendicular\', 2.5, 5.2)), if("capacity" = 1, $length, if($length < if("orientation" = \'diagonal\', 3.1 * "capacity", if("orientation" = \'perpendicular\', 2.5 * "capacity", (5.2 * "capacity") - 0.8)), ($length + (if("orientation" = \'parallel\', 0.8, if("orientation" = \'perpendicular\', 0.5, 0))) - (2 * if("orientation" = \'diagonal\', 1.55, if("orientation" = \'perpendicular\', 1.25, 2.6)))) / ("capacity" - 1), ($length - (2 * if("orientation" = \'diagonal\', 1.55, if("orientation" = \'perpendicular\', 1.25, 2.6)))) / ("capacity" - 1)))))'),
        'START_OFFSET' : QgsProperty.fromExpression('if("vehicle_designated" = \'bus\', 6 + (($length - (12 * "capacity")) / 2), if("source:capacity" = \'estimated\', if("orientation" = \'diagonal\', ($length - (3.1*("capacity" - 1))) / 2, if("orientation" = \'perpendicular\', ($length - (2.5*("capacity" - 1))) / 2, ($length - (5.2*("capacity" - 1))) / 2)), if("capacity" < 2, $length / 2, if("orientation" = \'diagonal\', 1.55, if("orientation" = \'perpendicular\', if($length < if("orientation" = \'diagonal\', 3.1 * "capacity", if("orientation" = \'perpendicular\', 2.5 * "capacity", (5.2 * "capacity") - 0.8)), 0.9, 1.25), if($length < if("orientation" = \'diagonal\', 3.1 * "capacity", if("orientation" = \'perpendicular\', 2.5 * "capacity", (5.2 * "capacity") - 0.8)), 2.2, 2.6))))))'),
        'OUTPUT' : data_dir + 'parking/street_parking_points.geojson' })['OUTPUT']
    processing.run('native:translategeometry', {'INPUT' : layer_parking,
        #Formula: -cos/sin "angle" * distance to kerb, inverted for on_kerb/shoulder parking, + offset if diagonal parking (inverted, if diagonal parking direction is inverted, esp. in oneway streets on the left side – 1.2 is a good fitting default in most situations, in reality it's depending on the exact parking angle)
        'DELTA_X' : QgsProperty.fromExpression('-cos(("angle") * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)) * if("parking" = \'on_kerb\' or "parking" = \'shoulder\', -1, if("parking" = \'lane\' or "parking" = \'street_side\' or "parking" IS NULL, 1, 0)) + (if("orientation" = \'diagonal\', sin(("angle") * (pi() / 180)) * if("highway:oneway" = \'yes\' and "side" = \'left\', 1.2, -1.2), 0)) * if("parking" = \'on_kerb\' or "parking" = \'shoulder\', -1, if("parking" = \'lane\' or "parking" = \'street_side\' or "parking" IS NULL, 1, 0))'),
        'DELTA_Y' : QgsProperty.fromExpression('sin(("angle") * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)) * if("parking" = \'on_kerb\' or "parking" = \'shoulder\', -1, if("parking" = \'lane\' or "parking" = \'street_side\' or "parking" IS NULL, 1, 0)) + (if("orientation" = \'diagonal\', cos(("angle") * (pi() / 180)) * if("highway:oneway" = \'yes\' and "side" = \'left\', 1.2, -1.2), 0)) * if("parking" = \'on_kerb\' or "parking" = \'shoulder\', -1, if("parking" = \'lane\' or "parking" = \'street_side\' or "parking" IS NULL, 1, 0))'),
        'OUTPUT' : proc_dir + 'street_parking_points_processed.geojson' })

    #unbearbeitete Kopie im parking-Ordner speichern
    processing.run('native:translategeometry', {'INPUT' : layer_parking,
        'DELTA_X' : QgsProperty.fromExpression('-cos(("angle") * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)) * if("parking" = \'on_kerb\' or "parking" = \'shoulder\', -1, if("parking" = \'lane\' or "parking" = \'street_side\' or "parking" IS NULL, 1, 0)) + (if("orientation" = \'diagonal\', sin(("angle") * (pi() / 180)) * if("highway:oneway" = \'yes\' and "side" = \'left\', 1.2, -1.2), 0)) * if("parking" = \'on_kerb\' or "parking" = \'shoulder\', -1, if("parking" = \'lane\' or "parking" = \'street_side\' or "parking" IS NULL, 1, 0))'),
        'DELTA_Y' : QgsProperty.fromExpression('sin(("angle") * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)) * if("parking" = \'on_kerb\' or "parking" = \'shoulder\', -1, if("parking" = \'lane\' or "parking" = \'street_side\' or "parking" IS NULL, 1, 0)) + (if("orientation" = \'diagonal\', cos(("angle") * (pi() / 180)) * if("highway:oneway" = \'yes\' and "side" = \'left\', 1.2, -1.2), 0)) * if("parking" = \'on_kerb\' or "parking" = \'shoulder\', -1, if("parking" = \'lane\' or "parking" = \'street_side\' or "parking" IS NULL, 1, 0))'),
        'OUTPUT' : data_dir + 'parking/street_parking_points_translated.geojson' })

    layer_cars = QgsVectorLayer(proc_dir + 'street_parking_points_processed.geojson|geometrytype=Point', 'Fahrzeuge', 'ogr')
    layer_cars = clearAttributes(layer_cars, ['orientation', 'markings', 'markings:type', 'width', 'condition_class', 'vehicle_designated', 'highway:oneway', 'side', 'angle'])
    QgsProject.instance().addMapLayer(layer_cars, False)
 
    #Neue Attribute für Fahrzeugmodell und Farbe anlegen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Generiere Fahrzeugmodelleigenschaften...')
    layer_cars.startEditing()
    if layer_cars.fields().indexOf('@modell') == -1:
        layer_cars.dataProvider().addAttributes([QgsField('@modell', QVariant.String)])
    if layer_cars.fields().indexOf('@colour') == -1:
        layer_cars.dataProvider().addAttributes([QgsField('@colour', QVariant.String)])
    layer_cars.updateFields()
    id_modell = layer_cars.fields().indexOf('@modell')
    id_colour = layer_cars.fields().indexOf('@colour')

    #Fahrzeuge durchgehen und Farbe/Modell zufällig festlegen oder auf Sonderfahrzeuge (Polizei/Taxi) prüfen
    colours = ['black', 'dark_blue', 'gray', 'green', 'red', 'silver', 'white', 'yellow']
    for feature in layer_cars.getFeatures():
        modell = NULL
        colour = NULL
        vehicles = feature.attribute('vehicle_designated')
        if vehicles == 'emergency':
            modell = 'car-police'
            colour = 'silver'
        elif vehicles == 'taxi':
            modell = 'car-taxi'
            colour = 'yellow'
        elif vehicles == 'motorcar':
            modell = 'car-simple0' + str(random.randint(1, 2))
            colour = colours[random.randint(0, 7)]
        elif vehicles == 'hgv':
            # Einzelne Transporter auf hgv-Parkstreifen durch Sattelzüge ersetzen
            layer_cars.removeSelection()
            layer_cars.select(feature.id())
            # im Umkreis von 8 Metern (halbe Sattelschlepper-Länge) nach Nachbarfahrzeugen suchen
            hgv_buffer = processing.run('native:buffer', { 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_cars.id(), selectedFeaturesOnly=True), 'DISTANCE' : 8, 'OUTPUT': 'memory:'})['OUTPUT']
            processing.run('native:selectbylocation', {'INPUT' : layer_cars, 'INTERSECT' : hgv_buffer, 'PREDICATE' : [6]})
            # nur zu Sattelschlepper umwandeln, wenn zwei Nachbarn (Annahme: davor und dahinter)
            if layer_cars.selectedFeatureCount() == 3:
                # nur zu Sattelschlepper umwandeln, wenn nicht in Kurve
                min_angle = NULL
                max_angle = NULL
                for neighbour_hgv in layer_cars.selectedFeatures():
                    angle = neighbour_hgv.attribute('angle')
                    if min_angle == NULL or angle < min_angle:
                        min_angle = angle
                    if max_angle == NULL or angle > max_angle:
                        max_angle = angle
                if max_angle - min_angle < 5:
                    # nur ein paar einzelne Sattelschlepper
                    if random.random() > 0.7:
                        modell = 'hgv-simple01'
                        colour = colours[random.randint(0, 7)]
                        # Ausgewählte Nachbarfahrzeuge löschen
                        layer_cars.deselect(feature.id())
                        layer_cars.deleteSelectedFeatures()

            # Andere Fahrzeuge als Kleinlaster darstellen
            if modell == NULL:
                modell = 'car-simple03'
                colour = colours[random.randint(0, 7)]
        elif vehicles == 'bus':
            modell = 'bus-simple01'
            colour = colours[random.randint(0, 7)]
        else:
            #In 10% der Fälle Kleinlaster, sonst Pkw
            if random.random() > 0.1:
                modell = 'car-simple0' + str(random.randint(1, 2))
            else:
                modell = 'car-simple03'
            colour = colours[random.randint(0, 7)]
        layer_cars.changeAttributeValue(feature.id(), id_modell, modell)
        layer_cars.changeAttributeValue(feature.id(), id_colour, colour)
    layer_cars.commitChanges()
    qgis.core.QgsVectorFileWriter.writeAsVectorFormat(layer_cars, proc_dir + 'street_parking_points_processed.geojson', 'utf-8', QgsCoordinateReferenceSystem(crs_from), 'GeoJson')



#-------------------------------------------------------------------------------
# bessere Segmente zur Beschriftung von Straßennamen und Gewässern generieren
#-------------------------------------------------------------------------------
if proc_labels:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Erzeuge Segmente für Straßen- und Gewässernamen...')
    if not layer_raw_highway_ways:
        layer_raw_highway_ways = QgsVectorLayer(data_dir + 'highway.geojson|geometrytype=LineString', 'highway (raw)', 'ogr')
    if not layer_raw_path_ways:
        layer_raw_path_ways = QgsVectorLayer(data_dir + 'path.geojson|geometrytype=LineString', 'path (raw)', 'ogr')
    if not layer_raw_waterway_ways:
        layer_raw_waterway_ways = QgsVectorLayer(data_dir + 'waterway.geojson|geometrytype=LineString', 'waterway (raw)', 'ogr')
    layer_bridges = QgsVectorLayer(data_dir + 'bridge.geojson|geometrytype=Polygon', 'bridge (raw)', 'ogr')

    streetname_attributes = ['name', 'highway', 'dual_carriageway', 'bicycle_road']
    waterway_attributes = ['name', 'waterway']

    #für Straßennamen:
    #nur Straßennetz verarbeiten
    layer_streets = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_highway_ways, 'EXPRESSION' : '"highway" IS NOT \'platform\' and NOT("highway" like \'%_link\') and "highway" IS NOT NULL', 'OUTPUT': 'memory:'})['OUTPUT']

    #Straßen und Wege nach den Merkmalen Name, Klassifikation und Zweirichtungs-Fahrbahn vereinigen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Straßen nach gemeinsamen Merkmalen vereinigen...')
    layer_streets = processing.run('native:dissolve', { 'FIELD' : streetname_attributes, 'INPUT' : layer_streets, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_ways = processing.run('native:dissolve', { 'FIELD' : streetname_attributes, 'INPUT' : layer_raw_path_ways, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_streetnames = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_streets, layer_ways], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_streetnames = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_streetnames, 'EXPRESSION' : '"name" IS NOT NULL', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_streetnames = processing.run('native:reprojectlayer', { 'INPUT' : layer_streetnames, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']

    #Zweirichtungs-Fahrbahnen herauslösen
    layer_streetnames_dual = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_streetnames, 'EXPRESSION' : '"dual_carriageway" IS \'yes\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_streetnames_not_dual = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_streetnames, 'EXPRESSION' : '"dual_carriageway" IS NOT \'yes\'', 'OUTPUT': 'memory:'})['OUTPUT']

    print(time.strftime('%H:%M:%S', time.localtime()), '   Zweirichtungs-Fahrbahnen vereinfachen...')
    #Allen Zweirichtungs-Fahrbahnen und ihren Parallel-Segmenten eine neue eindeutige ID geben
    layer_streetnames_dual = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_streetnames_dual, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_streetnames_dual.startEditing()
    for dual_street in layer_streetnames_dual.getFeatures():
        layer_streetnames_dual.changeAttributeValue(dual_street.id(), layer_streetnames_dual.fields().indexOf('id'), dual_street.id())
    layer_streetnames_dual.commitChanges()

    #Zweirichtungs-Fahrbahnen an den Stellen trennen, an denen sie sich aufteilen (=Schnittpunkt mit Einrichtungs-Fahrbahnen gleichen Namens)
    merge_list = []
    QgsProject.instance().addMapLayer(layer_streetnames_dual, False)
    QgsProject.instance().addMapLayer(layer_streetnames_not_dual, False)
    for dual_street in layer_streetnames_dual.getFeatures():
        layer_streetnames_dual.removeSelection()
        segment_id = dual_street.id()
        layer_streetnames_dual.select(segment_id)
        name = dual_street.attribute('name')
        processing.run('qgis:selectbyattribute', {'INPUT' : layer_streetnames_not_dual, 'FIELD' : 'name', 'VALUE' : name })
        layer_streetnames_dual_segment = processing.run('native:splitwithlines', { 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_streetnames_dual.id(), selectedFeaturesOnly=True), 'LINES' : QgsProcessingFeatureSourceDefinition(layer_streetnames_not_dual.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']
        merge_list.append(layer_streetnames_dual_segment)

    layer_streetnames_dual = processing.run('native:mergevectorlayers', { 'LAYERS' : merge_list, 'OUTPUT': 'memory:'})['OUTPUT']

    #eins der Parallel-Segmente entfernen - Straßenname soll nur auf einer der beiden Seiten angezeigt werden
    #dafür 15 Meter Puffer um Mittelpunkt ziehen und Objekte gleichen Namens in der Umgebung löschen
    layer_streetnames_dual.startEditing()
    continue_list = []
    for dual_street in layer_streetnames_dual.getFeatures():
        if dual_street.id() in continue_list:
            continue
        dual_street_geom = dual_street.geometry()
        dist = dual_street_geom.length() / 2
        center_point = dual_street_geom.interpolate(dist)
        buffer_geom = center_point.buffer(15, 2)
        #Neuen Layer für Puffer erzeugen
        layer_buffer = QgsVectorLayer("Polygon?crs=" + crs_to, "dual_carriageway_buffer", "memory")
        provider = layer_buffer.dataProvider()
        layer_buffer.updateFields() 
        buffer_feat = QgsFeature()
        buffer_feat.setGeometry(buffer_geom)
        provider.addFeature(buffer_feat)
        layer_buffer.updateExtents()

        #Schwester-Segmente in der Umgebung löschen
        processing.run('native:selectbylocation', {'INPUT' : layer_streetnames_dual, 'INTERSECT' : layer_buffer, 'METHOD' : 0, 'PREDICATE' : [0]})
        layer_streetnames_dual.deselect(dual_street.id())
        for feat in layer_streetnames_dual.selectedFeatures():
            if feat.attribute('name') == dual_street.attribute('name'):
                #bei kurzen Wegstücken verhindern, dass Vor- oder Nachfolger-Segmente mit gelöscht werden
                if dist <= 15 and feat.attribute('id') != dual_street.attribute('id'):
                    continue
                continue_list.append(feat.id())
                layer_streetnames_dual.deleteFeature(feat.id())

    layer_streetnames_dual.commitChanges()

    #Alle Teile in einem Layer vereinigen und bereinigen
    layer_streetnames = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_streetnames_dual, layer_streetnames_not_dual], 'OUTPUT': 'memory:'})['OUTPUT']
    #dual_carriageway bei Vereinigung angrenzender Segmente ignorieren, um häufige Zerstückelung z.B. an Mittelinseln zu vermeiden
    if 'dual_carriageway' in streetname_attributes:
        streetname_attributes.remove('dual_carriageway')
    layer_streetnames = processing.run('native:dissolve', { 'FIELD' : streetname_attributes, 'INPUT' : layer_streetnames, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_streetnames = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_streetnames, 'OUTPUT': 'memory:'})['OUTPUT']

    #Nebenstraßen an Hauptstraßen (primary/secondary) teilen
    layer_main_streets = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_streetnames, 'EXPRESSION' : '"highway" = \'primary\' or "highway" = \'secondary\'', 'OUTPUT': 'memory:'})['OUTPUT']
    QgsProject.instance().addMapLayer(layer_streetnames, False)
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_streetnames, 'EXPRESSION' : '"highway" IS NOT \'primary\' and "highway" IS NOT \'secondary\'' })
    layer_streetnames = processing.run('native:splitwithlines', { 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_streetnames.id(), selectedFeaturesOnly=True), 'LINES' : layer_main_streets, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_streetnames = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_streetnames, layer_main_streets], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_streetnames = clearAttributes(layer_streetnames, streetname_attributes)
    qgis.core.QgsVectorFileWriter.writeAsVectorFormat(layer_streetnames, proc_dir + 'street_names.geojson', 'utf-8', QgsCoordinateReferenceSystem(crs_from), 'GeoJson')

    #für Gewässernamen:
    print(time.strftime('%H:%M:%S', time.localtime()), '   Gewässerlinien an Brücken segmentieren...')
    #Tunnel ausschließen und Gewässerlinien nach Namen auflösen
    layer_waterways = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_waterway_ways, 'EXPRESSION' : '"tunnel" IS NULL', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_waterways = processing.run('native:reprojectlayer', { 'INPUT' : layer_waterways, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_waterways = processing.run('native:dissolve', { 'FIELD' : waterway_attributes, 'INPUT' : layer_waterways, 'OUTPUT': 'memory:'})['OUTPUT']
    #Beschriftungs-Punktekette im Abstand von 1200 Metern erzeugen (= Zieldistanz wiederholender Beschriftungen)
    layer_waterways_points = processing.run('native:pointsalonglines', {'INPUT' : layer_waterways, 'DISTANCE' : 1200, 'START_OFFSET' : 600, 'END_OFFSET' : 600, 'OUTPUT': 'memory:'})['OUTPUT']
    #Gewässerlinien an Brücken auftrennen, um Beschriftung idealerweise zwischen Brücken zu platzieren
    layer_waterways = processing.run('native:difference', {'INPUT' : layer_waterways, 'OVERLAY' : layer_bridges, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_waterways = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_waterways, 'OUTPUT': 'memory:'})['OUTPUT']
    #Beschriftungs-Punkte an nahe Gewässerlinien versetzen
    layer_waterways_points = processing.run('native:snapgeometries', { 'BEHAVIOR' : 1, 'INPUT' : layer_waterways_points, 'REFERENCE_LAYER' : layer_waterways, 'TOLERANCE' : 30, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_waterways_points = processing.run('native:buffer', { 'INPUT' : layer_waterways_points, 'DISTANCE' : 0.1, 'OUTPUT': 'memory:'})['OUTPUT']
    #nur die Gewässersegmente behalten, die einen Punkt der Beschriftungs-Punktekette schneiden
    layer_waterways = clearAttributes(layer_waterways, waterway_attributes)
    layer_waterways = processing.run('native:extractbylocation', { 'INPUT' : layer_waterways, 'INTERSECT' : layer_waterways_points, 'PREDICATE' : [0], 'OUTPUT' : proc_dir + 'waterway_names.geojson' })



#-----------------------------------------------------------------------------------------------------------
# Erzeugt einen Layer mit Kiezflächen, denen Zahlen zu vorhandenen Stellplätzen aller Art zugeordnet sind
#-----------------------------------------------------------------------------------------------------------
if proc_parking_areas:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Ermittle Stellplätze in einzelnen Kiezen...')

    print(time.strftime('%H:%M:%S', time.localtime()), '...Lade Daten...')
    layer_parking_areas = QgsVectorLayer(parking_dir + 'parking_area.geojson|geometrytype=Polygon', 'parking areas', 'ogr')
    layer_parking_areas = processing.run('native:reprojectlayer', { 'INPUT' : layer_parking_areas, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking_lanes_points = QgsVectorLayer(data_dir + 'parking/parking_way_points_translated.geojson|geometrytype=Point', 'parking street points', 'ogr')
    layer_kieze = QgsVectorLayer(parking_dir + 'kieze.geojson|geometrytype=Polygon', 'kieze', 'ogr')

    #Parkplätze für Kund:innen oder Mitarbeiter:innen sowie ungenutzte Parkplätze herausfiltern
    layer_parking_areas = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_parking_areas, 'EXPRESSION' : '"status" IS NOT \'disused\' and "access" IS NOT \'customers\' and "access" IS NOT \'employees\' and "access" IS NOT \'no\' and "access" IS NOT \'police\'', 'OUTPUT': 'memory:'})['OUTPUT']

    #Punkte in Parkplätzen entsprechend ihrer Kapazität erzeugen
    print(time.strftime('%H:%M:%S', time.localtime()), '...Erzeuge Einzelpunkte...')
    layer_parking_area_points = processing.run('native:randompointsinpolygons', { 'INCLUDE_POLYGON_ATTRIBUTES' : True, 'INPUT' : layer_parking_areas, 'MAX_TRIES_PER_POINT' : 10, 'MIN_DISTANCE' : 0, 'MIN_DISTANCE_GLOBAL' : 0, 'POINTS_NUMBER' : QgsProperty.fromExpression('"capacity"'), 'SEED' : None, 'OUTPUT': 'memory:'})['OUTPUT']

    QgsProject.instance().addMapLayer(layer_parking_area_points, False)

    #Einzelne Stellplätze zählen
    print(time.strftime('%H:%M:%S', time.localtime()), '...Zähle Stellplätze für Straßenparken...')
    #1) Straßenparken - sowohl separat gemappte Flächen als auch aus dem Parkstreifenlayer ermitteln
    layer_parking_kieze = processing.run('native:countpointsinpolygon', { 'FIELD' : 'parking_street-lanes-lines', 'POINTS' : layer_parking_lanes_points, 'POLYGONS' : layer_kieze, 'OUTPUT': 'memory:'})['OUTPUT']
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_parking_area_points, 'EXPRESSION' : '"parking" = \'lane\' or "parking" = \'street_side\''})
    layer_parking_kieze = processing.run('native:countpointsinpolygon', { 'FIELD' : 'parking_street-lanes-areas', 'POINTS' : QgsProcessingFeatureSourceDefinition(layer_parking_area_points.id(), selectedFeaturesOnly=True), 'POLYGONS' : layer_parking_kieze, 'OUTPUT': 'memory:'})['OUTPUT']
    #2) Park-/Stellplätze
    print(time.strftime('%H:%M:%S', time.localtime()), '...Zähle Stellplätze für Park-/Stellplätze...')
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_parking_area_points, 'EXPRESSION' : '"parking" = \'surface\' or "parking" = \'level\' or "parking" = \'rooftop\''})
    layer_parking_kieze = processing.run('native:countpointsinpolygon', { 'FIELD' : 'parking_surface', 'POINTS' : QgsProcessingFeatureSourceDefinition(layer_parking_area_points.id(), selectedFeaturesOnly=True), 'POLYGONS' : layer_parking_kieze, 'OUTPUT': 'memory:'})['OUTPUT']
    #3) Tiefgaragen
    print(time.strftime('%H:%M:%S', time.localtime()), '...Zähle Stellplätze für Tiefgaragen...')
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_parking_area_points, 'EXPRESSION' : '"parking" = \'underground\''})
    layer_parking_kieze = processing.run('native:countpointsinpolygon', { 'FIELD' : 'parking_underground', 'POINTS' : QgsProcessingFeatureSourceDefinition(layer_parking_area_points.id(), selectedFeaturesOnly=True), 'POLYGONS' : layer_parking_kieze, 'OUTPUT': 'memory:'})['OUTPUT']
    #4) Garagen/Carports
    print(time.strftime('%H:%M:%S', time.localtime()), '...Zähle Stellplätze für Garagen/Carports...')
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_parking_area_points, 'EXPRESSION' : '"parking" = \'carport\' or "parking" = \'garage\' or "parking" = \'garages\''})
    layer_parking_kieze = processing.run('native:countpointsinpolygon', { 'FIELD' : 'parking_garage_carports', 'POINTS' : QgsProcessingFeatureSourceDefinition(layer_parking_area_points.id(), selectedFeaturesOnly=True), 'POLYGONS' : layer_parking_kieze, 'OUTPUT': 'memory:'})['OUTPUT']
    #5) Parkhäuser
    print(time.strftime('%H:%M:%S', time.localtime()), '...Zähle Stellplätze für Parkhäuser...')
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_parking_area_points, 'EXPRESSION' : '"parking" = \'multi-storey\''})
    layer_parking_kieze = processing.run('native:countpointsinpolygon', { 'FIELD' : 'parking_multi-storey', 'POINTS' : QgsProcessingFeatureSourceDefinition(layer_parking_area_points.id(), selectedFeaturesOnly=True), 'POLYGONS' : layer_parking_kieze, 'OUTPUT' : parking_dir + 'parking_kieze.geojson' })



#-------------------------------------------------------------------------------------
# Filtert separat gemappte geschützte Radspuren und richtet sie an Straßenlinie aus
#-------------------------------------------------------------------------------------
if proc_protected_bl:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Richte geschützte Radstreifen aus...')
    if not layer_raw_highway_ways:
        layer_raw_highway_ways = QgsVectorLayer(data_dir + 'highway.geojson|geometrytype=LineString', 'highway (raw)', 'ogr')
    if not layer_raw_path_ways:
        layer_raw_path_ways = QgsVectorLayer(data_dir + 'path.geojson|geometrytype=LineString', 'path (raw)', 'ogr')

    #geschützte Radstreifen herausfiltern
    layer_pbl = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_path_ways, 'EXPRESSION' : '("cycleway" = \'lane\' or "cycleway:type" = \'lane\') and ("separation" ~ \'bollard\' or "separation:left" ~ \'bollard\' or "separation:both" ~ \'bollard\' or "separation" ~ \'flex_post\' or "separation:left" ~ \'flex_post\' or "separation:both" ~ \'flex_post\' or "separation" ~ \'vertical_panel\' or "separation:left" ~ \'vertical_panel\' or "separation:both" ~ \'vertical_panel\' or "separation" ~ \'separation_kerb\' or "separation:left" ~ \'separation_kerb\' or "separation:both" ~ \'separation_kerb\'  or "separation" ~ \'bump\' or "separation:left" ~ \'bump\' or "separation:both" ~ \'bump\' or "separation" ~ \'planter\' or "separation:left" ~ \'planter\' or "separation:both" ~ \'planter\' or "separation" ~ \'railing\' or "separation:left" ~ \'railing\' or "separation:both" ~ \'railing\'  or "separation" ~ \'fence\' or "separation:left" ~ \'fence\' or "separation:both" ~ \'fence\' or "separation" ~ \'jersey_barrier\' or "separation:left" ~ \'jersey_barrier\' or "separation:both" ~ \'jersey_barrier\' or "separation" ~ \'guard_rail\' or "separation:left" ~ \'guard_rail\' or "separation:both" ~ \'guard_rail\' or "separation" ~ \'structure\' or "separation:left" ~ \'structure\' or "separation:both" ~ \'structure\')', 'OUTPUT': 'memory:'})['OUTPUT']
    #Straßen mit parallel gemappten Radwegen herausfiltern
    layer_roads = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_highway_ways, 'EXPRESSION' : '"cycleway"=\'separate\' or "cycleway:both"=\'separate\' or "cycleway:right"=\'separate\' or "cycleway:left"=\'separate\'', 'OUTPUT': 'memory:'})['OUTPUT']

    #in metrisches KBS reprojizieren
    layer_pbl = processing.run('native:reprojectlayer', { 'INPUT' : layer_pbl, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_roads = processing.run('native:reprojectlayer', { 'INPUT' : layer_roads, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']

    #geschützte Radstreifen an nageliegende Straßensegmente anpassen
    layer_pbl_snapped = processing.run('native:snapgeometries', { 'BEHAVIOR' : 1, 'INPUT' : layer_pbl, 'REFERENCE_LAYER' : layer_roads, 'TOLERANCE' : 20, 'OUTPUT' : proc_dir + 'pbl_snapped.geojson' })



print(time.strftime('%H:%M:%S', time.localtime()), 'Abgeschlossen.')