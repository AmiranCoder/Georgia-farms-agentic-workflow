---
name: regional-scout
description: Discovers raw farm, farm shop, dairy hub, pick-your-own, and delivery cooperative leads across Georgia using bilingual web searches and structured extraction.
---

# Regional Scout Skill

## Role & Mission
The **Regional Scout** is an autonomous discovery agent responsible for systematically exploring regions across the Republic of Georgia to uncover authentic local farms, farm shops, artisan creameries/dairies, pick-your-own operations, and delivery cooperatives.

This skill is designed around **Andrew Ng's Tool Use and Planning Patterns**:
- Formulates multi-angle bilingual search queries.
- Generates and executes `execution/search_georgia.py`.
- Aggregates unstructured web data into structured JSON at `output/raw_leads.json`.

---

## 1. Operating Procedure

### Step 1: Pre-Execution Planning Alignment
- Inspect `plan.md` to identify the designated target regions (e.g., Kakheti, Kvemo Kartli) and categories for the current cycle.
- Do not run discovery on unlisted regions without updating `plan.md`.

### Step 2: Query Generation Matrix
For each target region, construct bilingual query matrices pairing the region with each category:

| Category | English Query Formats | Georgian Query Formats (ქართული) |
|---|---|---|
| `farm_shop` | `"{region} farm shop"`, `"{region} organic farm Georgia direct sale"` | `"{region_ka} ფერმის მაღაზია"`, `"{region_ka} ფერმერული მეურნეობა გაყიდვა"` |
| `dairy_hub` | `"{region} cheese factory Georgia"`, `"{region} dairy farm Sulguni Guda"` | `"{region_ka} ყველის საწარმო"`, `"{region_ka} რძის გადამუშავება ქარხანა"` |
| `pick_your_own` | `"{region} pick your own fruit Georgia"`, `"{region} berry orchard visit"` | `"{region_ka} თვითკრეფა"`, `"{region_ka} ხილის ბაღი კრეფა"` |
| `delivery_coop` | `"{region} agricultural cooperative Georgia"`, `"farm delivery {region} Georgia"` | `"{region_ka} სასოფლო სამეურნეო კოოპერატივი"`, `"ფერმერული პროდუქტების მიტანა"` |

### Step 3: Script Authoring & Execution
Author `execution/search_georgia.py` which:
1. Queries web search APIs, Google/DuckDuckGo endpoints, and verified public directories (e.g., Rural Development Agency of Georgia RDA, Georgian Farmers' Association GFA, Elkana Bio Farmers, Facebook farm directory pages).
2. Parses titles, snippets, phone numbers, location hints, and web URLs.
3. Formats records according to the standard Raw Lead Schema.
4. Appends or writes records to `output/raw_leads.json` safely.

### Step 4: Verification of Scout Output
Ensure `output/raw_leads.json`:
- Is valid JSON.
- Contains all mandatory raw fields (`id`, `name_en`, `name_ka`, `region`, `municipality_or_village`, `category`, `phone`, `website_or_social`, `source_url`, `products`, `description`, `discovered_at`).
- Has populated phone numbers or social links where available.

---

## 2. Input / Output Specifications

- **Input**: Target regions from `plan.md` and bilingual search configurations.
- **Output**: `output/raw_leads.json` (Structured array of raw candidate entities).
- **Execution Script**: `execution/search_georgia.py`.

---

## 3. Success Metrics
- 100% of discovered items belong to one of the 4 defined categories.
- Both Georgian and English name fields (`name_en`, `name_ka`) are populated.
- Output file exists and is cleanly serializable.
