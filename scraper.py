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
        movie_link = link["href"]
    else:
        return "Relevant movie link not found in search results"

    movie_page = requests.get(f"https://www.imdb.com{movie_link}", headers=headers)
    movie_soup = BeautifulSoup(movie_page.content, "lxml")

    # Extract storyline
    storyline_div = movie_soup.find("div", class_="ipc-overflowText--children")
    if storyline_div:
        storyline = storyline_div.find(
            "div", class_="ipc-html-content-inner-div"
        ).get_text(strip=True)
    else:
        storyline = "Storyline not found on the movie page"

    return storyline


# Read CSV
df = pd.read_csv("imdbtest.csv")

# Fetch storylines and update dataframe
storylines = []
for title in df["Title"]:
    print(f"Fetching storyline for {title}...")
    try:
        storyline = get_imdb_storyline(title)
        storylines.append(storyline)
    except Exception as e:
        storylines.append(f"Error: {str(e)}")
        print(f"Error while fetching storyline for {title}: {str(e)}")
    time.sleep(2)  # Sleep for 2 seconds

df["Storyline"] = storylines
df.to_csv("updated_movies_with_storyline.csv", index=False)
