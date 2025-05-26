import os
import requests
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from dotenv import load_dotenv
#%%
# Read API key from local dotenv and set base URL
load_dotenv()
API_KEY = os.getenv("SCOPUS_API_KEY")
if not API_KEY:
    raise EnvironmentError("SCOPUS_API_KEY not set. Please set it as an environment variable.")

BASE_URL = "https://api.elsevier.com/content/search/scopus"

# %%Define your list of search terms
search_terms = [
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
#%%
# Query each term and count publication years
results = {}
for term in search_terms:
    print(f"Querying: {term}")
    all_years = []
    start = 0
    while True:
        params = {
            "query": f'TITLE-ABS-KEY("{term}")',
            "apiKey": API_KEY,
            "count": 25,
            "start": start
        }
        headers = {"Accept": "application/json"}
        r = requests.get(BASE_URL, headers=headers, params=params)
        data = r.json()
        
        entries = data.get("search-results", {}).get("entry", [])
        if not entries:
            break
        for entry in entries:
            date = entry.get("prism:coverDate", "")
            if date:
                year = date[:4]
                all_years.append(year)
        
        start += 25
        if start >= int(data["search-results"]["opensearch:totalResults"]):
            break

    year_counts = Counter(all_years)
    results[term] = year_counts

# Convert to DataFrame
years = sorted({year for counts in results.values() for year in counts})
df = pd.DataFrame(index=years)
for term, counts in results.items():
    df[term] = [counts.get(year, 0) for year in years]

# Convert index to numeric and sort
df.index = pd.to_numeric(df.index)
df.sort_index(inplace=True)

# Plot
plt.figure(figsize=(14, 8))
for column in df.columns:
    plt.plot(df.index, df[column], label=column)
plt.xlabel("Year")
plt.ylabel("Number of Publications")
plt.title("Publication Trends in Scopus by Keyword")
plt.legend(loc="upper left", fontsize="small")
plt.grid(True)
plt.tight_layout()

# Show and export
plt.show()
df.to_csv("scopus_keyword_trends.csv")
