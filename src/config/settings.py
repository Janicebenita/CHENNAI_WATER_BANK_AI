"""Central application and engineering configuration.

The values here are prototype assumptions, not calibrated Chennai measurements.
Keeping them in one place makes the model auditable and easy to tune.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache


@dataclass(frozen=True)
class QualityThresholds:
    recharge_turbidity_max_ntu: float = 5.0
    storage_turbidity_max_ntu: float = 25.0
    ph_min: float = 6.5
    ph_max: float = 8.5


@dataclass(frozen=True)
class DecisionThresholds:
    soil_saturation_recharge_block_percent: float = 85.0
    tank_nearly_full_percent: float = 80.0
    high_drain_stress_percent: float = 70.0


@dataclass(frozen=True)
class DecisionWeights:
    storage_capacity: float = 0.45
    storage_drain_stress: float = 0.35
    storage_headroom: float = 0.20
    recharge_capacity: float = 0.40
    recharge_soil: float = 0.25
    recharge_drain_stress: float = 0.20
    recharge_tank_pressure: float = 0.15
    discharge_capacity_pressure: float = 0.45
    discharge_soil: float = 0.35
    discharge_drain_stress: float = 0.20


@dataclass(frozen=True)
class Settings:
    app_name: str = "Chennai Water Bank"
    data_backend: str = "memory"
    demo_mode: bool = True
    gcp_project: str | None = None
    firestore_database: str = "(default)"
    firestore_max_attempts: int = 3
    firestore_initial_delay_ms: int = 200
    firestore_max_delay_ms: int = 2000
    firestore_timeout_seconds: int = 5
    moss_enabled: bool = False
    moss_project_id: str | None = None
    moss_project_key: str | None = field(default=None, repr=False)
    moss_index_name: str = "chennai-water-bank-events"
    moss_top_k: int = 4
    default_region: str = "asia-south1"
    simulation_interval_minutes: int = 15
    quality: QualityThresholds = field(default_factory=QualityThresholds)
    decision: DecisionThresholds = field(default_factory=DecisionThresholds)
    weights: DecisionWeights = field(default_factory=DecisionWeights)


def _as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _bounded_int(value: str | None, default: int, low: int, high: int) -> int:
    try:
        parsed = int(value) if value is not None else default
    except (TypeError, ValueError):
        parsed = default
    return max(low, min(high, parsed))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return environment-aware settings without requiring cloud credentials."""
    return Settings(
        data_backend=os.getenv("DATA_BACKEND", "memory").strip().lower(),
        demo_mode=_as_bool(os.getenv("DEMO_MODE"), True),
        gcp_project=os.getenv("GOOGLE_CLOUD_PROJECT") or None,
        firestore_database=os.getenv("FIRESTORE_DATABASE", "(default)"),
        firestore_max_attempts=_bounded_int(os.getenv("FIRESTORE_MAX_ATTEMPTS"), 3, 1, 5),
        firestore_initial_delay_ms=_bounded_int(os.getenv("FIRESTORE_INITIAL_DELAY_MS"), 200, 0, 5000),
        firestore_max_delay_ms=_bounded_int(os.getenv("FIRESTORE_MAX_DELAY_MS"), 2000, 0, 10000),
        firestore_timeout_seconds=_bounded_int(os.getenv("FIRESTORE_TIMEOUT_SECONDS"), 5, 1, 30),
        moss_enabled=_as_bool(os.getenv("MOSS_ENABLED"), False),
        moss_project_id=os.getenv("MOSS_PROJECT_ID") or None,
        moss_project_key=os.getenv("MOSS_PROJECT_KEY") or None,
        moss_index_name=(
            os.getenv("MOSS_INDEX_NAME", "chennai-water-bank-events").strip()
            or "chennai-water-bank-events"
        ),
        moss_top_k=_bounded_int(os.getenv("MOSS_TOP_K"), 4, 1, 10),
    )


# Uncalibrated screening assumptions for Problem 2.3, separate from routing weights.
PRIORITY_WEIGHTS = {
    key: 0.125
    for key in (
        "elevation_m",
        "slope_deg",
        "drainage_density_km_km2",
        "rainfall_mm",
        "ndvi",
        "land_use",
        "soil",
        "surface_water_pct",
    )
}
# (normalization minimum, maximum, reverse direction). Bounds are demo anchors.
PRIORITY_RANGES = {
    "elevation_m": (0.0, 100.0, True),
    "slope_deg": (0.0, 15.0, False),
    "drainage_density_km_km2": (0.0, 5.0, False),
    "rainfall_mm": (0.0, 2500.0, False),
    "ndvi": (-1.0, 1.0, True),
    "surface_water_pct": (0.0, 100.0, True),
}
PRIORITY_LAND_USE = {
    "Tree cover": 0.2,
    "Shrubland": 0.3,
    "Grassland": 0.4,
    "Cropland": 0.6,
    "Built-up": 1.0,
    "Bare / sparse vegetation": 0.8,
    "Snow / ice": 0.0,
    "Permanent water": 0.0,
    "Herbaceous wetland": 0.0,
    "Mangroves": 0.0,
    "Moss / lichen": 0.3,
}
# Hydrologic soil groups: higher runoff potential => more retention assessment need.
PRIORITY_SOIL = {"A": 0.25, "B": 0.5, "C": 0.75, "D": 1.0}
PRIORITY_CLASSES = (
    (0.8, "VERY HIGH"),
    (0.6, "HIGH"),
    (0.4, "MODERATE"),
    (0.2, "LOW"),
    (0.0, "VERY LOW"),
)
PRIORITY_MIN_COVERAGE = 0.5
