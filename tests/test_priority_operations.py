"""Shared snapshot connection, geographic association and no-allocation side effects."""
from copy import deepcopy
from dataclasses import replace

from streamlit.testing.v1 import AppTest

from src.geospatial.data import load_sample
from src.geospatial.node_link import nodes_in_zone
from src.persistence.memory_repository import MemoryRepository
from src.simulation.simulator import DigitalSensorSimulator


def test_association_uses_coordinates_not_priority():
    nodes = MemoryRepository.from_demo_data().list_nodes()
    features = load_sample()["features"]
    mapping = {f["properties"]["zone_id"]: nodes_in_zone(f, nodes) for f in features}
    assert {k for k, v in mapping.items() if v} == {"C22", "C23", "C33", "C41"}
    assert sum(map(len, mapping.values())) == len(nodes) == 6
    changed = deepcopy(features)
    for feature in changed:
        feature["properties"]["priority_score"] = 1.0
    assert [nodes_in_zone(f, nodes) for f in changed] == list(mapping.values())


def test_polygon_boundary_hole_and_unsupported():
    node = MemoryRepository.from_demo_data().list_nodes()[0]
    feature = {"geometry": {"type": "Polygon", "coordinates": [
        [[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]],
        [[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5], [0.5, 0.5]],
    ]}}
    boundary = replace(node, longitude=0, latitude=1)
    hole = replace(node, longitude=1, latitude=1)
    outside = replace(node, longitude=3, latitude=3)
    assert nodes_in_zone(feature, [boundary, hole, outside]) == [boundary]
    assert nodes_in_zone({"geometry": {"type": "Point"}}, [node]) == []
    assert nodes_in_zone({"geometry": {"type": "Polygon", "coordinates": []}}, [node]) == []


def _page(zone):
    return AppTest.from_string(f"""
from src.geospatial.data import load_sample
from src.ui.priority_operations import render_priority_operations
feature = next(f for f in load_sample()['features'] if f['properties']['zone_id'] == '{zone}')
render_priority_operations(feature)
""")


def test_connected_view_uses_active_decisions_without_mutating_allocation():
    nodes = MemoryRepository.from_demo_data().list_nodes()
    steps = DigitalSensorSimulator().simulate_network(nodes)
    before = deepcopy(steps)
    app = _page("C33")
    app.session_state["storm_steps"] = steps
    app.run()
    assert not app.exception
    assert len(app.metric) == 12
    latest = {s.node_id: s for s in steps}
    feature = next(f for f in load_sample()["features"] if f["properties"]["zone_id"] == "C33")
    for i, node in enumerate(nodes_in_zone(feature, nodes)):
        allocation = latest[node.node_id].decision.allocation
        assert app.metric[i * 4].value == f"{allocation.incoming_l:,.0f}"
        assert app.metric[i * 4 + 2].value == f"{allocation.recharged_l:,.0f}"
    assert app.session_state["storm_steps"] == before
    baseline = DigitalSensorSimulator().simulate_network(nodes, steps=4)
    app.session_state["storm_steps"] = baseline
    app.button[0].click().run()
    assert not app.exception
    assert app.metric[0].value != f"{latest['WB-VEL-01'].decision.allocation.incoming_l:,.0f}"
    app.session_state["storm_steps"] = []
    app.run()
    assert len(app.warning) == 3
    assert len(app.metric) == 0


def test_unmapped_zone_has_no_operational_decision():
    app = _page("C13").run()
    assert not app.exception
    assert "no configured demonstration node" in app.info[0].value
    assert len(app.metric) == 0
