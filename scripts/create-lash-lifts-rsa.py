#!/usr/bin/env python3
"""Create Lash Lifts RSA (social proof + trust variant) for A/B testing.

Steps:
1. Draft the RSA (returns preview + plan_id)
2. Apply the plan with dry_run=False
"""

import json
import sys

sys.path.insert(0, "/Users/bobbybot/Projects/adloop/src")

from adloop.config import load_config
from adloop.ads.write import (
    draft_responsive_search_ad,
    confirm_and_apply,
)

config = load_config()

# --- Step 1: Draft ---
headlines = [
    "12 Five-Star Reviews",        # 22 chars - social proof
    "Lash Lifts From $75",         # 19 chars - price
    "Certified Lash Artists",      # 22 chars - trust
    "7 Private Suites",            # 16 chars - specifics
    "Open 7 Days a Week",          # 19 chars - convenience
    "Winnipeg Lash Lift Pros",     # 23 chars - location
    "Results Last 6-8 Weeks",      # 22 chars - numbers/specifics
    "Book Your Lash Lift Today",   # 25 chars - CTA
    "Trusted by 100+ Clients",     # 23 chars - social proof
    "2211 McPhillips St",          # 18 chars - location
]

descriptions = [
    "12 five-star Google reviews. Certified lash artists in 7 private suites. Book today.",   # 85 chars
    "Lash lifts from $75. Beautiful, natural-looking results that last 6-8 weeks.",           # 78 chars
    "Open 7 days a week at 2211 McPhillips St. Winnipeg's trusted lash lounge.",              # 74 chars
    "Certified lash artists deliver stunning lifts in a luxury private suite setting.",        # 82 chars
]

# Verify character counts
print("=== Headline Character Counts ===")
for h in headlines:
    count = len(h)
    status = "OK" if count <= 30 else "OVER"
    print(f"  [{count:2d}] {status}: {h}")

print("\n=== Description Character Counts ===")
for d in descriptions:
    count = len(d)
    status = "OK" if count <= 90 else "OVER"
    print(f"  [{count:2d}] {status}: {d}")

print("\n=== Drafting RSA ===")
draft_result = draft_responsive_search_ad(
    config,
    customer_id="168-203-3495",
    ad_group_id="192083196862",
    headlines=headlines,
    descriptions=descriptions,
    final_url="https://lavilash.ca/ads/lash-lifts",
    path1="Lash-Lifts",
    path2="Winnipeg",
)

print(json.dumps(draft_result, indent=2))

if "error" in draft_result:
    print("\nDraft failed. Aborting.")
    sys.exit(1)

plan_id = draft_result.get("plan_id")
if not plan_id:
    print("\nNo plan_id returned. Aborting.")
    sys.exit(1)

print(f"\n=== Applying Plan {plan_id} (dry_run=False) ===")
apply_result = confirm_and_apply(
    config,
    plan_id=plan_id,
    dry_run=False,
)

print(json.dumps(apply_result, indent=2))

if apply_result.get("status") == "APPLIED":
    print("\nRSA created successfully.")
else:
    print(f"\nApply result: {apply_result.get('status', 'UNKNOWN')}")
