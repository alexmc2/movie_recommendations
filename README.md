# Movie Generator

![In Progress](https://img.shields.io/badge/Status-In%20Progress-yellow)

This repo is the ~~early~~ middle stages of a movie recommendation app that uses OpenAI's embeddings to calculate relatedness between films and make recommendations based on them.

I was inspired to make this app while watching a Colt Steel Udemy tutorial on OpenAI text embeddings where a sample of film data was used for demonstration purposes. I thought it would be a fun and interesting challenge to expand on this idea with a much larger dataset and a frontend user interface. I used scripts to collect the data for the top 10,000 films on IMDB and embedded this into the vector database using OpenAI's text-embedding-ada-002 model. 

The backend is built with Python (Flask), and ~~Vite~~ Next.js is used for the frontend. I've also created an Amazon RDS SQL database to store the film data, and this is used to make image cards on the frontend for each film recommendation. 

The app will also be deployed using AWS.  

Here's an interesting 2D visualisation of the embeddings created by the text-embedding-ada-002 model. This graph represents the top 10,000 films on IMDB which have been clustered together based on relatedness between the films.

![Screenshot1](https://user-images.githubusercontent.com/119585058/276747742-863f7472-28fe-498b-ba43-cde8429f6f24.png)

[https://atlas.nomic.ai/map/503f6783-82d0-4ce8-88a1-a4c3f1c90bc0/748c4f9e-8e10-40d8-858d-e83af1e2bb6b?xs=-28.13648&xf=53.89644&ys=-27.22295&yf=26.12872](https://atlas.nomic.ai/map/503f6783-82d0-4ce8-88a1-a4c3f1c90bc0/748c4f9e-8e10-40d8-858d-e83af1e2bb6b?xs=-28.13648&xf=53.89644&ys=-27.22295&yf=26.12872)

The app will feature a "Moviebot" that uses the embeddings in its film recommendations. It will also include admin functionality to insert new films into the database. 

![Screenshot2](https://user-images.githubusercontent.com/119585058/276906109-1bdb1e3a-eeb9-4545-980f-480eb7c37e5f.png)

~~I am currently designing the UI. The Moviebot chat interface will sit on the left and the image cards will be returned on the right (desktop). This is dummy data but the finished app will return the films from Amazon RDS.~~


![Screenshot3](https://user-images.githubusercontent.com/119585058/278186451-2ea44a36-21bd-4a02-bd04-42ce76390340.png)


After a lot of trial and error (many, many errors), I've finally managed to get the data flow through the app working as intended:


-The user sends a message to the chatbot asking for a film recommendation. 

-The chatbot responds with movie recommendations in textual format.

-The chatbot uses both the embeddings and Open AI chat functionality in the response. These embeddings are stored in ChromaDB, a vector database. 

-The system extracts the unique ID from the response (this is hidden from the user).

-Using the extracted ID, the system fetches the film data from an Amazon RDS SQL database where the data is also stored. This process is triggered by the user pressing "Show     Movies!"

-The frontend displays this data in the form of image cards. 




![Screenshot3](https://user-images.githubusercontent.com/119585058/279509607-19bcab58-0477-4956-960f-3e07f92c0351.png)


![Screenshot3](https://user-images.githubusercontent.com/119585058/279548280-87504e1b-798c-4fd4-b82c-5630aead831c.png)





There are still a lot of refinements and tweaking needed before it can be deployed. The moviebot itself needs some work in terms of how it's using the embedded data in the response, for example, and some design issues still need to be addressed. I'm now researching fine tuning for LLMs with a view to implementing this in my app and creating a chatbot film expert. I'm overall very pleased with how the app is progressing so far. :D