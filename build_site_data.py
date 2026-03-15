"""
Build a compact JSON for the website by merging CSV stats with AI exposure scores.

Reads occupations.csv (for stats) and scores.json (for AI exposure).
Writes site/data.json.

India-specific fields:
  - pay_inr: Annual pay in INR
    - nco_code: NCO-2015 4-digit occupation code
      - sector: Broad sector (Agriculture/Industry/Services/Elementary)
        - nic_sector: NIC sector classification

        Usage:
          uv run python build_site_data.py
          """

import csv
import json
import os
from collections import Counter


def main():
        # Load AI exposure scores
        with open("scores.json", encoding="utf-8") as f:
                    scores_list = json.load(f)
                scores = {s["slug"]: s for s in scores_list}

    # Load CSV stats
    with open("occupations.csv", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)

    # Merge
    data = []
    for row in rows:
                slug = row["slug"]
                score = scores.get(slug, {})

        pay_inr = None
        if row.get("median_pay_annual_inr"):
                        try:
                                            pay_inr = int(row["median_pay_annual_inr"])
except ValueError:
                pass

        num_jobs = None
        if row.get("num_jobs"):
                        try:
                                            num_jobs = int(row["num_jobs"])
except ValueError:
                pass

        outlook = None
        if row.get("growth_outlook_pct"):
                        try:
                                            outlook = int(row["growth_outlook_pct"])
except ValueError:
                pass

        data.append({
                        "title": row["title"],
                        "slug": slug,
                        "category": row["category"],
                        "nco_code": row.get("nco_code", ""),
                        "nic_sector": row.get("nic_sector", ""),
                        "sector": row.get("sector", ""),
                        "pay_inr": pay_inr,
                        "jobs": num_jobs,
                        "outlook": outlook,
                        "outlook_desc": row.get("growth_outlook_desc", ""),
                        "education": row.get("entry_education", ""),
                        "skill_level": row.get("skill_level", ""),
                        "exposure": score.get("exposure"),
                        "exposure_rationale": score.get("rationale"),
                        "url": row.get("url", ""),
        })

    os.makedirs("site", exist_ok=True)
    with open("site/data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

    print(f"Wrote {len(data)} Indian occupations to site/data.json")

    total_jobs = sum(d["jobs"] for d in data if d["jobs"])
    scored = sum(1 for d in data if d["exposure"] is not None)
    print(f"Total jobs represented: {total_jobs}")
    print(f"Occupations with AI exposure scores: {scored}/{len(data)}")

    cats = Counter(d["category"] for d in data)
    print("\nBy NCO category:")
    for cat, count in sorted(cats.items()):
                print(f"  {cat}: {count}")

    sectors = Counter(d["sector"] for d in data if d["sector"])
    if sectors:
                print("\nBy broad sector:")
                for sector, count in sorted(sectors.items()):
                                print(f"  {sector}: {count}")


if __name__ == "__main__":
        main()
