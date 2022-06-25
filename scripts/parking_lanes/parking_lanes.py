#------------------------------------------------------------------------------#
#   Parking lane analysis with OSM data                                        #
#------------------------------------------------------------------------------#
#   OSM data processing for QGIS/PyGIS to generate parking lane data.          #
#   Run this Overpass query -> https://overpass-turbo.eu/s/1jAp                #
#   and save the result at 'data/input.geojson' (or another directory, if      #
#   specified otherwise in the directory variable) before running this script. #
#                                                                              #
#   > version/date: 2022-06-25                                                 #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
#   V a r i a b l e s   a n d   S e t t i n g s                                #
#------------------------------------------------------------------------------#

from qgis.core import *
from os.path import exists
import os, processing, math, time

#working directory, see https://stackoverflow.com/a/65543293/729221
from console.console import _console
dir = _console.console.tabEditorWidget.currentWidget().path.replace("parking_lanes.py","")
dir_input = dir + 'data/input.geojson'
dir_output = dir + 'data/output/'

#coordinate reference system
#Attention: EPSG:25833 (ETRS89 / UTM zone 33N) is used here – other CRS may be necessary at other locations.
#A metric CRS is necessary to calculate with metre units and distances.
crs_from = "EPSG:4326"
crs_to = "EPSG:25833"
transform_context = QgsCoordinateTransformContext()
transform_context.addCoordinateOperation(QgsCoordinateReferenceSystem(crs_from), QgsCoordinateReferenceSystem(crs_to), "")
coordinateTransformContext=QgsProject.instance().transformContext()
save_options = QgsVectorFileWriter.SaveVectorOptions()
save_options.driverName = 'GeoJSON'
save_options.ct = QgsCoordinateTransform(QgsCoordinateReferenceSystem(crs_from), QgsCoordinateReferenceSystem(crs_to), coordinateTransformContext)

#default width of streets (if not specified more precisely on the data object)
width_minor_street = 11
width_primary_street = 17
width_secondary_street = 15
width_tertiary_street = 13
width_service = 4
width_driveway = 2.5

#default width of parking lanes (if not specified more precisely on the data object)
width_para = 2   #parallel parking -----
width_diag = 4.5 #diagonal parking /////
width_perp = 5   #perpendicular p. |||||

#parking space length / distance per vehicle depending on parking direction
#TODO: Attention: In some calculation steps that use field calculator formulas, these values are currently still hardcoded – if needed, the formulas would have to be generated as a string using these variables
car_dist_para = 5.2     #parallel parking
car_dist_diag = 3.1     #diagonal parking (angle: 60 gon = 54°)
car_dist_perp = 2.5     #perpendicular parking
car_length = 4.4        #average motor car length (a single car, without manoeuvring distance)
car_width = 1.8         #average motor car width

bus_length = 12         #average bus length – currently not in use
hgv_articulated_length = 16 #average length of semi-trailer trucks – currently not in use

#buffers/radii kept free at certain objects (meter)
buffer_driveway           = 4   #4   //free space at driveways
buffer_traffic_signals    = 10  #10  //in front of traffic lights
buffer_crossing_zebra     = 4.5 #4.5 //on zebra crossings
buffer_crossing_marked    = 2   #2   //on other marked crossings
buffer_crossing_protected = 3   #3   //on crossings protected by buffer markings, kerb extensions etc.
buffer_bus_stop           = 15  #15  //at bus stops
buffer_bus_stop_range     = 2   #2   //Distance where segments with parking lanes are searched for cutting at bus stops (must always be >= than "buffer_bus_stop")

process_lane_installations= True # If True, parking lanes are cutted at installations on the carriageway (on lane bicycle parking, parkletts...)
process_separate_areas    = True # If True, separately mapped street side and lane parking areas are included and converted into lines that fit as closely as possible
create_point_chain        = True # If True, an extra layer with points for each individual vehicle will be created from the parking lanes

#list of highway tags that do not belong to the regular road network but are also analysed
is_service_list = ['service', 'track', 'bus_guideway', 'footway', 'cycleway', 'path']

#list of attributes kept for the street layer
#Attention: Certain width specifications are also processed (fillBaseAttributes()), but they should not be specified here.
#"parking:lane:left/right:position" are new attributes for collecting the parking lane position.
#"error_output" is a new attribute to collect errors and inconsistencies
street_key_list = [
'id',
'highway',
'name',
'width_proc',
'width_proc:effective',
'surface',
'parking:lane:left',
'parking:lane:right',
'parking:lane:left:position',
'parking:lane:right:position',
'parking:lane:left:width',
'parking:lane:right:width',
'parking:lane:left:width:carriageway',
'parking:lane:right:width:carriageway',
'parking:lane:left:offset',
'parking:lane:right:offset',
'error_output'
]

#attribute keep list for parking lane layers (parking:lane:* and parking:condition:* are also stored)
#Attention: In prepareLayers(), specifications are prefixed with "highway:" to clarify the attribute as a road property.
parking_key_list = [
'id',
'highway',
'name',
'width_proc',
'width_proc:effective',
'error_output'
]


#------------------------------------------------------------------------------#
#   V a r i a b l e s   E n d                                                  #
#------------------------------------------------------------------------------#



def clearAttributes(layer, attributes):
#-------------------------------------------------------------------------------
# Deletes unnecessary attributes.
#-------------------------------------------------------------------------------
# > layer: The layer to be cleaned up.
# > attributes: List of attributes that should be kept.
#-------------------------------------------------------------------------------
    attr_count = len(layer.attributeList())
    delete_list = []
    for id in range(0, attr_count):
        if not layer.attributeDisplayName(id) in attributes:
            delete_list.append(layer.attributeDisplayName(id))
    layer = processing.run('qgis:deletecolumn', { 'INPUT' : layer, 'COLUMN' : delete_list, 'OUTPUT': 'memory:'})['OUTPUT']
    return(layer)



def prepareLayers():
#-------------------------------------------------------------------------------
# Read input file, process and interpolate street and parking lane data
# and provide separate layers for further processing:
# (1) street layer (esp. for rendering),
# (2) service way layer (esp. for processing of driveways)
# (3) parking lane (left side of the road)
# (4) parking lane (right side of the road)
# (5) point layer for crossing processing etc.
# (6) polygon layer for processing of separately mapped lane- and street side parking
#-------------------------------------------------------------------------------
    print(time.strftime('%H:%M:%S', time.localtime()), 'Read data...')
    if not exists(dir_input):
        print(time.strftime('%H:%M:%S', time.localtime()), '[!] Error: Found no valid input at "' + dir_input + '".')
        return False
    layer_lines = QgsVectorLayer(dir_input + '|geometrytype=LineString', 'input line data', 'ogr')
    layer_points = QgsVectorLayer(dir_input + '|geometrytype=Point', 'input point data', 'ogr')
    if(process_separate_areas or process_lane_installations):
        layer_polygons = QgsVectorLayer(dir_input + '|geometrytype=Polygon', 'input polygon data', 'ogr')
    else:
        layer_polygons = NULL

    print(time.strftime('%H:%M:%S', time.localtime()), 'Reproject layers...')
    layer_lines = processing.run('native:reprojectlayer', { 'INPUT' : layer_lines, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_points = processing.run('native:reprojectlayer', { 'INPUT' : layer_points, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']
    if layer_polygons is not NULL:
        layer_polygons = processing.run('native:reprojectlayer', { 'INPUT' : layer_polygons, 'TARGET_CRS' : QgsCoordinateReferenceSystem(crs_to), 'OUTPUT': 'memory:'})['OUTPUT']

    #Straßen- und Parkstreifenattribute vorbereiten
    print(time.strftime('%H:%M:%S', time.localtime()), 'Prepare street data...')
    layer_lines = fillBaseAttributes(layer_lines)
    layer_street = clearAttributes(layer_lines, street_key_list)
    expr_street = expr_service = ''
    expr_connect = 0
    for cat in is_service_list:
        if expr_connect:
            expr_street += ' AND '
            expr_service += ' OR '
        else:
            expr_connect = 1
        expr_street += '"highway" IS NOT \'' + cat + '\''
        expr_service += '"highway" IS \'' + cat + '\''
    layer_service = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_street, 'EXPRESSION' : expr_service, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_street = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_street, 'EXPRESSION' : expr_street, 'OUTPUT': 'memory:'})['OUTPUT']

    QgsProject.instance().addMapLayer(layer_street, False)
    group_streets.insertChildNode(0, QgsLayerTreeLayer(layer_street))
    QgsProject.instance().addMapLayer(layer_service, False)
    group_streets.insertChildNode(0, QgsLayerTreeLayer(layer_service))

    #Parkstreifen separat vorbereiten
    print(time.strftime('%H:%M:%S', time.localtime()), 'Prepare parking lane data (clean attributes)...')
    attr_list = []
    for id in range(0, len(layer_lines.attributeList())):
        attr_name = layer_lines.attributeDisplayName(id)
        if attr_name in parking_key_list or 'parking:lane' in attr_name or 'parking:condition' in attr_name:
            attr_list.append(attr_name)
    layer_parking_lanes = clearAttributes(layer_lines, attr_list)

    #exclude service ways without parking lane information
    print(time.strftime('%H:%M:%S', time.localtime()), 'Prepare parking lane data (split up sides)...')
    expr_both = expr_street + ' OR ((' + expr_service + ') AND ("parking:lane:left" IS NOT NULL OR "parking:lane:right" IS NOT NULL))'
    layer_parking_lanes = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_parking_lanes, 'EXPRESSION' : expr_both, 'OUTPUT': 'memory:'})['OUTPUT']

    #keep some street attributes in new attributes with prefix
    QgsProject.instance().addMapLayer(layer_parking_lanes, False)
    with edit(layer_parking_lanes):
        for attr in parking_key_list:
            if attr != 'id' and attr != 'highway' and attr != 'error_output':
                layer_parking_lanes.renameAttribute(layer_parking_lanes.fields().indexOf(attr), 'highway:' + attr)

    #split up left and right parking lane layer
    expr_left = expr_street + ' OR ((' + expr_service + ') AND "parking:lane:left" IS NOT NULL)'
    expr_right = expr_street + ' OR ((' + expr_service + ') AND "parking:lane:right" IS NOT NULL)'
    layer_parking_left = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_parking_lanes, 'EXPRESSION' : expr_left, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking_right = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_parking_lanes, 'EXPRESSION' : expr_right, 'OUTPUT': 'memory:'})['OUTPUT']

    #prepare parking lane attributes
    layer_parking_left = prepareParkingLane(layer_parking_left, 'left', True)
    layer_parking_right = prepareParkingLane(layer_parking_right, 'right', True)

    return([layer_street, layer_service, layer_parking_left, layer_parking_right, layer_points, layer_polygons])



