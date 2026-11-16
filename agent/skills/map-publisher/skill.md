---
name: map-publisher
description: Geocodes verified farm locations, enforces bounding-box evaluation standards, and publishes an interactive Leaflet map to georgia_farms_map.html.
---

# Map Publisher Skill (Tool Use & Geographic Evals)

## Role & Mission
The **Map Publisher** agent is responsible for converting textual farm directories into an interactive, visually rich, geospatial product modeled after [farmsaround.com](https://farmsaround.com).

This skill embodies **Andrew Ng's Tool Use and Quantitative Evaluations Patterns**:
- Uses geocoding APIs and fallback geographic gazetteers to resolve coordinates.
- Applies strict quantitative validation (bounding-box evaluation: `41.0 <= lat <= 43.5`, `40.0 <= lon <= 46.7`).
- Generates a standalone, dependency-bundled, mobile-responsive Leaflet interactive map at `output/georgia_farms_map.html`.

---

## 1. Operating Procedure

### Step 1: Geocoding Pipeline
Author and execute `execution/geocode_farms.py`:
1. Read `output/verified_farms.json`.
2. For each farm, attempt high-precision geocoding using:
   - Specific village/town and municipality name in Georgia (e.g., `Tsinandali, Telavi Municipality, Kakheti, Georgia`).
   - OpenStreetMap / Nominatim API (with polite user-agent header and rate limiting).
   - Local fallback gazetteer for Georgian municipalities and major farming villages to guarantee zero-failure offline resilience.

### Step 2: Geographic Evaluation Gate (Bounding Box)
Every geocoded coordinate pair `(lat, lon)` is evaluated against Georgia's official territory limits:
- **Latitude**: `41.0000 <= lat <= 43.5000`
- **Longitude**: `40.0000 <= lon <= 46.7000`

**Evaluation Rules**:
- Coordinates outside this bounding box (e.g. accidentally pointing to Georgia, USA, or ocean) **FAIL** evaluation and must be re-geocoded against the specific Georgian municipality or flagged.
- Only entities passing 100% bounding box evaluations are written to the map data payload.

### Step 3: Interactive Leaflet Map Generation
Author and execute `execution/publish_map.py` to create `output/georgia_farms_map.html`.
The interactive map must provide:
1. **Modern Responsive UI**:
   - Sidebar/drawer showing farm listings, live search bar, and filter buttons by Category and Region.
   - Header with stats summary (Total Farms, Regions Covered, Active Categories).
2. **Category-Themed Custom Markers**:
   - `farm_shop`: Emerald Green / Shop icon.
   - `dairy_hub`: Amber Gold / Cheese & Milk icon.
   - `pick_your_own`: Crimson Berry / Fruit icon.
   - `delivery_coop`: Royal Blue / Truck & Delivery icon.
3. **Bilingual Interactive Popups**:
   - Farm name in English and Georgian (`სახელი ქართულად`).
   - Category badge with color coding.
   - Address and Municipality.
   - Phone with clickable `tel:` link.
   - Products tag list.
   - Direct link to website / Facebook page.
4. **Interactive Controls**:
   - Search by name, product (e.g. "Guda", "strawberries", "wine", "cheese"), village, or region.
   - Category filter pills.
   - Region selector.
   - "Zoom to Fit Nationwide" and region quick-jump buttons.

---

## 2. Input / Output Specifications

- **Input**: `output/verified_farms.json`.
- **Outputs**:
  - `output/georgia_farms_map.html` (Standalone interactive Leaflet map).
  - Geocoding and evaluation report in console / logs.
- **Execution Scripts**:
  - `execution/geocode_and_publish.py` (or `execution/publish_map.py`).

---

## 3. Success Metrics
- 100% of plotted coordinates pass bounding-box evaluation (`41.0 <= lat <= 43.5` and `40.0 <= lon <= 46.7`).
- Leaflet map loads cleanly in any browser with interactive panning, zooming, filtering, and popup dialogs.
- Clear bilingual presentation for local and international users.
