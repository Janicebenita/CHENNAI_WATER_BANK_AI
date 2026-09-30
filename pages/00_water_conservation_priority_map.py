"""Problem 2.3: where to prioritize conservation before simulating node operations."""

import copy
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.config.settings import (
    PRIORITY_LAND_USE,
    PRIORITY_RANGES,
    PRIORITY_SOIL,
    PRIORITY_WEIGHTS,
)
from src.geospatial.data import DATA_DIR, apply_csv, csv_template, load_sample
from src.geospatial.priority import recommendation, score_zones, validate_weights
from src.simulation.scenarios import SCENARIOS
from src.ui.scenario_controls import run_scenario
from src.ui.priority_operations import render_priority_operations
from src.ui.components import decision_card, safety_notice
from src.ui.theme import configure_page, render_sidebar_context

configure_page("Water Conservation Priority Map", "🌍")
render_sidebar_context()
st.markdown(
    '<div class="eyebrow">GEOIMPATHON 1.0 · WATER RESOURCE MANAGEMENT · PROBLEM STATEMENT 2.3</div>',
    unsafe_allow_html=True,
)
st.title("Water Conservation Priority Map")
st.write("**Watershed-Based Water Resource Priority Mapping**")
st.caption(
    "Spatial evidence → priority zones → conservation recommendation → deterministic Water Bank scenario"
)
st.caption(
    "Demonstration Analysis Zones · not official watersheds · field validation required"
)

sample = load_sample()
collection = sample
weights = dict(PRIORITY_WEIGHTS)
with st.sidebar.expander("Priority model · weights & data", expanded=False):
    st.caption(
        "Equal demonstration weights avoid claiming evidence for expert/calibrated weights. They are not Chennai policy weights. Terrain and vegetation can be correlated; sensitivity and local calibration are still needed."
    )
    columns = st.columns(2)
    for i, key in enumerate(weights):
        weights[key] = columns[i % 2].number_input(
            key,
            min_value=0.0,
            max_value=1.0,
            value=0.125,
            step=0.025,
            format="%.3f",
            key="priority_weight_" + key,
        )
    st.write(f"Weight sum: **{sum(weights.values()):.3f}** (must equal 1)")
    st.latex(r"P_z = \frac{\sum_{i\in A}w_i n_{zi}}{\sum_{i\in A}w_i}")
    st.caption(
        "A is the same set of available, positively weighted indicators across every zone. Missing values are excluded, never replaced with zero. At least 50% of original weight is required. The full eight-input score uses denominator 1. Classes: ≥0.8 Very High; ≥0.6 High; ≥0.4 Moderate; ≥0.2 Low; otherwise Very Low."
    )
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Indicator": k,
                    "Min": v[0],
                    "Max": v[1],
                    "Higher priority when": "lower" if v[2] else "higher",
                }
                for k, v in PRIORITY_RANGES.items()
            ]
        ),
        hide_index=True,
    )
    st.caption(
        "Demo objective: retention assessment opportunity/need — lower elevation, higher slope/drainage/rainfall, lower vegetation/surface-water occurrence. These directions are not recharge suitability rules. Values clip to the displayed anchors."
    )
    st.json(
        {
            "land_cover_demo_scores": PRIORITY_LAND_USE,
            "soil_hydrologic_group_demo_scores": PRIORITY_SOIL,
        },
        expanded=False,
    )
    st.download_button(
        "Download indicator CSV template",
        csv_template(sample),
        "priority_indicator_template.csv",
        "text/csv",
    )
    uploaded = st.file_uploader(
        "Optional: eight-indicator CSV for these zones (source and period required)",
        type=["csv"],
    )
    if uploaded is not None:
        try:
            collection = apply_csv(sample, uploaded.getvalue().decode("utf-8-sig"))
            st.warning(
                "User-supplied indicators: provenance declarations are not independently verified. Bundled satellite evidence has not been modified."
            )
        except (ValueError, UnicodeDecodeError) as exc:
            st.error(str(exc))
            st.stop()
try:
    validate_weights(weights)
except ValueError as exc:
    st.error(str(exc))
    st.stop()
with st.sidebar:
    require_full = st.toggle(
        "Require complete data for every positively weighted indicator", value=False
    )
features = collection["features"]
if not features:
    st.warning("No analysis zones available.")
    st.stop()
results = score_zones(features, weights, require_full=require_full)
records = []
for feature, result in zip(features, results):
    p = feature["properties"]
    records.append(
        {
            "Zone": p["zone_id"],
            "Location": p["zone"],
            "Priority": result["priority"],
            "Priority Score": result["score"],
            "Rainfall (mm/year)": p.get("rainfall_mm"),
            "Slope (°)": p.get("slope_deg"),
            "Drainage Density (km/km²)": p.get("drainage_density_km_km2"),
            "NDVI": p.get("ndvi"),
            "Land Use": p.get("land_use"),
            "Soil": p.get("soil"),
            "Surface Water Occurrence (%)": p.get("surface_water_pct"),
            "Elevation (m)": p.get("elevation_m"),
            "Recommended Intervention": recommendation(
                result["priority"], p.get("land_use")
            ),
        }
    )
