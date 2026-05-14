from datetime import datetime, timedelta
from math import radians, degrees, sin, cos, atan2, asin
import gpxpy.gpx

# -----------------------------
# INPUTS
# -----------------------------
start_lat = 40.7128
start_lon = -74.0060

speed_mps = 7.8               # meters per second
distance_m = 28164            # total distance traveled in meters
bearing_deg = 45            # northeast

num_points = 3600

# -------------------------------------------------
# EARTH CONSTANTS
# -------------------------------------------------
EARTH_RADIUS_M = 6371000

# -------------------------------------------------
# DESTINATION CALCULATION
# -------------------------------------------------
def destination_point(lat, lon, bearing_deg, distance_m):
    lat1 = radians(lat)
    lon1 = radians(lon)
    bearing = radians(bearing_deg)

    angular_distance = distance_m / EARTH_RADIUS_M

    lat2 = asin(
        sin(lat1) * cos(angular_distance) +
        cos(lat1) * sin(angular_distance) * cos(bearing)
    )

    lon2 = lon1 + atan2(
        sin(bearing) * sin(angular_distance) * cos(lat1),
        cos(angular_distance) - sin(lat1) * sin(lat2)
    )

    return degrees(lat2), degrees(lon2)

# Calculate destination
end_lat, end_lon = destination_point(
    start_lat,
    start_lon,
    bearing_deg,
    distance_m
)

print("Destination:", end_lat, end_lon)

# -------------------------------------------------
# GPX GENERATION
# -------------------------------------------------
gpx = gpxpy.gpx.GPX()

track = gpxpy.gpx.GPXTrack()
gpx.tracks.append(track)

segment = gpxpy.gpx.GPXTrackSegment()
track.segments.append(segment)

start_time = datetime.utcnow()

total_time_sec = distance_m / speed_mps
time_step = total_time_sec / (num_points - 1)

# Create intermediate points
for i in range(num_points):
    fraction = i / (num_points - 1)

    lat = start_lat + (end_lat - start_lat) * fraction
    lon = start_lon + (end_lon - start_lon) * fraction

    point_time = start_time + timedelta(seconds=i * time_step)

    point = gpxpy.gpx.GPXTrackPoint(
        latitude=lat,
        longitude=lon,
        elevation=0,
        time=point_time
    )

    segment.points.append(point)

# -------------------------------------------------
# SAVE GPX
# -------------------------------------------------
with open("generated_route.gpx", "w") as f:
    f.write(gpx.to_xml())

print("GPX file written: generated_route.gpx")