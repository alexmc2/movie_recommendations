import mysql.connector
from dotenv import dotenv_values

config = dotenv_values(".env")


def fetch_movie_from_db_by_title(movie_title):
    conn = mysql.connector.connect(
        host="movies.co6s2as3b2c8.eu-west-2.rds.amazonaws.com",
        user="Alex",
        password=config["DB_PASSWORD"],
        database="movies",
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE title = %s;", (movie_title,))
    row = cursor.fetchone()
    if not row:
        print(f"No movie found in the database for title: {movie_title}")
    movie = {
        "ID": row[0],
        "title": row[1],
        "year": row[2],
        "rating": row[4],
        "description": row[12],
        "imageUrl": row[14],
    }
    cursor.close()
    conn.close()
    return movie
