import React, { useEffect, useState } from 'react';
import ImageCard from '../components/ImageCard';
import MovieBot from '../components/MovieBot';

function Index() {
  const [movies, setMovies] = useState([]);

  const fetchMovies = () => {
    fetch('http://localhost:8080/api/movies')
      .then((response) => response.json())
      .then((data) => {
        setMovies(data);
      });
  };

  useEffect(() => {
    fetchMovies();
  }, []);

  return (
    <div>
      <MovieBot title="MovieBot" movies={movies} />
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 m-8 gap-0 ">
        {movies.map((movie) => (
          <ImageCard
            key={movie.title}
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
