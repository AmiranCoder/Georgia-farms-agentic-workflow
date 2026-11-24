#!/usr/bin/env python3
"""
Tbilisi Wide Real Dairy Map Publisher
Generates output/tbilisi_dairy_map.html and updates output/index.html.
Features:
- Centered on Tbilisi [41.7200, 44.7800], zoom 12
- District dropdown filters: All Tbilisi, Saburtalo, Vake, Vera / Mtatsminda, Dighomi, Didube / Chugureti, Gldani / Mukhiani, Nadzaladevi / Sanzona, Isani / Samgori, Varketili / Vazisubani, Avlabari / Ortachala
- 4 Dairy categories: Fresh Milk, Matsoni & Sour Cream & Cottage Cheese, Artisanal Cheese, Dairy Delivery
- Near Me button in sidebar controls (with distance calculation and radius filter)
- Google Maps view button with high contrast & readability
- Compact responsive popups for mobile devices
- WhatsApp direct click-to-chat links (wa.me)
- Bilingual KA / EN toggle
- Welcome modal: "ეს არის თბილისის ნატურალური რძის რუკა"
"""

import json
import os
import urllib.parse

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "output", "tbilisi_farms.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "output", "tbilisi_dairy_map.html")
INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "output", "index.html")

CAT_META = {
    "fresh_milk": {
        "color": "#0284c7",
        "emoji": "🥛",
        "label_en": "Fresh & Bio Milk",
        "label_ka": "ცოცხალი & ბიო რძე"
    },
    "matsoni_cream": {
        "color": "#059669",
        "emoji": "🥣",
        "label_en": "Matsoni, Cream & Curd",
        "label_ka": "მაწონი, არაჟანი & ხაჭო"
    },
    "cheese_artisan": {
        "color": "#d97706",
        "emoji": "🧀",
        "label_en": "Artisanal Cheese",
        "label_ka": "ხელნაკეთი ყველი"
    },
    "delivery_coop": {
        "color": "#7c3aed",
        "emoji": "🚚",
        "label_en": "Dairy Delivery",
        "label_ka": "რძის მიტანა"
    }
}

DISTRICT_GROUPS = [
    {"id": "all", "label_en": "All Tbilisi Districts", "label_ka": "მთელი თბილისი"},
    {"id": "Saburtalo", "label_en": "Saburtalo", "label_ka": "საბურთალო"},
    {"id": "Vake", "label_en": "Vake", "label_ka": "ვაკე"},
    {"id": "Vera", "label_en": "Vera / Mtatsminda", "label_ka": "ვერა / მთაწმინდა"},
    {"id": "Dighomi", "label_en": "Dighomi / Didi Dighomi", "label_ka": "დიღომი / დიდი დიღომი"},
    {"id": "Didube", "label_en": "Didube / Chugureti", "label_ka": "დიდუბე / ჩუღურეთი"},
    {"id": "Gldani", "label_en": "Gldani / Mukhiani", "label_ka": "გლდანი / მუხიანი"},
    {"id": "Nadzaladevi", "label_en": "Nadzaladevi / Sanzona", "label_ka": "ნაძალადევი / სანზონა"},
    {"id": "Isani", "label_en": "Isani / Samgori", "label_ka": "ისანი / სამგორი"},
    {"id": "Varketili", "label_en": "Varketili / Vazisubani", "label_ka": "ვარკეთილი / ვაზისუბანი"},
    {"id": "Avlabari", "label_en": "Avlabari / Ortachala", "label_ka": "ავლაბარი / ორთაჭალა"}
]

def map_district_group(district_name):
    if not district_name or district_name == "All Tbilisi":
        return "all"
    d = district_name.lower()
    if "saburtalo" in d:
        return "Saburtalo"
    elif "vake" in d:
        return "Vake"
    elif "vera" in d or "mtatsminda" in d:
        return "Vera"
    elif "dighomi" in d:
        return "Dighomi"
    elif "didube" in d or "chugureti" in d:
        return "Didube"
    elif "gldani" in d or "mukhiani" in d:
        return "Gldani"
    elif "nadzaladevi" in d or "sanzona" in d:
        return "Nadzaladevi"
    elif "isani" in d or "samgori" in d:
        return "Isani"
    elif "varketili" in d or "vazisubani" in d:
        return "Varketili"
    elif "avlabari" in d or "ortachala" in d:
        return "Avlabari"
    return "all"

