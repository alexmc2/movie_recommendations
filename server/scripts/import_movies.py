import csv

import boto3
import mysql.connector

# Download CSV from S3
s3 = boto3.client("s3")
s3.download_file("movie-app-database", "imdb_full_list.csv", "/tmp/imdb_full_list.csv")

# Connect to MySQL RDS
conn = mysql.connector.connect(
    host="movies.co6s2as3b2c8.eu-west-2.rds.amazonaws.com",
    user="Alex",
)
cursor = conn.cursor()

# Create the database and set it to be used
cursor.execute("CREATE DATABASE IF NOT EXISTS movies")
cursor.execute("USE movies")


# Create table (if not exists)
create_table_query = """
CREATE TABLE IF NOT EXISTS movies (
    ID VARCHAR(255) PRIMARY KEY,
    Title VARCHAR(255),
    Year INT,
    RunTime INT,
    Rating FLOAT,
    Votes INT,
    MetaScore INT,
    Gross BIGINT,
    Genre VARCHAR(255),
    Certification VARCHAR(50),
    Director VARCHAR(255),
    Stars TEXT,
    Description TEXT,
    PlotKeywords TEXT,
    PrimaryImageURL TEXT
);
"""
cursor.execute(create_table_query)

# Insert data from CSV
with open("/tmp/imdb_full_list.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for row in reader:
        cursor.execute(
            "INSERT INTO movies VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            row,
        )

conn.commit()
cursor.close()
conn.close()
