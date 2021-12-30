# post_processing.py for QGIS

**Python script for QGIS for post processing osm data for rendering in the micromap**

This script generates special data layers that improve the rendering of the "straßenraumkarte"/micromap. This includes in particular a processed lane layer to render lane markings.

## How to use

1. If other OSM data than the sample data are required, they can be downloaded via [Overpass querys](https://github.com/SupaplexOSM/strassenraumkarte-neukoelln/blob/main/scripts/post_processing/layer). Adjust the BBOX if you want to download the data for a different area than the example area (Berlin-Neukölln). Export the results to `layer/geojson/[layer name].geojson` (or any other directory, as defined in the script). The sample data are sufficient if you only want to generate the lane layer.
2. Open the post processing script and adjust the project directory (so that the osm data can be found). In the first few lines of the script you can select which processing steps are to be executed: For the lane markings, for example, set `proc_lane_markings=1` (default).
3. Run the python script in QGIS. The post processed layers are saved at `layers/geojson/post_processed` by default.

## The script includes these processing steps, among others

- Generating a layer for road markings - contains lines for individual lanes as well as attributes of how these lanes are marked.
- Processing of building parts to be able to represent building parts of different heights and "floating" building parts.
- Generating points within a hexagonal grid in forests to represent them more realistically.
- Alignment of street furniture such as street cabinets or street lamps to the nearest street if no orientation/direction is specified.
- Generating defined, continuous street segments for nicer street labelling.
