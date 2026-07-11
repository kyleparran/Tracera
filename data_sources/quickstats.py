"""USDA NASS QuickStats — yields, production, acreage, prices.

Prototype & docs: Prototype_quick_Stats.ipynb
"""
import requests
import pandas as pd
from ._common import get_key, SAMPLE_FARM

BASE = "https://quickstats.nass.usda.gov/api/api_GET/"


def quickstats(**params) -> pd.DataFrame:
    """Query the QuickStats API and return a tidy DataFrame.

    Common filters: commodity_desc, statisticcat_desc, agg_level_desc,
    state_alpha, county_name, year (append __GE/__LE for ranges).
    """
    params = {"key": get_key("NASS_API_KEY"), "format": "JSON", **params}
    r = requests.get(BASE, params=params, timeout=60)
    if r.status_code == 400:                      # too-broad / empty query
        raise ValueError(r.json().get("error", r.text))
    r.raise_for_status()
    return pd.DataFrame(r.json()["data"])


def county_yield(commodity="CORN", state=None, county=None, since=2000) -> pd.DataFrame:
    """County yield history (bu/acre) for a commodity."""
    state = state or SAMPLE_FARM["state_alpha"]
    county = county or SAMPLE_FARM["county_name"]
    df = quickstats(commodity_desc=commodity, statisticcat_desc="YIELD",
                    agg_level_desc="COUNTY", state_alpha=state, county_name=county,
                    year__GE=str(since), reference_period_desc="YEAR")
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    return df.sort_values("year").reset_index(drop=True)
