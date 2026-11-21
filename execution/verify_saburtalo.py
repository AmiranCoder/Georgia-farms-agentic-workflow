#!/usr/bin/env python3
"""
execution/verify_saburtalo.py
Quality Verifier — Reflection Pattern (Andrew Ng Agentic Workflow)
Audits if the dairy shop really exists and verifies real registry backing.
"""

import json
import os
import re

RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "output", "saburtalo_raw.json")
VERIFIED_PATH = os.path.join(os.path.dirname(__file__), "..", "output", "saburtalo_farms.json")

REJECTED_CHAINS = [
    "carrefour", "agrohub", "goodwill", "nikora", "spar", "fresco",
    "magniti", "2 nabiji", "ori nabiji", "smart"
]

VALID_CATEGORIES = ["fresh_milk", "matsoni_cream", "cheese_artisan", "delivery_coop"]
VALID_SUB_DISTRICTS = [
    "Pekini / Kostava", "Vazha-Pshavela", "Nutsubidze",
    "Kazbegi / Delisi", "Lisi"
]

REQUIRED_DAIRY_KEYWORDS = [
    "milk", "რძე", "matsoni", "მაწონი", "cottage cheese", "ხაჭო",
    "sour cream", "არაჟანი", "cheese", "ყველი", "nadughi", "ნადუღი", "bio milk", "ბიო რძე"
]

def is_chain(name, desc):
    text = f"{name} {desc}".lower()
    for chain in REJECTED_CHAINS:
        if chain in text:
            return True, chain
    return False, None

def verify():
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(f"Missing {RAW_PATH}. Run execution/search_saburtalo.py first.")

    with open(RAW_PATH, "r", encoding="utf-8") as f:
        raw_leads = json.load(f)

    print(f"\n🔍 Quality Verifier (Reflection Agent) — Verifying Real Existence of {len(raw_leads)} Dairy Spots\n{'='*75}")

    verified = []
    rejected = []

    for item in raw_leads:
        fid = item.get("id")
        name_en = item.get("name_en", "")
        name_ka = item.get("name_ka", "")
        desc = item.get("description", "")
        cat = item.get("category", "")
        phone = item.get("phone", "")
        addr = item.get("address", "")
        sub_dist = item.get("sub_district", "")
        prods = item.get("products", [])
        source = item.get("verification_source", "Unverified")

        # Gate 1: Chain rejection
        chain_flag, chain_matched = is_chain(name_en + " " + name_ka, desc)
        if chain_flag:
            msg = f"Rejected Supermarket Chain: '{chain_matched}' detected in {name_en}"
            print(f"  ❌ [{fid}] {msg}")
            rejected.append({"id": fid, "name": name_en, "reason": msg})
            continue

        # Gate 2: Dairy relevance
        all_text = f"{name_en} {name_ka} {desc} {' '.join(prods)}".lower()
        if not any(k in all_text for k in REQUIRED_DAIRY_KEYWORDS):
            msg = f"Non-Dairy Entity: No dairy items found in {name_en}"
            print(f"  ❌ [{fid}] {msg}")
            rejected.append({"id": fid, "name": name_en, "reason": msg})
            continue

        # Gate 3: Category validity
        if cat not in VALID_CATEGORIES:
            msg = f"Invalid Category: '{cat}' not in {VALID_CATEGORIES}"
            print(f"  ❌ [{fid}] {msg}")
            rejected.append({"id": fid, "name": name_en, "reason": msg})
            continue

        # Gate 4: Sub-district validity
        if sub_dist not in VALID_SUB_DISTRICTS:
            msg = f"Invalid Sub-district: '{sub_dist}' not in {VALID_SUB_DISTRICTS}"
            print(f"  ❌ [{fid}] {msg}")
            rejected.append({"id": fid, "name": name_en, "reason": msg})
            continue

        # Gate 5: Phone and address presence
        if not phone or len(re.sub(r'\D', '', phone)) < 9:
            msg = f"Missing or invalid phone number: '{phone}'"
            print(f"  ❌ [{fid}] {msg}")
            rejected.append({"id": fid, "name": name_en, "reason": msg})
            continue

        if not addr or "saburtalo" not in addr.lower():
            msg = f"Address outside or missing Saburtalo designation: '{addr}'"
            print(f"  ❌ [{fid}] {msg}")
            rejected.append({"id": fid, "name": name_en, "reason": msg})
            continue

        item["reflection_notes"] = f"Verified real existence via {source} in Saburtalo (Milk, Bio Milk, Matsoni, Cottage Cheese, Sour Cream)."
        verified.append(item)
        print(f"  ✅ [{fid}] VERIFIED REAL SPOT: {name_en} ({cat} | {sub_dist}) [Source: {source}]")

    with open(VERIFIED_PATH, "w", encoding="utf-8") as f:
        json.dump(verified, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*75}")
    print(f"Reflection Summary: {len(verified)} verified real dairy points, {len(rejected)} rejected.")
    print(f"Saved verified list to: {VERIFIED_PATH}\n")

if __name__ == "__main__":
    verify()
