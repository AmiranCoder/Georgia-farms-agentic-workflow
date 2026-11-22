#!/usr/bin/env python3
"""
execution/publish_saburtalo.py
Map Publisher — Saburtalo Real Verified Dairy Directory (Leaflet + Google Roadmap/Satellite Layers)
"""

import json
import os

VERIFIED_PATH = os.path.join(os.path.dirname(__file__), "..", "output", "saburtalo_farms.json")
OUTPUT_POC_PATH = os.path.join(os.path.dirname(__file__), "..", "output", "saburtalo_poc.html")
OUTPUT_INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "output", "index.html")

SABURTALO_BOUNDS = {
    "lat_min": 41.7050,
    "lat_max": 41.7550,
    "lon_min": 44.7000,
    "lon_max": 44.7900
}

# High-Precision Gazetteer for Real Verified Saburtalo Dairy Spots
SABURTALO_GAZETTEER = {
    "71 Vazha-Pshavela Ave (BCB Courtyard), Saburtalo, Tbilisi":            (41.7225, 44.7310), # Milk Laboratory
    "87 Vazha-Pshavela Ave, Saburtalo, Tbilisi":                            (41.7212, 44.7262), # Cheese House Abasha
    "41 Al. Kazbegi Ave, Saburtalo, Tbilisi":                               (41.7242, 44.7525), # Monastery Dairy Products
    "Intersection of Vazha-Pshavela Ave & Asatiani St, Saburtalo, Tbilisi": (41.7260, 44.7470), # Dedoplistskaro Dairy
    "15 Al. Kazbegi Ave (m² Complex), Saburtalo, Tbilisi":                  (41.7280, 44.7615), # Tserti Kazbegi
    "2 Davit Gamrekeli St, Saburtalo, Tbilisi":                             (41.7265, 44.7680), # Tserti Gamrekeli
    "10 Viktor Dolidze St, Saburtalo, Tbilisi":                             (41.7185, 44.7780), # Georgian Basket Aristeus
    "13 Bakhtrioni St, Saburtalo, Tbilisi":                                 (41.7222, 44.7675), # Beka's Nobati Bakhtrioni
    "34 Viktor Dolidze St, Saburtalo, Tbilisi":                             (41.7198, 44.7745), # Beka's Nobati Dolidze
    "Nutsubidze Plateau 4th Micro-district, Bldg 5, Saburtalo, Tbilisi":    (41.7160, 44.7210), # Vazi & Baraka Dairy Point
    "77 Nutsubidze St, Saburtalo, Tbilisi":                                 (41.7205, 44.7440), # Nutsubidze Village Dairy Pavilion
    "3 Tamarashvili St (at Delisi Metro Exit), Saburtalo, Tbilisi":          (41.7258, 44.7488), # Delisi Metro Dairy Kiosk
    "4 Lisi Lake Road, Saburtalo, Tbilisi":                                 (41.7450, 44.7350), # Lisi Lake Organic Dairy Pavilion
    "Tsodoreti Road (Lisi Heights Area), Saburtalo, Tbilisi":                (41.7485, 44.7180), # Tsodoreti Ridge Dairy Gate
    "12 Bakhtrioni St Hub, Saburtalo, Tbilisi":                             (41.7220, 44.7680), # Aria Farm Delivery Hub
    "15 Al. Kazbegi Ave Hub, Saburtalo, Tbilisi":                           (41.7282, 44.7610), # Tserti Courier Hub
    "18 Kavtaradze St, Saburtalo, Tbilisi":                                 (41.7225, 44.7360), # Vazha & Nutsubidze Dispatch
}

CATEGORY_STYLES = {
    "fresh_milk":    {"color": "#0284c7", "emoji": "🥛", "label_en": "Milk & Bio Milk",       "label_ka": "ცოცხალი & ბიო რძე"},
    "matsoni_cream": {"color": "#059669", "emoji": "🥣", "label_en": "Matsoni, Cream & Curd", "label_ka": "მაწონი, არაჟანი & ხაჭო"},
    "cheese_artisan":{"color": "#d97706", "emoji": "🧀", "label_en": "Artisanal Cheese",      "label_ka": "ხელნაკეთი ყველი"},
    "delivery_coop": {"color": "#7c3aed", "emoji": "🚚", "label_en": "Dairy Delivery Co-op",  "label_ka": "რძის პროდუქტების მიტანა"},
}

SUB_DISTRICT_NAMES = {
    "Pekini / Kostava": {"en": "Pekini / Kostava", "ka": "პეკინი / კოსტავა"},
    "Vazha-Pshavela":   {"en": "Vazha-Pshavela",   "ka": "ვაჟა-ფშაველა"},
    "Nutsubidze":       {"en": "Nutsubidze",       "ka": "ნუცუბიძე"},
    "Kazbegi / Delisi": {"en": "Kazbegi / Delisi", "ka": "ყაზბეგი / დელისი"},
    "Lisi":             {"en": "Lisi",             "ka": "ლისი"},
}

DAIRY_QUICK_FILTERS = [
    {"id": "all", "label_en": "All Dairy", "label_ka": "ყველა რძის ნაწარმი", "icon": "🥛"},
    {"id": "milk", "label_en": "Milk / Bio Milk", "label_ka": "ცოცხალი & ბიო რძე", "icon": "🥛", "terms": ["milk", "რძე", "bio milk", "ბიო რძე", "raw milk", "ნედლი რძე"]},
    {"id": "cottage_cheese", "label_en": "Cottage Cheese", "label_ka": "ხაჭო", "icon": "🥣", "terms": ["cottage cheese", "ხაჭო", "curd"]},
    {"id": "matsoni", "label_en": "Matsoni", "label_ka": "მაწონი", "icon": "🏺", "terms": ["matsoni", "მაწონი"]},
    {"id": "sour_cream", "label_en": "Sour Cream", "label_ka": "არაჟანი", "icon": "🍶", "terms": ["sour cream", "არაჟანი", "cream"]},
    {"id": "cheese", "label_en": "Cheese / Sulguni", "label_ka": "ყველი / სულგუნი", "icon": "🧀", "terms": ["cheese", "ყველი", "sulguni", "სულგუნი", "guda", "გუდა", "tenili", "თენილი"]},
]

