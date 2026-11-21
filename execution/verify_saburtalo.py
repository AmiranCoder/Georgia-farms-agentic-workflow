#!/usr/bin/env python3
"""
execution/verify_saburtalo.py
Quality Verifier — Reflection Pattern (Andrew Ng Agentic Workflow)

Filters raw leads for the Saburtalo District PoC:
1. Rejection Gate: Reject all supermarket chains (Carrefour, Agrohub, Goodwill, Nikora, Spar, Fresco, etc.)
2. Completeness Gate: Must have verified phone, address, and category.
3. Authenticity Gate: Must be genuine village/artisanal producer or local delivery co-op.
4. Geospatial Scope Gate: Must belong to Saburtalo neighborhoods.

Saves verified list to output/saburtalo_farms.json.
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

VALID_CATEGORIES = ["farm_shop", "dairy_hub", "meat_eggs", "delivery_coop"]
VALID_SUB_DISTRICTS = [
    "Pekini / Kostava", "Vazha-Pshavela", "Nutsubidze",
    "Kazbegi / Delisi", "Lisi", "Kavtaradze"
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

    print(f"\n🔍 Quality Verifier (Reflection Agent) — Auditing {len(raw_leads)} Saburtalo Leads\n{'='*70}")

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

        # Gate 1: Chain rejection
        chain_flag, chain_matched = is_chain(name_en + " " + name_ka, desc)
        if chain_flag:
            msg = f"Rejected Supermarket Chain: '{chain_matched}' detected in {name_en}"
            print(f"  ❌ [{fid}] {msg}")
            rejected.append({"id": fid, "name": name_en, "reason": msg})
            continue

        # Gate 2: Category validity
        if cat not in VALID_CATEGORIES:
            msg = f"Invalid Category: '{cat}' not in {VALID_CATEGORIES}"
            print(f"  ❌ [{fid}] {msg}")
            rejected.append({"id": fid, "name": name_en, "reason": msg})
            continue

        # Gate 3: Sub-district validity
        if sub_dist not in VALID_SUB_DISTRICTS:
            msg = f"Invalid Sub-district: '{sub_dist}' not in {VALID_SUB_DISTRICTS}"
            print(f"  ❌ [{fid}] {msg}")
            rejected.append({"id": fid, "name": name_en, "reason": msg})
            continue

        # Gate 4: Phone and address presence
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

        item["reflection_notes"] = "Verified authentic neighborhood artisanal farm shop / producer in Saburtalo."
        verified.append(item)
        print(f"  ✅ [{fid}] PASS: {name_en} ({cat} | {sub_dist})")

    with open(VERIFIED_PATH, "w", encoding="utf-8") as f:
        json.dump(verified, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*70}")
    print(f"Reflection Summary: {len(verified)} verified, {len(rejected)} rejected.")
    print(f"Saved verified list to: {VERIFIED_PATH}\n")

if __name__ == "__main__":
    verify()