def fillBaseAttributes(layer):
#-------------------------------------------------------------------------------
# Get base attributes for streets like width information and
# get left and right parking lane attributes.
#-------------------------------------------------------------------------------
# > layer: layer with street and parking lane information.
#-------------------------------------------------------------------------------
    layer.startEditing()

    #Breiten- und Parkstreifenattribute anlegen, falls diese nicht existieren
    for attr in ['width_proc', 'width_proc:effective', 'parking:lane:left', 'parking:lane:right', 'parking:lane:left:position', 'parking:lane:right:position', 'parking:lane:left:width', 'parking:lane:right:width', 'parking:lane:left:width:carriageway', 'parking:lane:right:width:carriageway', 'parking:lane:left:offset', 'parking:lane:right:offset', 'error_output']:
        if layer.fields().indexOf(attr) == -1:
            layer.dataProvider().addAttributes([QgsField(attr, QVariant.String)])
    layer.updateFields()

    id_width = layer.fields().indexOf('width_proc')
    id_width_effective = layer.fields().indexOf('width_proc:effective')
    id_parking_left = layer.fields().indexOf('parking:lane:left')
    id_parking_right = layer.fields().indexOf('parking:lane:right')
    id_parking_left_position = layer.fields().indexOf('parking:lane:left:position')
    id_parking_right_position = layer.fields().indexOf('parking:lane:right:position')
    id_parking_left_width = layer.fields().indexOf('parking:lane:left:width')
    id_parking_right_width = layer.fields().indexOf('parking:lane:right:width')
    id_parking_left_width_carriageway = layer.fields().indexOf('parking:lane:left:width:carriageway')
    id_parking_right_width_carriageway = layer.fields().indexOf('parking:lane:right:width:carriageway')
    id_parking_left_offset = layer.fields().indexOf('parking:lane:left:offset')
    id_parking_right_offset = layer.fields().indexOf('parking:lane:right:offset')
    id_error = layer.fields().indexOf('error_output')

    if layer.fields().indexOf('parking:lane:both') + id_parking_left + id_parking_right == -3:
        print(time.strftime('%H:%M:%S', time.localtime()), 'NOTE: Input dataset ("' + dir_input + '") does not contain parking lane information ("parking:lane:*")!')

    #Basisattribute ermitteln
    id_width = layer.fields().indexOf('width_proc')
    wd = layer.fields().indexOf('width')
    wd_car = layer.fields().indexOf('width:carriageway')
    wd_est = layer.fields().indexOf('est_width')
    constr = layer.fields().indexOf('construction')
    for feature in layer.getFeatures():
        error = ''

        #Parkausrichtung ermitteln (Längs-, Schräg-, Querparken)
        parking_left = feature.attribute('parking:lane:left')
        parking_right = feature.attribute('parking:lane:right')
        if layer.fields().indexOf('parking:lane:both') != -1:
            parking_orientation = feature.attribute('parking:lane:both')
            if parking_orientation != NULL:
                if parking_left == NULL:
                    parking_left = parking_orientation
                    layer.changeAttributeValue(feature.id(), id_parking_left, parking_orientation)
                else:
                    error += '[pl01l] Attribute "parking:lane:left" und "parking:lane:both" gleichzeitig vorhanden. '
                if parking_right == NULL:
                    parking_right = parking_orientation
                    layer.changeAttributeValue(feature.id(), id_parking_right, parking_orientation)
                else:
                    error += '[pl01r] Attribute "parking:lane:right" und "parking:lane:both" gleichzeitig vorhanden. '
            else:
                if (not parking_left or not parking_right) and feature.attribute('highway') not in is_service_list:
                    error += '[no_pl] Parkstreifeninformation nicht für alle Seite vorhanden. '
        else:
            if (not parking_left or not parking_right) and feature.attribute('highway') not in is_service_list:
                error += '[no_pl] Parkstreifeninformation nicht für alle Seite vorhanden. '

        #Parkposition ermitteln (insbes. Straßen-/Bordsteinparken)
        for side in ['left', 'right']:
            position = NULL
            if side == 'left':
                parking_orientation = parking_left
            else:
                parking_orientation = parking_right
            if parking_orientation:
                dir_side = 'parking:lane:' + side + ':' + parking_orientation in layer.attributeAliases()
                dir_both = 'parking:lane:both:' + parking_orientation in layer.attributeAliases()

                if dir_side:
                    position = feature.attribute('parking:lane:' + side + ':' + parking_orientation)
                if dir_both:
                    if position and feature.attribute('parking:lane:both:' + parking_orientation):
                        error += '[pl02' + side[:1] + '] Attribute "parking:lane:' + side + ':' + parking_orientation +'" und "parking:lane:both:' + parking_orientation + '" gleichzeitig vorhanden. '
                    if not position:
                        position = feature.attribute('parking:lane:both:' + parking_orientation)

                if side == 'left':
                    parking_left_position = position
                    layer.changeAttributeValue(feature.id(), id_parking_left_position, position)
                else:
                    parking_right_position = position
                    layer.changeAttributeValue(feature.id(), id_parking_right_position, position)

        parking_left_width = 0; parking_right_width = 0
        if parking_left or parking_right:
            #Parkstreifenbreite ermitteln
            if layer.fields().indexOf('parking:lane:left:width') != -1:
                parking_left_width = feature.attribute('parking:lane:left:width')
            if layer.fields().indexOf('parking:lane:right:width') != -1:
                parking_right_width = feature.attribute('parking:lane:right:width')
            if layer.fields().indexOf('parking:lane:both:width') != -1:
                parking_width = feature.attribute('parking:lane:both:width')
                if parking_width != NULL:
                    if parking_left_width == NULL:
                        parking_left_width = parking_width
                        layer.changeAttributeValue(feature.id(), id_parking_left_width, parking_width)
                    else:
                        error += '[pl03l] Attribute "parking:lane:left:width" und "parking:lane:both:width" gleichzeitig vorhanden. '
                    if parking_right_width == NULL:
                        parking_right_width = parking_width
                        layer.changeAttributeValue(feature.id(), id_parking_right_width, parking_width)
                    else:
                        error += '[pl03r] Attribute "parking:lane:right:width" und "parking:lane:both:width" gleichzeitig vorhanden. '
            #Parkstreifenbreite aus Parkrichtung abschätzen, wenn nicht genauer angegeben
            if parking_left_width == NULL:
                parking_left_width = 0
                if parking_left == 'parallel':
                    parking_left_width = width_para
                if parking_left == 'diagonal':
                    parking_left_width = width_diag
                if parking_left == 'perpendicular':
                    parking_left_width = width_perp

            if parking_right_width == NULL:
                parking_right_width = 0
                if parking_right == 'parallel':
                    parking_right_width = width_para
                if parking_right == 'diagonal':
                    parking_right_width = width_diag
                if parking_right == 'perpendicular':
                    parking_right_width = width_perp

            layer.changeAttributeValue(feature.id(), id_parking_left_width, parking_left_width)
            layer.changeAttributeValue(feature.id(), id_parking_right_width, parking_right_width)

        #Fahrbahnbreite ermitteln
        width = NULL
        #Mögliche vorhandene Breitenattribute prüfen: width:carriageway, width, est_width
        if wd_car != -1:
            width = feature.attribute('width:carriageway')
        if width == NULL and wd != -1 :
            width = feature.attribute('width')
        if width == NULL and wd_est != -1:
            width = feature.attribute('est_width')

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
            highway = feature.attribute('highway')
            if highway == 'primary':
                width = width_primary_street
            if highway == 'secondary':
                width = width_secondary_street
            if highway == 'tertiary':
                width = width_tertiary_street
            if highway in is_service_list:
                width = width_service
                if layer.fields().indexOf('service') != -1:
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
                    if construction in is_service_list:
                        width = width_service

            if width == NULL:
                width = width_minor_street
        layer.changeAttributeValue(feature.id(), id_width, width)

        #Offset der Parkstreifen für spätere Verschiebung ermitteln (offset-Linie liegt am Bordstein)
        parking_left_width_carriageway = 0
        parking_right_width_carriageway = 0
        if parking_left in ['parallel', 'diagonal', 'perpendicular']:
            parking_left_width_carriageway = parking_left_width
            if parking_left_position == 'half_on_kerb':
                parking_left_width_carriageway = parking_left_width_carriageway / 2
            if parking_left_position in ['on_kerb', 'shoulder', 'lay_by', 'street_side']:
                parking_left_width_carriageway = 0
        if parking_right in ['parallel', 'diagonal', 'perpendicular']:
            parking_right_width_carriageway = parking_right_width
            if parking_right_position == 'half_on_kerb':
                parking_right_width_carriageway = parking_right_width_carriageway / 2
            if parking_right_position in ['on_kerb', 'shoulder', 'lay_by', 'street_side']:
                parking_right_width_carriageway = 0

        width_pl = parking_left_width
        if not width_pl:
            width_pl = 0
        width_pr = parking_right_width
        if not width_pr:
            width_pr = 0

        width_effective = float(width) - float(parking_left_width_carriageway) - float(parking_right_width_carriageway)
        parking_left_offset = (width_effective / 2) + float(parking_left_width_carriageway)
        parking_right_offset = -(width_effective / 2) - float(parking_right_width_carriageway)

# Archivierte Berechnung für eine offset-Linie in der Mitte der tatsächlichen Parkspur
#        parking_left_offset = (width_effective / 2) + (float(width_pl) / 2)
#        parking_right_offset = -(width_effective / 2) - (float(width_pr) / 2)

        layer.changeAttributeValue(feature.id(), id_width_effective, width_effective)
        layer.changeAttributeValue(feature.id(), id_parking_left_width_carriageway, parking_left_width_carriageway)
        layer.changeAttributeValue(feature.id(), id_parking_right_width_carriageway, parking_right_width_carriageway)
        layer.changeAttributeValue(feature.id(), id_parking_left_offset, parking_left_offset)
        layer.changeAttributeValue(feature.id(), id_parking_right_offset, parking_right_offset)

        #Mögliche Fehlermeldungen in Attribut speichern
        if error == '':
            error = NULL
        layer.changeAttributeValue(feature.id(), id_error, error)

    layer.updateFields()
    layer.commitChanges()

    return(layer)



