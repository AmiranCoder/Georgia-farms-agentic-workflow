#!/usr/bin/env python3
"""
execution/publish_map.py
Map Publisher — Nationwide Phase (Andrew Ng: Tool Use + Quantitative Evaluations Pattern)

Geocodes verified farms across all regions of Georgia using a curated high-precision gazetteer,
enforces 100% bounding box evaluations (41.0–43.5° N, 40.0–46.7° E),
and renders output/georgia_farms_map.html with:
  - Zero-seam Leaflet tile rendering (CSS background & subpixel overlap)
  - Full Georgian / English Language Switcher (EN | ქართული) in header
  - Google Roadmap & Google Satellite/Hybrid layers with dynamic &hl=ka / &hl=en tile language
  - Fully translated UI labels, region dropdown, category filter buttons, sidebar cards, and popups
"""

import json
import os

VERIFIED_PATH = os.path.join(os.path.dirname(__file__), "..", "output", "verified_farms.json")
OUTPUT_PATH   = os.path.join(os.path.dirname(__file__), "..", "output", "georgia_farms_map.html")

# ─── Official Territorial Bounding Box of Georgia ───────────────────────────
GEO_BOUNDS = {"lat_min": 41.0, "lat_max": 43.5, "lon_min": 40.0, "lon_max": 46.7}

# ─── Curated High-Precision Nationwide Gazetteer ────────────────────────────
GEORGIA_GAZETTEER = {
    # Tbilisi & Surroundings
    "Tbilisi Logistics Hub, Direct Delivery across Tbilisi, Georgia":            (41.7151, 44.7871),
    "eBazaar Farmers Network, Central Delivery Hub, Tbilisi, Georgia":           (41.7225, 44.7712),
    "Sioni Street, Old Tbilisi, Tbilisi, Georgia":                               (41.6912, 44.8075),

    # Mtskheta-Mtianeti
    "Pasanauri, Aragvi Gorge, Dusheti Municipality, Mtskheta-Mtianeti, Georgia": (42.3508, 44.6931),
    "Shio-Mgvime Valley, Mtskheta Municipality, Mtskheta-Mtianeti, Georgia":     (41.8624, 44.6408),

    # Shida Kartli
    "Ateni village, Gori Municipality, Shida Kartli, Georgia":                   (41.9056, 44.1031),
    "Karaleti village, Gori Municipality, Shida Kartli, Georgia":                 (42.0210, 44.0915),

    # Samtskhe-Javakheti
    "Andriatsminda village, Akhaltsikhe Municipality, Samtskhe-Javakheti, Georgia":(41.6052, 43.1210),
    "Tsnisi village, Akhaltsikhe Municipality, Samtskhe-Javakheti, Georgia":      (41.6421, 43.0154),

    # Imereti
    "Paliashvili Street, Kutaisi, Imereti, Georgia":                             (42.2662, 42.7180),
    "Obcha village, Baghdati Municipality, Imereti, Georgia":                     (42.1030, 42.8421),

    # Samegrelo-Zemo Svaneti
    "Senaki Municipality, Samegrelo-Zemo Svaneti, Georgia":                      (42.2710, 42.0652),
    "Tsalenjikha Municipality, Samegrelo-Zemo Svaneti, Georgia":                 (42.6052, 42.0720),

    # Adjara
    "Chvana Gorge, Shuakhevi Municipality, Autonomous Republic of Adjara, Georgia":(41.6255, 42.1852),
    "Chakvi, Kobuleti Municipality, Autonomous Republic of Adjara, Georgia":     (41.7252, 41.7335),

    # Guria
    "Kveda Bakhvi village, Ozurgeti Municipality, Guria, Georgia":               (41.9510, 42.0520),
    "Likhauri village, Ozurgeti Municipality, Guria, Georgia":                   (41.8752, 42.0014),

    # Racha-Lechkhumi
    "#2 Vazha-Pshavela / #7 Kostava St, Ambrolauri, Racha-Lechkhumi, Georgia":   (42.5215, 43.1512),
    "Shaori Reservoir, Ambrolauri Municipality, Racha-Lechkhumi, Georgia":       (42.4720, 43.0425),

    # Kakheti (Pilot)
    "Qvemo Alvani village, Akhmeta Municipality, Kakheti, Georgia":               (42.0481, 45.2098),
    "Shalauri village, Telavi Municipality, Kakheti, Georgia":                   (41.9220, 45.4700),
    "7a Chavchavadze St, Sighnaghi, Kakheti, Georgia":                           (41.6155, 45.9200),
    "Ninotsminda village, Sagarejo Municipality, Kakheti, Georgia":               (41.7500, 45.3700),
    "Sighnaghi–Telavi area, Kakheti, Georgia":                                    (41.7500, 45.6000),
    "Kakheti Region (Direct Deliveries to Tbilisi), Georgia":                    (41.9100, 45.3600),
    "Gurjaani / Kvareli, Alazani Valley, Kakheti, Georgia":                       (41.7400, 45.8000),

    # Kvemo Kartli (Pilot)
    "Bolnisi Municipality, Kvemo Kartli, Georgia":                                (41.4517, 44.5236),
    "Marneuli / Bolnisi / Tsalka municipalities, Kvemo Kartli, Georgia":         (41.4800, 44.7200),
}

# ─── Canonical Georgian Address Mapping ─────────────────────────────────────
GEORGIAN_ADDRESSES = {
    "Tbilisi Logistics Hub, Direct Delivery across Tbilisi, Georgia":            "თბილისის ლოგისტიკური ცენტრი, მიტანა თბილისის მასშტაბით",
    "eBazaar Farmers Network, Central Delivery Hub, Tbilisi, Georgia":           "eBazaar ფერმერთა ქსელი, ცენტრალური ჰაბი, თბილისი",
    "Sioni Street, Old Tbilisi, Tbilisi, Georgia":                               "სიონის ქუჩა, ძველი თბილისი, თბილისი",
    "Pasanauri, Aragvi Gorge, Dusheti Municipality, Mtskheta-Mtianeti, Georgia": "ფასანაური, არაგვის ხეობა, დუშეთის მუნიციპალიტეტი, მცხეთა-მთიანეთი",
    "Shio-Mgvime Valley, Mtskheta Municipality, Mtskheta-Mtianeti, Georgia":     "შიომღვიმის ხეობა, მცხეთის მუნიციპალიტეტი, მცხეთა-მთიანეთი",
    "Ateni village, Gori Municipality, Shida Kartli, Georgia":                   "სოფელი ატენი, გორის მუნიციპალიტეტი, შიდა ქართლი",
    "Karaleti village, Gori Municipality, Shida Kartli, Georgia":                 "სოფელი ყარალეთი, გორის მუნიციპალიტეტი, შიდა ქართლი",
    "Andriatsminda village, Akhaltsikhe Municipality, Samtskhe-Javakheti, Georgia":"სოფელი ანდრიაწმინდა, ახალციხის მუნიციპალიტეტი, სამცხე-ჯავახეთი",
    "Tsnisi village, Akhaltsikhe Municipality, Samtskhe-Javakheti, Georgia":      "სოფელი წნისი, ახალციხის მუნიციპალიტეტი, სამცხე-ჯავახეთი",
    "Paliashvili Street, Kutaisi, Imereti, Georgia":                             "ფალიაშვილის ქუჩა, ქუთაისი, იმერეთი",
    "Obcha village, Baghdati Municipality, Imereti, Georgia":                     "სოფელი ობჩა, ბაღდათის მუნიციპალიტეტი, იმერეთი",
    "Senaki Municipality, Samegrelo-Zemo Svaneti, Georgia":                      "სენაკის მუნიციპალიტეტი, სამეგრელო-ზემო სვანეთი",
    "Tsalenjikha Municipality, Samegrelo-Zemo Svaneti, Georgia":                 "წალენჯიხის მუნიციპალიტეტი, სამეგრელო-ზემო სვანეთი",
    "Chvana Gorge, Shuakhevi Municipality, Autonomous Republic of Adjara, Georgia":"ჭვანის ხეობა, შუახევის მუნიციპალიტეტი, აჭარის ა.რ.",
    "Chakvi, Kobuleti Municipality, Autonomous Republic of Adjara, Georgia":     "ჩაქვი, ქობულეთის მუნიციპალიტეტი, აჭარის ა.რ.",
    "Kveda Bakhvi village, Ozurgeti Municipality, Guria, Georgia":               "სოფელი ქვედა ბახვი, ოზურგეთის მუნიციპალიტეტი, გურია",
    "Likhauri village, Ozurgeti Municipality, Guria, Georgia":                   "სოფელი ლიხაური, ოზურგეთის მუნიციპალიტეტი, გურია",
    "#2 Vazha-Pshavela / #7 Kostava St, Ambrolauri, Racha-Lechkhumi, Georgia":   "ვაჟა-ფშაველას #2 / კოსტავას #7, ამბროლაური, რაჭა-ლეჩხუმი",
    "Shaori Reservoir, Ambrolauri Municipality, Racha-Lechkhumi, Georgia":       "შაორის წყალსაცავი, ამბროლაურის მუნიციპალიტეტი, რაჭა-ლეჩხუმი",
    "Qvemo Alvani village, Akhmeta Municipality, Kakheti, Georgia":               "სოფელი ქვემო ალვანი, ახმეტის მუნიციპალიტეტი, კახეთი",
    "Shalauri village, Telavi Municipality, Kakheti, Georgia":                   "სოფელი შალაური, თელავის მუნიციპალიტეტი, კახეთი",
    "7a Chavchavadze St, Sighnaghi, Kakheti, Georgia":                           "ჭავჭავაძის ქ. 7ა, სიღნაღი, კახეთი",
    "Ninotsminda village, Sagarejo Municipality, Kakheti, Georgia":               "სოფელი ნინოწმინდა, საგარეჯოს მუნიციპალიტეტი, კახეთი",
    "Sighnaghi–Telavi area, Kakheti, Georgia":                                    "სიღნაღი–თელავის მიდამოები, კახეთი",
    "Kakheti Region (Direct Deliveries to Tbilisi), Georgia":                    "კახეთის რეგიონი (მიტანა თბილისში)",
    "Gurjaani / Kvareli, Alazani Valley, Kakheti, Georgia":                       "გურჯაანი / ყვარელი, ალაზნის ველი, კახეთი",
    "Bolnisi Municipality, Kvemo Kartli, Georgia":                                "ბოლნისის მუნიციპალიტეტი, ქვემო ქართლი",
    "Marneuli / Bolnisi / Tsalka municipalities, Kvemo Kartli, Georgia":         "მარნეული / ბოლნისი / წალკა, ქვემო ქართლი",
}

