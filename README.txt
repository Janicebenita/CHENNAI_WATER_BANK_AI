<!-- Chennai Water Bank AI | GeoImpathon 1.0 | Problem Statement 2.3 -->

<p align="center">
  <img src="Docs/chennai-water-bank-banner.png" width="100%" alt="Chennai Water Bank AI — conceptual geospatial water-conservation project banner" />
</p>

<p align="center"><sub>Concept artwork · not satellite imagery or evidence of deployed infrastructure.</sub></p>

<h1 align="center">🌊 CHENNAI WATER BANK AI</h1>

<h3 align="center">
From Geospatial Evidence to Actionable Water-Conservation Intelligence
</h3>

<p align="center">
  <strong>GEOIMPATHON 1.0 — Geospatial Ideas for Greener Earth</strong><br />
  Water Resource Management · Problem Statement 2.3<br />
  <strong>Watershed-Based Water Resource Priority Mapping</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/GEOSPATIAL-PRIORITY_MAPPING-087F8C?style=for-the-badge" alt="Geospatial priority mapping" />
  <img src="https://img.shields.io/badge/PROBLEM_2.3-8_INPUTS_SUPPORTED-2563EB?style=for-the-badge" alt="Eight problem inputs supported" />
  <img src="https://img.shields.io/badge/EVIDENCE-6_OF_8_BUNDLED-D97706?style=for-the-badge" alt="Six of eight bundled indicators" />
  <img src="https://img.shields.io/badge/ENGINEERING-DETERMINISTIC-2563EB?style=for-the-badge" alt="Deterministic engineering" />
  <img src="https://img.shields.io/badge/AI-ADVISORY-7C3AED?style=for-the-badge" alt="Advisory AI" />
  <img src="https://img.shields.io/badge/STATUS-PROVISIONAL_PROTOTYPE-D97706?style=for-the-badge" alt="Provisional prototype" />
</p>

<p align="center">
  <a href="https://github.com/Janicebenita/CHENNAI_WATER_BANK_AI/actions/workflows/ci.yml"><img src="https://github.com/Janicebenita/CHENNAI_WATER_BANK_AI/actions/workflows/ci.yml/badge.svg" alt="Continuous integration" /></a>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/Streamlit-Interactive_Dashboard-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit dashboard" />
  <img src="https://img.shields.io/badge/Tests-103_passed-15803D" alt="103 tests passed at verified revision" />
  <img src="https://img.shields.io/badge/Coverage-95.30%25-15803D" alt="95.30 percent verified test coverage" />
</p>

<p align="center">
  <a href="#-see-it-in-action"><strong>▶ See It in Action</strong></a> ·
  <a href="#-water-conservation-priority-map"><strong>🗺 Explore Priority Mapping</strong></a> ·
  <a href="#-problem-23-coverage"><strong>🎯 Problem 2.3 Coverage</strong></a> ·
  <a href="#-run-locally"><strong>🚀 Run Locally</strong></a>
</p>

> ## Where should water-conservation intervention be investigated — and what could a distributed Water Bank do there?
>
> **Chennai Water Bank AI** combines source-derived geospatial indicators, a transparent multi-criteria priority model, explainable conservation recommendations, and deterministic rainwater-allocation simulation.
>
> It connects two complementary questions:
>
> **WHERE should conservation intervention be investigated?**  
> **WHAT could a configured Water Bank node do during a simulated rainfall event?**

> [!IMPORTANT]
> **Current evidence:** 12 demonstration analysis zones · 6 bundled source-derived indicators · 8 supported model inputs.  
> **Drainage density and soil are not bundled and are not fabricated.**  
> Boundaries are demonstration rectangles, not official micro-watersheds.  
> Current priority classifications are **provisional**.
>
> **Deployment:** the existing staging service may predate the Problem 2.3 adaptation. The new priority page is available in this repository and local runs; its Cloud Run deployment has not yet been verified.

---

# ⚡ Chennai Water Bank AI in 30 Seconds

| 01 — OBSERVE | 02 — PRIORITIZE | 03 — EXPLAIN | 04 — ACT |
|---|---|---|---|
| Combine geospatial evidence | Calculate a transparent priority score | Show why a zone received its score | Connect planning context to a separate Water Bank scenario |
| DEM, slope, rainfall, NDVI, land cover, surface water + supported soil/drainage inputs | Multi-criteria priority model | Indicator contributions + evidence coverage | STORE → RECHARGE → DOWNSTREAM |

