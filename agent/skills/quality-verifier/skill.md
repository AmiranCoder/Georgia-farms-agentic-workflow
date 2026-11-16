---
name: quality-verifier
description: Implements Andrew Ng's Reflection pattern to audit, critique, filter, and verify raw farm leads into verified_farms.json.
---

# Quality Verifier Skill (Reflection Pattern)

## Role & Mission
The **Quality Verifier** agent acts as an autonomous critic and auditor. Grounded in **Andrew Ng's Reflection Pattern**, this agent does not accept raw scout output at face value. Instead, it inspects, challenges, and refines candidates through a critical reflection loop before promoting them into the verified registry.

---

## 1. Reflection Criteria & Evaluation Gates

Every raw lead from `output/raw_leads.json` must pass four strict evaluative filters:

### Gate 1: Non-Producer & Supermarket Exclusion
- **Blacklist**: National supermarket chains (Carrefour, Goodwill, Nikora, Spar, Ori Nabiji, Magniti, Agrohub retail branch vs farm, Europroduct).
- **Industrial Exclusions**: Wholesalers of imported grain/meat, packaging manufacturers, agricultural chemical/seed resellers, international logistics brokers.
- **Rule**: Only genuine primary producers, farm shops located at or affiliated with farms, artisanal workshops, pick-your-own destinations, and farmer-owned cooperatives may pass.

### Gate 2: Contact Veracity & Phone Formatting
- Telephone numbers must be normalized into standard international Georgian format:
  - Mobile format: `+995 5XX XX XX XX`
  - Landline format: `+995 32 2XX XX XX` (Tbilisi) or regional area code e.g. `+995 350 XX XX` (Telavi).
- If a phone is present, it must be verified as structurally valid for Georgia (`+995` prefix followed by 9 digits). Leads with no phone must have a verified active digital contact channel (direct messaging link, WhatsApp, active email, or verifiable website).

### Gate 3: 2025–2026 Recency & Operational Vitality
- Check for signs of operational activity in 2025–2026:
  - Recent posts or catalog updates on social channels.
  - Active presence in current governmental agricultural support registries (e.g., RDA - Produce in Georgia 2024-2026 programs).
  - Explicit confirmation that the farm welcomes visitors, processes orders, or sells current season crops.
  - Permanent closures or abandoned listings must be rejected with an audit log reason.

### Gate 4: Geographic Integrity & Category Precision
- Verify that `region` corresponds to an authentic administrative area in Georgia.
- Correct misplaced categories (e.g., a pick-your-own strawberry farm wrongly labeled `delivery_coop` must be corrected to `pick_your_own`).

---

## 2. Reflection Workflow

```
[output/raw_leads.json]
         |
         v
+-----------------------------------+
|     Reflection Audit Engine       |
|  (execution/verify_leads.py)      |
+-----------------------------------+
   |                             |
   | [Fail: Supermarket,         | [Pass: Authentic,
   |  Inactive, Bad Contact]     |  Valid +995, 2025-26 Active]
   v                             v
[Audit Log / Rejected]      [output/verified_farms.json]
```

1. **Read**: Load `output/raw_leads.json`.
2. **Critique**: Run heuristic and web validation checks per lead. Record a `reflection_notes` entry explaining why the record passed or what edits were applied.
3. **Format & Enrich**: Standardize bilingual labels, addresses, product tags, and verify phone numbers.
4. **Publish Verified List**: Write validated, deduplicated, cleanly formatted records to `output/verified_farms.json`.

---

## 3. Input / Output Specifications

- **Input**: `output/raw_leads.json`.
- **Output**: `output/verified_farms.json`.
- **Execution Script**: `execution/verify_leads.py`.

---

## 4. Verified Farm Schema Specification
Each item in `output/verified_farms.json` must provide:
- `id`: Unique identifier (e.g. `farm-geo-XXX`).
- `name_en`: English display name.
- `name_ka`: Georgian display name (`ქართული`).
- `region`: Canonical region name.
- `municipality_or_village`: Local administrative unit.
- `address`: Detailed human-readable address.
- `category`: Exactly one of `farm_shop`, `dairy_hub`, `pick_your_own`, `delivery_coop`.
- `phone`: Cleaned `+995` formatted string.
- `phone_verified`: Boolean indicator.
- `website_or_social`: Valid web presence URL.
- `products`: Array of primary produce/items.
- `description`: Verified summary of activities.
- `verification_status`: `"verified"`
- `activity_checked_2025_2026`: Boolean indicator.
- `reflection_notes`: Audit rationale from the reflection pass.
