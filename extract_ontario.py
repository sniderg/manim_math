import json

with open("assets/ontario.geojson", "r") as f:
    data = json.load(f)

print(f"Total features: {len(data['features'])}")

ontario_feature = None
for feature in data['features']:
    props = feature.get('properties', {})
    # Check common property names for name
    name = props.get('name') or props.get('NAME') or props.get('nom')
    if name and 'Ontario' in name:
        ontario_feature = feature
        print(f"Found Ontario: {name}")
        break

if ontario_feature:
    output_data = {
        "type": "FeatureCollection",
        "features": [ontario_feature]
    }
    with open("assets/ontario.geojson", "w") as f:
        json.dump(output_data, f)
    print("Saved assets/ontario.geojson")
else:
    print("Could not find Ontario in features.")
