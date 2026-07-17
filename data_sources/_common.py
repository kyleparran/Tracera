"""Shared helpers for the Tracera data-source notebooks.

Two jobs:
  1. Load API credentials from the project ``.env``.
  2. Expose the farm ``FIELDS`` so every source is queried at the same
     place(s) and the results are cross-comparable.
"""
from __future__ import annotations

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # dotenv is optional; env vars may be provided another way
    load_dotenv = None

# Repo root = parent of this file's directory (data_sources/..)
REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = REPO_ROOT / ".env"


def load_env() -> None:
    """Load variables from the project .env into os.environ (idempotent)."""
    if load_dotenv is not None:
        load_dotenv(ENV_PATH)


def get_key(name: str, *, required: bool = True) -> str:
    """Return an env var, with a clear message if it is missing.

    Pass ``required=False`` to get an empty string instead of raising.
    """
    load_env()
    val = os.environ.get(name, "").strip()
    if not val and required:
        raise RuntimeError(
            f"Missing credential '{name}'. Add it to {ENV_PATH} "
            f"(see README.md for the free signup link)."
        )
    return val


# --- Farm fields ---------------------------------------------------------
# Add a field by copying a block below. Each field carries its county so the
# county-level sources (QuickStats, CDL acreage, Drought Monitor, RMA) work
# per field. Both current fields are in Monroe County, Michigan (FIPS 26115).
input_name_farm_1 = "Ault's"
input_name_farm_2 = "Rado's"

FIELDS = [
    {
        "id": input_name_farm_1,
        "name": "North 80",
        "lat": 41.896389,
        "lon": -83.623750,
        "crop": "corn",
        "acres": 20.49,
        "state_alpha": "MI",
        "state_fips": "26",
        "county_name": "MONROE",
        "county_fips": "115",
        "fips": "26115",
    },
    {
        "id": input_name_farm_2,
        "name": "Field 2",
        "lat": 41.909583,
        "lon": -83.632444,
        "crop": "soybeans",
        "acres": 67,
        "state_alpha": "MI",
        "state_fips": "26",
        "county_name": "MONROE",
        "county_fips": "115",
        "fips": "26115",
    },
]

# Primary field used by the single-field source notebooks. Every notebook
# imports SAMPLE_FARM; point it at whichever field you want, or loop FIELDS.
SAMPLE_FARM = FIELDS[0]


def get_field(field_id: str) -> dict:
    """Look up a field by its id, e.g. get_field("Ault's")."""
    for f in FIELDS:
        if f["id"] == field_id:
            return f
    raise KeyError(f"No field {field_id!r}. Known ids: {[f['id'] for f in FIELDS]}")


def field_polygon(lat: float | None = None, lon: float | None = None,
                  half_side_deg: float = 0.0045) -> dict:
    """A small square GeoJSON polygon (~1 km across) around a point.

    Defaults to the primary field (SAMPLE_FARM). Used for field-scale
    queries (OpenET, Planetary Computer). Half-side ~0.0045 deg ≈ 500 m.
    """
    lat = SAMPLE_FARM["lat"] if lat is None else lat
    lon = SAMPLE_FARM["lon"] if lon is None else lon
    d = half_side_deg
    return {
        "type": "Polygon",
        "coordinates": [[
            [lon - d, lat - d],
            [lon + d, lat - d],
            [lon + d, lat + d],
            [lon - d, lat + d],
            [lon - d, lat - d],
        ]],
    }


if __name__ == "__main__":
    load_env()
    print("Repo root:", REPO_ROOT)
    for f in FIELDS:
        print(f"Field: {f['id']} / {f['name']} ({f['lat']}, {f['lon']}) "
              f"- {f['county_name']} Co, {f['state_alpha']} [{f['fips']}]")
    print("NASS key present:", bool(get_key("NASS_API_KEY", required=False)))
