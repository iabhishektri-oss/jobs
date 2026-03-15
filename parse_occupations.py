"""
Parse India's National Classification of Occupations (NCO-2015) to extract
all occupations and build occupations.json.

The NCO-2015 is organized into:
  - 10 Major Groups (1-digit codes)
    - 43 Sub-Major Groups (2-digit codes)
      - 130 Minor Groups (3-digit codes)
        - 410 Unit Groups (4-digit codes)

        Data source:
          - NCO-2015 HTML/PDF from: https://labour.gov.in/sites/default/files/NCO-2015.pdf
            - NOS portal: https://www.nqr.gov.in/
              - NSDC sector skill council pages

              This script parses a locally saved HTML version of the NCO index page
              (saved as nco_index.html) to build occupations.json.

              To get the source file:
                1. Visit https://www.nqr.gov.in/ or https://labour.gov.in/
                  2. Save the occupation listing page as nco_index.html

                  Usage:
                    uv run python parse_occupations.py
                    """

from bs4 import BeautifulSoup
import json
import re

# NCO-2015 Major Group names (for categorization)
NCO_MAJOR_GROUPS = {
        "1": "Managers",
        "2": "Professionals",
        "3": "Technicians and Associate Professionals",
        "4": "Clerical Support Workers",
        "5": "Service and Sales Workers",
        "6": "Skilled Agricultural, Forestry and Fishery Workers",
        "7": "Craft and Related Trades Workers",
        "8": "Plant and Machine Operators and Assemblers",
        "9": "Elementary Occupations",
        "0": "Armed Forces Occupations",
}

def slugify(title):
        """Convert occupation title to a URL-friendly slug."""
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug.strip())
        slug = re.sub(r'-+', '-', slug)
        return slug

def get_category_from_nco_code(nco_code):
        """Map NCO code to major group category name."""
        if nco_code and len(nco_code) >= 1:
                    major = nco_code[0]
                    return NCO_MAJOR_GROUPS.get(major, "Other")
                return "Other"

