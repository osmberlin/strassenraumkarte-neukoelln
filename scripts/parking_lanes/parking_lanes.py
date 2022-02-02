#-----------------------------------------------------------------------------#
#   Parking lane analysis with OSM data                                       #
#   ------------------------------------------------------------------------- #
#   OSM data post-processing for QGIS/PyGIS for rendering the parkingmap at   #
#   https://supaplexosm.github.io/strassenraumkarte-neukoelln/?map=parkingmap #
#                                                                             #
#   > version/date: 2021-12-28                                                #
#-----------------------------------------------------------------------------#

#-------------------------------------------------#
#   V a r i a b l e s   a n d   S e t t i n g s   #
#-------------------------------------------------#

from qgis.core import *
import os, processing, math, time

#working directory, see https://stackoverflow.com/a/65543293/729221
from console.console import _console
dir = _console.console.tabEditorWidget.currentWidget().path.replace("parking_lanes.py","")

#coordinate reference system – storage options
#Attention: EPSG:25833 (ETRS89 / UTM zone 33N) is used here – other CRS may be necessary at other locations.
#A metric CRS is necessary to calculate with metre units and distances.
transform_context = QgsCoordinateTransformContext()
transform_context.addCoordinateOperation(QgsCoordinateReferenceSystem("EPSG:4326"), QgsCoordinateReferenceSystem("EPSG:25833"), "")
coordinateTransformContext=QgsProject.instance().transformContext()
save_options = QgsVectorFileWriter.SaveVectorOptions()
save_options.driverName = 'GeoJSON'
save_options.ct = QgsCoordinateTransform(QgsCoordinateReferenceSystem("EPSG:4326"), QgsCoordinateReferenceSystem("EPSG:25833"), coordinateTransformContext)

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
vehicle_dist_para = 5.2     #parallel parking
vehicle_dist_diag = 3.1     #diagonal parking (angle: 60 gon = 54°)
vehicle_dist_perp = 2.5     #perpendicular parking
vehicle_length = 4.4        #average vehicle length (a single vehicle, wwithout manoeuvring distance)
vehicle_width = 1.8         #average vehicle width

#list of highway tags that do not belong to the regular road network but are also analysed
is_service_list = ['service', 'track', 'bus_guideway', 'footway', 'cycleway', 'path']

#list of attributes kept for the street layer
#Attention: Certain width specifications are also processed (fillBaseAttributes()), but they should not be specified here.
#"parking:lane:left/right:position" are new attributes for collecting the parking lane position.
#"error_output" is a new attribute to collect errors and inconsistencies
street_key_list = [
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
'highway',
'name',
'width_proc',
'width_proc:effective',
'error_output'
]


#-------------------------------
#   V a r i a b l e s   E n d
#-------------------------------



