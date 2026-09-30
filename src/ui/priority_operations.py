"""Read-only connection to the Command Centre's active simulation snapshot."""

import streamlit as st

from src.geospatial.node_link import nodes_in_zone
from src.ui.components import decision_card, latest_steps
from src.ui.runtime import get_active_steps, load_nodes


def render_priority_operations(feature):
    zone_id = feature["properties"]["zone_id"]
    st.subheader("Connected Command Centre · human review")
    st.caption(
        "SIMULATED DATA · Demonstration nodes are associated by their configured coordinates "
        "inside this demonstration analysis zone. These are not installed infrastructure. "
        "Decisions use the same active storm snapshot as the Command Centre, not the priority score."
    )
    nodes = nodes_in_zone(feature, load_nodes())
    if not nodes:
        st.info(
            f"{zone_id}: no configured demonstration node within this zone. "
            "No connected operational recommendation is available. "
            "Use the separate hypothetical scenario below for exploration."
        )
        return
    latest = latest_steps(get_active_steps())
    st.write(f"**{zone_id} · {len(nodes)} associated demonstration node(s)**")
    st.caption(
        "Updates when this page is opened or refreshed after a Command Centre simulation "
        "in the same session. This is a simulation snapshot, not live telemetry."
    )
    st.button("Refresh Command Centre snapshot", key="priority_refresh")
    for node in nodes:
        st.markdown(f"#### {node.name} · {node.node_id}")
        step = latest.get(node.node_id)
        if step is None:
            st.warning("No active operating snapshot for this node. No recommendation available.")
            continue
        state = step.sensor_state
        st.caption(
            f"Simulated pulse {step.step_index + 1} · generated {state.timestamp.isoformat()} · "
            f"configured location {node.latitude:.4f}, {node.longitude:.4f}"
        )
        decision_card(step.decision)
        allocation = step.decision.allocation
        cols = st.columns(4)
        for col, label, value in zip(
            cols,
            ["Runoff this pulse (L)", "Stored (L)", "Modelled recharge (L)", "Downstream (L)"],
            [allocation.incoming_l, allocation.stored_l, allocation.recharged_l, allocation.downstream_l],
        ):
            col.metric(label, f"{value:,.0f}")
        with st.expander(f"Operating inputs and explanation · {node.node_id}"):
            st.write({
                "Rainfall intensity (mm/hr)": state.rainfall_intensity_mm_hr,
                "Rainfall depth this pulse (mm)": step.rainfall_depth_mm,
                "Catchment area (m²)": node.catchment_area_m2,
                "Runoff coefficient": node.runoff_coefficient,
                "Tank capacity (L)": node.storage_capacity_l,
                "Storage before decision (L)": step.storage_before_l,
                "Storage after allocation (L)": step.storage_after_l,
                "Configured recharge capacity (L/hr)": node.recharge_capacity_l_per_hour,
                "Recharge available": node.recharge_available,
                "Simulated soil saturation (%)": state.soil_saturation_percent,
                "Drain stress (%)": state.drain_stress_percent,
                "Turbidity (NTU)": state.turbidity_ntu,
                "pH": state.ph,
                "Contamination detected": state.contamination_detected,
                "First flush active": state.first_flush_active,
            })
            for action, reason in step.decision.rejected_alternatives.items():
                st.write(f"**Why not {action.replace('_', ' ')}:** {reason}")
            for constraint in step.decision.constraints:
                st.caption(constraint)
            st.caption(f"Mass-balance residual: {allocation.mass_balance_error_l:.8f} L")
        st.info("Awaiting human review. This recommendation sends no infrastructure commands.")
    if st.button("Open Command Centre — simulate or reset the shared storm"):
        st.switch_page("pages/01_command_center.py")