> **The central idea:** move from **“Where does conservation deserve investigation?”** to **“What conservation action could be evaluated there?”**

---

# 🎬 See It in Action

## Priority Map Demo

> 🎥 **Demo media pending:** replace this placeholder with a recording of the actual Water Conservation Priority Map after final UI verification.

Recommended asset path:

```text
Docs/priority-map-demo.gif
```

When available:

```html
<p align="center">
  <img src="Docs/priority-map-demo.gif"
       width="95%"
       alt="Chennai Water Bank AI interactive Water Conservation Priority Map" />
</p>
```

## Selected Zone

> 🖼️ **Screenshot pending:** use a real screenshot showing a selected demonstration analysis zone with its actual priority score, evidence and recommendation.

Recommended asset path:

```text
Docs/priority-zone-selected.png
```

## Impact Analytics

> 🖼️ **Use only authentic UI media** from the demonstrated simulation.

Recommended asset path:

```text
Docs/impact-analytics.png
```

---

# 🧭 One System, Two Water-Conservation Questions

| 🌍 GEOSPATIAL PLANNING | 💧 WATER BANK ENGINEERING |
|---|---|
| **WHERE** should conservation intervention be investigated? | **WHAT** could a configured Water Bank node do during a simulated rainfall event? |
| Source-derived spatial evidence | Synthetic operational inputs |
| Transparent priority index | Deterministic allocation |
| Candidate analysis zones | STORE / RECHARGE / DOWNSTREAM |
| Planning decision support | Scenario evaluation |

> **These analyses are deliberately separated.** Spatial priority does not automatically become rainfall input, tank capacity, recharge capacity, or a live infrastructure command.

---

# 🎯 Problem 2.3 Coverage

The challenge calls for water-conservation priority zones based on eight geospatial parameters. Chennai Water Bank AI supports all eight model inputs while explicitly distinguishing between bundled source-derived evidence and currently missing evidence.

| Required indicator | Model support | Bundled evidence | Current status |
|---|---:|---:|---|
| 🏔 DEM / Elevation | ✅ | ✅ | Source-derived |
| 📐 Slope | ✅ | ✅ | Derived from DEM |
| 🌊 Drainage Density | ✅ | ❌ | Requires sourced import |
| 🌧 Rainfall | ✅ | ✅ | NASA POWER 2024 regional value |
| 🌿 NDVI | ✅ | ✅ | Sentinel-2 derived |
| 🏙 Land Use / Cover | ✅ | ✅ | ESA WorldCover |
| 🪨 Soil | ✅ | ❌ | Requires sourced hydrologic soil group import |
| 💦 Surface-Water Occurrence | ✅ | ✅ | JRC / Google GSW |

```text
MODEL INPUT SUPPORT          8 / 8
BUNDLED SOURCED INDICATORS   6 / 8
MISSING BUNDLED EVIDENCE     Soil · Drainage Density
CURRENT PRIORITY STATUS      PROVISIONAL
```

> **Important:** 8/8 model support does **not** mean 8/8 bundled data completeness.

---

# 🛰️ From Earth Observation to Conservation Priority

```mermaid
flowchart LR
    A["🛰️ Geospatial Sources"] --> B["📊 Indicator Processing"]
    B --> C["⚖️ Transparent Priority Index"]
    C --> D["🗺️ Priority Zones"]
    D --> E["🔍 Explain Score"]
    E --> F["📍 Conservation Recommendation"]

    F -. "separate scenario" .-> G["💧 Water Bank"]
    G --> H["STORE"]
    G --> I["RECHARGE"]
    G --> J["DOWNSTREAM"]
```

**Geospatial evidence → Priority Index → Priority Zone → Explanation → Recommendation**

Separately:

**Synthetic event → Deterministic Water Bank → Volume allocation**

The Priority Index does not directly calculate storage or recharge volumes.

---

# 🗺️ Water Conservation Priority Map

| 🗺 EXPLORE | 🔎 UNDERSTAND | 📤 EXPORT |
|---|---|---|
| Pan and zoom across analysis zones | Inspect score and contributing indicators | Download scored CSV |
| Hover over polygons | Review effective weights | Download scored GeoJSON |
| View priority classes | Inspect evidence completeness | Continue analysis externally |

## Priority Classes

```text
VERY HIGH    ≥ 0.80
HIGH         ≥ 0.60
MODERATE     ≥ 0.40
LOW          ≥ 0.20
VERY LOW     < 0.20
UNRANKED     insufficient evidence
```