def prepareLayers():
#-----------------------------------------------------------------------------------
#   L a y e r   v o r b e r e i t e n
#-----------------------------------------------------------------------------------
# Straßen-Rohdaten einlesen und vier neue Bearbeitungslayer erstellen/speichern:
# (1) Straßenlayer (insbes. zur Visualisierung),
# (2) service-Layer (insbes. zum Verschnitt von Einfahrten)
# (3) Parkstreifen links
# (4) Parkstreifen rechts
# (sowie einen Layer mit Gehwegübergängen, der nicht gerendert wird)
#-----------------------------------------------------------------------------------
    print(time.strftime('%H:%M:%S', time.localtime()), 'Prepare street data...')
    layer_raw = QgsVectorLayer(dir + 'data/input.geojson|geometrytype=LineString', 'streets (raw)', 'ogr')
    layer_crossing = QgsVectorLayer(dir + 'data/input.geojson|geometrytype=Point', 'pedestrian crossings (raw)', 'ogr')

    #Abbrechen, wenn keine Parkstreifen-Attribute vorhanden sind
    if not fillBaseAttributes(layer_raw, False):
        return False

    print(time.strftime('%H:%M:%S', time.localtime()), 'Insert street data...')

    #Straßen-Input in einen Straßen- und einen Einfahrtlayer teilen
    QgsVectorFileWriter.writeAsVectorFormatV2(layer_raw, dir + 'data/streets_processed.geojson', transform_context, save_options)
    QgsVectorFileWriter.writeAsVectorFormatV2(layer_raw, dir + 'data/service_processed.geojson', transform_context, save_options)
    QgsVectorFileWriter.writeAsVectorFormatV2(layer_crossing, dir + 'data/crossing.geojson', transform_context, save_options)
    layer_street = QgsProject.instance().addMapLayer(QgsVectorLayer(dir + 'data/streets_processed.geojson', 'streets', 'ogr'), False)
    group_streets.insertChildNode(0, QgsLayerTreeLayer(layer_street))
    layer_service = QgsProject.instance().addMapLayer(QgsVectorLayer(dir + 'data/service_processed.geojson', 'driveways', 'ogr'), False)
    group_streets.insertChildNode(0, QgsLayerTreeLayer(layer_service))
    layer_crossing = QgsProject.instance().addMapLayer(QgsVectorLayer(dir + 'data/crossing.geojson', 'pedestrian crossings', 'ogr'), False)

    #Parkstreifen separat vorbereiten
    print(time.strftime('%H:%M:%S', time.localtime()), 'Insert parking lane data...')
    QgsVectorFileWriter.writeAsVectorFormatV2(layer_raw, dir + 'data/parking_lanes/parking_lanes_left.geojson', transform_context, save_options)
    QgsVectorFileWriter.writeAsVectorFormatV2(layer_raw, dir + 'data/parking_lanes/parking_lanes_right.geojson', transform_context, save_options)
    layer_parking_left = QgsVectorLayer(dir + 'data/parking_lanes/parking_lanes_left.geojson', 'parking lane left', 'ogr')
    layer_parking_right = QgsVectorLayer(dir + 'data/parking_lanes/parking_lanes_right.geojson', 'parking lane right', 'ogr')
    #layer_parking_left = QgsProject.instance().addMapLayer(QgsVectorLayer(dir + 'parking_lanes_left.geojson', 'parking lane left', 'ogr'))
    #layer_parking_right = QgsProject.instance().addMapLayer(QgsVectorLayer(dir + 'parking_lanes_right.geojson', 'parking lane right', 'ogr'))

    print(time.strftime('%H:%M:%S', time.localtime()), 'Edit street data: Clean up dataset...')
    layer_street.startEditing()
    layer_service.startEditing()

    #Straßen- und Einfahrten-Layer separieren/nicht benötige Objekte jeweils löschen
    for feature in layer_street.getFeatures():
        if feature.attribute('highway') in is_service_list:
            layer_street.deleteFeature(feature.id())
        else:
            layer_service.deleteFeature(feature.id())

    attributes = len(layer_street.attributeList())
    for id in range(attributes-1, 0, -1):
        if not layer_street.attributeDisplayName(id) in street_key_list:
            layer_street.deleteAttribute(id)
            layer_service.deleteAttribute(id)
    layer_street.updateFields()
    layer_street.commitChanges()
    layer_service.updateFields()
    layer_service.commitChanges()

    #zunächst alle unbenötigten Attribute löschen - (2) für Parkstreifenlayer
    print(time.strftime('%H:%M:%S', time.localtime()), 'Edit parking lane data: Clean up dataset...')
    layer_parking_left.startEditing()
    layer_parking_right.startEditing()

    for side in ['left', 'right']:
        if side == 'left':
            layer = layer_parking_left
        else:
            layer = layer_parking_right

        #Erschließungs-/Wirtschaftswege ohne Parkplatzinformation entfernen
        for feature in layer.getFeatures():
            if feature.attribute('highway') in is_service_list:
                if not feature.attribute('parking:lane:left') and not feature.attribute('parking:lane:right'):
                    layer_parking_left.deleteFeature(feature.id())
                    layer_parking_right.deleteFeature(feature.id())

        attributes = len(layer.fields().allAttributesList())
        for id in range(attributes-1, 0, -1):
            if not layer.attributeDisplayName(id) in parking_key_list and not 'parking:lane' in layer.attributeDisplayName(id) and not 'parking:condition' in layer.attributeDisplayName(id):
                layer.deleteAttribute(id)

        #Bewahrte Felder umbenennen, um den Bezug auf die Straßenbreite zu verdeutlichen
        for attr in parking_key_list:
            if attr != 'highway' and attr != 'error_output':
                layer.renameAttribute(layer.fields().indexOf(attr), 'highway:'+attr)

        layer.updateFields()
        layer.commitChanges()

        if side == 'left':
            layer_parking_left = layer
        else:
            layer_parking_right = layer

    return([layer_street, layer_service, layer_parking_left, layer_parking_right, layer_crossing])



