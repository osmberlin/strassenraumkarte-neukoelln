# parking_lanes.py for QGIS

**Python script for QGIS to generate parking lanes from OSM data**

## How to use

1. Run [Overpass-Query](https://overpass-turbo.eu/s/1jAp) for street and parking lane data
2. Export result as GeoJSON to 'data/input.geojson'
3. Run this python script in QGIS
   1. "Plugins" => "Python Console"
   1. (If internal Python Editor Panel is hidden: Right click in Console => "Show Editor")
   1. Open File in QGIS Python Editor
   1. Run from there (Note: Do _not_ use the "Browser" => File => "Run Script")
4. For the final result, some steps for quality assurance should be done afterwards:
   - Check the resulting parking lane data for bugs, depending on how accurate you need it to be. Street segments with diagonal or perpendicular parking have the highest potential for accuracy failures, depending on how accurately the OSM data is mapped.
   - Locate objects that affect parking in parking lanes (e.g. street trees or lanterns in the parking lane area, street furniture in kerbside parking) and cut them off from the parking lane segments.


## Note

- Directory: Make sure that the following directory structure exists.

  ```
  └ your-directory
    ├ data/
    ┊ └ input.geojson
    └ styles/
      └ [various style files for provisional rendering].qml
  ```

- Coordinate Reference System: Results are saved in EPSG:25833 (ETRS89 / UTM zone 33N). A different CRS may be necessary at other locations and can be set in the script.

- Highway Line Representation: There is no consensus yet on which line the highway objekt in OSM represents exactly: The centerline of the carriageway or the driving line. So far, this script calculates the location of parking lanes according to variant B in [this figure](https://wiki.openstreetmap.org/wiki/File:Highway_representation.png) (driving line). ![](https://wiki.openstreetmap.org/wiki/File:Highway_representation.png)

- This script is intended for the calculation of parking spaces on (or next to) the street. Depending on your needs, it may be useful to include parking spaces in car parks, multi-storey car parks, underground garages, etc.

- Background: This script was originally based on very basic programming and QGIS knowledge. Many steps have been solved more effectively in the meantime, but there are more that can certainly be solved much more elegantly. Plus there are still some (marked) TODO's that would make it even better. I am happy about improvements and extensions!

## Changelog

- 2022-06-25 + Added error if input file don't exist
- 2022-06-23 + Added processing for facilities on the carriageway (bicycle parking, parkletts)
- 2022-06-22 + Added processing for separately mapped street side/lane parking
- 2022-06-18 * Extremely optimised data preparation (script runtime reduced more than 8 times)
- 2022-06-10 * Identifier for the side of the street (right/left/separate) is stored as a new attribute and not as a suffix of the ID
- 2022-06-09 + Added processing and buffer rendering of bus stops
- 2022-06-09 * Road segments without parking lanes are stored separately instead of simply being deleted
- 2022-06-03 + [Overpass Query] Added an BBOX-by-coordinates option and bus stops in the overpass query
- 2022-06-03 * Updated `styles/parking_lanes.qml` for correct rendering of reverse parking lane line directions (see below)
- 2022-06-03 * Reverse parking lane line directions to get lines pointing in the same direction as the traffic flow (for right-hand traffic)
- 2022-06-03 + Added `crossing:buffer_protection` to crossing types that are buffered
- 2022-06-03 * Variables instead of fixed values for buffer radii
- 2022-02-02 ! Fixed imports and set `path` within Python
- 2021-06-18 + Added support/attribute for `parking:condition:...:vehicles`
- 2021-03-11 + Added new method to correctly exclude parking lanes in the intersection area
- 2021-03-11 + Added note on inclusion of separately mapped parking spaces
- 2021-03-11 ! Fixed that parking point chain was only displayed, but could not be moved, used or saved
- 2021-03-11 ! Fixed parking point chain offset from street_side parking lanes
- 2021-03-11 ! Fixed "time.strftime"-error under certain rare circumstances in def prepareParkingLane (rearranged processing print outputs)
