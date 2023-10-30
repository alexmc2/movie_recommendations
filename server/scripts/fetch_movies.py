import mysql.connector
from dotenv import dotenv_values

config = dotenv_values(".env")

# Connect to MySQL RDS
conn = mysql.connector.connect(
    host="movies.co6s2as3b2c8.eu-west-2.rds.amazonaws.com",
    user="Alex",
    password=config["DB_PASSWORD"],
    database="movies",
)
cursor = conn.cursor()

# Fetch the first 10 rows
cursor.execute("SELECT * FROM movies LIMIT 10;")
rows = cursor.fetchall()

# Print the rows
for row in rows:
    print(row)

cursor.close()
conn.close()
