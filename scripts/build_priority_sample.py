"""Optional preprocessing only: pip install rasterio Pillow. Runtime needs neither GDAL nor network.
Fetch immutable dated inputs, cache clipped arrays, then aggregate demonstration grid zones.
Run from repository root: python scripts/build_priority_sample.py
"""

from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import urllib.request
import numpy as np
from PIL import Image
import rasterio
from rasterio.vrt import WarpedVRT
from rasterio.transform import from_bounds
from rasterio.enums import Resampling

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/priority"
RAW = OUT / "source"
RAW.mkdir(parents=True, exist_ok=True)
BBOX = (80.10, 12.88, 80.28, 13.16)
WIDTH, HEIGHT = 360, 560
TRANSFORM = from_bounds(*BBOX, WIDTH, HEIGHT)
ITEM = "https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a/items/S2B_44PMV_20240229_0_L2A"
RAIN = "https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR&community=AG&longitude=80.2&latitude=13.0&start=20240101&end=20241231&format=JSON"
WATER = "https://storage.googleapis.com/global-surface-water/downloads2021/occurrence/occurrence_80E_20Nv1_4_2021.tif"
LAND = "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_N12E078_Map.tif"
urls = {}


def fetch(url, name):
    path = RAW / name
    urls[name] = url
    if not path.exists():
        with urllib.request.urlopen(url, timeout=90) as response:
            path.write_bytes(response.read())
    return path


def clip(url, name):
    urls[name + ".npz"] = url
    path = RAW / (name + ".npz")
    if path.exists():
        return np.load(path)["data"]
    with rasterio.Env(
        GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
        CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif",
        GDAL_HTTP_TIMEOUT="60",
    ):
        with rasterio.open(url) as src:
            with WarpedVRT(
                src,
                crs="EPSG:4326",
                transform=TRANSFORM,
                width=WIDTH,
                height=HEIGHT,
                resampling=Resampling.nearest,
            ) as vrt:
                data = vrt.read(1)
    np.savez_compressed(path, data=data)
    print("Clipped", name, flush=True)
    return data