> Thresholds are demonstration thresholds, not government-defined Chennai policy thresholds.

---

<details>
<summary><strong>⚖️ How is the Water Conservation Priority Index calculated?</strong></summary>

All eight starting weights are **0.125**, summing to 1. These are **demonstration weights**, not government or scientifically calibrated Chennai policy weights.

\[
P_z =
\frac{\sum_{i \in A} w_i n_{z,i}}
{\sum_{i \in A} w_i}
\]

Where:

- \(P_z\) is the priority score for zone \(z\)
- \(w_i\) is the configured indicator weight
- \(n_{z,i}\) is the normalized value for indicator \(i\)
- \(A\) is the same available, positively weighted indicator set across all zones

### Missing-data behaviour

- Missing values are never zero-filled.
- At least 50% of original weight must be available.
- Bundled data currently supplies 75% of total original weight.
- Full-data mode requires every positively weighted indicator.
- All eight indicators must have positive weights for complete-data mode to require all eight.

### Numerical normalization

Clipped:

```text
(x - min) / (max - min)
```

and reversed where specified.

### Demonstration anchors

- Elevation: 0–100 m, lower → higher priority
- Slope: 0–15°
- Drainage density: 0–5 km/km²
- Annual rainfall: 0–2,500 mm
- NDVI: −1 to 1, lower → higher priority
- Surface-water occurrence: 0–100%, lower → higher priority

Higher slope, drainage density and rainfall represent retention assessment need/opportunity in this demonstration model. They do **not** establish recharge suitability.

Land-cover and soil-group scoring tables are exposed in the UI and centralized with other geospatial assumptions in:

```text
src/config/settings.py
```

### Priority classes

- Very High ≥ 0.8
- High ≥ 0.6
- Moderate ≥ 0.4
- Low ≥ 0.2
- Very Low < 0.2

Insufficient evidence remains unranked.

These are fixed demonstration thresholds, not quantiles engineered to force high-priority zones.

Correlated indicators, mixed dates and scoring direction require sensitivity analysis and professional review.

</details>

---

# 🔍 From a Coloured Polygon to an Explainable Decision

```mermaid
flowchart LR
    A["Select Zone"] --> B["Priority Score"]
    B --> C["Indicator Contributions"]
    C --> D["Evidence Coverage"]
    D --> E["Recommendation"]
    E --> F["Field Review"]
```

A priority colour alone is not a decision.

Selecting a zone exposes the evidence contributing to its classification and converts that evidence into a transparent planning recommendation.

### Recommendation logic

**High priority**  
Investigate distributed storage, retention capacity and candidate Water Bank placement.

**Moderate priority**  
Targeted assessment and monitoring.

**Low priority**  
Monitoring; this is not a claim that conservation is unnecessary.

**Water / wetland / mangrove classes**  
Habitat-protection guidance rather than infrastructure installation guidance.

> [!WARNING]
> **Recharge requires certified site testing and professional hydrogeological assessment. Field validation is required.**

---

# 💧 From Priority Mapping to Distributed Water Intelligence

<h2 align="center">STORE → RECHARGE → DOWNSTREAM</h2>

The Water Bank simulation is a separate deterministic engineering layer.

```mermaid
flowchart LR
    R["🌧️ Simulated Runoff"] --> S{"Safety + Capacity Logic"}

    S --> A["🏦 STORE"]
    S --> B["🌱 MODELLED RECHARGE"]
    S --> C["🌊 DOWNSTREAM FLOW"]

    A --> D["📊 Mass-Balanced Accounting"]
    B --> D
    C --> D
```

### Engineering safeguards

- Unsafe and first-flush water cannot directly recharge.
- Allocation remains capacity-constrained.
- Volumes remain nonnegative.
- Allocation remains mass-balanced.
- The original six demonstration nodes remain simulated.

Original simulated demonstration locations:

- Adyar
- Anna Nagar
- Perungudi
- T. Nagar
- Tambaram
- Velachery

These are separate from the 12 geospatial analysis zones and do not represent deployed municipal assets.

---

# 📊 Demonstrated Simulation Impact

| Metric | Simulated event value |
|---|---:|
| Calculated runoff | **1,036,747 L** |
| Stored locally | **279,123 L** |
| Routed toward modelled recharge | **9,490 L** |
| Immediate downstream flow | **748,134 L** |
| **Retained from immediate downstream flow** | **288,612 L** |
| **Simulated event runoff retained** | **≈ 27.8%** |

