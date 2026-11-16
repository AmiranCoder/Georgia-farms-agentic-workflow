# Nationwide Georgia Fresh Produce Directory — Multi-Agent System Architecture

Modeled after [farmsaround.com](https://farmsaround.com), this system orchestrates autonomous AI agents to discover, verify, geocode, and publish a comprehensive, interactive nationwide directory of local agriculture in the Republic of Georgia (საქართველო).

The architecture is explicitly grounded in **Andrew Ng's 4 Agentic AI Design Patterns**:
1. **Planning**: Goal decomposition into staged execution loops, dynamic query generation, and mandatory pre-execution checklist validation in `plan.md`.
2. **Reflection**: Multi-pass critique and verification cycles where a specialized agent validates source recency (2025–2026), filters out industrial importers/supermarket chains, and tests contact veracity.
3. **Tool Use**: Leveraging external tools including bilingual web search engines, OpenStreetMap/Nominatim geocoders, bounding-box evaluators, and Leaflet map synthesizers.
4. **Multi-Agent Collaboration**: Specialized functional roles passing structured, typed artifacts through discrete pipeline stages (`raw_leads.json` → `verified_farms.json` → `georgia_farms_map.html`).

---

## 1. Core Objectives & Scope

### Primary Mission
Identify active, authentic local producers, farm gates, artisanal cheese and dairy workshops, pick-your-own operations, and farm-to-table delivery cooperatives across all 9 historic and administrative agricultural regions of Georgia:
- **Kakheti (კახეთი)**: Viticulture, artisan wine farms, sun-grown vegetables, sheep cheese (Tushuri Guda), fruit orchards.
- **Kartli / Kvemo Kartli & Shida Kartli (ქართლი / ქვემო ქართლი & შიდა ქართლი)**: Stone fruits, apples, greenhouse vegetables, dairy clusters, Sulguni/Imeruli cooperatives.
- **Imereti (იმერეთი)**: Herbs, greenhouse greens, Imeretian cheese, corn, wine varieties (Tsitska/Tsolikouri).
- **Samegrelo (სამეგრელო)**: Hazelnut groves, Megrelian Sulguni, dairy farms, subtropical crops.
- **Adjara (აჭარა)**: Citrus, tea plantations, high-altitude alpine dairy hubs, honey.
- **Samtskhe-Javakheti (სამცხე-ჯავახეთი)**: Alpine Tenili and Meskhian cheeses, seed potatoes, mountain apiaries.
- **Guria (გურია)**: Artisanal tea, citrus, hazelnuts, local dairy and poultry.
- **Racha-Lechkhumi & Kvemo Svaneti (რაჭა-ლეჩხუმი)**: Mountain ham, local beans, high-altitude honey, mountain viticulture.
- **Mtskheta-Mtianeti (მცხეთა-მთიანეთი)**: High-altitude dairy, mountain herbs, trout farms, eco-farms.

### Standard Categories
Every lead must be classified into exactly one of four core categories:
1. `farm_shop`: On-farm store, farm gate sales point, artisanal winery/estate shop selling local farm produce directly to consumers (ფერმის მაღაზია, ადგილობრივი მარანი / პროდუქციის გაყიდვა).
2. `dairy_hub`: Cheese dairy, creamery, milk collection and processing cooperative producing authentic Georgian cheeses such as Sulguni, Tushuri Guda, Tenili, or Imeruli (ყველის საწარმო, რძის გადამამუშავებელი ქარხანა / კოოპერატივი).
3. `pick_your_own`: Orchards, berry plantations, and vineyards offering self-harvesting and direct consumer picking experiences (თვითკრეფა, ხილის / კენკრის ბაღები).
4. `delivery_coop`: Farmer association, regional community-supported agriculture (CSA), or direct producer-to-door delivery cooperative operating locally (სასოფლო-სამეურნეო კოოპერატივი, ფერმერული პროდუქტების მიტანის სერვისი).

---

## 2. Mandatory Operational Rules

### Rule A: Mandatory Planning (`plan.md`)
Before running any web extraction, scraper, verifier, or map generation scripts, agents **MUST** create or update `plan.md`. The plan must articulate:
- Current targeted regions and categories.
- Specific hypotheses and search queries.
- Defined input/output artifact states.
- Explicit checklist of milestones with completed/pending status indicators.

### Rule B: Mandatory Bilingual Search (ქართული & English)
All search procedures must execute parallel queries in both English and Georgian. Georgian agricultural enterprises frequently maintain Facebook pages, cooperative registries, or regional directories exclusively in Georgian script (`მხედრული`). 
- **Georgian terms**: ფერმა, მეურნეობა, აგროტურისტული ფერმა, ყველის საწარმო, რძის გადამუშავება, თვითკრეფა, კენკრის ბაღი, სასოფლო-სამეურნეო კოოპერატივი, ნატურალური პროდუქტები, გუდა, სულგუნი, თენირი, კახეთი, ქართლი, ა.შ.
- **English terms**: farm shop, dairy farm, artisanal cheese Georgia, pick your own berries Georgia, fruit orchard Kakheti, farm delivery cooperative Tbilisi Georgia.

### Rule C: Andrew Ng's Reflection Standard
Raw internet leads must never be directly published. The `quality-verifier` agent must inspect every candidate lead:
- Exclude nationwide grocery chains (Carrefour, Goodwill, Nikora, Spar, Ori Nabiji, Magniti).
- Exclude wholesale food importers, packaging distributors, and chemical/fertilizer suppliers.
- Confirm active operation in 2025–2026 (or active social media/website presence).
- Confirm valid Georgian telephone contact format starting with `+995` (e.g., `+995 5XX XX XX XX` or landline `+995 32 2XX XX XX`).
- Flag and correct hallucinated locations or improper categories.

### Rule D: Strict Geographic Bounding Box Evaluation
All geocoded farm locations must be strictly validated against the official territorial bounding box of Georgia:
- **Latitude**: `41.0000° N` to `43.5000° N`
- **Longitude**: `40.0000° E` to `46.7000° E`
Any coordinate falling outside this boundary fails evaluation and must either be re-geocoded using high-resolution administrative data (village, municipality, region) or dropped.

---

## 3. Multi-Agent Team Structure

```
+-------------------------------------------------------------+
|                      Lead Orchestrator                      |
|                  (Maintains plan.md & State)                |
+-------------------------------------------------------------+
                               |
        +----------------------+----------------------+
        |                                             |
        v                                             v
+-----------------------+                    +-----------------------+
|    Regional Scout     |                    |   Quality Verifier    |
| (agent/skills/        | === raw_leads ===> | (agent/skills/        |
|  regional-scout)      |       .json        |  quality-verifier)    |
| Pattern: Tool Use     |                    | Pattern: Reflection   |
+-----------------------+                    +-----------------------+
                                                         |
                                                verified_farms.json
                                                         |
                                                         v
                                             +-----------------------+
                                             |     Map Publisher     |
                                             | (agent/skills/        |
                                             |  map-publisher)       |
                                             | Pattern: Tool & Eval  |
                                             +-----------------------+
                                                         |
                                                georgia_farms_map.html
```

### Agent Roles & Skills
1. **Regional Scout (`agent/skills/regional-scout/skill.md`)**
   - **Responsibility**: Systematic bilingual scanning of target regions.
   - **Artifacts Handled**: Writes and runs `execution/search_georgia.py`; outputs `output/raw_leads.json`.
   - **Pattern**: Tool Use & Planning.

2. **Quality Verifier (`agent/skills/quality-verifier/skill.md`)**
   - **Responsibility**: In-depth critique, deduping, telephone formatting, activity verification (2025–2026), and strict exclusion filtering.
   - **Artifacts Handled**: Reads `output/raw_leads.json`; outputs `output/verified_farms.json`.
   - **Pattern**: Reflection & Self-Correction.

3. **Map Publisher (`agent/skills/map-publisher/skill.md`)**
   - **Responsibility**: Geocoding, bounding-box evaluation, categorization styling, and HTML/Leaflet map rendering.
   - **Artifacts Handled**: Reads `output/verified_farms.json`; outputs `output/georgia_farms_map.html`.
   - **Pattern**: Tool Use & Quantitative Evaluations.

---

## 4. Standard Data Schema

### Raw Lead Schema (`output/raw_leads.json`)
```json
[
  {
    "id": "raw-001",
    "name_en": "Marani & Dairy Farm Kakheti",
    "name_ka": "მარანი და რძის ფერმა კახეთი",
    "region": "Kakheti",
    "municipality_or_village": "Telavi",
    "category": "dairy_hub",
    "phone": "+995 599 12 34 56",
    "website_or_social": "https://facebook.com/...",
    "source_url": "https://...",
    "products": ["Tushuri Guda Cheese", "Cow Milk", "Rkatsiteli Wine"],
    "description": "Artisanal dairy workshop and vineyard offering cheese tastings.",
    "discovered_at": "2026-11-16T10:27:00Z"
  }
]
```

### Verified Farm Schema (`output/verified_farms.json`)
```json
[
  {
    "id": "farm-geo-001",
    "name_en": "Marani & Dairy Farm Kakheti",
    "name_ka": "მარანი და რძის ფერმა კახეთი",
    "region": "Kakheti",
    "municipality_or_village": "Telavi",
    "address": "Telavi Municipality, Kakheti, Georgia",
    "category": "dairy_hub",
    "phone": "+995 599 12 34 56",
    "phone_verified": true,
    "website_or_social": "https://facebook.com/...",
    "products": ["Tushuri Guda Cheese", "Cow Milk", "Rkatsiteli Wine"],
    "description": "Artisanal dairy workshop producing certified Tushuri Guda.",
    "verification_status": "verified",
    "activity_checked_2025_2026": true,
    "reflection_notes": "Confirmed active Facebook page updated in 2025; direct producer not a retailer."
  }
]
```

### Published Map Feature (Embedded in `output/georgia_farms_map.html`)
Contains geocoded `lat` / `lon` conforming to `41.0 <= lat <= 43.5` and `40.0 <= lon <= 46.7`, custom Leaflet pin markers color-coded by category, searchable UI drawer, filter toggles by region and category, and bilingual popups.
