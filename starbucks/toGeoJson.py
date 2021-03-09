import json
import sys

import geojson

data = json.load(sys.stdin)

name = []
for name, name_data in data['Name'].items():
    locations = []
    for location in name_data['locations']:
        locations.append((float(location['latitude']), float(location['longitude'])))
        
name.append(geojson.Feature(geometry=geojson.MultiPoint(locations), properties={'Name': name}))

result = geojson.GeometryCollection(projects)
geojson.dump(result, sys.stdout)