def main():
    item = json.loads(fetch(ITEM, "sentinel_item.json").read_text())
    bands = {}
    for band in ("red", "nir", "scl"):
        bands[band] = clip(item["assets"][band]["href"], band)
    # Earth Search legacy COGs can already include the BOA offset. Respect item flag.
    applied = item["properties"].get("earthsearch:boa_offset_applied", False)
    for band in ("red", "nir"):
        meta = item["assets"][band]["raster:bands"][0]
        raw = bands[band].astype(float)
        bands[band] = raw * meta.get("scale", 1) + (
            0 if applied else meta.get("offset", 0)
        )
        bands[band][raw == 0] = np.nan
    valid = np.isin(bands["scl"], [4, 5]) & (bands["red"] >= 0) & (bands["nir"] >= 0)
    denominator = bands["nir"] + bands["red"]
    ndvi = np.full(denominator.shape, np.nan)
    np.divide(
        bands["nir"] - bands["red"],
        denominator,
        out=ndvi,
        where=valid & (denominator > 0),
    )
    land = clip(LAND, "worldcover")
    water = clip(WATER, "water_occurrence").astype(float)
    water[water > 100] = np.nan
    lons = BBOX[0] + (np.arange(WIDTH) + 0.5) * (BBOX[2] - BBOX[0]) / WIDTH
    lats = BBOX[3] - (np.arange(HEIGHT) + 0.5) * (BBOX[3] - BBOX[1]) / HEIGHT
    # Sample Terrarium pixels at the shared grid; slopes first computed at source resolution.
    z = 12
    xs = (lons + 180) / 360 * 2**z
    ys = (1 - np.arcsinh(np.tan(np.radians(lats))) / math.pi) / 2 * 2**z
    xmin, xmax = int(xs.min()), int(xs.max())
    ymin, ymax = int(ys.min()), int(ys.max())
    mosaic = np.empty(((ymax - ymin + 1) * 256, (xmax - xmin + 1) * 256))
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            url = f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
            rgb = np.asarray(
                Image.open(fetch(url, f"dem_{z}_{x}_{y}.png")).convert("RGB"),
                dtype=float,
            )
            mosaic[
                (y - ymin) * 256 : (y - ymin + 1) * 256,
                (x - xmin) * 256 : (x - xmin + 1) * 256,
            ] = rgb[:, :, 0] * 256 + rgb[:, :, 1] + rgb[:, :, 2] / 256 - 32768
    spacing = 40075016.686 * math.cos(math.radians(13.02)) / (2**z * 256)
    dy, dx = np.gradient(mosaic, spacing)
    slope = np.degrees(np.arctan(np.hypot(dx, dy)))
    rows = np.floor((ys - ymin) * 256).astype(int)
    cols = np.floor((xs - xmin) * 256).astype(int)
    elevation = mosaic[np.ix_(rows, cols)]
    slope = slope[np.ix_(rows, cols)]
    rain = json.loads(fetch(RAIN, "power_2024.json").read_text())
    days = rain["properties"]["parameter"]["PRECTOTCORR"]
    if len(days) != 366 or any(v < 0 for v in days.values()):
        raise ValueError("Incomplete daily rainfall: cannot label annual total")
    annual = sum(days.values())
    features = []
    labels = {
        10: "Tree cover",
        20: "Shrubland",
        30: "Grassland",
        40: "Cropland",
        50: "Built-up",
        60: "Bare / sparse vegetation",
        70: "Snow / ice",
        80: "Permanent water",
        90: "Herbaceous wetland",
        95: "Mangroves",
        100: "Moss / lichen",
    }
    for row in range(4):
        for col in range(3):
            sl = np.s_[row * 140 : (row + 1) * 140, col * 120 : (col + 1) * 120]
            west = BBOX[0] + col * 0.06
            east = west + 0.06
            north = BBOX[3] - row * 0.07
            south = north - 0.07
            values, counts = np.unique(land[sl][land[sl] > 0], return_counts=True)
            dominant = int(values[np.argmax(counts)]) if len(values) else None
            coverage = float(np.isfinite(ndvi[sl]).mean())
            props = {
                "zone_id": f"C{row + 1}{col + 1}",
                "zone": f"Chennai grid {row + 1}-{col + 1}",
                "elevation_m": round(float(np.mean(elevation[sl])), 3),
                "slope_deg": round(float(np.mean(slope[sl])), 3),
                "drainage_density_km_km2": None,
                "rainfall_mm": round(annual, 2),
                "ndvi": round(float(np.nanmean(ndvi[sl])), 4)
                if coverage >= 0.2
                else None,
                "land_use": labels.get(dominant),
                "soil": None,
                "surface_water_pct": round(float(np.nanmean(water[sl])), 3)
                if np.isfinite(water[sl]).any()
                else None,
                "ndvi_valid_fraction": round(coverage, 4),
                "rainfall_period": "2024 annual; shared regional POWER cell",
                "latitude": round((north + south) / 2, 5),
                "longitude": round((west + east) / 2, 5),
            }
            features.append(
                {
                    "type": "Feature",
                    "id": props["zone_id"],
                    "properties": props,
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [west, south],
                                [east, south],
                                [east, north],
                                [west, north],
                                [west, south],
                            ]
                        ],
                    },
                }
            )
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "bbox": BBOX,
        "crs": "EPSG:4326",
        "grid_resolution_degrees": 0.0005,
        "zone_type": "Demonstration Analysis Zones; rectangular grid, NOT delineated watersheds",
        "sentinel_date": "2024-02-29",
        "sentinel_boa_offset_already_applied": applied,
        "rainfall_period": "2024-01-01/2024-12-31",
        "worldcover_year": 2021,
        "surface_water_period": "1984-2021 JRC GSW v1.4; superseded product with known occurrence inconsistencies; screening only",
        "terrain_resolution_m_approx": round(spacing, 2),
        "files": {
            p.name: {
                "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                "source_url": urls.get(p.name),
            }
            for p in RAW.iterdir()
            if p.is_file()
        },
        "missing": ["drainage_density_km_km2", "soil"],
        "processing": "Nearest-neighbour common WGS84 sample grid (~54m), not exhaustive native-resolution zonal statistics. Mean DEM and source-gradient slope; cloud/shadow masked land NDVI from SCL 4/5 with >=20% valid grid coverage; modal WorldCover class. Annual rainfall sums 366 regional reanalysis days, shared across all zones. No spatial rainfall downscaling. Mean JRC long-term water occurrence over valid grid samples (0 included; 255 excluded), not water-area percentage. No water occurrence derived from a single image.",
    }
    (OUT / "zones.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": features}, indent=2)
    )
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(
        "Saved",
        len(features),
        "zones; annual regional rainfall",
        round(annual, 2),
        "mm",
        flush=True,
    )


if __name__ == "__main__":
    main()
