import re

import chromadb
import openai
from dotenv import dotenv_values
from embeddings import get_embedding

# Load environment variables
config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

# Setup Chroma client for local access
chroma_client = chromadb.PersistentClient(path="./chroma")
collection_name = "movie_embeddings"
collection = chroma_client.get_or_create_collection(name=collection_name)


def insert_movie(movie_data):
    # Generate an embedding for the movie description
    movie_embedding = get_embedding(
        movie_data["Description"], model="text-embedding-ada-002"
    )
    # Prepare the document to be inserted
    document = {"document": movie_data, "embedding": movie_embedding.tolist()}
    # Insert the document into the collection
    collection.insert(document)


def search_movies(query_description, n=3):
    query_embedding = get_embedding(query_description, model="text-embedding-ada-002")
    results = collection.query(query_embeddings=[query_embedding.tolist()], n_results=n)

    movie_titles = [res["document"]["Title"] for res in results]
    movie_imdb_ids = [res["document"]["ID"] for res in results]

    movies = [
        {
            "id": res["document"]["ID"],
            "title": res["document"]["Title"],
            "year": str(res["document"]["Year"]),
            "runtime": res["document"]["Run Time"],
            "rating": res["document"]["Rating"],
            "votes": res["document"]["Votes"],
            "metascore": res["document"]["MetaScore"],
            "gross": res["document"]["Gross"],
            "genre": res["document"]["Genre"],
            "certification": res["document"]["Certification"],
            "director": res["document"]["Director"],
            "stars": res["document"]["Stars"],
            "description": res["document"]["Description"],
            "plot_keywords": res["document"]["Plot Keywords"],
            "imageUrl": res["document"]["Image URL"],
        }
        for res in results
    ]

    return movie_titles, movie_imdb_ids, movies


def moviebot_chat(user_msg):
    messages = [
        {
            "role": "system",
            "content": "You are a conversational chatbot. Your personality is: extremely grumpy and annoyed",
        }
    ]
    messages.append({"role": "user", "content": user_msg})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    return response.choices[0].message["content"]

    # Extract IMDb IDs from the bot message
    # imdb_ids = re.findall(r"tt\d+", bot_msg)

    # return bot_msg, imdb_ids