def parse_nco_index(html_path):
        """
            Parse the NCO index HTML file and extract all unit group occupations.

                    Expected HTML structure (from nqr.gov.in or labour.gov.in):
                        Each occupation row contains: NCO code, occupation title, description link
                            """
    with open(html_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")

    occupations = {}  # slug -> occupation dict

    # Try to find occupation table rows
    # Adjust selectors based on actual HTML structure of the source
    rows = soup.find_all("tr")

    for row in rows:
                cells = row.find_all(["td", "th"])
                if len(cells) < 2:
                                continue

                # Look for NCO code pattern (4-digit number)
                first_cell_text = cells[0].get_text(strip=True)
                nco_match = re.match(r'^(\d{4})$', first_cell_text)

        if nco_match:
                        nco_code = nco_match.group(1)
                        title = cells[1].get_text(strip=True)

            # Get URL if there's a link
                        link = cells[1].find("a") or (cells[2].find("a") if len(cells) > 2 else None)
                        url = ""
                        if link and link.get("href"):
                                            href = link["href"]
                                            if href.startswith("http"):
                                                                    url = href
                        else:
                                                url = f"https://www.nqr.gov.in{href}"

            if title and nco_code:
                                slug = slugify(title)
                                category = get_category_from_nco_code(nco_code)

                if slug not in occupations:
                                        occupations[slug] = {
                                                                    "title": title,
                                                                    "nco_code": nco_code,
                                                                    "category": category,
                                                                    "slug": slug,
                                                                    "url": url,
                                        }

    return list(occupations.values())


def build_default_occupations():
        """
            Build a default list of major Indian occupations based on NCO-2015
                when the HTML source file is not available.

                        This covers the most significant occupational categories in India
                            by employment size, drawn from PLFS data and NCO-2015 unit groups.
                                """
    occupations = [
                # Major Group 1: Managers
        {"title": "Chief Executives and Senior Officials", "nco_code": "1111", "category": "Managers", "url": ""},
                {"title": "Business Services Managers", "nco_code": "1212", "category": "Managers", "url": ""},
                {"title": "Hotel and Restaurant Managers", "nco_code": "1411", "category": "Managers", "url": ""},
                {"title": "Retail and Wholesale Trade Managers", "nco_code": "1420", "category": "Managers", "url": ""},

                # Major Group 2: Professionals
                {"title": "Software and Applications Developers", "nco_code": "2512", "category": "Professionals", "url": ""},
                {"title": "Database and Network Professionals", "nco_code": "2521", "category": "Professionals", "url": ""},
                {"title": "Medical Doctors", "nco_code": "2211", "category": "Professionals", "url": ""},
                {"title": "Nursing Professionals", "nco_code": "2221", "category": "Professionals", "url": ""},
                {"title": "Secondary Education Teachers", "nco_code": "2330", "category": "Professionals", "url": ""},
                {"title": "Primary School Teachers", "nco_code": "2341", "category": "Professionals", "url": ""},
                {"title": "Finance Professionals", "nco_code": "2411", "category": "Professionals", "url": ""},
                {"title": "Chartered Accountants", "nco_code": "2411", "category": "Professionals", "url": ""},
                {"title": "Civil Engineers", "nco_code": "2142", "category": "Professionals", "url": ""},
                {"title": "Electrical Engineers", "nco_code": "2151", "category": "Professionals", "url": ""},
                {"title": "Mechanical Engineers", "nco_code": "2144", "category": "Professionals", "url": ""},
                {"title": "Lawyers and Legal Professionals", "nco_code": "2611", "category": "Professionals", "url": ""},
                {"title": "Architects and Town Planners", "nco_code": "2161", "category": "Professionals", "url": ""},

                # Major Group 3: Technicians and Associate Professionals
                {"title": "Medical and Pharmaceutical Technicians", "nco_code": "3212", "category": "Technicians and Associate Professionals", "url": ""},
                {"title": "ICT Operations and User Support Technicians", "nco_code": "3513", "category": "Technicians and Associate Professionals", "url": ""},
                {"title": "Financial and Mathematical Associate Professionals", "nco_code": "3311", "category": "Technicians and Associate Professionals", "url": ""},
                {"title": "Sales and Purchasing Agents", "nco_code": "3322", "category": "Technicians and Associate Professionals", "url": ""},
                {"title": "Building and Fire Inspectors", "nco_code": "3123", "category": "Technicians and Associate Professionals", "url": ""},

                # Major Group 4: Clerical Support Workers
                {"title": "General Office Clerks", "nco_code": "4110", "category": "Clerical Support Workers", "url": ""},
                {"title": "Data Entry Clerks", "nco_code": "4132", "category": "Clerical Support Workers", "url": ""},
                {"title": "Bank Tellers and Related Clerks", "nco_code": "4211", "category": "Clerical Support Workers", "url": ""},
                {"title": "Customer Information Clerks", "nco_code": "4221", "category": "Clerical Support Workers", "url": ""},
                {"title": "Accounting and Bookkeeping Clerks", "nco_code": "4311", "category": "Clerical Support Workers", "url": ""},

                # Major Group 5: Service and Sales Workers
                {"title": "Shop Salespersons", "nco_code": "5223", "category": "Service and Sales Workers", "url": ""},
                {"title": "Street and Market Salespersons", "nco_code": "5211", "category": "Service and Sales Workers", "url": ""},
                {"title": "Domestic Cleaners and Helpers", "nco_code": "5152", "category": "Service and Sales Workers", "url": ""},
                {"title": "Cooks", "nco_code": "5120", "category": "Service and Sales Workers", "url": ""},
                {"title": "Waiters and Bartenders", "nco_code": "5131", "category": "Service and Sales Workers", "url": ""},
                {"title": "Personal Care Workers", "nco_code": "5321", "category": "Service and Sales Workers", "url": ""},
                {"title": "Security Guards", "nco_code": "5414", "category": "Service and Sales Workers", "url": ""},
                {"title": "Hairdressers and Beauticians", "nco_code": "5141", "category": "Service and Sales Workers", "url": ""},
                {"title": "Drivers and Mobile Plant Operators", "nco_code": "8322", "category": "Service and Sales Workers", "url": ""},
                {"title": "Call Centre Salespersons (BPO/ITES)", "nco_code": "5244", "category": "Service and Sales Workers", "url": ""},

                # Major Group 6: Skilled Agricultural Workers
                {"title": "Crop Farmers", "nco_code": "6111", "category": "Skilled Agricultural, Forestry and Fishery Workers", "url": ""},
                {"title": "Animal Producers", "nco_code": "6121", "category": "Skilled Agricultural, Forestry and Fishery Workers", "url": ""},
                {"title": "Fishery Workers", "nco_code": "6221", "category": "Skilled Agricultural, Forestry and Fishery Workers", "url": ""},

                # Major Group 7: Craft and Trades Workers
                {"title": "Building Frame and Related Trades Workers", "nco_code": "7112", "category": "Craft and Related Trades Workers", "url": ""},
                {"title": "Electricians", "nco_code": "7411", "category": "Craft and Related Trades Workers", "url": ""},
                {"title": "Plumbers and Pipe Fitters", "nco_code": "7126", "category": "Craft and Related Trades Workers", "url": ""},
                {"title": "Welders and Flame Cutters", "nco_code": "7212", "category": "Craft and Related Trades Workers", "url": ""},
                {"title": "Garment and Related Trades Workers", "nco_code": "7531", "category": "Craft and Related Trades Workers", "url": ""},
                {"title": "Handicraft Workers", "nco_code": "7317", "category": "Craft and Related Trades Workers", "url": ""},
                {"title": "Printing Trades Workers", "nco_code": "7322", "category": "Craft and Related Trades Workers", "url": ""},

                # Major Group 8: Plant and Machine Operators
                {"title": "Motor Vehicle Drivers", "nco_code": "8322", "category": "Plant and Machine Operators and Assemblers", "url": ""},
                {"title": "Two and Three Wheeled Motor Vehicle Drivers", "nco_code": "8321", "category": "Plant and Machine Operators and Assemblers", "url": ""},
                {"title": "Textile and Related Machine Operators", "nco_code": "8151", "category": "Plant and Machine Operators and Assemblers", "url": ""},
                {"title": "Assemblers", "nco_code": "8211", "category": "Plant and Machine Operators and Assemblers", "url": ""},
                {"title": "Mining and Quarrying Machine Operators", "nco_code": "8111", "category": "Plant and Machine Operators and Assemblers", "url": ""},

                # Major Group 9: Elementary Occupations
                {"title": "Agricultural Labourers", "nco_code": "9211", "category": "Elementary Occupations", "url": ""},
                {"title": "Construction Labourers", "nco_code": "9312", "category": "Elementary Occupations", "url": ""},
                {"title": "Domestic Workers and Household Helpers", "nco_code": "9111", "category": "Elementary Occupations", "url": ""},
                {"title": "Street Vendors", "nco_code": "9520", "category": "Elementary Occupations", "url": ""},
                {"title": "Garbage Collectors", "nco_code": "9129", "category": "Elementary Occupations", "url": ""},
                {"title": "Porters and Carriers", "nco_code": "9333", "category": "Elementary Occupations", "url": ""},
                {"title": "Delivery Workers", "nco_code": "9334", "category": "Elementary Occupations", "url": ""},
    ]

    # Add slugs
    for occ in occupations:
                occ["slug"] = slugify(occ["title"])
                if not occ.get("url"):
                                occ["url"] = f"https://www.nqr.gov.in/search?q={occ['title'].replace(' ', '+')}"

            return occupations


def main():
        import os

    # Try to parse from downloaded HTML first
    if os.path.exists("nco_index.html"):
                print("Parsing NCO index from nco_index.html...")
                occupations = parse_nco_index("nco_index.html")
                print(f"Parsed {len(occupations)} occupations from HTML")
else:
        print("nco_index.html not found. Using built-in NCO-2015 occupation list.")
        print("To get more complete data, download the NCO index page:")
        print("  - Visit https://www.nqr.gov.in/ and save the occupation listing as nco_index.html")
        print("  - Or visit https://labour.gov.in/ for the NCO-2015 document")
        occupations = build_default_occupations()
        print(f"Built default list of {len(occupations)} key Indian occupations")

    # Sort by category then title
    occupations.sort(key=lambda x: (x["category"], x["title"]))

    print(f"\nTotal unique occupations: {len(occupations)}")
    print("\n--- Occupations by category ---")
    from collections import Counter
    cats = Counter(o["category"] for o in occupations)
    for cat, count in sorted(cats.items()):
                print(f"  {cat}: {count}")

    print("\n--- First 10 occupations ---")
    for occ in occupations[:10]:
                print(f"  [{occ['nco_code']}] {occ['title']} ({occ['category']})")

    # Save to JSON for further analysis
    with open("occupations.json", "w", encoding="utf-8") as f:
                json.dump(occupations, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(occupations)} occupations to occupations.json")


if __name__ == "__main__":
        main()
