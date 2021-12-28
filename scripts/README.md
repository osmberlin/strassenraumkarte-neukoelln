# parking_lanes.py
**Python script for QGIS to generate parking lanes from OSM data**

*How to use:*

1. Run Overpass-Query for street and parking lane data: http://overpass-turbo.eu/s/127h
2. Export result to 'data/input.geojson'
3. Run this python script in QGIS
4. For the final result, separate steps still have to be done individually afterwards:
* Include bus stops and cut the parking lanes on the side of the road where they are located.
* Locate objects that affect parking in parking lanes (e.g. street trees or lanterns in the parking lane area, street furniture in kerbside parking) and cut them off from the parking lane segments.
* Check the resulting parking lane data for bugs, depending on how accurate you need it to be.
* Include separately mapped parking areas if needed (parking=surface, street_side etc.)

*Note:*

* Directory: Make sure that the following directory structure is existing (you can [download everything here](https://github.com/SupaplexOSM/strassenraumkarte-neukoelln/tree/main/scripts)). Store the directory path to this structure in the variable "dir".

      └ your-directory
       ├ data/
       ┊ └ input.geojson
       └ styles/
         └ [various style files for provisional rendering]

* Coordinate Reference System: Results are saved in EPSG:25833 (ETRS89 / UTM zone 33N). A different CRS may be necessary at other locations (see below).

* Highway Line Representation: There is no consensus yet on which line the highway objekt in OSM represents exactly: The centreline of the carriageway or the driving line. So far, this script calculates the location of parking lanes according to variant B in [this figure](https://wiki.openstreetmap.org/wiki/File:Highway_representation.png) (driving line).

* Background: This script is based on very basic programming and QGIS knowledge. Many steps can certainly be solved much more effectively or elegantly, plus there are still some (marked) TODO's that would make it even better. I am happy about improvements and extensions!


# Changelog

* 2021-03-11  + Added new method to correctly exclude parking lanes in the intersection area
* 2021-03-11  + Added note on inclusion of separately mapped parking spaces
* 2021-03-11  ! Fixed that parking point chain was only displayed, but could not be moved, used or saved
* 2021-03-11  ! Fixed parking point chain offset from street_side parking lanes
* 2021-03-11  ! Fixed "time.strftime"-error under certain rare circumstances in def prepareParkingLane (rearranged processing print outputs)
* 2021-06-18  + Added support/attribute for "parking:condition:...:vehicles"



# post_processing.py
**Python script for QGIS for post processing osm data for rendering in the micromap**

This script generates special data layers that improve the rendering of the "straßenraumkarte"/micromap. This includes in particular a processed lane layer to render lane markings.

*How to use:*

1. If other OSM data than the sample data are required, they can be downloaded via an [Overpass query](https://github.com/SupaplexOSM/strassenraumkarte-neukoelln/blob/main/scripts/layer/overpass_links). Adjust the BBOX if you want to download the data for a different area than the example area (Berlin-Neukölln). Export the results to 'layer/geojson/[layer name].geojson' (or any other directory, as defined in the script). The sample data are sufficient if you only want to generate the lane layer.
2. Open the post processing script and adjust the project directory (so that the osm data can be found). In the first few lines of the script you can select which processing steps are to be executed: For the lane markings, for example, set "proc_lane_markings" to "1" (default).
3. Run the python script in QGIS. The post processed layers are saved at 'layers/geojson/post_processed' by default (can be adjusted in the script).

The script includes these processing steps, among others:
* Generating a layer for road markings - contains lines for individual lanes as well as attributes of how these lanes are marked.
* Processing of building parts to be able to represent building parts of different heights and "floating" building parts.
* Generating points within a hexagonal grid in forests to represent them more realistically.
* Alignment of street furniture such as street cabinets or street lamps to the nearest street if no orientation/direction is specified.
* Generating defined, continuous street segments for nicer street labelling.
