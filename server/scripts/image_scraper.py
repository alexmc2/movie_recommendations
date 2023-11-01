import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

# script for scraping images from imdb website

def get_imdb_image(movie_title, year):
    search_url = f"https://www.imdb.com/find?q={movie_title}+{year}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    # Extract the most relevant movie link from the search results
    link = soup.find("a", href=re.compile(r"/title/tt\d+/"))

    if not link:
        return "Relevant movie link not found in search results"

    movie_id = re.search(r"/title/(tt\d+)/", link["href"]).group(1)
    image_url = f"https://www.imdb.com/title/{movie_id}/mediaviewer/"

    image_page = requests.get(image_url, headers=headers)
    image_soup = BeautifulSoup(image_page.content, "lxml")

    # Extract primary image URL
    image_tags = image_soup.select(
        "div.sc-7c0a9e7c-2.kEDMKk img, div.sc-7c0a9e7c-3.lhANrx img"
    )
    if image_tags:
        return image_tags[0]["src"]

    return "Primary image not found on the movie page"


# Read CSV
df = pd.read_csv("./data/imdb_full_list.csv")

# Fetch primary images and update dataframe
image_list = []
for index, row in df.iterrows():
    title = row["Title"]
    year = row["Year"]
    existing_image_url = row.get("Primary Image URL", "")

    # Skip if image URL is already present
    if pd.notna(existing_image_url) and "http" in existing_image_url:
        image_list.append(existing_image_url)
        continue

    print(f"Fetching primary image for {title} ({year})...")
    try:
        image_url = get_imdb_image(title, year)
        image_list.append(image_url)
    except Exception as e:
        image_list.append(f"Error: {str(e)}")
        print(f"Error while fetching primary image for {title} ({year}): {str(e)}")
    time.sleep(2)  # Sleep for 2 seconds to avoid rate limiting

df["Primary Image URL"] = image_list
df.to_csv("./data/imdb_full_list.csv", index=False)
