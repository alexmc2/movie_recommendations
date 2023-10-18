import openai
from dotenv import dotenv_values
import numpy as np
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_random_exponential
import tiktoken

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

dataset_path = "./imdb.csv"

df = pd.read_csv(dataset_path)

movies = df.sort_values("Description", ascending=False)

print(movies)

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(5))

def get_embedding(text, model='text-embedding-ada-002'):

    text = text.replace('\n', ' ')
    
    return openai.Embedding.create(input=text, model=model)["data"][0]["embedding"]