> ## 💧 288,612 L retained
>
> **Approximately 27.8% of this demonstrated simulated event runoff is retained from immediate downstream flow.**

> [!CAUTION]
> **Simulation result — NOT a claim of 27.8% flood reduction.**

These values are:

- simulated volume-allocation estimates;
- not municipal observations;
- not measured groundwater recharge;
- not hydraulic flood-depth predictions;
- not flood-damage reduction estimates.

Independently rounded displayed totals can differ by one litre.

The priority map does not establish these volumes as outcomes in its analysis zones.

---

# 📡 Evidence, Not Black Boxes

| Evidence | Source |
|---|---|
| Terrain / DEM | Mapzen / Tilezen |
| Rainfall | NASA POWER |
| NDVI | Copernicus Sentinel-2 |
| Land cover | ESA WorldCover |
| Surface-water occurrence | JRC / Google GSW |

> Every bundled source subset is accompanied by provenance information. The source manifest records URLs, dates, bounding box, processing information and SHA-256 hashes.

<details>
<summary><strong>📚 View full data-source provenance and processing notes</strong></summary>

| Official parameter | Bundled evidence | Processing / limitation |
|---|---|---|
| DEM / elevation | Mapzen/Tilezen terrain tiles, zoom 12 | Terrarium RGB decoding; mean elevation. Source mosaic, not a certified local survey. |
| Slope | Derived from the same DEM | Gradient in metres, converted to degrees; approximately 37 m terrain pixels. Correlated with terrain. |
| Drainage density | **Missing** | Accept sourced km/km² through CSV. Hydrologically conditioned drainage extraction is a next step. |
| Rainfall | NASA POWER PRECTOTCORR, 2024 | Sum of 366 daily regional reanalysis values: 1,623.87 mm. Same regional value for all zones; not a rain-gauge measurement or local rainfall gradient. |
| NDVI | Copernicus Sentinel-2B L2A, 29 February 2024, tile 44PMV | (NIR−red)/(NIR+red); honours already-applied BOA offset. SCL classes 4/5 retain cloud-free land; at least 20% valid zonal sample coverage required. One date, not climatology. |
| Land use / cover | ESA WorldCover 2021 v200 | Modal sampled land-cover class; not parcel land use or development permission. |
| Soil | **Missing** | Accept sourced hydrologic soil group A/B/C/D through CSV; do not infer from vegetation. |
| Surface-water occurrence | EC JRC/Google GSW v1.4, 1984–2021 | Mean sampled occurrence, 0–100%; excludes nodata 255. Frequency of water presence, not water-area percentage. Legacy version has provider-reported inconsistencies corrected in v1.5; upgrade/validate before decisions. |

### Source descriptions

- Terrain service: https://www.mapzen.com/blog/terrain-tile-service/
- NASA POWER: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- Earth Search: https://github.com/Element84/earth-search
- Sentinel-2 processing: https://sentiwiki.copernicus.eu/web/s2-processing
- ESA WorldCover: https://esa-worldcover.org/en/data-access
- JRC GSW: https://global-surface-water.appspot.com/download

### Provenance files

The source manifest is stored at:

```text
data/priority/manifest.json
```

It records:

- source URLs;
- dates;
- bounding box;
- processing information;
- SHA-256 hashes.

Cached source subsets are stored under:

```text
data/priority/source/
```

The application does not require runtime API credentials or online analytical services for the bundled workflow.

The common 0.0005° grid uses nearest-neighbour samples of approximately 54 m rather than exhaustive native-resolution zonal statistics.

Study extent:

```text
80.10–80.28° E
12.88–13.16° N
```

### Attribution

© ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium.

Zanaga et al. (2022), DOI: 10.5281/zenodo.7254221 — CC BY 4.0.

Sentinel-2: Copernicus/ESA via Element 84.

Terrain: Mapzen/Tilezen and contributing sources.

Rainfall: NASA POWER.

Surface water: EC JRC/Google; Pekel et al. (2016), *Nature* 540, DOI: 10.1038/nature20584.

Sources remain their providers' products; this project adds demonstration analysis.

</details>

---

# 🛡️ Responsible AI by Design

> ## AI assists. Engineering governs. Humans review.

| 🤖 AI | ⚙️ ENGINEERING | 👤 HUMAN |
|---|---|---|
| Interpretation assistance | Authoritative deterministic calculations | Final judgement |
| Optional advisory layer | Safety gates | Field validation |
| No infrastructure command authority | Mass-balanced allocation | Professional review |

