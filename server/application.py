import json
import re

import openai
from dotenv import dotenv_values
from fetch_movies_db import fetch_movie_from_db_by_imdb_id
from flask import Flask, Response, jsonify, request, stream_with_context
from flask_cors import CORS
from moviebot import insert_movie, moviebot_chat, search_movies

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# /api/home
@app.route("/api/home", methods=["GET"])
def return_home():
    return jsonify(
        {
            "message": "Hello World!",
        }
    )


@app.route("/api/movies", methods=["GET"])
def get_movies():
    movie_imdb_ids = request.args.getlist("imdb_ids")
    movies = [fetch_movie_from_db_by_imdb_id(imdb_id) for imdb_id in movie_imdb_ids]
    return jsonify(movies)


@app.route("/api/moviebot", methods=["POST"])
def moviebot():
    user_msg = request.json.get("message")
    bot_msg = moviebot_chat(user_msg)

    print(f"Chatbot Response: {bot_msg}")  # Print the chatbot's response

    # Check if the bot wants to search movies using embeddings
    if "search_movies:" in bot_msg:
        query = bot_msg.split("search_movies:")[-1].strip()
        recommended_movies_from_embeddings = search_movies(query, n=3)

        # Extract IMDb IDs from the recommended movies
        movie_imdb_ids = [movie["ID"] for movie in recommended_movies_from_embeddings]

        # Fetch detailed movie data using IMDb IDs from the Amazon database
        recommended_movies = [
            fetch_movie_from_db_by_imdb_id(imdb_id) for imdb_id in movie_imdb_ids
        ]

        # Construct a bot message with movie titles
        titles_msg = ", ".join(
            [movie["title"] for movie in recommended_movies if movie]
        )
        bot_response_msg = f"I recommend the following movies: {titles_msg}"
    else:
        # If the bot's response doesn't involve searching movies, use the original bot message
        bot_response_msg = bot_msg
        recommended_movies = []

    return jsonify(
        {"bot_msg": bot_response_msg, "recommended_movies": recommended_movies}
    )


# @app.route("/api/moviebot", methods=["POST"])
# def moviebot():
#     user_msg = request.json.get("message")
#     bot_msg, imdb_ids = moviebot_chat(user_msg)

#     # Fetch detailed movie data using IMDb IDs from the Amazon database
#     recommended_movies = [
#         fetch_movie_from_db_by_imdb_id(imdb_id) for imdb_id in imdb_ids
#     ]

#     # Construct a bot message with movie titles
#     titles_msg = ", ".join(
#         [movie["title"] for movie in recommended_movies if movie]
#     )
#     bot_response_msg = f"I recommend the following movies: {titles_msg}"

#     return jsonify(
#         {"bot_msg": bot_response_msg, "recommended_movies": recommended_movies}
#     )


@app.route("/api/insert_movie", methods=["POST"])
def insert_movie_endpoint():
    movie_data = request.json
    insert_movie(movie_data)
    return jsonify({"message": "Movie inserted successfully!"})


if __name__ == "__main__":
    app.run(debug=True, port=8080)
