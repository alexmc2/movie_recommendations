import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_imdb_storyline(movie_title):
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
        storyline_url = f"https://www.imdb.com/title/{movie_id}/"
    else:
        return "Relevant movie link not found in search results"

    storyline_page = requests.get(storyline_url, headers=headers)
    storyline_soup = BeautifulSoup(storyline_page.content, "lxml")

    # Extract storyline
    storyline_div = storyline_soup.find(
        "div", {"data-testid": "storyline-plot-summary"}
    )
    if storyline_div:
        storyline_text = storyline_div.text.strip()
        storyline_text = storyline_text.split("—")[0].strip()  # Remove author's name
        return storyline_text
    else:
        return "Storyline not found on the movie page"


# Read CSV
df = pd.read_csv("./test.csv")

# Fetch storyline and update dataframe
storyline_list = []
for title in df["Title"]:
    print(f"Fetching storyline for {title}...")
    try:
        storyline = get_imdb_storyline(title)
        storyline_list.append(storyline)
    except Exception as e:
        storyline_list.append(f"Error: {str(e)}")
        print(f"Error while fetching storyline for {title}: {str(e)}")
    time.sleep(2)  # Sleep for 2 seconds to avoid rate limiting

df["Storyline"] = storyline_list
df.to_csv("./test.csv", index=False)
