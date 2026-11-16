# Execution Plan: Nationwide Georgia Fresh Produce Directory

**Current Status**: IN PROGRESS (Nationwide Scale-up Phase)  
**Target Regions**: Nationwide across Georgia:
- **Tbilisi & Surroundings**: Tbilisi (თბილისი), Mtskheta-Mtianeti (მცხეთა-მთიანეთი)
- **Central & Southern Georgia**: Shida Kartli (შიდა ქართლი), Kvemo Kartli (ქვემო ქართლი), Samtskhe-Javakheti (სამცხე-ჯავახეთი)
- **Western & Black Sea Georgia**: Imereti (იმერეთი), Samegrelo-Zemo Svaneti (სამეგრელო), Adjara (აჭარა), Guria (გურია), Racha-Lechkhumi (რაჭა-ლეჩხუმი)
- **Eastern Viticulture & Dairy Hub**: Kakheti (კახეთი)

**Target Categories**: `farm_shop`, `dairy_hub`, `pick_your_own`, `delivery_coop`  
**Agentic AI Patterns Applied**: Planning, Tool Use, Reflection, Multi-Agent Collaboration

---

## 1. Objectives & Scope
Scale the directory from the 2-region pilot to a nationwide directory covering all agricultural regions and the capital:
1. **Tbilisi & Surroundings**: Fresh dairy (matsoni, artisanal cheese, raw milk), free-range village eggs (სოფლის კვერცხი), farm-raised poultry/meat (სოფლის ხორცი), and organic farm-to-table delivery cooperatives.
2. **Central & Southern Georgia**: Stone fruits (peaches, plums), apples, seed & mountain potatoes, highland alpine cheeses (Tenili), and mountain honey.
3. **Western & Black Sea Georgia**: Hazelnuts, artisanal tea plantations, citrus, Megrelian Sulguni, Rachuli smoked ham (Lori) & slow-cooked beans, berries, and agritourism farms.
4. **Eastern Georgia**: Viticulture, Tushuri Guda cheese, fruit orchards, and winery farm shops.

Strict quality controls: no mass supermarkets (Carrefour, Goodwill, Nikora, Agrohub retail branches, Spar) or mass resellers. Only authentic primary producers, artisanal processors, and genuine farm delivery cooperatives with verified active presence in 2025–2026.

---

## 2. Bilingual Search Hypotheses & Query Strategy

### Tbilisi & Mtskheta-Mtianeti
- **Delivery Coop / Farm Shop**:
  - EN: `"Tbilisi farm delivery cooperative"`, `"saguleti farm delivery matsoni eggs"`, `"ebazaar.ge georgia farm produce"`
  - KA: `"თბილისი სოფლის პროდუქტები მიტანა"`, `"საგულეთი ფერმა მაწონი კვერცხი"`, `"ებბაზარი ფერმერული პროდუქტები"`
- **Dairy / Trout / Agrotourism**:
  - EN: `"Mtskheta monastery dairy honey"`, `"Pasanauri Aragvi trout farm Mtskheta-Mtianeti"`
  - KA: `"მცხეთის მონასტრის მაწონი ყველი"`, `"ფასანაური არაგვის კალმახის ფერმა"`

### Central & Southern (Shida Kartli, Samtskhe-Javakheti)
- **Farm Shop / Pick-Your-Own**:
  - EN: `"Gori apple orchard farm shop"`, `"Ateni stone fruit peach farm Gori"`, `"Kaspi plum orchard"`
  - KA: `"გორის ვაშლის ბაღი ფერმა"`, `"ატენის ატმის ბაღი შიდა ქართლი"`, `"კასპის ხეხილის ბაღები"`
- **Dairy Hub / Potatoes**:
  - EN: `"Akhaltsikhe Tenili cheese Inasaridze farm"`, `"Moskhi potato cooperative Tsnisi Samtskhe-Javakheti"`
  - KA: `"ინასარიძის ფერმა თენილი ყველი ანდრიაწმინდა"`, `"კოოპერატივი მოსხი მესხური კარტოფილი წნისი"`

### Western & Black Sea (Imereti, Samegrelo, Adjara, Guria, Racha-Lechkhumi)
- **Dairy Hub & Farm Shop**:
  - EN: `"Imeretian cheese Kutaisi dairy farm"`, `"Samegrelo Sulguni farm Zugdidi"`, `"Racha Natural Products Ambrolauri"`
  - KA: `"იმერული ყველის ფერმა ქუთაისი"`, `"სამეგრელოს სულგუნის ფერმა ზუგდიდი"`, `"რაჭის ნატურალური პროდუქტები ამბროლაური"`
- **Tea & Citrus & Berries**:
  - EN: `"Tenitea organic tea farm Guria Ozurgeti"`, `"Shuakhevi alpine honey citrus farm Adjara"`, `"Likhauri hazelnut Guria"`
  - KA: `"ტენითი ორგანული ჩაის ფერმა გურია ოზურგეთი"`, `"შუახევის სამთო თაფლი აჭარა"`, `"ლიხაურის თხილის ფერმა"`

---

## 3. Pipeline Milestones & Checklist

- [x] **Phase 0: Workspace Architecture Setup**
  - [x] Create `agents.md` root context with Andrew Ng's agentic patterns
  - [x] Create `agent/skills/regional-scout/skill.md`
  - [x] Create `agent/skills/quality-verifier/skill.md`
  - [x] Create `agent/skills/map-publisher/skill.md`
  - [x] Create empty `execution/` and `output/` directories