### Current AI boundary

- Moss remains optional and disabled by default.
- The Water Conservation Priority Map requires no AI calls.
- Authoritative engineering values remain in the deterministic core.
- Advisory output cannot command infrastructure.

This project is not autonomous infrastructure.

---

# 🔌 From Software to Future Edge Intelligence

The separate ESP32 device is a **physical proof-of-concept** exploring possible future sensing and edge-control integration.

Recommended authentic media path:

```text
Docs/esp32-prototype.jpg
```

If authentic team-owned prototype media is available:

```html
<p align="center">
  <img src="Docs/esp32-prototype.jpg"
       width="70%"
       alt="ESP32 Water Bank physical proof-of-concept" />
</p>
```

> **Physical proof-of-concept · currently offline · not a live Chennai deployment**

Separate prototype interface:

https://chennai-water-bank-prototype-1032997828322.asia-south1.run.app/prototype_node

---

# 🏗️ System Architecture

```mermaid
flowchart TB
    subgraph GEO["GEOSPATIAL PLANNING"]
        DS["Public Geospatial Sources"]
        PP["Offline Processing"]
        PI["Priority Engine"]
        PM["Interactive Priority Map"]
        DS --> PP --> PI --> PM
    end

    subgraph ENG["DETERMINISTIC WATER BANK"]
        HY["Hydrology"]
        DE["Decision Engine"]
        SIM["Simulation"]
        IMP["Impact Analytics"]
        HY --> DE --> SIM --> IMP
    end

    subgraph ADV["OPTIONAL ADVISORY LAYER"]
        AI["Moss / AI Interpretation"]
    end

    PM -. "planning context" .-> HY
    IMP -. "authoritative values" .-> AI
```

<details>
<summary><strong>🧑‍💻 View repository architecture</strong></summary>

```text
app.py / pages/
    Existing Streamlit entry and navigation

pages/00_water_conservation_priority_map.py
    New Problem 2.3 priority page

src/geospatial/priority.py
    Normalization, scoring, classification, recommendation

src/geospatial/data.py
    Offline evidence and validated CSV import

src/config/settings.py
    Central geospatial assumptions + unchanged engine settings

scripts/build_priority_sample.py
    Optional reproducible source preprocessing

data/priority/
    GeoJSON, provenance and source subsets

src/decision/ + src/hydrology/
    Existing deterministic engineering core

src/simulation/ + src/impact/
    Existing synthetic scenarios and volume accounting

src/agents/ + src/memory/
    Optional advisory layer
```

</details>

---

# 🔬 What the Prototype Does — and Does Not Claim

| ✅ DOES | ❌ DOES NOT CLAIM |
|---|---|
| Screen demonstration analysis zones | Official micro-watershed delineation |
| Combine source-derived spatial indicators | Scientifically calibrated Chennai policy weights |
| Support all eight challenge inputs | Complete bundled evidence for all eight |
| Explain priority contributions | Certified recharge suitability |
| Evaluate synthetic Water Bank scenarios | Live Chennai infrastructure operation |
| Account for simulated volumes | Hydraulic flood-depth prediction |
| Provide advisory AI interpretation | Autonomous infrastructure control |

This distinction is intentional.

Scientific transparency is part of the engineering design.

---

<details>
<summary><strong>⚠️ Current limitations and required validation</strong></summary>

- Demonstration rectangles, not official micro-watersheds.
- DEM conditioning, catchment delineation and boundary validation remain outstanding.
- Soil and drainage density are missing from the bundled sample.
- Six-input rankings are provisional.
- Import sourced missing evidence for the full supported model.
- Mixed acquisition periods.
- Single-date NDVI.
- Regional rainfall is shared by all zones.
- Limited terrain resolution.
- Sampled zonal aggregation.
- Legacy JRC v1.4 occurrence caveat.
- Demonstration weights, normalization anchors and thresholds remain uncalibrated.
- Priority is not intervention effectiveness.
- Priority is not recharge permission.
- No live physical sensing.
- No autonomous infrastructure control.
- No calibrated hydraulic flood-depth or flood-damage model.
- External map tiles require internet.
- Scoring, tables, recommendations and polygon geometry do not require external map tiles.

</details>

---

# ✅ Engineering Validation

At the verified adaptation baseline:

| Validation item | Recorded result |
|---|---|
| Tests | **103 passed** |
| Coverage | **95.30%** |
| Python | **3.12.14** |
| Ruff | **Passed** |
| compileall | **Passed** |
| GitHub CI | **Passed at verified revision** |

