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

Make sure that the following folder structure is existing (you can [download everything here](https://github.com/SupaplexOSM/strassenraumkarte-neukoelln/tree/main/scripts)). Store the directory path to this structure in the variable "dir".

    └ your-directory
     ├ data/
     ┊ └ input.geojson
     └ styles/
       └ [various style files for provisional rendering]

This script is based on very basic programming and QGIS knowledge. Many steps can certainly be solved much more effectively or elegantly, plus there are still some (marked) TODO's that would make it even better. I am happy about improvements and extensions!

Note: There is no consensus yet on which line the highway objekt in OSM represents exactly: The centreline of the carriageway or the driving line. So far, this script calculates the location of parking lanes according to variant B in [this figure](https://wiki.openstreetmap.org/wiki/File:Highway_representation.png) (driving line).