- [x] **Phase 1: Pilot Regional Scout Execution (Kakheti & Kvemo Kartli)** ✅ 2026-11-16
- [x] **Phase 2: Pilot Quality Verifier Reflection Loop** ✅ 2026-11-16
- [x] **Phase 3: Pilot Map Publisher & Geospatial Evaluation** ✅ 2026-11-16
- [x] **Phase 4: Tile Style Upgrade (Google Maps Road & Satellite switcher)** ✅ 2026-11-16

- [x] **Phase 5: Nationwide Scale-up (All Regions & Tbilisi)** ✅ 2026-11-16
  - [x] Scaled `execution/search_georgia.py` to nationwide scope: 32 raw leads gathered across 11 regions (Tbilisi + 10 administrative regions)
  - [x] Updated `execution/verify_leads.py` with 4-gate reflection audit:
    - 🔴 Caught & rejected `Agrohub Saburtalo Retail Branch` (supermarket chain)
    - 🔴 Caught & rejected `Goodwill Vake Supermarket` (supermarket chain)
    - 🔴 Caught & rejected `Carrefour Georgia — Rustavi Hypermarket` (supermarket chain)
    - 🔴 Caught & rejected `Tsalka Mountain Dairy Hub (No Contact)` (Gate 2 contact veracity failure)
    - 🟢 Verified 28 genuine primary agricultural producers & artisanal cooperatives with active 2025–2026 presence and normalized +995 contacts
  - [x] Updated `execution/publish_map.py` with high-precision nationwide gazetteer:
    - 28/28 verified farms geocoded with **100% Bounding-Box PASS** (`41.0 <= lat <= 43.5`, `40.0 <= lon <= 46.7`, 0 failures)
  - [x] Regenerated `output/georgia_farms_map.html`:
    - Full nationwide Region dropdown filter (Tbilisi, Adjara, Guria, Imereti, Kakheti, Kvemo Kartli, Mtskheta-Mtianeti, Racha-Lechkhumi, Samegrelo-Zemo Svaneti, Samtskhe-Javakheti, Shida Kartli)
    - Google Roadmap & Google Satellite live layer switcher in top-right
    - Category filtering (`farm_shop`, `dairy_hub`, `pick_your_own`, `delivery_coop`), bilingual Georgian/English cards, and live product/village search

- [x] **Phase 6: UI Polish & Bilingual Language Switcher** ✅ 2026-11-16
  - [x] Fixed faint horizontal grid lines between Leaflet tiles:
    - Added `.leaflet-container { background: #e8eaed !important; }`
    - Added `.leaflet-tile-container img { width: 256.5px !important; height: 256.5px !important; outline: 1px solid transparent; }`
  - [x] Integrated full Georgian / English switcher (`ქართული | EN`) in top-right header:
    - Dynamic Google Maps tile language via `&hl=ka` (Georgian map labels) and `&hl=en` (English map labels)
    - Fully translated UI elements: header title/subtitle, stats counters, search placeholder, region dropdown options, category filter pills (`ფერმერული მაღაზია`, `რძის პროდუქტები`, `კრეფა / აგროტურიზმი`, `მიტანის სერვისი`)
    - Sidebar cards & map popups dynamically switch titles, addresses, product tags, and descriptions between natural Georgian and English
    - Live multi-attribute search works across both languages seamlessly
  - [x] Replaced tile scale with subpixel margin overlap (`img.leaflet-tile { width: 256px !important; margin: -0.5px; padding: 0.5px; }`)

- [x] **Phase 7: Google Maps Navigation Links & Andrew Ng Agentic Evaluation Suite** ✅ 2026-11-16
  - [x] Generated real Google Maps navigation links (`https://www.google.com/maps/search/?api=1&query=<lat>,<lon>`) for all 28 verified producers
  - [x] Rendered interactive navigation buttons in both sidebar cards and map pin popups:
    - English: `"📍 View on Google Maps"`
    - Georgian: `"📍 ნახე Google Maps-ზე"`
  - [x] Persisted coordinates & Google Maps URLs into `output/verified_farms.json`
  - [x] Regenerated `output/georgia_farms_map.html`
  - [x] Built `execution/evaluate_directory.py` auditing Schema, Geospatial Bounding Box, Balance, Duplicates, and Map Artifacts
  - [x] Ran evaluation suite: **Composite Score 100.0% (Grade: A+)**
  - [x] Saved comprehensive audit report to `output/eval_report.md`

- [x] **Phase 8: Mobile Responsiveness & Viewport Optimization (< 768px)** ✅ 2026-11-16
  - [x] Added viewport meta tag with `maximum-scale=1.0, user-scalable=no` for mobile browsers
  - [x] Added `@media (max-width: 768px)` stylesheet ensuring seamless smartphone interaction:
    - Compact header preventing horizontal overflow while keeping bilingual switcher & farm counter badge aligned
    - Horizontally scrollable single-row category filter pills (`overflow-x: auto`, `white-space: nowrap`)
    - Touch-friendly tap targets (`min-height: 40px`, padding: 9px 14px) for search inputs, dropdowns, and buttons
    - Mobile-responsive Leaflet popups with dynamic `maxWidth: 260`
    - Floating bottom toggle button (`"📋 List View (28)"` / `"🗺️ Map View"` in EN, `"📋 სიის ნახვა (28)"` / `"🗺️ რუკის ნახვა"` in KA) allowing one-tap switching between full-screen map and searchable farm list
  - [x] Regenerated `output/georgia_farms_map.html`
  - [x] Re-ran `execution/evaluate_directory.py`: **100.0% Pass (Grade A+)** with mobile responsiveness audit included



