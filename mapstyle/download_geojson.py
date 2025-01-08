import requests
import json

# change to your bounding box
bbox = "52.4543246009110788,13.3924347464750326,52.5009195009107046,13.4859782"

# change if needed
rootdir = "~/strassenraumkarte-neukoelln/mapstyle/layer/geojson"

def overpass_to_file(file_basename, query):
    print(f"START to query {file_basename}...")
    data = api_request(query)

    print(f"... write {file_basename} to file...")
    with open(f"{rootdir}/{file_basename}.geojson", 'w') as f:
        json.dump(data, f)

    print(f"...DONE {file_basename}")

def api_request(query):
    data = f"[out:json][bbox:{bbox}];{query}out body;>;out skel qt;"
    res = requests.request(method='get', url='https://overpass-api.de/api/interpreter', data=data)
    return res.json()

overpass_to_file("amenity", f"""
                 (
                     nwr["amenity"];
                    nwr["disused:amenity"];
                  );""")
overpass_to_file("area_highway", f"""
                 (
                    nwr["area:highway"];
                    nwr["road_marking"];
                    nwr["road_marking:forward"];
                    nwr["road_marking:backward"];
                    nwr["road_marking:left"];
                    nwr["road_marking:right"];
                );
                 """)
overpass_to_file("barriers", f"""
                 (
                    nwr["barrier"]["location"!='underground']["level"!="-1"]["level"!="-2"]["level"!="-3"];
                 );
                 """)
overpass_to_file("bridge", f"""
                 (
                    way["man_made"='bridge'];
                    relation["man_made"='bridge'];
                 );
                 """)
overpass_to_file("building_part", f"""
                 (
                    way["building:part"]["location"!='underground']["level"!="-1"]["level"!="-2"]["level"!="-3"];
                 );
                 """)
overpass_to_file("buildings", f"""
                 (
                    nwr["building"]["location"!='underground']["level"!="-1"]["level"!="-2"]["level"!="-3"];
                 );
                 """)
overpass_to_file("entrance", f"""
                 (
                    node["entrance"];
                    node["entrance_marker:subway"];
                    node["entrance_marker:s-train"];
                 );
                 """)
overpass_to_file("highway", f"""
                 (
                    // streets
                    way["highway"="primary"];
                    way["highway"="primary_link"];
                    way["highway"="secondary"];
                    way["highway"="secondary_link"];
                    way["highway"="tertiary"];
                    way["highway"="tertiary_link"];
                    way["highway"="residential"];
                    way["highway"="unclassified"];
                    way["highway"="living_street"];
                    way["highway"="pedestrian"];
                    way["highway"="road"];
                    way["highway"="service"];
                    way["highway"="track"];
                    way["highway"="bus_guideway"];

                    // streets under construction
                    way["highway"="construction"]["construction"="primary"];
                    way["highway"="construction"]["construction"="primary_link"];
                    way["highway"="construction"]["construction"="secondary"];
                    way["highway"="construction"]["construction"="secondary_link"];
                    way["highway"="construction"]["construction"="tertiary"];
                    way["highway"="construction"]["construction"="tertiary_link"];
                    way["highway"="construction"]["construction"="residential"];
                    way["highway"="construction"]["construction"="unclassified"];
                    way["highway"="construction"]["construction"="living_street"];
                    way["highway"="construction"]["construction"="pedestrian"];
                    way["highway"="construction"]["construction"="road"];
                    way["highway"="construction"]["construction"="service"];
                    way["highway"="construction"]["construction"="track"];
                    way["highway"="construction"]["construction"="bus_guideway"];

                    // bus stops
                    way["highway"="platform"];
                    way["public_transport"="platform"];
                    node["highway"="bus_stop"];

                    // crossings and traffic signals
                    node["highway"="traffic_signals"];
                    node["highway"="crossing"];
                    node["highway"="stop"];
                    node["highway"="give_way"];
                    node["kerb"];

                    // traffic calming
                    nwr["traffic_calming"];

                 );
                 """)
overpass_to_file("housenumber", f"""
                 (
                    nwr["addr:housenumber"][!"name"][!"disused:name"][!"amenity"][!"shop"][!"disused:amenity"][!"disused:shop"][!"healthcare"][!"office"][!"leisure"][!"craft"];
                 );
                 """)
overpass_to_file("landuse", f"""
                 (
                    way["landuse"];
                    relation["landuse"];
                    way["landcover"];
                    relation["landcover"];
                 );
                 """)
overpass_to_file("leisure", f"""
                 (
                    nwr["leisure"];
                 );
                 """)
overpass_to_file("man_made", f"""
                 (
                    nwr["man_made"='water_well'];
                    nwr["man_made"='monitoring_station'];
                    nwr["man_made"='mast'];
                    nwr["man_made"='pole'];
                    nwr["man_made"='flagpole'];
                    nwr["man_made"='chimney'];
                    nwr["man_made"='street_cabinet'];
                    nwr["man_made"='manhole'];
                    nwr["man_made"='planter'];
                    nwr["man_made"='guard_stone'];

                    nwr["man_made"='embankment'];

                    nwr["highway"='street_lamp'];
                    nwr["highway"='traffic_sign'];

                    nwr["advertising"];

                    nwr["emergency"='fire_hydrant'];

                    nwr["tourism"='artwork'];
                    nwr["tourism"='information'];

                    nwr["historic"='memorial'];

                    nwr["amenity"='loading_ramp'];
                    nwr["amenity"='vending_machine']["vending"='parking_tickets'];
                 );
                 """)
overpass_to_file("motorway", f"""
                 (
                    way["highway"="motorway"];
                    way["highway"="trunk"];
                    way["highway"="motorway_link"];
                    way["highway"="trunk_link"];
                 );
                 """)
overpass_to_file("natural", f"""
                 (
                    nwr["natural"];
                 );
                 """)
overpass_to_file("path", f"""
                 (
                    way["highway"="path"];
                    way["highway"="footway"];
                    way["highway"="steps"];
                    way["highway"="cycleway"];

                    way["highway"="track"];
                 );
                 """)
overpass_to_file("place", f"""
                 (
                    nwr["place"];
                 );
                 """)
overpass_to_file("playground", f"""
                 (
                    nwr["playground"];
                    nwr["skatepark:obstacles"];
                 );
                 """)
overpass_to_file("railway", f"""
                 (
                    nwr["railway"];
                 );
                 """)
overpass_to_file("routes", f"""
                 (
                    relation["route"="bicycle"];
                 );
                 """)
overpass_to_file("waterway", f"""
                 (
                    way["waterway"];
                 );
                 """)

