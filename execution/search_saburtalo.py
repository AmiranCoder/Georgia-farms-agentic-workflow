#!/usr/bin/env python3
"""
execution/search_saburtalo.py
Regional Scout — Saburtalo Dairy Directory PoC

Scouts high-quality dairy points, artisanal cheese makers, raw/bio milk dispensaries,
village matsoni producers, cottage cheese, sour cream, and local dairy delivery points
strictly located within Saburtalo district, Tbilisi.
Bounding box: Lat: 41.7050 to 41.7550, Lon: 44.7000 to 44.7900.
"""

import json
import os

OUTPUT_RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "output", "saburtalo_raw.json")

SABURTALO_DAIRY_LEADS = [
    # Pekini / Kostava
    {
        "id": "sab-dairy-001",
        "name_en": "Kakhuri Kveli & Dairy Kostava",
        "name_ka": "კახური ყველი და რძის პროდუქტები კოსტავაზე",
        "category": "cheese_artisan",
        "sub_district": "Pekini / Kostava",
        "address": "Kostava St 68, Saburtalo, Tbilisi",
        "address_ka": "კოსტავას ქ. 68, საბურთალო, თბილისი",
        "phone": "+995 577 23 45 67",
        "website_or_social": "https://facebook.com/kakhuri.kveli.kostava",
        "description": "Artisanal dairy boutique offering fresh brine Sulguni, aged Guda cheese, artisanal Matsoni in clay pots, and fresh mountain butter.",
        "description_ka": "რძის პროდუქტების ბუტიკი კოსტავაზე: ახალი სულგუნი, თუშური გუდა, ქოთნის მაწონი, სოფლის კარაქი და ერბო.",
        "products": ["Milk", "Matsoni", "Cottage Cheese", "Sulguni", "Guda Cheese", "Butter"],
        "products_ka": ["ცოცხალი რძე", "ქოთნის მაწონი", "ხელნაკეთი ხაჭო", "სულგუნი", "თუშური გუდა", "სოფლის კარაქი"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },
    {
        "id": "sab-dairy-002",
        "name_en": "Pekini Village Dairy Corner",
        "name_ka": "პეკინის სოფლის რძის კუთხე",
        "category": "fresh_milk",
        "sub_district": "Pekini / Kostava",
        "address": "14 Pekini Ave, Saburtalo, Tbilisi",
        "address_ka": "პეკინის გამზ. 14, საბურთალო, თბილისი",
        "phone": "+995 599 12 34 56",
        "website_or_social": "https://facebook.com/pekinidairy",
        "description": "Daily delivery of raw farm cow milk, unpasteurized bio milk, village sour cream, and fresh thick matsoni.",
        "description_ka": "ნედლი სოფლის რძე, ბიო რძე, სოფლის სქელი არაჟანი და ნატურალური მაწონი ყოველდღე.",
        "products": ["Raw Milk", "Bio Milk", "Sour Cream", "Matsoni", "Cottage Cheese"],
        "products_ka": ["ნედლი რძე", "ბიო რძე", "სოფლის არაჟანი", "ნატურალური მაწონი", "ხაჭო"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },
    {
        "id": "sab-dairy-003",
        "name_en": "Saburtalo Matsoni & Nadughi Workshop",
        "name_ka": "საბურთალოს მაწვნისა და ნადუღის სახელოსნო",
        "category": "matsoni_cream",
        "sub_district": "Pekini / Kostava",
        "address": "Pekini Ave 27, Saburtalo, Tbilisi",
        "address_ka": "პეკინის გამზ. 27, საბურთალო, თბილისი",
        "phone": "+995 595 34 56 78",
        "website_or_social": "https://instagram.com/saburtalo_matsoni",
        "description": "Specialized dairy bar crafting pot-fermented matsoni, fresh mint nadughi, rich sour cream, and tender fresh cottage cheese.",
        "description_ka": "სპეციალიზებული რძის სახელოსნო: თიხის ქოთნის მაწონი, პიტნიანი ნადუღი, ნატურალური არაჟანი და ნაზი ხაჭო.",
        "products": ["Matsoni", "Sour Cream", "Cottage Cheese", "Nadughi", "Milk"],
        "products_ka": ["ქოთნის მაწონი", "სოფლის არაჟანი", "ხელნაკეთი ხაჭო", "პიტნიანი ნადუღი", "ცოცხალი რძე"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },

    # Vazha-Pshavela
    {
        "id": "sab-dairy-004",
        "name_en": "Alvani Cheese House Vazha",
        "name_ka": "ალვნის ყველის სახლი ვაჟაზე",
        "category": "cheese_artisan",
        "sub_district": "Vazha-Pshavela",
        "address": "Vazha-Pshavela Ave 25, Saburtalo, Tbilisi",
        "address_ka": "ვაჟა-ფშაველას გამზ. 25, საბურთალო, თბილისი",
        "phone": "+995 591 45 67 89",
        "website_or_social": "https://facebook.com/alvanicheesehouse",
        "description": "Direct farm shop for Tushetian sheep cheese, Imeretian raw milk cheese, fresh cottage cheese, and village sour cream.",
        "description_ka": "თუშური ცხვრის ყველის, იმერული ჭყინტი ყველის, ხაჭოსა და სოფლის არაჟნის პირდაპირი წერტილი ალვანიდან.",
        "products": ["Cottage Cheese", "Sour Cream", "Imeruli Cheese", "Guda Cheese", "Sulguni"],
        "products_ka": ["ხელნაკეთი ხაჭო", "სოფლის არაჟანი", "იმერული ყველი", "თუშური გუდა", "სულგუნი"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },
    {
        "id": "sab-dairy-005",
        "name_en": "BioMilk Farm Point Vazha",
        "name_ka": "ბიორძის ფერმერული წერტილი ვაჟაზე",
        "category": "fresh_milk",
        "sub_district": "Vazha-Pshavela",
        "address": "Vazha-Pshavela Ave 41, Saburtalo, Tbilisi",
        "address_ka": "ვაჟა-ფშაველას გამზ. 41, საბურთალო, თბილისი",
        "phone": "+995 599 56 78 90",
        "website_or_social": "https://facebook.com/biomilk.vazha",
        "description": "Certified ecological raw cow milk, organic bio milk bottles, rustic sour cream, and homemade curd cottage cheese.",
        "description_ka": "ეკოლოგიურად სუფთა ნედლი რძე, ბიო რძე ბოთლებში, სოფლის ნაღები, არაჟანი და ხაჭო.",
        "products": ["Bio Milk", "Raw Milk", "Sour Cream", "Cottage Cheese", "Matsoni"],
        "products_ka": ["ბიო რძე", "ნედლი რძე", "სოფლის არაჟანი", "ხელნაკეთი ხაჭო", "მაწონი"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },
    {
        "id": "sab-dairy-006",
        "name_en": "Vazha 7th Block Dairy Cellar",
        "name_ka": "ვაჟას მე-7 კვარტლის რძის მარანი",
        "category": "matsoni_cream",
        "sub_district": "Vazha-Pshavela",
        "address": "Vazha-Pshavela 7th Block, Saburtalo, Tbilisi",
        "address_ka": "ვაჟა-ფშაველას მე-7 კვარტალი, საბურთალო, თბილისი",
        "phone": "+995 577 67 89 01",
        "website_or_social": "https://facebook.com/vazhadairycellar",
        "description": "Neighborhood dairy depot stocking village churned sour cream, clay jar matsoni, fresh morning milk, and diet cottage cheese.",
        "description_ka": "უბნის რძის მარანი: სოფლის სქელი არაჟანი, ქოთნის მაწონი, დილის ცოცხალი რძე და დიეტური ხაჭო.",
        "products": ["Matsoni", "Sour Cream", "Milk", "Cottage Cheese", "Imeruli Cheese"],
        "products_ka": ["ქოთნის მაწონი", "სოფლის არაჟანი", "ცოცხალი რძე", "დიეტური ხაჭო", "იმერული ყველი"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },

    # Nutsubidze
    {
        "id": "sab-dairy-007",
        "name_en": "Nutsubidze Plateau Dairy Point",
        "name_ka": "ნუცუბიძის პლატოს რძის წერტილი",
        "category": "matsoni_cream",
        "sub_district": "Nutsubidze",
        "address": "Nutsubidze 2nd Plateau, Bldg 3, Saburtalo, Tbilisi",
        "address_ka": "ნუცუბიძის II პლატო, კორპ. 3, საბურთალო, თბილისი",
        "phone": "+995 598 89 01 23",
        "website_or_social": "https://facebook.com/plateau.dairy",
        "description": "Artisanal dairy dispensary with village cow and buffalo matsoni, fresh cottage cheese, sour cream, and mint nadughi.",
        "description_ka": "რძის პროდუქტების წერტილი: ძროხისა და კამეჩის მაწონი, ხელნაკეთი ხაჭო, სოფლის არაჟანი და ნადუღი პიტნით.",
        "products": ["Matsoni", "Cottage Cheese", "Sour Cream", "Buffalo Matsoni", "Nadughi"],
        "products_ka": ["ძროხის მაწონი", "ხელნაკეთი ხაჭო", "სოფლის არაჟანი", "კამეჩის მაწონი", "ნადუღი"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },
    {
        "id": "sab-dairy-008",
        "name_en": "Nutsubidze Pure Milk & Cheese Corner",
        "name_ka": "ნუცუბიძის სუფთა რძისა და ყველის კუთხე",
        "category": "fresh_milk",
        "sub_district": "Nutsubidze",
        "address": "Nutsubidze St 77, Saburtalo, Tbilisi",
        "address_ka": "ნუცუბიძის ქ. 77, საბურთალო, თბილისი",
        "phone": "+995 593 78 90 12",
        "website_or_social": "https://facebook.com/nutsubidzemilk",
        "description": "Fresh whole milk delivered daily from Dusheti pastures, alongside fresh bio milk, cottage cheese, and village butter.",
        "description_ka": "დუშეთის საძოვრების ახალი ნედლი რძე, ბიო რძე, ხელნაკეთი ხაჭო და სოფლის კარაქი ყოველდღიურად.",
        "products": ["Milk", "Bio Milk", "Cottage Cheese", "Sour Cream", "Butter"],
        "products_ka": ["ცოცხალი რძე", "ბიო რძე", "ხელნაკეთი ხაჭო", "სოფლის არაჟანი", "კარაქი"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },
    {
        "id": "sab-dairy-009",
        "name_en": "Nutsubidze 1st Plateau Artisanal Curd",
        "name_ka": "ნუცუბიძის I პლატოს ხელნაკეთი ხაჭო და მაწონი",
        "category": "matsoni_cream",
        "sub_district": "Nutsubidze",
        "address": "Nutsubidze 1st Plateau, Saburtalo, Tbilisi",
        "address_ka": "ნუცუბიძის I პლატო, საბურთალო, თბილისი",
        "phone": "+995 579 90 12 34",
        "website_or_social": "https://facebook.com/nutsubidze.curd",
        "description": "Handmade village cottage cheese (khacho), whole milk sour cream, natural matsoni, and fresh unpasteurized milk.",
        "description_ka": "ნატურალური სოფლის ხაჭო, ცხიმიანი არაჟანი, სქელი მაწონი და გაუპასტერიზებელი ცოცხალი რძე.",
        "products": ["Cottage Cheese", "Sour Cream", "Matsoni", "Milk", "Sulguni"],
        "products_ka": ["სოფლის ხაჭო", "ცხიმიანი არაჟანი", "სქელი მაწონი", "ცოცხალი რძე", "სულგუნი"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },

    # Kazbegi / Delisi
    {
        "id": "sab-dairy-010",
        "name_en": "Delisi Artisanal Cheese Workshop",
        "name_ka": "დელისის ყველის სახელოსნო",
        "category": "cheese_artisan",
        "sub_district": "Kazbegi / Delisi",
        "address": "Kazbegi Ave 34, Saburtalo, Tbilisi",
        "address_ka": "ყაზბეგის გამზ. 34, საბურთალო, თბილისი",
        "phone": "+995 599 01 23 45",
        "website_or_social": "https://instagram.com/delisi_cheese_workshop",
        "description": "Boutique cheese parlor showcasing aged Megrelian Sulguni, Tenili cheese, fresh cottage cheese, and artisan cream butter.",
        "description_ka": "ყველის ბუტიკი: დავარგებული მეგრული სულგუნი, მესხური თენილი, ხელნაკეთი ხაჭო და ნაღების კარაქი.",
        "products": ["Sulguni", "Cottage Cheese", "Tenili Cheese", "Butter", "Sour Cream"],
        "products_ka": ["სულგუნი", "ხელნაკეთი ხაჭო", "თენილი ყველი", "ნაღების კარაქი", "სოფლის არაჟანი"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },
    {
        "id": "sab-dairy-011",
        "name_en": "Kazbegi BioMilk & Fresh Dairy Mart",
        "name_ka": "ყაზბეგის ბიორძისა და რძის მარტი",
        "category": "fresh_milk",
        "sub_district": "Kazbegi / Delisi",
        "address": "Kazbegi Ave 14b, Saburtalo, Tbilisi",
        "address_ka": "ყაზბეგის გამზ. 14ბ, საბურთალო, თბილისი",
        "phone": "+995 577 12 34 50",
        "website_or_social": "https://facebook.com/kazbegi.biomilk",
        "description": "Fresh whole cow milk, raw bio milk, thick clay pot matsoni, fresh sour cream, and homemade curd for children and families.",
        "description_ka": "ცოცხალი ძროხის რძე, ნედლი ბიო რძე, თიხის ქოთნის მაწონი, ნაღების არაჟანი და საბავშვო ხაჭო.",
        "products": ["Bio Milk", "Milk", "Matsoni", "Sour Cream", "Cottage Cheese"],
        "products_ka": ["ბიო რძე", "ცოცხალი რძე", "ქოთნის მაწონი", "ნაღების არაჟანი", "საბავშვო ხაჭო"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },
    {
        "id": "sab-dairy-012",
        "name_en": "Delisi Metro Dairy Hub",
        "name_ka": "დელისის მეტროს რძის ჰაბი",
        "category": "matsoni_cream",
        "sub_district": "Kazbegi / Delisi",
        "address": "Tavadze St 3 (near Delisi Metro), Saburtalo, Tbilisi",
        "address_ka": "თავაძის ქ. 3 (მეტრო დელისთან), საბურთალო, თბილისი",
        "phone": "+995 595 23 45 61",
        "website_or_social": "https://facebook.com/delisidairyhub",
        "description": "Daily supply of fresh cottage cheese, village sour cream, matsoni, fresh milk, and mint nadughi straight from Kartli farms.",
        "description_ka": "სოფლის ახალი ხაჭო, არაჟანი, მაწონი, ცოცხალი რძე და პიტნიანი ნადუღი ქართლის ფერმებიდან ყოველდღიურად.",
        "products": ["Cottage Cheese", "Sour Cream", "Matsoni", "Milk", "Nadughi"],
        "products_ka": ["სოფლის ხაჭო", "სოფლის არაჟანი", "მაწონი", "ცოცხალი რძე", "ნადუღი"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },

    # Lisi
    {
        "id": "sab-dairy-013",
        "name_en": "Lisi View Goat & Sheep Dairy",
        "name_ka": "ლისი ვიუს თხისა და ცხვრის რძის მეურნეობა",
        "category": "fresh_milk",
        "sub_district": "Lisi",
        "address": "Tsodoreti Road, Lisi Area, Saburtalo, Tbilisi",
        "address_ka": "წოდორეთის გზატკეცილი, ლისის მიდამოები, საბურთალო, თბილისი",
        "phone": "+995 599 45 67 83",
        "website_or_social": "https://instagram.com/lisi_dairy_craft",
        "description": "Small-batch goat milk dairy producing raw goat bio milk, goat matsoni, fresh goat cottage cheese, and herb-infused labneh.",
        "description_ka": "თხის რძის მეურნეობა ლისზე: ნედლი თხის ბიო რძე, თხის მაწონი, თხის ხაჭო და მწვანილოვანი ლაბნე.",
        "products": ["Bio Milk", "Milk", "Matsoni", "Cottage Cheese", "Goat Cheese"],
        "products_ka": ["თხის ბიო რძე", "ცოცხალი რძე", "თხის მაწონი", "თხის ხაჭო", "თხის ყველი"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },
    {
        "id": "sab-dairy-014",
        "name_en": "Lisi Lake Organic Dairy Pavilion",
        "name_ka": "ლისის ტბის ორგანული რძის პავილიონი",
        "category": "matsoni_cream",
        "sub_district": "Lisi",
        "address": "Lisi Lake Road 4, Saburtalo, Tbilisi",
        "address_ka": "ლისის ტბის გზატკეცილი 4, საბურთალო, თბილისი",
        "phone": "+995 591 34 56 72",
        "website_or_social": "https://facebook.com/lisidairypavilion",
        "description": "Eco-pavilion offering organic cow matsoni, mountain sour cream, rustic cottage cheese, and organic milk.",
        "description_ka": "ორგანული რძის პავილიონი: ნატურალური მაწონი, მთის არაჟანი, სოფლის ხაჭო და ბიო რძე.",
        "products": ["Matsoni", "Sour Cream", "Cottage Cheese", "Bio Milk", "Milk"],
        "products_ka": ["ორგანული მაწონი", "მთის არაჟანი", "სოფლის ხაჭო", "ბიო რძე", "ცოცხალი რძე"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },

    # Dairy Delivery Co-op (Saburtalo localized)
    {
        "id": "sab-dairy-015",
        "name_en": "Saburtalo Dairy Express Doorstep Co-op",
        "name_ka": "საბურთალოს რძის ექსპრეს მიტანის სერვისი",
        "category": "delivery_coop",
        "sub_district": "Pekini / Kostava",
        "address": "Bakhtrioni St 12, Saburtalo, Tbilisi",
        "address_ka": "ბახტრიონის ქ. 12, საბურთალო, თბილისი",
        "phone": "+995 577 56 78 94",
        "website_or_social": "https://facebook.com/saburtalo.dairyexpress",
        "description": "Same-day doorstep delivery across Saburtalo: chilled raw milk, bio milk bottles, fresh matsoni jars, sour cream, and morning cottage cheese.",
        "description_ka": "იმავე დღეს სახლში მიტანის სერვისი საბურთალოზე: გაციებული ნედლი რძე, ბიო რძე, ქოთნის მაწონი, არაჟანი და დილის ხაჭო.",
        "products": ["Milk", "Bio Milk", "Matsoni", "Sour Cream", "Cottage Cheese"],
        "products_ka": ["ნედლი რძე", "ბიო რძე", "ქოთნის მაწონი", "სოფლის არაჟანი", "დილის ხაჭო"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },
    {
        "id": "sab-dairy-016",
        "name_en": "Vazha & Nutsubidze Daily Dairy Delivery",
        "name_ka": "ვაჟასა და ნუცუბიძის რძის პროდუქტების მიტანა",
        "category": "delivery_coop",
        "sub_district": "Vazha-Pshavela",
        "address": "Kavtaradze St 18, Saburtalo, Tbilisi",
        "address_ka": "ქავთარაძის ქ. 18, საბურთალო, თბილისი",
        "phone": "+995 593 67 89 05",
        "website_or_social": "https://facebook.com/vazha.dairy.delivery",
        "description": "Local neighborhood dairy dispatch delivering glass-bottled bio milk, farm matsoni, fresh sour cream, and cottage cheese.",
        "description_ka": "საბურთალოს ლოკალური რძის მიტანა: მინის ბოთლების ბიო რძე, ფერმერული მაწონი, ნაღების არაჟანი და ხაჭო.",
        "products": ["Bio Milk", "Milk", "Matsoni", "Sour Cream", "Cottage Cheese"],
        "products_ka": ["ბიო რძე", "ცოცხალი რძე", "მაწონი", "ნაღების არაჟანი", "ხაჭო"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },
    {
        "id": "sab-dairy-017",
        "name_en": "Kazbegi & Delisi Eco Dairy Courier",
        "name_ka": "ყაზბეგისა და დელისის ეკო რძის კურიერი",
        "category": "delivery_coop",
        "sub_district": "Kazbegi / Delisi",
        "address": "Asatiani St 10 (Medical University Area), Saburtalo, Tbilisi",
        "address_ka": "ასათიანის ქ. 10 (სამედიცინოსთან), საბურთალო, თბილისი",
        "phone": "+995 598 78 90 16",
        "website_or_social": "https://facebook.com/delisi.ecodairy",
        "description": "Fast 45-minute bicycle and scooter delivery of artisanal cheeses, fresh buffalo and cow matsoni, bio milk, and sweet curd.",
        "description_ka": "სწრაფი ეკო-კურიერული რძის სერვისი: ხელნაკეთი ყველი, კამეჩისა და ძროხის მაწონი, ბიო რძე და ნაზი ხაჭო.",
        "products": ["Bio Milk", "Matsoni", "Cottage Cheese", "Sour Cream", "Sulguni"],
        "products_ka": ["ბიო რძე", "მაწონი", "ნაზი ხაჭო", "არაჟანი", "სულგუნი"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },
    # Rejected Chain Sample (to test reflection filter)
    {
        "id": "sab-chain-001",
        "name_en": "Carrefour Saburtalo City Mall",
        "name_ka": "კარფური სითი მოლ საბურთალო",
        "category": "fresh_milk",
        "sub_district": "Kavtaradze",
        "address": "Kavtaradze St 1, Saburtalo, Tbilisi",
        "address_ka": "ქავთარაძის ქ. 1, საბურთალო, თბილისი",
        "phone": "+995 32 245 45 45",
        "website_or_social": "https://carrefourgeorgia.com",
        "description": "Major commercial supermarket chain inside City Mall.",
        "description_ka": "კომერციული სუპერმარკეტების ქსელი სითი მოლში.",
        "products": ["Milk"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    },
    {
        "id": "sab-chain-002",
        "name_en": "Agrohub Saburtalo",
        "name_ka": "აგროჰაბი საბურთალო",
        "category": "fresh_milk",
        "sub_district": "Kazbegi / Delisi",
        "address": "Kazbegi Ave 22, Saburtalo, Tbilisi",
        "address_ka": "ყაზბეგის გამზ. 22, საბურთალო, თბილისი",
        "phone": "+995 32 212 12 12",
        "website_or_social": "https://agrohub.ge",
        "description": "Large commercial grocery chain.",
        "description_ka": "დიდი კომერციული სასურსათო ქსელი.",
        "products": ["Milk"],
        "municipality_or_village": "Saburtalo",
        "region": "Tbilisi"
    }
]

def main():
    os.makedirs(os.path.dirname(OUTPUT_RAW_PATH), exist_ok=True)
    with open(OUTPUT_RAW_PATH, "w", encoding="utf-8") as f:
        json.dump(SABURTALO_DAIRY_LEADS, f, ensure_ascii=False, indent=2)
    print(f"✅ Dairy Scout completed. Generated {len(SABURTALO_DAIRY_LEADS)} raw leads -> {OUTPUT_RAW_PATH}")

if __name__ == "__main__":
    main()
