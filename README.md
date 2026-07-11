# Tracera — Agricultural Data Sources

A vetted library of **20 data sources** for an app that helps farmers make decisions from
historical data — **weather, soil, yields, water, vegetation, risk, and markets**. Each source
has its own notebook that documents what it offers *and* contains a **working API connection**
returning a tidy `pandas` DataFrame.

Every point/field query uses one shared sample location — **Story County, Iowa** (a real
corn/soybean field at `42.05, -93.50`) — so results are directly comparable across sources.

> **US-focused** (USDA/gov sources prioritized) · **free-first** (16 of 20 run with no paid key)
> · satellite via **Microsoft Planetary Computer**.

---

## Quick start

```bash
python -m pip install -r requirements.txt      # deps
cp .env.example .env                            # then add any keys you have
jupyter lab                                     # open any notebook and Run All
```

Start with **`00_data_sources_index.ipynb`** — the catalog + a live smoke-test of the free stack.

---

## The 20 sources

Legend — **Key:** 🔑 needs a free key · 💤 optional key · ⭕ none. **Live** = runs today as shipped.

### Crops, yields & farm economics
| Source | Notebook | What you get | Key | Live |
|---|---|---|:--:|:--:|
| NASS QuickStats | `Prototype_quick_Stats.ipynb` | Yields, production, acreage, prices (county→national) | 🔑 *(you have it)* | ✅ |
| ERS ARMS | `ers_arms.ipynb` | Farm financials, costs & returns, practices | 💤 *(DEMO_KEY works)* | ✅ |

### Soil
| Source | Notebook | What you get | Key | Live |
|---|---|---|:--:|:--:|
| SSURGO (Soil Data Access) | `soil_ssurgo.ipynb` | Survey-grade soil profile: texture, AWC, OM, pH, drainage | ⭕ | ✅ |
| ISRIC SoilGrids | `soil_grids.ipynb` | Global 250 m soil properties (fallback / cross-check) | ⭕ | ✅¹ |

### Weather & climate (historical)
| Source | Notebook | What you get | Key | Live |
|---|---|---|:--:|:--:|
| gridMET | `gridmet.ipynb` | 4 km daily US weather + reference ET, 1979→ | ⭕ | ✅ |
| NASA POWER | `nasa_power_api.ipynb` | Daily solar + meteorology + soil wetness, global | ⭕ | ✅ |
| Open-Meteo | `open_meteo_historical.ipynb` | Daily reanalysis + ET0, global, 1940→ | ⭕ | ✅ |
| NOAA NCEI / CDO | `Prototype_weather_noaa.ipynb` | Official station records (GHCN-Daily) | 💤 | ✅² |

### Water & evapotranspiration
| Source | Notebook | What you get | Key | Live |
|---|---|---|:--:|:--:|
| OpenET | `openet.ipynb` | Field-scale actual evapotranspiration (water use) | 🔑 | 🔑³ |
| USGS NWIS | `usgs_water.ipynb` | Streamflow & groundwater levels | ⭕ | ✅ |
| NRCS SCAN/SNOTEL | `nrcs_scan_snotel.ipynb` | In-situ station precip/temp (soil moisture varies) | ⭕ | ✅ |

### Vegetation & remote sensing
| Source | Notebook | What you get | Key | Live |
|---|---|---|:--:|:--:|
| Sentinel-2 NDVI (Planetary Computer) | `satellite_ndvi.ipynb` | 10 m crop-health NDVI time series | 💤 | ✅ |
| Soil moisture + VegScape/CROP-CASMA | `vegscape_cropcasma.ipynb` | Gridded soil moisture (POWER) + USDA MODIS/SMAP refs | ⭕ | ✅ |
| Cropland Data Layer | `cropland_cdl.ipynb` | Per-field crop rotation history + county acreage | ⭕ | ✅ |

### Risk & drought
| Source | Notebook | What you get | Key | Live |
|---|---|---|:--:|:--:|
| US Drought Monitor | `drought_monitor.ipynb` | Weekly drought category by county, 2000→ | ⭕ | ✅ |
| RMA Cause of Loss | `rma_crop_loss.ipynb` | *Why* crops failed + indemnities (county×crop×cause) | ⭕ | ✅ |

