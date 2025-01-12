import requests
import csv

# Constants
ORCID_ID = "0000-0002-1226-1828"  # Replace with your ORCID ID
ACCESS_TOKEN = "your_access_token_here"  # Replace with your ORCID access token
OUTPUT_FILE = "publications.tsv"

# Headers for the API request
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json",
}

# ORCID API URL
API_URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"

# Fetch publications from ORCID
response = requests.get(API_URL, headers=HEADERS)
response.raise_for_status()
works = response.json().get("group", [])

# Extract information for each publication
data = []
for work_group in works:
    work_summary = work_group.get("work-summary", [{}])[0]
    pub_date = "-"  # Default if no date is available
    publication_date = work_summary.get("publication-date")
    if publication_date:
        year = publication_date.get("year", {}).get("value", "")
        month = publication_date.get("month", {}).get("value", "")
        day = publication_date.get("day", {}).get("value", "")
        pub_date = "-".join(filter(None, [year, month, day]))

    title = work_summary.get("title", {}).get("title", {}).get("value", "")
    venue = work_summary.get("journal-title", {}).get("value", "")
    excerpt = work_summary.get("short-description", "")
    citation = work_summary.get("citation", {}).get("citation", "")
    url_slug = work_summary.get("path")
    paper_url = None
    slides_url = None

    for ext_id in work_summary.get("external-ids", {}).get("external-id", []):
        if ext_id.get("external-id-type") == "doi":
            paper_url = f"https://doi.org/{ext_id.get('external-id-value')}"

    data.append({
        "pub_date": pub_date,
        "title": title,
        "venue": venue,
        "excerpt": excerpt,
        "citation": citation,
        "url_slug": url_slug,
        "paper_url": paper_url,
        "slides_url": slides_url,
    })

# Write data to a TSV file
with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "pub_date", "title", "venue", "excerpt", "citation", "url_slug", "paper_url", "slides_url"
    ], delimiter="\t")
    writer.writeheader()
    writer.writerows(data)

print(f"Publications exported to {OUTPUT_FILE}")