def geocode(addr):
    if addr in SABURTALO_GAZETTEER:
        return SABURTALO_GAZETTEER[addr]
    for key, coords in SABURTALO_GAZETTEER.items():
        if addr.lower()[:15] in key.lower():
            return coords
    return None

def passes_bbox(lat, lon):
    return (SABURTALO_BOUNDS["lat_min"] <= lat <= SABURTALO_BOUNDS["lat_max"] and
            SABURTALO_BOUNDS["lon_min"] <= lon <= SABURTALO_BOUNDS["lon_max"])

def build_features(farms):
    features = []
    passed = 0
    for farm in farms:
        coords = geocode(farm["address"])
        if not coords:
            raise ValueError(f"Missing coords in gazetteer for {farm['address']}")
        lat, lon = coords
        if not passes_bbox(lat, lon):
            raise ValueError(f"Coordinates ({lat}, {lon}) outside Saburtalo BBox for {farm['name_en']}")

        passed += 1
        fid = farm["id"]
        gmaps_url = f"https://www.google.com/maps/search/?api=1&query={lat:.5f},{lon:.5f}"
        farm["lat"] = lat
        farm["lon"] = lon
        farm["coordinates"] = {"lat": lat, "lon": lon}
        farm["google_maps_url"] = gmaps_url

        style = CATEGORY_STYLES.get(farm["category"], CATEGORY_STYLES["fresh_milk"])
        sub_info = SUB_DISTRICT_NAMES.get(farm["sub_district"], {"en": farm["sub_district"], "ka": farm["sub_district"]})

        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {
                "id": fid,
                "name_en": farm["name_en"],
                "name_ka": farm.get("name_ka") or farm["name_en"],
                "sub_district": farm["sub_district"],
                "sub_district_en": sub_info["en"],
                "sub_district_ka": sub_info["ka"],
                "region": farm.get("region", "Tbilisi"),
                "category": farm["category"],
                "cat_label_en": style["label_en"],
                "cat_label_ka": style["label_ka"],
                "color": style["color"],
                "emoji": style["emoji"],
                "address_en": farm["address"],
                "address_ka": farm.get("address_ka", farm["address"]),
                "phone": farm.get("phone", ""),
                "website": farm.get("website_or_social", ""),
                "google_maps_url": gmaps_url,
                "products_en": farm.get("products", []),
                "products_ka": farm.get("products_ka", farm.get("products", [])),
                "desc_en": farm.get("description", ""),
                "desc_ka": farm.get("description_ka", farm.get("description", "")),
                "notes": farm.get("reflection_notes", ""),
                "source": farm.get("verification_source", "Verified")
            }
        })

    print(f"✅ Saburtalo Real Dairy Features: {passed} passed strict bounding box.")
    return features

