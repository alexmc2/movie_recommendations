import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

# this script is used to scrape the plot keywords from IMDB

def get_imdb_keywords(movie_title):
    search_url = f"https://www.imdb.com/find?q={movie_title}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    # Extract the most relevant movie link from the search results
    link = soup.find("a", href=re.compile(r"/title/tt\d+/"))
    if link:
        movie_id = re.search(r"/title/(tt\d+)/", link["href"]).group(1)
        keywords_url = (
            f"https://www.imdb.com/title/{movie_id}/keywords/?ref_=tt_stry_kw"
        )
    else:
        return "Relevant movie link not found in search results"

    keywords_page = requests.get(keywords_url, headers=headers)
    keywords_soup = BeautifulSoup(keywords_page.content, "lxml")

    # Extract plot keywords
    keyword_anchors = keywords_soup.find_all(
        "a", class_="ipc-metadata-list-summary-item__t"
    )

    if keyword_anchors:
        # Extracting all the keywords and joining them into a single string
        keyword_list = [item.get_text(strip=True) for item in keyword_anchors]
        keyword_string = ", ".join(keyword_list)
    else:
        keyword_string = "Plot keywords not found on the movie page"

    return keyword_string


# Read CSV
df = pd.read_csv("./data/imdb03.csv")

# Fetch plot keywords and update dataframe
keywords_list = []
for title in df["Title"]:
    print(f"Fetching plot keywords for {title}...")
    try:
        keywords = get_imdb_keywords(title)
        keywords_list.append(keywords)
    except Exception as e:
        keywords_list.append(f"Error: {str(e)}")
        print(f"Error while fetching plot keywords for {title}: {str(e)}")
    time.sleep(2)  # Sleep for 2 seconds

df["Plot Keywords"] = keywords_list
df.to_csv("./data/updated_movies_with_keywords03.csv", index=False)