# ─── Comprehensive Georgian Descriptions & Products ────────────────────────
GEORGIAN_ENRICHMENT = {
    "farm-geo-001": {
        "desc_ka": "ფერმიდან სახლში მიტანის სერვისი: ნატურალური, დანამატების გარეშე დამზადებული ქართული რძის ნაწარმი (ქოთნის სქელი მაწონი, ცოცხალი რძე, ნადუღი, კარაქი) და სოფლის კვერცხი თბილისის მასშტაბით.",
        "products_ka": ["ნატურალური მაწონი", "ნედლი რძე", "ხელნაკეთი ხაჭო", "სოფლის კვერცხი", "სოფლის კარაქი", "სოფლის ფრინველი"]
    },
    "farm-geo-002": {
        "desc_ka": "ციფრული პლატფორმა და ლოგისტიკური ჰაბი, რომელიც საქართველოს სხვადასხვა რეგიონის მცირე ფერმერებსა და კოოპერატივებს პირდაპირ აკავშირებს თბილისის მომხმარებლებთან.",
        "products_ka": ["სულგუნი", "იმერული ყველი", "სოფლის კვერცხი", "მთის თაფლი", "სოფლის ხორცი", "სეზონური ბოსტნეულის ყუთები"]
    },
    "farm-geo-003": {
        "desc_ka": "ავთენტური პირდაპირი სავაჭრო წერტილი ძველ თბილისში, რომელიც მარაგდება ექსკლუზიურად რეგიონული სამონასტრო მეურნეობებისა და ეკო-ფერმების მიერ. ახალი პროდუქცია კვირაში ორჯერ ჩამოდის.",
        "products_ka": ["სამონასტრო მაწონი", "სამკურნალო მცენარეების ჩაი", "ალპური ველური თაფლი", "სუფთა ცვილის სანთლები", "სოფლის კვერცხი", "გუდის ყველი"]
    },
    "farm-geo-004": {
        "desc_ka": "მთის ცივი წყაროს კალმახის მეურნეობა ზემო არაგვის ხეობაში. სტუმრებს შეუძლიათ პირდაპირ ადგილზე შეიძინონ ახლად დაჭერილი მდინარის კალმახი და ალპური თაფლი.",
        "products_ka": ["ცოცხალი მთის კალმახი", "ალპური ველური თაფლი", "მთის მწვანილი", "თონის შოთი"]
    },
    "farm-geo-005": {
        "desc_ka": "მცირე საოჯახო თხის ფერმა და ყველის საწარმო მცხეთის კლდეებში. სპეციალიზებულია თხის რძეზე, მაწონსა და დავარგებულ მწვანილოვან ყველებზე.",
        "products_ka": ["თხის მაწონი", "თხის რძე", "მწვანილოვანი თხის ყველი", "ცაცხვის თაფლი"]
    },
    "farm-geo-006": {
        "desc_ka": "მრავალწლიანი ხეხილისა და ყურძნის მეურნეობა ატენის ხეობის უნიკალურ მიკროკლიმატში. ყიდის ხეზე დამწიფებულ თეთრ ატამსა და ქლიავს პირდაპირ ბაღიდან.",
        "products_ka": ["ატენური თეთრი ატამი", "ტკბილი ქლიავი", "ახალი ბალი", "ატენური თეთრი ღვინო"]
    },
    "farm-geo-007": {
        "desc_ka": "ვაშლისა და მსხლის ინტენსიური ბაღი გორის ვაკეზე. სთავაზობს სეზონურ თვითკრეფას აგვისტოდან ოქტომბრის ბოლომდე.",
        "products_ka": ["ვაშლი გოლდენი", "ვაშლი რედ დელიშესი", "ვაშლი გალა", "შემოდგომის მსხალი", "ნატურალური წვენი"]
    },
    "farm-geo-008": {
        "desc_ka": "Slow Food Presidium-ის აღიარებული ყველის ოსტატი. აცოცხლებს მესხური თენილი ყველის უძველეს ტრადიციას — თმისებრ წვრილ ძაფებად დაწელილ ყველს, რომელიც თიხის ქოთანში ნაღებთან ერთად ძველდება.",
        "products_ka": ["იუნესკოს თენილი ყველი", "ალპური კარაქი", "მესხური ნადუღი", "კალმახი"]
    },
    "farm-geo-009": {
        "desc_ka": "ფერმერთა კოოპერატივი, რომელიც აერთიანებს 1200+ მეტრზე მოყვანილ ეკოლოგიურად სუფთა, მინერალებით მდიდარ მთის კარტოფილს.",
        "products_ka": ["მესხური მთის კარტოფილი", "ნიორი", "ძირხვენები", "ორგანული ლობიო"]
    },
    "farm-geo-010": {
        "desc_ka": "ისტორიული ფერმერული გაცვლის ცენტრი, რომელიც აერთიანებს მცირე ფერმერებს წყალტუბოდან, თერჯოლიდან და ზესტაფონიდან. ყველი ყოველდღიურად დილის წველიდან მოდის.",
        "products_ka": ["ახალი იმერული ყველი", "შებოლილი სულგუნი", "ნადუღი პიტნით", "სოფლის ერბო", "ჭვიშტარის ფქვილი"]
    },
    "farm-geo-011": {
        "desc_ka": "ქალთა მიერ დაარსებული ორგანული მეურნეობა იმერეთის ბორცვებზე. აწარმოებს ბიოდინამიკურ ღვინოებს, თაფლს და ადგილობრივ ხილს.",
        "products_ka": ["ციცქა-ცოლიკოურის ნატურალური ღვინო", "კრახუნა", "ველური თაფლი", "კაკალი", "ხელნაკეთი ტყლაპი"]
    },
    "farm-geo-012": {
        "desc_ka": "ხელნაკეთი კოოპერატივი, რომელიც ინარჩუნებს მეგრული სულგუნის ტრადიციას. იყენებს მეგრული წითელი ჯიშის ძროხების რძეს.",
        "products_ka": ["ტრადიციული მეგრული სულგუნი", "მურყნის ბოლზე შებოლილი სულგუნი", "ახალი გებჟალია პიტნის მაწონში", "მეგრული კარაქი"]
    },
    "farm-geo-013": {
        "desc_ka": "მეურნეობა კოლხეთის დაბლობზე. სთავაზობს მოცვის სეზონურ თვითკრეფას და ანაკლიური ჯიშის ორგანულ თხილს.",
        "products_ka": ["ანაკლიური ორგანული თხილი", "მოცვი (ივლისი)", "მაყვალი", "სუბტროპიკული მანდარინი"]
    },
    "farm-geo-014": {
        "desc_ka": "მაღალმთიანი რძის საწარმო ჭვანის ულამაზეს ხეობაში. ალპურ საძოვრებზე გაზრდილი ძროხების ცხიმიანი რძით მზადდება ლეგენდარული აჭარული ყაიმაღი და ყველი.",
        "products_ka": ["აჭარული ჩოგი", "ალპური ყაიმაღი", "წაბლის თაფლი", "მთის ერბო"]
    },
    "farm-geo-015": {
        "desc_ka": "ზღვისპირა ფერდობის პლანტაცია შავ ზღვასთან. სტუმრებს შეუძლიათ საკუთარი ხელით დაკრიფონ მწიფე მანდარინი, ფორთოხალი და მონაწილეობა მიიღონ ჩაის კრეფაში.",
        "products_ka": ["საცუმას მანდარინი (თვითკრეფა)", "მაიერის ლიმონი", "ტკბილი ფორთოხალი", "ხელნაკეთი შავი და მწვანე ჩაი"]
    },
    "farm-geo-016": {
        "desc_ka": "პრემიერ-მწარმოებელი გურიის ბუტიკური ორგანული ჩაის წარმოებაში. ფერმის მაღაზია სთავაზობს ჩაის დეგუსტაციას და პირდაპირ ვაკუუმ-შეფუთვებს.",
        "products_ka": ["ორგანული შავი ჩაი", "ხელნაკეთი მწვანე ჩაი", "ალპური მოცვის ფოთლის ჩაი", "წაბლის თაფლი"]
    },
    "farm-geo-017": {
        "desc_ka": "სასოფლო-სამეურნეო კოოპერატივი, რომელიც აერთიანებს ოზურგეთის ორგანულ თხილსა და ტრადიციულ მზეზე გამომშრალ ხურმის ჩირს.",
        "products_ka": ["გარჩეული გურული თხილი", "ხურმის ჩირი", "ადგილობრივი ციტრუსი", "თხილის ზეთი"]
    },
    "farm-geo-018": {
        "desc_ka": "ოფიციალური რეგიონული კოოპერატივი ამბროლაურსა და ონში. განთქმულია მურყნის ხის ბოლზე შებოლილი რაჭული ლორითა და ადგილობრივი ლობიოთი.",
        "products_ka": ["დაცული გეოგრაფიული აღნიშვნის რაჭული ლორი", "რაჭული ლობიო", "მთის ყვავილის თაფლი", "ადგილობრივი ნიგოზი"]
    },
    "farm-geo-019": {
        "desc_ka": "მაღალმთიანი ტბისპირა თევზსაშენი და საოჯახო ყველის საწარმო ცივი წყაროს წყლებითა და რაჭული სამყურას საძოვრებით.",
        "products_ka": ["ცოცხალი მთის კალმახი", "რაჭული ხაჭო-ყველი", "ველური მწვანილის კარაქი", "შებოლილი მთის ყველი"]
    },
    "farm-geo-020": {
        "desc_ka": "სერტიფიცირებული კოოპერატივი, რომელიც აწარმოებს ავთენტურ თუშურ გუდას. ყველი მწიფდება ტრადიციულ ცხვრის გუდაში (გუდის ტყავში).",
        "products_ka": ["თუშური გუდა (სვილობი)", "ლართუშო", "დოვნა", "ჩოგი"]
    },
    "farm-geo-021": {
        "desc_ka": "ბუტიკური აგროტურისტული ყველის ფერმა ალაზნის ველზე. ფრანგული ტექნოლოგიით დამზადებული თხისა და ძროხის ხელნაკეთი ყველები, დეგუსტაცია და ღია კაფე.",
        "products_ka": ["თხის ყველი ნახშირით", "ბონა (თეთრი ობით)", "აშმელო", "ლაბნე", "სულგუნი"]
    },
    "farm-geo-022": {
        "desc_ka": "ცნობილი ნატურალური ღვინის მარანი და ფერმერული მაღაზია სიღნაღში (ჭავჭავაძის 7ა). ქვევრის ღვინოები და ორგანული სოფლის პროდუქტები.",
        "products_ka": ["რქაწითელი ნატურალური ღვინო", "მწვანე ქარვისფერი ღვინო", "ადგილობრივი თაფლი", "ჩურჩხელა", "ჭაჭა", "სეზონური პროდუქტები"]
    },
    "farm-geo-023": {
        "desc_ka": "მარანი და ფერმის მაღაზია სოფელ ნინოწმინდაში, საგარეჯოში. ყიდის კლასიკურ და ქვევრის ღვინოებს პირდაპირ მარნიდან.",
        "products_ka": ["რეგიონული ღვინოები", "ქვევრის ღვინის პარტიები", "რქაწითელი", "საფერავი"]
    },
    "farm-geo-024": {
        "desc_ka": "საოჯახო მარნები სიღნაღსა და თელავში სტუმრებს სთავაზობენ რთველში უშუალო მონაწილეობას, ყურძნის კრეფას და ღვინის დაწურვას.",
        "products_ka": ["რქაწითელი ყურძენი", "საფერავი ყურძენი", "მწვანე ყურძენი"]
    },
    "farm-geo-025": {
        "desc_ka": "ამერიკული CSA მოდელის პიონერი საქართველოში. კახეთის ფერმერული პროდუქტების რეგულარული ყუთების მიტანა თბილისსა და კახეთში.",
        "products_ka": ["სეზონური ბოსტნეულის ყუთები", "მწვანილის კონები", "სოფლის კვერცხი", "სოფლის თაფლი", "ხილის ყუთები"]
    },
    "farm-geo-026": {
        "desc_ka": "ღია გრუნტის მარწყვისა და ბლის ბაღები ალაზნის ველზე (გურჯაანი/ყვარელი), პირდაპირი თვითკრეფის შესაძლებლობით.",
        "products_ka": ["მარწყვი (მაისი-ივნისი)", "ბალი (ივნისი-ივლისი)", "ქლიავი", "ლეღვი"]
    },
    "farm-geo-027": {
        "desc_ka": "ქალთა მიერ დაარსებული კოოპერატივი ბოლნისში. 100% ნატურალური რძის ნაწარმი: სულგუნი, იმერული ყველი, ნადუღი და კარაქი.",
        "products_ka": ["სულგუნი", "იმერული ყველი", "ნადუღი", "კარაქი", "ნედლი რძე"]
    },
    "farm-geo-028": {
        "desc_ka": "საქართველოს ფერმერთა ასოციაციის კოოპერატივების ქსელი ქვემო ქართლში (მარნეული, ბოლნისი, წალკა). ფერმერული პროდუქციის გაერთიანება და მიწოდება.",
        "products_ka": ["სეზონური ბოსტნეული", "რძის პროდუქტები", "მარცვლეული", "პარკოსნები"]
    }
}

