# parking_lanes.py for QGIS

**Python script for QGIS to generate parking lanes from OSM data**

## How to use

1. Run Overpass-Query for street and parking lane data: [https://overpass-turbo.eu/s/1j0u](https://overpass-turbo.eu/s/1j0u)
2. Export result as GeoJSON to 'data/input.geojson'
3. Run this python script in QGIS
   1. "Plugins" => "Python Console"
   1. (If internal Python Editor Panel is hidden: Right click in Console => "Show Editor")
   1. Open File in QGIS Python Editor
   1. Run from there
      Note: Do _not_ use the "Browser" => File => "Run Script"
4. For the final result, separate steps still have to be done individually afterwards:

   - Include bus stops and cut the parking lanes on the side of the road where they are located.
     TODO: This could be automated by snapping bus stops or waiting areas to nearby parking lane segments, searching for the nearest side of the road to cut them on that side only.
   - Locate objects that affect parking in parking lanes (e.g. street trees or lanterns in the parking lane area, street furniture in kerbside parking) and cut them off from the parking lane segments.
   - Check the resulting parking lane data for bugs, depending on how accurate you need it to be.
   - Include separately mapped parking areas if needed (parking=surface, street_side etc.)

## Note

- Directory: Make sure that the following directory structure exists.

  ```
  └ your-directory
    ├ data/
    ┊ └ input.geojson
    └ styles/
      └ [various style files for provisional rendering].qml
  ```

- Coordinate Reference System: Results are saved in EPSG:25833 (ETRS89 / UTM zone 33N). A different CRS may be necessary at other locations (see below).

- Highway Line Representation: There is no consensus yet on which line the highway objekt in OSM represents exactly: The centerline of the carriageway or the driving line. So far, this script calculates the location of parking lanes according to variant B in [this figure](https://wiki.openstreetmap.org/wiki/File:Highway_representation.png) (driving line). ![](https://wiki.openstreetmap.org/wiki/File:Highway_representation.png)

- Background: This script is based on very basic programming and QGIS knowledge. Many steps can certainly be solved much more effectively or elegantly, plus there are still some (marked) TODO's that would make it even better. I am happy about improvements and extensions!

## Changelog

- 2022-06-03 + Added an BBOX-by-coordinates option and bus stops in the overpass query
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
