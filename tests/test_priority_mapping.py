"""Scientific boundaries and deterministic priority-model regression tests."""

import csv
import hashlib
import io
import json
import math
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from src.config.settings import PRIORITY_WEIGHTS
from src.geospatial.data import DATA_DIR, apply_csv, csv_template, load_sample
from src.geospatial.priority import (
    classify,
    indicators,
    normalize,
    recommendation,
    score_zone,
    score_zones,
    validate_weights,
)


def test_normalization_clips_and_reverses():
    assert normalize(-20, 0, 100) == 0
    assert normalize(120, 0, 100) == 1
    assert normalize(25, 0, 100, True) == 0.75
    assert normalize(None, 0, 1) is None
    assert normalize(float("nan"), 0, 1) is None
    assert normalize(float("inf"), 0, 1) is None
    with pytest.raises(ValueError):
        normalize(1, 1, 1)
    with pytest.raises(ValueError):
        normalize("garbage", 0, 1)


@pytest.mark.parametrize(
    "value,expected",
    [
        (0, "VERY LOW"),
        (0.199, "VERY LOW"),
        (0.2, "LOW"),
        (0.4, "MODERATE"),
        (0.6, "HIGH"),
        (0.8, "VERY HIGH"),
        (1, "VERY HIGH"),
        (None, "INSUFFICIENT DATA"),
    ],
)
def test_classification(value, expected):
    assert classify(value) == expected


@pytest.mark.parametrize("value", [-0.1, 1.1, float("nan"), float("inf")])
def test_invalid_score(value):
    with pytest.raises(ValueError):
        classify(value)


def test_weight_validation():
    assert sum(validate_weights(PRIORITY_WEIGHTS).values()) == 1
    for invalid in [
        {},
        {**PRIORITY_WEIGHTS, "ndvi": -0.1},
        {**PRIORITY_WEIGHTS, "ndvi": float("nan")},
        {**PRIORITY_WEIGHTS, "ndvi": 0.3},
        {**PRIORITY_WEIGHTS, "ndvi": "x"},
    ]:
        with pytest.raises(ValueError):
            validate_weights(invalid)


def test_full_score_independent_hand_calculation():
    # All numeric factors at 0.5, soil B=0.5, land grassland=0.4.
    p = {
        "elevation_m": 50,
        "slope_deg": 7.5,
        "drainage_density_km_km2": 2.5,
        "rainfall_mm": 1250,
        "ndvi": 0,
        "land_use": "Grassland",
        "soil": "B",
        "surface_water_pct": 50,
    }
    result = score_zone(p, require_full=True)
    assert result["score"] == pytest.approx((7 * 0.5 + 0.4) / 8)
    assert result["coverage"] == 1
    assert not result["provisional"]
    assert sum(result["contributions"].values()) == pytest.approx(result["score"])


def test_missing_is_not_zero_and_complete_mode_refuses():
    features = load_sample()["features"]
    p = features[0]["properties"]
    r = score_zone(p)
    assert r["available_count"] == 6
    assert r["coverage"] == 0.75
    assert r["provisional"]
    assert "soil" not in r["effective_weights"]
    assert sum(r["effective_weights"].values()) == pytest.approx(1)
    assert score_zone(p, require_full=True)["score"] is None
    assert score_zone({})["score"] is None


def test_common_mask_prevents_incomparable_rankings():
    f = load_sample()["features"]
    f[0]["properties"]["ndvi"] = None
    results = score_zones(f)
    assert {r["coverage"] for r in results} == {0.625}
    assert all("ndvi" not in r["effective_weights"] for r in results)
    assert score_zones([]) == []


def test_categories_and_recommendations():
    with pytest.raises(ValueError):
        indicators({"soil": "unvalidated"})
    for label in [
        "VERY HIGH",
        "HIGH",
        "MODERATE",
        "LOW",
        "VERY LOW",
        "INSUFFICIENT DATA",
    ]:
        assert recommendation(label) == recommendation(label)
    assert "certified site testing" in recommendation("HIGH")
    assert "Collect missing" in recommendation("INSUFFICIENT DATA")
    assert "Protect" in recommendation("HIGH", "Permanent water")
    with pytest.raises(ValueError):
        recommendation("other")