def fillBaseAttributes(layer, commit):
#---------------------------------------------------------------------------
#   S t r a ß e n - B a s i s a t t r i b u t e   e r m i t t e l n
#---------------------------------------------------------------------------
# Ermittelt - wenn nicht explizit angegeben - grob die Breite der Straße
# und ihrer Parkstreifen und teilt Parkstreifenattribute vollständig auf
# separate Attribute für beide Seiten auf.
# > layer:  Der Layer, für den die Straßenbreiten ermittelt werden sollen.
# > commit: (True/False) Gibt an, ob die Änderungen in layer gespeichert
#           werden. "False" kann z.B. Änderungen am Input-Layer verhindern.
#---------------------------------------------------------------------------
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
        print(time.strftime('%H:%M:%S', time.localtime()), 'Input dataset ("' + dir + 'data/input.geojson' + '") does not contain parking lane information ("parking:lane:*"). Processing aborted.')
        return(False)

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
                if not parking_left or not parking_right:
                    error += '[no_pl] Parkstreifeninformation nicht für alle Seite vorhanden. '
        else:
            if not parking_left or not parking_right:
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
            if wd_est != -1:
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
    if commit:
        layer.commitChanges()

    return(True)



def prepareParkingLane(layer, side, clean):
#------------------------------------------------------------------------------------
#   P a r k s p u r i n f o r m a t i o n e n   z u s a m m e n f ü h r e n
#------------------------------------------------------------------------------------
# Überträgt Parkstreifenattribute für beide Richtungen in separate, gebündelte Attribute.
# > layer: Der Layer, für den die Parkstreifeninfos gebündelt werden sollen.
# > side:  Straßenseite, der dieser Layer entspricht ('left'/'right')
# > clean: (True/False) Gibt an, ob die Attributtabelle nach Abschluss der Be-
#          rechnungen von überflüssigen Einzelattributen des Rohdatensatzes
#          bereinigt werden soll. Insbesondere für die Fehlersuche im Rohdaten-
#          satz kann es hilfreich sein, die Attribute zum Vergleich zu behalten.
#------------------------------------------------------------------------------------

    id_left = layer.fields().indexOf('parking:lane:left')
    id_right = layer.fields().indexOf('parking:lane:right')

    layer.startEditing()

    #Neue Attribute für Parkstreifeninformationen erstellen und deren ID's zur späteren Bearbeitung ermitteln
    for attr in ['parking', 'orientation', 'position', 'condition', 'condition:other', 'condition:other:time', 'vehicles', 'maxstay', 'capacity', 'source:capacity', 'width', 'offset']:
        layer.dataProvider().addAttributes([QgsField(attr, QVariant.String)])
    layer.updateFields()

    id_id = layer.fields().indexOf('id')
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

        #Identifikator für rechte bzw. linke Parkstreifen in ID ergänzen, um diese später auseinanderhalten zu können
        id = feature.attribute('id')
        if side == 'left':
            id = id + '_l'
        elif side == 'right':
            id = id + '_r'
        layer.changeAttributeValue(feature.id(), id_id, id)

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
            layer.deleteFeature(feature.id())
            continue

        parking_offset = feature.attribute('parking:lane:' + side + ':offset')

        #Parkstreifen-Ausrichtung und Breite übernehmen
        parking_position = feature.attribute('parking:lane:' + side + ':position')
        parking_width = feature.attribute('parking:lane:' + side + ':width')
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

        #Segmente löschen, an denen ausschließlich Park- und Halteverbot besteht
        if parking_condition == 'no_parking' and parking_condition_other == 'no_stopping' or parking_condition == 'no_stopping' and parking_condition_other == 'no_parking':
            layer.deleteFeature(feature.id())
            continue

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
        for attr in layer_parking_left.attributeAliases():
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
        if parking_position == 'lay_by' or parking_position == 'street_side':
            layer.changeAttributeValue(feature.id(), id_parking, 'street_side')
        else:
            layer.changeAttributeValue(feature.id(), id_parking, 'lane')
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

    #Abschließend bei Bedarf nicht mehr benötigte parking:lane-Attribute entfernen
    if clean:
        attributes = len(layer.fields().allAttributesList())
        for id in range(attributes-1, 0, -1):
            if 'parking:lane' in layer.attributeDisplayName(id) or 'parking:condition' in layer.attributeDisplayName(id):
                layer.deleteAttribute(id)
        layer.updateFields()

    layer.commitChanges()

    return(True)