Verified commit:

https://github.com/Janicebenita/CHENNAI_WATER_BANK_AI/commit/03f83ea2d96a6b032c9d4fffee1907318157e694

These are recorded results for that verified revision.

The CI badge at the top reflects the latest workflow status.

---

# 🚀 Run Locally

## Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

$env:DATA_BACKEND="memory"
$env:MOSS_ENABLED="false"

python -m streamlit run app.py
```

## Linux / macOS

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

export DATA_BACKEND=memory
export MOSS_ENABLED=false

python -m streamlit run app.py
```

## Validation

```powershell
python -m pytest
python -m ruff check .
python -m compileall -q app.py pages src tests scripts
```

No runtime dependency, Docker startup, port or CI changes were required for this adaptation.

Cloud Run continues listening on:

```text
0.0.0.0:$PORT
```

Bundle:

```text
data/priority/
```

with deployment.

Optional geospatial preparation:

```powershell
python -m pip install rasterio Pillow
python scripts/build_priority_sample.py
```

The preprocessing script:

- reuses cached subsets;
- performs no credentialed access;
- does not run during application startup;
- may fetch public data if cache files are absent;
- requires source/version and hash verification after refresh.

---

# 📂 Repository Guide

| Path | Purpose |
|---|---|
| `pages/00_water_conservation_priority_map.py` | Problem 2.3 interactive map |
| `src/geospatial/priority.py` | Normalization, scoring and classification |
| `src/geospatial/data.py` | Evidence loading and validated imports |
| `src/config/settings.py` | Geospatial assumptions and configuration |
| `data/priority/` | Priority data, provenance and source subsets |
| `scripts/build_priority_sample.py` | Reproducible preprocessing |
| `src/hydrology/` | Deterministic hydrology |
| `src/decision/` | Engineering decision logic |
| `src/simulation/` | Synthetic scenario simulation |
| `src/impact/` | Volume accounting |
| `src/agents/` | Optional advisory layer |

---

# 🔄 Optional Data Import

The optional CSV import supports all eight challenge indicators.

The import requires:

- every demonstration zone exactly once;
- all eight indicator columns;
- source declaration;
- observation period.

Validation rejects:

- duplicate zones;
- invalid numerical ranges;
- unknown classes;
- absent provenance declarations.

Blank values remain missing.

Imported declarations are marked:

> **user-supplied, not independently verified**

Imports affect only the current session.

They do not overwrite bundled source files.

---

# 🌐 Existing Staging Demo

Existing Water Bank staging service:

https://chennai-water-bank-ai-staging-1032997828322.asia-south1.run.app/

> **Note:** this staging service may predate the new Problem 2.3 Priority Map adaptation. Do not present it as verification of the new priority page until the updated deployment is confirmed.

---

# 👥 Team LOGOS VICTORIS

| Role | Team Member |
|---|---|
| **Team Lead** | **[Janice Benita F](https://github.com/Janicebenita)** |
| **Team Member** | **Tytus Glaston** |

Built for:

**GeoImpathon 1.0 — Geospatial Ideas for Greener Earth**  
**Water Resource Management · Problem Statement 2.3**

---

# 🔗 Project Links

<p align="center">
  <a href="https://github.com/Janicebenita/CHENNAI_WATER_BANK_AI"><strong>Submission Repository</strong></a>
  ·
  <a href="https://github.com/Janicebenita/chennai-water-bank-ai"><strong>Original Project</strong></a>
  ·
  <a href="https://www.youtube.com/watch?v=hvbKTbRtTag"><strong>Earlier Water Bank Demo</strong></a>
</p>

> The earlier video demonstrates the Water Bank system. It does **not** demonstrate the newly added Problem 2.3 Water Conservation Priority Map.

---

<h2 align="center">
🌧️ MAP → PRIORITIZE → CONSERVE → ACT 💧
</h2>

<h3 align="center">
Bank the Rain. Reduce Immediate Runoff.<br />
Build Urban Water Resilience.
</h3>

<p align="center">
  <strong>CHENNAI WATER BANK AI</strong><br />
  Geospatial Water Conservation Priority Mapping &amp; Distributed Rainwater Intelligence
</p>

---

## Final Project Position

**Chennai Water Bank AI connects transparent geospatial water-conservation priority screening with explainable recommendations and a separate deterministic Water Bank simulation — helping move from identifying WHERE intervention deserves investigation toward understanding WHAT could be evaluated next.**
