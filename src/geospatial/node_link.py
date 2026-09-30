"""Coordinate association for demonstration nodes; no inferred infrastructure."""


def _in_ring(longitude, latitude, ring):
    inside = False
    for a, b in zip(ring, ring[1:] + ring[:1]):
        ax, ay = a[:2]
        bx, by = b[:2]
        cross = (longitude - ax) * (by - ay) - (latitude - ay) * (bx - ax)
        if abs(cross) < 1e-12 and min(ax, bx) <= longitude <= max(ax, bx) and min(ay, by) <= latitude <= max(ay, by):
            return True
        if (ay > latitude) != (by > latitude):
            if longitude < (bx - ax) * (latitude - ay) / (by - ay) + ax:
                inside = not inside
    return inside


def nodes_in_zone(feature, nodes):
    """Include polygon boundaries; exclude holes. Unsupported geometry fails closed."""
    geometry = feature.get("geometry") or {}
    if geometry.get("type") != "Polygon":
        return []
    rings = geometry.get("coordinates") or []
    if not rings or len(rings[0]) < 3:
        return []
    return [
        node for node in nodes
        if _in_ring(node.longitude, node.latitude, rings[0])
        and not any(_in_ring(node.longitude, node.latitude, hole) for hole in rings[1:])
    ]
