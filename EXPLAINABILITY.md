# Chennai Water Conservation Priority Agent Explainability

## Decision and Reasoning Process

The agent's decision process validates each available indicator, normalizes it according to declared rules, applies configured weights, and combines the effective contributions into a transparent priority score. Its reasoning assigns a provisional class such as Very High, High, Moderate, Low, Very Low, or Unranked and explains the evidence and missing-data conditions behind that result.

The geospatial priority decision remains separate from the Water Bank engineering decision. When a synthetic Water Bank scenario is examined, deterministic safety gates, capacity constraints, nonnegative volumes, and mass balance govern storage, modelled recharge, and downstream allocation.

## Inputs and Data Sources Used

Input data can include DEM or elevation, derived slope, drainage density, rainfall, NDVI, land use or land cover, hydrologic soil group, and surface-water occurrence. Bundled data sources currently include Mapzen or Tilezen terrain, NASA POWER rainfall, Copernicus Sentinel-2-derived NDVI, ESA WorldCover land cover, and JRC or Google Global Surface Water evidence.

The model supports all eight challenge indicators, but the bundled workflow currently contains six source-derived indicators and awaits sourced soil-group and drainage-density layers. User-imported data must include every demonstration zone, all indicator columns, source declarations, and observation periods, while blank values remain explicitly missing.

## Outputs and Supporting Evidence

The agent outputs georeferenced provisional priority zones, scores, classes, indicator contributions, effective weights, evidence coverage, missing-input warnings, and planning recommendations. Supporting evidence remains connected to source provenance, acquisition or observation periods, processing descriptions, spatial bounds, and available SHA-256 hashes.

The separate engineering output may show deterministic STORE, RECHARGE, or DOWNSTREAM allocation with simulated runoff, locally stored volume, modelled recharge, immediate downstream flow, and mass balance. These simulation results are supporting scenario evidence and do not modify the geospatial priority score.

## Limits, Constraints, and Known Issues

A central limitation is that the twelve analysis zones are demonstration units rather than officially delineated micro-watersheds, and the present six-input rankings are provisional. Current constraints include missing bundled soil and drainage-density evidence, uncalibrated weights and thresholds, single-date NDVI, regional rainfall, incomplete field validation, and the absence of a calibrated hydraulic flood model.

The model does not certify recharge suitability, approve infrastructure, predict flood depth or damage, or represent live Chennai operations. The optional Moss advisory layer is disabled by default, the priority map makes no AI calls, and advisory output cannot command infrastructure.

## Uncertainty and Human Review

Uncertainty increases when evidence layers are missing, spatial resolution is coarse, observations represent only one period, user-supplied provenance is unverified, or indicator weights have not been professionally calibrated. Zones with insufficient evidence may remain Unranked, and missing values are never treated as zero or silently imputed.

Human review is required before interpreting a priority result as a planning decision or linking it to site action. Recharge proposals require certified site testing, hydrogeological assessment, environmental and regulatory review, engineering design, and field validation.

## Responsible Use and Safety Constraints

The agent distinguishes geospatial planning evidence from synthetic operational-event data and never converts annual rainfall directly into storm-event rainfall, storage sizing, recharge capacity, or live control signals. Demonstrated retained-runoff percentages describe simulated volume allocation and are not claims of equivalent flood reduction.

Habitat-sensitive zones must be reviewed for protection rather than assumed suitable for construction. The ESP32 proof of concept remains separate, offline, and non-deployed, with deterministic edge safety required before any future operational integration.
