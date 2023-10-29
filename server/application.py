import json

import openai
from dotenv import dotenv_values
from fetch_movies_db import fetch_movie_from_db_by_title
from flask import Flask, Response, jsonify, request, stream_with_context
from flask_cors import CORS
from moviebot import insert_movie, moviebot_chat, search_movies

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

app = Flask(__name__)
CORS(app)


# /api/home
@app.route("/api/home", methods=["GET"])
def return_home():
    return jsonify(
        {
            "message": "Hello World!",
        }
    )


# /api/movies
# @app.route("/api/movies", methods=["GET"])
# def get_movies():
# Fetch movies from the database
# hardcoded movies for testing
# movies = [
#     {
#         "title": "Interstellar",
#         "imageUrl": "https://m.media-amazon.com/images/M/MV5BMjA3NTEwOTMxMV5BMl5BanBnXkFtZTgwMjMyODgxMzE@._V1_.jpg",
#         "description": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.",
#         "rating": "8.6",
#         "year": "2014",
#     },
#     {
#         "title": "A Beautiful Mind",
#         "imageUrl": "https://m.media-amazon.com/images/M/MV5BZTY1NTZhNDUtMzIzZC00YjgzLTlhMzEtYWUzM2U1NzIzZWI3XkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_.jpg",
#         "description": "After John Nash, a brilliant but asocial mathematician, accepts secret work in cryptography, his life takes a turn for the nightmarish.",
#         "rating": "8.2",
#         "year": "2001",
#     },
#     {
#         "title": "The Terminator",
#         "imageUrl": "https://m.media-amazon.com/images/M/MV5BMjAyMTk3ODA2MF5BMl5BanBnXkFtZTcwMTkzNDQyNA@@._V1_.jpg",
#         "description": "A human soldier is sent from 2029 to 1984 to stop an almost indestructible cyborg killing machine, sent from the same year, which has been programmed to execute a young woman whose unborn son is the key to humanity's future salvation.",
#         "rating": "8.1",
#         "year": "1984",
#     },
#     {
#         "title": "Solaris",
#         "imageUrl": "https://m.media-amazon.com/images/M/MV5BMTQ5NjczMDg0N15BMl5BanBnXkFtZTgwMzIyOTIwOTE@._V1_.jpg",
#         "description": "A psychologist is sent to a station orbiting a distant planet in order to discover what has caused the crew to go insane.",
#         "rating": "8.0",
#         "year": "1972",
#     },
#     {
#         "title": "Gattaca",
#         "imageUrl": "https://m.media-amazon.com/images/M/MV5BMTY4MDAzNTI1MF5BMl5BanBnXkFtZTcwODkwODYyNA@@._V1_.jpg",
#         "description": "A genetically inferior man assumes the identity of a superior one in order to pursue his lifelong dream of space travel.",
#         "rating": "7.7",
#         "year": "1997",
#     },
#     {
#         "title": "Gravity",
#         "imageUrl": "https://m.media-amazon.com/images/M/MV5BMTQ1NzcyODEwMl5BMl5BanBnXkFtZTgwNTQ4MjQ3MDE@._V1_.jpg",
#         "description": "Two astronauts work together to survive after an accident leaves them stranded in space.",
#         "rating": "7.7",
#         "year": "2013",
#     },
#     {
#         "title": "Contact",
#         "imageUrl": "https://m.media-amazon.com/images/M/MV5BMTQ1NzcyODEwMl5BMl5BanBnXkFtZTgwNTQ4MjQ3MDE@._V1_.jpg",
#         "description": "Dr. Ellie Arroway, after years of searching, finds conclusive radio proof of extraterrestrial intelligence, sending plans for a mysterious machine.",
#         "rating": "7.5",
#         "year": "1997",
#     },
#     {
#         "title": "Blade Runner",
#         "imageUrl": "https://m.media-amazon.com/images/M/MV5BNzQzMzJhZTEtOWM4NS00MTdhLTg0YjgtMjM4MDRkZjUwZDBlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg",
#         "description": "In the futuristic year of 2019, Los Angeles has become a dark and depressing metropolis, filled with urban decay.",
#         "rating": "8.1",
#         "year": "1982",
#     },
#     {
#         "title": "The Matrix",
#         "imageUrl": "https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg",
#         "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
#         "rating": "8.7",
#         "year": "1999",
#     },
#     {
#         "title": "Inception",
#         "imageUrl": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg",
#         "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.",
#         "rating": "8.8",
#         "year": "2010",
#     },
# ]

# return jsonify(movies)


@app.route("/api/movies", methods=["GET"])
def get_movies():
    # Instead of hardcoded movies, fetch the recommended movies from the movie bot
    user_msg = "Recommend me some movies"  # You can customize this message
    bot_msg = moviebot_chat(user_msg)
    print("MovieBot Response:", bot_msg)
    recommended_movie_titles = []

    if "search_movies:" in bot_msg:
        query = bot_msg.split("search_movies:")[-1].strip()
        recommended_movies_from_embeddings = search_movies(query, n=3)
        for movie in recommended_movies_from_embeddings:
            title = movie["title"]
            recommended_movie_titles.append(title)

    recommended_movies = [
        fetch_movie_from_db_by_title(title) for title in recommended_movie_titles
    ]
    print("Recommended Movies:", recommended_movies)
    return jsonify(recommended_movies)



@app.route("/api/moviebot", methods=["POST"])
def moviebot():
    user_msg = request.json.get("message")
    bot_msg = moviebot_chat(user_msg)

    recommended_movie_titles = []

    # Check if the bot wants to search movies using embeddings
    if "search_movies:" in bot_msg:
        query = bot_msg.split("search_movies:")[-1].strip()
        recommended_movies_from_embeddings = search_movies(query, n=3)
        bot_msg = "Here are some movie recommendations based on your query:\n"
        for movie in recommended_movies_from_embeddings:
            title = movie["title"]
            recommended_movie_titles.append(title)
            bot_msg += f"\nTitle: {title} ({movie['year']})"
            bot_msg += f"\nDescription: {movie['description']}\n"

    # Fetch movies from the database using the titles
    recommended_movies = [
        fetch_movie_from_db_by_title(title) for title in recommended_movie_titles
    ]

    return jsonify({"bot_msg": bot_msg, "recommended_movies": recommended_movies})


@app.route("/api/insert_movie", methods=["POST"])
def insert_movie_endpoint():
    movie_data = request.json
    insert_movie(movie_data)
    return jsonify({"message": "Movie inserted successfully!"})


if __name__ == "__main__":
    app.run(debug=True, port=8080)
