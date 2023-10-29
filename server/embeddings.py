from typing import Dict, List

import chromadb
import numpy as np
import openai
import pandas as pd
import tiktoken
from dotenv import dotenv_values

# from nomic import atlas  # comment out atlas code
from tenacity import retry, stop_after_attempt, wait_random_exponential

# Load environment variables
config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

# Initialize ChromaDB in Persistent Mode
chroma_client = chromadb.PersistentClient(path="./chroma")

# Create or get the movie embeddings collection
collection_name = "film_embeddings"
collection = chroma_client.get_or_create_collection(name=collection_name)


# Load the CSV file
def load_movie_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def extract_embedding_text(movie: pd.Series) -> str:
    # Check if "Plot Keywords" is a string
    if isinstance(movie["Plot Keywords"], str):
        # Extract and weight the plot keywords
        keywords = movie["Plot Keywords"].split(",")

        weighted_keywords = []
        weights = [4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2] + [1] * (
            len(keywords) - 15
        )

        for keyword, weight in zip(keywords, weights):
            weighted_keywords.extend([keyword.strip()] * weight)

        # Replace the original keywords with the weighted ones
        movie["Plot Keywords"] = " ".join(weighted_keywords)
    else:
        # If "Plot Keywords" is not a string, provide a default value or skip
        movie["Plot Keywords"] = ""

    # Join all movie attributes to form the embedding text
    return " ".join(map(str, movie.values))


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(5))
def get_embedding(text: str, model="text-embedding-ada-002") -> List[float]:
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=text, model=model)["data"][0]["embedding"]


def compute_and_store_movie_embeddings(movies: pd.DataFrame) -> Dict[str, List[float]]:
    embeddings = {}
    metadata = {}  # Store the entire movie data as metadata

    for _, movie in movies.iterrows():
        # Check if the movie unique ID already exists in the collection
        existing_embedding = collection.get(ids=[movie["ID"]])
        print(f"Existing embedding for {movie['ID']}:", existing_embedding)
        if existing_embedding["ids"]:  # Check if the 'ids' list is not empty
            print(f"Embedding for '{movie['Title']}' already exists. Skipping...")
            continue

        print(f"Generating embedding for '{movie['Title']}'...")
        text = extract_embedding_text(movie)
        embedding = get_embedding(text)
        embeddings[movie["ID"]] = embedding
        metadata[movie["ID"]] = movie.to_dict()

        # Add the embedding to Chroma collection
        collection.add(
            documents=[movie["Title"]], embeddings=[embedding], ids=[movie["ID"]]
        )

    return embeddings, metadata


# Calculate the cost of embedding using tiktoken
def calculate_embedding_cost(texts: List[str]) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    total_tokens = sum(len(encoding.encode(text)) for text in texts)
    return total_tokens


def convert_floats_to_strings(data_dict):
    return {k: str(v) if isinstance(v, float) else v for k, v in data_dict.items()}


if __name__ == "__main__":
    print("Loading movie data...")
    movies = load_movie_data("./data/imdb_full_list.csv")

    print("Computing and storing movie embeddings...")
    film_embeddings, movie_metadata = compute_and_store_movie_embeddings(movies)

    print(f"Number of embeddings: {len(film_embeddings)}")

    embeddings_list = list(film_embeddings.values())

    # Create the data list with floats converted to strings
    data = [
        {
            "ID": movie_metadata[movie_id]["ID"],
            "Title": movie_metadata[movie_id]["Title"],
            **convert_floats_to_strings(movie_metadata[movie_id]),
        }
        for movie_id in film_embeddings.keys()
    ]

    # Comment out atlas code
    # project = atlas.map_embeddings(
    #     embeddings=np.array(embeddings_list), data=data, id_field="ID"
    # )

    # Calculate the cost of embeddings
    embedding_texts = [extract_embedding_text(movie) for _, movie in movies.iterrows()]
    total_cost = calculate_embedding_cost(embedding_texts)
    print(f"Total cost of embeddings: {total_cost} tokens")
