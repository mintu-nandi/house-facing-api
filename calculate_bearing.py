import math

def calculate_bearing(lat1, lon1, lat2, lon2):
    """Calculate the compass direction (bearing) from house to entrance."""
    delta_lon = math.radians(lon2 - lon1)
    lat1, lat2 = map(math.radians, [lat1, lat2])

    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon))

    bearing = math.atan2(x, y)
    bearing = math.degrees(bearing)
    compass = ["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"]
    direction = compass[round(bearing / 45) % 8]

    return direction, bearing
