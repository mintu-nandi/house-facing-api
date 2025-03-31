from flask import Flask, request, jsonify
import requests
import math

app = Flask(__name__)

OS_PLACES_API_KEY = "YOUR_OS_API_KEY"
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"

def get_coordinates(address):
    """Fetch latitude & longitude from OS Places API"""
    url = f"https://api.os.uk/search/names/v1/find?query={address}&key={OS_PLACES_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "results" in data and len(data["results"]) > 0:
        lat = data["results"][0]["geometry"]["y"]
        lon = data["results"][0]["geometry"]["x"]
        return lat, lon
    return None, None

def get_house_entrance(lat, lon):
    """Fetch entrance location from OSM Overpass API"""
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node["entrance"](around:20,{lat},{lon});
    out;
    """
    response = requests.get(overpass_url, params={'data': query})
    data = response.json()

    if "elements" in data and len(data["elements"]) > 0:
        entrance = data["elements"][0]
        return entrance["lat"], entrance["lon"]
    return None, None

def get_street_view_image(lat, lon):
    """Fetch Google Street View image of house entrance"""
    url = f"https://maps.googleapis.com/maps/api/streetview?size=600x300&location={lat},{lon}&key={GOOGLE_API_KEY}"
    return url

def calculate_bearing(lat1, lon1, lat2, lon2):
    """Calculate compass direction from house to entrance"""
    delta_lon = math.radians(lon2 - lon1)
    lat1, lat2 = map(math.radians, [lat1, lat2])

    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon))

    bearing = math.atan2(x, y)
    bearing = math.degrees(bearing)
    compass = ["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"]
    direction = compass[round(bearing / 45) % 8]

    return direction, bearing

@app.route('/api/house-facing', methods=['GET'])
def house_facing():
    address = request.args.get('address')
    if not address:
        return jsonify({"error": "Address is required"}), 400

    lat, lon = get_coordinates(address)
    if lat is None:
        return jsonify({"error": "Could not retrieve location data"}), 404

    entrance_lat, entrance_lon = get_house_entrance(lat, lon)
    if entrance_lat is None:
        return jsonify({"error": "Could not find entrance"}), 404

    facing_direction, compass_angle = calculate_bearing(lat, lon, entrance_lat, entrance_lon)
    street_view_image = get_street_view_image(entrance_lat, entrance_lon)

    return jsonify({
        "address": address,
        "latitude": lat,
        "longitude": lon,
        "entrance_latitude": entrance_lat,
        "entrance_longitude": entrance_lon,
        "facing_direction": facing_direction,
        "compass_angle": compass_angle,
        "street_view_image": street_view_image
    })

if __name__ == '__main__':
    app.run(debug=True)