def prepareParkingLane(layer, side, clean):
#-------------------------------------------------------------------------------
# Converts parking lane attributes for both directions into separate,
# grouped attributes.
#-------------------------------------------------------------------------------
# > layer: The layer for which the parking lane information is to be aggregated.
# > side:  ('left' or 'right'): Side of the street that is represented by the layer.
# > clean: (True or False): Clean up attribute table after processing?
#-------------------------------------------------------------------------------

    id_left = layer.fields().indexOf('parking:lane:left')
    id_right = layer.fields().indexOf('parking:lane:right')

    layer.startEditing()

    #Neue Attribute für Parkstreifeninformationen erstellen und deren ID's zur späteren Bearbeitung ermitteln
    for attr in ['side', 'parking', 'orientation', 'position', 'condition', 'condition:other', 'condition:other:time', 'vehicles', 'maxstay', 'capacity', 'source:capacity', 'width', 'offset']:
        if layer.fields().indexOf(attr) == -1:
            layer.dataProvider().addAttributes([QgsField(attr, QVariant.String)])
    layer.updateFields()

    id_id = layer.fields().indexOf('id')
    id_side = layer.fields().indexOf('side')
    id_parking = layer.fields().indexOf('parking')
    id_parking_orientation = layer.fields().indexOf('orientation')
    id_parking_position = layer.fields().indexOf('position')
    id_parking_condition = layer.fields().indexOf('condition')
    id_parking_condition_other = layer.fields().indexOf('condition:other')
    id_parking_condition_other_time = layer.fields().indexOf('condition:other:time')
    id_parking_vehicles = layer.fields().indexOf('vehicles')
    id_parking_maxstay = layer.fields().indexOf('maxstay')
    id_parking_capacity = layer.fields().indexOf('capacity')
    id_parking_source_capacity = layer.fields().indexOf('source:capacity')
    id_parking_width = layer.fields().indexOf('width')
    id_parking_offset = layer.fields().indexOf('offset')
    id_error = layer.fields().indexOf('error_output')

    cond_side = 'parking:condition:'+side in layer.attributeAliases()
    cond_both = 'parking:condition:both' in layer.attributeAliases()
    cond_default_side = 'parking:condition:'+side+':default' in layer.attributeAliases()
    cond_default_both = 'parking:condition:both:default' in layer.attributeAliases()
    cond_time_side = 'parking:condition:'+side+':time_interval' in layer.attributeAliases()
    cond_time_both = 'parking:condition:both:time_interval' in layer.attributeAliases()
    vehicles_side = 'parking:condition:'+side+':vehicles' in layer.attributeAliases()
    vehicles_both = 'parking:condition:both:vehicles' in layer.attributeAliases()
    maxstay_side = 'parking:condition:'+side+':maxstay' in layer.attributeAliases()
    maxstay_both = 'parking:condition:both:maxstay' in layer.attributeAliases()
    capacity_side = 'parking:lane:'+side+':capacity' in layer.attributeAliases()
    capacity_both = 'parking:lane:both:capacity' in layer.attributeAliases()

    #Straßenabschnitte einzeln durchgehen und Parkstreifeninformationen zusammenfassend auslesen
    for feature in layer.getFeatures():
        parking = NULL
        parking_orientation = NULL
        parking_position = NULL
        parking_condition = NULL
        parking_condition_other = NULL
        parking_condition_other_time = NULL
        parking_vehicles = NULL
        parking_maxstay = NULL
        parking_capacity = NULL
        parking_source_capacity = NULL
        parking_width = NULL
        parking_offset = NULL

        #Relevante parkstreifenseitige Fehlermeldungen übernehmen, falls vorhanden
        error = feature.attribute('error_output')
        error_new = ''
        if error != NULL:
            for i in range(1, 4):
                error_code = '[pl0' + str(i) + side[:1] + ']'
                if error_code in error:
                    f_string = error[error.find(error_code):]
                    if not '[' in f_string[1:]:
                        error_new += f_string
                    else:
                        f_stop = f_string[1:].find('[') + 1
                        error_new += f_string[:f_stop]
        error = error_new

        readable_attributes = ['parking:lane:both', 'parking:lane:'+side, 'parking:lane:'+side+':capacity', 'parking:lane:both:capacity', 'parking:lane:'+side+':width', 'parking:lane:both:width', 'parking:lane:'+side+':width:carriageway', 'parking:lane:'+side+':position', 'parking:lane:'+side+':offset', 'parking:condition:'+side, 'parking:condition:both', 'parking:condition:'+side+':default', 'parking:condition:both:default', 'parking:condition:'+side+':time_interval', 'parking:condition:both:time_interval', 'parking:condition:'+side+':vehicles', 'parking:condition:both:vehicles', 'parking:condition:'+side+':maxstay', 'parking:condition:both:maxstay']

        #Parkstreifeninfos auslesen (entweder aus left/right-Tagging oder aus both-Tagging)
        if side == 'left' and id_left != -1:
            parking_orientation = feature.attribute('parking:lane:left')
        if side == 'right' and id_right != -1:
            parking_orientation = feature.attribute('parking:lane:right')

        #Segmente ohne Parkplätze löschen
        parking_list = ['parallel', 'diagonal', 'perpendicular', 'marked']
        if parking_orientation in parking_list:
            parking_source_capacity = 'estimated'
        else:
            parking_source_capacity = NULL
            parking_orientation = NULL

        parking_offset = feature.attribute('parking:lane:' + side + ':offset')

        #Parkstreifen-Ausrichtung und Breite übernehmen
        parking_position = feature.attribute('parking:lane:' + side + ':position')
        if parking_position == 'lay_by' or parking_position == 'street_side':
            parking = 'street_side'
        elif parking_position:
            parking = 'lane'
        else:
            parking_side = feature.attribute('parking:lane:' + side)
            if parking_side == 'separate' or parking_side == 'no':
                parking = parking_side
            else:
                parking = 'unknown'
            parking_position = NULL

        parking_width = feature.attribute('parking:lane:' + side + ':width')
        if parking_orientation:
            readable_attributes.append('parking:lane:' + side + ':' + parking_orientation)
            readable_attributes.append('parking:lane:both:' + parking_orientation)

        #Parkstreifen-Regeln (und Abweichungen) ermitteln (kostenfrei, Ticket, Halte-/Parkverbote zu bestimmten Zeiten...)
        if cond_default_side:
            parking_condition_default = feature.attribute('parking:condition:' + side + ':default')
        else:
            parking_condition_default = NULL
        if cond_default_both:
            if parking_condition_default and feature.attribute('parking:condition:both:default'):
                error += '[pc01' + side[:1] + '] Attribute "parking:condition:' + side + ':default" und "parking:condition:both:default" gleichzeitig vorhanden. '
            if not parking_condition_default:
                parking_condition_default = feature.attribute('parking:condition:both:default')

        if not parking_condition_default:
            if cond_side:
                parking_condition = feature.attribute('parking:condition:' + side)
            if cond_both:
                if parking_condition and feature.attribute('parking:condition:both'):
                    error += '[pc02' + side[:1] + '] Attribute "parking:condition:' + side + '" und "parking:condition:both" gleichzeitig vorhanden. '
                if not parking_condition:
                    parking_condition = feature.attribute('parking:condition:both')
        else:
            parking_condition = parking_condition_default
            if cond_side:
                cond = feature.attribute('parking:condition:' + side)
            if cond_both:
                if cond and feature.attribute('parking:condition:both'):
                    error += '[pc02' + side[:1] + '] Attribute "parking:condition:' + side + '" und "parking:condition:both" gleichzeitig vorhanden. '
                if not cond:
                    cond = feature.attribute('parking:condition:both')

            #Mögliche conditional-Schreibweisen auflösen - Achtung, fehleranfällig, wenn andere conditions als Zeitangaben verwendet werden!
            if cond:
                if not '@' in cond:
                    parking_condition_other = cond
                else:
                    pos = cond.find('@')
                    if cond[pos - 1] == ' ':
                        cond_ = cond[:pos - 1]
                    else:
                        cond_ = cond[:pos]
                    time = cond[pos + 1:]
                    if time[0] == ' ':
                        time = time[1:]
                    if time[0] == '(':
                        time = time[1:len(time)-1]

                    parking_condition_other = cond_
                    parking_condition_other_time = time

#        #Segmente löschen, an denen ausschließlich Park- und Halteverbot besteht
#        if parking_condition == 'no_parking' and parking_condition_other == 'no_stopping' or parking_condition == 'no_stopping' and parking_condition_other == 'no_parking':
#            layer.deleteFeature(feature.id())
#            continue

        if cond_time_side:
            if parking_condition_other_time and feature.attribute('parking:condition:' + side + ':time_interval'):
                error += '[pc03' + side[:1] + '] Zeitliche Parkbeschränkung sowohl im conditional-restrictions- als auch im parking:lane:' + side + ':time_interval-Schema vorhanden. '
            parking_condition_other_time_set = feature.attribute('parking:condition:' + side + ':time_interval')
        else:
            parking_condition_other_time_set = NULL
        if cond_time_both:
            if parking_condition_other_time_set and feature.attribute('parking:condition:both:time_interval'):
                error += '[pc04' + side[:1] + '] Attribute "parking:condition:' + side + ':time_interval" und "parking:condition:both:time_interval" gleichzeitig vorhanden. '
            if not parking_condition_other_time_set:
                parking_condition_other_time_set = feature.attribute('parking:condition:both:time_interval')
        if not parking_condition_other_time:
            parking_condition_other_time = parking_condition_other_time_set

        if maxstay_side:
            parking_maxstay = feature.attribute('parking:condition:' + side + ':maxstay')
        if maxstay_both:
            if parking_maxstay and feature.attribute('parking:condition:both:maxstay'):
                error += '[pc05' + side[:1] + '] Attribute "parking:condition:' + side + ':maxstay" und "parking:condition:both:maxstay" gleichzeitig vorhanden. '
            if not parking_maxstay:
                parking_maxstay = feature.attribute('parking:condition:both:maxstay')

        if capacity_side:
            parking_capacity = feature.attribute('parking:lane:' + side + ':capacity')
        if capacity_both:
            if parking_capacity and feature.attribute('parking:lane:both:capacity'):
                error += '[pc06' + side[:1] + '] Attribute "parking:lane:' + side + ':capacity" und "parking:lane:both:capacity" gleichzeitig vorhanden. '
            if not parking_capacity:
                parking_capacity = feature.attribute('parking:lane:both:capacity')
        if parking_capacity != NULL:
            parking_source_capacity = 'OSM'

        if vehicles_side:
            parking_vehicles = feature.attribute('parking:condition:' + side + ':vehicles')
        if vehicles_both:
            if parking_vehicles and feature.attribute('parking:condition:both:vehicles'):
                error += '[pc07' + side[:1] + '] Attribute "parking:condition:' + side + ':vehicles" und "parking:condition:both:vehicles" gleichzeitig vorhanden. '
            if not parking_vehicles:
                parking_vehicles = feature.attribute('parking:condition:both:vehicles')

        #Nicht berücksichtigte, spezielle parking:lane-Attribute erkennen und ausgeben
        for attr in layer.attributeAliases():
            if 'parking:lane' in attr or 'parking:condition' in attr:
                if side == 'left':
                    if not 'right' in attr and not attr in readable_attributes:
                        if feature.attribute(attr):
                            error += '[ig_al] Attribut "' + attr + '" nicht berücksichtigt. '
                elif side == 'right':
                    if not 'left' in attr and not attr in readable_attributes:
                        if feature.attribute(attr):
                            error += '[ig_ar] Attribut "' + attr + '" nicht berücksichtigt. '

        #ermittelte Parkstreifeninformationen in die Attributtabelle des Straßenabschnitts übertragen
        layer.changeAttributeValue(feature.id(), id_side, side)
        layer.changeAttributeValue(feature.id(), id_parking, parking)
        layer.changeAttributeValue(feature.id(), id_parking_orientation, parking_orientation)
        layer.changeAttributeValue(feature.id(), id_parking_position, parking_position)
        layer.changeAttributeValue(feature.id(), id_parking_condition, parking_condition)
        layer.changeAttributeValue(feature.id(), id_parking_condition_other, parking_condition_other)
        layer.changeAttributeValue(feature.id(), id_parking_condition_other_time, parking_condition_other_time)
        layer.changeAttributeValue(feature.id(), id_parking_vehicles, parking_vehicles)
        layer.changeAttributeValue(feature.id(), id_parking_maxstay, parking_maxstay)
        layer.changeAttributeValue(feature.id(), id_parking_capacity, parking_capacity)
        layer.changeAttributeValue(feature.id(), id_parking_source_capacity, parking_source_capacity)
        layer.changeAttributeValue(feature.id(), id_parking_width, parking_width)
        layer.changeAttributeValue(feature.id(), id_parking_offset, parking_offset)

        #mögliche Fehlermeldungen dokumentieren
        if error == '':
            error = NULL
        layer.changeAttributeValue(feature.id(), id_error, error)
    layer.commitChanges()

    #Abschließend bei Bedarf nicht mehr benötigte parking:lane-Attribute entfernen
    if clean:
        attr_list = []
        for id in range(0, len(layer.attributeList())):
            attr_name = layer.attributeDisplayName(id)
            if not 'parking:lane' in attr_name and not 'parking:condition' in attr_name:
                attr_list.append(attr_name)
        layer = clearAttributes(layer, attr_list)

    return(layer)



