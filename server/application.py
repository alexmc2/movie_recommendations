from flask import Flask, jsonify
from flask_cors import CORS

# app instance
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
@app.route("/api/movies", methods=["GET"])
def get_movies():
    # Fetch movies from the database
    movies = [
        # Sample data
        {"title": "Interstellar", "imageUrl": "https://m.media-amazon.com/images/M/MV5BMjA3NTEwOTMxMV5BMl5BanBnXkFtZTgwMjMyODgxMzE@._V1_.jpg"},
       
    ]
    return jsonify(movies)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
