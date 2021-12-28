#---------------------------------------------------------------------------#
#   Straßenraumkarte / micromap post processing script                      #
#   --------------------------------------------------                      #
#   OSM data post-processing for QGIS/PyGIS for rendering the micromap at   #
#   https://supaplexosm.github.io/strassenraumkarte-neukoelln/?map=micromap #
#                                                                           #
#   > version/date: 2021-12-28                                              #
#---------------------------------------------------------------------------#

import os, processing, math, random, time

#-------------------------------------------------#
#   V a r i a b l e s   a n d   S e t t i n g s   #
#-------------------------------------------------#

#processing steps - set "1" for the needed step(s) befor running the script:
proc_crossings      = 0     # < # Fahrbahnbezogene Eigenschaften von Querungsstellen ermitteln und übertragen
proc_cr_markings    = 0     #   # Querungsstellen mit randseitigen Markierungen am Bordstein ausrichten
proc_cr_lines       = 0     # < # Linien markierter Gehweg-Querungsstellen erzeugen
proc_cr_tactile_pav = 0     # < # Taktile Bodenleitsysteme entlang von Bordsteinen und Wegen generieren
proc_lane_markings  = 1     # < # Straßenmarkierungen erzeugen
proc_highway_backup = 0     # < # Straßenlinien als Backup in fahrbahnfreien Bereichen erzeugen
proc_service        = 0     #   # service-Wege mit gleichen Eigenschaften zusammenführen, um Lücken zu vermeiden
proc_oneways        = 0     #   # Für Einbahnstraßen separate Linien zur Markierung erzeugen
proc_traffic_calming= 0     #   # Straßeneigenschaften auf Verkehrsberuhigungsmaßnahmen übertragen
proc_cycleways      = 0     #   # Radwege nachbearbeiten
proc_path_areas     = 0     #   # Vereinigt aneinander angrenzende Wegeflächen und erzeugt deren Outlines
proc_building_parts = 0     # < # Gebäudeteile auf Stockwerksunterschiede auflösen, Gebäudegrundrisse / schwebende Gebäudeteile verarbeiten
proc_housenumbers   = 0     #   # Hausnummern gleichmäßig zum Gebäudeumriss ausrichten
proc_water_body     = 0     # < # Gewässerkörper zu einem Einzelpolygon vereinigen
proc_landcover      = 0     #   # Bereiche mit "landcover=*" in Polygone umwandeln (werden nur als Linien erkannt)
proc_playground     = 0     #   # Gras-Flächen zur besseren Darstellung aus playground-Polygonen ausstanzen
proc_orient_man_made= 0     # < # Richtet bestimmte Straßenmöbel zur nächstgelegenen Straße hin aus (Straßenlaternen, Schaltkästen)
proc_trees          = 0     # < # Baumkronendurchmesser und Stammumfang abschätzen
proc_forests        = 0     #   # Waldbäume über ein hexagonales Gitter interpolieren
proc_cars           = 0     #   # Fahrzeuge auf Parkstreifen mit Farben und Fahrzeugmodellen generieren
proc_labels         = 0     #   # bessere Segmente zur Beschriftung von Straßennamen und Gewässern generieren

