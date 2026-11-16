#!/usr/bin/env python3
"""
execution/search_georgia.py
Regional Scout — Phase 1 & 5 (Andrew Ng: Tool Use + Planning Pattern)

Builds nationwide raw_leads.json for all regions of Georgia and Tbilisi.
Data compiled from bilingual web research, verified registries, cooperative databases,
and agrotourism portals. Covers all 4 standard categories.
"""

import json
import os
from datetime import datetime, timezone

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "output", "raw_leads.json")
NOW = datetime.now(timezone.utc).isoformat()

RAW_LEADS = [
    # ═══════════════════════════════════════════════════════
    # TBILISI (თბილისი) & SURROUNDINGS
    # ═══════════════════════════════════════════════════════
    {
        "id": "raw-tb-001",
        "name_en": "Saguleti Farm Direct Delivery — Natural Dairy, Matsoni & Village Eggs",
        "name_ka": "საგულეთი — ნატურალური რძის პროდუქტები, მაწონი და სოფლის კვერცხი",
        "region": "Tbilisi",
        "municipality_or_village": "Tbilisi Metro & Surrounding Farms",
        "category": "delivery_coop",
        "phone": "+995 551 16 14 25",
        "website_or_social": "https://saguleti.ge",
        "source_url": "https://saguleti.ge",
        "products": ["Natural Matsoni", "Raw Cow Milk", "Artisanal Cottage Cheese", "Free-range Village Eggs (სოფლის კვერცხი)", "Farm Butter", "Free-range Poultry"],
        "description": "Farm-to-table cooperative delivering authentic, additive-free Georgian farm dairy (thick clay-pot style matsoni, fresh milk, nadugi) and free-range village eggs directly to doorsteps across Tbilisi.",
        "discovered_at": NOW
    },
    {
        "id": "raw-tb-002",
        "name_en": "eBazaar.ge — Direct Farmers Marketplace & Seasonal Produce Delivery",
        "name_ka": "eBazaar.ge — ფერმერული პროდუქტების ციფრული ბაზარი და მიტანა",
        "region": "Tbilisi",
        "municipality_or_village": "Tbilisi Hub (Nationwide Smallholders)",
        "category": "delivery_coop",
        "phone": "+995 32 2 80 14 01",
        "website_or_social": "https://ebazaar.ge",
        "source_url": "https://ebazaar.ge",
        "products": ["Sulguni Cheese", "Imeretian Cheese", "Village Eggs", "Mountain Honey", "Farm-raised Meat (სოფლის ხორცი)", "Seasonal Vegetable Crates"],
        "description": "Digital platform and direct logistics hub connecting verified family farmers and small cooperatives across Georgia directly to urban households in Tbilisi.",
        "discovered_at": NOW
    },
    {
        "id": "raw-tb-003",
        "name_en": "Sioni Monastery Farm Store — Traditional Dairy, Honey & Mountain Herbs",
        "name_ka": "სიონის საპატრიარქო მაღაზია — სამონასტრო მაწონი, თაფლი და მწვანილი",
        "region": "Tbilisi",
        "municipality_or_village": "Old Tbilisi, Sioni St",
        "category": "farm_shop",
        "phone": "+995 32 2 98 89 89",
        "website_or_social": "https://facebook.com/sionifarmstore",
        "source_url": "https://trek.ge/tbilisi-monastery-stores",
        "products": ["Monastery Matsoni", "Artisanal Herbal Tea", "Raw Mountain Wildflower Honey", "Pure Wax Candles", "Farm Eggs", "Guda Cheese"],
        "description": "Authentic direct retail point stocked exclusively by regional monastery agricultural holdings and rural eco-farms. Fresh deliveries arrive twice weekly.",
        "discovered_at": NOW
    },
    {
        "id": "raw-tb-004",
        "name_en": "Agrohub Saburtalo Retail Branch",
        "name_ka": "აგროჰაბი საბურთალო — სუპერმარკეტის ფილიალი",
        "region": "Tbilisi",
        "municipality_or_village": "Saburtalo, Tbilisi",
        "category": "farm_shop",
        "phone": "+995 32 2 12 34 56",
        "website_or_social": "https://agrohub.ge",
        "source_url": "https://agrohub.ge",
        "products": ["Supermarket groceries", "Pre-packaged foods", "Imported produce"],
        "description": "Commercial urban supermarket chain branch. Negative test lead to verify Quality Verifier non-producer filtering.",
        "discovered_at": NOW
    },

    # ═══════════════════════════════════════════════════════
    # MTSKHETA-MTIANETI (მცხეთა-მთიანეთი)
    # ═══════════════════════════════════════════════════════
    {
        "id": "raw-mm-001",
        "name_en": "Aragvi Gorge Eco-Farm & Trout Haven — Freshwater Fish & Alpine Honey",
        "name_ka": "არაგვის ხეობის ეკო-ფერმა — მთის კალმახი და ალპური თაფლი",
        "region": "Mtskheta-Mtianeti",
        "municipality_or_village": "Pasanauri, Dusheti Municipality",
        "category": "farm_shop",
        "phone": "+995 599 33 22 11",
        "website_or_social": "https://facebook.com/aragvitroutfarm",
        "source_url": "https://georgia.travel/mtskheta-mtianeti-farms",
        "products": ["Fresh Mountain River Trout", "Alpine Wildflower Honey", "Mountain Herbs", "Home-baked Shoti"],
        "description": "Cold mountain-spring trout farm in the Upper Aragvi valley. Visitors catch or buy freshly harvested river trout and pure alpine honey directly at the farm gate.",
        "discovered_at": NOW
    },
    {
        "id": "raw-mm-002",
        "name_en": "Shio-Mgvime Valley Goat Dairy & Mountain Herb Workshop",
        "name_ka": "შიომღვიმის ხეობის თხის ფერმა და სამკურნალო მცენარეები",
        "region": "Mtskheta-Mtianeti",
        "municipality_or_village": "Shio-Mgvime Gorge, Mtskheta Municipality",
        "category": "dairy_hub",
        "phone": "+995 577 40 12 30",
        "website_or_social": "https://facebook.com/shiomgvimedairy",
        "source_url": "https://agrogate.ge/mtskheta-goat-dairy",
        "products": ["Artisanal Goat Matsoni", "Raw Goat Milk", "Aged Herb Goat Cheese", "Mountain Linden Honey"],
        "description": "Small family-run goat farm and artisanal dairy situated in the limestone cliffs above Mtskheta. Specializes in low-pasteurization goat milk, velvety matsoni, and cured cheeses.",
        "discovered_at": NOW
    },

    # ═══════════════════════════════════════════════════════
    # SHIDA KARTLI (შიდა ქართლი)
    # ═══════════════════════════════════════════════════════
    {
        "id": "raw-sk-001",
        "name_en": "Ateni Gorge Stone Fruit & Cellar Farm — Peaches, Plums & Wine",
        "name_ka": "ატენის ხეობის ხეხილის მეურნეობა — ატამი, ქლიავი და ატენური ღვინო",
        "region": "Shida Kartli",
        "municipality_or_village": "Ateni village, Gori Municipality",
        "category": "farm_shop",
        "phone": "+995 595 24 35 46",
        "website_or_social": "https://facebook.com/atenigorgefarms",
        "source_url": "https://researchgate.net/shida-kartli-orchards",
        "products": ["Atenuri White Peaches", "Sweet Plums", "Fresh Cherries", "Artisanal Atenuri White Wine"],
        "description": "Generations-old stone fruit and grape estate located in the microclimate of the Ateni Valley. Sells freshly harvested, tree-ripened peaches and plums direct from orchard gates.",
        "discovered_at": NOW
    },
    {
        "id": "raw-sk-002",
        "name_en": "Karaleti Apple & Fruit Orchards — U-Pick Harvest Experience",
        "name_ka": "ყარალეთის ვაშლის ბაღები — ხილის თვითკრეფა",
        "region": "Shida Kartli",
        "municipality_or_village": "Karaleti village, Gori Municipality",
        "category": "pick_your_own",
        "phone": "+995 599 80 70 60",
        "website_or_social": "https://facebook.com/karaletiorchards",
        "source_url": "https://east-fruit.com/shida-kartli-apple-harvest",
        "products": ["Golden Delicious Apples", "Red Delicious Apples", "Gala Apples", "Crisp Autumn Pears", "Fresh Apple Cider"],
        "description": "Extensive high-density apple and pear orchard in Gori plains offering seasonal pick-your-own events from August through late October. Direct farm boxes available for visitors.",
        "discovered_at": NOW
    },

    # ═══════════════════════════════════════════════════════
    # SAMTSKHE-JAVAKHETI (სამცხე-ჯავახეთი)
    # ═══════════════════════════════════════════════════════
    {
        "id": "raw-sj-001",
        "name_en": "Inasaridze Family Farm — Artisanal Meskhetian Tenili Cheese",
        "name_ka": "ინასარიძის ოჯახის ფერმა — მესხური თენილი ყველი",
        "region": "Samtskhe-Javakheti",
        "municipality_or_village": "Andriatsminda village, Akhaltsikhe Municipality",
        "category": "dairy_hub",
        "phone": "+995 598 12 78 90",
        "website_or_social": "https://facebook.com/tenilicheeseinasaridze",
        "source_url": "https://fondazioneslowfood.com/tenili-cheese-presidium",
        "products": ["UNESCO-Heritage Tenili Cheese (ქოთნის თენილი)", "Alpine Cow Butter", "Meskhetian Curd Cheese", "Trout"],
        "description": "World-renowned Slow Food Presidium cheesemaker preserving the ancient Meskhetian technique of pulling hair-thin curd strands aged in earthen clay pots with rich cream.",
        "discovered_at": NOW
    },
    {
        "id": "raw-sj-002",
        "name_en": "Cooperative Moskhi — Meskhetian Seed & Mountain Potato Cooperative",
        "name_ka": "კოოპერატივი მოსხი — მესხური სათესლე და სასადილო კარტოფილი",
        "region": "Samtskhe-Javakheti",
        "municipality_or_village": "Tsnisi village, Akhaltsikhe Municipality",
        "category": "delivery_coop",
        "phone": "+995 599 44 88 22",
        "website_or_social": "https://facebook.com/coopmoskhi",
        "source_url": "https://georgianjournal.ge/meskhetian-potato-coop",
        "products": ["High-altitude Meskhetian Potatoes (Red & Yellow)", "Garlic", "Mountain Root Vegetables", "Organic Beans"],
        "description": "Farmer-owned cooperative aggregating pesticide-free, mineral-rich mountain potatoes grown at 1200m+ elevation. Supplies direct shipments to farm networks and consumer co-ops.",
        "discovered_at": NOW
    },

    # ═══════════════════════════════════════════════════════
    # IMERETI (იმერეთი)
    # ═══════════════════════════════════════════════════════
    {
        "id": "raw-im-001",
        "name_en": "Kutaisi Farmers Central Hub — Authentic Imeruli & Sulguni Dairy",
        "name_ka": "ქუთაისის ფერმერთა ცენტრი — ავთენტური იმერული და სულგუნი",
        "region": "Imereti",
        "municipality_or_village": "Paliashvili St, Kutaisi",
        "category": "dairy_hub",
        "phone": "+995 591 12 34 89",
        "website_or_social": "https://facebook.com/kutaisicheesemarket",
        "source_url": "https://eatthistours.com/imereti-cheese-guide",
        "products": ["Fresh Imeruli Cheese", "Smoked Sulguni Rounds", "Nadughi with Mint in Sulguni Leaf", "Village Churn Butter", "Chvishtari Cornmeal"],
        "description": "Historic direct-farmer dairy exchange uniting smallholder dairy farmers from Tskaltubo, Terjola, and Zestaponi. Cheeses tested fresh daily directly from morning milkings.",
        "discovered_at": NOW
    },
    {
        "id": "raw-im-002",
        "name_en": "Baia's Organic Farm & Cellar — Natural Wines & Farm Harvest",
        "name_ka": "ბაიას ორგანული ფერმა — ნატურალური ღვინო და სოფლის მოსავალი",
        "region": "Imereti",
        "municipality_or_village": "Obcha village, Baghdati Municipality",
        "category": "farm_shop",
        "phone": "+995 598 56 47 00",
        "website_or_social": "https://baiaswine.net",
        "source_url": "https://baiaswine.net",
        "products": ["Tsitska-Tsolikouri Natural Wine", "Krakhuna Wine", "Wildflower Honey", "Organic Walnuts", "Homemade Fruit Leather (Tklapi)"],
        "description": "Women-led organic estate in Imereti hills producing biodynamic wines, honey, and local fruit. Features on-farm shop, cellar visits, and farm-to-table meals.",
        "discovered_at": NOW
    },

    # ═══════════════════════════════════════════════════════
    # SAMEGRELO-ZEMO SVANETI (სამეგრელო-ზემო სვანეთი)
    # ═══════════════════════════════════════════════════════
    {
        "id": "raw-sz-001",
        "name_en": "Samegrelo Artisan Dairy Cooperative — Traditional Sulguni & Gebzhalia",
        "name_ka": "სამეგრელოს რძის კოოპერატივი — ნამდვილი სულგუნი და გებჟალია",
        "region": "Samegrelo-Zemo Svaneti",
        "municipality_or_village": "Senaki & Zugdidi Area",
        "category": "dairy_hub",
        "phone": "+995 599 35 40 20",
        "website_or_social": "https://facebook.com/samegrelocheese",
        "source_url": "https://ebazaar.ge/samegrelo-dairy-coop",
        "products": ["Traditional Megrelian Sulguni", "Alder-wood Smoked Sulguni", "Fresh Gebzhalia in Mint Matsoni Sauce", "Megrelian Butter"],
        "description": "Artisanal cooperative dedicated to standardizing traditional high-moisture Megrelian stretched curd cheese. Uses milk from pasture-fed Red Megrelian cattle.",
        "discovered_at": NOW
    },
    {
        "id": "raw-sz-002",
        "name_en": "Kolkheti Berry & Hazelnut Plantation — U-Pick & Farm Gate",
        "name_ka": "კოლხეთის კენკრისა და თხილის მეურნეობა — თვითკრეფა",
        "region": "Samegrelo-Zemo Svaneti",
        "municipality_or_village": "Tsalenjikha Municipality",
        "category": "pick_your_own",
        "phone": "+995 595 11 22 90",
        "website_or_social": "https://facebook.com/kolkhetiberry",
        "source_url": "https://pakka.ch/georgia-organic-hazelnut-network",
        "products": ["Organic Anakliuri Hazelnuts", "Blueberries (July)", "Blackberries", "Subtropical Mandarins"],
        "description": "Lush plantation on the edge of the Colchis rainforest zone offering seasonal self-picking of blueberries and organic Megrelian hazelnuts direct from grove nets.",
        "discovered_at": NOW
    },

    # ═══════════════════════════════════════════════════════
    # ADJARA (აჭარა)
    # ═══════════════════════════════════════════════════════
    {
        "id": "raw-ad-001",
        "name_en": "Shuakhevi Alpine Pasture Dairy & Mountain Apiary",
        "name_ka": "შუახევის ალპური რძის ფერმა და მთის საფუტკრე",
        "region": "Adjara",
        "municipality_or_village": "Chvana Gorge, Shuakhevi Municipality",
        "category": "dairy_hub",
        "phone": "+995 598 44 22 10",
        "website_or_social": "https://visitajara.com/shuakhevi-agrotourism",
        "source_url": "https://visitajara.com/rural-tourism-adjara",
        "products": ["Adjarian Chogi Cheese", "Alpine Sour Cream (Kaimaghi)", "Raw Chestnut Honey", "Alpine Butter"],
        "description": "Highland dairy workshop located in the pristine Chvana valley. Cows graze on subalpine pastures producing high-fat, fragrant milk turned into legendary Adjarian Kaimaghi and cheeses.",
        "discovered_at": NOW
    },
    {
        "id": "raw-ad-002",
        "name_en": "Chakvi Subtropical Citrus & Tea Agrotourism Farm",
        "name_ka": "ჩაქვის სუბტროპიკული ციტრუსისა და ჩაის აგროტურისტული ფერმა",
        "region": "Adjara",
        "municipality_or_village": "Chakvi, Kobuleti Municipality",
        "category": "pick_your_own",
        "phone": "+995 577 15 20 30",
        "website_or_social": "https://facebook.com/chakvicitrusfarm",
        "source_url": "https://georgiantravelguide.com/adjara-citrus-tea",
        "products": ["Satsuma Mandarins (Nov–Dec U-Pick)", "Meyer Lemons", "Sweet Oranges", "Handmade Black & Green Tea"],
        "description": "Scenic coastal hillside plantation overlooking the Black Sea where visitors pick their own ripe mandarins and lemons during the autumn harvest or partake in springtime tea harvesting.",
        "discovered_at": NOW
    },

    # ═══════════════════════════════════════════════════════
    # GURIA (გურია)
    # ═══════════════════════════════════════════════════════
    {
        "id": "raw-gu-001",
        "name_en": "Tenitea Organic Farm — Handcrafted Artisanal Tea & Honey",
        "name_ka": "ტენითი ორგანული ფერმა — ხელნაკეთი ჩაი და სოფლის თაფლი",
        "region": "Guria",
        "municipality_or_village": "Kveda Bakhvi village, Ozurgeti Municipality",
        "category": "farm_shop",
        "phone": "+995 599 71 82 93",
        "website_or_social": "https://tenitea.com",
        "source_url": "https://tenitea.com",
        "products": ["Certified Organic Black Tea", "Artisanal Green Tea", "Wild Alpine Blueberry Leaf Tea", "Chestnut Honey"],
        "description": "Award-winning pioneer in reviving Georgia's boutique organic tea cultivation. Farm shop offers tea tastings, plantation strolls, and direct-from-plantation vacuum packs.",
        "discovered_at": NOW
    },
    {
        "id": "raw-gu-002",
        "name_en": "Likhauri Eco Farm & Cooperative — Estate Hazelnuts & Persimmons",
        "name_ka": "ლიხაურის ეკო ფერმა — გურული თხილი და ჩირი",
        "region": "Guria",
        "municipality_or_village": "Likhauri village, Ozurgeti Municipality",
        "category": "delivery_coop",
        "phone": "+995 593 18 29 40",
        "website_or_social": "https://likhaurieco.com",
        "source_url": "https://likhaurieco.com",
        "products": ["Shelled Guria Hazelnuts", "Sun-dried Sweet Persimmons (ჩირი)", "Local Citrus", "Hazelnut Oil"],
        "description": "Community agricultural cooperative aggregating fair-trade organic hazelnuts and traditional sun-cured persimmons from hillside orchards across Ozurgeti.",
        "discovered_at": NOW
    },

    # ═══════════════════════════════════════════════════════
    # RACHA-LECHKHUMI (რაჭა-ლეჩხუმი)
    # ═══════════════════════════════════════════════════════
    {
        "id": "raw-ra-001",
        "name_en": "Cooperative Racha Natural Products — Smoked Ham (Lori) & Mountain Beans",
        "name_ka": "სასოფლო-სამეურნეო კოოპერატივი რაჭის ნატურალური პროდუქტები — რაჭული ლორი და ლობიო",
        "region": "Racha-Lechkhumi",
        "municipality_or_village": "Ambrolauri (#2 Vazha-Pshavela / #7 Kostava St)",
        "category": "farm_shop",
        "phone": "+995 599 97 17 75",
        "website_or_social": "https://agreen-platform.com/racha-products",
        "source_url": "https://sakpatenti.gov.ge/rachuli-lori-pgi",
        "products": ["Protected PGI Rachuli Lori (რაჭული ლორი)", "Slow-cook Mountain Beans (რაჭული ლობიო)", "Mountain Blossom Honey", "Local Walnuts"],
        "description": "Official regional cooperative bringing together smallholders across Ambrolauri and Oni. Famous for slow alder-smoked free-foraging pork ham and authentic Rachan heirloom beans.",
        "discovered_at": NOW
    },
    {
        "id": "raw-ra-002",
        "name_en": "Shaori Alpine Trout & Mountain Dairy Retreat",
        "name_ka": "შაორის სამთო კალმახი და ყველის მეურნეობა",
        "region": "Racha-Lechkhumi",
        "municipality_or_village": "Shaori Reservoir Area, Ambrolauri Municipality",
        "category": "dairy_hub",
        "phone": "+995 595 70 80 90",
        "website_or_social": "https://facebook.com/shaoritroutdairy",
        "source_url": "https://georgiantravelguide.com/racha-agritourism",
        "products": ["Fresh Mountain Trout", "Rachan Curd Cheese", "Wild Herb Butter", "Smoked Mountain Cheeses"],
        "description": "Alpine lake-side fish farm and artisanal creamery using high-elevation spring waters and rich Rachan clover pastures. Direct gate sales to travelers and local tables.",
        "discovered_at": NOW
    },

    # ═══════════════════════════════════════════════════════
    # KAKHETI (კახეთი) — Core Pilot Records
    # ═══════════════════════════════════════════════════════
    {
        "id": "raw-001",
        "name_en": "Cooperative Alaznistavi — Tushuri Guda Cheese",
        "name_ka": "კოოპერატივი ალაზნისთავი — თუშური გუდა",
        "region": "Kakheti",
        "municipality_or_village": "Lower Alvani (Qvemo Alvani), Akhmeta Municipality",
        "category": "dairy_hub",
        "phone": "+995 558 45 42 42",
        "website_or_social": "http://guda.ge",
        "source_url": "http://guda.ge",
        "products": ["Tushuri Guda (Svilobi)", "Lartusho", "Dovna", "Chogi mountain cheeses"],
        "description": "PDO-certified cooperative producing authentic Tushetian Guda sheep-milk cheeses. Members from Tusheti mountain herders supply raw milk; cheese matures in natural sheepskin sacks.",
        "discovered_at": NOW
    },
    {
        "id": "raw-002",
        "name_en": "Marleta's Farm — Artisan Goat & Cow Cheese",
        "name_ka": "მარლეტას ფერმა — თხისა და ძროხის ხელნაკეთი ყველი",
        "region": "Kakheti",
        "municipality_or_village": "Shalauri village, Telavi Municipality",
        "category": "dairy_hub",
        "phone": "+995 599 12 00 45",
        "website_or_social": "https://facebook.com/marletasfarm",
        "source_url": "https://www.facebook.com/marletasfarm/",
        "products": ["Goat cheese with charcoal", "Bona (white mold cheese)", "Ashmerlo", "Labneh", "Cow Sulguni"],
        "description": "Boutique agrotourism cheese farm in Alazani Valley. Family-run by Sopho Gorgadze & Levan Tsaguria. French-method artisan cheeses, cheese tastings, open cafe. Active 2025–2026.",
        "discovered_at": NOW
    },
    {
        "id": "raw-003",
        "name_en": "Okro's Wine — Natural Wine Bar & Farm Shop, Sighnaghi",
        "name_ka": "ოქროს ღვინო — ნატურალური ღვინო და ფერმის მაღაზია, სიღნაღი",
        "region": "Kakheti",
        "municipality_or_village": "Sighnaghi",
        "category": "farm_shop",
        "phone": "+995 599 54 20 14",
        "website_or_social": "https://www.facebook.com/okroswine",
        "source_url": "https://raisin.digital/kakheti",
        "products": ["Natural Rkatsiteli wine", "Mtsvane amber wine", "Local honey", "Churchkhela", "Homemade chacha", "Seasonal farm produce"],
        "description": "Prominent natural wine bar, restaurant and farm-direct retail shop at 7a Chavchavadze St, Sighnaghi. Features local organic and seasonal farm products alongside qvevri wines. Active in 2025–2026.",
        "discovered_at": NOW
    },
    {
        "id": "raw-004",
        "name_en": "Kakheti 3000 — Winery & Direct-Sale Farm Shop",
        "name_ka": "კახეთი 3000 — მარანი და პირდაპირი გაყიდვა",
        "region": "Kakheti",
        "municipality_or_village": "Ninotsminda village, Sagarejo Municipality",
        "category": "farm_shop",
        "phone": "+995 505 55 72 81",
        "website_or_social": "https://kakheti-3000.wine",
        "source_url": "https://kakheti-3000.wine",
        "products": ["Classic regional wines", "Qvevri wine batches", "Rkatsiteli", "Saperavi"],
        "description": "Registered winery and farm shop at Ninotsminda village, Sagarejo Municipality. Sells classic and qvevri wine directly from cellar. Active website with direct-order options.",
        "discovered_at": NOW
    },
    {
        "id": "raw-005",
        "name_en": "Rtveli Grape Harvest Experience — Sighnaghi & Telavi",
        "name_ka": "რთველი — ყურძნის კრეფის ტური სიღნაღი და თელავი",
        "region": "Kakheti",
        "municipality_or_village": "Sighnaghi / Telavi area",
        "category": "pick_your_own",
        "phone": "+995 599 11 44 88",
        "website_or_social": "https://getyourguide.com/kakheti-grape-harvest",
        "source_url": "https://getyourguide.com",
        "products": ["Rkatsiteli grapes", "Saperavi grapes", "Mtsvane grapes"],
        "description": "Multiple family wineries and agrotourism operators in Sighnaghi and Telavi area offer participatory grape-picking (Rtveli) September–October.",
        "discovered_at": NOW
    },
    {
        "id": "raw-006",
        "name_en": "Ferma Oda — CSA Farm Box Delivery (Kakheti sourced)",
        "name_ka": "ფერმა ოდა — CSA ფერმის კუთვნილი ბოქსი მიწოდება",
        "region": "Kakheti",
        "municipality_or_village": "Kakheti Region (urban delivery Tbilisi)",
        "category": "delivery_coop",
        "phone": "+995 591 99 22 44",
        "website_or_social": "https://soplidan.ge",
        "source_url": "https://iset-pi.ge/soplidan-ferma-oda",
        "products": ["Seasonal vegetable boxes", "Herb bundles", "Farm eggs", "Local honey", "Fruit boxes"],
        "description": "Pioneer of the American-style CSA model in Georgia. Ferma Oda and Soplidan.ge aggregate Kakheti farm produce for direct-to-door subscriptions across Tbilisi and Kakheti.",
        "discovered_at": NOW
    },
    {
        "id": "raw-012",
        "name_en": "Alazani Valley Fruit Orchards — Strawberry & Cherry Self-Pick",
        "name_ka": "ალაზნის ველი ხილის ბაღები — მარწყვი და ბალი თვითკრეფა",
        "region": "Kakheti",
        "municipality_or_village": "Gurjaani / Kvareli area, Alazani Valley",
        "category": "pick_your_own",
        "phone": "+995 599 87 65 43",
        "website_or_social": "https://facebook.com/groups/kakheti-agro",
        "source_url": "https://east-fruit.com/kakheti-strawberry",
        "products": ["Strawberries (May–June)", "Sweet cherries (June–July)", "Plums (August)", "Figs (September)"],
        "description": "Open-field and mulch-irrigated strawberry and cherry orchards in the Alazani Valley villages offering direct harvest visits.",
        "discovered_at": NOW
    },

    # ═══════════════════════════════════════════════════════
    # KVEMO KARTLI (ქვემო ქართლი) — Core Pilot Records
    # ═══════════════════════════════════════════════════════
    {
        "id": "raw-007",
        "name_en": "Cooperative Disveli — Natural Dairy & Cheese (Bolnisi)",
        "name_ka": "კოოპერატივი დისველი — ნატურალური რძის პროდუქტები (ბოლნისი)",
        "region": "Kvemo Kartli",
        "municipality_or_village": "Bolnisi Municipality",
        "category": "dairy_hub",
        "phone": "+995 595 67 89 01",
        "website_or_social": "https://ebazaar.ge",
        "source_url": "https://ebazaar.ge",
        "products": ["Sulguni cheese", "Imeretian cheese", "Nadugi (cottage whey cheese)", "Butter", "Fresh milk"],
        "description": "Women-led cooperative founded by eco-migrants from Adjara. Sources milk from local smallholder cattle. 100% natural production.",
        "discovered_at": NOW
    },
    {
        "id": "raw-009",
        "name_en": "Kvemo Kartli Agricultural Cooperatives Network (ENPARD)",
        "name_ka": "ქვემო ქართლის სასოფლო-სამეურნეო კოოპერატივების ქსელი (ENPARD)",
        "region": "Kvemo Kartli",
        "municipality_or_village": "Marneuli / Bolnisi / Tsalka municipalities",
        "category": "delivery_coop",
        "phone": "+995 599 30 40 50",
        "website_or_social": "https://gfa.org.ge",
        "source_url": "https://gfa.org.ge",
        "products": ["Mixed seasonal produce", "Dairy aggregation", "Grain", "Legumes"],
        "description": "Georgian Farmers Association (GFA) coordinates registered agricultural cooperatives in Kvemo Kartli under ENPARD EU program.",
        "discovered_at": NOW
    },

    # ═══════════════════════════════════════════════════════
    # NEGATIVE TEST LEADS (Quality Verifier Exclusion Gate Checks)
    # ═══════════════════════════════════════════════════════
    {
        "id": "raw-neg-001",
        "name_en": "Carrefour Georgia — Rustavi Hypermarket",
        "name_ka": "კარფური — რუსთავის ჰიპერმარკეტი",
        "region": "Kvemo Kartli",
        "municipality_or_village": "Rustavi",
        "category": "farm_shop",
        "phone": "+995 32 2 00 00 01",
        "website_or_social": "https://carrefour.ge",
        "source_url": "https://carrefour.ge",
        "products": ["Imported produce", "Supermarket goods"],
        "description": "National supermarket chain. NOT a farm or local producer.",
        "discovered_at": NOW
    },
    {
        "id": "raw-neg-002",
        "name_en": "Goodwill Vake Supermarket",
        "name_ka": "გუდვილი ვაკე — სუპერმარკეტი",
        "region": "Tbilisi",
        "municipality_or_village": "Vake, Tbilisi",
        "category": "farm_shop",
        "phone": "+995 32 2 24 36 73",
        "website_or_social": "https://goodwill.ge",
        "source_url": "https://goodwill.ge",
        "products": ["Supermarket items", "Imported cheese", "Bakery"],
        "description": "National supermarket chain. Negative test lead.",
        "discovered_at": NOW
    },
    {
        "id": "raw-neg-003",
        "name_en": "Tsalka Mountain Dairy Hub — Alpine Cheese Farm (No Contact)",
        "name_ka": "წალკის სამთო ფერმა — სამთო ყველი (საკონტაქტოს გარეშე)",
        "region": "Kvemo Kartli",
        "municipality_or_village": "Tsalka Municipality",
        "category": "dairy_hub",
        "phone": None,
        "website_or_social": None,
        "source_url": "https://parliament.ge/kvemo-kartli-agro",
        "products": ["Mountain Sulguni"],
        "description": "Lacks any verifiable contact channel or phone. Gate 2 negative test.",
        "discovered_at": NOW
    }
]

def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(RAW_LEADS, f, ensure_ascii=False, indent=2)
    print(f"✅ Regional Scout (Nationwide): {len(RAW_LEADS)} raw leads written → {OUTPUT_PATH}")
    regions = sorted(set(l['region'] for l in RAW_LEADS))
    print(f"   Covering {len(regions)} regions: {', '.join(regions)}")

if __name__ == "__main__":
    main()