def render_html(features):
    geojson_str = json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False, indent=2)
    sub_districts_json = json.dumps(SUB_DISTRICT_NAMES, ensure_ascii=False)
    cat_styles_json = json.dumps(CATEGORY_STYLES, ensure_ascii=False)
    dairy_filters_json = json.dumps(DAIRY_QUICK_FILTERS, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="ka">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>🥛 Saburtalo Real Dairy Directory | საბურთალოს ნამდვილი რძის ობიექტების რუკა</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; display: flex; flex-direction: column; height: 100vh; overflow: hidden; color: #202124; }}

  /* Zero-seam Leaflet tile rendering */
  .leaflet-container {{ background: #e8eaed !important; }}
  .leaflet-tile {{
    outline: 1px solid transparent;
    transform-origin: 0 0;
    -webkit-backface-visibility: hidden;
    backface-visibility: hidden;
  }}
  .leaflet-tile-loaded {{ box-shadow: 0 0 1px rgba(0, 0, 0, 0.05); }}
  img.leaflet-tile {{
    width: 256px !important;
    height: 256px !important;
    margin: -0.5px;
    padding: 0.5px;
  }}

  /* Header */
  #header {{
    background: linear-gradient(135deg, #0369a1 0%, #0284c7 45%, #059669 100%);
    color: white; padding: 12px 22px;
    display: flex; align-items: center; justify-content: space-between; gap: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.25); z-index: 1000; flex-shrink: 0;
  }}
  .header-left {{ flex: 1; }}
  #header-title {{ font-size: 1.35rem; font-weight: 700; letter-spacing: -0.2px; }}
  #header-title span {{ font-weight: 300; opacity: 0.92; font-size: 1.05rem; }}
  #header-sub {{ font-size: 0.78rem; opacity: 0.9; margin-top: 3px; }}

  .header-right {{ display: flex; align-items: center; gap: 20px; }}
  .stats {{ display: flex; gap: 18px; }}
  .stat {{ text-align: center; }}
  .stat .num {{ font-size: 1.55rem; font-weight: 800; line-height: 1; }}
  .stat .lbl {{ font-size: 0.65rem; opacity: 0.85; text-transform: uppercase; letter-spacing: 0.5px; }}

  /* Language Switcher Pill */
  .lang-switcher {{
    display: flex; align-items: center;
    background: rgba(255, 255, 255, 0.22);
    border: 1.5px solid rgba(255, 255, 255, 0.45);
    border-radius: 24px; padding: 3px; gap: 2px;
  }}
  .lang-btn {{
    border: none; background: transparent; color: white;
    padding: 6px 13px; font-size: 0.82rem; font-weight: 700;
    border-radius: 20px; cursor: pointer; transition: all 0.2s ease;
  }}
  .lang-btn.active {{
    background: white; color: #0369a1;
    box-shadow: 0 2px 6px rgba(0,0,0,0.25);
  }}
  .lang-btn:hover:not(.active) {{ background: rgba(255, 255, 255, 0.15); }}

  /* Layout */
  #main {{ display: flex; flex: 1; overflow: hidden; position: relative; }}

  /* Sidebar */
  #sidebar {{
    width: 410px; min-width: 320px; background: #f8fafc;
    border-right: 1px solid #e2e8f0; display: flex; flex-direction: column;
    overflow: hidden; z-index: 500;
  }}
  #controls {{ padding: 12px; background: white; border-bottom: 1px solid #e2e8f0; }}
  #search {{
    width: 100%; padding: 9px 14px; border: 1.5px solid #cbd5e1; border-radius: 20px;
    font-size: 0.88rem; outline: none; margin-bottom: 9px; transition: border-color 0.2s;
  }}
  #search:focus {{ border-color: #0284c7; box-shadow: 0 0 0 3px rgba(2,132,199,0.15); }}
  
  #subdistrict-select {{
    width: 100%; padding: 8px 12px; border: 1.5px solid #cbd5e1; border-radius: 8px;
    font-size: 0.85rem; margin-bottom: 9px; outline: none; background: white; font-weight: 500;
  }}

  /* Dairy Product Pills */
  .dairy-pill-bar {{
    display: flex; gap: 6px; overflow-x: auto; padding-bottom: 8px; margin-bottom: 8px;
    scrollbar-width: thin;
  }}
  .dairy-pill-bar::-webkit-scrollbar {{ height: 4px; }}
  .dairy-pill-bar::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 4px; }}
  .dairy-pill {{
    display: inline-flex; align-items: center; gap: 4px;
    border: 1.5px solid #cbd5e1; background: #f1f5f9; border-radius: 16px;
    padding: 5px 11px; font-size: 0.74rem; font-weight: 700; cursor: pointer;
    white-space: nowrap; color: #334155; transition: all 0.18s ease;
  }}
  .dairy-pill:hover {{ background: #e2e8f0; border-color: #94a3b8; }}
  .dairy-pill.active {{ background: #0284c7; color: white; border-color: #0284c7; box-shadow: 0 2px 6px rgba(2,132,199,0.3); }}

  /* Category Filter Buttons */
  .cat-filters {{ display: flex; flex-wrap: wrap; gap: 5px; }}
  .cat-btn {{
    border: 1.5px solid #cbd5e1; background: white; border-radius: 14px;
    padding: 4px 9px; font-size: 0.72rem; font-weight: 600; cursor: pointer;
    transition: all 0.15s ease;
  }}
  .cat-btn.active {{ background: #0f172a; color: white !important; border-color: #0f172a !important; }}

  /* Near Me Button in Sidebar Controls */
  .near-me-btn {{
    width: 100%; margin-bottom: 9px;
    display: flex; align-items: center; justify-content: center; gap: 7px;
    background: #ffffff; color: #0284c7; border: 1.5px solid #0284c7; border-radius: 8px;
    padding: 8px 14px; font-size: 0.85rem; font-weight: 700; cursor: pointer; white-space: nowrap;
    box-shadow: 0 1px 3px rgba(2,132,199,0.12); transition: all 0.2s ease;
  }}
  .near-me-btn:hover {{ background: #f0f9ff; border-color: #0369a1; transform: translateY(-1px); box-shadow: 0 3px 8px rgba(2,132,199,0.2); }}
  .near-me-btn.active {{
    background: #0284c7; color: white; border-color: #0369a1;
    box-shadow: 0 2px 6px rgba(2,132,199,0.35);
  }}
  .near-me-btn.locating {{ opacity: 0.85; cursor: wait; background: #fef3c7; color: #92400e; border-color: #fde68a; }}

  /* Near Me Status Bar */
  #near-me-status-bar {{
    background: #f0f9ff; border-left: 4px solid #0284c7; border-bottom: 1px solid #bae6fd;
    padding: 9px 12px; font-size: 0.78rem; color: #0369a1; display: flex; flex-direction: column; gap: 6px;
  }}
  .status-main {{ display: flex; align-items: center; justify-content: space-between; gap: 8px; }}
  .status-text {{ font-weight: 600; line-height: 1.35; }}
  .reset-btn {{
    background: white; color: #0284c7; border: 1px solid #bae6fd; border-radius: 6px;
    padding: 3px 8px; font-size: 0.72rem; font-weight: 700; cursor: pointer; white-space: nowrap;
    transition: all 0.15s ease;
  }}
  .reset-btn:hover {{ background: #e0f2fe; border-color: #7dd3fc; }}
  .status-controls {{ display: flex; align-items: center; gap: 8px; }}
  .radius-select-label {{ font-weight: 600; color: #0369a1; font-size: 0.74rem; }}
  .radius-dropdown {{
    padding: 3px 8px; border: 1px solid #7dd3fc; border-radius: 6px;
    background: white; color: #0369a1; font-size: 0.76rem; font-weight: 600; outline: none;
  }}

  /* Distance Badges */
  .fc-distance-bar, .popup-distance-bar {{
    display: flex; flex-wrap: wrap; align-items: center; gap: 5px;
    margin-top: 8px; padding-top: 7px; border-top: 1px dashed #e2e8f0;
  }}
  .dist-badge {{
    display: inline-flex; align-items: center; gap: 3px;
    padding: 3px 7px; border-radius: 6px; font-size: 0.72rem; font-weight: 600;
  }}
  .dist-km {{ background: #e0f2fe; color: #0369a1; }}
  .dist-drive {{ background: #fef3c7; color: #92400e; }}
  .dist-walk {{ background: #f1f5f9; color: #475569; }}

  /* User Location Pulsing Marker */
  .user-pulse-marker {{ position: relative; width: 24px; height: 24px; }}
  .user-pulse-dot {{
    width: 14px; height: 14px; background: #0284c7; border: 2.5px solid white;
    border-radius: 50%; position: absolute; top: 5px; left: 5px;
    box-shadow: 0 0 8px rgba(2,132,199,0.9); z-index: 2;
  }}
  .user-pulse-ring {{
    position: absolute; width: 34px; height: 34px; top: -5px; left: -5px;
    background: rgba(2, 132, 199, 0.45); border-radius: 50%;
    animation: userPulse 2s infinite ease-out; z-index: 1;
  }}
  @keyframes userPulse {{
    0% {{ transform: scale(0.4); opacity: 1; }}
    100% {{ transform: scale(2.2); opacity: 0; }}
  }}
  .user-popup {{ padding: 4px 2px; font-size: 0.85rem; line-height: 1.4; }}
  .user-popup-title {{ font-weight: 700; color: #0284c7; font-size: 0.95rem; margin-bottom: 4px; }}
  .user-popup-coords {{ color: #64748b; font-size: 0.78rem; margin-bottom: 4px; }}
  .user-popup-address {{ font-size: 0.82rem; color: #334155; font-weight: 500; }}

  /* List & Cards */
  #farm-list {{ flex: 1; overflow-y: auto; padding: 10px; }}
  .farm-card {{
    background: white; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 13px; margin-bottom: 10px; cursor: pointer; transition: all 0.2s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }}
  .farm-card:hover {{ border-color: #0284c7; transform: translateY(-1.5px); box-shadow: 0 4px 12px rgba(2,132,199,0.12); }}
  .fc-cat {{ display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 0.72rem; font-weight: 700; color: white; margin-bottom: 6px; }}
  .fc-name {{ font-size: 0.96rem; font-weight: 700; color: #0f172a; line-height: 1.3; }}
  .fc-name-sec {{ font-size: 0.78rem; color: #64748b; margin-bottom: 5px; }}
  .fc-loc {{ font-size: 0.78rem; color: #334155; margin-bottom: 6px; }}
  .fc-tags {{ display: flex; flex-wrap: wrap; gap: 4px; margin-top: 5px; }}
  .tag {{ background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 4px; padding: 2px 6px; font-size: 0.68rem; color: #166534; font-weight: 600; }}
  .tag.tag-highlight {{ background: #e0f2fe; border-color: #bae6fd; color: #0369a1; }}
  .fc-phone {{ font-size: 0.78rem; margin-top: 6px; color: #0369a1; font-weight: 600; }}
  .fc-phone a {{ color: #0369a1; text-decoration: none; }}
  .fc-phone a:hover {{ text-decoration: underline; color: #0284c7; }}
  .fc-gmaps {{ margin-top: 7px; }}
  .gmaps-link {{
    display: inline-flex; align-items: center; gap: 4px; font-size: 0.74rem; font-weight: 600;
    color: #0284c7; text-decoration: none; padding: 3px 8px; border-radius: 6px;
    background: #e0f2fe; transition: background 0.15s;
  }}
  .gmaps-link:hover {{ background: #bae6fd; }}
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
    <h1 id="header-title">🥛 Saburtalo Real Dairy Directory <span>| საბურთალოს ნამდვილი რძის ობიექტები</span></h1>
    <div id="header-sub">Verified Real Shops & Delivery • Saburtalo District, Tbilisi • Raw Milk, Bio Milk, Cottage Cheese, Matsoni, Sour Cream</div>
  </div>
  <div class="header-right">
    <div class="stats">
      <div class="stat"><div class="num" id="stat-total">{len(features)}</div><div class="lbl" id="stat-lbl-farms">Dairy Hubs</div></div>
      <div class="stat"><div class="num" id="stat-subdistricts">5</div><div class="lbl" id="stat-lbl-subdistricts">Zones</div></div>
      <div class="stat"><div class="num">4</div><div class="lbl" id="stat-lbl-categories">Categories</div></div>
    </div>
    <div class="lang-switcher">
      <button id="lang-btn-ka" class="lang-btn active" onclick="switchLanguage('ka')">ქართული</button>
      <button id="lang-btn-en" class="lang-btn" onclick="switchLanguage('en')">EN</button>
    </div>
  </div>
</div>

<div id="main">
  <div id="sidebar">
    <div id="controls">
      <input id="search" type="text" placeholder="Search milk, cottage cheese, matsoni, sour cream, bio milk…"/>
      <select id="subdistrict-select"></select>
      <button id="near-me-btn" class="near-me-btn" onclick="triggerNearMe()" title="Find dairy near my location">
        <span id="near-me-icon">📍</span> <span id="near-me-label">ჩემთან ახლოს</span>
      </button>

      <!-- Quick Dairy Product Pills Bar -->
      <div class="dairy-pill-bar" id="dairy-pill-bar">
        <button class="dairy-pill active" data-prod="all">🥛 <span class="pill-text">ყველა რძის ნაწარმი</span></button>
        <button class="dairy-pill" data-prod="milk">🥛 <span class="pill-text">ცოცხალი & ბიო რძე</span></button>
        <button class="dairy-pill" data-prod="cottage_cheese">🥣 <span class="pill-text">ხაჭო</span></button>
        <button class="dairy-pill" data-prod="matsoni">🏺 <span class="pill-text">მაწონი</span></button>
        <button class="dairy-pill" data-prod="sour_cream">🍶 <span class="pill-text">არაჟანი</span></button>
        <button class="dairy-pill" data-prod="cheese">🧀 <span class="pill-text">ყველი / სულგუნი</span></button>
      </div>

      <div class="cat-filters">
        <button id="cat-btn-all" class="cat-btn active" data-cat="all" style="border-color:#37474f;color:#37474f">🗺 All</button>
        <button id="cat-btn-fresh_milk" class="cat-btn" data-cat="fresh_milk" style="border-color:#0284c7;color:#0284c7">🥛 Milk & Bio Milk</button>
        <button id="cat-btn-matsoni_cream" class="cat-btn" data-cat="matsoni_cream" style="border-color:#059669;color:#059669">🥣 Matsoni & Cream</button>
        <button id="cat-btn-cheese_artisan" class="cat-btn" data-cat="cheese_artisan" style="border-color:#d97706;color:#d97706">🧀 Artisanal Cheese</button>
        <button id="cat-btn-delivery_coop" class="cat-btn" data-cat="delivery_coop" style="border-color:#7c3aed;color:#7c3aed">🚚 Dairy Delivery</button>
      </div>
    </div>
    <div id="near-me-status-bar" style="display: none;">
      <div class="status-main">
        <span id="near-me-status-text" class="status-text">ნაჩვენებია რძის ობიექტები თქვენგან 5 კმ-ის რადიუსში</span>
        <button id="reset-near-me-btn" class="reset-btn" onclick="resetNearMe()">ყველას ჩვენება</button>
      </div>
      <div class="status-controls">
        <span id="radius-select-label" class="radius-select-label">რადიუსი:</span>
        <select id="radius-select" class="radius-dropdown" onchange="changeRadius(this.value)">
          <option value="2">2 კმ (საბურთალო)</option>
          <option value="5" selected>5 კმ</option>
          <option value="10">10 კმ</option>
          <option value="all">მთელი საბურთალო</option>
        </select>
      </div>
    </div>
    <div id="farm-list"></div>
    <div id="no-results">No verified dairy producers match your search criteria.</div>
  </div>
  <div id="map">
  </div>
</div>

<button id="mobile-view-toggle" class="mobile-toggle-btn" onclick="toggleMobileView()">
  <span id="mobile-toggle-text">📋 სიის ნახვა ({len(features)})</span>
</button>

<div id="welcome-modal" class="modal-overlay" onclick="closeWelcomeModal(event)">
  <div class="modal-card" onclick="event.stopPropagation()">
    <div class="modal-icon">🥛 🧀</div>
    <div id="modal-title" class="modal-title">საბურთალოს ნამდვილი რძის ობიექტები</div>
    <div id="modal-desc" class="modal-desc">
      იპოვეთ ნამდვილი, შემოწმებული ობიექტები საბურთალოზე, სადაც შეგიძლიათ შეიძინოთ ცოცხალი და ბიო რძე, სოფლის ხაჭო, ქოთნის მაწონი, ნაღების არაჟანი და ხელნაკეთი ყველი!
    </div>
    <button id="modal-btn" class="modal-btn" onclick="closeWelcomeModal()">გასაგებია</button>
  </div>
</div>

<script>
const GEOJSON = {geojson_str};
const SUB_DISTRICT_NAMES = {sub_districts_json};
const CATEGORY_STYLES = {cat_styles_json};
const DAIRY_QUICK_FILTERS = {dairy_filters_json};

const I18N = {{
  en: {{
    title: "🥛 Saburtalo Real Dairy Directory",
    title_sub: "| Real Verified Shops & Spots",
    subtitle: "Verified Real Shops & Delivery • Saburtalo District, Tbilisi • Raw Milk, Bio Milk, Cottage Cheese, Matsoni, Sour Cream",
    hubs: "Dairy Hubs",
    subdistricts: "Zones",
    categories: "Categories",
    search_placeholder: "Search milk, cottage cheese, matsoni, sour cream, bio milk…",
    all_subdistricts: "All Saburtalo",
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
    radius_all: "All Saburtalo",
    showing_within_radius: "Showing dairy points within {{radius}} km of your location",
    fallback_closest: "No dairy points within {{radius}} km — showing {{count}} closest locations",
    showing_all_sorted: "Showing all dairy points sorted by distance from your location",
    reset_all: "Reset / Show All",
    your_location: "📍 Your Current Location",
    gps_loc: "Current GPS Location",
    modal_title: "🥛 Saburtalo Real Dairy Directory",
    modal_desc: "Discover real verified dairy shops and spots in Saburtalo: raw milk, bio milk, artisan cottage cheese, pot-fermented matsoni, fresh sour cream, and local delivery!",
    modal_btn: "Explore Dairy",
    geo_fallback_msg: "Geolocation unavailable. Using Pekini/Kostava center as demo."
  }},
  ka: {{
    title: "🥛 საბურთალოს ნამდვილი რძის ობიექტები",
    title_sub: "| გადამოწმებული რეალური მაღაზიები",
    subtitle: "გადამოწმებული რეალური მაღაზიები • საბურთალოს რაიონი • ცოცხალი რძე, ბიო რძე, ხაჭო, მაწონი, არაჟანი",
    hubs: "რძის წერტილი",
    subdistricts: "უბანი",
    categories: "კატეგორია",
    search_placeholder: "მოძებნეთ რძე, ხაჭო, მაწონი, არაჟანი, ბიო რძე, ყველი...",
    all_subdistricts: "მთელი საბურთალო",
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
    radius_all: "მთელი საბურთალო",
    showing_within_radius: "ნაჩვენებია რძის ობიექტები თქვენგან {{radius}} კმ-ის რადიუსში",
    fallback_closest: "{{radius}} კმ-ში ობიექტი ვერ მოიძებნა — ნაჩვენებია {{count}} უახლოესი",
    showing_all_sorted: "ნაჩვენებია ყველა ობიექტი თქვენი მდებარეობიდან მანძილის მიხედვით",
    reset_all: "ყველას ჩვენება",
    your_location: "📍 თქვენი მდებარეობა",
    gps_loc: "მიმდინარე GPS ლოკაცია",
    modal_title: "საბურთალოს ნამდვილი რძის ობიექტები",
    modal_desc: "იპოვეთ ნამდვილი, შემოწმებული ობიექტები საბურთალოზე, სადაც შეგიძლიათ შეიძინოთ ცოცხალი და ბიო რძე, სოფლის ხაჭო, ქოთნის მაწონი, ნაღების არაჟანი და ხელნაკეთი ყველი!",
    modal_btn: "გასაგებია",
    geo_fallback_msg: "გეოლოკაცია მიუწვდომელია. დემო მდებარეობად არჩეულია პეკინის ცენტრი."
  }}
}};

let currentLang = 'ka';
let userCoords = null;
let isNearMeActive = false;
let activeRadiusKm = 5;
let userMarker = null;
let userRadiusCircle = null;
let activeDairyPill = 'all';

function getDistanceKm(lat1, lon1, lat2, lon2) {{
  const R = 6371;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}}

function calculateTravelTimes(distKm) {{
  const driveMinutes = Math.max(1, Math.round((distKm / 35) * 60));
  const walkMinutes = Math.max(1, Math.round((distKm / 4.5) * 60));
  return {{ driveMinutes, walkMinutes }};
}}

function formatMinutes(mins, lang) {{
  const isKa = (lang === 'ka');
  if (mins < 60) return isKa ? `${{mins}} წთ` : `${{mins}} min`;
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  return isKa ? `${{h}} სთ ${{m}} წთ` : `${{h}} h ${{m}} m`;
}}

function getWhatsAppUrl(phone) {{
  if (!phone) return '';
  let digits = phone.replace(/\\D/g, '');
  if (!digits) return '';
  if (digits.length === 9) digits = '995' + digits;
  else if (digits.length === 8 && digits.startsWith('32')) digits = '995' + digits;
  return `https://wa.me/${{digits}}`;
}}

const map = L.map('map', {{
  center: [41.7255, 44.7485],
  zoom: 14,
  zoomControl: true
}});

function getGoogleTileUrl(layerType, lang) {{
  return `https://mt{{s}}.google.com/vt/lyrs=${{layerType}}&hl=${{lang}}&x={{x}}&y={{y}}&z={{z}}`;
}}

const googleRoad = L.tileLayer(getGoogleTileUrl('m', currentLang), {{
  attribution: 'Map data © Google', subdomains: '0123', maxZoom: 20
}}).addTo(map);

const googleSat = L.tileLayer(getGoogleTileUrl('y', currentLang), {{
  attribution: 'Imagery © Google', subdomains: '0123', maxZoom: 20
}});

let layerControl = L.control.layers(
  {{ [I18N[currentLang].google_roadmap]: googleRoad, [I18N[currentLang].google_satellite]: googleSat }},
  {{}},
  {{ position: 'topright', collapsed: false }}
).addTo(map);

function updateLayerControlLabels(lang) {{
  map.removeControl(layerControl);
  layerControl = L.control.layers(
    {{ [I18N[lang].google_roadmap]: googleRoad, [I18N[lang].google_satellite]: googleSat }},
    {{}},
    {{ position: 'topright', collapsed: false }}
  ).addTo(map);
}}

function makeIcon(color, emoji) {{
  return L.divIcon({{
    className: '',
    html: `<div style="
      background:${{color}};width:34px;height:34px;border-radius:50% 50% 50% 0;
      transform:rotate(-45deg);border:3px solid white;
      box-shadow:0 3px 8px rgba(0,0,0,0.35);
      display:flex;align-items:center;justify-content:center;">
      <span style="transform:rotate(45deg);font-size:15px">${{emoji}}</span>
    </div>`,
    iconSize: [34, 34], iconAnchor: [17, 34], popupAnchor: [0, -36]
  }});
}}

function createUserMarker(lat, lon, addressText) {{
  const pulseIcon = L.divIcon({{
    className: 'user-location-marker-container',
    html: `<div class="user-pulse-marker"><div class="user-pulse-ring"></div><div class="user-pulse-dot"></div></div>`,
    iconSize: [24, 24], iconAnchor: [12, 12], popupAnchor: [0, -14]
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
    radius: Number(radius) * 1000,
    color: '#0284c7',
    weight: 2,
    opacity: 0.75,
    fillColor: '#38bdf8',
    fillOpacity: 0.12,
    dashArray: '6, 6'
  }}).addTo(map);
}}

function buildPopupHtml(p, lang, lat, lon) {{
  const isKa = (lang === 'ka');
  const nameMain = isKa ? p.name_ka : p.name_en;
  const nameSec = isKa ? p.name_en : p.name_ka;
  const catLabel = isKa ? p.cat_label_ka : p.cat_label_en;
  const subName = isKa ? p.sub_district_ka : p.sub_district_en;
  const addr = isKa ? p.address_ka : p.address_en;
  const desc = isKa ? p.desc_ka : p.desc_en;
  const prods = (isKa ? p.products_ka : p.products_en || []).map(t => `<span class="tag tag-highlight">${{t}}</span>`).join('');

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
    const subName = isKa ? p.sub_district_ka : p.sub_district_en;
    const addr = isKa ? p.address_ka : p.address_en;
    const tags = (isKa ? p.products_ka : p.products_en || []).map(t => `<span class="tag tag-highlight">${{t}}</span>`).join('');

    let distCardHtml = '';
    if (userCoords) {{
      const d = getDistanceKm(userCoords.lat, userCoords.lon, lat, lon);
      const times = calculateTravelTimes(d);
      const driveStr = formatMinutes(times.driveMinutes, lang);
      const walkStr = formatMinutes(times.walkMinutes, lang);
      const dUnit = (lang === 'ka' ? 'კმ' : 'km');
      distCardHtml = `
        <div class="fc-distance-bar" onclick="event.stopPropagation();">
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
      <div class="fc-source">✓ Source: ${{p.source}}</div>
      ${{waCardHtml}}
      ${{distCardHtml}}
      ${{gmapsCardHtml}}
    `;
    card.addEventListener('click', () => {{
      if (window.innerWidth <= 768) setMobileView('map');
      map.flyTo([lat, lon], 16, {{ duration: 1.0 }});
      markers.forEach(m => {{
        if (m.featureProps.id === p.id) setTimeout(() => m.openPopup(), 500);
      }});
    }});
    list.appendChild(card);
  }});
}}

function closeWelcomeModal(e) {{
  if (e && e.target && e.target.id !== 'welcome-modal' && e.target.id !== 'modal-btn') return;
  const modal = document.getElementById('welcome-modal');
  if (modal) {{
    modal.classList.add('hidden');
    setTimeout(() => {{ modal.style.display = 'none'; }}, 250);
  }}
}}

const subDistrictsList = Object.keys(SUB_DISTRICT_NAMES);

function populateSubDistrictSelect(lang) {{
  const sel = document.getElementById('subdistrict-select');
  const prevVal = sel.value;
  sel.innerHTML = `<option value="">${{I18N[lang].all_subdistricts}} (${{subDistrictsList.length}})</option>`;
  subDistrictsList.forEach(k => {{
    const name = SUB_DISTRICT_NAMES[k][lang];
    const opt = document.createElement('option');
    opt.value = k;
    opt.textContent = name;
    if (k === prevVal) opt.selected = true;
    sel.appendChild(opt);
  }});
}}

let currentMobileView = 'map';
function updateMobileToggleBtn() {{
  const btnText = document.getElementById('mobile-toggle-text');
  if (!btnText) return;
  const count = document.getElementById('stat-total').textContent || '17';
  btnText.textContent = (currentMobileView === 'list')
    ? I18N[currentLang].toggle_map
    : `${{I18N[currentLang].toggle_list}} (${{count}})`;
}}

function setMobileView(view) {{
  if (window.innerWidth > 768) return;
  currentMobileView = view;
  const sidebar = document.getElementById('sidebar');
  const mapElem = document.getElementById('map');
  if (view === 'list') {{
    sidebar.classList.add('mobile-active');
    mapElem.classList.add('mobile-hidden');
  }} else {{
    sidebar.classList.remove('mobile-active');
    mapElem.classList.remove('mobile-hidden');
    setTimeout(() => map.invalidateSize(), 150);
  }}
  updateMobileToggleBtn();
}}

function toggleMobileView() {{
  setMobileView(currentMobileView === 'map' ? 'list' : 'map');
}}

function triggerNearMe() {{
  const btn = document.getElementById('near-me-btn');
  const lbl = document.getElementById('near-me-label');
  btn.classList.add('locating');
  lbl.textContent = I18N[currentLang].near_me_locating;

  function onLocationFound(lat, lon) {{
    btn.classList.remove('locating');
    btn.classList.add('active');
    lbl.textContent = I18N[currentLang].near_me;
    userCoords = {{ lat, lon, address: '' }};
    isNearMeActive = true;

    if (userMarker && map.hasLayer(userMarker)) map.removeLayer(userMarker);
    userMarker = createUserMarker(lat, lon, '').addTo(map);
    userMarker.openPopup();

    updateUserRadiusCircle(lat, lon, activeRadiusKm);
    updateAllMarkersPopups();
    applyFilters();
  }}

  function onLocationError(err) {{
    btn.classList.remove('locating');
    console.warn('Geolocation fallback to Saburtalo center:', err);
    alert(I18N[currentLang].geo_fallback_msg);
    onLocationFound(41.7225, 44.7310);
  }}

  if ('geolocation' in navigator) {{
    navigator.geolocation.getCurrentPosition(
      pos => onLocationFound(pos.coords.latitude, pos.coords.longitude),
      err => onLocationError(err),
      {{ timeout: 8000, enableHighAccuracy: true }}
    );
  }} else {{
    onLocationError(new Error('Geolocation not supported'));
  }}
}}

function changeRadius(val) {{
  activeRadiusKm = (val === 'all') ? 'all' : Number(val);
  if (userCoords) updateUserRadiusCircle(userCoords.lat, userCoords.lon, activeRadiusKm);
  applyFilters();
}}

function resetNearMe() {{
  isNearMeActive = false;
  activeRadiusKm = 5;
  userCoords = null;
  const btn = document.getElementById('near-me-btn');
  if (btn) btn.classList.remove('active');
  if (userRadiusCircle && map.hasLayer(userRadiusCircle)) {{
    map.removeLayer(userRadiusCircle);
    userRadiusCircle = null;
  }}
  if (userMarker && map.hasLayer(userMarker)) {{
    map.removeLayer(userMarker);
    userMarker = null;
  }}
  document.getElementById('near-me-status-bar').style.display = 'none';
  document.getElementById('radius-select').value = '5';
  updateAllMarkersPopups();
  applyFilters();
  map.setView([41.7255, 44.7485], 14);
}}

let activeCat = 'all';
let activeSubDistrict = '';
let searchText = '';

function matchDairyPill(p, pillKey) {{
  if (pillKey === 'all') return true;
  const filterDef = DAIRY_QUICK_FILTERS.find(f => f.id === pillKey);
  if (!filterDef || !filterDef.terms) return true;
  const targetStr = ((p.products_en || []).concat(p.products_ka || []).concat([p.desc_en, p.desc_ka, p.name_en, p.name_ka])).join(' ').toLowerCase();
  return filterDef.terms.some(term => targetStr.includes(term.toLowerCase()));
}}

function applyFilters() {{
  const q = searchText.toLowerCase().trim();
  let candidateFeatures = GEOJSON.features.slice();

  if (isNearMeActive && userCoords) {{
    document.getElementById('near-me-status-bar').style.display = 'flex';
    const withDist = candidateFeatures.map(f => {{
      const [lon, lat] = f.geometry.coordinates;
      return {{ f, dist: getDistanceKm(userCoords.lat, userCoords.lon, lat, lon) }};
    }});
    withDist.sort((a, b) => a.dist - b.dist);

    if (activeRadiusKm === 'all') {{
      candidateFeatures = withDist.map(item => item.f);
      document.getElementById('near-me-status-text').textContent = I18N[currentLang].showing_all_sorted;
    }} else {{
      const inRadius = withDist.filter(item => item.dist <= activeRadiusKm);
      if (inRadius.length < 2) {{
        candidateFeatures = withDist.slice(0, 5).map(item => item.f);
        document.getElementById('near-me-status-text').textContent =
          I18N[currentLang].fallback_closest.replace('{{radius}}', activeRadiusKm).replace('{{count}}', candidateFeatures.length);
      }} else {{
        candidateFeatures = inRadius.map(item => item.f);
        document.getElementById('near-me-status-text').textContent =
          I18N[currentLang].showing_within_radius.replace('{{radius}}', activeRadiusKm);
      }}
    }}
  }} else {{
    document.getElementById('near-me-status-bar').style.display = 'none';
  }}

  const filtered = candidateFeatures.filter(f => {{
    const p = f.properties;
    const matchCat = activeCat === 'all' || p.category === activeCat;
    const matchSub = !activeSubDistrict || p.sub_district === activeSubDistrict;
    const matchPill = matchDairyPill(p, activeDairyPill);

    const prodsAll = (p.products_en || []).concat(p.products_ka || []).join(' ').toLowerCase();
    const matchSearch = !q ||
      p.name_en.toLowerCase().includes(q) ||
      p.name_ka.toLowerCase().includes(q) ||
      p.sub_district_en.toLowerCase().includes(q) ||
      p.sub_district_ka.toLowerCase().includes(q) ||
      p.address_en.toLowerCase().includes(q) ||
      p.address_ka.toLowerCase().includes(q) ||
      p.desc_en.toLowerCase().includes(q) ||
      p.desc_ka.toLowerCase().includes(q) ||
      prodsAll.includes(q);

    return matchCat && matchSub && matchPill && matchSearch;
  }});

  buildSidebar(filtered, currentLang);
  updateMobileToggleBtn();

  const visibleIds = new Set(filtered.map(f => f.properties.id));
  markers.forEach(m => {{
    if (visibleIds.has(m.featureProps.id)) {{
      if (!map.hasLayer(m)) m.addTo(map);
    }} else {{
      if (map.hasLayer(m)) map.removeLayer(m);
    }}
  }});

  if (isNearMeActive && userCoords) {{
    const boundsGroup = [];
    if (userMarker) boundsGroup.push(userMarker);
    if (userRadiusCircle && map.hasLayer(userRadiusCircle)) boundsGroup.push(userRadiusCircle);
    markers.filter(m => visibleIds.has(m.featureProps.id)).forEach(m => boundsGroup.push(m));
    if (boundsGroup.length > 0) map.fitBounds(L.featureGroup(boundsGroup).getBounds().pad(0.1));
  }} else if (filtered.length > 0) {{
    map.fitBounds(L.featureGroup(markers.filter(m => visibleIds.has(m.featureProps.id))).getBounds().pad(0.1));
  }}
}}

function switchLanguage(lang) {{
  currentLang = lang;
  const isKa = (lang === 'ka');
  document.getElementById('lang-btn-ka').classList.toggle('active', isKa);
  document.getElementById('lang-btn-en').classList.toggle('active', !isKa);

  document.getElementById('header-title').innerHTML = `${{I18N[lang].title}} <span>${{I18N[lang].title_sub}}</span>`;
  document.getElementById('header-sub').textContent = I18N[lang].subtitle;
  document.getElementById('stat-lbl-farms').textContent = I18N[lang].hubs;
  document.getElementById('stat-lbl-subdistricts').textContent = I18N[lang].subdistricts;
  document.getElementById('stat-lbl-categories').textContent = I18N[lang].categories;

  document.getElementById('search').placeholder = I18N[lang].search_placeholder;
  document.getElementById('no-results').textContent = I18N[lang].no_results;

  // Update Dairy Quick Pills
  document.querySelectorAll('.dairy-pill').forEach(btn => {{
    const prodKey = btn.dataset.prod;
    const filterDef = DAIRY_QUICK_FILTERS.find(f => f.id === prodKey);
    if (filterDef) {{
      const textSpan = btn.querySelector('.pill-text');
      if (textSpan) textSpan.textContent = isKa ? filterDef.label_ka : filterDef.label_en;
    }}
  }});

  document.getElementById('cat-btn-all').textContent = I18N[lang].all_cats;
  document.getElementById('cat-btn-fresh_milk').textContent = I18N[lang].fresh_milk;
  document.getElementById('cat-btn-matsoni_cream').textContent = I18N[lang].matsoni_cream;
  document.getElementById('cat-btn-cheese_artisan').textContent = I18N[lang].cheese_artisan;
  document.getElementById('cat-btn-delivery_coop').textContent = I18N[lang].delivery_coop;

  const nearMeLbl = document.getElementById('near-me-label');
  if (nearMeLbl) nearMeLbl.textContent = I18N[lang].near_me;
  const resetBtn = document.getElementById('reset-near-me-btn');
  if (resetBtn) resetBtn.textContent = I18N[lang].reset_all;
  const radLbl = document.getElementById('radius-select-label');
  if (radLbl) radLbl.textContent = I18N[lang].radius_label;
  const radSelect = document.getElementById('radius-select');
  if (radSelect) {{
    radSelect.options[0].textContent = I18N[lang].radius_2;
    radSelect.options[1].textContent = I18N[lang].radius_5;
    radSelect.options[2].textContent = I18N[lang].radius_10;
    radSelect.options[3].textContent = I18N[lang].radius_all;
  }}

  const modalTitle = document.getElementById('modal-title');
  if (modalTitle) modalTitle.textContent = I18N[lang].modal_title;
  const modalDesc = document.getElementById('modal-desc');
  if (modalDesc) modalDesc.textContent = I18N[lang].modal_desc;
  const modalBtn = document.getElementById('modal-btn');
  if (modalBtn) modalBtn.textContent = I18N[lang].modal_btn;

  populateSubDistrictSelect(lang);
  googleRoad.setUrl(getGoogleTileUrl('m', lang));
  googleSat.setUrl(getGoogleTileUrl('y', lang));
  updateLayerControlLabels(lang);
  updateAllMarkersPopups();
  applyFilters();
  updateMobileToggleBtn();
}}

// Category Button Clicks
document.querySelectorAll('.cat-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeCat = btn.dataset.cat;
    applyFilters();
  }});
}});

// Dairy Quick Pill Clicks
document.querySelectorAll('.dairy-pill').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('.dairy-pill').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeDairyPill = btn.dataset.prod;
    applyFilters();
  }});
}});

document.getElementById('subdistrict-select').addEventListener('change', e => {{
  activeSubDistrict = e.target.value;
  applyFilters();
}});

document.getElementById('search').addEventListener('input', e => {{
  searchText = e.target.value;
  applyFilters();
}});

populateSubDistrictSelect(currentLang);
switchLanguage('ka');
map.setView([41.7255, 44.7485], 14);
</script>
</body>
</html>"""

def main():
    if not os.path.exists(VERIFIED_PATH):
        raise FileNotFoundError(f"Missing {VERIFIED_PATH}. Run verify_saburtalo.py first.")

    with open(VERIFIED_PATH, "r", encoding="utf-8") as f:
        farms = json.load(f)

    print(f"\n🗺 Saburtalo Real Dairy Publisher — Geocoding & Rendering {len(farms)} Real Dairy Locations\n{'─'*70}")
    features = build_features(farms)
    html_content = render_html(features)

    with open(OUTPUT_POC_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)

    with open(OUTPUT_INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)

    with open(VERIFIED_PATH, "w", encoding="utf-8") as f:
        json.dump(farms, f, ensure_ascii=False, indent=2)

    print(f"✅ Saburtalo Real Dairy Map Created: {OUTPUT_POC_PATH}")
    print(f"✅ Output index.html Created: {OUTPUT_INDEX_PATH}")
    print(f"   Locations plotted: {len(features)}")
    print(f"   Bounding Box: Lat [{SABURTALO_BOUNDS['lat_min']}, {SABURTALO_BOUNDS['lat_max']}], Lon [{SABURTALO_BOUNDS['lon_min']}, {SABURTALO_BOUNDS['lon_max']}]")

if __name__ == "__main__":
    main()