def getIntersections(layer, method):
#-------------------------------------------------------------------------------
#   ---(Funktion derzeit ungenutzt)---
#-------------------------------------------------------------------------------
# Ermittelt Straßenkreuzungen.
#-------------------------------------------------------------------------------
# > layer: Der Layer, für den die Kreuzungen ermittelt werden sollen.
# > method: ('full', 'fast') Die Berechnungsmethode, mit der
# vorgegangen wird.
#   > 'full': Ermittelt alle Schnittpunkte des Straßenlayers mit
#     sich selbst, an denen mehr als zwei Segmente zusammentreffen.
#     Vollständige, aber rechenaufwendige Methode.
#   > 'fast': Wesentlich schnellere Variante, bei der mit einem
#     nach Straßennamen aufgelösten Straßenlayer gerechnet wird.
#     In Einzelfällen können hierbei jedoch Kreuzungen fehlen,
#     wenn die sich kreuzenden Straßen den selben Namen tragen.
#-------------------------------------------------------------------------------

    if method != 'fast':
        # Straßen in Einzelteile zerlegen, um die Anzahl abgehender Wege sicher für jede Kreuzung ermitteln zu können
        expl_street = processing.run('native:explodelines', {'INPUT' : layer, 'OUTPUT': 'memory:'})['OUTPUT']

        # Kreuzungspunkte inklusive zahlreicher Pseudo-Nodes ermitteln
        intersections = processing.run('native:lineintersections', {'INPUT' : expl_street, 'INTERSECT' : expl_street, 'OUTPUT': dir_output + 'buffer_points/intersections.geojson'})['OUTPUT']

        intersections = QgsProject.instance().addMapLayer(QgsVectorLayer(dir_output + 'buffer_points/intersections.geojson', 'Straßenkreuzungen', 'ogr'))
        intersections.startEditing()

        # Variable für Breitenangabe der Kreuzung bereithalten
        intersections.dataProvider().addAttributes([QgsField('intersection_width', QVariant.String)])
        intersections.updateFields()
        id_width = intersections.fields().indexOf('intersection_width')

        for feature in intersections.getFeatures():
            # Punkte einzeln durchgehen und identische Punkte auswählen
            intersections.removeSelection()
            intersections.select(feature.id())
            processing.run('native:selectbylocation', {'INPUT' : intersections, 'INTERSECT' : QgsProcessingFeatureSourceDefinition(dir_output + 'buffer_points/intersections.geojson', selectedFeaturesOnly=True, featureLimit=-1, geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid), 'PREDICATE' : [3]})

            # Befinden sich nur 2 Punkte an einem Ort: Pseudo-Node löschen
            if intersections.selectedFeatureCount() < 3:
                intersections.deleteSelectedFeatures()
                continue

            # Ansonsten Kreuzungsbreite ermitteln und Mehrfachpunkte löschen
            width = 0
            del_features = []
            for sel_feature in intersections.selectedFeatures():
                feat_width = sel_feature.attribute('width_proc')
                if float(feat_width) > width:
                    width = float(feat_width)
            intersections.deselect(feature.id())
            intersections.deleteSelectedFeatures()

            intersections.changeAttributeValue(feature.id(), id_width, width)
    else:
        # schnelle, aber ungenaue Variante: Straßenlayer nach "name" auflösen und Schnittpunkte ermitteln
        layer_diss = processing.run('native:dissolve', {'FIELD' : ['name'], 'INPUT': layer, 'OUTPUT': 'memory:'})['OUTPUT']
        intersections = processing.run('native:lineintersections', {'INPUT' : layer_diss, 'INTERSECT' : layer_diss, 'OUTPUT': 'memory:'})['OUTPUT']
        intersections = processing.run('native:deleteduplicategeometries', { 'INPUT' : intersections, 'OUTPUT': 'memory:'})['OUTPUT']

        QgsProject.instance().addMapLayer(intersections)
        intersections.startEditing()

        # Breitenangabe für Kreuzung ermitteln
        intersections.dataProvider().addAttributes([QgsField('intersection_width', QVariant.String)])
        intersections.updateFields()
        id_width = intersections.fields().indexOf('intersection_width')
        for feature in intersections.getFeatures():
            width = max([float(feature.attribute('width_proc')), float(feature.attribute('width_proc_2'))])
            intersections.changeAttributeValue(feature.id(), id_width, width)

    intersections.commitChanges()
    return(intersections)



