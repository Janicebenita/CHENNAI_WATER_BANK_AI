"""Bundled source-derived evidence and validated user-supplied indicator overlays."""

from __future__ import annotations
import copy
import csv
import io
import json
import math
from pathlib import Path
from src.config.settings import PRIORITY_WEIGHTS
from src.geospatial.priority import indicators

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "priority"


def load_sample():
    return json.loads((DATA_DIR / "zones.geojson").read_text(encoding="utf-8"))


def apply_csv(collection, text):
    """Replace indicator rows only; never accept executable content or remote fetch URLs.

    Each supplied row describes all eight indicators plus source/date declarations.
    Blank indicators stay missing; original observations are not silently blended.
    """
    reader = csv.DictReader(io.StringIO(text))
    required = {"zone_id", "source", "period", *PRIORITY_WEIGHTS}
    if not required.issubset(reader.fieldnames or []):
        raise ValueError(
            "CSV requires zone_id, source, period and all eight indicator columns"
        )
    output = copy.deepcopy(collection)
    zones = {f["properties"]["zone_id"]: f["properties"] for f in output["features"]}
    seen = set()
    for row in reader:
        zone_id = row["zone_id"]
        if zone_id not in zones or zone_id in seen:
            raise ValueError("Unknown or duplicate zone_id")
        if not row.get("source", "").strip() or not row.get("period", "").strip():
            raise ValueError("Every row requires nonempty source and period")
        seen.add(zone_id)
        props = zones[zone_id]
        for key in PRIORITY_WEIGHTS:
            value = (row.get(key) or "").strip()
            if key in {"soil", "land_use"}:
                props[key] = value or None
            else:
                number = float(value) if value else None
                if number is not None:
                    if not math.isfinite(number):
                        raise ValueError("Nonfinite indicator values are not allowed")
                    bounds = {
                        "ndvi": (-1, 1),
                        "slope_deg": (0, 90),
                        "surface_water_pct": (0, 100),
                        "elevation_m": (-500, 9000),
                    }
                    low, high = bounds.get(key, (0, float("inf")))
                    if not low <= number <= high:
                        raise ValueError(f"Invalid physical range for {key}")
                props[key] = number
        indicators(props)
        props["source"] = row["source"].strip()
        props["period"] = row["period"].strip()
        props["provenance_status"] = "USER-SUPPLIED; NOT INDEPENDENTLY VERIFIED"
    if seen != set(zones):
        raise ValueError(
            "Supply exactly one row for every zone for comparable coverage"
        )
    return output


def csv_template(collection):
    out = io.StringIO()
    writer = csv.DictWriter(
        out, fieldnames=["zone_id", *PRIORITY_WEIGHTS, "source", "period"]
    )
    writer.writeheader()
    for f in collection["features"]:
        writer.writerow({"zone_id": f["properties"]["zone_id"]})
    return out.getvalue()