def getIntersections(layer, method):
#---------------------------------------------------------------------
#   K r e u z u n g e n   e r m i t t e l n
#---------------------------------------------------------------------
#   ---(Funktion derzeit ungenutzt)---
#---------------------------------------------------------------------
# Ermittelt Straßenkreuzungen.
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
#---------------------------------------------------------------------

    if method != 'fast':
        # Straßen in Einzelteile zerlegen, um die Anzahl abgehender Wege sicher für jede Kreuzung ermitteln zu können
        expl_street = processing.run('native:explodelines', {'INPUT' : layer, 'OUTPUT': 'memory:'})['OUTPUT']

        # Kreuzungspunkte inklusive zahlreicher Pseudo-Nodes ermitteln
        intersections = processing.run('native:lineintersections', {'INPUT' : expl_street, 'INTERSECT' : expl_street, 'OUTPUT': dir + 'data/buffer_points/intersections.geojson'})['OUTPUT']

        intersections = QgsProject.instance().addMapLayer(QgsVectorLayer(dir + 'data/buffer_points/intersections.geojson', 'Straßenkreuzungen', 'ogr'))
        intersections.startEditing()

        # Variable für Breitenangabe der Kreuzung bereithalten
        intersections.dataProvider().addAttributes([QgsField('intersection_width', QVariant.String)])
        intersections.updateFields()
        id_width = intersections.fields().indexOf('intersection_width')

        for feature in intersections.getFeatures():
            # Punkte einzeln durchgehen und identische Punkte auswählen
            intersections.removeSelection()
            intersections.select(feature.id())
            processing.run('native:selectbylocation', {'INPUT' : intersections, 'INTERSECT' : QgsProcessingFeatureSourceDefinition(dir + 'data/buffer_points/intersections.geojson', selectedFeaturesOnly=True, featureLimit=-1, geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid), 'PREDICATE' : [3]})

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
#---------------------------------------------------------------------
#   B o r d s t e i n s c h n i t t p u n k t e   e r m i t t e l n
#---------------------------------------------------------------------
# Ermittelt die Schnittkanten von Bordsteinen im Kreuzungsbereich.
# > layer: Der Layer, für den die Schnittpunkte ermittelt werden sollen.
#---------------------------------------------------------------------

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
#-------------------------------------------------------------
#   E i n m ü n d u n g e n   f r e i h a l t e n
#-------------------------------------------------------------
# Entfernt Abschnitte aus Parkstreifenlayern, wenn an dieser
# Stelle ein Weg (Straße, Einfahrt) einmündet.
# > layer_parking: Der betroffene Parkstreifen-Layer
# > layer_intersect: Der einmündende Layer
# > buffer: Ausdruck/Formel zur Ermittlung des Radius,
#   der freigehalten werden soll
# > buffer_name: Wenn angegeben, wird der erzeugte Puffer
#   mit diesem Namen der Karte hinzugefügt
# > intersects (optional): Wenn hier ein Punktlayer
#   übergeben wird, wird dieser gepuffert, statt die
#   Kreuzungspunkte aus den ersten beiden Layern zu berechen.
#-------------------------------------------------------------

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



