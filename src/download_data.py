import requests
import pandas as pd
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

# Make sure the raw data directory exists
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


def download_world_bank_data(indicator, filename):
    """
    Download South Africa data for a World Bank indicator
    and save it as a CSV file.
    """

    url = (
        f"https://api.worldbank.org/v2/country/ZAF/"
        f"indicator/{indicator}?format=json&per_page=100"
    )

    print(f"\nDownloading: {indicator}")

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    # World Bank API returns metadata followed by records
    records = data[1]

    rows = []

    for record in records:
        rows.append({
            "Country": record["country"]["value"],
            "Country_Code": record["countryiso3code"],
            "Year": int(record["date"]),
            "Value": record["value"]
        })

    df = pd.DataFrame(rows)

    # Sort chronologically
    df = df.sort_values("Year")

    # Save CSV
    output_path = RAW_DATA_DIR / filename
    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")
    print(f"Rows: {len(df)}")

    return df


# Dataset 1: Unemployment
unemployment = download_world_bank_data(
    "SL.UEM.TOTL.ZS",
    "south_africa_unemployment.csv"
)


# Dataset 2: Tertiary education enrolment
education = download_world_bank_data(
    "SE.TER.ENRR",
    "south_africa_tertiary_education.csv"
)


print("\n======================================")
print("DATA DOWNLOAD COMPLETED")
print("======================================")

print("\nUnemployment:")
print(unemployment.head())

print("\nTertiary Education:")
print(education.head())