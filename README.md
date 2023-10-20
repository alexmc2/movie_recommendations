# Movie Generator

![In Progress](https://img.shields.io/badge/Status-In%20Progress-yellow)

This repo is the early stages of a movie recommendation app that will use OpenAI's embeddings to calculate relatedness between films and make recommendations based on them

The backend will be built with Python (Flask), and Vite will be used for the frontend. I'll be using Chroma to store the embeddings due to it's easy integration with OpenAi.

The app will be deployed using AWS.

I've collected and embedded the movie data (IMDB's top 10,000) into the Chroma vector database and I'm about to start building the backend.

Here's an interesting 2D visualisation of the embeddings created by OpenAI's text-embedding-ada-002 model. This graph represents the top 10,000 films on IMDB which have been clustered together based on relatedness between the films.

![Screenshot1](https://user-images.githubusercontent.com/119585058/276747742-863f7472-28fe-498b-ba43-cde8429f6f24.png)

[https://atlas.nomic.ai/map/503f6783-82d0-4ce8-88a1-a4c3f1c90bc0/748c4f9e-8e10-40d8-858d-e83af1e2bb6b?xs=-28.13648&xf=53.89644&ys=-27.22295&yf=26.12872](https://atlas.nomic.ai/map/503f6783-82d0-4ce8-88a1-a4c3f1c90bc0/748c4f9e-8e10-40d8-858d-e83af1e2bb6b?xs=-28.13648&xf=53.89644&ys=-27.22295&yf=26.12872)

The app will feature a "Moviebot" that uses the embeddings in its film recommendations. It will also include admin functionality to insert new films into the database. 

![Screenshot1](https://user-images.githubusercontent.com/119585058/276906109-1bdb1e3a-eeb9-4545-980f-480eb7c37e5f.png)
