import math

def to_radians(degree):
    return degree * math.pi / 180

def calculate_distance(coord1, coord2):
    earth_radius = 6371000

    coord1_parts = coord1.split(',')
    coord2_parts = coord2.split(',')

    lat1 = float(coord1_parts[0])
    lon1 = float(coord1_parts[1])
    lat2 = float(coord2_parts[0])
    lon2 = float(coord2_parts[1])

    lat_rad1 = to_radians(lat1)
    lon_rad1 = to_radians(lon1)
    lat_rad2 = to_radians(lat2)
    lon_rad2 = to_radians(lon2)

    lat_diff = lat_rad2 - lat_rad1
    lon_diff = lon_rad2 - lon_rad1

    a = math.sin(lat_diff / 2) * math.sin(lat_diff / 2) + \
        math.cos(lat_rad1) * math.cos(lat_rad2) * math.sin(lon_diff / 2) * math.sin(lon_diff / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = earth_radius * c

    return distance