def bufferCrossing(layer_parking, layer_crossing, side):
#-----------------------------------------------------------------------------
#   G e h w e g ü b e r g ä n g e   f r e i h a l t e n
#-----------------------------------------------------------------------------
# Entfernt Abschnitte aus Parkstreifenlayern im Bereich von
# Gehwegübergängen, an denen die Fahrbahn für querenden
# Fußverkehr freigehalten wird.
# > layer_parking: Der betroffene Parkstreifen-Layer
# > layer_crossing: Layer mit Gehwegübergängen
#-----------------------------------------------------------------------------

# Puffer-Radien:
#    highway = traffic_signals                   -> 10 m (laut StVO)
#        traffic_signals:direction=forward: rechts abziehen
#        traffic_signals:direction=backward: links abziehen
#        !traffic_signals:direction: beidseitig abziehen
#    crossing = marked                           -> 2 m
#    crossing = zebra OR crossing_ref = zebra    -> 4.5 m (4 Meter Zebrastreifen sowie laut StVO 5 Meter davor)
#    crossing:buffer_marking                     -> 3 m
#        both: an beiden abziehen
#        left/right je Seite abziehen
#    crossing:kerb_extension                     -> 3 m
#        both: an beiden abziehen
#        left/right je Seite abziehen
#-----------------------------------------------------------------------------

    #Übergänge nach gemeinsamen Kriterien/Radien auswählen und Teilpuffer (mit Radius x) ziehen:
    #Vor Lichtzeichenanlagen/Ampeln 10 Meter Halteverbot (StVO) - beidseitig berücksichtigen, wenn Ampel nicht fahrtrichtungsabhängig erfasst ist
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_crossing, 'EXPRESSION' : '\"highway\" = \'traffic_signals\' AND \"traffic_signals:direction\" IS NOT \'forward\' AND \"traffic_signals:direction\" IS NOT \'backward\''})
    buffer01 = processing.run('native:buffer', {'DISTANCE' : 10, 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_crossing.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']
    #...oder nur von einer Seite abziehen, wenn die Ampel fahrtrichtungsabhängig erfasst ist
    if side == 'left':
        processing.run('qgis:selectbyexpression', {'INPUT' : layer_crossing, 'EXPRESSION' : '\"highway\" = \'traffic_signals\' AND \"traffic_signals:direction\" = \'backward\''})
    if side == 'right':
        processing.run('qgis:selectbyexpression', {'INPUT' : layer_crossing, 'EXPRESSION' : '\"highway\" = \'traffic_signals\' AND \"traffic_signals:direction\" = \'forward\''})
    buffer_s01 = processing.run('native:buffer', {'DISTANCE' : 10, 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_crossing.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']

    #An Gehwegvorstreckungen oder markierten Übergangs-Sperrflächen: 3 Meter
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_crossing, 'EXPRESSION' : '\"crossing:kerb_extension\" = \'both\' OR \"crossing:buffer_marking\" = \'both\''})
    buffer02 = processing.run('native:buffer', {'DISTANCE' : 3, 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_crossing.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']
    #...oder nur von einer Seite abziehen, falls nur einseitig vorhanden
    if side == 'left':
        processing.run('qgis:selectbyexpression', {'INPUT' : layer_crossing, 'EXPRESSION' : '\"crossing:kerb_extension\" = \'left\' OR \"crossing:buffer_marking\" = \'left\''})
    if side == 'right':
        processing.run('qgis:selectbyexpression', {'INPUT' : layer_crossing, 'EXPRESSION' : '\"crossing:kerb_extension\" = \'right\' OR \"crossing:buffer_marking\" = \'right\''})
    buffer_s02 = processing.run('native:buffer', {'DISTANCE' : 3, 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_crossing.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']

    #An Fußgängerüberwegen/Zebrastreifen: 4,5 Meter (4 Meter Zebrastreifenbreite sowie laut StVO 5 Meter Parkverbot davor)
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_crossing, 'EXPRESSION' : '\"crossing\" = \'zebra\' OR \"crossing_ref\" = \'zebra\' OR \"crossing\" = \'traffic_signals\''})
    buffer03 = processing.run('native:buffer', {'DISTANCE' : 4.5, 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_crossing.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']

    #An sonstigen markierten Überwegen: 2 Meter
    processing.run('qgis:selectbyexpression', {'INPUT' : layer_crossing, 'EXPRESSION' : '\"crossing\" = \'marked\''})
    buffer04 = processing.run('native:buffer', {'DISTANCE' : 2, 'INPUT' : QgsProcessingFeatureSourceDefinition(layer_crossing.id(), selectedFeaturesOnly=True), 'OUTPUT': 'memory:'})['OUTPUT']

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



def getCapacity(layer):
#-----------------------------------------------------------------------------
#   S t e l l p l a t z z a h l   p r ü f e n
#-----------------------------------------------------------------------------
# Entfernt Liniensegmente aus Parkstreifenlayern, wenn diese zu kurz zum
# Parken sind (Platz für weniger als ein Fahrzeug) und ergänzt/korrigiert
# Kapazitätsangeben (je nach Parkrichtung).
# > layer: Der Layer, für den die Segmente geprüft werden sollen.
#-----------------------------------------------------------------------------

    layer.startEditing()
    id_capacity = layer.fields().indexOf('capacity')
    vehicle_diag_width = math.sqrt(vehicle_width * 0.5 * vehicle_width) + math.sqrt(vehicle_length * 0.5 * vehicle_length)
#Korrektur/Verbesserung: Bei Einstellwinkel 60 gon = 54 Grad: vehicle_length * sin (36 Grad) + vehicle_width * cos(36 Grad) = 4.04 Meter
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
            if length < vehicle_length:
                layer.deleteFeature(feature.id())
                continue
            elif capacity == NULL:
                #Anzahl Parkplätze ergibt sich aus Segmentlänge - abzüglich eines Ragierabstands zwischen zwei Fahrzeugen, der an einem der beiden Enden des Segments nicht benötigt wird
                capacity = math.floor((length + (vehicle_dist_para - vehicle_length)) / vehicle_dist_para)
                layer.changeAttributeValue(feature.id(), id_capacity, capacity)
        elif orientation == 'diagonal':
            if length < vehicle_diag_width:
                layer.deleteFeature(feature.id())
                continue
            elif capacity == NULL:
                capacity = math.floor((length + (vehicle_dist_diag - vehicle_diag_width)) / vehicle_dist_diag)
                layer.changeAttributeValue(feature.id(), id_capacity, capacity)
        elif orientation == 'perpendicular':
            if length < vehicle_width:
                layer.deleteFeature(feature.id())
                continue
            elif capacity == NULL:
                capacity = math.floor((length + (vehicle_dist_perp - vehicle_width)) / vehicle_dist_perp)
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



#--------------------------------
#      S c r i p t   S t a r t
#--------------------------------

#create necessary directories if not existing
need_dir = ["data/parking_lanes/"]
for d in need_dir:
    if not os.path.exists(dir + d):
        os.makedirs(dir + d)

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
    layer_crossing = layers[4]

    layer_street.loadNamedStyle(dir + 'styles/street_simple.qml')
    layer_service.loadNamedStyle(dir + 'styles/street_simple.qml')

    #separate and bundle parking lane attributes to a left and a right layer
    print(time.strftime('%H:%M:%S', time.localtime()), 'Processing parking lane data...')
    prepareParkingLane(layer_parking_left, 'left', True)
    prepareParkingLane(layer_parking_right, 'right', True)

    #connect adjoining parking lane segments with same properties
    #TODO Warning: Can possibly lead to faults if two segments with opposite directions but the same properties meet.
    layer_parking_left = processing.run('native:dissolve', {'INPUT': layer_parking_left, 'FIELD' : ['highway:name','parking','orientation','position','condition','condition:other','condition:other:time','vehicles','maxstay','capacity','width','offset'], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking_right = processing.run('native:dissolve', {'INPUT': layer_parking_right, 'FIELD' : ['highway:name','parking','orientation','position','condition','condition:other','condition:other:time','vehicles','maxstay','capacity','width','offset'], 'OUTPUT': 'memory:'})['OUTPUT']

    #calculate angles at pedestrian crossings (for rendering and spatial calculations)
    layer_vertices = processing.run('native:extractvertices', {'INPUT': layer_street, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing = processing.run('native:joinattributesbylocation', {'INPUT': layer_crossing, 'JOIN' : layer_vertices, 'JOIN_FIELDS' : ['angle'], 'OUTPUT': 'memory:'})['OUTPUT']
    #also apply street width
    layer_crossing = processing.run('native:joinattributesbylocation', {'INPUT': layer_crossing, 'JOIN' : layer_street, 'JOIN_FIELDS' : ['width_proc', 'parking:lane:right:width:carriageway', 'parking:lane:left:width:carriageway'], 'OUTPUT': 'memory:'})['OUTPUT']
    layer_crossing = QgsProject.instance().addMapLayer(layer_crossing, False)

    #keep parking lanes free in the area of pedestrian crossings (before offset, because affects both sides)
    layer_parking_left = bufferCrossing(layer_parking_left, layer_crossing, 'left')
    layer_parking_right = bufferCrossing(layer_parking_right, layer_crossing, 'right')

    #offset parking lanes according to the lane width
    layer_parking_left = processing.run('native:offsetline', {'INPUT': layer_parking_left, 'DISTANCE' : QgsProperty.fromExpression('"offset"'), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking_right = processing.run('native:offsetline', {'INPUT': layer_parking_right, 'DISTANCE' : QgsProperty.fromExpression('"offset"'), 'OUTPUT': 'memory:'})['OUTPUT']

    #merge left and right parking lane layers (turn one side before)
    layer_parking_right = processing.run('native:reverselinedirection', {'INPUT': layer_parking_right, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking = processing.run('native:mergevectorlayers', {'LAYERS' : [layer_parking_left,layer_parking_right], 'OUTPUT': 'memory:'})['OUTPUT']
    QgsProject.instance().addMapLayer(layer_parking, False)

    print(time.strftime('%H:%M:%S', time.localtime()), 'Processing intersection/driveway zones...')

    #separately cut off parking lanes on service roads near the intersection area
    #Select service roads with parking lane information, determine intersections with roads and buffer these by the width of the road + 5 metre distance
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
    layer_parking = bufferIntersection(layer_parking, layer_service, 'max("width_proc" / 2, 2)', 'driveways', NULL)

    #calculate kerb intersection points
    print(time.strftime('%H:%M:%S', time.localtime()), 'Processing kerb intersection points...')
    intersects = getKerbIntersections(layer_street)

    #locate 5-metre buffers around kerb intersections and cut from parking lanes
    intersects_buffer = processing.run('native:buffer', {'DISTANCE' : 5, 'INPUT' : intersects, 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking = processing.run('native:difference', {'INPUT' : layer_parking, 'OVERLAY' : intersects_buffer, 'OUTPUT': 'memory:'})['OUTPUT']

    #convert multi-part parking lanes into single-part objects
    layer_parking = processing.run('native:multiparttosingleparts', {'INPUT' : layer_parking, 'OUTPUT': 'memory:'})['OUTPUT']

    #delete parking lane segments/line artefacts if they are too short for parking...
    #...and add capacity information to line segments or correct cutting errors
    layer_parking = getCapacity(layer_parking)

    #add parking lanes to map
    layer_parking.setName('parking lanes')
    QgsProject.instance().addMapLayer(layer_parking, False)
    group_parking.insertChildNode(0, QgsLayerTreeLayer(layer_parking))

    layer_parking.loadNamedStyle(dir + 'styles/parking_lanes.qml')

    #convert parking lanes into chains of points for each individual vehicle
    #Method A: simple calculation for nodes on kerb line
    #layer_parking_chain = processing.run('native:pointsalonglines', {'INPUT' : layer_parking, 'DISTANCE' : QgsProperty.fromExpression('if("orientation" = \'parallel\' OR "orientation" = \'diagonal\' OR "orientation" = \'perpendicular\' OR "orientation" = \'marked\', $length / "capacity", 0)'), 'START_OFFSET' : QgsProperty.fromExpression('if(\"parking\" = \'parallel\', 2.6 - 0.4, if(\"parking\" = \'diagonal\', 1.27, if(\"parking\" = \'perpendicular\', 1.25 - 0.4, 0)))'), 'END_OFFSET' : QgsProperty.fromExpression('if(\"parking\" = \'parallel\', 2.6 - 0.4, if(\"parking\" = \'diagonal\', 3.11, if(\"parking\" = \'perpendicular\', 1.25 - 0.4, 0)))'), 'OUTPUT': 'memory:'})['OUTPUT']

    #Method B: complex calculation and offset of the point to the centre of the vehicle
    layer_parking_chain = processing.run('native:pointsalonglines', {'INPUT' : layer_parking, 'DISTANCE' : QgsProperty.fromExpression('if("source:capacity" = \'estimated\', if("orientation" = \'diagonal\', 3.1, if("orientation" = \'perpendicular\', 2.5, 5.2)), if("capacity" = 1, $length, if($length < if("orientation" = \'diagonal\', 3.1 * "capacity", if("orientation" = \'perpendicular\', 2.5 * "capacity", (5.2 * "capacity") - 0.8)), ($length + (if("orientation" = \'parallel\', 0.8, if("orientation" = \'perpendicular\', 0.5, 0))) - (2 * if("orientation" = \'diagonal\', 1.55, if("orientation" = \'perpendicular\', 1.25, 2.6)))) / ("capacity" - 1), ($length - (2 * if("orientation" = \'diagonal\', 1.55, if("orientation" = \'perpendicular\', 1.25, 2.6)))) / ("capacity" - 1))))'), 'START_OFFSET' : QgsProperty.fromExpression('if("source:capacity" = \'estimated\', if("orientation" = \'diagonal\', ($length - (3.1*("capacity" - 1))) / 2, if("orientation" = \'perpendicular\', ($length - (2.5*("capacity" - 1))) / 2, ($length - (5.2*("capacity" - 1))) / 2)), if("capacity" < 2, $length / 2, if("orientation" = \'diagonal\', 1.55, if("orientation" = \'perpendicular\', if($length < if("orientation" = \'diagonal\', 3.1 * "capacity", if("orientation" = \'perpendicular\', 2.5 * "capacity", (5.2 * "capacity") - 0.8)), 0.9, 1.25), if($length < if("orientation" = \'diagonal\', 3.1 * "capacity", if("orientation" = \'perpendicular\', 2.5 * "capacity", (5.2 * "capacity") - 0.8)), 2.2, 2.6)))))'), 'OUTPUT': 'memory:'})['OUTPUT']
    layer_parking_chain = processing.run('native:translategeometry', {'INPUT' : layer_parking_chain, 'DELTA_X' : QgsProperty.fromExpression('if("position" = \'on_street\' or "position" IS NULL, cos((("angle") - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)), if("position" = \'street_side\' or "position" = \'on_kerb\' or "position" = \'shoulder\', -cos((("angle") - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)), 0))'), 'DELTA_Y' : QgsProperty.fromExpression('if("position" = \'on_street\' or "position" IS NULL, sin(("angle" - 180 - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)), if("position" = \'street_side\' or "position" = \'on_kerb\' or "position" = \'shoulder\', -sin(("angle" - 180 - if("orientation" = \'diagonal\', if("oneway_direction" = \'true\', -27, 27), 0)) * (pi() / 180)) * if("orientation" = \'diagonal\', 2.1, if("orientation" = \'perpendicular\', 2.2, 1)), 0))'), 'OUTPUT': 'memory:'})['OUTPUT']

    #add point chain to map
    layer_parking_chain.setName('parking lanes (points)')
    QgsProject.instance().addMapLayer(layer_parking_chain, False)
    group_parking.insertChildNode(0, QgsLayerTreeLayer(layer_parking_chain))

    print(time.strftime('%H:%M:%S', time.localtime()), 'Completed. Generated parking lane data can now be saved.')
