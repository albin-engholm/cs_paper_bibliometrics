import requests
import pandas as pd
import matplotlib.pyplot as plt

# List of keywords
keywords = [
    "systems engineering",
    "system dynamics",
    "engineering systems",
    "systemic design",
    "soft systems methodology",
    "systems thinking",
    "complex adaptive systems",
    "transition research",
    "strategic niche management",
    "strategic transition management",
    "exploratory modeling",
    "life-cycle optimization",
    "operations research",
    "transport policy analysis"
]

# Base API endpoint for group_by queries
BASE_URL = "https://api.openalex.org/works"

# Function to fetch publication year counts using group_by
def fetch_publication_counts(keyword,journal_only=False):
    journal_only=journal_only
    if journal_only:
        params = {
            "search": keyword,
            "group_by": "publication_year",
            "mailto": "your_email@example.com",
            "filter": "primary_location.source.type:journal"

        }

    else:
        params = {
            "search": keyword,
            "group_by": "publication_year",
            "mailto": "your_email@example.com"
        }
    r = requests.get(BASE_URL, params=params)
    data = r.json()
    
    counts = {}
    try:
        for item in data["group_by"]:
            year = str(item["key"])
            counts[year] = item["count"]
    except Exception as e:
        print(f"Failed to parse group_by results for '{keyword}'. Error: {e}. Raw response: {data}")
    
    return counts


# Collect all results
all_data = {}
for kw in keywords:
    print(f"Processing: {kw}")
    all_data[kw] = fetch_publication_counts(kw)

# Create DataFrame
all_years = sorted({year for d in all_data.values() for year in d})
df = pd.DataFrame(index=all_years)
for kw, counts in all_data.items():
    df[kw] = [counts.get(year, 0) for year in all_years]
#%%
# Convert index to numeric and sort
df.index = pd.to_numeric(df.index)
df.sort_index(inplace=True)
df_complete = df.copy()
df = df[(df.index>1899) & (df.index<2024)]
# Plot results
plt.figure(figsize=(14, 8))
for column in df.columns:
    plt.plot(df.index, df[column], label=column)
plt.xlabel("Year")
plt.ylabel("Number of Publications")
plt.title("Publication Trends in OpenAlex by Keyword")
plt.legend(loc="upper left", fontsize="small")
plt.grid(True)
plt.tight_layout()

# Show and export
plt.show()
df.to_csv("openalex_keyword_trends_by_year.csv")
df.tail()

# %%