# ─── Category Visual Styles & Bilingual Labels ──────────────────────────────
CATEGORY_STYLES = {
    "farm_shop":    {"color": "#2d7a2d", "emoji": "🏪", "label_en": "Farm Shop",     "label_ka": "ფერმერული მაღაზია"},
    "dairy_hub":    {"color": "#d4a017", "emoji": "🧀", "label_en": "Dairy Hub",     "label_ka": "რძის პროდუქტები"},
    "pick_your_own":{"color": "#c0392b", "emoji": "🍓", "label_en": "Pick Your Own", "label_ka": "კრეფა / აგროტურიზმი"},
    "delivery_coop":{"color": "#2471a3", "emoji": "🚚", "label_en": "Delivery Coop", "label_ka": "მიტანის სერვისი"},
}

REGION_NAMES = {
    "Tbilisi":                {"en": "Tbilisi",                "ka": "თბილისი"},
    "Adjara":                 {"en": "Adjara",                 "ka": "აჭარა"},
    "Guria":                  {"en": "Guria",                  "ka": "გურია"},
    "Imereti":                {"en": "Imereti",                "ka": "იმერეთი"},
    "Kakheti":                {"en": "Kakheti",                "ka": "კახეთი"},
    "Kvemo Kartli":           {"en": "Kvemo Kartli",           "ka": "ქვემო ქართლი"},
    "Mtskheta-Mtianeti":      {"en": "Mtskheta-Mtianeti",      "ka": "მცხეთა-მთიანეთი"},
    "Racha-Lechkhumi":        {"en": "Racha-Lechkhumi",        "ka": "რაჭა-ლეჩხუმი"},
    "Samegrelo-Zemo Svaneti": {"en": "Samegrelo-Zemo Svaneti", "ka": "სამეგრელო-ზემო სვანეთი"},
    "Samtskhe-Javakheti":     {"en": "Samtskhe-Javakheti",     "ka": "სამცხე-ჯავახეთი"},
    "Shida Kartli":           {"en": "Shida Kartli",           "ka": "შიდა ქართლი"},
}

def geocode(farm):
    addr = farm.get("address", "")
    if addr in GEORGIA_GAZETTEER:
        return GEORGIA_GAZETTEER[addr]
    for key, coords in GEORGIA_GAZETTEER.items():
        if farm.get("municipality_or_village", "").lower()[:12] in key.lower():
            return coords
    return None

def passes_bbox(lat, lon):
    return (GEO_BOUNDS["lat_min"] <= lat <= GEO_BOUNDS["lat_max"] and
            GEO_BOUNDS["lon_min"] <= lon <= GEO_BOUNDS["lon_max"])

def build_features(farms):
    features = []
    passed, failed = 0, 0
    for farm in farms:
        coords = geocode(farm)
        if not coords:
            print(f"  ⚠️  NO COORDINATES: {farm['name_en']}")
            failed += 1
            continue
        lat, lon = coords
        if not passes_bbox(lat, lon):
            print(f"  🚫 OUTSIDE GEORGIA BBOX (lat={lat}, lon={lon}): {farm['name_en']}")
            failed += 1
            continue

        passed += 1
        fid = farm["id"]
        gmaps_url = f"https://www.google.com/maps/search/?api=1&query={lat:.5f},{lon:.5f}"
        farm["lat"] = lat
        farm["lon"] = lon
        farm["coordinates"] = {"lat": lat, "lon": lon}
        farm["google_maps_url"] = gmaps_url

        enrichment = GEORGIAN_ENRICHMENT.get(fid, {})
        style = CATEGORY_STYLES.get(farm["category"], CATEGORY_STYLES["farm_shop"])
        reg_info = REGION_NAMES.get(farm["region"], {"en": farm["region"], "ka": farm["region"]})
        address_ka = GEORGIAN_ADDRESSES.get(farm["address"], farm.get("address", ""))

        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {
                "id": fid,
                "name_en": farm["name_en"],
                "name_ka": farm.get("name_ka") or farm["name_en"],
                "region_en": reg_info["en"],
                "region_ka": reg_info["ka"],
                "region": farm["region"],
                "category": farm["category"],
                "cat_label_en": style["label_en"],
                "cat_label_ka": style["label_ka"],
                "color": style["color"],
                "emoji": style["emoji"],
                "address_en": farm["address"],
                "address_ka": address_ka,
                "phone": farm.get("phone", ""),
                "website": farm.get("website_or_social", ""),
                "google_maps_url": gmaps_url,
                "products_en": farm.get("products", []),
                "products_ka": enrichment.get("products_ka", farm.get("products", [])),
                "desc_en": farm.get("description", ""),
                "desc_ka": enrichment.get("desc_ka", farm.get("description", "")),
                "notes": farm.get("reflection_notes", "")
            }
        })
        print(f"  ✅ BBOX EVAL PASS [{farm['region']}] (lat={lat:.4f}, lon={lon:.4f}) — {farm['name_en'][:42]}")

    print(f"\nGeospatial Evaluation: {passed} PASS, {failed} FAIL")
    return features

