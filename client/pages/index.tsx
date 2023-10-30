import React from 'react';
import ImageCard from '../components/ImageCard';
import MovieBot from '../components/MovieBot';

function Index({ movies, displayedMovies }) {
  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 m-8 gap-0 ">
        {displayedMovies &&
          displayedMovies.length > 0 &&
          displayedMovies.map((movie) => (
            <ImageCard
              key={movie.ID} // Use the unique ID as the key
              title={movie.title}
              imageUrl={movie.imageUrl}
              description={movie.description}
              year={movie.year}
              rating={movie.rating}
            />
          ))}
      </div>
    </div>
  );
}


export default Index;
