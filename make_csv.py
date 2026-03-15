value
elif any(k in field for k in ["salary", "pay", "wage", "remuneration", "earning"]):
                row["median_pay_annual_inr"], row["median_pay_monthly_inr"] = parse_inr_pay(value)
elif any(k in field for k in ["employment", "number of jobs", "workforce"]):
                row["num_jobs"] = parse_number(value)
elif any(k in field for k in ["outlook", "growth", "projection"]):
                row["growth_outlook_pct"], row["growth_outlook_desc"] = parse_outlook(value)
elif any(k in field for k in ["training", "on-the-job"]):
                row["training"] = value
elif any(k in field for k in ["sector type", "broad sector"]):
                row["sector"] = value

    # Also look for definition lists (common in government sites)
    for dl in soup.find_all("dl"):
                items = list(dl.children)
                for i, item in enumerate(items):
                                if item.name == "dt" and i + 1 < len(items):
                                                    field = clean(item.get_text()).lower()
                                                    next_item = items[i + 1]
                                                    if hasattr(next_item, 'get_text'):
                                                                            value = clean(next_item.get_text())

                    if any(k in field for k in ["education", "qualification"]):
                                                if not row["entry_education"]:
                                                                                row["entry_education"] = value
                    elif any(k in field for k in ["sector", "industry"]):
                                                if not row["nic_sector"]:
                                                                                row["nic_sector"] = value

                            # Determine broad sector from NCO code if not found
                            if not row["sector"] and occ_meta.get("nco_code"):
                                        major = occ_meta["nco_code"][0]
                                        sector_map = {
                                            "1": "Services", "2": "Services", "3": "Services",
                                            "4": "Services", "5": "Services",
                                            "6": "Agriculture",
                                            "7": "Industry", "8": "Industry",
                                            "9": "Elementary",
                                        }
                                        row["sector"] = sector_map.get(major, "Other")

    return row


def main():
        with open("occupations.json", encoding="utf-8") as f:
                    occupations = json.load(f)

    fieldnames = [
                "title", "category", "slug", "nco_code", "nic_sector", "sector",
                "median_pay_annual_inr", "median_pay_monthly_inr",
                "entry_education", "skill_level", "training",
                "num_jobs", "growth_outlook_pct", "growth_outlook_desc",
                "url",
    ]

    rows = []
    missing = 0
    for occ in occupations:
                html_path = f"html/{occ['slug']}.html"
        if not os.path.exists(html_path):
                        missing += 1
                        # Still include the occupation with metadata from occupations.json
                        row = {
                            "title": occ["title"],
                            "category": occ["category"],
                            "slug": occ["slug"],
                            "nco_code": occ.get("nco_code", ""),
                            "nic_sector": "",
                            "sector": "",
                            "median_pay_annual_inr": "",
                            "median_pay_monthly_inr": "",
                            "entry_education": "",
                            "skill_level": "",
                            "training": "",
                            "num_jobs": "",
                            "growth_outlook_pct": "",
                            "growth_outlook_desc": "",
                            "url": occ.get("url", ""),
                        }
                        rows.append(row)
                        continue
                    row = extract_occupation(html_path, occ)
        rows.append(row)

    with open("occupations.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to occupations.csv (missing HTML: {missing})")

    # Quick sanity check
    print(f"\nSample rows:")
    for r in rows[:3]:
                pay = r['median_pay_annual_inr']
        pay_str = f"₹{pay}/yr" if pay else "pay unknown"
        print(f"  {r['title']}: {pay_str}, {r['num_jobs'] or 'unknown'} jobs, NCO: {r['nco_code']}")


if __name__ == "__main__":
        main()
