# Some research notes about how to automate the downloading of overpass queries.

## Constrians

Since everything here are Python scripts that ran from within QGIS, this scripts should as well.

## OSM JSON to GeoJSON

https://pypi.org/project/osm2geojson/

```
pip install osm2geojson
json2geojson(dict json_from_overpass)
```

```python
import codecs
import osm2geojson

with codecs.open('file.json', 'r', encoding='utf-8') as data:
    json = data.read()

shapes_with_props = osm2geojson.json2shapes(json)
# >> [ { "shape": <Shapely-object>, "properties": {...} }, ... ]
```

## Overpass API Query <<<- das hier müsste direkt geojson ausgeben

https://github.com/mvexel/overpass-api-python-wrapper

ABER: Sucht neuen Maintainer.

```python
import overpass
api = overpass.API()
# api = overpass.API(endpoint="https://overpass.myserver/interpreter")
# "out body; >; out skql qt;" ==> "out geom", siehe https://gis.stackexchange.com/a/187754/194701
response = api.get('node["name"="Salt Lake City"]', verbosity='out geom', responseformat="geojson")
```

## Overpass API Query

https://github.com/DinoTools/python-overpy
https://python-overpy.readthedocs.io/en/latest/example.html

ABER: Unklar, wie ich daraus dann GeoJSON baue.

```
pip install overpy
```

```python
import overpy

api = overpy.Overpass()

# fetch all ways and nodes
result = api.query("""
    way(50.746,7.154,50.748,7.157) ["highway"];
    (._;>;);
    out body;
    """)
```

## Tools, Links

- Step by step tutorial https://janakiev.com/blog/openstreetmap-with-python-and-overpass-api/

- Statistik Tool https://github.com/mocnik-science/osm-python-tools