frame = pd.DataFrame(records)
valid = frame.dropna(subset=["Priority Score"])
top = (
    valid.sort_values(["Priority Score", "Zone"], ascending=[False, True]).iloc[0]
    if len(valid)
    else None
)
cols = st.columns(4)
cols[0].metric("Analysis zones", len(frame))
cols[1].metric(
    "Very High / High", int(frame["Priority"].isin(["VERY HIGH", "HIGH"]).sum())
)
cols[2].metric(
    "Mean priority score",
    f"{valid['Priority Score'].mean():.3f}" if len(valid) else "Unranked",
)
cols[3].metric(
    "Highest-priority zone", top["Zone"] if top is not None else "Insufficient data"
)
missing = [k for k in PRIORITY_WEIGHTS if k not in results[0]["effective_weights"]]
st.warning(
    f"Evidence coverage: {results[0]['available_count']}/8 active indicators; {results[0]['coverage']:.0%} of original weight. Excluded/missing: {', '.join(missing) or 'none'}. {'PROVISIONAL priorities.' if results[0]['provisional'] else 'Full enabled-indicator coverage; still uncalibrated.'}"
)
colors = {
    "VERY HIGH": "#d73027",
    "HIGH": "#f7943d",
    "MODERATE": "#e4ce58",
    "LOW": "#74bfa3",
    "VERY LOW": "#4597c5",
    "INSUFFICIENT DATA": "#86929a",
}
map_column, recommendation_column = st.columns([2.15, 1], gap="large")
with recommendation_column:
    st.subheader("Explore a zone")
    selected = st.selectbox(
        "Inspect a priority zone",
        list(frame["Zone"]),
        index=list(frame["Zone"]).index(top["Zone"]) if top is not None else 0,
    )
    index = list(frame["Zone"]).index(selected)
    p = features[index]["properties"]
    r = results[index]
    st.subheader(f"{selected} · {r['priority']}")
    st.metric(
        "Priority score", f"{r['score']:.3f}" if r["score"] is not None else "Unranked"
    )
    st.markdown("#### Recommended intervention")
    st.write(records[index]["Recommended Intervention"])
    st.caption(
        f"Zone centre: {p['latitude']:.4f}° N, {p['longitude']:.4f}° E. No physical Water Bank installation is implied."
    )
    with st.expander("Why this priority? · indicator contributions", expanded=False):
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Indicator": k,
                        "Normalized": r["normalized"][k],
                        "Original weight": weights[k],
                        "Effective weight": r["effective_weights"].get(k, 0),
                        "Contribution": r["contributions"].get(k),
                    }
                    for k in PRIORITY_WEIGHTS
                ]
            ),
            hide_index=True,
            width="stretch",
        )
        if uploaded is not None:
            st.write(
                {
                    "source": p["source"],
                    "period": p["period"],
                    "status": p["provenance_status"],
                }
            )
        else:
            st.caption(
                f"NDVI valid land sample fraction: {p['ndvi_valid_fraction']:.1%}. Cloud/shadow/water excluded; ≥20% required."
            )

with map_column:
    st.subheader("Priority zones · Chennai study-area context")
    basemap = st.toggle("Online OpenStreetMap context", value=True)
    fig = px.choropleth_map(
        frame,
        geojson=collection,
        locations="Zone",
        featureidkey="properties.zone_id",
        color="Priority",
        color_discrete_map=colors,
        category_orders={"Priority": list(colors)},
        hover_name="Location",
        hover_data={
            "Zone": True,
            "Priority Score": ":.3f",
            "Slope (°)": ":.2f",
            "NDVI": ":.3f",
            "Surface Water Occurrence (%)": ":.2f",
        },
        center={"lat": 13.02, "lon": 80.21},
        zoom=10,
        map_style="open-street-map" if basemap else "white-bg",
        opacity=0.72,
    )
    fig.add_trace(
        go.Scattermap(
            lat=[13.0827],
            lon=[80.2707],
            mode="markers+text",
            text=["Chennai context"],
            textposition="top center",
            marker={"size": 10, "color": "#234e70"},
            name="City reference",
            hovertemplate="Chennai reference point; not an installed node<extra></extra>",
        )
    )
    fig.update_layout(
        height=540,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        legend={"orientation": "h", "y": -0.08},
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#bdd0cd", "size": 16},
        hoverlabel={"font_size": 16},
        uirevision="priority-map",
    )
    ring = features[index]["geometry"]["coordinates"][0]
    fig.add_trace(
        go.Scattermap(
            lon=[point[0] for point in ring],
            lat=[point[1] for point in ring],
            mode="lines",
            line={"width": 4, "color": "#163c67"},
            showlegend=False,
            hoverinfo="skip",
        )
    )
    st.plotly_chart(
        fig, width="stretch", config={"displayModeBar": False, "scrollZoom": True}
    )
    st.caption(
        "Pan, zoom and hover to inspect. Colours are screening classes, not flood hazard or construction approval. Turn context off for an offline polygon map. OpenStreetMap © contributors. Rectangles are explicitly demonstration analysis zones."
    )
