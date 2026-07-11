"""USDA Cropland Data Layer — crop rotation history & county acreage.

Prototype & docs: cropland_cdl.ipynb
"""
import io
import re
import requests
import pandas as pd
from pyproj import Transformer
from ._common import SAMPLE_FARM

CDL = "https://nassgeodata.gmu.edu/axis2/services/CDLService"
_to_albers = Transformer.from_crs("EPSG:4326", "EPSG:5070", always_xy=True)


def cdl_value(year, lat=None, lon=None):
    """The crop grown at a point in a given year (reprojects lon/lat to Albers)."""
    lat = SAMPLE_FARM["lat"] if lat is None else lat
    lon = SAMPLE_FARM["lon"] if lon is None else lon
    x, y = _to_albers.transform(lon, lat)
    r = requests.get(f"{CDL}/GetCDLValue", params={"year": year, "x": x, "y": y}, timeout=90)
    r.raise_for_status()
    m = re.search(r'value: (\d+), category: "([^"]+)"', r.text)
    return {"year": year, "value": int(m.group(1)), "crop": m.group(2)} if m else None


def cdl_rotation(lat=None, lon=None, years=range(2015, 2025)) -> pd.DataFrame:
    """Multi-year crop rotation at a point."""
    return pd.DataFrame([cdl_value(y, lat, lon) for y in years]).set_index("year")


def cdl_county_acreage(year, fips=None) -> pd.DataFrame:
    """County crop acreage histogram for a year (GetCDLStat CSV)."""
    fips = fips or SAMPLE_FARM["fips"]
    r = requests.get(f"{CDL}/GetCDLStat", params={"year": year, "fips": fips, "format": "csv"}, timeout=120)
    url = re.search(r"<returnURL>(.*?)</returnURL>", r.text).group(1)
    df = pd.read_csv(io.StringIO(requests.get(url, timeout=60).text))
    df.columns = [c.strip() for c in df.columns]
    return df.sort_values("Acreage", ascending=False).reset_index(drop=True)