### Markets & terrain
| Source | Notebook | What you get | Key | Live |
|---|---|---|:--:|:--:|
| Grain futures (Yahoo) | `cme.ipynb` | Corn/soy/wheat daily prices (CME direct is paid) | ⭕ | ✅ |
| AMS Market News | `ams_market_news_prototype.ipynb` | Local cash / terminal prices (→ basis) | 🔑 | ✅ |
| FRED | `fred_prototype.ipynb` | Input costs, PPIs, rates, macro | 🔑 | ✅ |
| USGS 3DEP elevation | `usgs_elevation.ipynb` | Elevation → slope/aspect for a field | ⭕ | ✅ |

¹ SoilGrids is heavily rate-limited (frequent 503s); the notebook retries and degrades gracefully.
² NOAA token configured — runs live via the token-free NCEI service plus the CDO API.
³ Key configured and confirmed valid (Tier 1); OpenET's *data* endpoint currently returns a
  transient server-side error, so the notebook shows account status and handles it gracefully —
  it will return ET once OpenET's backend recovers.

---

## Credentials you need

Most sources need **nothing**. To light up the remaining few, get these free keys and paste them
into `.env`:

| Env var | For | Where | Needed? |
|---|---|---|---|
| `NASS_API_KEY` | QuickStats | quickstats.nass.usda.gov/api | ✅ set |
| `OPENET_API_KEY` | OpenET (water use) | etdata.org → request key | ✅ set (valid; data API in temp outage) |
| `FRED_API_KEY` | FRED (economics) | fredaccount.stlouisfed.org/apikeys | ✅ set — live |
| `AMS_API_KEY` | AMS Market News | mymarketnews.ams.usda.gov | ✅ set — live |
| `ERS_API_KEY` | ERS ARMS | api.data.gov/signup | ✅ set — live |
| `NOAA_CDO_TOKEN` | NOAA station search | ncdc.noaa.gov/cdo-web/token | ✅ set — live |
| `PC_SDK_SUBSCRIPTION_KEY` | Planetary Computer (Sentinel-2) | not required — anonymous access | ⭕ not needed |
| `PC_SDK_SUBSCRIPTION_KEY` | Planetary Computer | planetarycomputer.microsoft.com | optional (higher limits) |

`.env` is git-ignored. `.env.example` documents the same list.

---

## Repo layout

```
Tracera/
├── 00_data_sources_index.ipynb   # catalog + live smoke-test of the free stack
├── <source>.ipynb                # 20 source notebooks (see table above)
├── data_sources/                 # reusable, importable helpers
│   ├── _common.py                #   .env loader + SAMPLE_FARM + field_polygon()
│   ├── quickstats.py  cdl.py  weather.py  futures.py  elevator.py
│   └── __init__.py
├── requirements.txt
├── .env / .env.example
└── data_cache/                   # on-demand downloads (git-ignored)
```

## Reusable package

The notebooks are prototypes; the stable pull functions are distilled into `data_sources/`:

```python
from data_sources import SAMPLE_FARM
from data_sources.quickstats import county_yield
from data_sources.cdl import cdl_rotation, cdl_county_acreage
from data_sources.weather import open_meteo_daily, gridmet_series
from data_sources.elevator import elevation, slope_aspect
from data_sources.futures import grain_futures

cdl_rotation(years=range(2021, 2024))   # -> Corn / Corn / Soybeans at the sample field
```

## How the sources combine (decisions Tracera can support)

- **Yield benchmark** — QuickStats (county yield) × CDL (was this field even that crop?).
- **Water balance / irrigation** — OpenET (actual ET) − gridMET/Open-Meteo (reference ET & rain),
  with NASA POWER soil moisture and USGS/NWIS supply context.
- **Risk profile** — RMA Cause of Loss (what fails here) × Drought Monitor × SSURGO drainage.
- **Marketing** — futures (`cme`) + local cash (AMS) = **basis**; FRED + ERS ARMS for cost/margin.
- **In-season crop health** — Sentinel-2 NDVI curve × soil moisture × GDD.