cols = st.columns(3)
for col, label, key, fmt in zip(
    cols,
    [
        "Rainfall indicator (mm/year)",
        "Vegetation indicator (NDVI)",
        "Surface-water occurrence (%)",
    ],
    ["Rainfall (mm/year)", "NDVI", "Surface Water Occurrence (%)"],
    [".1f", ".3f", ".2f"],
):
    mean = frame[key].mean()
    col.metric(label, format(mean, fmt) if pd.notna(mean) else "Missing")
st.caption(
    "Bundled sample: POWER 2024 regional rainfall (same value in every zone; not a gauge observation); Sentinel-2 land NDVI 29 Feb 2024; JRC 1984–2021 mean water occurrence, not percentage water area. Imported rows use their declared source/period instead."
)

st.subheader("Sortable zone evidence")
st.dataframe(frame, hide_index=True, width="stretch")
st.download_button(
    "Download priority table",
    frame.to_csv(index=False),
    "conservation_priorities.csv",
    "text/csv",
)
export = copy.deepcopy(collection)
for feature, result in zip(export["features"], results):
    feature["properties"].update(result)
export["analysis_metadata"] = {
    "weights": weights,
    "zone_type": "Demonstration Analysis Zones, NOT watersheds",
    "calibration": "DEMONSTRATION WEIGHTS; not validated policy",
    "source": "Bundled manifest.json"
    if uploaded is None
    else "User-declared, not independently verified",
}
st.download_button(
    "Download scored GeoJSON",
    json.dumps(export, allow_nan=False),
    "conservation_priorities.geojson",
    "application/geo+json",
)

render_priority_operations(features[index])

st.subheader("Separate hypothetical Water Bank scenario")
st.caption(
    "Zone selection supplies planning context only. Annual rainfall, priority and NDVI are NOT converted into event rainfall, tank capacity or recharge rates. The following scenario is explicitly synthetic and does not alter Network Simulation or its Impact Analytics."
)
scenario_key = st.selectbox(
    "Synthetic Water Bank operating scenario",
    list(SCENARIOS),
    format_func=lambda k: SCENARIOS[k].name,
)
if st.button("Evaluate Water Bank scenario for selected zone", type="primary"):
    _, _, runoff, decision = run_scenario(SCENARIOS[scenario_key])
    st.write(f"Planning context: **{selected}** · SIMULATED WATER BANK DATA")
    decision_card(decision)
    allocation = decision.allocation
    cols = st.columns(4)
    for col, label, value in zip(
        cols,
        ["Runoff (L)", "Stored (L)", "Modelled recharge (L)", "Downstream (L)"],
        [runoff, allocation.stored_l, allocation.recharged_l, allocation.downstream_l],
    ):
        col.metric(label, f"{value:,.0f}")
    st.caption(
        "Volume-allocation estimate, not a hydraulic flood-depth or damage model."
    )
safety_notice()
st.markdown("[Open Scenario Lab → edit synthetic engineering inputs](./scenario_lab)")
st.markdown("[Open existing network Impact Analytics](./impact_analytics)")
with st.expander("Provenance · processing · validation limits"):
    st.markdown(
        "**REAL / REMOTE-SENSING INPUTS:** terrain tiles, Sentinel-2, ESA WorldCover, JRC water occurrence. **REANALYSIS:** NASA POWER rainfall. **DERIVED:** sampled zone indicators and priority index. **SIMULATED:** separate Water Bank event allocation."
    )
    st.write(
        "Drainage density and hydrologic soil group are not bundled. Supply validated measurements/derived values through the CSV interface. Complete-data mode refuses to rank without them. Official DEM watershed delineation, drainage conditioning, local rainfall, seasonal NDVI, soil validation and calibration are next validation steps."
    )
    st.write(
        "The JRC v1.4 1984–2021 occurrence layer is a reproducible legacy sample; its provider reports inconsistencies corrected in v1.5. Upgrade and validate before decisions. Dates/resolutions differ across inputs. Coarse terrain and a single NDVI date cannot establish parcel-scale suitability."
    )
    st.caption(
        "© ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium. Sentinel-2: Copernicus / ESA via Element 84. Terrain: Mapzen / Tilezen and contributing sources. Rainfall: NASA POWER. Source: EC JRC/Google; Pekel et al., Nature 540 (2016), doi:10.1038/nature20584."
    )
    st.json(json.loads((DATA_DIR / "manifest.json").read_text()), expanded=False)
st.caption(
    "AI assists. Engineering governs. Humans review. ESP32: separate physical proof of concept, currently offline and not required for this demonstration."
)
