import chromadb
import openai
from dotenv import dotenv_values
from embeddings import get_embedding

# Load environment variables
config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

# Setup Chroma client for local access
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection_name = "movie_embeddings"
collection = chroma_client.get_or_create_collection(name=collection_name)


def insert_movie(movie_data):
    # Generate an embedding for the movie description
    movie_embedding = get_embedding(
        movie_data["Description"], engine="text-embedding-ada-002"
    )
    # Prepare the document to be inserted
    document = {"document": movie_data, "embedding": movie_embedding.tolist()}
    # Insert the document into the collection
    collection.insert(document)


def search_movies(query_description, n=3):
    query_embedding = get_embedding(query_description, engine="text-embedding-ada-002")
    results = collection.query(query_embeddings=[query_embedding.tolist()], n_results=n)
    movies = [
        {
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
        }
        for res in results
    ]
    return movies


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