def render_html(features):
    geojson_str = json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False, indent=2)
    regions_en = sorted(set(f["properties"]["region_en"] for f in features))
    region_names_json = json.dumps(REGION_NAMES, ensure_ascii=False)
    cat_styles_json = json.dumps(CATEGORY_STYLES, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="ka">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>🇬🇪 Nationwide Georgia Fresh Produce Directory | FarmsAround Georgia</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; display: flex; flex-direction: column; height: 100vh; overflow: hidden; color: #202124; }}

  /* ── 1. Fix Leaflet Tile Seams / White Grid Lines ── */
  .leaflet-container {{
    background: #e8eaed !important;
  }}
  .leaflet-tile {{
    outline: 1px solid transparent;
    transform-origin: 0 0;
    -webkit-backface-visibility: hidden;
    backface-visibility: hidden;
  }}
  .leaflet-tile-loaded {{
    box-shadow: 0 0 1px rgba(0, 0, 0, 0.05);
  }}
  img.leaflet-tile {{
    width: 256px !important;
    height: 256px !important;
    margin: -0.5px;
    padding: 0.5px;
  }}

  /* ── Header ── */
  #header {{
    background: linear-gradient(135deg, #1b4d1b 0%, #2e7d32 55%, #f57f17 100%);
    color: white; padding: 12px 22px;
    display: flex; align-items: center; justify-content: space-between; gap: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.3); z-index: 1000; flex-shrink: 0;
  }}
  .header-left {{ flex: 1; }}
  #header-title {{ font-size: 1.35rem; font-weight: 700; letter-spacing: -0.2px; }}
  #header-title span {{ font-weight: 300; opacity: 0.92; font-size: 1.1rem; }}
  #header-sub {{ font-size: 0.76rem; opacity: 0.88; margin-top: 3px; }}

  .header-right {{ display: flex; align-items: center; gap: 20px; }}
  .stats {{ display: flex; gap: 18px; }}
  .stat {{ text-align: center; }}
  .stat .num {{ font-size: 1.55rem; font-weight: 800; line-height: 1; }}
  .stat .lbl {{ font-size: 0.65rem; opacity: 0.85; text-transform: uppercase; letter-spacing: 0.5px; }}

  /* ── Language Switcher Pill ── */
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
    background: white; color: #1b4d1b;
    box-shadow: 0 2px 6px rgba(0,0,0,0.25);
  }}
  .lang-btn:hover:not(.active) {{
    background: rgba(255, 255, 255, 0.15);
  }}

  /* ── Layout ── */
  #main {{ display: flex; flex: 1; overflow: hidden; }}

  /* ── Sidebar ── */
  #sidebar {{
    width: 390px; min-width: 320px; background: #fafafa;
    border-right: 1px solid #e0e0e0; display: flex; flex-direction: column;
    overflow: hidden; z-index: 500;
  }}
  #controls {{ padding: 12px; background: white; border-bottom: 1px solid #e5e5e5; }}
  #search {{
    width: 100%; padding: 9px 14px; border: 1.5px solid #d0d7de; border-radius: 20px;
    font-size: 0.88rem; outline: none; margin-bottom: 9px; transition: border-color 0.2s;
  }}
  #search:focus {{ border-color: #2e7d32; box-shadow: 0 0 0 3px rgba(46,125,50,0.15); }}
  
  .filter-row {{
    display: flex; gap: 8px; margin-bottom: 9px;
  }}
  #region-select {{
    flex: 1.3; padding: 8px 12px; border: 1.5px solid #d0d7de; border-radius: 8px;
    font-size: 0.85rem; outline: none; background: white; font-weight: 500;
  }}
  .near-me-btn {{
    flex: 1; display: inline-flex; align-items: center; justify-content: center; gap: 5px;
    background: #e8f0fe; color: #1a73e8; border: 1.5px solid #a8c7fa; border-radius: 8px;
    padding: 8px 10px; font-size: 0.8rem; font-weight: 700; cursor: pointer; white-space: nowrap;
    transition: all 0.2s ease;
  }}
  .near-me-btn:hover {{ background: #d2e3fc; border-color: #1a73e8; }}
  .near-me-btn.active {{
    background: #1a73e8; color: white; border-color: #1557b0;
    box-shadow: 0 2px 6px rgba(26,115,232,0.3);
  }}
  .near-me-btn.locating {{ opacity: 0.85; cursor: wait; background: #fef3c7; color: #92400e; border-color: #fde68a; }}

  /* ── Near Me Status Bar ── */
  #near-me-status-bar {{
    background: #eff6ff; border-left: 4px solid #1a73e8; border-bottom: 1px solid #bfdbfe;
    padding: 9px 12px; font-size: 0.78rem; color: #1e3a8a; display: flex; flex-direction: column; gap: 6px;
  }}
  .status-main {{ display: flex; align-items: center; justify-content: space-between; gap: 8px; }}
  .status-text {{ font-weight: 600; line-height: 1.35; }}
  .reset-btn {{
    background: white; color: #1a73e8; border: 1px solid #bfdbfe; border-radius: 6px;
    padding: 3px 8px; font-size: 0.72rem; font-weight: 700; cursor: pointer; white-space: nowrap;
    transition: all 0.15s ease;
  }}
  .reset-btn:hover {{ background: #dbeafe; border-color: #93c5fd; }}
  .status-controls {{ display: flex; align-items: center; gap: 8px; }}
  .radius-select-label {{ font-weight: 600; color: #1e40af; font-size: 0.74rem; }}
  .radius-dropdown {{
    padding: 3px 8px; border: 1px solid #93c5fd; border-radius: 6px;
    background: white; color: #1e3a8a; font-size: 0.76rem; font-weight: 600; outline: none;
  }}

  /* ── Distance Bar & Badges on Cards and Popups ── */
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
  .draw-route-btn {{
    display: inline-flex; align-items: center; gap: 4px;
    background: #1a73e8; color: white; border: none; border-radius: 6px;
    padding: 4px 9px; font-size: 0.72rem; font-weight: 700; cursor: pointer;
    transition: background 0.18s ease;
  }}
  .draw-route-btn:hover {{ background: #1557b0; }}

  /* ── User Location Pulsing Marker & Popup ── */
  .user-pulse-marker {{ position: relative; width: 24px; height: 24px; }}
  .user-pulse-dot {{
    width: 14px; height: 14px; background: #1a73e8; border: 2.5px solid white;
    border-radius: 50%; position: absolute; top: 5px; left: 5px;
    box-shadow: 0 0 8px rgba(26,115,232,0.9); z-index: 2;
  }}
  .user-pulse-ring {{
    position: absolute; width: 34px; height: 34px; top: -5px; left: -5px;
    background: rgba(26, 115, 232, 0.45); border-radius: 50%;
    animation: userPulse 2s infinite ease-out; z-index: 1;
  }}
  @keyframes userPulse {{
    0% {{ transform: scale(0.4); opacity: 1; }}
    100% {{ transform: scale(2.2); opacity: 0; }}
  }}
  .user-popup {{ padding: 4px 2px; font-size: 0.85rem; line-height: 1.4; }}
  .user-popup-title {{ font-weight: 700; color: #1a73e8; font-size: 0.95rem; margin-bottom: 4px; }}
  .user-popup-coords {{ color: #64748b; font-size: 0.78rem; margin-bottom: 4px; }}
  .user-popup-address {{ font-size: 0.82rem; color: #334155; font-weight: 500; }}

  /* ── Route Info Floating Pill on Map ── */
  .route-info-pill {{
    position: absolute; top: 14px; left: 50%; transform: translateX(-50%);
    z-index: 1000; background: white; padding: 8px 14px; border-radius: 24px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.22); border: 1.5px solid #bfdbfe;
    display: flex; align-items: center; gap: 10px; font-size: 0.82rem;
    font-weight: 600; color: #1e3a8a; pointer-events: auto; white-space: nowrap;
    max-width: 90vw;
  }}
  .route-clear-btn {{
    background: #fee2e2; color: #b91c1c; border: none; border-radius: 50%;
    width: 20px; height: 20px; display: flex; align-items: center; justify-content: center;
    cursor: pointer; font-weight: bold; font-size: 0.75rem; transition: background 0.15s ease;
  }}
  .route-clear-btn:hover {{ background: #fca5a5; }}

  .cat-filters {{ display: flex; flex-wrap: wrap; gap: 6px; }}
  .cat-btn {{
    padding: 5px 11px; border: 2px solid #ccc; border-radius: 20px;
    font-size: 0.74rem; font-weight: 600; cursor: pointer; background: white; transition: all 0.18s;
  }}
  .cat-btn.active {{ color: white !important; }}
  .cat-btn[data-cat="all"].active          {{ background: #37474f; border-color: #37474f; }}
  .cat-btn[data-cat="farm_shop"].active    {{ background: #2d7a2d; }}
  .cat-btn[data-cat="dairy_hub"].active    {{ background: #d4a017; }}
  .cat-btn[data-cat="pick_your_own"].active {{ background: #c0392b; }}
  .cat-btn[data-cat="delivery_coop"].active {{ background: #2471a3; }}

  #farm-list {{ overflow-y: auto; flex: 1; padding: 10px 10px 20px; }}
  .farm-card {{
    background: white; padding: 12px; margin-bottom: 9px; border-radius: 10px; cursor: pointer;
    border: 1px solid #e2e8f0; transition: all 0.15s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }}
  .farm-card:hover {{ border-color: #2e7d32; box-shadow: 0 4px 10px rgba(0,0,0,0.08); transform: translateY(-1.5px); }}
  .farm-card .fc-cat {{
    font-size: 0.65rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.4px; padding: 2px 7px; border-radius: 10px;
    color: white; display: inline-block; margin-bottom: 5px;
  }}
  .farm-card .fc-name {{ font-size: 0.93rem; font-weight: 700; color: #1a202c; line-height: 1.35; }}
  .farm-card .fc-name-sec {{ font-size: 0.78rem; color: #718096; margin-top: 2px; }}
  .farm-card .fc-loc {{ font-size: 0.76rem; color: #4a5568; margin-top: 4px; display: flex; align-items: center; gap: 4px; }}
  .farm-card .fc-tags {{ margin-top: 6px; display: flex; flex-wrap: wrap; gap: 3px; }}
  .farm-card .tag {{ font-size: 0.68rem; background: #edf2f7; color: #2d3748; border-radius: 6px; padding: 2px 6px; font-weight: 500; }}
  #no-results {{ text-align: center; padding: 40px 20px; color: #a0aec0; display: none; font-size: 0.9rem; }}

  /* ── Map ── */
  #map {{ flex: 1; }}

  /* ── Popups ── */
  .popup-card {{ max-width: 310px; font-size: 0.84rem; line-height: 1.45; }}
  .popup-cat {{
    color: white; border-radius: 10px; padding: 3px 9px; font-size: 0.7rem;
    font-weight: 700; display: inline-block; margin-bottom: 6px; text-transform: uppercase;
  }}
  .popup-card h3 {{ font-size: 1.02rem; margin: 4px 0 2px; color: #1a202c; font-weight: 700; line-height: 1.35; }}
  .popup-sec {{ color: #718096; font-size: 0.8rem; margin-bottom: 6px; }}
  .popup-addr {{ color: #4a5568; margin-bottom: 4px; }}
  .popup-phone {{ margin-bottom: 4px; }}
  .popup-phone a {{ color: #2e7d32; font-weight: 700; text-decoration: none; }}
  .popup-web {{ margin-bottom: 6px; }}
  .popup-web a {{ color: #1976d2; text-decoration: none; font-weight: 600; }}
  .popup-tags {{ margin: 6px 0; display: flex; flex-wrap: wrap; gap: 3px; }}
  .popup-tags .tag {{ background: #f1f5f9; color: #334155; border-radius: 6px; padding: 2px 7px; font-size: 0.72rem; font-weight: 500; }}
  .popup-desc {{ margin-top: 6px; color: #334155; font-size: 0.81rem; line-height: 1.42; }}
  .popup-gmaps {{ margin-top: 8px; margin-bottom: 2px; }}
  .gmaps-btn {{
    display: inline-flex; align-items: center; gap: 5px;
    background: #f1f5f9; color: #1a73e8 !important;
    border: 1px solid #cbd5e1; border-radius: 6px;
    padding: 5px 11px; font-size: 0.78rem; font-weight: 700;
    text-decoration: none; transition: all 0.2s ease;
  }}
  .gmaps-btn:hover {{
    background: #e0f2fe; border-color: #38bdf8; color: #0284c7 !important;
  }}

  .fc-gmaps {{ margin-top: 8px; display: flex; }}
  .gmaps-link {{
    display: inline-flex; align-items: center; gap: 4px;
    font-size: 0.74rem; font-weight: 600; color: #1a73e8;
    background: #f8fafc; border: 1px solid #e2e8f0;
    padding: 4px 9px; border-radius: 6px; text-decoration: none;
    transition: all 0.18s ease;
  }}
  .gmaps-link:hover {{
    background: #e0f2fe; color: #0284c7; border-color: #bae6fd;
  }}
  .popup-notes {{ margin-top: 6px; padding-top: 6px; border-top: 1px dashed #e2e8f0; color: #2e7d32; font-size: 0.72rem; }}
  .leaflet-popup-content {{ min-width: 250px; }}

  /* ── Floating Mobile View Toggle Button (Hidden on Desktop) ── */
  .mobile-toggle-btn {{
    display: none;
  }}

  /* ── Responsive Mobile Styles (Screens <= 768px) ── */
  @media (max-width: 768px) {{
    #header {{
      padding: 8px 12px;
      height: 56px;
      gap: 8px;
    }}
    .header-left {{
      overflow: hidden;
    }}
    #header-title {{
      font-size: 0.98rem;
      line-height: 1.2;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      max-width: 175px;
    }}
    #header-title span {{
      display: none;
    }}
    #header-sub {{
      display: none;
    }}
    .header-right {{
      gap: 8px;
    }}
    .stats {{
      gap: 8px;
    }}
    .stats .stat:nth-child(2),
    .stats .stat:nth-child(3) {{
      display: none;
    }}
    .stat .num {{
      font-size: 1.15rem;
    }}
    .stat .lbl {{
      font-size: 0.55rem;
    }}
    .lang-switcher {{
      padding: 2px;
      gap: 1px;
    }}
    .lang-btn {{
      padding: 4px 8px;
      font-size: 0.72rem;
    }}

    /* ── Main Layout on Mobile ── */
    #main {{
      position: relative;
      flex-direction: column;
      height: calc(100vh - 56px);
      overflow: hidden;
    }}

    /* ── Mobile Sidebar (Full-View Drawer Toggleable) ── */
    #sidebar {{
      width: 100% !important;
      min-width: 100% !important;
      height: 100% !important;
      display: none;
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      z-index: 1200;
      background: #fafafa;
    }}
    #sidebar.mobile-active {{
      display: flex !important;
    }}

    /* ── Map on Mobile ── */
    #map {{
      width: 100%;
      height: 100% !important;
      flex: 1;
    }}
    #map.mobile-hidden {{
      display: none !important;
    }}

    /* ── Touch-Friendly Controls (Min 40px Tap Targets) ── */
    #controls {{
      padding: 10px;
    }}
    #search {{
      min-height: 42px;
      font-size: 0.92rem;
      margin-bottom: 8px;
      border-radius: 22px;
    }}
    .filter-row {{
      gap: 6px;
      margin-bottom: 8px;
    }}
    #region-select {{
      min-height: 42px;
      font-size: 0.88rem;
    }}
    .near-me-btn {{
      min-height: 42px;
      font-size: 0.8rem;
      padding: 6px 8px;
    }}
    .draw-route-btn {{
      min-height: 38px;
      width: 100%;
      justify-content: center;
      font-size: 0.78rem;
      margin-top: 4px;
    }}
    .route-info-pill {{
      top: 8px;
      padding: 6px 12px;
      font-size: 0.76rem;
      max-width: 95vw;
    }}

    /* ── Horizontally Scrollable Category Pills Row on Mobile ── */
    .cat-filters {{
      display: flex;
      flex-wrap: nowrap !important;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      gap: 6px;
      padding-bottom: 6px;
      margin-bottom: 2px;
    }}
    .cat-filters::-webkit-scrollbar {{
      height: 4px;
    }}
    .cat-filters::-webkit-scrollbar-thumb {{
      background: #cbd5e1;
      border-radius: 4px;
    }}
    .cat-btn {{
      flex: 0 0 auto;
      min-height: 40px;
      padding: 8px 14px;
      font-size: 0.8rem;
      white-space: nowrap;
    }}

    /* ── Mobile Touch Targets for Navigation ── */
    .gmaps-link {{
      min-height: 40px;
      width: 100%;
      justify-content: center;
      font-size: 0.84rem;
    }}
    .gmaps-btn {{
      min-height: 40px;
      width: 100%;
      justify-content: center;
      font-size: 0.84rem;
    }}

    /* ── Mobile-Friendly Leaflet Popups (Max-Width 260px) ── */
    .popup-card {{
      max-width: 250px;
      font-size: 0.8rem;
    }}
    .leaflet-popup-content {{
      min-width: 220px !important;
      margin: 10px 12px;
    }}

    /* ── Floating Toggle Button (Map / List) ── */
    .mobile-toggle-btn {{
      display: flex;
      align-items: center;
      justify-content: center;
      position: fixed;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 1500;
      background: #1b4d1b;
      color: white;
      border: 2px solid white;
      border-radius: 30px;
      padding: 10px 22px;
      font-size: 0.92rem;
      font-weight: 700;
      box-shadow: 0 4px 14px rgba(0,0,0,0.38);
      cursor: pointer;
      min-height: 44px;
      white-space: nowrap;
      transition: all 0.2s ease;
    }}
    .mobile-toggle-btn:active {{
      transform: translateX(-50%) scale(0.96);
      background: #153e15;
    }}
  }}
</style>
</head>
<body>

<div id="header">
  <div class="header-left">
    <h1 id="header-title">🇬🇪 Nationwide Georgia Fresh Produce Directory <span>| ქართული ფერმების ეროვნული კატალოგი</span></h1>
    <div id="header-sub">Modeled after FarmsAround • All 9 Regions & Tbilisi • 100% Genuine Artisanal Producers</div>
  </div>
  <div class="header-right">
    <div class="stats">
      <div class="stat"><div class="num" id="stat-total">{len(features)}</div><div class="lbl" id="stat-lbl-farms">Farms</div></div>
      <div class="stat"><div class="num" id="stat-regions">{len(regions_en)}</div><div class="lbl" id="stat-lbl-regions">Regions</div></div>
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
      <input id="search" type="text" placeholder="Search farms, products (e.g. Tenili, matsoni, tea)…"/>
      <div class="filter-row">
        <select id="region-select"></select>
        <button id="near-me-btn" class="near-me-btn" onclick="triggerNearMe()" title="Find farms near my location">
          <span id="near-me-icon">📍</span> <span id="near-me-label">ჩემთან ახლოს</span>
        </button>
      </div>
      <div class="cat-filters">
        <button id="cat-btn-all" class="cat-btn active" data-cat="all" style="border-color:#37474f;color:#37474f">🗺 All</button>
        <button id="cat-btn-farm_shop" class="cat-btn" data-cat="farm_shop" style="border-color:#2d7a2d;color:#2d7a2d">🏪 Farm Shop</button>
        <button id="cat-btn-dairy_hub" class="cat-btn" data-cat="dairy_hub" style="border-color:#d4a017;color:#d4a017">🧀 Dairy Hub</button>
        <button id="cat-btn-pick_your_own" class="cat-btn" data-cat="pick_your_own" style="border-color:#c0392b;color:#c0392b">🍓 Pick Your Own</button>
        <button id="cat-btn-delivery_coop" class="cat-btn" data-cat="delivery_coop" style="border-color:#2471a3;color:#2471a3">🚚 Delivery Coop</button>
      </div>
    </div>
    <div id="near-me-status-bar" style="display: none;">
      <div class="status-main">
        <span id="near-me-status-text" class="status-text">ნაჩვენებია ფერმები თქვენგან 25 კმ-ის რადიუსში</span>
        <button id="reset-near-me-btn" class="reset-btn" onclick="resetNearMe()">ყველას ჩვენება</button>
      </div>
      <div class="status-controls">
        <span id="radius-select-label" class="radius-select-label">რადიუსი:</span>
        <select id="radius-select" class="radius-dropdown" onchange="changeRadius(this.value)">
          <option value="10">10 კმ</option>
          <option value="25" selected>25 კმ</option>
          <option value="50">50 კმ</option>
          <option value="all">მთელი საქართველო</option>
        </select>
      </div>
    </div>
    <div id="farm-list"></div>
    <div id="no-results">No verified producers match your search criteria.</div>
  </div>
  <div id="map">
    <div id="route-info-pill" class="route-info-pill" style="display: none;"></div>
  </div>
</div>

<button id="mobile-view-toggle" class="mobile-toggle-btn" onclick="toggleMobileView()">
  <span id="mobile-toggle-text">📋 სიის ნახვა (28)</span>
</button>

<script>
const GEOJSON = {geojson_str};
const REGION_NAMES = {region_names_json};
const CATEGORY_STYLES = {cat_styles_json};

// ── Complete Bilingual Translations ────────────────────────────────────────
const I18N = {{
  en: {{
    title: "🇬🇪 Nationwide Georgia Fresh Produce Directory",
    title_sub: "| Local Farms & Artisanal Food",
    subtitle: "Modeled after FarmsAround • All 9 Regions & Tbilisi • 100% Genuine Artisanal Producers",
    farms: "Farms",
    regions: "Regions",
    categories: "Categories",
    search_placeholder: "Search farms, products (e.g. Tenili, matsoni, tea)…",
    all_regions: "All Regions",
    all_cats: "🗺 All",
    farm_shop: "🏪 Farm Shop",
    dairy_hub: "🧀 Dairy Hub",
    pick_your_own: "🍓 Pick Your Own",
    delivery_coop: "🚚 Delivery Coop",
    no_results: "No verified producers match your search criteria.",
    call: "Call",
    website: "Website / Direct Page",
    verified_badge: "Verified Producer",
    gmaps_btn: "📍 View on Google Maps",
    google_roadmap: "Google Roadmap",
    google_satellite: "Google Satellite",
    toggle_list: "📋 List View",
    toggle_map: "🗺️ Map View",
    near_me: "📍 Near Me",
    near_me_locating: "📍 Locating...",
    radius_label: "Radius:",
    radius_10: "10 km",
    radius_25: "25 km",
    radius_50: "50 km",
    radius_all: "All Georgia",
    showing_within_radius: "Showing farms within {radius} km of your location",
    fallback_closest: "No farms within {radius} km — showing {count} closest locations",
    showing_all_sorted: "Showing all farms sorted by distance from your location",
    reset_all: "Reset / Show All",
    your_location: "📍 Your Current Location",
    gps_loc: "Current GPS Location",
    draw_route: "🚗 Draw Route",
    clear_route: "Clear Route",
    geo_fallback_msg: "Geolocation unavailable or denied. Using Tbilisi center as demo."
  }},
  ka: {{
    title: "🇬🇪 საქართველოს ფერმერული პროდუქტების ეროვნული კატალოგი",
    title_sub: "| ადგილობრივი მეურნეობები",
    subtitle: "FarmsAround-ის მოდელი • ყველა რეგიონი და თბილისი • 100% ავთენტური ადგილობრივი მეურნეობები",
    farms: "მეურნეობა",
    regions: "რეგიონი",
    categories: "კატეგორია",
    search_placeholder: "მოძებნეთ ფერმები, პროდუქტები (მაგ. თენილი, მაწონი, ჩაი)...",
    all_regions: "ყველა რეგიონი",
    all_cats: "🗺 ყველა",
    farm_shop: "🏪 ფერმერული მაღაზია",
    dairy_hub: "🧀 რძის პროდუქტები",
    pick_your_own: "🍓 კრეფა / აგროტურიზმი",
    delivery_coop: "🚚 მიტანის სერვისი",
    no_results: "მითითებული ფილტრებით მეურნეობა ვერ მოიძებნა.",
    call: "დარეკვა",
    website: "ვებ-გვერდი / ბმული",
    verified_badge: "შემოწმებული მეურნეობა",
    gmaps_btn: "📍 ნახე Google Maps-ზე",
    google_roadmap: "Google რუკა",
    google_satellite: "Google თანამგზავრი",
    toggle_list: "📋 სიის ნახვა",
    toggle_map: "🗺️ რუკის ნახვა",
    near_me: "📍 ჩემთან ახლოს",
    near_me_locating: "📍 ძიება...",
    radius_label: "რადიუსი:",
    radius_10: "10 კმ",
    radius_25: "25 კმ",
    radius_50: "50 კმ",
    radius_all: "მთელი საქართველო",
    showing_within_radius: "ნაჩვენებია ფერმები თქვენგან {radius} კმ-ის რადიუსში",
    fallback_closest: "{radius} კმ-ში ფერმა ვერ მოიძებნა — ნაჩვენებია {count} უახლოესი",
    showing_all_sorted: "ნაჩვენებია ყველა ფერმა თქვენი მდებარეობიდან მანძილის მიხედვით",
    reset_all: "ყველას ჩვენება",
    your_location: "📍 თქვენი მდებარეობა",
    gps_loc: "მიმდინარე GPS ლოკაცია",
    draw_route: "🚗 მარშრუტის ჩვენება",
    clear_route: "მარშრუტის წაშლა",
    geo_fallback_msg: "გეოლოკაცია მიუწვდომელია. დემო მდებარეობად არჩეულია თბილისის ცენტრი."
  }}
}};

let currentLang = 'ka'; // Default to Georgian as requested
let userCoords = null; // {{ lat, lon, address }}
let isNearMeActive = false;
let activeRadiusKm = 25;
let userMarker = null;
let userRadiusCircle = null;
let currentRouteLayer = null;
let isFallbackClosest = false;

// ── Geodesic & Travel Time Helpers ─────────────────────────────────────────
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
  const driveMinutes = Math.max(1, Math.round((distKm / 50) * 60));
  const walkMinutes = Math.max(1, Math.round((distKm / 4.5) * 60));
  return {{ driveMinutes, walkMinutes }};
}}

function formatMinutes(mins, lang) {{
  const isKa = (lang === 'ka');
  if (mins < 60) {{
    return isKa ? `${{mins}} წთ` : `${{mins}} min`;
  }}
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  if (m === 0) {{
    return isKa ? `${{h}} სთ` : `${{h}} h`;
  }}
  return isKa ? `${{h}} სთ ${{m}} წთ` : `${{h}} h ${{m}} m`;
}}

function reverseGeocode(lat, lon, callback) {{
  const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${{lat}}&lon=${{lon}}&zoom=14&addressdetails=1`;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 2500);

  fetch(url, {{
    signal: controller.signal,
    headers: {{ 'Accept-Language': currentLang === 'ka' ? 'ka,en' : 'en' }}
  }})
    .then(r => r.json())
    .then(data => {{
      clearTimeout(timer);
      const addr = data.address || {{}};
      const place = addr.city || addr.town || addr.village || addr.suburb || addr.municipality || addr.state || '';
      const road = addr.road || addr.pedestrian || '';
      const label = [road, place].filter(Boolean).join(', ') || (data.display_name ? data.display_name.split(',').slice(0, 2).join(',') : '');
      callback(label);
    }})
    .catch(() => {{
      clearTimeout(timer);
      callback(null);
    }});
}}

// ── Map Initialization ─────────────────────────────────────────────────────
const map = L.map('map', {{
  center: [42.0, 43.6],
  zoom: 8,
  zoomControl: true
}});

// ── Google Maps Base Layers with Language Parameter (&hl=) ─────────────────
// NOTE: Google tile URLs are unofficial and not licensed for third-party use.
function getGoogleTileUrl(layerType, lang) {{
  return `https://mt{{s}}.google.com/vt/lyrs=${{layerType}}&hl=${{lang}}&x={{x}}&y={{y}}&z={{z}}`;
}}

const googleRoad = L.tileLayer(getGoogleTileUrl('m', currentLang), {{
  attribution: 'Map data © <a href="https://maps.google.com" target="_blank">Google</a>',
  subdomains: '0123',
  maxZoom: 20
}});

const googleSat = L.tileLayer(getGoogleTileUrl('y', currentLang), {{
  attribution: 'Imagery © <a href="https://maps.google.com" target="_blank">Google</a>',
  subdomains: '0123',
  maxZoom: 20
}});

googleRoad.addTo(map);

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

function updateTileLanguage(lang) {{
  googleRoad.setUrl(getGoogleTileUrl('m', lang));
  googleSat.setUrl(getGoogleTileUrl('y', lang));
  updateLayerControlLabels(lang);
}}

// ── Custom Marker Icon Factory ─────────────────────────────────────────────
function makeIcon(color, emoji) {{
  return L.divIcon({{
    className: '',
    html: `<div style="
      background:${{color}};width:34px;height:34px;border-radius:50% 50% 50% 0;
      transform:rotate(-45deg);border:3px solid white;
      box-shadow:0 3px 8px rgba(0,0,0,0.4);
      display:flex;align-items:center;justify-content:center;">
      <span style="transform:rotate(45deg);font-size:14px">${{emoji}}</span>
    </div>`,
    iconSize: [34, 34], iconAnchor: [17, 34], popupAnchor: [0, -36]
  }});
}}

// ── User Location Marker & Circle Creator ──────────────────────────────────
function createUserMarker(lat, lon, addressText) {{
  const pulseIcon = L.divIcon({{
    className: 'user-location-marker-container',
    html: `
      <div class="user-pulse-marker">
        <div class="user-pulse-ring"></div>
        <div class="user-pulse-dot"></div>
      </div>
    `,
    iconSize: [24, 24],
    iconAnchor: [12, 12],
    popupAnchor: [0, -14]
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
    color: '#1a73e8',
    weight: 2,
    opacity: 0.75,
    fillColor: '#38bdf8',
    fillOpacity: 0.12,
    dashArray: '6, 6'
  }}).addTo(map);
}}

// ── Dynamic Bilingual Popup Builder ────────────────────────────────────────
function buildPopupHtml(p, lang, lat, lon) {{
  const isKa = (lang === 'ka');
  const nameMain = isKa ? p.name_ka : p.name_en;
  const nameSec = isKa ? p.name_en : p.name_ka;
  const catLabel = isKa ? p.cat_label_ka : p.cat_label_en;
  const regName = isKa ? p.region_ka : p.region_en;
  const addr = isKa ? p.address_ka : p.address_en;
  const desc = isKa ? p.desc_ka : p.desc_en;
  const prods = isKa ? p.products_ka : p.products_en;
  const tagsHtml = (prods || []).slice(0, 6).map(t => `<span class="tag">${{t}}</span>`).join('');

  let phoneHtml = '';
  if (p.phone) {{
    const clean = p.phone.replace(/\\s/g, '');
    phoneHtml = `<p class="popup-phone">📞 <a href="tel:${{clean}}">${{p.phone}}</a></p>`;
  }}

  let webHtml = '';
  if (p.website) {{
    webHtml = `<p class="popup-web">🌐 <a href="${{p.website}}" target="_blank" rel="noopener">${{I18N[lang].website}}</a></p>`;
  }}

  let gmapsHtml = '';
  if (p.google_maps_url) {{
    gmapsHtml = `<div class="popup-gmaps"><a href="${{p.google_maps_url}}" target="_blank" rel="noopener" class="gmaps-btn">${{I18N[lang].gmaps_btn}}</a></div>`;
  }}

  let distHtml = '';
  if (userCoords && lat !== undefined && lon !== undefined) {{
    const d = getDistanceKm(userCoords.lat, userCoords.lon, lat, lon);
    const times = calculateTravelTimes(d);
    const driveStr = formatMinutes(times.driveMinutes, lang);
    const walkStr = formatMinutes(times.walkMinutes, lang);
    const dUnit = (lang === 'ka' ? 'კმ' : 'km');
    const safeName = nameMain.replace(/'/g, "\\'");
    distHtml = `
      <div class="popup-distance-bar">
        <span class="dist-badge dist-km">📏 ${{d.toFixed(1)}} ${{dUnit}}</span>
        <span class="dist-badge dist-drive">🚗 ${{driveStr}}</span>
        <span class="dist-badge dist-walk">🚶 ${{walkStr}}</span>
        <button class="draw-route-btn" onclick="drawRouteTo(event, ${{lat}}, ${{lon}}, '${{safeName}}')">${{I18N[lang].draw_route}}</button>
      </div>
    `;
  }}

  return `
    <div class="popup-card">
      <div class="popup-cat" style="background:${{p.color}}">${{p.emoji}} ${{catLabel}}</div>
      <h3>${{nameMain}}</h3>
      <div class="popup-sec">${{nameSec}}</div>
      <p class="popup-addr">📍 <strong>${{regName}}</strong>: ${{addr}}</p>
      ${{phoneHtml}}
      ${{webHtml}}
      ${{distHtml}}
      ${{gmapsHtml}}
      <div class="popup-tags">${{tagsHtml}}</div>
      <p class="popup-desc">${{desc}}</p>
      <p class="popup-notes"><em>✅ ${{I18N[lang].verified_badge}}</em></p>
    </div>
  `;
}}

// ── Plotted Markers Collection ─────────────────────────────────────────────
const getPopupMaxWidth = () => (window.innerWidth <= 768 ? 260 : 320);
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

// ── Sidebar Builder ────────────────────────────────────────────────────────
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
    const regName = isKa ? p.region_ka : p.region_en;
    const addr = isKa ? p.address_ka : p.address_en;
    const prods = isKa ? p.products_ka : p.products_en;
    const tags = (prods || []).slice(0, 4).map(t => `<span class="tag">${{t}}</span>`).join('');

    let gmapsCardHtml = '';
    if (p.google_maps_url) {{
      gmapsCardHtml = `<div class="fc-gmaps"><a href="${{p.google_maps_url}}" target="_blank" rel="noopener" class="gmaps-link" onclick="event.stopPropagation();">${{I18N[lang].gmaps_btn}}</a></div>`;
    }}

    let distCardHtml = '';
    if (userCoords) {{
      const d = getDistanceKm(userCoords.lat, userCoords.lon, lat, lon);
      const times = calculateTravelTimes(d);
      const driveStr = formatMinutes(times.driveMinutes, lang);
      const walkStr = formatMinutes(times.walkMinutes, lang);
      const dUnit = (lang === 'ka' ? 'კმ' : 'km');
      const safeName = nameMain.replace(/'/g, "\\'");
      distCardHtml = `
        <div class="fc-distance-bar" onclick="event.stopPropagation();">
          <span class="dist-badge dist-km">📏 ${{d.toFixed(1)}} ${{dUnit}}</span>
          <span class="dist-badge dist-drive">🚗 ${{driveStr}}</span>
          <span class="dist-badge dist-walk">🚶 ${{walkStr}}</span>
          <button class="draw-route-btn" onclick="drawRouteTo(event, ${{lat}}, ${{lon}}, '${{safeName}}')">${{I18N[lang].draw_route}}</button>
        </div>
      `;
    }}

    const card = document.createElement('div');
    card.className = 'farm-card';
    card.innerHTML = `
      <span class="fc-cat" style="background:${{p.color}}">${{p.emoji}} ${{catLabel}}</span>
      <div class="fc-name">${{nameMain}}</div>
      <div class="fc-name-sec">${{nameSec}}</div>
      <div class="fc-loc">📍 <strong>${{regName}}</strong> • ${{addr.split(',')[0]}}</div>
      <div class="fc-tags">${{tags}}</div>
      ${{distCardHtml}}
      ${{gmapsCardHtml}}
    `;
    card.addEventListener('click', () => {{
      if (window.innerWidth <= 768) {{
        setMobileView('map');
      }}
      map.flyTo([lat, lon], 13, {{ duration: 1.2 }});
      markers.forEach(m => {{
        if (m.featureProps.id === p.id) {{
          setTimeout(() => m.openPopup(), 600);
        }}
      }});
    }});
    list.appendChild(card);
  }});
}}

// ── Region Dropdown Builder ────────────────────────────────────────────────
const regionsList = Object.keys(REGION_NAMES);

function populateRegionSelect(lang) {{
  const sel = document.getElementById('region-select');
  const prevVal = sel.value;
  sel.innerHTML = `<option value="">${{I18N[lang].all_regions}} (${{regionsList.length}})</option>`;
  regionsList.forEach(rKey => {{
    const rName = REGION_NAMES[rKey][lang];
    const opt = document.createElement('option');
    opt.value = rKey;
    opt.textContent = rName;
    if (rKey === prevVal) opt.selected = true;
    sel.appendChild(opt);
  }});
}}

// ── Mobile View Toggle Controller ──────────────────────────────────────────
let currentMobileView = 'map';

function updateMobileToggleBtn() {{
  const btnText = document.getElementById('mobile-toggle-text');
  if (!btnText) return;
  const count = document.getElementById('stat-total').textContent || '28';
  if (currentMobileView === 'list') {{
    btnText.textContent = I18N[currentLang].toggle_map;
  }} else {{
    btnText.textContent = `${{I18N[currentLang].toggle_list}} (${{count}})`;
  }}
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
    setTimeout(() => {{ map.invalidateSize(); }}, 150);
  }}
  updateMobileToggleBtn();
}}

function toggleMobileView() {{
  setMobileView(currentMobileView === 'map' ? 'list' : 'map');
}}

window.addEventListener('resize', () => {{
  const sidebar = document.getElementById('sidebar');
  const mapElem = document.getElementById('map');
  if (window.innerWidth > 768) {{
    sidebar.classList.remove('mobile-active');
    mapElem.classList.remove('mobile-hidden');
  }} else {{
    setMobileView(currentMobileView);
  }}
  map.invalidateSize();
}});

// ── Near Me & Geolocation Controllers ──────────────────────────────────────
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

    reverseGeocode(lat, lon, (placeLabel) => {{
      if (placeLabel && userCoords) {{
        userCoords.address = placeLabel;
        const addrEl = document.getElementById('user-popup-address');
        if (addrEl) addrEl.textContent = placeLabel;
      }}
    }});

    updateAllMarkersPopups();
    applyFilters();
  }}

  function onLocationError(err) {{
    btn.classList.remove('locating');
    console.warn('Geolocation failed or denied, using Tbilisi fallback:', err);
    alert(I18N[currentLang].geo_fallback_msg);
    onLocationFound(41.7151, 44.7871);
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
  if (userCoords) {{
    updateUserRadiusCircle(userCoords.lat, userCoords.lon, activeRadiusKm);
  }}
  applyFilters();
}}

function resetNearMe() {{
  isNearMeActive = false;
  activeRadiusKm = 25;
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
  clearCurrentRoute();
  document.getElementById('near-me-status-bar').style.display = 'none';
  document.getElementById('radius-select').value = '25';
  updateAllMarkersPopups();
  applyFilters();
  const allMarkersGroup = L.featureGroup(markers);
  map.fitBounds(allMarkersGroup.getBounds().pad(0.1));
}}

function clearCurrentRoute() {{
  if (currentRouteLayer && map.hasLayer(currentRouteLayer)) {{
    map.removeLayer(currentRouteLayer);
    currentRouteLayer = null;
  }}
  const pill = document.getElementById('route-info-pill');
  if (pill) pill.style.display = 'none';
}}

function drawRouteTo(event, farmLat, farmLon, farmName) {{
  if (event) event.stopPropagation();
  if (!userCoords) {{
    alert(currentLang === 'ka' ? 'გთხოვთ ჯერ ჩართოთ "ჩემთან ახლოს"' : 'Please activate "Near Me" first');
    triggerNearMe();
    return;
  }}
  clearCurrentRoute();

  const [uLat, uLon] = [userCoords.lat, userCoords.lon];
  const distKm = getDistanceKm(uLat, uLon, farmLat, farmLon);
  const times = calculateTravelTimes(distKm);

  function showRoutePill(distanceDisplay, minutesDisplay) {{
    let pill = document.getElementById('route-info-pill');
    if (!pill) return;
    const driveStr = formatMinutes(minutesDisplay, currentLang);
    const distUnit = (currentLang === 'ka' ? 'კმ' : 'km');
    pill.innerHTML = `
      <span>🚗 <strong>${{farmName}}</strong> • ${{distanceDisplay}} ${{distUnit}} (~${{driveStr}})</span>
      <button class="route-clear-btn" onclick="clearCurrentRoute()" title="${{I18N[currentLang].clear_route}}">✕</button>
    `;
    pill.style.display = 'flex';
  }}

  function drawFallbackPolyline() {{
    const line = L.polyline([[uLat, uLon], [farmLat, farmLon]], {{
      color: '#2563eb',
      weight: 4,
      opacity: 0.9,
      dashArray: '8, 8'
    }});
    currentRouteLayer = L.featureGroup([line]).addTo(map);
    map.fitBounds(currentRouteLayer.getBounds().pad(0.2));
    showRoutePill(distKm.toFixed(1), times.driveMinutes);
    if (window.innerWidth <= 768) setMobileView('map');
  }}

  const osrmUrl = `https://router.project-osrm.org/route/v1/driving/${{uLon}},${{uLat}};${{farmLon}},${{farmLat}}?overview=full&geometries=geojson`;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 3500);

  fetch(osrmUrl, {{ signal: controller.signal }})
    .then(r => r.json())
    .then(data => {{
      clearTimeout(timer);
      if (data.routes && data.routes[0]) {{
        const geom = data.routes[0].geometry;
        const latlngs = geom.coordinates.map(c => [c[1], c[0]]);
        const roadDistKm = (data.routes[0].distance / 1000).toFixed(1);
        const roadMin = Math.round(data.routes[0].duration / 60);

        const casing = L.polyline(latlngs, {{ color: '#0d47a1', weight: 7, opacity: 0.45, lineCap: 'round', lineJoin: 'round' }});
        const core = L.polyline(latlngs, {{ color: '#2563eb', weight: 4.5, opacity: 0.95, lineCap: 'round', lineJoin: 'round' }});
        currentRouteLayer = L.featureGroup([casing, core]).addTo(map);
        map.fitBounds(currentRouteLayer.getBounds().pad(0.18));
        showRoutePill(roadDistKm, roadMin);
        if (window.innerWidth <= 768) setMobileView('map');
      }} else {{
        drawFallbackPolyline();
      }}
    }})
    .catch(() => {{
      clearTimeout(timer);
      drawFallbackPolyline();
    }});
}}

// ── Filtering Logic ────────────────────────────────────────────────────────
let activeCat = 'all';
let activeRegion = '';
let searchText = '';

function applyFilters() {{
  const q = searchText.toLowerCase().trim();
  const isKa = (currentLang === 'ka');

  let candidateFeatures = GEOJSON.features.slice();

  // If Near Me is active, calculate distances and handle radius filtering
  if (isNearMeActive && userCoords) {{
    document.getElementById('near-me-status-bar').style.display = 'flex';

    const withDist = candidateFeatures.map(f => {{
      const [lon, lat] = f.geometry.coordinates;
      const dist = getDistanceKm(userCoords.lat, userCoords.lon, lat, lon);
      return {{ f, dist }};
    }});

    // Sort by distance ascending
    withDist.sort((a, b) => a.dist - b.dist);

    if (activeRadiusKm === 'all') {{
      candidateFeatures = withDist.map(item => item.f);
      isFallbackClosest = false;
      document.getElementById('near-me-status-text').textContent = I18N[currentLang].showing_all_sorted;
    }} else {{
      const inRadius = withDist.filter(item => item.dist <= activeRadiusKm);
      if (inRadius.length < 2) {{
        candidateFeatures = withDist.slice(0, 5).map(item => item.f);
        isFallbackClosest = true;
        document.getElementById('near-me-status-text').textContent =
          I18N[currentLang].fallback_closest
            .replace('{radius}', activeRadiusKm)
            .replace('{count}', candidateFeatures.length);
      }} else {{
        candidateFeatures = inRadius.map(item => item.f);
        isFallbackClosest = false;
        document.getElementById('near-me-status-text').textContent =
          I18N[currentLang].showing_within_radius
            .replace('{radius}', activeRadiusKm);
      }}
    }}
  }} else {{
    document.getElementById('near-me-status-bar').style.display = 'none';
  }}

  const filtered = candidateFeatures.filter(f => {{
    const p = f.properties;
    const matchCat = activeCat === 'all' || p.category === activeCat;
    const matchRegion = !activeRegion || p.region === activeRegion;

    const prodsAll = (p.products_en || []).concat(p.products_ka || []).join(' ').toLowerCase();
    const matchSearch = !q ||
      p.name_en.toLowerCase().includes(q) ||
      p.name_ka.toLowerCase().includes(q) ||
      p.region_en.toLowerCase().includes(q) ||
      p.region_ka.toLowerCase().includes(q) ||
      p.address_en.toLowerCase().includes(q) ||
      p.address_ka.toLowerCase().includes(q) ||
      prodsAll.includes(q);

    return matchCat && matchRegion && matchSearch;
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
    if (boundsGroup.length > 0) {{
      const group = L.featureGroup(boundsGroup);
      map.fitBounds(group.getBounds().pad(0.12));
    }}
  }} else if (filtered.length > 0) {{
    const group = L.featureGroup(markers.filter(m => visibleIds.has(m.featureProps.id)));
    map.fitBounds(group.getBounds().pad(0.12));
  }}
}}

// ── Switch Language Controller ─────────────────────────────────────────────
function switchLanguage(lang) {{
  currentLang = lang;
  const isKa = (lang === 'ka');

  // Toggle active button
  document.getElementById('lang-btn-ka').classList.toggle('active', isKa);
  document.getElementById('lang-btn-en').classList.toggle('active', !isKa);

  // Update Header
  document.getElementById('header-title').innerHTML = `${{I18N[lang].title}} <span>${{I18N[lang].title_sub}}</span>`;
  document.getElementById('header-sub').textContent = I18N[lang].subtitle;

  // Update Stat Labels
  document.getElementById('stat-lbl-farms').textContent = I18N[lang].farms;
  document.getElementById('stat-lbl-regions').textContent = I18N[lang].regions;
  document.getElementById('stat-lbl-categories').textContent = I18N[lang].categories;

  // Update Search input
  document.getElementById('search').placeholder = I18N[lang].search_placeholder;
  document.getElementById('no-results').textContent = I18N[lang].no_results;

  // Update Category buttons
  document.getElementById('cat-btn-all').textContent = I18N[lang].all_cats;
  document.getElementById('cat-btn-farm_shop').textContent = I18N[lang].farm_shop;
  document.getElementById('cat-btn-dairy_hub').textContent = I18N[lang].dairy_hub;
  document.getElementById('cat-btn-pick_your_own').textContent = I18N[lang].pick_your_own;
  document.getElementById('cat-btn-delivery_coop').textContent = I18N[lang].delivery_coop;

  // Update Near Me & Radius Labels
  const nearMeLbl = document.getElementById('near-me-label');
  if (nearMeLbl) nearMeLbl.textContent = I18N[lang].near_me;
  const resetBtn = document.getElementById('reset-near-me-btn');
  if (resetBtn) resetBtn.textContent = I18N[lang].reset_all;
  const radLbl = document.getElementById('radius-select-label');
  if (radLbl) radLbl.textContent = I18N[lang].radius_label;
  const radSelect = document.getElementById('radius-select');
  if (radSelect) {{
    radSelect.options[0].textContent = I18N[lang].radius_10;
    radSelect.options[1].textContent = I18N[lang].radius_25;
    radSelect.options[2].textContent = I18N[lang].radius_50;
    radSelect.options[3].textContent = I18N[lang].radius_all;
  }}

  // Update User Marker popup if present
  if (userMarker && userCoords) {{
    const addrLabel = userCoords.address || (lang === 'ka' ? 'მიმდინარე GPS ლოკაცია' : 'Current GPS Location');
    const userPopupHtml = `
      <div class="user-popup">
        <div class="user-popup-title">${{I18N[lang].your_location}}</div>
        <div class="user-popup-coords"><code>${{userCoords.lat.toFixed(4)}}° N, ${{userCoords.lon.toFixed(4)}}° E</code></div>
        <div id="user-popup-address" class="user-popup-address">${{addrLabel}}</div>
      </div>
    `;
    const wasOpen = userMarker.isPopupOpen();
    userMarker.bindPopup(userPopupHtml, {{ maxWidth: getPopupMaxWidth() }});
    if (wasOpen) userMarker.openPopup();
  }}

  // Update Region dropdown
  populateRegionSelect(lang);

  // Update Google tile language
  updateTileLanguage(lang);

  // Re-bind all marker popups in active language
  updateAllMarkersPopups();

  // Re-render sidebar and update mobile toggle button
  applyFilters();
  updateMobileToggleBtn();
}}

// ── Event Listeners ────────────────────────────────────────────────────────
document.querySelectorAll('.cat-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeCat = btn.dataset.cat;
    applyFilters();
  }});
}});

document.getElementById('region-select').addEventListener('change', e => {{
  activeRegion = e.target.value;
  applyFilters();
}});

document.getElementById('search').addEventListener('input', e => {{
  searchText = e.target.value;
  applyFilters();
}});

// ── Initial Setup ──────────────────────────────────────────────────────────
populateRegionSelect(currentLang);
switchLanguage('ka'); // Set initial view to Georgian

const allMarkersGroup = L.featureGroup(markers);
map.fitBounds(allMarkersGroup.getBounds().pad(0.1));
</script>
</body>
</html>"""

def main():
    with open(VERIFIED_PATH, "r", encoding="utf-8") as f:
        farms = json.load(f)

    print(f"\n🗺  Map Publisher — Geocoding & Upgrading Leaflet UI for {len(farms)} verified farms\n{'─'*70}")
    features = build_features(farms)

    regions = sorted(set(f["properties"]["region"] for f in features))
    html_content = render_html(features)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Persist updated coordinates and Google Maps URLs into verified_farms.json
    with open(VERIFIED_PATH, "w", encoding="utf-8") as f:
        json.dump(farms, f, ensure_ascii=False, indent=2)

    print(f"\n{'─'*70}")
    print(f"✅ Interactive Nationwide Leaflet Map Generated: {OUTPUT_PATH}")
    print(f"✅ Verified Farms Updated with Coordinates & Google Maps Links: {VERIFIED_PATH}")
    print(f"   Farms plotted: {len(features)}")
    print(f"   Regions covered ({len(regions)}): {', '.join(regions)}")
    print(f"   Map URL: file://{os.path.abspath(OUTPUT_PATH)}")

if __name__ == "__main__":
    main()
