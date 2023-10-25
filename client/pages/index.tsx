import React, { useEffect, useState } from 'react';
import ImageCard from '../components/ImageCard';

function Index() {
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
        />
      ))}
    </div>
  );
}

export default Index;