def render_html(features):
    geojson_str = json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False)
    district_groups_json = json.dumps(DISTRICT_GROUPS, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="ka">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>თბილისის ნამდვილი რძის რუკა | Tbilisi Real Dairy Map</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; height: 100vh; display: flex; flex-direction: column; background: #f8fafc; color: #0f172a; }}
  
  /* Header */
  #header {{
    background: #0369a1; color: white; padding: 10px 20px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15); z-index: 1000; flex-shrink: 0;
  }}
  .header-left {{ display: flex; flex-direction: column; gap: 2px; }}
  #header-title {{ font-size: 1.15rem; font-weight: 800; display: flex; align-items: center; gap: 8px; }}
  #header-sub {{ font-size: 0.76rem; opacity: 0.9; color: #e0f2fe; }}
  .header-right {{ display: flex; align-items: center; gap: 14px; }}
  .lang-toggle {{
    background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.4);
    color: white; border-radius: 20px; padding: 4px 12px; font-size: 0.82rem;
    font-weight: 700; cursor: pointer; transition: all 0.2s;
  }}
  .lang-toggle:hover {{ background: rgba(255,255,255,0.3); }}
  .stats {{ font-size: 0.8rem; background: rgba(0,0,0,0.2); padding: 4px 10px; border-radius: 12px; }}

  /* Main Layout */
  #main {{ display: flex; flex: 1; overflow: hidden; position: relative; }}
  
  /* Sidebar */
  #sidebar {{
    width: 380px; background: white; border-right: 1px solid #e2e8f0;
    display: flex; flex-direction: column; z-index: 500; flex-shrink: 0;
  }}
  #controls {{ padding: 14px; border-bottom: 1px solid #e2e8f0; background: #f8fafc; }}
  
  .search-box {{ position: relative; margin-bottom: 10px; }}
  .search-box input {{
    width: 100%; padding: 8px 12px 8px 34px; border: 1px solid #cbd5e1;
    border-radius: 8px; font-size: 0.88rem; outline: none; transition: border 0.2s;
  }}
  .search-box input:focus {{ border-color: #0284c7; }}
  .search-icon {{ position: absolute; left: 10px; top: 9px; font-size: 0.9rem; color: #64748b; }}
  
  .district-select {{
    width: 100%; padding: 8px 10px; border: 1px solid #cbd5e1;
    border-radius: 8px; font-size: 0.85rem; font-weight: 600;
    background: white; color: #0f172a; margin-bottom: 9px; outline: none; cursor: pointer;
  }}
  .district-select:focus {{ border-color: #0284c7; }}

  /* Near Me Button in Sidebar Controls */
  .near-me-btn {{
    display: flex; align-items: center; justify-content: center; gap: 7px;
    width: 100%; margin-bottom: 9px; padding: 8px 14px;
    background: white; border: 1.5px solid #0284c7; color: #0284c7;
    border-radius: 8px; font-size: 0.85rem; font-weight: 700;
    cursor: pointer; transition: all 0.2s ease;
  }}
  .near-me-btn:hover {{ background: #f0f9ff; }}
  .near-me-btn.active {{ background: #0284c7; color: white; }}

  /* Near Me Status Bar */
  .near-me-status-bar {{
    display: none; background: #e0f2fe; border: 1px solid #bae6fd;
    border-radius: 8px; padding: 7px 10px; margin-bottom: 9px;
    font-size: 0.78rem; color: #0369a1;
  }}
  .near-me-status-bar.visible {{ display: flex; flex-direction: column; gap: 5px; }}
  .nms-top {{ display: flex; align-items: center; justify-content: space-between; }}
  .nms-reset {{ background: none; border: none; color: #0284c7; font-weight: 700; cursor: pointer; font-size: 0.76rem; }}
  .nms-reset:hover {{ text-decoration: underline; }}
  .radius-selector {{ display: flex; align-items: center; gap: 6px; font-size: 0.76rem; }}
  .radius-selector select {{
    padding: 2px 6px; border: 1px solid #bae6fd; border-radius: 4px;
    background: white; font-size: 0.76rem; font-weight: 600; color: #0369a1; cursor: pointer;
  }}

  /* Categories */
  .cat-pills {{ display: flex; gap: 6px; overflow-x: auto; padding-bottom: 2px; }}
  .cat-pills::-webkit-scrollbar {{ height: 4px; }}
  .cat-pills::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 4px; }}
  .cat-pill {{
    flex: 0 0 auto; padding: 5px 10px; border-radius: 16px; font-size: 0.76rem;
    font-weight: 600; border: 1px solid #cbd5e1; background: white; color: #475569;
    cursor: pointer; transition: all 0.15s;
  }}
  .cat-pill:hover {{ background: #f1f5f9; }}
  .cat-pill.active {{ background: #0284c7; color: white; border-color: #0284c7; }}

  /* Cards List */
  #farm-list {{ flex: 1; overflow-y: auto; padding: 12px; display: flex; flex-direction: column; gap: 10px; }}
  .farm-card {{
    background: white; border: 1px solid #e2e8f0; border-radius: 10px;
    padding: 12px; cursor: pointer; transition: all 0.2s ease;
  }}
  .farm-card:hover {{ border-color: #0284c7; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.06); }}
  .farm-card.selected {{ border-color: #0284c7; background: #f0f9ff; }}
  
  .fc-cat {{ display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 700; color: white; margin-bottom: 6px; }}
  .fc-name {{ font-size: 0.96rem; font-weight: 700; color: #0f172a; margin-bottom: 2px; }}
  .fc-name-sec {{ font-size: 0.78rem; color: #64748b; margin-bottom: 5px; }}
  .fc-loc {{ font-size: 0.78rem; color: #475569; margin-bottom: 4px; display: flex; align-items: center; gap: 4px; }}
  .fc-phone {{ font-size: 0.8rem; margin-bottom: 6px; }}
  .fc-phone a {{ color: #128c7e; text-decoration: none; font-weight: 700; }}
  .fc-phone a:hover {{ text-decoration: underline; }}
  .fc-tags {{ display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 6px; }}
  .tag {{ background: #f1f5f9; color: #334155; font-size: 0.72rem; padding: 2px 7px; border-radius: 6px; }}
  
  .fc-distance-bar {{
    display: flex; align-items: center; gap: 6px; margin: 6px 0;
    font-size: 0.74rem; font-weight: 600;
  }}
  .dist-badge {{ display: inline-flex; align-items: center; gap: 3px; padding: 2px 6px; border-radius: 6px; }}
  .dist-km {{ background: #e0f2fe; color: #0369a1; }}
  .dist-drive {{ background: #fef3c7; color: #92400e; }}
  .dist-walk {{ background: #dcfce7; color: #166534; }}

  .fc-gmaps {{ margin-top: 6px; }}
  .gmaps-link {{
    display: inline-flex; align-items: center; justify-content: center; gap: 4px; width: 100%;
    background: #0f172a; color: #ffffff !important; border-radius: 6px;
    padding: 6px 10px; font-size: 0.76rem; font-weight: 700; text-decoration: none;
    transition: background 0.15s;
  }}
  .gmaps-link:hover {{ background: #1e293b; color: #38bdf8 !important; }}
  .fc-source {{ font-size: 0.68rem; color: #059669; margin-top: 4px; font-weight: 600; }}

  /* Map Container */
  #map {{ flex: 1; height: 100%; position: relative; }}

  /* Popups */
  .popup-card {{ padding: 4px; max-width: 290px; }}
  .popup-cat {{ display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: 700; color: white; margin-bottom: 6px; }}
  .popup-card h3 {{ font-size: 1.02rem; font-weight: 700; margin-bottom: 2px; color: #0f172a; }}
  .popup-sec {{ font-size: 0.8rem; color: #64748b; margin-bottom: 6px; }}
  .popup-addr {{ font-size: 0.8rem; color: #334155; margin-bottom: 6px; line-height: 1.35; }}
  .popup-phone {{ font-size: 0.82rem; margin-bottom: 5px; }}
  .popup-phone a {{ color: #128c7e; font-weight: 700; text-decoration: none; }}
  .popup-phone a:hover {{ text-decoration: underline; }}
  .popup-tags {{ display: flex; flex-wrap: wrap; gap: 4px; margin: 6px 0; }}
  .popup-desc {{ font-size: 0.78rem; color: #475569; line-height: 1.4; margin: 6px 0; }}
  .popup-notes {{ font-size: 0.72rem; color: #0369a1; margin-top: 4px; }}
  .popup-gmaps {{ margin-top: 8px; }}
  .gmaps-btn {{
    display: inline-flex; align-items: center; justify-content: center; width: 100%; text-align: center;
    background: #0f172a; color: #ffffff !important; padding: 8px 12px;
    border-radius: 8px; font-size: 0.84rem; font-weight: 700; text-decoration: none;
    box-shadow: 0 2px 6px rgba(15,23,42,0.3); transition: all 0.15s ease;
    border: 1px solid #1e293b; letter-spacing: 0.2px;
  }}
  .gmaps-btn:hover {{
    background: #1e293b; color: #38bdf8 !important;
    box-shadow: 0 4px 10px rgba(15,23,42,0.4);
  }}

  /* Welcome Modal */
  .modal-overlay {{
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    background: rgba(15, 23, 42, 0.65); backdrop-filter: blur(4px);
    display: flex; align-items: center; justify-content: center;
    z-index: 9999; opacity: 1; transition: opacity 0.25s ease;
  }}
  .modal-overlay.hidden {{ opacity: 0; pointer-events: none; }}
  .modal-card {{
    background: #ffffff; border-radius: 20px;
    padding: 28px 24px 22px; max-width: 440px; width: 90%;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3); text-align: center;
    border: 1.5px solid rgba(2, 132, 199, 0.25);
    animation: modalPop 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }}
  @keyframes modalPop {{
    0% {{ transform: scale(0.85); opacity: 0; }}
    100% {{ transform: scale(1); opacity: 1; }}
  }}
  .modal-icon {{ font-size: 2.8rem; line-height: 1; margin-bottom: 12px; }}
  .modal-title {{ font-size: 1.25rem; font-weight: 800; color: #0369a1; margin-bottom: 8px; line-height: 1.35; }}
  .modal-desc {{ font-size: 0.9rem; color: #475569; line-height: 1.55; margin-bottom: 20px; }}
  .modal-btn {{
    background: linear-gradient(135deg, #0369a1 0%, #0284c7 100%);
    color: white; border: none; border-radius: 24px;
    padding: 10px 28px; font-size: 0.92rem; font-weight: 700;
    cursor: pointer; box-shadow: 0 4px 12px rgba(2,132,199,0.35);
    transition: all 0.2s ease;
  }}
  .modal-btn:hover {{
    transform: translateY(-1.5px);
    box-shadow: 0 6px 16px rgba(2,132,199,0.45);
    background: linear-gradient(135deg, #02537c 0%, #0369a1 100%);
  }}

  /* Mobile Responsive */
  .mobile-toggle-btn {{ display: none; }}
  #no-results {{ display: none; padding: 20px; text-align: center; color: #666; font-size: 0.88rem; }}

  @media (max-width: 768px) {{
    #header {{ padding: 10px 14px; }}
    #header-title {{ font-size: 1.05rem; }}
    #header-title span {{ display: none; }}
    .stats {{ display: none; }}
    #main {{ position: relative; }}
    #sidebar {{
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      z-index: 800; transform: translateX(-100%); transition: transform 0.25s ease;
    }}
    #sidebar.mobile-active {{ transform: translateX(0); }}
    #map.mobile-hidden {{ display: none; }}
    .mobile-toggle-btn {{
      display: flex; align-items: center; justify-content: center;
      position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
      z-index: 1500; background: #0369a1; color: white;
      border: 2px solid white; border-radius: 30px;
      padding: 10px 22px; font-size: 0.92rem; font-weight: 700;
      box-shadow: 0 4px 14px rgba(0,0,0,0.38); cursor: pointer;
    }}

    /* Compact Leaflet Popups on Mobile */
    .leaflet-popup-content-wrapper {{
      padding: 4px;
      border-radius: 12px;
    }}
    .leaflet-popup-content {{
      margin: 10px 12px;
      max-width: 250px !important;
      min-width: 210px !important;
      line-height: 1.35;
    }}
    .popup-card {{
      max-width: 245px;
      padding: 0;
    }}
    .popup-card h3 {{
      font-size: 0.94rem;
      margin-bottom: 2px;
    }}
    .popup-sec {{
      font-size: 0.74rem;
      margin-bottom: 4px;
    }}
    .popup-addr {{
      font-size: 0.75rem;
      margin-bottom: 4px;
    }}
    .popup-phone {{
      font-size: 0.78rem;
      margin-bottom: 4px;
    }}
    .popup-tags {{
      gap: 3px;
      margin: 4px 0;
    }}
    .tag {{
      font-size: 0.68rem;
      padding: 2px 6px;
    }}
    .popup-desc {{
      font-size: 0.72rem;
      line-height: 1.35;
      margin: 4px 0;
      max-height: 60px;
      overflow-y: auto;
    }}
    .popup-distance-bar {{
      margin: 4px 0;
      gap: 4px;
    }}
    .dist-badge {{
      font-size: 0.68rem;
      padding: 2px 5px;
    }}
    .gmaps-btn {{
      padding: 6px 10px;
      font-size: 0.78rem;
      min-height: 36px;
    }}
  }}
</style>
</head>
<body>

<div id="header">
  <div class="header-left">
    <h1 id="header-title">🥛 Tbilisi Real Dairy Directory <span>| თბილისის ნამდვილი რძის ობიექტები</span></h1>
    <div id="header-sub">Verified Real Shops & Delivery across all Tbilisi Districts • Raw Milk, Bio Milk, Curd, Matsoni, Sour Cream</div>
  </div>
  <div class="header-right">
    <div class="stats"><span id="stat-total">0</span> <span id="stat-label">ობიექტი</span></div>
    <button class="lang-toggle" onclick="toggleLang()" id="lang-btn">English</button>
  </div>
</div>

<div id="main">
  <div id="sidebar">
    <div id="controls">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="search-input" placeholder="ძიება: რძე, მაწონი, ხაჭო, არაჟანი..." oninput="onSearchInput()">
      </div>

      <select class="district-select" id="district-select" onchange="onDistrictChange()">
        <!-- Populated via JS -->
      </select>

      <!-- Near Me Button in Sidebar -->
      <button id="near-me-btn" class="near-me-btn" onclick="triggerNearMe()" title="იპოვე უახლოესი ობიექტები">
        📍 ჩემთან ახლოს
      </button>

      <!-- Near Me Status Bar -->
      <div id="near-me-status-bar" class="near-me-status-bar">
        <div class="nms-top">
          <span id="nms-text">📍 ლოკაცია ნაპოვნია</span>
          <button class="nms-reset" onclick="resetNearMe()">ყველას ჩვენება</button>
        </div>
        <div class="radius-selector">
          <span id="radius-label">რადიუსი:</span>
          <select id="radius-select" onchange="changeRadius(this.value)">
            <option value="2">2 კმ</option>
            <option value="5" selected>5 კმ</option>
            <option value="10">10 კმ</option>
            <option value="all">მთელი თბილისი</option>
          </select>
        </div>
      </div>

      <div class="cat-pills">
        <button class="cat-pill active" onclick="setCategory('all')" data-cat="all">🗺 ყველა</button>
        <button class="cat-pill" onclick="setCategory('fresh_milk')" data-cat="fresh_milk">🥛 ცოცხალი & ბიო რძე</button>
        <button class="cat-pill" onclick="setCategory('matsoni_cream')" data-cat="matsoni_cream">🥣 მაწონი, არაჟანი & ხაჭო</button>
        <button class="cat-pill" onclick="setCategory('cheese_artisan')" data-cat="cheese_artisan">🧀 ხელნაკეთი ყველი</button>
        <button class="cat-pill" onclick="setCategory('delivery_coop')" data-cat="delivery_coop">🚚 რძის მიტანა</button>
      </div>
    </div>
    <div id="farm-list"></div>
    <div id="no-results">შესაბამისი რძის ობიექტი ვერ მოიძებნა.</div>
  </div>

  <div id="map"></div>
</div>

<button class="mobile-toggle-btn" id="mobile-toggle" onclick="toggleMobileView()">📋 სიის ნახვა</button>

<!-- Welcome Modal -->
<div id="welcome-modal" class="modal-overlay">
  <div class="modal-card">
    <div class="modal-icon">🥛</div>
    <h2 class="modal-title" id="modal-title">ეს არის თბილისის ნატურალური რძის რუკა</h2>
    <p class="modal-desc" id="modal-desc">
      აღმოაჩინეთ მაღალი ხარისხის, ნამდვილი და შემოწმებული რძის პროდუქტების მაღაზიები, ფერმერული დახლები და მიტანის წერტილები თბილისის ყველა უბანში (საბურთალო, ვაკე, ვერა, დიღომი, გლდანი, ისანი, ვარკეთილი და სხვა).
    </p>
    <button class="modal-btn" id="modal-btn" onclick="closeWelcomeModal()">გასაგებია, რუკის გახსნა</button>
  </div>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const GEOJSON = {geojson_str};
const DISTRICT_GROUPS = {district_groups_json};

let currentLang = 'ka';
let currentCategory = 'all';
let currentDistrict = 'all';
let currentSearch = '';
let currentRadius = 5; // default 5 km
let userCoords = null; // {{ lat, lon, address }}
let userMarker = null;
let userRadiusCircle = null;
let isNearMeActive = false;

const I18N = {{
  en: {{
    header_title: "🥛 Tbilisi Real Dairy Directory",
    header_sub: "Verified Real Shops & Delivery across all Tbilisi Districts • Raw Milk, Bio Milk, Curd, Matsoni, Sour Cream",
    stat_label: "spots",
    search_placeholder: "Search: milk, matsoni, cottage cheese, sour cream...",
    all_districts: "All Tbilisi Districts",
    all_cats: "🗺 All",
    fresh_milk: "🥛 Milk & Bio Milk",
    matsoni_cream: "🥣 Matsoni & Cream",
    cheese_artisan: "🧀 Artisanal Cheese",
    delivery_coop: "🚚 Dairy Delivery",
    no_results: "No verified dairy producers match your search criteria.",
    call: "Call / WhatsApp",
    website: "Website / Page",
    verified_badge: "Verified Real Existence",
    gmaps_btn: "📍 View on Google Maps",
    google_roadmap: "Google Roadmap",
    google_satellite: "Google Satellite",
    toggle_list: "📋 List View",
    toggle_map: "🗺️ Map View",
    near_me: "📍 Near Me",
    near_me_locating: "📍 Locating...",
    radius_label: "Radius:",
    radius_2: "2 km",
    radius_5: "5 km",
    radius_10: "10 km",
    radius_all: "All Tbilisi",
    reset_filter: "Show All",
    loc_found: "📍 Location detected",
    your_location: "📍 Your Location",
    modal_title: "This is the Tbilisi Real Dairy Map",
    modal_desc: "Discover verified high-quality dairy shops, farm creameries, artisanal cheese cellars, and fresh milk delivery services across all Tbilisi districts (Saburtalo, Vake, Vera, Dighomi, Gldani, Isani, Varketili, etc.).",
    modal_btn: "Explore the Map"
  }},
  ka: {{
    header_title: "🥛 Tbilisi Real Dairy Directory",
    header_sub: "Verified Real Shops & Delivery across all Tbilisi Districts • Raw Milk, Bio Milk, Curd, Matsoni, Sour Cream",
    stat_label: "ობიექტი",
    search_placeholder: "ძიება: რძე, მაწონი, ხაჭო, არაჟანი, ყველი...",
    all_districts: "მთელი თბილისი",
    all_cats: "🗺 ყველა",
    fresh_milk: "🥛 ცოცხალი & ბიო რძე",
    matsoni_cream: "🥣 მაწონი, არაჟანი & ხაჭო",
    cheese_artisan: "🧀 ხელნაკეთი ყველი",
    delivery_coop: "🚚 რძის მიტანა",
    no_results: "მითითებული ფილტრებით რძის ობიექტი ვერ მოიძებნა.",
    call: "დარეკვა / WhatsApp",
    website: "ვებ-გვერდი / ბმული",
    verified_badge: "ნამდვილი შემოწმებული ობიექტი",
    gmaps_btn: "📍 ნახე Google Maps-ზე",
    google_roadmap: "Google რუკა",
    google_satellite: "Google თანამგზავრი",
    toggle_list: "📋 სიის ნახვა",
    toggle_map: "🗺️ რუკის ნახვა",
    near_me: "📍 ჩემთან ახლოს",
    near_me_locating: "📍 ძიება...",
    radius_label: "რადიუსი:",
    radius_2: "2 კმ",
    radius_5: "5 კმ",
    radius_10: "10 კმ",
    radius_all: "მთელი თბილისი",
    reset_filter: "ყველას ჩვენება",
    loc_found: "📍 ლოკაცია ნაპოვნია",
    your_location: "📍 თქვენი ლოკაცია",
    modal_title: "ეს არის თბილისის ნატურალური რძის რუკა",
    modal_desc: "აღმოაჩინეთ მაღალი ხარისხის, ნამდვილი და შემოწმებული რძის პროდუქტების მაღაზიები, ფერმერული დახლები და მიტანის წერტილები თბილისის ყველა უბანში (საბურთალო, ვაკე, ვერა, დიღომი, გლდანი, ისანი, ვარკეთილი და სხვა).",
    modal_btn: "გასაგებია, რუკის გახსნა"
  }}
}};

function closeWelcomeModal() {{
  const modal = document.getElementById('welcome-modal');
  if (modal) {{
    modal.classList.add('hidden');
    setTimeout(() => modal.remove(), 350);
  }}
}}

// ── Map Init (Centered on Tbilisi) ──────────────────────────────────
const map = L.map('map', {{
  center: [41.7200, 44.7800],
  zoom: 12,
  zoomControl: true
}});

function getGoogleTileUrl(layerType, lang) {{
  return `https://mt{{s}}.google.com/vt/lyrs=${{layerType}}&hl=${{lang}}&x={{x}}&y={{y}}&z={{z}}`;
}}

let roadLayer = L.tileLayer(getGoogleTileUrl('m', currentLang), {{
  maxZoom: 20,
  subdomains: ['0', '1', '2', '3'],
  attribution: '&copy; Google Maps'
}}).addTo(map);

let satLayer = L.tileLayer(getGoogleTileUrl('y', currentLang), {{
  maxZoom: 20,
  subdomains: ['0', '1', '2', '3'],
  attribution: '&copy; Google Maps'
}});

const baseLayers = {{
  [I18N[currentLang].google_roadmap]: roadLayer,
  [I18N[currentLang].google_satellite]: satLayer
}};
const layerControl = L.control.layers(baseLayers, null, {{ position: 'topright' }}).addTo(map);

function updateLayerLabels() {{
  layerControl.remove();
  roadLayer.setUrl(getGoogleTileUrl('m', currentLang));
  satLayer.setUrl(getGoogleTileUrl('y', currentLang));
  const newBase = {{
    [I18N[currentLang].google_roadmap]: roadLayer,
    [I18N[currentLang].google_satellite]: satLayer
  }};
  layerControl = L.control.layers(newBase, null, {{ position: 'topright' }}).addTo(map);
}}

function makeIcon(color, emoji) {{
  return L.divIcon({{
    className: 'custom-pin',
    html: `<div style="
      background-color: ${{color}};
      width: 32px; height: 32px;
      border-radius: 50% 50% 50% 0;
      transform: rotate(-45deg);
      border: 2px solid white;
      box-shadow: 0 2px 5px rgba(0,0,0,0.3);
      display: flex; align-items: center; justify-content: center;
    "><span style="transform: rotate(45deg); font-size: 15px;">${{emoji}}</span></div>`,
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32]
  }});
}}

function getWhatsAppUrl(phone) {{
  if (!phone) return '#';
  const cleanDigits = phone.replace(/[^0-9]/g, '');
  let intlDigits = cleanDigits;
  if (!intlDigits.startsWith('995') && intlDigits.length === 9) {{
    intlDigits = '995' + intlDigits;
  }}
  return `https://wa.me/${{intlDigits}}`;
}}

function getDistanceKm(lat1, lon1, lat2, lon2) {{
  const R = 6371;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}}

function calculateTravelTimes(distanceKm) {{
  const driveMinutes = Math.round((distanceKm / 30) * 60);
  const walkMinutes = Math.round((distanceKm / 4.5) * 60);
  return {{
    driveMinutes: Math.max(1, driveMinutes),
    walkMinutes: Math.max(1, walkMinutes)
  }};
}}

function formatMinutes(minutes, lang) {{
  if (lang === 'ka') {{
    if (minutes < 60) return `${{minutes}} წთ`;
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    return m > 0 ? `${{h}} სთ ${{m}} წთ` : `${{h}} სთ`;
  }} else {{
    if (minutes < 60) return `${{minutes}} min`;
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    return m > 0 ? `${{h}} hr ${{m}} min` : `${{h}} hr`;
  }}
}}

function createUserPulseMarker(lat, lon, addressText) {{
  const pulseIcon = L.divIcon({{
    className: 'user-location-pulse-wrapper',
    html: `
      <div class="user-pulse-center">
        <div class="user-pulse-ring"></div>
        <div class="user-pulse-dot"></div>
      </div>
    `,
    iconSize: [36, 36],
    iconAnchor: [18, 18],
    popupAnchor: [0, -18]
  }});

  const marker = L.marker([lat, lon], {{ icon: pulseIcon, zIndexOffset: 2000 }});
  const addrLabel = addressText || (currentLang === 'ka' ? 'მიმდინარე GPS ლოკაცია' : 'Current GPS Location');
  const popupHtml = `
    <div class="user-popup">
      <div class="user-popup-title">${{I18N[currentLang].your_location}}</div>
      <div class="user-popup-coords"><code>${{lat.toFixed(4)}}° N, ${{lon.toFixed(4)}}° E</code></div>
      <div id="user-popup-address" class="user-popup-address">${{addrLabel}}</div>
    </div>
  `;
  marker.bindPopup(popupHtml, {{ maxWidth: getPopupMaxWidth() }});
  return marker;
}}

function updateUserRadiusCircle(lat, lon, radius) {{
  if (userRadiusCircle && map.hasLayer(userRadiusCircle)) {{
    map.removeLayer(userRadiusCircle);
    userRadiusCircle = null;
  }}
  if (radius === 'all') return;
  userRadiusCircle = L.circle([lat, lon], {{
    radius: radius * 1000,
    color: '#0284c7',
    fillColor: '#38bdf8',
    fillOpacity: 0.12,
    weight: 1.5,
    dashArray: '4, 4'
  }}).addTo(map);
}}

function triggerNearMe() {{
  const btn = document.getElementById('near-me-btn');
  btn.textContent = I18N[currentLang].near_me_locating;
  btn.disabled = true;

  if (!navigator.geolocation) {{
    alert(currentLang === 'ka' ? 'გეოლოკაცია არ არის მხარდაჭერილი თქვენს ბრაუზერში.' : 'Geolocation is not supported by your browser.');
    btn.textContent = I18N[currentLang].near_me;
    btn.disabled = false;
    return;
  }}

  navigator.geolocation.getCurrentPosition(
    position => {{
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;
      userCoords = {{ lat, lon, address: '' }};
      isNearMeActive = true;

      if (userMarker && map.hasLayer(userMarker)) {{
        map.removeLayer(userMarker);
      }}

      userMarker = createUserPulseMarker(lat, lon, '');
      userMarker.addTo(map);

      updateUserRadiusCircle(lat, lon, currentRadius);

      document.getElementById('near-me-status-bar').classList.add('visible');
      btn.classList.add('active');
      btn.textContent = I18N[currentLang].near_me;
      btn.disabled = false;

      map.flyTo([lat, lon], 13, {{ animate: true, duration: 1.0 }});

      render();
      updateAllMarkersPopups();
    }},
    err => {{
      console.warn("Geolocation error:", err);
      // Fallback: Tbilisi Center (Rustaveli / Liberty Square)
      const fallbackLat = 41.6965;
      const fallbackLon = 44.7990;
      userCoords = {{ lat: fallbackLat, lon: fallbackLon, address: (currentLang === 'ka' ? 'თბილისის ცენტრი (ნაგულისხმევი)' : 'Tbilisi Center (Default)') }};
      isNearMeActive = true;

      if (userMarker && map.hasLayer(userMarker)) map.removeLayer(userMarker);
      userMarker = createUserPulseMarker(fallbackLat, fallbackLon, userCoords.address);
      userMarker.addTo(map);
      updateUserRadiusCircle(fallbackLat, fallbackLon, currentRadius);

      document.getElementById('near-me-status-bar').classList.add('visible');
      btn.classList.add('active');
      btn.textContent = I18N[currentLang].near_me;
      btn.disabled = false;

      map.flyTo([fallbackLat, fallbackLon], 13, {{ animate: true, duration: 1.0 }});

      render();
      updateAllMarkersPopups();
    }},
    {{ timeout: 7000, maximumAge: 60000 }}
  );
}}

function resetNearMe() {{
  isNearMeActive = false;
  userCoords = null;
  if (userMarker && map.hasLayer(userMarker)) map.removeLayer(userMarker);
  if (userRadiusCircle && map.hasLayer(userRadiusCircle)) map.removeLayer(userRadiusCircle);
  userMarker = null;
  userRadiusCircle = null;

  document.getElementById('near-me-status-bar').classList.remove('visible');
  document.getElementById('near-me-btn').classList.remove('active');

  render();
  updateAllMarkersPopups();
  map.flyTo([41.7200, 44.7800], 12);
}}

function changeRadius(val) {{
  currentRadius = (val === 'all' ? 'all' : parseFloat(val));
  if (userCoords && isNearMeActive) {{
    updateUserRadiusCircle(userCoords.lat, userCoords.lon, currentRadius);
  }}
  render();
}}

function buildPopupHtml(p, lang, lat, lon) {{
  const isKa = (lang === 'ka');
  const nameMain = isKa ? p.name_ka : p.name_en;
  const nameSec = isKa ? p.name_en : p.name_ka;
  const catLabel = isKa ? p.cat_label_ka : p.cat_label_en;
  const subName = isKa ? (p.sub_district || p.district) : (p.sub_district || p.district);
  const addr = isKa ? (p.address_ka || p.address) : p.address;
  const desc = isKa ? (p.description_ka || p.description) : p.description;
  const prodsList = isKa ? (p.products_ka || p.products) : p.products;
  const prods = (prodsList || []).map(t => `<span class="tag">${{t}}</span>`).join('');

  let phoneHtml = '';
  if (p.phone) {{
    const waUrl = getWhatsAppUrl(p.phone);
    phoneHtml = `<p class="popup-phone">📞 <a href="${{waUrl}}" target="_blank" rel="noopener noreferrer" title="WhatsApp">${{p.phone}}</a></p>`;
  }}

  let distHtml = '';
  if (userCoords && lat !== undefined && lon !== undefined) {{
    const d = getDistanceKm(userCoords.lat, userCoords.lon, lat, lon);
    const times = calculateTravelTimes(d);
    const driveStr = formatMinutes(times.driveMinutes, lang);
    const walkStr = formatMinutes(times.walkMinutes, lang);
    const dUnit = (lang === 'ka' ? 'კმ' : 'km');
    distHtml = `
      <div class="popup-distance-bar">
        <span class="dist-badge dist-km">📏 ${{d.toFixed(1)}} ${{dUnit}}</span>
        <span class="dist-badge dist-drive">🚗 ${{driveStr}}</span>
        <span class="dist-badge dist-walk">🚶 ${{walkStr}}</span>
      </div>
    `;
  }}

  let gmapsHtml = '';
  if (p.google_maps_url) {{
    gmapsHtml = `<div class="popup-gmaps"><a href="${{p.google_maps_url}}" target="_blank" rel="noopener" class="gmaps-btn">${{I18N[lang].gmaps_btn}}</a></div>`;
  }}

  return `
    <div class="popup-card">
      <div class="popup-cat" style="background:${{p.color}}">${{p.emoji}} ${{catLabel}}</div>
      <h3>${{nameMain}}</h3>
      <div class="popup-sec">${{nameSec}}</div>
      <p class="popup-addr">📍 <strong>${{subName}}</strong>: ${{addr}}</p>
      ${{phoneHtml}}
      ${{distHtml}}
      <div class="popup-tags">${{prods}}</div>
      <p class="popup-desc">${{desc}}</p>
      ${{gmapsHtml}}
      <p class="popup-notes"><em>✅ ${{I18N[lang].verified_badge}} [${{p.source}}]</em></p>
    </div>
  `;
}}

const getPopupMaxWidth = () => (window.innerWidth <= 768 ? 260 : 300);
let markers = [];
GEOJSON.features.forEach(f => {{
  const p = f.properties;
  const [lon, lat] = f.geometry.coordinates;
  const marker = L.marker([lat, lon], {{ icon: makeIcon(p.color, p.emoji) }})
    .bindPopup(buildPopupHtml(p, currentLang, lat, lon), {{ maxWidth: getPopupMaxWidth() }});
  marker.featureProps = p;
  marker.coords = [lat, lon];
  marker.addTo(map);
  markers.push(marker);
}});

function updateAllMarkersPopups() {{
  markers.forEach(m => {{
    const wasOpen = m.isPopupOpen();
    m.bindPopup(buildPopupHtml(m.featureProps, currentLang, m.coords[0], m.coords[1]), {{ maxWidth: getPopupMaxWidth() }});
    if (wasOpen) m.openPopup();
  }});
}}

function buildSidebar(features, lang) {{
  const isKa = (lang === 'ka');
  const list = document.getElementById('farm-list');
  const noRes = document.getElementById('no-results');
  list.innerHTML = '';
  document.getElementById('stat-total').textContent = features.length;

  if (features.length === 0) {{
    noRes.style.display = 'block';
    return;
  }}
  noRes.style.display = 'none';

  features.forEach(f => {{
    const p = f.properties;
    const [lon, lat] = f.geometry.coordinates;
    const nameMain = isKa ? p.name_ka : p.name_en;
    const nameSec = isKa ? p.name_en : p.name_ka;
    const catLabel = isKa ? p.cat_label_ka : p.cat_label_en;
    const subName = isKa ? (p.sub_district || p.district) : (p.sub_district || p.district);
    const addr = isKa ? (p.address_ka || p.address) : p.address;
    const prodsList = isKa ? (p.products_ka || p.products) : p.products;
    const tags = (prodsList || []).slice(0, 4).map(t => `<span class="tag">${{t}}</span>`).join('');

    let distCardHtml = '';
    if (userCoords) {{
      const d = getDistanceKm(userCoords.lat, userCoords.lon, lat, lon);
      const times = calculateTravelTimes(d);
      const driveStr = formatMinutes(times.driveMinutes, lang);
      const walkStr = formatMinutes(times.walkMinutes, lang);
      const dUnit = (lang === 'ka' ? 'კმ' : 'km');
      distCardHtml = `
        <div class="fc-distance-bar">
          <span class="dist-badge dist-km">📏 ${{d.toFixed(1)}} ${{dUnit}}</span>
          <span class="dist-badge dist-drive">🚗 ${{driveStr}}</span>
          <span class="dist-badge dist-walk">🚶 ${{walkStr}}</span>
        </div>
      `;
    }}

    let waCardHtml = '';
    if (p.phone) {{
      const waUrl = getWhatsAppUrl(p.phone);
      waCardHtml = `<div class="fc-phone">📞 <a href="${{waUrl}}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();" title="WhatsApp">${{p.phone}}</a></div>`;
    }}

    let gmapsCardHtml = '';
    if (p.google_maps_url) {{
      gmapsCardHtml = `<div class="fc-gmaps"><a href="${{p.google_maps_url}}" target="_blank" rel="noopener" class="gmaps-link" onclick="event.stopPropagation();">${{I18N[lang].gmaps_btn}}</a></div>`;
    }}

    const card = document.createElement('div');
    card.className = 'farm-card';
    card.innerHTML = `
      <span class="fc-cat" style="background:${{p.color}}">${{p.emoji}} ${{catLabel}}</span>
      <div class="fc-name">${{nameMain}}</div>
      <div class="fc-name-sec">${{nameSec}}</div>
      <div class="fc-loc">📍 <strong>${{subName}}</strong> • ${{addr.split(',')[0]}}</div>
      <div class="fc-tags">${{tags}}</div>
      ${{distCardHtml}}
      ${{waCardHtml}}
      ${{gmapsCardHtml}}
      <div class="fc-source">✅ ${{I18N[lang].verified_badge}} [${{p.source}}]</div>
    `;

    card.addEventListener('click', () => {{
      document.querySelectorAll('.farm-card').forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      map.flyTo([lat, lon], 16, {{ animate: true, duration: 0.8 }});
      const m = markers.find(mk => mk.coords[0] === lat && mk.coords[1] === lon);
      if (m) m.openPopup();
      if (window.innerWidth <= 768) {{
        toggleMobileView();
      }}
    }});

    list.appendChild(card);
  }});
}}

function populateDistrictSelect(lang) {{
  const isKa = (lang === 'ka');
  const sel = document.getElementById('district-select');
  sel.innerHTML = '';
  DISTRICT_GROUPS.forEach(dg => {{
    const opt = document.createElement('option');
    opt.value = dg.id;
    opt.textContent = isKa ? dg.label_ka : dg.label_en;
    if (dg.id === currentDistrict) opt.selected = true;
    sel.appendChild(opt);
  }});
}}

function render() {{
  const query = currentSearch.toLowerCase().trim();

  let filtered = GEOJSON.features.filter(f => {{
    const p = f.properties;
    const [lon, lat] = f.geometry.coordinates;

    // Category filter
    if (currentCategory !== 'all' && p.category !== currentCategory) return false;

    // District filter
    if (currentDistrict !== 'all') {{
      const dGroup = p.district_group || 'all';
      if (dGroup !== currentDistrict) return false;
    }}

    // Text search filter
    if (query) {{
      const haystack = [
        p.name_en, p.name_ka,
        p.sub_district, p.district,
        p.address, p.address_ka,
        p.description, p.description_ka,
        (p.products || []).join(' '),
        (p.products_ka || []).join(' ')
      ].join(' ').toLowerCase();
      if (!haystack.includes(query)) return false;
    }}

    // Radius filter (if Near Me active)
    if (isNearMeActive && userCoords && currentRadius !== 'all') {{
      const d = getDistanceKm(userCoords.lat, userCoords.lon, lat, lon);
      if (d > currentRadius) return false;
    }}

    return true;
  }});

  // Sort by distance if Near Me active
  if (isNearMeActive && userCoords) {{
    filtered.sort((a, b) => {{
      const dA = getDistanceKm(userCoords.lat, userCoords.lon, a.geometry.coordinates[1], a.geometry.coordinates[0]);
      const dB = getDistanceKm(userCoords.lat, userCoords.lon, b.geometry.coordinates[1], b.geometry.coordinates[0]);
      return dA - dB;
    }});
  }}

  // Update map markers visibility
  const visibleCoords = new Set(filtered.map(f => `${{f.geometry.coordinates[1]}},${{f.geometry.coordinates[0]}}`));
  markers.forEach(m => {{
    const key = `${{m.coords[0]}},${{m.coords[1]}}`;
    if (visibleCoords.has(key)) {{
      if (!map.hasLayer(m)) m.addTo(map);
    }} else {{
      if (map.hasLayer(m)) map.removeLayer(m);
    }}
  }});

  buildSidebar(filtered, currentLang);
}}

function onSearchInput() {{
  currentSearch = document.getElementById('search-input').value;
  render();
}}

function onDistrictChange() {{
  currentDistrict = document.getElementById('district-select').value;
  render();
}}

function setCategory(cat) {{
  currentCategory = cat;
  document.querySelectorAll('.cat-pill').forEach(btn => {{
    btn.classList.toggle('active', btn.dataset.cat === cat);
  }});
  render();
}}

function toggleLang() {{
  currentLang = (currentLang === 'ka' ? 'en' : 'ka');
  const t = I18N[currentLang];

  document.getElementById('lang-btn').textContent = (currentLang === 'ka' ? 'English' : 'ქართული');
  document.getElementById('stat-label').textContent = t.stat_label;
  document.getElementById('search-input').placeholder = t.search_placeholder;
  document.getElementById('near-me-btn').textContent = t.near_me;
  document.getElementById('nms-text').textContent = t.loc_found;
  document.getElementById('radius-label').textContent = t.radius_label;
  document.querySelector('.nms-reset').textContent = t.reset_filter;

  populateDistrictSelect(currentLang);
  updateLayerLabels();
  updateAllMarkersPopups();
  render();
}}

let mobileSidebarActive = false;
function toggleMobileView() {{
  mobileSidebarActive = !mobileSidebarActive;
  const sb = document.getElementById('sidebar');
  const btn = document.getElementById('mobile-toggle');
  sb.classList.toggle('mobile-active', mobileSidebarActive);
  btn.textContent = mobileSidebarActive ? I18N[currentLang].toggle_map : I18N[currentLang].toggle_list;
}}

// Initialize
populateDistrictSelect(currentLang);
render();
</script>
</body>
</html>
"""

def main():
    print(f"Loading verified Tbilisi dairy spots from {DATA_PATH}...")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        spots = json.load(f)

    features = []
    for s in spots:
        cat = s.get("category", "fresh_milk")
        meta = CAT_META.get(cat, CAT_META["fresh_milk"])
        d_group = map_district_group(s.get("sub_district") or s.get("district"))
        
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(s["lon"]), float(s["lat"])]
            },
            "properties": {
                "id": s["id"],
                "name_en": s["name_en"],
                "name_ka": s["name_ka"],
                "category": cat,
                "color": meta["color"],
                "emoji": meta["emoji"],
                "cat_label_en": meta["label_en"],
                "cat_label_ka": meta["label_ka"],
                "district": s.get("district", "Tbilisi"),
                "sub_district": s.get("sub_district", s.get("district", "Tbilisi")),
                "district_group": d_group,
                "address": s.get("address", ""),
                "address_ka": s.get("address_ka", s.get("address", "")),
                "phone": s.get("phone", ""),
                "google_maps_url": s.get("google_maps_url", f"https://www.google.com/maps/search/?api=1&query={s['lat']:.5f},{s['lon']:.5f}"),
                "website": s.get("website_or_social", ""),
                "description": s.get("description", ""),
                "description_ka": s.get("description_ka", s.get("description", "")),
                "products": s.get("products", []),
                "products_ka": s.get("products_ka", s.get("products", [])),
                "source": s.get("verification_source", "Verified Registry")
            }
        }
        features.append(feature)

    print(f"Generated {len(features)} GeoJSON features for Tbilisi.")
    html_content = render_html(features)

    # Save to tbilisi_dairy_map.html
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Generated {OUTPUT_PATH}")

    # Save to index.html as current live app
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Updated {INDEX_PATH}")

if __name__ == "__main__":
    main()
