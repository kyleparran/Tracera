"""USGS 3DEP elevation + slope/aspect.

Prototype & docs: usgs_elevation.ipynb
"""
import math
import requests
from ._common import SAMPLE_FARM

EPQS = "https://epqs.nationalmap.gov/v1/json"


def elevation(lat=None, lon=None) -> float:
    """Ground elevation (metres) at a point from USGS 3DEP."""
    lat = SAMPLE_FARM["lat"] if lat is None else lat
    lon = SAMPLE_FARM["lon"] if lon is None else lon
    r = requests.get(EPQS, params={"x": lon, "y": lat, "units": "Meters",
                     "wkid": 4326, "includeDate": False}, timeout=60)
    r.raise_for_status()
    return float(r.json()["value"])


def slope_aspect(lat=None, lon=None, d=0.0014) -> dict:
    """Approximate slope (%) and aspect (deg) from a small elevation cross (~150 m)."""
    lat = SAMPLE_FARM["lat"] if lat is None else lat
    lon = SAMPLE_FARM["lon"] if lon is None else lon
    north, south = elevation(lat + d, lon), elevation(lat - d, lon)
    east, west = elevation(lat, lon + d), elevation(lat, lon - d)
    span_m = 2 * d * 111_000
    dz_ns, dz_ew = north - south, east - west
    slope = math.hypot(dz_ns, dz_ew) / span_m * 100
    aspect = (math.degrees(math.atan2(dz_ew, dz_ns)) + 360) % 360
    return {"slope_pct": round(slope, 2), "aspect_deg": round(aspect, 0)}