#project directory
main_dir = '/your/directory/' #<<<<<<<< fill in your project directory here!
data_dir = main_dir + 'layer/geojson/'
proc_dir = data_dir + 'layer/geojson/post_processed/'

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
'width:lanes:backward',
'width:effective',
'lane_markings',
'lane_markings:junction',
'lane_markings:crossing',
'overtaking',
'placement',
'placement:forward',
'placement:backward',
'placement:start',
'placement:forward:start',
'placement:backward:start',
'placement:end',
'placement:forward:end',
'placement:backward:end',
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
'cycleway:left:surface:colour'
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

    print(time.strftime('%H:%M:%S', time.localtime()), '   Bearbeite Daten: Datensatz bereinigen...')
    layer_street = clearAttributes(layer_street, street_key_list)

    #Attribute für crossings bereinigen
    attr_list = [
        'id',
        'highway',
        'crossing',
        'crossing_ref',
        'crossing:island',
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
                if unit in width:
                    width = width[:len(width) - len(unit)]
                    if 'cm' in unit:
                        width = width / 100

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
    layer.startEditing()
    attr_count = len(layer.attributeList())
    for id in range(attr_count - 1, 0, -1):
        if not layer.attributeDisplayName(id) in attributes:
            layer.deleteAttribute(id)
    layer.updateFields()
    layer.commitChanges()
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
#-------------------------------------------------------------------------------
    #Winkel am Zweigpunkt des dual carriageways ermitteln
    angle_dual = math.degrees(geom.angleAtVertex(vertex))
    #Winkel des eigentlichen Straßenverlaufs am selben Punkt der gemeinsamen Einrichtungs-Fahrbahn ermitteln
    layer_lanes.removeSelection()
    lane_id = lane_dual.id()
    layer_lanes.select(lane_id)
    width_lanes_dual = lanes_dict['width_lanes'][lane_dual.attribute('id')]
    #...dafür zunächst anschließendes (= berührendes) Einrichtungswegstück selektieren
    processing.run('native:selectbylocation', {'INPUT' : layer_lanes_single_carriageway, 'INTERSECT' : QgsProcessingFeatureSourceDefinition(layer_lanes.id(), selectedFeaturesOnly=True), 'METHOD' : 0, 'PREDICATE' : [4]})
    #...und dann Winkel dieses Wegstücks am selben Punkt ermitteln
    dual_carriageway_opposite_direction = NULL
    for lane_single in layer_lanes_single_carriageway.selectedFeatures():
        vertex_count_single = len(lane_single.geometry().asPolyline())
        geom_single = lane_single.geometry()
        start_vertex_single_x = geom_single.vertexAt(0).x()
        start_vertex_single_y = geom_single.vertexAt(0).y()
        if start_vertex_single_x == vertex_x and start_vertex_single_y == vertex_y:
            angle = math.degrees(geom_single.angleAtVertex(0))
            width_lanes = lanes_dict['width_lanes'][lane_single.attribute('id')]
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
                width_lanes = lanes_dict['width_lanes'][lane_single.attribute('id')]
                placement_single = lane_single.attribute('placement_abs')
                lanes_single = int(lane_single.attribute('lanes'))
                if vertex == 0:
                    dual_carriageway_opposite_direction = 0
                else:
                    dual_carriageway_opposite_direction = 1

    #Distanz der Abweichung ermitteln
    distance = 0
    placement_pos_single = placement_single[0:len(placement_single) - 1]
    placement_lane_single = int(placement_single[len(placement_single)-1:len(placement_single)])
    placement_dual = lane.attribute('placement_abs')
    placement_pos_dual = placement_dual[0:len(placement_dual) - 1]
    placement_lane_dual = int(placement_dual[len(placement_dual)-1:len(placement_dual)])
    lanes_dual = int(lane.attribute('lanes'))
    lanes_diff = lanes_single - lanes_dual

    if dual_carriageway_opposite_direction == 1:
        angle += 180
        placement_lane_dual_reverse = abs(placement_lane_dual - lanes_dual - 1)
        if placement_pos_dual == 'left_of:':
            placement_pos_dual_reverse = 'right_of:'
        elif placement_pos_dual == 'right_of:':
            placement_pos_dual_reverse = 'left_of:'
        else:
            placement_pos_dual_reverse = placement_pos_dual
        for l in range(1, len(width_lanes) + 1):
            if l >= placement_lane_dual_reverse and l < placement_lane_single:
                distance += float(width_lanes[l - 1]) / 2 + float(width_lanes[l]) / 2
        if placement_pos_single == 'left_of:':
            distance -= float(width_lanes[placement_lane_single - 1]) / 2
        if placement_pos_single == 'right_of:':
            distance += float(width_lanes[placement_lane_single - 1]) / 2
        if placement_pos_dual_reverse == 'left_of:':
            distance += float(width_lanes[placement_lane_dual_reverse - 1]) / 2
        if placement_pos_dual_reverse == 'right_of:':
            distance -= float(width_lanes[placement_lane_dual_reverse - 1]) / 2

    if dual_carriageway_opposite_direction == 0:
        for l in range(1, len(width_lanes) + 1):
            if l > placement_lane_single and l <= placement_lane_dual + lanes_diff:
                distance += float(width_lanes[l - 1])

        if placement_pos_single == 'left_of:':
            distance += float(width_lanes[placement_lane_single - 1]) / 2
        if placement_pos_single == 'right_of:':
            distance -= float(width_lanes[placement_lane_single - 1]) / 2
        if placement_pos_dual == 'left_of:':
            distance -= float(width_lanes[placement_lane_dual + lanes_diff - 1]) / 2
        if placement_pos_dual == 'right_of:':
            distance += float(width_lanes[placement_lane_dual + lanes_diff - 1]) / 2

    distance += (float(width_lanes[lanes_diff]) - float(width_lanes_dual[0])) / 2

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
        placement = placement_backward
        l_b = int(placement_backward[-1])
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

    l = int(placement[-1])
    l += l_f
    if l_b:
        l = l_b

    l += l_extra

    placement = placement[0:-1] + str(l)
    return(placement)



#--------------------------------
#      S c r i p t   S t a r t
#--------------------------------
print(time.strftime('%H:%M:%S', time.localtime()), 'Starte Post-processing:')

#-------------------------------------------------------------------------------
# Fahrbahnbezogene Eigenschaften von Querungsstellen ermitteln und übertragen
#-------------------------------------------------------------------------------
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
    layers = prepareLayers(layer_raw_highway_ways, layer_raw_path_ways, layer_raw_highway_points)
    if layers:
        layer_street = layers[0]
        layer_path = layers[1]
        layer_crossing = layers[2]

        #Straßen-Schnittpunkteigenschaften erheben
        layer_intersections = processing.run('native:lineintersections', {'INPUT': layer_street, 'INTERSECT': layer_path, 'INPUT_FIELDS' : ['highway'], 'INTERSECT_FIELDS_PREFIX': 'crossing:', 'OUTPUT': 'memory:'})['OUTPUT']

        #Winkel an Übergängen berechnen
        layer_vertices = processing.run('native:extractvertices', {'INPUT': layer_street, 'OUTPUT': 'memory:'})['OUTPUT']

        print(time.strftime('%H:%M:%S', time.localtime()), '   Eigenschaften auf Querungsstellen übertragen...')
        #Straßenbreite
        layer_crossing = processing.run('native:joinattributesbylocation', {'INPUT': layer_crossing, 'JOIN' : layer_street, 'JOIN_FIELDS' : ['width:carriageway', 'oneway'], 'OUTPUT': 'memory:'})['OUTPUT']
        #Straßeneigenschaften
        layer_crossing = processing.run('native:joinattributesbylocation', {'INPUT': layer_crossing, 'JOIN' : layer_intersections, 'JOIN_FIELDS' : ['crossing:highway'], 'OUTPUT': 'memory:'})['OUTPUT']
        #Winkel
        layer_crossing = processing.run('native:joinattributesbylocation', {'INPUT': layer_crossing, 'JOIN' : layer_vertices, 'JOIN_FIELDS' : ['angle'], 'OUTPUT': 'memory:'})['OUTPUT']

        crossing_attr_list = [
        'id',
        'highway',
        'crossing',
        'crossing_ref',
        'crossing:island',
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
        'angle'
        ]

        layer_crossing = clearAttributes(layer_crossing, crossing_attr_list)
        layer_crossing = processing.run('native:deleteduplicategeometries', {'INPUT': layer_crossing, 'OUTPUT' : proc_dir + 'crossing.geojson' })



#-------------------------------------------------------------------------
# Querungsstellen mit randseitigen Markierungen am Bordstein ausrichten
#-------------------------------------------------------------------------
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

    layer_crossing.startEditing()
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
    layer_crossing.commitChanges()

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
        layer_raw_kerb_street_areas_polygons = QgsVectorLayer(data_dir + 'kerb/kerb_street_areas.geojson|geometrytype=Polygon', 'Fahrbahnbereiche (raw)', 'ogr')
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
    qgis.core.QgsVectorFileWriter.writeAsVectorFormat(layer_crossing_buffer_markings, proc_dir + 'crossing_buffer_markings.geojson', 'utf-8', QgsCoordinateReferenceSystem(crs_from), 'GeoJson')



#-----------------------------------------------------
# Linien markierter Gehweg-Querungsstellen erzeugen
#-----------------------------------------------------
if proc_cr_lines:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Markierungen an Querungsstellen erzeugen...')
    print(time.strftime('%H:%M:%S', time.localtime()), '   Datensätze laden...')
    layer_crossing = QgsVectorLayer(proc_dir + 'crossing.geojson|geometrytype=Point', 'Querungsstellen', 'ogr')
    if not layer_raw_path_ways:
        layer_raw_path_ways = QgsVectorLayer(data_dir + 'path.geojson|geometrytype=LineString', 'path (raw)', 'ogr')
    layer_crossing_path = layer_raw_path_ways

    if not layer_raw_kerb_street_areas_polygons:
        layer_raw_kerb_street_areas_polygons = QgsVectorLayer(data_dir + 'kerb/kerb_street_areas.geojson|geometrytype=Polygon', 'Fahrbahnbereiche (raw)', 'ogr')
    layer_carriageway = layer_raw_kerb_street_areas_polygons

    #QgsProject.instance().addMapLayer(layer_carriageway, False)

    #neuen Layer für Querungsstellenmarkierungen speichern
    layer_crossing_path = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_crossing_path, 'EXPRESSION' : '"footway" = \'crossing\'', 'OUTPUT': 'memory:'})['OUTPUT']
    #layer_crossing_path = clearAttributes(layer_crossing_path, ['id', 'highway', 'crossing', 'crossing_ref', 'width'])
    layer_crossing_path = processing.run('native:reprojectlayer', { 'INPUT' : layer_crossing_path, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']

    #bestimmte Straßen-/crossing-Eigenschaften an querende Linien übergeben (relevant zur späteren Darstellung spezieller Fälle wie schrägen Zebrastreifen oder Kürzung im Bereich von randseitigen Markierungen)
    layer_crossing_path = processing.run('native:joinattributesbylocation', {'INPUT': layer_crossing_path, 'JOIN' : layer_crossing, 'JOIN_FIELDS' : ['crossing', 'crossing_ref', 'angle', 'crossing:buffer_marking'], 'PREFIX' : 'highway:', 'OUTPUT': 'memory:'})['OUTPUT']

    QgsProject.instance().addMapLayer(layer_crossing, False)
    QgsProject.instance().addMapLayer(layer_crossing_path, False)

    print(time.strftime('%H:%M:%S', time.localtime()), '   Lineare Querungen ermitteln (Eigenschaften vereinheitlichen)...')

    #nur Wege verarbeiten, die markierte Querungsstellen sein können (Ampeln, Zebrastreifen, sonstige "marked" crossings)
    layer_crossing_path.startEditing()
    id_crossing_crossing_path = layer_crossing_path.fields().indexOf('crossing')
    id_crossing_crossing_nodes = layer_crossing.fields().indexOf('crossing')
    id_crossing_ref_crossing_path = layer_crossing_path.fields().indexOf('crossing_ref')
    id_crossing_ref_crossing_nodes = layer_crossing.fields().indexOf('crossing_ref')
    for path in layer_crossing_path.getFeatures():
        crossing = NULL
        crossing_ref = NULL
        if id_crossing_crossing_path != -1:
            crossing = path.attribute('crossing')
            if crossing == 'unmarked':
                layer_crossing_path.deleteFeature(path.id())
                continue
        if id_crossing_ref_crossing_path != -1:
            crossing_ref = path.attribute('crossing_ref')
            if crossing_ref == 'zebra':
                crossing = 'zebra'
        #Wegelinien ohne "crossing"-Angabe: Angabe aus crossing-Node extrahieren
        if crossing == NULL:
            layer_crossing_path.removeSelection()
            layer_crossing_path.select(path.id())
            processing.run('native:selectbylocation', {'INPUT' : layer_crossing, 'INTERSECT' : QgsProcessingFeatureSourceDefinition(layer_crossing_path.id(), selectedFeaturesOnly=True), 'PREDICATE' : [0]})
            for crossing_node in layer_crossing.selectedFeatures():
                if id_crossing_crossing_nodes != -1:
                    crossing = crossing_node.attribute('crossing')
                if id_crossing_ref_crossing_nodes != -1:
                    crossing_ref = crossing_node.attribute('crossing_ref')
                if crossing_ref == 'zebra':
                    crossing = 'zebra'
        #nur markierte crossings weiter berücksichtigen
        if crossing != 'marked' and crossing != 'traffic_signals' and crossing != 'zebra':
            layer_crossing_path.deleteFeature(path.id())
            continue
        layer_crossing_path.changeAttributeValue(path.id(), id_crossing_crossing_path, crossing)

    print(time.strftime('%H:%M:%S', time.localtime()), '   Lineare Querungen ermitteln (Wegstücke ermitteln)...')

    layer_vertices = processing.run('native:extractvertices', {'INPUT': layer_crossing_path, 'OUTPUT': 'memory:'})['OUTPUT']
    QgsProject.instance().addMapLayer(layer_vertices, False)

    #alle crossing-Punkte auswählen, die für spätere Markierungen in Frage kommen
    layer_crossing = processing.run('qgis:extractbyexpression', {'INPUT' : layer_crossing, 'EXPRESSION' : '"crossing:highway" IS NOT \'cycleway\' and ("crossing" = \'traffic_signals\' or "crossing" = \'marked\' or "crossing" = \'zebra\' or "crossing_ref" = \'zebra\')', 'OUTPUT': 'memory:'})['OUTPUT']
    QgsProject.instance().addMapLayer(layer_crossing, False)

    #Die Stützpunkte jedes Weges durchgehen und prüfen, ob die Linien über die crossing-Punkte hinausgehen (also vermutlich bis zum Bordstein)
    #für jeden Weg Anzahl der Stützpunkte = maximalen Stützpunkt-Index ermitteln
    #TODO: Einfachere und schnellere Möglichkeit: crossings explodieren und prüfen, ob an crossing-Nodes mehr als eine Linie anschließt

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
    layer_crossing_path.commitChanges()

    #an Punkten ohne querende Linie: Querungslinie durch Versatz aus crossing-Node selbst erzeugen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Markierungslinien aus crossing-Nodes ableiten...')

    #alle crossing-Nodes auswählen, die nicht auf einer bereits erzeugten Linie liegen
    layer_crossing.selectAll()
    processing.run('native:selectbylocation', {'INPUT' : layer_crossing, 'INTERSECT' : layer_crossing_path, 'METHOD' : 3, 'PREDICATE' : [0]})

    crossing_line_markings_point1 = processing.run('native:translategeometry', {'INPUT' : QgsProcessingFeatureSourceDefinition(layer_crossing.id(), selectedFeaturesOnly=True), 'DELTA_X' : QgsProperty.fromExpression('-cos(if("crossing:direction:angle", "crossing:direction:angle" + 90, "angle") * (pi() / 180)) * (("width:carriageway" / 2) + 1)'), 'DELTA_Y' : QgsProperty.fromExpression('sin(if("crossing:direction:angle", "crossing:direction:angle" + 90, "angle") * (pi() / 180)) * (("width:carriageway" / 2) + 1)'), 'OUTPUT': 'memory:'})['OUTPUT']
    crossing_line_markings_point2 = processing.run('native:translategeometry', {'INPUT' : QgsProcessingFeatureSourceDefinition(layer_crossing.id(), selectedFeaturesOnly=True), 'DELTA_X' : QgsProperty.fromExpression('cos(if("crossing:direction:angle", "crossing:direction:angle" + 90, "angle") * (pi() / 180)) * (("width:carriageway" / 2) + 1)'), 'DELTA_Y' : QgsProperty.fromExpression('-sin(if("crossing:direction:angle", "crossing:direction:angle" + 90, "angle") * (pi() / 180)) * (("width:carriageway" / 2) + 1)'), 'OUTPUT': 'memory:'})['OUTPUT']

    #Punkte miteinander verbinden
    crossing_line_markings = processing.run('native:hublines', { 'HUBS' : crossing_line_markings_point1, 'HUB_FIELD' : 'id', 'HUB_FIELDS' : ['id'], 'SPOKES' : crossing_line_markings_point2, 'SPOKE_FIELD' : 'id', 'SPOKE_FIELDS' : ['crossing','crossing_ref'], 'OUTPUT': 'memory:'})['OUTPUT']

    #Einfache Geometrieprüfung: kurze Linien nicht weiter berücksichtigen
    crossing_line_markings.startEditing()
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
    crossing_line_markings.commitChanges()

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
    layer_crossing_lines.startEditing()
    layer_crossing_lines.deleteSelectedFeatures()
    layer_crossing_lines.commitChanges()

    layer_crossing_lines = processing.run('native:mergevectorlayers', {'LAYERS': [layer_crossing_lines, layer_crossing_lines1, layer_crossing_lines2], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing_lines = clearAttributes(layer_crossing_lines, ['id', 'highway', 'crossing', 'crossing_ref', 'temporary', 'width', 'highway:angle', 'highway:crossing:buffer_marking'])

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
        layer_raw_path_ways = QgsVectorLayer(data_dir + 'path.geojson|geometrytype=LineString', 'path (raw)', 'ogr')

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
    layer_junction_areas = layer_raw_area_highway_polygons
    layer_junction_areas = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_junction_areas, 'EXPRESSION' : '"junction" = \'yes\' OR "crossing" = \'traffic_signals\' OR "crossing" = \'marked\' OR "crossing" = \'zebra\'', 'OUTPUT': 'memory:'})['OUTPUT']
    #QgsProject.instance().addMapLayer(layer_junction_areas, True) # <----------------------------------------------------------------------------

    if not layer_raw_highway_points:
        layer_raw_highway_points = QgsVectorLayer(data_dir + 'highway.geojson|geometrytype=Point', 'highway (raw)', 'ogr')
    layer_stop_nodes = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_highway_points, 'EXPRESSION' : '"highway" = \'traffic_signals\' or "highway" = \'stop\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_stop_nodes = clearAttributes(layer_stop_nodes, ['id', 'highway', 'traffic_signals:direction', 'direction', 'stop_line', 'stop_line:angle'])

    #Fahrbahnen mit Fahrspurmarkierungen oder Abbiegespuren einladen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Lade Straßennetz...')
    if not layer_raw_highway_ways:
        layer_raw_highway_ways = QgsVectorLayer(data_dir + 'highway.geojson|geometrytype=LineString', 'highway (raw)', 'ogr')
    layer_lanes = layer_raw_highway_ways

    #Segmente an Ampeln und Stopschildern zur Generierung der Haltelinien ebenfalls einbeziehen
    layer_lanes_stop_lines = processing.run('native:extractbylocation', { 'INPUT' : layer_lanes, 'INTERSECT' : layer_stop_nodes, 'PREDICATE' : [0], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_lanes, 'EXPRESSION' : '"highway" IS NOT \'construction\' AND ("lane_markings" = \'yes\' OR "turn:lanes" IS NOT NULL OR "turn:lanes:forward" IS NOT NULL OR "turn:lanes:backward" IS NOT NULL OR "cycleway" = \'lane\' OR "cycleway:both" = \'lane\' OR "cycleway:right" = \'lane\' OR "cycleway:left" = \'lane\')', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_lanes, layer_lanes_stop_lines], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes = processing.run('native:deleteduplicategeometries', {'INPUT': layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']

    print(time.strftime('%H:%M:%S', time.localtime()), '   Vereinfache Straßeninformationen...')
#    layer_lanes = processing.run('native:dissolve', { 'FIELD' : lanes_attributes, 'INPUT' : layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']
#    layer_lanes = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes = clearAttributes(layer_lanes, lanes_attributes)
    #in metrisches Koordinatensystem konvertieren
    layer_lanes = processing.run('native:reprojectlayer', { 'INPUT' : layer_lanes, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']


#    QgsProject.instance().addMapLayer(layer_lanes, True)


    print(time.strftime('%H:%M:%S', time.localtime()), '   Bereite Fahrspuren vor...')
    #Attribut für Versatz ergänzen
    layer_lanes.startEditing()

    for attr in ['lanes', 'lanes:forward', 'lanes:backward', 'oneway', 'oneway:bicycle', 'placement_abs', 'offset', 'offset_delta', 'turn', 'reverse', 'width', 'access', 'surface:colour', 'marking:left', 'marking:right', 'buffer:left', 'buffer:right', 'separation:left', 'separation:right', 'lanes_forward', 'lanes_backward', 'id_instance']:
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
    lanes_dict['marking_lanes'] = {}
    lanes_dict['marking_right_lanes'] = {}
    lanes_dict['reverse_lanes'] = {}
    lanes_dict['placement'] = {}
    lanes_dict['segments_before'] = {}
    lanes_dict['segments_after'] = {}
    transition_dict = {}
    for lane in layer_lanes.getFeatures():
        oneway = oneway_bicycle = dual_carriageway = lane_markings = lanes = lanes_unmarked = lanes_forward = lanes_forward_unmarked = lanes_backward = lanes_backward_unmarked = lanes_conditional = lanes_forward_conditional = lanes_backward_conditional = turn_lanes = turn_lanes_forward = turn_lanes_backward = bus_lanes = bus_lanes_forward = bus_lanes_backward = psv_lanes = psv_lanes_forward = psv_lanes_backward = NULL
        cycleway_lanes = cycleway_lanes_forward = cycleway_lanes_backward = width_lanes = width_lanes_forward = width_lanes_backward = width_effective = overtaking = placement = placement_forward = placement_backward = placement_start = placement_forward_start = placement_backward_start = placement_end = placement_forward_end = placement_backward_end = cycleway = cycleway_both = cycleway_left = cycleway_right = cycleway_width = cycleway_both_width = cycleway_right_width = cycleway_left_width = NULL
        cycleway_buffer = cycleway_buffer_left = cycleway_buffer_right = cycleway_buffer_both = cycleway_both_buffer = cycleway_both_buffer_left = cycleway_both_buffer_right = cycleway_both_buffer_both = cycleway_right_buffer = cycleway_right_buffer_left = cycleway_right_buffer_right = cycleway_right_buffer_both = cycleway_left_buffer = cycleway_left_buffer_left = cycleway_left_buffer_right = cycleway_left_buffer_both = 0
        cycleway_separation = cycleway_separation_left = cycleway_separation_right = cycleway_separation_both = cycleway_both_separation = cycleway_both_separation_left = cycleway_both_separation_right = cycleway_both_separation_both = cycleway_right_separation = cycleway_right_separation_left = cycleway_right_separation_right = cycleway_right_separation_both = cycleway_left_separation = cycleway_left_separation_left = cycleway_left_separation_right = cycleway_left_separation_both = NULL
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
        if layer_lanes.fields().indexOf('width:lanes:backward') != -1:
            width_lanes_backward = lane.attribute('width:lanes:backward')
        if layer_lanes.fields().indexOf('width:effective') != -1:
            width_effective = lane.attribute('width:effective')
        if layer_lanes.fields().indexOf('overtaking') != -1:
            overtaking = lane.attribute('overtaking')
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
        marking_lanes = []
        for i in range(lanes):
            #Überholverbot = durchgezogene Linie
            if overtaking == 'no' and i == lanes_backward:
                marking_lanes.append('solid_line')
            else:
                if lanes_unmarked:
                    if i < lanes_backward:
                        if not lanes_backward_unmarked:
                            if lanes_forward_unmarked:
                                lanes_backward_unmarked = lanes_unmarked - lanes_forward_unmarked
                            else:
                                lanes_backward_unmarked = lanes_unmarked / 2
                        diff_lanes_backward = lanes_backward_unmarked - lanes_backward_marked
                        if i < diff_lanes_backward:
                            marking_lanes.append('no')
                        else:
                            marking_lanes.append('unspecified')
                    else:
                        if i >= lanes_backward + lanes_forward_marked:
                            marking_lanes.append('no')
                        else:
                            marking_lanes.append('unspecified')
                else:
                    if lane_markings or turn_lanes or turn_lanes_forward or turn_lanes_backward:
                        marking_lanes.append('unspecified')
                    else:
                        marking_lanes.append('no')
        lanes_dict['marking_lanes'][lane.attribute('id')] = marking_lanes

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
                lanes_dict['marking_lanes'][lane.attribute('id')][lanes_backward - 1] = 'solid_line'
                if len(lanes_dict['marking_lanes'][lane.attribute('id')]) > lanes_backward:
                    lanes_dict['marking_lanes'][lane.attribute('id')][lanes_backward] = 'solid_line'

        #Busspur-Informationen für alle Spuren von links nach rechts speichern
        access_lanes = []
        #keine Unterscheidung zwischen bus und psv notwendig – alles als Busspur deklarieren
        lanes_bus += lanes_psv
        lanes_bus_forward += lanes_psv_forward
        lanes_bus_backward += lanes_psv_backward

        #TODO: lanes:bus/psv:forward/backward wird zur Zeit noch nicht unterstützt – nur einfaches lanes:bus/lanes:psv
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
#            layer_lanes.deleteFeature(lane.id())
#            continue

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
        l = int(placement[-1])

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
                cyclelanes_forward = 1
            if cycleway_left == 'lane' or cycleway_both == 'lane':
                cyclelanes_backward = 1
            if cycleway == 'lane':
                cyclelanes_forward = 1
                if not oneway == 'yes':
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
                l = int(placement[-1])
                l += 1
                placement = placement[0:-1] + str(l)
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
                lanes_dict['marking_lanes'][lane.attribute('id')].append('unspecified')
            if cyclelanes_backward:
                lanes_dict['turn_lanes'][lane.attribute('id')].insert(0, 'none')
                lanes_dict['access_lanes'][lane.attribute('id')].insert(0, 'bicycle')
                lanes_dict['width_lanes'][lane.attribute('id')].insert(0, cycleway_left_width)
                lanes_dict['marking_lanes'][lane.attribute('id')].insert(0, 'unspecified')
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

        #Geschützte Radstreifen und Bodenmarkierungen erkennen (cycleway:separation)
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

        buffer_left_lanes = []
        buffer_right_lanes = []
        separation_left_lanes = []
        separation_right_lanes = []

        for i in range(lanes):
            if lanes_dict['access_lanes'][lane.attribute('id')][i] == 'bicycle' or lanes_dict['cycleway_lanes'][lane.attribute('id')][i] == 'lane':
                if i + 1 <= lanes_backward:
                    buffer_left_lanes.append(float(cycleway_left_buffer_left))
                    buffer_right_lanes.append(float(cycleway_left_buffer_right))
                    separation_left_lanes.append(cycleway_left_separation_left)
                    separation_right_lanes.append(cycleway_left_separation_right)
                else:
                    buffer_left_lanes.append(float(cycleway_right_buffer_left))
                    buffer_right_lanes.append(float(cycleway_right_buffer_right))
                    separation_left_lanes.append(cycleway_right_separation_left)
                    separation_right_lanes.append(cycleway_right_separation_right)
            else:
                buffer_left_lanes.append(0)
                buffer_right_lanes.append(0)
                separation_left_lanes.append(NULL)
                separation_right_lanes.append(NULL)
        lanes_dict['buffer_left_lanes'][lane.attribute('id')] = buffer_left_lanes
        lanes_dict['buffer_right_lanes'][lane.attribute('id')] = buffer_right_lanes
        lanes_dict['separation_left_lanes'][lane.attribute('id')] = separation_left_lanes
        lanes_dict['separation_right_lanes'][lane.attribute('id')] = separation_right_lanes

        #Offset/Position der linkesten Spur an evtl. vorhandene Puffer anpassen
        for i in range(lanes):
            if i <= lanes_backward:
                offset += buffer_left_lanes[i]
                if i > 0:
                   offset += buffer_right_lanes[i]

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
#       layer_lanes_dual_carriageway = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_lanes_dual_carriageway, 'OUTPUT': 'memory:'})['OUTPUT']
#       layer_lanes_dual_carriageway = processing.run('native:splitwithlines', { 'INPUT' : layer_lanes_dual_carriageway, 'LINES' : layer_lanes_dual_carriageway, 'OUTPUT': 'memory:'})['OUTPUT']

        #Start- und End-Vertices auswählen
        layer_dual_carriageways_vertices = processing.run('native:extractspecificvertices', { 'INPUT' : layer_lanes_dual_carriageway, 'VERTICES' : '0,-1', 'OUTPUT': 'memory:'})['OUTPUT']
        #Stützpunkte mit Liniensegmenten ohne dual_carriageway verschneiden, um nur Verzweigungspunkte zu erhalten
        layer_lanes_single_carriageway = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_lanes, 'EXPRESSION' : '"dual_carriageway" IS NOT \'yes\' and ("lane_markings" IS \'yes\' or "turn_lanes" IS \'yes\')', 'OUTPUT': 'memory:'})['OUTPUT']
        processing.run('native:selectbylocation', {'INPUT' : layer_dual_carriageways_vertices, 'INTERSECT' : layer_lanes_single_carriageway, 'METHOD' : 0, 'PREDICATE' : [4]})
        #Stützpunkte in Kreuzungsbereichen (area_highway/junction) aus der Auswahl entfernen -> alle übriggebliebenen sollten (meist) Verzweigungspunkte sein
        processing.run('native:selectbylocation', {'INPUT' : layer_dual_carriageways_vertices, 'INTERSECT' : layer_junction_areas, 'METHOD' : 3, 'PREDICATE' : [6] })


        #QgsProject.instance().addMapLayer(layer_dual_carriageways_vertices, True)


        #Koordinaten der ausgewählten Punkte speichern
        vertex_list = []
        for vertex in layer_dual_carriageways_vertices.selectedFeatures():
            vertex_x = vertex.geometry().asPoint().x()
            vertex_y = vertex.geometry().asPoint().y()

            vertex_list.append([vertex_x, vertex_y])

        #alle Zweirichtungs-Segmente durchgehen und verzweigende Start-/End-Vertices versetzen
#        layer_lanes.startEditing()
        for lane in layer_lanes.getFeatures():
            #nur explizit markierte Fahrspuren behandeln
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

            placement_pos_from = placement_from[0:-1]
            placement_pos_to = placement_to[0:-1]
            placement_lane_from = placement_lane_from_value = int(placement_from[-1])
            placement_lane_to = placement_lane_to_value = int(placement_to[-1])

            #ein Ende des Segments versetzen (des Ende zur Richtung mit mehr Fahrspuren)
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

        #individuellen Versatz entsprechend der Spurbreiten und Puffer ermitteln und nachjustieren
        width_lanes = lanes_dict['width_lanes'][lane.attribute('id')]
        buffer_left_lanes = lanes_dict['buffer_left_lanes'][lane.attribute('id')]
        buffer_right_lanes = lanes_dict['buffer_right_lanes'][lane.attribute('id')]
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

        # > Markierung der Linie (üblicherweise links der Spur)
        marking_lanes = lanes_dict['marking_lanes'][lane.attribute('id')]
        marking = marking_lanes[instance]

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

        cycleway_lanes = lanes_dict['cycleway_lanes'][lane.attribute('id')]
        cycleway = cycleway_lanes[instance]
        if cycleway == 'lane':
            access = 'bicycle'
            layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('access'), access)
            lanes_dict['access_lanes'][lane.attribute('id')][instance] = access

        surface_colour = 'none'
        clr = marking_right = NULL
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
            #TODO: Radweglinie aus exclusive/etc.-Schema ableiten
            #...in Linienrichtung
            if separation_left:
                if 'dashed_line' in separation_left:
                    marking = 'dashed_line'
                elif 'solid_line' in separation_left:
                    marking = 'solid_line'
                else:
                    marking = 'unspecified'
            if separation_right:
                if 'dashed_line' in separation_right:
                    marking_right = 'dashed_line'
                elif 'solid_line' in separation_right:
                    marking_right = 'solid_line'
                else:
                    marking_right = 'no'

            if marking_right != 'dashed_line' and marking_right != 'solid_line':
                #Radstreifen in Mittellage: Wenn nicht anders angegeben, von gestrichelter Linie ausgehen
                if instance != 0 and instance != lanes - 1:
                    if (not reverse and access_lanes[instance + 1] == 'vehicle') or (reverse and access_lanes[instance - 1] == 'vehicle'):
                        marking_right = 'dashed_line'

        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('surface:colour'), surface_colour)
        layer_lanes.changeAttributeValue(lane.id(), layer_lanes.fields().indexOf('marking:left'), marking)
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
        if lane.attribute('reverse') == 1:
            layer_lanes.select(lane.id())
    layer_lanes_reversed = processing.run('native:reverselinedirection', {'INPUT' : QgsProcessingFeatureSourceDefinition(layer_lanes.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']

    features = layer_lanes.getFeatures()
    ids = [ f.id() for f in features if f.attribute('reverse') == 1]
    with edit(layer_lanes):
        layer_lanes.deleteFeatures(ids)

    layer_lanes.commitChanges()

    layer_lanes = processing.run('native:mergevectorlayers', {'LAYERS' : [layer_lanes, layer_lanes_reversed], 'OUTPUT': 'memory:'})['OUTPUT']


    #Spurversätze korrigieren, z.B. bei Erhöhung von Fahrspuren
    layer_lanes.startEditing()
    for lane in layer_lanes.getFeatures():
        num_lanes = len(lanes_dict['width_lanes'][lane.attribute('id')])
        segments_before = lanes_dict['segments_before'][lane.attribute('id')]
        num_segments_before = len(segments_before['id'])
        #keine angrenzenden Segmente: kein Handlungsbedarf, TODO: Mit mehr als 2 angrenzenden Segmenten umgehen
        if num_segments_before < 1 or num_segments_before > 2:
            continue

        #TODO: Fehlermeldung, wenn schonmal ein Segment mit gleicher id_instance verschoben wurde!

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
                            if lane.attribute('reverse') == 0:
                                vertex = 0
                                vertex_before = vertex_count_before - 1
                            else:
                                vertex = vertex_count - 1
                                if lane_before.attribute('reverse') == 0:
                                    vertex_before = vertex_count_before - 1
                                else:
                                    vertex_before = 0
                            x_before = geom_lane_before.vertexAt(vertex_before).x()
                            y_before = geom_lane_before.vertexAt(vertex_before).y()
                            layer_lanes.moveVertex(x_before, y_before, lane.id(), vertex)
                    continue
#            #kein Handlungsbedarf bei gerader Differenz der Spurzahlen
#            if not abs(num_lanes - num_lanes_before) % 2:
#                continue
            #TODO: kein Handlungsbedarf, wenn beide Segmente mit zueinander passenden placment-Attributen ausgestattet sind:
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
                            if lane.attribute('reverse') == 0:
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
                            if lane.attribute('reverse') == 0:
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

        if num_segments_before == 2:
            if lanes_dict['access_lanes'][lane.attribute('id')][instance] == 'bicycle':
                processing.run('qgis:selectbyattribute', { 'INPUT' : layer_lanes, 'FIELD' : 'id', 'VALUE' : segments_before['id'][0]})
                for lane_before in layer_lanes.getSelectedFeatures():
                    if segments_before['inverted'][0] == 0:
                        #Nur Spuren angleichen, die in die gleiche Richtung führen
                        if lane_before.attribute('reverse') != lane.attribute('reverse'):
                            continue
                        if lane_before.attribute('access') == 'bicycle':
                            cyclelane_same_direction = cyclelane_before_same_direction = 0
                            reverse = lane.attribute('reverse')
                            for i in range(num_lanes):
                                if lanes_dict['access_lanes'][lane.attribute('id')][i] == 'bicycle' and lanes_dict['reverse_lanes'][lane.attribute('id')][i] == reverse:
                                    cyclelane_same_direction += 1
                            num_lanes_before = len(lanes_dict['access_lanes'][segments_before['id'][0]])
                            reverse_before = lane_before.attribute('reverse')
                            for i in range(num_lanes_before):
                                if lanes_dict['access_lanes'][lane_before.attribute('id')][i] == 'bicycle' and lanes_dict['reverse_lanes'][lane_before.attribute('id')][i] == reverse_before:
                                    cyclelane_before_same_direction += 1

                            if cyclelane_same_direction > 1 or cyclelane_before_same_direction > 1:
                                #TODO: Umgang mit (seltener) Situation, wenn mehrere Radspuren pro Richtung aufeinandertreffen
                                continue
                            else:
                                if lane.attribute('reverse') == 0:
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

    layer_lanes.commitChanges()

#TODO: Für Auflösung der Spuren nach gemeinsamen Merkmalen bräuchte es ein Attribut "is_middle_lane" o.ä., um Fahrspuren zu identifizieren, die an entgegengesetzte Fahrspuren angrenzen – das geht zur Zeit nur über lane und lane:forward – diese beiden Attribute beim Auflösen zu berücksichtigen, würde das Auflösen jedoch weitgehend unnütz machen
#    dissolve_attr = ['turn', 'reverse', 'width', 'access', 'surface:colour', 'lane_markings', 'marking:left', 'marking:right']
#    #für schönere/zusammenhängendere Markierungen nach gemeinsamen Merkmalen auflösen
#    layer_lanes = processing.run('native:dissolve', { 'FIELD' : dissolve_attr, 'INPUT' : layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']
#    layer_lanes = processing.run('native:multiparttosingleparts', {'INPUT' : layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']

    #Linien zur schöneren Darstellung noch einmal drehen (von der Kreuzung ausgehend beginnen – immer gleicher Markierungsabstand)
    layer_lanes = processing.run('native:reverselinedirection', {'INPUT' : layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']

    #Liste von Attributen, die an jeder Spur am Ende erhalten bleiben
#    list_lane_attributes = ['reverse', 'lane_markings', 'marking:left', 'marking:right', 'turn', 'width', 'access', 'surface:colour']
    list_lane_attributes = ['lanes', 'lanes:forward', 'id_instance', 'instance', 'reverse', 'lane_markings', 'marking:left', 'marking:right', 'buffer:left', 'buffer:right', 'separation:left', 'separation:right', 'turn', 'width', 'access', 'surface:colour']

    #Markierungen in Knotenpunktbereichen (in Kreuzungen) entfernen
    #Wenn "lane_markings:junction" = 'yes', "lane_markings:crossing" = 'yes' oder "cycleway:*type"='crossing', dann Markierungen dennoch darstellen
    QgsProject.instance().addMapLayer(layer_junction_areas, False)

    #Fahrradfurten in Knotenpunktbereichen separieren, um sie später wieder hinzuzufügen
    layer_lanes_bicycle_crossing = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_lanes, 'EXPRESSION' : '"access" = \'bicycle\' and ("cycleway:type" = \'crossing\' or "cycleway:both:type" = \'crossing\' or ("cycleway:right:type" = \'crossing\' and "reverse" = 0) or ("cycleway:left:type" = \'crossing\' and "reverse" = 1))', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes_bicycle_crossing = processing.run('native:clip', {'INPUT': layer_lanes_bicycle_crossing, 'OVERLAY': layer_junction_areas, 'OUTPUT': 'memory:'})['OUTPUT']

    processing.run('qgis:selectbyexpression', {'INPUT' : layer_junction_areas, 'EXPRESSION' : '"junction" = \'yes\''})
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

    #nach gemeinsamen Attributen auflösen, bereinigen und speichern
    #TODO: Neues Attribut für innerste Spur einer Fahrtrichtung anlegen, um auch "lanes", "lanes:forward", evtl. instance ignorieren zu können
    list_lane_attributes.remove('id_instance')
    layer_lanes = processing.run('native:dissolve', { 'FIELD' : list_lane_attributes, 'INPUT' : layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']
    list_lane_attributes.append('id_instance')
    layer_lanes = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_lanes, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_lanes = clearAttributes(layer_lanes, list_lane_attributes)
    qgis.core.QgsVectorFileWriter.writeAsVectorFormat(layer_lanes, proc_dir + 'marked_lanes.geojson', 'utf-8', QgsCoordinateReferenceSystem(crs_from), 'GeoJson')

    #--------------------------------------
    #Abschließend Haltelinien generieren
    #--------------------------------------
    print(time.strftime('%H:%M:%S', time.localtime()), '   Generiere Haltelinien...')
    lanes_attributes_plus_id = lanes_attributes
    lanes_attributes_plus_id.insert(0, 'id')
    layer_stop_nodes = processing.run('native:joinattributesbylocation', {'INPUT': layer_stop_nodes, 'JOIN' : layer_raw_highway_ways, 'JOIN_FIELDS' : lanes_attributes_plus_id, 'METHOD' : 1, 'PREDICATE' : [0], 'PREFIX' : 'highway:', 'OUTPUT': 'memory:'})['OUTPUT']

    #Haltelinienpunkte und Knotenpunktbereiche in metrische KBS reprojizieren
    layer_stop_nodes = processing.run('native:reprojectlayer', { 'INPUT' : layer_stop_nodes, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    QgsProject.instance().addMapLayer(layer_stop_nodes, False)
    layer_junction_areas_outlines = processing.run('native:polygonstolines', { 'INPUT' : layer_junction_areas, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_junction_areas_outlines = processing.run('native:reprojectlayer', { 'INPUT' : layer_junction_areas_outlines, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']

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
    layer_stop_lines = QgsVectorLayer("LineString?crs=" + crs_to + "&field=road_marking:string&field=road_marking:left:string&field=road_marking:right:string&field=stop_line:string", "Haltelinien", "memory")
    provider = layer_stop_lines.dataProvider()
    layer_stop_lines.updateFields() 

    #Haltelinien erzeugen
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
        placement_lane = int(placement[-1])
        placement_pos = placement[0:-1]
        lanes_width = lanes_dict['width_lanes'][highway_id]
        lanes_reverse = lanes_dict['reverse_lanes'][highway_id]
        direction = NULL
        if layer_stop_nodes.fields().indexOf('direction') != -1:
            direction = stop_node.attribute('direction')
        if stop_node_type == 'traffic_signals' and layer_stop_nodes.fields().indexOf('traffic_signals:direction') != -1:
            direction = stop_node.attribute('traffic_signals:direction')

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
            line.setAttributes(['stop_line', NULL, NULL, 'solid_line'])
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
                junction_line.setAttributes(['stop_line', NULL, NULL, 'solid_line'])
                provider.addFeature(junction_line)
                layer_stop_lines.updateExtents()

#            QgsProject.instance().addMapLayer(layer_junction_lines, True)

    #Segmente ausschließen, die sich auf anderen Fahrbahnbereichen befinden - insbesondere auf naheliegenden Gegenfahrbahnen von dual_carriageways
    #über Schnittpunkte von Straßen und Knotenpunktflächen ermittelt, gepuffert entsprechend der Fahrbahnbreite
    layer_junction_enter_nodes = processing.run('native:lineintersections', {'INPUT': layer_junction_areas_outlines, 'INTERSECT': layer_highway_lanes, 'INPUT_FIELDS' : ['junction'], 'INTERSECT_FIELDS' : ['id','name','highway', 'lanes'], 'INTERSECT_FIELDS_PREFIX': '', 'OUTPUT': 'memory:'})['OUTPUT']
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
    layer_road_markings = clearAttributes(layer_road_markings, ['id', 'road_marking', 'road_marking:left', 'road_marking:right', 'stop_line'])

    #Linien auf Fahrbahnbereiche beschneiden
    if not layer_raw_kerb_street_areas_polygons:
        layer_raw_kerb_street_areas_polygons = QgsVectorLayer(data_dir + 'kerb/kerb_street_areas.geojson|geometrytype=Polygon', 'Fahrbahnbereiche (raw)', 'ogr')
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
        layer_raw_kerb_street_areas_polygons = QgsVectorLayer(data_dir + 'kerb/kerb_street_areas.geojson|geometrytype=Polygon', 'Fahrbahnbereiche (raw)', 'ogr')
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
    layer_highway = processing.run('native:dissolve', { 'FIELD' : ['highway', 'service', 'width', 'width:carriageway'], 'INPUT' : layer_highway, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_highway = clearAttributes(layer_highway, ['highway', 'service', 'width', 'width:carriageway'])
    layer_highway = processing.run('native:multiparttosingleparts', {'INPUT' : layer_highway, 'OUTPUT' : proc_dir + 'service.geojson' })



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
    #Radwege und markierte Querungsstellen herausfiltern und reprojizieren
    layer_cycleways_on_lane = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_path_ways, 'EXPRESSION' : '"highway" = \'cycleway\' and ("cycleway:type" = \'lane\' or "cycleway:type" = \'crossing\')', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_cycleways_off_lane = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_path_ways, 'EXPRESSION' : '"highway" = \'cycleway\' and "cycleway:type" IS NOT \'lane\' and "cycleway:type" IS NOT \'crossing\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossings = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_path_ways, 'EXPRESSION' : '"footway" = \'crossing\' and ("crossing" = \'traffic_signals\' or "crossing" = \'marked\' or "crossing" = \'zebra\')', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossings = processing.run('native:reprojectlayer', { 'INPUT' : layer_crossings, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    #Radwege an markierten Querungsstellen unterbrechen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Radwege an Querungsstellen unterbrechen...')
    layer_crossings_buffer = processing.run('native:buffer', { 'INPUT' : layer_crossings, 'DISTANCE' : QgsProperty.fromExpression('if("width", "width" / 2, 3)'), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_cycleways_on_lane = processing.run('native:difference', {'INPUT' : layer_cycleways_on_lane, 'OVERLAY' : layer_crossings_buffer, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_cycleways = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_cycleways_on_lane, layer_cycleways_off_lane], 'OUTPUT': 'memory:'})['OUTPUT']

    #Radwege an  Haltelinien aufspalten
    layer_stop_lines = QgsVectorLayer(proc_dir + 'road_markings.geojson|geometrytype=LineString', 'road markings', 'ogr')
    layer_stop_lines = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_stop_lines, 'EXPRESSION' : '"road_marking" = \'stop_line\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_cycleways = processing.run('native:splitwithlines', { 'INPUT' : layer_cycleways, 'LINES' : layer_stop_lines, 'OUTPUT': 'memory:'})['OUTPUT']

    #kurze Wegstücke entfernen
    layer_cycleways = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_cycleways, 'EXPRESSION' : '$length > 2.5', 'OUTPUT': 'memory:'})['OUTPUT']

    #Flächen für Radweg-Querungen im Fahrbahnbereich erzeugen, um überschneidende Linien zu überdecken
    #TODO: Begrenzungslinien besser durch Versatz erzeugen und überschneidende Linien ausschließen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Deckende Radwegflächen in Kreuzungsbereichen erzeugen...')
    layer_cycleways_crossings = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_cycleways, 'EXPRESSION' : '"cycleway:type" = \'crossing\' and "surface:colour" IS NULL', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_cycleways_crossings = processing.run('native:reprojectlayer', { 'INPUT' : layer_cycleways_crossings, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_cycleways_crossings = processing.run('native:buffer', { 'INPUT' : layer_cycleways_crossings, 'DISTANCE' : QgsProperty.fromExpression('if("width", "width" / 2, 0.5)'), 'END_CAP_STYLE' : 1, 'OUTPUT': 'memory:'})['OUTPUT']
    #Flächen auf Fahrbahnbereiche beschneiden
    if not layer_raw_kerb_street_areas_polygons:
        layer_raw_kerb_street_areas_polygons = QgsVectorLayer(data_dir + 'kerb/kerb_street_areas.geojson|geometrytype=Polygon', 'Fahrbahnbereiche (raw)', 'ogr')
    layer_cycleways_crossings = processing.run('native:clip', {'INPUT' : layer_cycleways_crossings, 'OVERLAY' : layer_raw_kerb_street_areas_polygons, 'OUTPUT' : proc_dir + 'cycleways_crossing.geojson' })

    #Radwege bereinigen und abspeichern
    layer_cycleways = clearAttributes(layer_cycleways, ['id', 'highway', 'oneway', 'cycleway:type', 'crossing', 'width', 'surface', 'smoothness', 'surface:colour', 'separation', 'separation:left', 'separation:right', 'separation:both', 'buffer', 'buffer:left', 'buffer:right', 'buffer:both', 'lanes', 'turn:lanes', 'placement'])
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



#-------------------------------------------------------------------------------------------------------------
# Gebäudeteile auf Stockwerksunterschiede auflösen, Gebäudegrundrisse / schwebende Gebäudeteile verarbeiten
#-------------------------------------------------------------------------------------------------------------
if proc_building_parts:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Verarbeite Gebäudeteile...')
    #Gebäudeteile mit gemeinsamen Höhenmerkmalen zusammenführen
    layer_building_parts_raw = QgsVectorLayer(data_dir + 'building_part.geojson|geometrytype=Polygon', 'Gebäudeteile (roh)', 'ogr')
    layer_building_parts_raw = clearAttributes(layer_building_parts_raw, building_key_list)
    layer_building_parts = processing.run('native:fixgeometries', { 'INPUT' : layer_building_parts_raw, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_parts = processing.run('native:dissolve', { 'FIELD' : ['building:levels','building:min_level','roof:levels'], 'INPUT' : layer_building_parts, 'OUTPUT' : proc_dir + 'building_parts_dissolved.geojson' })

    print(time.strftime('%H:%M:%S', time.localtime()), 'Erzeuge Gebäudegrundflächen...')
    #Gebäudeteile mit "building:min_level" > 0 oder "min_height" > 0 oder "roof" von Grundfläche abziehen
    if not layer_raw_buildings_polygons:
        layer_raw_buildings_polygons = QgsVectorLayer(data_dir + 'buildings.geojson|geometrytype=Polygon', 'buildings (raw)', 'ogr')
    layer_buildings = layer_raw_buildings_polygons
    layer_buildings = clearAttributes(layer_buildings, building_key_list)

    layer_building_parts_min_level_1 = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_building_parts_raw, 'EXPRESSION' : '\"building:min_level\" > 0 OR \"min_height\" > 0 OR \"building:part\" = \'roof\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_building_parts_min_level_0 = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_building_parts_raw, 'EXPRESSION' : '((\"building:min_level\" <= 0 OR \"min_height\" <= 0) OR (\"building:min_level\" IS NULL AND \"min_height\" IS NULL)) AND \"building:part\" <> \'roof\'', 'OUTPUT': 'memory:'})['OUTPUT']

    QgsProject.instance().addMapLayer(layer_building_parts_min_level_1, False)
    QgsProject.instance().addMapLayer(layer_building_parts_min_level_0, False)

    #vorher Gebäudeteile ohne min_level von allen Gebäudeteilen abziehen, um Gebäudeteile innerhalb von (schwebenden) Gebäudeteilen zu berücksichtigen
    layer_building_parts_min_level = processing.run('native:difference', {'INPUT' : QgsProcessingFeatureSourceDefinition(layer_building_parts_min_level_1.id(), flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometrySkipInvalid), 'OVERLAY' : QgsProcessingFeatureSourceDefinition(layer_building_parts_min_level_0.id(), flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometrySkipInvalid), 'OUTPUT': 'memory:'})['OUTPUT']

    layer_buildings = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_buildings, 'EXPRESSION' : '\"building\" IS NOT \'roof\' AND ("building:min_level" <= 0 OR "building:min_level" IS NULL) AND ("min_height" <= 0 OR "min_height" IS NULL)', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_buildings = processing.run('native:difference', { 'INPUT': layer_buildings, 'OVERLAY' : layer_building_parts_min_level, 'OUTPUT' : proc_dir + 'building_parts_min_level.geojson' })



#------------------------------------------------
# Hausnummern an inneren Gebäudeumring versetzen
#------------------------------------------------
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



#-----------------------------------------------------------------------------
# Gras-Flächen zur besseren Darstellung aus playground-Polygonen ausstanzen
#-----------------------------------------------------------------------------
if proc_playground:
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



#-----------------------------------------------------------------------------------------------------
# Richtet bestimmte Straßenmöbel zur nächstgelegenen Straße hin aus (Straßenlaternen, Schaltkästen)
#-----------------------------------------------------------------------------------------------------
if proc_orient_man_made:
    print(time.strftime('%H:%M:%S', time.localtime()), 'Straßenmöbel ausrichten...')
    print(time.strftime('%H:%M:%S', time.localtime()), '   Straßenreferenz einladen...')
    if not layer_raw_highway_ways:
        layer_raw_highway_ways = QgsVectorLayer(data_dir + 'highway.geojson|geometrytype=LineString', 'highway (raw)', 'ogr')
    if not layer_raw_path_ways:
        layer_raw_path_ways = QgsVectorLayer(data_dir + 'path.geojson|geometrytype=LineString', 'path (raw)', 'ogr')
    print(time.strftime('%H:%M:%S', time.localtime()), '   Straßenreferenz zusammenführen...')
    layer_full_way_network = processing.run('native:mergevectorlayers', { 'CRS' : QgsCoordinateReferenceSystem(crs_to), 'LAYERS' : [layer_raw_highway_ways, layer_raw_path_ways], 'OUTPUT': 'memory:'})['OUTPUT']
#    #layer_full_way_network = clearAttributes(layer_full_way_network, ['id', 'highway', 'name'])
#    print(time.strftime('%H:%M:%S', time.localtime()), '   Straßenreferenz transformieren...')
#    QgsVectorFileWriter.writeAsVectorFormatV2(layer_full_way_network, proc_dir + 'full_way_network.geojson', transform_context, save_options)
#    layer_full_way_network = QgsVectorLayer(proc_dir + 'full_way_network.geojson|geometrytype=LineString', 'Straßen- und Wegenetz', 'ogr')
#
    print(time.strftime('%H:%M:%S', time.localtime()), '   Straßenmöbel einladen...')
    if not layer_raw_man_made_points:
        layer_raw_man_made_points = QgsVectorLayer(data_dir + 'man_made.geojson|geometrytype=Point', 'man_made (raw)', 'ogr')

    #Straßenmöbel filtern, für die eine Richtung relevant sein kann (Straßenlaternen, Schaltkästen)
    layer_street_furniture = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_man_made_points, 'EXPRESSION' : '("highway" = \'street_lamp\' AND "lamp_mount" = \'bent_mast\') OR "man_made" = \'street_cabinet\'', 'OUTPUT': 'memory:'})['OUTPUT']
    print(time.strftime('%H:%M:%S', time.localtime()), '   Straßenmöbel reprojizieren...')
    layer_street_furniture = processing.run('native:reprojectlayer', { 'INPUT' : layer_street_furniture, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
#    QgsVectorFileWriter.writeAsVectorFormatV2(layer_street_furniture, proc_dir + 'street_furniture.geojson', transform_context, save_options)
#    layer_street_furniture = QgsVectorLayer(proc_dir + 'street_furniture.geojson|geometrytype=Point', 'Straßenmöbel', 'ogr')
#
    #Puffer (11 Meter) um relevante Straßenmöbel erzeugen, um im Folgenden nur Straßen in diesem Bereich zu berücksichtigen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Relevante Straßen und Wege selektieren...')
    layer_street_furniture_buffer = processing.run('native:buffer', { 'INPUT' : layer_street_furniture, 'DISTANCE' : 11, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_next_streets = processing.run('native:extractbylocation', { 'INPUT' : layer_full_way_network, 'INTERSECT' : layer_street_furniture_buffer, 'PREDICATE' : [0], 'OUTPUT': 'memory:'})['OUTPUT']

    #dichte Punktekette aus Straßen und Wegen erzeugen, um anschließend Abstand zu nächstgelegenem Punkt zu ermitteln
    print(time.strftime('%H:%M:%S', time.localtime()), '   Wegenetz in Punkte umwandeln...')
    layer_next_streets_points = processing.run('native:pointsalonglines', {'INPUT' : layer_next_streets, 'DISTANCE' : 0.5, 'OUTPUT': 'memory:'})['OUTPUT']
#    #Punkte außerhalb des Referenz-Radius um Straßenmöbel zur Beschleunigung des Prozesses verwerfen
#    layer_next_streets_points = processing.run('native:extractbylocation', { 'INPUT' : layer_next_streets_points, 'INTERSECT' : layer_street_furniture_buffer, 'PREDICATE' : [0], 'OUTPUT': 'memory:'})['OUTPUT']
#    print(time.strftime('%H:%M:%S', time.localtime()), '   Nächstgelegenen Straßenpunkt ermitteln...')

    #Zunächst Verbindung zu nächstgelegener Verkehrsstraße suchen
    print(time.strftime('%H:%M:%S', time.localtime()), '   An Verkehrsstraßen ausrichten...')
    QgsProject.instance().addMapLayer(layer_next_streets_points, False)
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_next_streets_points, 'EXPRESSION' : '"highway" IS \'primary\' or "highway" IS \'secondary\' or "highway" IS \'tertiary\' or "highway" IS \'residential\' or "highway" IS \'unclassified\' or "highway" IS \'living_street\' or "highway" IS \'pedestrian\' or "highway" IS \'road\''})
    layer_shortest_distance_lines_streets = processing.run('qgis:distancetonearesthublinetohub', { 'FIELD' : 'highway', 'HUBS' : QgsProcessingFeatureSourceDefinition(layer_next_streets_points.id(), selectedFeaturesOnly=True), 'INPUT' : layer_street_furniture, 'UNIT' : 0, 'OUTPUT': 'memory:'})['OUTPUT']
    #Anfangs-Stützpunkt der Verbindungslinie ist das Straßenmöbel-Objekt – Winkel wird dabei mit übergeben 
    layer_street_furniture_streets = processing.run('native:extractspecificvertices', { 'INPUT' : layer_shortest_distance_lines_streets, 'VERTICES' : '0', 'OUTPUT': 'memory:'})['OUTPUT']
    #Elemente extrahieren, die bis zu 11 Meter von Verkehrsstraßen entfernt liegen (bei Nebenstraßen etwas weniger)
    layer_street_furniture_streets = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_street_furniture_streets, 'EXPRESSION' : '"direction" IS NULL AND ((\"HubName\" = \'primary\' OR \"HubName\" = \'secondary\' OR \"HubName\" = \'tertiary\') AND \"HubDist\" < 11) OR ((\"HubName\" = \'residential\' OR \"HubName\" = \'unclassified\' OR \"HubName\" = \'living_street\' OR \"HubName\" = \'pedestrian\' OR \"HubName\" = \'road\') AND \"HubDist\" < 10)', 'OUTPUT': 'memory:'})['OUTPUT']

    #Wenn keine Verkehrsstraße in der Nähe, an sonstigen Wegen in der nahen Umgebung (5 Meter) ausrichten
    print(time.strftime('%H:%M:%S', time.localtime()), '   An sonstigen Wegen ausrichten...')
    layer_next_streets_points.invertSelection()
    layer_shortest_distance_lines_ways = processing.run('qgis:distancetonearesthublinetohub', { 'FIELD' : 'highway', 'HUBS' : QgsProcessingFeatureSourceDefinition(layer_next_streets_points.id(), selectedFeaturesOnly=True), 'INPUT' : layer_street_furniture, 'UNIT' : 0, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_street_furniture_ways = processing.run('native:extractspecificvertices', { 'INPUT' : layer_shortest_distance_lines_ways, 'VERTICES' : '0', 'OUTPUT': 'memory:'})['OUTPUT']
    #Objekte extrahieren, die bis zu 5 Meter von sonstigen Wegen entfernt liegen
    layer_street_furniture_ways = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_street_furniture_ways, 'EXPRESSION' : '"direction" IS NULL AND "HubDist" < 5', 'OUTPUT': 'memory:'})['OUTPUT']
    print(time.strftime('%H:%M:%S', time.localtime()), '   Verwerfe Mehrfach-Objekte...')
    #Objekte verwerfen, wenn diese bereits eine Ausrichtung zu einer Verkehrsstraße haben
    layer_street_furniture_ways = processing.run('native:extractbylocation', { 'INPUT' : layer_street_furniture_ways, 'INTERSECT' : layer_street_furniture_streets, 'PREDICATE' : [2], 'OUTPUT': 'memory:'})['OUTPUT']
    #Neu erzeugte Objekte vereinigen und originale Objekte an dieser Position ersetzen
    layer_street_furniture_oriented = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_street_furniture_streets, layer_street_furniture_ways], 'OUTPUT': 'memory:'})['OUTPUT']
    print(time.strftime('%H:%M:%S', time.localtime()), '   Vereinige ausgerichtete Straßenmöbel...')
    layer_street_furniture = processing.run('native:extractbylocation', { 'INPUT' : layer_street_furniture, 'INTERSECT' : layer_street_furniture_oriented, 'PREDICATE' : [2], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_street_furniture = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_street_furniture, layer_street_furniture_oriented], 'OUTPUT': 'memory:'})['OUTPUT']
    print(time.strftime('%H:%M:%S', time.localtime()), '   Bereinige Daten...')
    layer_street_furniture = clearAttributes(layer_street_furniture, ['id', 'man_made', 'highway', 'direction', 'angle', 'ref', 'street_cabinet', 'width', 'length', 'lamp_mount'])
    print(time.strftime('%H:%M:%S', time.localtime()), '   Speichere Daten...')
    QgsProject.instance().addMapLayer(layer_street_furniture, False)
    layer_street_furniture.selectAll()
    processing.run('native:saveselectedfeatures', { 'INPUT' : layer_street_furniture, 'OUTPUT' : proc_dir + 'street_furniture.geojson' })



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

    layer_forest = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_landuse_polygons, 'EXPRESSION' : '"landuse" = \'forest\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_wood = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_natural_polygons, 'EXPRESSION' : '"natural" = \'wood\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_forest = processing.run('native:mergevectorlayers', { 'LAYERS' : [layer_forest, layer_wood], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_forest = clearAttributes(layer_forest, ['id', 'landuse', 'natural', 'name', 'leaf_type', 'leaf_cycle'])
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
    layer_parking = QgsVectorLayer(data_dir + 'parking/parking_way.geojson|geometrytype=LineString', 'Parkstreifen', 'ogr')

    #Parkstreifen in einzelne Punkte unterteilen und diese zur Fahrzeugmitte versetzen
    layer_parking = processing.run('native:pointsalonglines', {'INPUT' : layer_parking, 'DISTANCE' : QgsProperty.fromExpression('if("vehicles" = \'bus\', 12, if("source:capacity" = \'estimated\', if("orientation" = \'diagonal\', 3.1, if("orientation" = \'perpendicular\', 2.5, 5.2)), if("capacity" = 1, $length, if($length < if("orientation" = \'diagonal\', 3.1 * "capacity", if("orientation" = \'perpendicular\', 2.5 * "capacity", (5.2 * "capacity") - 0.8)), ($length + (if("orientation" = \'parallel\', 0.8, if("orientation" = \'perpendicular\', 0.5, 0))) - (2 * if("orientation" = \'diagonal\', 1.55, if("orientation" = \'perpendicular\', 1.25, 2.6)))) / ("capacity" - 1), ($length - (2 * if("orientation" = \'diagonal\', 1.55, if("orientation" = \'perpendicular\', 1.25, 2.6)))) / ("capacity" - 1)))))'), 'START_OFFSET' : QgsProperty.fromExpression('if("vehicles" = \'bus\', 6 + (($length - (12 * "capacity")) / 2), if("source:capacity" = \'estimated\', if("orientation" = \'diagonal\', ($length - (3.1*("capacity" - 1))) / 2, if("orientation" = \'perpendicular\', ($length - (2.5*("capacity" - 1))) / 2, ($length - (5.2*("capacity" - 1))) / 2)), if("capacity" < 2, $length / 2, if("orientation" = \'diagonal\', 1.55, if("orientation" = \'perpendicular\', if($length < if("orientation" = \'diagonal\', 3.1 * "capacity", if("orientation" = \'perpendicular\', 2.5 * "capacity", (5.2 * "capacity") - 0.8)), 0.9, 1.25), if($length < if("orientation" = \'diagonal\', 3.1 * "capacity", if("orientation" = \'perpendicular\', 2.5 * "capacity", (5.2 * "capacity") - 0.8)), 2.2, 2.6))))))'), 'OUTPUT' : data_dir + 'parking/parking_way_points.geojson' })['OUTPUT']
    processing.run('native:translategeometry', {'INPUT' : layer_parking, 'DELTA_X' : QgsProperty.fromExpression('if("position" = \'on_street\' or "position" = \'street_side\' or "position" IS NULL, cos((("angle") - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)), if("position" = \'on_kerb\' or "position" = \'shoulder\', -cos((("angle") - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)), 0))'), 'DELTA_Y' : QgsProperty.fromExpression('if("position" = \'on_street\' or "position" = \'street_side\' or "position" IS NULL, sin(("angle" - 180 - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)), if("position" = \'on_kerb\' or "position" = \'shoulder\', -sin(("angle" - 180 - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)), 0))'), 'OUTPUT' : proc_dir + 'parking_way_points_processed.geojson' })
    #unbearbeitete Kopie im parking-Ordner speichern
    processing.run('native:translategeometry', {'INPUT' : layer_parking, 'DELTA_X' : QgsProperty.fromExpression('if("position" = \'on_street\' or "position" = \'street_side\' or "position" IS NULL, cos((("angle") - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)), if("position" = \'on_kerb\' or "position" = \'shoulder\', -cos((("angle") - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)), 0))'), 'DELTA_Y' : QgsProperty.fromExpression('if("position" = \'on_street\' or "position" = \'street_side\' or "position" IS NULL, sin(("angle" - 180 - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)), if("position" = \'on_kerb\' or "position" = \'shoulder\', -sin(("angle" - 180 - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)), 0))'), 'OUTPUT' : data_dir + 'parking/parking_way_points_translated.geojson' })

    layer_cars = QgsVectorLayer(proc_dir + 'parking_way_points_processed.geojson|geometrytype=Point', 'Fahrzeuge', 'ogr')
    layer_cars = clearAttributes(layer_cars, ['vehicles', 'orientation', 'oneway_direction', 'angle']) 
    QgsProject.instance().addMapLayer(layer_cars, False)
 
    #Neue Attribute für Fahrzeugmodell und Farbe anlegen
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
        vehicles = feature.attribute('vehicles')
        if vehicles == 'police':
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

    streetname_attributes = ['name', 'highway', 'dual_carriageway']
    waterway_attributes = ['name', 'waterway']

    #für Straßennamen:
    #nur Straßennetz verarbeiten
    layer_streets = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_raw_highway_ways, 'EXPRESSION' : '"highway" IS NOT \'platform\' and NOT("highway" like \'%_link\') and "highway" IS NOT NULL', 'OUTPUT': 'memory:'})['OUTPUT']

    #Straßen und Wege nach den Merkmalen Name, Klassifikation und Zweirichtungs-Fahrbahn vereinigen
    print(time.strftime('%H:%M:%S', time.localtime()), '   Straßen nach gemeinsamen Merkmalen vereinigen...')
    layer_streets = processing.run('native:dissolve', { 'FIELD' : streetname_attributes, 'INPUT' : layer_streets, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_ways = processing.run('native:dissolve', { 'FIELD' : ['name', 'highway', 'dual_carriageway'], 'INPUT' : layer_raw_path_ways, 'OUTPUT': 'memory:'})['OUTPUT']
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
    layer_streetnames = processing.run('native:dissolve', { 'FIELD' : ['name', 'highway'], 'INPUT' : layer_streetnames, 'OUTPUT': 'memory:'})['OUTPUT']
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



print(time.strftime('%H:%M:%S', time.localtime()), 'Abgeschlossen.')
