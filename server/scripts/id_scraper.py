import re
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_imdb_id(movie_title, year):
    search_url = f"https://www.imdb.com/find?q={movie_title}+{year}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    # Extract the most relevant movie link from the search results
    link = soup.find("a", href=re.compile(r"/title/tt\d+/"))
    if link:
        movie_id = re.search(r"/title/(tt\d+)/", link["href"]).group(1)
        return movie_id
    else:
        return "Movie ID not found"

# Read CSV
df = pd.read_csv("../data/imdb_full_list.csv")

# Fetch IMDb IDs and replace the "Index" column
id_list = []
for index, row in df.iterrows():
    title = row["Title"]
    year = row["Year"]
    print(f"Fetching IMDb ID for {title} ({year})...")
    try:
        movie_id = get_imdb_id(title, year)
        id_list.append(movie_id)
    except Exception as e:
        id_list.append(f"Error: {str(e)}")
        print(f"Error while fetching IMDb ID for {title} ({year}): {str(e)}")
    time.sleep(2)  # Sleep for 2 seconds to avoid rate limiting

df["Index"] = id_list
df.to_csv("../data/imdb_full_list.csv", index=False)