def getKerbIntersections(layer):
#-------------------------------------------------------------------------------
# Determines the intersection points of kerbs in junction areas.
#-------------------------------------------------------------------------------
# > layer: The layer for which the intersections are to be determined.
#-------------------------------------------------------------------------------

    #Zunächst kurze Unterbrechungen an Kreuzungen erzeugen, um fehlerhafte Schnittpunkte (bei leichten Kurven) nach Versatz zu vermeiden
    layer_diss_streets = layer
    #layer_diss_streets = processing.run('native:dissolve', {'FIELD' : ['name','parking:lane:left:offset','parking:lane:right:offset'], 'INPUT': layer, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_streets_intersect = processing.run('native:lineintersections', {'INPUT' : layer_diss_streets, 'INTERSECT' : layer_diss_streets, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_streets_intersect_buffer = processing.run('native:buffer', {'DISTANCE' : 0.1, 'INPUT' : layer_streets_intersect, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_streets_diff = processing.run('native:difference', {'INPUT' : layer_diss_streets, 'OVERLAY' : layer_streets_intersect_buffer, 'OUTPUT': 'memory:'})['OUTPUT']

    #Bordsteinlinien durch Versatz simulieren
    layer_kerb_left = processing.run('native:offsetline', {'INPUT': layer_streets_diff, 'DISTANCE' : QgsProperty.fromExpression('"parking:lane:left:offset"'), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_kerb_right = processing.run('native:offsetline', {'INPUT': layer_streets_diff, 'DISTANCE' : QgsProperty.fromExpression('"parking:lane:right:offset"'), 'OUTPUT': 'memory:'})['OUTPUT']

    #QgsProject.instance().addMapLayer(layer_kerb_left)
    #QgsProject.instance().addMapLayer(layer_kerb_right)

    #Schnittpunkte aller Linien bestimmen
    layer_streets_intersect1 = processing.run('native:lineintersections', {'INPUT' : layer_kerb_left, 'INTERSECT' : layer_kerb_right, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_streets_intersect2 = processing.run('native:lineintersections', {'INPUT' : layer_kerb_left, 'INTERSECT' : layer_kerb_left, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_streets_intersect3 = processing.run('native:lineintersections', {'INPUT' : layer_kerb_right, 'INTERSECT' : layer_kerb_right, 'OUTPUT': 'memory:'})['OUTPUT']

    layer_streets_intersect = processing.run('native:mergevectorlayers', {'LAYERS' : [layer_streets_intersect1,layer_streets_intersect2,layer_streets_intersect3], 'OUTPUT': 'memory:'})['OUTPUT']

    QgsProject.instance().addMapLayer(layer_streets_intersect, False)
    group_buffer.insertChildNode(0, QgsLayerTreeLayer(layer_streets_intersect))
    layer_streets_intersect.setName('kerb intersection points')
    layer_streets_intersect.loadNamedStyle(dir + 'styles/kerb_intersections.qml')

    return(layer_streets_intersect)



def bufferIntersection(layer_parking, layer_intersect, buffer, buffer_name, intersects):
#-------------------------------------------------------------------------------
# Remove parts from parking lanes if a way (road, driveway,...) joins/cross.
#-------------------------------------------------------------------------------
# > layer_parking: The affected parking lane layer.
# > layer_intersect: The layer with intersecting ways.
# > buffer: Expression/formula to determine the radius to be kept free
# > buffer_name: If specified, the created buffer will be
#   added to the map with this name.
# > intersects (optional): If a point layer is given here,
#   it will be buffered instead of the intersections
#   from the first two layers.
#-------------------------------------------------------------------------------

    if not intersects:
        intersects = processing.run('native:lineintersections', {'INPUT' : layer_parking, 'INTERSECT' : layer_intersect, 'OUTPUT': 'memory:'})['OUTPUT']
    intersects_buffer = processing.run('native:buffer', {'DISTANCE' : QgsProperty.fromExpression(buffer), 'INPUT' : intersects, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking = processing.run('native:difference', {'INPUT' : layer_parking, 'OVERLAY' : intersects_buffer, 'OUTPUT': 'memory:'})['OUTPUT']

    if buffer_name:
        QgsProject.instance().addMapLayer(intersects_buffer, False)
        group_buffer.insertChildNode(0, QgsLayerTreeLayer(intersects_buffer))
        intersects_buffer.loadNamedStyle(dir + 'styles/buffer_dashed.qml')
        intersects_buffer.setName(buffer_name)

    return(layer_parking)



def bufferCrossing(layer_parking, layer_points, side):
#-------------------------------------------------------------------------------
# Removes parts from parking lane layer in the area of esp. crossings where
# the roadway is kept clear for crossing pedestrian traffic.
#-------------------------------------------------------------------------------
# > layer_parking: The affected parking lane layer.
# > layer_points: Layer with point data for crossings, traffic lights, etc.
# > side: The affected side of the street (left, right or both)
#-------------------------------------------------------------------------------
# Buffer radii:
#    highway = traffic_signals                   -> 10 m
#        traffic_signals:direction=forward: remove on right side only
#        traffic_signals:direction=backward: remove on left side only
#        !traffic_signals:direction: remove on both sides
#    crossing = marked                           -> 2 m
#    crossing = zebra OR crossing_ref = zebra    -> 4.5 m (4 m for zebra and 5 m in front according to german law)
#    crossing:buffer_marking                     -> 3 m
#        both: remove on both sides
#        left/right remove on one side only
#    crossing:kerb_extension                     -> 3 m
#        both: remove on both sides
#        left/right remove on one side only
#-------------------------------------------------------------------------------

    #Übergänge nach gemeinsamen Kriterien/Radien auswählen und Teilpuffer (mit Radius x) ziehen:
    #Vor Lichtzeichenanlagen/Ampeln 10 Meter Halteverbot (StVO) - beidseitig berücksichtigen, wenn Ampel nicht fahrtrichtungsabhängig erfasst ist
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_points, 'EXPRESSION' : '\"highway\" = \'traffic_signals\' AND \"traffic_signals:direction\" IS NOT \'forward\' AND \"traffic_signals:direction\" IS NOT \'backward\''})
    buffer01 = processing.run('native:buffer', {'DISTANCE' : buffer_traffic_signals, 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_points.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']
    #...oder nur von einer Seite abziehen, wenn die Ampel fahrtrichtungsabhängig erfasst ist
    if side == 'left':
        processing.run('qgis:selectbyexpression', {'INPUT' : layer_points, 'EXPRESSION' : '\"highway\" = \'traffic_signals\' AND \"traffic_signals:direction\" = \'backward\''})
    if side == 'right':
        processing.run('qgis:selectbyexpression', {'INPUT' : layer_points, 'EXPRESSION' : '\"highway\" = \'traffic_signals\' AND \"traffic_signals:direction\" = \'forward\''})
    buffer_s01 = processing.run('native:buffer', {'DISTANCE' : buffer_traffic_signals, 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_points.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']

    #An Gehwegvorstreckungen oder markierten Übergangs-Sperrflächen: 3 Meter
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_points, 'EXPRESSION' : '\"crossing:kerb_extension\" = \'both\' OR \"crossing:buffer_marking\" = \'both\' OR \"crossing:buffer_protection\" = \'both\''})
    buffer02 = processing.run('native:buffer', {'DISTANCE' : buffer_crossing_protected, 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_points.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']
    #...oder nur von einer Seite abziehen, falls nur einseitig vorhanden
    if side == 'left':
        processing.run('qgis:selectbyexpression', {'INPUT' : layer_points, 'EXPRESSION' : '\"crossing:kerb_extension\" = \'left\' OR \"crossing:buffer_marking\" = \'left\' OR \"crossing:buffer_protection\" = \'left\''})
    if side == 'right':
        processing.run('qgis:selectbyexpression', {'INPUT' : layer_points, 'EXPRESSION' : '\"crossing:kerb_extension\" = \'right\' OR \"crossing:buffer_marking\" = \'right\' OR \"crossing:buffer_protection\" = \'right\''})
    buffer_s02 = processing.run('native:buffer', {'DISTANCE' : buffer_crossing_protected, 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_points.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']

    #An Fußgängerüberwegen/Zebrastreifen: 4,5 Meter (4 Meter Zebrastreifenbreite sowie laut StVO 5 Meter Parkverbot davor)
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_points, 'EXPRESSION' : '\"crossing\" = \'zebra\' OR \"crossing_ref\" = \'zebra\' OR \"crossing\" = \'traffic_signals\''})
    buffer03 = processing.run('native:buffer', {'DISTANCE' : buffer_crossing_zebra, 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_points.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']

    #An sonstigen markierten Überwegen: 2 Meter
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_points, 'EXPRESSION' : '\"crossing\" = \'marked\''})
    buffer04 = processing.run('native:buffer', {'DISTANCE' : buffer_crossing_marked, 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_points.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']

    #verschiedene Teilpuffer zusammenführen und von Parkstreifen abziehen
    buffer = processing.run('native:mergevectorlayers', {'LAYERS' : [buffer01,buffer02,buffer03,buffer04], 'OUTPUT': 'memory:'})['OUTPUT']
    buffer_s = processing.run('native:mergevectorlayers', {'LAYERS' : [buffer_s01,buffer_s02], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking = processing.run('native:difference', {'INPUT' : layer_parking, 'OVERLAY' : buffer, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking = processing.run('native:difference', {'INPUT' : layer_parking, 'OVERLAY' : buffer_s, 'OUTPUT': 'memory:'})['OUTPUT']

    #Puffer anzeigen
    if side == 'left':
        QgsProject.instance().addMapLayer(buffer, False)
        group_buffer.insertChildNode(0, QgsLayerTreeLayer(buffer))
        buffer.loadNamedStyle(dir + 'styles/buffer_dashed.qml')
        buffer.setName('pedestrian crossings')

        QgsProject.instance().addMapLayer(buffer_s, False)
        group_buffer.insertChildNode(0, QgsLayerTreeLayer(buffer_s))
        buffer_s.loadNamedStyle(dir + 'styles/buffer_dashed_left.qml')
        buffer_s.setName('crossings/traffic signals (left)')
    if side == 'right':
        QgsProject.instance().addMapLayer(buffer_s, False)
        group_buffer.insertChildNode(0, QgsLayerTreeLayer(buffer_s))
        buffer_s.loadNamedStyle(dir + 'styles/buffer_dashed_right.qml')
        buffer_s.setName('crossings/traffic signals (right)')

    return(layer_parking)



def bufferBusStop(layer_parking, layer_points, layer_virtual_kerb):
#-------------------------------------------------------------------------------
# Removes parts from parking lane layers in the area of bus stops (buffer
# radius 15 meter according to german law).
#-------------------------------------------------------------------------------
# > layer_parking: The affected parking lane layer.
# > layer_points: Layer with bus stops (OSM nodes: highway=bus_stop).
# > layer_virtual_kerb: Snap bus stops to this geometries.
#-------------------------------------------------------------------------------

    #extract bus stops from point input
    layer_bus_stops = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_points, 'EXPRESSION' : '"highway" = \'bus_stop\'', 'OUTPUT': 'memory:'})['OUTPUT']

    #merge offset road segments with and without parking lanes and snap bus stops to closest line
    layer_bus_stops_snapped = processing.run('native:snapgeometries', { 'BEHAVIOR' : 1, 'INPUT' : layer_bus_stops, 'REFERENCE_LAYER' : layer_virtual_kerb, 'TOLERANCE' : 8, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_bus_stops_snapped = processing.run('native:joinbynearest', {'INPUT': layer_bus_stops_snapped, 'INPUT_2' : layer_virtual_kerb, 'FIELDS_TO_COPY' : ['highway:name','side'], 'PREFIX' : 'parking_lane:', 'MAX_DISTANCE' : buffer_bus_stop_range, 'NEIGHBORS' : 1, 'OUTPUT': 'memory:'})['OUTPUT']

    #buffer bus stops that are on or very near to road segments with parking lanes
    #(assume that there is no need to buffer bus stops at road segments without parking lanes because impact of bus stop is still mapped)
    #therefore: create small buffer for bus stops and extract all features intersecting with parking lane segments
    layer_bus_stops_buffer_range = processing.run('native:buffer', {'DISTANCE' : buffer_bus_stop_range, 'INPUT' : layer_bus_stops_snapped, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_bus_stops_buffer_range_snapped = processing.run('native:extractbylocation', { 'INPUT' : layer_bus_stops_buffer_range, 'INTERSECT' : layer_parking, 'PREDICATE' : [0], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_bus_stops_buffer = processing.run('native:buffer', {'DISTANCE' : buffer_bus_stop - buffer_bus_stop_range, 'INPUT' : layer_bus_stops_buffer_range_snapped, 'OUTPUT': 'memory:'})['OUTPUT']
    QgsProject.instance().addMapLayer(layer_bus_stops_buffer, False)

    #for every single bus stop:
    for bus_stop in layer_bus_stops_buffer.getFeatures():
        layer_bus_stops_buffer.removeSelection()
        layer_bus_stops_buffer.select(bus_stop.id())
        #extract all nearby parking lanes with same street name and side tag as the road segment the bus stop was snapped to
        layer_parking_intersect = processing.run('native:extractbylocation', {'INPUT' : layer_parking, 'INTERSECT' : QgsProcessingFeatureSourceDefinition(layer_bus_stops_buffer.id(), selectedFeaturesOnly=True), 'PREDICATE' : [0,6], 'OUTPUT': 'memory:'})['OUTPUT']

        layer_parking_intersect.startEditing()
        for parking_lane in layer_parking_intersect.getFeatures():
            #cut only segments with same street name...
            if parking_lane.attribute('highway:name') != bus_stop.attribute('parking_lane:highway:name'):
                layer_parking_intersect.deleteFeature(parking_lane.id())
                continue
            #...and on same side of the street
            if parking_lane.attribute('side') != bus_stop.attribute('parking_lane:side'):
                layer_parking_intersect.deleteFeature(parking_lane.id())

        layer_parking_intersect.commitChanges()

        #reduce parking lanes to segments outside this bus stop buffer, cut the segments inside this bus stop buffer and merge both layers again
        processing.run('native:selectbylocation', {'INPUT' : layer_parking, 'INTERSECT' : layer_parking_intersect, 'PREDICATE' : [3]})
        with edit(layer_parking):
            layer_parking.deleteSelectedFeatures()
        layer_parking_intersect = processing.run('native:difference', {'INPUT' : layer_parking_intersect, 'OVERLAY' : QgsProcessingFeatureSourceDefinition(layer_bus_stops_buffer.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']
        layer_parking = processing.run('native:mergevectorlayers', {'LAYERS' : [layer_parking, layer_parking_intersect], 'OUTPUT': 'memory:'})['OUTPUT']

    #add all bus stops to buffer folder
    QgsProject.instance().addMapLayer(layer_bus_stops, False)
    group_buffer.insertChildNode(0, QgsLayerTreeLayer(layer_bus_stops))
    layer_bus_stops.loadNamedStyle(dir + 'styles/buffer_bus_stop.qml')
    layer_bus_stops.setName('bus stops')

    return(layer_parking)



def processLaneInstallations(layer_parking, layer_polygons, layer_virtual_kerb):
#-------------------------------------------------------------------------------
# Cut parking lane segments at installations on the carriageway
# (bicycle parking, parkletts...)
#-------------------------------------------------------------------------------
# > layer_parking: The affected parking lane layer.
# > layer_polygons: The layer containing installations of interest (see below)
# > layer_virtual_kerb: Snap installations of interest to this geometries.
#-------------------------------------------------------------------------------
# > installations of interest:
# amenity=bicycle_parking + bicycle_parking:position=lane
# amenity=bicycle_parking + bicycle_parking:position=street_side
# amenity=small_vehicle_parking + small_vehicle_parking:position=lane
# amenity=small_vehicle_parking + small_vehicle_parking:position=street_side
# leisure=parklet
# leisure=outdoor_seating + outdoor_seating=parklet
#-------------------------------------------------------------------------------

    #extract installations of interest from polygon input
    layer_installations = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_polygons, 'EXPRESSION' : '("amenity" = \'bicycle_parking\' AND "bicycle_parking:position" = \'lane\') OR ("amenity" = \'bicycle_parking\' AND "bicycle_parking:position" = \'street_side\') OR ("amenity" = \'small_vehicle_parking\' AND "small_vehicle_parking:position" = \'lane\') OR ("amenity" = \'small_vehicle_parking\' AND "small_vehicle_parking:position" = \'street_side\') OR "leisure" = \'parklet\' OR ("leisure" = \'outdoor_seating\' and "outdoor_seating" = \'parklet\')', 'OUTPUT': 'memory:'})['OUTPUT']
    #convert to lines and snap installations outlines to nearby parking lanes
    layer_installations = processing.run('native:polygonstolines', { 'INPUT' : layer_installations, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_installations = processing.run('native:snapgeometries', { 'BEHAVIOR' : 1, 'INPUT' : layer_installations, 'REFERENCE_LAYER' : layer_virtual_kerb, 'TOLERANCE' : 10, 'OUTPUT': 'memory:'})['OUTPUT']
    #buffer lines with rectangular shape
    layer_installations = processing.run('native:buffer', {'INPUT' : layer_installations, 'DISTANCE' : 2, 'END_CAP_STYLE' : 1, 'JOIN_STYLE' : 2, 'MITER_LIMIT' : 2, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking = processing.run('native:difference', {'INPUT' : layer_parking, 'OVERLAY' : layer_installations, 'OUTPUT': 'memory:'})['OUTPUT']
    #add buffer to map
    QgsProject.instance().addMapLayer(layer_installations, False)
    group_buffer.insertChildNode(0, QgsLayerTreeLayer(layer_installations))
    layer_installations.loadNamedStyle(dir + 'styles/buffer_dashed.qml')
    layer_installations.setName('on lane installations')
    #return cutted parking lane layer
    return(layer_parking)



def processSeparateParkingAreas(layer_parking, layer_polygons, layer_virtual_kerb):
#-------------------------------------------------------------------------------
# Converts separately mapped street side parking areas and parking lanes
# into line segments similar to street side parking lanes mapped on the
# street/highway line.
#-------------------------------------------------------------------------------
# > layer_parking: The affected parking lane layer.
# > layer_polygons: Layer with separately mapped parking areas.
# > layer_virtual_kerb: "Virtual kerb" layer (highway line offset by
#   carriageway width) to distinguish inner and outer parking area lines.
#-------------------------------------------------------------------------------

    #extract separately mapped parking areas from polygon input
    layer_parking_areas = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_polygons, 'EXPRESSION' : '"amenity" = \'parking\' AND ("parking" = \'street_side\' OR "parking" = \'lane\')', 'OUTPUT': 'memory:'})['OUTPUT']
    #convert parking bay polygons into lines
    layer_parking_lines = processing.run('native:polygonstolines', { 'INPUT' : layer_parking_areas, 'OUTPUT': 'memory:'})['OUTPUT']
    #explode both line layers in single segments and get line directions/angles for every segment
    layer_parking_lines = processing.run('native:explodelines', { 'INPUT' : layer_parking_lines, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_kerb = processing.run('native:explodelines', { 'INPUT' : layer_virtual_kerb, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking_lines = processing.run('qgis:fieldcalculator', { 'INPUT': layer_parking_lines, 'FIELD_NAME': 'proc_line_angle', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 6, 'FIELD_PRECISION': 3, 'NEW_FIELD': True, 'FORMULA': 'line_interpolate_angle($geometry,0)', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_kerb = processing.run('qgis:fieldcalculator', { 'INPUT': layer_kerb, 'FIELD_NAME': 'proc_line_angle', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 6, 'FIELD_PRECISION': 3, 'NEW_FIELD': True, 'FORMULA': 'line_interpolate_angle($geometry,0)', 'OUTPUT': 'memory:'})['OUTPUT']
    #atopt line angle of the nearest street segment at every parking area outline segment
    layer_parking_lines = processing.run('native:joinbynearest', {'INPUT': layer_parking_lines, 'INPUT_2' : layer_kerb, 'FIELDS_TO_COPY' : ['highway','highway:name','proc_line_angle'], 'PREFIX' : 'highway:', 'MAX_DISTANCE' : 15, 'NEIGHBORS' : 1, 'OUTPUT': 'memory:'})['OUTPUT']
    #ignore line segments whose angle deviates significantly from the angle of the road to create 'inner' and 'outer' lines
    #outer line represents the virtual kerb the parking lane is located/rendered at
    #inner line is needed for interpolate the parking orientation if not mapped
    layer_parking_lines_outer = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_parking_lines, 'EXPRESSION' : 'abs("proc_line_angle" - "highway:proc_line_angle") < 25', 'OUTPUT': 'memory:'})['OUTPUT']
    #dissolve line segments with same id (= line segments of the same parking area)
    layer_parking_lines_outer = processing.run('native:dissolve', { 'FIELD' : ['id'], 'INPUT' : layer_parking_lines_outer, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking_lines_outer = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_parking_lines_outer, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking_lines_outer = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_parking_lines_outer, 'EXPRESSION' : '$length > 1.7', 'OUTPUT': 'memory:'})['OUTPUT']

    #clean up and synchronize attributes
    layer = layer_parking_lines_outer
    parking_areas_attribute_list = [
    'id',
    'side',
    'parking',
    'highway',
    'highway:name',
    'orientation',
    'position',
    'condition',
    'condition:other',
    'condition:other:time',
    'vehicles',
    'maxstay',
    'capacity',
    'source:capacity'
    ]

    #create same attributes as in parking lane layer
    layer.startEditing()
    for attr in parking_areas_attribute_list:
        if layer.fields().indexOf(attr) == -1:
            layer.dataProvider().addAttributes([QgsField(attr, QVariant.String)])
    layer.updateFields()

    id_side = layer.fields().indexOf('side')
    id_highway = layer.fields().indexOf('highway')
    id_highway_name = layer.fields().indexOf('highway:name')
    id_orientation = layer.fields().indexOf('orientation')
    id_position = layer.fields().indexOf('position')
    id_condition = layer.fields().indexOf('condition')
    id_condition_other = layer.fields().indexOf('condition:other')
    id_condition_other_time = layer.fields().indexOf('condition:other:time')
    id_vehicles = layer.fields().indexOf('vehicles')
    id_source_capacity = layer.fields().indexOf('source:capacity')

    orientation_dict_distance = {}

    #translate attributes from polygon
    for feature in layer.getFeatures():
        highway = NULL
        highway_name = NULL
        orientation = NULL
        position = NULL
        condition = NULL
        condition_other = NULL
        condition_other_time = NULL
        vehicles = NULL

        #side
        side = 'separate' #TODO: pick real side from virtual kerb segment and use separate_left/separate_right?
        #highway
        if layer.fields().indexOf('parking:street_side:of') != -1:
            highway = feature.attribute('parking:street_side:of')
        if not highway:
            highway = feature.attribute('highway:highway')
        #highway:name
        if layer.fields().indexOf('parking:street_side:of:name') != -1:
            highway_name = feature.attribute('parking:street_side:of:name')
        if not highway_name:
            highway_name = feature.attribute('highway:highway:name')
        #TODO if not highway_name: pick highway name from virtual kerb segment
        #orientation
        if layer.fields().indexOf('parking:orientation') != -1:
            orientation = feature.attribute('parking:orientation')
        if not orientation:
            #interpolate orientation from disance between inner and outer line
            if not orientation_dict_distance:
                #extract inner lines without orientation attribute
                layer_parking_lines_inner = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_parking_lines, 'EXPRESSION' : '(abs("proc_line_angle" - ("highway:proc_line_angle" - 180)) < 25 or abs("proc_line_angle" - ("highway:proc_line_angle" + 180)) < 25) and "parking:orientation" is NULL', 'OUTPUT': 'memory:'})['OUTPUT']

                #derive orientation by distance between inner and outer line, store values for each id in a dict
                orientation_dict_distance = getOrientationDictByDistance(layer_parking_lines_inner, layer_parking_lines_outer)
                #TODO: alternative method: calculate capacity by area, derive orientation by density of parking cars along representing line of the area

            if feature.attribute('id') in orientation_dict_distance.keys():
                orientation = orientation_dict_distance[feature.attribute('id')]
            else:
                print(time.strftime('%H:%M:%S', time.localtime()), '   [!] Note: Calculating orientation for ' + feature.attribute('id') + ' failed. Assumed parallel parking.')
                orientation = 'parallel'
        #position
        if layer.fields().indexOf('parking:position') != -1:
            position = feature.attribute('parking:position')
        if not position:
            if feature.attribute('parking') == 'lane':
                position = 'on_street'
            else:
                position = 'street_side'
        #condition
        if layer.fields().indexOf('access') != -1:
            access = feature.attribute('access')
            if access == 'yes':
                condition = 'free'
            else:
                condition = access
        #condition:other
        if layer.fields().indexOf('access:conditional') != -1:
            condition_other = feature.attribute('access:conditional')
        #condition:other:time   #TODO: separate access:conditional (* @ and @ *)
        #vehicles               #TODO: taxi=designated -> 'taxi' etc.
        #capacity: separate function, see below
        #source:capacity
        if feature.attribute('capacity'):
            source_capacity = 'OSM'
        else:
            source_capacity = 'estimated'

        layer.changeAttributeValue(feature.id(), id_side, side)
        layer.changeAttributeValue(feature.id(), id_highway, highway)
        layer.changeAttributeValue(feature.id(), id_highway_name, highway_name)
        layer.changeAttributeValue(feature.id(), id_orientation, orientation)
        layer.changeAttributeValue(feature.id(), id_position, position)
        layer.changeAttributeValue(feature.id(), id_condition, condition)
        layer.changeAttributeValue(feature.id(), id_condition_other, condition_other)
        layer.changeAttributeValue(feature.id(), id_condition_other_time, condition_other_time)
        layer.changeAttributeValue(feature.id(), id_vehicles, vehicles)
        layer.changeAttributeValue(feature.id(), id_source_capacity, source_capacity)

    layer.updateFields()
    layer.commitChanges()

    #delete unused attributes
    layer = clearAttributes(layer, parking_areas_attribute_list)

    return(layer)



def getOrientationDictByDistance(layer_parking_lines_inner, layer_parking_lines_outer):
#-------------------------------------------------------------------------------
# Interpolate parking orientation of a separately mapped street side parking
# area (without orientation attribute) by calculating the median distance
# between the inner and the outer outline.
# Assume parallel parking if distance < 4,25m, perpendicular parking if
# distance > 4,75m, and diagonal parking if distance between 4.25-4,75m.
#-------------------------------------------------------------------------------
# > layer_parking_lines_inner: Layer containing the inner lines (the line
#   parallel and next to the street).
# > layer_parking_lines_outer: Layer containing the outer lines (the line
#   parallel and next to the kerb).
#-------------------------------------------------------------------------------

    print(time.strftime('%H:%M:%S', time.localtime()), 'Interpolate missing orientation values...')
    orientation_dict_distance = {}

    #dissolve line segments with same id (= line segments of the same parking area)
    layer_parking_lines_inner = processing.run('native:dissolve', { 'FIELD' : ['id'], 'INPUT' : layer_parking_lines_inner, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking_lines_inner = processing.run('native:multiparttosingleparts', { 'INPUT' : layer_parking_lines_inner, 'OUTPUT': 'memory:'})['OUTPUT']
    #create a reference line with distance of 4.5m to inner line
    layer_reference_line = processing.run('native:offsetline', {'INPUT': layer_parking_lines_inner, 'DISTANCE' : 4.5, 'OUTPUT': 'memory:'})['OUTPUT']
    #extract outer lines without orientation attribute
    layer_chain = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_parking_lines_outer, 'EXPRESSION' : '"parking:orientation" is NULL', 'OUTPUT': 'memory:'})['OUTPUT']
    #create a point chain along the outer line
    layer_chain = processing.run('native:pointsalonglines', {'INPUT' : layer_chain, 'DISTANCE' : 2, 'START_OFFSET' : 1, 'OUTPUT': 'memory:'})['OUTPUT']
    #snap point chain to 4.5m reference line

    #TODO: snap only to line with same ID

    layer_snap_chain = processing.run('native:snapgeometries', { 'BEHAVIOR' : 1, 'INPUT' : layer_chain, 'REFERENCE_LAYER' : layer_reference_line, 'TOLERANCE' : 8, 'OUTPUT': 'memory:'})['OUTPUT']
    #get distance for every point pair
    layer_hub_lines = processing.run('qgis:distancetonearesthublinetohub', { 'INPUT' : layer_chain, 'HUBS' : layer_snap_chain, 'FIELD' : 'id', 'UNIT' : 0, 'OUTPUT': 'memory:'})['OUTPUT']
    #get angle of hub line
    layer_hub_lines = processing.run('qgis:fieldcalculator', { 'INPUT': layer_hub_lines, 'FIELD_NAME': 'connecting_angle', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 6, 'FIELD_PRECISION': 3, 'NEW_FIELD': True, 'FORMULA': 'line_interpolate_angle($geometry,0)', 'OUTPUT': 'memory:'})['OUTPUT']
    #get offset angle, exclude values without right angle (these are points that couldn't be snapped directly to the line)
    #use negative distance values for distances > 4.5m, poitive values for distances < 4.5m
    layer_hub_lines = processing.run('qgis:fieldcalculator', { 'INPUT': layer_hub_lines, 'FIELD_NAME': 'offset_distance', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 6, 'FIELD_PRECISION': 3, 'NEW_FIELD': True, 'FORMULA': 'if(abs(abs(if("proc_line_angle" - "connecting_angle" < 0, "proc_line_angle" - "connecting_angle" + 180, "proc_line_angle" - "connecting_angle" - 180)) - 90) < 5, if(if("proc_line_angle" - "connecting_angle" < 0, "proc_line_angle" - "connecting_angle" + 180, "proc_line_angle" - "connecting_angle" - 180) < 0, -"HubDist", "HubDist"), NULL)', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_hub_lines = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_hub_lines, 'EXPRESSION' : '"offset_distance" is not NULL', 'OUTPUT': 'memory:'})['OUTPUT']
    #get median distance for each OSM-feature by it's id
    layer_hub_lines = processing.run('qgis:fieldcalculator', { 'INPUT': layer_hub_lines, 'FIELD_NAME': 'offset_median', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 6, 'FIELD_PRECISION': 3, 'NEW_FIELD': True, 'FORMULA': 'median("offset_distance",group_by:="id")', 'OUTPUT': 'memory:'})['OUTPUT']

    for hub_line in layer_hub_lines.getFeatures():
        id = hub_line.attribute('id')
        if not id in orientation_dict_distance.keys():
            offset = hub_line.attribute('offset_median')
            #no or large offset? invalid value.
            if offset != 0 and (not offset or abs(offset) > 3):
                orientation_dict_distance[id] = NULL
            elif abs(offset) < 0.25:
                orientation_dict_distance[id] = 'diagonal'
            elif offset <= -0.25:
                orientation_dict_distance[id] = 'perpendicular'
            else:
                orientation_dict_distance[id] = 'parallel'

    return(orientation_dict_distance)



def getCapacity(layer):
#-------------------------------------------------------------------------------
# Removes line segments from parking lane layers if they are too short for
# parking (space for less than one vehicle) and adds/corrects capacity
# attributes (depending on parking orientation).
#-------------------------------------------------------------------------------
# > layer: The layer for which the segments are to be checked.
#-------------------------------------------------------------------------------

    layer.startEditing()
    id_capacity = layer.fields().indexOf('capacity')
    car_diag_width = math.sqrt(car_width * 0.5 * car_width) + math.sqrt(car_length * 0.5 * car_length)
#Korrektur/Verbesserung: Bei Einstellwinkel 60 gon = 54 Grad: car_length * sin (36 Grad) + car_width * cos(36 Grad) = 4.04 Meter
    for feature in layer.getFeatures():
        orientation = feature.attribute('orientation')
        capacity = feature.attribute('capacity')
        geom = feature.geometry()
        length = geom.length()

        has_capacity = False
        if capacity != NULL:
            has_capacity = True

        if orientation == 'parallel':
            #Wenn Segment zu kurz für ein Fahrzeug: löschen
            if length < car_length:
                layer.deleteFeature(feature.id())
                continue
            elif capacity == NULL:
                #Anzahl Parkplätze ergibt sich aus Segmentlänge - abzüglich eines Ragierabstands zwischen zwei Fahrzeugen, der an einem der beiden Enden des Segments nicht benötigt wird
                capacity = math.floor((length + (car_dist_para - car_length)) / car_dist_para)
                layer.changeAttributeValue(feature.id(), id_capacity, capacity)
        elif orientation == 'diagonal':
            if length < car_width:
                layer.deleteFeature(feature.id())
                continue
            elif capacity == NULL:
                capacity = math.floor((length + (car_dist_diag - car_diag_width)) / car_dist_diag)
                layer.changeAttributeValue(feature.id(), id_capacity, capacity)
        elif orientation == 'perpendicular':
            if length < car_width:
                layer.deleteFeature(feature.id())
                continue
            elif capacity == NULL:
                capacity = math.floor((length + (car_dist_perp - car_width)) / car_dist_perp)
                layer.changeAttributeValue(feature.id(), id_capacity, capacity)

        if capacity == NULL:
            layer.changeAttributeValue(feature.id(), id_capacity, 0)

        #Schnittfehler bei Segmenten mit gegebener Stellplatzzahl korrigieren
        #(vorgegebene capacity auf Segmente aufteilen, falls sie geteilt wurden)
        if has_capacity:
            id = feature.attribute('id')
            length_sum = 0
            for other_feature in layer.getFeatures('"id" = \'' + id + '\''):
                other_geom = other_feature.geometry()
                length_sum += other_geom.length()
            if length < length_sum:
                capacity_single = round((length / length_sum) * int(capacity))
                layer.changeAttributeValue(feature.id(), id_capacity, capacity_single)
                if capacity_single == 0:
                    layer.deleteFeature(feature.id())

    layer.updateFields()
    layer.commitChanges()
    return(layer)



#------------------------------------------------------------------------------#
#      S c r i p t   S t a r t                                                 #
#------------------------------------------------------------------------------#

#create necessary directories if not existing
need_dir = [dir_output]
for d in need_dir:
    if not os.path.exists(d):
        os.makedirs(d)

#create layer groups
group_parking = QgsProject.instance().layerTreeRoot().addGroup('parking')
group_buffer = QgsProject.instance().layerTreeRoot().addGroup('buffer')
group_buffer.setExpanded(False)
group_streets = QgsProject.instance().layerTreeRoot().addGroup('streets')
group_streets.setExpanded(False)

#prepare layers with specific data (streets, parking lanes, pedestrian crossings)
layers = prepareLayers()
if layers:
    layer_street = layers[0]
    layer_service = layers[1]
    layer_parking_left = layers[2]
    layer_parking_right = layers[3]
    layer_points = layers[4]
    layer_polygons = layers[5]

    #create "virtual kerb" layer where parking lanes are located later for snapping features that affect parking
    if process_separate_areas or buffer_bus_stop or process_lane_installations:
        layer_virtual_kerb_left = processing.run('native:offsetline', {'INPUT': layer_parking_left, 'DISTANCE' : QgsProperty.fromExpression('"offset"'), 'OUTPUT': 'memory:'})['OUTPUT']
        layer_virtual_kerb_left = processing.run('native:reverselinedirection', {'INPUT': layer_virtual_kerb_left, 'OUTPUT': 'memory:'})['OUTPUT']
        layer_virtual_kerb_right = processing.run('native:offsetline', {'INPUT': layer_parking_right, 'DISTANCE' : QgsProperty.fromExpression('"offset"'), 'OUTPUT': 'memory:'})['OUTPUT']
        layer_virtual_kerb = processing.run('native:mergevectorlayers', {'LAYERS' : [layer_virtual_kerb_left, layer_virtual_kerb_right], 'OUTPUT': 'memory:'})['OUTPUT']

    layer_street.loadNamedStyle(dir + 'styles/street_simple.qml')
    layer_service.loadNamedStyle(dir + 'styles/street_simple.qml')

    #separate and bundle parking lane attributes to a left and a right layer
    print(time.strftime('%H:%M:%S', time.localtime()), 'Processing parking lane data...')

    #connect adjoining parking lane segments with same properties
    #TODO Warning: Can possibly lead to faults if two segments with opposite directions but the same properties meet.
    layer_parking_left = processing.run('native:dissolve', {'INPUT': layer_parking_left, 'FIELD' : ['highway:name','parking','orientation','position','condition','condition:other','condition:other:time','vehicles','maxstay','capacity','width','offset'], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking_right = processing.run('native:dissolve', {'INPUT': layer_parking_right, 'FIELD' : ['highway:name','parking','orientation','position','condition','condition:other','condition:other:time','vehicles','maxstay','capacity','width','offset'], 'OUTPUT': 'memory:'})['OUTPUT']

    #calculate angles at pedestrian crossings (for rendering and spatial calculations)
    layer_vertices = processing.run('native:extractvertices', {'INPUT': layer_street, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_points = processing.run('native:joinattributesbylocation', {'INPUT': layer_points, 'JOIN' : layer_vertices, 'JOIN_FIELDS' : ['angle'], 'OUTPUT': 'memory:'})['OUTPUT']
    #also apply street width
    layer_points = processing.run('native:joinattributesbylocation', {'INPUT': layer_points, 'JOIN' : layer_street, 'JOIN_FIELDS' : ['width_proc', 'parking:lane:right:width:carriageway', 'parking:lane:left:width:carriageway'], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_points = QgsProject.instance().addMapLayer(layer_points, False)

    #store road segments without parking lanes separately
    layer_no_parking_left = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_parking_left, 'EXPRESSION' : '"parking" IS \'no\' OR "parking" IS \'separate\' OR "parking" IS \'unknown\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking_left = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_parking_left, 'EXPRESSION' : '"parking" IS NOT \'no\' AND "parking" IS NOT \'separate\' AND "parking" IS NOT \'unknown\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_no_parking_right = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_parking_right, 'EXPRESSION' : '"parking" IS \'no\' OR "parking" IS \'separate\' OR "parking" IS \'unknown\'', 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking_right = processing.run('qgis:extractbyexpression', { 'INPUT' : layer_parking_right, 'EXPRESSION' : '"parking" IS NOT \'no\' AND "parking" IS NOT \'separate\' AND "parking" IS NOT \'unknown\'', 'OUTPUT': 'memory:'})['OUTPUT']

    #keep parking lanes free in the area of pedestrian crossings (before offset, because affects both sides)
    layer_parking_left = bufferCrossing(layer_parking_left, layer_points, 'left')
    layer_parking_right = bufferCrossing(layer_parking_right, layer_points, 'right')

    #offset parking lanes according to the lane width
    print(time.strftime('%H:%M:%S', time.localtime()), 'Offset parking lane data...')
    layer_parking_left = processing.run('native:offsetline', {'INPUT': layer_parking_left, 'DISTANCE' : QgsProperty.fromExpression('"offset"'), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking_right = processing.run('native:offsetline', {'INPUT': layer_parking_right, 'DISTANCE' : QgsProperty.fromExpression('"offset"'), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_no_parking_left = processing.run('native:offsetline', {'INPUT': layer_no_parking_left, 'DISTANCE' : QgsProperty.fromExpression('"offset"'), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_no_parking_right = processing.run('native:offsetline', {'INPUT': layer_no_parking_right, 'DISTANCE' : QgsProperty.fromExpression('"offset"'), 'OUTPUT': 'memory:'})['OUTPUT']

    #merge left and right parking lane layers (reverse left side line direction before)
    layer_parking_left = processing.run('native:reverselinedirection', {'INPUT': layer_parking_left, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking = processing.run('native:mergevectorlayers', {'LAYERS' : [layer_parking_left,layer_parking_right], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_no_parking_left = processing.run('native:reverselinedirection', {'INPUT': layer_no_parking_left, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_no_parking = processing.run('native:mergevectorlayers', {'LAYERS' : [layer_no_parking_left, layer_no_parking_right], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_no_parking = processing.run('qgis:deletecolumn', {'INPUT' : layer_no_parking, 'COLUMN' : ['path'], 'OUTPUT': 'memory:'})['OUTPUT']

    #include separately mapped parking areas and convert them to lines
    if process_separate_areas:
        print(time.strftime('%H:%M:%S', time.localtime()), 'Include separately mapped parking areas...')
        layer_parking_separate = processSeparateParkingAreas(layer_parking, layer_polygons, layer_virtual_kerb)
    #keep parking lanes free in the area of bus stops
    if buffer_bus_stop:
        print(time.strftime('%H:%M:%S', time.localtime()), 'Processing bus stops...')
        layer_parking = bufferBusStop(layer_parking, layer_points, layer_virtual_kerb)
    #cut segments at installations on the carriageway (bicycle parking, parkletts...)
    if process_lane_installations:
        print(time.strftime('%H:%M:%S', time.localtime()), 'Processing installations on lane...')
        layer_parking = processLaneInstallations(layer_parking, layer_polygons, layer_virtual_kerb)
    #TODO cut lowered kerbs
    #TODO cut buffers from objects that affect on_kerb/half_on_kerb/shoulder/street_side parking

    QgsProject.instance().addMapLayer(layer_parking, False)

    #separately cut off parking lanes on service roads near the intersection area
    #Select service roads with parking lane information, determine intersections with roads and buffer these by the width of the road + 5 metre distance
    print(time.strftime('%H:%M:%S', time.localtime()), 'Processing intersection/driveway zones...')
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_service, 'EXPRESSION' : ' \"parking:lane:left\" IS NOT NULL OR \"parking:lane:right\" IS NOT NULL'})
    intersects = processing.run('native:lineintersections', {'INPUT' : QgsProcessingFeatureSourceDefinition(layer_service.id(), selectedFeaturesOnly=True), 'INTERSECT' : layer_street, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_service.removeSelection()
    intersects_buffer = processing.run('native:buffer', {'DISTANCE' : QgsProperty.fromExpression('("width_proc_2" / 2) + 5'), 'INPUT' : intersects, 'OUTPUT': 'memory:'})['OUTPUT']
    #add buffer to map
    QgsProject.instance().addMapLayer(intersects_buffer, False)
    group_buffer.insertChildNode(0, QgsLayerTreeLayer(intersects_buffer))
    intersects_buffer.loadNamedStyle(dir + 'styles/buffer_dashed.qml')
    intersects_buffer.setName('shorten service roads')
    #cut the buffers just created from the parking lanes belonging to service roads
    processing.run('qgis:selectbyattribute', {'FIELD' : 'highway', 'INPUT' : layer_parking, 'VALUE' : 'service'})
    layer_parking_service = processing.run('native:difference', {'INPUT' : QgsProcessingFeatureSourceDefinition(layer_parking.id(), selectedFeaturesOnly=True), 'OVERLAY' : intersects_buffer, 'OUTPUT': 'memory:'})['OUTPUT']
    #replace old, uncut parking lanes with newly created cut parking lanes
    layer_parking.startEditing()
    for feature in layer_parking.selectedFeatures():
        layer_parking.deleteFeature(feature.id())
    layer_parking.commitChanges()
    layer_parking = processing.run('native:mergevectorlayers', {'LAYERS' : [layer_parking,layer_parking_service], 'OUTPUT': 'memory:'})['OUTPUT']

    #cut off parking lanes in the carriageway areas
    #Method A - simple but not reliable at intersections between narrow and wider roads:
    #detect intersections between street and parking lane lines, buffer them and cut from parking lane to avoid false parking lanes in large intersection areas
    #layer_parking = bufferIntersection(layer_parking, layer_street, '(min("highway:width_proc", "width_proc") / 2) - 2', 'road junctions', NULL)

    #Method B - maybe slower but safer:
    #buffer the highway line according to its width and cut off parking lanes within this buffer
    centerline = processing.run('native:offsetline', { 'DISTANCE' : QgsProperty.fromExpression('"parking:lane:left:offset" - (("parking:lane:left:offset" + abs("parking:lane:right:offset")) / 2)'), 'INPUT' : layer_street, 'OUTPUT': 'memory:'})['OUTPUT']
    carriageway_buffer = processing.run('native:buffer', { 'DISTANCE' : QgsProperty.fromExpression('("width_proc" / 2) - 0.5'), 'END_CAP_STYLE' : 1, 'INPUT' : centerline, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking = processing.run('native:difference', { 'INPUT' : layer_parking, 'OVERLAY' : carriageway_buffer, 'OUTPUT': 'memory:'})['OUTPUT']

    #keep parking lanes free in driveway zones
    if buffer_driveway:
        layer_parking = bufferIntersection(layer_parking, layer_service, 'max("width_proc" / 2, ' + str(buffer_driveway / 2) + ')', 'driveways', NULL)
        if process_separate_areas:
            layer_parking_separate = bufferIntersection(layer_parking_separate, layer_service, 'max("width_proc" / 2, ' + str(buffer_driveway / 2) + ')', 'driveways (separate parking areas)', NULL)

    #calculate kerb intersection points
    print(time.strftime('%H:%M:%S', time.localtime()), 'Processing kerb intersection points...')
    intersects = getKerbIntersections(layer_street)

    #locate 5-metre buffers around kerb intersections and cut from parking lanes
    intersects_buffer = processing.run('native:buffer', {'DISTANCE' : 5, 'INPUT' : intersects, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking = processing.run('native:difference', {'INPUT' : layer_parking, 'OVERLAY' : intersects_buffer, 'OUTPUT': 'memory:'})['OUTPUT']

    #convert multi-part parking lanes into single-part objects
    layer_parking = processing.run('native:multiparttosingleparts', {'INPUT' : layer_parking, 'OUTPUT': 'memory:'})['OUTPUT']

    #merge with parking lane lines from separately mapped street side/lane parking areas
    if process_separate_areas:
        layer_parking = processing.run('native:mergevectorlayers', {'LAYERS' : [layer_parking, layer_parking_separate], 'OUTPUT': 'memory:'})['OUTPUT']

    #delete parking lane segments/line artefacts if they are too short for parking...
    #...and add capacity information to line segments or correct cutting errors
    layer_parking = getCapacity(layer_parking)
    #delete unimportant processing attribute and save output file
    layer_parking = processing.run('qgis:deletecolumn', {'INPUT' : layer_parking, 'COLUMN' : ['path'], 'OUTPUT': 'memory:'})['OUTPUT']
    
    print(time.strftime('%H:%M:%S', time.localtime()), 'Save parking lanes...')
    QgsVectorFileWriter.writeAsVectorFormatV2(layer_parking, dir_output + 'parking_lanes.geojson', transform_context, save_options)

    #add parking lanes to map
    layer_no_parking.setName('no parking lanes')
    QgsProject.instance().addMapLayer(layer_no_parking, False)
    group_parking.insertChildNode(0, QgsLayerTreeLayer(layer_no_parking))
    layer_no_parking.loadNamedStyle(dir + 'styles/parking_lanes_no.qml')

    layer_parking.setName('parking lanes')
    QgsProject.instance().addMapLayer(layer_parking, False)
    group_parking.insertChildNode(0, QgsLayerTreeLayer(layer_parking))
    layer_parking.loadNamedStyle(dir + 'styles/parking_lanes.qml')

    #convert parking lanes into chains of points for each individual vehicle
    if create_point_chain:
        print(time.strftime('%H:%M:%S', time.localtime()), 'Convert lanes to points...')
        #Method A: simple calculation for nodes on kerb line
        #layer_parking_chain = processing.run('native:pointsalonglines', {'INPUT' : layer_parking, 'DISTANCE' : QgsProperty.fromExpression('if("orientation" = \'parallel\' OR "orientation" = \'diagonal\' OR "orientation" = \'perpendicular\' OR "orientation" = \'marked\', $length / "capacity", 0)'), 'START_OFFSET' : QgsProperty.fromExpression('if(\"parking\" = \'parallel\', 2.6 - 0.4, if(\"parking\" = \'diagonal\', 1.27, if(\"parking\" = \'perpendicular\', 1.25 - 0.4, 0)))'), 'END_OFFSET' : QgsProperty.fromExpression('if(\"parking\" = \'parallel\', 2.6 - 0.4, if(\"parking\" = \'diagonal\', 3.11, if(\"parking\" = \'perpendicular\', 1.25 - 0.4, 0)))'), 'OUTPUT' : dir_output + 'parking_points.geojson' })

        #Method B: complex calculation and offset of the point to the centre of the vehicle
        layer_parking_chain = processing.run('native:pointsalonglines', {'INPUT' : layer_parking, 'DISTANCE' : QgsProperty.fromExpression('if("source:capacity" = \'estimated\', if("orientation" = \'diagonal\', 3.1, if("orientation" = \'perpendicular\', 2.5, 5.2)), if("capacity" = 1, $length, if($length < if("orientation" = \'diagonal\', 3.1 * "capacity", if("orientation" = \'perpendicular\', 2.5 * "capacity", (5.2 * "capacity") - 0.8)), ($length + (if("orientation" = \'parallel\', 0.8, if("orientation" = \'perpendicular\', 0.5, 0))) - (2 * if("orientation" = \'diagonal\', 1.55, if("orientation" = \'perpendicular\', 1.25, 2.6)))) / ("capacity" - 1), ($length - (2 * if("orientation" = \'diagonal\', 1.55, if("orientation" = \'perpendicular\', 1.25, 2.6)))) / ("capacity" - 1))))'), 'START_OFFSET' : QgsProperty.fromExpression('if("source:capacity" = \'estimated\', if("orientation" = \'diagonal\', ($length - (3.1*("capacity" - 1))) / 2, if("orientation" = \'perpendicular\', ($length - (2.5*("capacity" - 1))) / 2, ($length - (5.2*("capacity" - 1))) / 2)), if("capacity" < 2, $length / 2, if("orientation" = \'diagonal\', 1.55, if("orientation" = \'perpendicular\', if($length < if("orientation" = \'diagonal\', 3.1 * "capacity", if("orientation" = \'perpendicular\', 2.5 * "capacity", (5.2 * "capacity") - 0.8)), 0.9, 1.25), if($length < if("orientation" = \'diagonal\', 3.1 * "capacity", if("orientation" = \'perpendicular\', 2.5 * "capacity", (5.2 * "capacity") - 0.8)), 2.2, 2.6)))))'), 'OUTPUT': 'memory:'})['OUTPUT']
        layer_parking_chain = processing.run('native:translategeometry', {'INPUT' : layer_parking_chain, 'DELTA_X' : QgsProperty.fromExpression('if("position" = \'on_street\' or "position" IS NULL or "side" = \'separate\', cos((("angle") - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', -2.1, if("orientation" = \'perpendicular\', -2.2, -1)), if(("position" = \'street_side\' or "position" = \'on_kerb\' or "position" = \'shoulder\') and "side" is not \'separate\', -cos((("angle") - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', -2.1, if("orientation" = \'perpendicular\', -2.2, -1)), 0))'), 'DELTA_Y' : QgsProperty.fromExpression('if("position" = \'on_street\' or "position" IS NULL or "side" = \'separate\', sin(("angle" - 180 - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', -2.1, if("orientation" = \'perpendicular\', -2.2, -1)), if(("position" = \'street_side\' or "position" = \'on_kerb\' or "position" = \'shoulder\') and "side" is not \'separate\', -sin(("angle" - 180 - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', -2.1, if("orientation" = \'perpendicular\', -2.2, -1)), 0))'), 'OUTPUT': 'memory:'})['OUTPUT']

        #offset to the left side of the line for reversed line directions/left hand traffic
        #TODO: Add variable for right or left hand traffic (and use this also for reversing line direction)
        #layer_parking_chain = processing.run('native:translategeometry', {'INPUT' : layer_parking_chain, 'DELTA_X' : QgsProperty.fromExpression('if("position" = \'on_street\' or "position" IS NULL or "side" = \'separate\', cos((("angle") - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)), if(("position" = \'street_side\' or "position" = \'on_kerb\' or "position" = \'shoulder\') and "side" is not \'separate\', -cos((("angle") - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)), 0))'), 'DELTA_Y' : QgsProperty.fromExpression('if("position" = \'on_street\' or "position" IS NULL or "side" = \'separate\', sin(("angle" - 180 - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)), if(("position" = \'street_side\' or "position" = \'on_kerb\' or "position" = \'shoulder\') and "side" is not \'separate\', -sin(("angle" - 180 - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)), 0))'), 'OUTPUT': 'memory:'})['OUTPUT']

        #add point chain to map
        layer_parking_chain.setName('parking lanes (points)')
        QgsProject.instance().addMapLayer(layer_parking_chain, False)
        group_parking.insertChildNode(0, QgsLayerTreeLayer(layer_parking_chain))

        print(time.strftime('%H:%M:%S', time.localtime()), 'Save parking points...')
        QgsVectorFileWriter.writeAsVectorFormatV2(layer_parking, dir_output + 'parking_points.geojson', transform_context, save_options)

    #focus on parking layer
    iface.mapCanvas().setExtent(layer_parking.extent())

    print(time.strftime('%H:%M:%S', time.localtime()), 'Completed.')
