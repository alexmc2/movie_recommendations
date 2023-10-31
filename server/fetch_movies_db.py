import mysql.connector
from dotenv import dotenv_values

config = dotenv_values(".env")


def fetch_movie_from_db_by_imdb_id(imdb_id):
    try:
        conn = mysql.connector.connect(
            host="movies.co6s2as3b2c8.eu-west-2.rds.amazonaws.com",
            user="Alex",
            password=config["DB_PASSWORD"],
            database="movies",
        )
        print("Connected to the database successfully!")

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies WHERE ID = %s;", (imdb_id,))
        print(f"Executed query for IMDb ID: {imdb_id}")
        row = cursor.fetchone()
        if not row:
            print(f"No movie found in the database for IMDb ID: {imdb_id}")
            return None
        movie = {
            "ID": row[0],
            "title": row[1],
            "year": row[2],
            "rating": row[4],
            "description": row[12],
            "imageUrl": row[14],
        }
        print(f"Movie found in the database: {movie}")

        cursor.close()
        conn.close()
        return movie
    except Exception as e:
        print(f"Error fetching movie from database: {e}")
        return None


# Test the function
result = fetch_movie_from_db_by_imdb_id("tt0110357")
print(result)


# import mysql.connector
# from dotenv import dotenv_values

# config = dotenv_values("../.env")
# print("Starting the script...")


# try:
#     conn = mysql.connector.connect(
#         host="movies.co6s2as3b2c8.eu-west-2.rds.amazonaws.com",
#         user="Alex",
#         password=config["DB_PASSWORD"],
#         database="movies",
#     )
#     print("Connected to the database successfully!")
#     conn.close()
# except Exception as e:
#     print(f"Error connecting to the database: {str(e)}")
