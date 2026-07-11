"""Historical weather helpers (global Open-Meteo + US gridMET).

Prototypes & docs: open_meteo_historical.ipynb, gridmet.ipynb, nasa_power_api.ipynb
"""
import requests
import pandas as pd
from ._common import SAMPLE_FARM

_OPEN_METEO_DAILY = ("temperature_2m_max", "temperature_2m_min",
                     "precipitation_sum", "et0_fao_evapotranspiration")


def open_meteo_daily(start, end, lat=None, lon=None, daily=_OPEN_METEO_DAILY) -> pd.DataFrame:
    """Daily reanalysis weather anywhere (no key). Dates as 'YYYY-MM-DD'."""
    lat = SAMPLE_FARM["lat"] if lat is None else lat
    lon = SAMPLE_FARM["lon"] if lon is None else lon
    r = requests.get("https://archive-api.open-meteo.com/v1/archive", params={
        "latitude": lat, "longitude": lon, "start_date": start, "end_date": end,
        "daily": ",".join(daily), "timezone": "America/Chicago"}, timeout=60)
    r.raise_for_status()
    d = r.json()["daily"]
    return pd.DataFrame(d).assign(time=lambda x: pd.to_datetime(x["time"])).set_index("time")


# gridMET aggregated-file token -> internal NetCDF variable name (US only, ~4 km).
GRIDMET = {
    "tmmx": "daily_maximum_temperature",                     # K
    "tmmn": "daily_minimum_temperature",                     # K
    "pr":   "precipitation_amount",                          # mm
    "pet":  "daily_mean_reference_evapotranspiration_grass", # mm (reference ET)
    "vpd":  "daily_mean_vapor_pressure_deficit",             # kPa
}
_THREDDS = "http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_met_{tok}_1979_CurrentYear_CONUS.nc"


def gridmet_series(tok, start, end, lat=None, lon=None) -> pd.Series:
    """gridMET daily point series via OPeNDAP (scaling applied by xarray). US only."""
    import xarray as xr
    lat = SAMPLE_FARM["lat"] if lat is None else lat
    lon = SAMPLE_FARM["lon"] if lon is None else lon
    ds = xr.open_dataset(_THREDDS.format(tok=tok), engine="pydap")
    return (ds[GRIDMET[tok]].sel(lat=lat, lon=lon, method="nearest")
                            .sel(day=slice(start, end)).to_series())
