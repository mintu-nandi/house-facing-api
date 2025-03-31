import requests

def get_house_entrance(lat, lon):
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node["entrance"](around:20,{lat},{lon});
    out;
    """
    response = requests.get(overpass_url, params={'data': query})
    data = response.json()

    if "elements" in data and len(data["elements"]) > 0:
        entrance = data["elements"][0]  # Take the first entrance found
        return entrance["lat"], entrance["lon"]
    return None, None
