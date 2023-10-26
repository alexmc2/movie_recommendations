import React, { useEffect, useState } from 'react';
import ImageCard from '../components/ImageCard';

function Cards() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8080/api/movies')
      .then((response) => response.json())
      .then((data) => {
        setMovies(data);
      });
  }, []);

  return (
    <div>
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
  );
}

export default Cards;
