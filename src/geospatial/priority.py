"""Transparent screening, not a calibrated watershed or recharge suitability model."""

from __future__ import annotations

import math
from collections.abc import Mapping
from src.config.settings import (
    PRIORITY_CLASSES,
    PRIORITY_LAND_USE,
    PRIORITY_MIN_COVERAGE,
    PRIORITY_RANGES,
    PRIORITY_SOIL,
    PRIORITY_WEIGHTS,
)


def normalize(value, lower: float, upper: float, reverse: bool = False):
    """Clip to fixed demonstration anchors; missing/nonfinite is never zero."""
    if not math.isfinite(lower) or not math.isfinite(upper) or upper <= lower:
        raise ValueError("Normalization bounds must be finite and increasing")
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError("Indicator must be numeric or missing") from None
    if not math.isfinite(number):
        return None
    result = min(1.0, max(0.0, (number - lower) / (upper - lower)))
    return 1.0 - result if reverse else result


def validate_weights(weights: Mapping[str, float]) -> dict[str, float]:
    if set(weights) != set(PRIORITY_WEIGHTS):
        raise ValueError("Provide exactly the eight official indicator weights")
    try:
        result = {k: float(v) for k, v in weights.items()}
    except (TypeError, ValueError):
        raise ValueError("Weights must be numeric") from None
    if any(not math.isfinite(v) or v < 0 for v in result.values()):
        raise ValueError("Weights must be finite and nonnegative")
    if not math.isclose(sum(result.values()), 1.0, abs_tol=1e-8):
        raise ValueError("Weights must sum to 1")
    return result


def indicators(properties: Mapping) -> dict:
    result = {
        k: normalize(properties.get(k), *bounds)
        for k, bounds in PRIORITY_RANGES.items()
    }
    for key, choices in (("land_use", PRIORITY_LAND_USE), ("soil", PRIORITY_SOIL)):
        value = properties.get(key)
        if value is not None and value not in choices:
            raise ValueError(f"Unknown {key}: {value}")
        result[key] = choices.get(value)
    return result


def classify(score: float | None) -> str:
    if score is None:
        return "INSUFFICIENT DATA"
    if not math.isfinite(score) or not 0 <= score <= 1:
        raise ValueError("Score must be finite in [0, 1]")
    return next(label for threshold, label in PRIORITY_CLASSES if score >= threshold)


def score_zone(properties, weights=None, *, allowed=None, require_full=False):
    weights = validate_weights(PRIORITY_WEIGHTS if weights is None else weights)
    values = indicators(properties)
    active = {
        k: v
        for k, v in values.items()
        if v is not None and weights[k] > 0 and (allowed is None or k in allowed)
    }
    coverage = sum(weights[k] for k in active)
    complete = all(
        values[k] is not None and (allowed is None or k in allowed)
        for k in weights
        if weights[k] > 0
    )
    eligible = coverage >= PRIORITY_MIN_COVERAGE and (complete or not require_full)
    contributions = (
        {k: weights[k] * v / coverage for k, v in active.items()} if coverage else {}
    )
    score = sum(contributions.values()) if eligible else None
    return {
        "score": score,
        "priority": classify(score),
        "coverage": coverage,
        "available_count": len(active),
        "provisional": not complete,
        "contributions": contributions,
        "normalized": values,
        "effective_weights": {k: weights[k] / coverage for k in active}
        if coverage
        else {},
    }


def score_zones(features, weights=None, require_full=False):
    """Use the same indicator intersection in every zone so rankings are comparable."""
    common = set(PRIORITY_WEIGHTS)
    for feature in features:
        common &= {
            k for k, v in indicators(feature["properties"]).items() if v is not None
        }
    return [
        score_zone(f["properties"], weights, allowed=common, require_full=require_full)
        for f in features
    ]


def recommendation(priority: str, land_use=None) -> str:
    if land_use in {"Permanent water", "Herbaceous wetland", "Mangroves"}:
        return "Protect water/wetland habitat; no Water Bank placement inferred. Ecological and field review required."
    if priority == "INSUFFICIENT DATA":
        return "Collect missing spatial evidence before assigning intervention priority; field validation required."
    if priority in {"VERY HIGH", "HIGH"}:
        return "Prioritize distributed storage and retention assessment; investigate candidate Water Bank placement. Evaluate recharge only after certified site testing. Field validation required."
    if priority == "MODERATE":
        return "Monitor and assess targeted retention; recharge requires certified site testing and field validation."
    if priority in {"LOW", "VERY LOW"}:
        return "Maintain and monitor existing conditions; this screening does not rule out local conservation needs."
    raise ValueError("Unknown priority class")
