# Movie Generator

![In Progress](https://img.shields.io/badge/Status-In%20Progress-yellow)

This repo is the early stages of a movie recommendation app that will use OpenAI's embeddings to calculate relatedness between films and make recommendations based on them

The backend will be built with Python (Flask), and ~~Vite~~ Next.js will be used for the frontend. I'll be using Chroma to store the embeddings due to it's easy integration with OpenAI.

The app will be deployed using AWS.

I've collected and embedded the movie data (IMDB's top 10,000) into the Chroma vector database.

Here's an interesting 2D visualisation of the embeddings created by OpenAI's text-embedding-ada-002 model. This graph represents the top 10,000 films on IMDB which have been clustered together based on relatedness between the films.

![Screenshot1](https://user-images.githubusercontent.com/119585058/276747742-863f7472-28fe-498b-ba43-cde8429f6f24.png)

[https://atlas.nomic.ai/map/503f6783-82d0-4ce8-88a1-a4c3f1c90bc0/748c4f9e-8e10-40d8-858d-e83af1e2bb6b?xs=-28.13648&xf=53.89644&ys=-27.22295&yf=26.12872](https://atlas.nomic.ai/map/503f6783-82d0-4ce8-88a1-a4c3f1c90bc0/748c4f9e-8e10-40d8-858d-e83af1e2bb6b?xs=-28.13648&xf=53.89644&ys=-27.22295&yf=26.12872)

The app will feature a "Moviebot" that uses the embeddings in its film recommendations. It will also include admin functionality to insert new films into the database. 

![Screenshot2](https://user-images.githubusercontent.com/119585058/276906109-1bdb1e3a-eeb9-4545-980f-480eb7c37e5f.png)

~~I am currently designing the UI. The Moviebot chat interface will sit on the left and the image cards will be returned on the right (desktop). This is dummy data but the finished app will return the films from Amazon RDS (SQL database).~~


![Screenshot3](https://user-images.githubusercontent.com/119585058/278186451-2ea44a36-21bd-4a02-bd04-42ce76390340.png)


After a lot of trial and error (so many errors), I've finally managed to get the data flow through the app working as intended:


The user sends a message to the chatbot asking for a film recommendation. 

The chatbot responds with movie recommendations in textual format.

The chatbot uses both the embeddings and Open AI chat functionality in the response. These embeddings are stored in ChromaDB, a vector database. 

The system extracts the unique ID from the response (this is hidden from the user).

Using the extracted ID, the system fetches the film data from an Amazon RDS SQL database where the data is also stored. This process is triggered by the user pressing "Show Movies!"

The frontend displays this data in the form of image cards. 



![Screenshot3](https://user-images.githubusercontent.com/119585058/279502721-62841024-05f7-4623-a973-d29bede792db.png)



There are still a lot of refinements and tweaking needed before it can be deployed. The moviebot itself needs some work in terms of how it's using the embedded data in the response, for example, and some design issues still need to be addressed. I'm pleased with how the app is progressing so far, though. :D