def complete_csv():
    collection = load_sample()
    out = io.StringIO()
    writer = csv.DictWriter(
        out, fieldnames=["zone_id", *PRIORITY_WEIGHTS, "source", "period"]
    )
    writer.writeheader()
    for f in collection["features"]:
        p = f["properties"]
        writer.writerow(
            {
                **{k: p.get(k) for k in PRIORITY_WEIGHTS},
                "zone_id": p["zone_id"],
                "soil": "B",
                "drainage_density_km_km2": 1.2,
                "source": "TEST FIXTURE ONLY — synthetic additional inputs",
                "period": "test",
            }
        )
    return out.getvalue()


def test_import_preserves_geometry_and_requires_provenance():
    original = load_sample()
    updated = apply_csv(original, complete_csv())
    assert updated["features"][0]["geometry"] == original["features"][0]["geometry"]
    assert original["features"][0]["properties"]["soil"] is None
    assert (
        score_zone(updated["features"][0]["properties"], require_full=True)["score"]
        is not None
    )
    for text in [
        "wrong,header\n",
        csv_template(original),
        complete_csv().replace("C11", "wrong"),
        complete_csv().replace("C12", "C11"),
        complete_csv().replace("1.2", "nan"),
        complete_csv().replace("1.2", "-2"),
        "\n".join(complete_csv().splitlines()[:-1]),
    ]:
        with pytest.raises(ValueError):
            apply_csv(original, text)


def test_bundled_provenance_and_numeric_integrity():
    manifest = json.loads((DATA_DIR / "manifest.json").read_text())
    for name, record in manifest["files"].items():
        assert (
            hashlib.sha256((DATA_DIR / "source" / name).read_bytes()).hexdigest()
            == record["sha256"]
        )
        assert record["source_url"].startswith("https://")
    for f in load_sample()["features"]:
        p = f["properties"]
        assert p["soil"] is None and p["drainage_density_km_km2"] is None
        assert 0 <= p["surface_water_pct"] <= 100
        assert -1 <= p["ndvi"] <= 1
        assert math.isclose(p["rainfall_mm"], 1623.87)
        assert f["geometry"]["coordinates"][0][0] == f["geometry"]["coordinates"][0][-1]


def test_priority_page_and_engine_bridge(monkeypatch):
    monkeypatch.setenv("MOSS_ENABLED", "false")
    monkeypatch.setenv("DATA_BACKEND", "memory")
    root = Path(__file__).resolve().parents[1]
    app = AppTest.from_file(
        str(root / "pages/00_water_conservation_priority_map.py"), default_timeout=30
    ).run()
    assert not app.exception
    assert any("PROBLEM STATEMENT 2.3" in x.value for x in app.markdown)
    assert len(app.get("plotly_chart")) == 1
    next(
        b
        for b in app.button
        if b.label == "Evaluate Water Bank scenario for selected zone"
    ).click().run()
    assert not app.exception
    assert any("Stored (L)" == x.label for x in app.metric)
    next(t for t in app.toggle if t.label.startswith("Require complete")).set_value(
        True
    ).run()
    assert not app.exception
    assert any(x.value == "Unranked" for x in app.metric)
    app.number_input[0].set_value(0.5).run()
    assert any("sum to 1" in x.value for x in app.error)


def test_existing_full_event_metrics_preserved():
    from src.persistence.memory_repository import MemoryRepository
    from src.simulation.simulator import DigitalSensorSimulator
    from src.impact.calculator import aggregate_impacts, impact_from_decision

    steps = DigitalSensorSimulator().simulate_network(
        MemoryRepository.from_demo_data().list_nodes()
    )
    impact = aggregate_impacts(impact_from_decision(s.decision) for s in steps)
    assert [
        round(getattr(impact, k))
        for k in (
            "stormwater_received_l",
            "stored_l",
            "recharged_l",
            "immediate_downstream_l",
            "retained_l",
        )
    ] == [1036747, 279123, 9490, 748134, 288612]
    assert round(impact.retention_percentage, 1) == 27.8
