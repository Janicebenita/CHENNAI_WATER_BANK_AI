# Chennai Water Conservation Priority Agent

## Purpose

The agent helps planners investigate where water-conservation attention may be needed by combining provenance-aware geospatial evidence with a transparent multi-criteria priority model. It also connects planning context to a separate deterministic Water Bank simulation without converting map scores into infrastructure commands.

## Geospatial Investigation Approach

The agent evaluates supported indicators for elevation, slope, drainage density, rainfall, vegetation, land cover, soil group, and surface-water occurrence. It normalizes available evidence, applies configurable weights and explicit missing-data rules, calculates indicator contributions, and classifies demonstration analysis zones using declared thresholds.

## Evidence Integrity

The agent preserves source declarations, observation periods, processing notes, spatial boundaries, and available file hashes. Missing soil-group or drainage-density evidence remains missing rather than being estimated, silently zero-filled, or presented as complete coverage.

## Engineering Boundary

The geospatial model answers where conservation investigation may be prioritized, while the deterministic Water Bank layer evaluates what a configured node could do during a synthetic event. Priority scores do not automatically determine tank capacity, recharge capacity, event rainfall, routing decisions, or physical control signals.

## Explainability and Recommendations

The agent exposes each zone's score, class, effective weights, indicator contributions, evidence coverage, missing inputs, and planning recommendation. Water, wetland, and mangrove contexts receive habitat-protection guidance rather than automatic installation guidance.

## Human Governance and Uncertainty

The agent labels current rankings as provisional because only six of the eight supported indicators are bundled and the twelve zones are demonstration units rather than official micro-watersheds. Field action requires professional hydrologic, hydrogeological, environmental, regulatory, and engineering validation.
