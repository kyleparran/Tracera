"""Shared helpers for the Tracera data-source notebooks.

Two jobs:
  1. Load API credentials from the project ``.env``.
  2. Expose ONE sample farm location so every source is queried at the same
     place and the results are cross-comparable.
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


# --- Sample farm: Story County, Iowa -------------------------------------
# Central Iowa corn/soybean country — well covered by every US data source.
SAMPLE_FARM = {
    "name": "Story County, Iowa (sample farm)",
    # A point on real cropland (verified corn/corn/soybean rotation in the
    # USDA Cropland Data Layer) so every source returns representative data.
    "lat": 42.05,
    "lon": -93.50,
    "state_alpha": "IA",
    "state_fips": "19",
    "county_fips": "169",   # county portion only
    "fips": "19169",        # full state+county FIPS
    "county_name": "STORY",
}


def field_polygon(lat: float | None = None, lon: float | None = None,
                  half_side_deg: float = 0.0045) -> dict:
    """A small square GeoJSON polygon (~1 km across) around a point.

    Used for field-scale queries (OpenET, Planetary Computer). The default
    half-side of ~0.0045 deg is roughly 500 m, i.e. a ~1 km x 1 km field.
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
    print("Repo root :", REPO_ROOT)
    print("Sample farm:", SAMPLE_FARM["name"], f'({SAMPLE_FARM["lat"]}, {SAMPLE_FARM["lon"]})')
    print("NASS key present:", bool(get_key("NASS_API_KEY", required=False)))
