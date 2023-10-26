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
  );
}

export default Index;
